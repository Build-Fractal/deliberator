# Purist Enforcement Audit: SKILL.md Specification Completeness

**Auditor**: The Purist
**Date**: 2026-03-19
**Subject**: `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md`
**Scope**: 10 specification gap categories, all 24 templates across 4 modes

---

## Methodology

Every behavior the tool exhibits must be traceable to an explicit instruction in SKILL.md. Every template variable must be defined exactly once. Every error path must have a specified message. Ambiguity in a spec is a bug.

For each item: **Specified** (explicitly addressed in SKILL.md text), **Implied** (inferable but not stated), or **Missing** (not addressed, ambiguity exists).

---

## 1. Variable Audit: SKILL.md Definitions vs. Template Usage

### Variables Defined in SKILL.md

| Variable | Defined in SKILL.md Section | Phase(s) |
|---|---|---|
| `{AGENT_NAME}` | Phase 1 (L179) | 1, 3, 4 |
| `{AGENT_PROMPT}` | Phase 1 (L180) | 1, 3, 4 |
| `{AGENT_DOCS}` | Phase 1 (L181) | 1, 2, 3, 4 |
| `{TARGET_PATH}` | Phase 1 (L182-183) | 1, 5 |
| `{TARGET_FILES}` | Phase 1 (L183) | 1, 2, 3, 4, 6 |
| `{OUTPUT_PATH}` | Phase 1 (L184) | All |
| `{MODE}` | Phase 1 (L185) | 1, 5, 6 |
| `{PRIOR_FILES}` | Phase 1 (L187) | 1 |
| `{REVIEWER_NAME}` | Phase 2 (L208) | 2 |
| `{REVIEWER_PROMPT}` | Phase 2 (L209) | 2 |
| `{REVIEWED_NAME}` | Phase 2 (L210) | 2 |
| `{REVIEWED_REVIEW_PATH}` | Phase 2 (L211) | 2 |
| `{REVIEWER_REVIEW_PATH}` | Phase 2 (L212) | 2 |
| `{CROSS_REVIEWS_OF_ME}` | Phase 3 (L226) | 3 |
| `{MY_CROSS_REVIEWS}` | Phase 3 (L227) | 3 |
| `{MY_REVIEW_PATH}` | Phase 3 (L228) | 3 |
| `{ITERATION}` | Phase 3 (L230) | 3 |
| `{ALL_REVISION_PATHS}` | Phase 4 (L241) | 4 |
| `{MY_REVISION_PATH}` | Phase 4 (L242) | 4 |
| `{ALL_REVIEWS}` | Phase 5 (L256) | 5 |
| `{ALL_CROSS_REVIEWS}` | Phase 5 (L257) | 5 |
| `{ALL_REVISIONS}` | Phase 5 (L258) | 5 |
| `{ALL_DISPUTES}` | Phase 5 (L259) | 5, 6 |
| `{AGENT_NAMES}` | Phase 5 (L261) | 5, 6 |
| `{ARBITER_NAME}` | Phase 6 (L291) | 6 |
| `{ARBITER_PROMPT}` | Phase 6 (L292) | 6 |
| `{ARBITER_DOCS}` | Phase 6 (L293) | 6 |
| `{GROUNDING_PATH}` | Phase 6 (L294) | 6 |
| `{SYNTHESIS_PATH}` | Phase 6 (L295) | 6 |
| `{TRIGGER}` | Phase 6 (L302) | 6 |

### Variables Used in Templates but NOT Defined in SKILL.md

| Variable | Template(s) | Status |
|---|---|---|
| `{AGENT_ROLE}` | `red-blue/review.md` (L3), `red-blue/revision.md` (L3), `red-blue/disputes.md` (L3) | **Missing** |
| `{REVIEWER_ROLE}` | `red-blue/cross-review.md` (L7) | **Missing** |
| `{REVIEWED_ROLE}` | `red-blue/cross-review.md` (L9) | **Missing** |

