# Spec Compliance Review: 013-objective-function-templates

**Reviewer Role**: spec-compliance
**Date**: 2026-03-23
**Spec Version**: Draft (2026-03-22)
**Implementation Scope**: `schema/objective-functions/` YAML templates, `conversus/schemas/objectives.py` Pydantic models

---

## Executive Summary

The implementation delivers a solid and well-structured objective function template library that meets the majority of the spec's requirements. Twenty-one objective function templates and six constraint templates exist, covering all four conversus modes with mode-specific and cross-mode forms. The Pydantic validation models enforce the required fields and cross-field invariants. However, there are several deviations from the spec's letter: the import path differs from FR-011's prescribed `conversus_schemas` package name, the example format is inconsistent across templates, constraint templates lack the `example` fields that SC-005 implicitly requires, and the `cooperative-fairness` template is an addition not listed in the spec's Section 2 catalog. None of these are showstoppers, but several require explicit decisions about whether the spec or the implementation is the source of truth.

---

## Alignment

### 1. Template Schema Structure (FR-001, FR-002) -- MET

Every objective function template is a YAML file located at `schema/objective-functions/{template-name}.yml`. Each contains all eight required fields from FR-002: `name`, `description`, `form`, `game_form`, `mode_compatibility`, `parameters`, `constraints`, and `example`. The field naming, structure, and formatting are consistent across all 21 templates. The file path convention (`schema/objective-functions/` inside the conversus submodule) satisfies the relative path requirement.

### 2. Parameter Definitions (FR-003, FR-004, FR-005) -- MET

Every parameter defines `name`, `type`, and `description` as required. Parameters include `range`, `default`, and `gap_question` where applicable. The `function`-type parameters all specify `derived_from` as required by FR-005 (e.g., `cooperative-integration.yml` has `accepted_recs` derived from "synthesis recommendation scorecard"). Parameters with defaults are treated as optional, and those with `gap_question` are correctly positioned as the gaps for guided construction (FR-004).

### 3. Constraint Template Schema (FR-006, FR-007) -- MET

All six constraint templates reside at `schema/objective-functions/constraints/{name}.yml`. Each defines the four required fields from FR-007: `name`, `form`, `parameters`, and `mode_compatibility`. The six templates map exactly to the spec's Section 2 list: budget, capacity, mutual-exclusivity, minimum-coverage, non-negativity, and bounds.

### 4. Pydantic Validation Models (FR-008, FR-009, FR-010) -- MET

The `objectives.py` module implements `ObjectiveTemplate`, `ConstraintTemplate`, and `ParameterDefinition` as separate Pydantic models. Cross-field invariants are correctly enforced: `mode_compatibility` entries are validated against `VALID_MODES`, `game_form` is validated against `VALID_GAME_FORMS`, function-type parameters require `derived_from`, and range-default consistency is checked. The validators use `model_validator(mode="after")` for clean post-initialization validation.

### 5. Library Completeness -- Counts (FR-012 through FR-015) -- MET

| Requirement | Threshold | Actual Count | Status |
|---|---|---|---|
| FR-012: Total objective templates | >= 20 | 21 | PASS |
| FR-013: Mode-specific per mode (>= 3 each) | 3 per mode | Cooperative: 4, WTA: 3, PD: 3, Red-Blue: 3 | PASS |
| FR-014: Cross-mode templates | >= 5 | 7 (budget-constrained, time-constrained, general-linear, general-quadratic, weighted-sum, minimax, lexicographic) | PASS |
| FR-015: Constraint templates | >= 4 | 6 | PASS |

### 6. No Solver Logic Constraint (Section 5) -- MET

The templates are purely declarative YAML data with no computation. The Pydantic models perform validation only -- no solver imports, no optimization routines, no runtime computation. The `click` dependency in `pyproject.toml` is for the linter CLI, not solver logic.

---

## Missed Opportunities

### 1. FR-011 Import Path Mismatch -- DEVIATION

FR-011 requires: `from conversus_schemas.objectives import ObjectiveTemplate, ConstraintTemplate, ParameterDefinition`. The actual import path is `from conversus.schemas.objectives import ...` (package name `conversus`, subpackage `schemas`). This is a direct deviation from the spec's letter. The `conversus.schemas` path is arguably better (it groups schemas under the main package rather than creating a separate top-level package), but the spec text is unambiguous. Either the spec should be amended to match the implementation, or the implementation should expose a `conversus_schemas` compatibility alias.

### 2. SC-005 Gap: Constraint Templates Have No Example Parameterizations

SC-005 states: "The full library contains 20-30 templates, each with at least one working example parameterization." None of the six constraint templates include an `example` field. This creates ambiguity: does "template" in SC-005 refer only to objective templates, or also to constraint templates? The conservative reading includes constraints, and they currently fail this criterion. Adding minimal examples to each constraint YAML would close this gap.

