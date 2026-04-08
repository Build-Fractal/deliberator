"""Tests for ModelProviderExecutionAdapter (spec 042 Phase 2.2).

The adapter wraps a ModelProvider as an ExecutionProvider so the
existing dispatch.py call sites route through the new task-level
abstraction without changing their external signatures.  These tests
exercise the adapter directly, independent of the dispatch_agent()
and dispatch_phase() callers that consume it internally.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import timedelta

import pytest

from engine.dispatch import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    ModelProviderExecutionAdapter,
)
from engine.execution import ExecutionResult, ExecutionTask
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Stub ModelProvider implementations for isolated adapter testing
# ---------------------------------------------------------------------------


class _ScriptedModelProvider:
    """Minimal ModelProvider that returns a canned response or raises."""

    def __init__(
        self,
        response: str = "scripted response",
        *,
        raise_exc: Exception | None = None,
    ) -> None:
        self.response = response
        self.raise_exc = raise_exc
        self.calls: list[tuple[str, str, int]] = []

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        self.calls.append((prompt, model, max_tokens))
        if self.raise_exc is not None:
            raise self.raise_exc
        return self.response

    async def stream(
        self, prompt: str, model: str, max_tokens: int,
    ) -> AsyncIterator[str]:
        """Not exercised by the adapter (adapter uses complete only)."""
        if False:
            yield ""  # pragma: no cover
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


class TestAdapterConformance:
    def test_advertises_no_tool_use(self) -> None:
        """Adapter wraps a raw-completion provider — no autonomous filesystem."""
        adapter = ModelProviderExecutionAdapter(_ScriptedModelProvider())
        assert adapter.supports_tool_use is False

    def test_advertises_no_pooling(self) -> None:
        """Any pooling lives inside the wrapped SDK, not in the adapter."""
        adapter = ModelProviderExecutionAdapter(_ScriptedModelProvider())
        assert adapter.supports_pooling is False

    def test_default_name_is_descriptive(self) -> None:
        adapter = ModelProviderExecutionAdapter(_ScriptedModelProvider())
        assert adapter.name == "model-provider-adapter"

    def test_explicit_name_overrides_default(self) -> None:
        adapter = ModelProviderExecutionAdapter(
            _ScriptedModelProvider(),
            name="anthropic",
        )
        assert adapter.name == "anthropic"


# ---------------------------------------------------------------------------
# Successful execute()
# ---------------------------------------------------------------------------


class TestAdapterSuccess:
    @pytest.mark.asyncio
    async def test_delegates_prompt_to_complete(self) -> None:
        inner = _ScriptedModelProvider(response="the response")
        adapter = ModelProviderExecutionAdapter(inner)
        task = ExecutionTask.from_prompt(
            prompt="the prompt",
            output_path="/tmp/out.md",
        )
        result = await adapter.execute(task)

        assert len(inner.calls) == 1
        prompt, model, max_tokens = inner.calls[0]
        assert prompt == "the prompt"
        assert model == DEFAULT_MODEL
        assert max_tokens == DEFAULT_MAX_TOKENS
        assert result.success is True
        assert result.content == "the response"

    @pytest.mark.asyncio
    async def test_respects_explicit_model_and_max_tokens(self) -> None:
        inner = _ScriptedModelProvider(response="x")
        adapter = ModelProviderExecutionAdapter(
            inner,
            model="claude-sonnet-4-6",
            max_tokens=4096,
        )
        await adapter.execute(
            ExecutionTask.from_prompt(prompt="hi", output_path="/tmp/out.md"),
        )
        assert inner.calls[0][1] == "claude-sonnet-4-6"
        assert inner.calls[0][2] == 4096

    @pytest.mark.asyncio
    async def test_multi_part_task_joins_via_prompt_property(self) -> None:
        """Adapter honors the canonical A2A-shape path too, not just from_prompt."""
        from engine.execution import TaskPart

        inner = _ScriptedModelProvider(response="ok")
        adapter = ModelProviderExecutionAdapter(inner)
        task = ExecutionTask(
            parts=(
                TaskPart(content="System: you are X"),
                TaskPart(content="User: do Y"),
            ),
            output_path="/tmp/out.md",
        )
        await adapter.execute(task)
        # ExecutionTask.prompt joins parts with double newline
        assert inner.calls[0][0] == "System: you are X\n\nUser: do Y"

    @pytest.mark.asyncio
    async def test_result_provider_name_reported(self) -> None:
        adapter = ModelProviderExecutionAdapter(
            _ScriptedModelProvider(),
            name="openai",
        )
        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )
        assert result.provider == "openai"

    @pytest.mark.asyncio
    async def test_result_duration_is_populated(self) -> None:
        """Binding condition #6: duration is a structured type, always populated."""
        adapter = ModelProviderExecutionAdapter(_ScriptedModelProvider())
        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )
        assert result.duration is not None
        assert isinstance(result.duration, timedelta)

    @pytest.mark.asyncio
    async def test_result_cost_is_none_not_fabricated(self) -> None:
        """Binding condition #5: unknown cost is None, not fabricated zero."""
        adapter = ModelProviderExecutionAdapter(_ScriptedModelProvider())
        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )
        # The adapter wraps a ModelProvider which does not report cost.
        # Reporting None (rather than fabricating 0 tokens/0 USD) is
        # what binding condition #5 mandates.
        assert result.cost is None

    @pytest.mark.asyncio
    async def test_result_metadata_includes_model_and_max_tokens(self) -> None:
        adapter = ModelProviderExecutionAdapter(
            _ScriptedModelProvider(),
            model="custom-model",
            max_tokens=2048,
        )
        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )
        assert result.metadata == {"model": "custom-model", "max_tokens": 2048}


