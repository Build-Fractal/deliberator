# Phase 1 Compliance Audit — P2/P3 Backlog Hardening (Spec 005)

**Auditor**: compliance-auditor
**Date**: 2026-03-20
**Scope**: Tasks T001-T005 (verification of 10 fully-implemented FRs + 1 partial FR-011)

---

### Executive Summary

Spec 005 is a hardening specification that adds safety gates, output validation, shared subsystem documentation, and status-tracking infrastructure to the conversus multi-agent deliberation system. Its Phase 1 work is strictly verification: confirming that 10 functional requirements previously implemented in SKILL.md and the template files remain correct. The spec correctly identifies which FRs are done, which are partial, and which remain. My audit verifies each FR against the actual file contents.

The audit finds all 10 fully-implemented FRs satisfied. FR-001 (draft markers on non-cooperative templates) is present and correct. FR-002/FR-003 (SKILL.md Step 3 draft check) are correctly placed before variable substitution. FR-004/FR-005/FR-006 (Phase 6 output validation) are correctly specified as non-blocking warnings. FR-010 (Dispute-Parsing Subsystem documentation) is thorough, with input/output/parsing rules and a stable-interface contract. FR-018 (Baseline Features) documents all seven organic features. FR-011 is confirmed partial exactly as expected: the Round Termination Check (L459-469) and Trigger Evaluation (L531-542) both use inline parsing logic rather than cross-referencing the Dispute-Parsing Subsystem section (L641-668).

The single most important recommendation: T019/T019a (Phase 4 tasks to remediate FR-011) must explicitly verify that the replacement cross-references produce identical parsing behavior to the inline logic they replace, since the inline logic in Round Termination Check (L460, L467) omits structural-marker support that the Dispute-Parsing Subsystem specifies as primary.

---

### Alignment

- **[T001 / FR-001 — Draft markers present]** (spec.md L200-202): All three non-cooperative arbitration templates contain `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` as their first line. Winner-take-all (L1), red-blue (L1), and prisoners-dilemma (L1) all have the marker. The cooperative template (L1) correctly does NOT have the marker. This directly satisfies FR-001 and all four acceptance scenarios in US1. [`templates/winner-take-all/arbitration.md, L1`; `templates/red-blue/arbitration.md, L1`; `templates/prisoners-dilemma/arbitration.md, L1`; `templates/cooperative/arbitration.md, L1`]

- **[T002 / FR-002, FR-003 — Draft check in Step 3]** (spec.md L203-204): SKILL.md L249 contains the draft marker check with the correct error message: "Template {path} is marked as draft and cannot be used in production runs. This template requires a separate game-dynamics analysis spec before activation." This check occurs in Step 3 (Load Templates), after template file existence validation (L247) but before Step 4 (Execute Phases), which is where variable substitution happens. FR-003's requirement that the check occur before variable substitution is satisfied by placement. [`SKILL.md, L249`]

- **[T003 / FR-004, FR-005, FR-006 — Output validation]** (spec.md L207-210): SKILL.md L581 specifies post-Phase-6 output validation checking four required headings: "Process Note", "Decision Framework", "Binding Decisions", "Summary of Changes Required". L581 explicitly states "The warning is informational — it does not block the file from being written or the conversus run from completing." This satisfies FR-006 (non-blocking). The warning message format names missing headings, satisfying FR-005. [`SKILL.md, L581`]

- **[T004 / FR-010 — Dispute-Parsing Subsystem]** (spec.md L220): SKILL.md L641-668 documents the Dispute-Parsing Subsystem as a standalone shared section with: input specification (synthesis file path, L645), dual outputs (boolean and integer count, L647-649), three-tier parsing rules (structural markers primary, heading fallback, default safety, L651-664), heading matching semantics (L666), and stable-interface contract (L668). This fully satisfies FR-010's requirements for input, output, parsing rules, and stable interface. [`SKILL.md, L641-668`]

- **[T005 / FR-018 — Baseline Features]** (spec.md L246): SKILL.md L692-704 contains the "Baseline Features (organic, pre-spec)" section listing seven features: `iterations` field, `prior:` context mechanism, multi-file target resolution, path-list variable formatting, template variable substitution, background agent dispatch, and non-negotiable multi-agent rules. FR-018 requires documentation of "context mechanism, iterations field, path-list formatting rules, multi-file target resolution." All four are present, plus three additional features. [`SKILL.md, L692-704`]

