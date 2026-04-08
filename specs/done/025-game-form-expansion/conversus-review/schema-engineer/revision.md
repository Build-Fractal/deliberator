# Phase 3 Revision: schema-engineer

**Spec**: 025-game-form-expansion
**Agent**: schema-engineer

---

## Position Changes After Cross-Review

### MAINTAINED: Finding #1 (BayesianGame prior key validation) -- MEDIUM

All agents converge on MEDIUM severity. The game-theorist provides the strongest example: arbitrary keys like `"INVALID_KEY"` pass validation when prior sums to 1.0. The spec-compliance agent notes this weakens FR-002's spirit.

**Implementation recommendation refined**: The validator should:
1. Extract the ordered list of player names from type_spaces keys
2. Compute the Cartesian product of their type lists
3. For each product tuple, create the comma-joined string (matching the convention used in prior keys)
4. Assert that every key in `self.prior` is in this valid set

```python
from itertools import product

@model_validator(mode="after")
def validate_structure(self) -> BayesianGame:
    if not self.type_spaces:
        raise ValueError("Bayesian game must have at least one player type space.")
    total = sum(self.prior.values())
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Prior probabilities must sum to 1.0, got {total:.6f}.")
    # Validate prior keys against type space Cartesian product
    players = sorted(self.type_spaces.keys())
    type_lists = [self.type_spaces[p] for p in players]
    valid_keys = {",".join(combo) for combo in product(*type_lists)}
    invalid_keys = set(self.prior.keys()) - valid_keys
    if invalid_keys:
        raise ValueError(
            f"Prior keys {sorted(invalid_keys)} are not valid type profiles. "
            f"Valid keys are combinations from type_spaces: {sorted(valid_keys)}"
        )
    return self
```

### WITHDRAWN: Finding #4 (PotentialGame naming)

Both the game-theorist and spec-compliance confirm this is purely stylistic with zero compliance impact. The `form: Literal["potential"]` discriminator is sufficient for identification. Withdrawn.

### MAINTAINED: Finding #2 (VALID_FIELD_TYPES duplicate) -- LOW

No one contested this. Cosmetic fix, should be cleaned up.

### MAINTAINED: Finding #3 (discriminated union type) -- INFO

The spec-compliance agent confirms no FR requires this. I maintain it as a design recommendation for future work. The implementation path is straightforward with Pydantic's `Field(discriminator="form")`.

### NEW: Frozen model config (from spec-compliance) -- INFO

The spec-compliance agent suggests adding `model_config = {"frozen": True}` to game form models. This is consistent with `PipelineResult` in the engine and appropriate for mathematical specification objects that should not be mutated after construction. Accepted as an INFO-level design suggestion.

### NEW: Mode mapping referential integrity test (from spec-compliance) -- LOW

The spec-compliance agent notes that no test verifies that `form` values in mode-mapping.yml reference existing YAML schema files. A test like:

```python
def test_mapping_forms_have_yaml_schemas():
    mapping = load_mode_mapping(SCHEMA_DIR / "mode-mapping.yml")
    for mode, entry in mapping.mappings.items():
        schema_path = SCHEMA_DIR / f"{entry.form}.yml"
        assert schema_path.exists(), f"Mode '{mode}' maps to form '{entry.form}' but {schema_path} does not exist"
```

would catch dangling references. Accepted as LOW.

### NEW: compute_potential return value semantics (self-identified) -- INFO

My cross-review of the game-theorist noted that `compute_potential()` returns a scalar (max potential value) rather than the full potential matrix or the equilibrium strategy profile. For diagnostic purposes ("This game has a potential function; the Nash equilibrium is at strategy profile (i, j)"), the argmax would be more informative. Noted for future enhancement.

---

## Revised Finding Table

| # | Severity | Finding | Status |
|---|----------|---------|--------|
| 1 | MEDIUM | BayesianGame prior keys not validated against type space Cartesian product | Surviving -- unanimous |
| 2 | LOW | Duplicate entry in VALID_FIELD_TYPES | Surviving -- uncontested |
| 3 | LOW | Missing mode mapping referential integrity test | New -- from spec-compliance |
| 4 | INFO | No discriminated union type for generic deserialization | Surviving -- deferred |
| 5 | INFO | Frozen model config for immutable game specifications | New -- from spec-compliance |
| 6 | INFO | compute_potential() returns scalar, not full matrix/argmax | New -- self-identified |
