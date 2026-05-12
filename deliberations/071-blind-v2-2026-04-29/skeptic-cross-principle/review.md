### Executive Summary

The constitution establishes five testing-related principles that attempt to govern different aspects of test quality, cost management, and maintenance discipline. However, these principles suffer from significant architectural overlap and leave critical gaps in their coordination. The behavior-over-shape extension to Principle IX cleanly defers to test-fix discipline in Principle XXVIII, but the remaining principles create a fractured testing governance model where the boundaries between "ordinary production bugs" and "safety-critical production bugs" are undefined, meta-test maintenance requirements conflict with defunct test deletion procedures, and citation requirements drift across different test lifecycle stages. The strongest case for consolidation lies in merging Principles XXV and XXVIII into a unified "Test Lifecycle Discipline" principle that addresses the full spectrum of test creation, maintenance, and deletion in a coherent framework.

### Alignment

- **Clean deferral pattern** (L1035-1036): Principle XXVIII explicitly states "assertion-fidelity discipline is governed by Principle IX (behavior-over-shape extension)" rather than restating the same requirements, demonstrating proper single-source-of-truth discipline.

- **Mechanical verification consistency** (L1045-1047, L1061-1066): Both XXVI and XXVIII specify concrete mechanical checks (meta-test length assertions, diff-shape lint validation) that align with the constitutional inclusion criteria's requirement for automated verification capability.

- **Lifecycle stage separation** (L933-937 vs L1040-1047): XXV's cost justification requirement applies at test creation time while XXVIII's skip citation applies at test maintenance time, suggesting proper temporal boundaries rather than overlap.

### Missed Opportunities

- **Safety-critical boundary definition**: The constitution fails to define what distinguishes "safety-critical production bugs" requiring Defense-in-Depth contract tests from "ordinary production bugs" requiring only test-fix categorization. This creates enforcement ambiguity where contributors cannot determine which discipline applies.

- **Meta-test coordination with test deletion**: XXVI requires meta-tests for parametrize lists but XXVIII allows "defunct test" deletion without addressing whether the parametrize list must be updated simultaneously. This creates a mechanical gap where meta-tests could fail after legitimate test deletions.

- **Citation requirement convergence**: XXV and XXVIII establish parallel citation requirements (cost justification vs skip reasons) that could be unified under a broader test documentation discipline, reducing cognitive overhead for contributors managing both live tests and skip directives.

- **Test lifecycle state machine**: The principles treat test creation (XXV), maintenance (XXVIII), and coverage verification (XXVI) as independent concerns, missing the opportunity to define a coherent state transition model that governs how tests move through their lifecycle.

- **Cross-principle enforcement gaps**: The principles lack cross-references that would clarify interaction points, such as whether a "defunct test" deletion in a safety-critical path triggers Defense-in-Depth requirements or whether live test skips require both cost justification AND skip citation.

- **Temporal ordering conflicts**: The principles don't address scenarios where multiple disciplines apply simultaneously, such as when a live test in a safety-critical path gets skipped due to production bugs, potentially requiring compliance with XXV, XXIV, and XXVIII simultaneously.

### Off-Base Assumptions

- **Independent governance model assumption** (scattered throughout L923-1075): The constitution assumes that test creation, maintenance, and deletion can be governed by independent principles without coordination points. In practice, these activities form a connected lifecycle where decisions in one area directly impact others, making the fractured governance model actively harmful to contributor clarity.

- **Clear safety-critical boundary assumption** (L894-897 vs L1057): Principle XXIV assumes the boundary between synthesis/provider protocols and ordinary code paths is self-evident, but Principle XXVIII's production bug categorization makes no reference to safety-critical requirements, suggesting the boundary is actually unclear and requires explicit definition.

### Actionable Recommendations

