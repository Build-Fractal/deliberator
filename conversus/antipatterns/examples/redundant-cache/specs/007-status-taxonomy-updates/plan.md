# Implementation Plan: Status Taxonomy Updates

**Branch**: `007-status-taxonomy-updates` | **Date**: 2026-03-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/007-status-taxonomy-updates/spec.md`

## Summary

Implement Phase 2 gate binding commitments to make STATUS.md's taxonomy authoritative: add the "Not assessed" acceptance label, add a compound-label permission rule, relabel spec 003, document spec 004 gaps, add a gap documentation convention note, annotate tasks.md for Phase 3 readiness, and record post-conditions for Phase 4.

## Technical Context

**Language/Version**: Markdown (specification documents, no code)
**Primary Dependencies**: None — all changes are to `.md` specification files
**Storage**: N/A — file-based documentation
**Testing**: Manual verification against FR acceptance criteria
**Target Platform**: Agent runtime (Claude Code) consuming STATUS.md as cross-spec reference
**Project Type**: Agent skill specification (prompt-driven orchestration)
**Constraints**: Changes must not alter existing STATUS.md structure; additions only. Post-conditions are recorded in the Phase 2 gate summary.
**Scale/Scope**: 2 files modified (`specs/STATUS.md`, `specs/005-p2p3-backlog-hardening/tasks.md`), 0 files created

## Project Structure

### Documentation (this feature)

```text
specs/007-status-taxonomy-updates/
├── plan.md              # This file
├── spec.md              # Feature specification
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Task list
```

### Source Files (repository root)

```text
conversus/
└── specs/
    ├── STATUS.md                                    # Modified: taxonomy additions + spec entry edits
    └── 005-p2p3-backlog-hardening/
        ├── tasks.md                                 # Modified: T007 and T012a annotations
        └── gates/phase-2/summary/final.md           # Post-conditions already recorded (FR-011, FR-013, FR-014)
```

**Structure Decision**: No new files. All changes are targeted edits to existing Markdown files. Post-conditions (FR-011 transition criteria, FR-013 FR-023 update, FR-014 spec 002 re-evaluation) are already recorded in the Phase 2 gate summary — verified, no edits needed.

## Implementation Approach

### What's Already Done (Post-conditions)

| FR | What | Where | Status |
|----|------|-------|--------|
| FR-011 | Transition criteria recorded as T008 input | Phase 2 gate summary L202 | Already present |
| FR-013 | FR-023 Phase 4 post-condition | Phase 2 gate summary L212 | Already present |
| FR-014 | Spec 002 re-evaluation post-condition | Phase 2 gate summary L214 | Already present |

### What Remains (13 FRs — 2 files to modify)

#### Group A: STATUS.md Taxonomy & Entry Edits (10 FRs)

**File**: `specs/STATUS.md`

1. **FR-001 + FR-002**: Add "Not assessed" to Acceptance Tier — definition must not reference implementation state
2. **FR-003**: Relabel spec 003 from "Not started" to "Not assessed"
3. **FR-004 + FR-005**: Add Gaps line to spec 004 in spec 001's format
4. **FR-006 + FR-007 + FR-008**: Add compound-label permission rule; verify spec 004 compliance (no modification needed)
5. **FR-012**: Add gap documentation convention note to taxonomy
6. **FR-015 + FR-016**: Verification — all acceptance labels defined, all entries have both tiers

#### Group B: tasks.md Annotations (2 FRs)

**File**: `specs/005-p2p3-backlog-hardening/tasks.md`

1. **FR-009**: Annotate T007 with spec 005 exclusion
2. **FR-010**: Add labeling guidance to T012a

### Implementation Order

1. **STATUS.md taxonomy edits** — all Group A items in a single pass
2. **tasks.md annotations** — both Group B items
3. **Verification pass** — FR-015 and FR-016 compliance check

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Compound-label rule invalidates existing spec 004 format | None | N/A | Rule is designed to sanction the existing format |
| Spec 003 "Not assessed" creates confusion with "Not started" | Low | Low | Labels are in different tiers (acceptance vs. implementation) |
| Gap convention note conflicts with future specs' formats | Low | Low | Note is descriptive of precedent, not prescriptive |

## Complexity Tracking

No complexity violations. All changes are documentation edits to existing files. No new abstractions, no new files, no behavioral changes.
