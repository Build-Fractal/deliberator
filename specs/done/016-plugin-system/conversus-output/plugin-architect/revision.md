# Plugin Architect Revision: 016 Plugin System Infrastructure

**Reviewer**: plugin-architect
**Revision iteration**: 1
**Date**: 2026-03-24

---

## Recommendation Dispositions

#### Recommendation 1: Add features: Optional[FeatureSet] to DeliberationState

- **Original position**: Add FeatureSet field so plugins access pre-extracted features.
- **Disposition**: Modified
- **Explanation**: Spec-compliance DC-1 correctly notes that spec 016 declares "Depends On: None." Adding a FeatureSet import creates a dependency on spec 015. Schema-engineer DC-1 raises the architectural concern of cross-package imports. Modified recommendation: add `features: dict[str, Any] | None = None` as an untyped field on DeliberationState. The orchestrator populates it with the serialized FeatureSet dict. Plugins that need typed access import FeatureSet themselves and call `FeatureSet.model_validate(state.features)`. This preserves spec 016's dependency-free status while providing the data pathway.

#### Recommendation 2: Remove or rename config parameter on execute()

- **Original position**: Remove the redundant `config` parameter.
- **Disposition**: Modified
- **Explanation**: Schema-engineer DC-1 proposes complementary fixes: type the state config AND remove the parameter. Modified recommendation: remove the `config` parameter from `execute()`. The new signature is `execute(self, state: DeliberationState) -> PluginResult`. Plugins read `state.config` for deliberation config and `self.plugin_config` for plugin-specific config. This eliminates the redundancy and the naming confusion.

#### Recommendation 3: Add hook: HookPoint parameter to execute()

- **Original position**: Let multi-hook plugins know which hook fired.
- **Disposition**: Withdrawn
- **Explanation**: With R-2's simplified signature `execute(self, state: DeliberationState)`, adding `hook` to the signature reintroduces parameter bloat. Multi-hook plugins can determine the hook from `state` context (e.g., `state.synthesis is None` at PRE_EXECUTION). The use case is rare (most plugins register for one hook). Withdrawn in favor of a simpler API surface.

#### Recommendation 4: Support named plugin class resolution

- **Original position**: Add optional `class_name` field to plugin config.
- **Disposition**: Surviving
- **Explanation**: Schema-engineer T-3 suggests deferring. The current first-found behavior is a documented limitation. Named resolution is a low-cost addition (one config field, one `getattr()` call in `_find_plugin_class()`). No cross-review argues it creates problems; only that it is not urgent. Maintaining at P2.

#### Recommendation 5: Define engine integration points

- **Original position**: Add execute_hooks() calls to the engine pipeline.
- **Disposition**: Surviving
- **Explanation**: All three reviews identify engine integration as the highest-priority gap. Spec-compliance DC-2 confirms this is a spec 016 deliverable. The integration points are: `run_pipeline()` calls `execute_hooks(PRE_EXECUTION)` after config parsing, `_run_single_round()` calls `execute_hooks(POST_PHASE_5)` after synthesis, `run_pipeline()` calls `execute_hooks(POST_DELIBERATION)` after all rounds, and `run_pipeline()` calls `execute_hooks(POST_ARBITRATION)` after arbitration.

#### Recommendation 6: Add POST_ITERATION hook

- **Original position**: Enable per-iteration plugin execution for convergence predictors.
- **Disposition**: Withdrawn
- **Explanation**: Spec-compliance T-1 and schema-engineer T-2 both argue this is scope creep for spec 016. The spec defines four hooks. A fifth hook should be proposed by spec 018 (convergence predictor) if needed. Withdrawn.

#### Recommendation 7: Add plugin-to-plugin data passing via PluginContext

- **Original position**: Pass accumulated results from prior plugins.
- **Disposition**: Withdrawn
- **Explanation**: Schema-engineer DC-2 and spec-compliance T-2 both argue this is speculative scope creep. No current spec requires cross-plugin communication. Plugins can read each other's output files if needed. Withdrawn.

#### Recommendation 8: Align AgentState with AgentFeatures

- **Original position**: Make AgentState reference AgentFeatures or use AgentFeatures directly.
- **Disposition**: Modified
- **Explanation**: Schema-engineer T-2 notes that with features on DeliberationState (R-1 modified), AgentState.positions becomes redundant. Spec-compliance T-3 notes the field is dead. Modified recommendation: remove `positions: list[dict[str, Any]]` from AgentState since it is never populated. AgentState retains its summary fields (recommendation_count, concession_count, surviving_count) as lightweight metrics. Feature vectors are accessed through `state.features`.

---

## New Recommendations

No new recommendations. The cross-review process did not surface issues outside the scope of my original review.

---

## Position Summary

Withdrew 3, modified 3, maintained 2. Added 0 new recommendations.

The most significant changes are the three withdrawals (hook parameter, POST_ITERATION hook, PluginContext). All three were correctly identified as scope creep by cross-reviewers. The spec 016 framework should remain minimal; extensions belong in the plugin specs that need them.

My highest-priority surviving recommendation is R-5 (engine integration). Without it, the plugin system is a framework without a caller. FR-006 cannot be MET until the orchestrator calls `execute_hooks()`.
