# Cooperative Review — functional-typing

## Executive Summary

Spec 006 introduces inter-round arbitration with configurable influence levels, adding two orthogonal capabilities (`timing` and `influence`) to the existing arbiter subsystem. From a functional programming and type safety perspective, the implementation is remarkably well-grounded. The `InfluenceLevel` and `ArbiterTiming` StrEnums in `models.py` are correctly defined as closed behavioral enums per Constitution Principle IX, the Pydantic models enforce immutability via `frozen=True` and `extra: "forbid"`, and the linter's validation pipeline is composed of pure functions that take explicit inputs and return typed `LintError` lists without side effects.

The spec's primary weakness is a consistency gap: `validate.py` compares phase names against raw string literals (`phase == "arbitration"`, `phase == "synthesis"`, `phase == "cross-round-synthesis"`) in five locations rather than using the `Phase` StrEnum that `models.py` already defines. The `Phase` enum exists, is imported nowhere in `validate.py`, and its members go unused in the exact code paths where they should enforce exhaustive matching. Additionally, the `cooperative.yml` mode schema hardcodes the `required_headings` for arbitration as binding-only headings with no mechanism to express influence-adjusted alternatives, creating a structural gap that FR-023 identifies but the schema does not yet model.

My most important recommendation: import and use the `Phase` StrEnum in `validate.py` for all phase comparisons, completing the enum coverage that Constitution Principle IX mandates for closed behavioral choices with distinct code paths.

## Alignment

- **StrEnum for InfluenceLevel and ArbiterTiming** (`models.py`, L24-43): Both enums correctly use `StrEnum` from Python 3.11+, making them YAML-serializable while preserving type safety. Each value triggers distinct template language, dispute counting logic, and heading validation -- exactly the "closed behavioral choice" pattern that Principle IX mandates. `[constitution.md, L185-188]`

- **Pydantic model immutability** (`models.py`, L247): `TemplateContext` sets `model_config = {"extra": "forbid", "frozen": True}`, preventing undeclared variables from sneaking through and making context instances immutable after construction. This enforces the FP principle that data should not be mutated after creation. `[python-functional-howto.md, L82-93]`

- **Pure function composition in validate.py** (`validate.py`, L315-339): The `validate_template` function composes five pure check functions (`check_unknown_variables`, `check_missing_required_variables`, `check_mode_specific_variables`, `check_required_headings`, `check_structural_markers`) by concatenating their return lists. Each function takes explicit typed inputs and returns `list[LintError]` with no side effects. This is textbook functional composition. `[constitution.md, L149-157]`

- **INFLUENCE_LEVEL typed as InfluenceLevel enum** (`models.py`, L360): `ArbitrationContext.INFLUENCE_LEVEL` is typed as `InfluenceLevel` with default `InfluenceLevel.BINDING`, not as a raw string. This means Pydantic validates influence values at construction time, catching invalid values before template substitution. `[constitution.md, L175-177]`

- **ConfigCondition Pydantic model** (`models.py`, L122-133): The `config_conditions` field on `VariableDefinition` uses a typed `ConfigCondition` model rather than raw dicts, exactly as Principle IX mandates: "Raw dicts from YAML/JSON parsing MUST be loaded into typed Pydantic models before use." `[constitution.md, L175-177]`

- **Open vs. closed enum distinction** (`models.py`, L69-73, L77-93): The code correctly distinguishes between closed behavioral enums (`Phase`, `ErrorType`, `InfluenceLevel`, `ArbiterTiming` as StrEnums) and open registries (`VALID_VARIABLE_TYPES` as `frozenset[str]`, mode names via `get_valid_modes()`). This directly follows the Principle IX guidance on when to use StrEnum vs. str+frozenset. `[constitution.md, L185-194]`

## Missed Opportunities

- **Phase enum unused in validate.py**: `validate.py` imports `VALID_PHASES` (the backward-compatible `frozenset[str]`) but never imports or uses the `Phase` StrEnum. Lines 248, 258, 270, 293, and 294 compare `phase` against string literals like `"arbitration"`, `"synthesis"`, and `"cross-round-synthesis"`. These are closed behavioral comparisons -- each triggers distinct validation logic -- and should use `Phase.ARBITRATION`, `Phase.SYNTHESIS`, `Phase.CROSS_ROUND_SYNTHESIS`. The `Phase` enum was defined precisely for this purpose. Impact: **high**. `[models.py, L77-89; constitution.md, L185-188]`

