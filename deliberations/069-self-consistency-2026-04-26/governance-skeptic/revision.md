# Governance-Skeptic Revision (Phase 3, iteration 1)

### Recommendation Dispositions

#### Recommendation 1: Lift the gate to a subsection

- **Original position**: Promote the gate from a third bullet under Governance to a sibling subsection `### Constitutional Inclusion Criteria`.
- **Disposition**: **Surviving**.
- **Explanation**: Both cross-reviewers endorsed this as a safe structural fix. Strictness-skeptic SA-1 explicitly says the change is "harmless to the strictness debate" and improves audit-trail discoverability. Practitioner DC-4 raises a tension with their own sync-impact-report proposal but does not contest the merit — only the redundancy of doing both. The redundancy concern is illusory: the sync impact report announces the change in the document's history; the subsection houses the rule itself. They are different artifacts and both should land. No modification needed.

#### Recommendation 2: Wire the gate into the amendment workflow explicitly

- **Original position**: Add to the Amendments bullet that amendments proposing a new principle MUST include an Inclusion Criteria Self-Assessment in the Sync Impact Report.
- **Disposition**: **Modified**.
- **Explanation**: Strictness-skeptic DC-2 raises a real problem: an enforcement hook on a mis-calibrated gate amplifies miscalibration into procedural force. Practitioner T-2 sharpens this by noting that the Sync Impact Report carries substance but cannot be mechanically enforced, while a CI lint can enforce form but not substance. I now believe both pieces are needed and the original recommendation was incomplete.
- **Concrete modification**: The Amendments bullet should require *two* enforcement surfaces, scaled to materiality. (a) For amendments proposing a new principle OR an extension to an existing principle, the Sync Impact Report MUST contain an "Inclusion Criteria Self-Assessment" section addressing each criterion. "N/A — typo fix" is a valid answer for clarification-class amendments, but the section MUST exist. (b) A CI lint on the constitution PR MUST grep for the section heading and fail the PR when absent. The lint enforces *form*; reviewers audit *substance* against the headings. This addresses strictness-skeptic's calibration concern by making the bar lightweight for trivial changes and addresses practitioner's mechanical-enforcement concern by adding the lint that the original recommendation lacked.

#### Recommendation 3: Define extension semantics

- **Original position**: Extensions to grandfathered principles (sub-sections introduced via "Extension (vN.N.N):" or "Clarification (vN.N.N):" headers) ARE subject to this gate.
- **Disposition**: **Modified**.
- **Explanation**: Strictness-skeptic DC-1 makes a load-bearing point I underweighted: under the current AND'd three-criterion structure, subjecting extensions to the full gate effectively freezes the constitution at v2.4.0 because extensions are inherently narrower than principles and will struggle with criterion 3 (distinctness from the host they extend). Practitioner T-1 reaches the same conclusion via a different path: "skeptic's clean rule risks blocking valid v2.3.0-style extensions." Both reviewers agree the loophole is real but the cure as drafted is worse than the disease.
- **Concrete modification**: Extensions ARE subject to the gate, with two narrowing carve-outs. (a) Criterion 3 (distinctness) is automatically satisfied for an extension when the extension's scope is a strict subset of the host principle's scope and the extension explicitly identifies which sentence(s) of the host it refines — this is the natural semantics of "extension" and removes the criterion-3 freeze. (b) Pure clarification headers ("Clarification (vN.N.N):") that add no new normative content are governed by Versioning's PATCH classification and require a Sync Impact Report rationale but not a full Inclusion Criteria Self-Assessment. The carve-outs preserve the loophole-closure (you cannot bury new normative content inside an existing principle) while admitting legitimate refinements.

#### Recommendation 4: Tighten falsifiability of criterion #1

- **Original position**: Require the amendment PR description to contain a one-paragraph sketch of the proposed check, identifying the check type from a fixed taxonomy (CI lint, parity test, structural assertion, schema validation, contract test, meta-test) and the specific artifact it would inspect.
- **Disposition**: **Withdrawn**.
- **Explanation**: Strictness-skeptic DC-3 made the strongest counter-argument in either cross-review: the fixed taxonomy bakes in a bias toward behavioral/lintable invariants and against formal/taste-level invariants. Their hypothetical (Principle X "Zen of Python Output" cannot satisfy any taxonomy entry) is a clean falsification of my proposal. Practitioner DC-1 reached the same conclusion from a velocity angle: pinning the taxonomy upfront forces premature commitment. The two cross-reviews converged on the same critique from different lenses, which is strong signal that the recommendation as drafted was wrong.
- I am withdrawing rather than modifying because the substance of the fix — "actually require a sketch" — is preserved by Recommendation 2's self-assessment requirement. The self-assessment will contain an answer to criterion 1; if the answer is rhetorically empty, that is a reviewer judgment call, not a taxonomy violation. Removing the taxonomy preserves room for formal/taste-level principles without losing the dogfooding improvement. Strictness-skeptic gets credit for this withdrawal.

