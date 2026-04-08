# Taxonomy Reviewer — Phase 2 Revision (Iteration 1)

**Reviewer**: taxonomy-reviewer
**Date**: 2026-03-20
**Gate**: Phase 2 (Two-Tier Status Convention)
**Spec**: 005-p2p3-backlog-hardening

---

### Recommendation Dispositions

#### Recommendation 1: Add "Not started" to acceptance tier

- **Original position**: Add "Not started" as a third acceptance-tier label with the definition "No acceptance criteria have been evaluated. The spec has no implementation to assess."
- **Disposition**: Modified
- **Explanation**:
  - Both cross-reviews agreed that a third acceptance-tier value is needed — this was the highest-confidence finding across all three reviewers. However, the consistency-checker's cross-review (Dangerous Contradictions, first item) challenged the label name, arguing that reusing "Not started" across both tiers "undermines orthogonality by creating parsing ambiguity when a reader sees 'Not started' and must determine which tier it belongs to." The consistency-checker proposed "not-assessed" as semantically more precise for the acceptance tier's domain (evaluation state, not implementation state). The scope-boundary cross-review (Tensions, second item) challenged the definition wording, arguing that "The spec has no implementation to assess" creates a dependency between the acceptance label and the implementation tier, violating the orthogonality principle (STATUS.md L22-24). Scope-boundary proposed "The spec's features are not yet implemented" or simply dropping the second sentence.
  - **New recommendation**: Add a third acceptance-tier label named **"Not assessed"** with the definition: **"No acceptance criteria have been evaluated."** Drop the second sentence entirely. The label name "Not assessed" is semantically precise for the acceptance tier's domain — it describes evaluation state rather than implementation state, which is what the acceptance tier measures. Dropping the causal explanation ("The spec has no implementation to assess") preserves orthogonality — the acceptance tier should not reference implementation status in its definitions. The one-sentence definition is also consistent with the brevity of the other two acceptance-tier definitions.
  - The consistency-checker's argument about parsing ambiguity is the decisive factor. In STATUS.md, spec 003 (L41) displays both tiers on the same line: "**Implementation**: Not started | **Acceptance**: Not started." If the same label name appears in both tiers with different definitions, a reader scanning the taxonomy section must track which tier definition applies where. Using "Not assessed" for the acceptance tier makes tier membership unambiguous from the label alone.

#### Recommendation 2: Add explicit acceptance gaps to spec 004

- **Original position**: Add a Gaps field to spec 004's entry identifying which acceptance criteria remain unmet, parallel to spec 001's treatment.
- **Disposition**: Surviving
- **Explanation**:
  - The scope-boundary cross-review (Dangerous Contradictions, first item) challenged the priority, assigning P2 where I assigned P1. The consistency-checker's cross-review (Dangerous Contradictions, third item) also noted the priority divergence and suggested that my P1 is "more defensible" because spec 004's missing gap documentation means the taxonomy is "not fully applied" per the Phase 2 checkpoint (tasks.md L47: "Two-tier convention defined and applied to all 4 specs").
  - I maintain P1. The Phase 2 checkpoint says the taxonomy must be "authoritative." The taxonomy defines "Feature-complete" as having "acceptance criteria gaps remain" (STATUS.md L19). If spec 004 uses this label without listing gaps, the label is incomplete — the convention is defined but not fully applied. Spec 001 (STATUS.md L32) demonstrates the expected format: label plus enumerated gaps. Spec 004 (STATUS.md L46-48) uses the same label but shifts gap information into a narrative "Discovery" paragraph without identifying which acceptance criteria are unmet. The inconsistency is within the very file Phase 2 produces.
  - The specific gaps to document are the acceptance scenarios from spec 004 that depend on discovery CLI commands (FR-022-024), which are unimplemented. The consistency-checker's cross-review (Safe Agreements, second item) identified the specific scenarios: "US-3 through US-6 acceptance scenarios are not testable (discovery features not implemented)." This provides the concrete gap content.

#### Recommendation 3: Reconcile US5 AS3 gap list with FR-013 gap list

