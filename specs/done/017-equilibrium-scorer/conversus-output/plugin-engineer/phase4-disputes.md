# Phase 4 Disputes: plugin-engineer

**Spec**: 017-equilibrium-scorer
**Reviewer**: plugin-engineer
**Date**: 2026-03-24
**Phase**: 4 (Dispute Declaration)

---

## Active Disputes

### Dispute 1: FR-008 Compliance Level

**My position**: PARTIALLY MET (filename format differs from spec)
**Opposing position**: MET (game-theorist -- intent satisfied)

**Argument**: The spec's language is "the output filename MUST include the round number: `equilibrium-score-round-{N}.json`." The MUST keyword plus a specific format string constitutes a normative requirement. If the spec intended flexibility, it would say "MUST include the round number in the filename" without providing a specific format. The implementation's deviation is justified by engineering concerns (consistency, collision avoidance), but the spec is the governing document. The fix is to update the spec, not to retroactively declare compliance.

**Proposed resolution**: Accept PARTIALLY MET and create a follow-up to update the spec to reflect the base infrastructure's pattern.

---

## Resolved Disagreements

1. **FR-005 NOT MET**: Unanimous.
2. **FR-007 PARTIALLY MET**: Unanimous.
3. **Undocumented gamma config**: All reviewers acknowledge this is beyond spec scope. Not a compliance issue, but a documentation gap.

---

## Concessions

I concede to game-theorist on the mathematical adequacy of the heuristic payoffs. My initial concern about the PD best-response model was addressed: the upper-bound approach is standard for heuristic equilibrium checking and does not produce incorrect equilibrium/non-equilibrium classifications in the test cases provided.
