"""Config parsing for the ``plugins:`` section of conversus.yml.

Validates plugin declarations: ``name`` and ``package`` are required,
``config`` is an optional dict.  Returns typed ``PluginConfigEntry``
objects for use by ``load_plugins()``.

This module is independent of the engine config parser — it can be
called standalone or integrated by the orchestrator.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class PluginConfigError(Exception):
    """Raised when a plugin config entry fails validation."""

    pass


# ---------------------------------------------------------------------------
# Config model
# ---------------------------------------------------------------------------


class PluginConfigEntry(BaseModel):
    """A validated plugin declaration from conversus.yml.

    Example YAML::

        plugins:
          - name: my-plugin
            package: conversus-nashopt
            config:
              threshold: 0.8
    """

    model_config = {"frozen": True}

    name: str
    package: str
    config: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def parse_plugins_config(
    raw: Any,
) -> list[PluginConfigEntry]:
    """Parse and validate the ``plugins:`` section from a conversus config.

    Rules:
      - ``None`` or empty list → empty result (FR-002: no behavioral change).
      - Each entry must be a dict with ``name`` (str) and ``package`` (str).
      - ``config`` is optional; defaults to empty dict.
      - Duplicate plugin names are rejected.

    Args:
        raw: The raw value of the ``plugins`` key from YAML. May be
            ``None``, ``[]``, or a list of dicts.

    Returns:
        List of validated ``PluginConfigEntry`` objects.

    Raises:
        PluginConfigError: On any validation failure.
    """
    if raw is None:
        return []

    if not isinstance(raw, list):
        raise PluginConfigError(
            "plugins: must be a list of plugin declarations."
        )

    if len(raw) == 0:
        return []

    entries: list[PluginConfigEntry] = []
    seen_names: set[str] = set()

    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise PluginConfigError(
                f"plugins[{i}]: each plugin must be a YAML mapping."
            )

        name = item.get("name")
        if not name or not isinstance(name, str):
            raise PluginConfigError(
                f"plugins[{i}]: 'name' is required and must be a string."
            )

        package = item.get("package")
        if not package or not isinstance(package, str):
            raise PluginConfigError(
                f"plugins[{i}] ('{name}'): 'package' is required and must "
                "be a string."
            )

        config = item.get("config", {})
        if config is None:
            config = {}
        if not isinstance(config, dict):
            raise PluginConfigError(
                f"plugins[{i}] ('{name}'): 'config' must be a mapping."
            )

        if name in seen_names:
            raise PluginConfigError(
                f"plugins[{i}]: duplicate plugin name '{name}'."
            )
        seen_names.add(name)

        entries.append(
            PluginConfigEntry(name=name, package=package, config=config)
        )

    return entries
