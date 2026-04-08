# Solver Engineer Disputes -- Spec 022 Kalman Convergence

**Reviewer**: solver-engineer
**Phase**: 4 (disputes)
**Date**: 2026-04-01

---

## Resolved Disagreements

The following disagreements from Phase 2 have been resolved through cross-review:

1. **F=I model choice**: Withdrawn. Random walk is appropriate for deliberation systems. No dispute.
2. **`initial_P` configurability priority**: Downgraded to P3. Agree it is not a compliance requirement.
3. **Joseph form priority**: Downgraded to P4. Agree it is not required at this scale.

---

## Remaining Disputes

### Dispute 1: Severity of the singular matrix handling

**My position**: The `ValueError` raised by `_mat_inverse()` when `S` is singular is a legitimate safety net, but returning the prior state unchanged (recommendation 9 in my revised review) would be more resilient.

**Plugin-engineer's counter**: "Returning the prior unchanged would silently ignore the observation, which is arguably worse than failing loudly."

**My response**: The plugin-engineer makes a fair point about silent data loss. However, the current behavior is also not ideal: the exception propagates to `predict_convergence()` which catches it and falls back to OLS, losing *all* Kalman state -- not just one observation. A better middle ground: catch the singular matrix specifically in `kalman_update()`, log a warning with the observation that caused it, and return the prior state. This preserves the Kalman state history (the prior states from previous rounds are still valid) while skipping the problematic observation. The OLS fallback should be reserved for structural failures, not one bad observation.

**Recommended resolution**: Catch `ValueError` from `_mat_inverse()` inside `kalman_update()`, log the observation, return the prior state. This is more granular than the current all-or-nothing fallback.

---

### Dispute 2: Whether the eq_score dimension concern is a calibration issue or an integration issue

**My position (revised)**: The equilibrium score dimension being always 0.0 is both a calibration issue (inflates covariance trace, distorts confidence) and an integration issue (TODO not resolved).

**Spec-compliance position**: This is primarily an FR-003 concern -- the spec says "MUST track equilibrium_score" and tracking a zero-valued dimension is technically compliant but practically useless.

**Plugin-engineer position**: This is primarily an integration concern (scores not wired through).

**My response**: All three framings are correct but the remediation is singular: wire the scores through. The calibration distortion is a *symptom* of the missing integration, not a separate problem. The confidence calibration fix (recommendation 1) will not fully resolve the issue if 1/3 of the state vector has no observations. Both fixes are needed. I recommend coupling these into a single P1/P2 work item: "Wire equilibrium scores AND re-evaluate confidence calibration with full 3D observations."

**Recommended resolution**: Treat as a coupled work item. Wire scores first (integration fix), then validate that confidence calibration works correctly with all three dimensions populated.

---

### Dispute 3: Whether SC-002 is PARTIALLY MET or MET

**My position**: SC-002 should be PARTIALLY MET. The spec-compliance reviewer revised to PARTIALLY MET after the plugin-engineer's cross-review.

**No remaining dispute**: All three reviewers now agree SC-002 is PARTIALLY MET due to the relaxed test assertion. The test should assert `stag_width >= conv_width` for full compliance.

---

## Consensus Items

All three reviewers agree on the following (no disputes):

1. FR-005 is PARTIALLY MET and requires storing innovation vectors. (Critical priority)
2. FR-007 plugin config wiring for Q/R is missing. (Critical priority)
3. Confidence calibration (`compute_kalman_confidence`) depends on arbitrary initialization. (High priority)
4. Equilibrium scores are not wired through. (High priority)
5. Method validation for `convergence_method` config is needed. (High priority)
6. The implementation is a solid v1 with clear, scoped remediation paths.
