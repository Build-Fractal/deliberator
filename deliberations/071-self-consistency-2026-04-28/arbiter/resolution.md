I'll read the required files in the specified order to understand the disputes and ground my decisions properly.

---

### Process Note

This arbitration was triggered by the `always` condition specified for spec-071 deliberation. Four disputes remain from the synthesis after the four-agent deliberation process involving wording-precision, cross-principle-coherence, pr-evidence-grounding, and devils-advocate. This is a **cooperative** deliberation with subject arbitration, where I am ruling on disputes about the candidate v2.5.0 constitutional amendment that adds Principle XXVIII (Test-Fix Boundary Preservation).

### Decision Framework

The following principles from the candidate v2.5.0 constitution (grounding document) govern my binding decisions:

- **Constitutional Inclusion Criteria (v2.4.0 Governance section)**: A principle qualifies for constitutional inclusion only if it satisfies all three criteria: (1) mechanical verification capability - at least one form of automated check must be feasible such that a future PR violating the principle would fail the check, (2) falsifiable scope - the principle's wording must be specific enough to flag violations without requiring interpretation, and (3) distinct from existing principles - the principle must cover concerns not already addressable by composing existing principles.

- **Spec-Implementation Parity (Principle XIV)**: Specs and implementations must agree on what was built. When implementation intentionally narrows or broadens the scope of a functional requirement, the spec text must be updated to match. A spec that says one thing when the implementation does another is a bug in the spec.

- **Observable Deliberation (Principle V)**: Every phase must report progress. Output validation must catch malformed results. Agents must not silently swallow errors. Failure handling preserves prior phase results.

- **Single Source of Truth (Principle XI)**: Every piece of information must have exactly one authoritative source. All other representations must be derived from that source, not maintained independently. When two sources disagree, it is always a bug.

- **Reproducibility Over Inconsistency (Principle VII)**: Given the same inputs, conversus must produce structurally identical output. Deterministic orchestration is non-negotiable. Template variable substitution is mechanical.

- **Safety-Critical Defense-in-Depth (Principle XXIV)**: Safety-critical paths must implement three-layer defense: schema-level required fields, parser-level validation, and contract test reproducing the failure scenario.

- **Evidence Foundation Requirement (implicit from SIR audit status)**: The Sync Impact Report acknowledges the amendment is "evidence-pending" and cites specific PRs and investigation artifacts as empirical foundation.

### Binding Decisions

#### Dispute: Evidence validation timing

**Positions:**
- **pr-evidence-grounding**: Defer ratification until supporting investigation artifacts, PR #42 analysis, and mechanical verification capabilities can be independently validated.
- **wording-precision**: Evidence validation should be "post-ratification follow-up work" while acknowledging evidence concerns as valid.

**Synthesizer's assessment:** pr-evidence-grounding's position is stronger because constitutional principles should have verifiable foundations. If PR #42 doesn't exist or investigation outputs are fabricated, the entire empirical foundation collapses.

**Ruling:** Defer ratification pending evidence validation. The amendment cannot proceed until PR #42 claims and supporting investigation artifacts are verified.

**Grounding citation:** Constitutional Inclusion Criteria require that amendments satisfy falsifiable scope (Criterion 2). If the empirical foundation is unverified or false, the principle's rationale becomes non-falsifiable speculation rather than documented evidence. Additionally, Single Source of Truth (Principle XI) requires that PR #42 claims have exactly one authoritative source—the actual PR content, not the SIR's description of it.

**Rationale:** Constitutional integrity requires verifiable foundations. The candidate amendment cites "PR #42 is the canonical exemplar" and references "95 failing tests" investigation outputs as its empirical basis. If these artifacts don't exist or don't support the claimed patterns, ratifying the principle would embed false information in the constitution with constitutional authority. This creates more dangerous precedent than deferring ratification until evidence validation completes.

**Rejected position:** wording-precision's position that evidence validation can be post-ratification follow-up work assumes the principle has merit independent of its empirical foundation. However, constitutional principles derive their authority from their factual accuracy combined with their normative value. Separating these undermines constitutional credibility.

