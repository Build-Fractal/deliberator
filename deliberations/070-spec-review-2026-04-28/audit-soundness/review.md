### Executive Summary

Spec 070 conducts a formal audit of three grandfathered constitutional principles (VI, X, XVI) against the v2.4.0 Constitutional Inclusion Criteria gate, proposing migration paths for those that fail. The spec's analytical framework is methodologically sound, applying each criterion systematically across all three principles. However, the introduction of a novel "SPLIT" verdict for Principle XVI creates tension with the binary pass/fail nature of the constitutional gate, and some reasoning lacks sufficient concreteness to meet the gate's "one paragraph sketch" standard for mechanical verification. The spec's most significant contribution is demonstrating how the v2.4.0 gate applies retroactively to existing principles, but it risks implicit redefinition of what "passing" means.

Most important recommendation: **Clarify whether the SPLIT verdict is a legitimate third disposition under the constitutional gate or constitutes an unauthorized redefinition of the gate's binary criteria.**

### Alignment

- **Systematic criterion application** (L30, L52-64, L72-84, L92-107): The spec correctly applies all three constitutional criteria (mechanical verification, falsifiable scope, distinctness) to each principle individually, providing verdicts per criterion. This follows the gate's requirement for comprehensive evaluation against all criteria. [CONSTITUTION.md, L1078-1099]

- **Grandfathering provision compliance** (L10-12, L24): The spec correctly identifies itself as the "migration spec" anticipated by the v2.4.0 grandfathering language and positions the audit as prospective guidance rather than retroactive enforcement. [CONSTITUTION.md, L1115-1119]

- **Non-goals scope discipline** (L36-42): The spec explicitly excludes auditing the other 24 principles, redefining the gate, and performing migrations within the spec itself, maintaining appropriate boundaries for a governance-meta audit.

- **Constitutional precedence recognition** (L6-7): The spec correctly identifies that it operates under the constitutional amendment process and that implementation PRs will be governed by existing verification protocols (spec 067).

### Missed Opportunities

- **Concrete mechanization sketches**: The spec repeatedly concludes that principles fail Criterion 1 without providing the "one paragraph sketch" the constitutional gate actually requires. For Principle VI, the spec could sketch a concrete CI lint that flags `.md` files in specific directories (`skills/`, `presets/`, `templates/`) as a partial mechanization, even if acknowledging this captures only a subset of the principle's scope. Impact: **medium** - reduces confidence in verdicts.

- **Gate-text line citations**: When applying constitutional criteria, the spec references the gate conceptually but never cites specific lines from CONSTITUTION.md L1078-1099. Direct quotation would strengthen the audit's grounding and demonstrate that verdicts follow from constitutional text rather than interpretation. Impact: **medium** - weakens evidence base.

- **Precedent analysis for SPLIT disposition**: The spec introduces a novel "SPLIT" verdict without examining whether the constitutional gate permits partial compliance. The gate text uses binary language ("qualifies for constitutional inclusion only if it satisfies all three"). Impact: **high** - creates constitutional interpretation ambiguity.

