# Enforcement Audit: SKILL.md Pragmatist Review

**Reviewer**: The Pragmatist
**Date**: 2026-03-19
**Scope**: Will an LLM following SKILL.md produce correct behavior end-to-end?
**Method**: Read every template variable reference in SKILL.md, cross-reference against every `{VARIABLE}` in every cooperative template, trace the iteration loop, and identify where execution will break.

---

## 1. Agent Counts Per Phase

**Verdict: Works**

The SKILL.md is unambiguous:

- Phase 1: N agents
- Phase 2: N*(N-1) agents
- Phase 3: N agents
- Phase 4: N agents
- Phase 5: 1 agent
- Phase 6: 1 agent (conditional)

The formula is stated, the math is worked out for N=3 (13 without arbiter, 14 with), and rule #1 ("One agent per output file") reinforces it. An LLM will get this right.

One minor note: the SKILL.md says "For 3 agents without arbiter: 13 total agent launches" and "N^2 + N + 1" which checks out (9 + 3 + 1 = 13). The math is consistent. No issue.

---

## 2. Iteration Loop Clarity

**Verdict: Fragile**

The iteration loop diagram is correct and the file-naming convention is specified:

```
Iteration 1: cross-reviews read review.md, revisions write revision.md
Iteration 2: cross-reviews read revision.md, revisions write revision_2.md
Iteration N: cross-reviews read revision_{N-1}.md, revisions write revision_{N}.md
```

**Problem 1: Naming inconsistency at iteration 1.** The output for iteration 1 is `revision.md` (no suffix), but iteration 2 produces `revision_2.md`. This means the naming convention has a special case: iteration 1 = `revision.md`, iteration N>1 = `revision_{N}.md`. This is stated clearly in the SKILL.md. But when iteration 2's cross-reviews need to read the previous revision, they should read `revision.md` (from iteration 1) -- and the SKILL.md says "Iteration 2: cross-reviews read `revision.md` (not `review.md`)". This is correct but relies on the LLM tracking that `revision_{N-1}.md` when N=2 means `revision_1.md` which is actually `revision.md` (no suffix). The SKILL.md handles this by saying "iteration 1: `review.md`, iteration N>1: `revision_{N-1}.md`" for the cross-review read path -- but that only covers what cross-reviews read in iteration 1 vs N>1, not what `revision_{N-1}` resolves to when N=2.

**Fix**: Add an explicit note: "When computing `revision_{N-1}.md`: if N-1 equals 1, the path is `revision.md` (not `revision_1.md`). The unsuffixed `revision.md` is always the iteration-1 output."

**Problem 2: `{ITERATION}` variable defined but never used in templates.** The SKILL.md defines `{ITERATION}` as a template variable for Phase 3 (revision), but the cooperative `revision.md` template does not contain `{ITERATION}` anywhere. This is harmless -- the variable will be replaced with nothing or the orchestrator will just set it and the template won't use it. But it signals a disconnect: the SKILL.md author intended the template to use it, the template author didn't. If a future template does use it, it'll work. As-is, it's dead weight.

**Fix**: Either add `{ITERATION}` to the revision template (e.g., in a header: "Iteration {ITERATION}") or remove it from the SKILL.md variable list. Prefer adding it to the template -- it's useful metadata.

---

## 3. Template Variables: SKILL.md Definitions vs. Template Usage

**Verdict: Fragile (two mismatches)**

### Complete variable audit:

#### Phase 1 (review.md template uses):
| Variable | In Template | Defined in SKILL.md Phase 1 | Match |
|---|---|---|---|
| `{AGENT_NAME}` | Yes | Yes | OK |
| `{AGENT_PROMPT}` | Yes | Yes | OK |
| `{MODE}` | Yes | Yes | OK |
| `{TARGET_FILES}` | Yes | Yes | OK |
| `{AGENT_DOCS}` | Yes | Yes | OK |
| `{OUTPUT_PATH}` | Yes | Yes | OK |

`{TARGET_PATH}` is defined in SKILL.md Phase 1 but not used in the template. Harmless (unused variable).
`{PRIOR_FILES}` is injected conditionally per SKILL.md instructions. Not in the template -- correct, it's appended dynamically.

