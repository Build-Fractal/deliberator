### Recommendation Dispositions

#### Recommendation 1: Document the no-reuse rule

- **Original position**: Add a "Principle Number Stability" subsection to the Governance section explicitly prohibiting reuse of retired numbers VI and X.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged the substance of this recommendation. The cross-review of my work (body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Diagnostic framing" — Dangerous Contradictions item 3) noted that my P1 findings and body-coherence-skeptic's P1 findings occupy non-overlapping domains and suggested presenting them as parallel P1 tracks rather than competing priorities. That is correct process guidance, not a challenge to the recommendation's substance.

The Safe Agreements section of that same cross-review explicitly corroborates this finding: "The constitution's own documentation principles (IV, XI) are violated by the undocumented gap behavior" — confirmed independently by both reviews from different constitutional provisions. The no-reuse rule belongs in the document, documented in the Governance section as its authoritative home. Its absence is not defensible by the document's own standards (Principle IV: specification text IS the implementation; Principle XI: single source of truth).

One structural note prompted by cross-review: this recommendation and Recommendations 2 and 3 become a mandatory atomic bundle once Recommendation 3 is implemented (see Recommendation 3 modification below). Recommendation 1 cannot land without Recommendations 2, 3, and 6 landing in the same PR.

---

#### Recommendation 2: Add tombstone entries for VI and X

- **Original position**: Add stub entries for VI and X in the numbered sequence, with "[RETIRED]" status and "Number reserved; never reused."
- **Disposition**: Modified
- **Explanation**: The cross-review of my work (body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Dangerous Contradictions," item 1 — "VI's retirement status: 'never reused' vs. 'gate-eligible' — a three-way conflict") correctly identified a self-contradiction between this recommendation and Recommendation 6. My Recommendation 2 says VI and X are "never reused"; my Recommendation 6 said "any future principle assigned those numbers is subject to the full three-criterion gate" — implying assignment remains possible. These positions are mutually exclusive.

The cross-review argued: "The cleaner governance position is 'never reused' (consistent with the RFC/CVE rationale that drives the rest of numbering-skeptic's argument)." I accept this without reservation. My Recommendation 6's gate-eligible language was an error — I was hedging between the RFC model (never reuse) and a softer model (reuse permitted if it passes the gate), and the hedge is incoherent. RFC numbers and CVE numbers are never reused regardless of whether new content would qualify for the position. A number that can be reassigned if the new content is good enough is not a stable identifier; it is a recyclable slot. These are different conceptual models, and my analysis committed to one while my recommendations partially implemented the other.

**Modified recommendation**: The tombstone entries for VI and X should state permanent retirement with no gate path:

```
### VI. [RETIRED]
*Retired. Number permanently reserved; MUST NOT be reused by any future amendment.
This follows RFC and CVE numbering discipline: retired numbers preserve
the validity of all historical citations regardless of whether future
content would otherwise qualify for this position.*

### X. [RETIRED]
*Retired. Number permanently reserved; MUST NOT be reused by any future amendment.*
```

The cross-review also notes (Tensions, "XIX separation of invariants") that if multi-agent isolation content is ever elevated from XIX to a standalone principle, it should receive XXIX (not VI). The tombstone for VI can optionally note this, but the core change is the removal of any gate-eligible ambiguity from both tombstones and from Recommendation 6.

---

#### Recommendation 3: Add principle numbers to Principle II's stable-interfaces list

- **Original position**: Add principle numbers (Roman numerals) to Principle II's stable-interfaces list with a MUST NOT reuse prohibition and a cross-reference to the Governance section.
- **Disposition**: Modified
- **Explanation**: The cross-review of my work (body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Tensions," item 3 — "Principle II's stable-interfaces expansion: atomicity implication") identified a consequence I did not acknowledge: Principle II itself requires that "changing a stable interface requires updating every consumer... in a single atomic change." Adding principle numbers to Principle II's stable-interfaces list immediately triggers this atomicity requirement.

The cross-review states: "numbering-skeptic's seven recommendations become a required atomic bundle the moment Recommendation 3 is implemented — a constraint numbering-skeptic's review does not explicitly acknowledge." This is correct and is not a minor implementation detail. If Recommendation 3 lands without Recommendations 1, 2, and 6, the stable-interface declaration exists but its consumers (no-reuse rule, tombstones, grandfathering correction) have not been updated — which is itself a violation of Principle II's atomicity clause. The recommendation, if accepted, creates an obligation to accept the bundle.

**Modified recommendation**: The recommendation stands — principle numbers should be added to Principle II's stable-interfaces list. But with explicit acknowledgment that this recommendation MUST NOT land in isolation. It requires a single atomic PR that also includes:
- Recommendation 1 (no-reuse rule text in Governance)
- Recommendation 2 (tombstone entries for VI and X)
- Recommendation 4 modified (removal checklist with arbiter-ruling coordination)
- Recommendation 6 modified (grandfathering clause correction, gate-eligible language removed)

This changes the PR structure from seven independent recommendations to one mandatory atomic bundle (Recommendations 1+2+3+4+6) plus two independent follow-ups (Recommendations 5 and 7). Presenting this as seven optional improvements would be a misrepresentation of what implementation actually requires under Principle II.

---

#### Recommendation 4: Extend amendment process with removal checklist

- **Original position**: Add a removal checklist to the Governance Amendments subsection covering tombstone creation, MAJOR version bump, citation audit, and retirement list update.
- **Disposition**: Modified
- **Explanation**: The cross-review of my work (body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Tensions," item 2 — "Arbiter rulings as a constitutional amendment mechanism — addressed in one review, absent in the other") identified that my removal checklist assumes developer-initiated amendments. Three principles (XXIV, XXV, XXVII) were substantively shaped by arbiter rulings without documented amendment records — a mechanism my checklist does not cover. The critical gap the cross-review correctly identifies: if an arbiter ruling removes a principle, my checklist fires for the number-retirement step but body-coherence-skeptic's mechanism fires for the ruling-to-amendment pipeline; neither fires the other. An arbiter-initiated removal falls through both mechanisms.

The cross-review proposed (Dangerous Contradictions, item 2): "When an arbiter ruling removes a principle, the removal checklist... applies in addition to the amendment record requirement." I accept this framing.

**Modified recommendation**: The removal checklist in the Governance Amendments subsection should include a conditional clause: "When the removal originates from an arbiter ruling (see Arbiter Rulings sub-clause), the arbiter amendment record requirement applies in addition to this checklist — both mechanisms fire; neither substitutes for the other." This makes the two governance mechanisms additive rather than parallel. The complete Governance section update — this checklist plus body-coherence-skeptic's arbiter-ruling sub-clause — should be drafted jointly as a coordinated MINOR-class amendment PR. My checklist is necessary but not sufficient; body-coherence-skeptic's arbiter-ruling mechanism addresses the complementary dimension I did not see.

---

#### Recommendation 5: Clarify denominator ambiguity in calibration footnote

- **Original position**: Add a count parenthetical to the Governance calibration footnote: "(The constitution currently has 26 active principles; numbers VI and X are retired.)" Leave the exemplar list unchanged ("fine as-is").
- **Disposition**: Modified
- **Explanation**: The cross-review of my work (body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Dangerous Contradictions," item 2 — "Calibration exemplar list: 'fine as-is' vs. 'replace XII and XIII'") correctly identified that my "fine as-is" assessment of the exemplar list was wrong, and that body-coherence-skeptic's analysis is more precise.

Principle XII contains "The linter SHOULD eventually check for dead variables" — "eventually" is a deferral, not a named verification artifact. Principle XIII contains "The test suite SHOULD verify enum completeness: grep for string literals" — SHOULD-deferred language does not meet the "explicitly named verification artifact" bar the calibration guidance is trying to teach. My original review (Missed Opportunities, item 5) cited these same line references but concluded only that the count parenthetical was needed and the exemplar list was fine. That conclusion was inconsistent with my own evidence. The cross-review exposed that inconsistency clearly: I identified the SHOULD-deferred language as a problem in my own Missed Opportunities section and then did not carry it to a recommendation. That is an analysis error, not a judgment call I should defend.

The cross-review's Safe Agreements section corroborates body-coherence-skeptic's finding at high confidence: "Two reviews with entirely different analytical frameworks independently cited the same two line references (XII L268–269, XIII L288), identified the same linguistic indicator of failure (SHOULD vs. MUST, 'eventually' vs. a concrete check), and reached the same prescriptive conclusion." Independent derivation of identical proposed text is strong corroboration.

**Modified recommendation**: Apply both fixes atomically in a single edit to the calibration footnote — body-coherence-skeptic's exemplar replacement (drop XII and XIII, add XXVIII) and my count parenthetical. The combined text: "(The constitution currently has 26 active principles; numbers VI and X are retired.) When drafting new principles, prefer the structural pattern of principles whose verification artifact is named explicitly (e.g., Principles XXIV, XXVI, XXVIII)." These two fixes address different parts of the same paragraph; there is no trade-off between them. This recommendation can land independently of the atomic bundle (Recommendations 1+2+3+4+6) since it modifies only the Governance calibration footnote.

---

#### Recommendation 6: Bring principle-number stability under the three-criterion gate retroactively as a governance note

- **Original position**: Add a governance note clarifying that the gate governs additions and the retirement policy governs removals, and state that VI and X are "gate-eligible" if future content qualifies.
- **Disposition**: Modified
- **Explanation**: The cross-review of my work (body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Dangerous Contradictions," item 1) correctly identified this recommendation as containing the self-contradiction with Recommendation 2. I cannot simultaneously argue that VI and X are permanently tombstoned (Recommendation 2) and gate-eligible (Recommendation 6). The cross-review is right: "these are not reconcilable by rewording. The cleaner governance position is 'never reused.'"

I withdraw the gate-eligible language entirely. The RFC/CVE discipline that motivates my entire analysis is incompatible with a gate-eligible carve-out. I was hedging, and the hedge destroyed the internal coherence of my recommendation set. Honest withdrawal of the incorrect clause is the only defensible response.

**Modified recommendation**: The governance note should drop all gate-eligible language and commit to the clean position: "Principle number retirement is governed by the Principle Number Stability policy, not the three-criterion gate. The gate governs what is added; the retirement policy governs what is removed and permanently retires the associated number. Numbers VI and X are permanently retired and MUST NOT be reused by any future amendment regardless of whether proposed content would satisfy the gate criteria." This makes the two mechanisms non-overlapping and resolves the contradiction. This note lands as part of the atomic bundle with Recommendations 1+2+3+4.

---

#### Recommendation 7: Extend Principle II's breaking-change definition to include principle-number reuse

- **Original position**: Add explicit language to Principle II stating that reusing a retired principle number is a breaking change.
- **Disposition**: Surviving
- **Explanation**: No cross-review directly challenged this recommendation. The cross-review of my work (body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Tensions," item 3) notes that Principle II's stable-interfaces expansion (Recommendation 3) already implies the breaking-change consequence by making principle numbers stable interfaces. This observation correctly identifies Recommendation 7 as derivable from Recommendation 3, but does not argue it is therefore unnecessary.

Making the breaking-change consequence explicit converts an implicit norm into an enforceable rule that appears in Principle II's own breaking-change section. The implicit consequence ("principle numbers are stable interfaces, therefore reusing one is a breaking change") may be derivable by a careful reader, but the document's own Principle IV demands that invariants be written down, not derivable. A future contributor unfamiliar with the reasoning chain should not need to reconstruct the implication.

Given the atomicity bundle identified in Recommendation 3's modification, this recommendation would logically land as part of the same atomic PR. It remains P3 as originally classified — it is a consequence of Recommendation 3, not a prerequisite for it.

---

### New Recommendations

- **Explicitly bundle the atomic amendment PR** (Priority: P1)
  - **Triggered by**: Cross-review of my work, body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Tensions," item 3 — "Principle II's stable-interfaces expansion: atomicity implication." The cross-review identifies that implementing Recommendation 3 triggers Principle II's own atomicity requirement, converting related recommendations into a mandatory bundle. My original review presented seven independent recommendations and did not acknowledge this constraint.
  - **Proposed change**: The synthesis should explicitly designate Recommendations 1, 2, 3, 4 (modified), 6 (modified), and 7 as a single atomic amendment PR, not as independent recommendations that can be accepted or deferred individually. The amendment PR description should cite Principle II's atomicity clause as the reason for bundling. Recommendation 5 remains separable and can land independently.
  - **Rationale**: Partial implementation is not neutral — it is actively harmful. Accepting Recommendation 3 (add principle numbers to Principle II's stable-interfaces list) without simultaneously accepting Recommendations 1 and 2 (no-reuse rule and tombstones) would leave the stable-interface declaration without its required consumer updates, violating Principle II's atomicity clause in the act of implementing it. The bundling requirement is load-bearing and must appear explicitly in the synthesis output rather than being left to the implementor to infer.

- **Retroactive documentation symmetry for arbiter-originated amendments** (Priority: P2)
  - **Triggered by**: Cross-review of my work, body-coherence-skeptic/cross-reviews/numbering-skeptic.md, "Tensions," item 5 — "Retroactive documentation symmetry: tombstones vs. arbiter ruling records." The cross-review identifies that my tombstone recommendation is retroactive (add records now for historical gaps) while body-coherence-skeptic's arbiter-ruling mechanism is prospective only, leaving XXIV L724–727, XXV L774–775, and XXVII L836–839 without retroactive records even as VI and X receive tombstones.
  - **Proposed change**: Apply retroactive documentation symmetrically. The three arbiter-originated amendments embedded in XXIV, XXV, and XXVII should receive explicit Origin note amendments crediting the 2026-04-25 deliberation ruling as the amendment mechanism — three small edits parallel to the two tombstones for VI and X. If the synthesis chooses the prospective-only approach instead (no tombstones for VI/X, no retroactive Origin note edits), that is also consistent — but the asymmetric approach (tombstones retroactively for numbers, nothing retroactively for arbiter rulings) creates an incomplete historical record.
  - **Rationale**: If the constitution adds tombstones for VI and X, it is declaring that its historical record should be complete. That declaration makes the absence of retroactive records for the three arbiter-originated amendments more conspicuous, not less. The retroactive approach is preferable: the cost is three small Origin note edits plus two tombstones; the benefit is a document whose historical record is internally consistent with its stated governance standards. The cross-review correctly identifies this asymmetry as a coordination requirement neither review originally addressed.

---

### Position Summary

I withdrew the gate-eligible language from Recommendation 6 — a genuine self-contradiction with Recommendation 2 that the cross-review identified correctly and that I cannot defend — and modified five other recommendations: Recommendation 2 (commit unambiguously to "permanently retired, never reused"), Recommendation 3 (acknowledge the atomicity bundle consequence triggered by adding principle numbers to Principle II), Recommendation 4 (incorporate the arbiter-ruling coordination dependency identified by body-coherence-skeptic), Recommendation 5 (accept body-coherence-skeptic's exemplar replacement of XII and XIII, a more precise analysis I should have reached from my own evidence), and Recommendation 6 (drop all gate-eligible language to resolve the self-contradiction). Recommendations 1 and 7 survive unchanged. In total: 0 withdrawn, 5 modified, 2 surviving, 2 new.

The most significant change in my thinking is the atomicity bundle consequence identified in Recommendation 3's modification. I presented seven independent recommendations; the cross-review correctly showed that implementing Recommendation 3 — adding principle numbers to Principle II's stable-interfaces list — triggers Principle II's own atomicity clause and converts the related recommendations into a mandatory bundle. This is not a minor implementation detail. A synthesis that accepts Recommendation 3 while deferring Recommendations 1, 2, or 6 would itself violate Principle II in the act of implementing it. The practical output of my review should be described not as seven improvements but as one non-separable atomic amendment plus two independent follow-ups. The cross-review exposed a structural error in how I packaged my findings, and the modification is substantive.

My highest-priority surviving recommendation is the atomic bundle: document the no-reuse rule, add tombstones, add principle numbers to Principle II's stable-interfaces list, extend the removal checklist to address arbiter-initiated removals, and correct the grandfathering clause — all in a single coordinated amendment PR. This bundle survives because it addresses the core finding with the highest risk if unimplemented: an undocumented governance invariant that a future contributor could violate in good faith, and that Principle II's own atomicity clause demands be addressed all at once. The cross-review process did not weaken this finding; it strengthened it by showing that partial implementation would itself constitute a constitutional violation.