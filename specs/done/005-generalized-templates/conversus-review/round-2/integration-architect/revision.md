# Integration Architect Revision -- Round 2

**Reviewer**: integration-architect
**Spec**: `005-generalized-templates`
**Round**: 2 of 2 (post-cross-review revision)
**Date**: 2026-03-21

---

## Recommendation Dispositions

### Rec 1: Update SKILL.md `allowed-tools` for linter invocation (P2)

**Original position**: Add a spec note specifying `uv run python linter/validate.py --mode {mode}` as the invocation mechanism and update SKILL.md `allowed-tools`.

**Disposition**: WITHDRAWN.

Both cross-reviewers identified a real problem. functional-typing's DC-1 is the sharper critique: I simultaneously endorse the programmatic API (P1-2) as the canonical decoupled interface and then recommend solving the invocation problem by shelling out to the CLI entry point -- which means the primary consumer never exercises the decoupled property that P1-2 was designed to achieve. game-engine-advocate's DC-1 adds that P2-8 (`[project.scripts]` entry point) will change the invocation surface, making a spec note about `uv run python linter/validate.py` immediately stale.

functional-typing correctly identifies the root cause: the SKILL.md invocation pathway is a spec 008 concern (executable conversus), not a spec 005 concern. Spec 005 delivers the library API. Spec 008 defines how the orchestrator calls it. Labeling this P2 in spec 005 is scope inflation -- the exact pattern Round 1 corrected in game-engine-advocate's original recommendations. I should have recognized this from my own analysis. Withdrawn without replacement.

### Rec 2: Add reverse template existence check to the linter (P3)

**Original position**: Iterate `templates/{mode}/*.md` and flag any template file not declared in the mode schema's `templates` list.

**Disposition**: MAINTAINED, with priority adjustment consideration.

game-engine-advocate's T-1 raises a valid point: when P2-1 ships and the mode schema `templates` list becomes the authoritative declaration, orphaned templates represent templates the orchestrator will never load. This strengthens the case for the check but argues for bundling it with P2-1 rather than deferring to P3. I accept this reasoning -- the reverse check is logically part of making the `templates` list authoritative. If the synthesizer bundles it with P2-1, I support that. If P2-1's scope is already too large, P3 remains defensible.

functional-typing's DC-2 identifies a subtlety I missed: the reverse template check (MO-2) and the filename-phase constraint (Rec 4) could conflict when a template file exists, IS listed in the mode schema, but has a filename that does not match a known phase name. The resolution functional-typing proposes -- validate the mode schema `templates` list entries against known phase names -- is the correct bridging validation. I incorporate this: the reverse template check should also verify that every entry in the mode schema `templates` list corresponds to a recognized phase name. This makes MO-2 and Rec 4 reinforcing rather than conflicting.

### Rec 3: Fix `ROUND_SYNTHESES` comment in models.py (P3)

**Original position**: Change the comment from "newline-separated paths" to "pre-formatted synthesis content per round" and exclude from P1-3 PathList conversion.

**Disposition**: MAINTAINED.

Both cross-reviewers either endorse or do not challenge this recommendation. game-engine-advocate's T-2 agrees it is sound and P3-appropriate. functional-typing's T-1 raises the broader question of whether a systematic audit of all model field comments against their schema declarations should accompany P1-3. I agree this is a good observation, but I maintain the point fix is the correct deliverable for spec 005. A systematic audit is implementation hygiene during P1-3 execution, not a separate spec deliverable. The implementer of P1-3 should verify each field's schema type before applying PathList -- that is due diligence, not a spec requirement.

### Rec 4: Document filename-phase constraint in Extension Points (P2-6 addendum)

**Original position**: Document in P2-6 that "template filenames must match phase names exactly" and that "variant templates for the same phase must use conditional blocks within a single template, not separate files."

**Disposition**: MODIFIED. Document the constraint. Remove the prescription.

game-engine-advocate's DC-2 correctly identifies that prescribing conditional blocks as the mandated workaround oversteps spec 005's authority. The Round 1 synthesis's S1 principle says spec 005 freezes the foundation; spec 007 designs extensions with full knowledge of that foundation. Documenting the constraint ("filenames currently map 1:1 to phases; the linter's `phase = tmpl_path.stem` pattern depends on this") is correct and useful. Prescribing how future specs must work around the constraint ("must use conditional blocks") is spec 005 reaching into spec 007's design space.

**Revised action**: P2-6 should state: "Template filenames map 1:1 to phase names (`phase = tmpl_path.stem`). This is a load-bearing assumption in the linter. Downstream specs that need per-phase variants should be aware that introducing multiple template files for a single phase would require linter changes."

### Rec 5: Note `validate_templates` evolution path in Extension Points (P2-6 addendum)

**Original position**: Document that `validate_templates` may evolve from boolean to structured config, with the boolean form remaining valid for backward compatibility.

**Disposition**: MODIFIED. Weaken the commitment.

