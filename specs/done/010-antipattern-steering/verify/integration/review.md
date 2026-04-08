# Integration Review: 010-antipattern-steering

**Reviewer**: integration
**Date**: 2026-03-20
**Scope**: Cross-file reference consistency and functional coherence of the antipattern steering system

---

### Executive Summary

Spec 010-antipattern-steering introduces a lightweight antipattern catalog system that agents consult before proposing new artifacts, closing the loop between observed behavioral mistakes and prevention. The integration surface spans four files: the catalog itself (`antipatterns/catalog.md`), the agent orchestration spec (`SKILL.md`), the project constitution (`.specify/memory/constitution.md`), and the format contract (`specs/010-antipattern-steering/contracts/catalog-format.md`). From an integration perspective, the system is well-structured -- references between SKILL.md, the constitution, and the catalog are consistent in path and behavioral intent, the catalog entry format conforms to the contract, and keyword tags are synchronized between the Summary Index and the entry body.

However, there are two blocking integration failures. First, the example path referenced in the catalog entry (`specs/001-antipattern-steering/examples/redundant-cache/`) does not exist on disk -- it is a dead link. This is referenced across six files (catalog, tasks, quickstart, plan, research, conversus.yml) and constitutes a systemic broken reference. Second, the constitution's Principle IV (L73-75) still mandates STATUS.md maintenance as the "authoritative cross-spec reference," which directly contradicts the antipattern catalog's first entry that identifies STATUS.md maintenance as a waste pattern. These two issues mean an agent following the system's own instructions would encounter contradictory guidance and a dead reference.

The most important recommendation is: resolve the STATUS.md contradiction between constitution Principle IV and the redundant-cache antipattern entry before shipping, because this guarantees agents will receive conflicting instructions.

### Alignment

- **[Catalog path consistency]** (SKILL.md L202, constitution L181, catalog L1): All three files reference the catalog at the identical path `antipatterns/catalog.md`. An agent following SKILL.md will find the file exactly where it is told to look. `[contracts/catalog-format.md, L97]` specifies this path in the integration contract.

- **[4-step workflow preserved]** (SKILL.md L204-207, contracts/catalog-format.md L99-102): The SKILL.md Antipattern Check section maintains the contract's 4-step structure (read index, match, follow correction, proceed if no match). Step 2 was extended with keyword retrieval guidance per T008, but the original steps remain intact. The contract's skeletal 4 steps are a proper subset of the SKILL.md implementation. `[contracts/catalog-format.md, L89-103]`.

- **[Keyword synchronization]** (catalog.md L10, L53): The Summary Index Keywords column (`tracking, cache, artifact-creation, status, taxonomy, deliberation-drift, convention-over-content, speckit-duplication`) exactly matches the entry's Keywords section (same tags in same order, with backtick formatting in the entry body). This satisfies data-model.md L73: "Tags appear in both the entry's Keywords field and the Summary Index Keywords column." `[data-model.md, L72-73]`.

- **[Entry format conformance]** (catalog.md L14-53, contracts/catalog-format.md L26-59): The `redundant-cache` entry follows the contract's field order exactly: H2 heading, Status, Observed, Summary, then H3 subsections for Symptoms, Root Cause, Example, Correction, When This Does NOT Apply, Keywords. All required fields are present. `[contracts/catalog-format.md, L71-80]`.

- **[Constitution catalog reference]** (constitution.md L181-192): The Known Antipatterns section correctly references `antipatterns/catalog.md` as the catalog location and `specs/010-antipattern-steering/contracts/catalog-format.md` as the governing contract. It accurately summarizes the SKILL.md workflow: "read the Summary Index, match against current work, follow corrections." `[contracts/catalog-format.md, L89-91]`.

- **[Maintenance procedures]** (catalog.md L57-71): The Maintenance section documents both add and deprecate workflows correctly. Adding specifies append-before-Maintenance, add index row, no existing entry modification (FR-010). Deprecation specifies Status change, Deprecation Note section, index removal (FR-009). Both match the contract's Versioning section. `[contracts/catalog-format.md, L107-108]`.

### Missed Opportunities

- **[Dead example path not caught by validation tasks]**: T011 in tasks.md (L77) specifies validating that "catalog entry Example section references valid paths in `specs/001-antipattern-steering/examples/redundant-cache/`." The task is marked complete (`[x]`), but the path does not exist on disk. No `specs/001-antipattern-steering/` directory exists in the conversus project -- only `specs/009-antipattern-steering/` and `specs/010-antipattern-steering/`. This is referenced in catalog.md L33, tasks.md L38 and L77, quickstart.md L15 and L47, and the conversus.yml verification config L57. The validation task should have caught this. Impact: **high**. `[tasks.md, L77]`.

