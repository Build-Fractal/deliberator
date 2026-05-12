# Functional-Typing Review — 007-subcommand-dispatch-define

**Reviewer**: functional-typing (structural correctness & specification compliance)
**Scope**: Dispatch routing correctness, backward compatibility, define handler completeness, schema correctness

---

### Executive Summary

Spec 007 introduces subcommand dispatch to SKILL.md (routing `/conversus` invocations to `run` or `define` handlers) and implements the first guided workflow command, `/conversus define`, which converts natural-language problem descriptions into structured `problem.md` artifacts. The dispatch mechanism is additive — it prefixes the existing execution flow with a routing table and renames two headings (`Input` to `Run: Input`, `Execution` to `Run: Execution`) to namespace them under the `run` subcommand.

The implementation in SKILL.md is structurally sound. The dispatch table (L22-27) routes all four cases specified by FR-001 through FR-004, the `run` path preserves full behavioral equivalence (the heading renames are purely cosmetic and do not alter any step content), and the `define` handler covers every functional requirement (FR-005 through FR-012) with dedicated subsections. The `problem.md` schema in SKILL.md (L824-850) is character-for-character identical to the spec's schema (spec L45-71). There are no structural omissions, no missing FR coverage, and no schema drift.

My most important recommendation: add explicit dispatch precedence rules (L31-32) to handle edge cases where the first argument could be interpreted as either a subcommand or a config file path (e.g., `/conversus run.yml` or `/conversus define.yml`).

### Alignment

- **Dispatch table completeness** (SKILL.md L22-27, spec FR-001 through FR-004): The dispatch table in SKILL.md covers all four routing cases required by the spec: `run [config]` routes to Run: Input (FR-001/002), `define [description]` routes to Define: Problem Definition (FR-001), no-arguments defaults to `run` (FR-003), and the unknown-subcommand error message (L31-32) matches FR-004. The table format makes routing unambiguous — no implicit dispatch logic.

- **Backward-compatible default** (SKILL.md L26, spec FR-003/SC-004): The no-arguments row explicitly states "Defaults to `run` (backward compatible)" with a direct anchor to `Run: Input`. This matches both FR-003 ("MUST default to `run`") and SC-004 ("/conversus with no arguments defaults to run behavior"). The parenthetical "(backward compatible)" is a useful signal to implementers.

- **Run path heading renames** (SKILL.md L36, L43, spec L17): The spec states "The existing `/conversus run` handler is unchanged" and identifies the heading renames ("Input to Run: Input, Execution to Run: Execution") as the only changes to the run path. SKILL.md confirms this: `## Run: Input` (L36) replaces what was `## Input`, and `## Run: Execution` (L43) replaces what was `## Execution`. All content beneath these headings is untouched — Step 1 through Step 5, template variables, phase execution, arbitration, dispute parsing, and the report format are identical to their pre-dispatch state.

- **Schema fidelity** (SKILL.md L824-850, spec L45-71): The `problem.md` schema in the define handler's Output section reproduces the spec's schema exactly: same heading hierarchy (`# Problem Definition`, `## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`), same placeholder text, same `[CLARIFY: ...]` tag syntax. No fields added, removed, or reworded.

- **FR-to-section mapping** (SKILL.md L769-876): Every functional requirement in the define handler has a corresponding SKILL.md section: FR-005 maps to Input (L774-783), FR-006 maps to Context Ingestion (L797-802) and Input form 2 (L778), FR-007 maps to Output (L822) and Input `--output` (L784), FR-008 maps to Problem Type Classification (L804-818), FR-009 maps to the schema in Output (L824-850), FR-010 maps to Ambiguity handling (L852), FR-011 maps to Existing File Check (L788-793), FR-012 maps to Input form 3 (L779-782).

### Missed Opportunities

