# Build-Our-Own-Advocate — Phase 4 Closing Argument

**Round**: 1, Phase 4 (Closing Arguments / Disputes)
**Iteration**: 1
**Date**: 2026-04-05
**Position**: Build conversus's own `ExecutionProvider` Protocol. Ship 4 providers in v1 (`mock`, `anthropic`, `claude-code` via direct `claude -p --bare` subprocess, `opencode` via `HTTPProvider`). `LiteLLMProvider` ships as an optional v1 companion package. `SubprocessProvider` and `HTTPProvider` base classes factor out the substrate. A2A is a triggered roadmap commitment with `conversus-a2a-claude` as a planned post-042 standalone pioneer artifact. Protocol field shape is designed A2A-friendly in Week 1 as a docstring-level constraint with no `a2a-sdk` dependency.

---

## Head-to-Head Scorecard

Seven criteria matter for spec 042's architectural decision. The weighting rationale comes directly from the validation battery (`specs/042-execution-providers/validation.md`) and the hard dependencies listed in spec 048.

**Scoring scale**: Strong / Adequate / Weak. Factual-witness (backbone-researcher) is scored on *evidentiary coverage*, not architectural preference — the researcher is non-advocating.

| Criterion | Weight | Build-Our-Own (me) | Backbone-Researcher (witness) | LiteLLM-Hybrid | A2A-Future |
|---|---|---|---|---|---|
| **1. Protocol ownership (conversus-owned `ExecutionProvider`)** | **High** — load-bearing for every downstream spec (046, 048, 020); validation §5.4 is a ground-truth constraint | **Strong** — origin of the claim; both adversarial advocates conceded verbatim that protocol ownership is "conversus code, not LiteLLM" (litellm-hybrid §8 Week 1) and "the correct v1 foundation" (a2a-future §5) | **Strong** (witness) — §5.4 "no unifying library exists" is the finding that forced both competitors to my position | **Strong** (absorbed) — litellm-hybrid now ships spec 042 §3 verbatim; this is my protocol with their name on it | **Strong** (absorbed) — a2a-future now calls build-our-own "the correct v1 foundation" |
| **2. v1 provider coverage (tool-use + no-tool-use + HTTP + subprocess)** | **High** — validation §4.1 "replay spec 042 deliberation" requires exercising every substrate; minimum-validating-set matters | **Strong** — 4 providers (`mock`, `anthropic`, `claude-code`, `opencode`) exercise **every** axis: no-tool-use Tier-3, subprocess Tier-1, HTTP Tier-1, test-substitution. Adding any 5th v1 provider adds zero validation coverage | N/A (witness) — confirms the taxonomy in §7, §10 | **Adequate** — proposes `mock` + `claude-code` + `litellm` only. Misses `HTTPProvider` substrate entirely in v1; OpenCode/A2A slot has no v1 validation. The only v1 plan that does not exercise the HTTP path | **Weak** — does not propose a concrete v1 provider set beyond "whatever the hybrid ships"; concedes subprocess baseline |
| **3. Free-tier friction (spec 033 / validation §2.3 API-key-less user)** | **High** — validation §2.3 "a free-tier user with no API keys — only Claude Code locally — can run a deliberation" is a named pass criterion | **Strong** — `claude-code` direct-CLI provider requires zero env vars, zero API keys. The `claude` binary handles auth. Free-tier user installs `pip install conversus` + has Claude Code locally = it works. `anthropic` native option available for users with API keys but no Claude Code | N/A (witness) — §5.5 flags cold-start as orthogonal cost, not friction | **Adequate** — `mock` + `claude-code` works for the named scenario. But dropping `anthropic` native means the free-tier user who wants direct-API must immediately install the LiteLLM dep tree. More friction, not less | **Adequate** — inherits whatever the hybrid ships; does not contest this axis |
| **4. Spec 048 unblocking on the only calendar that exists** | **Critical** — validation §1.1 lists spec 048 as a HARD dependency blocker; a2a-future §2 conceded "build-our-own wins this axis outright" | **Strong** — ~13–19 working days to v1 ship. No external ecosystem dependencies. `ClaudeCodeProvider` subprocess path works against tools that exist today. spec 048 unblocks immediately after Phase 6 | **Strong** (witness) — §5.2 confirms "A2A coding-agent ecosystem is empty"; subprocess is the only 2026-04 calendar | **Strong** — same timeline (converged to spec 042 §3 verbatim); one adapter less, roughly same wall clock | **Adequate** — conceded outright in their §2. A2A-first timeline is "2027–2028 event"; they do not claim to unblock spec 048 faster than build-our-own |
| **5. A2A future-proofing (one-way door protection)** | **Medium-High** — a2a-future's surviving claim; validation §1.2 requires URL-addressable schema not be forbidden | **Strong** — absorbed a2a-future's one-way door argument: protocol field shape designed A2A-friendly in Week 1 as docstring constraint (structured parts semantics, references, metadata), zero `a2a-sdk` dependency in v1. `register_provider_instance()` hook for dynamic discovery. Triggered roadmap commitment to `a2a` row in §11. **Conversus authors `conversus-a2a-claude` as a standalone pioneer artifact post-v1** — the single most ecosystem-leveraged deliverable in the deliberation | N/A (witness) — §5.2 flags empty ecosystem; §11 obs 3 recommends A2A-semantic shape, which my Phase 3 adopts | **Weak** — litellm-hybrid's cross-review §5.2 acknowledged the one-way door as "residual disagreement" and said they would "add a docstring." This is my position, absorbed. But litellm-hybrid does **not** commit to `conversus-a2a-claude` or runtime registration hook | **Strong** (as claim) — but their v1 deliverable is exactly the set of amendments I now absorb. Their three amendments (protocol shape, pioneer wrapper, URL schema) are all inside my Phase 3 plan |
| **6. LoC realism (validation §5.1 ground truth constraint)** | **Medium** — validation §5.1 requires honest accounting of subprocess lifecycle cost | **Adequate** — corrected from Phase 1 ~500–700 LoC to Phase 3 ~1,400–1,500 LoC (core + engine-side adaptation). Factored via `SubprocessProvider`/`HTTPProvider` base classes. **Conceded** the original number was ~2x low | **Strong** (witness) — the forcing function behind my correction; §2.3 established the realistic cost envelope | **Adequate** — claims 300 fewer lines by dropping `anthropic`. True as arithmetic; the ~300 lines are the disputed redundancy (see "Why Pick Me" below) | **Adequate** — adds the `conversus-a2a-claude` wrapper (~300–600 LoC), explicitly post-v1 and standalone. Same envelope when scoped honestly |
| **7. Test isolation / `mock` provider story** | **Medium** — validation §4.1/4.2/4.3 replay tests require reproducible dispatch doubles | **Strong** — `MockProvider` is a Protocol-typed test double replacing ad-hoc agent mocking. **Conceded** the "3,428 tests" rhetoric was under-specified; downgraded claim to structural benefit, which holds | **Adequate** (witness) — §7 of researcher cross-review noted the claim was un-audited; factual scope correctly flagged | **Strong** — ships `mock` in v1 identically. Zero delta on this axis | **Adequate** — inherits from baseline; does not contest |

