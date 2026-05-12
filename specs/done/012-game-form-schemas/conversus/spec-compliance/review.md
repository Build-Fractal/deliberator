# Spec Compliance Review: 012-game-form-schemas

**Reviewer role**: spec-compliance
**Date**: 2026-03-22
**Spec under review**: `/conversus/specs/012-game-form-schemas/spec.md`

---

### Executive Summary

Spec 012 establishes a library of four game theory form schemas (normal-form, GNEP, parametric, Stackelberg), a mode-to-form mapping, and corresponding Pydantic validation models. The implementation covers the full FR surface area (FR-001 through FR-011) and tests explicitly track all four success criteria (SC-001 through SC-004). This is a schema-only spec with no solver logic, and the boundary is cleanly respected.

The overall compliance posture is **strong with material gaps in FR-003, FR-010, and FR-011**. The YAML schema files exist and are well-structured, the Pydantic models enforce the stated structural invariants, and the test suite is directly mapped to the success criteria. However, several field type declarations in the YAML schemas are semantically incorrect (FR-003 type mismatch between declared types and actual example structures), the `pyproject.toml` defines the package as `conversus` rather than `conversus-schemas` (FR-010), and there is no evidence that YAML schema files are bundled as package data (FR-011). These are not cosmetic issues; they affect downstream consumers who rely on the schema files and import paths specified in the spec.

From a compliance standpoint, 7 of 11 FRs are fully met, 2 are partially met, and 2 are not met. All four SCs are functionally met by the test suite, though SC-004 is tested at the wrong granularity (it tests import safety within the existing environment rather than in a minimal `pydantic`+`pyyaml`-only environment as specified).

---

### Alignment

- **FR-001 (YAML file locations)**: Fully met. All four schema files exist at the specified paths: `schema/game-forms/normal-form.yml`, `schema/game-forms/gnep.yml`, `schema/game-forms/parametric.yml`, `schema/game-forms/stackelberg.yml`.

- **FR-002 (top-level fields)**: Fully met. Every YAML file contains `form`, `description`, `fields`, and `example` as top-level keys with the required substructure (per-field name, type, required flag, description).

- **FR-004 (mode-to-form mapping)**: Fully met. `schema/game-forms/mode-mapping.yml` defines all four required mappings: `cooperative -> gnep`, `winner-take-all -> normal-form`, `prisoners-dilemma -> gnep`, `red-blue -> gnep`.

- **FR-005 (override notes)**: Fully met. Each mapping entry includes a `note` field explaining the rationale and, in the case of `winner-take-all`, explicitly noting when an alternative form might be preferred.

- **FR-008 (no solver imports)**: Fully met. `game_forms.py` imports only `pathlib`, `typing`, `yaml`, and `pydantic`. The explicit comment on line 8 references FR-008. The test `test_no_solver_imports` checks for `nashopt`, `jax`, `scipy`, and `amplpy`.

- **FR-009 (import path)**: Fully met. `__init__.py` re-exports `NormalFormGame`, `GNEPGame`, `ParametricGame`, `StackelbergGame` from `conversus_schemas.game_forms`. The import statement `from conversus_schemas.game_forms import ...` matches the spec exactly.

---

### Missed Opportunities

- **FR-003 type mismatch for `strategies` field (normal-form.yml line 27)**: The schema declares `strategies` as `type: list[string]`, but the example shows a `dict[str, list[str]]` (mapping from player name to strategy list), and the Pydantic model types it as `dict[str, list[str]]`. The closed type set in FR-003 does not include `dict` or `map` types, which means the schema either needs a new type or the field type is misstated. Impact: any tooling that consumes the YAML schema declarations for codegen or validation will produce wrong types.

- **FR-003 type mismatch for `decision_variables` (gnep.yml line 28, parametric.yml line 29)**: Declared as `type: list[string]` but the example is a `dict[str, list[str]]` and the Pydantic model is `dict[str, list[str]]`. Same issue as above.

