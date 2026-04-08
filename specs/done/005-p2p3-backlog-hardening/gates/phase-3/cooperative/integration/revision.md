# Phase 3 Gate Revision — Integration Checker

**Agent**: integration
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening
**Revision**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Add Phase 4 cross-reference to Dispute-Parsing heading-match note

- **Original position**: Append a T013 cross-reference to STATUS.md L93's heading-match gap note so implementors know the gap has a scheduled fix.
- **Disposition**: Surviving
- **Explanation**:
  Both cross-reviewers validated this recommendation. Compliance's cross-review (Safe Agreements, "Phase 4 cross-references needed in shared subsystem entries") confirmed that "integration provides the stronger evidence here" and that the cross-reference is "a small textual addition with high information value." Scope-boundary's cross-review (Safe Agreements, "Dispute-Parsing Subsystem heading-match gap is the most significant content issue") agreed explicitly, stating the two perspectives "converge: the gap is both procedurally significant (unmet obligation) and operationally dangerous (divergent implementations)" and that "integration's Recommendation 1 should be adopted."

  Compliance's Tensions section ("Scope of Phase 4 cross-references in STATUS.md") raised a legitimate concern that adding Phase 4 content to a Phase 3 deliverable could be a scope violation under the principle that "each phase produces a deliverable accurate as of its completion date" (Phase 2 final.md L116). However, compliance's own suggested resolution acknowledges that SC-003's "zero ambiguity about what is safe to build on" standard may require the cross-reference. The cross-reference does not import Phase 4 implementation content; it records that a known gap has a scheduled remediation, which is informational context about the current state of the subsystem. This is analogous to a "Depends On" field noting a future dependency — it describes the current document's incompleteness, not Phase 4's deliverable.

  P1 priority is maintained. The operational risk — implementors defining their own heading-match semantics in the absence of a visible remediation path — is the most consequential content gap in STATUS.md.

#### Recommendation 2: Add spec 002 Phase 4 re-evaluation note

- **Original position**: Add a note to spec 002's entry stating that Phase 4 T019 will modify the Round Termination Check and that the Spec-complete label should be re-evaluated afterward.
- **Disposition**: Modified
- **Explanation**:
  Compliance's cross-review (Tensions, "Scope of Phase 4 cross-references in STATUS.md") challenged whether Phase 4 forward references belong in STATUS.md at all, noting the Phase 2 synthesis principle about phase-scoped deliverables. Compliance suggested the cross-reference might belong in the Phase 3 gate summary rather than STATUS.md itself. Scope-boundary's cross-review did not challenge this recommendation directly but flagged the tension between "explicit caveat versus cross-phase purity" (Tensions, "Spec 002 effort 'None' versus Phase 4 T019 dependency"), noting that the convention choice of spec-scoped vs. impact-scoped effort fields determines whether the caveat applies.

  The original recommendation tried to do two things: (1) preserve the Phase 2 synthesis post-condition about re-evaluating the label, and (2) alert implementors to the upcoming modification. Compliance's challenge is strongest against (2) — STATUS.md should not become a forward-looking change log. But (1) is a different matter: the Phase 2 synthesis (final.md L214, P3 item 4) explicitly recorded the re-evaluation obligation, and STATUS.md is where labels live. If the re-evaluation trigger is not near the label it applies to, it is effectively invisible.

  **Modified recommendation**: Instead of the full note originally proposed, add a single parenthetical to spec 002's Notes field: "Notes: All 36 FRs represented in SKILL.md. Cross-round synthesis template exists. Runtime correctness of stagnation detection depends on spec 001's parsing subsystem. (Phase 4 post-condition: re-evaluate Spec-complete label after T019 modifies Round Termination Check cross-references.)" This is lighter than the original, explicitly labeled as a post-condition rather than current-state commentary, and keeps the trigger adjacent to the label it governs. Priority remains P1 because the obligation is inherited from Phase 2's binding commitments.

#### Recommendation 3: Rewrite spec 005 risk-of-gap as cost-of-absence statement

