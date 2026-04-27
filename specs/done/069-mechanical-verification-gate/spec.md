# Feature Specification: Mechanical Verification Capability — Governance Gate for Constitutional Inclusion

**Feature ID**: `069-mechanical-verification-gate`
**Created**: 2026-04-26
**Status**: Done — implemented as CONSTITUTION.md v2.4.0 MINOR (PR #32) after both verifications passed (2026-04-26 self-consistency, 2026-04-26 blind). Closed 2026-04-27.
**Depends On**: `CONSTITUTION.md` Governance section (target of this amendment), `067-verification-methodology` (defines the verification protocol this spec must satisfy)
**Governed by**: `CONSTITUTION.md` Governance section ("MINOR for new principles or material expansions") — this spec proposes a material expansion of the amendment criteria themselves
**Originating context**: 2026-04-25 v2.3.0 blind verification deliberation, finding #3. The arbiter ruled: *"establish in the governance section that 'mechanical verification capability is required for constitutional inclusion — principles that cannot be automatically verified belong in operational guidance where human judgment is appropriate.'"* This spec proposes the wording that operationalizes that ruling.

> **Scope discipline**: This spec amends the **amendment criteria**. It does NOT add or modify any operational principle. It changes what future principles MUST satisfy to enter the constitution at all.

> **Recursive concern**: this spec proposes a gate. The gate's first test is itself — does the proposed wording for "mechanical verification capability is required" pass its own bar? §6 addresses this.

---

## 1. Summary

The blind verification deliberation that surfaced spec 068 also surfaced a structural critique: **the constitution accumulates principles whose compliance cannot be mechanically verified**. The current 27 principles include some whose enforcement requires "reviewer judgment" — at PR-review time, at deliberation time, or never. Principles that cannot be checked by a CI hook, a parity test, or a structural lint accumulate as ceremonial language: present in the document, ignored in practice.

The arbiter's specific recommendation: add a **governance-level gate** stating that constitutional inclusion requires mechanical verification capability. Principles that resist mechanical verification belong in operational guidance (CONTRIBUTING.md, SKILL.md, spec-specific notes) where human judgment is the explicit interpretive frame.

This spec proposes the wording for that gate.

## 2. Goals

1. Add a governance-level requirement that constitutional inclusion is gated on mechanical verifiability.
2. Define "mechanical verification capability" specifically enough that a future amendment author can self-assess whether their principle qualifies.
3. Provide a fallback path (operational guidance) for principles that fail the gate, so the gate is not a "no, we cannot codify this concern" rejection.
4. Preserve existing principles. The gate is **prospective** — applies to amendments after this spec lands, not retroactively to v2.3.x principles.
5. Avoid making the gate so strict it blocks principles that catch real bugs but require subtle automation.

## 3. Non-goals

- **Retroactive removal of existing principles**. This spec does not propose dropping XVI (which the gate might fail), nor any other current principle. Migration is a separate, future, intentional act.
- **Defining the verification automation**. The gate requires that automation is *possible*; it does not require it to *exist* at amendment time. Implementation can follow the spec.
- **Replacing human review**. Mechanical verification supplements, not replaces, code review. A principle that catches some bugs by lint and others by reviewer judgment is fine — at least one mechanical check must exist.
- **Reopening the existing constitution wholesale**. The gate is a forward filter, not a backward audit.

## 4. Proposed amendment

MINOR-level — this is a material expansion of the governance criteria. Version bump: 2.3.x → 2.4.0.

### 4.1 Add a "Constitutional Inclusion Criteria" subsection to Governance

**Location**: insert immediately after the existing `**Versioning**:` bullet in the Governance section, before the `**Compliance**:` bullet.

**Proposed text**:

```markdown
- **Constitutional Inclusion Criteria** (added v2.4.0): a principle qualifies for
  constitutional inclusion only if it satisfies all three:

  1. **Mechanical verification capability**: at least one form of
     automated check (CI lint, parity test, structural assertion,
     schema validation, or equivalent) MUST be feasible such that a
     future PR violating the principle would fail the check. The
     check does NOT have to exist at amendment time, but the path
     to building it MUST be concrete enough that an engineer reading
     the principle can sketch the check in one paragraph.

  2. **Falsifiable scope**: the principle's wording MUST be specific
     enough to flag a hypothetical future PR as violating, without
     requiring "interpretation." If a reviewer must reason "well, X
     might be okay if Y," the principle is too vague for the
     constitution and belongs in operational guidance.

  3. **Distinct from existing principles**: the principle MUST cover
     concerns not already addressable by composing existing principles.
     Restating an existing principle in different words is rejected
     by this gate. Refining or extending an existing principle goes
     in that principle's body, not as a new principle.

  Principles that fail any criterion belong in **operational guidance**:
  `CONTRIBUTING.md`, the relevant spec, `SKILL.md` instructions, or
  domain-specific reference documents. Operational guidance is the
  explicit home for "judgment calls" and "rules of thumb"; the
  constitution is the home for invariants.

  This gate applies **prospectively** — to amendments landing after
  v2.4.0. Existing principles I-XXVII are grandfathered. Migrating
  any of them to operational guidance is a separate, intentional act
  governed by the same amendment process (with the receiving document
  identified explicitly in the migration spec).
```

### 4.2 Sync Impact Report (MINOR)

```markdown
<!--
Sync Impact Report
Version change: 2.3.x → 2.4.0 (MINOR — Governance section expanded with
Constitutional Inclusion Criteria gate)
Added principles: none
Modified sections:
  - Governance — added "Constitutional Inclusion Criteria" subsection
    requiring mechanical verification capability, falsifiable scope, and
    distinctness from existing principles for new amendments
Removed sections: none
Templates requiring updates: none in this repo
Rationale: 2026-04-25 blind verification (deliberations/v2.3.0-blind-
verification-2026-04-25/) finding #3 ruled that "mechanical verification
capability is required for constitutional inclusion." This amendment
operationalizes that ruling as a forward gate on constitutional
amendments. Existing principles are grandfathered; migration of
sub-mechanical principles to operational guidance is a separate
intentional act.
Governance log entry: 2026-04-26 in CONSTITUTIONAL_CONVERSATIONS.md.
-->
```

## 5. Worked examples — does each existing principle pass the gate?

This is **non-binding analysis** (existing principles are grandfathered) but informs whether the gate is appropriately scoped. If most existing principles fail, the gate is too strict; if all pass, it's too lax to do useful work.

| # | Principle | Mechanical check feasible? | Notes |
|---|---|---|---|
| I | Spec-Driven Development | Yes — CI hook checks PRs touching SKILL.md require a `specs/{NNN}-{name}/` reference | |
| II | Stable Interfaces | Yes — variable schema parity test, dispatch table snapshot test | |
| III | Backward-Compatible Extension | Yes — existing-config-roundtrip test ensures omitting new fields preserves output | |
| IV | Documentation Is the Product | Partial — STATUS.md update can be checked; "SKILL.md is single source of truth" cannot | Borderline; passes by virtue of the STATUS.md half |
| V | Observable Deliberation | Yes — phase progress emission can be asserted in pipeline tests | |
| VI | Scripts Over Markdown | No — judgment call about "drives behavior" vs "human orientation" | **WOULD FAIL** the gate today; grandfathered |
| VII | Reproducibility Over Inconsistency | Yes — same-config-twice byte-equality test | |
| VIII | Templating Engines Over Inference | Yes — template variable substitution test | |
| IX | Functional Programming and Clean Code (+ behavior-over-shape extension) | Partial — type checks pass; "pure functions" needs review judgment | Borderline; the operational test in the v2.3.0 extension helps |
| X | Zen of Python Output | No — aesthetic judgment | **WOULD FAIL** the gate today; grandfathered |
| XI | Single Source of Truth (+ Registry-First) | Yes — parity tests (PR #18, #22 are examples) | |
| XII | No Dead Infrastructure | Yes — used-variable lint, dead-code check | |
| XIII | Enum Completeness | Yes — pattern-match exhaustiveness check | |
| XIV | Spec-Implementation Parity | Partial — file-existence checks pass; "implementation matches intent" needs review | |
| XV | Plugin Isolation (+ registry-as-extension-interface) | Yes — plugin namespace assertions, identical-output-with/without-plugin test | |
| XVI | Mathematical Transparency | **NO** — "user understanding" cannot be mechanically verified | **WOULD FAIL** the gate today; grandfathered. (See spec 068 for an unrelated correctness fix.) |
| XVII-XXI | Decomposition principles | Yes — load-trigger lint, file-existence, content-classification checks | |
| XXII | Distribution Surface Integrity | Yes — version-source parity test, force-include manifest lint, install-test in CI | |
| XXIII | Provider Robustness Contract | Yes — token-reporting assertion per provider, retry-jitter test, format-tolerance fixtures | |
| XXIV | Safety-Critical Defense-in-Depth | Yes — schema-required-field check, parser-validation test, contract-test-presence lint | |
| XXV | Live Test Cost Discipline | Yes — `@pytest.mark.live` lint, marker-taxonomy check | |
| XXVI | Meta-Testing for Parametrized Capabilities | Yes — meta-test pattern itself is a mechanical check | |
| XXVII | Operator-Configurable Tool Surface | Yes — env var → tool list assertion (similar to PR #14's tests) | |

**Summary**: 3 existing principles (VI, X, XVI) would fail the gate today. The gate is **calibrated correctly** — strict enough to filter out aesthetic / judgment-call additions, but most evidence-grounded principles pass. The grandfathering provision protects the existing 3, and migrating them is explicitly out of scope for this spec.

## 6. The recursive test — does this spec pass its own gate?

The proposed governance amendment must satisfy its own three criteria:

### 6.1 Mechanical verification capability

The gate ITSELF can be checked mechanically: a CI hook walks every spec proposing a constitutional amendment, parses its §4.1 (or equivalent) for self-assessment against the three criteria, and fails the PR if the self-assessment is missing or any criterion is marked "no." This is the same kind of structural check Phase 1 / Phase 2 drift guards use.

The check is feasible. Whether it gets built is a separate engineering decision.

### 6.2 Falsifiable scope

A future amendment spec that proposes a vague principle (e.g., "code should be elegant") would fail criterion 2 (falsifiable scope) without interpretation: there is no mechanical way to flag inelegant code. The gate's wording is concrete enough to apply.

### 6.3 Distinct from existing principles

Principle XI (Single Source of Truth) and Principle XII (No Dead Infrastructure) are adjacent but neither speaks to **inclusion criteria for new amendments**. Both speak to existing artifacts. The gate is governance-level, addressing the meta-process. Distinctness holds.

### 6.4 Verdict

This spec passes its own gate. ✅

(Recursive bootstrap is intentional. The gate must apply to itself or it is not a gate.)

## 7. Verification (per spec 067 §4.1)

The implementation PR cannot merge without BOTH self-consistency and blind verification deliberations.

### 7.1 Self-consistency verification

**Target**: amended `CONSTITUTION.md` v2.4.0 with v2.4.0 markers visible.
**Acceptance bar**: 0 ACCEPT-level findings on the new Governance subsection specifically.
**Specific check**: does the new subsection introduce its own contradictions or wording ambiguities? §6 above is the spec's pre-emptive answer; the deliberation should test it.

### 7.2 Blind verification

**Target**: stripped v2.4.0 produced by `scripts/strip-constitution-for-blind.py --version v2.4.0`.
**Agents**: per spec 067 §4.3.1 — `preset: devils-advocate` for skeptic agents (one of which should specifically argue that the gate is too strict and rejects useful principles), `preset: balanced-arbiter` for the arbiter.
**Acceptance bar**: 0 ACCEPT-level findings on the gate's wording. Findings on existing principles surfaced incidentally are deferred (consistent with how spec 068 was surfaced and handled).

### 7.3 Both deliberations filed in `CONSTITUTIONAL_CONVERSATIONS.md`

Per spec 067 §4.5.

## 8. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| The gate is too strict and rejects useful principles | High | §5's worked-examples analysis shows most evidence-grounded principles pass. The blind verification §7.2 explicitly asks an agent to argue the gate is too strict. |
| The gate becomes a rubber stamp because self-assessment is the loophole | Medium | Reviewer can challenge a self-assessment. Future tooling could add a CI hook (§6.1) that requires the self-assessment block to be present, structured, and non-empty. |
| Grandfathered principles (VI, X, XVI) become "second class" | Low | Grandfathering is permanent. Migration to operational guidance is its own amendment process. The gate doesn't degrade existing principles. |
| The gate triggers a wave of "let's migrate everything to operational guidance" PRs | Medium | §3 explicitly forbids retroactive migration. Each migration requires its own intentional spec. |

## 9. Open questions

- **Q1**: Should the self-assessment block be a STRUCTURED form (YAML with `mechanical_check_sketch:` etc) or freeform prose? Recommend: freeform prose for now; future work can add structure if compliance is uneven.
- **Q2**: Where does the self-assessment block live in amendment specs — top, in §1 Summary, or its own section? Recommend: own section ("Constitutional Inclusion Self-Assessment") at the end of §4 (proposed amendment) so reviewers see it adjacent to the wording.
- **Q3**: Should existing principles be re-audited against the gate as a **non-binding** exercise? Recommend: yes, as a future task (own spec). The §5 table here is informal; a formal audit could surface migration candidates.
- **Q4**: Does this require a MINOR (2.4.0) bump or could it be PATCH (2.3.2)? The amendment changes inclusion *criteria* — that's a material expansion of how amendments work, which feels MINOR. Recommend: 2.4.0.

## 10. Acceptance criteria for this spec

This spec is "done" when:

1. The proposed gate wording survives review without substantive rewrite.
2. The §5 worked-examples analysis is reviewed; if more than 5 existing principles fail the gate, the gate is too strict and the spec is revised.
3. Q1-Q4 in §9 are resolved.
4. Self-consistency verification: 0 ACCEPT-level findings on the new Governance subsection.
5. Blind verification (using `presets/role/devils-advocate.yml` and `balanced-arbiter.yml`): 0 ACCEPT-level findings on the gate's wording. The blind run MUST include an agent prompt explicitly arguing the gate is too strict.
6. Both verification deliberations filed in `CONSTITUTIONAL_CONVERSATIONS.md`.
7. Implementation PR (the actual `CONSTITUTION.md` edit) is filed and merged.

## 11. References

- `CONSTITUTION.md` Governance section (target of amendment)
- `CONSTITUTIONAL_CONVERSATIONS.md` — 2026-04-25 blind verification entry, finding #3
- `deliberations/v2.3.0-blind-verification-2026-04-25/round-2/arbiter/resolution.md` (the originating arbiter ruling)
- Spec 067 — Verification methodology
- Spec 068 — Principle XVI fix (sibling spec from the same blind verification)

## Closure note (2026-04-27)

**Implementation**: PR #32 — `feat(constitution): v2.3.2 → v2.4.0 — mechanical verification capability gate`

**Verification**:
- Self-consistency: `deliberations/069-self-consistency-2026-04-26/` (PASS WITH FIXES)
- Blind: `deliberations/069-blind-2026-04-26/` (PASS WITH FIXES)

**Governance log**: 2026-04-26 self-consistency entry + 2026-04-26 blind entry in `CONSTITUTIONAL_CONVERSATIONS.md`

Re-verification was NOT run after fixes were folded in — flagged retroactively as a methodology gap by the 2026-04-27 post-v2.4.0 gap analysis. Spec 067 v2 amendment (PR #35) addresses this for future amendments. This implementation is grandfathered.

