# Scope-Boundary Revision — Phase 2 Gate (Spec 005)

**Reviewer**: scope-boundary
**Revision iteration**: 1
**Date**: 2026-03-20
**Gate**: Phase 2 (Two-Tier Status Convention)

---

### Recommendation Dispositions

#### Recommendation 1: Add "Not started" to acceptance tier taxonomy

- **Original position**: Add "Not started" to the acceptance tier taxonomy with definition "No acceptance criteria have been evaluated. The spec's features are not yet implemented."
- **Disposition**: Modified
- **Explanation**:
  - consistency-checker's cross-review (Dangerous Contradictions, "Label name for the missing acceptance-tier value") argued that reusing "Not started" from the implementation tier "breaks mutual exclusivity" between tiers and creates cross-tier terminological overlap in the very taxonomy designed to be orthogonal. consistency-checker proposed "not-assessed" as a distinct label. My own cross-review of consistency-checker (Dangerous Contradictions, "Acceptance tier label for unimplemented specs") acknowledged this was a legitimate concern and agreed that "Not assessed" is more precise because it avoids confusion with the implementation tier's identical label.
  - taxonomy-reviewer's cross-review (Safe Agreements, first bullet) confirmed the underlying problem is real and agreed it is a blocking P1 item, but did not weigh in on the label name dispute.
  - **Modified recommendation**: Add a third acceptance-tier label named **"Not assessed"** (not "Not started") with the definition: "No acceptance criteria have been evaluated." Drop the second sentence entirely — the orthogonality section (STATUS.md L22-24) already establishes that the tiers are independent, and including a causal explanation ("The spec's features are not yet implemented") reintroduces coupling between tiers. Apply this label to spec 003's acceptance tier (STATUS.md L41). This modification preserves the core value (the taxonomy must define every label it uses) while eliminating the cross-tier terminological overlap that consistency-checker correctly identified.

#### Recommendation 2: Document spec 004 acceptance gaps

- **Original position**: Add a `**Gaps**:` line to spec 004's entry identifying FR-022-024 (discovery commands) as the acceptance criteria gap.
- **Disposition**: Modified
- **Explanation**:
  - taxonomy-reviewer's cross-review (Safe Agreements, "Spec 004 needs explicit acceptance gap documentation") agreed on the need but assigned P1 priority where I assigned P2. My own cross-review of taxonomy-reviewer (Dangerous Contradictions, "Priority divergence on spec 004 gap documentation") conceded that scope-boundary should yield to P1: "the taxonomy definition of 'Feature-complete' explicitly states 'acceptance criteria gaps remain,' and spec 001 sets an enumerated-gaps precedent at STATUS.md L32. Spec 004 using the same label without enumerated gaps is an internal inconsistency within the very file Phase 2 produces."
  - consistency-checker's cross-review (Dangerous Contradictions, "Scope of gap documentation obligation") raised a deeper question: should gaps be documented as FRs or as acceptance scenarios? consistency-checker argued that referencing US-3 through US-6 acceptance scenarios is more appropriate for the acceptance tier, while FR-based gaps are implementation-tier language. My own cross-review of consistency-checker (Tensions, "Priority assignment for spec 004 acceptance gap documentation") noted this ambiguity and acknowledged that consistency-checker's Recommendation #8 (document the relationship between FRs and acceptance scenarios) would resolve it.
  - **Modified recommendation**: Upgrade to **P1**. Add a `**Gaps**:` line to spec 004's entry identifying **FR-022-024 (discovery commands — `/conversus presets` list, filter, detail)** as the acceptance criteria gap preventing "Spec-complete" status. Use FR-based gap references for consistency with spec 001's existing documentation (STATUS.md L32), which was established by FR-013 (`spec.md` L226). The question of whether to adopt acceptance-scenario-based gap references is a convention decision that, if taken, should be applied uniformly across all specs — that uniformity work belongs in Phase 3, not as a mid-stream convention change in Phase 2.

#### Recommendation 3: Remove or justify "(e.g., ...)" examples in Feature-complete definition

