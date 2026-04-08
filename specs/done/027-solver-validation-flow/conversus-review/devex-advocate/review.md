# Phase 1 Review: devex-advocate

**Spec**: 027-solver-validation-flow
**Agent**: devex-advocate
**Round**: 1
**Focus**: Is generate_validation_config() intuitive? Are auto-agents useful? Sensitivity template actionable? What's missing for end-to-end use?

---

## Overall Assessment

The validation flow has a clean design center: generate a conversus config from a solver solution, run a deliberation, get a structured verdict. The Pydantic models are well-shaped and the test suite demonstrates real-world scenarios. However, there are significant gaps between what the spec promises (a full loop from solve to re-solve) and what the implementation delivers (config generation and verdict models only).

**Verdict**: PARTIAL PASS -- the implemented surface is good, but the end-to-end developer story has critical missing pieces.

---

## Detailed Findings

### 1. generate_validation_config() Intuitiveness -- GOOD WITH GAPS

The function signature is clean:

```python
def generate_validation_config(
    solution_path: Path,
    problem_path: Path | None = None,
    objective_path: Path | None = None,
    problem_type: str = "general",
    output_dir: Path = Path("validation-output"),
) -> dict[str, Any]:
```

**What works well**:
- Path-based API is natural for a CLI workflow
- Optional problem_path/objective_path reflects real usage where a user might only have a solution file
- Default problem_type="general" is a sensible zero-config starting point
- Return type `dict[str, Any]` aligns with the "generate YAML then run" pattern

**What's unintuitive**:
- `problem_type` is a magic string with no discoverability. A developer has to read the source to know the valid values are "general", "assignment", "portfolio". An enum or Literal type would give IDE autocomplete and static analysis. The ValueError message lists valid types, but that's runtime feedback only.
- The returned dict is untyped. A `ValidationConfig` Pydantic model (or TypedDict) would let developers inspect the structure statically and validate before writing to YAML.
- No docstring example. The docstring explains the parameters but doesn't show a single usage example, which is the fastest path to understanding for a new developer.

**Severity**: MEDIUM. The function works but violates the principle of least astonishment for the `problem_type` parameter.

### 2. Auto-Generated Agents -- USEFUL BUT INCOMPLETE

The agent templates per problem type are well-constructed. The prompts are specific enough to guide meaningful review (e.g., the fairness-advocate explicitly says "Flag cases where the best resources are concentrated on low-priority tasks") rather than generic ("review the solution for fairness").

**What works well**:
- Each agent has a distinct, non-overlapping role
- The sensitivity instructions are embedded in the right agents (not all agents, which would be wasteful)
- The assignment fairness-advocate prompt directly addresses SC-001 (best engineer to lowest-priority project)

**What's missing**:
- Only 3 problem types are implemented. The spec's table (section 3) lists 5 types: assignment, scheduling, portfolio, negotiation, general. Scheduling and negotiation are not implemented. The test even acknowledges this -- `test_unknown_problem_type_raises` expects "scheduling" to fail.
- The spec's table shows a 4th agent column for some types (constraint auditor for assignment, dependency checker for scheduling). The implementation uses 3 agents per type. This is not necessarily wrong (3 vs 4 is a design choice) but the deviation from spec is undocumented.
- No mechanism for the user to add custom agents alongside the auto-generated ones. A real-world user will want domain-specific agents (e.g., "regulatory compliance" for healthcare portfolio optimization) mixed with the auto-generated template agents.

**Severity**: MEDIUM. Two of five spec'd problem types are unimplemented; no custom agent extension point.

### 3. Sensitivity Analysis Template -- ACTIONABLE BUT NOT STRUCTURED ENOUGH

The `_SENSITIVITY_INSTRUCTIONS` block is:

```
For each key parameter in the solution, analyze:
- What happens if this parameter changes by +/-10%?
- Does the solution remain feasible?
- How much does the objective value change?
Structure findings as: parameter, change, feasibility_impact, objective_impact
```

