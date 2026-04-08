# Phase 1 Review: schema-engineer

**Spec**: 026-optimization-template-library
**Agent**: schema-engineer
**Focus**: Templates follow YAML schema? gap_question fields present? Constraint references valid?

---

## Executive Summary

All 15 new objective function templates and 4 new constraint templates conform to the established YAML schema structure. The required fields (`name`, `description`, `form`, `game_form`, `mode_compatibility`, `parameters`, `constraints`, `example`) are present in every template. Every non-derived parameter carries a `gap_question` field. All constraint references resolve to existing YAML files in the constraints directory. The test suite (`test_templates_expanded.py`) provides thorough parametric validation.

**Verdict**: PASS with 3 observations (1 Low, 2 Info).

---

## Detailed Findings

### 1. Template Schema Compliance (FR-001, FR-003)

Every new template validates against the `ObjectiveTemplate` Pydantic model, verified by:
- `TestSC003NewTemplatesValidate.test_new_template_validates` -- parametrized over all 15 names
- `TestAllTemplatesValidate.test_template_validates` -- parametrized over all YAML files in the schema directory

Field-by-field audit of the 5 sample templates provided:

| Template | name | description | form | game_form | mode_compat | params | constraints | example |
|----------|------|-------------|------|-----------|-------------|--------|-------------|---------|
| assignment-optimal | PASS | PASS (block scalar) | PASS | gnep | 2 modes | 3 params | 2 refs | 3 keys |
| portfolio-markowitz | PASS | PASS (block scalar) | PASS | parametric | 4 modes | 3 params | 3 refs | 3 keys |
| knapsack-binary | PASS | PASS (block scalar) | PASS | parametric | 3 modes | 3 params | 3 refs | 3 keys |
| network-min-cost | PASS | PASS (block scalar) | PASS | parametric | 4 modes | 3 params | 3 refs | 3 keys |
| set-cover | PASS | PASS (block scalar) | PASS | parametric | 3 modes | 3 params | 3 refs | 3 keys |

All templates use the `>` (folded block scalar) notation for `description`, which is consistent with existing templates. The `form` field uses a quoted string, also consistent.

### 2. gap_question Completeness (FR-002)

The test `TestGapQuestions.test_non_derived_params_have_gap_question` verifies that all non-function-type parameters have a `gap_question` field. Audit of the 5 sample templates:

**assignment-optimal**:
- `cost_matrix` (string): gap_question = "What is the cost of assigning each agent to each task?" -- PRESENT
- `n_agents` (integer): gap_question = "How many agents are available for assignment?" -- PRESENT
- `n_tasks` (integer): gap_question = "How many tasks need to be assigned?" -- PRESENT

**portfolio-markowitz**:
- `expected_returns` (string): gap_question = "What is the expected return for each option?" -- PRESENT
- `covariance_matrix` (string): gap_question = "What is the covariance matrix of returns across options?" -- PRESENT
- `risk_aversion` (float): gap_question = "How risk-averse should the allocation be?..." -- PRESENT

**knapsack-binary**:
- `values` (string): gap_question = "What is the value of each item?" -- PRESENT
- `weights` (string): gap_question = "What is the weight (resource cost) of each item?" -- PRESENT
- `capacity` (float): gap_question = "What is the maximum total weight capacity?" -- PRESENT

**network-min-cost**:
- `arc_costs` (string): gap_question = "What is the transport cost on each arc in the network?" -- PRESENT
- `arc_capacities` (string): gap_question = "What is the maximum flow capacity on each arc?" -- PRESENT
- `supply_demand` (string): gap_question = "What is the supply or demand at each node?" -- PRESENT

**set-cover**:
- `set_costs` (string): gap_question = "What is the cost of each set?" -- PRESENT
- `coverage_matrix` (string): gap_question = "Which elements does each set cover?" -- PRESENT
- `n_elements` (integer): gap_question = "How many elements must be covered?" -- PRESENT

All 15 parameters across 5 sample templates have gap_question fields. The test enforces this across all 15 templates.

### 3. Constraint References (FR-005)

The test `TestTemplateConstraintReferences.test_constraint_refs_exist` verifies that every constraint name referenced by a new template matches a file in `schema/objective-functions/constraints/`.

