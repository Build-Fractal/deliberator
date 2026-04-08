# Final Disputes: scope-boundary — Phase 1 (Spec 005)

**Reviewer**: scope-boundary
**Phase**: 4 (Cooperative Disputes)
**Date**: 2026-03-20

---

## Remaining Disputes

### Dispute 1: Where the FR-012 verification task belongs

Both reviews agree FR-012 sits in a verification blind spot: T006 is marked `[x]` but no Phase 1 task validates it. Compliance-auditor's New Recommendation A proposes adding T005b to Phase 1. I agree a verification task is needed. The dispute is placement.

Compliance-auditor frames T005b as a Phase 1 addition, which we both acknowledged conflicts with the read-only boundary. In their revision, they accept the read-only principle for Recommendations 3, 4, and 5 — but do not apply the same logic to New Recommendation A. Adding a task to Phase 1 is still a write to Phase 1's scope. The consistent position is: observe the gap in Phase 1, verify FR-012 as a pre-Phase-2 cleanup (the same "Phase 1.5" framing we converged on for other write-producing observations). The distinction matters because if we allow task additions to Phase 1, the read-only boundary we both agreed to becomes advisory rather than structural.

**My position**: FR-012 verification is a pre-Phase-2 gate activity, not a Phase 1 task addition. The observation belongs in Phase 1 findings; the verification task belongs outside Phase 1.

### Dispute 2: Priority of the "10 FRs" enumeration (P2 vs. P3)

Compliance-auditor's New Recommendation B assigns P2 to explicitly enumerating the "10 pre-existing FRs" in the Phase 1 header. My Recommendation 5 (surviving) assigns P3 to the same finding. Compliance-auditor's justification is that enumeration "forces resolution of whether the count is 9 or 10," tying it to the FR-012 gap.

I maintain P3. The count opacity is a documentation clarity issue, not a functional risk. Both reviews independently traced the FR-to-task mapping and reached the same conclusion about the gap. The enumeration makes the gate more auditable but does not change its outcome — Phase 1 either passes or fails on the same evidence regardless of whether the header lists the FR numbers. Tying the priority to the FR-012 gap conflates two distinct problems: the missing verification (which is P2) and the missing label (which is P3).

**My position**: Enumeration is P3. The FR-012 verification gap is P2. They are separate concerns with separate priorities.

---

## Convergence

### 1. Phase 1 is a read-only gate; write-producing findings belong outside Phase 1

Both revisions converge on this principle. Compliance-auditor explicitly adopts the "Phase 1.5" or "pre-Phase-2 cleanup" framing for Recommendations 3, 4, and 5. My revision reduces Recommendation 3 (STATUS.md baseline) from a Phase 1 task to a Phase 2 header precondition note. Neither reviewer now proposes modifications to tasks.md as Phase 1 pass/fail criteria.

### 2. FR-011 partial status requires acknowledging both inline-parsing sites

Compliance-auditor's Recommendation 2 (surviving, P2) proposes expanding spec.md L278 to mention both Round Termination Check and Trigger Evaluation. My revision conceded compliance-auditor is correct on this point and my original review was less thorough. My New Recommendation N1 proposes the same dual-site acknowledgment in T004's description. Both reviews now agree that the spec's assumption text is factually incomplete.

### 3. T019 introduces behavioral expansion, not a transparent refactor

Compliance-auditor's Recommendation 3 (modified) identifies that replacing inline parsing with a Dispute-Parsing Subsystem cross-reference introduces structural-marker support and case-insensitive heading matching that the inline logic did not have. My revision (Recommendation 7, modified) credits compliance-auditor's semantic-expansion analysis as the higher-impact concern. Both reviews now treat T019 as a behavioral change requiring documentation, not a drop-in replacement.

### 4. STATUS.md staleness after T019 requires a planned update

Compliance-auditor's Recommendation 4 (surviving, P2) proposes a post-T019 task to update the STATUS.md stagnation-detection entry that T008 creates. My cross-review (Safe Agreements, item 4) independently identified the same staleness risk. Both revisions endorse this finding without modification. The convergence is complete: T008 creates an entry that T019 will invalidate, and a planned update must exist.

### 5. Line number references in task descriptions should be replaced with section heading anchors

Compliance-auditor's revision explicitly concedes my Recommendation 2 is "the more forward-looking one." My revision maintains this at P2 without modification. Both reviews agree that T002's "L249" and T003's "L581-582" references are fragile and should use distinctive phrases or section headings instead. This is the single recommendation with the cleanest bilateral agreement.

---

## Final Position Statement

### Non-Negotiables

1. **The read-only boundary applies uniformly.** Any finding that produces a write to Phase 1's task list or scope definition is an observation to be acted upon outside Phase 1. This includes FR-012 verification (Dispute 1). The principle was established by both reviewers, conceded by compliance-auditor for three of their recommendations, and must not be selectively relaxed for new recommendations. If we add T005b, it belongs in a pre-Phase-2 gate, not in Phase 1's task list.

2. **T019 must be documented as a behavioral expansion.** The combined finding from both reviews — that cross-referencing the Dispute-Parsing Subsystem introduces capabilities (structural-marker support, case-insensitive matching) absent from the inline logic it replaces — must be surfaced before T019 executes. The note should cover both the semantic-expansion risk (compliance-auditor) and the parallel-safety precondition (scope-boundary). This is an observation for Phase 4 execution, not a Phase 1 gate criterion.

3. **Replace line number references with section heading anchors in T002 and T003.** Both reviews converge without reservation. Stale line numbers are the most likely source of false verification results if Phase 1 findings are revisited after Phase 4 edits SKILL.md.

### Flexibility

1. **FR-012 verification mechanism.** I insist it happens outside Phase 1, but I am flexible on whether it is a standalone task (T005b as pre-Phase-2), a note appended to the Phase 2 header, or folded into T016 (Phase 5 full-FR verification). The verification must occur; the vehicle is negotiable.

2. **Priority of the FR enumeration.** I hold P3 but will accept P2 if the synthesis determines that the count reconciliation (9 vs. 10) is blocking rather than clarifying. The enumeration itself is not in dispute — only its urgency.

3. **STATUS.md baseline verification placement.** My revised position (Phase 2 header precondition note) is lighter than my original (new Phase 1 task). I will accept compliance-auditor's even lighter framing (Phase 1 checkpoint annotation) if it makes the Phase 2 dependency explicit in any documented form. The key requirement is that the assumption is written down somewhere a Phase 2 executor will see it.
