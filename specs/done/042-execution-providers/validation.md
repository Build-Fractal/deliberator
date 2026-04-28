# Spec 042 — Validation Battery for the Winning Architecture

**Created**: 2026-04-05
**Purpose**: Tests the winning execution provider architecture must pass before
the arbiter's ruling is treated as final. This document is cited by the
conversus-chief-architect arbiter in Phase 6 of the spec 042 deliberation.

## Why this exists

The conversus deliberation (4 agents, winner-take-all, binding arbiter) will
select ONE architecture. That architecture then has to carry the weight of
every downstream spec that depends on it. Picking "the best position in the
deliberation" is not the same as picking "the architecture that makes the
rest of the roadmap easier." This document bridges that gap.

The arbiter must confirm — in the final ruling — that the winning architecture
passes each test below, or explicitly document which tests it cannot pass and
why the trade-off is acceptable.

---

## 1. Downstream spec compatibility

For each dependent spec, confirm the winner makes it *easier*, not harder.

### 1.1 Spec 048 — Autonomous Governance Mode (HARD dependency)

Spec 048 is the "CLI that runs outside your CLI" vision. It requires headless
execution in CI, cron, and git hooks. This is the *hard* dependency on 042.

**Test**: Can the winner support `conversus governance --gate pr` running
inside a GitHub Actions workflow with these constraints?
- No interactive terminal
- Exit codes: 0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE
- Per-invocation API key management (GitHub secrets → env)
- Artifact upload of deliberation output for PR comment posting
- Sub-5-minute wall time for the common case (small PR, no disputes)

**Pass criteria**: The winner must expose a non-interactive entry point, must
pass credentials through without leaking to logs, and must produce machine-
readable exit codes without Python exceptions bubbling out.

### 1.2 Spec 048 — Runtime agent discovery

Spec 048 §10 Q4 and Q8 ask about dynamic agent selection. The `.conversusrc`
file declares default agents — can these be URLs (pointing to A2A servers or
remote MCP servers) as well as preset strings?

