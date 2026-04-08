# Devil's Advocate Review: 009-Guided-Execution

**Reviewer**: devils-advocate (role/devils-advocate preset)
**Target**: specs/009-guided-execution/spec.md, SKILL.md (Converge handler)
**Date**: 2026-03-22

---

## Executive Summary

Spec 009 and its SKILL.md implementation present a clean UX wrapper around `/conversus run`. The consensus position will be that this is a well-scoped, minimal spec that "just works." I challenge that consensus. The spec makes several assumptions that deserve harder scrutiny: that a thin wrapper is sufficient for non-expert users, that staleness detection is meaningful, that the agent launch estimate is useful rather than alarming, and that the post-execution report can correctly assess dispute status without new logic. The spec also has a structural dependency problem -- it is the capstone of a four-spec guided workflow chain (007 -> 008 -> 009) where none of the upstream specs are implemented yet, making 009's "ready to build" posture premature.

---

## Alignment

### What the spec gets right

1. **Zero new engine logic** is the correct constraint. The spec (FR-006, FR-007) and the SKILL.md Converge handler both enforce this. The handler explicitly states: "Zero new execution logic. Multi-round execution (spec 002), arbitration (spec 001), and inter-round arbitration (spec 006) all work transparently." This is good architectural hygiene.

2. **Prerequisite routing** is thorough. The SKILL.md handler covers all four permutations of `problem.md` and `interests.md` existence, plus the staleness warning. FR-003, FR-004, FR-005 from the spec are fully mapped.

3. **The constraint in Section 4** -- "Must NOT require prior guided workflow steps" -- is well-conceived. It means `converge` works with hand-crafted YAML, not just the define-interests-mode pipeline. This prevents the guided workflow from becoming a walled garden.

---

## Missed Opportunities

### 1. No dry-run or cost estimation before token spend

The spec's SC-004 says the pre-execution summary should include "4 agents, cooperative mode, 1 round, estimated 21 agent launches." But agent launches are a meaningless proxy for cost. A user who does not understand the engine (the target persona per SC-001) has no mental model for what "21 agent launches" means in terms of time, token spend, or cost. The spec provides a number without a frame of reference.

Compare: if a cloud console said "this will launch 21 EC2 instances" with no pricing estimate, you would not call that user-friendly. The spec should either:
- Provide a rough token/time estimate (even "this typically takes 5-15 minutes and uses approximately X tokens"), or
- Acknowledge that the launch count is opaque to non-experts and explain what design decision makes it the best available proxy.

The SKILL.md implementation faithfully reproduces the formula `per_round_agents = N + iterations * (N*(N-1) + N) + N + 1`, but this formula is presented to the user as a bare number. For 5 agents with 2 iterations and 3 rounds, the estimate is 226 agent launches. A non-expert will see that number and either (a) have no idea what it means, or (b) panic and cancel.

### 2. No partial re-run or resume capability

If a 40-agent-launch deliberation fails at agent 35 (network error, timeout, model overload), the user starts over from scratch. `converge` is positioned as the "guided" path for non-experts, but it offers no recovery. A non-expert who just burned 34 successful agent calls and lost them to a Phase 5 failure will not have a good experience. The spec does not even acknowledge this failure mode, let alone address it.

This is not a request for new engine logic -- it is a request for the spec to state its position on failure recovery, even if that position is "out of scope, tracked as future work."

### 3. No config preview or diff capability

