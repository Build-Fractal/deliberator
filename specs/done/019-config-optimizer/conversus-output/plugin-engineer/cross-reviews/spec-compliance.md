# Phase 2 Cross-Review: plugin-engineer reviews spec-compliance

**Spec**: 019-config-optimizer
**Reviewer**: plugin-engineer
**Reviewing**: spec-compliance's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **FR-003 NOT MET**: No objective function input. Clear gap.
2. **FR-006, FR-007 NOT MET**: No AMPL/HiGHS. The grid search is the only backend.
3. **FR-014, FR-015 NOT MET**: No general-purpose API. The plugin is config-specific.
4. **FR-009 PARTIALLY MET**: Missing `recommended_mode` and `objective_value`.
5. **FR-017 MET (by design)**: Correct pattern identification.

## Points to Add

1. **Systemic pattern**: spec-compliance identifies "MET by design" for FR-017. This is the third spec where the premium method is absent and the fallback IS the implementation. This suggests the specs were written aspirationally while implementation focused on delivering useful heuristic results. The pattern is: spec envisions {nashopt, Kalman, AMPL}, implementation provides {heuristic payoffs, OLS slopes, grid search}. Both are valid, but the specs need updating.

2. **FR-016 extra fields**: spec-compliance notes `max_agents` and `cost_per_agent_launch` are not in the spec but exist in the config. These are useful extensions that do not conflict with spec requirements. Not non-compliant, but undocumented.

3. **FR-011 NOT VERIFIED**: Agree. Interactive confirmation is a calling-code responsibility. The plugin's role is to set `advisory=True`, which it does.

## Disagreement

**FR-002**: I agree with optimization-engineer that this should be NOT VERIFIED rather than PARTIALLY MET. No packaging infrastructure exists for any conversus plugin. This is a deployment gap, not a code-level compliance issue.
