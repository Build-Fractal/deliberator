"""Tests for engine.errors — WebError model and map_engine_error()."""

from __future__ import annotations

import pytest

from engine.config import ConfigError
from engine.errors import WebError, map_engine_error
from engine.phases import PipelineError
from engine.providers import ProviderError


class TestWebError:
    """WebError is a valid Pydantic model with expected fields."""

    def test_construction(self) -> None:
        err = WebError(error="bad config", category="config_error", status_code=400)
        assert err.error == "bad config"
        assert err.category == "config_error"
        assert err.status_code == 400
        assert err.detail is None

    def test_with_detail(self) -> None:
        err = WebError(
            error="server error",
            category="internal_error",
            status_code=500,
            detail="traceback here",
        )
        assert err.detail == "traceback here"


class TestMapEngineError:
    """map_engine_error() maps each exception type to the correct WebError."""

    def test_config_error(self) -> None:
        exc = ConfigError("Missing target file")
        result = map_engine_error(exc)
        assert result.status_code == 400
        assert result.category == "config_error"
        assert "Missing target file" in result.error

    def test_pipeline_error(self) -> None:
        exc = PipelineError("All agents failed")
        result = map_engine_error(exc)
        assert result.status_code == 500
        assert result.category == "pipeline_error"

    def test_provider_error_auth(self) -> None:
        exc = ProviderError("Invalid API key", category="auth")
        result = map_engine_error(exc)
        assert result.status_code == 401
        assert result.category == "auth_error"

    def test_provider_error_rate_limit(self) -> None:
        exc = ProviderError("Rate limited", category="rate_limit")
        result = map_engine_error(exc)
        assert result.status_code == 429
        assert result.category == "rate_limit"

    def test_provider_error_server(self) -> None:
        exc = ProviderError("Provider down", category="server")
        result = map_engine_error(exc)
        assert result.status_code == 502
        assert result.category == "provider_error"

    def test_provider_error_unknown_category(self) -> None:
        exc = ProviderError("Something weird", category="unknown")
        result = map_engine_error(exc)
        assert result.status_code == 502
        assert result.category == "provider_error"

    def test_value_error(self) -> None:
        exc = ValueError("Invalid input")
        result = map_engine_error(exc)
        assert result.status_code == 422
        assert result.category == "validation_error"

    def test_generic_exception(self) -> None:
        exc = RuntimeError("Unexpected failure")
        result = map_engine_error(exc)
        assert result.status_code == 500
        assert result.category == "internal_error"

    def test_type_error_falls_through(self) -> None:
        exc = TypeError("Wrong type")
        result = map_engine_error(exc)
        assert result.status_code == 500
        assert result.category == "internal_error"
