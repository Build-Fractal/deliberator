# Scope-Boundary Revision: Spec 010 — Agent Antipattern Steering

**Reviewer**: scope-boundary
**Revision**: 1
**Date**: 2026-03-20

---

### Recommendation Dispositions

**Recommendation 1 — Fix broken example path (P1)**
**Disposition**: Surviving

Both cross-reviews (compliance and integration) independently confirmed this as the highest-priority factual defect. The compliance cross-review validated my specific path fix (`specs/010-antipattern-steering/examples/redundant-cache/`) over integration's more open-ended "determine the correct location" recommendation. No cross-reviewer challenged the P1 classification or the rationale grounded in FR-004 and SC-004. The fix is mechanical and unambiguous.

However, I accept integration's observation (Tensions, "Broken path — same diagnosis, different scope of fix") that my original fix scope was incomplete. I identified 3 affected locations (catalog.md, tasks.md T003, tasks.md T011); integration identified 6 locations (adding quickstart.md twice and plan.md). The comprehensive fix should cover all 6 locations. I originally focused on runtime and implementation-record artifacts but understated the propagation into design documents. Updating all references is the correct approach, since these documents serve as the implementation record and future verification checklists.

**Recommendation 2 — Acknowledge constitution Principle IV tension (P2)**
**Disposition**: Modified

Both cross-reviews challenged my P2 classification. Compliance rated this P1 and proposed direct amendment of Principle IV. Integration also rated it P1 and proposed amending Principle IV before shipping.

I withdraw my P2 classification and upgrade to P1 — but I defend my proposed intervention scope. Here is the reasoning:

The compliance cross-review correctly identified that the constitution's Governance section (L196-199) creates a formal precedence rule: "This constitution supersedes conflicting guidance in individual specs or agent prompts." This means an agent encountering both Principle IV's STATUS.md MUST mandate and the redundant-cache antipattern will follow Principle IV, rendering the antipattern functionally inert against its primary target. Integration's cross-review reinforced this with the same governance citation. The compliance cross-review of my work explicitly called this out: the antipattern becomes "effectively dead letter" if Principle IV stands unqualified.

I was wrong about the urgency. The contradiction is not a future concern to be deferred — it is an active conflict that will produce contradictory agent behavior the first time an agent encounters both documents.

However, I maintain that a full rewrite or removal of Principle IV is outside spec 010's scope. Constitution L201-202 requires that amendments include "documentation of the change, rationale, and impact on existing specs," and Principle I itself requires behavioral changes to start with a specification. The compliance cross-review's own suggested resolution (in the Dangerous Contradictions section) arrived at the same middle ground I defend: "create a follow-up spec whose explicit scope is to amend Principle IV, combined with an interim note in the Known Antipatterns section acknowledging the conflict."

**Modified recommendation**: Add a qualifying inline note to Principle IV — e.g., appending to the STATUS.md bullet: "See `redundant-cache` in `antipatterns/catalog.md` for guidance on when STATUS.md maintenance is counterproductive." This neutralizes the contradiction for agents without removing the principle, stays within additive scope, and is consistent with the integration cross-review's suggested resolution. Elevate to P1. File a follow-up spec for full Principle IV reconciliation.

**Recommendation 3 — Add spec traceability for constitution update T006 (P2)**
**Disposition**: Surviving

The compliance cross-review treated T006 as fully satisfied without noting the traceability gap. The integration cross-review treated T006 as a positive integration point (Alignment, bullet 5) and did not flag it as over-scope. Both cross-reviews of my position agreed the finding is valid but suggested different handling.

The compliance cross-review of my work (Dangerous Contradictions, "T006 traceability") explicitly endorsed my position: "scope-boundary is correct on the traceability point — the spec does not list constitution.md as an integration point, so T006 lacks formal spec coverage." It recommended noting T006 as "implemented correctly but with a spec traceability gap" and adding constitution.md to the spec's Assumptions.

The integration cross-review (Tensions, "Scope of T006") called both positions defensible and recommended recording the traceability gap even if no code change is needed.

I survive this recommendation with no modification. The implementation is correct; the gap is formal. Adding constitution.md to the spec's Assumptions section is a one-line additive change that closes the gap.

**Recommendation 4 — Fix path reference in tasks.md T003 and T011 (P2)**
**Disposition**: Modified (merged with Recommendation 1)

The integration cross-review (Tensions, "T011 validation status") raised an important nuance: fixing the path in T011 and leaving it checked `[x]` implies the validation passed against the corrected path, which is historically inaccurate. Integration recommended unchecking T011 to preserve the audit record that validation was not actually performed against a valid path.

I concede this is a valid concern. My original recommendation was forward-looking ("fix and move on"), but integration's audit-preserving approach is more disciplined. The T011 checkbox should be unchecked after the path is corrected, with a note that re-validation is needed.

