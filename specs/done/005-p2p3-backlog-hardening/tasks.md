# Tasks: P2/P3 Backlog Hardening

**Input**: Design documents from `/specs/005-p2p3-backlog-hardening/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Not requested — no test tasks generated.

**Organization**: Tasks grouped by user story. Stories US1, US4, and US10 are already implemented (10 of 19 FRs done, 1 partial) — Phase 1 verifies them. Remaining 9 FRs target 2 files: `specs/STATUS.md` and `SKILL.md`.

**Convention**: Mark completed tasks with `- [x]`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Verification of Pre-Existing FRs)

**Purpose**: Confirm that 10 fully-implemented FRs and 1 partial (FR-011) are still correct before building on them

- [x] T001 [P] Verify draft markers exist as first line of templates/winner-take-all/arbitration.md, templates/red-blue/arbitration.md, templates/prisoners-dilemma/arbitration.md (US1: FR-001)
- [x] T002 [P] Verify SKILL.md Step 3 (L249) contains draft marker check with correct error message (US1: FR-002, FR-003)
- [x] T003 [P] Verify SKILL.md Phase 6 output validation (L581-582) checks four required section headings with non-blocking warning (US2: FR-004, FR-005, FR-006)
- [x] T004 [P] Verify SKILL.md Dispute-Parsing Subsystem section documents input, output, parsing rules, and stable-interface contract (US4: FR-010). Note: FR-011 is partial — Round Termination Check still uses inline parsing (remediated in T019)
- [x] T005 [P] Verify SKILL.md Baseline Features section documents iterations, prior, path-list formatting, multi-file target resolution, template variables, background dispatch, multi-agent rules (US10: FR-018)

**Checkpoint**: 10 pre-existing FRs verified, 1 partial (FR-011). Remaining 9 FRs ready for implementation.

---

## Phase 2: Foundational — Two-Tier Status Convention (US5, Priority: P2)

**Purpose**: Define the two-tier status convention that all STATUS.md updates depend on

**⚠️ CRITICAL**: STATUS.md enrichment tasks (Phase 3) depend on the taxonomy being defined first

**Goal**: Establish "feature-complete" / "spec-complete" convention alongside existing implementation-tier taxonomy.

**Independent Test**: STATUS.md taxonomy section includes both tier definitions and spec 001 is relabeled.

- [x] T006 [US5] Update taxonomy section in specs/STATUS.md to add two-tier acceptance convention: "feature-complete" (all major capabilities present, AC gaps remain) and "spec-complete" (all acceptance criteria met) alongside existing implementation tiers (FR-012)
- [x] T007 [US5] Update spec 001 entry in specs/STATUS.md to add acceptance status "feature-complete" with documented gaps: FR-023 (output validation — note: SKILL.md has it but template instructions pending), FR-025 (per-FR citation instructions), FR-026 (per-file attribution instructions). Apply acceptance labels to specs 002, 003, 004 as well (FR-013, FR-009). (Spec 005 entry deferred to T012a, Phase 3)

**Checkpoint**: Two-tier convention defined and applied to all 4 specs. STATUS.md taxonomy is authoritative.

---

## Phase 3: US3 + US8 + US9 + US11 — STATUS.md Enrichment (Priority: P1/P3)

**Purpose**: Complete STATUS.md as the single-document cross-spec reference

**Goal**: Add shared subsystem tracking, dependency map, risk-of-gap statements, effort estimates, and SKILL.md structure plan.

**Independent Test**: An implementor can determine status of any spec, subsystem, or dependency by reading specs/STATUS.md alone.

**Note**: All tasks edit the same file (specs/STATUS.md) — execute sequentially within this phase.

### Implementation

- [x] T008 [US3] Add "Shared Subsystems" section to specs/STATUS.md with three entries. Also add a maintenance note at the bottom: "This document MUST be updated when any spec's implementation or acceptance status changes." (FR-008a). Entries: (1) Dispute-Parsing Subsystem — SKILL.md section "Dispute-Parsing Subsystem", stable, consumers: 001, 002; (2) Structural Markers — with sub-entries for `DISPUTES_BEGIN/END` (consumers: 001, 002, synthesis templates) and `TEMPLATE_STATUS` (consumers: 005, all arbitration templates), stable; (3) Template Conventions — {VARIABLE} substitution, mode-specific templates, stable, consumers: all specs (FR-008). Also note under spec 002 entry: stagnation detection does not support structural-marker parsing (only heading-based), and heading-match semantics for dispute-parsing fallback are not explicitly specified.
- [x] T009 [US3] Add "Cross-Spec Dependencies" section to specs/STATUS.md showing dependency graph and recommended implementation order: 001 → 004 → 002 → 003, with rationale for ordering. Note: this section summarizes the per-spec "Depends On" fields — per-spec entries are authoritative (FR-008)
- [x] T010 [US8] Add "Risk-of-Gap" field to each spec entry in specs/STATUS.md: 001 = disputes remain unresolved, manual post-processing needed; 002 = single-pass deliberation only, no iterative convergence; 003 = users must manually configure conversus.yml, no guided workflow; 004 = agent definitions copy-pasted across configs, no reuse (FR-016)
- [x] T011 [US9] Add "Effort" field to each spec entry in specs/STATUS.md: 001 = Small (2 FRs remain, template-level instructions); 002 = None (complete); 003 = Large (5 new commands, Phase A/B/C delivery); 004 = Small (3 FRs for discovery CLI commands); 005 = Small (9 FRs, documentation edits only) (FR-017)
- [x] T012 [US11] Add "SKILL.md Structure Plan" section to specs/STATUS.md documenting how SKILL.md accommodates future specs: 002 = already integrated (rounds, cross-round synthesis, dispute-parsing subsystem sections); 003 = needs new Subcommand Dispatch section before Step 1, entry point routing, Phase A/B/C orchestration; 004 = already integrated (preset resolution in Step 1 config parsing) (FR-019)
- [x] T012a [US3] Add spec 005 entry to specs/STATUS.md with implementation status, acceptance status, key gaps, risk-of-gap, and effort estimate. Required by SC-003 ("status of any spec") (FR-008). Label spec 005 implementation status based on FRs completed at time of writing. If major capabilities are still pending and the gap list is unstable, label acceptance as "Not assessed." If all major capabilities are present with enumerable gaps, label as "Feature-complete" with gaps listed. Update both labels in Phase 5 (T016/T017).

**Checkpoint**: STATUS.md is the complete cross-spec reference with status for all 5 specs, subsystems, dependencies, risk, effort, and structure plan.

---

## Phase 4: US4 + US2 + US6 + US7 — SKILL.md Documentation (Priority: P1/P3)

**Purpose**: Add missing documentation to SKILL.md Phase 6 section

**Goal**: Explicit heading match semantics, Phase 4 missing document handling, and Phase 6 overwrite behavior.

**Independent Test**: SKILL.md Phase 6 section contains all three documentation additions.

**Note**: All tasks edit the same file (SKILL.md) — execute sequentially within this phase.

### Implementation

- [x] T019 [US4] In SKILL.md Round Termination Check section (the paragraph beginning "Read the current round's synthesis"), replace the inline dispute-counting specification with a cross-reference to the Dispute-Parsing Subsystem section. Execute BEFORE T019a and T013-T015 (edits flow downward in the file). (FR-011a — stagnation detection)
- [x] T019a [US4] In SKILL.md Trigger Evaluation section (L531-542), replace the inline disputes_remain parsing logic and mode-specific heading list with a cross-reference to the Dispute-Parsing Subsystem's boolean output. Retain `trigger: always` logic (no parsing needed) and the v1 cooperative-only note. Execute AFTER T019, BEFORE T013. (FR-011b — trigger evaluation)
- [x] T013 [US2] In SKILL.md output validation section (after the paragraph beginning "After Phase 6 completes successfully, validate that"), append as new sentence: heading validation is case-insensitive, scoped to heading lines (lines starting with `#`), and heading-level prefix is irrelevant (e.g., `## Process Note` and `### Process Note` both satisfy the "Process Note" check). Note: the headings validated here correspond to those instructed by `templates/cooperative/arbitration.md` — if the template's heading instructions change, update this list. (FR-007). **Verify**: spec.md US2 AS1-AS4.
- [x] T014 [US6] In SKILL.md Phase 6 section, add new paragraph before the failure handling list (before "If the Phase 6 agent fails"): "If a Phase 4 dispute document is missing or empty, Phase 6 proceeds with the available dispute documents. An empty disputes document means that agent has no remaining disputes." (FR-014). **Verify**: spec.md US6 AS1.
- [x] T015 [US7] In SKILL.md Phase 6 section, add after output validation as cross-reference: "Phase 6 follows the general overwrite semantics described in Important Notes: re-running overwrites any existing resolution.md." (FR-015). **Verify**: spec.md US7 AS1.

