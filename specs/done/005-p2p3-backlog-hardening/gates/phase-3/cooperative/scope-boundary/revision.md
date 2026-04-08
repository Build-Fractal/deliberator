# Phase 3 Revision — scope-boundary

**Agent**: scope-boundary
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening
**Revision iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Add transition criteria to STATUS.md

- **Original position**: Add dual-condition transition criteria after the "Interpreting the Two Tiers" paragraph at P1 priority, as a Phase 2 binding commitment that Phase 3 was obligated to implement via T008.
- **Disposition**: Modified
- **Explanation**:

  Both cross-reviews challenged the P1 priority but not the substance. compliance's cross-review (Dangerous Contradictions, first item) acknowledged that my reading of the Phase 2 synthesis is "more faithful" and offered to yield upward to P1, citing the "binding commitment" language as stronger than the P2 priority label. integration's cross-review (Dangerous Contradictions, first item) assigned P2 and framed it as a "deferred Phase 3 obligation" rather than a blocking omission, but suggested both items (transition criteria and the Dispute-Parsing cross-reference) should be P1 with different justifications.

  The modification concerns taxonomy-section placement. My original recommendation placed transition criteria "after L24 (after 'Interpreting the Two Tiers' paragraph), a new subsection or paragraph." In my own cross-review of compliance (Dangerous Contradictions, third item — "Transition criteria: where to place them"), I acknowledged that adding content to the taxonomy section is exactly the kind of taxonomy modification my mandate requires me to flag. I resolved this by accepting that the Phase 2 synthesis explicitly mandated it as a T008 input, which overrides my general principle that Phase 3 should not touch the taxonomy. I maintain that resolution.

  However, integration's cross-review (Tensions, first item — "Depth of Phase 2 accountability versus Phase 3 forward focus") correctly identifies that four of my eight recommendations address Phase 2 gaps, which could dominate the remediation effort at the expense of Phase 3 content quality. The modified recommendation preserves P1 priority for transition criteria but acknowledges that the synthesis should present this alongside integration's P1 items (Dispute-Parsing cross-reference) as co-equal priorities rather than allowing Phase 2 accountability to crowd out Phase 3 quality work.

  **Modified recommendation**: Add transition criteria to STATUS.md at P1 priority. Place after the "Interpreting the Two Tiers" paragraph (L24). Text: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." Frame this as a Phase 2 binding commitment executed in Phase 3, categorized separately from Phase 3's own content improvements in the final synthesis priority stack.

#### Recommendation 2: Resolve spec 003 acceptance label

- **Original position**: Fix the spec 003 "Not started" acceptance label to "Not assessed" at P1 priority, recommending Phase 3 make the change since Phase 2's synthesis unanimously agreed on it.
- **Disposition**: Modified
- **Explanation**:

  compliance's cross-review (Dangerous Contradictions, third item — "Phase 2 residuals — flag-only vs. fix-now") correctly identified the ownership tension: my review simultaneously characterizes this as a "Phase 2 deliverable" and recommends Phase 3 fix it. compliance's suggested resolution is pragmatic: "fix them in Phase 3, attribute the obligation to Phase 2, and note the Phase 2 implementation gap for process improvement." integration's cross-review (Dangerous Contradictions, second item — "Spec 003 acceptance label") noted that integration's own review did not flag this at all, treating the taxonomy as Phase 2's deliverable, and suggested the practical path is to "fix it now" but "frame it explicitly as a Phase 2 remediation being executed during Phase 3."

  In my own cross-review of compliance (Dangerous Contradictions, first item), I noted the logical problem in my position: if both recommendations are implemented, "Phase 3 simultaneously claims it should modify the taxonomy (compliance) and that any taxonomy modification is a scope boundary violation (scope-boundary)." My suggested resolution there was to "document these as Phase 2 incomplete items that constitute preconditions for the Phase 3 checkpoint claim." I also acknowledged in my cross-review of compliance (Tensions, first item — "Phase 2 synthesis authority: binding vs. advisory") that I selectively treat the Phase 2 synthesis as binding for transition criteria but not for taxonomy changes, and that compliance correctly identified this selectivity as a logical problem.

  The modification resolves the inconsistency. If the Phase 2 synthesis is binding (which I argued for transition criteria), then all its P1 items carry forward, including the "Not assessed" label. I cannot logically hold both that the synthesis is binding for transition criteria and advisory for the "Not assessed" label.

  **Modified recommendation**: Fix the spec 003 acceptance label at P1 priority. Add "Not assessed" to the Acceptance Tier taxonomy at L20 and update L45 from "Not started" to "Not assessed." Frame explicitly as Phase 2 remediation executed during Phase 3 — the obligation belongs to Phase 2, but the fix happens now because STATUS.md cannot pass SC-003 ("zero ambiguity") with an undefined label. This is consistent with the principle that Phase 2 binding commitments carry forward regardless of whether they touch taxonomy.

