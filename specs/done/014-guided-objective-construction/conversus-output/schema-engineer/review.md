# Schema Engineer Review — Spec 014: Guided Objective Construction

**Reviewer role**: Pydantic schema engineer
**Scope**: `construction.py` models, validation, type safety, protocol design
**Date**: 2026-03-24

---

## Executive Summary

The construction pipeline is structurally sound. The three-stage separation is clean, the `GapFiller` protocol is well-designed, and the Pydantic/dataclass split is appropriate (mutable output model vs. frozen intermediate state). However, **`AssembledObjective.source` does not match the FR-020 schema** — the spec requires a nested structure with `problem_md` path and per-parameter `filled_by`, while the implementation uses a flat `dict[str, str]`. Additionally, `fill_parameter_gaps` builds an internal `source` dict but discards it, forcing `construct_objective` to rebuild it from scratch — a fragile duplication. The `_substitute_symbolic_form` function has a substring-collision bug that will misfire on real templates. These are fixable without architectural changes.

---

## Alignment

### What the implementation gets right

1. **DecisionType enum + pattern registry (FR-001, FR-019)**: Clean separation of explicit-type-first with keyword-fallback. The normalization of hyphens/spaces to underscores before `DecisionType()` lookup is correct.

2. **GapFiller protocol (FR-022)**: `@runtime_checkable` is the right call — enables `isinstance` checks at test boundaries without requiring inheritance. The three implementations (Interactive, NonInteractive, and the test DictGapFiller) cover the protocol surface.

3. **FR-021 deferred handling**: Function-type parameters with `derived_from` are correctly identified in `identify_gaps` and given `<deferred: ...>` placeholders. The `_substitute_symbolic_form` correctly skips these.

4. **Frozen dataclasses for Stage 1 output**: `ParameterGap` and `GapList` are `frozen=True`, preventing accidental mutation between stages. Good defensive design.

5. **Template loading (FR-017)**: `load_objective_templates` follows the same `Path | None` default pattern as `load_mode_mapping` in `game_forms.py`. The `sorted()` glob ensures deterministic load order.

6. **FR-023 non-interactive behavior**: `NonInteractiveGapFiller` raises `RuntimeError` on `fill()`, and `fill_parameter_gaps` catches this for defaults. True gaps propagate the error correctly.

7. **Determinism (FR-012)**: No randomness anywhere. Template selection uses alphabetical sort. Symbolic form substitution sorts by key length descending.

---

## Missed Opportunities

### M1. `AssembledObjective.source` is structurally incomplete per FR-020

FR-020 specifies:

> `source` (dict with `problem_md` path and `filled_by` per parameter: `"explicit"`, `"default"`, or `"gap_filled"`)

The implementation uses `source: dict[str, str]` — a flat mapping of parameter name to provenance tag. This is missing:

- **`problem_md` path**: No field records which `problem.md` file was used as input. The spec requires this for traceability.
- **`filled_by` nesting**: The spec implies a structure like `{"problem_md": "path/to/problem.md", "filled_by": {"w": "default", "score": "deferred"}}`, not a flat dict where parameter provenance tags live at the same level as metadata.

The model validator checks that every parameter key exists in `source`, but there is no validation that `problem_md` is present.

### M2. `fill_parameter_gaps` builds and discards its source map

`fill_parameter_gaps` (line 542-585) constructs a `source: dict[str, str]` internally but only returns `filled` (the parameter values). The `construct_objective` orchestrator (lines 760-773) then rebuilds `source_map` from scratch using the same `gap_list` categories. This is fragile:

- If a user overrides a default during gap-filling, the override detection in `construct_objective` (line 766: `filled_params.get(name) != gap_list.defaults[name]`) uses value equality. For float parameters, this is brittle — `1.0` (default) vs `1.0` (user-typed) would be tagged `"default"` even though the user actively confirmed it.
- The internal `source` dict in `fill_parameter_gaps` has the correct provenance already. It should be returned alongside `filled`.

### M3. No `LLMGapFiller` implementation

FR-022 specifies both `InteractiveGapFiller` and `LLMGapFiller` as implementations. The `LLMGapFiller` that "accepts a model provider and generates contextual questions then maps answers" is absent. This is likely intentional (deferred to integration), but the spec lists it as a MUST-level requirement of Stage 2.

### M4. No FR-003 implementation (multi-candidate user selection)

FR-003 states: "When multiple templates are viable candidates, the parser MUST present them to the user with plain-language descriptions and ask for selection." The current `construct_objective` silently picks `candidates[0]`. There is no mechanism to present alternatives to the user.

---

## Off-Base Assumptions

### O1. `_substitute_symbolic_form` uses naive string replacement

The function (line 684-699) replaces parameter names with values using `str.replace()`. This causes substring collisions:

- Template form: `"J = -w * score + penalty * overlap"` with params `{"w": 2.0, "score": "...", "penalty": 3.0, ...}`
- Sorting by name length descending: `penalty` (7), `score` (5), `overlap` (7), `w` (1), `min_score` (9)
- Replacing `"w"` will match the `w` in `"score"` if score has already been replaced with a string not containing `w`, or the `w` in the literal `"winner"` if that appeared.
- Worse: the `w` in `overlap` would be replaced: `"o2.0erlap"` (corrupted).

The descending-length sort mitigates some cases (longer names first), but single-character parameter names like `w` will still corrupt any word containing `w`. The fix is to use word-boundary-aware replacement (`re.sub(r'\b{name}\b', ...)`) or a proper template syntax (`{w}`, `${w}`).

### O2. Catching `RuntimeError` as control flow for NonInteractiveGapFiller

