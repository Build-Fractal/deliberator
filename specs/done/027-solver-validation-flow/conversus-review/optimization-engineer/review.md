# Phase 1 Review: optimization-engineer

**Spec**: 027-solver-validation-flow
**Agent**: optimization-engineer
**Round**: 1
**Focus**: Sensitivity analysis rigor, AMPL feedback loop, problem type to agent mapping correctness, ability to catch real solver issues.

---

## Overall Assessment

The validation flow attempts something genuinely valuable: having multi-agent critique serve as a post-solve verification layer. From a solver engineering perspective, the mathematical content is mixed -- the sensitivity analysis framework is structurally sound but operationally incomplete, and the AMPL feedback loop (the spec's most ambitious claim) has no implementation path.

**Verdict**: PARTIAL PASS. Good conceptual design, but significant gaps in mathematical rigor and solver integration.

---

## Detailed Findings

### 1. Sensitivity Analysis Rigor -- STRUCTURALLY SOUND, COMPUTATIONALLY VAGUE

The `_SENSITIVITY_INSTRUCTIONS` block tells agents to analyze "what happens if parameter X changes by +/-10%?" with structured output fields: parameter, change, feasibility_impact, objective_impact.

**What's mathematically correct**:
- The four-field structure (parameter, change, feasibility_impact, objective_impact) maps to standard sensitivity analysis output. In LP duality, this corresponds to examining how perturbations to the right-hand side (constraint parameters) or cost coefficients (objective parameters) affect primal feasibility and optimal value.
- The +/-10% perturbation magnitude is reasonable as a default -- it's large enough to expose fragile optima without being so large that every solution appears sensitive.
- The `SensitivityFinding` Pydantic model enforces all four fields, preventing incomplete analysis.

**What's mathematically incomplete**:
- **No distinction between RHS sensitivity and cost sensitivity**. In LP, perturbing the right-hand side of a constraint (e.g., budget limit) affects feasibility and the dual price gives the exact marginal value. Perturbing a cost coefficient affects optimality but not feasibility. The instructions treat these as the same thing ("parameter changes"), which conflates two fundamentally different sensitivity regimes.
- **No shadow price / dual variable extraction**. For LP/MILP solutions, the solver already computes dual values (shadow prices) that give exact sensitivity information for small perturbations. The spec ignores this -- it asks LLM agents to guess at sensitivity when the solver has already computed it. This is like asking a human to estimate a derivative when the calculus is already done.
- **+/-10% is not always meaningful**. For integer variables (e.g., number of engineers in an assignment problem), a 10% change might be fractional and meaningless. For binary variables, any perturbation destroys the solution structure entirely. The instructions should differentiate between continuous and discrete parameter sensitivity.
- **No basis stability analysis**. In LP, a small perturbation can cause the optimal basis to change (basis transition), producing a discontinuous jump in the objective value. The sensitivity instructions don't distinguish between changes within the current basis (smooth, predictable via dual values) and basis transitions (discontinuous, potentially large impact).

**Severity**: MEDIUM. The framework is directionally correct but lacks the mathematical precision needed for rigorous solver validation. An LLM agent using these instructions will produce plausible-sounding but potentially incorrect sensitivity assessments.

### 2. AMPL Feedback Loop -- NOT IMPLEMENTABLE AS SPECIFIED

FR-010 says: "The validation output MUST be consumable by the solver for re-optimization (constraint feedback loop)." The `constraint_additions` field in `ValidationVerdict` is a `list[str]` -- free-form strings.

**The problem**: There is no path from free-form English strings to AMPL constraint syntax. Consider the test's example:

```python
constraint_additions=[
    "Add capacity constraint: sum(x[i]) <= 10",
    "Add fairness bound: max(x[i]) - min(x[i]) <= 3",
]
```

These look like constraints but are not valid AMPL. In AMPL, the first would be:
```ampl
subject to total_capacity: sum {i in ITEMS} x[i] <= 10;
```

The second is worse -- `max(x[i]) - min(x[i]) <= 3` requires auxiliary variables and linearization in a MILP context. An LLM agent writing natural-language constraint suggestions cannot produce solver-ready constraints without:
1. Knowledge of the specific AMPL model's sets, parameters, and variable names
2. Understanding of whether the problem is LP, MILP, QP, or nonlinear (determines linearization strategies)
3. Access to the AMPL model file itself (not just solution.yml)

**What would work**: A structured constraint template system where agents select from parameterized constraint families:
```python
@dataclass
class ConstraintAddition:
    type: Literal["bound", "capacity", "fairness", "linking"]
    expression: str  # template expression with variable references
    parameters: dict[str, float]  # numeric parameters
    ampl_template: str | None  # pre-computed AMPL syntax
```

**Severity**: HIGH. FR-010 is the spec's central feedback loop claim and cannot be satisfied with free-form strings. Either the spec needs amendment or a structured constraint generation system is needed.

### 3. Problem Type to Agent Mapping -- MOSTLY CORRECT

The mapping for implemented types is sound:

**General** (optimality-auditor, sensitivity-analyst, constraint-verifier):
- Correct. These three roles cover the standard LP/MILP post-solve checks: is the objective optimal, is it robust, are all constraints satisfied.

**Assignment** (efficiency-advocate, fairness-advocate, constraint-auditor):
- Correct. Assignment problems have a known tension between total cost minimization (efficiency) and equitable distribution (fairness). The constraint-auditor role addresses the common issue of missing capacity/eligibility constraints in assignment formulations.
- The fairness-advocate prompt correctly focuses on resource-priority mismatches, directly addressing SC-001.

**Portfolio** (return-maximizer, risk-minimizer, diversification-advocate):
- Correct. This maps to the standard mean-variance optimization trinity. Return maximizer checks for Pareto improvements; risk minimizer checks for tail exposure; diversification advocate checks for concentration risk.

**Missing types**:
- **Scheduling**: The spec lists makespan-optimizer, resource-utilizer, risk-assessor, dependency-checker. This is the correct decomposition for job-shop / flow-shop scheduling problems. Not implemented.
- **Negotiation**: The spec lists party advocates + mediator + legal reviewer. This maps to the mechanism design / bargaining game context from spec 021. Not implemented.

**Incorrect agent counts**: The spec table shows 4 agents for assignment and scheduling but the implementation uses 3. The missing 4th agent for assignment is "robustness tester" -- a role that would specifically check solution stability under constraint perturbation. This is a meaningful omission because without a dedicated robustness agent, robustness analysis is implicitly assumed to be part of the sensitivity analyst's role, but the assignment type has no sensitivity analyst.

**Severity**: MEDIUM. 3/5 types implemented; assignment missing a robustness agent that the spec explicitly includes.

### 4. Catching Real Solver Issues -- PARTIAL

The validation flow could catch certain classes of solver issues:

**Would catch**:
- Fairness violations in assignment solutions (via fairness-advocate)
- Missing constraints that lead to degenerate solutions (via constraint verifiers)
- Obvious sensitivity to parameter changes (via sensitivity instructions)
- Infeasible solutions presented as feasible (via constraint auditors)

**Would NOT catch**:
- **Local optima in nonlinear problems**: An LLM agent cannot determine if a nonlinear solver found a local vs. global optimum. This requires multistart verification or convexity analysis, neither of which is in the validation flow.
- **Numerical infeasibility**: Solutions with very small constraint violations (e.g., x = 10.0000001 against a bound of 10) that the solver reports as feasible but are technically infeasible. LLM agents reviewing YAML output cannot detect this.
- **Degeneracy**: Multiple optimal solutions with the same objective value but different variable assignments. The solver picks one arbitrarily; the validation flow has no mechanism to explore the alternative optimal space.
- **Solver parameter sensitivity**: The solution may depend on solver tolerances (optimality gap, feasibility tolerance, time limit). The validation flow analyzes problem parameter sensitivity but not solver configuration sensitivity.

**Severity**: MEDIUM. The flow catches structural issues well but misses numerical and algorithmic solver issues.

---

## Summary of Findings

| # | Severity | Finding |
|---|----------|---------|
| 1 | HIGH | AMPL feedback loop unimplementable with free-form constraint_additions strings |
| 2 | MEDIUM | Sensitivity analysis conflates RHS and cost coefficient sensitivity; ignores dual values |
| 3 | MEDIUM | No shadow price / dual variable extraction from solver output |
| 4 | MEDIUM | Assignment type missing 4th agent (robustness tester) from spec table |
| 5 | MEDIUM | Cannot catch local optima, numerical infeasibility, or degeneracy |
| 6 | LOW | +/-10% perturbation meaningless for integer/binary variables |
| 7 | LOW | No basis stability analysis for LP solutions |
| 8 | INFO | feasibility_impact field should use enum, not free-form string |

---

## Recommendation

REVISE. The conceptual design is strong -- multi-agent critique as a post-solve verification layer is genuinely valuable. But the mathematical rigor needs improvement: sensitivity analysis should distinguish between RHS and cost sensitivity, leverage existing dual values from the solver, and handle discrete vs. continuous parameters. The AMPL feedback loop needs a structured constraint generation system, not free-form strings. Missing problem types (scheduling, negotiation) should be implemented or explicitly deferred in the spec.
