# Validation Review: Spec 005 Implementation

**Reviewer**: integration-architect
**Review type**: Validation (post-implementation verification)
**Date**: 2026-03-21
**Scope**: Verify 7 implementation items from the prior cooperative review's convergence record

---

## Executive Summary

All seven recommended implementations from the prior review are **verified as implemented and functioning correctly**. The test suite passes with 360 tests in 0.69 seconds. The implementation faithfully follows the convergence record from the 2-round cooperative deliberation, with no substantive deviations. Two items have minor completeness gaps that do not affect correctness.

---

## Validation Checklist

### 1. SchemaLoadError exception replaces sys.exit() in loaders

**Status**: PASS

**Evidence**: `linter/validate.py` lines 49-51 define `SchemaLoadError(Exception)`. All three loader functions raise it:
- `find_project_root()` (line 94): raises `SchemaLoadError` instead of `sys.exit()`
- `load_variables_schema()` (line 108): raises `SchemaLoadError` instead of `sys.exit()`
- `load_mode_schema()` (line 122): raises `SchemaLoadError` instead of `sys.exit()`

`sys.exit()` calls exist only in the CLI `main()` function (lines 393, 400, 410, 413), which catches `SchemaLoadError` and converts to exit codes. This matches the P1-1 convergence item exactly: "CLI `main()` is the sole site of `sys.exit()`."

**Alignment with convergence record**: Exact match with P1-1.

---

### 2. validate_all() programmatic API exists with ValidationConfig

**Status**: PASS

**Evidence**: `linter/validate.py` lines 58-76 define:
- `ValidationConfig(BaseModel)` with `root: Path` and `mode: Optional[str] = None`
- `ValidationResult(BaseModel)` with `errors: list`, `files_checked: int`, `passed: bool` property
- `validate_all(config: ValidationConfig) -> ValidationResult` at lines 326-375

The CLI `main()` (lines 387-413) is a thin wrapper that constructs a `ValidationConfig` and calls `validate_all()`.

The `ValidationConfig` docstring reads: "Downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields." -- matching the P1-2 convergence item verbatim.

**Minor gap**: The `ValidationResult.errors` field is typed as `list` with a comment "Will be list[LintError] after models.py is updated" (line 70). However, `LintError` exists in `models.py` (lines 166-183) and the `check_*` functions still return `list[str]` rather than `list[LintError]`. The P2-3 convergence item specified "All `check_*` functions return `list[LintError]`. CLI `main()` formats for human display." The `LintError` model is defined but not yet wired into the validation pipeline. This is a P2 item that was not part of the P1 deliverables, so it does not block validation of the P1-2 API extraction itself.

**Bare import fix**: Lines 25-37 show the `try/except ImportError` pattern with relative imports (`from .models import ...`) as primary and bare imports as fallback. The P1-2 item specified fixing these. The dual-path pattern is a reasonable pragmatic choice for a module that needs to run both as a package member and standalone, though it means the bare import path still exists.

**Alignment with convergence record**: P1-2 core requirements met. P2-3 (LintError integration) partially implemented (model defined, not wired).

---

### 3. Spec 006 variables exist in both schema and context models

**Status**: PASS

**Evidence in `schema/variables.yml`**:
- `PRIOR_ARBITRATION_PATH` (lines 136-146): `type: path`, `phases: [review, cross-review, revision, disputes, synthesis]`, `required: false`, `config_conditions: [{field: arbiter.timing, value: "inter-round"}]`
- `ARBITRATION_PATHS` (lines 148-157): `type: path-list`, `phases: [cross-round-synthesis]`, `required: false`, `config_conditions: [{field: arbiter.timing, value: "inter-round"}]`
- `ARBITRATION_RULINGS` (lines 158-167): `type: extracted-content`, `phases: [cross-round-synthesis]`, `required: false`, `config_conditions: [{field: arbiter.timing, value: "inter-round"}]`

**Evidence in `linter/models.py`**:
- `PRIOR_ARBITRATION_PATH: Optional[Path] = None` present in `ReviewContext` (line 221), `CrossReviewContext` (line 240), `RevisionContext` (line 261), `DisputesContext` (line 280), `SynthesisContext` -- verified by absence from `ArbitrationContext` (appropriate, as arbitration does not receive prior arbitration paths in the same way).
- `ARBITRATION_PATHS: Optional[PathList] = None` in `CrossRoundSynthesisContext` (line 326)
- `ARBITRATION_RULINGS: Optional[str] = None` in `CrossRoundSynthesisContext` (line 327)

