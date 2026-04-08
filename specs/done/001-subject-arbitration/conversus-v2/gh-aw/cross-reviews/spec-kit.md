# gh-aw Cross-Review of spec-kit's v2 Review

**Cross-reviewer**: gh-aw
**Target review**: spec-kit v2 review (`conversus-v2/spec-kit/review.md`)
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Structured output schema -- normative FR vs. advisory guidance

spec-kit (Recommendation P2-4) demands the deferred structured output schema be elevated to a normative FR (proposed FR-028) that constrains future design: "A future version that implements structured extraction MUST support at minimum the following fields." gh-aw (Recommendation P3-8) recommends only extracting the schema into a standalone "Future Work" section for visibility, explicitly calling it "a documentation organization concern, not a correctness concern."

These positions contradict on whether the schema fields should carry normative weight. spec-kit wants a binding contract that locks future implementors into specific field names and types before any implementation experience exists. gh-aw treats the same fields as advisory placeholders that inform future design without constraining it. The danger: if spec-kit's position is adopted, the schema becomes a compatibility obligation before anyone has built the extraction pipeline. If the first implementation reveals that `ruling_type` should be an enum rather than a string, or that `confidence_level` needs to be a structured object rather than a scalar, the normative FR forces a spec amendment process for what should be an implementation discovery. Premature normative commitment to deferred features is how specs accumulate dead-letter requirements.

gh-aw's position: the schema fields should remain non-normative until at least one implementation attempt validates the field model. Document them visibly, but do not create a normative obligation for work that has not been designed.

### DC-2: Template filtering -- content inspection vs. location-based discovery

