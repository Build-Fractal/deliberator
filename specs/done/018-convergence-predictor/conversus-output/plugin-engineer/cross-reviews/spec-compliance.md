# Phase 2 Cross-Review: plugin-engineer reviews spec-compliance

**Spec**: 018-convergence-predictor
**Reviewer**: plugin-engineer
**Reviewing**: spec-compliance's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **FR-004 PARTIALLY MET**: Agree. The spec is explicit about Kalman filtering. OLS is a reasonable simplification but is not what was specified. The docstring acknowledges this.

2. **FR-013 MET (by design)**: Clever but accurate. The fallback path IS the primary path because the primary method (Kalman) was never implemented.

3. **SC-004 NOT VERIFIED**: Agree. No end-to-end accuracy test. The rounds-remaining estimation is tested in isolation but never compared to actual deliberation outcomes.

4. **All constraints MET**: Confirmed. The predictor is purely advisory, does not modify state, works with 1 round, and has no external dependencies.

## Points to Add

1. **FR-010 output filename**: Same deviation as spec 017. The spec says `plugins/convergence-prediction-round-{N}.json`, actual is `convergence-predictor-post_phase_5-round-{N}.json`. Consistent finding across both nashopt plugins. I would mark the output format as MET (all fields present) with the filename format as a separate noted deviation.

2. **FR-008 cost estimation accuracy**: statistician (in cross-review of my review) identified that the cost formula `rounds * (num_agents + 1)` drastically underestimates true agent launches. For 3 agents, the actual per-round cost is 16 (via D007 formula), but the predictor estimates 4. This means the "estimated additional agent launches" in the recommendation is misleading. The optimizer plugin (spec 019) has the correct cost formula via `engine.cost.estimate_cost`. The predictor should use the same formula.

## Disagreement

**FR-011**: I lean toward PARTIALLY MET. spec-compliance's reasoning is sound (auto_stop not consumed), but the reserved-for-future semantics are ambiguous. The spec says the config "MUST support" the field. "Support" could mean "accept without error" (MET) or "read and store for future use" (PARTIALLY MET). I acknowledge this is borderline.
