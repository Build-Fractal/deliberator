# Integration Architect Review: 009-Guided-Execution

**Reviewer**: integration-architect
**Spec**: `009-guided-execution`
**Implementation**: SKILL.md `Converge: Guided Execution` section (lines 1326-1508)
**Date**: 2026-03-22

---

## Executive Summary

The `converge` handler is cleanly implemented as a UX wrapper around the existing `run` engine. All 10 functional requirements from the spec map to concrete implementation sections in SKILL.md. The dispatch table, prerequisite routing, and delegation model are sound. Two issues require attention: (1) the spec's FR-003 routing to `/conversus interests` and `/conversus mode` is implemented with a third option ("Cancel entirely") that the spec does not mention, and (2) the `/conversus arbitrate` next-step suggestion references a subcommand listed as "not yet implemented" in the dispatch table, creating a dead reference in the guided flow.

---

## Alignment

### FR-to-Implementation Mapping

| FR | Spec Requirement | SKILL.md Implementation | Status |
|----|-----------------|------------------------|--------|
| **FR-001** | Read `conversus.yml`, present human-readable summary: mode (plain-language), agents (names + one-line perspectives), target docs, estimated launches | SKILL.md lines 1366-1408: Pre-Execution Summary section. Parses config using Run Step 1 schema. Presents mode with plain-language explanation (lines 1397-1400), agents with one-sentence perspective extracted from prompt (line 1408), target paths, rounds/iterations, and computed agent launch estimate using the `per_round_agents` formula. | **ALIGNED** |
| **FR-002** | User MUST confirm before execution. No silent execution. | SKILL.md lines 1410-1422: User Confirmation section. Explicit "Proceed? (yes / no)" with hard stop on decline. "No silent execution" is stated. | **ALIGNED** |
| **FR-003** | If user declines, route to `/conversus interests` (modify agents) or `/conversus mode` (change mode). | SKILL.md lines 1415-1422: Decline routing presents three options: interests, mode, or "Cancel entirely." The spec lists two routing targets; the implementation adds a third (cancel). This is a superset, not a violation, but the spec's "MUST route them" language does not contemplate cancellation. | **ALIGNED (superset)** |
| **FR-004** | If no `conversus.yml`, check for `problem.md` and `interests.md`. If both exist, run mode first. If neither, start from `/conversus define`. | SKILL.md lines 1336-1356: Missing Prerequisite Check. Four-case permutation: (1) both exist -> route to `/conversus mode`, (2) `interests.md` only -> route to `/conversus define`, (3) `problem.md` only -> route to `/conversus interests` then `/conversus mode`, (4) neither -> route to `/conversus define`. All four permutations are covered. | **ALIGNED** |
| **FR-005** | If `conversus.yml` exists but stale (interests.md modified more recently), warn and suggest re-running `/conversus mode`. | SKILL.md lines 1358-1364: Staleness Warning section. Compares modification times of `interests.md` vs `conversus.yml`. Warning is informational, user may proceed or regenerate. | **ALIGNED** |
| **FR-006** | Execution MUST delegate to existing `/conversus run` engine. Zero new execution logic. `converge` is routing + UX, not a new engine. | SKILL.md lines 1424-1428: Execution section. Explicitly states "Delegate to `/conversus run`" and "Zero new execution logic." Multi-round, arbitration, inter-round arbitration all described as "work transparently" via passthrough. | **ALIGNED** |
| **FR-007** | Multi-round execution, arbitration, and inter-round arbitration work transparently -- `converge` passes through. | SKILL.md line 1428: "The full Phase 1-6 pipeline, round loop, stagnation detection, and termination logic are all handled by the existing run engine." | **ALIGNED** |
| **FR-008** | Completion report MUST include: mode interpretation, path to `summary/final.md`, suggested next steps. | SKILL.md lines 1430-1508: Post-Execution Report section. Report structure includes mode interpretation (lines 1456-1460), results path (lines 1442-1444), and next steps by outcome (lines 1483-1507). | **ALIGNED** |
| **FR-009** | If disputes remain, suggest `/conversus arbitrate`. | SKILL.md lines 1466-1470: Disputes section, disputes-remain case: "To resolve them, configure an arbiter and run: /conversus arbitrate." | **ALIGNED (with caveat -- see below)** |
| **FR-010** | If all disputes converged, note arbitration is not needed. | SKILL.md lines 1472-1475: "All perspectives converged. No arbitration needed." | **ALIGNED** |

### Dispatch Routing Verification

The subcommand dispatch table (SKILL.md lines 20-39) correctly includes `converge`:

| Invocation | Routes to |
|---|---|
| `/conversus converge` | `Converge: Guided Execution` anchor |

The dispatch table is exhaustive with exact, case-sensitive matching (line 39). Unknown subcommands produce a clear error listing all available commands including `converge` (line 37). The no-argument default routes to `run`, not `converge`, preserving backward compatibility (line 31). This is correct -- `converge` is opt-in for guided users, not a replacement for `run`.