This is actionable -- an LLM agent receiving these instructions will produce sensitivity analysis. The `SensitivityFinding` Pydantic model matches the structure described in the instructions, creating a clean contract between the prompt and the output schema.

**What's missing**:
- The instructions say "+/-10%" but don't explain how an LLM agent is supposed to compute this. The agent is reviewing static YAML, not running the solver. It can identify which parameters are sensitive, but it cannot compute exact objective value changes. The instructions should acknowledge this is a qualitative/structural analysis, not a numerical one.
- The `feasibility_impact` field has no defined vocabulary. The test uses "feasible", "infeasible", "marginal" but the model accepts any string. A Literal type or enum would prevent garbage values.
- No guidance on how many parameters to analyze. An agent could produce 2 findings or 20.

**Severity**: LOW. The template works for LLM-based review but blurs the line between quantitative and qualitative analysis.

### 4. ValidationVerdict as Output Model -- WELL-DESIGNED

The Pydantic model is clean:
- `verdict: Literal["accept", "revise", "reject"]` -- clear three-valued outcome
- `confidence: float` with [0.0, 1.0] range -- appropriate
- `sensitivity_findings: list[SensitivityFinding]` -- structured output
- `constraint_additions: list[str]` -- free-form but purposeful
- `summary: str` -- human-readable narrative

The field_validator on confidence is redundant (the `ge=0.0, le=1.0` Field constraint already handles this) but harmless.

**What's missing**:
- No `iteration` field to track which validation pass this is (FR-011 says iterations are tracked)
- No `equilibrium_score` field (FR-006 says the equilibrium scorer runs post-deliberation; the verdict should carry the result)
- No link back to the source files (which solution.yml, which problem.md produced this verdict)

**Severity**: MEDIUM. The model captures the verdict but not the metadata needed for the iteration loop.

### 5. End-to-End Developer Story -- CRITICAL GAPS

A developer trying to use this end-to-end would need to:

1. Have a solution.yml (from AMPL/HiGHS)
2. Call `generate_validation_config()` to get a dict
3. Write the dict to YAML
4. Run the conversus engine with that YAML
5. Parse the output into a `ValidationVerdict`
6. If verdict is "revise", extract `constraint_additions` and feed them back to AMPL

Steps 3-6 have no implementation, no utility functions, no examples. The gap between "here's a config dict" and "here's a validated solution with feedback" is entirely on the developer.

**Specific missing pieces**:
- No `write_validation_config()` or `run_validation()` function that composes steps 2-4
- No function to parse a deliberation's synthesis output into a `ValidationVerdict`
- No function to convert `constraint_additions` into AMPL-compatible constraint syntax (FR-010)
- No integration with the convergence predictor (FR-012) -- not even a stub
- No `/conversus validate-solution` CLI command (FR-001) -- the entry point itself is unimplemented

**Severity**: HIGH. The spec describes a full loop; the implementation delivers only the config generation layer.

---

## Summary of Findings

| # | Severity | Finding |
|---|----------|---------|
| 1 | HIGH | End-to-end flow unimplemented: no CLI command, no config writer, no output parser, no AMPL feedback loop |
| 2 | MEDIUM | problem_type is an untyped magic string with no IDE discoverability |
| 3 | MEDIUM | Only 3 of 5 spec'd problem types implemented (missing scheduling, negotiation) |
| 4 | MEDIUM | ValidationVerdict missing iteration tracking and equilibrium_score fields |
| 5 | LOW | Sensitivity instructions blur quantitative/qualitative analysis boundary |
| 6 | LOW | SensitivityFinding.feasibility_impact accepts any string; should be constrained |
| 7 | INFO | Redundant field_validator on confidence (Field constraint already handles range) |

---

## Recommendation

REVISE. The config generation and data models are solid foundations, but the spec promises an end-to-end validation loop and the implementation stops at config generation. A developer cannot use this to validate a solver solution today without writing significant glue code. Priority actions: implement the CLI command (FR-001), add a config-to-deliberation runner, and add iteration/equilibrium metadata to the verdict model.
