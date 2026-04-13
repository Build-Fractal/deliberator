"""Tests for engine.settings — cascading settings resolution (spec 057).

Covers: ConversusSettings defaults, load_settings cascade (project >
global > defaults), nested PersistenceSettings merge, resolve_setting
CLI-flag override, and error handling for malformed YAML.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from engine.settings import (
    ConversusSettings,
    PersistenceSettings,
    load_settings,
    resolve_setting,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_settings(directory: Path, data: dict) -> Path:
    """Write a settings.yml file inside *directory*/.conversus/ and return
    the path to the YAML file."""
    settings_dir = directory / ".conversus"
    settings_dir.mkdir(parents=True, exist_ok=True)
    settings_file = settings_dir / "settings.yml"
    settings_file.write_text(yaml.dump(data, sort_keys=False), encoding="utf-8")
    return settings_file


# ===================================================================
# Defaults
# ===================================================================


class TestDefaults:
    """ConversusSettings() with no args returns all built-in defaults."""

    def test_default_settings(self) -> None:
        """ConversusSettings() with no args returns all defaults."""
        settings = ConversusSettings()
        assert settings.default_provider == "mock"
        assert settings.default_model is None
        assert settings.default_mode == "cooperative"
        assert settings.max_launches == 20

    def test_default_provider_is_mock(self) -> None:
        """The built-in default provider is 'mock' (no API key needed)."""
        settings = ConversusSettings()
        assert settings.default_provider == "mock"

    def test_default_persistence_enabled(self) -> None:
        """Persistence is enabled by default."""
        settings = ConversusSettings()
        assert settings.persistence.enabled is True
        assert settings.persistence.retention_days == 90

    def test_default_persistence_standalone(self) -> None:
        """PersistenceSettings() standalone also has correct defaults."""
        persistence = PersistenceSettings()
        assert persistence.enabled is True
        assert persistence.retention_days == 90


# ===================================================================
# Loading from files
# ===================================================================


class TestLoadFromFiles:
    """load_settings reads the cascade: project > global > defaults."""

    def test_load_settings_from_global(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """~/.conversus/settings.yml values are loaded."""
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        _write_settings(home, {
            "default_provider": "anthropic",
            "default_model": "sonnet",
        })

        # project_root points elsewhere — no project settings
        project = tmp_path / "project"
        project.mkdir()

        settings = load_settings(project_root=project)
        assert settings.default_provider == "anthropic"
        assert settings.default_model == "sonnet"

    def test_load_settings_project_overrides_global(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Project settings override global for the same key."""
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        _write_settings(home, {"default_provider": "anthropic"})
        _write_settings(tmp_path / "project", {"default_provider": "claude-code"})

        settings = load_settings(project_root=tmp_path / "project")
        assert settings.default_provider == "claude-code"

    def test_load_settings_global_fills_gaps(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Project sets provider, global sets model -- both survive."""
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        _write_settings(home, {"default_model": "opus"})
        _write_settings(tmp_path / "project", {"default_provider": "claude-code"})

        settings = load_settings(project_root=tmp_path / "project")
        assert settings.default_provider == "claude-code"
        assert settings.default_model == "opus"

    def test_load_settings_no_files_returns_defaults(self, tmp_path: Path) -> None:
        """When no settings files exist, returns built-in defaults."""
        settings = load_settings(project_root=tmp_path)
        assert settings.default_provider == "mock"
        assert settings.default_model is None
        assert settings.default_mode == "cooperative"
        assert settings.max_launches == 20
        assert settings.persistence.enabled is True

    def test_load_settings_invalid_yaml_returns_defaults(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Malformed YAML in settings file returns defaults with warning."""
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        # Write invalid YAML to global settings
        settings_dir = home / ".conversus"
        settings_dir.mkdir(parents=True, exist_ok=True)
        (settings_dir / "settings.yml").write_text(
            "{{invalid: yaml: [unterminated", encoding="utf-8"
        )

        settings = load_settings(project_root=tmp_path)
        # Should fall back to defaults rather than raising
        assert settings.default_provider == "mock"
        assert settings.default_model is None


# ===================================================================
# Nested persistence settings
# ===================================================================


class TestPersistenceSettingsMerge:
    """Project persistence overrides merge with global without losing keys."""

    def test_persistence_settings_merge(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Project persistence.enabled=false overrides global without
        losing retention_days."""
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        _write_settings(home, {
            "persistence": {"enabled": True, "retention_days": 30},
        })
        _write_settings(tmp_path / "project", {
            "persistence": {"enabled": False},
        })

        settings = load_settings(project_root=tmp_path / "project")
        assert settings.persistence.enabled is False
        # retention_days from global survives because project didn't set it
        assert settings.persistence.retention_days == 30


# ===================================================================
# resolve_setting
# ===================================================================


class TestResolveSetting:
    """resolve_setting: CLI flag (non-None, non-empty) wins over settings."""

    def test_resolve_setting_flag_wins(self) -> None:
        """Non-None flag value overrides the setting."""
        settings = ConversusSettings(default_provider="anthropic")
        result = resolve_setting(settings, "claude-code", "default_provider")
        assert result == "claude-code"

    def test_resolve_setting_falls_through_when_flag_none(self) -> None:
        """None flag value falls through to the setting value."""
        settings = ConversusSettings(default_provider="anthropic")
        result = resolve_setting(settings, None, "default_provider")
        assert result == "anthropic"

    def test_resolve_setting_falls_through_when_flag_empty(self) -> None:
        """Empty string flag value falls through to the setting value."""
        settings = ConversusSettings(default_provider="anthropic")
        result = resolve_setting(settings, "", "default_provider")
        assert result == "anthropic"
