# Functional Architect Review: 013 Objective Function Templates

**Reviewer**: functional-architect
**Perspective**: Composability, type safety, immutability, Constitution Principle IX compliance
**Date**: 2026-03-23

---

## Executive Summary

The objective function template library establishes a solid foundation: YAML templates as data, Pydantic models as validators, clear separation from solver logic. The spec and implementation correctly identify templates as the bridge between mode selection and guided construction, and the models follow several game_forms.py patterns (frozenset constants, model_validator, descriptive errors). However, the type system is doing too little work, composability between ObjectiveTemplate and ConstraintTemplate is non-existent at the model level, several validation gaps leave structurally invalid templates undetected, and there is no loader function analogous to `load_mode_mapping` for discovering and validating the template library. The result is a schema layer that validates individual files but cannot validate the library as a coherent whole.

---

## Alignment (What the spec and implementation get right)

### A1. Templates as immutable data, not computation

The spec's Constraint 1 ("Must NOT include solver logic") and the module docstring's "pure schema validation only" commitment align perfectly with Constitution IX's preference for immutable data structures and stateless validation. Templates are frozen YAML artifacts; models validate but never mutate them. This is the correct decomposition.

### A2. Frozenset constants for open registries

`VALID_PARAMETER_TYPES`, `VALID_MODES`, and `VALID_GAME_FORMS` all use `frozenset[str]`, matching the game_forms.py pattern exactly and following the Constitution IX guidance: open registries use `str` with `frozenset` validation, not `StrEnum`. This is consistent and correctly motivated -- mode names are data-driven, not code-path triggers.

### A3. Cross-field validators with descriptive errors

The `model_validator(mode="after")` pattern on ParameterDefinition, ConstraintTemplate, and ObjectiveTemplate mirrors game_forms.py's approach (NormalFormGame, GNEPGame, StackelbergGame all use the same pattern). Error messages include the field name, the invalid value, and the valid set -- matching the "principle of least surprise" requirement from Constitution IX.

### A4. Correct game_form-to-mode correspondence

Each YAML template's game_form selection is well-motivated: cooperative templates use GNEP (shared constraints), competitive templates use normal-form (simultaneous selection), prisoners-dilemma uses GNEP (coupled territory constraints), red-blue uses stackelberg (leader-follower). Cross-mode templates correctly use parametric (external parameter vector). This mapping is internally consistent with the mode-mapping schema from spec 012.

### A5. Function-type parameters require derived_from

FR-005 enforcement via the model_validator is correct and important. It ensures every function-type parameter documents which deliberation artifact provides its value, connecting templates to the deliberation pipeline. This is a real invariant, not ceremony.

### A6. Separation of constraint templates from objective templates

The architectural decision to make constraints composable attachments rather than embedded sub-objects is sound. A `budget` constraint template can be referenced by `cooperative-integration`, `risk-adversarial`, and `budget-constrained` without duplication. This follows the Single Source of Truth principle (Constitution XI).

---

## Missed Opportunities

### M1. No composability mechanism between ObjectiveTemplate and ConstraintTemplate

ObjectiveTemplate.constraints is `list[str]` -- bare string references to constraint template names. There is no mechanism to:
- Resolve constraint references to actual ConstraintTemplate instances
- Validate that referenced constraint names correspond to existing constraint YAML files
- Verify parameter compatibility between an objective's parameters and its referenced constraints' parameters
- Compose an ObjectiveTemplate with its ConstraintTemplates into a validated whole

In game_forms.py, the models validate structural relationships internally (payoff matrix dimensions match strategy cardinalities, objectives match players). Here, the cross-model relationship is unvalidated. A template can reference `constraints: [nonexistent-constraint]` and pass validation.

**Recommendation**: Add a `ComposedObjective` model or a `resolve_constraints` function that takes an ObjectiveTemplate and a dict of loaded ConstraintTemplates, validates all references resolve, and returns an immutable composed result.

### M2. The type system is dangerously loose -- `string` is a type-theoretic junk drawer

The `type` field in ParameterDefinition accepts `Literal["float", "integer", "string", "function"]`, but `string` is carrying at least four distinct semantic roles:

