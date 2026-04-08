# Blog Posts — To Write

Running catalog of stories from conversus development that deserve a writeup.
Add new entries at the top. Each entry captures the hook, the beats, and why
it matters so the draft doesn't have to reconstruct the story later.

---

## Draft queue

### 0. "We were sleeping on VSCode"
**Status**: story just-happened, ready to write (spec 049 origin, 2026-04-05)
**Hook**: The spec 042 deliberation just ruled on how conversus dispatches
TO other agent runtimes (Claude Code, OpenCode, etc.). Within 30 minutes
of the ruling, a different question surfaced: how do other agent runtimes
dispatch IN to conversus? The answer was hiding in plain sight.

**Beats**:
- The 042 ruling landed. Next step: update downstream specs and move to
  implementation. The orchestrator (me) proposed a parallel track: "ship
  conversus to Cursor, VSCode, Copilot, Claude Code" as a new spec 049,
  with all four hosts treated as parallel targets in a rough matrix.
- The user's three-word intervention: **"we are sleeping on vscode."**
- The reframe that followed: VSCode is not one of four hosts. It's the
  *dominant* host for conversus's target audience, for three reasons that
  all converge:
  1. **Audience overlap**: VSCode has the largest professional developer
     user base, and every feature in the post-042 roadmap targets
     professional developers. Spec 048 (governance gates in CI) is a
     GitHub feature. Microsoft owns both VSCode and GitHub. The audience
     for 048 IS the VSCode audience.
  2. **Multi-agent reach inside one host**: VSCode is where every agent
     tool lives — Copilot, Cline, Continue, Roo Code, Augment, Cursor
     (which is VSCode), plus the JetBrains/Zed refugees who use VSCode
     for certain workflows. Shipping to VSCode reaches all of them
     simultaneously via MCP (which every one of those agents now speaks).
  3. **Extension API vs skill format**: MCP lets hosts *invoke* conversus.
     The VSCode extension API lets us *render* conversus — sidebar panels,
     command palette, status bar, inline diagnostics on governance
     violations. A skill file can't do that.
- The 2-for-1 realization: an MCP server + a VSCode extension is actually
  a 2-for-1. The MCP server reaches every MCP-speaking host (Copilot,
  Cline, Continue, Roo Code, Augment, Cursor inheriting from VSCode). The
  VSCode extension reaches VSCode-and-forks with rich UX. Together they're
  the universal distribution mechanism. Separately they'd leave gaps.
- The spec 040 tension surfaced and resolved: is the Command Center
  actually a VSCode extension? The user's answer: "leave 040 as is."
  Correct call — Command Center targets non-technical stakeholders who
  don't use VSCode. The VSCode extension targets developers. Same data,
  different audiences, different rendering.
- The paid-tier gating rule: "MCP is paid if they are accessing paid
  features." Clean. Free tools succeed with the base install. Paid tools
  return a structured `PAID_TIER_REQUIRED` error without the paid package.
  Per-tool gating, not per-install gating — so free users see the full
  tool surface, they just get a clear error when they invoke a paid tool.
- The spec 049 draft emerged in one pass: 13 sections, 21 functional
  requirements, 9 success criteria, phasing coordinated with spec 042 so
  both ship in the same sprint window.

**The three-word observation that reshaped the roadmap**: "we are sleeping
on vscode." That's the whole story in six syllables. I had VSCode in the
matrix as a parallel target. The user had it as the primary target. The
difference between those two framings is the difference between "ship
something to every host, eventually" and "ship the right thing to the
right host, now."

**Why it matters**: Two lessons.
1. **Strategic weight doesn't come from presence in the list.** I had
   VSCode on the list. It was still being under-weighted because I hadn't
   reasoned about *why* it mattered — I'd just enumerated it. The user's
   intervention was a weight correction, not an addition.
2. **The best specs get written in the 30 minutes after a big decision,
   not the 30 days before the next one.** Spec 049 didn't exist an hour
   before it was drafted. It emerged because the 042 ruling exposed what
   *wasn't* in the plan. This is the "capture velocity" argument for
   keeping a blog_posts.md and writing specs the moment the gap is
   visible, not weeks later when the context has decayed.

**The close parallel**: the 042 deliberation and the 049 spec draft are
mirror images of each other. 042 is outbound dispatch (conversus → N
providers). 049 is inbound dispatch (N hosts → conversus). They compose
into a complete universal tool: run anywhere, invoke from anywhere.
Neither one is complete without the other. And neither one was complete
in my head until the user said six syllables and forced the reframe.

---


