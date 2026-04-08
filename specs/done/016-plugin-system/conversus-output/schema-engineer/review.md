# Schema Engineer Review: 016 Plugin System Infrastructure

**Reviewer**: schema-engineer
**Spec**: 016-plugin-system
**Date**: 2026-03-24

---

## Executive Summary

The Pydantic models and type definitions in `conversus/plugins/base.py` and `conversus/plugins/config.py` demonstrate careful schema design: all state models are frozen (immutable), the HookPoint enum uses `str, Enum` for dual string/enum usage, PluginResult is frozen with an `advisory` flag defaulting to True, and the config parser produces frozen PluginConfigEntry objects with duplicate-name rejection. The models follow the patterns established in `conversus/schemas/game_forms.py` (frozen models, model_validators, clear docstrings). However, I identify several type-safety and schema-design concerns: `DeliberationState.config` is `dict[str, Any]` (untyped), `AgentState.positions` is `list[dict[str, Any]]` (deeply untyped), `PluginResult.data` is `dict[str, Any]` (no schema for structured output), and the `Plugin.name` and `Plugin.hooks` class attributes lack type enforcement at instantiation time. These gaps do not break the current implementation but will create validation blind spots when plugin authors build against these interfaces.

---

## Alignment

### A-1: Frozen configuration is applied consistently

All five Pydantic models (`AgentState`, `RoundState`, `DeliberationState`, `PluginResult`, `PluginConfigEntry`) declare `model_config = {"frozen": True}`. This matches the pattern in `game_forms.py` (where game form models are immutable) and exceeds it (game_forms.py models do not use frozen config, but plugins models do). Frozen state is critical for the isolation guarantee: plugins cannot accidentally mutate the state they receive.

### A-2: HookPoint uses str + Enum for dual-purpose usage

`class HookPoint(str, Enum)` means hook values work as both enum members (for type checking) and strings (for filename construction). This is the correct pattern: `execute_hooks()` uses `hook.value` for filenames (line 291), and plugin registration uses `hook in p.hooks` for membership testing. No casting or `.value` calls needed in the common path.

### A-3: PluginResult advisory defaults to True

`advisory: bool = True` satisfies the spec's design principle 5 ("Plugin output is advisory"). A plugin author who forgets to set advisory gets the safe default. The `advisory=False` path is documented as "reserved for future autonomous mode," correctly deferring the semantics of actionable results.

### A-4: Config parsing enforces required fields and rejects duplicates

`parse_plugins_config()` validates `name` (required string), `package` (required string), and `config` (optional dict, defaults to empty). Duplicate names are rejected. None and empty list produce empty results (FR-002). The parser produces frozen `PluginConfigEntry` objects, preventing downstream mutation of config state.

### A-5: The plugin package imports nothing from engine/

The `__init__.py` re-exports from `base.py` and `config.py` only. Neither module imports anything from `engine/`. This satisfies FR-014 ("Plugin implementations depend on `conversus-plugins`; the core conversus engine does not") and maintains the package independence documented in the module docstrings.

---

## Missed Opportunities

### M-1: `DeliberationState.config` is `dict[str, Any]` -- no schema validation

The full conversus.yml config is passed to plugins as `config: dict[str, Any]`. Plugin authors who need specific config values (e.g., `config["mode"]`, `config["rounds"]`, `config["iterations"]`) must do untyped dict access with no compile-time or construction-time validation. The engine has an `EngineConfig` Pydantic model, but the plugins package cannot import it (no engine dependency). A `PluginFacingConfig` model with the subset of config fields plugins need (mode, rounds, iterations, agent_names) would provide type-safe access without importing the engine.

### M-2: `AgentState.positions` is `list[dict[str, Any]]` -- deeply untyped

The `positions` field is a list of untyped dicts. The spec says agents have "positions, concessions, recommendations" but does not define the dict structure. Plugin authors must guess or inspect runtime data. A `Position` model (even a minimal one with `recommendation: str`, `disposition: str`, `priority: str | None`) would provide a typed contract.

### M-3: `PluginResult.data` is `dict[str, Any]` -- no schema for structured output

Plugin output data is `dict[str, Any]`. This means each plugin defines its own ad-hoc output schema, and consumers of plugin output (including plugin-to-plugin communication) must parse untyped JSON. A `TypedDict` or Pydantic model per plugin would be more robust, but the framework cannot enforce this since each plugin defines its own data structure. At minimum, a `PluginResultSchema` base class that plugins can extend would provide a pattern.

