# Compliance Disputes: Spec 010 — Agent Antipattern Steering

**Reviewer**: compliance
**Phase**: 4 (Final Statement)
**Date**: 2026-03-20

---

### Remaining Disputes

**Dispute: Constitution Principle IV — Scope of the In-Spec Fix**

- **My claim**: The contradiction between Principle IV's STATUS.md MUST mandate (constitution L73-75) and the `redundant-cache` antipattern must be acknowledged within spec 010's remediation, but the actual Principle IV amendment belongs to a follow-up spec. My revised position (Recommendation 2) proposes: (1) add an acknowledgment note in the Known Antipatterns section (L179-192) stating that Principle IV's STATUS.md mandate predates the antipattern catalog and is under review, giving agents a resolution path; (2) queue a follow-up spec for the full constitutional amendment via `/speckit.constitution`.
- **Opposing position(s)**: Integration's revised position (Recommendation 2) proposes adding a qualifying inline note directly to Principle IV's STATUS.md bullet — e.g., appending "unless this practice is identified as an antipattern in `antipatterns/catalog.md`." Integration argues this is additive, consistent with Principle III (backward-compatible extension), and within T006's scope. Scope-boundary's revised position (Recommendation 2) converges with integration: add a qualifying inline note to Principle IV, elevate to P1, and file a follow-up spec for full reconciliation.
- **Why I will not concede**: The integration/scope-boundary approach modifies the semantic meaning of a constitutional principle by adding a conditional exception. Whether you call this "qualifying" or "amending," it changes the MUST mandate from unconditional to conditional. This is a material change to a principle, not a clarification or additive extension. The constitution's own amendment rules (L201-202) require "documentation of the change, rationale, and impact on existing specs." The Governance section (L196-199) establishes constitutional supremacy. A principle modification — even a narrow one — performed as a side-effect of a catalog-creation spec, without its own spec, without an impact analysis, and without following `/speckit.constitution`, sets a precedent that principles can be incrementally hollowed out by any spec that finds them inconvenient. The Known Antipatterns section (L179-192) already provides the correct resolution path: it tells agents to check the catalog. An agent reading both Principle IV and the Known Antipatterns section will encounter the catalog reference and find the `redundant-cache` entry, which provides the correction. Adding an explicit note that the conflict is under review makes the resolution path even clearer without touching the principle text.
- **Counter-argument to their position**: Integration argues the qualifying note is "consistent with Principle III: backward-compatible extension." But Principle III governs feature additions to the conversus system (optional fields, new SKILL.md sections), not modifications to constitutional principles. A constitutional principle is not a feature — it is a governance constraint that features must comply with. Backward-compatible extension means "omitting optional fields preserves existing behavior" (L52-53); it does not mean "adding conditionals to MUST mandates is backward-compatible." Scope-boundary's original review correctly identified this as an over-scope risk before reversing position under cross-review pressure. The fact that all three reviewers agree the contradiction is real and P1-level does not mean all three must agree on the same remediation path.
- **Proposed resolution path**: Both approaches neutralize the contradiction for agents — mine via the Known Antipatterns section, theirs via an inline Principle IV note. The synthesizer should evaluate whether modifying a constitutional principle within a spec that did not authorize it creates a governance precedent the project is willing to accept. If the project prefers the inline note, it should at minimum be accompanied by the version bump (1.1.0 to 1.2.0) and a Sync Impact Report update documenting the principle modification, per the constitution's own rules.

**Dispute: Constitution Version Bump Priority**

