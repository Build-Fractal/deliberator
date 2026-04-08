# Phase 4 Disputes: game-theorist

**Spec**: 025-game-form-expansion
**Agent**: game-theorist

---

## Surviving Disputes

### DISPUTE 1: is_potential_game() scope limitation (HIGH)

**Status**: SURVIVING -- unanimous across all three agents.

The spec describes the potential game diagnostic as "a check applied to existing game forms." The implementation is restricted to 2-player normal-form bimatrix games. The limitation is threefold:

1. **Mathematical**: N-player potential game detection requires payoff gradient field integrability checking, not implemented.
2. **Interface**: The function signature `payoff_matrix: list[list[float]]` structurally excludes non-matrix game representations (GNEP, parametric, stackelberg).
3. **Compliance**: FR-004's "existing game forms" language covers four forms; the diagnostic applies to a subset of one.

**Recommended resolution**: Amend spec section 2.1 to explicitly scope the diagnostic to 2-player normal-form games. Add docstring documentation of the restriction. Open a follow-up issue for N-player generalization.

### DISPUTE 2: BayesianGame prior key validation (MEDIUM)

**Status**: SURVIVING -- unanimous across all three agents.

The BayesianGame model validates `sum(prior.values()) == 1.0` but accepts arbitrary string keys. Invalid keys (e.g., `"garbage": 0.5, "also_garbage": 0.5`) pass validation silently. Keys should be validated against the Cartesian product of type_spaces values.

**Recommended resolution**: Add a model_validator computing the Cartesian product of type_spaces and verifying prior keys are valid type profile tuples.

### DISPUTE 3: Prior tolerance too tight (LOW)

**Status**: SURVIVING -- game-theorist and spec-compliance agree.

The tolerance `abs(total - 1.0) > 1e-6` may reject valid priors computed via floating-point normalization. A tolerance of `1e-4` would be more robust for automated pipelines while still catching specification errors.

**Recommended resolution**: Relax tolerance to 1e-4 or make it configurable.

---

## Withdrawn Disputes

- **MechanismDesignGame sparseness**: Downgraded to INFO. Accepted as appropriate for current phase.
- **v(empty) = 0 convention**: Withdrawn in prior round. Handled implicitly by solver defaults.
- **PotentialGame naming**: Withdrawn. Style preference with zero compliance impact.

---

## Settled Points (No Dispute)

- Shapley computation: CORRECT (all agents agree)
- Congestion game model: CORRECT (missing cost_functions is INFO-level)
- Repeated game discount_factor validation: CORRECT
- Mode mapping: COMPLETE with 5 new entries
- YAML schema structure: CONSISTENT with existing conventions
- FR-004: PASS (all agents converged)
- SC-005: PASS with spec threshold amendment to >= 9
