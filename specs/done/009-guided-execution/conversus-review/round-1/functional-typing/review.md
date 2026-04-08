# Cooperative Review: functional-typing

**Spec**: 009-guided-execution
**Target files**: `specs/009-guided-execution/spec.md`, `SKILL.md`
**Reviewer role**: Structural correctness and specification compliance
**Date**: 2026-03-22

---

## Executive Summary

The Converge handler in SKILL.md (lines 1326-1508) is a faithful implementation of spec 009. All ten functional requirements (FR-001 through FR-010) have corresponding handler sections. The implementation correctly maintains the zero-new-engine-logic constraint, the pre-execution summary is well-designed for non-experts, and the post-execution report properly references the Dispute-Parsing Subsystem. Two issues require attention: (1) FR-004's routing logic adds two sub-cases not in the spec (interests-without-problem, problem-without-interests) which is an expansion rather than a gap, and (2) the pre-execution summary labels its first field "Problem" but fills it with the mode, creating a confusing visual hierarchy.

---

## Alignment

### FR-001: Human-readable pre-execution summary

**Spec requirement** (spec.md, line 27): `/conversus converge` MUST read `conversus.yml` and present a human-readable summary: mode, agents, target documents, estimated agent launches.

**Implementation** (SKILL.md, lines 1366-1408): The "Pre-Execution Summary" section reads `conversus.yml`, parses it with the same schema as Run Step 1, and presents a structured summary including mode with plain-language explanation, agent names with one-sentence perspective summaries, target paths, output directory, rounds/iterations, and estimated agent launches. The plain-language mode explanations are provided at lines 1397-1400.

**Verdict**: Fully satisfied. The implementation exceeds the FR by also including the output directory, rounds, iterations, and arbiter configuration -- all useful for informed consent.

### FR-002: User confirmation before execution

**Spec requirement** (spec.md, line 28): The user MUST confirm before execution begins. No silent execution.

**Implementation** (SKILL.md, lines 1410-1422): "User Confirmation" section requires explicit user confirmation. Lines 1412-1413: "The user must explicitly confirm before execution begins. No silent execution." Decline routing is also specified.

**Verdict**: Fully satisfied. Exact language match with the spec requirement.

### FR-003: Decline routing to prior steps

**Spec requirement** (spec.md, line 29): If the user declines, the system MUST route them to `/conversus interests` or `/conversus mode`.

**Implementation** (SKILL.md, lines 1415-1422): When user says "no", the handler presents:
```
What would you like to change?
  - Agents or perspectives: /conversus interests
  - Mode or configuration: /conversus mode
  - Cancel entirely
```

**Verdict**: Fully satisfied. Adds "Cancel entirely" as a third option, which is a reasonable UX addition not contradicting the spec.

### FR-004: Missing prerequisite routing

**Spec requirement** (spec.md, lines 33-34): If no `conversus.yml` exists, check for `problem.md` and `interests.md`. If both exist, run mode selection first. If neither exists, start from `/conversus define`.

**Implementation** (SKILL.md, lines 1334-1356): The "Missing Prerequisite Check" section handles four sub-cases:
1. Both `problem.md` and `interests.md` exist (line 1341): routes to `/conversus mode` -- matches spec.
2. `interests.md` exists but `problem.md` does not (lines 1344-1346): routes to `/conversus define` first -- **expansion beyond spec**.
3. `problem.md` exists but `interests.md` does not (lines 1348-1349): routes to `/conversus interests` -- **expansion beyond spec**.
4. Neither exists (lines 1352-1354): routes to `/conversus define` -- matches spec.

**Verdict**: Satisfied with expansion. The spec only specifies two sub-cases (both exist, neither exists). The implementation adds two intermediate states (one without the other). This is a well-motivated completeness improvement -- a user who has `interests.md` but no `problem.md` would otherwise get the generic "neither exists" message, which is misleading. However, it should be noted that these additional branches are implementation decisions not backed by spec text.

### FR-005: Staleness warning

**Spec requirement** (spec.md, line 34): If `conversus.yml` exists but is stale (`interests.md` modified more recently), warn the user and suggest re-running `/conversus mode`.

