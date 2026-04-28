# Cross-Review: Test Architect's Review

**Reviewer**: Engine implementor
**Reviewing**: Test architect's review of Spec 061
**Date**: 2026-04-16

---

## Overall Assessment

The test architect's review is the strongest of the three reviews in identifying what the spec *doesn't* test. Where my review focused on whether the spec's proposed tests are implementable against the real codebase, the test architect asked the harder question: does the test matrix actually cover the code paths where bugs live? Their central thesis -- that the spec tests the "simple center" of the configuration space while leaving the "complex edges" untested -- is correct and is a genuine strategic risk to the eval suite's value.

That said, the review occasionally overextends into areas where the proposed additions are either impractical at this stage or lower-value than presented. Below I walk through the specific points of agreement, disagreement, and what each of us missed.

---

## Where I Agree

### 1. Mock provider masks real failures (section 4.1) -- the most important finding

This is the single most important point in the test architect's review, and I missed it entirely in mine. I flagged G6 (mock headline template not filled) as a P3 and moved on. The test architect correctly escalates this: mock provider returns `[mock:agent-name] {prompt}`, which does not contain the markdown headings (`### Headline`, `### Summary`) that `parse_synthesis` expects. The `StructuredDeliberation.from_events()` catches parse failures with a bare `except` and falls back to empty strings. This means every mock-based smoke test is testing the *fallback path*, not the *production path*.

This invalidates the entire smoke tier's claim to detect structural regressions. A mock smoke test that passes tells you the fallback path works; it tells you nothing about whether the synthesis parser works. The test architect is right that fixing this (via a "realistic response mode" in the mock provider) is the single highest-leverage change to the spec. I should have caught this -- I verified each bug against the codebase but did not trace the mock provider's output through the synthesis parser to see what actually happens downstream.

**Verdict: Agree. This should be elevated to a P0 required change.**

### 2. Multi-round pipeline tests (section 2.2)

The test architect is correct that `rounds > 1` is a high-complexity code path with zero dedicated eval tests. The phases.py orchestrator implements stagnation detection, cross-round synthesis, and inter-round arbitration -- these are the most intricate code paths in the engine. My review did not address this because I was focused on whether the spec's *existing* tests are implementable; I should have also asked whether the spec's test scope covers the riskiest code.

The specific test cases proposed (rounds=2 with convergence, rounds=3 with stagnation, rounds=5 with max_rounds termination) are concrete and implementable with mock provider. The `termination_reason` field is the right assertion target.

**Verdict: Agree. Multi-round tests belong in the functional tier at P0.**

### 3. Arbiter interaction (section 2.3)

The test architect correctly identifies that arbitration is a conditional Phase 6 with multiple trigger modes (`disputes_remain`, `always`) and influence levels (`binding`, `advisory`). The spec mentions arbiter only as a config parsing test ("With arbiter -- Valid"). The test architect's proposed tests (arbiter fires with/without disputes, binding vs advisory, timing=inter-round with rounds=1) are all implementable and cover real edge cases.

I would note that arbiter tests require a provider that produces genuine disputes. Mock provider will not generate real disputes because its canned output does not contain the structured disagreement markers that the dispute detection logic looks for. So arbiter tests with mock would likely test the "no disputes detected, arbiter does not fire" path. Testing the "arbiter fires on real disputes" path requires either a real provider or a mock enhancement that produces dispute-shaped output.

**Verdict: Agree on the gap. Partially disagree on immediate implementability -- arbiter-fires tests need the mock enhancement from point 1 above.**

### 4. Desktop extension divergence (section 2.5)

Two copies of the engine is a real risk. I did not address this because my review was scoped to the main engine, but the test architect is right that schema drift between `engine/results.py` and the desktop extension's inline type definitions is invisible without a parity test.

**Verdict: Agree. At minimum, a structural comparison test (JSON schemas match) should exist.**

### 5. Iterations loop (section 2.4)

The spec tests `iterations: 3` only as a config validation test ("Valid, cost estimate reflects 3x"). It does not test that 3 iterations actually produce 3 rounds of cross-review and revision. The test architect is right that this is a functional gap. The cost estimate assertion is necessary but not sufficient -- we also need to verify the output directory structure and the number of intermediate files.