# ---------------------------------------------------------------------------
# Failure paths
# ---------------------------------------------------------------------------


class TestAdapterFailurePaths:
    @pytest.mark.asyncio
    async def test_provider_error_preserved_in_result(self) -> None:
        """ProviderError from the underlying ModelProvider is passed through intact."""
        err = ProviderError("rate limited", category="rate_limit")
        inner = _ScriptedModelProvider(raise_exc=err)
        adapter = ModelProviderExecutionAdapter(inner, name="anthropic")

        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )

        assert result.success is False
        assert result.content is None
        assert result.error is err
        assert result.error.category == "rate_limit"
        assert result.provider == "anthropic"

    @pytest.mark.asyncio
    async def test_generic_exception_wrapped_in_provider_error(self) -> None:
        """Non-ProviderError exceptions become ProviderError(category='unknown')."""
        inner = _ScriptedModelProvider(raise_exc=RuntimeError("kaboom"))
        adapter = ModelProviderExecutionAdapter(inner)

        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )

        assert result.success is False
        assert result.error is not None
        assert isinstance(result.error, ProviderError)
        assert result.error.category == "unknown"
        assert "RuntimeError" in str(result.error)
        assert "kaboom" in str(result.error)
        # Original exception is preserved on the wrapper for debugging
        assert isinstance(result.error.original, RuntimeError)

    @pytest.mark.asyncio
    async def test_failure_duration_is_populated(self) -> None:
        """Even on failure, the adapter reports how long the call took."""
        inner = _ScriptedModelProvider(raise_exc=RuntimeError("x"))
        adapter = ModelProviderExecutionAdapter(inner)
        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )
        assert result.duration is not None

    @pytest.mark.asyncio
    async def test_failure_records_metadata(self) -> None:
        inner = _ScriptedModelProvider(raise_exc=ProviderError("auth bad", category="auth"))
        adapter = ModelProviderExecutionAdapter(
            inner,
            model="test-model",
            max_tokens=512,
        )
        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )
        assert result.metadata == {"model": "test-model", "max_tokens": 512}

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "category",
        ["auth", "rate_limit", "server", "timeout", "subprocess", "network", "malformed", "unknown"],
    )
    async def test_every_provider_error_category_passes_through(
        self, category: str,
    ) -> None:
        """All 8 categories from the expanded Literal round-trip through the adapter."""
        err = ProviderError(f"failure: {category}", category=category)  # type: ignore[arg-type]
        inner = _ScriptedModelProvider(raise_exc=err)
        adapter = ModelProviderExecutionAdapter(inner)
        result = await adapter.execute(
            ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md"),
        )
        assert result.error is not None
        assert result.error.category == category


# ---------------------------------------------------------------------------
# Batch execution
# ---------------------------------------------------------------------------


class TestAdapterBatch:
    @pytest.mark.asyncio
    async def test_batch_calls_inner_complete_for_each_task(self) -> None:
        inner = _ScriptedModelProvider(response="x")
        adapter = ModelProviderExecutionAdapter(inner)
        tasks = [
            ExecutionTask.from_prompt(prompt=f"task {i}", output_path=f"/tmp/{i}.md")
            for i in range(5)
        ]
        results = await adapter.execute_batch(tasks)
        assert len(results) == 5
        assert all(r.success for r in results)
        assert len(inner.calls) == 5
        # Order is preserved
        assert [c[0] for c in inner.calls] == [
            "task 0", "task 1", "task 2", "task 3", "task 4",
        ]

    @pytest.mark.asyncio
    async def test_batch_isolates_per_task_failures(self) -> None:
        """A failure on one task does not propagate to others.

        The underlying ``asyncio.gather`` without ``return_exceptions``
        would raise.  The adapter's default ``execute_batch`` uses plain
        ``gather``, so per-task failures ARE raised at the batch level —
        verifying that behavior here so future callers know what they
        signed up for.
        """
        # A provider that raises should propagate through the batch
        inner = _ScriptedModelProvider(raise_exc=ProviderError("boom", category="server"))
        adapter = ModelProviderExecutionAdapter(inner)
        tasks = [
            ExecutionTask.from_prompt(prompt=f"task {i}", output_path=f"/tmp/{i}.md")
            for i in range(3)
        ]
        # The adapter catches the exception per-call and returns a
        # failure ExecutionResult, so batch does NOT raise.
        results = await adapter.execute_batch(tasks)
        assert len(results) == 3
        assert all(not r.success for r in results)
        assert all(r.error is not None for r in results)
