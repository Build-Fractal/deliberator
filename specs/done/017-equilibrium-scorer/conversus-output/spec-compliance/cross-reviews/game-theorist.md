# Phase 2 Cross-Review: spec-compliance reviews game-theorist

**Spec**: 017-equilibrium-scorer
**Reviewer**: spec-compliance
**Reviewing**: game-theorist's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **nashopt never called**: game-theorist's identification of this gap aligns with my FR-005 NOT MET finding. game-theorist adds valuable context: the `solver` field is misleading.

2. **WTA magic threshold**: Valid concern. From a compliance perspective, the spec (Section 2.2) says "A loser is at equilibrium only if its criterion scores could not surpass the winner's." The threshold-based heuristic is an approximation of this, but the 2.0 value is not derived from the spec. The spec does not mandate a specific method, so this is implementation discretion, but the lack of documentation or configurability is a quality issue.

3. **PD strategic interaction gap**: game-theorist notes this is "acceptable for v1." From a compliance standpoint, the spec says "Agent i's payoff is claimed territory minus penalty for overreach." The implementation correctly computes this formula. The best-response heuristic is an implementation detail not constrained by the spec, so this is not a compliance issue.

## Points to Add

1. **Red-Blue payoff alignment with spec**: game-theorist assesses the adversarial model as "sound." I want to verify compliance with the spec formulas:
   - Spec: `J_red = sum(severity * confirmed_findings)`. Implementation: `severity_sum * confirmed_ratio`. This approximates the sum with a ratio-based calculation. The spec implies a per-finding sum, while the implementation uses an aggregate ratio. This is a reasonable simplification when per-finding data is unavailable, but it's a deviation from the literal spec.
   - Spec: `J_blue = sum(severity * mitigated_findings)`. Implementation uses `red_severity * mitigated_ratio`, which tracks blue's payoff relative to red's total severity. This is a valid interpretation.

2. **Heuristic fallback reasonableness**: game-theorist correctly assesses all four heuristics as "reasonable." From a compliance perspective, the spec's FR-005 envisions nashopt doing the heavy lifting, with heuristics as an unspecified fallback. The spec does not define what the heuristic should look like, so the implementation has latitude here.

## Disagreement

None. game-theorist's mathematical analysis complements the compliance review effectively.
