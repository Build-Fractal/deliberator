### Dangerous Contradictions

- **String-match algorithm specification conflict**
  - **wording-precision claims**: "Specify exact matching algorithm (e.g., 'exact substring match of principle header + first paragraph')" (Recommendation 5, L67)
  - **mechanical-verifiability claims**: "Define the heuristic as 'exact substring match of principle body text after normalizing whitespace'" (Recommendation 1, L39)
  - **Why this is dangerous**: These specify different matching scopes—header+first-paragraph vs full-body-text. If implemented separately, they would catch different violations and create inconsistent linter behavior across the same structural amendment.
  - **Suggested resolution**: mechanical-verifiability should yield on scope (header+first-paragraph is sufficient for duplication detection), wording-precision should yield on normalization (whitespace normalization prevents spurious failures).

- **Verification method authority hierarchy**
  - **wording-precision claims**: Manual negative checks in Section 7 should be "authoritative verification" while automation supplements them (implicit in Missed Opportunities framing, L179-186 as "mechanically falsifiable tests")
  - **mechanical-verifiability claims**: "Specify that the linter implements a subset of Section 7's checks automatically, with the manual checks serving as the authoritative verification for complex edge cases" (Recommendation 3, L51)
  - **Why this is dangerous**: If manual checks are authoritative for simple cases (wording-precision's view), automation becomes secondary. If automation is authoritative for simple cases (mechanical-verifiability's view), manual review becomes fallback. This creates unclear precedence when they disagree.
  - **Suggested resolution**: wording-precision should yield—automation should be authoritative for mechanically detectable violations, with manual checks reserved only for cases requiring human judgment that the linter cannot encode.

- **SIR audit trail vs algorithmic precision priority ordering**
  - **wording-precision claims**: "Specify SIR audit trail preservation" is Priority P1 (Recommendation 3, L53)
  - **mechanical-verifiability claims**: "Specify duplication detection algorithm" is Priority P1 (Recommendation 1, L37)
  - **Why this is dangerous**: If SIR preservation takes P1 precedence, algorithmic specification becomes P2, potentially delaying linter implementation. If algorithmic specification takes P1 precedence, SIR preservation becomes secondary, risking audit trail loss.
  - **Suggested resolution**: Both should be P1 since they address independent failure modes—audit trail preservation doesn't depend on linter algorithm specificity and vice versa. Declare them co-P1 rather than competing for priority ordering.

### Tensions

- **Documentation completeness vs algorithmic precision emphasis**
  - **wording-precision's position**: Focus on complete enumeration of cross-reference patterns, normative text boundaries, and SIR preservation requirements (Recommendations 2, 7, 3)
  - **mechanical-verifiability's position**: Focus on algorithmic specification for automated verification and linter implementation details (Recommendations 1, 4, 7)
  - **Nature of tension**: Both approaches improve verification rigor but pull implementation effort in different directions—comprehensive documentation vs automated tooling.
  - **Coordination needed**: Sequence documentation completeness first (enables consistent manual verification during development), then algorithmic specification (enables automated verification post-implementation).

- **Verbatim preservation standard granularity**
  - **wording-precision's position**: "byte-for-byte identical content" with complete enumeration of what constitutes normative text (Recommendation 1, L43)
  - **mechanical-verifiability's position**: "byte-equal content" verification via SHA-256 hashing "modulo documented cross-reference changes" (Recommendation 2, L45)
  - **Nature of tension**: Both want strict preservation but different implementation approaches—explicit enumeration vs cryptographic verification with exceptions.
  - **Coordination needed**: Combine approaches: use wording-precision's enumeration to define what gets hashed, use mechanical-verifiability's hashing to verify preservation of enumerated content.

- **Cross-reference completeness vs link validation focus**
  - **wording-precision's position**: "Complete cross-reference matrix documentation" covering all tier combinations and syntax patterns (Recommendation 2, L47)
  - **mechanical-verifiability's position**: "Cross-reference resolution validation" to verify rewritten references actually resolve (Recommendation 5, L61)
  - **Nature of tension**: Documentation ensures consistent syntax; validation ensures functional links. Both needed but different implementation moments.
  - **Coordination needed**: Apply wording-precision's matrix during spec writing (prevents syntax inconsistency), apply mechanical-verifiability's validation during implementation (catches broken links).

- **Manual verification reliability assessment**
  - **wording-precision's position**: Manual checks can be "mechanically falsifiable" and provide "concrete verification checks" (Alignment, L15)
  - **mechanical-verifiability's position**: "Manual review reliability assumption" is off-base because "automated checks are typically more reliable for mechanical verification tasks" (Off-Base Assumptions, L33)
  - **Nature of tension**: Different confidence levels in human vs automated verification for the same task class.
  - **Coordination needed**: Distinguish task classes—use automation for pattern matching and enumeration verification, use manual review for context-dependent judgment calls that resist algorithmic specification.

### Safe Agreements

- **Tier-coherence linter underspecification is critical**
  - **Shared position**: Both reviews identify the "string-match heuristic plus name-collision check" description as inadequately specified (wording-precision Missed Opportunities L31, mechanical-verifiability Executive Summary L3). Both flag this as requiring algorithmic precision before implementation.
  - **Combined evidence**: wording-precision provides falsifiability analysis (non-reproducible verification), mechanical-verifiability provides implementation analysis (unimplementable without deterministic algorithms). Together they demonstrate both verification credibility and practical feasibility problems.
  - **Confidence level**: High. This represents the most critical gap both perspectives identified in the mechanical verification surface.

- **Verbatim preservation contract terminology inconsistency**
  - **Shared position**: Both reviews identify the spec's inconsistent use of "every word...is preserved" vs "byte-equal content" as a precision problem requiring unification (wording-precision Recommendation 1 L41, mechanical-verifiability gap in Section 5 L23).
  - **Combined evidence**: wording-precision demonstrates the ambiguity allows formatting violations while claiming compliance; mechanical-verifiability demonstrates that "byte-equal content" claims require byte-level verification tools. Both perspectives converge on needing the stricter standard consistently applied.
  - **Confidence level**: High. The terminology inconsistency creates a falsifiable gap that both verification approaches independently flagged.

- **Cross-reference handling incompleteness across multiple dimensions**
  - **Shared position**: Both reviews identify cross-reference documentation as incomplete but from different angles—wording-precision flags missing syntax patterns and tier combinations (Missed Opportunities L23), mechanical-verifiability flags lack of resolution validation (Missed Opportunities L19).
  - **Combined evidence**: wording-precision's documentation analysis shows the spec covers only 2 of 6 possible reference patterns; mechanical-verifiability's validation analysis shows no verification that rewritten references actually resolve. Together they demonstrate both specification and verification gaps.
  - **Confidence level**: Medium. While both identify cross-reference problems, the solutions address different failure modes rather than reinforcing the same concern.

- **Conditions discharge empirical accuracy requirement**
  - **Shared position**: Both reviews flag that the spec's claims about condition status changes contain factual inaccuracies that undermine verification credibility (wording-precision Missed Opportunities L29, mechanical-verifiability alignment with empirical evidence requirement L17).
  - **Combined evidence**: wording-precision provides specific factual correction (V was already Provisional, not flipped from Satisfied); mechanical-verifiability frames this as essential for third-party verification of discharge accuracy. Both perspectives require empirical claims to match observable file state.
  - **Confidence level**: Medium. Both identify the accuracy requirement but from different verification credibility concerns rather than the same underlying analysis.