# Cross-Review: Consumer Advocate's Review of Spec 061

**Cross-reviewer**: Test architect
**Reviewing**: Consumer advocate's review
**Date**: 2026-04-16

---

## 1. Where I agree

### 1.1 SDK surface is a genuine P0 gap

The consumer advocate correctly flags the complete absence of `engine.sdk.Deliberation` from the eval suite (their section 1.4). I raised the same issue (my section 2.8) and we independently arrived at the same conclusion: the SDK returns `engine.sdk.Result` with different fields than the MCP `DecideResult`, making the spec's "structurally identical output" claim meaningless without including the SDK in cross-surface parity tests. Agreement is strong here -- this is a real gap, not a theoretical one.

### 1.2 The 8-mode ambiguity is consumer-hostile

Their section 1.2 nails this. The Desktop Extension manifest advertises 8 modes, the CLI accepts 4, and the spec marks 4 as "(if supported)." I raised the same concern (my section 3.1) but the consumer advocate frames it better: from the consumer's perspective, "if supported" is not a test plan, it is an admission that nobody has checked. Their proposed fix -- test each extended mode for either a clear error message or valid output -- is exactly right. The additional suggestion that `decide`'s error message should reference `run` as an alternative for config-only modes is a nice consumer-facing detail I did not think to specify.

### 1.3 Settings cascade env var layer is undertested

Their section 2.3 identifies that the env var layer (`CONVERSUS_DEFAULT_PROVIDER`) is how Desktop Extension users configure their provider, and the spec's cascade test omits it. I raised the cascade incompleteness more broadly (my section 3.4 -- each setting key at each cascade level), but the consumer advocate correctly identifies the *highest-impact* missing level. Agree fully.

### 1.4 Quality thresholds need calibration

Both reviews flag the 0.6-0.8 thresholds as arbitrary (my section 4.3, their section 6.3). The consumer advocate proposes a specific calibration method: run once, use scores as baseline, set thresholds at baseline minus a regression margin. This is a more actionable recommendation than my "run once and observe the distribution" suggestion. I would adopt their framing.

### 1.5 SKILL.md divergence should be earlier in implementation order

Their section 6.4 argues G10 should move from step 9 to step 4-5. I agree -- my review flags the SKILL.md observation as deserving a test dimension (my section 1, final paragraph) but I did not comment on implementation ordering. The consumer advocate is right that a divergence affecting every Claude Code Skill user today should not be deferred to last.

### 1.6 CI/CD exit code semantics

Their section 3.3 identifies governance exit codes (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE) as untested. I did not call this out explicitly. This is a real gap for CI/CD consumers using conversus as a quality gate -- the exit code is the entire interface. Agree this belongs at P1.

---

## 2. Where I disagree

### 2.1 SDK surface is P0; I would call it P1

The consumer advocate rates the SDK surface as P0. I rated it P2 (my recommendation 12). The rationale for my lower priority: the SDK is a programmatic wrapper around the same engine internals that CLI and MCP exercise. If CLI and MCP tests pass, the SDK is unlikely to have *engine-level* bugs -- the risk is schema divergence in the SDK's own `Result` type, which is a real but narrower problem than, say, the mock provider producing unparseable output (which breaks the entire smoke tier). I would place SDK parity at P1, between the consumer advocate's P0 and my original P2, because it is important but not blocking the eval suite's ability to catch engine regressions.

### 2.2 Paid tier placeholder tests are premature

Their section 4 spends significant space on paid tier considerations: HTTP surface shape, `PAID_TIER_REQUIRED` error tests, cost telemetry, persistence for billing. I understand the consumer-facing motivation, but the spec is titled "Engine Eval Suite" and the paid tier does not exist yet. Testing a `PAID_TIER_REQUIRED` error return is testing distribution packaging, not engine correctness. Cost telemetry is a provider-level concern. I would not add these to the eval suite spec -- they belong in the paid tier's own spec. The consumer advocate is right to flag persistence round-trip testing (I also flagged it at my section 2.6), but the paid tier framing adds unnecessary scope to an already large spec.

### 2.3 Cowork HTTP transport and .mcpb bundle tests are out of scope

Their sections 3.5 and 5.3 propose testing Cowork's HTTP+OAuth MCP transport and the `.mcpb` bundle build process. These are distribution and packaging concerns, not engine eval concerns. The engine eval suite should validate that the engine produces correct results through its defined surfaces (CLI, MCP handlers, SDK). How those surfaces are transported (stdio vs HTTP) and packaged (.mcpb vs pip) is a separate testing domain. Including them here dilutes the eval suite's focus.

