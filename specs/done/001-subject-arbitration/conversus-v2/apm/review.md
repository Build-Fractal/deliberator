# APM v2 Review: Subject Arbitration (Phase 6)

**Reviewer**: APM (Agent Package Manager)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Review Type**: v2 (post-synthesis revision check)
**Perspective**: Packaging, distribution, context compilation, agent primitives, SKILL.md execution model

---

## Executive Summary

The spec has been substantially improved by the v1 conversus cycle. Of the 17 changes recommended by the synthesis, the majority are well-integrated: structural HTML markers for trigger evaluation (FR-011), the `{REMAINING_DISPUTES}` template variable (FR-014), the `docs` vs. `grounding` citation-authority distinction (FR-024), failure semantics (FR-022), output validation (FR-023), and the observation carve-out reconciliation (FR-015.5) all land correctly. The spec now reads as a coherent, implementable design rather than a draft with known gaps. However, the integration introduces three new concerns: (1) the trigger evaluation in SKILL.md still uses the old heading-based parsing and does not reference the structural markers the spec now mandates, (2) the non-cooperative template disposition was resolved in the spec's Constraints section but the Implementation Guidance defers the mechanism, creating ambiguity about whether templates should exist in v1, and (3) the structured output schema is deferred in a way that may constrain future extraction design because the prose template headings are not explicitly designed to be machine-parseable. The four remaining disputes from v1 (structured output mechanism, template file placement, observation enforceability, low-confidence behavior) are adequately documented but only partially resolved in the spec text -- two are deferred, one is structurally resolved, and one is noted without a clear decision.

---

## Alignment

### 1. Structural HTML markers correctly replace heading-based parsing as primary trigger

FR-011 now specifies `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` as the primary mechanism with heading-based parsing as fallback. This directly implements APM's Dispute 3 position and the synthesis's P1 change #2. The dual-mechanism approach (markers primary, headings fallback) is the right call -- it hardens the trigger without breaking existing templates. The `{REMAINING_DISPUTES}` variable (FR-014) correctly references the marker-delimited content, making the arbiter's dispute scope machine-defined.

### 2. The `docs` vs. `grounding` distinction is now formally specified