- **No influence-aware heading model in mode schema**: `cooperative.yml` (L39-44) hardcodes `required_headings` as `["Process Note", "Decision Framework", "Binding Decisions", "Summary of Changes Required"]`. These are binding-only headings. When `influence: recommended` or `influence: advisory`, FR-023 requires different headings ("Recommended Resolutions", "Advisory Opinions", etc.). The mode schema has no mechanism to express this mapping -- the SKILL.md handles it procedurally, but the schema and linter cannot validate influence-adjusted headings statically. A richer `ArbitrationConfig` model with per-influence heading sets would close this gap. Impact: **high**. `[spec.md, L172-180; cooperative.yml, L39-44]`

- **Missing `ArbiterTiming` usage in SKILL.md validation logic**: The SKILL.md config parsing section (L187-191) describes validation of `arbiter.timing` and `arbiter.influence` using string comparisons. The StrEnums exist in `models.py` but there is no corresponding Pydantic config model that would enforce `ArbiterTiming` and `InfluenceLevel` at parse time. A `ConversusConfig` Pydantic model wrapping the full YAML config would catch invalid timing/influence values through Pydantic validation rather than ad-hoc string checks. Impact: **medium**. `[constitution.md, L175-177; models.py, L24-43]`

- **`VariableDefinition.phases` uses `list[str]` instead of `list[Phase]`**: In `models.py` L144, the `phases` field is typed as `list[str]` with a separate `field_validator` that checks against `VALID_PHASES`. If this were `list[Phase]`, Pydantic would enforce valid phase values at deserialization time without requiring a custom validator. The `Phase` StrEnum is YAML-compatible (it serializes as its string value), so this would work transparently. Impact: **medium**. `[models.py, L144, L160-169]`

- **`LintError.error_type` not validated in the string path**: In `models.py` L225, `error_type` is typed as `ErrorType`, which is correct. However, in `validate.py` L370 and L380, `LintError` instances are constructed with `error_type=ErrorType.MISSING_VARIABLE` for missing template directories and `ErrorType.UNKNOWN_VARIABLE` for unrecognized template names. These are semantic misuses -- a missing directory is not a "missing variable" and an unrecognized template name is not an "unknown variable." This suggests the `ErrorType` enum needs additional members (e.g., `MISSING_TEMPLATE`, `INVALID_SCHEMA_ENTRY`) or these errors need reclassification. Impact: **medium**. `[models.py, L96-106; validate.py, L370, L380]`

- **No exhaustive match enforcement**: Python's `match`/`case` with StrEnum can enforce exhaustive matching. The codebase uses `if`/`elif` chains for phase-specific logic in `check_required_headings` (L248-282) and `check_structural_markers` (L292-296). A `match phase:` statement would make missing cases visible and trigger linter warnings when new enum members are added. Impact: **medium**. `[python-functional-howto.md, general principles; constitution.md, L185-188]`

- **`ModeSchema.mode` is `str` rather than validated against available modes**: In `models.py` L205, `ModeSchema.mode` is typed as bare `str`. While the docstring explains that mode validity is enforced by file existence, a `field_validator` checking against dynamically discovered modes (via `get_valid_modes()`) would catch invalid mode names at model construction time. Impact: **low**. `[models.py, L204-218]`

- **PRIOR_ARBITRATION_SECTION required:true but conditionally present**: In `variables.yml` L177, `PRIOR_ARBITRATION_SECTION` is marked `required: true` with a `config_conditions` block. The linter currently treats `required: true` as unconditional (L193-196 in `validate.py` -- the `config_conditions` field is present on the model but never evaluated during validation). This means the linter will flag templates missing `{PRIOR_ARBITRATION_SECTION}` even when the variable is only required under `arbiter.timing == inter-round`. Impact: **medium**. `[variables.yml, L169-181; validate.py, L183-209]`

## Off-Base Assumptions

