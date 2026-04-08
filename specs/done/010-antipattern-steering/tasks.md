# Tasks: Agent Antipattern Steering

**Input**: Design documents from `/specs/010-antipattern-steering/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/catalog-format.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- This feature is pure markdown/documentation — no `src/` or `tests/` directories
- All paths are relative to the conversus project root

---

## Phase 1: Setup

**Purpose**: Create directory structure for the antipattern catalog

- [x] T001 Create `antipatterns/` directory at the conversus project root (adjacent to `presets/`, `templates/`, `specs/`)

**Checkpoint**: Directory exists, ready for catalog file creation

---

## Phase 2: User Story 1 — Record Observed Antipatterns (Priority: P1) MVP

**Goal**: Create a structured antipattern catalog seeded with the "redundant-cache" entry so maintainers can record and browse observed agent behavioral mistakes.

**Independent Test**: Open `antipatterns/catalog.md`, read the Summary Index, then read the full `redundant-cache` entry. Verify: (1) the entry is self-contained — a reader unfamiliar with the incident can understand the antipattern, (2) symptoms are specific enough to match against future work, (3) correction is actionable.

- [x] T002 [US1] Create `antipatterns/catalog.md` with file header (`# Antipattern Catalog`), agent instruction blockquote, and `## Summary Index` section containing an empty table with columns: Name, Summary, Keywords — follow the exact structure in `specs/010-antipattern-steering/contracts/catalog-format.md`
- [x] T003 [US1] Write the `redundant-cache` full entry section in `antipatterns/catalog.md` — adapt content from `antipatterns/examples/redundant-cache/README.md` to match the entry format defined in `specs/010-antipattern-steering/contracts/catalog-format.md`. Must include all required fields per `specs/010-antipattern-steering/data-model.md`: Status (Active), Observed (2026-03-20), Summary, Symptoms (≥2 items), Root Cause, Example (with real file/spec references to `antipatterns/examples/redundant-cache/`), Correction, When This Does NOT Apply (≥1 exclusion), Keywords (≥2 tags)
- [x] T004 [US1] Add `redundant-cache` row to the Summary Index table in `antipatterns/catalog.md` — populate Name (`redundant-cache`), Summary (one-line, <100 chars), and Keywords (comma-separated tags matching the entry's Keywords section)

**Checkpoint**: `antipatterns/catalog.md` exists with a scannable Summary Index and one complete, self-contained entry. Acceptance scenarios 1.1, 1.2, and 1.3 from spec.md are satisfied.

---

## Phase 3: User Story 2 — Agent Pre-Task Steering (Priority: P1)

**Goal**: Integrate the antipattern catalog into the agent workflow so deliberation agents check it before proposing new artifacts, closing the observation-to-prevention loop.

**Independent Test**: Read the SKILL.md Antipattern Check instruction. Verify: (1) it references `antipatterns/catalog.md`, (2) it specifies the 4-step check workflow (read index → match keywords/summary → read full entry → follow correction or proceed), (3) it's positioned so agents encounter it before phase execution.

- [x] T005 [US2] Add `### Antipattern Check` instruction block to `SKILL.md` — insert after Step 1 (config parsing), before Step 2 (output directory creation). Use the exact wording from the SKILL.md Integration Contract section of `specs/010-antipattern-steering/contracts/catalog-format.md`. The instruction must reference the catalog path `antipatterns/catalog.md` and specify the 4-step check workflow
- [x] T006 [P] [US2] Update the "Known Antipatterns" section in `.specify/memory/constitution.md` — add a reference to `antipatterns/catalog.md` as the catalog location and note that agents are instructed via SKILL.md to check it before proposing new artifacts

**Checkpoint**: SKILL.md contains the Antipattern Check instruction. Constitution references the catalog. Acceptance scenarios 2.1, 2.2, and 2.3 from spec.md are satisfied.

---

## Phase 4: User Story 3 — Contextual Retrieval (Priority: P2)

**Goal**: Enable keyword-based retrieval so agents can filter relevant antipatterns without loading the full catalog, supporting catalog growth beyond 10 entries.

**Independent Test**: Read the Summary Index Keywords column for `redundant-cache`. Search for keyword "tracking" — verify the entry is found. Search for keyword "authentication" — verify no entries match.

- [x] T007 [US3] Verify and refine keyword tags in `antipatterns/catalog.md` — ensure the `redundant-cache` entry's Keywords section contains descriptive, retrieval-friendly tags (at minimum: `tracking`, `cache`, `artifact-creation`, `status`, `deliberation-drift`, `speckit-duplication`) and that the Summary Index Keywords column exactly matches. Add any missing tags identified from the example README keywords list
- [x] T008 [US3] Extend the SKILL.md Antipattern Check instruction (added in T005) to include keyword-matching guidance — update step 2 to specify that agents can filter by matching task-derived keywords against the Summary Index Keywords column when the catalog exceeds 10 entries, reading only matched full entries. Edit in `SKILL.md`
- [x] T009 [US3] Add a `## Maintenance` section at the bottom of `antipatterns/catalog.md` documenting: (1) how to add a new entry (append section + add index row, per FR-010), (2) how to deprecate an entry (set Status to Deprecated, add Deprecation Note section, remove from Summary Index, per FR-009), (3) the constraint that entries must reference real incidents (SC-004)

**Checkpoint**: Keywords are consistent between entries and index. Retrieval workflow documented. Deprecation mechanism defined. Acceptance scenarios 3.1 and 3.2 from spec.md are satisfied.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validate completeness and consistency across all artifacts

- [x] T010 Validate `antipatterns/catalog.md` against all functional requirements — verify FR-001 through FR-010 from spec.md are satisfied: catalog exists (FR-001), entry has all required fields (FR-002), summary index present (FR-003), entry is self-contained (FR-004), keyword tags present (FR-007), append-only structure (FR-010)
- [x] T011 Validate cross-references — verify SKILL.md Antipattern Check references the correct path (`antipatterns/catalog.md`), constitution Known Antipatterns section references the catalog, and catalog entry Example section references valid paths in `antipatterns/examples/redundant-cache/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup (T001) — creates the catalog file
- **User Story 2 (Phase 3)**: Depends on US1 completion — needs catalog to exist before referencing it in SKILL.md
- **User Story 3 (Phase 4)**: Depends on US1 and US2 — refines keywords and extends SKILL.md instruction
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends only on Setup. No dependencies on other stories.
- **User Story 2 (P1)**: Depends on US1 (catalog must exist before SKILL.md can reference it). T006 (constitution update) can run in parallel with T005.
- **User Story 3 (P2)**: Depends on US1 (keywords in catalog) and US2 (SKILL.md instruction to extend). Can start after both are complete.

### Within Each User Story

- T002 → T003 → T004 (sequential: create file → add entry → add index row)
- T005 and T006 can run in parallel (different files)
- T007, T008, T009 can run in parallel (T007 edits catalog, T008 edits SKILL.md, T009 edits catalog — but T007 and T009 touch the same file, so run T007 first)

### Parallel Opportunities

- T005 and T006 (Phase 3): different files, no dependencies between them
- T008 (SKILL.md) can run in parallel with T007/T009 (catalog) in Phase 4

---

## Parallel Example: User Story 2

```bash
# Launch US2 tasks in parallel (different files):
Task: "Add Antipattern Check instruction to SKILL.md" (T005)
Task: "Update Known Antipatterns in constitution.md" (T006)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: US1 — Create catalog with seed entry (T002–T004)
3. Complete Phase 3: US2 — Add SKILL.md integration (T005–T006)
4. **STOP and VALIDATE**: Run a conversus deliberation to verify agents check the catalog
5. Deploy if ready — P1 requirements are fully satisfied

### Incremental Delivery

1. Setup → Catalog created (T001)
2. Add US1 → Catalog seeded with redundant-cache (T002–T004) → Validate independently
3. Add US2 → Agents check catalog (T005–T006) → Validate end-to-end
4. Add US3 → Keyword retrieval + maintenance docs (T007–T009) → Validate at scale
5. Polish → Cross-validate all artifacts (T010–T011)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All "files" are markdown — no compilation, no test suite, no build step
- Validation is manual: read the artifacts and verify against spec requirements
- Commit after each phase checkpoint