### 2.4 MCP tool count assertion for Cursor is a documentation concern, not a test

Their section 5.1 suggests asserting that the MCP tool count stays under Cursor's 40-tool limit. While this is useful consumer knowledge, it is a static property of the server definition, not a behavioral test. It belongs in a CI lint check on the MCP server module or in a compatibility matrix document, not in the engine eval suite.

---

## 3. What they caught that I missed

### 3.1 Desktop Extension content scanner rejection

Their section 3.1 item 1 is excellent: the Desktop Extension has a prompt-content scanner that can reject prompts with instructional directives. The `mcp_server.py` already uses a role-split pattern to work around this. I did not catch this at all. Testing that all 7 MCP prompts pass the content scanner is a legitimate eval concern -- if a prompt format change breaks the scanner workaround, Desktop users see failures.

### 3.2 Claude Code session detection env vars

Their section 3.2 item 2 identifies that `CLAUDECODE`, `CLAUDE_CODE`, `CLAUDE_CODE_ACTIVE` env vars trigger session detection in `engine/cli/context.py`, changing renderer and provider defaults. I missed this entirely. It is a straightforward test (set env var, check `InvocationContext.is_claude_code_session`) and catches a real failure mode: if session detection breaks, Claude Code users get the TUI renderer instead of the appropriate non-interactive renderer.

### 3.3 CI no-TTY login behavior

Their section 3.3 item 2 flags that `conversus login` in a headless CI environment (no TTY) might hang waiting for OAuth browser input instead of producing a clear error. I did not test auth lifecycle in enough detail -- my section 6.3 mentions login but does not cover the headless/non-interactive case specifically. This is a real CI/CD failure mode.

### 3.4 JSON error output consistency

Their section 3.3 item 4 asks whether `--format json` produces JSON even on error paths, or falls back to plain text. This is a critical CI/CD concern that I did not address. A pipeline parsing `conversus decide ... --format json | jq .headline` will break if the error path emits plain text instead of a JSON error object.

### 3.5 env var type coercion edge cases

Their section 2.4 identifies that `CONVERSUS_MAX_LAUNCHES=abc` should fail gracefully. I did not test env var parsing edge cases at all. The code in `engine/settings.py` handles this, but unvalidated env var parsing is a common source of production bugs.

### 3.6 Promptfoo shell quoting vulnerability

Their section 6.1 catches a shell injection/quoting issue in the promptfoo exec provider template: `{{prompt}}` containing double quotes will break the shell command. I missed this entirely. It affects eval suite reliability, not engine correctness, but a flaky eval suite is almost as bad as no eval suite.

---

## 4. What I caught that they missed

### 4.1 Multi-round pipeline testing (my most critical finding)

My section 2.2 identifies that `rounds > 1` is entirely untested. The `phases.py` orchestrator implements round loops with stagnation detection, cross-round synthesis, and inter-round arbitration. These are the highest-complexity code paths in the engine. The consumer advocate does not mention multi-round deliberation at all. This is a significant omission -- multi-round is not an exotic feature, it is a core pipeline capability that directly affects output quality. A consumer running `rounds: 3` in their config gets untested code paths.

### 4.2 Arbiter interaction testing

My section 2.3 covers the arbiter phase (conditional Phase 6) with its trigger conditions, influence levels, and timing options. The consumer advocate does not mention arbitration. For consumers using full config-based deliberations with `arbiter.trigger: disputes_remain`, this is a critical untested path.

### 4.3 Iteration loop testing

My section 2.4 identifies that `iterations: 3` is only tested as config validation, not as an actual pipeline execution test. The consumer advocate does not address this. The iteration loop around cross-review and revision is a core pipeline mechanism.

### 4.4 Mock provider masks real failures

My section 4.1 is arguably the single most important finding in either review: the mock provider returns canned text that does not contain the markdown headings `parse_synthesis` needs. The `from_events()` method catches parse failures with a bare `except` and falls back to empty strings. This means the entire smoke tier tests the fallback path, not the production path. The consumer advocate does not identify this issue. A smoke suite built on unparseable mock output will show green while the real pipeline remains broken. This is the highest-leverage fix in the spec.

### 4.5 Desktop Extension code divergence

My section 2.5 identifies that `desktop-extension/server/lib/engine/` is a separate copy of the engine with its own inline type definitions. The consumer advocate mentions the Desktop Extension but focuses on manifest-level concerns (mode count, content scanner). The code-level divergence -- two engine copies, two result type hierarchies, no parity test -- is a structural problem that the consumer advocate does not address.

### 4.6 Pydantic schema snapshot testing