### Prerequisite Routing Permutation Verification

The spec (FR-004) describes two conditions. The implementation (SKILL.md lines 1336-1356) covers all four permutations of `{problem.md, interests.md}` existence:

| problem.md | interests.md | Implementation Route | Spec Coverage |
|------------|-------------|---------------------|--------------|
| YES | YES | Route to `/conversus mode` | FR-004: "If both exist, run mode selection first" -- **MATCH** |
| NO | YES | Route to `/conversus define` first | Not explicitly in spec, but consistent with the prerequisite chain -- **REASONABLE EXTENSION** |
| YES | NO | Route to `/conversus interests` then `/conversus mode` | FR-004 does not enumerate this case explicitly; the spec says "If neither exists, start from `/conversus define`" -- the implementation correctly infers the middle step -- **REASONABLE EXTENSION** |
| NO | NO | Route to `/conversus define` | FR-004: "If neither exists, start from `/conversus define`" -- **MATCH** |

The implementation covers two cases the spec does not explicitly address (interests without problem, problem without interests). Both are handled correctly by routing to the earliest missing step in the `define -> interests -> mode` chain. This is sound engineering -- the spec's two-case description was an underspecification, not a constraint.

### UX Wrapper Verification

The handler is verified as a pure UX wrapper:

1. **No execution logic**: The Execution section (lines 1424-1428) contains exactly one action: "Delegate to `/conversus run`." No phase orchestration, no agent dispatch, no template loading, no output directory creation.

2. **No new state**: The handler reads `conversus.yml` (existing artifact), reads `interests.md` modification time (filesystem metadata only), and reads synthesis output (existing artifact from `run`). It creates no new persistent artifacts.

3. **No new configuration**: The handler does not extend the `conversus.yml` schema. It uses "the same schema defined in Run: Execution Step 1" (line 1370).

4. **Pre/post only**: The handler's three sections map to: pre-flight (prerequisite check, staleness warning, summary, confirmation), flight (delegation), and post-flight (report with interpretation and next steps). The flight section is a single delegation call.

5. **Dispute parsing reuse**: The post-execution report uses "the same Dispute-Parsing Subsystem as Phase 6 trigger evaluation" (line 1464), not a new parser.

---

## Missed Opportunities

### 1. Dead Reference: `/conversus arbitrate` Is Not Implemented

FR-009 and the post-execution report (lines 1469, 1489) suggest `/conversus arbitrate` as a next step. However, the dispatch table (line 34) explicitly lists `arbitrate` as "Future subcommands (not yet implemented)." A guided user who follows this suggestion will hit the unknown-subcommand error:

> Unknown subcommand: 'arbitrate'. Available commands: run, define, interests, mode, converge. (Future: arbitrate, gate)

**Recommendation**: The post-execution report should either (a) replace the `/conversus arbitrate` suggestion with guidance on how to add an `arbiter:` section to `conversus.yml` and re-run `/conversus converge`, or (b) note that `/conversus arbitrate` is a planned feature and provide the manual workaround in the interim. This is the highest-priority gap because it breaks the guided flow at the moment the user most needs guidance.

### 2. No `--output` Flag on Converge

Both `define`, `interests`, and `mode` accept `--output <dir>` to override the working directory. The `converge` handler has no `--output` flag -- it only reads from the current working directory (line 1336: "check whether `conversus.yml` exists in the working directory"). If a user ran `define --output my-delib/`, `interests --output my-delib/`, and `mode --output my-delib/`, they cannot run `converge` without `cd my-delib/` or moving the file.

**Recommendation**: Add `--output <dir>` to the converge handler for consistency with the upstream guided commands. This is a minor ergonomic gap, not a correctness issue.

### 3. No Handling of Run Engine Failures in Post-Execution

The post-execution report assumes a successful run. The `run` engine has explicit failure handling for Phase 6 (lines 662-666) and template validation (line 304), but the `converge` handler does not describe what happens if the delegated `run` fails mid-execution (e.g., template not found, agent timeout, validation error). Since `converge` is targeting non-experts, a plain-language failure report would be more valuable than the raw engine error.

**Recommendation**: Add a brief failure-handling clause: "If `/conversus run` fails, present the error in plain language and suggest corrective action (e.g., 'Template not found -- ensure the templates/ directory exists relative to your config file')."

### 4. Staleness Check Is One-Directional

FR-005 checks if `interests.md` is newer than `conversus.yml`. But `problem.md` could also have been modified after `conversus.yml` was generated (e.g., user refined the problem definition). The mode handler checks `interests.md` vs `conversus.yml` (line 1134), but neither handler checks `problem.md` vs `conversus.yml`.

**Recommendation**: Extend the staleness check to also compare `problem.md` modification time against `conversus.yml`. If `problem.md` is newer, suggest re-running both `/conversus interests` and `/conversus mode`.

---

## Off-Base Assumptions