**Modified recommendation**: Fix the path reference in T003 and T011 (as originally recommended), AND uncheck T011's completion box to reflect that its validation condition was never actually met. This merges the path fix (Recommendation 1's comprehensive scope) with integration's audit integrity concern.

**Recommendation 5 — Verify Summary Index keyword-to-entry consistency on future additions (P2)**
**Disposition**: Modified

The compliance cross-review (Tensions, "Summary Index keyword-sync durability") noted that compliance wants a broader field-validation checklist while I want a keyword-specific sync reminder, and recommended a single consolidated Maintenance checklist covering both concerns.

I accept the consolidation. A single Maintenance checklist item covering both keyword sync and field-count validation is better than two overlapping additions.

**Modified recommendation**: Add a consolidated verification bullet to the Maintenance section: "When adding a new entry, verify: (a) Keywords in the Summary Index row exactly match the entry's Keywords section, (b) all required fields are present per the contract in `specs/010-antipattern-steering/contracts/catalog-format.md`."

**Recommendation 6 — Confirm no template changes were made (P3)**
**Disposition**: Surviving

No cross-reviewer challenged this. It is a confirmation, not a change request. Both compliance and integration independently verified the same finding: no templates were modified. This remains a passed verification checkpoint.

**Recommendation 7 — Add explicit scope-boundary note about phase execution (P3)**
**Disposition**: Withdrawn

Neither cross-review mentioned or supported this recommendation. On reflection, this was overly cautious. The implementation is clean, the SKILL.md change is clearly bounded by its own H3 heading, and adding an explicit checkpoint against accidental bleed into adjacent content is solving a problem that does not exist. The existing task structure (T010 validating FRs, T011 validating cross-references) provides sufficient guardrails. I was projecting a risk that the implementation itself does not exhibit.

---

### New Recommendations

**N1. Update the contract's SKILL.md Integration "Exact wording" to match actual SKILL.md** (Priority: P2)
Source: integration cross-review (Tensions, "Contract 'Exact wording' divergence"), acknowledged in my cross-review of integration (Tensions, item 2, "integration has the stronger position here").

The contract at catalog-format.md L91 states "Exact wording" for the SKILL.md integration block. The actual SKILL.md step 2 (L205) includes keyword retrieval guidance added by T008 that is not present in the contract's "Exact wording" block. I should have caught this in my original review — it is the same type of internal consistency issue as the T006 traceability gap. The fix: either update the contract's step 2 to match SKILL.md, or replace "Exact wording" with "Minimum required content."

**N2. Bump constitution version from 1.1.0 to 1.2.0** (Priority: P3)
Source: integration cross-review (Tensions, "Constitution version bump"), acknowledged in my cross-review of integration (Tensions, item 4).

The constitution's Governance section (L203) specifies MINOR version bumps for "new principles or material expansions." Adding the Known Antipatterns section (L179-192) is a material expansion. The version at L208 still reads 1.1.0. This is a corollary of accepting T006 as in-scope — if the constitution was legitimately updated, the update must follow the constitution's own governance rules, including versioning. I should have identified this inconsistency as evidence that the constitution update was not fully thought through in the plan.

---

### Position Summary

The implementation of spec 010 is well-bounded and additive. All P1 and P2 functional requirements are implemented. The catalog contains exactly one seed entry conforming to the data model and contract. The SKILL.md change is a pure insertion. No templates, phase execution logic, or existing behavioral contracts were modified beyond the intended scope. The single factual error — a broken example path propagated from early design documents into the catalog entry — is mechanical to fix and does not reflect a deeper design problem.

My most significant revision is upgrading the constitution Principle IV tension from P2 to P1. Both cross-reviewers independently demonstrated, through the Governance precedence clause (L196-199), that the unqualified STATUS.md MUST mandate in Principle IV formally overrides the antipattern catalog's guidance — making the system's foundational entry functionally inert against its primary target. I was correct that a full constitutional amendment is outside spec 010's scope, but I was wrong to treat the contradiction as deferrable. The compromise is an additive qualifying note within Principle IV that reconciles the two documents for agents, combined with a follow-up spec for full resolution. This preserves scope discipline while neutralizing the active conflict.

I also acknowledge two gaps in my original review that the cross-reviews exposed: I missed the contract's "Exact wording" divergence from the actual SKILL.md content (flagged by integration), and I missed the constitution version bump requirement (also flagged by integration). Both are legitimate findings that my scope-boundary lens should have caught, since they represent internal consistency failures between artifacts that define the implementation boundary. My original review was thorough on spec-to-implementation traceability but insufficiently attentive to contract-to-implementation and governance-to-implementation consistency.
