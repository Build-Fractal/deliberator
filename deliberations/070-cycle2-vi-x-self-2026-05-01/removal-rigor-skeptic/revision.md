### Recommendation Dispositions

#### Recommendation 1: Correct the false cross-reference audit claim and repair L1589

- **Original position**: Correct the SIR's false claim of zero body-text cross-references to VI or X, and replace the stale L1589 sentence with text distinguishing the two remediation patterns — specifically naming VI and X as the canonical migrate-out examples.
- **Disposition**: Modified
- **Explanation**:

cross-reference-coherence's cross-review of my work identified a self-contradiction in my proposed replacement text: I named "Principles VI and X" as the migrate-out examples at L1589, but my own Recommendation 2 offered option (b) — retaining X via path (c). If option (b) were adopted, my repaired L1589 would immediately be wrong again. The cross-review states: "removal-rigor-skeptic's proposed L1589 text names VI and X as the migrate-out precedent — but removal-rigor-skeptic's own Rec 2 offers option (b) to retain X via path (c). If the arbiter accepts Rec 2 option (b) after adopting removal-rigor-skeptic's Rec 1 text, L1589 would again be wrong: it would name X as a migrate-out example when X was actually retained." (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Dangerous Contradictions, third bullet)

I accept this criticism. The proposed text was self-undermining. cross-reference-coherence's more conservative replacement text — naming the amendment by version and cycle rather than by principle numbers — survives any downstream decision about X's status.

The modified recommendation adopts cross-reference-coherence's conservative framing while incorporating one navigational improvement from my original (naming Principle XVI). The new proposed L1589 replacement:

> "The 2026-05-01 spec 070 cycle 1 amendment establishing this definition is the canonical path (c) precedent for grandfathered-principle remediation that elects to retain a principle in the constitution with a restructured headline (see Principle XVI). For grandfathered-principle remediation that elects to migrate the principle out entirely, see the v3.0.0 MAJOR amendment (spec 070 cycle 2) as the canonical migrate-out precedent."

This uses "restructured headline" (cross-reference-coherence's constitutionally-established terminology from Governance L1570), names Principle XVI for direct navigation, and avoids naming VI and X in body text (from cross-reference-coherence's conservative version). The SIR audit claim correction remains as originally stated: the cross-reference audit missed the plural form "Principles VI and X" at L1589; the corrected claim must acknowledge this body-text reference and document its repair. The core finding — L1589 is a live body-text reference, the SIR audit claim is false, and this is P1 — is confirmed independently by migration-soundness (migration-soundness/cross-reviews/removal-rigor-skeptic.md, Safe Agreements, first bullet). Priority remains P1.

---

#### Recommendation 2: Demonstrate that X's "one purpose per file" sub-bullet is Criterion 1-ineligible, or elevate it via path (c)

- **Original position**: Require the SIR to either document a Criterion 3 analysis showing X's one-purpose-per-file sub-bullet is a composition of existing principles (option a), or apply path (c) to retain X with that sub-bullet as the constitutional headline (option b).
- **Disposition**: Modified
- **Explanation**:

Both cross-reviews independently identified option (b) as creating dangerous downstream conflicts. migration-soundness's cross-review: "if rrs's path (c) analysis leads to reconstituting X's one-purpose-per-file substrate, the entire structure of docs/output-conventions.md changes, and ms's Recommendation 1 (add nav entry) and Recommendation 7 (atomic commit with all four files) would be acting on a document whose content is in flux." (migration-soundness/cross-reviews/removal-rigor-skeptic.md, Dangerous Contradictions, second bullet) cross-reference-coherence's cross-review: "If removal-rigor-skeptic's option (b) is adopted and X is retained via path (c), every cross-reference-coherence recommendation that depends on X being removed becomes moot or actively wrong." (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Dangerous Contradictions, first bullet)

Both cross-reviews converge on the same resolution: "the synthesis could require the SIR to add a documented path (c) evaluation of X's one-purpose-per-file sub-bullet... WITHOUT reconstituting X, thus satisfying rrs's analytical obligation while leaving ms's operational recommendations intact." (migration-soundness/cross-reviews/removal-rigor-skeptic.md, resolution paragraph under second dangerous contradiction)

I accept this framing. The analytical obligation the v2.6.0 path (c) precedent creates is that substrate analysis MUST be documented before migrate-out is chosen; it does NOT require that the substrate be retained. Option (a) was always sufficient to discharge the obligation; option (b) was an overreach that I offered without fully tracing its downstream consequences.

