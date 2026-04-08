# Integration Architect Review — 007-subcommand-dispatch-define

## Executive Summary

Spec 007 introduces subcommand dispatch to SKILL.md and implements the first guided workflow command, `/conversus define`. The dispatch mechanism routes based on the first argument after `/conversus`, with `run` preserving the existing deliberation engine and `define` producing a structured `problem.md`. This is foundational infrastructure: every future guided command (`interests`, `mode`, `converge`, `arbitrate`, `gate`) depends on the routing table established here.

The implementation in SKILL.md is faithful to the spec. All 12 functional requirements are represented, the dispatch table is clean, the define handler is self-contained, and no existing engine content was damaged. The heading renames from `## Input` to `## Run: Input` and `## Execution` to `## Run: Execution` are the only modifications to the pre-existing content, and they are correct namespace qualifications needed for multi-handler coexistence. The anchor links resolve properly.

My most important recommendation: add validation that `problem.md` output conforms to its schema before writing, mirroring the template validation pattern already established in the engine's Step 3.

## Alignment

- **Dispatch table structure** (SKILL.md L18-33): The routing table uses a markdown table with `Invocation` and `Routes to` columns, with anchor links to handler sections. This mirrors the existing pattern of using heading anchors for internal cross-references (e.g., engine templates reference phase sections). [SKILL.md, L24-25 for anchor links, L385-429 for Phase 1 as an example of referenced sections].

- **Backward compatibility preservation** (SKILL.md L26): `/conversus` with no arguments defaults to `run`, and the git diff confirms only two heading renames touched the existing engine content (`## Input` to `## Run: Input`, `## Execution` to `## Run: Execution`). The body text of both sections is unchanged. [spec.md, L29 (FR-003); SKILL.md L36-42 vs git diff showing identical body content].

- **Handler isolation** (SKILL.md L769-877): The define handler is a self-contained section between `---` horizontal rules. It references zero engine internals -- no template variables, no phase numbers, no mode logic, no Agent tool dispatching. It reads files, classifies, writes markdown, and reports. This clean separation means the define handler cannot accidentally regress the engine. [SKILL.md, L769-877 define handler; contrast with L300-598 engine execution which uses Agent tool, template variables, phase boundaries].

- **Context ingestion pattern** (SKILL.md L797-802): The `--context` path resolution (file or directory, non-recursive `.md` discovery) reuses the same convention as the engine's target resolution at L102-106. This consistency means users who know how `target:` works in `conversus.yml` will intuit how `--context` works in `define`. [SKILL.md, L102-106 target resolution; L797-802 context ingestion].

