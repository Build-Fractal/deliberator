### Recommendation Dispositions

#### Recommendation 1: Remove Self-Attestation Sentence

- **Original position**: Delete "Each requirement is mechanically verifiable, falsifiable, and distinct from existing principles" (L790) entirely from the principle body, treating the SIR as the sole home for criteria-compliance metadata.
- **Disposition**: Modified
- **Explanation**:

cross-principle-coherence's cross-review (Dangerous Contradiction 1: "Criteria compliance content in the principle body: add structured Verification block vs. remove meta-content entirely") identifies that my removal recommendation and CPC's structured-Verification-block recommendation embody "opposite architectural principles about where criteria compliance evidence belongs." CPC argues the principle body must be self-contained for future readers encountering the constitution without SIR comment blocks. gate-skeptic's cross-review (Dangerous Contradiction 3: "Self-attestation sentence: mandatory removal vs. conditional retention") does not independently flag L790 for removal and frames retention as a live possibility via its Recommendation 8 temporal-qualifier path — though gate-skeptic's cross-review also concludes "wording-precision's position is more thoroughly argued" and that gate-skeptic should yield on removal.

Both cross-reviews confirm in their respective Safe Agreements that the current sentence is scope-exceeding and unacceptable in its current form. The disagreement is about what, if anything, replaces it — not about whether the sentence survives.

My original review treated removal and the structured-block option as mutually exclusive under a SIR-vs-body architecture question. That framing was too rigid. CPC's cross-review correctly observes that the gate's Extension blocks paragraph already names `Verification:` blocks as a sanctioned body-content type, formally distinct from informal self-attestation prose in a normative paragraph. The synthesis-level question of whether to add a structured block (CPC Rec 4) is orthogonal to removing the informal sentence.

**Modified recommendation**: The informal, present-tense self-attestation sentence in its current form must be removed regardless of what replaces it. I withdraw the absolute architectural claim that "the SIR is the established home for this content" — structured `Verification:` blocks in the principle body are a constitutionally sanctioned format. If the synthesis elects to add such a block (CPC Rec 4), that is compatible with and complementary to removing the informal sentence. The removal of the informal sentence is the unconditional prerequisite; a structured block is the synthesis's option, not a contradiction of it.

---

#### Recommendation 2: Replace "no surprise math" with Conditional Gloss

- **Original position**: Replace "no surprise math" with a conditional gloss such as "assembly is reproducible given the same inputs (no structural drift after pinning)" or "assembly is stable given pinned parameters."
- **Disposition**: Modified
- **Explanation**:

gate-skeptic's cross-review raises two challenges. First, Dangerous Contradiction 1 ("'no surprise math': Delete vs. Replace") argues for deletion rather than replacement, on the grounds that the structural requirement for shape determinism already conveys the claim and any interpretive gloss risks reintroducing reader-relative language. Second, Dangerous Contradiction 2 (Priority divergence) identifies that gate-skeptic rates the standalone "no surprise math" cut as P3 while rating the full paragraph-level fix P1 — a sequencing risk where my P1 treatment of this item could be neutralized if it is absorbed into a wholesale paragraph rewrite without verifying that the replacement text also passes the accuracy screen.

gate-skeptic's Tension 5 ("Treatment of 'no surprise math': conditional replacement vs. full deletion") and my own cross-review of gate-skeptic (Safe Agreement on "no surprise math") together establish the synthesis constraint: any replacement must satisfy both gate-skeptic's Criterion 1 screen (no reader-relative predicates) AND my accuracy screen (correctly scoped to post-pinning assembly, not falsely implying no mathematical variation across invocations). My proposed replacements in the original review — "no structural drift after pinning," "assembly is stable given pinned parameters" — were not evaluated against Criterion 1. "Structural drift" is plausibly reader-relative; "stable" lacks a mechanical referent without elaboration.

In my cross-review of gate-skeptic (Dangerous Contradiction 1 suggested resolution), I proposed "assembly is deterministic given the same template and pinned parameters" as the candidate that satisfies both filters: "template" (a named artifact with an ID per spec 013) and "pinned parameter set" (a specific `objective.yml` file) are mechanically defined inputs, making the claim machine-checkable; "deterministic given the same… pinned parameters" correctly scopes the guarantee to post-pinning assembly without implying cross-run invariance.

