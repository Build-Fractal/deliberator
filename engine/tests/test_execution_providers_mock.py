"""Tests for MockExecutionProvider and the provider registry (spec 042 Phase 2.1)."""

from __future__ import annotations

import asyncio
from datetime import timedelta

import pytest

from engine.execution import (
    Cost,
    ExecutionResult,
    ExecutionTask,
    TaskPart,
)
from engine.execution.providers import (
    PROVIDER_REGISTRY,
    get_provider,
    register_provider,
)
from engine.execution.providers.mock import CallRecord, MockExecutionProvider
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestProviderRegistry:
    def test_mock_is_registered_at_import_time(self) -> None:
        """Importing the providers package eagerly registers ``mock``."""
        assert "mock" in PROVIDER_REGISTRY
        assert PROVIDER_REGISTRY["mock"] is MockExecutionProvider

    def test_get_provider_returns_instance(self) -> None:
        provider = get_provider("mock")
        assert isinstance(provider, MockExecutionProvider)

    def test_get_provider_passes_options_through(self) -> None:
        provider = get_provider(
            "mock",
            response_template="[custom:{agent_name}]",
            simulated_latency=0.0,
        )
        assert isinstance(provider, MockExecutionProvider)
        assert provider.response_template == "[custom:{agent_name}]"

    def test_get_provider_unknown_name_raises_with_list(self) -> None:
        with pytest.raises(ValueError, match="Unknown execution provider"):
            get_provider("nonexistent-provider")

    def test_get_provider_error_lists_available(self) -> None:
        try:
            get_provider("definitely-not-a-provider")
        except ValueError as exc:
            # The error message should include "mock" in the available list
            assert "mock" in str(exc)
        else:
            pytest.fail("Expected ValueError")

    def test_duplicate_registration_of_same_class_is_idempotent(self) -> None:
        """Re-importing the mock module does not raise."""
        # Simulate a re-import by calling register_provider with the same class
        register_provider("mock", MockExecutionProvider)  # should not raise

    def test_duplicate_registration_of_different_class_raises(self) -> None:
        class OtherProvider:
            name = "decoy"
            supports_tool_use = False
            supports_pooling = False

            async def execute(self, task: ExecutionTask) -> ExecutionResult:
                return ExecutionResult(success=True, output_path=task.output_path)

            async def execute_batch(
                self, tasks: list[ExecutionTask],
            ) -> list[ExecutionResult]:
                return [await self.execute(t) for t in tasks]

        with pytest.raises(ValueError, match="already registered"):
            register_provider("mock", OtherProvider)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# MockExecutionProvider — basic conformance
# ---------------------------------------------------------------------------


class TestMockProviderConformance:
    def test_protocol_attributes(self) -> None:
        provider = MockExecutionProvider()
        assert provider.name == "mock"
        assert provider.supports_tool_use is False
        assert provider.supports_pooling is False

    @pytest.mark.asyncio
    async def test_execute_returns_success_result(self) -> None:
        provider = MockExecutionProvider()
        task = ExecutionTask.from_prompt(
            prompt="review this",
            output_path="/tmp/out.md",
            metadata={"agent_name": "reviewer-a"},
        )
        result = await provider.execute(task)
        assert result.success is True
        assert result.output_path == "/tmp/out.md"
        assert result.content is not None
        assert result.error is None
        assert result.provider == "mock"

    @pytest.mark.asyncio
    async def test_execute_records_call(self) -> None:
        provider = MockExecutionProvider()
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata={"agent_name": "a", "phase": "review"},
        )
        await provider.execute(task)
        assert len(provider.calls) == 1
        call = provider.calls[0]
        assert isinstance(call, CallRecord)
        assert call.prompt == "x"
        assert call.output_path == "/tmp/out.md"
        assert call.metadata == {"agent_name": "a", "phase": "review"}

    @pytest.mark.asyncio
    async def test_result_duration_is_non_none(self) -> None:
        """Binding condition #6: duration is a structured type, always populated on success."""
        provider = MockExecutionProvider()
        task = ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md")
        result = await provider.execute(task)
        assert result.duration is not None
        assert isinstance(result.duration, timedelta)

    @pytest.mark.asyncio
    async def test_result_cost_has_none_usd_not_zero(self) -> None:
        """Binding condition #5: unknown cost is None, not 0.0."""
        provider = MockExecutionProvider()
        task = ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md")
        result = await provider.execute(task)
        assert result.cost is not None
        assert result.cost.input_tokens == 0
        assert result.cost.usd is None


