# Schema Engineer Review: 015 Feature Extraction Pipeline

**Reviewer**: schema-engineer
**Spec**: 015-feature-extraction
**Date**: 2026-03-24

---

## Executive Summary

The Pydantic models in `conversus/schemas/features.py` (AgentFeatures, RoundFeatures, FeatureSet) provide a structurally sound foundation for feature extraction output. All models are frozen (immutable), use appropriate defaults (zero/empty for graceful degradation per FR-003), and the top-level FeatureSet validates mode membership. However, the schema design has significant extensibility and type-safety concerns: AgentFeatures is a single flat model carrying fields for all four modes, creating a god-object that grows linearly with every new mode or feature; there is no per-mode discrimination, meaning a cooperative FeatureSet can carry non-zero red-blue fields without validation error; the agreement_matrix type `dict[str, dict[str, int]]` on RoundFeatures is semantically untyped and could benefit from a dedicated model; and the relationship between `features.py` models and `game_forms.py`/`objectives.py` patterns is inconsistent in several ways that will create friction for spec 016-019 plugins consuming these schemas.

---

## Alignment

### A-1: Frozen model config is correctly applied to all three models

`AgentFeatures`, `RoundFeatures`, and `FeatureSet` all declare `model_config = {"frozen": True}`. This matches the pattern established in `game_forms.py` (NormalFormGame, GNEPGame, etc. use Pydantic's model_validator but not frozen config) and exceeds it -- feature models are stricter about immutability. For a pipeline whose output is consumed by plugins (spec 016), immutability is the correct default: plugins receive frozen snapshots they cannot accidentally mutate.

### A-2: Default values enable graceful degradation for missing phases

Every numeric field on AgentFeatures defaults to `0` or `0.0`, and every list field uses `Field(default_factory=list)`. This means extraction can produce a valid AgentFeatures with only `agent_name` populated, which is exactly the behavior FR-003 requires when Phase 3 or Phase 4 files are missing. The pattern is consistent: no field on any of the three models requires a non-default value except `agent_name` on AgentFeatures and `mode` on FeatureSet.

### A-3: FeatureSet mode validation uses the canonical VALID_MODES set

The `model_validator(mode="after")` on FeatureSet checks `self.mode not in VALID_MODES` and raises a clear ValueError. The `VALID_MODES` frozenset is defined in `features.py` and matches the set in `objectives.py`, ensuring consistency. The validator runs after construction, so any attempt to create `FeatureSet(mode="invalid")` raises immediately.

### A-4: Multi-round structure supports time-series analysis

`FeatureSet.rounds: list[RoundFeatures]` with `RoundFeatures.round_number: int` directly implements FR-010's requirement for time-series analysis. The list structure allows round-over-round comparison, and the round_number field enables sparse round numbering (if a round is skipped due to agent failure).

### A-5: metadata field provides extension point without schema changes

`FeatureSet.metadata: dict[str, Any]` is used by `extraction.py` to store `output_dir`, `agent_count`, and `round_count`. This untyped dict serves as a pragmatic extension point: plugins can inspect metadata without requiring schema changes. The `dict[str, Any]` type is consistent with `PluginResult.data` in the plugin system (spec 016).

---

## Missed Opportunities

### M-1: AgentFeatures is a god-object carrying fields for all four modes

AgentFeatures has 22 fields spanning cooperative (position_vector, concession_rate, etc.), winner-take-all (ranking_position, criterion_scores, etc.), prisoners-dilemma (core_competency_count, territory_claim_vector, etc.), and red-blue (severity_vector, threat_count, etc.) features. In a cooperative extraction, 14 of these fields are unused zeros. This violates the principle of type-safe discrimination: a consumer receiving an AgentFeatures cannot determine from the type alone which fields are semantically meaningful for the current mode.

The `game_forms.py` models solve this correctly with discriminated unions: `NormalFormGame`, `GNEPGame`, `ParametricGame`, and `StackelbergGame` are separate models with a `form: Literal[...]` discriminator. AgentFeatures should follow the same pattern:

```python
class CooperativeAgentFeatures(BaseModel):
    agent_name: str
    recommendation_count: int = 0
    position_vector: list[int] = Field(default_factory=list)
    concession_rate: float = 0.0
    # ... cooperative-only fields

class RedBlueAgentFeatures(BaseModel):
    agent_name: str
    role: str | None = None
    severity_vector: list[int] = Field(default_factory=list)
    # ... red-blue-only fields

AgentFeaturesUnion = Annotated[
    CooperativeAgentFeatures | RedBlueAgentFeatures | ...,
    Field(discriminator="mode")
]
```

This is the highest-impact structural improvement for FR-007 extensibility: adding a new mode's features is a new model class, not 5-10 new fields on the existing god-object.

### M-2: No per-mode field validation on FeatureSet

FeatureSet validates `mode` membership but does not validate that the contained RoundFeatures/AgentFeatures carry mode-appropriate data. A FeatureSet with `mode="cooperative"` and agents carrying `severity_vector=[4,3,2,1]` is valid. This means a bug in the extraction pipeline that writes red-blue features into a cooperative FeatureSet would not be caught by schema validation. A model_validator on FeatureSet could check that mode-specific fields are zero/empty for non-matching modes.

### M-3: VALID_MODES is duplicated between features.py and objectives.py

Both `features.py` and `objectives.py` define `VALID_MODES` as identical frozensets. This creates a maintenance risk: adding a new mode requires updating both files. The canonical set should live in one location (e.g., `conversus/schemas/modes.py` or in `__init__.py`) and be imported by both modules.

### M-4: agreement_matrix type is semantically opaque

`RoundFeatures.agreement_matrix: dict[str, dict[str, int]]` is a nested dict that carries no semantic typing. A consumer must know that the outer keys are reviewer names, inner keys are reviewed names, and values are agreement counts. A dedicated `AgreementMatrix` model or at minimum a type alias would improve readability:

```python
AgreementMatrix = dict[str, dict[str, int]]  # reviewer -> reviewed -> count
```

Or better, a model with a validation invariant that the matrix is square (same keys in outer and inner dicts).

### M-5: RoundFeatures carries mode-specific aggregate fields as a flat structure

Like AgentFeatures, RoundFeatures has mode-specific fields (`score_differential` for WTA, `boundary_clarity` for PD, `landed_attack_count`/`coverage_score` for RB) alongside universal fields (`dispute_count`, `convergence_count`). The same god-object concern applies: a cooperative RoundFeatures carries 6 unused aggregate fields. The discriminated-union pattern from M-1 should extend to RoundFeatures as well.

### M-6: No `__all__` in features.py

The `features.py` module does not define `__all__`, unlike `game_forms.py` which is re-exported through `__init__.py`. While `__init__.py` re-exports the public names, the module itself should declare its public API to guide IDE autocompletion and documentation tools.

### M-7: FeatureSet.metadata lacks schema for expected keys

The `metadata: dict[str, Any]` is populated with `output_dir`, `agent_count`, `round_count` in `extraction.py` but these keys are not documented or typed in `features.py`. Consumers must read the extraction code to know what metadata is available. A `FeatureSetMetadata` model with typed fields and `model_config = {"extra": "allow"}` would provide a typed baseline while preserving extensibility.

### M-8: No JSON Schema export for features.json consumers

FR-009 requires plugins to "import and validate against" the FeatureSet model. External consumers (non-Python tools) cannot import Pydantic models. Generating a `features.schema.json` from `FeatureSet.model_json_schema()` at build time would extend the validation contract to any language. This parallels how the game form YAML schemas in `schema/game-forms/` serve as language-agnostic contracts.

---

## Off-Base Assumptions

### O-1: Territory claim vector is declared but never populated

AgentFeatures declares `territory_claim_vector: list[int]` for prisoners-dilemma mode, but `_extract_pd_agent_features()` in `extraction.py` never populates it. The PD extraction constructs an AgentFeatures without passing `territory_claim_vector`, so it defaults to an empty list. The spec's Section 2 defines this feature ("Binary per topic area: does this agent claim ownership?"), but the implementation does not extract it. Either the field should be removed from the model until extraction is implemented, or extraction should be implemented.

### O-2: `confirmed_count` on AgentFeatures is declared but never populated

The `confirmed_count: int = 0` field is listed in the red-blue section of AgentFeatures. The spec's Section 2 defines "Confirmed count: Findings confirmed as valid after adversarial challenge" as a red-blue feature. But `_extract_rb_agent_features()` never sets this field. Same resolution as O-1: implement or remove.

---

## Actionable Recommendations

1. **Refactor AgentFeatures into per-mode discriminated union** (Priority: P1)
   - Create `CooperativeAgentFeatures`, `WTAAgentFeatures`, `PDAgentFeatures`, `RedBlueAgentFeatures` with a `mode` discriminator. This is the single highest-impact change for FR-007 extensibility. New features for a mode are added to its specific model; new modes are new models.

2. **Add per-mode field validation to FeatureSet** (Priority: P2)
   - Add a model_validator on FeatureSet that verifies agents carry mode-appropriate feature types when using the discriminated union from R-1.

3. **Deduplicate VALID_MODES into a single canonical location** (Priority: P2)
   - Move `VALID_MODES` to `conversus/schemas/modes.py` or the package `__init__.py` and import from both `features.py` and `objectives.py`.

4. **Add AgreementMatrix type alias or model** (Priority: P3)
   - Create a semantic type alias or validated model for the nested dict structure, with a validation invariant that inner and outer key sets are identical.

5. **Remove or implement `territory_claim_vector` and `confirmed_count`** (Priority: P2)
   - These declared-but-unpopulated fields create a false API surface. Either implement the extraction logic or remove the fields and document them as future additions.

6. **Create typed FeatureSetMetadata model** (Priority: P3)
   - Replace `metadata: dict[str, Any]` with a typed model containing `output_dir: str`, `agent_count: int`, `round_count: int`, and `model_config = {"extra": "allow"}` for forward-compatible extensibility.

7. **Add `__all__` to features.py** (Priority: P3)
   - Define the public API surface explicitly.

8. **Generate features.schema.json at build time** (Priority: P3)
   - Add a build step that calls `FeatureSet.model_json_schema()` and writes the result to `schema/features/features.schema.json` for non-Python consumers.