- **Dispatch precedence for ambiguous first arguments**: The dispatch table (SKILL.md L22-27) does not specify what happens when the first argument is a string that could be interpreted as either a subcommand or a config path. For example, `/conversus run.yml` — is `run.yml` the config path passed to the `run` subcommand (missing its argument), or is it an unknown subcommand? Similarly, if a future file `define.yml` exists, `/conversus define.yml` is ambiguous. The spec (FR-001) says dispatch is "based on the first argument" but does not define exact-match-only semantics. Adding a rule like "subcommand matching requires an exact string match against the known subcommand list; partial matches or matches with file extensions are treated as config paths passed to the default `run` handler" would eliminate this class of ambiguity. Impact: **high** — without this, implementations may diverge on edge cases.

- **Error message for unknown subcommand lacks actionable guidance**: The unknown-subcommand error (SKILL.md L32) lists available and future commands but does not suggest what the user likely intended. For example, if the user types `/conversus defin` (typo), the error should suggest "Did you mean: define?" since the Levenshtein distance is 1. The current error is correct per FR-004 ("helpful error listing available commands") but "helpful" could be stronger. Impact: **low** — functional correctness is met, this is polish.

- **No validation of `--context` path existence in the define handler**: The Context Ingestion section (SKILL.md L797-802) specifies "Resolve the path. If a directory, read all `.md` files in it (non-recursive)." but does not specify what happens if the path does not exist. The `run` handler has explicit validation for target and doc paths (L195-196: "All resolved `TARGET_FILES` exist", "All agent `docs` paths exist"). The `define` handler should have equivalent validation: "If the `--context` path does not exist, fail with: 'Context path does not exist: {path}'." Impact: **medium** — without this, the handler's behavior on invalid paths is implementation-defined.

- **No validation that `--output` directory exists or is writable**: The Output section (SKILL.md L822) specifies writing to the output directory but does not validate the directory. The `run` handler creates output directories (Step 2, L234-266). The `define` handler should specify: "If the output directory does not exist, create it. If creation fails, fail with: 'Cannot create output directory: {path}'." Impact: **medium** — edge case but should be specified.

- **No explicit statement that `define` does not launch subagents**: The `define` handler describes a single-agent workflow (the main conversation analyzes input and writes `problem.md`), but this is implicit. Given that the `run` handler extensively documents its multi-agent dispatch model (L312-324), the `define` handler should explicitly state: "The define command executes in the main conversation. No subagents are launched." This prevents implementers from over-engineering the define path. Impact: **low** — inferable but worth stating.

- **Define handler Report section missing `--output` awareness**: The Report template (SKILL.md L860-870) shows `Output: {path to problem.md}` but does not specify how the path is constructed when `--output <dir>` is used. It should clarify: "The path shown is the absolute path to the written file, incorporating `--output` if specified." Impact: **low** — the intent is clear but the spec should be precise.

### Off-Base Assumptions

- **Assumption that heading renames are the "only changes" to the run path** (spec L17): The spec states "The existing `/conversus run` handler is unchanged" and implies that heading renames are cosmetic. This is correct for the content beneath the headings, but the dispatch table itself (SKILL.md L22-27) introduces a new structural dependency: the `run` handler is now reachable via an anchor link (`#run-input`) that did not exist before. If any external document or template references the old anchors (`#input`, `#execution`), those links break. The spec does not acknowledge this as a breaking change because the SKILL.md is self-contained — but the frontmatter `description` field (L3-10) was also updated to mention "Supports subcommands: run (deliberation engine), define (problem definition)." This frontmatter change is not listed in the spec's "what changes" section (spec L17). The assumption is not wrong per se, but it is incomplete — the frontmatter change should be acknowledged.

- **Assumption that `problem.md` schema sections are always populated**: The schema (spec L45-71 and SKILL.md L824-850) shows Constraints as a bulleted list and Success Criteria as prose. The Empty sections rule (SKILL.md L854) only covers Source Documents and Open Questions. If the user provides a vague one-word description ("architecture"), the Constraints section may have nothing to populate. The spec assumes the agent will always find constraints to list, but FR-010 only requires `[CLARIFY:]` tags for "ambiguities," not for empty sections. A rule like "If the agent cannot determine any constraints, use `- [CLARIFY: No constraints identified. What limits apply?]`" would close this gap.