**Checkpoint**: SKILL.md Phase 6 section is complete with all edge cases, match semantics, and overwrite behavior documented.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and cleanup

- [x] T016 Verify all 19 FRs (including FR-011 remediation) are satisfied by reading specs/STATUS.md and SKILL.md Phase 6 section against the FR list in specs/005-p2p3-backlog-hardening/spec.md
- [x] T017 Update timestamp at bottom of specs/STATUS.md to reflect current date. Verify STATUS.md contains a maintenance note stating the update obligation per FR-008a.
- [x] T018 Run quickstart.md verification checklist from specs/005-p2p3-backlog-hardening/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — verification only, all tasks [P]
- **Foundational (Phase 2)**: Depends on Phase 1 verification passing — defines taxonomy used by Phase 3
- **STATUS.md Enrichment (Phase 3)**: Depends on Phase 2 (taxonomy must be defined before applying labels)
- **SKILL.md Additions (Phase 4)**: Depends on Phase 1 — independent of Phases 2-3 (different file)
- **Polish (Phase 5)**: Depends on Phases 3 and 4 both being complete

### User Story Dependencies

- **US1 (Draft Template Safety Gate)**: Already done — verified in Phase 1
- **US2 (Output Validation)**: Phase 1 verifies FR-004/005/006; Phase 4 adds FR-007
- **US3 (Status Tracking)**: Phase 3 — depends on US5 (taxonomy)
- **US4 (Dispute-Parsing Spec)**: FR-010 done (Phase 1); FR-011 partial — remediated by T019 in Phase 4
- **US5 (Two-Tier Convention)**: Phase 2 — foundational, no dependencies on other stories
- **US6 (Phase 4 Edge Case)**: Phase 4 — independent of STATUS.md work
- **US7 (Overwrite Semantics)**: Phase 4 — independent of STATUS.md work
- **US8 (Risk-of-Gap)**: Phase 3 — depends on US5 (taxonomy labels)
- **US9 (Effort Estimates)**: Phase 3 — depends on US5 (taxonomy labels)
- **US10 (Baseline Features)**: Already done — verified in Phase 1
- **US11 (Structure Plan)**: Phase 3 — depends on US3 (subsystem context)

