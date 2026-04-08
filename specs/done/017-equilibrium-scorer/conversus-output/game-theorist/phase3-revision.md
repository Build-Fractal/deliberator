# Phase 3 Revision: game-theorist

**Spec**: 017-equilibrium-scorer
**Reviewer**: game-theorist
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From plugin-engineer

1. **Cooperative payoff docstring/code mismatch**: plugin-engineer correctly identifies that the docstring mentions concession_rate as a cost factor, but the code only uses `surviving_count`. I accept this finding. The docstring at line 43-44 says "We also factor in concession rate as a cost" but no concession_rate term appears in the payoff computation. This is a documentation bug, not a math error. The payoff function is mathematically correct for the spec's formula (`J_i = recommendations_accepted_in_synthesis`). **Updated assessment**: Add finding to my review.

2. **Red-Blue total_surface=0 edge case**: plugin-engineer raises a valid concern. When `total_surface == 0`, red gets `payoff = severity_sum` while blue gets `payoff = 0.0`. This is asymmetric and arguably wrong: if no attacks occurred, neither team should score as if they achieved their objective. **Updated assessment**: I now flag this as a mathematical concern. The fallback should set both payoffs to 0.0 when there is no attack surface to measure against.

### From spec-compliance

1. **Red-Blue spec alignment**: spec-compliance notes the per-finding sum vs. ratio-based approximation difference. I agree this is a reasonable simplification given the available data structure. AgentFeatures provides `severity_vector` (per-finding) and round-level aggregate counts. The ratio approach is the natural way to combine these. Not a mathematical error, but a documented approximation.

2. **FR-008 (filename format)**: I originally considered this MET. After reading spec-compliance's argument that the spec uses MUST with a specific format, I revise my position. This is a genuine spec deviation, even if the base pattern is better. **Updated assessment**: PARTIALLY MET.

---

## Updated Key Issues

1. **nashopt integration gap (critical)**: Unchanged. FR-005 is NOT MET. The scorer claims nashopt usage but never delegates to it.

2. **Magic threshold in WTA (medium)**: The 2.0 cutoff should be configurable or documented. No cross-reviewer disagreed.

3. **Red-Blue total_surface=0 asymmetry (medium, new)**: When no attacks exist, red gets full severity_sum while blue gets 0.0. Both should get 0.0 in this edge case.

4. **Cooperative docstring/code mismatch (low, new)**: Docstring claims concession_rate factoring that does not exist in code.

5. **PD strategic interaction simplification (low)**: Accepted by all reviewers as adequate for v1.

---

## Unchanged Assessments

- Cooperative payoff: Sound heuristic.
- WTA payoff structure: Correct (winner at equilibrium, losers conditional).
- PD payoff formula: Correctly implements territory - gamma * overreach.
- Red-Blue adversarial structure: Sound (minus the edge case).
- Equilibrium check logic: Correct epsilon comparison.
- Edge case handling: Well done for zero agents and payoff failures.
