# Final Disputes — Compliance Auditor (Phase 1, Spec 005)

**Auditor**: compliance-auditor
**Phase**: 4 (Final Position)
**Date**: 2026-03-20

---

## Remaining Disputes

### Dispute 1: Priority of FR-012 verification gap (my New Rec A vs. scope-boundary Rec 8)

Both reviews converge on the substance: T006 is marked `[x]`, FR-012 has no Phase 1 verification task, and this is a genuine blind spot. The dispute is narrow but consequential: scope-boundary reduced this from P1 to P2 in revision, and I concurred with P2 in my own New Recommendation A. However, scope-boundary frames the verification as "add T005b" (a new Phase 1 task), while I frame it as an observation to be resolved before Phase 2 begins. These are operationally different. Adding a task to Phase 1 retroactively changes a completed phase's scope. My position: the verification should be performed as a pre-Phase-2 gate check, not by reopening Phase 1's task list. The distinction matters for process integrity -- a phase that gains tasks after completion is no longer a reliable checkpoint.

### Dispute 2: Line number references — scope vs. mechanism (scope-boundary Rec 2)

scope-boundary's surviving Recommendation 2 (replace line number references with section heading references in T002 and T003) is correct in principle. I conceded this in cross-review. The remaining dispute is about when and how. scope-boundary treats this as a standalone P2 action item. I hold that it should be bundled with any other task description edits (e.g., the behavioral-change note on T019, the T004 dual-site note) as a single pre-Phase-2 editorial pass rather than a separate work item. The risk of stale line numbers is real but dormant until Phase 4 executes. A dedicated P2 work item for what amounts to two find-and-replace edits (L249 to "Step 3 draft-marker check section", L581-582 to "Phase 6 output validation section") is process overhead that a bundled editorial pass avoids.

---

## Convergence

### 1. Phase 1 is a read-only verification gate

Both reviews now agree that Phase 1 is unidirectional (does implementation satisfy spec?) and read-only (no writes to spec.md, tasks.md, or target files). All recommendations that require document edits are framed as observations to be acted upon between phases, not as Phase 1 pass/fail criteria. This resolved the most significant procedural tension from the original reviews.

### 2. FR-011 dual-site acknowledgment

Both reviews agree that spec.md L278 is factually incomplete (mentions only Round Termination Check, omits Trigger Evaluation) and that T004's description should note both sites. scope-boundary's New Recommendation N1 and my surviving Recommendation 2 address the same gap from different angles. The tasks document (T019 + T019a) already handles both sites correctly, so the risk is documentation accuracy, not implementation correctness.

### 3. STATUS.md staleness after T019

Both reviews independently identified that T008 creates a STATUS.md entry about stagnation detection's limitations, and T019 will invalidate that entry by replacing inline logic with a Dispute-Parsing Subsystem cross-reference. My Recommendation 4 and scope-boundary's endorsement of it (Rec 7 revision) are fully aligned. A post-T019 update task or dependency note is needed.

### 4. "10 pre-existing FRs" enumeration is necessary

Both reviews struggled to reconcile the checkpoint count at tasks.md L30. My New Recommendation B and scope-boundary's surviving Recommendation 5 converge: the checkpoint must explicitly list which FRs are counted. This also forces resolution of whether the count is 9 or 10, addressing the FR-012 verification gap.

### 5. STATUS.md baseline belongs as a Phase 2 precondition, not a Phase 1 task

scope-boundary originally proposed adding T005a to Phase 1 (Rec 3), then revised to a Phase 2 header precondition note. I originally scoped STATUS.md out of Phase 1 entirely, then adopted scope-boundary's revised position as more conservative and more correct. Both reviews now agree on the mechanism: a precondition note on the Phase 2 header, not a new Phase 1 task.

---

## Final Position Statement

### Non-Negotiables

1. **FR-012 must be verified before Phase 2 begins.** Whether via a new task (T005b) or a pre-Phase-2 gate check, an FR claimed as implemented but sitting in a verification blind spot cannot be carried forward unverified. The mechanism is negotiable; the requirement is not. An unverified FR in a verification phase undermines the gate's credibility for all subsequent phases.

2. **The "10 pre-existing FRs" checkpoint must enumerate the specific FR numbers.** An opaque count that neither reviewer could independently reconcile is not an auditable checkpoint. The enumeration forces the count to be correct and traceable. This is a minimum standard for any verification gate that downstream phases depend on.

3. **T019's behavioral expansion must be documented before execution.** T019 replaces inline heading-only parsing with a cross-reference to the Dispute-Parsing Subsystem, which introduces structural-marker support and case-insensitive/level-agnostic heading matching. This is a semantic expansion, not a transparent refactor. The T019 task description or a dependency note must acknowledge this so that the implementor treats it as a deliberate behavioral change. Without this, a silent capability expansion in a prompt-orchestrated system creates drift between what the spec assumes and what the implementation does.

### Flexibility

1. **Mechanism for FR-012 verification.** I accept either a new task (T005b as scope-boundary proposes) or a pre-Phase-2 gate check (my preference). The substance -- that FR-012 is verified -- matters more than the process container it sits in.

2. **Timing of line number replacement.** I accept scope-boundary's position that line numbers in T002/T003 should become section heading references. I am flexible on whether this is a standalone edit or bundled with other task description changes in a single pre-Phase-2 editorial pass.

3. **Placement of T019 behavioral-change documentation.** I accept the note being placed on T019's task description, as a new sub-task, or as a Phase 4 preamble note. The content (acknowledging semantic expansion and the STATUS.md staleness risk) is the non-negotiable; where it lives is not.
