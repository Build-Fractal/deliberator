# Scope-Boundary Review: Spec 010 — Agent Antipattern Steering

**Reviewer**: scope-boundary
**Date**: 2026-03-20
**Spec**: `/conversus/specs/010-antipattern-steering/spec.md`

---

### Executive Summary

Spec 010 introduces a structured antipattern catalog and an agent pre-task check to prevent recurring behavioral mistakes, specifically the "redundant-cache" pattern observed during the STATUS.md/specs 007-008 incident. The scope is deliberately narrow: one catalog file, one SKILL.md instruction block, one constitution cross-reference, and one seed entry. My job is to verify that the implementation neither exceeds nor falls short of this scope.

The implementation is well-bounded. All P1 features (Catalog Structure, Agent Integration) and all P2 features (Contextual Retrieval, Catalog Maintenance) are implemented. The catalog contains exactly one seed entry as specified. The SKILL.md change is purely additive. No templates, phase execution logic, or existing agent behaviors were modified. However, there are two boundary violations that require attention: (1) the catalog entry's Example section references a nonexistent path (`specs/001-antipattern-steering/examples/redundant-cache/`) when the actual path is `specs/010-antipattern-steering/examples/redundant-cache/`, and (2) the constitution still mandates STATUS.md maintenance (Principle IV, L73-75) which directly contradicts the antipattern being cataloged, yet spec 010 neither addresses nor acknowledges this tension.

My most important recommendation: fix the broken path reference in the catalog entry Example section, as it is the single factual error in the implementation that violates both FR-004 (self-contained entries) and SC-004 (real incident references).

### Alignment

- **[Seed entry scoping]** (spec.md L106, tasks.md L38-39): The catalog contains exactly one entry — `redundant-cache` — matching the spec's assumption that "the initial catalog is seeded with the 'redundant-cache' antipattern." No extra hypothetical entries were added. [plan.md, L20: "Initial seed of 1 antipattern entry"].

- **[Additive SKILL.md change]** (spec.md L109, SKILL.md L199-207): The Antipattern Check instruction is inserted as a new `### Antipattern Check` subsection between Step 1 (Parse Config) and Step 2 (Create Output Directories). No existing SKILL.md content was modified, deleted, or restructured. The git diff confirms the change is a pure insertion. This aligns with the spec's statement that "Agent prompt integration means adding a brief instruction" and the plan's Constitution Check noting "SKILL.md additions are additive" [plan.md, L29].

- **[Catalog location]** (spec.md L107): The catalog file lives at `antipatterns/catalog.md` at the conversus project root, adjacent to `presets/` and `templates/`. This matches the spec's assumption that "the catalog lives in the conversus project directory, accessible to all agents." [plan.md, L67: "The catalog lives in `antipatterns/catalog.md` at the conversus root, adjacent to `presets/` and `templates/`"].

- **[Data model fidelity]** (data-model.md L37-61, catalog.md L14-53): Every required field defined in the Antipattern Entry entity is present in the catalog entry. No extra fields were added. The field ordering matches the contract (catalog-format.md L73: "Fields appear in fixed order"). The Summary Index table has the three specified columns (Name, Summary, Keywords) and no additional columns.

- **[Append-only structure]** (spec.md L87, FR-010): The Maintenance section in catalog.md (L59-71) correctly documents that new entries must be appended without modifying existing entries. The catalog structure supports this — entries are sequential H2 sections with a Maintenance footer.

- **[P2 keyword retrieval]** (spec.md L79-83, SKILL.md L205): The SKILL.md Antipattern Check step 2 incorporates the keyword-matching guidance for catalogs exceeding 10 entries, satisfying FR-007 and FR-008 within the existing instruction block rather than adding separate retrieval infrastructure. This matches the spec's assumption that "keyword retrieval is a simple text match (grep-equivalent)" [spec.md, L108].

### Missed Opportunities

- **[Constitution Principle IV conflict]**: The constitution at `.specify/memory/constitution.md` L73-75 states: "STATUS.md MUST be updated when any spec's implementation or acceptance status changes. It is the authoritative cross-spec reference." The `redundant-cache` antipattern explicitly warns against creating and maintaining STATUS.md-style tracking documents. Spec 010 does not mention this contradiction. The plan added a "Known Antipatterns" section to the constitution (L179-192) but did not reconcile Principle IV with the antipattern it catalogs. This is not an over-scope issue (the implementation correctly did not modify Principle IV without a spec), but it is a missed opportunity to flag the tension for a follow-up spec. Impact: **high** — agents reading the constitution receive conflicting instructions.

- **[Broken example path reference]**: The catalog entry's Example section (catalog.md L33) references `specs/001-antipattern-steering/examples/redundant-cache/`, but this directory does not exist. The actual path is `specs/010-antipattern-steering/examples/redundant-cache/`. This same wrong path appears in tasks.md T003 (L38), T011 (L77), the plan (L63), quickstart.md, and research.md. The error propagated from the spec/plan design documents into the implementation. This violates FR-004 (self-contained entry requiring no cross-referencing to understand) since a reader following the path reference would find nothing. Impact: **high** — the entry's only concrete example reference is broken.

