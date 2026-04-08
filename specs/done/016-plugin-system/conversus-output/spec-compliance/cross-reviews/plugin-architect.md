# Spec Compliance Cross-Review of Plugin Architect
# Spec: 016-plugin-system

**Cross-reviewer**: spec-compliance
**Reviewing**: plugin-architect's review at `conversus-output/plugin-architect/review.md`
**My review**: `conversus-output/spec-compliance/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: FeatureSet on DeliberationState — spec scope concern

Plugin-architect R-1 recommends adding `features: Optional[FeatureSet]` to `DeliberationState`. This is architecturally sound but introduces a dependency on spec 015's types. Spec 016 says "Depends On: None (infrastructure foundation for all plugin specs)." Adding a FeatureSet dependency means spec 016 now depends on spec 015's output types, contradicting the "Depends On: None" declaration.

**My position**: The FeatureSet field should not be added in this spec. It should be added in spec 017 (equilibrium scorer) or a glue spec that bridges feature extraction and the plugin system. Spec 016 is the framework; it should remain dependency-free.

### DC-2: Engine integration as spec deliverable — implicit vs. explicit

Plugin-architect R-5 recommends defining engine integration points. My review R-1 recommends wiring plugin loading and execution into the engine pipeline. Both identify the gap. The contradiction is in whether this is a spec 016 deliverable or an engine-team task. The spec text implies the integration exists ("the orchestrator MUST call execute()"), but the implementation does not contain it.

**My position**: Engine integration is a spec 016 deliverable. FR-006 says "At each lifecycle hook point, the orchestrator MUST call `execute()`." If the orchestrator does not do this, FR-006 is NOT MET regardless of whether the framework function exists. The spec cannot be "done" without engine integration.

---

## Tensions

### T-1: POST_ITERATION hook — scope of spec 016

Plugin-architect M-3 proposes a `POST_ITERATION` hook. My review does not address hooks beyond the four specified. The spec defines exactly four hooks. Adding a fifth is a spec amendment, not a bug fix. I agree the hook would be useful for spec 018, but it should be proposed as part of that spec, not added to the framework spec.

### T-2: Plugin-to-plugin data passing

Plugin-architect M-4 proposes a PluginContext for cross-plugin communication. The spec does not define any cross-plugin communication mechanism. This is scope creep. If plugins 017-019 need to communicate, that requirement should surface from those specs and be backported to the framework.

### T-3: AgentState and AgentFeatures overlap

Plugin-architect M-5 identifies the overlap and recommends alignment. My review does not flag this specifically but notes that `AgentState` fields are not populated by any code (implicit in the fact that engine integration is missing). The resolution depends on whether AgentState is populated from engine data (current design) or from AgentFeatures (plugin-architect's proposal). The current design is consistent with the spec; the alignment proposal requires a design decision beyond the spec's scope.

---

## Safe Agreements

- **SA-1: Plugin ABC design is correct** -- Both reviews agree the ABC with class-level name/hooks and instance-level config is the right pattern.

- **SA-2: Exception isolation is robust** -- Both reviews agree FR-008 is fully MET.

- **SA-3: Output namespacing is correct** -- Both reviews agree plugin output is properly isolated in `plugins/`.

- **SA-4: HookPoint enum covers specified lifecycle points** -- Both reviews agree the four hooks match the spec.

- **SA-5: Engine integration is the critical missing piece** -- Both reviews independently identify this as the highest-priority gap.

- **SA-6: FR-012 package naming should be amended** -- Both reviews agree the spec should reference `conversus.plugins` not `conversus-plugins`.
