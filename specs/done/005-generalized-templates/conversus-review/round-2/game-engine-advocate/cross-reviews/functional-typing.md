# Cross-Review of functional-typing's Round 2 Review

**Cross-reviewer**: game-engine-advocate
**Reviewing**: functional-typing Round 2 review
**Date**: 2026-03-21

---

## Dangerous Contradictions

### DC-1: The `@field_validator` warning-not-rejection proposal undermines the registry pattern it claims to support

functional-typing proposes (Dispute 2 Refinement) that the `@field_validator` on `LintError.error_type` should issue a **warning** for unknown types rather than raise `ValueError`. The stated rationale is that strict rejection "would force plugin authors to register their types in the core module before they can return errors -- recreating the `Literal` problem in runtime form."

This contradicts the very pattern both agents accepted for modes. The `VALID_MODES` registry rejects unknown modes at validation time -- that is the point of the `@field_validator`. If mode validation rejected unknown modes but error-type validation merely warned, the system would have two semantically identical registries with opposite enforcement behaviors. A plugin author encountering this would reasonably ask: "Why does my custom mode get rejected but my custom error type gets silently warned?" The answer -- "because we think modes are more important than error types" -- is architecturally incoherent.

The correct resolution for plugin extensibility is the same for both registries: plugins register their extensions before producing values. For modes, a plugin registers a YAML file. For error types, a plugin registers its types into `KNOWN_ERROR_TYPES` at initialization. The registration mechanism is what spec 007 designs. A warning-only validator provides no typo protection (the primary use case for the registry) and creates a silent-failure path where a misspelled error type (`"misssing_variable"`) passes without detection.

functional-typing's concern about "recreating the `Literal` problem in runtime form" is unfounded. The `Literal` problem is that extending the set requires modifying source code and redeploying. A runtime `frozenset` can be extended programmatically at load time without source modification. The synthesizer's resolution already addresses this: "can be extended at load time." Warning-only validation is a weaker version of the same idea that loses the typo-catching benefit.

**Source**: functional-typing review, Dispute 2 Refinement (L44-52); Round 1 synthesis, Dispute 2 resolution (L214-227); my review, A3 (L31-34).

### DC-2: `ValidationContext` frozen dataclass duplicates and fragments the `ValidationConfig` model's role

functional-typing proposes (MO-1) a new `ValidationContext` frozen dataclass bundling `variables_schema`, `mode_schema`, and `all_var_names` as internal parameters to `validate_template`. This is positioned as distinct from `ValidationConfig` (the public API boundary) -- an "internal" dataclass that "reduces parameter passing."

This creates a dangerous architectural bifurcation. The Round 1 synthesis established `ValidationConfig` as the single configuration surface for the validation pipeline. functional-typing now proposes a second configuration object (`ValidationContext`) for internal plumbing, with a different construction path and different fields. When spec 007 adds plugin-variable awareness, it must now decide: does it extend `ValidationConfig` (the public surface) or `ValidationContext` (the internal plumbing)? The answer is "both" -- plugin variables affect both what the API accepts and what `validate_template` consults. Two configuration objects that must be kept in sync is a maintenance hazard that a single, well-structured `ValidationConfig` avoids.

The parameter-count concern is legitimate: `validate_template` taking 6+ parameters is unwieldy. But the solution is to derive `ValidationContext`-like state from `ValidationConfig` via a factory function, not to introduce a parallel configuration object. If `validate_all` constructs the schemas from `ValidationConfig` and passes them forward, the internal functions can receive the same `ValidationConfig` instance (or a derived view of it) without requiring a separate dataclass.

This is a genuine architectural risk, not a style preference. Two configuration objects with overlapping concerns is how systems accumulate "which config do I update?" bugs.

**Source**: functional-typing review, MO-1 (L69-85); Round 1 synthesis, Dispute 1 resolution (L198-211); my review, Dispute 1 engagement (L56-68).

---

## Tensions

### T-1: The `condition` field analysis (OBA-2) is correct but underweights the implication for P1-4

functional-typing correctly identifies (OBA-2) that the `condition` field in `variables.yml` contains prose documentation strings, not parseable expressions, despite the spec showing `condition: "rounds > 1"` as an apparently parseable form. The observation that `validate.py` never reads the `condition` field is factually accurate and valuable.

However, functional-typing's conclusion -- that P3-5 is "either redundant with P1-4 or complementary to it, depending on scope" -- underweights the tension. P1-4 introduces `config_conditions` as the typed, machine-readable mechanism for conditional variable requirements. If P1-4 is implemented correctly, the `condition` field in `variables.yml` becomes purely documentary. P3-5 (formalize condition syntax) would then formalize the documentation string, not the machine-readable condition -- which is a different kind of work than the Round 1 synthesis envisioned. The synthesis describes P3-5 as enabling the linter to "interpret" the condition field, implying machine-readability. But if P1-4 already provides machine-readable conditions through `ConfigCondition`, P3-5's scope shrinks to "make the documentation string parseable for... what consumer?"

I agree with functional-typing that this is a spec-implementation inconsistency. The tension is that the Round 1 synthesis may have P3-5 and P1-4 working at cross purposes without realizing it. This should be flagged in the final synthesis as a scoping question: does P3-5 extend `config_conditions` (adding more condition types to `ConfigCondition`), or does it formalize the prose `condition` field into a separate grammar? The former is useful; the latter is redundant work.

**Source**: functional-typing review, OBA-2 (L135-143); Round 1 synthesis, P1-4 (L290-296), P3-5 (L391-394); my review, A6 (L45-46).

### T-2: The `itertools.product` recommendation (MO-2) is technically sound but misaligned with the review's own priorities

