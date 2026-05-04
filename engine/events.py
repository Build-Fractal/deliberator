"""Lifecycle event models and emitter protocol.

Events are frozen Pydantic models emitted at key points during engine
execution.  The ``EventEmitter`` protocol is callback-based with no
transport assumption — callers supply a plain callable, and the engine
invokes it synchronously.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Callable, Protocol, Union

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Event models
# ---------------------------------------------------------------------------

class PhaseStarted(BaseModel):
    """Emitted when a deliberation phase begins."""

    model_config = {"frozen": True}

    phase: str
    agent_count: int
    timestamp: datetime


class AgentDispatched(BaseModel):
    """Emitted when a single agent is sent to the provider.

    The ``model`` field is ``None`` when the dispatch layer did not pin
    a specific model id (issue #54 refactor) — the provider then applies
    its own configured default. Telemetry consumers should display
    ``model`` as ``"(provider-default)"`` or similar when ``None``.
    """

    model_config = {"frozen": True}

    phase: str
    agent_name: str
    model: str | None
    timestamp: datetime


class AgentCompleted(BaseModel):
    """Emitted when a single agent finishes (success or failure)."""

    model_config = {"frozen": True}

    phase: str
    agent_name: str
    success: bool
    error: str | None
    duration_ms: int
    timestamp: datetime
    response_text: str | None = None
    cost_input_tokens: int | None = None
    cost_output_tokens: int | None = None
    cost_usd: float | None = None
    provider: str | None = None


class PhaseCompleted(BaseModel):
    """Emitted when all agents in a phase have finished."""

    model_config = {"frozen": True}

    phase: str
    agent_count: int
    success_count: int
    failure_count: int
    duration_ms: int
    timestamp: datetime


# ---------------------------------------------------------------------------
# Union type
# ---------------------------------------------------------------------------

EngineEvent = Union[PhaseStarted, AgentDispatched, AgentCompleted, PhaseCompleted]


# ---------------------------------------------------------------------------
# Emitter protocol + implementations
# ---------------------------------------------------------------------------

class EventEmitter(Protocol):
    """Protocol for receiving lifecycle events.

    No transport assumption — the emitter simply receives events and
    decides what to do with them (log, store, forward, discard).
    """

    def emit(self, event: EngineEvent) -> None:
        """Handle a lifecycle event."""
        ...


class CallbackEmitter:
    """Emitter that delegates to a plain callable.

    Parameters:
        callback: A function that accepts an :data:`EngineEvent`.
    """

    def __init__(self, callback: Callable[[EngineEvent], None]) -> None:
        self._callback = callback

    def emit(self, event: EngineEvent) -> None:
        self._callback(event)


class NullEmitter:
    """Emitter that silently discards all events.

    Used as the default when no callback is configured so callers don't
    need to check for ``None``.
    """

    def emit(self, event: EngineEvent) -> None:
        pass


class AsyncQueueEmitter:
    """Emitter that bridges sync ``emit()`` calls to an ``asyncio.Queue``.

    Designed for SSE streaming: the engine thread calls ``emit()``
    synchronously, and an async consumer reads events via ``async for``.

    Usage::

        emitter = AsyncQueueEmitter()
        # ... pass emitter to engine ...
        async for event in emitter.events():
            yield f"data: {event.model_dump_json()}\\n\\n"
    """

    def __init__(self) -> None:
        self._queue: asyncio.Queue[EngineEvent | None] = asyncio.Queue()

    def emit(self, event: EngineEvent) -> None:
        """Enqueue an event (non-blocking)."""
        self._queue.put_nowait(event)

    async def events(self) -> AsyncIterator[EngineEvent]:
        """Yield events until the sentinel ``None`` is received."""
        while True:
            event = await self._queue.get()
            if event is None:
                break
            yield event

    def close(self) -> None:
        """Send the sentinel to signal end-of-stream."""
        self._queue.put_nowait(None)
