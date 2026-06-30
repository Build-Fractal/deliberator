# Phase 2 Gate — Neutral Synthesis

**Synthesizer**: neutral
**Date**: 2026-03-20
**Gate**: Phase 2 (Two-Tier Status Convention)
**Spec**: 005-p2p3-backlog-hardening
**Target**: `deliberator/specs/STATUS.md`

---

### Process Summary

- **Agents**: 3 — taxonomy-reviewer, consistency-checker, scope-boundary
- **Total artifacts**: 15 files produced across all phases
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 23 (taxonomy-reviewer: 8, consistency-checker: 8, scope-boundary: 7)
- **Recommendations withdrawn** (Phase 3): 1 (taxonomy-reviewer Rec 7: "Partially feature-complete" / "In progress" label)
- **Recommendations modified** (Phase 3): 12 (taxonomy-reviewer: 5; consistency-checker: 6; scope-boundary: 3)
- **Recommendations surviving** (Phase 3): 10 (taxonomy-reviewer: 2; consistency-checker: 2; scope-boundary: 4)
- **New recommendations added** (Phase 3): 3 (taxonomy-reviewer: 1 — apply "Not assessed" to spec 003; consistency-checker: 1 — reconcile US5 AS3 with FR-013; scope-boundary: 1 — normalize spec 004 compound label)
- **Disputes remaining** (Phase 4): 3 (compound labels, transition criteria placement, FR-023 characterization)
- **Convergence points** (Phase 4): 5 unanimous, 1 bilateral

---

### Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| 1 | taxonomy-reviewer | Add third acceptance-tier label | P1 | Modified (name: "Not started" -> "Not assessed"; definition shortened) | consistency-checker, scope-boundary (label name) | Unanimous | Accepted-Modified |
| 2 | taxonomy-reviewer | Add acceptance gaps to spec 004 | P1 | Surviving | scope-boundary (priority) | Unanimous | Accepted |
| 3 | taxonomy-reviewer | Reconcile US5 AS3 with FR-013 gap list | P2 | Modified (downgraded to P3; reclassified as spec errata) | scope-boundary (scope) | None | Accepted-Modified |
| 4 | taxonomy-reviewer | Add transition criteria to taxonomy | P2 | Modified (refiled to Phase 3) | scope-boundary (phase placement) | Bilateral (substance) | Disputed |
| 5 | taxonomy-reviewer | Document compound-label conventions | P2 | Modified (constrained to existing tier values) | consistency-checker (normalize vs. permit) | Bilateral (taxonomy-reviewer + consistency-checker) | Disputed |
| 6 | taxonomy-reviewer | Verify spec 002 "Spec-complete" label | P2 | Modified (downgraded to P3; limited to dependency check) | scope-boundary (phase scope) | None | Accepted-Modified |
| 7 | taxonomy-reviewer | Add "In progress" acceptance label | P3 | Withdrawn | consistency-checker, scope-boundary | N/A | Rejected |
| 8 | taxonomy-reviewer | Scope-check "Interpreting the Two Tiers" | P3 | Surviving | None | Unanimous | Accepted |
| 9 | consistency-checker | Add "not-assessed" to acceptance tier | P1 | Modified (definition broadened; scoping rule dropped) | taxonomy-reviewer, scope-boundary (label name) | Unanimous | Accepted-Modified |
| 10 | consistency-checker | Normalize spec 004 compound label | P1 | Modified (shifted to permit compound labels) | taxonomy-reviewer (normalize vs. permit) | Bilateral (consistency-checker + taxonomy-reviewer) | Disputed |
| 11 | consistency-checker | Add acceptance gaps for spec 004 | P2 | Modified (upgraded to P1; FR-based with scenario parenthetical) | taxonomy-reviewer (priority) | Unanimous | Accepted-Modified |
| 12 | consistency-checker | Clarify FR-023 gap characterization | P2 | Modified (concise with T013 pointer) | scope-boundary (phase scope) | None | Disputed |
| 13 | consistency-checker | Define transition criteria | P2 | Modified (adopted dual-condition formulation) | scope-boundary (phase placement) | Bilateral (substance) | Disputed |
| 14 | consistency-checker | Verify spec 002 "Spec-complete" against scenarios | P2 | Modified (lightweight dependency check; downgraded to P3) | scope-boundary (scope depth) | None | Accepted-Modified |
| 15 | consistency-checker | Guidance for Phase 3 labeling of spec 005 | P3 | Surviving | None | Unanimous | Accepted |
| 16 | consistency-checker | Document FR vs. acceptance-scenario relationship | P3 | Surviving | None | None | Accepted |
| 17 | scope-boundary | Add "Not started" to acceptance tier | P1 | Modified (name: "Not started" -> "Not assessed"; definition shortened) | consistency-checker (label name) | Unanimous | Accepted-Modified |
| 18 | scope-boundary | Document spec 004 acceptance gaps | P2 | Modified (upgraded to P1) | taxonomy-reviewer (priority) | Unanimous | Accepted-Modified |
| 19 | scope-boundary | Remove/justify "(e.g., ...)" examples | P3 | Modified (retain; "e.g.," prefix sufficient) | taxonomy-reviewer (useful grounding) | None | Accepted-Modified |
| 20 | scope-boundary | Add T007 exclusion note for spec 005 | P3 | Surviving | None | Unanimous | Accepted |
| 21 | scope-boundary | Verify Phase 2 checkpoint | P2 | Surviving | None | Unanimous (indirectly) | Accepted |
| 22 | scope-boundary | Confirm "Interpreting the Two Tiers" scope | P3 | Surviving | None | Unanimous | Accepted |
| 23 | scope-boundary | Confirm no SKILL.md changes in Phase 2 | P1 | Surviving | None | Unanimous | Accepted |
| N1 | taxonomy-reviewer | Apply "Not assessed" to spec 003 entry | P1 | New (Phase 3) | None | Unanimous | Accepted |
| N2 | consistency-checker | Reconcile spec.md US5 AS3 with FR-013 | P2 | New (Phase 3) | None | None | Accepted |
| N3 | scope-boundary | Normalize spec 004 compound implementation label | P1 | New (Phase 3) | taxonomy-reviewer, consistency-checker | None | Disputed |