My section 5.2 proposes snapshot tests for result type JSON schemas to catch breaking changes for MCP consumers. The consumer advocate discusses schema differences between surfaces (their section 1.3) but does not propose schema stability testing as a regression mechanism.

### 4.7 Per-agent provider override (heterogeneous deliberation)

My section 2.1 identifies that `AgentConfig` supports per-agent `provider`, `agent_model`, and `timeout` overrides, enabling mixed-provider deliberations. This is not exotic -- it is in the config schema. The consumer advocate does not mention it.

### 4.8 Cancellation testing

My section 2.7 covers `CancellationFlag` from `engine/cancel.py` -- mid-pipeline cancellation, partial output preservation. The consumer advocate does not address cancellation. For long-running multi-round deliberations, cancellation is a real user action.

### 4.9 VALID_PROVIDERS hardcoded to two

My section 6.1 identifies that `config.py` line 82 hardcodes `VALID_PROVIDERS = ("anthropic", "openai")`, meaning full YAML configs can only specify two providers despite 13+ being registered. The consumer advocate mentions provider counts in the context of instantiation but does not catch this config-level restriction.

---

## 5. Synthesis: combined priority list

Taking the best findings from both reviews, here is how I would re-prioritize:

### P0 (must fix before implementation)

1. **Fix mock provider to return parseable synthesis** (my finding, missed by consumer advocate). Without this, the smoke tier is meaningless.
2. **Add multi-round pipeline tests** (my finding, missed by consumer advocate). Highest-complexity untested code paths.
3. **Test adhoc red-blue end-to-end through parse_config** (both reviews agree this is P0 via G1).
4. **Define provider test levels** (my finding, complementary to their provider concerns).

### P1 (must fix before the paid tier)

5. **Add SDK surface to cross-surface parity** (both reviews; I concede P1 over my original P2, but not the consumer advocate's P0).
6. **Test all 8 modes explicitly** with clear error-or-success semantics (both reviews).
7. **Add settings cascade env var layer test** (consumer advocate's finding, well-argued).
8. **Move SKILL.md parity test earlier** in implementation order (consumer advocate's finding).
9. **Add CI/CD governance exit code tests** (consumer advocate's finding, I missed it).
10. **Add arbiter and iteration pipeline tests** (my finding, missed by consumer advocate).
11. **Address Desktop Extension code divergence** (my finding, missed by consumer advocate).
12. **Add JSON error output consistency test** for `--format json` on error paths (consumer advocate's finding).
13. **Add Pydantic schema snapshot tests** (my finding).
14. **Add per-agent provider override tests** (my finding).
15. **Fix VALID_PROVIDERS to match the execution registry** or test the discrepancy (my finding).

### P2 (before declaring the suite complete)

16. **Add combinatorial smoke matrix** (consumer advocate's finding, my section 3 also supports this).
17. **Add cancellation tests** (my finding).
18. **Add persistence round-trip tests** (both reviews).
19. **Calibrate deepeval thresholds from baselines** (both reviews; consumer advocate's framing is better).
20. **Add Claude Code session detection test** (consumer advocate's finding).
21. **Add Desktop content scanner prompt tests** (consumer advocate's finding).
22. **Add no-TTY login error test** (consumer advocate's finding).
23. **Test env var type coercion edge cases** (consumer advocate's finding).
24. **Fix promptfoo shell quoting** (consumer advocate's finding).

---

## 6. Overall assessment of the consumer advocate's review

The consumer advocate brings a valuable perspective that my review lacks: they think about real users hitting real configuration paths in real editor environments. Their findings on Desktop content scanner behavior, Claude Code session detection, CI/CD exit codes, and JSON error output consistency are all things I missed because I was focused on the test matrix's structural completeness rather than specific consumer journeys.

Their weaknesses are the inverse of their strengths: they focus heavily on distribution-layer concerns (Cowork HTTP transport, .mcpb bundles, Cursor tool limits, paid tier HTTP surface) that are out of scope for an engine eval suite, and they miss the engine's internal complexity (multi-round, arbitration, iteration loops, cancellation, mock provider parse failures). The engine eval suite's primary job is to validate that the engine produces correct results. Consumer-specific transport and packaging concerns are important but belong in separate test suites.

The most concerning gap in the consumer advocate's review is the absence of any mention of multi-round deliberation, arbitration, or the mock provider's unparseable output. These are the findings I consider most critical in my own review. A consumer advocate who validates that all surfaces return the right schema but misses that the pipeline's most complex code paths are untested is solving the wrong problem first.

That said, the consumer advocate's review and mine are strongly complementary. The union of both reviews covers significantly more ground than either alone. The combined priority list above reflects that.
