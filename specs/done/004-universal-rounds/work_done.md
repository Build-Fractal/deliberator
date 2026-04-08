# Work Done: Spec 004 — Universal Rounds, Stagnation, and Arbitration

**Branch**: `004-universal-rounds`
**Date**: 2026-03-20

## Summary

Extended `rounds > 1`, `stagnation: detect`, and `arbiter` from cooperative-only to all four competition modes (red-blue, winner-take-all, prisoners-dilemma).

## Changes Made

### SKILL.md (4 edits)

| Change | FR | Details |
|--------|-----|---------|
| Removed arbiter mode restriction | FR-001 | Deleted: `"arbiter is only supported in cooperative mode"` validation rule |
| Removed rounds mode restriction | FR-001 | Deleted: `"rounds > 1 is only supported in cooperative mode"` validation rule |
| Updated Phase 6 forward-compat note | FR-001 | Replaced v1-restriction note with: "Arbitration is supported for all four modes" |
| Added mode-specific Phase 6 validation headings | FR-009 | Replaced single heading list with mode-keyed table matching actual template headings |

### Templates — Draft Markers Removed (3 files)

| File | FR |
|------|-----|
| `templates/red-blue/arbitration.md` | FR-006 |
| `templates/winner-take-all/arbitration.md` | FR-007 |
| `templates/prisoners-dilemma/arbitration.md` | FR-008 |

### Templates — Created (3 new files)

| File | FR | Key Framing |
|------|-----|-------------|
| `templates/red-blue/cross-round-synthesis.md` | FR-003 | Risk trajectory, attack pattern shifts, defense effectiveness, final risk register |
| `templates/winner-take-all/cross-round-synthesis.md` | FR-004 | Ranking trajectory, proposal evolution, final ranking and selection |
| `templates/prisoners-dilemma/cross-round-synthesis.md` | FR-005 | Boundary trajectory, cooperation dynamics, tit-for-tat emergence, final boundary map |

## FR Coverage

| FR | Status | Notes |
|----|--------|-------|
| FR-001 | Done | Both validation rules removed |
| FR-002 | Already done | Dispute-Parsing Subsystem already defines mode-specific headings |
| FR-003 | Done | Red-blue cross-round-synthesis template created |
| FR-004 | Done | Winner-take-all cross-round-synthesis template created |
| FR-005 | Done | Prisoners-dilemma cross-round-synthesis template created |
| FR-006 | Done | Red-blue arbitration template un-drafted |
| FR-007 | Done | Winner-take-all arbitration template un-drafted |
| FR-008 | Done | Prisoners-dilemma arbitration template un-drafted |
| FR-009 | Done | Mode-specific Phase 6 validation headings added to SKILL.md |
| FR-010 | Verified | Round-aware variables are populated generically by the orchestrator — no mode gate exists |

## Additional Fixes (from constitution review + test run)

| Fix | Source |
|-----|--------|
| Removed stale "cooperative mode only" comment from SKILL.md L34 YAML schema | Constitution review (P1) |
| Fixed WTA cross-round-synthesis heading: `Remaining Contested Positions` → `Remaining Disputes` | Constitution review (Principle II violation) |
| Fixed PD cross-round-synthesis heading level: `### Remaining Disputed Boundaries` → `## Disputed Boundaries` | Constitution review (Principle II violation) |

## Test Run: 3-Mode Multi-Round Deliberation

Exercised all changes with a 3-mode parallel conversus run targeting the spec 004 implementation itself.

### Configuration

| Mode | Agents | Rounds | Stagnation | Arbiter |
|------|--------|--------|------------|---------|
| Red-Blue | attacker (red), defender (blue) | 3 max | detect | conversus-engine, constitution grounding |
| Winner-Take-All | template-approach, engine-approach | 3 max | detect | conversus-engine, constitution grounding |
| Prisoners-Dilemma | engine-owner, template-owner | 3 max | detect | conversus-engine, constitution grounding |

### Results

| Mode | Rounds Used | Termination | Disputes R1 | Disputes R2 | Arbiter Triggered |
|------|-------------|-------------|-------------|-------------|-------------------|
| Red-Blue | 2/3 | Converged | 3 (severity) | 0 | No (no disputes) |
| Winner-Take-All | 2/3 | Converged | 3 (minor) | 0 | No (no disputes) |
| Prisoners-Dilemma | 2/3 | Converged | 2 (governance) | 0 | No (no disputes) |

**Total agents launched: 69** across 3 modes × 2 rounds + 3 cross-round syntheses.

### Key Findings from Red-Blue Stress Test

The red-team attacker found a **critical template gap** that the implementation missed:

| Threat | Severity | Finding |
|--------|----------|---------|
| THREAT-01 | **CRITICAL** | Non-cooperative Phase 1 review templates lack `{PRIOR_ROUND_SECTION}` — Round 2+ agents won't read prior round synthesis |
| THREAT-10 | **HIGH** | Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers |
| THREAT-02 | **MEDIUM** | Non-cooperative arbitration templates omit `{REMAINING_DISPUTES}` extraction section |
| THREAT-04 | **MEDIUM** | Spec FR-009 heading names diverge from actual template/SKILL.md headings |
| THREAT-05 | **MEDIUM** | WTA stagnation fallback causes `trigger: disputes_remain` to degrade to `trigger: always` |
| THREAT-06 | **LOW** | WTA dispute entry pattern undefined for counting |

**Verdict**: Engine is correct. Templates need completeness fixes before non-cooperative multi-round runs are production-ready.

### Winner-Take-All Verdict

**Winner: template-approach** (template-first architecture). The engine-approach conceded in Round 1 Phase 3, repositioning as enhancements within template-first. Five runner-up contributions adopted (mode interface contract docs, heading validation tool spec, role enforcement acknowledgment).

### Prisoners-Dilemma Boundary Map

Full cooperation across both rounds. 21 boundaries resolved: 11 engine-exclusive, 6 template-exclusive, 4 shared interfaces with bilateral governance protocols.

### Output Location

All deliberation artifacts at `specs/004-universal-rounds/test/{red-blue,winner-take-all,prisoners-dilemma}/`:
- `round-1/` — Round 1 artifacts (reviews, cross-reviews, revisions, disputes, synthesis)
- `round-2/` — Round 2 artifacts
- `summary/final.md` — Cross-round synthesis (start here)

## What Did NOT Change

- Cooperative mode behavior — untouched
- Single-round execution — untouched
- Round loop mechanics — unchanged
- `iterations` field — continues to work orthogonally
- Phase 1-5 templates for any mode — unchanged
- Dispute-Parsing Subsystem — unchanged (already mode-aware)
