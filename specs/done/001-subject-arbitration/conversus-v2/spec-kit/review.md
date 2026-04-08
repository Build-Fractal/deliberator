# Spec-Kit v2 Review: Subject Arbitration (Phase 6)

**Reviewer**: spec-kit (SDD framework)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Review Type**: v2 post-synthesis integration review
**Prior Review**: [`conversus/spec-kit/review.md`](../../conversus/spec-kit/review.md)
**Synthesis**: [`conversus/summary/final.md`](../../conversus/summary/final.md)

---

## Executive Summary

The spec has absorbed the v1 conversus process well. Of the 17 actionable spec changes recommended by the synthesis, 15 are integrated correctly, 1 is partially integrated, and 1 is structurally present but functionally incomplete. The spec is materially stronger than the pre-conversus draft: failure semantics (FR-022), output validation (FR-023), structural trigger markers (FR-011), the docs-vs-grounding distinction (FR-024), per-file attribution (FR-026), requirement-identifier traceability (FR-025), grounding document stability (Assumptions), idempotency semantics (FR-027), and the information-asymmetry reframe (Assumptions) are all correctly integrated.

The remaining gaps are concentrated in two areas: (1) the structured output schema is deferred but the deferral contract is weaker than what the synthesis prescribed, and (2) the observation carve-out resolution (FR-015.5) adopts a position but does not fully document the rejected alternatives or the rationale for choosing one enforcement model over another. Neither gap is a correctness defect -- both are completeness issues that affect downstream consumers (SDD pipeline, template authors) more than Phase 6 runtime behavior.

From spec-kit's perspective, the spec is now ready for implementation planning. The deferred structured output schema is the only item that will require a follow-up spec before the SDD pipeline can consume arbitration output programmatically.

---

## Alignment

### 1. Convergence points are faithfully integrated

All 8 convergence points from the synthesis are present in the spec. The grounding singularity (FR-002, FR-024), Phase 6 failure semantics (FR-022), cooperative-only restriction (FR-004, Constraints), backward compatibility (FR-005), structural HTML markers (FR-011), information-asymmetry reframe (Assumptions), schema versioning deferral (absence is correctness), and template extensibility (FR-013, FR-014) are all traceable to specific spec text. The spec does not silently drop or dilute any convergence point.

### 2. The trigger mechanism is correctly layered

FR-011 implements the exact hierarchy the synthesis prescribed: structural HTML markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`) as the primary mechanism, heading-based parsing (`### Remaining Disputes` with `**Dispute:` entries) as the backward-compatible fallback. The `{REMAINING_DISPUTES}` variable (FR-014) extracts content between the markers, satisfying spec-kit's conditional concession from Dispute 2. The Assumptions section correctly elevates the marker requirement to a MUST for Phase 5 synthesis templates. This resolves the original fragility that all three agents flagged.

### 3. The docs-vs-grounding distinction is normatively specified

FR-024 ("The `docs` field provides read-only context only. Only the `grounding` document MAY be cited as authority in binding decisions. Citations to `docs` entries are permitted for factual context but MUST NOT serve as the sole basis for a ruling.") is the exact formalization spec-kit requested in N-3 and the synthesis recommended in P1 item 5. The "sole basis" qualifier is a pragmatic addition -- it permits contextual references to docs without opening the citation-laundering vector. This is a well-calibrated integration.

### 4. Non-cooperative template status is explicitly addressed

