I'll read all the required files to understand the deliberation and make my rulings. Let me start with my grounding document.

# Process Note

This arbitration was activated under the `always` condition for this cooperative deliberation. Four disputes remain from the synthesis after a thorough four-phase deliberation process. The participating agents were: tier-classifier, inclusion-criteria-auditor, admission-auditor-oss, and admission-auditor-enhanced. This is a **cooperative** deliberation with subject arbitration, where I serve as the system being reviewed and have operational knowledge of the design intent.

# Decision Framework

Drawing from `/Users/business-daddy/code/payer-index-mono/conversus-oss/CONSTITUTION.md` v3.2.3, the following principles are relevant to the remaining disputes:

- **Constitutional Inclusion Criteria (§ Governance, lines 2018-2091)**: Principles qualify for constitutional inclusion only if they satisfy mechanical verification capability, falsifiable scope, and distinctness from existing principles.
- **Grandfathering Immunity (§ Governance, lines 2075-2091)**: Pre-v2.4.0 principles retain ratified status and are protected from Constitutional Inclusion Criteria re-evaluation.
- **Principle Number Stability (§ Governance, Principle Number Stability subsection)**: Principle numbers are stable interfaces; tier reclassification cannot re-trigger Constitutional Inclusion Criteria evaluation.
- **Constitutional Authority Hierarchy (§ Governance)**: The constitution governs when specs or other guidance conflict; CONSTITUTION.md takes precedence over subsidiary compliance documents.
- **Amendment Pathway Requirements (§ Governance)**: MAJOR amendments require full deliberation process including self-consistency and blind verification.
- **Spec-Implementation Parity (Principle XIV)**: The spec and implementation must agree; drift between spec and reality is a defect requiring correction.
- **Single Source of Truth (Principle XI)**: Every piece of information must have exactly one authoritative source; duplicates create drift.

# Binding Decisions

## Dispute: Constitutional Procedure vs. Substantive Compliance Sequencing

**Positions:**
- **inclusion-criteria-auditor**: False compliance claims must be corrected before grandfathering interpretation matters; constitutional honesty is prerequisite to constitutional theory.
- **admission-auditor-enhanced**: Verification contingent on admission avoids procedural deadlock while preserving compliance rigor.

**Synthesizer's assessment:** The synthesis identified this as a dispute between "amendment execution vs. constitutional honesty" with different approaches to sequencing procedural questions and compliance verification.

**Ruling:** Adopt admission-auditor-enhanced's position - verification contingent on admission with immediate remediation deadlines if gaps are found.

**Grounding citation:** Constitutional Authority Hierarchy principle and Amendment Pathway Requirements. The constitution establishes that MAJOR amendments follow a specific pathway (originating → spec → verification → ratification). Blocking the amendment pathway for compliance questions that can be resolved within the amendment process violates the established constitutional procedure.

**Rationale:** Constitutional procedure must enable rather than obstruct constitutional governance. admission-auditor-enhanced correctly identified that requiring perfect compliance before establishing governance infrastructure creates a chicken-and-egg problem. The tier extraction amendment's purpose is to establish suite governance; suite members cannot exist without governance, but governance cannot function without members to govern.

**Rejected position:** inclusion-criteria-auditor's insistence on resolving false compliance claims first would create procedural deadlock. While constitutional honesty is important, the constitutional framework provides mechanisms for addressing compliance issues within the amendment process rather than blocking it entirely.

**Required changes:** Proceed with tier extraction amendment using verification-contingent-on-admission for disputed compliance claims, with immediate remediation deadlines established upon admission.

## Dispute: Mechanical Verification Authority for Grandfathered Principles

**Positions:**
- **admission-auditor-oss**: Technical findings about CI enforcement gaps remain valid regardless of grandfathering status; grandfathering protects principle validity, not compliance auditing accuracy.
- **inclusion-criteria-auditor**: Grandfathered principles retain immunity from gate re-evaluation including evidence standards from Constitutional Inclusion Criteria.

**Synthesizer's assessment:** The synthesis noted this as "compliance accountability vs. constitutional stability" with questions about whether grandfathering protects compliance claims or just principle existence.

**Ruling:** Adopt admission-auditor-oss's position - grandfathering protects principle validity but not demonstrably false compliance claims.

**Grounding citation:** Grandfathering Immunity provision and Spec-Implementation Parity (Principle XIV). Grandfathering was designed to protect constitutional validity of pre-gate principles, not to immunize false factual claims about implementation status. Principle XIV requires that specs and implementation agree; this applies to compliance declarations regardless of principle age.

**Rationale:** Grandfathering immunity applies to constitutional validity (preventing principle removal due to Constitutional Inclusion Criteria failures), not to factual accuracy of implementation claims. admission-auditor-oss's technical findings about CI enforcement gaps are empirical audit findings, not constitutional interpretations. If repos claim "Satisfied" on grandfathered principles while lacking the stated implementation mechanisms, this violates Principle XIV regardless of grandfathering status.

**Rejected position:** inclusion-criteria-auditor's position would create an unauditable class of principles where factual compliance claims are immune from verification. This undermines constitutional accountability and violates Principle XIV's requirement for spec-implementation parity.

**Required changes:** Establish that grandfathering protects constitutional validity but not factual accuracy of compliance claims. Technical audit findings about implementation gaps remain valid and actionable for grandfathered principles.

## Dispute: Cross-Repo Coordination Infrastructure Timing

