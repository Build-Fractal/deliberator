# Cross-Review of integration-architect's Review

**Cross-reviewer**: functional-typing
**Target review**: integration-architect's review of 007-subcommand-dispatch-define
**Date**: 2026-03-22

---

### Dangerous Contradictions

- **Dispatch ambiguity handling: implicit pass-through vs. strict error**
  - **integration-architect claims**: The unknown-subcommand error at SKILL.md L31-32 is sufficient and "follows the same pattern as engine validation errors" (Alignment, bullet 5). Their review does not raise dispatch precedence as a concern. The FR-to-Implementation Mapping section marks FR-004 as "Yes" without qualification, accepting the error-on-unknown behavior as complete.
  - **functional-typing claims**: The dispatch table "does not specify what happens when the first argument is a string that could be interpreted as either a subcommand or a config file path" (Missed Opportunities, bullet 1). My P1 recommendation proposes that non-matching first arguments should be treated as config file paths routed to `run` rather than triggering an error: "If it does not exactly match any known subcommand, it is treated as a config file path and routed to `run`" (Actionable Recommendations, item 1).
  - **Why this is dangerous**: Integration-architect's review implicitly endorses the current behavior where `/conversus my-config.yml` would produce "Unknown subcommand: 'my-config.yml'" -- an error. My review proposes it should silently route to `run`. If both positions inform implementation without resolution, the dispatch semantics are ambiguous: some implementers will error on unrecognized first arguments, others will pass them through to `run`. This is a fundamental routing question that affects every invocation where the user omits the explicit `run` keyword.
  - **Suggested resolution**: The spec should explicitly choose one behavior. The pass-through approach (my position) is more backward-compatible since existing users may already invoke `/conversus config.yml` without the `run` keyword. However, integration-architect's implicit acceptance of strict matching has merit for clarity. The resolution should define exact-match semantics and specify the fallback: either error (strict) or route-to-run (permissive). Either is defensible; ambiguity is not.

- **Post-write validation vs. dispatch precedence as top priority**
  - **integration-architect claims**: Their "most important recommendation" is "add validation that `problem.md` output conforms to its schema before writing" (Executive Summary). Their first P1 recommendation is post-write schema validation for `problem.md` (Actionable Recommendations, item 1), arguing that "downstream commands (`interests`, `mode`) will parse `problem.md` by heading -- a missing section will cause silent failures."
  - **functional-typing claims**: My "most important recommendation" is "add explicit dispatch precedence rules (L31-32) to handle edge cases where the first argument could be interpreted as either a subcommand or a config file path" (Executive Summary). My first P1 recommendation is the dispatch precedence rule (Actionable Recommendations, item 1).
  - **Why this is dangerous**: These are not contradictory in substance -- both could be adopted. The danger is in prioritization. If implementation resources are limited, integration-architect's priority (output validation) addresses a downstream consumption risk, while my priority (dispatch precedence) addresses a routing correctness risk. Implementing output validation without dispatch precedence means the system validates artifacts for a handler it may not correctly route to. Implementing dispatch precedence without output validation means routing is correct but artifacts may be malformed.
  - **Suggested resolution**: Both should be P1. Dispatch precedence is a prerequisite -- it determines whether the define handler is even reached. Output validation is a consequence -- it ensures the handler's product is well-formed. The natural ordering is: fix routing first (dispatch precedence), then validate output (schema check). If only one can be adopted, dispatch precedence is structurally prior.

- **Refine semantics: operational rules vs. unspecified**
  - **integration-architect claims**: The refine behavior is "underspecified" and proposes specific operational rules: "The `## Decision` statement is replaced with the new input's distilled decision. `## Constraints` are merged (existing + new, deduplicated). `## Open Questions` are merged, with resolved questions removed" (Missed Opportunities, bullet 6; Actionable Recommendations, item 2). They propose field-by-field merge semantics with six sub-rules (a through f).
  - **functional-typing claims**: My review does not raise refine semantics as a concern. The Existing File Check section (SKILL.md L788-793) was evaluated as structurally complete per FR-011 (Alignment section, FR-to-section mapping).
  - **Why this is dangerous**: Integration-architect's proposed merge semantics (replace Decision, merge Constraints, union Source Documents, re-evaluate Type) are substantive design decisions that go beyond the spec's requirements. FR-011 requires only that the agent "present it and ask whether to refine or replace" and "Never silently overwrite." The spec intentionally leaves the refinement algorithm to the agent's judgment. If integration-architect's detailed merge rules are adopted as normative, they constrain agent behavior in ways the spec did not intend. If they are not adopted, the behavior remains implementation-defined as my review implicitly accepted.
  - **Suggested resolution**: The spec should define a minimal contract for "refine" (e.g., "all existing sections must be preserved in the output; new information may be added to any section") without prescribing exact merge algorithms. Integration-architect's six sub-rules are useful as implementation guidance but should not be normative -- they over-specify a behavior that benefits from agent flexibility.

### Tensions

- **Multiple `--context` paths: explicit support vs. clarification of single-path constraint**
  - Integration-architect recommends supporting `--context path1 --context path2` as a P2 feature addition, arguing that "the engine's `target:` supports lists" and "forcing users to put all context documents in one directory is an artificial constraint" (Missed Opportunities, bullet 3; Actionable Recommendations, item 3).
  - My review raises the same issue but from the opposite direction: I recommend clarifying that `--context` is single-path-only and stating "To include multiple context sources, point to a directory containing them" (Actionable Recommendations, item 8, P3).
  - These positions create friction: one advocates expanding the interface, the other advocates documenting its current limitation. Both agree the spec is silent on multiplicity. The tension is whether this spec should expand scope (integration-architect) or defer expansion while closing the ambiguity (functional-typing). Given that this is spec 007 and the define command is the first guided workflow command, my position favors shipping a well-specified minimal interface.