**Weighting rationale**: criteria 1, 2, 3, 4 are High because the validation battery (`validation.md`) names each as a blocking pass criterion. Spec 048 unblocking (criterion 4) is the single highest stake — the validation document's §7 states a "hard dependency" failure triggers rejection. Criterion 5 (A2A future-proofing) is Medium-High because it is a2a-future's entire surviving claim and a validation §1.2 schema concern. Criteria 6 and 7 are Medium because they are engineering discipline concerns, not architectural blockers.

---

## Conceded Weaknesses

I list every concession I made in Phase 2 and Phase 3 without spin. The judge will compare this against the actual record.

### 1. LoC estimate was ~2x low for `claude-code` (Phase 3, from backbone-researcher §2.3)

- **Raised by**: backbone-researcher, in the cross-review of my Phase 1 position
- **Weakness**: I cited `tool-landscape.md`'s "100–200 lines per adapter" figure as ground truth. A production `claude-code` subprocess provider realistically needs 400–800 LoC when you count lifecycle, JSON stream parsing, flag marshalling, binary discovery, cold-start economics, `read_paths` semantics, and `output_path` enforcement
- **My Phase 3 response**: Adopted. Revised total from ~500–700 LoC to ~1,400–1,500 LoC (core + engine-side tool-use adaptation). Factored the substrate into `SubprocessProvider` base class so the work lives in one place
- **Severity**: **Moderate**. The original number was wrong. The architectural conclusion — that the refactor is tractable — survives with an honest number. The researcher's own Phase 3 revision (§Partially Rebutted §1) agrees: "the *total* cost at v1 is roughly the same — the substrate has to exist somewhere"

### 2. `claude-agent-sdk` path was misleading in the dependency table (Phase 2, from backbone-researcher §4.1)

