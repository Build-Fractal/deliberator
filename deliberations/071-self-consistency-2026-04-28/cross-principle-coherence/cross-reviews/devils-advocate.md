### Dangerous Contradictions

- **Ratification timing and scope**
  - **devils-advocate claims**: "Defer ratification until a second independent case study validates the pattern and the operational scaffolding is implemented" (Executive Summary). The principle "suffers from critical flaws that make it unsuitable for constitutional ratification at this time" (Executive Summary).
  - **cross-principle-coherence claims**: Focuses on "Integration improvements" through explicit cross-references and coordination clauses, implying ratification should proceed with modifications rather than deferral.
  - **Why this is dangerous**: If devils-advocate's deferral recommendation is adopted, the integration work cross-principle-coherence proposes becomes moot. If cross-principle-coherence's integration approach is adopted without addressing devils-advocate's foundational concerns, the principle gets ratified with unresolved scope boundaries.
  - **Suggested resolution**: Devils-advocate should acknowledge whether integration improvements could address their distinctness concerns, or cross-principle-coherence should engage with the evidence threshold question for constitutional inclusion.

- **Constitutional Inclusion Criteria Criterion 3 interpretation**
  - **devils-advocate claims**: "No clear argument establishes why this isn't already covered by Principle IX's behavior-over-shape extension" (Missed Opportunities). "Either demonstrate why XXVIII covers concerns not addressable by composing Principle IX with operational guidance, or merge XXVIII content into Principle IX as an extension" (Actionable Recommendations #3).
  - **cross-principle-coherence claims**: "XXVIII correctly targets the test-fixing lifecycle stage, which is distinct from test authoring (IX)" (Alignment). "Both address the same anti-pattern but from different lifecycle stages (authoring vs fixing)" (Missed Opportunities).
  - **Why this is dangerous**: These represent fundamentally different interpretations of what constitutes "distinct from existing principles." Devils-advocate treats lifecycle stage distinction as insufficient for Criterion 3; cross-principle-coherence treats it as sufficient but poorly coordinated.
  - **Suggested resolution**: The synthesis must resolve whether lifecycle-stage scoping satisfies Criterion 3's distinctness requirement, or whether devils-advocate's compositional approach (IX + operational guidance) is the constitutionally correct path.

- **Enforcement mechanism prioritization**
  - **devils-advocate claims**: "Implement the mechanical enforcement mechanisms before constitutional ratification, or acknowledge that the principle alone is insufficient" (Actionable Recommendations #2). "The SIR's defense-in-depth claim is invalid if the defense layers don't exist."
  - **cross-principle-coherence claims**: Focuses on making "the claimed mechanical verification capability visible and actionable for implementors" (Actionable Recommendations #4) and "Specify mechanical verification artifact" rather than blocking ratification on implementation.
  - **Why this is dangerous**: Devils-advocate would block constitutional ratification pending operational implementation; cross-principle-coherence would ratify with promises of future implementation. This creates a constitutional precedence question about whether enforcement mechanisms must exist before principles are ratified.
  - **Suggested resolution**: Cross-principle-coherence should address whether constitutional ratification without implemented enforcement violates the spirit of the Constitutional Inclusion Criteria gate, or devils-advocate should clarify whether adequate specification of the mechanism (not just implementation) satisfies Criterion 1.

### Tensions

- **Evidence threshold for constitutional inclusion**
  - **devils-advocate's position**: "Constitutional principles should demonstrate generalizability across multiple cases to avoid overfitting to specific circumstances" (Actionable Recommendations #1).
  - **cross-principle-coherence's position**: Accepts the PR #42 case study as sufficient foundation but focuses on cross-principle integration issues rather than evidence sufficiency.
  - **Nature of tension**: Devils-advocate applies a higher evidence bar for constitutional inclusion; cross-principle-coherence assumes the existing evidence meets the threshold and focuses on technical integration.
  - **Coordination needed**: Agreement on what evidence threshold Constitutional Inclusion Criteria Criterion 2 actually requires for falsifiable scope, and whether single-incident principles can satisfy it.

- **Bureaucratic overhead vs. principled discipline**
  - **devils-advocate's position**: "Administrative overhead tends to degrade into checklist theater unless actively beneficial" (Actionable Recommendations #5). "Contributors will game the system by claiming all fixes are 'fixture drift' to minimize effort."
  - **cross-principle-coherence's position**: Treats the categorization framework as "exhaustive coverage of the fix space, creating clear decision boundaries" (Alignment) without addressing compliance erosion risks.
  - **Nature of tension**: Devils-advocate emphasizes degradation risks of bureaucratic requirements; cross-principle-coherence emphasizes their structural completeness.
  - **Coordination needed**: Assessment of whether the categorization requirement provides enough value to justify its administrative overhead, and what mitigation prevents gaming.

- **Scope of mechanical verification claims**
  - **devils-advocate's position**: "Define the concrete AST-diff heuristics that constitute mechanical verification of the principle" (Actionable Recommendations #6). The current claims are "underspecified rather than concrete."
  - **cross-principle-coherence's position**: "Makes the claimed mechanical verification capability visible and actionable for implementors" (Actionable Recommendations #4) but doesn't challenge the feasibility claims.
  - **Nature of tension**: Devils-advocate questions whether mechanical verification is actually feasible as claimed; cross-principle-coherence assumes feasibility but wants better specification.
  - **Coordination needed**: Technical assessment of whether "AST-diff heuristics for assertion loosening" can actually detect the prohibited patterns at the granularity Constitutional Inclusion Criteria Criterion 1 requires.

- **Integration vs. replacement approach to Principle IX overlap**
  - **devils-advocate's position**: "Either demonstrate why XXVIII covers concerns not addressable by composing Principle IX with operational guidance, or merge XXVIII content into Principle IX as an extension" (Actionable Recommendations #3).
  - **cross-principle-coherence's position**: "Add clarification: 'This requirement reinforces Principle IX's behavior-over-shape testing at fix-time'" (Actionable Recommendations #1), suggesting coordination rather than replacement.
  - **Nature of tension**: Devils-advocate leans toward merging into IX or operational guidance; cross-principle-coherence leans toward cross-referencing for coordination.
  - **Coordination needed**: Determination of whether the overlap is extensive enough to warrant merging, or whether explicit coordination preserves the lifecycle-stage distinction both reviews acknowledge exists.

### Safe Agreements

- **Principle IX overlap recognition**
  - **Shared position**: Both reviews identify significant overlap between XXVIII's assertion fidelity clause and IX's behavior-over-shape operational test definition. Devils-advocate notes "Lines 758-784 overlap significantly with Principle IX's behavior-over-shape testing framework" (Actionable Recommendations #3). Cross-principle-coherence notes "Both address the same anti-pattern but from different lifecycle stages (authoring vs fixing)" (Missed Opportunities).
  - **Combined evidence**: The assertion-loosening prohibition ("replacing exact value matches with type-only checks") appears in both principles with similar intent but different scopes.
  - **Confidence level**: High. This overlap is textually verifiable and both reviews provide specific line citations.

- **Mechanical verification capability gaps**
  - **Shared position**: Both reviews identify problems with the SIR's Criterion 1 claims. Devils-advocate notes "provides no specification" for the AST-diff heuristics (Actionable Recommendations #6). Cross-principle-coherence notes "XXVIII itself contains no reference to this verification mechanism, making the mechanical checking capability invisible to implementors" (Missed Opportunities).
  - **Combined evidence**: The constitutional text lacks the verification mechanism specification that the SIR claims satisfies Criterion 1.
  - **Confidence level**: High. Both reviews identify the same gap between SIR claims and principle text.

- **Cross-principle coordination deficits**
  - **Shared position**: Both reviews recognize that XXVIII fails to coordinate with related constitutional principles. Devils-advocate notes "Distinctness demonstration" problems (Missed Opportunities). Cross-principle-coherence systematically identifies missing coordination with XXIV, XXVI, and V (Missed Opportunities).
  - **Combined evidence**: XXVIII operates in isolation rather than composing cleanly with existing constitutional testing discipline.
  - **Confidence level**: Medium. While both recognize coordination problems, they propose different solutions (devils-advocate leans toward merging/deferral, cross-principle-coherence toward explicit cross-referencing).