- **Vectors**: `weights` ("0.5, 0.3, 0.2"), `p` ("-4, -6"), `cost` ("1.5, 3.0, 2.0")
- **Matrices**: `Q` ("[[2, 0], [0, 2]]")
- **Booleans**: `normalize` ("true" or "false")
- **Enumerations**: `territory_granularity` ("section", "paragraph", "sentence", "topic"), `confirmation_standard` ("plausible", "demonstrated", "proven")

This means the Pydantic model cannot validate any of these values meaningfully. A parameter declared as type `string` with `default: "true"` that is semantically boolean cannot be range-checked, cannot be validated against allowed values, and cannot be parsed by the guided construction pipeline (spec 014) without out-of-band knowledge.

**Recommendation**: Extend VALID_PARAMETER_TYPES to include at least `vector`, `matrix`, `boolean`, and `enum`. For `enum`, add an `allowed_values` field to ParameterDefinition. This gives spec 014's pipeline something to work with when generating gap-filling prompts.

### M3. No loader function for the template library

game_forms.py provides `load_mode_mapping()` -- a single function that discovers, loads, and validates the mode-mapping YAML. objectives.py provides no equivalent. There is no way to:
- Discover all template YAML files in `schema/objective-functions/`
- Load and validate them in bulk
- Filter templates by mode
- Verify library completeness (FR-012 through FR-015)

The success criteria SC-003 ("filtering templates by mode_compatibility returns at least 3 cooperative-specific templates plus all cross-mode templates") is untestable without a loader.

**Recommendation**: Add `load_objective_templates(path: Path | None = None) -> dict[str, ObjectiveTemplate]` and `load_constraint_templates(path: Path | None = None) -> dict[str, ConstraintTemplate]` following the `load_mode_mapping` pattern. These become the authoritative entry point for spec 014's guided construction pipeline.

### M4. No duplicate parameter name validation

Nothing prevents a template from declaring two parameters with the same name. The YAML would parse, the Pydantic model would accept a `parameters` list with `[{name: "x", ...}, {name: "x", ...}]`, and downstream consumers would silently shadow one definition with the other. game_forms.py validates player-set/strategy-set uniqueness implicitly via dict keys; here, parameters are a list and get no uniqueness check.

**Recommendation**: Add a model_validator to ObjectiveTemplate and ConstraintTemplate that checks `len(set(p.name for p in self.parameters)) == len(self.parameters)`.

### M5. Empty mode_compatibility is silently accepted

Both ObjectiveTemplate and ConstraintTemplate validate that mode_compatibility entries are valid mode names, but neither validates that the list is non-empty. A template with `mode_compatibility: []` passes validation but is unreachable -- it applies to no mode and would never be selected by the guided construction pipeline. This is dead infrastructure that the model should prevent.

**Recommendation**: Add `if not self.mode_compatibility: raise ValueError(...)` to both validators.

### M6. Example field is structurally unvalidated

ObjectiveTemplate.example is `dict[str, Any]` -- a completely untyped bag. The spec requires "minimal valid parameterization" (FR-002), but the model cannot verify that the example's keys correspond to the template's parameter names, that the values are type-compatible, or that the example satisfies range constraints. game_forms.py's models validate structural invariants deeply (recursive matrix dimension checking); here, the example is opaque.

**Recommendation**: Add a model_validator that checks every parameter name appears as a key in the example dict (unless the parameter has a default), and that example values for typed parameters (float, integer) pass range checks.

### M7. ConstraintTemplate has no `description` field

ObjectiveTemplate requires `description` (FR-002). ConstraintTemplate does not, despite FR-007 implicitly requiring human-readable documentation for constraints. The budget.yml constraint has no description field; it relies on in-YAML comments. This is inconsistent and means the guided construction pipeline has no programmatic access to constraint descriptions for plain-language explanations (Constitution XVI: Mathematical Transparency).

**Recommendation**: Add `description: str` to ConstraintTemplate.

### M8. No schema directory resolution for objectives

game_forms.py has `_schema_dir()` that resolves the path to `schema/game-forms/` relative to the package. objectives.py has no equivalent. Without it, any future loader function will need to re-derive the path, violating DRY and introducing drift risk.