- **[FR-011 partial — confirmed as expected]** (spec.md L221, assumptions L278): The Round Termination Check (L459-469) uses inline parsing: "Find the `### Remaining Disputes` heading and count `**Dispute:` entries under it" (L460) and "count `**Dispute:` entries under `### Remaining Disputes`" (L467). The Trigger Evaluation (L531-542) similarly defines its own inline parsing with mode-specific headings. Neither cross-references the Dispute-Parsing Subsystem section (L641-668). This matches the spec's assumption (L278): "SKILL.md Round Termination Check still uses inline dispute-counting logic independent of the Dispute-Parsing Subsystem." [`SKILL.md, L460, L467, L534, L537-540`; `spec.md, L278`]

---

### Missed Opportunities

- **[Heading-level specificity gap in output validation]**: FR-007 (spec.md L211) requires heading validation to be "case-insensitive and match as substring within heading lines." SKILL.md L581 specifies the four required headings and warning behavior, but does NOT currently specify case-insensitive matching or heading-level flexibility. T003 verifies FR-004/005/006 (which are satisfied), but FR-007 is not yet implemented — it is correctly deferred to T013 (Phase 4). The Phase 1 verification scope is correct in excluding FR-007, but the tasks document (T003 description, tasks.md L26) does not explicitly note that FR-007 is out of scope for Phase 1. This could cause confusion if an auditor reads T003 and checks for FR-007. Impact: low. [`spec.md, L211`; `tasks.md, L26`; `SKILL.md, L581`]

- **[Inline parsing inconsistency between Round Termination and Dispute-Parsing Subsystem]**: The Round Termination Check (L459-460) hardcodes `### Remaining Disputes` with a triple-hash heading level, while the Dispute-Parsing Subsystem (L666) specifies "Heading lookups are case-insensitive and match any heading level." The inline logic is less flexible than the shared subsystem it should reference. T019 (tasks.md L86) will replace the inline logic with a cross-reference, but the tasks document does not explicitly flag this behavioral difference as a concern. When the cross-reference is made, the heading-level flexibility of the Dispute-Parsing Subsystem will effectively expand the parsing semantics — this may be intentional, but it is not documented as such. Impact: medium. [`SKILL.md, L460 vs L666`; `tasks.md, L86`]

