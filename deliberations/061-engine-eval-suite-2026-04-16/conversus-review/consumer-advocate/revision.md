# Consumer Advocate Revised Position: Spec 061 — Engine Eval Suite

**Reviewer role**: Consumer advocate
**Revision date**: 2026-04-16
**Revision basis**: Cross-reviews from test-architect and engine-implementor

---

## Summary of revision

Both cross-reviews identified a meaningful pattern in my original review: I was thorough on consumer surface coverage but missed the engine's internal complexity. The test-architect's findings on multi-round deliberation, arbitration, mock provider parse failures, and cancellation are gaps I should have caught. The engine-implementor's findings on the dual provider resolution path and the `quality_indicators` schema error are concrete factual corrections. I accept both critiques and incorporate their strongest findings below.

At the same time, both reviewers pushed back on my distribution-layer and future-consumer recommendations. I accept most of those objections but hold firm on a few where the consumer perspective justifies inclusion even in an engine eval spec.

---

## 1. What I withdraw

### 1.1 Cowork HTTP transport and claude.ai web skills testing (original 3.5, 5.3 in part)

Both reviewers correctly identify these as out of scope for the engine eval suite. Cowork does not exist as a shipping consumer. The HTTP+OAuth MCP transport is a distribution concern, not an engine concern. I withdraw the recommendation to add test sections for Cowork and claude.ai as planned consumers. A one-line note in the consumer table ("Cowork -- planned, HTTP+OAuth MCP transport") is sufficient.

### 1.2 .mcpb bundle build test (original 5.3)

The engine-implementor is right: building a ZIP archive and checking its contents is a packaging test, not an engine eval test. This belongs in the Desktop Extension's own CI pipeline. Withdrawn.

### 1.3 MCP tool count assertion for Cursor's 40-tool limit (original 5.1)

The test-architect correctly reframes this as a static documentation concern, not a behavioral test. Conversus exposes 4 tools; the 40-tool limit is about the user's total MCP server portfolio. A CI lint check or a compatibility note in the distribution docs is the right home. Withdrawn from the eval suite.

### 1.4 Paid tier HTTP surface placeholder test section (original 4.1)

The engine-implementor's argument against placeholder tests is persuasive: they pass trivially, catch zero regressions, and create false coverage. I still believe the paid tier transition deserves forward-thinking, but a TODO comment in the spec is sufficient. A placeholder test section is premature. Withdrawn.

### 1.5 Non-darwin platform compatibility test (original 3.1 item 4)

The engine is platform-agnostic Python. The darwin restriction is a Desktop Extension packaging choice. Testing a declared platform constraint is testing packaging, not engine correctness. Withdrawn.

### 1.6 SDK surface at P0 -- downgraded to P1

The test-architect argues the SDK wraps the same engine internals that CLI and MCP exercise, so its risk profile is schema divergence rather than engine-level bugs. The engine-implementor agrees the SDK is critical but frames it as a parity concern. I concede P1 is the right priority. The SDK is important and must be in the suite, but it does not block the eval suite's initial ability to catch engine regressions.

---

## 2. What I strengthen

### 2.1 Settings cascade env var layer is a must-fix, not a should-fix (original 2.3)

The engine-implementor explicitly states: "They are right and I was wrong to rate this 'should fix.' It is a 'must fix.'" The test-architect agrees this is the highest-impact missing cascade level. The env var layer (`CONVERSUS_DEFAULT_PROVIDER`) is how Desktop Extension users configure providers via `user_config` in manifest.json. I strengthen this to P0: the settings cascade test must explicitly include the env var level with the 5-step test I originally specified.

### 2.2 SKILL.md parity must move earlier in implementation order (original 6.4)

Both reviewers agree. The engine-implementor's framing is worth quoting: "SKILL.md divergence is a P1 gap affecting real users today, and deferring it to step 9 of 10 means the most commonly used consumer surface remains broken for the entire implementation timeline." I strengthen the recommendation: move to step 4-5, immediately after fixing G1 and G2, before wiring remaining providers.

### 2.3 Governance exit codes for CI/CD are a real gap (original 3.3 item 1)

Neither cross-reviewer disputes this. The test-architect explicitly says "I did not call this out explicitly. This is a real gap." The engine-implementor says "I did not catch this at all." The engine has two exit code schemes (interactive and governance), and CI/CD pipelines acting as quality gates need the governance scheme (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE). I strengthen this to P1 and add specificity: the eval suite must test `conversus governance` with at least one scenario for each exit code value.

### 2.4 JSON error output consistency (original 3.3 item 4)

