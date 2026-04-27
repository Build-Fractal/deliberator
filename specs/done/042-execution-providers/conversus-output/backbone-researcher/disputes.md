# Backbone Researcher — Phase 4 Closing Argument

**Role**: Tooling archaeologist. Non-advocate. My "position" is the set of factual findings the winning architecture must respect, regardless of which advocate the arbiter selects.
**Phase**: Round 1, Phase 4 (disputes / closing)
**Date**: 2026-04-05
**Iteration**: 1

---

## Framing for the Arbiter

I am not asking to win. The three advocates are asking to win — one of them will. My job in Phase 4 is to put on the record the set of ground-truth findings the winning architecture **must not contradict**, so the arbiter can test the ruling against the evidence rather than against rhetoric.

Read this document as the judge's factual witness. The scorecard below scores each advocate on **fidelity to research findings**, not on my preferred architecture vs theirs (I have no preferred architecture). The "Why Pick Me" section is reframed as "Why The Arbiter Must Respect These Facts." The conceded weaknesses are scope limitations in my own research — things I did not audit, corrections other agents surfaced.

If any advocate's v1 plan contradicts a §5 ground-truth constraint from `validation.md`, that contradiction is the arbiter's problem. My job is to make the contradictions visible.

---

## Head-to-Head Scorecard: Fidelity to Research Findings

Seven criteria, each grounded in a specific Phase 1 finding or `validation.md` §5 constraint. Scoring scale: **Strong** (fully respects the finding, often sharpens it), **Adequate** (respects the finding but does not elevate it), **Weak** (partially contradicts or under-weights the finding), **Contradicts** (false claim against the evidence).

Self-scored honestly as **backbone-researcher**: I include myself because the arbiter reads all scorecards side-by-side, and my scope limits (§ Conceded Weaknesses) mean I should not claim Strong everywhere.

| Criterion | Weight | backbone-researcher | build-our-own-advocate | litellm-hybrid-advocate | a2a-future-advocate |
|---|---|---|---|---|---|
| **1. Respects subprocess-CLI-JSON as the de facto backbone** (Phase 1 §7, §10; validation §5.1) | High | Strong — original finding | Strong — `SubprocessProvider` base class is the architecturally correct response; `claude-agent-sdk` dropped from v1 | Strong — "five of six agent runtimes are subprocess-spawn-a-CLI" conceded; ships `SubprocessProvider` | Strong — conceded "subprocess providers are the v1 baseline" and does not reopen |
| **2. Correctly separates A2A from Zed/JetBrains ACP** (Phase 1 §6; validation §5 implicit) | High | Strong — original correction | Strong — conceded, renames `acp` → `a2a`, splits `zed-acp` as separate lower-priority row | Adequate — acknowledges the confusion in their cross-review §2 but does not propagate into their v1 artifact list | Strong — explicit concession, credits backbone, treats as "joint ratification" |
| **3. Does not promise an A2A provider in v1 without a named counterparty** (Phase 1 §9; validation §5.2) | High | Strong — original finding | Strong — `a2a` is "awaiting counterparties"; ship-trigger tied to ≥3 shipping coding-agent wrappers | Strong — "defer A2A to Phase 3 when counterparty wrappers exist" | Strong — conceded Round 1's "bet everything on A2A now"; revised position defers client provider to Phase 3 and ships pioneer wrapper as separate post-v1 artifact |
| **4. Respects that MCP is tools, not dispatch** (validation §5.3) | Med | Strong — original finding | Strong — no MCP-as-dispatch confusion; MCP remains tool-use inside agents | Strong — same | Strong — same |
| **5. Does not under-estimate per-provider LoC cost** (Phase 1 §2.3, §4; partially rebutted in my own revision) | Med | Adequate — my original 400–800 LoC estimate was right in aggregate but misattributed to per-adapter instead of base-class substrate; corrected in Phase 3 revision | Strong — adopted the refactoring (`SubprocessProvider` base ~300–400 + per-tool subclasses ~100–150, total v1 ~800–1,200 LoC); explicitly conceded their "100–200 lines per adapter" was ~2x low | Strong — accepted the SubprocessProvider factoring; revised timeline 4–5 weeks for SKILL.md parity | Adequate — conceded Round 1 "thirty lines" wrapper estimate was wishful; revised to "300–600 lines" per researcher's number |
| **6. Addresses cold-start amortization** (Phase 1 §11 obs. 10; validation §5.5) | Med | Strong — original finding | Strong — moves `opencode` into v1 specifically to validate long-lived-process transport; acknowledges subprocess pooling is future work | Adequate — flags need for pooled-subprocess provider; no v1 deliverable addressing it | Strong — proposes standalone `conversus-a2a-claude` as long-lived HTTP server specifically to amortize cold start; explicit post-v1 roadmap |
| **7. Acknowledges no unifying library exists** (Phase 1 §0, §7; validation §5.4) | High | Strong — original finding | Strong — "no wheel exists" is the load-bearing claim of their Phase 1 and was verified by me | Strong — explicit concession: "the 'no wheel exists' argument is correct"; protocol is conversus IP, not LiteLLM-shaped | Strong — "protocol is conversus IP" is accepted in revision; A2A is an adapter behind it, not a replacement |