**Gap 1.1** -- **Missing**: `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` are used in 4 red-blue templates but never defined in SKILL.md. The `role` field exists in the config schema (agents may have `role: red | blue`), but no template variable definition maps this field to `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, or `{REVIEWED_ROLE}`. An implementer would have to guess the mapping.

**Required addition to SKILL.md, Phase 1 template variables section:**

```
- `{AGENT_ROLE}` — agent's `role` from config (only for `red-blue` mode: `red` or `blue`)
```

**Required addition to SKILL.md, Phase 2 template variables section:**

```
- `{REVIEWER_ROLE}` — the reviewing agent's `role` from config (`red` or `blue`)
- `{REVIEWED_ROLE}` — the reviewed agent's `role` from config (`red` or `blue`)
```

**Required addition to SKILL.md, Phase 3 and Phase 4 template variables sections:**

```
- `{AGENT_ROLE}` — agent's `role` from config (`red` or `blue`, only for `red-blue` mode)
```

### Variables Defined in SKILL.md but Unused in Some Expected Templates

| Variable | Defined For | Not Used In |
|---|---|---|
| `{PRIOR_FILES}` | Phase 1 | Only cooperative `review.md` could use it; none of the other 3 mode review templates reference it |
| `{TARGET_PATH}` | Phases 1, 5 | Used in synthesis templates inconsistently -- cooperative and winner-take-all synthesis use `{TARGET_PATH}`, but prisoners-dilemma synthesis also uses `{TARGET_PATH}`, and red-blue synthesis uses `{TARGET_PATH}` |
| `{ITERATION}` | Phase 3 | None of the 4 revision templates reference `{ITERATION}` |

**Gap 1.2** -- **Missing**: `{ITERATION}` is defined as a Phase 3 variable in SKILL.md (L230) but is not referenced in any of the 4 revision templates. It is defined but has no consumer. Either the templates should use it, or the variable definition should be removed from SKILL.md. This is a dead variable.

**Gap 1.3** -- **Missing**: `{PRIOR_FILES}` injection is specified only for Phase 1 (SKILL.md L191-195), and the injection instruction says to append the section "after the 'What to Read' section." However, only the cooperative review template has a section labeled "What to Read." The winner-take-all review template labels it "Files to Read." The prisoners-dilemma review template labels it "Files to Read." The red-blue review template labels it "What to Read." The injection point name is inconsistent with template headings across modes. Furthermore, no template for any mode contains the `{PRIOR_FILES}` variable as a placeholder -- the spec says to "append this section" dynamically, which is a second injection mechanism not present in any other variable. This dual mechanism (placeholder substitution vs. section appending) is underspecified.

**Required addition**: Either standardize all review templates to have the same "What to Read" section heading, or specify the injection target heading per mode.

---

## 2. Error Messages: Validation Rules vs. Specified Messages

### Rules with Explicit Error Messages

| Validation Rule | Error Message | Status |
|---|---|---|
| `arbiter.grounding` required | "arbiter.grounding is required -- the arbiter must declare its decision framework." | **Specified** (L94) |
| `arbiter.trigger` invalid | "arbiter.trigger must be 'disputes_remain' or 'always'." | **Specified** (L95) |
| `arbiter.grounding` path missing | "arbiter.grounding path does not exist: {path}" | **Specified** (L96) |

### Rules WITHOUT Explicit Error Messages

| Validation Rule | SKILL.md Reference | Status |
|---|---|---|
| `mode` is not one of the valid values | L87 | **Missing** |
| Resolved `TARGET_FILES` file does not exist | L88 | **Missing** |
| Agent `docs` path does not exist | L89 | **Missing** |
| Fewer than 2 agents defined | L90 | **Missing** |
| `red-blue` mode missing red or blue role | L91 | **Missing** |
| `prior` file does not exist | L92 | **Missing** |
| `arbiter.name` missing | L97 | **Missing** |
| `arbiter.prompt` missing | L97 | **Missing** |
| `arbiter.docs` path does not exist | L98 | **Missing** |
| Config file not found (no path given, no `conversus.yml`) | L21 | **Missing** |
| Config file at given path not found | L22 | **Missing** |
| Config YAML parse error | Implied | **Missing** |

**Gap 2.1** -- **Missing**: 11 out of 14 validation rules lack specified error messages. SKILL.md L100 says only "If validation fails, report the error and stop," which is a generic catch-all without message templates. The 3 arbiter-specific rules have explicit messages, creating an inconsistency where arbiter validation is formally specified but all other validation is informal.

**Required addition**: Each validation rule should have a specified error message format. Example:

```
- `mode` invalid: "Invalid mode '{value}'. Must be one of: cooperative, winner-take-all, prisoners-dilemma, red-blue."
- Target file missing: "Target file does not exist: {path}"
- Agent docs missing: "Agent '{name}' docs path does not exist: {path}"
- Too few agents: "At least 2 agents are required. Found: {count}."
- Red-blue role missing: "red-blue mode requires at least one agent with role: red and one with role: blue."
- Prior file missing: "Prior context file does not exist: {path}"
- Arbiter name missing: "arbiter.name is required."
- Arbiter prompt missing: "arbiter.prompt is required."
- Arbiter docs missing: "arbiter.docs path does not exist: {path}"
- Config not found: "No conversus config found. Looked for: {path}"
- YAML parse error: "Failed to parse config: {error}"
```

---

## 3. Phase Sequencing: Order of Operations

**Status: Specified** (with one gap)

The iteration loop diagram at SKILL.md L154-163 is unambiguous:

```
Phase 1 -> [Phase 2 -> Phase 3] x iterations -> Phase 4 -> Phase 5 -> Phase 6 (conditional)
```

The spec explicitly states:
- "Run phases sequentially" (L128)
- "Within each phase, launch all agents in parallel" (L128)
- "Phase boundaries are hard barriers" (L141)
- "Wait for ALL agents in the current phase to complete before launching ANY agent in the next phase" (L141)

**Gap 3.1** -- **Implied**: The spec says Phase 5 runs as foreground ("not in background -- wait for result", L251) and Phase 6 also runs foreground (L288). However, for Phases 1-4, the spec says "use `run_in_background: true`" (L340). The distinction between foreground and background execution is stated in the "Important Notes" section at the bottom (L340) but is NOT stated in each phase section. The Phase 1 section says "launch ALL Phase 1 agents in a single message (parallel)" (L199) but does not explicitly say `run_in_background: true`. An implementer reading only the phase section would miss this.

**Required addition**: Each phase section should explicitly state the execution mode, or the "Important Notes" directive should be elevated to the Phase 4 execution header.

---

## 4. `prior:` Field Injection Point

**Status: Missing** (partial specification)

SKILL.md L191-195 states:

> If `{PRIOR_FILES}` is non-empty, append this section to every agent prompt after the "What to Read" section

**Gap 4.1** -- **Missing**: The injection point "after the 'What to Read' section" is ambiguous across modes:

| Mode | Review Template Section Heading | Match? |
|---|---|---|
| cooperative | "What to Read" | Yes |
| winner-take-all | "Files to Read" | No |
| prisoners-dilemma | "Files to Read" | No |
| red-blue | "What to Read" | Yes |

The spec names a specific section heading that 2 of 4 modes do not use. An implementer must decide whether "What to Read" is a literal heading match or a semantic instruction.

**Gap 4.2** -- **Missing**: The spec says to inject prior context into "every agent prompt." Does "every" mean every phase, or only Phase 1? The surrounding context is the Phase 1 section, but the text says "every agent prompt" without qualification. If prior context should be injected into Phase 2, 3, 4, 5, and 6 prompts as well, the injection point for those phases is unspecified (they have different section structures).

**Required addition**:

```
Prior context injection applies ONLY to Phase 1 review prompts. For templates
using "Files to Read" as their heading (winner-take-all, prisoners-dilemma),
append the prior context block after the "Files to Read" section.
```

Or, alternatively, add `{PRIOR_FILES}` as an explicit placeholder in all Phase 1 templates with a defined position.

---

## 5. Revision File Naming Convention for `iterations > 1`

**Status: Specified** (for Phase 3, partially for Phase 4 and Phase 5)

SKILL.md L166-170 specifies:

```
- Iteration 1: revisions write `revision.md`
- Iteration 2: revisions write `revision_2.md`
- Iteration N: revisions write `revision_{N}.md`
- Phase 4 disputes read the final revision file from the last iteration
- Each iteration's cross-reviews overwrite the previous cross-review files
```

**Gap 5.1** -- **Implied**: Phase 3 (L229) specifies the output path pattern. Phase 4 (L241-242) says `{ALL_REVISION_PATHS}` and `{MY_REVISION_PATH}` reference the "final revision from the last iteration." But the spec does not explicitly state the formula for computing "final revision path":

- If iterations=1: `{output}/{agent}/revision.md`
- If iterations=2: `{output}/{agent}/revision_2.md`
- If iterations=N: `{output}/{agent}/revision_{N}.md`

This is inferable from L166-168 but never stated as a single formula.

**Gap 5.2** -- **Missing**: Phase 5 synthesis variable `{ALL_REVISIONS}` (L258) is described as "newline-separated list of all revision.md paths." The ".md" in the description implies the base name `revision.md`, but for iterations > 1, the final revision is `revision_{N}.md`. Does `{ALL_REVISIONS}` include ALL revisions from ALL iterations (revision.md, revision_2.md, ... revision_N.md), or only the final revision from the last iteration?

SKILL.md says: "All Phase 3 revisions (revised positions after cross-review)" in the cooperative synthesis template, which is ambiguous. The Phase 4 text says disputes "read the final revision file" (L169), suggesting only the final matters. But Phase 5 might want the full history for traceability.

**Required addition**:

```
For iterations > 1:
- `{ALL_REVISIONS}` in Phase 5 contains ONLY the final revision paths (revision_{N}.md),
  not intermediate revisions. The synthesis reads the final converged positions.
