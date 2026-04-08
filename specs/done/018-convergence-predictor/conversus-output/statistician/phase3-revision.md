# Phase 3 Revision: statistician

**Spec**: 018-convergence-predictor
**Reviewer**: statistician
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From plugin-engineer

1. **position_drift always 0.0**: plugin-engineer identifies that `_build_feature_history()` never populates `position_vector`, so `_compute_position_drift()` always returns 0.0. I missed this because I reviewed the pure functions in isolation without tracing the data flow from the plugin. **Updated assessment**: position_drift is a dead metric in the current implementation. The FR-010 field is present but uninformative.

2. **Cost estimation 4x underestimate**: Critical finding. The predictor estimates per-round cost as `num_agents + 1` but the actual D007 formula gives ~16 for 3 agents. This makes FR-008's "estimated additional agent launches" misleading. **Updated assessment**: I now flag this as a data quality issue that should use the same cost formula as the optimizer plugin.

### From spec-compliance

1. **FR-006 and flat disputes**: spec-compliance points out that FR-006 says "If the rate is zero or negative, report stagnation." Flat disputes (zero rate) mapping to stagnation IS spec-compliant. I revise my concern: the classification is correct per spec. My concern about adversarial modes is a spec-design issue, not an implementation issue.

2. **FR-011 auto_stop**: spec-compliance maintains PARTIALLY MET while I argued for MET. After reflection, I accept that "MUST support" is stronger than "MUST not crash on." I revise to PARTIALLY MET.

---

## Updated Key Issues

1. **FR-004 OLS vs. Kalman (critical)**: The spec requires Kalman filtering. Implementation uses OLS. Material deviation acknowledged by all reviewers.
2. **Equilibrium trend integration incomplete (medium)**: TODO in code. Equilibrium trend is always 0.
3. **Cost estimation underestimate (medium, new)**: 4x underestimate of per-round agent launches.
4. **position_drift always 0.0 (low, new)**: Dead metric due to unpopulated position vectors.
5. **Flat disputes as stagnation (revised)**: Now classified as spec-compliant per FR-006.
6. **Confidence not statistically grounded (documentation)**: Should be documented as a heuristic indicator.

---

## Unchanged Assessments

- Linear slope computation: Sound.
- Dispute and concession trends: Correct.
- CONVERGE/STAGNATE/UNCERTAIN logic: Sound.
- Rounds remaining cap at 10: Appropriate safeguard.
