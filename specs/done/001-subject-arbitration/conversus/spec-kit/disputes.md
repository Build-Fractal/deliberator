# Spec-Kit Final Disputes: Subject Arbitration (Phase 6)

**Agent**: spec-kit (SDD framework)
**Phase**: Disputes (Phase 4)
**Date**: 2026-03-19
**Inputs**: All three revised positions (spec-kit, APM, gh-aw)

---

## Remaining Disputes

### Dispute 1: Structured output in the resolution — engine-extracted vs. arbiter-produced

All three revised positions agree that machine-readable structured data should exist alongside the human-readable resolution. The disagreement is over **who produces it and when it enters the artifact**.

- **Spec-kit (revised P1-1)**: The arbiter produces a fenced YAML block at the end of `resolution.md`, validated post-hoc. Graceful degradation if malformed.
- **APM (revised P3-9)**: The engine extracts structured data from the resolution prose after Phase 6 completes. The arbiter produces only prose. The extraction is a post-processing step.
- **gh-aw (revised P1-3)**: No structured format requirements on the arbiter for v1. Machine-readable data should be engine-extracted, not LLM-demanded.

APM and gh-aw align against spec-kit on this point. Their shared argument is that requiring an LLM to produce both prose and structured YAML simultaneously creates a consistency risk the engine can eliminate. Spec-kit's counter: engine extraction depends on reliable heading structure and consistent prose formatting, which is itself fragile. An explicit structured block -- even one that sometimes fails validation -- gives downstream tooling a direct parse target rather than forcing regex extraction from prose whose formatting is not contractually guaranteed.

**Spec-kit's position**: The fenced YAML block produced by the arbiter remains superior for the SDD pipeline. Engine extraction is a bet that prose structure will be stable enough to parse reliably. A YAML block that the agent is explicitly instructed to produce, with a post-validation step that flags failures, is more honest about the reliability boundary. The validation layer (which all three agree on) handles the failure case. However, if the arbiter community resolves this against spec-kit, the critical requirement is that *some* structured representation exists and that its schema is defined in the spec -- the extraction mechanism is secondary to the schema definition. Spec-kit will accept engine extraction if the output schema is normatively specified.

---

### Dispute 2: Trigger mechanism — APM structural markers vs. spec-kit HTML comment signal

All three revised positions agree that heading-based parsing alone is insufficient. The disagreement is over the hardening mechanism.

