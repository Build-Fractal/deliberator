# Compliance Review — T001: Verify Draft Markers Exist

**Reviewer role**: compliance (spec-compliance auditor verifying FR-001)
**Requirement under review**: FR-001 — Templates winner-take-all/arbitration.md, red-blue/arbitration.md, and prisoners-dilemma/arbitration.md MUST contain `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` as their first line.

---

### Executive Summary

FR-001 requires that three non-cooperative arbitration templates carry the exact draft marker `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` as their first line, and that the cooperative template does NOT carry this marker. This is a safety gate preventing untested game-dynamics templates from being loaded in production runs (spec.md L10-14). The requirement is binary and easily auditable: either the marker is present in the correct position with correct syntax, or it is not.

All three non-cooperative templates pass FR-001 compliance. Each file's first line is the exact string `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` with correct HTML comment syntax, no whitespace prefix, no typos, and no trailing characters. The cooperative template correctly omits the marker — its first line is the heading `# Cooperative Arbitration...`. There are zero compliance violations for FR-001 as currently written. My most important recommendation is to formalize the negative requirement (cooperative template MUST NOT contain the marker) as an explicit functional requirement, since the spec's acceptance scenario 4 tests for it but FR-001 does not mandate it.

### Alignment

- **Draft marker placement** (spec.md L202, FR-001): All three non-cooperative templates place the marker as their literal first line (line 1), matching the "as their first line" requirement exactly. Verified against the template files: `winner-take-all/arbitration.md` L1, `red-blue/arbitration.md` L1, `prisoners-dilemma/arbitration.md` L1. [spec.md, L202]

- **Marker syntax correctness** (spec.md L254): The marker uses standard HTML comment syntax (`<!-- ... -->`), matching the Key Entities definition of "An HTML comment (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`) placed as the first line of templates." No malformed delimiters, no extra spaces inside the comment body, no trailing whitespace. [spec.md, L254]

- **Cooperative template exclusion** (spec.md L23, Acceptance Scenario 4): `cooperative/arbitration.md` begins with `# Cooperative Arbitration — Phase 6: Subject Arbitration` on line 1. No draft marker is present anywhere in the file. This aligns with acceptance scenario 4's expectation that the cooperative template loads normally. [spec.md, L23]

- **Consistency across templates** (spec.md L202): The exact same string is used in all three files — there is no variation in capitalization, spacing, or punctuation. This is important because FR-002 specifies a string match check at engine load time; inconsistent markers would risk bypassing the check. [spec.md, L202-204]

### Missed Opportunities

- **Explicit negative requirement for cooperative template**: FR-001 only states what three templates MUST contain. Acceptance scenario 4 (spec.md L23) tests that the cooperative template does NOT contain the marker, but no FR explicitly mandates this. If someone accidentally adds a draft marker to the cooperative template, FR-001 would still pass while acceptance scenario 4 would fail. A dedicated requirement (e.g., "FR-001a: templates/cooperative/arbitration.md MUST NOT contain the draft marker") would close this gap. [spec.md, L202 vs L23]. Impact: medium.

- **No marker validation for non-arbitration templates**: FR-001 covers only `arbitration.md` in the three non-cooperative directories. If other template files exist in those directories (e.g., review templates, synthesis templates), the spec does not address whether they should also carry draft markers. The spec's scope is explicitly arbitration templates, but a compliance auditor cannot verify completeness without knowing the full template inventory. [spec.md, L202]. Impact: low.

- **No specification of marker-only validation**: FR-003 (spec.md L204) requires that the draft marker check occurs before variable substitution, but the spec does not specify whether the check should be a first-line-only check or a file-wide scan. The Key Entities definition says "placed as the first line" (L254), but FR-002's check description ("check loaded templates for the draft marker") does not explicitly constrain the scan to line 1. An adversarial reading could implement a whole-file scan that would reject a template if the marker appeared anywhere, not just line 1. [spec.md, L203-204, L254]. Impact: low.

- **No enforcement of marker immutability**: The spec establishes no mechanism to prevent removal of the draft marker from non-cooperative templates before the non-cooperative modes are validated. This is a process gap — someone could remove the marker, and without CI-level enforcement, the safety gate disappears silently. [spec.md, L200-204]. Impact: medium.

- **Edge case: BOM or encoding markers before line 1**: The spec does not address what happens if a file has a UTF-8 BOM (`\xEF\xBB\xBF`) before the draft marker. A BOM would make the marker technically not the "first line" depending on the parser. This is an edge case but relevant for files edited across platforms. [spec.md, L202, L254]. Impact: low.

### Off-Base Assumptions

- **No incorrect assumptions detected**: The spec's assumptions about FR-001 are straightforward and accurate. The assumption that "the three non-cooperative arbitration templates already exist in the templates directory" (spec.md L273) is confirmed — all three files exist and contain the marker. The assumption that the marker is an HTML comment (L254) is correct; it follows standard `<!-- ... -->` syntax. There are no factual errors in the spec's treatment of FR-001.

### Actionable Recommendations

