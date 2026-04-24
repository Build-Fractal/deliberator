"""OpenAI provider using the official ``openai`` SDK.

Accepts an explicit ``api_key`` or falls back to the ``OPENAI_API_KEY``
environment variable via the SDK's default behaviour.  All SDK errors are
wrapped into :class:`engine.providers.ProviderError` so callers never import
the ``openai`` package directly.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import openai

from engine.providers import ProviderError


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

        # Token usage from the most recent successful call.  Side-channel
        # for the ModelProviderExecutionAdapter: the ``ModelProvider``
        # protocol returns text only, so the SDK's ``response.usage`` is
        # captured here.  ``None`` until the first successful call that
        # carries usage data.  For streaming, populated from the final
        # chunk's ``usage`` field when ``stream_options`` requests it.
        self.last_usage: dict[str, int] | None = None

    def _record_usage(self, usage: object | None) -> None:
        """Capture ``response.usage`` into :attr:`last_usage` (best-effort)."""
        if usage is None:
            return
        try:
            input_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
            output_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        except (TypeError, ValueError):
            return
        self.last_usage = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        """Send a single-shot completion request and return the full text."""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            self._record_usage(getattr(response, "usage", None))
            return response.choices[0].message.content
        except openai.AuthenticationError as exc:
            raise ProviderError(
                f"OpenAI authentication failed: {exc}",
                category="auth",
                original=exc,
            ) from exc
        except openai.RateLimitError as exc:
            raise ProviderError(
                f"OpenAI rate limit exceeded: {exc}",
                category="rate_limit",
                original=exc,
            ) from exc
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

    async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
        """Stream text chunks from a completion request.

        Requests ``stream_options={"include_usage": True}`` so the final
        chunk carries the cumulative ``usage`` counters; that chunk has
        no choices/content, so the loop simply records usage and skips.
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                stream_options={"include_usage": True},
            )
            async for chunk in response:
                # The usage-only final chunk has no choices.
                chunk_usage = getattr(chunk, "usage", None)
                if chunk_usage is not None:
                    self._record_usage(chunk_usage)
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except openai.AuthenticationError as exc:
            raise ProviderError(
                f"OpenAI authentication failed: {exc}",
                category="auth",
                original=exc,
            ) from exc
        except openai.RateLimitError as exc:
            raise ProviderError(
                f"OpenAI rate limit exceeded: {exc}",
                category="rate_limit",
                original=exc,
            ) from exc
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