- **Pipeline overview: forward reference vs. out of scope**
  - Integration-architect recommends adding a "Pipeline Overview" subsection after the Report section describing all three guided setup commands and how they chain (Actionable Recommendations, item 4, P2). They argue the "Next step" reference at L869 is "a dead end" since `/conversus interests` does not exist yet.
  - My review does not raise this concern. The "Next step: /conversus interests" line at L869 was not flagged because it is a forward reference -- common in incremental spec development. Adding a pipeline overview describing commands that do not yet exist introduces speculative content into an implementation document.
  - The tension is between user comprehension (integration-architect's concern -- users need to know why they are doing this step) and specification discipline (my concern -- SKILL.md should only describe implemented behavior). A compromise would be a single sentence ("This is the first of a series of guided setup commands") without enumerating unimplemented commands.

- **`--type` override flag scope**
  - Integration-architect proposes a `--type` override flag (Actionable Recommendations, item 5, P2) allowing expert users to skip classification.
  - My review does not propose any new flags beyond the existing `--context` and `--output`. Adding `--type` expands the define handler's interface surface in a way that is not motivated by any FR. FR-008 requires classification, not skipping classification.
  - This is a tension between interface minimalism (my implicit position) and expert-user ergonomics (integration-architect's explicit position). The flag is reasonable but is a feature addition, not a gap in the spec.

- **Anchor link fragility: runtime parser vs. GFM assumption**
  - Integration-architect raises concern about anchor link rendering for colon-containing headings (Actionable Recommendations, item 6, P2), noting that "SKILL.md is consumed by an agent runtime, not GitHub" and the runtime's markdown parser must follow the same slug algorithm.
  - My review mentions the anchor links only to confirm they work (Alignment, bullet 3: "All content beneath these headings is untouched") but does not raise parser compatibility as a concern.
  - The tension is real but low-impact for this spec. If the agent runtime does not follow GFM slug rules, the entire dispatch table breaks -- not just the define handler. This is a platform concern, not a spec concern.

- **Frontmatter change acknowledgment**
  - My review flags the frontmatter `description` field update (SKILL.md L3-10) as an undocumented change that should be acknowledged in the spec (Actionable Recommendations, item 3, P2). The spec says "The existing `/conversus run` handler is unchanged" but does not mention the description field.
  - Integration-architect's review notes the frontmatter change positively in the Additional Verification section ("description field in frontmatter expanded to mention subcommands (L9-10)") but does not flag it as an omission from the spec.
  - The tension is about spec completeness: I treat it as a gap; integration-architect treats it as obviously correct and not worth flagging. Both positions are defensible, but if the spec is the authoritative record of what changed, it should enumerate all changes.

### Safe Agreements

- **Handler isolation is well-implemented and critical**
  - Integration-architect: "The define handler is a self-contained section between `---` horizontal rules. It references zero engine internals -- no template variables, no phase numbers, no mode logic, no Agent tool dispatching" (Alignment, bullet 3).
  - Functional-typing: "All content beneath these headings is untouched -- Step 1 through Step 5, template variables, phase execution, arbitration, dispute parsing, and the report format are identical to their pre-dispatch state" (Alignment, bullet 3).
  - Both reviews independently verified handler isolation from complementary angles: integration-architect confirmed the define handler does not reach into the engine; I confirmed the engine was not modified by the define handler. This bidirectional verification strengthens confidence that the dispatch mechanism is non-invasive.

- **`--context` path validation is missing and needed**
  - Integration-architect: "Add error handling for unreadable context documents" (Actionable Recommendations, item 8, P3), proposing fail-on-nonexistent and warn-on-unreadable semantics.
  - Functional-typing: "Add `--context` path validation to define handler" (Actionable Recommendations, item 2, P1), proposing fail-on-nonexistent and warn-on-empty-directory semantics.
  - Both reviews independently identified the same gap: SKILL.md L797-802 specifies context ingestion behavior but not failure behavior. The run handler validates paths at L195-196; the define handler should do the same. The difference in priority (P3 vs. P1) reflects different risk assessments, but the recommendation is convergent.

- **Schema fidelity between spec and SKILL.md is exact**
  - Integration-architect: Verified all 12 FRs against SKILL.md implementation in a detailed FR-to-Implementation Mapping table, marking all as "Yes" with specific line citations.
  - Functional-typing: "The `problem.md` schema in SKILL.md (L824-850) is character-for-character identical to the spec's schema (spec L45-71)" (Alignment, bullet 4). Separately verified all FR-to-section mappings (Alignment, bullet 5).
  - Both reviews independently confirmed full FR coverage with no schema drift. This is the strongest agreement in both reviews and provides high confidence that the implementation is spec-compliant.

- **Single-agent execution model should be stated explicitly**
  - Integration-architect: "Document that define does not use the Agent tool" (Actionable Recommendations, item 7, P3), proposing a note that "This command runs in the main conversation thread. It does not dispatch sub-agents."
  - Functional-typing: "Explicitly state that `define` is a single-agent command" (Actionable Recommendations, item 6, P2), proposing nearly identical text: "This command executes entirely in the main conversation. No subagents are launched."
  - Both reviews identified the same implicit assumption and proposed the same fix. The priority difference (P3 vs. P2) is minor. The convergence on exact wording reinforces that this is an obvious gap worth closing.
