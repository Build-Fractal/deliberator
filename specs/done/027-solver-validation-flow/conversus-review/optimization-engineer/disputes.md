# Phase 4 Disputes: optimization-engineer

**Spec**: 027-solver-validation-flow
**Agent**: optimization-engineer
**Round**: 1

---

## Surviving Disputes

### DISPUTE 1: AMPL constraint feedback loop is structurally broken (HIGH)

**Status**: SURVIVING -- unanimous across all three agents.

FR-010 requires output "consumable by the solver for re-optimization." The `constraint_additions: list[str]` field holds natural-language descriptions that no solver can parse. The gap is not just implementation but also spec-level: FR-010 does not define a constraint interchange format.

**Recommended resolution**: Define a structured constraint format. At minimum, typed constraint templates with parameterized expressions. At best, solver-specific code generation (AMPL, Pyomo) as an output layer.

### DISPUTE 2: End-to-end integration is missing (HIGH)

**Status**: SURVIVING -- unanimous across all three agents.

The validation flow exists as config generation + data models. The CLI command (FR-001), equilibrium scorer integration (FR-006/FR-007), and convergence predictor (FR-012) are completely absent. This represents 5 NOT MET FRs out of 12.

**Recommended resolution**: Implement the CLI command as the integration point. Equilibrium scoring and convergence prediction can be gated behind feature flags with clear "requires spec 021/022" error messages.

### DISPUTE 3: Sensitivity analysis lacks mathematical rigor (MEDIUM)

**Status**: SURVIVING -- optimization-engineer and devex-advocate agree; spec-compliance acknowledges.

Three specific mathematical gaps:
1. RHS vs. cost sensitivity conflation: treating constraint parameter changes and objective coefficient changes as the same "parameter perturbation" produces misleading analysis
2. No leverage of solver-computed dual values: asking LLM agents to derive sensitivity from static YAML when the solver has already computed shadow prices
3. +/-10% perturbation is meaningless for discrete variables: integer/binary parameters require structural sensitivity analysis, not percentage perturbation

**Recommended resolution**: (a) Amend sensitivity instructions to distinguish continuous and discrete parameters. (b) Define a solution schema that includes dual values, enabling agents to use solver-computed sensitivity data. (c) Explicitly label the analysis as "structural assessment" when solver data is unavailable.

### DISPUTE 4: Solution input schema is undefined (MEDIUM)

**Status**: SURVIVING -- optimization-engineer and devex-advocate agree.

`generate_validation_config()` accepts `solution_path: Path` but the file's expected content is unspecified. Without a schema, agents review an opaque file. A `SolverSolution` model would standardize: objective value, variable assignments, constraint slack, solve status, solver metadata.

**Recommended resolution**: Define `SolverSolution` as a Pydantic model in `conversus/schemas/validation.py`. The model should be permissive (most fields optional) to accommodate different solver outputs, but define the canonical structure.

---

## Withdrawn Disputes

- **Cannot catch local optima / numerical infeasibility / degeneracy**: Downgraded from MEDIUM to LOW after spec-compliance correctly noted these are out of scope for the spec's stated purpose (qualitative multi-perspective review, not numerical solver verification).
- **Shadow price extraction**: Downgraded from finding to design suggestion. No FR requires it.
- **Basis stability analysis**: Reclassified as a limitation observation, not a gap.

---

## Settled Points (No Dispute)

- Problem type to agent mapping: CORRECT for implemented types (general, assignment, portfolio)
- Agent prompts contain domain-specific critique instructions (not generic)
- SensitivityFinding model has correct four-field structure
- ValidationVerdict three-valued outcome (accept/revise/reject) is appropriate
- Cooperative mode is the correct choice for validation deliberations (agents collaborate to find issues, not compete)
- Config defaults (iterations: 1, rounds: 1) are reasonable for validation