functional-typing proposes (MO-2) using `itertools.product` in test case generators, citing Constitution Principle IX's FP guidance. The recommendation is technically correct -- `itertools.product` makes cross-products explicit and cleans up three-level nesting.

The tension is with functional-typing's own stated priority framework. The review's executive summary says "the remaining work is execution, not design." MO-2 is neither execution nor design -- it is a style refactoring of existing test code that works correctly. In a Round 2 review where the purpose is to engage with the synthesizer's dispute resolutions and identify missed opportunities that affect correctness or architecture, a P3 test readability improvement dilutes the signal. functional-typing's MO-1 (ValidationContext) and OBA-2 (condition field inconsistency) are substantive; MO-2 is noise by the review's own standard.

This is a minor tension, not a contradiction. The recommendation is not wrong. It simply consumes attention in a review focused on resolving architectural disputes.

**Source**: functional-typing review, MO-2 (L87-117), Executive Summary (L14).

### T-3: The "non-breaking" qualification (OBA-1) is valid but already resolved by the synthesizer's own choice

functional-typing correctly notes (OBA-1) that the synthesizer's reasoning -- "no external consumers means non-breaking" -- is imprecise, because internal test code IS a consumer. Adding positional parameters to `validate_template` without keyword-only enforcement would break `test_validate.py`.

I raised an almost identical concern in my own review (Dispute 1 engagement): the synthesizer's reasoning about "no external consumers" establishes a dangerous principle even though the conclusion is correct. functional-typing and I arrive at the same destination from different directions: functional-typing from the test-suite-as-consumer angle, I from the forward-compatibility-principle angle.

The tension is that functional-typing acknowledges the `ValidationConfig` model resolves the practical problem (Pydantic models absorb new fields with defaults) but still frames this as an "off-base assumption." It is more accurately a "reasoning shortcut" -- the synthesizer reached the right answer for the right structural reasons (Pydantic model extensibility) but articulated a secondary justification (no external consumers) that does not hold under scrutiny. Our two reviews converge on the same correction without conflict.

**Source**: functional-typing review, OBA-1 (L123-131); my review, Dispute 1 engagement (L58-66).

---

## Safe Agreements

### SA-1: The `ValidationConfig` Pydantic model is the correct API boundary pattern

functional-typing explicitly accepts the `ValidationConfig` model and provides three compelling additional justifications: named fields with defaults (non-breaking extension), validation at construction (pre-execution rejection), and serialization for testing (JSON round-trip for CI fixtures). My review accepts the same pattern and requests only a docstring refinement specifying anticipated plugin extensions. These positions are fully compatible: adopt `ValidationConfig`, document the anticipated extension in the docstring.

**Source**: functional-typing review, Dispute 1 Confirmation (L56-63); my review, Dispute 1 engagement (L56-68), R1 (L132-140).

### SA-2: `SchemaLoadError` purification (P1-1) is the highest-priority correctness fix

functional-typing identifies P1-1 as "the single most important change for functional correctness." My review does not dispute this -- it is upstream of every other improvement. Impure loaders that call `sys.exit()` block testability, composability, and the programmatic API. Both reviews treat this as settled and non-controversial.

**Source**: functional-typing review, Convergence endorsement (L33-34); my review (implicit -- no challenge to P1-1 in any section).

### SA-3: `frozen=True` on core TemplateContext models with composition for plugins

functional-typing endorses P2-5 and explains the architectural logic: immutability enforces construction discipline, and plugin data flows through a separate `PluginContext`. My review (A2) confirms no `dict[str, Any]` on TemplateContext, and my Round 1 concession of `frozen=True` for core models is maintained. Both reviews agree that spec 007 handles plugin extensibility through composition, not through relaxing core model constraints.

**Source**: functional-typing review, Convergence endorsement (L37-38); my review, A2 (L27-28).

### SA-4: The `error_type` field should be `str` with a `KNOWN_ERROR_TYPES` registry

Both reviews accept the synthesizer's resolution on Dispute 2/3 (error_type as `str` validated against a `frozenset`). The disagreement identified in DC-1 above is about **enforcement behavior** (reject vs. warn), not about the type choice itself. On the fundamental question -- `str` over `Literal`, validated against a runtime registry -- both reviews are aligned without reservation.

**Source**: functional-typing review, Dispute 2 Refinement (L44-52); my review, A3 (L31-34).

### SA-5: All Round 1 concessions are maintained without reversal

functional-typing explicitly accepts all four synthesizer dispute resolutions and does not reverse any Round 1 concessions. My review maintains all seven Round 1 concessions and closes three of four disputes entirely. Neither review attempts to re-litigate settled positions. The deliberation's intellectual movement is preserved.

**Source**: functional-typing review, Alignment section (L19-28); my review, Summary of Positions table (L181-189), Concessions maintained (L193-204).

### SA-6: P1-4 (`ConfigCondition` model) is the correct typed approach for machine-readable conditions

functional-typing endorses P1-4 and connects it to the `condition` field analysis (OBA-2). My review (A6) endorses P1-4 as establishing a precedent for typed extension mechanisms. Both reviews agree that `ConfigCondition` is the right abstraction for spec 006's conditional variables and that it sets a composable pattern for spec 007.

**Source**: functional-typing review, OBA-2 (L135-143); my review, A6 (L45-46).

### SA-7: The synthesizer's reasoning about "no external consumers" needs qualification

As detailed in T-3, both reviews independently identify that the synthesizer's secondary justification -- "no external consumers means non-breaking" -- is imprecise. functional-typing notes internal tests as consumers; I note the forward-compatibility principle. Both reviews agree the `ValidationConfig` model resolves the practical concern, making this a reasoning-quality issue rather than a decision-quality issue.

**Source**: functional-typing review, OBA-1 (L123-131); my review, Dispute 1 engagement (L58-66).