1. **Add negative requirement for cooperative template** (Priority: P1)
   - **Current state**: FR-001 (spec.md L202) only specifies what three templates MUST contain. The cooperative template's exemption is implicit (tested in acceptance scenario 4, L23, but not required by any FR).
   - **Proposed change**: Add FR-001a: "Template `templates/cooperative/arbitration.md` MUST NOT contain `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` as its first line or anywhere in the file."
   - **Rationale**: Acceptance scenarios should verify requirements, not define them. The negative case is a load-bearing property of the system — the cooperative template is the only production-usable template. A missing requirement means a passing FR-001 audit could coexist with a failing acceptance scenario 4. [spec.md, L23 vs L202]
   - **Risk if ignored**: An accidental addition of the draft marker to the cooperative template would not be caught by FR-level compliance auditing, only by acceptance testing. This creates a gap between requirement verification and acceptance verification.

2. **Constrain draft marker check to line 1 in FR-002** (Priority: P2)
   - **Current state**: FR-002 (spec.md L203) says "check loaded templates for the draft marker" without specifying that the check is line-1-only, though FR-001 says "as their first line" and the Key Entities definition (L254) says "placed as the first line."
   - **Proposed change**: Amend FR-002 to: "SKILL.md Step 3 MUST check the first line of loaded templates for the draft marker."
   - **Rationale**: The current wording of FR-002 is ambiguous about scan scope. "Check for" could mean a whole-file search. Explicit line-1 scoping aligns FR-002 with FR-001's placement requirement and prevents over-broad rejection. [spec.md, L203, L254]
   - **Risk if ignored**: An implementation that scans the entire template file could reject templates that mention the draft marker in documentation or comments, causing false positives.

3. **Add acceptance scenario for marker syntax precision** (Priority: P2)
   - **Current state**: Acceptance scenarios 1-3 (spec.md L20-22) verify that the marker is present and triggers rejection. No scenario verifies that a syntactically similar but incorrect marker (e.g., `<!-- CONVERSUS:TEMPLATE_STATUS:draft -->` without the space, or `<!-- CONVERSUS:TEMPLATE_STATUS: Draft -->` with capitalization) does NOT trigger rejection.
   - **Proposed change**: Add acceptance scenario 5: "Given a template whose first line is `<!-- CONVERSUS:TEMPLATE_STATUS: active -->`, When the engine loads this template, Then loading succeeds normally (the marker must match exactly)."
   - **Rationale**: The draft check is a string match. Without a negative test for similar-but-different strings, there is no verification that the check is precise rather than overly broad (e.g., matching any `TEMPLATE_STATUS` comment). [spec.md, L20-23]
   - **Risk if ignored**: An overly broad implementation could block templates with status markers other than "draft" (e.g., a future `active` or `stable` status marker).

4. **Document marker format in a single canonical location** (Priority: P2)
   - **Current state**: The marker format appears in FR-001 (L202), Key Entities (L254), and acceptance scenarios (L20-22). These three locations must stay in sync.
   - **Proposed change**: Designate Key Entities (L254) as the canonical definition and have FR-001 and acceptance scenarios reference it: "the draft marker as defined in Key Entities."
   - **Rationale**: Three independent copies of the same string create drift risk. If the marker format ever changes, all three must be updated simultaneously. A single canonical definition with references eliminates this risk. [spec.md, L202, L254, L20-22]
   - **Risk if ignored**: A future spec amendment could update one location but not the others, creating an internal inconsistency that a compliance auditor would have to adjudicate.

5. **Add edge case for empty template with only draft marker** (Priority: P3)
   - **Current state**: Edge cases (spec.md L191) address "a template file is empty but has the draft marker" and correctly state it triggers rejection. However, there is no explicit acceptance scenario for this.
   - **Proposed change**: Add to Edge Cases or as an acceptance scenario: "Given a template containing only the draft marker and no other content, When the engine loads this template, Then it fails with the draft rejection error before any empty-template error."
   - **Rationale**: This edge case is documented in prose (L191) but not tested. Making it an acceptance scenario ensures implementations handle ordering correctly (draft check before content validation, per FR-003). [spec.md, L191, L204]
   - **Risk if ignored**: An implementation might check for empty templates before checking for draft markers, producing a confusing "empty template" error instead of the expected "draft template" error.

6. **Verify marker survives template compilation/preprocessing** (Priority: P3)
   - **Current state**: FR-003 (spec.md L204) requires the check occurs before variable substitution. This is correctly specified. However, there is no verification that whatever process populates template files (e.g., git operations, CI, template compilation) preserves the marker.
   - **Proposed change**: Add a constraint note: "The draft marker MUST be preserved through any file-level preprocessing (e.g., line-ending normalization, encoding conversion) that occurs before engine load."
   - **Rationale**: If a preprocessing step strips HTML comments or normalizes whitespace, the marker could be silently removed. FR-003 addresses engine-level ordering but not pre-engine processing. [spec.md, L204]
   - **Risk if ignored**: A CI pipeline or file-processing step could strip the marker before the engine sees it, silently disabling the safety gate.

### Referenced Documentation

- `conversus/specs/005-p2p3-backlog-hardening/spec.md` — sections/lines cited: L10-14 (User Story 1), L20-23 (acceptance scenarios 1-4), L191 (edge case: empty template with marker), L200-204 (FR-001, FR-002, FR-003), L254 (Key Entities: Draft Marker), L273 (Assumption: templates exist)
- `conversus/templates/winner-take-all/arbitration.md` — sections/lines cited: L1 (draft marker present)
- `conversus/templates/red-blue/arbitration.md` — sections/lines cited: L1 (draft marker present)
- `conversus/templates/prisoners-dilemma/arbitration.md` — sections/lines cited: L1 (draft marker present)
- `conversus/templates/cooperative/arbitration.md` — sections/lines cited: L1 (no draft marker, heading present)
