"""Shared fixtures for engine test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

from engine.config import EngineConfig, parse_config
from engine.events import CallbackEmitter, EngineEvent
from engine.providers import MockProvider


# ---------------------------------------------------------------------------
# Rate-limit retry defaults (autouse)
# ---------------------------------------------------------------------------
#
# The provider layer retries 429s with exponential backoff (see
# ``engine.providers._retry``).  For the test suite we disable retry by
# default so tests that mock a persistent rate-limit error do not sleep
# through multiple backoff intervals.  Tests that explicitly exercise
# retry behavior opt back in via monkeypatch.

@pytest.fixture(autouse=True)
def _disable_rate_limit_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CONVERSUS_RATE_LIMIT_MAX_ATTEMPTS", "1")


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.fixture
def example_config_path() -> Path:
    """Absolute path to conversus.example.yml."""
    return PROJECT_ROOT / "conversus.example.yml"


# ---------------------------------------------------------------------------
# Temporary directories
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_output_dir(tmp_path: Path) -> Path:
    """Fresh temporary directory for engine output."""
    out = tmp_path / "output"
    out.mkdir()
    return out


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_provider() -> MockProvider:
    """A MockProvider with the default canned response."""
    return MockProvider()


@pytest.fixture
def custom_mock_provider():
    """Factory fixture: call with custom response_text."""
    def _factory(response_text: str = "Custom mock response") -> MockProvider:
        return MockProvider(response_text=response_text)
    return _factory


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

@pytest.fixture
def event_collector() -> tuple[CallbackEmitter, list[EngineEvent]]:
    """A CallbackEmitter that appends events to a list.

    Returns (emitter, events_list) so tests can emit and assert.
    """
    events: list[EngineEvent] = []
    emitter = CallbackEmitter(lambda e: events.append(e))
    return emitter, events


# ---------------------------------------------------------------------------
# Pre-parsed config
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_engine_config(example_config_path: Path) -> EngineConfig:
    """Pre-parsed EngineConfig from the example config file."""
    return parse_config(example_config_path)