### Weighting Rationale

- **Criteria 1, 2, 3, 7** are weighted **High** because they correspond directly to the §5 ground-truth constraints in `validation.md`. Any ruling that contradicts these is subject to automatic rejection under §7 of the validation document ("The winning architecture is **rejected or referred back** if any §5 ground-truth constraint is contradicted").
- **Criteria 4, 5, 6** are weighted **Medium** because they are downstream implications of the High-weight findings and matter for the implementation plan, but an advocate can partially miss them without violating a hard constraint.
- **Criterion 7** gets High weight even though it is a meta-finding, because it is load-bearing for every subsequent decision: if a unifying library existed, the whole deliberation would collapse to "just use that library."

### Observations from the scorecard

- **Every advocate now scores Strong or Adequate on every criterion.** This is the single most important result in the deliberation: the adversarial process worked. No surviving position contradicts a ground-truth finding. The disagreement has collapsed from "which architecture is correct" to "which v1 scope is correct within a shared architecture."
- **The only Adequate (not Strong) ratings are me on #5 (scope limit) and litellm-hybrid on #2 and #6.** Litellm-hybrid's #2 Adequate is because their Phase 3 revision does not carry the A2A-vs-ACP spec rename into their deliverable list — they accept the terminology fix but leave it to the spec amendment rather than naming it in their v1 scope. Their #6 Adequate is because they acknowledge cold-start as a concern but ship no v1 deliverable against it.
- **Build-our-own and a2a-future score identically Strong on all High-weight criteria.** This is not a coincidence — both advocates converged on the same architectural shape (conversus-owned protocol, subprocess v1, A2A as forward work) during the adversarial process. The remaining disagreement between them is about one additional standalone artifact (`conversus-a2a-claude`), which is not an architectural difference.
- **None of my findings was successfully contradicted by any advocate.** Four were ratified verbatim, three were sharpened by advocates (who factored them into architectural patterns I did not explicitly draw), and one was corrected on a minor date (A2A merger August 2025, not September).

---

## Conceded Weaknesses

These are scope limitations of my research. I list them because the arbiter should not attribute my authority to claims outside my scope, and because I want the deliberation record to be honest about what I did and did not verify.

1. **I did not audit the conversus test suite.** Build-our-own's claim that the `mock` provider "stabilizes 3,428 tests" was not verified by me. Build-our-own themselves downgraded the framing in Phase 3, but the count remains un-measured. I was not the right person to measure it; the monorepo's conversus submodule has its own agent for internal code claims.
    - **Raised by**: self, in my own Phase 2 cross-review of build-our-own §7.
    - **Severity**: Minor. Does not affect any §5 ground-truth constraint. Any v1 plan that treats `mock` as a test-infrastructure foundation is making an implicit claim the advocates have not measured.

