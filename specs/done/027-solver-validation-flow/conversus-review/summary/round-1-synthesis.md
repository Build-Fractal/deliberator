# Conversus Review Synthesis: 027-solver-validation-flow -- Round 1

**Agents**: devex-advocate, optimization-engineer, spec-compliance
**Phases completed**: P1 (review) -> P2 (cross-review) -> P3 (revision) -> P4 (dispute) -> P5 (synthesis)
**Round**: 1 of 3 (max)
**Targets reviewed**:
- `specs/027-solver-validation-flow/spec.md`
- `conversus/schemas/validation.py`
- `tests/test_validation.py`

---

## Verdict: REVISE

The implementation delivers a solid foundation layer -- config generation, Pydantic data models, and a well-tested agent template system. The mathematical content is directionally correct and the developer-facing API is clean. However, the spec describes an end-to-end validation loop (define, solve, validate, feedback, re-solve) and the implementation covers only the config generation and data modeling layers. Five of twelve functional requirements are NOT MET, primarily due to missing integration with the CLI, equilibrium scorer, convergence predictor, and solver feedback loop.

---

## Consensus Points

1. **Config generation is well-designed**: `generate_validation_config()` produces correct conversus.yml configs with problem-type-specific agents. The function signature is clean, defaults are sensible, and the target list construction handles all combinations of optional paths correctly.

2. **Agent templates are domain-appropriate**: The agent prompts for general, assignment, and portfolio types contain specific, non-overlapping critique instructions. The sensitivity instructions are embedded in the right agents (not all agents). The fairness-advocate prompt directly addresses SC-001.

3. **ValidationVerdict model is structurally sound**: The three-valued verdict (accept/revise/reject) with confidence, sensitivity findings, constraint additions, and summary captures the essential output of a validation deliberation. Pydantic validation enforces type safety and range constraints.

4. **SensitivityFinding model is correctly structured**: The four-field model (parameter, change, feasibility_impact, objective_impact) maps to standard sensitivity analysis output. All fields are required, preventing incomplete findings.

5. **Test suite is thorough for the implemented scope**: 462 lines covering config generation, agent verification, sensitivity instructions, model validation, boundary conditions, and success criteria scenarios. The tests verify both positive and negative cases.

6. **Section 6 constraints are all satisfied**: The validation deliberation uses the standard engine, agents are template-generated (not hardcoded), and the flow does not modify the original solution.

7. **SC-001 is satisfied**: The fairness-advocate prompt for assignment problems instructs the agent to flag best-resource-to-low-priority-task mismatches.

8. **SC-005 is satisfied**: A 3-agent validation deliberation requires 16 LLM calls, completing well under 10 minutes with parallel execution.

---

## DISPUTES_BEGIN

### DISPUTE 1: End-to-end validation flow is unimplemented
- **Severity**: HIGH
- **Agents**: All three (unanimous)
- **Description**: The spec describes a CLI command (`/conversus validate-solution`) that generates a config, runs a deliberation, parses output, and produces a ValidationVerdict. The implementation provides only `generate_validation_config()` and the Pydantic models. Five integration layers are missing: CLI command (FR-001), deliberation runner, output parser, equilibrium scorer (FR-006/FR-007), and convergence predictor (FR-012). This represents 5 NOT MET FRs.
- **Recommendation**: Implement the CLI command as the integration point. Phase the remaining integrations: Phase 2 for CLI + execution, Phase 3 for equilibrium/convergence.
- **Disposition**: SURVIVING

### DISPUTE 2: AMPL constraint feedback loop is structurally broken
- **Severity**: HIGH
- **Agents**: All three (unanimous)
- **Description**: FR-010 requires validation output "consumable by the solver for re-optimization." The `constraint_additions: list[str]` field holds natural-language descriptions (e.g., "Add capacity constraint: sum(x[i]) <= 10") that no solver can parse. The gap is both implementation-level (no structured constraint format) and spec-level (FR-010 does not define a constraint interchange format). The spec-compliance agent revised FR-010 from PARTIALLY MET to NOT MET.
- **Recommendation**: (a) Amend FR-010 to specify a structured constraint format. (b) Replace `list[str]` with typed `ConstraintAddition` objects with expression templates and parameters. (c) Implement solver-specific code generation as a separate layer.
- **Disposition**: SURVIVING

### DISPUTE 3: Solution input schema is undefined
- **Severity**: MEDIUM
- **Agents**: devex-advocate, optimization-engineer (spec-compliance acknowledges)
- **Description**: `generate_validation_config()` accepts `solution_path: Path` but the expected content of the YAML file is unspecified. Agents review an opaque file with no guaranteed structure. A `SolverSolution` Pydantic model (objective value, variable assignments, constraint slack, solve status, solver metadata) would standardize the input, enable structured prompts, and allow pre-deliberation validation.
- **Recommendation**: Define `SolverSolution` model in `conversus/schemas/validation.py`. Make most fields optional to accommodate different solvers.
- **Disposition**: SURVIVING

### DISPUTE 4: Sensitivity analysis misrepresents its nature
- **Severity**: MEDIUM
- **Agents**: All three (unanimous from different angles)
- **Description**: The sensitivity instructions imply quantitative computation ("What happens if parameter X changes by +/-10%?") but the mechanism is qualitative (LLM assessment of static YAML). Three specific gaps: (a) RHS and cost coefficient sensitivity are conflated, (b) solver-computed dual values are not leveraged, (c) +/-10% perturbation is meaningless for integer/binary variables. The instructions should explicitly acknowledge the qualitative nature of the analysis.
- **Recommendation**: Amend instructions to state "structural/qualitative assessment." Distinguish continuous and discrete parameters. Define solution schema that includes dual values when available.
- **Disposition**: SURVIVING

