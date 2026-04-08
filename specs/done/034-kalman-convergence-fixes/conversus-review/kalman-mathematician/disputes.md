# Kalman-Mathematician — Phase 4 Disputes

## Resolved Disputes

All cross-review challenges were resolved in Phase 3 revisions:

1. **F-9 priority**: Upgraded to P1 — consensus reached.
2. **F-4 scoping**: Reclassified as REQUIRED-ELSEWHERE — consensus reached.
3. **SC-004 criteria**: Enhanced test requirements accepted.
4. **test inversion (C-3)**: Accepted as P2 compliance gap.

## Remaining Disputes

### DISPUTE-1: R[2][2] calibration basis

**Position**: The current R[2][2] = 0.05 is calibrated to 10x the concession_rate noise. However, this assumes the equilibrium score has 10x more measurement noise than concession rate. If the EquilibriumScorer uses the heuristic path (not nashopt), the actual noise could be higher (heuristic payoff comparisons are coarser than exact solver). The R value should be conditional on the solver path used.

**Counter-argument expected**: The spec says "Recommended: 0.05" without distinguishing solver paths. The calibration is for the general case.

**Priority**: P3 — academic concern, not blocking.

## Convergence Assessment

All substantive disputes are resolved. No P1 or P2 disputes remain. The one remaining dispute (R calibration basis) is P3 and does not block convergence.

**Status**: CONVERGED.
