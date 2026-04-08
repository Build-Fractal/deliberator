"""Unit tests for engine.cli.progress — RichProgressHandler."""

from __future__ import annotations

from datetime import datetime, timezone
from io import StringIO

import pytest
from rich.console import Console

from engine.cli.progress import RichProgressHandler
from engine.events import (
    AgentCompleted,
    AgentDispatched,
    PhaseCompleted,
    PhaseStarted,
)

_NOW = datetime.now(tz=timezone.utc)


# ── Fixtures ──────────────────────────────────────────────────────────────


def _make_console(*, force_terminal: bool = False) -> tuple[Console, StringIO]:
    """Create a Console that captures output to a StringIO buffer."""
    buf = StringIO()
    console = Console(file=buf, force_terminal=force_terminal)
    return console, buf


# ── PhaseStarted ──────────────────────────────────────────────────────────


def test_phase_started_renders_phase_name_and_count() -> None:
    console, buf = _make_console()
    handler = RichProgressHandler(console=console)

    handler(PhaseStarted(phase="review", agent_count=3, timestamp=_NOW))

    output = buf.getvalue()
    assert "review" in output
    assert "3 agents" in output
    assert "⏳" in output


# ── AgentDispatched ───────────────────────────────────────────────────────


def test_agent_dispatched_renders_name_and_model() -> None:
    console, buf = _make_console()
    handler = RichProgressHandler(console=console)

    handler(
        AgentDispatched(
            phase="review",
            agent_name="pragmatist",
            model="claude-3-sonnet",
            timestamp=_NOW,
        )
    )

    output = buf.getvalue()
    assert "pragmatist" in output
    assert "claude-3-sonnet" in output
    assert "→" in output


# ── AgentCompleted (success) ──────────────────────────────────────────────


def test_agent_completed_success_renders_checkmark_and_duration() -> None:
    console, buf = _make_console()
    handler = RichProgressHandler(console=console)

    handler(
        AgentCompleted(
            phase="review",
            agent_name="pragmatist",
            success=True,
            error=None,
            duration_ms=1234,
            timestamp=_NOW,
        )
    )

    output = buf.getvalue()
    assert "✓" in output
    assert "pragmatist" in output
    assert "1234ms" in output
    assert "✗" not in output


# ── AgentCompleted (failure) ──────────────────────────────────────────────


def test_agent_completed_failure_renders_x_and_error() -> None:
    console, buf = _make_console()
    handler = RichProgressHandler(console=console)

    handler(
        AgentCompleted(
            phase="review",
            agent_name="devils-advocate",
            success=False,
            error="timeout after 30s",
            duration_ms=30000,
            timestamp=_NOW,
        )
    )

    output = buf.getvalue()
    assert "✗" in output
    assert "devils-advocate" in output
    assert "30000ms" in output
    assert "timeout after 30s" in output


def test_agent_completed_failure_without_error_text() -> None:
    console, buf = _make_console()
    handler = RichProgressHandler(console=console)

    handler(
        AgentCompleted(
            phase="review",
            agent_name="pragmatist",
            success=False,
            error=None,
            duration_ms=500,
            timestamp=_NOW,
        )
    )

    output = buf.getvalue()
    assert "✗" in output
    assert "pragmatist" in output


# ── PhaseCompleted ────────────────────────────────────────────────────────


def test_phase_completed_renders_counts_and_duration() -> None:
    console, buf = _make_console()
    handler = RichProgressHandler(console=console)

    handler(
        PhaseCompleted(
            phase="cross-review",
            agent_count=2,
            success_count=2,
            failure_count=0,
            duration_ms=4567,
            timestamp=_NOW,
        )
    )

    output = buf.getvalue()
    assert "cross-review" in output
    assert "2/2 succeeded" in output
    assert "4567ms" in output
    assert "✓" in output


def test_phase_completed_with_failures() -> None:
    console, buf = _make_console()
    handler = RichProgressHandler(console=console)

    handler(
        PhaseCompleted(
            phase="review",
            agent_count=3,
            success_count=1,
            failure_count=2,
            duration_ms=9000,
            timestamp=_NOW,
        )
    )

    output = buf.getvalue()
    assert "1/3 succeeded" in output


# ── TTY behavior ──────────────────────────────────────────────────────────


def test_non_tty_output_has_no_ansi_escapes() -> None:
    """Console with force_terminal=False produces clean text."""
    console, buf = _make_console(force_terminal=False)
    handler = RichProgressHandler(console=console)

    handler(PhaseStarted(phase="review", agent_count=2, timestamp=_NOW))

    output = buf.getvalue()
    assert "\x1b[" not in output


def test_tty_output_contains_ansi_escapes() -> None:
    """Console with force_terminal=True produces ANSI-styled text."""
    console, buf = _make_console(force_terminal=True)
    handler = RichProgressHandler(console=console)

    handler(PhaseStarted(phase="review", agent_count=2, timestamp=_NOW))

    output = buf.getvalue()
    assert "\x1b[" in output


# ── Callable protocol ────────────────────────────────────────────────────


def test_handler_is_callable() -> None:
    """RichProgressHandler instances are callable (for CallbackEmitter)."""
    handler = RichProgressHandler()
    assert callable(handler)


def test_handler_works_with_callback_emitter() -> None:
    """Verify integration with CallbackEmitter."""
    from engine.events import CallbackEmitter

    console, buf = _make_console()
    handler = RichProgressHandler(console=console)
    emitter = CallbackEmitter(handler)

    emitter.emit(PhaseStarted(phase="synthesis", agent_count=1, timestamp=_NOW))

    output = buf.getvalue()
    assert "synthesis" in output