# ---------------------------------------------------------------------------
# Response resolution — the 3-tier order
# ---------------------------------------------------------------------------


class TestResponseResolution:
    @pytest.mark.asyncio
    async def test_template_expansion_with_all_placeholders(self) -> None:
        provider = MockExecutionProvider(
            response_template="[{phase}:{agent_name}] {prompt} -> {output_path}",
        )
        task = ExecutionTask.from_prompt(
            prompt="review spec",
            output_path="/tmp/out.md",
            metadata={"agent_name": "fp-guru", "phase": "review"},
        )
        result = await provider.execute(task)
        assert result.content == "[review:fp-guru] review spec -> /tmp/out.md"

    @pytest.mark.asyncio
    async def test_response_map_wins_over_template(self) -> None:
        provider = MockExecutionProvider(
            response_template="[template]",
            response_map={"fp-guru": "mapped response for fp-guru"},
        )
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata={"agent_name": "fp-guru"},
        )
        result = await provider.execute(task)
        assert result.content == "mapped response for fp-guru"

    @pytest.mark.asyncio
    async def test_map_miss_falls_through_to_callable(self) -> None:
        def make_response(task: ExecutionTask) -> str:
            return f"callable saw {task.parts[0].content!r}"

        provider = MockExecutionProvider(
            response_map={"fp-guru": "guru only"},
            response_fn=make_response,
        )
        task = ExecutionTask.from_prompt(
            prompt="hello",
            output_path="/tmp/out.md",
            metadata={"agent_name": "sdet"},  # not in map
        )
        result = await provider.execute(task)
        assert result.content == "callable saw 'hello'"

    @pytest.mark.asyncio
    async def test_callable_falls_through_to_template(self) -> None:
        """With no callable and no map hit, template is used."""
        provider = MockExecutionProvider(response_template="[fallback:{agent_name}]")
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata={"agent_name": "nobody"},
        )
        result = await provider.execute(task)
        assert result.content == "[fallback:nobody]"

    @pytest.mark.asyncio
    async def test_no_agent_name_uses_template(self) -> None:
        provider = MockExecutionProvider(
            response_template="anonymous: {prompt}",
            response_map={"fp-guru": "never reached"},
        )
        task = ExecutionTask.from_prompt(prompt="hi", output_path="/tmp/out.md")
        result = await provider.execute(task)
        assert result.content == "anonymous: hi"


# ---------------------------------------------------------------------------
# Failure path
# ---------------------------------------------------------------------------


class TestMockProviderFailurePath:
    @pytest.mark.asyncio
    async def test_fail_for_agents_returns_error_result(self) -> None:
        provider = MockExecutionProvider(fail_for_agents={"broken-agent"})
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata={"agent_name": "broken-agent"},
        )
        result = await provider.execute(task)
        assert result.success is False
        assert result.content is None
        assert result.error is not None
        assert isinstance(result.error, ProviderError)
        assert result.error.category == "unknown"

    @pytest.mark.asyncio
    async def test_fail_for_agents_still_records_call(self) -> None:
        """Tests should see the failed call in the log."""
        provider = MockExecutionProvider(fail_for_agents={"broken"})
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata={"agent_name": "broken"},
        )
        await provider.execute(task)
        assert len(provider.calls) == 1

    @pytest.mark.asyncio
    async def test_fail_set_only_matches_exact_agent_name(self) -> None:
        """A different agent name should still succeed."""
        provider = MockExecutionProvider(fail_for_agents={"broken"})
        task = ExecutionTask.from_prompt(
            prompt="x",
            output_path="/tmp/out.md",
            metadata={"agent_name": "working"},
        )
        result = await provider.execute(task)
        assert result.success is True


# ---------------------------------------------------------------------------
# Batch execution
# ---------------------------------------------------------------------------


