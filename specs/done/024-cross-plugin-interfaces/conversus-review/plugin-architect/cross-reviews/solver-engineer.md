# Cross-Review: Plugin-Architect Reviews Solver-Engineer

**Reviewer**: plugin-architect
**Reviewed**: solver-engineer
**Round**: 1, Phase 2
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1. Disagreement on whether Q/R auto-sizing in convergence.py is correct

The solver-engineer states that "Q/R auto-sizing in convergence.py is correctly placed" and that "the caller's Q/R override the 2x2 defaults" (Alignment point 5). However, both reviews agree that `run_kalman_filter` defaults to 2x2 Q/R when called without explicit overrides (solver-engineer R1, plugin-architect P1/O3). The contradiction is in the solver-engineer's framing: calling the convergence.py placement "correct" implies the bug is contained, when in fact any caller of `run_kalman_filter` that omits Q/R with 3D data triggers the mismatch. The solver-engineer's own R1 contradicts their Alignment point 5 -- if the auto-sizing is "correctly placed," why is R1 a critical fix? The real issue is that the defense is in the wrong layer: `run_kalman_filter` should auto-size defaults from observation dimension, not rely on every caller to pass correct matrices.

### DC-2. Conflicting assessment of whether the replicated-score problem is a "bias" or "fabricated data"

Plugin-architect (M5) characterizes the single-element equilibrium_scores replicated across rounds as "fabricated data for all but the latest observation, which mathematically degrades the state estimate." The solver-engineer (Off-Base 2) frames it as a "false prior that biases the filter toward the most recent value" and notes it "artificially shrinks covariance." These are not the same thing. Fabricated data implies the filter produces worse estimates than 2D. A false prior that shrinks covariance implies the filter produces overconfident estimates that may still be directionally correct. The distinction matters for the fix: if it is fabricated data, the 3D path should not run at all with a single score. If it is a false prior with shrunken covariance, a masked observation approach (solver-engineer R2) could salvage partial value. The two reviews recommend incompatible remedies without acknowledging the mathematical disagreement.

### DC-3. Contradictory positions on whether the 3D path improves predictions

Plugin-architect (M5) says the Kalman filter "is operating on fabricated data" and implies the 3D path actively harms predictions. The solver-engineer (Off-Base 1) goes further, arguing that even with correct data, "3D observation produces better Kalman predictions than 2D is not unconditionally true" due to signal double-counting between concession_rate and eq_score. Yet the solver-engineer's Alignment section praises the "NxN generalization" as "well-structured" and proposes fixes (R2, R3, R5, R6) that assume the 3D path is worth saving. Plugin-architect provides no such fixes for the 3D numerical path, focusing instead on data availability. If the plugin-architect is right that the data is fabricated, the solver-engineer's calibration recommendations (R5, R6) are tuning a fundamentally broken input. If the solver-engineer is right that the path is salvageable, the plugin-architect's framing undersells the importance of accumulation fixes.

---

## Tensions

### T1. Severity of the zero-score sentinel issue

Both reviews flag the `any(s != 0.0 for s in equilibrium_scores)` gate as problematic (plugin-architect O1, solver-engineer Off-Base 3). However, plugin-architect rates the fix as P1-Critical (alongside Q/R dimension mismatch), while the solver-engineer rates it as P2-Important (R4). The plugin-architect's reasoning is that a legitimate 0.0 score is now possible with spec 024's real wiring. The solver-engineer agrees on the semantics but considers it secondary to the numerical bugs. The difference is defensible -- architectural purity vs. numerical impact -- but the priority gap could cause this fix to be deferred when it arguably gates the correctness of the 3D path.

### T2. Scope of the accumulation fix

Plugin-architect (P1) proposes three alternatives for accumulating equilibrium scores: a history key in plugin_results, a predictor-internal accumulator, or persistent plugin_results across rounds. The solver-engineer (R3) proposes the same three options but adds a fourth: extending `RoundState` with an `eq_score` field. The solver-engineer explicitly notes that a predictor-internal accumulator "already has self.plugin_config, could add self._score_history" -- acknowledging this conflicts with stateless plugin design but treating it as pragmatically acceptable. Plugin-architect notes the conflict but does not endorse it. This tension reflects a deeper disagreement about whether plugins should be stateful for cross-round data.

### T3. Whether the frozen Pydantic shallow copy is a real problem

Plugin-architect (O2) identifies that mutable values in `plugin_results` can be mutated by consumers because `model_copy` is shallow. The solver-engineer does not mention this at all, instead praising the frozen state as clean (Alignment point 2). Plugin-architect recommends `copy.deepcopy` (P3). The solver-engineer's silence suggests they consider the practical risk negligible since current produced values are floats and strings. The tension is whether to design defensively for future producers or accept the current safety profile.

### T4. Priority of the performance concern in topological sort

Plugin-architect (M8) flags the O(N^2 log N) re-sort in Kahn's algorithm and recommends heapq as P3-Medium. The solver-engineer does not mention this at all, focusing exclusively on numerical correctness. This reflects differing review scopes -- architectural hygiene vs. solver correctness -- but the plugin-architect's own caveat ("fine for the expected plugin count under 20") undermines the priority assignment.

---

## Safe Agreements

### SA-1. Q/R dimension mismatch in run_kalman_filter is a critical bug

Both reviews independently identify that `default_Q()` and `default_R()` return 2x2 matrices while 3D observations require 3x3 (plugin-architect O3/P1, solver-engineer R1). Both recommend auto-sizing defaults from observation dimension. The fix is unambiguous and both rate it P1-Critical.

### SA-2. Single-element equilibrium_scores defeats the 3D Kalman path

Both reviews identify that the predictor receives only the current round's score and wraps it in a single-element list (plugin-architect M5, solver-engineer Missed Opportunity 1). Both agree this means `_equilibrium_trend` always returns 0.0 and the historical observations are replicated rather than real. Both recommend accumulation across rounds as the fix.

### SA-3. The topological sort and graceful degradation are correct

Both reviews validate Kahn's algorithm, declaration-order tiebreaking, and the `None`-based graceful degradation path (plugin-architect A2/A3, solver-engineer Alignment 1/2/3). Neither review identifies any bug in the sort itself or in the fallback to 2D when the scorer is absent.
