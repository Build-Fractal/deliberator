# Consistency Checker Revision — Phase 2: Two-Tier Status Convention

**Reviewer**: consistency-checker
**Date**: 2026-03-20
**Spec**: 005-p2p3-backlog-hardening
**Gate**: Phase 2 (Two-Tier Status Convention)
**Revision iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Add "not-assessed" to the acceptance tier

- **Original position**: Add a third acceptance-tier value ("not-assessed") or a scoping rule to handle specs with zero implementation, because the two-value acceptance tier cannot represent spec 003's state.
- **Disposition**: Modified
- **Explanation**:
  Both taxonomy-reviewer and scope-boundary challenged the label name, not the substance. taxonomy-reviewer's cross-review (Dangerous Contradictions, "Acceptance tier label naming") argued that formalizing the existing "Not started" label is simpler than introducing new vocabulary. scope-boundary's cross-review (Dangerous Contradictions, "Acceptance tier label for unimplemented specs") made the same argument with a different framing: "Not started" already exists in STATUS.md L41, so legitimizing it has lower adoption friction.

  However, both cross-reviewers' own analyses ultimately conceded the core semantic point. taxonomy-reviewer's cross-review resolution states: "consistency-checker's 'not-assessed' is semantically more precise because it describes the evaluation state rather than the implementation state, which is the acceptance tier's domain." scope-boundary's cross-review resolution states: "consistency-checker's terminology is more precise — 'Not started' risks confusion with the implementation tier's identical label."

  I withdraw the alternative scoping rule ("acceptance labels only apply when implementation > 0"), which scope-boundary correctly identified as adding unnecessary complexity that would complicate T012a's labeling of spec 005 (scope-boundary cross-review, Dangerous Contradictions, suggested resolution). The modified recommendation retains "not-assessed" as the label name but broadens its definition per taxonomy-reviewer's suggestion to cover both "no implementation exists to assess" and "implementation exists but acceptance has not been formally evaluated." This handles spec 005's Phase 3 state where partial implementation exists but no formal acceptance evaluation has occurred.

  **Modified recommendation**: Add a third acceptance-tier value to STATUS.md's Acceptance Tier section: "**Not assessed**: No acceptance evaluation has been performed. Either no implementation exists to evaluate, or implementation exists but acceptance criteria have not been formally verified." Apply this label to spec 003's acceptance column and to spec 004's discovery component. Drop the alternative scoping rule.

#### Recommendation 2: Normalize spec 004's compound implementation label

- **Original position**: Either relabel spec 004 as "Partially-complete" (option a) or explicitly permit compound labels (option b), with preference for option (a).
- **Disposition**: Modified
- **Explanation**:
  taxonomy-reviewer's cross-review (Dangerous Contradictions, "Spec 004 compound label") argued that "Partially-complete" loses information about which subsystem is complete and that compound labels are pragmatically useful when specs have independently-implementable subsystems. taxonomy-reviewer's suggested resolution endorsed my option (b) over option (a): "Given that spec 004 genuinely has two independently-implementable subsystems... the pragmatic answer is consistency-checker's option (b): explicitly permit compound labels." scope-boundary's cross-review (Dangerous Contradictions, "Scope of spec 004's compound implementation label") also sided with my option (b) via option (a), suggesting relabeling as "Partially-complete" and moving the split to the gaps field — but this was before the coordination resolved toward compound labels.

  In my own cross-review of taxonomy-reviewer (Dangerous Contradictions, "Whether spec 004's compound implementation label should be normalized or formalized"), I proposed a cooperative resolution: permit compound labels but constrain them to use only existing tier values as components. I still hold this position. The key insight from taxonomy-reviewer is correct — "Partially-complete" genuinely loses information that a reader needs. But compound labels must use the controlled vocabulary, not invent new terms.

  **Modified recommendation**: Explicitly permit compound labels in the Implementation Tier section of STATUS.md's taxonomy. Add a rule: "Specs with independently-implementable subsystems may use compound labels combining the defined values (e.g., 'Implementation-complete (core) / Not started (discovery)'). Each component must use one of the three defined implementation-tier labels." Retain spec 004's current label format, which already complies with this rule. Priority remains P1 because the taxonomy section must document what it permits before Phase 3.

#### Recommendation 3: Add acceptance gap documentation for spec 004