**Status**: story complete, ready to write (spec 042 deliberation, 2026-04-03 → 2026-04-05)
**Hook**: We used conversus to decide conversus's own execution provider
architecture. Four agents, winner-take-all, binding arbiter, 26 agent runs
across six phases in a single round. By Phase 3, all three advocates had
absorbed each other's positions into a shared architecture. By Phase 6, the
arbiter had bolted 14 binding conditions onto the winner's plan. The
deliberation WAS the test case — and it converged cleanly in one round.

**Beats**:
- **The setup**: spec 042 needed an architectural decision (build own vs
  LiteLLM hybrid vs A2A future). Instead of picking, we ran a deliberation.
  The config seeded a `backbone-researcher` agent whose job was NOT to
  advocate — just to establish ground truth about what production tools
  actually use. Three advocates, one factual witness, one binding arbiter.
- **Phase 1 — the factual bombshells that reshaped the debate**: the
  backbone-researcher's opening review established three findings that
  none of the advocates could work around:
  - Claude Agent SDK is itself a CLI subprocess wrapper around the `claude`
    binary, not a rich SDK. The whole "we get the SDK for free" framing died.
  - Google/IBM A2A and Zed/JetBrains Agent Client Protocol are *different*
    protocols — spec 042 had been conflating them for months. The ACP row
    in the v1 matrix was actually two rows pretending to be one.
  - No major coding agent (Claude Code, Aider, Copilot, Codex, Gemini,
    OpenCode) has been wrapped as an A2A server as of 2026-04. The A2A
    ecosystem was empty at the counterparty layer — "one provider, every
    tool" was a promise with no counterparties.
- **Phase 2 — the cross-review landslide**: 12 cross-reviews, 4 agents ×
  3 opponents each. The LiteLLM advocate's 70/30 split died here: the
  backbone-researcher pointed out that LiteLLM covers model APIs but not
  the Claude Code CLI agent loop, so the "30%" (agent runtimes) is
  actually 75% of the work. The A2A advocate's "one provider, every tool"
  died here too: no counterparty ecosystem means the advocate was
  proposing to write every wrapper themselves AND the HTTP lifecycle
  scaffolding — strictly more code than the direct providers they were
  attacking.
- **Phase 3 — the convergence**: this is the quiet beat that's easy to
  miss but it's the most important one. All three advocates updated
  their positions based on what they'd learned in Phase 2. The
  build-our-own advocate absorbed the LiteLLM position outright: "my plan
  now includes LiteLLMProvider as a v1 optional companion." The LiteLLM
  advocate retired the word "hybrid" and narrowed their disagreement to
  a single adapter file (300 lines — ship LiteLLM instead of a hand-rolled
  AnthropicProvider). The A2A advocate pivoted from "ship A2A first" to
  a partial-incorporation ask with three specific claims: protocol shape,
  pioneer wrapper, spec 048 URL entries.
- **Phase 4 — the scorecard moment**: head-to-head scorecards forced
  each advocate to publicly score their competitors on shared criteria.
  The LiteLLM advocate played a tactical move: "the template says
  silence-is-concession, and my 'LiteLLM proxy mode fronting subprocess
  tools' claim has been unchallenged through 6 cross-reviews and 3
  revisions — by the formal rules, I've already won this point." The
  backbone-researcher reframed their role as the "judge's factual
  witness" instead of competing for winner status — a clean solution
  to the non-advocate problem.
- **Phase 5 — the verdict**: build-own wins 127/140, LiteLLM runner-up
  at 113/140 (10% margin), A2A eliminated at 94/140 with partial
  incorporation honored. The judge invoked the "tiebreaker is risk"
  rule: on the close call of "AnthropicProvider alongside LiteLLM"
  vs "LiteLLM replaces it," the judge reasoned that shipping *both*
  is cheap insurance — the cost of being wrong is asymmetric (ship
  less than enough → user-visible break; ship more than enough → 300
  lines of dead code that can be removed later).
- **Phase 6 — the arbiter's bolt-on**: conversus-chief-architect (the
  subject arbiter) affirmed the verdict but added 14 binding conditions.
  Seven from the validation battery, three from the a2a-future advocate's
  partial-incorporation asks, four from operational knowledge the judge
  couldn't see (LiteLLM supply-chain resilience, free-tier API-key-less
  user story, SubprocessProvider base class, `.conversusrc` URL schema).
  Affirm-with-conditions is the ideal outcome — the verdict holds, AND
  the arbiter's operational knowledge lands as concrete implementation
  requirements.