- **Original position**: Either remove the parenthetical examples from STATUS.md L19 or add a marker that they are illustrative, not exhaustive.
- **Disposition**: Modified
- **Explanation**:
  - taxonomy-reviewer's cross-review (Dangerous Contradictions, "Parenthetical examples in Feature-complete definition") identified this as a direct contradiction between my position (embellishment) and taxonomy-reviewer's position (useful grounding). The cross-review proposed a compromise: retain the examples but rephrase to make them clearly illustrative — "change to something like '(examples: missing template instructions, incomplete edge case documentation — not exhaustive).'" taxonomy-reviewer's cross-review noted that scope-boundary already offers this compromise in the original Recommendation #3.
  - consistency-checker's cross-review (Tensions, "Strictness of 'match the spec exactly' vs. helpful elaboration") noted that consistency-checker did not flag this issue at all and that scope-boundary's P3 priority correctly reflects low impact. The suggested coordination was to address it at zero marginal cost if the taxonomy section is edited for other reasons.
  - **Modified recommendation**: Retain the examples. The existing "e.g.," prefix is the standard English marker for non-exhaustive illustration and is sufficient. Since the taxonomy section will be edited for other reasons (adding the "Not assessed" label per Recommendation 1), a reviewer can confirm that "e.g.," is unambiguous during that edit. No separate action item is needed. This modification reflects that my original concern, while technically valid under a strict "match the spec exactly" reading, does not rise to the level of a standalone recommendation. The "e.g.," prefix already does the job.

#### Recommendation 4: Add explicit T007 exclusion note for spec 005

- **Original position**: Append "(Spec 005 entry deferred to T012a, Phase 3)" to T007's description in tasks.md.
- **Disposition**: Surviving
- **Explanation**:
  - consistency-checker's cross-review (Tensions, "Spec 005 self-tracking: boundary clarity vs. forward guidance") endorsed this recommendation as complementary to consistency-checker's own recommendation to add labeling instructions to T012a itself. The cross-review suggested adopting both: "annotate T007 with the deferral note (scope-boundary's recommendation) AND annotate T012a with labeling instructions (consistency-checker's recommendation). This closes the gap from both ends."
  - taxonomy-reviewer's cross-review (Safe Agreements, "Spec 005 omission from STATUS.md is by-design for Phase 2") agreed the omission is by-design and noted scope-boundary's recommendation as a "valid process concern."
  - No one challenged this recommendation. It remains a P3 documentation hygiene improvement. The value is small but the cost is near zero: one parenthetical appended to a task description. It makes the Phase 2/Phase 3 handoff for spec 005 explicit rather than implicit.

#### Recommendation 5: Verify Phase 2 checkpoint against FR-012 and FR-009 satisfaction

- **Original position**: Verify that every acceptance label used in STATUS.md is defined in the taxonomy, and every spec entry has both tier labels.
- **Disposition**: Surviving
- **Explanation**:
  - No cross-review directly challenged this recommendation. It is a meta-recommendation — it asks for verification that the taxonomy is internally consistent, which is the precondition for calling the taxonomy "authoritative" (tasks.md L47).
  - The cross-reviews from both taxonomy-reviewer and consistency-checker reinforced this recommendation indirectly. Both identified the same root inconsistency (undefined "Not started" acceptance label) that this verification would catch. taxonomy-reviewer's cross-review (Safe Agreements, first bullet) stated: "The taxonomy cannot be called 'authoritative' (Phase 2 checkpoint language, tasks.md L47) while using an undefined label." consistency-checker's cross-review (Safe Agreements, first bullet) called it "the single most consequential definitional gap."
  - This recommendation survives because it is the procedural check that ensures Recommendations 1 and 2 are not optional — they are preconditions for the Phase 2 checkpoint to be truthful. Priority remains P2.

#### Recommendation 6: Confirm "Interpreting the Two Tiers" section does not exceed minimum-necessary scope

- **Original position**: No change needed. The section is minimal and necessary. Flag if any future expansion is proposed.
- **Disposition**: Surviving
- **Explanation**:
  - taxonomy-reviewer's cross-review (Safe Agreements, "The 'Interpreting the Two Tiers' paragraph is at the right level of detail") agreed the section should remain as-is. taxonomy-reviewer's own Recommendation #8 proactively defended the dependency sentence.
  - consistency-checker's cross-review (Safe Agreements, "The 'Interpreting the Two Tiers' section is appropriately scoped") also agreed, noting that both reviews evaluated it from different lenses (scope minimality vs. interpretive completeness) and both approved.
  - No one challenged this. The recommendation was defensive from the start — it confirms a status quo rather than proposing a change. Its value is that it creates an explicit record that this section was reviewed and approved at its current length, which gives Phase 3 reviewers a baseline to measure against if expansion is proposed.

#### Recommendation 7: Confirm no SKILL.md changes occurred in Phase 2