- **Raised by**: backbone-researcher
- **Weakness**: I labeled `claude-code` as "`claude-agent-sdk` OR subprocess (zero new deps)." This elided that `claude-agent-sdk` is (a) an alpha-at-0.1.56 PyPI package, (b) itself a subprocess wrapper around the bundled `claude` CLI binary, and (c) even the "OR subprocess" path still needs the `claude` CLI on PATH
- **My Phase 3 response**: Dropped `claude-agent-sdk` from the v1 plan entirely. `ClaudeCodeProvider` invokes `claude -p --bare --output-format json` directly via `asyncio.create_subprocess_exec`. Deployment docs explicitly list the `claude` CLI binary as a prerequisite
- **Severity**: **Minor**. The correction *strengthens* the plan — dropping an alpha dep with bundled-binary distribution complexity is a win, not a loss. All three advocates converged on direct-CLI as the right path

### 3. ACP/A2A conflation in spec 042 §11 (Phase 3, from backbone-researcher §3.2)

- **Raised by**: backbone-researcher (first), then joint-ratified by all three advocates
- **Weakness**: My Phase 1 "ACP-compatible superset" framing inherited spec 042's ambiguous "ACP" umbrella. A2A (LF AI & Data, JSON-RPC over HTTP, headless dispatch) and Zed/JetBrains Agent Client Protocol (stdio JSON-RPC, IDE integration) are different protocols with different wires
- **My Phase 3 response**: Conceded fully. Spec 042 §11 must rename `acp` → `a2a` and add a separate (lower-priority) `zed-acp` row. My "superset" argument applies to A2A's Task Request model, not to the IDE-facing stdio protocol
- **Severity**: **Minor**. Spec-hygiene fix, not an architectural change. Every advocate agreed in cross-review; the correction is joint-ratified and the architecture is unchanged

### 4. `LiteLLMProvider` belongs in the v1 provider set (Phase 2, from litellm-hybrid)

- **Raised by**: litellm-hybrid-advocate
- **Weakness**: My Phase 1 "defer LiteLLM" position understated LiteLLM's genuine operational value (100+ model long-tail, retry/cost/rate-limit discipline, proxy mode, local/self-hosted coverage)
- **My Phase 3 response**: Absorbed. `LiteLLMProvider` ships in v1 as an optional companion package (`conversus-provider-litellm`). This is the superset: users pick `conversus-provider-litellm` for breadth or `conversus-provider-anthropic` for minimum dependency footprint. Both coexist under the same Protocol
- **Severity**: **Moderate** (as a Phase 1 framing error), **nil** after absorption. The litellm-hybrid advocate's Phase 3 closing concedes the architecture is mine; the remaining disagreement is a single adapter file (§ below)

### 5. `mock` provider "stabilizes 3,428 tests" was under-specified (Phase 3, self-raised)

- **Raised by**: self, in my own cross-review §5.1
- **Weakness**: I had not enumerated how many of conversus's 3,428 tests actually exercise agent dispatch vs template rendering vs phase logic. The rhetoric over-claimed
- **My Phase 3 response**: Downgraded. The revised claim is "`MockProvider` replaces ad-hoc agent mocking with a protocol-typed test double, one mock and one source of truth." The structural benefit holds regardless of the exact test count
- **Severity**: **Minor**. The rhetoric was oversized; the underlying advantage is real and unique to protocol ownership (LiteLLM cannot provide it for Tier-1; A2A cannot provide it in 2026-04)

### 6. Engine-side tool-use adaptation is a non-trivial cost I did not price in Phase 1 (Phase 3, self-raised)

- **Raised by**: self, in cross-review §5.2
- **Weakness**: Spec 042 §4 lines 268–290's inline-and-post-write logic (for `supports_tool_use=False` providers) is ~150–250 LoC that lives on the engine side, not in any provider. My Phase 1 LoC budget did not include it
- **My Phase 3 response**: Added to the Phase 1 LoC budget explicitly. Validated end-to-end by `AnthropicProvider` in implementation Phase 2
- **Severity**: **Minor**. It was priced in by Phase 3; the total envelope (~1,400–1,500 LoC) reflects it

---

## Surviving Advantages

### Unchallenged strengths (no competitor attacked these)

1. **The engine has exactly one dispatch call site** (Phase 1 §2.4, established Phase 1, unchallenged through Phase 3). `Agent(prompt=..., run_in_background=True)` in SKILL.md is the only place the refactor touches. No competitor contested this. FR-009/010/011 backward-compat guarantees are trivially achievable because there is one place to change. The backbone-researcher's §1.4 independently confirmed the claim.

