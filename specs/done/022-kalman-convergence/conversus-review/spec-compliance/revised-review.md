# Spec Compliance Revised Review -- Spec 022 Kalman Convergence

**Reviewer**: spec-compliance
**Phase**: 3 (revised after cross-review)
**Date**: 2026-04-01

---

## Changes from Phase 1

1. **Upgraded FR-005 severity from "Moderate" to "Critical."** The solver-engineer's cross-review correctly argued that "MUST use X, not Y" where the implementation uses something closer to Y should be rated higher. The spec explicitly says "MUST use the innovation sequence (prediction error), not trend extrapolation." The current implementation compares successive state estimates, which is a filtered/smoothed version of the trend -- closer to what the spec prohibits than what it requires. Spec compliance is about mechanism, not just outcome.

2. **Downgraded SC-002 from MET to PARTIALLY MET.** The plugin-engineer's cross-review correctly identified that the test assertion `stag_width >= conv_width * 0.5` is weaker than the spec requirement of "wider confidence bounds." The spec says "wider" which implies strict inequality, not "at least half as wide." The test should enforce `stag_width >= conv_width` or the SC is not fully verified.

3. **Added: FR-004 calibration concern.** The solver-engineer's confidence calibration finding (`1 - trace(P_final) / trace(P_initial)` depends on arbitrary initialization) affects the "calibrated" part of "calibrated confidence intervals." The confidence *intervals* (from `P[0][0]`) are properly calibrated under the Gaussian model. But the *point confidence* (from `compute_kalman_confidence()`) is not calibrated against the data -- it is calibrated against the initialization choice. Since this point confidence drives the `min_confidence` classification logic, the prediction outcomes (converge/stagnate/uncertain) are sensitive to initialization. FR-004 remains MET because the spec focuses on confidence intervals, but I add a compliance note.

4. **Added: SC-004 verification note.** The plugin-engineer's cross-review noted I should verify the OLS output is compatible with pre-022 behavior, not just that a test exists. The test `test_ols_behavior_unchanged` verifies `prediction="converge"`, `confidence > 0.5`, `fixed_point_exists=True`, which covers the key outputs. No new fields are added to the OLS path (method defaults to "ols", confidence_bounds defaults to None).

5. **Added: Section 5 (Dependencies) assessment.** The spec says scipy is an "optional runtime dependency." The implementation has no scipy dependency at all -- it exceeds the spec by eliminating the dependency entirely rather than making it optional.

6. **Added: Hook point verification.** `predictor.py` line 181: `hooks = [HookPoint.POST_PHASE_5]`. This satisfies the "What does not change" section.

---

## Revised FR Assessment

### FR-001: MET (unchanged)
Kalman filter used when method="auto" and 2+ rounds. Pure Python implementation always available.

### FR-002: MET (unchanged)
OLS fallback via method="ols", auto with <2 rounds, or Kalman exception.

### FR-003: MET (unchanged)
3D state vector [dispute_count, concession_rate, equilibrium_score] implemented.

### FR-004: MET (with compliance note)
Confidence intervals produced from P[0][0] with configurable sigma. Confidence bounds included in output.

**Compliance note**: The *point* confidence from `compute_kalman_confidence()` is initialization-dependent and therefore not properly calibrated. This does not affect FR-004 (which specifies "calibrated confidence intervals" -- the intervals are calibrated) but affects the reliability of the `min_confidence` threshold classification. See solver-engineer M1 finding.

### FR-005: PARTIALLY MET (severity upgraded to Critical)
Fixed-point detection uses state estimate deltas (line 381) rather than the innovation sequence (line 289, computed but discarded). The spec uses "MUST" and explicitly contrasts innovation sequence with trend extrapolation.

### FR-006: MET (unchanged)
`method` and `confidence_bounds` in PluginResult.data. Verified by tests.

### FR-007: PARTIALLY MET (unchanged)
Function layer accepts Q/R. Plugin config layer does not wire them through.

### FR-008: MET (unchanged)
Kalman path computes its own rounds_remaining from state estimates.

---

## Revised SC Assessment

### SC-001: MET (unchanged)
Kalman gives higher confidence than OLS for decreasing disputes. Test verified.

### SC-002: PARTIALLY MET (downgraded from MET)
The test assertion `stag_width >= conv_width * 0.5` does not enforce "wider confidence bounds" as the spec requires. The stagnation bounds could be half the width of convergence bounds and the test would pass. To be MET, the test should assert `stag_width >= conv_width` (strictly wider or equal).

**Remediation**: Tighten the test assertion or add a separate test with controlled noise parameters that reliably produces wider stagnation bounds.

### SC-003: MET (unchanged)
Non-linear convergence pattern correctly handled with Kalman prediction.

### SC-004: MET (unchanged)
OLS behavior identical to pre-022 implementation. No scipy dependency exists.

---

## Revised Recommendations

### P1 (Critical)

1. **Fix FR-005: Store innovation vectors and use them for fixed-point detection.** Modify `kalman_update()` to return or store the innovation vector. Modify `detect_fixed_point()` to check innovation magnitudes, not state estimate deltas.

2. **Fix FR-007 plugin config: Wire Q/R from plugin config.** Read `process_noise_Q` and `observation_noise_R` from `plugin_config` in `ConvergencePredictor.execute()` and pass to `predict_convergence()`.

3. **Fix SC-002 test: Tighten the assertion.** Replace `stag_width >= conv_width * 0.5` with `stag_width >= conv_width` or add a controlled test that reliably produces wider stagnation bounds.

### P2 (High)

4. **Fix confidence calibration (FR-004 compliance note).** Replace `1 - trace(P_final) / trace(P_initial)` with a formulation that does not depend on initialization. This affects the `min_confidence` classification reliability.

5. **Add boundary test for 2-observation Kalman filter.** Verify the filter produces a valid prediction with high uncertainty when auto mode activates at the minimum threshold.

6. **Wire equilibrium scores.** Remove the TODO in predictor.py and connect the EquilibriumScorer output to the Kalman predictor.

### P3 (Medium)

7. **Add test for Kalman exception fallback.** Force a Kalman failure and verify OLS fallback with logged warning.

8. **Add test for invalid convergence_method config.** Verify graceful handling of unrecognized method strings.

9. **Document the auto-mode threshold rationale and F=I model choice.**

### P4 (Low)

10. **Make the auto-mode threshold configurable.** Add `kalman_min_rounds` to plugin config with default 2.

---

## Referenced Documentation

- `specs/done/022-kalman-convergence/spec.md` -- Feature specification (87 lines)
- `conversus/plugins/nashopt/kalman.py` -- Kalman filter core (436 lines)
- `conversus/plugins/nashopt/convergence.py` -- Convergence prediction (703 lines)
- `conversus/plugins/nashopt/predictor.py` -- Plugin wrapper (296 lines)
- `conversus/plugins/nashopt/__init__.py` -- Package exports (67 lines)
- `tests/test_kalman.py` -- Test suite (1002 lines)
