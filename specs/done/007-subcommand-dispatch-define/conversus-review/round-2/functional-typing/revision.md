# Revision: functional-typing (Round 2, Iteration 1)

**Agent**: functional-typing
**Round**: 2 of 2
**Revision iteration**: 1
**Date**: 2026-03-22

---

## Recommendation Dispositions

### Rec #1: Reconcile heading count between Change 1 and Change 10

**Original**: If both post-write schema validation (Change 1) and `## Status` (Change 10) are adopted, validation must check for 8 headings. Listed 9 headings explicitly (including `# Problem Definition` and the 8 `##`-level headings).

**Cross-review feedback**:
- Integration-architect (DC-1) notes that Rec #1 and Rec #3 target different change items (Change 1 and Change 7) and could be adopted independently, risking inconsistency. Also observes that referencing "all required headings" without hardcoding a count avoids the coupling problem.
- Integration-architect (DC-2) challenges the placement of `## Status` between `# Problem Definition` and `## Decision`, arguing it breaks reading flow by inserting metadata before the anchoring decision statement. Proposes end-of-schema or frontmatter placement instead.
- Devils-advocate (DC-2) flags that FR coverage was claimed "unchanged from Round 1" despite accepting a new schema element, creating a logical inconsistency with MO-3's assertion that spec.md L45-71 must be updated.

**Disposition**: REVISED.

I accept three corrections:

1. **Heading count language**: Integration-architect is right that hardcoding "8" creates coupling between Rec #1 and Rec #3. The validation should reference "all required headings" and enumerate them in a single authoritative list. If `## Status` is later removed, the count updates in one place. I revise the recommendation to: "Post-write validation must confirm the presence of all headings defined in the schema block. If `## Status` is adopted, the schema block's heading list is the single source of truth for validation." This eliminates the 7-vs-8 fragility.

2. **Placement**: Integration-architect's DC-2 makes a compelling UX argument grounded in spec.md L87 (non-expert user principle). The non-expert opens `problem.md` and should see the decision statement first, not a machine status indicator. The `## Decision` heading at SKILL.md L827 is the anchoring content. I withdraw my condition 3 (placement between `# Problem Definition` and `## Decision`). The correct placement is after `## Source Documents` -- the last section in the current schema (SKILL.md L847). Status is a summary property of the whole document and belongs at the end, where a reader who has already absorbed the content encounters it. This is consistent with the arbiter's "factual annotation" framing: annotations describe the artifact, they do not precede the artifact's content.

3. **FR coverage consistency**: Devils-advocate's DC-2 is structurally correct. My FR coverage section claimed "unchanged from Round 1" while MO-3 simultaneously argued the normative schema must expand. These cannot both be true. The resolution: FR-009 (spec.md L38) lists required sections by name ("Decision, Type, Context, Constraints, Success Criteria, Open Questions, Source Documents"). `## Status` is not in that list. Adding `## Status` to SKILL.md does not change FR-009 coverage -- it is a non-FR enhancement to the schema. MO-3's recommendation to update spec.md L45-71 is better framed as updating the illustrative schema block to match the implementation, not as expanding the FR. I revise MO-3 to reflect this: the spec.md schema block should be updated for consistency, but FR-009 remains satisfied by the original 7 content sections.

**Atomicity**: I accept integration-architect's observation that Rec #1 and Rec #3 must be treated as an atomic unit if `## Status` is adopted. Both or neither; adopting Change 10 without updating the validation list and refine invariants produces internal contradictions. The revision text should state this dependency explicitly.

---

### Rec #2: Reaffirm all P1 changes from the synthesis

