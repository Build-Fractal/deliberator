# Phase 3 Cooperative Deliberation — Neutral Synthesis

**Synthesizer**: neutral
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening
**Target**: `deliberator/specs/STATUS.md`

---

### Process Summary

- **Agents**: 3 — compliance, integration, scope-boundary
- **Total artifacts**: 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes)
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 25 (compliance: 9, integration: 8, scope-boundary: 8)
- **Recommendations withdrawn** (Phase 3): 1 (compliance Rec 7: FR-008a normalization)
- **Recommendations modified** (Phase 3): 14 (compliance: 6 — Recs 1, 2, 3, 4, 6, 9; integration: 5 — Recs 2, 3, 4, 6, 8; scope-boundary: 4 — Recs 1, 2, 5, 6 + Rec 8 merged into Rec 2)
- **Recommendations surviving** (Phase 3): 7 (compliance: 2 — Recs 5, 8; integration: 3 — Recs 1, 5, 7; scope-boundary: 3 — Recs 3, 4, 7; note: scope-boundary Rec 8 merged into Rec 2 counts as modified)
- **New recommendations added** (Phase 3): 5 (compliance: 2 — risk-of-gap rewrite, maintenance note broadening; integration: 2 — "Not assessed" label, compound-label rule; scope-boundary: 1 — FR-017 effort field acknowledgment)
- **Disputes remaining** (Phase 4): 5 (compliance: 3; integration: 3; scope-boundary: 2; with significant overlap — 3 distinct dispute topics)
- **Convergence points** (Phase 4): 7 unanimous + 2 bilateral = 9 total convergence points (with overlap across agents; 7 distinct positions converged)

---

### Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| C1 | compliance | Enrich Effort fields to four dimensions | P1 | Modified (compact inline format) | integration (format), scope-boundary (not evaluated) | Majority (compliance + scope-boundary agree on four-dimension requirement; integration agrees gap exists but disputes format) | Disputed |
| C2 | compliance | Add "Not assessed" to Acceptance Tier taxonomy | P1 | Modified (Phase 2 attribution framing) | scope-boundary (phase attribution only) | Unanimous | Accepted-Modified |
| C3 | compliance | Add compound-label permission rule | P1 | Modified (Phase 2 attribution framing) | scope-boundary (phase attribution only) | Unanimous on substance; Majority on priority (P1 vs P2) | Accepted-Modified |
| C4 | compliance | Add transition criteria to taxonomy | P2 | Modified (upgraded to P1) | scope-boundary (priority), integration (priority) | Unanimous | Accepted-Modified |
| C5 | compliance | Add "Depends On" to spec 001 | P2 | Surviving | None | Bilateral (compliance + scope-boundary) | Accepted |
| C6 | compliance | Add Location field to Structural Markers | P3 | Modified (reclassified as improvement) | integration (factual correction), scope-boundary (editorial enhancement) | None (uncontested but not explicitly adopted by others) | Accepted-Modified |
| C7 | compliance | Normalize FR-008a to FR-008 | P3 | Withdrawn | integration (traceability evidence) | N/A | Rejected |
| C8 | compliance | Add gap documentation convention note | P3 | Surviving | None | None (uncontested) | Accepted |
| C9 | compliance | Verify spec 005 gap list completeness | P3 | Modified (circularity filter applied) | scope-boundary (self-reference risk) | None (uncontested as modified) | Accepted-Modified |
| I1 | integration | Add Phase 4 cross-reference to Dispute-Parsing | P1 | Surviving | None | Unanimous | Accepted |
| I2 | integration | Add spec 002 Phase 4 re-evaluation note | P1 | Modified (lighter parenthetical) | compliance (scope concern), scope-boundary (phase purity) | None (disputed by scope-boundary) | Disputed |
| I3 | integration | Rewrite spec 005 risk-of-gap | P2 | Modified (scoped to remaining FRs) | compliance (scoping) | Unanimous | Accepted-Modified |
| I4 | integration | Add comparative anchor to effort estimates | P2 | Modified (elevated to P1, combined with FR-017) | compliance (insufficient alone) | Unanimous on scale definition; Disputed on per-spec format | Accepted-Modified (scale definition); Disputed (per-spec format) |
| I5 | integration | Specify existing SKILL.md sections for spec 003 | P2 | Surviving | None | None (uncontested) | Accepted |
| I6 | integration | Add transition criteria | P2 | Modified (elevated to P1) | scope-boundary (priority) | Unanimous | Accepted-Modified |
| I7 | integration | Consolidate spec 004 discovery prerequisite timing | P3 | Surviving | None | None (uncontested) | Accepted |
| I8 | integration | Update spec 002 effort field re: T019 | P3 | Modified (absorbed into I2) | scope-boundary (convention question) | N/A (absorbed) | Absorbed into I2 |
| S1 | scope-boundary | Add transition criteria to STATUS.md | P1 | Modified (Phase 2 framing, co-equal with Phase 3 items) | None on substance; compliance on priority (resolved) | Unanimous | Accepted-Modified |
| S2 | scope-boundary | Resolve spec 003 acceptance label | P1 | Modified (Phase 2 attribution, merged with S8) | compliance (phase attribution) | Unanimous | Accepted-Modified |
| S3 | scope-boundary | Add "Depends On" to spec 001 | P2 | Surviving | None | Bilateral (compliance + scope-boundary) | Accepted |
| S4 | scope-boundary | Add "Depends On" to spec 004 | P2 | Surviving | None | Bilateral (compliance + scope-boundary) | Accepted |
| S5 | scope-boundary | Verify compound-label rule implementation | P2 | Modified (upgraded to P1, add rule) | None on substance | Unanimous on substance; Majority on priority | Accepted-Modified |
| S6 | scope-boundary | Broaden maintenance note scope | P3 | Modified (combined with FR ref) | compliance (FR-008a normalization component disputed) | Bilateral (scope-boundary + compliance on broadening) | Disputed (FR-008a component); Accepted (broadening component) |
| S7 | scope-boundary | Add spec 005 to SKILL.md Structure Plan | P3 | Surviving | None | None (uncontested) | Accepted |
| S8 | scope-boundary | Add "Not assessed" acceptance label to taxonomy | P1 | Modified (merged into S2) | None | Unanimous | Merged into S2 |
| C-new-1 | compliance | Rewrite spec 005 risk-of-gap (new) | P2 | N/A (new in Phase 3) | None | Unanimous | Accepted |
| C-new-2 | compliance | Broaden maintenance note trigger (new) | P3 | N/A (new in Phase 3) | None | Bilateral | Accepted |
| I-new-1 | integration | Add "Not assessed" label (new) | P1 | N/A (new in Phase 3) | None | Unanimous | Accepted |
| I-new-2 | integration | Add compound-label rule (new) | P2 | N/A (new in Phase 3) | None on substance | Unanimous on substance; disputed priority | Accepted (substance) |
| S-new-1 | scope-boundary | Acknowledge FR-017 effort field incompleteness (new) | P2 | N/A (new in Phase 3) | None | Majority | Accepted |

