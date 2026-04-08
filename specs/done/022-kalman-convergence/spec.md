# Feature Specification: Kalman-Filtered Convergence Prediction

**Feature ID**: `022-kalman-convergence`
**Created**: 2026-03-25
**Status**: Draft
**Depends On**: `018-convergence-predictor` (heuristic predictor to upgrade), `015-feature-extraction` (feature time series), `021-nashopt-integration` (equilibrium scores as input signal)
**Origin**: Review finding — spec 018 implements linear OLS trend only. This spec delivers Kalman-filtered surrogate models.

---

## 1. Feature Summary

Replace the linear trend analysis in the convergence predictor with Kalman-filtered surrogate models that track uncertainty and predict convergence with calibrated confidence intervals. The linear predictor remains as the zero-dependency fallback.

**What changes**: `conversus/plugins/nashopt/convergence.py` gains a Kalman filter path. New `conversus/plugins/nashopt/kalman.py` implements the state estimator. Confidence intervals replace point estimates.

**What does not change**: Plugin interface. Hook point (POST_PHASE_5). Prediction categories (CONVERGE/STAGNATE/UNCERTAIN). Output format.

---

## 2. Technical Approach

### Kalman State Model

State vector per round: `[dispute_count, concession_rate, equilibrium_score]`

```
x_k = F * x_{k-1} + w    (process model: linear trend)
z_k = H * x_k + v         (observation: feature extraction output)
```

Where:
- `F` is the state transition matrix (trend extrapolation)
- `H` is the observation matrix (identity — we observe all state variables)
- `w ~ N(0, Q)` is process noise (models deliberation unpredictability)
- `v ~ N(0, R)` is observation noise (models extraction imprecision)

### Confidence Calibration

The Kalman filter's posterior covariance `P` provides natural confidence bounds:
- Confidence = 1 - trace(P) / trace(P_prior)
- As more rounds are observed, P shrinks and confidence increases
- With 1 round: high uncertainty, UNCERTAIN prediction
- With 3+ rounds: narrowed bounds, definitive prediction

### Fixed-Point Detection

Instead of extrapolating a linear trend to zero, the Kalman model detects when the state estimate for disputes has converged to a fixed point (innovation sequence drops below threshold). This is more robust than linear extrapolation for non-linear convergence patterns.

---

## 3. Functional Requirements

- **FR-001**: When `scipy` (or a minimal Kalman implementation) is available, the predictor MUST use the Kalman filter instead of linear OLS.
- **FR-002**: When `scipy` is not available, the predictor MUST fall back to the existing linear OLS path.
- **FR-003**: The Kalman filter MUST track `[dispute_count, concession_rate, equilibrium_score]` as a 3D state vector.
- **FR-004**: The Kalman filter MUST produce calibrated confidence intervals, not point confidence values.
- **FR-005**: Fixed-point detection MUST use the innovation sequence (prediction error), not trend extrapolation.
- **FR-006**: The `PluginResult.data` dict MUST include `method: "kalman"` (or `method: "ols"`) and confidence bounds.
- **FR-007**: Process noise `Q` and observation noise `R` MUST be configurable via plugin config.
- **FR-008**: Cost estimation (FR-008 from spec 018) MUST use the Kalman model's predicted rounds remaining, not the linear estimate.

---

## 4. Success Criteria

- **SC-001**: Given a 3-round deliberation with decreasing disputes (5, 3, 1), the Kalman predictor gives higher confidence than the linear predictor.
- **SC-002**: Given a 2-round deliberation with identical dispute counts, the Kalman predictor correctly identifies stagnation with wider confidence bounds than 3+ rounds.
- **SC-003**: The Kalman filter correctly handles non-linear convergence (e.g., disputes: 10, 7, 5, 4, 4, 3 — diminishing returns pattern).
- **SC-004**: With scipy uninstalled, behavior is identical to the current linear OLS implementation.

---

## 5. Dependencies

- `scipy` — for `scipy.linalg` (matrix operations in Kalman update). Alternatively, a minimal pure-Python Kalman implementation (~50 lines) could avoid this dependency.
- Optional runtime dependency, not a package requirement.

---

## 6. Constraints

- Must NOT add scipy to core package requirements.
- Must NOT change the Plugin interface or prediction categories.
- Must NOT break the linear OLS fallback path.
- The Kalman filter must work with as few as 2 data points (rounds), producing high-uncertainty predictions.
