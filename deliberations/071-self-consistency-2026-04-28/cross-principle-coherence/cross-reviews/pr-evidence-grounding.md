### Dangerous Contradictions

- **Evidence-pending vs. amendment approach**
  - **pr-evidence-grounding claims**: "Flag this amendment as 'evidence-pending' until the supporting investigation artifacts, PR #42 analysis, and mechanical verification capabilities can be independently validated" (Executive Summary) and recommends deferring ratification entirely (Recommendation 1).
  - **cross-principle-coherence claims**: Recommends seven specific amendments to XXVIII's text to resolve cross-principle conflicts and make it compositional with existing principles (Actionable Recommendations 1-7).
  - **Why this is dangerous**: If pr-evidence-grounding's deferral is accepted, cross-principle-coherence's textual amendments become irrelevant. If cross-principle-coherence's amendments are implemented while evidence issues remain unresolved, the principle gains constitutional authority based on unverified empirical claims.
  - **Suggested resolution**: Implement cross-principle-coherence's amendments AND adopt pr-evidence-grounding's evidence-pending status. The amended text addresses internal consistency issues while the evidence-pending status prevents ratification until empirical claims are validated.

- **Constitutional gate compliance assessment scope**
  - **pr-evidence-grounding claims**: "Promised scripts satisfy mechanical verification" assumption is off-base (Off-Base Assumptions, L16-22) and recommends requiring "actual implementation of the lint script" (Recommendation 4).
  - **cross-principle-coherence claims**: "SIR claims Criterion 3 (distinctness) PASS but XXVIII clause 1 directly overlaps IX's operational test definition" (Off-Base Assumptions) and recommends acknowledging "this extends IX rather than being fully distinct" (Recommendation 6).
  - **Why this is dangerous**: The reviews identify different Constitutional Inclusion Criteria violations - pr-evidence-grounding focuses on Criterion 1 (mechanical verification) while cross-principle-coherence focuses on Criterion 3 (distinctness). Both could be correct, meaning XXVIII fails multiple gate criteria.
  - **Suggested resolution**: Combine both assessments - acknowledge that XXVIII likely fails both Criterion 1 (no existing verification mechanism) AND Criterion 3 (overlaps with IX) rather than treating them as alternative gate failures.

- **Verification mechanism status**
  - **pr-evidence-grounding claims**: The lint script "doesn't exist" and the SIR makes promises about future capabilities that don't satisfy current gate requirements (Recommendations 4, 7).
  - **cross-principle-coherence claims**: The verification mechanism is "underspecified rather than concrete" and should be made "visible and actionable for implementors" by referencing the promised script (Recommendation 4).
  - **Why this is dangerous**: pr-evidence-grounding treats the missing script as a blocker requiring actual implementation, while cross-principle-coherence treats it as a documentation issue requiring better specification. These approaches pull in opposite directions - one stops ratification, the other fixes the text.
  - **Suggested resolution**: pr-evidence-grounding should yield - the Constitutional gate explicitly allows promised verification mechanisms if they're "concrete enough that an engineer reading the principle can sketch the check in one paragraph." cross-principle-coherence's documentation fix addresses the concreteness requirement without requiring actual implementation.

### Tensions

- **Fix-first vs. evidence-first priority**
  - **pr-evidence-grounding's position**: Multiple P1 recommendations focus on evidence validation and investigation artifact preservation before addressing the principle's content (Recommendations 1-3).
  - **cross-principle-coherence's position**: Multiple P1 recommendations focus on fixing the principle's cross-references and lifecycle coordination issues (Recommendations 1-2).
  - **Nature of tension**: Both approaches are necessary but have different timelines - evidence validation could take significant time while textual amendments can be implemented immediately.
  - **Coordination needed**: Sequence the work - implement cross-principle-coherence's textual fixes first (they improve the principle regardless of evidence status), then resolve pr-evidence-grounding's evidence validation requirements before final ratification.

- **Gate interpretation strictness**
  - **pr-evidence-grounding's position**: Interprets Constitutional Inclusion Criteria as requiring existing verification mechanisms: "The Constitutional Inclusion Criteria gate should verify actual capability, not promised capability" (Recommendation 4).
  - **cross-principle-coherence's position**: Accepts promised verification mechanisms but requires them to be properly documented: "Makes the claimed mechanical verification capability visible and actionable" (Recommendation 4).  
  - **Nature of tension**: Different readings of the same gate text - whether "feasible" verification requires implementation or just concrete specification.
  - **Coordination needed**: Clarify gate interpretation precedent - review how previous principles (post-v2.4.0) have satisfied Criterion 1 and apply consistent standards.

