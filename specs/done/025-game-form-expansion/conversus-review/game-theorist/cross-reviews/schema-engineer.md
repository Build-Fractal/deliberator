# Cross-Review: game-theorist reviewing schema-engineer

**Spec**: 025-game-form-expansion
**Reviewer**: game-theorist
**Subject**: schema-engineer Phase 1 review

---

## Verified Claims

### 1. Validator completeness table is accurate

The schema-engineer's model-by-model validator audit is correct. Each model's validators enforce the right structural invariants for schema-level validation. The distinction between "sufficient for schema validation" and "sufficient for solver integration" is well-drawn.

### 2. VALID_FIELD_TYPES duplicate is real

Confirmed: `"map[string, list[string]]"` appears twice in the frozenset literal. The frozenset constructor silently deduplicates, so there is no runtime effect, but the duplication is a copy-paste artifact that should be cleaned.

### 3. YAML schema structure audit is thorough

The five-column table verifying form, description, fields, example across all schemas is correct. The observation that field types are drawn from VALID_FIELD_TYPES and verified by `test_schema_field_types_valid` is accurate.

---

## Disagreements

### 1. BayesianGame prior key validation severity: Info -> Medium

The schema-engineer rates the missing prior key validation as "Info" in finding #1's table but describes it more urgently in the text. I rate this **Medium**. Consider:

```python
BayesianGame(
    type_spaces={"p1": ["H", "L"], "p2": ["H", "L"]},
    prior={"nonsense_a": 0.5, "nonsense_b": 0.5},
)
```

This passes all validators. The prior sums to 1.0. But the keys have no relation to the type spaces. When the Harsanyi transformation attempts to expand this into a normal-form game, it will either crash with a key lookup error or produce a silently malformed game matrix. The validator should check that prior keys are elements of the Cartesian product `T_1 x T_2 x ... x T_N`, encoded as comma-joined sorted type strings.

This is not Info -- it is a genuine validation gap that allows semantically invalid models to pass construction.

### 2. PotentialGame naming: agree it is low priority

The suggestion to rename to `PotentialGameResult` is reasonable but I agree with the schema-engineer's own characterization as "Info." The `form: Literal["potential"]` discriminator makes the intent clear in code. Renaming would cascade to tests and YAML schemas for marginal clarity gain. Defer to cleanup.

### 3. Discriminated union: agree it is future work

The schema-engineer correctly notes this is not required by any FR. The `form` discriminator is already consistently applied, making the union type a pure additive convenience. Agree with "Info" classification.

---

## Additions

### Prior tolerance value

The schema-engineer did not comment on the BayesianGame prior tolerance of `1e-6`. For manually authored YAML priors (e.g., `0.25, 0.25, 0.25, 0.25`), this tolerance is fine -- exact decimals sum exactly. For priors computed via normalization of floating-point values (e.g., Dirichlet samples), accumulated float error can exceed 1e-6 for large type spaces. A tolerance of `1e-4` would be more robust while still catching genuine specification errors (e.g., probabilities that sum to 0.6).

### Model immutability

None of the new models use `model_config = {"frozen": True}`. The existing `PipelineResult` in the engine uses this pattern. For game form models that represent mathematical objects (which should not be mutated after construction), frozen models would be appropriate. This is a design suggestion, not a gap.
