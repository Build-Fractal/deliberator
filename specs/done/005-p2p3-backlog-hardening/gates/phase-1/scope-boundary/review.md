# Scope-Boundary Review — Phase 1: Initial Utilization Review

**Spec**: 005-p2p3-backlog-hardening
**Reviewer role**: scope-boundary
**Date**: 2026-03-20

---

### Executive Summary

Spec 005 is a backlog-hardening effort that consolidates 11 user stories (19 FRs) covering draft template safety markers, post-Phase-6 output validation, cross-spec status tracking, shared dispute-parsing documentation, two-tier status conventions, and several P3 documentation items. The spec claims that 10 FRs are already implemented and 1 is partial (FR-011), leaving 9 FRs for implementation across Phases 2-4. The tasks document (`tasks.md`) organizes this into 5 phases, with Phase 1 designated as pure verification — read-only confirmation that the 10 pre-existing FRs remain intact.

From a scope-boundary perspective, this spec is well-structured. Phase 1 is explicitly read-only (all 5 tasks are marked `[P]` for parallel, and their descriptions use the verb "Verify"). No Phase 1 task creates, modifies, or deletes any file. The phase boundaries between read-only Phase 1 and write-oriented Phases 2-4 are clean, with Phase 2 depending on Phase 1 passing but not on any artifact Phase 1 produces. The checkpoint ("10 pre-existing FRs verified, 1 partial (FR-011). Remaining 9 FRs ready for implementation.") is achievable by reading existing files only.

My most important recommendation: document the specific SKILL.md line numbers or section identifiers that each Phase 1 task must inspect, because two tasks (T002, T003) reference line numbers that may have drifted since the task document was written, and a Phase 1 failure caused by stale line references is a false negative that would incorrectly block Phase 2.

### Alignment

- **[Phase 1 is read-only]** (`tasks.md`, L20-30): All five Phase 1 tasks use the verb "Verify" and describe reading existing files to confirm FR satisfaction. No task instructs the agent to create, edit, or delete any file. This is the correct scope for a verification phase. [`tasks.md`, L20-30]

- **[Tasks are genuinely parallel]** (`tasks.md`, L14, L132): All five Phase 1 tasks are marked `[P]` and target different files or non-overlapping sections of SKILL.md (T001: template files; T002: SKILL.md Step 3; T003: SKILL.md Phase 6; T004: SKILL.md Dispute-Parsing Subsystem section; T005: SKILL.md Baseline Features section). There are no hidden dependencies. [`tasks.md`, L14, L132]

- **[Checkpoint is verification-only]** (`tasks.md`, L30): The Phase 1 checkpoint states "10 pre-existing FRs verified, 1 partial (FR-011). Remaining 9 FRs ready for implementation." This produces no artifact — it is a pass/fail gate. The checkpoint is achievable entirely through file reading. [`tasks.md`, L30]

- **[FR-011 partial status is acknowledged]** (`tasks.md`, L27): T004 explicitly notes "FR-011 is partial — Round Termination Check still uses inline parsing (remediated in T019)" and does not attempt to fix it. The remediation is correctly deferred to Phase 4 (T019). This is clean scope separation. [`tasks.md`, L27, L86]

- **[Phase dependency chain is acyclic]** (`tasks.md`, L109-114): Phase 1 has no dependencies. Phase 2 depends on Phase 1. Phase 3 depends on Phase 2. Phase 4 depends on Phase 1 (not Phase 2 or 3). Phase 5 depends on Phases 3 and 4. No circular dependencies exist. [`tasks.md`, L109-114]

### Missed Opportunities

- **[Explicit pass/fail criteria for each verification task]**: Each Phase 1 task says "Verify X exists" but does not specify what constitutes a verification failure versus a pass. For example, T001 says "Verify draft markers exist as first line" — but what if the marker exists on line 2 instead of line 1? Should the verifier report a failure or a degraded pass? The spec (FR-001, `spec.md` L202) says "MUST contain ... as their first line," so line 2 is a failure, but the task description does not make this explicit. Without pass/fail criteria, two verifiers could reach different conclusions. Impact: medium. [`tasks.md`, L24; `spec.md`, L202]

