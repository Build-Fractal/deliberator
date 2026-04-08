# Cross-Review: Solver-Engineer Reviews Plugin-Architect

**Reviewer**: solver-engineer
**Reviewed**: plugin-architect
**Round**: 1, Phase 2
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1. Plugin-architect's Q/R fix proposes hardcoded 3x3 matrices; solver-engineer requires calibrated values

Plugin-architect (P1) proposes a fix for the Q/R dimension mismatch with specific hardcoded values: `Q = [[1.0, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.01]]` for the 3D case. The solver-engineer (R5) explicitly argues that the eq_score noise should be 10x the concession noise: `R[2][2] = 0.05` rather than `0.005`, because equilibrium score "compounds extraction noise, concession noise, and mode-specific logic." The plugin-architect's proposed Q matrix uses `0.01` for the third dimension (same as concession_rate), while the solver-engineer's analysis shows this underestimates process noise for eq_score. Deploying the plugin-architect's hardcoded values without the solver-engineer's calibration would create a filter that trusts eq_score too much, producing overconfident predictions -- the opposite of the spec's intent.

### DC-2. Plugin-architect frames the Kalman dimension issue as a "latent bug"; solver-engineer shows it is currently contained

Plugin-architect (O3) claims that calling `run_kalman_filter(observations_3d)` without explicit Q/R will produce "a corrupted matrix" because `_mat_add` on 2x2 + 3x3 "won't crash... it will just silently use the smaller dimension." The solver-engineer (Alignment 5) notes that "Q/R auto-sizing in convergence.py is correctly placed" -- meaning `_predict_convergence_kalman` always passes explicit 3x3 Q/R, so the `default_Q()` path is never triggered in the current codebase for 3D data. The plugin-architect is correct that the latent bug exists in the `run_kalman_filter` API, but wrong that it is currently triggered. The solver-engineer is correct that the current wiring is safe, but agrees (R1) that the API should be hardened. The contradiction is in urgency: plugin-architect treats this as an active corruption bug; solver-engineer treats it as a defensive improvement.

### DC-3. Contradictory characterization of the single-score problem's mathematical impact

Plugin-architect (M5) states the Kalman filter "is operating on fabricated data for all but the latest observation, which mathematically degrades the state estimate rather than improving it." This is an unqualified claim of degradation. The solver-engineer (Off-Base 2) provides a more nuanced analysis: the replicated score is "mathematically equivalent to asserting that eq_score was constant across all rounds -- a false prior that biases the filter toward the most recent value" and "artificially shrinks covariance." Shrinking covariance is not necessarily degradation -- it means overconfidence, which can produce better point estimates at the cost of poorly calibrated uncertainty bounds. The plugin-architect's blanket "degrades" claim does not hold if the most recent eq_score happens to be representative. The solver-engineer's "false prior" framing is mathematically more precise and leads to a different fix (masked observation update) than the plugin-architect's implication that the 3D path should not be used at all with limited data.

### DC-4. Deep immutability concern raised by plugin-architect, absent from solver-engineer

Plugin-architect (O2) identifies that mutable values in `plugin_results` can leak mutations across consumers because `model_copy` is shallow, and recommends `copy.deepcopy` (P3). The solver-engineer does not address mutation safety at all, praising the frozen state as "properly rebuilt via model_copy for each consumer" (Alignment 2). For a numerical solver, mutation of shared state between plugins would be catastrophic -- a consumer modifying a shared list of scores would corrupt all subsequent consumers' inputs. The solver-engineer's omission of this concern is surprising given the severity of the failure mode in numerical contexts.

---

## Tensions

### T1. Namespace collision prevention: urgency and mechanism

Plugin-architect (M1) proposes a namespace convention like `"equilibrium-scorer.score"` or a uniqueness check. The solver-engineer does not mention namespace collisions or duplicate producers at all. This could reflect the solver-engineer's narrower scope (numerical correctness rather than plugin ecosystem design), but the consequence of two producers silently overwriting scores would be a numerical bug -- squarely within the solver-engineer's domain. The solver-engineer's silence does not mean disagreement but leaves the architectural risk unaddressed from a numerical perspective.

### T2. Whether the frozen state copy mechanism is sufficient

Plugin-architect identifies shallow copy as a risk (O2) and recommends deep copy or immutable-value documentation (P3). The solver-engineer praises the same mechanism as clean (Alignment 2). The tension is whether current value types (floats, strings) make the risk theoretical or whether the recommendation should be preemptive for future producers that may store lists or dicts.

### T3. Priority ranking of the zero-score sentinel fix

Plugin-architect rates the `any(s != 0.0)` fix as P1-Critical. The solver-engineer rates it as P2-Important (R4). Both agree on the semantics: a legitimate 0.0 is informative. The disagreement is about whether this is a correctness bug (plugin-architect: it discards valid data, breaking the 3D path) or a robustness concern (solver-engineer: the fix is important but secondary to the dimension mismatch and replicated-score bugs which affect all 3D invocations, not just the zero-score edge case).

---

## Safe Agreements

### SA-1. The Q/R dimension mismatch in run_kalman_filter must be fixed

Both reviews identify this as a critical issue (plugin-architect O3/P1, solver-engineer R1). Both recommend auto-sizing default Q/R from observation dimension. The specific values differ (see DC-1), but the structural fix is identical.

### SA-2. Equilibrium score accumulation across rounds is necessary

Both reviews identify the single-element equilibrium_scores list as a fundamental limitation (plugin-architect M5/P1, solver-engineer Missed Opportunity 1/R3). Both note that `_equilibrium_trend` always returns 0.0 and the Kalman filter receives replicated rather than real historical data. Both recommend some form of cross-round persistence.

### SA-3. The topological sort implementation is correct

Both reviews validate Kahn's algorithm with declaration-order tiebreaking (plugin-architect A3, solver-engineer Alignment 1). Neither identifies any bug in the sort logic itself. Both confirm it satisfies FR-005 through FR-007.

### SA-4. The zero-score sentinel conflates "no data" with "score equals zero"

Both reviews flag the `any(s != 0.0 for s in equilibrium_scores)` check as semantically incorrect (plugin-architect O1, solver-engineer Off-Base 3). Both agree that `None` should be the sentinel for "no data" and that 0.0 is a legitimate observation. The fix recommendations are functionally identical.
