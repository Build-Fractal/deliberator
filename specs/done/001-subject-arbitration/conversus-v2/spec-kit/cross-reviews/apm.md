# Spec-Kit Cross-Review of APM's v2 Review

**Cross-Reviewer**: spec-kit
**Reviewed Agent**: APM
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1. Structured output schema: "acceptable deferral" vs. "downgrade from synthesis mandate"

APM's Missed Opportunity 2 calls the structured output schema deferral "acceptable for v1" and recommends adding lightweight structural conventions (labeled fields like `**Dispute:**`, `**Ruling:**`, `**Grounding:**`) inside the prose template to make future extraction viable. Spec-kit's Missed Opportunity 1 calls the same deferral a "downgrade from what the three-agent process recommended" and demands the schema fields be elevated to a normative FR (proposed FR-028) with a binding commitment that future versions MUST implement them.

These are incompatible remediation strategies. APM's approach embeds extractability into prose conventions -- the schema emerges from parsing. Spec-kit's approach codifies the schema as a first-class requirement -- the schema exists independently of any template's prose structure. If both are applied, the spec would contain a normative FR mandating specific schema fields AND a prose convention that bakes those same fields into template headings, creating two sources of truth for the same contract. When the structured extraction mechanism is eventually designed, implementors would face a choice: parse the prose conventions (APM's model) or implement against the normative schema (spec-kit's model). The synthesis recommended defining the fields normatively and deferring the mechanism. APM's recommendation silently downgrades "define normatively" to "establish conventions." This is the more dangerous of the two positions because it looks like compliance while reducing the commitment.

**Resolution required**: The spec must choose one authority for the schema fields. Spec-kit maintains that normative FR status is the correct choice per the synthesis directive. If APM's prose conventions are also adopted, they must be subordinate to (and validated against) the normative schema, not a substitute for it.

### DC-2. Observation carve-out: "faithfully reconciled" vs. "incomplete audit trail"

APM's Alignment 6 declares FR-015.5 "faithful to the synthesis" and moves on without further comment. Spec-kit's Missed Opportunity 4 identifies the same FR-015.5 as missing documentation of the rejected enforcement models (APM's structural-only, spec-kit's structural + semantic, gh-aw's no-formalization) and the rationale for the chosen position.

This is not a difference of emphasis -- it is a factual disagreement about whether a synthesis obligation has been met. The synthesis identified three competing positions on observation enforceability and resolved them. The spec adopted a position but did not record why the alternatives were rejected. APM's review declares this resolved. Spec-kit's review says it is not. If APM's assessment is accepted, the audit trail for this disputed resolution is permanently incomplete. If spec-kit's assessment is accepted, additional text is required in the spec.

**Resolution required**: The question is whether "adopts a position" equals "resolves a dispute." Spec-kit's position is that resolution requires rationale, not just selection. A deliberation process that produces rulings without reasons is procedurally deficient regardless of whether the ruling itself is correct. APM should clarify whether it considers rationale documentation optional for dispute resolutions.

### DC-3. Success criteria coverage: silent acceptance vs. P1 correctness gap

APM's review does not flag the absence of success criteria for the 10 post-conversus requirements (FR-022 through FR-027, modified FR-011, FR-014, FR-015). Spec-kit identifies this as a P1 correctness issue: without SC entries for failure fallback (FR-022), output validation (FR-023), docs-citation constraint (FR-024), and idempotency (FR-027), the success criteria section does not reflect the spec's actual acceptance bar.

APM's silence implies the existing SC-001 through SC-007 are sufficient. Spec-kit explicitly says they are not. This is a dangerous contradiction because it produces divergent answers to "is this spec ready for implementation planning?" APM's review concludes with recommendations for SKILL.md sync, template contract fixes, and structural conventions -- all of which assume the spec's acceptance criteria are adequate. Spec-kit's review says the acceptance criteria themselves are incomplete.

**Resolution required**: Either APM agrees that new requirements need corresponding success criteria (in which case its review understated a material gap) or APM provides a rationale for why the existing SC set covers the new FRs (in which case spec-kit will evaluate that rationale). There is no middle ground -- a spec either has acceptance criteria for its requirements or it does not.

---

## Tensions

### T-1. SKILL.md drift: same finding, different risk framing

Both reviews flag the SKILL.md trigger evaluation drift as P1. APM frames it as "specification-implementation drift that will produce incorrect behavior" (Missed Opportunity 1). Spec-kit frames it as a "spec-to-implementation consistency fix, not a design change" (Missed Opportunity 3). The remediation is identical (update SKILL.md to reference markers first, headings as fallback). The risk assessment is not: APM implies an implementor following SKILL.md would build fundamentally wrong logic; spec-kit implies the logic would be functionally correct via the fallback path but inconsistent with the spec's intended hierarchy.

This tension matters for prioritization. If APM's framing is correct, the SKILL.md fix blocks implementation. If spec-kit's framing is correct, it is a documentation debt item that should be fixed promptly but does not block a correct implementation (since heading-based parsing, the only mechanism SKILL.md describes, is the designated fallback and would work).

### T-2. Template authoring contract: add requirements vs. narrow scope

APM's Missed Opportunity 3 and P1 item 2 demand that per-file attribution (FR-026) be added to the template authoring contract. Spec-kit's Off-Base Assumption 2 and P2 item 6 demand that the contract be explicitly scoped to cooperative mode, since non-cooperative modes produce different Phase 5 output structures.

These are not contradictory -- both could be applied -- but they create a tension in contract design philosophy. APM is strengthening the contract by adding obligations. Spec-kit is weakening the contract's applicability by narrowing its scope. Applied together, the contract would say more about what cooperative-mode templates must do while simultaneously disclaiming relevance to non-cooperative modes. The risk is that template authors reading a heavily qualified, scope-limited contract treat it as provisional rather than binding.

### T-3. Forward-compatibility: extensibility points vs. scope narrowing

APM wants the trigger enum documented as extensible with unknown values producing validation errors (Missed Opportunity 5, P2 item 5). Spec-kit wants the template authoring contract scoped to cooperative mode with future mode-specific variants explicitly deferred (P2 item 6). Both are forward-compatibility interventions, but they reflect opposing instincts: APM's instinct is to design extension points now so future additions are clean; spec-kit's instinct is to narrow current commitments so future additions are unconstrained. Neither is wrong. The tension is whether the spec should optimize for "future additions are easy" (APM) or "future additions are free to diverge" (spec-kit).

### T-4. Grounding document stability: operational risk vs. not raised

APM identifies the absence of a verification mechanism for grounding document stability as an off-base assumption (Off-Base 1) and proposes content hashing at config validation time with a warning at Phase 6 dispatch. Spec-kit does not raise this concern. The tension is not a disagreement -- spec-kit did not evaluate and reject the concern; it simply did not surface it. APM's analysis is reasonable: a 30+ minute conversus run could encounter concurrent edits. However, the mitigation (content hashing) introduces implementation complexity that exceeds the stated scope of v1. Spec-kit's implicit position is that the stability assumption is acceptable as an assumption, since assumptions are by definition unverified constraints on the operating environment. Verifying assumptions converts them into requirements, which is a scope expansion.

### T-5. "Binding" semantics: misleading term vs. accepted terminology

APM's Off-Base Assumption 2 flags that "binding" decisions are only binding within the deliberation record, not on downstream actors, and recommends clarifying language (P3 item 8). Spec-kit does not raise this. The tension: APM sees ambiguity in a core term; spec-kit either considers the meaning self-evident from context ("final for this conversus run" in Key Entities) or considers it an acceptable term-of-art that does not require disambiguation. Spec-kit's position, stated here: the Key Entities definition is adequate, but APM's proposed clarifying sentence is harmless and could be adopted without objection.

---

## Safe Agreements

### SA-1. The 8 convergence points from the synthesis are faithfully integrated

Both reviews independently verify that all convergence points from the v1 synthesis are present, traceable to specific spec text, and not diluted. APM's Alignment section 1-6 and spec-kit's Alignment section 1-6 cover overlapping ground and reach the same conclusion: grounding singularity, failure semantics, cooperative-only restriction, structural HTML markers, docs-vs-grounding distinction, and non-cooperative template gating are all correctly integrated. There is no daylight between the two reviews on these points.

### SA-2. FR-011 (structural HTML markers) and FR-024 (docs-vs-grounding) are well-calibrated

Both reviews specifically call out these two FRs as precisely calibrated integrations of the synthesis recommendations. APM describes the marker mechanism as "the right call" and the docs distinction as "precisely calibrated." Spec-kit describes the marker mechanism as implementing "the exact hierarchy the synthesis prescribed" and the docs distinction as "the exact formalization spec-kit requested." These are the two strongest points of agreement and represent the spec's most successful synthesis integrations.

### SA-3. FR-022 (failure semantics) and FR-023 (output validation) are comprehensive

Both reviews confirm that the failure/validation split is correct: FR-022 handles catastrophic failure (agent crash, timeout) with Phase 5 fallback, while FR-023 handles structural non-conformance (successful but malformed output) with a warning-not-blocking approach. Both reviews credit this as faithful to the synthesis's unanimous convergence. APM notes the warning approach "avoids the failure mode where valid reasoning is discarded"; spec-kit notes the split "correctly distinguishes catastrophic failure from structural non-conformance."

### SA-4. SKILL.md trigger evaluation must be updated (P1)

Both reviews independently identify the SKILL.md trigger evaluation drift and classify it as P1. The diagnosis is identical: SKILL.md describes only heading-based parsing; the spec mandates markers as primary. The prescribed fix is identical: update SKILL.md to check for structural markers first, fall back to heading parsing. This is the single highest-priority action item on which both reviews fully agree in finding, classification, and remediation.
