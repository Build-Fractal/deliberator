# Phase 3 Cooperative Revision — Compliance

**Agent**: compliance
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening
**Revision iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Enrich Effort fields to four dimensions

- **Original position**: Effort fields for all five specs must be expanded to include the four dimensions FR-017 explicitly requires (new files, logic complexity, testing surface, relative effort), not just the relative-effort label and a summary sentence.
- **Disposition**: Modified
- **Explanation**:

Integration's cross-review (Dangerous Contradictions, "Effort field remediation scope") challenged the mechanical four-line-per-spec format, arguing it would add twenty additional data points to a document meant to be scannable, and proposed a comparative anchor (scale definition) as an alternative. Integration's suggested compromise was to add a single parenthetical clarification addressing the most decision-relevant non-obvious dimension rather than mechanically listing all four. Scope-boundary's cross-review (Dangerous Contradictions, "Effort field enrichment: P1 fix vs. acceptable paraphrase") did not contest the recommendation on its merits but noted it was outside scope-boundary's evaluation area, and explicitly stated "compliance's analysis of the T011-vs-FR-017 gap is well-grounded in the spec text."

Integration is correct that scanability matters and that twenty additional sub-lines would degrade the quick-reference function of STATUS.md. However, the FR-017 text (spec.md L242) is unambiguous: "covering: new files, logic complexity, testing surface, and relative effort (small/medium/large)." The colon-and-list construction is enumerative. The FR requires coverage of all four dimensions, not just the most interesting one.

**Modified recommendation**: Each spec's Effort field must address all four FR-017 dimensions, but in a compact inline format rather than four separate lines. Example for spec 001: "**Effort**: Small — New files: none; logic complexity: low (template-level instructions); testing surface: behavioral verification of template output. 2 FRs remain (FR-025 per-FR citation, FR-026 per-file attribution)." Additionally, adopt integration's comparative-anchor proposal as a secondary improvement: add a one-sentence scale definition to the taxonomy section (e.g., "Small = targeted edits to existing files; Medium = new sections or modest new functionality; Large = multiple new components with cross-cutting integration"). The four-dimension inline format satisfies FR-017's literal requirement while the compact delivery preserves scanability. The scale definition is additive, not a substitute. Priority remains P1 for the four-dimension enrichment; P2 for the scale definition.

#### Recommendation 2: Add "Not assessed" to Acceptance Tier taxonomy

- **Original position**: Add "Not assessed" as a third acceptance-tier label and relabel spec 003 from "Not started" to "Not assessed."
- **Disposition**: Modified
- **Explanation**:

Scope-boundary's cross-review (Dangerous Contradictions, "Phase 2 residuals: flag-only vs. fix-now") challenged the framing of this as a Phase 3 obligation. Scope-boundary's argument: this is a Phase 2 deliverable, and fixing it in Phase 3 constitutes a taxonomy modification that falls outside Phase 3's task scope. Scope-boundary proposed documenting these as "Phase 2 incomplete items that constitute preconditions for the Phase 3 checkpoint claim" and resolving them in a targeted Phase 2 remediation pass rather than as Phase 3 task outputs. Integration's cross-review (Tensions, "Spec 003 'Not assessed' label") confirmed this is "a genuine inconsistency that integration missed" and agreed it should be fixed regardless of phase attribution, stating: "The question of which phase owns the fix is secondary to getting it done."

Scope-boundary's phase-attribution argument has formal merit: T006 and T007 (Phase 2 tasks) are the natural owners of taxonomy changes, and Phase 3's task list does not include taxonomy modifications. However, scope-boundary's own Safe Agreements section acknowledges the fix is needed and assigns it high confidence. The Phase 3 checkpoint claims STATUS.md is the "complete cross-spec reference" — a document containing an undefined label ("Not started" in the Acceptance Tier for spec 003) cannot satisfy this claim. The fix must happen before Phase 3 can pass.

**Modified recommendation**: Add "Not assessed" to the Acceptance Tier taxonomy and relabel spec 003. Attribute the obligation to Phase 2's binding commitment (final.md L122-126, L186-188). Frame the edit as a Phase 2 remediation prerequisite for Phase 3 checkpoint passage, not as a Phase 3 task output. This preserves scope-boundary's phase-attribution model while ensuring the fix is not deferred. Priority remains P1.

#### Recommendation 3: Add compound-label permission rule to Implementation Tier