### Actionable Recommendations

1. **Add dispatch precedence rule** (Priority: P1)
   - **Current state**: SKILL.md L22-27 lists subcommands in a table but does not specify matching semantics (exact match vs. prefix match vs. contains).
   - **Proposed change**: Add after L27: "Subcommand matching is exact and case-sensitive. The first argument is compared against the known subcommand list (`run`, `define`). If it does not exactly match any known subcommand, it is treated as a config file path and routed to `run` (e.g., `/conversus my-config.yml` is equivalent to `/conversus run my-config.yml`)."
   - **Rationale**: The current `run` handler (SKILL.md L38-41) already accepts an optional path argument. Without precedence rules, `/conversus my-config.yml` could either route to `run` with `my-config.yml` as the config path, or trigger the unknown-subcommand error. The former is more useful and backward-compatible.
   - **Risk if ignored**: Implementations will handle ambiguous first arguments inconsistently. Some will emit errors for valid config paths; others will silently route to `run`. Neither matches user intent predictably.

2. **Add `--context` path validation to define handler** (Priority: P1)
   - **Current state**: Context Ingestion (SKILL.md L797-802) says "Resolve the path" but does not specify failure behavior for nonexistent paths.
   - **Proposed change**: Add to Context Ingestion after L797: "If the `--context` path does not exist, fail with: 'Context path does not exist: {path}'. If the path is a directory containing no `.md` files, warn: 'No .md files found in context directory: {path}' and proceed without context."
   - **Rationale**: The `run` handler validates all input paths (SKILL.md L195-196). The `define` handler should maintain the same validation discipline. Silent failure on missing context paths would produce a `problem.md` that appears complete but lacks the context the user intended.
   - **Risk if ignored**: Users who mistype a `--context` path get a `problem.md` with no context incorporation and no error, making the mistake invisible.

3. **Acknowledge frontmatter change in spec** (Priority: P2)
   - **Current state**: Spec L17 says "SKILL.md gains a 'Subcommand Dispatch' section before Step 1. A new `/conversus define` command handler is added. The existing `/conversus run` handler is unchanged." The frontmatter `description` field change (SKILL.md L3-10 now includes "Supports subcommands: run (deliberation engine), define (problem definition)") is not mentioned.
   - **Proposed change**: Amend spec L17 to: "SKILL.md gains a 'Subcommand Dispatch' section before Step 1, the frontmatter description is updated to list supported subcommands, and a new `/conversus define` command handler is added. The existing `/conversus run` handler is renamed (Input to Run: Input, Execution to Run: Execution) but behaviorally unchanged."
   - **Rationale**: The frontmatter is the skill's external interface — agent runtimes use it for discovery and matching. Changing it without documenting the change creates a discrepancy between the spec and the implementation.
   - **Risk if ignored**: Spec reviewers checking "what changed" against the diff will find an undocumented frontmatter modification. Minor but erodes spec trustworthiness.

4. **Add `--output` directory creation semantics** (Priority: P2)
   - **Current state**: SKILL.md L784 and L822 reference `--output <dir>` but do not specify behavior when the directory does not exist.
   - **Proposed change**: Add to the Output section (after L822): "If the output directory does not exist, create it (including intermediate directories). If creation fails, fail with: 'Cannot create output directory: {path}'."
   - **Rationale**: The `run` handler specifies directory creation in Step 2 (L234-266). The `define` handler should be equivalently explicit.
   - **Risk if ignored**: Implementations may silently fail, create the directory, or error — inconsistent behavior across runtimes.