#### Recommendation 3: Add "Depends On" field to spec 001 entry

- **Original position**: Add `**Depends On**: (none -- foundational)` to spec 001's entry for consistency with the dependency graph.
- **Disposition**: Surviving
- **Explanation**:

  compliance's cross-review (Safe Agreements, second item — "'Depends On' field should be present for spec 001") confirmed this as a shared position at P2, noting the combined evidence from both reviews strengthens the case. integration's cross-review (Tensions, third item — "'Depends On' field consistency") raised the tension between structural completeness and information value, noting that adding "(none -- foundational)" to spec 001 "adds no new information; it just makes the entry structurally parallel with the others."

  integration's observation is factually correct but does not change my position. The issue is not information density but interpretive ambiguity. STATUS.md L129 declares "per-spec entries are authoritative." If the authoritative entry for spec 001 omits the "Depends On" field entirely, a reader cannot distinguish between "assessed as having no dependencies" and "dependency assessment omitted." The dependency graph at L111 answers the question, but the authoritative-source note directs readers to the per-spec entries, not the graph. Adding the field at P2 is a low-cost fix that eliminates this ambiguity. compliance's observation that "a reader cannot determine whether the dependency was assessed or simply omitted" captures the issue precisely.

#### Recommendation 4: Add "Depends On" field to spec 004 entry

- **Original position**: Add `**Depends On**: (none -- self-contained engine)` to spec 004's entry.
- **Disposition**: Surviving
- **Explanation**:

  No cross-review directly challenged this recommendation. compliance's cross-review (Safe Agreements, second item) noted that "covering spec 004 as well" strengthens the consistency case. integration's cross-review (Tensions, third item) grouped this with Recommendation 3 as a structural-completeness question. The same reasoning from Recommendation 3 applies: the fix is low-cost, eliminates ambiguity about whether the dependency was assessed, and maintains the authoritative-source principle from L129. P2 priority is appropriate.

#### Recommendation 5: Verify compound-label rule was implemented

- **Original position**: Verify whether the compound-label permission rule from Phase 2's synthesis (final.md L192) was intentionally deferred or accidentally omitted, and if omitted, add it.
- **Disposition**: Modified
- **Explanation**:

  compliance's cross-review (Dangerous Contradictions, third item) framed this as P1 because "Phase 2 synthesis P1-4 (final.md L192) recommended this as a P1 change." In my own cross-review of compliance (Dangerous Contradictions, first item), I acknowledged that my mandate to flag taxonomy changes creates a contradiction: I flag taxonomy modifications as Phase 2 scope violations, yet the compound-label rule is a taxonomy modification that Phase 2's synthesis explicitly recommended. In my cross-review of integration (Dangerous Contradictions, third item), I noted that integration's review did not mention the compound-label rule at all and recommended they add it as a finding.

  The modification follows the same logic as Recommendation 2. If the Phase 2 synthesis is binding (which I now accept consistently), then the compound-label permission rule — recorded as P1 item 4 in the Actionable Spec Changes (final.md L192) — carries forward as an obligation. My original "verify" framing was hedging. The Phase 2 synthesis is explicit: the rule should be added.

  **Modified recommendation**: Add the compound-label permission rule to the Implementation Tier section at P1 priority. Text per Phase 2 synthesis (final.md L192): "Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label." Frame as Phase 2 remediation executed during Phase 3, same as Recommendations 1 and 2.

#### Recommendation 6: Broaden maintenance note scope

