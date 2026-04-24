"""OpenAI provider using the official ``openai`` SDK.

Accepts an explicit ``api_key`` or falls back to the ``OPENAI_API_KEY``
environment variable via the SDK's default behaviour.  All SDK errors are
wrapped into :class:`engine.providers.ProviderError` so callers never import
the ``openai`` package directly.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

import openai

from engine.providers import ProviderError
from engine.providers._retry import (
    compute_backoff_delay,
    get_max_attempts,
    parse_retry_after,
)


class OpenAIProvider:
    """Async OpenAI Chat Completions provider.

    Parameters:
        api_key: Explicit API key.  When *None* the SDK reads
            ``OPENAI_API_KEY`` from the environment automatically.
    """

    def __init__(self, api_key: str | None = None) -> None:
        if api_key is not None:
            self.client = openai.AsyncOpenAI(api_key=api_key)
        else:
            self.client = openai.AsyncOpenAI()

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        """Send a single-shot completion request and return the full text.

        Retries transient 429 rate-limit responses with exponential
        backoff; see :mod:`engine.providers._retry` for policy.
        """
        max_attempts = get_max_attempts()
        for attempt in range(max_attempts):
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.choices[0].message.content
            except openai.AuthenticationError as exc:
                raise ProviderError(
                    f"OpenAI authentication failed: {exc}",
                    category="auth",
                    original=exc,
                ) from exc
            except openai.RateLimitError as exc:
                if attempt == max_attempts - 1:
                    raise ProviderError(
                        f"OpenAI rate limit exceeded: {exc}",
                        category="rate_limit",
                        original=exc,
                    ) from exc
                await asyncio.sleep(
                    compute_backoff_delay(
                        attempt, retry_after=parse_retry_after(exc)
                    )
                )
            except openai.APIStatusError as exc:
                raise ProviderError(
                    f"OpenAI API error (status {exc.status_code}): {exc}",
                    category="server",
                    original=exc,
                ) from exc
            except openai.APIError as exc:
                raise ProviderError(
                    f"OpenAI API error: {exc}",
                    category="unknown",
                    original=exc,
                ) from exc
        raise RuntimeError("retry loop exited without returning or raising")

    async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
        """Stream text chunks from a completion request.

        Retries rate-limit failures only before any chunk has been
        yielded — once output has started flowing to the consumer a
        retry would replay text, so we let such errors surface instead.
        """
        max_attempts = get_max_attempts()
        for attempt in range(max_attempts):
            yielded_any = False
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,
                )
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content is not None:
                        yielded_any = True
                        yield chunk.choices[0].delta.content
                return
            except openai.AuthenticationError as exc:
                raise ProviderError(
                    f"OpenAI authentication failed: {exc}",
                    category="auth",
                    original=exc,
                ) from exc
            except openai.RateLimitError as exc:
                if yielded_any or attempt == max_attempts - 1:
                    raise ProviderError(
                        f"OpenAI rate limit exceeded: {exc}",
                        category="rate_limit",
                        original=exc,
                    ) from exc
                await asyncio.sleep(
                    compute_backoff_delay(
                        attempt, retry_after=parse_retry_after(exc)
                    )
                )
            except openai.APIStatusError as exc:
                raise ProviderError(
                    f"OpenAI API error (status {exc.status_code}): {exc}",
                    category="server",
                    original=exc,
                ) from exc
            except openai.APIError as exc:
                raise ProviderError(
                    f"OpenAI API error: {exc}",
                    category="unknown",
                    original=exc,
                ) from exc
