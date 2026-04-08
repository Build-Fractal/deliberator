"""Core plugin infrastructure: models, base class, loading, and execution.

Implements FR-001 through FR-015 from spec 016-plugin-system.

Design rules:
  - All state models are frozen Pydantic (immutable).
  - Plugins observe, never modify, core artifacts (Principle XV).
  - Plugin output is advisory by default.
  - The plugin package imports nothing from ``engine/``.
  - Dependencies limited to pydantic + stdlib (FR-013).
"""

from __future__ import annotations

import importlib
import json
import logging
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger("conversus.plugins")


# ---------------------------------------------------------------------------
# HookPoint enum
# ---------------------------------------------------------------------------


class HookPoint(str, Enum):
    """Lifecycle hook points where plugins can execute.

    Plugins declare which hooks they subscribe to via their ``hooks``
    attribute.  The orchestrator calls ``execute_hooks`` at each point.
    """

    PRE_EXECUTION = "pre_execution"
    POST_PHASE_5 = "post_phase_5"
    POST_DELIBERATION = "post_deliberation"
    POST_ARBITRATION = "post_arbitration"


# ---------------------------------------------------------------------------
# State models (frozen, read-only)
# ---------------------------------------------------------------------------


class AgentState(BaseModel):
    """Per-agent snapshot passed to plugins.

    Captures an agent's participation metrics for a single round.
    """

    model_config = {"frozen": True}

    name: str
    recommendation_count: int = 0
    concession_count: int = 0
    surviving_count: int = 0
    positions: list[dict[str, Any]] = []


class RoundState(BaseModel):
    """Snapshot of a single completed round."""

    model_config = {"frozen": True}

    round_number: int
    agents: list[AgentState] = []
    synthesis_text: str = ""
    dispute_count: int = 0
    convergence_count: int = 0
    plugin_results: dict[str, Any] = {}


class DeliberationState(BaseModel):
    """Read-only state object passed to plugins at each hook point.

    Captures the full deliberation context a plugin needs to produce its
    advisory output.  Frozen — plugins cannot mutate this.

    ``plugin_results`` is populated by the orchestrator (``execute_hooks``)
    after each plugin executes.  Consumers read producer output from this
    dict.  Defaults to empty (FR-010 of spec 024).
    """

    model_config = {"frozen": True}

    mode: str
    round: int
    agents: list[AgentState] = []
    synthesis: str | None = None
    history: list[RoundState] = []
    output_dir: Path
    config: dict[str, Any] = {}
    plugin_results: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# PluginResult
# ---------------------------------------------------------------------------


class PluginResult(BaseModel):
    """Value returned by ``Plugin.execute()``.

    ``advisory=True`` (default) means the result is informational.
    A future autonomous mode may act on ``advisory=False`` results.
    """

    model_config = {"frozen": True}

    recommendation: str
    data: dict[str, Any] = {}
    advisory: bool = True


# ---------------------------------------------------------------------------
# Plugin base class (ABC)
# ---------------------------------------------------------------------------