- **Original position**: Align the gap count between US5 AS3 (which frames FR-023 as a partial gap, listing two full gaps) and FR-013 (which lists three full gaps including FR-023).
- **Disposition**: Modified
- **Explanation**:
  - The scope-boundary cross-review (Tensions, fifth item) argued that the reconciliation belongs outside Phase 2: "US5 AS3 is a spec-level acceptance scenario — if it is inconsistent with FR-013, that is a spec-internal issue, not a STATUS.md issue. Phase 2 implemented FR-013 correctly in STATUS.md." This is a valid scope argument: Phase 2 edits STATUS.md, not spec.md, and STATUS.md correctly follows FR-013's three-gap formulation. The FR-013/STATUS.md alignment is not in dispute — only the US5 AS3 framing is inconsistent.
  - The consistency-checker's cross-review (Tensions, first item) raised a separate issue: the STATUS.md parenthetical for FR-023 is incomplete because it mentions template instructions but omits heading match semantics (spec 005 FR-007, planned for T013 in Phase 4). This is a within-document precision issue.
  - **New recommendation**: (a) Downgrade to P3 and reclassify as a spec errata note rather than a Phase 2 gate item. STATUS.md correctly implements FR-013; the US5 AS3 framing discrepancy is a spec-internal documentation issue that does not affect Phase 2's deliverables. (b) Separately, accept the consistency-checker's observation that the FR-023 parenthetical in STATUS.md could mention the heading-match semantics dependency (FR-007), but defer this to Phase 4 when T013 actually implements FR-007, at which point the FR-023 gap characterization in STATUS.md should be updated to reflect the complete picture. Filing this as a Phase 4 post-condition rather than a Phase 2 fix avoids editing STATUS.md for a dependency that has not yet been implemented.

#### Recommendation 4: Add transition criteria to taxonomy section

- **Original position**: Add a paragraph to the taxonomy section defining when a spec moves from "feature-complete" to "spec-complete" (all documented gaps resolved and all acceptance scenarios pass).
- **Disposition**: Modified
- **Explanation**:
  - The scope-boundary cross-review (Dangerous Contradictions, second item) directly challenged the phase placement: "Transition criteria define when labels change, which is an operational process rule, not a taxonomy definition... taxonomy-reviewer should yield on placing this in Phase 2. Transition criteria are valuable but belong in Phase 3 alongside FR-008's maintenance obligation (T008 in tasks.md L63)." The argument distinguishes between static definitions (what labels mean — Phase 2 scope) and operational rules (when labels change — Phase 3 scope).
  - This argument is persuasive. Phase 2's task descriptions (tasks.md L44-45) focus on "add two-tier acceptance convention" (T006) and "apply acceptance labels" (T007). Neither task mentions transition rules. FR-012 defines the labels; FR-008 defines the maintenance obligation. Phase 3's T008 explicitly operationalizes FR-008 with a maintenance note. Transition criteria are the natural companion to the maintenance obligation, not to the label definitions.
  - **New recommendation**: Refile as a Phase 3 input. When T008 adds the maintenance note to STATUS.md (tasks.md L63), the transition criteria should be included as part of that note: "A spec transitions from feature-complete to spec-complete when all documented gaps are resolved. Gaps are considered resolved when their corresponding acceptance scenarios pass." This formulation uses the dual-condition structure from my original review (gaps resolved AND scenarios pass) but places it where it operationally belongs — alongside the maintenance obligation, not alongside the definitions.
  - The consistency-checker's cross-review (Tensions, fourth item) endorsed my dual-condition formulation over the consistency-checker's single-condition version, noting that it "prevents the awkward state of 'spec-complete with documented gaps.'" I maintain the dual-condition structure. The phase placement changes; the substance does not.

#### Recommendation 5: Document compound-label conventions for multi-subsystem specs

