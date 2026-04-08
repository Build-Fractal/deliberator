# Round 2 Review: optimization-engineer

**Spec**: 027-solver-validation-flow
**Agent**: optimization-engineer
**Round**: 2
**Input**: Round 1 synthesis with 6 surviving disputes

---

## Dispute Status Assessment

### DISPUTE 1 (End-to-end flow) -- ACCEPT PHASING RESOLUTION

The phased approach is pragmatic. From a solver engineering perspective, Phase 1 (models + config) provides the specification layer. Phase 2 (CLI + execution) provides the runtime layer. Phase 3 (equilibrium + convergence + AMPL feedback) provides the integration layer. Each phase is independently testable and deliverable.

I accept the resolution. The dispute dissolves if the spec acknowledges the current implementation as Phase 1.

**Status**: RESOLVABLE.

### DISPUTE 2 (AMPL feedback loop) -- ACCEPT RESOLUTION WITH TECHNICAL SPECIFICATION

The `ConstraintAddition` model needs precise definition. I propose:

```python
class ConstraintAddition(BaseModel):
    constraint_type: Literal["bound", "capacity", "linking", "fairness", "custom"]
    description: str  # human-readable explanation
    lhs_expression: str  # left-hand side, using model variable names
    sense: Literal["<=", ">=", "=="]
    rhs_value: float | str  # numeric value or parameter reference
    variables_referenced: list[str]  # model variables this constraint involves
```

This is more structured than `list[str]` but does not attempt full AMPL code generation. The `variables_referenced` field enables validation against the model's variable set. The `lhs_expression` uses algebraic notation that a code generation layer can translate to AMPL/Pyomo.

The devex-advocate's request for `human_readable` is met by the `description` field.

**Status**: RESOLVABLE -- requires model definition and spec FR-010 amendment.

### DISPUTE 3 (Solution input schema) -- ACCEPT RESOLUTION

I propose the following `SolverSolution` model:

```python
class SolverSolution(BaseModel):
    objective_value: float | None = None
    solve_status: Literal["optimal", "feasible", "infeasible", "unbounded", "error"] | None = None
    variables: dict[str, float] = Field(default_factory=dict)
    constraint_slack: dict[str, float] = Field(default_factory=dict)
    dual_values: dict[str, float] = Field(default_factory=dict)
    solver_name: str | None = None
    solve_time_seconds: float | None = None
```

All fields optional (except the model itself) to accommodate different solver outputs. The `dual_values` field enables the sensitivity enrichment discussed in Dispute 4.

**Status**: RESOLVABLE.

### DISPUTE 4 (Sensitivity qualitative nature) -- ACCEPT RESOLUTION

I propose amended sensitivity instructions:

> "This is a structural sensitivity assessment based on problem analysis, not a numerical re-solve. For each key parameter, assess:
> - Is this parameter's value close to a constraint boundary? (fragile feasibility)
> - Does this parameter appear in the objective function with a large coefficient? (high objective sensitivity)
> - Is this parameter discrete (integer/binary)? If so, analyze the impact of adding/removing one unit rather than percentage perturbation.
> - If dual values are available in the solution, use them to identify binding constraints and their marginal values.
> Structure findings as: parameter, change, feasibility_impact, objective_impact"

This preserves the structured output format while setting correct expectations about the analysis type.

**Status**: RESOLVABLE.

### DISPUTE 5 (SC-002) -- ACCEPT PARTIALLY MET

I did not take a strong position in Round 1. I accept PARTIALLY MET as the consensus. The framework is designed to enable the finding; runtime demonstration is pending.

**Status**: RESOLVED.

### DISPUTE 6 (Missing problem types) -- ACCEPT RESOLUTION

Scheduling template:
```python
"scheduling": [
    {"name": "makespan-optimizer", "prompt": "..."},
    {"name": "resource-utilizer", "prompt": "..."},
    {"name": "dependency-checker", "prompt": "..." + _SENSITIVITY_INSTRUCTIONS},
]
```

Negotiation template:
```python
"negotiation": [
    {"name": "party-advocate", "prompt": "..."},
    {"name": "mediator", "prompt": "..." + _SENSITIVITY_INSTRUCTIONS},
    {"name": "fairness-auditor", "prompt": "..."},
]
```

**Status**: RESOLVABLE -- straightforward template addition.

---

## New Observations (Round 2)

### The ConstraintAddition model bridges the spec gap

The proposed `ConstraintAddition` model addresses both the implementation gap and the spec gap identified in Round 1. FR-010's language ("consumable by the solver") is satisfied if:
1. The model provides structured constraint data (type, expression, sense, RHS)
2. A code generation layer (separate concern, potentially spec 023) translates to solver-specific syntax
3. The contract between validation output and solver input is the `ConstraintAddition` schema

This decouples the validation flow (spec 027's concern) from the AMPL code generation (spec 023's concern). The validation flow produces structured constraint recommendations; the solver integration layer consumes them.

### Dual values as the sensitivity bridge

If `SolverSolution` includes `dual_values`, the sensitivity analysis can be enriched without solver re-runs. For LP solutions, dual values give exact local sensitivity (marginal value of relaxing each constraint). For MILP solutions, dual values from the LP relaxation give approximate sensitivity. The sensitivity instructions can check: "If dual_values are available, report the binding constraints and their shadow prices as the primary sensitivity findings."

This partially addresses the mathematical rigor concern from Round 1 without requiring solver re-runs.
