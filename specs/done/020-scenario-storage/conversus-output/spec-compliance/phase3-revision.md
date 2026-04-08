# Phase 3 Revision: spec-compliance

**Spec**: 020-scenario-storage
**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From storage-architect

1. **FR-002 PARTIALLY MET**: Accepted. Mode validation missing. `VALID_SCENARIO_MODES` defined but not enforced. Revised from MET.

2. **`exists()` not in protocol**: Valid finding. Not a compliance issue (the spec only requires save/load/list/append_run) but a design quality concern.

### From plugin-engineer

1. **RunRecord field divergence**: Confirmed. The spec's Section 2.3 and the RunRecord model have different fields. FR-007 is still MET (run appended) but the record structure is not spec-aligned.

2. **Missing error handling**: Critical for robustness. Not a compliance issue per se (no FR says "handle store errors") but violates the general principle of plugin graceful degradation.

---

## Updated Compliance Matrix

| Requirement | Phase 1 | Phase 3 | Change Reason |
|-------------|---------|---------|---------------|
| FR-001 | MET | MET | |
| FR-002 | MET | **PARTIALLY MET** | Mode validation missing |
| FR-003 | MET | MET | |
| FR-004 | NOT VERIFIED | NOT VERIFIED | CLI layer |
| FR-005 | NOT VERIFIED | NOT VERIFIED | CLI layer |
| FR-006 | MET | MET | |
| FR-007 | MET | MET | Record appended; field names differ |
| FR-008 | NOT VERIFIED | NOT VERIFIED | CLI layer |
| FR-009 | NOT VERIFIED | NOT VERIFIED | CLI layer |
| FR-010 | NOT VERIFIED | NOT VERIFIED | CLI layer |
| FR-011 | MET | MET | |
| FR-012 | NOT VERIFIED | NOT VERIFIED | CLI layer |
| FR-013 | NOT VERIFIED | NOT VERIFIED | CLI layer |
| FR-014 | MET | MET | |
| FR-015 | MET | MET | |
| FR-016 | MET | MET | |
| FR-017 | NOT IMPLEMENTED | NOT IMPLEMENTED | |
| FR-018 | N/A | N/A | |
| FR-019 | MET | MET | |
| SC-001 | MET | MET | |
| SC-002 | NOT VERIFIED | NOT VERIFIED | |
| SC-003 | NOT IMPLEMENTED | NOT IMPLEMENTED | |
| SC-004 | MET | MET | |
| SC-005 | MET | MET | |

### New Findings

- **RunRecord field divergence**: `termination_reason` vs spec's `outcome`, missing `agents_launched`.
- **Missing store error handling**: Plugin should wrap store operations.
- **`exists()` not in ScenarioStore protocol**: Plugin depends on it.