### M-4: Plugin.name and Plugin.hooks have no validation at instantiation

The `Plugin` ABC declares `name: str` and `hooks: list[HookPoint]` as class attributes, but `__init__` does not validate them. A Plugin subclass that forgets to set `name` will raise an `AttributeError` only when `execute_hooks()` accesses `plugin.name`. A constructor validation in `Plugin.__init__` would catch this earlier:

```python
def __init__(self, plugin_config=None):
    if not hasattr(self, 'name') or not self.name:
        raise TypeError(f"{type(self).__name__} must define a 'name' attribute.")
    if not hasattr(self, 'hooks') or not self.hooks:
        raise TypeError(f"{type(self).__name__} must define a 'hooks' attribute.")
    self.plugin_config = plugin_config or {}
```

### M-5: RoundState does not reference round output paths

`RoundState` captures `round_number`, `agents`, `synthesis_text`, `dispute_count`, and `convergence_count`. But it does not include the file paths for the round's artifacts (review files, revision files, synthesis file). A plugin analyzing historical rounds must construct file paths from conventions rather than reading them from the state. Adding `artifact_paths: dict[str, Path] = {}` to RoundState would provide this without breaking existing consumers.

### M-6: No version field on Plugin or PluginResult

There is no versioning mechanism for plugins. A plugin that changes its output schema between versions will produce incompatible `data` dicts without any signal to consumers. Adding `version: str` to the Plugin class and `plugin_version: str` to PluginResult output would enable consumers to handle schema evolution.

### M-7: `load_plugins()` accepts raw dicts instead of PluginConfigEntry

The `load_plugins()` function signature is `load_plugins(plugin_configs: list[dict[str, Any]])`. It receives raw dicts, not the validated `PluginConfigEntry` objects produced by `parse_plugins_config()`. This means the config parsing and plugin loading are not type-connected: a caller could pass unvalidated dicts to `load_plugins()`, bypassing the parsing validation. The signature should be `load_plugins(plugin_configs: list[PluginConfigEntry])` with the function accessing `.name`, `.package`, `.config` via typed attributes.

### M-8: execute_hooks() creates plugins/ dir even when all plugins fail

If all applicable plugins raise exceptions, `execute_hooks()` still creates the `plugins/` subdirectory (line 282). An empty `plugins/` directory signals that plugins were configured but produced no output, which is potentially useful for debugging. But it also means core output is not byte-identical with and without plugins if any plugins are declared -- the directory itself is a side effect. This is a minor FR-011 edge case: "Core deliberation output MUST be identical with or without plugins installed." The `plugins/` directory is not core output, but its presence changes the output directory structure.

---

## Off-Base Assumptions

### O-1: `positions: list[dict[str, Any]]` field is never populated by any code

The `AgentState.positions` field defaults to `[]` and there is no code in the codebase that constructs AgentState with non-empty positions. The field exists in the model but is dead. Either the engine should populate it when constructing DeliberationState, or the field should be removed.

---

## Actionable Recommendations

1. **Create PluginFacingConfig model for typed config access** (Priority: P2)
   - Define a model with `mode: str`, `rounds: int`, `iterations: int`, `agent_names: list[str]` -- the subset plugins actually need. Replace `DeliberationState.config: dict[str, Any]` with `DeliberationState.config: PluginFacingConfig`.

2. **Add validation for Plugin.name and Plugin.hooks in __init__** (Priority: P1)
   - Catch missing class attributes at instantiation time rather than at hook execution time.

3. **Change load_plugins() to accept list[PluginConfigEntry]** (Priority: P2)
   - Type-connect config parsing and plugin loading.

4. **Define a minimal Position model for AgentState.positions** (Priority: P3)
   - Or remove the field if it is truly dead (O-1).

5. **Add version field to Plugin class** (Priority: P3)
   - Enable consumers to handle plugin schema evolution.

6. **Remove or populate AgentState.positions** (Priority: P2)
   - Dead fields create a false API surface.

7. **Only create plugins/ dir when at least one plugin succeeds** (Priority: P3)
   - Avoid empty directory side effects. Check if any results were produced before `mkdir`.

8. **Add `__all__` to base.py** (Priority: P3)
   - The module re-exports through `__init__.py` but does not declare its public API.
