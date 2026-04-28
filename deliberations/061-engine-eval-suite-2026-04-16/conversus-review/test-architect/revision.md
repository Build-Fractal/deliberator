# Test Architect -- Revised Position

**Original review**: review.md
**Cross-reviews received from**: engine-implementor, consumer-advocate
**Date**: 2026-04-16

---

## What I Withdraw

### 1. "Fix the mock provider to return parseable synthesis" as a P0 (original recommendation #2)

The consumer-advocate's counter-proposal is better than mine. I originally called for building a "realistic response mode" in the mock provider that generates well-structured markdown per phase and mode. The consumer-advocate correctly identifies this as "a test infrastructure project masquerading as a bug fix" -- it entangles mock provider behavior with synthesis format expectations and blurs the clean separation between the structural smoke tier and the semantic quality tier.

I withdraw the recommendation to modify the mock provider. The consumer-advocate's alternative -- a single targeted smoke test that calls `parse_synthesis()` directly with a known-good markdown fixture and asserts the five output fields are populated -- addresses my core concern (synthesis parser regressions are invisible in the smoke tier) without the engineering cost or tier-blurring risk. The mock provider stays cheap and deterministic. The parser gets its own dedicated regression test. My original diagnosis was correct; my proposed remedy was wrong.

### 2. Cancellation tests at P2 (original recommendation #13)

The engine-implementor is right that cancellation tests belong at P3, not P2. `CancellationFlag` is cooperative (check-between-phases), the mechanism is straightforward, and meaningful testing requires either a slow provider or phase-boundary injection -- both of which are disproportionate for v1 of the suite. I was conflating "untested code path" with "high-risk code path." The cancellation mechanism is low-complexity even though it is untested. P3.

### 3. Persistence internals as eval-suite concerns (original section 2.6, items 3-4)

The engine-implementor correctly distinguishes eval-suite scope from unit-test scope. "Persistence disabled via settings" and "old deliberation cleanup" are unit test concerns that belong in `engine/tests/`, not in the eval suite. The eval suite validates externally observable behavior. I withdraw these two items from the eval suite scope. The persist-then-read round-trip test remains valid as an integration test (both reviewers agree), but it is P3, not P2.

### 4. `--format rich` structural testing beyond exit-code-zero (original recommendation #16)

The engine-implementor is right that validating rich terminal rendering in CI requires a terminal emulator, which is disproportionate. Exit-code-zero and "produces output to stdout" is sufficient for the eval suite. Full structural validation of rich output is P4 at best. Withdrawn from the priority list.

---

## What I Strengthen

### 1. Multi-round pipeline tests remain P0 -- with stronger justification

Both cross-reviewers validate this finding. The engine-implementor calls it "the most intricate code paths in the engine" and agrees it belongs at P0. The consumer-advocate does not mention multi-round at all, which actually reinforces my point: if the consumer-facing reviewers are not thinking about rounds, stagnation, and convergence termination, then only the test architect is advocating for coverage of these paths. Without a dedicated champion, they will be deprioritized indefinitely.

I strengthen this: the multi-round tests are not just P0 -- they should be the first functional tests implemented after the P0 bug fixes. The specific test cases I proposed (rounds=2 convergence, rounds=3 stagnation, rounds=5 max_rounds) are confirmed implementable by the engine-implementor. The `termination_reason` field is the correct assertion target.

### 2. `VALID_PROVIDERS` hardcoded to two is more severe than I initially framed

Both cross-reviewers validated this finding. The engine-implementor calls it "a critical structural finding" and a "config validation bug" distinct from the auth.py resolution divergence. The consumer-advocate identified that it means even after auth wiring is fixed, config-file-based runs cannot use most providers.

I strengthen this from a section 6.1 structural observation to a known gap nomination. This should become G11 (or whatever the next gap number is): `VALID_PROVIDERS` in `config.py` line 82 is hardcoded to `("anthropic", "openai")`, which means YAML configs with any other provider are rejected at parse time, while CLI `--provider` bypasses this entirely. The eval suite must include a test that writes a YAML config with each registered provider name and verifies whether `parse_config` accepts it.

