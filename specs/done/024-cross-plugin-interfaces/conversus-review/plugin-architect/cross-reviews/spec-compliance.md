# Cross-Review: Plugin-Architect Reviews Spec-Compliance

**Reviewer**: plugin-architect
**Reviewed**: spec-compliance
**Round**: 1, Phase 2
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1. Spec-compliance says "None identified" in Off-Base Assumptions; plugin-architect identifies three

Spec-compliance (Off-Base section) explicitly states "None identified in the core implementation." Plugin-architect identifies three off-base assumptions: the all-zero heuristic conflating absent data with zero scores (O1), the assumption that frozen Pydantic provides deep immutability (O2), and the assumption that Kalman dimension switching is transparent (O3). Of these, O1 and O3 are not mere missed opportunities but incorrect assumptions baked into the implementation logic. Spec-compliance's clean bill of health on assumptions means it either did not evaluate the convergence/Kalman layer at the assumption level, or it assessed these design choices as correct. Either way, the O1 zero-score conflation directly affects spec-compliance's own SC-002 verdict -- the "all-zero" fallback path that spec-compliance marks as MET is the very heuristic plugin-architect flags as off-base.

### DC-2. SC-001 verdict: MET vs. functionally broken

Spec-compliance marks SC-001 as MET, citing that "ConvergencePredictor reads `state.plugin_results.get('equilibrium_score')`" and passes it through to the 3D Kalman path (SC-001 evidence). Plugin-architect (M5) argues that the predictor wraps the single score in a one-element list, which means "rounds 1 through N all get the same eq_score from round N" -- the 3D Kalman filter operates on fabricated data. Spec-compliance acknowledges the single-element issue as a missed opportunity (Missed Opportunity 2) but does not consider it grounds for failing SC-001. The disagreement is about whether SC-001 means "the predictor uses the score" (spec-compliance's reading) or "the predictor uses the score effectively" (plugin-architect's reading). If the data is fabricated for all but the latest round, the predictor is technically using the score but not gaining the quality improvement the spec motivates.

### DC-3. Orchestration scope: spec-compliance flags an inconsistency that plugin-architect treats as correct

Spec-compliance (recommendation 10) notes that "spec section 8 states 'This spec does NOT implement the orchestration layer (#6/ORC)' but the implementation does wire orchestration logic in `execute_hooks`" and calls this "strictly beyond spec scope." Plugin-architect (A4) praises this same implementation as a "clean separation: declarations on ABC, execution in orchestrator" and treats the `execute_hooks` orchestration as a strength. This is a genuine contradiction about whether the implementation overstepped its spec boundary. If spec-compliance is correct that orchestration was out of scope, then the entire `execute_hooks` wiring should be flagged as scope creep. If plugin-architect is correct that the separation is clean and desirable, then the spec text is stale and should be updated (which spec-compliance also suggests). The reviews reach opposite conclusions about whether this is a problem.

---

## Tensions

### T1. Duplicate producer detection: error type and severity

Both reviews flag duplicate producers as a problem. Plugin-architect (M1, M7, P2) recommends raising `PluginDependencyCycleError` and treats it as P2-High. Spec-compliance (Missed Opportunity 3, recommendation 1) also recommends detection but suggests either `PluginDependencyCycleError` or "a new `DuplicateProducerError`" and rates it P1-High. The tension is twofold: spec-compliance rates it higher, and the error type matters -- a duplicate producer is not a cycle, and reusing `PluginDependencyCycleError` conflates two distinct failure modes. Plugin-architect's code sample reuses the cycle error; spec-compliance at least considers a dedicated type.

### T2. Whether `id(p)` usage is a real concern

Spec-compliance (Missed Opportunity 4) flags `id(p)` as unstable "across garbage collection cycles" and recommends using plugin name or integer index. Plugin-architect does not mention this at all, implicitly treating it as safe. Spec-compliance's own caveat -- "in practice this is safe because all plugins are alive during the sort call" -- weakens its own concern. Plugin-architect's silence may be more accurate: the plugins are held in a list passed to the function, so they cannot be garbage-collected during the sort. The concern is theoretically valid but practically moot.

### T3. Cross-hook lifetime documentation vs. specification

Plugin-architect (M2, P2-High) recommends adding an FR to the spec defining cross-hook lifetime semantics ("FR-011"). Spec-compliance (Missed Opportunity 1, recommendation 3) recommends adding documentation to the `execute_hooks` docstring. The difference is significant: a new FR is a spec-level constraint that must be tested and validated; a docstring note is informal guidance. Plugin-architect treats the undefined lifetime as a spec gap; spec-compliance treats it as a documentation gap. The correct scope depends on whether cross-hook data flow will ever be needed -- if so, the spec should define it; if not, documentation suffices.

### T4. Test coverage assessment

Spec-compliance maps every FR and SC to specific test classes and marks all as MET. Plugin-architect (M9) identifies a specific gap: "no test for producer that fails mid-chain." Spec-compliance does not mention this scenario at all. Additionally, spec-compliance's own recommendation 2 acknowledges that the SC-001 test "does not assert that 3D Kalman was actually used." These are compatible findings but spec-compliance's FR/SC verdicts create an impression of complete coverage that the identified test gaps undermine.

### T5. Assessment of the scorer's self-nesting pattern

Plugin-architect (M4) calls the `score_data["equilibrium_score"] = score_data["score"]` pattern a "workaround" that is "boilerplate-prone and easy to forget," recommending the orchestrator store the entire `result.data` under a plugin-namespaced key. Spec-compliance (Off-Base 2, minor) acknowledges the duplication is "subtle" but calls the approach "correct" since it is "necessary because `execute_hooks` extracts only keys listed in `produces`." The disagreement is about whether the extraction design is right: plugin-architect wants to change the orchestrator; spec-compliance accepts the current contract.

---

## Safe Agreements

### SA-1. All ten functional requirements are implemented correctly

Both reviews validate the core mechanism: `produces`/`consumes` declarations, topological sort, `plugin_results` propagation, graceful degradation, and cycle detection. Plugin-architect's Alignment section (A1-A6) and spec-compliance's FR table (FR-001 through FR-010 all MET) converge on this assessment.

### SA-2. Single-element equilibrium_scores is a limitation worth addressing

Plugin-architect (M5) and spec-compliance (Missed Opportunity 2) both identify that the predictor receives only the current round's score and that `_equilibrium_trend` requires 2+ values. Both recommend accumulation across rounds. Neither considers this a spec violation, but both flag it as a meaningful gap in the implementation's value delivery.

### SA-3. Duplicate producer keys should be detected

Plugin-architect (M1, M7) and spec-compliance (Missed Opportunity 3) independently identify that two plugins producing the same key results in silent overwrite. Both recommend detection and an error. The fix is uncontroversial.
