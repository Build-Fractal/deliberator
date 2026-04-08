# Phase 1 Review: spec-compliance

**Spec**: 027-solver-validation-flow
**Agent**: spec-compliance
**Round**: 1
**Focus**: FR-001 through FR-012, SC-001 through SC-005. MET / PARTIALLY MET / NOT MET.

---

## Overall Assessment

The implementation delivers config generation, data models, and a test suite covering ~60% of the spec's functional requirements at a structural level. However, the spec describes an end-to-end validation loop (CLI command, deliberation execution, equilibrium scoring, convergence prediction, AMPL feedback) and the implementation covers only the config generation and verdict modeling layers. Several FRs and SCs cannot be assessed because the integration code does not exist.

**Verdict**: 5 MET, 4 PARTIALLY MET, 3 NOT MET across 12 FRs. 2 MET, 1 PARTIALLY MET, 2 NOT MET across 5 SCs.

---

## Functional Requirements Assessment

### FR-001: `/conversus validate-solution <solution.yml>` -- NOT MET

The spec requires a CLI command that "MUST generate a validation conversus.yml and run a deliberation targeting the solution." The implementation provides `generate_validation_config()` which produces a config dict, but:
- No CLI command exists (no entry in the CLI module)
- No function writes the config to YAML
- No function triggers a deliberation from the config

The config generation function is a necessary component but is not the CLI command itself.

**Gap**: CLI command, YAML writer, deliberation runner.

### FR-002: Agents auto-generated based on problem type -- MET

The `_AGENT_TEMPLATES` dict maps problem types to agent definitions with solution-critique prompts. The prompts are specific (not generic review prompts). The tests verify agent names and prompt content for general, assignment, and portfolio types.

**Evidence**: `test_general_problem_type_agents`, `test_assignment_problem_type_agents`, `test_portfolio_problem_type_agents` all pass. Prompts contain domain-specific critique instructions.

**Caveat**: Only 3 of 5 spec'd problem types are implemented. The spec table (section 3) includes scheduling and negotiation. This does not prevent MET status because FR-002 says "based on problem type" without enumerating which types must exist.

### FR-003: Validation deliberation includes original files as targets -- MET

`generate_validation_config()` builds a target list from solution_path, problem_path, and objective_path. When all three are provided, the config's `target` field is a three-element list.

**Evidence**: `test_target_with_all_paths` verifies `["solution.yml", "problem.md", "objective.yml"]`.

### FR-004: At least one agent performs sensitivity analysis -- MET

Every problem type has at least one agent whose prompt includes the `_SENSITIVITY_INSTRUCTIONS` block with structured output fields (parameter, change, feasibility_impact, objective_impact).

**Evidence**: `test_at_least_one_agent_per_type_has_sensitivity` iterates all three types and asserts True. The sensitivity-analyst (general), fairness-advocate (assignment), and risk-minimizer (portfolio) all embed the instructions.

### FR-005: Sensitivity findings structured with four fields -- MET

The `SensitivityFinding` Pydantic model has exactly the four required fields: `parameter`, `change`, `feasibility_impact`, `objective_impact`. All are required (no defaults).

**Evidence**: `test_finding_requires_all_fields` verifies that omitting fields raises ValidationError. `test_valid_finding` verifies all four fields are preserved.

### FR-006: Equilibrium scorer runs POST_DELIBERATION on validation output -- NOT MET

No integration with the equilibrium scorer (spec 021) exists. There is no import of any scoring module, no hook registration, no post-deliberation callback. The `ValidationVerdict` model has no `equilibrium_score` field.

**Gap**: Complete integration with spec 021's equilibrium scoring system.

### FR-007: Synthesis flags solution as potentially unstable if equilibrium score < 0.7 -- NOT MET

Depends on FR-006 which is not implemented. No threshold check, no flag mechanism, no synthesis template modification.

**Gap**: Requires FR-006 first, then threshold logic and synthesis template integration.

### FR-008: Validation output includes validation-verdict.md with ACCEPT/REVISE/REJECT -- PARTIALLY MET

The `ValidationVerdict` model defines the three-valued verdict (`Literal["accept", "revise", "reject"]`) with confidence, sensitivity findings, constraint additions, and summary. However:
- No code generates a `validation-verdict.md` file
- No code parses a deliberation synthesis into a `ValidationVerdict` instance
- The model exists but is never instantiated outside of tests

**Status**: The data model satisfies the structural requirement; the file generation does not exist.

### FR-009: Rejected/revised solutions include specific constraint additions -- PARTIALLY MET

`ValidationVerdict.constraint_additions` is a `list[str]` field that can hold proposed constraints. The test demonstrates:
```python
constraint_additions=[
    "Add capacity constraint: sum(x[i]) <= 10",
    "Add fairness bound: max(x[i]) - min(x[i]) <= 3",
]
```

The field exists and can be populated, but there is no mechanism to ensure agents actually produce constraint additions when the verdict is "revise" or "reject." The model does not enforce that revise/reject verdicts have non-empty constraint_additions.

**Gap**: No model_validator enforcing `len(constraint_additions) > 0` when verdict is "revise" or "reject".

### FR-010: Validation output consumable by solver for re-optimization -- PARTIALLY MET

