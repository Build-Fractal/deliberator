# Integration Architect Review — 008-interests-mode

**Spec**: `008-interests-mode` (Interest Discovery & Mode Selection)
**Target**: SKILL.md implementation of `interests` and `mode` handlers
**Date**: 2026-03-22

---

## Executive Summary

The SKILL.md implementation at lines 926-1296 is a faithful, thorough realization of spec 008. Every functional requirement (FR-001 through FR-013) has a direct, traceable counterpart in the SKILL.md handlers. All five success criteria (SC-001 through SC-005) are achievable from the implementation as written. The dispatch table, prerequisite routing, anchor links, and schema alignment with the run engine are all correctly wired.

There are two areas where the implementation goes beyond the spec in useful ways (existing-file refine semantics, staleness warning via mtime), one area where coverage is complete but the generated schema's roundtrip fidelity deserves explicit call-out, and one latent risk around preset-backed agents in generated configs that merits attention.

---

## Alignment: FR-to-Implementation Mapping

### FR-001: Read problem.md, suggest 2-5 interests with name/perspective/prompt/docs

**Satisfied.** SKILL.md lines 926-928: "`/conversus interests` reads `problem.md` and identifies the competing perspectives that will deliberate. Each interest becomes an agent with a name, perspective, calibrated identity prompt, and suggested documentation paths."

Lines 955-956: "Read the Type field from `problem.md` and generate 2-5 interests calibrated to the problem type."

Lines 1034-1046 define the output schema requiring `Perspective`, `Prompt`, and `Docs` fields per interest under `###` headings.

### FR-002: Prompts calibrated to problem type

**Satisfied.** SKILL.md lines 957-962 contain the exact calibration table from the spec:
- `selection`: adversarial ("passionate advocate")
- `integration`: cooperative ("ensure requirements are met while finding workable integration points")
- `scoping`: honesty-calibrated ("honestly declare what falls within your responsibility")
- `stress-test`: red/blue roles ("red-team attacker" / "blue-team defender")

These match the spec's four calibration styles at spec lines 32-36.

### FR-003: User MAY add explicit interests via `--add <name>`

**Satisfied.** SKILL.md lines 947-949: "`/conversus interests --add <name>` -- adds a named interest to the suggestions. The agent generates a prompt for it and asks the user for documentation paths. May be repeated: `--add security --add performance`."

Lines 968-970 define the follow-up questions for `--add` interests.

### FR-004: Ungrounded agents marked with [NEEDS DOCS]

**Satisfied.** SKILL.md lines 974-981: "If an interest has no documentation paths (empty `docs` list), mark it with: `[NEEDS DOCS: <suggestion of what documentation would strengthen this interest's arguments>]`" with a user-facing warning about weaker arguments.

Line 1050 reinforces: "If empty, use `- (none)` and include the `[NEEDS DOCS: ...]` tag after it."

### FR-005: Existing interests.md triggers add/remove/modify flow

**Satisfied.** SKILL.md lines 996-1004: "If `interests.md` already exists in the output directory: 1. Read and present the existing interests to the user as a numbered list with names and perspectives. 2. Ask: 'interests.md already exists with {count} interests. Add new interests, remove existing ones, or modify?' 3. Based on user choice: Add/Remove/Modify."

Line 1004: "Never silently overwrite an existing `interests.md`."

### FR-006: Preset matching and suggestion

**Satisfied.** SKILL.md lines 985-992: "After generating interests, check whether any interest matches a preset from the `presets/` directory (spec 004). For each interest, search all preset files for name or category matches. If a preset matches a suggested interest, note it to the user: 'Interest "{name}" matches the `{category/preset-name}` preset. Use the preset?'"

Lines 1041 and 1052 define the `Preset` field in the interests.md schema.

### FR-007: Mode recommendation via decision matrix

**Satisfied.** SKILL.md lines 1136-1143 contain the decision matrix with all four problem types, their default modes, and confidence levels. Plain-language descriptions are included (e.g., "Find the best option -- each perspective argues for its choice, and the strongest case wins"), satisfying the constraint at spec line 103 about not requiring game theory knowledge.