- **Error message pattern** (SKILL.md L31-32): The unknown subcommand error message follows the same pattern as engine validation errors (name the problem, show the available options). [SKILL.md, L220 for the engine's validation error style; L31-32 for dispatch error].

## Missed Opportunities

- **No schema validation for problem.md output**: The engine validates templates against `schema/variables.yml` before execution (SKILL.md L286-295). The define handler writes `problem.md` without any post-write validation that all required sections are present. Given that the agent is generating content (not filling templates), a malformed `problem.md` missing `## Type` or `## Constraints` would silently break downstream commands. A lightweight post-write check that all 7 required headings exist would mirror the engine's own validation discipline. Impact: **high**. [SKILL.md, L286-295 template validation; L822-850 problem.md schema].

- **No `--dry-run` flag**: The engine has no equivalent, but `define` is a generative command where the user may want to preview the structured output before committing to disk. A `--dry-run` that prints the `problem.md` content to the console without writing would reduce friction in iterative problem refinement. Impact: **medium**. [spec.md, L34-41 for the input/output flow; SKILL.md L822 "Write problem.md to the output directory"].

- **Multiple `--context` paths not specified**: The engine's `target:` field supports lists (SKILL.md L59-68). The define handler's `--context <path>` is described as singular (spec.md L36, SKILL.md L778). Users often have multiple relevant documents in different directories (e.g., a spec and an architecture doc). Supporting `--context path1 --context path2` or `--context path1,path2` would align with the engine's multi-target capability. Impact: **medium**. [SKILL.md, L57-68 multi-target resolution; L778 single --context path].

- **No connection to conversus.yml generation**: The report section says "Next step: /conversus interests" (SKILL.md L869), but neither this spec nor SKILL.md describes how `problem.md` feeds into `conversus.yml` construction. The define handler is positioned as the "entry point for users who want guided deliberation setup" (L771), but the pipeline from `problem.md` to a runnable config is not even sketched. A forward reference or pipeline overview would help users understand why they are doing this step. Impact: **medium**. [SKILL.md, L771 "entry point for guided deliberation setup"; L869 "Next step: /conversus interests"].

- **No `--type` override flag**: FR-008 (spec.md L38) requires automatic type classification with ambiguity handling. But expert users who already know their problem type should be able to skip classification by passing `--type selection`. This avoids unnecessary `[CLARIFY:]` tags and speeds up the workflow. Impact: **low**. [spec.md, L38 FR-008; SKILL.md L804-818 type classification].

- **Existing file refine behavior underspecified**: SKILL.md L791 says "incorporate the user's new input while preserving existing structure" but does not define what "preserving existing structure" means operationally. Does it merge constraints? Append open questions? Replace the decision statement? Without this, different agent models will implement "refine" differently, producing inconsistent behavior. Impact: **medium**. [SKILL.md, L788-793 existing file check].

## Off-Base Assumptions

- **The spec assumes `--context` paths are always local files**: spec.md L36 and SKILL.md L778, L797-802 describe context ingestion as reading from local file paths. This is correct for the current implementation. However, the SKILL.md `allowed-tools` line (L14) includes `Bash(ls:*)` and the engine already resolves paths relative to the config file (L280). No off-base assumption here -- the local-file constraint is appropriate and consistent with existing tooling. No correction needed.

The spec makes no incorrect assumptions about the integration architecture. The dispatch mechanism, handler isolation, and content flow are all sound.

## Actionable Recommendations

1. **Add post-write schema validation for problem.md** (Priority: P1)
   - **Current state**: SKILL.md L822 says "Write `problem.md` to the output directory. The file MUST follow this schema:" followed by the template, but no validation step checks the output after writing.
   - **Proposed change**: Add a "### Output Validation" subsection after "### Output" (after L850) that reads the written `problem.md` and verifies all 7 required headings exist (`# Problem Definition`, `## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`). If any heading is missing, warn the user but do not delete the file (matching the engine's Phase 6 output validation pattern at L659).
   - **Rationale**: The engine validates template output at L659-676. The define handler should apply the same discipline. Downstream commands (`interests`, `mode`) will parse `problem.md` by heading -- a missing section will cause silent failures.
   - **Risk if ignored**: Malformed `problem.md` files that crash or confuse subsequent pipeline commands. No automated check means errors surface only when the user manually inspects the file.

2. **Specify refine semantics for existing problem.md** (Priority: P1)
   - **Current state**: SKILL.md L791 says "If refine: incorporate the user's new input while preserving existing structure" with no further detail.
   - **Proposed change**: Add operational rules: (a) The `## Decision` statement is replaced with the new input's distilled decision. (b) `## Constraints` are merged (existing + new, deduplicated). (c) `## Open Questions` are merged, with resolved questions removed if the new input answers them. (d) `## Type` is re-evaluated. (e) `## Source Documents` are unioned. (f) `## Context` is rewritten to incorporate both old and new information.
   - **Rationale**: Without defined merge semantics, each agent invocation may refine differently, making the command non-deterministic in a way that undermines trust. The engine specifies exact overwrite/merge semantics for presets at L180-184 -- the same precision is needed here.
   - **Risk if ignored**: Users who use "refine" will get inconsistent results across invocations, eroding confidence in the define command.

3. **Support multiple --context paths** (Priority: P2)
   - **Current state**: SKILL.md L778 describes `--context path/to/spec.md` as a single path.
   - **Proposed change**: Allow `--context` to be specified multiple times or accept a comma-separated list: `/conversus define --context specs/003/spec.md --context docs/architecture.md`. Resolve each path using the same rules at L797-798 (file or directory).
   - **Rationale**: The engine's `target:` supports lists (SKILL.md L59-68). Real-world problems have multiple relevant documents. Forcing users to put all context documents in one directory is an artificial constraint.
   - **Risk if ignored**: Users will work around this by copying documents into a single directory, creating stale duplicates that drift from their sources.

4. **Add a forward pipeline reference in the report** (Priority: P2)
   - **Current state**: SKILL.md L869 says "Next step: /conversus interests" but there is no explanation of the full pipeline or how `problem.md` is consumed.
   - **Proposed change**: Add a brief pipeline overview after the Report section (before the `---` at L877):
     ```
     ### Pipeline Overview

     `/conversus define` is the first of three guided setup commands:
     1. `/conversus define` -- produce `problem.md` (this command)
     2. `/conversus interests` -- identify stakeholder perspectives from the problem definition
     3. `/conversus mode` -- select a game theory mode and generate `conversus.yml`

     Each command's output feeds the next. The pipeline produces a runnable `conversus.yml` without requiring manual config authoring.
     ```
   - **Rationale**: SKILL.md L771 positions define as "the entry point for guided deliberation setup" but the pipeline is never described. Users need to understand the purpose of the step they are performing. [SKILL.md, L771, L869].
   - **Risk if ignored**: Users complete `define` and do not know what to do next because `/conversus interests` does not exist yet. The "Next step" reference is a dead end.

5. **Add --type override flag** (Priority: P2)
   - **Current state**: SKILL.md L804-818 always performs classification. No way to skip it.
   - **Proposed change**: Add `--type <selection|integration|scoping|stress-test>` flag to the Input section (L775). When provided, skip classification and use the specified type directly. Still run the rest of the define pipeline (constraints, open questions, etc.).
   - **Rationale**: Expert users who know their problem type should not have to accept or reject a classification. This mirrors the engine's `validate_templates: false` escape hatch at L55 -- power users can skip automated checks when they know what they want.
   - **Risk if ignored**: Minor friction for expert users. They will manually edit the `## Type` section after generation.

6. **Verify anchor link rendering for colon-containing headings** (Priority: P2)
   - **Current state**: SKILL.md L25 links to `#define-problem-definition` targeting the heading `## Define: Problem Definition` at L769.
   - **Proposed change**: No text change needed, but add a comment in the spec (spec.md) noting that the colon in the heading is dropped in anchor generation (GitHub/CommonMark slug rules: lowercase, strip special chars, spaces to hyphens). This is currently correct but fragile -- if someone adds parentheses or other punctuation to the heading, the link breaks silently.
   - **Rationale**: The anchor link `#define-problem-definition` resolves correctly under GitHub-Flavored Markdown rules (the colon is stripped). However, SKILL.md is consumed by an agent runtime, not GitHub. The runtime's markdown parser must follow the same slug algorithm. If it does not, dispatch will fail to navigate to the handler.
   - **Risk if ignored**: If the agent runtime's markdown parser handles anchor slugs differently from GFM, the dispatch table's links will not resolve and the agent will not find the define handler section.

7. **Document that define does not use the Agent tool** (Priority: P3)
   - **Current state**: SKILL.md L14 lists `allowed-tools: Agent Read Write Bash(ls:*)`. The define handler uses Read (to read context docs and existing problem.md) and Write (to write problem.md) but never uses Agent. This is implicit from reading the handler but never stated.
   - **Proposed change**: Add a note at the top of the define handler (after L771): "This command runs in the main conversation thread. It does not dispatch sub-agents."
   - **Rationale**: The engine's NON-NEGOTIABLE MULTI-AGENT RULES at L312-324 are prominent and might lead readers to assume all commands use sub-agents. Explicitly stating that define is a single-agent command clarifies the execution model and sets expectations for latency (fast, no parallel agent overhead).
   - **Risk if ignored**: Users or maintainers may incorrectly assume define launches agents, leading to confusion about why it is fast and about its error handling model.

8. **Add error handling for unreadable context documents** (Priority: P3)
   - **Current state**: SKILL.md L797-802 describes context ingestion but does not specify what happens if a `--context` path does not exist or is unreadable.
   - **Proposed change**: Add after L798: "If the path does not exist, fail with: 'Context path does not exist: {path}'. If a file within a context directory is unreadable, warn and skip that file."
   - **Rationale**: The engine validates that all `docs` paths exist (SKILL.md L196) and all `TARGET_FILES` exist (L195). The define handler should apply the same validation. [SKILL.md, L195-196 path validation in Step 1].
   - **Risk if ignored**: Silent failures when a context path is misspelled. The user gets a `problem.md` without the context they intended.

## FR-to-Implementation Mapping

### Subcommand Dispatch (FR-001 through FR-004)

| FR | Requirement | SKILL.md Implementation | Satisfied? |
|----|-------------|------------------------|------------|
| FR-001 | Dispatch based on first argument; known subcommands: `run`, `define` | L18-28: Dispatch table listing `run` and `define` with routing targets. L29: "Future subcommands (not yet implemented): `interests`, `mode`, `converge`, `arbitrate`, `gate`." | Yes |
| FR-002 | `/conversus run` routes to existing Step 1-5 with zero behavioral change | L24: Routes to `[Run: Input](#run-input)`. Git diff confirms body of Run: Input (L36-42) and Run: Execution (L43+) is unchanged -- only headings renamed from `## Input` and `## Execution`. | Yes |
| FR-003 | No arguments defaults to `run` | L26: "`/conversus` (no arguments) \| Defaults to `run` (backward compatible)" | Yes |
| FR-004 | Unknown subcommands produce helpful error | L31-32: "If the first argument does not match a known subcommand, emit: > Unknown subcommand: '{cmd}'. Available commands: run, define. (Future: interests, mode, converge, arbitrate, gate)" | Yes |

### Define Handler (FR-005 through FR-012)

| FR | Requirement | SKILL.md Implementation | Satisfied? |
|----|-------------|------------------------|------------|
| FR-005 | Accept natural-language description inline or interactively | L775-783: Three input forms: inline (quoted text), with context (--context), interactive (questions). | Yes |
| FR-006 | `--context <path>` reads context documents and incorporates constraints | L778 (input form 2), L795-802 (Context Ingestion subsection with 5-step resolution process). | Yes |
| FR-007 | Output is `problem.md` in working directory or `--output <dir>` | L784: "`--output <dir>` overrides the output directory (default: current working directory)." L822: "Write `problem.md` to the output directory." | Yes |
| FR-008 | Problem type classification with ambiguity handling | L804-818: Classification table with 4 types and ambiguity `[CLARIFY:]` tag pattern. | Yes |
| FR-009 | Structured sections in problem.md | L822-850: Full schema with all 7 required sections (Decision, Type, Context, Constraints, Success Criteria, Open Questions, Source Documents). | Yes |
| FR-010 | Ambiguities marked with `[CLARIFY: ...]` tags | L852: "Any field where the agent cannot confidently determine the content MUST include a `[CLARIFY: ...]` tag." L815-818: Type-specific CLARIFY example. | Yes |
| FR-011 | Existing problem.md: present and ask refine/replace, never silently overwrite | L786-793: Existing File Check subsection with 4-step flow and explicit "Never silently overwrite." | Yes |
| FR-012 | No description + no context: ask clarifying questions interactively | L779-782: Interactive form with three specific questions: "What decision are you facing?", "Who or what are the competing perspectives?", "What are the constraints?" | Yes |

### Success Criteria (SC-001 through SC-005)

| SC | Criterion | Achievable? | Evidence |
|----|-----------|-------------|----------|
| SC-001 | Inline description produces `problem.md` with type `selection` | Yes | L777 (inline input), L810 (`selection` type maps to "Choosing between discrete alternatives"), L822-850 (output schema). A Redis-vs-Postgres description maps cleanly to `selection`. |
| SC-002 | `--context specs/003/spec.md` incorporates domain details | Yes | L778, L795-802 (Context Ingestion reads documents, extracts constraints, incorporates into Constraints/Context/Success Criteria sections, lists paths in Source Documents). |
| SC-003 | `/conversus run conversus.yml` works identically | Yes | L24 routes to `[Run: Input](#run-input)`. Git diff confirms zero changes to engine body text. Only heading renames (`## Input` -> `## Run: Input`, `## Execution` -> `## Run: Execution`). |
| SC-004 | No arguments defaults to `run` | Yes | L26: Explicit default-to-run row in dispatch table. |
| SC-005 | Vague description produces `[CLARIFY:]` tags | Yes | L852: "Vague descriptions should produce more `[CLARIFY:]` tags, not hallucinated specifics." Combined with L815-818 type ambiguity CLARIFY pattern and L844-845 Open Questions CLARIFY schema. |

### Additional Verification

**Anchor link resolution**: The dispatch table at L25 links to `#define-problem-definition`. The heading `## Define: Problem Definition` at L769 generates this anchor under GitHub-Flavored Markdown slug rules (lowercase, strip colons, spaces to hyphens). The link resolves correctly. The `#run-input` anchor at L24 targets `## Run: Input` at L36. Also resolves correctly.

**No existing content modified**: The git diff shows exactly three change regions: (1) description field in frontmatter expanded to mention subcommands (L9-10), (2) `## Input` renamed to `## Run: Input` and `## Execution` renamed to `## Run: Execution` with the new Subcommand Dispatch section inserted before them (L18-42), (3) the Define handler section added at L769-877 before `## Important Notes`. No line within the engine body (L43-767) was changed.

**No engine internal references in define handler**: The define handler (L769-877) does not reference: template variables (`{VARIABLE}`), phase numbers, Agent tool dispatch, `conversus.yml`, mode logic, preset resolution, the Dispute-Parsing Subsystem, or any engine step. It is completely self-contained with its own Input, Output, and Report subsections.

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/spec.md` -- sections/lines cited: L13-17 (Feature Summary), L27-31 (FR-001 through FR-004), L34-41 (FR-005 through FR-012), L36 (--context), L38 (FR-008), L45-71 (problem.md schema), L77-81 (SC-001 through SC-005), L87-89 (constraints)
- `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md` -- sections/lines cited: L9-10 (description), L14 (allowed-tools), L18-33 (Subcommand Dispatch), L24-26 (dispatch table entries), L31-32 (unknown subcommand error), L36-42 (Run: Input), L43 (Run: Execution), L55 (validate_templates), L57-68 (multi-target resolution), L102-106 (target resolution), L180-184 (preset inline overrides), L195-196 (path validation), L220 (validation error style), L280 (template path resolution), L286-295 (template validation), L300-598 (engine execution), L312-324 (NON-NEGOTIABLE MULTI-AGENT RULES), L385-429 (Phase 1), L659-676 (Phase 6 output validation), L769-877 (Define handler), L771 (entry point description), L775-784 (input forms), L786-793 (existing file check), L795-802 (context ingestion), L804-818 (type classification), L822-854 (output schema and handling), L856-875 (report), L869 (next step reference)
