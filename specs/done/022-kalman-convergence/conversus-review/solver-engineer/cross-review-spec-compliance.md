# Cross-Review: solver-engineer reviews spec-compliance

**Reviewer**: solver-engineer
**Reviewing**: spec-compliance/review.md
**Phase**: 2 (cross-review)
**Date**: 2026-04-01

---

## Agreement

1. **FR-005 PARTIALLY MET is the correct call.** The spec-compliance reviewer correctly identifies that `detect_fixed_point()` uses state estimate deltas rather than the innovation sequence. The innovation vector is computed on line 289 of `kalman.py` but discarded. This is the most important compliance finding in the entire review. The state delta is a filtered (smoothed) quantity while the innovation is the raw prediction error -- they have different statistical properties and the spec is explicit about requiring the innovation.

2. **FR-007 PARTIALLY MET is correct.** Function layer supports Q/R; plugin config layer does not. The evidence is clear and the gap is well-scoped.

3. **All SC verdicts are accurate.** The test evidence cited for each SC is correct and sufficient. SC-002's relaxed assertion is noted appropriately.

4. **Constraints compliance is accurate.** All four constraints (no scipy, no interface change, no OLS breakage, 2-point minimum) are correctly verified.

5. **The observation that both point confidence and intervals are provided is astute.** The spec says "confidence intervals replace point estimates" but having both is better. This is a good example of exceeding the spec while maintaining backward compatibility.

## Disagreement

1. **FR-005 severity should be CRITICAL, not "Moderate."** The spec-compliance reviewer rates the FR-005 gap as "Moderate" severity. I disagree -- the spec uses the word "MUST" and explicitly contrasts the innovation sequence with trend extrapolation. The current implementation is closer to trend comparison (comparing successive state estimates) than to innovation analysis. For a spec-compliance review, "MUST use X, not Y" where the implementation uses something closer to Y should be rated higher. The behavior may be "similar in practice" but spec compliance is about mechanism, not just outcome.

2. **The SC-002 relaxed assertion should be flagged more prominently.** The test uses `stag_width >= conv_width * 0.5` which means stagnation bounds could be *half* the width of convergence bounds and still pass. The spec says "wider confidence bounds" without qualification. The test should use `stag_width >= conv_width` (strictly wider) or the SC should be rated PARTIALLY MET. The current 0.5x threshold is too lenient.

3. **Missing: no assessment of the confidence calibration formula.** FR-004 is marked MET because confidence intervals exist, but the *calibration* part of "calibrated confidence intervals" is not assessed. The formula `1 - trace(P_final) / trace(P_initial)` depends on the arbitrary initialization P, which means the confidence value is not properly calibrated against the data. The intervals themselves (from `P[0][0]`) are well-calibrated under the Gaussian assumption, but the point confidence is not. FR-004 may still be MET (the intervals are the primary requirement), but the calibration quality deserves discussion.

## Observations the spec-compliance reviewer missed

1. **No assessment of spec section 6 constraints in FR context.** Section 6 lists: "The Kalman filter must work with as few as 2 data points (rounds), producing high-uncertainty predictions." The constraint is verified as MET, but there is no test that explicitly checks *high uncertainty* with exactly 2 points. The `identical_disputes_history` fixture has 2 rounds but tests classification, not uncertainty magnitude.

2. **FR-001 interpretation is generous.** The spec says "when scipy (or a minimal Kalman implementation) is available." The implementation always has the minimal Kalman implementation available (it is built-in, not optional). So the condition "when available" is always true, meaning the predictor should *always* use Kalman unless there is a deliberate OLS override. The "auto" mode falls back to OLS with < 2 rounds, which could be argued as an FR-001 gap for the 1-round case. The spec-compliance review does not raise this.

3. **No cross-reference to FR-008 from spec 018.** FR-008 in spec 022 references "FR-008 from spec 018." The spec-compliance review does not verify that the cost estimation in `_build_recommendation()` is consistent with what spec 018's FR-008 requires.

## Net assessment

The spec-compliance review is the most rigorous of the three Phase 1 reviews. The FR-by-FR structure with evidence citations is exactly what a compliance review should be. The two PARTIALLY MET findings are accurate. The main gaps are the soft severity on FR-005, the lenient SC-002 test assertion, and the missing calibration assessment under FR-004. The recommendations are actionable and correctly prioritized.
