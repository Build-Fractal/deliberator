"""Anthropic Claude provider using the official ``anthropic`` SDK.

Reads ``ANTHROPIC_API_KEY`` from the environment via the SDK's default
behaviour (no explicit key parameter).  All SDK errors are wrapped into
:class:`engine.providers.ProviderError` so callers never import the
``anthropic`` package directly.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import anthropic

from engine.providers import ProviderError

# Version string for stealth headers. Derived from installed Claude Code
# binary at import time; falls back to "unknown" if not installed.
import subprocess as _subprocess

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
        if auth_token is not None and is_oauth_token(auth_token):
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

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        """Send a single-shot completion request and return the full text."""
        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except anthropic.AuthenticationError as exc:
            raise ProviderError(
                f"Anthropic authentication failed: {exc}",
                category="auth",
                original=exc,
            ) from exc
        except anthropic.RateLimitError as exc:
            raise ProviderError(
                f"Anthropic rate limit exceeded: {exc}",
                category="rate_limit",
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

    async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
        """Stream text chunks from a completion request."""
        try:
            async with self.client.messages.stream(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except anthropic.AuthenticationError as exc:
            raise ProviderError(
                f"Anthropic authentication failed: {exc}",
                category="auth",
                original=exc,
            ) from exc
        except anthropic.RateLimitError as exc:
            raise ProviderError(
                f"Anthropic rate limit exceeded: {exc}",
                category="rate_limit",
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
