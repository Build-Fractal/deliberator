# Feature Specification: Audit Grandfathered Principles (VI, X, XVI) Against the v2.4.0 Constitutional Inclusion Gate

**Feature ID**: `070-grandfathered-audit`
**Created**: 2026-04-27
**Status**: Draft v1 — awaiting verification deliberations (per spec 067)
**Depends On**: `069-mechanical-verification-gate` (defines the gate this spec audits against), `067-verification-methodology` (defines the verification protocol the implementation PR must satisfy)
**Governed by**: `CONSTITUTION.md` Governance section — amendment process. This spec is governance-meta: it audits existing principles against criteria already in force. The implementation follow-up (which would actually edit `CONSTITUTION.md` to migrate any failing principle) is governed by the same MAJOR/MINOR/PATCH rules as any constitutional amendment.
**Originating context**: 2026-04-27 post-v2.4.0 gap analysis (`deliberations/post-v2.4.0-gap-analysis-2026-04-27/`). After v2.4.0 landed (spec 069), a gap-analysis deliberation reviewed what the new Constitutional Inclusion Criteria gate implied for the principles that were grandfathered. The arbitration recommended a follow-up spec that formally audits the three grandfathered principles spec 069 §5 flagged (VI, X, XVI), proposes operational-guidance migration paths for any that fail the audit, and preserves the audit trail for any that pass.

> **Scope discipline**: This spec audits **three specific principles** (VI, X, XVI) against the v2.4.0 gate. It does NOT propose any new principle. It does NOT directly edit any principle text in `CONSTITUTION.md` — actual migration of a failing principle to operational guidance would be a separate, intentional implementation PR that this spec authorizes but does not perform. It does NOT re-audit principles spec 069 §5 already classified as passing.

> **Recursive concern**: this spec uses the v2.4.0 gate to evaluate principles that v2.4.0 explicitly grandfathered. The grandfathering provision (spec 069 §4.1, last paragraph) anticipates this exact follow-up: *"Migrating any of them to operational guidance is a separate, intentional act governed by the same amendment process (with the receiving document identified explicitly in the migration spec)."* This spec is the migration spec for VI, X, and XVI. It applies the gate as the audit rubric, not as retroactive enforcement.

---

## 1. Summary

The Constitutional Inclusion Criteria gate (added in v2.4.0 by spec 069) is **prospective**: it applies to amendments after v2.4.0, and existing principles I-XXVII are grandfathered. Spec 069 §5 included a non-binding worked-examples analysis that classified each existing principle as passing or failing the gate today. Three principles were flagged as failing:

- **VI Scripts Over Markdown** — judgment call about "drives behavior" vs "human orientation"
- **X Zen of Python Output** — aesthetic judgment, not falsifiable
- **XVI Mathematical Transparency** — "user understanding" cannot be mechanically verified

Grandfathering is appropriate as a transition mechanism but should not be permanent for principles that genuinely fail the gate. Permanent grandfathering creates a two-tier constitution: principles held to the new bar, and legacy principles that survive only because they predate the bar. That two-tier structure undermines the gate's claim that the constitution is the home for invariants and operational guidance is the home for judgment calls.

This spec performs a formal, criterion-by-criterion audit of VI, X, and XVI. For each principle that fails the audit, it proposes a specific operational-guidance target (CONTRIBUTING.md, the relevant SKILL.md, a domain spec, or a new reference document) and a one-paragraph summary of what the migrated guidance should say. For any principle that turns out to pass on closer inspection, it documents the reasoning so the spec 069 §5 verdict is overturned in the audit trail rather than silently. The actual migration — editing `CONSTITUTION.md` to remove or rewrite the principle and adding the corresponding operational guidance — is a separate implementation PR, governed by spec 067's verification protocol.

## 2. Goals

