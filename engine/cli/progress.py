"""Rich-based progress handler for deliberation engine events.

Renders lifecycle events to stderr using Rich formatting. When the
output stream is not a TTY (piped), Rich automatically strips ANSI
escape sequences — producing clean, human-readable text.

Usage::

    from engine.cli.progress import RichProgressHandler
    from engine.events import CallbackEmitter

    handler = RichProgressHandler()
    emitter = CallbackEmitter(handler)
    # engine emits events → handler renders them on stderr
"""

from __future__ import annotations

from rich.console import Console

from engine.events import (
    AgentCompleted,
    AgentDispatched,
    EngineEvent,
    PhaseCompleted,
    PhaseStarted,
)


class RichProgressHandler:
    """Callable event handler that renders engine events via Rich.

    Compatible with :class:`engine.events.CallbackEmitter` — pass an
    instance directly as the callback::

        emitter = CallbackEmitter(RichProgressHandler())

    Parameters:
        console: Rich Console to render to. Defaults to
                 ``Console(stderr=True)`` so progress output goes to
                 stderr while result output goes to stdout.
    """

    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console(stderr=True)

    def __call__(self, event: EngineEvent) -> None:
        """Dispatch an engine event to the appropriate renderer."""
        if isinstance(event, PhaseStarted):
            self._console.log(
                f"⏳ Phase: {event.phase} ({event.agent_count} agents)"
            )
        elif isinstance(event, AgentDispatched):
            self._console.log(
                f"  → {event.agent_name} dispatched to {event.model}"
            )
        elif isinstance(event, AgentCompleted):
            marker = "✓" if event.success else "✗"
            msg = f"  {marker} {event.agent_name} ({event.duration_ms}ms)"
            if not event.success and event.error:
                msg += f" — {event.error}"
            self._console.log(msg)
        elif isinstance(event, PhaseCompleted):
            self._console.log(
                f"✓ Phase: {event.phase} — "
                f"{event.success_count}/{event.agent_count} succeeded "
                f"({event.duration_ms}ms)"
            )