- **Assumption: config_conditions are enforced during linting** (`variables.yml`, L94-96, L144-145, L178-181): The `variables.yml` schema defines `config_conditions` on several variables (ROUND, MAX_ROUNDS, PRIOR_SYNTHESIS_PATH, PRIOR_ARBITRATION_PATH, PRIOR_ARBITRATION_SECTION, etc.), suggesting these conditions control when the variable is required. However, `validate.py`'s `check_missing_required_variables` function (L183-209) does not evaluate `config_conditions` at all -- it checks `required`, `phases`, and `modes` but ignores `config_conditions`. The conditions are metadata-only, not enforced. This creates a false sense of precision: the schema declares conditions that the tooling does not implement. For spec 006's new variables (`PRIOR_ARBITRATION_SECTION`, `INFLUENCE_LEVEL`), this means the linter will either always require them (if `required: true`) or never require them (if `required: false`), regardless of the declared conditions.

- **Assumption: the linter can validate influence-adjusted headings** (`spec.md`, FR-023; `cooperative.yml`, L39-44): FR-023 specifies that Phase 6 output validation must use influence-adjusted headings. The mode schema (`cooperative.yml`) only stores one set of `required_headings` -- the binding defaults. The linter's `check_required_headings` function reads from `mode_schema.arbitration.required_headings` without any awareness of influence level. This means the linter validates templates against binding headings regardless of influence, and cannot catch a template that uses "Recommended Resolutions" instead of "Binding Decisions." This is a design gap, not a bug -- linting is config-unaware by design -- but the spec's FR-023 language implies validation happens at the linter level when it actually must happen at runtime in the orchestrator.

## Actionable Recommendations

1. **Use Phase enum in validate.py** (Priority: P1)
   - **Current state**: `validate.py` L248, L258, L270, L293-294 compare `phase` against string literals (`"arbitration"`, `"synthesis"`, `"cross-round-synthesis"`).
   - **Proposed change**: Import `Phase` from `models.py`. Replace all string comparisons with enum members: `phase == Phase.ARBITRATION`, `phase == Phase.SYNTHESIS`, `phase == Phase.CROSS_ROUND_SYNTHESIS`. The `phase` parameter in `check_required_headings` and `check_structural_markers` should be typed as `Phase` instead of `str`.
   - **Rationale**: Constitution Principle IX mandates StrEnum for closed behavioral choices with distinct code paths. Phase comparisons in these functions are exactly that -- each branch triggers distinct validation logic. `[constitution.md, L185-188]`
   - **Risk if ignored**: Adding a new phase (e.g., from a plugin) will require searching for string literals rather than following the type system. Typos in phase strings will not be caught at import time.

2. **Add influence-aware heading map to ArbitrationConfig** (Priority: P1)
   - **Current state**: `ArbitrationConfig` in `models.py` L191-194 has `required_headings: list[str]`, and `cooperative.yml` hardcodes binding headings. The SKILL.md (L651-653) describes the influence-to-heading mapping procedurally.
   - **Proposed change**: Extend `ArbitrationConfig` with an `influence_headings` field: `influence_headings: dict[InfluenceLevel, list[str]] = Field(default_factory=dict)`. Populate in `cooperative.yml` with all three heading sets. Provide a `get_headings(influence: InfluenceLevel) -> list[str]` method that returns `required_headings` as the binding default or the influence-specific override.
   - **Rationale**: The heading-to-influence mapping is a closed behavioral choice that belongs in typed data, not in procedural SKILL.md prose. Modeling it in the schema makes it available to both the linter (future config-aware validation) and the orchestrator. `[spec.md, L172-180; constitution.md, L185-188]`
   - **Risk if ignored**: The influence-heading mapping exists only in SKILL.md prose, unreachable by the linter or any Pydantic validation. If someone adds a new influence level, there is no schema-level reminder to define its headings.