- **Original position**: Add a compound-label permission rule to the Implementation Tier section so that spec 004's existing label format has a formal definition.
- **Disposition**: Modified
- **Explanation**:

Scope-boundary's cross-review (Dangerous Contradictions, "Phase 2 residuals: flag-only vs. fix-now") applied the same phase-attribution challenge as for Recommendation 2. The compound-label rule is a Phase 2 deliverable (final.md L192, P1-4), and adding it in Phase 3 constitutes taxonomy modification. Integration's cross-review (Tensions, "Spec 003 'Not assessed' label" — which covers the broader Phase 2 residuals pattern) confirms that Phase 2 residuals should be evaluated on their merits, not dropped because only one reviewer flagged them.

The same reasoning as Recommendation 2 applies. The compound-label rule is a Phase 2 obligation that was not implemented. Spec 004's entry (STATUS.md L52) already uses the compound format. A taxonomy that does not define a label format in active use is incomplete.

**Modified recommendation**: Add the compound-label permission rule as specified. Attribute the obligation to Phase 2 (final.md L192). Frame as a Phase 2 remediation prerequisite for Phase 3 checkpoint passage. Priority: P1 (unchanged), but with the phase-attribution clarification.

#### Recommendation 4: Add transition criteria to taxonomy section

- **Original position**: Add dual-condition transition criteria after the "Interpreting the Two Tiers" paragraph, at P2 priority.
- **Disposition**: Modified
- **Explanation**:

Scope-boundary's cross-review (Dangerous Contradictions, "Transition criteria: where to place them") agreed on the substance and formulation but assigned P1 rather than P2, and noted that the Phase 2 synthesis explicitly recorded this as a binding commitment (final.md L171: "binding commitment, not an optional suggestion"). Scope-boundary argued that the Phase 2 synthesis's "binding" language was meant to prevent exactly the scenario where this is treated as optional. In my own cross-review of scope-boundary (Dangerous Contradictions, "Transition criteria priority classification"), I acknowledged scope-boundary's reading of the synthesis is more faithful and stated: "I should yield upward to P1."

Integration's cross-review (Dangerous Contradictions, "Priority assignment of transition criteria") proposed a middle-ground: acknowledge the Phase 2 binding commitment as real but classify the absence as a spec-level gap rather than a Phase 3 execution failure, since the task decomposition (T008 in tasks.md L63) does not mention transition criteria.

Scope-boundary is correct on priority. The Phase 2 synthesis (final.md L202) explicitly assigned this to T008 and called it binding. Integration is correct that T008's task description does not mention transition criteria — this is a task-decomposition gap, not evidence that the obligation does not exist.

**Modified recommendation**: Add dual-condition transition criteria after the "Interpreting the Two Tiers" paragraph, at **P1** priority (upgraded from P2). The formulation is unchanged: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." Attribute to Phase 2 binding commitment (final.md L171, L202). Frame as a Phase 2 remediation prerequisite for Phase 3 checkpoint passage, consistent with the modified framing for Recommendations 2 and 3.

#### Recommendation 5: Add "Depends On" line to spec 001 entry

- **Original position**: Add `**Depends On**: None (foundational)` to spec 001's entry to eliminate ambiguity about whether the dependency was assessed.
- **Disposition**: Surviving
- **Explanation**:

Neither integration nor scope-boundary challenged this recommendation. Scope-boundary's cross-review (Safe Agreements, "Spec 001 missing 'Depends On' field") explicitly agreed, assigning identical priority (P2) and near-identical wording. Integration's cross-review does not address this item. In my own cross-review of scope-boundary (Safe Agreements, "'Depends On' field should be present for spec 001"), I confirmed the agreement and noted scope-boundary additionally flagged spec 004 as having the same gap.

This recommendation survives at P2. Scope-boundary's observation about spec 004 is well-taken — spec 004's entry (STATUS.md L51-56) also lacks a "Depends On" field, and the Cross-Spec Dependencies graph (L116) shows it has no dependencies. Both specs should be fixed together for consistency.

#### Recommendation 6: Add Location field to Structural Markers subsystem entry

- **Original position**: Add a Location field to the Structural Markers entry (STATUS.md L95-99) for consistency with the other two subsystem entries.
- **Disposition**: Modified
- **Explanation**:

