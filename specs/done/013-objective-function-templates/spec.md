# Feature Specification: Objective Function Template Library

**Feature ID**: `013-objective-function-templates`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `012-game-form-schemas` (game form Pydantic models, YAML schema conventions)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 11 Approach 2: Symbolic Logic Templates, decision Q6: curated template library of ~29 forms). See also `archive/game-engine-vision/decisions/Q06-objective-function-templates.md`.

---

## 1. Feature Summary

A curated library of ~20-30 canonical objective function templates, parameterized and customizable. Each template defines a known mathematical form, the parameters users must provide, the gaps an LLM should ask about, and which conversus modes the template applies to.

Templates are the bridge between "what kind of decision is this?" (spec 008 mode selection) and "what mathematical function should we optimize?" (spec 014 guided construction). They are stored as YAML files, validated by Pydantic models, and consumed by the guided construction pipeline and the plugin system.

The library ships curated and mathematically validated for v1 (per decision Q6). Community contributions come later.

**What changes**: New `schema/objective-functions/` directory with ~25 YAML template files. New Pydantic models for template validation. Standard constraint templates.

**What does not change**: SKILL.md. Template system. Execution engine. No solver logic.

---

## 2. Template Categories

### Per-Mode Templates

**Cooperative**:
- `cooperative-integration`: `J = -accepted_recs + lambda * disputes` -- minimize disputes, maximize accepted recommendations
- `cooperative-quality`: `J = -quality_score + mu * revision_count` -- maximize quality, penalize excessive revision
- `cooperative-consensus`: `J = -agreement_rate + nu * holdout_penalty` -- maximize agreement, penalize holdouts

**Winner-Take-All**:
- `competitive-selection`: `J = -w * score + penalty * overlap` -- maximize score, penalize overlap with competitors
- `competitive-ranking`: `J = -rank_position` -- maximize ranking position (simplest WTA form)
- `competitive-threshold`: `J = -score * I(score > threshold)` -- maximize score only if above a quality threshold

**Prisoners Dilemma**:
- `territory-claiming`: `J = territory - gamma * overreach` -- maximize territory, penalize overreach into contested areas
- `territory-cooperative`: `J = territory + delta * shared_benefit - gamma * overreach` -- territory with cooperation incentive
- `boundary-negotiation`: `J = -boundary_violations + sigma * clarity` -- minimize violations, maximize boundary clarity

**Red-Blue**:
- `risk-adversarial`: `J_red = -confirmed_risks; J_blue = -mitigated` -- adversarial risk assessment
- `risk-severity`: `J_red = -sum(severity * confirmed); J_blue = -sum(severity * mitigated)` -- severity-weighted
- `risk-coverage`: `J_red = -coverage_of_attack_surface; J_blue = -coverage_of_defenses` -- coverage-based

### Cross-Mode Templates

- `budget-constrained`: `J = quality - beta * agent_cost` -- quality within budget (any mode)
- `time-constrained`: `J = quality - tau * rounds_used` -- quality within round budget (any mode)
- `general-quadratic`: `J = (1/2) x^T Q x + p^T x` -- standard quadratic form (any mode)
- `general-linear`: `J = c^T x` -- simplest possible form (any mode)
- `weighted-sum`: `J = sum(w_i * f_i(x))` -- weighted sum of sub-objectives (any mode)
- `minimax`: `J = max_i(f_i(x))` -- minimize worst-case outcome (any mode)
- `lexicographic`: `J = [f_1(x), f_2(x), ...]` -- prioritized objectives (any mode)

### Constraint Templates

Standard constraints that can be attached to any objective:
- `budget`: `sum(cost_i * x_i) <= B` -- total cost within budget
- `capacity`: `sum(x_i) <= C` -- total allocation within capacity
- `mutual-exclusivity`: `sum(x_i) = 1` -- exactly one option selected (WTA)
- `minimum-coverage`: `sum(x_i) >= K` -- at least K options included
- `non-negativity`: `x_i >= 0` for all i
- `bounds`: `l_i <= x_i <= u_i` -- per-variable bounds

