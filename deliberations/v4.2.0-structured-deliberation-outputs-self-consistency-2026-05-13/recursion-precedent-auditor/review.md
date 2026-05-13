# Review: v4.2.0 Structured Deliberation Outputs — Recursion Precedent Audit

## Executive Summary

Spec v4.2.0 implements Tier 2 Principle XXVIII (Persistence Contract Discipline) by mandating JSON Schema for deliberation outputs while exempting itself from this requirement via RECURSION-EXEMPTED status. This creates a methodological bootstrap paradox: the spec that establishes schema discipline cannot itself use that discipline without creating circular dependency. However, the exemption's framing and scope present significant precedent risks that mirror the v4.1.0 override-with-rationale pattern that self-consistency arbitration `8f90e2d` explicitly rejected. The exemption violates the cross-tier weakening prohibition through implicit relief and creates an exploitable precedent for future schema-related amendments.

**Most important recommendation:** Reframe RECURSION-EXEMPTED as a temporal constraint rather than a procedural exemption to prevent precedent abuse.

## Alignment

- **Principle II retroactive-obligation grounding** (spec § 9.1): The exemption correctly identifies that Principle II forbids mid-flight interface changes, providing doctrinal anchor for the methodological fixed-point logic.

- **Post-ratification governance review commitment** (spec § 9.1): The spec appropriately flags the recursion question for future governance review rather than establishing permanent precedent.

- **Cross-tier weakening awareness** (QUESTION.md L47): The framing question correctly identifies the v4.1.0 self-consistency precedent as the relevant comparison point for evaluating exemption legitimacy.

- **Temporal scope boundary** (spec § 11 tiered rollout): The exemption is temporally bounded by the 2026-12-01 cliff, preventing indefinite exemption claims.

## Missed Opportunities

- **Explicit precedent-scope limitation**: The exemption fails to include explicit anti-precedent language preventing future amendments from citing RECURSION-EXEMPTED as justification. Reference: v4.1.0 precedent scope language was established to prevent exactly this abuse pattern. **Impact: high**.

- **Formal Relief pathway consideration**: The exemption bypasses COMPLIANCE.md Part VI formal Relief mechanisms without justification for why those procedures are inadequate. Reference: Tier 2 CONSTITUTION.md L653 cross-tier weakening prohibition criterion (i). **Impact: high**.

- **Cross-amendment citation prevention**: No mechanism prevents future schema-related amendments from claiming similar "meta-schema" exemptions. The precedent scope is uncontained. **Impact: high**.

- **Override-with-rationale pattern analysis**: The exemption lacks explicit analysis of why it differs from the v4.1.0 pattern that was constitutionally rejected. **Impact: medium**.

- **Implementation-impact audit**: No verification that existing implementations remain XXVIII-compliant under the exemption interpretation. Reference: Tier 2 CONSTITUTION.md L655 cross-tier weakening prohibition criterion (ii). **Impact: medium**.

- **Governance review timeline**: The post-ratification review commitment lacks binding timeline, allowing indefinite deferral of the precedent question. **Impact: low**.

## Off-Base Assumptions

- **Assumption stated** (spec § 9.1): "This is consistent with Tier 1 Principle II (stable interfaces): asking the verification methodology to migrate its substrate mid-deliberation is exactly the kind of mid-flight interface change Principle II forbids."

  **Why it is wrong**: Principle II governs interface stability, not procedural methodology. The verification methodology is not a "stable interface" in Principle II's technical sense - it is operational procedure. Principle II applies to dispatch table subcommands, template variables, and reference file paths, not to verification output formats.

- **Assumption stated** (spec § 13): "The verification trail for v4.2.0 itself stays markdown — a fixed point in the migration."

  **Why it is wrong**: "Fixed point" implies mathematical/logical necessity, but this is actually a procedural accommodation. The true fixed point would be temporal ordering: v4.2.0 cannot use JSON because JSON validation doesn't exist until v4.2.0 creates it. The fixed-point framing obscures the temporal constraint.

## Actionable Recommendations

