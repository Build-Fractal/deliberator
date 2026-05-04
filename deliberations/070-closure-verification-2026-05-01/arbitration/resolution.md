I'll read the synthesis and all Phase 4 dispute documents before writing my arbitration resolution.

Now I have everything I need. Let me write the arbitration resolution.

### Process Note

This arbitration was triggered by the `always` condition — subject arbitration is unconditionally activated in the spec-070 closure verification deliberation configuration. Five disputes remain unresolved from the Phase 5 synthesis. Three agents participated in the deliberation: **audit-faithfulness** (content-fidelity scope), **gap-detector** (process-completeness scope), and **implementation-pragmatist** (governance-pragmatics scope). This is a **cooperative** deliberation with subject arbitration, meaning the arbiter is the system under review — spec 070 and its implementation artifacts — exercising binding decision authority grounded in the spec text.

---

### Decision Framework

The following principles from spec 070 (`specs/done/070-grandfathered-audit/spec.md`) bear on the five remaining disputes. All rulings below cite at least one of these.

- **[§4.1 Coordinate Migration Content]**: The proposed migration target for Principle VI "should be" a note covering "(a) what kinds of repository artifacts are appropriate for prose markdown vs. structured/executable formats, (b) the practical heuristic ('if an agent or pipeline parses it, it should be a script, config, or structured data'), (c) examples drawn from current `skills/`, `presets/`, and `templates/` usage." Items (a)–(c) are presented as a coordinate list prescription for content completeness. (spec 070 §4.1, final paragraph of migration-target proposal.)

- **[§5.3 Success Criteria — Migration Completeness]**: "A migration is complete when: The migrated content exists in its new home... The implementation PR includes the spec 067 §4 verification artifacts (both self-consistency and blind deliberations) and a passing acceptance bar... Cross-references from other principles, specs, and skills point at the new location. A `CONSTITUTIONAL_CONVERSATIONS.md` entry records the migration." (spec 070 §5.3, five-bullet list.)

- **[§6.2 Blind Verification Mandate — Contrarian Prompt Required]**: "The blind run MUST include an agent prompt explicitly arguing one or more of VI/X/XVI passes the gate on closer reading and should NOT be migrated." The mandate uses `MUST`, not `SHOULD`. (spec 070 §6.2, penultimate sentence of the Acceptance bar paragraph.)

- **[§6.3 Two-Tier Verification Structure]**: "The implementation PR(s) that perform actual `CONSTITUTION.md` migration are verified per spec 067 in their own right — this spec's verification covers the audit conclusions, not the resulting amendments." This two-tier structure distinguishes spec-level verification (auditing §4 conclusions) from implementation-PR verification (auditing the migration artifacts). (spec 070 §6.3.)

