# Integration Review — Revision 1

**Reviewer**: integration
**Date**: 2026-03-20
**Revision**: 1 (post cross-review)

---

### Recommendation Dispositions

**Recommendation 1: Fix example path references (P1)**
**Disposition**: Modified

My original recommendation framed this as an open question — "determine the correct location for the example artifacts." Both the compliance cross-review and the scope-boundary cross-review correctly pointed out that the artifacts exist at `specs/010-antipattern-steering/examples/redundant-cache/` (confirmed by filesystem inspection: the directory contains `README.md`, `STATUS.md`, `deliberations/`, and `specs/`). The `001` prefix is a propagated typo, not a missing-artifact problem. I verified this independently — `specs/001-antipattern-steering/` does not exist, and `specs/010-antipattern-steering/examples/redundant-cache/` does.

**Revised recommendation**: Replace `001` with `010` in all referencing files. This is a find-and-replace, not an investigation. The affected files remain the same six I originally identified: `catalog.md` L33, `tasks.md` L38 and L77, `quickstart.md` L15 and L47, and `plan.md` L63. Priority remains P1.

Credit: compliance's cross-review (Dangerous Contradictions, item 1) and scope-boundary's cross-review (Dangerous Contradictions, item 1) both identified the specific correct path with filesystem evidence.

---

**Recommendation 2: Resolve STATUS.md contradiction in constitution (P1)**
**Disposition**: Modified

My original recommendation proposed amending Principle IV directly — removing or qualifying the STATUS.md mandate. Scope-boundary's cross-review raised a legitimate objection: spec 010 did not authorize constitution amendments beyond adding the Known Antipatterns reference section. Modifying a constitutional principle is a governance action that, per the constitution's own amendment rules (L201-202), requires documentation of change, rationale, and impact. A full rewrite of Principle IV would exceed spec 010's scope (spec.md L109 limits integration points to "SKILL.md or templates").

However, scope-boundary's proposed P2 deferral is too permissive. The contradiction is live: constitution L196-199 establishes that "the constitution governs unless the spec explicitly documents and justifies the deviation." Since the catalog entry does not document such a deviation, agents following governance rules will maintain STATUS.md despite the catalog warning against it. This defeats the antipattern system on its very first entry.

**Revised recommendation**: Add a qualifying inline note to Principle IV's STATUS.md bullet — for example: "STATUS.md MUST be updated when any spec's implementation or acceptance status changes, unless this practice is identified as an antipattern in `antipatterns/catalog.md` (see `redundant-cache`)." This is additive (consistent with Principle III: backward-compatible extension), stays within the scope of what spec 010's constitution integration task (T006) was meant to achieve, and neutralizes the contradiction without a full principle rewrite. A separate follow-up spec should handle the full Principle IV revision if the project decides STATUS.md maintenance should be permanently retired. Priority remains P1, but the scope of the fix is narrowed from "rewrite" to "qualify with cross-reference."

Credit: scope-boundary's cross-review (Dangerous Contradictions, item 2) identified the scope concern. Compliance's cross-review (Tensions, item 1) confirmed P1 priority was correct but noted the need for a version bump.

---

**Recommendation 3: Update contract to reflect extended step 2 (P2)**
**Disposition**: Surviving

Both cross-reviews handled this differently. Compliance's cross-review acknowledged the divergence should be addressed (Dangerous Contradictions, item 2: "Integration is correct that a document labeled 'Exact wording' should match the actual file"). Scope-boundary's cross-review agreed integration had the stronger position (Tensions, item 2: "If the contract claims 'Exact wording' and the actual wording differs, that is a contract violation regardless of whether the divergence is beneficial").

No cross-review argued this recommendation was wrong. The options remain: update the contract's step 2 to match SKILL.md, or relabel "Exact wording" as "Minimum wording" to permit additive extensions. Priority remains P2.

---

**Recommendation 4: Add Maintenance section to contract template (P2)**
**Disposition**: Surviving

Compliance's cross-review (Tensions, item 3) confirmed this is a legitimate gap: "Integration sees a structural gap in the contract (something exists in the catalog that the contract does not define)." Scope-boundary's cross-review acknowledged the concern (Tensions, item 3: "the contract's claim to define 'the exact structure' (L7) without including the Maintenance section is a gap integration correctly identified"). Neither cross-review challenged the substance of this recommendation. Priority remains P2.

---

**Recommendation 5: Add disambiguation for Maintenance heading (P2)**
**Disposition**: Modified (downgraded to P3)

Compliance's cross-review (Tensions, item 3) characterized the disambiguating sentinel comment as "a reasonable P3 enhancement but not a prerequisite for shipping." Scope-boundary's cross-review did not challenge the substance but implicitly treated it as lower priority than the contract-level fix (recommendation 4). At the current catalog size (one entry), the risk of a retrieval mechanism misidentifying the Maintenance heading as an entry is theoretical. The concern becomes practical only when automated keyword retrieval is implemented and the catalog has enough entries to warrant programmatic parsing.

**Revised recommendation**: Downgrade to P3. The fix is still valid — a sentinel comment like `<!-- CATALOG:ENTRIES_END -->` would prevent false positives in future retrieval — but it is not needed until keyword retrieval tooling is built.

