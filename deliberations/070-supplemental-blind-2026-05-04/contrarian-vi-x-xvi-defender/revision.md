### Recommendation Dispositions

#### Recommendation 1: Retain Principle VI with directory-resolution clarification

- **Original position**: Retain VI in the constitution with a Clarification block specifying that CI linting against architectural directories satisfies Criterion 1 and that "'artifact drives behavior' resolves to membership in those directories by convention."
- **Disposition**: Modified
- **Explanation**:

Gate-faithfulness's cross-review (Dangerous Contradictions, "VI migration verdict: correct vs. incorrectly decided") supplied the principled distinction my conditional verdict required. The distinction: IX's judgment-laden "prefer" qualifier accompanies a dense block of entirely mechanical MUST requirements — all signatures must have type annotations, all data structures must use Pydantic models, StrEnum for closed behavioral choices, etc. VI's scope-qualifier "when the artifact drives behavior" is the sole trigger for VI's sole prescription, with no accompanying mechanical MUST block. This is a genuine and articulable distinction.

My conditional — "incorrectly decided unless the principled distinction is supplied" — is therefore conditionally satisfied. The distinction now exists in the deliberation record. The migration verdict stands; what I framed as a retention argument becomes a documentation-adequacy argument: the migration was not wrongly decided, but it was inadequately documented because the distinction was never stated in the original SIR.

Gate-faithfulness (Dangerous Contradictions, "MUST→SHOULD Characterization") also correctly identifies a factual error in my original review. I wrote that "the principle-level obligation is encoded as MUST." This is not textually grounded: VI uses SHOULD at line 353 — "it SHOULD be a script, config, or structured data." There is no MUST to reduce. I withdraw the MUST→SHOULD concern entirely as applied to VI.

CPC's cross-review (Dangerous Contradictions, "VI: Full constitutional retention versus split-migrate along XVII taxonomy") correctly identifies that my retention recommendation and CPC's split-migrate routing recommendation are mutually exclusive. Given that the principled distinction has been articulated and the migration stands, I yield the retention position. CPC's XVII-routing analysis becomes the operative remediation for the migration's routing quality.

**New form**: Accept that VI's migration is correctly decided, subject to the condition that the v3.0.0 SIR explicitly documents the IX/VI distinction (IX's judgment-laden qualifier is accompanied by mechanical MUST requirements; VI's is not). Carry the directory-resolution lint into the receiving operational guidance document as a partial enforcement mechanism for the most common violation pattern. Do not advocate for constitutional retention.

---

#### Recommendation 2: Retain Principle X under renamed headline "Output Structure Invariants"

- **Original position**: Retain X in the constitution under a renamed headline, elevating the four sub-bullets as operative content, and adding an explicit Verification block with named CI checks.
- **Disposition**: Modified
- **Explanation**:

Gate-faithfulness (Tensions, "Sub-bullet independence as Criterion 1 rescue for X vs. headline-level framing as principle identity") raises a genuine ambiguity in the gate's Criterion 1 text. Gate-faithfulness argues the headline prescription "Output MUST be clean, readable, and unsurprising" is the operative requirement, and the sub-bullets are supporting illustrations rather than independent operative claims. Under that reading, one verifiable sub-bullet does not rescue the principle from a Criterion 1 failure rooted in the headline. I argued "at least one form" is satisfied by one verifiable sub-bullet. The gate text does not resolve which granularity applies.

Gate-faithfulness's Recommendation 2 points toward a productive resolution: evaluate the refactored text (not the original X framing) against the gate criteria. This is what path-(c) was designed for. However, my original Recommendation 2 named the refactored headline "Output Structure Invariants" without specifying whether that headline itself would be mechanical. "Output Structure Invariants" is still a summary label, not a verifiable claim. The headline must become a mechanical assertion, not merely a more accurate description.

CPC's cross-review (Tensions, "X's sub-bullet 3 and Principle V") raises an XI concern I had not addressed: X's error-handling sub-bullet ("Errors should never pass silently — warnings are emitted for malformed output, missing documents, and edge cases") may duplicate V's third bullet ("Output validation emits warnings for malformed output but does NOT block file writes"). If the two are genuinely identical in scope, retaining both in the constitution creates an XI violation regardless of whether X is retained or refactored. CPC notes that X's bullet adds "missing documents" and "edge cases" — if that addition constitutes a genuine specialization rather than a restatement, the XI concern evaporates. This must be resolved before sub-bullet 3 can be included in any retained version of X.

**New form**: Advocate for path-(c) refactoring with three conditions that must be satisfied before the refactored X can be treated as gate-passing:

