### Executive Summary

The constitution under review establishes comprehensive testing principles across multiple dimensions: behavioral verification, safety-critical defense, cost management, coverage maintenance, and fix discipline. From a cross-principle analysis perspective, the testing-related principles (IX, XXIV, XXV, XXVI, XXVIII) demonstrate both strong complementary design and concerning overlaps that violate the constitution's own distinctness gate. The behavior-over-shape testing extension in Principle IX and the assertion fidelity rule in Principle XXVIII explicitly prohibit the same specific action (replacing exact-value assertions with type-only checks), creating redundancy that the constitution's Criterion 3 was designed to prevent. Most critically, the constitution needs to consolidate redundant testing rules into a coherent testing framework rather than scattering related constraints across multiple principles.

### Alignment

- **Behavior-over-shape foundation** (L346-366): Principle IX establishes the fundamental distinction between behavioral and structural testing, correctly identifying that tests verifying field presence without meaning are insufficient. This provides the conceptual foundation for testing discipline throughout the constitution.

- **Safety-critical scope definition** (L573-595): Principle XXIV clearly defines safety-critical paths as synthesis verdict generation and provider protocol implementation, providing concrete boundaries rather than subjective "important code" designations.

- **Cost discipline taxonomy** (L597-632): Principle XXV establishes a clear marker system (`@pytest.mark.live`) and CI opt-out mechanism, preventing runaway test costs in continuous integration.

- **Meta-testing coverage guards** (L654-675): Principle XXVI addresses the systematic problem of coverage drift as capability sets grow, providing automated detection of forgotten test updates.

### Missed Opportunities

- **Testing principle consolidation**: The constitution scatters related testing constraints across five separate principles rather than organizing them into a coherent testing framework. A unified "Testing Discipline" principle could address behavior verification, cost management, and fix discipline systematically.

- **Cross-principle dependency mapping**: The constitution fails to explicitly map how testing principles interact when multiple apply to the same scenario (e.g., fixing a failing safety-critical live test with parametrized capabilities).

- **Testing lifecycle integration**: The constitution treats different testing phases (creation, maintenance, fixing) as separate concerns rather than as a unified workflow that should be governed consistently.

- **Verification artifact coordination**: Each testing principle defines its own verification approach without coordinating with others, creating potential CI complexity and redundant checking mechanisms.

- **Testing antipattern catalog**: The constitution references an antipattern catalog but doesn't integrate testing-specific antipatterns into the testing principles themselves.

- **Progressive testing disclosure**: The constitution applies progressive disclosure to skill content but not to testing requirements, missing an opportunity to reduce cognitive load for different testing scenarios.

### Off-Base Assumptions

- **Distinctness gate compliance**: The constitution assumes Principles IX and XXVIII address distinct concerns, but both explicitly prohibit replacing exact-value assertions with type-only checks (L361-363, L693-695). This violates Criterion 3 of the constitutional inclusion gate established in the same document.

- **Safety-critical boundary clarity**: The constitution assumes the boundary between ordinary and safety-critical bugs is self-evident beyond the two specified domains, but XXVIII's "production bug" category provides no guidance for determining when contract tests are required.

- **Independent testing principles**: The constitution assumes testing principles can be applied independently, but real scenarios often trigger multiple principles simultaneously without clear precedence rules.

### Actionable Recommendations

1. **Consolidate redundant assertion rules** (Priority: P1)
   - **Current state**: Principle IX (L361-363) and Principle XXVIII (L693-695) both prohibit replacing exact-value assertions with type-only checks.
   - **Proposed change**: Remove the assertion fidelity language from XXVIII and reference IX's behavior-over-shape extension instead: "Assertion fidelity: fixes MUST preserve behavioral verification per Principle IX..."
   - **Rationale**: The constitution's own Criterion 3 prohibits principles that restate existing concerns in different words.
   - **Risk if ignored**: The constitution violates its own distinctness gate, undermining constitutional authority and creating confusion about which principle governs assertion quality.