- **Original position**: Replace the tautological risk-of-gap statement with a consequence-oriented statement following the pattern of specs 001-004.
- **Disposition**: Modified
- **Explanation**:
  Compliance's cross-review (Dangerous Contradictions, "Spec 005 risk-of-gap: tautology vs. forward reference") agreed that the current text is outdated but challenged the replacement text I proposed, noting that my rewrite "describes the pre-spec-005 state, not the current state where Phase 3 has partially delivered." Compliance proposed scoping the rewrite to remaining unimplemented FRs rather than the full spec scope. Scope-boundary's cross-review (Tensions, "Spec 005 risk-of-gap: self-referential vs. outdated") acknowledged the interpretive ambiguity — is the field about "cost of never implementing" or "current remaining risk" — and concluded that "integration's proposed rewrite is better regardless, because it follows the pattern established by specs 001-004."

  Compliance's point about scoping to remaining work is well-taken. The risk-of-gap field should answer "what happens if this spec is never implemented" (the pre-spec state), but since spec 005 is partially implemented, the honest answer must distinguish what has already been delivered from what remains at risk.

  **Modified recommendation**: Replace STATUS.md L63 with: "SKILL.md Phase 6 edge cases (heading match semantics, missing document handling, overwrite behavior) remain undocumented, and the dispute-parsing subsystem's inline references in Round Termination Check and Trigger Evaluation have not been consolidated, increasing the risk of divergent parsing implementations across consumers." This scopes the risk to the remaining unimplemented FRs (FR-007, FR-011, FR-014, FR-015) rather than claiming STATUS.md "lacks complete cross-spec reference information" (which Phase 3 has already remediated). Priority remains P2.

#### Recommendation 4: Add comparative anchor to effort estimates

- **Original position**: Add a one-sentence scale definition to make the Small/Medium/Large labels meaningful to readers who were not part of the original estimation.
- **Disposition**: Modified
- **Explanation**:
  Compliance's cross-review (Dangerous Contradictions, "Effort field sufficiency standard") identified a genuine tension between my recommendation and compliance's own Recommendation 1 (P1). Compliance requires a four-dimension breakdown per FR-017's explicit text ("new files, logic complexity, testing surface, and relative effort"); I proposed a comparative anchor without the per-field breakdowns. Compliance's suggested resolution was to combine: add the four-dimension breakdown per FR-017 (P1) and include a comparative anchor as a secondary improvement (P2). Scope-boundary's cross-review (Tensions, "Effort estimate calibration") acknowledged that my reading of FR-017's "relative" clause is more thorough than their assessment but suggested the anchor sentence belong in the taxonomy or enrichment section, not in per-spec entries.

  Compliance is right that FR-017 textually requires four dimensions, and my recommendation addressed only one axis of the insufficiency. However, I maintain that mechanically expanding each effort field to four sub-lines would degrade STATUS.md's scan-ability without proportional benefit — this was the concern I raised in my cross-review of compliance (Dangerous Contradictions, "Effort field remediation scope"). The compromise I proposed there — a global scale definition plus a single parenthetical per spec addressing the most decision-relevant non-obvious dimension — remains the right balance.

  **Modified recommendation**: (a) Add a one-sentence preamble to the taxonomy or Phase 3 enrichment section: "Effort is relative: Small = targeted edits to existing files; Medium = new sections or modest new functionality; Large = multiple new components with cross-cutting integration." (b) Expand each effort field with a concise parenthetical covering the most decision-relevant FR-017 dimensions, not a mechanical four-line breakdown. For example, spec 004's field becomes: "Small (discovery only) -- 3 new CLI commands, no new parsing logic, testing: command output verification." This satisfies FR-017's coverage requirement while preserving scan-ability. Priority elevated to P1 to align with compliance's assessment that this is an FR-compliance issue, not merely a usability enhancement.

#### Recommendation 5: Specify which existing SKILL.md sections change for spec 003

- **Original position**: Add existing-section modification targets (Step 1, Step 4, Step 5) to the spec 003 SKILL.md Structure Plan entry.
- **Disposition**: Surviving
- **Explanation**:
  Compliance's cross-review (Tensions, "Granularity of SKILL.md Structure Plan for spec 003") noted the tension between structural presence and content completeness and stated the resolution should be consistent with how the effort field sufficiency question is resolved. Scope-boundary's cross-review did not challenge this recommendation and, under Tensions ("Spec 005 SKILL.md Structure Plan — completeness versus task fidelity"), discussed a related but distinct issue (whether spec 005 should be included in the structure plan).

  No cross-reviewer contested the substance. FR-019 (spec.md L250) explicitly requires identifying "which existing sections change and what new sections are needed." The current entry covers only the latter. The fix is straightforward: add the three existing-section targets. If the synthesis applies a structural-presence standard (the entry exists, detail deferred), this recommendation would be downgraded. But under FR-019's explicit two-clause requirement, the entry is incomplete without the existing-section analysis. I maintain P2 — this is important for advance planning but not blocking.