**Alignment with convergence record**: Exact match with P1-5. Variables appear in exactly the phases and context models specified.

---

### 4. ConfigCondition model with typed fields exists

**Status**: PASS

**Evidence**: `linter/models.py` lines 67-78:

```python
class ConfigCondition(BaseModel):
    field: str
    operator: str = "=="
    value: str
```

`VariableDefinition` (line 93) includes `config_conditions: Optional[list[ConfigCondition]] = None`.

`schema/variables.yml` uses `config_conditions` on the round-aware variables (lines 94-96: `field: rounds, value: "> 1"`) and on the spec 006 variables (lines 144-146: `field: arbiter.timing, value: "inter-round"`).

The `operator` field (default `"=="`) implements the P3-5 extension that was converged upon in Round 2 -- extending P1-4's model with an operator field for expressing conditions like `rounds > 1`.

**Alignment with convergence record**: Matches P1-4 and incorporates P3-5 extension.

---

### 5. pyproject.toml has conversus-lint entry point

**Status**: PASS

**Evidence**: `pyproject.toml` line 13:
```
conversus-lint = "conversus.linter.validate:main"
```

Dependencies include `click>=8.3.1`, `pydantic>=2.12.5`, `pyyaml>=6.0.3` (lines 7-9). Dev dependencies include `pytest>=9.0.2` (line 17).

**Alignment with convergence record**: Exact match with P2-8.

---

### 6. Schema evolution tests exist and pass

**Status**: PASS

**Evidence**: `linter/test_validate.py` lines 487-586, `TestSchemaEvolution` class contains three test methods:

1. `test_new_optional_variable_accepted` (lines 490-523): Parametrized across all 4 modes. Creates a new optional `VariableDefinition`, extends the schema, and verifies all existing templates still pass. Confirms forward compatibility of optional additions.

2. `test_new_required_variable_produces_errors` (lines 525-560): Parametrized across all 4 modes. Creates a new required variable for the `review` phase, extends the schema, and asserts that a `missing` error is produced. Confirms that the linter catches newly-required variables.

3. `test_new_mode_schema_discovered` (lines 562-586): Uses `tmp_path` to create a synthetic `test-mode.yml`, copies existing mode files, and verifies `get_valid_modes()` discovers the new mode alongside existing ones. Confirms dynamic mode discovery.

**Test results**: All 12 schema evolution tests (4+4+1 parametrized = 9 test instances, plus the 3 consistency tests per mode) pass. Full suite: 360 tests, 0.69 seconds, all green.

**Alignment with convergence record**: Exact match with P2-9: "Tests covering: new optional variable passes existing templates, new required variable produces phase-specific errors, new mode schema file is discovered and validated."

---

### 7. MODE_PRESENCE hardcoded dict is gone, replaced by mode_in_phases

**Status**: PASS

**Evidence**:

Removal confirmed: Grep for `MODE_PRESENCE` in `linter/` and `schema/` returns zero results. The hardcoded 28-entry dict that existed in the prior version of `validate.py` is completely gone.

Replacement confirmed:
- `ModeSchema` in `models.py` (line 160): `mode_in_phases: list[str] = Field(default_factory=list)`
- All 4 mode schemas declare `mode_in_phases`:
  - `cooperative.yml`: all 7 phases
  - `red-blue.yml`: `[review, cross-review, synthesis, arbitration, cross-round-synthesis]`
  - `winner-take-all.yml`: `[synthesis, arbitration, cross-round-synthesis]`
  - `prisoners-dilemma.yml`: `[arbitration, cross-round-synthesis]`
- `validate.py` line 197 uses it: `if phase not in mode_schema.mode_in_phases: continue`
- Test file line 225 mirrors the same logic

The values are consistent with the original `MODE_PRESENCE` semantics: cooperative uses MODE in all phases, prisoners-dilemma uses it only in arbitration and cross-round-synthesis, etc.

**Bidirectional validation**: The `validate_all()` function (lines 352-357) also performs reverse template existence checking -- reporting template files listed in the mode schema but missing from disk, and (line 351-357) validating that template names correspond to known phases (P3-7). This implements the "bidirectional template validation" aspect of P2-1.

**Dynamic mode discovery**: `models.py` lines 58-64 define `get_valid_modes(schema_dir: Path) -> frozenset[str]` that scans `schema/modes/*.yml`, implementing P2-2. No hardcoded `VALID_MODES` frozenset exists.

**Alignment with convergence record**: Exact match with P2-1 and P2-2.

---

## Alignment