- **[No acceptance scenario for constitution cross-reference]**: The plan added T006 (constitution update) which goes beyond the spec's stated scope. The spec mentions only SKILL.md and templates (L109) as integration points. While the constitution cross-reference is reasonable and non-destructive, there is no acceptance scenario validating it, and the spec does not mention constitution.md. This means T006 has no spec-level traceability. Impact: **medium** — the task is reasonable but ungrounded in the spec.

- **[Summary Index summary exceeds character limit]**: The data-model.md (L29) specifies Summary must be "<100 chars." The actual summary in the catalog — "Do not create tracking documents that duplicate computable state" — is 65 characters, so it passes. However, neither the catalog's Maintenance section nor any tooling enforces this constraint. For future entries, the 100-char limit could silently be violated. Impact: **low** — not a current violation, but a durability gap.

- **[No deprecation example in seed]**: The spec defines a deprecation flow (FR-009, data-model.md L84-98), the contract documents it (catalog-format.md L82-87), and the Maintenance section documents it (catalog.md L66-71). But there is no example of a deprecated entry in the catalog. While this is expected for a seed with only one active entry, User Story 3 acceptance scenario testing would benefit from a deprecated example to verify the Summary Index exclusion behavior. Impact: **low** — correct for initial seed but untested.

### Off-Base Assumptions

- **[Spec assumes only SKILL.md/templates as integration points]**: The spec at L109 states: "Agent prompt integration means adding a brief instruction to conversus SKILL.md or templates — not modifying the agents' core behavior." The plan (plan.md L62) and tasks (tasks.md T006, L52) extend this to include `.specify/memory/constitution.md`. This is not wrong per se — the constitution update is a cross-reference, not a behavioral modification — but the spec's scoping statement does not account for it. The plan made the right call to include the constitution reference, but the spec should have listed constitution.md as an affected artifact. The correct understanding: any artifact that agents read as context before deliberation is an integration point, including the constitution.

### Actionable Recommendations

1. **Fix broken example path** (Priority: P1)
   - **Current state**: catalog.md L33 references `specs/001-antipattern-steering/examples/redundant-cache/`. This path does not exist.
   - **Proposed change**: Replace with `specs/010-antipattern-steering/examples/redundant-cache/` throughout the catalog entry's Example section.
   - **Rationale**: The actual directory is at `specs/010-antipattern-steering/examples/redundant-cache/` (verified via filesystem). FR-004 requires entries to be self-contained; a broken path violates this. SC-004 requires references to real observed incidents; a nonexistent path fails verification. [tasks.md T011, L77: "catalog entry Example section references valid paths in `specs/001-antipattern-steering/examples/redundant-cache/`" — this task checkpoint itself has the wrong path].
   - **Risk if ignored**: The only concrete example reference in the seed entry leads nowhere. Agents and humans following the reference will not find the supporting evidence, undermining the entry's credibility and self-containedness.

2. **Acknowledge constitution Principle IV tension** (Priority: P2)
   - **Current state**: Constitution L73-75 mandates STATUS.md maintenance. The `redundant-cache` antipattern warns against this exact practice. No artifact acknowledges the contradiction.
   - **Proposed change**: Add a note to the "Known Antipatterns" section of constitution.md (L179-192) acknowledging that Principle IV's STATUS.md reference predates the antipattern catalog and should be reviewed in a follow-up spec (e.g., as a spec 012 or similar hygiene item). Alternatively, add a "When This Does NOT Apply" entry in the antipattern for the specific STATUS.md usage that Principle IV mandates.
   - **Rationale**: Agents encounter both the constitution mandate and the antipattern warning. Without reconciliation, an agent faces contradictory instructions — exactly the kind of ambiguity the antipattern system is meant to resolve. [plan.md L29: "No existing interfaces modified; catalog is a new artifact. SKILL.md additions are additive" — the plan intended no changes to existing content, but the tension remains].
   - **Risk if ignored**: An agent following the antipattern check may refuse to update STATUS.md, violating Principle IV. Or an agent following Principle IV may create exactly the redundant cache the antipattern warns against. The contradiction will surface in the next deliberation that touches cross-spec status.