**Recommendation**: Add `_objective_schema_dir()` and `_constraint_schema_dir()` helper functions following the same pattern as `_schema_dir()`.

### M9. YAML example structures are inconsistent across templates

Some templates use flat key-value examples (`cooperative-integration.yml`: `{accepted_recs: 12, disputes: 3, ...}`). Others embed the full template structure inside the example (`weighted-sum.yml`: `{name: weighted-sum, form: ..., game_form: ..., parameters: {...}}`). The spec says "minimal valid parameterization," which suggests the flat form. The nested form duplicates the template structure inside its own example field, violating Constitution XI (Single Source of Truth).

**Recommendation**: Standardize all examples to the flat parameter-values-only form. Document the convention in the spec.

---

## Off-Base Assumptions

### O1. Constraint references as bare strings will survive composition

The assumption that `constraints: ["budget", "non-negativity"]` is sufficient breaks down at every composition boundary. The guided construction pipeline (spec 014) will need to resolve these references to actual ConstraintTemplate instances, validate parameter compatibility, and present constraint parameters alongside objective parameters for gap-filling. Bare strings defer all this work to the consumer without providing any resolution mechanism. This is not just an incomplete feature -- it is an architectural assumption that downstream can handle unresolved references, which contradicts the "Templating Engines Over Inference" principle (Constitution VIII). The resolution mechanism should be deterministic and provided by the schema layer, not inferred by the consumer.

### O2. The `range` field as an untyped dict is adequate

`ParameterDefinition.range` is `Optional[dict[str, Any]]`. The validator checks for `min` and `max` keys but does not enforce structure. A range could contain `{"min": 0, "max": 5, "banana": true}` and pass validation. Worse, the budget.yml constraint has `range: {min: 0}` on a string-type parameter (`cost`), which is semantically incoherent -- `min: 0` on a comma-separated string has no meaning. The lack of type-aware range validation means the range field is a suggestion to humans, not a machine-enforceable constraint.

### O3. The `form` field as a plain string provides mathematical transparency

Constitution XVI requires that "every objective function template documents its mathematical form." The `form` field is a free-text string (`"J = -accepted_recs + lambda * disputes"`). This is human-readable but not machine-parseable. The spec assumes this is sufficient for the guided construction pipeline, but spec 014 will eventually need to map parameter names to positions in the mathematical expression. A plain string makes this mapping dependent on naming conventions and string parsing rather than structured data. This is not necessarily wrong for v1, but the assumption that `form` as a string is the long-term representation should be explicit.

---

## Actionable Recommendations

### R1. Add a `load_objective_templates()` function (Priority: High)

Follow the `load_mode_mapping()` pattern from game_forms.py. This function should:
1. Accept an optional `path` argument defaulting to the bundled schema directory.
2. Discover all `.yml` files in `schema/objective-functions/` (excluding `constraints/`).
3. Load each through `ObjectiveTemplate.model_validate()`.
4. Return a `dict[str, ObjectiveTemplate]` keyed by template name.
5. Validate library completeness: at least 20 templates, every mode has 3+ templates, 5+ cross-mode templates.

Add a parallel `load_constraint_templates()` for `schema/objective-functions/constraints/`.

**Constitution alignment**: IX (stateless function), XII (no dead infrastructure -- ensures every YAML file is loadable).

### R2. Add a `validate_library_integrity()` function (Priority: High)

A pure function that takes `dict[str, ObjectiveTemplate]` and `dict[str, ConstraintTemplate]` and validates cross-references:
- Every constraint name referenced in any ObjectiveTemplate.constraints exists in the constraint dict.
- Every mode in every template's mode_compatibility is represented by at least 3 mode-specific templates.
- FR-012 through FR-015 completeness checks.

**Constitution alignment**: IX (composable pure function), V (observable validation).

### R3. Extend the parameter type system (Priority: High)

Add `"vector"`, `"matrix"`, `"boolean"` to VALID_PARAMETER_TYPES. Consider `"enum"` with an `allowed_values: list[str]` field on ParameterDefinition. Update the model_validator:
- `boolean` type: validate default is `"true"` or `"false"` (or native bool).
- `enum` type: validate default is in `allowed_values`.
- `vector`/`matrix` type: validate range applies to element values.

