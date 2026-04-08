"""Tests for ModelProvider implementations — OpenAI and Anthropic.

Validates protocol conformance, success paths (complete and stream),
error-category mapping, and constructor parameterisation.
All tests use mocked SDK clients — no real API calls are made.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import openai
import pytest

from engine.providers import ModelProvider, ProviderError
from engine.providers.anthropic import AnthropicProvider, CLAUDE_CODE_VERSION, is_oauth_token
from engine.providers.openai import OpenAIProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _openai_response(content: str) -> MagicMock:
    """Build a mock ChatCompletion response with a single choice."""
    message = MagicMock()
    message.content = content
    choice = MagicMock()
    choice.message = message
    response = MagicMock()
    response.choices = [choice]
    return response


def _openai_stream_chunks(texts: list[str | None]) -> AsyncIterator:
    """Build an async iterator of mock streaming chunks.

    Each entry becomes one ``chunk.choices[0].delta.content``.  ``None``
    entries simulate chunks with no content (e.g. role-only deltas).
    """

    async def _gen():
        for text in texts:
            delta = MagicMock()
            delta.content = text
            choice = MagicMock()
            choice.delta = delta
            chunk = MagicMock()
            chunk.choices = [choice]
            yield chunk

    return _gen()


def _mock_httpx_response(status_code: int = 500) -> httpx.Response:
    """Create a minimal httpx.Response for constructing OpenAI SDK errors."""
    return httpx.Response(
        status_code=status_code,
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )


def _mock_httpx_request() -> httpx.Request:
    """Create a minimal httpx.Request for constructing ``openai.APIError``."""
    return httpx.Request("POST", "https://api.openai.com/v1/chat/completions")


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


class TestProtocolConformance:
    """Verify both providers satisfy the ``ModelProvider`` runtime protocol."""

    def test_openai_satisfies_protocol(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        assert isinstance(provider, ModelProvider)

    def test_anthropic_satisfies_protocol(self) -> None:
        provider = AnthropicProvider()
        assert isinstance(provider, ModelProvider)

    def test_mock_provider_satisfies_protocol(self) -> None:
        from engine.providers import MockProvider

        provider = MockProvider()
        assert isinstance(provider, ModelProvider)


# ---------------------------------------------------------------------------
# OpenAI — success paths
# ---------------------------------------------------------------------------


class TestOpenAIComplete:
    """Test the ``complete`` method returns full text from the API response."""

    async def test_complete_success(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        mock_create = AsyncMock(return_value=_openai_response("Hello, world!"))
        provider.client.chat.completions.create = mock_create

        result = await provider.complete(prompt="Hi", model="gpt-4o", max_tokens=100)

        assert result == "Hello, world!"
        mock_create.assert_awaited_once_with(
            model="gpt-4o",
            max_tokens=100,
            messages=[{"role": "user", "content": "Hi"}],
        )


class TestOpenAIStream:
    """Test the ``stream`` method yields text chunks, skipping None deltas."""

    async def test_stream_success(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        chunks = _openai_stream_chunks(["Hello", None, ", ", "world", None, "!"])
        mock_create = AsyncMock(return_value=chunks)
        provider.client.chat.completions.create = mock_create

        collected: list[str] = []
        async for text in provider.stream(prompt="Hi", model="gpt-4o", max_tokens=100):
            collected.append(text)

        assert collected == ["Hello", ", ", "world", "!"]
        mock_create.assert_awaited_once_with(
            model="gpt-4o",
            max_tokens=100,
            messages=[{"role": "user", "content": "Hi"}],
            stream=True,
        )


# ---------------------------------------------------------------------------
# OpenAI — error mapping
# ---------------------------------------------------------------------------


class TestOpenAIErrorMapping:
    """Verify all 4 OpenAI SDK error types map to the correct ProviderError category."""

    async def test_auth_error_on_complete(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.AuthenticationError(
            message="Invalid API key",
            response=_mock_httpx_response(401),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            await provider.complete(prompt="Hi", model="gpt-4o", max_tokens=100)

        assert exc_info.value.category == "auth"
        assert exc_info.value.original is exc

    async def test_rate_limit_error_on_complete(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.RateLimitError(
            message="Rate limit exceeded",
            response=_mock_httpx_response(429),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            await provider.complete(prompt="Hi", model="gpt-4o", max_tokens=100)

        assert exc_info.value.category == "rate_limit"
        assert exc_info.value.original is exc

    async def test_status_error_on_complete(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.APIStatusError(
            message="Internal server error",
            response=_mock_httpx_response(500),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            await provider.complete(prompt="Hi", model="gpt-4o", max_tokens=100)

        assert exc_info.value.category == "server"
        assert exc_info.value.original is exc

    async def test_api_error_on_complete(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.APIError(
            message="Connection error",
            request=_mock_httpx_request(),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            await provider.complete(prompt="Hi", model="gpt-4o", max_tokens=100)

        assert exc_info.value.category == "unknown"
        assert exc_info.value.original is exc

    async def test_auth_error_on_stream(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.AuthenticationError(
            message="Invalid API key",
            response=_mock_httpx_response(401),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            async for _ in provider.stream(prompt="Hi", model="gpt-4o", max_tokens=100):
                pass

        assert exc_info.value.category == "auth"

    async def test_rate_limit_error_on_stream(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.RateLimitError(
            message="Rate limit exceeded",
            response=_mock_httpx_response(429),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            async for _ in provider.stream(prompt="Hi", model="gpt-4o", max_tokens=100):
                pass

        assert exc_info.value.category == "rate_limit"

    async def test_status_error_on_stream(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.APIStatusError(
            message="Bad gateway",
            response=_mock_httpx_response(502),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            async for _ in provider.stream(prompt="Hi", model="gpt-4o", max_tokens=100):
                pass

        assert exc_info.value.category == "server"

    async def test_api_error_on_stream(self) -> None:
        provider = OpenAIProvider(api_key="test-key")
        exc = openai.APIError(
            message="Timeout",
            request=_mock_httpx_request(),
            body=None,
        )
        provider.client.chat.completions.create = AsyncMock(side_effect=exc)

        with pytest.raises(ProviderError) as exc_info:
            async for _ in provider.stream(prompt="Hi", model="gpt-4o", max_tokens=100):
                pass

        assert exc_info.value.category == "unknown"


# ---------------------------------------------------------------------------
# OpenAI — constructor
# ---------------------------------------------------------------------------


class TestOpenAIConstructor:
    """Verify the constructor passes api_key correctly to the SDK client."""

    def test_custom_api_key(self) -> None:
        provider = OpenAIProvider(api_key="sk-test-custom-key")
        assert provider.client.api_key == "sk-test-custom-key"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "sk-env-key"})
    def test_env_api_key(self) -> None:
        provider = OpenAIProvider()
        assert provider.client.api_key == "sk-env-key"


# ---------------------------------------------------------------------------
# Anthropic — stealth headers
# ---------------------------------------------------------------------------


class TestAnthropicStealthHeaders:
    """Verify stealth header injection for OAuth tokens and absence for API keys."""

    def test_oauth_token_gets_stealth_headers(self) -> None:
        """OAuth token (sk-ant-oat prefix) must trigger all 3 stealth headers."""
        provider = AnthropicProvider(auth_token="sk-ant-oat-test123")
        headers = provider.client._custom_headers

        assert headers["user-agent"] == f"claude-cli/{CLAUDE_CODE_VERSION}"
        assert headers["x-app"] == "cli"
        assert headers["anthropic-beta"] == "claude-code-20250219,oauth-2025-04-20"

    def test_api_key_auth_no_stealth_headers(self) -> None:
        """Regular API key (non-OAuth prefix) must NOT get stealth headers."""
        provider = AnthropicProvider(auth_token="sk-ant-abc123")
        headers = provider.client._custom_headers

        assert "user-agent" not in headers
        assert "x-app" not in headers
        assert "anthropic-beta" not in headers

    def test_env_var_auth_no_stealth_headers(self) -> None:
        """No auth_token (env var path) must NOT get stealth headers."""
        provider = AnthropicProvider()
        headers = provider.client._custom_headers

        assert "user-agent" not in headers
        assert "x-app" not in headers
        assert "anthropic-beta" not in headers

    def test_is_oauth_token_helper(self) -> None:
        """is_oauth_token correctly identifies sk-ant-oat prefix tokens."""
        assert is_oauth_token("sk-ant-oat-xxx") is True
        assert is_oauth_token("sk-ant-oat-") is True
        assert is_oauth_token("sk-ant-abc123") is False
        assert is_oauth_token("") is False
        assert is_oauth_token("sk-ant-oatmeal") is True  # prefix match only

    def test_claude_code_version_constant(self) -> None:
        """CLAUDE_CODE_VERSION is detected from binary or 'unknown'."""
        import re

        assert isinstance(CLAUDE_CODE_VERSION, str)
        assert len(CLAUDE_CODE_VERSION) > 0
        # Either semver from installed claude, or "unknown" if not installed
        assert re.match(r"^\d+\.\d+\.\d+$", CLAUDE_CODE_VERSION) or CLAUDE_CODE_VERSION == "unknown", (
            f"Expected semver or 'unknown', got: {CLAUDE_CODE_VERSION}"
        )
