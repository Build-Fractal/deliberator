# Functional Architect Review -- Spec 014: Guided Objective Construction

## Executive Summary

The `construction.py` module is a well-structured, 790-line implementation of the three-stage guided objective construction pipeline specified in spec 014. It follows the established conversus patterns closely: pure functions for all pipeline stages, Pydantic for validation, frozen dataclasses for intermediate state, and a pluggable protocol (`GapFiller`) for the interactive boundary. The codebase demonstrates strong composability -- each stage can be tested and invoked independently, and the top-level `construct_objective` orchestrator is a thin composition of the three stages.

The test suite covers all five success criteria (SC-001 through SC-005) and exercises edge cases including integer coercion, frozen dataclass enforcement, and the non-interactive gap filler's refusal behavior. Coverage is thorough at the unit level but has structural gaps around `fill_parameter_gaps` returning a flat dict that silently drops the source map, forcing the orchestrator to reconstruct it from gap-list categories -- a pattern that introduces a subtle redundancy and a potential correctness hazard.

Overall, this is a solid implementation. The recommendations below are refinements, not rewrites.

## Alignment

### What follows the established patterns well

1. **Pure function pipeline.** `classify_decision_type`, `select_candidate_templates`, `extract_explicit_parameters`, `identify_gaps`, `fill_parameter_gaps`, and `assemble_objective` are all stateless pure functions that accept explicit dependencies. This matches the functional service layer mandate in the project's CLAUDE.md and mirrors `game_forms.py` / `objectives.py` exactly.

2. **Pydantic for output validation.** `AssembledObjective` uses a model validator to enforce cross-field invariants (mode validity, source-parameter correspondence), matching the pattern in `ObjectiveTemplate`, `ConstraintTemplate`, `NormalFormGame`, etc.

3. **Frozen dataclasses for intermediate state.** `ParameterGap` and `GapList` are `frozen=True`, preventing accidental mutation between pipeline stages. This is consistent with the immutability-first approach seen in `FeatureSet` and `RoundFeatures` (Pydantic frozen models in `features.py`).

4. **Protocol-based dependency injection.** The `GapFiller` protocol with `@runtime_checkable` cleanly separates the interactive concern from the deterministic pipeline. The three implementations (`InteractiveGapFiller`, `NonInteractiveGapFiller`, and test-only `DictGapFiller`) demonstrate the extension point without coupling.

5. **Deterministic template loading.** `load_objective_templates` and `load_constraint_templates` use `sorted()` for filesystem traversal, ensuring deterministic ordering across platforms. This mirrors `load_mode_mapping` in `game_forms.py`.

6. **FR traceability.** Every function docstring and inline comment cites its functional requirement. The test classes are grouped by FR/SC.

### Where it diverges

1. **`fill_parameter_gaps` returns a flat dict, not a structured result.** Every other pipeline stage returns a typed, validatable object (`DecisionType`, `list[ObjectiveTemplate]`, `dict[str, Any]` with known keys, `GapList`, `AssembledObjective`). Stage 2 returns a raw `dict[str, Any]` without the source map, forcing `construct_objective` to rebuild it. This breaks the composability chain.

2. **`_substitute_symbolic_form` uses naive string replacement.** Unlike the rest of the module, which operates on validated, typed data, this function does raw `str.replace` sorted by key length. This is fragile when parameter names are substrings of each other (e.g., `w` and `w_fast`) or appear in non-parameter positions in the symbolic form.

3. **`load_constraint_templates` is defined but never consumed.** The assembly stage references constraints by name (strings), but no function in the pipeline loads and validates constraint parameters or attaches constraint symbolic forms to the output. This is declared in the spec (FR-011: "selected constraints with parameters") but not yet wired.

## Missed Opportunities

1. **Typed Stage 2 result.** A `FilledParameters` dataclass (or Pydantic model) containing `values: dict[str, Any]` and `source: dict[str, str]` would make the `fill_parameter_gaps -> assemble_objective` handoff type-safe and eliminate the redundant source map reconstruction in `construct_objective` (lines 760-773).

