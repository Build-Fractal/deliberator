# Spec Compliance Review: 014 Guided Objective Construction

**Reviewer**: spec-compliance
**Date**: 2026-03-24
**Spec**: `specs/014-guided-objective-construction/spec.md`
**Implementation**: `conversus/schemas/construction.py`
**Tests**: `tests/test_construction.py`

---

## Executive Summary

The implementation covers the structural backbone of the 3-stage pipeline faithfully. All five success criteria have test coverage, the deterministic stages (1 and 3) contain no LLM calls, and the `GapFiller` protocol cleanly separates interactive from non-interactive use. However, several functional requirements are only partially met or not met at all. The most significant gaps are: FR-003 (no multi-template presentation/user-selection logic), FR-009 (no `gap_fill_model` configuration surface), FR-014 (no `conversus.yml` integration), FR-020 (the `source` dict is missing the `problem_md` path and the `filled_by` sub-dict structure), and FR-022 (no `LLMGapFiller` implementation). FR-015 and FR-013 are structurally satisfied by the package boundary but lack any explicit test proving the claim. Overall, the implementation is a solid Stage-1-through-3 engine that needs a handful of targeted additions to reach full spec compliance.

---

## Alignment

### FR-001 -- Decision type from keyword/pattern matching (no LLM) -- **MET**
- `classify_decision_type()` at line 264 uses compiled regex patterns in `_DECISION_TYPE_PATTERNS` (lines 67-89). No LLM call.
- Tests: `TestClassifyDecisionType` covers all four types plus edge cases (lines 122-170).

### FR-002 -- Select top 1-3 candidate templates -- **MET**
- `select_candidate_templates()` at line 311 accepts `max_candidates` (default 3) and returns mode-specific before general.
- Tests: `TestSelectCandidateTemplates` validates count range and ordering (lines 236-288).

### FR-003 -- Present multiple viable templates to user for selection -- **NOT MET**
- `construct_objective()` (line 706) silently takes `candidates[0]` (line 751) with no user-facing presentation or selection prompt.
- No function, protocol method, or test addresses template-choice interaction.

### FR-004 -- Extract explicit parameter values from problem text -- **MET**
- `extract_explicit_parameters()` at line 378 uses `_NUMBER_PATTERN` and `_BUDGET_PATTERN`.
- Tests: `TestExtractExplicitParameters` covers numeric, equals, dollar-sign, out-of-range, and no-match cases (lines 296-379).

### FR-005 -- Generate plain-language contextualised question per gap -- **PARTIALLY MET**
- `fill_parameter_gaps()` (line 515) passes `gap.gap_question` and `problem_context` to the filler. For defaults, it constructs a question (line 553). However, the question for true gaps is the template's `gap_question` verbatim -- there is no contextualisation logic that rewrites the question using problem-specific details as the spec envisions ("You mentioned Redis is faster...").
- No test verifies that questions are contextualised beyond the raw `gap_question`.

### FR-006 -- Map answers to typed parameter values respecting type and range -- **MET**
- `_coerce_value()` (line 423) and `_value_in_range()` (line 438) enforce type coercion and range checks.
- Tests: `test_fills_true_gaps`, `test_integer_coercion`, `test_ignores_out_of_range_values`.

### FR-007 -- Re-ask with guidance on invalid answers -- **MET**
- `_fill_single_gap()` (line 588) retries up to `max_retries` times and builds guidance messages (lines 605-616).
- **No test** exercises the retry path (see Missed Opportunities), but the implementation is present.

### FR-008 -- Present defaults and ask whether to accept or adjust -- **MET**
- `fill_parameter_gaps()` lines 551-577 construct a question for each default and accept empty-string as "keep default".
- Tests: `test_accepts_defaults_with_empty_answer`, `test_overrides_default_with_answer`, `test_non_interactive_filler_uses_defaults`.

### FR-009 -- `gap_fill_model` configurable in config -- **NOT MET**
- No configuration key, config file reader, or parameter for `gap_fill_model` exists anywhere in the codebase. The `GapFiller` protocol is pluggable, but the spec requires a named config field.

