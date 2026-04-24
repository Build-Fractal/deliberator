"""Rate-limit retry helpers shared by the Anthropic and OpenAI providers.

Conversus fans out multiple agents concurrently using the caller's auth
token, so a 429 from same-tenant contention is common — and transient.
Without retry, a single rate-limit response kills the agent within ~2s
and aborts the deliberation before any gate verdict is produced. This
module adds a small, provider-agnostic backoff around the SDK call.

Retry policy (all configurable via env vars):

- ``CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS`` — max attempts per call
  (default 3). A value of 1 disables retry.
- ``CONVERSUS_RATE_LIMIT_BASE_DELAY`` — seconds of base delay for
  exponential backoff (default 1.0). Delay for attempt ``n`` is
  ``base_delay * 2**n`` with ±25% jitter, clamped to ``max_delay``.
- ``CONVERSUS_RATE_LIMIT_MAX_DELAY`` — per-attempt cap in seconds
  (default 30.0). Also clamps server-provided ``Retry-After`` values so
  a pathological header cannot stall a deliberation indefinitely.

If the 429 response carries a ``Retry-After`` header (delta-seconds or
HTTP-date, per RFC 7231), it is preferred over the exponential-backoff
delay.
"""

from __future__ import annotations

import os
import random
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_BASE_DELAY = 1.0
DEFAULT_MAX_DELAY = 30.0


def get_max_attempts() -> int:
    """Return the configured retry budget (min 1)."""
    raw = os.environ.get("CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS")
    if raw is None:
        return DEFAULT_MAX_ATTEMPTS
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_MAX_ATTEMPTS
    return max(1, value)


def get_base_delay() -> float:
    """Return the configured base delay in seconds (clamped ≥ 0)."""
    raw = os.environ.get("CONVERSUS_RATE_LIMIT_BASE_DELAY")
    if raw is None:
        return DEFAULT_BASE_DELAY
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_BASE_DELAY
    return max(0.0, value)


def get_max_delay() -> float:
    """Return the configured per-attempt max delay (clamped ≥ 0)."""
    raw = os.environ.get("CONVERSUS_RATE_LIMIT_MAX_DELAY")
    if raw is None:
        return DEFAULT_MAX_DELAY
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_MAX_DELAY
    return max(0.0, value)


def parse_retry_after(exc: BaseException) -> float | None:
    """Extract a ``Retry-After`` hint (seconds) from a provider error.

    Both the Anthropic and OpenAI SDKs attach the raw ``httpx.Response``
    to their ``RateLimitError`` instances as ``.response``. This helper
    reads the header without importing either SDK.

    Returns ``None`` when no header is present or the value cannot be
    parsed — callers fall back to exponential backoff in that case.
    """
    response = getattr(exc, "response", None)
    if response is None:
        return None
    headers = getattr(response, "headers", None)
    if headers is None:
        return None
    raw = headers.get("retry-after") or headers.get("Retry-After")
    if raw is None:
        return None
    raw = str(raw).strip()
    if not raw:
        return None
    # RFC 7231 §7.1.3: either delta-seconds or HTTP-date.
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        target = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None
    if target is None:
        return None
    if target.tzinfo is None:
        target = target.replace(tzinfo=timezone.utc)
    delta = (target - datetime.now(timezone.utc)).total_seconds()
    return max(0.0, delta)


def compute_backoff_delay(
    attempt: int,
    *,
    retry_after: float | None = None,
    base_delay: float | None = None,
    max_delay: float | None = None,
    rng: random.Random | None = None,
) -> float:
    """Return seconds to sleep before the next retry attempt.

    A server-provided ``retry_after`` wins (still clamped by
    ``max_delay`` so a bad header cannot stall indefinitely). Otherwise
    uses exponential backoff — ``base_delay * 2**attempt`` with ±25%
    jitter — capped at ``max_delay``.
    """
    if base_delay is None:
        base_delay = get_base_delay()
    if max_delay is None:
        max_delay = get_max_delay()
    if retry_after is not None:
        return min(max(0.0, retry_after), max_delay)
    raw = base_delay * (2**attempt)
    if rng is None:
        jitter = random.uniform(0.75, 1.25)
    else:
        jitter = rng.uniform(0.75, 1.25)
    return min(raw * jitter, max_delay)