- **Original position**: Add acceptance gaps for spec 004 referencing US-3 through US-6 acceptance scenarios.
- **Disposition**: Modified
- **Explanation**:
  taxonomy-reviewer's cross-review (Tensions, "Priority assignment for acceptance gap documentation on spec 004") argued this should be P1, not P2, because the Phase 2 checkpoint ("STATUS.md taxonomy is authoritative," tasks.md L47) requires complete application of the taxonomy to all specs — and a "Feature-complete" label without gap documentation is incomplete application. scope-boundary's cross-review (Tensions, "Priority assignment for spec 004 acceptance gap documentation") agreed on the problem and the P2 priority, noting the content disagreement on whether gaps should reference FRs or acceptance scenarios.

  In my own cross-review of scope-boundary (Dangerous Contradictions, "Scope of gap documentation obligation"), I identified the tension between FR-based gaps and acceptance-scenario-based gaps, and proposed FR-based gaps with parenthetical noting affected acceptance scenarios as the pragmatic convention. I maintain this position on gap content, but I yield to taxonomy-reviewer on priority: P1 is correct.

  The checkpoint says "Two-tier convention defined and applied to all 4 specs." If spec 001 has gap documentation but spec 004 does not, the convention is not uniformly applied. This is a Phase 2 completeness issue, not Phase 3 enrichment.

  **Modified recommendation**: Add acceptance gap documentation for spec 004. Use FR-based identifiers consistent with spec 001's precedent, with parenthetical noting acceptance scenario impact: "**Gaps**: FR-022 (preset list command), FR-023 (preset filter command), FR-024 (preset detail command) — discovery features not started; acceptance scenarios US-3 through US-6 not testable." Priority upgraded to P1.

#### Recommendation 4: Clarify FR-023 gap characterization in STATUS.md

- **Original position**: Expand STATUS.md L32's FR-023 parenthetical to distinguish between the existing validation check and the pending heading match semantics (spec 005 FR-007).
- **Disposition**: Modified
- **Explanation**:
  scope-boundary's cross-review (Tensions, "Depth of FR-023 gap characterization") raised a legitimate scope concern: FR-007 is a Phase 4 task (T013), and enriching the gap description with Phase 4 cross-references could be Phase 3 content leaking backward. However, scope-boundary's resolution conceded: "If Phase 2 wrote the text, Phase 2 should fix it."

  taxonomy-reviewer's cross-review (Tensions, "Scope of FR-023 gap characterization") identified a different symptom of the same issue: US5 AS3 in spec.md treats FR-023 as a partial gap, while FR-013 lists it as a full gap. taxonomy-reviewer recommended reconciling these two framings.

  In my own cross-review of taxonomy-reviewer (Tensions, "Granularity of FR-023 gap characterization"), I noted that both fixes address different symptoms and should both be applied. I still hold this position, but I accept scope-boundary's framing: the STATUS.md fix should be concise with a pointer, not an exhaustive cross-spec breakdown.

  **Modified recommendation**: Revise STATUS.md L32's FR-023 parenthetical to: "FR-023 (output validation — SKILL.md validation check exists; heading match semantics and template-level instructions pending; see T013)." This is concise, accurate, and does not import Phase 3 structural elements. Separately, reconcile spec.md US5 AS3's treatment of FR-023 with FR-013's gap list per taxonomy-reviewer's recommendation. Priority remains P2.

#### Recommendation 5: Define acceptance label transition criteria

- **Original position**: Add a transition rule: "A spec transitions from feature-complete to spec-complete when all acceptance scenarios defined in its spec.md are verified as satisfied."
- **Disposition**: Modified
- **Explanation**:
  taxonomy-reviewer's cross-review (Tensions, "Transition criteria specificity") identified that my one-condition formulation (acceptance scenarios only) is weaker than taxonomy-reviewer's two-condition formulation ("all documented gaps are resolved AND all acceptance scenarios pass"). taxonomy-reviewer's cross-review resolution stated: "taxonomy-reviewer's dual-condition formulation is more conservative and prevents a scenario where a spec is relabeled 'spec-complete' while its Gaps field still lists items."

  This is correct. My original formulation has a gap: if all acceptance scenarios pass but documented gaps remain in the Gaps field (e.g., gaps that do not map to specific acceptance scenarios), the spec would qualify as "spec-complete" under my rule while still having documented gaps — an awkward state that undermines the Gaps field's utility.

  In my own cross-review of taxonomy-reviewer (Tensions, "Whether transition criteria belong in Phase 2 or Phase 3 scope"), I proposed making gap resolution the primary trigger with scenario verification as the evidence. I now adopt a cleaner version of taxonomy-reviewer's two-condition formulation.

  scope-boundary's cross-review (Tensions, "Acceptance label transition criteria") noted this could be Phase 3 scope but conceded: "A one-sentence transition rule that clarifies when labels change is defensibly part of defining those labels." I agree — transition criteria are definitional, not enrichment.

  **Modified recommendation**: Add to the taxonomy section: "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied." Priority remains P2.

