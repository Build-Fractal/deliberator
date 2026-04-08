# Game-Theorist Review: Guided Objective Function Construction (Spec 014)

**Reviewer**: game-theorist (game theory mathematician)
**Scope**: Does the construction pipeline correctly bridge natural-language problem descriptions to parameterized objective functions?
**Date**: 2026-03-24

---

## Executive Summary

The three-stage construction pipeline in `construction.py` is architecturally sound. The separation of deterministic stages (1 and 3) from the interactive stage (2) is well-motivated and correctly enforced -- no LLM imports leak into Stages 1 or 3. Decision type classification maps correctly to template `mode_compatibility` entries. Template selection, parameter extraction, gap identification, and assembly each do their job. The `GapFiller` protocol is clean and extensible.

However, there are several mathematical and structural issues that could produce incorrect objective functions in non-trivial cases. The most serious: `fill_parameter_gaps` builds an internal `source` map but discards it (returns only `filled`), forcing `construct_objective` to reconstruct the source map by comparing filled values against defaults -- a comparison that can silently misclassify a user who deliberately confirms the default as `"default"` instead of `"gap_filled"`. Additionally, the symbolic form substitution uses naive string replacement that will produce incorrect results when parameter names are substrings of each other or of mathematical symbols. These are not theoretical concerns; they are triggered by the existing template library.

---

## Alignment

### (1) Decision Type Classification -> Template mode_compatibility

**Verdict: Correct.**

The mapping in `_DECISION_TYPE_MODE` is:
- `SELECTION` -> `winner-take-all`
- `INTEGRATION` -> `cooperative`
- `SCOPING` -> `prisoners-dilemma`
- `STRESS_TEST` -> `red-blue`

This matches FR-018 exactly. `select_candidate_templates` filters templates by checking `target_mode in template.mode_compatibility`, which correctly handles both mode-specific templates (e.g., `competitive-selection` with `mode_compatibility: [winner-take-all]`) and general templates (e.g., `weighted-sum` with all four modes). The priority ordering (mode-specific first, general second) is also correct for the intended ranking behavior.

The keyword patterns for fallback classification are comprehensive and well-constructed. The tie-breaking rule (highest match count, then enum definition order) is deterministic but could produce surprising results when a problem description mentions keywords from multiple types -- see Recommendation 3.

### (2) Template Selection Logic

**Verdict: Sound with a gap.**

The logic correctly partitions candidates into mode-specific and general, sorts each group alphabetically for determinism, and returns the top `max_candidates`. The `GENERAL_TEMPLATE_NAMES` frozenset correctly identifies the five general-purpose templates.

However, there is no scoring beyond the binary mode-specific/general partition. For example, `SELECTION` with `winner-take-all` might return `budget-constrained`, `competitive-selection`, and `competitive-ranking` in alphabetical order, with `budget-constrained` first -- even though `competitive-selection` is semantically the better match. The alphabetical tiebreaker is deterministic but not semantically meaningful. See Recommendation 4.

### (3) Explicit Parameter Extraction

**Verdict: Appropriately conservative.**

The extraction uses two complementary patterns: `_NUMBER_PATTERN` for `name is/=/: value` forms, and `_BUDGET_PATTERN` for `$value` forms. Both require an exact parameter name match (case-insensitive) against the template's parameter list, and both validate extracted values against range constraints. Out-of-range values are silently discarded rather than extracted -- this is the correct conservative behavior.

The budget-like parameter detection hard-codes a set of known budget-related names (`"budget"`, `"b"`, `"cost"`, `"budget_constraint"`). This is fragile but acceptable for the current template library. The pattern will not match parameter names like `agent_cost` or `beta` even when a dollar amount appears in the text, which is correct (avoiding false positives).

### (4) Assembly and Value Substitution

**Verdict: Functionally correct for current templates, but the substitution method is fragile.**

The `_substitute_symbolic_form` function performs literal string replacement on the symbolic form, sorted by name length descending. This prevents the common substring issue where replacing `w` would corrupt `w_i` -- but only because longer names are replaced first. The approach will still fail when a numeric substitution creates a string that matches another parameter name, or when a parameter name appears inside a mathematical function name. See Recommendation 1.

The assembly correctly skips deferred placeholders (strings starting with `"<deferred:"`), preserving readability of the symbolic form.

### (5) Function-Type Parameter Handling

**Verdict: Correct.**

`identify_gaps` correctly routes `type == "function"` parameters with `derived_from` into the `deferred` category. `fill_parameter_gaps` stores deferred parameters with a `"<deferred: {derived_from}>"` placeholder. `assemble_objective` includes them in the output with source `"deferred"`. The `_substitute_symbolic_form` function correctly skips deferred placeholders during substitution.

One edge case is not tested: a `function`-type parameter that appears in `explicit_params` (user somehow provides a value for it). In `identify_gaps`, explicit params take precedence over the deferred check (line 479), which means a function parameter could be treated as explicit rather than deferred. This may be intentional but is unspecified.

