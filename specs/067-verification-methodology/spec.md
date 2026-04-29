# Feature Specification: Constitutional Verification Methodology — Both Self-Consistency AND Blind

**Feature ID**: `067-verification-methodology`
**Created**: 2026-04-26
**Status**: Draft v2 — re-verification trigger + cost reporting added 2026-04-27
**Depends On**: `066-constitution-v2.3.0` (which §7 this spec supersedes)
**Governed by**: `CONSTITUTION.md` Governance section — amendment process
**Originating context**: 2026-04-25 v2.3.0 deliberation chain. Self-consistency verification (per spec 066 §7) ruled `PASS WITH FIXES` but with *process meta*, not content fixes — agents read the v2.3.0 markers and pivoted into "ratify the additions" mode. A subsequent blind verification (markers stripped) found 3 substantive content issues the self-consistency run missed, including a logical contradiction in Principle XVI that **predated the v2.3.0 amendment by months**. See `CONSTITUTIONAL_CONVERSATIONS.md` 2026-04-25 entries for full chain.

> **Scope discipline**: This spec amends the verification protocol that constitutional amendment specs must satisfy before merging their implementation PR. It does NOT amend any constitutional principle. It does NOT change the deliberation engine. It changes the **acceptance bar** that future amendment specs must meet, codifying the lesson surfaced 2026-04-25.

---

## 1. Summary

Spec 066 §7 prescribed a single verification deliberation against the proposed amended text, with acceptance bar "0 disputes raised." That protocol has a structural flaw: the agents and arbiter receive the amended text *with* its v2.3.0 markers (Sync Impact Report, "Extension (v2.3.0)" labels, "Origin: PR #X" attributions). These markers anchor agents into "ratify the recent additions" mode — a confirmation bias that prevents the verification from catching:

- Principles that aren't worth their constitutional bandwidth (the agents' job becomes "approve" not "audit").
- **Pre-existing flaws revealed by the audit** — e.g., a logical contradiction in Principle XVI that the blind verification caught because it had no signal to focus only on "what changed."
- Wording or scope issues that survive specifically *because* they look approved.

The 2026-04-25 v2.3.0 deliberation chain demonstrated this empirically: self-consistency produced process-meta findings; the same agents reviewing a stripped version produced concrete content findings. The methodology lesson is general: **self-consistency catches drift in the recent additions; blind catches problems anywhere in the document — including longstanding ones recent reviewers have stopped questioning.**

This spec amends the verification protocol to require **both** methodologies for every constitutional amendment, with combined acceptance bar.

## 2. Goals

