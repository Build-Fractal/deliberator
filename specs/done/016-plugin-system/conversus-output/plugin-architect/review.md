# Plugin Architect Review: 016 Plugin System Infrastructure

**Reviewer**: plugin-architect
**Spec**: 016-plugin-system
**Date**: 2026-03-24

---

## Executive Summary

The plugin system in `conversus/plugins/` implements a clean, minimal infrastructure that satisfies the spec's five design principles (core works alone, plugins optional, plugins swappable, one-direction data flow, advisory output). The `Plugin` ABC, `HookPoint` enum, `DeliberationState` frozen model, and `execute_hooks()` function form a cohesive framework. The isolation guarantee (plugins never modify core artifacts) is enforced structurally: `DeliberationState` is frozen, plugin output is namespaced to `{output}/plugins/`, and the plugin package imports nothing from `engine/`. However, the hook system has meaningful limitations that will constrain specs 017-019: there is no mechanism for plugins to access the `FeatureSet` from spec 015 (the state model predates feature extraction), the `config` parameter on `execute()` receives plugin-specific config but not the full deliberation config, hooks fire at phase boundaries but not at iteration boundaries within the Phase 2-3 loop, and the plugin-to-plugin data passing story is absent. These are architectural decisions, not bugs, but they will create friction for plugin authors building convergence predictors (spec 018) and config optimizers (spec 019).

---

## Alignment

### A-1: Plugin ABC enforces the correct contract

The `Plugin` class is an ABC with `execute()` as the only abstract method. `name` and `hooks` are class attributes (not instance attributes), which is correct: they are static properties of the plugin class, not configurable per-instance. The `__init__` accepts `plugin_config` for instance-level configuration, maintaining the separation between plugin identity (class-level) and plugin parameterization (instance-level).

### A-2: HookPoint enum covers the specified lifecycle points

The four hook points (PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, POST_ARBITRATION) match the spec's Section 2 lifecycle hooks table exactly. Using `str, Enum` ensures hook values are string-serializable for filenames (FR-009).

### A-3: DeliberationState is frozen and read-only

`DeliberationState` uses `model_config = {"frozen": True}`, enforcing immutability. The model contains mode, round, agents, synthesis, history, output_dir, and config -- matching the spec's Section 2 DeliberationState definition. The `agents` field uses `list[AgentState]` where AgentState is also frozen. Test `TestDeliberationState.test_frozen` confirms mutation raises an exception.

### A-4: Plugin output is correctly namespaced

`execute_hooks()` writes output to `{output}/plugins/{plugin-name}-{hook}-round-{N}.json`, creating the `plugins/` subdirectory only when plugins are present (line 282: `plugins_dir.mkdir(parents=True, exist_ok=True)`). This ensures FR-010 compliance: plugin output is namespaced, not mixed with core output.

### A-5: Exception isolation is implemented

The `execute_hooks()` try/except block (lines 284-312) catches any exception from `plugin.execute()`, logs it, and continues to the next plugin. This satisfies FR-008: plugin failure does not block core deliberation. The exception is logged with `exc_info=True` for debugging.

### A-6: Sequential declaration-order execution is enforced

`execute_hooks()` filters plugins by hook registration (`hook in p.hooks`) and iterates in list order. Since `load_plugins()` preserves declaration order from the config, FR-007 is satisfied. Test `test_sequential_declaration_order` confirms this with order-tracking plugins.

### A-7: Config parsing is robust

`parse_plugins_config()` handles None, empty list, and populated list correctly. It validates required fields (name, package), rejects duplicates, and produces frozen `PluginConfigEntry` objects. The `PluginConfigError` exception type enables config-specific error handling upstream.

---

## Missed Opportunities

### M-1: No mechanism for plugins to access FeatureSet (spec 015)

The `DeliberationState` model does not include a `features` field. Plugins that need feature vectors (equilibrium scorer spec 017, convergence predictor spec 018) must independently call `extract_features()` from the output directory. This is duplicative: the orchestrator should extract features once and pass them through the state. The missing field is:

```python
class DeliberationState(BaseModel):
    # ... existing fields ...
    features: Optional[FeatureSet] = None  # from spec 015
```

Without this, every numerical plugin will import and call `extract_features()` independently, violating the one-extraction-per-hook principle that the pipeline should enforce.

### M-2: `execute()` receives plugin-specific config, not deliberation config

The `Plugin.execute()` signature is `execute(self, state: DeliberationState, config: dict)`. The `config` parameter receives `plugin.plugin_config` (line 286), not the full deliberation config. But `DeliberationState` already contains `config: dict[str, Any]` with the full conversus.yml config. A plugin thus receives two config dicts: `state.config` (full) and the `config` parameter (plugin-specific). This is redundant and confusing. The `config` parameter on `execute()` should be either removed (plugins read their config from `self.plugin_config`) or renamed to `plugin_config` for clarity.

### M-3: No hook for iteration boundaries within the Phase 2-3 loop

The spec defines four hooks: PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, POST_ARBITRATION. The engine's Phase 2-3 loop (`for iteration in range(1, config.iterations + 1)`) has no hook point. A convergence predictor (spec 018) that wants to assess convergence after each cross-review/revision iteration has no hook to fire at. It must wait until POST_PHASE_5 (after all iterations complete), losing per-iteration granularity.