### 1. None Identified in the Spec-to-Implementation Mapping

The spec's constraints are correctly respected:

- "Must NOT add execution logic" (spec Constraint 1) -- verified, the handler delegates entirely.
- "Must NOT require prior guided workflow steps" (spec Constraint 2) -- verified: the handler works with a hand-crafted `conversus.yml` that was never produced by `define/interests/mode`. The prerequisite check (lines 1336-1356) only fires when `conversus.yml` is absent. If the file exists, the handler proceeds regardless of whether `problem.md` or `interests.md` exist.

### 2. Spec Assumption Worth Noting

The spec states (FR-001): "estimated agent launches." The implementation computes `max_total_agents` using the formula from the run engine. This is a maximum, not an estimate -- actual launches may be lower due to early termination. The implementation correctly labels it "Estimated agent launches" (line 1388), which matches the spec language, but the underlying formula computes the upper bound. This is accurate labeling (an upper-bound estimate is still an estimate), but could confuse users who expect an exact number.

---

## Actionable Recommendations

| Priority | Recommendation | Rationale |
|----------|---------------|-----------|
| **P0** | Replace `/conversus arbitrate` suggestions in the post-execution report with actionable workaround guidance until the `arbitrate` subcommand is implemented. | Dead reference breaks the guided flow for the primary persona (non-expert user). |
| **P1** | Add `--output <dir>` flag to the converge handler. | Consistency with `define`, `interests`, and `mode` handlers; prevents workflow breakage when users specify a non-default output directory. |
| **P2** | Add plain-language failure handling for delegated `run` errors. | Non-expert users (SC-001 persona) cannot interpret raw engine errors. |
| **P2** | Extend staleness check to include `problem.md` modification time. | Prevents stale config execution when the problem definition changes. |
| **P3** | Clarify in the post-execution report that "Estimated agent launches" is an upper bound. | Prevents confusion when actual launches are lower due to early termination. |

---

## Success Criteria Verification

### SC-001: Non-expert can execute without editing YAML or understanding engine internals.

**SATISFIED.** The `converge` handler provides a complete guided path: prerequisite routing (lines 1336-1356) catches users who skipped steps, the pre-execution summary (lines 1366-1408) presents the config in plain language, and the post-execution report (lines 1430-1508) interprets results with mode-specific guidance. At no point does the handler require the user to read or edit YAML. The one gap is the `/conversus arbitrate` dead reference (see P0 recommendation), which would break the guided flow if disputes remain.

### SC-002: Output from `/conversus converge` is identical to `/conversus run` with the same config.

**SATISFIED.** The Execution section (line 1426) states: "Delegate to `/conversus run` using the `conversus.yml` in the working directory. This is the same engine invoked by `/conversus run` with no arguments." The handler adds pre-flight and post-flight UX but does not modify inputs, outputs, or engine behavior. The `converge` handler's post-execution report is supplementary (line 1432: "supplements (does not replace) the run engine's own Step 5 report"), so the run engine's standard report is also emitted.

### SC-003: Missing prerequisites route to the correct prior step, not an error.

**SATISFIED.** All four prerequisite permutations produce actionable routing messages (lines 1340-1354), not error codes or stack traces. Each message names the specific command to run next. The routing messages use plain language consistent with the guided workflow persona. See the prerequisite routing permutation table above for detailed verification.

### SC-004: Pre-execution summary is plain language, not a YAML dump.

**SATISFIED.** The summary format (lines 1374-1393) uses structured plain text with labeled fields. Mode is presented with a plain-language explanation (lines 1397-1400), not the YAML key. Agents are presented with one-sentence perspectives extracted from prompts (line 1408), not raw prompt text. The spec's example ("4 agents, cooperative mode, 1 round, estimated 21 agent launches. Proceed?") maps directly to the implementation's format. The implementation adds more structure (separate lines for each field) but maintains the plain-language requirement.

---

## Referenced Documentation

- **Spec**: `<HOME>/code/payer-index-mono/conversus/specs/009-guided-execution/spec.md` -- 10 FRs, 4 SCs, 2 constraints
- **Implementation**: `<HOME>/code/payer-index-mono/conversus/SKILL.md` -- Converge handler at lines 1326-1508; dispatch table at lines 20-39; run engine at lines 44-745; dispute-parsing subsystem at lines 747-774; define handler at lines 778-927; interests handler at lines 930-1105; mode handler at lines 1108-1323
- **Dispatch table**: SKILL.md lines 24-31 -- `converge` routes to `Converge: Guided Execution` anchor
- **Future subcommands**: SKILL.md line 34 -- `arbitrate` and `gate` listed as not yet implemented
- **Agent launch formula**: SKILL.md lines 1402-1406 -- `per_round_agents = N + iterations * (N*(N-1) + N) + N + 1`
- **Dispute-Parsing Subsystem**: SKILL.md lines 747-774 -- reused by converge post-execution report (line 1464)
