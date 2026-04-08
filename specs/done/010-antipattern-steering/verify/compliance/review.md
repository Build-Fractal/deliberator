# Compliance Review: Spec 010 — Agent Antipattern Steering

**Reviewer**: compliance
**Date**: 2026-03-20
**Spec version reviewed**: Draft (2026-03-20)
**Artifacts reviewed**: spec.md, data-model.md, contracts/catalog-format.md, tasks.md, antipatterns/catalog.md, SKILL.md, constitution.md, checklists/requirements.md

---

### Executive Summary

Spec 010 defines a structured antipattern catalog and agent pre-task steering mechanism to prevent deliberation agents from repeating observed behavioral mistakes. The spec is well-structured: it separates catalog structure (FR-001 through FR-004) from agent integration (FR-005, FR-006), contextual retrieval (FR-007, FR-008), and maintenance lifecycle (FR-009, FR-010). The implementation largely follows through on these requirements. All eleven tasks in tasks.md are checked off, the catalog file exists with a well-formed seed entry, SKILL.md contains the Antipattern Check instruction, and the constitution references the catalog.

However, the compliance audit reveals two blocking defects and several material gaps. First, the catalog's Example section references a non-existent path (`specs/001-antipattern-steering/examples/redundant-cache/`) — the actual path is `specs/010-antipattern-steering/examples/redundant-cache/`. This violates SC-004's requirement for concrete, real references. Second, constitution.md Principle IV (L73-75) still mandates STATUS.md as "the authoritative cross-spec reference" — directly contradicting the `redundant-cache` antipattern, which identifies STATUS.md maintenance as the canonical example of wasted effort. These contradictions undermine the catalog's authority and will confuse agents that read both documents.

The most important recommendation is: fix the broken example path in catalog.md and resolve the constitution.md contradiction with Principle IV before declaring this spec complete.

---

### Alignment

- **FR-001 — Catalog exists** (spec.md L69): The catalog file exists at `antipatterns/catalog.md` as a structured markdown document. This satisfies FR-001 fully. [catalog-format.md, L1-9]

- **FR-003 — Summary Index present** (spec.md L71): The catalog includes a `## Summary Index` section with a properly formatted table containing Name, Summary, and Keywords columns, with one active entry row. This matches the contract's specified structure exactly. [catalog-format.md, L17-23]

- **FR-005 + FR-006 — SKILL.md integration** (spec.md L76-77): SKILL.md contains the `### Antipattern Check` section (SKILL.md L199-207) positioned after Step 1 (config parsing) and before Step 2 (output directory creation), exactly as specified in the contract. It references `antipatterns/catalog.md` and specifies the 4-step workflow. [catalog-format.md, L89-103]

- **FR-009 — Deprecation mechanism** (spec.md L86): The Maintenance section at the bottom of catalog.md (L59-71) documents the deprecation workflow: set Status to Deprecated, add Deprecation Note section, remove from Summary Index. This matches the data model's state transition specification. [data-model.md, L87-98]

- **FR-010 — Append-only** (spec.md L87): The Maintenance section explicitly instructs "Do NOT modify any existing entries (FR-010: append-only)" (catalog.md L64). The catalog structure supports this — new entries append before the Maintenance section, new index rows append to the table.

- **Constitution integration** (tasks.md L52): The constitution's "Known Antipatterns" section (constitution.md L179-192) references `antipatterns/catalog.md` and describes the SKILL.md enforcement mechanism, satisfying T006.

---

### Missed Opportunities

- **Cross-reference validation between catalog and constitution**: The spec requires that the Example field reference real files (SC-004, spec.md L102) and the catalog-format contract specifies the exact Example field must reference "real files/specs" (catalog-format.md L77). However, there is no requirement or task for validating that referenced paths actually exist at implementation time. T011 (tasks.md L77) mentions validating cross-references but only as a manual polish step. An automated or checklist-driven path-existence check would have caught the broken `specs/001-antipattern-steering/` reference. Impact: high.

- **Constitution consistency gate**: The spec acknowledges that the catalog lives alongside other governance documents (spec.md L107) but does not require a consistency check between catalog entries and constitution principles. The constitution's Principle IV actively mandates STATUS.md maintenance — the exact behavior the `redundant-cache` antipattern warns against. A requirement to reconcile catalog entries with constitutional principles would prevent this contradiction. Impact: high.

- **Entry validation checklist**: The data model defines precise validation rules (data-model.md L56-61): symptoms >= 2, scope >= 1 exclusion, keywords >= 2 tags, real example references. The tasks reference these constraints (T003, tasks.md L38) but there is no standalone validation checklist artifact that can be run against the catalog post-implementation. The requirements.md checklist (checklists/requirements.md) validates the spec's quality, not the implementation's conformance. Impact: medium.

