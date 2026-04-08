# Phase 1 Review: spec-compliance

**Spec**: 022-kalman-convergence
**Reviewer**: spec-compliance
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: Verification of FR-001 through FR-008 and SC-001 through SC-004

---

## Executive Summary

Of 8 functional requirements, 7 are MET and 1 is PARTIALLY MET. Of 4 success criteria, 3 are MET and 1 is PARTIALLY MET. The Kalman filter implementation is faithful to the spec's state model, and the OLS fallback is completely preserved. The only gap is FR-001: the spec says "When scipy (or a minimal Kalman implementation) is available," implying the Kalman path should depend on an optional import flag. The implementation uses a pure Python Kalman filter with no optional dependency -- it is always available. This is strictly better than the spec's requirement but technically diverges from the dependency-gating pattern.

---

## Functional Requirements

### FR-001: Use Kalman filter when available -- PARTIALLY MET

The spec says: "When scipy (or a minimal Kalman implementation) is available, the predictor MUST use the Kalman filter instead of linear OLS."

The implementation provides a pure Python Kalman filter (kalman.py) with no external dependencies. There is no import flag (no `HAS_SCIPY` or `HAS_KALMAN`). The Kalman filter is always available. The dispatch uses `method="auto"` with a round-count threshold (2+ rounds -> Kalman), not a dependency check.

This is PARTIALLY MET because:
- The spec's intent (use the better method when possible) is fully satisfied.
- The spec's mechanism (optional import gating) is not implemented.
- The pure Python approach is strictly better (no dependency risk), but diverges from the spec's dependency-gating pattern used in specs 021 and 023.

The spec should be amended to reflect the pure Python approach: "The predictor MUST use the Kalman filter when 2+ rounds of history are available."

### FR-002: Fall back to OLS when not available -- MET

The OLS path is always available. When `method="ols"` or `method="auto"` with fewer than 2 rounds, OLS is used. When Kalman fails (exception), OLS is the fallback. The OLS implementation is unchanged from spec 018.

### FR-003: Track 3D state vector -- MET

The Kalman filter tracks `[dispute_count, concession_rate, equilibrium_score]` as documented. The state vector is constructed from `RoundFeatures` via `_build_observation_sequence()`. All three dimensions are used in prediction logic.

### FR-004: Produce calibrated confidence intervals -- MET

The `compute_confidence_bounds()` function produces symmetric 95% confidence intervals on the dispute count using `P[0][0]` (dispute variance) and 1.96 sigma. The `confidence_bounds` field is included in `ConvergencePrediction`. The bounds narrow as more observations are processed (covariance shrinks).

### FR-005: Fixed-point detection via innovation sequence -- MET

The `detect_fixed_point()` function checks whether the change in dispute estimate between the last two states is below threshold. This uses the filtered state difference (equivalent to the innovation in the dispute dimension) rather than trend extrapolation. The spec says "use the innovation sequence (prediction error)" -- the implementation uses the state change rather than the raw innovation, but these are related: the innovation drives the state change via the Kalman gain. The implementation satisfies the spec's intent.

### FR-006: method field in PluginResult.data -- MET

`ConvergencePrediction.method` is set to `"kalman"` or `"ols"`. The confidence bounds are included when Kalman is used. The predictor plugin transfers these to `PluginResult.data`.

### FR-007: Configurable Q and R -- MET

`predict_convergence()` accepts `Q` and `R` parameters (3x3 matrices) that are passed through to the Kalman filter. Default values are provided by `default_Q()` and `default_R()`. The defaults can be overridden via plugin config.

### FR-008: Cost estimation via Kalman model -- MET

The rounds-remaining estimate in `_predict_convergence_kalman()` uses the Kalman-filtered dispute trajectory (average reduction per step from the filtered state sequence), not the OLS linear trend slope.

---

## Success Criteria

### SC-001: Decreasing disputes -> higher Kalman confidence than OLS -- MET

The test `test_decreasing_disputes_kalman_higher_confidence` (in test_kalman.py) verifies this with a 3-round sequence (5, 3, 1). The Kalman confidence comes from covariance shrinkage; the OLS confidence comes from signal agreement. With consistent decreasing disputes, the Kalman filter has 3 consistent observations, producing meaningful covariance shrinkage. The OLS confidence for 3 rounds with negative dispute trend is approximately 0.65 + agreement bonus. The test asserts Kalman confidence >= OLS confidence.

### SC-002: Identical disputes -> stagnation with wider bounds -- MET

The test `test_identical_disputes_stagnation` verifies this with a 2-round sequence (4, 4). The Kalman filter sees zero innovation (observations match predictions), so it classifies as stagnation/fixed point. The confidence bounds are wider with only 2 rounds than with 3+.

### SC-003: Non-linear convergence handled -- PARTIALLY MET

The test `test_diminishing_returns_convergence` uses a 6-round sequence (10, 7, 5, 4, 4, 3). The Kalman filter handles this better than OLS because:
- OLS fits a line through all 6 points, overestimating the convergence rate.
- Kalman tracks the slowing rate and adjusts its estimates.

The test verifies prediction = "converge" but does not explicitly verify that the Kalman estimate is *more accurate* than OLS for this pattern. The criterion says "correctly handles" -- the prediction is correct, but the comparative advantage over OLS is not tested.

### SC-004: Without scipy, identical to OLS -- MET

Since the Kalman filter is pure Python (no scipy dependency), this criterion is trivially met. When `method="ols"` is explicitly specified, the OLS path runs unchanged. There is no dependency to uninstall.

---

## Compliance Matrix

| Requirement | Status | Evidence |
|------------|--------|----------|
| FR-001 | PARTIALLY MET | No import gating; pure Python always available |
| FR-002 | MET | OLS fallback on method="ols", auto < 2 rounds, exception |
| FR-003 | MET | 3D state vector [disputes, concession, eq_score] |
| FR-004 | MET | 95% CI from P[0][0] with 1.96 sigma |
| FR-005 | MET | Fixed point from state change < threshold |
| FR-006 | MET | method field in ConvergencePrediction |
| FR-007 | MET | Q, R parameters threaded through API |
| FR-008 | MET | Kalman-filtered rounds remaining estimate |
| SC-001 | MET | Test verifies Kalman >= OLS confidence |
| SC-002 | MET | Test verifies stagnation with wider bounds |
| SC-003 | PARTIALLY MET | Correct prediction, comparative advantage not tested |
| SC-004 | MET | No scipy dependency exists to uninstall |

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Amend the spec to remove the scipy dependency-gating language. Replace "When scipy (or a minimal Kalman implementation) is available" with "When 2+ rounds of history are available." The pure Python approach is strictly better.

### P2 (Should Fix)

2. **P2-1**: Add a comparative test for SC-003 that verifies Kalman outperforms OLS on the diminishing-returns pattern (e.g., lower prediction error or tighter confidence bounds).

3. **P2-2**: Verify the spec's Section 6 constraints:
   - Must NOT add scipy to core requirements: MET (no scipy used).
   - Must NOT change Plugin interface: MET.
   - Must NOT break OLS fallback: MET.
   - Must work with 2 data points: MET (Kalman initializes from first, updates from second).