2. **Template selection as a user-facing step (FR-003).** The spec requires presenting multiple candidates to the user when more than one is viable. Currently, `construct_objective` silently picks `candidates[0]`. The `GapFiller` protocol could be extended, or a separate `TemplateSelector` protocol could handle this. As it stands, FR-003 is partially unimplemented.

3. **Regex-based parameter extraction is conservative to a fault.** `extract_explicit_parameters` only handles `name is/=/: value` and `$value` patterns. It cannot extract values from natural phrasing like "we have a budget of $500/month" when the parameter name does not appear as a prefix token. A lightweight alias map (parameter name -> list of aliases) on `ParameterDefinition` would improve extraction recall without adding LLM dependency.

4. **No logging.** `extraction.py` uses `logging.getLogger(__name__)` and `warnings.warn` for missing files. `construction.py` does neither, making debugging of Stage 1 classification failures and Stage 2 retry loops opaque. The pattern is established in the sibling module; it should be adopted here.

5. **`construct_objective` does file I/O.** The YAML write at lines 784-787 couples orchestration to file output. Separating `write_objective(objective, path)` as a standalone function (mirroring `write_features` in `extraction.py`) would keep the orchestrator pure.

## Off-Base Assumptions

1. **Tie-breaking in `classify_decision_type` uses enum definition order.** The `max()` key lambda `(scores[dt], -list(DecisionType).index(dt))` creates an implicit priority (SELECTION > INTEGRATION > SCOPING > STRESS_TEST) that is not documented in the spec. If the spec intended alphabetical or frequency-weighted tie-breaking, this would silently produce wrong results. The assumption is not wrong per se, but it is undocumented and the negative-index trick is brittle if enum members are reordered.

2. **`NonInteractiveGapFiller` is used for defaults too.** When `fill_parameter_gaps` encounters a default parameter, it calls `filler.fill()` and catches the `RuntimeError` from `NonInteractiveGapFiller` to fall back to the default. This works but conflates "I cannot interact" with "accept the default." A cleaner model would skip the filler call entirely for defaults in non-interactive mode.

3. **`_DECISION_TYPE_MODE` assumes a 1:1 mapping between decision type and mode.** The spec says general templates are candidates for all types, but the mode mapping is fixed. If a user specifies `mode="cooperative"` for a `SELECTION` problem, `select_candidate_templates` will use `target_mode = "winner-take-all"` (from the decision type), ignoring the user's mode override. The `mode` parameter to `select_candidate_templates` is shadowed by the internal lookup.

4. **`GapList.gaps` is a mutable list inside a frozen dataclass.** `frozen=True` on a dataclass prevents attribute reassignment but does not prevent mutation of mutable fields (`gaps.append(...)` would succeed after construction). The frozen test in the test suite only checks attribute reassignment, not content mutation. This is a known Python limitation, not a bug, but it undermines the immutability guarantee the frozen annotation communicates.

## Actionable Recommendations

### P1 -- Correctness and Spec Compliance

**R1. Return a typed result from `fill_parameter_gaps` that includes the source map.**

Current state: `fill_parameter_gaps` returns `dict[str, Any]` (just values). The source map is constructed internally but discarded. `construct_objective` rebuilds it by re-walking `gap_list` categories.

Problem: The source map reconstruction at lines 760-773 can diverge from what Stage 2 actually computed, particularly when a default is overridden (the override-detection comparison `filled_params.get(name) != gap_list.defaults[name]` is fragile with float equality).

Fix: Define a `FilledParameters` dataclass with `values: dict[str, Any]` and `source: dict[str, str]`. Have `fill_parameter_gaps` return it. Remove the reconstruction logic from `construct_objective`.

**R2. Fix the shadowed `mode` parameter in `select_candidate_templates`.**

Current state: Line 331 (`target_mode = _DECISION_TYPE_MODE.get(decision_type, mode)`) means the caller's `mode` argument is used only as a fallback when the decision type is not in `_DECISION_TYPE_MODE`. Since all four decision types are mapped, the caller's `mode` is always ignored.