In `fill_parameter_gaps` (line 558-564), the code uses a `try/except RuntimeError` around `filler.fill()` to detect non-interactive mode. This works but is semantically wrong — `RuntimeError` is a broad exception. A custom exception (`GapFillRefused` or similar) would prevent accidental swallowing of unrelated `RuntimeError`s from bugs in real filler implementations.

### O3. `_coerce_value` returns `None` for `"boolean"` type

`ParameterDefinition` accepts `type="boolean"` (from `VALID_PARAMETER_TYPES` in `objectives.py`), but `_coerce_value` has no branch for `"boolean"` — it falls through to `return None`. Any boolean parameter would fail coercion in gap-filling and extraction. The test suite does not cover boolean parameters.

---

## Actionable Recommendations

### P1: Fix `AssembledObjective.source` to match FR-020 structure

**Priority**: P1 (spec non-compliance)

Restructure `source` from `dict[str, str]` to a model:

```python
class SourceProvenance(BaseModel):
    problem_md: str | None = None
    filled_by: dict[str, str]

class AssembledObjective(BaseModel):
    ...
    source: SourceProvenance
```

Update `assemble_objective` and `construct_objective` to pass the `problem_md` path. Update the validator to check `filled_by` keys match `parameters` keys. Update all tests that construct `source` dicts.

### P1: Return source map from `fill_parameter_gaps`

**Priority**: P1 (data loss / fragile reconstruction)

Change the return type to `tuple[dict[str, Any], dict[str, str]]` or introduce a `FillResult` dataclass:

```python
@dataclass(frozen=True)
class FillResult:
    parameters: dict[str, Any]
    source_map: dict[str, str]
```

Remove the duplicate source-map reconstruction logic from `construct_objective`.

### P1: Fix `_substitute_symbolic_form` substring collision

**Priority**: P1 (correctness bug)

Replace `result.replace(name, str(value))` with word-boundary-aware substitution:

```python
result = re.sub(rf'\b{re.escape(name)}\b', str(value), result)
```

Add a test with the `competitive-selection` template's actual form (`"J = -w * score + penalty * overlap"`) to verify `w` does not corrupt `score` or `overlap`.

### P1: Add boolean coercion to `_coerce_value`

**Priority**: P1 (silent failure for valid parameter type)

Add a branch:

```python
elif param_type == "boolean":
    lower = value_str.strip().lower()
    if lower in ("true", "1", "yes"):
        return True
    elif lower in ("false", "0", "no"):
        return False
    return None
```

Add test coverage for boolean parameter extraction and gap-filling.

### P2: Introduce a custom exception for GapFiller refusal

**Priority**: P2 (robustness)

Define `GapFillRefused(Exception)` in the module. Have `NonInteractiveGapFiller` raise it instead of `RuntimeError`. Catch `GapFillRefused` specifically in `fill_parameter_gaps`. This prevents swallowing unrelated `RuntimeError`s from buggy filler implementations.

### P2: Implement FR-003 multi-candidate presentation

**Priority**: P2 (spec requirement, user experience)

When `len(candidates) > 1`, the pipeline should use the `GapFiller` (or a separate `TemplateSelector` protocol) to present candidates and let the user choose. Currently `candidates[0]` is silently used. At minimum, add a `template_selector` callback parameter to `construct_objective`.

### P2: Add `problem_md` path parameter to `construct_objective`

**Priority**: P2 (traceability, FR-020)

Add a `problem_md_path: str | None = None` parameter so the provenance chain is complete. When `output_path` is set, `problem_md_path` should default to `"problem.md"` (relative to the working directory) per the spec's expected workflow.

### P2: Validate `source` provenance tags are from a closed set

**Priority**: P2 (type safety)

The `AssembledObjective` validator checks that every parameter has a source entry, but does not validate that values are from `{"explicit", "default", "gap_filled", "deferred"}`. A `Literal` type or explicit check would catch typos:

```python
VALID_SOURCE_TAGS: frozenset[str] = frozenset({
    "explicit", "default", "gap_filled", "deferred",
})
```

### P3: Add `.yaml` extension support to `load_objective_templates`

**Priority**: P3 (robustness)

`load_objective_templates` only globs `*.yml`. If anyone adds a `.yaml` file, it will be silently ignored. `load_mode_mapping` in `game_forms.py` does not have this issue because it loads a single known file. Add `*.yaml` glob or document the `.yml`-only convention explicitly.

### P3: Test `_fill_single_gap` retry path with range guidance

**Priority**: P3 (coverage)

The retry logic in `_fill_single_gap` (lines 596-624) builds guidance messages for out-of-range values, but no test exercises the retry path where the first answer is invalid and a second valid answer is provided. The `SequentialGapFiller` test helper exists but is unused. Add a test using it.

---

## Referenced Documentation

| Document | Path | Relevance |
|---|---|---|
| Spec 014 | `conversus/specs/014-guided-objective-construction/spec.md` | Primary specification. FR-020 source structure, FR-022 GapFiller protocol, FR-003 multi-candidate, FR-021 deferred. |
| `construction.py` | `conversus/conversus/schemas/construction.py` | Implementation under review. |
| `test_construction.py` | `conversus/tests/test_construction.py` | Test suite. 831 lines, covers most paths. |
| `objectives.py` | `conversus/conversus/schemas/objectives.py` | `ObjectiveTemplate`, `ParameterDefinition`, `ConstraintTemplate` models. `VALID_MODES`, `VALID_PARAMETER_TYPES` constants. |
| `game_forms.py` | `conversus/conversus/schemas/game_forms.py` | `load_mode_mapping()` pattern used as reference for `load_objective_templates()`. `VALID_FIELD_TYPES` constant. |
| `competitive-selection.yml` | `conversus/schema/objective-functions/competitive-selection.yml` | Example template demonstrating the substring-collision risk in symbolic form substitution. |