**Verdict: Agree.**

### 6. Pydantic schema snapshot tests (section 5.2)

This is a good idea I did not think of. If a field is added, removed, or renamed on `DecideResult`, `RunResult`, or `ValidateResult`, every MCP consumer breaks silently. A snapshot test that fails on schema changes is cheap to implement and high-value for catching breaking changes before they ship.

**Verdict: Agree. Should be in the smoke tier.**

### 7. Provider test levels (section 4.4)

The test architect's four-level taxonomy (import / instantiate / auth-resolve / dispatch) is better than what I proposed. My review distinguished "resolution" tests from "execution" tests but conflated import and instantiation. The test architect's breakdown is more precise and more useful for implementation: each provider gets tested at the highest level for which we have infrastructure (import and instantiate for all 13, auth-resolve for the 4 with auth.py wiring, dispatch for mock/demo only in CI).

My review added a fifth nuance the test architect's taxonomy does not quite capture: the distinction between auth.py `resolve_provider` and run.py `resolve_execution_provider`. A provider can pass level 3 (auth-resolve) through one path and fail through another. Both reviews identify this divergence, but from different angles -- I found it by tracing the code, the test architect found it by asking "what does 'instantiate' actually prove?"

**Verdict: Agree on the taxonomy. My R5 (distinguish the two resolution paths) is complementary to their recommendation #4.**

---

## Where I Disagree

### 1. Cancellation tests (section 2.7) -- P2 is too high

The test architect lists cancellation tests as a missing dimension and includes them in their P2 recommendations ("should fix before declaring the suite complete"). I disagree on priority. `CancellationFlag` is a cooperative cancellation mechanism -- it sets a flag that phases check between operations. Testing this meaningfully requires either a slow provider (so you can cancel mid-deliberation) or injecting the flag between phases (which is a unit test of the check logic, not an eval test).

For the first version of the eval suite, cancellation testing is P3. The engine's cancellation behavior is straightforward (check flag, raise if set), and the risk of a cancellation bug shipping is low compared to the risk of the mock-provider, multi-round, and arbiter gaps. I would defer this until after the eval suite is delivering value on the higher-priority dimensions.

**Verdict: Disagree on priority. P3, not P2.**

### 2. Persistence layer tests (section 2.6) -- partially disagree

The test architect says the spec does not test persistence at all. This is technically correct, but `engine/tests/` likely already has persistence tests (the infrastructure exists and is used by the handlers). The eval suite's job is to validate the *engine's externally observable behavior*, not to re-test internal plumbing that has unit test coverage.

That said, the "round-trip" test (persist then list/read) is genuinely valuable as an integration test and should be included. But "old deliberation cleanup" and "persistence disabled via settings" are unit test concerns, not eval suite concerns.

**Verdict: Partially agree. Persist-then-read round-trip belongs in the eval suite. The other persistence tests belong in the unit test suite.**

### 3. SDK surface testing (section 2.8) -- agree on the gap, disagree on framing

The test architect correctly identifies that `engine.sdk.Deliberation` returns `engine.sdk.Result`, which has different fields than `engine.results.DecideResult`. This is a real parity gap. However, the test architect frames this as "the spec's cross-surface parity claim (3.3.3) is incomplete," which implies the fix is to extend 3.3.3 to include the SDK.

I would frame it differently: the SDK is a *programmatic consumer surface*, not a *test surface*. The eval suite uses promptfoo (CLI) and pytest (MCP handlers) as its two execution paths. Adding a third execution path (SDK) to the eval framework is significant engineering. The more practical fix is to add a dedicated `test_sdk_parity.py` that compares SDK output fields against the canonical `ConversusOutput` model, and to document that SDK parity is a *unit-level concern* covered by the existing test suite, not an *eval-level concern*.

The consumer advocate's review makes the same point more forcefully (SDK is the primary surface for CI/CD consumers), and I think they are right that it belongs in the eval suite. But the test architect's framing of "cross-surface parity" needs to account for the fact that SDK returns a fundamentally different wrapper type by design -- parity means the inner content matches, not that the wrapper types are identical.

**Verdict: Agree on the gap. Disagree on framing -- SDK parity is about inner content equivalence, not structural type identity.**

