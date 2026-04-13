# Tasks: Status Taxonomy Updates

**Input**: Design documents from `/specs/007-status-taxonomy-updates/`
**Prerequisites**: plan.md (required), spec.md (required)

**Tests**: Not requested — no test tasks generated.

**Organization**: Tasks grouped by target file. All changes are additive edits to existing Markdown files.

**Convention**: Mark completed tasks with `- [x]`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

---

## Phase 1: Taxonomy Additions (STATUS.md)

**Purpose**: Make the taxonomy section authoritative by adding missing definitions

- [x] T001 [P] [US1] Add "Not assessed" acceptance label to specs/STATUS.md Acceptance Tier section: `- **Not assessed**: No acceptance criteria have been evaluated.` Definition must not reference implementation state. (FR-001, FR-002)

- [x] T002 [P] [US3] Add compound-label permission rule to specs/STATUS.md Implementation Tier section: "Specs with independently-implementable subsystems may use compound labels composed of existing tier values. Each component must use a defined implementation-tier label." (FR-006, FR-007)

- [x] T003 [P] [US1] Add gap documentation convention note to specs/STATUS.md taxonomy section: "Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability." (FR-012)

**Checkpoint**: Taxonomy section defines all three acceptance labels, permits compound implementation labels, and specifies gap documentation format.

---

## Phase 2: Spec Entry Edits (STATUS.md)

**Purpose**: Apply taxonomy changes to spec entries

- [x] T004 [US1] Relabel spec 003's acceptance field in specs/STATUS.md from "Not started" to "Not assessed". (FR-003)

- [x] T005 [US2] Add Gaps line to spec 004's entry in specs/STATUS.md: `**Gaps**: FR-022 (preset list command), FR-023 (preset filter command), FR-024 (preset detail command) — discovery features not started; acceptance scenarios US-3 through US-6 not testable.` Format consistent with spec 001. (FR-004, FR-005)

- [x] T006 [US3] Verify spec 004's existing compound label ("Implementation-complete (core) / Not started (discovery)") complies with the compound-label rule added in T002. No modification needed — verification only. (FR-008)

**Checkpoint**: All spec entries use defined taxonomy labels. Spec 004 has gap documentation matching spec 001's format.

---

## Phase 3: tasks.md Annotations (Phase 3 Readiness)

**Purpose**: Prepare task descriptions for Phase 3 contributors

- [x] T007 [P] [US4] Annotate T007 in specs/005-p2p3-backlog-hardening/tasks.md with spec 005 exclusion: append "(Spec 005 entry deferred to T012a, Phase 3)". (FR-009)

- [x] T008 [P] [US4] Add labeling guidance to T012a in specs/005-p2p3-backlog-hardening/tasks.md: instructions for choosing spec 005 implementation and acceptance labels based on FR completion state. (FR-010)

**Checkpoint**: Phase 3 contributors have explicit guidance for T007 scope and T012a labeling.

---

## Phase 4: Verification

**Purpose**: Confirm all taxonomy and entry changes are consistent

- [x] T009 [US1] Verify every acceptance label used in specs/STATUS.md spec entries is defined in the taxonomy section. Expected: "Feature-complete", "Spec-complete", "Not assessed" — all defined. (FR-015)

- [x] T010 [US1] Verify every spec entry in specs/STATUS.md has both an implementation-tier and an acceptance-tier label. Expected: all 5 specs (001-005) have both. (FR-016)

- [x] T011 Verify post-conditions are recorded in Phase 2 gate summary: (a) transition criteria for T008 (FR-011 at L202), (b) FR-023 update after T013 (FR-013 at L212), (c) spec 002 re-evaluation after T019 (FR-014 at L214). Verification only — content already present.

**Checkpoint**: All 16 FRs satisfied. STATUS.md taxonomy is authoritative.

---

## Dependencies & Execution Order

- **Phase 1**: All three taxonomy tasks [P] run in parallel — different sections of the same file
- **Phase 2**: Depends on Phase 1 (labels must be defined before applying)
- **Phase 3**: Independent of Phases 1-2 (different file) — can run in parallel with Phase 2
- **Phase 4**: Depends on all prior phases (verification)

---

## Notes

- All tasks edit only 2 files: `specs/STATUS.md` and `specs/005-p2p3-backlog-hardening/tasks.md`
- Post-conditions (FR-011, FR-013, FR-014) are already recorded in the Phase 2 gate summary — no edits needed, verification only
- All tasks are marked [x] because implementation was completed inline during the spec 007 session
