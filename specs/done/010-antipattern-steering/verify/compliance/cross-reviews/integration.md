# Cross-Review: integration's Review from compliance's Perspective

**Cross-reviewer**: compliance
**Reviewing**: integration's Phase 1 review
**Date**: 2026-03-20

---

### Dangerous Contradictions

- **Example path: typo correction vs. missing artifacts**
  - **integration claims**: The example path `specs/001-antipattern-steering/examples/redundant-cache/` "does not exist on disk" and "either the numbering convention changed, the example directory was never created, or it was placed elsewhere." Integration frames this as an open question requiring determination of the "correct location" (Actionable Recommendations #1, Off-Base Assumptions #1).
  - **compliance claims**: The correct path is `specs/010-antipattern-steering/examples/redundant-cache/` and the artifacts exist there. The `001` is a propagated typo, not a missing-artifact problem (Off-Base Assumptions, second item; Actionable Recommendations #1: "The actual artifacts exist at `specs/010-antipattern-steering/examples/redundant-cache/` (confirmed by filesystem inspection)").
  - **Why this is dangerous**: If integration's recommendation is adopted as-is ("determine the correct location"), it introduces unnecessary investigation work and risks creating duplicate artifacts or restructuring the path. If compliance's recommendation is adopted ("change `001` to `010`"), the fix is a straightforward find-and-replace. But if the synthesizer treats these as the same finding without resolving the ambiguity, the remediation action could be misdirected -- someone might create a `specs/001-antipattern-steering/` directory to make the references valid, rather than correcting the references.
  - **Suggested resolution**: Compliance's position should govern here because it includes filesystem verification evidence. The fix is to replace `001` with `010` in all six referencing files. Integration's recommendation #1 should be narrowed from "determine the correct location" to "correct the path prefix from `001` to `010`."

- **Scope of contract "exact wording" divergence**
  - **integration claims**: The contract (catalog-format.md L91) specifies "Exact wording" for the SKILL.md integration block, and SKILL.md step 2 diverges from this wording. Integration recommends updating the contract to match SKILL.md, framing this as a blocking consistency issue (Missed Opportunities, second item; Actionable Recommendations #3, Priority P2).
  - **compliance claims**: Compliance's review notes FR-006 and FR-008 as implemented, with step 2 "enhanced with keyword filtering for >10 entries" (Requirement Verification Matrix, FR-006 row). Compliance does not flag the contract-vs-SKILL.md wording divergence as an issue -- it is treated as an expected enhancement per T008.
  - **Why this is dangerous**: These two positions produce different remediation actions. Integration says the contract must be updated (a new change required). Compliance says no change is needed (the enhancement is within scope). If both positions coexist without resolution, a future implementer reading the contract will either (a) follow the outdated exact wording and regress SKILL.md, or (b) follow SKILL.md and assume the contract is advisory. Neither outcome is clean.
  - **Suggested resolution**: Integration is correct that a document labeled "Exact wording" should match the actual file. Compliance should acknowledge this gap. The contract's step 2 should be updated to match SKILL.md, or the "Exact wording" label should be softened to "Minimum wording" to permit additive extensions. This is a P2 fix -- it does not block shipping but should be tracked.

- **No additional contradictions identified.** The remaining positions from both reviews are either aligned or create tensions (addressed below) rather than direct contradictions.

---

### Tensions

- **Severity of the STATUS.md constitution contradiction**
  - **integration's position**: Frames the contradiction as a P1 blocking integration failure requiring constitution amendment before shipping. Proposes three specific amendment options and notes a version bump to 1.2.0 is required (Actionable Recommendations #2, #8; Missed Opportunities, fourth item).
  - **compliance's position**: Also flags this as P1 and proposes amending Principle IV with specific replacement language. Does not mention the version bump requirement (Actionable Recommendations #2).
  - **Nature of tension**: Both reviews agree this is P1, but they differ on the scope of the fix. Integration treats this as a two-part change (amend principle + bump version), while compliance treats it as a single content change. Integration's approach is more procedurally complete but adds a dependency on constitution governance mechanics. Compliance's approach is more surgical but risks violating the constitution's own versioning rules (L203: MINOR for material expansions).
  - **Coordination needed**: The synthesizer should adopt integration's position on the version bump as an additional requirement alongside compliance's proposed amendment language. Both are needed -- the amendment without the version bump would itself violate the constitution's governance section.

- **T011 disposition: fail vs. uncheck**
  - **integration's position**: Recommends marking T011 incomplete (`[ ]`) "until the example path issue is resolved" (Actionable Recommendations #6, Priority P2).
  - **compliance's position**: Marks T011 as "Fail" in the Task Completion Verification table and recommends adding explicit path-existence validation to T011's definition (Actionable Recommendations #3, Priority P1; Task Completion Verification table, T011 row).
  - **Nature of tension**: These are different remediation strategies. Unchecking T011 treats the problem as incomplete work. Marking it as "Fail" and strengthening the validation criteria treats the problem as a process deficiency. Integration's approach fixes the symptom (incorrect checkbox). Compliance's approach fixes the root cause (insufficient validation criteria) and the symptom (the broken path).
  - **Coordination needed**: Both actions should be taken: uncheck T011 (integration's recommendation) AND add path-existence validation to T011's definition (compliance's recommendation). The synthesizer should combine these as a single compound recommendation.

- **Maintenance section contract gap: structural vs. disambiguating**
  - **integration's position**: Raises two related concerns -- (1) the contract template does not include a Maintenance section (Actionable Recommendations #4, P2) and (2) the Maintenance H2 heading is indistinguishable from entry H2 headings (Actionable Recommendations #5, P2; Missed Opportunities, third and seventh items).
  - **compliance's position**: Does not flag the Maintenance section omission from the contract or the heading-level ambiguity. Compliance focuses on field-level validation within entries (Actionable Recommendations #7, P3).
  - **Nature of tension**: Integration sees a structural gap in the contract (something exists in the catalog that the contract does not define). Compliance sees a validation gap in the maintenance procedure (the procedure lacks a machine-checkable format). These are different layers of the same problem: the Maintenance section is under-specified both in the contract and in its own content.
  - **Coordination needed**: Integration's contract-level fix (add Maintenance section to the contract template) should be adopted as the primary recommendation. Compliance's field-checklist recommendation can be folded into that contract addition. The disambiguating sentinel comment (integration's recommendation #5) is a reasonable P3 enhancement but not a prerequisite for shipping.

- **Success criteria measurability**
  - **integration's position**: Does not explicitly address SC-001 or SC-002 measurability. The review focuses on integration surface consistency rather than success criteria testability.
  - **compliance's position**: Flags SC-001 as "Not measurable" (no detection mechanism), SC-002 as "Not measurable" (no timing instrumentation), and SC-003 as "Not testable at current scale" (Requirement Verification Matrix; Actionable Recommendations #5, #6).
  - **Nature of tension**: These are complementary rather than conflicting perspectives, but they create a tension about what "done" means. Integration implicitly treats the spec as shippable if integration surfaces are consistent. Compliance explicitly notes that three of four success criteria cannot currently be verified, which raises the question of whether the spec can be declared complete.
  - **Coordination needed**: The synthesizer should distinguish between "implementation complete" (integration's lens) and "success criteria verifiable" (compliance's lens). SC-001 and SC-002 should be acknowledged as aspirational bounds in the final synthesis without blocking the spec's completion. SC-004 is the one that must be fully satisfied before shipping.

- **Catalog self-reference and traceability**
  - **integration's position**: Notes that the catalog does not reference the governing spec (Missed Opportunities, fifth item; Actionable Recommendations #7, P3). Proposes adding an HTML comment footer.
  - **compliance's position**: Does not raise this issue. Compliance verifies the constitution references the catalog (Task Completion Verification, T006 row) but does not check the reverse direction.
  - **Nature of tension**: Integration values bidirectional traceability (catalog points to its own governing spec). Compliance is satisfied with unidirectional traceability (constitution and SKILL.md point to catalog). Neither is wrong -- this is a trade-off between minimalism (compliance) and discoverability (integration).
  - **Coordination needed**: This should remain a P3 recommendation. The catalog's purpose is to be read by agents, not to serve as a specification governance artifact. An HTML comment is low-cost and does not clutter the agent-facing content.

---

### Safe Agreements

- **Broken example path is a P1 blocker**
  - **Shared position**: Both reviews identify the `specs/001-antipattern-steering/examples/redundant-cache/` reference as a critical defect. Integration flags it as a "blocking integration failure" (Executive Summary, Missed Opportunities first item, Off-Base Assumptions first item). Compliance flags it as a P1 recommendation and marks FR-002, T003, T010, T011, and SC-004 as partially or fully failed due to this path (Requirement Verification Matrix; Task Completion Verification; Catalog Entry Field Validation, Example row).
  - **Combined evidence**: Integration provides breadth -- identifying six files that reference the broken path (catalog.md, tasks.md x2, quickstart.md x2, plan.md). Compliance provides depth -- tracing the impact through FR-002 ("Partially implemented"), SC-004 ("Partially satisfied"), and three task failures. Together, these establish that the broken path affects both the user-facing catalog and the implementation tracking infrastructure.
  - **Confidence level**: High. This is the single most well-evidenced finding across both reviews and should be the first remediation item in the synthesis.

- **STATUS.md constitution contradiction is a P1 blocker**
  - **Shared position**: Both reviews identify the contradiction between constitution Principle IV (L73-75, mandating STATUS.md) and the `redundant-cache` antipattern (catalog.md L22-33, condemning STATUS.md). Integration frames it as agents receiving "contradictory MUST-level instructions" (Executive Summary, Missed Opportunities fourth item). Compliance frames it as the constitution overriding the catalog per governance precedence rules (Off-Base Assumptions first item; Actionable Recommendations #2).
  - **Combined evidence**: Both reviews cite the constitution's governance section (L196-199) establishing that the constitution takes precedence. This means the antipattern entry is effectively dead letter -- agents following governance rules will maintain STATUS.md despite the catalog warning against it. Integration adds the version-bump requirement (L203). Compliance adds specific replacement language for Principle IV. Together, these provide both the rationale for the fix and the implementation path.
  - **Confidence level**: High. This is the second most important finding and both reviews converge on the same priority, diagnosis, and remediation direction.

- **Catalog entry format conformance is complete (modulo Example path)**
  - **Shared position**: Both reviews confirm that the `redundant-cache` entry follows the contract's field order and includes all required fields. Integration verifies field order and naming (Alignment, fourth item: "follows the contract's field order exactly"). Compliance verifies individual field validation constraints (Catalog Entry Field Validation table: all fields pass except Example).
  - **Combined evidence**: Integration checks structural conformance (correct H2/H3 hierarchy, correct section ordering). Compliance checks data validation (Symptoms >= 2 items, Keywords >= 2 tags, Summary < 100 chars). Together, these confirm both the shape and the content quality of the entry.
  - **Confidence level**: High. The entry is well-formed. The only defect is the Example path, which is a reference error, not a structural or content quality issue.

- **SKILL.md integration is correctly positioned and functional**
  - **Shared position**: Both reviews confirm that the Antipattern Check section in SKILL.md is correctly placed (after Step 1 / config parsing, before Step 2 / output directory creation), references the correct catalog path, and preserves the 4-step workflow. Integration confirms this in Alignment items one, two, and five. Compliance confirms it in the FR-005 and FR-006 rows of the Requirement Verification Matrix.
  - **Combined evidence**: Integration verifies path consistency across three files (SKILL.md, constitution, catalog). Compliance verifies the instruction satisfies two functional requirements (FR-005, FR-006). The only divergence is whether step 2's keyword extension needs contract reconciliation (see Tensions above), which is a contract-level concern, not a functional one.
  - **Confidence level**: High. The agent-facing integration surface works as designed.

---

### Referenced Documentation

- **integration's review**: `/Users/business-daddy/code/payer-index-mono/conversus/specs/010-antipattern-steering/verify/integration/review.md`
- **compliance's review**: `/Users/business-daddy/code/payer-index-mono/conversus/specs/010-antipattern-steering/verify/compliance/review.md`
- `specs/010-antipattern-steering/spec.md` -- L69-87 (FRs), L99-102 (SCs), L107 (assumptions)
- `specs/010-antipattern-steering/data-model.md` -- L33 (bidirectional sync), L56 (example validation), L72-73 (keyword tags)
- `specs/010-antipattern-steering/contracts/catalog-format.md` -- L7 (purpose), L12-59 (template), L77 (example requirement), L89-103 (SKILL.md integration contract), L91 (exact wording)
- `specs/010-antipattern-steering/tasks.md` -- L38 (T003), L52 (T006), L77 (T011)
- `antipatterns/catalog.md` -- L22-33 (redundant-cache entry core), L57-71 (maintenance)
- `SKILL.md` -- L199-207 (Antipattern Check)
- `.specify/memory/constitution.md` -- L73-75 (Principle IV), L179-192 (Known Antipatterns), L196-199 (governance precedence), L203 (versioning)
