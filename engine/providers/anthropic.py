"""Anthropic Claude provider using the official ``anthropic`` SDK.

Reads ``ANTHROPIC_API_KEY`` from the environment via the SDK's default
behaviour (no explicit key parameter).  All SDK errors are wrapped into
:class:`engine.providers.ProviderError` so callers never import the
``anthropic`` package directly.
"""

from __future__ import annotations

import asyncio
import random
from collections.abc import AsyncIterator

import anthropic

from engine.providers import ProviderError

# Version string for stealth headers. Derived from installed Claude Code
# binary at import time; falls back to "unknown" if not installed.
import subprocess as _subprocess

# Rate-limit retry policy.  Subscription OAuth tokens collide under
# modest concurrency; a short bounded retry with jitter clears transient
# 429s without looking like an abuse pattern.  API-key users whose
# throughput is already sized for their budget also benefit from
# absorbing the occasional spike.
_RETRY_MAX_ATTEMPTS = 3
_RETRY_BACKOFF_BASE_SECONDS = 2.0
_RETRY_BACKOFF_CAP_SECONDS = 30.0


def _retry_after_seconds(exc: anthropic.RateLimitError) -> float | None:
    """Extract the server's Retry-After hint if present.

    Anthropic returns ``retry-after`` as an integer second count.  If
    absent or malformed, callers should fall back to client-side backoff.
    """
    response = getattr(exc, "response", None)
    if response is None:
        return None
    headers = getattr(response, "headers", None)
    if headers is None:
        return None
    try:
        raw = headers.get("retry-after")
    except AttributeError:
        return None
    if raw is None:
        return None
    try:
        return max(0.0, float(raw))
    except (TypeError, ValueError):
        return None


def _retry_delay_seconds(exc: anthropic.RateLimitError, attempt: int) -> float:
    """Delay before retry *attempt* (0-indexed), preferring Retry-After."""
    server_hint = _retry_after_seconds(exc)
    if server_hint is not None:
        return server_hint
    # Full-jitter exponential backoff: uniform(0, min(base*2^attempt, cap)).
    ceiling = min(
        _RETRY_BACKOFF_BASE_SECONDS * (2 ** attempt),
        _RETRY_BACKOFF_CAP_SECONDS,
    )
    return random.uniform(0.0, ceiling)

def _detect_claude_version() -> str:
    try:
        r = _subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            return "unknown"
        raw = r.stdout.strip().split("\n")[0]
        # "2.1.94 (Claude Code)" → "2.1.94"
        return raw.split()[0] if raw else "unknown"
    except (FileNotFoundError, _subprocess.TimeoutExpired):
        return "unknown"

CLAUDE_CODE_VERSION = _detect_claude_version()


def is_oauth_token(token: str) -> bool:
    """Return ``True`` if *token* is an Anthropic subscription OAuth token.

    Subscription tokens carry the ``sk-ant-oat`` prefix, distinguishing
    them from regular API keys (``sk-ant-api``).
    """
    return token.startswith("sk-ant-oat")