- **Original position**: Verify via git diff or file inspection that SKILL.md has not been modified since Phase 1 completed.
- **Disposition**: Surviving
- **Explanation**:
  - Both cross-reviews confirmed this is a valid concern. taxonomy-reviewer's cross-review (Safe Agreements, "No SKILL.md modifications in Phase 2 / Phase boundaries intact") stated: "scope-boundary performed a systematic phase-boundary check... The combined assessment from a scope-focused reviewer and a taxonomy-focused reviewer both finding clean boundaries is a strong signal." consistency-checker's cross-review (Safe Agreements, "Phase boundaries are intact") confirmed the same from a consistency perspective.
  - No one challenged this. It is a structural verification that costs nothing and provides the assurance that Phase 4's SKILL.md work starts from the expected baseline. Priority remains P1 because a SKILL.md modification during Phase 2 would be the most consequential phase boundary violation — it would invalidate Phase 4's assumptions about the file's state.

---

### New Recommendations

- **Normalize spec 004's compound implementation label** (Priority: P1)
  - **Triggered by**: consistency-checker's cross-review of scope-boundary (Tensions, "Spec 004's compound implementation label") and my own cross-review of consistency-checker (Dangerous Contradictions, "Scope of spec 004's compound implementation label"). consistency-checker's original review flagged that STATUS.md L46 uses "Implementation-complete (core) / Not started (discovery)" — a compound format that is not defined in the three-value implementation tier taxonomy (L9-13). My cross-review acknowledged: "consistency-checker identifies a genuine taxonomy consistency issue that scope-boundary missed entirely... This is exactly the kind of controlled-vocabulary violation that scope-boundary's own mandate is designed to catch."
  - **Proposed change**: Relabel spec 004's implementation tier from "Implementation-complete (core) / Not started (discovery)" to **"Partially-complete"** and move the core/discovery detail into the existing notes field (e.g., "Core (FR-001-021) implementation-complete, discovery (FR-022-024) not started"). This preserves the three-value controlled vocabulary without information loss. The Phase 2 checkpoint claims "STATUS.md taxonomy is authoritative" (tasks.md L47) — an authoritative taxonomy whose own entries violate its controlled vocabulary is not authoritative.
  - **Rationale**: I missed this in my original review because I was focused on the acceptance tier (Phase 2's primary addition) and treated the implementation tier labels as pre-existing givens. consistency-checker correctly pointed out that the checkpoint's "authoritative" claim covers both tiers. If Phase 2 defines both tiers of the taxonomy but only enforces one, the enforcement is incomplete. This finding falls squarely within scope-boundary's mandate: the taxonomy's controlled vocabulary must be consistently applied in the same file that defines it.

---

### Position Summary

Of my original 7 recommendations, I modified 3 (Recommendations 1, 2, and 3), maintained 4 (Recommendations 4, 5, 6, and 7), and withdrew none. I added 1 new recommendation (normalize spec 004's compound implementation label). The total actionable set is now 5 items requiring changes (Recommendations 1, 2, 4, and the new recommendation at P1; Recommendation 5 at P2) and 2 items confirming the status quo (Recommendations 6 and 7).

The most significant change in my thinking was the label name for the missing acceptance-tier value. My original recommendation reused "Not started" from the implementation tier, which consistency-checker correctly identified as violating the very orthogonality principle I was enforcing. When two tiers are defined as measuring "different dimensions" (STATUS.md L5), sharing a label name between them creates exactly the terminological ambiguity the taxonomy exists to prevent. "Not assessed" is the right name because it describes an acceptance-tier state in acceptance-tier language — criteria evaluation status — without borrowing implementation-tier vocabulary. This was a genuine blind spot: I was so focused on the taxonomy having a third value that I did not scrutinize the value's name against the taxonomy's own design principle.

My remaining highest-priority recommendation is the new one: normalizing spec 004's compound implementation label to "Partially-complete." This should survive into the final synthesis because it addresses a controlled-vocabulary violation in the implementation tier that is structurally identical to the acceptance-tier violation all three reviewers already agree must be fixed. The Phase 2 checkpoint claims the taxonomy is "authoritative." An authoritative taxonomy that tolerates ad-hoc compound labels in one tier while rigorously enforcing controlled vocabulary in the other tier is inconsistent on its face. If the synthesis fixes the acceptance tier (adding "Not assessed") but leaves the implementation tier's compound label uncorrected, Phase 3 inherits a STATUS.md where one tier's vocabulary is enforced and the other's is not — and T012a (adding spec 005) will have no guidance on whether compound implementation labels are permitted.
