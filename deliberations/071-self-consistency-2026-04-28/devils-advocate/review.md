### Executive Summary

Principle XXVIII (Test-Fix Boundary Preservation) attempts to codify discipline around test-fixing methodology to prevent production bugs from being masked by careless test repairs. While this addresses a real problem demonstrated in the PR #42 case study, the principle suffers from critical flaws that make it unsuitable for constitutional ratification at this time. The principle overfits to a single incident, relies on operational scaffolding that doesn't yet exist, and imposes bureaucratic overhead that will likely degrade into checklist theater. Most critically, it fails the v2.4.0 Constitutional Inclusion Criteria by not being meaningfully distinct from existing Principle IX. **Recommendation: Defer ratification until a second independent case study validates the pattern and the operational scaffolding is implemented.**

### Alignment

- **Single incident recognition** (L776-784): The principle correctly identifies that the PR #42 investigation revealed a systematic methodology problem where production bugs were nearly buried under mechanical test failures. This demonstrates awareness of a real failure mode.

- **Behavioral testing emphasis** (L758-760): The focus on "preserve or strengthen the test's verification of real behavior" aligns with preventing regression to shape-only testing patterns that miss functional problems.

- **Skip citation discipline** (L762-766): Requiring citations and remediation timelines for test skips addresses the common antipattern of accumulating unexplained disabled tests that become technical debt.

### Missed Opportunities

- **Multi-incident validation**: The principle relies entirely on PR #42 as its founding case study. A constitutional principle should demonstrate the pattern across multiple independent incidents to prove generalizability rather than overfitting to circumstantial details of a single investigation.

- **Enforcement mechanism integration**: The principle acknowledges four-layer defense (principle + PR template + CI lint + spec 067 §4.6) but only implements one layer in this amendment. The other three layers constitute the actual enforcement mechanism.

- **Friction impact assessment**: No analysis is provided of how the mandatory categorization requirement will affect contributor velocity or the likelihood of compliance erosion through least-effort categorization.

- **Consistency with existing constitutional vocabulary**: The principle uses RFC 2119 keywords inconsistently ("MAY tighten; MAY NOT loosen" vs "MUST classify") without explanation for the asymmetry.

- **Distinctness demonstration**: No clear argument establishes why this isn't already covered by Principle IX's behavior-over-shape extension, which explicitly covers test authoring discipline.

### Off-Base Assumptions

- **Constitutional vs. operational scope boundary**: The principle assumes that test-fixing discipline belongs at the constitutional level, but the v2.4.0 Constitutional Inclusion Criteria establish that principles must be mechanically verifiable and distinct from existing principles. XXVIII appears to fail both tests.

- **Enforcement completeness**: The SIR claims "three layers all have to fail simultaneously" for regression to occur, but three of those four layers don't exist yet. The principle assumes constitutional ratification can proceed based on promised future implementation of its enforcement mechanism.

- **Compliance sustainability**: The principle assumes that requiring explicit categorization of every test fix will improve discipline, but provides no evidence that this bureaucratic requirement won't degrade into perfunctory compliance that defeats its purpose.

### Actionable Recommendations

1. **Defer ratification pending second case study** (Priority: P1)
   - **Current state**: Principle is based solely on PR #42 investigation findings.
   - **Proposed change**: Identify and document a second independent incident where test-fixing discipline prevented or would have prevented production bugs from being masked.
   - **Rationale**: Constitutional principles should demonstrate generalizability across multiple cases to avoid overfitting to specific circumstances.
   - **Risk if ignored**: The principle may be solving a problem that was unique to PR #42's circumstances rather than a systematic methodology gap.

2. **Implement operational scaffolding before ratification** (Priority: P1)
   - **Current state**: Three of four enforcement layers (PR template, CI lint, spec 067 §4.6) are deferred to follow-up PRs.
   - **Proposed change**: Implement the mechanical enforcement mechanisms before constitutional ratification, or acknowledge that the principle alone is insufficient.
   - **Rationale**: The SIR's defense-in-depth claim is invalid if the defense layers don't exist.
   - **Risk if ignored**: The principle becomes a moral exhortation without enforcement, likely to be ignored under pressure.

3. **Establish distinctness from Principle IX** (Priority: P1)
   - **Current state**: Lines 758-784 overlap significantly with Principle IX's behavior-over-shape testing framework (L334-352).
   - **Proposed change**: Either demonstrate why XXVIII covers concerns not addressable by composing Principle IX with operational guidance, or merge XXVIII content into Principle IX as an extension.
   - **Rationale**: Constitutional Inclusion Criterion 3 requires distinctness from existing principles.
   - **Risk if ignored**: The amendment fails the v2.4.0 constitutional gate and should be rejected.

4. **Resolve RFC 2119 keyword inconsistency** (Priority: P2)
   - **Current state**: "MAY tighten; MAY NOT loosen" (L760-762) vs "MUST classify" (L767-776) without justification for asymmetry.
   - **Proposed change**: Either make both requirements mandatory ("MUST NOT loosen") or both permissive ("SHOULD classify"), with rationale.
   - **Rationale**: Constitutional principles should use RFC 2119 keywords consistently to avoid ambiguity in enforcement.
   - **Risk if ignored**: Contributors may interpret the asymmetry as inconsistent priority signaling.

5. **Address categorization friction** (Priority: P2)
   - **Current state**: Every PR fixing failing tests must classify each fix into one of four categories (L767-776).
   - **Proposed change**: Provide evidence that this bureaucratic requirement improves outcomes, or replace with lighter-weight heuristics.
   - **Rationale**: Administrative overhead tends to degrade into checklist theater unless actively beneficial.
   - **Risk if ignored**: Contributors will game the system by claiming all fixes are "fixture drift" to minimize effort.

6. **Clarify mechanical verification capability** (Priority: P2)
   - **Current state**: The SIR references `scripts/lint-test-fixes.py` as a future implementation but provides no specification.
   - **Proposed change**: Define the concrete AST-diff heuristics that constitute mechanical verification of the principle.
   - **Rationale**: Constitutional Inclusion Criterion 1 requires that mechanical verification be feasible and concrete enough to sketch in one paragraph.
   - **Risk if ignored**: The principle may be unenforceable through automation, reducing it to manual review burden.

7. **Provide compliance degradation mitigation** (Priority: P3)
   - **Current state**: No mechanism prevents contributors from providing perfunctory categorizations to satisfy the requirement.
   - **Proposed change**: Define what constitutes adequate justification for each category and how reviewers should validate classifications.
   - **Rationale**: Bureaucratic requirements without quality controls become compliance theater.
   - **Risk if ignored**: The categorization requirement becomes meaningless overhead without improving actual test-fixing discipline.

### Referenced Documentation

- No documentation files were provided for the devils-advocate tool perspective.