**Modified recommendation**: Replace "no surprise math" with "assembly is deterministic given the same template and pinned parameters." Replace the primary gloss "template shapes are stable" with "assembly structure is deterministic" (the "template shapes are stable" problem is addressed in Rec 3). Priority remains P1. The decision to replace rather than delete is maintained: the design-intent paragraph's explanatory function is legitimate; the specific gloss is wrong, not the category. Both reviews' Safe Agreement confirms removal is settled; the synthesis should use the Criterion 1-compliant replacement text, not deletion with no substitute.

---

#### Recommendation 3: Fix "template shapes are stable" to Avoid Template-Mutability Misreading

- **Original position**: Replace "template shapes are stable" in the opening paragraph (L788) with "assembly structure is deterministic given the same template and pinned parameters."
- **Disposition**: Modified
- **Explanation**:

CPC's cross-review (Tension — "'Shape' terminology fix location — design-intent paragraph vs. v2.3.2 clarification block" and Safe Agreement — "'Shape' should be replaced with 'structure' throughout Principle XVI's body") identifies that both WP and CPC independently recommend "shape" → "structure" replacements but at different locations: WP targets the opening paragraph; CPC targets the v2.3.2 clarification block ("assembled objective function's *shape* (parameter names, template selection, gap-identifier set)"). CPC correctly notes that applying only one fix leaves "shape" terminology inconsistent within XVI: corrected in one section, uncorrected in another.

CPC's cross-review of WP (Dangerous Contradiction 3: "Scope of the 'unchanged body'") flags a scope tension: the v2.3.2 clarification block is declared UNCHANGED in the amendment's SIR scope statement. Modifying it under v2.6.0 ratification expands the stated amendment scope. CPC suggests either commissioning a targeted audit of the v2.3.2 change, or bundling both "shape" corrections into a separate follow-up amendment with full dual-perspective review.

**Modified recommendation**: Apply "template shapes are stable" → "assembly structure is deterministic given the same template and pinned parameters" to the opening paragraph within the current v2.6.0 scope (this is within the declared rewrite boundary). For the v2.3.2 clarification block's "assembled objective function's *shape*" language: the synthesis must decide between two options before ratification. Option A: expand v2.6.0's scope to include the v2.3.2 block fix, update the SIR scope statement accordingly, and apply "shape" → "structure" as a single coordinated pass. Option B: defer the v2.3.2 block fix to a follow-up PATCH with a scope statement that acknowledges both instances of "shape" usage and the IX cross-principle collision. Do not ratify with the two instances of "shape" corrected in only one location; post-ratification inconsistency within XVI's body is worse than deferred correction.

---

#### Recommendation 4: Add Enforcement and Falsification Sub-Bullets for Shape Determinism and Plain-Language Pairing

- **Original position**: Add parallel Enforcement and Falsification sub-bullets to the v2.3.2 Clarification block for requirements (2) and (3), conditioned on retention of the self-attestation sentence at L790. If L790 is removed, priority drops to P3.
- **Disposition**: Modified
- **Explanation**:

Two challenges in CPC's cross-review require me to correct genuine errors in the original recommendation.

First, CPC (Dangerous Contradiction 2: "Priority assignment for the plain-language pairing enforcement gap") argues that conditioning this recommendation on L790's adoption status was wrong. "The XV↔XVI conflict is operational, not documentary. WP Rec 4's priority should not be downgraded on the basis that WP Rec 1 is adopted; the body still needs enforcement evidence even if the self-attestation sentence is removed." This is correct. The enforcement chain for plain-language pairing and shape determinism is absent from the principle body regardless of whether any sentence asserts verifiability. My conditionality logic was: "if L790 is removed, the body no longer asserts 'mechanically verifiable,' so the absence of enforcement sub-bullets becomes less problematic." That reasoning was wrong — the enforcement chain's absence is a defect in its own right, not a dependent variable.

Second, CPC (Dangerous Contradiction 3: "XVI's authority to MUST-require plugin output format: uncontested vs. an ungrounded assumption") argues that my Rec 4's proposed Falsification sub-bullet — "A future PR that adds a numerical recommendation field without an adjacent plain-language explanation field violates this principle" — implicitly assigns core-gate consequences to a XVI violation. Plugin recommendations are plugin output; XV governs enforcement over plugin output via warn-and-continue. A Falsification sub-bullet that makes the violation belong to XVI without cross-referencing XV's enforcement machinery is operationally misleading.

