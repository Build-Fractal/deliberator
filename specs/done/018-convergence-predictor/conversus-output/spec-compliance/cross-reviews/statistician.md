# Phase 2 Cross-Review: spec-compliance reviews statistician

**Spec**: 018-convergence-predictor
**Reviewer**: spec-compliance
**Reviewing**: statistician's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **Equilibrium trend integration incomplete**: statistician and plugin-engineer both identify the TODO. This is visible in the code: `equilibrium_scores=None,  # TODO: read from scorer output`. The equilibrium trend function is implemented but never receives data.

2. **Confidence is a heuristic, not statistical**: Valid concern. The spec says "confidence: float 0.0-1.0" without clarifying its interpretation. The implementation is a data-sufficiency indicator, which is reasonable but should be documented.

3. **Flat disputes classification**: statistician raises a nuanced point about adversarial modes. From a compliance perspective, the spec does not prescribe how to handle flat dispute trends. FR-006 says "If the rate is zero or negative, report stagnation." Zero rate (flat) mapping to stagnation is actually spec-compliant per the literal text of FR-006.

4. **Concession rate averaging**: Valid statistical concern but not a compliance issue. The spec does not prescribe the aggregation method.

## Points to Add

1. **FR-004 and Kalman filtering**: statistician confirms the gap between OLS and Kalman filtering. From a compliance perspective, the spec's Section 2.2 is quite specific: "Build a linear surrogate model of each agent's best-response function using Kalman filtering (gnep-learn's approach)." The implementation builds linear surrogate models (OLS slope) but without the recursive Kalman update, noise model, or state estimation. This is a material deviation, not just a simplification.

2. **Position drift uninformative**: Relevant to FR-010 compliance. The `position_drift` field is always 0.0 because position vectors are never populated through the state-based path. The field is present (FR-010 MET) but contains no useful information.

## Disagreement

**FR-011**: statistician argues this should be MET because "reserved" means "must exist but must not have behavior." I can see the logic, but "support" in FR-011 arguably means the field should be documented in the config schema and validated (e.g., must be boolean). The implementation uses `config.get()` which accepts any key silently. I maintain PARTIALLY MET but accept this is debatable.