(a) The headline must be a mechanical assertion, not a rhetorical one. A candidate: "Output tree follows predictable flat structure: `summary/final.md` as starting point; agent output one level deep." This claim is directly verifiable by parity test and path-depth lint, satisfying Criterion 1 on its own terms rather than relying on a sub-bullet to rescue a non-mechanical headline.

(b) Sub-bullet 3 (error-handling) must be verified as a genuine specialization of V's third bullet before being included in the refactored principle. If it adds "missing documents" and "edge cases" that V does not cover, it is a specialization and may remain. If it merely restates V's output-validation requirement in different vocabulary, it should be deleted — not migrated — to avoid the XI violation.

(c) A Verification block must name specific CI checks for at least the `summary/final.md` parity test and the path-depth lint, satisfying Criterion 1's "concrete enough to sketch in one paragraph" requirement.

If these three conditions are satisfied, the refactored X passes the gate and should be retained. If they cannot be satisfied without further amendments, migration proceeds — but with the `summary/final.md` constraint carried as a MUST-level requirement in the receiving document, per the cross-review safe agreement that this sub-requirement must survive at full normative force regardless of migration outcome.

---

#### Recommendation 3: Record cycle-1 XVI refactor as defensive improvement, not gate-required correction

- **Original position**: Amend the cycle-1 governance log to characterize the path-(c) headline refactor as a defensive quality improvement rather than a gate-required correction, since the pre-cycle-1 body's three numbered rules already independently satisfied Criterion 2.
- **Disposition**: Surviving
- **Explanation**:

Gate-faithfulness (Safe Agreements, "XVI's path-(c) disposition was substantively correct and the plain-language sub-bullet is the sole migrated clause") confirms path-(c) was the right outcome for XVI and identifies the plain-language clause at lines 694–698 as the correct and sole migration target. Gate-faithfulness does not contest my claim that the pre-refactor body's numbered rules were already Criterion-2-compliant. The non-contestation is implicit concession: the finding stands unchallenged.

CPC's cross-review (Dangerous Contradictions, "XVI status") identifies a tension between CPC's grandfathered-with-partial-upgrade annotation and my governance log correction, but also provides the resolution: "The governance log can record both findings: the three numbered rules were Criterion-2-compliant before the cycle-1 refactor; the plain-language explanation clause was a genuine Criterion 2 failure that remains partially unresolved even after the refactor." These are not contradictory — they address different sub-elements and different points in XVI's history.

The composite governance log entry my Recommendation 3 should produce: (a) the pre-cycle-1 body's three numbered rules (within-run determinism, cross-run reproducibility, LLM re-invocation prohibition) were Criterion-2-compliant before cycle 1; (b) the plain-language explanation requirement was and remains a genuine Criterion 2 failure not addressed by the cycle-1 headline refactor; (c) the v2.3.2 extension further strengthened Criterion 1 compliance via `SourceProvenance.filled_by` audit hooks and the explicit falsification clause; (d) the cycle-1 headline refactor improved readability as a constitutional statement but was not gate-required, since the body already carried the falsifiable claims.

No cross-review contested the core finding. The recommendation survives.

---

#### Recommendation 4: Require principled-distinction documentation for Criterion 2 judgment-call migrations

- **Original position**: Add to the gate text a requirement that when a migration rests on the "judgment call" ground, the migration spec must explicitly address whether analogous qualifiers in retained principles pass by a different standard, and if so, state the principled distinction.
- **Disposition**: Surviving
- **Explanation**:

Both cross-reviews converge on this recommendation and neither challenges it. Gate-faithfulness (Safe Agreements, "IX/XV/XXIV Asymmetry Must Be Explicitly Documented in the v3.0.0 SIR") confirms the asymmetry argument must be documented and provides the specific substantive content for the Asymmetry Resolution section. CPC has an independent analogous recommendation and describes the two as convergent.

The cross-review process has, in fact, demonstrated why this recommendation matters: gate-faithfulness articulated the IX/VI distinction in a cross-review that would not have been produced under the original deliberation process. The distinction is now in the deliberation record, but only by accident — because a cross-review was commissioned for this supplemental deliberation. Recommendation 4 closes the structural gap that made this accidental: it makes the principled-distinction analysis mandatory in the migration SIR itself rather than depending on a subsequent deliberation to supply it retroactively.

The recommendation survives at P1 priority, strengthened by cross-review agreement.

---

#### Recommendation 5: Validate cycle 2A's document scope before citing its findings as gate assessment