3. **Reclassify semantic misuses of ErrorType** (Priority: P2)
   - **Current state**: `validate.py` L370 uses `ErrorType.MISSING_VARIABLE` for missing template directories, and L380 uses `ErrorType.UNKNOWN_VARIABLE` for unrecognized template names in mode schema. These are not variable errors.
   - **Proposed change**: Add `ErrorType.MISSING_TEMPLATE = "missing_template"` and `ErrorType.INVALID_SCHEMA_ENTRY = "invalid_schema_entry"` to the `ErrorType` enum. Update the `validate_all` function to use the new error types. Update `KNOWN_ERROR_TYPES` (the backward-compatible frozenset alias).
   - **Rationale**: Each ErrorType member should map to a distinct detection mechanism, per the enum's own docstring: "each has distinct detection logic in check_* functions." Using MISSING_VARIABLE for a missing directory conflates two unrelated error categories. `[models.py, L96-100]`
   - **Risk if ignored**: Consumers filtering errors by type (e.g., "show me all missing variable errors") will get false matches from directory and schema issues.

4. **Type VariableDefinition.phases as list[Phase]** (Priority: P2)
   - **Current state**: `models.py` L144 types `phases` as `list[str]` with a custom validator (L160-169) checking against `VALID_PHASES`.
   - **Proposed change**: Change to `phases: list[Phase]`. Remove the `validate_phases` field_validator -- Pydantic will enforce valid Phase values during deserialization of the YAML-derived dict, since `Phase` is a StrEnum.
   - **Rationale**: This eliminates a manual validator by leveraging the type system directly. Fewer validators means less surface area for bugs. The Phase enum was created to replace string-based phase references. `[constitution.md, L185-188]`
   - **Risk if ignored**: The manual validator duplicates what the type system could enforce automatically, creating two places to update when phases change.

5. **Implement config_conditions evaluation in the linter** (Priority: P2)
   - **Current state**: `variables.yml` declares `config_conditions` on ROUND, MAX_ROUNDS, PRIOR_SYNTHESIS_PATH, PRIOR_ARBITRATION_PATH, PRIOR_ARBITRATION_SECTION, and INFLUENCE_LEVEL. `validate.py` never evaluates these conditions.
   - **Proposed change**: In `check_missing_required_variables`, when a variable has `config_conditions`, skip the required check (the variable is conditionally required and cannot be validated without config context). Alternatively, add a `config_aware_validate` function that accepts a parsed config and evaluates conditions. At minimum, document that `config_conditions` are schema metadata only, not linter-enforced, to prevent false expectations.
   - **Rationale**: The current state is misleading -- the schema declares precision that the tooling does not deliver. Spec 006 adds two new variables with config_conditions, compounding the gap. `[variables.yml, L169-189; validate.py, L183-209]`
   - **Risk if ignored**: Developers writing new templates will see `config_conditions` in the schema and assume the linter enforces them. When it does not, they may omit conditionally-required variables without linter feedback.

6. **Use match/case for phase-specific validation logic** (Priority: P2)
   - **Current state**: `check_required_headings` (L248-282) and `check_structural_markers` (L292-296) use `if`/`elif` chains for phase dispatch.
   - **Proposed change**: Refactor to `match phase:` with `case Phase.ARBITRATION:`, `case Phase.SYNTHESIS:`, `case Phase.CROSS_ROUND_SYNTHESIS:`, and a `case _:` default. This makes the exhaustiveness of the match visible and triggers linter warnings if a new Phase member is added without a corresponding case.
   - **Rationale**: Python 3.10+ structural pattern matching with StrEnum provides compile-time-adjacent exhaustiveness checking when paired with tools like mypy or pyright. This is the idiomatic way to handle closed behavioral dispatch in modern Python. `[python-functional-howto.md, general principles; constitution.md, L185-188]`
   - **Risk if ignored**: Adding a new phase to the Phase enum will not produce any warning in `check_required_headings` or `check_structural_markers`, making it easy to forget phase-specific validation.

7. **Create a ConversusConfig Pydantic model** (Priority: P3)
   - **Current state**: SKILL.md describes config validation procedurally (L173-199). There is no Pydantic model for the full `conversus.yml` config.
   - **Proposed change**: Define `ArbiterConfig(BaseModel)` with `timing: ArbiterTiming = ArbiterTiming.FINAL` and `influence: InfluenceLevel = InfluenceLevel.BINDING`, and a top-level `ConversusConfig(BaseModel)` wrapping all config fields. The SKILL.md orchestrator would parse YAML into this model, getting Pydantic validation of timing/influence values for free.
   - **Rationale**: Constitution Principle IX: "ALL data structures MUST use Pydantic models for validation and type safety. Raw dicts from YAML/JSON parsing MUST be loaded into typed Pydantic models before use." The config is currently a raw dict. `[constitution.md, L175-177]`
   - **Risk if ignored**: The InfluenceLevel and ArbiterTiming enums exist but are only used in ArbitrationContext (the template context model). The config itself -- where these values originate -- is validated by ad-hoc string comparisons in the orchestrator rather than by the type system.

