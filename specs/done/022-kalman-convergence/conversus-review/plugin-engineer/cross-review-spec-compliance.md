# Cross-Review: plugin-engineer reviews spec-compliance

**Reviewer**: plugin-engineer
**Reviewing**: spec-compliance/review.md
**Phase**: 2 (cross-review)
**Date**: 2026-04-01

---

## Agreement

1. **FR-005 PARTIALLY MET is correct and well-evidenced.** The spec-compliance reviewer provides the clearest analysis of why state estimate deltas are not the same as the innovation sequence. The evidence chain (line 289 computes innovation, line 381 checks state deltas) is precise. This is the most defensible finding in any of the three reviews.

2. **FR-007 PARTIALLY MET with the function-vs-plugin split is the right way to frame it.** The spec-compliance review correctly distinguishes between "function layer MET" and "plugin config layer NOT MET." This granularity helps prioritize the fix -- it is a wiring issue, not a design issue.

3. **FR-001 through FR-004, FR-006, FR-008 verdicts are all well-supported.** Each has specific code line references and test evidence. The methodology (code evidence + test evidence) is sound.

4. **Constraints compliance table is clean and accurate.** All four constraints verified with evidence.

5. **SC-001 through SC-004 all MET with test citations.** The test names are accurate and the test logic supports the verdicts.

## Disagreement

1. **SC-002 should be PARTIALLY MET, not MET.** The spec says "stagnation with wider confidence bounds than 3+ rounds." The test uses `stag_width >= conv_width * 0.5`, meaning stagnation bounds could be half the width of converging bounds and still pass. That is not "wider" -- it is "at least half as wide." The spec language is clear: "wider confidence bounds." If the test does not enforce this, the SC is not fully MET. The spec-compliance review notes the relaxed assertion but still gives a MET verdict, which is inconsistent.

2. **FR-004 MET is correct but the review undersells the calibration issue.** The spec says "calibrated confidence intervals." The intervals from `P[0][0]` are calibrated under the Gaussian assumption (the Kalman filter's native output). The point confidence from `compute_kalman_confidence()` is NOT calibrated (it depends on initialization). The spec-compliance review marks FR-004 MET and notes the dual output, but does not flag that the point confidence (which drives the `min_confidence` classification logic) is poorly calibrated. This matters because the prediction classification (converge/stagnate/uncertain) depends on `confidence >= min_confidence`, and the confidence value is initialization-dependent.

3. **Missing: the review does not assess whether the tests actually pass.** The spec-compliance review cites test names as evidence but does not verify whether the test assertions match the spec requirements precisely. For SC-002, the test assertion is weaker than the spec requirement. For SC-001, the test uses `>=` (greater than or equal) which technically allows equal confidence -- "higher confidence" in the spec implies strict inequality.

## Observations the spec-compliance reviewer missed

1. **The `convergence_method` config key naming is not specified in the spec.** The spec says "configurable via plugin config" for Q/R but does not specify config key names for the method selection. The implementation uses `convergence_method` which is reasonable but undocumented. A compliance review should note this as an implementation decision outside spec scope.

2. **No assessment of the spec's "What does not change" section.** The spec explicitly states: "Plugin interface. Hook point (POST_PHASE_5). Prediction categories. Output format." The constraints table covers interface and categories but does not explicitly verify that the hook point is still POST_PHASE_5 (it is -- line 181 of predictor.py) or that the output format is preserved (it is -- with additive fields only).

3. **No assessment of section 5 (Dependencies).** The spec says scipy is an "Optional runtime dependency, not a package requirement." The implementation has no scipy dependency at all (not even optional). This could be noted as exceeding the spec -- the implementation eliminated the dependency entirely rather than making it optional.

4. **The review does not assess FR naming consistency.** FR-008 in spec 022 references "FR-008 from spec 018" which creates a cross-spec dependency. The compliance review should verify that the two FR-008s are consistent and that the implementation satisfies both.

## Net assessment

The spec-compliance review is the most structured and evidence-based of the three. The FR-by-FR format with code line references and test citations is excellent. The two PARTIALLY MET findings are accurate and actionable. The main weakness is SC-002 being marked MET when the test assertion is weaker than the spec requirement, and the missing calibration analysis under FR-004. Recommendations are well-prioritized and the distinction between P1-P4 levels is clear.
