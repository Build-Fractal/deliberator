# Cross-Review: schema-engineer reviewing optimization-engineer

**Spec**: 026-optimization-template-library

---

## Agreement

The optimization-engineer's mathematical review is comprehensive. I agree with:

- All 15 formulations are mathematically correct
- Parameters are reasonable and well-typed
- Examples produce feasible instances
- The concern about PSD validation for covariance matrices being a solver-time issue

## Disagreements

None. The optimization-engineer's mathematical assessment is authoritative and well-supported.

## Additions

### 1. Parameter type consistency

The optimization-engineer notes that string-encoded matrices require parsing. I want to highlight a schema-level observation: all matrix/vector parameters use `type: string` with a description explaining the encoding format. This is consistent across templates, which is good.

However, the `type` values used in templates are constrained by the `ObjectiveTemplate` Pydantic model. The valid types should include `string`, `integer`, `float`, and potentially `boolean`. All new templates use only `string`, `integer`, and `float` -- which are standard. No template uses `function` type (which would be excluded from gap_question requirements).

### 2. Template-to-constraint correspondence

The optimization-engineer verified that formulations match their declared constraints. I can confirm from the schema side that all constraint references resolve to existing files:

- `integrality` -> constraints/integrality.yml (exists)
- `cardinality` -> constraints/cardinality.yml (exists)
- `precedence` -> constraints/precedence.yml (exists)
- `flow-conservation` -> constraints/flow-conservation.yml (exists)
- Existing constraints (budget, bounds, non-negativity, etc.) all resolve correctly

This is formally verified by `TestTemplateConstraintReferences.test_constraint_refs_exist`.