**Original**: Changes 1, 2, and 3 from the Round 1 synthesis are correct and should be adopted without modification (aside from heading count fix in Rec #1).

**Cross-review feedback**:
- Integration-architect (SA-2) confirms P1 changes are unanimous and unchanged. No contestation from any reviewer.
- Devils-advocate (SA-2, SA-3, SA-4) confirms all three P1 changes without modification.

**Disposition**: HELD. No revision needed. Changes 1, 2, and 3 remain unanimous P1 across all reviewers in both rounds. This is the most robust consensus position in the entire deliberation.

---

### Rec #3: Add `## Status` re-evaluation to refine invariants

**Original**: Change 7's four refine invariants should become five: (a) all required headings present, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated, (e) Status re-evaluated based on `[CLARIFY:]` tag count.

**Cross-review feedback**:
- Integration-architect (T-1) leans toward the mechanical formulation (status as pure function of tag count) but raises the behavioral question of whether refine re-evaluates previously resolved sections. Notes this is orthogonal to tag counting.
- Devils-advocate (T-2) accepts the logical necessity but identifies a tension with the "zero-cost" framing: a refine invariant is not zero-cost -- it adds a post-condition, test coverage, and edge case analysis. Also notes that "actively managed state" is a different category from "factual annotation computed once at write time."

**Disposition**: REVISED with refinement.

Devils-advocate's T-2 is the strongest challenge. The tension is real: I framed `## Status` as "zero-cost producer-side action" in my RD-1 concession, then proposed a fifth refine invariant that creates ongoing maintenance obligations. These are in tension. I resolve the tension by clarifying the cost model:

- The `## Status` field is zero-cost in the sense that the information it reports is *already computed*. SKILL.md L865 already counts `[CLARIFY:]` tags for the Report section. Writing that count into the artifact requires no additional computation.
- The refine invariant (e) does not add a new computation either. The refine path already produces a final output. The Report section already counts tags in that output. Status re-evaluation is: "set the same field using the same count you already computed for the Report." It is mechanically coupled to the Report's existing tag count, not independently computed.

The cost is not computational -- it is contractual. The invariant creates a testable obligation: after any refine, `## Status` must be consistent with the `[CLARIFY:]` tag count. This is a real obligation, and I should not have elided it with "zero-cost." The revised framing: the `## Status` field has zero marginal computation cost (the data already exists) but non-zero contractual cost (the consistency obligation must be maintained across write paths). This is an acceptable cost for a field that makes the artifact self-documenting.

Integration-architect's behavioral question (does refine re-evaluate previously resolved sections?) is correctly identified as orthogonal. Rule (e) says: "after the refine completes, status reflects the final tag count." It does not prescribe what the refine process examines -- only what the output must satisfy. The define handler's judgment about which sections to re-evaluate during refine remains unconstrained by the invariant.

---

### Rec #4: Reaffirm all P2 changes from the synthesis

**Original**: Changes 4-9 from the Round 1 synthesis are correct and should be adopted. Change 10 should be adopted with stated conditions.

**Cross-review feedback**:
- Integration-architect (SA-6) confirms C-4 through C-13 settled without further analysis.
- Devils-advocate (SA-10) confirms Changes 4-9 accepted without modification.

**Disposition**: REVISED on Change 10 conditions only.

Per Rec #1 disposition, condition 3 on Change 10 (placement between `# Problem Definition` and `## Decision`) is withdrawn. The revised conditions on Change 10 are:

1. The define handler sets the status; spec 007 does not state what consumers do with it.
2. No RFC 2119 SHOULD language prescribing downstream behavior.
3. *(Withdrawn)* ~~The `## Status` section goes between `# Problem Definition` and `## Decision`.~~ Replaced by: The `## Status` section goes after `## Source Documents` as the final section in the schema.

Integration-architect's T-2 (strictness of "no SHOULD language" condition) suggests that explicitly banning SHOULD is a negative requirement harder to verify than simply stating the jurisdictional boundary. This is a fair methodological point, but the negative requirement serves a specific purpose: the arbiter explicitly set aside devils-advocate's "SHOULD check" language (resolution.md, RD-1), and the condition records that decision to prevent re-introduction in the synthesis. The ban is not on the word "should" in lowercase descriptive prose -- it is on RFC 2119 uppercase SHOULD creating normative obligations for downstream consumers. I hold this condition as stated.

---

### Rec #5: Update spec.md schema block if `## Status` is adopted

**Original**: Spec.md L45-71 should include `## Status` to stay consistent with the SKILL.md schema.

**Cross-review feedback**:
- Devils-advocate (DC-2) notes that if spec.md L45-71 is updated, FR-009's implicit scope expands. If not, spec.md and SKILL.md disagree.

**Disposition**: REVISED per FR coverage correction.

The update to spec.md L45-71 is for illustrative consistency, not for expanding FR-009. FR-009 (spec.md L38) lists required content sections by name; `## Status` is a non-FR metadata enhancement. The spec.md schema block at L45-71 is an illustrative example (it appears in a fenced code block labeled "problem.md Schema"), not a normative requirement list. Adding `## Status` to the example makes it consistent with SKILL.md but does not change what FR-009 requires. The recommendation should include a note clarifying this distinction: "`## Status` is a schema enhancement implemented in SKILL.md; FR-009's section requirements are unchanged."

Priority remains P3. This is a documentation consistency fix with no behavioral impact.

---

### Rec #6: Reaffirm all P3 changes from the synthesis

**Original**: Changes 11-14 from the Round 1 synthesis are appropriate low-risk additions.

**Cross-review feedback**:
- Devils-advocate (OBA-3) argues Change 14 should be elevated from P3 to P2 and co-located with the schema.
- Integration-architect (SA-6) confirms all remaining items settled.

**Disposition**: HELD with annotation.

I addressed devils-advocate's priority elevation argument in my cross-review (T-3 in my cross-review of devils-advocate): the argument conflates placement (formatting decision, zero cost) with priority (implementation ordering). Co-locating Change 14's text adjacent to the schema is a good idea and should be done. Elevating its priority from P3 to P2 is not justified -- it is a forward-looking note about consumers that do not yet exist. I hold P3 for the priority while endorsing co-location as a formatting choice.

---

## New Recommendations

### New Rec #1: Specify write-failure behavior in the define handler (P2)

Devils-advocate's MO-1 (cross-review of my review, referenced in my cross-review T-1) identifies a real gap: the Report section at SKILL.md L856-875 assumes `problem.md` was successfully written. No behavior is specified for write failure. While I noted in my cross-review that the define handler uses the same Write tool as other handlers (SKILL.md L14: `allowed-tools: Agent Read Write Bash(ls:*)`), the Report section's success assumption should be guarded.

**Recommendation**: Add a one-sentence clause before the Report section (after SKILL.md L855): "If writing `problem.md` fails, report the error to the user and do not print the success report." This mirrors the error-handling discipline in the engine's Phase 6 failure handling (SKILL.md L653-657), where partial/failed output is explicitly addressed.

*Traced to*: Devils-advocate MO-1, SKILL.md L856-875 (Report assumes success), SKILL.md L653-657 (Phase 6 failure handling precedent).

### New Rec #2: State that `## Status` placement is after `## Source Documents` (P2)

My original Rec #1 specified placement between `# Problem Definition` and `## Decision`. Integration-architect's DC-2 correctly identified this as a UX error: the non-expert user (spec.md L87) should see the decision statement before machine metadata. I now recommend end-of-schema placement explicitly.

**Recommendation**: If `## Status` is adopted, it is the final section in the schema, placed after `## Source Documents` (SKILL.md L847). The heading is `## Status` and the content is a single line: `draft — {N} items need clarification` or `ready`. This placement ensures the substantive content (Decision through Source Documents) is presented first, and the status annotation summarizes the artifact's completeness at the end.

*Traced to*: Integration-architect DC-2, spec.md L87 (non-expert user principle), SKILL.md L822-850 (current schema ordering).

---

## Position Summary

Round 2 has produced strong convergence. All five RD disputes from Round 1 are resolved: I conceded on RD-1 (`## Status`) and RD-2 (shared validation), held on RD-3 (multi-path `--context` deferral) and RD-4 (`--force`/`--dry-run` deferral), and adopted the arbiter's formulation on RD-5 (refine semantics). All three reviewers now align on every dispute.

The cross-reviews surfaced two substantive corrections to my original Round 2 positions:

1. **`## Status` placement** (integration-architect DC-2): My condition 3 was wrong. Placing a metadata field before the decision statement degrades UX for the non-expert user. End-of-schema placement is correct. I withdraw the original placement and propose `## Status` after `## Source Documents`.

2. **Heading count hardcoding** (integration-architect DC-1): Hardcoding "8 headings" creates brittle coupling between recommendations. The validation should reference "all headings in the schema" with one authoritative list, not a hardcoded count.

One challenge I engaged but did not concede: devils-advocate's T-2 tension between "zero-cost" and "refine invariant obligation." The field is zero marginal computation cost (the tag count is already computed for the Report); the contractual cost (maintaining consistency across write paths) is real but acceptable. I refined the framing rather than abandoning the position.

The remaining disagreement surface is narrow: whether Change 14 should be P2 or P3 (I hold P3), and whether the "no SHOULD language" condition is necessary as an explicit ban or whether the jurisdictional boundary suffices (I hold the explicit ban as a record of the arbiter's decision on RD-1). Neither of these affects the spec's structural integrity.

All 12 functional requirements remain correctly implemented. The three P1 changes (post-write schema validation, `--context` path validation, dispatch matching semantics) are unanimous. The deliberation has been monotonically convergent -- no position reversals, only refinements toward shared ground.