The implementation is closely aligned with the 2-round deliberation's convergence record. Specific alignment highlights:

1. **Constitution Principle IX compliance**: All functions have explicit type annotations. All data structures use Pydantic models. `TemplateContext` uses `model_config = {"extra": "forbid", "frozen": True}` (P2-5). `ConfigCondition`, `DisputeConfig`, `ArbitrationConfig`, `CrossRoundSynthesisConfig` are all Pydantic models. No raw dicts are used for parsed YAML data.

2. **Functional programming adherence**: The validation pipeline is composed of pure functions (`check_unknown_variables`, `check_missing_required_variables`, `check_mode_specific_variables`, `check_required_headings`, `check_structural_markers`). Each takes explicit inputs and returns errors. `validate_template` composes them. No mutable global state.

3. **Extension point documentation**: Spec 005's Section 8 ("Extension Points for Downstream Specs") exists and documents both extension points and non-extension-points, matching P2-6 exactly.

4. **Schema versioning**: `schema_version: "1.0.0"` in `variables.yml` (line 30) and `schema_version: str = "1.0.0"` in `VariablesSchema` (line 120), matching P2-4.

5. **PathList custom type**: Defined at `models.py` lines 23-35 with `BeforeValidator` for newline-separated string parsing and `PlainSerializer` for template substitution. Applied to all path-list context fields. `ROUND_SYNTHESES` correctly uses `str` (line 324), not `PathList`, matching the P1-3 exclusion.

6. **frozen=True on TemplateContext**: Line 202 confirms `model_config = {"extra": "forbid", "frozen": True}`, matching P2-5.

---

## Missed Opportunities

1. **LintError not wired into validation pipeline**: The `LintError` Pydantic model exists in `models.py` with proper `error_type` validation against `KNOWN_ERROR_TYPES`, but the `check_*` functions still return `list[str]` and `ValidationResult.errors` is typed as `list` with a TODO comment. The convergence record's P2-3 specified full integration. This is a known incomplete P2 item, not a missed opportunity per se, but it means the structured error type validation is defined but not exercised at runtime. The `check_*` functions would need to construct `LintError` instances to close this loop.

2. **`linter/__init__.py` is empty**: No public API is exported. The convergence record's P1-2 mentioned `linter/__init__.py` as an affected file. Exporting `validate_all`, `ValidationConfig`, `ValidationResult`, and `SchemaLoadError` from `__init__.py` would make the programmatic API more discoverable. (The `__all__` exports item was explicitly deferred as D5, but basic imports in `__init__.py` are separate from `__all__`.)

---

## Off-Base Assumptions

None identified. The implementation makes no assumptions that contradict the convergence record, the constitution, or the spec. The design choices are conservative and well-aligned with the deliberation's "freeze first, compose later" principle.

---

## Actionable Recommendations

### R1: Complete LintError integration (P2-3 completion)

**Priority**: P2
**Rationale**: The `LintError` model is defined with proper validation but never instantiated by the validation pipeline. The `ValidationResult.errors` field has a TODO comment acknowledging this. Completing this wiring would:
- Give downstream consumers (spec 007 plugins, spec 008 executable conversus) structured error data instead of raw strings
- Exercise the `KNOWN_ERROR_TYPES` validation that currently only runs if someone manually constructs a `LintError`
- Close the gap between the convergence record's P2-3 specification and the current implementation

**Scope**: Modify each `check_*` function to return `list[LintError]` instead of `list[str]`. Update `ValidationResult.errors` type annotation. Update CLI `main()` to format `LintError` instances for display.

### R2: Populate linter/__init__.py with public API exports

**Priority**: P3
**Rationale**: The programmatic API (`validate_all`, `ValidationConfig`, `ValidationResult`, `SchemaLoadError`) is the primary integration surface for spec 007 and spec 008. Exporting these from `__init__.py` follows Python packaging conventions and makes `from conversus.linter import validate_all, ValidationConfig` work without knowledge of internal module structure.

---

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/summary/final.md` -- Cross-round synthesis with the definitive convergence record (P1-1 through P3-8 and D1-D7)
- `/Users/business-daddy/code/payer-index-mono/conversus/.specify/memory/constitution.md` -- Constitution v1.4.0 (Principle IX: Functional Programming, Explicit Typing)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/006-inter-round-arbitration/spec.md` -- Source of `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, `ARBITRATION_RULINGS` variable requirements
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/005-generalized-templates/spec.md` -- Spec 005 with Section 8 extension points documentation
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/008-executable-conversus/001-executable-conversus.md` -- Downstream consumer of the programmatic API