---

**Recommendation 6: Mark T011 incomplete (P2)**
**Disposition**: Modified (combined with compliance's recommendation)

Compliance's cross-review (Tensions, item 2) correctly identified that my recommendation alone is insufficient: "Unchecking T011 treats the problem as incomplete work. Marking it as 'Fail' and strengthening the validation criteria treats the problem as a process deficiency." Compliance recommends adding explicit path-existence validation to T011's definition. Both actions are needed.

**Revised recommendation**: (1) Uncheck T011 (`[ ]`), (2) amend T011's description to require filesystem path verification (not just reading the path string), and (3) re-execute validation after the path typo is fixed (recommendation 1). Only re-check T011 when the path resolves to an existing directory. Priority remains P2, but the recommendation is now a compound action.

Credit: compliance's cross-review (Tensions, item 2) identified the process deficiency that my original recommendation left unaddressed.

---

**Recommendation 7: Add catalog self-reference to format contract (P3)**
**Disposition**: Surviving

Compliance's cross-review (Tensions, item 5) characterized this as a trade-off between minimalism and discoverability and agreed it should remain P3. No cross-review challenged the substance. The recommendation stands: add an HTML comment footer to `antipatterns/catalog.md` referencing the governing contract at `specs/010-antipattern-steering/contracts/catalog-format.md`.

---

**Recommendation 8: Verify constitution version bump requirement (P3)**
**Disposition**: Modified (elevated to P2, tied to recommendation 2)

Compliance's cross-review (Tensions, item 1) explicitly noted that "the amendment without the version bump would itself violate the constitution's governance section." Scope-boundary's cross-review (Tensions, item 4) confirmed the version bump is required: "Adding a Known Antipatterns section (L179-192) is a material expansion." The constitution was modified (Known Antipatterns section added at L179-192) but the version remains 1.1.0 (L208). Per L203, MINOR bumps are required for "new principles or material expansions." Adding a new section with a MUST-level instruction ("Agents MUST check the antipattern catalog") qualifies as a material expansion.

**Revised recommendation**: Bump the constitution version from 1.1.0 to 1.2.0 and update the Sync Impact Report (L1-16) to document the Known Antipatterns section addition and the Principle IV qualification. This should be executed alongside recommendation 2, not deferred. Priority elevated to P2.

Credit: compliance's cross-review (Tensions, item 1) identified the version bump as a necessary corollary.

---

### New Recommendations

**N1. Verify the full blast radius of the `001` typo via grep (P1)**

Both compliance and scope-boundary identified fewer affected files than my original review. My review found six files; compliance found three locations in tasks.md; scope-boundary found the catalog plus two tasks.md references. To ensure no references are missed when applying the fix, run a grep for `001-antipattern-steering` across the entire conversus directory before executing the find-and-replace. This prevents partial fixes where some files are updated and others retain the broken path.

Credit: compliance's cross-review (Tensions, item 3) noted the discrepancy in affected file counts and recommended a comprehensive grep.

**N2. Address T006 scope traceability gap (P3)**

Scope-boundary's review (Missed Opportunities, bullet 3) flagged that T006 (constitution Known Antipatterns update) lacks spec-level traceability — spec.md L109 only mentions "SKILL.md or templates" as integration points, but the implementation added a constitution section. My original review treated this as a positive integration point without questioning its authorization. Scope-boundary is correct that the traceability gap exists, even though the constitution update is functionally sound. The fix is lightweight: add a note to spec.md's Assumptions section acknowledging `.specify/memory/constitution.md` as an integration point, or add the constitution reference to the spec's list of integration targets.

Credit: scope-boundary's cross-review (Tensions, item 1) and original review (Missed Opportunities, bullet 3) identified this gap.

---

### Position Summary

The cross-review process narrowed two of my findings and strengthened four others. The most significant correction is to recommendation 1: the example path is not a missing-artifact mystery but a simple `001` to `010` typo, confirmed by both other reviewers via filesystem inspection. I verified this independently and accept their position fully. My original framing wasted remediation energy by suggesting investigation where a find-and-replace suffices.

The STATUS.md contradiction (recommendation 2) remains the most architecturally significant finding. All three reviewers agree the contradiction exists and is harmful. The cross-reviews refined the remediation: scope-boundary correctly identified that a full Principle IV rewrite exceeds spec 010's authorized scope, while compliance correctly insisted on P1 priority. My revised position synthesizes both constraints — a qualifying inline note that neutralizes the contradiction without a governance-level principle rewrite, paired with the version bump that the constitution's own rules require for material expansions. This respects scope boundaries while preventing agents from receiving contradictory MUST-level instructions.

The remaining recommendations — contract step 2 update (R3), Maintenance section in contract (R4), T011 compound fix (R6), and catalog self-reference (R7) — survived cross-review scrutiny without substantive challenge. The Maintenance heading disambiguation (R5) was correctly downgraded from P2 to P3 as a theoretical concern at current catalog scale. The new recommendations (N1: grep verification before fix, N2: T006 traceability) emerged directly from cross-review tensions and fill gaps my original review overlooked.
