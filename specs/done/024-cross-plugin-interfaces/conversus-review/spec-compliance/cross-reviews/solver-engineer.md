# Cross-Review: Spec-Compliance Reviews Solver-Engineer

**Reviewer**: spec-compliance
**Reviewed**: solver-engineer
**Round**: 1, Phase 2
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1. Solver-engineer's Off-Base 1 challenges the spec's central premise; spec-compliance's SC-001 MET depends on it

The solver-engineer (Off-Base 1) argues that "3D observation produces better Kalman predictions than 2D is not unconditionally true" because eq_score may double-count concession_rate signal, "inflating confidence without improving accuracy." If this is correct, then SC-001 -- which spec-compliance marks as MET based on the predictor using the 3D path -- achieves the letter of the spec while potentially violating its spirit. The spec's motivation (lines 7-8, 16-19) is that the 3D Kalman path is superior; the solver-engineer presents a mathematical argument that it may not be. Spec-compliance does not evaluate whether the spec's motivating assumption is valid -- it only checks whether the implementation matches the spec. This is a dangerous gap: all SCs can be MET while the feature actively degrades prediction quality.

### DC-2. Solver-engineer's R2 proposes masked observation update; this would break SC-002's test evidence

Solver-engineer (R2) recommends that when `len(equilibrium_scores) < len(history)`, the system should "only attach eq_score to the rounds where data exists, and use 2D observations for rounds without data." This means a single deliberation could have a mix of 2D and 3D observations. Spec-compliance's SC-002 test evidence (`test_2d_without_eq_scores`, `test_2d_with_none_eq_scores`) validates a clean binary: either all observations are 2D or all are 3D. The solver-engineer's masked approach creates a third state (mixed dimensionality) that the current test suite does not cover and that the spec does not define. If R2 is implemented, SC-002's tests would need to be rewritten to handle the mixed case, and the spec would need a new SC or FR for partial-data behavior.

### DC-3. Solver-engineer rates Q/R mismatch as P1-Critical but also says convergence.py handles it correctly

Solver-engineer (Alignment 5) states "Q/R auto-sizing in convergence.py is correctly placed" and that "the caller's Q/R override the 2x2 defaults." Then (R1) the solver-engineer rates the same Q/R mismatch as P1-Critical. Spec-compliance sees no current failure -- `_predict_convergence_kalman` always passes explicit Q/R. If the defense is correctly placed (Alignment 5), then R1 is a defensive hardening request, not a critical bug fix. The solver-engineer's own analysis undermines the P1 severity by confirming the current caller handles it. The risk is future callers, which would make this P2 or P3 from a compliance standpoint (not currently violating any FR or SC).

---

## Tensions

### T1. Whether R5 (R noise calibration) is a spec concern or a tuning concern

Solver-engineer (R5) recommends changing `R[2][2]` from `0.005` to `0.05` because equilibrium score "compounds extraction noise, concession noise, and mode-specific logic." From a spec-compliance perspective, the spec does not specify noise matrix values -- it specifies that the predictor should use eq_score when available (SC-001) and fall back to 2D when not (SC-002). Noise calibration is a parameter tuning concern outside the spec's scope. However, if poor calibration causes the 3D path to produce worse predictions than 2D, the spec's motivation is undermined even though all SCs are technically MET.

### T2. Joseph form covariance update (R7) is a numerical improvement beyond spec scope

Solver-engineer (R7) recommends the Joseph form for the Kalman covariance update to prevent loss of positive-definiteness. This is a valid numerical concern but has no connection to spec 024's functional requirements or success criteria. The spec adds produces/consumes declarations and data flow; it does not modify the Kalman filter's internal numerics. From a spec-compliance perspective, R7 belongs in a separate enhancement spec or maintenance task.

### T3. Whether docstring drift (R10) is a compliance issue

Solver-engineer (R10) notes that docstrings in convergence.py and kalman.py still say "2D" when the code now handles 2D/3D. Spec-compliance would consider this a documentation accuracy concern but not a functional requirement violation -- no FR or SC requires docstring accuracy. However, stale documentation about the state vector dimensionality could mislead future implementers and is a reasonable maintenance concern.

### T4. Initial covariance tuning (R6) priorities

Solver-engineer (R6) recommends changing the 3D initial P diagonal from `[10.0, 1.0, 1.0]` to `[10.0, 1.0, 0.25]` for the eq_score dimension. Like R5, this is parameter tuning. Spec-compliance cannot validate whether `1.0` or `0.25` is the correct initial variance without domain expertise about equilibrium score distributions. The recommendation may be mathematically sound, but it is outside the scope of FR/SC verification.

---

## Safe Agreements

### SA-1. The topological sort and plugin ordering are correct

Spec-compliance (FR-005, FR-007 MET) and the solver-engineer (Alignment 1) both validate Kahn's algorithm and declaration-order tiebreaking. The sort correctly orders scorer before predictor.

### SA-2. Graceful degradation when the scorer is absent is clean

Spec-compliance (FR-004, SC-002 MET) and the solver-engineer (Alignment 3) both confirm that `plugin_results.get("equilibrium_score")` returns `None` when the scorer is not installed, and the predictor falls back to 2D observations without error.

### SA-3. Historical equilibrium score accumulation would add value

Spec-compliance (Missed Opportunity 2, recommendation 4) and the solver-engineer (Missed Opportunity 1, R3) both identify the single-element score limitation and recommend accumulation across rounds. Both treat this as an enhancement rather than a bug, acknowledging the current behavior is per-spec but limiting.