- **Original position**: Before closing the spec 070 migration record, confirm whether cycle 2A reviewed the pre-migration or post-migration document. If post-migration, annotate the cycle 2A findings as a consistency check on the post-migration document rather than an independent gate assessment of whether removal was warranted.
- **Disposition**: Surviving
- **Explanation**:

Neither cross-review contests the factual claim that cycle 2A reviewed a post-migration document, nor disputes that a gate assessment must be performed on a document containing the principles being assessed. CPC (Safe Agreements, "Contrarian audit-trail record required by AC #5") confirms the AC #5 mandate was procedurally unmet by prior deliberations. Gate-faithfulness (Tensions, "Cycle 2A Procedural Validity") does not dispute the procedural objection — it argues only that the merits-based defense independently establishes the verdict, which is a compatible position.

The two framings can coexist: cycle 2A's findings are valid as a consistency check on the post-migration document's internal coherence but cannot serve as the primary gate assessment of whether removal was warranted, because the principles being assessed were absent from the document reviewed. The present deliberation constitutes the retroactive contrarian assessment that AC #5 required. The governance log should acknowledge this explicitly rather than allowing cycle 2A to be retroactively characterized as satisfying a mandate it structurally could not satisfy.

The recommendation survives.

---

#### Recommendation 6: Audit normative strength in all operational guidance migrations

- **Original position**: All migrations from the constitution to operational guidance must include a normative-strength analysis confirming whether MUST obligations in the migrated principle are preserved, intentionally demoted, or inadvertently weakened.
- **Disposition**: Modified
- **Explanation**:

Gate-faithfulness (Dangerous Contradictions, "MUST→SHOULD Characterization of VI's Normative Strength") correctly identifies a factual error in the VI-specific application of this recommendation. VI uses SHOULD at line 353. My claim that "the principle-level obligation is encoded as MUST" is not textually grounded. Gate-faithfulness is right that the VI-specific application of Recommendation 6 rests on a false premise and should be redirected.

Gate-faithfulness further suggests redirecting the normative-strength concern to X, where MUST language does appear in the headline: "Output MUST be clean, readable, and unsurprising." This is the correct application target. If X migrates in its original form, the headline's MUST must either be preserved as MUST in the receiving document or the demotion must be explicitly justified.

CPC (Tensions, "Normative-strength preservation") notes the normative-strength test and the XVII-taxonomy test are jointly necessary conditions for migration validity. A migration that routes correctly under XVII but inadvertently reduces MUST to SHOULD is still defective. The general process control is sound; only the VI-specific application was wrong.

**New form**: Retain the general requirement: all migration SIRs must include a normative-strength analysis for each MUST obligation in the migrated principle, confirming whether the MUST is preserved, intentionally demoted with justification, or inadvertently weakened. Remove the VI-specific application as factually incorrect — VI uses SHOULD, not MUST, so there is no MUST to track for VI. Apply to X specifically: "Output MUST be clean, readable, and unsurprising" is a MUST-level headline claim; the migration SIR for X must address this MUST explicitly. The general process control remains P2 for all future migrations.

---

#### Recommendation 7: Enter contrarian findings in governance log regardless of migration outcome

- **Original position**: Enter a summary of the contrarian arguments in CONSTITUTIONAL_CONVERSATIONS.md under the spec 070 implementation entry, with each principle's strongest pass-argument and strongest counter-argument stated, clearly labeled as the contrarian assessment AC #5 required.
- **Disposition**: Surviving
- **Explanation**:

Both cross-reviews independently support this recommendation. Gate-faithfulness frames the motivation as defensive — preempt future reversal arguments by addressing the asymmetry challenge explicitly in the record. I frame it as due-process — the spec required the assessment and neither prior deliberation satisfied it. These framings are compatible and both support the same action.

CPC (Safe Agreements, "Contrarian audit-trail record required by AC #5") confirms the mandate was procedurally unmet and that the present deliberation remedies the gap. The substantive content of the governance log entry is now well-specified: gate-faithfulness has provided the IX/VI distinction; my review has provided the strongest pass-arguments for each principle; the cross-reviews have identified where the pass-arguments hold and where they yield. All of this material belongs in the governance log entry as the complete record of the contrarian assessment.

No cross-review challenged this recommendation. It survives.

---

#### Recommendation 8: Clarify Criterion 2 evaluation scope as headline-plus-body

- **Original position**: Add a clarifying sentence to Criterion 2 stating that the criterion applies to the principle as a whole — headline and body together — and that headline ambiguity resolved by a specific body does not constitute a Criterion 2 failure when the body provides the falsifiable claim.
- **Disposition**: Surviving
- **Explanation**:

