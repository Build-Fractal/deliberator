# Schema Engineer Cross-Review of Plugin Architect
# Spec: 016-plugin-system

**Cross-reviewer**: schema-engineer
**Reviewing**: plugin-architect's review at `conversus-output/plugin-architect/review.md`
**My review**: `conversus-output/schema-engineer/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: FeatureSet on DeliberationState — schema dependency concern

Plugin-architect R-1 recommends adding `features: Optional[FeatureSet] = None` to `DeliberationState`. This creates an import dependency from `conversus.plugins.base` on `conversus.schemas.features` (for the `FeatureSet` type). My review's A-5 confirms the plugins package imports nothing from the schemas package. Adding the FeatureSet import would violate the current architectural boundary.

**My position**: The dependency direction matters. The spec says plugins depend on the plugin package; the plugin package depends on nothing. If `DeliberationState` imports `FeatureSet`, then the plugin package depends on the schemas package. This is architecturally acceptable (plugins -> schemas -> pydantic) but it changes the dependency graph. The alternative is to type the field as `dict[str, Any] | None` (the serialized FeatureSet) and let plugins import FeatureSet themselves for deserialization. This preserves package independence at the cost of consumer convenience.

**Resolution needed**: Decide whether `conversus.plugins` may import from `conversus.schemas`. If yes, add the typed FeatureSet field. If no, use `dict[str, Any]` and document the schema reference.

### DC-2: Plugin-to-plugin data passing — PluginContext vs. keeping it simple

Plugin-architect M-4 proposes a `PluginContext` for accumulating results from prior plugins. My review does not address inter-plugin communication. The `PluginContext` adds complexity to the framework for a use case that is speculative: the spec does not define any plugin that consumes another plugin's output. Plugins 017-019 consume feature vectors from spec 015, not from each other.

**My position**: Defer plugin-to-plugin data passing. The current design where plugins read the `plugins/` directory for prior plugin output is adequate for the foreseeable use cases. If cross-plugin communication becomes necessary, it should be a separate spec rather than added to the framework prematurely.

---

## Tensions

### T-1: execute() config parameter — remove vs. type

Plugin-architect M-2 recommends removing or renaming the `config` parameter on `execute()`. My review M-1 recommends typing the state config. These are complementary fixes (see plugin-architect DC-1 cross-review). The tension is in the migration path: removing `config` from `execute()` is a breaking API change for any plugin that already uses it (even though no external plugins exist yet). Renaming to `plugin_config` is non-breaking because it is a keyword argument.

### T-2: POST_ITERATION hook — scope creep vs. genuine need

Plugin-architect M-3 proposes a `POST_ITERATION` hook for per-iteration plugin execution. The spec explicitly does not include this hook. Adding it requires engine modifications (adding a call site in the iteration loop) and expands the plugin system's scope beyond what spec 016 defines. This should be deferred to a spec 018 (convergence predictor) requirement, not added to the framework spec.

### T-3: Named plugin class resolution

Plugin-architect M-6 proposes an optional `class_name` field in plugin config for resolving specific classes from multi-class modules. My review does not address this. The current first-found behavior is adequate for the one-plugin-per-package convention. Named resolution adds config complexity for an edge case. Defer until a real multi-class package exists.

---

## Safe Agreements

- **SA-1: Plugin ABC enforces the correct contract** -- Both reviews agree the ABC design is sound.

- **SA-2: Exception isolation is correctly implemented** -- Both reviews confirm try/except in execute_hooks() satisfies FR-008.

- **SA-3: Sequential execution is enforced** -- Both reviews confirm declaration-order iteration.

- **SA-4: AgentState overlaps with AgentFeatures** -- Plugin-architect M-5 and my O-1 both identify this. The field overlap should be resolved.

- **SA-5: Engine integration is the missing piece** -- Both reviews independently identify that the plugin system is implemented but not wired into the engine.