**Test**: Does the winner's provider registry support URL-addressable agents
as first-class entries, even if the implementation says "not yet supported" in
v1? (This is the a2a-future-advocate's flagged concern.)

**Pass criteria**: The config schema must not forbid URL entries. An error
saying "URL-addressable agents not yet supported in v1" is acceptable; a
schema that rejects the field outright is not, because it would require a
migration to add later.

### 1.3 Spec 040 — Command Center

Spec 040 is a non-technical dashboard + copilot that shells out to conversus
for deliberations. It needs rich metadata, not just final output.

**Test**: Can a dashboard (web or TUI) display the following while a
deliberation is running?
- Phase progress (which phase, which agent within the phase)
- Per-agent token/dollar cost so far
- Per-agent elapsed time
- Cancel button that actually kills in-flight subprocesses
- Final artifacts with stable paths for dashboard linking

**Pass criteria**: The winner must expose these as structured events or
polling endpoints, not just end-of-run logs.

### 1.4 Spec 046 — Commentator Agents (post-synthesis dispatch)

Spec 046 runs two commentator agents AFTER Phase 5 synthesis to write
play-by-play and color commentary. Can be invoked post-hoc on an existing
deliberation output.

**Test**: Can the winner dispatch a "second pass" agent that reads prior
round outputs from disk and writes narrative to a new file, with access
to the same provider registry as the original deliberation?

**Pass criteria**: Commentator agents must be plain `ExecutionProvider`
invocations, not a special case. If spec 046 needs a new code path,
something is wrong with the winner's abstraction.

### 1.5 Specs 043/044 — AMPL Game-Theoretic Solvers (paid tier)

AMPL agents shell out to external solvers (AMPL, Knitro, Gurobi). They're
paid-tier and optional.

**Test**: Does the winner allow an agent to invoke an external solver
without forcing every deliberation to pay that cost? I.e., can AMPL-using
agents be provider instances that are only registered when the paid tier
is installed?

**Pass criteria**: `pip install conversus` (free tier) must work without
AMPL. `pip install conversus-solvers` must make AMPL providers available
without touching free-tier code.

### 1.6 Spec 020 — Scenario Storage (feature extraction)

Scenarios aggregate deliberation metadata across runs for cross-run queries.

**Test**: Does the winner surface enough metadata (per-agent start/end
timestamps, costs, identities, phase transitions) to populate a scenario
store? Can downstream queries like "show all deliberations where an agent
claimed a <1-week deadline" (spec 047) be answered?

**Pass criteria**: Metadata must be first-class fields on the
`ExecutionResult`, not buried in free-form log output.

### 1.7 Spec 047 — Structured Duration Parser

Less directly dependent, but feature extraction needs structured timing
data. The winner must expose per-agent wall-clock duration as a
`Duration` (not just seconds-as-float) so downstream temporal queries
compose.

**Pass criteria**: `ExecutionResult.duration` is a `Duration` or convertible
to one with zero loss of precision.

---

## 2. Free/Paid tier compatibility (spec 033)

The provider layer is free-tier infrastructure. Spec 033 partitioned
conversus into "deliberation is free, scoring is paid." The winner must
preserve that partition.

### 2.1 Free-tier install test

**Test**: In a clean venv, `pip install conversus` (no paid extras).
Create a minimal `conversus.yml` with 2 agents. Run it using only:
- The `mock` provider (for one agent)
- The `claude-code` provider (for the other — assume `claude` CLI installed)

**Pass criteria**: The run completes without any `pip install conversus-*`
beyond the base package. No import errors. No "paid tier required" errors.

### 2.2 Paid-tier layered install test

**Test**: Install `conversus-solvers` on top of free tier. Verify the
free-tier deliberation from §2.1 still runs identically. Then verify the
paid tier adds AMPL providers to the registry without modifying free-tier
code paths.

**Pass criteria**: Layered install. No version conflicts. No duplication
of provider classes. Uninstalling paid tier reverts to free-tier behavior.

### 2.3 API-key-less free-tier user

**Test**: A free-tier user with no API keys — only Claude Code installed
locally — can run a deliberation. (This is the "pip install conversus
and it just works if you already use Claude Code" user story.)

**Pass criteria**: The `claude-code` provider must not require environment
variables or API keys. It shells out to the locally-installed `claude`
binary which handles auth itself. If this is false, the free tier has
friction for the most common user.

---

## 3. Infrastructure stress tests

### 3.1 Concurrency

Deliberation phases launch N agents in parallel. Cross-reviews can be up
to 12 (for 4 agents × 3 peers). Phase 4 disputes can match.

**Test**: Launch 12 agents in a single phase. Measure wall-clock time
for phase completion. Verify no serialization.

**Pass criteria**: Phase wall-clock ≈ max agent wall-clock + small
overhead. Not sum of agent wall-clocks. Linear scaling confirmation.

### 3.2 Cost telemetry

Spec 033 paid tier may meter by cost. Commentator agents reference cost
in narration. Command Center displays it.

**Test**: Run a deliberation with a provider that returns cost metadata
(Anthropic, OpenAI). Verify per-agent cost is captured in the
`ExecutionResult` and aggregated at the phase and run level.

**Pass criteria**: Per-agent cost, per-phase cost, per-run cost all
queryable from structured output. Missing data is represented as `None`,
not silently zero.

### 3.3 Failure taxonomy

The arbiter needs to reason about failure modes. "Something went wrong"
is not enough.

**Test**: Simulate each of these and verify the `ExecutionResult.error`
category is correct:
- Provider auth failure (401)
- Provider rate limit (429)
- Provider server error (5xx)
- Subprocess timeout
- Subprocess non-zero exit
- Network unreachable
- Provider returned malformed output

**Pass criteria**: Each failure maps to a distinct `ProviderError.category`
(`auth`, `rate_limit`, `server`, `timeout`, `subprocess`, `network`,
`malformed`, `unknown`). The existing `Literal` type added to spec 045
must be expanded.

### 3.4 Secrets handling

API keys must not leak.

**Test**: Audit the path from `conversus.yml` → provider subprocess.
Verify:
- Keys are not written to argv (visible in `ps`)
- Keys are not logged at info level
- Keys are not included in `ExecutionResult` for downstream storage
- Keys can be passed via env var vs. explicit file vs. keyring

**Pass criteria**: Each provider documents its secret intake method.
None of them put secrets in argv.

### 3.5 MCP tool-use inside an agent

**Critical distinction**: MCP is tools (filesystem, fetch, etc.), not
dispatch. An agent running inside conversus may need to USE MCP tools
during its execution. This must be preserved.

**Test**: Configure a `claude-code` provider with an MCP server in its
`.mcp.json`. Verify the agent can use MCP tools during its deliberation
phase.

**Pass criteria**: MCP tool-use works without conversus-side plumbing.
The winner's abstraction does not accidentally break MCP.

### 3.6 Graceful cancellation

Command Center needs a cancel button. CI needs to kill long-running
deliberations.

**Test**: Launch a deliberation. Send SIGTERM mid-phase. Verify:
- All in-flight subprocesses receive the signal
- Partial output is preserved on disk
- No orphaned subprocesses remain

**Pass criteria**: Clean shutdown. `ps` shows no lingering `claude` or
`aider` processes after SIGTERM.

---

## 4. Meta-tests (replay conversus against itself)

These are the highest-signal tests because they're live workloads that
already work today.

### 4.1 Replay spec 042 deliberation through the winner

**Test**: Run the spec 042 deliberation (this one) through the winning
architecture. Same 4 agents, same 2 rounds, same binding arbiter. Verify
outputs are structurally identical to the current run.

**Pass criteria**: Same phase structure, same artifact paths, same
agent identities. Differences in LLM output are expected; differences
in orchestration are not.

### 4.2 Replay spec 045 test coverage deliberation

**Test**: Simpler 5-agent deliberation that converged in Round 1. Run
through the winner. Faster smoke test than §4.1.

**Pass criteria**: Full deliberation completes, converges in Round 1,
produces synthesis output.

### 4.3 Replay spec 031 55-agent review (scale test)

**Test**: The docs site review used 55 domain-specialist agents. Run
a subset (say 10-20) through the winner. Stress test for concurrency,
cost tracking at scale, and subprocess pool behavior.

**Pass criteria**: No deadlocks, no hangs, costs correctly aggregated
across all agents, subprocess cold-start is amortized (not 55 × 2s of
setup cost).

---

## 5. Ground-truth constraints (from backbone-researcher)

These are non-negotiable facts from Phase 1 research. The winner must not
silently contradict them.

### 5.1 Claude Agent SDK is a subprocess wrapper

**Constraint**: The `claude-code` provider MUST use subprocess of the
`claude` CLI binary, either directly or via `claude-agent-sdk` (which is
itself a subprocess wrapper). The winner must not pretend there is a
non-subprocess path.

### 5.2 A2A coding-agent ecosystem is empty (as of 2026-04)

**Constraint**: If the winner promises an `a2a` provider for v1, it must
name the specific A2A server counterparty. If there is no counterparty,
the provider can only serve an A2A server that conversus itself authors.
"A2A provider" in the v1 set without a named counterparty is a false
promise.

### 5.3 MCP is tools, not dispatch

**Constraint**: The winner's execution provider protocol must not conflate
MCP with agent dispatch. Agents USE MCP tools during execution; the
provider layer DOES NOT USE MCP to dispatch to other agents.

### 5.4 No unifying library exists

**Constraint**: No existing library handles both agent runtimes (Claude
Code, Aider, OpenCode) AND model APIs (Anthropic, OpenAI) under one
abstraction. The protocol must be conversus-owned. (All three advocates
agreed on this in Phase 2.)

### 5.5 Cold start is real and un-amortized

**Constraint**: Subprocess cold start (1-3s per invocation) × N agents
per phase is a real cost. The winner must either document the cost
explicitly or expose a pooling hook (`supports_pooling` flag, process
pool, or similar) for future optimization.

---

## 6. Arbiter instructions

In the Phase 6 ruling, the arbiter must:

1. **List each test above**
2. For each, state: **PASS**, **FAIL**, or **N/A** with one-sentence rationale
3. For any **FAIL**, state whether it's:
   - a blocker (winner must be rejected or the test must be deferred as a known gap)
   - a Phase 1-6 implementation requirement (winner acceptable if the plan addresses it)
   - an explicit trade-off (winner acceptable because the cost of passing exceeds the value)
4. Conclude with the final ruling and explicit acknowledgment of which tests
   were not addressed

The arbiter is conversus-chief-architect, with influence=binding. The ruling
is the definitive architectural decision for spec 042 and blocks/unblocks
specs 040, 043, 044, 046, 048.

---

## 7. Pass threshold

The winning architecture is **accepted** if:

- Zero blockers in §1 (downstream spec compatibility)
- Zero blockers in §2 (free/paid tier)
- All §5 ground-truth constraints respected
- At most 2 "Phase 1-6 implementation requirement" items (tests that pass
  once the implementation is complete but don't yet)
- The arbiter explicitly addresses every test

The winning architecture is **rejected or referred back** if:

- Any §5 ground-truth constraint is contradicted
- Any §1 hard dependency (048) cannot be satisfied
- The arbiter skips tests or refuses to rule on them

---

## 8. What this document is not

- **Not a replacement for the deliberation.** The advocates make the case;
  the arbiter rules; this document tests the ruling.
- **Not an implementation plan.** Spec 042 §4-6 is the implementation plan;
  this is the acceptance criteria for the architectural shape.
- **Not exhaustive.** Additional tests can be added before Phase 6 if the
  deliberation surfaces new concerns. Additions must be written here, not
  improvised in the arbiter's ruling.
