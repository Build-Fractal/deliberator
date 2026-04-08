# gh-aw Final Disputes: Subject Arbitration (Phase 6)

**Agent**: gh-aw (GitHub Agentic Workflows)
**Date**: 2026-03-19
**Phase**: Final disputes after revision round

---

## Remaining Disputes

### Dispute 1: Structured output requirements on the arbiter agent in v1

**Disputed with**: spec-kit (revised P1-1)

Spec-kit's revised position calls for a fenced YAML code block at the end of `resolution.md` containing dispute IDs, ruling types, grounding citations, and required-change summaries. APM's revised position (P3-9) delegates extraction to the engine but still expects the resolution template's headings to "support reliable extraction." Both positions assume the arbiter agent will produce output with enough structural regularity for machine consumption in v1.

gh-aw maintains that requiring ANY structured format from the arbiter -- whether inline YAML, HTML markers, or extraction-friendly headings -- is premature for the initial release. The arbiter is an LLM agent. Its output is probabilistic prose, not schema-conforming data. Spec-kit's revised position adds a validation step and graceful degradation, which is better than the original, but the degradation path ("structured block is flagged as unreliable") means downstream tooling must handle two output states: reliable-structured and unreliable-structured. That is more complex than a single state: prose-only.

The correct v1 contract: `resolution.md` is human-readable prose with required section headings (validated by the heading-presence check from our P1-3). Machine-readable extraction is a v2 concern that should be designed after observing actual arbiter output patterns across real runs. Designing extraction schemas before we have real output data is speculative engineering.

APM's revised P3-9 is closer to our position (engine-extracted, not arbiter-produced) but still asks the spec to define an extraction schema now. We dispute that the schema can be meaningfully defined before production use reveals what the arbiter actually produces.

### Dispute 2: Non-cooperative templates -- relocation vs. in-place acknowledgment

**Disputed with**: spec-kit (P2-5)

All three agents agree the template/constraint mismatch must be resolved. APM withdrew its "enable all modes" recommendation. The remaining disagreement is between spec-kit's position (acknowledge templates in the spec as draft/experimental, retain them in place) and gh-aw's revised position (move templates to `templates/_draft/` or `templates/_future/`).

Spec-kit argues the templates are "preparatory design artifacts" that "document intent and reduce future implementation cost." gh-aw maintains that any file in an active template directory is discoverable by template-scanning tooling. A template at `templates/prisoners-dilemma/arbitration.md` will be found by any glob pattern that discovers `templates/cooperative/arbitration.md`. An acknowledgment note in the spec does not prevent tooling from loading the file. The only way to prevent accidental activation is physical separation: move the files out of the active template tree.

This is not about discarding work. The templates are retained, versioned, and accessible. The dispute is solely about directory placement: active template tree vs. a clearly-marked draft directory. Spec-kit's "acknowledge and document" approach relies on humans reading documentation before using templates. gh-aw's relocation approach relies on directory structure, which tooling respects automatically.

### Dispute 3: Observation carve-out scope and enforceability

**Disputed with**: APM (revised P1-3), spec-kit (N-1)

APM's revised position permits observations in the Confidence Assessment section, labeled as non-binding, excluded from Binding Decisions and Summary of Changes Required. Spec-kit's N-1 adopts nearly identical language. Both frame this as reconciling FR-015.5 with the template's observation instructions.

gh-aw accepts the principle but disputes the enforceability. The proposed constraint is: "observations that appear in binding sections violate FR-015.5." But who enforces this? The heading-presence validator checks for section existence, not section content. No proposed validation mechanism inspects whether text in the Binding Decisions section is a "ruling" or a "laundered observation." The distinction between "the arbiter rules that X should change" and "the arbiter observes that X would benefit from change" is semantic, not structural. An LLM can trivially rephrase one as the other.

gh-aw's position: if the carve-out cannot be structurally enforced, it should not be formalized as a requirement. Instead, the template instruction should remain as-is (soft guidance to the arbiter), and FR-015.5 should remain as-is (hard prohibition on new recommendations). The ambiguity between the soft template guidance and the hard formal requirement is a feature: it gives the arbiter room for professional judgment while maintaining a clear bright-line rule for accountability. Formalizing the exception without an enforcement mechanism creates a rule that is simultaneously too precise to be guidance and too vague to be enforced.

---

## Convergence

