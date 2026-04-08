"""Tests for the ExecutionProvider protocol and task/result types (spec 042).

Phase 1 coverage: validates the protocol shape, the structured
``ExecutionTask`` dataclass with A2A-Task-Request-compatible fields, the
``from_prompt()`` compatibility constructor (binding condition #1), the
``ExecutionResult`` dataclass with structured cost/duration/error fields
(binding conditions #4, #5, #6), and the expanded ``ProviderErrorCategory``
Literal (binding condition #4).

These tests do not exercise any real provider implementation — Phase 2 adds
the ``mock``, ``claude-code``, ``opencode``, and ``anthropic`` providers and
their own test suites.  This file covers the type shapes only.
"""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import get_args

import pytest

from engine.execution import (
    Cost,
    Duration,
    ExecutionProvider,
    ExecutionResult,
    ExecutionTask,
    Reference,
    TaskPart,
    TaskPartMediaType,
)
from engine.providers import ProviderError, ProviderErrorCategory


# ---------------------------------------------------------------------------
# ProviderErrorCategory — binding condition #4
# ---------------------------------------------------------------------------


class TestProviderErrorCategoryExpansion:
    """Spec 042 binding condition #4: expand the Literal to 8 values."""

    def test_literal_has_exactly_eight_values(self) -> None:
        """The expanded set covers the full subprocess + HTTP failure matrix."""
        values = set(get_args(ProviderErrorCategory))
        assert values == {
            "auth",
            "rate_limit",
            "server",
            "timeout",
            "subprocess",
            "network",
            "malformed",
            "unknown",
        }

    def test_four_original_categories_still_present(self) -> None:
        """Backward compatibility — no existing category was removed."""
        values = set(get_args(ProviderErrorCategory))
        assert {"auth", "rate_limit", "server", "unknown"}.issubset(values)

    def test_four_new_categories_added(self) -> None:
        """The four new failure modes required by binding condition #4."""
        values = set(get_args(ProviderErrorCategory))
        assert {"timeout", "subprocess", "network", "malformed"}.issubset(values)

    @pytest.mark.parametrize(
        "category",
        ["auth", "rate_limit", "server", "timeout", "subprocess", "network", "malformed", "unknown"],
    )
    def test_provider_error_accepts_every_category(self, category: str) -> None:
        """Every Literal value constructs a valid ``ProviderError``."""
        err = ProviderError("boom", category=category)  # type: ignore[arg-type]
        assert err.category == category
        assert str(err) == "boom"


# ---------------------------------------------------------------------------
# TaskPart and Reference — structured content shapes
# ---------------------------------------------------------------------------


class TestTaskPart:
    def test_default_media_type_is_markdown(self) -> None:
        """Phase templates are markdown by construction — default reflects this."""
        part = TaskPart(content="hello")
        assert part.media_type == "text/markdown"

    def test_frozen_dataclass(self) -> None:
        """Parts are immutable — the engine can safely share references across providers."""
        part = TaskPart(content="hello")
        with pytest.raises(Exception):  # FrozenInstanceError in 3.10+
            part.content = "goodbye"  # type: ignore[misc]

    def test_media_type_literal_closed_set(self) -> None:
        """Only text/plain and text/markdown are valid media types in v1."""
        assert set(get_args(TaskPartMediaType)) == {"text/plain", "text/markdown"}


class TestReference:
    def test_uri_required(self) -> None:
        ref = Reference(uri="/tmp/input.md")
        assert ref.uri == "/tmp/input.md"
        assert ref.description is None

    def test_description_optional(self) -> None:
        ref = Reference(uri="/tmp/input.md", description="input context")
        assert ref.description == "input context"

    def test_frozen_dataclass(self) -> None:
        ref = Reference(uri="/tmp/input.md")
        with pytest.raises(Exception):
            ref.uri = "/tmp/other.md"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ExecutionTask — canonical shape + from_prompt compat constructor
# ---------------------------------------------------------------------------


