# Principle XXVIII Fit Audit — v4.2.0 v3 Structured Deliberation Outputs

## Executive Summary

v4.2.0 v3 implements JSON Schema-based structured deliberation outputs as the first concrete application of Tier 2 Principle XXVIII (Persistence Contract Discipline) to conversus-oss. The spec correctly addresses all five XXVIII sub-clauses within its declared scope (six deliberation output types) and successfully applies the fifteen D-conditions from the original self-consistency review. The implementation demonstrates mechanical CI enforcement, bidirectional validation, proper fixture coverage, and complete consumer contract documentation. However, this represents partial XXVIII compliance—deliberation outputs only—rather than universal coverage of all conversus-oss persistent state surfaces. **The D-condition fixes are correctly implemented, and v3 satisfies XXVIII requirements for its declared scope without introducing new constitutional gaps.**

## Alignment

- **Schema location declaration** (§ 4.0, § 6.1): Correctly implements D9 by declaring canonical location `engine/schema/v1/*.schema.json` in CONFORMANCE.md and linking from both README.md and CLAUDE.md, satisfying sub-clause 1's discoverable location requirements. [CONSTITUTION.md, L505-510]

- **Bidirectional drift detection** (§ 5.4): Implements D12 with CI jobs that validate both forward conformance (artifacts→schema) and backward compatibility (schema changes→existing artifacts), meeting sub-clause 2's bidirectional enforcement mandate. [CONSTITUTION.md, L538-545]

- **Consumer contract specification** (§ 7.1): Implements D11 with six required sections in CONSUMER-CONTRACT.md, including explicit stability guarantees and display-text surface declarations, satisfying sub-clauses 4 and 5. [CONSTITUTION.md, L572-577]

- **Fixture coverage expansion** (§ 5.3): Implements D14 by specifying four fixture types (conformant, missing-required, wrong-type, enum-violation) that exceed sub-clause 2's minimum of three fixtures and cover field presence, types, and value constraints. [CONSTITUTION.md, L538-545]

- **Schema versioning discipline** (§ 4.8): Uses semantic versioning with documented MAJOR/MINOR/PATCH bump rules and consumer-impact qualification, satisfying sub-clause 3's versioning requirements. [CONSTITUTION.md, L555-560]

## Missed Opportunities

- **Universal scope clarification**: The spec explicitly scopes to deliberation outputs only (§ 3 non-goals) but doesn't clarify how remaining conversus-oss persistent state (engine state, provider tokens, evaluation results) will achieve XXVIII compliance by the 2026-12-01 deadline. **Impact: medium** - leaves XXVIII remediation incomplete.

- **Cross-suite applicability modeling**: While § 9.3 documents forward-promotion pathway to Tier 2, the spec doesn't model how other conversus-family repos would adapt the JSON Schema approach for their own deliberation-like artifacts. **Impact: low** - limits reusability of the infrastructure investment.

- **Enforcement timeline integration**: The spec shows CI gates and validation but doesn't explicitly map these to the universal remediation deadline enforcement mechanism described in XXVIII's "Remediation-Blocked" escalation procedure. **Impact: medium** - potential gap in deadline compliance verification.

- **Schema evolution testing**: While § 5.4 shows schema-version-bump detection, the spec doesn't mandate testing actual schema evolution scenarios (MINOR additions, MAJOR breaking changes) against the consumer contract stability guarantees. **Impact: low** - theoretical validation only.

## Off-Base Assumptions

- **Partial implementation sufficiency**: The spec assumes that implementing XXVIII for deliberation outputs constitutes sufficient progress toward the 2026-12-01 deadline, but XXVIII sub-clause 1 states "Every stateful artifact" must comply. The assumption of incremental implementation is reasonable but doesn't address timeline pressure. [CONSTITUTION.md, L490-494]

- **CI gate enforcement equivalence**: v3 § 5.1 treats PR-blocking CI gates as constitutionally equivalent to runtime validation for enforcement purposes, but this assumes CI coverage equals production enforcement - a gap that could occur if artifacts are written outside the CI-gated development flow. [CONSTITUTION.md, L538-545]

## Actionable Recommendations

1. **Clarify XXVIII compliance scope** (Priority: P2)
   - **Current state**: § 3 non-goals lists exclusions without timeline for XXVIII compliance completion.
   - **Proposed change**: Add § 1.3 "XXVIII Compliance Strategy" stating this spec covers deliberation outputs with follow-up specs for remaining persistent state before 2026-12-01.
   - **Rationale**: XXVIII requires universal coverage; partial implementation needs explicit remediation path. [CONSTITUTION.md, L594-602]
   - **Risk if ignored**: Missed deadline triggers "Remediation-Blocked" status per XXVIII enforcement mechanism.

