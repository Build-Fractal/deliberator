# gh-aw Cross-Review of APM's v2 Review

**Cross-reviewer**: gh-aw
**Reviewing**: APM v2 review (`conversus-v2/apm/review.md`)
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1. APM treats output validation (FR-023) as settled; gh-aw identifies an unresolved conflict with failure semantics (FR-022)

APM's Alignment section 4 states that FR-023 "strikes the right balance between strictness and pragmatism" and treats the write-with-warning behavior as fully resolved. gh-aw's Missed Opportunity 3 identifies a direct conflict: FR-022 says malformed output means no `resolution.md` is written, while FR-023 says failed validation means the file IS written with a warning. APM's recommendation P1-3 (internal structure convention for Binding Decisions) assumes the file always lands and focuses on making it parseable. If FR-022 is interpreted broadly -- "malformed output" includes structurally incomplete prose -- then the file may never be written in the first place, and APM's extractability concern becomes moot. These two reviews cannot both be correct: either the file is always written (APM's assumption) or there is an ambiguous state where it might not be (gh-aw's finding). Adopting APM's P1-3 without first resolving the FR-022/FR-023 disambiguation (gh-aw's P1-1) builds structure on an unstable foundation. The FR-022/FR-023 boundary must be settled before any recommendation that depends on the file being reliably present.

### DC-2. APM's forward-compatibility convention for Binding Decisions conflicts with the spec's deferred structured output strategy

APM's Missed Opportunity 2 and P1-3 recommend adding a lightweight structural convention now (`**Dispute:**`, `**Ruling:**`, `**Grounding:**` labeled fields) inside Binding Decisions entries so that a future extraction mechanism has a reliable parsing target. gh-aw's P3-8 recommends extracting the deferred structured output schema to a standalone section precisely because it is not yet normative. These positions pull in opposite directions: APM wants to bake proto-structured output into the prose template now; gh-aw treats the schema as explicitly deferred and wants it visibly separated from normative requirements. The danger is that APM's convention, once adopted, becomes a de facto schema that constrains the future structured output design. If the eventual extraction mechanism uses JSON or YAML (as the Implementation Guidance already sketches), the labeled-fields convention in prose would be redundant at best and a conflicting contract at worst. The spec deliberately deferred structured output to avoid premature commitment. Introducing a structural convention that serves only the deferred mechanism inverts that decision.

### DC-3. APM recommends SKILL.md sync as P1; gh-aw's trigger concerns reveal that syncing SKILL.md to the current spec would propagate an underspecified definition

APM's P1-1 is urgent and correct in identifying SKILL.md/spec drift on trigger evaluation. But gh-aw's P1-2 identifies that the spec's primary trigger mechanism itself is underspecified: "dispute entry" is not defined for the marker-based path. Syncing SKILL.md to FR-011 as currently written would replace a known-wrong implementation (heading-based only) with an ambiguously-specified one (marker-based with undefined "dispute entry"). The contradiction is operational: APM's fix, applied in isolation, would update SKILL.md to say "check whether at least one dispute entry exists between the markers" without defining what a dispute entry is -- the exact gap gh-aw flags. The correct sequence is to first define "dispute entry" for the primary mechanism (gh-aw's P1-2), then sync SKILL.md (APM's P1-1). Reversing this order bakes ambiguity into the executable skill definition.

---

## Tensions

### T-1. Template authoring contract scope: APM wants it expanded, gh-aw wants it enforced