- **[Structural-marker support absent from inline Round Termination logic]**: The Dispute-Parsing Subsystem (L651-656) specifies structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`) as the primary parsing method, with heading-based parsing as fallback. The inline Round Termination Check (L459-460) only uses heading-based parsing — it has no structural-marker support. When T019 replaces the inline logic with a cross-reference, the Round Termination Check will gain structural-marker support as a side effect. This is an implicit behavioral change that should be explicitly acknowledged. Impact: medium. [`SKILL.md, L459-460 vs L651-656`; `tasks.md, L86`]

- **[Cooperative template lacks `{REMAINING_DISPUTES}` section context]**: The cooperative arbitration template (L34-40) includes a `{REMAINING_DISPUTES}` variable section with instructions to use extracted disputes. The output validation (L581) checks for "Summary of Changes Required" as a required heading, but the cooperative template (L94-101) uses "### Summary of Changes Required" while the spec (FR-004, spec.md L208) lists "Summary of Changes Required" without specifying heading level. This alignment is correct because heading validation ignores level, but this detail depends on FR-007 (not yet implemented). Until FR-007 is implemented, the output validation semantics for heading-level matching are unspecified in SKILL.md. Impact: low. [`templates/cooperative/arbitration.md, L94-101`; `SKILL.md, L581`; `spec.md, L208, L211`]

- **[No verification of `Confidence Assessment` heading in output validation]**: The cooperative arbitration template (L104-111) instructs the arbiter to produce a "Confidence Assessment" section. FR-004 (spec.md L208) only requires four headings: "Process Note", "Decision Framework", "Binding Decisions", "Summary of Changes Required." The "Confidence Assessment" section is instructed by the template but not validated by the engine. This is not a bug — the spec intentionally limits validation to the most critical sections — but it represents an opportunity to catch additional malformed output. Impact: low. [`templates/cooperative/arbitration.md, L104-111`; `spec.md, L208`]

- **[Stagnation detection does not support structural markers]**: The tasks document (T008, tasks.md L63) notes: "stagnation detection does not support structural-marker parsing (only heading-based)." This is accurate per the current Round Termination Check (L459-469). However, after T019 replaces the inline logic with a cross-reference to the Dispute-Parsing Subsystem, stagnation detection WILL gain structural-marker support. The T008 note in STATUS.md will become inaccurate after T019 is completed. There is no task to update STATUS.md after T019. Impact: medium. [`tasks.md, L63, L86`; `SKILL.md, L459-469, L641-668`]

---

### Off-Base Assumptions

- **[Assumption: FR-011 partial status is solely about Round Termination Check]** (spec.md L278): The spec states "FR-011 is partially complete: STATUS.md cross-reference exists but SKILL.md Round Termination Check still uses inline dispute-counting logic independent of the Dispute-Parsing Subsystem." This is correct but incomplete. The Trigger Evaluation section (SKILL.md L531-542) ALSO uses inline parsing logic independent of the Dispute-Parsing Subsystem. The tasks document correctly addresses both locations — T019 targets Round Termination (L86) and T019a targets Trigger Evaluation (L87) — but the spec's assumption only mentions Round Termination. The assumption should acknowledge both inline-parsing sites. [`spec.md, L278`; `SKILL.md, L531-542`; `tasks.md, L86-87`]

- **[Assumption: Draft marker error message matches exactly]** (spec.md L203): FR-002 specifies the error message as "Template {path} is marked as draft and cannot be used in production runs." SKILL.md L249 actually contains a longer message: "Template {path} is marked as draft and cannot be used in production runs. This template requires a separate game-dynamics analysis spec before activation." The SKILL.md message is a superset of the FR-002 message. This is not a failure — the FR's required text is present as a prefix — but the spec and the implementation do not match exactly. The spec should either update FR-002 to reflect the full message or explicitly state that the message must contain the specified text (substring match). [`spec.md, L203`; `SKILL.md, L249`]

---

### Actionable Recommendations

1. **Update FR-002 error message to match SKILL.md** (Priority: P2)
   - **Current state**: FR-002 (spec.md L203) specifies: "Template {path} is marked as draft and cannot be used in production runs."
   - **Proposed change**: Update FR-002 to: "Template {path} is marked as draft and cannot be used in production runs. This template requires a separate game-dynamics analysis spec before activation." — matching the actual SKILL.md L249 text.
   - **Rationale**: Spec and implementation should match exactly to prevent future auditors from flagging a false discrepancy. [`SKILL.md, L249`]
   - **Risk if ignored**: Minor — a future compliance check could flag the message mismatch as a failure, wasting audit time.

2. **Expand spec assumption about FR-011 partial status** (Priority: P2)
   - **Current state**: Spec assumption (spec.md L278) mentions only Round Termination Check as the site of inline parsing.
   - **Proposed change**: Update L278 to: "FR-011 is partially complete: STATUS.md cross-reference exists but SKILL.md Round Termination Check (L459-469) and Trigger Evaluation (L531-542) both still use inline dispute-counting logic independent of the Dispute-Parsing Subsystem."
   - **Rationale**: Accuracy. The tasks document (T019, T019a) correctly identifies both sites, but the spec assumption should match. [`spec.md, L278`; `tasks.md, L86-87`]
   - **Risk if ignored**: An implementor reading only the spec (not tasks) may think T019 alone fully remediates FR-011, missing the Trigger Evaluation site.

3. **Add behavioral-change note to T019 task description** (Priority: P2)
   - **Current state**: T019 (tasks.md L86) says "replace the inline dispute-counting specification with a cross-reference to the Dispute-Parsing Subsystem section" without noting behavioral implications.
   - **Proposed change**: Append to T019: "Note: This replacement introduces two behavioral changes: (1) structural-marker support is added as the primary parsing method (the inline logic only used heading-based parsing), and (2) heading matching becomes case-insensitive and level-agnostic (the inline logic hardcoded `### Remaining Disputes`). Both changes are intentional — the Dispute-Parsing Subsystem is the authoritative specification."
   - **Rationale**: Explicit documentation of behavioral changes prevents implementors from treating the cross-reference as a pure refactor. [`SKILL.md, L459-460 vs L651-668`]
   - **Risk if ignored**: An implementor may not realize the cross-reference changes parsing behavior, leading to untested behavioral expansion.

4. **Add task to update STATUS.md T008 note after T019 completes** (Priority: P2)
   - **Current state**: T008 (tasks.md L63) instructs adding to STATUS.md: "stagnation detection does not support structural-marker parsing (only heading-based)." This is true before T019 but false after.
   - **Proposed change**: Add a dependency note to T019 or a new sub-task in Phase 5: "After T019: update STATUS.md Dispute-Parsing Subsystem entry to note that stagnation detection now uses the full Dispute-Parsing Subsystem (structural markers primary, heading fallback)."
   - **Rationale**: STATUS.md is a living document (spec.md L286). T008 creates an entry that T019 invalidates. Without a task to update it, STATUS.md becomes stale immediately. [`tasks.md, L63, L86`; `spec.md, L286`]
   - **Risk if ignored**: STATUS.md will contain inaccurate information about the Dispute-Parsing Subsystem's consumers, contradicting the "single-document reference" goal (SC-003).