#### Recommendation 5: Add tie-breaker for criterion #3

- **Original position**: When distinctness is contested, the burden is on the amendment author to identify which existing principle(s) cover ≥80% of the proposed scope and explain why the residual ≥20% requires a new principle.
- **Disposition**: **Modified**.
- **Explanation**: Strictness-skeptic T-3 prefers a "cleanliness" rule over a quantitative threshold. Practitioner T-3 (commenting on my recommendation directly) flags that "what counts as 20% residual? lines of text? semantic distance?" is itself contested — a quantitative threshold creates new litigation surface. I withdrew the original numeric framing but the underlying need (a tie-breaker) remains.
- **Concrete modification**: Replace "≥80%/≥20% scope decomposition" with: "When distinctness is contested, the amendment author MUST identify the existing principle(s) closest to the proposed scope and EITHER (a) demonstrate that composition of those principles cannot produce the same operational guarantee without runtime-inferred coordination, OR (b) propose the principle as an extension of the closest existing principle. If neither option is satisfied, the amendment is not yet ready for the gate." This adopts strictness-skeptic's "cleanliness" framing (operational coordination must not be runtime-inferred) without their unconstrained wording, and avoids practitioner's quantification concern. The XV ↔ XXVII coordination passes under this rule because the cross-references are explicit, not runtime-inferred.

#### Recommendation 6: Document a documented override path

- **Original position**: Rejection by any criterion MAY be overridden by an arbiter ruling in a deliberation where ≥3 independent agents converged on the principle's necessity.
- **Disposition**: **Withdrawn**.
- **Explanation**: Practitioner DC-2 is correct that "≥3 agents converging on necessity" is the *normal* deliberation pattern — every existing principle was ratified through a converged deliberation, so the override criterion is satisfied by definition for any principle that reaches the constitution. The override would not function as an override; it would function as the default path. Strictness-skeptic T-4 raises a related but distinct concern (override creates a chokepoint-with-bypass that prevents systemic recalibration). Both critiques are valid and both surface that my recommendation, as drafted, was structurally broken.
- A revised override path would need a stricter trigger (e.g., unanimous arbiter + documented inability to route to operational guidance, per practitioner) AND a sequencing rule with strictness-skeptic's R-10 retrospective loosening (tracked overrides that exceed a threshold trigger gate recalibration). That is a substantively different proposal that should be developed in a follow-up amendment after v2.4.0 ships, not bolted onto this revision. Withdrawing.

#### Recommendation 7: Harmonize MUST/SHOULD/MAY across Governance

- **Original position**: Rewrite Amendments and Versioning bullets to use uniform RFC 2119 modal verbs matching the new gate.
- **Disposition**: **Modified**.
- **Explanation**: Practitioner DC-3 raises a real conflict: a uniform MUST treatment of all amendments collides with their PATCH carve-out for trivial changes. I rejected the practitioner PATCH carve-out in my own cross-review (it creates an exploitable bypass), but the underlying observation — that not all amendments should bear the same procedural weight — is correct. The fix is to scale the requirement, not to exempt categories.
- **Concrete modification**: Rewrite Amendments to: "Amendments MUST document the change, rationale, and impact on existing specs in the Sync Impact Report. Amendments proposing a new principle or an extension to an existing principle MUST additionally include an Inclusion Criteria Self-Assessment per the Constitutional Inclusion Criteria subsection. Use `/speckit.constitution` to update." Versioning leader becomes "Version bumps MUST follow:" Both bullets now use MUST, but the procedural cost scales with the amendment's content (rationale only for clarifications, full self-assessment for new content). This composes cleanly with Recommendation 2's modified form.

#### Recommendation 8: Clarify the relationship to Versioning classification

- **Original position**: Add a Versioning sub-bullet declaring that an amendment redirected from a new principle to an extension is MINOR, not PATCH.
- **Disposition**: **Modified**.
- **Explanation**: Strictness-skeptic DC-4 argues this fights the natural Versioning rule and creates a perverse incentive away from "extension to existing principle" (now MINOR + gated) toward shopping for a new-principle slot. Practitioner T-3 reaches a compatible conclusion via "the PATCH carve-out applies only to clarifications of existing principles, not to new content routed through an existing principle's body." Both cross-reviewers agree the *boundary* between PATCH and MINOR is what needs articulation, not a blanket "redirected = MINOR" rule.
- **Concrete modification**: Replace the original sub-bullet with: "An extension that adds new normative content to an existing principle is MINOR ('material expansion'). An extension that only refines wording, adds cross-references, or clarifies scope without changing what the principle requires of consumers is PATCH ('clarification'). The classification is determined by *consumer impact*, not author intent — if a previously-passing artifact would now fail under the extension, the extension is MINOR." This addresses strictness-skeptic's perverse-incentive concern (the gate doesn't redirect classification; consumer impact does) and practitioner's ambiguity concern (the discriminator is concrete and testable).