Adding `POST_ITERATION` or `POST_PHASE_3` hooks would require modifying the engine's phase loop, which conflicts with FR-014 ("Plugin implementations depend on `conversus-plugins`; the core conversus engine does not"). However, the engine already imports nothing from the plugins package -- hooks are fired by the orchestrator, not the engine. An optional hook invocation in the phase loop would not create a dependency; it would be a call site, not an import.

### M-4: No plugin-to-plugin data passing

If plugin A (equilibrium scorer) runs at POST_PHASE_5 and plugin B (config optimizer) wants to use plugin A's output, there is no mechanism for B to read A's result. Plugin B would need to parse A's JSON output file from the `plugins/` directory. This is fragile: it couples plugin B to plugin A's output filename convention. A `PluginContext` object that accumulates results from prior plugins within the same hook execution would enable clean data passing:

```python
class PluginContext:
    prior_results: dict[str, PluginResult]  # plugin_name -> result
```

### M-5: AgentState model is disconnected from AgentFeatures (spec 015)

The `AgentState` model in `base.py` has fields (`recommendation_count`, `concession_count`, `surviving_count`, `positions`) that overlap with but do not match `AgentFeatures` from spec 015. This creates two parallel representations of agent state: one for plugins (AgentState) and one for feature extraction (AgentFeatures). Plugin authors must choose which to use, and neither is a superset of the other.

The fix is either: (a) make AgentState a lightweight wrapper that references AgentFeatures, or (b) drop AgentState and use AgentFeatures directly in DeliberationState. Option (b) is cleaner but creates a dependency from the plugins package on the schemas package.

### M-6: Plugin loading uses first-found Plugin subclass, not named resolution

`_find_plugin_class()` returns the first `Plugin` subclass found in the module via `dir()` iteration. If a module contains multiple Plugin subclasses (e.g., a library providing both a scorer and a predictor), only the first one (in `dir()` alphabetical order) is loaded. The loading mechanism should support either (a) a module-level `plugin` variable pointing to the class, or (b) a class name specified in the config entry.

### M-7: `execute_hooks()` does not pass the hook point to plugins

Plugins registered for multiple hooks (e.g., `hooks = [HookPoint.POST_PHASE_5, HookPoint.POST_DELIBERATION]`) receive the same `execute()` call signature regardless of which hook fired. A plugin cannot determine which hook triggered its execution without inspecting the `state` (e.g., checking if synthesis is None for PRE_EXECUTION). Adding a `hook: HookPoint` parameter to `execute()` would be a clean extension.

### M-8: No plugin initialization hook

Plugins are instantiated in `load_plugins()` with `plugin_cls(plugin_config=config)`. There is no post-instantiation initialization hook where a plugin could validate its config or set up resources. If a plugin needs to validate that its config has a required key, it must do so in `__init__`, which means validation errors surface during loading (good) but with a generic exception rather than a plugin-specific error message.

---

## Off-Base Assumptions

### O-1: Engine integration points are not defined

The spec says plugins fire at lifecycle hook points, but the engine's `phases.py` does not import or call `execute_hooks()`. The wiring between the engine pipeline and the plugin system is unspecified. Looking at `engine/phases.py`, there is no mention of plugins anywhere in the 860-line file. The integration will require modifying `_run_single_round()` and `run_pipeline()` to call `execute_hooks()` at the appropriate points.

The spec says "The orchestrator MUST call `execute()` on every plugin registered for that hook" (FR-006), but the orchestrator code does not yet contain these calls. This is presumably intended to be implemented as part of this spec, but the spec text reads as if the integration already exists.

---

## Actionable Recommendations

1. **Add `features: Optional[FeatureSet] = None` to DeliberationState** (Priority: P1)
   - Specs 017-019 will all need feature vectors. Extracting once and passing through state is cleaner than each plugin independently calling `extract_features()`.

2. **Remove or rename the `config` parameter on `execute()`** (Priority: P2)
   - Either remove it (plugins use `self.plugin_config`) or rename to `plugin_config` to distinguish from `state.config`.

3. **Add `hook: HookPoint` parameter to `execute()`** (Priority: P2)
   - Enables multi-hook plugins to determine which hook fired without state inspection.

4. **Support named plugin class resolution in config** (Priority: P2)
   - Add an optional `class_name` field to plugin config entries. `load_plugins()` uses it to resolve a specific class from the module instead of first-found.

5. **Define engine integration points in spec or code** (Priority: P1)
   - Add `execute_hooks()` calls to `_run_single_round()` (POST_PHASE_5) and `run_pipeline()` (PRE_EXECUTION, POST_DELIBERATION, POST_ARBITRATION). This is the missing wiring that makes the plugin system functional.

6. **Add `POST_ITERATION` hook for per-iteration plugin execution** (Priority: P3)
   - Enables convergence predictors to run after each Phase 2-3 cycle. Requires a call site in the engine's iteration loop.

7. **Add plugin-to-plugin data passing via PluginContext** (Priority: P3)
   - Pass accumulated results from prior plugins within the same hook execution.

8. **Align AgentState with AgentFeatures or document the difference** (Priority: P2)
   - Either make AgentState reference AgentFeatures, or document that AgentState is a lightweight snapshot while AgentFeatures is the full numerical vector.