### Parallel Opportunities

- **Phase 1**: All 5 verification tasks (T001-T005) run in parallel — different file sections
- **Phase 3 + Phase 4**: These phases edit different files (STATUS.md vs SKILL.md) and can run in parallel
- **Within Phase 3**: Tasks T008-T012 edit the same file — must be sequential
- **Within Phase 4**: Tasks T019, T019a, T013-T015 edit the same file — must be sequential (T019 first, then T019a, then T013-T015)

---

## Parallel Example: Phases 3 + 4

```bash
# Phase 3 and Phase 4 can run concurrently (different files):

# Agent A: STATUS.md enrichment (Phase 3)
Task: "Add Shared Subsystems section to specs/STATUS.md"
Task: "Add Cross-Spec Dependencies section to specs/STATUS.md"
Task: "Add Risk-of-Gap to each spec in specs/STATUS.md"
Task: "Add Effort estimates to each spec in specs/STATUS.md"
Task: "Add SKILL.md Structure Plan section to specs/STATUS.md"

# Agent B: SKILL.md additions (Phase 4)
Task: "Add heading match semantics to SKILL.md output validation"
Task: "Add Phase 4 missing document edge case to SKILL.md"
Task: "Add Phase 6 overwrite semantics to SKILL.md"
```

---

## Implementation Strategy

### MVP First (Phase 2 — Two-Tier Convention)

1. Complete Phase 1: Verify pre-existing FRs (5 min)
2. Complete Phase 2: Define taxonomy (US5) — this is the foundational piece
3. **STOP and VALIDATE**: STATUS.md taxonomy is correct and applied to all 4 specs
4. This alone resolves the labeling disagreement from the self-audit

### Incremental Delivery

1. Phase 1 → Verification passes → confidence that 11 FRs are intact
2. Phase 2 → Two-tier convention applied → labeling clarity (US5)
3. Phase 3 → STATUS.md enriched → complete implementor reference (US3, US8, US9, US11)
4. Phase 4 → SKILL.md additions → complete Phase 6 documentation (US2, US6, US7)
5. Phase 5 → Polish → all 19 FRs verified

### Single-Developer Strategy

Since this is a documentation-only feature with small scope:

1. Do Phases 1-2 first (verification + taxonomy) — ~10 tasks
2. Do Phase 3 (STATUS.md) — 5 sequential edits to one file
3. Do Phase 4 (SKILL.md) — 3 sequential edits to one file
4. Do Phase 5 (final verification) — 3 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US1, US4, US10 are already complete — Phase 1 verifies them only
- All implementation tasks (T006-T015, T019) edit only 2 files: `specs/STATUS.md` and `SKILL.md`
- Commit after each phase for clean git history
- Each phase is independently verifiable against the spec's acceptance scenarios
