# Schema Engineer Review: 012-game-form-schemas

**Reviewer**: schema-engineer
**Date**: 2026-03-22
**Spec**: 012-game-form-schemas

---

### Executive Summary

Spec 012 establishes the mathematical vocabulary for the conversus game engine by defining four game theory forms (normal-form, GNEP, parametric, Stackelberg) as YAML schemas with corresponding Pydantic models. The scope is deliberately narrow: pure data schemas with no solver logic. This is the right call. The models are clean, the structural validators catch the most critical invariants (dimension matching, player-objective alignment), and the error messages are genuinely useful. The separation of schema from computation is a solid foundation that specs 013-020 can build on.

However, the current implementation leaves significant Pydantic capability on the table. The models do not use `Literal` types for the `form` discriminator, do not leverage Pydantic's discriminated union pattern for polymorphic deserialization, and duplicate validation logic across `GNEPGame` and `ParametricGame` rather than expressing the inheritance relationship the spec describes. The `ParametricGame` is described as "extending GNEP" in both the spec prose and the YAML schema, yet the Pydantic model copies all GNEP fields and validators verbatim. This duplication will become a maintenance hazard as downstream specs add fields or tighten invariants.

The package structure also needs attention. The spec requires `conversus-schemas` to be a standalone pip-installable package (FR-010), but the `pyproject.toml` declares the package as `conversus` with no sub-package or separate build target for `conversus-schemas`. The YAML files are referenced via `Path(__file__).parent.parent.parent` filesystem traversal, which will break the moment the package is installed in a site-packages directory rather than run from the source tree. These are solvable problems, but they need to be solved before spec 013 starts adding more models to the same package.

### Alignment

- **Pydantic `model_validator(mode="after")` is used correctly** for cross-field structural invariants (payoff dimensions vs. strategy cardinalities, player-objective matching). This is the right hook for these checks.
- **Error messages are specific and actionable.** They name the offending players, report expected vs. actual dimensions, and distinguish "missing" from "extra." This is materially better than what most schema libraries produce by default.
- **`Optional` fields are correctly typed.** `local_constraints` and `coupled_constraints` default to `None`, not empty collections, which avoids the mutable-default-argument trap and accurately represents "not specified" vs. "empty."
- **`frozenset` for `VALID_FIELD_TYPES`** is the right choice over a plain set -- it signals immutability to both the runtime and the reader.
- **`BaseModel` rather than `dataclass`** is the correct choice here because the models need validators, serialization, and schema generation -- all Pydantic strengths.
- **No solver imports** (FR-008) is enforced and tested (test `test_no_solver_imports` reloads the module and checks `sys.modules`). This is a strong guarantee.

### Missed Opportunities