### 4. "No test for the G1 bug pattern" (section 5.3) -- this is already covered

The test architect says "the existing test (test_adhoc.py line 49-57) only checks the raw YAML, not whether parse_config(config_path) succeeds." They recommend the eval suite add a test that calls `parse_config` on the generated config.

This is exactly what my R1 says: "red-blue tests must use pre-built YAML configs, not the adhoc decide path." The eval suite's red-blue smoke test *is* the regression test for G1 -- once G1 is fixed, the smoke test passing is the regression gate. The test architect's framing suggests an additional, dedicated regression test is needed. I think the smoke test suffices, provided it actually exercises `parse_config` end-to-end (which it does, because `decide` calls `build_adhoc_config` then `parse_config`).

**Verdict: Disagree. The smoke test IS the regression test. No additional dedicated test needed.**

### 5. Format x Surface matrix (section 3.3)

The test architect identifies that `--format rich` output has no structural assertions. This is true, but rich output is a terminal rendering concern. The eval suite's job is to validate engine correctness, not terminal formatting. Testing that `--format rich` exits 0 and produces output to stdout is sufficient. Validating that the rich output "can be consumed by a terminal renderer without errors" requires running a terminal emulator in CI, which is disproportionate engineering for the value.

**Verdict: Disagree. Exit-code-zero test for --format rich is sufficient. Structural rich output testing is P4.**

---

## What They Caught That I Missed

### 1. Mock provider synthesis path (section 4.1)
As discussed above, this is the most important finding. I missed it completely. The entire smoke tier is testing fallback code paths because mock output is unparseable by the synthesis parser. This finding alone justifies the test architect's review.

### 2. Multi-round and iteration pipeline tests (sections 2.2, 2.4)
I was focused on whether the spec's proposed tests are implementable and did not ask whether the spec's test scope covers the engine's riskiest code paths. The multi-round orchestrator and iteration loop are the most complex code in phases.py and they have zero eval coverage. I should have caught this.

### 3. Two MCP servers / two result type hierarchies (section 6.2)
I noted that `engine/run.py` has a different provider resolution path than `engine/auth.py` (my R11), but I did not notice that the desktop extension has its own inline result types that can drift from `engine/results.py`. The test architect's observation about schema drift between two independently maintained type hierarchies is sharper than mine.

### 4. `VALID_PROVIDERS` hardcoded to two (section 6.1)
This is a critical structural finding. `config.py` line 82 only allows `provider: anthropic` or `provider: openai` in YAML configs, while `resolve_execution_provider` accepts 13+. This means a user who writes a YAML config with `provider: ollama` gets a config validation error, even though `--provider ollama` on the CLI works fine. This is a different bug from the auth.py resolution divergence I identified -- it is a config validation bug. The eval suite should test this explicitly: write a YAML config with each provider name and verify whether `parse_config` accepts it.

### 5. Login handler testing (section 6.3)
I did not address `login_mcp` at all. The test architect correctly notes that auth lifecycle (login, verify credentials persist, logout idempotent) is load-bearing for real providers and deserves concrete assertions.

---

## What I Caught That They Missed

### 1. The two provider resolution paths (auth.py vs run.py)
My review identified that `engine/auth.py` `resolve_provider()` and `engine/run.py` `resolve_execution_provider()` are different functions with different provider coverage, and that MCP handlers use the former while CLI uses the latter. I proposed adding this as G11. The test architect identifies a related symptom (`VALID_PROVIDERS` in config.py) but does not trace the root cause to the handler-level divergence. The test architect's provider test levels (import/instantiate/auth-resolve/dispatch) are the right taxonomy, but they do not distinguish *which* auth resolution path is being tested, which is the actual bug.

### 2. Settings cascade isolation requirement
My R9 notes that every test must either mock `load_settings()` or run in a clean temp directory with `HOME` overridden, because the handlers call `load_settings()` which reads from `~/.conversus/settings.yml`. If either file exists on the developer machine or CI runner, mock provider defaults get overridden. The test architect does not mention test isolation for settings, which would cause flaky tests in practice.

