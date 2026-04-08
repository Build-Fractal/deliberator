# Arbitration: Binding Resolutions

**Arbiter**: The Subject (spec owner)
**Date**: 2026-03-19
**Grounding Document**: `/Users/business-daddy/code/payer-index-mono/conversus/specs/001-subject-arbitration/spec.md`
**Scope**: 3 micro-disputes surviving the 4-phase cooperative-mode dispute resolution process

---

## Process Note

Phase 5 synthesis identified 3 remaining micro-disputes after 4 phases of deliberation by 3 agents (Mechanist, Pragmatist, Purist). All 4 original blockers reached unanimous or 2:1 resolution. The 3 micro-disputes are narrow calibration questions within settled architectural decisions. This Phase 6 arbitration resolves each with a binding decision grounded in the spec's own requirements and design values.

---

## Decision Framework

The grounding document is the spec itself: `spec.md` for Feature Specification: Subject Arbitration (Phase 6). Rulings are grounded in:

- The spec's functional requirements (FR-001 through FR-027)
- The spec's success criteria (SC-001 through SC-007)
- The spec's stated constraints and design values
- The spec's edge case definitions and implementation guidance

The arbiter evaluates each dispute against the spec's internal consistency requirements and its stated design philosophy, particularly the principle articulated in FR-012: "better to run the arbiter unnecessarily than to skip it when disputes exist" -- which establishes a system-wide preference for false positives over false negatives, and more broadly, for action over inaction when costs are asymmetric.

---

## Binding Decisions

### Micro-Dispute A: Prose Conventions -- MAY vs. SHOULD (Blocker 2 Residual)

**Dispute**: The Purist maintains that template-author prose conventions (`**Dispute:**`, `**Ruling:**`, etc.) should be stated at SHOULD-level in the deferred structured output section. The Mechanist and Pragmatist maintain MAY-level in Implementation Guidance. The question is both the normative weight (MAY vs. SHOULD) and the document location (Implementation Guidance vs. deferred section).

**Positions**:

- **Mechanist**: MAY in Implementation Guidance. SHOULD creates unenforceable pseudo-contracts. The engine cannot validate prose conventions, so normative language suggesting compliance is expected will lure downstream consumers into depending on something the system does not guarantee.
- **Pragmatist**: MAY in Implementation Guidance. Retreated from SHOULD after acknowledging the Mechanist's argument. MAY communicates "here is a useful pattern" without creating an obligation. Accepts that this reduces naming entropy without creating false contracts.
- **Purist**: SHOULD in the deferred section. Argues that the spec already contains unenforceable behavioral constraints (FR-015, FR-024), so adding SHOULD-level formatting conventions is architecturally identical. Implementation Guidance is where implementors look for engine behavior, not where template authors look for output expectations. The deferred section is the audience-appropriate location.

**Ruling**: **MAY in Implementation Guidance. The 2:1 majority position is adopted.**

**Grounding**: The spec draws a clear architectural line between the normative output contract and advisory guidance. FR-018 defines the section headings as the sole v1 output contract. The spec's Constraints section states: "The arbiter MUST NOT introduce new recommendations." By analogy, the spec itself should not introduce normative obligations (SHOULD) for conventions it explicitly defers and cannot enforce. The spec's own deferred section header -- "Structured Output Schema (Deferred)" -- signals that this content is not yet normative.

The Purist's argument about FR-015 is substantive but distinguishable. FR-015's behavioral constraints (e.g., "do NOT introduce new recommendations") are instructions to the arbiter agent within a template -- they shape LLM generation behavior for a single invocation. SHOULD-level prose conventions in the deferred section are instructions to human template authors across all future template versions -- they create a standing expectation that accrues contractual force through repetition, exactly as the Mechanist warned. The enforcement surface differs: FR-015 is consumed by the engine and injected into a prompt; deferred-section SHOULD conventions are consumed by humans reading the spec. The Pragmatist's self-diagnosis -- "I was doing purist work under a pragmatist banner" -- applies symmetrically: SHOULD in a deferred section is doing normative work under an advisory banner.

The Purist's document-location concern (Implementation Guidance vs. deferred section) is legitimate but separable from the normative-level question. The MAY-level guidance may be placed in either location as an editorial decision. The binding ruling is on normative level: MAY, not SHOULD.

**Rejected Position**: SHOULD-level conventions in the deferred section. The asymmetry between engine-enforced and human-enforced SHOULD obligations is real. When the engine cannot validate compliance, SHOULD creates an obligation that no actor in the system can discharge, which erodes the meaning of SHOULD across the entire spec.

