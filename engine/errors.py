"""Web error mapping for engine exceptions.

Provides a ``WebError`` model and ``map_engine_error()`` function that
translates engine-layer exceptions into HTTP-friendly error payloads.
Used by the FastAPI layer to return structured JSON error responses.
"""

from __future__ import annotations

from pydantic import BaseModel

from engine.config import ConfigError
from engine.phases import PipelineError
from engine.providers import ProviderError, ProviderErrorCategory


class WebError(BaseModel):
    """Structured HTTP error response for web consumers.

    Attributes:
        error: Short human-readable error message.
        category: Machine-readable error category (e.g. ``"config_error"``).
        status_code: Suggested HTTP status code.
        detail: Optional longer description or traceback excerpt.
    """

    error: str
    category: str
    status_code: int
    detail: str | None = None


def map_engine_error(exc: Exception) -> WebError:
    """Map an engine exception to a structured ``WebError``.

    Mapping rules (``ProviderError`` categories expanded per spec 042
    binding condition #4):

    - ``ConfigError`` → 400, ``config_error``
    - ``PipelineError`` → 500, ``pipeline_error``
    - ``ProviderError(category="auth")`` → 401, ``auth_error``
    - ``ProviderError(category="rate_limit")`` → 429, ``rate_limit``
    - ``ProviderError(category="server")`` → 502, ``provider_error``
    - ``ProviderError(category="timeout")`` → 504, ``provider_timeout``
    - ``ProviderError(category="subprocess")`` → 502, ``provider_subprocess_error``
    - ``ProviderError(category="network")`` → 502, ``provider_network_error``
    - ``ProviderError(category="malformed")`` → 502, ``provider_malformed_output``
    - ``ProviderError(category="unknown")`` → 502, ``provider_error`` (fallback)
    - ``ValueError`` → 422, ``validation_error``
    - Any other → 500, ``internal_error``

    Args:
        exc: The exception to map.

    Returns:
        A ``WebError`` with appropriate status code and category.
    """
    if isinstance(exc, ConfigError):
        return WebError(
            error=str(exc),
            category="config_error",
            status_code=400,
        )

    if isinstance(exc, ProviderError):
        category: ProviderErrorCategory = getattr(exc, "category", "unknown")
        if category == "auth":
            return WebError(
                error=str(exc),
                category="auth_error",
                status_code=401,
            )
        if category == "rate_limit":
            return WebError(
                error=str(exc),
                category="rate_limit",
                status_code=429,
            )
        if category == "server":
            return WebError(
                error=str(exc),
                category="provider_error",
                status_code=502,
            )
        if category == "timeout":
            return WebError(
                error=str(exc),
                category="provider_timeout",
                status_code=504,
            )
        if category == "subprocess":
            return WebError(
                error=str(exc),
                category="provider_subprocess_error",
                status_code=502,
            )
        if category == "network":
            return WebError(
                error=str(exc),
                category="provider_network_error",
                status_code=502,
            )
        if category == "malformed":
            return WebError(
                error=str(exc),
                category="provider_malformed_output",
                status_code=502,
            )
        # Fallback for "unknown" and any future category additions.  The
        # 502 status code is first-class API surface for generic provider
        # failures — see :data:`engine.providers.ProviderErrorCategory`.
        return WebError(
            error=str(exc),
            category="provider_error",
            status_code=502,
        )

    if isinstance(exc, PipelineError):
        return WebError(
            error=str(exc),
            category="pipeline_error",
            status_code=500,
        )

    if isinstance(exc, ValueError):
        return WebError(
            error=str(exc),
            category="validation_error",
            status_code=422,
        )

    # Catch-all
    return WebError(
        error=str(exc),
        category="internal_error",
        status_code=500,
    )