#### Recommendation 6: Add transition criteria as deferred Phase 3 obligation

- **Original position**: Add dual-condition transition criteria to the taxonomy section, framed as a P2 deferred obligation.
- **Disposition**: Modified
- **Explanation**:
  Both cross-reviewers challenged the P2 priority. Scope-boundary's cross-review (Dangerous Contradictions, "Transition criteria: binding commitment vs. deferred obligation") made the strongest case: "The Phase 2 synthesis language is unambiguous: 'The synthesis records this as a binding commitment, not an optional suggestion' (final.md L171). A binding commitment from a prior phase cannot be a P2 item in the phase that was obligated to implement it." Scope-boundary recommended I yield on priority. Compliance's cross-review (Dangerous Contradictions, "Phase 2 binding commitments: inherited obligation vs. informational context") raised the same concern, noting the classification determines whether Phase 3 can pass its checkpoint without transition criteria.

  I concede on priority. My original P2 framing treated this as a quality improvement rather than an inherited obligation. The Phase 2 synthesis (final.md L171) is unambiguous: it recorded the dual-condition formulation as a "binding commitment" for T008. T008 is a Phase 3 task. Calling this P2 effectively downgrades a prior-phase binding commitment, which undermines the inter-phase continuity the deliberation framework depends on. Scope-boundary's argument is decisive.

  **Modified recommendation**: Add transition criteria to the taxonomy section at P1 priority. The text is unchanged from my original: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." The change is solely the priority elevation from P2 to P1, reflecting the Phase 2 binding commitment.

#### Recommendation 7: Consolidate spec 004 discovery prerequisite timing

- **Original position**: Expand spec 003's "Depends On" field to include the timing constraint that spec 004 discovery features must be implemented before spec 003 Phase A.
- **Disposition**: Surviving
- **Explanation**:
  No cross-reviewer challenged this recommendation. Compliance's cross-review did not mention it. Scope-boundary's cross-review (Tensions, "'Depends On' field consistency") addressed a related but distinct issue (whether specs 001 and 004 need explicit "Depends On: None" fields) without contesting the spec 003 timing consolidation.

  The recommendation remains valid on its merits. The timing constraint is currently split across two entries (STATUS.md L46 and L55-56) and the dependency graph (L115). Consolidating it into spec 003's "Depends On" field is a low-cost improvement that makes the sequencing constraint visible in one place. P3 priority is appropriate — this is a usability enhancement, not a compliance issue.

#### Recommendation 8: Update spec 002 effort field to note Phase 4 T019 dependency

- **Original position**: Append a note to spec 002's effort field explaining that spec 005 Phase 4 (T019) will modify the Round Termination Check section.
- **Disposition**: Modified
- **Explanation**:
  Scope-boundary's cross-review (Tensions, "Spec 002 effort 'None' versus Phase 4 T019 dependency") framed this as a convention question: are effort fields spec-scoped (only the spec's own remaining work) or impact-scoped (including cross-spec modifications)? Scope-boundary noted that if effort is spec-scoped, "None" is correct and no caveat is needed. Compliance's cross-review did not address this recommendation.

  Scope-boundary's framing clarifies the issue. The effort field's purpose is to help maintainers prioritize spec-level work. Spec 002 has no remaining work from its own perspective — T019 is a spec 005 task that modifies a section spec 002 depends on. Adding T019 context to spec 002's effort field conflates two different questions: "how much work remains on spec 002" (none) and "will spec 002's implementation be affected by other specs" (yes). The latter belongs in the Notes field, not the Effort field.

  **Modified recommendation**: Instead of appending to the Effort field, the T019 cross-reference is already addressed by Recommendation 2 (modified above), which adds a Phase 4 post-condition parenthetical to spec 002's Notes field. This recommendation is therefore absorbed into Recommendation 2. If the synthesis adopts Recommendation 2's modified form, no separate action is needed for the effort field. If Recommendation 2 is rejected, fall back to a minimal Notes-field addition: "Note: spec 005 Phase 4 (T019) will modify the Round Termination Check section's parsing cross-references." Priority remains P3.

---

### New Recommendations

#### Add "Not assessed" acceptance label and update spec 003 (Priority: P1)

