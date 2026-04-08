# Phase 5 Synthesis: Spec 022 -- Kalman-Filtered Convergence Prediction

**Spec**: 022-kalman-convergence
**Date**: 2026-04-01
**Agents**: statistician, plugin-engineer, spec-compliance

---

## Overall Assessment

The Kalman-filtered convergence predictor is mathematically correct and well-integrated with the existing plugin system. The pure Python 3x3 matrix operations are verified correct. The Kalman predict-update cycle faithfully implements the standard linear Kalman filter. Confidence calibration via covariance trace ratio is sound. Fixed-point detection via state change is more robust than OLS linear extrapolation. The OLS fallback is completely preserved. The method dispatch (auto/kalman/ols) is clean. The only spec compliance gap is FR-001: the spec describes scipy-gated dispatch, but the implementation uses a pure Python Kalman filter that is always available (strictly better). Full consensus was achieved with no remaining disputes.

---

## Consensus Findings

### 1. Pure Python Kalman Filter Is Correct (Consensus)

**Unanimous**. All 12 matrix helper functions are verified correct via analytic methods (identity, roundtrip, invariant checks). The Kalman predict and update equations are standard. The state model `[dispute_count, concession_rate, equilibrium_score]` with F = I and H = I is the simplest valid model. The filter correctly:
- Initializes from the first observation with high uncertainty.
- Updates toward observations with each round.
- Shrinks covariance monotonically with consistent observations.
- Handles 2+ data points (minimum for meaningful filtering).

### 2. Spec Amendment Needed for FR-001 (Consensus)

**Unanimous**. The spec says "When scipy (or a minimal Kalman implementation) is available." The implementation provides a minimal pure Python Kalman filter with no optional dependency. The spec should be amended to: "When 2+ rounds of history are available, the predictor MUST use the Kalman filter." This reflects the actual (and superior) implementation.

### 3. Initial Covariance Bias Must Be Documented (Consensus)

**Unanimous**. The initial covariance `diag(10, 1, 1)` makes confidence 83% dispute-driven (10/12 of the trace). This is a correct design choice (disputes are the primary convergence indicator) but must be documented to avoid user confusion.

### 4. Exception Handling Should Differentiate Logging Levels (Consensus)

**Consensus (statistician + plugin-engineer)**. The broad `except Exception` in the Kalman fallback should differentiate:
- Expected failures (ValueError, ArithmeticError): WARNING level.
- Unexpected failures (TypeError, AttributeError): ERROR level.
Both fall back to OLS, but ERROR triggers monitoring alerts.

### 5. OLS Backward Compatibility Preserved (Consensus)

**Unanimous**. The OLS path is extracted into `_predict_convergence_ols()` with no behavioral change. The ConvergencePrediction dataclass extension (new `method` and `confidence_bounds` fields with backward-compatible defaults) does not affect existing consumers.

### 6. Observation Noise R[0][0] Is Conservative (Consensus)

**Unanimous after revision**. R[0][0] = 0.5 for dispute counts is high given that disputes are integers with near-zero extraction noise. This makes the filter trust the process model over observations (smoother, less reactive). Document this as a deliberate trade-off.

### 7. All Constraints MET (Consensus)

**Unanimous**:
- No scipy dependency: MET (pure Python).
- No Plugin interface change: MET.
- No OLS breakage: MET.
- Works with 2 data points: MET.

### 8. Confidence Asymptote at ~91.5% (Finding)

spec-compliance calculates that confidence plateaus at `1 - trace(Q)/trace(P_initial) ~= 0.915` after many rounds. This is mathematically correct and desirable (reflects irreducible process noise). Document in the default_Q docstring.

---

<!-- DISPUTES_BEGIN -->

## Unresolved Disputes

None. All disagreements were resolved during the cross-review and revision phases. The specific resolutions:

- **Joseph form priority**: Downgraded from P2 to P3 by consensus. Simple form is correct for the expected input range.
- **SC-003 classification**: Upgraded from PARTIALLY MET to MET by consensus. "Correctly handles" is satisfied by the current test.
- **Exception handling**: Resolved by compromise -- catch all, differentiate logging levels.
- **Auto-dispatch threshold**: plugin-engineer withdrew configurability recommendation.

<!-- DISPUTES_END -->

---

## Compliance Summary

| Requirement | Status | Action |
|------------|--------|--------|
| FR-001 | PARTIALLY MET | Amend spec: remove scipy language |
| FR-002 | MET | None |
| FR-003 | MET | None |
| FR-004 | MET | None |
| FR-005 | MET | None |
| FR-006 | MET | None |
| FR-007 | MET | None |
| FR-008 | MET | None |
| SC-001 | MET | None |
| SC-002 | MET | None |
| SC-003 | MET | None |
| SC-004 | MET | None |
| Constraints | ALL MET | None |

---

## Recommended Actions (Priority Order)

1. **P1**: Amend spec FR-001 to remove scipy gating language; replace with round-count dispatch.
2. **P1**: Document initial covariance `diag(10, 1, 1)` bias in `run_kalman_filter()` docstring.
3. **P1**: Differentiate exception logging levels in Kalman fallback (WARNING vs. ERROR).
4. **P2**: Document R[0][0] = 0.5 conservatism and its smoothing-vs-reactivity trade-off.
5. **P2**: Clarify confidence_bounds None semantics in ConvergencePrediction docstring.
6. **P2**: Add classification edge case tests (dispute_est near 1.0, dispute_delta near 0.0).
7. **P2**: Add OLS regression test verifying identical output pre/post spec 022 refactor.
8. **P3**: Document confidence asymptote (~91.5%) in default_Q docstring.
9. **P3**: Consider Joseph form if numerical issues are observed in production.
10. **P3**: Consider configurable fixed-point detection threshold.
