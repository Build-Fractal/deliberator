# Cross-Review: game-engine-advocate Round 2 Review

**Cross-reviewer**: integration-architect
**Reviewing**: game-engine-advocate Round 2 review
**Date**: 2026-03-21

---

## Dangerous Contradictions

### DC-1: The docstring specificity request for ValidationConfig subtly reintroduces the coupling it claims to avoid

game-engine-advocate's R1 asks that the `ValidationConfig` docstring specify not just "spec 007 may extend this model" but concretely: "Anticipated extensions include `known_plugin_variables: frozenset[str]` for declaring plugin-contributed variables that should not be flagged as unknown by the linter."

game-engine-advocate frames this as "documentation only" and "costs nothing." This understates the commitment. Writing a specific field name, type, and semantic description into a docstring creates a de facto contract. A spec 007 implementer reading that docstring will treat `known_plugin_variables: frozenset[str]` as the blessed design, even if spec 007's actual needs turn out to require something different -- perhaps `plugin_schema: PluginVariableRegistry` that carries not just names but types, defaults, and validation rules. The docstring would then be either misleading (if left unchanged) or a source of unnecessary coordination cost (if someone feels obligated to update spec 005's docstring when spec 007's design diverges).

This contradicts game-engine-advocate's own governing principle (A1): "spec 005 optimizes for correctness of the current system; spec 007 designs extension mechanisms with full knowledge of the frozen foundation." A docstring that prescribes spec 007's field name and type is spec 005 reaching into spec 007's design space. The synthesizer's original formulation -- "spec 007 may extend this model" -- is intentionally vague because the extension's shape is spec 007's decision to make.

**My position**: The docstring should say "spec 007 may extend this model with plugin-aware fields" (which is what the synthesis already specifies). It should not name a specific field, type, or semantic. game-engine-advocate's R1 is scope inflation dressed as documentation.

### DC-2: MO-2 (ModeSchema field-level extensibility) contradicts the freeze-first principle while claiming to support it

game-engine-advocate's MO-2 recommends documenting that `ModeSchema` fields may be added by downstream specs, with unknown fields handled gracefully via `extra = "ignore"` or a version-aware parser. game-engine-advocate acknowledges this is "documentation only -- no implementation change in spec 005."

But recommending `extra = "ignore"` on `ModeSchema` -- even as a future documentation note -- directly contradicts the unanimous convergence on `extra = "forbid"` as a safety net (Round 1 synthesis, R2 resolution, Convergence item 10). The synthesis explicitly lists `extra = "forbid"` on TemplateContext as a "NOT extension point" in P2-6. While `ModeSchema` is not `TemplateContext`, the same principle applies: strict validation catches typos and structural errors. If spec 007 needs new fields on `ModeSchema`, the correct approach is the same one the deliberation chose for everything else: add the fields explicitly to the model, not silently ignore unknown ones.

game-engine-advocate's R3 (recommending this be documented) would plant the idea that `extra = "ignore"` is an anticipated direction for `ModeSchema`, creating normative pressure toward a pattern the entire deliberation rejected for core models. This is the `extra = "allow"` argument (GE-2, withdrawn in Round 1) reappearing through a side door.

**My position**: If P2-6 documents `ModeSchema` extensibility, it should say "downstream specs may add typed fields to `ModeSchema` by modifying the Pydantic model definition" -- the same pattern as every other model extension. It should NOT suggest `extra = "ignore"` as an approach.

---

## Tensions

### T-1: Scope of "documentation only" recommendations

game-engine-advocate characterizes all 4 of its new Round 2 recommendations as "documentation refinements to existing synthesis deliverables, not new implementation requirements. Total new implementation cost: zero lines of code in spec 005." This is technically true but elides the real cost: documentation in a spec creates normative expectations for implementers. Spec text is not commentary -- it is instruction.

R1 (docstring prescribing a specific field) and R3 (documenting `extra = "ignore"` as an option) both shape spec 007's design space in ways their "zero cost" framing conceals. R2 (documenting `PHASE_CONTEXT_MODELS` extensibility) and R4 (schema version compatibility deferral note) are genuinely low-cost documentation additions. The tension is that game-engine-advocate applies a uniform "zero cost" label to items with materially different normative weight.

I agree that documentation is important. I disagree that all documentation is equal in consequence.

### T-2: PHASE_CONTEXT_MODELS extensibility documentation (MO-1/R2) -- agreement on substance, disagreement on urgency

game-engine-advocate's R2 asks that `PHASE_CONTEXT_MODELS` be explicitly listed as an extensible registry in P2-6. The reasoning is sound: FT-8 was unanimously withdrawn specifically because this is a registry spec 007 needs to extend, and that decision is not currently captured in the P2-6 specification.