### Convergence 1: Singular grounding document as the core integrity mechanism

All three agents converged fully on this point across both rounds. APM withdrew its multi-path `grounding` proposal (P2-4). gh-aw withdrew its citation-scope expansion (P2-7). Spec-kit held firm and was validated. The single grounding document, cited as the sole authority in binding decisions, is the spec's strongest design decision and the foundation of arbiter accountability. `docs` provides read-only context; only `grounding` carries citation authority. This is settled.

### Convergence 2: Phase 6 failure semantics

All three agents agree that Phase 6 failure must fall back to Phase 5 output as the terminal state, with a warning in the final report, and no partial `resolution.md` left on disk. APM adopted gh-aw's P1-1. Spec-kit created N-2 endorsing the same semantics. No agent disputed this at any point. This is the cleanest consensus across all reviews.

### Convergence 3: Trigger evaluation must be hardened with structured signals

All three agents agree that heading-based trigger parsing is the spec's most dangerous fragility. All three converged on APM's structural HTML markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`) as the canonical mechanism. gh-aw adopted this in its revised P1-2. Spec-kit adopted a compatible HTML comment approach in its revised P1-3 (boolean signal with heading fallback). The specific marker syntax may vary, but the principle is settled: structured signals replace prose parsing for control flow, with heading parsing retained only as a backward-compatible fallback.

### Convergence 4: Cooperative-only restriction (FR-004) must be retained

APM withdrew its recommendation to enable all modes. All three agents agree that non-cooperative modes require separate game-theoretic analysis before activation. The remaining dispute (Dispute 2 above) is about how to handle the existing templates, not whether to enable the modes. The restriction itself is settled.

### Convergence 5: Backward compatibility design is correct and complete

All three agents independently validated the opt-in model (FR-005, SC-004) across both rounds. No agent at any point proposed changes to the backward-compatibility design. Zero behavioral change when the `arbiter` field is omitted. Additive-only extension. This is the most thoroughly validated aspect of the spec.

---

## Final Position Statement

gh-aw entered this deliberation focused on operational safety: failure modes, output validation, execution robustness, and the gap between what the spec describes and what actually happens when an LLM agent runs Phase 6 in a CI pipeline. Two rounds of cross-review confirmed that this focus was complementary to APM's mechanism-design perspective and spec-kit's pipeline-integration perspective.

We withdrew three recommendations. Dry-run mode (P2-5) was correctly identified by APM as a contradiction in terms -- a non-binding ruling defeats the value proposition of arbitration, and adoption risk is an operational concern addressed by starting small, not by fragmenting the output contract. The metadata sidecar (P2-6) broke the single-artifact-per-phase model that all three agents value. Citation scope expansion (P2-7) dissolved the single-document accountability model we ourselves praised as the spec's strongest design.

We modified two recommendations. Trigger robustness (P1-2) narrowed from three options to one, adopting APM's structural HTML markers as the superior mechanism because they serve both trigger evaluation and dispute extraction. Output validation (P1-3) was scoped to exclude structured format requirements on the arbiter for v1, aligning with our own cross-review finding that demanding YAML from an LLM without enforcement creates false confidence.

Our five surviving recommendations remain unchanged: failure semantics (P1-1), template/constraint mismatch resolution via relocation (P2-4), grounding document guidance (P3-8), idempotency semantics (P3-9), and quorum trigger for future iterations (P3-10).

The three remaining disputes are genuine disagreements about design philosophy, not misunderstandings:

1. **Structured output timing**: gh-aw believes machine-readable extraction should be designed after observing real arbiter output, not before. Spec-kit and APM want to define schemas now. This is a build-measure-learn disagreement.

2. **Template relocation**: gh-aw believes directory structure is the only reliable mechanism for preventing accidental template activation. Spec-kit believes documentation is sufficient. This is a tooling-trust disagreement.

3. **Observation enforceability**: gh-aw believes formalizing an exception without a structural enforcement mechanism creates a rule that cannot be audited. APM and spec-kit believe the formal carve-out is still valuable as a constraint on the arbiter's instructions. This is a rules-vs-guidance disagreement.

On every other point -- grounding integrity, failure semantics, trigger hardening, cooperative-only restriction, backward compatibility -- the three agents have converged. The spec's core design is sound. The remaining disputes concern v1 scope and enforcement mechanisms, not architectural direction.