### FR-008: Mixed signals present top 2 candidates with trade-off comparison

**Satisfied.** SKILL.md lines 1159-1176: "When no single mode has a clear lead (top two modes are within close signal density), present the top 2 candidates with a plain-language trade-off comparison" with an explicit template showing Option A vs Option B, signals that match each, and a user prompt.

Line 1176: "Do not use game theory terminology in the comparison unless the user has already used it."

### FR-009: User MAY override recommendation

**Satisfied.** SKILL.md lines 1180-1191: The `--mode <mode-name>` flag, validation of mode names, and trade-off explanation when the override differs from recommendation. Quote: "If the chosen mode differs from the recommendation, explain the trade-off in plain language."

### FR-010: Output is a valid conversus.yml with mode, target, output, agents, iterations

**Satisfied.** SKILL.md lines 1231-1260 define the generated YAML structure with all required fields: `mode`, `target` (from problem.md Source Documents), `output` (default `conversus-output/`), `iterations` (default 1), and `agents` with `name`, `prompt`, `docs`, and conditional `role`.

Line 1254: "`target`: the Source Documents paths from `problem.md`."

### FR-011: Generated YAML uses exact same schema as hand-crafted configs

**Satisfied.** SKILL.md line 1231: "The file MUST use the exact same schema as hand-crafted configs (as defined in the Run: Execution Step 1 section). No schema extensions."

Lines 1263-1273 define post-write validation using the same validation rules from Run: Execution Step 1 (mode enum, target existence, 2+ agents, name pattern, role validation for red-blue).

### FR-012: Existing conversus.yml shows diff and asks before overwriting

**Satisfied.** SKILL.md lines 1214-1227: "If `conversus.yml` already exists in the output directory: 1. Read the existing config. 2. Show what would change: mode, agents, target. 3. Ask: 'Overwrite with the new configuration?'"

Line 1227: "Never silently overwrite an existing `conversus.yml`."

### FR-013: Staleness warning when interests.md changed since conversus.yml

**Satisfied.** SKILL.md lines 1117-1122: "If `interests.md` has a more recent modification time than `conversus.yml` (when `conversus.yml` already exists), warn: 'interests.md has changed since conversus.yml was last generated. Your config may be out of date.'"

---

## Success Criteria Verification

### SC-001: interests + mode on "selection" problem produces mode: winner-take-all

**Achievable.** The interests handler (lines 957-958) generates adversarial interests for `selection` type. The mode handler's decision matrix (line 1140) maps `selection` to `winner-take-all` with High confidence. The generated conversus.yml (lines 1236-1250) will contain `mode: winner-take-all`.

### SC-002: Agent identity prompts reference specific problem context

**Achievable.** SKILL.md line 966: "Each generated interest must reference the specific problem context from `problem.md` -- the Decision, Constraints, and Context sections. Do not produce generic 'You are an expert in X' placeholders."

### SC-003: Generated conversus.yml is valid input for /conversus run

**Achievable.** Post-write validation (lines 1263-1273) applies the same validation rules as Run: Execution Step 1. The schema at lines 1235-1250 uses the same YAML structure as the run engine's schema (lines 54-104). No schema extensions are introduced (line 1231).

### SC-004: Overriding mode to cooperative on a selection problem produces correct output with trade-off explanation

**Achievable.** Lines 1180-1191 handle the `--mode` override. When the chosen mode differs from the recommendation, the handler explains the trade-off (line 1183-1190) and proceeds with the chosen mode (line 1191). The generated conversus.yml will contain the overridden mode.

### SC-005: Missing problem.md routes to /conversus define

**Achievable.** SKILL.md lines 934-939: "If `problem.md` does not exist: 'No problem.md found. Run `/conversus define` first to create a problem definition.' Stop processing."

---

## Dispatch Table and Routing Verification

### Dispatch table (lines 23-29)

