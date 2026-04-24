"""Tests for the rate-limit retry helper module.

Covers the small pure-logic surface in :mod:`engine.providers._retry`:
env var parsing, ``Retry-After`` header extraction, and delay
computation. Provider-level retry integration is covered by
``test_providers.py`` and ``test_execution_providers_anthropic.py``.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from unittest.mock import MagicMock

import pytest

from engine.providers import _retry


# ---------------------------------------------------------------------------
# Env var parsing
# ---------------------------------------------------------------------------


class TestEnvVars:
    def test_max_attempts_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS", raising=False)
        assert _retry.get_max_attempts() == _retry.DEFAULT_MAX_ATTEMPTS

    def test_max_attempts_honours_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS", "7")
        assert _retry.get_max_attempts() == 7

    def test_max_attempts_floors_to_one(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS", "0")
        assert _retry.get_max_attempts() == 1
        monkeypatch.setenv("CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS", "-5")
        assert _retry.get_max_attempts() == 1

    def test_max_attempts_falls_back_on_garbage(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS", "not-a-number")
        assert _retry.get_max_attempts() == _retry.DEFAULT_MAX_ATTEMPTS

    def test_base_delay_honours_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CONVERSUS_RATE_LIMIT_BASE_DELAY", "0.25")
        assert _retry.get_base_delay() == pytest.approx(0.25)

    def test_max_delay_honours_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CONVERSUS_RATE_LIMIT_MAX_DELAY", "2.5")
        assert _retry.get_max_delay() == pytest.approx(2.5)


# ---------------------------------------------------------------------------
# Retry-After parsing
# ---------------------------------------------------------------------------


def _exc_with_retry_after(value: str | None) -> Exception:
    """Build a fake provider error carrying a ``Retry-After`` header."""
    response = MagicMock()
    if value is None:
        response.headers = {}
    else:
        response.headers = {"retry-after": value}
    exc = Exception("rate limit")
    exc.response = response  # type: ignore[attr-defined]
    return exc


class TestParseRetryAfter:
    def test_missing_header_returns_none(self) -> None:
        assert _retry.parse_retry_after(_exc_with_retry_after(None)) is None

    def test_exc_without_response_returns_none(self) -> None:
        assert _retry.parse_retry_after(Exception("no response attr")) is None

    def test_delta_seconds(self) -> None:
        assert _retry.parse_retry_after(_exc_with_retry_after("42")) == pytest.approx(42.0)

    def test_delta_seconds_fractional(self) -> None:
        assert _retry.parse_retry_after(_exc_with_retry_after("2.5")) == pytest.approx(2.5)

    def test_delta_seconds_negative_clamped_to_zero(self) -> None:
        assert _retry.parse_retry_after(_exc_with_retry_after("-1")) == pytest.approx(0.0)

    def test_http_date_future(self) -> None:
        future = datetime.now(timezone.utc) + timedelta(seconds=30)
        value = format_datetime(future, usegmt=True)
        parsed = _retry.parse_retry_after(_exc_with_retry_after(value))
        assert parsed is not None
        # Allow a small tolerance since wall-clock ticks during the call.
        assert 25 <= parsed <= 35

    def test_http_date_past_clamps_to_zero(self) -> None:
        past = datetime.now(timezone.utc) - timedelta(seconds=30)
        value = format_datetime(past, usegmt=True)
        assert _retry.parse_retry_after(_exc_with_retry_after(value)) == pytest.approx(0.0)

    def test_invalid_value_returns_none(self) -> None:
        assert _retry.parse_retry_after(_exc_with_retry_after("not-a-date")) is None

    def test_empty_value_returns_none(self) -> None:
        assert _retry.parse_retry_after(_exc_with_retry_after("   ")) is None


# ---------------------------------------------------------------------------
# Backoff delay
# ---------------------------------------------------------------------------


class TestComputeBackoffDelay:
    def test_retry_after_wins_over_exponential(self) -> None:
        delay = _retry.compute_backoff_delay(
            attempt=5, retry_after=3.0, base_delay=1.0, max_delay=60.0
        )
        assert delay == pytest.approx(3.0)

    def test_retry_after_capped_by_max_delay(self) -> None:
        delay = _retry.compute_backoff_delay(
            attempt=0, retry_after=999.0, base_delay=1.0, max_delay=10.0
        )
        assert delay == pytest.approx(10.0)

    def test_exponential_grows_with_attempt(self) -> None:
        rng = random.Random(0)
        d0 = _retry.compute_backoff_delay(0, base_delay=1.0, max_delay=60.0, rng=rng)
        rng = random.Random(0)
        d1 = _retry.compute_backoff_delay(1, base_delay=1.0, max_delay=60.0, rng=rng)
        assert d1 > d0  # same jitter seed, higher attempt → bigger delay

    def test_exponential_clamped_by_max_delay(self) -> None:
        delay = _retry.compute_backoff_delay(
            attempt=10, base_delay=1.0, max_delay=5.0,
            rng=random.Random(0),
        )
        assert delay <= 5.0

    def test_jitter_range(self) -> None:
        # With base 4.0, attempt 0 → raw 4.0, jittered to [3.0, 5.0].
        for seed in range(20):
            delay = _retry.compute_backoff_delay(
                attempt=0, base_delay=4.0, max_delay=60.0,
                rng=random.Random(seed),
            )
            assert 3.0 <= delay <= 5.0
