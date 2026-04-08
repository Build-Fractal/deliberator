# Cross-Review: solver-engineer reviews plugin-engineer

**Reviewer**: solver-engineer
**Reviewing**: plugin-engineer/review.md
**Phase**: 2 (cross-review)
**Date**: 2026-04-01

---

## Agreement

1. **FR-007 gap is real and critical.** The plugin-engineer correctly identifies that Q/R are not wired from plugin config to `predict_convergence()`. This is a genuine compliance gap -- the function API supports it, the plugin layer does not. Fully agree this is P1.

2. **Equilibrium scores TODO is a real problem.** The third state variable (eq_score) being permanently 0.0 means 1/3 of the Kalman state vector carries no information. This is not just a TODO -- it degrades the filter's ability to produce meaningful multi-dimensional state estimates. The process noise Q adds uncertainty to this dimension every step with no corrective observations, which inflates the overall covariance trace and distorts confidence.

3. **Silent fallback concern is valid.** The OLS result from a failed Kalman path looks identical to an intentional OLS selection. Adding a `fallback_reason` or `fallback: true` flag would be operationally valuable.

4. **Method validation concern is valid.** An unrecognized method string silently resolving to OLS is a configuration footgun.

## Disagreement

1. **"auto" threshold of 2 is not arbitrary -- it is mathematically grounded.** The plugin-engineer calls the 2-round threshold "arbitrary" and suggests 3 might be better. With 2 observations and a 3x3 state, the filter is not "underdetermined" -- the Kalman filter is a recursive estimator, not a batch regression. It produces a valid posterior after each observation, with the covariance reflecting the remaining uncertainty. The filter is designed to work with 1+ observations. The auto threshold of 2 is the minimum for detecting a *trend* (you need 2 points to see a direction), which is the right threshold for convergence prediction.

2. **The Kalman path not using OLS trends is a feature, not a missed opportunity.** The plugin-engineer notes the two paths are "self-contained" and cannot be blended. This is correct architecture. Mixing OLS trends into the Kalman state would violate the information-theoretic basis of the Kalman filter (double-counting evidence). If an ensemble is desired, it should be a proper Bayesian model average, not an ad-hoc blend.

3. **The `_predict_convergence_kalman` branching is complex but necessary.** The 5-way branching reflects genuinely distinct prediction scenarios (fixed-point convergence, trending down, trending up, flat with fixed point, flat without). A lookup table would obscure the distinct reasoning strings and make the confidence-threshold logic harder to follow. Refactoring for readability is fine, but the current structure is not over-engineered.

## Observations the plugin-engineer missed

1. **The plugin-engineer does not discuss mathematical correctness of the Kalman filter itself.** The review focuses entirely on the integration layer. No assessment of whether the matrix operations are correct, whether the confidence calibration formula is sound, or whether the fixed-point detection mechanism matches the spec. This is expected given the "plugin-engineer" role but leaves a gap in overall coverage.

2. **No mention of numerical stability.** The plugin-engineer's scope is integration, but the filter's failure modes (singular S matrix, negative covariance) directly affect the plugin's reliability. The exception fallback path that the review discusses is triggered precisely by these numerical issues.

## Net assessment

The plugin-engineer review is thorough on integration concerns and correctly identifies the two most important compliance gaps (FR-007 plugin wiring, equilibrium scores). The "arbitrary threshold" and "self-contained paths" concerns are overstated but not harmful. The recommendations are actionable and well-prioritized.