FR-024 codifies what was unanimous convergence: `docs` provides read-only context, only the `grounding` document may be cited as authority, and `docs` citations cannot serve as the sole basis for a ruling. This is the exact formulation the synthesis recommended (P1 change #5). The phrasing "permitted for factual context but MUST NOT serve as the sole basis" is precisely calibrated -- it allows the arbiter to reference documentation without undermining grounding singularity.

### 3. Failure semantics are comprehensive and correctly scoped

FR-022 implements the unanimous convergence on Phase 6 failure handling: Phase 5 output as terminal state, diagnostic warning emitted, no partial `resolution.md`, Phase 1-5 record not invalidated. This was gh-aw's original recommendation that all three agents adopted without counterargument. The spec's implementation is faithful to the synthesis.

### 4. Output validation strikes the right balance between strictness and pragmatism

FR-023 validates section headings but treats malformed output as a warning, not a blocking error. The file is still written. This matches the synthesis's P1 change #3 and avoids the failure mode where valid reasoning is discarded because the agent used a slightly different heading name. The warning ensures malformed output is never silently accepted.

### 5. Non-cooperative template gating is correctly specified

The Constraints section now explicitly states that non-cooperative templates are draft/experimental, must not be activatable in v1, require a separate game-dynamics analysis, and may exist with a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker but must be filtered by the engine at runtime. This resolves the substance of Dispute 2 (templates are retained as design artifacts but cannot activate) while acknowledging the file-placement disagreement as an implementation detail.

### 6. The observation carve-out is reconciled with FR-015.5

FR-015 item 5 now explicitly states that observations in the Confidence Assessment section, labeled non-binding, are not new recommendations -- they are permitted as long as confined to that section. This implements APM's structural constraint (Confidence Assessment section only) as the minimum enforceable rule while acknowledging spec-kit's semantic layer (must not prescribe changes) in the qualifying language. The reconciliation is faithful to the synthesis's P1 change #4.

---

## Missed Opportunities

### 1. SKILL.md trigger evaluation is out of sync with the spec

The conversus SKILL.md (the executable skill definition at `conversus/SKILL.md`) still describes trigger evaluation using only the heading-based mechanism: "Find the `### Remaining Disputes` heading. Check whether there is at least one `**Dispute:` entry under it." It does not reference the structural HTML markers that FR-011 now mandates as the primary mechanism. An implementor following SKILL.md would build the old parsing logic. An implementor following the spec would build the marker-based logic. This is a specification-implementation drift that will produce incorrect behavior.

### 2. The structured output schema deferral lacks a forward-compatibility constraint

The Implementation Guidance defines a structured output schema (dispute_id, ruling_type, grounding_citation, etc.) and defers the production mechanism. This is acceptable for v1. However, the spec does not constrain the prose template to use headings and structure that would make future extraction reliable. FR-018 requires section headings (Process Note, Decision Framework, Binding Decisions, Summary of Changes Required) but does not specify the internal structure of Binding Decisions entries in a way that guarantees extractability. A future engine extractor would need to parse free-form prose within each binding decision to find dispute IDs, rulings, and citations. Adding a lightweight structural convention now (e.g., each binding decision begins with "**Dispute:** ...", "**Ruling:** ...", "**Grounding:** ...") would make the deferred extraction mechanism viable without requiring arbiter-produced YAML.

### 3. Per-file attribution (FR-026) is specified but the template contract does not enforce it

FR-026 requires that binding decisions specify which file is affected when multiple targets exist. The template authoring contract in Implementation Guidance lists the invariants template authors must preserve, but per-file attribution is not among them. A template author could write a compliant template (per the contract) that produces binding decisions without file attribution, violating FR-026. The authoring contract should include this requirement.

### 4. The idempotency semantics (FR-027) do not address the arbitration directory

FR-027 specifies that re-running Phase 6 overwrites `resolution.md`. However, it does not address whether the `{output}/arbitration/` directory is cleaned before re-run (e.g., if a previous run left additional files in that directory). This is a minor gap but could matter if future versions add sidecar files or if manual files are placed in the directory between runs.

### 5. The `trigger: quorum` future option is noted but the trigger enum is not designed for extension

The Implementation Guidance mentions `trigger: quorum` as a future option. However, FR-002 defines `trigger` as an enum of exactly two values (`disputes_remain`, `always`), and FR-003/US2-SC4 validate against exactly these values. Adding `quorum` would require changing validation logic. If the trigger field were documented as an extensible enum (with unknown values producing a validation error rather than being silently ignored), future additions would be cleaner.

### 6. No guidance on arbiter prompt length relative to grounding document size

The Edge Cases section addresses large grounding documents (>50K tokens) by instructing the agent to read the file rather than inlining it. But the arbiter's own prompt (`arbiter.prompt` field) has no size guidance. In practice, the arbiter prompt plus the template plus the dispute content could exceed context limits. The spec should note that the arbiter prompt should be concise (role and constraints only) since the grounding document and disputes provide the substantive content.

---

## Off-Base Assumptions

### 1. The assumption that grounding document stability is sufficient without a verification mechanism

The spec adds a stability note (the grounding document is assumed stable for the run duration), which is correct. However, the spec does not provide any mechanism to detect or warn about instability. If a conversus run takes 30+ minutes across 6 phases, a concurrent edit to the grounding document could produce an arbitration ruling that cites a version of the document that no longer exists. A lightweight mitigation (hash the grounding document at config validation time; warn if it differs at Phase 6 dispatch time) would make the stability assumption verifiable rather than aspirational. This is not a v1 requirement, but the assumption as written implies a guarantee the system does not provide.

### 2. The framing of "binding" decisions assumes single-run finality

The spec defines binding decisions as "final for this conversus run" (Key Entities section). This is technically correct but obscures the practical reality: most conversus outputs feed into downstream processes (spec-kit's `/speckit.specify`, manual code changes, PR creation). A binding decision that is "final for this run" but ignored by the implementor is not meaningfully binding. The spec could acknowledge that "binding" refers to the deliberation record's finality, not to any enforcement mechanism on downstream actors. This is a documentation clarity issue, not a design flaw.

### 3. The template authoring contract assumes template authors understand the Phase 5 output format

The Implementation Guidance's template authoring contract lists what Phase 5 output elements Phase 6 consumes. But it does not specify how template authors should verify their template against these elements. In a packaging context, where templates might be distributed as part of an APM package, a template author in a different project would need to read the Phase 5 synthesis template to understand the output format. A cross-reference to the synthesis template (or a schema of Phase 5 output) would make the contract self-contained.

---

## Actionable Recommendations

### P1 -- Required for Correctness

1. **Sync SKILL.md trigger evaluation with the spec's FR-011.** The conversus SKILL.md must reference structural HTML markers as the primary trigger mechanism, with heading-based parsing as fallback. Currently SKILL.md describes only the heading-based approach. An implementor following SKILL.md will build the wrong logic. Update the Phase 6 trigger evaluation section of `conversus/SKILL.md` to match FR-011's dual-mechanism specification.

2. **Add per-file attribution to the template authoring contract.** The Implementation Guidance's template authoring contract (section "Template authors MUST preserve these invariants") should include: "When multiple target files exist, binding decisions must specify which file each required change applies to (per FR-026)." Without this, the contract and the requirement are disconnected.

3. **Define internal structure convention for Binding Decisions entries.** Within FR-018 or as a new FR, specify that each binding decision entry in `resolution.md` should use consistent sub-headings or labeled fields (e.g., `**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Rejected Positions:**`, `**Required Changes:**`). This is already implied by FR-019 but not formalized as a structural convention. Making it explicit ensures that the deferred structured extraction mechanism (Implementation Guidance) has a reliable parsing target.

### P2 -- Required for Design Integrity

4. **Extend FR-027 idempotency to cover the arbitration directory.** Clarify whether re-running Phase 6 cleans the `{output}/arbitration/` directory or only overwrites `resolution.md`. Recommendation: overwrite `resolution.md` only, leave other files untouched (consistent with "the engine creates the directory" semantics in FR-017, which implies the directory may pre-exist).

5. **Add a forward-compatibility note to the trigger enum.** In FR-002 or the Implementation Guidance, note that the `trigger` field is an extensible enum. Unknown trigger values should produce a validation error (not silent acceptance). This makes the `trigger: quorum` future extension clean and prevents configs with typos from silently defaulting.

6. **Cross-reference the Phase 5 synthesis template in the template authoring contract.** The contract should point to the synthesis template (or document its output schema) so that Phase 6 template authors can verify their template consumes the correct Phase 5 output elements without needing to read the synthesis template source.

### P3 -- Recommended Improvement

7. **Add arbiter prompt sizing guidance to Edge Cases.** Note that `arbiter.prompt` should be concise (role definition and behavioral constraints only) because the grounding document and dispute content provide the substantive input. This prevents context-limit issues when large grounding documents combine with verbose arbiter prompts.

8. **Clarify "binding" in the Key Entities section.** Add a sentence: "Binding refers to the finality of the deliberation record -- no further conversus phases revisit the decision. It does not imply enforcement on downstream actors who consume the resolution." This prevents misinterpretation of the arbiter's authority scope.

---

## Referenced Documentation

| Document | Relevance |
|----------|-----------|
| `conversus/specs/001-subject-arbitration/spec.md` | Primary spec under review (v2, post-synthesis) |
| `conversus/specs/001-subject-arbitration/conversus/summary/final.md` | v1 synthesis -- baseline for change verification |
| `conversus/specs/001-subject-arbitration/conversus/apm/review.md` | APM's v1 review -- original positions |
| `conversus/specs/001-subject-arbitration/conversus/apm/disputes.md` | APM's v1 disputes -- non-negotiable positions and convergence |
| `conversus/SKILL.md` | Conversus skill definition -- contains SKILL.md/spec drift on trigger evaluation |
| `apm/docs/src/content/docs/introduction/key-concepts.md` | APM primitive taxonomy, constitution injection pattern |
| `apm/docs/src/content/docs/guides/skills.md` | APM skill packaging and distribution model |
