# APM Cross-Review of Spec-Kit's v2 Review

**Cross-reviewer**: APM
**Reviewing**: spec-kit v2 review (`conversus-v2/spec-kit/review.md`)
**Against**: APM v2 review (`conversus-v2/apm/review.md`)
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1. Structured output schema: normative FR vs. forward-compatible prose convention

Spec-kit recommends elevating the deferred schema fields into a normative FR (proposed FR-028) that constrains future versions to implement those specific fields (P2 rec #4). APM recommends the opposite leverage point: define internal structure conventions for Binding Decisions prose entries now (P1 rec #3) so that the deferred extraction mechanism has a reliable parsing target. These are not complementary -- they pull in opposite directions. Spec-kit's approach locks the *output schema* normatively while leaving the *prose structure* free-form. APM's approach locks the *prose structure* while leaving the *output schema* advisory. If both are adopted simultaneously, the normative schema fields (dispute_id, ruling_type, etc.) would be committed as requirements, but the prose entries that produce them would also be structurally constrained -- creating a double-binding where a future implementor must satisfy both the field contract and the prose convention, with no guarantee the two remain aligned as the spec evolves. One must be primary. The spec should choose whether the schema or the prose structure is the normative commitment, and make the other derived.

### DC-2. `affected_target_file` cardinality: singular field vs. implicit FR-026 semantics

Spec-kit flags that the deferred schema's `affected_target_file` is singular and should be pluralized to `affected_target_files` (Off-Base #1) because a single dispute may affect multiple files. APM flags the adjacent but conflicting problem: FR-026 requires per-file attribution in binding decisions but the template authoring contract does not enforce it (Missed Opportunity #3). These two observations, taken together, expose a design contradiction. If `affected_target_files` becomes a list (spec-kit's fix), the schema implies one ruling maps to many files. If the template contract enforces per-file attribution (APM's fix), the prose implies each binding decision specifies exactly which file it targets -- pushing toward one ruling per file, or at least one explicit file per change line. The schema pluralization and the attribution enforcement model different cardinalities. Adopting both without reconciliation would produce a schema that says "a ruling touches N files" alongside prose that says "each change is attributed to a specific file," with no defined mapping between the two.

### DC-3. Template authoring contract scope: cooperative-only vs. mode-universal with missing invariants

Spec-kit recommends scoping the template authoring contract explicitly to cooperative mode (P2 rec #6), noting that non-cooperative modes produce fundamentally different Phase 5 outputs. APM recommends adding per-file attribution and Phase 5 output cross-references to the *existing* contract (P1 rec #2, P2 rec #6) without scoping it to cooperative mode -- treating the contract as the universal contract that needs to be complete. If spec-kit's scoping is adopted first, APM's additions become cooperative-mode-specific invariants, and non-cooperative modes get no contract at all. If APM's additions are adopted first, the contract grows but remains implicitly universal, and spec-kit's later scoping would need to decide which invariants are truly cooperative-only and which are mode-universal. The danger is sequencing: whichever recommendation lands first constrains how the other can be integrated, and neither review acknowledges the dependency.

### DC-4. Content-presence validation: trigger-level guard vs. no equivalent APM concern

Spec-kit identifies a gap where structural markers could be present but contain only whitespace, causing Phase 6 to fire with an empty `{REMAINING_DISPUTES}` variable (Missed Opportunity #2, P1 rec #3). Spec-kit recommends the trigger should evaluate to `false` when markers contain only whitespace. APM does not flag this gap and instead focuses on the opposite edge: `trigger: always` firing with zero disputes, which is a legitimate use case (US1-AS3 subject endorsement). These two positions become dangerous when combined. Spec-kit's whitespace guard would make empty-marker content a "no disputes" signal at the trigger level. But APM's `trigger: always` discussion (Missed Opportunity #5, noting the enum extensibility problem) implicitly assumes the trigger fires regardless of content. If the whitespace guard is adopted for `trigger: disputes_remain` but not documented as inapplicable to `trigger: always`, an implementor could apply it universally, blocking the subject-endorsement use case where `trigger: always` fires with legitimately empty dispute content.

---

## Tensions

### T-1. Severity of SKILL.md drift: correctness defect vs. consistency fix

Both reviews flag the SKILL.md trigger evaluation drift as P1. However, they frame the severity differently. APM calls it a defect that "will produce incorrect behavior" -- an implementor following SKILL.md builds the wrong logic. Spec-kit calls it "a spec-implementation consistency fix, not a design change" -- the spec already prescribes the correct behavior and the implementation guidance lags behind. The practical difference: APM's framing implies SKILL.md is a normative implementation document whose incorrectness is a blocking defect. Spec-kit's framing implies SKILL.md is derivative documentation that should be synced but whose current state does not invalidate the spec. This tension reflects a deeper disagreement about SKILL.md's authority level that neither review makes explicit.

### T-2. Observation carve-out completeness: adequate vs. incomplete audit trail

APM considers FR-015.5 a faithful reconciliation of the three v1 positions (Alignment #6). Spec-kit considers FR-015.5 positionally adequate but lacking rationale documentation (Missed Opportunity #4) -- it does not record why the structural + labeling model was chosen over the structural-only (APM) or no-formalization (gh-aw) alternatives. The tension: APM treats the chosen position as self-evidently correct (it implements APM's structural constraint as the minimum enforceable rule). Spec-kit treats the choice as one of several defensible options whose selection requires documented justification. For a spec produced by a formal deliberation process, spec-kit's audit-trail expectation is harder to dismiss, but APM's "correct is correct" stance has the pragmatic advantage of not reopening a resolved dispute.

### T-3. Structured output deferral: acceptable for v1 vs. normative downgrade

Both reviews agree the structured output schema is deferred. They disagree on whether the deferral is a problem. APM treats it as "acceptable for v1" (Missed Opportunity #2) and focuses on making the deferred mechanism viable via prose structure conventions. Spec-kit treats it as a normative downgrade from the synthesis recommendation (Missed Opportunity #1): the synthesis wanted normative schema fields in the Requirements section, the spec put them in non-normative Implementation Guidance. Spec-kit is right that there is a material difference between normative and advisory schema fields; APM is right that the mechanism viability matters more than the normative status of the field list. Neither review acknowledges the other's valid concern.

### T-4. Success criteria gap: explicit new SCs vs. no mention

Spec-kit identifies that the 10 new functional requirements (FR-022 through FR-027 and modifications) have no corresponding success criteria, and recommends adding at minimum 4 new SC entries (P1 rec #2). APM does not flag the success criteria gap at all. This is not a contradiction -- APM may consider success criteria a documentation completeness issue rather than a correctness issue -- but the asymmetry is notable. If the spec is consumed by spec-kit's SDD pipeline, missing SCs are a structural defect because the pipeline uses SCs for acceptance verification. If the spec is consumed by APM's packaging and distribution model, SCs may be less load-bearing. The tension is about whose consumption model sets the completeness bar.

### T-5. Grounding document stability: aspirational vs. verifiable

APM flags that the grounding document stability assumption has no verification mechanism and recommends a lightweight hash-check mitigation (Off-Base #1). Spec-kit does not flag this at all -- it treats the stability assumption as correctly integrated (Alignment #1 notes "grounding document stability (Assumptions)" as a convergence point faithfully integrated). The tension: APM sees an assumption without enforcement as an implicit guarantee the system cannot provide. Spec-kit sees the same assumption as a correctly stated precondition that the spec is not obligated to enforce. This reflects different philosophies about where assumptions end and requirements begin.

---

## Safe Agreements

### SA-1. SKILL.md trigger evaluation must be updated

Both reviews independently identify the SKILL.md trigger evaluation drift as a P1 issue requiring immediate correction. Both describe the same problem (SKILL.md describes only heading-based parsing, not the structural HTML markers FR-011 mandates as primary). Both recommend the same fix (update SKILL.md to match the marker-primary, heading-fallback hierarchy). Both cite the same root cause (the spec was updated but SKILL.md was not). This is the strongest convergence point between the two reviews -- identical problem, identical severity, identical fix.

### SA-2. The docs-vs-grounding distinction is well-calibrated

Both reviews explicitly commend FR-024's formulation. APM calls the "sole basis" qualifier "precisely calibrated" (Alignment #2). Spec-kit calls it "a well-calibrated integration" and "the exact formalization spec-kit requested" (Alignment #3). Both note that the phrasing permits contextual references to docs without opening citation-laundering or undermining grounding singularity. This is the clearest example of a synthesis recommendation that both consumers consider correctly implemented.

### SA-3. Non-cooperative template gating resolves Dispute 2 correctly

Both reviews agree that the Constraints section's treatment of non-cooperative templates (draft/experimental, not activatable in v1, marker-based status, engine-level filtering) correctly resolves the substance of Dispute 2. APM notes it "resolves the substance ... while acknowledging the file-placement disagreement as an implementation detail" (Alignment #5). Spec-kit notes it "adopts spec-kit's in-place-with-markers position while incorporating gh-aw's concern about automated discovery" (Alignment #4). Both consider the marker approach over filesystem relocation to be the right trade-off.

### SA-4. Failure semantics faithfully implement the synthesis

Both reviews confirm FR-022 correctly implements the unanimous convergence on Phase 6 failure handling: Phase 5 as terminal state, diagnostic warning, no partial output, Phase 1-5 record preserved. APM calls it "faithful to the synthesis" (Alignment #3). Spec-kit calls it matching "the unanimous convergence point exactly" and praises the FR-022/FR-023 separation as a nuance "the synthesis implied but did not explicitly separate" (Alignment #5). No disagreement on correctness, completeness, or framing.

---

## Summary

The two reviews are substantially aligned on what the spec gets right (6 alignment points overlap almost perfectly) and on the highest-priority fix (SKILL.md drift). The dangerous contradictions cluster around the structured output design space: the reviews pull in opposite directions on whether to normatively lock the schema fields or the prose structure, and on whether file attribution should be singular or plural. The template authoring contract receives conflicting expansion recommendations (scope it narrower vs. add more invariants) that cannot both be adopted without explicit reconciliation. The content-presence guard interacts unsafely with the `trigger: always` use case. The tensions reflect deeper philosophical differences -- SKILL.md's authority level, the completeness bar for success criteria, whether assumptions require enforcement mechanisms -- that are worth surfacing but do not require resolution for v1 implementation to proceed.
