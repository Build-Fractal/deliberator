# Phase 2 Cross-Review: statistician reviews spec-compliance

**Spec**: 018-convergence-predictor
**Reviewer**: statistician
**Reviewing**: spec-compliance's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **FR-004 PARTIALLY MET**: Strongly agree. The spec explicitly describes "Kalman filtering" and "gnep-learn's active learning approach." The implementation uses OLS linear regression. While OLS can be seen as a degenerate case of Kalman filtering (with no process noise model), the implementation lacks the recursive update, state estimation, and noise modeling that characterize Kalman filtering. spec-compliance's PARTIALLY MET is the right call.

2. **FR-013 MET (by design)**: Clever observation. Since no Kalman filter exists, the fallback heuristic IS the primary path. The requirement is technically satisfied by not having a failure mode.

3. **SC-004 NOT VERIFIED**: Agree. No end-to-end accuracy testing exists. My concern about linear extrapolation underestimating rounds remaining is relevant here.

## Points to Add

1. **FR-003 calibration precision**: spec-compliance marks FR-003 as MET because confidence is in 0.30-0.45 for single rounds. I want to add statistical context: the spec's 0.3-0.5 range is sensible for a single data point. With one observation, any trend estimate has infinite variance (you cannot compute a slope from one point). The capped confidence of 0.45 is conservative and appropriate. However, the zero-disputes case (confidence 0.30-0.45, prediction "converge") may be overconfident -- one round of zero disputes does not guarantee convergence. The code handles this by capping at 0.45, but even 0.45 confidence for a "converge" prediction from one round is generous.

2. **FR-011 auto_stop**: spec-compliance marks as PARTIALLY MET because auto_stop is not consumed. I agree with the nuance: "reserved for future" means the config should accept the key without error, which Pydantic config dicts do by default (extra keys are ignored). The spirit of FR-011 is that the field exists in the config schema. Since there is no formal config schema (it uses `config.get()`), "support" means "does not crash on." This is MET in that sense.

## Disagreement

**FR-011**: I believe this should be MET, not PARTIALLY MET. The spec says auto_stop is "reserved for future autonomous mode; when true, stagnation prediction above confidence threshold triggers automatic stop recommendation." The reserved semantics mean the field MUST exist but MUST NOT have behavior yet. The implementation satisfies both conditions: the field can be passed in config (no crash), and it has no effect. This is the correct behavior for a reserved field.