spec-kit (Alignment 4) endorses the draft template marker approach (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`) as the correct resolution, calling it a design that "preserves the naming convention and makes future activation a config change rather than a file move." gh-aw (Off-Base Assumption 1) explicitly rejects this pattern as contrary to how template discovery works: "A file at `templates/prisoners-dilemma/arbitration.md` will be discovered by `templates/*/arbitration.md` globs regardless of what HTML comments it contains."

The contradiction is architectural. spec-kit's SDD pipeline resolves template status through document metadata (frontmatter, markers) -- content-aware filtering is native to that model. gh-aw's compilation model resolves template discoverability through filesystem location -- a file's path determines whether it enters the pipeline, not its content. Both reviews agree the engine "MUST" filter drafts, but they disagree on whether content-based filtering is a sound mechanism. gh-aw's review further identifies that no FR actually requires the engine to parse the marker (Missed Opportunity 1), making the MUST in the Constraints section unimplementable without additional specification work. spec-kit treats the marker as sufficient; gh-aw treats it as creating technical debt that directory-based separation would avoid.

The danger: an implementor following spec-kit's reading builds a content-aware template loader. An implementor following gh-aw's reading builds a directory-based template loader with a `_draft/` convention. Both believe they are compliant with the spec. The implementations are incompatible.

### DC-3: Success criteria gap -- severity assessment

spec-kit (Missed Opportunity 5) identifies that the 10 post-conversus requirements (FR-022 through FR-027 and modifications to FR-011, FR-014, FR-015) lack corresponding success criteria and elevates this to P1 (Required for Correctness), recommending 4 new SC entries. gh-aw's review does not mention success criteria at all -- not in Alignment, Missed Opportunities, or Recommendations.

This is not a difference in how to fix the gap; it is a difference in whether the gap matters. spec-kit treats success criteria as a structural requirement of well-formed specifications: if FRs exist without SCs, the spec is incomplete. gh-aw's silence implies that success criteria are downstream artifacts that do not affect the spec's correctness or implementability. From gh-aw's operational perspective, an FR with RFC 2119 keywords is testable by definition -- the MUST/SHOULD/MAY language is the acceptance criterion. From spec-kit's SDD perspective, explicit SCs are the bridge between spec and test plan, and their absence creates a verification gap.

The danger: if both perspectives are left unreconciled, the spec has a structural ambiguity about what constitutes "complete." spec-kit's SDD pipeline will flag the spec as incomplete (missing SCs). gh-aw's CI pipeline will treat the FRs as testable requirements and proceed. Downstream consumers inherit whichever interpretation their toolchain imposes.

---

## Tensions

### T-1: `{REMAINING_DISPUTES}` extraction validation -- same concern, different scoping

Both reviews identify the missing validation of `{REMAINING_DISPUTES}` content after extraction. spec-kit (Missed Opportunity 2, Recommendation P1-3) frames it as a trigger-evaluation concern: "If the structural markers are present but contain only whitespace, the trigger evaluates to `false`." gh-aw (Missed Opportunity 2, Recommendation P3-6) frames it as a data-flow concern: the engine should "log a diagnostic if the extraction is empty when the trigger evaluated to `true`."

The tension: spec-kit wants to prevent Phase 6 from running (change trigger semantics); gh-aw wants Phase 6 to run but emit a warning (preserve trigger semantics, add observability). spec-kit's approach is safer but breaks the `trigger: always` override. gh-aw's approach preserves all trigger modes but relies on downstream consumers to act on the warning. Neither review addresses what happens when their preferred approach interacts with the other's trigger scenarios.

### T-2: FR-022/FR-023 boundary -- one review sees a conflict, the other sees clean separation

gh-aw (Missed Opportunity 3, Recommendation P1-1) identifies an explicit conflict between FR-022 ("malformed output" triggers failure, no file written) and FR-023 (validation failure emits warning, file IS written). gh-aw recommends disambiguating by scoping FR-022 to agent-process failure and FR-023 to output-content validation. spec-kit (Alignment 5) reads the same two requirements and concludes they are "correctly distinguished" -- "a nuance the synthesis implied but did not explicitly separate."

The tension is interpretive. spec-kit sees the FR-022/FR-023 relationship as clear from context. gh-aw sees it as ambiguous to an implementor who reads "malformed output" in FR-022 and "validation fails" in FR-023 as describing the same state. Both reviews are reading the same spec text and arriving at different conclusions about its clarity, which is itself evidence that the text is ambiguous. If two careful reviewers disagree on whether a distinction is explicit, implementors will also disagree.

### T-3: The `trigger: always` endorsement path -- acknowledged vs. analyzed

Both reviews flag the `trigger: always` + no-disputes edge case. spec-kit (Recommendation P3-8) treats it as a documentation gap: "Document the interaction between `trigger: always` and the `{REMAINING_DISPUTES}` variable." gh-aw (Off-Base Assumption 2, Recommendation P2-5) treats it as a design gap: the template instructions become "vacuous" when no disputes exist, and the spec needs either a separate endorsement format, conditional template logic, or an explicit acknowledgment.

The tension is in severity. spec-kit says "document the edge case." gh-aw says "design for the edge case." spec-kit's position implies the current template can handle it with adequate documentation. gh-aw's position implies the current template structurally cannot handle it because its instructions presuppose disputes. This maps to a broader pattern: spec-kit trusts template authors to interpret instructions flexibly; gh-aw wants the spec to eliminate ambiguity before it reaches the template author.

### T-4: SKILL.md drift -- P1 concern vs. unmentioned

spec-kit (Missed Opportunity 3, Recommendation P1-1) identifies that SKILL.md's Phase 6 trigger evaluation still describes only heading-based parsing and does not reference the structural markers that FR-011 designates as primary. spec-kit classifies this as P1 (Required for Correctness). gh-aw's review does not mention SKILL.md at all.

The tension reveals a scope difference. spec-kit treats SKILL.md as an implementation artifact that must track the spec. gh-aw treats the spec as the authoritative source and does not audit downstream implementation documents against it. Both are defensible scopes for a v2 review, but the practical consequence is that spec-kit's review catches a real drift that gh-aw's review misses entirely. If SKILL.md is used as the runtime prompt for the conversus engine, this drift could cause the engine to use the fallback mechanism as the only mechanism, silently ignoring the primary trigger path.

### T-5: Observation carve-out rationale -- audit trail vs. shipped spec

spec-kit (Missed Opportunity 4, Recommendation P2-5) flags that FR-015.5's observation carve-out does not document rejected alternatives or rationale, and recommends adding a "Conversus Review Rationale" subsection for all 4 dispute resolutions. gh-aw's review does not raise this concern. gh-aw's review focuses on whether the adopted positions are operationally sound, not on whether the rejection rationale is recorded.

The tension is about what a spec owes its readers. spec-kit's SDD model treats rationale as a first-class spec artifact -- the "why" is as important as the "what." gh-aw's operational model treats the spec as a contract: if the adopted position is clear and implementable, the rejected alternatives are historical context that belongs in the conversus record, not the spec itself. Both are legitimate positions, but they produce different spec structures.

---

## Safe Agreements

### SA-1: The spec is materially stronger and ready for implementation

Both reviews open with the same assessment. spec-kit: "the spec is materially stronger than the pre-conversus draft" and "now ready for implementation planning." gh-aw: "the spec is materially stronger than the pre-synthesis version." Both reviews confirm that the core convergence points -- failure semantics (FR-022), structural markers (FR-011), output validation (FR-023), grounding singularity (FR-024), idempotency (FR-027), cooperative-only restriction (FR-004) -- are faithfully integrated. Neither review identifies a blocking defect that would prevent implementation from proceeding.

### SA-2: The docs-vs-grounding citation boundary (FR-024) is correctly specified

spec-kit (Alignment 3) calls FR-024 "the exact formalization spec-kit requested" and praises the "sole basis" qualifier as "well-calibrated." gh-aw (Missed Opportunity 5) calls the boundary "sound" and agrees with the semantic design. Both reviews accept FR-024's substance. gh-aw's additional recommendation (P2-4) to add an explicit template instruction mirroring FR-024 in FR-015 is an enforcement concern, not a disagreement with the boundary itself. Both agents agree on what the rule says; they differ only on how aggressively the template should restate it.

### SA-3: Non-cooperative templates must not be activatable in v1

Both reviews confirm that the cooperative-only restriction is correctly specified. spec-kit (Alignment 4) validates the Constraints section language and the marker mechanism. gh-aw (Alignment, implicit in the FR-004 references) confirms that FR-004 correctly rejects non-cooperative activation at config validation time. The disagreement on HOW to prevent activation (markers vs. directory separation) does not extend to WHETHER to prevent it -- both reviews treat v1 cooperative-only as a settled convergence point.

### SA-4: The template authoring contract fills a real gap

spec-kit (Alignment, via the trigger mechanism and template extensibility validation) and gh-aw (Alignment 5) both affirm that the Implementation Guidance section's template authoring contract addresses a gap from the v1 spec. spec-kit validates the Phase 5-to-Phase 6 data flow variables. gh-aw validates the four template invariants. Neither review challenges the contract's substance; both treat it as a correct adoption of recommendations from the v1 round.

---

## Summary

The two reviews converge on the spec's overall quality and readiness. The dangerous contradictions cluster around the boundary between spec-kit's document-metadata model and gh-aw's filesystem-location model (template filtering), the appropriate normative weight for deferred features (structured output schema), and the definition of spec completeness (success criteria). The tensions reveal consistent patterns: spec-kit reads the spec through the lens of SDD structural requirements (rationale, SCs, SKILL.md sync); gh-aw reads it through the lens of operational implementability (failure-state disambiguation, trigger semantics, template behavior under edge cases). These are complementary perspectives, not irreconcilable ones, but the three dangerous contradictions require explicit resolution before implementation to prevent divergent interpretations.
