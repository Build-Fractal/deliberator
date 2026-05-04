"""OpenAI-compatible HTTP execution providers for local inference servers.

Many local inference runtimes expose an OpenAI-compatible
``/v1/chat/completions`` endpoint:

- **Ollama**: ``http://localhost:11434/v1``
- **llama.cpp (llama-server)**: ``http://localhost:8080/v1``
- **vLLM**: ``http://localhost:8000/v1``
- **LM Studio**: ``http://localhost:1234/v1``
- **LocalAI**: ``http://localhost:8080/v1``

This module provides a shared :class:`OpenAICompatibleProvider` base
that wraps the ``openai`` Python client with a custom ``base_url``, and
thin subclasses for specific runtimes.  Each subclass just sets default
URL, model, and registration name.

All providers in this module have ``supports_tool_use=False`` — they
are direct model APIs, not agent runtimes.  The engine pre-reads
reference file contents into the prompt and post-writes output from
:attr:`ExecutionResult.content` (same pattern as
:class:`AnthropicExecutionProvider`).

Cost telemetry: the OpenAI client returns ``usage.prompt_tokens`` and
``usage.completion_tokens``, which we extract into :class:`Cost`.
Local models have ``usd=None`` (no dollar cost) but token counts are
still meaningful for throughput tracking.
"""

from __future__ import annotations

import asyncio
import time
from datetime import timedelta
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from engine.execution.provider import (
    Cost,
    ExecutionResult,
    ExecutionTask,
)
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Reference inlining (shared with AnthropicExecutionProvider)
# ---------------------------------------------------------------------------

def _inline_references(task: ExecutionTask) -> str:
    """Prepend reference file contents to the prompt."""
    if not task.references:
        return task.prompt

    blocks: list[str] = []
    for ref in task.references:
        path = Path(ref.uri)
        try:
            content = path.read_text(encoding="utf-8")
            label = ref.description or path.name
            blocks.append(
                f"<reference path=\"{ref.uri}\" label=\"{label}\">\n"
                f"{content}\n"
                f"</reference>"
            )
        except OSError:
            blocks.append(
                f"<reference path=\"{ref.uri}\" error=\"file not found or unreadable\" />"
            )

    return "\n\n".join(blocks) + "\n\n" + task.prompt


# ---------------------------------------------------------------------------
# OpenAICompatibleProvider base
# ---------------------------------------------------------------------------


class OpenAICompatibleProvider:
    """Execution provider for any server with an OpenAI-compatible API.

    Uses the ``openai`` Python client with a custom ``base_url``.
    Subclasses set different defaults for URL, model, and name.

    This class is directly usable — it's not abstract.  You can
    instantiate ``OpenAICompatibleProvider(base_url=..., model=...)``
    for any OpenAI-compatible server without subclassing.

    Args:
        base_url: Base URL of the API server (e.g., ``"http://localhost:11434/v1"``).
        model: Default model name.  Per-task override via ``task.metadata["model"]``.
        max_tokens: Default max tokens.  Per-task override via ``task.metadata["max_tokens"]``.
        api_key: API key if required.  Most local servers accept any string.
        provider_name: Name for the registry and result metadata.
    """

    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(
        self,
        base_url: str = "http://localhost:8080/v1",
        model: str = "default",
        max_tokens: int = 16384,
        api_key: str = "not-needed",
        provider_name: str = "openai-compat",
    ) -> None:
        self._base_url = base_url
        self._model = model
        self._max_tokens = max_tokens
        self._provider_name = provider_name
        self._client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    @property
    def name(self) -> str:
        return self._provider_name

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        # Issue #54 contract: dispatch layer passes None when there is
        # no model override, so the provider applies its own default.
        # Local providers (ollama, llama-cpp, vllm) have their own
        # default models (e.g. qwen3:0.6b). The legacy guard below
        # defended against the old leak of ``claude-sonnet-4-20250514``
        # from dispatch — issue #54 retired that leak, but the guard
        # remains useful for explicit Anthropic-model overrides that
        # callers may still pass; in that case prefer the local
        # provider's own default since the Anthropic id won't resolve
        # against a local server.
        task_model = task.metadata.get("model") or ""
        model = self._model if not task_model or task_model.startswith("claude") else task_model
        max_tokens = task.metadata.get("max_tokens", self._max_tokens)
        prompt = _inline_references(task)

        start = time.monotonic()
        try:
            response = await self._client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as exc:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"{self._provider_name} error: {type(exc).__name__}: {exc}",
                    category="network" if "connect" in str(exc).lower() else "unknown",
                    original=exc,
                ),
                cost=None,
                duration=timedelta(seconds=time.monotonic() - start),
                provider=self.name,
                metadata={"model": model, "base_url": self._base_url},
            )

        content = ""
        if response.choices:
            content = response.choices[0].message.content or ""

        # Extract token usage
        cost = None
        if response.usage:
            cost = Cost(
                input_tokens=response.usage.prompt_tokens or 0,
                output_tokens=response.usage.completion_tokens or 0,
                usd=None,  # Local models — no dollar cost
            )

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=content,
            error=None,
            cost=cost,
            duration=timedelta(seconds=time.monotonic() - start),
            provider=self.name,
            metadata={
                "model": model,
                "base_url": self._base_url,
                "finish_reason": response.choices[0].finish_reason if response.choices else None,
            },
        )

    async def execute_batch(
        self,
        tasks: list[ExecutionTask] | tuple[ExecutionTask, ...],
    ) -> list[ExecutionResult]:
        return list(await asyncio.gather(*(self.execute(t) for t in tasks)))


