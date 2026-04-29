### Executive Summary

CONSTITUTION-v2.5.0-candidate.md introduces Principle XXVIII (Test-Fix Boundary Preservation) with extensive empirical claims anchored to PR #42 and a 2026-04-28 investigation that allegedly found 95 failing tests, 1 production bug, and established a disciplined approach to test fixing. The principle aims to codify test-fix discipline to prevent production bugs from being buried behind mechanical test fixes. However, the constitution contains multiple unverified empirical claims and relies on evidence artifacts that are either not present in the repository or referenced without validation. The evidence grounding is fundamentally compromised by the absence of the supporting investigation outputs, PR #42 verification, and the mechanical verification script that supposedly satisfies the Constitutional Inclusion Criteria. **Most critical recommendation: Flag this amendment as "evidence-pending" until the supporting investigation artifacts, PR #42 analysis, and mechanical verification capabilities can be independently validated.**

### Alignment

- **Empirical claim structure** (L45-60): The SIR follows a structured approach to documenting rationale with specific numbers, dates, and references that would be verifiable if the supporting evidence existed.
- **Constitutional Inclusion Criteria application** (L16-34): The assessment methodically addresses all three criteria (mechanical verification, falsifiable scope, distinctness) as required by the v2.4.0 governance gate.
- **Origin note cross-referencing** (L1131-1135): Principle XXVIII includes a proper Origin note that cross-references the same investigation claimed in the SIR, maintaining consistency in the evidence narrative.
- **Follow-up artifact planning** (L35-44): The SIR explicitly identifies follow-up PRs and their scope (lint script, PR template, spec amendments) rather than leaving implementation unclear.

### Missed Opportunities

- **Evidence validation protocol**: The constitution provides no mechanism for validating empirical claims before ratification. Without a "show your work" requirement, constitutional amendments can make unverifiable assertions about prior events.
- **Investigation output preservation**: The constitution lacks requirements for preserving the deliberation artifacts that support constitutional amendments. The referenced "4-subagent investigation outputs" and "2026-04-28 4-subagent investigation" are not locatable for verification.
- **Mechanical verification temporal requirements**: The Constitutional Inclusion Criteria gate allows principles to be ratified based on promised future scripts rather than existing ones. This creates a gap where principles can pass the gate without demonstrable mechanical verification.
- **PR anchoring verification**: When amendments claim to be anchored in specific PRs (like PR #42), no verification process confirms the claimed relationship exists or that the PR exemplifies the principle being codified.
- **Counterfactual evidence standards**: The SIR makes counterfactual claims ("A naive sweep would have buried the production bugs") without establishing standards for what evidence would support or refute such claims.
- **Spec reference validation**: Multiple spec references (045, 067, 069, 071) are cited without validation that they contain the claimed content or support the claimed relationships.

### Off-Base Assumptions

- **Investigation outputs exist** (L43, L1131): The constitution assumes the "2026-04-28 4-subagent investigation" outputs exist and are accessible for validation, but they are not present in the repository structure provided.
- **PR #42 exemplifies the principle** (L43, L47): The text assumes PR #42 demonstrates the engine/handlers.py import shadowing fix and serves as the "canonical exemplar" without evidence that this PR exists or contains the claimed content.
- **Promised scripts satisfy mechanical verification** (L16-22): The SIR assumes that describing a future `scripts/lint-test-fixes.py` satisfies the Constitutional Inclusion Criteria requirement for mechanical verification capability, even though the script doesn't exist.

### Actionable Recommendations

1. **Flag amendment as evidence-pending** (Priority: P1)
   - **Current state**: SIR claims validation based on specific investigation outputs and PR #42 (L43-60, L1131-1135).
   - **Proposed change**: Add "Evidence Status: PENDING — claims validation deferred pending location of supporting artifacts" to the SIR header.
   - **Rationale**: The empirical claims are unverifiable without the referenced investigation outputs, PR #42, and spec documents.
   - **Risk if ignored**: Constitutional amendments will be ratified based on unverifiable claims, undermining the constitutional authority.

2. **Require investigation artifact preservation** (Priority: P1)
   - **Current state**: SIR references "4-subagent investigation outputs" and categorization results without providing access to these artifacts (L46-50).
   - **Proposed change**: Constitutional amendments citing investigation results MUST preserve the investigation artifacts in the `deliberations/` directory structure.
   - **Rationale**: Evidence grounding requires access to the actual evidence, not just claims about it.
   - **Risk if ignored**: Future constitutional disputes cannot be resolved because supporting evidence is inaccessible.

3. **Verify PR #42 anchoring claims** (Priority: P1)
   - **Current state**: Multiple references to PR #42 as containing engine/handlers.py import shadowing fix and serving as "canonical exemplar" (L43, L47, L1132).
   - **Proposed change**: Before ratification, validate that PR #42 exists, contains the claimed fix, and demonstrates the principle being codified.
   - **Rationale**: Constitutional principles anchored to specific PRs must be verifiable against those PRs.
   - **Risk if ignored**: The principle may be anchored to nonexistent or irrelevant evidence.

4. **Implement mechanical verification before ratification** (Priority: P1)
   - **Current state**: SIR claims Criterion 1 satisfaction based on promised `scripts/lint-test-fixes.py` (L16-22).
   - **Proposed change**: Require actual implementation of the lint script or explicit deferral of Criterion 1 satisfaction to a future amendment.
   - **Rationale**: The Constitutional Inclusion Criteria gate should verify actual capability, not promised capability.
   - **Risk if ignored**: Principles pass the gate without demonstrable mechanical verification, creating enforcement gaps.

5. **Validate spec reference accuracy** (Priority: P2)
   - **Current state**: Multiple spec references (045, 067 §4.6, 069, 071) cited without verification (L41-42, L61-67).
   - **Proposed change**: Before ratification, verify that referenced specs exist and contain the claimed content.
   - **Rationale**: Constitutional cross-references must be accurate for the constitution to serve as authoritative guidance.
   - **Risk if ignored**: Constitution contains broken or misleading cross-references.

6. **Establish counterfactual evidence standards** (Priority: P2)
   - **Current state**: SIR makes counterfactual claim about what "naive sweep would have buried" without evidence standards (L51-53).
   - **Proposed change**: Define standards for what evidence supports counterfactual claims in constitutional rationale.
   - **Rationale**: Counterfactuals require specific evidence patterns to be credible.
   - **Risk if ignored**: Constitutional rationale can include unverifiable speculation.

7. **Document evidence gap acknowledgment** (Priority: P3)
   - **Current state**: SIR presents claims as verified facts when evidence status is uncertain.
   - **Proposed change**: Explicitly acknowledge which claims are pending verification in the SIR text.
   - **Rationale**: Transparency about evidence status helps readers assess constitutional reliability.
   - **Risk if ignored**: Readers may assume unverified claims have been validated.

### Referenced Documentation

- `CONSTITUTION-v2.5.0-candidate.md` — sections/lines cited: L16-22 (Criterion 1 assessment), L35-44 (follow-up artifacts), L43 (PR #42 reference), L45-60 (SIR rationale), L1131-1135 (Principle XXVIII Origin note), L1186-1192 (Constitutional Inclusion Criteria mechanical verification requirement)