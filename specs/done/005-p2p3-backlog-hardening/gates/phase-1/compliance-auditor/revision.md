# Revision: Compliance Audit — Phase 1 (Spec 005)

**Auditor**: compliance-auditor
**Revision Iteration**: 1
**Date**: 2026-03-20

---

## Recommendation Dispositions

### Recommendation 1 — Update FR-002 error message to match SKILL.md
**Original priority**: P2
**Disposition**: Modified

scope-boundary's cross-review (Dangerous Contradiction 2) correctly identifies that this is a question of verification directionality. Their framing is precise: "The bidirectional view demands spec edits during Phase 1; the unidirectional view does not." I was applying bidirectional verification (spec must match implementation AND implementation must match spec) when Phase 1 is explicitly a unidirectional gate: does the implementation satisfy the spec?

The implementation text is a superset of the FR-002 text. The FR says the engine must fail with "Template {path} is marked as draft and cannot be used in production runs." The implementation emits exactly that string, followed by additional context. The requirement is satisfied. Updating FR-002 is not a Phase 1 concern.

However, the underlying observation remains valid as a documentation hygiene item. If FR-002 is read as an exact-match specification (which is a defensible reading of "MUST fail with:"), then the spec and implementation are technically out of sync. This is a P3 documentation cleanup for Phase 5, not a Phase 1 finding.

**Modified recommendation**: Downgrade to P3. Add to Phase 5 polish: "Verify FR-002 error message text matches SKILL.md L249 exactly, or add 'at minimum' qualifier to FR-002." This is not a Phase 1 pass/fail concern.

---

### Recommendation 2 — Expand spec assumption about FR-011 partial status
**Original priority**: P2
**Disposition**: Surviving

scope-boundary's cross-review (Dangerous Contradiction 4) acknowledges I am correct here: "Compliance-auditor is correct here and my review is less thorough on this point. Both inline-parsing sites should be acknowledged." scope-boundary raises the valid question of whether the incompleteness is a Phase 1 concern or a Phase 4 concern. The answer is that it is a spec-accuracy concern that exists independently of phase boundaries. The spec's assumption text (L278) is factually incomplete regardless of when it is corrected.

The operational risk is low because tasks.md correctly addresses both sites (T019 and T019a). But the spec is the normative document, and an assumption that omits half the problem sites is misleading. An implementor reading only spec.md would underestimate the scope of FR-011 remediation.

**Surviving recommendation**: Expand spec.md L278 to mention both Round Termination Check and Trigger Evaluation as sites of inline parsing. Priority remains P2 because spec accuracy is a first-order concern for any document intended as an authoritative reference.

---

### Recommendation 3 — Add behavioral-change note to T019 task description
**Original priority**: P2
**Disposition**: Modified

scope-boundary's cross-review (Dangerous Contradiction 1) raises an important procedural point: Phase 1 is a read-only gate, and recommending writes to tasks.md as part of Phase 1 findings risks violating that boundary. scope-boundary proposes a resolution: treat these as "Phase 1 audit observations that are implemented before Phase 2 begins (as a 'Phase 1.5' or pre-Phase-2 cleanup)." This is the correct framing.

Additionally, scope-boundary's cross-review (Dangerous Contradiction 3 in my cross-review of them) identifies a complementary risk I had not raised: T019 as a parallel-safety risk (does the cross-reference cause Phase 4 to read Phase 3's target file?). My analysis focused exclusively on semantic expansion. Both risks are real and require documentation on T019.

The underlying analytical finding is unchanged: replacing inline heading-only parsing with a cross-reference to the Dispute-Parsing Subsystem introduces structural-marker support and case-insensitive/level-agnostic heading matching. This is a behavioral expansion, not a pure refactor. But the mechanism for surfacing this finding must respect the read-only Phase 1 boundary.