Neither reviewer disputes that `--format json` must produce valid JSON even on error paths. The test-architect explicitly calls this "a critical CI/CD concern that I did not address." I strengthen this: the eval suite must verify that for every error scenario in section 3.1.7, `--format json` produces a parseable JSON error object (not plain text), and that stdout contains only JSON while stderr contains only log-level messages.

### 2.5 Desktop Extension content scanner rejection (original 3.1 item 1)

The test-architect rates this as "excellent" and says "I did not catch this at all." The engine-implementor agrees this is a real failure mode. The MCP server already uses a role-split workaround for the content scanner. If a prompt format change breaks the workaround, Desktop users see failures with no engine-level explanation. I strengthen this to P1: all 7 MCP prompts must be tested against content scanner patterns.

---

## 3. What I accept from the cross-reviews and incorporate

### 3.1 Mock provider parse failure is the highest-leverage fix (test-architect, their 4.1)

This is the most important finding I missed. The mock provider returns canned text (`[mock:agent-name] {prompt}`) that does not contain the markdown headings `parse_synthesis` needs. The `from_events()` method catches parse failures with a bare `except` and falls back to empty strings. This means the entire smoke tier tests the fallback path, not the production path.

This is devastating to the eval suite's value proposition. A smoke suite that shows green while the production parse path is broken is worse than no smoke suite -- it creates false confidence. I accept this as P0 and incorporate it into my revised priority list above all my original P0 items.

The fix: the mock provider needs a "realistic response mode" that returns well-structured markdown per phase and mode, or all structural assertions in the smoke tier are meaningless.

### 3.2 Multi-round pipeline testing is a critical gap (test-architect, their 2.2)

I did not mention multi-round deliberation at all. The test-architect correctly identifies that `rounds > 1` exercises the highest-complexity code paths in the engine: round loops with stagnation detection, cross-round synthesis, and inter-round arbitration. These are not exotic features -- any consumer using `rounds: 3` in their config hits untested code.

I accept this as P0 (engine-level risk justifies it even though it is not surface-specific) and incorporate it: at minimum, test rounds=2 with mock provider, verify 2 review phases in the event log, and verify correct `termination_reason`.

### 3.3 Arbiter interaction testing (test-architect, their 2.3)

I missed arbitration entirely. For consumers using full config-based deliberations with `arbiter.trigger: disputes_remain`, this is a critical untested path. I accept this as P1 and incorporate the test-architect's minimum test set: trigger=disputes_remain with and without disputes, influence=binding vs advisory.

### 3.4 Iteration loop testing (test-architect, their 2.4)

I treated `iterations: 3` only as a config parsing concern (via the spec). The test-architect correctly notes that the iteration loop around cross-review and revision is a core pipeline mechanism that must be tested as actual execution, not just config validation. I accept this as P1.

### 3.5 Desktop Extension code divergence (test-architect, their 2.5)

I focused on manifest-level concerns (mode count, content scanner). The test-architect identified a structural problem I missed: `desktop-extension/server/lib/engine/` is a separate copy of the engine with its own inline type definitions. Two engine copies with two result type hierarchies and no parity test is a ticking time bomb for consumer-facing schema drift. I accept this as P1 and incorporate it.

### 3.6 Dual provider resolution path (engine-implementor, their section 1 analysis)

The engine-implementor traces the 9-unwired-providers bug to its root cause: `handlers.py` calls `resolve_provider` (auth.py) while the CLI path uses `resolve_execution_provider` (run.py). These resolve different provider sets with different fallback behavior. My original review treated the 9 unwired providers as a flat fact. The engine-implementor's root cause analysis matters for the spec because:

1. The implementation order step 5 ("wire remaining providers into auth resolver") is misdirected -- the fix is in `handlers.py`, not `auth.py`.
2. The eval suite should test both resolution paths explicitly, not just provider instantiation.

I incorporate this and recommend the spec add this as G11.

### 3.7 `quality_indicators` schema is wrong (engine-implementor, their R2)

The spec shows `quality_indicators` as `["<string>", ...]` but the actual `ConversusOutput` model has it as a `QualityIndicators` object with integer fields (`agent_count`, `mode`, `phases_completed`, etc.). This is a concrete factual error that will cause the output schema test (3.1.6) to fail immediately. I missed this entirely. Incorporated as a must-fix.

### 3.8 First eval run sequencing error (engine-implementor, their R6)