---

### Dangerous Contradictions Found

**Resolved Contradictions**:

1. **Transition criteria priority: P1 vs. P2.** Compliance and integration both initially assigned P2; scope-boundary assigned P1. Scope-boundary cited the Phase 2 synthesis language: "a binding commitment, not an optional suggestion" (final.md L171). **Resolution**: Both compliance and integration conceded to P1 during revision. Compliance stated scope-boundary's reading is "more faithful" (compliance cross-review of scope-boundary, Dangerous Contradictions). Integration called it "a calibration error rather than a principled disagreement" (integration revision, Position Summary). All three agents converged on P1 unanimously.

2. **Phase 2 residuals: fix-now vs. flag-only.** Compliance treated Phase 2 binding commitments ("Not assessed" label, compound-label rule, transition criteria) as Phase 3 compliance gaps requiring immediate action. Scope-boundary treated them as Phase 2 scope items that Phase 3 should flag but not fix, since taxonomy modifications are Phase 2 scope. **Resolution**: Scope-boundary conceded the logical inconsistency in selectively treating the Phase 2 synthesis as binding for transition criteria but advisory for taxonomy changes (scope-boundary revision, Position Summary). All three agents adopted the "Phase 2 remediation executed during Phase 3" framing: the obligation belongs to Phase 2, the execution happens now because the Phase 3 checkpoint cannot pass without them.

3. **FR-008a normalization: change to FR-008 vs. retain FR-008a.** Compliance proposed normalizing "(FR-008a)" to "(FR-008)" in the maintenance note. Integration demonstrated that "FR-008a" appears in tasks.md as an established sub-requirement identifier, and normalization would break traceability. **Resolution**: Compliance withdrew Recommendation 7 with an explicit concession: "Integration is right. I had only checked traceability in one direction" (compliance revision, Recommendation 7). This is a clean resolution.

4. **Spec 005 risk-of-gap: tautological vs. adequate.** Integration flagged the risk-of-gap statement as tautological (describing deliverables, not consequences) and factually stale (referencing pre-Phase-3 state). Compliance's initial review treated it as structurally adequate. **Resolution**: Compliance conceded after cross-review, adding a new recommendation to rewrite the statement (compliance revision, New Recommendations). All three agents converged on scoping the rewrite to remaining unimplemented FRs.

5. **Spec 003 acceptance label: missed by integration.** Scope-boundary's cross-review of integration identified that integration failed to flag the undefined "Not started" label in the Acceptance Tier. **Resolution**: Integration acknowledged this as "a genuine oversight in my original review" (integration revision, New Recommendations) and added the fix as a new P1 recommendation.

**Unresolved Contradictions**:

1. **Effort field format: compact four-dimension inline vs. selective parenthetical.** Compliance and scope-boundary argue FR-017's "covering: new files, logic complexity, testing surface, and relative effort" is an enumerative requirement mandating all four dimensions per spec. Integration argues the dimensions can be addressed selectively, with a global scale definition making some dimensions inferable. **Agents on each side**: Compliance + scope-boundary (four-dimension coverage) vs. integration (selective parenthetical). **Synthesizer assessment**: Compliance's reading of FR-017 is stronger. The colon-and-list construction ("covering: X, Y, Z, and W") is standard requirements enumeration. Scope-boundary's observation about US9's verification criterion ("STATUS.md contains an 'Effort' field for each of the 5 specs") creating ambiguity is fair, but verification criteria test the minimum observable condition, not the full requirement — FR-017 itself is authoritative on what the content must cover. However, integration's scanability concern is legitimate and compliance's compact inline format already addresses it. The dispute is narrower than it appears: all three agents agree the current fields are insufficient, agree a global scale definition should be added, and agree the fields need more dimensional coverage. The remaining disagreement is whether every dimension must be explicitly labeled per spec or whether dimensions inferable from the scale tier can be omitted.

2. **Spec 002 Phase 4 re-evaluation note placement: STATUS.md vs. gate summary.** Integration proposes adding a post-condition parenthetical to spec 002's Notes field. Scope-boundary opposes embedding temporal predicates about future phases in a current-state document, citing the Phase 2 principle that each phase produces a deliverable accurate as of its completion date (final.md L116). **Agents on each side**: Integration (STATUS.md entry) vs. scope-boundary (gate summary). Compliance raised the concern in cross-review but did not take a firm position. **Synthesizer assessment**: Scope-boundary's position is stronger for the general principle but weaker for the specific case. The Phase 2 synthesis itself recorded the re-evaluation obligation (final.md L214), and if STATUS.md is the authoritative single-document reference (SC-003), then a reader who does not consult gate summaries will miss the obligation. However, scope-boundary correctly identifies that Phase 4 post-conditions scale poorly in STATUS.md — if every cross-spec modification generates a post-condition note, the entries become forward-looking change logs. The compromise is to permit the specific re-evaluation note (it is a documented Phase 2 obligation) while establishing a principle that STATUS.md entries generally describe current state, with inherited post-conditions from prior deliberations being the narrow exception.

3. **Maintenance note FR-008a reference in scope-boundary's combined edit.** Scope-boundary's revised Recommendation 6 combines trigger-scope broadening with changing "(FR-008a)" to "(FR-008)". Compliance withdrew the normalization in Phase 3 after integration's evidence. **Agents on each side**: Scope-boundary (normalize) vs. compliance + integration (retain FR-008a). **Synthesizer assessment**: Compliance and integration's position is clearly stronger. Compliance originated the normalization proposal, evaluated the counter-evidence, and explicitly withdrew. Scope-boundary's revision appears to have incorporated compliance's original (pre-withdrawal) recommendation. The trigger-scope broadening should be adopted; the FR-008a normalization should be rejected.

---

### Systemic Contradictions

- **Phase 2 obligation inheritance model**
  - **Manifests in**: Transition criteria priority dispute, "Not assessed" label phase attribution, compound-label rule ownership, maintenance note FR-008a reference, and the Phase 2 remediation framing dispute.
  - **Root cause**: The Phase 2 synthesis created "binding commitments" but the Phase 3 task decomposition (tasks.md) did not incorporate them. This left a gap between inter-phase obligations and intra-phase task definitions. Each agent resolved the gap differently: compliance treated the synthesis as authoritative over the task list; scope-boundary initially treated the task list as defining Phase 3's scope; integration evaluated each item on its merits without a systematic framework.
  - **Implication for spec**: The deliberator deliberation framework needs an explicit rule about how binding commitments from phase gate syntheses are carried into subsequent phase task lists. The current convention — recording commitments in the synthesis document and hoping they are incorporated — creates the exact obligation gap this deliberation spent significant effort resolving. The spec should either (a) require that phase gate syntheses produce a machine-readable commitments list that the next phase's tasks.md must incorporate, or (b) declare that the synthesis document itself is authoritative and its commitments are automatically in scope for the next phase regardless of task decomposition.

