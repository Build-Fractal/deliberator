# Game-Theorist Revision

**Date**: 2026-03-24
**Inputs**: Phase 1 review, 3 cross-reviews received (from schema-engineer, functional-architect, spec-compliance), 3 cross-reviews written (of schema-engineer, functional-architect, spec-compliance)

---

## Recommendation Dispositions

### Recommendation 1: Replace string-based symbolic substitution with delimited replacement
**Status: SURVIVING (P1)**

All four reviewers identify this bug. Schema-engineer, functional-architect, and spec-compliance all agree on the regex word-boundary fix. Functional-architect initially classified it P2 but is the sole outlier (3 P1 vs 1 P2). Functional-architect's DC-1 cross-review of me initially questioned whether word boundaries handle mathematical expressions but then withdrew the concern after analysis. The fix is trivial (one regex line) and the bug is one template edit away from corrupting output. P1 stands.

### Recommendation 2: Return the source map from `fill_parameter_gaps`
**Status: SURVIVING (P1)**

Unanimous agreement across all four reviewers. This is the highest-confidence finding. Schema-engineer proposes a `FillResult` dataclass; functional-architect proposes `FilledParameters` dataclass; both are the same pattern with different names. I accept the named-dataclass approach over my original tuple proposal -- it's more consistent with the project's frozen-dataclass pattern.

### Recommendation 3: Add disambiguation for multi-type keyword matches
**Status: MODIFIED (P2, warning instead of exception)**

Functional-architect and spec-compliance both push back on raising `ValueError` for ambiguous classification. Functional-architect argues the pipeline should never refuse to produce output. Spec-compliance notes the conflict with FR-023 non-interactive mode -- an exception halts the pipeline with no recovery path. I accept this criticism. The deterministic tiebreaker is preferable to an exception.

Modified recommendation: When the top two decision types have match counts within 1 of each other, log a warning (if logging is added per functional-architect's R6) and add a `classification_confidence: float` field to the return or a metadata dict. Do not raise an exception. The caller can use `explicit_type` to override if the low-confidence classification produces wrong results.

### Recommendation 4: Add boolean type coercion
**Status: MODIFIED (P2, bidirectional coercion)**

Schema-engineer's cross-review correctly identifies that my original fix (`value_str.lower() in ("true", "1", "yes")`) maps everything including garbage to a boolean, which is wrong for extraction (where None means "don't extract"). I accept schema-engineer's bidirectional approach with explicit true/false branches and None for unrecognized input.

Modified from P1 to P2: functional-architect's cross-review notes that no boolean parameters exist in the current template library, so the bug has no current trigger. It's a latent bug, not an active one. P2 is correct.

### Recommendation 5: Validate string parameters with known options against an enum
**Status: SURVIVING (P2)**

No cross-reviewer pushes back on this. Spec-compliance notes it requires a schema change to `ParameterDefinition`, which should be a spec amendment. I accept that framing -- the `options` field should be proposed as a spec amendment, not applied directly. The recommendation stands as P2 with the caveat that it requires a schema change.

### Recommendation 6: Implement FR-003 multi-template presentation
**Status: MODIFIED (P1, upgraded)**

Spec-compliance's cross-review makes a compelling argument: the spec uses MUST, and every multi-template case triggers the violation (not just "rare ambiguous scenarios" as I originally claimed). SELECTION problems produce 3+ candidates, and `candidates[0]` is always silently used. I was wrong to classify this as P2. Upgraded to P1.

However, I maintain that the P1 fix should be minimal: add a `template_selector` callback to `construct_objective` that defaults to `lambda candidates: candidates[0]` for backward compatibility. The full interactive presentation can follow as a P2 enhancement.

### Recommendation 7: Make non-interactive detection explicit
**Status: SURVIVING (P2)**

All reviewers agree the RuntimeError pattern is fragile. Consensus converges on a custom `GapFillRefused` exception defined alongside the `GapFiller` protocol. This is the least-invasive fix. I withdraw my `is_interactive` property proposal (it changes the protocol) and my `isinstance` check proposal (it couples to implementation). The custom exception is the right approach.

### Recommendation 8: Integrate constraint parameter gap-filling
**Status: MODIFIED (P2, upgraded from P3)**

Functional-architect classifies constraint wiring as P1 and argues FR-011 requires constraints "with parameters." Spec-compliance's cross-review of functional-architect does a grammatical analysis of the spec sentence and concludes "selected constraints" is a separate item from "all parameters with provenance." I find spec-compliance's reading more convincing. However, constraint names without parameters are not fully actionable. Upgraded from P3 to P2.

### Recommendation 9: Add `problem.md` Type field parser
**Status: SURVIVING (P3)**

No strong pushback. Spec-compliance notes FR-019 is MET at the function level (accepts `explicit_type`). The parser is a convenience for CLI integration. P3 is correct.

### Recommendation 10: Improve template ranking beyond alphabetical
**Status: SURVIVING (P3)**

No strong pushback, but spec-compliance notes the spec doesn't specify ranking criteria beyond mode compatibility. The alphabetical ordering is compliant but not optimal. P3 is correct -- this is a UX improvement, not a compliance fix.

---

## New Recommendations

### NEW-1: Add logging to construction pipeline (P2)
**Source**: Functional-architect's R6, which I failed to raise.

Functional-architect correctly identifies that `extraction.py` uses `logging.getLogger(__name__)` and `warnings.warn`, while `construction.py` has neither. Classification failures and retry loops are opaque without logging. I should have flagged this as a consistency gap.

### NEW-2: Strengthen mode override test (P3)
**Source**: Functional-architect's R8, which identifies that `test_explicit_mode_override` doesn't verify template selection actually matched cooperative mode.

Whether the mode parameter is an override or a fallback (spec-compliance's reading), the test should verify what it claims to test.

---

## Position Summary

My core position is unchanged: the pipeline architecture is sound, and the most dangerous bugs are the str.replace collision (P1) and the source map data loss (P1). I've upgraded FR-003 to P1 after spec-compliance's persuasive argument about MUST-level requirements. I've downgraded boolean coercion from P1 to P2 (no current trigger) and softened disambiguation from ValueError to a warning.

The cross-review process revealed two gaps in my original review: (1) I didn't assess SC-002 or FR-009/FR-014/FR-022, which spec-compliance correctly flags as NOT MET; (2) I didn't raise logging, which functional-architect correctly identifies as a pattern violation.

**Final P1 list**: str.replace fix, source map return, FR-003 multi-template (minimal callback).
**Final P2 list**: Boolean coercion, disambiguation warning, string enum validation, GapFillRefused exception, constraint gap-filling, logging.
**Final P3 list**: problem.md parser, template ranking, mode override test.
