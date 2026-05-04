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
# Fail-fast detection for provider error strings returned as agent content.
# ---------------------------------------------------------------------------
#
# Some provider transports (notably the claude-code subprocess against an
# OAuth session that lacks access to the requested model) return their error
# message as the assistant's response text rather than as a structured error.
# Without this guard, the engine writes the error string into every per-agent
# artifact, the pipeline "completes" all 5 phases, and the user sees a
# successful-looking deliberation built entirely on the same error message.
#
# Patterns must be specific enough not to false-positive on legitimate
# discussions of LLM error handling. The substring is matched
# case-insensitively against the leading 1KB of the response.

PROVIDER_PASSTHROUGH_ERROR_PATTERNS: tuple[str, ...] = (
    # claude-code OAuth: model id not reachable by the session
    "there's an issue with the selected model",
)


class FatalProviderResponseError(Exception):
    """Raised when a provider returns an error message in place of agent
    content. Aborts the pipeline so the error doesn't propagate silently
    into the synthesis as if it were valid deliberation output.
    """


def _detect_provider_passthrough_error(content: str | None) -> str | None:
    """Return the matched pattern if *content* looks like a provider error
    string masquerading as agent output, else ``None``.
    """
    if not content:
        return None
    head = content[:1000].lower()
    for pattern in PROVIDER_PASSTHROUGH_ERROR_PATTERNS:
        if pattern in head:
            return pattern
    return None


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
        model: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        name: str = "model-provider-adapter",
    ) -> None:
        self._inner = inner
        # ``None`` resolves to DEFAULT_MODEL at adapter construction
        # time (the underlying ModelProvider.complete contract is
        # non-Optional). The adapter's own contract surfaces None
        # cleanly to callers, but it must pass a concrete string into
        # the legacy completion API. Per issue #54: the adapter is the
        # boundary between Optional[str] dispatch and concrete-string
        # completion calls.
        self._model = model if model is not None else DEFAULT_MODEL
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

        # Read token usage off the wrapped ModelProvider's side-channel,
        # if it implements one.  ``AnthropicProvider`` and ``OpenAIProvider``
        # populate ``last_usage`` after ``complete()``; providers that do
        # not implement the side-channel get ``cost=None`` (preserving the
        # "unknown ≠ zero" semantics of binding condition #5).
        cost: Cost | None = None
        usage = getattr(self._inner, "last_usage", None)
        if usage:
            try:
                cost = Cost(
                    input_tokens=int(usage.get("input_tokens", 0) or 0),
                    output_tokens=int(usage.get("output_tokens", 0) or 0),
                    usd=None,
                )
            except (AttributeError, TypeError, ValueError):
                cost = None

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=response_text,
            error=None,
            cost=cost,
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
    model: str | None,
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
        model: LLM model identifier, or ``None`` to use the provider's
            own default. Passing ``None`` is the canonical way to say
            "no model override" — providers see ``task.metadata["model"]``
            as ``None`` and apply their own configured default. Issue #54
            refactor (PR #128) replaced the prior value-blocklist guard
            in ``claude_code.py`` with this contract; the dispatch layer
            no longer leaks ``DEFAULT_MODEL`` as a sentinel that providers
            had to special-case.
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
        # Streaming path requires a concrete model id (the legacy
        # ModelProvider.stream signature is non-Optional). Resolve
        # None to DEFAULT_MODEL at this boundary; the issue #54
        # contract is preserved for the non-streaming path which is
        # the dominant code path.
        stream_model = model if model is not None else DEFAULT_MODEL
        try:
            chunks: list[str] = []
            async for chunk in provider.stream(prompt, stream_model, max_tokens):
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
        # ModelProviderExecutionAdapter resolves None internally to its
        # configured default model.
        exec_provider = ModelProviderExecutionAdapter(
            provider,
            model=model,
            max_tokens=max_tokens,
            name=getattr(provider, "name", "model-provider-adapter")
            if hasattr(provider, "name")
            else "model-provider-adapter",
        )

    # task.metadata["model"] carries None when the caller wants the
    # provider's own default (issue #54 contract). Providers that read
    # this metadata MUST treat None as "no override" and fall back to
    # their configured default. Do NOT substitute DEFAULT_MODEL here —
    # that re-introduces the silent leak the issue #54 refactor removed.
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

        # Fail-fast: if the provider returned an error message in place of
        # agent content (e.g., claude-code OAuth on an unreachable model),
        # surface it loudly rather than writing the error string into the
        # artifact and letting the pipeline synthesize stub deliberation.
        matched = _detect_provider_passthrough_error(response_text)
        if matched is not None:
            error_msg = (
                f"Provider returned error message in place of agent response "
                f"(matched pattern: {matched!r}). Verify the configured model "
                f"is reachable from this session. First 500 chars: "
                f"{response_text.strip()[:500]}"
            )
            emitter.emit(AgentCompleted(
                phase=phase,
                agent_name=agent_name,
                success=False,
                error=error_msg,
                duration_ms=duration_ms,
                timestamp=datetime.now(timezone.utc),
            ))
            raise FatalProviderResponseError(error_msg)

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
    model: str | None,
    max_tokens: int,
    provider: AnyProvider,
    emitter: EventEmitter,
    *,
    phase: str = "review",
    agent_providers: dict[str, AnyProvider] | None = None,
    agent_models: dict[str, str | None] | None = None,
    agent_timeouts: dict[str, int] | None = None,
) -> list[tuple[str, str, str | None]]:
    """Dispatch all agents in a phase concurrently.

    Uses ``asyncio.gather(return_exceptions=True)`` so that one agent
    failing does not crash others.

    Args:
        agents: List of ``(agent_name, filled_prompt)`` tuples.
        model: LLM model identifier (default for all agents), or
            ``None`` to use each provider's own default. See
            :func:`dispatch_agent` docstring for the contract.
        max_tokens: Maximum tokens for each response.
        provider: Default ``ExecutionProvider`` for agents without an
            override in *agent_providers*.
        emitter: Event emitter for lifecycle events.
        phase: Phase name for event tagging (default ``"review"``).
        agent_providers: Optional per-agent provider overrides.  Keys
            are agent names; values are ``ExecutionProvider`` instances.
            Agents not in this dict use the default *provider*.
        agent_models: Optional per-agent model overrides.  Keys are
            agent names; values are model identifier strings or
            ``None`` (provider-default). Agents not in this dict use
            the default *model*.

    Returns:
        List of ``(agent_name, response_text, error_or_none)`` in the
        same order as the input agents list.
    """
    _providers = agent_providers or {}
    _models = agent_models or {}
    _timeouts = agent_timeouts or {}

    # Per-provider concurrency gating.  Providers that declare an
    # ``effective_concurrency`` (e.g., :class:`AnthropicProvider` when
    # authenticated with a subscription OAuth token) have a per-instance
    # ceiling that, if exceeded, produces 429s that cascade into phase
    # failure.  Providers that don't expose the property pass through
    # ungated — API-key users keep the current fan-out behavior.
    provider_sems: dict[int, asyncio.Semaphore] = {}

    def _sem_for(prov: AnyProvider) -> asyncio.Semaphore | None:
        cap = getattr(prov, "effective_concurrency", None)
        if cap is None:
            return None
        key = id(prov)
        sem = provider_sems.get(key)
        if sem is None:
            sem = asyncio.Semaphore(cap)
            provider_sems[key] = sem
        return sem

    async def _gated_dispatch(
        name: str,
        prompt: str,
        prov: AnyProvider,
    ) -> tuple[str, str | None]:
        """Per-agent dispatch wrapped in optional provider concurrency gate.

        **Concurrency model** (issue #61): this function IS invoked
        concurrently across agents. The caller builds one coroutine per
        agent (line ~510 below) and runs them all through
        ``asyncio.gather(*tasks, return_exceptions=True)``. Concurrency is
        bounded per-provider by the ``provider_sems`` semaphore (capped at
        the provider's ``effective_concurrency`` if it exposes one), not
        sequential.

        **Fail-fast invariant**: ``FatalProviderResponseError`` is raised
        from inside ``dispatch_agent`` when the provider returns an error
        string as content (PR #52 Bug 3a). With ``return_exceptions=True``
        the exception is collected as a result value, then the
        post-``gather`` loop (below) re-raises the FIRST occurrence.
        Concurrent peers complete before the re-raise — their results are
        discarded but their side-effects (events emitted, sub-tasks
        already in flight) cannot be undone. Acceptable trade-off given
        ``effective_concurrency`` caps the blast radius.

        The 2026-04-29 session-review deliberation characterized this as
        "_gated_dispatch is not invoked concurrently in the current
        engine" — that statement is structurally incorrect against the
        code as it stands; the fail-fast pattern works because of
        ``return_exceptions=True`` + sequential post-processing, not
        because dispatch is sequential.
        """
        sem = _sem_for(prov)
        if sem is None:
            return await dispatch_agent(
                prompt=prompt,
                agent_name=name,
                model=_models.get(name, model),
                max_tokens=max_tokens,
                provider=prov,
                emitter=emitter,
                phase=phase,
                timeout=_timeouts.get(name),
            )
        async with sem:
            return await dispatch_agent(
                prompt=prompt,
                agent_name=name,
                model=_models.get(name, model),
                max_tokens=max_tokens,
                provider=prov,
                emitter=emitter,
                phase=phase,
                timeout=_timeouts.get(name),
            )

    tasks = [
        _gated_dispatch(name, prompt, _providers.get(name, provider))
        for name, prompt in agents
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    output: list[tuple[str, str, str | None]] = []
    for i, result in enumerate(results):
        agent_name = agents[i][0]
        if isinstance(result, FatalProviderResponseError):
            # Provider returned an error string as agent content. Abort the
            # whole pipeline rather than letting it propagate as valid
            # deliberation output.
            raise result
        if isinstance(result, BaseException):
            # Unexpected exception that wasn't caught by dispatch_agent
            output.append((agent_name, "", f"Unhandled: {type(result).__name__}: {result}"))
        else:
            response_text, error = result
            output.append((agent_name, response_text, error))

    return output
