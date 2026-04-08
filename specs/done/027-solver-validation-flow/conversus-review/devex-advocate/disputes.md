# Phase 4 Disputes: devex-advocate

**Spec**: 027-solver-validation-flow
**Agent**: devex-advocate
**Round**: 1

---

## Surviving Disputes

### DISPUTE 1: End-to-end flow is unimplemented (HIGH)

**Status**: SURVIVING -- unanimous across all three agents.

The spec describes a complete validation loop (CLI command to verdict to solver feedback). The implementation delivers config generation and data models only. Five integration layers are missing: CLI command (FR-001), deliberation runner, output parser, AMPL feedback (FR-010), and convergence predictor (FR-012).

**Recommended resolution**: Implement `/conversus validate-solution` as the entry point that composes: config generation, YAML write, engine execution, output parsing into ValidationVerdict. AMPL feedback and convergence predictor can be stubbed with explicit "not yet implemented" errors.

### DISPUTE 2: AMPL constraint feedback loop is structurally broken (HIGH)

**Status**: SURVIVING -- unanimous across all three agents.

`constraint_additions` as `list[str]` with natural-language descriptions cannot satisfy FR-010 ("consumable by the solver"). The spec itself underspecifies the constraint interchange format. Both the implementation and the spec need amendment.

**Recommended resolution**: (a) Spec amendment: define a structured constraint addition format (type, expression template, parameters). (b) Implementation: replace `list[str]` with `list[ConstraintAddition]` where ConstraintAddition has typed fields. (c) Accept that full AMPL code generation is a separate concern (spec 023 territory).

### DISPUTE 3: Missing solution input schema (MEDIUM)

**Status**: SURVIVING -- devex-advocate and optimization-engineer agree; spec-compliance acknowledges implicitly.

There is no defined schema for `solution.yml`. Agents review an opaque file with unknown structure. A `SolverSolution` Pydantic model (objective value, variable assignments, constraint slack, solve status) would standardize the input.

**Recommended resolution**: Define a `SolverSolution` model in `conversus/schemas/validation.py` and have `generate_validation_config()` accept it (or validate the YAML against it).

### DISPUTE 4: Sensitivity analysis misrepresents its nature (MEDIUM)

**Status**: SURVIVING -- all three agents converge from different angles.

The sensitivity instructions imply quantitative computation (+/-10% impacts) but the mechanism is qualitative (LLM assessment of static YAML). The devex-advocate identifies the DX confusion; the optimization-engineer identifies the mathematical inaccuracy; the spec-compliance agent identifies the compliance risk to FR-004/FR-005.

**Recommended resolution**: Amend the sensitivity instructions to explicitly state "structural/qualitative assessment, not numerical re-solve." Update FR-004/FR-005 language to acknowledge the qualitative nature.

---

## Withdrawn Disputes

- **Custom agent extension point**: Withdrawn after optimization-engineer showed dict is naturally composable.
- **Agent count deviation from spec table**: Withdrawn. The spec table is illustrative; FR-002 does not mandate a count.

---

## Settled Points (No Dispute)

- FR-002 agent templates: CORRECT (all agents agree prompts are domain-specific and well-constructed)
- FR-003 target list: CORRECT (all paths included when provided)
- FR-004 sensitivity instructions: STRUCTURALLY PRESENT (in at least one agent per type)
- FR-005 SensitivityFinding model: STRUCTURALLY COMPLETE (four required fields)
- SC-001 fairness detection: SATISFIED (prompt addresses the scenario)
- SC-005 timing: SATISFIED (16 LLM calls, well under 10 minutes)
- Section 6 constraints: ALL MET (same engine, template-based, no modification)
- ValidationVerdict model: WELL-DESIGNED (three-valued verdict, confidence, findings, additions, summary)