class TestExecutionTaskCanonical:
    """Canonical A2A-Task-Request-compatible construction."""

    def test_minimal_task_requires_parts_and_output_path(self) -> None:
        task = ExecutionTask(
            parts=(TaskPart(content="review this spec"),),
            output_path="/tmp/out.md",
        )
        assert len(task.parts) == 1
        assert task.parts[0].content == "review this spec"
        assert task.output_path == "/tmp/out.md"
        assert task.references == ()
        assert task.metadata == {}
        assert task.stream is False

    def test_empty_parts_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="at least one part"):
            ExecutionTask(parts=(), output_path="/tmp/out.md")

    def test_empty_output_path_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="output_path"):
            ExecutionTask(
                parts=(TaskPart(content="x"),),
                output_path="",
            )

    def test_references_are_tuple_not_list(self) -> None:
        """Frozen dataclass semantics require hashable collections."""
        task = ExecutionTask(
            parts=(TaskPart(content="x"),),
            output_path="/tmp/out.md",
            references=(Reference(uri="/tmp/a.md"), Reference(uri="/tmp/b.md")),
        )
        assert isinstance(task.references, tuple)
        assert len(task.references) == 2

    def test_stream_flag_exists_but_defaults_false(self) -> None:
        """Binding condition #1: protocol shape reserves streaming for v2."""
        task = ExecutionTask(
            parts=(TaskPart(content="x"),),
            output_path="/tmp/out.md",
        )
        assert task.stream is False


class TestExecutionTaskFromPrompt:
    """Binding condition #1: from_prompt() compat constructor."""

    def test_wraps_prompt_in_single_text_part(self) -> None:
        task = ExecutionTask.from_prompt(
            prompt="You are a reviewer...",
            output_path="/tmp/out.md",
        )
        assert len(task.parts) == 1
        assert task.parts[0].content == "You are a reviewer..."
        assert task.parts[0].media_type == "text/markdown"
        assert task.output_path == "/tmp/out.md"

    def test_read_paths_become_references(self) -> None:
        task = ExecutionTask.from_prompt(
            prompt="Review spec and research report",
            output_path="/tmp/out.md",
            read_paths=["/tmp/spec.md", "/tmp/research.md"],
        )
        assert len(task.references) == 2
        assert task.references[0].uri == "/tmp/spec.md"
        assert task.references[1].uri == "/tmp/research.md"
        # Descriptions remain None in the flat path
        assert task.references[0].description is None

    def test_metadata_is_preserved(self) -> None:
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata={"phase": "review", "agent_name": "reviewer-a", "round": 1},
        )
        assert task.metadata == {"phase": "review", "agent_name": "reviewer-a", "round": 1}

    def test_metadata_is_copied_not_aliased(self) -> None:
        """Caller mutations after construction must not leak into the task."""
        original = {"phase": "review"}
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata=original,
        )
        original["phase"] = "cross-review"
        assert task.metadata == {"phase": "review"}

    def test_no_read_paths_yields_empty_references(self) -> None:
        task = ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md")
        assert task.references == ()

    def test_tuple_read_paths_accepted(self) -> None:
        """``read_paths`` accepts both list and tuple."""
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            read_paths=("/tmp/a.md", "/tmp/b.md"),
        )
        assert len(task.references) == 2


class TestExecutionTaskProperties:
    """Convenience properties for providers that operate on flat shapes."""

    def test_prompt_joins_all_parts_with_double_newline(self) -> None:
        task = ExecutionTask(
            parts=(
                TaskPart(content="Part 1"),
                TaskPart(content="Part 2"),
                TaskPart(content="Part 3"),
            ),
            output_path="/tmp/out.md",
        )
        assert task.prompt == "Part 1\n\nPart 2\n\nPart 3"

    def test_prompt_single_part_returns_just_that_content(self) -> None:
        task = ExecutionTask.from_prompt(prompt="single", output_path="/tmp/out.md")
        assert task.prompt == "single"

    def test_read_paths_property_returns_uris(self) -> None:
        task = ExecutionTask(
            parts=(TaskPart(content="x"),),
            output_path="/tmp/out.md",
            references=(
                Reference(uri="/tmp/a.md", description="A"),
                Reference(uri="/tmp/b.md"),
            ),
        )
        assert task.read_paths == ("/tmp/a.md", "/tmp/b.md")

    def test_read_paths_property_empty_when_no_references(self) -> None:
        task = ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md")
        assert task.read_paths == ()


# ---------------------------------------------------------------------------
# Cost and Duration — binding conditions #5 and #6
# ---------------------------------------------------------------------------


class TestCost:
    def test_default_values(self) -> None:
        c = Cost()
        assert c.input_tokens == 0
        assert c.output_tokens == 0
        assert c.usd is None
        assert c.currency == "USD"

    def test_full_construction(self) -> None:
        c = Cost(input_tokens=1500, output_tokens=400, usd=0.0234)
        assert c.input_tokens == 1500
        assert c.output_tokens == 400
        assert c.usd == pytest.approx(0.0234)

    def test_usd_none_distinct_from_zero(self) -> None:
        """Binding condition #5: unknown cost is None, not zero."""
        unknown_cost = Cost(input_tokens=100, output_tokens=50, usd=None)
        free_cost = Cost(input_tokens=100, output_tokens=50, usd=0.0)
        assert unknown_cost.usd is None
        assert free_cost.usd == 0.0
        assert unknown_cost != free_cost