8. **Add PRIOR_ARBITRATION_PATH to ReviewContext as mandatory for inter-round** (Priority: P3)
   - **Current state**: `ReviewContext` in `models.py` L267 has `PRIOR_ARBITRATION_PATH: Optional[Path] = None`. FR-013 states this MUST be a mandatory read when inter-round arbitration fired in the prior round.
   - **Proposed change**: Consider adding a `model_validator` on `ReviewContext` that enforces: when `PRIOR_ARBITRATION_SECTION` is non-empty, `PRIOR_ARBITRATION_PATH` must also be non-None. This would catch orchestrator bugs where the section text is populated but the path is missing.
   - **Rationale**: FR-013 explicitly says "MUST receive {PRIOR_ARBITRATION_PATH} as a mandatory read." The current Optional typing does not enforce this constraint. A cross-field validator would. `[spec.md, L143; models.py, L267]`
   - **Risk if ignored**: An orchestrator bug could populate the arbitration section text without providing the path, causing the agent to see instructions referencing a document it cannot read.

## Referenced Documentation

- `conversus/.specify/memory/constitution.md` -- sections/lines cited: L141-194 (Principle IX: Functional Programming and Clean Code, Explicit Typing), L175-177 (Pydantic mandate), L185-194 (StrEnum vs. frozenset guidance)
- `conversus/.firecrawl/python-functional-howto.md` -- sections/lines cited: L82-93 (FP introduction, immutability), general principles (composition, pure functions)
- `conversus/linter/models.py` -- sections/lines cited: L24-43 (InfluenceLevel, ArbiterTiming StrEnums), L69-73 (VALID_VARIABLE_TYPES), L77-93 (Phase, VALID_PHASES), L96-110 (ErrorType, KNOWN_ERROR_TYPES), L122-133 (ConfigCondition), L135-169 (VariableDefinition), L191-194 (ArbitrationConfig), L204-218 (ModeSchema), L221-228 (LintError), L235-250 (TemplateContext), L253-269 (ReviewContext), L347-361 (ArbitrationContext), L377-395 (PHASE_CONTEXT_MODELS, runtime assertion)
- `conversus/linter/validate.py` -- sections/lines cited: L183-209 (check_missing_required_variables), L238-282 (check_required_headings), L285-312 (check_structural_markers), L315-339 (validate_template), L346-402 (validate_all), L370, L380 (misclassified error types)
- `conversus/schema/variables.yml` -- sections/lines cited: L94-96 (ROUND config_conditions), L136-167 (PRIOR_ARBITRATION_PATH, ARBITRATION_PATHS, ARBITRATION_RULINGS), L169-189 (PRIOR_ARBITRATION_SECTION, INFLUENCE_LEVEL)
- `conversus/schema/modes/cooperative.yml` -- sections/lines cited: L39-44 (arbitration required_headings)
- `conversus/specs/006-inter-round-arbitration/spec.md` -- sections/lines cited: L115-118 (FR-001 through FR-004), L143 (FR-013), L161-162 (FR-018, FR-019), L172-180 (FR-023)
- `conversus/SKILL.md` -- sections/lines cited: L78-79 (timing/influence config fields), L187-191 (validation rules), L488-509 (inter-round arbitration), L651-655 (influence-adjusted heading validation)
- `conversus/templates/cooperative/arbitration.md` -- sections/lines cited: L11 (INFLUENCE_LEVEL usage), L70-73 (influence-adjusted heading instructions)
- `conversus/templates/cooperative/synthesis.md` -- sections/lines cited: L103-112 (Arbiter-Resolved Disputes section)
- `conversus/templates/cooperative/review.md` -- sections/lines cited: L24 (PRIOR_ARBITRATION_SECTION placement)
- `conversus/templates/cooperative/cross-round-synthesis.md` -- sections/lines cited: L92-100 (Resolution Attribution section)
