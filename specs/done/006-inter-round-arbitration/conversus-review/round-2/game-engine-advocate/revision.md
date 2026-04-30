# Revision -- game-engine-advocate (Round 2)

## Recommendation Dispositions

### Rec 1: Specify provisional-resolution marker lifecycle (P2)
**Disposition: Maintain at P2. Lifecycle design is settled.**
Three-agent convergence on the lifecycle: markers are round-scoped, re-opened disputes return to DISPUTES_BEGIN/DISPUTES_END, PROVISIONALLY_RESOLVED markers exist only for disputes that remain provisionally resolved in the current round. functional-typing and integration-architect both endorse this design. integration-architect adds a Principle II observation: mark the markers as unstable until one spec has consumed them. Accepted.

### Rec 2: Ensure influence_headings YAML is plugin-extensible (P1-design)
**Disposition: Maintain. Reclassify as design constraint within P1 item 1, not a separate recommendation.**
integration-architect's cross-review correctly notes that "P1-design" is not a standard priority tier. This is a design constraint on the existing P1 influence_headings item, not a new P1 recommendation. The substance is settled: `dict[str, list[str]]` with string keys. All three agents converge.

### Rec 3: Formalize template last-mile audit (P2)
**Disposition: Maintain at P2, with scope clarification.**
Cross-reviews from functional-typing and integration-architect both note the need to separate the immediate action (document the manual audit practice) from the future enhancement (linter --audit mode). integration-architect raises a valid concern about false positives for variables provisioned for future specs. Agreed: the audit should be advisory, not blocking. Clarifying scope: the spec 006 action is documenting the manual practice; the automated check is a future spec.

### Rec 4: Document stagnation-influence interaction (P3)
**Disposition: Maintain at P3.**
Integration-architect confirms this overlaps with Round 1 P3 item 16. No priority change needed.

### Rec 5: Maintain game engine structural compatibility (confirmation)
**Disposition: Maintain as confirmation.**
No new concerns. The P1 implementation preserves extensibility.

## New Recommendations

### NEW-1: Confirm no objection to Phase enum items (Priority: P2)
**Source: Cross-reviews from functional-typing and integration-architect noting gap.**
Both co-reviewers note that game-engine-advocate did not address P2 items 4, 5, and 12 (Phase enum in validate.py, VariableDefinition.phases typing, match/case). These have functional-typing + integration-architect consensus from Round 1. game-engine-advocate confirms: no objection to any of these items. The Phase enum is a closed behavioral choice (Constitution Principle IX). Plugin phases would be handled by the factory extension pattern, not by bypassing the enum. The match/case default branch correctly handles future plugin phases.

### NEW-2: Endorse P2 sub-ordering (Priority: P2-meta)
**Source: integration-architect Round 2 Rec 4, noted as gap in cross-reviews.**
integration-architect's P2-easy / P2-structural distinction is pragmatic and correct. game-engine-advocate endorses the categorization:
- P2-easy: items 8, 10, 9, 11, 6 (documentation and path fixes)
- P2-structural: items 4, 5, 7, 12 (type system and markers)

The provisional markers (item 7) are in P2-structural because they introduce a new stable interface. This is the right placement.

## Position Summary

After cross-reviews, the game-engine-advocate position has narrowed further:

1. **Provisional-resolution marker lifecycle settled**: Three-agent convergence on round-scoped markers with re-opened disputes moving back to DISPUTES_BEGIN/DISPUTES_END. The stability recommendation (mark as unstable until validated) is accepted.

2. **influence_headings field type settled**: Reclassified from "P1-design" to "design constraint within P1 item 1." The string-keyed `dict[str, list[str]]` type is unanimous.

3. **Gaps filled**: Confirmed no objection to Phase enum items (NEW-1). Endorsed P2 sub-ordering (NEW-2). The game-engine-advocate's Round 2 review did not address these, and cross-reviewers correctly flagged the omission.

4. **Template last-mile audit scoped**: Immediate action is manual practice documentation; automated linter check is a future spec. The audit should be advisory (not blocking) to handle variables provisioned for future specs.

The game-engine-advocate's core finding from Round 1 remains: spec 006 makes no decisions requiring game engine rework. Round 2 refinements are about implementation precision and filling coverage gaps in the game-engine-advocate's review.
