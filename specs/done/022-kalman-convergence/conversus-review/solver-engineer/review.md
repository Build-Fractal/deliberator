# Solver Engineer Review -- Spec 022 Kalman Convergence

**Reviewer**: solver-engineer
**Phase**: 1 (independent review)
**Date**: 2026-04-01
**Spec**: 022-kalman-convergence
**Files reviewed**: spec.md, kalman.py, convergence.py, predictor.py, test_kalman.py

---

## Executive Summary

The Kalman filter implementation is mathematically correct for the stated model (F=I, H=I, diagonal Q/R). The 3x3 matrix operations are sound and well-tested, the standard predict-update cycle is faithfully reproduced, and the cofactor-based inverse is textbook. However, the confidence calibration has a structural flaw: it compares initial covariance to final covariance, which conflates filter initialization choices with genuine information gain. Fixed-point detection is a simplification of what the spec describes -- it checks state estimate deltas rather than the innovation sequence proper. The implementation is a solid v1 but leaves numerical edge cases and calibration rigor on the table.

---

## Alignment

### What the implementation gets right

1. **Correct Kalman update equations.** The predict step `P_pred = F P F^T + Q` and update step `K = P_pred H^T S^{-1}`, `x_post = x_pred + K * innovation`, `P_post = (I - KH) P_pred` are textbook correct for the linear Gaussian case. Since F=I and H=I, the simplifications are valid.

2. **Pure Python matrix math is correct.** The 3x3 cofactor-based inverse matches the analytic formula. Determinant computation via Sarrus' rule is correct. Matrix multiplication uses the standard O(n^3) triple loop. All operations verified by roundtrip tests (A @ A^{-1} = I).

3. **Diagonal noise assumption is reasonable.** For 3 uncorrelated state variables (dispute_count, concession_rate, eq_score) that have very different magnitudes and units, diagonal Q and R are the right starting point. Cross-correlations can be added later as off-diagonal terms without changing the filter equations.

4. **Initialization from first observation.** Setting x_0 = z_0 with high initial P is standard practice when no prior exists. The heterogeneous initial P (10.0 for disputes, 1.0 for rates/scores) correctly reflects the different scales of the state variables.

5. **Confidence bounds from P[0][0].** Using the posterior variance of the dispute estimate to construct a symmetric Gaussian CI is standard Kalman output. The 1.96-sigma default gives a proper 95% CI under Gaussian assumptions.

---

## Missed Opportunities

### M1: Covariance shrinkage confidence is structurally flawed

The confidence formula `1 - trace(P_final) / trace(P_initial)` has a fundamental problem: `P_initial` is the *initialization* covariance, not the prior covariance. With `initial_P = diag(10, 1, 1)` and `trace = 12.0`:

- After 1 observation: confidence = 0.0 (initial = final).
- After 2 observations: confidence depends on how much P shrank from the arbitrary starting point.

This means confidence is calibrated against an *arbitrary* initialization choice, not against genuine information content. If you change `initial_P` to `diag(100, 10, 10)`, confidence jumps even though you have the same observations. A better approach: base confidence on the ratio of posterior variance to observation noise variance, or use the Kalman filter's own normalized innovation squared (NIS) statistic.

### M2: Fixed-point detection checks state deltas, not innovations

The spec explicitly says (FR-005): "Fixed-point detection MUST use the innovation sequence (prediction error), not trend extrapolation." The implementation in `detect_fixed_point()` checks `abs(states[-1].x[0] - states[-2].x[0])`, which is the *state estimate* change, not the innovation (z - H*x_pred). These are related but distinct: the state estimate change is a filtered quantity, while the innovation is the raw prediction error. The innovation sequence has well-known statistical properties (white noise when the filter is well-tuned) that the state delta does not.

### M3: Joseph form not used for covariance update

The implementation uses `P_post = (I - KH) P_pred` which is the standard form. This is fine for well-conditioned problems but can lose positive semi-definiteness due to floating-point errors. The Joseph form `P_post = (I - KH) P_pred (I - KH)^T + K R K^T` is numerically more stable. For 3x3 with double precision this is unlikely to bite, but it is a known best practice and costs negligible computation at this matrix size.

### M4: No singular matrix recovery path

