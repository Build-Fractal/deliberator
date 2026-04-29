### Executive Summary

Principle XXVIII (Test-Fix Boundary Preservation) aims to codify discipline for fixing failing tests without weakening their verification of real behavior. As a cross-principle coherence audit, I find significant overlaps and gaps with existing constitutional principles that create ambiguity about authority and scope. The principle introduces test-fix methodology that intersects with Principle IX's behavior-over-shape testing requirements, Principle XXIV's safety-critical contract testing, and Principle XXVI's meta-testing coverage. While the intent is sound, the current wording fails to clearly delineate its lifecycle-specific scope from existing authoring and coverage principles, creating potential conflicts rather than clean composition. Most critically, the principle needs explicit cross-references to clarify how it composes with existing testing discipline rather than replacing or contradicting it.

### Alignment

- **Lifecycle-specific focus** (L1858-1890): XXVIII correctly targets the test-fixing lifecycle stage, which is distinct from test authoring (IX) and coverage maintenance (XXVI). This addresses a genuine gap in constitutional coverage of the fix-time decision process.

- **Concrete violation examples** (L1869-1870): The principle provides specific examples of prohibited loosening ("`==` with `in`", "exact value matches with type-only checks") that align with IX's operational test definition of prohibited shape-only assertions.

- **Categorization framework** (L1880-1887): The four-category taxonomy (fixture/path drift, production bug, legitimate test bug, defunct test) provides exhaustive coverage of the fix space, creating clear decision boundaries for contributors.

- **Verifiable requirements** (L1888-1889): The requirement that classification "appears in the PR description and is verifiable against the diff" aligns with constitutional preference for mechanically-checkable discipline.

### Missed Opportunities

- **IX lifecycle coordination**: The spec fails to explicitly coordinate XXVIII's "replacing exact value matches with type-only checks" prohibition with IX's existing behavior-over-shape operational test definition. Both address the same anti-pattern but from different lifecycle stages (authoring vs fixing), creating potential for contributors to view them as conflicting rather than complementary. Impact: high.

- **XXIV safety-critical composition**: XXVIII's "production bug" category is silent about XXIV's contract test requirement for safety-critical paths. When fixing a production bug in a safety-critical path, it's unclear whether the fix MUST add a contract test per XXIV or whether keeping the test "as-is" per XXVIII is sufficient. Impact: high.

- **XXVI coverage preservation**: The "defunct test" category lacks coordination with XXVI's meta-testing requirements. Deleting a defunct test from a parametrized capability set could violate XXVI's coverage assertions without explicit guidance to update meta-test counts. Impact: medium.

- **V observability coordination**: XXVIII's skip citation requirement overlaps with V's "errors should never pass silently" principle but doesn't reference it, missing an opportunity to ground the citation discipline in existing observability requirements. Impact: low.

- **Constitutional gate self-verification**: The SIR's Criterion 1 assessment claims mechanical verification via "AST-diff heuristics" but XXVIII itself contains no reference to this verification mechanism, making the mechanical checking capability invisible to implementors. Impact: medium.

- **Cross-lifecycle enforcement**: The spec misses the opportunity to clarify how XXVIII's fix-time discipline reinforces IX's authoring-time behavior-over-shape requirement, creating a defensive discipline that prevents degradation of IX compliance over time. Impact: medium.

### Off-Base Assumptions

- **Principle distinctness assumption**: The SIR claims XXVIII is "distinct from existing principles" but the assertion fidelity clause (L1869-1870) directly overlaps with IX's operational test definition, contradicting the distinctness claim for Constitutional Inclusion Criteria Criterion 3.

- **Mechanical verification feasibility**: The SIR claims "AST-diff heuristics for assertion loosening" provide mechanical verification capability, but XXVIII contains no specification of what constitutes detectable "loosening" at the AST level, making the verification mechanism underspecified rather than concrete.

### Actionable Recommendations

