# Cross-Review: game-engine-advocate reviewing functional-typing

## Dangerous Contradictions

None identified. The functional-typing recommendations strengthen the type system without blocking any game engine integration paths. All StrEnum and Pydantic model improvements are additive and extensible via the factory pattern.

## Tensions

### T1: Phase Enum Strictness vs. Plugin-Contributed Phases

**functional-typing** recommends (Rec 1, P1) replacing all string literal phase comparisons in `validate.py` with `Phase` enum members and typing the `phase` parameter as `Phase` instead of `str`.

**game-engine-advocate** notes that the Phase enum is a closed behavioral enum extensible via factory pattern. If a plugin contributes a new phase (e.g., `Phase.GAME_ANALYSIS`), the `validate.py` functions typed with `Phase` would accept the core `Phase` enum but not the factory-produced extended enum unless the type signature uses `Union[Phase, ExtendedPhase]` or a protocol.

The practical tension: strict `Phase` typing in `validate.py` is correct for the current system but creates a migration step when plugins extend phases. The resolution is straightforward -- the factory-produced enum is a StrEnum subclass, so a `StrEnum` type hint (or a protocol) would accept both. But functional-typing's recommendation as stated would use the concrete `Phase` type, which is slightly too narrow for the extensibility path.

This tension is low-severity because: (1) the game engine is archived, (2) Python's duck typing means the code would work at runtime even with the narrower type hint, and (3) the factory pattern documentation already signals the extension path.

### T2: match/case Exhaustiveness vs. Plugin Phase Injection

**functional-typing** recommends (Rec 6, P2) using `match`/`case` with `Phase` StrEnum for exhaustive matching in `check_required_headings` and `check_structural_markers`.

**game-engine-advocate** observes that exhaustive matching is a double-edged sword for extensibility. If a plugin adds a new phase via factory, the `match`/`case` in core validation will hit the `case _:` default branch. This is correct behavior (unknown phases get default validation), but it means the exhaustiveness guarantee only applies to core phases. The `match`/`case` approach is still better than `if`/`elif` because it makes the default case explicit, but it does not provide the same guarantee for plugin-contributed phases.

This is not a contradiction -- both approaches agree that explicit dispatch is better than string comparisons. The tension is about whether the exhaustiveness framing overpromises for the plugin case.

### T3: ConversusConfig Pydantic Model Scope

**functional-typing** recommends (Rec 7, P3) creating a `ConversusConfig` Pydantic model wrapping the full `conversus.yml` config, including `ArbiterConfig` with typed `ArbiterTiming` and `InfluenceLevel` fields.

**game-engine-advocate** would support this but notes the model must be designed for extensibility. A frozen `ConversusConfig` model would reject unknown fields from plugin configs. The model should either use `model_config = {"extra": "allow"}` for plugin sections or define a `plugins: dict[str, Any]` catch-all field. The functional-typing recommendation does not address this, and a strict model could block plugin config injection.

## Safe Agreements

### SA1: Influence-Aware Heading Validation Is P1
Both agents agree the static `required_headings` in `cooperative.yml` is the highest-priority gap. functional-typing's approach (typed `dict[InfluenceLevel, list[str]]` on ArbitrationConfig) is compatible with game-engine-advocate's preferred solution (structured data that plugins could extend).

### SA2: StrEnum Implementation Is Correct and Extensible
Both agents validate the StrEnum pattern. functional-typing confirms the closed behavioral enum pattern; game-engine-advocate confirms the factory extension docstrings. No disagreement on the current implementation.

### SA3: config_conditions Are Metadata-Only (Not Linter-Enforced)
functional-typing's Off-Base Assumption 1 identifies that `config_conditions` are not evaluated by the linter. game-engine-advocate validates the `config_conditions` schema entries as correctly provisioned for future use. Both agree the conditions exist in schema but are not enforced -- they differ only in whether this is a gap (functional-typing) or correct forward-provisioning (game-engine-advocate).

### SA4: ErrorType Reclassification Is Warranted
functional-typing identifies semantic misuse of `ErrorType.MISSING_VARIABLE` for missing template directories (Rec 3). game-engine-advocate does not address this directly but the new error types (MISSING_TEMPLATE, INVALID_SCHEMA_ENTRY) are additive StrEnum members that follow the factory extension pattern. No extensibility concern.

### SA5: Backward Compatibility Is Preserved
Both agents confirm that omitting `timing` and `influence` produces behavior identical to pre-spec-006 defaults. The default values (`final`, `binding`) are correctly implemented.
