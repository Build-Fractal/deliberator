# Phase 4 Disputes: spec-compliance

**Spec**: 017-equilibrium-scorer
**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Phase**: 4 (Dispute Declaration)

---

## Active Disputes

### Dispute 1: FR-008 Compliance Level

**My position**: PARTIALLY MET (specific format in spec not followed)
**Opposing position**: MET (game-theorist)

**Argument**: I align with plugin-engineer. The spec contains "MUST" language with a specific filename pattern. In RFC 2119 terms, MUST means "the definition is an absolute requirement." The example `equilibrium-score-round-{N}.json` is presented as the required format, not an illustration. The actual format is defensible engineering, but the spec needs to be updated to match reality. Until then, the assessment is PARTIALLY MET.

**Proposed resolution**: Agree with plugin-engineer -- mark as PARTIALLY MET and recommend spec update.

---

## Resolved Disagreements

No other active disputes. Consensus reached on:

1. **FR-005 NOT MET**: All three reviewers agree.
2. **FR-007 PARTIALLY MET**: All three reviewers agree.
3. **Mathematical soundness of payoffs**: game-theorist's analysis accepted by all.
4. **Error handling robustness**: Confirmed by all reviewers.

---

## Concessions

I concede to game-theorist that SC-003 is MET despite thin evidence. The criterion asks for "meaningful score differentiation," and the 1.0 vs. 0.5 difference between converged and disputed outcomes is indeed meaningful. More granular tests would be nice but are not required for the SC to be met.