- **Original position**: Amend the maintenance note at L138 to cover subsystem stability changes, consumer changes, and structure plan updates, at P3 priority.
- **Disposition**: Modified
- **Explanation**:

  compliance's cross-review (Tensions, first item — "Scope of maintenance note — narrow vs. broad") identified that compliance and I address different aspects of the same maintenance note: compliance wants to fix the FR-008a sub-identifier traceability, while I want to broaden the trigger scope. compliance recommended the synthesis combine both changes.

  integration's cross-review (Dangerous Contradictions, third item — "Maintenance note scope") acknowledged my observation as correct ("the maintenance note's scope does not cover Phase 3's additions") while also noting integration's assessment is technically accurate ("the note does implement FR-008a as written"). integration's suggested resolution: broaden the note at P3, since "FR-008a's language is narrower than the document's needs, and the maintenance note should exceed the minimum FR requirement."

  The modification incorporates compliance's FR reference fix. Both changes should be made in a single edit to avoid two-pass modification of the same line.

  **Modified recommendation**: Amend the maintenance note at L138 in a single edit: (1) change "(FR-008a)" to "(FR-008)" for traceability to the spec's FR list, and (2) broaden the trigger: "This document MUST be updated when any spec's implementation or acceptance status changes, when shared subsystem stability or consumers change, or when the SKILL.md Structure Plan is affected by implementation progress (FR-008)." Priority: P3. Credit: compliance's FR reference normalization (compliance review, Recommendation 7) combined with my scope broadening.

#### Recommendation 7: Add spec 005 to SKILL.md Structure Plan

- **Original position**: Add a spec 005 entry to the SKILL.md Structure Plan section, since spec 005 has more pending SKILL.md work than any other spec.
- **Disposition**: Surviving
- **Explanation**:

  compliance's cross-review (Tensions, second item — "Spec 005 in SKILL.md Structure Plan — missing vs. out-of-scope") correctly noted the tension between FR-019 ("future spec implementations") and T012's narrower scope ("specs 002, 003, 004"). compliance reads T012 literally; I read FR-019 broadly. compliance's recommended resolution is sound: "note that T012 is task-compliant but FR-019-incomplete" and "recommend the spec 005 entry as a low-cost addition (scope-boundary's Rec 7, P3) that closes the gap between task and FR without reopening T012's scope."

  integration's cross-review (Tensions, second item) similarly noted the tension and suggested the synthesis decide whether T012's scope is deliberate or an oversight. integration's framing — "the resolution depends on whether the structure plan is meant to be exhaustive (all pending SKILL.md work) or scoped (only specs whose SKILL.md integration requires advance planning)" — is useful, but spec 005's pending SKILL.md work (FR-007, FR-011, FR-014, FR-015) is the largest remaining SKILL.md workload, making it the strongest candidate for advance structural planning.

  No cross-review argued against adding the entry; the tension is about whether it is required or merely useful. At P3, this is a low-cost improvement that closes the task-vs-FR gap. I maintain the recommendation.

#### Recommendation 8: Add "Not assessed" acceptance label to taxonomy

- **Original position**: Add "Not assessed" to the Acceptance Tier taxonomy as a prerequisite for Phase 3's checkpoint claim.
- **Disposition**: Modified (merged with Recommendation 2)
- **Explanation**:

  This recommendation and Recommendation 2 address two sides of the same fix: Recommendation 8 proposes adding the label to the taxonomy; Recommendation 2 proposes applying it to spec 003. compliance's cross-review (Safe Agreements, first item) confirmed both reviews assign P1 and cited three independent grounds (FR-009 violation, Phase 2 binding convergence, SC-005 failure). No cross-review challenged the substance.

  The modification merges this with Recommendation 2 into a single action item. Maintaining them as separate recommendations in my original review was analytically useful (taxonomy definition vs. label application) but operationally redundant — the implementor must do both in a single pass. The merged recommendation (stated under Recommendation 2 above) covers both: add the definition and apply the label.

  **Modified recommendation**: Merged into Recommendation 2. The single action is: add "Not assessed" to the Acceptance Tier taxonomy definition and update spec 003's acceptance label from "Not started" to "Not assessed." P1 priority. Phase 2 remediation executed during Phase 3.

### New Recommendations

#### Acknowledge FR-017 effort field incompleteness (Priority: P2)