- **Bidirectional sync validation between index and entries**: The data model requires "every active entry must have a corresponding row (bidirectional sync)" (data-model.md L33). The current catalog has only one entry so this is trivially satisfied, but there is no defined mechanism for validating this invariant as entries accumulate. A machine-readable format or a validation script reference would provide ongoing assurance. Impact: medium.

- **SC-001 testability**: SC-001 (spec.md L99) requires "zero repeated instances of previously cataloged antipatterns." This is the strongest success criterion but is entirely aspirational — there is no mechanism to detect or report when an agent ignores the catalog. The spec could define a post-deliberation review step that checks whether any output exhibits cataloged symptoms. Impact: medium.

- **SC-002 overhead measurement**: SC-002 (spec.md L100) specifies "less than 30 seconds of overhead." There is no mechanism to measure this. For a markdown-only feature this is inherently untestable unless agent timing is instrumented. The spec should either acknowledge this is an aspirational bound or define how it would be measured. Impact: low.

---

### Off-Base Assumptions

- **Constitution Principle IV contradicts the seed antipattern**: The spec assumes the antipattern catalog's guidance will be internally consistent with other governance documents (spec.md L107: "The catalog lives in the conversus project directory, accessible to all agents"). However, constitution.md Principle IV (L73-75) states: "STATUS.md MUST be updated when any spec's implementation or acceptance status changes. It is the authoritative cross-spec reference." This directly contradicts the `redundant-cache` antipattern, which identifies STATUS.md as a redundant cache of computable state (catalog.md L27-33). An agent reading both documents receives conflicting MUST-level instructions. The constitution was not amended to remove or qualify Principle IV's STATUS.md mandate as part of this spec's implementation. This is a real conflict, not a hypothetical one.

- **Example path assumes spec numbering 001**: The catalog entry's Example section (catalog.md L33) references `specs/001-antipattern-steering/examples/redundant-cache/`. The actual path is `specs/010-antipattern-steering/examples/redundant-cache/`. The `001` prefix appears to be a typo from early development. The tasks reference this same incorrect path (tasks.md L38, L64, L77), suggesting the error was present in the task definitions and propagated into the implementation.

---

### Actionable Recommendations

1. **Fix broken example path** (Priority: P1)
   - **Current state**: catalog.md L33 references `specs/001-antipattern-steering/examples/redundant-cache/`. tasks.md L38, L64, L77 also reference this path.
   - **Proposed change**: Change all occurrences of `specs/001-antipattern-steering/` to `specs/010-antipattern-steering/` in catalog.md. Update tasks.md references for consistency.
   - **Rationale**: SC-004 (spec.md L102) requires "100% of cataloged antipatterns include a concrete example from an observed incident." A broken path fails this criterion — the example is not verifiable. The actual artifacts exist at `specs/010-antipattern-steering/examples/redundant-cache/` (confirmed by filesystem inspection).
   - **Risk if ignored**: Every agent or human following the Example reference hits a dead end. SC-004 is not satisfied. The catalog's credibility as a real-incident-based resource is undermined.

2. **Resolve constitution Principle IV contradiction** (Priority: P1)
   - **Current state**: Constitution Principle IV (constitution.md L73-75) mandates STATUS.md as "the authoritative cross-spec reference." The `redundant-cache` antipattern (catalog.md L27-33) identifies STATUS.md as a redundant cache that should not exist.
   - **Proposed change**: Amend Principle IV to remove or qualify the STATUS.md mandate. For example: "Cross-spec status is derived from speckit artifacts (tasks.md checkboxes, spec.md acceptance scenarios), not from manually-maintained summary documents. See antipatterns/catalog.md: redundant-cache."
   - **Rationale**: Constitution.md L196-199 states: "This constitution supersedes conflicting guidance in individual specs or agent prompts." An agent reading both documents will follow the constitution's MUST over the catalog's correction, defeating the purpose of the antipattern entry. [constitution.md, L196-199; catalog.md L37-43]
   - **Risk if ignored**: Agents receive contradictory MUST-level instructions. The `redundant-cache` antipattern is effectively dead letter — the constitution overrides it. Future STATUS.md maintenance cycles will recur.

3. **Add path-existence validation to T011** (Priority: P1)
   - **Current state**: T011 (tasks.md L77) says "Validate cross-references — verify ... catalog entry Example section references valid paths." T011 is checked off, but the path is invalid.
   - **Proposed change**: Add an explicit validation step: "For each path referenced in Example sections, verify the path exists by listing the directory. Record the verification result."
   - **Rationale**: The current T011 wording allows "validation" to mean reading the references without actually checking they resolve. A stricter requirement would have caught the `001` vs `010` typo. [data-model.md L56: "example must reference a real observed incident"]
   - **Risk if ignored**: Future entries with broken references pass validation. SC-004 compliance degrades silently.