The dispatch table at SKILL.md lines 23-29 includes all four subcommands:

| Invocation | Routes to |
|---|---|
| `/conversus interests [options]` | `[Interests: Interest Discovery](#interests-interest-discovery)` |
| `/conversus mode [options]` | `[Mode: Mode Selection](#mode-mode-selection)` |

Both anchors resolve correctly:
- `#interests-interest-discovery` matches the heading at line 926: `## Interests: Interest Discovery`
- `#mode-mode-selection` matches the heading at line 1093: `## Mode: Mode Selection`

Line 37: "Subcommand matching is exact and case-sensitive. The dispatch table is exhaustive."

### Prerequisite routing

**Interests handler prerequisite** (lines 933-941):
- Missing `problem.md` produces: "No problem.md found. Run `/conversus define` first."
- Stops processing. Does not attempt inference. Correct per SC-005.
- Also validates problem.md headings if it exists (line 941).

**Mode handler prerequisite** (lines 1099-1115):
- Missing `interests.md` with `problem.md` present: "Run `/conversus interests` first."
- Missing both: "Start with `/conversus define`."
- Missing `problem.md` with `interests.md` present: "Run `/conversus define` first. The mode command needs both."
- Three-case routing covers all prerequisite permutations correctly.

---

## Generated conversus.yml Schema Alignment with Run Engine

The generated schema (lines 1235-1250) maps to the run engine schema (lines 54-104):

| Generated Field | Run Engine Field | Alignment |
|---|---|---|
| `mode` | `mode` | Exact match -- same enum values |
| `target` (list of paths) | `target` (string or list) | Compatible -- run engine accepts both |
| `output: conversus-output/` | `output` | Exact match |
| `iterations: 1` | `iterations` | Exact match |
| `agents[].name` | `agents[].name` | Exact match -- same `[a-z0-9][a-z0-9-_]*` pattern |
| `agents[].prompt` | `agents[].prompt` | Exact match |
| `agents[].docs` | `agents[].docs` | Exact match |
| `agents[].role` | `agents[].role` | Exact match -- only for red-blue mode |
| `agents[].preset` | `agents[].preset` | Exact match -- line 1260 |

Fields intentionally omitted from generation: `rounds`, `stagnation`, `validate_templates`, `prior`, `arbiter`. This is correct -- these are advanced fields that users add manually. The generated config is a valid minimal config.

---

## Missed Opportunities

### 1. No `--context` passthrough from interests to mode

The interests handler reads `problem.md` from the output directory but does not support a `--context` flag to ingest additional docs during interest generation. The define handler has `--context`. This is not a spec violation (the spec does not require it for interests), but the asymmetry may confuse users who expect the guided workflow to accumulate context.

### 2. No draft/ready status on interests.md

The define handler annotates `problem.md` with `status: draft | ready` based on `[CLARIFY:]` tags. The interests handler does not produce a similar status field on `interests.md`, even though `[NEEDS DOCS:]` tags serve an analogous "not fully ready" role. The spec does not require it, but parity would enable downstream commands to check readiness programmatically.

### 3. Heuristic detection signals are documented but not structured

The heuristic mode detection signals (SKILL.md lines 1149-1155) are prose descriptions. A structured signal-to-mode mapping (similar to the decision matrix table) would make the detection logic more deterministic and testable. The spec similarly leaves these as prose (spec lines 63-68).

---

## Off-Base Assumptions

None identified. The implementation faithfully reflects the spec's scope, constraints, and design intent. The three constraints from spec section 4 are all honored:

1. **No game theory knowledge required** -- SKILL.md line 1176: "Do not use game theory terminology in the comparison unless the user has already used it." Decision matrix includes plain-language descriptions (lines 1140-1143).

2. **No agents generated without user confirmation** -- Interests handler: line 1020 "Do not write `interests.md` until the user confirms." Mode handler: line 1210 "Do not write `conversus.yml` until the user confirms."

