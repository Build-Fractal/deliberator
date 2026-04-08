"""Tests for engine.execution.providers.anthropic — AnthropicExecutionProvider.

Tests the Phase 2.3 execution provider without hitting the real Anthropic API.
Uses unittest.mock to patch the AsyncAnthropic client's messages.create method.
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import anthropic

from engine.execution import (
    ExecutionProvider,
    ExecutionResult,
    ExecutionTask,
    Reference,
    TaskPart,
)
from engine.execution.providers import PROVIDER_REGISTRY, get_provider
from engine.execution.providers.anthropic import (
    AnthropicExecutionProvider,
    _inline_references,
)
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_sdk_response(
    text: str = "Hello, world!",
    input_tokens: int = 42,
    output_tokens: int = 17,
    stop_reason: str = "end_turn",
    message_id: str = "msg_test_123",
) -> MagicMock:
    """Build a fake ``anthropic.types.Message``-shaped response object."""
    content_block = MagicMock()
    content_block.text = text

    usage = MagicMock()
    usage.input_tokens = input_tokens
    usage.output_tokens = output_tokens

    response = MagicMock()
    response.content = [content_block]
    response.usage = usage
    response.stop_reason = stop_reason
    response.id = message_id

    return response


def _make_task(
    prompt: str = "Test prompt",
    output_path: str = "/tmp/test-output.md",
    agent_name: str = "test-agent",
    model: str | None = None,
    read_paths: list[str] | None = None,
) -> ExecutionTask:
    """Build a minimal ExecutionTask for tests."""
    metadata: dict[str, Any] = {"agent_name": agent_name, "phase": "review"}
    if model is not None:
        metadata["model"] = model
    return ExecutionTask.from_prompt(
        prompt=prompt,
        output_path=output_path,
        read_paths=read_paths,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------


class TestRegistration:
    """Verify the provider is registered correctly in the package registry."""

    def test_anthropic_registered(self) -> None:
        assert "anthropic" in PROVIDER_REGISTRY
        assert PROVIDER_REGISTRY["anthropic"] is AnthropicExecutionProvider

    def test_get_provider_resolves(self) -> None:
        provider = get_provider("anthropic")
        assert isinstance(provider, AnthropicExecutionProvider)
        assert provider.name == "anthropic"


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


class TestProtocolConformance:
    """Verify AnthropicExecutionProvider satisfies the ExecutionProvider protocol."""

    def test_isinstance_check(self) -> None:
        provider = AnthropicExecutionProvider()
        assert isinstance(provider, ExecutionProvider)

    def test_properties(self) -> None:
        provider = AnthropicExecutionProvider()
        assert provider.name == "anthropic"
        assert provider.supports_tool_use is False
        assert provider.supports_pooling is False

    def test_has_execute_method(self) -> None:
        provider = AnthropicExecutionProvider()
        assert callable(getattr(provider, "execute", None))

    def test_has_execute_batch_method(self) -> None:
        provider = AnthropicExecutionProvider()
        assert callable(getattr(provider, "execute_batch", None))


# ---------------------------------------------------------------------------
# Execution — success paths
# ---------------------------------------------------------------------------


class TestExecuteSuccess:
    """Tests for the happy-path execute() call."""

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_basic_execute(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_sdk_response(text="The answer is 4.")
        )
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        task = _make_task(prompt="What is 2+2?")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content == "The answer is 4."
        assert result.error is None
        assert result.provider == "anthropic"
        assert result.output_path == task.output_path

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_cost_telemetry(self, mock_cls: MagicMock) -> None:
        """Binding condition #5: cost data must be extracted from SDK response."""
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_sdk_response(input_tokens=100, output_tokens=50)
        )
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.cost is not None
        assert result.cost.input_tokens == 100
        assert result.cost.output_tokens == 50
        assert result.cost.usd is None  # SDK doesn't provide dollar amount
        assert result.cost.currency == "USD"

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_duration_is_populated(self, mock_cls: MagicMock) -> None:
        """Binding condition #6: duration must be a real timedelta."""
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=_make_sdk_response())
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.duration is not None
        assert result.duration.total_seconds() >= 0

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_metadata_includes_stop_reason_and_id(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_sdk_response(stop_reason="max_tokens", message_id="msg_abc")
        )
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.metadata["stop_reason"] == "max_tokens"
        assert result.metadata["message_id"] == "msg_abc"

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_model_override_from_metadata(self, mock_cls: MagicMock) -> None:
        """Task metadata['model'] should override the provider default."""
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=_make_sdk_response())
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider(model="default-model")
        task = _make_task(model="claude-opus-4-20250514")
        asyncio.run(provider.execute(task))

        call_kwargs = mock_client.messages.create.call_args
        assert call_kwargs.kwargs["model"] == "claude-opus-4-20250514"