Integration's cross-review (Tensions, "Shared subsystem entry consistency") acknowledged a factual error in integration's own review: integration had claimed all three entries share identical field structures, which is incorrect. Integration confirmed compliance's finding and stated the recommendation is "reasonable, though the broader issue is that no formal field schema was specified for subsystem entries, making 'inconsistency' a judgment call rather than a compliance failure."

Scope-boundary's cross-review (Tensions, "Structural Markers subsystem: Location field inconsistency") made a similar distinction: "Compliance's recommendation adds content to Phase 3 that was not specified in T008's task description. T008 (tasks.md L63) specifies the three entries and their content but does not mandate uniform fields across entries." Scope-boundary characterized this as an "editorial enhancement rather than a task requirement."

Both cross-reviews are correct that T008 does not mandate uniform fields. The inconsistency is real (integration conceded their factual error) but it is an improvement recommendation, not a compliance gap.

**Modified recommendation**: Add a Location field to the Structural Markers entry. Reclassify from "compliance gap" to "improvement recommendation." Priority remains P3. The edit is low-cost and strengthens SC-003's "zero ambiguity" standard for shared subsystems.

#### Recommendation 7: Normalize FR-008a reference in maintenance note

- **Original position**: Change "(FR-008a)" to "(FR-008)" in STATUS.md L138 because the sub-identifier is not in the spec's FR list.
- **Disposition**: Withdrawn
- **Explanation**:

Integration's cross-review (Dangerous Contradictions, "FR-008a identifier treatment") challenged this directly: tasks.md L63 uses "FR-008a" as a distinct identifier for the maintenance obligation sub-requirement. Normalizing to "(FR-008)" would break traceability between tasks.md and STATUS.md. Integration's suggested resolution was to keep "(FR-008a)" and add a traceability note: "FR-008a refers to the maintenance sub-requirement within FR-008 (spec.md L215)."

Integration is right. I had only checked traceability in one direction (STATUS.md to spec.md) and missed the tasks.md link. The identifier "FR-008a" appears in tasks.md T008 (L63), T017 (L101), and is the established convention for referring to the maintenance obligation sub-requirement. Changing it to "FR-008" would create the exact traceability problem I was trying to solve, just in the opposite direction. Keeping "FR-008a" and adding a brief traceability note (if desired) is the correct approach.

#### Recommendation 8: Add gap documentation convention note

- **Original position**: Add a convention note to the taxonomy section specifying that gap documentation uses FR identifiers as primary references.
- **Disposition**: Surviving
- **Explanation**:

No cross-review challenged this recommendation. It was not addressed by integration or scope-boundary in their cross-reviews of my work. In my own cross-reviews, I noted this recommendation is grounded in Phase 2 synthesis P3-1 (final.md L208), which recommended it as a low-cost addition to prevent Phase 3 ambiguity.

The recommendation survives at P3. It is a minor addition (one sentence) with low cost and clear traceability to the Phase 2 synthesis. Without it, Phase 4 contributors updating gap fields may use inconsistent formats (some FR-based, some scenario-based).

#### Recommendation 9: Verify spec 005 gap list completeness

- **Original position**: Verify that spec 005's gap list (FR-007, FR-011, FR-014, FR-015) is complete, since tasks.md shows additional remaining FRs that may not be represented.
- **Disposition**: Modified
- **Explanation**:

Scope-boundary's cross-review (Tensions, "Spec 005 gap list completeness") raised an important structural concern: adding STATUS.md-targeted FRs to the gap list risks creating a self-referential loop. Scope-boundary's analysis: "STATUS.md-targeted FRs (e.g., FR-008 sub-requirements, FR-009 label compliance) should be evaluated: if they describe a state that changes only when STATUS.md is edited, listing them as gaps in the STATUS.md entry creates a self-referential loop where the entry can never be complete." Integration's cross-review (Safe Agreements, "Spec 005 gap field accuracy concern") added a temporal concern: the risk-of-gap statement was written before Phase 3 work was done and not updated afterward.

Scope-boundary's circularity filter is a genuine insight I missed. The gap list should include unimplemented FRs, but only those whose implementation targets a file other than STATUS.md itself. The current four gaps (FR-007, FR-011, FR-014, FR-015) all target SKILL.md, which explains why they were selected — not incompleteness, but deliberate scoping to avoid self-reference.