The modified recommendation: withdraw option (b) entirely. The recommendation is now option (a) only — the SIR MUST add a paragraph documenting the Criterion 3 analysis of X's "one clear purpose per output file" sub-bullet against existing principles (V and VII), demonstrating it is or is not an independent claim. If the analysis concludes the sub-bullet is a composition of V and VII, migrate-out stands and migration-soundness's operational recommendations proceed unaffected. If the analysis concludes it is independent, a subsequent amendment may reconstitute it under path (c), but that is a separate deliberation. The current amendment must show the work before the migrate-out precedent is established. Priority remains P1.

---

#### Recommendation 3: Document the Criterion 1 vs. Criterion 2 distinction in the SIR rationale

- **Original position**: Revise the SIR to correctly classify VI's failure as Criterion 2 (falsifiable scope) rather than Criterion 1 (mechanical verification), and document that Criterion 2 failures map to wording refinement as a first step before migrate-out.
- **Disposition**: Surviving
- **Explanation**:

cross-reference-coherence's cross-review of my work identified this as a "dangerous contradiction" — correctly classifying VI's failure as Criterion 2 might mean wording refinement was a live option the SIR dismissed. The cross-review proposes the resolution: "even if VI fails Criterion 2 rather than Criterion 1, no viable wording refinement exists (the 'drives behavior' qualifier cannot be operationalized by rewriting alone), so the migrate-out conclusion holds independently of the criterion label." (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Dangerous Contradictions, second bullet)

I accept this resolution as the most defensible path — the migrate-out conclusion survives correct criterion identification. But this resolution must appear IN THE SIR. The SIR currently invokes the wrong criterion AND reaches the right outcome; that combination creates a misleading precedent for future amendment authors evaluating judgment-laden qualifiers. They will look to this SIR and see: "Criterion 1 failure → migrate-out" when the correct logic is: "Criterion 2 failure → evaluate wording refinement first → if no viable refinement, migrate-out." The current SIR short-circuits this reasoning chain by mislabeling the failure type.

The recommendation survives because: (a) the criterion misidentification is factual, not interpretive; (b) the correct resolution — "even with Criterion 2 identification, no viable wording refinement exists for 'drives behavior'" — is a stronger justification than the SIR provides; and (c) future amendments encountering judgment-laden qualifiers will need this reasoning chain, not the mislabeled shortcut. migration-soundness did not address this point (scope exclusion). Priority remains P1.

---

#### Recommendation 4: Justify normative downgrade from MUST to SHOULD, or preserve MUST weight in migrated documents

- **Original position**: Either add a SIR paragraph explaining the MUST→SHOULD downgrade, or revise the migrated documents to retain MUST weight for mechanically-applicable sub-rules.
- **Disposition**: Surviving
- **Explanation**:

migration-soundness's cross-review of my work identifies this as a "dangerous contradiction" between ms's "confirmed clean" finding (Rec 6) and my "unjustified bundled change" position. The cross-review itself provides the resolution: "ms's Recommendation 6 should be scoped narrowly: it verified that no inadvertent MUST-strength language slipped into the migrated bullet bodies — a check for unintended MUST usage, not an endorsement of the wholesale MUST→SHOULD policy." (migration-soundness/cross-reviews/removal-rigor-skeptic.md, Dangerous Contradictions, first bullet, resolution paragraph) The cross-review further concedes: "removal-rigor-skeptic's framing is analytically stronger — the gate text does not require normative downgrade."

This is a concession from ms, not a challenge to my position. ms's clean finding and my defect finding are not in the same domain: ms verified absence of accidental MUSTs; I flagged the deliberate wholesale downgrade as requiring separate justification.

cross-reference-coherence's cross-review notes a downstream tension: normalizing CONTRIBUTING.md as a governance destination while also restoring MUST weight would create an unusual operational guidance document carrying constitutional-obligation weight. (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Tensions, first bullet) This concern applies to option (b) of my recommendation. Option (a) — adding SIR justification — is unaffected. The recommendation stands with preference shifted toward option (a): add a SIR paragraph justifying the downgrade. Option (b) remains a fallback only if the SIR cannot produce justification. Priority remains P2.

---

#### Recommendation 5: Add annotation to v2.4.0 SIR's "All three retain ratified status"

- **Original position**: Add a forward-reference annotation to the v2.4.0 SIR block immediately after "All three retain ratified status" noting that VI and X were subsequently removed in v3.0.0 and XVI was remediated via path (c) in v2.6.0.
- **Disposition**: Modified
- **Explanation**:

cross-reference-coherence's cross-review of my work identified the self-contradiction I overlooked: I validated "Audit trails are not mutable" in my Alignment section while simultaneously recommending an annotation to a verbatim-preserved audit-trail block. The cross-review: "The annotation recommendation could conflict with the audit-trail discipline both reviews affirm. cross-reference-coherence explicitly validates 'Audit-trail verbatim preservation (SIR L80-88): the decision to preserve prior SIR comment blocks verbatim rather than retroactively editing them is correct governance discipline'... The v2.4.0 SIR's 'All three retain ratified status' is verbatim preserved content. removal-rigor-skeptic's annotation recommendation adds text to a verbatim-preserved block." (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Tensions, third bullet)

Even though I framed the annotation as a "forward reference, not retroactive revision," this distinction is difficult to maintain as a durable governance rule. Every future annotator will make the same argument — forward references feel categorically different from revision until the volume of annotations makes the preserved blocks unreadable. cross-reference-coherence's alternative (Governance body pointer, their Rec 4) achieves the same navigational result without touching any SIR comment block.

The modified recommendation: withdraw the SIR annotation approach. Replace with support for cross-reference-coherence's Rec 4: add a forward-navigation paragraph to the Governance body text (not inside any SIR block) pointing readers to the v3.0.0 amendment as the canonical migrate-out precedent and noting VI and X as the grandfathered principles remediated under it. This makes VI and X's disposition reachable from Governance body text without modifying the audit trail. Priority P2 maintained; implementation method changed.

---

#### Recommendation 6: Address the comparative-principles asymmetry or document why it does not apply

- **Original position**: Add a paragraph to the SIR rationale explaining why Principles XV, XXIV, and IX survive the same "judgment-laden qualifier" analysis that removed VI and X, preventing the removal precedent from being extended to those principles in future deliberations.
- **Disposition**: Surviving
- **Explanation**:

Neither cross-review contested this finding. migration-soundness's cross-review of my work confirms the finding is uncontested: "the arbiter should treat removal-rigor-skeptic's asymmetry finding as uncontested. migration-soundness's silence on this point is not rebuttal. Recommendation 6... should be adopted without requiring further cross-review resolution." (migration-soundness/cross-reviews/removal-rigor-skeptic.md, Tensions, comparative-principles asymmetry section)

cross-reference-coherence's cross-review of my work notes: "cross-reference-coherence's scope excluded comparative-principles analysis. removal-rigor-skeptic's Rec 6 should be evaluated on its own merits without inference from cross-reference-coherence's silence." (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Tensions, fourth bullet)

