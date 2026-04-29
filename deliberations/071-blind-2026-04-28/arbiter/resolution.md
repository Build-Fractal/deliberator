I'll help you arbitrate this constitutional review. Let me start by reading the required documents in the specified order to understand the deliberation and make informed binding decisions.

---

### Process Note

This arbitration was triggered by the `always` condition specified in the deliberation configuration. Three disputes remain from the synthesis phase of this cooperative deliberation with subject arbitration. The participating agents were skeptic-mathematical, skeptic-cross-principle, and practitioner, who conducted a thorough review of Principle XXVIII (Test-Fix Boundary Preservation) in the constitution. This is a **cooperative** deliberation where I, as independent-arbiter, serve as the subject of review with binding decision authority over unresolved disputes.

### Decision Framework

The key principles from the constitution (CONSTITUTION-v2.5.0-blind.md) that govern my decisions on these disputes are:

- **Constitutional Inclusion Criteria (lines 1109-1119)**: A principle qualifies for constitutional inclusion only if it satisfies all three criteria: (1) mechanical verification capability such that "a future PR violating the principle would fail the check," (2) falsifiable scope specific enough to flag violations without interpretation, and (3) distinctness from existing principles.

- **Constitutional Gate Function (lines 1110-1112)**: The inclusion criteria require that a principle "satisfies all three" criteria—this establishes gates as blocking requirements, not parallel concerns.

- **Prospective Application (lines 1147-1151)**: "This gate applies prospectively—to amendments landing after v2.4.0. Existing principles I-XXVII are grandfathered," establishing that constitutional standards apply to future amendments while preserving existing principles' legitimacy.

- **Operational Guidance Distinction (lines 1141-1145)**: "Principles that fail any criterion belong in operational guidance: AGENTS.md, the relevant spec, SKILL.md instructions, or domain-specific reference documents. Operational guidance is the explicit home for 'judgment calls' and 'rules of thumb.'"

- **Constitutional Self-Compliance Requirement**: The constitution establishes its own authority through adherence to its stated principles, particularly the inclusion criteria it defines.

- **Grandfathering Doctrine (lines 1147-1151)**: "Migrating any of [the grandfathered principles] to operational guidance is a separate, intentional act governed by the same amendment process."

- **Evidence Standards and Constitutional Legitimacy**: Constitutional principles derive authority from principled application of standards; retroactive adequacy evaluations undermine this authority.

### Binding Decisions

#### Dispute: Principle constitutional status vs. operational guidance placement

**Positions:**
- **practitioner**: Argues that format-checking-only verification requires moving the principle to operational guidance, stating "Constitutional principles require robust automated enforcement...verifying that categorization was *attempted* does not verify that it was *done correctly*."
- **skeptic-mathematical and skeptic-cross-principle**: Argue partial automation satisfies constitutional inclusion requirements, with skeptic-mathematical stating "partial automation satisfies [constitutional] requirement even if complete automation is not possible."

**Synthesizer's assessment:** The synthesizer found practitioner's position stronger, noting that "Constitutional Inclusion Criterion 1 requires mechanical verification 'such that a future PR violating the principle would fail the check.' Format-checking categorization presence does not verify categorization correctness, which is the principle's actual intent."

**Ruling:** Adopt practitioner's position. Principle XXVIII must be moved to operational guidance due to insufficient mechanical verification capability.

**Grounding citation:** Constitutional Inclusion Criteria (lines 1113-1119) require "at least one form of automated check...MUST be feasible such that a future PR violating the principle would fail the check." The distinction between operational guidance and constitutional principles (lines 1141-1145) explicitly states that principles requiring "judgment calls" belong in operational guidance. Format-checking categorization presence is procedural compliance, not substantive verification of correct categorization—the principle's actual behavioral intent.

**Rationale:** The constitutional inclusion criteria establish a bright-line test for mechanical verification. While format-checking constitutes "a form of automated check," it fails the consequential test: "such that a future PR violating the principle would fail the check." A PR that provides incorrect categorization (e.g., labeling a production bug as "fixture drift") would pass format-checking while violating the principle's substantive requirements. This creates a false sense of enforcement while relying on human reviewer discipline—precisely the scenario operational guidance is designed to handle.

**Rejected position:** skeptic-mathematical and skeptic-cross-principle's partial automation argument conflates procedural compliance with substantive verification. While their position correctly identifies that some automation is feasible, it incorrectly assumes this satisfies Criterion 1. The constitutional standard is not "some automation" but automation that would "fail the check" for actual violations.

**Required changes:** Move Principle XXVIII from the Core Principles section to operational guidance documentation (AGENTS.md or equivalent), implementing the AST parsing automation as operational tooling rather than constitutional enforcement. Update any cross-references to XXVIII throughout the constitution to reflect its new operational guidance status.

#### Dispute: Evidence standards framing for constitutional principles

**Positions:**
- **skeptic-mathematical**: Frames enhanced evidence requirements as fixing inadequate historical evidence, arguing "single-incident principles risk overfitting to their origin circumstances."
- **skeptic-cross-principle**: Prefers framing as enhanced standards for future principles without retroactive judgment, stating "Retroactive inadequacy evaluation undermines constitutional legitimacy."

**Synthesizer's assessment:** The synthesizer found skeptic-cross-principle's position stronger: "Constitutional authority depends on principled application of standards. Retroactively declaring existing principles inadequately evidenced creates precedent for arbitrarily questioning any principle."