2. **I did not measure actual subprocess cold-start with `--bare` across all six CLI tools.** My "1–3 second cold start" figure is based on public documentation, release notes, and two measurements on Claude Code in my own environment. I did not replicate the measurement on Aider, Copilot CLI, Codex CLI, Gemini CLI, or Continue `cn`. The order of magnitude is likely correct; the exact number is not per-tool verified.
    - **Raised by**: self, in Phase 1 §11 obs. 10 with explicit caveat.
    - **Severity**: Moderate. The constraint in `validation.md` §5.5 is "cold start is real and un-amortized," which is met even at the low end of my range. The exact figure would matter if an advocate were pricing a specific latency budget; none of the three does.

3. **I had the A2A merger date right (August 2025) but my original `tool-landscape.md` reference document cited "September 2025" in one place.** A2a-future-advocate flagged this. I corrected it in my Phase 3 revision.
    - **Raised by**: a2a-future-advocate §6 citations table.
    - **Severity**: Minor. Zero impact on substantive claims. The canonical date per the LF AI blog is 2025-08-29.

4. **I did not verify LiteLLM's release cadence, test suite size, or production usage beyond published facts.** Litellm-hybrid cited "41,900 stars, multi-release-per-month cadence, Stripe and OpenAI in production." I cross-checked the star count and the release cadence via GitHub's public API but did not independently verify the production-use claim.
    - **Raised by**: self, in my Phase 2 cross-review of litellm-hybrid §7.
    - **Severity**: Minor. Litellm-hybrid's claim is consistent with public information; I just cannot confirm the production-use specifics. All three advocates and I accept LiteLLM's operational posture as a shared working assumption.

5. **I did not survey the Copilot CLI headless surface completely.** My Phase 1 §12 flagged this as an under-documented area. No advocate closed the gap. Build-our-own's cross-review §5.5 downgraded `copilot` to "exploratory — verify headless surface before committing."
    - **Raised by**: self, in Phase 1 §12 and Phase 3 revision risks section.
    - **Severity**: Moderate for any v1 plan that includes `copilot`; near-zero for the three actual Phase 3 plans (none ships `copilot` in v1).

6. **I did not verify the end-to-end composition of "LiteLLM proxy in front of subprocess tools."** Litellm-hybrid's cross-review §4.2 claims this works for Aider, Continue, Codex via `OPENAI_BASE_URL`. The claim is theoretically sound based on each tool's documented OpenAI-compatible mode, but I did not exercise the composition in practice.
    - **Raised by**: self, in Phase 3 revision risks section.
    - **Severity**: Minor. It is a post-v1 enhancement pattern, not a v1 dependency.

7. **My research is a 2026-04 snapshot.** The A2A coding-agent ecosystem finding ("empty") is accurate as of 2026-04-03. By the time synthesis ships, it may have changed (a community wrapper, a vendor announcement, an A2A hackathon outcome). I commit to updating the findings if contradicted by new evidence.
    - **Raised by**: self, proactively.
    - **Severity**: Inherent to any tool-landscape research. The arbiter should treat the findings as "correct at 2026-04" and build re-verification into the v1 implementation timeline.

---

## Surviving Advantages

The findings that survived cross-review either unchallenged or challenged-and-held. Each is cited with which advocate ratified it.

### Unchallenged findings (not attacked by any advocate)

1. **`claude-agent-sdk` is itself a subprocess wrapper around the bundled `claude` CLI binary, not a library API.** Going Python → Node SDK → CLI is strictly worse than Python → CLI directly.
    - **Ratified by**: Build-our-own (§4.1 of their Phase 3 revision, drops `claude-agent-sdk` from v1 entirely), litellm-hybrid (§2.1, cites as "what the research refutes"), a2a-future (§4.2, cites in explaining wrapper cost).
    - **Phase established**: Phase 1 §1.2, §11 obs. 8.