- **The meta moment that matters**: the deliberation produced a better
  architecture than any single author would have designed. Before it
  started, we had three plausible positions and no way to pick. After it
  ended, we had one plan with 14 binding conditions, three partial
  incorporations from the losing position, ratified terminology fixes
  (ACP → A2A + zed-acp), and a validation battery of 28 tests the winner
  must pass. That plan is *strictly better* than any of the Phase 1
  positions — including the winner's own opening argument.

**The tactical moments worth highlighting in the post**:
1. **Silence-is-concession**: the LiteLLM advocate caught an unchallenged
   claim and cashed it in by citing the template rule explicitly. Shows
   that formal deliberation rules create real incentives.
2. **The scope-limited witness**: the backbone-researcher declined to
   "pick themselves" as winner and instead served as the judge's factual
   witness. This is a role that only exists because of the non-advocate
   seat we carved out in the config.
3. **Convergence as a signal**: Phase 3 showed the disagreement narrowing
   from "three incompatible architectures" to "three micro-decisions
   within one shared architecture." That narrowing IS the deliberation
   working — it's the anti-echo-chamber result.
4. **The 10% margin tiebreaker**: close calls get decided by risk
   asymmetry, not by expected value. This is exactly why adversarial
   deliberation beats single-author design on high-stakes decisions.
5. **Affirm-with-conditions**: the three-layer structure (advocates →
   judge → arbiter) exists precisely so the arbiter can say "yes, AND
   here are the things the judge couldn't see." It's better than either
   "override" (destabilizing) or "pure affirm" (wastes the arbiter's
   operational knowledge).

**The 14 binding conditions as narrative climax**:
- Protocol shape A2A-Task-Request-compatible in Week 1 (partial
  incorporation from the losing A2A advocate)
- `conversus-a2a-claude` as post-v1 standalone pioneer artifact
- `.conversusrc::default_agents` URL schema from day 1
- `ProviderError.category` expanded Literal
- Per-agent cost telemetry as structured field
- Duration as structured type (spec 047 compatible)
- SIGTERM handling + subprocess cleanup
- Replay harness: spec 042/045/031 deliberations runnable through the
  new architecture as integration tests
- MCP tool-use preserved inside agent execution
- Secrets never in argv
- 12-agent parallel phase concurrency test
- Free-tier clean-venv install test
- Paid-tier layered install test
- API-key-less free-tier user story (local `claude` binary, zero API keys)

Each of these is a *concrete implementation requirement* that emerged
from the adversarial process — not a handwave, not a "nice to have,"
but a line in a validation battery the winner must pass.

**Artifacts to link in the post**:
- `specs/042-execution-providers/spec.md` (the updated spec with the
  Decision Record block at the top)
- `specs/042-execution-providers/validation.md` (the 28-test battery)
- `specs/042-execution-providers/conversus-output/summary/final.md`
  (Phase 5 judge verdict)
- `specs/042-execution-providers/conversus-output/arbitration/resolution.md`
  (Phase 6 binding arbitration — 14 conditions)
- The individual `review.md`, `revision.md`, `disputes.md` files for
  readers who want to see the debate unfold

**Why it matters**: Demonstrates conversus's actual value prop — not
"multi-agent chat" but "adversarial deliberation as a decision-making
tool when the stakes and blast radius are high." This post is the
proof-of-concept for the tool itself. We used conversus to decide how
conversus dispatches tasks to other agents. The winner's plan was
better than any single author's opening argument. The losing positions
contributed specific artifacts to the winner's plan. The arbiter's
operational knowledge landed as 14 concrete implementation requirements.
This is the "closing the loop" moment — the tool proving its own thesis
by being the decision mechanism for its own design.

**Secondary frame**: the post also proves that adversarial deliberation
can converge in a single round when the factual grounding is strong.
Stagnation detection was configured but never triggered — the
disagreement narrowed monotonically across phases. That's the
meta-result: good research + honest advocates + binding arbiter =
single-round convergence even on high-stakes architectural decisions.

---

### 2. "The test that documented the bug"
**Status**: story ready to write (spec 045 outcome, 2026-04-02)
**Hook**: A test passing doesn't mean the code is right. A test can silently
encode the bug you haven't noticed yet.

**Beats**:
- `errors.py:79-83` had a test asserting that `category` defaulted to
  `"unknown"` when constructor received an invalid value
- Conversus spec 045 deliberation flagged this as "the test documents the
  bug — the test is wrong, not just the code"
- I pushed back initially ("the test passes, coverage is 100%")
- Then I read the test more carefully and saw: it was asserting that
  `ProviderError("mystery")` silently became `category="unknown"`, which
  meant we were *swallowing* typos in production error handling