gate-skeptic's cross-review (Tension — enforcement gap) adds that body sub-bullets should be complemented by filed tracking tickets so external accountability exists alongside in-body documentation.

**Modified recommendation**: Add Enforcement and Falsification sub-bullets for shape determinism and plain-language pairing as P2, unconditionally (priority does not depend on L790 adoption status). The plain-language pairing Falsification sub-bullet must be scoped: "A future PR that adds a numerical recommendation field without an adjacent plain-language explanation field violates this principle's output-pairing requirement; the violation is handled as malformed plugin output under Principle XV's warn-and-continue enforcement model." File GitHub issues for the parity test and schema lint enforcement artifacts before ratification; cite the issue numbers in the sub-bullets. CPC's enforce-mode cross-reference to XV (addressed in the new recommendation below) must be added before or alongside these sub-bullets, as it is the prerequisite that gives the scoped Falsification sub-bullet its constitutional grounding.

---

#### Recommendation 5: Clarify "auditable" in the Parameter-Pinning Gloss

- **Original position**: Replace "(auditable)" with "(persisted to `objective.yml`, not re-resolved)" — rated P3 as a standalone orientation improvement.
- **Disposition**: Modified
- **Explanation**:

gate-skeptic's cross-review (Dangerous Contradiction 4: "Priority of 'auditable' correction") directly challenges the P3 priority: "Gate-skeptic's priority is better calibrated to the constitutional stakes. The question of whether 'auditable' passes Criterion 1 is not a low-stakes clarity question — it is the same category of question the amendment was created to resolve for 'user MUST understand.'" gate-skeptic's argument applies with full force: "auditable" is a reader-relative predicate. Whether a process is "auditable" requires a reader to assess rather than a machine to check. An automated CI check cannot flag a missing "auditability" property; it can flag a missing `SourceProvenance.filled_by` entry in `objective.yml`.

Both cross-reviews' Safe Agreements confirm the fix direction — gate-skeptic's text "(persisted to `objective.yml` via `SourceProvenance.filled_by`)" and my text "(persisted to `objective.yml`, not re-resolved)" target the same mechanical referent. gate-skeptic's formulation is more precise: it names the specific field (`SourceProvenance.filled_by`) that a checking tool would inspect, not just the file. This directly satisfies Criterion 1 in a way my formulation does not.

My P3 rating was wrong because I applied an "orientation adequacy" standard to this gloss rather than the constitutional Criterion 1 standard. The design-intent paragraph's glosses are not mere orientation aids — they are part of the principle's plain-language exposition of mechanically verifiable requirements. The standard for language in that paragraph is the same as for the requirements themselves.

**Modified recommendation**: Upgrade priority to P1. Replace "(auditable)" with "(persisted to `objective.yml` via `SourceProvenance.filled_by`)" — adopting gate-skeptic's more precise formulation. This satisfies Criterion 1 (the field is mechanically inspectable), matches the body's own reference at L860-862, and is no less concise than the original gloss.

---

#### Recommendation 6: Update the SIR Scope Statement to Accurately Reflect the Net-New Sentence

- **Original position**: If the self-attestation sentence is retained, update the SIR scope statement to acknowledge it as a net-new addition rather than a "restructuring" of prior content.
- **Disposition**: Modified
- **Explanation**:

CPC's cross-review (Tension — "SIR scope statement vs. gate text as governance documentation targets") correctly identifies that my Rec 6 is a transitional, instance-level fix while CPC's Rec 2 — adding gate text explicitly covering headline rewrites of grandfathered principles as a category — is the durable structural fix that resolves the governance gap unconditionally. CPC notes: "WP Rec 6 is made redundant by CPC Rec 2 if both are adopted together."

The logic of Rec 6 was: if the sentence is net-new and the SIR claims only "restructuring," the scope statement is factually inaccurate, which future auditors will find. That concern is valid. But its operative window is narrow: Rec 6 applies only if (a) Rec 1 is not adopted (sentence is retained) AND (b) CPC Rec 2 is not adopted (no gate text update). In my recommended path, Rec 1 removes the sentence, making there nothing net-new for the SIR to acknowledge. If the synthesis also pursues CPC Rec 2, the governance gap is addressed at the structural level regardless.

