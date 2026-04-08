# Phase 1 Review: statistician

**Spec**: 022-kalman-convergence
**Reviewer**: statistician
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: Mathematical correctness of Kalman filter, pure Python 3x3 matrix ops, confidence calibration

---

## Executive Summary

The Kalman filter implementation is mathematically correct. The predict-update cycle implements the standard linear Kalman filter equations faithfully. The pure Python 3x3 matrix operations are correct (verified against analytic results for identity, diagonal, and general invertible matrices). Confidence calibration via covariance trace ratio is a sound heuristic. Fixed-point detection via innovation magnitude is more robust than linear extrapolation for non-linear convergence. However, there are three concerns: (1) the confidence formula uses initial trace as denominator, but the initial state's covariance is set to a hardcoded `diag(10, 1, 1)` which creates a scale bias favoring the dispute dimension, (2) the covariance update uses the basic form `P = (I - KH)P_pred` which is numerically less stable than the Joseph form, and (3) the process noise Q and observation noise R defaults embed assumptions about deliberation dynamics that are not validated.

---

## 3x3 Matrix Operations

### Correctness Verification

All 12 matrix helper functions are correct:

| Function | Verification Method | Result |
|----------|-------------------|--------|
| `_eye3()` | Direct inspection | Correct |
| `_zeros3()` | Direct inspection | Correct |
| `_mat_add()` | A + A = 2A for identity | Correct |
| `_mat_sub()` | A - A = 0 for identity | Correct |
| `_mat_mul()` | A @ I = A; diagonal multiplication | Correct |
| `_mat_transpose()` | Symmetric matrix invariant | Correct |
| `_mat_scale()` | 2 * I = diag(2,2,2) | Correct |
| `_mat_trace()` | tr(diag(a,b,c)) = a+b+c | Correct |
| `_mat_det()` | det(I) = 1; det(diag) = product; det(singular) = 0 | Correct |
| `_mat_inverse()` | A @ A^{-1} = I roundtrip; singular raises ValueError | Correct |
| `_mat_vec_mul()` | diag(a,b,c) @ [x,y,z] = [ax,by,cz] | Correct |
| `_vec_sub()`, `_vec_norm()` | Direct computation | Correct |

The cofactor-based inverse formula (adjugate / determinant) is the standard closed-form for 3x3. The singularity check (`abs(det) < 1e-12`) is appropriate for the expected magnitude range of covariance matrices in this application.

### Design Decision: Pure Python vs. numpy

The choice to use pure Python for 3x3 operations is sound. The matrices are always exactly 3x3, so the O(n^3) matrix multiply is O(27) -- constant time. numpy overhead for array creation, dispatch, and memory allocation would dominate for matrices this small. The pure Python path also eliminates the numpy dependency, keeping the convergence predictor zero-dependency.

---

## Kalman Filter Core

### State Model

The state vector `[dispute_count, concession_rate, equilibrium_score]` is well-chosen. These three dimensions capture the key convergence signals:
- `dispute_count`: the primary convergence indicator (approaching zero = converging).
- `concession_rate`: the behavioral signal (agents yielding = cooperation).
- `equilibrium_score`: the game-theoretic signal (system approaching Nash equilibrium).

The transition matrix F = I (identity) models the assumption that the state persists between rounds with process noise. This is the simplest valid choice. A more sophisticated model could use F with a trend component (e.g., F[0][0] slightly < 1.0 to model expected dispute decay), but the identity model is correct as a baseline.

### Predict Step

The predict equations are correct:
- `x_pred = F @ x` (state extrapolation)
- `P_pred = F @ P @ F^T + Q` (covariance growth)

With F = I, these simplify to `x_pred = x` and `P_pred = P + Q`. The code correctly handles the general case (non-identity F is supported via parameter).

### Update Step

The update equations are correct:
- Innovation: `y = z - H @ x_pred` (prediction error)
- Innovation covariance: `S = H @ P_pred @ H^T + R`
- Kalman gain: `K = P_pred @ H^T @ S^{-1}`
- State update: `x_post = x_pred + K @ y`
- Covariance update: `P_post = (I - KH) @ P_pred`

With H = I (we observe all state variables), these simplify correctly.

### Concern: Covariance Update Stability

The implementation uses the "simple" form: `P = (I - KH) @ P_pred`. This is mathematically equivalent to the Joseph form `P = (I - KH) @ P_pred @ (I - KH)^T + K @ R @ K^T` but is numerically less stable. For well-conditioned matrices (which is the case for 3x3 diagonal-dominant covariances), the simple form is adequate. However, if Q or R are poorly chosen (very small or very large), the simple form can produce a non-positive-semidefinite P, which would break subsequent updates.

Given the 3x3 size and the expected range of noise parameters, this is a theoretical concern, not a practical one. But the Joseph form is easy to implement (same computational cost for 3x3) and eliminates the risk.

---

## Confidence Calibration

### Formula

```python
confidence = 1.0 - trace(P_posterior) / trace(P_initial)
```

This measures how much the covariance has shrunk relative to the initial uncertainty. The spec says: "Confidence = 1 - trace(P) / trace(P_prior)" where P_prior refers to the initial prior, not the per-step prior.

### Concern: Initial Covariance Bias

The initial covariance is `diag(10, 1, 1)`, which gives trace = 12. The dispute dimension contributes 10/12 = 83% of the trace. This means confidence is dominated by the dispute dimension's uncertainty reduction. If disputes converge quickly but concession rate and equilibrium score remain noisy, confidence will still be high. Conversely, if concession rate and equilibrium score converge but disputes remain uncertain, confidence will be low.

This is arguably correct behavior (disputes are the primary convergence indicator), but it should be documented as a design choice, not an accident.

### Confidence Bounds

The confidence interval on dispute count uses `P[0][0]` (dispute variance) with a 1.96-sigma multiplier (95% CI). This is a standard Gaussian confidence interval on the Kalman posterior. The formula is correct. The `max(0.0, P[0][0])` guard prevents negative variance from numerical issues.

---

## Fixed-Point Detection

The implementation checks `abs(states[-1].x[0] - states[-2].x[0]) < threshold`. This is the innovation in the dispute dimension only. The spec says "innovation sequence drops below threshold" -- the implementation simplifies from a 3D innovation to a 1D dispute-change check.

This simplification is acceptable because the dispute count is the primary convergence indicator. However, a system where disputes are stable but concession rate is still changing would be falsely classified as a fixed point. For the use case (deciding whether another round is useful), dispute stability is the right criterion.

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Document the initial covariance bias. The `diag(10, 1, 1)` initial P makes confidence dispute-dominated. This is a deliberate design choice and should be documented.

### P2 (Should Fix)

2. **P2-1**: Consider the Joseph form for covariance update. It is the same computational cost and eliminates numerical instability risk.

3. **P2-2**: Validate that the default Q and R values produce reasonable results across a range of deliberation patterns (e.g., fast convergence, slow convergence, stagnation, divergence).

### P3 (Consider)

4. **P3-1**: The fixed-point detection threshold (default 0.1) is a tuning parameter that may need adjustment. Consider making it configurable via the predictor plugin config.