# ---------------------------------------------------------------------------
# Execution — error paths
# ---------------------------------------------------------------------------


class TestExecuteErrors:
    """Each Anthropic SDK error type maps to the correct ProviderError category."""

    @pytest.mark.parametrize(
        "exc_cls,expected_category",
        [
            (anthropic.AuthenticationError, "auth"),
            (anthropic.RateLimitError, "rate_limit"),
        ],
    )
    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_specific_errors(
        self,
        mock_cls: MagicMock,
        exc_cls: type,
        expected_category: str,
    ) -> None:
        mock_client = MagicMock()
        # Construct the exception with the shape the SDK uses
        mock_response = MagicMock()
        mock_response.status_code = 401 if expected_category == "auth" else 429
        mock_response.headers = {}
        exc = exc_cls(
            message="test error",
            response=mock_response,
            body=None,
        )
        mock_client.messages.create = AsyncMock(side_effect=exc)
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == expected_category
        assert result.error.original is exc
        assert result.content is None
        assert result.cost is None  # No cost on failure

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_api_status_error(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.headers = {}
        exc = anthropic.APIStatusError(
            message="Internal server error",
            response=mock_response,
            body=None,
        )
        mock_client.messages.create = AsyncMock(side_effect=exc)
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "server"

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_generic_api_error(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 502
        mock_response.headers = {}
        exc = anthropic.APIError(
            message="Connection reset",
            request=MagicMock(),
            body=None,
        )
        mock_client.messages.create = AsyncMock(side_effect=exc)
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "unknown"

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_unexpected_exception(self, mock_cls: MagicMock) -> None:
        """Non-anthropic exceptions should also produce a clean error result."""
        mock_client = MagicMock()
        exc = RuntimeError("Something unexpected")
        mock_client.messages.create = AsyncMock(side_effect=exc)
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "unknown"
        assert result.error.original is exc

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_error_result_has_duration(self, mock_cls: MagicMock) -> None:
        """Even failed results should report duration."""
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(side_effect=RuntimeError("boom"))
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.duration is not None
        assert result.duration.total_seconds() >= 0


# ---------------------------------------------------------------------------
# Reference inlining
# ---------------------------------------------------------------------------


class TestReferenceInlining:
    """Tests for _inline_references — the reference→prompt prepending logic."""

    def test_no_references_returns_prompt_unchanged(self) -> None:
        task = _make_task(prompt="Hello world")
        assert _inline_references(task) == "Hello world"

    def test_existing_file_inlined(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("File content here")
            f.flush()

            task = ExecutionTask.from_prompt(
                prompt="Analyze this file",
                output_path="/tmp/out.md",
                read_paths=[f.name],
            )
            result = _inline_references(task)

            assert "File content here" in result
            assert "Analyze this file" in result
            assert f'path="{f.name}"' in result

    def test_missing_file_graceful(self) -> None:
        task = ExecutionTask.from_prompt(
            prompt="Analyze this",
            output_path="/tmp/out.md",
            read_paths=["/nonexistent/file.md"],
        )
        result = _inline_references(task)

        assert "file not found or unreadable" in result
        assert "Analyze this" in result

    def test_multiple_references_ordered(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f1:
            f1.write("Content A")
            f1.flush()
            with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f2:
                f2.write("Content B")
                f2.flush()

                task = ExecutionTask.from_prompt(
                    prompt="Review both",
                    output_path="/tmp/out.md",
                    read_paths=[f1.name, f2.name],
                )
                result = _inline_references(task)

                # Both contents present, prompt at end
                assert "Content A" in result
                assert "Content B" in result
                assert result.endswith("Review both")

    def test_reference_with_description(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Spec content")
            f.flush()

            task = ExecutionTask(
                parts=(TaskPart(content="Review this spec"),),
                output_path="/tmp/out.md",
                references=(Reference(uri=f.name, description="The main spec"),),
            )
            result = _inline_references(task)

            assert 'label="The main spec"' in result


# ---------------------------------------------------------------------------
# Batch execution
# ---------------------------------------------------------------------------


class TestBatchExecution:
    """Tests for execute_batch — concurrent dispatch via asyncio.gather."""

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_batch_returns_all_results(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=_make_sdk_response())
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        tasks = [_make_task(agent_name=f"agent-{i}") for i in range(3)]
        results = asyncio.run(provider.execute_batch(tasks))

        assert len(results) == 3
        assert all(r.success for r in results)

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_batch_isolates_failures(self, mock_cls: MagicMock) -> None:
        """One task failing should not prevent others from succeeding."""
        call_count = 0

        async def side_effect(*args: Any, **kwargs: Any) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("Boom on second call")
            return _make_sdk_response(text=f"Response {call_count}")

        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(side_effect=side_effect)
        mock_cls.return_value = mock_client

        provider = AnthropicExecutionProvider()
        tasks = [_make_task(agent_name=f"agent-{i}") for i in range(3)]
        results = asyncio.run(provider.execute_batch(tasks))

        assert len(results) == 3
        successes = [r for r in results if r.success]
        failures = [r for r in results if not r.success]
        assert len(successes) == 2
        assert len(failures) == 1


# ---------------------------------------------------------------------------
# OAuth / client construction
# ---------------------------------------------------------------------------


class TestClientConstruction:
    """Verify the OAuth token handling mirrors engine.providers.anthropic."""

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_no_token(self, mock_cls: MagicMock) -> None:
        AnthropicExecutionProvider()
        mock_cls.assert_called_once_with()

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_regular_token(self, mock_cls: MagicMock) -> None:
        AnthropicExecutionProvider(auth_token="sk-ant-api-regular-key")
        mock_cls.assert_called_once_with(auth_token="sk-ant-api-regular-key")

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_oauth_token_adds_stealth_headers(self, mock_cls: MagicMock) -> None:
        AnthropicExecutionProvider(auth_token="sk-ant-oat-subscription-token")
        call_kwargs = mock_cls.call_args.kwargs
        assert call_kwargs["auth_token"] == "sk-ant-oat-subscription-token"
        assert "user-agent" in call_kwargs["default_headers"]
        assert "claude-cli/" in call_kwargs["default_headers"]["user-agent"]


# ---------------------------------------------------------------------------
# End-to-end with mock (no network)
# ---------------------------------------------------------------------------


class TestEndToEnd:
    """Integration-style tests using the provider via the registry."""

    @patch("engine.execution.providers.anthropic.anthropic.AsyncAnthropic")
    def test_registry_round_trip(self, mock_cls: MagicMock) -> None:
        """get_provider('anthropic') → execute() → result with cost data."""
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(
            return_value=_make_sdk_response(
                text="Registry round-trip works!",
                input_tokens=200,
                output_tokens=80,
            )
        )
        mock_cls.return_value = mock_client

        provider = get_provider("anthropic")
        task = _make_task(prompt="Registry test")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content == "Registry round-trip works!"
        assert result.cost is not None
        assert result.cost.input_tokens == 200
        assert result.cost.output_tokens == 80
        assert result.provider == "anthropic"