1. **Per-principle gate audit** — apply each of the three v2.4.0 criteria (mechanical verification capability, falsifiable scope, distinct from existing principles) to VI, X, and XVI individually, with reasoning per criterion and a per-criterion verdict.
2. **Migration path proposal** — for each principle that fails the audit, identify a specific operational-guidance target document and outline the content the migrated guidance should carry, so the implementation PR has a concrete starting point.
3. **Risk register for migration** — surface the risks that come with moving a principle out of the constitution (loss of enforcement weight, future authors not consulting the new home, fragmentation of guidance across many documents) with proposed mitigations.
4. **Preserve audit trail for principles that pass review** — if closer analysis flips a spec 069 §5 "would fail" verdict to "actually passes," document that reasoning explicitly so the precedent is on the record.
5. **Authorize, but do not perform, the implementation PR** — this spec produces the audit and the migration plan; the implementation PR (the actual `CONSTITUTION.md` edit + operational-guidance content addition) is filed separately and verified per spec 067.

## 3. Non-goals

- **Auditing principles spec 069 §5 already classified as passing**. The other 24 principles are out of scope. If the audit of VI/X/XVI surfaces a methodology that should be applied broadly, that is a future spec.
- **Migrating any principle in this spec**. No `CONSTITUTION.md` edits are proposed here. Migration is the implementation PR's job, gated on this spec's acceptance criteria.
- **Redefining the v2.4.0 gate criteria**. The audit applies the gate as written. If the audit reveals the gate is too strict or too lax, that is grounds for a future amendment to spec 069 / `CONSTITUTION.md`, not for adjusting the rubric mid-audit.
- **Retroactive enforcement against principles that pass the audit**. A principle that passes the audit stays in the constitution unmodified. The grandfathering provision still protects principles in this slate that turn out to pass on review — they are no longer at risk of migration even by this audit's conclusion.
- **Litigating the spec 069 §5 verdicts in this spec's narrative**. Q1 in §8 acknowledges they may need their own deliberation; this spec's body proceeds as if §5's three flags are the right slate to audit, while leaving the door open in §8.

## 4. Per-principle audit

Each subsection restates the principle, applies the three v2.4.0 criteria, gives a verdict per criterion, and either proposes a migration target (if the principle fails) or documents the pass-on-review reasoning.

### 4.1 Principle VI — Scripts Over Markdown

**Principle restatement**: Prefer executable scripts, configs, or structured data over freeform markdown when the artifact drives agent or automation behavior. Markdown is appropriate for human orientation (quickstart, README); structured/executable formats are required when downstream automation must parse the artifact to make decisions.

**Criterion 1 — Mechanical verification capability**:
- **Verdict**: FAIL.
- **Reasoning**: The principle's enforcement requires classifying each markdown file as either "drives behavior" or "human orientation." That classification is a judgment call. A CI hook that flags every new `.md` file would be too aggressive (correctly flags the rare violation, also flags every quickstart and README). A CI hook that flags only `.md` files in specific directories (`skills/`, `presets/`) is feasible but only enforces a narrower rule than the principle states — the principle's general "if it drives behavior" framing escapes mechanical capture. The path-to-mechanical-check sketch the v2.4.0 gate requires is not concrete enough; the sketch reduces to "manually classify each file," which is the human judgment the gate is supposed to filter out.

**Criterion 2 — Falsifiable scope**:
- **Verdict**: FAIL.
- **Reasoning**: A reviewer presented with a hypothetical PR adding `docs/orchestration-notes.md` cannot determine, from the principle alone, whether the PR violates it. The reviewer must ask "does this drive behavior?" — exactly the "well, X might be okay if Y" reasoning the v2.4.0 falsifiable-scope criterion rejects.

**Criterion 3 — Distinct from existing principles**:
- **Verdict**: PASS.
- **Reasoning**: Principle XVII (Content Classification) covers "execution logic and contribution guidelines must live in separate formats" — adjacent but distinct. XVII is about *not splitting* a single rule across two surfaces; VI is about *which surface is right* for a given artifact. Composing existing principles does not produce VI's claim.

**Audit verdict**: FAILS the gate (2 of 3 criteria fail). Spec 069 §5's classification holds.

**Proposed migration target**: `CONTRIBUTING.md` (or a new top-level `docs/authoring-conventions.md` if `CONTRIBUTING.md` does not yet have an "authoring conventions" section). The migrated content should be a one-page authoring-conventions note covering: (a) what kinds of repository artifacts are appropriate for prose markdown vs. structured/executable formats, (b) the practical heuristic ("if an agent or pipeline parses it, it should be a script, config, or structured data"), (c) examples drawn from current `skills/`, `presets/`, and `templates/` usage. Tone shifts from "MUST" to "prefer" — operational guidance is the explicit home for preferences and judgment.

