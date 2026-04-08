# Cross-Review: game-theorist reviewing schema-engineer

**Spec**: 025-game-form-expansion

---

## Agreement

I agree with the schema-engineer's assessment that the models are well-structured and validators enforce appropriate invariants. The observation about the duplicate `VALID_FIELD_TYPES` entry is correct and I missed it. The suggestion for a discriminated union type is valuable -- without it, generic deserialization of game forms from YAML requires manual dispatch.

## Disagreements

### 1. BayesianGame prior key validation (Medium, not Info)

The schema-engineer lists this as "Info" severity. I believe it should be **Medium**. Invalid prior keys silently produce a valid model that would fail at solver time. For example:

```python
BayesianGame(
    type_spaces={"p1": ["H", "L"], "p2": ["H", "L"]},
    prior={"garbage_key": 0.5, "also_garbage": 0.5},
)
```

This passes validation (prior sums to 1.0) but is semantically invalid. The model should validate that prior keys correspond to the Cartesian product of type spaces, or at minimum that all prior keys reference valid type combinations.

### 2. PotentialGame naming (Agree but Low priority)

The suggestion to rename `PotentialGame` to `PotentialGameResult` is reasonable. However, the model's `form: Literal["potential"]` discriminator makes its role clear in code, and renaming would require updating YAML schemas and tests. I would defer this to a cleanup pass.

## Additions

The schema-engineer did not comment on the tolerance in the Bayesian prior sum check (`abs(total - 1.0) > 1e-6`). This tolerance is tight enough for manually specified priors but may be too tight for computed priors (e.g., after normalization of floating-point values). A tolerance of `1e-4` would be more forgiving while still catching genuine errors. This is a minor point.
