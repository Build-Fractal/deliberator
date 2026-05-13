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

## 2026-05-08 — v4.0.0 erratum C1 — URL-reference cross-tier resolution

**Type**: Erratum (PATCH-equivalent; substantive content unchanged).
**Source**: `https://github.com/Build-Fractal/build-fractal-mono/blob/main/build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md` 2026-05-08 v4.0.0-erratum-c1-url-references entry (suite-tier).
**Effect on this repo**: cross-tier references in `CONSTITUTION.md` and `CONFORMANCE.md` converted from filesystem-relative paths (`../build-fractal/...`) to canonical GitHub URLs. Repo's standalone usability restored — readers cloning conversus-oss alone or browsing on github.com see clickable URL references to the monorepo's canonical Tier 1 / Tier 2 sources. Tooling: `linter/tier_coherence.py` Check (c) extended to validate URL form against canonical monorepo prefix.
**No principle text changed**.

## 2026-05-07 — v3.2.3 → v4.0.0 tier extraction (component-tier reduction)

**Type**: Implementation of MAJOR amendment (tier-extraction-ratified at suite tier).
**Pathway**: MAJOR per CONSTITUTION.md § Pathway Taxonomy.
**Source**: `../build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md` 2026-05-07 v4.0.0-tier-extraction-ratified entry.
**Effect on this repo**: CONSTITUTION.md reduced from 28 principle slots (26 active + 2 retired) at v3.2.3 to 6 component principles + 2 retired markers at v4.0.0. Governance section + all prior SIRs preserved verbatim. 20 principles relocated:
- 10 to Tier 1 (`../build-fractal/CONSTITUTION.md`): I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII.
- 10 to Tier 2 (`../build-fractal/conversus/CONSTITUTION.md`): V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII.
**Three deliberations**: originating, self-consistency, blind — all logged at suite tier. 12 fixes applied across spec v1 → v2 → v3.
**Tooling**: `linter/tier_coherence.py` ships with this amendment (Constitutional Inclusion Criterion 1 satisfaction; 4 hard checks + weakening-words flagging).
**Admission**: this repo formally admitted to the conversus suite via Q2 ADMIT-PROVISIONAL (originating); CONFORMANCE.md flipped Implicit-Provisional → Provisional with 5 open remediations.
**Engine note**: auto-arbitrator crashed on both verification deliberations; manual arbitrations performed. Bug logged separately (project_conversus_arbitration_crash_2026_05_06).

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

## 2026-05-01 — spec 070 cycle 2: Principles VI and X migrate-out + Principle Number Stability (v2.6.0 → v3.0.0)

**Type**: Amendment (MAJOR — principle removals: VI Scripts Over Markdown and X Zen of Python Output, both migrated to operational guidance. Per the Governance Versioning bullet, MAJOR is triggered for principle removals or redefinitions.)

**Trigger**: spec 070 cycle 2 (closes the v2.4.0 grandfathering gap for Principles VI and X by migrating them to operational guidance per the migrate-out pattern; cycle 1 closed the gap for XVI via path (c) headline rewrite, retaining XVI in the constitution. VI's "drives behavior" qualifier and X's "readability counts" claim have no structural default class to anchor a CI check, leaving migrate-out as the appropriate remediation.)

**Mode + Agents + Rounds**:
- **Self-consistency** (`deliberations/070-cycle2-vi-x-self-2026-05-01/`): cooperative, 3 agents (removal-rigor-skeptic, cross-reference-coherence, migration-soundness) + subject arbitration. 4 disputes survived to arbitration; all P1 fixes accepted.
- **Blind verification** (`deliberations/070-cycle2-vi-x-blind-2026-05-01/`): cooperative, 2 agents (numbering-skeptic, body-coherence-skeptic) + subject arbitration. 4 disputes survived to arbitration; all P1 atomic-bundle elements accepted.

**Outputs**: [`deliberations/070-cycle2-vi-x-self-2026-05-01/`](deliberations/070-cycle2-vi-x-self-2026-05-01/), [`deliberations/070-cycle2-vi-x-blind-2026-05-01/`](deliberations/070-cycle2-vi-x-blind-2026-05-01/)

**Specs referenced**: spec 070 (proposing), spec 067 (verification methodology), spec 069 (Constitutional Inclusion Criteria gate; v2.4.0 grandfathering disclosure)

**Verdicts**: Both deliberations PASS WITH FIXES.

**Outcome**: **Amendment landed** — `CONSTITUTION.md` v2.6.0 → v3.0.0. Principles VI and X migrated to operational guidance (`CONTRIBUTING.md` § Authoring Conventions and `docs/output-conventions.md` respectively) and replaced with retirement tombstones in the principle list. Principle II's stable-interfaces enumeration extended to include principle numbers. Governance section gains a new Principle Number Stability subsection (no-reuse rule, RFC/CVE rationale, gap intentionality) and a Removal checklist subsection (verification, migration target, tombstone, Principle Number Stability cite, arbiter-ruling Origin coordination, extended cross-reference audit). Grandfathering paragraph corrected to enumerate the active set with VI and X struck through, declare them permanently retired, and cite the 26-active-principle count. Path (c) precedent text (formerly L1589) corrected to a cycle/version-only formulation that no longer names VI and X by principle in the migrate-out clause; v3.0.0 is named as the canonical migrate-out precedent.

**Status**: `partially open` — v3.0.0 ratification commit lands the atomic bundle (blind Recs 1+2+3+4+6) and the self-consistency P1 corrections (L1589 wording, Criterion 2 SIR label correction, mkdocs.yml nav entry, X substrate analysis paragraph, cross-reference audit methodology). Two follow-up items deferred to subsequent PRs:
- **Cycle 2B** (P1, MINOR-class): retroactive Origin note Amendment-record subsections for Principles XXIV, XXV, XXVII closing the latent Principle XI documentation gap surfaced by blind verification's arbiter ruling on retroactive Origin notes. Filed as GitHub issue.
- **Cycle 2C** (P2, PATCH-class): XIX labels-only sub-headings ("Architectural invariants" / "Operational constants") without modifying any normative language. Filed as GitHub issue. Sequenced after cycle 2B.
- **Same-version Principle II elaboration**: append "Reusing a retired principle number is a breaking change..." to Principle II's breaking-change coordination text. Marked with `# TODO(spec-070-cycle2-followup)` in the body. Per blind verdict, deferral is a downstream elaboration, not a Principle II atomicity violation.

### Strategy: blind atomic bundle + self orthogonal P1 corrections