5. **Clarify T003 scope excludes FR-007** (Priority: P3)
   - **Current state**: T003 (tasks.md L26) says "Verify SKILL.md Phase 6 output validation (L581-582) checks four required section headings with non-blocking warning (US2: FR-004, FR-005, FR-006)." FR-007 is not mentioned.
   - **Proposed change**: Append to T003 description: "(FR-007 heading match semantics deferred to T013, Phase 4)."
   - **Rationale**: Explicit scope exclusion prevents auditors from checking FR-007 in Phase 1 and flagging a false failure. [`tasks.md, L26`; `spec.md, L211`]
   - **Risk if ignored**: Negligible — but explicit scoping is cheap and prevents confusion.

6. **Verify cooperative template headings match FR-004 validation list** (Priority: P3)
   - **Current state**: FR-004 (spec.md L208) lists four required headings. The cooperative template (L50-111) instructs five sections: Process Note, Decision Framework, Binding Decisions, Summary of Changes Required, and Confidence Assessment.
   - **Proposed change**: Add a note to FR-004 or the output validation section: "The validation checks a subset of the template-instructed sections. 'Confidence Assessment' is instructed by the template but not validated — it is a recommended section, not a required one."
   - **Rationale**: Makes the deliberate asymmetry between template instructions and validation explicit. [`templates/cooperative/arbitration.md, L104`; `spec.md, L208`]
   - **Risk if ignored**: A future maintainer may wonder why Confidence Assessment is instructed but not validated, and may add it to the validation list unnecessarily.

7. **Document that non-cooperative template draft messages include game-dynamics note** (Priority: P3)
   - **Current state**: The draft marker error (SKILL.md L249) includes "This template requires a separate game-dynamics analysis spec before activation." This is specific to the draft-marker use case for non-cooperative templates.
   - **Proposed change**: Add to FR-001 or the Key Entities section (spec.md L254): "The draft marker error message is intentionally specific to the non-cooperative template case. If draft markers are used for other purposes in the future, the error message text in SKILL.md Step 3 may need parameterization."
   - **Rationale**: Forward compatibility note. The current error message conflates "draft" with "non-cooperative game dynamics." [`SKILL.md, L249`; `spec.md, L254`]
   - **Risk if ignored**: If draft markers are later used for other template states (e.g., experimental cooperative templates), the error message will be misleading.

---

### Verification Summary Table

| Task | FR(s) | Status | Evidence |
|------|-------|--------|----------|
| T001 | FR-001 | **PASS** | Draft marker present as L1 in all 3 non-cooperative templates; absent from cooperative template |
| T002 | FR-002, FR-003 | **PASS** | SKILL.md L249 has check with correct error message; placement in Step 3 ensures it runs before Step 4 variable substitution |
| T003 | FR-004, FR-005, FR-006 | **PASS** | SKILL.md L581 checks 4 headings, emits per-heading warnings, explicitly non-blocking |
| T004 | FR-010 | **PASS** | SKILL.md L641-668 documents full subsystem: input, outputs, 3-tier parsing, heading matching, stable contract |
| T004 | FR-011 (partial) | **PASS (partial as expected)** | Round Termination (L459-469) and Trigger Evaluation (L531-542) both use inline parsing; remediation deferred to T019/T019a |
| T005 | FR-018 | **PASS** | SKILL.md L692-704 lists 7 baseline features covering all 4 required items plus 3 additional |

**Checkpoint result**: 10 pre-existing FRs verified PASS. 1 partial (FR-011) verified as expected. Remaining 9 FRs (FR-007, FR-008, FR-009, FR-011 remediation, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-019) ready for implementation in Phases 2-5.

---

### Referenced Documentation

- `conversus/templates/winner-take-all/arbitration.md` — sections/lines cited: L1
- `conversus/templates/red-blue/arbitration.md` — sections/lines cited: L1
- `conversus/templates/prisoners-dilemma/arbitration.md` — sections/lines cited: L1
- `conversus/templates/cooperative/arbitration.md` — sections/lines cited: L1, L34-40, L50-111, L94-101, L104-111
- `conversus/specs/005-p2p3-backlog-hardening/spec.md` — sections/lines cited: L200-204, L207-211, L220-221, L246, L254, L278, L286
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` — sections/lines cited: L24-28, L63, L86-87
- `conversus/SKILL.md` — sections/lines cited: L249, L459-469, L531-542, L575-582, L641-668, L666, L692-704