### FR-010 -- Assembled `objective.yml` validates against `AssembledObjective` Pydantic model -- **MET**
- `assemble_objective()` returns `AssembledObjective` which runs a `model_validator` (lines 181-196).
- Tests: `TestAssembleObjective`, `TestSC003ValidObjectiveYml`.

### FR-011 -- Output includes template name, game form, mode, all parameters, constraints, symbolic form -- **MET**
- `AssembledObjective` model (line 166) has all required fields.

### FR-012 -- Deterministic assembly: same inputs = same output -- **MET**
- `_substitute_symbolic_form()` sorts by key length descending (line 694) for deterministic substitution. No randomness.
- `select_candidate_templates()` sorts by name (lines 345-346).
- Test: `TestSC004Determinism.test_same_inputs_same_output`.

### FR-013 -- Opt-in integration with `/conversus mode` -- **PARTIALLY MET**
- The construction pipeline exists as a standalone function (`construct_objective`), which could be called by `/conversus mode`. However, no integration code or opt-in prompt has been implemented. The spec says "MAY offer to run", so the pipeline being available is sufficient structurally, but no integration point or test exists.

### FR-014 -- `objective.yml` referenced in `conversus.yml` under `objective` field -- **NOT MET**
- No code writes or modifies `conversus.yml`. `construct_objective()` writes `objective.yml` to an arbitrary `output_path` but does not touch `conversus.yml`.

### FR-015 -- No import errors when `conversus-schemas` is not installed -- **MET (by design)**
- The construction module lives inside `conversus.schemas` and only imports `pydantic`, `yaml`, and sibling modules. No external game-engine or solver dependencies.
- However, **no test** explicitly proves this claim by testing the import path in isolation (contrast with `test_game_forms.py` lines 187-208 which has an explicit importability test). SC-005 comment in the test file (line 8) says "Tested indirectly" which is insufficient.

### FR-016 -- Pipeline ships in `conversus-schemas`, no extra dependencies beyond pydantic/pyyaml -- **MET**
- The module imports only `re`, `dataclasses`, `enum`, `pathlib`, `typing` (stdlib), `yaml`, and `pydantic`.

### FR-017 -- `load_objective_templates(templates_dir)` discovers YAML files in `schema/objective-functions/` -- **MET**
- `load_objective_templates()` at line 212 globs `*.yml` and validates each via `ObjectiveTemplate.model_validate`.
- Tests: `TestLoadObjectiveTemplates` (lines 180-213).

### FR-018 -- Decision type to mode mapping is explicit and deterministic -- **MET**
- `_DECISION_TYPE_MODE` dict (lines 92-97) maps each `DecisionType` to a specific mode string, matching the spec's table exactly.
- General templates handled via `GENERAL_TEMPLATE_NAMES` (line 40).

### FR-019 -- Decision type from `problem.md` Type field first, keyword fallback -- **MET**
- `classify_decision_type()` checks `explicit_type` first (line 282), falls back to patterns.
- Tests: `test_explicit_type_overrides_keywords`, `test_invalid_explicit_type_falls_back_to_keywords`.

### FR-020 -- `AssembledObjective` Pydantic model with required fields -- **PARTIALLY MET**
- Fields present: `template_name`, `game_form`, `mode`, `parameters`, `constraints`, `symbolic_form`, `source`.
- **Missing from `source` dict**: The spec requires `source` to contain `problem_md` path (the path to the problem.md file) alongside per-parameter `filled_by` entries. The implementation's `source` is a flat `dict[str, str]` mapping parameter names to provenance tags. It contains no `problem_md` key.

### FR-021 -- Function-type parameters recorded as deferred with `derived_from` placeholder -- **MET**
- `identify_gaps()` line 483 catches `type == "function"` params and stores `derived_from` value.
- `fill_parameter_gaps()` line 547 sets `filled[name] = "<deferred: {derived_from}>"` and `source[name] = "deferred"`.
- Tests: `test_function_params_are_deferred`, `test_deferred_params_have_placeholder`.

