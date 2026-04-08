# Scope-Boundary Revision — Phase 1: Initial Utilization Review

**Spec**: 005-p2p3-backlog-hardening
**Reviewer role**: scope-boundary
**Revision iteration**: 1
**Date**: 2026-03-20

---

## Recommendation Dispositions

### Recommendation 1: Add explicit pass/fail criteria to Phase 1 tasks
**Original priority**: P2
**Disposition**: Modified

Compliance-auditor's cross-review (Tensions, item 1) acknowledges that embedding pass/fail criteria in the tasks document is "more durable" than a one-time audit, but notes that their own review already served as the pass/fail determination by citing exact file locations and matching them against FR text. The tension they identify is real: my recommendation is about process durability (any future re-run of Phase 1 would be unambiguous), while compliance-auditor's approach is sufficient for a single execution.

I modify the priority from P2 to P3. The practical question compliance-auditor raises -- whether Phase 1 will ever re-run -- is the right one. Phase 1 is a one-shot verification gate for this spec. If SKILL.md content shifts during Phase 4, Phase 5's T016 performs the re-verification, not Phase 1. The criteria still belong in the tasks document for auditability, but the risk of ambiguity in practice is lower than I originally assessed because both reviewers independently reached the same pass/fail conclusions without formalized criteria.

### Recommendation 2: Replace line number references with section heading references in T002 and T003
**Original priority**: P2
**Disposition**: Surviving (P2)

Compliance-auditor's cross-review (Tensions, item 2) explicitly concedes this point: "scope-boundary's concern is the more forward-looking one." They acknowledge that their own review uses the same fragile line numbers as evidence anchors without flagging them as fragile. The cross-review correctly identifies that for a single-pass audit current line numbers are reliable, but for a living tasks document they are not.

This recommendation survives without modification. Both Phase 4 tasks (T019, T019a, T013) edit SKILL.md, which will shift the line numbers referenced by T002 (L249) and T003 (L581-582). If Phase 1 is ever re-examined or cited as precedent, stale line numbers produce confusion. Section heading anchors are strictly superior.

### Recommendation 3: Add a Phase 1 task to verify STATUS.md baseline
**Original priority**: P2
**Disposition**: Modified

Compliance-auditor's cross-review (Dangerous Contradictions, item 2) frames this as a genuine disagreement about Phase 1's verification boundary. Compliance-auditor treats Phase 1 as responsible only for the FRs explicitly assigned to its tasks. I treated Phase 1 as responsible for verifying all preconditions of downstream phases. Compliance-auditor concedes that my position is "the more conservative one" but maintains their narrower scoping is also defensible.

I modify the recommendation. The original proposal (add T005a to verify STATUS.md exists with entries for specs 001-004) overreaches. Phase 1's stated purpose is "Confirm that 10 fully-implemented FRs and 1 partial (FR-011) are still correct." STATUS.md baseline verification is not an FR verification -- it is a precondition check for Phase 2. The correct placement is as a precondition note on Phase 2's header, not as a new Phase 1 task. Modified proposal: add to the Phase 2 header, after "Depends on Phase 1 verification passing": "Precondition: specs/STATUS.md exists with per-spec entries for specs 001-004. If STATUS.md structure has drifted, T006 and T007 instructions may need adjustment." This keeps Phase 1 scope clean while making the Phase 2 dependency explicit. Priority reduced to P3.

### Recommendation 4: Add negative verification for cooperative template
**Original priority**: P3
**Disposition**: Surviving (P3)

Compliance-auditor's cross-review (Tensions, item 3) validates this finding precisely: "the negative check was performed but is not encoded in the task definition. If a different auditor runs Phase 1 using only the task descriptions, they would not perform the negative check. scope-boundary is right that the task description should include it." Compliance-auditor performed the check and it passes, but the gap is in task specification, not verification outcome. Both reviews agree on the substance. This survives at P3 as originally assessed.

### Recommendation 5: Enumerate verified FRs explicitly in Phase 1 header
**Original priority**: P3
**Disposition**: Surviving (P3)

Compliance-auditor's cross-review (Dangerous Contradictions, item 1) substantially strengthens this recommendation. Their own Verification Summary Table only shows 8 full + 1 partial = 9 entries, yet the checkpoint claims "10 pre-existing FRs verified PASS." Compliance-auditor explicitly concedes: "I concede scope-boundary identified a verification gap my audit missed." The FR count discrepancy is real: FR-001 through FR-006 (6) + FR-010 (1) + FR-018 (1) = 8 fully verified, plus FR-011 partial. The "10" in the checkpoint is opaque without enumeration.

This recommendation survives. The convergence of both reviews on the count opacity -- compliance-auditor conceding the gap, and the cross-review's "Resolution needed" statement -- confirms that explicit enumeration is necessary for the gate to be auditable. Priority remains P3 because the practical impact is documentation clarity, not a functional risk.

### Recommendation 6: Confirm Phase 4 does not encroach on Phase 1 scope
**Original priority**: P1
**Disposition**: Withdrawn

This was a confirmation, not a recommendation. As I stated in the original review: "No change needed -- this is a confirmation, not a recommendation." Both reviews agree the Phase 1 / Phase 4 boundary for FR-011 is correctly drawn. Including a confirmation as a numbered recommendation was misleading. Compliance-auditor's cross-review does not challenge it because there is nothing to challenge -- it is already correct. Withdrawing as a recommendation; the confirmation stands as an alignment finding.

### Recommendation 7: Verify that Phase 3 + Phase 4 parallel execution does not create scope leaks
**Original priority**: P2
**Disposition**: Modified

