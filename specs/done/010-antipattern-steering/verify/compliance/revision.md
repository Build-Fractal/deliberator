# Compliance Revision: Spec 010 — Agent Antipattern Steering

**Reviewer**: compliance
**Revision iteration**: 1
**Date**: 2026-03-20
**Inputs**: Original compliance review, cross-reviews from integration and scope-boundary, compliance's own cross-reviews of integration and scope-boundary

---

### Recommendation Dispositions

#### Recommendation 1: Fix broken example path

- **Original position**: Change all occurrences of `specs/001-antipattern-steering/` to `specs/010-antipattern-steering/` in catalog.md and tasks.md.
- **Disposition**: Modified
- **Explanation**: Integration's cross-review (Tensions, "Broken path: scope of affected files") correctly identified that my original recommendation scoped the fix too narrowly. I listed catalog.md and tasks.md as the affected files but missed quickstart.md (L15, L47) and plan.md (L63), which integration traced. Scope-boundary's cross-review (Tensions, item 1) confirmed the broader propagation list and suggested treating plan.md and research.md as historical errata rather than mandatory fixes. I accept both corrections. The modified recommendation: fix catalog.md (runtime artifact agents actually read) and tasks.md (implementation record with validation checkpoints) as mandatory P1 changes. Additionally fix quickstart.md references, since it serves as onboarding documentation for future implementers. For plan.md and research.md, note the path discrepancy as known errata without requiring changes to design-phase documents, since they are historical records of the planning process, not runtime artifacts. Integration's recommendation to perform a grep for `001-antipattern-steering` across the full conversus directory is the correct approach to identify the definitive file list.

#### Recommendation 2: Resolve constitution Principle IV contradiction

- **Original position**: Amend Principle IV directly to remove or qualify the STATUS.md mandate, as a P1 blocking defect.
- **Disposition**: Modified
- **Explanation**: Scope-boundary's cross-review (Dangerous Contradictions, item 1) raised a procedural challenge I failed to account for: constitution.md Principle I (L24-29) requires that every behavioral change start with a specification, and the constitution's own Amendments section (L201-202) requires documented rationale and impact analysis via `/speckit.constitution`. Amending Principle IV inline as part of spec 010's implementation would itself be a scope violation — spec 010's scope is explicitly "one catalog file, one SKILL.md instruction block" (spec.md L109). Integration's cross-review (Tensions, "Constitution Principle IV: amendment scope") reinforced this by noting the version bump requirement (MINOR bump from 1.1.0 to 1.2.0 per L203). I was correct that the contradiction is real and high-impact — the constitution's governance clause (L196-199) means Principle IV's MUST overrides the catalog's correction, making the antipattern functionally inert. But I was wrong to prescribe the fix as in-scope for spec 010. The modified recommendation: (1) downgrade from P1 to P2 within spec 010's remediation scope; (2) add an acknowledgment note in the constitution's Known Antipatterns section (L179-192) stating that Principle IV's STATUS.md mandate predates the antipattern catalog and is under review — this gives agents encountering both documents a resolution path without performing an unauthorized constitutional amendment; (3) queue a follow-up spec whose explicit scope is to amend Principle IV, following the constitution's own amendment process. This preserves my substantive finding while respecting scope-boundary's procedural discipline.

#### Recommendation 3: Add path-existence validation to T011

- **Original position**: Add an explicit validation step to T011 requiring filesystem verification of referenced paths.
- **Disposition**: Modified
- **Explanation**: Integration's cross-review (Dangerous Contradictions, item 1) identified a sequencing problem: if T011's wording is tightened (my recommendation) without first unchecking the box (integration's recommendation 6), the task remains marked complete against its new, stricter criteria — a worse state than before. Integration is correct that the checkbox is currently dishonest and must be unchecked first. The modified recommendation is a compound action: (1) uncheck T011 immediately (integration's recommendation), (2) amend T011's description to require actual filesystem verification of referenced paths ("For each path referenced in Example sections, verify the path exists by listing the directory. Record the verification result."), (3) fix the broken path in catalog.md, (4) re-execute T011 validation and only recheck the box when all paths resolve. This combines integration's data-integrity fix with my process-improvement fix in the correct sequence.