### FR-022 -- `GapFiller` protocol with `InteractiveGapFiller` and `LLMGapFiller` -- **PARTIALLY MET**
- `GapFiller` protocol (line 104) with `fill(question, context) -> str` is correct.
- `InteractiveGapFiller` (line 117) exists.
- **`LLMGapFiller` is not implemented.** The spec explicitly names it as a required implementation.

### FR-023 -- Non-interactive mode reports errors for parameters without defaults -- **MET**
- `NonInteractiveGapFiller.fill()` raises `RuntimeError` (line 132).
- For defaults, `fill_parameter_gaps()` catches the `RuntimeError` and uses the default (lines 558-563).
- For true gaps, the `RuntimeError` propagates up.
- Tests: `test_non_interactive_filler_raises_on_gap`, `test_non_interactive_filler_uses_defaults`.

### SC-001 -- SELECTION problem -> competitive-selection template -- **MET**
- Test: `TestSC001EndToEnd.test_selection_problem_gets_competitive_selection` (line 651).
- Also `test_sc001_selection_gets_competitive_selection` (line 275).

### SC-002 -- Stage 2 maps "speed is twice as important" to weight values -- **NOT MET**
- No test or code demonstrates natural-language-to-relative-weight mapping. The `DictGapFiller` in tests returns pre-mapped numeric strings. The spec's example of converting "speed is twice as important as cost" into `speed_weight=2.0, cost_weight=1.0` requires either LLM-based interpretation or a dedicated mapping function, neither of which exists.

### SC-003 -- Stage 3 produces valid `objective.yml` -- **MET**
- Test: `TestSC003ValidObjectiveYml` (lines 572-615).

### SC-004 -- Determinism -- **MET**
- Test: `TestSC004Determinism.test_same_inputs_same_output` (lines 622-644).

### SC-005 -- `/conversus mode` without schemas works identically -- **PARTIALLY MET**
- Structurally true (separate package), but no test proves this. The test file acknowledges "Tested indirectly" (line 8).

---

## Missed Opportunities

1. **No retry/re-ask test (FR-007)**: `_fill_single_gap` has retry logic (lines 596-624) but no test exercises it. A `SequentialGapFiller` helper already exists (line 73) and could feed an invalid answer followed by a valid one.

2. **No natural-language mapping test (SC-002)**: The spec's headline scenario -- "speed is twice as important" mapped to relative weights -- has no test or implementation path. This is the single most visible success criterion gap.

3. **No `conversus.yml` integration (FR-014)**: Writing `objective.yml` is implemented, but the pipeline never updates `conversus.yml` to point at it. This breaks the downstream plugin consumption chain.

4. **No explicit importability test (FR-015 / SC-005)**: `test_game_forms.py` has a proper importability test for its module. `test_construction.py` does not replicate this pattern for its own module.

5. **`source` dict lacks `problem_md` path (FR-020)**: The `source` field only maps parameter names to provenance tags. The spec explicitly requires a `problem_md` path field to record which problem file was used as input.

---

## Off-Base Assumptions

1. **First-candidate auto-selection is sufficient (FR-003)**: The orchestrator at line 751 (`template = candidates[0]`) assumes the top-ranked template is always correct. The spec requires presenting multiple candidates with descriptions and asking the user to pick. This is not a "nice-to-have" -- FR-003 uses "MUST present".

2. **`source` as flat parameter-to-tag dict satisfies FR-020**: The implementation treats `source` as `{param_name: provenance_tag}`. The spec defines `source` as containing both `problem_md` (a path) and per-parameter `filled_by` entries. These are structurally different.

3. **`gap_fill_model` is covered by GapFiller pluggability**: The protocol-based GapFiller is a good pattern, but FR-009 specifically requires a named configuration key (`gap_fill_model`) in config. The pluggable protocol and the config surface are complementary, not substitutes.

---

## Actionable Recommendations

### P1 (Spec violations that block compliance)

**R1. Implement multi-template user selection (FR-003).**
Add a method to the `GapFiller` protocol (or a separate `TemplateSelector` protocol) that presents candidate template descriptions and returns the user's choice. Update `construct_objective()` to call it when `len(candidates) > 1` instead of silently picking `candidates[0]`. The `NonInteractiveGapFiller` variant should pick the first candidate automatically.
- Files: `conversus/schemas/construction.py` lines 749-751.

