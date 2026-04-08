# Cross-Review: devex-advocate reviewing optimization-engineer

**Spec**: 027-solver-validation-flow
**Reviewer**: devex-advocate
**Subject**: optimization-engineer Phase 1 review
**Round**: 1

---

## Verified Claims

### 1. AMPL feedback loop is unimplementable with free-form strings -- CONFIRMED

The optimization-engineer's strongest finding. A `list[str]` of natural-language constraint descriptions has no path to AMPL syntax without an intermediate translation layer. The suggested `ConstraintAddition` dataclass with typed fields and an `ampl_template` is a much better design. From a developer experience perspective, this is worse than the optimization-engineer states -- a developer would receive constraint_additions strings, have no idea what to do with them, and abandon the feedback loop.

### 2. Sensitivity analysis conflates RHS and cost sensitivity -- CONFIRMED

Valid mathematical point that also has a DX implication: a developer who reads the sensitivity instructions might not understand why two "parameters" with similar +/-10% changes produce completely different behavior (one affects feasibility, one affects optimality). The instructions should at minimum acknowledge the distinction.

### 3. Missing shadow price extraction -- CONFIRMED

This is the most actionable finding from a DX perspective. Solvers already compute dual values. Asking LLM agents to re-derive sensitivity information from static YAML is wasteful. The validation flow should accept solver output that includes dual values and surface them to the agents as grounding data, not ask agents to guess.

---

## Disagreements

### 1. Finding severity: "Cannot catch local optima" is overstated -- MEDIUM should be LOW

The optimization-engineer rates "cannot catch local optima, numerical infeasibility, or degeneracy" as MEDIUM. I disagree with grouping these three issues at the same severity.

- **Local optima**: Fair point, but the spec does not claim to validate nonlinear solver output. The problem types (assignment, portfolio, scheduling, negotiation, general) are overwhelmingly LP/MILP territory where local optima are not an issue (LP is convex; MILP solvers provide optimality gaps). Rating this as a gap is projecting future requirements onto the current spec.
- **Numerical infeasibility**: Valid, but this is a solver configuration issue, not a validation flow issue. The validation flow reviews the solution, not the solver's numerical behavior.
- **Degeneracy**: Valid observation, but degeneracy detection is a specialized solver feature (e.g., Gurobi's solution pool). It is unreasonable to expect a multi-agent critique system to solve this.

Each of these is INFO or LOW individually. Grouping them into a single MEDIUM finding inflates the severity.

### 2. Missing 4th agent is not necessarily wrong

The optimization-engineer flags that the assignment type has 3 agents instead of the spec's 4 (missing "robustness tester"). The spec's table in section 3 is descriptive, not prescriptive -- it shows example agents per problem type. The functional requirements (FR-002) say agents MUST be "auto-generated based on problem type with solution-critique prompts" but do not specify a minimum agent count. Having 3 focused agents is a reasonable design choice that keeps deliberation costs lower.

---

## Additions

### Developer-facing implication of the structured constraint proposal

The optimization-engineer's `ConstraintAddition` dataclass is the right direction, but from a DX perspective it needs one more field: `human_readable: str` -- the natural language explanation of why this constraint is being added. A developer reviewing the validation output needs to understand the intent, not just the AMPL syntax. The technical constraint and the human rationale should travel together.

### Solution metadata is missing from the validation input

The optimization-engineer focuses on output (constraint_additions) but does not mention that the input is also underspecified. The `solution_path` is a Path to a YAML file, but there is no schema for what that YAML file should contain. A solver solution could include objective value, variable assignments, constraint slack values, dual values, solve status, solver name/version. Without a defined input schema, agents are reviewing an opaque file.
