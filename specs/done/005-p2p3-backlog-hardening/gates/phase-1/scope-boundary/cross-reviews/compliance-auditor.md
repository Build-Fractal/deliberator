# Cross-Review: compliance-auditor (from scope-boundary perspective)

**Reviewer**: scope-boundary
**Reviewing**: compliance-auditor's Phase 1 review
**Date**: 2026-03-20

---

## Dangerous Contradictions

### 1. Recommendations that modify Phase 1 scope vs. Phase 1 as read-only gate

Compliance-auditor's Recommendation 3 proposes appending a behavioral-change note to T019's task description in `tasks.md`. Recommendation 4 proposes adding a new sub-task in Phase 5 to update STATUS.md after T019. Recommendation 5 proposes modifying T003's description to add an FR-007 scope exclusion note. All three recommendations propose *writing* to the tasks document as part of Phase 1 findings.

My review (Alignment, item 1) explicitly establishes that "All five Phase 1 tasks use the verb 'Verify' and describe reading existing files to confirm FR satisfaction. No task instructs the agent to create, edit, or delete any file." If compliance-auditor's recommendations are acted upon during or as a condition of Phase 1 passing, they violate the read-only boundary.

**Resolution path**: Compliance-auditor's findings are analytically correct — the behavioral change in T019, the STATUS.md staleness after T019, and the FR-007 scope ambiguity are all real. The contradiction is about *when* these changes happen. If they are treated as Phase 1 audit observations that are implemented before Phase 2 begins (as a "Phase 1.5" or pre-Phase-2 cleanup), the scope boundary holds. If they are treated as Phase 1 pass/fail criteria, Phase 1 is no longer read-only.

[compliance-auditor Recommendations 3, 4, 5; scope-boundary Alignment item 1]

### 2. FR-002 error message mismatch: spec drift vs. implementation correctness

Compliance-auditor's Recommendation 1 and Off-Base Assumption 2 flag that SKILL.md L249 contains a longer error message than FR-002 specifies, and propose updating FR-002 in `spec.md` to match. My review does not flag this as an issue — I assessed T002 as verifying FR-002 and FR-003, and noted it as passing because the implementation includes the required text.

This is a genuine conflict about what "verify" means. Compliance-auditor treats verification as bidirectional: the implementation must match the spec AND the spec must match the implementation. My review treats verification as unidirectional: the implementation satisfies the spec's requirement (the spec text is a substring of the implementation text, so the requirement is met). The bidirectional view demands spec edits during Phase 1; the unidirectional view does not.

**Resolution path**: If the spec is the normative document and Phase 1 verifies implementation against spec, the superset message passes. If the audit standard requires exact text matching, the spec must be updated — but that is a Phase 2+ activity, not Phase 1 verification.

[compliance-auditor Recommendation 1, Off-Base Assumption 2; scope-boundary Alignment item 1, Recommendation 6 (confirmation that Phase 4 does not encroach)]

### 3. Whether T006's pre-completion creates an unverified FR in Phase 1

My review (Recommendation 8) flags that T006 is marked `[x]` (already complete), meaning FR-012 was implemented but is not verified by any Phase 1 task. I recommend adding T005b to verify it. Compliance-auditor does not mention T006's completed status or FR-012's verification gap at all — their Verification Summary Table lists only T001-T005 and does not address FR-012.

This is a contradiction about completeness. My review says Phase 1 has a gap (FR-012 unverified), while compliance-auditor's review implicitly treats Phase 1 as complete by not flagging this gap. The "10 pre-existing FRs" count in the checkpoint (`tasks.md` L30) is central to this: if FR-012 is among the 10, it needs a verification task; if it is not, the count may be wrong.

[scope-boundary Recommendation 8; compliance-auditor Verification Summary Table]

### 4. Spec assumption incompleteness: Round Termination only vs. both inline sites

Compliance-auditor's Off-Base Assumption 1 identifies that spec.md L278 mentions only the Round Termination Check as the site of inline parsing, while both Round Termination (L459-469) AND Trigger Evaluation (L531-542) use inline logic. They recommend expanding the assumption. My review (Alignment item 4) notes that "T004 explicitly notes 'FR-011 is partial — Round Termination Check still uses inline parsing (remediated in T019)'" and considers this clean scope separation — I did not flag the Trigger Evaluation omission as an issue.

Compliance-auditor is correct here and my review is less thorough on this point. Both inline-parsing sites should be acknowledged. However, the contradiction is about whether this incompleteness is a Phase 1 concern (spec accuracy) or a Phase 4 implementation concern (T019a already addresses it in `tasks.md` L87).

[compliance-auditor Off-Base Assumption 1, Recommendation 2; scope-boundary Alignment item 4]

---

## Tensions

### 1. Depth of behavioral analysis in a verification phase

Compliance-auditor's Missed Opportunities section performs deep behavioral analysis: heading-level specificity gaps, structural-marker support differences between inline logic and the Dispute-Parsing Subsystem, stagnation detection implications, and cooperative template heading coverage. This is analytically excellent work, but it probes behaviors that are explicitly deferred to Phases 2-4.

My review deliberately avoids this depth, focusing instead on whether Phase 1 tasks can be executed as specified without scope leakage. Both approaches serve the gate, but they create tension: compliance-auditor's depth risks generating recommendations that pull Phase 2-4 concerns into Phase 1, while my restraint risks missing important context that should inform Phase 1's pass/fail judgment.