### 3. The `run_decide_mcp` mock provider default cascade issue
My review notes that `run_decide_mcp` treats `provider="mock"` as "not explicitly set" (handlers.py lines 105-107: `provider if provider != "mock" else None`), meaning the settings cascade can override it. This is a subtle test reliability issue: a test passing `provider="mock"` may actually resolve to a different provider depending on the environment. The test architect does not address this.

### 4. promptfoo CLI flag name (`--format` vs `--output-format`)
My R4 flags that the spec uses `--format json` but the actual CLI may use a different flag name. The test architect does not verify CLI flag names against the actual codebase.

### 5. deepeval judge model specification
My R10 notes that deepeval defaults to GPT-4 as the LLM judge, and the spec does not specify which judge model to use. If the team wants to use Anthropic models as judges, this needs explicit configuration. The test architect does not address the judge model choice.

### 6. `_run_in_process` path in handlers.py
My review notes that the `_run_in_process` helper (handlers.py line 491) also calls `resolve_provider` from auth.py, making it a third code path with the same auth resolution limitation. The test architect does not trace this path.

### 7. conftest.py fixture integration
My review notes that the existing test suite has `engine/tests/conftest.py` with shared fixtures and the eval suite should integrate rather than creating parallel infrastructure. The test architect does not address test infrastructure reuse.

---

## Reconciled Priority List

Combining both reviews, here is my proposed implementation priority:

| Priority | Item | Source |
|---|---|---|
| P0 | Fix mock provider to return parseable synthesis (or add realistic response mode) | Test architect, section 4.1 |
| P0 | Add multi-round pipeline tests (rounds=2 convergence, rounds=3 stagnation) | Test architect, section 2.2 |
| P0 | Scope first eval run to exclude red-blue; use pre-built configs for red-blue | Engine implementor, R1/R6 |
| P0 | Fix quality_indicators schema in spec (nested object, not string array) | Engine implementor, R2 |
| P0 | Use wrapper script for promptfoo exec provider (shell quoting) | Engine implementor, R3 |
| P1 | Add arbiter tests (at least trigger=disputes_remain with/without disputes) | Test architect, section 2.3 |
| P1 | Add iteration loop tests (iterations=3 produces 3 cross-review rounds) | Test architect, section 2.4 |
| P1 | Define provider test levels (import/instantiate/auth-resolve/dispatch) per provider | Test architect, section 4.4 |
| P1 | Add Pydantic schema snapshot tests for result types | Test architect, section 5.2 |
| P1 | Specify intermediate artifact access for quality tests | Engine implementor, R8 |
| P1 | Add settings cascade isolation (clean HOME, no project settings) to test fixtures | Engine implementor, R9 |
| P1 | Test VALID_PROVIDERS in config.py against execution provider registry | Test architect, section 6.1 |
| P1 | Distinguish auth.py and run.py resolution paths as separate known gap (G11) | Engine implementor, R5/R7 |
| P2 | Add desktop extension schema parity test | Test architect, section 2.5 |
| P2 | Add SDK to cross-surface parity (inner content, not wrapper type) | Test architect, section 2.8 |
| P2 | Specify deepeval judge model | Engine implementor, R10 |
| P2 | Add CI runner requirements to spec | Engine implementor, R12 |
| P2 | Add login/logout lifecycle tests | Test architect, section 6.3 |
| P3 | Cancellation tests | Test architect, section 2.7 |
| P3 | Persistence round-trip test | Test architect, section 2.6 |
| P3 | Rich format exit-code test | Test architect, section 3.3 |

---

## Final Assessment

The test architect's review is strong. Its most valuable contribution -- that mock provider output bypasses the synthesis parser, making the entire smoke tier test fallback paths rather than production paths -- is a finding that would have caused weeks of wasted effort if discovered after implementation. The missing test dimensions (multi-round, arbiter, iterations) are real and important.

The review slightly overextends on cancellation, persistence internals, and rich format structural testing, where the engineering cost exceeds the bug-detection value for v1 of the eval suite. But these are priority disagreements, not correctness disagreements.

The combination of both reviews covers the spec's gaps comprehensively: my review ensures the proposed tests are *implementable* against the real codebase; the test architect's review ensures the test *scope* covers the code paths where bugs actually live. Both are necessary.
