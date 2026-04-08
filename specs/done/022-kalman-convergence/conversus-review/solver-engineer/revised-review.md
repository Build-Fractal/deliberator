# Solver Engineer Revised Review -- Spec 022 Kalman Convergence

**Reviewer**: solver-engineer
**Phase**: 3 (revised after cross-review)
**Date**: 2026-04-01

---

## Changes from Phase 1

1. **Withdrawn: F=I as "off-base assumption."** Both cross-reviewers (plugin-engineer and spec-compliance) correctly argued that F=identity is the right choice for a deliberation system without physics. Disputes do not have momentum or velocity -- each round is a fresh agent interaction. The Kalman gain naturally adapts to trends through the innovation signal. F=I (random walk model) is more honest than an augmented velocity model that would overfit 2-3 data points. Reclassified from "off-base assumption" to "deliberate simplification, documented."

2. **Downgraded: `initial_P` configurability from P2 to P3.** The spec-compliance reviewer noted that `initial_P` is not mentioned in any FR or SC. The plugin-engineer noted that `initial_P` washes out after 2-3 observations. The confidence calibration fix (recommendation 1, retained at P1) is the proper solution to P-initialization sensitivity, not making P a tuning knob.

3. **Downgraded: Joseph form from P2 to P4.** Both cross-reviewers agreed this is a best practice but not required for 3x3 double-precision matrices at the scales involved. The spec does not mention numerical stability requirements. Retained as a low-priority preventive measure.

4. **Added: FR-007 plugin config gap.** Both cross-reviewers flagged that Q/R are not wired from plugin config to `predict_convergence()`. I missed this because my review focused on `kalman.py` and the math layer. This is a clear compliance gap and I add it as a P1 recommendation.

5. **Added: Equilibrium score dimension concern.** The plugin-engineer pointed out that the eq_score state dimension is always 0.0 because scores are not wired through (TODO in predictor.py). This means process noise inflates covariance in that dimension with no corrective observations, distorting the overall trace and confidence calculation. This amplifies my M1 finding (confidence calibration) -- the trace includes a dimension with unbounded growth.

6. **Retained: Confidence calibration (M1) at P1.** All reviewers agreed this is the most impactful finding. The spec-compliance reviewer explicitly noted it should have been flagged under FR-004.

7. **Retained: Innovation sequence for fixed-point detection (M2) at P1.** All three reviews converge on this being a compliance gap (FR-005 PARTIALLY MET). Upgraded from "missed opportunity" to "compliance gap requiring remediation."

---

## Revised Recommendations

### P1 (Critical)

1. **Fix confidence calibration.** Replace `1 - trace(P_final) / trace(P_initial)` with a formulation invariant to initialization. Recommended approach: use the ratio of posterior variance to the steady-state Kalman gain covariance, or the normalized innovation squared (NIS) averaged over the sequence. At minimum, normalize against `P_initial + Q` (the first prediction covariance) rather than `P_initial` alone.

2. **Fix fixed-point detection to use actual innovations.** Modify `kalman_update()` to return the innovation vector alongside the updated state. Add a `KalmanTrace` dataclass or extend `KalmanState` with an `innovation` field. Rewrite `detect_fixed_point()` to check innovation magnitudes. This closes FR-005.

3. **Wire Q/R from plugin config.** In `ConvergencePredictor.execute()`, read `config.get("process_noise_Q")` and `config.get("observation_noise_R")` and pass to `predict_convergence()`. This closes FR-007 at the plugin layer.

### P2 (High)

4. **Add observation validation.** Before processing each observation in `run_kalman_filter()`, verify all elements are finite (`math.isfinite`). Skip the update with a warning if not.

5. **Wire equilibrium scores from prior rounds.** Resolve the TODO in `predictor.py` line 257. The eq_score dimension carrying no information degrades the filter and inflates covariance in that dimension, compounding the confidence calibration issue.

6. **Make `initial_P` configurable** (downgraded from original P2). Add an `initial_P` parameter to `run_kalman_filter()` with the current `diag(10,1,1)` as default.

### P3 (Medium)

7. **Document the F=I model choice.** Add a module-level note explaining that the random walk model is deliberate, not an oversight, and that an augmented state with velocity is not appropriate for this domain.

8. **Add a `KalmanTrace` dataclass.** Return per-step innovation vectors and covariance traces for downstream diagnostics. This enables FR-005 compliance and future filter tuning (innovation whiteness tests, NIS).

9. **Handle singular S gracefully.** Return the prior state with a warning instead of raising `ValueError`. Prevents triggering the OLS fallback for transient numerical issues.

### P4 (Low)

10. **Add property tests for matrix operations.** Test algebraic invariants: `(AB)^T = B^T A^T`, `det(AB) = det(A)*det(B)`, `A A^{-1} = I` for random matrices.

11. **Apply Joseph form for covariance update** (downgraded from original P2). `P_post = (I-KH) P_pred (I-KH)^T + K R K^T`. Negligible cost, prevents theoretical PSD loss.

12. **Enforce covariance symmetry.** After each update, apply `P = (P + P^T) / 2`.

---

## Referenced Documentation

- `conversus/plugins/nashopt/kalman.py` -- Kalman filter core (436 lines)
- `conversus/plugins/nashopt/convergence.py` -- Convergence prediction (703 lines)
- `conversus/plugins/nashopt/predictor.py` -- Plugin wrapper (296 lines)
- `tests/test_kalman.py` -- Test suite (1002 lines)
- `specs/done/022-kalman-convergence/spec.md` -- Feature specification (87 lines)
