"""Settings loader for the deliberator engine (spec 057).

Implements the settings cascade for ``DeliberatorSettings``:

    ┌─────────────────────────────────────────────┐
    │  CLI flag  (resolve_setting)                │  ← highest priority
    ├─────────────────────────────────────────────┤
    │  Environment variables                      │  ← Desktop Extension
    │  (DELIBERATOR_DEFAULT_PROVIDER, etc.)          │    user_config
    ├─────────────────────────────────────────────┤
    │  <project>/.deliberator/settings.yml          │
    ├─────────────────────────────────────────────┤
    │  ~/.deliberator/settings.yml                  │
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

logger = logging.getLogger("deliberator.settings")

_SETTINGS_REL = Path(".deliberator") / "settings.yml"


# ---------------------------------------------------------------------------
# Pydantic settings models
# ---------------------------------------------------------------------------


class PersistenceSettings(BaseModel):
    """Controls deliberation persistence behaviour."""

    model_config = ConfigDict(frozen=True)

    enabled: bool = True
    retention_days: int = 90


class DeliberatorSettings(BaseModel):
    """Top-level settings for the deliberator engine.

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


def load_settings(project_root: Path | None = None) -> DeliberatorSettings:
    """Load settings using the three-tier cascade.

    Resolution order (most-specific wins):

    1. ``<project_root>/.deliberator/settings.yml`` — project-level
    2. ``~/.deliberator/settings.yml`` — global (user-level)
    3. Built-in defaults (Pydantic model defaults)

    When *project_root* is ``None``, :func:`engine.persistence.find_user_project_root`
    is used to discover it.

    Args:
        project_root: Explicit project root.  ``None`` triggers automatic
            discovery via ``find_user_project_root()``.

    Returns:
        A frozen ``DeliberatorSettings`` instance.
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
    # and provider URLs (OLLAMA_BASE_URL) are NOT part of DeliberatorSettings.
    # They are consumed directly by the provider resolution layer in
    # engine/auth.py via os.environ.get(). Do not add them here.
    env_overrides: dict[str, Any] = {}
    if os.environ.get("DELIBERATOR_DEFAULT_PROVIDER"):
        env_overrides["default_provider"] = os.environ["DELIBERATOR_DEFAULT_PROVIDER"]
    if os.environ.get("DELIBERATOR_DEFAULT_MODE"):
        env_overrides["default_mode"] = os.environ["DELIBERATOR_DEFAULT_MODE"]
    if os.environ.get("DELIBERATOR_DEFAULT_MODEL"):
        env_overrides["default_model"] = os.environ["DELIBERATOR_DEFAULT_MODEL"]
    if os.environ.get("DELIBERATOR_MAX_LAUNCHES"):
        try:
            env_overrides["max_launches"] = int(os.environ["DELIBERATOR_MAX_LAUNCHES"])
        except ValueError:
            logger.warning("Invalid DELIBERATOR_MAX_LAUNCHES: %s", os.environ["DELIBERATOR_MAX_LAUNCHES"])

    if env_overrides:
        merged = _deep_merge(merged, env_overrides)

    return DeliberatorSettings(**merged)


def resolve_setting(
    settings: DeliberatorSettings,
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
        settings: The loaded ``DeliberatorSettings`` instance.
        flag_value: The value passed via CLI flag, or ``None``.
        setting_name: Attribute name on ``DeliberatorSettings`` to fall
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


# Map DeliberatorSettings field names to the env vars that override them.
# Kept in lockstep with the env_overrides logic in load_settings(). When you
# add a new env-overridable field there, add it here too.
_ENV_VAR_FOR_FIELD: dict[str, str] = {
    "default_provider": "DELIBERATOR_DEFAULT_PROVIDER",
    "default_mode": "DELIBERATOR_DEFAULT_MODE",
    "default_model": "DELIBERATOR_DEFAULT_MODEL",
    "max_launches": "DELIBERATOR_MAX_LAUNCHES",
}


class CascadeEntry(NamedTuple):
    """A single resolved setting with the layer it came from.

    Used by ``deliberator status`` to show which tier of the cascade
    supplied each effective value.
    """

    key: str
    value: Any
    source: Literal["default", "global", "project", "env"]
    source_path: Path | None


def _coerce_env_value(field_name: str, raw: str) -> Any:
    """Coerce a raw environment-variable string into the field's type.

    Mirrors the int-parsing branch in ``load_settings`` for
    ``DELIBERATOR_MAX_LAUNCHES``.  Returns ``None`` if coercion fails so
    the caller can fall through to the next tier.
    """
    if field_name == "max_launches":
        try:
            return int(raw)
        except ValueError:
            return None
    return raw


def resolve_provider_with_context(
    settings: DeliberatorSettings,
    flag_value: str | None,
    context_default: str,
    project_root: Path | None = None,
) -> str:
    """Resolve ``default_provider`` with context-aware fallback.

    Tier order:
      1. Explicit CLI flag (if non-empty)
      2. Env var or YAML setting (cascade — env > project > global)
      3. Context-inferred default (when the cascade returned the
         built-in Pydantic default — i.e., the user expressed no
         preference at any tier)
      4. Built-in default ("mock")

    The context-inferred default lets the engine prefer a sensible
    provider for the current session (e.g., ``claude-code`` when
    invoked from a Claude Code session) without overriding any
    explicit user setting. A user with ``default_provider: anthropic``
    in ``~/.deliberator/settings.yml`` still gets anthropic; only the
    "no preference anywhere" path uses the context inference.

    Args:
        settings: The loaded ``DeliberatorSettings`` instance.
        flag_value: Value passed via ``--provider`` flag, or ``None``.
        context_default: The provider name suggested by
            ``InvocationContext.default_provider``. Typically
            ``"claude-code"`` in Claude Code sessions, ``"mock"``
            elsewhere.
        project_root: Project root for cascade introspection.

    Returns:
        The resolved provider name.
    """
    if flag_value:
        return flag_value

    entries = inspect_settings_cascade(project_root=project_root)
    provider_entry = next(
        (e for e in entries if e.key == "default_provider"), None
    )
    if provider_entry is not None and provider_entry.source != "default":
        # User set it explicitly via env/project/global — respect it.
        return str(provider_entry.value)

    # No user preference at any cascade tier; use context inference.
    return context_default


def inspect_settings_cascade(
    project_root: Path | None = None,
) -> list[CascadeEntry]:
    """Return per-key resolution of every ``DeliberatorSettings`` field.

    Walks the cascade tiers (env → project → global → default) and
    determines, for each field declared on ``DeliberatorSettings``, which
    tier supplied the effective value.  Used by ``deliberator status`` to
    show users where each setting came from.

    Args:
        project_root: Explicit project root.  ``None`` triggers
            automatic discovery via ``find_user_project_root()``.

    Returns:
        A list of ``CascadeEntry`` tuples — one per field on
        ``DeliberatorSettings`` — preserving model field order.
    """
    if project_root is None:
        from engine.persistence import find_user_project_root

        project_root = find_user_project_root()

    global_path = Path.home() / _SETTINGS_REL
    project_path = project_root / _SETTINGS_REL

    global_data = _read_yaml(global_path)
    project_data = _read_yaml(project_path)

    defaults = DeliberatorSettings()

    entries: list[CascadeEntry] = []
    for field_name in DeliberatorSettings.model_fields:
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
