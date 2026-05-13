Looking at spec v2 as the principle-xxviii-fit-auditor, I need to systematically verify whether v2 correctly implements each sub-clause of Tier 2 Principle XXVIII. My default posture is to defend the status quo - XXVIII is ratified constitutional doctrine; v2 is the candidate implementation.

### Executive Summary

Spec v2 attempts to implement Principle XXVIII's persistent state schema discipline for conversus-oss deliberation outputs. The spec addresses the core mandate by transitioning from markdown display-text contracts to JSON Schema-enforced structural contracts. However, v2 contains three implementation gaps that prevent full XXVIII compliance: incomplete discoverable-location documentation, missing bidirectional validation enforcement, and underspecified CONSUMER-CONTRACT.md content. Additionally, v2 oversatisfies XXVIII by mandating performance requirements and rollout procedures beyond constitutional scope. My most important recommendation is to close the discoverable-location gap by documenting the schema directory in CONFORMANCE.md.

### Alignment

- **JSON Schema as mechanical enforcement** (`L526-527`): v2 correctly selects Python `jsonschema` library as a machine-executable validator that produces binary pass/fail with specific failure descriptions, satisfying sub-clause 2's mechanical enforcement requirement. [CONSTITUTION.md, L527-531]

- **SemVer versioning with consumer-impact rules** (`L463-469`): v2's § 4.8 implements sub-clause 3's versioning mandate with proper SemVer semantics, including the consumer-impact qualification that field renames are MAJOR even when technically additive. [CONSTITUTION.md, L547-553]

- **Required three-fixture CI enforcement** (`L542-547`): v2's § 5.3 mandates exactly the three fixture types required by XXVIII sub-clause 2: conformant, missing required field, and wrong field type, with CI validation. [CONSTITUTION.md, L538-545]

- **Cross-product consumer enforcement** (`L580`): v2's § 6.2 correctly implements sub-clause 4 by requiring orchestrator CI to validate against vendored conversus-oss fixture sets, satisfying consumer-side enforcement. [CONSTITUTION.md, L563-568]

### Missed Opportunities

- **Bidirectional validation coverage** (`L534-535`): v2 mentions "Advanced validations beyond write-time scope" but doesn't explicitly mandate the bidirectional validation required by sub-clause 2 - that schema changes trigger CI verification of existing producer code conformance. Impact: high.

- **CONFORMANCE.md schema directory documentation**: v2 places schemas under `engine/schema/v1/` but doesn't document this as a suite-convention directory in CONFORMANCE.md, potentially violating sub-clause 1's discoverable-location requirement. [CONSTITUTION.md, L503-508]. Impact: medium.

- **CONSUMER-CONTRACT.md content specification** (`L571`): v2 mandates creating CONSUMER-CONTRACT.md but doesn't specify whether it will contain the explicit surface declarations required by sub-clause 5. Impact: high.

- **Schema evolution automation**: v2 could strengthen sub-clause 3 compliance by mandating automated schema version bumps on schema file changes, preventing silent format changes. [CONSTITUTION.md, L552-553]. Impact: low.

- **Display-text migration tracking**: v2 could document remaining display-text surfaces during the markdown-to-JSON migration to ensure sub-clause 5 compliance is maintained throughout the transition. Impact: medium.

- **Envelope schema completeness verification**: v2 could mandate CI validation that the envelope schema's discriminator pattern correctly references all per-type body schemas, preventing schema drift. Impact: medium.

### Off-Base Assumptions

- **Performance budget constitutional scope** (`L532`): v2 assumes XXVIII mandates <100ms validation performance, but sub-clause 2 only requires "machine-executable" validation without performance constraints. The constitutional principle doesn't establish performance as a compliance criterion.

- **Tiered rollout constitutionally required** (`L664-669`): v2 treats the four-tier implementation rollout as a constitutional mandate, but XXVIII only requires the end state of mechanical enforcement, not the migration path to achieve it.

### Actionable Recommendations