1. Future amendments cannot land with only self-consistency verification.
2. Both methodologies must run; both must produce verdicts.
3. The blind methodology has a normative stripping recipe so future implementers don't have to invent it.
4. Pre-existing flaws surfaced by the blind run get explicit handling — they can be deferred (out of the current amendment's scope) but cannot be silently ignored.
5. The combined acceptance bar is concrete enough that a CI hook could, in principle, enforce it.

## 3. Non-goals

- **Replacing the conversus engine.** Both verifications run in conversus today.
- **Mandating which agents to use.** The number and roles of review agents stay at the amendment author's discretion.
- **Mandating a maximum cost budget.** Verification cost is a function of agent count + rounds; this spec doesn't cap it.
- **Retroactive verification.** v2.2.0 and earlier amendments don't get re-verified by this protocol. Future amendments only.

## 4. The amended verification protocol

Replace spec 066 §7 with the following (this spec is the canonical text; spec 066 §7 is superseded as of merge):

### 4.1 Both methodologies are required

Every constitutional amendment spec MUST include verification deliberation results from both:

- **Self-consistency verification**: agents review the amended text *with* version markers, Sync Impact Report header, and Origin attributions visible. Arbiter grounded in the amended text. Catches: wording drift between spec and implementation, mechanical inconsistencies in the recent additions, scope creep.
- **Blind verification**: agents review the amended text with version markers stripped. Arbiter grounded in the stripped text. Agents and arbiter explicitly told they do not know which principles are recent. Catches: principles that don't earn their bandwidth, contradictions anywhere in the document, pre-existing flaws.

The two methodologies test orthogonal failure modes. Either alone is insufficient.

### 4.2 Stripping recipe (normative)

To produce the blind target text, the implementer MUST:

1. **Remove the Sync Impact Report HTML comment** at the top of the constitution.
2. **Remove version markers** from new principles. Specifically: `**Extension (vX.Y.Z):**` → `**Extension:**`; any prose-level `(vX.Y.Z)` mentions inside principle bodies are removed.
3. **Strip Origin attributions referencing the originating deliberation or specific PRs** *for the new/extended principles only*. Existing pre-amendment Origin lines (e.g., spec 005, spec 011a) are preserved — they're not anchoring artifacts of the current amendment.
4. **Anonymize the version footer** to "(under review)" instead of the candidate version number.
5. **Verify zero leakage**: grep the stripped text for the candidate version string (e.g., "v2.3.0", "2026-04-25"). 0 matches required.

The resulting file lives at `deliberations/{amendment-slug}-blind-verification-{date}/CONSTITUTION-blind.md`.

### 4.3 Agent framing for the blind run

Blind-run agent prompts MUST NOT mention:

- The candidate version number
- The originating deliberation
- The PRs whose evidence the amendment was derived from
- That the document is under review for an amendment

Blind-run agent prompts SHOULD include explicit instructions to consider **removing** principles that don't earn their keep. The default conversus deliberation framing leans toward additive recommendations; blind verification needs prompts that empower subtractive judgments.

### 4.3.1 Use existing role presets — do NOT hand-roll

The conversus presets directory already supplies the role personas this methodology needs. Future blind verifications MUST use these presets rather than hand-roll new agent prompts:

| Role purpose | Preset | Composable? |
|---|---|---|
| Skeptical reviewer that challenges agreed-upon positions | `preset: devils-advocate` | yes — compose with a domain modifier (e.g. `[devils-advocate, security]`) |
| Adversarial reviewer that seeks to break a position | `preset: red-team` | yes |
| Independent arbiter that issues binding rulings grounded in a declared framework | `preset: balanced-arbiter` | no — used standalone |

Hand-rolled equivalents (e.g., the 2026-04-25 blind run's `skeptic` / `skeptic-2` / `practitioner` agents) duplicate work and produce inconsistent framing across amendment cycles. The presets exist precisely to make this methodology reusable. If a needed role is *not* in `presets/role/`, the appropriate move is to ADD it to the preset registry — not to inline a one-off prompt in the verification config.

The 2026-04-25 blind run that motivated this spec did NOT use these presets — that was a methodology mistake the spec is correcting prospectively. The deliberation outputs remain valid, but future runs use the presets.

### 4.4 Combined acceptance bar

The amendment's implementation PR may merge only if:

- **Self-consistency**: 0 ACCEPT-level findings on the amendment package's wording. PASS or PASS WITH FIXES that name only wording-precision corrections (which the implementer applies and re-verifies).
- **Blind**: 0 ACCEPT-level findings on the new/extended principles specifically. Findings on **pre-existing principles** (e.g., the XVI logical contradiction surfaced 2026-04-25) are explicitly out of scope for the current amendment but MUST be filed as deferred follow-ups in `CONSTITUTIONAL_CONVERSATIONS.md` with a follow-up spec linked.

If either run produces ACCEPT-level findings on the amendment itself, the implementer applies fixes and re-runs the affected verification before merging. Re-running both is not required if only one run flagged the issue.

**Re-verification after fixes** (added v2 2026-04-27): when ACCEPT-level findings are folded into the implementation PR, the affected methodology MUST be re-run before merge. The acceptance bar is "0 ACCEPT-level findings on the as-merged text," not "0 ACCEPT findings on the originally-deliberated text." A merge with fixes applied but not re-verified is a methodology violation.

The 2026-04-27 post-v2.4.0 gap analysis surfaced this gap retroactively: the spec 068 (PR #29) and spec 069 (PR #32) implementations merged with 7 and 3 ACCEPT fixes respectively, without re-running the affected verification. Future implementation PRs MUST schedule re-verification before merge. Implementations already merged are grandfathered (the gap analysis doesn't retroactively block them) but the re-verification finding stands as a methodology lesson.

**Practical implementation**: re-run only the methodology that produced ACCEPT findings. If self-consistency had 0 ACCEPT and blind had 4, only re-run blind after fixes. If both had ACCEPTs, re-run both. The cost of re-verification (~17 launches per methodology) is part of the methodology's discipline.

### 4.5 Documentation in `CONSTITUTIONAL_CONVERSATIONS.md`

Both verification deliberations MUST be filed as separate entries in `CONSTITUTIONAL_CONVERSATIONS.md`. Each entry includes:

- The methodology used (`self-consistency` or `blind`)
- The arbiter's verdict line
- Findings categorized as ACCEPT / REJECT / DEFER per arbiter ruling
- For DEFER findings, what would unblock acceptance (e.g., "needs own spec," "needs more evidence")
- The methodology cost (agent launches consumed across all phases including arbitration). Format: "Cost: ~N launches" inline with the verdict line.
- Re-verification status (when the implementation PR included fixes): whether re-verification ran, what its verdict was, what its cost was. Format: a "Re-verification" sub-section after the main verdict.

The 2026-04-25 entries (both methodologies) serve as the canonical example — see them for format.

### 4.6 Test-fix discipline during verification

*Added 2026-04-29 per spec 071 §8 (Principle XXVIII implementation).*

When a verification deliberation surfaces failing tests in the deliberation's target codebase, the implementer MUST run the **4-subagent investigation pattern** (root-cause categorization per Principle XXVIII categories — fixture drift / production bug / legitimate test bug / defunct test) BEFORE proposing fixes.

**Why this is binding**: a naive "make tests pass" sweep buries the failure mode this protocol exists to surface. The 2026-04-28 spec 045 verification (canonical exemplar) surfaced 95 failing tests, of which 1 was a production bug (engine/handlers.py import shadowing — PR #42), ~70 were mechanical fixture-path drifts, and 3 were legitimate test bugs. Without the discipline, the production bug would have been mislabeled as fixture drift and shipped silently. Categorization is the load-bearing primitive of Principle XXVIII; this section binds spec 067 verification deliberations to that primitive.

**The pattern**:

1. Dispatch one subagent per category (4 total, parallel) with read-only access to the failing-test surface. Each subagent triages each failing test against its assigned category, returning a per-test verdict ("yes this is fixture drift", "no this is actually a production bug", or "doesn't fit my category").
2. The implementer collates the 4 verdicts. Tests with single-category consensus are categorized; tests with multi-category disagreement get a 5th investigation pass to resolve.
3. Categorization MUST be ratified by the implementer BEFORE any fix lands. Diffs that change the categorization mid-PR violate Principle XXVIII clause 2's diff-shape consistency check.
4. The PR description for the fix MUST cite this section (`spec 067 §4.6`) and link the categorization output (deliberation directory or equivalent artifact).

**Reference implementation**: PR #42 (conversus-oss, merged 2026-04-28). Future PRs that exercise this pattern SHOULD link back to PR #42 as exemplar until enough exemplars exist (~3) to consolidate into a SKILL.md.

**Out of scope for this section**: failing tests that arise outside a verification deliberation. The 4-subagent pattern is specifically scoped to verification-surfaced failures because that's the case where naive sweeping is most tempting (the implementer is under pressure to clear the verification gate). Other failing-test contexts retain their existing discipline (Principle XXVIII applies regardless; this section adds the verification-deliberation-specific pre-investigation requirement).

## 5. Acceptance criteria for this spec

This spec is "done" when:

1. The protocol §4 is reviewed and approved.
2. The stripping recipe §4.2 is mechanical enough that a Python script could implement it.
3. A follow-up implementation PR amends the relevant tooling — at minimum, a `scripts/strip-constitution-for-blind.py` reference implementation that takes `CONSTITUTION.md` + a version string and emits the blind text.
4. Spec 066 §7 is annotated as superseded with a forward-reference to this spec.

## 6. Open questions

- **Q1**: Should the verification deliberations be required to use *different agent personas* between self-consistency and blind? Argument for: prevents the same agent from importing self-consistency framing into the blind run. Argument against: agent personas are already different by purpose (wording-precision vs skeptic), and re-using a registry of personas keeps deliberations comparable across amendments. Recommend: NOT required, but RECOMMENDED.
- **Q2**: Should the implementer be allowed to run *only the blind* methodology (skipping self-consistency) if they're confident in the wording? Argument for: blind catches everything self-consistency catches. Argument against: blind agents told "you don't know history" can't notice a wording change *between spec text and implementation text* — that's exactly what self-consistency is for. Recommend: NO, both are required.
- **Q3**: Should verification cost be reported in the entry? Useful for budgeting future amendments. Recommend: YES, include "Cost: ~N launches" in each entry.

## 7. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Blind verification surfaces a defect in a *new* principle that the self-consistency run already approved | High | Acceptance bar §4.4 requires 0 ACCEPT-level findings on either run for the amendment to merge. Disagreement between runs is itself a signal — block merge until reconciled. |
| Blind verification surfaces *too many* pre-existing flaws to handle in the current amendment cycle | Medium | §4.4 carves out pre-existing flaws as DEFER-with-follow-up. The current amendment isn't blocked, but the issues become tracked work. |
| Stripping recipe leaks a version marker due to a regex bug | Medium | §4.2.5 requires zero-leakage verification (grep for candidate version string). A reference script (§5.3) reduces the chance of hand-edit errors. |
| Implementers skip the blind run "to save time" | High | This spec makes both methodologies required. CI cannot enforce it (it's a process check), but the audit trail in `CONSTITUTIONAL_CONVERSATIONS.md` makes skips visible to reviewers. |

## 8. References

- Spec 066 — Constitution v2.3.0 amendment package (this spec supersedes §7)
- `CONSTITUTIONAL_CONVERSATIONS.md` — 2026-04-25 entries (self-consistency + blind, the empirical motivation)
- `deliberations/v2.3.0-verification-2026-04-25/` — self-consistency outputs (process-meta verdict)
- `deliberations/v2.3.0-blind-verification-2026-04-25/` — blind outputs (3 substantive findings, including pre-existing XVI contradiction)
- `deliberations/post-v2.4.0-gap-analysis-2026-04-27/` — source of v2 amendments (re-verification trigger §4.4 + cost reporting §4.5); see `arbitration/resolution.md` for the binding decisions and the spec 068/069 grandfathering note
- CONSTITUTION.md Governance section — amendment process
