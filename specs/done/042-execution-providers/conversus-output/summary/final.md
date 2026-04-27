# Verdict — Spec 042 Execution Provider Architecture

**Phase**: 5 (Judge's binding verdict)
**Date**: 2026-04-05
**Mode**: Winner-take-all
**Judge**: Neutral synthesis agent

---

## Judging Criteria

Derived from `specs/042-execution-providers/spec.md`, `specs/042-execution-providers/validation.md`, and `specs/048-autonomous-governance-mode/spec.md` — NOT from what the advocates argued about. The competitors tended to frame criteria around LoC counts, "who wrote the protocol," and adapter redundancy; the target documents themselves weight things differently.

### 1. Unblocks spec 048 on the only calendar that exists — **Critical**
- **Weight justification**: Spec 048 §9 lists spec 042 as a HARD DEPENDENCY ("Spec 042 dependency: Autonomous mode REQUIRES execution providers (headless execution). Cannot ship before 042."). Validation battery §1.1 is the first test and §7 states the winner is "rejected or referred back if any §1 hard dependency (048) cannot be satisfied." This is the single highest-stakes test in the validation document.
- **Source**: `spec 048 §9`, `validation.md §1.1`, `validation.md §7`.

### 2. Passes the §5 ground-truth constraints from validation.md — **Critical**
- **Weight justification**: `validation.md §7` states explicitly: *"The winning architecture is rejected or referred back if any §5 ground-truth constraint is contradicted."* §5 enumerates five non-negotiables: (5.1) Claude Agent SDK is a subprocess wrapper, (5.2) A2A coding-agent ecosystem is empty, (5.3) MCP is tools not dispatch, (5.4) no unifying library exists, (5.5) cold start is real. A ruling that violates any of these is automatically vulnerable to rejection.
- **Source**: `validation.md §5`, `validation.md §7`.

### 3. Exercises the full substrate matrix in v1 (validation replay) — **High**
- **Weight justification**: Validation battery §4.1/§4.2/§4.3 require replaying the spec 042 deliberation, the spec 045 deliberation, and the spec 031 55-agent review through the winner. §3.1 requires concurrency testing at 12 agents in parallel. The winner's v1 scope must exercise every important axis (no-tool-use Tier-3, tool-use subprocess, and ideally an HTTP transport for cold-start mitigation) or the replay tests cannot validate the architecture against downstream specs 040/043/044/046/048.
- **Source**: `validation.md §3.1`, `validation.md §4.1`, `validation.md §4.2`, `validation.md §4.3`.

### 4. Free-tier friction & API-key-less user (spec 033 partition) — **High**
- **Weight justification**: `validation.md §2.3` names this as an explicit pass criterion: *"A free-tier user with no API keys — only Claude Code installed locally — can run a deliberation."* Spec 048 §12 (phasing) and spec 042 §10 (Constraints) require the `claude-code` provider to be a core reference implementation and `mock` to ship with core. The validation document flags that failure here means "the free tier has friction for the most common user."
- **Source**: `validation.md §2.1–§2.3`, `spec 042 §10`, `spec 048 Phase 1-6 phasing`.

### 5. Spec 048 runtime agent discovery / URL-addressable registry — **High**
- **Weight justification**: `validation.md §1.2` is explicit: *"The config schema must not forbid URL entries. An error saying 'URL-addressable agents not yet supported in v1' is acceptable; a schema that rejects the field outright is not, because it would require a migration to add later."* This is a downstream-compatibility constraint that the arbiter must test. Spec 048 §10 Q4 (multi-repo governance) and §11 (seven execution surfaces) depend on this.
- **Source**: `validation.md §1.2`, `spec 048 §10 Q4`, `spec 048 §10 Q8`, `spec 048 §11`.

### 6. Forward compatibility with A2A when ecosystem matures — **Medium**
- **Weight justification**: Spec 042 §2 maps conversus phase dispatch 1:1 to A2A Task Request semantics. Spec 042 §11 lists `acp` (now `a2a`) as "Priority — universal provider." The winning architecture should be able to absorb A2A as an additive provider without protocol breaking changes. `validation.md §5.2` makes A2A v1 deferral acceptable, but the protocol shape must not foreclose future A2A adoption. This is Medium (not High) because the empty ecosystem finding means A2A is a 2027+ concern, and the risk is manageable with a Week-1 design note.
- **Source**: `spec 042 §2`, `spec 042 §11`, `spec 042 §12 Q6`, `validation.md §5.2`.

### 7. Simplicity / maintenance discipline / v1 scope hygiene — **Medium**
- **Weight justification**: Spec 042 §10 Constraints: *"Provider implementations are optional packages — only `mock` ships with core `conversus`."* The winner must respect the free-tier/paid-tier partition from spec 033 (validation §2) and must not bloat core. Ongoing maintenance (per-SDK price tables, retry curves, rate-limit headers) is a real operational cost that scales with the number of hand-rolled direct-API adapters. This is Medium because every surviving Phase 3 plan satisfies the hygiene requirements; the discipline criterion differentiates on the margin.
- **Source**: `spec 042 §10`, `spec 042 §11`, `validation.md §2`.

---

## Per-Agent Scorecard

### backbone-researcher

**Scoring note**: The backbone-researcher is a factual witness, not an architectural competitor. Their "position" is a set of ground-truth findings that constrain the decision space, not a proposed architecture. Per the judge instructions, I score them **N/A — factual witness, not an architectural competitor**. Their findings are treated as settled inputs that every other advocate was required to respect. A summary of their role:

**Opening Position**: "These are the factual constraints every winning architecture must respect: no unifying library exists, subprocess-CLI-JSON is the de facto backbone, `claude-agent-sdk` is itself a subprocess wrapper, A2A coding-agent ecosystem is empty in 2026-04, MCP is tools not dispatch, two different protocols share the 'ACP' name, cold start is ~1–3s per invocation."

**Attacks Received**: Not an advocate; no architectural attacks landed. Minor factual corrections (A2A merger month: August not September) accepted cleanly. LoC estimate for subprocess adapters refactored into base-class factoring by build-our-own advocate — researcher accepted the refactoring as "architecturally superior."

**Attacks Delivered (as factual observations)**: Eight of nine factual claims were independently ratified by at least two of the three advocates during cross-review. The empty A2A coding-agent ecosystem finding forced a2a-future-advocate to fully pivot their Round 1 position. The `claude-agent-sdk` subprocess-wrapper finding eliminated the "Node bridge" phantom option from every advocate's v1 plan. The two-ACP finding moved from "minor nit" to "mandatory spec fix" and was universally adopted.

**Credibility Assessment**: Exemplary. Conceded scope limits (did not audit the conversus test suite, LiteLLM release cadence, or Copilot CLI headless surface) cleanly. Self-flagged gaps in Phase 1 that later became relevant. Non-advocating posture held through all four phases. Their disputes.md explicitly declines to pick a winner and says *"all three revised positions are consistent with the factual landscape."* This is the correct posture for a factual witness and it was honored.

**Verdict on the factual witness**: All seven of my judging criteria treat the backbone-researcher's findings as **joint-ratified constraints** on the decision. The three advocates are scored on fidelity to these constraints. The researcher is not a candidate for winner because they are not advocating for an architecture.

---

### build-our-own-advocate

**Opening Position** (Phase 1): "Conversus should define and ship its own minimal `ExecutionProvider` Protocol (spec 042 §3) unchanged, with `mock` + `anthropic` + `claude-code` as the v1 provider set. External SDKs live at the adapter layer, never at the protocol layer. LiteLLM and A2A are additive downstream adapters, not foundations."

**Evolved Position** (Phase 3/4): Four providers in v1 (`mock` + `anthropic` + `claude-code` via direct `claude -p --bare` + `opencode` via `HTTPProvider`), with `SubprocessProvider` and `HTTPProvider` base classes absorbing the common substrate. `LiteLLMProvider` ships as an optional companion package in v1. Absorbed a2a-future's protocol-shape amendment, `register_provider_instance()` runtime hook, and the `conversus-a2a-claude` post-v1 standalone pioneer artifact.

**Attacks Received**:
- **"100–200 LoC per adapter is ~2x low for `claude-code`"** (backbone researcher §2.3) — **Conceded and absorbed**. Factored the substrate into `SubprocessProvider` base class, raised total v1 estimate to ~1,400–1,500 LoC. Researcher accepted the refactoring as architecturally superior.
- **"`claude-code` is not zero-dep; `claude-agent-sdk` path is misleading"** (backbone §4.1) — **Conceded**. Dropped `claude-agent-sdk` from v1 plan entirely; went direct to `claude -p --bare`. This concession strengthened the plan.
- **"The single `acp` row conflates two protocols"** (backbone §3.2) — **Conceded**. Renames to `a2a` and adds separate `zed-acp` row. Researcher's own cross-review noted this correction actually *strengthens* build-our-own because owning the protocol is what lets you have two rows for two wire protocols.
- **"`LiteLLMProvider` belongs in v1"** (litellm-hybrid §5) — **Absorbed**. `LiteLLMProvider` ships in v1 as optional companion package. This collapsed the architectural disagreement with litellm-hybrid to a single adapter file.
- **"You did not address cold-start economics"** (backbone §4.3) — **Rebutted via plan amendment**. Moved `opencode` into v1 specifically to validate the HTTP substrate and provide a cold-start-free option.
- **"Protocol shape is a one-way door"** (a2a-future Phase 3 §1) — **Rebutted via absorption**. Accepted the A2A-Task-Request-semantic design note as Week 1 deliverable at ~4 hours of cost.
- **"v1 has redundant `anthropic` + `litellm` coverage"** (litellm-hybrid Phase 3/4) — **Defended but weakly**. Build-our-own's defense rests on three arguments: resilience (LiteLLM-free fallback), validation coverage (exercise direct-SDK path), and superset posture (contain everyone's best ideas). Each is defensible but none is overwhelming; litellm-hybrid's rebuttal that "`LiteLLMProvider.supports_tool_use=False` exercises the same engine path" is technically correct.

