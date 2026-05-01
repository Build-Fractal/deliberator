# Feature Specification: Test-Fix Boundary Preservation (Proposed Principle XXVIII)

**Feature ID**: `071-test-fix-boundary-preservation`
**Created**: 2026-04-28
**Status**: Implemented 2026-04-30 — `CONSTITUTION.md` v2.5.0 added Principle XXVIII (v2 wording, ratified-with-override). All three follow-on PRs merged: PR #47 (spec 067 §4.6 amendment), PR #48 (PR template), PR #49 (`scripts/lint-test-fixes.py` + advisory CI workflow). Verification trail: `deliberations/071-self-consistency-2026-04-28/`, `deliberations/071-blind-2026-04-28/` (v1), `deliberations/071-blind-v2-2026-04-29/` (v2). Override rationale logged in `CONSTITUTIONAL_CONVERSATIONS.md` 2026-04-29 entry. Moved to `specs/done/`.
**Depends On**: `067-verification-methodology` (defines the verification protocol the implementation PR must satisfy and the §4.6 amendment this spec proposes), `069-mechanical-verification-gate` (defines the v2.4.0 Constitutional Inclusion Criteria gate this principle must pass)
**Governed by**: `CONSTITUTION.md` Governance section, especially the v2.4.0 Constitutional Inclusion Criteria gate. As a proposed new principle (post-v2.4.0), this spec is bound by the prospective inclusion gate; it must self-assess against the gate criteria before it can be ratified.
**Originating context**: 2026-04-28 spec-045 coverage verification surfaced 95 failing tests in `conversus-oss`. A 4-subagent investigation (Categories A/B/C/D) found 1 production bug (engine/handlers.py import shadowing — landed in PR #42), 1 production bug candidate (engine/_root.find_project_root resolution fragility — Cat D), ~70 mechanical fixture-path drifts (Cat A), and 3 remaining failures the bug-fix subagent refused to "fix" because doing so would have weakened assertions. A naive "make tests pass" sweep would have buried the production bugs and the 3 genuine gaps behind the noise. The framework that prevented this was the user's binding instruction: "if a test passes after fix, it must have real boundaries." This spec proposes codifying that instruction as Principle XXVIII and operationalizing it via four enforcement layers.

> **Scope discipline**: This spec **proposes** Principle XXVIII and the layered enforcement model. It does NOT edit `CONSTITUTION.md`, does NOT create `scripts/lint-test-fixes.py`, does NOT modify `.github/pull_request_template.md`, and does NOT amend `specs/067-verification-methodology/spec.md`. Each of those is a follow-up implementation PR authorized by this spec's acceptance criteria, not performed within it.

> **Inclusion-gate self-assessment is required**: per spec 069, every new principle proposed after v2.4.0 must self-assess against the three Constitutional Inclusion Criteria. §5 of this spec performs that self-assessment. If the assessment fails, this spec must be reframed as operational guidance instead of a constitutional principle.

---

## 1. Summary

This spec proposes adding **Principle XXVIII — Test-Fix Boundary Preservation** to `CONSTITUTION.md`. The principle codifies the discipline that when fixing a failing test, the fix MUST preserve or strengthen the test's verification of real behavior — never weaken it. Every test fix MUST be classified as exactly one of four categories (fixture/path drift, production bug, legitimate test bug, defunct test), and the classification MUST be verifiable against the diff. The principle is layered with three operational enforcement mechanisms: (1) an addition to the PR template requiring authors to declare the categorization and assertion-fidelity status; (2) an advisory CI lint script (`scripts/lint-test-fixes.py`, filed as a follow-up PR) that uses AST-diff heuristics to flag suspicious assertion changes; and (3) an amendment to spec 067 §4.6 requiring the 4-subagent investigation pattern when verification deliberations surface failing tests.

The "why" is anchored in the 2026-04-28 PR #42 case study. Without the user's binding principle in the prompt, two production bugs (engine/handlers.py shadowing; engine/_root path resolution fragility) would have shipped silently behind 95 "failing tests" that a naive sweep would have made green. The principle is the codification of that prompt-time discipline, transferring the load-bearing instruction from prompt-by-prompt repetition to a constitutional invariant that survives across sessions, agents, and future contributors. Three layers (principle + PR template + CI lint + spec 067 §4.6) all have to fail simultaneously for this class of regression to ship — that is the residual-risk floor this spec accepts.

## 2. Goals

1. **Codify the discipline** as Principle XXVIII so the binding instruction lives in the constitution rather than in any single prompt or session.
2. **Operationalize via PR template** so authors are forced to declare the categorization at PR-open time, making "I just made it pass" structurally visible to reviewers.
3. **Mechanically enforce via CI lint** so the most common loosening patterns (`==` → `in`, exact-value → type-check, dropped assertions, uncited skips) are flagged automatically, with line numbers, on every PR that touches a test file.
4. **Update spec 067** to require the 4-subagent investigation pattern when a verification deliberation surfaces failing tests — the pattern PR #42 exercised becomes the canonical first response.
5. **Make "test fix" a recognized PR class** with explicit discipline, distinct from "feature" or "refactor" PRs, so reviewers know which checklist to apply.

## 3. Non-goals

- **Not eliminating the human judgment moment.** Categorization itself is irreducibly a judgment call; the layered enforcement only forces that judgment to be made explicitly and visibly, not to be made by a tool.
- **Not auto-fixing weakened assertions.** The lint flags suspicious patterns; it does not rewrite them. Auto-rewrites would mask intent and create a new bypass surface.
- **Not blocking all skip directives.** `pytest.skip()` and `@pytest.mark.skip` remain legitimate when they cite a bug ID and a remediation timeline. The principle disciplines uncited skips, not skips themselves.
- **Not retroactive enforcement.** This principle applies prospectively, to PRs filed after it lands. Existing tests with vague skip markers or loose assertions are not in scope; an audit of existing test discipline is a separate spec if needed.
- **Not a replacement for behavior-over-shape (Principle IX) or meta-testing (Principle XXVI).** Those principles govern *test authoring* and *coverage drift*; this principle governs *test-fix discipline* — the moment when a failing test is being made green. §5.3 substantiates the distinctness claim.

## 4. Proposed Principle XXVIII (v2 — revised after blind verification 2026-04-28)

> **Revision context**: v1 (with three clauses including "assertion fidelity") failed blind verification on three counts: (a) assertion fidelity duplicated Principle IX's behavior-over-shape extension; (b) format-checking the category label was theater rather than substantive verification of categorization correctness; (c) RFC 2119 "MAY NOT" was non-conformant. v2 drops clause 1 (deferred to IX), strengthens clause 3 with a diff-shape consistency check (mechanically substantive), and acknowledges the residual non-mechanical limit explicitly. See `deliberations/071-blind-2026-04-28/arbiter/resolution.md` for the v1 verdict.

The proposed wording, to be inserted into `CONSTITUTION.md` after Principle XXVII (Operator-Configurable Tool Surface):

```markdown
### XXVIII. Test-Fix Boundary Preservation

When fixing a failing test, the fix MUST preserve the test's
verification of real behavior. Assertion-fidelity discipline is
governed by Principle IX (behavior-over-shape extension); this
principle adds two mechanically verifiable disciplines that
operate at fix-time.

1. **Skip discipline**: any `pytest.skip()`, `@pytest.skip`, or
   `@pytest.mark.skip` newly introduced in a PR MUST cite the bug
   being skipped (issue or PR number) and a remediation timeline.
   "Flaky", "slow", "broken", or similar without a citation is
   prohibited.
   *Mechanical check*: any newly added skip directive whose
   adjacent comment or docstring does not match
   `(issue|PR|#\d+|TODO\(.+\))` plus a timeline cue is a violation.

2. **Test-or-bug categorization with diff-shape consistency**:
   every PR that modifies a test file in a fix-time context MUST
   declare each fix as exactly one of four categories, and the
   PR's diff shape MUST match the declared category:

   | Category | Required diff signature |
   |---|---|
   | fixture/path drift | only test files modified |
   | production bug | ≥1 production-source file modified |
   | legitimate test bug | only test files modified; PR body cites the test-side bug |
   | defunct test | test deletion (not modification); PR body cites why the behavior is no longer relevant |

   *Mechanical check*: the lint reads the declared category from
   a structured PR-template field, computes the actual diff
   shape, and flags any mismatch. A mismatch is the violation,
   not the misjudgment that produced it — mismatch is
   structurally detectable; misjudgment is not, and that limit
   is acknowledged rather than papered over.

*Origin*: 2026-04-28 spec-045 verification surfaced 95 failing
tests; the 4-subagent investigation found 1 production bug
(engine/handlers.py import shadowing — PR #42) hiding behind
~70 mechanical failures. A naive sweep would have labeled the
shadowing fix as "fixture drift" and shipped it; the diff-shape
check (production-source edit incompatible with that label) is
the discipline that catches that exact failure mode.
```

The wording is deliberately compact. The two-clause structure mirrors the format of recent principles (XXIV, XXVI, XXVII): a one-sentence rule with explicit cross-reference to IX, a numbered enumeration of the two mechanically verifiable disciplines, and an *Origin* note that anchors the principle in a concrete case study.

## 5. Constitutional inclusion gate self-assessment

Per spec 069's Constitutional Inclusion Criteria, every new principle proposed after v2.4.0 must self-assess against three criteria before it can be ratified. This section performs that assessment.

### 5.1 Criterion 1 — Mechanical verification capability

**Verdict**: PASS.

**Reasoning**: The principle's two clauses are mechanically checkable via the lint script described in §6 (`scripts/lint-test-fixes.py`). For clause 1 (skip discipline), the script walks the PR diff for files matching `**/test_*.py` or `**/*_test.py`, identifies newly added `pytest.skip(...)`, `@pytest.skip`, or `@pytest.mark.skip` directives, and flags any whose adjacent comment or docstring does not match `(issue|PR|#\d+|TODO\(.+\))` plus a remediation timeline cue. For clause 2 (categorization with diff-shape consistency), the script reads the structured category field from the PR body (per §7's template), computes the actual diff shape (which paths under `**/test_*.py|**/*_test.py` were modified vs which production-source paths were touched), and flags any mismatch — for example, a "fixture drift" claim accompanied by production-source edits, or a "defunct test" claim with no test deletions. The diff-shape check is substantively verifying, not format-checking: a PR mislabeling a production bug as fixture drift produces a structurally detectable mismatch (production source touched + "fixture drift" label), which the lint surfaces. What the lint cannot verify is *categorization correctness within the test-only quadrant* — i.e., whether a "fixture drift" claim with only test-file edits is in fact a "legitimate test bug" miscategorized. That residual is acknowledged in clause 2's text and Q1 in §11. The capability that exists (skip-citation enforcement + diff-shape consistency) satisfies the v2.4.0 gate's "future PR violating the principle would fail the check" standard for the dominant failure mode the principle was designed to catch (the PR #42 case study, where a naive sweep would have labeled a production bug as fixture drift).

### 5.2 Criterion 2 — Falsifiable scope

**Verdict**: PASS.

**Reasoning**: For any test-file diff, a reviewer can ask the author "which of the four categories does this fix belong to?" If the answer is "I weakened the assertion to make the test pass," the PR violates Principle XXVIII. If the answer fits none of the four categories cleanly — for example "I rewrote the test to assert something looser because the original assertion was too strict" — that admission is itself the violation, because the four categories are exhaustive over the legitimate fix-time decisions: either the test's intent is preserved (fixture drift), the code is wrong (production bug), the test is wrong but documented (legitimate test bug), or the behavior under test no longer exists (defunct test). A loosened assertion in service of "make it pass" maps to none of these. The reviewer-and-author conversation is the falsifiability test, and it terminates in a PR-level pass/fail. There is no "well, X might be okay if Y" residue — the categories are a partition of the legitimate fix space.

### 5.3 Criterion 3 — Distinct from existing principles

**Verdict**: PASS.

**Reasoning**: v1 of this spec proposed an "assertion fidelity" clause that the blind verification correctly identified as a restatement of Principle IX's v2.3.0 behavior-over-shape extension (which already prohibits `assert "headline" in result`, `assert isinstance(rounds_completed, int)`, and the "type-only check" patterns the v1 clause named). v2 drops that clause and explicitly cross-references IX in the principle headline; assertion-fidelity discipline at fix-time is now home to IX, not XXVIII. The remaining two clauses (skip discipline + categorization with diff-shape consistency) cover ground IX does not address:

- **Principle IX (extended v2.3.0 — behavior-over-shape testing)** prohibits writing or rewriting an assertion in shape-only form. It does NOT govern the discipline of *declaring what kind of fix* a PR is performing (categorization), nor does it govern the discipline of *citing skipped bugs* (which is about test-suite hygiene, not assertion shape). v2 of XXVIII explicitly defers assertion fidelity to IX in its headline.

- **Principle XXIV (Safety-Critical Defense-in-Depth)** requires contract tests reproducing failure scenarios for safety-critical synthesis paths. It is about *coverage* — that certain failure modes must have tests at all — not about fix-time discipline.

- **Principle XXVI (Meta-Testing for Parametrized Capabilities)** governs coverage drift across capability sets (e.g., when a new model is added, all capability tests must extend to it). It is about completeness over a parametrization axis, not about test-fix categorization or skip hygiene.

The niche XXVIII fills after the v2 revision is narrow but real: the moment a contributor opens a failing test file in a fix-time PR, declares why they're modifying it, and gets a mechanical check that the declaration is consistent with the diff. That niche is empty in IX, XXIV, and XXVI. The distinctness claim holds for v2 in a way it did not for v1.

### 5.4 Self-assessment conclusion

The principle passes all three criteria. It is admissible as a constitutional amendment under the v2.4.0 gate, subject to the verification protocol in §9 (self-consistency + blind verification per spec 067).

## 6. Mechanical enforcement: CI lint

This spec proposes a follow-up PR adding `scripts/lint-test-fixes.py`. That script is *not* implemented in this spec — only its contract is described, so the principle's mechanical-verification-capability claim in §5.1 has a concrete referent.

**Behavior** (v2 — narrowed after blind verification dropped assertion-loosening detection as IX's territory):

- Walks the PR diff in two passes: a *test-side pass* over files matching `**/test_*.py` or `**/*_test.py`, and a *production-side pass* over everything else excluding `docs/`, `specs/`, `deliberations/`, `.github/`.
- **Skip-discipline check (clause 1)**: in the test-side pass, identifies newly added `pytest.skip(...)`, `@pytest.skip`, or `@pytest.mark.skip` directives. For each, walks adjacent comment lines and docstrings and matches against `(issue|PR|#\d+|TODO\(.+\))` plus a remediation cue (regex including `by \d{4}-\d{2}-\d{2}`, `next release`, `before merge`, etc.). Newly added skip directives without a citation are flagged as violations.
- **Diff-shape-consistency check (clause 2)**: reads the declared category from a structured PR-template field (per §7 — the field is an HTML comment marker `<!-- test-fix-category: ... -->` or equivalent machine-readable form). Compares against the actual diff shape from the two passes:
  - Claim "fixture/path drift" + production-side modifications detected → mismatch (flagged).
  - Claim "production bug" + zero production-side modifications → mismatch (flagged).
  - Claim "defunct test" + zero test-file deletions → mismatch (flagged).
  - Claim "legitimate test bug" + missing PR-body bug citation (regex against PR body for issue/PR number) → mismatch (flagged).
- Produces a CI annotation: warns with file paths and line numbers for each flag. Does not block merge automatically — the PR template (§7) carries the blocking requirement via explicit reviewer sign-off.

**Heuristic limit acknowledged**: the diff-shape check cannot detect a misjudgment within a category — for example, a "fixture drift" claim with only test-file edits that is actually a "legitimate test bug" miscategorized. That residual is exactly what the principle's clause 2 acknowledges and what reviewer judgment must catch. The lint catches the high-frequency, structurally detectable failure mode (label vs diff inconsistency); it is not a substitute for review.

**Primary enforcement** is the PR template (§7) plus Principle XXVIII itself. The lint catches the cases the author or reviewer might miss; it does not replace either.

**What v1's lint did and v2's does not**: v1 included AST-diff detection of assertion loosening (`==` → `in`, exact → type-only). Those checks now belong in a Principle IX lint (or are out of scope entirely if IX-violating assertions are caught at code review). Putting them in v2's XXVIII lint would re-create the distinctness conflict the blind verification flagged.

## 7. PR template additions

This spec proposes a follow-up PR adding the following section to `.github/pull_request_template.md`:

```markdown
## Test fixes (required if any test file is modified)

If this PR is fixing a failing test (Principle XXVIII), declare the
category in the machine-readable marker below. If multiple test fixes
in different categories, list one marker per fix.

<!-- test-fix-category: fixture-drift | production-bug | legitimate-test-bug | defunct-test -->

Self-check (each box must be ticked or the PR violates Principle XXVIII):

- [ ] The category marker above declares each test fix
- [ ] The diff shape matches the declared category
  (fixture-drift: only test files; production-bug: ≥1 production-source
  file; legitimate-test-bug: only test files + PR body cites the test-side
  bug; defunct-test: test deletion + PR body explains why)
- [ ] Any newly added `pytest.skip` cites the bug + remediation timeline
- [ ] Assertion-fidelity discipline (Principle IX behavior-over-shape) was
  preserved; loosened assertions, if any, are justified in the PR body
- [ ] If `lint-test-fixes.py` flagged anything, the flag is justified
```

The structured category marker (HTML comment with a known prefix) is what the lint script reads to perform the diff-shape consistency check (§6). The checkbox structure forces an explicit declaration; the marker makes that declaration machine-readable so the lint can act on it.

## 8. Spec 067 amendment (operational guidance for verification deliberations)

This spec proposes a follow-up PR adding a new §4.6 to `specs/067-verification-methodology/spec.md`:

> **§4.6 Test-fix discipline during verification.** When a verification deliberation surfaces failing tests in the deliberation's target codebase, the implementer MUST run the 4-subagent investigation pattern (root-cause categorization per Principle XXVIII categories — fixture drift / production bug / legitimate test bug / defunct test) BEFORE proposing fixes. The pattern dispatches one subagent per category and produces a per-test classification, which the implementer reviews and ratifies before any test or code change is made. PR #42 (2026-04-28, conversus-oss) is the canonical reference implementation and should be linked from any future PR that exercises this pattern, until enough exemplars exist to consolidate into a SKILL.md.

The amendment makes the 4-subagent pattern the explicit first response to "verification surfaced failing tests," rather than ad-hoc per-deliberation invention. PR #42 is the canonical exemplar; later deliberations link back to it until the pattern matures into its own skill.

## 9. Verification

Per spec 067 §4 (and the v2 protocol if landed by the time this spec ships), this spec must run BOTH self-consistency verification AND blind verification before its implementation PR (the actual `CONSTITUTION.md` edit adding Principle XXVIII) can land.

**Where the deliberations live**:
- Self-consistency: `deliberations/071-self-consistency-{date}/`
- Blind: `deliberations/071-blind-{date}/`

**Acceptance bar**: 0 ACCEPT-level findings on Principle XXVIII wording specifically. Findings on §6 (lint contract), §7 (PR template), or §8 (spec 067 amendment) are tolerable at REVISE level if they do not alter the principle text — those sections specify follow-up PRs which can be revised independently. The principle text itself, being the load-bearing constitutional change, must clear with no ACCEPT findings.

**What "0 ACCEPT findings on principle wording" means concretely**: if either deliberation surfaces a finding rated ACCEPT (i.e., the reviewer believes the wording must change before merge), this spec returns to Draft status and the wording is revised. REVISE-rated findings prompt a response in the spec but do not block. INFO-rated findings are noted for future reference.

## 10. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| The CI lint produces too many false positives, gets ignored by authors and reviewers alike | Medium | Heuristic + human review by design; lint warns, PR template requires explicit sign-off; track false-positive rate quarterly and tune the heuristic; Q1 in §11 considers escalation from advisory to blocking only after the rate stabilizes. |
| Authors checkbox-comply without thinking, ticking all four boxes by reflex | Medium | Reviewer asks "which category?" verbally on first round of review; a checkbox without a corresponding written categorization in the PR body is itself a violation; the categorization claim is verifiable against the diff (per §5.2), so a reflexive tick produces structural inconsistency that becomes visible. |
| Principle interpreted too strictly, blocks legitimate test refactoring (e.g., consolidating duplicate tests, renaming for clarity) | Low | The four categories include "legitimate test bug" — refactoring that genuinely improves the test lands there, with the bug-or-improvement documented in the PR body. Pure cosmetic refactoring (renames, formatting) is out of scope of the principle, which only triggers on *fixing failing tests*. |
| Production bugs still ship if reviewer is also incurious and lint is silent | High | All four layers (principle + PR template + CI lint + spec 067 §4.6 protocol) must fail simultaneously for this class of regression to ship. This is the residual risk this spec accepts; no enforcement mechanism eliminates it entirely. The 4-subagent pattern in §4.6 is the deepest layer — a verification deliberation that runs the pattern would catch what slips through the other three. |
| The principle accumulates exception cases over time, eroding into a checklist nobody reads | Low | The categorization clause is exhaustive over legitimate fixes (per §5.2); exception cases would have to redefine the partition, which is a constitutional amendment, not an erosion. The MAJOR/MINOR governance process (CONSTITUTION.md Versioning) catches that. |
| Q3 (mutation testing) gets deferred forever and the lint heuristic stays brittle | Low | Q3 is explicitly a follow-up question in §11; if the lint's false-positive or false-negative rate becomes unacceptable, mutation testing as a 5th layer becomes a separate spec rather than an implicit obligation of this one. |

## 11. Open questions

- **Q1**: Should the CI lint be advisory (annotation only) or blocking (failing CI status)? Recommend: advisory at first, observe false-positive rate over 3-6 months, escalate to blocking if discipline holds and the rate is acceptable. A premature blocking lint that fires on legitimate work would erode trust in the principle itself.
- **Q2**: Does this principle interact with the verification methodology (spec 067) in a stronger way than §8 captures? Specifically — when blind verification surfaces a failing test, the implementer applies the principle automatically, but should that automatic application be encoded as an obligation rather than a recommendation? The §4.6 amendment uses MUST language, which is the strong form. If §4.6 lands as drafted, the obligation is explicit.
- **Q3**: Mutation testing as a 5th layer? `mutmut` (or equivalent) can detect when an assertion no longer catches mutations of the production code — i.e., the strongest possible check that an assertion is doing real work. Cost: very high (mutation suites are minutes-to-hours per run). Defer to a follow-up spec; the four-layer model in this spec is sufficient for the discipline this spec targets.
- **Q4**: Version bump. Adding a new principle is a MINOR version bump per CONSTITUTION.md Versioning (new principle, no breaking change to existing principles, no change to amendment process). v2.4.0 → v2.5.0.

## 12. Acceptance criteria for this spec

This spec is "done" — meaning ratified, ready for implementation PRs to file — when:

1. Principle XXVIII wording (§4) is reviewed and approved by the verification deliberations (§9).
2. The §5 self-assessment satisfies the v2.4.0 Constitutional Inclusion Criteria gate as judged by the deliberations (no ACCEPT-level finding rejecting any of the three criterion verdicts).
3. The CI lint reference implementation (`scripts/lint-test-fixes.py`) is filed in a follow-up PR. This spec authorizes the script's contract (§6) but does not produce the script.
4. PR template additions (§7) are filed in a follow-up PR.
5. Spec 067 amendment §4.6 (§8) is filed in a follow-up PR.
6. Both verification deliberations (§9) run with 0 ACCEPT findings on principle wording.
7. The implementation PR (the actual `CONSTITUTION.md` edit adding Principle XXVIII and bumping the version to v2.5.0) merges.

Items 3, 4, and 5 are independent PRs that can proceed in parallel once the principle wording clears the deliberations. Item 7 is the gating merge — once it lands, Principle XXVIII is in force and the follow-up PRs (3-5) become the operational scaffolding around it.

## 13. References

- **PR #42** — `fix(handlers,tests): resolve find_project_root shadowing + quality-floor path drift`. The case study that originated this principle. Demonstrates the 4-subagent investigation pattern and the assertion-fidelity discipline in action.
- **Spec 045** — test-coverage-review (now in `specs/done/`). The verification deliberation that surfaced the 95 failing tests.
- **Spec 067** — verification-methodology. Defines the protocol the implementation PR must satisfy and the §4.6 amendment this spec proposes.
- **Spec 069** — mechanical-verification-gate. Defines the v2.4.0 Constitutional Inclusion Criteria gate this principle's §5 self-assessment satisfies.
- **CONSTITUTION.md v2.4.0** — current state. The implementation PR bumps this to v2.5.0 (MINOR, per §11 Q4).
- **2026-04-28 4-subagent investigation outputs** — Cat A (fixture-path drift), Cat B (production bug surface), Cat C (legitimate test bugs), Cat D (defunct or fragile-by-design tests). The verdicts feed PR #42's commit narrative and the §4.6 amendment's reference implementation.
