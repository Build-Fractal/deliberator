# Implementation Plan: P2/P3 Backlog Hardening

**Branch**: `005-p2p3-backlog-hardening` | **Date**: 2026-03-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-p2p3-backlog-hardening/spec.md`

## Summary

Close documentation and validation gaps identified by the conversus self-audit. 10 of 19 FRs are fully implemented, 1 is partial (FR-011). Remaining work: enrich `specs/STATUS.md` with two-tier status labels, shared subsystem tracking, risk/effort assessments, and a SKILL.md structure plan; add documentation notes to SKILL.md Phase 6 section; add Round Termination cross-reference for FR-011.

## Technical Context

**Language/Version**: Markdown (specification documents, no code)
**Primary Dependencies**: None — all changes are to `.md` specification files
**Storage**: N/A — file-based documentation
**Testing**: Manual verification against FR acceptance criteria
**Target Platform**: Agent runtime (Claude Code) consuming SKILL.md as orchestration spec
**Project Type**: Agent skill specification (prompt-driven orchestration)
**Performance Goals**: N/A — documentation changes only
**Constraints**: Changes must not break existing SKILL.md behavior; STATUS.md must remain a useful single-document reference
**Scale/Scope**: 2 files modified (`specs/STATUS.md`, `SKILL.md`), 0 files created

## Constitution Check

*No constitution file found at `.specify/memory/constitution.md`. Gate skipped.*

## Project Structure

### Documentation (this feature)

```text
specs/005-p2p3-backlog-hardening/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: FR state analysis
├── data-model.md        # Phase 1: document entity model
├── quickstart.md        # Phase 1: implementation summary
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
conversus/
├── SKILL.md                    # Modified: 4 documentation edits (3 in Phase 6 section, 1 in Round Termination)
└── specs/
    └── STATUS.md               # Modified: enriched with 5 new sections
```

**Structure Decision**: No new files. All changes are targeted edits to two existing Markdown files. No source code directories apply — this is a documentation-only feature.

## Implementation Approach

### What's Already Done (10 FRs — no action needed)

| FR | What | Where |
|----|------|-------|
| FR-001 | Draft markers in templates | `templates/{mode}/arbitration.md` line 1 |
| FR-002 | Draft check in Step 3 | SKILL.md Step 3 template loading |
| FR-003 | Check before variable substitution | SKILL.md Step 3 (precedes Step 4) |
| FR-004 | Output validation | SKILL.md Phase 6 output validation section |
| FR-005 | Warning on missing headings | SKILL.md Phase 6 output validation section |
| FR-006 | Non-blocking validation | SKILL.md Phase 6 output validation section |
| FR-010 | Dispute-parsing shared spec | SKILL.md section "Dispute-Parsing Subsystem" |
| FR-018 | Baseline features documented | SKILL.md section "Baseline Features" |

### What's Partially Done (1 FR)

| FR | What | Where | Gap |
|----|------|-------|-----|
| FR-011 | Specs reference shared parsing | `specs/STATUS.md` spec 002 entry, SKILL.md L453-469, SKILL.md L531-542 | Two consumers use inline parsing instead of referencing Dispute-Parsing Subsystem: (a) Round Termination Check — inline dispute-counting, (b) Trigger Evaluation — inline heading-based parsing with mode-specific heading list |

### What Remains (9 FRs — 2 files to modify)

#### Group A: STATUS.md Enrichment (6 FRs)

**File**: `specs/STATUS.md`

1. **FR-009 + FR-012 + FR-013**: Add two-tier status convention
   - Add "Taxonomy" section explaining feature-complete vs spec-complete alongside existing implementation tiers
   - Update spec 001 label to include "feature-complete" classification
   - Apply convention to all 4 specs

2. **FR-008**: Add shared subsystem tracking section
   - Document dispute-parsing subsystem (SKILL.md L641-666, stable, consumers: 001, 002)
   - Document structural markers (stable, consumers: 001, 002, 005)
   - Document template conventions (stable, consumers: all)

3. **FR-016**: Add risk-of-gap statement per spec
   - 001: Disputes remain unresolved; manual post-processing needed
   - 002: Single-pass deliberation only; no iterative convergence improvement
   - 003: Users must manually configure conversus.yml; no guided workflow
   - 004: Agent definitions copy-pasted across configs; no reuse mechanism

4. **FR-017**: Add effort estimates per spec
   - 001: Small — 3 FRs remain (FR-023 engine logic exists but template instructions pending; FR-025/026 are template instructions)
   - 002: Complete — 0 remaining
   - 003: Large — 5 new commands, Phase A/B/C delivery
   - 004: Small (discovery) — 3 FRs for CLI list/filter/detail commands

5. **FR-019**: Add SKILL.md structure plan section
   - 002: Already integrated (rounds/stagnation at L34-35, cross-round synthesis, dispute-parsing subsystem)
   - 003: Needs new "Subcommand Dispatch" section before Step 1, entry point routing, Phase A/B/C orchestration logic
   - 004: Already integrated (preset resolution in Step 1 L92-174)

#### Group B: SKILL.md Phase 6 Documentation (2 FRs)

**File**: `SKILL.md`

1. **FR-007**: Add explicit heading match semantics to output validation (after L581)
   - Specify case-insensitive matching
   - Specify substring matching within heading lines (## or ### prefix acceptable)

2. **FR-014**: Add Phase 4 missing document edge case note (after L574 or before failure handling)
   - "If a Phase 4 dispute document is missing or empty, Phase 6 proceeds with available documents."

3. **FR-015**: Add Phase 6 overwrite semantics (near failure handling section)
   - "Phase 6 arbitration follows the same overwrite semantics: re-running overwrites any existing resolution.md."

### Implementation Order

1. **STATUS.md enrichment** — all Group A items in a single pass (FR-008, FR-009, FR-012, FR-013, FR-016, FR-017, FR-019)
2. **SKILL.md additions** — all Group B items in a single pass (FR-007, FR-011, FR-014, FR-015)

This order ensures STATUS.md (the living reference) is complete before SKILL.md behavioral documentation is tightened.

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| STATUS.md becomes stale after creation | Medium | Low | Document update obligation in STATUS.md itself |
| Two-tier convention conflicts with existing taxonomy | Low | Medium | Integrate rather than replace; research.md documents decision |
| SKILL.md additions change engine behavior | Low | Minor | FR-007 adds explicit matching semantics that refine existing behavior. In a prompt-orchestrated system, SKILL.md text changes are specification changes. |

## Complexity Tracking

No complexity violations. All changes are documentation edits to existing files. No new abstractions, no new files, no behavioral changes.
