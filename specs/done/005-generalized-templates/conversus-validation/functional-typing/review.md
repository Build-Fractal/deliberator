# Validation Review: Spec 005 Implementation

**Reviewer**: functional-typing
**Date**: 2026-03-21
**Scope**: Verify all 5 P1 recommendations from the prior cooperative review were implemented correctly, follow Constitution Principle IX, and introduce no new issues.
**Test suite result**: 360/360 passed in 0.70s
**Linter result**: All 28 templates valid against schema.

---

## Executive Summary

The P1 implementations are correct and complete. All five P1 recommendations from the prior review have been faithfully implemented in a manner consistent with Constitution Principle IX (Functional Programming and Clean Code, including Explicit Typing). The code demonstrates disciplined separation of concerns: schema-loading functions are pure (raise exceptions, no side effects), the programmatic API uses typed Pydantic models throughout, and the `PathList` custom type bridges Pydantic's type system with conversus's newline-delimited template convention cleanly.

The implementation also absorbed the full P2 and P3 backlog items that were within scope. Mode schemas declare `mode_in_phases` and `templates` lists (P2-1). `get_valid_modes()` dynamically scans the schema directory (P2-2). `LintError` is a Pydantic model with `@field_validator` on `error_type` against `KNOWN_ERROR_TYPES` (P2-3, though not yet wired into `check_*` return types -- see Missed Opportunities). Schema versioning is present (P2-4). `frozen=True` is applied (P2-5). Extension points are documented in the spec (P2-6). `pyproject.toml` has the entry point (P2-8). Schema evolution regression tests are comprehensive (P2-9). `ConfigCondition` includes the `operator` field (P3-5). `P3-7` validation of mode schema template entries against phase names is implemented.

The 360-test suite is data-driven, covering positive validation of all 28 templates, negative detection of missing required variables, typo detection with fuzzy suggestions, structural marker enforcement, arbitration heading enforcement, dispute heading enforcement, mode-specific variable enforcement, and schema evolution scenarios. This is thorough and well-structured.

---

## Alignment

### P1-1: Purify schema-loading functions -- PASS

**Recommendation**: Replace `sys.exit(2)` and `click.echo()` in `load_variables_schema`, `load_mode_schema`, and `find_project_root` with `SchemaLoadError` exceptions. CLI `main()` is the sole site of `sys.exit()`.

**Implementation**: Correct. `validate.py` line 49-51 defines `SchemaLoadError(Exception)`. Lines 82-97 (`find_project_root`), 100-111 (`load_variables_schema`), and 114-125 (`load_mode_schema`) all raise `SchemaLoadError` on failure. All four `sys.exit()` calls (lines 393, 400, 410, 413) and all `click.echo()` calls (lines 392, 399, 403, 406, 408, 409, 412) are confined to the `main()` function (lines 387-417). The functions include docstrings with `Raises: SchemaLoadError` documentation.

**Principle IX compliance**: Yes. These are pure functions -- they take explicit inputs, return typed models, and signal failure via exceptions rather than side effects. No mutable global state, no I/O side effects.

### P1-2: Extract programmatic validation API -- PASS

**Recommendation**: Create `validate_all(config: ValidationConfig) -> ValidationResult` with typed Pydantic models. Fix bare imports. Click CLI becomes a thin wrapper.

**Implementation**: Correct. `validate.py` lines 58-76 define `ValidationConfig(BaseModel)` with `root: Path` and `mode: Optional[str] = None`, and `ValidationResult(BaseModel)` with `errors: list`, `files_checked: int`, and a `passed` property. The `validate_all()` function (lines 326-375) accepts `ValidationConfig` and returns `ValidationResult`. The `main()` function (lines 387-417) is a thin CLI wrapper that constructs a `ValidationConfig`, calls `validate_all()`, and formats output.

The `ValidationConfig` docstring (line 63) reads: "Downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields." This matches the recommendation exactly.

Bare imports are handled via try/except blocks (lines 24-37) supporting both relative (`from .models import ...`) and absolute (`from models import ...`) import paths, enabling both package and standalone usage.

**Principle IX compliance**: Yes. `validate_all` is a pure function -- given the same `ValidationConfig` input and filesystem state, it produces the same `ValidationResult`. The `ValidationConfig` model provides a single, typed configuration surface.

### P1-3: Define `PathList` custom type -- PASS