Both cross-reviews are consistent: scope exclusion from both, not disagreement on the merits. The recommendation stands on its substantive grounds. Without documented distinction between "judgment-laden but structurally anchored" (XV, XXIV, IX each have a CI-detectable default class even if edge cases require judgment) and "irreducibly judgment-dependent" (VI's "drives behavior" qualifier has no structural default class), this amendment's removal rationale is available as a template for future deliberations targeting XV, XXIV, or IX under identical reasoning. Priority remains P2.

---

#### Recommendation 7: Document why bundling two MAJOR removals into one amendment is appropriate

- **Original position**: Add a sentence to the SIR justifying why both removals were bundled into one deliberation cycle rather than two independent cycles.
- **Disposition**: Surviving
- **Explanation**:

migration-soundness did not address bundling (scope exclusion). cross-reference-coherence's cross-review of my work asks for clarification: "removal-rigor-skeptic should clarify whether Rec 7 is requesting a documentation improvement (add a bundling justification to the existing SIR) or a process question (should the amendment be split)." (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Tensions, fourth bullet)

To answer directly: Recommendation 7 is a documentation improvement only. I am not arguing the amendment should be split. The one-sentence justification I sketched in the original — "both removals are governed by the same analytic framework; the analytical question is identical for both; bundling is appropriate because independent cycles increase process cost without adding analytical rigor" — is all the SIR requires. This closes the bundling question for future amendment authors without requiring structural changes to the amendment itself.

No cross-review challenged the substantive concern. Both noted scope exclusion. The recommendation stands, clarified as documentation only. Priority P3 unchanged.

---

#### Recommendation 8: Extend cross-reference audit methodology to plural forms and prepositional phrases

- **Original position**: Add plural forms ("Principles VI" and "VI and X") to the standard cross-reference audit methodology; document the updated methodology in the SIR. Classified P3.
- **Disposition**: Modified
- **Explanation**:

cross-reference-coherence's cross-review of my work argues for upgrading to P2: "The methodology fix is already implicated in Rec 1 (correct the false SIR claim) and Rec 2 (correct the SIR audit language); it is not a standalone process improvement but a consequence of the same defect. Separating it to P3 would mean the SIR correction is adopted without documenting why the initial audit missed L1589." (cross-reference-coherence/cross-reviews/removal-rigor-skeptic.md, Tensions, priority classification bullet)

This argument is correct. The methodology gap is not a future-proofing concern — it produced the specific defect in the current amendment's SIR. If the SIR is corrected per Rec 1 (acknowledge L1589 was missed, update the claim) without also correcting the methodology description, the updated SIR ends up containing a corrected audit claim whose methodology section still describes the incomplete regex that failed. The audit claim correction and the methodology correction are parts of the same repair.

The modified recommendation: upgrade to P2. The methodology correction should be co-packaged with the Rec 1 SIR correction so that the SIR's updated audit section simultaneously (a) acknowledges L1589 was missed, (b) explains why — the plural form "Principles VI and X" was not in the search terms, and (c) states the corrected methodology for future amendments (include singular, plural, and adjacent-phrase forms of removed principle identifiers).

---

### New Recommendations

- **Establish sequencing dependency: analytical fixes precede operational completion acceptance** (Priority: P1)
  - **Triggered by**: migration-soundness/cross-reviews/removal-rigor-skeptic.md, Tensions section ("Scope division creates different priority orderings" and "Whether the Principle X migrate-out decision was properly grounded"); the same cross-review's treatment of the overall amendment integrity verdict contradiction.
  - **Proposed change**: The synthesis should explicitly declare that the analytical fixes from this review's scope (Recs 1–3, specifically the documented substrate analysis for X per Rec 2 modified) are sequencing gates for migration-soundness's operational completions (ms Recs 1 and 7 — mkdocs.yml nav entry and atomic commit boundary). Specifically: the SIR's documented substrate analysis must confirm migrate-out stands before migration-soundness's "substantially sound" operational verdict is ratified. If the substrate analysis changes X's disposition, ms's document-structural recommendations require revision. If the substrate analysis confirms migrate-out, ms's recommendations proceed unchanged. The two tracks can run in parallel; the analytical track's conclusion must be stable before the operational track is ratified as complete.
  - **Rationale**: migration-soundness's cross-review of my work states: "the arbiter should sequence these: constitutional integrity defects (removal-rigor-skeptic's scope) as gating; operational discoverability fixes (migration-soundness's scope) as non-blocking but required before the distribution surface is complete." Neither cross-review elevated this sequencing requirement to a concrete recommendation. Without an explicit directive in the synthesis, implementers face unclear ordering when two parallel P1 tracks appear to conflict — they will either block each other unnecessarily or proceed in the wrong order, ratifying operational completeness for a document structure that may change. This is a coordination requirement that falls between the scopes of both other reviewers and requires explicit synthesis articulation.

---

### Position Summary

I withdrew one recommendation in substance (Rec 5's SIR annotation approach, replaced by cross-reference-coherence's Governance body pointer), modified three (Rec 1's proposed L1589 replacement text to remove naming of VI and X; Rec 2 narrowed to option (a) only — documented substrate analysis without reconstituting X; Rec 8 upgraded from P3 to P2), and maintained four surviving recommendations (Recs 3, 4, 6, 7) with clarification on scope and implementation preference.

The most significant change was recognizing the self-contradiction my Recommendation 2 option (b) created for Recommendation 1. By offering to retain X via path (c) as an alternative outcome, I undermined the L1589 replacement text I was simultaneously proposing — text that names VI and X as canonical migrate-out examples. cross-reference-coherence's cross-review identified this precisely. The resolution was available in my own original recommendation: option (a) (require documented substrate analysis in the SIR) was always sufficient to discharge the analytical obligation; option (b) (reconstitute X) was an overreach that I included without tracing its downstream consequences for migration-soundness's operational work. Withdrawing option (b) eliminates the self-contradiction, eliminates the cascade conflict with migration-soundness's recommendations, and leaves the analytical obligation intact in its narrower form. The same logical move required the L1589 replacement text to be made more conservative — not naming VI and X, which might change status — matching cross-reference-coherence's version.

My remaining highest-priority recommendation is Recommendation 3: document the Criterion 1 vs. Criterion 2 distinction in the SIR rationale with the explicit conclusion that even if VI fails Criterion 2 (not Criterion 1), no viable wording refinement exists and migrate-out stands independently. This creates the most durable governance precedent. The L1589 repair (Rec 1) addresses the most visible current defect, but its impact is bounded to one sentence in one amendment. The criterion-conflation documentation creates a reusable analytical template: future amendment authors evaluating judgment-laden qualifiers need the complete reasoning chain (Criterion 2 failure → evaluate wording refinement → if no viable refinement, migrate-out), not the current SIR's mislabeled shortcut (Criterion 1 failure → migrate-out). Getting this wrong propagates through every future deliberation that cites v3.0.0 as precedent for handling qualitative judgment calls in constitutional language.