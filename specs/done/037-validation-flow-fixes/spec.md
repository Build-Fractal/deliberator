# Feature Specification: Validation Flow Fixes

**Feature ID**: `037-validation-flow-fixes`
**Created**: 2026-04-01
**Status**: Draft
**Files**: `conversus/schemas/validation.py`, `tests/test_validation.py`

---

## Items (7)

### HIGH
- **H-4**: ConstraintAddition typed model. Replace `constraint_additions: list[str]` with Pydantic model: `constraint_type`, `expression`, `parameters`, `target_solver`.
- **D-1**: SolverSolution input schema. Define model with: `objective_value`, `variable_assignments`, `solver_status`, `constraints_satisfied`, `solve_time_ms`.

### MEDIUM
- **D-4**: Sensitivity analysis qualitative framing. Prompt says "±10% change" implying quantitative analysis but agent can't compute it. Fix: reframe as qualitative reasoning about parameter sensitivity.
- **M-3**: Add validation templates for 4 new modes (negotiation, resource-allocation, fair-division, mechanism-design) to `_AGENT_TEMPLATES`.
- **NEW-10**: Track validate-solution Phase 2 (CLI command + execution pipeline). Create tracking section in spec or separate spec.
- **NEW-11**: Track Phase 3 blocked items (equilibrium scorer + convergence predictor integration, blocked on 021/022).

### LOW
- **NEW-8**: Constrain `feasibility_impact` to Literal enum instead of freetext string.
- **NEW-9**: Remove redundant `confidence_in_range` field_validator.

## Success Criteria
- SC-001: ConstraintAddition validates with typed fields.
- SC-002: SolverSolution model validates solution structure.
- SC-003: Sensitivity prompt says "reason about" not "compute."
- SC-004: All 8 modes have validation agent templates.