- The formula for the final revision path is:
  - iterations=1: `{output}/{agent}/revision.md`
  - iterations>1: `{output}/{agent}/revision_{iterations}.md`
```

**Gap 5.3** -- **Missing**: Phase 2 cross-review output files are stated to "overwrite the previous cross-review files" (L170). The output path is `{output}/{A}/cross-reviews/{B}.md`. For iteration 2+, the cross-reviews are overwritten in place. But the spec does not state whether a consumer of Phase 5 synthesis should be told that cross-reviews represent only the latest iteration's exchange, or the full history. Since they are overwritten, only the latest exists, but this side effect is never flagged to the Phase 5 synthesis agent.

---

## 6. Template Loading: Missing Template File

**Status: Missing**

SKILL.md L116-124 describes template loading:

> Read the prompt template for each phase from `conversus/templates/{mode}/`

And L124:

> Find the monorepo root by looking for the `conversus/templates/` directory starting from the current working directory and walking up.

There is no specification of what happens if:

1. The `conversus/templates/` directory cannot be found (no monorepo root found).
2. A specific template file is missing (e.g., `cooperative/arbitration.md` does not exist).
3. The mode directory does not exist (e.g., `templates/prisoners-dilemma/` is absent).

**Gap 6.1** -- **Missing**: No error message or behavior is specified for template loading failures.

**Required addition**:

```
If the `conversus/templates/` directory cannot be found by walking up from the
current directory, fail with: "Cannot find conversus templates directory.
Searched from {cwd} to filesystem root."