class TestMockProviderBatch:
    @pytest.mark.asyncio
    async def test_execute_batch_runs_all_tasks(self) -> None:
        provider = MockExecutionProvider()
        tasks = [
            ExecutionTask.from_prompt(
                prompt=f"task {i}",
                output_path=f"/tmp/out-{i}.md",
                metadata={"agent_name": f"agent-{i}"},
            )
            for i in range(5)
        ]
        results = await provider.execute_batch(tasks)
        assert len(results) == 5
        assert all(r.success for r in results)

    @pytest.mark.asyncio
    async def test_batch_preserves_order(self) -> None:
        provider = MockExecutionProvider(response_template="{agent_name}")
        tasks = [
            ExecutionTask.from_prompt(
                prompt="x",
                output_path=f"/tmp/out-{i}.md",
                metadata={"agent_name": f"agent-{i}"},
            )
            for i in range(3)
        ]
        results = await provider.execute_batch(tasks)
        assert [r.content for r in results] == ["agent-0", "agent-1", "agent-2"]

    @pytest.mark.asyncio
    async def test_batch_records_all_calls(self) -> None:
        provider = MockExecutionProvider()
        tasks = [
            ExecutionTask.from_prompt(
                prompt=f"task {i}",
                output_path=f"/tmp/out-{i}.md",
                metadata={"agent_name": f"agent-{i}"},
            )
            for i in range(3)
        ]
        await provider.execute_batch(tasks)
        assert len(provider.calls) == 3


# ---------------------------------------------------------------------------
# Test helpers: reset(), last_call()
# ---------------------------------------------------------------------------


class TestMockProviderTestHelpers:
    @pytest.mark.asyncio
    async def test_reset_clears_call_log(self) -> None:
        provider = MockExecutionProvider()
        task = ExecutionTask.from_prompt(prompt="x", output_path="/tmp/out.md")
        await provider.execute(task)
        assert len(provider.calls) == 1
        provider.reset()
        assert provider.calls == []

    @pytest.mark.asyncio
    async def test_last_call_returns_most_recent(self) -> None:
        provider = MockExecutionProvider()
        for i in range(3):
            await provider.execute(
                ExecutionTask.from_prompt(
                    prompt=f"task {i}",
                    output_path=f"/tmp/out-{i}.md",
                ),
            )
        last = provider.last_call()
        assert last.prompt == "task 2"
        assert last.output_path == "/tmp/out-2.md"

    def test_last_call_raises_when_empty(self) -> None:
        provider = MockExecutionProvider()
        with pytest.raises(IndexError):
            provider.last_call()


# ---------------------------------------------------------------------------
# Canonical structured shape support (not just from_prompt)
# ---------------------------------------------------------------------------


class TestMockProviderCanonicalShape:
    """The mock provider must handle tasks constructed via the canonical path too."""

    @pytest.mark.asyncio
    async def test_multi_part_task(self) -> None:
        """A task with multiple parts (e.g., identity + phase template) works."""
        provider = MockExecutionProvider(response_template="{prompt}")
        task = ExecutionTask(
            parts=(
                TaskPart(content="You are a reviewer."),
                TaskPart(content="Review the spec below."),
                TaskPart(content="=== SPEC ===\nSpec content."),
            ),
            output_path="/tmp/out.md",
            metadata={"agent_name": "reviewer"},
        )
        result = await provider.execute(task)
        # The response template uses {prompt} which joins all parts with \n\n
        assert result.content is not None
        assert "You are a reviewer." in result.content
        assert "=== SPEC ===" in result.content

    @pytest.mark.asyncio
    async def test_records_part_count(self) -> None:
        """CallRecord tracks how many parts the task had."""
        provider = MockExecutionProvider()
        task = ExecutionTask(
            parts=(
                TaskPart(content="a"),
                TaskPart(content="b"),
                TaskPart(content="c"),
            ),
            output_path="/tmp/out.md",
        )
        await provider.execute(task)
        assert provider.last_call().part_count == 3

    @pytest.mark.asyncio
    async def test_records_stream_flag(self) -> None:
        provider = MockExecutionProvider()
        task = ExecutionTask(
            parts=(TaskPart(content="x"),),
            output_path="/tmp/out.md",
            stream=True,
        )
        await provider.execute(task)
        assert provider.last_call().stream is True


# ---------------------------------------------------------------------------
# End-to-end: resolve via registry and run
# ---------------------------------------------------------------------------


class TestEndToEnd:
    @pytest.mark.asyncio
    async def test_registry_resolved_provider_executes_task(self) -> None:
        """Full path: registry lookup → instantiation → execution → result."""
        provider = get_provider("mock", response_template="E2E: {prompt}")
        task = ExecutionTask.from_prompt(
            prompt="end-to-end test",
            output_path="/tmp/e2e.md",
            metadata={"agent_name": "e2e"},
        )
        result = await provider.execute(task)
        assert result.success is True
        assert result.content == "E2E: end-to-end test"
        assert result.provider == "mock"
