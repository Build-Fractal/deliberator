# Spec-Compliance Revision — Spec 024: Cross-Plugin Interfaces

**Reviewer**: spec-compliance
**Round**: 1, Phase 3 (Revision)
**Date**: 2026-04-01

**Inputs**: Own review, cross-reviews received (plugin-architect, solver-engineer), cross-reviews written (about plugin-architect, solver-engineer).

---

## Positions Revised

### R1. Revise SC-001 from MET to PARTIAL

**Original position**: SC-001 ("ConvergencePredictor uses real eq_score when EquilibriumScorer is installed") marked as MET based on evidence that the predictor reads the score from `plugin_results` and passes it through to `predict_convergence`.

**Revision**: Both plugin-architect (M5, cross-review DC-1) and solver-engineer (Off-Base 2, cross-review DC-1) argue that the predictor receives only a single score replicated across all historical rounds, which the solver-engineer characterizes as a "false prior that artificially shrinks covariance." The spec's motivation section (lines 7-8, 16-19) explicitly states the goal is to restore the quality regression caused by the 3D-to-2D downgrade. If the 3D path operates on replicated rather than real per-round data, the quality improvement is unrealized.

I revise SC-001 to **PARTIAL**: the wiring is correct (the predictor receives and passes through the real eq_score for the current round), but the full intent of the success criterion -- quality improvement from 3D Kalman -- is not yet delivered due to the single-element history limitation.

### R2. Acknowledge off-base assumptions in the convergence layer

**Original position**: "None identified in the core implementation."

**Revision**: The plugin-architect (O1, O3) and solver-engineer (Off-Base 1, 2, 3) identified three off-base assumptions in the convergence/Kalman layer that I missed:

1. The `any(s != 0.0)` gate conflates "no data" with "score equals zero" (plugin-architect O1, solver-engineer Off-Base 3). This is a genuine assumption error, not just a missed opportunity.
2. The spec assumes 3D is unconditionally better than 2D (solver-engineer Off-Base 1). Signal double-counting is a valid mathematical concern.
3. Replicated scores do not constitute real 3D observations (solver-engineer Off-Base 2).

My original review focused on the plugin framework layer (declarations, sort, orchestration) and did not deeply evaluate the Kalman layer's mathematical assumptions. I accept these findings and revise my Off-Base section to include items 1 and 3. Item 2 (conditional 3D superiority) is the spec's assumption, not the implementation's, so it belongs as a spec-level concern rather than an implementation off-base assumption.

### R3. Revise SC-002 evidence to exclude the zero-score case

**Original position**: SC-002 evidence included `test_2d_with_all_zero_eq_scores` as positive evidence for the fallback path.

**Revision**: The solver-engineer's cross-review (DC-2) correctly identifies that the all-zero fallback is wrong behavior validated by a test. A deliberation where the scorer produces legitimate zeros should use 3D, not fall back to 2D. The SC-002 verdict remains MET for the absent-scorer case (`None`, empty list), but I remove `test_2d_with_all_zero_eq_scores` from the positive evidence and add it as a test that validates incorrect behavior. SC-002 is MET with a caveat: the zero-score edge case needs a fix.

### R4. Upgrade duplicate-producer detection to P1-High

**Original position**: P1-High (recommendation 1).

**Revision**: I maintain P1-High but adopt the plugin-architect's recommendation of using a dedicated `DuplicateProducerError` rather than reusing `PluginDependencyCycleError`. A cycle and a duplicate producer are semantically different failures. The error type should reflect the failure mode.

---

## Positions Maintained

### M1. Cross-hook lifetime is a documentation concern, not a new FR (DISPUTE)

Plugin-architect (M2, P2-High) insists on adding "FR-011" to the spec. I maintain that a docstring note in `execute_hooks` is sufficient for three reasons:

