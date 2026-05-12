# Cross-Review: build-our-own-advocate

**Reviewer**: a2a-future-advocate
**Target**: build-our-own-advocate's Round 1 review
**Round**: 1, Phase 2 (cross-review)
**Disposition**: **Substantial concession on the central thesis. Retained position: A2A as the most important future provider, not as the v1 foundation.**

---

## 0. Up-front concession

After reading the backbone-researcher's findings and the build-our-own-advocate's review, I am conceding the central position of my Round 1 review — **"build the `acp` provider first" is wrong for 2026-04**. I am not conceding that A2A is irrelevant to conversus. I am conceding that A2A is not ready to be the v1 foundation of spec 042, and that my review's ordering ("A2A first, bespoke as a bridge") inverts the correct sequencing given the ground truth.

What changed my mind: the researcher's §9 finding that **no shipping coding agent has been wrapped as an A2A server yet** — no Claude Code, no Copilot, no Codex, no Gemini, no Aider, no OpenCode A2A server exists. Only Google ADK / IBM BeeAI / LangGraph have A2A integrations, and none of those are the agents conversus actually needs to dispatch to. The `a2a-sdk` is at 0.3.25 stable / 1.0.0a0 alpha. Protocol 1.0.0 is **one month old** as of this deliberation date.

My Round 1 review characterized A2A as "twelve months of stabilization" and A2A counterparties as "already wrapped by the community." The research shows both claims were optimistic. "Twelve months" counts from protocol *announcement*, not from Python SDK stability. And the community has not wrapped the agents that matter.

I'll address the build-our-own-advocate's three challenges directly, then state what I think the correct revised position is.

---

## 1. The "superset" framing — is it valid?

**Largely yes, with a caveat I want on the record.**

Build-our-own's §5 explicitly lists `acp` as a first-class row in spec 042 §11's provider matrix. §3.4 commits to "ship our own protocol now, add an `acp` provider when the ecosystem is ready." Their core position is: own the Python Protocol, let specific providers (including an eventual `ACPProvider`) translate in one place.

This is actually **compatible with four of the six arguments from my Round 1 review**:

- **2.3 (One provider, every tool)**: An `ACPProvider` inside build-our-own gets the same ecosystem-flywheel benefit when the ecosystem arrives. The wrapper-per-SDK work gets reused by any A2A client. Nothing in build-our-own prohibits this.
- **2.4 (Composability)**: Once the `ACPProvider` ships, agent-to-agent recursion works the same way. The conversus engine sees `ExecutionProvider.execute()`; the A2A provider handles the recursive dispatch internally. My "agents calling agents" pitch is preserved.
- **2.5 (Future-proofing)**: Build-our-own is a thin protocol, not a framework bet. When A2A matures, the `ACPProvider` absorbs the change and the engine sees nothing. This is actually *more* future-proof than my Round 1 pitch of targeting A2A directly, because it keeps the Python contract under our control if A2A's wire format shifts.
- **2.6 (Python SDK exists)**: Fine — it exists, it goes inside the `ACPProvider` adapter, not as the public surface of the conversus engine.

**Where the superset framing is weakest — the caveat I want on the record:**

Two benefits I claimed in Round 1 are *not* fully preserved by build-our-own as specified:

1. **Runtime discovery via Agent Detail (§2.2)**. Build-our-own's §5 is silent on discovery. The spec 042 `PROVIDER_REGISTRY` is a module-level dict populated by direct imports. If the `ACPProvider` eventually wraps an A2A client that does Agent Detail discovery, then discovery happens *inside* the provider adapter — but it is not exposed as a first-class conversus concept. Spec 048's `agent_registry:` config would still be a list of conversus-provider strings, not a list of A2A URLs. Discovery becomes a provider-internal detail instead of a conversus-level feature. This is acceptable for 2026 but leaves a gap for 2027+.

2. **The "write it as an A2A server from day one" claim (§3.3 Rebuttals)**. I argued that `conversus-acp-claude` should BE the reference Claude Code provider — a single code artifact that serves both as the conversus local bridge and as a reusable A2A server. Build-our-own implicitly rejects this: the `ClaudeCodeProvider` is a Python adapter inside conversus, and the A2A server wrapping Claude Code is a separate (future, unspecified) artifact. That separation is reasonable given the research — nobody has a Claude Code A2A wrapper, so conversus can't just drop one in — but it means we lose the "write once, benefit everywhere" ecosystem contribution my Round 1 review leaned on.