### (6) Gap-Filling Adequacy

**Verdict: Adequate for current types, incomplete for future types.**

- **float**: Coerced via `float()`, validated against `range`. Correct.
- **integer**: Coerced via `int(float())`, validated against `range`. Correct.
- **string**: Any non-empty answer accepted (line 618-619). Correct but no enum validation for parameters with known valid options (e.g., `confirmation_standard` with options `"plausible"`, `"demonstrated"`, `"proven"`).
- **boolean**: Listed in `VALID_PARAMETER_TYPES` but `_coerce_value` returns `None` for boolean type (falls into the `else` branch). No boolean-type parameters exist in the current template library, but this is a latent bug.
- **function**: Correctly deferred, never gap-filled.

---

## Missed Opportunities

1. **No constraint parameter gap-filling.** The pipeline handles objective template parameters but not constraint template parameters. A constraint like `budget` has its own parameters (`budget_limit`, etc.) that are loaded via `load_constraint_templates` but never integrated into the gap-filling flow. The `assemble_objective` function accepts constraint names but never fills their parameters.

2. **No multi-template presentation (FR-003).** The spec requires presenting 1-3 candidates when multiple templates are viable, with plain-language descriptions. `construct_objective` currently always takes `candidates[0]` without consulting the user. The `GapFiller` protocol could support this, but no implementation exists.

3. **No `problem.md` Type field extraction (FR-019).** The `construct_objective` function accepts `explicit_type` as a parameter, but there is no parser that reads `problem.md` and extracts the Type field. The spec envisions this as the primary classification path with keyword matching as fallback; the implementation only has the fallback.

4. **Source map discarded in Stage 2.** `fill_parameter_gaps` meticulously builds a `source` dict tracking whether each parameter was explicit, default, gap_filled, or deferred -- then discards it, returning only `filled`. The caller `construct_objective` reconstructs the source map by re-categorizing from `gap_list`, introducing the value-comparison bug described in Recommendation 2.

---

## Off-Base Assumptions

1. **Alphabetical ordering as a proxy for relevance.** `select_candidate_templates` sorts mode-specific templates alphabetically, but alphabetical order has no relationship to semantic fit. This means `budget-constrained` ranks above `competitive-selection` for `SELECTION` problems despite `competitive-selection` being the canonical match. The test `test_sc001_selection_gets_competitive_selection` passes only because it checks membership, not position.

2. **String replacement as symbolic substitution.** Treating the symbolic form as a raw string and using `str.replace()` is not symbolic substitution -- it is text munging. For the current template library this works because parameter names do not collide with mathematical notation, but it is one template away from producing wrong output. For example, a template with parameters named `x` and `max` would corrupt `max(...)` expressions.

3. **The `NonInteractiveGapFiller` exception-catching pattern.** In `fill_parameter_gaps`, default parameters are handled by calling `filler.fill()` and catching `RuntimeError` to detect non-interactive mode (lines 558-564). This means any `GapFiller` implementation that raises `RuntimeError` for any reason will silently use defaults instead of propagating the error. The detection of non-interactive mode should be explicit (e.g., `isinstance` check or a method on the protocol) rather than exception-based.

---

## Actionable Recommendations

### P1 (Correctness)

**Recommendation 1: Replace string-based symbolic substitution with delimited replacement.**

`_substitute_symbolic_form` uses `str.replace(name, str(value))` which will produce incorrect results if a parameter name appears as a substring of another token. Sort-by-length-descending mitigates but does not eliminate this: a value substitution could introduce new matchable substrings.

Replace with word-boundary-aware substitution:

```python
def _substitute_symbolic_form(form: str, params: dict[str, Any]) -> str:
    result = form
    for name, value in sorted(params.items(), key=lambda kv: -len(kv[0])):
        if isinstance(value, str) and value.startswith("<deferred:"):
            continue
        result = re.sub(rf'\b{re.escape(name)}\b', str(value), result)
    return result
```

This prevents `w` from matching inside `w_i` or `overlap` from matching inside `overlap_penalty`.

**Recommendation 2: Return the source map from `fill_parameter_gaps`.**

`fill_parameter_gaps` builds a precise `source` dict but discards it. `construct_objective` (lines 761-773) then reconstructs the source map by comparing `filled_params.get(name) != gap_list.defaults[name]`. This comparison is wrong when a user explicitly confirms the default value through the gap filler -- the source should be `"gap_filled"` (user actively chose it) but is recorded as `"default"` (passively accepted).

Change `fill_parameter_gaps` to return `tuple[dict[str, Any], dict[str, str]]` and consume the source map directly in `construct_objective`.

**Recommendation 3: Add disambiguation for multi-type keyword matches.**

When `classify_decision_type` finds matches for multiple decision types, it picks the one with the most keyword hits. A problem description like "Choose between cooperative strategies to integrate risk mitigation" triggers SELECTION, INTEGRATION, and STRESS_TEST simultaneously. The highest-count-wins rule is fragile; a single extra keyword occurrence flips the classification.

