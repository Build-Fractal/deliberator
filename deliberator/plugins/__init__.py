"""deliberator.plugins: Plugin system infrastructure for the deliberator engine.

Provides the base class, lifecycle hooks, state interface, output namespace,
config parsing, and dynamic loading for the deliberator plugin framework.

Plugins observe deliberation state and produce advisory output.  They never
modify core artifacts (Constitution Principle XV — Plugin Isolation).

This package is independent of the engine — no engine imports here.

NOTE: This package ships as ``deliberator.plugins`` (not ``deliberator-plugins``
as FR-012 originally stated in the spec).

Optional dependency convention:
Each plugin that wraps an optional solver uses a module-level HAS_* flag:
  HAS_NASHOPT (nashopt/solver.py) — True when nashopt + jax importable
  HAS_AMPL (optimizer/ampl_model.py) — True when amplpy + highspy importable
Plugins check this flag to dispatch between solver and heuristic paths.
Tests can mock the flag to exercise both paths.
"""

from deliberator.plugins.base import (
    AgentState,
    DeliberationState,
    HookPoint,
    Plugin,
    PluginDependencyCycleError,
    PluginResult,
    RoundState,
    _topological_sort_plugins,
    execute_hooks,
    load_plugins,
)
from deliberator.plugins.config import (
    PluginConfigEntry,
    parse_plugins_config,
)

__all__ = [
    # Core models
    "AgentState",
    "DeliberationState",
    "HookPoint",
    "Plugin",
    "PluginDependencyCycleError",
    "PluginResult",
    "RoundState",
    # Loading & execution
    "_topological_sort_plugins",
    "execute_hooks",
    "load_plugins",
    # Config
    "PluginConfigEntry",
    "parse_plugins_config",
]
