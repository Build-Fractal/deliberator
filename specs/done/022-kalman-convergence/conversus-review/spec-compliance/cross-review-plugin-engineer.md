# Cross-Review: spec-compliance reviews plugin-engineer

**Reviewer**: spec-compliance
**Reviewing**: plugin-engineer/review.md
**Phase**: 2 (cross-review)
**Date**: 2026-04-01

---

## Agreement

1. **FR-007 plugin config gap (M1) is correctly identified and is the most actionable finding.** The plugin-engineer provides the exact code location (predictor.py line 253) where Q/R should be read from config. This aligns with my FR-007 PARTIALLY MET finding and provides the clearest remediation path.

2. **Equilibrium scores TODO (M2) is a real integration gap.** The third state dimension carrying no information degrades the filter's effectiveness. From a compliance perspective, FR-003 says the filter "MUST track" equilibrium_score -- tracking a dimension that is always 0.0 is technically tracking it but practically useless. The spec assumes equilibrium scores will be available (it lists spec 021 as a dependency).

3. **Method validation (M3) is a legitimate concern.** An unrecognized method string silently resolving to OLS is a configuration safety issue. From a compliance perspective, FR-001 and FR-002 only specify the Kalman and OLS paths, so an unknown method is undefined behavior.

4. **Silent fallback concern (M4) is valid for operational visibility.** The method field saying "ols" when Kalman was attempted and failed is misleading. From a compliance perspective, FR-006 requires `method: "kalman"` or `method: "ols"` -- but a fallback scenario is neither intentional Kalman nor intentional OLS. Adding a `fallback_reason` field would not violate FR-006 (additive field) while improving observability.

5. **The type alias recommendation (10) is a good code quality suggestion.** A single `ConvergenceMethod` type used across modules would prevent drift between the plugin config validation and the function signature.

## Disagreement

1. **The "auto" threshold being "arbitrary" is overstated.** The plugin-engineer suggests 3 rounds might be better than 2. From a spec compliance perspective, the spec says "the Kalman filter must work with as few as 2 data points" and the auto mode activates at 2. This is *exactly* what the spec requires. Raising the threshold to 3 would mean the auto mode does not use Kalman at the spec's stated minimum, which would be a compliance gap.

2. **The refactoring recommendation (9) for `_predict_convergence_kalman` is out of scope for a spec compliance review.** The function's branching complexity does not affect any FR or SC. Code readability is an engineering concern, not a compliance concern. The P4 priority is appropriate but the recommendation belongs in a code quality review, not a compliance context.

3. **The "ensemble" mode observation (O2) is forward-looking but not a gap.** The plugin-engineer notes the two paths cannot be blended. The spec does not require blending -- it specifies Kalman as the primary path and OLS as the fallback. The two paths being self-contained is a correct implementation of the spec's two-method architecture.

## Observations the plugin-engineer missed

1. **No FR-005 assessment.** The plugin-engineer does not evaluate whether fixed-point detection uses the innovation sequence as required. This is the most significant compliance gap in the implementation and the plugin-engineer's review does not mention it. The `detect_fixed_point()` function is called from the Kalman prediction path in `convergence.py`, which is part of the integration layer the plugin-engineer reviews.

2. **No assessment of FR-004 (confidence intervals vs. point estimates).** The plugin-engineer discusses confidence bounds in the output format context (FR-006) but does not evaluate whether the confidence intervals are "calibrated" as FR-004 requires. The solver-engineer's finding that the confidence metric depends on arbitrary initialization would strengthen the plugin-engineer's analysis.

3. **No assessment of whether the fallback path preserves SC-004.** SC-004 requires behavior "identical to the current linear OLS implementation" when scipy is unavailable. The plugin-engineer discusses the fallback but does not verify that the OLS output is byte-for-byte compatible with the pre-022 implementation. The spec-compliance review cites a specific test (`test_ols_behavior_unchanged`) for this.

4. **No mention of the `ConvergencePrediction` dataclass backward compatibility.** The plugin-engineer notes that `method` and `confidence_bounds` have defaults, but does not verify that existing consumers of `ConvergencePrediction` (if any) are not broken by the new fields. With `frozen=True` dataclass and keyword-with-default fields, this is safe, but it is worth verifying explicitly.

## Net assessment

The plugin-engineer review is strong on integration concerns (config passthrough, error handling, output format) and correctly identifies the FR-007 plugin wiring gap as the most actionable fix. The main gaps are the missing FR-005 and FR-004 assessments, which are partially explained by the plugin-engineer role being focused on integration rather than filter mechanics. The recommendations are practical and well-prioritized, with the P1 items (Q/R wiring, method validation) being clear, low-risk fixes. The "arbitrary threshold" concern should be reconsidered in light of the spec's explicit 2-round minimum requirement.