- **FR-003 type mismatch for `objectives` (gnep.yml line 35, parametric.yml line 35)**: Declared as `type: list[string]` but the example is a `dict[str, str]` and the Pydantic model is `dict[str, str]`. Neither `dict[str, str]` nor `map` appear in the closed type set.

- **FR-003 type mismatch for `follower_variables` (stackelberg.yml line 41)**: Declared as `type: list[string]` but the example and Pydantic model use `dict[str, list[str]]`.

- **FR-003 type mismatch for `follower_objectives` (stackelberg.yml line 55)**: Declared as `type: list[string]` but the example and Pydantic model use `dict[str, str]`.

- **FR-007 partial: `form` field not validated against expected value**: The Pydantic models declare `form` with a default value (e.g., `form: str = "normal-form"`) but do not validate that the provided value matches the expected form identifier. A `NormalFormGame` instance could be created with `form: "gnep"` and pass validation. This violates the spirit of FR-007 ("enforce required fields, type constraints, and structural invariants").

- **FR-010 package naming**: The spec requires models to ship in the `conversus-schemas` package. The `pyproject.toml` defines `name = "conversus"`, not `name = "conversus-schemas"`. The importable package directory is `src/conversus_schemas/` (which works at module level), but the pip-installable package name is `conversus`, not `conversus-schemas`. Downstream specs that `pip install conversus-schemas` will fail.

- **FR-011 package data**: The spec requires YAML schema files to be "included as package data, loadable at runtime for reference and validation." There is no `[tool.setuptools.package-data]` or equivalent configuration in `pyproject.toml`. The `_schema_dir()` function uses relative path traversal from the source file rather than `importlib.resources` or a package data mechanism. This works in development but will break when the package is installed from a wheel (the `schema/` directory is outside `src/` and will not be included).

- **SC-004 environment isolation not truly tested**: The test `test_no_solver_imports` checks that solver modules are not present in `sys.modules` after import, which is a reasonable proxy. However, SC-004 specifies "an environment with only `pydantic` and `pyyaml` installed," which implies an isolated virtual environment test. The current test would pass even if solver libraries were installed but simply not imported. Impact: low, but a CI step with a minimal venv would be more rigorous.

---

### Off-Base Assumptions

- **The closed type set (FR-003) is insufficient for the actual data structures used**: The spec defines 8 allowed types (`string`, `integer`, `float`, `list[string]`, `list[float]`, `matrix`, `function`, `constraint_list`), but at least 6 fields across the four schemas require `dict`-like types (`dict[str, list[str]]`, `dict[str, str]`, `dict[str, list[str]]`). The implementation silently diverges by using `dict` types in Pydantic models while the YAML schemas declare `list[string]`. Either the spec's FR-003 type set needs to be expanded (e.g., add `map[string, list[string]]`, `map[string, string]`), or the YAML schemas need to use compound type descriptors. As-is, the YAML schemas are not self-consistent with their own examples.

- **`ParametricGame` does not actually extend `GNEPGame`**: The spec (Section 2, Parametric Game Form) states "Inherits all GNEP fields." The Pydantic model `ParametricGame` is a standalone `BaseModel` that duplicates the GNEP fields and validation logic rather than inheriting from `GNEPGame`. This means changes to `GNEPGame` validation (e.g., adding a new invariant) will not propagate to `ParametricGame`. The duplication is already visible: the `validate_structure` method in `ParametricGame` (lines 186-213) repeats the same player-objective and decision-variable checks as `GNEPGame` (lines 137-163).

- **`_schema_dir()` assumes a specific directory layout**: The function walks up three parent levels from `game_forms.py` to find the schema directory (line 43: `Path(__file__).resolve().parent.parent.parent / "schema" / "game-forms"`). This only works when the code is run from the source tree. After `pip install`, the `schema/` directory will not be at that relative path. This contradicts FR-011's requirement that YAML files be "loadable at runtime."

---

### Actionable Recommendations