---

### Dangerous Contradictions Found

**Resolved Contradictions**

1. **Acceptance-tier label name: "Not started" vs. "not-assessed"**
   - **Contradiction**: taxonomy-reviewer and scope-boundary proposed reusing "Not started" from the implementation tier. consistency-checker proposed "not-assessed" as a semantically distinct label. Using the same name across orthogonal tiers creates parsing ambiguity; introducing a new name breaks from existing STATUS.md usage.
   - **Resolution**: Both taxonomy-reviewer and scope-boundary conceded during Phase 3 revision. taxonomy-reviewer cited "parsing ambiguity" as the decisive factor (revision, Rec 1). scope-boundary acknowledged the orthogonality violation as "a genuine blind spot" (revision, Position Summary). All three agents converged on "Not assessed."

2. **Acceptance-tier label definition: one-sentence vs. two-sentence**
   - **Contradiction**: consistency-checker proposed a two-clause definition covering both "no implementation exists to evaluate" and "implementation exists but acceptance criteria have not been formally verified." taxonomy-reviewer and scope-boundary proposed a single sentence: "No acceptance criteria have been evaluated," arguing the second clause couples the acceptance tier to implementation state.
   - **Resolution**: Partially resolved. taxonomy-reviewer and scope-boundary converged on the single-sentence definition. consistency-checker did not fully concede but indicated flexibility (disputes, Flexibility item 2), accepting the short definition if a usage note clarifies that the label applies regardless of implementation state. The definition text is settled; the usage-note question is a minor residual.

3. **Priority of spec 004 acceptance gap documentation: P1 vs. P2**
   - **Contradiction**: taxonomy-reviewer assigned P1; scope-boundary and consistency-checker originally assigned P2. P1 implies the gate cannot pass without the fix; P2 implies it can.
   - **Resolution**: scope-boundary and consistency-checker both conceded P1 in their Phase 3 revisions. scope-boundary cited taxonomy-reviewer's argument about the Phase 2 checkpoint requiring uniform application (scope-boundary revision, Rec 2). consistency-checker cited the same checkpoint language (consistency-checker revision, Rec 3). Unanimous P1.