- **[Stale line number references]**: T002 references "SKILL.md Step 3 (L249)" and T003 references "SKILL.md Phase 6 output validation (L581-582)." These line numbers correspond to the current SKILL.md content, but line numbers drift as the file is edited. If a future Phase 2 or Phase 3 edit shifts SKILL.md content before Phase 1 re-runs (e.g., in a CI context), the line references become misleading. The tasks should reference section headings or anchors rather than line numbers. Impact: medium. [`tasks.md`, L25-26]

- **[No verification of FR-007 partial state]**: FR-007 (heading validation is case-insensitive and matches as substring within heading lines) is listed as needing implementation in Phase 4 (T013), but no Phase 1 task verifies whether the current SKILL.md output validation section already partially addresses this. The current SKILL.md L581-582 says to check for required section headings but does not specify case-insensitivity or heading-level matching. Phase 1 could verify this gap explicitly so Phase 4's T013 is properly scoped. Impact: low. [`spec.md`, L211; `tasks.md`, L88]

- **[No verification of STATUS.md existing state]**: The spec assumes STATUS.md "exists with basic per-spec status" (`spec.md`, L275). Phase 1 has no task that verifies STATUS.md's current content against this assumption. If STATUS.md were to be deleted or substantially altered before Phase 2, the Phase 2 tasks (T006, T007) would need different instructions. A Phase 1 verification of STATUS.md's baseline state would make the Phase 2 dependency explicit. Impact: medium. [`spec.md`, L275; `tasks.md`, L34-47]

- **[No verification of template cooperative/arbitration.md lacking draft marker]**: T001 verifies the three non-cooperative templates have draft markers. The inverse check — that `templates/cooperative/arbitration.md` does NOT have a draft marker (spec.md L23, US1 AS4) — is not explicitly assigned to any Phase 1 task. While T001's description says "Verify draft markers exist as first line of [three templates]," it does not include the negative check. This negative check is part of the acceptance scenario. Impact: low. [`spec.md`, L23; `tasks.md`, L24]

- **[No enumeration of the "10 FRs" being verified]**: The Phase 1 purpose says "Confirm that 10 fully-implemented FRs and 1 partial (FR-011) are still correct" but does not enumerate which 10 FRs those are. The mapping must be inferred: T001 covers FR-001, T002 covers FR-002 and FR-003, T003 covers FR-004/FR-005/FR-006, T004 covers FR-010, T005 covers FR-018. That is 9 FRs (FR-001 through FR-006, FR-010, FR-018) plus the partial FR-011 = 10 + 1 partial. But the tasks document does not surface this count reconciliation. An explicit FR enumeration in the Phase 1 header would prevent miscounting. Impact: low. [`tasks.md`, L20-22]

### Off-Base Assumptions

- **[Phase 1 tasks T001-T005 are all [P] with no hidden dependencies]** (`tasks.md`, L14, L24-28): This assumption is correct. T001 reads three template files. T002 reads SKILL.md Step 3. T003 reads SKILL.md Phase 6. T004 reads SKILL.md Dispute-Parsing Subsystem section. T005 reads SKILL.md Baseline Features section. These are non-overlapping file reads with no data dependency between them. The `[P]` annotation is accurate.

- **[FR-011 is partial by design]** (`tasks.md`, L27; `spec.md`, L278): This is correct. The spec's own Assumptions section (L278) states "FR-011 is partially complete: STATUS.md cross-reference exists but SKILL.md Round Termination Check still uses inline dispute-counting logic independent of the Dispute-Parsing Subsystem." T004 verifies FR-010 (the subsystem exists) and notes FR-011 is partial. T019 in Phase 4 remediates it. No off-base assumption here.

The spec makes no incorrect assumptions about scope boundaries. The Phase 1 / Phase 2-4 separation is clean.

### Actionable Recommendations