Constraint reference map for new templates:

| Template | Constraints Referenced | All Exist? |
|----------|----------------------|------------|
| assignment-optimal | mutual-exclusivity, non-negativity | YES |
| assignment-balanced | mutual-exclusivity, non-negativity, bounds | YES |
| portfolio-markowitz | budget, non-negativity, bounds | YES |
| portfolio-robust | budget, non-negativity, bounds | YES |
| knapsack-binary | budget, integrality, non-negativity | YES |
| knapsack-multi | budget, integrality, non-negativity, capacity | YES |
| set-cover | minimum-coverage, integrality, non-negativity | YES |
| network-min-cost | flow-conservation, capacity, non-negativity | YES |
| network-max-flow | flow-conservation, capacity, non-negativity | YES |
| facility-location | budget, integrality, non-negativity | YES |
| scheduling-precedence | precedence, non-negativity | YES |
| scheduling-resource | capacity, precedence, non-negativity | YES |
| epsilon-constraint | bounds, non-negativity | YES |
| goal-programming | bounds, non-negativity | YES |
| pareto-frontier | bounds, non-negativity | YES |

All referenced constraints resolve. New constraints (integrality, cardinality, precedence, flow-conservation) are all present in the constraints directory.

### 4. Template Count (SC-001)

`TestSC001TemplateCount` asserts `len(TEMPLATE_YMLS) >= 35`. The directory listing shows 36 template YAML files (21 existing + 15 new). Threshold met with 1 file of margin.

### 5. Constraint Count (SC-002)

`TestSC002ConstraintCount` asserts `len(CONSTRAINT_YMLS) >= 10`. The directory listing shows exactly 10 constraint files (6 existing + 4 new). Threshold met exactly.

**Observation SE-1 (Info)**: The constraint count meets the threshold with zero margin. If any constraint file is accidentally deleted, renamed, or moved, SC-002 will fail. This is a test robustness concern, not a compliance failure.

### 6. game_form Field

All new templates declare a `game_form` value. The test `test_new_template_has_game_form` verifies the value is not None. Values observed:
- `gnep`: assignment-optimal (appropriate -- agents competing for task allocations)
- `parametric`: portfolio-markowitz, knapsack-binary, network-min-cost, set-cover, and most others (appropriate -- optimization with parameters)

**Observation SE-2 (Low)**: No test validates that game_form values correspond to actual game form YAML files in `schema/game-forms/`. The ObjectiveTemplate model accepts any string for `game_form`. A template with `game_form: nonexistent` would pass all current tests. A cross-reference test would prevent this.

### 7. mode_compatibility Field

All new templates declare at least one compatible mode. The test `test_new_template_has_mode_compatibility` verifies `len >= 1`. Observed patterns:
- 4 modes (all): portfolio-markowitz, network-min-cost (broad applicability)
- 3 modes: knapsack-binary, set-cover (excluding red-blue)
- 2 modes: assignment-optimal (cooperative, winner-take-all only)

**Observation SE-3 (Info)**: Similar to game_form, no test validates that mode_compatibility values are drawn from a known set of valid modes. A template with `mode_compatibility: ["fake-mode"]` would pass.

### 8. New Constraint Template Structure

The 4 new constraint templates follow the `ConstraintTemplate` schema:
- `name`: matches filename stem
- `description`: concise single-line
- `form`: mathematical expression
- `parameters`: list (some have parameters, e.g., flow-conservation has supply_demand; integrality has variable_type)
- `mode_compatibility`: full 4-mode compatibility for all 4 constraints

The constraint schema is simpler than the objective template schema (no `game_form`, `constraints`, or `example` fields).

---

## Concerns

| # | Severity | Item |
|---|----------|------|
| SE-1 | Info | Constraint count at exact threshold (10/10), zero margin |
| SE-2 | Low | game_form values not cross-validated against game-forms/*.yml |
| SE-3 | Info | mode_compatibility values not validated against known mode set |

---

## Recommendation

**Accept.** The template library is structurally sound, gap_questions are complete, constraint references are valid, and the test suite provides comprehensive parametric validation. The Low concern (SE-2) is a test coverage gap that should be addressed with a cross-reference test.