3. **No hard-coded agents or doc paths** -- All interests are generated from problem context (line 966). No hard-coded agent names or paths appear in either handler.

---

## Actionable Recommendations

### R-1: Validate preset-backed agent roundtrip (Priority: Medium)

SKILL.md line 1260 says: "If an interest referenced a preset, include `preset: <category/preset-name>` on the agent entry instead of inlining the prompt." This is efficient, but it means the generated conversus.yml's validity depends on the preset file existing at run time. The post-write validation (lines 1263-1273) checks that each agent has `name` and `prompt` (or `preset`) but does not resolve the preset to verify it exists. Consider adding preset existence validation to the post-write check to catch stale preset references before `/conversus run` fails.

### R-2: Clarify target path handling when Source Documents is "(none)" (Priority: Medium)

SKILL.md line 1254 handles the case: "If Source Documents contains `(none)`, ask the user: 'What files should agents review?'" This is correct, but the spec's problem.md schema (spec lines 879-881) shows Source Documents as a list of paths. The `(none)` sentinel comes from the define handler's empty-section handling (SKILL.md line 891). Consider documenting this sentinel explicitly in the interests handler as well, since interests also reads problem.md's Source Documents when constructing its Problem Reference section.

### R-3: Coordinate interest name validation across handlers (Priority: Low)

Both handlers independently validate interest/agent names against `[a-z0-9][a-z0-9-_]*` (interests: line 964, mode: line 1268, run: line 198). This is correct but the pattern is specified in three places. If the pattern changes, all three must be updated. This is a documentation/maintenance observation, not a bug.

### R-4: Consider adding `--dry-run` to mode handler (Priority: Low)

The define handler notes `--dry-run` as a future consideration (SKILL.md line 797). The mode handler generates a more consequential artifact (the executable conversus.yml). A `--dry-run` flag that outputs the YAML to stdout without writing would pair well with the existing confirmation flow. Not a spec requirement, but a natural extension.

---

## Referenced Documentation

| Reference | Location | Purpose |
|---|---|---|
| Spec FR-001 through FR-006 | spec.md lines 31-40 | Interest discovery requirements |
| Spec FR-007 through FR-013 | spec.md lines 44-59 | Mode selection requirements |
| Spec SC-001 through SC-005 | spec.md lines 93-97 | Success criteria |
| Spec decision matrix | spec.md lines 46-52 | Mode recommendation table |
| Spec heuristic signals | spec.md lines 63-68 | Signal-to-mode inference |
| Spec interests.md schema | spec.md lines 72-87 | Output format |
| Spec constraints | spec.md lines 101-105 | Design constraints |
| SKILL.md dispatch table | SKILL.md lines 23-29 | Subcommand routing |
| SKILL.md interests handler | SKILL.md lines 926-1090 | Full interests implementation |
| SKILL.md mode handler | SKILL.md lines 1093-1296 | Full mode implementation |
| SKILL.md run engine schema | SKILL.md lines 54-104 | conversus.yml schema definition |
| SKILL.md agent name validation | SKILL.md line 198 | Name pattern constraint |
| SKILL.md prerequisite check (interests) | SKILL.md lines 933-941 | Missing problem.md routing |
| SKILL.md prerequisite check (mode) | SKILL.md lines 1099-1115 | Three-case prerequisite routing |
| SKILL.md interest generation table | SKILL.md lines 957-962 | Calibration by problem type |
| SKILL.md mode decision matrix | SKILL.md lines 1136-1143 | Mode recommendation with descriptions |
| SKILL.md mixed-signal handling | SKILL.md lines 1159-1176 | Top-2 candidate presentation |
| SKILL.md post-write validation (interests) | SKILL.md lines 1055-1064 | Interest output validation |
| SKILL.md post-write validation (mode) | SKILL.md lines 1262-1275 | Config output validation |
| SKILL.md staleness warning | SKILL.md lines 1117-1122 | interests.md vs conversus.yml mtime check |
| SKILL.md preset-backed agents | SKILL.md line 1260 | Preset reference in generated config |