The Constraints section includes: "Non-cooperative mode arbitration templates are draft/experimental. They MUST NOT be activatable in v1." The `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker mechanism is specified. The engine filtering requirement is stated. This resolves Dispute 2 from the synthesis by adopting spec-kit's in-place-with-markers position while incorporating gh-aw's concern about automated discovery. The spec chose the marker approach over filesystem relocation, which preserves the naming convention and makes future activation a config change rather than a file move.

### 5. Failure semantics are comprehensive and correctly scoped

FR-022 covers agent failure (timeout, crash, malformed output), preserves Phase 5 as the terminal state, requires a diagnostic warning, prevents partial output, and protects the Phase 1-5 record. This matches the unanimous convergence point exactly. The separation between FR-022 (failure semantics) and FR-023 (output validation for successful-but-malformed output) correctly distinguishes catastrophic failure from structural non-conformance -- a nuance the synthesis implied but did not explicitly separate.

### 6. The Implementation Guidance section is appropriately non-normative

The spec correctly separates normative requirements (FR-xxx, SC-xxx) from non-normative guidance (Implementation Guidance section). The spec-kit project convention, grounding document requirements, template authoring contract, structured output schema deferral, and trigger quorum future work are all in the non-normative section. This follows spec-kit's own pattern where the spec defines WHAT and WHY, and the plan defines HOW.

---

## Missed Opportunities

### 1. Structured output schema deferral lacks a binding commitment to the schema fields

The synthesis P3 item 12 recommended: "Normatively define the fields: dispute ID, ruling type, grounding citation, required changes, affected target file, confidence level. Defer the production mechanism to v2 if needed, but define the schema now." The spec's Implementation Guidance section lists these fields under "Structured Output Schema (Deferred)" but frames them as "defined for future structured extraction" rather than as a normative schema that future versions MUST implement. The difference matters: a normative schema in the Requirements section constrains future design; a non-normative schema in Implementation Guidance is advisory. The synthesis wanted the former. The spec delivers the latter. This is a downgrade from what the three-agent process recommended.

### 2. No validation that the `{REMAINING_DISPUTES}` variable content is non-empty when the trigger fires

FR-011 checks for "at least one dispute entry" between the structural markers to determine whether to trigger Phase 6. FR-014 defines `{REMAINING_DISPUTES}` as "content extracted from between the markers." But nothing validates that the extracted content is meaningful -- if the markers exist but contain only whitespace or a stale placeholder, the trigger fires and the arbiter receives empty dispute content. The trigger evaluation (FR-011) and the variable extraction (FR-014) are decoupled in a way that could produce a Phase 6 invocation with no actual dispute material to arbitrate.

### 3. SKILL.md trigger evaluation does not reference structural markers

The SKILL.md Phase 6 trigger evaluation section (line 255) still describes only heading-based parsing: "Find the `### Remaining Disputes` heading. Check whether there is at least one `**Dispute:` entry under it." It does not mention the structural HTML markers that FR-011 now designates as the primary mechanism. This is a spec-to-implementation drift: the spec says markers are primary and headings are fallback, but the implementation guidance in SKILL.md only describes the fallback.

### 4. The observation carve-out (FR-015.5) does not document the rejected enforcement models

The synthesis identified three competing positions on observation enforceability (APM: structural-only, spec-kit: structural + semantic, gh-aw: no formalization). FR-015.5 adopts a position (observations permitted in Confidence Assessment, labeled non-binding, not prescribing changes) but does not record why the other models were rejected. For a spec that went through a formal deliberation process, the absence of rationale for disputed resolutions weakens the audit trail. Template authors who later encounter the rule will not know why it was chosen over the alternatives.

### 5. Success criteria do not cover the new requirements

SC-001 through SC-007 were written before the conversus process. The 10 new functional requirements (FR-022 through FR-027, plus the modifications to FR-011, FR-014, FR-015) have no corresponding success criteria. For example: there is no SC for "Phase 6 failure falls back to Phase 5 with a warning" (FR-022), no SC for "output validation flags malformed resolution" (FR-023), and no SC for "re-running Phase 6 overwrites previous output" (FR-027). This creates a gap between what the spec requires and what the spec declares success looks like.

---

## Off-Base Assumptions

### 1. The structured output schema fields assume a one-dispute-one-file mapping

The deferred schema includes `affected_target_file` as a singular field per dispute ruling. In multi-target conversus runs, a single dispute may affect multiple files (e.g., a dispute about data model naming affects both `spec.md` FR definitions and `data-model.md` entity definitions). The schema should use a list type for `affected_target_file` or acknowledge that a ruling may map to multiple files. The current singular field will force either duplicate entries or lossy representation when the schema is eventually implemented.

### 2. The template authoring contract assumes Phase 5 output structure is stable across modes

The Implementation Guidance section states that Phase 6 templates consume `{SYNTHESIS_PATH}`, `{REMAINING_DISPUTES}`, `{ALL_DISPUTES}`, and `{TARGET_FILES}`. This contract assumes that all modes produce the same Phase 5 output structure (specifically, the structural markers). But non-cooperative modes have fundamentally different Phase 5 outputs (trust-scored responsibility maps for PD, risk verdicts for Red-Blue). When non-cooperative arbitration is eventually activated, the template authoring contract will need mode-specific variants. The current contract is correct for cooperative mode but is written as if it were mode-universal.

---

## Actionable Recommendations

### P1 -- Required for Correctness

