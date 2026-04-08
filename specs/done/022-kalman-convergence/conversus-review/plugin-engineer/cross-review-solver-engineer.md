# Cross-Review: plugin-engineer reviews solver-engineer

**Reviewer**: plugin-engineer
**Reviewing**: solver-engineer/review.md
**Phase**: 2 (cross-review)
**Date**: 2026-04-01

---

## Agreement

1. **Confidence calibration flaw (M1) is the strongest finding.** The solver-engineer's analysis of `1 - trace(P_final) / trace(P_initial)` being dependent on the arbitrary `initial_P` is convincing. Changing `initial_P` from `diag(10,1,1)` to `diag(100,10,10)` would dramatically change the confidence score for the same observations. This is a real calibration defect that affects the prediction classification (which uses confidence vs. `min_confidence` threshold).

2. **Fixed-point detection gap (M2) is valid and well-argued.** The distinction between state estimate deltas and the innovation sequence is important. The innovation has known statistical properties (should be white noise when the filter is well-tuned) that make it a better convergence diagnostic. Agree this needs fixing.

3. **Observation validation (M3, recommendation 3) is practical and important.** A NaN or inf in the observation vector would silently corrupt the entire filter state and cascade through all subsequent rounds. This is a real operational risk.

4. **Joseph form recommendation (recommendation 4) is correct but low urgency.** For 3x3 double-precision matrices with the magnitudes involved (disputes ~0-20, rates ~0-1, scores ~0-1), the standard form will not lose positive semi-definiteness in practice. But it costs almost nothing to add, so agree it is a good preventive measure.

5. **Property tests for matrix operations (recommendation 9) are a good idea.** The current tests verify specific cases but algebraic invariants like `(AB)^T = B^T A^T` would catch subtle errors that point tests miss.

## Disagreement

1. **F=I is not an "off-base assumption" -- it is the correct choice for this system.** The solver-engineer flags F=identity as assuming "no trend dynamics" and suggests an augmented state with velocity. But the deliberation system has no physics -- disputes do not have inertia or velocity. Each round's dispute count is a fresh outcome of agent interactions, not a trajectory with momentum. Using F=I (random walk) is more honest than assuming constant velocity, which would overfit short sequences and make false predictions (e.g., after 5->3, predicting 1 then -1). The Kalman gain naturally tracks trends through the difference between prediction and observation. F=I is the right call.

2. **The singular matrix recovery recommendation (recommendation 8) conflates two issues.** If `S = P_pred + R` is singular, it means `P_pred + R` has a zero eigenvalue, which implies both the prior uncertainty and observation noise in some direction are zero. This would mean we have perfect information in that direction, which contradicts having an observation. In practice with diagonal Q and R (both positive diagonal), S will never be singular. The `ValueError` is a safety net for pathological inputs (e.g., user passes `R = zeros`), not a production failure mode. Returning the prior unchanged would silently ignore the observation, which is arguably worse than failing loudly.

3. **`initial_P` configurability (recommendation 5) is medium priority, not high.** The solver-engineer rates this P2 (high) but in practice, users will not tune `initial_P` -- they will tune Q and R. The initial P washes out after 2-3 observations regardless of its value. The confidence calibration fix (recommendation 1) is the real solution to the P-initialization sensitivity, not making P configurable.

## Observations the solver-engineer missed

1. **No discussion of the plugin integration layer.** The solver-engineer review focuses entirely on `kalman.py` and the math in `convergence.py`. No assessment of whether the plugin wiring in `predictor.py` correctly passes parameters, handles errors, or formats output. The Q/R config passthrough gap (which both the plugin-engineer and spec-compliance reviews flag) is not mentioned.

2. **No discussion of the equilibrium score dimension.** The solver-engineer discusses the 3D state vector but does not note that the equilibrium_score component is always 0.0 because the scores are not wired through (TODO in predictor.py). This means the filter is tracking a 3D state where one dimension has no observations -- the process noise Q inflates covariance in that dimension every step with no corrective update, which distorts the overall trace and confidence.

3. **No discussion of test coverage gaps.** The solver-engineer notes the test suite but does not assess what is missing (e.g., no test for Kalman exception fallback, no test for 2-observation boundary, no test for the equilibrium score dimension).

## Net assessment

The solver-engineer review is mathematically rigorous and provides the deepest analysis of the filter mechanics. The confidence calibration finding (M1) is the most important issue across all reviews and requires remediation before the Kalman confidence score can be trusted. The F=I critique is overstated for this domain. The review's blind spot is the integration layer -- it treats `kalman.py` in isolation without considering how the math connects to the plugin config and output format.
