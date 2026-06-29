"""Tests for engine.settings — cascading settings resolution (spec 057).

Covers: DeliberatorSettings defaults, load_settings cascade (project >
global > defaults), nested PersistenceSettings merge, resolve_setting
CLI-flag override, and error handling for malformed YAML.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from engine.settings import (
    CascadeEntry,
    DeliberatorSettings,
    PersistenceSettings,
    inspect_settings_cascade,
    load_settings,
    resolve_setting,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_settings(directory: Path, data: dict) -> Path:
    """Write a settings.yml file inside *directory*/.deliberator/ and return
    the path to the YAML file."""
    settings_dir = directory / ".deliberator"
    settings_dir.mkdir(parents=True, exist_ok=True)
    settings_file = settings_dir / "settings.yml"
    settings_file.write_text(yaml.dump(data, sort_keys=False), encoding="utf-8")
    return settings_file


# ===================================================================
# Defaults
# ===================================================================


class TestDefaults:
    """DeliberatorSettings() with no args returns all built-in defaults."""

    def test_default_settings(self) -> None:
        """DeliberatorSettings() with no args returns all defaults."""
        settings = DeliberatorSettings()
        assert settings.default_provider == "mock"
        assert settings.default_model is None
        assert settings.default_mode == "cooperative"
        assert settings.max_launches == 20

    def test_default_provider_is_mock(self) -> None:
        """The built-in default provider is 'mock' (no API key needed)."""
        settings = DeliberatorSettings()
        assert settings.default_provider == "mock"

    def test_default_persistence_enabled(self) -> None:
        """Persistence is enabled by default."""
        settings = DeliberatorSettings()
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
        """~/.deliberator/settings.yml values are loaded."""
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
        settings_dir = home / ".deliberator"
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
        settings = DeliberatorSettings(default_provider="anthropic")
        result = resolve_setting(settings, "claude-code", "default_provider")
        assert result == "claude-code"

    def test_resolve_setting_falls_through_when_flag_none(self) -> None:
        """None flag value falls through to the setting value."""
        settings = DeliberatorSettings(default_provider="anthropic")
        result = resolve_setting(settings, None, "default_provider")
        assert result == "anthropic"

    def test_resolve_setting_falls_through_when_flag_empty(self) -> None:
        """Empty string flag value falls through to the setting value."""
        settings = DeliberatorSettings(default_provider="anthropic")
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
            "DELIBERATOR_DEFAULT_PROVIDER",
            "DELIBERATOR_DEFAULT_MODE",
            "DELIBERATOR_DEFAULT_MODEL",
            "DELIBERATOR_MAX_LAUNCHES",
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

        # Defaults match DeliberatorSettings()
        defaults = DeliberatorSettings()
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

        monkeypatch.setenv("DELIBERATOR_DEFAULT_PROVIDER", "openai")

        entries = inspect_settings_cascade(project_root=project)
        by_key = {e.key: e for e in entries}

        assert by_key["default_provider"].source == "env"
        assert by_key["default_provider"].value == "openai"
        assert by_key["default_provider"].source_path is None

    def test_inspect_cascade_env_max_launches_coerced_to_int(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """DELIBERATOR_MAX_LAUNCHES is parsed as int when set via env."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)
        monkeypatch.setenv("DELIBERATOR_MAX_LAUNCHES", "77")

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
        monkeypatch.setenv("DELIBERATOR_MAX_LAUNCHES", "not-an-int")

        entries = inspect_settings_cascade(project_root=tmp_path / "project")
        by_key = {e.key: e for e in entries}

        assert by_key["max_launches"].source == "default"
        assert by_key["max_launches"].value == 20

    def test_inspect_cascade_returns_all_field_count(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Result has exactly one entry per DeliberatorSettings.model_fields key."""
        self._clear_env(monkeypatch)
        home = tmp_path / "home"
        home.mkdir()
        monkeypatch.setattr(Path, "home", lambda: home)

        entries = inspect_settings_cascade(project_root=tmp_path / "project")

        assert len(entries) == len(DeliberatorSettings.model_fields)
        keys_in_result = {e.key for e in entries}
        assert keys_in_result == set(DeliberatorSettings.model_fields.keys())

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


# ===================================================================
# All-five-levels cascade precedence  (spec 061 step 9)
# ===================================================================
#
# These tests use the `clean_settings` conftest fixture (P0 infrastructure
# called out by spec 061 step 9). They exercise `default_provider` — the
# canonical cascade key — at each tier, demonstrating that resolution
# walks the cascade in the documented order.
#
# Existing tests in TestLoadFromFiles and TestInspectSettingsCascade cover
# pairwise comparisons. This class fills the gap with a single, fully-
# populated cascade where every layer holds a *different* value, so the
# precedence ordering is unambiguous.


class TestProviderAllFiveLevels:
    """default_provider resolves correctly when all 5 cascade layers are set.

    Layer ordering, highest → lowest:
        1. CLI flag      (resolve_setting flag_value arg)
        2. Env var       (DELIBERATOR_DEFAULT_PROVIDER)
        3. Project YAML  (<project>/.deliberator/settings.yml)
        4. Global YAML   (~/.deliberator/settings.yml)
        5. Default       (DeliberatorSettings.default_provider = "mock")

    Each test populates layer N with a unique sentinel, then asserts
    `inspect_settings_cascade` reports that layer as the source.
    Removing the highest layer should drop resolution to the next.
    """

    def test_all_five_layers_populated_cli_flag_wins(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """CLI flag dominates env, project, global, defaults."""
        _write_settings(clean_settings.home, {"default_provider": "L4_global"})
        _write_settings(clean_settings.project, {"default_provider": "L3_project"})
        monkeypatch.setenv("DELIBERATOR_DEFAULT_PROVIDER", "L2_env")

        # CLI flag is enforced via resolve_setting (post-cascade).
        # The cascade itself sees only env > project > global > default.
        settings = load_settings(project_root=clean_settings.project)
        assert resolve_setting(settings, "L1_cli_flag", "default_provider") == "L1_cli_flag"

    def test_env_wins_when_no_cli_flag(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """No CLI flag → env var is the highest active layer."""
        _write_settings(clean_settings.home, {"default_provider": "L4_global"})
        _write_settings(clean_settings.project, {"default_provider": "L3_project"})
        monkeypatch.setenv("DELIBERATOR_DEFAULT_PROVIDER", "L2_env")

        entries = inspect_settings_cascade(project_root=clean_settings.project)
        provider = next(e for e in entries if e.key == "default_provider")
        assert provider.source == "env"
        assert provider.value == "L2_env"
        assert provider.source_path is None

    def test_project_wins_when_env_unset(
        self, clean_settings
    ) -> None:
        """No CLI, no env → project YAML wins."""
        _write_settings(clean_settings.home, {"default_provider": "L4_global"})
        project_file = _write_settings(
            clean_settings.project, {"default_provider": "L3_project"}
        )

        entries = inspect_settings_cascade(project_root=clean_settings.project)
        provider = next(e for e in entries if e.key == "default_provider")
        assert provider.source == "project"
        assert provider.value == "L3_project"
        assert provider.source_path == project_file

    def test_global_wins_when_project_unset(
        self, clean_settings
    ) -> None:
        """No CLI, no env, no project YAML → global YAML wins."""
        global_file = _write_settings(
            clean_settings.home, {"default_provider": "L4_global"}
        )

        entries = inspect_settings_cascade(project_root=clean_settings.project)
        provider = next(e for e in entries if e.key == "default_provider")
        assert provider.source == "global"
        assert provider.value == "L4_global"
        assert provider.source_path == global_file

    def test_default_wins_when_all_higher_unset(
        self, clean_settings
    ) -> None:
        """Empty cascade → built-in default ('mock')."""
        entries = inspect_settings_cascade(project_root=clean_settings.project)
        provider = next(e for e in entries if e.key == "default_provider")
        assert provider.source == "default"
        assert provider.value == "mock"
        assert provider.source_path is None


# ===================================================================
# Env var type coercion  (spec 061 step 9)
# ===================================================================


class TestEnvVarTypeCoercion:
    """Env var strings are coerced to the model's declared types.

    Env vars arrive as strings (POSIX), but `DeliberatorSettings` declares
    typed fields. Coercion happens in `load_settings`'s env_overrides
    block. These tests pin the contract for each typed field and the
    documented failure modes.
    """

    def test_max_launches_coerced_to_int(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """DELIBERATOR_MAX_LAUNCHES='42' → max_launches == 42 (int)."""
        monkeypatch.setenv("DELIBERATOR_MAX_LAUNCHES", "42")
        settings = load_settings(project_root=clean_settings.project)
        assert settings.max_launches == 42
        assert isinstance(settings.max_launches, int)

    def test_max_launches_invalid_int_falls_through_to_default(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Non-numeric env value → coercion logs and falls through."""
        monkeypatch.setenv("DELIBERATOR_MAX_LAUNCHES", "not-a-number")
        settings = load_settings(project_root=clean_settings.project)
        # Default is 20; invalid env must NOT raise nor leave an unset field
        assert settings.max_launches == 20

    def test_max_launches_invalid_int_falls_through_to_global(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Invalid env coercion preserves a lower-tier YAML value (no clobber)."""
        _write_settings(clean_settings.home, {"max_launches": 99})
        monkeypatch.setenv("DELIBERATOR_MAX_LAUNCHES", "garbage")
        settings = load_settings(project_root=clean_settings.project)
        # Global YAML's 99 must survive — invalid env doesn't override
        # with a default, it leaves the lower tier intact.
        assert settings.max_launches == 99

    def test_string_fields_passed_through_unchanged(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """String-typed env vars round-trip without coercion."""
        monkeypatch.setenv("DELIBERATOR_DEFAULT_PROVIDER", "claude-code")
        monkeypatch.setenv("DELIBERATOR_DEFAULT_MODE", "winner-take-all")
        monkeypatch.setenv("DELIBERATOR_DEFAULT_MODEL", "claude-opus-4-5")

        settings = load_settings(project_root=clean_settings.project)

        assert settings.default_provider == "claude-code"
        assert settings.default_mode == "winner-take-all"
        assert settings.default_model == "claude-opus-4-5"

    def test_empty_string_env_var_treated_as_unset(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Empty DELIBERATOR_DEFAULT_PROVIDER='' must not override lower tiers.

        Empty strings are how shells signal "I cleared this var" without
        unsetting it. Treating them as values would mean a `unset
        DELIBERATOR_DEFAULT_PROVIDER; export DELIBERATOR_DEFAULT_PROVIDER=`
        sequence quietly clobbers the user's settings.yml. The cascade
        must skip empty env values and fall through.
        """
        _write_settings(clean_settings.home, {"default_provider": "anthropic"})
        monkeypatch.setenv("DELIBERATOR_DEFAULT_PROVIDER", "")

        settings = load_settings(project_root=clean_settings.project)
        # Global YAML's value must survive; empty string is not a value.
        assert settings.default_provider == "anthropic"


# ===================================================================
# Conftest fixture invariants  (spec 061 step 9)
# ===================================================================


class TestCleanSettingsFixtureInvariants:
    """The clean_settings fixture upholds its documented contract."""

    def test_clean_settings_clears_all_cascade_env_vars(
        self, clean_settings
    ) -> None:
        """Every env var the cascade reads is unset under the fixture."""
        import os
        # _CASCADE_ENV_VARS is the conftest authority for what the cascade reads
        from engine.tests.conftest import _CASCADE_ENV_VARS

        for var in _CASCADE_ENV_VARS:
            assert var not in os.environ, (
                f"clean_settings should have cleared {var}"
            )

    def test_cascade_env_var_list_matches_settings_module(self) -> None:
        """conftest._CASCADE_ENV_VARS must stay in lockstep with settings module.

        If a new env-overridable field is added to engine/settings.py, the
        conftest fixture must clear it too — otherwise cascade tests will
        leak the developer's real env into the test scope.
        """
        from engine.settings import _ENV_VAR_FOR_FIELD
        from engine.tests.conftest import _CASCADE_ENV_VARS

        assert set(_CASCADE_ENV_VARS) == set(_ENV_VAR_FOR_FIELD.values()), (
            "conftest._CASCADE_ENV_VARS drifted from settings._ENV_VAR_FOR_FIELD; "
            "update conftest.py to include all cascade env vars."
        )

    def test_clean_settings_provides_isolated_home_and_project(
        self, clean_settings
    ) -> None:
        """home and project are real, distinct, writable directories."""
        assert clean_settings.home.is_dir()
        assert clean_settings.project.is_dir()
        assert clean_settings.home != clean_settings.project
        # Both must be inside tmp_path so cleanup is automatic.
        assert clean_settings.home.parent == clean_settings.project.parent

    def test_clean_settings_patches_path_home(
        self, clean_settings
    ) -> None:
        """Path.home() returns the fixture's home, not the developer's."""
        assert Path.home() == clean_settings.home


# ===================================================================
# resolve_provider_with_context — Phase 3 context-aware default
# ===================================================================
#
# The helper resolves default_provider with an additional tier in
# the cascade: when no explicit user preference exists at any tier
# (CLI / env / project YAML / global YAML), use the InvocationContext's
# session-inferred default. Explicit settings ALWAYS win.


class TestResolveProviderWithContext:
    """resolve_provider_with_context applies session inference correctly."""

    def test_explicit_flag_wins_over_context(
        self, clean_settings
    ) -> None:
        """CLI flag wins regardless of context."""
        from engine.settings import resolve_provider_with_context
        settings = load_settings(project_root=clean_settings.project)
        result = resolve_provider_with_context(
            settings,
            "anthropic",  # explicit flag
            "claude-code",  # context default
            project_root=clean_settings.project,
        )
        assert result == "anthropic"

    def test_global_yaml_wins_over_context(
        self, clean_settings
    ) -> None:
        """User's settings.yml respected even when context has a default."""
        _write_settings(clean_settings.home, {"default_provider": "anthropic"})
        from engine.settings import resolve_provider_with_context
        settings = load_settings(project_root=clean_settings.project)
        result = resolve_provider_with_context(
            settings,
            None,  # no flag
            "claude-code",  # context default
            project_root=clean_settings.project,
        )
        assert result == "anthropic"

    def test_project_yaml_wins_over_context(
        self, clean_settings
    ) -> None:
        """Project-level settings.yml wins over context inference."""
        _write_settings(clean_settings.project, {"default_provider": "openai"})
        from engine.settings import resolve_provider_with_context
        settings = load_settings(project_root=clean_settings.project)
        result = resolve_provider_with_context(
            settings,
            None,
            "claude-code",
            project_root=clean_settings.project,
        )
        assert result == "openai"

    def test_env_var_wins_over_context(
        self, clean_settings, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """DELIBERATOR_DEFAULT_PROVIDER wins over context inference."""
        monkeypatch.setenv("DELIBERATOR_DEFAULT_PROVIDER", "openai")
        from engine.settings import resolve_provider_with_context
        settings = load_settings(project_root=clean_settings.project)
        result = resolve_provider_with_context(
            settings,
            None,
            "claude-code",
            project_root=clean_settings.project,
        )
        assert result == "openai"

    def test_no_user_preference_uses_context_default(
        self, clean_settings
    ) -> None:
        """No flag, no env, no YAML → context-inferred default wins."""
        from engine.settings import resolve_provider_with_context
        settings = load_settings(project_root=clean_settings.project)
        result = resolve_provider_with_context(
            settings,
            None,
            "claude-code",  # context says use this
            project_root=clean_settings.project,
        )
        assert result == "claude-code"

    def test_no_user_preference_with_mock_context_returns_mock(
        self, clean_settings
    ) -> None:
        """No user preference + plain TTY context → mock fallback."""
        from engine.settings import resolve_provider_with_context
        settings = load_settings(project_root=clean_settings.project)
        result = resolve_provider_with_context(
            settings,
            None,
            "mock",  # plain TTY context
            project_root=clean_settings.project,
        )
        assert result == "mock"

    def test_explicit_mock_in_yaml_respected_over_context(
        self, clean_settings
    ) -> None:
        """A user who deliberately sets default_provider: mock in YAML
        gets mock, even when context would prefer claude-code.

        Pins the no-override-explicit-preference contract: setting
        'mock' deliberately is a real choice (e.g., for cost-safety
        in a project) and the context-aware fallback must respect it.
        """
        _write_settings(clean_settings.home, {"default_provider": "mock"})
        from engine.settings import resolve_provider_with_context
        settings = load_settings(project_root=clean_settings.project)
        result = resolve_provider_with_context(
            settings,
            None,
            "claude-code",
            project_root=clean_settings.project,
        )
        # YAML-set mock wins over context-inferred claude-code
        assert result == "mock"
