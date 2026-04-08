# Quickstart: P2/P3 Backlog Hardening

**Branch**: `005-p2p3-backlog-hardening` | **Date**: 2026-03-20

## What This Feature Does

Closes documentation and validation gaps identified by the conversus self-audit (14-agent, 6-phase run). Adds status tracking, enriches cross-spec metadata, and hardens SKILL.md with missing edge case documentation.

## Implementation Summary

**10 of 19 FRs are fully implemented, 1 is partial (FR-011).** The remaining 9 FRs are targeted documentation updates:

### Files to Modify

1. **`specs/STATUS.md`** — Enrich with two-tier status labels, shared subsystem tracking, risk-of-gap assessments, effort estimates, cross-spec dependency map, and SKILL.md structure plan
2. **`SKILL.md`** — Add heading match semantics to output validation (FR-007), Phase 4 missing document edge case (FR-014), Phase 6 overwrite semantics (FR-015)

### No Files to Create

All target files already exist. This is purely an enrichment/documentation task.

## Verification

After implementation, verify:

1. `specs/STATUS.md` contains:
   - Two-tier status labels for all 4 specs
   - Shared subsystem section with stability status
   - Risk-of-gap statement per spec
   - Effort estimate per spec
   - SKILL.md structure plan section

2. `SKILL.md` Phase 6 section contains:
   - Explicit case-insensitive heading matching note
   - Phase 4 missing document graceful handling note
   - Phase 6 overwrite semantics note

## Implementation Order

1. STATUS.md enrichment (FR-008, FR-009, FR-012, FR-013, FR-016, FR-017, FR-019)
2. SKILL.md Phase 6 documentation additions (FR-007, FR-014, FR-015)