2. **The `Agent` tool in SKILL.md is not a protocol and is not portable.** It is addressable only from inside a live Claude Code session. This is the entire motivation for spec 042 existing.
    - **Ratified by**: All three advocates. Build-our-own (§1.3 of Phase 3 revision, "the factual basis for spec 042 existing at all"). Litellm-hybrid (§2.1, "LiteLLM does not help with the Claude Code agent loop"). A2a-future (treated as given).
    - **Phase established**: Phase 1 §1.4, §11 obs. 1.

3. **OpenCode is architecturally distinct from other coding agents — it is the lone HTTP-first exception with `opencode serve` and OpenAPI 3.1.** ~100 lines of `httpx` against the OpenAPI spec is sufficient for integration.
    - **Ratified by**: Build-our-own (Phase 3 revision moves `opencode` into v1 provider set in direct response), litellm-hybrid (§3.3 table acknowledges as third transport), a2a-future (§3.3 cites as near-term alternative to A2A).
    - **Phase established**: Phase 1 §2, §11.

### Attacked and held (cross-review surfaced critique, finding survived)

4. **The two-ACP problem — spec 042 §11 conflates Google/IBM A2A (headless HTTP) with Zed/JetBrains Agent Client Protocol (IDE stdio).** These are different wires, different threat models, different use cases.
    - **Attack**: Treated initially as a minor terminology nit by all three advocates in Phase 1.
    - **Defense**: Cross-review surfaced that the conflation produces real v1 scoping errors — a2a-future-advocate explicitly built their Round 1 position on the ambiguity and conceded the error in Phase 2.
    - **Status**: Upgraded from "minor nit" to "mandatory spec fix" by adversarial process. All three advocates ratified in their Phase 3 revisions.
    - **Phase established**: Phase 1 §6. Phase 2 ratification: build-our-own cross-review §1.6, litellm-hybrid cross-review acknowledgment, a2a-future explicit concession §1.1.

5. **No shipping coding agent exposes an A2A server in 2026-04.** Protocol v1.0.0 released 2026-03-12 (three weeks before Phase 1). `a2a-sdk` Python is 0.3.25 stable / 1.0.0a0 alpha. No Anthropic/Claude Code / GitHub Copilot / Aider / OpenCode / Codex / Gemini CLI reference. Framework integrations exist only in Google ADK, LangGraph, BeeAI — none of which are the coding agents conversus would dispatch to.
    - **Attack**: A2a-future-advocate's Round 1 position depended on treating A2A as a near-term v1 deliverable.
    - **Defense**: A2a-future-advocate conceded in their Phase 2 cross-review §1.2 ("the researcher is right") and pivoted their Phase 3 revision to "ship subprocess v1, A2A client deferred to Phase 3, standalone `conversus-a2a-claude` wrapper as post-v1 pioneer artifact."
    - **Status**: The single most factually decisive finding in the deliberation. Forced a revision of the A2A advocate's entire implementation plan.
    - **Phase established**: Phase 1 §9. Phase 3 ratification: a2a-future-advocate's Position Summary, "my Round 1 thesis is dead."

6. **Cost estimates for per-provider adapters were understated by the advocates; the researcher's aggregate estimate was correct; the correct factoring is a `SubprocessProvider` base class, not per-adapter duplication.**
    - **Attack**: Build-our-own's Phase 1 cited "100–200 lines per adapter." My Phase 2 cross-review argued the production `claude-code` subprocess adapter is 400–800 LoC.
    - **Defense**: Build-our-own accepted the correction and responded with a better architectural factoring (shared `SubprocessProvider` base absorbs the substrate once). I accepted the factoring as architecturally superior in my Phase 3 revision. The aggregate cost is ~800–1,200 LoC for v1, which all three advocates now agree on.
    - **Status**: The adversarial process improved the architecture. The finding that was attacked (per-adapter cost) survives in the aggregate; the factoring (base class) is a joint product of the deliberation.
    - **Phase established**: Phase 1 §1, §3, §5.2, §10. Phase 2 correction by me. Phase 3 ratification by build-our-own §1, accepted by litellm-hybrid in their Phase 3 revision.