### 3. `example` Field Format Inconsistency Across Templates

Mode-specific templates (e.g., `cooperative-integration.yml`) use a flat key-value `example` block with just parameter values. Cross-mode templates (e.g., `budget-constrained.yml`, `weighted-sum.yml`) include redundant top-level fields (`name`, `form`, `game_form`) inside the example block plus a `computed_objective` field. This inconsistency means the `ObjectiveTemplate` model validates the example as `dict[str, Any]` without enforcing a specific structure. A standardized example schema would make templates more uniform and machine-parseable.

### 4. SC-001 Cannot Be Verified Without Test Infrastructure

SC-001 requires that `ObjectiveTemplate.model_validate(yaml.safe_load(open("schema/objective-functions/cooperative-integration.yml")))` succeeds. No test file exists for objective template validation (only `tests/test_game_forms.py` exists). This success criterion is currently unverifiable in CI. A `tests/test_objectives.py` file that loads each YAML and validates it against the Pydantic model would close this gap and also serve as a regression guard.

### 5. SC-002 and SC-003 Untested

SC-002 (invalid mode raises ValidationError) and SC-003 (filtering cooperative templates returns >= 3 plus cross-modes) are untested. The Pydantic model logic supports both, but neither has a test proving it works. These are straightforward to implement and would significantly increase confidence.

### 6. `cooperative-fairness` Is an Undocumented Addition

The spec's Section 2 lists exactly three cooperative templates: `cooperative-integration`, `cooperative-quality`, `cooperative-consensus`. The implementation adds a fourth: `cooperative-fairness`. This is a good addition (Rawlsian fairness is a well-motivated objective), but it is not mentioned in the spec. This creates spec-to-implementation drift. The spec's Section 2 should be updated to include it, or the template should be marked as a bonus/extension beyond the spec's catalog.

### 7. No `description` Field on Constraint Templates

While FR-007 does not explicitly require a `description` field for constraints (only `name`, `form`, `parameters`, `mode_compatibility`), FR-002 requires it for objective templates. The asymmetry is defensible from a strict reading, but adding `description` to constraints would improve self-documentation and consistency. The YAML files include header comments that serve as de facto descriptions, but these are not machine-readable.

### 8. No Programmatic Template Discovery or Registry

The spec does not require a template registry, but SC-003 implies the ability to "filter templates by `mode_compatibility`." There is no loader function or registry that discovers YAML files in `schema/objective-functions/`, loads them, and enables filtering. The Pydantic models validate individual files but do not provide collection-level operations. This gap will become the responsibility of spec 014 (guided construction), but a minimal `load_all_templates()` function would make SC-003 testable today.

### 9. No `description` in `ConstraintTemplate` Pydantic Model

The `ConstraintTemplate` Pydantic model has no `description` field. If constraint YAML files are ever extended to include descriptions (see point 7 above), the model will reject them. This is not a current failure but creates a forward-compatibility risk.

---

## Off-Base Assumptions

### 1. `click` Dependency Potentially Violates Section 5 Constraint

Section 5 states: "Must NOT depend on any library beyond pydantic and pyyaml." The `pyproject.toml` lists `click>=8.3.1` as a project dependency. While `click` is used by the linter CLI (`conversus-lint`) and not by the template schema package itself, the dependency is declared at the project level, not isolated to an optional extra or separate package. A strict reading of the constraint considers this a violation. The resolution is either to move `click` to an optional dependency group (e.g., `[project.optional-dependencies] cli = ["click>=8.3.1"]`) or to amend the spec to acknowledge the linter tooling as an exemption.

### 2. Overloading `type: string` for Structured Data

Several parameters use `type: string` for data that is structurally richer than a string. Examples: `Q` in `general-quadratic` is documented as "nested list notation" but typed as `string`; `weights` in `weighted-sum` is "comma-separated values" but typed as `string`; `tolerance` in `lexicographic` is similarly a list encoded as a string. Yet the actual YAML `example` sections provide these as native YAML lists (e.g., `Q: [[2, 0], [0, 2]]`, `weights: [0.5, 0.3, 0.2]`). This creates a type mismatch between the declared parameter type and the example usage. The spec's FR-003 type vocabulary (`float`, `integer`, `string`, `function`) may be too narrow for structured data; an `array` or `object` type could resolve this tension.

### 3. `example` Blocks in Cross-Mode Templates Include Non-Parameter Keys

The `example` block in `budget-constrained.yml`, `time-constrained.yml`, `general-linear.yml`, `general-quadratic.yml`, `weighted-sum.yml`, `minimax.yml`, and `lexicographic.yml` includes keys like `name`, `form`, `game_form`, and `computed_objective` that are not parameter names. This contradicts the spec's FR-002 definition of `example` as a "minimal valid parameterization" -- a parameterization should contain only parameter values. The `ObjectiveTemplate` model accepts this because `example` is typed as `dict[str, Any]`, but it undermines the semantic contract. These extra keys should be removed to match the mode-specific templates' cleaner format, or the spec should clarify what `example` means.