**Positions:**
- **admission-auditor-oss**: Coordination infrastructure must be established before coordinated deadlines; current mechanisms are inadequate for atomic delivery of cross-repo remediations.
- **admission-auditor-enhanced**: Joint tracking issues are sufficient coordination infrastructure for cross-repo remediations.

**Synthesizer's assessment:** The synthesis identified this as "realistic implementation vs. procedural progress" with questions about coordination mechanism adequacy.

**Ruling:** Adopt admission-auditor-oss's position - establish coordination infrastructure before setting coordinated deadlines.

**Grounding citation:** Single Source of Truth (Principle XI) and Constitutional Authority Hierarchy. Cross-repo coordination requires actual coordination mechanisms, not just parallel tracking. The constitution requires single sources of truth; coordinated deadlines without coordination mechanisms create multiple independent sources making the same claim without coordination infrastructure to ensure consistency.

**Rationale:** admission-auditor-oss correctly identified that joint tracking issues are project management tools, not coordination infrastructure. The XXII remediation deadline clustering (both repos targeting 2026-08-01 with "spec 077 TBD") demonstrates the coordination gap. Independent repos with independent release cycles cannot guarantee atomic delivery without explicit coordination mechanisms.

**Rejected position:** admission-auditor-enhanced's assumption that joint tracking issues provide sufficient coordination infrastructure underestimates coordination complexity. Tracking progress is not the same as ensuring atomic delivery across independent governance boundaries.

**Required changes:** Before setting coordinated Provisional deadlines, establish coordination mechanisms including: shared specifications for coordinated work, explicit dependency ordering for non-atomic delivery, or coordination failure recovery procedures.

## Dispute: Templating Surface Investigation Approach

**Positions:**
- **tier-classifier**: Empirical audit must precede tier classification decisions to prevent immediate compliance failures.
- **admission-auditor-enhanced**: Templating surface investigation should be independent of tier reclassification timing; factual questions should be resolved regardless of analytical frameworks.

**Synthesizer's assessment:** The synthesis characterized this as "methodological rigor vs. immediate compliance accuracy" with different approaches to investigation sequencing.

**Ruling:** Adopt tier-classifier's position - empirical audit must precede tier classification.

**Grounding citation:** Spec-Implementation Parity (Principle XIV) and Constitutional Inclusion Criteria enforcement. Tier classification creates constitutional requirements; if classification is based on incorrect factual assumptions, it creates immediate constitutional violations. Principle XIV requires specs (tier assignments) to match implementation (actual repo surfaces).

**Rationale:** tier-classifier identified a critical methodological point: tier reclassification without empirical verification of the surface being classified creates constitutional requirements repos cannot meet. If VIII moves to Suite tier while conversus has local templates contradicting its N/A claim, tier extraction creates immediate compliance failures on day one of the new constitutional structure.

**Rejected position:** admission-auditor-enhanced's separation of factual investigation from tier classification timing treats them as independent when they are constitutionally linked. Factual accuracy about templating surfaces directly determines appropriate tier placement; the investigations cannot be meaningfully separated.

**Required changes:** Conduct empirical audit of actual templating surfaces in both repos before finalizing tier assignments. If audit reveals templating surfaces in repos claiming N/A, either update tier classification or require compliance claim corrections.

# Summary of Changes Required

1. **Verification-contingent admission approach** (from Dispute 1): Establish admission with immediate empirical verification requirements post-admission, avoiding procedural deadlock. Priority: P1.

2. **Grandfathering scope clarification** (from Dispute 2): Document that grandfathering protects constitutional validity but not factual accuracy of compliance claims. Technical audit findings remain valid for grandfathered principles. Priority: P1.

3. **Coordination infrastructure before coordinated deadlines** (from Dispute 3): Establish coordination mechanisms (shared specs, dependency ordering, or failure recovery) before setting cross-repo remediation deadlines. Priority: P1.

4. **Empirical audit before tier finalization** (from Dispute 4): Conduct current-state audit of templating surfaces in both repos before finalizing tier assignments to ensure classification accuracy. Priority: P1.

# Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| Constitutional procedure sequencing | Verification contingent on admission | High | Strong constitutional grounding in amendment pathway requirements; procedural deadlock violates constitutional design |
| Grandfathering authority scope | Technical findings remain valid | High | Clear distinction between constitutional validity (protected) and factual accuracy (not protected) in grandfathering provisions |
| Coordination infrastructure timing | Infrastructure before coordinated deadlines | High | Principle XI requires actual coordination mechanisms, not just tracking; coordination complexity underestimated by opposing position |
| Templating surface investigation | Empirical audit before classification | Medium | Strong methodological grounding, but templating surface scope is limited; consequences of wrong classification are manageable |

The deliberation quality was high, with systematic critique preventing rubber-stamp approval and evidence-based revision preventing hasty tier extraction. The unanimous convergence on grandfathering-reclassification interaction resolution provides a solid procedural foundation. The disputes were genuine edge cases arising from coordination complexity rather than fundamental design flaws.

**Q1 RULING: APPROVE-AS-DRAFTED — the 10/10/6 tier classification proceeds contingent on empirical audit verification of templating surfaces**

**Q2 RULING: ADMIT-PROVISIONAL — admission with immediate verification of technical audit findings and coordination infrastructure establishment**

**Q3 RULING: ADMIT-PROVISIONAL — admission contingent on empirical verification of Plugin Isolation and templating surface claims post-PR #30**