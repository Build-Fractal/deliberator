### Executive Summary

The constitution's Principle XXVIII (Test-Fix Boundary Preservation) attempts to establish discipline around fixing failing tests to prevent real bugs from being swept under the rug during test cleanup. The principle aims to ensure that when tests are made green, their verification of actual system behavior is preserved rather than simply making the test pass through assertion weakening or incorrect categorization of the underlying issue.

From a logical coherence perspective, the principle suffers from a fundamental mismatch between its stated goal and its enforcement mechanisms. The headline promises preservation of "verification of real behavior" but the body delivers only process and metadata checks that operate at the surface level. While the categorization framework (fixture drift, production bug, legitimate test bug, defunct test) provides useful structure, the mechanical verification claims cannot substantively detect when the principle's core intent is violated.

My most important recommendation is that this principle either needs stronger behavioral verification mechanisms that actually check assertion fidelity, or it should be reframed as a process discipline principle rather than claiming to preserve behavioral verification.

### Alignment

- **No external documentation provided**: No grounding material was listed for this review, so alignment assessment is limited to logical analysis of the principle itself.

### Missed Opportunities

- **Assertion content verification**: The principle cross-references Principle IX for "assertion-fidelity discipline" but provides no mechanism to verify that test fixes don't weaken behavioral assertions into shape-only checks. A stronger verification system would analyze assertion changes semantically, not just structurally.

- **Test quality metrics**: The principle focuses on categorization but misses opportunities to measure assertion strength degradation. Metrics on assertion specificity, behavioral coverage, or mutation test survival rates could provide quantitative verification of boundary preservation.

- **Cross-principle enforcement**: While referencing Principle IX's behavior-over-shape testing requirements, there's no enforcement link ensuring test fixes comply with that principle's operational test criteria.

- **Remediation tracking**: The skip discipline requires timeline citations but provides no verification that cited timelines are reasonable or that skipped tests are actually re-enabled as promised.

- **Historical pattern analysis**: The principle emerges from a single incident but doesn't leverage patterns from multiple fix scenarios to refine the categorization framework or identify additional violation modes.

- **Semantic diff analysis**: The diff-shape consistency check operates at file-level granularity but misses opportunities for semantic analysis of assertion changes within test files.

### Off-Base Assumptions

- **Mechanical verification sufficiency**: The principle assumes that format-checking surface signals (citation patterns, diff shapes) can meaningfully enforce behavioral intent preservation. This assumption is internally contradicted by the acknowledgment that "misjudgment is not [structurally detectable]."

- **Category exhaustiveness**: The four-category framework assumes all legitimate test fixes can be cleanly classified, but edge cases like framework API changes with behavioral implications blur the fixture/production-bug boundary.

- **Skip vs deletion consistency**: The principle assumes skips-with-timelines and deletion-for-defunct-tests are consistent policies, but provides no clear guidance for "temporarily disabled pending framework fix" scenarios.

### Actionable Recommendations

1. **Reframe headline promise** (Priority: P1)
   - **Current state**: "When fixing a failing test, the fix MUST preserve the test's verification of real behavior" (L1073)
   - **Proposed change**: "When fixing a failing test, the fix MUST follow categorization discipline and skip citation requirements to prevent silent behavior verification loss"
   - **Rationale**: Current headline overpromises what the mechanical disciplines can verify
   - **Risk if ignored**: Constitutional Inclusion Criterion 1 violation - mechanical verification claims that don't actually verify the stated intent

2. **Clarify skip-deletion boundary** (Priority: P1)
   - **Current state**: Skip discipline allows temporary disabling while defunct test category requires deletion
   - **Proposed change**: Add explicit guidance on when temporary skips vs immediate deletion apply
   - **Rationale**: Current logic creates inconsistency between temporarily disabled and defunct test handling
   - **Risk if ignored**: Confusion about when to skip vs delete, undermining both disciplines

3. **Strengthen Principle IX cross-reference** (Priority: P2)
   - **Current state**: "Assertion-fidelity discipline is governed by Principle IX" (L1074-1075)
   - **Proposed change**: Specify that test fixes MUST pass Principle IX's operational test criteria for behavior-over-shape validation
   - **Rationale**: Current cross-reference is decorative rather than enforceable
   - **Risk if ignored**: Gap between promised behavioral verification and actual process checking

4. **Enhance mechanical check claims** (Priority: P2)
   - **Current state**: Claims mechanical verification of boundary preservation through format checks
   - **Proposed change**: Acknowledge explicitly that mechanical checks verify process compliance, not behavioral preservation
   - **Rationale**: Current claims overstate what format checking can verify
   - **Risk if ignored**: False confidence in verification completeness

5. **Refine categorization edge cases** (Priority: P3)
   - **Current state**: Four-category framework assumes clean classification
   - **Proposed change**: Add guidance for hybrid scenarios (framework changes affecting behavior)
   - **Rationale**: Current categories don't cleanly handle all legitimate fix types
   - **Risk if ignored**: Arbitrary categorization decisions weakening the discipline

6. **Add evidence base diversification** (Priority: P3)
   - **Current state**: Single-incident origin from coverage verification deliberation
   - **Proposed change**: Reference additional scenarios where the discipline applies beyond the original investigation
   - **Rationale**: Constitutional principles should demonstrate general applicability
   - **Risk if ignored**: Perception of overfitting to specific incident circumstances

### Referenced Documentation

- `CONSTITUTION-v2.5.0-blind.md` — sections/lines cited: L1073-1095 (Principle XXVIII), L511-528 (Principle IX behavior-over-shape extension)