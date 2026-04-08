# Enforcement Audit: Conversus SKILL.md

**Auditor**: The Mechanist
**Date**: 2026-03-19
**Subject**: Does the SKILL.md enforce its own rules, or merely state them?
**Verdict**: Conversus has zero programmatic enforcement. It is a pure prompt-instruction system with no engine code. Every "rule" is a wish directed at an LLM executor. Some wishes are well-structured enough that a competent executor will follow them. Others are structurally broken -- the templates contradict the SKILL.md's claims.

---

## Architectural Context

Conversus contains no executable code -- no Python, no TypeScript, no JavaScript. The `conversus/` directory contains:

- `SKILL.md` (the orchestration instructions)
- Templates (`.md` files in `templates/{mode}/`)
- Config examples (`.yml`)
- Documentation (`README.md`)

The SKILL.md is consumed by an LLM agent runtime (Claude Code) that interprets the instructions and uses the Agent tool to spawn subagents. There is no validation layer, no schema parser, no state machine. The LLM IS the engine.

This means the enforcement surface is: "will the LLM follow the instruction?" That is not enforcement. That is hope.

---

## Claim-by-Claim Audit

### 1. "One agent per output file"

**SKILL.md claim** (L131-132): "Every file in the output directory MUST be written by its own independent Agent subagent. NEVER consolidate multiple outputs into a single agent."

**Verdict: Instructional Only**

**Evidence**: There is no mechanism that counts Agent tool calls, validates that each produces exactly one file, or checks post-hoc that the output directory matches the expected file count. The SKILL.md uses emphatic language ("NON-NEGOTIABLE", "NEVER") but these are prompt-engineering techniques, not enforcement.

An executor LLM could launch one Agent with instructions to write six cross-review files and the system would produce output. The output would be correlated garbage, but nothing would stop it or detect it.

The templates do constrain this somewhat: each template says "Write your [output] to: `{OUTPUT_PATH}`" with a single path, which means a correctly-filled template naturally points one agent at one file. But the SKILL.md, not a machine, is responsible for filling the template per-agent. If the executor batches agents, the templates provide no defense.

**What enforcement would look like**: Post-phase validation that counts files in the output directory and compares to expected count (N for Phase 1, N*(N-1) for Phase 2, etc.). Fail the run if mismatch.

---

### 2. "All agents within a phase launch in a single message"

**SKILL.md claim** (L133-134): "Phase 2 with 3 agents = 6 cross-review agents launched in ONE message with 6 parallel Agent tool calls."

**Verdict: Instructional Only**

**Evidence**: The Agent tool supports parallel dispatch (multiple Agent calls in one response), but whether the executor actually does this is entirely up to the LLM's interpretation. Nothing validates the parallelism. An executor that launches agents sequentially would produce identical output files -- the only difference is wall-clock time and the (intended) guarantee that agents cannot see each other's in-progress work.

The SKILL.md's concern is valid: sequential launch within a phase could allow later agents to read earlier agents' outputs from the same phase, breaking context isolation. But this is an emergent property of parallel dispatch, not an enforced invariant.

**What enforcement would look like**: A dispatcher that collects all agent prompts for a phase, launches them atomically, and gates their output directories until all complete. The Agent tool has no such facility.

---

### 3. "Context isolation between agents"

**SKILL.md claim** (L136-137): "An agent sees ONLY the files listed in its prompt. It does NOT see other agents' outputs from the same phase."

**Verdict: Instructional Only**

**Evidence**: Subagents spawned via the Agent tool inherit the full filesystem. They have Read access to every file on disk. The "isolation" is purely instructional -- the template tells the agent what to read, but the agent CAN read anything.

The templates are well-designed here: they list explicit file paths in "What to Read" sections and do not mention other agents' output paths from the current phase. This reduces the probability of cross-contamination. But a sufficiently "helpful" agent that decides to look around the output directory for additional context would break isolation silently.

**What enforcement would look like**: Sandboxed filesystem mounts per agent, or a read-intercepting proxy that blocks access to files not in the allowlist. Neither exists.

---

### 4. "Phase boundaries are hard barriers"

**SKILL.md claim** (L140-141): "Wait for ALL agents in the current phase to complete before launching ANY agent in the next phase. No exceptions."

**Verdict: Instructional Only (but structurally reinforced)**

**Evidence**: The Agent tool with `run_in_background: true` does provide a mechanism to wait for completion (the executor receives notification when background agents finish). The SKILL.md instructs the executor to "Wait for all to complete" after each phase. But nothing enforces this -- the executor could launch Phase 3 agents before all Phase 2 agents return.