4. **Add constitution consistency check to implementation workflow** (Priority: P2)
   - **Current state**: No task or requirement checks for contradictions between catalog entries and constitution principles.
   - **Proposed change**: Add a validation rule to the Maintenance section of catalog.md: "Before adding an entry whose Correction contradicts a constitutional principle, either (a) amend the constitution first via /speckit.constitution, or (b) note the conflict in the entry with a reference to the constitutional principle and a rationale for why the antipattern overrides it."
   - **Rationale**: The constitution has explicit governance precedence (constitution.md L196-199). Catalog entries that contradict it without acknowledgment create ambiguity. [constitution.md L196-199; spec.md L59: "What happens when two antipatterns conflict"]
   - **Risk if ignored**: Future antipattern entries may silently contradict constitutional principles, creating agent confusion with no resolution path.

5. **Define SC-001 measurement mechanism** (Priority: P2)
   - **Current state**: SC-001 (spec.md L99) says "zero repeated instances of previously cataloged antipatterns" but defines no detection method.
   - **Proposed change**: Add a note to SC-001: "Measured by post-deliberation review: if any deliberation output proposes an artifact matching a cataloged antipattern's symptoms, SC-001 is violated. Detection is manual until automated symptom matching is implemented."
   - **Rationale**: A success criterion that cannot be measured is not a criterion — it is an aspiration. Defining the measurement method, even if manual, makes it actionable. [spec.md L95-102]
   - **Risk if ignored**: SC-001 can never be formally satisfied or formally violated. It provides no signal.

6. **Clarify SC-003 "performance degrades" threshold** (Priority: P2)
   - **Current state**: SC-003 (spec.md L101) says "at least 50 entries before retrieval performance degrades — keyword-based retrieval scales linearly."
   - **Proposed change**: Clarify that "performance" here means agent context window consumption, not computation time. At 50 entries, the Summary Index table is approximately 50 lines — well within any agent context window. The risk is not speed but context budget allocation. Reword to: "The Summary Index supports 50+ entries within a single agent context read. Full-entry retrieval is filtered by keyword match, loading only relevant entries."
   - **Rationale**: For a markdown-based catalog with no computation, "retrieval performance" is misleading. The actual constraint is context window budget. [spec.md L101; catalog-format.md L89-103]
   - **Risk if ignored**: Future implementors may waste effort optimizing computation speed for a problem that is actually about context window management.

7. **Add field-count validation to catalog entry template** (Priority: P3)
   - **Current state**: The data model lists 11 fields (data-model.md L42-53) with validation rules, but the catalog Maintenance section (catalog.md L62) lists them in prose without a machine-checkable format.
   - **Proposed change**: Add a comment or checklist in the Maintenance section enumerating all required fields with their validation constraints, e.g.: "Required fields: Status, Observed (YYYY-MM-DD), Summary (<100 chars), Symptoms (>=2 bullets), Root Cause, Example (real refs), Correction, When This Does NOT Apply (>=1 exclusion), Keywords (>=2 tags)."
   - **Rationale**: The current Maintenance section includes this information but in flowing text. A structured checklist reduces the chance of future entries omitting fields. [data-model.md L42-61]
   - **Risk if ignored**: Future entries may omit required fields without detection until the next compliance audit.

---

### Detailed Requirement Verification Matrix

| Requirement | Status | Evidence | Notes |
|-------------|--------|----------|-------|
| FR-001 | **Implemented** | `antipatterns/catalog.md` exists as structured document | -- |
| FR-002 | **Partially implemented** | Entry has all required fields per data-model.md, but Example references non-existent path `specs/001-antipattern-steering/` | Path should be `specs/010-antipattern-steering/` |
| FR-003 | **Implemented** | Summary Index table at top of catalog.md with Name, Summary, Keywords columns | -- |
| FR-004 | **Implemented** | Entry is self-contained — reading it provides full context | -- |
| FR-005 | **Implemented** | SKILL.md L199-207 contains Antipattern Check instruction | -- |
| FR-006 | **Implemented** | Instruction references `antipatterns/catalog.md` and specifies 4-step workflow | Step 2 enhanced with keyword filtering for >10 entries |
| FR-007 | **Implemented** | Entry has 8 keyword tags; index Keywords column matches | -- |
| FR-008 | **Implemented** | SKILL.md step 2 specifies keyword matching against Summary Index; grep-equivalent retrieval | -- |
| FR-009 | **Implemented** | Maintenance section documents deprecation workflow (catalog.md L67-71) | -- |
| FR-010 | **Implemented** | Maintenance section states "Do NOT modify any existing entries" (catalog.md L64) | -- |
| SC-001 | **Not measurable** | No detection mechanism defined | Aspirational; see recommendation 5 |
| SC-002 | **Not measurable** | No timing instrumentation | Reasonable assumption for summary index scan |
| SC-003 | **Not testable at current scale** | Only 1 entry; design supports scaling | -- |
| SC-004 | **Partially satisfied** | Example references real incident but path is broken | `specs/001-antipattern-steering/` does not exist; correct path is `specs/010-antipattern-steering/` |