- **Original position**: Add a note to the Implementation Tier section permitting compound labels for specs with independently-implementable subsystems.
- **Disposition**: Modified
- **Explanation**:
  - The consistency-checker's cross-review (Dangerous Contradictions, second item) proposed the opposite approach: normalize spec 004's compound label to "Partially-complete" with subsystem details in the gaps field. Their argument was that compound labels weaken the taxonomy's role as a controlled vocabulary. However, the same cross-review ultimately suggested a compromise (consistency-checker's own option (b)): "explicitly permit compound labels in the taxonomy, but require them to use only the existing three values as components."
  - In my own cross-review of the consistency-checker (Dangerous Contradictions, second item), I argued for this same compromise: "explicitly permit compound labels in the taxonomy with a clear rule for when they apply. This gives taxonomy-reviewer the granularity they want while addressing consistency-checker's concern about undocumented formats."
  - **New recommendation**: Add a note to the Implementation Tier section that permits compound labels but constrains them to existing tier values: "Specs with independently-implementable subsystems may use compound labels composed of existing tier values to distinguish subsystem status (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use a defined implementation-tier label." This preserves the controlled vocabulary (only the three defined labels appear as components) while accommodating the real-world need for subsystem-level granularity. It is the least disruptive change that closes the gap between what the taxonomy defines and what STATUS.md actually uses.
  - I accept the scope-boundary's implicit position that this is not the highest-priority issue (scope-boundary did not flag compound labels at all), and maintain P2 priority. This is a taxonomy-completeness item, not a gate blocker, but it should be resolved before Phase 3 adds spec 005 (T012a), which may also have subsystem variance.

#### Recommendation 6: Verify spec 002's "Spec-complete" label is justified

- **Original position**: Verify that spec 002's acceptance scenarios are fully satisfied and note the T019 temporal risk (Phase 4 parsing changes could invalidate the label).
- **Disposition**: Modified
- **Explanation**:
  - The scope-boundary cross-review (Dangerous Contradictions, third item) directly challenged this: "If the synthesis follows taxonomy-reviewer, Phase 2 must now audit spec 002's acceptance scenarios against Phase 4's planned changes (T019) before passing the gate. This pulls Phase 4 analysis into Phase 2, violating the phase boundary." Their suggested resolution is a compromise: "Phase 2 should not block on this, but the observation should be recorded as a risk note for Phase 4."
  - The scope-boundary argument about phase boundary violation is correct. Phase 2 defines and applies labels based on current state. Auditing labels against future phase changes is inherently a forward-looking activity that belongs in the phase where those changes occur. My original recommendation conflated two concerns: (a) whether the label is currently accurate, and (b) whether it will remain accurate after T019. Concern (a) is Phase 2 scope; concern (b) is Phase 4 scope.
  - The consistency-checker's cross-review (Tensions, second item) separated these concerns clearly: "Present-facing verification (consistency-checker) should be addressed in Phase 2... Future-facing staleness (taxonomy-reviewer) should be addressed by adding a note to spec 002's entry."
  - **New recommendation**: (a) Downgrade to P3 and limit Phase 2 scope to noting that spec 002's "Spec-complete" label is based on FR coverage in SKILL.md and the dependency note (STATUS.md L37-38) already qualifies runtime correctness. Do not block Phase 2 on acceptance-scenario verification. (b) Record a Phase 4 post-condition: "After T019 modifies dispute-parsing cross-references, re-evaluate spec 002's Spec-complete label against its acceptance scenarios." This separates the temporal risk from the current-state assessment and places each concern in its correct phase.

#### Recommendation 7: Add a "Partially feature-complete" or "In progress" acceptance label

- **Original position**: Add a fourth acceptance-tier label to handle spec 005's eventual state when it has some implementation but an unstable gap list.
- **Disposition**: Withdrawn
- **Explanation**:
  - The consistency-checker's cross-review (Tensions, third item) proposed a simpler alternative: use the existing "feature-complete" label with explicit guidance in T012a's task description ("Label acceptance status as 'feature-complete' with gaps listing the remaining Phase 4 FRs"). The scope-boundary cross-review (Tensions, third item) argued that adding a label FR-012 does not define would be an embellishment, and that deferring to Phase 3 is appropriate since the labeling question has not yet been encountered.
  - Both arguments are correct, and together they are decisive. Adding a fourth acceptance label for a single anticipated case (spec 005 in T012a) is disproportionate to the problem. The modified Recommendation 1 already adds "Not assessed" as the third label, which covers the case where no acceptance criteria have been evaluated. When spec 005 reaches Phase 3's T012a, the implementor can use either "Not assessed" (if the gap list is not yet stable) or "Feature-complete" (if major capabilities are present and gaps are enumerable). The existing three-label system, once the third label is added, is sufficient for all currently foreseeable states. I was solving a problem that the corrected taxonomy already handles.

