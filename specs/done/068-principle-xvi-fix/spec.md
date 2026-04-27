# Feature Specification: Principle XVI Logical Contradiction Fix

**Feature ID**: `068-principle-xvi-fix`
**Created**: 2026-04-26
**Status**: Done — implemented as CONSTITUTION.md v2.3.2 PATCH (PR #29) after both verifications passed (2026-04-26 self-consistency, 2026-04-26 blind). Closed 2026-04-27.
**Depends On**: `CONSTITUTION.md` Principle XVI (target of this fix), `067-verification-methodology` (defines the verification protocol this spec must satisfy)
**Governed by**: `CONSTITUTION.md` Governance section (PATCH for clarifications, MINOR for material expansions)
**Originating context**: 2026-04-25 v2.3.0 blind verification deliberation surfaced a logical contradiction in Principle XVI that **predates v2.3.0** (added with the original game-engine vision in spec 016). The self-consistency verification could not have caught this — the principle was not under amendment review. The blind methodology surfaced it as a "review the whole document" finding. See `CONSTITUTIONAL_CONVERSATIONS.md` 2026-04-25 blind verification entry, finding #2.

> **Scope discipline**: This spec proposes wording to resolve the contradiction in Principle XVI. It does NOT propose new principles. It does NOT broaden XVI's scope. It does NOT touch the optimization architecture itself — the math + plugin layout is correct; the principle wording mis-describes what's deterministic and when.

> **Verification status**: Per spec 067 §4.1, the implementation PR cannot merge without BOTH self-consistency and blind verification deliberations. This spec produces the wording; deliberations come next.

---

## 1. Summary

Principle XVI says:

> "The 3-stage pipeline (symbolic parsing → LLM gap-filling → deterministic assembly) ensures the math reflects user intent. The LLM asks questions; the user's answers become parameters; **the math is pre-defined**."

And separately:

> "Solver choice (nashopt, AMPL, future alternatives) is an implementation detail."

The contradiction the 2026-04-25 blind verification surfaced: **LLM gap-filling is stochastic** (LLM output is not deterministic across calls), but the principle calls the overall pipeline "deterministic assembly" and the math "pre-defined." A reader trying to apply the principle to a future PR cannot tell whether stochastic LLM-derived parameter values violate the principle or fall within its spirit.

The fix is a wording clarification, not an architectural change. The intended invariants are:

1. **The math template is pre-defined** (the objective function shape is fixed at design time).
2. **The parameters that fill the template are user-derived via LLM gap-filling** — stochastic at the LLM step, but cached/pinned once obtained so repeated runs use the same values.
3. **The assembly of (template + parameters) into a final objective function is mechanically deterministic given the parameters**.

The current wording conflates (1)-(3) into a single "deterministic" claim. The fix names each stage explicitly.

## 2. Goals

1. Resolve the logical contradiction between "LLM gap-filling" (stochastic) and "deterministic assembly" / "pre-defined math" (deterministic) in Principle XVI's wording.
2. Preserve every architectural intent the original principle expressed — this is a wording fix, not a behavior change.
3. Make the principle operationally checkable: a future PR claiming to violate XVI should be auditable against the wording.
4. Avoid expanding XVI's scope — the principle remains about *what gets optimized* and *user understanding of it*, not about *general determinism*.

## 3. Non-goals

- **Changing the 3-stage pipeline.** Symbolic parsing → LLM gap-filling → deterministic assembly is the actual implementation; the principle should describe it correctly, not redesign it.
- **Removing or merging Principle XVI.** It earns its keep; only its wording is wrong.
- **Adding a new "determinism" principle.** Principle VII (Reproducibility Over Inconsistency) already covers reproducibility broadly. XVI is the optimization-specific specialization.
- **Resolving the broader determinism-vs-LLM tension across the constitution.** That's a separate concern.

## 4. Proposed amendment

PATCH-level clarification (governance section: "PATCH for clarifications"). Version bump: 2.3.1 → 2.3.2.

### 4.1 Replace the first bullet of XVI

**Current text** (lines 455-460 of `CONSTITUTION.md`):

```
- The 3-stage pipeline (symbolic parsing → LLM gap-filling →
  deterministic assembly) ensures the math reflects user intent.
  The LLM asks questions; the user's answers become parameters;
  the math is pre-defined. The LLM does not generate the objective
  function — it translates gap identifiers into natural-language
  questions and answers into parameter values.
```

**Proposed text**:

```
- The 3-stage pipeline (symbolic parsing → LLM gap-filling →
  mechanical assembly) ensures the math reflects user intent. The
  three stages have different determinism properties, and conflating
  them is the source of past wording confusion:

    1. **Symbolic parsing**: deterministic — given a template ID,
       the parser yields the same gap identifiers every time.
    2. **LLM gap-filling**: stochastic at the LLM call, but the
       resulting parameter values are **pinned per deliberation
       run**. Repeating a deliberation with the same input does NOT
       re-call the LLM for parameters; cached values from the first
       resolution are reused. Cross-run variance is acceptable;
       within-run variance is prohibited.
    3. **Mechanical assembly**: deterministic — given a template
       and a fully-pinned parameter set, the resulting objective
       function is identical bit-for-bit on every assembly.

  The math template is pre-defined at design time (spec 013). The
  LLM does not generate the objective function — it translates gap
  identifiers into natural-language questions and the user's
  answers into parameter values. Once parameters are pinned, the
  optimization is reproducible (Principle VII applies).
```

### 4.2 Add a clarifying paragraph at the end of XVI

**New paragraph** (appended after the existing "Solver choice…" bullet):

```
**Clarification (v2.3.2): determinism scope.** Principle XVI claims
**within-run** determinism for the assembled objective function and
**cross-run** reproducibility once parameters are pinned. It does
NOT claim the LLM gap-filling step itself is deterministic; that
step is allowed to be stochastic, and the discipline is in pinning
its output rather than re-running it. A future PR that re-resolves
parameters mid-deliberation, or that lets parameter values drift
during a single optimization run, violates this principle.
```

### 4.3 Sync Impact Report (PATCH)

To replace the v2.3.1 SIR header (or append as a new historical SIR if §4.5 of v2.3.1's report is preserved):

```markdown
<!--
Sync Impact Report
Version change: 2.3.1 → 2.3.2 (PATCH — Principle XVI determinism-scope
clarification, resolves logical contradiction surfaced by 2026-04-25
blind verification, finding #2)
Added principles: none
Modified principles:
  - XVI. Mathematical Transparency — replaced first bullet to name the
    three stages' distinct determinism properties; added a "determinism
    scope" clarification paragraph
Removed sections: none
Templates requiring updates: none
Rationale: 2026-04-25 blind verification (deliberations/v2.3.0-blind-
verification-2026-04-25/) flagged a logical contradiction between
"LLM gap-filling" (stochastic) and "deterministic assembly" / "pre-
defined math" (deterministic) in XVI's wording. The fix clarifies
which stage is deterministic and what within-run vs cross-run
reproducibility means. No architectural change.
Governance log entry: 2026-04-26 in CONSTITUTIONAL_CONVERSATIONS.md.
-->
```

## 5. Verification (per spec 067 §4.1)

The implementation PR (the actual `CONSTITUTION.md` edit) cannot merge without BOTH:

### 5.1 Self-consistency verification

**Target**: amended `CONSTITUTION.md` v2.3.2 with v2.3.2 markers visible.
**Acceptance bar**: 0 ACCEPT-level findings on the XVI changes specifically.
**Agents**: at minimum a wording-precision agent. Reuse the 2026-04-25 self-consistency config as a template (`deliberations/v2.3.0-verification-2026-04-25/conversus.yml`).

### 5.2 Blind verification

**Target**: stripped v2.3.2 produced by `scripts/strip-constitution-for-blind.py --version v2.3.2`.
**Agents**: per spec 067 §4.3.1, use `preset: devils-advocate` for skeptic agents and `preset: balanced-arbiter` for the arbiter. Do NOT hand-roll.
**Acceptance bar**: 0 ACCEPT-level findings on the XVI revisions specifically. New pre-existing flaws surfaced are deferred to their own follow-up specs.

### 5.3 Both deliberations filed in `CONSTITUTIONAL_CONVERSATIONS.md`

Per spec 067 §4.5. Format follows the 2026-04-25 entries.

## 6. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| The proposed wording introduces a new contradiction (e.g., the "pinned per deliberation run" claim conflicts with how parameters actually flow) | Medium | Verification deliberations §5 catch this — arbiter rules ACCEPT and the implementation gets revised. |
| The amendment scope creeps from "wording fix" to "redesign optimization architecture" | High | §3 explicitly forbids architectural changes. Reviewers reject any code change in the implementation PR — only `CONSTITUTION.md` text moves. |
| The 3-stage pipeline names ("symbolic parsing", "LLM gap-filling", "mechanical assembly") don't match what the actual implementation calls them | Medium | Verify against `conversus/optimizer/`, `conversus/plugins/nashopt/` (or wherever the optimization layer lives) before merging. If names differ, update the spec to match the code, not vice versa. |
| Renaming "deterministic assembly" to "mechanical assembly" creates confusion with the original game-engine docs | Low | Keep "deterministic" in §4.1's stage 3 description; only the umbrella term shifts. |

## 7. Open questions

- **Q1**: Does the actual codebase pin parameter values per deliberation run, or is the pinning aspirational? The amendment claims pinning is the discipline. If the code re-resolves parameters mid-run, the spec is inaccurate. **Required check** before deliberations: grep `conversus/` for parameter-resolution call sites.
- **Q2**: Is "v2.3.2" the right version, or should this go in a v2.4.0 alongside other deferred fixes? Recommend: ship as 2.3.2 standalone unless other deferred fixes are queued at the same time.
- **Q3**: Should the Sync Impact Report list v2.3.1 in the version-change line or v2.3.0 (since v2.3.1 was a clarification)? Recommend: 2.3.1 → 2.3.2 (every PATCH increments).

## 8. Acceptance criteria for this spec

This spec is "done" when:

1. The proposed wording survives review without substantive rewrite.
2. Q1 is answered (parameter-pinning is verified in code or the wording is amended to match reality).
3. Q2 and Q3 are resolved.
4. Self-consistency verification deliberation produces 0 ACCEPT-level findings.
5. Blind verification deliberation (using `presets/role/devils-advocate.yml` and `balanced-arbiter.yml`, no hand-rolling) produces 0 ACCEPT-level findings on the XVI revisions specifically.
6. Both verification deliberations filed as entries in `CONSTITUTIONAL_CONVERSATIONS.md`.
7. Implementation PR (the actual `CONSTITUTION.md` edit) is filed and merged.

## 9. References

- `CONSTITUTION.md` Principle XVI (current target text)
- `CONSTITUTIONAL_CONVERSATIONS.md` — 2026-04-25 blind verification entry, finding #2
- `deliberations/v2.3.0-blind-verification-2026-04-25/round-2/arbiter/resolution.md` (the blind arbiter's specific suggested fix wording)
- Spec 067 — Verification methodology (the protocol this spec follows)
- Spec 016 — game-engine vision (origin of Principle XVI)
- Spec 013 — objective function templates (referenced in XVI)

## Closure note (2026-04-27)

**Implementation**: PR #29 — `feat(constitution): v2.3.1 → v2.3.2 — Principle XVI determinism-scope clarification`

**Verification**:
- Self-consistency: `deliberations/068-self-consistency-2026-04-26/` (PASS WITH FIXES, 3 ACCEPT)
- Blind: `deliberations/068-blind-2026-04-26/` (PASS WITH FIXES, 4 ACCEPT)

**Fixes folded in**: 7 ACCEPT findings (3 from self-consistency + 4 from blind)

**Governance log**: 2026-04-26 self-consistency entry + 2026-04-26 blind entry in `CONSTITUTIONAL_CONVERSATIONS.md`

Re-verification was NOT run after fixes were folded in — flagged retroactively as a methodology gap by the 2026-04-27 post-v2.4.0 gap analysis. Spec 067 v2 amendment (PR #35) addresses this for future amendments. This implementation is grandfathered.

