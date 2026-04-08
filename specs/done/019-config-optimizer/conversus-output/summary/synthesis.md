# Phase 5 Synthesis: Spec 019 -- Config Optimizer

**Spec**: 019-config-optimizer
**Date**: 2026-03-24
**Agents**: optimization-engineer, plugin-engineer, spec-compliance

---

## Overall Assessment

The Config Optimizer plugin is a well-engineered heuristic optimizer with a sound quality model, correct cost formula, and robust infeasibility detection. The Plugin ABC conformance is complete and the PRE_EXECUTION hook is correctly implemented. However, this spec has the most NOT MET requirements of the four reviewed: AMPL integration (FR-006, FR-007), objective function input (FR-003), general-purpose API (FR-014, FR-015), and mode as a decision variable are all absent. The implementation delivers a useful grid search optimizer but falls short of the spec's vision of an AMPL-based MIP solver with general-purpose optimization capabilities.

---

## Consensus Findings

### 1. AMPL Integration Absent -- FR-006, FR-007 NOT MET (Critical)

**Unanimous**. The spec envisions MIP formulation using AMPL with HiGHS solver. No AMPL code exists. The grid search replaces the solver entirely. Comments in the code mark "AMPL integration points" but no integration is present.

**Recommendation**: Either (a) implement AMPL/HiGHS integration, or (b) update the spec to describe the grid search as the v1 approach with AMPL as a future enhancement. Option (b) is pragmatic -- optimization-engineer confirms the grid search provides optimal results for the 135-point discrete space.

### 2. Mode Not Searched -- FR-009 PARTIALLY MET (Critical)

**Unanimous**. The spec lists `mode` as a decision variable (Section 2: {cooperative, wta, pd, rb}). The grid search only covers rounds, iterations, and agent_count. `recommended_mode` is missing from the output. `objective_value` is also absent.

**Recommendation**: Add mode to the search space (4 modes * 135 grid points = 540 total, still trivial) and include `recommended_mode` and `objective_value` in output.

### 3. Objective Function Input Not Read -- FR-003 NOT MET (Medium)

**Unanimous**. The spec says the optimizer "MUST accept an objective function (`objective.yml` from spec 014) as input." The implementation reads only budget and quality_threshold from config. No objective function parsing exists.

**Recommendation**: Implement objective function reading or update spec to defer to a future version.

### 4. General-Purpose API Not Implemented -- FR-014, FR-015 NOT MET (Medium)

**Unanimous**. No `solve(model, data, solver)` API. No custom model support via `model_file`. The implementation is config-specific.

**Recommendation**: Defer to future AMPL integration.

### 5. Quality Model Well-Designed (Consensus)

The exponential saturation curves with weighted geometric mean produce sensible quality estimates. Monotonicity is verified across all three dimensions. The minimal config (~0.19) and maximal config (~0.93) bracket the quality range appropriately. Parameters are not data-derived but are reasonable heuristics for v1.

### 6. Cost Model Correct (Consensus)

Uses `engine.cost.estimate_cost` for the canonical D007 formula. Per-round cost scales linearly with rounds. Arbiter adds 1 per round. Test coverage includes known-value regression anchor.

### 7. Infeasibility Detection Well-Implemented (Consensus)

Dual-path: budget-constrained (reports minimum budget needed) and quality-unreachable (reports threshold is too high). Clear reasoning strings with actionable information.

### 8. auto_optimize Flag Correct (Consensus)

Controls `PluginResult.advisory`. Default False = advisory. True = actionable. The plugin never modifies config directly (FR-013 MET).

### 9. Error Handling Robust (Consensus)

Missing budget, invalid budget, and infeasible optimization all handled gracefully with clear error messages.

---

<!-- DISPUTES_BEGIN -->

## Unresolved Disputes

None. All disagreements were resolved during the cross-review phase. Full consensus was achieved on all findings.

<!-- DISPUTES_END -->

---

## Compliance Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-001 | MET | |
| FR-002 | NOT VERIFIED | Packaging concern |
| FR-003 | **NOT MET** | No objective function input |
| FR-004 | MET | |
| FR-005 | MET | |
| FR-006 | **NOT MET** | No AMPL MIP formulation |
| FR-007 | **NOT MET** | No HiGHS solver |
| FR-008 | MET | |
| FR-009 | PARTIALLY MET | Missing recommended_mode, objective_value |
| FR-010 | MET | |
| FR-011 | NOT VERIFIED | Calling-code responsibility |
| FR-012 | MET | |
| FR-013 | MET | |
| FR-014 | **NOT MET** | No general-purpose API |
| FR-015 | **NOT MET** | No custom model support |
| FR-016 | PARTIALLY MET | Some fields unused |
| FR-017 | MET (by design) | |
| FR-018 | N/A | |
| SC-001 | MET | |
| SC-002 | MET | |
| SC-003 | PARTIALLY MET | Missing mode |
| SC-004 | NOT VERIFIED | |
| SC-005 | NOT VERIFIED | |

**MET**: 8/18 FR, 2/5 SC
**PARTIALLY MET**: 2 FR, 1 SC
**NOT MET**: 5 FR
**NOT VERIFIED**: 3 FR, 2 SC
**N/A**: 1 FR

---

## Recommended Actions

1. Add mode to search space and include `recommended_mode` in output (fixes FR-009 and SC-003).
2. Decide: Implement AMPL/HiGHS (FR-006, FR-007) or update spec to accept grid search as v1.
3. Implement objective function reading (FR-003) or defer to future version.
4. Add `objective_value` to output (FR-009).
5. Document quality model parameters with rationale.
6. Improve infeasibility message for unreachable quality thresholds.
7. Validate budget > 0 explicitly for better error messages.

## Systemic Observation

This is the third of four specs where the implementation provides heuristic fallbacks while the spec envisions premium methods (nashopt in 017, Kalman in 018, AMPL in 019). The project should decide whether to (a) implement the premium methods or (b) update all specs to reflect the heuristic approaches as the v1 design, with premium methods as documented future enhancements.
