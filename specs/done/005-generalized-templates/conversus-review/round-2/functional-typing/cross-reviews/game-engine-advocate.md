# Cross-Review of game-engine-advocate (Round 2)

**Reviewer**: functional-typing
**Reviewing**: game-engine-advocate Round 2 review
**Round**: 2 of 2
**Date**: 2026-03-21

---

## Dangerous Contradictions

### DC-1: The `@field_validator` on `error_type` cannot simultaneously "validate against a known registry" and permit plugin-contributed types

game-engine-advocate accepts the synthesizer's Dispute 2 resolution (A3) -- `str` with `@field_validator` checking against `KNOWN_ERROR_TYPES` -- and describes it as "checking against this set" while also noting that "plugin validators producing `LintError(error_type="invalid_objective_schema")` need a runtime-open type." These two statements are in tension.

If the `@field_validator` raises `ValueError` for unknown types (standard Pydantic validation behavior), then a plugin returning `LintError(error_type="invalid_objective_schema")` will be rejected at construction -- recreating the `Literal` problem in runtime form. If it does not reject, then it is not "validating against" the registry in any meaningful sense.

My own Round 2 review (Dispute 2 Refinement) addresses this directly: I propose the validator issues a **warning** for unknown types rather than raising `ValueError`. game-engine-advocate's review does not address validator strictness at all, which means the resolution game-engine-advocate accepts is ambiguous on the exact point that matters for plugin extensibility.

This is not a contradiction between game-engine-advocate's position and mine -- we agree on the outcome (`str`, open to plugins). It is a contradiction within game-engine-advocate's acceptance: the review simultaneously endorses "validation against a known registry" and "runtime-open type for plugins" without specifying how the validator reconciles these. The reconciliation matters for implementation.

**Risk**: An implementer reading only game-engine-advocate's acceptance could build a strict validator that rejects plugin error types, defeating the purpose of the `str` choice. My warning-based validator proposal resolves this, but game-engine-advocate neither endorses nor engages with it.

**Severity**: Moderate. The underlying agreement exists; the implementation guidance is missing.

### DC-2: R1 docstring specificity recommendation (game-engine-advocate) vs. the "freeze first, compose later" principle (also game-engine-advocate)

game-engine-advocate's strongest Round 2 position is R1: the `ValidationConfig` docstring should specify the anticipated extension as `known_plugin_variables: frozenset[str]`. game-engine-advocate simultaneously reaffirms the "freeze first, compose later" principle (A1) as the governing principle for Round 2 positions.

These are in mild tension. The "freeze first, compose later" principle means spec 005 defines the frozen foundation; spec 007 designs the extension mechanisms. Embedding a specific anticipated parameter name and type signature (`known_plugin_variables: frozenset[str]`) in spec 005's docstring is a form of composing before freezing -- it commits spec 005 to a specific extension shape that spec 007 has not yet designed. What if spec 007 discovers that the right extension is not a simple frozenset of variable names but a more structured `PluginVariableRegistry` that carries metadata? The docstring would then be misleading.

game-engine-advocate's own Round 1 trajectory -- conceding 7 of 10 recommendations as scope inflation -- was driven precisely by this pattern: encoding spec 007 assumptions into spec 005. R1's docstring recommendation is a milder form of the same pattern.

The synthesizer's resolution ("spec 007 may extend this model") is deliberately vague because the extension shape is a spec 007 design decision. Sharpening the docstring to a specific parameter name narrows the design space without spec 007's input.

**Risk**: Low. A docstring is trivially changed. But the reasoning pattern -- "I concede the implementation but encode the intent in documentation" -- is worth flagging because it applies the same scope-inflation impulse to prose instead of code.

**Severity**: Low. The recommendation itself is harmless. The reasoning pattern is the concern.

---

## Tensions

### T-1: game-engine-advocate's MO-1 (`PHASE_CONTEXT_MODELS` in P2-6) vs. my OBA-2 (condition field's relationship to `config_conditions`)

game-engine-advocate's MO-1 asks P2-6 to document `PHASE_CONTEXT_MODELS` as an explicitly extensible registry. My OBA-2 asks P3-5 to clarify the relationship between the free-text `condition` field and the typed `config_conditions` model from P1-4.

These are not contradictory, but they reveal a broader tension: P2-6 (extension contract documentation) is accumulating responsibilities from multiple agents. game-engine-advocate adds `PHASE_CONTEXT_MODELS` extensibility. My review adds the `condition`/`config_conditions` relationship. If every agent loads their deferred concerns into P2-6, it becomes a catch-all document rather than a focused extension contract.

The tension is about P2-6's scope discipline: should it document only the extension/non-extension points (as the synthesizer specified), or should it also absorb registry-level implementation guidance and field-level semantic clarifications? game-engine-advocate's MO-1 is defensible (it is genuinely about extensibility), but MO-2 and MO-3 start to stretch P2-6's scope.

**Resolution path**: P2-6 should contain two categories: (1) extension points (where downstream specs add things) and (2) non-extension points (where they must not). `PHASE_CONTEXT_MODELS` belongs in category 1. ModeSchema field-level extensibility (MO-2) and schema version compatibility (MO-3) are implementation guidance that belongs in spec 007's design phase, not spec 005's extension contract.

### T-2: game-engine-advocate's MO-2 (`ModeSchema` field extensibility) vs. the existing `extra = "forbid"` consensus

game-engine-advocate's MO-2 notes that `ModeSchema` uses Pydantic's default behavior (which, under the consensus, means `extra = "forbid"`) and suggests that P2-6 should document how unknown fields should be handled -- either `extra = "ignore"` or version-aware loading.