4. **Parenthetical examples in Feature-complete definition: embellishment vs. useful grounding**
   - **Contradiction**: scope-boundary flagged the "(e.g., ...)" examples in STATUS.md L19 as an embellishment beyond FR-012. taxonomy-reviewer affirmed them as useful and non-distorting.
   - **Resolution**: scope-boundary conceded in Phase 3 revision, accepting that the existing "e.g.," prefix is the standard marker for non-exhaustive illustration and is sufficient (scope-boundary revision, Rec 3). No change to STATUS.md needed.

5. **Spec 002 "Spec-complete" label validity**
   - **Contradiction**: scope-boundary accepted the label at face value. taxonomy-reviewer and consistency-checker questioned whether the label is justified given the spec 001 parsing dependency and T019's upcoming changes.
   - **Resolution**: taxonomy-reviewer conceded the phase-boundary argument (revision, Rec 6), accepting that Phase 2 assesses current-state accuracy and T019-related risk is a Phase 4 concern. consistency-checker downgraded to P3 and accepted a lightweight dependency check rather than full scenario verification. The label stands for Phase 2; a Phase 4 post-condition check is recorded.

**Unresolved Contradictions**

1. **Compound implementation labels: permit vs. normalize** (see Remaining Disputes, Dispute 1)

2. **Transition criteria phase placement: Phase 2 vs. Phase 3** (see Remaining Disputes, Dispute 2)

3. **FR-023 gap characterization: Phase 2 revision vs. Phase 4 deferral** (see Remaining Disputes, Dispute 3)

---

### Systemic Contradictions