- **[SKILL.md step 2 diverges from contract without contract update]**: The contract (catalog-format.md L91) specifies "Exact wording" for the SKILL.md integration block. SKILL.md L205 extends step 2 with keyword retrieval guidance ("When the catalog exceeds 10 entries, filter by matching task-derived keywords...") that is not present in the contract's exact wording (L100). Per the contract's own rule (L109), "Format changes to this contract require updating all existing entries for consistency." The contract should be updated to reflect the extended step 2, or the divergence should be documented. Impact: **medium**. `[contracts/catalog-format.md, L91, L100, L109]`.

- **[No validation that Maintenance section is positioned correctly]**: The catalog.md Maintenance section (L57) is an H2 heading like entry sections. The contract template (catalog-format.md L12-59) does not include a Maintenance section, so there is no contract-level guidance on where it sits or how to distinguish it from entries. The add procedure (catalog.md L62) says "before this Maintenance section," but an agent parsing H2 headings for entries would also match `## Maintenance`. A sentinel comment or different heading level would prevent misidentification. Impact: **medium**. `[contracts/catalog-format.md, L12-59]`.

- **[Constitution Principle IV mandates STATUS.md but antipattern condemns it]**: Constitution.md L73-75 states "STATUS.md MUST be updated when any spec's implementation or acceptance status changes. It is the authoritative cross-spec reference." The redundant-cache antipattern (catalog.md L22-25, L29, L33) identifies STATUS.md maintenance as the exact antipattern being cataloged. An agent following both the constitution and the antipattern catalog receives contradictory MUST-level instructions. The constitution was not amended to remove or qualify the STATUS.md mandate. Impact: **high**. `[constitution.md, L73-75; catalog.md, L22-33]`.

- **[No cross-reference from catalog entry back to spec 010]**: The catalog entry references `specs/001-antipattern-steering/examples/redundant-cache/` for example artifacts but does not reference the governing spec `specs/010-antipattern-steering/` that defines the catalog system itself. A maintainer reading the catalog has no link to the spec that defines its format contract. The constitution (L192) references the contract, but the catalog itself does not. Impact: **low**. `[catalog.md, L33; constitution.md, L192]`.

- **[Quickstart references nonexistent seed file]**: Quickstart.md L15 references `specs/001-antipattern-steering/examples/redundant-cache/README.md` as the content source for seeding the catalog. This file does not exist. The quickstart is the implementer's entry point -- a broken reference here blocks anyone attempting to follow the implementation checklist. Impact: **high**. `[quickstart.md, L15, L47]`.

- **[No machine-readable delimiter between entries and Maintenance]**: The catalog uses `---` horizontal rules between entries (catalog.md L12, L55) and before the Maintenance section. These delimiters are visual only. There is no machine-readable marker (e.g., `<!-- CATALOG:ENTRIES_END -->`) that a retrieval mechanism could use to distinguish entry content from maintenance documentation. For P2 keyword retrieval, a grep-based search would also match text in the Maintenance section. Impact: **low**. `[catalog.md, L12, L55; spec.md, L108]`.

### Off-Base Assumptions

- **[Example artifacts from spec 001 exist]**: The spec, tasks, quickstart, and catalog all assume that `specs/001-antipattern-steering/examples/redundant-cache/` exists and contains the original STATUS.md, fix-it specs, and deliberation summaries (tasks.md L38, quickstart.md L15, catalog.md L33). This directory does not exist on disk. The specs directory contains `009-antipattern-steering` and `010-antipattern-steering` but no `001-antipattern-steering`. Either the numbering convention changed, the example directory was never created, or it was placed elsewhere. The correct path needs to be determined and all six referencing files updated.

- **[Constitution and catalog are consistent on STATUS.md]**: T006 (tasks.md L52) and the constitution's Known Antipatterns section (constitution.md L179-192) were updated to reference the catalog. However, the constitution was not amended to resolve the contradiction between Principle IV's STATUS.md mandate (L73-75) and the catalog's first entry condemning STATUS.md maintenance. The implementation assumed adding a Known Antipatterns section was sufficient without reviewing whether existing constitution principles conflict with the new catalog content.

### Actionable Recommendations

