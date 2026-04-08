# Deliberation Synthesis: Spec 010 — Agent Antipattern Steering

**Synthesizer**: neutral
**Date**: 2026-03-20
**Specification**: `/conversus/specs/010-antipattern-steering/spec.md`

---

## Process Summary

- **Agents**: 3 — compliance, integration, scope-boundary
- **Total artifacts**: 15 (3 Phase 1 reviews + 6 Phase 2 cross-reviews + 3 Phase 3 revisions + 3 Phase 4 disputes)
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 22 (compliance: 7, integration: 8, scope-boundary: 7)
- **Recommendations withdrawn** (Phase 3): 1 (scope-boundary R7: explicit phase-execution boundary note)
- **Recommendations modified** (Phase 3): 11 (compliance: R1, R2, R3, R4, R7; integration: R1, R2, R5, R6, R8; scope-boundary: R2, R4, R5)
- **Recommendations surviving** (Phase 3): 6 (compliance: R5, R6; integration: R3, R4, R7; scope-boundary: R1, R3, R6)
- **New recommendations added** (Phase 3): 6 (compliance: A, B; integration: N1, N2; scope-boundary: N1, N2)
- **Disputes remaining** (Phase 4): 3 (Principle IV remediation location, constitution version bump priority, `001` typo blast radius completeness)
- **Convergence points** (Phase 4): 5

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| C-R1 | compliance | Fix broken example path (`001` to `010`) in catalog.md and tasks.md | P1 | Modified (expanded scope to include quickstart.md; plan.md/research.md as errata) | integration (broader file list), scope-boundary (confirmed correct path) | Unanimous P1 | **Converged** |
| C-R2 | compliance | Resolve constitution Principle IV contradiction by amending Principle IV directly | P1 | Modified (downgraded to P2 within spec 010; deferred amendment to follow-up spec; acknowledgment note in Known Antipatterns section) | scope-boundary (scope violation), integration (agreed P1 but also accepted narrower scope for fix) | Disputed — remediation location | **Disputed** |
| C-R3 | compliance | Add path-existence validation to T011 | P1 | Modified (combined with integration R6: uncheck T011 first, then amend, then re-validate) | integration (sequencing concern) | Unanimous compound action | **Converged** |
| C-R4 | compliance | Add constitution consistency check to implementation workflow | P2 | Modified (moved to contract as lightweight check, not standing gate) | integration (new workflow overhead), scope-boundary (scope creep risk) | Agreed on contract placement | **Converged** (folded into Maintenance section in contract) |
| C-R5 | compliance | Define SC-001 measurement mechanism | P2 | Surviving | scope-boundary (deferred to compliance), integration (acknowledged gap) | No challenge | **Accepted** |
| C-R6 | compliance | Clarify SC-003 "performance degrades" threshold | P2 | Surviving | integration (noted downstream impact on step 2 rationale) | No challenge to substance | **Accepted** |
| C-R7 | compliance | Add field-count validation to catalog entry template | P3 | Modified (moved to contract; consolidated with scope-boundary R5 keyword-sync) | integration (contract vs. catalog placement) | Agreed on consolidated contract checklist | **Converged** (merged with SB-R5) |
| I-R1 | integration | Fix example path references across 6 files | P1 | Modified (narrowed from "determine correct location" to "replace `001` with `010`") | compliance (specific path known), scope-boundary (filesystem verified) | Unanimous P1 | **Converged** |
| I-R2 | integration | Resolve STATUS.md contradiction in constitution by amending Principle IV | P1 | Modified (narrowed to qualifying inline note on Principle IV, not full rewrite) | scope-boundary (scope violation), compliance (procedural discipline) | Disputed — remediation location | **Disputed** |
| I-R3 | integration | Update contract to reflect extended step 2 ("Exact wording" divergence) | P2 | Surviving | None | Unanimous P2 | **Converged** |
| I-R4 | integration | Add Maintenance section to contract template | P2 | Surviving | None | Unanimous P2 | **Converged** |
| I-R5 | integration | Add disambiguation for Maintenance heading (sentinel comment) | P2 | Modified (downgraded to P3) | compliance (P3 enhancement, not prerequisite) | Agreed as P3 | **Accepted** (P3) |
| I-R6 | integration | Mark T011 incomplete (uncheck box) | P2 | Modified (combined with compliance R3 into compound action) | compliance (also needs process fix, not just uncheck) | Unanimous compound action | **Converged** |
| I-R7 | integration | Add catalog self-reference to format contract (HTML comment footer) | P3 | Surviving | None | No challenge | **Accepted** |
| I-R8 | integration | Verify constitution version bump requirement (1.1.0 to 1.2.0) | P3 | Modified (elevated to P2, tied to Principle IV fix) | compliance (should be coupled with Principle IV amendment), scope-boundary (P3 sufficient) | Disputed — priority | **Disputed** |
| SB-R1 | scope-boundary | Fix broken example path in catalog.md | P1 | Surviving (scope expanded to match integration's 6-file list) | None | Unanimous P1 | **Converged** |
| SB-R2 | scope-boundary | Acknowledge constitution Principle IV tension | P2 | Modified (upgraded to P1; inline qualifying note on Principle IV + follow-up spec) | compliance (P1 agreed but different remediation), integration (P1, inline note) | Disputed — remediation location | **Disputed** |
| SB-R3 | scope-boundary | Add spec traceability for constitution update T006 | P2 | Surviving | compliance (initially missed), integration (initially missed) | Unanimous P3 | **Converged** |
| SB-R4 | scope-boundary | Fix path reference in tasks.md T003 and T011 | P2 | Modified (merged with R1; added T011 uncheck per integration) | integration (audit-integrity argument for unchecking) | Unanimous compound action | **Converged** |
| SB-R5 | scope-boundary | Verify Summary Index keyword-to-entry consistency on future additions | P2 | Modified (consolidated with compliance R7 into single contract checklist) | compliance (broader field-validation checklist) | Agreed on consolidation | **Converged** (merged with C-R7) |
| SB-R6 | scope-boundary | Confirm no template changes were made | P3 | Surviving (confirmation, not change) | None | Verified by all | **Accepted** (verification passed) |
| SB-R7 | scope-boundary | Add explicit scope-boundary note about phase execution | P3 | Withdrawn | Neither cross-review mentioned or supported it | N/A | **Withdrawn** |
| C-RA | compliance | Acknowledge SKILL.md step 2 divergence from contract "Exact wording" | New (P2) | New in Phase 3 | Source: integration cross-review | Unanimous P2 | **Converged** (same as I-R3) |
| C-RB | compliance | Note T006 spec traceability gap | New (P3) | New in Phase 3 | Source: scope-boundary cross-review | Unanimous P3 | **Converged** (same as SB-R3) |
| I-N1 | integration | Verify full `001` typo blast radius via grep before fix | New (P1) | New in Phase 3 | Source: file-count discrepancy across reviews | Unanimous | **Converged** |
| I-N2 | integration | Address T006 scope traceability gap | New (P3) | New in Phase 3 | Source: scope-boundary review | Unanimous P3 | **Converged** (same as SB-R3) |
| SB-N1 | scope-boundary | Update contract's SKILL.md Integration "Exact wording" to match actual SKILL.md | New (P2) | New in Phase 3 | Source: integration cross-review | Unanimous P2 | **Converged** (same as I-R3) |
| SB-N2 | scope-boundary | Bump constitution version from 1.1.0 to 1.2.0 | New (P3) | New in Phase 3 | Source: integration cross-review | Disputed — priority | **Disputed** (P2 vs. P3) |

---

## Dangerous Contradictions Found

### Resolved Contradictions

**1. Example path: investigation vs. find-and-replace**

- **Phase 1 positions**: Integration framed the broken path as an open question requiring investigation ("determine the correct location"). Compliance and scope-boundary asserted the correct path is `specs/010-antipattern-steering/examples/redundant-cache/`, verified by filesystem inspection.
- **Resolution**: Integration accepted the specific path fix in Phase 3 (integration revision, R1). All three agents converged on a mechanical find-and-replace of `001` with `010`. Integration independently verified the filesystem evidence.
- **Synthesizer assessment**: Correctly resolved. Compliance's and scope-boundary's filesystem-verified evidence was conclusive. Integration's caution was understandable but unnecessary.

**2. T011 disposition: uncheck vs. fail-and-strengthen**

- **Phase 1 positions**: Integration recommended unchecking T011 (data integrity fix). Compliance recommended strengthening T011's validation criteria (process fix).
- **Resolution**: Both agents accepted the compound action in Phase 3: uncheck first (integration), then amend criteria (compliance), then re-validate. Scope-boundary concurred.
- **Synthesizer assessment**: Correctly resolved. The compound action addresses both the symptom (dishonest checkbox) and the root cause (insufficient validation criteria).

**3. Broken path file scope: 3 vs. 6 vs. 8 files**

- **Phase 1 positions**: Compliance found 3 locations, scope-boundary found 5, integration found 6.
- **Resolution**: Integration's Phase 4 disputes document (Dispute 3) expanded the count to 8 after a grep, adding `conversus.yml` L57 and `research.md` L71. All agents converged on a grep-first approach to identify the definitive list.
- **Synthesizer assessment**: Correctly resolved. Integration's N1 recommendation (grep before fix) is the definitive approach. The synthesizer notes that all three agents' revisions understated the affected file count, validating the necessity of the grep step.

### Unresolved Contradictions

**1. Constitution Principle IV — remediation location**

This is the deliberation's central unresolved contradiction. See **Remaining Disputes, Dispute 1** below for full analysis.

**2. Constitution version bump — priority classification**

See **Remaining Disputes, Dispute 2** below.

---

## Systemic Contradictions

1. **Governance documents were modified without following their own governance rules.** The constitution was materially expanded (Known Antipatterns section added at L179-192, containing a MUST-level instruction) without the required version bump (L203), without documentation of change, rationale, and impact (L201-202), and without spec-level authorization (spec.md L109 lists only "SKILL.md or templates"). Three separate manifestations of the same root cause: T006 was added to the task list during planning without checking whether it triggered the constitution's own amendment process. This is the systemic issue underlying both remaining disputes.

2. **Validation tasks were marked complete without actual validation.** T011 claims cross-reference validation was performed, but the validated path does not exist. T010 claims FR validation was performed, but the broken path means FR-002 and SC-004 are only partially satisfied. The validation process lacks a concrete verification step (listing directories, checking file existence) and relies on textual review of path strings. This systemic gap enabled the `001` typo to propagate from design documents through implementation to the verification phase without detection.

3. **The contract claims authority it does not exercise.** Catalog-format.md (L7) states it defines "the exact structure" of catalog.md, and (L91) labels the SKILL.md integration block as "Exact wording." In practice, the implementation diverges from both claims: the catalog includes a Maintenance section the contract does not define, and SKILL.md step 2 extends beyond the contract's "exact" text. The contract's authority claims are aspirational rather than enforced, creating a false sense of specification coverage.

4. **Cross-document consistency is not systematically checked.** The constitution's Principle IV mandates STATUS.md maintenance while the catalog's first entry condemns it. This contradiction was introduced during spec 010 implementation and persisted through all task checkpoints because no task or validation step checks for conflicts between catalog entries and constitutional principles. The edge case section of the spec (L59) anticipates conflicting antipatterns but not conflicts between antipatterns and governance documents.

5. **Design-phase path errors propagate into implementation without a correction mechanism.** The `001` typo originated in early design documents (plan.md, tasks.md) and propagated into the implementation artifact (catalog.md), the implementation record (tasks.md validation checkpoints), onboarding documentation (quickstart.md), and the verification configuration (conversus.yml). No step in the workflow compares design-phase references against actual filesystem state. The error's presence in 8 files across design, implementation, and verification phases demonstrates that path references are copied forward without verification at any stage.

---

## Convergence Achieved

Ordered by strength of agreement (strongest first):

1. **Broken example path is the single P1 factual defect.** All three agents identified this independently in Phase 1, maintained it through all four phases, and agree unanimously on the fix: replace `001-antipattern-steering` with `010-antipattern-steering` across all referencing files, preceded by a comprehensive grep. The correct path `specs/010-antipattern-steering/examples/redundant-cache/` was filesystem-verified by both compliance and scope-boundary. (compliance review R1; integration review R1; scope-boundary review R1; all Phase 4 convergence sections)

2. **T011 must be unchecked and re-validated as a compound action.** All three agents converged on the four-step sequence: uncheck T011, amend its description to require filesystem path verification, fix the broken path, then re-execute validation. This originated from two independent Phase 1 recommendations (integration R6: uncheck; compliance R3: strengthen criteria) that were merged during cross-review and accepted by scope-boundary in revision. (compliance revision R3; integration revision R6; scope-boundary revision R4; all Phase 4 convergence sections)

3. **Contract "Exact wording" label must be reconciled with actual SKILL.md content.** Integration identified this in Phase 1; compliance and scope-boundary missed it initially but both accepted the finding during cross-review and added it as new recommendations. All three agree on P2 priority and that either updating the contract text or relabeling the heading resolves the issue. (integration review R3; compliance revision RA; scope-boundary revision N1; all Phase 4 convergence sections)

4. **T006 has a spec traceability gap that should be closed.** Scope-boundary identified this in Phase 1; compliance and integration initially treated T006 as satisfactorily implemented. Both accepted the gap during cross-review and added new recommendations. All agree the implementation is functionally correct and the gap is formal, resolvable by adding constitution.md to the spec's Assumptions section. (scope-boundary review R3; compliance revision RB; integration revision N2; all Phase 4 convergence sections)

5. **Catalog Maintenance section and validation checklist belong in the contract.** Three separate Phase 1 recommendations (integration R4: Maintenance section in contract; compliance R7: field-count validation; scope-boundary R5: keyword-sync verification) were consolidated during cross-review into a single position: the contract is the single source of truth for structural requirements, validation rules, and maintenance procedures. (compliance revision R7; integration revision R4; scope-boundary revision R5; all Phase 4 convergence sections)

6. **The implementation is well-bounded and additive.** All three agents confirmed that no templates, phase execution logic, or existing agent behaviors were modified beyond the additive Antipattern Check insertion in SKILL.md. The one scope extension (T006, constitution update) was acknowledged as additive and non-destructive. (compliance review Alignment FR-005/FR-006/FR-010; integration review Alignment bullets 1-6; scope-boundary review Alignment bullets 2-5)

7. **The catalog entry's data model fidelity is correct (modulo Example path).** Both structural conformance (field ordering matches contract) and content validation (field-count constraints satisfied) were independently verified. Compliance checked field-by-field validation, integration checked structural ordering, scope-boundary checked data model alignment. The sole defect is the broken Example path reference. (compliance review Catalog Entry Field Validation table; integration review Alignment bullet 4; scope-boundary review Alignment bullet 4)

8. **Constitution Principle IV creates a real, high-impact contradiction with the seed antipattern.** All three agents agree this contradiction exists, that it is harmful, and that the governance precedence clause (L196-199) means Principle IV's MUST overrides the catalog entry's correction. The disagreement is solely about the appropriate remediation scope and location within spec 010, not about the existence or severity of the problem. (All Phase 1 reviews; all Phase 3 revisions; all Phase 4 dispute documents)

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

### Dispute 1: Constitution Principle IV — Remediation Location

- **Positions**:
  - **Integration + scope-boundary** (aligned in Phase 3/4): Add a qualifying inline note directly to Principle IV's STATUS.md bullet on L73-75 — e.g., appending "unless this practice is identified as an antipattern in `antipatterns/catalog.md` (see `redundant-cache`)" or "See `redundant-cache` in `antipatterns/catalog.md` for guidance on when STATUS.md maintenance is counterproductive." Classify as P1. File a follow-up spec for full reconciliation. (integration revision R2; scope-boundary revision R2; integration disputes Dispute 1; scope-boundary disputes Dispute 1)
  - **Compliance** (revised in Phase 3, held in Phase 4): Do NOT modify Principle IV's operative text. Instead, add an acknowledgment note to the Known Antipatterns section (L179-192) stating that Principle IV's STATUS.md mandate predates the catalog and is under review. Queue a follow-up spec for the formal constitutional amendment. (compliance revision R2; compliance disputes Dispute 1)

- **Arguments**:
  - **Integration/scope-boundary's strongest argument**: The constitution's Governance precedence clause (L196-199) states "This constitution supersedes conflicting guidance in individual specs or agent prompts." An acknowledgment note placed in the Known Antipatterns section is formally subordinate to Principle IV's unqualified MUST mandate. An agent following governance rules will resolve the conflict in favor of Principle IV and maintain STATUS.md, ignoring the acknowledgment note as informational. Only a qualification on Principle IV itself — the operative text — can actually neutralize the contradiction for governance-rule-following agents. (integration disputes, Dispute 1; scope-boundary disputes, Dispute 1)
  - **Compliance's strongest argument**: Adding a conditional clause to a MUST-level instruction changes its semantics, constituting a material amendment. The constitution's own amendment rules (L201-202) require "documentation of the change, rationale, and impact on existing specs." Spec 010's authorized scope (L109) covers "SKILL.md or templates," not constitutional principle modification. Performing a constitutional amendment as a side-effect of a catalog-creation spec sets a precedent that principles can be incrementally hollowed out by any spec that finds them inconvenient. (compliance disputes, Dispute 1)

- **Synthesizer assessment**: Integration and scope-boundary have the stronger functional argument. The governance precedence clause is explicit and unambiguous — it formally subordinates any content in the Known Antipatterns section to Principle IV's operative text. Compliance's proposed remediation, while procedurally disciplined, would leave agents receiving contradictory instructions with no governance-level resolution, because the MUST in Principle IV formally overrides the acknowledgment note in a section that has no governance-override authority. However, compliance raises a legitimate procedural concern: adding a conditional exception to a MUST-level constitutional instruction is substantively an amendment, regardless of its git-diff footprint.

  The key insight is scope-boundary's flexibility statement (Phase 4 disputes): "If the synthesizer rules that a cross-reference append is PATCH-level (L204: 'clarifications'), that resolves the scope objection." This offers a path through the impasse. A pure cross-reference (e.g., "See `redundant-cache` in `antipatterns/catalog.md`") is closer to a clarification than an amendment. A conditional exception (e.g., "unless this practice is identified as an antipattern") is closer to an amendment. The wording matters.

- **Recommended resolution**: Add a cross-reference note to Principle IV's STATUS.md bullet — e.g., appending: "For guidance on when this practice is counterproductive, see `redundant-cache` in `antipatterns/catalog.md`." This is a clarifying cross-reference, not a conditional exception, and can defensibly be classified as PATCH-level per L204. It does not add an "unless" clause or change the MUST semantics; it directs agents to additional context that informs their judgment. Simultaneously, file a follow-up spec for formal Principle IV reconciliation through `/speckit.constitution`. Execute the constitution version bump (1.1.0 to 1.2.0) alongside this change to satisfy the governance versioning rules.

### Dispute 2: Constitution Version Bump Priority

- **Positions**:
  - **Integration** (Phase 3/4): P2, tied to the Principle IV qualification. Must be atomic with the Principle IV fix. (integration revision R8; integration disputes Dispute 2)
  - **Scope-boundary** (Phase 3/4): P3, standalone governance housekeeping. Should not gate spec completion. (scope-boundary revision N2; scope-boundary disputes Dispute 2)
  - **Compliance** (Phase 3/4): No explicit priority assigned; argues the bump must be coupled with whatever Principle IV resolution is chosen, not performed independently. (compliance disputes, Dispute 2)

- **Arguments**:
  - **Integration's strongest argument**: The Known Antipatterns section contains a MUST-level instruction ("Agents MUST check the antipattern catalog"). A MUST-level behavioral directive is a material expansion. Shipping the constitution with a MUST-level addition and no version bump violates the constitution's own versioning contract. The version number becomes unreliable as an indicator of what an agent should expect. (integration disputes, Dispute 2)
  - **Scope-boundary's strongest argument**: The version bump is mechanical governance housekeeping that does not affect agent behavior, does not block any functional requirement, and does not create a contradiction. Classification matters because it determines whether the bump gates the "spec complete" verdict — and it should not. (scope-boundary disputes, Dispute 2)
  - **Compliance's strongest argument**: The version bump and the Principle IV resolution are coupled actions. Performing the bump without the Principle IV resolution documents an incomplete change. The two belong together. (compliance disputes, Dispute 2)

- **Synthesizer assessment**: Integration's argument that a MUST-level addition requires a version bump per the constitution's own rules (L203) is textually well-supported. Scope-boundary's argument that it should not gate spec completion is pragmatically reasonable. Compliance's coupling argument is logically coherent but creates a chicken-and-egg problem if the Principle IV resolution is deferred.

- **Recommended resolution**: P2, executed alongside the Principle IV cross-reference note recommended in Dispute 1. If both changes are made atomically (cross-reference append + version bump to 1.2.0 + Sync Impact Report update), all three agents' constraints are satisfied: integration gets the bump at appropriate priority, scope-boundary avoids it gating spec completion as a standalone item, and compliance gets the coupling with the Principle IV change.

### Dispute 3: Affected File Count for `001` Typo

- **Positions**:
  - **Integration** (Phase 4): Eight files contain the broken reference, including `conversus.yml` L57 and `research.md` L71 — files not identified in any agent's Phase 3 revision. (integration disputes, Dispute 3)
  - **Compliance and scope-boundary** (Phase 3): Six files (integration's original count) or fewer.

- **Arguments**:
  - This is not a substantive disagreement — all agents agree the fix should be preceded by a comprehensive grep (integration N1, endorsed by all). Integration's Phase 4 finding simply demonstrates that the grep has already revealed additional files.

- **Synthesizer assessment**: Integration is correct. The grep-first approach is the definitive method. The specific file count in any recommendation is an approximation that the grep will supersede.

- **Recommended resolution**: The spec change should specify a grep for `001-antipattern-steering` across the entire conversus directory as the first step, with all matches corrected. No hardcoded file list. Integration's finding of 8 files validates this approach.

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1 — Must implement

**1. Fix broken example path across all referencing files.** (Traces to: C-R1, I-R1, SB-R1, I-N1)

Run `grep -r "001-antipattern-steering" .` across the conversus directory to identify all references. Replace `001-antipattern-steering` with `010-antipattern-steering` in every match. Known affected files include catalog.md L33, tasks.md L38 and L77, quickstart.md L15 and L47, plan.md L63, conversus.yml L57, and research.md L71 — but the grep is the authoritative source.

**2. Uncheck T011, amend its validation criteria, and re-validate.** (Traces to: C-R3, I-R6, SB-R4)

Execute in sequence: (a) uncheck T011 (`[ ]`) to reflect that its validation condition was never actually met, (b) amend T011's description to require filesystem path verification ("For each path referenced in Example sections, verify the path exists by listing the directory. Record the verification result."), (c) apply the path fix from item 1, (d) re-execute T011 validation and only recheck the box when all paths resolve.

**3. Add a cross-reference to Principle IV's STATUS.md bullet and bump the constitution version.** (Traces to: C-R2, I-R2, SB-R2, I-R8, SB-N2)

Append a cross-reference note to the STATUS.md bullet in Principle IV (constitution.md L73-75) — e.g., "For guidance on when this practice is counterproductive, see `redundant-cache` in `antipatterns/catalog.md`." Simultaneously bump the constitution version from 1.1.0 to 1.2.0 and update the Sync Impact Report (L1-16) to document both the Known Antipatterns section addition and the Principle IV cross-reference. File a follow-up spec for full Principle IV reconciliation through `/speckit.constitution`.

### P2 — Should implement

**4. Reconcile contract "Exact wording" with actual SKILL.md step 2.** (Traces to: I-R3, C-RA, SB-N1)

Update catalog-format.md L91-103 to either (a) match the current SKILL.md step 2 wording including keyword retrieval guidance from T008, or (b) relabel "Exact wording" as "Minimum required content" to permit additive extensions.

**5. Add Maintenance section to the contract template.** (Traces to: I-R4, C-R7, SB-R5)

Append a `## Maintenance` section to catalog-format.md defining the expected structure for Adding and Deprecating entries. Include a consolidated validation checklist covering: (a) all required fields per the data model (Status, Observed, Summary <100 chars, Symptoms >=2, Root Cause, Example with real refs, Correction, When This Does NOT Apply >=1, Keywords >=2), (b) keyword synchronization between Summary Index rows and entry Keywords sections, (c) a check that the entry's Correction does not contradict any constitutional principle (if it does, note the conflict in the entry).

**6. Define SC-001 measurement mechanism.** (Traces to: C-R5)

Add a note to SC-001 (spec.md L99): "Measured by post-deliberation review: if any deliberation output proposes an artifact matching a cataloged antipattern's symptoms, SC-001 is violated. Detection is manual until automated symptom matching is implemented."

**7. Clarify SC-003 "performance degrades" threshold.** (Traces to: C-R6)

Reword SC-003 (spec.md L101) to: "The Summary Index supports 50+ entries within a single agent context read. Full-entry retrieval is filtered by keyword match, loading only relevant entries." This reframes performance as context window budget rather than computation speed, which is the actual constraint for a markdown-based catalog.

### P3 — Consider implementing

**8. Add spec traceability for T006.** (Traces to: SB-R3, C-RB, I-N2)

Add constitution.md to spec.md's Assumptions section (L104-110) as an affected artifact, acknowledging it as an integration point beyond "SKILL.md or templates."

**9. Add disambiguation for Maintenance heading.** (Traces to: I-R5)

Add a sentinel comment (e.g., `<!-- CATALOG:ENTRIES_END -->`) before the Maintenance section in catalog.md to enable future retrieval mechanisms to distinguish entries from maintenance documentation.

**10. Add catalog self-reference to the catalog file.** (Traces to: I-R7)

Add an HTML comment footer to `antipatterns/catalog.md` referencing the governing contract: `<!-- Format governed by specs/010-antipattern-steering/contracts/catalog-format.md -->`.

---

## Key Concessions

1. **Compliance downgraded the Principle IV amendment from P1-in-scope to P2-deferred.** In Phase 1, compliance classified direct amendment of Principle IV as P1 and proposed specific replacement language. After scope-boundary's cross-review demonstrated that constitutional amendments require their own spec per the constitution's Principle I and amendment rules (L201-202), compliance accepted the procedural argument and downgraded the in-scope remediation to an acknowledgment note, deferring the actual principle modification to a follow-up spec. (compliance revision R2)

2. **Scope-boundary upgraded the Principle IV tension from P2 to P1.** In Phase 1, scope-boundary classified the contradiction as a "missed opportunity" at P2 and explicitly noted the implementation "correctly did not modify Principle IV without a spec." After both compliance and integration demonstrated through the governance precedence clause (L196-199) that the unqualified MUST makes the antipattern functionally inert, scope-boundary accepted the urgency argument and upgraded to P1 — while maintaining the narrower remediation scope. (scope-boundary revision R2)

3. **Integration accepted the specific path fix over open-ended investigation.** In Phase 1, integration framed the broken example path as requiring investigation ("determine the correct location"). After compliance and scope-boundary independently verified the correct path via filesystem inspection, integration accepted that the fix is a mechanical find-and-replace, not an investigation. (integration revision R1)

4. **Scope-boundary withdrew its recommendation for explicit phase-execution boundary notes.** After neither cross-review mentioned or supported the recommendation, scope-boundary recognized it as overly cautious for an implementation that is already cleanly bounded by its own H3 heading. (scope-boundary revision R7)

5. **Scope-boundary conceded the T011 audit-integrity argument.** In Phase 1, scope-boundary recommended a forward-looking approach: fix the path reference in T011 and move on. After integration's cross-review argued that leaving T011 checked while correcting its path implies validation passed against the corrected path (which is historically inaccurate), scope-boundary accepted the audit-preserving approach: uncheck first, then fix, then re-validate. (scope-boundary revision R4)

6. **Compliance and scope-boundary both accepted the contract "Exact wording" divergence finding.** Both missed this in Phase 1. Integration identified it. Both accepted it during cross-review: compliance added it as New Recommendation A, scope-boundary added it as N1, and scope-boundary explicitly stated "integration has the stronger position here." (compliance revision RA; scope-boundary revision N1)