**Implementation** (SKILL.md, lines 1358-1364): "Staleness Warning" compares modification times and emits the warning. The warning is informational and does not block execution.

**Verdict**: Fully satisfied. Line 1364 explicitly states: "This warning is informational. The user may proceed or regenerate."

### FR-006: Delegation to existing run engine

**Spec requirement** (spec.md, line 38): Execution MUST delegate to the existing `/conversus run` engine. Zero new execution logic.

**Implementation** (SKILL.md, lines 1424-1428): The "Execution" section states: "Delegate to `/conversus run` using the `conversus.yml` in the working directory." Line 1428 reinforces: "Zero new execution logic."

**Verdict**: Fully satisfied. The implementation adds no Phase logic, no template handling, no agent dispatch -- all of that remains in the Run handler (Step 4, lines 308-367).

### FR-007: Multi-round/arbitration transparency

**Spec requirement** (spec.md, line 39): Multi-round execution, arbitration, and inter-round arbitration work transparently.

**Implementation** (SKILL.md, line 1428): "`converge` passes through whatever the config specifies. The full Phase 1-6 pipeline, round loop, stagnation detection, and termination logic are all handled by the existing run engine."

**Verdict**: Fully satisfied. Explicit enumeration of the features that pass through transparently.

### FR-008: Completion report content

**Spec requirement** (spec.md, line 43): The completion report MUST include: what the mode means for interpreting results, path to `summary/final.md`, and suggested next steps.

**Implementation** (SKILL.md, lines 1430-1507): The "Post-Execution Report" includes:
- Mode interpretation guidance (lines 1456-1460) with mode-specific reading instructions.
- Results path to `{output}/summary/final.md` (line 1442) with context about single-round vs. multi-round.
- Arbiter ruling path when applicable (lines 1446-1448).
- Disputes section (lines 1462-1481).
- Next steps by outcome (lines 1483-1507).

**Verdict**: Fully satisfied. Exceeds the requirement with mode-specific interpretation guidance and conditional arbiter information.

### FR-009: Suggest arbitration when disputes remain

**Spec requirement** (spec.md, line 44): If disputes remain, suggest `/conversus arbitrate`.

**Implementation** (SKILL.md, lines 1466-1470):
```
Status: {dispute_count} dispute(s) remain unresolved.
  To resolve them, configure an arbiter and run: /conversus arbitrate
```

And in next steps (lines 1485-1489), disputes-remaining paths route to `/conversus arbitrate`.

**Verdict**: Fully satisfied.

### FR-010: Note when arbitration unnecessary

**Spec requirement** (spec.md, line 45): If all disputes converged, note that arbitration is not needed.

**Implementation** (SKILL.md, lines 1472-1475):
```
Status: All perspectives converged. No arbitration needed.
```

Next steps (lines 1499-1501) confirm: "No further deliberation needed."

**Verdict**: Fully satisfied.

---

## Zero New Engine Logic Assessment

The converge handler contains no execution logic. Specifically:

- **No phase orchestration**: No references to Phase 1-6 dispatch, template loading, agent launch, or background dispatch. All of that resides in Run Steps 2-4 (SKILL.md lines 243-367+).
- **No agent management**: No `run_in_background`, no agent prompt construction, no cross-review pair calculation.
- **No output file creation**: The converge handler reads output files (for the post-execution report via the Dispute-Parsing Subsystem) but never writes deliberation artifacts.
- **Delegation is explicit**: Line 1426 states "Delegate to `/conversus run`" -- this is routing, not reimplementation.

The only "logic" in converge is: (1) prerequisite file existence checks, (2) staleness comparison via modification time, (3) config parsing for the summary, (4) agent launch estimation formula, and (5) Dispute-Parsing Subsystem invocation for the post-execution report. Items 1-3 are pure UX. Item 4 reuses the formula from Run Step 4 (line 315). Item 5 reuses the subsystem defined at lines 747-775.

**Verdict**: The zero-new-engine-logic constraint is upheld.

---

## Pre-Execution Summary Quality