### Task Completion Verification

| Task | Checked | Verified | Issue |
|------|---------|----------|-------|
| T001 | [x] | Pass | `antipatterns/` directory exists |
| T002 | [x] | Pass | catalog.md created with correct structure |
| T003 | [x] | **Fail** | Example references wrong path (`001` vs `010`) |
| T004 | [x] | Pass | Summary Index row matches entry data |
| T005 | [x] | Pass | SKILL.md contains Antipattern Check at correct position |
| T006 | [x] | Pass | Constitution Known Antipatterns section references catalog |
| T007 | [x] | Pass | Keywords refined; 8 tags present; index matches |
| T008 | [x] | Pass | SKILL.md step 2 extended with keyword-matching guidance |
| T009 | [x] | Pass | Maintenance section documents add/deprecate workflows |
| T010 | [x] | **Partial** | FR validation claimed but broken path not caught |
| T011 | [x] | **Fail** | Cross-reference validation claimed but `specs/001-antipattern-steering/` path does not exist |

### Catalog Entry Field Validation (redundant-cache)

| Field | Required | Present | Valid | Notes |
|-------|----------|---------|-------|-------|
| Status | no (default Active) | Yes | Yes | "Active" |
| Observed | yes | Yes | Yes | "2026-03-20" in YYYY-MM-DD format |
| Summary | yes | Yes | Yes | <100 chars, matches index |
| Symptoms | yes (>=2) | Yes | Yes | 4 items |
| Root Cause | yes | Yes | Yes | Paragraph with context |
| Example | yes (real refs) | Yes | **No** | References non-existent path `specs/001-antipattern-steering/` |
| Correction | yes | Yes | Yes | Actionable with specific alternatives |
| When This Does NOT Apply | yes (>=1) | Yes | Yes | 3 exclusions |
| Keywords | yes (>=2) | Yes | Yes | 8 tags, backtick-formatted, comma-separated |

### Summary Index Consistency Check

| Check | Result |
|-------|--------|
| Every active entry has index row | Pass (1 entry, 1 row) |
| No deprecated entries in index | Pass (no deprecated entries) |
| Name matches H2 heading | Pass (`redundant-cache`) |
| Summary matches entry Summary | Pass (identical text) |
| Keywords match entry Keywords | Pass (identical tags) |

---

### Referenced Documentation

- `specs/010-antipattern-steering/spec.md` — sections/lines cited: L69 (FR-001), L70 (FR-002), L71 (FR-003), L72 (FR-004), L76 (FR-005), L77 (FR-006), L81 (FR-007), L82 (FR-008), L86 (FR-009), L87 (FR-010), L99 (SC-001), L100 (SC-002), L101 (SC-003), L102 (SC-004), L107 (assumptions), L59 (edge cases)
- `specs/010-antipattern-steering/data-model.md` — sections/lines cited: L33 (bidirectional sync), L42-53 (entry fields), L56-61 (validation rules), L87-98 (state transitions)
- `specs/010-antipattern-steering/contracts/catalog-format.md` — sections/lines cited: L1-9 (purpose), L17-23 (summary index structure), L66-80 (field contracts), L77 (example requirement), L89-103 (SKILL.md integration contract)
- `specs/010-antipattern-steering/tasks.md` — sections/lines cited: L38 (T003), L52 (T006), L64 (T007), L77 (T011)
- `specs/010-antipattern-steering/checklists/requirements.md` — sections/lines cited: L1-36 (full checklist)
- `antipatterns/catalog.md` — sections/lines cited: L1-71 (full catalog), L33 (broken example path), L37-43 (correction), L62-64 (maintenance add workflow), L67-71 (maintenance deprecation workflow)
- `SKILL.md` — sections/lines cited: L199-207 (Antipattern Check section)
- `.specify/memory/constitution.md` — sections/lines cited: L63-75 (Principle IV), L73-75 (STATUS.md mandate), L179-192 (Known Antipatterns), L196-199 (governance precedence)