1. **Add IX lifecycle coordination clause** (Priority: P1)
   - **Current state**: XXVIII clause 1 prohibits "replacing exact value matches with type-only checks" with no reference to IX's behavior-over-shape extension.
   - **Proposed change**: Add clarification: "This requirement reinforces Principle IX's behavior-over-shape testing at fix-time: a test that fails IX's operational test definition after fix violates this principle regardless of whether it passes."
   - **Rationale**: Prevents interpretation of XXVIII as superseding or conflicting with IX's existing requirements.
   - **Risk if ignored**: Contributors may view the two principles as conflicting authorities, leading to inconsistent enforcement.

2. **Specify XXIV safety-critical composition** (Priority: P1)
   - **Current state**: XXVIII "production bug" category says "fix the code (test stays as-is)" with no reference to XXIV contract test requirements.
   - **Proposed change**: Add to production bug category: "For safety-critical paths (per Principle XXIV), the fix MUST also add a contract test reproducing the failure scenario unless one already exists."
   - **Rationale**: Clarifies that XXIV's contract test requirement is additional to, not replaced by, XXVIII's test preservation requirement.
   - **Risk if ignored**: Safety-critical production bugs may be fixed without adding the defensive contract tests XXIV requires.

3. **Cross-reference XXVI for defunct test deletions** (Priority: P2)
   - **Current state**: "Defunct test" category has no reference to XXVI meta-testing requirements.
   - **Proposed change**: Add to defunct test category: "When deleting a test from a parametrized capability set, update the corresponding meta-test per Principle XXVI to maintain coverage assertions."
   - **Rationale**: Prevents defunct test deletions from silently breaking XXVI's coverage discipline.
   - **Risk if ignored**: Meta-tests will fail after legitimate defunct test deletions, creating false CI failures.

4. **Specify mechanical verification artifact** (Priority: P2)
   - **Current state**: No reference to the "AST-diff heuristics" claimed in the SIR's Criterion 1 assessment.
   - **Proposed change**: Add enforcement note: "Mechanical verification via `scripts/lint-test-fixes.py` (filed as follow-up per spec 071 §6) detects assertion loosening patterns in test file diffs."
   - **Rationale**: Makes the claimed mechanical verification capability visible and actionable for implementors.
   - **Risk if ignored**: The constitutional gate's Criterion 1 requirement remains unverifiable, weakening the principle's enforcement foundation.

5. **Ground skip citation in V observability** (Priority: P3)
   - **Current state**: XXVIII clause 2 requires citation for skips with no reference to Principle V.
   - **Proposed change**: Add parenthetical: "MUST cite the bug being skipped (issue or PR number) and a remediation timeline (per Principle V's observability requirement)."
   - **Rationale**: Connects the citation discipline to existing constitutional observability requirements rather than introducing an orphaned rule.
   - **Risk if ignored**: Skip citation appears as arbitrary bureaucracy rather than principled observability discipline.

6. **Clarify Constitutional Inclusion Criteria compliance** (Priority: P2)
   - **Current state**: SIR claims Criterion 3 (distinctness) PASS but XXVIII clause 1 directly overlaps IX's operational test definition.
   - **Proposed change**: Either revise XXVIII to clearly differentiate from IX's scope or acknowledge in the SIR that this extends IX rather than being fully distinct.
   - **Rationale**: Ensures honest compliance with the constitutional gate rather than overstating distinctness.
   - **Risk if ignored**: Sets precedent for gate circumvention via misleading distinctness claims.

7. **Add falsification clause for mechanical verification** (Priority: P3)
   - **Current state**: No concrete falsification scenario provided for the mechanical verification claim.
   - **Proposed change**: Add to enforcement note: "A future PR that loosens assertions to make tests pass without adding justification violates this principle and should be detected by the AST-diff lint."
   - **Rationale**: Provides concrete falsification scenario per Constitutional Inclusion Criteria Criterion 2.
   - **Risk if ignored**: Verification capability remains theoretical rather than operationally testable.

### Referenced Documentation

- `CONSTITUTION-v2.5.0-candidate.md` — sections/lines cited: L1858-1890 (Principle XXVIII), L665-710 (Principle IX behavior-over-shape extension), L1470-1495 (Principle XXIV), L1545-1570 (Principle XXVI), L308-325 (Principle V), L1765-1830 (Constitutional Inclusion Criteria gate)