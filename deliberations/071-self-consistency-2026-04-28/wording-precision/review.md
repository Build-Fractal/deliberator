### Executive Summary

Principle XXVIII (Test-Fix Boundary Preservation) establishes discipline around maintaining test integrity when fixing failing tests, requiring fixes to preserve or strengthen behavioral verification rather than weaken assertions to achieve passing status. The principle addresses a critical gap in testing methodology by preventing the burial of production bugs behind superficial test fixes. While the principle's core intent is sound and the three-clause structure provides good coverage, several wording imprecisions create ambiguity in enforcement boundaries. The operational definitions contain gaps that could lead to inconsistent application, particularly around what constitutes adequate justification for assertion changes and timeline specifications for skipped tests. The most critical issue is the vague "without justification" qualifier in clause 1, which undermines the precision needed for consistent enforcement.

### Alignment

- **Strong imperative language** (L1-3): The principle correctly uses "MUST preserve or strengthen" to establish a non-negotiable boundary around test integrity, aligning with constitutional requirements for clear enforcement criteria.

- **Concrete violation examples** (L7-9): The specific examples of loosening ("replacing `==` with `in`, replacing exact value matches with type-only checks") provide reviewers with concrete patterns to recognize, supporting consistent application.

- **Exhaustive classification requirement** (L15-22): The "exactly one of" language creates a complete partition of fix types, preventing ambiguous categorizations that could weaken enforcement.

- **Mechanical verification hook** (L23): The requirement that "classification appears in the PR description and is verifiable against the diff" establishes a concrete audit trail for enforcement.

### Missed Opportunities

- **Precision in justification standards**: The principle uses "without justification" but fails to define what constitutes adequate justification, leaving a critical enforcement gap that could lead to reviewer disagreement.

- **Timeline specification format**: Clause 2 requires "a remediation timeline" but provides no format constraints, allowing vague statements like "soon" or "eventually" that defeat the accountability purpose.

- **Boundary case handling**: The principle claims the four categories are exhaustive but provides no guidance for edge cases like framework API changes or test environment shifts that don't clearly map to any category.

- **Quantitative precision for assertions**: The "tighten vs loosen" distinction lacks precision for numerical assertions - is changing `assert x > 5` to `assert x > 4` tightening or loosening the constraint?

- **Citation format specification**: Clause 2 requires citing "issue or PR number" but doesn't specify format, allowing inconsistent references that complicate tracking.

- **Cross-principle coordination**: The principle references "verifiable against the diff" but doesn't coordinate with existing verification principles for consistent audit approaches.

### Off-Base Assumptions

- **Binary tighten/loosen assumption** (L6-7): The principle assumes all assertion changes can be cleanly categorized as tightening or loosening, but complex assertions involving multiple conditions may not fit this binary model.

- **Universal pytest applicability** (L11): The principle specifically names `pytest.skip()` constructs, assuming pytest is the only testing framework in scope, which may not hold across all project components.

### Actionable Recommendations

1. **Define justification standards** (Priority: P1)
   - **Current state**: Line 9 uses "without justification" with no definition of adequate justification.
   - **Proposed change**: Add specific criteria: "Justification MUST include: (a) the specific test condition that prevented the original assertion from passing, (b) evidence that the modified assertion still verifies the intended behavior, (c) confirmation that the change does not mask a production defect."
   - **Rationale**: Enforcement requires concrete standards, not subjective interpretation.
   - **Risk if ignored**: Reviewers will apply inconsistent standards, undermining the principle's protective effect.

2. **Specify timeline format requirements** (Priority: P1)
   - **Current state**: Line 12-13 requires "remediation timeline" without format specification.
   - **Proposed change**: Replace with "a specific remediation timeline (target version, quarter, or dependency milestone)"
   - **Rationale**: Accountability requires concrete timelines, not vague commitments.
   - **Risk if ignored**: Skip citations become meaningless without enforceable timeline commitments.

3. **Clarify RFC 2119 compliance** (Priority: P2)
   - **Current state**: Line 6 uses "MAY NOT loosen" which could be misread as permissive.
   - **Proposed change**: Replace "MAY NOT" with "MUST NOT" for clarity, or add footnote clarifying RFC 2119 equivalence.
   - **Rationale**: Constitutional text should avoid potential misinterpretation of normative language.
   - **Risk if ignored**: Readers may misunderstand the prohibition strength.

4. **Add boundary case guidance** (Priority: P2)
   - **Current state**: Lines 15-22 claim exhaustive categorization without addressing edge cases.
   - **Proposed change**: Add clause: "For boundary cases (framework API changes, test environment shifts), default to 'fixture/path drift' unless the change reveals a production defect."
   - **Rationale**: Exhaustive claims require exhaustive coverage or explicit fallback rules.
   - **Risk if ignored**: Edge cases will be categorized inconsistently, weakening the classification discipline.

5. **Define assertion complexity boundaries** (Priority: P2)
   - **Current state**: Lines 6-9 assume binary tighten/loosen categorization applies universally.
   - **Proposed change**: Add qualifier: "For assertions involving multiple conditions or complex predicates, decompose into constituent assertions and evaluate each component separately."
   - **Rationale**: Complex assertions need decomposition rules to apply the tighten/loosen test consistently.
   - **Risk if ignored**: Complex assertion changes will escape proper categorization.

6. **Standardize citation format** (Priority: P3)
   - **Current state**: Line 12 requires "issue or PR number" without format specification.
   - **Proposed change**: Specify format: "GitHub issue (#NNNN) or pull request (#NNNN) with working link."
   - **Rationale**: Consistent citation format improves trackability and audit compliance.
   - **Risk if ignored**: Citation quality will vary, reducing accountability effectiveness.

7. **Coordinate with verification infrastructure** (Priority: P3)
   - **Current state**: Line 23 mentions "verifiable against the diff" without connecting to existing verification patterns.
   - **Proposed change**: Cross-reference Principle XXIV's contract test requirements for systematic verification approach.
   - **Rationale**: Verification approaches should be consistent across constitutional principles.
   - **Risk if ignored**: Verification inconsistency reduces overall constitutional effectiveness.

### Referenced Documentation

- `CONSTITUTION-v2.5.0-candidate.md` — sections/lines cited: L1-3, L6-9, L11-13, L15-23