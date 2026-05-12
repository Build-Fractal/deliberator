# Schema Engineer Review: 013 Objective Function Templates

**Reviewer**: schema-engineer
**Spec**: 013-objective-function-templates
**Date**: 2026-03-23

---

## Executive Summary

The ObjectiveTemplate Pydantic model and its companion models (ParameterDefinition, ConstraintTemplate) provide a sound structural foundation for validating objective function template YAML files. The model correctly enforces the core FR requirements: required fields, type-literal validation, mode_compatibility membership, game_form membership, and the function-type derived_from invariant. However, the implementation has several meaningful gaps: no uniqueness enforcement on parameter names within a template, no validation that constraint references actually exist as YAML files, inconsistent example structures across templates, and an import path that diverges from the FR-011 specification. The YAML templates themselves are well-crafted and mathematically coherent, but they exhibit structural inconsistencies (some examples are flat key-value maps, others nest the full template structure) that would cause validation failures against the current Pydantic model.

---

## Alignment

### A-1: FR-003 parameter type system is well-scoped

The four-type system (`float`, `integer`, `string`, `function`) covers the actual parameter diversity observed across all 21 YAML templates. Every parameter in every template maps cleanly to one of these four types. The `Literal` constraint on ParameterDefinition.type catches typos at parse time rather than at solver time, which is the correct layer for a schema-only package.

### A-2: FR-005 function-type derived_from enforcement works

The model_validator correctly rejects function-type parameters missing `derived_from`. This is the most important cross-field invariant for the guided construction pipeline (spec 014), because function-type parameters are the bridge between deliberation artifacts and mathematical formalization. Every function-type parameter across the 21 templates includes a well-written `derived_from` string.

### A-3: FR-008 mode_compatibility and game_form validation is correct

The closed sets `VALID_MODES` and `VALID_GAME_FORMS` match the four modes from the README (cooperative, winner-take-all, prisoners-dilemma, red-blue) and the four game forms from spec 012 (normal-form, gnep, parametric, stackelberg). The model_validator rejects unknown entries. SC-002 would pass as specified.

### A-4: FR-010 range-default consistency is properly checked

When `range.min`, `range.max`, and `default` are all present, the validator confirms `min <= default <= max`. This is correctly implemented as an opt-in check -- it only fires when all three values exist, allowing parameters with open-ended ranges (e.g., `min: 0` without `max`) or no defaults.

### A-5: ConstraintTemplate model matches FR-007

The ConstraintTemplate model requires `name`, `form`, `parameters`, and `mode_compatibility`, exactly matching FR-007. Mode validation is shared logic with ObjectiveTemplate. All six constraint YAML files parse correctly against this model.

### A-6: Template library meets FR-012 through FR-015 cardinality requirements

The library ships 21 objective function templates (FR-012 requires >= 20): 4 cooperative, 3 winner-take-all, 3 prisoners-dilemma, 3 red-blue mode-specific templates plus 8 cross-mode templates. This satisfies FR-013 (>= 3 per mode) and FR-014 (>= 5 cross-mode). Six constraint templates satisfy FR-015 (>= 4). The cooperative mode has a fourth template (cooperative-fairness) beyond the three listed in Section 2 of the spec, which is fine -- the spec says "at least."

---

## Missed Opportunities

### M-1: No uniqueness enforcement on parameter names within a template

ParameterDefinition validates individual parameters, but ObjectiveTemplate does not check that `parameters` contains unique names. A YAML template with two parameters both named `lambda` would pass validation silently. This is a real risk: the cooperative-integration template uses `lambda` (a Python reserved word) as a parameter name, and copy-paste errors could duplicate it. The model_validator on ObjectiveTemplate should add:

```python
names = [p.name for p in self.parameters]
if len(names) != len(set(names)):
    dupes = [n for n in names if names.count(n) > 1]
    raise ValueError(f"Duplicate parameter names: {set(dupes)}")
```

### M-2: Constraint references are never validated against actual constraint files

ObjectiveTemplate.constraints is `list[str]` with no validation that the referenced constraint names correspond to actual constraint YAML files. A template referencing `constraints: ["nonexistent-constraint"]` would pass validation. While the spec does not explicitly require this (FR-008 says "compatible constraint templates (references)"), the word "references" implies referential integrity. At minimum, a `VALID_CONSTRAINTS` frozenset mirroring `VALID_MODES` and `VALID_GAME_FORMS` would catch typos.

### M-3: Example field structure is inconsistent across templates

Some templates use a flat key-value example (cooperative-integration: `{accepted_recs: 12, disputes: 3, lambda: 1.0}`), while others nest the full template structure inside example (weighted-sum: `{name: "weighted-sum", form: "...", game_form: "parametric", parameters: {...}}`). The Pydantic model types `example` as `dict[str, Any]`, so both pass validation, but this inconsistency means downstream consumers cannot reliably extract parameterized examples. The spec says "minimal valid parameterization" (FR-002), which the flat format satisfies more faithfully.