**Attacks Delivered**:
- **"The 3-of-12 framing undercounts LiteLLM"** — Conceded to litellm-hybrid's rebuttal; adopted the ~25/75 ratio instead.
- **"No wheel exists; you're reinventing nothing"** — **Decisive**. Ratified by the researcher and conceded verbatim by both adversarial advocates. This is the load-bearing architectural claim.
- **"A2A-future conflates Zed/JetBrains ACP with Google/IBM A2A"** — **Decisive against a2a-future Round 1**. Forced a2a-future to concede their central position.
- **"The hybrid's 'splits the abstraction in half' frame collapses under subprocess collapse"** — Partially successful; contributed to litellm-hybrid dropping the "hybrid" label.

**Credibility Assessment**: **High**. Every weakness raised was either conceded cleanly or absorbed with a concrete plan amendment. The LoC correction was owned publicly. The Phase 3 revision is meaningfully different from Phase 1 (4 providers, 2 base classes, ~1,500 LoC honest estimate). The Phase 4 closing scorecard scores them Strong/Adequate honestly — no inflated self-scoring. Conceded the `mock` "3,428 tests" rhetoric as under-specified before being attacked on it.

**Criterion Scores**:

| Criterion | Score (1-5) | Justification |
|---|---|---|
| 1. Unblocks spec 048 on calendar | 5 | ~13–19 working days, zero ecosystem dependencies, subprocess-CLI works today, `ClaudeCodeProvider` gives SKILL.md backward compat. A2A-future explicitly conceded "build-our-own wins this axis outright." |
| 2. Respects §5 ground-truth constraints | 5 | Every §5 constraint respected. Subprocess wrapper (5.1) ✓, A2A ecosystem empty / deferred with trigger (5.2) ✓, MCP excluded from dispatch layer (5.3) ✓, no unifying library (5.4) ✓, cold start addressed via `OpenCodeProvider` HTTP path (5.5) ✓. |
| 3. Exercises full substrate matrix | 5 | Only plan that ships both `SubprocessProvider` AND `HTTPProvider` base classes validated in v1. `mock` validates Protocol, `anthropic` validates `supports_tool_use=False` + inline adaptation, `claude-code` validates subprocess substrate, `opencode` validates HTTP substrate + cold-start-free path. Literally the minimum set that validates every axis. |
| 4. Free-tier / API-key-less user | 5 | `claude-code` direct-CLI path requires no env vars, no API keys. `pip install conversus` + local Claude Code = it works. Native `anthropic` is the backup for users with API keys but no Claude Code. Zero LiteLLM dependency in the free-tier default path. |
| 5. Runtime agent discovery / URL registry | 4 | Absorbed `register_provider_instance()` runtime hook in the registry. Did NOT propagate the URL-accepting schema change into spec 048's `.conversusrc::default_agents` — a2a-future's third held claim. The registry supports it; the spec 048 schema would still need to be extended. Partial credit. |
| 6. Forward compat with A2A | 4 | Triggered roadmap commitment (3-of-6 counterparty condition). Explicitly commits to `conversus-a2a-claude` as post-v1 pioneer artifact. Accepts the Week 1 protocol-shape design note from a2a-future. Only loses a point because the A2A-shape docstring is "accepted" rather than specified verbatim in the revision. |
| 7. Simplicity / scope hygiene | 3 | The parallel `anthropic` + `litellm` v1 set is a defensible resilience call but is litellm-hybrid's strongest attack. Ships 4 providers where 3 would arguably validate the same axes. "Dead weight" charge has some merit on the narrow question of "which user installs both simultaneously." |