- **Triggered by**: Scope-boundary's cross-review (Dangerous Contradictions, "Spec 003 acceptance label: pre-existing gap vs. not flagged") identified that my review failed to flag spec 003's use of "Not started" in the Acceptance Tier (STATUS.md L45), which is an Implementation Tier label not defined in the Acceptance Tier taxonomy (L15-20). Scope-boundary noted: "integration's mandate as integration checker includes assessing whether 'STATUS.md content is accurate, internally consistent, actionable for a new implementor'... An internally inconsistent label-to-taxonomy relationship is exactly the kind of integration issue this review should surface." Compliance's cross-review (Tensions, "Treatment of Phase 2 residuals") made the same observation.
- **Proposed change**: (a) Add to the Acceptance Tier taxonomy (STATUS.md, after L20): `- **Not assessed**: No acceptance criteria have been evaluated.` (b) Update STATUS.md L45 from `**Acceptance**: Not started` to `**Acceptance**: Not assessed`. This implements Phase 2 final synthesis P1 items 1 and 2 (final.md L186-188), which were unanimously agreed but not carried into Phase 3's implementation.
- **Rationale**: This is a genuine oversight in my original review. I validated the taxonomy section as "cleanly separated" (Alignment, item 1) without checking whether every label in active use is defined in that taxonomy. The cross-tier label reuse violates FR-009 (spec.md L216), which requires status labels to use the two-tier convention. Scope-boundary is correct that this is an internal consistency issue squarely within my mandate as integration checker. The fix is small, the Phase 2 synthesis unanimously agreed on it, and leaving it unaddressed would mean an implementor encounters an undefined label with no way to determine whether it is intentional or erroneous.

#### Add compound-label permission rule to Implementation Tier taxonomy (Priority: P2)

- **Triggered by**: Scope-boundary's cross-review (Dangerous Contradictions, "Compound-label permission rule: absent from integration's analysis") identified that STATUS.md L52 uses a compound label format ("Implementation-complete (core) / Not started (discovery)") without the taxonomy defining compound-label conventions. Phase 2 final synthesis P1 item 4 (final.md L192) recommended adding a compound-label rule.
- **Proposed change**: Add to the Implementation Tier section (after L13): "Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label."
- **Rationale**: Like the "Not assessed" label, this was a Phase 2 recommendation that was not carried into implementation. My original review referenced the spec 004 entry in multiple places (Recommendation 7 on discovery timing, Recommendation 8 on effort) without noticing that the label format itself lacks taxonomic backing. Scope-boundary is correct that this should have been flagged. The Phase 2 synthesis's recommended resolution (final.md L165) adopted compound labels with the constraining rule by a bilateral agreement with scope-boundary's flexibility conditions met. Without the rule, the taxonomy implicitly permits a format it does not define, creating precedent for ad-hoc label extensions. P2 rather than P1 because the compound label already exists and is interpretable — the risk is future inconsistency, not current unreadability.

---

### Position Summary

Of my original 8 recommendations, I maintained 2 (Recommendations 1 and 5), modified 5 (Recommendations 2, 3, 4, 6, and 8), and maintained 1 (Recommendation 7) at its original priority. No recommendations were withdrawn. I added 2 new recommendations surfaced by the cross-review process: the "Not assessed" acceptance label (P1) and the compound-label permission rule (P2).

The most significant change in my thinking was the priority elevation of Recommendation 6 (transition criteria) from P2 to P1. Scope-boundary's cross-review made an argument I cannot rebut: the Phase 2 synthesis recorded the dual-condition formulation as a "binding commitment, not an optional suggestion" (final.md L171), and T008 — the Phase 3 task that was supposed to implement it — is marked complete without including it. My original P2 framing effectively treated a binding inter-phase obligation as a discretionary improvement, which would set a precedent for deprioritizing any binding commitment from a prior phase. Scope-boundary correctly identified that this undermines the deliberation framework's continuity guarantees. I concede this was a calibration error rather than a principled disagreement.

My remaining highest-priority recommendation is Recommendation 1: adding the T013 cross-reference to the Dispute-Parsing heading-match note (P1). Both cross-reviewers validated this as the most significant content gap in STATUS.md. The argument is simple: STATUS.md L93 identifies a known limitation (heading-match semantics are not explicitly specified) without indicating whether it will be fixed, when, or by whom. An implementor building on the dispute-parsing subsystem encounters this note and has no basis for deciding whether to wait for the fix or work around it. The cross-reference costs one clause ("Phase 4 task T013 (FR-007) will add explicit matching rules") and converts an open-ended deficiency into a scheduled remediation. This is the single change most likely to prevent divergent implementations — the exact failure mode SC-004 exists to prevent. It should survive into the final synthesis because no cross-reviewer contested its value, and it is the highest-leverage content fix relative to its size.
