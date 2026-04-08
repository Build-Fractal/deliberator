# Phase 3 Revision: spec-compliance

**Agent**: spec-compliance
**Spec**: 022-kalman-convergence
**Date**: 2026-04-01
**Inputs**: statistician cross-review, plugin-engineer cross-review

---

## Disposition of Original Recommendations

### P1-1. Amend spec to remove scipy gating language -- MAINTAINED

**Original**: Replace "When scipy is available" with "When 2+ rounds of history are available."

**Cross-review support**: All three agents agree the spec should be amended to reflect the pure Python approach.

**Priority**: Remains P1.

---

### P2-1. Add comparative test for SC-003 -- MODIFIED

**Original**: Verify Kalman outperforms OLS on diminishing-returns pattern.

**Cross-review response**: plugin-engineer argues SC-003 says "correctly handles" not "better than OLS." statistician provides a mathematical argument for Kalman superiority but agrees a test would help.

**Revised position**: I accept plugin-engineer's reading of SC-003 as "correctly handles." The current test (prediction = "converge") satisfies this. However, the comparative advantage is a valuable property that should be tested separately.

**Revised recommendation**: Mark SC-003 as MET (current test is sufficient for the criterion). Add a separate non-SC test that verifies Kalman produces tighter confidence bounds than OLS for the diminishing-returns pattern.

**Priority**: Downgraded to P3 (the existing test is sufficient for SC-003).

---

### P2-2. Verify constraints -- MAINTAINED

**Original**: Explicitly verify all 4 constraints from Section 6.

All constraints verified:
- No scipy dependency: MET (pure Python).
- No Plugin interface change: MET.
- No OLS breakage: MET.
- Works with 2 data points: MET (filter initializes + 1 update).

**Priority**: Remains P2 (for completeness of the compliance record).

---

## Revised Compliance Matrix

| Requirement | Original | Revised | Note |
|------------|----------|---------|------|
| FR-001 | PARTIALLY MET | PARTIALLY MET (spec amendment) | Amend spec to remove scipy language |
| FR-002 | MET | MET | No change |
| FR-003 | MET | MET | No change |
| FR-004 | MET | MET | No change |
| FR-005 | MET | MET | Threshold semantics noted but not a gap |
| FR-006 | MET | MET | No change |
| FR-007 | MET | MET | No change |
| FR-008 | MET | MET | No change |
| SC-001 | MET | MET | No change |
| SC-002 | MET | MET | No change |
| SC-003 | PARTIALLY MET | MET | Test verifies correct handling |
| SC-004 | MET | MET | No change |
| Constraints | MET | MET | All 4 verified |

---

## New Recommendations from Cross-Reviews

### N-1. Document initial covariance design choice (from statistician P1-1)

All agents agree the initial `diag(10, 1, 1)` makes confidence dispute-dominated. This should be documented in the `run_kalman_filter()` docstring.

**Priority**: P1 (adopted from statistician).

### N-2. Document observation noise semantics (from statistician revised P2-2)

R[0][0] = 0.5 for dispute counts is conservative. Document that this makes the filter trust the process model over observations, producing smoother but less reactive estimates.

**Priority**: P2.

### N-3. Test classification edge cases (from plugin-engineer N-1)

Add tests for boundary values: dispute_est near 1.0, dispute_delta near 0.0, confidence near min_confidence threshold.

**Priority**: P2.