**Modified recommendation**: Demote to P3 contingent. This recommendation is moot if either Rec 1 (sentence removal) or CPC Rec 2 (gate text update) is adopted. It applies only as a fallback governance patch when both primary fixes are declined: in that case, the SIR scope statement must add: "one net-new sentence added to the opening paragraph asserting criteria compliance status; not a restructuring of prior content." The synthesis should treat CPC Rec 2 as the independent priority governance fix and this recommendation as a residual safeguard.

---

#### Recommendation 7: Consider Whether the Design-Intent Paragraph Warrants Normative Status

- **Original position**: Evaluate whether the design-intent paragraph belongs in the Origin note rather than the principle body, since constitutional principle bodies typically contain normative requirements while the paragraph contains design-rationale prose; evaluate after L790 is removed.
- **Disposition**: Surviving
- **Explanation**:

gate-skeptic's cross-review (Tension — "Precedent management: path (c) governance definition vs. design-intent paragraph normative status") correctly observes that its own concern is inter-principle in scope — the ungovernanced path (c) precedent for all grandfathered principles — while my Rec 7 is intra-principle in scope — the paragraph's status within XVI's body. gate-skeptic treats its concern as higher constitutional impact and suggests both be pursued, with the inter-principle concern given priority. This is not a challenge to the substance of Rec 7; it is a prioritization note.

No cross-review argued that the paragraph's ambiguous normative status is acceptable or that it should stay where it is. CPC's safe agreement confirms the amendment's constitutional logic is sound and defects are localized to the opening paragraph's prose quality — which includes the question of whether design-rationale prose belongs there.

The concern remains valid and not captured by any other recommendation: if the design-intent paragraph survives in its current location after the P1 fixes, future interpreters may apply "is achieved through these structural requirements" as a normative constraint meaning the structural requirements must demonstrably achieve user understanding. This resurrects the epistemically unverifiable claim in a new form — as a purpose clause whose satisfaction is not mechanically checkable. The Origin note is the established constitutional location for design-rationale prose (XXVIII's origin note demonstrates the pattern); the body is the established location for normative requirements.

**Affirmed at P3.** No cross-review challenged this recommendation's substance. The synthesis should evaluate the design-intent paragraph's status after applying the P1 wording fixes — if the remaining prose (stripped of L790 and with accurate glosses) reads as normative text rather than explanatory commentary, move it to the Origin note.

---

#### Recommendation 8: Verify Present-Tense "is mechanically verifiable" Against Evidence-Pending Status

- **Original position**: If the self-attestation sentence is retained, add a temporal qualifier ("each requirement is designed to be mechanically verifiable") to resolve the internal inconsistency with the body's own "evidence-pending" acknowledgment.
- **Disposition**: Surviving
- **Explanation**:

Both cross-reviews independently confirmed the internal inconsistency. CPC's cross-review of WP (Dangerous Contradiction 2, third bullet in gate-skeptic's cross-review of WP, and Safe Agreements in both reviews) treat this as a robustly evidenced finding: L790's present-tense "is mechanically verifiable" conflicts with L872-876's honest "evidence-pending" and "filed as a follow-up" language for the very same requirements the sentence claims are presently verifiable.

gate-skeptic's cross-review (Dangerous Contradiction 3) suggests that gate-skeptic should yield to WP's removal recommendation (Rec 1), making Rec 8 the fallback rather than the primary path. No cross-review argued the inconsistency is acceptable as-is; the disagreement was only about whether to remove the sentence or qualify it.

Rec 8's status is correctly ordered as fallback: Rec 1 (removal) is the unconditional first choice; Rec 8 (temporal qualifier) is the second choice if the synthesis declines Rec 1. Both choices resolve the internal inconsistency. The synthesis should be presented with both explicitly, with Rec 1 marked as the cleaner resolution because a temporal qualifier still leaves a compliance-metadata sentence in the body, while removal eliminates both the precedent concern and the consistency problem simultaneously.

**Affirmed at P2 as a conditional fallback.** Operative only if Rec 1 is declined. If Rec 1 is adopted, Rec 8 is moot and should not be applied.

---

### New Recommendations

