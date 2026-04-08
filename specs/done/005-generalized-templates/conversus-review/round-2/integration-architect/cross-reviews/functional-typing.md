# Cross-Review of functional-typing's Round 2 Review

**Cross-reviewer**: integration-architect
**Reviewing**: functional-typing Round 2 review
**Date**: 2026-03-21

---

## Dangerous Contradictions

### DC-1: Dispute 2 refinement (warning-only validation) contradicts the mode validation precedent it claims to follow

functional-typing accepts the synthesizer's resolution on Dispute 2 -- `str` with `@field_validator` checking against `KNOWN_ERROR_TYPES` -- and then proposes that the validator should issue a **warning** rather than raise `ValueError` for unknown types. The stated rationale is that unknown error types from plugin `check_*` functions mean "I don't recognize this yet," not "this is invalid."

This directly contradicts the mode validation precedent that functional-typing claims to mirror. The synthesizer's resolution on modes uses `@field_validator` that **rejects** unknown modes (a mode not in `VALID_MODES` is invalid). The synthesizer's Dispute 2 resolution explicitly says "mirroring the mode resolution" and "applying the same pattern to error types produces a coherent, predictable system." functional-typing endorses this coherence argument in its Alignment section ("the synthesizer's pattern-consistency argument ... is more architecturally coherent") and then immediately proposes breaking the pattern by downgrading rejection to a warning.

The underlying concern is legitimate: plugin-contributed `check_*` functions need to return errors with custom types. But the answer is the same as for modes -- the `KNOWN_ERROR_TYPES` set is extended at load time when plugins register, not bypassed via warning-only validation. A warning-only validator means `LintError` instances with typos in `error_type` (e.g., `"missing_variabel"`) silently pass through, which defeats the typo-catching purpose the synthesizer explicitly cited as integration-architect's concern being addressed.

**Severity**: Medium. The refinement is framed as minor, but if adopted it would make `error_type` validation semantically different from mode validation without justification, undermining the pattern-consistency principle that resolved the original dispute.

### DC-2: MO-1 (ValidationContext dataclass) introduces a second config-bundling pattern alongside ValidationConfig

functional-typing proposes a frozen `ValidationContext` dataclass to bundle schema-related parameters passed to `validate_template`, reducing its parameter count. This is proposed at P2, alongside the already-converged P1-2 `ValidationConfig` Pydantic model that bundles parameters for `validate_all`.

The result is two distinct parameter-bundling abstractions for the same validation pipeline:
- `ValidationConfig` (Pydantic model, external API boundary): bundles `root` and `mode` for callers of `validate_all`.
- `ValidationContext` (frozen dataclass, internal): bundles `variables_schema`, `mode_schema`, and `all_var_names` for internal `validate_template` calls.

functional-typing correctly notes that `ValidationContext` is "not a new Pydantic model (it's internal to the linter, not a schema artifact)" -- but the distinction between "external Pydantic model" and "internal frozen dataclass" for what are both parameter-bundling objects in the same call chain is a design-time burden. A reviewer encountering both will need to understand why one is Pydantic and the other is a dataclass, why one is frozen by `model_config` and the other by `@dataclass(frozen=True)`, and when to use which.

This is not necessarily wrong -- internal and external boundaries can legitimately use different patterns. But the Round 1 synthesis never surfaced this dual-abstraction question, and functional-typing does not address the coordination between them. If `validate_all` constructs a `ValidationContext` from its `ValidationConfig` to pass to `validate_template`, the two models have a dependency relationship that should be designed together, not introduced in separate priority tiers (P1 vs. P2).

**Severity**: Medium. Not a logical contradiction, but an architectural coordination gap that could produce a clumsy implementation if the two models are designed independently.

---

## Tensions

### T-1: OBA-1 ("non-breaking" qualification) is correct but applies to a resolved dispute

functional-typing's OBA-1 correctly notes that the synthesizer's reasoning -- "no external consumers means non-breaking" -- is imprecise. Adding parameters to `validate_template` without keyword-only enforcement WILL break existing tests. This is a valid technical observation.

However, the synthesizer's resolution (use `ValidationConfig` model) already handles this, as functional-typing acknowledges: "The `ValidationConfig` model is non-breaking because Pydantic models absorb new fields with defaults, not because there are no callers." The observation is correct, but the correction applies to the synthesizer's reasoning, not to the synthesizer's resolution. Since Round 2 is about evaluating resolutions rather than editing the synthesis document's prose, this observation has no actionable consequence. It reads as a precision correction on already-settled analysis.