1. **P1 -- Expand FR-003 type set or fix YAML type declarations**
   - **Current state**: At least 6 fields declare `type: list[string]` in YAML but are actually `dict[str, list[str]]` or `dict[str, str]` in both examples and Pydantic models.
   - **Proposed change**: Add `map[string, string]` and `map[string, list[string]]` to the FR-003 closed type set, then update all affected YAML field declarations (`strategies`, `decision_variables`, `objectives`, `follower_variables`, `follower_objectives`, `local_constraints`, `follower_constraints`).
   - **Rationale**: The YAML schemas are the canonical reference for downstream codegen and documentation. Incorrect type declarations undermine the entire purpose of having machine-readable schemas.
   - **Risk if ignored**: Any tooling that reads the YAML `type` field to generate code, documentation, or validation will produce incorrect output. Downstream specs 013-020 that consume these schemas will build on a false foundation.

2. **P1 -- Fix package name to `conversus-schemas` (FR-010)**
   - **Current state**: `pyproject.toml` declares `name = "conversus"`.
   - **Proposed change**: Either rename the package to `conversus-schemas` in `pyproject.toml` or update FR-010 in the spec to match the actual package name. If the intent is that `conversus-schemas` is a sub-package of the broader `conversus` project, this should be documented.
   - **Rationale**: FR-010 explicitly says "MUST ship in the `conversus-schemas` package (pip installable)." The current name does not match.
   - **Risk if ignored**: Downstream specs and consumers that reference `pip install conversus-schemas` will fail. The dependency contract is broken before it starts.

3. **P1 -- Configure YAML files as package data (FR-011)**
   - **Current state**: No `[tool.setuptools.package-data]` in `pyproject.toml`. The `_schema_dir()` function uses relative path traversal that breaks after installation.
   - **Proposed change**: Add package data configuration to include `schema/game-forms/*.yml`. Replace `_schema_dir()` with `importlib.resources` for runtime access. Alternatively, move the YAML files into the `src/conversus_schemas/` package directory.
   - **Rationale**: FR-011 requires YAML files to be "included as package data, loadable at runtime." The current approach only works in development.
   - **Risk if ignored**: Any installed (non-editable) consumer of this package will get `FileNotFoundError` when calling `load_mode_mapping()` without an explicit path.

4. **P2 -- Add `form` field validation with `Literal` types (FR-007)**
   - **Current state**: `form` fields use `str` with a default value but no enforcement. `NormalFormGame(form="gnep", ...)` would pass validation.
   - **Proposed change**: Use `Literal["normal-form"]`, `Literal["gnep"]`, `Literal["parametric"]`, `Literal["stackelberg"]` for the `form` field in each model.
   - **Rationale**: FR-007 requires enforcement of "type constraints and structural invariants." The `form` field is the type discriminator and should be constrained.
   - **Risk if ignored**: Misuse is possible but unlikely in practice. However, if a discriminated union is later built over these models (likely for downstream specs), the lack of `Literal` types will prevent Pydantic's discriminator dispatch from working.

5. **P2 -- Make `ParametricGame` inherit from `GNEPGame`**
   - **Current state**: `ParametricGame` duplicates all GNEP validation logic (lines 186-209 mirror lines 137-162).
   - **Proposed change**: Have `ParametricGame` extend `GNEPGame` and add only the `parameters` field and its non-empty validation.
   - **Rationale**: The spec says "Inherits all GNEP fields." Duplication means future GNEP invariant changes will not propagate. This is a correctness risk for downstream specs that add validation rules.
   - **Risk if ignored**: Validation drift between GNEP and Parametric models as the codebase evolves.