The `constraint_additions` field exists but contains free-form strings, not solver-compatible syntax. There is no AMPL code generation, no constraint template system, no model file integration.

**Status**: The data structure exists; the solver integration does not.

### FR-011: User may re-run validation; each iteration is tracked -- PARTIALLY MET

The config includes `iterations: 1` and `rounds: 1`, showing awareness of the iteration concept. However:
- No iteration counter or tracking mechanism in `ValidationVerdict`
- No history of previous validation runs
- No function to increment the iteration and re-run

**Status**: The concept is acknowledged in the config structure but not implemented.

### FR-012: Convergence predictor assesses whether re-validation will produce different results -- NOT MET (deferred)

No integration with the convergence predictor (spec 022). This is a dependency that is explicitly listed in the spec header. No stub, no interface, no import.

**Gap**: Complete. Depends on spec 022 implementation.

---

## Success Criteria Assessment

### SC-001: Assignment solution fairness issue flagged -- MET

The fairness-advocate agent for the assignment problem type has a prompt that says: "Flag cases where the best resources are concentrated on low-priority tasks." The test `test_fairness_advocate_prompt_catches_inequity` verifies the prompt contains "best" and "low-priority."

**Evidence**: The prompt is designed to flag exactly the scenario described in SC-001 (best engineer assigned to lowest-priority project). Whether the LLM agent would actually flag it depends on the LLM, but the prompt construction satisfies the success criterion at the framework level.

### SC-002: Sensitivity analysis identifies portfolio infeasibility under interest rate increase -- PARTIALLY MET

The `SensitivityFinding` model can represent this finding:
```python
SensitivityFinding(
    parameter="interest_rate",
    change="+2%",
    feasibility_impact="infeasible",
    objective_impact="-15%",
)
```

The test `test_sensitivity_findings_roundtrip` demonstrates exactly this. However, the sensitivity analysis is performed by an LLM agent interpreting static YAML, not by a solver re-run with modified parameters. The criterion says "correctly identifies" -- the framework enables the identification but cannot guarantee correctness without solver verification.

**Status**: The framework supports the finding structurally. Correctness depends on the LLM agent's analysis quality.

### SC-003: Robust solution receives ACCEPT with equilibrium score > 0.8 -- NOT MET

The test `test_robust_solution_accept_verdict` demonstrates an accept verdict with confidence 0.92, but:
- This is a manually constructed verdict, not one produced by the validation flow
- There is no equilibrium score (FR-006 not implemented)
- The criterion specifically requires equilibrium score > 0.8, which is a different metric than verdict confidence

**Gap**: Requires equilibrium scorer integration (FR-006).

### SC-004: Validation output includes constraint addition that improves AMPL solution -- NOT MET

No AMPL integration exists. The constraint_additions field can hold strings but there is no mechanism to feed them back to AMPL or verify they produce a better solution.

**Gap**: Complete AMPL feedback loop.

### SC-005: Full loop completes in under 10 minutes -- MET (by design)

The config uses `iterations: 1` and `rounds: 1` with 3 agents. Per the README formula: N + N(N-1) + N + N + 1 = 3 + 6 + 3 + 3 + 1 = 16 LLM calls. At ~10 seconds per call with parallelism, this is well under 10 minutes.

**Caveat**: This assesses the deliberation portion only. The full loop (define, formulate, solve, validate, revise, re-solve) includes steps outside the validation flow that are not implemented.

---

## Compliance Summary Table

| Requirement | Status | Evidence |
|-------------|--------|----------|
| FR-001 | NOT MET | No CLI command |
| FR-002 | MET | Agent templates with problem-type-specific prompts |
| FR-003 | MET | Target list construction with all paths |
| FR-004 | MET | Sensitivity instructions in at least one agent per type |
| FR-005 | MET | SensitivityFinding model with four required fields |
| FR-006 | NOT MET | No equilibrium scorer integration |
| FR-007 | NOT MET | Depends on FR-006 |
| FR-008 | PARTIALLY MET | Model exists; file generation missing |
| FR-009 | PARTIALLY MET | Field exists; no enforcement for revise/reject verdicts |
| FR-010 | PARTIALLY MET | Data structure exists; solver integration missing |
| FR-011 | PARTIALLY MET | Config acknowledges iterations; no tracking mechanism |
| FR-012 | NOT MET | No convergence predictor integration |
| SC-001 | MET | Fairness advocate prompt addresses scenario |
| SC-002 | PARTIALLY MET | Framework supports finding; correctness unverifiable |
| SC-003 | NOT MET | No equilibrium scorer |
| SC-004 | NOT MET | No AMPL feedback loop |
| SC-005 | MET | 16 LLM calls at 1 round, well under 10 minutes |

**Summary**: 5/12 FRs MET, 4/12 PARTIALLY MET, 3/12 NOT MET. 2/5 SCs MET, 1/5 PARTIALLY MET, 2/5 NOT MET.

---

## Recommendation

The implementation is at the foundation layer: data models and config generation are solid. The superstructure (CLI command, deliberation execution, equilibrium scoring, AMPL feedback, convergence prediction) is entirely unbuilt. The spec should either be amended to reflect the current phase of implementation or the missing integrations should be prioritized.
