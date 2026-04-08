# Integration Disputes — Final Position

**Reviewer**: integration
**Phase**: 4 (disputes)
**Date**: 2026-03-20

---

## Remaining Disputes

### Dispute 1: Constitution Principle IV — inline qualification is necessary now, not deferrable

All three reviewers agree the contradiction between Principle IV's STATUS.md MUST mandate (constitution L73-75) and the `redundant-cache` antipattern entry is real, harmful, and P1. All three revised positions converge on an additive qualifying note rather than a full principle rewrite. This is resolved in direction.

What remains disputed is **whether the qualifying note is within spec 010's authorized scope**. Scope-boundary's revision upgraded this to P1 and proposed the same inline qualification I did — but hedged with "file a follow-up spec for full Principle IV reconciliation." Compliance's revision downgraded to P2 within spec 010's scope and proposed only an acknowledgment note in the Known Antipatterns section, deferring the actual Principle IV modification to a follow-up spec.

I dispute compliance's P2 deferral. An acknowledgment note in the Known Antipatterns section (L179-192) does not neutralize the contradiction — the Governance section (L196-199) explicitly states the constitution supersedes conflicting guidance. An agent reading both documents and following governance rules will resolve the conflict in favor of Principle IV, ignoring the acknowledgment note as informational. The qualifying note must be **on Principle IV itself** (L73-75), not in a downstream section that Governance rules subordinate. This is not a full rewrite — it is a cross-reference addition consistent with Principle III (backward-compatible extension). Task T006 already modified the constitution by adding the Known Antipatterns section; adding a qualifying clause to Principle IV is the same category of additive change.

Scope-boundary's revised position aligns with mine here. The dispute is specifically with compliance's remediation location.

### Dispute 2: Constitution version bump priority — P2, not P3

Scope-boundary's revision classified the version bump (1.1.0 to 1.2.0) as P3. I elevated it to P2 in my revision and tied it to the Principle IV qualification. Compliance did not assign a priority but noted the bump is required.

I maintain P2. The constitution's own governance rules (L203) define MINOR bumps as required for "new principles or material expansions." The Known Antipatterns section (L179-192) contains a MUST-level instruction ("Agents MUST check the antipattern catalog"). A MUST-level behavioral directive is a material expansion by any reasonable reading. Shipping the constitution with a MUST-level addition and no version bump violates the constitution's own versioning contract. This is not cosmetic — it means the constitution's version number is unreliable as an indicator of what an agent should expect, which undermines the versioning system's purpose.

The bump should be executed alongside the Principle IV qualification as a single atomic change.

### Dispute 3: Conversus.yml itself contains the `001` typo

My grep confirmed that `conversus.yml` L57 (the verification configuration file driving this very deliberation) references `specs/001-antipattern-steering/examples/redundant-cache/`. This file was not included in any reviewer's affected-file list during the revision phase, including my own. The total affected file count is **seven**, not six:

1. `catalog.md` L33
2. `tasks.md` L38
3. `tasks.md` L77
4. `quickstart.md` L15
5. `quickstart.md` L47
6. `plan.md` L63
7. `verify/conversus.yml` L57

Additionally, `research.md` L71 contains the same reference, bringing the total to **eight**. My revision's recommendation N1 (grep before fix) would catch these, but the synthesizer should note that the affected-file counts in all three revisions are incomplete.

---

## Convergence

### 1. Broken example path is the single P1 factual defect

All three reviewers independently confirmed: `specs/001-antipattern-steering/` does not exist, `specs/010-antipattern-steering/examples/redundant-cache/` does. The fix is a mechanical find-and-replace across all referencing files. Unanimous P1, unanimous on the nature of the fix (typo, not missing artifact). No dispute remains on this point.

### 2. T011 must be unchecked and re-executed after the path fix

All three revised positions converge on a compound action: uncheck T011, amend its validation criteria to require filesystem path verification, fix the path, then re-validate. Compliance and I arrived at this independently; scope-boundary accepted integration's audit-integrity reasoning in their revision. The sequencing (uncheck first, then fix, then re-validate) is agreed.

### 3. Contract "Exact wording" divergence must be resolved

All three revised positions agree that the contract's SKILL.md Integration section (catalog-format.md L91) claims "Exact wording" but the actual SKILL.md step 2 (L205) includes keyword retrieval guidance not present in the contract. All agree this must be fixed. The two options — update contract text to match SKILL.md, or relabel "Exact wording" as "Minimum wording" — are both acceptable. No dispute on the existence or priority (P2) of this issue.

### 4. T006 traceability gap is real but non-blocking

All three revised positions acknowledge that T006 (constitution Known Antipatterns update) traces to no spec-level requirement — spec.md L109 lists only "SKILL.md or templates" as integration points. The implementation is functionally correct; the gap is formal. Adding constitution.md to the spec's Assumptions section closes it. P3, non-blocking.

### 5. Catalog Maintenance section and validation checklist belong in the contract

All three revised positions converge on the contract (catalog-format.md) as the single source of truth for structural requirements, validation rules, and maintenance procedures. The catalog's Maintenance section should reference the contract rather than duplicating validation constraints. Compliance, scope-boundary, and I all modified our original positions to reach this agreement during the revision phase.

---

## Final Position Statement

### Non-Negotiables

1. **The `001` to `010` path fix must cover all files, verified by grep.** Eight files contain the broken reference. A partial fix leaves the system in a worse state than an unfixed one — some paths resolve, some do not, and future validators cannot distinguish fixed-and-verified references from unfixed ones. The grep must run before any find-and-replace.

2. **The Principle IV qualification must be on Principle IV itself, not in a downstream section.** The constitution's Governance precedence clause (L196-199) means any acknowledgment placed in the Known Antipatterns section is formally subordinate to Principle IV's unqualified MUST. An inline qualifying note on L73-75 — a cross-reference, not a rewrite — is the minimum intervention that actually neutralizes the contradiction for agents following governance rules.

3. **The contract's "Exact wording" label must match reality.** A contract that claims exact correspondence and does not match the implementation is worse than no contract. Either the text is updated or the label is changed. This is an integration integrity requirement — the contract is the authoritative specification for the SKILL.md integration block, and divergence between the two creates a regeneration risk where future implementers regress the T008 enhancement.

4. **T011 must be unchecked before the path is fixed.** The checkbox is a historical claim that validation passed. It did not. Re-checking it after the fix is applied preserves audit integrity. This ordering is non-negotiable for the same reason integration checks exist: cross-references must be verifiably correct, not assumed correct.

### Flexibility

- **Version bump priority**: I maintain P2, but if the synthesizer determines P3 is defensible (because the version number has no runtime consumers today), I will not block on this.
- **Contract Maintenance section format**: Whether the contract defines the Maintenance section as a full template or as a set of validation rules is a design choice I am flexible on. The requirement is that the contract acknowledges and specifies the Maintenance section — the format is negotiable.
- **Plan.md and research.md path fixes**: These are historical design documents. Fixing the path is correct and costs nothing, but if the synthesizer classifies them as errata that do not require remediation, I accept that as defensible — they are not runtime artifacts.
- **Scope-boundary's withdrawn recommendation 7** (explicit phase-execution boundary note): Scope-boundary was right to withdraw this. The implementation is clean and does not exhibit the risk the recommendation was designed to prevent.