2. **Owning the Protocol is exactly what lets us have two provider rows for two wire protocols** (Phase 3, emerged from cross-review). Under a LiteLLM-shaped or A2A-shaped architecture, splitting `acp` into `a2a` and `zed-acp` would require the external framework to have opinions. Under a conversus-owned Protocol, the split is trivial: two rows, two adapters. The backbone-researcher's own critique §3.2 concluded: *"build-our-own actually **strengthens** when you acknowledge the split — because owning the Protocol is exactly what lets you have two providers where the wire-level standard has two protocols."*

3. **`SubprocessProvider` base-class factoring is the `BaseIntegrator` pattern applied to execution providers** (Phase 3, new argument). The monorepo's own integrator architecture principle — "one base, many file types; new integrators add what to deploy, never how to deploy" — maps exactly onto the execution provider layer. `SubprocessProvider` factors the six-tool substrate into one place; `HTTPProvider` factors the long-lived-connection substrate into another. This is not advocacy — it is consistent with the monorepo's existing engineering discipline. The backbone-researcher's Phase 3 revision §New Argument 2 explicitly endorsed this as "the correct response to my Phase 1 §7 finding."

4. **The 4-provider v1 set validates every substrate and every tool-use mode** (Phase 3, new argument). `mock` validates the Protocol shape. `anthropic` validates `supports_tool_use=False` + engine-side file inlining. `claude-code` validates `SubprocessProvider` + `supports_tool_use=True`. `opencode` validates `HTTPProvider`. Any fifth v1 provider adds zero validation coverage; any smaller v1 set leaves a substrate unexercised. litellm-hybrid's v1 proposal drops `anthropic` AND drops `opencode` — the only v1 plan that fails to exercise the HTTP substrate at all.

### Rebutted attacks (competitors attacked, defense held)

5. **"Mock stabilizes tests" downgrade did not weaken the underlying advantage** (Phase 3). The rhetorical claim was downgraded, but the structural benefit — one Protocol-typed test double replacing scattered ad-hoc patterns — is unique to protocol ownership. LiteLLM cannot provide it for Tier-1 (LiteLLM does not dispatch agents). A2A cannot provide it in 2026-04 (no counterparties). Only a conversus-owned Protocol gives us a conversus-owned mock.

6. **Protocol shape ossification is an absorbable concern, not an architectural blocker** (Phase 3 vs a2a-future). a2a-future's one-way-door argument is serious and I absorb it: design the field shape A2A-friendly in Week 1 as a docstring constraint with `parts`-style semantic structure, zero `a2a-sdk` dependency. ~4 hours of design work. The defense held because the absorption is cheap and preserves the future migration path without adopting A2A in v1.

### Competitor concessions I do not share

7. **Both adversarial advocates explicitly conceded protocol ownership to me, verbatim** (Phase 2 and Phase 3):
   - litellm-hybrid §10: *"The build-our-own advocate wrote a better review than I did on the protocol-ownership question."*
   - litellm-hybrid §8 Week 1 deliverable: *"Implement `ExecutionProvider`, `ExecutionTask`, `ExecutionResult` per spec 042 §3 — conversus code, not LiteLLM."*
   - a2a-future §5: *"Build-our-own's `ExecutionProvider` protocol is the correct v1 foundation for spec 042. A2A is the most important future provider within that protocol, not a replacement for it."*

   These are not paraphrases. Both competing advocates' closing positions cite my protocol as the foundation of theirs. The architectural question is not contested at Phase 4; only the v1 provider count is.

8. **a2a-future conceded build-our-own wins spec 048 unblocking "outright"** (Phase 2, quoted in my Phase 3 §Reinforced Strengths §4). The hard-dependency argument moved from "my claim" to "stipulated by all parties." Spec 048 cannot ship without spec 042 shipping first, and the only architecture that ships spec 042 in 2026-04 is build-our-own (with litellm-hybrid now being a subset of this, by their own admission).

---

## Why Pick Me

### 1. The core decision

The single most important factor for spec 042 is this: **which architecture makes every downstream spec easier, not harder, while unblocking spec 048 on the only calendar that exists?** The validation battery (`validation.md` §1.1, §7) elevates spec 048 to blocker status — if the winner cannot unblock autonomous governance mode in 2026-04, the winner must be rejected. Every advocate now agrees the A2A ecosystem is empty in 2026-04 (validation §5.2, joint-ratified). Every advocate now agrees subprocess-CLI is the baseline. Every advocate now agrees the protocol must be conversus-owned (validation §5.4, joint-ratified).