#### Recommendation 8: Scope-check the "Interpreting the Two Tiers" paragraph

- **Original position**: Retain the dependency sentence in the "Interpreting the Two Tiers" paragraph (STATUS.md L24) as a natural part of explaining orthogonality, preempting a possible scope-boundary challenge.
- **Disposition**: Surviving
- **Explanation**:
  - The scope-boundary cross-review (Tensions, first item) confirmed that the section is "minimal and necessary" and explicitly approved retention. Both reviews agree the paragraph should stay as-is. The scope-boundary review added one qualifying principle: "expansion belongs in a separate document, not in this section." This establishes a boundary against future growth of the paragraph, which is reasonable.
  - No reviewer challenged the substance of this recommendation. The preemptive defense was correct — scope-boundary did evaluate this content and found it within scope. The dependency sentence stays, and the synthesis should note that the "Interpreting the Two Tiers" paragraph is at its maximum appropriate length for Phase 2.

---

### New Recommendations

- **Constrain STATUS.md label entries to use "Not assessed" instead of "Not started" for spec 003's acceptance tier** (Priority: P1)
  - **Triggered by**: The consistency-checker's cross-review (Dangerous Contradictions, first item) and scope-boundary's cross-review (Tensions, second item), both of which identified that borrowing the implementation tier's "Not started" label for the acceptance tier creates ambiguity. The modified Recommendation 1 changes the taxonomy definition but does not address the existing usage in STATUS.md L41.
  - **Proposed change**: Update spec 003's entry in STATUS.md L41 from "**Acceptance**: Not started" to "**Acceptance**: Not assessed" to match the new taxonomy definition. This is the application-side companion to the definition-side change in modified Recommendation 1.
  - **Rationale**: Defining a label without applying it leaves the same inconsistency that the original "Not started" problem created — an undefined label in use. Both the definition and the usage must be updated in the same Phase 2 pass.

---

### Position Summary

Of my eight original recommendations, I maintained two (Recommendations 2 and 8), modified five (Recommendations 1, 3, 4, 5, and 6), and withdrew one (Recommendation 7). I added one new recommendation to close a gap exposed by the label-name change in modified Recommendation 1.

The most significant change in my thinking was on phase boundaries. Three of my five modifications (Recommendations 3, 4, and 6) involved accepting the scope-boundary reviewer's argument that Phase 2 should define and apply labels based on current state, not anticipate future phases or add operational process rules. I had conflated "the taxonomy should be complete" with "the taxonomy should handle everything Phase 3 and Phase 4 will need." The scope-boundary reviewer correctly drew the line: Phase 2 defines what labels mean and applies them to all four specs. Transition rules belong with Phase 3's maintenance obligation (T008). Future-facing label verification belongs in the phase that makes the changes. Spec-internal documentation inconsistencies (US5 AS3 vs. FR-013) are errata, not Phase 2 gate items. This sharpened my understanding of what "authoritative taxonomy" means for the Phase 2 checkpoint — it means the taxonomy section defines every label actually used, and every feature-complete label has documented gaps. It does not mean the taxonomy anticipates every future state or resolves every cross-document inconsistency in spec.md.

My highest-priority surviving recommendation is Recommendation 2: add explicit acceptance gaps to spec 004. This is the most impactful remaining fix because it closes an internal inconsistency within STATUS.md itself — spec 001 documents its feature-complete gaps (L32) and spec 004 does not (L46-48). The taxonomy's definition of "feature-complete" explicitly states that "acceptance criteria gaps remain," which implies those gaps should be enumerable. Without gap documentation, the "Feature-complete" label on spec 004 is a classification without evidence. Both the consistency-checker and scope-boundary agreed the fix is needed; the only disagreement was priority. The Phase 2 checkpoint requires the convention to be "applied to all 4 specs," and incomplete application to spec 004 means the checkpoint is not fully met.