1. **Fix example path references** (Priority: P1)
   - **Current state**: Six files reference `specs/001-antipattern-steering/examples/redundant-cache/` (catalog.md L33, tasks.md L38, tasks.md L77, quickstart.md L15, quickstart.md L47, plan.md L63). This path does not exist.
   - **Proposed change**: Determine the correct location for the example artifacts. If they were never created, either create the directory with the referenced artifacts or update all six references to point to whatever location actually contains the original STATUS.md and related specs (e.g., `specs/STATUS.md`, `specs/done/007-status-taxonomy-updates/`, etc.). If the spec numbering changed from 001 to 009/010, update all references to use the correct prefix.
   - **Rationale**: SC-004 (spec.md L102) requires that "100% of cataloged antipatterns include a concrete example from an observed incident." A dead link to example artifacts undermines the entry's self-contained nature (FR-004) and makes validation task T011 unverifiable. `[spec.md, L102; data-model.md, L56]`.
   - **Risk if ignored**: An agent reading the catalog entry and attempting to examine the referenced example artifacts will fail. New contributors trying to understand the antipattern by reviewing the original incident cannot do so. The catalog entry's Example section becomes hearsay rather than verifiable evidence.

2. **Resolve STATUS.md contradiction in constitution** (Priority: P1)
   - **Current state**: Constitution Principle IV (L73-75) mandates "STATUS.md MUST be updated when any spec's implementation or acceptance status changes." The redundant-cache antipattern entry (catalog.md L22-33) identifies STATUS.md maintenance as a waste pattern.
   - **Proposed change**: Amend constitution Principle IV to remove or qualify the STATUS.md mandate. Options: (a) remove the STATUS.md bullet entirely and add a cross-reference to the redundant-cache antipattern, (b) replace the STATUS.md mandate with guidance to derive status from speckit artifacts (matching the catalog's Correction section), or (c) add a note that this principle is superseded by the antipattern catalog entry. This requires a constitution version bump (1.1.0 -> 1.2.0 per the Governance section's amendment rules, L201-202).
   - **Rationale**: The constitution's Governance section (L196-199) states "When a spec contradicts a constitutional principle, the constitution governs unless the spec explicitly documents and justifies the deviation." The antipattern catalog does not document a deviation from Principle IV. Agents encountering both instructions will follow the constitution (MUST-level) and maintain STATUS.md, defeating the antipattern's purpose. `[constitution.md, L196-199; catalog.md, L37-43]`.
   - **Risk if ignored**: Agents will continue maintaining STATUS.md because the constitution's MUST-level mandate takes precedence over the catalog's guidance. The very antipattern the system was built to prevent will continue occurring.

3. **Update contract to reflect extended step 2** (Priority: P2)
   - **Current state**: Contracts/catalog-format.md L91 specifies "Exact wording" for the SKILL.md integration block. Step 2 in the contract (L100) reads: "If any entry's keywords or summary matches your current work, read the full entry." Step 2 in SKILL.md (L205) reads: "Match your current work against entry keywords and summaries. When the catalog exceeds 10 entries, filter by matching task-derived keywords against the Summary Index Keywords column and read only matched full entries."
   - **Proposed change**: Update the contract's SKILL.md Integration Contract section (L93-103) to match the current SKILL.md wording, reflecting the keyword retrieval extension added in T008. Alternatively, add a note that the SKILL.md block may be extended beyond the contract's minimum wording.
   - **Rationale**: The contract labels this "Exact wording" (L91). A divergence between the contract and the actual SKILL.md content means a future implementer consulting the contract would produce incorrect output. `[contracts/catalog-format.md, L91]`.
   - **Risk if ignored**: Future catalog format updates that consult the contract will use the outdated step 2 wording, potentially overwriting the keyword retrieval extension in SKILL.md.

4. **Add Maintenance section to contract template** (Priority: P2)
   - **Current state**: The contract's catalog file structure template (catalog-format.md L12-59) defines the header, summary index, and entry sections but does not include the Maintenance section that exists in the actual catalog (catalog.md L57-71).
   - **Proposed change**: Append a `## Maintenance` section to the contract template showing the expected structure for Adding and Deprecating entries. This formalizes what is currently only in the catalog itself.
   - **Rationale**: The contract (L7) states it "defines the exact structure of `antipatterns/catalog.md`." A section that exists in the catalog but not the contract is a structural divergence. `[contracts/catalog-format.md, L7]`.
   - **Risk if ignored**: A future re-implementation of the catalog from the contract would omit the Maintenance section, losing the documented add/deprecate procedures.

