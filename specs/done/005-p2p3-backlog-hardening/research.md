# Research: P2/P3 Backlog Hardening

**Branch**: `005-p2p3-backlog-hardening` | **Date**: 2026-03-20
**FR Traceability**: FR numbers below correspond to spec.md as of 2026-03-20. If FRs are renumbered, this mapping must be updated.

## Implementation State Analysis

The primary research question was: "How much of this spec is already implemented?" The answer: **most of it**.

### Decision: Scope is primarily gap-fill, not greenfield

**Rationale**: The self-audit that produced these P2/P3 items ran AFTER significant implementation work had already been done on SKILL.md. Many items were implemented during the self-audit's own delivery phase (commit `944c776`). The remaining work is targeted enrichment.

**Alternatives considered**:
- Treat all 19 FRs as new work → rejected because most are already satisfied, leading to wasted effort
- Close the spec as "already done" → rejected because several FRs have genuine gaps (STATUS.md enrichment, two-tier convention, SKILL.md documentation additions)

### FR-by-FR State Assessment

| FR | Status | Evidence | Remaining Work |
|----|--------|----------|----------------|
| FR-001 (draft markers in templates) | Done | All 3 templates have `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` on line 1 | None |
| FR-002 (draft check in Step 3) | Done | SKILL.md L249 | None |
| FR-003 (check before variable substitution) | Done | SKILL.md L249 — check is in Step 3 before Step 4 execution | None |
| FR-004 (output validation) | Done | SKILL.md L581-582 | None |
| FR-005 (warning on missing headings) | Done | SKILL.md L581-582 | None |
| FR-006 (non-blocking validation) | Done | SKILL.md L581-582 | None |
| FR-007 (case-insensitive heading match) | Gap | SKILL.md output validation section says "contains required section headings" but doesn't specify: (a) matching scoped to heading lines (lines starting with `#`), (b) case-insensitivity, (c) heading-level prefix irrelevance. Note: "contains" already implies substring matching. | Add three specific matching clarifications |
| FR-008 (STATUS.md) | Partial | `specs/STATUS.md` exists with per-spec status but lacks shared subsystem tracking, cross-spec dependency map as a dedicated section | Add shared subsystem section, dependency visualization |
| FR-009 (two-tier labels in STATUS.md) | Gap | STATUS.md uses "Implementation-complete" / "Partially-complete" / "Not started" — not the feature-complete/spec-complete convention | Update taxonomy and labels |
| FR-010 (dispute-parsing shared spec) | Done | SKILL.md L641-666 — complete with input, output, parsing rules, stable-interface contract | None |
| FR-011 (specs reference shared parsing) | Partial | Spec 002 STATUS.md entry references spec 001's parsing subsystem, but SKILL.md Round Termination Check (section "Round Termination Check") still contains inline dispute-counting logic independent of the Dispute-Parsing Subsystem | Add cross-reference from Round Termination Check to Dispute-Parsing Subsystem |
| FR-012 (two-tier convention documented) | Gap | Current STATUS.md has a different three-tier taxonomy | Define and apply two-tier convention |
| FR-013 (spec 001 as feature-complete) | Gap | Spec 001 is "Partially-complete" in current taxonomy | Relabel with rationale |
| FR-014 (Phase 4 missing docs edge case) | Gap | Not in SKILL.md Phase 6 section | Add documentation note |
| FR-015 (Phase 6 overwrite semantics) | Partial | SKILL.md L670 covers general overwrite but Phase 6 isn't explicit | Add Phase 6-specific note |
| FR-016 (risk-of-gap per spec) | Gap | Not in STATUS.md | Add risk-of-gap section |
| FR-017 (effort estimates per spec) | Gap | Not in STATUS.md | Add effort estimates |
| FR-018 (baseline features documented) | Done | SKILL.md L690-702 | None |
| FR-019 (SKILL.md structure plan) | Gap | No planning document exists | Create structure plan |

### Summary

- **Already done**: 10 of 19 FRs (FR-001 through FR-006, FR-010, FR-018, and FR-003)
- **Partially done**: 1 FR (FR-011 — STATUS.md cross-reference exists but Round Termination Check uses inline parsing)
- **Remaining gaps**: 9 FRs requiring targeted updates to STATUS.md and SKILL.md

### Decision: Merge two-tier convention with existing taxonomy

**Rationale**: The current STATUS.md uses a three-tier system ("Implementation-complete", "Partially-complete", "Not started") which maps to implementation fidelity. The spec requests a two-tier system ("feature-complete", "spec-complete") which maps to acceptance-criteria coverage. These are complementary, not conflicting — the solution is to add the two-tier convention alongside the existing taxonomy, not replace it.

**Alternatives considered**:
- Replace existing taxonomy entirely → rejected because "Implementation-complete" and "Not started" carry useful information that "feature-complete" / "spec-complete" doesn't capture
- Keep both taxonomies independently → rejected as confusing; integrate them into a unified view

### Decision: STATUS.md is the right location for risk/effort assessments

**Rationale**: Risk-of-gap (FR-016) and effort estimates (FR-017) are cross-cutting concerns that apply across all specs. Putting them in individual spec files would fragment the view. STATUS.md is the single-document cross-spec tracker.

### Decision: SKILL.md structure plan goes in STATUS.md

**Rationale**: The structure plan (FR-019) describes how future spec implementations will modify SKILL.md. This is cross-cutting metadata, not a standalone document. A dedicated section in STATUS.md keeps all implementation guidance in one place.