Compliance-auditor's cross-review (Dangerous Contradictions, item 3) reframes the T019 risk in a way I had not considered. My original analysis focused on parallel-safety (does Phase 3 read SKILL.md, creating a dependency on Phase 4's write target?). Compliance-auditor identifies a different risk: T019's cross-reference replacement introduces behavioral changes (structural-marker support, case-insensitive heading matching) that the inline logic did not have, and T008 creates a STATUS.md entry about the Dispute-Parsing Subsystem that T019 may invalidate.

Both risks are real, and the cross-review is correct that they require different mitigations. However, the parallel-safety concern I originally raised has a lower probability than I assessed. Currently no Phase 3 task reads SKILL.md, and no Phase 4 task reads STATUS.md. The precondition note I proposed is still useful for preventing future regressions, but is lower priority. Modified: reduce priority to P3. The behavioral-change risk compliance-auditor identifies (T019 expanding semantics beyond what inline logic did) is the higher-impact concern, but it belongs to compliance-auditor's domain, not scope-boundary's. I credit compliance-auditor's Recommendation 3 as the more actionable mitigation for the T019 risk.

Compliance-auditor's cross-review (Safe Agreements, item 4) also identifies a STATUS.md staleness risk that both reviews converge on: T008 creates an entry whose content T019 may invalidate. Their Recommendation 4 (add a post-T019 update task) is well-placed. I endorse this as a cross-review finding rather than claiming it as my own.

### Recommendation 8: Confirm T006 is marked [x] correctly
**Original priority**: P1
**Disposition**: Surviving (P2)

Compliance-auditor's cross-review (Dangerous Contradictions, item 1) fully validates this: "an FR is claimed as implemented but sits in the verification blind spot between Phase 1 (which does not check it) and Phase 2 (which considers it done)." Compliance-auditor's own review does not mention T006's completed status or FR-012's verification gap. Their cross-review explicitly concedes: "scope-boundary's Recommendation 8 (add T005b to verify FR-012) directly addresses this; my review does not."

This recommendation survives. I modify the priority from P1 to P2. A P1 priority was overstated -- FR-012 (taxonomy section) is a documentation structure, and T006 being marked [x] means it was already executed. The risk is that the execution was incorrect, which is lower than a completely unverified functional requirement. But it does need verification: an unverified FR in a verification phase is a process gap regardless of the FR's nature.

---

## New Recommendations

### N1. Acknowledge the dual-site nature of FR-011 in T004's description (Priority: P3)

Emerged from compliance-auditor's Off-Base Assumption 1 (spec.md L278 mentions only Round Termination Check, but Trigger Evaluation is also an inline-parsing site) and my own cross-review (Dangerous Contradictions, item 4), where I conceded compliance-auditor is correct and my review was less thorough on this point. The tasks document handles both sites (T019 + T019a), so the operational risk is low. But T004's description says "Round Termination Check still uses inline parsing" without mentioning Trigger Evaluation. Since T019a exists specifically to address the second site, T004's note should say: "FR-011 is partial -- Round Termination Check and Trigger Evaluation both still use inline parsing (remediated in T019 and T019a respectively)." This makes the Phase 1 observation match the Phase 4 remediation scope.

### N2. Adopt compliance-auditor's FR-002 superset message observation as a Phase 2 documentation note (Priority: P3)

Emerged from compliance-auditor's cross-review (Tensions, item 4) and my cross-review (Dangerous Contradictions, item 2). SKILL.md L249 contains a longer error message than FR-002 specifies (it appends "This template requires a separate game-dynamics analysis spec before activation"). My original review treated this as a unidirectional pass (implementation satisfies spec). Compliance-auditor treats it as bidirectional drift (spec should match implementation). Both views are defensible, but the drift should be documented. Rather than editing spec.md during Phase 1 (violating read-only scope), add a note to the Phase 2 header or Phase 5's T016: "FR-002 error message in SKILL.md is a superset of the spec text. Consider updating spec.md FR-002 to match the actual implementation during Phase 5."

---

## Position Summary

Of my 8 original recommendations, I withdraw 1 (Recommendation 6, which was a confirmation misclassified as a recommendation), modify 3 (Recommendations 1, 3, and 7 -- all reduced in priority based on compliance-auditor's cross-review arguments), and maintain 4 as surviving (Recommendations 2, 4, 5, and 8). I add 2 new recommendations that emerged from cross-review analysis. The final count is 6 surviving/modified recommendations plus 2 new, for 8 total actionable items.

The most significant change is the modification to Recommendation 3 (STATUS.md baseline verification). Compliance-auditor correctly identified that adding a Phase 1 task to verify STATUS.md expands Phase 1's scope beyond its stated purpose of verifying pre-existing FRs. I originally framed this as a precondition gap; compliance-auditor framed it as a scope expansion. The resolution -- moving the precondition check to a Phase 2 header note rather than a new Phase 1 task -- respects both concerns. This revision reflects a general recalibration: my original review was somewhat expansionist about Phase 1's responsibilities, treating it as a comprehensive precondition gate rather than a focused FR verification pass. Compliance-auditor's narrower interpretation is more consistent with the tasks document's stated purpose.

The highest-priority surviving recommendation is Recommendation 2 (replace line number references with section heading anchors, P2). Both reviews converge on line numbers being fragile, and compliance-auditor explicitly concedes the forward-looking concern. This is the single change most likely to prevent a false verification result if Phase 1's findings are revisited after Phase 4 edits shift SKILL.md content. Recommendation 8 (verify FR-012 / T006 completion, now P2) is the close second -- an unverified FR in a verification-only phase is a structural gap that both reviews independently identify.