# ---------------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------------


class OllamaProvider(OpenAICompatibleProvider):
    """Execution provider for Ollama (local LLM server).

    Ollama exposes an OpenAI-compatible API at ``/v1`` on port 11434.
    Default model is ``qwen3:0.6b`` (fast, small, good for testing).
    Override with any model in ``ollama list``.

    Args:
        model: Ollama model name (e.g., ``"llama3"``, ``"qwen3:0.6b"``).
        base_url: Ollama server URL.  Default ``http://localhost:11434/v1``.
        max_tokens: Default max tokens.
    """

    def __init__(
        self,
        model: str = "qwen3:0.6b",
        base_url: str = "http://localhost:11434/v1",
        max_tokens: int = 16384,
    ) -> None:
        super().__init__(
            base_url=base_url,
            model=model,
            max_tokens=max_tokens,
            api_key="ollama",
            provider_name="ollama",
        )


# ---------------------------------------------------------------------------
# llama.cpp (llama-server)
# ---------------------------------------------------------------------------


class LlamaCppProvider(OpenAICompatibleProvider):
    """Execution provider for llama.cpp's ``llama-server``.

    llama-server exposes an OpenAI-compatible API at ``/v1`` on port 8080.
    Start the server with::

        llama-server -m model.gguf --port 8080

    Args:
        model: Model name as known to the server.  If the server only
            has one model loaded, any string works.
        base_url: Server URL.  Default ``http://localhost:8080/v1``.
        max_tokens: Default max tokens.
    """

    def __init__(
        self,
        model: str = "default",
        base_url: str = "http://localhost:8080/v1",
        max_tokens: int = 4096,
    ) -> None:
        super().__init__(
            base_url=base_url,
            model=model,
            max_tokens=max_tokens,
            api_key="llama-cpp",
            provider_name="llama-cpp",
        )


# ---------------------------------------------------------------------------
# vLLM
# ---------------------------------------------------------------------------


class VLLMProvider(OpenAICompatibleProvider):
    """Execution provider for vLLM's OpenAI-compatible server.

    Start the server with::

        python -m vllm.entrypoints.openai.api_server \\
            --model meta-llama/Llama-3-8b-chat-hf --port 8000

    Args:
        model: Model name as served by vLLM.
        base_url: Server URL.  Default ``http://localhost:8000/v1``.
        max_tokens: Default max tokens.
    """

    def __init__(
        self,
        model: str = "default",
        base_url: str = "http://localhost:8000/v1",
        max_tokens: int = 16384,
    ) -> None:
        super().__init__(
            base_url=base_url,
            model=model,
            max_tokens=max_tokens,
            api_key="vllm",
            provider_name="vllm",
        )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

from engine.execution.providers import register_provider  # noqa: E402

register_provider("ollama", OllamaProvider)
register_provider("llama-cpp", LlamaCppProvider)
register_provider("vllm", VLLMProvider)