The pre-execution summary (lines 1366-1408) is well-structured for non-experts. Specific strengths:

1. **Plain-language mode explanations** (lines 1397-1400): Each mode is described in terms of what it does ("Find common ground," "Find the best option," "Figure out who owns what," "Stress-test the plan") rather than using game-theory terminology.

2. **Agent perspective summaries** (line 1408): Extracts one-sentence summaries instead of dumping full prompts.

3. **Launch estimate** (lines 1402-1406): Gives users a concrete number to reason about token cost before committing.

4. **Arbiter disclosure** (lines 1390-1391): If configured, the arbiter's name, trigger, timing, and influence are all visible.

**One concern**: The summary template at line 1377 labels the first field `Problem:` but fills it with the mode and its explanation. The spec's SC-004 (spec.md, line 54) expects a format like "4 agents, cooperative mode, 1 round, estimated 21 agent launches. Proceed?" The current template does communicate all of this, but the `Problem:` label is misleading -- it suggests a problem description (from `problem.md`) rather than the deliberation mode. This is a labeling issue, not a functional gap. The field should be labeled `Mode:` to match FR-001's language and the post-execution report's structure (which correctly uses `Mode:` at line 1439).

---

## Post-Execution Report: Dispute-Parsing Subsystem Usage

The post-execution report (lines 1462-1481) correctly references the Dispute-Parsing Subsystem. Specifically:

- **Line 1464**: "Use the same Dispute-Parsing Subsystem as Phase 6 trigger evaluation" -- this is the correct subsystem, defined at lines 747-775.
- **Subsystem outputs are used correctly**: The boolean output (`has disputes`) drives the three-way branching (disputes remain / all converged / arbitration ran). The integer output (`dispute_count`) is surfaced in the "disputes remain" message at line 1468.
- **Mode-appropriate headings**: The Dispute-Parsing Subsystem (lines 764-768) uses mode-specific headings (`### Remaining Disputes` for cooperative, `## Runner-Up` for winner-take-all, `### Disputed Risks` for red-blue, `## Disputed Boundaries` for prisoners-dilemma). The converge handler inherits this behavior by delegating to the subsystem rather than reimplementing parsing.

**One observation**: The handler does not explicitly state which file to parse for multi-round runs vs. single-round runs. The Phase 6 trigger evaluation (line 624) specifies: "For multi-round runs, this is the cross-round synthesis. For single-round runs, this is the Phase 5 synthesis." The converge post-execution report at line 1442 does distinguish these cases for display purposes, but the dispute-parsing instruction at line 1464 simply says "Check the run engine's output" without specifying which file. In practice, `{output}/summary/final.md` is the correct file in both cases (it is the Phase 5 synthesis for single-round and the cross-round synthesis for multi-round), so this is a documentation clarity issue rather than a functional bug.

---

## Missed Opportunities

### 1. No validation error preview in pre-execution summary

The handler parses the config at line 1370 and reports validation errors if parsing fails. However, there is no preview of potential issues that are warnings rather than errors -- for example, if `validate_templates: false` is set, the user is not warned that template validation will be skipped. For a guided on-ramp targeting non-experts, surfacing this in the summary would increase confidence.

### 2. No cost/time estimation beyond agent count

The pre-execution summary provides an agent launch count but no rough token or time estimate. For non-experts, "42 agent launches" is less meaningful than "approximately 15-20 minutes and ~200K tokens." This may be out of scope for 009 (it would require engine instrumentation), but it is the single most impactful addition for the guided workflow's target audience.

### 3. No dry-run capability

The spec's constraint at line 61 states: "`/conversus converge` works with a hand-crafted `conversus.yml`." A `--dry-run` flag that shows the pre-execution summary without the confirmation prompt would be useful for CI/CD pipelines or quick config validation. This is acknowledged as a future consideration in the Define handler (SKILL.md, line 801) but not carried forward to converge.

### 4. No prior context disclosure

If `prior:` files are configured in `conversus.yml`, the pre-execution summary does not mention them. For a user who inherited a config from a previous run, not knowing that prior context will influence all agents is a significant information gap. The summary template (lines 1374-1393) should include a "Prior context: {paths}" line when `PRIOR_FILES` is non-empty.