**Modified recommendation**: The behavioral-change note for T019 remains P2, but it is explicitly an observation to be acted upon between Phase 1 and Phase 2 (or at the start of Phase 4 when T019 is being executed), not as a Phase 1 pass/fail criterion. The note should cover both the semantic-expansion risk I identified and the parallel-safety concern scope-boundary identified.

---

### Recommendation 4 — Add task to update STATUS.md T008 note after T019
**Original priority**: P2
**Disposition**: Surviving

scope-boundary's cross-review (Safe Agreement 4) independently confirms this finding: "Both reviews identify the same staleness risk through different analytical lenses." scope-boundary arrives at it via parallel-safety analysis; I arrive at it via temporal-consistency analysis. The convergence of two independent analyses strengthens the case.

The core problem is unchanged: T008 instructs creating a STATUS.md entry stating "stagnation detection does not support structural-marker parsing (only heading-based)." After T019 replaces inline logic with a Dispute-Parsing Subsystem cross-reference, this statement becomes false. Without a task to update it, STATUS.md will contain inaccurate information, directly undermining SC-003's "single-document reference" goal.

The same Phase 1 read-only boundary applies here (per scope-boundary's Dangerous Contradiction 1). This recommendation is an observation to be acted upon when planning Phase 4/5, not a Phase 1 gate criterion.

**Surviving recommendation**: Add a dependency note to T019 or a new Phase 5 sub-task to update the STATUS.md stagnation-detection entry after T019 completes. Priority P2. To be implemented outside Phase 1.

---

### Recommendation 5 — Clarify T003 scope excludes FR-007
**Original priority**: P3
**Disposition**: Modified

scope-boundary's cross-review (Tension 5) characterizes this as a tension between "compliance thoroughness" and "scope discipline." Their position is that the observation "belongs in a Phase 4 review" rather than a Phase 1 review. I partly agree: the risk of confusion is genuinely low because FR-007 is clearly listed as a Phase 4 task (T013) in tasks.md.

However, the modification I propose is lighter than what scope-boundary suggests. The task descriptions in tasks.md are concise by design. Adding "(FR-007 deferred to T013)" as a parenthetical to T003 is a one-line clarification, not scope expansion. It costs nothing and prevents exactly the confusion I described.

**Modified recommendation**: Downgrade from P3 to informational. If any task descriptions are being edited for other reasons (e.g., as part of the behavioral-change note on T019), a parenthetical noting FR-007 deferral could be added to T003. Not worth a standalone edit.

---

### Recommendation 6 — Verify cooperative template headings match FR-004 validation list
**Original priority**: P3
**Disposition**: Withdrawn

On reflection, this recommendation conflates two distinct concerns: (1) the asymmetry between template-instructed sections and engine-validated sections, and (2) the heading-level matching semantics. The first is a deliberate design choice explicitly noted in the spec (FR-004 lists four headings, not five). The second is covered by FR-007 (deferred to T013). There is no ambiguity to resolve and no documentation gap to fill. The spec is intentional about validating a subset, and adding a note to FR-004 explaining why "Confidence Assessment" is excluded would be over-documentation.

Credit to scope-boundary's overall framing (Tension 5) for clarifying that observations about template/validation asymmetry belong in the scope of the spec authors, not in a Phase 1 compliance audit.

---

### Recommendation 7 — Document that draft messages include game-dynamics note
**Original priority**: P3
**Disposition**: Withdrawn

This recommendation was speculative and forward-looking: "If draft markers are used for other purposes in the future, the error message text may need parameterization." This is a design concern about future extensibility, not a compliance finding. Phase 1 is verification of current state, not future-proofing. The observation is technically valid but does not belong in a compliance audit. It would be appropriate as a design note in a future spec that extends draft-marker functionality.

---

## New Recommendations

### New Recommendation A — FR-012 verification gap (Priority: P2)
**Source**: scope-boundary's cross-review (Dangerous Contradiction 3) and my own cross-review (Dangerous Contradiction 1)

scope-boundary identified a verification gap that my original audit missed entirely. T006 is marked `[x]` (already complete), meaning FR-012 (two-tier status taxonomy) was implemented before Phase 1 ran. But no Phase 1 task verifies FR-012. The "10 pre-existing FRs" claim in the Phase 1 checkpoint (tasks.md L30) is opaque: my own Verification Summary Table lists only 8 fully verified FRs (FR-001 through FR-006, FR-010, FR-018) plus 1 partial (FR-011), totaling 9 — not 10.

The most likely reconciliation: FR-012 is the tenth, implemented via T006 before Phase 1 and therefore counted as "pre-existing." But it has no verification task. This means either: (a) the count should be 9 full + 1 partial, or (b) a verification task for FR-012 should exist in Phase 1.

scope-boundary recommends adding T005b to verify FR-012. I concur. An FR that is claimed as implemented but sits in a verification blind spot weakens the Phase 1 gate. This is my most significant oversight from the original review.

### New Recommendation B — Explicit enumeration of "10 FRs" (Priority: P2)
**Source**: scope-boundary's Recommendation 5, corroborated by Dangerous Contradiction 1 in my cross-review

The checkpoint statement "10 pre-existing FRs verified" (tasks.md L30) does not enumerate which 10. Both reviews struggled to reconcile this count. The checkpoint should list the 10 FR numbers explicitly so that any future verifier can trace each one to a verification task. This could be as simple as: "FRs verified: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-010, FR-012, FR-018 (9 full) + FR-011 (partial)."

Note: this enumeration also forces resolution of whether the count is 9 or 10, addressing New Recommendation A above.

### New Recommendation C — STATUS.md baseline verification (Priority: P3)
**Source**: scope-boundary's Recommendation 3

scope-boundary argues that Phase 1 should verify STATUS.md's current state because Phase 2 tasks (T006, T007) depend on it existing with a particular structure. My original review scoped Phase 1 strictly to the FRs assigned to T001-T005, treating STATUS.md as out of scope. scope-boundary's position is more conservative and more correct: if a precondition is assumed but unverified, the gate is weaker.

I do not fully adopt scope-boundary's recommendation to add a new task (T005a), because adding tasks to Phase 1 conflicts with the read-only boundary we both agree on. However, the Phase 1 checkpoint should note the assumption that STATUS.md exists with the structure Phase 2 expects, so that if the assumption fails, Phase 2 tasks will surface it immediately rather than failing cryptically.

---

## Position Summary

Of my 7 original recommendations, I withdraw 2 (Recommendations 6 and 7), modify 3 (Recommendations 1, 3, and 5), and maintain 2 (Recommendations 2 and 4). I add 3 new recommendations (A, B, C) derived from scope-boundary's cross-review findings.

The most significant change is acknowledging the FR-012 verification gap (New Recommendation A). scope-boundary identified that T006 is marked complete but no Phase 1 task verifies FR-012, and that the "10 pre-existing FRs" count cannot be reconciled from my own Verification Summary Table. This is a genuine blind spot in my original audit: I verified what the Phase 1 tasks told me to verify, but did not check whether the task list itself was complete relative to the checkpoint's claim. scope-boundary's broader scoping — checking whether Phase 1 tasks cover everything the checkpoint asserts — caught what my narrower scoping missed. I credit scope-boundary fully for this finding.

The highest-priority surviving recommendation is Recommendation 4 (STATUS.md staleness after T019), now reinforced by convergent analysis from both reviewers. T008 creates a STATUS.md entry that T019 will invalidate. Without a planned update, STATUS.md becomes stale in exactly the way the spec warns against (spec.md L286: "STATUS.md is a living document"). This recommendation, combined with Recommendation 3's behavioral-change note, ensures that T019's cross-reference replacement is treated as a deliberate behavioral expansion rather than a transparent refactor. Both recommendations are observations to be acted upon outside Phase 1, respecting the read-only boundary that scope-boundary correctly established and I originally risked violating.