**Required changes:** Flag CONSTITUTION-v2.5.0-candidate.md as "evidence-pending" in its header. Add requirement to validate PR #42 existence and content, verify investigation artifacts referenced in the SIR, and confirm spec references (045, 067, 069) contain claimed content before proceeding with ratification.

#### Dispute: Constitutional Inclusion Criteria interpretation ambiguity

**Positions:**
- **pr-evidence-grounding and devils-advocate**: Criterion 1 requires actual implementation vs. cross-principle-coherence argues promised verification mechanisms satisfy the standard if concrete enough for engineers to "sketch in one paragraph."
- **cross-principle-coherence**: Promised verification mechanisms satisfy the standard if concrete enough for engineers to "sketch in one paragraph."

**Synthesizer's assessment:** The ambiguity itself is the problem - multiple agents interpreting the same gate text differently undermines consistent constitutional governance.

**Ruling:** The Constitutional Inclusion Criteria require clarification before applying them to XXVIII. The current wording creates legitimate interpretive ambiguity that affects constitutional governance beyond this amendment.

**Grounding citation:** Constitutional Inclusion Criteria text states the check "does NOT have to exist at amendment time, but the path to building it MUST be concrete enough that an engineer reading the principle can sketch the check in one paragraph." This language allows for promised mechanisms but sets a concreteness standard. The ambiguity lies in whether this standard is met by the current SIR claims about "AST-diff heuristics."

**Rationale:** Multiple intelligent agents interpreting the same constitutional gate text differently reveals that the gate itself needs clarification to ensure consistent application. This is a meta-constitutional governance issue that affects all future amendments, not just XXVIII. Resolving the interpretive ambiguity is prerequisite to fair application of the gate.

**Rejected position:** Neither implementation-required nor specification-sufficient interpretations are definitively wrong based on the current text. The problem is the ambiguity that allows both interpretations to seem reasonable.

**Required changes:** Amend the Constitutional Inclusion Criteria in the Governance section to clarify whether Criterion 1 requires actual implementation of verification mechanisms or accepts concrete specification sufficient for implementation sketching. This clarification must be completed before the XXVIII amendment can be fairly evaluated against the gate.

#### Dispute: Categorization friction vs. rigorous standards

**Positions:**
- **devils-advocate**: The four-category classification creates bureaucratic overhead that degrades into checklist theater with contributors claiming "fixture drift" regardless of criteria complexity.
- **wording-precision**: Proposes more rigorous categorization standards to prevent gaming and improve enforcement precision.

**Synthesizer's assessment:** Both positions acknowledge the current categorization system is inadequate. wording-precision's precision approach aligns with constitutional enforcement patterns.

**Ruling:** Implement wording-precision's rigorous categorization standards while incorporating devils-advocate's reviewer guidelines for detecting inappropriate "fixture drift" classifications.

**Grounding citation:** Principle XXVIII clause 3 requires "every PR fixing failing tests MUST classify each fix" using four categories. Constitutional Inclusion Criteria Criterion 2 (falsifiable scope) requires the principle's wording to be "specific enough to flag a hypothetical future PR as violating, without requiring 'interpretation.'" Vague categorization criteria violate this falsifiability requirement.

**Rationale:** Constitutional enforcement requires operationally testable standards, not interpretive guidance that depends on reviewer judgment. devils-advocate's gaming concerns are valid but procedurally addressable through reviewer training and oversight. wording-precision's detailed criteria approach provides the falsifiable boundaries required by the Constitutional Inclusion Criteria gate.

**Rejected position:** devils-advocate's concern about bureaucratic overhead is valid but doesn't override the constitutional requirement for falsifiable enforcement standards. The solution is better reviewer guidelines, not vaguer criteria.

**Required changes:** Replace "without justification" in XXVIII clause 1 with specific three-part criteria: test condition that prevented original assertion, evidence that modified assertion still verifies intended behavior, confirmation that change doesn't mask production defect. Add reviewer guidelines for detecting inappropriate "fixture drift" categorizations to the operational scaffolding planned for follow-up PRs.