I note this as a tension rather than an agreement because the underlying principle matters: "no external consumers" is not a general justification for breaking changes, and future specs should not cite it. functional-typing is right to flag this even though it changes nothing in the current scope.

### T-2: MO-2 (itertools.product in tests) sits in tension with functional-typing's own Round 1 withdrawal

In Round 1, functional-typing withdrew its `itertools.chain.from_iterable` optimization after integration-architect argued it "optimized concatenation of the wrong abstraction." The concession was recorded in the synthesis (Section 8, functional-typing concession #4). Now in Round 2, functional-typing proposes a different `itertools` usage (`itertools.product` in test case generators) at P3, citing Constitution Principle IX's FP guidance.

These are technically different proposals (one was about error aggregation, the other about test case generation), and the Round 1 withdrawal was about applying FP tools to production error handling, not test utilities. But the pattern of proposing itertools-based refactors across rounds, after having a similar proposal rebuffed, creates a tension: is this a distinct, well-justified recommendation, or is it relitigating the same aesthetic preference in a different venue?

I lean toward accepting it as distinct -- test case generators are genuinely a good fit for `itertools.product`, and P3 priority is appropriately modest. But the optics should be acknowledged.

### T-3: OBA-2 (condition field is documentation-only) overlaps with my MO-3 (ROUND_SYNTHESES type mismatch) as instances of a broader spec-implementation divergence pattern

functional-typing identifies that the `condition` field in `variables.yml` is prose documentation in the implementation but looks like a parseable expression in the spec. My review (MO-3) identifies that `ROUND_SYNTHESES` is declared as `extracted-content` in the schema but commented as "newline-separated paths" in the models. Both are instances of the same underlying issue: the spec and schema describe one thing, the implementation does another, and the linter does not validate the correspondence.

Neither review synthesizes these into a systemic observation. The Round 1 synthesis's P3-5 (formalize condition syntax) partially addresses functional-typing's finding, and my Rec 3 (fix ROUND_SYNTHESES comment) addresses mine, but a broader audit of schema-type-to-implementation-type correspondence would catch both and any others. This is not a contradiction between our reviews -- it is a missed opportunity to generalize.

---

## Safe Agreements

### SA-1: All four dispute resolutions are accepted without reversal

Both reviews accept the synthesizer's resolutions on all four disputes. Neither review reverses any Round 1 concession. This is the most important agreement: the deliberation's convergence is stable through Round 2.

### SA-2: P1-1 (purify schema-loading functions) is the highest-leverage change

functional-typing calls this "the single most important change for functional correctness." My review calls it "the single highest-leverage change." We agree on both the priority and the reasoning: every downstream integration depends on the linter being callable without side effects. The unanimity on this item across both rounds and all agents is the strongest signal in the deliberation.

### SA-3: ValidationConfig Pydantic model is the correct API boundary pattern

Both reviews endorse the synthesizer's `ValidationConfig` approach for Dispute 1. functional-typing provides the type-theoretic justification (named fields with defaults, validation at construction, serialization for testing). My review endorses it on integration grounds (stable extension surface). The convergence is from different analytical angles to the same conclusion.

### SA-4: P1-4 (ConfigCondition model) is correctly prioritized as P1

functional-typing endorses it implicitly through its OBA-2 analysis (connecting `config_conditions` to the `condition` field gap). My review explicitly ties it to spec 006's `PRIOR_ARBITRATION_PATH`. Both reviews agree this is a P1 item that enables downstream spec integration.

### SA-5: frozen=True on TemplateContext is architecturally correct

functional-typing (P2-5 endorsement) and my review (implicit via acceptance of all convergence items) agree that immutability on core context models with composition for plugin extensibility is the right design. The "freeze first, compose later" principle identified by the Round 1 synthesis holds.

### SA-6: OBA-2 (condition field analysis) and my ROUND_SYNTHESES finding are complementary

As noted in T-3, both reviews identify spec-implementation divergences in different locations. functional-typing's analysis is more thorough (connecting P1-4, P3-5, and the actual condition field values), while mine is narrower (single field, single fix). Both point toward the same need for systematic type-correspondence checking between schema declarations and model implementations.

### SA-7: The Round 1 process was effective and the synthesis is high quality

Both reviews open with explicit endorsement of the Round 1 synthesis quality. functional-typing: "a rigorous, well-traced resolution." My review: "high-quality synthesis." Neither review identifies structural flaws in the synthesis process or major errors in the converged items. The remaining work is execution and gap-filling, not re-litigation.
