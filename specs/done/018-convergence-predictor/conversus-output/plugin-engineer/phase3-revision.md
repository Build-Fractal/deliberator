# Phase 3 Revision: plugin-engineer

**Spec**: 018-convergence-predictor
**Reviewer**: plugin-engineer
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From statistician

1. **Cost estimation 4x underestimate**: statistician validated my concern about the per-round cost formula. For 3 agents: actual cost is 16 per round (review=3, cross-review=6, revision=3, disputes=3, synthesis=1), estimate is 4 (agents + 1). This is a material accuracy issue in the convergence recommendation. **Updated assessment**: The predictor should import and use `engine.cost.estimate_cost` like the optimizer does.

2. **Flat disputes spec compliance**: statistician revised their position after my FR-006 reference. Flat disputes mapping to stagnation is spec-compliant.

### From spec-compliance

1. **FR-008 cost accuracy**: spec-compliance notes the cost underestimate may make FR-008 PARTIALLY MET. I agree -- the "estimated additional agent launches" field is present but the number is wrong by a factor of 4. The format is correct, the data is misleading.

2. **position_drift data quality**: My cross-review finding that position_drift is always 0.0 is confirmed. Structural compliance (field present) but no semantic value.

---

## Updated Key Issues

1. **Equilibrium score integration TODO (medium)**: Unchanged. The predictor should read scorer output from the plugins directory.
2. **Cost estimation accuracy (medium, elevated)**: Was low, now medium after consensus that 4x underestimate is misleading.
3. **position_drift dead metric (low)**: Structural compliance only.
4. **auto_stop config not consumed (low)**: Reserved-for-future semantics accepted.

---

## Unchanged Assessments

- Full ABC conformance.
- Hook execution correct for POST_PHASE_5.
- Coexistence with scorer works at infrastructure level.
- Output format structurally compliant (all FR-010 fields present).
- Error handling robust.
- Recommendation strings match FR-007/FR-008 format.