If a required template file is missing, fail with:
"Template not found: conversus/templates/{mode}/{phase}.md"

If the arbiter is not configured, the arbitration.md template is not required.
Only load it when Phase 6 will execute.
```

---

## 7. Agent Model Selection

**Status: Missing**

SKILL.md does not address whether different agents can use different LLM models. The `agents:` config schema (L55-61) defines `name`, `prompt`, `docs`, and `role`, but no `model` field.

**Gap 7.1** -- **Missing**: The spec does not state:
- Whether all agents use the same model as the orchestrating conversation.
- Whether a `model` field is supported per agent.
- Whether the arbiter can use a different model.

This is a design decision, not an oversight -- but a complete spec must state it explicitly, even if the answer is "all agents use the orchestrator's model."

**Required addition**:

```
All subagents (deliberation agents, synthesis agent, arbitration agent) use the same
model as the orchestrating conversation. Per-agent model selection is not supported.
```

Or, if model selection is desired:

```yaml
agents:
  - name: agent-name
    model: claude-opus-4-6  # optional, defaults to orchestrator's model
    prompt: |
      ...
```

---

## 8. Output Overwrite Behavior

**Status: Missing**

SKILL.md does not specify what happens if the output directory already contains files from a previous run.

**Gap 8.1** -- **Missing**: Consider the scenario:
1. User runs conversus, producing `output/apm/review.md`, `output/summary/final.md`, etc.
2. User modifies the config (adds an agent, changes a prompt).
3. User runs conversus again with the same `output:` path.

Does the skill:
- Silently overwrite all existing files?
- Warn before overwriting?
- Fail if output directory exists?
- Clear the output directory first?
- Skip phases whose outputs already exist?

For iterations > 1, the spec says cross-reviews "overwrite the previous cross-review files" (L170), which implies overwrite-is-default. But this is only stated for the intra-run iteration case, not for re-runs.

**Gap 8.2** -- **Missing**: If an agent is removed between runs, stale files from the removed agent persist in the output directory. For example, if the first run had agents [apm, spec-kit, gh-aw] and the second run has only [apm, spec-kit], the `output/gh-aw/` directory still exists with outdated artifacts. The spec does not address stale file cleanup.

**Required addition**:

```
Output overwrite behavior: If the output directory already exists, the skill
overwrites files produced by the current run without warning. Files from previous
runs that are not produced by the current run (e.g., directories for removed agents)
are NOT deleted. The skill does not perform cleanup of stale artifacts.

