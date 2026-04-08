# Cross-Review: spec-compliance reviewing schema-engineer

**Spec**: 025-game-form-expansion
**Reviewer**: spec-compliance
**Subject**: schema-engineer Phase 1 review

---

## Verified Claims

### 1. Model architecture patterns table is accurate

The four-pattern assessment (Literal discriminator, model_validator, docstrings, Optional fields) is correct. All six new models consistently apply these patterns. The observation that PotentialGame and MechanismDesignGame correctly omit model_validator (no cross-field constraints) shows good judgment -- validators should exist where needed, not as boilerplate.

### 2. Validator completeness audit is thorough

The six-row table mapping each model to its validators and gap analysis is the most useful artifact in the schema-engineer's review. I verify each row:

- PotentialGame: correct (diagnostic result, no cross-field constraints)
- CoalitionalGame: correct (non-empty players, grand coalition key)
- CongestionGame: correct (non-empty resources, strategy subset)
- BayesianGame: correctly flags prior key validation gap
- RepeatedGame: correct (open interval constraint)
- MechanismDesignGame: correct (Literal enum sufficiency)

### 3. YAML-Pydantic consistency guarantee is well-identified

The observation that `test_yaml_example_validates` provides a schema-model consistency guarantee is accurate and well-framed. This pattern means YAML schema drift from Pydantic models is caught automatically.

### 4. Discriminated union suggestion is well-motivated

The code snippet showing `Annotated[Union[...], Field(discriminator="form")]` is practical and implementable. The `form` field is already present on every model, making this zero-effort to add.

---

## Disagreements

### 1. Finding #1 severity: Medium is correct, but needs compliance context

The schema-engineer rates the BayesianGame prior key gap as MEDIUM. I agree with the severity but want to add compliance framing: this gap means the BayesianGame model does not fully satisfy FR-002 ("MUST have a Pydantic model with validators"). The model has a validator (prior sums to 1.0), but the validator is incomplete -- it validates a necessary condition (probabilities sum to 1) without validating a sufficient condition (keys correspond to valid type profiles).

Strictly read, FR-002 says "with validators" (plural) but does not specify which invariants must be validated. The prior-sum validator exists, so the literal requirement is met. But the spirit of FR-002 is that the model should catch invalid inputs at construction time, and this model does not catch semantically invalid prior keys.

I maintain the FR-002 PASS verdict because the validator exists, but annotate it as having a known gap.

### 2. Finding #4 (PotentialGame naming) is not a compliance concern

The schema-engineer lists this as "Info" which is appropriate. I want to explicitly confirm: no FR or SC requires any specific naming convention for Pydantic models. The `form: Literal["potential"]` discriminator is the identifier, not the class name. Renaming to PotentialGameResult would be a code quality improvement but has zero compliance implications.

### 3. Finding #5 (coalitional YAML example includes unrequired empty coalition key) -- harmless

The schema-engineer notes that the coalitional.yml example includes `"": 0` (empty coalition) but the model does not require it. This is actually good practice -- the example demonstrates the complete characteristic function specification that a user would typically provide, even though the model only requires the grand coalition key. The solver code uses `dict.get(key, 0.0)` to handle missing keys, so the empty coalition key is optional.

This is not an inconsistency -- it is a helpful example that exceeds the minimum requirements.

---

## Additions

### Mode mapping referential integrity

The schema-engineer correctly notes that all five new mappings are "semantically appropriate" but does not assess referential integrity: whether the `form` values in mode-mapping.yml reference YAML schemas that actually exist in `schema/game-forms/`. A check would verify:

```
coalition-attribution -> coalitional -> coalitional.yml exists
resource-sharing -> congestion -> congestion.yml exists
negotiation -> bayesian -> bayesian.yml exists
multi-round -> repeated -> repeated.yml exists
mechanism -> mechanism-design -> mechanism-design.yml exists
```

All five exist. This could be a test case: load mode-mapping.yml, for each entry, verify that `{form}.yml` exists in the game-forms directory.

### Frozen model consideration

The schema-engineer does not discuss model immutability. Game form models represent mathematical specifications that should not be mutated after construction. Adding `model_config = {"frozen": True}` to each model would enforce this invariant at the Pydantic level, consistent with the `PipelineResult` model in the engine.
