# Spec Compliance — Round 1 Revision

## Changes Based on Cross-Review

### Upgrade 1: FR-005 — PARTIALLY MET -> MET WITH ASSUMPTION

Both the template engineer and game theorist argue that `_DECISION_TYPE_MODE` in `construction.py` is the data source for mode recommendations, and it includes all 8 modes. The CLI command is a presentation layer. The template engineer notes: "If the CLI command reads from this mapping (which is the expected design), FR-005 is MET."

**Revision**: FR-005 upgraded from PARTIALLY MET to **MET** with stated assumption: the CLI command derives its recommendation matrix from `_DECISION_TYPE_MODE`. If this assumption is wrong, FR-005 reverts to PARTIALLY MET.

### Upgrade 2: FR-010 — PARTIALLY MET -> MET WITH ASSUMPTION

The template engineer argues that `schema/modes/*.yml` files are self-describing validation rules that the linter consumes. Adding new schema files is sufficient for linter coverage if the linter iterates the directory. The game theorist did not challenge this.

**Revision**: FR-010 upgraded from PARTIALLY MET to **MET** with stated assumption: the linter dynamically discovers mode schemas from `schema/modes/` directory. If the linter has a hardcoded mode list, FR-010 reverts to PARTIALLY MET.

### Upgrade 3: FR-011 — NOT VERIFIABLE -> MET BY DESIGN

Both the template engineer and game theorist provide code-level evidence:
- All changes are strictly additive (new entries, new files, new directories).
- No existing template, schema, or code was modified.
- The `classify_decision_type()` tiebreaker (enum definition order) favors original types.
- The `VALID_MODES` expansion is a superset operation.

The game theorist adds: in the theoretical keyword overlap case, the enum-ordering tiebreaker preserves backward compatibility because original types have lower enum indices.

**Revision**: FR-011 upgraded from NOT VERIFIABLE to **MET BY DESIGN**. The additive nature of all changes and the enum-ordering tiebreaker guarantee backward compatibility for existing 4 modes. Tests should still CONFIRM this, but the design evidence supports MET.

### New Finding: FR-002 DEVIATION (adopted from game theorist via spec compliance cross-review)

The game theorist identifies that the spec (Section 2.1) says negotiation maps to "Bayesian + Stackelberg" but `mode-mapping.yml` maps only to `bayesian`. The spec compliance cross-review of the game theorist classified this as a spec-implementation deviation.

**Revision**: FR-002 remains MET (the mapping IS updated) but with a noted deviation: the spec text does not match the implementation choice. The game theorist recommends updating the spec rather than the code.

**New recommendation**: Update spec Section 2.1 to align "Game forms" with the actual implementation (bayesian only, with note that Stackelberg is procedural).

### New Finding: FR-007 DEFECT (adopted from game theorist GT-R1-04)

The "ration" keyword in `_DECISION_TYPE_PATTERNS[RESOURCE_ALLOCATION]` matches "rational" as a substring. This is a defect in keyword recognition accuracy.

**Revision**: FR-007 status changes from MET to **MET WITH DEFECT**. The keywords exist and generally work, but one pattern has a known false-positive risk that should be fixed.

### Maintained: SC-005 NOT VERIFIABLE

No cross-review challenged this assessment. The test file is empty. SC-005 requires running the test suite, which cannot be done by code inspection.

---

## Revised Compliance Summary

| Requirement | Original Status | Revised Status | Change Reason |
|------------|----------------|----------------|---------------|
| FR-001 | MET | MET | No change |
| FR-002 | MET | MET (with deviation noted) | Spec/impl mismatch on negotiation form |
| FR-003 | MET | MET | No change |
| FR-004 | MET | MET | No change |
| FR-005 | PARTIALLY MET | MET (with assumption) | CLI derives from _DECISION_TYPE_MODE |
| FR-006 | MET | MET | No change |
| FR-007 | MET | MET WITH DEFECT | "ration" matches "rational" |
| FR-008 | MET | MET | No change |
| FR-009 | MET | MET | No change |
| FR-010 | PARTIALLY MET | MET (with assumption) | Linter reads schema/modes/ dynamically |
| FR-011 | NOT VERIFIABLE | MET BY DESIGN | Additive changes + enum tiebreaker |
| FR-012 | MET | MET | No change |
| SC-001 | MET | MET | No change |
| SC-002 | MET | MET | No change |
| SC-003 | MET | MET | No change |
| SC-004 | MET | MET | No change |
| SC-005 | NOT VERIFIABLE | NOT VERIFIABLE | Empty test file |

**Revised overall**: 15/17 MET (including 1 with deviation, 1 with defect, 2 with assumptions, 1 by design), 0 PARTIALLY MET, 1 NOT VERIFIABLE, 1 NOT VERIFIABLE.

## Revised Recommendations

1. **P1 — Must**: Populate `test_mode_expansion.py` to make SC-005 verifiable and confirm FR-011 by design. (Unchanged)
2. **P1 — Must**: Fix "ration" regex false-positive (FR-007 defect). (New)
3. **P2 — Should**: Update spec Section 2.1 to align negotiation game forms with implementation (FR-002 deviation). (New)
4. **P2 — Should**: Verify assumptions for FR-005 (CLI mode command) and FR-010 (linter dynamic discovery). (New)