1. **Taxonomy completeness vs. Phase 2 scope minimalism**
   - **Manifests in**: Transition criteria placement dispute (taxonomy-reviewer/consistency-checker want Phase 2; scope-boundary wants Phase 3). Compound label permission dispute (taxonomy-reviewer/consistency-checker want to extend taxonomy; scope-boundary wants to normalize entries). "In progress" label proposal (taxonomy-reviewer Rec 7, withdrawn). FR-023 enrichment dispute.
   - **Root cause**: Phase 2's checkpoint claims the taxonomy is "authoritative" (tasks.md L47), but the task descriptions (T006, T007) are narrowly scoped to adding the acceptance convention and applying labels. "Authoritative" can mean either "defines everything used" (scope-boundary's reading) or "defines everything needed for unambiguous future use" (taxonomy-reviewer and consistency-checker's reading). The two interpretations pull Phase 2 in opposite directions.
   - **Implication for spec**: The spec should clarify what "authoritative" means in the Phase 2 checkpoint. If it means "all labels in use are defined and consistently applied," the checkpoint is satisfiable with minimal additions (third acceptance label, spec 004 gaps). If it means "the taxonomy is complete enough that Phase 3 can apply labels without ambiguity," it requires transition criteria and compound-label conventions. The deliberation surfaced this ambiguity but did not resolve it.

2. **Controlled vocabulary purity vs. information density at the label level**
   - **Manifests in**: Compound implementation label dispute (scope-boundary wants three-value strict vocabulary; taxonomy-reviewer and consistency-checker want structured composition). spec 004's current label format. Future spec 005 labeling in T012a.
   - **Root cause**: The implementation tier was designed with three values for a four-spec system where all specs had uniform structure. Spec 004's two independent subsystems (core engine vs. discovery CLI) broke this assumption. The taxonomy has no mechanism for representing within-spec variance without either losing information (normalize to "Partially-complete") or extending the vocabulary format (compound labels).
   - **Implication for spec**: STATUS.md should decide whether labels are a quick-reference index (favoring compound labels for density) or a controlled vocabulary for programmatic/process use (favoring normalization). If the former, compound labels need formal rules. If the latter, the notes field must reliably carry the subsystem detail that labels omit.

3. **FR-based gap references vs. acceptance-scenario-based gap references**
   - **Manifests in**: Spec 004 gap content dispute (scope-boundary/taxonomy-reviewer prefer FR-based; consistency-checker originally preferred acceptance-scenario-based). consistency-checker Rec 16 (document FR-vs-scenario relationship). FR-023 characterization dispute (what level of detail in gap descriptions).
   - **Root cause**: The acceptance tier measures "acceptance criteria" but gap documentation uses FR identifiers (per FR-013 and spec 001's precedent). FRs and acceptance scenarios are different constructs that do not always map one-to-one. The taxonomy does not specify which construct gap documentation should reference.
   - **Implication for spec**: Add a brief convention note specifying that gap documentation uses FR identifiers as primary references (consistent with FR-013's precedent) with optional acceptance-scenario annotations for traceability. This prevents Phase 3 contributors from making ad-hoc choices.

4. **Current-state accuracy vs. forward-facing completeness**
   - **Manifests in**: Spec 002 "Spec-complete" verification depth. FR-023 enrichment with Phase 4 cross-references. Transition criteria as a Phase 3 safeguard. taxonomy-reviewer Rec 7 (anticipating spec 005's future label needs).
   - **Root cause**: Phase 2 produces a snapshot (STATUS.md) that subsequent phases depend on. The taxonomy-reviewer and consistency-checker instinctively tried to future-proof the snapshot; the scope-boundary correctly pointed out that future-proofing imports later-phase concerns into the current phase. The tension is structural: any status-tracking system invites forward-looking analysis, but phased delivery requires strict temporal boundaries.
   - **Implication for spec**: Establish a principle that each phase produces a deliverable accurate as of its completion date. Forward-facing risks are recorded as post-conditions for the relevant future phase, not as corrections to the current phase's deliverable. This principle was implicitly applied by the scope-boundary agent and accepted by taxonomy-reviewer during revision, but it is not codified.

---

### Convergence Achieved

1. **Add "Not assessed" as third acceptance-tier label** — Strength: Unanimous
   - **Agreed recommendation**: Add to STATUS.md's Acceptance Tier section: `- **Not assessed**: No acceptance criteria have been evaluated.` Apply this label to spec 003's acceptance tier (replacing "Not started" at STATUS.md L41). Drop any causal sentence linking to implementation state.
   - **Supporting agents**: taxonomy-reviewer (revision, Rec 1), consistency-checker (revision, Rec 1), scope-boundary (revision, Rec 1). Confirmed in all three dispute documents (convergence sections).
   - **Evidence basis**: FR-012 (spec.md L225) defines two acceptance labels; STATUS.md L41 uses a third ("Not started") that is not in the taxonomy. FR-009 (spec.md L216) requires labels to use the defined convention. Using an undefined label violates FR-009 and falsifies the Phase 2 checkpoint claim that the taxonomy is "authoritative" (tasks.md L47).
   - **Pre-existing or earned**: Earned. All three agents identified the missing third label in Phase 1, but the label *name* was disputed. consistency-checker proposed "not-assessed"; taxonomy-reviewer and scope-boundary proposed "Not started." Convergence on "Not assessed" was earned through cross-review, with consistency-checker's semantic argument (acceptance tier measures evaluation state, not implementation state) proving decisive.

2. **Add explicit acceptance gaps to spec 004 at P1** — Strength: Unanimous
   - **Agreed recommendation**: Add a `**Gaps**:` line to spec 004's STATUS.md entry: `**Gaps**: FR-022 (preset list command), FR-023 (preset filter command), FR-024 (preset detail command) — discovery features not started; acceptance scenarios US-3 through US-6 not testable.` Use FR-based identifiers as primary references consistent with spec 001's format.
   - **Supporting agents**: taxonomy-reviewer (revision, Rec 2), consistency-checker (revision, Rec 3), scope-boundary (revision, Rec 2). All upgraded to P1.
   - **Evidence basis**: STATUS.md L19 defines "Feature-complete" as having "acceptance criteria gaps remain." Spec 001 (STATUS.md L32) enumerates its gaps. Spec 004 (STATUS.md L46-48) uses the same label without enumeration. The Phase 2 checkpoint (tasks.md L47) requires the convention to be "applied to all 4 specs."
   - **Pre-existing or earned**: Earned on priority. All three agents identified the need in Phase 1, but scope-boundary and consistency-checker originally assigned P2. taxonomy-reviewer's argument about the checkpoint requiring uniform application earned the P1 upgrade during revision.

3. **"Interpreting the Two Tiers" paragraph is correctly scoped** — Strength: Unanimous
   - **Agreed recommendation**: Retain STATUS.md L22-24 as-is. The dependency sentence is a natural part of explaining orthogonality. No modification in Phase 2. Resist future expansion; any additions belong in a separate document or Phase 3.
   - **Supporting agents**: taxonomy-reviewer (revision, Rec 8), scope-boundary (revision, Rec 6), consistency-checker (implicitly, no challenge in any phase).
   - **Evidence basis**: scope-boundary confirmed the section is "minimal and necessary" (revision, Rec 6). taxonomy-reviewer confirmed it "prevents the labeling disagreements the convention was designed to resolve" (Phase 1 review, Alignment). consistency-checker found no consistency issues.
   - **Pre-existing or earned**: Pre-existing. All three agents agreed from Phase 1. No position shifted.

4. **No SKILL.md modifications in Phase 2** — Strength: Unanimous
   - **Agreed recommendation**: Verify that SKILL.md has not been modified since Phase 1. Phase 4's SKILL.md work (T013-T015, T019) starts from the Phase 1-verified baseline. Phase boundaries are intact.
   - **Supporting agents**: scope-boundary (revision, Rec 7, P1), taxonomy-reviewer (cross-review Safe Agreements), consistency-checker (cross-review Safe Agreements).
   - **Evidence basis**: Phase 2 tasks (T006, T007) target only STATUS.md. SKILL.md modifications are explicitly scoped to Phase 4 (tasks.md L74-93).
   - **Pre-existing or earned**: Pre-existing. Agreed from Phase 1.

5. **Spec 005 self-tracking: annotate T007 and T012a** — Strength: Unanimous
   - **Agreed recommendation**: (a) Append "(Spec 005 entry deferred to T012a, Phase 3)" to T007's description. (b) Add labeling guidance to T012a: "Label spec 005 implementation status based on FRs completed at time of writing. If major capabilities are still pending and the gap list is unstable, label acceptance as 'Not assessed.' If all major capabilities are present with enumerable gaps, label as 'Feature-complete' with gaps listed. Update both labels in Phase 5 (T016/T017)."
   - **Supporting agents**: scope-boundary (revision, Rec 4), consistency-checker (revision, Rec 7), taxonomy-reviewer (revision, Rec 7 withdrawal endorses three-label sufficiency for spec 005).
   - **Evidence basis**: SC-003 (spec.md L265) requires spec status in STATUS.md. T007 covers specs 001-004 but does not mention spec 005. T012a (tasks.md L68) handles spec 005 in Phase 3 but lacks labeling instructions.
   - **Pre-existing or earned**: Earned. scope-boundary proposed the T007 annotation; consistency-checker proposed the T012a guidance. Cross-review identified them as complementary. taxonomy-reviewer's withdrawal of Rec 7 confirmed the three-label system suffices.

6. **Dual-condition transition criteria formulation** — Strength: Bilateral (taxonomy-reviewer + consistency-checker)
   - **Agreed recommendation**: When transition criteria are added, they must state: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." The dual-condition prevents the inconsistent state of "Spec-complete with documented gaps."
   - **Supporting agents**: taxonomy-reviewer (revision, Rec 4), consistency-checker (revision, Rec 5). scope-boundary did not take a position on formulation but did not dispute the substance.
   - **Evidence basis**: consistency-checker's original single-condition formulation (scenarios only) would allow a spec to be relabeled "Spec-complete" while its Gaps field still listed items. taxonomy-reviewer identified this flaw in cross-review. consistency-checker conceded and adopted the dual-condition version.
   - **Pre-existing or earned**: Earned. consistency-checker modified their original formulation after taxonomy-reviewer's cross-review challenge.

<!-- DELIBERATOR:DISPUTES_BEGIN -->
### Remaining Disputes

- **Dispute: Compound implementation labels — permit vs. normalize**
  - **Positions**: taxonomy-reviewer and consistency-checker advocate permitting compound labels in the Implementation Tier section, constrained to use only existing tier values as components (e.g., "Implementation-complete (core) / Not started (discovery)"). scope-boundary advocates normalizing spec 004 to "Partially-complete" and moving subsystem detail into the notes field, preserving the strict three-value controlled vocabulary. Cite: taxonomy-reviewer disputes Rec 5; consistency-checker disputes Rec 2; scope-boundary disputes, first item.
  - **Arguments**: taxonomy-reviewer and consistency-checker argue that "Partially-complete" loses operationally critical information at the label level — an implementor building on spec 004's core engine needs to see at a glance that core is complete and discovery is not, without reading the notes field. They argue compound labels use only defined vocabulary at the component level and therefore do not violate the controlled vocabulary. scope-boundary argues that compound labels are a formatting extension the taxonomy does not define, that FR-012 says nothing about extending the implementation tier's format, and that introducing compound-label rules in Phase 2 is taxonomy enrichment beyond T006/T007's scope.
  - **Synthesizer assessment**: The evidence favors permitting compound labels. First, the bilateral agreement (taxonomy-reviewer + consistency-checker) is substantively stronger than scope-boundary's position because it addresses the operational concern: STATUS.md exists to enable quick status assessment (STATUS.md L5), and "Partially-complete" without glanceable subsystem detail degrades this function. Second, the compound label format uses only defined tier values — "Implementation-complete" and "Not started" are both in the taxonomy at L11 and L13 — so the controlled vocabulary is preserved at the component level. Third, scope-boundary's own flexibility statement (disputes, Flexibility item 1) accepts compound labels if constrained to existing tier values and limited to a single-sentence rule. The conditions for scope-boundary's acceptance are met by the taxonomy-reviewer/consistency-checker proposal. Fourth, Phase 3's T012a will need to label spec 005, which may also have subsystem variance; establishing the convention now prevents ad-hoc formatting in T012a.
  - **Recommended resolution**: Adopt compound labels with the constraining rule. Add to the Implementation Tier section of STATUS.md: "Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label." Retain spec 004's current label format, which already complies with this rule.

- **Dispute: Transition criteria placement — Phase 2 taxonomy section vs. Phase 3 maintenance note**
  - **Positions**: consistency-checker advocates adding the dual-condition transition criteria to the Phase 2 taxonomy section as a definitional companion to the label definitions. taxonomy-reviewer (after revision) and scope-boundary advocate deferring to Phase 3, placing the criteria alongside T008's maintenance obligation (FR-008). Cite: consistency-checker disputes, second item; taxonomy-reviewer disputes, second item; scope-boundary disputes, second item.
  - **Arguments**: consistency-checker argues transition criteria are the "completion condition for a label definition" — without them, the boundary between "Feature-complete" and "Spec-complete" is implicit and derivable only by inference. consistency-checker cites scope-boundary's cross-review concession that a one-sentence rule is "defensibly part of defining those labels." taxonomy-reviewer and scope-boundary argue that transition criteria are operational rules about when labels change (temporal predicates), not static definitions of what labels mean, and that tasks.md L44-45 (T006, T007) do not include transition rules in Phase 2's scope. taxonomy-reviewer notes that T008 has not yet been implemented, so placing criteria in Phase 3 costs nothing.
  - **Synthesizer assessment**: The evidence slightly favors Phase 3 placement. The decisive factor is that taxonomy-reviewer — the agent whose mandate most naturally covers definitional completeness — explicitly accepted the scope-boundary argument and refiled transition criteria to Phase 3 during revision. This creates a 2-1 split (taxonomy-reviewer + scope-boundary for Phase 3; consistency-checker for Phase 2). The substance is unanimously agreed (the dual-condition formulation); only the placement is disputed. Since T006 and T007 are already marked complete in tasks.md L44-45, adding transition criteria in Phase 2 requires reopening completed tasks. Phase 3's T008 is the natural home because it operationalizes FR-008's maintenance obligation, which governs exactly when labels change. However, consistency-checker's argument has merit: if Phase 3 is delayed, the taxonomy exists without transition criteria during the gap. This risk is low given that Phase 3 immediately follows Phase 2.
  - **Recommended resolution**: Defer transition criteria to Phase 3 as an explicit T008 input. Record the agreed dual-condition formulation: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." Phase 3's T008 implementation must include this formulation. The synthesis records this as a binding commitment, not an optional suggestion.

- **Dispute: FR-023 gap characterization — Phase 2 revision vs. Phase 4 deferral**
  - **Positions**: consistency-checker advocates revising STATUS.md L32's FR-023 parenthetical now to add "heading match semantics and template-level instructions pending; see T013" (consistency-checker revision, Rec 4, P2). taxonomy-reviewer and scope-boundary advocate leaving STATUS.md L32 as-is for Phase 2, deferring the enrichment to Phase 4 when T013 implements FR-007 (taxonomy-reviewer revision, Rec 3; scope-boundary disputes, third item).
  - **Arguments**: consistency-checker argues the current parenthetical is imprecise — it mentions template instructions but omits heading match semantics (spec 005 FR-007), and "if Phase 2 wrote the text, Phase 2 should fix it." taxonomy-reviewer and scope-boundary argue that STATUS.md L32 accurately implements FR-013 (spec.md L226), which does not mention heading match semantics or T013. Enriching the text with Phase 4 cross-references imports future-phase awareness into Phase 2's deliverable and creates a maintenance burden if T013's scope changes.
  - **Synthesizer assessment**: The evidence favors deferral. STATUS.md L32 is a near-verbatim implementation of FR-013. The text is not wrong — it is scoped to what FR-013 specifies. Adding "heading match semantics" and "see T013" introduces a forward reference to Phase 4 work that does not yet exist. This is enrichment, not correction. consistency-checker's principle ("if Phase 2 wrote the text, Phase 2 should fix it") is reasonable in general but does not apply when the text accurately implements its source requirement. However, consistency-checker's observation that the FR-023 characterization omits the heading-match-semantics dependency is factually correct and should be recorded for Phase 4.
  - **Recommended resolution**: Leave STATUS.md L32 as-is for Phase 2. Record as a Phase 4 post-condition: "After T013 implements FR-007 heading match semantics, update the FR-023 gap characterization in STATUS.md to reflect the complete picture (validation check + heading match semantics + template instructions)." This preserves the observation without importing Phase 4 content into Phase 2.
<!-- DELIBERATOR:DISPUTES_END -->

---

### Actionable Spec Changes

**P1 — Must implement** (blocking issues or unanimous convergence):

1. **Add "Not assessed" to the acceptance tier taxonomy**: Add to STATUS.md's Acceptance Tier section (after L20): `- **Not assessed**: No acceptance criteria have been evaluated.` Source: Convergence point 1 (unanimous); Recommendations #1/#9/#17. This is the single most consequential finding — without it, the Phase 2 checkpoint claim that "STATUS.md taxonomy is authoritative" (tasks.md L47) is false.

2. **Apply "Not assessed" label to spec 003**: Update STATUS.md L41 from `**Acceptance**: Not started` to `**Acceptance**: Not assessed`. Source: taxonomy-reviewer new Recommendation N1 (unanimous convergence).

3. **Add acceptance gap documentation to spec 004**: Add a `**Gaps**:` line to spec 004's STATUS.md entry: `**Gaps**: FR-022 (preset list command), FR-023 (preset filter command), FR-024 (preset detail command) — discovery features not started; acceptance scenarios US-3 through US-6 not testable.` Source: Convergence point 2 (unanimous); Recommendations #2/#11/#18.

4. **Add compound-label permission rule to Implementation Tier section**: Add to STATUS.md's Implementation Tier section (after L13): "Specs with independently-implementable subsystems may use compound labels composed of existing tier values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label." Source: Dispute resolution (Dispute 1); Recommendations #5/#10. Bilateral agreement with scope-boundary flexibility conditions met.

5. **Verify no SKILL.md modifications in Phase 2**: Confirm via file inspection that SKILL.md has not been modified since Phase 1. Source: Convergence point 4 (unanimous); Recommendation #23.

**P2 — Should implement** (majority convergence or strong single-agent case):

1. **Annotate T007 with spec 005 exclusion note**: Append to T007's description in tasks.md: "(Spec 005 entry deferred to T012a, Phase 3)." Source: Convergence point 5 (unanimous); Recommendation #20.

2. **Add labeling guidance to T012a**: Add to T012a in tasks.md: "Label spec 005 implementation status based on FRs completed at time of writing. If major capabilities are still pending and the gap list is unstable, label acceptance as 'Not assessed.' If all major capabilities are present with enumerable gaps, label as 'Feature-complete' with gaps listed. Update both labels in Phase 5 (T016/T017)." Source: Convergence point 5 (unanimous); Recommendations #15/#20.

3. **Record dual-condition transition criteria as Phase 3 T008 input**: Record in the Phase 2 gate summary (this document) that T008 must add transition criteria to the taxonomy section: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." Source: Convergence point 6 (bilateral); Dispute resolution (Dispute 2); Recommendations #4/#13.

4. **Verify Phase 2 checkpoint against FR-012 and FR-009**: After implementing P1 changes above, verify that (a) every acceptance label used in STATUS.md is defined in the taxonomy section, and (b) every spec entry has both an implementation-tier and acceptance-tier label. Source: Recommendation #21.

**P3 — Consider implementing** (bilateral agreement or strong but disputed):

1. **Add gap documentation convention note**: Add a one-sentence note to the taxonomy section: "Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability." Source: Recommendation #16. Note: No cross-review challenged this; low-cost addition that prevents Phase 3 ambiguity about gap documentation format.

2. **Reconcile spec.md US5 AS3 with FR-013 gap list**: Either align US5 AS3 to list all three gaps (FR-023, FR-025, FR-026) consistently with FR-013, or add a parenthetical to US5 AS3 explaining FR-023's partial-gap status. Source: Recommendations #3/N2. Note: This is a spec.md edit, not a STATUS.md edit — it is a documentation errata, not a Phase 2 gate item.

3. **Record FR-023 Phase 4 post-condition**: Record that after T013 implements FR-007, the FR-023 gap characterization in STATUS.md L32 should be updated to include heading match semantics. Source: Dispute resolution (Dispute 3); Recommendations #3/#12. Note: STATUS.md L32 is left as-is for Phase 2; the observation is preserved for Phase 4 action.

4. **Record spec 002 Phase 4 re-evaluation**: Record that after T019 modifies dispute-parsing cross-references, spec 002's "Spec-complete" label should be re-evaluated against its acceptance scenarios. Source: Recommendations #6/#14. Note: The label is accurate for Phase 2's current-state assessment; this is a forward-facing risk note.

5. **Confirm "Interpreting the Two Tiers" section is at maximum appropriate length**: Mark this section as reviewed and approved. Any future expansion should be resisted; additions belong in a separate document or Phase 3 enrichment. Source: Convergence point 3 (unanimous); Recommendations #8/#22.

---

### Key Concessions

**taxonomy-reviewer**:
- Conceded label name "Not started" in favor of "Not assessed" after consistency-checker argued that reusing the implementation tier's label undermines orthogonality (revision, Rec 1). This was the most significant concession: taxonomy-reviewer acknowledged that "parsing ambiguity is the decisive factor."
- Conceded Phase 2 placement of transition criteria, accepting scope-boundary's argument that they are operational rules belonging in Phase 3 (revision, Rec 4). Stated this was the most significant change in thinking: "I had conflated 'the taxonomy should be complete' with 'the taxonomy should handle everything Phase 3 and Phase 4 will need.'"
- Conceded Phase 2 scope for spec 002 verification and FR-023 reconciliation, accepting scope-boundary's phase-boundary arguments (revision, Recs 3 and 6).
- Withdrew Recommendation 7 (fourth acceptance label "In progress") after consistency-checker and scope-boundary showed the three-label system is sufficient (revision, Rec 7).

**consistency-checker**:
- Conceded the alternative scoping rule ("acceptance labels only apply when implementation > 0") per scope-boundary's argument that it adds unnecessary complexity for T012a (revision, Rec 1).
- Conceded preference for normalizing compound labels to "Partially-complete" (option a), accepting taxonomy-reviewer's argument that compound labels composed of existing tier values preserve information without violating the controlled vocabulary (revision, Rec 2).
- Conceded original P2 priority for spec 004 gap documentation, upgrading to P1 per taxonomy-reviewer's checkpoint argument (revision, Rec 3).
- Conceded single-condition transition criteria formulation, adopting taxonomy-reviewer's dual-condition version after accepting the "Spec-complete with documented gaps" flaw (revision, Rec 5).
- Conceded P2 priority for spec 002 verification, downgrading to P3 and accepting a lightweight dependency check (revision, Rec 6).

**scope-boundary**:
- Conceded label name "Not started" in favor of "Not assessed," acknowledging the orthogonality violation as "a genuine blind spot" (revision, Position Summary).
- Conceded P2 priority for spec 004 gap documentation, upgrading to P1 per taxonomy-reviewer's checkpoint argument (revision, Rec 2).
- Conceded the parenthetical examples concern, accepting that the "e.g.," prefix is sufficient (revision, Rec 3).
- Added a new recommendation (normalize spec 004 compound label) after consistency-checker identified a controlled-vocabulary violation scope-boundary had missed (revision, New Recommendations). This was an acknowledgment of a blind spot rather than a concession on an existing position.
- Did not concede on compound label normalization, transition criteria placement, or FR-023 deferral — maintaining these positions through Phase 4 disputes while indicating flexibility on conditions.
