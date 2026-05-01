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
- [x] Phase 1 (manifest tools[] from CAPABILITIES) operationalizes Principle XXII — PR #18, merged 2026-04-25 (auto-merge after CI green).
- [x] Implementation PR — apply spec 066's wording to `CONSTITUTION.md` itself (Sync Impact Report bumped to v2.3.0, principles XXII-XXVII appended, IX + XI extended). — PR #19, in review (with XXVII registry-boundary clarification from blind verification).
- [x] Verification deliberations (BOTH self-consistency AND blind methodology) completed 2026-04-25. See entries below.

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

---

## 2026-04-25 — v2.3.0 verification (self-consistency)

**Type**: Deliberation
**Trigger**: spec 066 §7 — re-run arbitration against the proposed v2.3.0 text before the implementation PR merges. Acceptance bar: 0 ACCEPT-level findings.

**Mode**: cooperative
**Agents (3)**: wording-precision, cross-principle-coherence, pr-evidence-grounding
**Rounds**: 1 of 1 configured
**Termination**: completed
**Arbiter**: subject arbitration grounded in `CONSTITUTION.md` (v2.3.0 amended text), `trigger: always`, `timing: final`, `influence: binding`
**Provider**: claude-code

**Outputs**: [`deliberations/v2.3.0-verification-2026-04-25/`](deliberations/v2.3.0-verification-2026-04-25/)

**Methodology flaw discovered mid-session**: agents and arbiter were given the *amended* constitution with all v2.3.0 markers visible (Sync Impact Report header, "Extension (v2.3.0)" labels, "Origin: PR #X" attributions). This anchored agents into "ratify the recent additions" mode rather than "audit the whole document." Result: agents spiraled into process-meta disputes (document version control, evidence classification) rather than concrete content critique. Verdict was `PASS WITH FIXES` but the fixes were process-level, not text-level.

**Status**: `closed` — superseded by the blind run below for content-level verification.

**Outcome**: useful as a self-consistency / wording-precision check, but does not constitute independent verification of the amendment package's merit. Future amendments should run BOTH a self-consistency check (this methodology) AND a blind check (next entry).

---

## 2026-04-25 — v2.3.0 verification (blind methodology)

**Type**: Deliberation
**Trigger**: ratification-bias concern flagged on the self-consistency run above. Run a *blind* verification — strip v2.3.0 markers, agents review the constitution as if from scratch, no anchoring.

**Mode**: cooperative
**Agents (3)**: skeptic, skeptic-2, practitioner — framed to argue for *removing* principles that don't earn their keep, not just to ratify
**Rounds**: 1 of 1 configured
**Termination**: completed
**Arbiter**: independent arbiter grounded in stripped `CONSTITUTION-blind.md`, `trigger: always`, `timing: final`, `influence: binding`. Arbiter prompt explicitly stated "you do NOT know the history of this document."
**Provider**: claude-code

**Stripping methodology**: removed Sync Impact Report header, removed `**Extension (v2.3.0):**` markers, stripped `*Origin: PR #X*` attributions on the new principles, removed mentions of the 2026-04-25 deliberation. Verified 0 v2.3.0/2026-04-25 mentions remain in the target text.

**Outputs**: [`deliberations/v2.3.0-blind-verification-2026-04-25/`](deliberations/v2.3.0-blind-verification-2026-04-25/)

**Outcome**: 3 substantive findings, all in scope of architectural correctness rather than v2.3.0-specific:

