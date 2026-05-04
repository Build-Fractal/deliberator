I'll read the required files in order before writing the arbitration resolution.

Now reading the Phase 4 dispute documents.

I have now read all required materials. I'll produce the arbitration resolution as the file content.

### Process Note

This arbitration was activated by the `always` trigger condition — subject arbitration fires unconditionally at the conclusion of this cooperative deliberation. Three disputes remain from the Phase 5 synthesis, all extracted under the `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers.

Participating agents: **pathway-defender** and **pathway-skeptic** in a **cooperative** deliberation (2 agents, 1 round, 8 total artifacts: 2 Phase 1 reviews + 2 Phase 2 cross-reviews + 2 Phase 3 revisions + 2 Phase 4 dispute documents). Subject arbitration: I am **pathway-taxonomy-arbiter**, the system whose v3.1.2 governance log entry is under review. My grounding is CONSTITUTIONAL_CONVERSATIONS.md (the v3.1.2 entry's four-pathway table, its surrounding methodology notes, and the accumulated governance precedents from v2.4.0 through v3.1.3).

---

### Decision Framework

The following principles from CONSTITUTIONAL_CONVERSATIONS.md govern the remaining disputes. Every binding decision below cites at least one of these.

- **[Enumerated mandatory conditions pattern]**: The v3.0.0 Governance Removal checklist (CONSTITUTIONAL_CONVERSATIONS.md, "2026-05-01 — spec 070 cycle 2" entry, "Required changes applied") established the constitutional pattern: governance requirements that depend on sequential or conditional compliance must appear as separately enumerated, mandatory checklist items — not as sub-notes embedded in prose. The checklist's six sub-items (a)–(f) each carry independent mandatory force precisely because they are separate items, not because they are comprehensive. A condition embedded in a prose paragraph reads as historical annotation; a condition enumerated as a list item reads as a requirement.

- **[Gate-enforcement vs. routing distinction]**: The v3.1.2 methodology note's pathway table (CONSTITUTIONAL_CONVERSATIONS.md, "2026-05-01 — Constitution v3.1.2" entry, "Pathway" section) was explicitly designed to let future amendment authors self-classify. Self-classification requires knowing what conditions must be satisfied to invoke a given pathway — not merely whether deliberation is required. The table's rows exist because different authorization mechanisms attach different mandatory conditions to the act of skipping deliberation. This is the operative design intent embedded in the document itself.

- **[Self-citation constraint on canonical examples]**: The v2.4.0 blind verification entry (CONSTITUTIONAL_CONVERSATIONS.md, "2026-04-25 — v2.3.0 verification (blind methodology)") established that adversarial blind verification surfaces content-level problems "anywhere in the document — including longstanding ones recent reviewers have stopped questioning." Applied to the self-referential pathway creation problem: when a governance mechanism's sole canonical example is the act that created it, the mechanism cannot rely on the canonical example as independent verification of the conditions it defines. The canonical example's self-consistency must be assessed explicitly and any gap must be acknowledged in the governance record.

- **[Priority escalation authority]**: The v2.6.0 cycle 1 arbitral precedent (CONSTITUTIONAL_CONVERSATIONS.md, "2026-05-01 — spec 070 cycle 1" entry, "Arbitral precedent: WP Rec 7 elevation") established that arbiters may upgrade a convergence point's priority classification when "constitutional grounding requires it" — specifically when a lower-priority framing would leave a genuine defect unaddressed for no principled reason. This precedent is directly applicable to the P2 vs. P3 severity dispute.

- **[Override-with-rationale precedent]**: The v2.4.0 XXVIII entry (CONSTITUTIONAL_CONVERSATIONS.md, "2026-04-29 — spec 071" entry, "Override-with-rationale") established that a blind verdict's ruling can be overridden when applying its standard uniformly would shrink existing ratified constitutional content. The override must name the uniform-application argument specifically. This precedent is the limiting principle on synthesizer authority: when a synthesizer adopts one agent's position over another's, the override must cite the grounding framework that makes the adopted position more aligned.

- **[Provisional status for first-use pathways]**: The v2.4.0 blind verification entry and the v3.0.0 SIR's "Follow-up TODOs" both demonstrate that governance mechanisms newly introduced in a single session carry a documentation burden: they must acknowledge their own bootstrapping limitations. The "both self-consistency AND blind verification" requirement (established in the v2.4.0 methodology lesson) applies the same principle — the first use of a verification methodology is the most fragile, and governance tools that acknowledge that fragility explicitly are more trustworthy than ones that do not.

- **[False authority claim = P2 governance debt]**: The v3.0.0 entry's "Cross-reference audit methodology" section (CONSTITUTIONAL_CONVERSATIONS.md, "2026-05-01 — spec 070 cycle 2" entry) established that missed cross-references are governance debt — specifically that a plural-form miss discovered at L1589 required the v3.0.0 SIR to establish a more thorough singular/plural/adjacent-phrase audit methodology going forward. The same logic applies to false authority claims: a citation that lends apparent support to a structural claim the citation's source context does not underwrite is governance debt of the same class, and must be corrected with similar urgency.

---

### Binding Decisions

#### Dispute: Classification axis — authorization-mechanism vs. deliberation-requirement

**Positions:**
- **pathway-defender**: The taxonomy's operative axis is "what preconditions authorize skipping deliberation?" — requiring separate rows 3 and 4 because gate conditions are sub-case-specific and only enforceable when attached to a specific row. A parenthetical sub-note in a collapsed row communicates history, not mandatory requirements. (defender disputes.md, first dispute.)
- **pathway-skeptic**: The taxonomy's operative axis is "does this amendment need deliberation?" — under which both rows answer identically ("no, when verbatim preservation holds"), making separate rows a structural over-decomposition. The authorization-mechanism distinction belongs in a sub-note, not a separate routing row. (skeptic disputes.md, first dispute.)

**Synthesizer's assessment:** The defender's position is stronger on gate-enforcement grounds. The taxonomy answers both the routing function (deliberation required?) and the gate-enforcement function (what conditions must be satisfied?). Gate conditions (a)–(c) attach to row 4 specifically; a collapsed row makes them appear as definitional refinements rather than mandatory requirements. Synthesis recommends row retention with Authorization-basis column and a dual-function note below the table. (synthesis final.md, Remaining Disputes, Dispute 1.)

**Ruling:** Retain rows 3 and 4 as separate rows. Add an Authorization-basis column to the taxonomy table. Add a dual-function note below the table stating both the routing function (all single-PR rows: "no deliberation required when verbatim preservation holds") and the gate-enforcement function (Authorization basis governs what conditions must be satisfied to invoke each single-PR pathway).

**Grounding citation:** The enumerated mandatory conditions pattern (Decision Framework, first principle): the v3.0.0 Governance Removal checklist established that requirements that depend on sequential or conditional compliance must appear as separately enumerated mandatory items, not as sub-notes in prose. Gate conditions (a)–(c) in the defender's revised Rec 3 are exactly this class of requirement — they are mandatory conditions that a claiming amendment must satisfy affirmatively before invoking row 4. In a collapsed row, they appear attached to a sub-note rather than to a row, which is the structural equivalent of embedding the Removal checklist's conditions in a paragraph rather than listing them as (a)–(f). The v3.0.0 checklist's design demonstrates that separately enumerated items carry mandatory force; sub-notes do not.

Additionally, the gate-enforcement vs. routing distinction (Decision Framework, second principle): the v3.1.2 methodology note was explicitly built for future amendment author self-classification. Self-classification requires knowing what conditions must be satisfied — not merely whether deliberation is required. The skeptic's routing-only framing correctly describes one function of the table but omits the function that motivates the row structure.

**Rationale:** Both agents agreed to accept the synthesizer's axis declaration (defender disputes.md, "Proposed resolution path": "I commit to accepting the synthesizer's axis choice"; skeptic disputes.md, "Flexibility" item 1: "if the synthesizer declares the 'authorization mechanism' axis operative and retains separate rows, I will not block the outcome"). The synthesizer declared the authorization-mechanism axis operative. The governing question is therefore not which axis is abstractly better, but whether the synthesizer's declaration is grounded in the documents I am bound by. It is: the Removal checklist precedent demonstrates that the governance log itself, when building mandatory-condition structures, uses separate enumerated items rather than sub-notes. A governance mechanism that follows a weaker structural form than the governance log's own precedents would set a regressive structural precedent.

**Rejected position:** pathway-skeptic's collapse recommendation. Its strongest argument — that an orchestrator routing an amendment needs to answer "do I need deliberation?" (a binary), not "which authorization class applies?" (a classification) — is correct as a description of the routing function. The routing function alone would support collapse. What the argument does not address is that the taxonomy simultaneously serves the gate-enforcement function, and for that function, collapsed rows with sub-notes are not enforcement mechanisms. Skeptic's own revised Rec 5 (scope-coverage requirement as condition (b)) is a mandatory gate condition; making it visible as a row-level requirement, not a sub-note, is the only structural form consistent with mandatory enforcement.

**Required changes:** In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology section:
1. Retain rows 3 and 4 as separate rows in the taxonomy table.
2. Add a fifth column "Authorization basis" with values: "Full dual-deliberation (spec 067)" (row 1/v3.0.0); "Absence of new normative content" (rows 2–3/v3.1.0 and v3.1.1); "Prior deliberation scope coverage of deferred wording" (row 4/v3.1.2).
3. Add a note below the table: "For routing: all single-PR rows answer 'no deliberation required when verbatim preservation holds.' Authorization basis governs what conditions must be satisfied to invoke each single-PR pathway — see gate conditions for row 4 below."

---

#### Dispute: Provisional label vs. self-consistency-gap acknowledgment

**Positions:**
- **pathway-defender**: Address the self-consistency gap with an explicit acknowledgment note naming condition (b) specifically — the v3.0.0 deliberation's scope coverage of the deferred sentence's substantive claim is not determinable from the governance log as written. (defender disputes.md, second dispute.)
- **pathway-skeptic**: Apply a "Provisional" label to row 4 with a two-example canonicity requirement, as a separate and complementary mechanism addressing pathway maturity rather than canonical-example self-consistency. (skeptic disputes.md, Tensions, self-citation severity.)

**Synthesizer's assessment:** Both measures address different concerns and should coexist. The acknowledgment note is specific and backward-looking (names the canonical example's limitation); the provisional label is forward-looking (signals pathway maturity). Neither substitutes for the other. Both cross-reviews confirmed compatibility. (synthesis final.md, Remaining Disputes, Dispute 2.)

**Ruling:** Implement both: the acknowledgment note as the primary mechanism (naming condition (b) specifically and stating the gap is not determinable from the current governance log), and the provisional label as the secondary maturity indicator (row 4 entry adds "Provisional — single canonical example (canonical status requires two independent uses from distinct sessions without governance anomalies)").

**Grounding citation:** The self-citation constraint on canonical examples (Decision Framework, third principle): when a governance mechanism's sole canonical example is the act that created it, the mechanism cannot rely on the canonical example as independent verification of the conditions it defines. The canonical example's self-consistency must be assessed explicitly and any gap acknowledged in the governance record. The acknowledgment note is the mechanism that satisfies this principle. The provisional label satisfies the related but distinct requirement that governance tools acknowledge their bootstrapping limitations explicitly (Decision Framework, fifth principle).

**Rationale:** Defender's non-negotiable — that the acknowledgment note must be included regardless of whether the provisional label is also applied — is grounded in Principle XI (Single Source of Truth, CONSTITUTION.md). The governance log is the authoritative record for what deliberations evaluated. If the canonical example's claim to satisfy condition (b) is not determinable from that record, the record has a gap, and the gap must be named rather than papered over. Skeptic's provisional label does not name the gap — it signals maturity uncertainty. Both signals are accurate and non-redundant. Defender's cross-review of skeptic (disputes.md, Tensions, second item) and skeptic's cross-review of defender (disputes.md, Tensions, fourth item) both confirm the mechanisms are complementary. There is no principled reason to implement one and exclude the other.

**Rejected position:** Neither position is fully rejected. The dispute was whether to implement one mechanism or both. Both are adopted. If forced to adjudicate which is more important: the acknowledgment note is primary because it closes the self-defeating loop (a pathway whose canonical example may fail its own gate conditions must acknowledge that gap — not doing so would leave the gate appearing self-serving). The provisional label is secondary because it addresses a different concern (maturity) that is genuine but less urgent.

**Required changes:** In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology section:
1. Add the self-consistency gap acknowledgment note: "Self-consistency note: condition (b) above raises a self-consistency question for this entry's canonical example. The v3.0.0 deliberation validated the Principle II stable-interfaces enumeration extension as an architectural change. Whether the deliberation's scope explicitly covered the correctness of the specific elaboration sentence ('Reusing a retired principle number is a breaking change — any historical document that cited the retired number by identity would thereafter refer to a different principle.') is not determinable from the governance log as written. If scope did not extend to that sentence's substantive claim, v3.1.2 satisfies conditions (a) and (c) but not (b). Future applications of this pathway must resolve condition (b) affirmatively — by citing the specific deliberation phase and finding that evaluated the claim's correctness — before invoking the low-cost pathway. This gap does not void the pathway's analytical framework; it identifies a documentation deficiency in the canonical example."
2. In the taxonomy table, add to row 4's entry: "Provisional — single canonical example (canonical status requires two independent uses from distinct sessions without governance anomalies)."

---

#### Dispute: RFC/CVE analogy severity — P2 vs. P3

**Positions:**
- **pathway-skeptic**: P2 severity — the correction must precede structural decisions because the uncorrected analogy provides false authority for the multi-pathway taxonomy structure and should not remain as background reasoning while structural decisions are finalized. (skeptic disputes.md, second dispute.)
- **pathway-defender**: P3 severity — the correction is a separable vocabulary note that can follow structural decisions as cleanup; the correction is warranted regardless of structural outcome. (defender disputes.md, convergence section, RFC/CVE item.)

**Synthesizer's assessment:** Content is converged; both agents agree the correction must be made. P2 classification is adopted because the correction removes a false authority claim that could be invoked in future governance discussions — treating it as P2 signals promptness, not as an afterthought. Sequencing is moot in a synthesis that resolves all decisions simultaneously. (synthesis final.md, Remaining Disputes, Dispute 3.)

**Ruling:** Adopt P2 severity. The RFC/CVE analogy correction must be implemented at the same priority as the structural recommendations, not as trailing cleanup. The correction must explicitly state that the RFC/CVE reference in Principle Number Stability supports identifier stability — the no-reuse rule for principle numbers — and that RFC and CVE processes use single amendment pathways; the conversus multi-pathway taxonomy is a departure from that model, not an extension of it. The analogy cannot be cited as authority for adding new pathway rows.

**Grounding citation:** The false authority claim = P2 governance debt principle (Decision Framework, sixth principle): the v3.0.0 cross-reference audit methodology established that missed cross-references and misattributed citations are governance debt — to be corrected with the same urgency as other P1/P2 items, not deferred to trailing cleanup. The L1589 plural-form miss was corrected in the same v3.0.0 ratification commit, not in a follow-up patch. The analogy mismatch is a citation that lends apparent support to a structural claim the citation's source context does not underwrite. That is governance debt of the same class.

Additionally, the priority escalation authority precedent (Decision Framework, fourth principle): the v2.6.0 cycle 1 arbitral precedent established that arbiters may upgrade a convergence point's priority classification when the constitutional grounding requires it — "the first use of arbitral authority to upgrade a convergence point's priority classification rather than resolve a disputed position." Here, the RFC/CVE correction is fully converged in content; the dispute is only about severity. Upgrading from P3 to P2 is the same action the v2.6.0 arbiter took with WP Rec 7. The grounding justification is analogous: leaving a false authority claim in place at P3 priority — where it can persist while structural recommendations are implemented — introduces precisely the compounding-authority risk the skeptic's P2 argument identifies.

**Rationale:** The defender's "separable from structural outcome" argument correctly observes that the correction's content does not depend on the row-structure decision. This is true. But separability of content is not the same as separability of priority. A correction that is functionally unconstrained (can be made independently of other decisions) can still carry P2 urgency if the reason for its urgency is future-compounding rather than current-blocking. The skeptic's argument is that an uncorrected misattributed precedent can be invoked in future governance discussions as implicit support for adding new taxonomy rows. That argument does not require the correction to block the current structural decision — it requires the correction to be contemporaneous with the structural decision so that the record establishes the boundary clearly. P2 achieves this; P3 does not.

**Rejected position:** pathway-defender's P3 framing. Its strongest argument — "separable from the structural outcome" — is accurate but addresses the wrong question. Separability describes content independence; priority describes urgency and sequencing relative to other changes. P3 framing implies trailing cleanup, which leaves the false authority claim in place in the implementing PR's governance record. The correction is cheap (one sentence), the content is fully converged, and the risk of deferral (future orchestrators invoking the analogy as implicit multi-pathway authority) is concrete. There is no principled reason to defer it to a P3 trailing note.

**Required changes:** In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology note, add at P2 priority alongside structural changes: "Note on the RFC/CVE analogy: the RFC/CVE reference in Principle Number Stability supports identifier stability — the no-reuse rule for principle numbers. RFC and CVE processes use single amendment pathways; the conversus multi-pathway taxonomy is a departure from that model, not an extension of it. The analogy cannot be cited as authority for adding new pathway rows to this taxonomy."

---

### Summary of Changes Required

**P1 — Required for correctness**

1. **Retain rows 3 and 4 as separate rows** (from Dispute: Classification axis): In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology section, keep the taxonomy table's four separate rows. Do not collapse rows 3 and 4. Priority: P1.

2. **Add Authorization-basis column to taxonomy table** (from Dispute: Classification axis): In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology section, add a fifth column "Authorization basis" to the four-row taxonomy table with values: "Full dual-deliberation (spec 067)" (v3.0.0); "Absence of new normative content" (v3.1.0, v3.1.1); "Prior deliberation scope coverage of deferred wording" (v3.1.2). Priority: P1.

3. **Add dual-function routing note below taxonomy table** (from Dispute: Classification axis): In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology section, add below the taxonomy table: "For routing: all single-PR rows answer 'no deliberation required when verbatim preservation holds.' Authorization basis governs what conditions must be satisfied to invoke each single-PR pathway." Priority: P1.

4. **Add self-consistency gap acknowledgment note** (from Dispute: Provisional label vs. self-consistency-gap acknowledgment): In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology section, add the acknowledgment note naming condition (b) specifically and stating the gap is not determinable from the current governance log. Full text specified in Required changes above. Priority: P1.

**P2 — Required for design integrity**

5. **Add provisional label to row 4** (from Dispute: Provisional label vs. self-consistency-gap acknowledgment): In the taxonomy table, row 4 entry, add: "Provisional — single canonical example (canonical status requires two independent uses from distinct sessions without governance anomalies)." Priority: P2.

6. **Add RFC/CVE analogy correction** (from Dispute: RFC/CVE analogy severity): In `CONSTITUTIONAL_CONVERSATIONS.md`, v3.1.2 methodology note, add the note correcting the analogy's scope — RFC/CVE supports identifier stability, not multi-pathway taxonomy structure; the analogy cannot be cited as authority for adding new pathway rows. Full text specified in Required changes above. Priority: P2.

**P3 — Recommended from convergence (not from disputes — included for completeness)**

All P1 and P2 changes from the convergence section of the synthesis (prospective-only clause, scope-coverage requirement, gate conditions, migration disclaimer, vocabulary distinction) remain as-specified in the synthesis's Actionable Spec Changes. No ruling in this arbitration modifies the converged recommendations — they are outside arbitral scope.

---

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| Classification axis — authorization-mechanism vs. deliberation-requirement | Retain rows 3 and 4; add Authorization-basis column; add dual-function routing note | High | Grounded directly in v3.0.0 Removal checklist precedent and v3.1.2 design intent; both agents agreed to accept the synthesizer's axis declaration; defender's enforcement-visibility argument is structurally demonstrable |
| Provisional label vs. self-consistency-gap acknowledgment | Implement both acknowledgment note (P1) and provisional label (P2) | High | Both mechanisms address categorically different concerns confirmed independently by both cross-reviews; no principled reason to implement one and not the other; defender's non-negotiable is grounded in Principle XI |
| RFC/CVE analogy severity — P2 vs. P3 | P2 severity | Medium-High | Content is fully converged; severity grading rests on the compounding-authority argument (which is sound) and the priority escalation precedent (which is applicable); "Medium" component: the practical consequence in a simultaneous-resolution synthesis is modest, but the precedent value of recording it as P2 rather than P3 is real |

**Overall deliberation quality assessment:** This was a high-quality cooperative deliberation. The 6 convergence points achieved through cross-review represent substantive concessions on both sides: the defender's "implicit validation" retraction was the most significant — a complete analytical reversal, not a strategic concession — and the skeptic's concession that the Off-Base Assumption #1 was "partially misstated" demonstrates the cross-review process working as designed. The 3 remaining disputes are all structural-form disputes where content was already converged, which is the appropriate scope for arbitration (disputes about enforcement mechanism and priority, not about what the governance record should say).

The deliberation also surfaced a systemic observation worth noting here (not as a ruling): the pathway taxonomy's value as a governance tool depends entirely on the migration to CONSTITUTION.md that both agents unanimously identified as the structural prerequisite. The P1 enrichments in the governance log are valuable as records of intent; they become enforceable only after migration. The arbiter notes this as an observation — not a ruling, since migration is already the unanimous P1 recommendation of the deliberation — to underscore that the implementing PR's most consequential action is migration, not any of the enrichment changes.

---

PATHWAY-TAXONOMY VERDICT: RETAIN (with modifications per Disputes 1, 2, and 3 above — add Authorization-basis column, dual-function routing note, self-consistency-gap acknowledgment note, provisional label for row 4, and RFC/CVE analogy correction)