To ensure a clean run, the user should delete the output directory before re-running.
```

---

## 9. `{TARGET_FILES}` Formatting

**Status: Partially Specified**

SKILL.md L183 states:

> `{TARGET_FILES}` -- newline-separated list of ALL resolved target file absolute paths.

**Gap 9.1** -- **Specified** (paths are absolute): L183 explicitly says "absolute paths."

**Gap 9.2** -- **Specified** (format is one per line): L183 says "newline-separated."

**Gap 9.3** -- **Missing**: Are paths bare (one path per line) or formatted as markdown list items (`- path/to/file.md`)? The templates use `{TARGET_FILES}` in different contexts:

- Cooperative review.md (L14): Placed after a numbered list item, where bare paths would break markdown formatting.
- Winner-take-all review.md (L18-19): Placed after a bold heading, implying bare paths on their own lines.
- Prisoners-dilemma review.md (L25): After "the following target files:" followed by `{TARGET_FILES}` on the next line.

Looking at the cooperative review template lines 13-14:
```
1. **Target files** (the documents under review -- read ALL of these):
{TARGET_FILES}
```

If `{TARGET_FILES}` expands to bare paths, the markdown is:
```
1. **Target files** (the documents under review):
/abs/path/spec.md
/abs/path/plan.md
```

This is valid but not a nested list. If it expands to `- /abs/path/spec.md`, it becomes a nested list under item 1. The cooperative cross-review template (L23) places it differently:
```
3. **Target specification** (the original document under review):
   the target files:
{TARGET_FILES}
```

The indentation/formatting semantics differ between templates. The spec should state the exact format.

**Required addition**:

```
`{TARGET_FILES}` expands to one absolute path per line, no prefix characters. Example:
  /abs/path/to/spec.md
  /abs/path/to/plan.md

