# Phase 3 Revision: devex-advocate

**Spec**: 027-solver-validation-flow
**Agent**: devex-advocate
**Round**: 1

---

## Position Changes After Cross-Review

### MAINTAINED: Finding #1 (End-to-end gap) -- HIGH, confirmed

Both cross-reviewers reinforce this finding:
- **optimization-engineer** confirms the gap, adding that config generation without a solver runner is "analogous to generating a model file without having a solver to run it."
- **spec-compliance** maps the gap precisely to NOT MET FRs (FR-001, FR-006, FR-007, FR-012).

No change to severity or recommendation.

### REVISED: Finding #2 (problem_type as untyped string) -- MAINTAINED at MEDIUM

Both cross-reviewers confirm the finding:
- **optimization-engineer** confirms from a solver domain perspective (problem types are always enums in solver tools).
- **spec-compliance** agrees it aligns with FR-002's spirit.

I accept the optimization-engineer's reframing that the missing types (scheduling, negotiation) are a domain coverage issue, not just a DX issue. The developer experience problem (no autocomplete) and the domain coverage problem (3/5 types) are distinct but both stem from the same design choice (magic string instead of enum).

### REVISED: Finding #3 (Missing problem types) -- UPGRADED to include domain argument

The optimization-engineer's point is strong: scheduling and negotiation problems have fundamentally different validation concerns that generic agents cannot address. A scheduling solution with a bad makespan due to unexploited critical-path dependencies would not be caught by general agents. This is not just "2 types are missing" -- it is "2 domains are unreachable."

I accept the reframing but maintain MEDIUM severity. The types can be added incrementally.

### REVISED: Finding #4 (ValidationVerdict metadata) -- DOWNGRADED from MEDIUM to LOW

The optimization-engineer argues that missing iteration/equilibrium_score fields are additive gaps that do not require redesigning existing code. I accept this. The fields can be added to the model without changing any existing behavior. LOW is appropriate for additive-only changes.

However, I accept the spec-compliance agent's point that these are compliance gaps (FR-011, FR-006), not just DX gaps. The compliance dimension makes them actionable even at LOW severity.

### MAINTAINED: Finding #5 (Sensitivity qualitative/quantitative blur) -- REVISED from LOW to MEDIUM

The spec-compliance agent argues this should be MEDIUM because it affects the trustworthiness of FR-004/FR-005 satisfaction. I accept this upgrade. The sensitivity instructions direct agents to produce findings that look quantitative but are qualitatively derived. A developer reading `objective_impact: "-15%"` would reasonably assume this was computed, not estimated. The instructions should explicitly state that findings are LLM-assessed structural analysis, not solver-computed values.

The optimization-engineer's cross-review reinforces this: the sensitivity analysis should either (1) acknowledge it's qualitative or (2) leverage solver-computed dual values. Option 1 is honest and achievable today; option 2 is correct but requires solver integration.

### REVISED: Finding #6 (feasibility_impact unconstrained) -- MAINTAINED at LOW

The spec-compliance agent adds compliance teeth: FR-005 requires "impact on solution feasibility," and a free-form string allows meaningless values. A `Literal["feasible", "infeasible", "marginal", "unknown"]` vocabulary would satisfy both the DX concern (discoverability) and the compliance concern (decision-relevant information).

### WITHDRAWN: Custom agent extension point concern

The optimization-engineer correctly argues that the dict-based return type is the extension point. Appending to `config["agents"]` is trivial. The concern was misplaced.

### NEW: Solution input schema is missing (from optimization-engineer)

The optimization-engineer identifies a foundational gap I missed: there is no defined schema for `solution.yml`. The function accepts a Path but the file's expected content is undefined. Without a `SolverSolution` model (objective value, variable assignments, constraint slack, solve status), agents are reviewing an opaque file. This is both a DX problem (developers don't know what to put in solution.yml) and a quality problem (agents can't reliably parse unstructured input).

**Severity**: MEDIUM. This is a foundation-level gap that affects the quality of all downstream analysis.

### NEW: Revise/reject should enforce constraint_additions (from spec-compliance)

The spec-compliance agent's observation about FR-009 is actionable. A model_validator enforcing non-empty constraint_additions for revise/reject verdicts would make the data model self-documenting and close the FR-009 compliance gap.

**Severity**: LOW. Straightforward model_validator addition.

---

## Revised Finding Table

| # | Severity | Finding | Status |
|---|----------|---------|--------|
| 1 | HIGH | End-to-end flow unimplemented (CLI, runner, parser, AMPL feedback, convergence) | Surviving -- unanimous |
| 2 | MEDIUM | problem_type is an untyped magic string | Surviving -- unanimous |
| 3 | MEDIUM | Only 3 of 5 problem types; scheduling/negotiation domains unreachable | Surviving -- reframed with domain argument |
| 4 | MEDIUM | Sensitivity analysis qualitative/quantitative blur (upgraded from LOW) | Surviving -- spec-compliance concurs |
| 5 | MEDIUM | No solution input schema (SolverSolution model) | New -- from optimization-engineer |
| 6 | LOW | ValidationVerdict missing iteration and equilibrium_score fields (downgraded from MEDIUM) | Surviving -- severity revised |
| 7 | LOW | feasibility_impact unconstrained; should be Literal enum | Surviving |
| 8 | LOW | Revise/reject verdicts should enforce non-empty constraint_additions | New -- from spec-compliance |
| 9 | INFO | Redundant field_validator on confidence | Surviving |
