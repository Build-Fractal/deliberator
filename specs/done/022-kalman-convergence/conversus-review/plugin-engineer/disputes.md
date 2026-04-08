# Plugin Engineer Disputes -- Spec 022 Kalman Convergence

**Reviewer**: plugin-engineer
**Phase**: 4 (disputes)
**Date**: 2026-04-01

---

## Resolved Disagreements

1. **Auto threshold of 2**: Withdrawn. The threshold aligns with the spec's 2-point minimum requirement and the Kalman filter's recursive nature. No dispute.
2. **Kalman/OLS blending**: Withdrawn. Self-contained paths are correct architecture. An ensemble would require proper Bayesian model averaging, which is a separate feature.
3. **`_predict_convergence_kalman` refactoring**: Removed from recommendations. Code quality concern, not compliance or integration.

---

## Remaining Disputes

### Dispute 1: Granularity of the Kalman exception fallback

**My position**: When the Kalman path fails with an exception, the result should include `fallback_reason` in the output data to distinguish intentional OLS from fallback OLS.

**Solver-engineer's counter**: The fallback should be more granular -- catch singular matrix specifically inside `kalman_update()` and return the prior state, reserving OLS fallback for structural failures.

**My response**: Both positions are valid and not contradictory. The solver-engineer's suggestion (catch singular S in `kalman_update()`, return prior) prevents losing the entire Kalman state for one bad observation. My suggestion (add `fallback_reason` to output) addresses the *observability* of the fallback at the plugin layer. Both should be implemented:

1. Inner recovery: `kalman_update()` catches singular matrix, logs warning, returns prior.
2. Outer recovery: `predict_convergence()` catches structural failures, falls back to OLS.
3. Output observability: When outer fallback triggers, add `fallback_reason` to output data.

**Recommended resolution**: Implement both. Inner granular recovery + outer structural fallback + output observability.

---

### Dispute 2: Whether `fallback_reason` in output is sufficient or if `method` should indicate fallback

**My position**: Add a `fallback_reason: str | None` field to `PluginResult.data`. Keep `method: "ols"` when OLS is used (even as fallback).

**Potential counter** (not raised by other reviewers but anticipated): `method: "ols_fallback"` would be more discoverable than a separate field.

**My response**: Changing `method` to include fallback variants would break FR-006 compliance, which specifies `method: "kalman"` or `method: "ols"`. Adding `fallback_reason` as a new additive field maintains FR-006 compliance while providing the needed observability. Consumers that do not know about `fallback_reason` ignore it.

**Recommended resolution**: Additive `fallback_reason` field, not a new `method` variant.

---

### Dispute 3: Priority of equilibrium score wiring vs. confidence calibration fix

**My position**: Wire equilibrium scores first (P2), then fix confidence calibration.

**Solver-engineer position**: Couple them as a single work item: wire scores, then re-validate calibration with full 3D observations.

**My response**: I agree with coupling, but the ordering matters. The confidence calibration fix (changing the formula in `compute_kalman_confidence()`) can and should be done independently of the score wiring. The formula `1 - trace(P_final) / trace(P_initial)` is flawed regardless of whether eq_score is populated. Waiting to wire scores before fixing the formula delays a P1 fix behind a P2 dependency.

**Recommended resolution**: Fix confidence calibration formula independently (P1). Wire equilibrium scores (P2). Validate the combination after both are done.

---

## Consensus Items

All three reviewers agree on the following (no disputes):

1. FR-005 is PARTIALLY MET -- innovation vectors needed for fixed-point detection. (P1)
2. FR-007 plugin config wiring for Q/R is missing. (P1)
3. SC-002 is PARTIALLY MET -- test assertion too relaxed. (P1)
4. Confidence calibration formula is initialization-dependent. (P1)
5. Equilibrium scores not wired through. (P2)
6. Method validation for config values is needed. (P1)
7. The implementation is architecturally sound with well-scoped gaps.
