# APM Final Disputes: Subject Arbitration (Phase 6)

**Agent**: APM (Agent Package Manager)
**Date**: 2026-03-19
**Phase**: Disputes (post-revision)

---

## Remaining Disputes

### Dispute 1: Structured output mechanism — fenced YAML block vs. engine-only extraction

**Claim**: The structured data from Phase 6 resolution should be produced exclusively by the engine as a post-processing extraction step, never as a format requirement on the arbiter agent.

**spec-kit's position** (revised P1-1): Require a fenced YAML code block at the end of `resolution.md` that the arbiter agent itself produces, validated post-hoc by the engine. If validation fails, the block is flagged as unreliable but the resolution stands.

**Counter-argument**: Asking an LLM to produce both coherent prose *and* a correctly structured YAML block in a single generation creates a dual-format consistency risk that the engine can eliminate entirely. The arbiter's job is to reason through disputes and produce a well-grounded narrative decision. Structured extraction is a mechanical transformation of that narrative -- parsing headings, extracting dispute IDs, pulling confidence levels -- that deterministic code performs with 100% reliability on validated prose. Spec-kit's approach accepts unreliable structured data as a known failure mode and builds degradation logic around it. APM's approach eliminates the failure mode by never asking the LLM to do the mechanical work in the first place. gh-aw's revised P1-3 aligns with APM here: "Machine-readable structured data should be extracted by the engine from the validated prose, not demanded of the LLM agent as a second output format."

**Proposed resolution**: The arbiter produces prose only. The engine runs heading-presence validation (gh-aw P1-3), then extracts structured data from the validated prose into a structured representation. The extraction schema is defined in the spec so that template headings and structure support reliable parsing. No YAML block in the resolution template, no dual-format burden on the agent.

---

### Dispute 2: Non-cooperative template disposition — draft directory vs. acknowledged-in-spec

**Claim**: The non-cooperative arbitration templates should be retained in the active template directory, acknowledged in the spec as drafts, and gated behind a future spec for activation.

**gh-aw's position** (revised P2-4): Remove non-cooperative templates from the active `templates/{mode}/` directories entirely. Relocate them to `templates/_future/` or `templates/_draft/` to prevent accidental discovery by template-scanning tooling.

**Counter-argument**: Moving templates to a separate directory discards the design signal they carry. The templates are not dead code -- they are design artifacts that document how arbitration semantics should differ per mode (dispute resolution vs. verdict review vs. boundary assignment vs. risk assessment). Any future author writing these templates would need to re-derive the same per-mode reasoning. Keeping them in-place under a clearly documented draft status preserves that work while preventing activation. The "accidental discovery" risk gh-aw cites is a tooling concern, not a specification concern. Template-scanning tooling should respect the FR-004 constraint and the documented draft status, not the other way around. If tooling cannot distinguish active from draft templates in the same directory, the tooling needs a filtering mechanism (e.g., a frontmatter field `status: draft`), not a filesystem reorganization that loses context.

**Proposed resolution**: Retain templates in `templates/{mode}/arbitration.md`. Add a frontmatter field `status: draft` to non-cooperative templates. Update FR-004 to reference this status field. Template-scanning tooling filters on status, not directory location. The spec acknowledges these templates as preparatory design artifacts gated behind a separate game-dynamics analysis spec. This is spec-kit's P2-5 position, which all three reviewers converged toward in principle -- the disagreement is only about where the files physically live.

---

### Dispute 3: Trigger mechanism — HTML boundary markers vs. boolean HTML comment

**Claim**: The Phase 5 trigger mechanism should use APM's boundary markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`) that serve both trigger evaluation and content extraction.

**spec-kit's position** (revised P1-3): Use a boolean HTML comment (`<!-- CONVERSUS:DISPUTES_REMAIN: {true|false} -->`) at the end of Phase 5 output, with heading parsing as a backward-compatible fallback. The heading is demoted from control-flow signal to human-readable display.

**Counter-argument**: spec-kit's boolean comment answers only one question: "Are there remaining disputes?" APM's boundary markers answer two: "Are there remaining disputes?" (content exists between markers) and "What are they?" (the content itself). The second question matters because APM's surviving P2-6 proposes `{REMAINING_DISPUTES}` as a Phase 6 template variable that feeds the actual dispute text into the arbiter's prompt. With spec-kit's boolean comment, the engine still needs to parse prose headings to extract dispute content for the variable -- the very fragility all three reviews flagged. With APM's boundary markers, extraction is a trivial substring operation between two known delimiters. The boolean comment solves the trigger problem but not the extraction problem; the boundary markers solve both with one mechanism. gh-aw's revised P1-2 explicitly adopts APM's boundary marker approach over its own original proposals for this reason.

**Proposed resolution**: Adopt boundary markers as the primary mechanism. Add spec-kit's backward-compatible fallback (heading parsing when markers are absent) for existing templates. This gives new templates a single mechanism that serves both trigger evaluation and content extraction, while not breaking templates that predate the markers.

---

### Dispute 4: Low-confidence ruling behavior — justified confidence vs. no special treatment

**Claim**: Low-confidence rulings should carry a mandatory one-sentence justification that makes the confidence assessment self-documenting and actionable.

**gh-aw's position** (implicit in cross-review T-5): Low-confidence tagging creates perverse incentives for arbiters to report Medium confidence to avoid additional requirements. The confidence field should carry no behavioral consequences.