If a single target file exists, `{TARGET_FILES}` is a single line with that path.
```

Similarly, `{AGENT_DOCS}`, `{ALL_REVIEWS}`, `{ALL_CROSS_REVIEWS}`, `{ALL_REVISIONS}`, `{ALL_DISPUTES}`, `{CROSS_REVIEWS_OF_ME}`, `{MY_CROSS_REVIEWS}`, `{ALL_REVISION_PATHS}`, `{ARBITER_DOCS}`, and `{PRIOR_FILES}` are all described as "newline-separated list" but the exact formatting (bare vs. prefixed) is not stated.

---

## 10. Cross-Review Ordering

**Status: Specified**

SKILL.md L205-213 defines the cross-review pair relationship:

> For each pair (agent-A, agent-B) where A != B, launch a background Agent.

And:

> `{REVIEWER_NAME}` -- the agent doing the reviewing (A)
> `{REVIEWED_NAME}` -- the agent being reviewed (B)
> `{OUTPUT_PATH}` -- absolute path to `{output}/{A}/cross-reviews/{B}.md`

This means:
- A reviews B -> written to `{output}/A/cross-reviews/B.md`
- B reviews A -> written to `{output}/B/cross-reviews/A.md`

These are two distinct files in two distinct directories. **(A reviews B) is NOT the same file as (B reviews A).** The output path pattern `{output}/{REVIEWER}/cross-reviews/{REVIEWED}.md` makes the directionality unambiguous.

**Status: Specified.** The file naming convention encodes directionality. No ambiguity.

---

## Summary of Gaps

| # | Gap | Severity | Status |
|---|---|---|---|
| 1.1 | `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` undefined in SKILL.md | High -- red-blue mode is broken without these | **Missing** |
| 1.2 | `{ITERATION}` defined but unused by any template | Low -- dead variable, no functional impact | **Missing** |
| 1.3 | `{PRIOR_FILES}` injection point inconsistent with template headings; dual injection mechanism | Medium -- implementer must guess for 2 of 4 modes | **Missing** |
| 2.1 | 11 of 14 validation rules lack specified error messages | Medium -- inconsistent rigor, arbiter rules have messages but nothing else does | **Missing** |
| 3.1 | `run_in_background` not stated per-phase, only in bottom notes | Low -- present but in wrong location | **Implied** |
| 4.1 | Prior injection section heading mismatch across modes | Medium -- "What to Read" vs "Files to Read" | **Missing** |
| 4.2 | Prior injection scope (Phase 1 only? all phases?) ambiguous | Medium -- "every agent prompt" is overbroad | **Missing** |
| 5.1 | Final revision path formula not stated as single rule | Low -- inferable from examples | **Implied** |
| 5.2 | `{ALL_REVISIONS}` scope for iterations > 1 (all revisions or only final?) | Medium -- affects synthesis completeness | **Missing** |
| 5.3 | Cross-review overwrite side effect not communicated to Phase 5 agent | Low -- latent traceability issue | **Missing** |
| 6.1 | No error behavior for missing templates | Medium -- silent failure possible | **Missing** |
| 7.1 | Agent model selection not addressed | Low -- design decision, but spec must be explicit | **Missing** |
| 8.1 | Output overwrite behavior on re-run not specified | Medium -- data loss risk | **Missing** |
| 8.2 | Stale artifact cleanup not addressed | Low -- cosmetic but confusing | **Missing** |
| 9.3 | List variable formatting (bare paths vs. markdown prefixed) not specified | Low -- affects markdown rendering in templates | **Missing** |

### Counts

- **Specified**: 3 items (arbiter error messages, cross-review ordering, target paths are absolute/newline-separated)
- **Implied**: 3 items (phase sequencing background mode, final revision path formula, cross-review overwrite scope)
- **Missing**: 13 items

### Critical Path

**Gap 1.1 is a blocking defect.** The `red-blue` mode cannot be correctly implemented from SKILL.md alone because 3 template variables (`{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}`) are used in templates but never defined in the spec. An implementer has no formal instruction to populate these variables. The mapping from `config.agents[].role` to template variables must be stated explicitly.

---

## Appendix: Full Template Variable Cross-Reference

### Cooperative Mode

| Template | Variables Used |
|---|---|
| `review.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{MODE}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `cross-review.md` | `{REVIEWER_NAME}`, `{REVIEWER_PROMPT}`, `{MODE}`, `{REVIEWED_NAME}`, `{REVIEWED_REVIEW_PATH}`, `{REVIEWER_REVIEW_PATH}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `revision.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{MODE}`, `{MY_REVIEW_PATH}`, `{CROSS_REVIEWS_OF_ME}`, `{MY_CROSS_REVIEWS}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `disputes.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{MODE}`, `{ALL_REVISION_PATHS}`, `{MY_REVISION_PATH}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `synthesis.md` | `{MODE}`, `{AGENT_NAMES}`, `{TARGET_PATH}`, `{ALL_REVIEWS}`, `{ALL_CROSS_REVIEWS}`, `{ALL_REVISIONS}`, `{ALL_DISPUTES}`, `{OUTPUT_PATH}` |
| `arbitration.md` | `{ARBITER_NAME}`, `{ARBITER_PROMPT}`, `{TRIGGER}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`, `{ALL_DISPUTES}`, `{TARGET_FILES}`, `{ARBITER_DOCS}`, `{AGENT_NAMES}`, `{MODE}`, `{OUTPUT_PATH}` |

### Winner-Take-All Mode

| Template | Variables Used |
|---|---|
| `review.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `cross-review.md` | `{REVIEWER_NAME}`, `{REVIEWER_PROMPT}`, `{REVIEWED_NAME}`, `{TARGET_FILES}`, `{REVIEWED_REVIEW_PATH}`, `{REVIEWER_REVIEW_PATH}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `revision.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{TARGET_FILES}`, `{MY_REVIEW_PATH}`, `{CROSS_REVIEWS_OF_ME}`, `{MY_CROSS_REVIEWS}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `disputes.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{TARGET_FILES}`, `{MY_REVISION_PATH}`, `{ALL_REVISION_PATHS}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `synthesis.md` | `{MODE}`, `{AGENT_NAMES}`, `{TARGET_PATH}`, `{ALL_REVIEWS}`, `{ALL_CROSS_REVIEWS}`, `{ALL_REVISIONS}`, `{ALL_DISPUTES}`, `{OUTPUT_PATH}` |
| `arbitration.md` | `{ARBITER_NAME}`, `{ARBITER_PROMPT}`, `{TRIGGER}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`, `{ALL_DISPUTES}`, `{TARGET_FILES}`, `{ARBITER_DOCS}`, `{AGENT_NAMES}`, `{MODE}`, `{OUTPUT_PATH}` |

### Prisoners-Dilemma Mode

| Template | Variables Used |
|---|---|
| `review.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `cross-review.md` | `{REVIEWER_NAME}`, `{REVIEWER_PROMPT}`, `{REVIEWED_NAME}`, `{REVIEWED_REVIEW_PATH}`, `{REVIEWER_REVIEW_PATH}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `revision.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{MY_REVIEW_PATH}`, `{CROSS_REVIEWS_OF_ME}`, `{MY_CROSS_REVIEWS}`, `{TARGET_FILES}`, `{OUTPUT_PATH}` |
| `disputes.md` | `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{MY_REVISION_PATH}`, `{ALL_REVISION_PATHS}`, `{TARGET_FILES}`, `{OUTPUT_PATH}` |
| `synthesis.md` | `{AGENT_NAMES}`, `{TARGET_PATH}`, `{ALL_REVIEWS}`, `{ALL_CROSS_REVIEWS}`, `{ALL_REVISIONS}`, `{ALL_DISPUTES}`, `{OUTPUT_PATH}` |
| `arbitration.md` | `{ARBITER_NAME}`, `{ARBITER_PROMPT}`, `{TRIGGER}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`, `{ALL_DISPUTES}`, `{TARGET_FILES}`, `{ARBITER_DOCS}`, `{AGENT_NAMES}`, `{MODE}`, `{OUTPUT_PATH}` |

### Red-Blue Mode

| Template | Variables Used |
|---|---|
| `review.md` | `{AGENT_NAME}`, **`{AGENT_ROLE}`**, `{AGENT_PROMPT}`, `{MODE}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `cross-review.md` | `{REVIEWER_NAME}`, **`{REVIEWER_ROLE}`**, `{REVIEWER_PROMPT}`, `{REVIEWED_NAME}`, **`{REVIEWED_ROLE}`**, `{MODE}`, `{REVIEWED_REVIEW_PATH}`, `{REVIEWER_REVIEW_PATH}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `revision.md` | `{AGENT_NAME}`, **`{AGENT_ROLE}`**, `{AGENT_PROMPT}`, `{MY_REVIEW_PATH}`, `{CROSS_REVIEWS_OF_ME}`, `{MY_CROSS_REVIEWS}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `disputes.md` | `{AGENT_NAME}`, **`{AGENT_ROLE}`**, `{AGENT_PROMPT}`, `{MY_REVISION_PATH}`, `{ALL_REVISION_PATHS}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}` |
| `synthesis.md` | `{MODE}`, `{AGENT_NAMES}`, `{TARGET_PATH}`, `{ALL_REVIEWS}`, `{ALL_CROSS_REVIEWS}`, `{ALL_REVISIONS}`, `{ALL_DISPUTES}`, `{OUTPUT_PATH}` |
| `arbitration.md` | `{ARBITER_NAME}`, `{ARBITER_PROMPT}`, `{TRIGGER}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`, `{ALL_DISPUTES}`, `{TARGET_FILES}`, `{ARBITER_DOCS}`, `{AGENT_NAMES}`, `{MODE}`, `{OUTPUT_PATH}` |