3. **Add spec traceability for constitution update** (Priority: P2)
   - **Current state**: T006 updates the constitution's Known Antipatterns section, but spec.md L109 limits integration points to "SKILL.md or templates." The constitution update has no spec-level acceptance scenario.
   - **Proposed change**: Either (a) add a note to the spec's Assumptions section acknowledging constitution.md as an integration point, or (b) add a brief User Story 2 acceptance scenario: "Given the constitution governs agent behavior, When the antipattern catalog is created, Then the constitution references the catalog location so agents encounter it via multiple paths."
   - **Rationale**: Scope-boundary integrity requires that every implementation task traces to a spec requirement. T006 is reasonable but ungrounded. [tasks.md T006, L52: "Update the 'Known Antipatterns' section in `.specify/memory/constitution.md`"].
   - **Risk if ignored**: Future scope-boundary reviews will flag T006 as an over-scope violation. The task's legitimacy is clear from context, but formal traceability prevents ambiguity.

4. **Fix path reference in tasks.md T003 and T011** (Priority: P2)
   - **Current state**: tasks.md T003 (L38) and T011 (L77) reference `specs/001-antipattern-steering/examples/redundant-cache/`. This is the same broken path as in the catalog.
   - **Proposed change**: Replace with `specs/010-antipattern-steering/examples/redundant-cache/` in both task descriptions.
   - **Rationale**: While tasks.md is a design artifact (not a runtime artifact), it serves as the implementation record. Cross-references must be valid for future verification passes. [tasks.md T011, L77: validation task itself has the wrong path, making the validation checkpoint unreliable].
   - **Risk if ignored**: Future validation runs using T011 as a checklist will check the wrong path and incorrectly report success or failure.

5. **Verify Summary Index keyword-to-entry consistency on future additions** (Priority: P2)
   - **Current state**: The current seed entry has matching keywords between Summary Index (L10) and entry Keywords section (L53). The Maintenance section (L62) documents the requirement but there is no automated validation.
   - **Proposed change**: Add a Maintenance section bullet: "Verify Keywords in the Summary Index row exactly match the entry's Keywords section — mismatches break keyword-based retrieval."
   - **Rationale**: FR-007 requires keyword tags for retrieval. data-model.md L33 requires "bidirectional sync" between the Summary Index and entries. As the catalog grows, manual sync becomes error-prone. An explicit reminder in the Maintenance instructions reduces the risk. [data-model.md, L33: "Every active Antipattern Entry must have a corresponding row (bidirectional sync)"].
   - **Risk if ignored**: A future entry could have mismatched keywords, causing the Summary Index to return results the full entry does not support, or vice versa.

6. **Confirm no template changes were made** (Priority: P3)
   - **Current state**: The scope explicitly excludes template changes. Filesystem examination confirms no files in `templates/` were modified.
   - **Proposed change**: No change needed — this is a confirmation that the implementation correctly stayed in scope. Record this as a passed verification in the scope-boundary checklist.
   - **Rationale**: [plan.md L29: "No existing interfaces modified." spec.md L109: "not modifying the agents' core behavior"]. Templates are the primary behavioral contract for deliberation agents; any template change would be a major scope violation.
   - **Risk if ignored**: None — this is already correct.

7. **Add explicit scope-boundary note about phase execution** (Priority: P3)
   - **Current state**: The plan's Constitution Check (plan.md L32) states "Feature does not modify phase execution or output validation" for Principle V. This is accurate — no phase execution logic was changed.
   - **Proposed change**: The tasks.md or a verification checklist should include an explicit checkpoint: "Verify no changes to templates/, no changes to phase execution steps in SKILL.md beyond the Antipattern Check insertion." This makes the out-of-scope boundary explicit for future audits.
   - **Rationale**: The Antipattern Check is positioned between Step 1 and Step 2 of SKILL.md execution. A careless edit could accidentally modify Step 1 or Step 2. An explicit checkpoint prevents drift. [tasks.md T010, L76: validation task checks FRs but does not explicitly verify no out-of-scope changes].
   - **Risk if ignored**: Low — the current implementation is clean, but future modifications to the Antipattern Check section could accidentally bleed into adjacent SKILL.md content.

### Referenced Documentation

- `conversus/specs/010-antipattern-steering/spec.md` — sections/lines cited: L6, L20-22, L36-38, L52-53, L69-72, L76-78, L80-83, L86-87, L106-110
- `conversus/specs/010-antipattern-steering/data-model.md` — sections/lines cited: L9-20, L24-35, L37-61, L84-98
- `conversus/specs/010-antipattern-steering/contracts/catalog-format.md` — sections/lines cited: L9-60, L66-80, L82-87, L89-103
- `conversus/specs/010-antipattern-steering/tasks.md` — sections/lines cited: L25, L37-39, L51-53, L64-66, L76-77
- `conversus/specs/010-antipattern-steering/plan.md` — sections/lines cited: L8, L13, L20, L29-36, L57-67, L70-77
- `conversus/antipatterns/catalog.md` — sections/lines cited: L1-71 (entire file)
- `conversus/SKILL.md` — sections/lines cited: L196-210
- `conversus/.specify/memory/constitution.md` — sections/lines cited: L57-58, L69-75, L179-192
- `conversus/specs/010-antipattern-steering/examples/redundant-cache/README.md` — sections/lines cited: L1-60