6. **P2 -- Add `local_constraints` and `follower_constraints` type consistency in YAML**
   - **Current state**: `local_constraints` in gnep.yml and parametric.yml is typed as `constraint_list`, which is in the FR-003 set. But the Pydantic model types it as `Optional[dict[str, list[str]]]` -- a per-player mapping, not a flat list. Similarly, `follower_constraints` in stackelberg.yml is `constraint_list` but modeled as `Optional[dict[str, list[str]]]`.
   - **Proposed change**: Either define `constraint_list` semantics precisely (flat list vs. per-player mapping) in the spec, or add a `constraint_map` type to FR-003.
   - **Rationale**: The `constraint_list` type name suggests a flat list, but the actual structure is a per-player mapping. This ambiguity will confuse consumers.
   - **Risk if ignored**: Downstream codegen or validation tooling will interpret `constraint_list` incorrectly.

7. **P2 -- Add a test for SC-001 that matches the exact code in the success criterion**
   - **Current state**: The test `test_normal_form_example_validates` loads the YAML, extracts `data["example"]`, and validates. SC-001's literal code is `NormalFormGame.model_validate(yaml.safe_load(open("schema/game-forms/normal-form.yml")))`, which would validate the *entire file* (including `form`, `description`, `fields`, `example`), not just the `example` key.
   - **Proposed change**: The test is correct in spirit (the whole file should not validate as a game instance). But SC-001's wording should be clarified to say `data["example"]`, or a comment should note the intentional deviation.
   - **Rationale**: Literal compliance with SC-001 as written would fail because the top-level YAML includes `fields` and `description` which are not part of the game model. The test correctly handles this but should document why.
   - **Risk if ignored**: Future auditors may flag this as non-compliant.

8. **P3 -- Add negative tests for `form` field mismatch**
   - **Current state**: No test verifies that `NormalFormGame(form="gnep", ...)` is rejected.
   - **Proposed change**: Add tests for each model that verify the `form` field must match the expected value. These tests would fail today (validating that Recommendation 4 is needed).
   - **Rationale**: Defensive testing against misuse, especially important if discriminated unions are planned.
   - **Risk if ignored**: Misuse goes undetected until a runtime bug surfaces.

9. **P3 -- Add a test that `VALID_FIELD_TYPES` covers all types used in YAML schemas**
   - **Current state**: `VALID_FIELD_TYPES` is defined in `game_forms.py` (line 24-33) but never used for validation. No test verifies that all `type:` values in the YAML files are members of this set.
   - **Proposed change**: Add a parametrized test that loads each YAML schema, extracts all `type` values from the `fields` list, and asserts membership in `VALID_FIELD_TYPES`.
   - **Rationale**: FR-003 mandates a closed type set. The constant exists but is not enforced anywhere. This is dead code unless it is wired into validation.
   - **Risk if ignored**: The closed type set is aspirational rather than enforced. New schema files could introduce arbitrary types without detection.

10. **P3 -- Add `ModeMapping` and `ModeFormMapping` to `__init__.py` exports**
    - **Current state**: `__init__.py` exports `load_mode_mapping` but not the `ModeMapping` or `ModeFormMapping` models.
    - **Proposed change**: Add `ModeMapping` and `ModeFormMapping` to `__all__` in `__init__.py`.
    - **Rationale**: Downstream consumers who receive a `ModeMapping` instance from `load_mode_mapping()` cannot type-hint against it without importing from the submodule. This is an ergonomic gap.
    - **Risk if ignored**: Minor typing inconvenience; no functional impact.

---

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/012-game-form-schemas/spec.md` -- the specification under review
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/normal-form.yml` -- normal form schema file
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/gnep.yml` -- GNEP schema file
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/parametric.yml` -- parametric schema file
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/stackelberg.yml` -- Stackelberg schema file
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/mode-mapping.yml` -- mode-to-form mapping file
- `<HOME>/code/payer-index-mono/conversus/src/conversus_schemas/game_forms.py` -- Pydantic model implementation
- `<HOME>/code/payer-index-mono/conversus/src/conversus_schemas/__init__.py` -- package exports
- `<HOME>/code/payer-index-mono/conversus/tests/test_game_forms.py` -- test suite
- `<HOME>/code/payer-index-mono/conversus/pyproject.toml` -- package configuration
