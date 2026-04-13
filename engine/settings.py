"""Settings loader for the conversus engine (spec 057).

Implements the settings cascade for ``ConversusSettings``:

    ┌─────────────────────────────────────────────┐
    │  CLI flag  (resolve_setting)                │  ← highest priority
    ├─────────────────────────────────────────────┤
    │  <project>/.conversus/settings.yml          │
    ├─────────────────────────────────────────────┤
    │  ~/.conversus/settings.yml                  │
    ├─────────────────────────────────────────────┤
    │  Built-in defaults  (Pydantic model)        │  ← lowest priority
    └─────────────────────────────────────────────┘

Resolution: most-specific wins.  Project-level overrides global-level;
global-level overrides built-in defaults.  ``resolve_setting`` lets a
CLI flag override everything.

Constitution compliance
-----------------------
- Principle IX: Pydantic models with frozen config, explicit typing on
  every function signature.
- Principle XI: single source of truth — all settings logic lives here;
  callers import rather than reimplementing.

See ``specs/057-settings-cascade.md``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger("conversus.settings")

_SETTINGS_REL = Path(".conversus") / "settings.yml"


# ---------------------------------------------------------------------------
# Pydantic settings models
# ---------------------------------------------------------------------------


class PersistenceSettings(BaseModel):
    """Controls deliberation persistence behaviour."""

    model_config = ConfigDict(frozen=True)

    enabled: bool = True
    retention_days: int = 90


class ConversusSettings(BaseModel):
    """Top-level settings for the conversus engine.

    All fields carry sensible defaults so a zero-config experience is
    possible.  Values are overridden via the YAML settings cascade
    described in the module docstring.
    """

    model_config = ConfigDict(frozen=True)

    default_provider: str = "mock"
    default_model: str | None = None
    default_mode: str = "cooperative"
    max_launches: int = 20
    persistence: PersistenceSettings = PersistenceSettings()


# ---------------------------------------------------------------------------
# Deep merge helper
# ---------------------------------------------------------------------------


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge *override* into *base*, returning a new dict.

    Scalar values in *override* replace those in *base*.  When both
    sides have a ``dict`` for the same key, the merge recurses so that
    nested keys (e.g. ``persistence.enabled``) can be overridden
    without losing sibling keys (e.g. ``persistence.retention_days``).
    """
    merged: dict[str, Any] = {**base}
    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


# ---------------------------------------------------------------------------
# YAML reading helper
# ---------------------------------------------------------------------------


def _read_yaml(path: Path) -> dict[str, Any]:
    """Read a YAML file, returning an empty dict on any failure."""
    if not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            logger.warning("Settings file %s is not a YAML mapping — ignored", path)
            return {}
        return data
    except (yaml.YAMLError, OSError) as exc:
        logger.warning("Could not read settings at %s: %s", path, exc)
        return {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_settings(project_root: Path | None = None) -> ConversusSettings:
    """Load settings using the three-tier cascade.

    Resolution order (most-specific wins):

    1. ``<project_root>/.conversus/settings.yml`` — project-level
    2. ``~/.conversus/settings.yml`` — global (user-level)
    3. Built-in defaults (Pydantic model defaults)

    When *project_root* is ``None``, :func:`engine.persistence.find_project_root`
    is used to discover it.

    Args:
        project_root: Explicit project root.  ``None`` triggers automatic
            discovery via ``find_project_root()``.

    Returns:
        A frozen ``ConversusSettings`` instance.
    """
    # Resolve project root lazily so callers don't need to.
    if project_root is None:
        from engine.persistence import find_project_root

        project_root = find_project_root()

    # Tier 3 → 2: start with global settings
    global_path = Path.home() / _SETTINGS_REL
    merged: dict[str, Any] = _read_yaml(global_path)

    # Tier 2 → 1: project-level overrides global
    project_path = project_root / _SETTINGS_REL
    project_data = _read_yaml(project_path)
    if project_data:
        merged = _deep_merge(merged, project_data)

    return ConversusSettings(**merged)


def resolve_setting(
    settings: ConversusSettings,
    flag_value: str | None,
    setting_name: str,
) -> str:
    """Resolve a single setting with CLI-flag priority.

    If *flag_value* is a non-empty string it wins (CLI flags override
    the entire settings cascade).  Otherwise the value is read from
    *settings* by attribute name.

    This is the helper that handlers call, e.g.::

        provider = resolve_setting(settings, provider_arg, "default_provider")

    Args:
        settings: The loaded ``ConversusSettings`` instance.
        flag_value: The value passed via CLI flag, or ``None``.
        setting_name: Attribute name on ``ConversusSettings`` to fall
            back to.

    Returns:
        The resolved string value.
    """
    if flag_value is not None and flag_value != "":
        return flag_value
    value = getattr(settings, setting_name)
    # Coerce to str for callers that expect a string return.
    return str(value) if value is not None else ""