**Bold** entries are variables used in templates but not defined in SKILL.md.

### Variables Missing `{AGENT_DOCS}` in Specific Templates

The prisoners-dilemma `revision.md` and `disputes.md` templates do NOT include `{AGENT_DOCS}` in their "Files to Read" section, while all other modes' revision and disputes templates do include agent documentation. This means prisoners-dilemma agents lose access to their grounding documentation in Phases 3 and 4. This is either intentional (the recalibration is based solely on cross-reviews and prior declarations) or an omission. SKILL.md does not clarify this distinction.

**Gap (additional)**: Prisoners-dilemma Phase 3 and Phase 4 templates omit `{AGENT_DOCS}`. If intentional, SKILL.md should state this exception. If unintentional, the templates have a bug.

---

## Appendix: Inconsistencies Between SKILL.md and Templates

### `{MODE}` Usage Inconsistency

SKILL.md defines `{MODE}` as a Phase 1 and Phase 5 variable. However:
- Cooperative templates use `{MODE}` in Phases 1, 2, 3, 4, 5, and 6.
- Winner-take-all templates do NOT use `{MODE}` in Phases 1-4 (the mode is hardcoded in template text as "winner-take-all").
- Prisoners-dilemma templates do NOT use `{MODE}` in Phases 1-4 (hardcoded as "Prisoner's Dilemma").
- Red-blue templates use `{MODE}` in Phases 1, 2, 5, and 6.