This is in tension with the unanimous consensus on `extra = "forbid"` for core models. The suggestion to consider `extra = "ignore"` on `ModeSchema` would be the first exception to the "forbid on all core models" rule. game-engine-advocate correctly frames this as documentation, not implementation -- but documenting that an exception "may" be needed plants the seed for the exception.

From a type-safety perspective, `extra = "ignore"` silently swallows typos in mode schema YAML files, which is the exact failure mode that `extra = "forbid"` prevents. The better pattern, consistent with the deliberation's consensus, is: spec 007 adds its fields to `ModeSchema` explicitly (via a subclass or model update), and `extra = "forbid"` continues to catch errors. This is how `TemplateContext` extension works (via `PluginContext` composition), and there is no reason `ModeSchema` should follow a different pattern.

### T-3: game-engine-advocate's "zero new lines of code" framing vs. the implementation implications of the docstring recommendation

game-engine-advocate frames all Round 2 recommendations as "documentation refinements" with "total new implementation cost: zero lines of code." This is technically true but slightly misleading regarding R1 (the docstring recommendation). A docstring that specifies `known_plugin_variables: frozenset[str]` as the anticipated extension has implementation weight: it creates an implicit contract that spec 007 implementers will reference. If the contract is wrong, it must be corrected, which is a coordination cost.

The tension is between "zero cost" framing and the actual cost of maintaining documentation-as-contract. This is not a significant concern -- docstrings are cheap to update -- but the "zero cost" claim understates the commitment that a specific parameter name in a docstring creates.

---

## Safe Agreements

### SA-1: The "freeze first, compose later" principle is correctly identified as the governing resolution

game-engine-advocate's A1 and my own review both affirm this principle. It emerged from the Round 1 cross-review process and correctly governs the boundary between spec 005 and spec 007. This is the most important intellectual output of the deliberation, and both reviews treat it as settled. The Round 1 dispute resolutions hold because they flow from this principle.

### SA-2: All four Round 1 dispute resolutions are accepted

game-engine-advocate accepts Disputes 2, 3, and 4 without reservation and narrows Dispute 1 to a docstring concern. My review accepts all four without reservation (with a refinement on Dispute 2's validator behavior). Neither review reopens any resolved dispute. The Round 1 synthesis is stable.

### SA-3: The `ValidationConfig` Pydantic model is the correct API pattern

game-engine-advocate (A1, Dispute 1 engagement) and my review (Dispute 1 Confirmation) both endorse `ValidationConfig` as superior to bare parameters. game-engine-advocate correctly identifies it as the forward-compatibility mechanism. My review adds three specific type-safety properties (named fields, construction validation, serialization). We arrive at the same conclusion from different analytical lenses, which strengthens the recommendation.

### SA-4: `PHASE_CONTEXT_MODELS` should not be `Final`

game-engine-advocate's MO-1 and the Round 1 convergence item 6 both confirm this. My Round 1 review withdrew FT-8 (`Final` on `PHASE_CONTEXT_MODELS`) based on game-engine-advocate's registry argument. game-engine-advocate now asks for explicit documentation of this decision in P2-6 to prevent future regression. This is a reasonable request -- the withdrawal was unanimous but undocumented outside the deliberation artifacts. Including `PHASE_CONTEXT_MODELS` in P2-6's extension points list costs one sentence and prevents a future implementer from re-adding `Final`.

### SA-5: The convergence scorecard is accurate and the process produced genuine intellectual movement

game-engine-advocate's A5 and my own review both confirm the scorecard's accuracy. game-engine-advocate explicitly accepts the "largest positional shift" characterization without defensiveness. This kind of transparent self-assessment validates the deliberation process. The fact that 7 of 10 recommendations were conceded as scope inflation -- and that this concession held through Round 2 without reversal -- demonstrates that the Round 1 process applied genuine corrective pressure.

### SA-6: P1-4 (`ConfigCondition` model) is correctly designed

game-engine-advocate's A6 and my review's endorsement of P1-4 are aligned. game-engine-advocate frames it as precedent-setting ("extension mechanisms use typed models, not untyped dicts"), which is the same conclusion my review reaches from a type-safety lens. The typed `ConfigCondition` model with `field: str` and `value: str` is the correct granularity for spec 006's needs while establishing the pattern for spec 007's future conditions.

### SA-7: P2-6 (extension contract documentation) is the most valuable non-code deliverable

game-engine-advocate calls P2-6 "the single most valuable non-code deliverable in spec 005 for spec 007's benefit" (A7). My review does not make this explicit ranking but consistently references P2-6 as the coordination mechanism between specs. We agree on its importance, even if we differ on its scope (see T-1 above).

### SA-8: All Round 1 concessions are maintained without reversal

game-engine-advocate explicitly lists all 7 Round 1 concessions as maintained. My review maintains all Round 1 concessions (FT-3 withdrawal, FT-8 withdrawal, FT-5 modification, itertools.chain withdrawal, FT-7 deferral). Neither review attempts to re-litigate settled positions. This confirms the stability of the Round 1 synthesis.

---

## Summary Assessment

game-engine-advocate's Round 2 review is well-disciplined and demonstrates genuine acceptance of the Round 1 resolutions. The review narrows rather than expands the remaining disagreements, which is the correct behavior for a final round. The three new recommendations (MO-1, MO-2, MO-3) are all documentation items with no implementation cost, consistent with the "freeze first, compose later" principle.

The two dangerous contradictions I identify are moderate-to-low severity. DC-1 (validator strictness ambiguity) is the more substantive concern because it affects implementation behavior, but the underlying agreement on `str` for `error_type` is clear. DC-2 (docstring specificity as mild scope inflation) is a reasoning-pattern concern, not a substantive disagreement.

The Round 1 dispute resolutions hold. No new blocking issues have emerged.
