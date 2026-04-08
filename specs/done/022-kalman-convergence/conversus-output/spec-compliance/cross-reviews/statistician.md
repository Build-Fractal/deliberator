# spec-compliance Cross-Review of statistician

**Cross-reviewer**: spec-compliance
**Reviewing**: statistician Phase 1 review of spec 022
**Date**: 2026-04-01

---

## Agreements

### 1. Matrix operation correctness is thoroughly verified

statistician's 12-function verification table with analytic methods provides strong evidence of mathematical correctness. The cofactor-based inverse and the singularity threshold analysis are valuable details that complement the compliance review.

### 2. State model choice is well-justified

The 3D state vector `[dispute_count, concession_rate, equilibrium_score]` captures the key convergence signals. The F = I (identity transition) is the simplest valid model. statistician correctly notes that a trend-based F could improve predictions but adds complexity.

### 3. Confidence calibration via trace ratio is sound

The formula `1 - trace(P) / trace(P_initial)` is a standard Kalman confidence heuristic. The initial covariance bias concern (P1-1) is well-articulated and should be documented.

---

## Tensions

### 1. Covariance update form: simple vs. Joseph

statistician recommends the Joseph form (P2-1) for numerical stability. From a compliance perspective, neither form is specified in the spec. The spec says "Kalman filter" without specifying the update form. Both forms implement the correct Kalman update. The choice between them is an implementation quality concern, not a compliance concern.

I would classify this as a P3 (consider) rather than P2 (should fix) because the simple form produces correct results for the expected input range. If numerical issues are observed in practice, the Joseph form can be added as a bugfix without changing the spec.

### 2. Fixed-point threshold semantics

statistician's analysis that state change is K * innovation (and therefore proportional but not equal to the innovation) is mathematically precise. From a compliance perspective, FR-005 says "use the innovation sequence (prediction error), not trend extrapolation." The implementation uses state change, which is derived from the innovation via the Kalman gain. The spec's intent (avoid linear extrapolation) is satisfied. The spec's letter (use the innovation directly) is approximately satisfied.

I maintain FR-005 as MET because the alternative (checking raw innovation magnitude) would produce equivalent results (K is a monotonic transform) and the spec's purpose is to distinguish the Kalman approach from OLS extrapolation.

---

## Missed Opportunities

### 1. No verification of the default noise matrices against the spec

The spec (Section 2) states that Q models "deliberation unpredictability" and R models "extraction imprecision." statistician describes the defaults (`Q = diag(1.0, 0.01, 0.01)`, `R = diag(0.5, 0.005, 0.005)`) and notes the dispute dimension has higher noise. But statistician does not verify whether these specific values are reasonable for the stated interpretation.

For example: Q[0][0] = 1.0 means the process model expects dispute counts to fluctuate by ~1 standard deviation per round. For a deliberation with 5 disputes, this is a 20% fluctuation -- plausible. R[0][0] = 0.5 means the observation model expects ~0.7 standard deviation of extraction noise on dispute counts -- this seems high (dispute counts are integers extracted from structured output, so extraction noise should be near zero).

This domain-specific validation is in statistician's wheelhouse and would strengthen the review.

### 2. No assessment of the Kalman filter's asymptotic behavior

What happens after 10+ rounds? The covariance P converges to the steady-state solution of the discrete algebraic Riccati equation: `P_ss = Q` (when F = H = I). This means the confidence plateaus at `1 - trace(Q) / trace(P_initial) = 1 - 1.02/12 ~= 0.915`. After many rounds, the filter is approximately 91.5% confident. This is a useful property: confidence never reaches 1.0, reflecting irreducible process noise. But it also means confidence never exceeds ~0.92 even with perfect data. statistician should verify this is reasonable.