- **Add enforce-mode cross-reference to Principle XV for the plain-language pairing requirement** (Priority: P1)
  - **Triggered by**: CPC's cross-review of WP (Dangerous Contradiction 2: "Priority assignment for the plain-language pairing enforcement gap"; Dangerous Contradiction 3: "XVI's authority to MUST-require plugin output format: uncontested vs. an ungrounded assumption"). CPC identifies that XVI's plain-language pairing MUST, without an enforce-mode clause, creates a silent operational conflict with Principle XV's warn-and-continue model: "a future implementor adds schema-level rejection of non-paired plugin output, triggering a core execution failure — a direct XV violation — while citing XVI's MUST as justification."
  - **Proposed change**: Add an enforce-mode clause explicitly to the plain-language output pairing requirement in the principle body — either as a sentence within the third headline requirement or as a clarifying sub-bullet in the 3-stage pipeline block's third bullet: "Plain-language pairing violations are handled as malformed plugin output per Principle XV (Plugin Isolation) warn-and-continue enforcement; they MUST NOT gate core execution." This is distinct from the Enforcement and Falsification sub-bullets in modified Rec 4, which document how violations are detected. This clause specifies what happens operationally when a violation is detected: execution continues, a warning is emitted, plugin output is flagged as malformed. Without this clause, XVI's MUST specifies a requirement but leaves its enforcement consequence undefined within XVI's text; XV's enforcement consequence can only be inferred by cross-referencing XV.
  - **Rationale**: Principle XV (L490-510) is explicit: "Plugin failure MUST NOT block core execution — warnings only." The plain-language pairing requirement governs plugin recommendation output. XVI's MUST without an enforce-mode clause creates an interpretive gap: a reader of XVI in isolation cannot determine whether a pairing violation blocks execution or triggers a warning. XV's warn-and-continue model resolves the gap, but only if the reader cross-references XV unprompted. The enforce-mode clause makes XVI self-contained on the enforcement consequence and eliminates the XV↔XVI operational conflict CPC identifies. This is not a new normative requirement — XV's warn-and-continue already governs — it is making the consequence explicit within XVI's text so the principle is self-sufficient.

---

### Position Summary

Of my original eight recommendations, I withdrew none, modified six (Recs 1, 2, 3, 4, 5, 6), and retained two unchanged (Recs 7, 8). I added one new recommendation. The modifications were substantive in three cases: Rec 5's priority upgrade from P3 to P1 corrects a genuine analytical error; Rec 4's removal of conditionality corrects a logical error in how I framed the enforcement gap; and Rec 1's architectural concession — withdrawing the absolute SIR-is-the-only-home claim — addresses a real gap in my original framing without abandoning the core removal recommendation.

The most significant change in my thinking was prompted by gate-skeptic's cross-review applying the Criterion 1 frame uniformly to all language in the design-intent paragraph. I treated "auditable" as a P3 orientation problem when it is a P1 constitutional defect: a reader-relative predicate of the same class as the "user understanding" claim the amendment was designed to retire. This was an inconsistency in my own analysis — I applied Criterion 1 rigorously to the self-attestation sentence and to "no surprise math" but somehow exempted "auditable" on the grounds that the body provides context at L860-862. That exemption was wrong; the body providing context is precisely the problem for a standalone plain-language gloss. gate-skeptic also prompted me to verify proposed replacements against Criterion 1, which produced the cleaner candidate "assembly is deterministic given the same template and pinned parameters" — a more precise formulation than my original proposed glosses. Regarding "no bare numbers" (the third design-intent gloss): gate-skeptic endorses it as genuinely mechanical, and I concur after evaluating it against both accuracy and Criterion 1 screens. Every plugin recommendation includes numerical outputs; the presence of an adjacent string explanation field is structurally checkable; "no bare numbers" accurately glosses the requirement without overpromising or introducing a reader-relative predicate. It should be retained.

My highest-priority recommendations entering synthesis are Recs 2 and 5 (the "no surprise math" and "auditable" replacements) and the new enforce-mode recommendation. Both reviews independently confirm from different analytical angles — Criterion 1 failure and body-consistency failure — that the design-intent paragraph's glosses are the amendment's primary problem zone. The self-attestation sentence (Rec 1) is also P1 and must be resolved, but the glosses are independently defective even if the sentence is removed. Addressing the three Criterion 1 failures in the design-intent paragraph is the minimum work required to close the same gap the amendment was designed to close in the headline.