I agree this is a gap in P2-6. My own review does not address it because I focused on integration pathway gaps rather than registry documentation gaps. The question is whether this belongs in P2-6 (game-engine-advocate's position) or can be addressed when spec 007 actually needs the extension (my instinct). Given that P2-6 already exists as a deliverable and adding one sentence costs nothing, I lean toward agreement. But the urgency is lower than game-engine-advocate implies -- no one is going to re-add `Final` to `PHASE_CONTEXT_MODELS` without checking the deliberation record.

### T-3: Schema version compatibility deferral (MO-3/R4) vs. my own position on versioning

game-engine-advocate's R4 recommends adding a note that schema version compatibility checking is deferred to the spec that introduces version 2.0. My own review does not address schema version compatibility directly, but I endorsed P2-4 (schema versioning) in Round 1 specifically on the grounds that versioning should precede the first schema evolution. game-engine-advocate's recommendation is consistent with this: establish the version field now, defer the compatibility validation logic to when it is needed. No tension here -- this is a clean sequencing of concerns.

### T-4: My reverse template check (Rec 2) and game-engine-advocate's silence on it

My Round 2 review proposes a reverse template existence check (templates on disk but not in mode schema are flagged). game-engine-advocate does not address this in its review, despite the game engine being the most likely source of new template files. This is not a contradiction -- game-engine-advocate simply focused on different concerns. But it is worth noting: if the game engine introduces new template types via plugins, the reverse template check becomes a plugin integration concern, not just a "pit of success" linter improvement. game-engine-advocate's silence suggests this is not on the game engine's radar, which may indicate it is genuinely low-priority for spec 007's use cases.

---

## Safe Agreements

### SA-1: The synthesizer's resolutions on Disputes 2, 3, and 4 are correct and fully closed

game-engine-advocate and I both accept the synthesizer's resolutions on Dispute 2 (no `dict[str, Any]`), Dispute 3 (`str` with registry for `error_type`), and Dispute 4 (import fix as part of P1). These disputes are genuinely resolved. Neither review reopens them or introduces residual concerns.

### SA-2: The "freeze first, compose later" principle governs both reviews

game-engine-advocate explicitly reaffirms this as "the governing principle for my Round 2 positions" (A1). My review applies the same principle implicitly throughout -- every recommendation I make (SKILL.md invocation pathway, reverse template check, ROUND_SYNTHESES comment fix, filename-phase constraint documentation, validate_templates evolution path) operates within spec 005's frozen foundation and does not pre-commit to spec 007 design decisions.

### SA-3: P1-4 (ConfigCondition model) and P2-6 (extension contract documentation) are the most valuable deliverables for downstream specs

game-engine-advocate (A6, A7) and I (Alignment section, Convergence endorsements) both identify these two items as load-bearing for spec 006 and spec 007 respectively. game-engine-advocate correctly observes that `ConfigCondition` establishes the precedent that "extension mechanisms use typed models, not untyped dicts" -- this aligns precisely with my own position throughout the deliberation.

### SA-4: All Round 1 concessions are maintained without reversal by both reviewers

game-engine-advocate maintains all 7 Round 1 concessions. I maintain all 5 Round 1 concessions. Neither reviewer attempts to reopen settled positions. This confirms the deliberation's stability.

### SA-5: The Round 1 synthesis is well-grounded and does not introduce new ideas or mischaracterize positions

game-engine-advocate's OB-1 section explicitly states "the Round 1 synthesis is well-grounded" and "the synthesizer did not introduce new ideas or mischaracterize any agent's position." My review reaches the same conclusion implicitly by engaging with the synthesis's resolutions on their merits rather than challenging their characterizations.

### SA-6: P2-1 (MODE_PRESENCE as YAML declarations) eliminates a major maintenance burden

game-engine-advocate (A6, referencing the `ConfigCondition` precedent) and I (Alignment section, calling the 28-entry hardcoded dict "the single largest maintenance burden in the linter") both treat the MODE_PRESENCE migration as high-value. The convergence on this item was unanimous in Round 1 and remains so.

### SA-7: Schema version field at P2 is correctly sequenced

game-engine-advocate's R4 and my Round 1 position both support establishing the version field before spec 006's schema evolution. We agree that the version field should exist before the first schema change, and that compatibility validation logic is a concern for when a second version is introduced.

---

## Summary

game-engine-advocate's Round 2 review is disciplined and well-structured. Of 4 new recommendations, 2 are safe additions to existing deliverables (R2 on PHASE_CONTEXT_MODELS, R4 on schema version deferral note), and 2 carry hidden normative weight that contradicts the deliberation's governing principles (R1 on ValidationConfig docstring specificity, R3 on ModeSchema `extra = "ignore"`). The review's characterization of all 4 as "zero implementation cost" is factually accurate for code but misleading for spec text, which shapes downstream design decisions.

The residual disagreement from Dispute 1 is now genuinely narrow: we agree on `ValidationConfig` without `known_plugin_variables`, and disagree only on whether the docstring should name a specific anticipated field. This is a minor point that the synthesizer can resolve straightforwardly.