#### Recommendation 9: Disambiguate "operational guidance" from `SKILL.md`

- **Original position**: Add a parenthetical noting that `SKILL.md` content is runtime-enforced, so placing a rule there strengthens it.
- **Disposition**: **Surviving**.
- **Explanation**: Strictness-skeptic T-2 endorses this as sharper than their MO-8 and notes their fix and mine pull in different directions but are both needed. Practitioner T-4 prefers a full routing decision tree but does not contest the substance. The parenthetical is the smaller fix and is uncontroversial; a routing tree is a separate operational-guidance improvement that can land in CONTRIBUTING.md without amending the constitution. No modification needed for v2.4.0.

#### Recommendation 10: Add a cross-reference to Principle XVII

- **Original position**: Add a cross-reference from the gate to Principle XVII (Content Classification).
- **Disposition**: **Surviving**.
- **Explanation**: Both cross-reviewers endorsed this independently (strictness-skeptic SA-4, practitioner SA-3). My own cross-review of practitioner critiqued the *direction* of their proposed cross-reference (their version went XVII → gate; mine goes gate → XVII). The constitution's reference topology (Governance references principles, not the reverse) supports my direction. No modification needed.

### New Recommendations

#### NR-1: Sequence the per-amendment self-assessment with a retrospective recalibration trigger

- **Origin**: Strictness-skeptic T-4 (their R-10 vs. my override) made me realize the constitution lacks any *systemic* recalibration mechanism for the gate itself. My withdrawn override (Recommendation 6) was the wrong instrument; their R-10 retrospective trigger is the right one but my original review did not engage with it.
- **Proposed change**: Add to the Constitutional Inclusion Criteria subsection: "If three or more proposed principles are rejected by this gate within a single MAJOR version cycle, the next MINOR amendment MUST include a calibration review of the rejections — concretely, evaluating whether the rejected proposals would have been admitted under the gate's intended bar, and proposing gate-text revisions if the rejection rate exceeds the gate's intended discrimination."
- **Rationale**: Without this, the gate has no self-correction. The calibration review is recorded in the Sync Impact Report, so it inherits the existing audit trail. This makes the gate provisional (per strictness-skeptic) without weakening its per-amendment rigor (per my original concern).

#### NR-2: Add a v2.4.0 Sync Impact Report to the candidate file

- **Origin**: Practitioner SA-2 (clean catch — the candidate file's top Sync Impact Report describes v2.3.0 → v2.3.1, not v2.3.1 → v2.4.0).
- **Proposed change**: Insert a new Sync Impact Report block at the very top of the file (above the existing v2.3.0 → v2.3.1 block, which becomes the second-most-recent). The new block describes the inclusion criteria amendment, lists itself as a Governance change (no new principles), and includes the first Inclusion Criteria Self-Assessment as a reflexive demonstration.
- **Rationale**: The constitution's own change-tracking discipline requires this. Practitioner caught a self-consistency gap that I missed. Including the first self-assessment in the v2.4.0 report dogfoods Recommendation 2.

### Position Summary

My core position survives Phase 2 with two material changes. The gate's procedural under-specification remains the central defect, and the structural fixes — lifting to a subsection, defining extension semantics, wiring an enforcement hook, harmonizing modal verbs, cross-referencing Principle XVII — all retain their merit. Cross-reviews validated these as the safe, convergent improvements. Where I was wrong, I was wrong about the *shape* of the procedural rigor, not the need for it: the fixed check-type taxonomy in Recommendation 4 baked in a behavioral bias that strictness-skeptic correctly flagged, and the override path in Recommendation 6 was structurally satisfied by the normal deliberation pattern as practitioner pointed out. Both withdrawals improve the proposal.

The deepest tension between my review and strictness-skeptic's — whether the gate is procedural or substantive — does not need to be resolved by v2.4.0 if the gate carries both surfaces (mechanical lint for form, substantive review for content) and includes a retrospective calibration trigger that preserves the option to recalibrate later. NR-1 captures this. The deepest tension with practitioner — whether to scale procedural cost by amendment class or to apply uniform process — resolves cleanly in favor of consumer-impact-based scaling: the costs scale, but the gate fires on every amendment that adds normative content. The PATCH carve-out is dangerous; the lightweight self-assessment for clarifications is not.

The remaining uncertainty is in Recommendation 3 (extension semantics) and Recommendation 5 (criterion 3 tie-breaker). My modifications resolve the freeze concern strictness-skeptic raised and the unquantified-residual concern practitioner raised, but both modifications introduce new judgment surfaces (subset-of-scope test, runtime-inferred-coordination test) that future amendments will probe. That is acceptable for v2.4.0 because the gate has explicit grandfathering for I-XXVII, the extension carve-outs are conservative (favor admission of legitimate refinements over loophole closure), and NR-1 provides the recalibration mechanism if these judgment surfaces prove problematic. Ship v2.4.0 with these modifications; revisit the extension-semantics and tie-breaker rules at the next MAJOR if they accumulate litigation.
