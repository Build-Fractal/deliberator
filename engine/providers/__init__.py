"""Model provider protocol and mock implementation.

The ``ModelProvider`` protocol defines the abstraction boundary between the
engine and LLM APIs.  Any class that implements ``complete`` and ``stream``
with the correct signatures is a valid provider — no base-class inheritance
required.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Literal, Protocol, runtime_checkable

#: Closed set of valid ``ProviderError.category`` values.
#:
#: Expanded per spec 042 binding condition #4 (arbitration 2026-04-05) to
#: cover the full subprocess and HTTP failure matrix.  Each category maps
#: to a distinct failure mode so downstream code can reason about failure
#: without string parsing:
#:
#: - ``"auth"``       — 401/403 from a model or agent API
#: - ``"rate_limit"`` — 429 from a model or agent API
#: - ``"server"``     — 5xx from a model or agent API
#: - ``"timeout"``    — subprocess or HTTP call exceeded its deadline
#: - ``"subprocess"`` — subprocess non-zero exit not captured as another
#:                      category (signal, unexpected termination, missing
#:                      binary, malformed argv)
#: - ``"network"``    — HTTP client failure before the server responded
#:                      (DNS, TCP, TLS, connection refused)
#: - ``"malformed"``  — provider returned output that does not conform to
#:                      the expected structure (JSON parse error, missing
#:                      required fields, schema validation failure)
#: - ``"unknown"``    — first-class fallback, NOT a sentinel: raised by the
#:                      Anthropic and OpenAI model providers on generic SDK
#:                      errors that do not map to a more specific category.
#:                      :func:`engine.errors.map_engine_error` routes it
#:                      through the fallback branch to a 502 response.
ProviderErrorCategory = Literal[
    "auth",
    "rate_limit",
    "server",
    "timeout",
    "subprocess",
    "network",
    "malformed",
    "unknown",
]


@runtime_checkable
class ModelProvider(Protocol):
    """Protocol for LLM completion providers.

    Implementations must supply both a non-streaming ``complete`` method and
    a streaming ``stream`` method.
    """

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        """Return the full text of a single completion."""
        ...

    async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
        """Yield text chunks as they arrive from the provider."""
        ...


class ProviderError(Exception):
    """Typed wrapper for provider-layer failures.

    Used by both :class:`ModelProvider` implementations (raw LLM APIs) and
    :class:`engine.execution.ExecutionProvider` implementations (agentic
    task dispatch).  The category field is the structured signal downstream
    code uses to distinguish failure modes — see
    :data:`ProviderErrorCategory` for the closed 8-value set.

    Attributes:
        category: One of the values in :data:`ProviderErrorCategory`.
        original: The underlying exception from the SDK or subprocess,
            if any.
    """

    category: ProviderErrorCategory
    original: BaseException | None

    def __init__(
        self,
        message: str,
        *,
        category: ProviderErrorCategory = "unknown",
        original: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.category = category
        self.original = original


@dataclass
class _CallRecord:
    """Record of a single MockProvider invocation."""

    method: str
    prompt: str
    model: str
    max_tokens: int


class MockProvider:
    """A test-friendly provider that returns configurable canned text.

    Every call to ``complete`` or ``stream`` is recorded in :attr:`calls` so
    that tests can assert on dispatch behavior.

    Parameters:
        response_text: Template for canned responses.  ``{model}`` is
            replaced with the model name at call time.
    """

    def __init__(self, response_text: str = "[Mock review response for {model}]") -> None:
        self.response_text = response_text
        self.calls: list[_CallRecord] = []

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        self.calls.append(_CallRecord(method="complete", prompt=prompt, model=model, max_tokens=max_tokens))
        return self.response_text.format(model=model)

    async def stream(self, prompt: str, model: str, max_tokens: int) -> AsyncIterator[str]:
        self.calls.append(_CallRecord(method="stream", prompt=prompt, model=model, max_tokens=max_tokens))
        text = self.response_text.format(model=model)
        for word in text.split():
            yield word + " "
