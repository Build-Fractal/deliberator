# Phase 3 Final Disputes — Integration Checker

**Agent**: integration
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening
**Phase**: 4 (Final Disputes and Convergence)

---

### Remaining Disputes

#### Dispute 1: Effort Field Format — Compact Inline Four-Dimension vs. Selective Parenthetical

- **My claim**: Effort fields should use a comparative anchor (global scale definition) plus a selective parenthetical per spec addressing the most decision-relevant FR-017 dimension, not a mechanical four-dimension inline breakdown for every spec. (Revision, Recommendation 4, Modified.)
- **Opposing position(s)**: Compliance requires each spec's Effort field to address all four FR-017 dimensions (new files, logic complexity, testing surface, relative effort) in a compact inline format. Compliance's modified recommendation (Revision, Recommendation 1) proposes a full four-dimension inline per spec: e.g., "Small -- New files: none; logic complexity: low (template-level instructions); testing surface: behavioral verification of template output." Scope-boundary's new recommendation (Revision, "Acknowledge FR-017 effort field incompleteness") endorses compliance's position that the current fields are incomplete against FR-017's literal text and assigns P2 for enrichment, but defers to compliance on format specifics.
- **Why I will not concede**: The four-dimension inline format creates five instances of formulaic sub-field enumeration (one per spec) that add volume without proportional decision-making value. STATUS.md serves as a quick-reference document (SC-003: "reading a single document"). The effort fields' primary function is prioritization (spec.md L145: "priority considers effort alongside value"). For prioritization, relative calibration between specs matters more than absolute dimensional breakdowns within each spec. A reader deciding between spec 001 (Small) and spec 003 (Large) gains that signal from the label; the dimensional breakdown tells them *why* it is Small or Large, which is useful but secondary. My modified recommendation (Revision, Recommendation 4) addresses FR-017 compliance by including dimensional coverage in a selective parenthetical, while the global scale definition makes all labels interpretable without per-spec repetition.
- **Counter-argument to their position**: Compliance reads FR-017's "covering: new files, logic complexity, testing surface, and relative effort" as requiring all four dimensions per spec entry. This reading treats STATUS.md effort fields as the sole implementation site for FR-017. But FR-017 (spec.md L242) says each spec "MUST include an order-of-magnitude effort estimate covering" those dimensions. The "covering" clause specifies what the estimate must *address*, not that each dimension must appear as a labeled sub-field. My approach covers all four dimensions: the scale definition addresses new files and logic complexity at the tier level (Small = "targeted edits to existing files" implies no new files and low logic complexity), and per-spec parentheticals address the non-obvious dimensions (testing surface, or specific file counts where the label alone is ambiguous). Compliance's format satisfies FR-017 more literally but at the cost of five formulaic entries that compress poorly and degrade scan-ability -- the very quality that makes STATUS.md useful for prioritization in the first place.
- **Proposed resolution path**: The synthesizer should adopt a hybrid: (a) the global scale definition (agreed by all agents), and (b) a per-spec enrichment that covers all four FR-017 dimensions but permits abbreviation when a dimension is inferable from the scale tier. For example, spec 002's effort field should not mechanically list "New files: none; logic complexity: none; testing surface: none" when "None -- complete" already communicates this. The test should be: could a reader unfamiliar with the project determine the rough scope of each dimension from the effort field plus the scale definition? If yes, FR-017 is satisfied regardless of whether each dimension has its own labeled sub-field.

#### Dispute 2: Compound-Label Permission Rule Priority — P1 vs. P2

- **My claim**: The compound-label permission rule should be added at P2 priority. The compound label already exists in STATUS.md L52 and is interpretable; the risk is future inconsistency, not current unreadability. (Revision, New Recommendations, "Add compound-label permission rule," P2.)
- **Opposing position(s)**: Scope-boundary's modified recommendation (Revision, Recommendation 5) assigns P1 priority, arguing that all Phase 2 binding commitments carry forward at their original priority. Compliance's modified recommendation (Revision, Recommendation 3) also assigns P1, framing it as a Phase 2 remediation prerequisite for Phase 3 checkpoint passage.
- **Why I will not concede**: I accept the principle that Phase 2 binding commitments carry forward. But the compound-label rule in the Phase 2 synthesis (final.md L192) was recorded under "Actionable Spec Changes" as P1 item 4, alongside items 1-3 that address undefined labels and missing definitions. Items 1-3 fix states where the document is *broken* -- a label in use has no definition, creating interpretive ambiguity. Item 4 fixes a state where the document is *incomplete* -- a format in use has no formal rule, but the format is self-documenting (the parenthetical structure of "Implementation-complete (core) / Not started (discovery)" is readable without a rule). The two categories have different urgency profiles. Elevating all four to the same priority conflates "this blocks interpretation" with "this lacks a formal definition for a readable format."
- **Counter-argument to their position**: Scope-boundary and compliance both derive P1 from the Phase 2 synthesis's priority label. But the Phase 2 synthesis grouped items 1-4 under a single P1 heading for administrative convenience -- all four were "Actionable Spec Changes (Priority: P1)." This grouping does not mean each item has identical urgency. The synthesis resolved *what* to do and recorded it at P1 as a block. The question of *relative urgency within the block* is a Phase 3 implementation concern, not a Phase 2 binding commitment. No reader of STATUS.md is currently blocked or confused by the absence of a compound-label rule; every reader who encounters spec 003's "Not started" acceptance label encounters an undefined term. These are not equivalent problems.
- **Proposed resolution path**: The synthesizer should adopt P1 for the "Not assessed" label and transition criteria (items where interpretation is blocked without the fix) and P2 for the compound-label rule (where the fix prevents future inconsistency but does not resolve a current ambiguity). If the synthesizer prefers uniform P1 for all Phase 2 binding commitments as a governance principle, I will accept that -- but the implementation order within P1 should still reflect the urgency distinction: undefined labels first, format rules second.

