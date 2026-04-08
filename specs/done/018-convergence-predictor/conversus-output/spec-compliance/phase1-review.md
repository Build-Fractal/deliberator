# Phase 1 Review: spec-compliance

**Spec**: 018-convergence-predictor
**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Check every FR and SC for compliance status.

---

## Functional Requirements

### FR-001: Register as `convergence-predictor` with hook `[POST_PHASE_5]`

**MET**

`ConvergencePredictor.name = "convergence-predictor"`, `hooks = [HookPoint.POST_PHASE_5]`. Verified by tests.

### FR-002: Ship in `conversus-nashopt` package alongside equilibrium scorer

**MET**

Both plugins in `conversus/plugins/nashopt/`. `__init__.py` exports both. `__all__ = ["ConvergencePredictor", "EquilibriumScorer"]`. Tests verify import.

### FR-003: After Round 1, produce prediction with low confidence (0.3-0.5)

**MET**

Single-round case: confidence capped at 0.45 via `confidence = min(confidence, 0.45)`. Base confidence for 1 round is 0.30. Range 0.30-0.45 is within the spec's 0.3-0.5 range. Test `test_single_round_low_confidence` verifies confidence < 0.6.

### FR-004: After Round 2+, use cross-round feature trajectories for surrogate models via Kalman filtering

**PARTIALLY MET**

The implementation uses linear regression (OLS) for trend analysis, not Kalman filtering. The spec specifically says "build surrogate models via Kalman filtering" and references "gnep-learn's active learning approach." The convergence.py module docstring acknowledges this: "implements a simplified version of the gnep-learn approach." The linear trend analysis is a reasonable simplification, but it is not Kalman filtering. The spec's Section 2 describes a specific process (linear surrogate models via Kalman filtering, fixed-point detection). The implementation uses OLS slope as a proxy for convergence/divergence, which is simpler than the described method.

### FR-005: Report `uncertain` when confidence below threshold

**MET**

When `confidence < min_confidence`, prediction is downgraded to "uncertain" with reasoning that mentions the threshold. Tests verify this with both high and low thresholds.

### FR-006: Estimated rounds from convergence rate; stagnation if rate <= 0

**MET**

`_estimate_rounds_remaining()` returns 0 if trend >= 0 (no convergence). Returns `ceil(dispute_count / abs(trend))` capped at 10. Test `TestEstimateRoundsRemaining` covers all cases.

### FR-007: Stagnation recommendation with concrete actions

**MET**

Stagnation recommendation includes: "(1) triggering arbitration, (2) adjusting agent configuration, (3) stopping and using current synthesis." Matches FR-007's required format exactly.

### FR-008: Convergence recommendation with estimated cost

**MET**

Convergence recommendation includes: "Estimated additional agent launches: {N}." Cost is computed as `estimated_rounds_remaining * (num_agents + 1)`. Tests verify.

### FR-009: Must NOT automatically stop rounds or trigger arbitration

**MET**

All results have `advisory=True`. No code path modifies deliberation state or triggers actions. The plugin is purely observational.

### FR-010: Output format with all required fields

**MET**

All eight required fields present: `prediction`, `confidence`, `estimated_rounds_remaining`, `current_round`, `dispute_trajectory`, `position_drift`, `fixed_point_exists`, `reasoning`. Test `test_data_contains_all_fr010_fields` verifies.

### FR-011: Config supports min_confidence and auto_stop

**PARTIALLY MET**

`min_confidence` is read and used: `config.get("min_confidence", 0.5)`. Default 0.5 matches spec.
`auto_stop` is documented in the class docstring but NOT read in `execute()`. The spec says it defaults to false and is "reserved for future autonomous mode." Since the config key exists conceptually but is never consumed, this is acceptable for the "reserved" semantics. However, a strict reading requires the config to "support" the field, which means at minimum accepting it without error.

### FR-012: Insufficient data returns uncertain

**MET**

No agents: returns uncertain. Single agent: handled via normal flow (produces uncertain at low confidence). Feature construction failure: caught and returns uncertain.

### FR-013: Kalman filter failure falls back to dispute count heuristics

**MET (by design)**

The implementation always uses dispute count heuristics (no Kalman filter exists to fail). This technically satisfies FR-013 by making the fallback the primary path. However, the intent was that Kalman is primary and heuristics are fallback. Since FR-004 is only PARTIALLY MET, this is a consequence of that gap.

---

## Success Criteria

### SC-001: Disputes 5->2 predicts converge with reasonable confidence

**MET**

`TestConvergePrediction.test_decreasing_disputes_predicts_converge` uses disputes 5->3->1, predicts converge with confidence > 0.5.

### SC-002: Disputes 3->5 predicts stagnate

**MET**

`TestStagnatePrediction.test_increasing_disputes_predicts_stagnate` uses disputes 3->5, predicts stagnate.

### SC-003: After Round 1, confidence below 0.6

**MET**

`test_single_round_low_confidence` verifies confidence < 0.6. Capped at 0.45.

### SC-004: Estimated rounds within +/-1 of actual

**NOT VERIFIED**

No test compares estimated rounds to actual convergence behavior on a real deliberation. The estimation function is tested in isolation, but the end-to-end accuracy is not validated.

### SC-005: Stagnation includes actionable suggestions

**MET**

Stagnation reasoning includes arbitration, config adjustment, and stopping suggestions. Tests verify.

---

## Constraints Compliance

| Constraint | Status |
|-----------|--------|
| Must NOT automatically stop | MET -- advisory only |
| Must NOT modify core round logic | MET -- read-only observer |
| Must NOT require more than Round 1 | MET -- works with 1 round |
| Must NOT depend beyond nashopt ecosystem | MET -- no external deps |

---

## Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-001 | MET | |
| FR-002 | MET | |
| FR-003 | MET | Confidence 0.30-0.45 |
| FR-004 | **PARTIALLY MET** | OLS, not Kalman filtering |
| FR-005 | MET | |
| FR-006 | MET | |
| FR-007 | MET | |
| FR-008 | MET | |
| FR-009 | MET | |
| FR-010 | MET | |
| FR-011 | PARTIALLY MET | auto_stop not consumed |
| FR-012 | MET | |
| FR-013 | MET (by design) | No Kalman to fail |
| SC-001 | MET | |
| SC-002 | MET | |
| SC-003 | MET | |
| SC-004 | NOT VERIFIED | No end-to-end accuracy test |
| SC-005 | MET | |