functional-typing's T-3 correctly identifies that pre-committing to backward compatibility of the boolean form ("the boolean form must remain valid") contradicts the "freeze first" principle. This constrains the structured form to a union type (`bool | ValidateTemplatesConfig`), which is a Pydantic antipattern. game-engine-advocate's T-3 adds a YAGNI concern: documenting a speculative evolution path for a field with exactly one consumer and one behavior (on/off) is low-value.

I accept both critiques. The revised formulation should be observational, not prescriptive.

**Revised action**: P2-6 should state: "The `validate_templates` field is boolean in v1. Granular validation control (per-mode, per-check-type) is a potential future concern but is not designed here." No backward-compatibility commitment. No shape suggestion.

---

## New Recommendations

### New Rec A: Validate mode schema `templates` entries against known phase names (P3)

**Context**: Emerged from functional-typing's DC-2, which identified a gap between MO-2 (reverse template check) and Rec 4 (filename-phase constraint). The mode schema `templates` list could declare a template name that does not correspond to any known phase, and no validation currently catches this.

**Action**: When validating mode schemas, check that each entry in the `templates` list is a recognized phase name (i.e., exists in the set of phases that the linter knows how to validate). This bridges the reverse template check (MO-2/Rec 2) and the filename-phase constraint (Rec 4) into a single coherent validation chain: (1) every template on disk must be declared in the schema, (2) every declaration in the schema must correspond to a recognized phase, (3) every recognized phase must have a template on disk.

**Priority**: P3. This is a "pit of success" validation that catches errors early. It becomes higher priority if the reverse template check is bundled with P2-1.

### New Rec B: Resolve `error_type` validator behavior -- reject vs. warn (P1-2 implementation detail)

**Context**: functional-typing's T-4 (on my review) and DC-1 (on my cross-review of functional-typing) identify a genuine ambiguity. I accepted the synthesizer's Dispute 2 resolution without specifying whether the `@field_validator` should reject unknown error types or warn-and-accept. functional-typing proposes warn-and-accept for plugin extensibility. I argued in my cross-review that warn-and-accept breaks the pattern consistency with mode validation and defeats typo-catching.

**Action**: The synthesizer should resolve this explicitly. My position is: reject unknown types at construction time, matching the mode validation pattern. Plugin-contributed `check_*` functions that introduce new error types must register them in `KNOWN_ERROR_TYPES` before constructing `LintError` instances -- the same pattern as mode registration. This maintains pattern consistency (one validation pattern for all extensible sets) and catches typos.

**Priority**: Implementation detail of P1-2, not a separate deliverable. But the synthesizer should state the behavior to prevent divergent implementations.

---

## Position Summary

| Item | Original Position | Disposition | Revised Position |
|---|---|---|---|
| Rec 1: SKILL.md linter invocation pathway | P2 | WITHDRAWN | Scope belongs to spec 008, not spec 005 |
| Rec 2: Reverse template existence check | P3 | MAINTAINED | P3 standalone, or bundled with P2-1 at synthesizer's discretion |
| Rec 3: Fix ROUND_SYNTHESES comment | P3 | MAINTAINED | No change |
| Rec 4: Document filename-phase constraint | P2-6 addendum | MODIFIED | Document the constraint; remove the prescription on how future specs must handle variants |
| Rec 5: Document validate_templates evolution | P2-6 addendum | MODIFIED | Observational note only; no backward-compatibility commitment, no shape suggestion |
| New Rec A: Validate templates against phase names | -- | NEW | P3 bridging validation between Rec 2 and Rec 4 |
| New Rec B: error_type validator rejects unknown types | -- | NEW | Synthesizer should specify; my position is reject, matching mode validation |

### Concessions

All 5 concessions from Round 1 are maintained without reversal:
1. MODE_PRESENCE endorsement retraction
2. Loader purity retraction
3. ConfigCondition typing upgrade
4. plugin_data withdrawal
5. Schema version upgrade

Rec 1 withdrawal is a new Round 2 concession: functional-typing and game-engine-advocate correctly identified it as scope inflation into spec 008's domain.

### Governing Principles

The cross-reviews reinforced three principles that guided my revisions:

1. **Freeze first, compose later** (S1). Rec 4 and Rec 5 originally violated this by prescribing future design choices. Both are now modified to document constraints without prescribing solutions.

2. **Spec 005 scope boundary**. Rec 1 violated this by pulling a spec 008 concern (orchestrator invocation pathway) into spec 005. Withdrawn.

3. **Pattern consistency over local optimization**. New Rec B applies this to the `error_type` validator: one validation pattern (reject unknown, register new entries) for all extensible sets (modes, error types). Warning-only validation for error types while rejecting for modes would create a gratuitous inconsistency.

### Final Assessment

The cross-reviews were effective. Of my 5 original recommendations, 1 was correctly identified as scope inflation and withdrawn, 2 were correctly identified as overly prescriptive and modified to be descriptive, and 2 were maintained. The 2 new recommendations that emerged from cross-review synthesis (phase-name validation bridging, error_type behavior specification) are both narrow, well-justified, and close genuine gaps rather than expanding scope. The deliberation is converged.