---

## Actionable Recommendations

### 1. CRITICAL: Reconcile Import Path (FR-011)

**Current**: `from conversus.schemas.objectives import ObjectiveTemplate, ConstraintTemplate, ParameterDefinition`
**Required**: `from conversus_schemas.objectives import ObjectiveTemplate, ConstraintTemplate, ParameterDefinition`

Options:
- (a) Amend FR-011 to `from conversus.schemas.objectives import ...` (preferred -- matches actual package structure).
- (b) Create a `conversus_schemas` package alias that re-exports from `conversus.schemas`.

### 2. HIGH: Add `tests/test_objectives.py` Covering SC-001, SC-002, SC-003

Create a test file that:
- Loads every YAML file in `schema/objective-functions/` and validates it against `ObjectiveTemplate` (SC-001).
- Loads every YAML file in `schema/objective-functions/constraints/` and validates it against `ConstraintTemplate`.
- Asserts that a template with `mode_compatibility: ["invalid-mode"]` raises `ValidationError` (SC-002).
- Asserts that filtering templates by `cooperative` mode returns >= 3 mode-specific + all cross-mode templates (SC-003).
- Verifies every template has a non-empty `example` (SC-005).

### 3. HIGH: Standardize `example` Block Format

Remove redundant keys (`name`, `form`, `game_form`) from example blocks in cross-mode templates. Optionally add `computed_objective` as a documentation-only key to all templates for consistency, or remove it everywhere.

### 4. MEDIUM: Add Examples to Constraint Templates (SC-005)

Add an `example` field to each constraint YAML and add a corresponding optional `example` field to the `ConstraintTemplate` Pydantic model. Example for `budget.yml`:
```yaml
example:
  cost: [1.5, 3.0, 2.0]
  B: 10.0
```

### 5. MEDIUM: Update Spec Section 2 to Include `cooperative-fairness`

Add `cooperative-fairness` to the spec's cooperative template list with its formula: `J = -min_i(allocation_i) + phi * variance(allocation)`. This brings the spec in line with the implementation and documents the Rawlsian fairness motivation.

### 6. MEDIUM: Isolate `click` Dependency

Move `click` to an optional dependency group to satisfy the Section 5 constraint:
```toml
[project.optional-dependencies]
cli = ["click>=8.3.1"]
```

### 7. LOW: Consider Adding `array` Parameter Type

The current `type` vocabulary (`float`, `integer`, `string`, `function`) forces structured data like matrices and weight vectors into `string` representation, which conflicts with their YAML-native list usage in examples. Adding `array` (or `list`) as a valid parameter type would resolve the type-example mismatch for `Q`, `c`, `weights`, `tolerance`, and similar parameters.

### 8. LOW: Add `description` to `ConstraintTemplate`

Add an optional `description: Optional[str] = None` field to the `ConstraintTemplate` Pydantic model and populate descriptions in constraint YAML files by promoting the existing header comments to YAML fields. This improves machine readability and consistency with `ObjectiveTemplate`.

### 9. LOW: Implement Minimal Template Registry

Add a `load_all_templates(directory: Path) -> list[ObjectiveTemplate]` function to `objectives.py` (or a new `registry.py` module) that discovers YAML files, validates them, and supports filtering by mode. This makes SC-003 directly testable and provides the foundation for spec 014's guided construction pipeline.

### 10. LOW: Add `computed_objective` Documentation Convention

Formalize `computed_objective` as an optional documentation-only key in examples (not validated by the model but useful for human readers). Apply it consistently across all templates to show what the objective evaluates to with the given parameter values.

---

## Referenced Documentation

| Document | Path | Relevance |
|---|---|---|
| Spec 013 | `conversus/specs/013-objective-function-templates/spec.md` | Primary spec under review |
| Pydantic models | `conversus/conversus/schemas/objectives.py` | Implementation of FR-008, FR-009, FR-010 |
| Package init | `conversus/conversus/schemas/__init__.py` | Export surface for FR-011 |
| Package config | `conversus/pyproject.toml` | Dependency declarations (Section 5 constraint) |
| Conversus README | `conversus/README.md` | Mode definitions and architecture context |
| Cooperative integration | `conversus/schema/objective-functions/cooperative-integration.yml` | Representative mode-specific template |
| Budget constraint | `conversus/schema/objective-functions/constraints/budget.yml` | Representative constraint template |
| Cooperative fairness | `conversus/schema/objective-functions/cooperative-fairness.yml` | Undocumented addition beyond spec catalog |
| Existing tests | `conversus/tests/test_game_forms.py` | Only existing test file; no objectives tests |
