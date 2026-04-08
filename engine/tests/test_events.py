"""Tests for engine.events — lifecycle event models and emitters."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from engine.events import (
    AgentCompleted,
    AgentDispatched,
    AsyncQueueEmitter,
    CallbackEmitter,
    EngineEvent,
    NullEmitter,
    PhaseCompleted,
    PhaseStarted,
)


# ---------------------------------------------------------------------------
# Event construction
# ---------------------------------------------------------------------------

class TestEventConstruction:
    """All 4 event types can be constructed with valid data."""

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def test_phase_started(self) -> None:
        e = PhaseStarted(phase="review", agent_count=3, timestamp=self._now())
        assert e.phase == "review"
        assert e.agent_count == 3

    def test_agent_dispatched(self) -> None:
        e = AgentDispatched(
            phase="review", agent_name="apm", model="claude-sonnet-4-20250514", timestamp=self._now()
        )
        assert e.agent_name == "apm"
        assert e.model == "claude-sonnet-4-20250514"

    def test_agent_completed_success(self) -> None:
        e = AgentCompleted(
            phase="review",
            agent_name="apm",
            success=True,
            error=None,
            duration_ms=150,
            timestamp=self._now(),
        )
        assert e.success is True
        assert e.error is None
        assert e.duration_ms == 150

    def test_agent_completed_failure(self) -> None:
        e = AgentCompleted(
            phase="review",
            agent_name="apm",
            success=False,
            error="RuntimeError: API timeout",
            duration_ms=3000,
            timestamp=self._now(),
        )
        assert e.success is False
        assert "timeout" in e.error.lower()

    def test_phase_completed(self) -> None:
        e = PhaseCompleted(
            phase="review",
            agent_count=3,
            success_count=2,
            failure_count=1,
            duration_ms=500,
            timestamp=self._now(),
        )
        assert e.success_count == 2
        assert e.failure_count == 1


# ---------------------------------------------------------------------------
# Frozen model (immutable after creation)
# ---------------------------------------------------------------------------

class TestEventFrozen:
    """Events cannot be modified after creation."""

    def test_phase_started_frozen(self) -> None:
        e = PhaseStarted(phase="review", agent_count=3, timestamp=datetime.now(timezone.utc))
        with pytest.raises(ValidationError):
            e.phase = "cross-review"

    def test_agent_completed_frozen(self) -> None:
        e = AgentCompleted(
            phase="review",
            agent_name="apm",
            success=True,
            error=None,
            duration_ms=100,
            timestamp=datetime.now(timezone.utc),
        )
        with pytest.raises(ValidationError):
            e.success = False


# ---------------------------------------------------------------------------
# CallbackEmitter
# ---------------------------------------------------------------------------

class TestCallbackEmitter:
    """CallbackEmitter delegates events to the callback."""

    def test_events_received(self) -> None:
        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))

        e1 = PhaseStarted(phase="review", agent_count=2, timestamp=datetime.now(timezone.utc))
        e2 = AgentDispatched(
            phase="review", agent_name="a", model="m", timestamp=datetime.now(timezone.utc)
        )
        emitter.emit(e1)
        emitter.emit(e2)

        assert len(events) == 2
        assert events[0] is e1
        assert events[1] is e2

    def test_multiple_callbacks(self) -> None:
        """Each CallbackEmitter wraps one callback; use multiple for fan-out."""
        events_a: list[EngineEvent] = []
        events_b: list[EngineEvent] = []

        emitter_a = CallbackEmitter(lambda e: events_a.append(e))
        emitter_b = CallbackEmitter(lambda e: events_b.append(e))

        event = PhaseStarted(phase="review", agent_count=1, timestamp=datetime.now(timezone.utc))
        emitter_a.emit(event)
        emitter_b.emit(event)

        assert len(events_a) == 1
        assert len(events_b) == 1


# ---------------------------------------------------------------------------
# NullEmitter
# ---------------------------------------------------------------------------

class TestNullEmitter:
    """NullEmitter silently discards events without raising."""

    def test_emit_does_not_raise(self) -> None:
        emitter = NullEmitter()
        event = PhaseStarted(phase="review", agent_count=1, timestamp=datetime.now(timezone.utc))
        # Should not raise
        emitter.emit(event)
        emitter.emit(event)
        emitter.emit(event)


# ---------------------------------------------------------------------------
# AgentCompleted.response_text
# ---------------------------------------------------------------------------

class TestAgentCompletedResponseText:
    """AgentCompleted has an optional response_text field (default None)."""

    def test_default_none(self) -> None:
        e = AgentCompleted(
            phase="review",
            agent_name="apm",
            success=True,
            error=None,
            duration_ms=100,
            timestamp=datetime.now(timezone.utc),
        )
        assert e.response_text is None

    def test_explicit_value(self) -> None:
        e = AgentCompleted(
            phase="review",
            agent_name="apm",
            success=True,
            error=None,
            duration_ms=100,
            timestamp=datetime.now(timezone.utc),
            response_text="The agent's full response here.",
        )
        assert e.response_text == "The agent's full response here."


# ---------------------------------------------------------------------------
# AsyncQueueEmitter
# ---------------------------------------------------------------------------

class TestAsyncQueueEmitter:
    """AsyncQueueEmitter bridges sync emit() to async event consumption."""

    @pytest.mark.asyncio
    async def test_emit_and_consume(self) -> None:
        emitter = AsyncQueueEmitter()
        e1 = PhaseStarted(phase="review", agent_count=2, timestamp=datetime.now(timezone.utc))
        e2 = PhaseCompleted(
            phase="review", agent_count=2, success_count=2,
            failure_count=0, duration_ms=100, timestamp=datetime.now(timezone.utc),
        )

        emitter.emit(e1)
        emitter.emit(e2)
        emitter.close()

        collected: list[EngineEvent] = []
        async for event in emitter.events():
            collected.append(event)

        assert len(collected) == 2
        assert collected[0] is e1
        assert collected[1] is e2

    @pytest.mark.asyncio
    async def test_close_sends_sentinel(self) -> None:
        emitter = AsyncQueueEmitter()
        emitter.close()

        collected: list[EngineEvent] = []
        async for event in emitter.events():
            collected.append(event)

        assert collected == []

    @pytest.mark.asyncio
    async def test_empty_queue_close(self) -> None:
        """Closing an empty queue should immediately end iteration."""
        emitter = AsyncQueueEmitter()
        emitter.close()

        count = 0
        async for _ in emitter.events():
            count += 1

        assert count == 0

    def test_emit_satisfies_protocol(self) -> None:
        """AsyncQueueEmitter has an emit(EngineEvent) -> None method."""
        emitter = AsyncQueueEmitter()
        event = PhaseStarted(phase="review", agent_count=1, timestamp=datetime.now(timezone.utc))
        # Should not raise
        emitter.emit(event)