#### Recommendation 4: Add constitution consistency check to implementation workflow

- **Original position**: Add a validation rule to the catalog Maintenance section requiring reconciliation between new catalog entries and constitutional principles before adding entries that contradict them.
- **Disposition**: Modified
- **Explanation**: Integration's cross-review (Tensions, "Constitution Principle IV: amendment scope") noted that this recommendation introduces a standing process gate not present in the current spec — a new workflow requirement. Scope-boundary's cross-review (Dangerous Contradictions, item 1) reinforced that adding process gates within spec 010 risks exceeding its scope. However, both reviewers agreed the underlying concern is valid: the constitution's governance precedence (L196-199) means catalog entries that contradict constitutional principles are dead letter unless the contradiction is acknowledged. The modification preserves the intent but changes the location: instead of adding a validation rule to the catalog Maintenance section (which integration correctly noted is already contractually unspecified), the consistency check should be defined in the contract (catalog-format.md) as part of the "Adding a New Entry" workflow. Specifically, the contract should include a step: "Before finalizing a new entry, verify its Correction does not contradict any constitutional principle. If it does, note the conflict in the entry and reference the constitutional principle." This is lighter than my original "must amend the constitution first" requirement and avoids scope creep.

#### Recommendation 5: Define SC-001 measurement mechanism

- **Original position**: Add a note to SC-001 defining post-deliberation review as the measurement method.
- **Disposition**: Surviving
- **Explanation**: Scope-boundary's cross-review (Tensions, item 2) explicitly deferred to compliance on this point, stating "SC-001 and SC-002 are compliance concerns, not scope violations. Both reviews are internally consistent on this point." Integration's cross-review (Tensions, "SC-001 measurability") acknowledged the gap and noted that if SC-001 measurement is added, integration should verify the mechanism's references are consistent with catalog symptom format. Neither cross-review challenged the substance of this recommendation. A success criterion that cannot be measured provides no signal — it can never be formally satisfied or formally violated. Defining the measurement method, even as "manual post-deliberation review," makes SC-001 actionable rather than aspirational. This remains a P2 recommendation.

#### Recommendation 6: Clarify SC-003 "performance degrades" threshold

- **Original position**: Redefine "performance" in SC-003 to mean agent context window consumption rather than computation speed, with specific rewording.
- **Disposition**: Surviving
- **Explanation**: Integration's cross-review (Tensions, "SC-003 'performance' interpretation") raised a valid downstream concern: if "performance" is reinterpreted as context window budget, the keyword filtering in SKILL.md step 2 becomes a context management strategy rather than a speed optimization, which changes the rationale for why it exists. This is a fair observation, but it strengthens rather than weakens my recommendation. The keyword filtering in SKILL.md step 2 IS a context management strategy — agents scan a summary index rather than loading full entries precisely to conserve context window budget. Reframing SC-003 to acknowledge this makes the rationale explicit and prevents future implementors from wasting effort optimizing computation speed for a markdown-based catalog where computation is not the bottleneck. Neither scope-boundary nor integration challenged the core claim that "retrieval performance" is misleading for a markdown catalog with no computation. This remains a P2 recommendation with the additional note that the rewording should explicitly connect keyword filtering to context window management.

#### Recommendation 7: Add field-count validation to catalog entry template

