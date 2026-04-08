# Phase 2 Cross-Review: plugin-engineer reviews game-theorist

**Spec**: 017-equilibrium-scorer
**Reviewer**: plugin-engineer
**Reviewing**: game-theorist's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **nashopt integration gap**: game-theorist correctly identifies that `nashopt.check_equilibrium()` is never called despite being imported. This is also visible from the plugin engineering side -- the `solver` field in output data switches between "nashopt" and "heuristic" based on import availability, but the computation path is identical. This is a bug that affects output integrity.

2. **Magic threshold (2.0) in WTA**: Valid concern. From an engineering perspective, this should at minimum be a named constant, and ideally a configurable parameter in the plugin config. The current hardcoded 2.0 is buried in the payoff function with only a code comment for justification.

3. **PD best-response simplification**: I accept game-theorist's assessment that this is adequate for v1. The function correctly computes the territory formula and the overreach penalty. The best-response estimate being a solo-optimal upper bound rather than a strategic best response is a documented limitation, not a defect.

## Points to Add

1. **Cooperative payoff concern -- concession_rate comment**: game-theorist notes "We also factor in concession rate as a cost" but the actual code does NOT use concession_rate in the cooperative payoff computation. The docstring mentions it but the code only uses `surviving_count`. This is a code/documentation mismatch, not a math issue, but worth flagging.

2. **Red-blue total_surface edge case**: If `total_surface == 0` (no attacks landed, mitigated, or accepted), the code falls through to `payoff = severity_sum` for red and `payoff = 0.0` for blue. This asymmetry is questionable -- if there were no attacks at all, should red get full payoff while blue gets zero? This might produce misleading equilibrium scores in edge cases.

## Disagreement

None. game-theorist's mathematical analysis is precise and well-evidenced.