- **My claim**: The constitution version bump from 1.1.0 to 1.2.0 is a necessary corollary of the Known Antipatterns section addition (L179-192), which is a material expansion per the constitution's versioning rules (L203). My revision did not assign an explicit priority to this because I treated it as part of the follow-up spec for the Principle IV amendment. The bump and the amendment should be a single atomic governance action.
- **Opposing position(s)**: Integration's revised position (Recommendation 8) elevates the version bump to P2 and ties it to their Recommendation 2 (the inline Principle IV note), arguing both should be executed together within spec 010. Scope-boundary's revised position (N2) classifies the version bump as P3, treating it as a standalone governance consistency fix.
- **Why I will not concede**: The version bump and the Principle IV resolution are coupled actions, not independent fixes. The Known Antipatterns section was added by T006, which all three reviewers agree has a spec traceability gap (it was not authorized by spec.md's integration points list at L109). Bumping the version without the Principle IV resolution documents an incomplete change — the Sync Impact Report would need to say "Added Known Antipatterns section" but could not coherently describe the Principle IV status because no decision has been made. Conversely, resolving Principle IV without the version bump violates the constitution's own governance rules. The two actions belong together in a follow-up spec that properly scopes the constitutional amendment. Performing the version bump now, detached from the principle resolution, creates an awkward intermediate state where the version is 1.2.0 but the governance conflict is unresolved and undocumented.
- **Counter-argument to their position**: Integration argues the bump should happen alongside their inline Principle IV note (P2). If the synthesizer accepts their Principle IV resolution, then coupling the bump with it is correct — but then both should be P1, not P2, because the principle modification is the higher-priority action that the bump follows. Scope-boundary's P3 classification treats the version bump as a standalone documentation fix, but the constitution's versioning rules are governance rules, not documentation conventions. A MINOR bump signals to consumers that the constitution's behavioral expectations have changed. Performing it at P3 priority means it could be deferred indefinitely while agents operate under a constitution whose version number understates its content.
- **Proposed resolution path**: If the synthesizer accepts the inline Principle IV note, the version bump must be P1 and executed atomically with it. If the synthesizer accepts my approach (defer principle modification to a follow-up spec), the version bump should accompany the follow-up spec, with a note in the current Known Antipatterns section that the version bump is pending the Principle IV amendment.

---

### Convergence

**Converged: Broken Example Path is P1 and Mechanical**

- **Shared position**: All references to `specs/001-antipattern-steering/` must be replaced with `specs/010-antipattern-steering/` across all affected files. The fix is a find-and-replace after a comprehensive grep to identify the full blast radius. This is the single clear blocking defect.
- **Agreeing agents**: compliance, integration, scope-boundary
- **Strength**: Unanimous
- **Path to convergence**: All three reviewers independently identified this in Phase 1. The cross-review process refined the affected file count (integration identified the broadest set at 6 locations) and confirmed the correct path via filesystem inspection.

**Converged: T011 Must Be Unchecked and Strengthened**

- **Shared position**: T011's checkbox must be unchecked because its validation condition (verifying cross-references) was never actually met — the broken path proves the validation passed against a non-existent directory. The task description should be amended to require filesystem verification of referenced paths, and the box should only be rechecked after re-execution with the corrected paths.
- **Agreeing agents**: compliance, integration, scope-boundary
- **Strength**: Unanimous
- **Path to convergence**: Integration proposed unchecking T011 in Phase 1. Compliance proposed strengthening T011's validation criteria in Phase 1. The cross-review process merged these into a compound action: uncheck, amend, fix path, re-validate, recheck. Scope-boundary conceded the audit-integrity argument during revision.

**Converged: Contract "Exact Wording" Must Be Reconciled with Actual SKILL.md**

- **Shared position**: The contract (catalog-format.md L91) labels the SKILL.md integration block as "Exact wording," but the actual SKILL.md step 2 (L205) includes keyword retrieval guidance added by T008 that is not present in the contract text. The contract must either be updated to match the implementation or relabeled from "Exact wording" to "Minimum required content."
- **Agreeing agents**: compliance, integration, scope-boundary
- **Strength**: Unanimous
- **Path to convergence**: Integration identified this in Phase 1. Compliance missed it initially but accepted the finding during cross-review and added it as New Recommendation A. Scope-boundary endorsed integration's position and added it as N1 during revision.

**Converged: T006 Has a Spec Traceability Gap**

- **Shared position**: T006 (constitution Known Antipatterns update) was implemented correctly but traces to no spec-level requirement. Spec.md L109 lists only "SKILL.md or templates" as integration points; constitution.md is not mentioned. The gap should be closed by adding constitution.md to the spec's Assumptions section as an affected artifact. This is a formal gap, not a functional defect.
- **Agreeing agents**: compliance, integration, scope-boundary
- **Strength**: Unanimous
- **Path to convergence**: Scope-boundary identified this in Phase 1. Compliance and integration initially treated T006 as satisfactorily implemented. Both accepted the traceability gap during cross-review and added corresponding new recommendations (compliance: New Recommendation B; integration: N2).

**Converged: Maintenance Section Belongs in Contract**

- **Shared position**: The catalog-format.md contract claims to define "the exact structure" of catalog.md (L7) but does not include the Maintenance section that exists in the implemented catalog. The contract should be updated to either define the Maintenance section or acknowledge it as an optional extension. Validation checklists (field-count, keyword-sync) should live in the contract as the single source of truth, not be duplicated in the catalog.
- **Agreeing agents**: compliance, integration, scope-boundary
- **Strength**: Unanimous
- **Path to convergence**: Integration identified the Maintenance section gap in Phase 1. Compliance proposed field-count validation in the catalog; integration proposed it in the contract. Cross-review converged on the contract as the correct location. Scope-boundary endorsed consolidation during revision.

---

### Final Position Statement

**Non-Negotiables** (2 items):

1. **The broken example path (`001` to `010`) must be fixed before spec 010 can be considered complete.** This is a factual error that causes the catalog's only entry to reference a non-existent directory, violating FR-004 (self-contained entries) and SC-004 (concrete examples from observed incidents). All three reviewers agree unanimously.

2. **Modifying a constitutional principle requires following the constitution's own amendment process.** Adding a conditional exception to Principle IV's MUST mandate — regardless of how it is framed — is a material change to a governance document that the constitution itself requires to go through `/speckit.constitution` with documented rationale and impact analysis (L201-202). Spec 010's scope (L109) authorizes SKILL.md and template integration, not constitutional principle modification. The antipattern system can function without the inline note because the Known Antipatterns section already directs agents to the catalog where the correction lives.

**Flexibility** (2 items):

1. **The constitution version bump can be P1 or P2 depending on how the Principle IV resolution is handled.** If the synthesizer accepts the inline Principle IV note, the bump must be P1 and atomic with it. If the synthesizer accepts deferral to a follow-up spec, the bump can accompany the follow-up. What must be preserved: the version bump happens, and it happens in the same change as the principle modification it documents.

2. **The contract "Exact wording" reconciliation can use either approach — update the text or relabel the heading.** Both achieve internal consistency. What must be preserved: the contract and SKILL.md must not contradict each other on what the integration block contains.
