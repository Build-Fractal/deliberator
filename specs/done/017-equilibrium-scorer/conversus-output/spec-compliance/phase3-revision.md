# Phase 3 Revision: spec-compliance

**Spec**: 017-equilibrium-scorer
**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From game-theorist

1. **FR-005 severity context**: game-theorist provides valuable context -- the heuristic payoff functions are actually more tailored to conversus than a generic `nashopt.check_equilibrium()` call would be. I accept this nuance but maintain FR-005 as NOT MET per the spec letter. The recommended fix (honestly report "heuristic" always, or actually delegate to nashopt) is sound.

2. **FR-008 MET argument**: game-theorist argues the filename format requirement is about including the round number, not the exact pattern. I remain at PARTIALLY MET. The spec says "MUST" with a specific format string. If the intent was flexible, the spec would say "MUST include the round number in the filename." However, I acknowledge this is a spec-quality issue as much as a code issue.

3. **FR-009 recommendation detail gap**: game-theorist notes the spec example mentions recommendation numbers, which are not available at the scorer's abstraction level. I upgrade FR-009 to "MET with noted gap" -- the requirement is met in substance (plain-language interpretation) but the implementation is less specific than the spec example.

4. **SC-003 evidence**: game-theorist suggests richer test data would strengthen the SC-003 claim. I agree the evidence is thin (two-value comparison), but the criterion says "meaningful score differentiation," and a 1.0 vs. 0.5 difference is meaningful. I maintain MET.

### From plugin-engineer

1. **FR-008 normative vs. intent**: plugin-engineer agrees with my PARTIALLY MET assessment for FR-008, reinforcing that the MUST language with a specific format is normative. I maintain my position.

2. **Undocumented gamma**: plugin-engineer raises the `gamma` config parameter not being in FR-010. This is not non-compliance (extra config is allowed), but it is undocumented behavior. I add this as a documentation finding.

---

## Updated Compliance Matrix

| Requirement | Phase 1 | Phase 3 | Change Reason |
|-------------|---------|---------|---------------|
| FR-001 | MET | MET | |
| FR-002 | MET | MET | |
| FR-003 | MET | MET (needs verification) | Direct features.json reading unclear |
| FR-004 | MET | MET | |
| FR-005 | NOT MET | NOT MET | Confirmed by all reviewers |
| FR-006 | MET | MET | |
| FR-007 | PARTIALLY MET | PARTIALLY MET | hook field value confirmed as issue |
| FR-008 | PARTIALLY MET | PARTIALLY MET | Maintained after debate |
| FR-009 | MET | MET (with noted gap) | Spec example more detailed than impl |
| FR-010 | MET | MET | |
| FR-011 | MET | MET | |
| FR-012 | MET | MET | |
| FR-013 | MET | MET | |
| SC-001 | MET | MET | |
| SC-002 | MET | MET | |
| SC-003 | MET | MET | Evidence thin but sufficient |
| SC-004 | NOT VERIFIED | NOT VERIFIED | |
| SC-005 | MET | MET | |

### New Findings

- **Undocumented `gamma` config**: Not in FR-010 spec but accepted by plugin. Documentation issue.
- **Red-Blue total_surface=0 asymmetry**: game-theorist/plugin-engineer identified edge case. Not a compliance issue (spec doesn't cover this case) but a correctness concern.
