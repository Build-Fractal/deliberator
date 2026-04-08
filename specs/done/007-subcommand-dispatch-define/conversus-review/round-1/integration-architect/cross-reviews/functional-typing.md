# Cross-Review: functional-typing's Phase 1 Review

**Cross-reviewer**: integration-architect
**Reviewing**: functional-typing's review of 007-subcommand-dispatch-define
**Scope**: Integration architecture perspective on structural correctness and specification compliance findings

---

## Dangerous Contradictions

### 1. Dispatch precedence: fallback-to-run vs. error-on-unknown

functional-typing recommends (Rec #1) that non-matching first arguments should be treated as config file paths routed to `run`: "subcommand matching requires an exact string match... partial matches or matches with file extensions are treated as config paths passed to the default `run` handler." This means `/conversus my-config.yml` silently routes to `run my-config.yml`.

My review (Alignment, "Backward compatibility preservation") treats the no-arguments default to `run` (SKILL.md L26) and the unknown-subcommand error (SKILL.md L31-32) as two distinct, correct behaviors -- one for empty input, one for unrecognized input. The dispatch table at L22-27 has exactly three rows: `run [config]`, `define [description]`, and no-arguments. The unknown-subcommand error at L31-32 is a fourth case that fires when the first argument matches none of the above.

functional-typing's fallback-to-run proposal would **eliminate the error path entirely for file-like arguments**. If a user types `/conversus definee` (typo), functional-typing's rule would route this to `run` with `definee` as the config path, where the engine would fail at Step 1 with "Config file not found: definee" -- a confusing error unrelated to the actual mistake. The current behavior (SKILL.md L31-32) would instead produce "Unknown subcommand: 'definee'. Available commands: run, define." which is immediately actionable.

The contradiction: functional-typing wants ambiguous first arguments to silently route to `run`; the existing SKILL.md behavior treats all non-matching first arguments as errors. My view is that the error path is the safer default. The spec (FR-003) says no-arguments defaults to `run`; FR-004 says unknown subcommands produce errors. A `run.yml` argument is not "no arguments" -- it is an unknown subcommand under FR-004. If the user wants to pass a config to `run`, the explicit invocation `/conversus run my-config.yml` (SKILL.md L24) is unambiguous.

**Resolution needed**: The spec should clarify whether the dispatch table at L22-27 is exhaustive (all other inputs trigger FR-004 errors) or whether there is an implicit fallback for file-path-like strings. I recommend keeping the error path and adding a suggestion: "Unknown subcommand: 'run.yml'. Did you mean: `/conversus run run.yml`?"

### 2. Schema validation: post-write check vs. no validation

My review (Rec #1, P1) recommends post-write schema validation for `problem.md` -- verifying all 7 required headings exist after the file is written, mirroring the engine's template validation at L286-295 and output validation at L659-676. functional-typing does not raise this concern at all. Their schema coverage analysis (Alignment, "Schema fidelity") concludes that the schema is "character-for-character identical" between spec and SKILL.md but does not consider whether the agent's generated output will actually conform to that schema at runtime.

This is not a disagreement about what the spec says -- it is a disagreement about what it omits. functional-typing's analysis is correct that the schema definition is faithful. My concern is that a faithful schema definition without runtime validation is like a type declaration without a type checker: it documents intent but does not enforce it. The engine enforces its own schemas (L286-295 template validation, L659-676 Phase 6 output validation). The define handler does not.

The danger is real because the define handler uses LLM generation (not template filling) to produce `problem.md`. Template filling is structurally constrained; LLM generation is not. An agent that omits `## Constraints` or writes `## Constraint` (singular) produces a file that looks valid but breaks downstream parsing by `/conversus interests` and `/conversus mode`.

**Resolution needed**: This is my highest-priority finding. functional-typing's silence on it does not mean disagreement -- it likely falls outside the "structural correctness" lens. But both perspectives should converge on adding a validation step.

---

## Tensions

### 1. Empty-section handling: [CLARIFY:] tags vs. sentinel values

functional-typing (Off-Base Assumptions, bullet 2; Rec #5, P2) identifies that SKILL.md L854 only covers empty-section handling for Source Documents and Open Questions, not Constraints or Success Criteria. They recommend adding `[CLARIFY:]` tags for empty Constraints and Success Criteria sections.

My review does not address empty-section handling directly, but my Rec #1 (post-write schema validation) implicitly covers this: a validation step that checks for required headings would catch completely missing sections. However, it would not catch present-but-empty sections -- a `## Constraints` heading with no bullet points beneath it passes heading validation but is semantically empty.

The tension: functional-typing wants the agent to proactively fill empty sections with `[CLARIFY:]` tags (a content-level concern); I want a structural check that headings exist (a schema-level concern). These are complementary, not contradictory. Both should be implemented. The `[CLARIFY:]` approach is consistent with FR-010 (SKILL.md L852: "Any field where the agent cannot confidently determine the content MUST include a `[CLARIFY: ...]` tag"), which already covers this case -- functional-typing is pointing out that the spec's own rule at L852 should logically apply to Constraints and Success Criteria even though the explicit empty-section rules at L854 only name Source Documents and Open Questions.

**Assessment**: functional-typing's recommendation is well-grounded in FR-010 and strengthens the spec. My schema validation recommendation operates at a different layer. Both should be adopted.

### 2. Frontmatter change acknowledgment: spec drift vs. integration surface

functional-typing (Off-Base Assumptions, bullet 1; Rec #3, P2) flags that the SKILL.md frontmatter `description` field was updated to mention subcommands (L9-10) but this change is not documented in the spec's "what changes" section (spec L17). They call this a spec trustworthiness issue.

My review (Alignment, "Dispatch table structure"; Additional Verification, "No existing content modified") explicitly notes the frontmatter change -- "the git diff shows exactly three change regions: (1) description field in frontmatter expanded to mention subcommands" -- but treats it as an expected consequence of adding subcommand dispatch, not as an omission.

The tension is about what the spec owes its readers. functional-typing views the spec as a change manifest that must enumerate every modified line; I view it as a behavioral contract where the frontmatter change is an obvious corollary of adding subcommands. functional-typing is technically correct: the spec says "What changes: SKILL.md gains a 'Subcommand Dispatch' section..." and does not mention the frontmatter update. However, the frontmatter `description` is the skill's external interface -- agent runtimes use it for discovery and matching (SKILL.md L3-10, `compatibility` field at L11-13). Changing it changes how the skill presents itself to the agent runtime.

**Assessment**: functional-typing's point has merit specifically because the frontmatter is an integration surface. I agree the spec should acknowledge it, even if briefly: "The frontmatter `description` is updated to list supported subcommands." One sentence resolves the gap.

### 3. Refine semantics: detailed merge rules vs. the current ambiguity

My review (Rec #2, P1) calls out that SKILL.md L791 "incorporate the user's new input while preserving existing structure" is operationally underspecified and proposes detailed merge rules: Decision is replaced, Constraints are merged and deduplicated, Open Questions are merged with resolved ones removed, Type is re-evaluated, Source Documents are unioned, Context is rewritten.

functional-typing does not flag refine semantics as a concern. Their analysis of the Existing File Check (Alignment, FR-to-section mapping) confirms that L788-793 satisfies FR-011 without questioning the granularity of the refine behavior.

The tension: functional-typing accepts the current refine specification as sufficient for FR-011 compliance; I argue it is insufficient for implementation consistency. FR-011 says "present it and ask whether to refine or replace" -- functional-typing correctly confirms this is implemented. But "refine" without operational definition means different agent models will merge differently, making the command non-deterministic in a way that undermines user trust. The engine specifies exact merge semantics for presets (SKILL.md L180-184: "Inline overrides apply"); the define handler's refine operation should be equally precise.

**Assessment**: Both positions are internally consistent. functional-typing is right that FR-011 is satisfied as written. I am right that the spec should say more. This tension resolves in favor of adding specificity -- not because functional-typing is wrong, but because the current spec leaves too much to implementation discretion for a user-facing operation.

### 4. Multiple --context paths: scope of spec 007

Both reviews identify the single-path limitation of `--context`. functional-typing (Rec #8, P3) asks for clarification on whether multiple paths are supported. My review (Rec #3, P2) more aggressively proposes supporting `--context path1 --context path2`, arguing alignment with the engine's multi-target resolution at L57-68.

The tension is priority. functional-typing treats this as a clarification (P3 -- just state the constraint). I treat it as a design gap (P2 -- add the capability). functional-typing's reasoning is sound: spec 007 says `--context <path>` singular, and documenting the constraint is sufficient for this spec. My reasoning is also sound: the engine already supports multi-target, and forcing users to consolidate context documents into a single directory creates a maintenance burden.

**Assessment**: functional-typing's conservative reading is appropriate for spec 007's scope. Multi-path support is a feature enhancement better deferred to a follow-up spec or addressed when `/conversus interests` is specified (since it will also need to consume multiple documents). For spec 007, documenting the single-path constraint (functional-typing's Rec #8) is the right move.

### 5. --context path validation: same finding, different framing

functional-typing (Rec #2, P1) and my review (Rec #8, P3) both identify that `--context` path validation is missing from the define handler. functional-typing rates it P1; I rate it P3. The difference is perspective: functional-typing evaluates this as a structural completeness gap (the run handler validates paths at L195-196 but the define handler does not), while I frame it as an error-handling edge case.

Reconsidering against the evidence, functional-typing's priority is more appropriate. SKILL.md L195-196 establishes a clear pattern: "All resolved `TARGET_FILES` exist" and "All agent `docs` paths exist." The define handler's `--context` is functionally equivalent to `docs` in the engine. Breaking this validation pattern is an internal inconsistency, not just an edge case. The user impact is also significant: a mistyped `--context` path silently produces a `problem.md` without the intended context, and nothing in the output indicates the context was missing.

**Assessment**: I concede that P1 is the correct priority for `--context` path validation. functional-typing's framing (structural parity with the run handler's validation discipline) is more compelling than my initial assessment.

---

## Safe Agreements

### 1. Dispatch table completeness and correctness

Both reviews confirm the dispatch table at SKILL.md L18-33 correctly implements FR-001 through FR-004. functional-typing: "The dispatch table covers all four routing cases required by the spec" (Alignment, bullet 1). My review: "The routing table uses a markdown table with Invocation and Routes to columns, with anchor links to handler sections" (Alignment, bullet 1). We both verify that the backward-compatible default (L26) matches FR-003 and SC-004. No disagreement on the table's structure or completeness.

### 2. Run path behavioral preservation

Both reviews confirm that the heading renames (`## Input` to `## Run: Input`, `## Execution` to `## Run: Execution`) are the only modifications to the existing engine content, and that all body text is unchanged. functional-typing: "All content beneath these headings is untouched -- Step 1 through Step 5, template variables, phase execution, arbitration, dispute parsing, and the report format are identical" (Alignment, bullet 3). My review: "the git diff confirms only two heading renames touched the existing engine content... The body text of both sections is unchanged" (Alignment, bullet 2). We agree this satisfies FR-002 and SC-003.

### 3. Schema fidelity between spec and SKILL.md

functional-typing: "The `problem.md` schema in the define handler's Output section reproduces the spec's schema exactly: same heading hierarchy... same placeholder text, same `[CLARIFY: ...]` tag syntax" (Alignment, bullet 4). My review's FR-to-Implementation Mapping (FR-009) confirms the same. The schema at SKILL.md L824-850 matches spec L45-71 exactly.

### 4. Handler isolation (define is self-contained)

My review (Alignment, bullet 3): "The define handler is a self-contained section... It references zero engine internals -- no template variables, no phase numbers, no mode logic, no Agent tool dispatching." functional-typing does not use the term "handler isolation" but confirms the same property implicitly through their FR-to-section mapping, which shows all define handler references fall within L769-876 with no cross-references to engine sections. Both reviews agree this clean separation prevents the define handler from accidentally regressing the engine.

### 5. Define should be documented as a single-agent command

functional-typing (Missed Opportunities, bullet 5; Rec #6, P2): "The `define` handler should explicitly state: 'The define command executes in the main conversation. No subagents are launched.'" My review (Rec #7, P3): "Add a note at the top of the define handler (after L771): 'This command runs in the main conversation thread. It does not dispatch sub-agents.'" The wording differs; the recommendation is identical. Both ground it in the contrast with the engine's prominent NON-NEGOTIABLE MULTI-AGENT RULES at L312-324.

### 6. Full FR coverage confirmed

Both reviews independently verify that all 12 functional requirements (FR-001 through FR-012) are satisfied in SKILL.md. functional-typing provides an FR-to-section mapping in their Alignment section; my review provides a tabular FR-to-Implementation Mapping with line references and satisfaction status. No FR is flagged as unsatisfied by either review.

### 7. Error message pattern consistency

functional-typing (Alignment, bullet 1): The unknown-subcommand error message (L31-32) "matches FR-004." My review (Alignment, bullet 5): "The unknown subcommand error message follows the same pattern as engine validation errors (name the problem, show the available options)." We agree the error format is correct and consistent with existing patterns.

---

## Summary

The two reviews are largely aligned on what spec 007 gets right (dispatch table, backward compatibility, schema fidelity, FR coverage, handler isolation). The most significant divergence is on dispatch precedence for ambiguous first arguments -- functional-typing wants fallback-to-run, I argue for preserving the error path. The most significant gap in functional-typing's review from my perspective is the absence of post-write schema validation for `problem.md`, which I rate P1. Conversely, functional-typing's P1 rating for `--context` path validation is better justified than my P3 rating -- I concede their priority is correct. On refine semantics, our disagreement is about sufficiency: functional-typing accepts FR-011 as satisfied by the current text, while I argue the operational detail is insufficient for consistent implementation. Both positions are defensible; the resolution favors adding specificity.