**Required Change to spec.md**:

Add to Implementation Guidance (after the "Template Authoring Contract" subsection):

> ### Prose Convention Guidance
>
> Template authors MAY use labeled sub-fields (e.g., `**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Required Changes:**`) as instructional hints to improve output regularity. This is a template-author design decision, not a spec-level contract. The engine does not validate sub-field presence or format.

No changes to the deferred structured output section's normative level. The existing "advisory for v1" framing is retained.

---

### Micro-Dispute B: Vacuous-Output Arbiter Instruction (Blocker 1 / Blocker 3 Residual)

**Dispute**: The Purist proposes adding a one-sentence behavioral constraint to FR-015: "If the arbiter determines that no actionable disputes exist in the input, the Binding Decisions section MUST state this explicitly rather than producing fabricated or speculative rulings." The Pragmatist considers SC-014 (post-hoc detection of zero binding decisions) sufficient. The Mechanist endorsed SC-014 and the Purist's report-level distinction as complementary but did not explicitly address the FR-015 instruction.

**Positions**:

- **Purist**: Add the instruction to FR-015. The content-negative trigger (Blocker 1 resolution) makes zero-dispute input a foreseeable condition, not an edge case. Foreseeable conditions require defined behavior. Without guidance, arbiters may hallucinate disputes to fill sections. One sentence, zero implementation cost.
- **Pragmatist**: SC-014 is sufficient. It detects vacuous output after the fact. The trigger definition is not the right fix because vacuous output can arise from multiple causes. Adding another behavioral constraint to FR-015 is prevention, and prevention belongs in the template, which already shapes arbiter behavior.
- **Mechanist**: Endorsed both SC-014 and the Purist's report-level distinction as complementary. Did not explicitly oppose the FR-015 addition.

**Ruling**: **Accept the Purist's proposed FR-015 addition. Both SC-014 and the FR-015 instruction are included.**

**Grounding**: The spec's edge case section already addresses this exact scenario: "What happens when the arbiter declares it cannot resolve a dispute? The arbiter should write: 'UNRESOLVED -- insufficient information to make a grounded decision.'" This establishes the spec's own precedent that foreseeable arbiter input conditions should have defined arbiter response behavior, not just post-hoc detection. The Purist's proposal is architecturally identical to this existing edge case definition -- it defines what the arbiter should do when an input condition arises, rather than relying solely on after-the-fact detection.

Furthermore, FR-015 already contains six behavioral constraints, all of which are prevention-oriented instructions to the arbiter agent. Adding a seventh that addresses a foreseeable input condition created by the Blocker 1 resolution (content-negative trigger) is consistent with the existing pattern. The spec's Constraints section states: "The arbiter MUST NOT introduce new recommendations. It resolves existing disputes -- it does not add to the deliberation record." The vacuous-input instruction is the logical complement: when there are no disputes to resolve, the arbiter must not fabricate them.

The Pragmatist's argument that SC-014 is sufficient confuses detection with prevention. The synthesis itself established the functional decomposition: "template is the primary prevention mechanism [...] engine is the primary detection mechanism." SC-014 is detection. The FR-015 instruction is prevention. Both are needed, by the architecture all three agents unanimously adopted for Blocker 4.

The Mechanist's silence on this point, combined with explicit endorsement of both SC-014 and the Purist's report-level distinction, is read as non-opposition.

**Rejected Position**: SC-014-only. Post-hoc detection without defined prevention behavior violates the template-prevention / engine-detection architecture that all three agents converged on for Blocker 4. The cost of the addition is one sentence. The cost of omission is undefined arbiter behavior on a foreseeable input condition.

**Required Change to spec.md**:

In FR-015, after instruction 7 (citation boundary), add instruction 8:

> 8\. If no actionable disputes exist in the input, state this explicitly in the Binding Decisions section rather than producing fabricated or speculative rulings

Add SC-014 to the Success Criteria section:

> - **SC-014**: Given a Phase 6 run where the arbiter produces output with all FR-018 section headings but zero binding decisions in the Binding Decisions section, When the engine validates the output, Then `resolution.md` is written and a validation warning is emitted: "Arbitration produced zero binding decisions -- verify dispute trigger content."

---

### Micro-Dispute C: SC-011 Normative Level -- SHOULD vs. MUST for Requirement Identifier References