### 4.2 Principle X — Zen of Python Output

**Principle restatement**: Output (the artifacts conversus produces — directory trees, summary files, agent reports, error messages) MUST be clean, readable, and unsurprising, in the spirit of the Zen of Python. Predictable output structure, flat over nested, sparse over dense, "if it's hard to explain, it's a bad idea."

**Criterion 1 — Mechanical verification capability**:
- **Verdict**: FAIL.
- **Reasoning**: "Clean," "readable," "unsurprising," "obvious" are aesthetic predicates. A subset of the principle's bullets *is* mechanical (e.g., "agent output is one level deep" — directory-depth lint is feasible; "summary/final.md is always the starting point" — file-existence check is feasible). But the principle's headline claim — that output should match the Zen of Python — has no mechanical analog. The path-to-mechanical-check sketch reduces to "ensure each individual aesthetic bullet has its own check," which is feasible only by replacing the principle with a list of narrower, mechanically-checkable rules. That replacement is exactly what migration to operational guidance accomplishes.

**Criterion 2 — Falsifiable scope**:
- **Verdict**: FAIL.
- **Reasoning**: "If the implementation is hard to explain, it's a bad idea" cannot flag a hypothetical future PR as violating without interpretation. A reviewer evaluating "is this implementation hard to explain?" is performing the judgment the gate is supposed to filter out.

**Criterion 3 — Distinct from existing principles**:
- **Verdict**: PARTIAL PASS.
- **Reasoning**: Principle IV (Documentation Is the Product) and Principle II (Stable Interfaces) both touch on output predictability, but neither covers aesthetics directly. Principle X's distinct contribution is the aesthetic stance. That contribution is real but is exactly what the gate is trying to filter into operational guidance.

**Audit verdict**: FAILS the gate (2 of 3 criteria fail). Spec 069 §5's classification holds.

**Proposed migration target**: a new top-level `docs/output-conventions.md` reference document, or a section in `CONTRIBUTING.md` titled "Output Conventions." The migrated content should: (a) state the aesthetic intent (Zen of Python spirit) in operational-guidance language, (b) extract the mechanically-checkable bullets (directory depth, `summary/final.md` entry point, "errors don't pass silently") into a separate "checkable conventions" subsection that *could* be backed by lints, (c) leave the aesthetic bullets as authoring guidance reviewers cite during PR review. Optionally, the mechanically-checkable subset could become a *new* principle proposal that passes the v2.4.0 gate — but that is a future spec, not part of this migration.

### 4.3 Principle XVI — Mathematical Transparency

**Principle restatement**: When optimization drives decisions in conversus, the user MUST understand what is being optimized. Objective functions are parameterized by user-provided values, not opaque model internals. The 3-stage pipeline (symbolic parsing → LLM gap-filling → deterministic assembly) ensures the math reflects user intent. Plugin recommendations include plain-language explanations alongside numerical outputs. The objective function is the contract between user intent and mathematical optimization.

**Criterion 1 — Mechanical verification capability**:
- **Verdict**: SPLIT.
  - "User understanding" itself is **NOT** mechanically verifiable. A CI check cannot determine that a user actually understood an explanation.
  - The structural sub-claims that *carry* the principle in practice **ARE** mechanically verifiable: (a) parameter pinning (LLM not re-invoked within a run, values persisted to `objective.yml`) — checkable by a CI lint detecting re-entrant `GapFiller.fill()` calls and a contract test reproducing the re-resolution failure; (b) plain-language explanations alongside numerical outputs — checkable by a structural lint on plugin recommendation output schemas; (c) objective-function-shape determinism cross-run — checkable by a parity test. Spec 068 (the determinism-scope clarification) and spec 069 §5's "WOULD FAIL" classification both flag the *headline framing* about "user understanding," not the structural substrate.
- **Reasoning**: This is the most nuanced of the three. The principle's structural enforcement (parameter pinning, plain-language pairing, shape determinism) can be mechanically verified and arguably already is in the v2.3.2 enforcement clauses. What cannot be verified is the wrapping claim that ties those structural rules to "user understanding" as a normative end.