**Recommendation**: Pydantic custom type storing `list[Path]` internally with `BeforeValidator` for newline-separated string parsing and custom serializer. Exclude `ROUND_SYNTHESES`.

**Implementation**: Correct. `models.py` lines 23-35 define `_parse_path_list` (BeforeValidator) and `_serialize_path_list` (PlainSerializer), composed into `PathList` as an `Annotated` type. The type is applied to `AGENT_DOCS`, `CROSS_REVIEWS_OF_ME`, `MY_CROSS_REVIEWS`, `ALL_REVIEWS`, `ALL_CROSS_REVIEWS`, `ALL_REVISIONS`, `ALL_DISPUTES`, `ALL_REVISION_PATHS`, `ARBITRATION_PATHS`, and `TARGET_FILES` fields across all context models.

`ROUND_SYNTHESES` (line 324) is correctly typed as `str` with comment `# pre-formatted synthesis content per round`, not `PathList`. This matches the P3-6 correction and P1-3 exclusion.

**Principle IX compliance**: Yes. `_parse_path_list` and `_serialize_path_list` are pure functions. The `Annotated` type composition uses Pydantic's declarative validator/serializer pattern rather than imperative class methods.

### P1-4: Add `config_conditions` field with typed `ConfigCondition` model -- PASS

**Recommendation**: `ConfigCondition(BaseModel)` with `field: str` and `value: str`. `config_conditions: Optional[list[ConfigCondition]] = None` on `VariableDefinition`.

**Implementation**: Correct. `models.py` lines 67-78 define `ConfigCondition` with `field: str`, `operator: str = "=="`, and `value: str`. The `operator` field satisfies P3-5 (extend with additional condition types). `VariableDefinition` (line 93) includes `config_conditions: Optional[list[ConfigCondition]] = None`.

In `schema/variables.yml`, lines 94-96, 108-110, 120-122, 130-134, 143-146, 153-156, 164-167 apply `config_conditions` to the appropriate round-aware and arbitration-aware variables with conditions like `field: rounds, value: "> 1"` and `field: arbiter.timing, value: "inter-round"`.

**Principle IX compliance**: Yes. `ConfigCondition` is a clean Pydantic model with typed fields. The `operator` field defaults to `"=="` maintaining backward compatibility.

### P1-5: Add spec 006 variables to context models and schema -- PASS

**Recommendation**: `PRIOR_ARBITRATION_PATH: Optional[Path] = None` on phases 1-5 context models. `ARBITRATION_PATHS` (PathList) and `ARBITRATION_RULINGS: Optional[str] = None` on `CrossRoundSynthesisContext`. Corresponding entries in `schema/variables.yml`.

**Implementation**: Correct. In `models.py`:
- `PRIOR_ARBITRATION_PATH: Optional[Path] = None` appears in `ReviewContext` (line 221), `CrossReviewContext` (line 240), `RevisionContext` (line 261), `DisputesContext` (line 279), and `SynthesisContext` (line 298).
- `ARBITRATION_PATHS: Optional[PathList] = None` appears in `CrossRoundSynthesisContext` (line 326).
- `ARBITRATION_RULINGS: Optional[str] = None` appears in `CrossRoundSynthesisContext` (line 327).

In `schema/variables.yml`:
- `PRIOR_ARBITRATION_PATH` (lines 136-146) has `config_conditions: [{field: arbiter.timing, value: "inter-round"}]`.
- `ARBITRATION_PATHS` (lines 147-156) and `ARBITRATION_RULINGS` (lines 158-167) both have the same config condition and are scoped to `cross-round-synthesis`.

**Principle IX compliance**: Yes. All fields are explicitly typed with Optional wrappers for nullable values. No duck typing.

---

## Missed Opportunities

### MO-1: `check_*` functions still return `list[str]`, not `list[LintError]` (P2-3 incomplete)

The `LintError` model exists in `models.py` (lines 166-183) with full `@field_validator` on `error_type`, and it is well-constructed. However, the `check_*` functions in `validate.py` (lines 163-293) still return `list[str]`, not `list[LintError]`. The `validate_template` function (line 302) returns `list[str]`, and `validate_all` stores errors as `list[str]` in `ValidationResult.errors` (line 71 declares `errors: list` without type parameter).

This means `LintError` is currently unused infrastructure. The P2-3 recommendation stated: "All `check_*` functions return `list[LintError]`. CLI `main()` formats for human display."