class Plugin(ABC):
    """Abstract base class for all conversus plugins.

    Subclasses must set ``name`` and ``hooks`` as class attributes and
    implement ``execute()``.

    Optionally, subclasses may declare ``produces`` and ``consumes``
    (spec 024 — cross-plugin interfaces):

      - ``produces``: data keys this plugin outputs after execution.
      - ``consumes``: data keys this plugin wants from other plugins.

    The orchestrator (``execute_hooks``) uses these declarations to
    sort plugins so producers run before consumers and to populate
    ``DeliberationState.plugin_results``.

    Plugin-specific configuration is passed at init time via
    ``plugin_config``.  The ``execute()`` method receives only the
    deliberation state -- no redundant config parameter.

    Example::

        class MyPlugin(Plugin):
            name = "my-plugin"
            hooks = [HookPoint.POST_PHASE_5]
            produces = ["my_data"]

            def execute(self, state):
                return PluginResult(recommendation="...", data={})
    """

    name: str
    hooks: list[HookPoint]
    produces: list[str] = []
    consumes: list[str] = []

    def __init__(self, plugin_config: dict[str, Any] | None = None) -> None:
        self.plugin_config = plugin_config or {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Validate that subclasses define ``name`` and ``hooks`` correctly."""
        super().__init_subclass__(**kwargs)

        # Skip validation for abstract subclasses
        if getattr(cls, "__abstractmethods__", None):
            return

        if not hasattr(cls, "name") or not isinstance(cls.name, str) or not cls.name:
            raise TypeError(
                f"Plugin subclass '{cls.__name__}' must define a non-empty "
                f"'name' class attribute (str)."
            )

        if (
            not hasattr(cls, "hooks")
            or not isinstance(cls.hooks, list)
            or not cls.hooks
        ):
            raise TypeError(
                f"Plugin subclass '{cls.__name__}' must define a non-empty "
                f"'hooks' class attribute (list of HookPoint values)."
            )

        for hook in cls.hooks:
            if not isinstance(hook, HookPoint):
                raise TypeError(
                    f"Plugin subclass '{cls.__name__}': hooks must contain "
                    f"HookPoint values, got {type(hook).__name__}."
                )

    @abstractmethod
    def execute(self, state: DeliberationState) -> PluginResult:
        """Execute the plugin logic against the current deliberation state.

        Plugin-specific config is available via ``self.plugin_config``.

        Args:
            state: Frozen snapshot of the current deliberation.

        Returns:
            A ``PluginResult`` with recommendation and data.
        """
        ...


# ---------------------------------------------------------------------------
# Dynamic loading (FR-003, FR-004, FR-005)
# ---------------------------------------------------------------------------


def _find_plugin_class(module: Any) -> type[Plugin] | None:
    """Find the first Plugin subclass in a module (excluding Plugin itself)."""
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (
            isinstance(attr, type)
            and issubclass(attr, Plugin)
            and attr is not Plugin
        ):
            return attr
    return None


def load_plugins(
    plugin_configs: list[dict[str, Any]],
) -> list[Plugin]:
    """Load and instantiate plugins from config entries.

    For each config entry:
      1. Import the package via ``importlib.import_module``.
      2. Find the ``Plugin`` subclass in the module.
      3. Instantiate with the plugin-specific config.

    If a package cannot be imported (not installed), a warning is logged
    and that plugin is skipped (FR-005).  No crash.

    Args:
        plugin_configs: List of dicts, each with ``name``, ``package``,
            and optional ``config``.

    Returns:
        List of instantiated ``Plugin`` objects, in declaration order.
    """
    loaded: list[Plugin] = []

    for entry in plugin_configs:
        name = entry.get("name", "<unknown>")
        package = entry.get("package", "")
        config = entry.get("config", {}) or {}

        if not package:
            logger.warning(
                "Plugin '%s': no package specified, skipping.", name
            )
            continue

        try:
            module = importlib.import_module(package)
        except ImportError:
            logger.warning(
                "Plugin '%s': package '%s' is not installed, skipping.",
                name,
                package,
            )
            continue

        plugin_cls = _find_plugin_class(module)
        if plugin_cls is None:
            logger.warning(
                "Plugin '%s': no Plugin subclass found in package '%s', "
                "skipping.",
                name,
                package,
            )
            continue

        try:
            instance = plugin_cls(plugin_config=config)
            loaded.append(instance)
            logger.info("Plugin '%s' loaded from '%s'.", name, package)
        except Exception:
            logger.warning(
                "Plugin '%s': failed to instantiate from package '%s', "
                "skipping.",
                name,
                package,
                exc_info=True,
            )

    return loaded


# ---------------------------------------------------------------------------
# Topological sort for plugin dependency ordering (spec 024)
# ---------------------------------------------------------------------------


class PluginDependencyCycleError(Exception):
    """Raised when plugin produces/consumes declarations form a cycle."""


class DuplicateProducerError(Exception):
    """Raised when two plugins declare the same ``produces`` key."""


def _topological_sort_plugins(
    plugins: list[Plugin],
    hook: HookPoint,
) -> list[Plugin]:
    """Sort plugins so producers execute before consumers.

    Builds a dependency graph from ``produces``/``consumes`` declarations
    and returns a topologically sorted list.  Plugins without declarations
    maintain their original declaration order relative to each other
    (FR-007, FR-009 of spec 024).

    Args:
        plugins: Plugins registered for a given hook point.
        hook: The hook point (used only for error messages).

    Returns:
        Plugins sorted so that any producer of a data key runs before
        any consumer of that key.

    Raises:
        PluginDependencyCycleError: If a cycle exists in the dependency
            graph.
    """
    if not plugins:
        return []

    # Map data key -> plugin that produces it
    producers: dict[str, Plugin] = {}
    for p in plugins:
        for key in getattr(p, "produces", []):
            if key in producers:
                existing = producers[key].name
                raise DuplicateProducerError(
                    f"Key '{key}' produced by both "
                    f"'{existing}' and '{p.name}'"
                )
            producers[key] = p

    # Build adjacency list: plugin -> set of plugins it must run after
    # (i.e., edges from dependency to dependent)
    plugin_index: dict[str, int] = {
        id(p): i for i, p in enumerate(plugins)
    }
    # predecessors[plugin_id] = set of plugin_ids that must run first
    predecessors: dict[int, set[int]] = {id(p): set() for p in plugins}

    for consumer in plugins:
        for key in getattr(consumer, "consumes", []):
            producer = producers.get(key)
            if producer is not None and producer is not consumer:
                predecessors[id(consumer)].add(id(producer))

    # Kahn's algorithm for topological sort
    in_degree: dict[int, int] = {
        id(p): len(predecessors[id(p)]) for p in plugins
    }
    # Successors: who depends on this plugin?
    successors: dict[int, list[int]] = {id(p): [] for p in plugins}
    for pid, preds in predecessors.items():
        for pred_id in preds:
            successors[pred_id].append(pid)

    # Start with plugins that have no dependencies, in declaration order
    queue: list[Plugin] = [p for p in plugins if in_degree[id(p)] == 0]
    sorted_plugins: list[Plugin] = []

    while queue:
        # Among ready plugins, pick by declaration order (stable sort)
        queue.sort(key=lambda p: plugin_index[id(p)])
        current = queue.pop(0)
        sorted_plugins.append(current)

        for succ_id in successors[id(current)]:
            in_degree[succ_id] -= 1
            if in_degree[succ_id] == 0:
                # Find the plugin object by id
                succ_plugin = next(
                    p for p in plugins if id(p) == succ_id
                )
                queue.append(succ_plugin)

    if len(sorted_plugins) != len(plugins):
        # Cycle detected — find the involved plugins for a clear error
        remaining = [
            p.name for p in plugins
            if id(p) not in {id(s) for s in sorted_plugins}
        ]
        raise PluginDependencyCycleError(
            f"Cycle detected in plugin dependencies at hook "
            f"'{hook.value}': {', '.join(remaining)}. "
            f"Check produces/consumes declarations."
        )

    return sorted_plugins


# ---------------------------------------------------------------------------
# Hook execution (FR-006, FR-007, FR-008, FR-009)
# ---------------------------------------------------------------------------


def execute_hooks(
    hook: HookPoint,
    plugins: list[Plugin],
    state: DeliberationState,
    output_dir: Path,
) -> list[PluginResult]:
    """Execute all plugins registered for a given hook point.

    Plugins are sorted so producers run before consumers (spec 024,
    FR-005, FR-007).  Within unrelated plugins, declaration order is
    preserved (FR-009).  If a plugin's ``execute()`` raises, the error
    is logged and execution continues with the next plugin (FR-008).

    After each plugin executes, its ``produces`` values are extracted
    from ``PluginResult.data`` and stored in ``plugin_results`` on the
    state passed to subsequent plugins (spec 024, FR-008).

    **Scoping**: ``plugin_results`` is accumulated per invocation of this
    function (i.e., per hook point).  Results from one hook invocation
    are **not** carried over to the next.  Each call starts from the
    ``plugin_results`` already present on the incoming ``state``.

    Results are written to ``{output_dir}/plugins/{name}-{hook}-round-{N}.json``
    (FR-009 of spec 016).  The ``plugins/`` subdirectory is created if
    it does not exist.

    Integration point for engine/phases.py:
        The engine pipeline should call ``execute_hooks()`` at each lifecycle
        point defined in ``HookPoint``:
          - ``HookPoint.PRE_EXECUTION``: after config parsing, before first
            agent launch.
          - ``HookPoint.POST_PHASE_5``: after each round's Phase 5 synthesis
            is complete.
          - ``HookPoint.POST_DELIBERATION``: after the final round completes
            (or stagnation detected).
          - ``HookPoint.POST_ARBITRATION``: after arbitration resolves
            remaining disputes.
        The actual wiring into ``engine/phases.py`` is deferred to a follow-up
        PR when the engine is ready for plugin integration.

    Args:
        hook: The lifecycle hook point being executed.
        plugins: All loaded plugins (filtering happens here).
        state: The current deliberation state snapshot.
        output_dir: Root output directory for the deliberation run.

    Returns:
        List of ``PluginResult`` objects from successful executions.

    Raises:
        PluginDependencyCycleError: If produces/consumes form a cycle.
    """
    results: list[PluginResult] = []

    # Filter to plugins registered for this hook
    applicable = [p for p in plugins if hook in p.hooks]
    if not applicable:
        return results

    # Sort by dependency order: producers before consumers (spec 024)
    applicable = _topological_sort_plugins(applicable, hook)

    plugins_dir = output_dir / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)

    # Accumulate plugin_results across executions at this hook point
    plugin_results: dict[str, Any] = dict(state.plugin_results)

    for plugin in applicable:
        # Build state with current plugin_results for this plugin
        current_state = state.model_copy(
            update={"plugin_results": plugin_results},
        )

        try:
            result = plugin.execute(current_state)
            results.append(result)

            # Extract produced values from result data (spec 024, FR-008)
            for key in getattr(plugin, "produces", []):
                if key in result.data:
                    plugin_results[key] = result.data[key]
                else:
                    logger.warning(
                        "Plugin '%s' declares produces=['%s'] "
                        "but did not emit it",
                        plugin.name,
                        key,
                    )

            # Write output file (FR-009)
            filename = (
                f"{plugin.name}-{hook.value}-round-{state.round}.json"
            )
            output_path = plugins_dir / filename
            output_data = {
                "plugin": plugin.name,
                "hook": hook.value,
                "round": state.round,
                "recommendation": result.recommendation,
                "data": result.data,
                "advisory": result.advisory,
            }
            output_path.write_text(
                json.dumps(output_data, indent=2, default=str),
                encoding="utf-8",
            )
        except Exception:
            logger.warning(
                "Plugin '%s' raised an exception at hook '%s', skipping.",
                plugin.name,
                hook.value,
                exc_info=True,
            )

    return results
