# Functional Architect Revision

**Date**: 2026-03-24
**Inputs**: Phase 1 review, 3 cross-reviews received (from game-theorist, schema-engineer, spec-compliance), 3 cross-reviews written (of game-theorist, schema-engineer, spec-compliance)

---

## Recommendation Dispositions

### R1: Return a typed result from `fill_parameter_gaps` that includes the source map
**Status: SURVIVING (P1)**

Unanimous agreement across all four reviewers. The named-dataclass approach (`FilledParameters` or `FillResult`) is accepted by all. I maintain the `FilledParameters` naming -- it describes the content (filled parameter values + source map), not the operation.

### R2: Fix the shadowed `mode` parameter in `select_candidate_templates`
**Status: MODIFIED (P2, downgraded from P1, test-only fix)**

Spec-compliance's cross-review makes a strong argument: FR-018 defines a *fixed* decision-type-to-mode mapping, and the `mode` parameter is a fallback for custom decision types, not an override. The grammatical analysis is convincing: the spec says "explicit and deterministic" mapping, which implies the mapping is authoritative.

I was wrong to classify this as P1 (correctness bug). The behavior is spec-correct: SELECTION always maps to winner-take-all, regardless of what the caller passes as `mode`. The `mode` parameter is a fallback path that only activates for custom/unknown decision types not in `_DECISION_TYPE_MODE`.

However, the test `test_explicit_mode_override` is misleading -- it claims to test mode override but doesn't verify template selection. Downgraded to P2 with a test-only fix: rewrite the test to either (a) test a custom decision type that triggers the fallback, or (b) rename it to `test_mode_carried_through_to_output` to accurately describe what it verifies.

### R3: Implement FR-003: multi-candidate template presentation
**Status: SURVIVING (P1)**

All reviewers agree FR-003 is unimplemented. Game-theorist upgrades to P1 in their revision. Spec-compliance was P1 from the start. I maintain P1.

Game-theorist's minimal fix (default `template_selector` callback) is the right incremental approach. The full interactive presentation is a follow-up.

### R4: Wire constraint template loading into the assembly stage
**Status: MODIFIED (P2, downgraded from P1)**

Spec-compliance's cross-review provides a compelling grammatical analysis of the FR-011 spec sentence: "all parameters with provenance" and "selected constraints" are separate comma-delimited items. "With parameters" modifies "all parameters," not "selected constraints." My reading that constraints need their own parameters in the output was a misparse of the spec.

The assembled output includes `constraints: list[str]` (constraint names), which satisfies FR-011 as currently written. Constraint parameter resolution is a follow-up feature. Downgraded to P2.

### R5: Replace naive `str.replace` with regex word-boundary substitution
**Status: MODIFIED (P1, upgraded from P2)**

Three reviewers classify this as P1; I was the sole P2 outlier. The argument that convinced me: the fix is trivial (one regex line), and the bug is one template edit away from producing wrong output. The competitive-selection template has `w` as a standalone parameter -- any template modification that introduces a word containing `w` in the symbolic form would trigger silent corruption. "Hasn't triggered yet" is not a valid defense for a trivial fix.

### R6: Add logging to the construction pipeline
**Status: SURVIVING (P2)**

No pushback from any cross-reviewer. Spec-compliance notes logging isn't a spec requirement, which is true, but it's a codebase-consistency requirement (extraction.py has it). P2 stands.

### R7: Separate `write_objective` from `construct_objective`
**Status: MODIFIED (P3, downgraded from P2)**

Game-theorist and spec-compliance both push back: `construct_objective` is an orchestrator, not a service function, and orchestrators commonly have side effects. The CLAUDE.md purity mandate applies to service functions. I accept the downgrade. The extraction pattern (`write_features`) is good practice but not a P2 urgency item when the current code works correctly and tests exercise the pure path via `output_path=None`.

### R8: Add a test that validates mode override actually changes template selection
**Status: MODIFIED (P3, aligned with R2 downgrade)**

Given R2's downgrade (the mode parameter is a fallback, not an override), the test should be rewritten to test the fallback path with a custom decision type, or renamed to accurately describe what it tests. P3.

### R9: Add a test for `_substitute_symbolic_form` with overlapping parameter names
**Status: SURVIVING (P2, upgraded from P3)**

This test becomes the regression test for the R5 fix. It should exist before the fix is applied (to demonstrate the bug) and pass after (to confirm the fix). Upgraded to P2 because it's the verification mechanism for a P1 fix.

### R10: Add a test for `GapList` content mutation (frozen bypass)
**Status: SURVIVING (P3)**

No pushback. This is an awareness item, not a correctness fix.

---

## New Recommendations

### NEW-1: Add `SourceProvenance` model for FR-020 compliance (P1)
**Source**: Schema-engineer's R1, which I didn't raise as a separate structural recommendation.

Schema-engineer's `SourceProvenance` model with required `problem_md` and `filled_by: dict[str, Literal[...]]` is the right approach. I originally proposed keeping `source` as `dict[str, str]` with `problem_md` as a separate field, but schema-engineer's nested model is more spec-faithful and more type-safe. Spec-compliance's point about `problem_md` being required (not optional) is also correct.

### NEW-2: Define `GapFillRefused` exception alongside `GapFiller` protocol (P2)
**Source**: Schema-engineer's P2 recommendation, confirmed by all cross-reviewers.

I didn't raise the RuntimeError pattern in my review, but all three other reviewers flag it. The consensus fix (custom exception in the same module as the protocol) is clean and non-breaking.

---

## Position Summary

The cross-review process changed two significant positions: (1) the shadowed mode parameter is not a bug -- it's spec-correct behavior with a misleading test name (downgraded from P1 to P2), and (2) constraint wiring is not a P1 -- the spec sentence was misparsed (downgraded from P1 to P2). Conversely, the str.replace fix was upgraded from P2 to P1 based on the 3-to-1 consensus.

My core position remains: the pipeline architecture is sound and follows established patterns well. The fixes are refinements, not rewrites.

**Final P1 list**: Source map return (FilledParameters), str.replace regex fix, FR-003 multi-template, SourceProvenance model.
**Final P2 list**: Mode override test rewrite, constraint wiring, logging, GapFillRefused exception, overlapping-params test.
**Final P3 list**: write_objective extraction, mode override test rename, GapList mutation test.