### M-4: No validation that example parameter keys match defined parameter names

Even if the example format were standardized, the model does not check that the keys in the `example` dict correspond to names in the `parameters` list. An example with `{typo_lambda: 1.0}` would pass validation. This cross-field invariant would catch data entry errors at the template authoring stage.

### M-5: The `range` field on ParameterDefinition is an unstructured dict

`range: Optional[dict[str, Any]]` accepts arbitrary keys. While the validator checks `min` and `max` when present, it does not reject unexpected keys (e.g., `range: {min: 0, maxx: 10}` silently ignores the typo). A dedicated RangeSpec model with `min: Optional[float]`, `max: Optional[float]`, and `model_config = ConfigDict(extra="forbid")` would catch this class of errors.

### M-6: No description field on ConstraintTemplate

FR-007 does not explicitly require `description`, but every objective template has one, and all six constraint YAML files include header comments that serve as implicit descriptions. Adding an optional `description` field to ConstraintTemplate would preserve self-documentation parity with ObjectiveTemplate and make constraint files more useful for the guided construction pipeline's LLM prompts.

### M-7: String-typed parameters masking structured data

Several parameters use `type: string` to encode structured data: `weights` ("0.5, 0.3, 0.2"), `Q` ("[[2, 0], [0, 2]]"), `tolerance` ("0, 0.05, 0.1"). The string type is technically correct per the four-type system, but it loses type safety for values that have clear numeric structure. This is a design limitation of the four-type system rather than a bug, but it means that downstream consumers must parse these strings manually with no schema guidance.

### M-8: Boolean values encoded as strings

The `normalize` parameter in weighted-sum and minimax uses `type: string` with values `"true"` / `"false"`. The type system lacks a `boolean` type, so this is the only option, but it creates a parsing burden for downstream consumers who must string-compare instead of using native boolean logic.

### M-9: No loader utility for objective templates paralleling load_mode_mapping

`game_forms.py` provides `load_mode_mapping()` for loading and validating mode-mapping.yml. No equivalent `load_objective_template()` or `load_constraint_template()` utility exists in `objectives.py`. Consumers must write their own YAML-load-then-validate boilerplate. The pattern is already established in the sibling module.

---

## Off-Base Assumptions

### O-1: FR-011 import path does not match implementation

FR-011 requires: `from conversus_schemas.objectives import ObjectiveTemplate, ConstraintTemplate, ParameterDefinition`. The actual import path is `from conversus.schemas.objectives import ...` (the package is named `conversus`, not `conversus_schemas`, and the module lives under `conversus/schemas/` not at the top level). This was already flagged in the 012 review for game_forms.py but has not been resolved. The `__init__.py` re-exports are correct within the `conversus.schemas` namespace, but FR-011 as written will produce an ImportError.

### O-2: ObjectiveTemplate.example typed too loosely for the spec's intent

FR-002 says the example should be a "minimal valid parameterization." The current `dict[str, Any]` type admits anything -- including empty dicts (the default_factory), nested template structures, or completely unrelated keys. The spec implies the example should be a mapping from parameter names to concrete values, which is a much tighter contract than what the model enforces.

### O-3: ConstraintTemplate lacks `description` and `example` fields present in the spec's sibling

The constraint template schema (FR-006, FR-007) is deliberately more minimal than the objective template schema, but the YAML constraint files include descriptive header comments that are invisible to the model. If constraints are consumed by the guided construction pipeline (spec 014) the same way objectives are, the absence of machine-readable description and example fields will create an asymmetry that downstream code must special-case around.

---

## Actionable Recommendations

### R-1: Add duplicate parameter name detection to ObjectiveTemplate.validate_template

Add to the existing model_validator:
```python
param_names = [p.name for p in self.parameters]
if len(param_names) != len(set(param_names)):
    duplicates = {n for n in param_names if param_names.count(n) > 1}
    raise ValueError(f"Duplicate parameter names: {sorted(duplicates)}")
```
**Priority**: High. Silent duplicates corrupt downstream parameter resolution.

### R-2: Add a VALID_CONSTRAINTS frozenset and validate constraint references

```python
VALID_CONSTRAINTS: frozenset[str] = frozenset({
    "budget", "capacity", "mutual-exclusivity",
    "minimum-coverage", "non-negativity", "bounds",
})
```
Validate in ObjectiveTemplate.validate_template:
```python
invalid_constraints = set(self.constraints) - VALID_CONSTRAINTS
if invalid_constraints:
    raise ValueError(f"Unknown constraint references: {sorted(invalid_constraints)}")
```
**Priority**: Medium. Prevents typos in constraint references.

### R-3: Standardize example format across all YAML templates

