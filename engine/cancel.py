"""Cancellation support for long-running deliberations.

Provides a ``CancellationFlag`` that can be checked between pipeline
phases, and a ``CancelledError`` subclass that distinguishes
engine-initiated cancellation from generic ``asyncio.CancelledError``.
"""

from __future__ import annotations

import asyncio


class CancelledError(asyncio.CancelledError):
    """Raised when an engine deliberation is explicitly cancelled.

    Subclasses ``asyncio.CancelledError`` so existing ``except
    CancelledError`` handlers catch it, while callers that need to
    distinguish engine cancellation from task-level cancellation can
    check ``isinstance(exc, engine.cancel.CancelledError)``.
    """

    pass


class CancellationFlag:
    """Thread-safe flag for cooperative cancellation of deliberations.

    Usage::

        flag = CancellationFlag()
        # ... pass to pipeline ...
        flag.cancel()  # triggers cancellation at next check point
    """

    def __init__(self) -> None:
        self._cancelled: bool = False

    def cancel(self) -> None:
        """Signal cancellation."""
        self._cancelled = True

    @property
    def is_cancelled(self) -> bool:
        """Return ``True`` if cancellation has been requested."""
        return self._cancelled
