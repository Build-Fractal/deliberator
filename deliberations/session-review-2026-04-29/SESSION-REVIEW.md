# Session Review — 2026-04-29

This document captures the engineering output of a 2026-04-29 session that produced 8 PRs (5 ratification, 2 dogfood-driven fixes from Brett, 1 follow-up test PR) plus 3 GH issues. The conversus deliberation reviewing this document is asked to evaluate the engineering judgment, identify gaps, and stress-test the override-with-rationale precedent established earlier in the session.

## Session timeline

1. **PR #46** — `feat(constitution): v2.4.0 → v2.5.0 — Principle XXVIII (Test-Fix Boundary Preservation)`. Ratified after self-consistency PASS WITH FIXES + blind v1 "move to operational guidance" + blind v2 PASS WITH FIXES. Override-with-rationale applied to blind v2 rulings 1+2 on the grounds that the arbiter's "acknowledged residual = operational guidance" reading, applied uniformly, would shrink Principle IX's behavior-over-shape extension.
2. **PR #47** — `docs(spec-067): add §4.6 — Test-fix discipline during verification`. Implements spec 071 §8.
3. **PR #48** — `feat(pr-template): add Principle XXVIII test-fix discipline section`. Implements spec 071 §7.
4. **PR #49** — `feat(lint): scripts/lint-test-fixes.py + advisory CI workflow`. Implements spec 071 §6. 641 LOC + 35 tests.
5. **PR #50** — `chore(specs): close 064-capability-discovery (move to done/)`. Cleanest close from the audit burndown.
6. **PR #51** (Brett) — `fix(skills): install probe + OAuth provider preflight + version bump`. Three skill-bundle bugs surfaced during dogfood.
7. **PR #52** (Brett) — `fix(engine): silent-stub abort + claude-code model passthrough + decide --model`. The HIGH-severity false-success deliberation fix.
8. **PR #56** — `test(cli): add decide --model propagation tests (closes #55)`. Two regression tests added as the executable follow-up.

All 8 merged.

## My review of PR #51 and PR #52

### PR #51 — skill bundle fixes

| Change | Verdict |
|---|---|
| `command -v conversus >/dev/null 2>&1` install probe | ✅ Correct — `--version` doesn't exist; `command -v` is canonical POSIX presence check; consistent across 8 skills |
| OAuth preflight in `decide`/`run` skills | ✅ Correct — `${CONVERSUS_PROVIDER+set}` properly distinguishes "unset" from "empty"; explicit operator value always wins |
| Plugin version 0.1.0 → 0.3.0 | ✅ Routine sync to CLI ship version |

**Concerns (non-blocking):**
- DRY violation: OAuth preflight duplicated verbatim in 3 places (orchestrator adapter, decide skill, run skill). At a 4th copy, factor out.
- The OAuth marker regex `(access_token|oauth|subscription)` is heuristic; false negatives just fall through to the 429.

### PR #52 — engine fixes

| Change | Verdict |
|---|---|
| Bug 3a — `FatalProviderResponseError` + pattern detection | ✅ Strong fix. `_detect_provider_passthrough_error` caps at 1KB head, case-insensitive, structured to grow. `_gated_dispatch` checks `FatalProviderResponseError` BEFORE generic `BaseException` — type-narrowing order is correct (XXVIII would be unhappy if reversed). |
| Bug 3b — `claude_code.py` model fallback | ⚠️ Works but is a value-blocklist (`if model == "claude-sonnet-4-20250514"`). The PR explicitly chose scoped fix over `Optional[str]` refactor. |
| Bug 3c — `decide --model` flag | ✅ Routine click option addition; threads through to `run_engine`. |

**Concerns (non-blocking):**
- No explicit test for `decide --model X` flow propagating to dispatcher.
- 1KB head check for passthrough detection is untested with long-response edge cases.
- Pattern is currently a singleton tuple; future-proof but not yet exercised.

## Follow-up issues filed

| Issue | Title | Status | Rationale for status |
|---|---|---|---|
| #53 | refactor: factor OAuth preflight into single source | filed, NOT executed | Issue text states trigger condition: "When a 4th use site appears, factor first." We're at 3 sites. Cross-repo source-path complexity (skills installed in `.claude/plugins/...`) makes the factoring substantially harder than the duplication tax warrants until the trigger fires. |
| #54 | refactor(engine): propagate Optional[str] model through dispatch (retire value-blocklist) | filed, NOT executed | Issue captures the bigger refactor PR #52 explicitly deferred. Multi-file scope, touches all providers. Benefits from review-before-execute. |
| #55 | test: add decide --model propagation test | filed AND executed via PR #56 | Smallest scope, highest test-discipline value (regression coverage for PR #52 Bug 3c that shipped without propagation assertion). |

## Executed work — PR #56

Added 2 regression tests in `engine/tests/test_cli.py::TestDecideCommand`:

1. `test_decide_model_flag_propagates_to_run_engine` — invokes `decide --model claude-3-5-haiku-20241022` with `run_engine` monkeypatched to capture kwargs; asserts the model value reached the dispatcher.
2. `test_decide_no_model_flag_propagates_none` — invokes `decide` without `--model`; asserts `model=None` is passed through (signaling "use provider default" rather than a hardcoded CLI fallback).

Both use `monkeypatch.setattr("engine.run.run_engine", fake_run_engine)`. Tests pass in 0.07s combined.

PR #56 self-categorized as `legitimate-test-bug` per Principle XXVIII clause 2: the test surface had a gap (no propagation assertion) that is now closed; PR body cites the originating PR (#52) as the bug source per the diff-shape rule.

## Questions for this deliberation

The agents are asked to address three questions:

### Q1 — Was the review thorough enough?

I identified 3 concerns on #51 (DRY duplication, regex heuristic, version sync routine) and 3 on #52 (no propagation test, 1KB head untested, singleton pattern tuple). Did I miss anything? Specifically:
- Are there security implications of the OAuth marker regex matching arbitrary substrings in `auth.json`?
- Is the `_gated_dispatch` re-raise pattern racy under concurrent agent dispatch in cooperative mode?
- Does the 1KB head check create an attack surface where a malicious provider could craft a response that hides the error string past byte 1000?

### Q2 — Was the execution scope-correct?

I executed only #55 (the test PR), deferring #53 (OAuth factor) and #54 (Optional[str] refactor). Was deferring #53 correct given the issue's own stated trigger condition? Or does "execute on the followup" override a self-imposed trigger?

### Q3 — Is the override-with-rationale precedent dangerous?

The earlier session ratified Principle XXVIII over the blind v2 verdict, citing "uniform application would shrink Principle IX." Is this precedent abuse-vulnerable? Specifically:
- Could a future amendment author cite "uniformity stress-test" to override any blind verdict by pointing at any analogous existing principle?
- What's the remedy if the precedent is invoked in bad faith?
- Should the precedent itself be promoted to a constitutional principle, or kept as a governance-log artifact?

## Acceptance bar for this deliberation

- 0 ACCEPT findings on the engineering work itself (PR #56 + the executed scope).
- ACCEPT findings on the override-with-rationale precedent (Q3) are explicitly DEFER-eligible — they affect future amendments, not this session's work.
- Findings on PR #51 or PR #52 (already merged) are RECOMMENDED-fix or filed as new issues; they do not block this deliberation's verdict.