Adopt the flat format consistently: example should contain only parameter-name-to-value mappings (e.g., `{lambda: 1.0, accepted_recs: 12}`). Remove the nested `name`, `form`, `game_form`, `parameters`, and `computed_objective` keys that appear in weighted-sum, minimax, lexicographic, budget-constrained, time-constrained, general-linear, and general-quadratic templates. The `computed_objective` annotation is useful but belongs in a separate field (e.g., `example_note`) rather than mixed into the parameterization dict.

**Priority**: High. Seven of 21 templates use a non-flat example structure that would confuse parameter extraction.

### R-4: Add cross-validation between example keys and parameter names

In ObjectiveTemplate.validate_template, after standardizing the example format:
```python
if self.example:
    param_names = {p.name for p in self.parameters}
    unknown_keys = set(self.example.keys()) - param_names
    if unknown_keys:
        raise ValueError(f"Example contains keys not in parameters: {sorted(unknown_keys)}")
```
**Priority**: Medium. Catches example/parameter mismatches.

### R-5: Create a RangeSpec model to replace dict[str, Any]

```python
class RangeSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    min: Optional[float] = None
    max: Optional[float] = None
```
Update ParameterDefinition to use `range: Optional[RangeSpec] = None`. This catches typos in range keys and makes the range structure self-documenting.

**Priority**: Medium. Prevents silent typo acceptance in range definitions.

### R-6: Add boolean to the parameter type system

Extend `VALID_PARAMETER_TYPES` to include `"boolean"` and update the `type` Literal accordingly. Convert `normalize` parameters in weighted-sum and minimax from `type: string` to `type: boolean`. This aligns the type system with the actual data semantics and removes the string-parsing burden.

**Priority**: Low. Only affects two parameters across 21 templates, but improves type fidelity.

### R-7: Add load_objective_template() and load_constraint_template() utilities

Mirror the `load_mode_mapping()` pattern from game_forms.py:
```python
def load_objective_template(path: Path) -> ObjectiveTemplate:
    with open(path) as f:
        data = yaml.safe_load(f)
    return ObjectiveTemplate.model_validate(data)

def load_all_objective_templates(directory: Path | None = None) -> list[ObjectiveTemplate]:
    if directory is None:
        directory = _schema_dir()
    return [load_objective_template(p) for p in directory.glob("*.yml")]
```
**Priority**: Medium. Eliminates boilerplate for downstream consumers and establishes a canonical loading path.

### R-8: Resolve the FR-011 import path discrepancy

Either (a) rename the package directory from `conversus/` to `conversus_schemas/` and update `pyproject.toml`, or (b) amend FR-011 in the spec to match the actual import path `from conversus.schemas.objectives import ...`. Option (b) is lower-risk given that the 012 implementation already established the `conversus.schemas` namespace.

**Priority**: High. FR-011 as written produces an ImportError against the current code.

### R-9: Add empty-parameters guard to ObjectiveTemplate

The model allows `parameters: []` (an empty list). While no current template has zero parameters, a carelessly authored template with no parameters would pass validation and produce a vacuous objective function. Add a check:
```python
if not self.parameters:
    raise ValueError("Objective template must define at least one parameter.")
```
**Priority**: Low. Defensive check against degenerate templates.

### R-10: Add model_config extra="forbid" to all models

Currently the models silently accept extra YAML keys (e.g., `computed_objective` in the nested example blocks). Adding `model_config = ConfigDict(extra="forbid")` to ObjectiveTemplate, ConstraintTemplate, and ParameterDefinition would catch extraneous fields that indicate authoring errors or format drift.

**Priority**: Medium. Prevents silent acceptance of unexpected fields.

---

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/013-objective-function-templates/spec.md` -- feature spec defining all FR and SC requirements
- `<HOME>/code/payer-index-mono/conversus/conversus/schemas/objectives.py` -- Pydantic models (ObjectiveTemplate, ConstraintTemplate, ParameterDefinition)
- `<HOME>/code/payer-index-mono/conversus/conversus/schemas/game_forms.py` -- sibling Pydantic models for game forms (load_mode_mapping pattern)
- `<HOME>/code/payer-index-mono/conversus/conversus/schemas/__init__.py` -- package re-exports
- `<HOME>/code/payer-index-mono/conversus/schema/objective-functions/cooperative-integration.yml` -- cooperative mode template
- `<HOME>/code/payer-index-mono/conversus/schema/objective-functions/competitive-selection.yml` -- winner-take-all mode template
- `<HOME>/code/payer-index-mono/conversus/schema/objective-functions/territory-claiming.yml` -- prisoners-dilemma mode template
- `<HOME>/code/payer-index-mono/conversus/schema/objective-functions/risk-adversarial.yml` -- red-blue mode template
- `<HOME>/code/payer-index-mono/conversus/schema/objective-functions/weighted-sum.yml` -- cross-mode template (example format inconsistency)
- `<HOME>/code/payer-index-mono/conversus/schema/objective-functions/constraints/budget.yml` -- constraint template
- `<HOME>/code/payer-index-mono/conversus/README.md` -- conversus framework documentation (mode definitions, directory structure)