- **Original position**: Add a structured checklist in the Maintenance section enumerating all required fields with their validation constraints.
- **Disposition**: Modified
- **Explanation**: Integration's cross-review (Tensions, "Entry validation: checklist artifact vs. contract amendment") correctly identified that my recommendation places validation rules in the catalog (the runtime artifact agents read) while integration's recommendation places structural requirements in the contract (the governance artifact that defines format). If both are implemented independently, validation rules exist in two places with no defined precedence. Scope-boundary's cross-review raised a complementary concern about keyword-sync validation (Recommendation 5 in scope-boundary's review). My own cross-review of integration agreed that the contract should be the single source of truth for structural and validation rules. The modified recommendation: add a consolidated validation checklist to the contract (catalog-format.md), not to the catalog Maintenance section. The checklist should cover both field-count validation (my original concern) and keyword synchronization between index and entries (scope-boundary's concern). The catalog Maintenance section should reference the contract for validation constraints rather than duplicating them. This remains P3.

---

### New Recommendations

#### New Recommendation A: Acknowledge SKILL.md step 2 divergence from contract "Exact wording"

- **Source**: Integration's cross-review of compliance (Dangerous Contradictions, item 2) identified that compliance certified FR-005/FR-006 as "Implemented" without noting that SKILL.md step 2 diverges from the contract's "Exact wording" label (catalog-format.md L91). The contract specifies "Exact wording" for the integration block, but SKILL.md step 2 (L205) includes keyword retrieval guidance added by T008 that is not present in the contract (L100).
- **Recommendation**: Update catalog-format.md to either (a) reflect the current SKILL.md step 2 wording, or (b) relabel the section from "Exact wording" to "Minimum wording" to accommodate additive extensions. Priority: P2. If the contract retains the "Exact wording" label without updating the text, a future implementer regenerating SKILL.md from the contract will silently regress the T008 keyword retrieval enhancement.
- **Why I missed this**: My review treated the T008 enhancement as an expected evolution of FR-006/FR-008, and I did not re-examine the contract's "Exact wording" constraint after verifying functional compliance. Integration is right that contract fidelity requires the contract text to match the implementation when the contract claims exact correspondence.

#### New Recommendation B: Note T006 spec traceability gap

- **Source**: Scope-boundary's cross-review of compliance (Dangerous Contradictions, item 2) flagged that T006 (constitution Known Antipatterns update) has no spec-level acceptance scenario. Spec.md L109 lists only "SKILL.md or templates" as integration points, yet T006 modifies constitution.md. Compliance accepted T006 as a verified pass without acknowledging this traceability gap.
- **Recommendation**: Note T006 as "implemented correctly but with a spec traceability gap." The implementation is well-formed — the Known Antipatterns section is accurate and useful — but the task traces to no spec requirement or acceptance scenario. To close the gap, add constitution.md to the spec's Assumptions section (L104-110) as an affected artifact, or add an acceptance scenario to User Story 2 covering the constitution cross-reference. Priority: P3. This does not block shipping but establishes a precedent that implementation tasks must trace to spec requirements.
- **Why I missed this**: My review validated T006 against the task description in tasks.md (L52) and confirmed the content was correct, but I did not check whether the task itself had spec-level grounding. Scope-boundary is correct that compliance should flag tasks that lack formal spec traceability, even when the implementation is sound.

---

### Position Summary

My original review identified seven recommendations, two of which I classified as P1 blocking defects: the broken example path and the constitution Principle IV contradiction. The cross-review process has confirmed the broken path as a genuine P1 blocker — all three reviewers agree on this finding with high confidence. However, the constitution Principle IV recommendation requires significant modification. Scope-boundary correctly argued that amending constitutional principles within spec 010's implementation scope violates the constitution's own amendment process (Principle I, Amendments section). The contradiction is real and functionally significant — I stand by the finding that Principle IV's MUST overrides the catalog entry's correction, making the antipattern inert — but the remedy must be a follow-up spec, not an inline amendment. I have downgraded this from P1 (fix now, within spec 010) to P2 (acknowledge now, fix via follow-up spec with proper constitutional amendment process).

The cross-reviews also exposed two gaps in my original analysis. First, I failed to flag the SKILL.md step 2 divergence from the contract's "Exact wording" label — integration correctly identified this as a contract fidelity issue that my requirement-by-requirement verification should have caught. Second, I accepted T006 without questioning its spec-level traceability — scope-boundary correctly noted that a compliance audit should verify tasks trace to spec requirements, not just that the implementation content is correct. Both gaps have been added as new recommendations.

The revised position retains five of the seven original recommendations in some form (two modified, two surviving, one substantially modified), withdraws none entirely, and adds two new recommendations from the cross-review process. The overall assessment remains that spec 010 is well-implemented with one clear blocking defect (the broken example path), one significant governance tension requiring a follow-up spec (Principle IV), and several process improvements that would strengthen the antipattern system's durability as the catalog grows.