**R2. Add `problem_md` path to `AssembledObjective.source` (FR-020).**
Change the `source` field from `dict[str, str]` to a structured model (or at minimum a dict) containing `problem_md: str` (path) plus `filled_by: dict[str, str]` (the current per-parameter provenance map). Update `construct_objective()` to accept and forward the problem path. Update all tests that construct `source` dicts.
- Files: `conversus/schemas/construction.py` line 179, lines 761-773.

**R3. Implement `conversus.yml` objective field (FR-014).**
After writing `objective.yml`, read the existing `conversus.yml` (or create one), add/update an `objective` key pointing to the relative path of `objective.yml`, and write it back. This is a small addition to `construct_objective()` gated on `output_path is not None`.
- Files: `conversus/schemas/construction.py` lines 784-788.

**R4. Implement `LLMGapFiller` (FR-022).**
The spec requires an `LLMGapFiller` implementation that accepts a model provider, generates contextual questions, and maps answers. Even if the actual LLM call is deferred to a runtime dependency, the class with its constructor signature (`model_provider` parameter) and question-contextualisation logic must exist. This also partially addresses FR-005 (contextualised questions).
- Files: new class in `conversus/schemas/construction.py` after `NonInteractiveGapFiller`.

**R5. Add `gap_fill_model` config surface (FR-009).**
Add a `gap_fill_model` parameter to `construct_objective()` (and document it as a `conversus.yml` config key). When provided, it should be used to instantiate the `LLMGapFiller`. When absent, default to the cheapest capable model (or `NonInteractiveGapFiller` if no model is available).
- Files: `conversus/schemas/construction.py` line 706.

### P2 (Test gaps and partial compliance)

**R6. Add retry/re-ask test (FR-007).**
Use `SequentialGapFiller` with `["invalid", "999", "5.0"]` for a param with range 0-10. Assert that the third answer is accepted and the filler was called three times.
- Files: `tests/test_construction.py`, new test in `TestFillParameterGaps`.

**R7. Add SC-002 natural-language mapping test.**
Create a test that exercises the full pipeline with a filler that returns "speed is twice as important as cost" and verifies the resulting weight ratio. This will likely require the `LLMGapFiller` or a dedicated answer-interpretation function.
- Files: `tests/test_construction.py`, new test class.

**R8. Add explicit importability test (FR-015 / SC-005).**
Mirror the pattern from `test_game_forms.py` lines 187-208: attempt to import `conversus.schemas.construction` with `conversus.schemas.objectives` already loaded, verify no `ImportError`. This makes the SC-005 claim testable rather than implicit.
- Files: `tests/test_construction.py`, new test class.

### P3 (Robustness and completeness)

**R9. Add question contextualisation to `fill_parameter_gaps` (FR-005).**
When `GapFiller` is asked a question, prepend or weave in problem-specific context beyond just passing `problem_context` as a separate argument. The filler should receive a question that references the specific problem (e.g., "You mentioned Redis vs Postgres. How important is speed on a scale of 0-10?"). This may be partially solved by `LLMGapFiller` (R4), but the non-LLM path should also improve.
- Files: `conversus/schemas/construction.py` lines 580-583.

**R10. Harden determinism test to cover YAML round-trip (SC-004).**
The current determinism test (`test_same_inputs_same_output`) compares `model_dump()` dicts. Add a variant that writes both runs to `objective.yml` via `construct_objective(output_path=...)` and asserts byte-identical YAML files. This catches any non-determinism in YAML serialisation (key ordering, float formatting).
- Files: `tests/test_construction.py`, extend `TestSC004Determinism`.

---

## Referenced Documentation

| Document | Path |
|---|---|
| Spec 014 | `specs/014-guided-objective-construction/spec.md` |
| Construction pipeline | `conversus/schemas/construction.py` |
| Objectives models (spec 013) | `conversus/schemas/objectives.py` |
| Test suite | `tests/test_construction.py` |
| Package exports | `conversus/schemas/__init__.py` |