### Ratified competitor concessions I benefit from

7. **All three advocates agree on the seven-point consensus from my Phase 3 revision's "Convergence" section**: spec 042 terminology fix, MCP is tools not dispatch, subprocess CLI is the portable baseline, OpenCode deserves an HTTP provider, A2A is the right long-term protocol, A2A coding-agent ecosystem is empty in 2026-04, `claude-agent-sdk` Node-bridge framing is misleading. **Seven joint-ratified facts — none of them contested in any Phase 3 revision.**
    - **Phase established**: Emerged during Phase 2 cross-reviews; ratified in all three Phase 3 revisions.

---

## Why The Arbiter Must Respect The Facts

### 1. The core decision

The arbiter is ruling on architecture. The architecture must pass the validation battery in `validation.md`. The validation battery is grounded in these findings. A ruling that contradicts a §5 ground-truth constraint is not a ruling on architecture — it is a ruling against evidence, and under `validation.md` §7 the winning architecture is "rejected or referred back if any §5 ground-truth constraint is contradicted." This is not my personal preference. It is the acceptance-criteria document the arbiter cited in their Phase 6 instructions.

The good news for the arbiter: **after three rounds of adversarial testing, none of the three surviving positions contradicts any §5 constraint.** Any of the three advocates' Phase 3 revisions can pass the validation battery, because each one has absorbed the ground-truth findings into their revised plan. The adversarial process did its job. The arbiter's decision is about v1 scope and emphasis — a legitimate engineering tradeoff — not about correctness.

### 2. The risk calculus

What does the arbiter risk by contradicting a ground-truth finding?

- **If the ruling promises an `a2a` provider in v1 without naming a shipping counterparty**: spec 042 ships with a dead row in the matrix. Users cannot use it. The roadmap advertises a capability that does not exist. Spec 048's governance CI gates have a config field (URL-addressable agents) that cannot be exercised. Six months after ship, the team either writes their own A2A counterparty (the "pioneer wrapper" path a2a-future-advocate revised toward) or removes the provider in a user-visible break. This is the exact mistake a2a-future-advocate made in Phase 1 and corrected in Phase 3. The arbiter should not repeat it in Phase 6.

- **If the ruling treats `claude-agent-sdk` as a library integration rather than a subprocess wrapper**: the `claude-code` provider has a phantom option in its implementation plan (Python → Node SDK → CLI) that is strictly worse than the direct subprocess path. The engineering team picks it because the spec describes it as a real option, discovers the added failure modes, and reworks during implementation. This is wasted work that the adversarial process has already eliminated.

- **If the ruling conflates A2A with Zed/JetBrains Agent Client Protocol**: the provider matrix has one row where it should have two, with wildly different priorities (A2A is forward-work for headless dispatch; Agent Client Protocol is out of scope for spec 042 entirely and belongs in a future IDE-integration spec). The conflation propagates into spec 048's registry schema, into the provider lifecycle, and into the conversus documentation. Every downstream reader of the spec inherits the error.

- **If the ruling under-estimates subprocess LoC cost**: the team ships v1 late, blames the estimate, and the spec 048 timeline slips. Build-our-own absorbed this correction in Phase 3 with the `SubprocessProvider` base class factoring. The arbiter should not reverse that decision.

- **If the ruling ignores cold-start amortization**: spec 048's CI governance scenarios hit a latency ceiling within months. Every PR triggers 30–150 subprocess spawns. The team either pools workers (protocol change, breaking) or tells users their governance runs take 5 minutes instead of 30 seconds. Neither is acceptable. The advocates have priced this in; the arbiter should, too.

### 3. The practical path

The arbiter should flag any ruling against the following:

- **Flag if**: the winning v1 scope includes an `a2a` provider with no named counterparty and no explicit "awaiting counterparties" status field.
- **Flag if**: the winning v1 scope depends on `claude-agent-sdk` rather than direct `claude -p --bare` subprocess invocation.
- **Flag if**: the winning spec 042 §11 matrix still uses "ACP" as an umbrella term or keeps a single `acp` row.
- **Flag if**: the winning cost estimate for subprocess providers (aggregate v1 LoC) is below ~800 lines, or above ~1,400 lines, without explicit justification.
- **Flag if**: the ruling treats MCP as an execution provider rather than as in-agent tool access.
- **Flag if**: the ruling does not address subprocess cold-start amortization either as documented accepted cost or as a pooling hook.
- **Flag if**: the ruling treats any claim as "backbone-researcher said so" outside the seven-point consensus — my scope is external tools, not conversus-internal numbers, not LiteLLM release cadence, not Copilot CLI headless details. Internal-codebase claims need advocate-level sourcing.

This list is not exhaustive and it is not the final arbiter ruling — it is the set of factual tripwires built into the adversarial record. If the ruling clears all seven tripwires, the ground-truth findings are respected, and the deliberation's factual foundation is preserved regardless of which advocate wins.

### 4. The honest ask

I am asking the arbiter to do three things:

1. **Treat the seven-point joint-ratified consensus** (in my Phase 3 revision's "Convergence" section, carried forward by every advocate) as settled fact for Phase 6 purposes. Do not re-litigate it in the ruling. Cite it, move on.

2. **Score the advocates on fidelity to the findings**, not on rhetorical polish. The scorecard above is my honest accounting; the arbiter should produce their own and compare. All three advocates are Strong or Adequate across the criteria — the decision is genuinely about v1 scope, not correctness.

3. **Acknowledge the 2026-04 snapshot limit.** The findings are ground truth as of the date they were gathered. If new evidence arrives before synthesis (a community A2A wrapper announcement, a shipping vendor integration, a protocol revision), the findings should be updated and the advocates allowed to revise. I commit to updating `tool-landscape.md` if contradicted. The deliberation should inherit that commitment.

What I am not asking: I am **not** asking the arbiter to pick me, to tilt toward build-our-own, to tilt toward litellm-hybrid, or to tilt toward a2a-future. My scope is factual witness. The arbiter picks the architecture; I just insist the architecture pass the validation battery that the facts underwrite.

---

## Closing — factual posture for synthesis and arbitration

Every surviving Phase 3 position is consistent with every Phase 1 finding. The adversarial process worked. The advocates converged on a shared architecture (conversus-owned `ExecutionProvider` protocol, subprocess-CLI-JSON backbone with optional HTTP transport, A2A deferred with a named trigger condition, LiteLLM as recommended Tier-3 implementation) and differ only on which three-or-four providers ship in the first release.

The decision is an engineering tradeoff between three legitimate v1 scopes:
- **Build-our-own**: `mock + anthropic + claude-code + opencode` (four providers, two substrates validated, parallel `anthropic` native adapter as reference).
- **Litellm-hybrid**: `mock + claude-code + litellm` (three providers, LiteLLM absorbs Tier-3 without a parallel native adapter).
- **A2a-future**: build-our-own's v1 scope plus a post-v1 commitment to `conversus-a2a-claude` as a standalone pioneer artifact and a forward-compatible `.conversusrc` schema.

Each of these v1 scopes is consistent with the facts. Each passes the §5 ground-truth constraints in `validation.md`. The arbiter's job is to pick the v1 scope that makes spec 048 and the downstream roadmap easier, not to pick the position that best reflects the facts — they all reflect the facts now.

If the arbiter respects the facts, the ruling will be defensible. If the arbiter contradicts any §5 constraint, the ruling will be vulnerable to rejection under `validation.md` §7. That is the arbiter's risk budget.

My role is complete. I report ground truth, I do not pick winners, and I stand by the seven-point consensus that survived contact with adversarial cross-review.