**Criterion 2 — Falsifiable scope**:
- **Verdict**: SPLIT.
  - The structural sub-claims (re-resolution prohibition, plain-language requirement, shape-determinism contract) ARE falsifiable. The v2.3.2 amendment's "Falsification" bullet explicitly names a failing PR pattern: *"A future PR that re-resolves parameters mid-deliberation, or that lets parameter values drift during a single optimization run, violates this principle."*
  - The headline "user MUST understand what is being optimized" framing is NOT falsifiable. A reviewer cannot mechanically classify a hypothetical PR as making the math less understandable to users.

**Criterion 3 — Distinct from existing principles**:
- **Verdict**: PASS.
- **Reasoning**: No other principle covers the user-intent-to-objective-function contract or the parameter-pinning discipline. Principle VII (Reproducibility) is adjacent — XVI explicitly carves an exception to VII for the LLM gap-filling stage — but the carve-out itself proves they are distinct.

**Audit verdict**: SPLIT — fails on the headline framing, passes on the structural substrate. The spec 069 §5 verdict ("WOULD FAIL") is correct about the *wording as written*. But the principle is doing real, mechanically-verifiable work in its structural bullets.

**Proposed migration path** (most nuanced of the three):
- **Option A — Refactor in place** (preferred): Rewrite Principle XVI so its headline claim is the falsifiable structural contract (parameter pinning, shape determinism, plain-language output pairing) and the "user understanding" language is repositioned as design intent in the body. The principle stays in the constitution but with a headline that passes the v2.4.0 gate. This is technically a refinement, which the v2.4.0 gate's criterion 3 says "goes in that principle's body." Refactoring the principle's wording without changing its enforcement is a PATCH-level edit.
- **Option B — Split** (fallback if A is contested): The structural substrate (parameter pinning, shape determinism, plain-language pairing) stays as Principle XVI under a new headline like *"Optimization Determinism and Plain-Language Output Pairing"*; the design-intent framing about user understanding moves to operational guidance in `CONTRIBUTING.md` or a new `docs/optimization-design-intent.md`. Cross-references are added so the design intent is discoverable from the principle body.
- **Recommendation**: pursue Option A in the implementation PR. Option B is the fallback if reviewer consensus rejects A.
- **Migration target for the headline-only content**: `docs/optimization-design-intent.md` (new), or a "Design Intent" subsection in `CONTRIBUTING.md`. Either way, the operational-guidance content explains *why* the structural rules exist (so users can understand and audit the math) without claiming "user understanding" as a falsifiable rule.

## 5. Migration plan

Ordering, risk, and per-principle success criteria for the **implementation PR(s)** that follow this spec. The implementation PRs are out of this spec's scope; this section is the plan they execute.

### 5.1 Ordering — easiest first

