# Phase 1 Review: schema-engineer

**Spec**: 026-optimization-template-library
**Agent**: schema-engineer
**Focus**: YAML schema compliance, gap_question completeness, constraint reference validity

---

## Overall Assessment

All 15 new templates follow the established YAML schema structure (`name`, `description`, `form`, `game_form`, `mode_compatibility`, `parameters`, `constraints`, `example`). The test suite (`test_templates_expanded.py`) provides parametric validation of every template against the `ObjectiveTemplate` Pydantic model. Constraint references are validated against existing constraint files.

**Verdict**: PASS.

---

## Detailed Findings

### 1. Template Schema Compliance

All 15 new templates have the required fields:
- `name`: matches the file stem (verified by test)
- `description`: present as YAML block scalar
- `form`: mathematical expression string
- `game_form`: references valid game form (gnep, parametric, normal-form)
- `mode_compatibility`: non-empty list
- `parameters`: list of parameter objects with name, type, description
- `constraints`: list of constraint references
- `example`: dict with at least one key

The `TestAllTemplatesValidate` class runs `ObjectiveTemplate.model_validate()` on every template YAML (old and new), ensuring schema-model consistency.

### 2. gap_question Completeness

The test `TestGapQuestions.test_non_derived_params_have_gap_question` verifies that all non-function parameters have a `gap_question` field. This is critical for the construction pipeline (spec 014).

Reviewing the sample templates:
- **assignment-optimal**: 3 parameters, all have gap_question -- PASS
- **portfolio-markowitz**: 3 parameters, all have gap_question -- PASS
- **knapsack-binary**: 3 parameters, all have gap_question -- PASS
- **network-min-cost**: 3 parameters, all have gap_question -- PASS
- **set-cover**: 3 parameters, all have gap_question -- PASS

The test skips `type: function` parameters (which are derived). This is the correct exclusion criterion.

### 3. Constraint References

The test `TestTemplateConstraintReferences.test_constraint_refs_exist` verifies that every constraint referenced by a new template corresponds to an existing constraint YAML file. This prevents broken references.

New templates reference the following constraints:
- `mutual-exclusivity`, `non-negativity` (existing)
- `budget`, `bounds`, `capacity` (existing)
- `minimum-coverage` (existing)
- `integrality`, `cardinality`, `precedence`, `flow-conservation` (new)

All referenced constraints exist in `schema/objective-functions/constraints/`.

### 4. Template Count Verification

`TestSC001TemplateCount` asserts `len(TEMPLATE_YMLS) >= 35`. The glob `SCHEMA_DIR.glob("*.yml")` collects all templates. With 20 existing + 15 new = 35 minimum. Current count from the file listing shows approximately 41 template YAMLs (including the existing ones), so this passes comfortably.

### 5. Constraint Count Verification

`TestSC002ConstraintCount` asserts `len(CONSTRAINT_YMLS) >= 10`. The constraints directory has:
- Existing: bounds, budget, capacity, minimum-coverage, mutual-exclusivity, non-negativity (6)
- New: integrality, cardinality, precedence, flow-conservation (4)
- Total: 10

This meets the threshold exactly.

### 6. game_form Field Consistency

All new templates declare a `game_form`:
- Most use `parametric` or `gnep` -- appropriate for optimization problems with parameters
- `assignment-optimal` uses `gnep` (agents competing for tasks) -- reasonable

The test `test_new_template_has_game_form` verifies this is not None.

### 7. mode_compatibility Field

The test `test_new_template_has_mode_compatibility` verifies at least one mode per template. All templates declare 2-4 compatible modes, typically including `cooperative` and `winner-take-all`.

---

## Concerns

| # | Severity | Item |
|---|----------|------|
| 1 | Info | Constraint count meets threshold exactly (10). Adding one more template could break it if it references a new constraint that doesn't exist yet. |
| 2 | Info | No validation that game_form values in templates reference existing game form YAML schemas |

---

## Recommendation

Accept. The template library is well-structured, gap_questions are complete, constraint references are valid, and the test suite provides comprehensive parametric validation.