### 3. Desktop extension divergence is a prerequisite, not just a test gap

The consumer-advocate's framing is sharper than mine: "The spec must first answer the test-architect's question: which copy is canonical? ... Only after this is resolved do the consumer-advocate's Desktop-specific behavioral tests become meaningful." This elevates my section 2.5 from "add a parity test" to "resolve the canonicality question before Desktop tests are meaningful at all." I originally framed this as P1 recommendation #7. It should be a P0 *question* that the spec must answer (even if the testing itself remains P1), because downstream test design depends on the answer.

### 4. The `is-json` promptfoo assertion weakness

The consumer-advocate independently validated this finding ("checking `headline !== undefined` while ignoring the other 4 required fields is insufficient"). The promptfoo assertions must validate all 5 required fields of the output schema. This is trivial to fix and has no reason to be deferred.

### 5. Pydantic schema snapshot tests -- now with cross-surface schema mapping

The consumer-advocate extends my schema snapshot recommendation (section 5.2) into a two-part approach: my snapshot test catches regressions over time, while their cross-surface schema mapping test catches cross-surface inconsistencies right now, using `ConversusOutput` as the canonical model. Both are needed, and together they form a more complete schema stability strategy than I originally proposed. I adopt this combined approach.

---

## What I Modify

### 1. SDK surface priority: P2 -> P1

