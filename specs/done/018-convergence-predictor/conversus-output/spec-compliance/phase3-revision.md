# Phase 3 Revision: spec-compliance

**Spec**: 018-convergence-predictor
**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From statistician

1. **FR-011 auto_stop**: statistician revised to PARTIALLY MET, aligning with my position. Consensus is PARTIALLY MET.

2. **FR-003 single-round confidence nuance**: statistician notes that 0.45 confidence for a "converge" prediction on zero-disputes single round may be generous. From a compliance standpoint, the spec says "Confidence is low (0.3-0.5 range)" for single round. The implementation's 0.30-0.45 is within range. MET maintained.

### From plugin-engineer

1. **FR-008 cost underestimate**: plugin-engineer and statistician both identify the 4x cost underestimate. I now revise FR-008 to PARTIALLY MET. The format is correct (includes estimated cost), but the number is materially inaccurate. The spec says the recommendation "MUST include estimated cost" -- the cost is included but wrong.

2. **FR-010 filename deviation**: Same pattern as spec 017. Noted but not a separate compliance issue since the base infrastructure handles naming.

---

## Updated Compliance Matrix

| Requirement | Phase 1 | Phase 3 | Change Reason |
|-------------|---------|---------|---------------|
| FR-001 | MET | MET | |
| FR-002 | MET | MET | |
| FR-003 | MET | MET | |
| FR-004 | PARTIALLY MET | PARTIALLY MET | OLS, not Kalman |
| FR-005 | MET | MET | |
| FR-006 | MET | MET | |
| FR-007 | MET | MET | |
| FR-008 | MET | **PARTIALLY MET** | Cost 4x underestimate |
| FR-009 | MET | MET | |
| FR-010 | MET | MET | Fields present; position_drift uninformative |
| FR-011 | PARTIALLY MET | PARTIALLY MET | auto_stop not consumed |
| FR-012 | MET | MET | |
| FR-013 | MET (by design) | MET (by design) | |
| SC-001 | MET | MET | |
| SC-002 | MET | MET | |
| SC-003 | MET | MET | |
| SC-004 | NOT VERIFIED | NOT VERIFIED | |
| SC-005 | MET | MET | |

### New Findings

- **Cost estimation underestimate**: `num_agents + 1` vs. actual D007 formula (4x difference for 3 agents).
- **position_drift always 0.0**: Field present but uninformative.
