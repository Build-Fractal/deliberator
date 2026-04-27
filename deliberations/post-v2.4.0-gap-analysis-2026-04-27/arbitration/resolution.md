# Arbitration — Post-v2.4.0 Gap Analysis (2026-04-27)

**Arbiter**: post-v2.4.0-arbiter (balanced-arbiter preset)
**Influence**: binding
**Trigger**: always
**Grounding**: CONSTITUTION.md v2.4.0 + recent-changes.md (PRs #15-#33)
**Acting under**: Governance §Constitutional Inclusion Criteria (v2.4.0)

---

## Process Note

- **Trigger**: `always` — this arbitration runs regardless of dispute count, per the v2.4.0 deliberation methodology for constitutional gap analyses.
- **Disputes remaining (per synthesis)**: 4 substantive disputes surfaced from cross-reviews and Phase-3 revisions. The four formal Phase 4 dispute files are empty (stream-failure stubs / cooperative-mode folding into Phase 3). The synthesis's "Remaining Disputes" section is the authoritative dispute record.
- **Agents**: governance, methodology, distribution, practitioner.
- **Mode**: cooperative with subject arbitration.
- **Scope note**: this is a forward-looking gap analysis. Rulings here are not blocking any merge; they direct subsequent amendment, spec-update, and operational-document PRs.
- **Arbitration posture**: the synthesizer recommended **zero** new principles. Per the brief's instructions, that is the strongest signal — I override only if a dispute reveals a finding the synthesizer missed. After review, I do not override the synthesizer's recommendations on any of the four disputes; I rule each as the synthesizer's recommended resolution would suggest, and I record the gate-criterion reasoning explicitly.

---

## Decision Framework

The following principles from CONSTITUTION.md v2.4.0 bear on the four remaining disputes. Each citation is to the ratified text reviewed at the start of this arbitration.

- **The Constitutional Inclusion Criteria gate** (Governance section, lines ~1077-1143): a principle qualifies for inclusion only if it satisfies all three criteria — (1) **mechanical verification capability** (CI lint, parity test, structural assertion, schema validation, or equivalent feasible such that a violating PR fails the check); (2) **falsifiable scope** (wording specific enough to flag a hypothetical PR without "interpretation"); (3) **distinctness** (covers concerns not addressable by composing existing principles). Failure of any criterion routes the proposal to operational guidance. Extension blocks are gate-exempt for criterion 3 by construction but MUST include the Verification artifact (criterion 1) when introducing new normative requirements and MUST declare in one sentence why the content belongs in the parent principle's body. **This gate is the primary instrument applied throughout this arbitration.**

- **Principle XI — Single Source of Truth** (lines ~431-474): every piece of information has exactly one authoritative source; v2.3.0 Registry-First Declaration extension establishes the registry as authoritative for tool/prompt/skill availability. Bears on Dispute 3 (governance-artifact authority placement).

- **Principle XII — No Dead Infrastructure** (lines ~476-498): every provisioned capability must have at least one consumer. Bears on Dispute 3 (stale-artifact detection placement).

- **Principle XVII — Content Classification** (lines ~686-713): execution logic and contribution guidelines must live in separate formats; runtime-enforced rules cannot split across both. The gate's "Coordination with Principle XVII" clause inherits this vocabulary for routing decisions to operational guidance. Bears on all four disputes.

- **Principle XXV — Live Test Cost Discipline** (lines ~923-966): tests that incur real-world cost must follow four discipline rules (explicit marker, cost justification, CI opt-out by default, taxonomy). Foundational for XXIII per its own text. Bears on Dispute 4 (cost-discipline placement).

- **Versioning** (lines ~1075-1076): MAJOR for principle removals or redefinitions; MINOR for new principles or material expansions; PATCH for clarifications. Bears on the version-bump recommendation for any ACCEPT.

- **Grandfathering disclosure** (lines ~28-36 of the v2.4.0 Sync Impact Report): the gate applies prospectively; existing principles I-XXVII are grandfathered; migration of any pre-gate principle to operational guidance is a separate intentional act governed by the same amendment process. Bears on Dispute 2 (grandfathering migration timeline).

---

## Binding Decisions

### Dispute 1: Constitutional Growth Direction (Add vs. Subtract)

**Positions:**
- **Practitioner**: Audit all 27 principles against the v2.4.0 gate; migrate failures to operational guidance; target ~15 principles; codify the size cap as a constitutional principle itself. Halt new additions until audit completes.
- **Governance / Methodology / Distribution**: Reject a constitutional size cap. Establish an *operational* growth budget in CONTRIBUTING.md instead. Allow audit and additions to proceed in parallel, with the v2.4.0 gate continuing to filter additions on their merits.

**Synthesizer's assessment:** "The cap-as-principle proposal is the weakest of practitioner's positions — it materially fails criterion 3 (distinctness from the gate itself, which already prevents bloat) and arguably criterion 1 (mechanical verification 'principle count <= 15' is trivially mechanical but the principle's *binding force* depends on which principle to remove, which is a judgment call). However, practitioner's underlying observation — that the panel structurally favors expansion — is correct, and the audit-of-existing-principles work is sound."

**Ruling:** **REJECT** the 15-principle cap as a constitutional principle (practitioner P3 modified). **OPERATIONAL** for the audit work itself (practitioner P1 modified) and for the growth-budget rule (governance Phase-3 add).

**Grounding citation:** v2.4.0 Constitutional Inclusion Criteria, criterion 3 (distinctness). The cap-as-principle composes from the gate itself (which is precisely the bloat-prevention mechanism) plus a process rule about migration; it does not introduce a distinct invariant. Criterion 1 is also weakly satisfied at best — `len(principles) <= 15` is a trivial count check, but the *binding* version requires choosing which principle to remove or block, which is a judgment call rather than a mechanical assertion against a hypothetical PR.

**Rationale:** A numeric cap is a forcing function, not an invariant. The constitution's job is to encode invariants; bounding *its own size* is what the inclusion gate already does, and a hard quota would create perverse incentives to push genuine invariants into operational guidance to stay under the line. Practitioner's diagnosis (panel composition structurally favors expansion) is real and is acknowledged in the synthesis's Systemic Contradiction #1 — but the answer to that diagnosis is to keep applying the gate strictly (which this arbitration does) and to mature growth-control discipline operationally first, per Principle XVII's distinction between contribution guidelines and runtime invariants. The audit project is sound and should ship — as a one-time governance project, not a new principle.

**Rejected position:** Practitioner's cap-as-principle. The position has merit as a forcing function but fails the gate, and the underlying concern is fully addressed by (a) continuing to apply the gate, (b) running the audit, and (c) shipping the growth budget as operational guidance.

**Required action:**
- **Audit (OPERATIONAL)**: ship a new spec — call it spec 070 or equivalent — that audits all 27 principles against the v2.4.0 gate, documents pass/fail per criterion, and proposes migration destinations for failures. Target: spec.
- **Growth budget (OPERATIONAL)**: ship a section in `CONTRIBUTING.md` (per spec 065 G7) capping new constitutional content per release window (e.g., max one new principle and two extensions per quarter; exceptions require justification). Target: CONTRIBUTING.md.
- **Distribution D++ (delay-pending-audit) qualifier**: accept only for non-P1 additions; explicit exceptions for verification cost discipline and re-verification triggers (see Dispute 4) on the grounds that those address the verification sustainability crisis the audit will need to operate within.

---

### Dispute 2: Grandfathering Migration Timeline

**Positions:**
- **Practitioner**: 90-day audit, 9-month migration completion (modified from original 30/180).
- **Governance**: No fixed timeline; framework establishment first, then migration.
- **Methodology / Distribution**: No specific timelines proposed; sequence (audit → new additions) but no calendar.

**Synthesizer's assessment:** "Practitioner's modified 90/270 timeline is reasonable IF verification cost discipline is in place by day 30. Without the cost framework, verification of migration decisions is itself unbounded. The dispute is real but tractable: sequence cost discipline → audit → migration."

**Ruling:** **OPERATIONAL** — the timeline question is calibration, not invariant. The dispute belongs in the audit spec and CONTRIBUTING.md, not in the constitution. The synthesizer's recommended sequence is adopted as the operational plan.

**Grounding citation:** v2.4.0 Constitutional Inclusion Criteria, criterion 2 (falsifiable scope) and the Governance section's grandfathering disclosure. Calendars and deadlines are calibration parameters; they do not yield a falsifiable invariant ("the constitution shall be migrated by date D" reduces to a process commitment, not a runtime contract). Per the gate's prospective-only scope clause, migration of grandfathered principles is an "intentional act governed by the same amendment process" — meaning each migration is its own amendment, with its own deliberation, on its own timeline.

**Rationale:** The disagreement is a real concern but is not constitutional. Both extremes have merit (aggressive timeline preserves gate credibility; framework-first prevents ad-hoc migrations). The synthesizer's sequence — land cost discipline (Dispute 4) first, then begin audit at day 30, then migration spec at day 120, completion at day 300 — is the right operational path because it makes the audit's verification budget predictable. Codifying any of those dates in the constitution would either harden a calibration choice into an invariant or create a self-violating principle if a date slips for legitimate reasons.

**Rejected position:** Both ends of the dispute are partially rejected at the constitutional level. Practitioner's hard 90/270 calendar fails the gate. Governance's open-ended "no timeline" is operationally insufficient. The compromise is: hard sequencing (cost first → audit → migration), soft calendar (target dates in the audit spec, revisable on evidence).

**Required action:**
- **Sequence (OPERATIONAL)**: in the audit spec (Dispute 1's required action), specify the dependency chain explicitly: cost-discipline extension to XXV (Dispute 4) lands first; audit begins after that PR merges; migration spec for VI/X/XVI lands at audit completion; migration completion is governed by the per-principle migration amendments, each on its own deliberation track.
- **Default targets**: 30 days for cost discipline, 120 days for audit completion, 300 days for migration completion. Recorded as targets in the audit spec, NOT in the constitution, NOT in CONTRIBUTING.md as deadlines. If a target slips, the slip is recorded in the governance log without amendment.
- **Per-principle migration amendments**: VI (Scripts Over Markdown) → AGENTS.md / SKILL.md operational guidance (synthesizer suggests XVII operational guidance; arbiter agrees). X (Zen of Python Output) → agentskills.io style guide or equivalent (synthesizer suggestion accepted). XVI (Mathematical Transparency) → spec 014 contract test for the plain-language requirement (synthesizer suggestion accepted; the v2.3.2 clarification already structures this path).

---

### Dispute 3: Governance-Artifact Discipline Mechanism (XI vs. XII vs. New Principle)

**Positions:**
- **Governance G3 (surviving) / Distribution D1 (modified)**: Extend Principle XI (Single Source of Truth) with a "Governance artifact authority" block.
- **Governance G5 (modified)**: Combine artifact preservation + retention into a single "deliberation governance" new principle.
- **Distribution D6 (surviving, P3)**: Extend Principle XII (No Dead Infrastructure) for stale-artifact detection.

**Synthesizer's assessment:** "XI extension is the cleanest fit for the *authority* question (deliberations/ is the single source for what was deliberated). XII extension is the cleanest fit for the *staleness* question. They are not competing — they address different aspects. A new 'deliberation governance' principle would risk failing the gate's distinctness criterion against XI + XII + XXV composed together."

**Ruling:** **OPERATIONAL** for the new "deliberation governance" combined principle (REJECT under the gate). **OPERATIONAL/EXTENSION-BLOCK** for the XI and XII extension proposals — they are gate-exempt for criterion 3 by construction (Extension blocks) but their wording, normative force, and verification artifact must be specified before they ship as a constitutional amendment. They are not standalone new principles; they ship as Extension blocks in a future PATCH amendment.

**Grounding citation:** v2.4.0 Constitutional Inclusion Criteria, criterion 3 (distinctness) for the standalone new-principle proposal; the Extension-blocks clause for the XI/XII paths. A combined "deliberation governance" principle would compose from XI (authority of source) + XII (no dead infrastructure) + XXV (cost discipline) and fails distinctness on its face. The two Extension paths are architecturally clean — they address different concerns (authority vs. staleness) and each anchors naturally to its parent.

**Rationale:** The synthesizer's split — XI extension for *authority*, XII extension for *staleness* — is correct. They are not competing framings; they are complementary, the same way Principles XV and XXVII bracket the registry's read/write contract. The synthesizer flagged correctly that combining them into one new principle would fail criterion 3 against the composition of three existing principles. Extension blocks are the right vehicle: they preserve XI's and XII's parent-anchor logic, they are gate-exempt for distinctness, and the verification artifact (CI lint over `deliberations/` directory structure + governance-log cross-references) is mechanical and concrete.

**Rejected position:** Governance G5 (combined "deliberation governance" new principle) — fails gate criterion 3. The aspiration to keep deliberation discipline coherent is valid; the answer is *cross-references between extension blocks*, not a new top-level entry.

**Required action:**
- **Extension to Principle XI (OPERATIONAL — pending amendment PR)**: draft a "Governance artifact authority" block declaring `deliberations/{topic}-{date}/`, `CONSTITUTIONAL_CONVERSATIONS.md`, and verification artifacts as the single authoritative source for deliberation history. Required Verification block: CI lint that verifies (1) every constitutional amendment PR adds a `deliberations/{topic}-{date}/` directory; (2) every governance log entry references an existing deliberations directory; (3) deliberations directory structure matches the spec 067/069 layout. Required one-sentence distinctness rationale per the gate's Extension-blocks clause: "deliberation outputs are the authoritative source for deliberation history, parallel to how `schema/variables.yml` is authoritative for variables." **Version bump if shipped: PATCH** (clarification/extension, no new principle).
- **Extension to Principle XII (OPERATIONAL — pending amendment PR)**: draft a stale-artifact-detection sub-bullet declaring `deliberations/` entries without a corresponding governance log entry as dead infrastructure (D6 retained at P3). Verification: CI lint cross-references `deliberations/*` directory listing against `CONSTITUTIONAL_CONVERSATIONS.md` entries. **Version bump if shipped together with the XI extension: PATCH.**
- **REJECT** the standalone "deliberation governance" combined principle proposal.
- **Combined version-bump note**: if the XI and XII extensions ship together with the XXV extension from Dispute 4, the combined amendment is still PATCH (no new principles, all extensions/clarifications).

---

### Dispute 4: Cost-Discipline Placement (XXV Extension vs. New Principle)

**Positions:**
- **Methodology M2 (surviving, P1)**: Reads as standalone "verification cost reporting" requirement.
- **Distribution D5 (modified, P1)**: Extend Principle XXV; explicitly upgraded to P1.
- **Governance G1 (modified, P1)**: "Establish constitutional cost discipline requirements"; mechanism unspecified.
- **Practitioner P2 (surviving, P1)**: Operational thresholds in spec 067, not constitutional.

**Synthesizer's assessment:** "The XXV extension framing won the cross-review consensus (3 of 4 agents). Practitioner's 'operational only' position is internally consistent but loses on the empirical evidence — without constitutional protection, cost reporting will be skipped during budget pressure exactly when it's most needed. The constitutional/operational split is: constitution mandates cost *reporting* (XXV extension); spec 067 sets the *thresholds*."

**Ruling:** **OPERATIONAL/EXTENSION-BLOCK** for the cost-reporting requirement (extends Principle XXV; Extension block, gate-exempt for criterion 3). **OPERATIONAL** for the threshold values (live in spec 067). **REJECT** the standalone new-principle framing.

**Grounding citation:** v2.4.0 Constitutional Inclusion Criteria, Extension-blocks clause; Principle XXV's foundational role for XXIII (provider robustness contract). The standalone new-principle framing fails criterion 3: "cost discipline" composes from XXV's existing four discipline rules (explicit marker, cost justification, CI opt-out, taxonomy) — extending XXV from test costs to deliberation costs is a within-scope expansion, not a distinct invariant. The Extension-block path passes the gate's verification requirement (criterion 1) by lint over governance log entries.

**Rationale:** The split between *reporting* (constitutional) and *thresholds* (operational) is correct because reporting is a structural invariant (a missing cost line is a mechanical failure of the contract) while thresholds are calibration parameters (different amendments have different appropriate caps). XXV is the right parent because its existing discipline structure — visibility, categorization, opt-out by default — generalizes cleanly from API-credit costs to agent-launch costs. The empirical evidence (~34 launches per amendment minimum) is the kind of quantified concern XXV exists to prevent. Practitioner's "operational only" position is internally consistent on cost-as-calibration but loses on the structural-reporting half: without constitutional anchor, the report line will be the first thing dropped under deadline pressure. The 3-of-4 cross-review consensus on XXV extension is dispositive; methodology M2's surviving wording should be rewritten in the implementing PR to match the XXV-extension architecture.

**Rejected position:** Methodology's standalone-new-principle framing (fails criterion 3) and practitioner's pure-operational placement (loses on the structural-reporting half of the split). Both have partial validity that is preserved in the ruling: methodology's P1 priority is upheld; practitioner's threshold-values-in-spec-067 placement is upheld.

**Required action:**
- **Extension to Principle XXV (OPERATIONAL — pending amendment PR)**: draft a "Deliberation cost reporting" block requiring every governance log entry for a constitutional amendment to include a `Verification cost:` line with agent-launch count, approximate token consumption, and wall-clock time. Required Verification block: CI lint over `CONSTITUTIONAL_CONVERSATIONS.md` checks each entry for the cost line. Required one-sentence distinctness rationale per the Extension-blocks clause: "deliberation costs and live test costs share the same cost-discipline invariant (visibility, categorization, opt-out by default), and XXV is already foundational for XXIII via the same pattern." **Version bump if shipped: PATCH** (extension to existing principle).
- **Re-verification triggers (Extension placement)**: place under XI Governance Artifact Authority Extension block (synthesizer's recommendation) on the rationale that the bug being prevented is "preserved artifacts don't match ratified text" — fundamentally an authority-of-source problem. Verification: text-diff classifier over PRs that modify ratified constitutional text + governance log entry schema enforces a `Re-verification status:` line. Ships as part of the same PATCH amendment as the other XI extension content, OR as a follow-up PATCH if the XI extension ships first.
- **Spec 067 modification (OPERATIONAL)**: tiered cost thresholds in the spec, not the constitution. Practitioner P2 absorbed here.
- **REJECT** standalone cost-discipline new principle. Methodology M2's recommendation text should be rewritten to the XXV-extension framing in the implementing PR.

---

## Recommended new principles

(none — the v2.4.0 gate appropriately routed all proposals to operational guidance or to Extension blocks on existing principles, indicating either correct gate calibration or that the post-v2.4.0 layer hasn't accumulated constitutional debt that requires a new top-level invariant.)

The deliberation produced **zero standalone new principles that pass the gate**. The synthesizer's recommendation of zero new principles is upheld in full. Three Extension-block proposals (XI Governance Artifact Authority, XII Stale-Artifact Detection, XXV Deliberation Cost Reporting) plus one Extension-block placement (re-verification triggers under XI) survive arbitration as candidates for a future PATCH amendment. Extension blocks are gate-exempt for criterion 3 by construction; they are not standalone new principles, and their amendment vehicle is PATCH unless the cumulative scope is material enough to warrant MINOR (not the case here).

---

## Recommended operational changes

The arbitration upholds the synthesizer's 14 operational recommendations in full. Each is reproduced below with target document and summary action. Items 15-18 are operational outputs of the four arbitrated disputes that fold cleanly into the same operational layer.

1. **Constitutional principle audit project (one-time).** Audit all 27 principles against the v2.4.0 gate; document migration destinations for VI, X, XVI; schedule additional migrations. **Target**: new spec (call it spec 070 or equivalent). **Source**: practitioner P1 modified, distribution D++.

2. **Verification cost thresholds (tiered).** Tiered launch caps for MINOR / MAJOR / wording-only amendments; explicit single-methodology escape for typo/formatting fixes. **Target**: spec 067 modification. **Source**: practitioner P2.

3. **Constitutional growth budget.** Operational rule capping new constitutional content per release window (e.g., max one new principle and two extensions per quarter; exceptions require justification). **Target**: CONTRIBUTING.md (per spec 065 G7). **Source**: governance Phase-3 add.

4. **Amendment batching guidance.** Quarterly batching for non-urgent constitutional changes; explicit "urgent" exception class. **Target**: CONTRIBUTING.md. **Source**: practitioner P6 modified, governance G2 modified.

5. **Cross-methodology reconciliation procedure.** Documented process for handling self-consistency vs. blind verification disagreements. **Target**: spec 067 §4.5 (new section). **Source**: methodology M6 modified.

6. **Infrastructure failure resilience pattern.** Codify agents-Write-directly pattern; mandate artifact preservation for incomplete runs. **Target**: spec 067 + memory entry. **Source**: methodology M5 surviving.

7. **Reference implementation requirement for documented methodologies.** Methodologies that affect amendment outcomes must include a reference implementation script (PR #25 strip script as exemplar). **Target**: spec 067. **Source**: methodology M+ Phase-3 add, distribution D2 (withdrawn but spirit retained here).

8. **Operational guidance precedence rules.** Hierarchy: Constitution > CONTRIBUTING.md > spec operational guidance > team practices. **Target**: Governance section of CONSTITUTION.md (modify existing text; not a new principle). **Source**: practitioner P5 surviving.

9. **Amendment impact assessment in PR template.** One-paragraph assessment of affected developers, compliance cost, and interactions with existing principles. **Target**: PR template. **Source**: practitioner P7 surviving.

10. **Branch-dependency documentation.** Constitutional amendments may only reference artifacts available on the target deployment branch. **Target**: CONTRIBUTING.md (synthesizer leaned operational; arbiter concurs — Principle II's "stable interfaces" is about *what* contracts are stable, not *where* artifacts live, so an II extension would over-stretch the principle). **Source**: distribution D3 surviving.

11. **Verification script versioning discipline.** Verification scripts (PR #25 strip script and successors) tagged consistently with constitutional versions they support. **Target**: spec 067 §4.2. **Source**: distribution D4 surviving.

12. **Stale artifact detection (CI check).** Mechanical implementation of XII Extension's lint scope — flag deliberations/ entries without a corresponding governance log entry. **Target**: implementation detail of the XII Extension block (Dispute 3). **Source**: distribution D6 surviving.

13. **Distribution surface enumeration mechanism.** Registry-based discovery of distribution surfaces. **Target**: defer to operational implementation when a fourth surface ships; arguably belongs as a Principle XXII extension, but the deliberation did not converge — leave for a future amendment cycle. **Source**: distribution D7 surviving (P3, lowest priority).

14. **Constitutional scope philosophy criteria.** Meta-criteria for deciding constitutional vs. operational placement beyond the v2.4.0 gate. **Target**: Governance section commentary or spec 070 (audit project). **Source**: practitioner P+ Phase-3 add.

15. **Audit / migration / cost-discipline sequencing (Dispute 2).** Hard sequence (cost-discipline Extension first → audit → per-principle migration amendments), soft calendar (targets recorded in audit spec, revisable on evidence). **Target**: audit spec (item 1) and CONTRIBUTING.md sequencing note.

16. **XI Governance Artifact Authority Extension draft (Dispute 3).** Draft and ship as a PATCH amendment; required Verification block specified in the Dispute 3 ruling. **Target**: future PATCH amendment PR.

17. **XII Stale-Artifact Detection Extension draft (Dispute 3).** Ship in the same PATCH amendment as item 16 if scope permits. **Target**: future PATCH amendment PR.

18. **XXV Deliberation Cost Reporting Extension draft (Dispute 4).** Ship in the same PATCH amendment as items 16-17, or as a separate PATCH if it lands first. The re-verification triggers Extension block (Dispute 4 second half) ships under XI per the synthesizer's recommended parent placement. **Target**: future PATCH amendment PR.

---

## Deferred

- **Standalone verification methodology section** (methodology M1 original, modified-but-unconverged version): the wording did not converge across cross-reviews and Phase 3. **Unblock condition**: audit project (operational item 1) clarifies whether dependency-management constitutes a distinct invariant beyond Principle XVII (Content Classification) + spec 067; if yes, draft an XVII Extension or new principle in a subsequent amendment cycle.

- **Distribution surface enumeration mechanism** (distribution D7, operational item 13): borderline against criterion 3 (distinctness vs. XI registry-as-extension-interface). **Unblock condition**: a fourth distribution surface ships, providing concrete evidence of a registry-vs-enumeration gap that XI cannot already address. If the gap surfaces, draft an XXII Extension.

- **Branch-dependency documentation as Principle II Extension** (distribution D3, operational item 10): arbiter ruled operational, but the underlying tension (II's "stable interfaces" vocabulary vs. "where artifacts live") may justify reconsideration. **Unblock condition**: a future amendment encounters a branch-availability bug that operational guidance failed to prevent — at that point reassess II Extension vs. operational guidance.

---

## Rejected

- **Constitutional 15-principle size cap as a principle** (practitioner P3 modified). **Reason**: fails v2.4.0 Constitutional Inclusion Criteria criterion 3 (distinctness — composes from the gate itself plus the migration mechanism); criterion 1 also weakly satisfied at best (the binding force depends on which principle to remove, a judgment call). The audit work and growth-budget rule (operational items 1 and 3) preserve the underlying concern.

- **Standalone "deliberation governance" combined new principle** (governance G5 modified). **Reason**: fails criterion 3 — composes from Principle XI (authority of source) + Principle XII (no dead infrastructure) + Principle XXV (cost discipline). Replaced by three coordinated Extension blocks (operational items 16-18).

- **Standalone "verification cost discipline" new principle** (methodology M2 surviving wording). **Reason**: fails criterion 3 — extends Principle XXV's existing cost-discipline structure rather than introducing a distinct invariant. Replaced by XXV Extension block (operational item 18).

- **Hard 90/270 grandfathering migration calendar in the constitution** (practitioner Phase-3 modified position on Dispute 2). **Reason**: fails criterion 2 (falsifiable scope — calendar deadlines are calibration commitments, not runtime invariants). Replaced by hard-sequence-soft-calendar operational guidance (operational item 15).

- **Formalize-both-methodologies as a constitutional principle** (governance G4, withdrawn in Phase 3). **Reason**: fails criterion 3 — spec 067 already enforces both-methodologies, and Principle XVII routes execution-logic to specs. Withdrawal is upheld.

- **Minimum verification thresholds (floors)** (methodology M3, withdrawn in Phase 3). **Reason**: contradicted practitioner's velocity ceilings; cost ceilings won the cross-review on sustainability grounds. Withdrawal is upheld.

- **Persona compliance, stagnation detection** (methodology M7, M8, withdrawn in Phase 3). **Reason**: spec 067 §4.3.1 already covers persona requirements; stagnation detection is operational. Withdrawals are upheld.

---

**POST-V2.4.0 GAP ANALYSIS: 0 ACCEPT, 14 OPERATIONAL, 3 DEFER, 7 REJECT.**