5. **Specify empty-section handling for Constraints and Success Criteria** (Priority: P2)
   - **Current state**: Empty section handling (SKILL.md L854) covers Source Documents ("(none -- no context documents provided)") and Open Questions ("(none)") but not Constraints or Success Criteria.
   - **Proposed change**: Add: "If no constraints can be determined, use: `- [CLARIFY: No constraints identified. What requirements or limitations apply?]`. If no success criteria can be determined, use: `[CLARIFY: What does a successful outcome look like?]`."
   - **Rationale**: FR-010 requires ambiguities to be marked with `[CLARIFY:]` tags. An empty Constraints or Success Criteria section is an ambiguity that should be surfaced, not left blank.
   - **Risk if ignored**: Vague input produces a `problem.md` with empty sections that appear complete, misleading downstream commands (`/conversus interests`, `/conversus mode`) that consume this artifact.

6. **Explicitly state that `define` is a single-agent command** (Priority: P2)
   - **Current state**: The define handler (SKILL.md L769-876) does not mention agent dispatch at all — it describes what to do but not the execution model.
   - **Proposed change**: Add to the `## Define: Problem Definition` section (after L771): "This command executes entirely in the main conversation. No subagents are launched. The orchestrator reads input, classifies the problem, and writes `problem.md` directly."
   - **Rationale**: SKILL.md's `run` handler extensively documents its multi-agent execution model (L312-324). The absence of equivalent documentation in `define` could lead implementers to assume subagent dispatch is needed. Explicit negation prevents over-engineering.
   - **Risk if ignored**: An implementer might launch a subagent for classification or context analysis, adding unnecessary complexity and latency to a simple single-agent operation.

7. **Add dispatch rule to Baseline Features inventory** (Priority: P3)
   - **Current state**: The Baseline Features section (SKILL.md L901-913) inventories pre-spec features. The dispatch mechanism introduced by spec 007 is not listed.
   - **Proposed change**: After spec 007 is implemented, add to Important Notes or a new "Spec-Backed Features" section: "**Subcommand dispatch**: `/conversus` routes to handlers based on the first argument (spec 007). Known subcommands: `run`, `define`."
   - **Rationale**: The Baseline Features section distinguishes organic features from spec-backed ones. Dispatch is foundational infrastructure that future specs (`interests`, `mode`, etc.) depend on. It should be catalogued.
   - **Risk if ignored**: Future spec authors may not know dispatch exists and may attempt to reinvent routing in their own specs.

8. **Clarify `--context` multiple-path semantics** (Priority: P3)
   - **Current state**: FR-006 (spec L36) says `--context <path>` (singular). SKILL.md L778 says `--context path/to/spec.md` (singular). But the Context Ingestion section (L797) handles both files and directories, implying a single path that may resolve to multiple files.
   - **Proposed change**: Clarify whether `--context` accepts multiple paths (e.g., `--context path1 --context path2` or `--context path1,path2`) or only a single path. If single-path-only, state: "`--context` accepts exactly one path. To include multiple context sources, point to a directory containing them."
   - **Rationale**: Without this, implementations may accept multiple `--context` flags or comma-separated lists, creating behavioral divergence.
   - **Risk if ignored**: Minor — most users will pass a single path or directory. But the spec should be unambiguous.

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/spec.md` — sections/lines cited: L3-6 (feature ID/metadata), L11-13 (feature summary), L17-19 (what changes/doesn't), L25-30 (FR-001 through FR-004), L34-41 (FR-005 through FR-012), L45-71 (problem.md schema), L77-81 (SC-001 through SC-005), L85-89 (constraints)
- `<HOME>/code/payer-index-mono/conversus/SKILL.md` — sections/lines cited: L1-16 (frontmatter), L18-33 (Subcommand Dispatch), L36-42 (Run: Input), L43-99 (Run: Execution / Step 1), L192-222 (validation rules), L234-266 (Step 2: Output Directories), L312-324 (multi-agent rules), L769-771 (Define: Problem Definition heading), L774-784 (Input subsection), L788-793 (Existing File Check), L797-802 (Context Ingestion), L804-818 (Problem Type Classification), L822-850 (Output / schema), L852-854 (Ambiguity/empty handling), L858-876 (Report), L879-899 (Important Notes), L901-913 (Baseline Features)