#### Recommendation 6: Verify spec 002 "Spec-complete" label against acceptance scenarios

- **Original position**: Spot-check spec 002's 18 acceptance scenarios against SKILL.md, or add a caveat that "Spec-complete" is based on FR coverage.
- **Disposition**: Modified
- **Explanation**:
  scope-boundary's cross-review (Tensions, "Scope of Phase 2 review: SKILL.md cross-verification depth") raised a legitimate scope question: does the Phase 2 gate check that labels are substantively accurate, or only syntactically valid and applied? scope-boundary's resolution suggested this "may need to be flagged as a Phase 3 prerequisite rather than a Phase 2 blocker."

  taxonomy-reviewer's cross-review (Tensions, "Spec 002 'Spec-complete' verification depth") framed the concern through the temporal lens: T019 (Phase 4) may change parsing behavior and invalidate the label. Their resolution proposed separating present-facing verification (Phase 2) from future-facing staleness (separate note).

  In my own cross-review of scope-boundary (Dangerous Contradictions, "Whether spec 002's 'Spec-complete' label is safe to accept at face value"), I proposed a lightweight spot-check as a compromise — not full verification but enough to confirm the label is defensible. scope-boundary accepted this approach in principle. I maintain this position but accept that full scenario-level verification is disproportionate for Phase 2.

  **Modified recommendation**: Perform a lightweight dependency-focused check: verify that spec 002's acceptance scenarios that depend on spec 001's parsing subsystem (specifically US-2 AS3 — stagnation with arbiter configured) can be evaluated given the current parsing implementation. If the dependency means these scenarios cannot be independently verified, add a qualification note to spec 002's entry: "Spec-complete (subject to re-evaluation after T019 modifies dispute-parsing cross-references)." Defer full scenario-level spot-checking to Phase 3 (T010/T011). Priority downgraded to P3 — this is a due-diligence check, not a blocker.

#### Recommendation 7: Add explicit guidance for Phase 3 on labeling spec 005 itself

- **Original position**: Add a note to T012a specifying what acceptance label to assign spec 005 when the task runs in Phase 3.
- **Disposition**: Surviving
- **Explanation**:
  taxonomy-reviewer's cross-review (Tensions, "Whether the taxonomy needs an 'in progress' acceptance label") proposed an alternative: adding a fourth acceptance-tier label ("Partially feature-complete" or "In progress") rather than using "feature-complete" with gap documentation. In my own cross-review of taxonomy-reviewer (Tensions), I argued against this: adding a fourth label for a single known case increases taxonomy complexity disproportionately.

  scope-boundary's cross-review (Tensions, "Spec 005 self-tracking") proposed a complementary fix: annotate T007 with an explicit exclusion note for spec 005, deferring to T012a. In my own cross-review of scope-boundary (Tensions, "Spec 005 self-tracking"), I identified these as complementary: annotate T007 on the "out" side AND annotate T012a on the "in" side.

  No cross-review challenged the substance of this recommendation. The only question was whether to also add a taxonomy label (taxonomy-reviewer) or a T007 exclusion note (scope-boundary). I adopt both as additions.

  **Surviving recommendation**: Add labeling guidance to T012a: "Label spec 005 implementation status based on FRs completed at time of writing. If major capabilities are still pending and the gap list is unstable, label acceptance as 'not-assessed.' If all major capabilities are present with enumerable gaps, label as 'feature-complete' with gaps listed. Update both labels in Phase 5 (T016/T017)." Also adopt scope-boundary's recommendation to annotate T007 with "(Spec 005 entry deferred to T012a, Phase 3)." Priority remains P3.

