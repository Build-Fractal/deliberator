"""Async agent dispatch with lifecycle event emission.

Dispatches LLM agents concurrently using ``asyncio.gather()`` with
per-agent error isolation.  Emits ``AgentDispatched`` before each call
and ``AgentCompleted`` after (with timing and success/failure state).

**Spec 042 CLI wiring**: :func:`dispatch_agent` and :func:`dispatch_phase`
accept :class:`~engine.execution.ExecutionProvider` directly.  Callers
resolve providers at the top (via :func:`engine.run.resolve_execution_provider`)
and pass the concrete ``ExecutionProvider`` through.  Legacy
``ModelProvider`` instances are wrapped in
:class:`ModelProviderExecutionAdapter` by the resolver before reaching
dispatch — dispatch only speaks ``ExecutionProvider``.

The streaming path is preserved for backward compatibility with callers
that pass a raw ``ModelProvider``: if the provider has a ``stream()``
method and ``streaming=True``, the legacy streaming path runs.  Native
``ExecutionProvider`` instances fall through to the non-streaming path
(streaming is reserved for v2 per spec 042).
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Any

from engine.events import AgentCompleted, AgentDispatched, EventEmitter
from engine.execution import (
    Cost,
    ExecutionResult,
    ExecutionTask,
)
from engine.execution.provider import ExecutionProvider
from engine.providers import ModelProvider, ProviderError

#: Union type for provider arguments.  Dispatch functions accept either
#: an ``ExecutionProvider`` (preferred) or a legacy ``ModelProvider``
#: (wrapped in adapter for backward compatibility).
AnyProvider = ExecutionProvider | ModelProvider

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_MAX_TOKENS = 16384


# ---------------------------------------------------------------------------
# ModelProvider → ExecutionProvider adapter (spec 042 Phase 2.2)
# ---------------------------------------------------------------------------


class ModelProviderExecutionAdapter:
    """Wrap a :class:`ModelProvider` as an :class:`ExecutionProvider`.

    Phase 2.2 of spec 042 requires every dispatch call to flow through
    the :class:`~engine.execution.ExecutionProvider` protocol.  The
    existing ``ModelProvider`` contract (``complete(prompt, model,
    max_tokens) -> str``) is a strict subset of the new task-level
    contract, so an adapter can wrap any ``ModelProvider`` and expose
    it through the new interface without changing the underlying
    implementation.

    The adapter is ``supports_tool_use=False`` because ``ModelProvider``
    is a raw completion API — agents do not have autonomous filesystem
    access.  Callers that need tool use must use a native
    :class:`ExecutionProvider` implementation (``claude-code``,
    ``opencode``) instead of wrapping a ``ModelProvider``.

    The adapter is ``supports_pooling=False`` because any pooling
    behavior lives inside the underlying ``ModelProvider`` SDK (the
    adapter has no state of its own).

    Args:
        inner: The ``ModelProvider`` to wrap.
        model: LLM model identifier to pass to
            :meth:`ModelProvider.complete` on each call.
        max_tokens: Token budget for each completion.
        name: Provider name to report on :attr:`ExecutionResult.provider`.
            Defaults to ``"model-provider-adapter"``; callers wrapping a
            known provider should pass the provider's canonical name
            (e.g., ``"anthropic"``, ``"openai"``, ``"mock"``).
    """

    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(
        self,
        inner: ModelProvider,
        *,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        name: str = "model-provider-adapter",
    ) -> None:
        self._inner = inner
        self._model = model
        self._max_tokens = max_tokens
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        """Execute an :class:`ExecutionTask` via the wrapped ``ModelProvider``.

        Extracts the prompt from ``task.parts`` (joined via
        :attr:`ExecutionTask.prompt`), calls the underlying
        ``complete()`` method, and wraps the text response in an
        :class:`ExecutionResult`.  The task's ``references`` are NOT
        read here — the caller is responsible for inlining file contents
        into the prompt before passing the task to this adapter, because
        :attr:`supports_tool_use` is ``False``.

        Failures from the underlying ``ModelProvider`` are caught and
        converted to an error :class:`ExecutionResult` with the wrapped
        :class:`ProviderError` intact.
        """
        start = time.monotonic()
        try:
            response_text = await self._inner.complete(
                task.prompt,
                self._model,
                self._max_tokens,
            )
        except ProviderError as exc:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=exc,
                cost=None,
                duration=timedelta(seconds=time.monotonic() - start),
                provider=self._name,
                metadata={"model": self._model, "max_tokens": self._max_tokens},
            )
        except Exception as exc:
            wrapped = ProviderError(
                f"{type(exc).__name__}: {exc}",
                category="unknown",
                original=exc,
            )
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=wrapped,
                cost=None,
                duration=timedelta(seconds=time.monotonic() - start),
                provider=self._name,
                metadata={"model": self._model, "max_tokens": self._max_tokens},
            )

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=response_text,
            error=None,
            # ModelProvider does not report cost data — leave None
            # rather than fabricating zero (binding condition #5).
            cost=None,
            duration=timedelta(seconds=time.monotonic() - start),
            provider=self._name,
            metadata={"model": self._model, "max_tokens": self._max_tokens},
        )

    async def execute_batch(
        self,
        tasks: list[ExecutionTask] | tuple[ExecutionTask, ...],
    ) -> list[ExecutionResult]:
        """Default batch implementation via ``asyncio.gather``."""
        return list(await asyncio.gather(*(self.execute(t) for t in tasks)))


# ---------------------------------------------------------------------------
# Single-agent dispatch
# ---------------------------------------------------------------------------

async def dispatch_agent(
    prompt: str,
    agent_name: str,
    model: str,
    max_tokens: int,
    provider: AnyProvider,
    emitter: EventEmitter,
    *,
    phase: str = "review",
    streaming: bool = False,
    stream_callback: Callable[[str], None] | None = None,
    timeout: int | None = None,
) -> tuple[str, str | None]:
    """Dispatch a single agent to the provider.

    Emits ``AgentDispatched`` before the call and ``AgentCompleted``
    after (regardless of success/failure).

    Args:
        prompt: The fully assembled prompt (file contents + filled template).
        agent_name: Human-readable agent name for events.
        model: LLM model identifier.
        max_tokens: Maximum tokens for the response.
        provider: An ``ExecutionProvider`` (preferred) or legacy
            ``ModelProvider``.  If a ``ModelProvider`` is passed, it is
            wrapped in :class:`ModelProviderExecutionAdapter` internally.
        emitter: Event emitter for lifecycle events.
        phase: Phase name for event tagging (default ``"review"``).
        streaming: When ``True`` and *stream_callback* is provided, use
            the provider's ``stream()`` method instead of ``complete()``.
            Only works with ``ModelProvider``; ``ExecutionProvider``
            falls through to the non-streaming path.
        stream_callback: Called with each text chunk during streaming.

    Returns:
        ``(response_text, None)`` on success, or ``("", error_message)``
        on failure.
    """
    emitter.emit(AgentDispatched(
        phase=phase,
        agent_name=agent_name,
        model=model,
        timestamp=datetime.now(timezone.utc),
    ))

    start = time.monotonic()

    # Streaming path stays on the legacy direct-call route: spec 042
    # v1 ExecutionProvider does not implement streaming (the ``stream``
    # flag on ExecutionTask is reserved for v2).  When streaming is
    # needed AND the provider is a ModelProvider with a stream() method,
    # fall back to ``ModelProvider.stream()`` directly.
    if streaming and stream_callback is not None and hasattr(provider, "stream"):
        try:
            chunks: list[str] = []
            async for chunk in provider.stream(prompt, model, max_tokens):
                stream_callback(chunk)
                chunks.append(chunk)
            response = "".join(chunks)

            duration_ms = int((time.monotonic() - start) * 1000)
            emitter.emit(AgentCompleted(
                phase=phase,
                agent_name=agent_name,
                success=True,
                error=None,
                duration_ms=duration_ms,
                timestamp=datetime.now(timezone.utc),
                response_text=response,
            ))
            return (response, None)
        except Exception as exc:
            duration_ms = int((time.monotonic() - start) * 1000)
            error_msg = f"{type(exc).__name__}: {exc}"
            emitter.emit(AgentCompleted(
                phase=phase,
                agent_name=agent_name,
                success=False,
                error=error_msg,
                duration_ms=duration_ms,
                timestamp=datetime.now(timezone.utc),
            ))
            return ("", error_msg)

    # Non-streaming path — route through ExecutionProvider.
    #
    # If the provider is already an ExecutionProvider, use it directly.
    # If it's a legacy ModelProvider, wrap it in the adapter first.
    exec_provider: ExecutionProvider
    if isinstance(provider, ExecutionProvider):
        exec_provider = provider
    else:
        exec_provider = ModelProviderExecutionAdapter(
            provider,
            model=model,
            max_tokens=max_tokens,
            name=getattr(provider, "name", "model-provider-adapter")
            if hasattr(provider, "name")
            else "model-provider-adapter",
        )

    task = ExecutionTask.from_prompt(
        prompt=prompt,
        # The legacy dispatch path does not write to disk — the engine
        # writes output itself based on the returned response text.
        # Synthesize a placeholder output_path so the task shape is
        # valid; downstream consumers of execute() ignore it.
        output_path=f"/dev/null/dispatch-agent/{agent_name}",
        metadata={
            "phase": phase,
            "agent_name": agent_name,
            "model": model,
            "max_tokens": max_tokens,
            **({"timeout": timeout} if timeout is not None else {}),
        },
    )
    result = await exec_provider.execute(task)
    duration_ms = int((time.monotonic() - start) * 1000)

    if result.success:
        response_text = result.content or ""
        emitter.emit(AgentCompleted(
            phase=phase,
            agent_name=agent_name,
            success=True,
            error=None,
            duration_ms=duration_ms,
            timestamp=datetime.now(timezone.utc),
            response_text=response_text,
            cost_input_tokens=result.cost.input_tokens if result.cost else None,
            cost_output_tokens=result.cost.output_tokens if result.cost else None,
            cost_usd=result.cost.usd if result.cost else None,
            provider=result.provider or None,
        ))
        return (response_text, None)

    # Failure path — ExecutionResult carries the error; unpack to the
    # legacy string format for backward compat with existing callers.
    err = result.error
    error_msg = (
        f"{type(err.original).__name__}: {err}"
        if err is not None and err.original is not None
        else (f"ProviderError: {err}" if err is not None else "Unknown error")
    )
    emitter.emit(AgentCompleted(
        phase=phase,
        agent_name=agent_name,
        success=False,
        error=error_msg,
        duration_ms=duration_ms,
        timestamp=datetime.now(timezone.utc),
    ))
    return ("", error_msg)


# ---------------------------------------------------------------------------
# Multi-agent concurrent dispatch
# ---------------------------------------------------------------------------

async def dispatch_phase(
    agents: list[tuple[str, str]],
    model: str,
    max_tokens: int,
    provider: AnyProvider,
    emitter: EventEmitter,
    *,
    phase: str = "review",
    agent_providers: dict[str, AnyProvider] | None = None,
    agent_models: dict[str, str] | None = None,
    agent_timeouts: dict[str, int] | None = None,
) -> list[tuple[str, str, str | None]]:
    """Dispatch all agents in a phase concurrently.

    Uses ``asyncio.gather(return_exceptions=True)`` so that one agent
    failing does not crash others.

    Args:
        agents: List of ``(agent_name, filled_prompt)`` tuples.
        model: LLM model identifier (default for all agents).
        max_tokens: Maximum tokens for each response.
        provider: Default ``ExecutionProvider`` for agents without an
            override in *agent_providers*.
        emitter: Event emitter for lifecycle events.
        phase: Phase name for event tagging (default ``"review"``).
        agent_providers: Optional per-agent provider overrides.  Keys
            are agent names; values are ``ExecutionProvider`` instances.
            Agents not in this dict use the default *provider*.
        agent_models: Optional per-agent model overrides.  Keys are
            agent names; values are model identifier strings.  Agents
            not in this dict use the default *model*.

    Returns:
        List of ``(agent_name, response_text, error_or_none)`` in the
        same order as the input agents list.
    """
    _providers = agent_providers or {}
    _models = agent_models or {}
    _timeouts = agent_timeouts or {}

    tasks = [
        dispatch_agent(
            prompt=prompt,
            agent_name=name,
            model=_models.get(name, model),
            max_tokens=max_tokens,
            provider=_providers.get(name, provider),
            emitter=emitter,
            phase=phase,
            timeout=_timeouts.get(name),
        )
        for name, prompt in agents
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    output: list[tuple[str, str, str | None]] = []
    for i, result in enumerate(results):
        agent_name = agents[i][0]
        if isinstance(result, BaseException):
            # Unexpected exception that wasn't caught by dispatch_agent
            output.append((agent_name, "", f"Unhandled: {type(result).__name__}: {result}"))
        else:
            response_text, error = result
            output.append((agent_name, response_text, error))

    return output