- **Triggered by**: compliance's cross-review of my review (Dangerous Contradictions, second item — "FR-017 effort field completeness"). compliance noted that my review "does not flag the absence of the four-dimension breakdown (new files, logic complexity, testing surface, relative effort) as a compliance gap" and that the "Effort fields are not mentioned in scope-boundary's Alignment section either." compliance's suggested resolution: "scope-boundary should acknowledge that the current Effort fields are incomplete against the FR's literal requirements."
- **Proposed change**: The current Effort fields in STATUS.md satisfy T011's task description (tasks.md L66) but not FR-017's full specification (spec.md L242), which requires estimates "covering: new files, logic complexity, testing surface, and relative effort." The colon-and-list construction in FR-017 is enumerative. The current fields provide relative effort labels and summary sentences but omit the four-dimension breakdown. This is the same T011-paraphrased-FR-017 gap that compliance identified (compliance review, Off-Base Assumptions, first bullet). I recommend adopting compliance's position that the Effort fields should be enriched to cover all four dimensions specified in FR-017, at P2 priority.
- **Rationale**: My original review did not evaluate FR-017 compliance at the dimension level because effort field content depth is not a scope-boundary concern. compliance's analysis is well-grounded in the spec text. My silence in the original review should not be interpreted as endorsement of the current Effort fields' completeness against FR-017. This is a compliance finding that my scope-boundary lens naturally missed, and the cross-review process correctly surfaced it.

### Position Summary

Of eight original recommendations, I withdrew zero, modified four (Recommendations 1, 2, 5, and 6 substantively; Recommendation 8 merged into Recommendation 2), and maintained three (Recommendations 3, 4, and 7). One new recommendation emerged from the cross-review process.

The most significant change in my thinking concerns the selective application of Phase 2 binding authority. In my original review, I treated the Phase 2 synthesis as binding for transition criteria (which I wanted in Phase 3) but not binding for taxonomy changes like the "Not assessed" label and compound-label rule (which I wanted to keep out of Phase 3 as scope violations). compliance's cross-review and my own cross-review of compliance both identified this selectivity as a logical inconsistency. I now accept a consistent principle: all binding commitments from the Phase 2 synthesis carry forward as Phase 3 obligations, regardless of whether they touch the taxonomy section. The practical consequence is that Recommendations 1, 2, 5, and 8 are all framed as Phase 2 remediation executed during Phase 3, with the obligation attributed to Phase 2 and the execution happening now. This resolves the contradiction between my scope-boundary mandate (flag taxonomy modifications) and the procedural reality (Phase 2's synthesis explicitly mandated these modifications).

My remaining highest-priority recommendation is the transition criteria addition (Recommendation 1, P1). This should survive into the final synthesis because it is the only Phase 2 binding commitment where the substance was unanimously agreed (the dual-condition formulation from Phase 2 Convergence point 6), the placement was resolved (Phase 3 via T008), and the implementation is a single sentence. It is the gap with the highest ratio of impact to effort: without it, the boundary between "Feature-complete" and "Spec-complete" remains implicit, meaning every future label transition is a judgment call rather than a verifiable condition. The compliance and integration cross-reviews both confirmed the gap exists; the only disagreement was priority level, and compliance explicitly yielded to P1.

---

### Referenced Documentation

- `conversus/specs/STATUS.md` -- L3-24, L30-35, L45, L52, L58-64, L66-84, L86-104, L106-129, L138
- `conversus/specs/005-p2p3-backlog-hardening/spec.md` -- L215-216 (FR-008, FR-009), L225 (FR-012), L242 (FR-017), L250 (FR-019), L265 (SC-003)
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` -- L44-45, L63-68, L86-90
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-2/summary/final.md` -- L152-156, L171, L186-192, L202
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-3/cooperative/compliance/cross-reviews/scope-boundary.md` -- Dangerous Contradictions (items 1-3), Tensions (items 1-4), Safe Agreements (items 1-3)
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-3/cooperative/integration/cross-reviews/scope-boundary.md` -- Dangerous Contradictions (items 1-3), Tensions (items 1-4), Safe Agreements (items 1-4)
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-3/cooperative/scope-boundary/cross-reviews/compliance.md` -- Dangerous Contradictions (items 1-3), Tensions (items 1-5)
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-3/cooperative/scope-boundary/cross-reviews/integration.md` -- Dangerous Contradictions (items 1-3), Tensions (items 1-4)