The model is correct and ready to be wired in. This is not a defect -- it is an incomplete P2 item, not a P1 item. But since `ValidationResult.errors` is typed as bare `list` (line 71) rather than `list[LintError]`, the programmatic API's return type is weaker than it could be. The comment on line 71 acknowledges this: "Will be list[LintError] after models.py is updated."

**Severity**: Low. The `LintError` model is structurally correct and the wiring is straightforward. This is a known P2 follow-up, not a missed P1 requirement.

### MO-2: `AGENT_NAME` not in `variables.yml` cross-review phase list

In `schema/variables.yml` line 177, `AGENT_NAME` lists phases `[review, revision, disputes]` but not `cross-review`. This matches the spec's original design (cross-review uses `REVIEWER_NAME` and `REVIEWED_NAME` instead), so it is not an error. However, the spec data model section (Section 3, line 108) lists `AGENT_NAME` with phases `[review, cross-review, revision, disputes]`, which disagrees with the implementation.

The implementation is correct -- cross-review templates use `REVIEWER_NAME`/`REVIEWED_NAME`, not `AGENT_NAME`. The spec's Section 3 data model example has a minor inaccuracy. This is cosmetic and does not affect behavior.

**Severity**: Negligible. The spec example is illustrative, not normative. The schema is the source of truth per the spec's own design.

---

## Off-Base Assumptions

None identified. The implementation faithfully follows the prior review's convergence record without over-interpreting or under-interpreting any recommendation.

---

## Actionable Recommendations

### AR-1: Wire `LintError` into `check_*` return types (P2-3 completion)

**Priority**: P2 (same as original)
**Files**: `linter/validate.py` (check_* functions), `linter/models.py` (no changes needed)
**Action**: Convert each `check_*` function to return `list[LintError]` instead of `list[str]`. Update `ValidationResult.errors` type annotation from `list` to `list[LintError]`. Update `main()` to format `LintError` instances for human display (e.g., `f"{err.file_path}: {err.message}"`).
**Rationale**: The model exists and is correct. Wiring it in completes the programmatic API contract. The current bare `list` type annotation on `ValidationResult.errors` weakens the API surface for downstream consumers (spec 007/008).

### AR-2: Tighten `ValidationResult.errors` type annotation

**Priority**: P3
**Files**: `linter/validate.py` line 71
**Action**: Change `errors: list` to `errors: list[str]` (if AR-1 is deferred) or `errors: list[LintError]` (if AR-1 is completed). The current bare `list` violates Principle IX's explicit typing mandate: "ALL function signatures MUST have explicit type annotations."
**Rationale**: While `list` is technically a valid type annotation, it is unparameterized and provides no type information about the element type. This is the only Principle IX violation I identified in the entire implementation.

---

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/.specify/memory/constitution.md` -- Principle IX (Functional Programming and Clean Code, Explicit Typing)
- `<HOME>/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/summary/final.md` -- Prior review convergence record (P1-1 through P1-5, P2-1 through P2-9, P3-1 through P3-8)
- `<HOME>/code/payer-index-mono/conversus/linter/models.py` -- Pydantic models (lines 1-347)
- `<HOME>/code/payer-index-mono/conversus/linter/validate.py` -- Linter implementation (lines 1-417)
- `<HOME>/code/payer-index-mono/conversus/linter/test_validate.py` -- Test suite (360 tests, lines 1-586)
- `<HOME>/code/payer-index-mono/conversus/schema/variables.yml` -- Variable schema (lines 1-468)
- `<HOME>/code/payer-index-mono/conversus/schema/modes/cooperative.yml` -- Mode schema (lines 1-50)
- `<HOME>/code/payer-index-mono/conversus/schema/modes/red-blue.yml` -- Mode schema (lines 1-49)
- `<HOME>/code/payer-index-mono/conversus/schema/modes/winner-take-all.yml` -- Mode schema (lines 1-47)
- `<HOME>/code/payer-index-mono/conversus/schema/modes/prisoners-dilemma.yml` -- Mode schema (lines 1-44)
- `<HOME>/code/payer-index-mono/conversus/pyproject.toml` -- Package config (lines 1-18)
- `<HOME>/code/payer-index-mono/conversus/specs/005-generalized-templates/spec.md` -- Spec with Section 8 extension points (lines 399-421)