Update existing YAML templates to use the new types. This is a breaking change to the template schema but the library is v1 and unreleased.

**Constitution alignment**: IX (explicit typing non-negotiable), VIII (templating engines over inference).

### R4. Add duplicate parameter name validation (Priority: Medium)

Add to both ObjectiveTemplate and ConstraintTemplate model_validators:

```python
param_names = [p.name for p in self.parameters]
if len(param_names) != len(set(param_names)):
    dupes = [n for n in param_names if param_names.count(n) > 1]
    raise ValueError(
        f"Duplicate parameter names: {sorted(set(dupes))}. "
        f"Each parameter must have a unique name."
    )
```

**Constitution alignment**: IX (principle of least surprise), VII (reproducibility -- duplicate names cause non-deterministic parameter resolution).

### R5. Add empty mode_compatibility validation (Priority: Medium)

Add to both ObjectiveTemplate and ConstraintTemplate model_validators:

```python
if not self.mode_compatibility:
    raise ValueError(
        "mode_compatibility must contain at least one mode. "
        "A template with no compatible modes is unreachable."
    )
```

**Constitution alignment**: XII (no dead infrastructure).

### R6. Add `description` field to ConstraintTemplate (Priority: Medium)

Add `description: str` to ConstraintTemplate. Update all constraint YAML files to include a description. This provides the guided construction pipeline (spec 014) with plain-language constraint explanations for user-facing prompts.

**Constitution alignment**: XVI (mathematical transparency -- constraints need plain-language explanations).

### R7. Standardize example field structure and add validation (Priority: Medium)

1. Standardize all YAML examples to flat parameter-values format (not nested template re-declarations).
2. Add a model_validator to ObjectiveTemplate:
   - Every parameter without a default must appear as a key in the example dict.
   - Float/integer values in the example must satisfy their parameter's range constraints.

**Constitution alignment**: XIV (spec-implementation parity -- spec says "minimal valid parameterization"), XI (single source of truth -- nested examples duplicate template structure).

### R8. Type the `range` field as a Pydantic model (Priority: Low)

Replace `range: Optional[dict[str, Any]]` with:

```python
class ParameterRange(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
```

Add a model_validator to ParameterDefinition that skips range validation for non-numeric types (string, function). This prevents the current situation where string-type parameters carry numerically-typed ranges that cannot be meaningfully enforced.

**Constitution alignment**: IX (explicit typing non-negotiable).

### R9. Add `_objective_schema_dir()` helper (Priority: Low)

Mirror game_forms.py's `_schema_dir()`:

```python
def _objective_schema_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "schema" / "objective-functions"
```

This is the prerequisite for R1's loader function and follows the established pattern.

**Constitution alignment**: XI (single source of truth for path resolution).

### R10. Export frozenset constants from objectives.py via __init__.py (Priority: Low)

`VALID_MODES`, `VALID_PARAMETER_TYPES`, and `VALID_GAME_FORMS` are defined in objectives.py but not exported from `__init__.py`. game_forms.py exports `VALID_FIELD_TYPES`. The objectives constants should be exported for consistency and for use by external validators (spec 014 pipeline, plugin validators).

**Constitution alignment**: II (stable interfaces -- constants are part of the public API).

---

## Referenced Documentation

| Document | Relevance |
|---|---|
| `conversus/.specify/memory/constitution.md` | Principles IX (functional programming), VIII (templating over inference), XI (single source of truth), XII (no dead infrastructure), XVI (mathematical transparency) |
| `conversus/schemas/game_forms.py` | Reference implementation for frozenset constants, model_validator patterns, `load_mode_mapping()` loader function, `_schema_dir()` path resolution |
| `conversus/schemas/objectives.py` | Target implementation under review |
| `conversus/specs/013-objective-function-templates/spec.md` | FR-002 through FR-016, SC-001 through SC-005 |
| `schema/objective-functions/*.yml` | 21 objective templates + 5 constraint templates (26 total YAML files) |
| `conversus/schemas/__init__.py` | Public API surface -- exports ObjectiveTemplate, ConstraintTemplate, ParameterDefinition but not frozenset constants |
| `conversus/README.md` | Mode definitions, phase structure, architectural invariants |
