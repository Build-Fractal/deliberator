# Plugin Engineer Revised Review -- Spec 022 Kalman Convergence

**Reviewer**: plugin-engineer
**Phase**: 3 (revised after cross-review)
**Date**: 2026-04-01

---

## Changes from Phase 1

1. **Withdrawn: "auto" threshold of 2 as "arbitrary."** The solver-engineer correctly argued that 2 is not arbitrary -- the Kalman filter is a recursive estimator that produces valid posteriors after each observation, and 2 rounds is the minimum needed to detect a trend direction. The spec-compliance reviewer noted that the spec explicitly says "the Kalman filter must work with as few as 2 data points," making 2 the natural threshold. Raising it to 3 would mean auto mode does not use Kalman at the spec's stated minimum. Reclassified from "off-base assumption" to "correct threshold, well-aligned with spec."

2. **Withdrawn: OLS/Kalman blending as "missed opportunity."** The solver-engineer pointed out that mixing OLS trends into the Kalman state would double-count evidence, violating the information-theoretic basis of the filter. The two paths being self-contained is correct architecture, not a limitation. If ensemble methods are desired, they should be proper Bayesian model averaging, which is a separate feature.

3. **Added: FR-005 compliance gap (innovation sequence).** The spec-compliance cross-review flagged that I missed the most significant compliance gap in the implementation. `detect_fixed_point()` checks state estimate deltas rather than the innovation sequence as FR-005 requires. The innovation vector is computed in `kalman_update()` (line 289) but discarded. I should have caught this in my review of the integration layer since `detect_fixed_point()` is called from `_predict_convergence_kalman()`.

4. **Added: Confidence calibration concern.** The solver-engineer's finding that `compute_kalman_confidence()` depends on arbitrary initialization (M1) has implications for the plugin layer. The confidence value drives the `min_confidence` threshold comparison that classifies predictions as converge/stagnate/uncertain. If the confidence is not properly calibrated, the classification logic produces unreliable outputs even though the integration wiring is correct. I should have caught this as a plugin reliability concern.

5. **Retained: Q/R plugin config wiring at P1.** All three reviews agree this is a compliance gap (FR-007). The fix is 3-5 lines of code.

6. **Retained: Method validation at P1.** The spec-compliance reviewer agreed this is a legitimate concern, noting that an unknown method value is "undefined behavior" per the spec.

7. **Retained: Equilibrium scores TODO at P2.** All reviewers agree this degrades the filter. The solver-engineer added that it compounds the confidence calibration issue by inflating covariance in the eq_score dimension.

8. **Downgraded: Refactoring `_predict_convergence_kalman` from P4 to out-of-scope.** The spec-compliance reviewer correctly noted this is a code quality concern, not a compliance or integration concern. Removed from recommendations.

---

## Revised Recommendations

### P1 (Critical)

1. **Wire Q/R from plugin config to `predict_convergence()`.** In `ConvergencePredictor.execute()`:
   ```python
   Q = config.get("process_noise_Q")
   R = config.get("observation_noise_R")
   ```
   Pass as `Q=Q, R=R` kwargs. Closes FR-007 at the plugin layer.

2. **Validate `convergence_method` config value.** At the top of `execute()`, check against `("auto", "kalman", "ols")`. Log warning and default to `"auto"` for unrecognized values. Prevents silent misconfiguration.

3. **Support FR-005 at the integration layer.** When the solver-engineer modifies `kalman_update()` to return innovation vectors, update `_predict_convergence_kalman()` and `detect_fixed_point()` calls to use innovation magnitudes instead of state deltas.

### P2 (High)

4. **Wire equilibrium scores from prior plugin results.** The `DeliberationState` should carry prior plugin outputs, or the predictor should read scores from the EquilibriumScorer's output. At minimum, document the integration pathway and remove the TODO. This affects filter effectiveness -- 1/3 of the state vector currently carries no information.

5. **Add `fallback_reason` field to PluginResult.data when Kalman falls back to OLS.** When the exception fallback is triggered (convergence.py line 690), propagate the reason into the output. This does not change the top-level format (additive field) but gives operators visibility.

6. **Add integration test for config passthrough.** Write a test that verifies `plugin_config={"process_noise_Q": [[...]], "observation_noise_R": [[...]]}` flows through and affects output. Also test `plugin_config={"convergence_method": "invalid"}` for graceful handling.

### P3 (Medium)

7. **Add test for Kalman exception fallback.** Force a Kalman failure (e.g., by passing a singular R matrix) and verify OLS fallback occurs with a logged warning.

8. **Document the auto-mode threshold rationale.** Add a code comment explaining why 2 rounds is the threshold, citing the spec's 2-point minimum and the Kalman filter's recursive nature.

9. **Add `kalman_diagnostics` sub-dict to output data.** Include innovation magnitude, covariance trace, and fixed-point status. This does not change top-level format but gives operators filter health visibility.

### P4 (Low)

10. **Define `ConvergenceMethod = Literal["auto", "kalman", "ols"]` type alias.** Reuse across `predict_convergence()` and `ConvergencePredictor.execute()` for single-source-of-truth validation.

---

## Referenced Documentation

- `conversus/plugins/nashopt/kalman.py` -- Kalman filter core (436 lines)
- `conversus/plugins/nashopt/convergence.py` -- Convergence prediction (703 lines)
- `conversus/plugins/nashopt/predictor.py` -- Plugin wrapper (296 lines)
- `conversus/plugins/nashopt/__init__.py` -- Package exports (67 lines)
- `tests/test_kalman.py` -- Test suite (1002 lines)
- `specs/done/022-kalman-convergence/spec.md` -- Feature specification (87 lines)