**Counter-argument**: spec-kit's revised P1-4 already addressed the perverse-incentive concern by withdrawing the mandatory follow-up field and replacing it with a one-sentence justification. The justification requirement applies to ALL confidence levels (High, Medium, Low), not just Low, which eliminates the incentive to game the level. "High -- grounding document directly addresses this tradeoff" is just as required as "Low -- grounding document is silent on performance vs. correctness tradeoffs." This is a transparency mechanism, not a penalty mechanism. Without justification, confidence levels are opaque labels that downstream consumers cannot interpret or challenge. APM adopted spec-kit's revised position (N-3 in APM's revision) because it adds signal value without adding process overhead. The question is whether any confidence-related requirement belongs in v1 at all. APM's position: it does, because the Confidence Assessment section already exists in the template -- making it self-documenting costs one sentence per ruling and makes the section useful rather than decorative.

**Proposed resolution**: Adopt spec-kit's revised P1-4: require a one-sentence justification for every confidence rating (all levels, not just Low). No behavioral triggers, no mandatory follow-up fields. The justification is informational, making the confidence section a meaningful audit artifact rather than an unjustified label.

---

## Convergence

### 1. Singular grounding document is the core integrity mechanism

All three reviews now agree that the `grounding` field must remain a single path. APM withdrew P2-4 (grounding as list) after spec-kit's "citation laundering" argument and gh-aw's "cherry-picking" argument proved decisive. gh-aw withdrew P2-7 (expand citation scope to `docs`). The consensus is complete: grounding singularity forces the arbiter to derive all rulings from one declared, bounded, human-verifiable document. `docs` provides read-only context but not citable authority.

### 2. Phase 6 failure falls back to Phase 5 with a warning

gh-aw's P1-1 (failure semantics) received no counterargument from any review. APM adopted it as N-1 in revision. Spec-kit adopted it as N-2 in revision. The specification gap is unanimously identified and the resolution is unanimously agreed: if the arbiter agent fails, Phase 5 output becomes the terminal state, a warning is emitted, and no partial `resolution.md` is written to disk.

### 3. Cooperative-only restriction (FR-004) is correct for v1

APM withdrew P1-1 (enable all modes) after both cross-reviewers demonstrated that non-cooperative modes have game-theoretic properties that arbitration can subvert. The three reviews now agree that FR-004 should be retained, non-cooperative templates should be acknowledged as draft/future work, and activation requires a separate spec analyzing per-mode implications. The only remaining disagreement is where the draft templates physically reside (Dispute 2 above).

### 4. Observations are permitted but structurally constrained

All three reviews agree that FR-015.5 ("no new recommendations") must coexist with the template's observation mechanism. The agreed resolution: observations are permitted only in the Confidence Assessment section, must be explicitly non-binding, and must not appear in Binding Decisions or Summary of Changes Required. An observation that implies a required change violates FR-015.5 regardless of labeling. This structural containment prevents scope laundering while preserving the arbiter's ability to flag genuine insights.

### 5. Schema versioning is premature (YAGNI)

APM withdrew P2-5 (add schema/version field) after gh-aw's argument that the `arbiter` field is fully additive and introduces no breaking change. No review argues for versioning in v1. The consensus: introduce versioning when a breaking change forces it, not preemptively after the first additive extension.

---

## Final Position Statement

### Non-Negotiable Positions

1. **Structured data must be engine-extracted, not arbiter-produced.** The arbiter generates prose. The engine extracts structure. This is a correctness position: deterministic code outperforms LLM generation for mechanical transformation, and dual-format requirements on the agent create a consistency failure mode that is avoidable by design. APM will not support a spec that requires the arbiter agent to produce YAML, JSON, or any structured format alongside its narrative resolution.

2. **Boundary markers over boolean signals for trigger evaluation.** The `{REMAINING_DISPUTES}` variable (surviving P2-6, unchallenged on substance by any review) requires content extraction, not just trigger detection. Boolean signals solve half the problem. Boundary markers solve the whole problem with one mechanism. APM will advocate for boundary markers as the canonical approach, with heading-based fallback for backward compatibility.

3. **The observation carve-out must be structurally constrained, not instruction-dependent.** Permitting observations "anywhere as long as they say non-binding" is an invitation to scope laundering. The constraint must be positional: Confidence Assessment section only. APM will not support an observation exemption that lacks structural boundaries.

### Areas of Flexibility

1. **Template file disposition.** APM prefers in-place draft status (frontmatter field) over directory relocation, but will accept either approach as long as the design artifacts are preserved and not deleted. If gh-aw's `_draft/` directory approach is adopted, the templates must carry their full content, not just stubs.

2. **Confidence justification.** APM supports spec-kit's revised one-sentence justification for all confidence levels, but recognizes this is a P2 concern, not P1. If the arbiter community resists per-ruling justification in v1, APM will accept deferral to v2 as long as the Confidence Assessment section remains in the template.

3. **Structured extraction schema.** APM's position is that the engine extracts structured data from prose, but is flexible on the schema format (YAML, JSON, or a conversus-specific format), the extraction timing (immediate post-Phase-6 vs. on-demand), and whether the extraction output is a sidecar file or an in-memory data structure consumed by downstream tooling. The principle (engine extracts, not agent produces) is non-negotiable; the implementation details are open.

4. **Post-arbitration validation scope.** APM supports gh-aw's heading-presence check as the v1 validation mechanism and is flexible on whether additional validation rules (grounding citation verification, dispute-ID coverage checks) are added in v1 or deferred. The validation framework should be extensible, but the initial rule set can be minimal.
