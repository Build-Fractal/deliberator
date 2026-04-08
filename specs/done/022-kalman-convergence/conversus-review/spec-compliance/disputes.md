# Spec Compliance Disputes -- Spec 022 Kalman Convergence

**Reviewer**: spec-compliance
**Phase**: 4 (disputes)
**Date**: 2026-04-01

---

## Resolved Disagreements

1. **FR-005 severity**: Upgraded to Critical per solver-engineer's argument. All reviewers now agree. No dispute.
2. **SC-002 verdict**: Downgraded to PARTIALLY MET per plugin-engineer's argument about the relaxed test assertion. All reviewers now agree. No dispute.
3. **F=I model choice**: All reviewers agree this is appropriate for the domain. No compliance concern.

---

## Remaining Disputes

### Dispute 1: Whether FR-004 compliance note should be a downgrade

**My position**: FR-004 remains MET because the spec says "calibrated confidence intervals" and the Kalman-produced intervals from `P[0][0]` are properly calibrated under the Gaussian model. The poorly calibrated *point* confidence from `compute_kalman_confidence()` is a separate concern -- it is not what FR-004 asks for. I added a compliance note but did not downgrade to PARTIALLY MET.

**Solver-engineer's implicit position**: The confidence calibration flaw affects the prediction classification (converge/stagnate/uncertain), which degrades the overall feature quality even if the intervals themselves are correct.

**Plugin-engineer's implicit position**: The point confidence drives the `min_confidence` threshold, which is the primary user-facing classification mechanism. If the confidence is not calibrated, the classification is unreliable.

**My response**: The distinction matters for compliance tracking. FR-004 specifies "calibrated confidence intervals." The intervals are calibrated. The point confidence is a *derived* metric used internally for classification -- it is not mentioned in FR-004. The classification logic is not specified in any FR (the prediction categories are specified but the logic for choosing between them based on confidence is implementation detail). Therefore, the calibration flaw is a quality issue, not a compliance issue. I maintain FR-004 as MET with a compliance note.

**Recommended resolution**: FR-004 remains MET. The confidence calibration flaw is tracked as a P2 quality issue, not a compliance gap. The compliance note in the revised review provides the necessary visibility.

---

### Dispute 2: Whether FR-001 should account for the 1-round auto case

**My position (raised by solver-engineer cross-review)**: FR-001 says "When [a Kalman implementation] is available, the predictor MUST use the Kalman filter instead of linear OLS." The pure Python implementation is *always* available. Therefore, the predictor should *always* use Kalman unless deliberately overridden by `method="ols"`. The auto mode falling back to OLS with 1 round could be an FR-001 gap.

**Counter-argument**: The spec also says the filter "must work with as few as 2 data points" (section 6), implying 1 data point is insufficient. The auto mode's 2-round threshold is consistent with this constraint. Additionally, FR-002 says "when [Kalman] is not available, fall back to OLS" -- the "not available" condition can reasonably be interpreted as "not applicable" (insufficient data), not just "missing dependency."

**My response**: The FR-001/FR-002 language was written with scipy availability in mind (an import-time check). The implementation reinterprets "availability" as "applicability" (sufficient data). This is a reasonable interpretation that avoids producing noisy predictions with 1 data point. The spec's section 6 constraint ("2 data points minimum") supports this interpretation. I maintain FR-001 as MET.

**Recommended resolution**: FR-001 remains MET. Document the interpretation that "available" means "applicable with sufficient data" for the auto mode.

---

### Dispute 3: Priority ordering of the remediation backlog

**My position**: The remediation backlog should be ordered by compliance impact:
1. FR-005 innovation sequence (P1 -- "MUST" violation)
2. FR-007 Q/R plugin config (P1 -- "MUST" violation)
3. SC-002 test assertion (P1 -- success criteria not verified)
4. Confidence calibration (P2 -- quality, not compliance)
5. Equilibrium scores (P2 -- practical effectiveness)
6. Method validation (P2 -- configuration safety)

**Solver-engineer position**: Confidence calibration should be P1 because it affects prediction reliability.

**Plugin-engineer position**: Method validation should be P1 because it prevents silent misconfiguration.

**My response**: From a strict spec compliance perspective, only FR-005 and FR-007 use "MUST" language and are not met. Everything else is either a quality improvement or a test gap. I recommend a two-tier approach: compliance P1 (FR-005, FR-007, SC-002 test) and quality P1 (confidence calibration, method validation). Both tiers should ship in the same PR but the compliance tier should be reviewed first.

**Recommended resolution**: Two-tier P1: compliance tier (FR-005, FR-007, SC-002) and quality tier (confidence calibration, method validation). Both ship together.

---

## Consensus Items

All three reviewers agree on the following (no disputes):

1. FR-005 is PARTIALLY MET and requires innovation sequence implementation. (Critical)
2. FR-007 is PARTIALLY MET at the plugin config layer. (Critical)
3. SC-002 is PARTIALLY MET due to relaxed test assertion. (Critical)
4. Confidence calibration formula has initialization dependency. (High)
5. Equilibrium scores not wired. (High)
6. The implementation is architecturally sound with well-scoped remediation.
7. F=I is correct for this domain. The pure Python approach is superior to optional scipy.
8. The 2-round auto threshold is correct and spec-aligned.
