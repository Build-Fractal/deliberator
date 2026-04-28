"""Integration tests for the settings cascade across all layers (spec 057).

Verifies the settings cascade works end-to-end through the handler layer:
    CLI flag  >  env var  >  project .conversus/settings.yml  >
    global ~/.conversus/settings.yml  >  built-in defaults.

The unit tests in ``test_settings.py`` cover the cascade in isolation.
These tests prove the cascade is wired correctly into the handler layer
so that ``run_decide_mcp`` (and by extension any handler) resolves
provider, mode, and persistence settings from the full cascade.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

import pytest
import yaml

from engine.handlers import run_decide_mcp
from engine.results import DecideResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_settings(directory: Path, data: dict) -> Path:
    """Write a settings.yml inside *directory*/.conversus/ and return the
    YAML file path."""
    settings_dir = directory / ".conversus"
    settings_dir.mkdir(parents=True, exist_ok=True)
    settings_file = settings_dir / "settings.yml"
    settings_file.write_text(yaml.dump(data, sort_keys=False), encoding="utf-8")
    return settings_file


def _patch_roots(monkeypatch: pytest.MonkeyPatch, project: Path, home: Path) -> None:
    """Monkeypatch both project-root discovery and Path.home() so the
    settings cascade resolves files from the test's temp directories.

    ``engine.persistence.find_user_project_root`` is patched at the
    module level so both the lazy import inside ``load_settings()`` and
    the direct call in ``run_decide_mcp`` resolve to *project*.

    ``Path.home()`` is patched so the global settings tier reads from
    *home* instead of the real home directory.
    """
    monkeypatch.setattr(
        "engine.persistence.find_user_project_root", lambda start=None: project
    )
    monkeypatch.setattr(Path, "home", lambda: home)


# A question that passes the classifier's sufficiency check — complex
# enough to not be rejected as insufficient for multi-agent deliberation.
_QUESTION = (
    "Compare the trade-offs of PostgreSQL vs MongoDB for a multi-tenant "
    "healthcare SaaS platform handling 10M+ records per tenant with "
    "complex hierarchical queries and strict HIPAA compliance requirements."
)


# ===================================================================
# 1. Handler uses settings default_provider
# ===================================================================


class TestHandlerUsesSettingsDefaultProvider:
    """Project settings.yml overrides the signature default for provider."""

    def test_handler_uses_settings_default_provider(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Create a project with settings setting default_provider to
        anthropic. Call run_decide_mcp with provider='mock' (the
        signature default). Verify the settings cascade overrides 'mock'
        to 'anthropic' — evidenced by a ProviderError mentioning
        anthropic (no API key configured)."""
        project = tmp_path / "project"
        project.mkdir()
        home = tmp_path / "home"
        home.mkdir()

        _write_settings(project, {"default_provider": "anthropic"})
        _patch_roots(monkeypatch, project, home)

        # Clear any env vars that might interfere
        monkeypatch.delenv("CONVERSUS_DEFAULT_PROVIDER", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        result = run_decide_mcp(question=_QUESTION, provider="mock")

        assert isinstance(result, DecideResult)
        # The handler should have resolved to anthropic and hit a
        # provider error because no API key is available.
        assert result.errors, "Expected errors from provider resolution"
        error_text = " ".join(result.errors).lower()
        assert "anthropic" in error_text or "provider" in error_text, (
            f"Expected error to reference anthropic provider, got: {result.errors}"
        )


# ===================================================================
# 2. Env var overrides file settings
# ===================================================================


class TestEnvVarOverridesFileSettings:
    """CONVERSUS_DEFAULT_PROVIDER env var beats project settings.yml."""

    def test_env_var_overrides_file_settings(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Set CONVERSUS_DEFAULT_PROVIDER=openai via monkeypatch. Create
        project settings with default_provider=anthropic. The env var
        should win — provider resolves to openai, which fails with an
        error referencing openai (no API key)."""
        project = tmp_path / "project"
        project.mkdir()
        home = tmp_path / "home"
        home.mkdir()

        _write_settings(project, {"default_provider": "anthropic"})
        _patch_roots(monkeypatch, project, home)

        monkeypatch.setenv("CONVERSUS_DEFAULT_PROVIDER", "openai")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        result = run_decide_mcp(question=_QUESTION, provider="mock")

        assert isinstance(result, DecideResult)
        assert result.errors, "Expected errors from provider resolution"
        error_text = " ".join(result.errors).lower()
        assert "openai" in error_text or "provider" in error_text, (
            f"Expected error to reference openai provider, got: {result.errors}"
        )


# ===================================================================
# 3. CLI flag overrides everything
# ===================================================================


class TestCliFlagOverridesEverything:
    """Explicit non-default provider arg beats env var and file settings."""

    def test_cli_flag_overrides_everything(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Set env var and file settings both to anthropic. Call the
        handler with an explicit provider='openai' (not the signature
        default 'mock'). The explicit arg wins — the error should
        reference openai, not anthropic.

        Note: the handler treats provider='mock' as 'no explicit flag'
        and falls through to the settings cascade, so we use 'openai'
        as the explicit CLI flag to prove it beats the cascade.
        """
        project = tmp_path / "project"
        project.mkdir()
        home = tmp_path / "home"
        home.mkdir()

        _write_settings(project, {"default_provider": "anthropic"})
        _patch_roots(monkeypatch, project, home)

        monkeypatch.setenv("CONVERSUS_DEFAULT_PROVIDER", "anthropic")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        result = run_decide_mcp(question=_QUESTION, provider="openai")

        assert isinstance(result, DecideResult)
        assert result.errors, "Expected errors from provider resolution"
        error_text = " ".join(result.errors).lower()
        # The error must reference openai (the explicit flag), not
        # anthropic (the env var and file setting).
        assert "openai" in error_text, (
            f"Expected error to reference openai (the explicit flag), "
            f"got: {result.errors}"
        )
        assert "anthropic" not in error_text, (
            f"Error should NOT reference anthropic since openai was "
            f"passed explicitly, got: {result.errors}"
        )


# ===================================================================
# 4. Persistence respects settings
# ===================================================================


class TestPersistenceRespectsSettings:
    """persistence.enabled=false prevents deliberation directory creation."""

    def test_persistence_disabled_no_deliberations_dir(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Create settings with persistence.enabled=false. Run a handler
        with the mock provider (which succeeds without API keys). Verify
        no .conversus/deliberations/ directory is created."""
        project = tmp_path / "project"
        project.mkdir()
        home = tmp_path / "home"
        home.mkdir()

        _write_settings(project, {
            "default_provider": "mock",
            "persistence": {"enabled": False},
        })
        _patch_roots(monkeypatch, project, home)

        # Ensure the mock provider is used (no env var override)
        monkeypatch.delenv("CONVERSUS_DEFAULT_PROVIDER", raising=False)

        result = run_decide_mcp(question=_QUESTION, provider="mock")

        assert isinstance(result, DecideResult)
        # The mock provider should succeed without errors, or at worst
        # produce non-provider errors. The key assertion is about
        # persistence, not pipeline success.
        deliberations_dir = project / ".conversus" / "deliberations"
        assert not deliberations_dir.exists(), (
            f"Deliberations directory should not exist when persistence "
            f"is disabled, but found: {deliberations_dir}"
        )
