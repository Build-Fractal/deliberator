"""Tests for OpenAI-compatible execution providers (ollama, llama-cpp, vllm).

Unit tests mock the OpenAI client. Live integration tests (marked
``@pytest.mark.live``) hit real local servers.
"""

from __future__ import annotations

import asyncio
import shutil
from datetime import timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from engine.execution import (
    ExecutionProvider,
    ExecutionResult,
    ExecutionTask,
)
from engine.execution.providers import PROVIDER_REGISTRY, get_provider
from engine.execution.providers.openai_compat import (
    LlamaCppProvider,
    OllamaProvider,
    OpenAICompatibleProvider,
    VLLMProvider,
    _inline_references,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_task(
    prompt: str = "Test prompt",
    output_path: str = "/tmp/test-output.md",
    agent_name: str = "test-agent",
    **extra_metadata: Any,
) -> ExecutionTask:
    metadata = {"agent_name": agent_name, "phase": "review", **extra_metadata}
    return ExecutionTask.from_prompt(
        prompt=prompt,
        output_path=output_path,
        metadata=metadata,
    )


def _make_openai_response(
    text: str = "Hello!",
    prompt_tokens: int = 10,
    completion_tokens: int = 5,
    finish_reason: str = "stop",
) -> MagicMock:
    """Build a fake openai ChatCompletion response."""
    choice = MagicMock()
    choice.message.content = text
    choice.finish_reason = finish_reason

    usage = MagicMock()
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens

    response = MagicMock()
    response.choices = [choice]
    response.usage = usage
    return response


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_ollama_registered(self) -> None:
        assert "ollama" in PROVIDER_REGISTRY

    def test_llama_cpp_registered(self) -> None:
        assert "llama-cpp" in PROVIDER_REGISTRY

    def test_vllm_registered(self) -> None:
        assert "vllm" in PROVIDER_REGISTRY

    def test_get_ollama(self) -> None:
        provider = get_provider("ollama")
        assert isinstance(provider, OllamaProvider)
        assert provider.name == "ollama"

    def test_get_llama_cpp(self) -> None:
        provider = get_provider("llama-cpp")
        assert isinstance(provider, LlamaCppProvider)
        assert provider.name == "llama-cpp"

    def test_get_vllm(self) -> None:
        provider = get_provider("vllm")
        assert isinstance(provider, VLLMProvider)
        assert provider.name == "vllm"

    def test_full_registry_count(self) -> None:
        """All 8 providers should be registered."""
        expected = {"mock", "anthropic", "claude-code", "aider", "opencode",
                    "ollama", "llama-cpp", "vllm"}
        assert expected.issubset(set(PROVIDER_REGISTRY.keys()))


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


class TestConformance:
    @pytest.mark.parametrize("name,cls", [
        ("ollama", OllamaProvider),
        ("llama-cpp", LlamaCppProvider),
        ("vllm", VLLMProvider),
    ])
    def test_isinstance(self, name: str, cls: type) -> None:
        provider = cls()
        assert isinstance(provider, ExecutionProvider)

    @pytest.mark.parametrize("cls", [OllamaProvider, LlamaCppProvider, VLLMProvider])
    def test_supports_tool_use_false(self, cls: type) -> None:
        assert cls().supports_tool_use is False

    @pytest.mark.parametrize("cls", [OllamaProvider, LlamaCppProvider, VLLMProvider])
    def test_supports_pooling_false(self, cls: type) -> None:
        assert cls().supports_pooling is False


# ---------------------------------------------------------------------------
# Default configuration
# ---------------------------------------------------------------------------


class TestDefaults:
    def test_ollama_defaults(self) -> None:
        p = OllamaProvider()
        assert p.name == "ollama"
        assert "11434" in p._base_url
        assert p._model == "qwen3:0.6b"

    def test_llama_cpp_defaults(self) -> None:
        p = LlamaCppProvider()
        assert p.name == "llama-cpp"
        assert "8080" in p._base_url

    def test_vllm_defaults(self) -> None:
        p = VLLMProvider()
        assert p.name == "vllm"
        assert "8000" in p._base_url

    def test_custom_base_url(self) -> None:
        p = OllamaProvider(base_url="http://gpu-server:11434/v1")
        assert p._base_url == "http://gpu-server:11434/v1"

    def test_custom_model(self) -> None:
        p = OllamaProvider(model="llama3:70b")
        assert p._model == "llama3:70b"


# ---------------------------------------------------------------------------
# OpenAI-compatible base — success path
# ---------------------------------------------------------------------------


class TestExecuteSuccess:
    @patch("engine.execution.providers.openai_compat.AsyncOpenAI")
    def test_basic_execute(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response(text="The answer.")
        )
        mock_cls.return_value = mock_client

        provider = OpenAICompatibleProvider(provider_name="test")
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is True
        assert result.content == "The answer."
        assert result.provider == "test"

    @patch("engine.execution.providers.openai_compat.AsyncOpenAI")
    def test_cost_telemetry(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response(prompt_tokens=50, completion_tokens=20)
        )
        mock_cls.return_value = mock_client

        provider = OpenAICompatibleProvider(provider_name="test")
        result = asyncio.run(provider.execute(_make_task()))

        assert result.cost is not None
        assert result.cost.input_tokens == 50
        assert result.cost.output_tokens == 20
        assert result.cost.usd is None  # Local — no dollar cost

    @patch("engine.execution.providers.openai_compat.AsyncOpenAI")
    def test_duration(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response()
        )
        mock_cls.return_value = mock_client

        provider = OpenAICompatibleProvider(provider_name="test")
        result = asyncio.run(provider.execute(_make_task()))

        assert result.duration is not None
        assert result.duration.total_seconds() >= 0

    @patch("engine.execution.providers.openai_compat.AsyncOpenAI")
    def test_model_override(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response()
        )
        mock_cls.return_value = mock_client

        provider = OpenAICompatibleProvider(model="default-model", provider_name="test")
        task = _make_task(model="override-model")
        asyncio.run(provider.execute(task))

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "override-model"


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


class TestExecuteErrors:
    @patch("engine.execution.providers.openai_compat.AsyncOpenAI")
    def test_connection_error(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=ConnectionError("Connection refused")
        )
        mock_cls.return_value = mock_client

        provider = OpenAICompatibleProvider(provider_name="test")
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "network"

    @patch("engine.execution.providers.openai_compat.AsyncOpenAI")
    def test_generic_error(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=RuntimeError("Something broke")
        )
        mock_cls.return_value = mock_client

        provider = OpenAICompatibleProvider(provider_name="test")
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "unknown"


# ---------------------------------------------------------------------------
# Batch execution
# ---------------------------------------------------------------------------


class TestBatch:
    @patch("engine.execution.providers.openai_compat.AsyncOpenAI")
    def test_batch(self, mock_cls: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=_make_openai_response()
        )
        mock_cls.return_value = mock_client

        provider = OpenAICompatibleProvider(provider_name="test")
        tasks = [_make_task(prompt=f"Task {i}") for i in range(3)]
        results = asyncio.run(provider.execute_batch(tasks))

        assert len(results) == 3
        assert all(r.success for r in results)


# ---------------------------------------------------------------------------
# Live tests — ollama
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestOllamaLive:
    """Live tests that hit the local Ollama server.

    Requires: ``ollama serve`` running and ``qwen3:0.6b`` model pulled.
    Run with: ``pytest -m live``
    """

    @pytest.fixture(autouse=True)
    def _skip_if_unavailable(self) -> None:
        if not shutil.which("ollama"):
            pytest.skip("ollama not installed")
        # Quick check if server is running
        import httpx
        try:
            httpx.get("http://localhost:11434/api/tags", timeout=2)
        except Exception:
            pytest.skip("ollama server not running")

    def test_ping_pong(self) -> None:
        provider = OllamaProvider(model="qwen3:0.6b")
        task = _make_task(prompt="/no_think Reply with exactly the word pong. Nothing else.")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content is not None
        assert "pong" in result.content.lower()
        assert result.provider == "ollama"

    def test_cost_has_tokens(self) -> None:
        provider = OllamaProvider(model="qwen3:0.6b")
        task = _make_task(prompt="/no_think Say hello.")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.cost is not None
        assert result.cost.input_tokens > 0
        assert result.cost.output_tokens > 0
        assert result.cost.usd is None  # Local — free

    def test_duration(self) -> None:
        provider = OllamaProvider(model="qwen3:0.6b")
        task = _make_task(prompt="/no_think Hi")
        result = asyncio.run(provider.execute(task))

        assert result.duration is not None
        assert result.duration.total_seconds() > 0
