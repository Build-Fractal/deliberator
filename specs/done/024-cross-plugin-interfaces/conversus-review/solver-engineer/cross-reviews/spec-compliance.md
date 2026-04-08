# Cross-Review: Solver-Engineer Reviews Spec-Compliance

**Reviewer**: solver-engineer
**Reviewed**: spec-compliance
**Round**: 1, Phase 2
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1. SC-001 verdict MET despite broken 3D Kalman data path

Spec-compliance marks SC-001 as MET, citing evidence that "ConvergencePredictor reads `state.plugin_results.get('equilibrium_score')` and passes it to `predict_convergence` as `equilibrium_scores`" (SC-001 row). The solver-engineer identifies three compounding numerical bugs in this exact path: (1) the single-element score list is replicated across all historical rounds, creating a false constant-score prior (Off-Base 2), (2) the `any(s != 0.0)` gate discards legitimate zero scores (Off-Base 3), and (3) the observation noise R for eq_score is miscalibrated, trusting it as much as concession_rate despite higher uncertainty (R5). The predictor "uses" the score in the narrowest syntactic sense, but the 3D Kalman path produces numerically degraded predictions with the current wiring. Marking SC-001 as MET without qualifying that the numerical benefit is unrealized is misleading.

### DC-2. SC-002 fallback path relies on a heuristic the solver-engineer considers off-base

Spec-compliance marks SC-002 as MET, citing that "the predictor produces 2D vectors when scores are `None`, empty, or all-zero" (SC-002 row). The solver-engineer (Off-Base 3) identifies that the "all-zero" condition is wrong: `any(s != 0.0 for s in equilibrium_scores)` conflates "no data" with "score equals zero." A deliberation where the scorer runs but all agents are far from equilibrium (score = 0.0) would incorrectly fall back to 2D. Spec-compliance's SC-002 evidence includes `test_2d_with_all_zero_eq_scores` as positive evidence -- but this test validates the wrong behavior. SC-002's intent is fallback when the scorer is absent, not when the scorer produces zeros. The MET verdict is correct for the absent-scorer case but incorrect for the zero-score case, which spec-compliance treats as equivalent.

### DC-3. "None identified" in Off-Base Assumptions contradicts multiple numerical concerns

Spec-compliance (Off-Base section) states "None identified in the core implementation. The implementation faithfully follows the spec's proposed solution without making unsupported leaps." The solver-engineer identifies three off-base assumptions: (1) "3D is unconditionally better than 2D" (Off-Base 1) -- the spec assumes 3D improves predictions, but signal double-counting between concession_rate and eq_score may inflate confidence without improving accuracy; (2) replicated scores constitute "3D observations" (Off-Base 2); (3) zero scores mean "no data" (Off-Base 3). These are assumptions embedded in the implementation's mathematical model, not just wiring issues. Spec-compliance's clean verdict on assumptions suggests the review did not evaluate the numerical layer's correctness assumptions.

---

## Tensions

### T1. Scope of "compliance" when the spec's motivating claim is numerically unvalidated

Spec-compliance correctly verifies that all FRs are implemented and all SCs pass their tests. The solver-engineer (Missed Opportunity 2) notes there is "no cross-validation of 2D vs 3D prediction quality" and "no mechanism to compare whether 3D actually improves predictions." The spec's motivation (lines 7-8, 16-19) is that the 3D path restores lost quality. If the 3D path does not actually improve quality (due to the issues in Off-Base 1), every FR and SC can be MET while the spec's purpose is defeated. This is a tension in review methodology: spec-compliance reviews the letter of the spec; the solver-engineer evaluates whether the letter achieves the spirit.

### T2. Whether orchestration in execute_hooks is scope creep

Spec-compliance (recommendation 10) flags that the spec says "This spec does NOT implement the orchestration layer (#6/ORC)" but the implementation wires orchestration in `execute_hooks`. The solver-engineer does not mention scope at all -- the orchestration is simply the mechanism that enables the data flow the solver-engineer evaluates. From a solver perspective, the orchestration is invisible infrastructure; from a compliance perspective, it is a scope boundary violation. The tension is whether spec-compliance should report this as a deviation or accept it as a practical necessity (which spec-compliance's own recommendation to "update the spec" implicitly does).

### T3. Test coverage sufficiency

Spec-compliance maps each SC to specific tests and considers coverage adequate, noting only that "the SC-001 test does not assert that 3D Kalman was actually used" (recommendation 2). The solver-engineer (R8) identifies a more fundamental gap: "no test verifies that the Kalman filter itself runs correctly with 3D data and produces reasonable state estimates." The solver-engineer wants tests that validate numerical outcomes (state dimension, confidence bounds, convergence behavior), not just data flow plumbing. Spec-compliance's test-per-SC mapping satisfies FR-level verification but leaves the numerical correctness of the 3D path entirely untested.

### T4. Priority of duplicate-producer detection

Spec-compliance rates duplicate-producer detection as P1-High (recommendation 1), calling it enforcement of the spec's DAG constraint. The solver-engineer does not mention duplicate producers at all. This may reflect differing scopes: spec-compliance sees a DAG invariant violation; the solver-engineer sees a single-producer ecosystem (EquilibriumScorer) where the issue is currently impossible. The tension is about whether to prioritize theoretical correctness (spec-compliance) or active numerical bugs (solver-engineer).

---

## Safe Agreements

### SA-1. The topological sort and declaration mechanism are correctly implemented

Spec-compliance (FR-005 through FR-007, all MET) and the solver-engineer (Alignment 1) both validate Kahn's algorithm, declaration-order tiebreaking, and the produces/consumes declarations on the Plugin ABC. Neither review identifies any issue with the sort logic.

### SA-2. Graceful degradation when the scorer is absent works correctly

Spec-compliance (FR-004 MET, SC-002 MET) and the solver-engineer (Alignment 3) both confirm that when the scorer is not installed, `plugin_results.get("equilibrium_score")` returns `None` and the predictor falls back cleanly to 2D. The absent-producer path is sound.

### SA-3. Historical score accumulation would improve the implementation

Spec-compliance (Missed Opportunity 2, recommendation 4) and the solver-engineer (Missed Opportunity 1, R3) both identify that the predictor receives only the current round's score and that historical accumulation would enable `_equilibrium_trend` and better Kalman tracking. Both recommend extending the data model to persist scores across rounds.
