# Implementation Engineer — Revision (Iteration 1)

## Recommendation Dispositions

#### Recommendation 1: Complete validator error object specification

- **Original position**: Add concrete Python class definitions, error factory methods, and jsonschema integration examples to § 4.9 as the foundation for both warning emission and CI gate detection.
- **Disposition**: Surviving
- **Explanation**: All three cross-reviews (naive-reader, risk-auditor, external-scholar) either explicitly agreed with this recommendation or did not challenge it. Risk-auditor's cross-review acknowledged this as a "core architecture" issue that "must be implementable" before operational planning can proceed. External-scholar focused on governance aspects but did not dispute the technical necessity. While naive-reader focused on CI mechanisms, they noted validator error specification as foundational. The lack of concrete Python implementation patterns in § 4.9 remains a blocking gap for implementation start.

#### Recommendation 2: Clarify fixture count and types

- **Original position**: Explicitly enumerate fixtures as "(a) conformant, (b) missing-required, (c) wrong-type, (d) enum-violation" and specify the total count is exactly four.
- **Disposition**: Surviving
- **Explanation**: Both naive-reader and risk-auditor explicitly agreed this was a problem in their cross-reviews, with naive-reader noting the "four vs three" ambiguity and risk-auditor acknowledging fixture specification inadequacy. External-scholar did not challenge this recommendation. The specification count ambiguity ("four fixture types" but describing "three types plus an additional enum-violation fixture") remains objectively present and blocks implementation.

#### Recommendation 3: Specify CI trigger completeness

- **Original position**: Add `templates/{mode}/` to trigger paths and specify trigger logic for output-affecting changes.
- **Disposition**: Surviving
- **Explanation**: Both naive-reader and risk-auditor agreed this was a problem in their cross-reviews, noting CI enforcement gaps and missing template directories from trigger paths. External-scholar did not challenge this. The missing trigger paths create an enforcement blind spot that must be addressed for proper CI coverage.

#### Recommendation 4: Add mode template migration implementation steps

- **Original position**: Specify slot marker patterns (`<<<FIELD_BEGIN>>>...<<<FIELD_END>>>`), parsing logic, and validation checkpoints per output type.
- **Disposition**: Modified
- **Explanation**: Naive-reader's cross-review elevated this to P1 priority, noting that template slot parsing is required for validator functionality. The circular dependency they identified (validator needs slot parsing, but slot parsing was treated as P2) is correct. **Modified recommendation**: Elevate to P1 priority and specify slot marker syntax as a prerequisite for validator implementation, not just a migration convenience.

#### Recommendation 5: Define performance budget by output type

- **Original position**: Specify budget ranges: review/cross-review <50ms, revision/disputes <75ms, synthesis/arbitration <150ms due to output size variance.
- **Disposition**: Surviving
- **Explanation**: External-scholar acknowledged the performance budget problem but didn't dispute the differentiated approach. Risk-auditor noted performance assumptions in their review but focused on operational risks rather than challenging the technical solution. Naive-reader's cross-review noted this as addressing size variance concerns. The universal <100ms budget ignores natural size differences between output types and is technically unsound.

#### Recommendation 6: Complete CONSUMER-CONTRACT.md linking specification

- **Original position**: Specify exact link text ("Persistence Contract") and markdown anchor format for README.md and CLAUDE.md links.
- **Disposition**: Surviving
- **Explanation**: Naive-reader agreed this was a problem in their cross-review, noting incomplete specification of link text and anchor format. Risk-auditor and external-scholar did not challenge this. The specification requires both README and CLAUDE links but doesn't specify how to implement them consistently.

#### Recommendation 7: Specify schema location verification mechanics

- **Original position**: Add CI check that greps for "engine/schema/v1" in both README.md and CLAUDE.md, failing if missing.
- **Disposition**: Surviving
- **Explanation**: None of the cross-reviews challenged this recommendation. The XXVIII sub-clause 1 requirement for discoverable location needs mechanical verification to ensure compliance.

#### Recommendation 8: Add temporal-constraint verification algorithm

- **Original position**: Specify git-based algorithm for verifying exemption applicability in future amendments.
- **Disposition**: Modified
- **Explanation**: External-scholar's cross-review noted that bootstrap patterns are "well-established" and the precedent framing was overstated, but they still supported the containment mechanisms having implementation value. **Modified recommendation**: Focus on the mechanical verification algorithm for the E2 technical precondition rather than framing it as novel precedent management. The algorithm is still needed to verify "no JSON Schema exists AND ratification stands schema up" for future amendments.

#### Recommendation 9: Specify GitHub Actions workflow completeness

- **Original position**: Provide complete `.github/workflows/schema-validate.yml` template with matrix strategies, artifact handling, and failure reporting.
- **Disposition**: Surviving
- **Explanation**: Naive-reader noted CI implementation gaps in their cross-review, supporting this recommendation. Risk-auditor and external-scholar focused on other aspects but didn't challenge the need for complete workflow specification. The incomplete CI specification creates implementation guesswork.

#### Recommendation 10: Add implementation order verification checkpoints

- **Original position**: Specify validation checkpoints between migration steps to verify step completion before proceeding.
- **Disposition**: Surviving
- **Explanation**: Risk-auditor's cross-review acknowledged implementation complexity and the need for operational risk management, which supports verification checkpoints. None of the cross-reviews challenged this recommendation. The multi-step rollout described in § 11 needs verification gates to prevent compound errors.

## New Recommendations

#### Strengthen E2 technical precondition enforcement

- **Priority**: P1
- **Triggered by**: External-scholar's cross-review noting that bootstrap patterns are standard, not novel, suggesting the containment mechanisms need to focus on mechanical verification rather than precedent novelty.
- **Proposed change**: In § 9.1 E2 technical precondition, add specific git commands for verification: condition (a) verified by `git ls-files engine/schema/v*/` returning empty; condition (b) verified by the spec's own ratification PR introducing the first schema files.
- **Rationale**: External-scholar correctly identified that bootstrap patterns are established practice, so the containment value lies in mechanical verification rather than precedent management. Concrete git commands make the technical precondition algorithmically verifiable by future amendment authors.

## Position Summary

I maintained 9 of my 10 original recommendations and modified 2 (template migration priority elevation and temporal-constraint verification focus). The most significant change in my thinking was recognizing that template slot syntax specification is a prerequisite for validator implementation, not a secondary migration concern—naive-reader's circular dependency analysis was correct.

My highest-priority surviving recommendation remains completing the validator error object specification in § 4.9 with concrete Python implementation patterns. This is the foundation that all other technical implementations depend on, and no cross-review challenged its necessity. The specification's implementability depends on resolving this technical foundation before engineers can proceed with CI gates, fixtures, or schema validation.

The cross-review process strengthened rather than weakened my implementability assessment. Multiple agents independently identified similar gaps from different perspectives, creating convergent evidence that the specification has concrete technical requirements that must be addressed before implementation can proceed successfully.