My original review placed SDK cross-surface parity at P2 (recommendation #12). The consumer-advocate argues for P0, noting that the SDK is the primary surface for programmatic Python consumers and CI/CD pipelines. The engine-implementor argues for keeping it lower but frames SDK parity as "inner content equivalence, not structural type identity."

I accept the engine-implementor's framing -- SDK parity means verifying that the inner content (headline, summary, full_analysis, quality_indicators, debate_transcript) maps consistently to CLI JSON output, not that `engine.sdk.Result` and `engine.results.DecideResult` are the same type. These are different wrapper types by design.

I accept the consumer-advocate's priority escalation partially. P0 is too high because the SDK cannot be meaningfully tested until the P0 bugs (G1, G2) are fixed and the mock provider's synthesis path is addressed. But P2 (original) is too low given that the SDK is how external Python code calls the engine. Modified to P1, implemented alongside settings cascade and SKILL.md parity tests, as the consumer-advocate recommends. The specific test is lightweight: `Deliberation(question="Q", provider="mock").run()` returns a `Result` whose field set maps to the CLI JSON output field set.

### 2. Arbiter tests: implementability depends on mock enhancement decision

My original review proposed arbiter tests at P1 (recommendation #6). The engine-implementor raises a practical constraint I did not consider: arbiter tests that verify "arbiter fires on real disputes" require a provider that produces genuine disputes. Mock provider output does not contain structured disagreement markers. Since I have now withdrawn the "realistic response mode" for mock, arbiter-fires tests need either a real provider or a mock fixture that produces dispute-shaped output.

I modify the recommendation: split arbiter tests into two tiers:
- **Smoke tier (P1)**: Arbiter configured but no disputes detected -- verify arbiter does not fire, and `trigger: always` -- verify arbiter fires regardless. These work with mock.
- **Functional tier (P2)**: Arbiter fires on real disputes, binding vs advisory influence, inter-round timing. These require either a real provider or a dedicated dispute-fixture mechanism.

### 3. Provider test levels: add a fifth level

My original four-level taxonomy (import / instantiate / auth-resolve / dispatch) is endorsed by the engine-implementor but missing a dimension identified by the consumer-advocate: **error-message quality**. For the 9+ providers that lack auth wiring, calling `resolve_execution_provider(name)` should produce an error message that names the provider, states what is missing, and suggests remediation.

Modified taxonomy:
1. **Import**: Module imports without error.
2. **Instantiate**: `get_provider(name)` returns an instance.
3. **Auth-resolve**: `resolve_execution_provider(name)` succeeds with credentials.
4. **Dispatch**: `provider.execute(task)` returns a valid `ExecutionResult`.
5. **Error-message quality**: For providers that fail at level 3 or 4, the error message names the provider, explains the failure, and suggests a fix.

The engine-implementor also adds a nuance my taxonomy missed: there are two auth resolution paths (`auth.py` `resolve_provider` vs `run.py` `resolve_execution_provider`), and a provider can pass level 3 through one path but fail through the other. Level 3 tests must cover both paths. I accept this and incorporate it.

### 4. G1 regression test: accept the engine-implementor's position with a caveat

The engine-implementor argues that the smoke test *is* the regression test for G1 -- once G1 is fixed, the smoke test passing is the regression gate, because `decide` calls `build_adhoc_config` then `parse_config` end-to-end. I accept this: a dedicated regression test separate from the smoke test is not needed.

However, I add a caveat: this only holds if the smoke test for red-blue mode actually exercises the `build_adhoc_config -> parse_config -> run_engine` path. If the smoke test uses a pre-built YAML config (as the engine-implementor's own R1 recommends), then it bypasses `build_adhoc_config` entirely, and the G1 regression path is untested. The engine-implementor's R1 ("use pre-built YAML configs for red-blue") and their G1 position ("the smoke test IS the regression test") are in tension. Resolution: the red-blue smoke test should use the adhoc path (not pre-built YAML), which serves as both the mode test and the G1 regression test.

### 5. Settings cascade test scope: narrowed but with isolation requirement

My original section 3.4 called for testing each setting key at each cascade level at each surface (a large combinatorial matrix). The engine-implementor does not dispute the need but adds a critical practical requirement I missed: every test must either mock `load_settings()` or run in a clean temp directory with `HOME` overridden, because settings files on the developer machine or CI runner will contaminate results. The engine-implementor also identifies a specific trap: `run_decide_mcp` treats `provider="mock"` as "not explicitly set" (handlers.py lines 105-107), so the settings cascade can override mock in tests.

I modify the recommendation: the settings cascade tests should focus on the provider key (the highest-value cascade target) and defer other setting keys to P2. But settings isolation must be in the shared test fixtures from day one -- it is a prerequisite for test reliability, not a test in itself. I adopt the engine-implementor's R9 as a P0 infrastructure requirement.

### 6. Quality thresholds: adopt the consumer-advocate's calibration methodology

My original section 4.3 offered two alternatives: calibrate from the first baseline run (P25), or declare thresholds aspirational. The consumer-advocate proposes a specific methodology: baseline minus 0.1 margin. Both reviewers converge on "run once, observe, then set." I adopt the consumer-advocate's approach as more prescriptive and actionable.

### 7. SKILL.md parity: accept escalation

My original review mentioned SKILL.md masking engine bugs (section 1, paragraph 3) but did not make it a numbered recommendation. The consumer-advocate argues persuasively that SKILL.md parity should move from step 9 to step 4-5 in the implementation order, and provides the concrete test: parse SKILL.md examples, run each via CLI, verify each SKILL.md-advertised provider resolves. I adopt this escalation and add it as a P1 recommendation.

---

## Items I Did Not Originally Address -- Accepting from Cross-Reviewers

### From the engine-implementor

1. **Two provider resolution paths (auth.py vs run.py)**: The engine-implementor identified that `engine/auth.py` `resolve_provider()` and `engine/run.py` `resolve_execution_provider()` are different functions with different provider coverage. MCP handlers use the former, CLI uses the latter. This should be documented as a known gap and both paths tested at provider level 3. I accept this as a P1 addition.

2. **`run_decide_mcp` mock provider default cascade**: `provider="mock"` is treated as "not explicitly set" in handlers.py, meaning settings cascade can override it. This is a test reliability landmine. Accepted as part of the P0 settings isolation requirement.

3. **promptfoo CLI flag name verification**: The spec uses `--format json` but the actual CLI may use a different flag name. Accepted -- the promptfoo config must be validated against the actual CLI argument parser.

4. **deepeval judge model specification**: deepeval defaults to GPT-4 as the LLM judge. If the team wants Anthropic models as judges, this needs explicit configuration in the spec. Accepted as a P2 addition.

5. **conftest.py fixture reuse**: The existing `engine/tests/conftest.py` has shared fixtures. The eval suite should integrate with these rather than creating parallel infrastructure. Accepted as a P1 implementation guideline.

### From the consumer-advocate

1. **CI/CD governance exit codes**: The engine has two exit code schemes (interactive and governance). CI/CD pipelines using conversus as a quality gate need governance exit codes (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE). I did not mention exit code semantics at all. This is a significant gap for CI/CD consumers. Accepted as P1.

2. **Env var type coercion edge cases**: `CONVERSUS_MAX_LAUNCHES=abc` should fall through gracefully. The settings cascade includes an env-var layer with type coercion, and malformed values are a distinct failure mode. Accepted as part of the settings cascade tests.

3. **MCP tool count assertion**: If conversus exposes too many MCP tools, Cursor users hit the 40-tool limit. This is a consumer-facing constraint the eval suite should enforce as a smoke test. Accepted as P2.

4. **Sensitive field handling**: `ANTHROPIC_API_KEY` marked `sensitive: true` should never appear in logs or error output. Secret leakage testing is a legitimate eval concern. Accepted as P2.

5. **Paid tier groundwork**: HTTP surface shape, `PAID_TIER_REQUIRED` error testing, cost telemetry verification. These are forward-looking but the spec is explicitly building toward a paid tier. Accepted as P2 placeholders that should be documented in the spec even if not implemented in v1.

---

## Revised Priority List

Incorporating all withdrawals, modifications, and accepted items:

| Priority | Item | Source | Change from original |
|---|---|---|---|
| P0 | Add `parse_synthesis()` fixture test (not mock provider rewrite) | Test architect (modified per consumer-advocate) | **Modified** -- targeted fixture test replaces mock rewrite |
| P0 | Add multi-round pipeline tests (rounds=2 convergence, rounds=3 stagnation, rounds=5 max_rounds) | Test architect, section 2.2 | Unchanged |
| P0 | Test adhoc red-blue end-to-end through `build_adhoc_config -> parse_config -> run_engine` | Test architect, section 5.3 (reconciled with engine-implementor) | **Modified** -- adhoc path, not pre-built YAML |
| P0 | Define provider test levels (5-level taxonomy) per provider | Test architect, section 4.4 (extended per consumer-advocate) | **Modified** -- added level 5 (error-message quality) |
| P0 | Settings isolation in shared test fixtures (clean HOME, mocked load_settings) | Engine-implementor R9 | **New** -- accepted from engine-implementor |
| P0 | Answer desktop extension canonicality question in the spec | Test architect, section 2.5 (elevated per consumer-advocate framing) | **Elevated** -- from P1 test to P0 question |
| P1 | Add SDK cross-surface parity test (inner content equivalence) | Test architect (modified per both cross-reviewers) | **Elevated** from P2 to P1 |
| P1 | Add arbiter smoke tests (trigger=always, trigger=disputes_remain with no disputes) | Test architect, section 2.3 (split per engine-implementor constraint) | **Modified** -- smoke-only at P1, full arbiter at P2 |
| P1 | Add iteration loop tests (iterations=3 produces 3 cross-review rounds) | Test architect, section 2.4 | Unchanged |
| P1 | Add Pydantic schema snapshot tests + cross-surface schema mapping against `ConversusOutput` | Test architect + consumer-advocate | **Strengthened** -- combined approach |
| P1 | Strengthen promptfoo assertions to validate all 5 required output fields | Test architect, section 4.2 | Unchanged |
| P1 | Nominate VALID_PROVIDERS config bug as new known gap; add parse_config test per provider | Test architect, section 6.1 | **Elevated** from observation to gap nomination |
| P1 | Distinguish auth.py and run.py resolution paths; test both at provider level 3 | Engine-implementor R5/R7 | **New** -- accepted from engine-implementor |
| P1 | SKILL.md parity test (parse examples, verify provider list matches) | Consumer-advocate (escalated from step 9 to step 4-5) | **New** -- accepted from consumer-advocate |
| P1 | CI/CD governance exit codes (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE) | Consumer-advocate, section 3.3 | **New** -- accepted from consumer-advocate |
| P1 | Settings cascade: provider key at each level, with env var type coercion edge cases | Test architect (narrowed) + consumer-advocate | **Modified** -- narrowed to provider key, added env var coercion |
| P1 | Integrate with existing conftest.py fixtures | Engine-implementor | **New** -- accepted from engine-implementor |
| P1 | Calibrate deepeval thresholds after first baseline run (baseline minus 0.1 margin) | Test architect + consumer-advocate | **Modified** -- adopted specific methodology |
| P2 | Add arbiter functional tests (real disputes, binding vs advisory, inter-round timing) | Test architect, section 2.3 | **Modified** -- split from P1 arbiter smoke |
| P2 | Desktop extension schema parity test (once canonicality is resolved) | Test architect, section 2.5 | Unchanged priority, but now depends on P0 answer |
| P2 | Specify deepeval judge model | Engine-implementor R10 | **New** -- accepted from engine-implementor |
| P2 | MCP tool count assertion (Cursor 40-tool limit) | Consumer-advocate, section 5.1 | **New** -- accepted from consumer-advocate |
| P2 | Sensitive field handling (API keys not in logs/errors) | Consumer-advocate, section 3.1 | **New** -- accepted from consumer-advocate |
| P2 | Paid tier placeholders (HTTP surface shape, PAID_TIER_REQUIRED, cost telemetry) | Consumer-advocate, section 4 | **New** -- accepted from consumer-advocate |
| P2 | Verify promptfoo CLI flag names against actual argument parser | Engine-implementor R4 | **New** -- accepted from engine-implementor |
| P2 | Settings cascade: remaining setting keys beyond provider | Test architect (deferred from P1) | **Deferred** from original scope |
| P3 | Cancellation tests | Test architect, section 2.7 | **Demoted** from P2 per engine-implementor |
| P3 | Persistence round-trip test (persist-then-read) | Test architect, section 2.6 | **Demoted** from P2, internals withdrawn |
| P3 | `--format rich` exit-code-zero test | Test architect, section 3.3 | **Demoted** from P2, structural testing withdrawn |

---

## Revised Verdict

Conditional approval, same as the original review. The cross-reviews did not introduce findings that would change the verdict to rejection -- the spec's two-layer eval architecture (promptfoo + deepeval) is sound, the Known Gaps table is a genuine strength, and the test markers map cleanly to CI cadence. But the conditions for approval have shifted:

**Original conditions** focused on engine-internal coverage gaps (multi-round, arbiter, mock provider, provider levels). **Revised conditions** are broader: the P0 list now includes settings isolation infrastructure (engine-implementor) and the desktop extension canonicality question (consumer-advocate framing), and the P1 list now includes consumer-facing concerns (SDK parity, CI/CD exit codes, SKILL.md parity) that I originally missed or underweighted.

The single most important revision is replacing my "fix the mock provider" P0 with the consumer-advocate's "add a parse_synthesis fixture test" approach. This addresses the same risk (synthesis parser regressions invisible in smoke tier) at a fraction of the cost, without compromising the clean separation between test tiers. The engine-implementor endorsed this resolution. All three reviewers are now aligned on the approach.

The second most important revision is acknowledging that my original review was biased toward engine-depth testing and underweighted consumer-surface testing. The consumer-advocate correctly identified that SDK parity, CI/CD exit codes, and SKILL.md consistency affect more users than multi-round stagnation detection. I still believe multi-round tests are P0 (the code paths are genuinely high-risk), but the implementation order should interleave engine-depth and consumer-surface tests as the consumer-advocate recommends, rather than completing one dimension before starting the other.
