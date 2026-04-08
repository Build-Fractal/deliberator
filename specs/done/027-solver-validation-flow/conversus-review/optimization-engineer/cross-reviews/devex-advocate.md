# Cross-Review: optimization-engineer reviewing devex-advocate

**Spec**: 027-solver-validation-flow
**Reviewer**: optimization-engineer
**Subject**: devex-advocate Phase 1 review
**Round**: 1

---

## Verified Claims

### 1. End-to-end gap is the dominant issue -- CONFIRMED

The devex-advocate correctly identifies that the implementation stops at config generation. The five missing steps (YAML writer, deliberation runner, output parser, AMPL feedback, convergence predictor) are real gaps. From a solver engineering perspective, the config generation layer is necessary but insufficient -- it is analogous to generating a model file without having a solver to run it.

### 2. problem_type as untyped string -- CONFIRMED

The devex-advocate's recommendation of an enum or Literal type is correct. In the solver world, problem classification is a discrete categorical choice (LP, MILP, QP, NLP, etc.) and is always represented as an enum. Using a plain string invites typos and invalid values that are caught only at runtime.

### 3. Redundant field_validator -- CONFIRMED

The devex-advocate correctly notes that the `confidence_in_range` validator duplicates the `Field(ge=0.0, le=1.0)` constraint. In Pydantic v2, the Field constraint is evaluated before field_validators. The validator adds no additional checking and could be removed without behavioral change.

---

## Disagreements

### 1. Missing problem types severity: MEDIUM is correct but the framing is wrong

The devex-advocate frames the missing scheduling and negotiation types as a developer experience issue ("3 of 5 spec'd types"). I agree with MEDIUM severity but disagree with the reasoning. The missing types are not primarily a DX issue -- they are a domain coverage issue.

Scheduling problems (job-shop, flow-shop, resource-constrained project scheduling) have fundamentally different validation concerns than assignment problems. A scheduling solution can be feasible but have a terrible makespan because critical-path dependencies were not exploited. The risk-assessor and dependency-checker agents from the spec's table address this. Without them, a developer using the validation flow for a scheduling problem would get generic "general" agents that lack scheduling domain knowledge.

Similarly, negotiation problems require party-specific advocates (each party has different preferences and constraints) and a mediator perspective. The "general" agents cannot substitute for this because they lack the multi-party framing.

### 2. Custom agent extension point: DISAGREE on severity

The devex-advocate rates the lack of a custom agent extension mechanism as part of finding #2 (MEDIUM). I disagree that this is a gap at all. The `generate_validation_config()` returns a dict. A developer can trivially add custom agents by appending to the `agents` list:

```python
config = generate_validation_config(solution_path=Path("solution.yml"))
config["agents"].append({
    "name": "regulatory-checker",
    "prompt": "You are a regulatory compliance reviewer...",
})
```

The dict-based return type is actually an advantage here -- it is maximally composable. A typed return (Pydantic model) would require either a mutation method or a copy-with-modifications pattern. The dict is the extension point.

### 3. ValidationVerdict missing iteration field: severity should be LOW, not MEDIUM

The devex-advocate rates the missing iteration/equilibrium_score fields as MEDIUM. The iteration field is a metadata concern -- it can be added to the verdict without changing the validation logic. The equilibrium_score field depends on an unimplemented integration (FR-006). Both are additive; neither requires redesigning existing code. LOW severity is appropriate for additive gaps.

---

## Additions

### Solution schema is the missing foundation

The devex-advocate identifies the end-to-end gap but does not name the root cause: there is no defined schema for `solution.yml`. The `generate_validation_config()` function accepts a Path, but what should that file contain? For the validation to be meaningful, agents need structured solution data:

- **Objective value**: The optimal value found by the solver
- **Variable assignments**: The decision variable values (x[i] = ...)
- **Constraint slack**: How much margin exists on each constraint
- **Solve status**: optimal, feasible, infeasible, time-limited
- **Solver metadata**: solver name, version, time, gap

Without a solution schema, agents are reviewing an opaque YAML file and guessing at its structure. A `SolverSolution` Pydantic model would standardize the input and enable structured prompts that reference specific solution fields.

### The sensitivity instructions assume solver re-runs but the design does not support them

The devex-advocate notes that sensitivity instructions are "actionable" -- I agree for qualitative analysis but not for quantitative. The instructions say "What happens if this parameter changes by +/-10%?" but the validation flow has no solver re-run capability. A mathematically rigorous sensitivity analysis for anything beyond LP (where dual values give exact local sensitivity) requires re-solving with perturbed parameters. The design should either:
1. Accept that sensitivity analysis is qualitative (LLM-based structural assessment)
2. Add a re-solve mechanism that perturbs parameters and re-runs the solver

Option 1 is honest and achievable. Option 2 is ambitious and valuable. The current implementation implicitly assumes option 2 but implements neither.
