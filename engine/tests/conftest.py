"""Shared fixtures for engine test suite."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from engine.config import EngineConfig, parse_config
from engine.events import CallbackEmitter, EngineEvent
from engine.providers import MockProvider


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.fixture
def example_config_path() -> Path:
    """Absolute path to deliberator.example.yml."""
    return PROJECT_ROOT / "deliberator.example.yml"


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


# ---------------------------------------------------------------------------
# Settings cascade isolation (spec 061 step 9 P0 infrastructure)
# ---------------------------------------------------------------------------

# Single source of truth for the env vars that participate in the cascade.
# Tests using `clean_settings` get all of these unset before they run.
# Kept in lockstep with engine.settings._ENV_VAR_FOR_FIELD; the unit test
# in test_settings.py asserts the two stay aligned.
_CASCADE_ENV_VARS: tuple[str, ...] = (
    "DELIBERATOR_DEFAULT_PROVIDER",
    "DELIBERATOR_DEFAULT_MODE",
    "DELIBERATOR_DEFAULT_MODEL",
    "DELIBERATOR_MAX_LAUNCHES",
)


@dataclass(frozen=True)
class CleanSettings:
    """Isolated settings environment for cascade tests.

    Provides a tmpfs-rooted ``home`` and ``project`` pair with all
    cascade env vars unset and ``Path.home()`` patched. Tests opt in
    by writing to ``home / ".deliberator" / "settings.yml"`` (global
    layer) or ``project / ".deliberator" / "settings.yml"`` (project
    layer), and by calling ``monkeypatch.setenv`` for the env layer.
    """

    home: Path
    project: Path


@pytest.fixture
def clean_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> CleanSettings:
    """Isolate the settings cascade from the developer's real environment.

    Clears every env var the cascade reads and patches ``Path.home`` to
    a tmp directory so global/project YAML resolution is fully scoped
    to the test. Returns a ``CleanSettings`` with ready-to-use
    ``home`` and ``project`` paths (already mkdir'd).

    Use this whenever a test exercises ``load_settings`` or
    ``inspect_settings_cascade`` and wants to start from a known clean
    slate. Without it, a developer with ``DELIBERATOR_*`` set in their
    shell can have local-only test failures that pass in CI.
    """
    for var in _CASCADE_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    home = tmp_path / "home"
    project = tmp_path / "project"
    home.mkdir()
    project.mkdir()
    monkeypatch.setattr(Path, "home", lambda: home)
    return CleanSettings(home=home, project=project)