- **[§9 Acceptance Criteria — AC #5]**: "Blind verification (per §6.2, using `presets/role/devils-advocate.yml` and `balanced-arbiter.yml`): 0 ACCEPT-level findings on the per-principle verdicts. The blind run MUST include an agent prompt explicitly arguing one or more of VI/X/XVI passes the gate on closer reading and should NOT be migrated." AC #5 names this as a required condition for spec closure. (spec 070 §9, fifth acceptance criterion.)

- **[§9 Acceptance Criteria — AC #4]**: "Self-consistency verification (per §6.1): 0 ACCEPT-level findings on the per-principle verdicts." This is the parallel track to AC #5 and confirms the spec requires both independent verification tracks before closure. (spec 070 §9, fourth acceptance criterion.)

- **[§7 Risk Register — Migration Loses Enforcement Weight]**: The risk that "Future authors don't consult `CONTRIBUTING.md` / `docs/*.md` and re-introduce the migrated patterns" is explicitly registered, with the mitigation "Add CI lints for the mechanically-checkable subset of each migrated principle (where one exists). Operational guidance is reinforced by automation, not just by document presence." This establishes that examples and concrete patterns are the mechanism by which the migration retains enforcement reach. (spec 070 §7, second risk row.)

---

### Binding Decisions

#### Dispute: §4.1(c) examples priority — P1 (AF) vs. P2 (GD + IP)

**Positions:**
- **audit-faithfulness** (disputes.md, Dispute 1 and Final Position Non-Negotiables): The §4.1(c) gap must be carried as "a confirmed P1 gap that needs resolution before the spec 070 migration can be considered fully executed." Spec 070 §4.1(c) is a coordinate list item structurally coequal with (a) and (b); the migration's practical value depends on examples being present.
- **gap-detector + implementation-pragmatist** (GD revision New Recs; IP disputes.md Dispute 1): P2, because the document is functional without examples — their absence represents a completeness deficit, not functional failure. IP: "A new contributor who reads this section can make a reasonable judgment call about whether a given artifact is appropriate."

**Synthesizer's assessment:** P2 is better supported. The test for P1 is functional failure. All three agents agree the migration is "substantively sound" (AF's own characterization). AF conflates "fully executed per the spec prescription" with "functionally broken." These are distinct standards. P1 should not become a completeness-ideal standard. (synthesis, Unresolved Contradictions §1.)

**Ruling:** Adopt P2 (GD + IP position), as refined by the synthesizer. The §4.1(c) examples gap is a committed, non-optional P2 item that must be resolved before spec 070 can be declared fully closed, but does not block other remediation work proceeding in parallel.

**Grounding citation:** Spec 070 §4.1 presents items (a)–(c) as a "should be" prescription for content coverage, not as a mandatory minimum for the migration to be operationally usable. The §5.3 Success Criteria test is whether "the migrated content exists in its new home" — the content does exist; the completeness question is whether all prescribed elements are present. §7's risk-register framing is instructive: concrete examples are the mechanism that reinforces operational guidance against re-introduction of the pattern. Their absence is a real risk, not a non-issue — but the §7 framing characterizes this as a mitigation mechanism, not a foundational requirement for the guidance to function at all.

**Rationale:** AF is correct that §4.1(c) is structurally coequal with (a) and (b) in the coordinate list, and correct that the items' purpose is to calibrate the "drives behavior" judgment. However, calibration precision is precisely what examples add — they improve a functional document rather than rescue a broken one. The critical test is whether a contributor reading the current CONTRIBUTING.md can make a correct judgment call. IP's direct assessment of the current text answers this: yes. P1 is reserved for items that would cause a contributor to apply the guidance incorrectly. P2 accurately classifies an item whose absence makes the guidance less vivid but does not cause misapplication.

**Rejected position:** AF's P1 position is not adopted because it requires reading "fully executed per spec prescription" as equivalent to "functionally complete for contributors." AF's own non-negotiables paragraph characterizes the migration as "substantively sound" — a characterization incompatible with P1 (functionally broken) classification. The strongest argument for P1 is that §4.1(c)'s coordinate structure implies all three items are mandatory for spec 070's own acceptance criteria. However, §9's acceptance criteria do not enumerate (a)–(c) individually; §9 AC #7 requires that implementation PRs be "filed" and proceed through verification, not that every prescriptive detail in §4 be instantiated. The coordinate list is a migration design prescription, not a spec-closure gate.

**Required changes:**
- `CONTRIBUTING.md` (§ Authoring Conventions): Add a subsection or inline examples — at minimum 2–3 concrete examples from actual files in `skills/`, `presets/`, and `templates/` directories — demonstrating the (a) orchestration-in-SKILL.md, (b) configuration-in-YAML, and (c) markdown-for-human-orientation patterns. Examples must reference files that currently exist in the repository; synthetic constructions are not acceptable per spec 070 §4.1(c)'s "drawn from current... usage" language. Priority: P2. Not a blocker for other P2 remediation work.

---

#### Dispute: §4.1(c) examples sequencing — after blind deliberation (GD) vs. parallel with documented contingency (AF + IP)

**Positions:**
- **gap-detector** (disputes.md, Dispute 1 and Final Position Flexibility): "These examples should be added only after the supplemental blind deliberation's contrarian-agent test resolves whether VI was correctly migrated... The dependency is structural, not a probability assessment." Adding examples before verification creates documented content that must be reversed if VI is overturned, expanding the reversal surface.
- **audit-faithfulness + implementation-pragmatist** (AF disputes.md Dispute 1; IP disputes.md Dispute 2): Examples can proceed in parallel because the probability of reversal is assessed as low by all agents; a parallel path with an explicit review obligation if reversal occurs honors the logical dependency without unnecessary serialization.

**Synthesizer's assessment:** The AF + IP compromise is more operationally sound, with one refinement: the examples should not merge before the supplemental blind deliberation has filed its initial verdict — a light gate that preserves the ability to incorporate early contrarian findings into example content. This is not a hard sequential block but an explicit documented review obligation. (synthesis, Unresolved Contradictions §2.)

**Ruling:** Adopt the synthesizer's refined AF + IP compromise. §4.1(c) examples may be drafted and merged in a separate commit or PR, provided: (i) the supplemental blind deliberation's `conversus.yml` and initial verdict are on record before the examples PR merges; (ii) the examples PR description (or `CONTRIBUTING.md`'s migration footnote) explicitly states that if the supplemental blind deliberation produces an affirmative contrarian PASS for VI, the Authoring Conventions section and examples must be revisited.

**Grounding citation:** Spec 070 §6.2's `MUST` language applies to the contrarian-agent mandate for the blind deliberation's configuration, not to the sequencing of downstream content work. Spec 070 §5.1 (ordering guidance) specifies ordering for migration steps by contention level — it does not impose ordering between content-enrichment work and process-verification work. The §7 risk register's mitigation mechanism framing (examples as enforcement-reach reinforcement) supports prioritizing example delivery over process parallelism, but §7 explicitly frames this as a mitigation, not a precondition.

**Rationale:** GD is correct that the logical dependency exists: examples that illustrate "how to apply VI's guidance in practice" draw their authority from VI's migration being a valid governance decision. If the contrarian deliberation overturns VI, the examples are not merely outdated — they are positively misleading for contributors. However, GD's structural-dependency argument is binding only if the reversal probability is non-negligible or if the reversal cost is high. All three agents assess the probability as low; the reversal cost (removing or revising a few examples) is minimal. The synthesizer's light gate — wait for the initial verdict before merging — preserves GD's core concern (don't commit content before the verification direction is known) without imposing hard serialization.

**Rejected position:** GD's hard-sequential position is not adopted because it treats a logical dependency as operationally binding regardless of probability or cost. GD acknowledges "the probability that the contrarian agent overturns the VI migration decision is low" — this acknowledgment undermines the case for hard serialization. The reversal-surface argument (larger revision if examples must be removed) is real but modest: directional bullets are already in place and would themselves need revision if VI were overturned; examples add some surface area but not a categorically different reversal obligation. The synthesizer's light gate captures GD's concern in a documented contingency obligation, which is the appropriate instrument for low-probability dependencies.

**Required changes:**
- No immediate file changes required by this ruling. The sequencing constraint is procedural: the §4.1(c) examples PR must not be merged until the supplemental blind deliberation from P1 item #1 (in the synthesis's Actionable Spec Changes section) has filed its initial verdict. The examples PR description must contain an explicit contingency note. This constraint should be recorded in the remediation plan for the follow-up spec or reopened spec 070 work.

---

#### Dispute: False attribution in GD cross-review of AF — manufactured contradiction

**Positions:**
- **audit-faithfulness** (disputes.md, Dispute 2 and Final Position Non-Negotiables): GD's Dangerous Contradiction #1 attributed to AF's Alignment section the item "(audit-faithfulness, Alignment, 'spec 067 preset discipline followed')" — which does not exist in AF's Alignment section. It exists in GD's own Alignment section. The attribution was constructed from misattributed evidence; the synthesis must not carry forward a contradiction between the two reviews, because no contradiction exists. Both findings are independent and additive.
- **gap-detector** (implicit, from revision behavior): GD's revision did not explicitly retract the attribution but cooperatively adopted AF's §5.3 framing, consistent with recognizing the error without naming it. GD's substantive §6.2 finding (contrarian prompt absent) is valid and independent regardless of attribution accuracy.

**Synthesizer's assessment:** AF is correct. Direct examination of the deliberation artifacts confirms the false attribution: GD's review.md Alignment section item 2 contains "spec 067 preset discipline followed" as GD's own check; AF's Alignment section (7 items) contains no §6.2 compliance claim. The manufactured contradiction should not reduce the weight of GD's §6.2 finding in the synthesis record. (synthesis, Unresolved Contradictions §3.)

**Ruling:** Accept AF's position in full. The synthesis record must explicitly state: (a) there is no contradiction between AF's Alignment section and GD's §6.2 finding; (b) GD's §6.2 process-completeness finding (contrarian prompt absent, cycle 2 target structurally unable to satisfy §9.5) is an independent, fully-supported finding that was never contested by AF's content-fidelity review; (c) AF's content-fidelity findings and GD's process-completeness findings cover different analytical domains and both stand at full weight.

**Grounding citation:** Spec 070 §6.2 and §6.3 explicitly distinguish spec-level verification (§6.2, auditing the §4 conclusions) from implementation-PR verification (§6.3). AF's scope is content fidelity against spec 070 §4's prescriptions; GD's scope is process completeness of the verification trail. These are different audit surfaces by the spec's own architecture. A contradiction cannot exist between findings that address non-overlapping questions.

**Rationale:** The false attribution is a factual error, not a position dispute. Fabricating a contradiction from a misattributed citation is a procedural error in GD's cross-review; the substantive §6.2 finding is independent of and unaffected by the error. AF's non-concession on this dispute is correct — the synthesis must not carry the manufactured contradiction forward, because doing so would inaccurately frame GD's §6.2 finding as a "surviving residue of a contested claim" rather than as a standalone finding that was never challenged on the merits. GD's implicit recognition of the error (not reproducing the false attribution in the revision's Position Summary) is consistent with an error acknowledged but not formally retracted. The arbitration record must make the retraction explicit.

**Rejected position:** There is no meaningful opposing position to reject here — GD's substantive finding is fully preserved by this ruling. The only thing rejected is the framing that a contradiction existed between AF's and GD's reviews. GD's strongest argument (that the §6.2 finding should receive full weight) is accepted in full. The attribution error is corrected without diminishing GD's finding.

**Required changes:**
- `deliberations/070-closure-verification-2026-05-01/summary/final.md` (or, if the synthesis is superseded by this arbitration resolution, this resolution itself): Add an explicit paragraph under the Systemic Contradictions section or as a synthesis correction note stating: "GD's Dangerous Contradiction #1 in the Phase 2 cross-review of AF rested on a false attribution. The item '(audit-faithfulness, Alignment, spec 067 preset discipline followed)' does not exist in AF's Alignment section; it exists in GD's own Alignment section (GD review.md, Alignment item 2). GD's §6.2 finding (contrarian prompt absent from both blind deliberations; cycle 2 target structurally unable to satisfy §9.5) is an independent process-completeness finding that was never contested on the merits by AF's content-fidelity review. Both findings stand at full weight as non-competing items from different analytical domains. No contradiction exists between AF's and GD's reviews."

---

#### Dispute: Scope of P0 blocking — governance hygiene blocked (GD) vs. not blocked (IP)

**Positions:**
- **gap-detector** (revision, Position Summary): "Every other finding in this review... presupposes that the migration decisions for VI, X, and XVI were correct. The contrarian-agent test is the only mechanism spec 070 prescribed to verify that presupposition adversarially. All remediation work is downstream of that structural fact."
- **implementation-pragmatist** (disputes.md, Dispute 3 and Final Position Non-Negotiables): The §9.5 gap is P0 for spec closure, but it does NOT block governance hygiene work that is accurate regardless of how migration decisions resolve — CONCONV documentation, the XIX tracking issue, the Governance list update, and docs/output-conventions.md bullet relocation.

**Synthesizer's assessment:** IP's distinction is valid. The test: "would this work be equally appropriate whether VI was migrated or not? If yes, it's not blocked." Applying this test: CONCONV documentation, XIX tracking issue, Governance list update, docs/output-conventions.md bullet relocation, mkdocs.yml verification, plain-language lint and test tickets — all are accurate and appropriate regardless of migration validity. §4.1(c) examples and unqualified v3.0.0 precedent citations are blocked. (synthesis, Unresolved Contradictions §4.)

**Ruling:** Adopt IP's distinction, operationalized with the synthesizer's bright-line test. The §9.5 supplemental blind deliberation is P0 for spec 070 closure and for any work that treats v3.0.0 as an unqualified, fully-verified migrate-out precedent. It does not block governance hygiene work that is independently accurate regardless of migration outcome. The following items proceed without waiting for §9.5 resolution: CONSTITUTIONAL_CONVERSATIONS.md coordinated update (recording what happened and what was deferred), XIX tracking issue filing, Governance operational-guidance list addition to CONSTITUTION.md, docs/output-conventions.md bullet relocation, mkdocs.yml nav verification. The following items remain conditioned on §9.5 resolution: §4.1(c) examples (per Dispute 2 ruling), and any citation to v3.0.0 as an unqualified migrate-out precedent that future amendment authors may rely on without acknowledging the §9.5 gap.

**Grounding citation:** Spec 070 §5.1 (ordering guidance) provides a sequencing principle for migration steps based on contention level — it does not impose ordering between process-verification and governance-hygiene tracks. Spec 070 §5.3 Success Criteria enumerate five requirements for migration completeness; the cross-references requirement (SC 4, Governance list pointer) is independent of the blind-verification requirement (SC 2). These are parallel conditions, not sequential ones. GD's "all remediation work is downstream" framing treats SC 2 as a gate on SC 4, which spec 070 §5.3's structure does not support.

**Rationale:** GD's position rests on the premise that every downstream action "presupposes the migration decisions were correct." This is true for a specific category of work: work that cites the migrations as valid precedent or that relies on the migration decisions being correct to derive authority. It is not true for work that accurately records what happened — regardless of whether what happened was correct. CONSTITUTIONAL_CONVERSATIONS.md documentation is history-recording, not endorsement. The XIX tracking issue corrects a SIR-documented governance anti-pattern ("NOT filed as an issue here") that exists independently of any migration decision. The Governance list update discharges a SIR-committed obligation — the SIR itself exists and made the commitment regardless of whether the migration was valid. GD's position, applied uniformly, would prevent correcting governance defects in the ratification record until the verification track resolves, which would leave the record less accurate during the remediation period. That is worse than proceeding with hygiene items that everyone agrees are correct.

**Rejected position:** GD's "all downstream work is blocked" position is not adopted because it collapses the distinction between endorsing a decision and accurately describing it. The structural fact that the contrarian test hasn't run does not make it incorrect to document that VI was migrated, that certain items were deferred in the SIR, or that the Governance section lacks a cross-reference pointer. These are facts about what happened, not claims about whether what happened was correct. GD's concern about "presupposing the migration was correct" is valid for work that relies on the migration's correctness — and this ruling preserves that concern by blocking §4.1(c) examples and unqualified precedent citations.

**Required changes:**
- No file changes are required by this ruling alone. The ruling provides the classification framework for the remediation plan. The following implementation items may proceed immediately (not blocked by §9.5): CONSTITUTIONAL_CONVERSATIONS.md coordinated update, XIX tracking issue, Governance operational-guidance list addition to CONSTITUTION.md, docs/output-conventions.md bullet relocation. The following must wait for §9.5 initial verdict: §4.1(c) examples (per Dispute 2 ruling above), any spec or governance document that cites v3.0.0 as a verified, unqualified migrate-out precedent for future use.

---

#### Dispute: Governance list framing — unmet §5.3 SC at PR #99 (GD) vs. deferred delivery obligation (IP)

**Positions:**
- **gap-detector** (revision, New Rec 3 and disputes.md Dispute 2): The missing Governance list is an unmet spec 070 §5.3 Success Criterion at PR #99 closure time, adding to the evidence that spec 070's closure was premature. The SIR's P2 self-classification deferred a delivery commitment but cannot self-certify an acceptance criterion as satisfied.
- **implementation-pragmatist** (disputes.md, Dispute 3): The SIR's own P2 classification governs. The item was consciously categorized as non-blocking; retroactively treating the SIR's deferred delivery as a failed acceptance criterion retroactively upgrades the SIR's self-assessment without affirmative evidence it was wrong.

**Synthesizer's assessment:** Both framings are accurate and serve different purposes. For historical characterization of PR #99: GD is correct — §5.3 SC 4 was open at closure time. For forward-looking action: IP is correct — the item is a P2 committed obligation to discharge in the next PATCH, not a retroactive priority escalation. Bifurcate. (synthesis, Unresolved Contradictions §5.)

**Ruling:** Adopt bifurcation per the synthesizer's recommendation. Both framings are correct and address different questions. They must both appear in the record without collapsing either into the other:

1. **For the historical record**: GD is correct. Spec 070 §5.3 SC 4 ("Cross-references from other principles, specs, and skills point at the new location") was open at PR #99 merge time. The CONCONV cycle 2 entry for PR #99 should accurately state that §5.3 SC 4 was unresolved at closure — this is an additional factual element in the premature closure finding alongside the §9 AC #5 gap. A SIR is a delivery artifact; it can sequence and defer work, but it cannot self-certify that a spec's own acceptance criteria have been satisfied. The §5.3 Success Criteria are the spec's criteria, not the SIR's criteria.

2. **For forward-looking action**: IP is correct. The appropriate forward-looking disposition of the Governance list update is P2 — committed, non-optional, to be discharged in the next PATCH cycle. The historical finding that §5.3 SC 4 was open at PR #99 does not require retroactively escalating the item beyond P2 for future scheduling purposes. The SIR's sequencing judgment (P2, not P1) should govern forward priority because it reflects a deliberate, contemporaneous assessment of relative urgency.

**Grounding citation:** Spec 070 §5.3 explicitly enumerates "Cross-references from other principles, specs, and skills point at the new location" as one of the five conditions for migration completeness. §9 AC #7 requires that "Implementation PR(s) are filed... and proceed through their own spec 067 verification independent of this spec." The v3.0.0 SIR deferred the Governance cross-reference update with explicit P2 language. Whether this deferral constituted a "satisfied" acceptance criterion or an "open" one is a question about the authority of a delivery artifact (SIR) relative to the spec's own acceptance language (§5.3). The spec's language governs: "cross-references point at the new location" is either true or it isn't at PR #99 merge time.

**Rationale:** The bifurcation resolves an apparent conflict that is actually a scope conflict. GD is making a historical accuracy claim: at PR #99, SC 4 was open. IP is making a prioritization claim: SC 4 should be treated as P2 for scheduling purposes going forward. Both claims are true, and each is correct within its domain. Collapsing them in either direction produces distortion: adopting only GD's framing would imply retroactive P1 escalation that the SIR's deliberate sequencing judgment doesn't warrant; adopting only IP's framing would produce a historical record that mischaracterizes which criteria were satisfied at PR #99 closure. Future amendment authors need both: they need to know SC 4 was open (to accurately understand what "spec closure" has historically meant), and they need to know the forward obligation is P2 (to sequence their own work correctly).

**Rejected position:** Neither position is rejected in substance; only the framing that one position eliminates the other is rejected. IP's strongest argument — that the SIR's contemporaneous judgment should govern — is accepted for forward-looking prioritization. GD's strongest argument — that the SIR cannot override the spec's own acceptance bar — is accepted for historical characterization. Both are preserved.

**Required changes:**
- `CONSTITUTIONAL_CONVERSATIONS.md` (cycle 2 entry for PR #99 / v3.0.0 ratification): Add a note to the cycle 2 entry stating that spec 070 §5.3 SC 4 was open at PR #99 merge time — the Governance section lacked a cross-reference pointer to CONTRIBUTING.md and docs/output-conventions.md as migration destinations, and the v3.0.0 SIR explicitly deferred this to a follow-up PATCH. This note should be added as part of the coordinated CONCONV update (confirmed convergence point) alongside the §9 AC #5 status note and the re-verification sub-sections. It must not be written as a retrospective criticism of a deliberate deferral decision, but as an accurate historical characterization of which criteria were open.
- `CONSTITUTION.md` (Governance section): Add the "Operational guidance documents" subsection listing CONTRIBUTING.md (§ Authoring Conventions) and `docs/output-conventions.md` as canonical migration destinations for VI and X content. This discharges the v3.0.0 SIR's explicit commitment. Priority: P2. Proceeds without waiting for §9.5 resolution (per Dispute 4 ruling above).

---

### Summary of Changes Required

**P0 — Blocking spec closure:**

1. **Run supplemental blind deliberation with contrarian agent** (from confirmed convergence point, not a dispute ruling): Configure a new blind deliberation against a pre-cycle-1 document (v2.4.0 or v2.5.0 era CONSTITUTION.md containing Principles VI, X, and XVI in un-migrated form) with at least one agent explicitly prompted to argue one or more of VI/X/XVI passes the v2.4.0 gate on closer reading and should NOT be migrated. Use `presets/role/devils-advocate.yml` for the skeptic role. Target document must be authenticated against git history before the run commences. File under `deliberations/070-supplemental-blind-YYYY-MM-DD/`. Priority: P0.

2. **Correct `specs/done/` placement** (from confirmed convergence point): Either (a) move spec 070 back to `specs/` pending §9 AC #5 satisfaction, or (b) file a named follow-up spec whose explicit purpose is to satisfy spec 070's unmet §9 AC #5, carrying its own spec 067 verification trail and an explicit statement that spec 070's `specs/done/` placement preceded §9 AC #5 satisfaction. The follow-up spec must be placed in active `specs/` directory; the `specs/done/` placement must be reversed until AC #5 is certified. Priority: P0.

**P2 — Secondary corrections (not blocked by §9.5 except as noted):**

3. **Add §4.1(c) concrete examples to `CONTRIBUTING.md`** (from Dispute 1 ruling, refined by Dispute 2 sequencing constraint): Add 2–3 concrete examples from actual `skills/`, `presets/`, and `templates/` files. Not blocked by §9.5, but must not merge until the supplemental blind deliberation has filed its initial verdict; PR description must carry explicit contingency note. Priority: P2.

4. **Add Governance operational-guidance list to `CONSTITUTION.md`** (from Dispute 5 ruling and confirmed convergence): Add subsection listing CONTRIBUTING.md and `docs/output-conventions.md` as canonical operational-guidance destinations for migrated VI and X content. Not blocked by §9.5. Priority: P2.

5. **Coordinated `CONSTITUTIONAL_CONVERSATIONS.md` update** (from confirmed convergence + Dispute 5 ruling): Single PR addressing: (a) re-verification sub-sections for cycle 1 and cycle 2 entries; (b) note on cycle 2 blind target's post-migration status and §9 AC #5 non-satisfaction; (c) note that §5.3 SC 4 was open at PR #99 closure; (d) verification that spec-level §6.1/§6.2 entries exist independently of implementation-cycle entries. Not blocked by §9.5. Priority: P2.

6. **Relocate `docs/output-conventions.md` checkable bullets** (from confirmed convergence): Move `summary/final.md` entry-point bullet and directory-depth bullet from Conventions section to Recommended implementation patterns section, verbatim. Not blocked by §9.5. Priority: P2.

7. **File XIX Operational constants migration eligibility tracking issue** (from confirmed convergence): File GitHub issue referencing the v3.1.1 SIR's "NOT filed as an issue here" language. Not blocked by §9.5. Priority: P2.

8. **Add false-attribution correction to synthesis record** (from Dispute 3 ruling): Add explicit statement that GD's §6.2 finding is independent of AF's review, both findings stand at full weight, and the manufactured contradiction in GD's Phase 2 cross-review rested on misattributed evidence. This may be handled as an annotation in the CONCONV coordinated update (item 5 above) or as a note in this resolution's propagation to the synthesis record. Priority: P2.

---

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| §4.1(c) examples priority | P2 (GD + IP position) | High | AF's own "substantively sound" characterization of the migration undermines P1; §5.3 Success Criteria language does not enumerate §4.1(c) items individually; GD + IP + synthesizer all converge on P2 |
| §4.1(c) examples sequencing | Parallel with documented contingency and initial-verdict light gate | High | Synthesizer's light gate resolves GD's structural-dependency concern without hard serialization; all three agents accept the contingency-documentation mechanism in their Flexibility sections |
| False attribution — manufactured contradiction | Accept AF: no contradiction; both findings independent and additive | High | Factual finding confirmed by direct examination of deliberation artifacts; GD's revision behavior (not reproducing attribution) is consistent with error recognized; synthesizer confirmed |
| Scope of P0 blocking | IP's distinction adopted with synthesizer's bright-line test | High | Spec 070 §5.3's parallel-conditions structure does not make verification a gate on hygiene work; GD's broadest claim (all downstream work) would block accurate record-keeping, which is counterproductive |
| Governance list framing | Bifurcate: GD correct for historical record; IP correct for forward action | High | Both framings are accurate within their domains; the appearance of conflict is a scope conflict; precedent from GD's own Dispute 2 proposed resolution endorses bifurcation; synthesizer's recommended resolution is the correct analytical move |

**Overall assessment:** This deliberation is of high quality. The three agents covered genuinely different analytical surfaces (content fidelity, process completeness, governance pragmatics), and the substantive disputes all reflect real tradeoffs rather than factual disagreements. The five remaining disputes were edge cases about classification precision (P1 vs. P2), operational sequencing (parallel vs. serial), record-keeping accuracy (false attribution), scope determination (what P0 blocks), and framing compatibility (historical vs. forward-looking). None required overturning a substantive finding; all were resolvable by applying the spec's own language to the classification questions the agents raised.

The systemic issue the synthesis correctly identifies — that spec 070 §9 AC #5 was not satisfied before `specs/done/` placement — is the most significant finding and drives the overall verdict. This is not a normal edge case; it is a structural gap in the closure process that the spec's own verification architecture was designed to prevent. The self-certification gap identified by the synthesis (an implementer placing a spec in `specs/done/` without producing the external verification artifact that §9 AC #5 required) represents a governance process failure that the remediation plan must correct before the record can accurately reflect spec 070 as complete.

---

**SPEC-070-CLOSURE VERDICT: PREMATURE — REOPEN**

Spec 070's placement in `specs/done/` was premature. Spec 070 §9 AC #5 — which requires a blind verification deliberation configured with a contrarian agent explicitly arguing one or more of VI/X/XVI passes the v2.4.0 gate on closer reading and should NOT be migrated, run against a pre-migration document — was not satisfied before PR #99 merged. The cycle 2 blind deliberation ran against `CONSTITUTION-v3.0.0-blind.md`, a post-migration document from which VI and X were already absent, making the required contrarian argument structurally impossible to construct regardless of agent configuration. The cycle 1 blind deliberation ran against XVI under a structural incoherence / redundancy framing, not a passes-the-gate-and-should-NOT-be-migrated framing.

Additionally, spec 070 §5.3 SC 4 (cross-references from other principles, specs, and skills point at the new location) was open at PR #99 merge time: the Governance section lacked the cross-reference pointer to CONTRIBUTING.md and docs/output-conventions.md that the v3.0.0 SIR itself committed to in a P2 follow-up.

The remedy is one of two equivalent paths: (a) move spec 070 back to `specs/` and complete the supplemental blind deliberation per §6.2 before re-closing, or (b) file a named follow-up spec with its own `specs/` directory placement, an explicit statement that spec 070's `specs/done/` placement preceded §9 AC #5 satisfaction, and a spec 067 verification trail tied to the contrarian deliberation completing. Path (b) must meet all three conditions from the convergence point; a follow-up spec that adds content improvements without explicitly naming the §9 AC #5 gap does not correct the false certification.

All P2 governance hygiene items identified above may proceed in parallel with this remediation, with the exception of §4.1(c) examples (which must not merge until the supplemental blind deliberation files its initial verdict per the Dispute 2 ruling).