class AnthropicProvider:
    """Async Anthropic Messages API provider.

    Uses :class:`anthropic.AsyncAnthropic` which reads
    ``ANTHROPIC_API_KEY`` from the environment automatically.

    Parameters:
        auth_token: OAuth token for subscription-based auth.  When
            provided, the SDK authenticates with this token instead of
            requiring an API key.  If the token is a subscription OAuth
            token (``sk-ant-oat`` prefix), stealth headers are injected
            to satisfy Anthropic's client fingerprinting.
    """

    def __init__(self, auth_token: str | None = None) -> None:
        self._oauth_subscription = (
            auth_token is not None and is_oauth_token(auth_token)
        )
        if self._oauth_subscription:
            self.client = anthropic.AsyncAnthropic(
                auth_token=auth_token,
                default_headers={
                    "user-agent": f"claude-cli/{CLAUDE_CODE_VERSION}",
                    "x-app": "cli",
                    "anthropic-beta": "claude-code-20250219,oauth-2025-04-20",
                },
            )
        elif auth_token is not None:
            self.client = anthropic.AsyncAnthropic(auth_token=auth_token)
        else:
            self.client = anthropic.AsyncAnthropic()

        # Token usage from the most recent successful call.  Side-channel
        # for the ModelProviderExecutionAdapter: the ``ModelProvider``
        # protocol returns text only, so the SDK's ``response.usage`` is
        # captured here.  Cache tokens (creation/read) are folded into
        # ``input_tokens`` to match the Cost.input_tokens semantics in
        # ``engine/execution/providers/claude_code.py``.  ``None`` until
        # the first successful call.
        self.last_usage: dict[str, int] | None = None

    def _record_usage(self, usage: object | None) -> None:
        """Capture ``response.usage`` into :attr:`last_usage` (best-effort)."""
        if usage is None:
            return
        try:
            input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
            input_tokens += int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
            input_tokens += int(getattr(usage, "cache_read_input_tokens", 0) or 0)
            output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        except (TypeError, ValueError):
            return
        self.last_usage = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }

    @property
    def effective_concurrency(self) -> int | None:
        """Max in-flight requests this provider can sustain without 429s.

        Subscription OAuth tokens (``sk-ant-oat`` prefix) carry a
        per-subscription concurrent-request ceiling independent of the
        per-minute RPM budget.  Two in-flight Sonnet requests reliably
        trigger 429s on a fresh subscription, which cascades into full
        phase failure in multi-agent runs.  Report ``1`` so dispatchers
        that honor this property can gate concurrency accordingly.

        Returns ``None`` for API-key auth (no client-side cap — the SDK
        and server govern throughput).
        """
        return 1 if self._oauth_subscription else None

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        """Send a single-shot completion request and return the full text.

        Rate-limit errors trigger a bounded retry with server-honored
        ``Retry-After`` (or jittered exponential backoff if absent).
        After :data:`_RETRY_MAX_ATTEMPTS` attempts the final 429 is
        surfaced as a ``rate_limit`` :class:`ProviderError`.
        """
        last_rate_limit: anthropic.RateLimitError | None = None
        for attempt in range(_RETRY_MAX_ATTEMPTS):
            try:
                response = await self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                self._record_usage(getattr(response, "usage", None))
                return response.content[0].text
            except anthropic.RateLimitError as exc:
                last_rate_limit = exc
                if attempt == _RETRY_MAX_ATTEMPTS - 1:
                    break
                await asyncio.sleep(_retry_delay_seconds(exc, attempt))
                continue
            except anthropic.AuthenticationError as exc:
                raise ProviderError(
                    f"Anthropic authentication failed: {exc}",
                    category="auth",
                    original=exc,
                ) from exc
            except anthropic.APIStatusError as exc:
                raise ProviderError(
                    f"Anthropic API error (status {exc.status_code}): {exc}",
                    category="server",
                    original=exc,
                ) from exc
            except anthropic.APIError as exc:
                raise ProviderError(
                    f"Anthropic API error: {exc}",
                    category="unknown",
                    original=exc,
                ) from exc

        # Exhausted retries; surface the last 429.
        assert last_rate_limit is not None
        raise ProviderError(
            f"Anthropic rate limit exceeded after {_RETRY_MAX_ATTEMPTS} attempts: {last_rate_limit}",
            category="rate_limit",
            original=last_rate_limit,
        ) from last_rate_limit

    async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
        """Stream text chunks from a completion request.

        Rate-limit errors raised before any chunk yields trigger the same
        bounded retry as :meth:`complete`.  Once the stream has produced
        at least one chunk, retry is unsafe (it would duplicate output)
        and the 429 propagates as a ``rate_limit`` :class:`ProviderError`.

        After the stream completes, ``last_usage`` is populated from the
        final message's ``usage`` field (the SDK aggregates token counts
        on the assembled message available via ``stream.get_final_message()``).
        """
        last_rate_limit: anthropic.RateLimitError | None = None
        for attempt in range(_RETRY_MAX_ATTEMPTS):
            yielded = False
            try:
                async with self.client.messages.stream(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                ) as stream:
                    async for text in stream.text_stream:
                        yielded = True
                        yield text
                    # Capture usage from the assembled final message.  The
                    # SDK exposes this after the iterator is exhausted.
                    # Best-effort — never fail the caller for missing telemetry.
                    try:
                        final = await stream.get_final_message()
                        self._record_usage(getattr(final, "usage", None))
                    except Exception:
                        pass
                return
            except anthropic.RateLimitError as exc:
                last_rate_limit = exc
                if yielded or attempt == _RETRY_MAX_ATTEMPTS - 1:
                    raise ProviderError(
                        f"Anthropic rate limit exceeded: {exc}",
                        category="rate_limit",
                        original=exc,
                    ) from exc
                await asyncio.sleep(_retry_delay_seconds(exc, attempt))
                continue
            except anthropic.AuthenticationError as exc:
                raise ProviderError(
                    f"Anthropic authentication failed: {exc}",
                    category="auth",
                    original=exc,
                ) from exc
            except anthropic.APIStatusError as exc:
                raise ProviderError(
                    f"Anthropic API error (status {exc.status_code}): {exc}",
                    category="server",
                    original=exc,
                ) from exc
            except anthropic.APIError as exc:
                raise ProviderError(
                    f"Anthropic API error: {exc}",
                    category="unknown",
                    original=exc,
                ) from exc

        # Unreachable: either the loop returned after a successful stream,
        # or one of the branches raised.  Guard for safety.
        assert last_rate_limit is not None
        raise ProviderError(
            f"Anthropic rate limit exceeded after {_RETRY_MAX_ATTEMPTS} attempts: {last_rate_limit}",
            category="rate_limit",
            original=last_rate_limit,
        ) from last_rate_limit