The SKILL.md variable definition says `{MODE}` is for "Phase 1" and "Phase 5" but cooperative templates use it in every phase. This is not a functional bug (the variable is populated for all phases) but it is a spec-template contract inconsistency.

### `{TARGET_PATH}` vs `{TARGET_FILES}` in Phase 5

The cooperative synthesis template uses both `{TARGET_PATH}` (L9: "The target specification under review: `{TARGET_PATH}`") and lists files under separate numbered items. The winner-take-all synthesis uses only `{TARGET_PATH}` (L20). But SKILL.md Phase 5 defines both `{TARGET_PATH}` (L255) and implies `{TARGET_FILES}` should be available. The Phase 5 synthesis templates only use `{TARGET_PATH}`, never `{TARGET_FILES}`. This is consistent within templates but the SKILL.md Phase 5 variable list does not include `{TARGET_FILES}` -- confirming that Phase 5 intentionally uses only `{TARGET_PATH}`. This is fine, but creates a question: when the target is multiple files, does the synthesis agent only see the "primary" target path (first file)? SKILL.md Phase 1 L182 says `{TARGET_PATH}` is "if single target file, its absolute path. If multiple, the first file's path (primary)." This means the Phase 5 synthesis agent may not have the full list of target files. This could be intentional (the synthesis reads all artifacts which already incorporate all target files) or a gap.