1. **Update SKILL.md trigger evaluation to match FR-011's marker-primary, heading-fallback hierarchy.** The SKILL.md Phase 6 trigger evaluation (Step 4, Phase 6 section) currently describes only heading-based parsing. It must be updated to check for `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers first, then fall back to heading parsing if markers are absent. This is a spec-implementation consistency fix, not a design change. The spec already prescribes the correct behavior; the implementation guidance lags behind.

2. **Add success criteria for the post-conversus requirements.** At minimum, add SC entries for: (a) Phase 6 failure produces Phase 5 terminal state with diagnostic warning (covers FR-022), (b) malformed resolution output triggers a validation warning (covers FR-023), (c) `docs` citations are never the sole basis for a binding ruling (covers FR-024), (d) re-running Phase 6 overwrites previous output (covers FR-027). Without these, the success criteria section does not reflect the spec's actual acceptance bar.

3. **Add a content-presence check between trigger evaluation and variable extraction.** FR-011 should include: "If the structural markers are present but contain only whitespace, the trigger evaluates to `false` (no disputes remain)." This prevents Phase 6 from running with an empty `{REMAINING_DISPUTES}` variable, which would produce an arbitration against nothing.

### P2 -- Required for Design Integrity

4. **Elevate the structured output schema fields from Implementation Guidance to a normative FR.** Create FR-028: "A future version that implements structured extraction from arbitration output MUST support at minimum the following fields: `dispute_id`, `ruling_type`, `grounding_citation`, `required_changes`, `affected_target_files` (list), `confidence_level`. The production mechanism is deferred." This preserves the deferral of the mechanism while making the schema commitment normative rather than advisory. Note the pluralization of `affected_target_files` to handle multi-file disputes.

5. **Add a Conversus Review Rationale subsection for disputed resolutions.** Under the existing "Conversus Review" section at the end of the spec, add brief rationale for the 4 dispute resolutions: structured output (deferred -- mechanism disputed, schema advisory), template placement (in-place with markers -- preserves naming convention), observation enforceability (structural + labeling -- minimum enforceable rule), low-confidence behavior (informational only -- avoids perverse incentives). This completes the audit trail that the deliberation process exists to produce.

6. **Scope the template authoring contract to cooperative mode.** Change "Phase 6 templates consume the following Phase 5 output elements" to "Cooperative-mode Phase 6 templates consume the following Phase 5 output elements." Add a note: "Non-cooperative modes may produce different Phase 5 output structures. Template authoring contracts for non-cooperative arbitration will be defined when those modes are activated." This prevents template authors from assuming the contract is mode-universal.

### P3 -- Recommended Improvement

7. **Add a `{TRIGGER_REASON}` template variable for the arbitration template.** The SKILL.md already defines `{TRIGGER}` (the trigger condition), but the arbiter's Process Note section would benefit from knowing why Phase 6 was activated -- "4 disputes remained" is more informative than "trigger: disputes_remain." The variable could contain the dispute count extracted during trigger evaluation. This is a small template-quality improvement that makes arbitration output more self-documenting.

8. **Document the interaction between `trigger: always` and the `{REMAINING_DISPUTES}` variable.** When `trigger: always` fires with zero remaining disputes, `{REMAINING_DISPUTES}` will be empty (no content between markers, or no markers at all). The template must handle this case -- the arbiter receives a "subject endorsement" instruction (US1-AS3) but an empty disputes variable. The template authoring contract should note this edge case explicitly.

---

## Referenced Documentation

| Document | Path | Relevance |
|----------|------|-----------|
| Subject Arbitration Spec (v2) | `conversus/specs/001-subject-arbitration/spec.md` | Primary review target |
| Conversus SKILL.md | `conversus/SKILL.md` | Implementation guidance, Phase 6 trigger evaluation drift |
| v1 Synthesis | `conversus/specs/001-subject-arbitration/conversus/summary/final.md` | 17 actionable changes, 8 convergence points, 4 disputes |
| spec-kit v1 Review | `conversus/specs/001-subject-arbitration/conversus/spec-kit/review.md` | Original 10 recommendations |
| spec-kit v1 Disputes | `conversus/specs/001-subject-arbitration/conversus/spec-kit/disputes.md` | Final positions on 4 disputes |
| spec-kit v1 Revision | `conversus/specs/001-subject-arbitration/conversus/spec-kit/revision.md` | Modified/withdrawn positions |
| Spec-Kit Spec Template | `spec-kit/templates/spec-template.md` | SDD spec structure requirements |
| Spec-Kit Constitution Template | `spec-kit/templates/constitution-template.md` | Grounding document parallel |
| Spec-Kit README | `spec-kit/README.md` | SDD philosophy and workflow |