1. **Principle VI** (clean migration to `CONTRIBUTING.md`). Lowest contention: aesthetic-adjacent, no enforcement substrate to preserve, no cross-reference web from other principles. Removing it from the constitution and re-housing it as authoring convention has minimal side effects.
2. **Principle X** (migration to `docs/output-conventions.md` or `CONTRIBUTING.md` section). Slightly more nuanced because the mechanically-checkable subset *could* become a new gate-passing principle. The implementation PR should explicitly close that question — either by including the new principle in the same PR (and verifying it through spec 067's protocol) or by deferring it to a follow-up spec.
3. **Principle XVI** (Option A refactor in place; Option B split as fallback). Highest contention: the principle is cross-referenced from VII, has v2.3.2 enforcement clauses, and recently survived spec 068's determinism-scope amendment. Rewriting its headline without breaking enforcement requires careful editing. This goes last so the easier migrations confirm the methodology before applying it to the high-stakes case.

### 5.2 Risk per migration

| Migration | Risk | Mitigation |
|---|---|---|
| VI → CONTRIBUTING.md | Future authors don't consult `CONTRIBUTING.md` and re-introduce prose-when-it-should-be-config patterns. | Add a CI hook (when feasible) that flags new `.md` files in `skills/`, `presets/`, `templates/` directories; cross-reference from `CONSTITUTION.md` Governance to `CONTRIBUTING.md` so the constitution still points at the conventions. |
| X → docs/output-conventions.md | Loss of "Zen of Python" framing as cultural signal. | Preserve the headline phrasing in the operational-guidance doc; cite it in PR review when relevant. Optionally split the mechanically-checkable subset into a new gate-passing principle (deferred to its own spec). |
| XVI Option A (refactor in place) | Reviewer consensus rejects "headline framing change" as a PATCH and demands MINOR. | The implementation PR self-assesses the version bump and surfaces it for review. If MINOR is required, the same PR can carry the bump. |
| XVI Option B (split) | Cross-references from Principle VII break; v2.3.2 enforcement clauses lose their containing principle's headline. | Implementation PR updates VII's reference, preserves the v2.3.2 enforcement clauses verbatim under the new headline, and verifies cross-references via existing structural checks. |

### 5.3 Success criteria per principle migrated

A migration is complete when:

- The migrated content exists in its new home (CONTRIBUTING.md / new doc / refactored principle body).
- `CONSTITUTION.md` no longer carries the failing wording (or, for XVI Option A, the wording is rewritten to pass the gate).
- The implementation PR includes the spec 067 §4 verification artifacts (both self-consistency and blind deliberations) and a passing acceptance bar.
- Cross-references from other principles, specs, and skills point at the new location.
- A `CONSTITUTIONAL_CONVERSATIONS.md` entry records the migration.

## 6. Verification

Per spec 067 §4 (and spec 067 v2's re-verification trigger amendment if landed), the implementation PR(s) that act on this audit cannot merge without **both** self-consistency and blind verification deliberations. This spec itself, as governance-meta with no `CONSTITUTION.md` edit, requires only the verification of its conclusions before its implementation PR can land.

### 6.1 Self-consistency verification

- **Target**: this spec's §4 audit conclusions, with markers visible.
- **Acceptance bar**: 0 ACCEPT-level findings on the per-principle verdicts. Findings on tone, ordering, or scope of the audit are addressable as revisions.
- **Specific check**: do the verdicts in §4 follow consistently from the v2.4.0 gate criteria as written in `CONSTITUTION.md`? §4.3's "split" verdict is the one most likely to be challenged.

### 6.2 Blind verification

- **Target**: the §4 audit with section labels and verdict markers stripped (per spec 067 §4.3.2's stripping recipe), so agents form independent judgments before seeing the spec's conclusion.
- **Agents**: `preset: devils-advocate` for skeptic agents (one of which should specifically argue that one or more of VI/X/XVI passes the gate on closer reading and should NOT be migrated), `preset: balanced-arbiter` for the arbiter.
- **Acceptance bar**: 0 ACCEPT-level findings on the per-principle verdicts. Findings on the methodology of the audit (how the criteria were applied, evidence cited) are addressable as revisions.

### 6.3 Implementation PRs verified separately

The implementation PR(s) that perform actual `CONSTITUTION.md` migration are verified per spec 067 in their own right — this spec's verification covers the audit conclusions, not the resulting amendments. Each migration PR carries its own self-consistency + blind deliberations.

### 6.4 Both deliberations filed in CONSTITUTIONAL_CONVERSATIONS.md

Per spec 067 §4.5.

## 7. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Migration to operational guidance loses the principle's enforcement weight — reviewers stop citing it. | Medium | Cross-reference from `CONSTITUTION.md` Governance to the new home so the constitution still points at the migrated content. Migration PRs add the cross-reference. |
| Future authors don't consult `CONTRIBUTING.md` / `docs/*.md` and re-introduce the migrated patterns. | Medium | Add CI lints for the mechanically-checkable subset of each migrated principle (where one exists). Operational guidance is reinforced by automation, not just by document presence. |
| Fragmentation — operational guidance ends up scattered across many files. | Low | Use `CONTRIBUTING.md` as the default home for migrated content, with `docs/*.md` only when the topic is large enough to warrant a dedicated doc. §4's per-principle proposals follow this convention. |
| The audit's conclusions are wrong — a principle migrated as "failing" actually passes on closer reading. | Medium | Spec 067 §4.2 blind verification with a devils-advocate skeptic explicitly arguing the principle should NOT migrate is the structural mitigation. §6.2 includes this requirement. |
| Migration triggers a cascade — once VI/X/XVI move, reviewers propose migrating other principles too. | Low | §3 explicitly forbids extending this audit to other principles. Cascade migrations require their own specs. |
| Version-bump ambiguity (PATCH vs MINOR vs MAJOR) is unresolved and blocks the implementation PRs. | Medium | §8 Q2 surfaces the question for resolution before the implementation PRs are filed. The spec 069 grandfathering language frames migration as "a separate, intentional act" but does not mandate a specific version-bump category. |

## 8. Open questions

- **Q1**: Are the spec 069 §5 verdicts on VI/X/XVI definitive, or do they need their own deliberation before this audit applies them as the input slate? Spec 069 §5 itself notes the analysis is "non-binding." Recommend: this spec's §4 IS that deliberation — §4 re-derives each verdict from first principles rather than inheriting §5's classification, so the audit stands on its own evidence even if §5's classification turns out to have been informal.
- **Q2**: Does migrating a principle out of `CONSTITUTION.md` require a MAJOR version bump (because principles are being removed from the document) or PATCH/MINOR (because the *content* moves to operational guidance rather than being deleted)? Recommend: MINOR if the migration preserves enforcement substance in operational guidance + adds a constitution → operational-guidance cross-reference; MAJOR only if the principle is deleted outright with no replacement guidance. For VI and X, MINOR is appropriate. For XVI Option A (refactor in place), PATCH is appropriate. For XVI Option B (split), MINOR. The implementation PR must justify its bump category.
- **Q3**: What's the right boundary between "this principle is a constitutional rule" and "this is operational guidance"? The v2.4.0 gate gives the criteria, but the *application* of those criteria to existing principles is judgment-laden. Recommend: the audit in §4 is the case study; methodology surfaced here can guide future migration decisions, but no formal rubric is needed beyond the v2.4.0 gate itself.
- **Q4**: If Principle X's mechanically-checkable subset becomes a new gate-passing principle, when does that proposal land — in the same implementation PR as the X migration, or as a follow-up spec? Recommend: follow-up spec. The migration PR should not be coupled to a new-principle proposal; the spec 067 verification is cleaner when each amendment is independent.
- **Q5**: Should `CONSTITUTIONAL_CONVERSATIONS.md` carry an entry for this audit even if no principle migrates (i.e., if all three pass on review)? Recommend: yes — the audit trail is valuable independent of outcome.

## 9. Acceptance criteria

This spec is "done" when:

1. §4's per-principle audits survive review without substantive rewrite of the verdicts (revisions to reasoning are fine; flipping a verdict triggers re-review).
2. §5's migration plan is accepted as the input plan for the implementation PR(s) — ordering, risks, and success criteria are agreed.
3. Q1-Q5 in §8 are resolved (or explicitly deferred to the implementation PR(s)).
4. Self-consistency verification (per §6.1): 0 ACCEPT-level findings on the per-principle verdicts.
5. Blind verification (per §6.2, using `presets/role/devils-advocate.yml` and `balanced-arbiter.yml`): 0 ACCEPT-level findings on the per-principle verdicts. The blind run MUST include an agent prompt explicitly arguing one or more of VI/X/XVI passes the gate on closer reading and should NOT be migrated.
6. Both verification deliberations filed in `CONSTITUTIONAL_CONVERSATIONS.md`.
7. Implementation PR(s) are filed (one per principle, or a single bundled PR per the §5 ordering) and proceed through their own spec 067 verification independent of this spec.

## 10. References

- `CONSTITUTION.md` — Governance section (defines the v2.4.0 Constitutional Inclusion Criteria gate); Principles VI, X, XVI (the audit targets).
- Spec `069-mechanical-verification-gate` — defines the gate this spec audits against; §4.1 grandfathering provision; §5 worked-examples analysis (the originating slate for this audit).
- Spec `067-verification-methodology` — defines the dual-verification protocol the implementation PR(s) must satisfy.
- Spec `068-principle-xvi-fix` — the v2.3.2 PATCH that scoped Principle XVI's determinism claims; relevant context for §4.3's Option A vs Option B analysis.
- `deliberations/post-v2.4.0-gap-analysis-2026-04-27/` — originating context for this spec; the arbitration recommended a follow-up spec to formally audit grandfathered principles and migrate failures to operational guidance.
- `CONSTITUTIONAL_CONVERSATIONS.md` — running log of constitutional amendments and verifications; will carry an entry for this audit and for each implementation PR.