### DISPUTE 5: SC-002 compliance status (CONTESTED)
- **Severity**: LOW
- **Agents**: devex-advocate (NOT MET) vs. spec-compliance (PARTIALLY MET)
- **Description**: SC-002 requires sensitivity analysis to "correctly identify" that a portfolio solution becomes infeasible under interest rate increase. The devex-advocate argues this requires demonstrated end-to-end behavior; the spec-compliance agent argues the framework is designed and equipped to produce such findings (structural satisfaction). The optimization-engineer did not take a strong position.
- **Recommendation**: Run an end-to-end integration test with a portfolio solution. Resolve based on observed behavior.
- **Disposition**: SURVIVING (interpretive disagreement)

### DISPUTE 6: Missing problem types (scheduling, negotiation)
- **Severity**: MEDIUM
- **Agents**: All three (unanimous)
- **Description**: The spec table lists 5 problem types; the implementation covers 3. `problem_type="scheduling"` raises ValueError. Scheduling and negotiation problems have domain-specific validation concerns that generic agents cannot address. FR-002 was revised from MET to PARTIALLY MET.
- **Recommendation**: Add scheduling and negotiation templates to `_AGENT_TEMPLATES`. The spec table provides agent names and roles.
- **Disposition**: SURVIVING

## DISPUTES_END

---

## Action Items

| Priority | Action | Owner | Effort |
|----------|--------|-------|--------|
| HIGH | Implement `/conversus validate-solution` CLI command (FR-001) | devex-advocate + spec-compliance | Medium |
| HIGH | Define structured `ConstraintAddition` model; amend FR-010 spec language | optimization-engineer | Medium |
| MEDIUM | Define `SolverSolution` input schema model | optimization-engineer + devex-advocate | Small |
| MEDIUM | Amend sensitivity instructions: explicitly qualitative, distinguish continuous/discrete | optimization-engineer | Small |
| MEDIUM | Add scheduling and negotiation problem type templates | devex-advocate | Small |
| MEDIUM | Add iteration tracking fields to ValidationVerdict (FR-011) | devex-advocate | Small |
| LOW | Add model_validator: revise/reject requires non-empty constraint_additions (FR-009) | spec-compliance | Trivial |
| LOW | Constrain feasibility_impact to Literal enum | optimization-engineer | Trivial |
| LOW | Add equilibrium_score field to ValidationVerdict (FR-006 prerequisite) | spec-compliance | Trivial |
| LOW | Remove redundant confidence field_validator | devex-advocate | Trivial |
| LOW | Phase the spec: Phase 1 (current), Phase 2 (CLI + execution), Phase 3 (integrations) | spec-compliance | Small |
| INFO | Run end-to-end test to resolve SC-002 dispute | all | Medium |

---

## Compliance Summary (Post-Round 1)

| Category | Total | MET | Partially MET | NOT MET |
|----------|-------|-----|---------------|---------|
| Functional Requirements (FR-001 to FR-012) | 12 | 3 | 3 | 6 |
| Success Criteria (SC-001 to SC-005) | 5 | 2 | 1 | 2 |
| Constraints (Section 6) | 3 | 3 | 0 | 0 |

**FR pass rate**: 3/12 MET (25%), 3/12 PARTIALLY MET (25%), 6/12 NOT MET (50%)
**SC pass rate**: 2/5 MET, 1/5 PARTIALLY MET, 2/5 NOT MET

---

## Trust Scorecard

### devex-advocate
- **Findings raised**: 7 original + 2 new from cross-review = 9
- **Accepted by peers**: 8/9
- **Withdrawn after challenge**: 1 (custom agent extension point)
- **Severity revisions**: Finding #4 downgraded MEDIUM->LOW, Finding #5 upgraded LOW->MEDIUM
- **Accuracy**: 97%
- **Assessment**: Strong end-to-end perspective. Correctly identified the dominant gap. Appropriately withdrew the extension point finding after optimization-engineer's dict argument.

### optimization-engineer
- **Findings raised**: 8 original + 2 new from cross-review = 10
- **Accepted by peers**: 8/10
- **Withdrawn after challenge**: 2 (local optima scope, shadow price requirement)
- **Severity revisions**: Finding #3 downgraded MEDIUM->LOW, Finding #5 downgraded MEDIUM->LOW
- **Accuracy**: 95%
- **Assessment**: Deepest mathematical analysis. AMPL feedback finding was the strongest individual contribution. Appropriately accepted scope corrections from spec-compliance.

### spec-compliance
- **Findings raised**: 17 FR/SC assessments + 3 constraint assessments
- **Revised after challenge**: 3 (FR-002 MET->PARTIAL, FR-010 PARTIAL->NOT MET, FR-011 PARTIAL->NOT MET)
- **Accuracy**: 90% (initial assessments too generous on 3 items; corrected in revision)
- **Assessment**: Most systematic methodology. Compliance matrix is the authoritative reference. Defended SC-002 PARTIALLY MET against devex-advocate with reasonable argument. Revisions were all in the correct direction.

---

## Stagnation Assessment

**Round 1 produced 6 surviving disputes.** Disputes span three severity levels (2 HIGH, 3 MEDIUM, 1 LOW) and cover distinct domains (integration, feedback loop, input schema, sensitivity rigor, compliance interpretation, type coverage). The disputes are substantive, not stylistic. Proceeding to Round 2.