#### Dispute: Operational scaffolding completeness timing

**Positions:**
- **devils-advocate**: Demands implementing mechanical enforcement mechanisms before constitutional ratification vs. cross-principle-coherence treats scaffolding as implementation details that can follow ratification.
- **cross-principle-coherence**: Scaffolding as implementation details that can follow ratification.

**Synthesizer's assessment:** Constitutional Inclusion Criteria allow promised enforcement if adequately specified. The principle text should include concrete verification specification, but full implementation can follow ratification.

**Ruling:** Require the principle text to include concrete AST-diff specification sufficient for implementation sketching, but allow operational scaffolding (PR template, CI lint) to be implemented in follow-up PRs as originally planned.

**Grounding citation:** Constitutional Inclusion Criteria Criterion 1 explicitly states the check "does NOT have to exist at amendment time, but the path to building it MUST be concrete enough that an engineer reading the principle can sketch the check in one paragraph." This allows promised mechanisms if adequately specified.

**Rationale:** The Constitutional Inclusion Criteria gate explicitly contemplates promised enforcement mechanisms. The current SIR's claims about "AST-diff heuristics for assertion loosening" are too vague to satisfy even the specification-based interpretation, but the principle can include concrete specification without requiring full implementation before ratification.

**Rejected position:** devils-advocate's demand for actual implementation before ratification contradicts the explicit Constitutional Inclusion Criteria text allowing promised mechanisms with adequate specification.

**Required changes:** Add concrete AST-diff specification to Principle XXVIII text sufficient for an engineer to sketch the implementation in one paragraph. Examples: specific AST node types to monitor (assignment expressions, comparison operators), patterns constituting "loosening" (== → in transformation, exact value → type-only checks), and detection heuristics. Operational scaffolding implementation can proceed in follow-up PRs per the original plan.

### Summary of Changes Required

1. **Evidence validation gate** (from Evidence validation timing): Flag amendment as "evidence-pending" and validate PR #42 claims, investigation artifacts, and spec references before ratification. Priority: P1.

2. **Constitutional Inclusion Criteria clarification** (from Constitutional Inclusion Criteria interpretation): Amend the Governance section to clarify whether Criterion 1 requires implementation or accepts specification for verification mechanisms. Priority: P1.

3. **Specific justification criteria** (from Categorization friction): Replace "without justification" with three-part criteria for assertion changes and add reviewer guidelines for categorization gaming detection. Priority: P1.

4. **Concrete verification specification** (from Operational scaffolding timing): Add AST-diff specification to principle text sufficient for implementation sketching while allowing scaffolding implementation in follow-up PRs. Priority: P2.

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| Evidence validation timing | Defer ratification pending validation | High | Clear grounding in Single Source of Truth and Constitutional Inclusion Criteria falsifiable scope requirements |
| Constitutional Inclusion Criteria interpretation | Clarify gate text before applying to XXVIII | High | Multiple agents interpreting same text differently demonstrates ambiguity requiring resolution |
| Categorization friction | Implement rigorous standards with reviewer guidelines | Medium | Balance between falsifiable enforcement and implementation friction; clear constitutional preference for specificity |
| Operational scaffolding timing | Require specification, allow implementation follow-up | High | Explicit Constitutional Inclusion Criteria text allows promised mechanisms with adequate specification |

The deliberation quality was excellent, with agents demonstrating intellectual honesty through meaningful position revisions and convergence on multiple complex issues. The remaining disputes represent genuine constitutional governance tensions rather than agent-level disagreements, particularly the evidence validation vs. amendment velocity trade-off and the specification vs. implementation standards for constitutional inclusion. These systemic tensions warrant the procedural clarity my rulings establish.

### SPEC-071 SELF-CONSISTENCY VERDICT: PASS WITH FIXES

The Constitutional amendment can proceed to implementation after the required changes are applied, with priority given to evidence validation and Constitutional Inclusion Criteria clarification as prerequisite actions.