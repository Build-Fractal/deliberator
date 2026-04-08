# Phase 1 Review: schema-engineer

**Spec**: 025-game-form-expansion
**Agent**: schema-engineer
**Focus**: Pydantic models well-designed? Validators complete? YAML schemas consistent?

---

## Overall Assessment

The Pydantic models are well-architected: correct use of `model_validator(mode="after")`, `Literal` discriminators, appropriate type annotations, and clean separation of validation from solver logic. YAML schemas follow the established convention (form, description, fields, example). The mode-mapping update is complete and semantically appropriate. Test coverage includes both Pydantic validation and YAML round-trip verification.

**Verdict**: PASS with minor schema refinement recommendations.

---

## Detailed Findings

### 1. Model Architecture Patterns -- EXCELLENT

All six new models follow the established pattern:

| Pattern | Applied consistently? | Notes |
|---------|----------------------|-------|
| `form: Literal[...]` discriminator | Yes | Enables future discriminated union dispatch |
| `@model_validator(mode="after")` | Yes (where needed) | PotentialGame and MechanismDesignGame omit it correctly -- no cross-field invariants |
| Docstrings with game-theoretic context | Yes | Each model explains the mathematical concept it represents |
| `Optional[...]` for non-required fields | Yes | CongestionGame cost_functions could benefit from this (currently absent, not optional) |

The `_GNEPValidationMixin` (lines 59-104) is a well-designed shared validation layer. The explicit note discouraging `isinstance` checks in favor of the `form` discriminator prevents a common inheritance-over-composition pitfall.

### 2. Validator Completeness Audit

| Model | Validators | Gap analysis |
|-------|-----------|-------------|
| PotentialGame | None | Correct -- it is a diagnostic result container, not a game definition. No cross-field constraints needed. |
| CoalitionalGame | `players` non-empty, grand coalition key present | Complete for schema validation. Could optionally enforce monotonicity (v(S) <= v(T) when S subset T) but this is not universally required. |
| CongestionGame | `resources` non-empty, agent strategy resources subset of declared resources | Complete. The subset check is the key structural invariant. |
| BayesianGame | `type_spaces` non-empty, prior sums to 1.0 (tolerance 1e-6) | **GAP**: Prior keys not validated against Cartesian product of type_spaces. Arbitrary string keys accepted. |
| RepeatedGame | `discount_factor` in open interval (0, 1) | Complete. Boundary exclusion is mathematically correct. |
| MechanismDesignGame | None (Literal enum fields only) | Acceptable for current scope. Enum constraints via Literal are sufficient. |

### 3. VALID_FIELD_TYPES Frozenset -- DUPLICATE ENTRY

Lines 24-39 of `game_forms.py`:

```python
VALID_FIELD_TYPES: frozenset[str] = frozenset({
    ...
    "map[string, list[string]]",
    ...
    "map[string, list[string]]",  # duplicate
})
```

The frozenset silently deduplicates, so this causes no runtime issue. However, it indicates a copy-paste error and should be cleaned up to avoid confusion during future edits.

### 4. YAML Schema Structure Audit

All five new schemas (coalitional.yml, congestion.yml, bayesian.yml, repeated.yml, mechanism-design.yml) follow the required structure:

| Required key | Present in all? | Notes |
|-------------|----------------|-------|
| `form` | Yes | Matches the Pydantic model's Literal discriminator |
| `description` | Yes | YAML block scalar (`>`) used consistently |
| `fields` | Yes | Each field has name, type, required, description |
| `example` | Yes | Validated by `test_yaml_example_validates` round-trip tests |

Field types in all schemas are drawn from `VALID_FIELD_TYPES`. The parametric test `test_schema_field_types_valid` verifies this programmatically.

### 5. YAML-Pydantic Consistency

The `example` block in each YAML schema is validated against the corresponding Pydantic model in tests. This is a strong consistency guarantee -- if the YAML example drifts from the Pydantic model (e.g., field renamed, type changed), the test catches it.

**Observation**: The coalitional.yml example includes the empty coalition key `""` mapping to 0, but the CoalitionalGame model does not require this key. The model only requires the grand coalition key. This asymmetry is harmless but could confuse YAML authors who omit the empty coalition.

### 6. Mode Mapping -- COMPLETE AND CONSISTENT

Five new mode-to-form mappings:

| Mode | Form | Semantic justification |
|------|------|----------------------|
| coalition-attribution | coalitional | Fair value attribution via Shapley values |
| resource-sharing | congestion | Shared resources with contention costs |
| negotiation | bayesian | Private information, Harsanyi transformation |
| multi-round | repeated | Folk Theorem cooperation dynamics |
| mechanism | mechanism-design | Incentive-compatible rule design |

All original mappings preserved. The `ModeMapping.lookup()` method provides clean access with a KeyError on unknown modes. The test `test_total_mappings_count` verifies >= 9 total mappings (4 original + 5 new = 9).

### 7. PotentialGame Model Design -- DIAGNOSTIC RESULT, NOT GAME FORM

The PotentialGame model (lines 298-309) stores the output of a diagnostic check:

```python
class PotentialGame(BaseModel):
    form: Literal["potential"] = "potential"
    potential_function: str
    is_potential: bool
```

This is not a game definition -- it records whether a game was identified as having a potential function. It does not appear in mode-mapping.yml and has no YAML schema with the standard form/description/fields/example structure. The naming `PotentialGame` could be read as "a game that is potential" (confusing) or "potential game diagnostic result" (intended). A rename to `PotentialGameResult` would improve clarity, but the `form: Literal["potential"]` discriminator disambiguates sufficiently.

### 8. Missing: Discriminated Union Type

With 9+ game forms, a discriminated union would enable generic deserialization:

```python
from typing import Annotated, Union
from pydantic import Field

GameForm = Annotated[
    Union[NormalFormGame, GNEPGame, ParametricGame, StackelbergGame,
          CoalitionalGame, CongestionGame, BayesianGame, RepeatedGame,
          MechanismDesignGame],
    Field(discriminator="form")
]
```

This is not required by any FR but would be valuable for downstream consumers that need to load arbitrary game form YAML files. The `form` discriminator is already in place on every model, making this a straightforward addition.

---

## Summary of Findings

| # | Severity | Finding |
|---|----------|---------|
| 1 | MEDIUM | BayesianGame prior keys not validated against type space Cartesian product |
| 2 | LOW | Duplicate entry in VALID_FIELD_TYPES frozenset (cosmetic) |
| 3 | INFO | No discriminated union type for generic game form deserialization |
| 4 | INFO | PotentialGame naming could be clearer (PotentialGameResult) |
| 5 | INFO | Coalitional YAML example includes empty coalition key not required by model |

---

## Recommendation

ACCEPT. Models are well-designed with correct validators, YAML schemas are consistent, and mode mapping is complete. Finding #1 (BayesianGame prior key validation) should be addressed to prevent silent acceptance of invalid configurations.