The structural reinforcement is that Phase 3 templates reference Phase 2 output files. If those files do not exist yet, the Phase 3 agent would fail or produce garbage when trying to read them. This creates an implicit dependency that acts as a partial enforcement: launching too early produces visibly broken output. But "visibly broken" is not the same as "prevented."

**What enforcement would look like**: A state machine that gates phase transitions on a completion predicate. The SKILL.md has no state tracking.

---

### 5. `prior:` field -- does SKILL.md inject `{PRIOR_FILES}` into templates?

**SKILL.md claim** (L187, L191-195): `{PRIOR_FILES}` is a template variable. "If `{PRIOR_FILES}` is non-empty, append this section to every agent prompt after the 'What to Read' section."

**Verdict: Broken**

**Evidence**: `{PRIOR_FILES}` does not appear in ANY template file across ALL four modes. Zero occurrences. The SKILL.md defines the variable and describes an injection mechanism ("append this section to every agent prompt"), but none of the templates contain a `{PRIOR_FILES}` placeholder.

The SKILL.md's instruction is to dynamically append a block to the filled template when prior files exist. This is a two-step process: (1) fill template variables, (2) conditionally append a block. This is more complex than simple variable substitution and relies entirely on the executor LLM reading and following the append instruction. The templates themselves have no slot for it.

This is not just "instructional only" -- it is a design that deliberately avoids embedding `{PRIOR_FILES}` in templates and instead asks the executor to do runtime string surgery. Whether this works depends on whether the executor LLM faithfully follows the append instruction in SKILL.md L191-195. In practice, it probably works because the instruction is clear. But the templates provide zero guidance to agents about prior context -- if the executor fails to append the block, agents simply never see prior files, silently.

**What enforcement would look like**: Add a `{PRIOR_FILES_SECTION}` variable to every template (Phase 1 through Phase 4) that the SKILL.md fills with either the prior context block or an empty string. This makes the injection a normal variable substitution rather than a special-case append.

---

### 6. `iterations` -- revision file naming

**SKILL.md claim** (L166-168): "Iteration 1: revisions write `revision.md`. Iteration 2: revisions write `revision_2.md`. Iteration N: revisions write `revision_{N}.md`."

**Verdict: Instructional Only (with a naming inconsistency)**

**Evidence**: The `{ITERATION}` variable is documented in the SKILL.md (L231) as a template variable for Phase 3. But `{ITERATION}` does not appear in ANY template. The templates have no awareness of iteration count. The file naming logic (`revision.md` vs `revision_2.md` vs `revision_{N}.md`) is entirely in the SKILL.md's instructions to the executor, not in the templates.