1. **Scope**: The spec explicitly states "This spec adds declarations to the Plugin ABC." Adding orchestration-lifetime FRs expands scope.
2. **Testability**: The current behavior (per-hook scoping) is an emergent property of `execute_hooks` re-initializing `plugin_results` from `state.plugin_results` at line 462. A test for this already exists implicitly in the execution tests. A formal FR would mandate a dedicated test for something already covered.
3. **Flexibility**: Formalizing per-hook scoping as an FR constrains future designs. If a future spec needs cross-hook data (e.g., for stateful plugins), the FR would need to be modified. A docstring communicates current behavior without creating a rigid constraint.

**Why maintained**: The plugin-architect's argument that "undocumented behavior that works by coincidence is worse for long-term maintenance" is valid, but documentation in the docstring is still documentation. The question is whether it needs to be a testable requirement or advisory guidance. I maintain the latter.

### M2. The orchestration in execute_hooks should be reconciled with spec section 8

I maintain that spec section 8's statement "This spec does NOT implement the orchestration layer (#6/ORC)" is inaccurate given the implementation. The plugin-architect praises the orchestration as a strength (A4); I agree it is well-implemented. But the spec text should be updated to reflect reality. This is not a criticism of the implementation -- it is a criticism of stale spec text.

### M3. Test-per-SC methodology is the correct compliance approach

The solver-engineer's cross-review (T1, T3) argues that all SCs can be MET while the spec's purpose is defeated, and that numerical correctness of the 3D path is untested. I accept both observations but maintain that spec-compliance review is correctly scoped to verifying FRs and SCs against the spec text. The spec's motivating assumption (3D improves quality) is a spec authoring concern, not a compliance concern. My revision of SC-001 to PARTIAL is as far as compliance review should go -- beyond that, the solver-engineer's concerns about calibration, double-counting, and Joseph form are numerical engineering concerns that should be addressed in a follow-up spec or implementation task, not by expanding the compliance review's scope.

---

## New Positions

### N1. Add a new SC for the zero-score sentinel fix

Neither the current spec nor my original review includes a success criterion that validates correct behavior when eq_score = 0.0. Given the consensus across all three reviewers that the `any(s != 0.0)` gate is wrong, I recommend adding:

**SC-006**: When `EquilibriumScorer` produces `equilibrium_score = 0.0`, `ConvergencePredictor` MUST use 3D observations (not fall back to 2D).

This makes the fix testable and prevents regression.

### N2. Acknowledge the solver-engineer's 3D Kalman test gap

The solver-engineer (R8) is correct that no test exercises the actual Kalman filter with 3D data end-to-end. While this is beyond spec 024's defined SCs, it is a meaningful gap in the implementation's validation. I add it as a P2 recommendation.

### N3. The solver-engineer's masked observation approach (R2) needs a spec addendum

If implemented, the masked observation approach (mixed 2D/3D observations within a single deliberation) creates behavior not defined by any FR or SC. A spec addendum or follow-up spec should define the expected behavior for partial equilibrium score availability.

---

## Summary of Verdict Changes

| Criterion | Original Verdict | Revised Verdict | Reason |
|-----------|-----------------|-----------------|--------|
| SC-001 | MET | PARTIAL | Quality benefit unrealized due to single-element history |
| SC-002 | MET | MET (with caveat) | Zero-score case validates wrong behavior |
| SC-003 | MET | MET | Unchanged |
| SC-004 | MET | MET | Unchanged |
| SC-005 | MET | MET | Unchanged |
| FR-001 through FR-010 | All MET | All MET | Unchanged |

## Summary of Priority Changes

| Item | Original Priority | Revised Priority | Reason |
|------|------------------|-----------------|--------|
| Duplicate producer detection | P1-High | P1-High (with DuplicateProducerError) | Error type refined |
| 3D Kalman end-to-end test | (new, adopted from solver-engineer) | P2-Medium | Not in spec SCs but important |
| Zero-score sentinel SC-006 | (new) | P1-High | Consensus across all reviewers |
| Cross-hook lifetime | P1-High (docstring) | P1-High (docstring, dispute with plugin-architect) | Maintained |