#### Recommendation 8: Document the relationship between FRs and acceptance scenarios in the taxonomy

- **Original position**: Add a clarifying note explaining that gap documentation may reference FRs (implementation requirements) or acceptance scenarios (testable behaviors).
- **Disposition**: Surviving
- **Explanation**:
  No cross-review directly challenged this recommendation. taxonomy-reviewer did not address it. scope-boundary's cross-review (Tensions, "Priority assignment for spec 004 acceptance gap documentation") noted that the tension between FR-based and acceptance-scenario-based gap documentation "reflects a deeper ambiguity that consistency-checker explicitly calls out (Actionable Recommendations #8) but scope-boundary does not address" — implicitly validating the need.

  In my own cross-review of scope-boundary (Dangerous Contradictions, "Scope of gap documentation obligation"), I identified the same FR-vs-acceptance-scenario tension and proposed a resolution: FR-based gaps with parenthetical noting affected acceptance scenarios. This resolution depends on establishing the convention that Recommendation 8 proposes.

  This recommendation is low priority but structurally important: without it, Phase 3 contributors will face the same ambiguity when writing T010 (risk-of-gap) and T012a (spec 005 entry). The convention should be brief.

  **Surviving recommendation**: Add a one-sentence convention note to the taxonomy section: "Gap documentation uses FR identifiers as primary references; affected acceptance scenarios may be noted parenthetically for traceability." Priority remains P3.

### New Recommendations

- **Reconcile spec.md US5 AS3 with FR-013 gap list** (Priority: P2)
  - **Triggered by**: taxonomy-reviewer's cross-review (Tensions, "Scope of FR-023 gap characterization"), which identified that US5 AS3 in spec.md treats FR-023 as a partial gap (listing only FR-025 and FR-026 as full gaps) while FR-013 lists all three (FR-023, FR-025, FR-026) as gaps. My own cross-review of taxonomy-reviewer (Tensions, "Granularity of FR-023 gap characterization") confirmed the two fixes address different symptoms and should both be applied.
  - **Proposed change**: Align US5 AS3's gap list with FR-013: either list all three FRs consistently in US5 AS3, or add a parenthetical to US5 AS3 explaining that FR-023 is a partial gap (validation logic exists, template instructions pending). The spec's internal references must be self-consistent.
  - **Rationale**: If US5 AS3 and FR-013 disagree about how many gaps spec 001 has, an implementor verifying acceptance scenario 3 will reach a different conclusion than one reading FR-013 directly. This is exactly the kind of inconsistency my mandate exists to catch, and I missed it in my original review. taxonomy-reviewer caught it.

### Position Summary

Of my original eight recommendations, I modified six (Recommendations 1-6), maintained two (Recommendations 7-8), and withdrew none. I added one new recommendation surfaced by taxonomy-reviewer's identification of a spec-internal inconsistency (US5 AS3 vs. FR-013) that I missed.

The most significant change in my thinking concerns the compound implementation label (Recommendation 2). I originally preferred normalizing spec 004 to "Partially-complete" because I prioritized controlled-vocabulary purity over information density. taxonomy-reviewer's argument — that compound labels composed from existing tier values preserve the vocabulary while retaining subsystem-level information — changed my position. The cooperative resolution of constraining compound labels to use only defined tier values addresses my original consistency concern without the information loss I was willing to accept. This modification also has the largest downstream impact: it changes the taxonomy from a strict three-value system to a structured-extension system, which affects how Phase 3's T012a will format spec 005's entry.

My remaining highest-priority recommendation is Recommendation 1 (add "not-assessed" to the acceptance tier), now modified to use a broader definition covering both unimplemented and unevaluated states. This should survive into the final synthesis because all three reviewers agree the problem is real and critical — the only disagreement was on the label name, and both cross-reviewers' resolutions favored "not-assessed" over "Not started" on semantic precision grounds. Without this fix, Phase 3 cannot assign acceptance labels consistently to spec 005 (T012a), and the Phase 2 checkpoint claim that "STATUS.md taxonomy is authoritative" is false — the taxonomy uses an undocumented label for spec 003. This is the single most consequential finding across all three reviews.
