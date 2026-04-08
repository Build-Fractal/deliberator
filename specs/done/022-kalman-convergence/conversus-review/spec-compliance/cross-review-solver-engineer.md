# Cross-Review: spec-compliance reviews solver-engineer

**Reviewer**: spec-compliance
**Reviewing**: solver-engineer/review.md
**Phase**: 2 (cross-review)
**Date**: 2026-04-01

---

## Agreement

1. **Confidence calibration flaw (M1) is the most impactful finding.** The solver-engineer's analysis is mathematically precise. The formula `1 - trace(P_final) / trace(P_initial)` makes confidence a function of the arbitrary `initial_P` rather than the data. This directly affects FR-004 compliance because the spec says "calibrated confidence intervals" -- if the confidence metric driving the classification is poorly calibrated, the intervals may be correctly sized but the prediction outcome (converge/stagnate/uncertain) is unreliable. I should have flagged this under FR-004 in my review.

2. **Innovation sequence vs. state deltas (M2) aligns with my FR-005 finding.** The solver-engineer provides the mathematical justification for why these are different: the innovation has known statistical properties (white noise under correct model) while the state delta is a filtered quantity. This strengthens the case for FR-005 PARTIALLY MET.

3. **Observation validation (M5) is a valid operational concern.** From a spec-compliance perspective, the spec does not explicitly require input validation, but it is implied by the constraint "must work with as few as 2 data points" -- "work" implies not crashing on reasonable inputs.

4. **The suggestion to add a `KalmanTrace` dataclass (recommendation 7) directly enables FR-005 compliance.** If innovation vectors are stored per-step, `detect_fixed_point()` can be rewritten to check innovation magnitudes, closing the FR-005 gap.

## Disagreement

1. **F=I is not an off-base assumption in the spec compliance context.** The spec says `F` is "the state transition matrix (trend extrapolation)" and the code docstring says "process model: linear trend extrapolation." The implementation then uses F=identity, which is not trend extrapolation -- it is a random walk. However, the spec also says F is defaulted and configurable. Since F=I is the default and the function accepts a custom F, this is within spec. The solver-engineer's concern is about modeling quality, not spec compliance.

2. **The priority ordering puts `initial_P` configurability too high.** The solver-engineer lists this as P2 (high priority). From a spec compliance perspective, `initial_P` is not mentioned in any FR or SC. Configurability of Q and R is required (FR-007); configurability of initial_P is not. This is a nice-to-have, not a compliance gap.

3. **Joseph form (recommendation 4) is a numerical best practice, not a spec requirement.** The spec does not mention numerical stability requirements. For 3x3 matrices with the scales involved, the standard form is adequate. The solver-engineer rates this P2; it should be P3 or P4 from a compliance perspective.

## Observations the solver-engineer missed

1. **No FR-by-FR compliance assessment.** The solver-engineer review is structured around mathematical correctness and engineering quality, not spec compliance. It does not systematically evaluate FR-001 through FR-008 or SC-001 through SC-004. The confidence calibration finding (M1) affects FR-004 compliance and the innovation finding (M2) affects FR-005, but these are not framed as compliance gaps.

2. **No mention of FR-007 plugin config gap.** The solver-engineer focuses on the Kalman math and does not assess whether Q/R configurability reaches the plugin config layer. The `predict_convergence()` function accepts Q/R as parameters, which the solver-engineer sees, but the missing plugin wiring is not noted.

3. **No mention of FR-006 (method field in output).** The solver-engineer does not verify that `PluginResult.data` includes `method: "kalman"` or `method: "ols"`. This is a spec requirement that the implementation satisfies, but the review does not assess it.

4. **No test coverage assessment.** The solver-engineer mentions the test suite exists but does not assess what is tested, what is missing, or whether the test assertions match the spec requirements. The property test recommendation (9) is about matrix operations, not about spec compliance testing.

## Net assessment

The solver-engineer review is the deepest technical analysis of the Kalman filter mechanics. The confidence calibration finding (M1) is the single most important issue across all three reviews and directly affects the reliability of prediction classification. The innovation vs. state delta finding (M2) is correctly identified and mathematically justified. However, the review does not frame findings in spec compliance terms, misses integration-layer gaps, and over-prioritizes numerical best practices that are not spec requirements. The recommendations are technically sound but the priority ordering should be adjusted for compliance context.