2. **Verify bidirectional CI implementation** (Priority: P1) 
   - **Current state**: § 5.4 describes drift-detection job conceptually but lacks implementation verification.
   - **Proposed change**: Add § 5.4.1 "Bidirectional Validation Verification" requiring CI job to demonstrate both directions work on committed test cases.
   - **Rationale**: Sub-clause 2 mandates bidirectional enforcement; description without verification doesn't satisfy mechanical requirement. [CONSTITUTION.md, L538-545]
   - **Risk if ignored**: CI gate could fail to catch schema evolution breaking existing artifacts, violating core XXVIII enforcement contract.

3. **Strengthen consumer contract stability guarantees** (Priority: P2)
   - **Current state**: § 7.1 section 2 lists stability guarantees but doesn't specify testing mechanism.
   - **Proposed change**: Require consumer-side CI in orchestrator that validates against versioned fixture set from conversus-oss.
   - **Rationale**: Sub-clause 4 requires consumer-coordinated migration; producer-only testing insufficient. [CONSTITUTION.md, L572-577]
   - **Risk if ignored**: Consumer contract drift could occur silently despite producer-side schema validation passing.

4. **Document schema evolution procedures** (Priority: P3)
   - **Current state**: § 4.8 defines SemVer bump rules but doesn't specify operational procedures for executing bumps.
   - **Proposed change**: Add § 4.8.1 "Schema Evolution Workflow" with step-by-step procedure for MAJOR/MINOR/PATCH changes.
   - **Rationale**: Sub-clause 3 requires documented bump procedure; classification rules alone insufficient for execution. [CONSTITUTION.md, L555-560]
   - **Risk if ignored**: Schema evolution could be inconsistently applied, violating consumer expectations.

5. **Verify D15 implementation completeness** (Priority: P1)
   - **Current state**: § 5.4 mentions schema-version-bump detection but doesn't specify detection logic.
   - **Proposed change**: Define exactly what constitutes "schema edited without version bump" - file timestamps, content hashes, or semantic analysis.
   - **Rationale**: D15 addresses "silent format changes are a violation" from sub-clause 3; vague detection undermines enforcement. [CONSTITUTION.md, L555-560]
   - **Risk if ignored**: Silent schema changes could violate XXVIII without CI detection, compromising consumer contract reliability.

6. **Cross-reference constitutional deadline enforcement** (Priority: P2)
   - **Current state**: Spec doesn't connect to XXVIII's "Remediation-Blocked" escalation mechanism.
   - **Proposed change**: Add § 6.3 "Deadline Compliance Verification" referencing XXVIII enforcement procedure and how this spec's delivery relates to conversus-oss compliance status.
   - **Rationale**: XXVIII includes specific enforcement mechanism that this implementation should explicitly satisfy. [CONSTITUTION.md, L594-616]
   - **Risk if ignored**: Unclear whether spec delivery constitutes sufficient XXVIII remediation progress.

7. **Validate fixture coverage completeness** (Priority: P2)
   - **Current state**: § 5.3 lists four fixture types but doesn't verify coverage of all error_code enum values from § 4.9.
   - **Proposed change**: Require fixture coverage to exercise every error_code in validator-error schema, not just structural categories.
   - **Rationale**: Sub-clause 2 requires validation of field presence, types, and value constraints; incomplete error path coverage undermines mechanical enforcement. [CONSTITUTION.md, L538-545]
   - **Risk if ignored**: Validator error paths could remain untested despite passing CI, reducing actual enforcement reliability.

## Referenced Documentation

- `build-fractal-mono/build-fractal/conversus/CONSTITUTION.md` — sections/lines cited: L490-494 (preamble), L505-510 (sub-clause 1), L538-545 (sub-clause 2), L555-560 (sub-clause 3), L572-577 (sub-clauses 4-5), L594-602, L594-616 (deadline enforcement)
- `specs/v4.2.0-structured-deliberation-outputs/spec.md` — sections cited: § 1, § 3, § 4.0, § 4.8, § 4.9, § 5.1, § 5.3, § 5.4, § 6.1, § 7.1, § 9.3
- `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-rerun-2026-05-13/QUESTION.md` — D-conditions D9-D15 verification requirements