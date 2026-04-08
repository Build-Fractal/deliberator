# Round 2 Review: Spec 005 -- Generalized Template Schema, Variables, and Linter

**Agent**: functional-typing
**Perspective**: Functional programming and type safety (Python FP paradigm, Pydantic v2)
**Round**: 2 of 2
**Date**: 2026-03-21

---

## Executive Summary

The Round 1 synthesis produced a rigorous, well-traced resolution of the deliberation's 29 original recommendations. The 4 remaining disputes are all resolvable -- none represent deep architectural disagreements. I concur with the synthesizer's resolutions on Disputes 1, 3, and 4, and offer a refinement on Dispute 2 that strengthens the synthesizer's position without reversing it. My Round 2 focus is on (a) confirming the synthesizer's dispute resolutions from a type-safety perspective, (b) identifying two missed opportunities in the P1 and P2 action items that the Round 1 process did not surface, and (c) correcting one off-base assumption in the synthesizer's analysis of the `error_type` dispute.

The implementation as it stands is already well-aligned with Constitution Principle IX. The Round 1 process correctly identified and resolved the major type-safety gaps (raw `str` path-lists, impure loaders, unstructured error returns). The remaining work is execution, not design.

---

## Alignment

### Synthesizer's Dispute Resolutions

**Dispute 1 (Programmatic API parameter design)**: The synthesizer's resolution -- `ValidationConfig` Pydantic model with `root` and `mode`, no `known_plugin_variables` -- is correct from a type-safety perspective. A Pydantic model is the ideal extension surface: adding a field with a default value is non-breaking, fully typed, and introspectable. This is strictly superior to both bare parameters (functional-typing's Round 1 position, which I now consider too conservative) and pre-emptive untyped parameters (game-engine-advocate's position). I accept the `ValidationConfig` model approach as an improvement over my original bare-parameter proposal.

**Dispute 3 (Schema version priority P2 vs. P3)**: I accept P2. The synthesizer's reasoning is sound -- the implementation cost is trivial, and establishing the convention before spec 006's schema evolution is pragmatically justified. My Round 1 objection was correct on the merits (no consumer, no validation) but wrong on the priority signal. I will not re-litigate this.

**Dispute 4 (Bare import fix sequencing)**: The synthesizer correctly identifies that the import fix and the programmatic API are the same unit of work. The distinction between P1 and P2 is artificial when one is a prerequisite for the other. I concur with the resolution: the import fix is part of P1-2, not a separate deliverable.

**Dispute 2 (error_type Literal vs. str)**: I accept the synthesizer's resolution (`str` with runtime validation against a known set) but offer a refinement below. My Round 1 position that `Literal` is correct for spec 005's scope was technically defensible, but the synthesizer's pattern-consistency argument (apply the same resolution used for modes) is more architecturally coherent. I do not reverse this concession.

### Round 1 Convergence Items

The 14 convergence items are well-structured and correctly prioritized. I specifically endorse:

- **P1-1 (Purify schema-loading functions)**: This is the single most important change for functional correctness. The current `sys.exit()` calls in `load_variables_schema` and `load_mode_schema` make these functions untestable in isolation and impossible to compose. The `SchemaLoadError` approach is textbook functional error handling.

- **P1-3 (PathList custom type)**: The `BeforeValidator` + custom serializer pattern is the right Pydantic v2 approach. This eliminates the most pervasive type-safety gap in the current models -- 10 fields typed as `str` that are semantically `list[Path]`.

- **P2-5 (frozen=True on TemplateContext)**: Immutability on the context models enforces construction discipline and prevents mutation after validation. The composition approach for plugins (separate `PluginContext`) is architecturally clean.

---

## Engagement with Round 1 Disputes

### Dispute 2 Refinement: `KNOWN_ERROR_TYPES` as `frozenset` with `@field_validator`

The synthesizer resolved this by proposing `str` with runtime validation against `KNOWN_ERROR_TYPES: frozenset[str]`, mirroring the mode validation pattern. I accept this resolution but propose a refinement that strengthens its type-safety properties without changing the surface-level decision.

The refinement: the `@field_validator` on `LintError.error_type` should issue a **warning** (not raise `ValueError`) when encountering an unknown error type. The rationale is that `VALID_MODES` rejection is correct (an unknown mode means the schema file is malformed), but an unknown error type from a plugin-contributed `check_*` function means "I don't recognize this yet," not "this is invalid." A strict validator that rejects unknown error types would force plugin authors to register their types in the core module before they can return errors -- recreating the `Literal` problem in runtime form.

The synthesizer's phrasing "validated against a known registry" is ambiguous on this point. I propose: validation logs a warning for unrecognized types but does not reject the `LintError` instance. The `KNOWN_ERROR_TYPES` set serves autocompletion and documentation, not gatekeeping.

This is a minor refinement, not a reversal. The synthesizer's resolution stands.

### Dispute 1 Confirmation: `ValidationConfig` Model

I want to explicitly record why the `ValidationConfig` model is the right answer from a typing perspective, beyond the synthesizer's analysis.

A Pydantic model as the API boundary gives us three properties simultaneously:
1. **Named fields with defaults** -- adding `known_plugin_variables: frozenset[str] = frozenset()` in spec 007 is a non-breaking, fully-typed change.
2. **Validation at construction** -- malformed configurations are rejected before `validate_all` begins execution. This is superior to bare parameters, which defer validation to the function body.
3. **Serialization for testing** -- `ValidationConfig` instances can be serialized to/from JSON for test fixtures and CI configuration, which bare parameters cannot.

game-engine-advocate's underlying concern (future extensibility) is fully addressed by this pattern. The `ValidationConfig` model IS the forward-compatibility mechanism; no speculative parameters are needed.

---

## Missed Opportunities

### MO-1: `validate_template` Return Type Should Be Generic Over Error Model

The Round 1 convergence correctly identifies that `check_*` functions should return `list[LintError]` (P2-3). However, the `validate_template` function signature (`validate.py` L281-305) composes these results via list concatenation. When the error model changes from `str` to `LintError`, this concatenation still works -- but the return type annotation should be explicitly `list[LintError]`, not inferred.

More importantly, `validate_template` currently takes 6 parameters. After P1-2 (programmatic API) and P1-4 (`config_conditions`), it will take more. This function should accept a `ValidationContext` (distinct from `TemplateContext`) that bundles the schema, mode schema, and all var names:

```python
@dataclass(frozen=True)
class ValidationContext:
    variables_schema: VariablesSchema
    mode_schema: ModeSchema
    all_var_names: frozenset[str]
```

This is not a new Pydantic model (it's internal to the linter, not a schema artifact), but a frozen dataclass that reduces parameter passing. The `validate_template` signature becomes `(template_path: Path, phase: str, mode: str, ctx: ValidationContext) -> list[LintError]`, which is more composable.

**Priority**: P2. This is a refactoring that improves composability but does not change behavior.

### MO-2: Test Generator Functions Should Use `itertools.product` for Case Generation

The test file (`test_validate.py`) contains 5 case-generator functions (`all_template_cases`, `required_variable_cases`, `structural_marker_cases`, `arbitration_heading_cases`, `dispute_heading_cases`). Several of these manually construct the cross-product of modes and phases using nested list comprehensions. For example, `all_template_cases` (L163-170):

```python
return [
    (mode, phase)
    for mode in MODES
    for phase in PHASES
    if template_path(mode, phase).exists()
]
```

This is fine for the simple case but becomes unwieldy for `required_variable_cases` (L192-214), which nests three levels (modes, phases, variables) with multiple filter conditions.

The `itertools.product` function would make the cross-product explicit:

```python
from itertools import product

def all_template_cases() -> list[tuple[str, str]]:
    return [
        (mode, phase)
        for mode, phase in product(MODES, PHASES)
        if template_path(mode, phase).exists()
    ]
```

For `required_variable_cases`, the improvement is more significant -- the three-level nesting becomes a flat `product(MODES, PHASES, vs.variables.items())` with a filter chain.

**Priority**: P3. This is a readability improvement consistent with Constitution Principle IX's FP guidance ("Use iterators, generators, and itertools/functools when they improve clarity").

---

## Off-Base Assumptions

### OBA-1: The Synthesizer's Claim That Adding a Parameter Is "Non-Breaking" Needs Qualification

The synthesizer states (Dispute 1 analysis): "since the API has no external consumers until spec 008 ships, any parameter addition before that point is non-breaking."

This is correct in a narrow sense (no external callers means no callers to break), but it elides a distinction that matters for the test suite. `test_validate.py` already calls `validate_template` with explicit positional arguments (L354-355). Adding parameters to `validate_template` without keyword-only enforcement WILL break existing tests unless the new parameters are keyword-only or have defaults.

The synthesizer's resolution (use `ValidationConfig` model) actually handles this correctly -- by bundling parameters into a model, the function signature is stable. But the reasoning that "no external consumers" means "non-breaking" should be stated more precisely: the `ValidationConfig` model is non-breaking because Pydantic models absorb new fields with defaults, not because there are no callers.

This is a clarification of the synthesizer's reasoning, not a disagreement with the resolution.

### OBA-2: `condition` Field Is Not "Free-Text" -- It Has Implicit Structure

The synthesizer and all three agents treated the `condition` field in `variables.yml` as free-text prose (e.g., P3-5 proposes formalizing its syntax). However, examining the actual `condition` values in the implementation:

- `variables.yml` L64-67: `condition: "Required in synthesis, arbitration, and cross-round-synthesis for all modes..."`
- `variables.yml` L95-97: `condition: "Required in cross-round-synthesis (used directly in template text)..."`

These are documentation strings, not machine-readable conditions. The spec's data model (Section 3) shows `condition: "rounds > 1"` which looks like a parseable expression, but the implementation uses prose sentences.

The disconnect is between the spec's aspiration (parseable conditions) and the implementation's reality (documentation strings). P3-5 (formalize condition syntax) correctly identifies this gap, but it should be flagged as a spec-implementation inconsistency rather than a "formalization" of something that currently works. The current implementation ignores the `condition` field entirely -- `validate.py` never reads it. P1-4 (`config_conditions` with typed `ConfigCondition` model) is the correct typed approach to machine-readable conditions, making P3-5 either redundant with P1-4 or complementary to it, depending on scope.

---

## Actionable Recommendations

### From Prior Disputes (accepting synthesizer's resolutions)

1. **Dispute 1**: Accept `ValidationConfig` model. No further action from functional-typing.

2. **Dispute 2**: Accept `str` with `KNOWN_ERROR_TYPES` validation. Recommend the `@field_validator` issue a warning for unknown types rather than reject the instance. This preserves plugin extensibility without sacrificing type documentation.

3. **Dispute 3**: Accept P2 for schema version field. No further action.

4. **Dispute 4**: Accept import fix as part of P1-2. No further action.

### New Recommendations

5. **MO-1 (P2)**: Introduce a frozen `ValidationContext` dataclass to bundle the 3 schema-related parameters passed to `validate_template`, reducing parameter count and improving composability. This should be implemented alongside P2-3 (structured error model) since both refactor the same function signatures.

6. **MO-2 (P3)**: Use `itertools.product` in test case generators where it improves readability over nested list comprehensions, consistent with Constitution Principle IX's FP guidance.

7. **OBA-2 (editorial)**: Clarify in P3-5's scope description that the `condition` field is currently documentation-only (never read by `validate.py`) and that P1-4's `config_conditions` model is the typed machine-readable alternative. P3-5 should specify whether it extends, replaces, or complements `config_conditions`.

---

## Referenced Documentation

- **Constitution Principle IX** (`.specify/memory/constitution.md` L141-184): Functional programming mandate, explicit typing requirements, Pydantic model mandate. The primary lens for this review.
- **Python Functional Programming HOWTO** (`.firecrawl/python-functional-howto.md`): Referenced by Principle IX. Relevant sections: composability, itertools, generator expressions.
- **Pydantic v2 `frozen` models**: Supports P2-5 (`frozen=True` on TemplateContext). Pydantic v2's `model_config = {"frozen": True}` makes instances hashable and immutable post-construction.
- **Pydantic v2 `BeforeValidator`**: Supports P1-3 (PathList custom type). The `Annotated[list[Path], BeforeValidator(parse_newline_paths)]` pattern is the standard Pydantic v2 approach for custom deserialization.
- **Round 1 Synthesis** (`round-1/summary/final.md`): All dispute resolutions and convergence items referenced above.
- **`linter/validate.py`** L281-305: `validate_template` function whose signature is affected by MO-1.
- **`linter/test_validate.py`** L163-214: Test case generators affected by MO-2.
- **`linter/models.py`** L129-270: `TemplateContext` hierarchy affected by P1-3, P2-5, and P1-5.
- **`schema/variables.yml`** L62-67, L93-97: `condition` field instances discussed in OBA-2.