**Phase 1: Works.**

#### Phase 2 (cross-review.md template uses):
| Variable | In Template | Defined in SKILL.md Phase 2 | Match |
|---|---|---|---|
| `{REVIEWER_NAME}` | Yes | Yes | OK |
| `{REVIEWER_PROMPT}` | Yes | Yes | OK |
| `{REVIEWED_NAME}` | Yes | Yes | OK |
| `{REVIEWED_REVIEW_PATH}` | Yes | Yes | OK |
| `{REVIEWER_REVIEW_PATH}` | Yes | Yes | OK |
| `{OUTPUT_PATH}` | Yes | Yes | OK |
| `{MODE}` | Yes | Yes (inherited) | OK |
| `{TARGET_FILES}` | Yes | Yes (inherited) | OK |
| `{AGENT_DOCS}` | Yes | **Not listed** | **MISMATCH** |

**Mismatch 1: `{AGENT_DOCS}` used in cross-review template but not defined in Phase 2 variable list.** The cross-review template at line 26 includes `{AGENT_DOCS}`. The SKILL.md Phase 2 section lists "Additional template variables" beyond Phase 1, but `{AGENT_DOCS}` is not in either the Phase 2 additional list or explicitly carried forward. A careful LLM will realize this should be the reviewer's docs and fill it from the agent config. A less careful LLM might leave it as a literal `{AGENT_DOCS}` string or skip it.

**Fix**: Add to Phase 2's variable list: "`{AGENT_DOCS}` -- newline-separated list of the reviewing agent's doc paths (same as Phase 1)." Or add a general statement that Phase 1 variables are inherited by all subsequent phases unless overridden.

#### Phase 3 (revision.md template uses):
| Variable | In Template | Defined in SKILL.md Phase 3 | Match |
|---|---|---|---|
| `{AGENT_NAME}` | Yes | Yes (inherited) | OK |
| `{AGENT_PROMPT}` | Yes | Yes (inherited) | OK |
| `{MODE}` | Yes | Yes (inherited) | OK |
| `{TARGET_FILES}` | Yes | Yes (inherited) | OK |
| `{AGENT_DOCS}` | Yes | Yes (inherited) | OK |
| `{MY_REVIEW_PATH}` | Yes | Yes | OK |
| `{CROSS_REVIEWS_OF_ME}` | Yes | Yes | OK |
| `{MY_CROSS_REVIEWS}` | Yes | Yes | OK |
| `{OUTPUT_PATH}` | Yes | Yes | OK |

`{ITERATION}` is defined in SKILL.md but not used in template. See finding #2 above.

**Phase 3: Works** (with the `{ITERATION}` dead-variable caveat).

#### Phase 4 (disputes.md template uses):
| Variable | In Template | Defined in SKILL.md Phase 4 | Match |
|---|---|---|---|
| `{AGENT_NAME}` | Yes | Yes (inherited) | OK |
| `{AGENT_PROMPT}` | Yes | Yes (inherited) | OK |
| `{MODE}` | Yes | Yes (inherited) | OK |
| `{TARGET_FILES}` | Yes | Yes (inherited) | OK |
| `{AGENT_DOCS}` | Yes | Yes (inherited) | OK |
| `{ALL_REVISION_PATHS}` | Yes | Yes | OK |
| `{MY_REVISION_PATH}` | Yes | Yes | OK |
| `{OUTPUT_PATH}` | Yes | Yes | OK |

**Phase 4: Works.**

#### Phase 5 (synthesis.md template uses):
| Variable | In Template | Defined in SKILL.md Phase 5 | Match |
|---|---|---|---|
| `{MODE}` | Yes | Yes | OK |
| `{AGENT_NAMES}` | Yes | Yes | OK |
| `{TARGET_PATH}` | Yes | Yes | OK |
| `{ALL_REVIEWS}` | Yes | Yes | OK |
| `{ALL_CROSS_REVIEWS}` | Yes | Yes | OK |
| `{ALL_REVISIONS}` | Yes | Yes | OK |
| `{ALL_DISPUTES}` | Yes | Yes | OK |
| `{OUTPUT_PATH}` | Yes | Yes | OK |

