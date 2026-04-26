# Constitutional Conversations

A chronological log of every conversus deliberation that produced — or
proposed — a change to `CONSTITUTION.md`. The constitution is the
governance contract; this file is its **governance log**.

## What this file is for

The constitution embeds a `Sync Impact Report` HTML comment at the top
of `CONSTITUTION.md` summarizing the most recent version bump. That's
useful for "what's the latest?" but invisible for:

- Deliberations whose proposed amendments were **deferred** (rejected
  or held until more evidence accrues)
- Deliberations that ruled on **clarifications** to existing principles
  (PATCH bumps that don't add principles)
- The **why** behind a version bump, beyond the one-line version diff
- The **PR-evidence chain** that justified each constitutional change
- The **cross-references** between deliberation outputs, spec files,
  and the resulting CONSTITUTION.md sections

A constitution without a governance log accumulates principles whose
provenance fades. Five years from now, "Why does Principle VII say X?"
should resolve to a deliberation, a set of PRs, and a ruling — not
"git blame says Brian wrote it on a Tuesday."

This file is the resolution.

## When to add an entry

Add an entry whenever any of these happen:

- A `conversus run` completes against `CONSTITUTION.md` (as target,
  grounding, or arbiter source).
- A spec proposes a constitutional amendment — even before it's run
  through deliberation.
- An amendment lands (`CONSTITUTION.md` version bump, no matter how small).
- A proposed amendment is **rejected** or **deferred** with reasoning.
  These leave no trace in `CONSTITUTION.md` itself; this file is where
  they live so the next person doesn't re-propose the same thing
  without knowing why it was rejected before.

## Entry format

Each entry is a level-2 heading with date + slug. Required fields:

- **Date** (ISO 8601, the day the deliberation completed or the
  amendment landed)
- **Type** (`Deliberation` / `Amendment` / `Proposal` / `Rejection`)
- **Trigger** (one sentence on what motivated this — e.g., "10 PRs
  merged since last review")
- **Mode + Agents + Rounds** (for deliberations)
- **Outputs path** (link to the deliberation directory in
  `deliberations/`)
- **PRs / specs referenced** (cross-references)
- **Outcome** (what changed or didn't, with status: `accepted`,
  `deferred`, `rejected`)
- **Status** (`open` while still being actioned, `closed` once all
  follow-up work has landed)

Keep entries terse — full context lives in the linked artifacts.
This file is an index, not a transcript.

---

## 2026-04-25 — Constitutional gap analysis since v2.2.0

**Type**: Deliberation
**Trigger**: 10 PRs merged since the v2.2.0 bump (5 SKILL.md
decomposition principles). The v2.2.0 sync impact report explicitly
left a follow-up TODO: *"Add a constitution-grounded agent to future
conversus deliberations reviewing decomposition changes."* Overdue.

**Mode**: cooperative
**Agents (4)**: governance, packaging-distribution, runtime-safety, testing-quality
**Rounds**: 2 of 2 configured (`stagnation: detect` did not fire; round 2 ran because round 1 produced unresolved disputes)
**Termination**: converged
**Arbiter**: subject arbitration grounded in `CONSTITUTION.md`, `trigger: always`, `timing: final`, `influence: binding`
**Provider**: claude-code (host CLI subscription)
**Cost**: ~52 LLM launches across all phases + arbitration

**Outputs**: [`deliberations/constitution-gap-analysis-2026-04-25/`](deliberations/constitution-gap-analysis-2026-04-25/)
- Cross-round synthesis: `summary/final.md`
- Final arbitration: `round-2/arbiter/resolution.md`
- 48 per-agent phase artifacts across rounds (4 reviews + 12 cross-reviews + 4 revisions + 4 disputes per round, ×2 rounds), plus per-round synthesis files, the cross-round synthesis, the arbitration resolution, and the seed inputs (`recent-changes.md`, `conversus.yml`). See the directory tree for the canonical count.

**PRs informing the deliberation** (the "what changed" record):
PR #4 (spec 064.1 runtime registration), #5 (claude-code tool-use response),
#6 (anthropic 429 retry + concurrency), #8 (token tracking + live tests),
#9 (claude-code JSON parser), #10 (red-blue contract break),
#11 (mcp_server.py wheel inclusion), #12 (prompt tests),
#13 (manifest version sync), #14 (CONVERSUS_DISABLED_TOOLS).

**Specs referenced**: spec 052 (open source extraction), spec 053 (public CI),
spec 054 (public docs), spec 055 (capability registry), spec 064 (capability discovery).

**Outcome — proposed v2.3.0 amendment package** (arbiter binding rulings):

*Stage 1 — Unanimous P1 (4 new principles)*:
1. **Distribution Surface Integrity** — single-source versioning, force-include discipline for non-package modules, end-to-end install testing.
2. **Provider Robustness Contract** — token reporting, retry-with-jitter, protocol tolerance, structurally-valid response handling.
3. **Safety-Critical Defense-in-Depth** — schema → parser → contract test pattern, scoped to **both** synthesis verdicts AND provider protocols (arbiter ruled testing-quality's broader scope over runtime-safety's narrower one).
4. **Live Test Cost Discipline Framework** — `@pytest.mark.live` markers, justification, CI opt-out.
   Plus extension of Principle IX to include **behavior-over-shape testing** as a general principle that domain-specific testing references (arbiter ruled testing-quality's framework approach over packaging-distribution's domain-specific approach).

*Stage 2 — Majority P2*:
- Meta-Testing for Parametrized Capabilities (foundational P1, but in stage 2 per priority hierarchy ruling)
- Registry-First Declaration (Principle XI extension)
- Standalone Operator Configuration Principle (arbiter ruled standalone over Principle XV extension)
- Retry-with-Jitter Standard Pattern, Token Consumption Transparency, Protocol Tolerance, Contract Test Coverage, Test Category Taxonomy.

**Status**: `open` — implementation in flight

**Follow-up actions**:
- [x] Draft `spec 066-constitution-v2.3.0` operationalizing the amendment package as concrete CONSTITUTION.md edits with sync impact report. — PR #17, merged 2026-04-25 (with reviewer-driven wording fixes)
- [x] Apply v2 to `spec 065-path-to-open-source` referencing the new principles (Distribution Surface Integrity affects gates G2/G9; Provider Robustness affects G5/G6). — PR #15, merged 2026-04-25
- [ ] Implementation PR — apply spec 066's wording to `CONSTITUTION.md` itself (Sync Impact Report bumped to v2.3.0, principles XXII-XXVII appended, IX + XI extended). — IN FLIGHT
- [ ] Run a verification deliberation against the proposed v2.3.0 text before the implementation PR merges — the arbiter already grounded the rulings in v2.2.0; the *amended* constitution should pass its own arbitration before landing. Acceptance bar per spec 066 §7: 0 disputes raised.
- [ ] Phase 1 (manifest tools[] from CAPABILITIES) operationalizes Principle XXII — PR #18, awaiting CI auto-merge.

**Self-referential observation from the deliberation**:
> *"Future constitutional deliberations should focus on systematic
> evidence collection before the deliberation rather than extending
> round counts for coordination disputes."*

The agents converged fast on evidence-grounded amendments (PRs #5–#14
provided clear failure patterns) and stalled on coordination disputes
(priority classification, structural boundaries — testing-quality vs
packaging-distribution on whether "behavioral validation" was domain-
specific or general). Apply this lesson to the next constitutional
review: bigger PR record, fewer rounds, sharper seed framing.
