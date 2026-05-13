### Recommendation Dispositions

#### Recommendation 1: Complete validator error object specification

- **Original position**: Add concrete Python class definitions, error factory methods, and jsonschema integration examples to § 4.9 as the foundation for both warning emission and CI gate detection
- **Disposition**: Modified  
- **Explanation**: naive-reader's cross-review identified a crucial circular dependency: "template slot parsing is required for validator functionality" while I claimed validator error specification was foundational first. Their analysis was correct - the validator cannot function without knowing how to parse agent output into the JSON envelope. I now recognize that template slot syntax specification must precede validator error specification, though both remain genuinely P1. The validator can initially work with dummy/hardcoded input during development while template parsing is refined, but the slot parsing foundation enables the validator architecture, not the reverse.

#### Recommendation 2: Clarify fixture count and types

- **Original position**: Explicitly enumerate fixtures as "(a) conformant, (b) missing-required, (c) wrong-type, (d) enum-violation" and specify the total count is exactly four
- **Disposition**: Surviving
- **Explanation**: All cross-reviewers agreed this is an objective ambiguity requiring resolution. external-scholar noted both reviews identified the "four vs three" fixture count problem and external-scholar's governance analysis confirms this blocks both implementation start and governance consistency. The specification count ambiguity remains objectively present and blocks implementation.

#### Recommendation 3: Specify CI trigger completeness

- **Original position**: Add `templates/{mode}/` to trigger paths and specify trigger logic for output-affecting changes to close enforcement blind spots
- **Disposition**: Surviving
- **Explanation**: naive-reader agreed this was a "CI enforcement gap" in their cross-review analysis, and risk-auditor confirmed "No cross-review challenged the need for explicit coordination mechanisms." The missing trigger paths create an enforcement blind spot that must be addressed for proper CI coverage. The technical specifics I provided complement the operational context others identified.

#### Recommendation 4: Add mode template migration implementation steps

- **Original position**: Specify slot marker patterns (`<<<FIELD_BEGIN>>>...<<<FIELD_END>>>`), parsing logic, and validation checkpoints per output type as the highest-risk implementation step
- **Disposition**: Modified
- **Explanation**: naive-reader's cross-review identified this as universally acknowledged as a foundational gap, but their circular dependency analysis was correct. Template slot syntax specification is a prerequisite for validator implementation, not a secondary migration concern. I now elevate this to P1 priority and recognize it must precede validator error specification work. Both are genuinely P1, but slot syntax enables validator functionality.

#### Recommendation 5: Define performance budget by output type  

- **Original position**: Specify budget ranges: review/cross-review <50ms, revision/disputes <75ms, synthesis/arbitration <150ms due to output size variance
- **Disposition**: Modified
- **Explanation**: Both naive-reader and risk-auditor correctly challenged the sequence. naive-reader stated "validate the <100ms performance assumption against representative large outputs before finalizing the architecture," and risk-auditor's modified recommendation incorporates differentiated budgets with prerequisite validation. I now accept that validation testing must precede budget specification. We should first validate feasibility against real large outputs, then set differentiated budgets based on empirical data rather than theoretical estimates.

#### Recommendation 6: Complete CONSUMER-CONTRACT.md linking specification

- **Original position**: Specify exact link text ("Persistence Contract") and markdown anchor format for README.md and CLAUDE.md links per XXVIII sub-clause 1 compliance
- **Disposition**: Surviving
- **Explanation**: naive-reader agreed this was a gap "all three cross-reviewers agreed" on in their cross-review analysis. external-scholar noted convergent analysis from different angles showing both content and linking mechanics gaps. The link consistency requirement enables automated verification of XXVIII sub-clause 1 compliance, which requires specific implementation patterns.

#### Recommendation 7: Specify schema location verification mechanics

- **Original position**: Add CI check that greps for "engine/schema/v1" in both README.md and CLAUDE.md, failing if missing, to mechanically verify discoverable location requirement
- **Disposition**: Surviving  
- **Explanation**: No cross-review challenged the technical necessity of mechanical verification for XXVIII sub-clause 1. Location declarations may drift without detection, violating XXVIII sub-clause 1, and the grep-based verification provides the mechanical enforcement the principle requires.

#### Recommendation 8: Add temporal-constraint verification algorithm

- **Original position**: Specify git-based algorithm for verifying the E2 technical precondition that future engineers need for mechanical verification of exemption applicability
- **Disposition**: Modified
- **Explanation**: external-scholar's cross-review argued for "active containment rather than normalization" while I focused on "mechanical verification rather than precedent management." I now recognize these serve complementary purposes: external-scholar's containment mechanisms provide the governance safeguards, while my mechanical verification algorithms make the containment algorithmically enforceable rather than interpretation-dependent. Focus on the mechanical verification algorithm for the E2 technical precondition rather than framing it as novel precedent management. Concrete git commands make the technical precondition algorithmically verifiable by future amendment authors.

#### Recommendation 9: Specify GitHub Actions workflow completeness

- **Original position**: Provide complete `.github/workflows/schema-validate.yml` template with matrix strategies, artifact handling, and failure reporting to eliminate CI configuration guesswork  
- **Disposition**: Surviving
- **Explanation**: naive-reader agreed on "CI implementation specification insufficiency" in their cross-review analysis, noting both perspectives identify CI gates as under-specified. Complete specifications are valuable for reducing implementation guesswork and standardizing enforcement across environments, though I acknowledge the broader CI feasibility validation naive-reader recommended should also occur.

#### Recommendation 10: Add implementation order verification checkpoints

- **Original position**: Specify validation checkpoints between steps in § 11's multi-step rollout to reduce compound error risk during complex implementation
- **Disposition**: Surviving
- **Explanation**: risk-auditor agreed this addresses "multi-step migration complexity" from their operational risk perspective in their cross-review analysis. Both technical step validation and operational contingency planning are needed to cover technical and operational failure modes in the complex migration path § 11 outlines.

### New Recommendations

**Elevate template slot syntax specification** (Priority: P1)
- **Triggered by**: naive-reader's circular dependency analysis in their cross-review of me, confirmed by external-scholar's agreement that "governance clarity and technical implementability are interdependent"
- **Proposed change**: Template slot syntax specification (`<<<FIELD_BEGIN>>>...<<<FIELD_END>>>` parsing patterns, escape sequences, validation) must be completed before validator error object specification, as validator functionality depends on slot parsing capability
- **Rationale**: The validator cannot parse agent output into JSON envelopes without slot syntax definition. This creates a foundational dependency that my original sequencing missed. Both are P1, but slot syntax enables the validator architecture.

### Position Summary

I modified 3 recommendations based on cross-review feedback, withdrew 0, and maintained 7 as surviving. The most significant change in my thinking was recognizing the circular dependency between validator error specification and template slot syntax - naive-reader's analysis correctly identified that slot syntax must come first since the validator depends on parsing capabilities, not the reverse.

My highest-priority surviving recommendation is completing the fixture count clarification (Recommendation 2), as this objective ambiguity in the spec text blocks implementation start and was confirmed as problematic by all cross-reviewers. The specification's "four vs three" fixture count problem requires immediate resolution before any validator implementation work can proceed meaningfully. This foundational gap, combined with the elevated template slot syntax specification, represents the critical path for making the spec implementable by engineers without additional guidance.