**Modified recommendation**: Verify the gap list is complete for SKILL.md-targeted FRs specifically. If any SKILL.md-targeted FRs are missing, add them. Do not add STATUS.md-targeted FRs to the gap list, as this would create a circular dependency. Add a parenthetical note in the spec 005 entry clarifying the scoping: "(SKILL.md-targeted FRs only; STATUS.md-targeted FRs are tracked by the maintenance obligation at the bottom of this document)." Priority: P3 (unchanged).

---

### New Recommendations

- **Rewrite spec 005 risk-of-gap as cost-of-absence statement** (Priority: P2)
  - **Triggered by**: Integration's cross-review of compliance (Tensions, "Spec 005 risk-of-gap characterization") flagged the current risk-of-gap statement as "self-referential without actionable consequence" and noted the statement is factually stale — the clause "STATUS.md lacks complete cross-spec reference information" describes the pre-Phase-3 state, but Phase 3 has already added that information. My own cross-review of integration (Dangerous Contradictions, "Spec 005 risk-of-gap: tautology vs. forward reference") confirmed the finding and noted that integration's proposed replacement also has a staleness problem.
  - **Proposed change**: Rewrite the spec 005 risk-of-gap field to describe the cost of the remaining unimplemented work, not the full spec scope. Proposed text: "SKILL.md Phase 6 edge cases (heading match semantics, missing document handling, overwrite behavior) remain undocumented, and the dispute-parsing subsystem's cross-references from its consumers are incomplete, increasing the risk of divergent implementations." This scopes the risk statement to the remaining SKILL.md gaps (FR-007, FR-011, FR-014, FR-015) rather than repeating what STATUS.md already provides.
  - **Rationale**: The current text (STATUS.md L63) is factually outdated and does not follow the consequence-oriented pattern used by specs 001-004. SC-003 requires the document to enable prioritization decisions; a stale risk statement undermines that function.

- **Broaden maintenance note trigger scope** (Priority: P3)
  - **Triggered by**: Scope-boundary's review (which I read during cross-review, cited in my cross-review of scope-boundary, Tensions, "Scope of maintenance note") identified that the maintenance note (STATUS.md L138) only covers "implementation or acceptance status changes" but Phase 3 added living-content sections (Shared Subsystems, Structure Plan) not covered by the trigger. Integration's cross-review did not flag this. My original review flagged only the FR-008a identifier, not the trigger scope.
  - **Proposed change**: Broaden the maintenance note to: "This document MUST be updated when any spec's implementation or acceptance status changes, when shared subsystem stability or consumer lists change, or when the SKILL.md Structure Plan is affected by new implementation work (FR-008a)." This covers the three categories of living content in STATUS.md: per-spec status, shared subsystems, and the structure plan.
  - **Rationale**: The current trigger is too narrow for the document STATUS.md has become. Without broadening, an implementor who changes a subsystem's stability status or adds a new consumer has no documented obligation to update STATUS.md.

---

### Position Summary

Of my nine original recommendations, I withdrew one (Recommendation 7: FR-008a normalization), modified five (Recommendations 1, 2, 3, 4, 6, and 9 — six total), and maintained two (Recommendations 5 and 8). I added two new recommendations that the cross-review process surfaced (spec 005 risk-of-gap rewrite, maintenance note scope broadening).

The most significant change in my thinking was on the phase-attribution framing for Phase 2 residuals. Both scope-boundary and integration challenged my treatment of Phase 2 binding commitments as Phase 3 task obligations. Scope-boundary's argument — that taxonomy modifications are Phase 2 scope regardless of which phase discovers the gap — is formally correct. However, the pragmatic reality is that these fixes must happen before Phase 3's checkpoint can pass, because a "complete cross-spec reference" cannot contain undefined labels or undocumented label formats. The resolution I adopted throughout (attribute to Phase 2, frame as a prerequisite for Phase 3 passage) preserves scope integrity while preventing indefinite deferral. This is a genuine synthesis of the two positions, not a strategic compromise.

My highest-priority remaining recommendation is Recommendation 1 (Enrich Effort fields to four dimensions, as modified to use compact inline format). This should survive into the final synthesis because FR-017's text is unambiguous — the "covering" clause enumerates four required dimensions, the current Effort fields address only one (relative effort), and no cross-reviewer contested the FR-017 interpretation. Integration's scanability concern is valid and is addressed by the compact inline format modification, but it does not override the FR's literal requirements. Without this fix, STATUS.md's Effort fields are structurally present but substantively incomplete against FR-017, undermining SC-006(d)'s requirement that effort estimates be present.