---

## Off-Base Assumptions

### 1. Pre-execution summary "Problem" field mislabeling

As noted in the summary quality section, the template at line 1377 uses `Problem:` as the label but fills it with the mode. This creates a false expectation that the problem definition from `problem.md` would be displayed. The label should be `Mode:` to match the post-execution report (line 1439) and the spec's FR-001 language.

### 2. Implicit assumption that `/conversus arbitrate` exists

FR-009's implementation (lines 1468-1469) routes to `/conversus arbitrate`, and the dispatch table (line 34) lists it as a future subcommand: "Future subcommands (not yet implemented): `arbitrate`, `gate`." The post-execution report confidently suggests `/conversus arbitrate` to the user, but this command does not exist yet. A non-expert following the guided flow will hit an "Unknown subcommand" error. The report should either:
- Gate the suggestion behind whether `arbitrate` is an implemented subcommand, or
- Add a parenthetical: "(coming soon -- for now, configure an `arbiter:` section in conversus.yml and re-run)"

### 3. FR-004 sub-case ordering assumes a specific workflow

The missing prerequisite check (lines 1340-1354) checks for `problem.md` and `interests.md` in a specific order. However, the check at line 1344 ("interests.md exists but problem.md does not") assumes this is an error state. A user might legitimately create `interests.md` manually without going through `/conversus define`. The routing message ("Run `/conversus define` first") may be unnecessarily prescriptive for advanced users. The spec's constraint at line 61 explicitly says converge should work with hand-crafted configs, but the prerequisite check only applies when `conversus.yml` is missing, so this is a minor tension rather than a contradiction.

---

## Actionable Recommendations

1. **P1 -- Fix "Problem" label to "Mode"**: Change line 1377 from `Problem: {mode in plain language}` to `Mode: {mode in plain language}`. This is a one-line fix that eliminates confusion between the problem definition artifact and the deliberation mode. Aligns with the post-execution report (line 1439) and FR-001's language.

2. **P1 -- Guard `/conversus arbitrate` suggestion**: At lines 1468-1469 and 1489, either add a note that `arbitrate` is not yet implemented, or rephrase to suggest configuring an `arbiter:` section in `conversus.yml` and re-running `/conversus converge`. This prevents non-experts from hitting a dead end in the guided flow.

3. **P2 -- Add prior context to pre-execution summary**: After the "Rounds:" line in the summary template (line 1387), add a conditional line: `Prior context: {paths, comma-separated}` when `PRIOR_FILES` is non-empty. This maintains informed consent for all configuration dimensions.

4. **P2 -- Clarify dispute-parsing file target**: At line 1464, specify: "Read `{output}/summary/final.md` (the cross-round synthesis for multi-round runs, or the Phase 5 synthesis for single-round runs)." This matches the Phase 6 trigger evaluation's specificity at line 624.

5. **P3 -- Consider `--dry-run` for converge**: Allow `converge --dry-run` to display the pre-execution summary and exit without prompting. Useful for config validation and non-interactive contexts. Low implementation cost since the summary logic already exists.

---

## Referenced Documentation

| Document | Lines | Relevance |
|----------|-------|-----------|
| `specs/009-guided-execution/spec.md` | 1-62 | Authoritative spec: FR-001 through FR-010, SC-001 through SC-004, constraints |
| `SKILL.md` | 20-37 | Subcommand dispatch table including `converge` routing |
| `SKILL.md` | 54-200 | Run: Input and config schema (reused by converge for parsing) |
| `SKILL.md` | 308-367 | Run: Step 4 Execute Phases (the engine converge delegates to) |
| `SKILL.md` | 691-745 | Run: Step 5 Report (the engine's own report that converge supplements) |
| `SKILL.md` | 747-775 | Dispute-Parsing Subsystem (reused by converge post-execution report) |
| `SKILL.md` | 1326-1508 | Converge: Guided Execution handler (primary review target) |
| `SKILL.md` | 1511-1545 | Important Notes and baseline features (context for engine delegation) |