- **No discriminated union for polymorphic game loading (high).** Downstream consumers (spec 013 references `game_form` as a field, spec 016's `DeliberationState` will carry a game instance) will need to deserialize a YAML blob into the correct model type. Pydantic's `Discriminator` on the `form` field would let consumers write `GameForm.model_validate(data)` and get the right subclass automatically. Without it, every consumer must implement their own dispatch table.

- **No `Literal` type on `form` fields (high).** Each model declares `form: str = "normal-form"` with a default but no constraint. A `NormalFormGame` instance with `form: "gnep"` will validate without error. Using `form: Literal["normal-form"]` would catch this at validation time and enable discriminated unions.

- **`ParametricGame` duplicates `GNEPGame` validation logic verbatim (medium).** The spec explicitly says "inherits all GNEP fields." The Pydantic model should inherit from `GNEPGame` (adding `parameters` and overriding `form`) or extract shared validation into a mixin/base. The current copy-paste means a bug fix in GNEP validation must be applied in two places.

- **No `model_config` for JSON schema generation (medium).** Pydantic v2's `model_config = ConfigDict(json_schema_extra=...)` and `Field(json_schema_extra=...)` can produce OpenAPI-compatible JSON Schema from these models. Spec 013 FR-008 requires an `ObjectiveTemplate` model that validates template YAML and references `game_form` from spec 012. If the game form models exported clean JSON Schema, the template models could use `$ref` for cross-schema validation.

- **No `field_validator` for individual field sanity checks (medium).** `players` accepts an empty list silently -- the `model_validator` only checks player-strategy alignment, not that `players` is non-empty. Similarly, `strategies` keys that are not in `players` are only caught implicitly. Field-level validators with `@field_validator("players")` would catch these earlier with better error locality.

- **No `model_serializer` or custom `model_dump` for round-trip fidelity (low).** The YAML schemas use `constraint_list` as a type, but the Pydantic models type constraints as `list[str]` or `dict[str, list[str]]`. There is no mechanism to validate that constraint expressions conform to any syntax. While full expression parsing is out of scope (FR-008), a regex-based `field_validator` could at least reject obviously malformed constraints (empty strings, missing operators).

- **`ModeMapping.lookup()` raises raw `KeyError` instead of a custom exception (low).** Downstream specs will need to distinguish "mode not found" from other key errors. A `ModeNotFoundError(KeyError)` subclass would be more ergonomic for consumers.

- **No `__repr__` or `__str__` customization (low).** When debugging, `NormalFormGame(form='normal-form', players=['Alice', 'Bob'], strategies=..., payoff_matrix=[[...]])` dumps the entire payoff matrix. A custom `__repr__` that truncates large structures would help during development.

- **`load_mode_mapping` has no caching (low).** If called multiple times in a plugin pipeline, it re-reads and re-parses the YAML file every time. A `@functools.lru_cache` or module-level singleton would be appropriate for an immutable mapping file.

### Off-Base Assumptions

- **The YAML schema files serve as both documentation AND runtime-loadable package data, but the code assumes filesystem layout.** The `_schema_dir()` function navigates `Path(__file__).parent.parent.parent / "schema" / "game-forms"`. This works in a source checkout but will fail when `conversus-schemas` is installed via pip, because `schema/` is not inside the Python package directory (`src/conversus_schemas/`). FR-011 requires YAML files to be "included as package data, loadable at runtime," but the current layout and `pyproject.toml` do not configure this. Either the YAML files must move inside `src/conversus_schemas/` or `importlib.resources` must be used instead of path traversal.

- **The spec states `ParametricGame` "inherits all GNEP fields" but the Pydantic model uses flat composition, not inheritance.** This is not merely a style choice -- it means `isinstance(parametric_game, GNEPGame)` returns `False`, which will surprise downstream code (spec 016 plugins, spec 017 equilibrium scorer) that may want to accept "any GNEP-like game" polymorphically. The spec's language implies an is-a relationship that the code does not express.

- **The `strategies` field in `NormalFormGame` is typed as `dict[str, list[str]]` but the YAML schema declares its type as `list[string]`.** The YAML schema `fields` section says `type: list[string]`, but the actual data structure (and the Pydantic model) is a mapping from player name to a list of strategy labels. This mismatch between the YAML schema's declared type system and the Pydantic model's actual types will cause confusion for anyone reading the YAML schema to understand the expected data shape.

- **`constraint_list` as a "closed set" type (FR-003) is underspecified.** The YAML schemas declare fields of type `constraint_list`, but the Pydantic models type these as `Optional[dict[str, list[str]]]` (per-player) or `Optional[list[str]]` (shared). There is no Pydantic type alias, custom type, or validator that corresponds to `constraint_list`. The closed type system exists only in the YAML documentation layer, not in the validation layer, making it a documentation fiction.

### Actionable Recommendations

1. **P1 -- Use `Literal` types for `form` discriminators.**
   - Current: `form: str = "normal-form"` on each model.
   - Proposed: `form: Literal["normal-form"] = "normal-form"` (and similarly for each form).
   - Rationale: Prevents cross-contamination (e.g., a GNEP payload accidentally validated by `NormalFormGame`). Enables Pydantic discriminated unions. Zero runtime cost.
   - Risk if ignored: Downstream specs that dispatch on `form` will need manual guards; silent misvalidation possible.

2. **P1 -- Create a discriminated union type `GameForm`.**
   - Current: No union type; consumers must dispatch manually.
   - Proposed: `GameForm = Annotated[Union[NormalFormGame, GNEPGame, ParametricGame, StackelbergGame], Discriminator("form")]` exported from `game_forms.py` and `__init__.py`.
   - Rationale: Spec 013 FR-002 requires `game_form` as a field on `ObjectiveTemplate`. Spec 016's `DeliberationState` will carry a game instance. A discriminated union lets both specs write `game: GameForm` and get automatic deserialization. This is the single highest-impact change for downstream ergonomics.
   - Risk if ignored: Every downstream consumer independently implements form dispatch, leading to inconsistent error handling and N copies of the same switch statement.

3. **P1 -- Fix package data resolution for installed packages.**
   - Current: `_schema_dir()` uses `Path(__file__).parent.parent.parent / "schema"`, which only works from the source tree.
   - Proposed: Use `importlib.resources.files("conversus_schemas") / "schema" / "game-forms"` and move the YAML files into the package, or add `[tool.setuptools.package-data]` to `pyproject.toml` with the correct paths. Alternatively, embed the schema data as Python constants if the files are small.
   - Rationale: FR-010 and FR-011 require a pip-installable package with bundled schema files. The current code fails this requirement when installed outside the source tree.
   - Risk if ignored: `load_mode_mapping()` and any future schema-loading function will raise `FileNotFoundError` in production installations.

4. **P1 -- Express `ParametricGame` inheritance from `GNEPGame`.**
   - Current: `ParametricGame(BaseModel)` copies all GNEP fields and validation logic.
   - Proposed: `ParametricGame(GNEPGame)` with `form: Literal["parametric"] = "parametric"` override and additional `parameters` field. Override `validate_structure` to call `super()` then check parameters.
   - Rationale: Eliminates duplicated validation code. Enables `isinstance(parametric, GNEPGame)` checks in downstream specs. Matches the spec's stated semantics.
   - Risk if ignored: Validation drift between GNEP and Parametric models. Downstream code cannot treat parametric games as GNEPs polymorphically.

5. **P2 -- Add `@field_validator("players")` for non-empty player lists.**
   - Current: An empty `players: []` passes field-level validation; the `model_validator` may or may not catch it depending on the form.
   - Proposed: `@field_validator("players") @classmethod def check_non_empty(cls, v): if not v: raise ValueError("Game must have at least one player."); return v`
   - Rationale: Fails fast with a clear message instead of producing confusing downstream errors (e.g., empty payoff matrix dimensions).
   - Risk if ignored: Edge case where empty player list produces cryptic validator errors.

6. **P2 -- Add a `StackelbergGame` validator ensuring leader is not in followers.**
   - Current: No check that `leader` and `followers` are disjoint.
   - Proposed: In `validate_structure`, assert `self.leader not in self.followers` with a message like "Leader '{self.leader}' cannot also be a follower."
   - Rationale: This is a structural invariant of the Stackelberg form. The spec says "leader commits first; followers respond." A player cannot be both.
   - Risk if ignored: Semantically invalid game instances pass validation, producing undefined behavior in downstream solvers (spec 017, 019).

7. **P2 -- Add a `StackelbergGame` validator ensuring `leader_variables` is non-empty.**
   - Current: `leader_variables: list[str]` accepts empty lists.
   - Proposed: `@field_validator("leader_variables") @classmethod def check_non_empty(cls, v): if not v: raise ValueError("Leader must have at least one decision variable."); return v`
   - Rationale: A leader with no variables is a degenerate case that the Stackelberg form cannot meaningfully represent.
   - Risk if ignored: Degenerate game instances pass validation.

8. **P2 -- Align YAML schema field types with Pydantic model types.**
   - Current: YAML says `strategies` has type `list[string]`, but the model types it as `dict[str, list[str]]`. YAML says `objectives` has type `list[string]`, but the model types it as `dict[str, str]`.
   - Proposed: Either update the YAML schema's `type` field to reflect the actual structure (e.g., `type: map[string, list[string]]`) or extend the closed type set in FR-003 to include map types.
   - Rationale: The YAML schemas are meant to be the authoritative documentation of data shape. If they disagree with the Pydantic models, one or both are wrong.
   - Risk if ignored: Consumers reading the YAML schema will construct invalid data and get confused by validation errors.

9. **P3 -- Export `ModeFormMapping` from `__init__.py`.**
   - Current: `__init__.py` exports `load_mode_mapping` but not `ModeFormMapping` or `ModeMapping`.
   - Proposed: Add `ModeMapping` and `ModeFormMapping` to `__all__`.
   - Rationale: Downstream specs may want to type-hint function parameters as `ModeMapping` or iterate over `ModeFormMapping` entries. Currently they must import from the submodule.
   - Risk if ignored: Minor ergonomic friction for downstream consumers.

10. **P3 -- Add `model_config = ConfigDict(frozen=True)` to all game form models.**
    - Current: Models are mutable after construction.
    - Proposed: `model_config = ConfigDict(frozen=True)` on the base or on each model.
    - Rationale: Game form schemas are definitional data -- they describe structure, not mutable state. Freezing them prevents accidental mutation and signals intent. It also makes them hashable, which could be useful for caching in plugin pipelines.
    - Risk if ignored: Accidental mutation in plugin code could corrupt shared game form instances.

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/012-game-form-schemas/spec.md`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/normal-form.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/gnep.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/parametric.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/stackelberg.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/mode-mapping.yml`
- `<HOME>/code/payer-index-mono/conversus/src/conversus_schemas/game_forms.py`
- `<HOME>/code/payer-index-mono/conversus/src/conversus_schemas/__init__.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_game_forms.py`
- `<HOME>/code/payer-index-mono/conversus/pyproject.toml`
- `<HOME>/code/payer-index-mono/conversus/specs/013-objective-function-templates/spec.md`
- `<HOME>/code/payer-index-mono/conversus/specs/016-plugin-system/spec.md`
- `<HOME>/code/payer-index-mono/conversus/specs/019-config-optimizer/spec.md`