**Ruling:** Adopt skeptic-cross-principle's position. Enhanced evidence requirements shall apply prospectively only, framed as strengthened standards for future principles without retroactive inadequacy claims.

**Grounding citation:** The Prospective Application provision (lines 1147-1151) establishes that constitutional changes "apply prospectively" while grandfathering existing principles. The Grandfathering Doctrine explicitly protects existing principles from retroactive evaluation under new standards. Constitutional authority depends on consistent application of established standards rather than post-hoc adequacy judgments.

**Rationale:** Constitutional legitimacy requires stable application of inclusion standards. The constitution itself acknowledges that existing principles were ratified under their historical context and explicitly grandfathers them from new requirements. Retroactively declaring principles inadequately evidenced while keeping them in force creates a precedent for arbitrary constitutional revision based on evolving standards rather than principled application of established criteria.

**Rejected position:** skeptic-mathematical's framing assumes authority to retrospectively evaluate constitutional principles against standards they were not originally required to meet. This approach would destabilize constitutional authority by making any principle subject to future adequacy challenges based on evolving evidence thresholds.

**Required changes:** Draft enhanced evidence requirements that explicitly apply to future constitutional amendments only, with language such as "Enhanced standards for future constitutional principles" and explicit grandfathering acknowledgment for existing principles I-XXVIII.

#### Dispute: Constitutional compliance precedence vs. logical rigor parallel tracking

**Positions:**
- **practitioner**: Treats constitutional distinctness violation as a blocking gate requiring resolution before other improvements, stating "A constitution that violates its own distinctness criterion...has no standing to enforce evidence standards on anyone else."
- **skeptic-mathematical**: Treats constitutional compliance and logical coherence as orthogonal issues requiring parallel resolution, arguing "Constitutional compliance and logical coherence are orthogonal concerns that must both be addressed."

**Synthesizer's assessment:** The synthesizer found practitioner's position stronger: "Constitutional inclusion criteria function as gates—principles that fail distinctness testing should be consolidated or removed before enhancement. The constitution's own integrity requires self-compliance before it can enforce standards on new amendments."

**Ruling:** Adopt practitioner's position. Constitutional compliance issues (RFC 2119 fix, distinctness violation resolution) must be addressed as Priority P1 before logical improvements.

**Grounding citation:** Constitutional Inclusion Criteria (lines 1110-1112) establish that a principle "qualifies for constitutional inclusion only if it satisfies all three" criteria, creating gate functions rather than parallel requirements. Constitutional Self-Compliance Requirement demands that the constitution adhere to its own stated principles before enforcing them on others. The distinctness criterion (Criterion 3, lines 1127-1131) prohibits principles that restate existing principles in different words.

**Rationale:** Constitutional gates are blocking requirements by definition. A principle that violates Criterion 3 (distinctness) fails the constitutional inclusion test and should not receive enhancement until the violation is resolved. Attempting to improve a principle that currently fails constitutional standards legitimizes non-compliance rather than fixing it. The constitution's authority to enforce standards on new amendments depends on its own compliance with established criteria.

**Rejected position:** skeptic-mathematical's orthogonal treatment incorrectly assumes that logical coherence improvements can proceed independently of constitutional compliance. This approach would cement constitutional violations by investing effort in improving non-compliant principles rather than addressing the compliance failure.

**Required changes:** Sequence work as Priority P1 (constitutional compliance: remove redundant assertion language from XXVIII that duplicates IX's behavior-over-shape extension, fix RFC 2119 "MAY NOT" to "MUST NOT" violations) before Priority P2 (logical improvements to remaining text after consolidation).

### Summary of Changes Required

1. **Move Principle XXVIII to operational guidance** (from Dispute: constitutional status): Transfer XXVIII from Core Principles to operational guidance documentation, implementing AST parsing as operational tooling. Priority: P1.

2. **Draft prospective-only enhanced evidence requirements** (from Dispute: evidence standards): Create enhanced evidence standards for future constitutional principles with explicit grandfathering language for existing principles I-XXVIII. Priority: P2.

3. **Sequence constitutional compliance before enhancements** (from Dispute: compliance precedence): Remove redundant assertion language from XXVIII and fix RFC 2119 violations before any logical improvements. Priority: P1.

4. **Update cross-references to reflect XXVIII's new status** (from constitutional status change): Modify any constitutional cross-references to XXVIII throughout the document to reflect its operational guidance classification. Priority: P1.

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| Constitutional status | Move to operational guidance | High | Clear constitutional inclusion criteria with specific mechanical verification requirements; bright-line test failure |
| Evidence standards | Prospective-only application | High | Explicit constitutional language on prospective application and grandfathering; constitutional legitimacy principles |
| Compliance precedence | Constitutional compliance first | High | Constitutional gate structure clearly establishes blocking requirements; self-compliance requirement for constitutional authority |

My overall assessment is that this deliberation identified genuine constitutional compliance issues that require systematic resolution. The disputes were not edge cases but fundamental questions about constitutional standards and self-compliance. The deliberation quality was high, with agents conducting thorough cross-principle analysis that revealed constitutional violations missed in initial reviews. The remaining disputes indicate proper functioning of adversarial review rather than systematic problems—they represent principled disagreements about constitutional standards that required authoritative resolution to prevent ongoing non-compliance.