Add a confidence threshold: when the top two types have match counts within 1 of each other, raise `ValueError` requesting explicit type specification rather than guessing. This aligns with the spec's conservative posture (FR-019 prefers explicit type).

**Recommendation 4: Add boolean type coercion.**

`_coerce_value` returns `None` for `param_type == "boolean"` because the `else` branch is a catch-all that returns `None`. `VALID_PARAMETER_TYPES` includes `"boolean"`, so a template author could reasonably define a boolean parameter. Add:

```python
elif param_type == "boolean":
    return value_str.lower() in ("true", "1", "yes")
```

### P2 (Robustness)

**Recommendation 5: Validate string parameters with known options against an enum.**

Several templates define string parameters with a fixed set of valid options described in the `description` field (e.g., `confirmation_standard`: `"plausible"`, `"demonstrated"`, `"proven"`; `territory_granularity`: `"section"`, `"paragraph"`, `"sentence"`, `"topic"`). The gap filler accepts any non-empty string, with no validation against the documented options.

Add an optional `options` field to `ParameterDefinition` for string-type parameters with a closed set of valid values, and validate against it in `_fill_single_gap`.

**Recommendation 6: Implement FR-003 multi-template presentation.**

`construct_objective` unconditionally uses `candidates[0]`. When `len(candidates) > 1`, the pipeline should present candidates to the user via the `GapFiller` protocol (or a separate `TemplateSelector` protocol) with plain-language descriptions, as FR-003 requires. Without this, template selection is entirely determined by alphabetical ordering, which is semantically arbitrary.

**Recommendation 7: Make non-interactive detection explicit rather than exception-based.**

Replace the `try: filler.fill(...) except RuntimeError` pattern in `fill_parameter_gaps` with an explicit check. Options:
- Add an `is_interactive` property to the `GapFiller` protocol.
- Use `isinstance(filler, NonInteractiveGapFiller)` before calling fill.
- Have `NonInteractiveGapFiller` raise a dedicated `GapFillerRefused` exception (not `RuntimeError`).

The current pattern means any `GapFiller` implementation that raises `RuntimeError` for legitimate failure reasons (network error, timeout) will silently use defaults.

### P3 (Completeness)

**Recommendation 8: Integrate constraint parameter gap-filling.**

`load_constraint_templates` loads and validates constraints, and `assemble_objective` attaches constraint names, but constraint parameters are never incorporated into the gap-filling pipeline. For example, the `budget` constraint has its own `budget_limit` parameter. Without filling these, the assembled objective references constraints that are incompletely parameterized.

**Recommendation 9: Add `problem.md` Type field parser (FR-019).**

The spec designates the explicit Type field as the primary classification mechanism, with keyword matching as fallback. Currently there is no code to parse a `problem.md` file and extract the Type field. Add a `parse_problem_md(path: Path) -> tuple[str, str | None]` function that returns `(problem_text, explicit_type)`.

**Recommendation 10: Improve template ranking beyond alphabetical.**

Replace alphabetical sorting within the mode-specific partition with a relevance heuristic. Options:
- Use keyword overlap between the problem text and the template description.
- Add a `priority` field to `ObjectiveTemplate` for manual curation.
- Match problem keywords against template parameter names and `gap_question` text.

This would ensure `competitive-selection` ranks above `budget-constrained` for SELECTION problems without relying on alphabetical order.

---

## Referenced Documentation

| Document | Path | Relevance |
|----------|------|-----------|
| Spec 014 | `conversus/specs/014-guided-objective-construction/spec.md` | Primary specification being implemented |
| Construction pipeline | `conversus/conversus/schemas/construction.py` | Implementation under review |
| Test suite | `conversus/tests/test_construction.py` | Verification of pipeline behavior |
| Objective schemas | `conversus/conversus/schemas/objectives.py` | `ObjectiveTemplate`, `ParameterDefinition`, `ConstraintTemplate` models |
| Competitive selection template | `conversus/schema/objective-functions/competitive-selection.yml` | Primary winner-take-all template |
| Cooperative consensus template | `conversus/schema/objective-functions/cooperative-consensus.yml` | Primary cooperative template |
| Territory claiming template | `conversus/schema/objective-functions/territory-claiming.yml` | Primary prisoners-dilemma template |
| Risk adversarial template | `conversus/schema/objective-functions/risk-adversarial.yml` | Primary red-blue template |
| Weighted sum template | `conversus/schema/objective-functions/weighted-sum.yml` | General template (all modes) |
| General linear template | `conversus/schema/objective-functions/general-linear.yml` | General template (all modes) |
| Budget constrained template | `conversus/schema/objective-functions/budget-constrained.yml` | Cross-mode template that exposes alphabetical ranking issue |
| Boundary negotiation template | `conversus/schema/objective-functions/boundary-negotiation.yml` | prisoners-dilemma template with string enum parameters |
