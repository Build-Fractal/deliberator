# Plugin Framework

Plugin abstract base class, hook-point lifecycle, deliberation state management, and orchestration utilities for extending the engine (spec 016, 024).

This module defines the core plugin infrastructure. `Plugin` is the abstract base class all plugins extend, declaring `name`, `hooks`, and optional `produces`/`consumes` for cross-plugin data flow. `HookPoint` enumerates the four lifecycle points where plugins can execute. `DeliberationState` is the frozen read-only snapshot passed to every `execute()` call. `load_plugins()` handles dynamic discovery via `importlib`, and `execute_hooks()` orchestrates execution with topological sorting, error isolation, and result file output. `PluginDependencyCycleError` and `DuplicateProducerError` are raised when dependency declarations are invalid.

::: conversus.plugins.base
    options:
      members:
        - Plugin
        - HookPoint
        - DeliberationState
        - PluginResult
        - AgentState
        - RoundState
        - PluginDependencyCycleError
        - DuplicateProducerError
        - load_plugins
        - execute_hooks