1. **Define safety-critical boundary explicitly** (Priority: P1)
   - **Current state**: XXIV defines safety-critical paths as "synthesis verdict generation AND provider protocol implementation" (L894-897) but XXVIII's production bug category (L1057) makes no reference to these paths.
   - **Proposed change**: Add a Safety-Critical subsection to XXVIII that explicitly states: "Production bugs in synthesis verdict generation or provider protocol implementation paths MUST trigger Principle XXIV Defense-in-Depth requirements in addition to diff-shape categorization."
   - **Rationale**: Without this coordination, contributors cannot determine when Defense-in-Depth applies to production bug fixes, creating enforcement gaps in safety-critical paths.
   - **Risk if ignored**: Safety-critical bugs will be fixed with ordinary production bug discipline, violating the three-layer defense requirement and potentially reintroducing the same class of silent failures that motivated XXIV.

2. **Specify meta-test maintenance for defunct deletions** (Priority: P1)
   - **Current state**: XXVI requires meta-tests for parametrize lists (L972-985) but XXVIII allows test deletion (L1059) without addressing parametrize list updates.
   - **Proposed change**: Add to XXVIII: "Defunct test deletions from parametrized test modules MUST update the parametrize list in the same PR to maintain meta-test compliance per Principle XXVI."
   - **Rationale**: The two principles create a mechanical conflict where legitimate test deletions cause meta-test failures unless coordinated.
   - **Risk if ignored**: Contributors will either avoid deleting obsolete tests (accumulating test debt) or break meta-tests (undermining coverage verification).

3. **Unify citation requirements under test documentation discipline** (Priority: P2)
   - **Current state**: XXV requires cost justification in docstrings (L933-937), XXVIII requires skip citations (L1040-1047) - parallel requirements with different formats.
   - **Proposed change**: Create a unified "Test Documentation Standard" section that covers both cost justification and skip citation requirements with consistent formatting guidelines.
   - **Rationale**: Parallel citation requirements create cognitive overhead and format drift between similar documentation needs.
   - **Risk if ignored**: Contributors will inconsistently apply citation requirements, leading to maintenance burden and reduced test maintainability.

4. **Add cross-principle interaction matrix** (Priority: P2)
   - **Current state**: The five testing principles operate independently without explicit coordination points.
   - **Proposed change**: Add a "Testing Principle Interactions" subsection that explicitly addresses scenarios where multiple principles apply (live safety-critical tests, parametrized live tests, etc.).
   - **Rationale**: Complex scenarios require clarity about which principles take precedence and how requirements compose.
   - **Risk if ignored**: Contributors facing multi-principle scenarios will make inconsistent choices, undermining the constitutional framework's predictability.

5. **Consolidate XXV and XXVIII into unified test lifecycle principle** (Priority: P3)
   - **Current state**: XXV governs test cost discipline, XXVIII governs test maintenance - artificially separated concerns in the same lifecycle.
   - **Proposed change**: Merge into "Test Lifecycle Discipline" covering creation (cost markers), maintenance (skip discipline), and deletion (categorization) as a coherent state machine.
   - **Rationale**: Test lifecycle events are interconnected and benefit from unified governance rather than principle fragmentation.
   - **Risk if ignored**: The artificial separation will continue creating coordination gaps and contributor confusion about which principle governs edge cases.

6. **Remove redundant distinctness claim in constitutional inclusion criteria** (Priority: P3)
   - **Current state**: The inclusion criteria claim principles must be "distinct from existing principles" (L1139-1143) but the constitution contains five testing principles with clear overlap.
   - **Proposed change**: Either consolidate the testing principles to satisfy the distinctness criterion or acknowledge that the criterion was applied retrospectively and grandfathered principles may not satisfy it.
   - **Rationale**: The constitution violates its own inclusion criteria by maintaining overlapping testing principles, creating meta-constitutional inconsistency.
   - **Risk if ignored**: Future constitutional amendments will be held to a standard that existing principles demonstrably fail, undermining the credibility of the inclusion criteria.

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/071-blind-v2-2026-04-29/CONSTITUTION-v2.5.0-blind.md` — sections/lines cited: L383-407 (IX behavior-over-shape), L894-922 (XXIV safety-critical), L923-967 (XXV cost discipline), L972-994 (XXVI meta-testing), L1032-1075 (XXVIII test-fix), L1139-1143 (inclusion criteria)