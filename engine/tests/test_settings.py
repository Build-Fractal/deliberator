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
    CascadeEntry,
    ConversusSettings,
    PersistenceSettings,
    inspect_settings_cascade,
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


# ===================================================================
# inspect_settings_cascade  (spec 057 SC-003)
# ===================================================================


class TestInspectSettingsCascade:
    """inspect_settings_cascade returns per-field source attribution."""

    @staticmethod
    def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
        for var in (
            "CONVERSUS_DEFAULT_PROVIDER",
            "CONVERSUS_DEFAULT_MODE",
            "CONVERSUS_DEFAULT_MODEL",
            "CONVERSUS_MAX_LAUNCHES",
        ):
            monkeypatch.delenv(var, raising=False)

    def test_inspect_cascade_default_only(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """No YAML, no env vars -> every entry has source='default'."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        entries = inspect_settings_cascade(project_root=tmp_path / "project")

        assert all(isinstance(e, CascadeEntry) for e in entries)
        assert all(e.source == "default" for e in entries)
        assert all(e.source_path is None for e in entries)

        # Defaults match ConversusSettings()
        defaults = ConversusSettings()
        for entry in entries:
            assert entry.value == getattr(defaults, entry.key)

    def test_inspect_cascade_global_only(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Global YAML supplies values; project absent."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        global_file = _write_settings(home, {
            "default_provider": "anthropic",
            "default_model": "sonnet",
        })

        entries = inspect_settings_cascade(project_root=tmp_path / "project")
        by_key = {e.key: e for e in entries}

        assert by_key["default_provider"].source == "global"
        assert by_key["default_provider"].value == "anthropic"
        assert by_key["default_provider"].source_path == global_file

        assert by_key["default_model"].source == "global"
        assert by_key["default_model"].value == "sonnet"

        # Untouched fields fall through to defaults
        assert by_key["default_mode"].source == "default"
        assert by_key["max_launches"].source == "default"

    def test_inspect_cascade_project_overrides_global(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Project YAML wins over global for the same key."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        _write_settings(home, {"default_provider": "anthropic"})
        project = tmp_path / "project"
        project_file = _write_settings(project, {"default_provider": "claude-code"})

        entries = inspect_settings_cascade(project_root=project)
        by_key = {e.key: e for e in entries}

        assert by_key["default_provider"].source == "project"
        assert by_key["default_provider"].value == "claude-code"
        assert by_key["default_provider"].source_path == project_file

    def test_inspect_cascade_env_overrides_yaml(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Environment variables win over both project and global YAML."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        _write_settings(home, {"default_provider": "anthropic"})
        project = tmp_path / "project"
        _write_settings(project, {"default_provider": "claude-code"})

        monkeypatch.setenv("CONVERSUS_DEFAULT_PROVIDER", "openai")

        entries = inspect_settings_cascade(project_root=project)
        by_key = {e.key: e for e in entries}

        assert by_key["default_provider"].source == "env"
        assert by_key["default_provider"].value == "openai"
        assert by_key["default_provider"].source_path is None

    def test_inspect_cascade_env_max_launches_coerced_to_int(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """CONVERSUS_MAX_LAUNCHES is parsed as int when set via env."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setenv("CONVERSUS_MAX_LAUNCHES", "77")

        entries = inspect_settings_cascade(project_root=tmp_path / "project")
        by_key = {e.key: e for e in entries}

        assert by_key["max_launches"].source == "env"
        assert by_key["max_launches"].value == 77

    def test_inspect_cascade_env_invalid_int_falls_through(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Invalid int env value falls through to lower tiers."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setenv("CONVERSUS_MAX_LAUNCHES", "not-an-int")

        entries = inspect_settings_cascade(project_root=tmp_path / "project")
        by_key = {e.key: e for e in entries}

        assert by_key["max_launches"].source == "default"
        assert by_key["max_launches"].value == 20

    def test_inspect_cascade_returns_all_field_count(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Result has exactly one entry per ConversusSettings.model_fields key."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        entries = inspect_settings_cascade(project_root=tmp_path / "project")

        assert len(entries) == len(ConversusSettings.model_fields)
        keys_in_result = {e.key for e in entries}
        assert keys_in_result == set(ConversusSettings.model_fields.keys())

    def test_inspect_cascade_handles_missing_yaml_files(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Missing global and project YAML paths don't raise."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        # nonexistent project path
        entries = inspect_settings_cascade(project_root=tmp_path / "does-not-exist")
        assert all(e.source == "default" for e in entries)