1. **Document schema directory location** (Priority: P1)
   - **Current state**: v2 places schemas at `engine/schema/v1/` without documenting this in CONFORMANCE.md (`L563`)
   - **Proposed change**: Add requirement that § 6.1 file edits include updating conversus-oss CONFORMANCE.md to declare `engine/schema/v1/` as a suite-convention directory per sub-clause 1
   - **Rationale**: Sub-clause 1 requires discoverable locations to be "documented in the repo's `CONFORMANCE.md`" [CONSTITUTION.md, L505-506]
   - **Risk if ignored**: Sub-clause 1 violation - schemas not in discoverable location

2. **Mandate bidirectional validation enforcement** (Priority: P1)
   - **Current state**: v2 mentions bidirectional validation as "Advanced validations beyond write-time scope" (`L534`)
   - **Proposed change**: Move bidirectional validation to required CI gate - schema changes must trigger validation that existing producer code still emits conformant artifacts
   - **Rationale**: Sub-clause 2 explicitly requires "any change to the schema itself MUST trigger CI verification" [CONSTITUTION.md, L535-537]
   - **Risk if ignored**: Sub-clause 2 violation - schema drift undetected

3. **Specify CONSUMER-CONTRACT.md content requirements** (Priority: P1)
   - **Current state**: v2 mandates creating CONSUMER-CONTRACT.md but doesn't specify content (`L571`)
   - **Proposed change**: Specify that CONSUMER-CONTRACT.md must explicitly declare JSON Schema surfaces with stability guarantees per sub-clause 5
   - **Rationale**: Sub-clause 5 requires explicit declaration "naming the specific display-text surface... and stating the stability guarantee" [CONSTITUTION.md, L572-577]
   - **Risk if ignored**: Sub-clause 5 violation - surfaces undeclared

4. **Remove constitutional performance claims** (Priority: P2)
   - **Current state**: v2 presents <100ms budget as implementing XXVIII C2 (`L532`)
   - **Proposed change**: Frame performance budget as implementation choice, not constitutional requirement
   - **Rationale**: XXVIII sub-clause 2 requires "machine-executable" validation without performance constraints [CONSTITUTION.md, L527-531]
   - **Risk if ignored**: Constitutional overreach - mandating requirements beyond XXVIII scope

5. **Clarify README.md + CLAUDE.md linking requirement** (Priority: P2)
   - **Current state**: v2 mentions linking from both files but doesn't specify the exact linking requirement (`L573-574`)
   - **Proposed change**: Explicitly state that both files must link to CONSUMER-CONTRACT.md as required by sub-clause 1
   - **Rationale**: Sub-clause 1 requires links from "BOTH the repo's top-level `README.md` AND its `CLAUDE.md`" [CONSTITUTION.md, L508-510]
   - **Risk if ignored**: Sub-clause 1 partial satisfaction

6. **Document fixture validation scope** (Priority: P3)
   - **Current state**: v2 specifies three fixtures but doesn't detail their validation coverage
   - **Proposed change**: Specify that fixtures must cover all schema constraints (field presence, types, value constraints, enum violations)
   - **Rationale**: Sub-clause 2 requires fixtures that validate "field presence, types, and value constraints" [CONSTITUTION.md, L530-531]
   - **Risk if ignored**: Incomplete sub-clause 2 implementation

7. **Strengthen schema evolution enforcement** (Priority: P3)
   - **Current state**: v2 documents bump procedure but doesn't enforce version changes
   - **Proposed change**: Mandate CI detection of schema changes without version bumps
   - **Rationale**: Sub-clause 3 states "Schema evolution MUST update the version; silent format changes are a violation" [CONSTITUTION.md, L552-553]
   - **Risk if ignored**: Sub-clause 3 enforcement gap

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/CONSTITUTION.md` — sections cited: L490-644 (full Principle XXVIII text), L503-508 (discoverable location), L527-531 (mechanical enforcement), L535-537 (bidirectional validation), L547-553 (versioning), L563-568 (consumer enforcement), L572-577 (declaration scope)