The question collapses to: **who ships the most validated v1 on the tightest honest timeline?**

My answer is four providers in ~1,400–1,500 LoC over ~13–19 working days: `mock` (Protocol validation), `anthropic` (no-tool-use path), `claude-code` (subprocess substrate + SKILL.md backward compat), `opencode` (HTTP substrate + cold-start mitigation). Every important axis of the Protocol is exercised before v1 ships. `LiteLLMProvider` lands the same week as an optional companion package. `conversus-a2a-claude` lands post-042 as the first A2A server wrapper of a shipping coding agent in the world — the single highest-leverage ecosystem contribution anyone proposed.

My plan is a **superset**. It contains everything litellm-hybrid ships (LiteLLMProvider as first-class v1) and everything a2a-future ships (A2A-shaped protocol, pioneer wrapper, URL-addressable registry hook), with one extra thing that they do not ship: a hand-rolled `AnthropicProvider` alongside `LiteLLMProvider`. That one extra thing is the sole remaining disputed line of code in the deliberation.

### 2. The risk calculus

**What the judge risks by picking me**: ~300 lines of adapter code (`AnthropicProvider` native SDK) and the ongoing maintenance cost of one SDK upgrade cycle. That is the entire downside. Specifically:

- If LiteLLM is healthy in 2027: the `AnthropicProvider` native adapter sees less use; users gravitate toward the LiteLLM companion package; the native adapter's maintenance is ~1 engineer-day per year
- If LiteLLM has an outage, pins go stale, or an enterprise air-gap requires zero framework deps: native `AnthropicProvider` is the resilience path, and users can reach Anthropic through a package with no LiteLLM in the dep tree. This is validation §2.1 "clean-venv free-tier install" *without* a LiteLLM transitive dependency
- If an enterprise compliance team forbids LiteLLM (PyPI package provenance, license review, security posture): native `AnthropicProvider` is the only path for Anthropic users in that segment

**What the judge risks by picking litellm-hybrid**: a v1 that does not exercise the HTTP substrate (no `OpenCodeProvider` in their v1 set) AND does not ship any LiteLLM-free Tier-3 path AND does not commit to `conversus-a2a-claude` as a pioneer artifact AND does not address the A2A one-way-door protocol shape beyond a promised docstring. Three of these four risks are serious; none is present in my plan.

**What the judge risks by picking a2a-future**: a2a-future's Phase 3 revision **already concedes** build-our-own is the correct v1 foundation. They are no longer proposing a competing architecture; they are proposing three amendments to the hybrid baseline that I have already absorbed. Picking a2a-future at Phase 6 means picking my architecture with the same amendments and a more restrictive framing around where they live (protocol shape constraint, post-v1 pioneer wrapper, URL registry hook — all three are inside my Phase 3 plan verbatim).

**What the judge risks by picking the backbone-researcher**: the researcher is the factual witness and explicitly does not recommend a winner. Scoring them as a fourth option is a category error — their report is shared input to all three advocates' positions. Every advocate built on their findings. The researcher's Phase 3 §Closing states directly: *"I do not recommend a winner. I report that all three revised positions are consistent with the factual landscape, and the decision is a matter of engineering priority, not correctness."*

The asymmetry is stark: my plan costs 300 lines of redundancy. The alternatives each cost a concrete v1 deliverable that my plan includes for free.

### 3. The practical path — the next 6 months