- **Phase-scoped deliverables vs. living-document function**
  - **Manifests in**: Spec 002 re-evaluation note placement, Dispute-Parsing T013 cross-reference, maintenance note trigger scope, and spec 005 risk-of-gap staleness.
  - **Root cause**: STATUS.md serves two conflicting functions: (1) a phase-scoped deliverable that should be accurate as of its completion date (Phase 2 principle, final.md L116), and (2) a living cross-spec reference that should always reflect current state and upcoming risks (SC-003's "zero ambiguity about what is safe to build on"). These functions create tension when Phase 3 content references Phase 4 work: forward references improve the living-document function but undermine the phase-scoped deliverable function.
  - **Implication for spec**: STATUS.md should be explicitly designated as a living document that transcends phase boundaries, with a clear convention for marking forward references (e.g., a "Post-conditions" sub-field in per-spec entries). Alternatively, phase-scoped deliverables and living documents should be separate artifacts, with STATUS.md as the living document and gate summaries as phase-scoped deliverables. The current ambiguity forces each deliberation to re-litigate the boundary.

- **Task decomposition fidelity to FRs**
  - **Manifests in**: Effort field dimension coverage (T011 paraphrased FR-017), SKILL.md Structure Plan scope (T012 narrowed FR-019 to three specs), and spec 005 gap list scoping.
  - **Root cause**: Task descriptions in tasks.md paraphrase FRs with varying degrees of fidelity. When a task description simplifies an FR, the implementation follows the task (which is the immediate instruction) rather than the FR (which is the authoritative requirement). This creates gaps that are only discovered during gate reviews when an agent checks FR compliance rather than task compliance.
  - **Implication for spec**: Task descriptions should either quote FR text verbatim for the key requirements or include explicit traceability markers (e.g., "This task satisfies FR-017's four-dimension requirement") so that implementors can check the authoritative source. The spec could require that each task's description link to its source FR(s) and note any intentional scope narrowing.

- **Review lens asymmetry**
  - **Manifests in**: FR-017 effort field coverage (compliance flagged, scope-boundary did not evaluate, integration proposed a different fix), spec 003 label (compliance and scope-boundary flagged, integration missed), Structural Markers Location field (compliance flagged, others did not evaluate).
  - **Root cause**: Each agent's mandate defines a review lens (compliance: FR satisfaction; integration: content accuracy and usability; scope-boundary: phase/scope integrity) that naturally excludes certain findings. Cross-review is designed to catch these gaps, and it largely worked — integration added the "Not assessed" label after scope-boundary's cross-review, scope-boundary acknowledged FR-017 after compliance's cross-review. But the process relies on cross-reviewers explicitly naming gaps rather than on structural coverage guarantees.
  - **Implication for spec**: The deliberation framework could add a coverage matrix requirement to the cross-review phase: each cross-reviewer must confirm they evaluated all actionable recommendations from the reviewed agent, even if the evaluation is "outside my mandate, no comment." This would prevent implicit endorsements through silence (e.g., scope-boundary's silence on effort fields being interpreted as acceptance).

---

### Convergence Achieved

1. **Transition criteria must be added at P1** — Strength: Unanimous
   - **Agreed recommendation**: Add to STATUS.md after the "Interpreting the Two Tiers" paragraph (L24): "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied."
   - **Supporting agents**: compliance (revision, Rec 4 modified), integration (revision, Rec 6 modified), scope-boundary (revision, Rec 1 modified)
   - **Evidence basis**: Phase 2 synthesis final.md L171 records this as a "binding commitment, not an optional suggestion" assigned to T008 (final.md L202). The dual-condition formulation was bilaterally agreed in Phase 2 (final.md L152-156). Without transition criteria, the boundary between Feature-complete and Spec-complete is implicit, making every future label transition a judgment call.
   - **Pre-existing or earned**: Earned. The formulation was agreed in Phase 2, but the priority required Phase 3 deliberation. Integration and compliance both upgraded from P2 to P1 after scope-boundary's cross-review argument proved decisive.

2. **Add "Not assessed" to Acceptance Tier and relabel spec 003** — Strength: Unanimous
   - **Agreed recommendation**: Add `- **Not assessed**: No acceptance criteria have been evaluated.` to the Acceptance Tier taxonomy (after L20). Change spec 003 (L45) from `**Acceptance**: Not started` to `**Acceptance**: Not assessed`. Frame as Phase 2 remediation executed during Phase 3.
   - **Supporting agents**: compliance (revision, Rec 2 modified), integration (revision, new rec), scope-boundary (revision, Rec 2 modified + Rec 8 merged)
   - **Evidence basis**: Phase 2 unanimously agreed (final.md L122-126, L186-188). FR-009 (spec.md L216) requires labels to use the defined convention. "Not started" is an Implementation Tier label used in the Acceptance Tier — a cross-tier reuse the Phase 2 deliberation identified as an orthogonality violation.
   - **Pre-existing or earned**: Pre-existing from Phase 2. Phase 3 deliberation resolved the phase-attribution question (Phase 2 obligation executed during Phase 3).

3. **Add compound-label permission rule to Implementation Tier** — Strength: Unanimous (substance), Majority (priority — P1: compliance + scope-boundary; P2: integration)
   - **Agreed recommendation**: Add to Implementation Tier section (after L13): "Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label."
   - **Supporting agents**: compliance (revision, Rec 3 modified), integration (revision, new rec), scope-boundary (revision, Rec 5 modified)
   - **Evidence basis**: Phase 2 synthesis P1 item 4 (final.md L192). Spec 004 (STATUS.md L52) already uses the compound format without formal taxonomic backing. The Phase 2 synthesis resolved this in favor of compound labels with a constraining rule (final.md L165).
   - **Pre-existing or earned**: Earned. Scope-boundary opposed compound labels in Phase 2 (advocating normalization to "Partially-complete"). In Phase 3, scope-boundary resolved the logical inconsistency by accepting that if the Phase 2 synthesis is binding for transition criteria, it must also be binding for the compound-label rule. This was the most significant position shift across both phases.

4. **Add T013 cross-reference to Dispute-Parsing heading-match note** — Strength: Unanimous
   - **Agreed recommendation**: Append to STATUS.md L93: "Phase 4 task T013 (FR-007) will add explicit matching rules."
   - **Supporting agents**: integration (revision, Rec 1 surviving), compliance (cross-review Safe Agreements), scope-boundary (cross-review Safe Agreements; disputes, Flexibility item 2)
   - **Evidence basis**: Without the cross-reference, implementors encounter a known gap with no visibility into whether it will be fixed (integration revision, Rec 1). This is "the exact failure mode SC-004 exists to prevent" (integration disputes, Non-Negotiables item 1). Scope-boundary acknowledges it describes "a current deficiency with a scheduled fix" rather than a future-phase post-condition.
   - **Pre-existing or earned**: Pre-existing. Integration identified this in Phase 1, both cross-reviewers validated it, and no agent contested it through any phase.

5. **Rewrite spec 005 risk-of-gap as cost-of-absence statement** — Strength: Unanimous
   - **Agreed recommendation**: Replace STATUS.md L63 with a consequence-oriented statement scoped to remaining unimplemented FRs (FR-007, FR-011, FR-014, FR-015), focusing on SKILL.md Phase 6 edge cases and incomplete dispute-parsing cross-references.
   - **Supporting agents**: integration (revision, Rec 3 modified), compliance (revision, new rec), scope-boundary (cross-review acknowledgment)
   - **Evidence basis**: The current text ("STATUS.md lacks complete cross-spec reference information") is factually stale — Phase 3 has already added that information. The statement does not follow the consequence-oriented pattern established by specs 001-004, reducing its comparative value for prioritization.
   - **Pre-existing or earned**: Earned. Integration identified the tautology in Phase 1. Compliance's cross-review refined the scoping. The final text converged during revision.

6. **Add "Depends On" fields to specs 001 and 004** — Strength: Bilateral (compliance + scope-boundary), integration non-opposing
   - **Agreed recommendation**: Add `**Depends On**: None (foundational)` to spec 001 and `**Depends On**: (none -- self-contained engine)` to spec 004.
   - **Supporting agents**: compliance (revision, Rec 5 surviving, P2), scope-boundary (revision, Recs 3-4 surviving, P2)
   - **Evidence basis**: STATUS.md L129 declares per-spec entries authoritative. An omitted field creates ambiguity about whether the dependency was assessed or omitted. The dependency graph (L111, L116) provides the information but is not the authoritative source per L129.
   - **Pre-existing or earned**: Pre-existing. Both agents identified this in Phase 1 and the position never shifted.

7. **Broaden maintenance note trigger scope** — Strength: Bilateral (compliance + scope-boundary), integration non-opposing
   - **Agreed recommendation**: Amend STATUS.md L138 to cover shared subsystem stability/consumer changes and SKILL.md Structure Plan updates, in addition to implementation/acceptance status changes. Retain "(FR-008a)" identifier.
   - **Supporting agents**: scope-boundary (revision, Rec 6 modified), compliance (revision, new rec)
   - **Evidence basis**: Phase 3 added living-content sections (Shared Subsystems, Structure Plan) not covered by the current maintenance trigger. Without broadening, these sections could become stale without anyone feeling obligated to update them.
   - **Pre-existing or earned**: Earned. Scope-boundary identified the trigger-scope gap; compliance contributed the FR reference context. The FR-008a retention was resolved through integration's traceability evidence and compliance's explicit withdrawal.

---

<!-- DELIBERATOR:DISPUTES_BEGIN -->
### Remaining Disputes

- **Dispute: Effort Field Format — Four-Dimension Inline vs. Selective Parenthetical**
  - **Positions**: Compliance requires each spec's Effort field to address all four FR-017 dimensions (new files, logic complexity, testing surface, relative effort) in a compact inline format (compliance disputes, Dispute 1). Integration proposes a global scale definition plus selective per-spec parentheticals covering only the most decision-relevant dimensions (integration disputes, Dispute 1). Scope-boundary endorses the four-dimension requirement but is flexible on format (scope-boundary disputes, Dispute 1).
  - **Arguments**: Compliance argues FR-017's "covering: new files, logic complexity, testing surface, and relative effort" is an enumerative construction requiring all four. Integration argues the scale definition implicitly addresses some dimensions (e.g., "Small = targeted edits" implies no new files and low complexity), and selective parentheticals preserve scanability. Scope-boundary raises the US9 verification criterion ("STATUS.md contains an 'Effort' field") as evidence of ambiguity between structural presence and dimensional completeness.
  - **Synthesizer assessment**: Compliance's FR-017 reading is the stronger interpretation. The "covering: X, Y, Z, and W" construction is standard requirements enumeration, not an illustrative list. Verification criteria specify what is mechanically testable, not the full scope of the requirement — otherwise no FR would require more than what its verification criterion checks. However, integration's scanability concern is legitimate and compliance's compact inline format already accommodates it. The remaining gap is narrow: whether dimensions inferable from the scale tier must still be explicitly stated. The pragmatic answer is yes, because (a) it eliminates judgment calls about what is "inferable," (b) the compact inline format keeps each entry to a single line, and (c) systematic coverage enables cross-spec comparison.
  - **Recommended resolution**: Adopt compliance's compact four-dimension inline format as the standard, with integration's global scale definition as a complementary addition. Permit abbreviation only when a dimension is genuinely null (e.g., spec 002's "None -- complete" need not mechanically list four dimensions of nothing). The test: every spec with remaining work must explicitly address all four FR-017 dimensions in its Effort field. The scale definition goes in the taxonomy section as a separate P2 addition. All three agents agree on the scale definition; the four-dimension inline format has majority support (compliance + scope-boundary) with integration's core concern (scanability) addressed by the compact format.

- **Dispute: Spec 002 Phase 4 Re-Evaluation Note Placement**
  - **Positions**: Integration proposes a parenthetical in spec 002's Notes field: "(Phase 4 post-condition: re-evaluate Spec-complete label after T019 modifies Round Termination Check cross-references.)" (integration disputes, Dispute 1 Non-Negotiables + revision Rec 2). Scope-boundary opposes embedding temporal predicates about future phases in STATUS.md per-spec entries, citing the Phase 2 principle that each phase produces a deliverable accurate as of its completion date (scope-boundary disputes, Dispute 2).
  - **Arguments**: Integration argues that if STATUS.md is the authoritative single-document reference, a reader who does not consult gate summaries will miss the re-evaluation obligation. The Phase 2 synthesis itself recorded this obligation (final.md L214). Scope-boundary argues that Phase 4 post-conditions scale poorly in STATUS.md entries, and the re-evaluation obligation should live in the gate summary, not the per-spec entry.
  - **Synthesizer assessment**: Both positions have merit, but the distinction scope-boundary draws between types of forward references is the most productive framework. The Dispute-Parsing T013 cross-reference (which all agents accept) describes a *current deficiency* with a *scheduled fix* — it tells a reader that something is broken now and when it will be fixed. The spec 002 re-evaluation note describes a *future event* that *may or may not* change a current label — it is predictive rather than descriptive. This distinction is principled and scalable. However, the re-evaluation obligation is real and must be recorded somewhere visible.
  - **Recommended resolution**: Record the spec 002 re-evaluation obligation in this synthesis document (which serves as the Phase 3 gate summary) as a formal post-condition for Phase 4. Do not add it to STATUS.md's per-spec Notes field. Establish a convention: STATUS.md entries may reference scheduled fixes for current deficiencies (like the T013 cross-reference) but should not contain post-conditions about future label re-evaluations. Post-conditions belong in gate summaries. **Phase 4 post-condition**: After T019 modifies the Round Termination Check to use a Dispute-Parsing Subsystem cross-reference, re-evaluate spec 002's "Spec-complete" label against spec 002's acceptance scenarios.

- **Dispute: Compound-Label Permission Rule Priority — P1 vs. P2**
  - **Positions**: Compliance and scope-boundary assign P1, deriving priority from the Phase 2 synthesis's P1 grouping (final.md L192). Integration assigns P2, arguing that while the compound label lacks formal backing, it is already in use, self-documenting, and interpretable — making it a future-inconsistency prevention measure rather than a current-interpretation blocker (integration disputes, Dispute 2).
  - **Arguments**: Compliance and scope-boundary argue that all Phase 2 binding commitments carry forward at their original priority level as a governance principle. Integration argues that the Phase 2 synthesis grouped four items under a single P1 heading for administrative convenience, and that urgency within the block should be differentiated: undefined labels (blocking interpretation) vs. undefined formats (preventing future inconsistency) are different categories.
  - **Synthesizer assessment**: Integration's distinction between "blocks interpretation" and "lacks formal definition for a readable format" is analytically sound. The "Not assessed" label and transition criteria fix states where the document is demonstrably broken — a label the taxonomy does not define, and a transition boundary that does not exist. The compound-label rule formalizes a pattern already in use. However, the governance principle that Phase 2 binding commitments carry forward intact is important for process integrity. The compromise that best serves both concerns is to adopt the rule at P1 (honoring the binding commitment) but sequence its implementation after the "Not assessed" label and transition criteria within the P1 block (honoring integration's urgency distinction).
  - **Recommended resolution**: Adopt the compound-label permission rule at P1, but with an explicit implementation ordering within P1: (1) "Not assessed" label + spec 003 relabeling, (2) transition criteria, (3) compound-label permission rule. This preserves the governance principle while acknowledging the urgency gradient. Integration stated willingness to accept P1 "if the synthesizer adopts the governance principle" with the ordering caveat (integration disputes, Flexibility item 2).
<!-- DELIBERATOR:DISPUTES_END -->

---

### Systemic Contradictions

*(See section above — consolidated under "Systemic Contradictions" heading per the template.)*

---

### Actionable Spec Changes

**P1 — Must implement** (blocking issues or unanimous convergence):

1. **Add "Not assessed" to Acceptance Tier taxonomy and relabel spec 003**: Add `- **Not assessed**: No acceptance criteria have been evaluated.` after STATUS.md L20. Change STATUS.md L45 from `**Acceptance**: Not started` to `**Acceptance**: Not assessed`. Source: Convergence point 2 (unanimous); Phase 2 binding commitment final.md L186-188; Recommendations C2, S2/S8, I-new-1.

2. **Add transition criteria to taxonomy section**: Add after the "Interpreting the Two Tiers" paragraph (STATUS.md L24): "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." Source: Convergence point 1 (unanimous); Phase 2 binding commitment final.md L171, L202; Recommendations C4, I6, S1.

3. **Add compound-label permission rule to Implementation Tier**: Add after STATUS.md L13: "Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label." Source: Convergence point 3 (unanimous substance, majority priority); Phase 2 binding commitment final.md L192; Recommendations C3, S5, I-new-2. Implement after items 1 and 2 within the P1 block.

4. **Add T013 cross-reference to Dispute-Parsing heading-match note**: Append to STATUS.md L93: "; Phase 4 task T013 (FR-007) will add explicit matching rules." Source: Convergence point 4 (unanimous); Recommendation I1.

5. **Enrich Effort fields to cover four FR-017 dimensions**: For each spec with remaining work (001, 003, 004, 005), expand the Effort field to address new files, logic complexity, testing surface, and relative effort in a compact inline format. Example for spec 001: "**Effort**: Small — New files: none; logic complexity: low (template-level instructions); testing surface: behavioral verification of template output. 2 FRs remain (FR-025 per-FR citation, FR-026 per-file attribution)." Spec 002's "None -- complete" may remain as-is. Source: Disputed resolution (synthesizer assessment favors compliance's reading of FR-017); Recommendations C1, I4, S-new-1.

**P2 — Should implement** (majority convergence or strong single-agent case):

1. **Add global scale definition for effort estimates**: Add to the taxonomy or enrichment section: "Effort is relative: Small = targeted edits to existing files; Medium = new sections or modest new functionality; Large = multiple new components with cross-cutting integration." Source: Recommendation I4 (scale definition component); agreed by all agents.

2. **Rewrite spec 005 risk-of-gap statement**: Replace STATUS.md L63 with a consequence-oriented statement scoped to remaining FRs: "SKILL.md Phase 6 edge cases (heading match semantics, missing document handling, overwrite behavior) remain undocumented, and the dispute-parsing subsystem's inline references in Round Termination Check and Trigger Evaluation have not been consolidated, increasing the risk of divergent parsing implementations across consumers." Source: Convergence point 5 (unanimous); Recommendations I3, C-new-1.

3. **Add "Depends On" fields to specs 001 and 004**: Add `**Depends On**: None (foundational)` to spec 001's entry (after L31). Add `**Depends On**: (none -- self-contained engine)` to spec 004's entry (after L52). Source: Convergence point 6 (bilateral); Recommendations C5, S3, S4.

4. **Specify existing SKILL.md sections that change for spec 003**: Add to STATUS.md spec 003 Structure Plan entry (L76-80): "Existing sections modified: Step 1 (Parse Config) for subcommand-specific validation rules; Step 4 (Execute Phases) for `converge` subcommand's Phase A/B/C orchestration flow; Step 5 (Report) for subcommand-specific output formatting." Source: Recommendation I5 (uncontested); FR-019 requires both new and existing sections.

5. **Add spec 002 Phase 4 re-evaluation note to spec 002 Notes field**: Add parenthetical to spec 002's Notes: "(Phase 4 post-condition: re-evaluate Spec-complete label after T019 modifies Round Termination Check cross-references.)" Source: Disputed resolution — synthesizer assessed this as a real obligation from Phase 2 (final.md L214) that warrants visibility, but as a compromise with scope-boundary's objection, implementors may alternatively record this post-condition in the gate summary only. Integration's Recommendation I2 (modified) is the source. Note: This is the one P2 item where agents disagree on placement. If the principle established in the disputes section (STATUS.md entries describe current deficiencies with scheduled fixes, not future events) is adopted strictly, this moves to the gate summary instead.

**P3 — Consider implementing** (bilateral agreement or strong but disputed):

1. **Broaden maintenance note trigger scope**: Amend STATUS.md L138 to: "This document MUST be updated when any spec's implementation or acceptance status changes, when shared subsystem stability or consumers change, or when the SKILL.md Structure Plan is affected by implementation progress (FR-008a)." Retain "(FR-008a)" — do not normalize to "(FR-008)". Source: Convergence point 7 (bilateral); Recommendations S6 (broadening component), C-new-2. Note: compliance's withdrawal of FR-008a normalization (C7) must be respected.

2. **Add spec 005 to SKILL.md Structure Plan**: Add entry: "### 005 — P2/P3 Backlog Hardening. **Status**: Needs additions. **Changes required**: Phase 6 heading match semantics (FR-007), dispute-parsing cross-references in Round Termination Check and Trigger Evaluation (FR-011), Phase 4 missing document edge case (FR-014), Phase 6 overwrite semantics (FR-015). Note: all changes are documentation edits to existing SKILL.md sections, not new structural additions." Source: Recommendation S7 (uncontested). Note: T012 specifies "specs 002, 003, 004" — this addition closes the gap between T012 and FR-019.

3. **Add Location field to Structural Markers subsystem entry**: Add after STATUS.md L96: "**Location**: SKILL.md Step 3 (TEMPLATE_STATUS check), Phase 5 synthesis templates (DISPUTES markers)." Source: Recommendation C6 (modified to improvement recommendation). Note: classified as an editorial improvement, not a compliance gap.

4. **Consolidate spec 004 discovery prerequisite timing**: Expand spec 003's "Depends On" field to: "004 (soft: `/deliberator interests` preset suggestions — discovery features (FR-022-024) must be implemented before spec 003 Phase A)." Source: Recommendation I7 (uncontested).

5. **Add gap documentation convention note**: Add to taxonomy section: "Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability." Source: Recommendation C8 (uncontested); Phase 2 synthesis P3-1 (final.md L208).

6. **Verify spec 005 gap list completeness for SKILL.md-targeted FRs**: Verify the four listed gaps (FR-007, FR-011, FR-014, FR-015) are complete for SKILL.md-targeted FRs. Do not add STATUS.md-targeted FRs (circularity risk). Add clarifying parenthetical: "(SKILL.md-targeted FRs only; STATUS.md-targeted FRs are tracked by the maintenance obligation at the bottom of this document)." Source: Recommendation C9 (modified with scope-boundary's circularity filter).

---

### Key Concessions

**compliance**:
- Withdrew Recommendation 7 (FR-008a normalization) after integration demonstrated that "FR-008a" traces to tasks.md as an established sub-requirement identifier. Compliance stated: "Integration is right. I had only checked traceability in one direction (STATUS.md to spec.md) and missed the tasks.md link" (compliance revision, Recommendation 7). This was a clean, evidence-based concession.
- Upgraded transition criteria from P2 to P1 after scope-boundary's argument about binding commitment language proved persuasive: "I should yield upward to P1, since the synthesis's use of 'binding commitment' was meant to prevent exactly the scenario where this is treated as optional" (compliance cross-review of scope-boundary, Dangerous Contradictions).
- Adopted the "Phase 2 remediation prerequisite" framing for all Phase 2 residuals (Recommendations 2, 3, 4) after scope-boundary's phase-attribution challenge: "This is a genuine synthesis of the two positions, not a strategic compromise" (compliance revision, Position Summary).
- Accepted scope-boundary's circularity filter for spec 005 gap list verification (Recommendation 9): "Scope-boundary's circularity filter is a genuine insight I missed" (compliance revision, Recommendation 9).

**integration**:
- Upgraded transition criteria from P2 to P1, calling the original assessment "a calibration error rather than a principled disagreement" (integration revision, Position Summary). This was the most significant concession by integration, as it accepted the precedent that Phase 2 binding commitments determine Phase 3 priorities.
- Added two new recommendations ("Not assessed" label, compound-label rule) after scope-boundary's cross-review identified these as oversight gaps in the original review: "This is a genuine oversight in my original review" (integration revision, new recommendation rationale for "Not assessed").
- Acknowledged factual error in the Alignment section regarding subsystem entry field consistency after compliance's cross-review noted the Structural Markers entry does not share the same field structure as the other two entries (integration cross-review of compliance, Tensions, "Shared subsystem entry consistency").
- Absorbed Recommendation 8 (spec 002 effort field T019 note) into Recommendation 2 after scope-boundary's framing clarified that effort fields should be spec-scoped, with cross-spec impacts belonging in the Notes field.

**scope-boundary**:
- Resolved the selective Phase 2 authority inconsistency — the most significant position shift in the entire deliberation. Scope-boundary had treated the Phase 2 synthesis as binding for transition criteria but advisory for taxonomy changes. After compliance's cross-review identified this as logically inconsistent, scope-boundary adopted a uniform principle: "all binding commitments from the Phase 2 synthesis carry forward as Phase 3 obligations, regardless of whether they touch the taxonomy section" (scope-boundary revision, Position Summary). This concession enabled the "Not assessed" label and compound-label rule to be accepted as Phase 3 actions.
- Upgraded compound-label permission rule from P2 "verify" to P1 "add" after accepting the logical consequence of the binding-authority principle (scope-boundary revision, Recommendation 5).
- Acknowledged FR-017 effort field incompleteness as a legitimate finding after compliance's cross-review, adding a new recommendation: "My silence in the original review should not be interpreted as endorsement of the current Effort fields' completeness against FR-017" (scope-boundary revision, New Recommendations).

---

### Phase 4 Post-Conditions

The following obligations were identified during this deliberation and must be tracked for Phase 4:

1. **Spec 002 label re-evaluation**: After T019 modifies the Round Termination Check to use a Dispute-Parsing Subsystem cross-reference, re-evaluate spec 002's "Spec-complete" label against spec 002's acceptance scenarios. Source: Phase 2 synthesis final.md L214; integration Recommendation I2.

---

*Synthesis complete. 15 artifacts analyzed across 4 deliberation phases. 7 convergence points achieved (5 unanimous, 2 bilateral). 3 disputes resolved by synthesizer assessment. All recommendations traced to source artifacts.*

*Updated: 2026-03-20*