**Problem**: The synthesis template uses `{TARGET_PATH}` in two places (line 9 and line 16) but the spec has multi-target support where `{TARGET_PATH}` is defined as "the first file's path (primary)." For a multi-file target, the synthesis agent would only see the primary file path in the "What to Read" section at line 16, missing the other target files entirely. The synthesis template does NOT use `{TARGET_FILES}`.

**Mismatch 2: Synthesis template lacks `{TARGET_FILES}`.** When multiple target files are configured, the Phase 5 synthesis agent is told to read `{TARGET_PATH}` (one file) while the original spec may span multiple files. The synthesizer needs all targets to produce accurate spec change recommendations.

**Fix**: In synthesis.md, replace the single `{TARGET_PATH}` reference under "What to Read" with `{TARGET_FILES}` (same pattern as all other phases). Keep `{TARGET_PATH}` in the context header as the "primary" spec. Add `{TARGET_FILES}` to the Phase 5 variable list in SKILL.md.

#### Phase 6 (arbitration.md template uses):
All variables match SKILL.md definitions. **Phase 6: Works.**

---

## 4. `{PRIOR_FILES}` Injection

**Verdict: Fragile**

The SKILL.md says:

> If `{PRIOR_FILES}` is non-empty, append this section to every agent prompt after the "What to Read" section

This is a runtime instruction to the orchestrating LLM: after filling the template, conditionally append a block. The instruction is clear in Phase 1 but only stated once. The question: does this apply to ALL phases, or just Phase 1?

**Problem**: The instruction says "every agent prompt" but is written inside the Phase 1 section (lines 191-195 in SKILL.md). An LLM reading linearly will see this as a Phase 1 instruction. The intent is clearly "all phases" (the word "every" is explicit), but the placement creates ambiguity. A careful LLM will follow "every agent prompt." A fast-reading LLM might only inject it in Phase 1.

Practically, prior files matter most for Phase 1 (initial reviews set the foundation). For Phases 2-4, agents are reading each other's outputs from the current run, so prior context is less critical. For Phase 5 synthesis and Phase 6 arbitration, the entire deliberation record is available. So even if an LLM only injects it in Phase 1, the output will likely be acceptable -- the Phase 1 agents carry the prior context into their reviews, which then propagates through cross-review and revision.

**Fix**: Move the `{PRIOR_FILES}` injection instruction to a general section before Phase 1 (e.g., as part of "Step 4: Execute Phases") and state explicitly: "For all phases, if `{PRIOR_FILES}` is non-empty, append the prior context block after the 'What to Read' section in the filled template." Alternatively, accept that Phase 1-only injection is sufficient and document that choice.

---

## 5. Phase 6 Trigger Evaluation

**Verdict: Fragile**

The trigger logic for `disputes_remain` is:

> Read the Phase 5 synthesis output file. Find the `### Remaining Disputes` heading. Check whether there is at least one `**Dispute:` entry under it. If yes, trigger is met.

**This works IF the synthesis template is followed exactly.** The synthesis template defines a `### Remaining Disputes` section with `**Dispute: [Label]**` entries. So there's an implicit contract between the synthesis template output format and the trigger parser.

**Problem 1: The synthesizer is an LLM, and LLMs paraphrase.** If the synthesis agent writes "**Dispute - [Label]**" or "#### Dispute: [Label]" or "**Remaining dispute: [Label]**", the trigger check will miss it. The SKILL.md says to look for `**Dispute:` which is a prefix match on bold text. This is fragile but defensible -- the synthesis template is explicit about the format, and LLMs generally follow structured templates well.

**Problem 2: The fallback is good.** "If the heading is not found or the file cannot be parsed, default to triggered (run Phase 6) as a safety measure." This is the right call -- it means the failure mode is "run arbitration when you didn't need to" rather than "skip arbitration when you did need it." Correct engineering.