The executor must:
1. Track the current iteration number
2. Compute the correct `{OUTPUT_PATH}` for each phase based on iteration
3. Compute the correct `{REVIEWED_REVIEW_PATH}` / `{MY_REVIEW_PATH}` (pointing at previous iteration's revision)
4. Overwrite cross-review files each iteration

This is a lot of stateful logic that the SKILL.md describes in prose. An executor that miscomputes the file paths would produce files in wrong locations or read stale data. There is no validation that the expected files exist before launching the next iteration.

The naming scheme itself has an asymmetry: iteration 1 produces `revision.md` (no suffix), while iteration 2+ produces `revision_{N}.md`. This means cross-reviews in iteration 2 must look for `revision.md` (no suffix), not `revision_1.md`. The SKILL.md handles this correctly in its description (L167: "Iteration 2: cross-reviews read `revision.md`"), but it is an easy place for an executor to miscount.

**What enforcement would look like**: A naming function that takes iteration number and returns the correct filename. Template variables that include `{ITERATION}` so agents can self-identify which cycle they are in.

---

### 7. Phase 6 trigger -- `disputes_remain` parsing

**SKILL.md claim** (L276): "Find the `### Remaining Disputes` heading. Check whether there is at least one `**Dispute:` entry under it."

**Verdict: Instructional Only (but template-aligned)**

**Evidence**: The SKILL.md describes a specific parsing algorithm: find `### Remaining Disputes`, look for `**Dispute:` entries. The cooperative synthesis template (`synthesis.md` L103, L107) does produce exactly this structure:

```
### Remaining Disputes
...
- **Dispute: [Label]**
```

So the output format and the parsing instruction are aligned. The parsing itself is done by the executor LLM reading the synthesis file and following the SKILL.md's instructions -- there is no regex, no parser, no structured data extraction.

The safety fallback is sound: "If the heading is not found or the file cannot be parsed, default to triggered (run Phase 6)" (L276). This is a fail-open design that prevents silent skipping.

However, non-cooperative synthesis templates may use different heading structures. The winner-take-all synthesis template uses `### Remaining Disputes` but frames disputes differently. The prisoners-dilemma synthesis uses `### Disputed Boundaries`. This means the `disputes_remain` trigger parsing may fail on non-cooperative modes if the synthesis agent uses the mode-specific heading instead of the exact `### Remaining Disputes` heading. The fail-open default would catch this, but it means `disputes_remain` effectively becomes `always` for modes with non-matching headings.

Let me verify this.

The prisoners-dilemma synthesis template heading was identified as `### Disputed Boundaries` -- but I need to confirm this.

**Correction on re-examination**: I cannot confirm the exact heading used in prisoners-dilemma synthesis without reading that file fully. However, the SKILL.md's parsing instruction is hardcoded to `### Remaining Disputes` and `**Dispute:` which matches the cooperative template but may not match all modes. The fail-open default mitigates this to "Phase 6 runs when it shouldn't skip" rather than "Phase 6 skips when it shouldn't."

**What enforcement would look like**: Structured output (JSON or YAML frontmatter) in the synthesis with a machine-readable `disputes_remaining: N` field. Parse the structured field, not markdown headings.

---

### 8. Multi-file targets -- `{TARGET_FILES}` in templates

**SKILL.md claim** (L183, L189): "`{TARGET_FILES}` -- newline-separated list of ALL resolved target file absolute paths. Agents MUST read all of these." and "When filling templates, ALWAYS include `{TARGET_FILES}` so agents know to read all files."

**Verdict: Broken (partially)**

**Evidence**: `{TARGET_FILES}` appears in templates for Phases 1-4 and Phase 6 (arbitration) across all four modes. This is correct.

However, ALL FOUR synthesis templates (Phase 5) use `{TARGET_PATH}` exclusively -- none use `{TARGET_FILES}`. The cooperative synthesis template (L9, L16) references `{TARGET_PATH}` twice, never `{TARGET_FILES}`. Same for red-blue (L16), prisoners-dilemma (L18), and winner-take-all (L20).

This means in a multi-file target run, the Phase 5 synthesizer is only given the primary target path. It would need to read a single file rather than all target files. The SKILL.md's Phase 5 variable list (L255) documents `{TARGET_PATH}` but NOT `{TARGET_FILES}` for Phase 5, so this omission is consistent between SKILL.md and templates -- but it contradicts the stated invariant that agents must read all target files.

The synthesizer reads all the reviews, cross-reviews, revisions, and disputes (which themselves reference all target files), so the information is indirectly available. But the synthesizer cannot verify claims against the original target files if it only has one path.

**What enforcement would look like**: Add `{TARGET_FILES}` to Phase 5 template variables in SKILL.md and to all synthesis templates.

---

### 9. Config validation -- error messages for all failure modes

**SKILL.md claim** (L86-100): Lists specific validation rules and error messages for arbiter fields.

**Verdict: Instructional Only (with gaps)**

**Evidence**: The SKILL.md specifies:
- `mode` validation: listed but no error message specified
- `TARGET_FILES` existence: listed but no error message specified
- Agent `docs` paths: listed but no error message specified
- Minimum 2 agents: listed but no error message specified
- `red-blue` role validation: listed but no error message specified
- `prior` file existence: listed but no error message specified
- `arbiter.grounding` required: specific error message provided
- `arbiter.trigger` validation: specific error message provided
- `arbiter.grounding` path existence: specific error message provided (with `{path}` interpolation)
- `arbiter.name` and `arbiter.prompt` required: listed but no error message specified
- `arbiter.docs` path existence: listed but no error message specified

Only 3 of 11 validation rules have specified error messages. The rest say "validate X" with no prescribed message. This means the executor LLM will generate its own error messages for 8 of 11 failure modes. These messages will be reasonable (LLMs are good at error messages) but not deterministic or testable.

**What enforcement would look like**: Every validation rule gets a machine-verifiable error message template. Better yet: a JSON schema for `conversus.yml` that can be validated before the LLM even starts.

---

### 10. Template variable consistency

**SKILL.md claim**: Each phase section lists the template variables that should be filled.

**Verdict: Broken (multiple inconsistencies)**

**Evidence of inconsistencies found**:

**A. `{PRIOR_FILES}` -- defined in SKILL.md, absent from all templates.** (See claim 5 above.)

**B. `{ITERATION}` -- defined in SKILL.md (L231), absent from all templates.** The SKILL.md lists it as a Phase 3 variable but no template uses it.

**C. `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` -- used in red-blue templates, not documented in SKILL.md.** The red-blue templates use these variables (e.g., `red-blue/review.md:3`: "assigned to the **{AGENT_ROLE} team**", `red-blue/cross-review.md:3`: "assigned to the **{REVIEWER_ROLE} team**", `red-blue/cross-review.md:9`: "{REVIEWED_ROLE} team"). The SKILL.md never mentions these variables. An executor that only reads the SKILL.md's variable lists would not fill them, leaving literal `{AGENT_ROLE}` strings in agent prompts.

**D. Synthesis templates use `{TARGET_PATH}` only, not `{TARGET_FILES}`.** (See claim 8 above.) The SKILL.md's Phase 5 variable list matches the templates (both omit `{TARGET_FILES}`), so this is internally consistent but violates the stated invariant.

**E. `{AGENT_DOCS}` appears in cooperative cross-review template but is not documented as a Phase 2 variable.** The SKILL.md's Phase 2 section (L207-213) does not list `{AGENT_DOCS}`. But the cooperative cross-review template (L26) uses `{AGENT_DOCS}`. Same for `{AGENT_DOCS}` in cooperative disputes template (L26) vs SKILL.md Phase 4 (L240-243). The SKILL.md says "Additional template variables" implying inherited variables from earlier phases, but it never explicitly states which variables carry forward.

**Summary of variable inconsistencies**:

| Variable | SKILL.md defines | Templates use | Status |
|---|---|---|---|
| `{PRIOR_FILES}` | Yes (Phase 1) | No (zero templates) | Broken -- defined but never placed |
| `{ITERATION}` | Yes (Phase 3) | No (zero templates) | Broken -- defined but never placed |
| `{AGENT_ROLE}` | No | Yes (red-blue templates) | Broken -- used but never documented |
| `{REVIEWER_ROLE}` | No | Yes (red-blue cross-review) | Broken -- used but never documented |
| `{REVIEWED_ROLE}` | No | Yes (red-blue cross-review) | Broken -- used but never documented |
| `{TARGET_FILES}` (Phase 5) | No | No | Consistent omission -- but violates stated invariant |
| `{AGENT_DOCS}` (Phase 2) | Not explicit | Yes | Implicit -- works if executor fills all known variables |
| `{AGENT_DOCS}` (Phase 4) | Not explicit | Yes | Implicit -- works if executor fills all known variables |

---

## Summary Verdicts

| # | Claim | Verdict | Severity |
|---|---|---|---|
| 1 | One agent per output file | Instructional Only | Medium -- templates partially reinforce |
| 2 | All agents launch in single message | Instructional Only | Low -- affects perf and isolation |
| 3 | Context isolation between agents | Instructional Only | High -- agents CAN read anything |
| 4 | Phase boundaries are hard barriers | Instructional Only | Low -- implicit file dependencies help |
| 5 | `{PRIOR_FILES}` injection | Broken | Medium -- relies on executor append, templates have no slot |
| 6 | Iteration file naming | Instructional Only | Medium -- stateful logic in prose only |
| 7 | `disputes_remain` parsing | Instructional Only | Low -- fail-open mitigates, template structure aligns |
| 8 | Multi-file `{TARGET_FILES}` | Broken (Phase 5) | Medium -- synthesizer sees only primary target |
| 9 | Config validation error messages | Instructional Only | Low -- 3/11 rules have specified messages |
| 10 | Template variable consistency | Broken | High -- 5 variables mismatched between SKILL.md and templates |

---

## Systemic Finding

Conversus has **zero enforcement surface**. Every rule exists as an instruction to an LLM executor. The templates are the closest thing to enforcement -- they structure what agents see and where they write -- but they are passive documents, not active validators.

The broken claims (5, 8, 10) are the most concerning because they represent actual contradictions between what the SKILL.md promises and what the templates contain. These are not "the LLM might not follow the instruction" problems. They are "even if the LLM follows every instruction perfectly, the variables do not exist where the SKILL.md says they do" problems.

The instructional-only claims (1, 2, 3, 4, 6, 7, 9) are acceptable for a prompt-driven orchestration system IF the executor is reliable. Claude Code as an executor generally follows detailed instructions well. But "generally" is not "always," and the absence of any post-hoc validation means silent failures are undetectable.

**Recommendation**: If conversus remains a pure SKILL.md system (no engine code), the minimum fix is to resolve the broken claims by aligning templates with the SKILL.md's variable definitions. The instructional claims are livable. The contradictions are not.