`converge` shows a summary and asks "Proceed?" But there is no way to see the full config, diff it against a previous run, or understand what changed since the last execution. For hand-crafted YAML users (permitted by Section 4's constraint), the summary may actually obscure details they care about. The one-sentence agent prompt summaries ("first line or summary of prompt") lose critical nuance.

### 4. The speckit integration in post-execution is premature

The SKILL.md Converge handler includes this next step for cooperative mode:
```
- To apply changes: /speckit.specify --input {output}/summary/final.md
```

This cross-tool integration is not mentioned anywhere in spec 009. It appears only in the SKILL.md implementation. This is spec drift -- the implementation includes behavior not authorized by any spec. Either spec 009 should document this integration, or the SKILL.md handler should remove it until a spec authorizes it.

---

## Off-Base Assumptions

### 1. "Staleness detection via modification time is meaningful"

FR-005 and the SKILL.md handler compare modification times of `interests.md` and `conversus.yml`. This assumption is fragile:

- **File copies, git operations, and editor autosaves all modify timestamps without changing content.** A `git checkout`, `git stash pop`, or even opening a file in some editors will update mtime. The staleness warning will fire on false positives.
- **Content changes that do not affect the config are invisible.** If a user edits `interests.md` to fix a typo in a perspective description but the agent prompts in `conversus.yml` are still correct, the warning fires unnecessarily.
- **The reverse is also broken.** If someone edits `conversus.yml` directly (adding an agent, changing mode), `interests.md` is now stale relative to the config, but the spec only checks one direction.

The spec should either use content hashing (store a hash of `interests.md` content inside `conversus.yml` when it is generated) or explicitly state that mtime-based detection is a best-effort heuristic with known false positives.

### 2. "A non-expert can interpret dispute status from the post-execution report"

The post-execution report tells the user "3 dispute(s) remain unresolved" and suggests `/conversus arbitrate`. But the target persona (SC-001: "a non-expert who used define -> interests -> mode") does not know what a "dispute" means in the conversus context, what arbitration does, or whether 3 disputes is a lot or a little.

The report provides status without interpretation. "3 disputes remain" is as opaque to a non-expert as "21 agent launches." The spec should require the report to explain what disputes are in plain language and what the practical consequence of unresolved disputes is (e.g., "3 areas where agents could not agree -- the synthesis document presents both sides but does not recommend a resolution").

### 3. "The prerequisite chain is stable enough to build against"

Spec 009 depends on spec 008 ("generates conversus.yml") which depends on spec 007 ("subcommand routing, problem.md schema"). Neither 007 nor 008 is implemented. The SKILL.md already contains handlers for `define`, `interests`, `mode`, and `converge` -- but these are all Draft status specs.

The converge handler's prerequisite routing (check for `problem.md`, `interests.md`, route to `define`/`interests`/`mode`) assumes those commands work. If 007 or 008's implementation reveals that `problem.md` or `interests.md` schemas need to change, the converge handler's routing logic and staleness detection both break.

Building the capstone before the foundation is validated is a risk the spec does not acknowledge. The dependency declaration says `Depends On: 008-interests-mode`, but it does not state whether 008 must be spec-complete or merely spec-drafted before 009 can be implemented.

### 4. "The agent launch formula is correct for all configurations"

The SKILL.md Converge handler uses the formula from Step 4:
```
per_round_agents = N + iterations * (N*(N-1) + N) + N + 1
max_total_agents = rounds * per_round_agents + (1 if arbiter) + (1 if rounds > 1)
```

But the Important Notes section gives a different simplified formula for single-round without arbiter: `N^2 + N + 1`. Let us verify with N=3, iterations=1:
- Step 4 formula: `3 + 1*(3*2 + 3) + 3 + 1 = 3 + 9 + 3 + 1 = 16`
- Important Notes: `9 + 3 + 1 = 13`

These do not agree. The Step 4 formula gives 16 for 3 agents; the Important Notes says 13. The discrepancy may come from how `iterations` is handled (whether the first cross-review counts as iteration 0 or 1), but the converge handler presents this number to the user as a commitment. If the estimate is wrong, the user either sees a number that is too high (wasting their trust) or too low (surprising them with extra agent calls). The spec should reconcile the two formulas or clarify which one the converge handler uses.

### 5. "Delegating to /conversus run is zero-complexity"

The spec and SKILL.md both insist converge "delegates to the existing /conversus run engine." But the SKILL.md handler says: "Delegate to /conversus run using the conversus.yml in the working directory." How does this delegation happen mechanically?

- Does `converge` call the `run` handler as a function? (There are no functions -- this is a SKILL.md, not code.)
- Does it re-invoke `/conversus run`? (This would be a new skill invocation mid-conversation.)
- Does the orchestrating agent simply proceed to execute Step 1 of the Run handler?

The spec says "delegate" but the SKILL.md is an instruction set for an LLM agent, not a codebase with function calls. The actual delegation mechanism is implicit: the agent reading the SKILL.md is expected to jump from the Converge handler to the Run handler sections. This is fragile -- it depends on the agent correctly interpreting "delegate" as "now follow the Run: Execution section." The spec should be explicit about what "delegation" means in a SKILL.md context.

---

## Actionable Recommendations

1. **Add a "What to Expect" section to the pre-execution summary** that translates agent launch count into approximate time and explains what happens during execution ("each agent reads the target documents and writes a review, then agents cross-review each other..."). This serves SC-001 (non-expert usability) far better than a bare number.

2. **Document the failure recovery position.** Even if the position is "failures require a full re-run," state it explicitly so non-experts know what to expect. Consider adding a recommendation in the post-failure output: "If this failed, you can re-run `/conversus converge` -- it will start fresh."

3. **Replace mtime-based staleness with content hashing**, or explicitly document mtime as a heuristic with known false-positive cases. If using mtime, add guidance: "This warning may appear after git operations that update file timestamps."

4. **Remove the speckit integration from the SKILL.md handler** (the `/speckit.specify --input` next step) or add it to spec 009's FR list. Undocumented cross-tool integrations are spec drift.

5. **Reconcile the agent launch formulas.** The Step 4 formula and the Important Notes formula disagree for N=3, iterations=1. The converge handler must use a single, verified formula. Add a worked example to the spec (not just the SKILL.md) showing the calculation for a concrete configuration.

6. **Make the delegation mechanism explicit in the spec.** Add a constraint or FR: "Delegation to /conversus run means the agent proceeds to execute Run: Execution Step 1 through Step 5 using the parsed config. No new skill invocation occurs."

7. **Add plain-language dispute explanation to the post-execution report.** Replace "3 dispute(s) remain unresolved" with something like "3 areas where agents could not reach agreement. The synthesis presents both perspectives but does not choose between them. To get a resolution, configure an arbiter."

---

## Referenced Documentation

- **specs/009-guided-execution/spec.md** -- Primary review target. FR-001 through FR-010, SC-001 through SC-004, constraints.
- **SKILL.md, lines 1326-1509** -- Converge: Guided Execution handler implementation.
- **SKILL.md, lines 308-370** -- Step 4: Execute Phases, agent launch formulas.
- **SKILL.md, lines 1511-1527** -- Important Notes, simplified agent count formulas.
- **SKILL.md, lines 747-775** -- Dispute-Parsing Subsystem (used by post-execution report).
- **specs/008-interests-mode/spec.md** -- Upstream dependency. Generates `conversus.yml` and `interests.md`.
- **specs/007-subcommand-dispatch-define/spec.md** -- Foundational dependency. Subcommand dispatch and `problem.md` schema.
- **specs/010-guided-arbitration/spec.md** -- Downstream consumer. `/conversus arbitrate` referenced in post-execution next steps.
- **specs/011-phase-consensus-gates/spec.md** -- Related spec demonstrating engine-independence pattern.
- **presets/role/devils-advocate.yml** -- Reviewer role definition.