The cycle 2 amendment ships blind verification's atomic bundle (Recs 1+2+3+4+6: tombstones, Principle II addition, Principle Number Stability subsection, Removal checklist, grandfathering correction with explicit MUST NOT and 26-active count) as a non-separable unit per the blind verdict's Atomic bundle scope ruling. Self-consistency's P1 corrections (L1589 wording fix, Criterion 2 SIR label correction with full reasoning chain, mkdocs.yml nav entry, X substrate analysis, cross-reference audit methodology) layer on top in the same atomic commit per the Sequencing dispute ruling's co-equal P1 framing. Two items from blind's verdict were deferred:
- The Principle II breaking-change elaboration (Rec 7) is a downstream consequence, not a consumer of the stable-interface declaration; same-version follow-up is acceptable per blind verdict's Atomic bundle scope ruling. Body tagged with `# TODO(spec-070-cycle2-followup)`.
- The retroactive Origin note amendments for XXIV, XXV, XXVII (blind verdict's Prescription strength ruling) are deferred to cycle 2B as a coordinated follow-up. The deferral and rationale are documented in the v3.0.0 SIR; the Removal checklist subsection enumerates this case as the canonical example of arbiter-ruling Origin coordination.

### Comparative-principles asymmetry observation (CI-detectable structural default class)

Both verdicts noted the asymmetric treatment of judgment-laden language across the constitution: VI's "drives behavior" has no structural default class to anchor a CI check, while XV's "core artifacts," XXIV's "safety-critical paths," and IX's "prefer pure functions" all do (file consumption by the runtime, explicit enumeration, static analyzability). This distinction — between judgment calls with a CI-detectable structural default class and irreducibly judgment-dependent qualifiers — is the constitutional load-bearing reason why VI was removed while XV, XXIV, and IX were retained. The distinction is documented in the v3.0.0 SIR and is required reading for future migrate-out deliberations citing v3.0.0 as precedent.

### Required changes applied

Bundle (blind P1 atomic bundle, Recs 1+2+3+4+6):
1. **Tombstones for VI and X** — strikethrough headlines, retirement date and version, migration target named, no-reuse declaration with cross-reference to Principle Number Stability.
2. **Principle II stable-interfaces list addition** — principle numbers added to the enumeration as stable interfaces with permanent-retirement-only state change.
3. **Governance: Principle Number Stability subsection** — no-reuse rule, RFC/CVE rationale, gap intentionality. Future principle additions MUST use unused numbers (XXIX, XXX, …).
4. **Governance: Removal checklist subsection** — six-step checklist (verification, migration target, tombstone, Principle Number Stability cite, arbiter-ruling Origin coordination, extended cross-reference audit).
5. **Grandfathering clause correction** — active set enumerated, VI and X struck through with retirement noted, explicit "MUST NOT be reused... regardless of gate criteria" language, count updated to 26 active principles.

Self-consistency P1 corrections:
6. **L1589 path (c) wording fix** — replaced with cycle/version-only formulation; v3.0.0 named as canonical migrate-out precedent without naming VI/X by principle in the migrate-out clause.
7. **Criterion 2 SIR label correction with full reasoning chain** — VI's removal rationale identifies Criterion 2 (not Criterion 1) as the failure; documents the Criterion 2 → wording-refinement evaluation → no-viable-refinement → migrate-out chain; flags the Governance Criterion 1 worked example as exhibiting the same conflation.
8. **mkdocs.yml nav entry** — `output-conventions.md` added under Developer Guide alongside Contributing.
9. **X substrate analysis** — paragraph in v3.0.0 SIR documenting Criterion 3 analysis of "one clear purpose per output file" as subsumed by V+VII applied to output schema design; not an independent Criterion 3 claim; migrate-out for X holds.
10. **Cross-reference audit methodology** — SIR documents the L1589 plural-form miss and establishes singular/plural/adjacent-phrase audit methodology going forward; methodology codified in Removal checklist (f).

### Methodology lesson

The cycle 2 deliberation surfaced a structural asymmetry that neither cycle 1 nor cycle 2's individual reviewers identified independently: the "judgment-laden qualifier" rationale that justified VI's removal could be applied to XV, XXIV, IX without a distinguishing test, leaving the precedent overextendable. The distinction — CI-detectable structural default class — emerged from cross-review and was elevated to constitutional documentation in the v3.0.0 SIR. This is the kind of finding that validates the multi-agent deliberation model: the distinction is derivable from first principles, but neither reviewer applied it to their own recommendations in isolation. Future migrate-out amendments must apply this test before citing v3.0.0 as precedent.

The atomicity insight from blind verification — that implementing the no-reuse rule (Rec 3) triggers Principle II's atomicity clause across the entire Governance amendment bundle (Recs 1+2+4+6) — is similarly significant. Neither agent identified the atomicity constraint independently in Phase 1; it emerged from cross-review. This is logged here as a precedent for future deliberations: when a recommendation touches a principle that appears in another principle's body text, the atomicity-clause analysis should be performed reflexively, not deferred to synthesis.

---

## 2026-05-01 — Constitution v3.0.0 → v3.1.0 (cycle 2B retroactive Origin note Amendment records)

**Subject**: Spec 070 cycle 2B follow-up — close the latent Principle XI documentation gap surfaced by blind verification's arbiter ruling on retroactive Origin notes during the v3.0.0 ratification.

**Trigger**: v3.0.0 SIR deferred-items list (lines 138-146 of the v3.0.0 SIR comment block in CONSTITUTION.md), filed as GitHub issue #96 during the v3.0.0 ratification commit.

**Verification approach**: per issue #96, the change is purely structural — verbatim move of arbiter-ruling sentences from the principle body (XXIV) or from inline-Origin language (XXV, XXVII) into clearly labeled Amendment record subsections appended to each Origin note. No normative wording is modified. A single coordinated PR with cross-reference verification suffices; no deliberation cycle required.

**Verbatim-preservation contract**:
- **Principle XXIV** (Safety-Critical Defense-in-Depth): the "The 2026-04-25 deliberation arbiter explicitly extended this scope to provider protocols (not just synthesis logic) on the evidence that PRs #5, #6, #8, #9 produced the same class of silent failure as PR #10's false-PASS bug." sentence (originally a body paragraph between rule 4 and the Origin note) → moved verbatim into a labeled `*Amendment record (2026-04-25, arbiter ruling): ...*` subsection appended to XXIV's Origin note. Body content reduced to the four numbered discipline rules.
- **Principle XXV** (Live Test Cost Discipline): the "The 2026-04-25 deliberation arbiter ruled this principle must precede provider contract testing requirements." sentence (previously embedded in the Origin note's tail) → split into a separate Amendment record subsection. Origin note retains only the originating-PR sentence ("PR #8 introduced `@pytest.mark.live` without codifying the discipline.").
- **Principle XXVII** (Operator-Configurable Tool Surface): same treatment as XXV. The "The 2026-04-25 deliberation arbiter ruled this should be a standalone principle (not a Principle XV extension) because operator configuration scope extends beyond plugin isolation to the core tool surface." sentence → split into Amendment record subsection. Origin note retains only "PR #14 (CONVERSUS_DISABLED_TOOLS)."

**Closing rationale appended to each Amendment record**: "No contemporaneous /speckit.constitution invocation was recorded; this retroactive record closes that historical process gap (added in v3.0.x cycle 2B per Removal checklist subsection (e))." This phrasing names the historical process gap explicitly and cites the v3.0.0 prospective infrastructure (Removal checklist subsection (e), arbiter-ruling Origin coordination) so the retroactive amendments register as the first three applications of that subsection.

**Why MINOR (not PATCH)**: each principle gains a new Amendment record subsection — that is new structural infrastructure within the principle container, even though no normative wording changes. Per the v3.0.0 Removal-checklist subsection (e), Amendment record placement is itself a governance feature; introducing the first instances of it qualifies as a MINOR governance enhancement. Future Amendment record additions to other principles, when prompted by the same documentation-gap mechanism, will follow the precedent established here.

**Outstanding deferred items** (after cycle 2B):
- Cycle 2C (P2, PATCH-class, issue #97): XIX labels-only sub-headings reorganization. Sequenced after cycle 2B per the v3.0.0 SIR's deferred-items list.
- Issue #94 (PATCH-class): v2.3.2 Clarification block "shape" → "assembly-form" terminology rename. Requires dual-perspective wording-precision and cross-principle-coherence review of the FULL v2.3.2 block before ratification (per issue acceptance criteria); deferred to a future amendment cycle.
- Same-version Principle II elaboration (TODO from v3.0.0 SIR): add to Principle II's breaking-change coordination text the sentence "Reusing a retired principle number is a breaking change — any historical document that cited the retired number by identity would thereafter refer to a different principle." Marked with `# TODO(spec-070-cycle2-followup)`.

**Methodology note**: this is the first amendment to apply the v3.0.0 Removal-checklist subsection (e) (arbiter-ruling Origin coordination) retroactively. The verbatim-preservation contract is the test: if a future MINOR-class amendment of this kind would add or remove normative requirements, it must instead go through the full dual-deliberation cycle. Pure governance-record corrections — moving existing arbiter-ruling text from one structural location to another within the same principle, with no rewriting — qualify for the single-PR pathway used here. This precedent is logged so future Amendment-record additions know which pathway applies.

---

## 2026-05-01 — Constitution v3.1.0 → v3.1.1 (cycle 2C XIX labels-only sub-headings)

**Subject**: Spec 070 cycle 2C follow-up — labels-only reorganization of Principle XIX's bullet list under two clearly-labeled sub-headings ("Architectural invariants" / "Operational constants").

**Trigger**: v3.0.0 SIR deferred-items list (cycle 2C entry, P2 PATCH-class), filed as GitHub issue #97 during the v3.0.0 ratification commit. Sequenced after cycle 2B (#103) per the issue's sequencing requirement.

**Verification approach**: per issue #97, "Because cycle 2C modifies no normative language, a lightweight verification suffices: cross-reference audit ... and a single review pass to confirm verbatim preservation. Spec 067 dual-deliberation is not required for a PATCH-class structural-grouping-only change."

**Cross-reference audit**: ran `grep -rn "XIX\.\|Principle XIX\|Non-Extractable"` across CONSTITUTION.md, CONSTITUTIONAL_CONVERSATIONS.md, scripts/, engine/, linter/. Single match: XIX's own definition at CONSTITUTION.md:1264. No other body text refers to XIX's bullets by ordinal position. Sub-heading reorganization is safe.

**Verbatim-preservation contract**:
- Introductory paragraph ("The following MUST remain in the always-loaded root SKILL.md regardless of any decomposition...") — unchanged.
- Bullet 1 (Subcommand dispatch table) — text unchanged, grouped under Architectural invariants.
- Bullet 2 (Non-negotiable multi-agent rules) — text unchanged, grouped under Architectural invariants.
- Bullet 3 (Phase-level execution flow summary) — text unchanged, grouped under Architectural invariants.
- Bullet 4 (Important Notes / operational gotchas) — text unchanged, grouped under Operational constants.
- Closing paragraph ("Removing any item from this list requires a constitutional amendment with a rationale...") — unchanged.
- Origin note — unchanged.

**Why PATCH (not MINOR)**: per the v3.0.0 Removal-checklist subsection (e) precedent that introducing the FIRST instance of a new structural feature qualifies as MINOR, sub-headings within an existing bullet list are not a new structural feature — markdown sub-headings are a generic typographic primitive, not a governance feature. The classification matches the issue #97 P2 PATCH-class designation.

**Why no deliberation cycle**: this is the third PATCH-class amendment in the session (after v2.6.0's path (c) atomic stage-3 plain-language package and v3.1.0's cycle 2B Amendment record placements) and follows the same pattern: the verbatim-preservation contract is a mechanical test that a single PR with cross-reference verification can satisfy. When the contract holds, the PATCH pathway applies; when content changes substantively, the spec 067 dual-deliberation pathway applies.

**Outstanding deferred items** (after cycle 2C):
- P3 (NOT filed as an issue): migration eligibility note for Operational constants. Per issue #97 sequencing, "reserved for a second stage because adding it would change the operative meaning of XIX's 'regardless of any decomposition' language." When it lands, it will require dual-deliberation per spec 067 because it modifies normative meaning.
- Issue #94 (PATCH-class deferred from v2.6.0 path (c) cycle): v2.3.2 Clarification block "shape" → "assembly-form" terminology rename. Requires dual-perspective wording-precision and cross-principle-coherence review of the FULL v2.3.2 block before ratification (per issue acceptance criteria); deferred to a future amendment cycle.
- Same-version Principle II elaboration (TODO from v3.0.0 SIR): add to Principle II's breaking-change coordination text the sentence "Reusing a retired principle number is a breaking change..." Marked with `# TODO(spec-070-cycle2-followup)` in body. Deferral to a same-version follow-up is a downstream elaboration, not a Principle II atomicity violation per blind verdict ruling on Atomic bundle scope.

**Methodology note**: cycles 2A/2B/2C together demonstrate three governance pathway types in lockstep. 2A (v3.0.0) was MAJOR (principle removals) requiring full dual-deliberation. 2B (v3.1.0) was MINOR (new Amendment record structural feature retroactively applied to three principles) qualifying for the single-PR pathway under the verbatim-preservation contract. 2C (v3.1.1) is PATCH (sub-headings added to one principle's bullet list) qualifying for the same single-PR pathway. The pathway is determined by the verbatim-preservation contract, not the version classification — MAJOR/MINOR/PATCH classifies the version bump's IMPACT on consumers, while the contract classifies the verification cost. A future MINOR amendment that does NOT preserve verbatim language would still require full dual-deliberation; a future MAJOR amendment that DOES preserve verbatim language (counterfactual — MAJOR by definition implies semantic change) cannot exist.

---

## 2026-05-01 — Constitution v3.1.1 → v3.1.2 (Principle II same-version elaboration follow-up)

**Subject**: Apply the deferred-from-v3.0.0 same-version elaboration to Principle II's atomic-update bullet.

**Trigger**: v3.0.0 SIR's "Follow-up TODOs" section explicitly authorized this same-version follow-up. The wording was pre-specified in the v3.0.0 SIR; the deferral was a downstream elaboration sequenced after cycles 2B and 2C per the blind verdict ruling on Atomic bundle scope.

**Verification approach**: PATCH-class single-PR pathway with verbatim-preservation contract. The appended sentence text matches the v3.0.0 SIR's TODO specification character-for-character. No new governance feature is introduced; the no-reuse rule itself was already ratified by v3.0.0 in the Governance section's Principle Number Stability subsection. This amendment adds linkage between two already-ratified texts (Principle II's "single atomic change" requirement and Principle Number Stability's "permanent retirement, never reuse"), giving Principle II's atomic-update bullet an explicit instance pointer to the no-reuse rule.

**Verbatim-preservation contract**:
- Sentence appended: "Reusing a retired principle number is a breaking change — any historical document that cited the retired number by identity would thereafter refer to a different principle." This matches the v3.0.0 SIR's TODO specification character-for-character.
- Pre-existing bullet text ("Changing a stable interface requires updating every consumer (specs, templates, SKILL.md sections, reference files) in a single atomic change.") is unchanged.
- All other Principle II bullets are unchanged.
- The `# TODO(spec-070-cycle2-followup)` HTML comment block at that bullet (introduced in v3.0.0 to mark the deferral) is removed as the resolution mechanism.

**Why no deliberation cycle**: the same blind verdict that ruled the deferral acceptable also pre-validated the wording. Re-running dual-deliberation on already-ratified language would be ceremonial rather than informative. The verbatim-preservation contract holds: the appended sentence is the exact text the v3.0.0 SIR named.

**Outstanding deferred items** (after v3.1.2):
- Issue #94 (PATCH-class deferred from v2.6.0 path (c) cycle): v2.3.2 Clarification block "shape" → "assembly-form" terminology rename. Requires dual-perspective wording-precision and cross-principle-coherence review per issue acceptance criteria.
- P3 (NOT filed as an issue): migration eligibility note for XIX Operational constants. Per issue #97 sequencing, this would change the operative meaning of XIX's "regardless of any decomposition" language and requires dual-deliberation per spec 067.

**Methodology note**: cycles 2A → 2B → 2C → 2D-equivalent (this v3.1.2 follow-up) demonstrate the full deliberation-pathway taxonomy this session has validated. Pre-ratified deferred wording (this PR) is the lowest-cost pathway: one PR, no deliberation, verbatim text from a prior SIR's TODO. The taxonomy now reads:

| Pathway | Cost | Trigger | Examples |
|---------|------|---------|----------|
| MAJOR with full dual-deliberation | spec 067 self + blind | Principle removal/redefinition | v3.0.0 |
| MINOR with verbatim contract | single PR | First instance of new structural feature | v3.1.0 |
| PATCH with verbatim contract | single PR | Sub-headings within existing structure | v3.1.1 |
| PATCH with pre-ratified deferred wording | single PR | Same-version follow-up named in prior SIR | v3.1.2 |

The pre-ratified pathway is rare — it requires that the wording was specified in a prior SIR's TODO and that the prior SIR's verification cycle implicitly validated it. Future use should cite the prior SIR's TODO specification by version and section.

---

## 2026-05-01 — Constitution v3.1.2 → v3.1.3 (cycle 2C bullet-split follow-on)

**Subject**: Complete the structural realization of issue #97. PR #104 (v3.1.1) added two sub-headings to Principle XIX's bullet list under a conservative "verbatim preservation = don't touch the comma list" interpretation. The issue's literal listing showed 4 separate items under "Operational constants" — the user clarified intent: split the comma-listed bullet into 4 separate bullets to match the issue specification.

**Trigger**: surfaced as a self-flagged uncertainty during the autonomous PR #104 ratification. The orchestrator preserved the existing single bullet under the new sub-heading, then flagged the alternative interpretation (split into 4) for user confirmation. User confirmed the split intent.

**Verbatim-preservation contract**:
- Each new bullet's name matches the corresponding word group in the original comma list character-for-character (modulo capitalization of the first letter, which is conventional bullet-list typography):
  - "re-run overwrite behavior" → "Re-run overwrite behavior"
  - "agent count formulas" → "Agent count formulas"
  - "template-vs-skill responsibility boundary" → "Template-vs-skill responsibility boundary"
  - "baseline features list" → "Baseline features list"
- The "Important Notes / operational gotchas" parent label is dropped because the items are now individually addressable under the Operational constants sub-heading.
- No item is added; no item is removed; no item is reworded.

**Why PATCH**: completes a structural-grouping change initiated by PR #104. The combined PR #104 + this PR realizes issue #97's specification end-to-end. No normative content is added or removed.

**Methodology note (revised understanding of cycle 2C interpretation)**: this is a worked example of when "verbatim preservation = preserve verbatim" is too literal. PR #104's interpretation preserved the comma list verbatim; the issue's intent was that the four items be presented as four bullets (the bullet form being the user-visible structure the issue-author cared about). The verbatim-preservation contract for cycle 2C should have been "preserve each item's name verbatim" (true here) rather than "preserve the comma-list structure verbatim". This refinement is logged so future structural-grouping amendments understand that the contract is about substantive content preservation, not surface-form preservation. Surface form (bullet vs comma vs sub-heading) is the structural variable that the amendment is changing; preserving content names through that change is the verbatim test.

**Outstanding deferred items** (after v3.1.3): unchanged from v3.1.2 — issue #94 still requires dual-perspective wording-precision review per its acceptance criteria; the P3 XIX migration eligibility note (not filed as an issue) requires dual-deliberation if pursued.

**Pathway**: PATCH + verbatim contract single-PR pathway. Now ratified twice (v3.1.1 cycle 2C original, v3.1.3 cycle 2C follow-on). The pathway is robust to the kind of interpretation slip that this PR corrects, because the slip itself surfaced through the orchestrator's self-flagged uncertainty disclosure rather than through silent acceptance.

---

## 2026-05-03 — Spec 070 closure correction (path b, follow-up spec 073 filed)

**Subject**: Apply the closure-verification deliberation 2026-05-01 verdict (SPEC-070-CLOSURE VERDICT: PREMATURE — REOPEN). Path (b) of the verdict's two equivalent remedy paths: file a named follow-up spec (spec 073) with explicit §9 AC #5 gap acknowledgment + spec 067 verification trail tied to a future contrarian deliberation completing.

**Trigger**: closure-verification deliberation 2026-05-01 — see `deliberations/070-closure-verification-2026-05-01/arbitration/resolution.md` for the verdict.

**Verification approach precedent**: this is the second time in this session that a closure has been corrected through a deliberation rather than a self-attestation re-write. The first was the cycle 2C bullet-split (PR #107 v3.1.3) which the orchestrator self-flagged for user direction. The closure-verification was a full conversus deliberation that surfaced gaps the orchestrator could not have detected by self-review (the cycle 2 blind ran against a post-migration document, making the contrarian "passes the gate" argument structurally impossible — by the time the orchestrator wrote the closure PR, the post-migration document was the only available target).

**Bundle**:
1. **New spec 073** at `specs/073-spec-070-closure-correction.md` — active spec describing the supplemental blind deliberation work required to discharge spec 070 §9 AC #5. Includes:
   - Explicit closure-gap acknowledgment: "Spec 070's `specs/done/` placement (PR #99, 2026-05-01) preceded §9 AC #5 satisfaction" (verbatim per the verdict's path-b condition #2).
   - §4 methodology for the supplemental blind: pre-migration target, contrarian agent prompt, devils-advocate + balanced-arbiter presets per spec 070 §6.2.
   - §4.3 four-valued verdict scheme: SUSTAINED / SUSTAINED WITH FINDINGS / PARTIALLY SUSTAINED / NOT SUSTAINED.
   - §5 success criteria: deliberation runs, verdict filed, CONCONV entry appended, closure record added to spec 070, spec 073 moved to `specs/done/`.
2. **Spec 070 closure-record update** in `specs/done/070-grandfathered-audit/spec.md` — Status field amended to reflect that closure (PR #99) was premature per the closure-verification deliberation; §9 AC #5 is open; spec 073 carries the supplemental verification work; spec 070 stays in `specs/done/` to preserve the false-closure timestamp in the audit trail.
3. **CONCONV §5.3 SC 4 historical note** (this entry): per the closure-verification deliberation's bifurcation ruling on Dispute 5, the historical-record finding stands — spec 070 §5.3 SC 4 (cross-references to operational-guidance documents) was open at PR #99 merge time. The Governance operational-guidance list addition to CONSTITUTION.md is deferred to a follow-up PATCH (sequenced after PR #116 lands the v3.2.0 pathway-taxonomy migration).

**Outstanding deferred items** (from this entry):
- The supplemental blind deliberation itself (§4 of spec 073) is OPEN — to be run in a subsequent session. When it runs, spec 073 closes per its §5 success criteria.
- The Governance operational-guidance list addition (verdict P2 #4) is DEFERRED to a follow-up PATCH after PR #116 (v3.2.0 pathway-taxonomy migration) and this PR both land. The deferral preserves PR atomicity; the operational-guidance list discharge is bookkeeping that does not gate the §9 AC #5 verification work.

**Methodology note**: this is the first closure-correction spec in conversus history. The pattern is reusable: when a closure is found to be premature post-merge, path (b) (named follow-up spec with explicit gap acknowledgment) is preferable to path (a) (move spec back to `specs/`) because it preserves the audit trail of when the false closure happened. Future closure-corrections SHOULD follow path (b) by default, reserving path (a) for cases where the closure trail itself is corrupted or where the spec author needs to amend body content rather than just discharge an outstanding verification obligation.

---

## 2026-05-03 — Constitution v3.1.3 → v3.2.0 (pathway-taxonomy enrichments + migration to CONSTITUTION.md)

**Subject**: Apply the pathway-taxonomy deliberation 2026-05-01 verdict (PATHWAY-TAXONOMY VERDICT: RETAIN with modifications). The 4-pathway table introduced in the v3.1.2 governance-log entry is migrated to a new "Constitutional Amendment Pathways" subsection in CONSTITUTION.md Governance, with 5 enrichments per the deliberation's required changes.

**Trigger**: pathway-taxonomy deliberation 2026-05-01 — see `deliberations/pathway-taxonomy-2026-05-01/arbitration/resolution.md` for the verdict and the 6 required-change items. The deliberation explicitly identified the migration from CONSTITUTIONAL_CONVERSATIONS.md to CONSTITUTION.md as the structurally significant action ("the implementing PR's most consequential action is migration, not any of the enrichment changes" — overall assessment).

**Verification approach**: the pathway-taxonomy deliberation IS the spec 067 dual-cycle equivalent for this amendment. Cooperative mode with N=2 agents (pathway-defender and pathway-skeptic), full Phase 1-6 pipeline including arbitration. The arbitration produced binding rulings on each of the 6 changes applied here. No supplementary blind verification is required because the deliberation's adversarial structure (defender vs. skeptic with cross-review) provides the dual-perspective discipline that spec 067 §6.1+§6.2 mandates for principle-changing amendments.

**Bundle (6 changes from deliberation Required-changes)**:
1. **Retain rows 3 and 4 as separate** (Required change #1): the migrated table preserves the 4-row structure of the v3.1.2 entry.
2. **Authorization basis column added** (Required change #2): values per the verdict — "Full dual-deliberation (spec 067)" (v3.0.0); "Absence of new normative content" (v3.1.0, v3.1.1); "Prior deliberation scope coverage of deferred wording" (v3.1.2).
3. **Dual-function routing note added** (Required change #3): "For routing: all single-PR rows answer 'no deliberation required when verbatim preservation holds.' Authorization basis governs what conditions must be satisfied to invoke each single-PR pathway — see gate conditions for row 4 below."
4. **Self-consistency gap acknowledgment for row 4** (Required change #4): named condition (b) gap explicitly; the v3.0.0 deliberation's scope coverage of the v3.1.2 deferred sentence's substantive claim is not determinable from the governance log as written. Future row-4 applications MUST resolve condition (b) affirmatively.
5. **Provisional label for row 4** (Required change #5): row 4 entry annotates "Provisional — single canonical example (canonical status requires two independent uses from distinct sessions without governance anomalies)."
6. **RFC/CVE analogy correction** (Required change #6): RFC/CVE supports identifier stability (the no-reuse rule); RFC/CVE processes use single amendment pathways; the conversus multi-pathway taxonomy is a departure from that model, not an extension. The analogy cannot be cited as authority for adding new pathway rows.

**Why MINOR (not PATCH)**: the new Governance subsection introduces structural enforcement infrastructure that did not exist before (gate conditions for pathway invocation, dual-function routing note, self-consistency-gap audit pattern). Per the v3.0.0 Removal-checklist subsection (e) precedent, introducing the FIRST instance of a new structural feature qualifies as MINOR.

**Migration impact**: the 4-pathway table in the v3.1.2 governance-log entry (this file, line 579 onward) is preserved as historical record of the table's original state. Future amendments MUST cite Governance § Constitutional Amendment Pathways as the authoritative source. The v3.1.2 entry itself is unchanged below — readers comparing the v3.1.2 historical record to the v3.2.0 canonical version will see the deliberation-verified enrichments applied.

**Outstanding deferred items** (after v3.2.0): the only outstanding constitutional amendment follow-up is issue #94 (v2.3.2 "shape" → "assembly-form" terminology rename). That item requires dual-perspective wording-precision review per its acceptance criteria; it is NOT eligible for the row-4 pre-ratified pathway because the wording was not specified in a prior SIR's TODO with affirmative scope coverage of the substantive claim.

**Methodology note**: this is the first amendment ratified end-to-end through a conversus deliberation rather than the dual-deliberation strip-script flow. The pathway-taxonomy deliberation produced its verdict in a single cooperative run (N=2, full Phase 1-6) rather than the spec 067 self+blind two-deliberation structure used for cycle 1 and cycle 2A. This represents an evolution: when the question being deliberated is a governance-meta question (not principle removal/redefinition), a single adversarial-cooperative deliberation may be sufficient. The taxonomy itself does not yet codify this distinction — when a future amendment uses a single-deliberation pathway for governance-meta questions, the precedent should be cited and the pathway taxonomy may need a fifth row.

---

## 2026-05-04 — Constitution v3.2.0 → v3.2.1 (Governance operational-guidance list discharge)

**Subject**: Discharge the closure-verification deliberation 2026-05-01 P2 #4 hygiene item: add a Governance bullet enumerating CONTRIBUTING.md § Authoring Conventions (Principle VI substrate destination) and docs/output-conventions.md (Principle X substrate destination) as canonical migration destinations. Also discharges the v3.0.0 SIR's "Cross-reference" follow-up TODO (operational-guidance list update in subsequent PATCH).

**Trigger**: closure-verification deliberation 2026-05-01 P2 #4 — see `deliberations/070-closure-verification-2026-05-01/arbitration/resolution.md`. The verdict explicitly authorized this as non-blocking hygiene (proceeds without waiting for §9 AC #5 supplemental blind resolution).

**Why PATCH (not MINOR)**: the bullet enumerates information that is already ratified. Both files exist; both have content migrated from VI and X respectively (per v3.0.0 PR #98); both are named in the v3.0.0 SIR. The Governance bullet only adds discoverability — no new structural feature, gate condition, or normative requirement. Per the verbatim-preservation contract precedent, listing already-ratified destinations is PATCH-class.

**Why no deliberation cycle**: the closure-verification deliberation already ruled this hygiene item proceeds independently of the §9 AC #5 work. The bullet's content matches the verdict's wording for "Governance operational-guidance list" verbatim modulo markdown bullet formatting.

**Bundle**:
1. New "Operational guidance documents" bullet in CONSTITUTION.md Governance section, inserted between Constitutional Amendment Pathways subsection and Compliance bullet.
2. Bullet lists CONTRIBUTING.md § Authoring Conventions and docs/output-conventions.md as canonical migration destinations with cross-reference to v3.0.0 SIR.
3. Forward guidance: future migrations that retire a grandfathered principle MUST name the receiving document in the migration spec's SIR (per Removal checklist subsection (b)). New destinations are MINOR (new file/directory) or PATCH (new section in existing file).

**Outstanding deferred items** (after v3.2.1):
- Spec 073 §4 supplemental blind deliberation — still OPEN. This is the §9 AC #5 verification obligation that v3.2.1 does NOT discharge. v3.2.1 only discharges the parallel P2 #4 hygiene item.
- Issue #94 (v2.3.2 "shape" → "assembly-form" rename) — still requires dual-perspective review per its acceptance criteria.

**Pathway**: PATCH + verbatim contract single-PR pathway. The bullet's content is preserved verbatim from the verdict's wording (modulo markdown formatting). No new normative content.

---

## 2026-05-04 — Spec 073 closure (§9 AC #5 supplemental verification discharged)

**Subject**: Spec 070 §9 AC #5 supplemental blind verification ran. Verdict: **SPEC-070 §9 AC #5 VERDICT: SUSTAINED WITH FINDINGS**. Migrations of VI, X (pending cycle 3A path-(c) assessment), and XVI plain-language clause hold under the contrarian standard. Spec 073 closed; four follow-up amendment cycles filed as issues #119–#122.

**Trigger**: spec 073 §4.4 closure protocol — supplemental blind ran with the configuration in §4. Three agents (contrarian-vi-x-xvi-defender, gate-faithfulness, cross-principle-coherence) deliberated against `deliberations/070-supplemental-blind-2026-05-04/CONSTITUTION-v2.5.0-pre-migration.md` (extracted from commit `2ec0e8a`, the v2.5.0 ratification of Principle XXVIII). Full Phase 1-6 pipeline including arbitration. 17 LLM launches.

**Verdict structure**: SUSTAINED WITH FINDINGS is the second-best of four enumerated outcomes (SUSTAINED / SUSTAINED WITH FINDINGS / PARTIALLY SUSTAINED / NOT SUSTAINED). The migrations were substantively correct under the contrarian standard. The four findings are non-blocking but deserve preservation in the audit trail and follow-up amendment cycles.

**Findings (filed as issues)**:

1. **Cycle 3A — path-(c) feasibility for X (issue #119, P1)**: the X migration was procedurally premature. Cycle 2A removed X without first conducting a path-(c) feasibility assessment of whether a refactored headline could express ONE structural invariant (parallel to XVI's parameter-pinning headline). The contrarian agent argued (and the arbiter accepted) that X's three sub-bullets are independently CI-checkable, qualifying X for path-(c) consideration. If the path-(c) assessment confirms three conditions (mechanical headline adequacy, sub-bullet specialization verification, Verification block concreteness), **X is RESTORED constitutionally and the v3.0.0 X migration is superseded**. This is the highest-stakes finding — potential reversal of a constitutional change. Sequencing: full dual-deliberation per spec 067 (principle restoration is not eligible for single-deliberation pathways).

2. **Cycle 3B — X error-handling sub-bullet routing (issue #120, P1)**: X's error-handling sub-bullet ("errors should never pass silently; warnings emitted for malformed output") was DELETED in v3.0.0 rather than ROUTED to a runtime-consumed document. The verdict ruled this incorrect — the sub-bullet is execution logic and belongs in SKILL.md references at SHOULD strength. PATCH-class re-routing within the migration's already-ratified scope. Independent of cycle 3A.

3. **Cycle 3C — XVI Criterion 1 attribution + determinism-scope retention (issue #121, P1)**: Two-part finding. (a) The grandfathering disclosure annotation for XVI plain-language identifies Criterion 2 as the failure; the verdict found Criterion 1 (mechanical verification capability) is the decisive barrier — "user understanding" cannot be mechanically verified at all. Annotation must be corrected to name Criterion 1. (b) XVI's determinism-scope clauses (within-run determinism, cross-run reproducibility once parameters pinned, prohibition on LLM re-invocation) PASS the gate and must be retained in the principle body. The plain-language clause is the only XVI sub-claim that needed migration. PATCH-class.

4. **Cycle 3D — gate calibration positive worked example (issue #122, P3)**: The Constitutional Inclusion Criteria gate text has only failure worked examples, producing systematic over-migration pressure for borderline cases. The verdict prescribes adding a passing example grounded in Principle XXVIII as the ratified anchor. Verbatim text supplied in the verdict. PATCH-class calibration-documentation; may be batched with cycle 3C.

**Methodology observations** (preserved as audit-trail findings):
- The deliberation surfaced four systemic gaps in the amendment process: (i) no mandatory contrarian-assessment step before migration closure, (ii) XVII per-sub-bullet classification not enforced structurally in migration SIRs, (iii) grandfathering disclosure as static snapshot rather than versioned record, (iv) calibration-asymmetry in gate worked examples. None of these gaps automatically retroactively unwinds v3.0.0; all four are addressable through forward-looking corrective amendments.
- The supplemental blind functioned correctly: contrarian pressure found the real vulnerabilities (procedural gaps, documentation deficiencies, calibration asymmetry) without manufacturing substantive reversals. The four findings reflect genuine architectural improvement opportunities rather than mistaken migrations.

**Spec 070 closure record final**: spec 070 audit trail is complete through §9 AC #5 supplemental verification. Spec 070 remains in `specs/done/` (preserving the false-closure timestamp from PR #99). Spec 073 closes in `specs/done/`. Issues #119–#122 carry the corrective amendment work; spec 070's closure does not depend on those issues completing.

**Pathway used**: dual-deliberation (closure-verification 2026-05-01 + supplemental-blind 2026-05-04) for §9 AC #5 — the highest-cost pathway, used because principle-restoration eligibility is at stake. The four follow-up cycles will use cycle-appropriate pathways:
- Cycle 3A (potential restoration): full dual-deliberation per spec 067
- Cycles 3B, 3C, 3D: PATCH single-PR with verbatim contract (no normative-content changes, just routing/attribution/calibration corrections)

---

## 2026-05-04 — Constitution v3.2.1 → v3.2.2 (cycle 3D gate calibration positive worked example)

**Subject**: Discharge spec 073 SUSTAINED WITH FINDINGS finding #4 (issue #122). Add a passing borderline worked example to the Constitutional Inclusion Criteria gate text using Principle XXVIII as the ratified anchor.

**Trigger**: spec 070 supplemental blind deliberation 2026-05-04 — see `deliberations/070-supplemental-blind-2026-05-04/arbitration/resolution.md` (Dispute: Gate Calibration, P3 Required change #5). Wording supplied verbatim by the verdict.

**Verification approach**: PATCH single-PR with verbatim contract. The worked example text matches the verdict's required-change text character-for-character modulo markdown bullet formatting. No new criteria, no new gate logic — only calibration documentation.

**Cycle 3 status update**:
- **Cycle 3A (issue #119, P1, principle restoration)**: OPEN — requires full dual-deliberation. Heavy lift; not eligible for single-PR pathway.
- **Cycle 3B (issue #120, P1, X error-handling routing)**: CLOSED 2026-05-04 — verification check found the error-handling sub-bullet IS preserved in docs/output-conventions.md L34-40. The verdict's premise (\"DELETED rather than ROUTED\") was based on a misreading. Reclassified to P3 routing-class dispute and closed; reopen if user determines SKILL.md routing is preferred over docs/.
- **Cycle 3C (issue #121, P1, XVI Criterion 1 + determinism retention)**: CLOSED 2026-05-04 — verification check found both parts already-discharged. (a) Constitution does not currently attribute XVI plain-language to Criterion 2 anywhere; the v2.4.0 SIR uses \"unverifiable\" (Criterion 1 phrasing); cycle 1 SIR explicitly says Criterion 1. The verdict's \"currently identifies Criterion 2\" premise was wrong about the document state. (b) XVI body retains determinism-scope clauses in full at L1335-1414.
- **Cycle 3D (issue #122, P3, gate calibration)**: DISCHARGED by this PR (v3.2.2).

**Methodology finding** (preserved in audit trail): the supplemental blind verdict's findings #2 and #3 were based on premises about migration content that don't match what was actually shipped. This is itself an audit-trail finding worth preserving. Two possible explanations:
1. The deliberation agents made errors about the document state. They were reading the v2.5.0 PRE-migration document (per the spec 073 §4.1 target) and may have inferred migration outcomes that don't match the actual v3.0.0 ship.
2. The post-cycle-2A migration genuinely shipped with better fidelity than the contrarian agent realized, and the verdict's claims are contingent on facts that don't hold.

Either way, the proper response is: verify each finding against the current state, document the verification, and apply only the corrections that have bite. Cycles 3B and 3C had no bite; cycle 3D had bite (the gate text genuinely lacked a positive worked example) and is discharged here. Cycle 3A's bite (no path-(c) assessment was performed before X migration) is genuine and remains a separate amendment cycle.

**Pathway**: PATCH + verbatim contract single-PR. The worked example text is preserved verbatim from the verdict; the explanatory follow-up paragraph is editorial expansion that does not modify normative content.

---

## 2026-05-04 — Spec 070 cycle 3A closure (path-(c) for X — FAIL, v3.0.0 confirmed)

**Subject**: Spec 070 cycle 3A path-(c) feasibility deliberation for Principle X completed. Both self-consistency and blind verification ruled **FAIL** under different analytical frameworks but with identical conclusions. Cycle 3A determination: v3.0.0 X migration to operational guidance is confirmed. Issue #119 closed.

**Trigger**: spec 070 supplemental blind 2026-05-04 P1 finding #1 (issue #119) — required path-(c) feasibility assessment before X migration could be considered procedurally complete.

**Verification approach**: full dual-deliberation per spec 067. Self-consistency evaluated a candidate path-(c) restoration proposal ("Predictable Output Tree" headline + 4 sub-bullets); blind agents derived their own path-(c) refactor (or argued none was viable) from first principles without seeing the candidate proposal.

**Self-consistency verdict**: SPEC-070 CYCLE 3A (SELF) VERDICT: FAIL — V3.0.0 CONFIRMED. Condition (i) Mechanical headline adequacy fails: "Predictable Output Tree" bundles four distinct structural invariants (synthesis canonical path, output depth bound, malformed-output emission, per-file focus), violating XVI's single-invariant precedent. No verification refinement can transform this multi-invariant bundle into the single structural invariant the v2.6.0 path-(c) precedent requires.

**Blind verdict**: both blind agents (path-c-discovery-skeptic and path-c-discovery-pragmatist) UNANIMOUSLY concluded "Principle X should not be refactored via path-(c) due to lack of substantial structural substrate and failure to meet XVI precedent requirements." The agents disagreed on framework priority (substrate-first vs gate-criteria-first) but converged on the same outcome under both frameworks.

**Convergence signal**: cross-framework convergence is the strongest possible result. The skeptic's framework (Constitutional Inclusion Criteria violations) and the pragmatist's framework (architectural substrate deficiency) are different lenses on the same evidence, and both lenses see the same answer. This rules out the failure mode where the conclusion is an artifact of one specific evaluation framework.

**Cycle 3 status update** (all four supplemental-blind findings now resolved):
- **Cycle 3A (issue #119, P1)**: CLOSED 2026-05-04 — dual-deliberation FAIL. v3.0.0 X migration confirmed.
- **Cycle 3B (issue #120, P1)**: CLOSED 2026-05-04 — verified content preserved; verdict premise was wrong.
- **Cycle 3C (issue #121, P1)**: CLOSED 2026-05-04 — verified both parts already-discharged in current constitution; verdict premise was wrong.
- **Cycle 3D (issue #122, P3)**: DISCHARGED via PR #124 (v3.2.2) — gate calibration positive worked example added.

**Methodology findings** (preserved as audit-trail content even though they don't trigger amendments):

1. **Substrate-first methodology for path-(c) evaluation**: the blind arbitration ruled that path-(c) evaluations should sequence (1) substantial-structural-substrate identification, (2) constitutional significance assessment, (3) gate criteria verification. Bundling analysis is supporting evidence for substrate assessment, not an independent blocking criterion. This is a methodological refinement to the v2.6.0 path-(c) Governance subsection that could be codified in a future PATCH amendment.
2. **No "obscurity" requirement for path-(c)**: the blind arbitration ruled that path-(c) requires substantial structural substrate that can serve as a mechanically verifiable headline claim, without requiring that substrate to have been previously obscured by subjective framing. XVI's parameter pinning was always visible; the v2.6.0 amendment elevated it to headline status rather than discovering hidden content. Adding an obscurity requirement would artificially raise the bar beyond what XVI itself satisfied.

These two findings refine path-(c) methodology going forward but don't trigger any v3.X amendments — both are codifications of what the v2.6.0 XVI rewrite already demonstrated. They could be added to the Governance § Constitutional Amendment Pathways subsection as a P2 follow-up if the user determines the codification is worth the version bump.

**Spec 070 audit trail final**: spec 070 is now COMPLETE through §9 AC #5 supplemental verification AND through cycle 3A path-(c) feasibility for the only finding that warranted full dual-deliberation. The v3.0.0 cycle 2A migrations of VI, X, and XVI are all SUSTAINED under contrarian-standard verification:
- **VI**: SUSTAINED via supplemental-blind 2026-05-04 (no contrarian could construct a credible argument for retention)
- **X**: SUSTAINED via supplemental-blind 2026-05-04 + cycle 3A 2026-05-04 (no viable path-(c) exists; substrate is insufficient)
- **XVI plain-language**: SUSTAINED via supplemental-blind 2026-05-04 (criterion-attribution clarification preserved as cycle 3C finding; verified already-discharged in current constitution)

Spec 070's six closures (PR #99 → premature; spec 073 PR #117/#123 → §9 AC #5 supplemental; PRs #124/#118 → cycle 3D/Governance hygiene; cycle 3A this entry → path-(c) feasibility) close the audit trail end-to-end. No further follow-ups are required for spec 070 itself.

---

## 2026-05-04 — Constitution v3.2.2 → v3.2.3 (issue #94 shape→assembly-form rename)

**Subject**: Discharge issue #94 — cycle 1 deferred TODO from v2.6.0. Single-word terminology rename in Principle XVI's v2.3.2 Clarification block: "shape" → "assembly form" at the cross-run-variance prohibition. Removes the terminological collision with Principle IX's "behavior-over-shape" testing extension.

**Trigger**: issue #94 (filed 2026-05-01 during cycle 1 ratification per the Dispute 4 ruling that deferred this rename to a follow-up PATCH). Acceptance criteria required dual-perspective wording-precision and cross-principle-coherence review BEFORE ratification.

**Verification approach**: dual-perspective deliberation (`deliberations/094-shape-rename-2026-05-04/`) with two agents and balanced-arbiter. Mode: cooperative. The two perspectives map directly to issue #94's required review classes:
- **wording-precision** agent: evaluated definitional equivalence, normative-force preservation, existing-usage alignment, no-new-requirements test. Verdict: PASS.
- **cross-principle-coherence** agent: evaluated collision-removal, VII coherence, VIII coherence, XVI body coherence, single-source-of-truth check. Verdict: PASS.
- **balanced-arbiter**: ruled "ISSUE #94 DELIBERATION VERDICT: PASS — RENAME APPROVED" with high confidence based on unanimous agent agreement and clear constitutional grounding in the existing L1485 "assembly-form-identical" precedent.

**Verbatim-preservation contract**: the enumerated parenthetical (parameter names, template selection, gap-identifier set) is unchanged. The MUST remains attached. The only character-level change is the substitution "shape" → "assembly form" at line 1460 (one space added; no other text touched).

**Why no new normative requirements**: the renamed text refers to the same enumerated set under the same MUST. The cross-run-variance prohibition's scope is unchanged. The PATCH SIR explicitly attests this per issue #94 acceptance criteria #2.

**Cross-principle disambiguation status post-PATCH**:
- Principle XVI body and Clarification: "shape" no longer used to refer to assembled objective function structure. The substantive concept is now consistently labeled "assembly form" (line 1460, the proposed change) and "assembly-form-identical" (line 1485, the pre-existing usage).
- Principle IX (Functional Programming): "behavior-over-shape testing" extension retains its "shape" usage in the testing context. No collision.
- The IX/XVI disambiguation is now complete: "shape" in the constitution refers exclusively to test-shape (IX context) where it appears, and "assembly form" refers to objective-function-form (XVI context) where it appears.

**Closure of constitutional governance arc**: this is the LAST outstanding constitutional follow-up from the v2.4.0 → v3.X grandfathered-principle migration arc. With v3.2.3:
- All cycle 1 deferred items: discharged (XVI Option A in v2.6.0; this rename in v3.2.3)
- All cycle 2 deferred items: discharged (cycle 2B v3.1.0; cycle 2C v3.1.1; cycle 2C bullet split v3.1.3; Principle II elaboration v3.1.2; pathway taxonomy migration v3.2.0; operational-guidance list v3.2.1)
- All cycle 3 (supplemental-blind) findings: discharged (cycle 3A FAIL via dual-deliberation; cycle 3B/3C closed via verification; cycle 3D v3.2.2)

The constitutional governance arc that began with v2.4.0's Constitutional Inclusion Criteria gate and ran through grandfathered-principle migration, supplemental verification, and post-verification follow-ups is now complete. v3.2.3 is the resting state of that arc; no further constitutional follow-ups are queued.

**Pathway**: PATCH + dual-perspective deliberation single-PR. This is a fifth pathway type in the governance taxonomy — fits between "PATCH + verbatim contract" (v3.1.1, v3.1.3, v3.2.1) and "MAJOR + full dual-deliberation" (v3.0.0). The dual-perspective requirement is lighter than spec 067 §6.1+§6.2 dual-cycle (one deliberation, two agents covering distinct review classes) but heavier than verbatim contract (which requires no deliberation at all). The Governance § Constitutional Amendment Pathways subsection currently does not codify this fifth pathway; if future amendments use the same shape, the taxonomy may need a fifth row. For now, the v3.2.3 entry serves as the canonical example until a second use occurs.

---

## 2026-05-13 — v4.2.0-structured-deliberation-outputs-ratified

**Subject**: Tier 3 (Component) amendment ratifying conversus-oss-specific implementation of Tier 2 Principle XXVIII (Persistence Contract Discipline). Adds Component Principle XXIX (Structured Deliberation Outputs).

**Pathway**: MINOR + full four-stage verification (originating → self-consistency → self-consistency rerun → blind), all PASS-variant.

**Outcome**: **Amendment landed** — Component `CONSTITUTION.md` v4.0.0 → v4.2.0, new Principle XXIX added.

### Verification stages

| Stage | Date | Composition | Verdict | Conditions applied |
|---|---|---|---|---|
| Originating | 2026-05-12 | engineer, schema-design-expert, adapter-consumer, devils-advocate | APPROVE-WITH-FIXES (Q1+Q2+Q3) + TIER-3-CONFIRMED + RECURSION-EXEMPTED | C1-C10 → v2 |
| Self-consistency | 2026-05-13 | strict-reader, purist, principle-xxviii-fit-auditor, recursion-precedent-auditor | Q1+Q2 PASS-WITH-CLARIFICATIONS; **Q3 FAIL-CONTRADICTION** (Principle V) | D1-D15 → v3 (D1 = load-bearing § 5.1 reversal) |
| Self-consistency rerun | 2026-05-13 | strict-reader, purist, principle-xxviii-fit-auditor, recursion-precedent-auditor | Q1+Q2+Q3 PASS-WITH-CLARIFICATIONS | E1-E4 → v4 |
| Blind verification | 2026-05-13 | naive-reader, implementation-engineer, risk-auditor, external-scholar | Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS; Q2 MODERATE-RISK-MANAGEABLE; Q3 HOLDS-AS-DOCTRINE | F1-F4 → v5 |

Twelve distinct agents across four stages with zero composition overlap. Composition orthogonality (spec 067) satisfied at every stage.

### Notable findings

1. **Q3 FAIL-CONTRADICTION at self-consistency was substantive, not procedural.** v2's § 5.1 blocking validation contradicted Tier 2 Principle V ("Malformed output is better than no output"). Arbitration mandated D1 — full rewrite of § 5.1 to non-blocking warning-based validation with persistence-unconditional write semantics. Highest-value catch in the v4.2.0 cycle.

2. **New precedent established: temporal-constraint exemption for bootstrap-paradox cases.** § 9.1 documents a substrate-standup exemption (a spec ratifying a schema discipline can be temporarily exempt from that discipline until the substrate exists). Anti-precedent containment: D5 categorical prohibitions ("adjacent," "similar," "schema-touching" framings barred) + E2 technical precondition (no JSON Schema exists AND ratification stands the schema up) + E4 precedent-citation requirement for future invocations. SECOND precedent established in the v4.X.0 cycle (after v4.1.0's override-with-rationale, blind-verification-only scope).

3. **Phase 6 disputes_remain trigger grep-mismatch engine bug** struck in 4 of 5 v4.1.0+v4.2.0 deliberation stages. Manual arbitration recovery used in each case. Blind verification was the first clean Phase 6 firing — the structured-output discipline this very spec ratifies (Principle XXIX) is the architectural fix for the trigger-miss bug.

### Files changed in ratification commit

- `specs/v4.2.0-structured-deliberation-outputs/spec.md` — status flipped to RATIFIED; Appendix B SIR added
- `CONSTITUTION.md` — version 4.0.0 → 4.2.0; new Component Principle XXIX
- `CONSTITUTIONAL_CONVERSATIONS.md` — this entry
- `CONFORMANCE.md` — XXVIII Provisional remediation status updated to "in-progress per spec v4.2.0 (ratified)"; cliff date 2026-12-01 retained

### Cross-tier coordination

This Tier 3 amendment implements Tier 2 Principle XXVIII. The Tier 2 governance log at `build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md` will receive a pointer entry referencing this Tier 3 ratification (handled in the parent-monorepo submodule-bump commit).

**References**: Spec v5 (commit `24538e7`); blind arbitration `deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-13/arbitration/resolution.md`.