[compliance-auditor Missed Opportunities items 2, 3, 5, 6; scope-boundary Alignment items 1-5]

### 2. Line number fragility: acknowledged but treated differently

Both reviews identify line number references as a concern. Compliance-auditor uses line numbers extensively throughout the review as evidence anchors (L249, L460, L467, L531-542, L581, L641-668, L666, L692-704). My review (Recommendation 2) explicitly recommends replacing line number references in task descriptions with section heading references, calling them "fragile references."

The tension: compliance-auditor's review is itself vulnerable to the same fragility it does not flag, while my review flags the fragility in task descriptions but does not propose a solution for audit reports. Both reviews would benefit from the same mitigation — anchoring to section headings or distinctive phrases rather than line numbers.

[compliance-auditor throughout; scope-boundary Recommendation 2]

### 3. STATUS.md baseline verification: flagged vs. unflagged

My review (Recommendation 3) proposes adding a Phase 1 task (T005a) to verify STATUS.md's baseline state, noting that Phase 2 tasks T006 and T007 depend on STATUS.md having a particular structure. Compliance-auditor does not address STATUS.md's baseline at all — their audit is scoped to the 5 existing Phase 1 tasks and does not consider what Phase 2 expects to find.

This creates tension because compliance-auditor's audit is narrower (verify what Phase 1 tasks say to verify) while my review is broader (verify what Phase 2 needs Phase 1 to have validated). Both scoping decisions are defensible, but they produce different confidence levels in the Phase 1 gate's utility as a foundation for Phase 2.

[scope-boundary Recommendation 3; compliance-auditor scope definition in Executive Summary]

### 4. Cooperative template negative check: explicit vs. implicit

My review (Recommendation 4) flags that T001 does not explicitly verify the cooperative template lacks a draft marker, despite acceptance scenario AS4 requiring this. Compliance-auditor's Alignment item 1 states "The cooperative template (L1) correctly does NOT have the marker" — they performed the check themselves but did not flag that no Phase 1 task formally requires it.

The tension: compliance-auditor's review proves the negative case holds (the cooperative template has no draft marker), but does not recommend that the task formally include this check. My review does not perform the check but recommends the task be explicit about it. The compliance audit compensates for the task gap in practice, but not in process.

[scope-boundary Recommendation 4; compliance-auditor Alignment item 1]

### 5. Whether "Confidence Assessment" heading omission is worth noting

Compliance-auditor's Missed Opportunity 5 notes that the cooperative template instructs a "Confidence Assessment" section (L104-111) but output validation only checks four headings, not five. My review does not mention this at all because it falls outside Phase 1's verification scope — Phase 1 verifies that the four specified headings are checked, not whether additional headings should be added.

The tension is between compliance thoroughness (noting every asymmetry between template instructions and validation) and scope discipline (restricting observations to what Phase 1 tasks cover). Both are valuable; the question is whether this observation belongs in a Phase 1 review or a Phase 4 review.

[compliance-auditor Missed Opportunity 5; scope-boundary overall framing]

---

## Safe Agreements

### 1. All 10 fully-implemented FRs pass verification

Both reviews independently confirm that T001-T005 verify their respective FRs correctly. Compliance-auditor provides line-level evidence for each (draft markers at L1 in three templates, SKILL.md L249 draft check, L581 output validation, L641-668 dispute-parsing subsystem, L692-704 baseline features). My review confirms the same tasks are properly scoped, genuinely parallel, and target non-overlapping file sections. Neither review finds a Phase 1 task that should fail.

[compliance-auditor Alignment items 1-5 and Verification Summary Table; scope-boundary Alignment items 1-4]

### 2. FR-011 partial status is correctly handled

Both reviews confirm that FR-011 is partial as expected, that the partial status is properly documented, and that remediation is correctly deferred to Phase 4 (T019/T019a). Compliance-auditor verifies the inline parsing locations (L459-469 and L531-542) against the Dispute-Parsing Subsystem (L641-668). My review confirms the boundary is clean: Phase 1 reads and notes the gap, Phase 4 writes the fix.

[compliance-auditor FR-011 partial verification and Alignment item 6; scope-boundary Alignment item 4 and Recommendation 6]

### 3. Phase 1 checkpoint is achievable through file reading alone

Both reviews confirm that the Phase 1 checkpoint ("10 pre-existing FRs verified, 1 partial (FR-011). Remaining 9 FRs ready for implementation.") produces no artifact and is a pass/fail gate achievable entirely through reading existing files. Neither review identifies a Phase 1 task that requires writing. This is the most important agreement: Phase 1 is genuinely verification-only.

[compliance-auditor Executive Summary paragraph 2; scope-boundary Alignment items 1, 3]

### 4. Phase dependency chain is sound

Both reviews implicitly validate the phase dependency structure. Compliance-auditor's recommendations for T019 behavioral notes and STATUS.md updates are framed as Phase 4/5 activities, not Phase 1 activities — confirming the phase ordering is correct even when proposing additions. My review explicitly validates the dependency chain as acyclic (Alignment item 5) and confirms Phase 3/4 parallel execution safety (Recommendation 7). Neither review identifies a circular dependency or a missing phase dependency.

[compliance-auditor Recommendations 3, 4 (phase placement); scope-boundary Alignment item 5, Recommendation 7]