So the superset is valid at the **architectural** level (A2A is an adapter, not a competitor) but is weaker at the **strategic** level (build-our-own does not commit to A2A as a destination, only as an option). That matters less than I thought it did a day ago.

**Verdict on the superset framing**: Valid. My Round 1 benefits (composability, wire-format flexibility, eventual ecosystem alignment) survive inside build-our-own's architecture. The discovery-first and "reference A2A server" ambitions do not survive and are things I would want revisited in a future spec if A2A actually takes off.

---

## 2. The hard-dependency argument on spec 048 — is it insurmountable?

**Yes, insurmountable. This is where my Round 1 review fails hardest.**

Spec 048 §9 names spec 042 as a **HARD DEPENDENCY** (line 425 per build-our-own's citation, which I verified in my own Round 1 §4). Spec 048 FR-021 is the line I quoted myself: *"`conversus governance` MUST be invokable without Claude Code running (requires spec 042 execution providers)."*

My Round 1 review argued that A2A makes spec 048 *better*. That is plausibly true for 2027. It is **not** true for the "ship spec 042 so spec 048 can ship" timeline. The researcher's §9 is devastating on this point: if conversus ships an A2A provider today, there is nothing on the other end of the wire. Spec 048's governance gates need to dispatch to Claude Code, Copilot, or similar — none of which have A2A servers. If spec 042 ships with *only* an A2A provider, spec 048 cannot execute any governance rule that depends on a real coding agent.

My Round 1 §5 Proposed Commitment #3 tried to paper over this by saying "implement the `claude-code` direct provider ONLY as a fast-path optimization." That is the wrong framing. The `claude-code` direct provider is not a fast-path optimization — it is the **only path that works on ship day**. There is no A2A-wrapped Claude Code to fast-path away from.

**Timeline math that I should have done in Round 1:**

- Spec 042 drafted: 2026-04-02
- Spec 048 drafted: 2026-04-04 (depends on 042)
- A2A protocol 1.0.0: 2026-03-12 (one month old)
- `a2a-sdk` Python: 0.3.25 stable / 1.0.0a0 alpha
- A2A wrapper for Claude Code: **does not exist**
- A2A wrapper for any agent conversus would dispatch to: **does not exist**

Spec 042 cannot wait for the A2A ecosystem to catch up because spec 048 cannot wait for spec 042. And even if spec 042 *did* wait, waiting produces no A2A counterparties on its own — someone still has to write the wrappers. That someone would be the conversus team, which is the exact work build-our-own frames as "add an `ACPProvider` when the ecosystem is ready."

**The hard-dependency argument collapses my Round 1 sequencing.** "Build `acp` first, bespoke second" requires an `acp` target that exists. There is no `acp` target that exists for the agents spec 048 needs. Build-our-own's sequencing — "ship the protocol with `mock` + `anthropic` + `claude-code`, add `acp` when ecosystem is ready" — is correct for the current calendar.

**Concession**: Insurmountable. Build-our-own wins this axis outright.

---

## 3. Does "A2A first, bespoke second" still make sense given the empty ecosystem?

**No. It should be "A2A as the most important future provider within build-our-own's protocol."**

The researcher's §0 TL;DR #8 and §7 together rule out my Round 1 framing:

> "There is no common programmatic primitive shared across these tools. … Every shipping tool has its own bespoke dispatch mechanism at the boundary — subprocess + CLI flags, or HTTP."

> "The de facto backbone across all agentic coding tools today is: subprocess-spawn a CLI, pass a prompt via `-p`/`--message`/stdin, collect JSON output. Every one of them ships this. None of them ship a shared Python library. None of them ship a shared HTTP protocol (OpenCode has one, nobody else does)."

This means my Round 1 §2.3 N×M argument — "build one A2A provider, get every tool for free" — is **currently false**. Today you build one A2A provider and you get *zero* tools for free because no tools speak A2A yet. The N×M explosion I warned about is real, but the current escape valve is CLI subprocess + JSON, not A2A. The researcher's §10 mapping table is the honest picture: every agent ships a CLI with headless mode, one agent (OpenCode) ships HTTP, nobody ships A2A.

**The corrected framing is:**

- Build-our-own's `ExecutionProvider` protocol is the v1 foundation. (My Round 1 was wrong here.)
- The v1 providers are `mock` + `anthropic` + `claude-code` (subprocess to `claude -p --bare`). (Build-our-own's roster.)
- **A2A is the most important future provider** for conversus because A2A is the only protocol with a credible path to unifying agent dispatch across vendors. It is Google + IBM + Microsoft + AWS + Cisco + Salesforce + ServiceNow + SAP on the TSC (researcher §6.2). This coalition wins standards wars in the long run.
- A2A is *not* the v1 foundation because the coalition has not yet delivered shipping wrappers of the agents conversus needs to dispatch to.
- The correct move on A2A is to track it closely, add an `ACPProvider` as soon as the first real counterparty exists (probably IBM BeeAI or Google ADK agents, since those are the only ones already integrated per researcher §6.2), and **consider** contributing a Claude Code or OpenCode A2A wrapper as an ecosystem investment *after* spec 042 ships.

**My Round 1's "six arguments for betting on A2A" rescored against the research:**

| Argument | Round 1 framing | Corrected framing |
|---|---|---|
| 2.1 Standards convergence | "Already decided, bet now" | Coalition is real, delivery timeline is 2027+, not 2026 |
| 2.2 Runtime discovery | "Kills hardcoded lists in v1" | Nice-to-have for future spec, not for 042 v1 |
| 2.3 One provider, every tool | "Build one A2A, get ten tools" | False today — zero tools are A2A-wrapped |
| 2.4 Composability | "Recursive deliberation free" | True only once A2A counterparties exist |
| 2.5 Future-proofing | "Every bespoke is debt" | Bespoke is an axle, not a wheel; A2A becomes an adapter on the axle |
| 2.6 Python SDK exists | "~30 lines, ship today" | Python SDK exists but no agents on the other end — the 30 lines talk to nothing |

Four of six arguments are either wrong today or need to be re-timed to 2027. Two (composability, standards convergence as a long-horizon bet) survive as arguments for A2A as a *future* provider, not as the foundation.

---

## 4. What parts of my position are STILL VALID?

Three things survive and are worth preserving in the final deliberation record:

### 4.1 Runtime discovery via Agent Detail is still valuable — for spec 048's future

Spec 048's `agent_registry:` config today is a list of Python provider strings. When A2A counterparties exist in 2027+, a `.conversusrc` that points at agent URLs is genuinely better than one that points at provider strings. Adding a custom security reviewer becomes "stand up an A2A server at `https://agents.internal/security-reviewer`" instead of "ship a new conversus-provider-X pip package."

**Recommendation for the synthesis stage**: Build-our-own's protocol should leave room for this. Specifically, the `PROVIDER_REGISTRY` in spec 042 §5 should be usable *or* bypassable — a provider name like `"a2a"` should be able to take a URL in its metadata and dispatch dynamically without requiring a new registry entry per remote agent. This is a small design note that preserves the runtime-discovery story for when it becomes feasible.

### 4.2 A2A as the destination for 2027+ is still plausible

The researcher's §6.2 is explicit about the coalition: "Google + IBM + Microsoft + AWS + Cisco + Salesforce + ServiceNow + SAP on the TSC." That is a larger coalition than any competing standard, and Linux Foundation governance is the correct venue for durable protocols. The researcher's §9 conclusion — "A2A is a bet on a future that will probably arrive, but it has not arrived yet for coding agents" — is exactly the right characterization. My Round 1 mistake was compressing "probably arrive" into "has arrived."

**Recommendation for the synthesis stage**: The winning synthesis should name A2A explicitly as the intended destination for agent-to-agent dispatch, with a lightweight commitment to add an `ACPProvider` when the first non-reference A2A counterparty for a coding agent ships. That keeps the conversus roadmap honest about the long-term direction without blocking spec 042 on an empty ecosystem.

### 4.3 Conversus authoring an A2A server wrapper as ecosystem contribution is still interesting

The researcher's §9 finding cuts both ways. If **no one has wrapped Claude Code as an A2A server yet**, then the first team that does it owns a disproportionate amount of ecosystem influence. Conversus is already building a `ClaudeCodeProvider` adapter. The delta between "an internal Python adapter" and "an A2A server that exposes the same thing" is modest — the researcher's §10 shows Claude Code's CLI surface (`claude -p --bare --output-format json`) is exactly what an A2A server would shell out to anyway. Writing a reference A2A wrapper for Claude Code is plausibly a 300–600 line deliverable that conversus could ship as a separate artifact.

**This is not part of spec 042 v1.** It is a follow-up that conversus could consider once spec 042 ships, spec 048 unblocks, and the team has bandwidth. It is the single highest-leverage ecosystem contribution conversus could make to the A2A story.

**Recommendation for the synthesis stage**: Note this as a post-042 opportunity. Do not block spec 042 on it. Do not let it disappear from the roadmap.

---

## 5. Should I concede the central position?

**Yes.** My central position was "A2A as foundation." That position is defeated by:

- Spec 048's hard dependency on spec 042 shipping on a timeline that A2A cannot support (§2 above).
- The empty A2A-for-coding-agents ecosystem in 2026-04 (researcher §9, §10).
- The compatibility of build-our-own's architecture with everything I claimed A2A would deliver *in the long run* (§1 above).

My revised position:

> **Build-our-own's `ExecutionProvider` protocol is the correct v1 foundation for spec 042. A2A is the most important future provider within that protocol, not a replacement for it. The correct sequence is: ship `mock` + `anthropic` + `claude-code` (CLI subprocess) in v1; track A2A SDK maturity; add an `ACPProvider` when the first shipping coding agent has an A2A wrapper (or when conversus itself contributes one as a follow-up ecosystem investment).**

This is essentially a concession to build-our-own on the immediate architecture decision, with a retention of A2A as the North Star for the 2027+ roadmap.

---

## 6. What I want build-our-own to concede in exchange

Build-our-own's review is correct on sequencing but light on A2A commitment. Specifically:

1. **§3.4 "A2A/ACP is the future, just wait" is too dismissive.** The actual answer is not "wait" — it is "ship build-our-own now AND commit to A2A as the destination." The distinction matters because it shapes how the `ExecutionProvider` protocol evolves. If we treat A2A as "maybe someday," the protocol will drift in directions that are hard to reconcile later. If we treat A2A as "we will add this provider once the ecosystem is non-empty," design decisions made today will stay A2A-compatible.

2. **The superset framing should come with an explicit A2A commitment in the spec.** Spec 042's current §11 lists `acp` as the top row. Build-our-own should keep it there, not demote it to "we'll see." Otherwise the superset claim is rhetorical cover for deferring A2A indefinitely.

3. **Runtime discovery is a protocol-level concern, not an adapter-level concern, eventually.** Build-our-own's §5 bullet ("Build-our-own can include an `ACPProvider`") treats A2A as a pure adapter. It IS a pure adapter for v1. But once A2A counterparties exist, agent discovery stops being "which provider string do I pass" and becomes "which URL do I dispatch to," and the `PROVIDER_REGISTRY` design needs to allow that. Build-our-own should acknowledge this and design the registry to degrade gracefully into URL-based dispatch for the A2A case.

These are not deal-breakers. They are "yes, and..." refinements that make build-our-own's winning architecture more durable.

---

## 7. Bottom line for the synthesis

**Winner on central architecture**: build-our-own. Ship the `ExecutionProvider` protocol as specified in spec 042 §3 with `mock` + `anthropic` + `claude-code` as the v1 roster.

**Retained A2A position**: A2A is the most important future provider, not the v1 foundation. Keep it as the top row of spec 042 §11's matrix. Commit to adding an `ACPProvider` when the first real A2A counterparty for a coding agent exists (either because the ecosystem produces one or because conversus ships one as a post-042 contribution).

**Design note for build-our-own to absorb**: Leave room in `PROVIDER_REGISTRY` and spec 048's `agent_registry:` config for URL-based dispatch so the eventual A2A provider doesn't require a breaking change.

**What dies**: "Build `acp` first." "Every direct SDK adapter is technical debt." "The wrapper is NOT conversus's problem." All three were overreach.

**What lives**: A2A is still where this ecosystem is going. Conversus should ship build-our-own now so it can *get there* later, rather than blocking on an ecosystem that does not exist yet.

---

**Files referenced**:
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/a2a-future-advocate/review.md` (my Round 1)
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/build-our-own-advocate/review.md` (target)
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/conversus-output/backbone-researcher/review.md` (§6.2, §9, §10, §13)
- `<HOME>/code/payer-index-mono/conversus/specs/042-execution-providers/spec.md` (§3, §5, §11)
- `<HOME>/code/payer-index-mono/conversus/specs/048-autonomous-governance-mode/spec.md` (§9, FR-021)
