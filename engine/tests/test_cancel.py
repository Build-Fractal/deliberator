"""Tests for engine.cancel — cancellation flag and error."""

from __future__ import annotations

import asyncio

from engine.cancel import CancellationFlag, CancelledError


class TestCancellationFlag:
    """CancellationFlag starts False, becomes True after cancel(), stays True."""

    def test_starts_not_cancelled(self) -> None:
        flag = CancellationFlag()
        assert flag.is_cancelled is False

    def test_cancel_sets_true(self) -> None:
        flag = CancellationFlag()
        flag.cancel()
        assert flag.is_cancelled is True

    def test_cancel_stays_true(self) -> None:
        flag = CancellationFlag()
        flag.cancel()
        assert flag.is_cancelled is True
        # Second read still True
        assert flag.is_cancelled is True

    def test_multiple_cancel_calls_idempotent(self) -> None:
        flag = CancellationFlag()
        flag.cancel()
        flag.cancel()
        assert flag.is_cancelled is True


class TestCancelledError:
    """CancelledError is a subclass of asyncio.CancelledError."""

    def test_is_asyncio_cancelled_error(self) -> None:
        exc = CancelledError("deliberation cancelled")
        assert isinstance(exc, asyncio.CancelledError)

    def test_can_be_caught_as_asyncio_cancelled(self) -> None:
        try:
            raise CancelledError("test")
        except asyncio.CancelledError:
            pass  # expected

    def test_distinguishable_from_generic_cancelled(self) -> None:
        exc = CancelledError("engine cancel")
        assert isinstance(exc, CancelledError)
        generic = asyncio.CancelledError()
        assert not isinstance(generic, CancelledError)