APM's Missed Opportunity 3 and P1-2 flag that the template authoring contract is missing per-file attribution (FR-026) and should cross-reference Phase 5 output format. These are additive -- APM wants the contract to cover more ground. gh-aw's Alignment 5 accepts the current contract's four invariants as "the right set" and focuses instead on enforcement gaps: the `docs` vs `grounding` citation boundary (gh-aw P2-4) is not carried into template instructions, and the draft marker has no engine-level FR behind it (gh-aw P2-3). The tension is scope vs. enforcement. APM's additions make the contract more complete on paper; gh-aw's additions make the existing contract more enforceable at runtime. Both are valid, but pursuing both simultaneously risks bloating the contract with requirements that have no validation mechanism. The resolution path is to prioritize enforcement of existing invariants (gh-aw's concern) before expanding the invariant set (APM's concern).

### T-2. Grounding document integrity: APM wants verification, gh-aw accepts the stability assumption

APM's Off-Base Assumption 1 identifies that the grounding document stability assumption is unverifiable and recommends a hash-based verification mechanism (hash at config validation, compare at Phase 6 dispatch). gh-aw's review does not flag grounding document stability at all -- it accepts the stability note as sufficient and focuses instead on the grounding document's citation boundary enforcement (FR-024). This reflects a genuine difference in operational model: APM's packaging context envisions runs spanning distributed systems where concurrent edits are plausible; gh-aw's CI dispatch context assumes a committed, immutable workspace where files do not change mid-run. Neither assumption is universally correct. The tension matters because a hash-verification mechanism would add a new engine capability requirement (file hashing at two lifecycle points) that gh-aw's operational model does not need and would view as unnecessary complexity.

### T-3. "Binding" semantics: APM wants explicit non-enforcement language, gh-aw implicitly treats binding as pipeline-terminal

APM's Off-Base Assumption 2 recommends clarifying that "binding" refers to deliberation-record finality, not enforcement on downstream actors. gh-aw's review does not question the "binding" semantics and in fact relies on them operationally: gh-aw's concern about the `trigger: always` endorsement path (Off-Base Assumption 2) assumes the arbiter's output IS the terminal pipeline state -- whatever the arbiter produces under `trigger: always` is what downstream consumers receive. If APM's clarification is adopted ("binding does not imply enforcement on downstream actors"), it weakens the authority of the `trigger: always` endorsement that gh-aw's recommendation (P2-5) tries to formalize. The tension is philosophical: APM views the arbiter as a deliberation recorder; gh-aw views the arbiter as a pipeline authority whose output shapes downstream behavior.

### T-4. Draft template placement: residual disagreement masked by compromise

APM's Alignment 5 accepts the Constraints section compromise (templates exist in-place with draft markers, filtered at runtime) as "correctly specified." gh-aw's Off-Base Assumption 1 explicitly rejects this compromise as creating technical debt: "runtime filtering of templates by content inspection is a pattern that gh-aw's compilation model explicitly avoids." APM calls it resolved; gh-aw calls it a known-bad pattern tolerated only because FR-004 prevents activation. This is not a contradiction (both acknowledge the compromise works for v1) but the tension is real: APM will treat the marker pattern as established precedent for future template gating; gh-aw will push to replace it with directory-based separation. Any future spec that extends template status management will re-open this dispute.

### T-5. Trigger enum extensibility vs. endorsement path specification

APM's Missed Opportunity 5 and P2-5 recommend documenting the `trigger` field as an extensible enum with validation errors for unknown values. gh-aw's P2-5 recommends specifying what happens under `trigger: always` with no disputes -- the endorsement path. These are complementary on the surface but tension emerges at the design level: APM's extensible-enum framing implies `trigger: quorum` could arrive as a third enum value processed through the same dispatch logic. gh-aw's endorsement-path concern reveals that even the existing two-value enum does not fully specify its dispatch behavior. Extending the enum before the existing values are fully specified risks compounding the underspecification.

---

## Safe Agreements

### SA-1. SKILL.md is out of sync with the spec and must be updated

APM's P1-1 (sync SKILL.md trigger evaluation with FR-011) and gh-aw's P1-2 (define "dispute entry" for the primary mechanism) both identify the SKILL.md/spec drift as a correctness issue requiring immediate action. The two recommendations are complementary: gh-aw's defines what the spec should say, APM's ensures SKILL.md reflects it. Neither review disputes the other's finding. This is the highest-confidence agreement in the cross-review.

### SA-2. The failure semantics (FR-022) and output validation (FR-023) alignment points are mutually consistent

APM's Alignment 3 and gh-aw's Alignment 1 both affirm that FR-022's failure semantics are correctly specified. APM's Alignment 4 and gh-aw's Alignment 3 both affirm that FR-023's output validation approach is sound. The disagreement is only about the boundary between the two (gh-aw's DC concern above), not about either FR in isolation. Both reviews agree that: Phase 5 fallback on failure is correct, no partial files should be written on agent-level failure, and warnings-not-blocks for validation are the right severity level.

### SA-3. The `docs` vs. `grounding` citation distinction (FR-024) is correctly specified

APM's Alignment 2 calls the FR-024 formulation "precisely calibrated." gh-aw's Missed Opportunity 5 calls it "sound." Both reviews accept the substance of the distinction. gh-aw pushes further on enforcement (the template should carry explicit instructions), but neither review disputes the design. This is a case where both agents converge on the same assessment from different operational perspectives.

### SA-4. The template authoring contract is a valuable addition

APM's Alignment section implicitly accepts the contract by building recommendations on top of it (expanding it with FR-026, cross-referencing Phase 5 output). gh-aw's Alignment 5 explicitly calls it "a direct adoption of gh-aw's N-1 recommendation" and affirms the four invariants. Both reviews propose improvements (APM: add more invariants; gh-aw: enforce existing ones), but neither questions the contract's existence or its current content. The contract is the strongest consensus artifact from the synthesis.