**Total Weighted Score**: Criterion 1 (Critical ×5 = 25), Criterion 2 (Critical ×5 = 25), Criterion 3 (High ×5 = 20), Criterion 4 (High ×5 = 20), Criterion 5 (High ×4 = 16), Criterion 6 (Medium ×4 = 12), Criterion 7 (Medium ×3 = 9) = **127/140**

---

### litellm-hybrid-advocate

**Opening Position** (Phase 1): "Spec 042 is ~30% agent-runtime and ~70% model-API. LiteLLM already solves the 70%. Build our own `ExecutionProvider` protocol but delegate Tier 3 to LiteLLM. Time-to-ship: 3 weeks."

**Evolved Position** (Phase 3/4): Retired the "hybrid" label entirely. Ship `mock` + `claude-code` + `litellm` as v1. Do NOT ship a parallel hand-rolled `anthropic` adapter. Architecture is 100% build-our-own's protocol. The single residual disagreement is one adapter file: include native `anthropic` alongside `LiteLLMProvider` (build-our-own's position) or not (litellm-hybrid's position).

**Attacks Received**:
- **"The 70/30 split is wrong; it's ~25/75 agent-runtime"** (backbone §1, build-our-own §1) — **Conceded**.
- **"144-cell surface area is ~6x overcounted"** (build-our-own §2) — **Conceded** to ~30–40 cells. Argued the operational argument is cell-count-invariant.
- **"Academic purism straw man was unfair"** (build-our-own §3) — **Conceded** fully in Phase 2. Retired the "hybrid is a different paradigm" framing.
- **"LiteLLM does not cover Claude Code workloads"** (backbone §2) — **Rebutted**. Distinguished Tier-1 agent-loop workloads (covered by `claude-code`) from Tier-3 direct-API workloads (covered by LiteLLM). The two coexist in the v1 plan.
- **"14-line adapter is happy-path only"** (backbone §4) — **Partially conceded**. Production-ready is ~80–120 lines and 2–4 engineer-days.
- **"LiteLLM is a single-vendor supply-chain risk"** (a2a-future Phase 1) — **Rebutted** by researcher's independent verification and a2a-future's own Phase 2 withdrawal.
- **"Protocol shape ossification risk"** (a2a-future Phase 3) — **Absorbed** at 4-hour design-note cost but not made binding.
- **"v1 without `HTTPProvider` leaves the HTTP substrate unvalidated"** (build-our-own Phase 4) — **Not rebutted**. This is a genuine gap. litellm-hybrid's v1 set has `mock` + `claude-code` + `litellm`; no `opencode`, no HTTP substrate validation.
- **"v1 without `anthropic` native leaves no API-key-based Tier-3 path without LiteLLM"** (build-our-own Phase 4) — **Rebutted weakly**. Litellm-hybrid's defense is "optional-package split provides the same isolation" — technically true, but it does not satisfy validation §2.3's "API-key-less free-tier user" scenario as cleanly as build-our-own's native `anthropic` option.

**Attacks Delivered**:
- **"LiteLLM proxy mode fronts subprocess tools (Aider, Continue `cn`, Codex via `OPENAI_BASE_URL`)"** — **UNCHALLENGED through 6 cross-reviews and 3 competitor revisions**. Litellm-hybrid flagged this explicitly in their closing argument as "silence is concession." I verified this by searching the artifacts: the claim appears in litellm-hybrid's cross-review of backbone §4.2 and is never engaged with by build-our-own or a2a-future in any subsequent document. Per the judge instructions, this attack stands uncontested. **However, it is not decisive** — the composition is theoretically sound but the backbone-researcher explicitly flagged in their Phase 3 risks section that "I did not verify the end-to-end composition" and rated it "interesting theoretical lever, not validated in practice."
- **"LiteLLM covers local/self-hosted runtimes (Ollama, VLLM, LMStudio, LocalAI)"** — Unchallenged. Valuable for spec 048's enterprise-VPC scenarios.
- **"v1 maintenance burden: twelve SDK upgrade cycles vs one LiteLLM upgrade cycle"** — Ratified verbatim by build-our-own's Phase 2 §5 concession.
- **"Build-our-own's `anthropic` + `litellm` is redundant"** — Partially landed but not decisive. Build-our-own's three-pronged defense (resilience, validation coverage, superset posture) is defensible.

**Credibility Assessment**: **High**. Conceded the framing error ("hybrid" retired in Phase 2) honestly and re-engineered their position. Self-identified the "academic purism" straw man. Phase 4 closing explicitly scopes the residual disagreement to one adapter file and does not inflate the win. The proxy-mode unchallenged claim is legitimately unchallenged (I verified). Self-scoring in closing is honest (marks themselves Adequate on several criteria rather than Strong everywhere).

**Criterion Scores**:

| Criterion | Score (1-5) | Justification |
|---|---|---|
| 1. Unblocks spec 048 on calendar | 5 | 3-week v1 minimal, 4–5 week SKILL.md parity. Essentially equal to build-our-own on this axis; both ship the same `SubprocessProvider` + `claude-code` machinery in the same timeframe. |
| 2. Respects §5 ground-truth constraints | 5 | Every §5 constraint respected after Phase 2 concessions. Subprocess (5.1) ✓, A2A deferred with trigger (5.2) ✓, MCP excluded (5.3) ✓, protocol is conversus code (5.4) ✓, cold start flagged (5.5) — though not mitigated by v1 deliverable. |
| 3. Exercises full substrate matrix | 3 | v1 is `mock` + `claude-code` + `litellm`. Ships `SubprocessProvider` but NOT `HTTPProvider`. `LiteLLMProvider` is a NativeProvider-style adapter that does not validate HTTP substrate. Leaves the HTTP transport unvalidated in v1. Significant gap on validation battery §3 and §4.1 replay tests. |
| 4. Free-tier / API-key-less user | 4 | `mock` + `claude-code` covers the named scenario. However, a free-tier user who wants direct-API access must install `conversus-provider-litellm`, which pulls in the LiteLLM dependency tree (FastAPI/Starlette transitively in some install paths). Higher dependency footprint than build-our-own's native `anthropic` option. |
| 5. Runtime agent discovery / URL registry | 2 | Phase 3 revision explicitly deferred this: *"Out of scope for v1 by spec definition."* a2a-future's validation battery §1.2 concern (URL entries must not be forbidden by schema) is not addressed. The lowest score among advocates on this criterion. |
| 6. Forward compat with A2A | 4 | Accepted the protocol-shape amendment as "4 hours of design notes" but explicitly noted "I will not make it a binding deliverable." Same triggered-commitment path as build-our-own otherwise. Loses a point relative to build-our-own because the docstring is "accepted but not binding." |
| 7. Simplicity / scope hygiene | 5 | Smallest v1 surface of any plan (3 providers, ~14–120 LoC for the LiteLLM adapter, zero redundant coverage). Strongest on this axis. The "one adapter less" argument is well-founded on narrow scope-hygiene grounds. |

**Total Weighted Score**: Criterion 1 (Critical ×5 = 25), Criterion 2 (Critical ×5 = 25), Criterion 3 (High ×3 = 12), Criterion 4 (High ×4 = 16), Criterion 5 (High ×2 = 8), Criterion 6 (Medium ×4 = 12), Criterion 7 (Medium ×5 = 15) = **113/140**

---

### a2a-future-advocate

**Opening Position** (Phase 1): "Conversus should bet on A2A as the canonical dispatch layer. Build the `acp` provider first. Every other adapter is technical debt. Ship `conversus-acp-claude` as reference A2A server wrapper."

**Evolved Position** (Phase 3/4): **Explicitly conceded the core position**. Round 1 is dead. Revised to three narrow claims: (1) design `ExecutionTask`/`ExecutionResult` field shape around A2A Task Request semantics in Week 1 as a design note; (2) author `conversus-a2a-claude` as a post-v1 standalone pioneer artifact; (3) extend `.conversusrc::default_agents` schema to accept URL entries with a "not yet supported" error in v1. **Explicitly asks for partial incorporation, not winner status** in Phase 4.

**Attacks Received**:
- **"ACP is two different protocols, you conflated them"** (backbone §6) — **Fully conceded** in Phase 2 cross-review §1.1 ("the researcher is right").
- **"The A2A coding-agent ecosystem is empty; no counterparties exist"** (backbone §9) — **Fully conceded**. Called it "the single most damaging factual error" against Round 1.
- **"Every future tool is A2A-native" is false"** — **Conceded**.
- **"Twelve months of stabilization counts from the wrong date"** — **Conceded**.
- **"30-line wrapper claim is ~10x low"** — **Conceded**.
- **"The wrapper is NOT conversus's problem was wishful thinking"** — **Partially conceded**; reframed as "conversus is the pioneer, here's the positive-EV argument." Researcher's own §5.2 endorsed the reframe.
- **"Build-our-own wins spec 048 unblocking outright"** — **Conceded in Phase 2 §2** as an explicit concession: "Insurmountable. Build-our-own wins this axis outright."
- **"Your 3-artifact plan hedges harder than the hybrid"** (build-our-own §4) — **Rebutted** in Phase 3 by clarifying the revised plan has 2 artifacts, not 3, with the pioneer wrapper explicitly post-v1.

**Attacks Delivered**:
- **"Protocol shape is a one-way door"** — **Partially landed**. Both other advocates accepted the concern; build-our-own absorbed it with a Week 1 design note commitment; litellm-hybrid accepted but did not bind it. This is a2a-future's strongest surviving claim.
- **"Spec 048 discovery gap — URL-addressable agents"** — **Unchallenged in the specific form**. Build-our-own added a `register_provider_instance()` runtime hook but did not propagate it into spec 048's `.conversusrc` schema. Litellm-hybrid explicitly deferred it. Validation battery §1.2 explicitly flags this as a pass criterion. **This is a2a-future's most defensible surviving claim** and is directly supported by the validation document.
- **"`conversus-a2a-claude` as post-v1 pioneer artifact has positive EV on both branches"** — **Endorsed by backbone-researcher §5.2** as a valid reframe. Build-our-own absorbed it in their Phase 3 plan.

**Credibility Assessment**: **Exemplary on concession discipline**. Conceded eight separate Round 1 errors cleanly in Phase 2/3. Explicitly retired "A2A first" and "wrap Claude Code as A2A server in v1" as Round 1 positions. Phase 4 closing is unusually honest — *"This is not a bid to win winner-take-all."* The self-scorecard in Phase 4 marks themselves **Weak on shipping velocity** and **Weak on current coverage**, which is accurate. Asking for partial incorporation rather than winner status is the correct posture given the Phase 2 concessions, and the judge instructions explicitly honor this.

**Criterion Scores**:

| Criterion | Score (1-5) | Justification |
|---|---|---|
| 1. Unblocks spec 048 on calendar | 2 | Round 1 plan would have delayed spec 042 indefinitely. Phase 3 revision has no unique v1 critical path — it inherits whatever the winner ships. Self-conceded "Weak" on this axis. |
| 2. Respects §5 ground-truth constraints | 4 | Round 1 violated §5.2 (empty A2A ecosystem). Phase 2/3 concessions bring the revised position into compliance. Loses a point because the path to compliance required abandoning the central thesis. |
| 3. Exercises full substrate matrix | 2 | Revised plan does not propose a concrete v1 provider set beyond inheriting the winner's. Does not directly address substrate validation. |
| 4. Free-tier / API-key-less user | 3 | Inherits whatever the winner ships. Not differentiated on this axis. |
| 5. Runtime agent discovery / URL registry | 5 | **Only advocate proposing the `default_agents` URL-entry schema change** with "not yet supported" error in v1. Directly answers validation battery §1.2. The one criterion where a2a-future has a unique, validated, uncontested win. |
| 6. Forward compat with A2A | 5 | The only position naming the one-way door explicitly. Week 1 protocol shape design note, triggered A2A commitment, pioneer wrapper as post-v1 artifact. This is the advocate whose entire surviving value is forward-compatibility insurance. |
| 7. Simplicity / scope hygiene | 3 | Amendments are cheap (~4 hours + 20 lines of schema). The main build is borrowed. Neither particularly simple nor particularly baroque. |

**Total Weighted Score**: Criterion 1 (Critical ×2 = 10), Criterion 2 (Critical ×4 = 20), Criterion 3 (High ×2 = 8), Criterion 4 (High ×3 = 12), Criterion 5 (High ×5 = 20), Criterion 6 (Medium ×5 = 15), Criterion 7 (Medium ×3 = 9) = **94/140**

---

## Winner

### Decision: **build-our-own-advocate**

**Rationale**:

**1. The decisive criteria are 1, 2, and 3 — spec 048 unblocking, §5 constraint respect, and full-substrate validation.** All three are Critical or High weight, and together they constitute 65 of 140 possible points (46%). Build-our-own scores Strong (5/5) on all three. Litellm-hybrid scores Strong on 1 and 2 but only Adequate (3/5) on criterion 3 because their v1 set omits the HTTP substrate (no `OpenCodeProvider`). This is the single biggest scoring gap between the two finalists: litellm-hybrid's v1 leaves the HTTP transport untested, which matters for the validation battery §4.1–§4.3 replay tests and for spec 048's long-fanout CI governance scenarios where subprocess cold-start is a documented concern (backbone §11 obs. 10, accepted by every advocate). Build-our-own's decision to move `opencode` into v1 in direct response to the researcher's cold-start finding is the kind of adversarial-process-driven refinement the deliberation is designed to produce.

**2. How the winner performed on the decisive criteria versus the runner-up.** Both finalists converged to within a single adapter file of each other, but the adapter-file delta is not where the criterion-weighted score separates. The separation happens on substrate validation (criterion 3, 20 points) and on spec 048 runtime-discovery schema headroom (criterion 5, 20 points). Build-our-own absorbed a2a-future's runtime-registry hook explicitly; litellm-hybrid explicitly deferred it. Build-our-own ships `OpenCodeProvider` in v1 to validate the HTTP substrate; litellm-hybrid does not ship an HTTP provider at all in v1. Each of these gaps is recoverable post-v1, but the validation battery wants both addressed in the ruling, not in a follow-on spec.

**3. What attacks the winner survived that the runner-up did not.** Build-our-own survived every factual attack from the researcher (LoC estimate, `claude-agent-sdk` dependency, ACP/A2A conflation) by absorbing each one into a strengthened plan. The corrections made the architecture better, not worse. Litellm-hybrid survived most attacks too, but they did not have a successful counter to build-our-own's "you omit the HTTP substrate and OpenCode's cold-start-free path from v1" critique — their closing argument does not mention `OpenCodeProvider` at all, which means the gap is real and unremediated. Build-our-own also survived a2a-future's strongest claim (protocol shape one-way door) by absorbing it as a Week 1 design note; litellm-hybrid absorbed the same claim but explicitly refused to bind it. Binding vs non-binding matters for a winner-take-all ruling because the arbiter's decision propagates into implementation; a non-binding absorption can be skipped.

**4. What the winner conceded and why those concessions are acceptable.** Build-our-own conceded the LoC estimate was ~2x low, the `claude-agent-sdk` path was misleading, the `acp`/`a2a` terminology conflated two protocols, LiteLLM belongs in v1 as an optional companion package, the "3 of 12 providers" framing was factually wrong, and the `mock` "3,428 tests" claim was rhetorically oversized. Every concession either strengthened the plan (dropping the `claude-agent-sdk` dependency) or was a minor framing correction (terminology, LoC, test count). No concession touched the core architectural claim that the protocol must be conversus-owned, that no unifying library exists, and that subprocess-CLI-JSON is the 2026-04 baseline. The concessions are acceptable because they demonstrate adversarial-process integrity rather than structural weakness.

**5. Practical implications of this choice.** Spec 048 (autonomous governance) unblocks in Month 2 of implementation — the single highest-stakes downstream spec. The validation battery replay tests (§4.1–§4.3) can exercise both subprocess and HTTP substrates in v1. The free-tier API-key-less user story (validation §2.3) is preserved via the native `AnthropicProvider` fallback path. The `conversus-a2a-claude` post-v1 pioneer artifact is committed as an ecosystem contribution. The spec 042 §11 matrix gets its terminology fix. Every advocate's strongest idea lives inside the winning plan.

---

## Runner-Up

### litellm-hybrid-advocate

**Why they lost**: Three criteria separated them from build-our-own.

- **Criterion 3 (full substrate validation)**: Litellm-hybrid's v1 set (`mock` + `claude-code` + `litellm`) ships `SubprocessProvider` but not `HTTPProvider`. The HTTP transport is entirely unvalidated in v1, which matters for validation battery §4.1–§4.3 replay tests, and it leaves cold-start mitigation as a documented concern with no v1 deliverable addressing it. Build-our-own specifically moved `opencode` into v1 to close this gap; litellm-hybrid did not.

- **Criterion 5 (runtime agent discovery / URL registry)**: Litellm-hybrid's Phase 3 revision explicitly defers this as "out of scope for v1 by spec definition." Validation battery §1.2 explicitly names this as a pass criterion (*"The config schema must not forbid URL entries... a schema that rejects the field outright is not [acceptable]"*). Build-our-own absorbed the `register_provider_instance()` hook; litellm-hybrid did not.

- **Criterion 4 (free-tier friction)**: Litellm-hybrid's v1 skips the native `AnthropicProvider` entirely, meaning a free-tier user who wants Anthropic API access but does not use Claude Code must install `conversus-provider-litellm` and pull in the LiteLLM dependency tree. Build-our-own provides a LiteLLM-free fallback path via native `AnthropicProvider`. This is a small but real friction difference for a user population that enterprise compliance teams care about.

**Conditions for reconsideration** (3 scenarios where litellm-hybrid would become the better choice):

1. **If LiteLLM's proxy mode composition with subprocess tools became the primary enterprise gateway story for spec 048**: Their unchallenged-through-silence claim about LiteLLM proxy fronting `OPENAI_BASE_URL`-honoring subprocess tools (Aider, Continue `cn`, Codex) would become strategically decisive. The backbone researcher flagged this as "interesting theoretical lever, not validated in practice." If a deployment validates it in practice within the next 3 months, the opportunity cost of shipping a parallel `AnthropicProvider` becomes a real loss instead of a cheap insurance policy.

2. **If the v1 engineering budget tightened further (e.g., to 2 weeks)**: Shipping only `mock` + `claude-code` + `litellm` is strictly faster than shipping 4 providers with 2 base classes. At a 2-week budget, the build-our-own v1 scope would not ship on time, and litellm-hybrid's narrower v1 would become the only viable option.

3. **If the validation battery §1.2 URL-schema constraint were relaxed**: The single biggest win for a2a-future's partial incorporation and for build-our-own's criterion-5 score is the URL-addressable registry commitment. If `validation.md` were revised to make §1.2 a "Phase 1-6 implementation requirement" rather than a blocking pass criterion, litellm-hybrid's criterion-5 score would rise to 3 or 4 and the overall gap would narrow considerably.

---

## Eliminated Competitors

### a2a-future-advocate

**Why eliminated**: Explicitly conceded in Phase 4 that they are not bidding to win winner-take-all. Their Phase 2/3 concessions on the A2A ecosystem emptiness, the ACP/A2A conflation, and the spec 048 hard-dependency argument eliminated their central thesis. The judge instructions explicitly honor their request for partial incorporation rather than treating them as a competitor for winner status.

**Best argument**: **Protocol shape is a one-way door.** The argument that `ExecutionTask`/`ExecutionResult` field shape is the only decision in spec 042 that is genuinely non-reversible is correct and was accepted by every other advocate. It is a 4-hour design commitment that costs nothing and prevents a 2027 breaking migration. The `.conversusrc::default_agents` URL-entry schema change is a directly supported ask from validation battery §1.2. These are real ecosystem-insurance wins. The backbone-researcher's §5.2 explicitly endorsed the `conversus-a2a-claude` pioneer-wrapper reframe as a valid positive-EV bet.

**Fatal weakness**: **No v1 critical path.** Round 1's "ship A2A first" was destroyed by the empty-ecosystem finding. Phase 3's three amendments are all cheap enough that they should be incorporated into the winner's plan, but none of them constitutes a standalone architecture. A2A-future is a partial-incorporation candidate, not a winner.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

**No remaining disputes — verdict is decisive, but one close call is worth recording.**

The gap between build-our-own (127/140) and litellm-hybrid (113/140) is 14 points out of 140 — a 10% margin. This is not a landslide; it is a decisive win with a real runner-up. The single largest contributor to the margin is criterion 3 (full substrate validation), where litellm-hybrid's v1 omits `OpenCodeProvider` and therefore does not exercise the HTTP transport substrate. If the validation battery tolerated an unvalidated HTTP substrate in v1, the margin would narrow to ~6 points and the ruling would be tight enough to warrant a tiebreaker on criterion 7 (simplicity), which litellm-hybrid wins.

The judge instructions named the tiebreaker as "which choice is safer to be wrong about." On the narrow question of the adapter-file delta (build-our-own ships parallel `anthropic` + `litellm`; litellm-hybrid ships `litellm` alone), build-our-own is safer to be wrong about: if the redundant adapter turns out to be unnecessary, it costs ~300 lines of maintenance; if the missing native path turns out to be necessary (enterprise compliance, LiteLLM outage, air-gap), adding it later is a user-visible break. Build-our-own's Phase 4 framing of this as "cheap insurance" is correct, and the tiebreaker confirms the ruling.

The litellm-hybrid advocate's unchallenged claim about LiteLLM proxy mode fronting subprocess tools (which I verified is genuinely unchallenged through 6 cross-reviews and 3 competitor revisions) is credited in their scoring on criterion 7 but does not flip the outcome. The backbone researcher explicitly noted they did not verify the end-to-end composition; the claim is "interesting theoretical lever, not validated in practice." Under the silence-is-concession rule, the claim stands, but it is not decisive on any of the three Critical/High criteria where the ruling is determined.
<!-- CONVERSUS:DISPUTES_END -->

---

## Decision Record

### Status
**Accepted** (pending arbiter ratification in Phase 6)

### Context
Conversus orchestration today is coupled to Claude Code's in-session `Agent` tool, which cannot run headless, in CI, or from the Python SDK. Spec 042 defines an `ExecutionProvider` protocol that decouples the engine from any single dispatch mechanism. Spec 048 (autonomous governance) declares spec 042 a HARD DEPENDENCY and cannot ship until the execution-provider layer is in place. The blog generation pipeline, the `conversus governance` CLI, GitHub Actions integration, and every headless execution surface named in spec 048 §11 are blocked on spec 042 shipping.

A winner-take-all deliberation between four agents (one factual witness and three architectural advocates) produced extensive convergence during adversarial cross-review. The central architectural question — whether conversus should own its own `ExecutionProvider` protocol or delegate the abstraction to an external framework (LiteLLM, A2A) — was answered in favor of conversus ownership by unanimous concession. The backbone researcher's factual findings (no unifying library exists; subprocess-CLI-JSON is the 2026-04 baseline; A2A coding-agent ecosystem is empty; `claude-agent-sdk` is a subprocess wrapper; MCP is tools not dispatch; two different protocols share the "ACP" name) were ratified by all three advocates by Phase 3.

The residual disagreements at Phase 4 were about v1 scope: which providers ship in the first release, whether to ship a parallel native `AnthropicProvider` alongside `LiteLLMProvider`, and whether to bind three specific forward-compatibility commitments (A2A-shaped protocol fields, post-v1 `conversus-a2a-claude` pioneer artifact, URL-addressable `.conversusrc::default_agents` schema).

### Decision
**Adopt build-our-own-advocate's Phase 3 architecture as the winning v1 plan for spec 042.** Ship conversus's own `ExecutionProvider` protocol (spec 042 §3 verbatim) with a `SubprocessProvider` base class and a `HTTPProvider` base class. Ship four providers in v1: `mock`, `anthropic` (native SDK), `claude-code` (via direct `claude -p --bare` subprocess, NOT through `claude-agent-sdk`), and `opencode` (via `HTTPProvider` against the published OpenAPI 3.1 spec). Ship `LiteLLMProvider` as an optional companion package (`conversus-provider-litellm`) in the same release window. Rename the spec 042 §11 `acp` row to `a2a` and add a separate lower-priority `zed-acp` row for IDE integration. Commit to `conversus-a2a-claude` as a post-042 standalone pioneer artifact when team bandwidth permits. Design `ExecutionTask` and `ExecutionResult` field shapes to be A2A-Task-Request-semantic-compatible as a Week 1 design note. Extend `.conversusrc::default_agents` schema to accept URL entries with a "URL-addressable agents not yet supported in v1" error.

### Alternatives Considered

- **litellm-hybrid-advocate (runner-up)**: Ship `mock` + `claude-code` + `litellm` as v1 with no parallel `anthropic` adapter and no `OpenCodeProvider`. Strongest on scope hygiene and maintenance burden minimization. Not selected because the v1 scope omits the HTTP substrate entirely, leaves validation battery §1.2 (URL schema) unaddressed, and forces the free-tier API-key-using user to take a LiteLLM dependency.

- **a2a-future-advocate**: Round 1 position ("ship A2A first") was conceded as defeated in Phase 2. Phase 3 revised position ("three forward-compatibility amendments to the winner") is not a standalone architecture; it is a partial-incorporation request that the winning plan honors (see Consequences → Positive).

- **backbone-researcher**: Not an architectural competitor. Factual witness role. Findings treated as joint-ratified constraints on the decision space.

### Consequences

**Positive consequences**:
- Spec 048 (autonomous governance) unblocks in ~13–19 working days, on the only calendar that permits spec 040/043/044/046/048 to ship on their respective roadmaps.
- Validation battery §3 (concurrency), §4 (replay tests), and §5 (ground-truth constraints) all pass with the four-provider v1 set exercising every important substrate axis.
- The free-tier API-key-less user (validation §2.3) can run a deliberation with zero env vars via the `claude-code` direct-CLI provider. Users with API keys but no Claude Code get the native `AnthropicProvider` fallback. Users wanting the 100+ model long tail install the optional `conversus-provider-litellm` package.
- **All three of a2a-future-advocate's partial-incorporation asks are honored**: (a) `ExecutionTask`/`ExecutionResult` field shape designed A2A-Task-Request-semantic-compatible in Week 1 as a design note with a `from_prompt()` compatibility constructor (cost: ~4 hours); (b) `conversus-a2a-claude` committed as a post-042 standalone pioneer artifact ensuring conversus is the first to wrap a shipping coding agent as an A2A server; (c) `.conversusrc::default_agents` schema accepts URL entries with a "not yet supported" error in v1, preventing a 2027 schema migration.
- The spec 042 §11 `acp` → `a2a` rename plus separate `zed-acp` row closes a spec-hygiene bug that the adversarial process elevated from "minor terminology nit" to "mandatory correction."
- The `SubprocessProvider` and `HTTPProvider` base classes apply the monorepo's existing `BaseIntegrator` discipline to the execution-provider layer, keeping substrate work factored into one place rather than duplicated across adapters.

**Negative consequences / accepted trade-offs**:
- **~300 lines of adapter redundancy**: Both `AnthropicProvider` and `LiteLLMProvider` ship in v1, and most users will install one or the other, not both. This is the single largest criticism from the litellm-hybrid advocate's closing. The trade-off is accepted because the redundancy provides resilience (LiteLLM-free Tier-3 path for compliance/air-gap/outage scenarios) and validation coverage (a native direct-SDK reference implementation that future adapter authors can copy without pulling in LiteLLM).
- **v1 LoC budget is ~1,400–1,500**, not the ~500–700 the Phase 1 build-our-own review cited. The corrected estimate is honest and still tractable, but it is ~2x the original rhetoric.
- **Subprocess cold-start (~1–3 seconds per `claude -p` invocation without `--bare`) is a documented operational cost** that the v1 `ClaudeCodeProvider` inherits. Mitigation is `--bare` mode by default and the `OpenCodeProvider` HTTP path for high-fanout workloads; full process-pooling is deferred to post-v1.
- **The `LiteLLMProvider` proxy-mode-fronting-subprocess-tools composition is unverified in practice**. Litellm-hybrid's unchallenged-through-silence claim about enterprise gateway integration via `OPENAI_BASE_URL` is theoretically sound but has not been end-to-end validated. The winning plan neither claims nor prevents this pattern; users who need it can exercise it independently.

**Risks to monitor**:
- **If LiteLLM's release cadence or security posture deteriorates** (missed security patches, breaking API changes, abandonment), the `LiteLLMProvider` optional package becomes a liability and users fall back to native adapters. The v1 plan's resilience via `AnthropicProvider` limits the blast radius but does not cover OpenAI, Gemini, Bedrock, Ollama, or the long tail. Trigger a review of the Tier-3 strategy if LiteLLM's maintainer health degrades.
- **If the A2A coding-agent ecosystem materializes faster than 2027** (e.g., Anthropic or GitHub ships an A2A server wrapper for their CLI in the next 6 months), the `a2a` provider triggered-commitment (3-of-6 counterparties) fires earlier than expected, and `conversus-a2a-claude` pioneer-artifact status depends on conversus shipping first. Monitor A2A ecosystem signals quarterly.
- **If validation battery §1.2 URL-schema requirement is exercised by a real spec 048 user** (someone configuring a custom governance agent behind a URL), the v1 "not yet supported" error must upgrade to a working `ACPProvider` dispatch path within one release cycle. This could fire before the A2A counterparty trigger does, and the team should be prepared to ship a minimal `ACPProvider` that dispatches to a single pre-wrapped agent (likely `conversus-a2a-claude`) as the proving-ground implementation.

---

**End of verdict. The Phase 6 arbiter (conversus-chief-architect) will affirm, override, or affirm-with-conditions this ruling against the validation battery in `validation.md`.**