**Weeks 1–3** (Implementation Phase 1–3): Protocol, data classes, registry with `register_provider_instance()` hook for future A2A discovery, `MockProvider`, `AnthropicProvider`, `SubprocessProvider` base class. Protocol field shape documented as A2A-Task-Request-semantic-compatible in the Week 1 PR (a2a-future's one-way door absorbed). ~880 LoC.

**Weeks 4–5** (Implementation Phase 4–5): `ClaudeCodeProvider` via direct `claude -p --bare` (no SDK), `HTTPProvider` base class, `OpenCodeProvider` against OpenAPI 3.1 spec. Cold-start-free path available for high-fanout spec 048 workloads. ~600 LoC.

**Week 6** (Implementation Phase 6): SKILL.md migration to `ClaudeCodeProvider` through the Protocol. FR-009/010/011 backward-compat tests. Spec 042 §11 rename (`acp` → `a2a`, add `zed-acp` row). `conversus-provider-litellm` optional package ships same week or right after. Spec 042 v1 closes. **Spec 048 unblocks.**

**Month 2–3**: `conversus-provider-litellm` graduates to recommended-default for Tier-3 breadth users. Post-042 ecosystem work begins: `AiderProvider`, `CopilotCLIProvider`, `GeminiCLIProvider` as `SubprocessProvider` subclasses land incrementally. Spec 048 implementation proceeds in parallel with governance mode reaching CI.

**Month 4–6**: `conversus-a2a-claude` standalone package authored as a post-042 ecosystem contribution — wrapping the existing `ClaudeCodeProvider`'s `claude -p --bare` machinery behind an A2A server interface. This is the single highest-leverage ecosystem bet in the deliberation: conversus becomes the first team to wrap a shipping coding agent as an A2A server, and every future A2A client in the world benefits. The work rests on the v1 subprocess machinery that already exists — the A2A server wrapper is an HTTP shell around code we wrote in Week 4. Meanwhile, when the triggered precondition fires (at least 3 of {Claude Code, Aider, OpenCode, Copilot, Codex, Gemini} ship A2A endpoints), the `a2a` client provider inside conversus lands as an `HTTPProvider` subclass — additive, non-breaking, one more row in the matrix.

This is not a roadmap of aspirations. Every step is a subclass of a base class that exists by Week 6. The validation battery tests are addressable because the abstraction is the right shape. Spec 048 unblocks in Month 2. Spec 046 and 020 follow.

### 4. The honest ask

I am asking the judge to accept exactly one trade-off: **~300 lines of adapter code (`AnthropicProvider` native SDK) that serves a smaller user segment than `LiteLLMProvider` does**, in exchange for four things:

1. **Resilience**: The v1 provider set contains a LiteLLM-free path to the Anthropic API. If LiteLLM has an outage, an enterprise air-gap, a dependency conflict, or a compliance rejection, users with Anthropic API keys still have a Tier-3 path. This is not theoretical — enterprise compliance teams reject PyPI packages for a variety of reasons, and conversus's free-tier audience is exactly the kind of user (individual developers, small teams, open-source projects) most likely to run into supply-chain friction that a framework absorbs. Having both adapters means the Tier-3 path survives independent of any single vendor's fortunes.

2. **Validation coverage**: `AnthropicProvider` exercises the `NativeProvider`-style direct-SDK adapter path. `LiteLLMProvider` exercises it too, but through a framework layer. Shipping both means the **pattern** is validated twice — once thinly (LiteLLM) and once deeply (native SDK). When a future user implements `conversus-provider-openai` or `conversus-provider-gemini`, they have a clean reference to follow that does not require pulling in LiteLLM. The litellm-hybrid advocate's claim that "`LiteLLMProvider.supports_tool_use = False` exercises the same engine path" is true for the engine, false for the adapter-authoring experience.

3. **Superset posture**: My plan is the only one all three advocates can sign onto without concessions to each other. litellm-hybrid's Phase 3 closing wants three things: the protocol, `LiteLLMProvider` in v1, and `claude-code` via subprocess. I ship all three. a2a-future's Phase 3 closing wants three things: A2A-shaped protocol, pioneer wrapper, URL-addressable registry. I ship all three. The only residual is 300 lines of resilience code that costs the deliberation nothing. A plan that strictly dominates on every competing axis except one minor redundancy is the plan that should win.

4. **The A2A future-proofing commitment is real, not cosmetic**: I am committing, as part of the v1 spec, to (a) design the `ExecutionTask`/`ExecutionResult` field shape A2A-Task-Request-semantic-compatible in Week 1 as a docstring-level constraint, (b) add `register_provider_instance()` to the registry for runtime dynamic discovery, (c) keep `a2a` as a first-class row in spec 042 §11 with a triggered elevation commitment (3-of-6 counterparty precondition), and (d) author `conversus-a2a-claude` as a standalone post-042 ecosystem package. No `a2a-sdk` dependency in v1 core. a2a-future's one-way door argument is taken seriously, not dismissed, and their single most valuable strategic idea (pioneer wrapper) is inside my plan.

The honest version of my ask is: **give me 300 lines of redundant-but-resilient code, and I give you the superset plan with every adversarial advocate's strongest ideas inside it, shipping on the only calendar spec 048 permits, validated on every important substrate, and forward-compatible with the A2A future that will probably arrive in 2027–2028.**

That is the trade-off. I believe the 300 lines are resilience, not waste. The judge should too.

---

**End of closing argument.**
