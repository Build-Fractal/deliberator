# Schema Engineer Revision

**Date**: 2026-03-24
**Inputs**: Phase 1 review, 3 cross-reviews received (from game-theorist, functional-architect, spec-compliance), 3 cross-reviews written (of game-theorist, functional-architect, spec-compliance)

---

## Recommendation Dispositions

### P1: Fix `AssembledObjective.source` to match FR-020 structure
**Status: MODIFIED (P1, required `problem_md`)**

Spec-compliance's cross-review correctly challenges my `problem_md: str | None = None` default: if `problem_md` is the traceability anchor, making it optional undermines the guarantee. I accept the modification: `problem_md` should be required, with a sentinel value like `"<stdin>"` for programmatic use without a file.

Functional-architect raises a competing approach: keep `source` as `dict[str, str]` and add `problem_md` as a *separate* field on `AssembledObjective`. This is less spec-faithful (the spec describes source as containing both) but less disruptive to existing code. I maintain the `SourceProvenance` model approach because: (1) the spec explicitly nests `problem_md` inside `source`, (2) the project uses Pydantic models for structured data, not flat dicts with mixed semantics.

### P1: Return source map from `fill_parameter_gaps`
**Status: SURVIVING (P1)**

Unanimous agreement. I accept functional-architect's `FilledParameters` naming suggestion -- it's more descriptive than my `FillResult`.

### P1: Fix `_substitute_symbolic_form` substring collision
**Status: SURVIVING (P1)**

3-to-1 agreement on P1 (functional-architect is the P2 outlier). Game-theorist's cross-review clarifies the specific failure modes. My original description of the `w`-inside-`score` scenario was inaccurate for the sort-by-length-descending implementation (score is replaced before w). The real threats are: (1) single-char parameters matching inside words not yet replaced, and (2) value substitutions introducing new matchable substrings. Both are addressed by the word-boundary regex fix.

### P1: Add boolean coercion to `_coerce_value`
**Status: MODIFIED (P2, downgraded)**

Game-theorist's cross-review and functional-architect's cross-review both note that no boolean parameters exist in the current template library, making this a latent bug with no current trigger. I accept the downgrade to P2. The fix itself should use my bidirectional approach (explicit true/false/None branches) per game-theorist's revision acceptance.

Functional-architect's cross-review also identifies a missing piece: the retry guidance path in `_fill_single_gap` has no boolean-specific guidance message. The fix should include guidance: "Please answer yes/no or true/false."

### P2: Introduce a custom exception for GapFiller refusal
**Status: SURVIVING (P2)**

All reviewers agree on the diagnosis. Consensus converges on `GapFillRefused(Exception)` defined alongside `GapFiller` in the same module. No further modification needed.

### P2: Implement FR-003 multi-candidate presentation
**Status: MODIFIED (P1, upgraded)**

Spec-compliance and functional-architect both classify FR-003 as P1. Game-theorist upgrades to P1 in their revision. The MUST language and the fact that every multi-template case triggers the violation make P1 correct. I accept the upgrade.

Game-theorist's minimal fix (default `template_selector` callback) is pragmatic for backward compatibility. The full interactive presentation can be a P2 follow-up.

### P2: Add `problem_md` path parameter to `construct_objective`
**Status: MERGED with source structure fix (P1)**

This is now part of the `SourceProvenance` restructuring. The `problem_md_path` parameter feeds into `SourceProvenance.problem_md` in the assembled output. No separate recommendation needed.

### P2: Validate `source` provenance tags are from a closed set
**Status: SURVIVING (P2)**

Functional-architect's cross-review suggests `Literal` type annotation over runtime validation for projects using mypy. I accept this: `Literal["explicit", "default", "gap_filled", "deferred"]` on the `filled_by` dict values is better than a runtime check. The Pydantic model can enforce this via the `Literal` type if `SourceProvenance.filled_by` is typed as `dict[str, Literal["explicit", "default", "gap_filled", "deferred"]]`.

### P3: Add `.yaml` extension support to `load_objective_templates`
**Status: WITHDRAWN**

Functional-architect's cross-review makes a strong argument: adding a second extension creates inconsistency. The project convention is `.yml` (all existing templates use it). The fix should be documentation (state the convention) not code (silently accept both). Withdrawn in favor of a documentation clarification.

### P3: Test `_fill_single_gap` retry path
**Status: SURVIVING (P3)**

Spec-compliance classifies the retry test as P2, which is arguably justified since FR-007 is a MUST requirement. But the implementation exists and is correct by inspection; the test is a regression-prevention measure. P3 stands.

---

## New Recommendations

### NEW-1: Separate `write_objective` from `construct_objective` (P3)
**Source**: Functional-architect's R7.

I didn't raise this in my review, but functional-architect correctly identifies that `extraction.py` has `write_features` as a standalone function. Separating file I/O from orchestration follows the established pattern and improves testability. Classified as P3 because the current code works correctly and tests use `output_path=None` to skip the write.

### NEW-2: Add logging to construction pipeline (P2)
**Source**: Functional-architect's R6.

I should have flagged the absence of logging as a pattern violation. The sibling module `extraction.py` uses `logging.getLogger(__name__)` and `warnings.warn`. The construction pipeline should do the same, especially for classification results and retry loops.

---

## Position Summary

My core position is unchanged: the source map data loss and str.replace collision are the most urgent bugs, and the `AssembledObjective.source` structure needs to match the spec. I've upgraded FR-003 to P1, downgraded boolean coercion to P2, and withdrawn the `.yaml` extension recommendation.

The cross-review process revealed I was inaccurate about the specific str.replace failure mode (my `w`-inside-`score` example was wrong for the current sort-by-length implementation). The real danger is more nuanced but equally valid, and the fix is the same.

**Final P1 list**: Source structure (SourceProvenance with required problem_md), source map return, str.replace fix, FR-003 multi-template.
**Final P2 list**: GapFillRefused exception, boolean coercion, provenance tag Literal validation, logging.
**Final P3 list**: Retry path test, write_objective extraction.