**Fix**: No critical fix needed. The design is fragile but the fallback makes it fail-safe rather than fail-silent. If you want to harden it: instruct the synthesis template to end the Remaining Disputes section with a machine-readable line like `<!-- disputes_count: N -->` that the trigger can parse deterministically. But this is over-engineering for a system where the orchestrator is an LLM parsing LLM output.

---

## 6. Edge Cases That Silently Produce Wrong Output

**Verdict: Two identified**

### Edge Case 1: Two-agent deliberation cross-review asymmetry

With N=2 agents (A, B), Phase 2 produces 2 cross-reviews: A reviews B and B reviews A. This is correct. But in Phase 3, agent A reads "cross-reviews written about me" (just B's review of A) and "cross-reviews I wrote" (just A's review of B). With only 2 agents, each agent sees the complete cross-review record. This means the revision phase has NO information asymmetry -- both agents see everything. The adversarial isolation claim is weakened. This isn't "wrong output" but it's a degenerate case where the system adds ceremony without the information-theoretic benefit of larger agent pools. **Not a bug, but worth documenting as a known limitation.**

### Edge Case 2: Agent name with special characters breaks file paths

If an agent is named `my-agent/v2` or `agent name` (with spaces or slashes), the output path `{output}/{agent-name}/review.md` produces invalid or unexpected paths. The SKILL.md does not validate agent names against filesystem-safe characters.

**Fix**: Add validation: "Agent names must be filesystem-safe: lowercase alphanumeric, hyphens, and underscores only. No spaces, slashes, or special characters."

### Edge Case 3: Cross-review file paths with problematic agent names

Phase 2 output path is `{output}/{A}/cross-reviews/{B}.md`. If agent names collide after filesystem normalization (e.g., "Agent_A" and "agent-a" on a case-insensitive filesystem), cross-reviews silently overwrite each other. Same fix as above.

### Edge Case 4: Empty docs list

If an agent has `docs: []` or no `docs` field, `{AGENT_DOCS}` resolves to an empty string. The templates say "read all of these thoroughly" followed by nothing. An LLM will handle this gracefully (nothing to read), but the template renders awkwardly. **Cosmetic, not functional.**

---

## 7. Where It Fails First With a Real `conversus.yml`

**Verdict: Template path resolution**

The SKILL.md says:

> Templates are in the `conversus/` directory relative to the monorepo root. Find the monorepo root by looking for the `conversus/templates/` directory starting from the current working directory and walking up.

**This is the first point of failure.** The orchestrating LLM is told to "walk up" from the current directory looking for `conversus/templates/`. This is a filesystem traversal instruction to an LLM that has `Read` and `Bash(ls:*)` available. Will the LLM:

1. Use `ls` to check directories? (Allowed by `Bash(ls:*)`)
2. Try to `Read` the template path directly? (Will work if it guesses right)
3. Get confused and try a nonexistent path?

In practice, if the user runs `/conversus run` from inside the `conversus/` directory, the templates are at `./templates/{mode}/`. If they run from the monorepo root, they're at `conversus/templates/{mode}/`. The SKILL.md's "walk up" instruction is reasonable but relies on the LLM implementing a loop, which is atypical for LLM behavior.

**More likely failure**: The LLM will just try `conversus/templates/{mode}/review.md` as a relative path from CWD. If CWD is the monorepo root, this works. If CWD is `specs/001-feature/`, it fails. The `allowed-tools` includes `Bash(ls:*)` which lets the LLM search, but this is still a fragile first step.

**Fix**: Resolve the template directory to an absolute path during Step 1 (config parsing) and state it explicitly: "Determine the absolute path to the `conversus/` package directory. Store this as `CONVERSUS_ROOT`. Templates are at `{CONVERSUS_ROOT}/templates/{mode}/`." Then give concrete resolution logic: "If `conversus/templates/` exists relative to CWD, use CWD. Otherwise, check the parent of the config file's directory. Otherwise, check common locations."

---

## 8. Minimum Fixes for End-to-End Execution

Ordered by impact on correctness:

### Fix 1: Add `{AGENT_DOCS}` to Phase 2 variable list (Fragile -> Works)
**Location**: SKILL.md, Phase 2 section (around line 207)
**Change**: Add `{AGENT_DOCS}` to the "Additional template variables" list for Phase 2. State it is the reviewing agent's docs.
**Impact**: Without this, an LLM may leave `{AGENT_DOCS}` unreplaced in cross-review prompts, causing agents to see a literal string instead of doc paths.

### Fix 2: Add `{TARGET_FILES}` to synthesis template (Fragile -> Works)
**Location**: `templates/cooperative/synthesis.md`, lines 15-16; also SKILL.md Phase 5 variable list
**Change**: Replace the single `{TARGET_PATH}` under "What to Read" with `{TARGET_FILES}` or add `{TARGET_FILES}` alongside it. Add `{TARGET_FILES}` to Phase 5 variable definitions in SKILL.md.
**Impact**: Without this, multi-target deliberations produce a synthesis where the synthesizer only reads one target file, missing context from the others.

### Fix 3: Clarify revision filename resolution for iteration 2 (Fragile -> Works)
**Location**: SKILL.md, iteration loop section (around line 166-168)
**Change**: Add: "Note: `revision_{N-1}.md` when N-1 equals 1 resolves to `revision.md` (no numeric suffix). The unsuffixed name is always the iteration-1 output."
**Impact**: Without this, an LLM implementing iterations > 1 may look for `revision_1.md` instead of `revision.md`, causing file-not-found errors in iteration 2 cross-reviews.

### Fix 4: Add agent name validation (Edge case -> Prevented)
**Location**: SKILL.md, Step 1 validation section
**Change**: Add: "Agent names must match `[a-z0-9][a-z0-9-_]*` (lowercase alphanumeric, hyphens, underscores, no leading hyphen). Reject configs with invalid agent names."
**Impact**: Prevents silent file path collisions and invalid directory names.

### Fix 5: Make template resolution explicit (Fragile -> Works)
**Location**: SKILL.md, Step 3
**Change**: Replace "walk up" instruction with: "Resolve the conversus package directory: start from the directory containing the `conversus.yml` config file and search for `templates/{mode}/review.md` by checking (1) a `conversus/` subdirectory of the config's parent, (2) the config's parent directory itself, (3) walking up parent directories looking for `conversus/templates/`. Store the resolved absolute path as `TEMPLATE_DIR`."
**Impact**: Reduces the chance of template-not-found on the very first step.

---

## Summary Scorecard

| # | Finding | Verdict | Fix Priority |
|---|---------|---------|-------------|
| 1 | Agent counts per phase | **Works** | -- |
| 2a | Iteration loop diagram | **Works** | -- |
| 2b | Revision filename at iteration boundary | **Fragile** | P2 |
| 2c | `{ITERATION}` dead variable | **Fragile** | P3 |
| 3a | Phase 1 variables | **Works** | -- |
| 3b | Phase 2 missing `{AGENT_DOCS}` | **Fragile** | P1 |
| 3c | Phase 3 variables | **Works** | -- |
| 3d | Phase 4 variables | **Works** | -- |
| 3e | Phase 5 missing `{TARGET_FILES}` | **Fragile** | P1 |
| 3f | Phase 6 variables | **Works** | -- |
| 4 | `{PRIOR_FILES}` injection scope | **Fragile** | P2 |
| 5a | Trigger evaluation parsing | **Fragile** | P3 (fail-safe) |
| 5b | Trigger fallback behavior | **Works** | -- |
| 6a | Two-agent degenerate case | **Works** (known limitation) | -- |
| 6b | Agent name validation | **Broken** (silent path corruption) | P1 |
| 6c | Empty docs cosmetic | **Works** | -- |
| 7 | Template path resolution | **Fragile** | P1 |

**Bottom line**: The SKILL.md is well-structured and will produce correct output for the happy path (cooperative mode, 3 agents, 1 iteration, single target file, run from monorepo root). The four P1 fixes address the cases where it will silently produce wrong output or fail to execute: missing `{AGENT_DOCS}` in Phase 2, missing `{TARGET_FILES}` in synthesis, unsafe agent names, and ambiguous template resolution. Apply those four and this skill works end-to-end for all configurations.
