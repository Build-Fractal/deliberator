"""Settings loader for the conversus engine (spec 057).

Implements the settings cascade for ``ConversusSettings``:

    ┌─────────────────────────────────────────────┐
    │  CLI flag  (resolve_setting)                │  ← highest priority
    ├─────────────────────────────────────────────┤
    │  Environment variables                      │  ← Desktop Extension
    │  (CONVERSUS_DEFAULT_PROVIDER, etc.)          │    user_config
    ├─────────────────────────────────────────────┤
    │  <project>/.conversus/settings.yml          │
    ├─────────────────────────────────────────────┤
    │  ~/.conversus/settings.yml                  │
    ├─────────────────────────────────────────────┤
    │  Built-in defaults  (Pydantic model)        │  ← lowest priority
    └─────────────────────────────────────────────┘

Resolution: most-specific wins.  Environment variables sit between CLI
flags and project settings because they represent the Desktop Extension's
``user_config`` — settings the user configured in Claude Desktop's
extension UI.  ``resolve_setting`` checks env vars before falling through
to the settings cascade.

Constitution compliance
-----------------------
- Principle IX: Pydantic models with frozen config, explicit typing on
  every function signature.
- Principle XI: single source of truth — all settings logic lives here;
  callers import rather than reimplementing.

See ``specs/057-settings-architecture.md``.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Literal, NamedTuple

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

    When *project_root* is ``None``, :func:`engine.persistence.find_user_project_root`
    is used to discover it.

    Args:
        project_root: Explicit project root.  ``None`` triggers automatic
            discovery via ``find_user_project_root()``.

    Returns:
        A frozen ``ConversusSettings`` instance.
    """
    # Resolve project root lazily so callers don't need to.
    if project_root is None:
        from engine.persistence import find_user_project_root

        project_root = find_user_project_root()

    # Tier 3 → 2: start with global settings
    global_path = Path.home() / _SETTINGS_REL
    merged: dict[str, Any] = _read_yaml(global_path)

    # Tier 2 → 1: project-level overrides global
    project_path = project_root / _SETTINGS_REL
    project_data = _read_yaml(project_path)
    if project_data:
        merged = _deep_merge(merged, project_data)

    # Tier 1 → 0: environment variables override file settings.
    # These are set by Claude Desktop's user_config mechanism when the
    # .mcpb extension is installed — the user fills in settings in the
    # Desktop UI and they arrive here as env vars. This is the bridge
    # between the Desktop Extension (no filesystem settings) and the
    # settings cascade that CLI/Claude Code users get via YAML files.
    #
    # NOTE: API keys (ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY)
    # and provider URLs (OLLAMA_BASE_URL) are NOT part of ConversusSettings.
    # They are consumed directly by the provider resolution layer in
    # engine/auth.py via os.environ.get(). Do not add them here.
    env_overrides: dict[str, Any] = {}
    if os.environ.get("CONVERSUS_DEFAULT_PROVIDER"):
        env_overrides["default_provider"] = os.environ["CONVERSUS_DEFAULT_PROVIDER"]
    if os.environ.get("CONVERSUS_DEFAULT_MODE"):
        env_overrides["default_mode"] = os.environ["CONVERSUS_DEFAULT_MODE"]
    if os.environ.get("CONVERSUS_DEFAULT_MODEL"):
        env_overrides["default_model"] = os.environ["CONVERSUS_DEFAULT_MODEL"]
    if os.environ.get("CONVERSUS_MAX_LAUNCHES"):
        try:
            env_overrides["max_launches"] = int(os.environ["CONVERSUS_MAX_LAUNCHES"])
        except ValueError:
            logger.warning("Invalid CONVERSUS_MAX_LAUNCHES: %s", os.environ["CONVERSUS_MAX_LAUNCHES"])

    if env_overrides:
        merged = _deep_merge(merged, env_overrides)

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


# ---------------------------------------------------------------------------
# Cascade introspection (spec 057 SC-003)
# ---------------------------------------------------------------------------


# Map ConversusSettings field names to the env vars that override them.
# Kept in lockstep with the env_overrides logic in load_settings(). When you
# add a new env-overridable field there, add it here too.
_ENV_VAR_FOR_FIELD: dict[str, str] = {
    "default_provider": "CONVERSUS_DEFAULT_PROVIDER",
    "default_mode": "CONVERSUS_DEFAULT_MODE",
    "default_model": "CONVERSUS_DEFAULT_MODEL",
    "max_launches": "CONVERSUS_MAX_LAUNCHES",
}


class CascadeEntry(NamedTuple):
    """A single resolved setting with the layer it came from.

    Used by ``conversus status`` to show which tier of the cascade
    supplied each effective value.
    """

    key: str
    value: Any
    source: Literal["default", "global", "project", "env"]
    source_path: Path | None


def _coerce_env_value(field_name: str, raw: str) -> Any:
    """Coerce a raw environment-variable string into the field's type.

    Mirrors the int-parsing branch in ``load_settings`` for
    ``CONVERSUS_MAX_LAUNCHES``.  Returns ``None`` if coercion fails so
    the caller can fall through to the next tier.
    """
    if field_name == "max_launches":
        try:
            return int(raw)
        except ValueError:
            return None
    return raw


def inspect_settings_cascade(
    project_root: Path | None = None,
) -> list[CascadeEntry]:
    """Return per-key resolution of every ``ConversusSettings`` field.

    Walks the cascade tiers (env → project → global → default) and
    determines, for each field declared on ``ConversusSettings``, which
    tier supplied the effective value.  Used by ``conversus status`` to
    show users where each setting came from.

    Args:
        project_root: Explicit project root.  ``None`` triggers
            automatic discovery via ``find_user_project_root()``.

    Returns:
        A list of ``CascadeEntry`` tuples — one per field on
        ``ConversusSettings`` — preserving model field order.
    """
    if project_root is None:
        from engine.persistence import find_user_project_root

        project_root = find_user_project_root()

    global_path = Path.home() / _SETTINGS_REL
    project_path = project_root / _SETTINGS_REL

    global_data = _read_yaml(global_path)
    project_data = _read_yaml(project_path)

    defaults = ConversusSettings()

    entries: list[CascadeEntry] = []
    for field_name in ConversusSettings.model_fields:
        env_var = _ENV_VAR_FOR_FIELD.get(field_name)
        env_raw = os.environ.get(env_var) if env_var else None

        if env_raw:
            coerced = _coerce_env_value(field_name, env_raw)
            if coerced is not None:
                entries.append(
                    CascadeEntry(
                        key=field_name,
                        value=coerced,
                        source="env",
                        source_path=None,
                    )
                )
                continue

        if field_name in project_data:
            entries.append(
                CascadeEntry(
                    key=field_name,
                    value=project_data[field_name],
                    source="project",
                    source_path=project_path,
                )
            )
            continue

        if field_name in global_data:
            entries.append(
                CascadeEntry(
                    key=field_name,
                    value=global_data[field_name],
                    source="global",
                    source_path=global_path,
                )
            )
            continue

        entries.append(
            CascadeEntry(
                key=field_name,
                value=getattr(defaults, field_name),
                source="default",
                source_path=None,
            )
        )

    return entries