- Fix: made `category` a `Literal` type, removed the silent fallback, the
  test flipped from "passes with silent corruption" to "fails at construction"
- The "I was wrong" moment: the deliberation was right, I was defending code
  coverage metrics instead of correctness

**Why it matters**: Coverage is a floor, not a ceiling. Tests can encode
bugs. Multi-agent review catches things a solo author's confirmation bias
will defend.

---

### 3. "1350 tests nobody was running"
**Status**: story ready to write (CI gap discovery, 2026-04-02)
**Hook**: We added tests for months. CI said they passed. Then we discovered
CI was running `pytest tests/` — and 1350 tests lived under `engine/tests/`
and `linter/`.

**Beats**:
- Baseline: 1346 tests, 92.97% coverage (reported)
- The moment: ran `pytest engine/tests/ linter/` locally and got a second
  test count CI had never seen
- The fix: one line in `.github/workflows/ci.yml` to add the two missing
  directories
- The constitution amendment: add a rule that CI MUST run all test dirs,
  and a check that fails if a new `tests/` directory appears without being
  added to CI
- The broader lesson: silence isn't safety. "All tests pass" means nothing
  if you're not counting which tests ran.

**Why it matters**: Observability of your own toolchain is as important as
observability of production. CI gaps are invisible by construction — you
only find them when something forces you to count.

---

### 4. "Half-shipped: the spec that made it to 'done' without finishing"
**Status**: story ready to write (spec 006 discovery, 2026-04-02)
**Hook**: `phases.py:661` had a branch that was unreachable at runtime.
Investigation: spec 006 (inter-round arbitration) had been marked "done"
with the kwarg plumbing implemented but the actual dispatch path never
wired up.

**Beats**:
- The dead code smell: static analysis flagged `phases.py:661` as
  unreachable
- The git archaeology: commit M added the branch, commit N added the
  plumbing, commit O marked spec 006 "done" — but the wiring between
  plumbing and branch was never written
- The decision: move spec 006 out of `specs/done/`, mark as "Half-shipped",
  document the gap in `IMPLEMENTATION-GAP.md`
- The meta-question: how many other "done" specs are half-shipped?
- The answer: we added a convention — `done/` means the feature is
  reachable end-to-end, tested, and documented. Anything less stays in
  `specs/` with a status tag.

**Why it matters**: Spec-driven development is only as honest as the
"done" folder. "Done" needs to mean "reachable + tested," not "tasks
checked off."

---

### 5. "Bug #4 and the spec it spawned"
**Status**: story ready to write (spec 047 origin, 2026-04-04)
**Hook**: A one-character regex fix exposed an architectural gap that
became spec 047 (Structured Duration Parser).

**Beats**:
- Bug #4: `_CONSTRAINT_PATTERN` in `linter/question_classifier.py` was
  `\b(month|year|week|day)\b` — missed "3 months" because of the plural
- The fast fix: add `s?` to each unit
- The realization: even after the fix, the classifier returned boolean —
  downstream code couldn't tell "3 months" from "30 years"
- The deeper realization: the regex conflated six different categories
  (deadline, performance, schedule, ttl, window, latency bound)
- The spec: 047 replaces the regex with a structured parser returning
  `TemporalMatch` objects with `Duration` + category
- The cascade: spec 047 unblocks 043 (AMPL time-ranged ZOPA), 046
  (commentator timing references), 048 (governance SLA enforcement), 020
  (scenario storage duration queries)

**Why it matters**: The simplest bug fix can expose the biggest gap.
Fixing the symptom without listening to what the symptom is telling you
is how tech debt compounds.

---

## Ideas (not yet stories)

- **"The package split that took 6 hours and unblocked everything"** —
  spec 032, once `pip install conversus` worked, every downstream spec
  got cheaper
- **"Free vs paid, deliberation vs scoring"** — spec 033's partitioning
  decision and why "deliberation is free, scoring is paid" is the right
  line
- **"The 55-agent review"** — spec 031, 55 domain-specialist reviewers on
  the docs site, what worked and what didn't
- **"Conversus as governance infrastructure"** — spec 048 "CLI that runs
  outside your CLI" vision
- **"Antipatterns as steering"** — spec 010, using a catalog of known
  antipatterns as active constraints on agent behavior

---

## Meta: why we keep this file

Most engineering stories are lost to the commit log. The commit says
*what* changed; the story is *why it mattered* — the wrong turn, the
concession, the meta-lesson. If we don't capture that at the moment it
happens, the blog post a month later is generic.

Add entries aggressively. Prune when they ship.