**Dispute**: SC-011 addresses binding decisions that use vague references (e.g., "the validation requirement") instead of specific identifiers (e.g., "FR-003") when the grounding document contains numbered requirements. The Pragmatist's formulation emits a validation warning (implying MUST-level detection). The Purist conditions the SC with "SHOULD reference specific identifiers" (implying a quality recommendation, not a hard requirement). The question is whether vague references produce a mandatory warning or are merely discouraged.

**Positions**:

- **Pragmatist**: Validation warning on vague references. The engine should actively flag this. If FR-025 requires specific identifiers, the SC that tests FR-025 should enforce it.
- **Purist**: SHOULD-level quality check, not blocking validation. Conditioned with "When the grounding document contains numbered requirements" to scope it appropriately. Vague references are undesirable but should not produce a warning that could be confused with a structural validation failure.
- **Mechanist**: Adopted the Pragmatist's SC formulation in the final position but did not explicitly address the SHOULD vs. MUST tension.

**Ruling**: **SHOULD-level quality check with a validation warning. The warning is emitted but explicitly labeled as a quality advisory, not a structural validation failure.**

**Grounding**: FR-025 states: "the arbiter's Required Changes MUST cite specific identifiers rather than making vague references." This is a MUST-level requirement on the arbiter's behavior. However, the spec's own architecture distinguishes between what the engine can check deterministically and what requires heuristic or human review. This distinction was a key convergence point (Convergence Point 15 in the synthesis: "Engine validation is heuristic (not deterministic) for citation checks"). Detecting whether a reference is "vague" vs. "specific" is a semantic judgment the engine cannot make deterministically -- unlike string-presence checks for section headings or grounding document paths.

The spec's FR-023 establishes the pattern: validation warnings are informational, not blocking. The file is still written. This same pattern applies to SC-011: the engine emits a warning when it detects potential vague references (a SHOULD-level quality check), but this warning is explicitly a quality advisory distinct from the structural warnings defined in FR-023.

The Purist's conditioning -- "When the grounding document contains numbered requirements or identifiers" -- is adopted because it scopes the check appropriately. A grounding document without numbered identifiers cannot produce specific identifier citations, and flagging their absence would be a false positive.

**Rejected Position**: Unconditional MUST-level validation warning without quality-advisory labeling. This would conflate a semantic quality check with the deterministic structural checks (heading presence, grounding-path presence) that the spec treats as MUST-level, undermining the carefully drawn boundary between deterministic and heuristic validation that all three agents converged on.

**Required Change to spec.md**:

Add SC-011 to the Success Criteria section:

> - **SC-011**: Given binding decisions that reference requirements in target documents using vague references (e.g., "the validation requirement") instead of specific identifiers (e.g., "FR-003"), When the grounding document contains numbered requirements or identifiers, Then a validation warning is emitted. This is a SHOULD-level quality advisory, not a structural validation failure. The warning SHOULD be visually or textually distinct from FR-023 structural warnings.

---

## Summary of Changes Required

All changes target `/Users/business-daddy/code/payer-index-mono/conversus/specs/001-subject-arbitration/spec.md`.

| # | Dispute | Ruling | Change |
|---|---------|--------|--------|
| A | Prose conventions: MAY vs. SHOULD | MAY in Implementation Guidance | Add "Prose Convention Guidance" subsection to Implementation Guidance with MAY-level template-author guidance |
| B | Vacuous-output arbiter instruction | Accept FR-015 addition + SC-014 | Add instruction 8 to FR-015; add SC-014 to Success Criteria |
| C | SC-011 normative level | SHOULD-level quality advisory with warning | Add SC-011 to Success Criteria with quality-advisory labeling and Purist's scoping condition |

---

## Implementation Readiness Assessment

**The spec is fully unblocked.**

All 4 original blockers are resolved (3 unanimously, 1 at 2:1 with the residual now resolved above). All 3 micro-disputes now have binding decisions. The changes required are text additions to existing sections -- no new mechanisms, no new abstractions, no architectural changes.

**Remaining work before implementation**:

1. **Apply the 3 text changes above** to `spec.md`. These are additive -- no existing text needs to be removed or restructured.
2. **Apply the synthesis text changes** documented in the Phase 5 final synthesis (FR-011 amendment, FR-023 amendment, FR-015 instruction 7, template authoring contract invariant, deferred structured output section, SC-008 through SC-014).
3. **Update spec status** from "Draft" to "Ready for Implementation."

**No further deliberation cycles are needed.** The 4-phase process with 3 agents produced 16 convergence points and 3 narrow micro-disputes. This arbitration resolves the 3 micro-disputes. The spec's requirements, success criteria, constraints, and implementation guidance form a complete, internally consistent specification ready for template authoring and engine implementation.
