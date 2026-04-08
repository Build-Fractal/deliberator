# Spec Compliance Disputes

**Date**: 2026-03-24
**Inputs**: All 4 revisions

---

## Remaining Disputes

### Dispute 1: FR-003 implementation scope -- am I satisfied with the proposed fix?

Game-theorist and functional-architect argue P1 must include the `TemplateSelector` protocol, `InteractiveTemplateSelector`, `NonInteractiveTemplateSelector`, and the `template_selector` parameter on `construct_objective`. Schema-engineer argues P1 is the callback, P2 is the implementations.

The spec says: "When multiple templates are viable candidates, the parser MUST present them to the user with plain-language descriptions and ask for selection." This requires *presentation* and *selection*, not just a callback mechanism. Game-theorist and functional-architect's position fully satisfies the spec. Schema-engineer's position satisfies the contract but not the behavior.

**My position**: Side with game-theorist and functional-architect. P1 includes implementations. The ~30 lines of code for protocol + two implementations is trivial. Shipping a callback with no callers is not compliance.

### Dispute 2: LLMGapFiller -- P2 with spec clarification vs accepted gap

My revision has LLMGapFiller at P2 pending spec clarification on the FR-016/FR-022 conflict. Game-theorist and schema-engineer accept this. Functional-architect accepts this. The question is whether "pending spec clarification" means "we'll do it after clarification" or "we'll file it and maybe never do it."

**My position**: The FR-016/FR-022 conflict is real and must be resolved in the spec. The resolution should be: FR-016 applies to import-time dependencies; FR-022's LLMGapFiller accepts the LLM client as a runtime-injected dependency (callable or protocol). This is a spec amendment, not a spec clarification. Until the amendment is made, LLMGapFiller is P2 with a clear path to implementation.

### Dispute 3: Retry test -- P2 or P3?

Schema-engineer maintains P3. My revision maintains P2. The argument: FR-007 is a MUST requirement. The implementation exists but has no test. An untested MUST is a regression risk. If the retry code is accidentally deleted or broken, no test catches it.

I acknowledge schema-engineer's point about engineering bandwidth -- the four P1s and other P2s are higher priority. But within the P2 tier, the retry test is important because it's the *only* verification of a MUST requirement.

**My position**: P2, but explicitly lower priority than the other P2 items (GapFillRefused, boolean coercion, logging). If bandwidth is limited, this is the last P2 to be implemented.

## Convergence

### C-1: Four P1 items are locked

The process has produced unanimous agreement on four P1 items. No revision or dispute challenges any of them:
1. **Source map return**: `FilledParameters` frozen dataclass from `fill_parameter_gaps`
2. **str.replace fix**: Regex word-boundary substitution in `_substitute_symbolic_form`
3. **FR-003**: `TemplateSelector` protocol + implementations + parameter
4. **FR-020**: `SourceProvenance` Pydantic model with required `problem_md`

### C-2: The str.replace vs boolean coercion priority question is resolved

All reviewers agree: str.replace is P1 (active risk), boolean coercion is P2 (latent risk with no current trigger). The cross-review process successfully distinguished between "bugs that can produce wrong output now" and "bugs that will produce wrong output when a new parameter type is used."

### C-3: LLMGapFiller deferred by unanimous consent

All four revisions accept that LLMGapFiller is P2, pending spec amendment to resolve the FR-016/FR-022 dependency conflict. The GapFiller protocol is infrastructure-ready for the implementation.

### C-4: Architecture praised by all four reviewers

The three-stage pipeline, frozen intermediates, GapFiller protocol, and pure-function design are unanimously endorsed. No architectural changes proposed. All fixes are targeted refinements.

### C-5: Spec-compliance gaps are acknowledged, not ignored

FR-009, FR-014, FR-022, SC-002 -- all four NOT MET / PARTIALLY MET items from my original review are now acknowledged by all reviewers. The disagreement was on *priority*, not on whether the gaps exist. The process moved these from "P1 blockers" to "P2 with clear implementation paths," which is appropriate for a pipeline that is architecturally sound and functionally correct for the implemented scope.

---

## Final Position

### Non-Negotiables
1. FR-003 P1 must include implementations, not just the callback. The spec uses MUST.
2. LLMGapFiller must have a clear implementation path (spec amendment + injected dependency design), not be permanently deferred.
3. The four P1 items are non-negotiable as a unit. They represent the minimum viable compliance fix set.

### Flexibility
- I can accept P2 or P3 for the retry test if the other P2 items are prioritized first.
- I can accept any `problem_md` value strategy (sentinel, constant, caller-provided) as long as the field is required.
- I can accept P3 for constraint wiring -- game-theorist's argument about construction vs execution scope is convincing.
- I accept that SC-002 depends on LLMGapFiller and cannot be meaningfully tested before it exists.