Problem: When `construct_objective` is called with `mode="cooperative"` for a SELECTION problem, templates compatible with `cooperative` should be returned, not `winner-take-all` templates. The test `test_explicit_mode_override` passes only because cooperative templates happen to have defaults for all parameters; it does not verify that templates were selected by cooperative mode compatibility.

Fix: In `select_candidate_templates`, prefer the caller's `mode` when explicitly passed, falling back to `_DECISION_TYPE_MODE` only when `mode` is None. Alternatively, add a `mode_override` parameter.

**R3. Implement FR-003: multi-candidate template presentation.**

The spec requires: "When multiple templates are viable candidates, the parser MUST present them to the user with plain-language descriptions and ask for selection." Currently, `candidates[0]` is always chosen silently. Add a `TemplateSelector` protocol (or reuse `GapFiller`) to present candidates when `len(candidates) > 1`.

**R4. Wire constraint template loading into the assembly stage.**

`load_constraint_templates` exists but is never called in the pipeline. FR-011 requires the output to include "selected constraints with parameters." The assembled output includes constraint names but not their parameters or symbolic forms. Either assemble full constraint data into the output or document this as a deferred follow-up.

### P2 -- Robustness and Maintainability

**R5. Replace naive `str.replace` in `_substitute_symbolic_form` with regex word-boundary substitution.**

Current approach: Sort parameters by name length (descending) and do `result.replace(name, str(value))`. This breaks when a parameter name like `w` appears inside a word (e.g., `weight`, `new_score`), or when two parameters share a prefix (e.g., `w` and `w1`).

Fix: Use `re.sub(rf'\b{re.escape(name)}\b', str(value), result)` to ensure only whole-token substitution. This matches the precision standard set by the regex-based classification in Stage 1.

**R6. Add logging to the construction pipeline.**

`extraction.py` uses `logging.getLogger(__name__)` and `warnings.warn`. `construction.py` has neither. Add `logger` and log: (a) classified decision type, (b) selected candidate templates, (c) extracted explicit parameters, (d) gap count, (e) retry attempts in `_fill_single_gap`. This is critical for debugging failed classifications in production use.

**R7. Separate `write_objective` from `construct_objective`.**

The file-write at lines 784-787 of `construct_objective` breaks the pure-function pattern. Extract it into a standalone `write_objective(objective: AssembledObjective, path: Path) -> None` function, mirroring `write_features` in `extraction.py`. This keeps `construct_objective` testable without filesystem side effects and follows the established pattern in the codebase.

### P3 -- Test Coverage and Edge Cases

**R8. Add a test that validates mode override actually changes template selection.**

`test_explicit_mode_override` verifies `obj.mode == "cooperative"` but does not check that cooperative-compatible templates were selected. Add an assertion that the chosen template has `"cooperative"` in `mode_compatibility`. This would have caught the R2 bug.

**R9. Add a test for `_substitute_symbolic_form` with overlapping parameter names.**

Create a template with parameters `w` and `w_fast`, both having numeric values. Assert that substituting `w=2.0` does not corrupt `w_fast` in the symbolic form string `"J = -w * score + w_fast * speed"`. This documents the current fragility (R5) and serves as the regression test for the fix.

**R10. Add a test for `GapList` content mutation (frozen bypass).**

Verify that while `gap_list.gaps = [...]` raises `AttributeError`, `gap_list.gaps.append(...)` succeeds. Document this as a known limitation or switch to `tuple` for truly immutable sequences. This is a documentation/awareness item, not necessarily a code change, but it should be explicit.

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/014-guided-objective-construction/spec.md` -- Feature specification, functional requirements FR-001 through FR-023, success criteria SC-001 through SC-005.
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/construction.py` -- Implementation under review.
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_construction.py` -- Test suite under review.
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/game_forms.py` -- Reference pattern for Pydantic models, mixin validation, mode mapping.
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/objectives.py` -- Reference pattern for parameter validation, frozenset constants, cross-field invariants.
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/extraction.py` -- Reference pattern for pipeline architecture, logging, `write_features` as standalone I/O function.
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/__init__.py` -- Public API surface for the schemas package.