- **Verification artifact identification**: For principles that DO pass criteria (like XVI's structural substrate), the spec doesn't identify what the "verification artifact" would be, despite this being required by the constitutional gate. Impact: **medium** - incomplete compliance analysis.

- **Cross-principle composition analysis**: When evaluating Criterion 3 (distinctness), the spec could more rigorously examine whether failing principles could be composed from existing passing principles, which would strengthen the migration rationale. Impact: **low** - missed analytical depth.

- **Migration risk quantification**: While Section 5.2 identifies migration risks, it doesn't assess the relative severity of keeping a failing principle vs. migrating it, which would inform prioritization decisions. Impact: **medium** - incomplete risk analysis.

### Off-Base Assumptions

- **Binary gate interpretation**: The spec assumes the constitutional gate permits a "SPLIT" verdict where some criteria pass and others fail (L93, L99, L107), but the gate text states principles qualify "only if [they satisfy] all three" criteria. This suggests the gate requires unanimous passage, not partial credit.

- **"Sketch concreteness" standard**: The spec applies an unstated standard for what constitutes a "concrete enough" sketch for mechanical verification, but the constitutional text only requires the sketch be "concrete enough that an engineer reading the principle can sketch the check in one paragraph." The spec's rejections may be overly stringent.

- **Grandfathering as protection**: The spec assumes grandfathered principles need "protection" from the gate (L40-41), but the constitutional text frames grandfathering as a transition mechanism, not permanent immunity. This colors the spec's urgency assessment.

### Actionable Recommendations

1. **Resolve SPLIT verdict constitutionality** (Priority: P1)
   - **Current state**: The spec introduces a "SPLIT" disposition for Principle XVI where some criteria pass and others fail (L93-107).
   - **Proposed change**: Either demonstrate that the constitutional gate permits partial compliance or reframe the SPLIT as a standard FAIL with nuanced migration options.
   - **Rationale**: The gate text "only if it satisfies all three" suggests binary evaluation; partial compliance may constitute gate redefinition.
   - **Risk if ignored**: Constitutional interpretation precedent that undermines the gate's authority and creates ambiguous compliance standards.

2. **Provide mechanization sketches for all FAIL verdicts** (Priority: P1)
   - **Current state**: The spec concludes principles fail Criterion 1 without sketching the required mechanical checks (L54, L74).
   - **Proposed change**: Add one-paragraph sketches showing how CI lints could partially enforce each failing principle, even if acknowledging limitations.
   - **Rationale**: The constitutional gate requires demonstration that mechanical verification is feasible, not that it's currently implemented.
   - **Risk if ignored**: Verdicts appear unsupported and may not meet the gate's evidential standard.

3. **Add direct constitutional citations** (Priority: P2)
   - **Current state**: The spec references gate criteria conceptually without quoting specific constitutional text.
   - **Proposed change**: Quote relevant lines from CONSTITUTION.md L1078-1099 when applying each criterion.
   - **Rationale**: Direct citation demonstrates that verdicts derive from constitutional text rather than interpretation.
   - **Risk if ignored**: Reduced credibility and potential for constitutional misapplication.

4. **Clarify verification artifacts for passing components** (Priority: P2)
   - **Current state**: For XVI's structural substrate that allegedly passes criteria, no verification artifact is identified (L95-96).
   - **Proposed change**: Specify what automated checks would verify parameter pinning, shape determinism, and plain-language pairing.
   - **Rationale**: Criterion 1 requires identification of the mechanical verification path for any passing determination.
   - **Risk if ignored**: Incomplete application of constitutional standards undermines the audit's thoroughness.

5. **Assess relative risks of retention vs. migration** (Priority: P2)
   - **Current state**: Section 5.2 identifies migration risks but not retention risks for failing principles (L126-133).
   - **Proposed change**: Add analysis of constitutional integrity costs from retaining principles that fail the gate.
   - **Rationale**: Complete risk assessment requires evaluating both sides of the migration decision.
   - **Risk if ignored**: Incomplete decision framework may bias toward status quo regardless of constitutional compliance.

6. **Define "concrete enough" standard** (Priority: P3)
   - **Current state**: The spec applies an unstated standard for mechanization sketch adequacy.
   - **Proposed change**: Explicitly state what makes a mechanical verification sketch "concrete enough" per the constitutional gate.
   - **Rationale**: Transparent evaluation criteria improve audit reproducibility and reduce apparent arbitrariness.
   - **Risk if ignored**: Verdicts may appear inconsistent or overly demanding.

7. **Examine composition alternatives for distinctness analysis** (Priority: P3)
   - **Current state**: Criterion 3 analysis focuses on whether existing principles cover the same ground without examining composition possibilities (L61-62, L81-82, L104-105).
   - **Proposed change**: For each principle, assess whether its concerns could be addressed by combining existing principles.
   - **Rationale**: Criterion 3 explicitly rejects concerns "addressable by composing existing principles."
   - **Risk if ignored**: Incomplete distinctness analysis may miss legitimate composition alternatives.

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/CONSTITUTION.md` — sections cited: L1078-1099 (Constitutional Inclusion Criteria), L1115-1119 (grandfathering provision)