5. **Add disambiguation for Maintenance heading** (Priority: P2)
   - **Current state**: The Maintenance section uses `## Maintenance` (H2), the same heading level as entry sections like `## redundant-cache` (catalog.md L14, L57). An agent or script parsing H2 headings to enumerate entries would incorrectly include Maintenance as an entry.
   - **Proposed change**: Either: (a) add a sentinel comment before the Maintenance section (e.g., `<!-- CATALOG:ENTRIES_END -->`), (b) change Maintenance to a different heading level (H1 appendix or move to a separate file), or (c) document in the contract that the final H2 section is always Maintenance and is not an entry.
   - **Rationale**: FR-008 (spec.md L82) requires a retrieval mechanism that returns only matching entries. If the retrieval mechanism scans H2 sections, it must know to exclude Maintenance. `[spec.md, L82; catalog.md, L57]`.
   - **Risk if ignored**: Keyword searches that match terms in the Maintenance section (e.g., "Deprecated," "Status") could produce false positives by returning Maintenance documentation as if it were an antipattern entry.

6. **Mark T011 incomplete** (Priority: P2)
   - **Current state**: T011 (tasks.md L77) is marked `[x]` (complete) but specifies validating that the catalog Example section "references valid paths in `specs/001-antipattern-steering/examples/redundant-cache/`." This path does not exist on disk.
   - **Proposed change**: Uncheck T011 (`[ ]`) until the example path issue is resolved.
   - **Rationale**: Marking a validation task complete when the validation condition is not met undermines the task tracking system's integrity. `[tasks.md, L77]`.
   - **Risk if ignored**: The task list falsely reports 100% completion, masking a known integration failure.

7. **Add catalog self-reference to format contract** (Priority: P3)
   - **Current state**: The catalog entry (catalog.md) does not reference the spec or contract that governs its format. The constitution (L192) references the contract, but the catalog is the artifact agents actually read.
   - **Proposed change**: Add a small footer or comment to the catalog file referencing the governing spec: e.g., `<!-- Format governed by specs/010-antipattern-steering/contracts/catalog-format.md -->`.
   - **Rationale**: FR-004 (spec.md L72) requires entries to be self-contained, but the catalog itself should also be traceable to its governing specification for maintainability. `[spec.md, L72]`.
   - **Risk if ignored**: A maintainer modifying the catalog has no in-file indication of where the format rules are documented, increasing the chance of format drift.

8. **Verify constitution version bump requirement** (Priority: P3)
   - **Current state**: The constitution was modified (Known Antipatterns section added, L179-192) but the version remains 1.1.0 (L208). The Governance section (L203) specifies MINOR bumps for "new principles or material expansions."
   - **Proposed change**: If the STATUS.md contradiction is resolved (recommendation 2), bump the constitution version to 1.2.0. If only the Known Antipatterns section was added without amending Principle IV, a MINOR bump to 1.2.0 is still warranted for the material expansion.
   - **Rationale**: The constitution's own versioning rules (L203) require a MINOR bump for material expansions. Adding a new section qualifies. `[constitution.md, L203]`.
   - **Risk if ignored**: The Sync Impact Report at the top of the constitution (L1-16) becomes out of date, and future audits cannot distinguish the pre-antipattern and post-antipattern versions of the constitution.

### Referenced Documentation

- `specs/010-antipattern-steering/spec.md` -- sections/lines cited: L72 (FR-004), L82 (FR-008), L102 (SC-004), L108 (assumptions)
- `specs/010-antipattern-steering/data-model.md` -- sections/lines cited: L56 (example validation), L72-73 (keyword tag rules)
- `specs/010-antipattern-steering/contracts/catalog-format.md` -- sections/lines cited: L7 (purpose), L12-59 (template), L71-80 (field contracts), L89-103 (SKILL.md integration contract), L91 (exact wording), L100 (step 2), L107-109 (versioning)
- `specs/010-antipattern-steering/tasks.md` -- sections/lines cited: L38 (T003 example path), L52 (T006), L77 (T011 validation)
- `specs/010-antipattern-steering/quickstart.md` -- sections/lines cited: L15 (seed data reference), L47 (key files table)
- `antipatterns/catalog.md` -- sections/lines cited: L1-71 (full catalog), L10 (index keywords), L14-53 (entry), L33 (example path), L53 (entry keywords), L57-71 (maintenance)
- `SKILL.md` -- sections/lines cited: L199-207 (antipattern check section), L202 (catalog path), L204-207 (4-step workflow)
- `.specify/memory/constitution.md` -- sections/lines cited: L73-75 (Principle IV STATUS.md mandate), L179-192 (Known Antipatterns), L196-199 (governance precedence), L201-203 (amendment/versioning rules), L208 (version number)