1. **Add explicit pass/fail criteria to Phase 1 tasks** (Priority: P2)
   - **Current state**: Tasks T001-T005 use "Verify" without defining what constitutes pass vs. fail (`tasks.md`, L24-28).
   - **Proposed change**: Append to each task description a parenthetical with the failure condition. Example for T001: "Verify draft markers exist as first line of templates/winner-take-all/arbitration.md, templates/red-blue/arbitration.md, templates/prisoners-dilemma/arbitration.md (FAIL if marker is absent, on wrong line, or has different syntax) (US1: FR-001)."
   - **Rationale**: Phase 1 is a gate. A gate without explicit pass/fail criteria is ambiguous. Two verifiers could disagree on whether a degraded state (e.g., marker on line 2) is a pass or fail. [`spec.md`, L202: "MUST contain ... as their first line."]
   - **Risk if ignored**: Verification could pass when it should fail (marker present but not on first line), allowing Phase 2 to proceed on a broken foundation.

2. **Replace line number references with section heading references in T002 and T003** (Priority: P2)
   - **Current state**: T002 says "SKILL.md Step 3 (L249)" and T003 says "SKILL.md Phase 6 output validation (L581-582)" (`tasks.md`, L25-26).
   - **Proposed change**: T002: "Verify SKILL.md Step 3 (the paragraph beginning 'If the loaded template's first line contains') contains draft marker check with correct error message." T003: "Verify SKILL.md Phase 6 section (the paragraph beginning 'After Phase 6 completes successfully, validate that') checks four required section headings with non-blocking warning."
   - **Rationale**: Line numbers are fragile references. SKILL.md is edited in Phases 2-4 of this very spec, which could shift content. Section headings and distinctive phrases are stable anchors. [`SKILL.md`, L249, L581-582 — these are the current correct locations but will drift.]
   - **Risk if ignored**: A verifier targeting L249 after a Phase 2 edit may read the wrong content and produce a false positive or false negative.

3. **Add a Phase 1 task to verify STATUS.md baseline** (Priority: P2)
   - **Current state**: No Phase 1 task verifies the current state of `specs/STATUS.md`. The spec assumes it "exists with basic per-spec status" (`spec.md`, L275), and Phase 2 tasks (T006, T007) depend on this.
   - **Proposed change**: Add T005a: "T005a [P] Verify specs/STATUS.md exists and contains entries for specs 001-004 with implementation status labels (US3: precondition for FR-008)."
   - **Rationale**: Phase 2's T006 adds a taxonomy section and T007 updates spec 001's entry. If STATUS.md's current structure differs from what T006/T007 expect, those tasks will fail in unexpected ways. A Phase 1 verification of the baseline makes the dependency explicit and surfaces structural drift early. [`spec.md`, L275; `tasks.md`, L44-45]
   - **Risk if ignored**: Phase 2 tasks could fail with confusing errors if STATUS.md has been modified between spec writing and task execution.

4. **Add negative verification for cooperative template** (Priority: P3)
   - **Current state**: T001 verifies the three non-cooperative templates have draft markers but does not verify that `templates/cooperative/arbitration.md` does NOT have one (`tasks.md`, L24).
   - **Proposed change**: Extend T001: "...and verify templates/cooperative/arbitration.md does NOT contain the draft marker (US1: FR-001 inverse, AS4)."
   - **Rationale**: Acceptance scenario 4 (`spec.md`, L23) explicitly tests this negative case. If someone accidentally adds a draft marker to the cooperative template, the system would reject the only production-ready template. Phase 1 should catch this. [`spec.md`, L23]
   - **Risk if ignored**: An accidental draft marker on the cooperative template would not be caught until runtime, when Phase 6 fails to load the template.

5. **Enumerate verified FRs explicitly in Phase 1 header** (Priority: P3)
   - **Current state**: Phase 1 purpose says "10 fully-implemented FRs and 1 partial" without listing them (`tasks.md`, L22).
   - **Proposed change**: Add after the Purpose line: "FRs verified: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-010, FR-018 (fully implemented); FR-011 (partial). Total: 8 full + 1 partial = 9 FRs verified, plus FR-012 taxonomy structure verified."
   - **Rationale**: The claim of "10 fully-implemented FRs" needs reconciliation. Counting FR-001 through FR-006 (6) + FR-010 (1) + FR-018 (1) = 8. The "10" likely includes FR-012 (taxonomy section already exists in STATUS.md per T006 being marked `[x]`) and possibly others. An explicit enumeration prevents miscounting and makes the gate auditable. [`tasks.md`, L22, L44]
   - **Risk if ignored**: Auditors cannot verify the "10 FRs" claim without manually tracing each task to its FR mapping.

