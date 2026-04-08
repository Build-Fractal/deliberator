# Spec Compliance Revision

**Date**: 2026-03-24
**Inputs**: Phase 1 review, 3 cross-reviews received (from game-theorist, schema-engineer, functional-architect), 3 cross-reviews written (of game-theorist, schema-engineer, spec-compliance)

---

## Recommendation Dispositions

### R1: Implement multi-template user selection (FR-003)
**Status: SURVIVING (P1)**

All four reviewers now agree FR-003 is P1. Game-theorist upgraded in their revision after accepting the MUST argument. The minimal fix (default `template_selector` callback on `construct_objective`) is the right incremental approach, with full interactive presentation as a follow-up.

### R2: Add `problem_md` path to `AssembledObjective.source` (FR-020)
**Status: MODIFIED (P1, adopt SourceProvenance model)**

Schema-engineer's `SourceProvenance` model is the cleanest implementation. I accept the nested model approach over my original "add problem_md to the flat dict" proposal. The `problem_md` field should be *required* (not optional), with a sentinel `"<stdin>"` for programmatic use. Schema-engineer's `Literal` typing on `filled_by` values is a good addition.

### R3: Implement `conversus.yml` objective field (FR-014)
**Status: MODIFIED (P2, downgraded from P1)**

Functional-architect's cross-review makes a valid point: modifying `conversus.yml` is an orchestration/integration concern, not a construction pipeline concern. The pipeline's job is to produce a valid `AssembledObjective` and optionally serialize it. Writing to `conversus.yml` should happen in the CLI layer or a higher-level integration function that calls `construct_objective`. The pipeline should not need to know `conversus.yml`'s schema.

Downgraded to P2, reframed: provide a utility function `register_objective_in_config(objective_path, config_path)` that can be called by the CLI integration layer. Don't put it inside `construct_objective`.

### R4: Implement `LLMGapFiller` (FR-022)
**Status: MODIFIED (P2, downgraded from P1)**

Schema-engineer's cross-review identifies a spec conflict: FR-022 requires LLMGapFiller, but FR-016 requires "no extra dependencies beyond pydantic/pyyaml." An LLMGapFiller needs an LLM client library. The resolution: LLMGapFiller should accept an LLM client as an *injected dependency* (a callable or protocol), so the class itself has no import-time dependency on any LLM library. This makes it a protocol consumer, not a library dependent.

However, this is a design decision that requires spec clarification. Downgraded to P2 pending that clarification. The GapFiller protocol is already designed for pluggability, so the infrastructure is in place.

### R5: Add `gap_fill_model` config surface (FR-009)
**Status: MODIFIED (P2, bundled with R4)**

FR-009 is meaningless without FR-022 (LLMGapFiller). The config key should be added alongside the LLMGapFiller implementation. Bundled with R4 at P2.

### R6: Add retry/re-ask test (FR-007)
**Status: SURVIVING (P2)**

No pushback. The implementation exists; the test doesn't. P2 is warranted because FR-007 is a MUST requirement and the test is the only proof of compliance.

### R7: Add SC-002 natural-language mapping test
**Status: MODIFIED (P3, deferred pending LLMGapFiller)**

SC-002 requires NLP interpretation of relative importance statements. This depends on the GapFiller implementation (specifically LLMGapFiller). Testing SC-002 before LLMGapFiller exists would require a mock that assumes the interpretation logic, which provides no real verification. Downgraded to P3, deferred until LLMGapFiller (R4) is implemented.

Game-theorist's cross-review and functional-architect's cross-review both argue SC-002 should be assessed against the filler, not the pipeline. I accept this reframing: the pipeline passes problem text to the filler; interpretation is the filler's job. SC-002 is NOT MET because the filler doesn't exist, but the pipeline is not the blocker.

### R8: Add explicit importability test (FR-015 / SC-005)
**Status: SURVIVING (P3)**

No strong pushback, but consensus is that it's a documentation gesture since every test imports the module. P3 is correct.

### R9: Add question contextualisation to `fill_parameter_gaps` (FR-005)
**Status: MODIFIED (P3, responsibility clarification)**

Functional-architect and game-theorist both argue that question contextualisation is the GapFiller's responsibility, not the pipeline's. The pipeline passes `problem_context` to the filler -- contextualising the question text is the filler's job (especially LLMGapFiller). I accept this reframing. FR-005 is PARTIALLY MET because the contextualisation mechanism exists (the `context` parameter) but no filler implementation uses it.

Downgraded to P3, reframed: improve contextualisation in GapFiller implementations, not in the pipeline.

### R10: Harden determinism test to cover YAML round-trip
**Status: SURVIVING (P3)**

No pushback. A YAML round-trip test would catch serialisation non-determinism. P3.

---

## New Recommendations

### NEW-1: Fix `_substitute_symbolic_form` substring collision (P1)
**Source**: Game-theorist R1, schema-engineer R3 -- both P1, confirmed by cross-reviews.

I didn't explicitly call this out as a separate recommendation in my review (I noted FR-012 determinism as MET). The deterministic *ordering* is correct, but the `str.replace` method is fragile. The regex word-boundary fix is trivial and addresses a real corruption risk. Adopted as P1.

### NEW-2: Return source map from `fill_parameter_gaps` (P1)
**Source**: All three other reviewers -- unanimous P1.

I identified the flat `source` dict as incomplete (FR-020) but didn't separately call out the data-loss bug where `fill_parameter_gaps` discards its internal source map. The reconstruction in `construct_objective` using value-comparison is fragile. Adopted as P1.

### NEW-3: Add `GapFillRefused` exception (P2)
**Source**: Schema-engineer P2, game-theorist P2 -- consensus across reviewers.

I didn't raise the RuntimeError pattern in my review. The custom exception defined alongside the GapFiller protocol is the clean fix. Adopted as P2.

---

## Position Summary

The cross-review process shifted my position significantly on three items: (1) FR-014 `conversus.yml` integration is the CLI layer's job, not the pipeline's (downgraded P1 to P2); (2) LLMGapFiller requires spec clarification on the FR-016 dependency conflict (downgraded P1 to P2); (3) SC-002 should be assessed against the filler, not the pipeline (downgraded P2 to P3).

Conversely, I adopted two P1 items from other reviewers that I missed: the str.replace collision and the source map data loss. These are bugs in the current code that I should have caught in my FR-by-FR analysis.

**Final P1 list**: FR-003 multi-template, FR-020 SourceProvenance, str.replace fix, source map return.
**Final P2 list**: FR-014 utility function, LLMGapFiller + gap_fill_model (bundled), retry test, GapFillRefused exception.
**Final P3 list**: SC-002 test (deferred), importability test, question contextualisation, YAML round-trip test.