CPC's cross-review (Tensions, "Constitutional gate clarification: Criterion 2 scope versus migration SIR process requirement") identifies my Recommendation 8 and CPC's XVII-classification table requirement as addressing complementary intervention points: my constitutional text amendment prevents misapplication at gate-assessment time (upstream); CPC's table prevents routing errors at migration-execution time (downstream). These are additive, not competing. Both should be adopted.

Gate-faithfulness's safe agreement that XVI's plain-language sub-bullet is the correct sole migration target implicitly supports the headline-plus-body reading: the gate correctly identified the sub-bullet (body element) as the failure, not the headline. This is consistent with evaluating the body as the carrier of falsifiable claims.

The clarification remains necessary even after accepting that the IX/VI distinction is articulable. The retained corpus (IX, XII, XIII, XVII, and others) consistently follows headline-summarizes/body-operationalizes convention. Without explicit Criterion 2 text confirming this, future reviewers may apply headline-only evaluation to principles whose bodies carry the falsifiable claims, producing false negatives for correctly-structured principles. No cross-review challenged this recommendation. It survives.

---

### New Recommendations

- **Require XVII-classification table in migration SIRs** (Priority: P2)
  - **Triggered by**: CPC's cross-review of my review (Safe Agreements, "Migration routing decisions require XVII taxonomy classification, and the current migrations have not applied it") and CPC's original review Recommendation 8, which proposes requiring a XVII-classification table as a required element of migration documentation.
  - **Proposed change**: Every migration SIR must include a classification table for each migrated sub-bullet with the following columns: `| Sub-bullet text | XVII classification (execution logic / contribution guideline) | Migration destination document | Normative-strength disposition |`. The table must appear in the SIR — not only in the receiving document — so future reviewers can verify routing decisions against XVII's taxonomy and normative-strength requirements without reconstructing the reasoning from first principles. The normative-strength column subsumes the substance of Recommendation 6's per-MUST tracking into a single auditable artifact.
  - **Rationale**: Both CPC's review and my cross-review of CPC independently identify that VI's and X's migration SIRs did not apply XVII's execution-logic vs. contribution-guidelines taxonomy. VI's sub-bullet "Orchestration logic belongs in SKILL.md" is execution logic under XVII's third bullet and cannot be housed in CONTRIBUTING.md — CONTRIBUTING.md is not read by the agent runtime during deliberation. This is a stream-crossing violation that a XVII-classification table would have caught before routing. The table requirement is a structural complement to my Recommendation 4 (principled-distinction documentation): Recommendation 4 addresses why a principle migrates; the XVII-classification table addresses where each sub-bullet goes when it does. The two together close both the Criterion 2 documentation gap and the routing-quality gap that the current migrations left open.

---

### Position Summary

After cross-review, I withdrew zero recommendations outright, modified three (Recommendations 1, 2, and 6), and maintained five (Recommendations 3, 4, 5, 7, and 8) substantially intact. One new recommendation emerged from CPC's analysis.

The most significant change in my thinking concerns Recommendation 1 and the VI verdict. My original conditional — "incorrectly decided unless the principled distinction is supplied" — was genuine, and gate-faithfulness supplied the distinction: IX's judgment-laden qualifier accompanies a dense block of mechanical MUST requirements; VI's scope-qualifier is the sole trigger for its sole prescription with no mechanical backup. This distinction is persuasive and I accept it. The migration verdict stands. What I framed as a retention argument is now more accurately a documentation-adequacy argument: the migration was not wrongly decided, but the absence of the principled distinction from the original SIR was a genuine procedural defect — and this deliberation exists to remedy that defect. The factual error on VI's normative strength (my claim that "the principle-level obligation is encoded as MUST" when VI uses SHOULD at line 353) was a genuine mistake that gate-faithfulness correctly identified, and Recommendation 6 is modified accordingly.

My remaining highest-priority recommendation is Recommendation 4: require principled-distinction documentation for Criterion 2 judgment-call migrations. The cross-review process itself demonstrates why this recommendation matters. The IX/VI distinction — the load-bearing structure of VI's migration case — was not documented in the original SIR. It was supplied only because a supplemental deliberation commissioned a cross-review that forced the question. Without Recommendation 4, the same gap will recur in future migrations: a principle will be migrated on judgment-call grounds, the analogous qualifiers in retained principles will go unaddressed, and a future contrarian review will find the same structural defect. With Recommendation 4, the principled-distinction analysis is structurally required in the migration SIR itself, producing an audit trail that is complete at the time of the migration rather than retroactively reconstructed in supplemental deliberation.