2. **Define safety-critical test-fix protocol** (Priority: P1)
   - **Current state**: XXVIII allows "production bug" fixes without clarifying when XXIV's contract test requirement applies.
   - **Proposed change**: Add to XXVIII: "Production bugs in safety-critical paths (per Principle XXIV scope) MUST include contract test additions in the same PR."
   - **Rationale**: Prevents safety-critical bugs from bypassing the three-layer defense requirement through the test-fix pathway.
   - **Risk if ignored**: Safety-critical bugs can be fixed without contract tests, defeating the defense-in-depth principle.

3. **Clarify meta-test interaction with defunct tests** (Priority: P1)
   - **Current state**: XXVI requires meta-tests for parametrize coverage, XXVIII allows defunct test deletion, but interaction is undefined.
   - **Proposed change**: Add to XXVIII defunct test category: "Deletion from parametrized test sets MUST update the parametrize list and meta-test expectations in the same PR."
   - **Rationale**: Prevents meta-test failures when legitimate test deletions occur.
   - **Risk if ignored**: Legitimate test cleanup triggers spurious meta-test failures, undermining the coverage guard system.

4. **Establish testing principle precedence** (Priority: P2)
   - **Current state**: No guidance when multiple testing principles apply to the same scenario.
   - **Proposed change**: Add a "Testing Principle Coordination" section clarifying that safety-critical requirements (XXIV) override cost discipline (XXV) when in conflict.
   - **Rationale**: Provides clear decision-making framework for complex testing scenarios.
   - **Risk if ignored**: Ambiguous situations lead to inconsistent application of testing principles.

5. **Align citation requirements** (Priority: P2)
   - **Current state**: XXV requires cost justification in docstrings, XXVIII requires bug citations for skips, using different formats and triggers.
   - **Proposed change**: Standardize citation format across both principles: "Issue/PR number and justification timeline."
   - **Rationale**: Consistent documentation requirements reduce cognitive load and improve maintainability.
   - **Risk if ignored**: Inconsistent citation practices create maintenance burden and compliance confusion.

6. **Add testing verification coordination** (Priority: P2)
   - **Current state**: Each testing principle defines separate verification mechanisms without coordination.
   - **Proposed change**: Reference a shared "Testing CI Framework" that coordinates live test gates, meta-test checks, and behavioral verification.
   - **Rationale**: Reduces CI complexity and provides unified testing verification.
   - **Risk if ignored**: Proliferating testing checks create CI maintenance burden and slow feedback cycles.

7. **Define testing lifecycle workflow** (Priority: P3)
   - **Current state**: Testing principles treat creation, maintenance, and fixing as separate concerns.
   - **Proposed change**: Add a workflow diagram showing how testing principles apply at different lifecycle stages.
   - **Rationale**: Provides clear guidance for when each principle applies during test evolution.
   - **Risk if ignored**: Developers must memorize complex principle interactions rather than following clear workflows.

8. **Integrate testing antipatterns** (Priority: P3)
   - **Current state**: Testing principles reference external antipattern catalog without integration.
   - **Proposed change**: Include testing-specific antipattern examples directly in relevant principles.
   - **Rationale**: Reduces external dependency and provides immediate context for testing discipline.
   - **Risk if ignored**: Testing antipatterns remain disconnected from enforcement mechanisms.

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/071-blind-2026-04-28/CONSTITUTION-v2.5.0-blind.md` — sections cited: L346-366 (Principle IX behavior-over-shape), L573-595 (Principle XXIV safety-critical), L597-632 (Principle XXV cost discipline), L654-675 (Principle XXVI meta-testing), L677-714 (Principle XXVIII test-fix), L361-363 (IX assertion rules), L693-695 (XXVIII assertion fidelity), L440-470 (constitutional inclusion criteria)