1. **Plugin Registry Boundary** — Principles XV and XXVII coordinate around the registry but neither explicitly defines the registry interface as an architectural boundary. **Required fix**: clarify XXVII (in scope for PR #19), defer XV addition to follow-up. ✅ Applied to PR #19 as "Registry as configuration boundary" sub-section.

2. **Mathematical Reproducibility logical contradiction (Principle XVI)** — XVI requires "deterministic assembly" while acknowledging "LLM gap-filling". Direct logical contradiction within ONE PRINCIPLE that predates v2.3.0. ⏸ **Deferred** — out of v2.3.0 scope; deserves its own spec + deliberation. The blind verification would not have surfaced this without ratification-bias-free framing.

3. **Mechanical Verification Requirement** — proposal that constitutional inclusion require mechanical verifiability (principles that fail this test belong in operational guidance). ⏸ **Deferred** — substantive governance change; needs its own amendment.

**Status**: `open` — applied fix #1 to PR #19; deferred fixes #2 and #3 to future amendments.

**Methodology lesson**:
> Self-consistency verification anchors on "what changed"; blind verification audits "what's there". Both are valuable. Self-consistency catches wording drift in the recent additions; blind catches content-level problems anywhere in the document — including longstanding ones recent reviewers have stopped questioning. Spec 066 §7's acceptance protocol should be amended to require BOTH; running only self-consistency is insufficient.

**Deferred follow-ups (from blind run, out of v2.3.0 scope)**:
- [ ] Spec proposing Principle XVI logical-contradiction fix (LLM gap-filling vs determinism). Should run through full deliberation since it touches optimization architecture.
- [ ] Spec proposing governance amendment: "mechanical verification capability is required for constitutional inclusion."
- [ ] Spec 066 §7 amendment requiring both self-consistency AND blind verification methodologies for future amendments.

---

## 2026-04-26 — Spec 068 verification (self-consistency)

**Type**: Deliberation
**Trigger**: spec 067 §4.1 — verification methodology required for spec 06X. Self-consistency check on the v2.3.2 candidate constitution (Principle XVI determinism-scope clarification, PATCH).

**Mode**: cooperative
**Agents (3)**: wording-precision, cross-principle-coherence, pr-evidence-grounding
**Rounds**: 1 of 1 configured
**Termination**: completed
**Arbiter**: subject arbitration with `balanced-arbiter` preset, grounding the v2.3.2 candidate constitution, `trigger: always`, `timing: final`, `influence: binding`
**Provider**: claude-code (host CLI subscription)

**Outputs**: [`deliberations/068-self-consistency-2026-04-26/`](deliberations/068-self-consistency-2026-04-26/)
- Final arbitration: `arbitration/resolution.md`
- 17 per-agent phase artifacts (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes + summary/final.md + arbitration/resolution.md), plus seed inputs (`CONSTITUTION-v2.3.2-candidate.md`, `conversus.yml`).

**Verdict**: PASS WITH FIXES — 3 ACCEPT-level findings, 1 DEFER, 0 REJECT.

**Findings (ACCEPT)**:
- **P1-A (Dispute 1)** — v2.3.2 SIR bullet (e) MUST hedge as "evidence-pending" (pinning discipline assumes spec 014 FR-012/SC-004 enforcement; contract test per Principle XXIV filed as a follow-up to spec 014; CI lint detecting re-entrant `GapFiller.fill()` per spec 068 follow-up).
- **P1-B (Dispute 2)** — Principle XVI stage 2 prose adopts the WP `GapFiller.fill()` protocol-boundary text composed with the synthesis `objective.yml` MUSTs (V observability via `SourceProvenance.filled_by` hook).
- **P1-C (Dispute 3)** — Rename "Mechanical assembly" → "Deterministic assembly" in XVI stage 3 AND append a one-line VIII coordination parenthetical (mechanical/deterministic vocabulary alignment).

**DEFER**: Dispute 4 — Principle II stable-interface sub-bullet for `objective.yml` schema deferred to v2.3.3 PATCH (unblock condition: a second consumer beyond spec 014 lands).

**Status**: `closed` — fixes folded into PR #29 (v2.3.1 → v2.3.2 implementation).

---

## 2026-04-26 — Spec 068 verification (blind methodology)

**Type**: Deliberation
**Trigger**: spec 067 §4.1 — both self-consistency AND blind verification required for spec 06X. Blind run on the stripped v2.3.2 candidate (`CONSTITUTION-v2.3.2-blind.md`) with v2.3.2 markers removed so agents judge Principle XVI on its merits, not on incumbency.

**Mode**: cooperative
**Agents (3)**: skeptic-mathematical, skeptic-cross-principle, practitioner (using `devils-advocate` and `pragmatist` presets to argue for *removing* principles that don't earn their keep)
**Rounds**: 1 of 1 configured
**Termination**: completed
**Arbiter**: subject arbitration with `balanced-arbiter` preset, grounding the stripped `CONSTITUTION-v2.3.2-blind.md`, `trigger: always`, `timing: final`, `influence: binding`. Arbiter prompt explicitly stated "you do NOT know the history of this document."
**Provider**: claude-code (host CLI subscription)

**Outputs**: [`deliberations/068-blind-2026-04-26/`](deliberations/068-blind-2026-04-26/)
- Final arbitration: `arbitration/resolution.md`
- 17 per-agent phase artifacts (same structure as the self-consistency run), plus stripped `CONSTITUTION-v2.3.2-blind.md` and `conversus.yml`.

**Verdict**: PASS WITH FIXES — 4 ACCEPT-level findings on Principle XVI, 0 DEFER, 0 REJECT.

**Findings (ACCEPT)**:
- **Structural fork** — adopt tightened-standalone XVI (no new principle numbers, no full decomposition); body rewrite ~4–8 operational bullets.
- **Test-contract sequencing** — route the parameter-pinning contract test through spec 013, not constitutional prose; spec 013 must ship first as a procedural merge gate (XII-safe).
- **Cross-reference graph asymmetry** — wire the V-emission clause subordinate to VII's reproducibility pre-conditions in one composed rule (subordinate-clause edit, not relocation).
- **XXIV scope residual** — drop the XXIV cross-reference from XVI; generic test-contract clause via spec 013 carries the verification load (XXIV's own scope text bounds it to synthesis verdicts + provider protocols; XI prohibits parallel doctrine).

Plus three procedural required-fixes-before-merge: append VII bilateral cross-reference + reproducibility pre-conditions clause; add `pinning` term-of-art to II's stable-interface vocabulary with V cross-reference; spec 013 procedural merge gate.

**Status**: `closed` — fixes folded into PR #29 (v2.3.1 → v2.3.2 implementation).

---

## 2026-04-26 — Spec 069 verification (self-consistency)

**Type**: Deliberation
**Trigger**: spec 067 §4.1 — verification methodology required for spec 06X. Self-consistency check on the v2.4.0 candidate constitution (Constitutional Inclusion Criteria gate, MINOR).

**Mode**: cooperative
**Agents (3)**: governance-skeptic, strictness-skeptic, practitioner
**Rounds**: 1 of 1 configured
**Termination**: completed
**Arbiter**: subject arbitration with `balanced-arbiter` preset, grounding the v2.4.0 candidate constitution, `trigger: always`, `timing: final`, `influence: binding`
**Provider**: claude-code (host CLI subscription)

**Outputs**: [`deliberations/069-self-consistency-2026-04-26/`](deliberations/069-self-consistency-2026-04-26/)
- Final arbitration: `arbitration/resolution.md`
- 16 per-agent phase artifacts (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes + summary/final.md + arbitration/resolution.md), plus seed inputs (`CONSTITUTION-v2.4.0-candidate.md`, `conversus.yml`).

**Verdict**: PASS WITH FIXES — 0 ACCEPT-level findings on the candidate amendment as drafted (effectively PASS for spec 067 §4.4 acceptance bar).

**Findings**: None against the candidate amendment. Three disputes resolved as: REJECT strictness-skeptic AND-coupling restructure (Dispute 1); DEFER verification-deliberation acceptance bar to v2.5.0 (Dispute 2); ACCEPT cooperative composition of precedent-log build-moment edits (Dispute 3 — operationalizes a convergent recommendation already in P2, not a defect-correction). Per the arbiter: "the candidate v2.4.0 amendment is shippable as drafted, with the convergent P1/P2 changes from the Phase 5 synthesis applied as already prioritized."

**Status**: `closed` — no defect fixes needed. Convergent P1/P2 fixes from synthesis already on PR #30's edit set.

---

## 2026-04-26 — Spec 069 verification (blind methodology)

**Type**: Deliberation
**Trigger**: spec 067 §4.1 — both self-consistency AND blind verification required for spec 06X. Blind run on the stripped v2.4.0 candidate (`CONSTITUTION-v2.4.0-blind.md`) with v2.4.0 markers removed so the gate is judged on its own merits, not on incumbency.

**Mode**: cooperative
**Agents (3)**: skeptic-mathematical, skeptic-cross-principle, practitioner
**Rounds**: 1 of 1 configured
**Termination**: completed
**Arbiter**: subject arbitration with `balanced-arbiter` preset, grounding the stripped `CONSTITUTION-v2.4.0-blind.md`, `trigger: always`, `timing: final`, `influence: binding`. Arbiter prompt: "the gate is judged on its own merits, with no incumbency advantage."
**Provider**: claude-code (host CLI subscription)

**Outputs**: [`deliberations/069-blind-2026-04-26/`](deliberations/069-blind-2026-04-26/)
- Final arbitration: `arbitration/resolution.md`
- 17 per-agent phase artifacts (same structure as the self-consistency run), plus stripped `CONSTITUTION-v2.4.0-blind.md` and `conversus.yml`.

**Verdict**: PASS WITH FIXES — 3 ACCEPT-level findings on the gate subsection.

**Findings (ACCEPT)**:
- **Dispute 1 — Grandfathering disposition** — REJECT strictness-skeptic's tiered classification + v3.0.0 deadline (would violate gate's own Prospective-Only Migration clause on day one); ACCEPT light non-precedential calibration footnote naming positive-exemplar principles (XI, XII, XIII, XXII, XXIV, XXVI); DEFER full corpus disposition to a follow-up grandfathering spec.
- **Dispute 2 — Criterion 3 operational test** — ACCEPT practitioner's middle ground: ship two worked examples in gate text (one Criterion-1 falsifiability rejection, one Criterion-3 distinctness rejection); PR template Distinctness section names closest existing principle + one-sentence insufficiency claim. Reject strictness-skeptic's three-part `(a)/(b)/(c)` block (the "novel predicate" sub-field inherits a known failure mode).
- **Dispute 3 — Extension-block treatment** — ACCEPT synthesizer's middle position: Extension/Clarification blocks added to grandfathered principles after gate ratification MUST include the structured `Verification:` block (Criterion 1) when introducing new normative requirements; Criterion 3 does not apply (incoherent for Extensions); wording-level clarifications exempt. Closes the prose-only Extension loophole demonstrated by IX/XI/XV v2.3.0 extensions.

**Status**: `closed` — fixes folded into PR #30 (v2.3.x → v2.4.0 implementation).

---

## 2026-04-27 — Post-v2.4.0 gap analysis

**Type**: Deliberation
**Trigger**: forward-looking gap analysis of changes since the 2026-04-25 gap analysis (PRs #15-#33, including v2.3.0 → v2.4.0 amendments) under the new v2.4.0 Constitutional Inclusion Criteria gate.

**Mode**: cooperative
**Agents (4)**: governance, methodology (preset: devils-advocate), distribution, practitioner (preset: pragmatist)
**Rounds**: 1 of 1 configured
**Termination**: completed
**Arbiter**: subject arbitration with `balanced-arbiter` preset, grounding `CONSTITUTION.md` (v2.4.0), trigger always, timing final, influence binding
**Provider**: claude-code (host CLI subscription)

**Outputs**: [`deliberations/post-v2.4.0-gap-analysis-2026-04-27/`](deliberations/post-v2.4.0-gap-analysis-2026-04-27/)

**Operational issue**: original Phase 5 synthesis hit a stream idle timeout mid-stream and only the metadata header landed. Recovered via Agent-tool-driven retry with Write-direct; full synthesis written.

**Verdict**: 0 ACCEPT, 14 OPERATIONAL, 3 DEFER, 7 REJECT.

**Why this matters**: 0 ACCEPT means the v2.4.0 gate filtered every proposal. Compare to the 2026-04-25 pre-gate gap analysis which produced 6 new principles + 2 extensions. The gate is doing exactly what spec 069 designed it to do: route operational concerns to operational documents instead of growing the constitution.

**Top OPERATIONAL recommendations** (14 total):
- **Spec 070** — audit grandfathered principles (VI, X, XVI) against the v2.4.0 gate; migrate failures to operational guidance.
- **Spec 067 amendment** — add re-verification trigger: fixes folded into implementation PR MUST be re-verified by re-running the affected methodology before merge. (Today's spec 068 + 069 implementations merged ACCEPT fixes without re-verification — methodology violation.)
- **Spec 067 amendment** — verification cost reporting: each governance log entry MUST include agent launches, not just verdict.
- **CONTRIBUTING.md** (per spec 065 G7) — growth budget for constitutional content (e.g., max 1 new principle + 2 extensions per quarter); PR-replacement-after-force-push pattern; naming-deliberation-prerequisites pattern.
- **Memory entries** — operational lessons: Write-direct discipline survives orchestrator stream failures; force-push closes PRs unexpectedly; parallel impl-subagent + verification deliberation pattern.

**Status**: `open` — operational follow-ups not yet filed; this entry is the canonical record of the gap analysis output.

**Methodology lesson**: the v2.4.0 gate's first real test ran cleanly. 14 OPERATIONAL routings is evidence of correct calibration. Future gap analyses should expect similar distributions — most session-end concerns are operational, not constitutional.

---

## 2026-04-29 — spec 071: Principle XXVIII (Test-Fix Boundary Preservation) ratified with override

**Type**: Amendment (with blind-verdict override)

**Trigger**: spec 071 §12 acceptance criteria; v2 blind verification PASS WITH FIXES required override decision

**Mode + Agents + Rounds**: cooperative, 3 agents (skeptic-mathematical, skeptic-cross-principle, practitioner) + balanced-arbiter, 1 round, run twice (blind v1 + blind v2). Self-consistency run separately with 4 agents + balanced-arbiter.

**Outputs**: [`deliberations/071-self-consistency-2026-04-28/`](deliberations/071-self-consistency-2026-04-28/), [`deliberations/071-blind-2026-04-28/`](deliberations/071-blind-2026-04-28/) (v1), [`deliberations/071-blind-v2-2026-04-29/`](deliberations/071-blind-v2-2026-04-29/) (v2)

**Specs referenced**: spec 071 (proposing), spec 067 (verification methodology), spec 069 (Constitutional Inclusion Criteria gate), spec 045 (originating coverage verification, now in `specs/done/`)

**PRs referenced**: PR #42 (case study — `find_project_root` import shadowing fix; merged 2026-04-28; verified merged with claimed content via `gh pr view 42`)

**Outcome**: **Amendment landed** — `CONSTITUTION.md` v2.4.0 → v2.5.0, Principle XXVIII added.

**Status**: `open` — pending three follow-up implementation PRs (PR template addition per spec 071 §7, lint-test-fixes.py per §6, spec 067 §4.6 amendment per §8).

### What happened

Spec 071 proposed Principle XXVIII codifying test-fix discipline, motivated by the 2026-04-28 PR #42 case study where a 4-subagent investigation surfaced 1 production bug + ~70 mechanical failures that a naive sweep would have buried. Per spec 067 §4, both self-consistency AND blind verification ran on the candidate constitution.

**Self-consistency (2026-04-28)**: PASS WITH FIXES (4 disputes — evidence validation, criteria interpretation ambiguity, three-part justification criteria, AST-diff specification). All fixes addressed in v2 or absorbed by other v2 changes.

**Blind v1 (2026-04-28)**: "move XXVIII to operational guidance" — three rulings: (a) clause 1 "assertion fidelity" duplicates Principle IX's behavior-over-shape extension (Criterion 3 distinctness fail); (b) format-checking categorization presence ≠ substantive verification (Criterion 1 fail); (c) RFC 2119 "MAY NOT" non-conformant.

**v1 → v2 revision (2026-04-29)**: dropped clause 1 (deferred to IX), strengthened clause 3 with diff-shape consistency check (the lint reads category claim and verifies against actual diff shape), fixed RFC 2119 by removing "MAY NOT" with the dropped clause.

**Blind v2 (2026-04-29)**: PASS WITH FIXES — three further rulings: (1) focus XXVIII on skip discipline only; drop categorization framework + headline behavioral preservation claim; (2) replace 4-category taxonomy with binary safety-critical vs non-safety-critical (derive from XXIV); (3) no emergency-bypass provisions.

### Override-with-rationale

Rulings 1 and 2 of the blind v2 verdict were overridden. Ruling 3 was N/A — v2 never proposed emergency-bypass provisions.

**Override of ruling 1 (focus on skip discipline only)**: the arbiter's reasoning — "categorization with diff-shape check has acknowledged residuals, therefore belongs in operational guidance" — applies a strict reading that, if applied uniformly, would shrink Principle IX's behavior-over-shape extension as well (which has analogous acknowledged residuals — "looks like loosening to AST diff" appears in IX's prose). Diff-shape consistency IS substantively verifying for the dominant failure mode the principle is designed to catch: a production-source edit incompatible with a "fixture drift" label is structurally detectable, which is exactly what the PR #42 case study would have produced under a naive-sweep label. The residual (a "fixture drift" claim with only test-file edits that is actually a "legitimate test bug" miscategorized) is honestly acknowledged in clause 2's text. Removing categorization entirely would render XXVIII unable to address its motivating incident; the operational scaffolding (PR template + lint) without a constitutional anchor decays into checklist-no-one-reads territory over time.

**Override of ruling 2 (binary safety-critical reframe)**: the arbiter proposed reframing categorization as binary safety-critical vs non-safety-critical (deriving the safety-critical definition from Principle XXIV). This solves a different problem — blast radius — than what XXVIII's originating incident (categorization-mode miscategorization) requires. A "production bug" miscategorized as "fixture drift" can occur on a non-safety-critical path and still hide a regression; reframing to safety-criticality leaves that failure mode unaddressed. The proposed reframe is a creative but orthogonal principle that does not displace the four-category framework's specific value.

### Why override and not iterate

Adversarial blind verification has now driven two principled refinements: v1 → v2 dropped a duplicate clause (genuine distinctness fix); v2 → v2-final further narrowing was rejected on the grounds above. Continued iteration would not converge — the arbiter's strict "acknowledged residual = operational guidance" reading, if applied uniformly, would relegate large portions of the existing constitution to operational guidance. That is a separate amendment cycle (grandfathering review per spec 069 §5), not a per-principle veto.

This override is logged here as a precedent: blind verdicts are weighted heavily but not absolute; uniform-application stress-tests are a legitimate override criterion when the same standard would shrink existing ratified principles.

### Acceptance bar disposition

Spec 071 §9 set "0 ACCEPT findings on principle wording" as the bar. Self-consistency: 4 ACCEPT, all addressed in v2. Blind v1: 3 ACCEPT, all addressed in v2. Blind v2: 3 ACCEPT, of which 2 overridden with rationale logged here, 1 N/A. The bar is met substantively for v2 as ratified.

### Follow-up TODOs (per spec 071 §12)

1. PR adding `.github/pull_request_template.md` with the structured machine-readable category marker.
2. PR adding `scripts/lint-test-fixes.py` with the skip-citation regex check + diff-shape consistency check.
3. PR amending `specs/067-verification-methodology/spec.md` with §4.6 codifying the 4-subagent investigation pattern as the canonical first response when verification surfaces failing tests.
4. Memory entry recording the override-precedent (the "uniform-application stress-test" criterion) for future amendment cycles.

### Methodology lesson

Adversarial blind review is rate-limited by uniform-application of its own standards. When a blind judge applies a standard whose uniform application would shrink existing ratified principles, the override-with-rationale pathway is the correct response — not continued iteration that would never converge, and not "demote the principle" that would silently embed asymmetric standards across the constitution. The override must be logged with the specific uniformity argument that justifies it; future amendments can cite this precedent or distinguish it.

## 2026-05-01 — spec 070 cycle 1: Principle XVI headline rewrite + path (c) Governance addition (v2.5.0 → v2.6.0)

**Type**: Amendment (MINOR; XVI headline rewrite is PATCH-class path (c) restructuring; Governance section addition defining path (c) is independently MINOR; combined package = MINOR)

**Trigger**: spec 070 cycle 1 (closes the v2.4.0 grandfathering gap for Principle XVI flagged in spec 069 §5: "user MUST understand the math" headline framing fails Constitutional Inclusion Criterion 1)

**Mode + Agents + Rounds**:
- **Self-consistency** (`deliberations/070-cycle1-xvi-self-2026-05-01/`): cooperative, 3 agents (wording-precision, cross-principle-coherence, gate-skeptic) + subject arbitration, 1 round. 8 convergence points (4 unanimous, 4 bilateral); 5 disputes survived to arbitration.
- **Blind verification** (`deliberations/070-cycle1-xvi-blind-2026-05-01/`): cooperative, 2 agents (skeptic-mathematical, skeptic-cross-principle) + subject arbitration, 1 round. 5 unanimous convergence points; 2 disputes survived to arbitration.

**Outputs**: [`deliberations/070-cycle1-xvi-self-2026-05-01/`](deliberations/070-cycle1-xvi-self-2026-05-01/), [`deliberations/070-cycle1-xvi-blind-2026-05-01/`](deliberations/070-cycle1-xvi-blind-2026-05-01/)

**Specs referenced**: spec 070 (proposing), spec 067 (verification methodology), spec 069 (Constitutional Inclusion Criteria gate; v2.4.0 grandfathering disclosure), spec 014 (FR-012/SC-004 — pinning behavior anchor), spec 013 (template definitions for stage 1 parsing)

**Verdicts**: Both deliberations PASS WITH FIXES.

**Outcome**: **Amendment landed** — `CONSTITUTION.md` v2.5.0 → v2.6.0. Principle XVI headline reduced to ONE structural invariant (parameter pinning); stage-3 of the 3-stage pipeline body relocated to attribute its guarantee to Principles VII and VIII (no additional normative requirement at stage 3); plain-language pairing requirement restructured as an atomic package (structural definition + XV enforce-mode clause + registry-emission cross-reference); design-intent paragraph relocated to Origin note with targeted wording fixes; stage-3 verification artifact added to Clarification (v2.3.2) Enforcement sub-bullet as a VII+VIII composition completeness test. Governance section gains new "Grandfathered-principle headline rewrites (path (c))" paragraph.

**Status**: `open` — pending v2.3.2 Clarification block "shape" follow-up PATCH ([issue #94](https://github.com/Build-Fractal/conversus-oss/issues/94)); pending implementation of the stage-3 assembly-form determinism completeness test (CI check) and the plain-language schema lint.

### Strategy: blind narrowing + self orthogonal fixes

Per spec 067, where two verification deliberations disagree on the architectural shape, the more rigorous standard governs. Blind verification ruled the headline must reduce to ONE structural invariant (parameter pinning only) on the grounds that stage-3's "shape determinism" claim is a VII+VIII composition (no Criterion 3 distinctness) and plain-language pairing is general output discipline (XV-territory). Self-consistency accepted the 3-invariant headline. Blind's narrowing was adopted as the architectural shape; self-consistency's orthogonal fixes (atomic plain-language package, design-intent prose relocation to Origin note, path (c) Governance definition) were layered on top.

### Required changes applied

Six dispute rulings drove the amendment text:

1. **Self Dispute 1 — design-intent paragraph wording fixes + WP Rec 7 mandatory relocation**: targeted fixes (L790 deletion; "(auditable)" → "(persisted to `objective.yml` via `SourceProvenance.filled_by`)"; "template shapes are stable (no surprise math)" → "assembly structure is deterministic given the same template and pinned parameters"; "(no bare numbers)" retained) + relocation of the corrected paragraph to the Origin note with "Design intent:" label.
2. **Self Dispute 2 — "no bare numbers" retention**: gloss preserved on the third structural requirement.
3. **Self Dispute 3 — atomic plain-language fix package**: structural definition + XV enforce-mode clause + registry-emission cross-reference shipped as a single atomic change to XVI's third bullet.
4. **Self Dispute 4 — v2.3.2 "shape" terminology Option B (defer)**: deferred to a named follow-up PATCH per audit-integrity grounds; SIR Disclosure section identifies both collision sites and cites the tracking issue.
5. **Self Dispute 5 — path (c) governance definition pre-ratification blocking**: new Governance paragraph defines the path (c) amendment category, its PATCH-class classification, the SIR attestation requirement, and the no-re-audit rule for pre-v2.4.0 grandfathered body content.
6. **Blind Dispute 1 (headline reduction) + Blind Dispute 2 (assembly-form rename)**: headline reduced to ONE invariant (parameter pinning); stage-3 body relocated with VII+VIII attribution; stage-3 verification artifact added to enforcement block as a VII+VIII composition completeness test (with future-amendment reconsideration clause); "assembly-form-identical" replaces "bit-for-bit identical" in the relocated stage-3 body for IX-collision avoidance.

### Arbitral precedent: WP Rec 7 elevation from P3 to mandatory

The self-consistency arbiter elevated WP Rec 7 (design-intent paragraph relocation to the Origin note) from P3 optional to MANDATORY co-blocking — the first use of arbitral authority in conversus to **upgrade a convergence point's priority classification** rather than resolve a disputed position. The grounding: GS's purpose-clause concern (the framing "is achieved through these structural requirements" invites implementors to argue non-conforming alternatives "achieve the design intent" by other means) is a Criterion 2 falsifiability defect; Origin-note relocation is the constitutionally established home for design-intent prose (see analogous patterns in Principles XIX, XXII Origin notes); GS's Rec 6 fallback established that targeted replacement is constitutionally adequate for the specific lexical defects, so the wholesale-replacement pathway was over-inclusive on GS's own evidentiary standard. Logged here as a precedent distinct from the path (c) amendment-category mechanism: arbiters may elevate priority classifications when the constitutional grounding requires it.

### Path (c) precedent established

This amendment is the canonical path (c) precedent for future remediation of grandfathered Principles VI (Scripts Over Markdown) and X (Zen of Python Output). Path (c) amendments are PATCH-class for the headline restructuring component; the path (c) SIR MUST include an explicit attestation that no new normative requirements are introduced by the headline restructuring itself. Body content that existed pre-v2.4.0 is not re-audited under the three-criterion gate when elevated to headline status under path (c); only genuinely new content is gated.

### Methodology lesson

Spec 067's verification methodology — running both self-consistency AND blind verification — produced complementary findings. Self-consistency surfaced wording quality and packaging issues (atomic plain-language package; design-intent prose positioning) that blind missed. Blind surfaced architectural shape issues (headline reduction; VII+VIII composition for stage-3) that self missed. Neither deliberation alone would have produced the final amendment; the combination — with the spec 067 conservative-wording rule directing which standard governs the architectural shape — did.