#### Dispute 3: Maintenance Note FR-008a Reference — Normalize to FR-008 vs. Retain FR-008a

- **My claim**: The "FR-008a" identifier in STATUS.md L138 should be retained because it traces to tasks.md T008 (L63), T017 (L101), and serves as the established convention for the maintenance sub-requirement. Normalizing to "FR-008" would break traceability between tasks.md and STATUS.md. (Revision, Recommendation disposition on compliance's Recommendation 7, which compliance withdrew.)
- **Opposing position(s)**: Scope-boundary's modified Recommendation 6 (Revision) proposes changing "(FR-008a)" to "(FR-008)" as part of a combined edit that also broadens the maintenance note's trigger scope, crediting compliance's original Recommendation 7. Compliance withdrew the normalization recommendation in their revision (Recommendation 7, Withdrawn), explicitly accepting that "FR-008a" should be retained. However, scope-boundary's revision was written after reading compliance's original review but the merged edit still includes the normalization.
- **Why I will not concede**: Compliance -- the agent who originally proposed the normalization -- withdrew it after reading my cross-review evidence that "FR-008a" traces to tasks.md. Scope-boundary's revision incorporates compliance's original recommendation without accounting for compliance's withdrawal. The identifier "FR-008a" appears three times in tasks.md (T004 L27, T008 L63, T017 L101) as a distinct sub-requirement identifier. Changing it to "FR-008" in STATUS.md severs the traceability chain that the identifier was created to maintain. FR-008 is the umbrella requirement (spec.md L215); FR-008a is the maintenance obligation sub-requirement extracted in task decomposition. The distinction is meaningful.
- **Counter-argument to their position**: Scope-boundary's argument for normalization is that "FR-008a" is "not in the spec's FR list" (inheriting compliance's original reasoning). This is true at the spec.md level but false at the tasks.md level. The task decomposition created "FR-008a" as a traceable sub-identifier precisely because FR-008 covers multiple obligations (create STATUS.md, maintain it, include subsystems, include dependencies) and the maintenance note implements only one of them. Removing the sub-identifier forces the reader to determine which part of FR-008 the maintenance note addresses. The correct resolution -- which compliance already accepted -- is to keep "FR-008a" and optionally add a brief traceability note ("FR-008a refers to the maintenance sub-requirement within FR-008").
- **Proposed resolution path**: The synthesizer should adopt scope-boundary's trigger-broadening edit but retain "(FR-008a)" rather than normalizing to "(FR-008)", consistent with compliance's concession. If scope-boundary's revision text was written before incorporating compliance's withdrawal, this is a sequencing artifact, not a substantive disagreement. The combined edit becomes: broaden the trigger scope (scope-boundary's contribution) + keep FR-008a (compliance's concession, integration's original position).

---

### Convergence

#### Converged: Transition Criteria at P1

- **Shared position**: Add dual-condition transition criteria to STATUS.md after the "Interpreting the Two Tiers" paragraph (L24): "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." Priority: P1. Attribute to Phase 2 binding commitment (final.md L171, L202).
- **Agreeing agents**: All three -- integration (Revision, Recommendation 6), compliance (Revision, Recommendation 4), scope-boundary (Revision, Recommendation 1).
- **Strength**: Unanimous
- **Path to convergence**: In Phase 2, the dual-condition formulation was unanimously agreed. In Phase 3 initial reviews, compliance assigned P2, integration assigned P2, and scope-boundary assigned P1. Cross-review surfaced the "binding commitment" language from final.md L171. Both compliance and integration conceded upward to P1 in their revisions. The formulation text was agreed from Phase 2; only the priority required deliberation.

#### Converged: "Not Assessed" Label for Spec 003

- **Shared position**: Add "Not assessed" to the Acceptance Tier taxonomy (after L20) and update spec 003's acceptance label from "Not started" to "Not assessed." Frame as Phase 2 remediation executed during Phase 3. Priority: P1.
- **Agreeing agents**: All three -- integration (Revision, New Recommendations, "Add 'Not assessed' acceptance label"), compliance (Revision, Recommendation 2), scope-boundary (Revision, Recommendation 2).
- **Strength**: Unanimous
- **Path to convergence**: Compliance flagged this in the initial review. Scope-boundary flagged it independently. Integration missed it in the initial review but accepted it as a genuine oversight after cross-review. All three agents converged during the revision phase on both the fix and the Phase 2 attribution framing.

#### Converged: Dispute-Parsing T013 Cross-Reference at P1

- **Shared position**: Append a T013 cross-reference to STATUS.md L93's heading-match gap note, converting it from an open-ended deficiency to a scheduled remediation. Proposed text addition: "Phase 4 task T013 (FR-007) will add explicit matching rules." Priority: P1.
- **Agreeing agents**: All three -- integration (Revision, Recommendation 1), compliance (cross-review Safe Agreements: "Phase 4 cross-references needed"), scope-boundary (cross-review Safe Agreements: "Dispute-Parsing heading-match gap is the most significant content issue").
- **Strength**: Unanimous
- **Path to convergence**: Integration identified this in the initial review. Both cross-reviewers validated it without challenge. No revision was needed -- the recommendation survived intact from Phase 2 through Phase 4.

#### Converged: Spec 005 Risk-of-Gap Rewrite

- **Shared position**: Replace STATUS.md L63's risk-of-gap statement with a consequence-oriented statement scoped to remaining unimplemented FRs (FR-007, FR-011, FR-014, FR-015), not the full spec scope. The current text is factually stale (it describes the pre-Phase-3 state). Priority: P2.
- **Agreeing agents**: All three -- integration (Revision, Recommendation 3), compliance (Revision, New Recommendations, "Rewrite spec 005 risk-of-gap"), scope-boundary (cross-review Tensions, acknowledging the rewrite is "better regardless").
- **Strength**: Unanimous
- **Path to convergence**: Integration flagged the tautology in the initial review. Compliance's cross-review confirmed the finding but challenged the replacement text's scope. Integration and compliance independently proposed scoping the rewrite to remaining SKILL.md-targeted FRs. Scope-boundary endorsed the direction. The final text converged during revision: all agents agree on scoping to remaining work and following the consequence-oriented pattern of specs 001-004.

#### Converged: "Depends On" Fields for Specs 001 and 004

- **Shared position**: Add `**Depends On**: None (foundational)` to spec 001 and `**Depends On**: None (self-contained engine)` to spec 004 for consistency with the dependency graph and the authoritative-source principle at L129. Priority: P2.
- **Agreeing agents**: Compliance (Revision, Recommendation 5), scope-boundary (Revision, Recommendations 3 and 4). Integration did not challenge or endorse explicitly but raised no objection.
- **Strength**: Bilateral (compliance and scope-boundary), with integration non-opposing.
- **Path to convergence**: Scope-boundary flagged both specs in the initial review. Compliance independently flagged spec 001 and adopted scope-boundary's observation about spec 004 during revision. Integration noted the fix adds no new information but did not contest the interpretive-ambiguity argument.

---

### Final Position Statement

**Non-Negotiables** (3 items):

1. **The T013 cross-reference must be added to the Dispute-Parsing heading-match note (STATUS.md L93).** This is the single highest-leverage content fix in STATUS.md. Without it, implementors encounter a known gap with no visibility into whether it will be fixed, when, or by whom -- the exact failure mode SC-004 exists to prevent. (Revision, Recommendation 1; unanimously supported by all agents.)

2. **Transition criteria must be added at P1 as a Phase 2 binding commitment.** The boundary between "Feature-complete" and "Spec-complete" is currently implicit. Without the dual-condition formulation, every future label transition is a judgment call rather than a verifiable condition. The Phase 2 synthesis (final.md L171) recorded this as binding, and all three agents now agree. (Revision, Recommendation 6; unanimously converged.)

3. **The "FR-008a" identifier must be retained in the maintenance note.** Compliance, who originally proposed the normalization, withdrew the recommendation after reviewing the traceability evidence. Normalizing to "FR-008" would break the tasks.md traceability chain. If the maintenance note's trigger scope is broadened (which I support), the broadening should use the existing identifier. (Revision, Recommendation 7 context; compliance withdrawal confirmed.)

**Flexibility** (3 items):

1. **Effort field four-dimension coverage.** I accept that FR-017 requires coverage of all four dimensions. I am flexible on format -- if compliance's compact inline approach can be adapted to permit abbreviation where dimensions are inferable from the scale tier (e.g., not mechanically listing "New files: none" for spec 002), I will accept it. What must be preserved: the global scale definition and the principle that scan-ability is not sacrificed for formulaic completeness.

2. **Compound-label rule priority.** I prefer P2 on urgency grounds but will accept P1 if the synthesizer adopts the governance principle that all Phase 2 binding commitments inherit their original priority block. What must be preserved: the implementation ordering within P1 should still fix undefined labels (the "Not assessed" label) before adding format rules (compound-label permission).

3. **Spec 005 entry in SKILL.md Structure Plan.** I did not flag this in my initial review and scope-boundary's case is reasonable (spec 005 has the largest remaining SKILL.md workload). I am flexible on inclusion at P3. What must be preserved: if included, the entry should note that spec 005's SKILL.md changes are documentation edits to existing sections, not new structural additions, to avoid implying a larger scope than exists.