- **APM (revised P1-2)**: Structural HTML markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`) that serve both trigger evaluation and content extraction for `{REMAINING_DISPUTES}`.
- **gh-aw (revised P1-2)**: Adopted APM's structural markers as the single canonical mechanism.
- **Spec-kit (revised P1-3)**: HTML comment `<!-- CONVERSUS:DISPUTES_REMAIN: {true|false} -->` as the trigger signal, with heading parsing as a backward-compatible fallback. The heading is presentation; the comment is the contract.

APM and gh-aw align on boundary markers. Spec-kit proposes a scalar boolean signal. The functional difference: APM's markers delineate content boundaries (enabling extraction of the disputes themselves), while spec-kit's comment is a pure trigger signal (presence/absence of disputes, not their content).

**Spec-kit's position**: APM's boundary markers are the better design if `{REMAINING_DISPUTES}` is adopted (APM P2-6), because they serve double duty -- trigger evaluation and content extraction from a single mechanism. Spec-kit's boolean comment serves only the trigger. If the spec adopts `{REMAINING_DISPUTES}` as a template variable, spec-kit concedes to APM's boundary markers. If `{REMAINING_DISPUTES}` is deferred, the boolean signal is simpler and sufficient. This dispute is contingent on the `{REMAINING_DISPUTES}` variable decision rather than being independently resolvable.

---

### Dispute 3: Non-cooperative templates — remove from active directory vs. acknowledge in place

All three revised positions agree that non-cooperative modes must not ship as active. The disagreement is over what to do with the existing template files.

- **gh-aw (revised P2-4)**: Remove templates from `templates/{mode}/` to a `templates/_future/` or `templates/_draft/` directory with a README. Prevents accidental discovery by template-scanning tooling.
- **spec-kit (revised P2-5)**: Acknowledge templates in the spec as draft/experimental. Retain FR-004 cooperative-only restriction. Gate activation behind a separate game-dynamics spec.
- **APM (revised, withdrawn P1-1)**: Adopted spec-kit's position (keep cooperative-only, formally status as drafts).

gh-aw raises a practical concern spec-kit did not address: if template-scanning tooling walks `templates/*/arbitration.md`, it will discover the non-cooperative templates and may treat them as available. Spec-kit's "acknowledge in spec" approach handles the human reader but not automated tooling.

**Spec-kit's position**: gh-aw's concern about automated discovery is valid. However, moving files to `_draft/` is a filesystem convention that itself requires tooling awareness -- scanners must know to skip `_` prefixed directories, which is not a universal convention. The more robust solution is both: keep the templates in their canonical paths (preserving the naming convention and making future activation a config change, not a file move), AND add a machine-readable marker inside each non-cooperative template (e.g., `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`) that tooling can check. FR-004 validation already prevents runtime use. The marker prevents tooling-level misinterpretation. This is a small concession to gh-aw's concern without adopting the filesystem relocation, which creates a different discovery problem (where did the templates go?).

---

### Dispute 4: Observation carve-out scope — section-restricted vs. label-restricted

All three revised positions agree that FR-015.5's "no new recommendations" constraint needs an explicit carve-out for observations noted in the Confidence Assessment. The disagreement is over how to prevent the observation mechanism from becoming a laundering vector.

- **APM (revised P1-3)**: Observations permitted ONLY in the Confidence Assessment section. Observations appearing in Binding Decisions or Summary of Changes Required violate FR-015.5 regardless of labeling.
- **gh-aw (N-2)**: Observations are informational annotations without decision authority. An observation that implies a required change is a new recommendation by another name and violates FR-015.5.
- **Spec-kit (revised P1-4, N-1)**: Observations explicitly excluded from binding decisions. Require a one-sentence justification alongside the confidence field. Do NOT make low-confidence rulings trigger mandatory process requirements (withdrawn to avoid perverse incentives).

APM's structural constraint (section-restricted) and gh-aw's semantic constraint (content-restricted: an observation implying a required change violates the rule) are complementary but create different enforcement surfaces. APM's is enforceable by an automated check (is this text in the right section?). gh-aw's requires judgment (does this observation imply a required change?).

**Spec-kit's position**: Both constraints should apply. APM's section restriction is the enforceable outer boundary -- observations must appear only in the Confidence Assessment section. gh-aw's semantic restriction is the interpretive inner boundary -- even within that section, an observation that prescribes a specific change is a recommendation in disguise. The spec should state both: "Observations MAY appear only in the Confidence Assessment section (structural constraint) and MUST NOT prescribe specific changes to the target artifact (semantic constraint). An observation that directs implementation is a recommendation subject to FR-015.5." This layered approach gives automated validation a checkable rule (section placement) and human reviewers a judgment criterion (prescriptive content).

---

## Convergence

### Convergence 1: Singular grounding document as the core integrity mechanism

All three revised positions explicitly affirm that `arbiter.grounding` must remain a single path, not a list. APM withdrew its multi-path proposal (P2-4). gh-aw withdrew its citation-scope expansion (P2-7). Spec-kit's original position (P2-6) stands reinforced. The grounding document's singularity prevents citation laundering and forces the arbiter to derive all rulings from one auditable framework. The `docs` field provides read-only context; only the grounding document may be cited as authority. This is the strongest consensus point across all three reviews and both cross-review rounds.

### Convergence 2: Phase 6 failure semantics — fall back to Phase 5

All three revised positions agree that Phase 6 failure must not invalidate the Phase 1-5 deliberation record. gh-aw originated this recommendation (P1-1). Spec-kit adopted it (N-2). APM adopted it (N-1). The terminal state on failure is Phase 5 output with a diagnostic annotation. No partial `resolution.md` on disk. This is a unanimous addition to the spec with zero disagreement on substance or mechanism.

### Convergence 3: Cooperative-only restriction (FR-004) is correct and must be retained

All three revised positions agree. APM withdrew its recommendation to enable all modes (P1-1), explicitly adopting spec-kit's position. gh-aw narrowed its "either/or" stance to "remove from active templates." The game-theoretic arguments are decisive: in PD mode, arbitration can rehabilitate trust scores; in Red-Blue mode, giving the attack target binding authority over findings is a security anti-pattern. Non-cooperative arbitration requires separate specification analyzing per-mode incentive dynamics.

### Convergence 4: The information-asymmetry assumption is too narrow and needs reframing

All three revised positions converge on a two-part framing: decision authority as the general principle, information asymmetry as the common but not required justification. Spec-kit originated the decision-authority reframe (P2-7), APM proposed the synthesis ("decision authority constrained by a grounding document, informed by the arbiter's unique integration perspective"), and spec-kit's revision adopted the synthesized version. gh-aw endorsed retaining both framings. The revised assumption broadens the spec's applicability beyond systems-with-operational-knowledge to any arbiter with legitimate decision authority.

### Convergence 5: Post-arbitration output validation is a v1 requirement

All three revised positions agree that the engine must validate the resolution's structural conformance after Phase 6 completes. gh-aw originated the heading-presence check (P1-3). APM adopted it (N-2). Spec-kit's structured YAML block includes a validation layer (revised P1-1). The specific validation mechanism differs (heading check vs. YAML parse), but the principle is unanimous: the engine must not silently accept malformed arbitration output. Validation warnings must appear in the final report.

---

## Final Position Statement

Spec-kit enters the synthesis phase holding firm on three positions and offering conditional concessions on two.

**Firm positions:**

1. **Structured output schema must be normatively defined in the spec**, regardless of whether the arbiter or the engine produces it. The dispute over extraction mechanism (Dispute 1) is secondary. What matters is that the spec defines the fields (dispute ID, ruling type, grounding citation, required changes, affected target file) so that any downstream consumer -- SDD pipeline, checklist generator, or human auditor -- knows what to expect. If the spec defines only prose sections and leaves structure as an implementation detail, every consumer will invent its own parser, and none will be reliable.

2. **The observation carve-out must be both structurally and semantically constrained** (Dispute 4). A section-only restriction is enforceable but gameable (write prescriptive observations in the right section). A semantic-only restriction is ungameable but unenforceable (who judges whether an observation "implies a required change"?). Both layers together create a defense-in-depth that neither achieves alone.

3. **Per-file attribution in binding decisions** (surviving P3-8), **requirement-identifier traceability** (surviving P1-2), and **grounding document stability** (surviving P3-10) are uncontested across all reviews and should be adopted without further deliberation.

**Conditional concessions:**

1. On trigger mechanism (Dispute 2): spec-kit will adopt APM's boundary markers if `{REMAINING_DISPUTES}` is accepted as a template variable. If the variable is deferred, the boolean signal is sufficient and simpler.

2. On structured output mechanism (Dispute 1): spec-kit will accept engine extraction over arbiter-produced YAML if the output schema is normatively specified in the spec. The schema definition is the non-negotiable; the production mechanism is negotiable.

The cross-review process surfaced genuine architectural tensions and resolved the largest ones (grounding singularity, cooperative-only restriction, failure semantics, information-asymmetry framing). The remaining disputes are implementation-mechanism disagreements within a shared design, not fundamental disagreements about what the spec should accomplish. The synthesis should be able to resolve them by choosing mechanisms and recording the rationale.
