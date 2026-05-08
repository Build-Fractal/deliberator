### Dangerous Contradictions

- **Arithmetic error prioritization conflict**
  - **mechanical-verifiability claims**: Rates "Specify duplication detection algorithm" as P1 priority, focusing on the "string-match heuristic" implementation details as the most critical gap (Actionable Recommendations #1).
  - **structural-integrity claims**: Rates "Fix tier classification arithmetic" as P1 priority, identifying a fundamental counting error where "spec claims 26 active principles but tier assignments only total 25" (Actionable Recommendations #1).
  - **Why this is dangerous**: If we implement the duplication detection algorithm without fixing the underlying arithmetic error, the linter will be checking for completeness against an incorrect baseline. The algorithm will validate the wrong principle count, potentially allowing the fundamental structural flaw to persist through implementation.
  - **Suggested resolution**: structural-integrity's arithmetic fix must be completed before mechanical-verifiability's algorithm specification. The counting error affects the scope of what the algorithm needs to validate.

- **Manual review reliability assessment**
  - **mechanical-verifiability claims**: "Manual review reliability assumption" is off-base, stating "automated checks are typically more reliable for mechanical verification tasks" and questions treating manual "negative checks" as authoritative (Off-Base Assumptions section).
  - **structural-integrity claims**: Recommends "Clarify linter vs manual check relationship" as P1, suggesting manual checks serve as "authoritative verification for complex edge cases" while automated linters handle subset verification (Actionable Recommendations #3).
  - **Why this is dangerous**: These positions create conflicting implementation guidance. If manual checks are unreliable, making them "authoritative for edge cases" is contradictory. If automated checks are always superior, the spec's Section 7 manual verification design is fundamentally flawed.
  - **Suggested resolution**: mechanical-verifiability should yield on wholesale rejection of manual checks. Instead, focus on making manual checks more systematic and auditable while automating what can be automated. The hybrid approach is more realistic than pure automation.

- **Implementation completeness vs. algorithm precision**
  - **mechanical-verifiability claims**: Focuses heavily on algorithm specification details like "exact substring match of principle body text after normalizing whitespace" and "SHA-256 hashes of principle bodies" (Actionable Recommendations #1, #2).
  - **structural-integrity claims**: Identifies missing file edits like "Add conversus governance log edit" and structural gaps like missing "file-edit dependency ordering" (Actionable Recommendations #2, #5).
  - **Why this is dangerous**: Implementing precise algorithms for an incomplete edit specification will produce a well-functioning linter that validates against the wrong scope. The structural gaps mean some changes won't be verified at all, regardless of algorithm quality.
  - **Suggested resolution**: structural-integrity's completeness checks should be resolved before mechanical-verifiability's precision refinements. Complete the edit specification first, then optimize the validation algorithms.

### Tensions

- **Verification philosophy: automated vs. hybrid approaches**
  - **mechanical-verifiability's position**: Strongly emphasizes automated verification, rating "fuzzy duplication detection" and "automated cross-reference validation" as high-impact missed opportunities (Missed Opportunities section).
  - **structural-integrity's position**: Accepts hybrid verification, recommending "manual 'negative checks'" as complementary to automated linter (Actionable Recommendations #3).
  - **Nature of tension**: These approaches represent different philosophies about verification reliability. Pure automation is theoretically superior but may miss edge cases; hybrid approaches acknowledge human judgment value but introduce consistency risks.
  - **Coordination needed**: Establish clear boundaries for when automation is sufficient vs. when manual verification adds value. Define specific criteria for escalating from automated to manual review.

- **Specification granularity preferences**
  - **mechanical-verifiability's position**: Demands very specific algorithmic details like "Define normalization as 'collapse multiple whitespace characters to single spaces'" (Actionable Recommendations #7).
  - **structural-integrity's position**: Focuses on structural completeness like ensuring "all tier principle sets equals the complete active principle set, with no overlaps" (Actionable Recommendations #6).
  - **Nature of tension**: These represent different approaches to specification quality - algorithmic precision vs. structural coverage. Both are necessary but require different types of detail.
  - **Coordination needed**: Layer the specifications - establish structural completeness first (structural-integrity focus), then add algorithmic precision (mechanical-verifiability focus) within that complete framework.

- **Priority weighting between foundational vs. refinement issues**
  - **mechanical-verifiability's position**: Treats algorithm specification and verbatim preservation automation as co-equal P1 priorities (Actionable Recommendations #1, #2).
  - **structural-integrity's position**: Treats arithmetic errors and missing file edits as foundational P1 issues that must be resolved before refinements (Actionable Recommendations #1, #2).
  - **Nature of tension**: This reflects different theories of technical debt - fix algorithms vs. fix foundations first. Both approaches have merit depending on the type of system failure being prevented.
  - **Coordination needed**: Establish dependency relationships between foundational and refinement fixes. Foundational issues (counting, completeness) should generally precede algorithmic refinements.

- **Scope of cross-reference validation**
  - **mechanical-verifiability's position**: Recommends "cross-reference resolution validation" to "parse Markdown links and verify that all internal cross-references resolve" (Actionable Recommendations #5).
  - **structural-integrity's position**: Recommends "cross-tier cross-reference validation" to ensure "cross-references between tiers use correct relative paths" (Actionable Recommendations #6).
  - **Nature of tension**: These overlap but emphasize different aspects - link resolution vs. path correctness. Both are needed but could duplicate effort if implemented independently.
  - **Coordination needed**: Combine these into a unified cross-reference validation system that checks both resolution and path correctness in a single pass.

- **Tombstone and historical preservation approaches**
  - **mechanical-verifiability's position**: Does not explicitly address retired principle handling in their recommendations.
  - **structural-integrity's position**: Specifically addresses "retired principle tombstone accuracy" verification (Actionable Recommendations #4).
  - **Nature of tension**: This represents a gap where structural-integrity covers historical preservation concerns that mechanical-verifiability doesn't address, potentially creating incomplete verification coverage.
  - **Coordination needed**: mechanical-verifiability should incorporate tombstone verification into their algorithmic framework to ensure retired principles are properly handled by the linter.

### Safe Agreements

- **Tier-coherence linter is essential infrastructure**
  - **Shared position**: Both reviews identify the tier-coherence linter as critical P1 infrastructure. mechanical-verifiability states it "correctly identifies that structural amendments require mechanical verification" (Alignment section). structural-integrity notes it as "the minimum mechanical check Constitutional Inclusion Criterion 1 demands" (Actionable Recommendations #3).
  - **Combined evidence**: mechanical-verifiability provides Constitutional Inclusion Criterion 1 compliance justification; structural-integrity provides structural amendment verification necessity. Together, these establish both regulatory and architectural requirements for the linter.
  - **Confidence level**: High. Both perspectives converge on necessity with complementary justifications.

- **Verbatim preservation requires automated verification**
  - **Shared position**: Both reviews identify verbatim preservation automation as high priority. mechanical-verifiability recommends "extend tier-coherence linter to compute SHA-256 hashes" for byte-equality verification (Actionable Recommendations #2). structural-integrity identifies that "Section 5 verbatim preservation contract relies on manual verification" as needing automation (Actionable Recommendations #2).
  - **Combined evidence**: mechanical-verifiability provides technical implementation approach (cryptographic hashing); structural-integrity identifies the gap in current specification. The combination shows both the need and a viable solution path.
  - **Confidence level**: High. Technical feasibility and specification gap both clearly established.

- **Cross-reference validation gaps need addressing**
  - **Shared position**: Both reviews identify cross-reference validation as underspecified. mechanical-verifiability notes "cross-reference rewriting is specified but not verified mechanically" (Missed Opportunities section). structural-integrity recommends "cross-tier cross-reference validation" for relative path accuracy (Actionable Recommendations #6).
  - **Combined evidence**: mechanical-verifiability demonstrates the specification describes rewriting without validation; structural-integrity shows tier-specific path correctness concerns. Together they cover both general link resolution and tier-specific path validation.
  - **Confidence level**: Medium. Agreement on need is strong, but implementation approach requires coordination between the two different scopes identified.

- **Version consistency enforcement addresses real failure modes**
  - **Shared position**: Both reviews recognize version consistency as important. mechanical-verifiability states it "addresses a concrete failure mode and is mechanically implementable" (Alignment section). structural-integrity includes version synchronization in missed opportunities for "automated consistency checking" (Missed Opportunities section).
  - **Combined evidence**: mechanical-verifiability establishes mechanical feasibility; structural-integrity identifies it as a systematic gap. Both recognize this as addressing operational failure modes rather than theoretical concerns.
  - **Confidence level**: High. Both mechanical feasibility and operational necessity are established from different analytical angles.