class TestDuration:
    """Binding condition #6: Duration is a structured type, not a float.

    v1 uses ``datetime.timedelta`` as the underlying type because it is
    stdlib and convertible with zero precision loss.  When spec 047 lands,
    the ``Duration`` alias will be redefined to point at the richer type.
    """

    def test_duration_is_timedelta_in_v1(self) -> None:
        assert Duration is timedelta

    def test_can_express_subprocess_cold_start(self) -> None:
        """Cold start for a subprocess provider is 1-3 seconds per invocation."""
        cold_start = Duration(seconds=2, microseconds=500_000)
        assert cold_start.total_seconds() == pytest.approx(2.5)

    def test_can_express_long_running_deliberation(self) -> None:
        """A full deliberation may run for several minutes."""
        run_time = Duration(minutes=45, seconds=32)
        assert run_time.total_seconds() == 45 * 60 + 32


# ---------------------------------------------------------------------------
# ExecutionResult — structured result shape
# ---------------------------------------------------------------------------


class TestExecutionResult:
    def test_minimal_success(self) -> None:
        result = ExecutionResult(success=True, output_path="/tmp/out.md")
        assert result.success is True
        assert result.output_path == "/tmp/out.md"
        assert result.content is None
        assert result.error is None
        assert result.cost is None
        assert result.duration is None
        assert result.provider == ""
        assert result.metadata == {}

    def test_full_success_with_cost_and_duration(self) -> None:
        result = ExecutionResult(
            success=True,
            output_path="/tmp/out.md",
            content="# Review\n\nThe spec is sound.",
            cost=Cost(input_tokens=1200, output_tokens=800, usd=0.018),
            duration=Duration(seconds=42),
            provider="claude-code",
            metadata={"model": "claude-sonnet-4-6", "chunks": 4},
        )
        assert result.success is True
        assert result.cost is not None
        assert result.cost.input_tokens == 1200
        assert result.duration is not None
        assert result.duration.total_seconds() == 42
        assert result.provider == "claude-code"

    def test_failure_carries_provider_error(self) -> None:
        """Binding condition #4: error is a structured ProviderError, not a string."""
        err = ProviderError("connection refused", category="network")
        result = ExecutionResult(
            success=False,
            output_path="/tmp/out.md",
            error=err,
            provider="opencode",
        )
        assert result.success is False
        assert result.error is err
        assert result.error.category == "network"

    @pytest.mark.parametrize(
        "category",
        ["timeout", "subprocess", "network", "malformed"],
    )
    def test_new_failure_categories_round_trip_through_result(self, category: str) -> None:
        """All four new categories from binding condition #4 are usable on results."""
        err = ProviderError(f"{category} failure", category=category)  # type: ignore[arg-type]
        result = ExecutionResult(
            success=False,
            output_path="/tmp/out.md",
            error=err,
            provider="claude-code",
        )
        assert result.error is not None
        assert result.error.category == category


# ---------------------------------------------------------------------------
# ExecutionProvider protocol — structural conformance
# ---------------------------------------------------------------------------


class _ConformingProvider:
    """Minimal stub provider used to verify protocol conformance at runtime."""

    name = "stub"
    supports_tool_use = False
    supports_pooling = False

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=task.prompt,
            provider=self.name,
        )

    async def execute_batch(self, tasks: list[ExecutionTask]) -> list[ExecutionResult]:
        return await asyncio.gather(*(self.execute(t) for t in tasks))


class TestExecutionProviderProtocol:
    def test_stub_conforms_to_protocol(self) -> None:
        """``@runtime_checkable`` Protocol — ``isinstance`` is valid."""
        provider = _ConformingProvider()
        assert isinstance(provider, ExecutionProvider)

    @pytest.mark.asyncio
    async def test_stub_executes_single_task(self) -> None:
        provider = _ConformingProvider()
        task = ExecutionTask.from_prompt(prompt="hello", output_path="/tmp/out.md")
        result = await provider.execute(task)
        assert result.success is True
        assert result.content == "hello"
        assert result.provider == "stub"

    @pytest.mark.asyncio
    async def test_stub_executes_batch(self) -> None:
        provider = _ConformingProvider()
        tasks = [
            ExecutionTask.from_prompt(prompt=f"task {i}", output_path=f"/tmp/out-{i}.md")
            for i in range(5)
        ]
        results = await provider.execute_batch(tasks)
        assert len(results) == 5
        assert all(r.success for r in results)
        assert [r.content for r in results] == [f"task {i}" for i in range(5)]