6. **Confirm Phase 4 does not encroach on Phase 1 scope** (Priority: P1)
   - **Current state**: Phase 4 tasks T019 and T019a remediate FR-011 by replacing inline parsing with cross-references (`tasks.md`, L86-87). Phase 1 T004 verifies FR-010 and notes FR-011 is partial. This boundary is clean.
   - **Proposed change**: No change needed — this is a confirmation, not a recommendation. The boundary is correctly drawn: Phase 1 reads and notes the gap; Phase 4 writes the fix. Documenting this confirmation in the review record.
   - **Rationale**: FR-011 remediation is the most likely boundary violation candidate. Confirming it is correctly placed prevents future confusion. [`tasks.md`, L27, L86-87]
   - **Risk if ignored**: N/A — this is already correct.

7. **Verify that Phase 3 + Phase 4 parallel execution does not create scope leaks** (Priority: P2)
   - **Current state**: `tasks.md` L133 states Phase 3 and Phase 4 can run in parallel because they edit different files (STATUS.md vs. SKILL.md). This is correct for file-level isolation.
   - **Proposed change**: Add a note to the Parallel Example section (L139-155): "Precondition: Phase 3 tasks do not read SKILL.md, and Phase 4 tasks do not read STATUS.md. If any task in either phase reads the other phase's target file, the phases cannot safely run in parallel."
   - **Rationale**: T019 (`tasks.md`, L86) replaces inline dispute-counting in SKILL.md with a cross-reference to the Dispute-Parsing Subsystem section — also in SKILL.md. T008 (`tasks.md`, L63) adds a Dispute-Parsing Subsystem entry to STATUS.md. If T008 needed to verify the SKILL.md section it references, it would read SKILL.md, creating a read dependency on Phase 4's write target. Currently T008 does not do this, but the precondition should be stated. [`tasks.md`, L63, L86, L133]
   - **Risk if ignored**: A future task addition to Phase 3 could introduce a cross-file read dependency that breaks parallel safety without anyone noticing.

8. **Confirm T006 is marked [x] correctly** (Priority: P1)
   - **Current state**: T006 is marked `[x]` (complete) in the tasks document (`tasks.md`, L44), meaning it was already executed. T006 is a Phase 2 task ("Update taxonomy section in specs/STATUS.md to add two-tier acceptance convention"). This is consistent with STATUS.md already containing the two-tier taxonomy section (`STATUS.md`, L5-24). However, Phase 1 does not verify this.
   - **Proposed change**: If T006 is already complete, add its FR (FR-012) to the Phase 1 verification scope. Add a task: "T005b [P] Verify specs/STATUS.md Taxonomy section contains both implementation tier and acceptance tier definitions (US5: FR-012, already implemented)."
   - **Rationale**: The Phase 1 purpose is to verify pre-existing FRs. If FR-012 is already implemented (T006 marked `[x]`), it should be verified in Phase 1 alongside the other pre-existing FRs. Currently it falls into a gap: Phase 1 does not verify it, and Phase 2 considers it done. [`tasks.md`, L22, L44; `STATUS.md`, L5-24]
   - **Risk if ignored**: FR-012 is unverified — it was implemented but never validated by the Phase 1 gate.

### Referenced Documentation

- `conversus/specs/005-p2p3-backlog-hardening/spec.md` — sections/lines cited: L14, L20-23, L202, L211, L275, L278
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` — sections/lines cited: L14, L20-30, L22, L24-28, L25-26, L27, L30, L34-47, L44-45, L63, L86-87, L88, L109-114, L132-133, L139-155
- `conversus/SKILL.md` — sections/lines cited: L249, L453-493, L531-542, L581-582, L641-668, L692-704
- `conversus/specs/STATUS.md` — sections/lines cited: L1-52 (full document), L5-24 (taxonomy section)
- `conversus/templates/cooperative/arbitration.md` — sections/lines cited: L1 (no draft marker)
- `conversus/templates/winner-take-all/arbitration.md` — sections/lines cited: L1 (draft marker present)
- `conversus/templates/red-blue/arbitration.md` — sections/lines cited: L1 (draft marker present)
- `conversus/templates/prisoners-dilemma/arbitration.md` — sections/lines cited: L1 (draft marker present)
