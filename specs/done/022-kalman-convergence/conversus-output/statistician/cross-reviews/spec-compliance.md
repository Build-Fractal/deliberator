# statistician Cross-Review of spec-compliance

**Cross-reviewer**: statistician
**Reviewing**: spec-compliance Phase 1 review of spec 022
**Date**: 2026-04-01

---

## Agreements

### 1. FR-001 PARTIALLY MET classification is correct

spec-compliance's nuanced analysis is right: the pure Python Kalman filter satisfies the spec's intent but not its mechanism. The spec describes a dependency-gated pattern (like specs 021 and 023), but the implementation chose a strictly better approach (no dependency). The spec should be amended. I agree with spec-compliance's recommended wording: "When 2+ rounds of history are available."

### 2. SC-004 is trivially met

Since there is no scipy dependency to uninstall, the fallback criterion is automatically satisfied. The pure Python approach collapses SC-004 into a tautology. This is fine -- the spec was written before the implementation chose the zero-dependency path.

### 3. Constraint verification is complete

spec-compliance verifies all 4 constraints from Section 6. All MET. The 2-data-point constraint (Kalman with only 2 rounds) is correctly verified: the filter initializes from round 1 and updates from round 2, producing a posterior with reduced uncertainty.

---

## Tensions

### 1. FR-005 interpretation: innovation vs. state change

spec-compliance marks FR-005 as MET, noting that the implementation uses state change rather than raw innovation but these are "related." I have a more precise assessment.

The Kalman innovation is `y_k = z_k - H @ x_pred`. The state change is `x_post - x_prior`. These are related by the Kalman gain: `x_post - x_pred = K @ y`. So the state change equals K times the innovation.

For fixed-point detection, the spec says "innovation sequence drops below threshold." The implementation checks state change (which is K * innovation). When K is stable (which it is after a few updates), the state change and the innovation are proportional. So checking state change is equivalent to checking innovation (with a different effective threshold). This is MET in spirit but the threshold semantics differ: the implementation's threshold applies to the state change, not the innovation. If someone tunes the threshold based on expected innovation magnitudes, they will get different behavior than expected.

I would mark FR-005 as MET with a note about the threshold semantics.

### 2. SC-003 assessment depth

spec-compliance marks SC-003 as PARTIALLY MET because the comparative advantage over OLS is not tested. I have a stronger position: the Kalman filter demonstrably handles diminishing returns better than OLS because of the state tracking. OLS fits a line through all points -- for the sequence (10, 7, 5, 4, 4, 3), the OLS slope is approximately -1.4/round, predicting round 7 disputes at ~1.3. The Kalman filter tracks the slowing rate and would predict round 7 disputes at ~2.5 (reflecting the plateau at 4,4 before the drop to 3). The Kalman estimate is more conservative and more accurate for non-linear patterns.

However, this is a mathematical argument, not a test-verified finding. I agree that a comparative test would strengthen SC-003.

---

## Missed Opportunities

### 1. No assessment of confidence calibration quality

spec-compliance verifies that confidence intervals are produced (FR-004 MET) but does not assess whether they are well-calibrated. A calibrated 95% CI should contain the true value 95% of the time. With only 3-6 rounds of data, the Kalman posterior is heavily influenced by the prior, so the CI may be overconfident or underconfident depending on the initial covariance choice.

This is a statistical quality concern that spec-compliance is not positioned to assess (it is in my domain), but it would be useful for spec-compliance to flag it as a known limitation.

### 2. No assessment of the ConvergencePrediction classification logic

spec-compliance verifies the `method` field and the compliance of each FR, but does not review the classification logic in `_predict_convergence_kalman()`. The if/elif chain that maps Kalman state to prediction categories (converge/stagnate/uncertain) has subtle interactions with `fixed_point`, `dispute_delta`, `confidence`, and `min_confidence`. This logic determines the user-facing prediction and deserves scrutiny.

For example: if `dispute_delta == 0` and `fixed_point is True` and `dispute_est > 1.0`, the prediction is "stagnate" -- correct. But if `dispute_delta == 0` and `fixed_point is True` and `dispute_est <= 1.0`, the prediction is "converge" -- is this correct? A fixed point at dispute_est = 0.8 means the system has stabilized near zero disputes, which is convergence. But a fixed point at dispute_est = 0.99 is ambiguous.