---

## 3. Functional Requirements

### Template Schema

- **FR-001**: Each objective function template MUST be a YAML file at `schema/objective-functions/{template-name}.yml`.
- **FR-002**: Each template MUST define:
  - `name`: string identifier (matches filename)
  - `description`: plain-language explanation of what this objective captures
  - `form`: symbolic mathematical expression (LaTeX-like notation)
  - `game_form`: reference to a game form from spec 012 (`gnep`, `normal-form`, etc.)
  - `mode_compatibility`: list of conversus modes this template applies to
  - `parameters`: list of parameter definitions
  - `constraints`: list of compatible constraint templates (references)
  - `example`: minimal valid parameterization

### Parameter Definitions

- **FR-003**: Each parameter MUST define: `name`, `type` (float, integer, string, function), `description` (plain-language), `range` (valid values, if bounded), `default` (if applicable), `gap_question` (the plain-language question to ask the user when this parameter is not specified).
- **FR-004**: Parameters with `gap_question` defined are the "gaps" that the guided construction pipeline (spec 014) fills interactively. Parameters with defaults are optional.
- **FR-005**: Parameters of type `function` MUST specify `derived_from` indicating which deliberation artifact provides the value (e.g., "synthesis recommendation scorecard", "cross-review contradiction count").

### Constraint Template Schema

- **FR-006**: Each constraint template MUST be a YAML file at `schema/objective-functions/constraints/{constraint-name}.yml`.
- **FR-007**: Each constraint MUST define: `name`, `form` (symbolic expression), `parameters` (same schema as objective parameters), `mode_compatibility`.

### Pydantic Models

- **FR-008**: An `ObjectiveTemplate` Pydantic model MUST validate template YAML files, enforcing required fields, type constraints, and cross-field invariants (e.g., `mode_compatibility` entries must be valid mode names).
- **FR-009**: A `ConstraintTemplate` Pydantic model MUST validate constraint YAML files.
- **FR-010**: A `ParameterDefinition` Pydantic model MUST validate individual parameter entries, including range validation (min <= default <= max when all three are present).
- **FR-011**: Models MUST be importable as `from conversus_schemas.objectives import ObjectiveTemplate, ConstraintTemplate, ParameterDefinition`.

### Library Completeness

- **FR-012**: The library MUST ship with at least 20 objective function templates covering all four modes.
- **FR-013**: Each mode MUST have at least 3 mode-specific templates.
- **FR-014**: At least 5 cross-mode templates MUST be included.
- **FR-015**: At least 4 constraint templates MUST be included.

### Package

- **FR-016**: Templates and models MUST ship in the `conversus-schemas` package alongside game form schemas (spec 012). No additional dependencies beyond `pydantic` and `pyyaml`.

---

## 4. Success Criteria

- **SC-001**: `ObjectiveTemplate.model_validate(yaml.safe_load(open("schema/objective-functions/cooperative-integration.yml")))` succeeds.
- **SC-002**: A template with `mode_compatibility: ["invalid-mode"]` raises `ValidationError`.
- **SC-003**: Given mode `cooperative`, filtering templates by `mode_compatibility` returns at least 3 cooperative-specific templates plus all cross-mode templates.
- **SC-004**: Every template's `gap_question` fields produce sensible plain-language questions (manual review during acceptance).
- **SC-005**: The full library contains 20-30 templates, each with at least one working example parameterization.

---

## 5. Constraints

- **Must NOT include solver logic.** Templates are data, not computation. They describe mathematical forms — they do not solve them.
- **Must NOT modify SKILL.md.** Templates are consumed by Python code (guided construction, plugins), not by the template orchestrator.
- **Must NOT depend on any library beyond pydantic and pyyaml.** Templates are pure schema.
- **Must NOT generate templates automatically.** The v1 library is curated and mathematically validated (decision Q6). Automated generation is a future concern.