1. **Reframe exemption as temporal constraint** (Priority: P1)
   - **Current state**: "RECURSION-EXEMPTED per Q3" language frames this as procedural exemption.
   - **Proposed change**: Replace with "TEMPORAL-ORDERING-CONSTRAINT: v4.2.0 verification outputs predate JSON schema availability by construction; JSON mandatory for specs ratified after v4.2.0 implementation completion."
   - **Rationale**: Temporal framing prevents precedent abuse by grounding the exemption in unrepeatable historical sequencing rather than exemptible procedure.
   - **Risk if ignored**: Future amendments claim "meta-schema" exemptions citing RECURSION-EXEMPTED precedent.

2. **Add explicit anti-precedent language** (Priority: P1)
   - **Current state**: § 9.1 and § 13 lack precedent-scope limitation.
   - **Proposed change**: Add to § 9.1: "This temporal constraint does NOT establish precedent for procedural exemptions from constitutional principles. Future amendments to schema-related specs remain bound by standard enforcement mechanisms."
   - **Rationale**: Prevents citation abuse; mirrors v4.1.0 precedent-scope limitation pattern established after override-with-rationale rejection.
   - **Risk if ignored**: Slippery precedent enables constitutional erosion via exemption proliferation.

3. **Remove Principle II misattribution** (Priority: P1)
   - **Current state**: § 9.1 cites Principle II as doctrinal support for exemption.
   - **Proposed change**: Replace Principle II citation with temporal-ordering rationale: "v4.2.0 verification outputs must predate the JSON validation infrastructure they specify by construction."
   - **Rationale**: Principle II governs interface stability, not procedural methodology; misattribution weakens both principles.
   - **Risk if ignored**: Principle II scope-creep enables future procedural exemptions under false doctrinal cover.

4. **Cross-tier weakening impact assessment** (Priority: P2)
   - **Current state**: No analysis of whether exemption violates Tier 2 CONSTITUTION.md L651-664 cross-tier weakening prohibition.
   - **Proposed change**: Add § 9.2 assessing exemption against criteria (i), (ii), (iii) with explicit finding that temporal constraint satisfies prohibition requirements.
   - **Rationale**: Constitutional compliance requires explicit verification against cross-tier weakening criteria.
   - **Risk if ignored**: Exemption challenged post-ratification on cross-tier weakening grounds.

5. **Binding governance review timeline** (Priority: P2)
   - **Current state**: § 9.1 commits to "post-ratification governance review" without timeline.
   - **Proposed change**: "Post-ratification governance review MUST be initiated within 90 days of v4.2.0 implementation completion (§ 11 step 6) to evaluate recursion patterns for future schema amendments."
   - **Rationale**: Binding timeline prevents indefinite deferral of precedent question.
   - **Risk if ignored**: Precedent question remains unresolved, enabling future abuse through procedural uncertainty.

6. **Future-extension constraint language** (Priority: P2)
   - **Current state**: No mechanism prevents future "meta-schema" exemption claims.
   - **Proposed change**: Add to § 13: "Future schema-related amendments creating new validation infrastructure are NOT exempt from using existing validation infrastructure. Each amendment must use the best available validation at time of specification."
   - **Rationale**: Prevents exemption proliferation by establishing "use best available" standard.
   - **Risk if ignored**: Each new schema amendment claims exemption from predecessor schemas.

7. **Override-with-rationale differentiation analysis** (Priority: P3)
   - **Current state**: No explicit comparison to v4.1.0 rejected precedent.
   - **Proposed change**: Add footnote in § 9.1 distinguishing temporal constraint from procedural override: "Unlike v4.1.0's override-with-rationale (procedural bypass), this constraint derives from unrepeatable temporal ordering."
   - **Rationale**: Explicit differentiation prevents constitutional conflation of temporal and procedural exemptions.
   - **Risk if ignored**: Future amendments conflate temporal constraints with procedural overrides.

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/conversus-oss/specs/v4.2.0-structured-deliberation-outputs/spec.md` — sections cited: L623-626 (§ 9.1), L705-711 (§ 13)
- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/CONSTITUTION.md` — sections cited: L490-644 (Principle XXVIII), L651-664 (cross-tier weakening prohibition)
- `/Users/business-daddy/code/payer-index-mono/build-fractal/CONSTITUTION.md` — sections cited: L84-114 (Principle II)
- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/conversus-oss/deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-2026-05-13/QUESTION.md` — sections cited: L47-48 (override-with-rationale precedent reference)