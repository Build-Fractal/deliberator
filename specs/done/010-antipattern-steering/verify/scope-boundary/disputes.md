# Scope-Boundary Disputes: Spec 010 — Agent Antipattern Steering

**Reviewer**: scope-boundary
**Phase**: Final (Phase 4 — Disputes)
**Date**: 2026-03-20

---

## Remaining Disputes

### Dispute 1: Constitution Principle IV — Inline Qualification vs. Follow-Up Spec

All three agents now agree on: (a) the contradiction is real, (b) Principle IV's governance precedence renders the `redundant-cache` antipattern functionally inert, and (c) a full rewrite of Principle IV exceeds spec 010's authorized scope. What remains disputed is the appropriate remediation within spec 010.

**Integration's position** (revision R2): Add a qualifying inline note to Principle IV's STATUS.md bullet — e.g., "unless this practice is identified as an antipattern in `antipatterns/catalog.md`." Integration classifies this as P1 and frames it as additive, consistent with Principle III.

**My position**: This remediation is still a constitutional amendment. Adding a conditional clause to a MUST-level instruction changes that instruction's semantics. It is additive in the git-diff sense but substantive in the governance sense. The constitution's own amendment process (L201-202) requires "documentation of the change, rationale, and impact on existing specs." Integration's proposed inline note satisfies none of these procedural requirements.

I accept P1 urgency. But the correct P1 action within spec 010's scope is: (1) add a note to the Known Antipatterns section (L179-192) explicitly acknowledging the Principle IV conflict — "Note: Principle IV's STATUS.md mandate predates this catalog entry. Agents encountering both should follow the catalog correction until a formal amendment reconciles the two documents." (2) File the follow-up spec immediately. This gives agents a documented resolution path without performing an unauthorized amendment to a constitutional principle.

The difference is narrow but principled: integration modifies Principle IV's operative text; I modify only the Known Antipatterns section that spec 010 already authorized. Both neutralize the contradiction for agents. Mine does so without touching a constitutional principle outside the spec's scope boundary.

### Dispute 2: Constitution Version Bump — P2 vs. P3

Integration elevated the version bump from P3 to P2 and tied it to the Principle IV fix. Compliance did not explicitly prioritize it. I originally classified it P3.

I maintain P3. The version bump is a mechanical governance housekeeping item. It does not affect agent behavior, does not block any functional requirement, and does not create a contradiction. It is a compliance gap in the constitution's own self-governance — real but not urgent. Tying it to the Principle IV remediation (as integration proposes) creates an artificial dependency: if the Principle IV fix is deferred to a follow-up spec, the version bump becomes part of that follow-up, not part of spec 010. If the Known Antipatterns section addition is the only constitutional change (as I propose), it still warrants a version bump, but it is a bookkeeping fix that can be applied alongside any of the other P2/P3 items without blocking anything.

Classification matters because it determines whether the version bump gates the "spec complete" verdict. It should not.

---

## Convergence

### 1. Broken Example Path (P1)

All three agents agree: replace `001-antipattern-steering` with `010-antipattern-steering` across all referencing files. The affected files are catalog.md, tasks.md (T003, T011), quickstart.md, and plan.md. A grep for `001-antipattern-steering` across the conversus directory is the correct method to identify the definitive list. This is the single unambiguous P1 blocking defect.

### 2. T011 Must Be Unchecked and Re-Validated

All three agents converged on the compound action: (1) uncheck T011, (2) amend T011's description to require filesystem path verification, (3) fix the broken path, (4) re-execute validation and only recheck when all paths resolve. Integration originated the unchecking recommendation; compliance added the process-improvement dimension; I concurred in revision. No remaining disagreement.

### 3. Contract "Exact Wording" Divergence (P2)

All three agents agree that the contract's SKILL.md Integration section (catalog-format.md L91) claims "Exact wording" but the actual SKILL.md step 2 (L205) includes keyword retrieval guidance from T008 not present in the contract. The fix is either to update the contract text to match SKILL.md or to relabel "Exact wording" as "Minimum required content." I missed this in my original review and accept it as a legitimate scope-consistency finding.

### 4. T006 Spec Traceability Gap (P3)

All three agents acknowledge that T006 (constitution Known Antipatterns update) has no formal grounding in spec.md's listed integration points (L109: "SKILL.md or templates"). The implementation is correct and useful, but the spec-to-task traceability is incomplete. The fix is additive: note constitution.md as an integration target in the spec's Assumptions section. No disagreement on substance, only on whether this is worth noting (all agree it is).

### 5. Catalog Maintenance Checklist Consolidation (P3)

Compliance proposed field-count validation; I proposed keyword-sync verification. All agents converged on a single consolidated checklist in the catalog's Maintenance section covering both concerns, with the contract (catalog-format.md) as the single source of truth for structural validation rules.

---

## Final Position Statement

### Non-Negotiables

1. **The broken example path is the only P1 blocking defect that spec 010 can fix directly.** All other P1-classified items involve artifacts outside spec 010's authorized scope boundary (constitution Principle IV operative text). Acknowledging conflicts is in-scope; amending principles is not.

2. **Constitution Principle IV's operative text must not be modified within spec 010's implementation.** The Known Antipatterns section (which spec 010 created) is the appropriate location for conflict acknowledgment. Modifying a MUST-level constitutional instruction requires the constitution's own amendment process — documentation, rationale, impact analysis, and a version bump — which is a follow-up spec, not an inline patch during verification.

3. **T011 must be unchecked.** A checked validation task that references a nonexistent path is a false attestation. The checkbox must reflect actual validation state, not aspirational completion.

### Flexibility

- **Principle IV inline qualification**: If the synthesizer determines that integration's additive inline note (appending a cross-reference to the STATUS.md bullet) is sufficiently narrow to not constitute a "principle redefinition" under the constitution's versioning rules, I will not block it. My concern is procedural discipline, not the text of the qualification. If the synthesizer rules that a cross-reference append is PATCH-level (L204: "clarifications"), that resolves the scope objection.

- **Version bump priority**: I classified P3; integration classified P2. Either is defensible. I defer to the synthesizer on whether it gates spec completion.

- **Contract update mechanism**: Whether the fix is updating the contract's step 2 text or relabeling "Exact wording" to "Minimum required content" is a style choice. Both resolve the divergence. I have no preference between them.

- **Design-phase document path fixes**: Compliance suggested treating plan.md and research.md path references as "known errata" without mandatory fixes. Integration included them in the comprehensive fix list. I am fine with either approach — the runtime artifacts (catalog.md, tasks.md, SKILL.md) are what agents consume; design documents are historical records.