If `S = P_pred + R` becomes singular (det < 1e-12), the filter raises `ValueError`. In a production convergence predictor, this should be handled gracefully -- e.g., skip the update and return the prior, or fall back to OLS. The exception will propagate up through the Kalman path and trigger the OLS fallback in `predict_convergence()`, but this is a blunt recovery.

### M5: No observation validation

There is no check that observation vectors have the right dimensionality or contain finite values. Passing `[nan, inf, 0.0]` will silently corrupt the filter state. A quick `all(math.isfinite(v) for v in obs)` check would prevent cascading failures.

---

## Off-Base Assumptions

### O1: F=I assumes no trend dynamics

The spec describes the process model as "linear trend extrapolation" (`x_k = F * x_{k-1} + w`), but the implementation uses F=identity. This means the process model assumes the state *persists* (random walk), not that it *trends*. For a system where disputes are expected to decrease round over round, a trend model would use an augmented state `[dispute, dispute_velocity, ...]` with F capturing the velocity. The current model works -- the Kalman gain adapts -- but it cannot predict ahead of the current observations. This is acceptable for a v1 but should be documented as a deliberate simplification.

### O2: Initial P scaling is undocumented

The choice of `initial_P = diag(10, 1, 1)` is reasonable but has no justification in the code or spec. The 10x scaling on disputes vs. rates/scores implicitly assumes disputes are "10x less certain" initially. This affects confidence calibration (see M1) and should be a configurable parameter or at least documented.

---

## Actionable Recommendations

### P1 (Critical)

1. **Fix confidence calibration.** Replace `1 - trace(P_final) / trace(P_initial)` with a formulation that is invariant to initialization. Candidate: `confidence = 1 - trace(P_final) / trace(P_prior_first_predict)` where `P_prior_first_predict = P_initial + Q`. This normalizes against the first prediction step rather than initialization. Better still: use the normalized estimation error squared (NEES) or averaged NIS.

2. **Fix fixed-point detection to use actual innovations.** Store the innovation vector `z - H*x_pred` during each `kalman_update()` call (it is already computed as `innovation` on line 289 of kalman.py but discarded). Return it alongside `KalmanState` or in a separate sequence. Then `detect_fixed_point()` can check innovation magnitude, not state deltas.

### P2 (High)

3. **Add observation validation.** Before processing each observation in `run_kalman_filter()`, verify all elements are finite. Log a warning and skip the update if not.

4. **Use Joseph form for covariance update.** Replace `P_post = (I - KH) P_pred` with `P_post = (I - KH) P_pred (I - KH)^T + K R K^T`. This costs one extra matrix multiply and two additions -- negligible for 3x3.

5. **Make initial_P configurable.** Add an `initial_P` parameter to `run_kalman_filter()` so callers can set it. Default to the current `diag(10, 1, 1)`.

### P3 (Medium)

6. **Document the F=I simplification.** Add a module-level note explaining that the current model is a random walk, not a trend model, and that an augmented state with velocity could be a future enhancement.

7. **Add a `KalmanTrace` dataclass.** Return per-step innovation vectors alongside states so that downstream code can perform proper filter diagnostics (innovation whiteness test, NIS test). This enables FR-005 compliance and future filter tuning.

8. **Handle singular S gracefully.** Instead of raising `ValueError`, return the prior state unchanged with a warning. This avoids triggering the OLS fallback for a transient numerical issue.

### P4 (Low)

9. **Add property tests for matrix operations.** The test suite verifies specific cases but does not test algebraic properties like `(AB)^T = B^T A^T`, `A A^{-1} = I` for random matrices, or `det(AB) = det(A) * det(B)`. These would catch subtle sign errors.

10. **Consider symmetric positive-definite enforcement.** After each update, force P_post to be symmetric via `P = (P + P^T) / 2`. This is cheap and prevents drift from asymmetric rounding.

---

## Referenced Documentation

- `conversus/plugins/nashopt/kalman.py` -- Kalman filter core implementation (436 lines)
- `conversus/plugins/nashopt/convergence.py` -- Convergence prediction with Kalman/OLS dispatch (703 lines)
- `conversus/plugins/nashopt/predictor.py` -- Plugin wrapper (296 lines)
- `tests/test_kalman.py` -- Test suite (1002 lines)
- `specs/done/022-kalman-convergence/spec.md` -- Feature specification (87 lines)