The engine-implementor identifies that step 3 (first eval run) will crash on ConfigError for red-blue mode rather than surfacing engine bugs. I praised the implementation order as "practical" without noticing that the harness itself will fail to run for red-blue mode. The first eval run must explicitly exclude red-blue and scope to cooperative, winner-take-all, and prisoners-dilemma with mock only. Incorporated.

### 3.9 Pydantic schema snapshot testing (test-architect, their 5.2)

I discussed schema differences between surfaces but did not propose schema stability testing as a regression mechanism. The test-architect's recommendation to dump each model's JSON schema and fail on unexpected changes is a concrete, low-cost regression catch. Incorporated as P1.

### 3.10 Per-agent provider override testing (test-architect, their 2.1)

`AgentConfig` supports per-agent `provider`, `agent_model`, and `timeout` overrides. Mixed-provider deliberations are in the config schema, so users will try them. I did not mention this. Incorporated as P1.

### 3.11 Cancellation testing (test-architect, their 2.7)

For long-running multi-round deliberations, mid-pipeline cancellation with partial output preservation is a real user action. I did not address it. Incorporated as P2.

### 3.12 Intermediate phase output access (engine-implementor, their R8)

The deepeval quality tests for phase-level metrics require access to intermediate artifacts not exposed in `DecideResult`. The spec must specify whether quality tests call `run_pipeline` directly or read from the persisted deliberation directory. Incorporated as a must-fix for the quality test section.

### 3.13 LLM judge model specification (engine-implementor, their R10)

deepeval defaults to GPT-4 as judge. If the project wants Anthropic models as judges, this must be configured explicitly. The spec should state which model to use. Incorporated as a should-fix.

---

## 4. What I modify

### 4.1 Paid tier testing: narrow from "placeholder sections" to "three concrete tests" (original section 4)

I withdraw the HTTP surface placeholder and the Cowork/claude.ai entries. But I maintain that three specific paid-tier-adjacent tests belong in the engine eval suite because they test existing engine code, not hypothetical features:

1. **PAID_TIER_REQUIRED error test**: `conversus_score` and other paid-tier tools exist in the codebase and return structured errors when `conversus-solvers` is not installed. This is engine behavior that happens today when a free-tier user calls the wrong tool. Test that the error is structured and actionable, not a crash.

2. **Persistence round-trip test**: `persist_deliberation()` and `list_deliberations()` exist in `engine/persistence.py` and are called by `engine/handlers.py` today. This is not a future feature. Test the round-trip: persist, list, show.

3. **Cost telemetry population**: `ExecutionResult.cost` is populated by providers today. The paid tier will use this for billing, but it is also consumer-facing information (users see cost estimates). Test that for providers that support cost reporting, the cost field is populated.

These are not paid-tier tests. They are tests of existing engine features that the paid tier will depend on. The distinction matters.

### 4.2 Combinatorial smoke matrix: reduce from P3 to P2 and scope to 6 combinations (original section 2.2)

Both cross-reviews support combinatorial testing in principle. The test-architect's mode x surface matrix and mode x provider matrix expose the sparse coverage. I modify my original P3 recommendation to P2 and reduce the matrix from "8-12 combinations" to 6 targeted combinations that cover the most common consumer configurations:

1. anthropic + cooperative + json (the default CI pipeline)
2. anthropic + red-blue + json (the most common non-default mode)
3. mock + cooperative + rich (developer testing)
4. Settings cascade: env var provider + CLI mode override (Desktop user config)
5. Target documents + preset agents (full config-based deliberation)
6. Per-agent provider override: agent A mock + agent B mock with different models (heterogeneous deliberation, per test-architect)

### 4.3 Claude Code session detection: maintain but add the test-architect's framing (original 3.2 item 2)

The test-architect calls this finding "something I missed entirely." The engine-implementor does not dispute it. I maintain the recommendation but adopt the test-architect's placement at P2. The test is simple: set `CLAUDECODE=1`, run CLI, verify `InvocationContext.is_claude_code_session` is True and renderer is not `tui`. Low effort, catches a real failure mode.

### 4.4 Promptfoo shell quoting: align with engine-implementor's fix (original 6.1)

Both the engine-implementor and I caught this independently. The engine-implementor proposes a wrapper script; I proposed a test with quotes in the question. Both are needed: the wrapper script fixes the vulnerability, the quote-containing test verifies the fix. I modify to recommend both.

### 4.5 Quality threshold calibration: maintain with test-architect's endorsement (original 6.3)

The test-architect says my calibration approach is "more actionable" than their own. The engine-implementor agrees. I maintain the recommendation: run the quality suite once with anthropic provider, use the resulting scores as baseline, set thresholds at baseline minus a regression margin (e.g., 0.1). Do not guess thresholds a priori.

