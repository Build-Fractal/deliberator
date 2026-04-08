# Phase 1 Review: schema-engineer

**Spec**: 025-game-form-expansion
**Agent**: schema-engineer
**Focus**: Pydantic model design, validators, YAML schema consistency

---

## Overall Assessment

The Pydantic models are well-structured with appropriate use of `model_validator(mode="after")` for structural invariants, `Literal` types for form discriminators, and `Optional` for non-required fields. YAML schemas follow existing conventions and include required sections (form, description, fields, example). The test suite validates both Python models and YAML schema round-trips.

**Verdict**: PASS with minor recommendations.

---

## Detailed Findings

### 1. Model Design Patterns -- GOOD

All new models follow the established pattern from the original four forms:
- `form: Literal[...]` as a discriminator field
- `@model_validator(mode="after")` for cross-field invariants
- Clear docstrings explaining the game-theoretic semantics

The `_GNEPValidationMixin` is well-designed for code reuse between GNEPGame and ParametricGame without creating a misleading inheritance hierarchy. The note about using `form` discriminator rather than `isinstance` is valuable.

### 2. Validator Completeness -- MOSTLY COMPLETE

| Model | Validators | Assessment |
|-------|-----------|------------|
| PotentialGame | None (no cross-field constraints) | Correct -- it's a diagnostic result, not a game definition |
| CoalitionalGame | Non-empty players, grand coalition key present | Good. Could additionally validate v(empty) = 0 convention |
| CongestionGame | Non-empty resources, agent strategies reference valid resources | Good |
| BayesianGame | Non-empty type spaces, prior sums to 1.0 | Good but prior keys not validated against type space Cartesian product |
| RepeatedGame | discount_factor in (0, 1) | Complete |
| MechanismDesignGame | None (only enum fields) | Acceptable -- Literal types enforce valid values |

### 3. Type Safety -- GOOD

- `dict[str, float]` for characteristic function is appropriate
- `dict[str, list[str]]` for type_spaces and agent_strategies are well-typed
- `Literal["shapley", "core", "nucleolus"]` for solution concept is a clean closed set
- `Literal["linear", "polynomial", "step"]` for cost types is well-chosen

### 4. YAML Schema Consistency

The test `TestNewYAMLSchemas` correctly verifies that all five new YAML schemas have the required top-level keys: `form`, `description`, `fields`, `example`. It also validates that field types are in the `VALID_FIELD_TYPES` frozenset.

**Issue**: The `VALID_FIELD_TYPES` set (lines 24-39) contains a duplicate entry:
```python
"map[string, list[string]]",  # appears twice
```
This does not cause bugs (it's a frozenset) but indicates a copy-paste slip.

### 5. Mode Mapping Updates -- COMPLETE

The test `TestExpandedModeMapping` verifies five new mode-to-form mappings:
- coalition-attribution -> coalitional
- resource-sharing -> congestion
- negotiation -> bayesian
- multi-round -> repeated
- mechanism -> mechanism-design

These are semantically appropriate mappings. The test also verifies that original mappings (cooperative, winner-take-all, prisoners-dilemma, red-blue) still work, which is good regression coverage.

### 6. PotentialGame Model Design -- UNUSUAL

The `PotentialGame` model (lines 298-309) has a different shape from other game forms:
```python
class PotentialGame(BaseModel):
    form: Literal["potential"] = "potential"
    potential_function: str
    is_potential: bool
```

This models the *result* of a potential game diagnostic check, not a game definition. This is consistent with the spec ("a check applied to existing game forms, not a separate form"), but having it as a Pydantic model alongside actual game forms is slightly misleading. It could be renamed `PotentialGameResult` for clarity.

### 7. Test Round-Trip Coverage -- GOOD

Each new model has a test that loads the corresponding YAML schema's `example` field and validates it via `Model.model_validate(data["example"])`. This ensures the YAML examples stay in sync with the Pydantic models.

### 8. Missing Feature: Union Type for Game Forms

There is no `GameForm = Union[NormalFormGame, GNEPGame, ...]` discriminated union type that would allow deserializing an arbitrary game form from YAML based on the `form` field. The original four forms also lack this, but with 9+ forms, a discriminated union would be valuable for generic deserialization.

---

## Summary of Issues

| # | Severity | Item |
|---|----------|------|
| 1 | Low | Duplicate entry in VALID_FIELD_TYPES frozenset |
| 2 | Low | PotentialGame model name could be PotentialGameResult for clarity |
| 3 | Info | No discriminated union type for generic game form deserialization |
| 4 | Info | BayesianGame prior keys not validated against type space Cartesian product |

---

## Recommendation

Accept. Models are well-designed, validators enforce the right invariants, YAML schemas are consistent with the existing library. The noted issues are minor and can be addressed incrementally.