- **Scope of constitutional evidence requirements**
  - **pr-evidence-grounding's position**: Wants constitutional amendments to preserve all supporting investigation artifacts and establish evidence validation protocols (Recommendations 2, 6).
  - **cross-principle-coherence's position**: Focuses on the principle's internal consistency and relationship to existing constitutional principles without addressing broader evidence standards.
  - **Nature of tension**: pr-evidence-grounding proposes meta-constitutional process changes while cross-principle-coherence works within existing constitutional frameworks.
  - **Coordination needed**: Determine whether evidence validation protocols belong in the constitution itself or in separate governance procedures - both reviews' recommendations can coexist if properly scoped.

- **Empirical claim treatment**
  - **pr-evidence-grounding's position**: Treats unverifiable empirical claims as disqualifying: "Constitutional amendments will be ratified based on unverifiable claims, undermining the constitutional authority" (Recommendation 1).
  - **cross-principle-coherence's position**: Focuses on whether the principle's logic is sound independent of its empirical justification, treating the Origin note as context rather than foundation.
  - **Nature of tension**: Different standards for how constitutional principles should be grounded - empirical evidence vs. logical consistency.
  - **Coordination needed**: Establish constitutional precedent for empirical vs. logical grounding - some principles may be valid based on logical necessity even if their motivating examples are unverifiable.

### Safe Agreements

- **Constitutional Inclusion Criteria gate issues**
  - **Shared position**: Both reviews identify problems with the SIR's Constitutional Inclusion Criteria assessment, though focusing on different criteria (pr-evidence-grounding: "Promised scripts satisfy mechanical verification" assumption is off-base; cross-principle-coherence: "SIR claims Criterion 3 (distinctness) PASS but XXVIII clause 1 directly overlaps IX's operational test definition").
  - **Combined evidence**: pr-evidence-grounding documents the missing verification infrastructure while cross-principle-coherence demonstrates the overlap with existing principles - together they show XXVIII's gate assessment is incomplete.
  - **Confidence level**: High - both reviews provide specific textual evidence for different aspects of gate non-compliance.

- **Mechanical verification specification inadequacy**
  - **Shared position**: Both identify that the mechanical verification capability claimed in the SIR is inadequately specified in the principle text (pr-evidence-grounding: recommends implementing the script; cross-principle-coherence: recommends documenting the verification mechanism better).
  - **Combined evidence**: pr-evidence-grounding shows the verification mechanism doesn't exist, cross-principle-coherence shows even the promised mechanism lacks concrete specification - gap exists at both implementation and documentation levels.
  - **Confidence level**: High - both reviews provide actionable recommendations that address different aspects of the same underlying problem.

- **Need for specific textual amendments**
  - **Shared position**: Both reviews recommend specific, actionable changes to the constitutional text rather than wholesale rejection (pr-evidence-grounding: 7 numbered recommendations; cross-principle-coherence: 7 numbered recommendations with specific text proposals).
  - **Combined evidence**: pr-evidence-grounding focuses on evidence grounding and validation protocols while cross-principle-coherence focuses on cross-references and lifecycle coordination - complementary amendment categories that don't conflict.
  - **Confidence level**: Medium - while both recommend amendments, pr-evidence-grounding's deferral stance creates uncertainty about whether amendments should be implemented before or after evidence validation.

- **Recognition of principle's sound intent**
  - **Shared position**: Both reviews acknowledge the underlying value of XXVIII's test-fix discipline despite their identified problems (pr-evidence-grounding: "The principle aims to codify test-fix discipline to prevent production bugs"; cross-principle-coherence: "While the intent is sound").
  - **Combined evidence**: Neither review attacks the fundamental concept, instead both provide constructive improvement paths - pr-evidence-grounding through evidence validation, cross-principle-coherence through better integration with existing principles.
  - **Confidence level**: Medium - while both acknowledge value, pr-evidence-grounding's evidence concerns create more fundamental challenges to ratification than cross-principle-coherence's integration issues.