---

## 5. Revised priority list

Incorporating findings from all three reviews, here is the consumer advocate's revised priority list. Items marked with their source.

### P0 (must fix before implementation)

1. **Fix mock provider to return parseable synthesis** -- test-architect finding, I missed. Without this, the smoke tier is meaningless.
2. **Add multi-round pipeline tests** (rounds > 1, stagnation detection, termination reasons) -- test-architect finding, I missed.
3. **Fix `quality_indicators` schema** to match actual `QualityIndicators` Pydantic model -- engine-implementor finding, I missed.
4. **Scope step 3** to exclude red-blue for the first eval run -- engine-implementor finding, I missed.
5. **Test all 5 settings cascade levels including env vars** -- my original finding, upgraded from P0 to confirmed P0 by both reviewers.
6. **Test adhoc red-blue end-to-end through `parse_config`** -- all three reviews agree (G1).

### P1 (must fix before the paid tier)

7. **Add SDK surface** (`engine.sdk.Deliberation`) to cross-surface parity tests -- my original P0, downgraded to P1 per test-architect's reasoning.
8. **Move SKILL.md parity test** to step 4-5 in implementation order -- my original finding, both reviewers agree.
9. **Add CI/CD governance exit code tests** (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE) -- my original finding, both reviewers missed.
10. **Add arbiter and iteration pipeline tests** -- test-architect finding, I missed.
11. **Address Desktop Extension code divergence** (two engine copies, two result type hierarchies) -- test-architect finding, I missed.
12. **Add JSON error output consistency test**: `--format json` produces JSON on error paths, not plain text -- my original finding, both reviewers agree.
13. **Correct G3 description** and add G11: dual provider resolution path is the root cause -- engine-implementor finding, I missed.
14. **Specify intermediate artifact access** for deepeval quality tests -- engine-implementor finding, I missed.
15. **Add Pydantic schema snapshot tests** for result type stability -- test-architect finding, I missed.
16. **Add per-agent provider override tests** (heterogeneous deliberation) -- test-architect finding, I missed.
17. **Fix VALID_PROVIDERS** to match the execution registry or test the discrepancy -- test-architect finding, I missed.
18. **Test Desktop Extension content scanner** for all 7 MCP prompts -- my original finding, both reviewers endorsed.
19. **Test the 4 extended modes** for clear error-or-success semantics -- my original finding, both reviewers agree.
20. **Add persistence round-trip tests** (persist, list, show) -- my original finding, both reviewers agree.
21. **Add PAID_TIER_REQUIRED structured error test** -- my original finding, narrowed from placeholder section.

### P2 (before declaring the suite complete)

22. **Add combinatorial smoke matrix** (6 cross-axis combinations per section 4.2 above) -- my original finding, scoped down.
23. **Calibrate deepeval thresholds from baselines** -- my original finding, both reviewers endorse my approach.
24. **Add cancellation tests** (mid-pipeline, partial output) -- test-architect finding, I missed.
25. **Add Claude Code session detection test** -- my original finding, both reviewers agree.
26. **Add no-TTY login error test** for headless CI -- my original finding, test-architect endorsed.
27. **Test env var type coercion edge cases** (`CONVERSUS_MAX_LAUNCHES=abc`) -- my original finding, both reviewers agree.
28. **Fix promptfoo shell quoting** (wrapper script + quote-in-question test) -- both implementor and I caught this.
29. **Specify LLM judge model** for deepeval -- engine-implementor finding.
30. **Add cost telemetry population test** for providers that support it -- my original finding, narrowed.

---

## 6. What this revision reflects

My original review was strong on consumer surface coverage and weak on engine internals. The test-architect exposed three critical gaps I missed entirely: mock provider parse failures, multi-round pipeline complexity, and arbitration. The engine-implementor exposed two factual errors: the `quality_indicators` schema and the first eval run sequencing. Both reviewers correctly identified that about 30% of my recommendations (bundle tests, platform tests, future consumer placeholders, tool count limits) belong in other specs.

The revised position drops five recommendations, downgrades one priority, strengthens four findings, accepts thirteen findings from the other reviewers, and modifies five recommendations to incorporate cross-review feedback. The net result is a priority list that covers both the consumer surface concerns (my strength) and the engine-internal complexity (the test-architect's strength) while respecting the eval suite's scope boundary (the engine-implementor's correction).

The union of all three reviews is significantly stronger than any individual review. The spec has clear marching orders.
