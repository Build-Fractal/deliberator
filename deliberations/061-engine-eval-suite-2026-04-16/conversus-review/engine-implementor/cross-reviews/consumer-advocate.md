# Engine Implementor Cross-Review of Consumer Advocate

**Cross-reviewer**: Engine implementor
**Reviewing**: Consumer advocate's review of Spec 061
**Date**: 2026-04-16

---

## Overall Assessment

The consumer advocate's review is the strongest complement to my own. Where I evaluated the spec against the engine's actual code paths and asked "can I build this test?", they evaluated it against the consumer surface area and asked "does this test protect real users?" Those are the two questions that matter, and the spec needs to satisfy both.

Their review is approximately 75% additive to mine. The overlapping 25% gives me confidence in convergence; the divergent 75% exposes blind spots I missed. I have a few technical disagreements, but they are minor relative to the valid concerns raised.

---

## Where I Agree

### 1. SDK surface is a critical omission (their 1.4, P0)

I completely missed this. The `engine.sdk.Deliberation` class is a first-class consumer surface, and I did not mention it once in my review. The consumer advocate is right that it must be in the cross-surface parity tests (3.3.3). My review focused on the divergence between `resolve_provider` (auth.py) and `resolve_execution_provider` (run.py), but the SDK has a *third* resolution path through `Deliberation.run()`. If we are testing cross-surface parity, omitting the SDK means we are only testing 2 of 3 programmatic surfaces.

I would add: the SDK is the most likely surface for CI/CD pipeline integration. A CI pipeline will `from engine import Deliberation` rather than shelling out to `conversus decide`. If the SDK path has different behavior from the CLI or MCP path (and given the provider resolution divergence I identified, it almost certainly does), CI users will hit bugs that the eval suite would not catch.

### 2. The 5-level settings cascade including env vars (their 2.3, P0)

I noted in my review (R9) that tests must isolate the settings cascade, but I framed it as a "should fix" concern about test hygiene. The consumer advocate correctly escalates this to P0 and identifies the specific reason: Desktop Extension users configure providers via `CONVERSUS_DEFAULT_PROVIDER` through `user_config` in the manifest. If the env var layer is not explicitly tested, the most common Desktop configuration path is untested.

They are right and I was wrong to rate this "should fix." It is a "must fix."

### 3. SKILL.md parity should be earlier in implementation order (their 6.4)

We both flagged G10 but the consumer advocate's reasoning for moving it earlier is sharper than mine. My review mentioned G10 as a known gap without disputing its placement at step 9. The consumer advocate points out that SKILL.md divergence is a P1 gap affecting real users *today*, and deferring it to step 9 of 10 means the most commonly used consumer surface (Claude Code Skill) remains broken for the entire implementation timeline. Moving it to step 4 or 5 is correct.

### 4. Governance exit codes for CI/CD (their 3.3, item 1)

I did not catch this at all. The engine has two exit code schemes (interactive and governance), and CI/CD pipelines acting as quality gates need the governance scheme (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE). The spec's CI/CD test in section 3.3.2 says "exit codes" generically but does not specify which scheme. This is exactly the kind of consumer-specific detail that the spec must be explicit about.

### 5. Promptfoo shell-quoting vulnerability (their 6.1, my R3)

We both caught the `{{prompt}}` shell injection risk in the promptfoo exec provider. This is reassuring convergence -- it means neither of us is hallucinating the problem. Their framing (include a test with quotes in the question) is a good addition to my recommendation (use a wrapper script). Both are needed: the wrapper script fixes the vulnerability, and the quote-containing test verifies the fix.

### 6. Quality threshold calibration (their 6.3)

The consumer advocate's recommendation to run the quality suite once, use resulting scores as baseline, and set thresholds at baseline minus a regression margin is more practical than the spec's approach of setting thresholds a priori. I noted in my review (section 3.2.2) that the 0.7 threshold for red-blue adversarial coverage is arbitrary and recommended starting at 0.5. Their approach is better: do not guess at all, measure first, then set thresholds relative to the measurement.

---

## Where I Disagree

### 1. MCP tool count assertion for Cursor's 40-tool limit (their 5.1, P2)

The consumer advocate recommends testing that conversus fits within Cursor's 40-tool limit. This is not an engine eval concern -- it is a distribution packaging concern. The conversus MCP server exposes 4 tools (validate, run, decide, login). The 40-tool limit applies to the total tools across *all* MCP servers a user has registered in Cursor. Conversus cannot test or control how many other MCP servers a Cursor user has installed. The right place for this is the distribution strategy or the Desktop Extension manifest documentation, not the engine eval suite.

### 2. .mcpb bundle build test (their 5.3, P2)

Testing that `desktop-extension/build.sh` produces a valid `.mcpb` bundle is a build/packaging test, not an engine eval test. The eval suite's scope (section 1) is "validate the engine across surfaces." The build artifact is upstream of the engine -- it packages the engine, it does not exercise it. This belongs in the Desktop Extension's own CI, not in Spec 061.

### 3. Platform compatibility test for non-darwin (their 3.1, item 4)

Testing that the extension works on non-darwin platforms when the manifest explicitly declares `"platforms": ["darwin"]` is testing a declared constraint, not an engine bug. The engine itself is platform-agnostic (Python, runs anywhere). The darwin restriction is a Desktop Extension packaging choice. If the eval suite adds a test "run on Linux, expect clear error," that test belongs in the Desktop Extension repo, not the engine eval suite.

### 4. Paid tier HTTP surface placeholder (their 4.1, P2)

The consumer advocate wants a placeholder test section for the HTTP API surface. I understand the forward-thinking motivation, but placeholder tests that do nothing are noise. They pass trivially, they do not catch regressions, and they create a false sense of coverage. The paid tier HTTP surface does not exist yet. When it exists, we will write tests for it. Adding "TODO: test HTTP surface" to the spec is fine as a note; adding a placeholder test section is premature.

### 5. Cowork and claude.ai as planned consumers (their 5.5, P2)

Similar reasoning. Documenting future consumers is useful for the product roadmap, not for the eval spec. The spec should test what exists. A note in section 1's consumer table saying "Cowork (planned, HTTP+OAuth MCP transport)" is sufficient. Adding test sections for consumers that do not exist yet dilutes the spec's focus.

---

## What They Caught That I Missed

### 1. SDK surface entirely absent

This is the most significant gap. I am embarrassed to have missed it. The `engine.sdk` module is a concrete, shipped, importable API. It is arguably the cleanest consumer surface because it bypasses both CLI argument parsing and MCP handler wrappers. If it is not in the parity tests, we are testing the wrappers but not the thing they wrap.

### 2. Governance exit codes

I mentioned exit codes only in the context of promptfoo's exec provider treating non-zero as failure. The consumer advocate identified the deeper issue: the engine has *two* exit code schemes, and CI/CD consumers need the governance scheme. This is a real consumer-facing behavior that the spec does not test.

### 3. Persistence round-trip tests

The consumer advocate notes that `persist_deliberation()` and `list_deliberations()` are not covered. I mentioned persistence only in the context of accessing intermediate phase outputs for quality tests (my section 3.2.1). They correctly identify that persistence is itself a testable contract, not just a data access mechanism.

### 4. Extension content scanner rejection

Desktop Extension prompts must pass the content scanner, and the MCP server already uses a role-split workaround. I did not consider this because I was focused on engine internals, but from the consumer perspective this is a real failure mode: a prompt that works in development fails after deployment because the content scanner rejects it.

### 5. The `claude-desktop` provider CLI fallback behavior

When `provider=claude-desktop` is used from CLI (no MCP context), the handler falls back to anthropic credentials. The consumer advocate correctly identifies this as a testable consumer behavior. I mentioned the handlers.py fallback logic (lines 182-194) in my review under G4 but did not specify a test for the fallback path.

### 6. `CONVERSUS_MAX_LAUNCHES=abc` type coercion edge case

Concrete and testable. Settings env var parsing with invalid types should fall through gracefully. I did not think about this because I was focused on the happy path of the settings cascade.

### 7. Consumer output schema mapping (CLI JSON vs MCP DecideResult)

I identified the structural divergence between the two surfaces (my section 3.3.3) but the consumer advocate's framing is sharper: a consumer *migrating* from CLI to MCP will encounter a schema change. The test they propose (CLI JSON fields must be a strict subset of MCP DecideResult.output fields) is a concrete assertion I should have specified.

---

## What I Caught That They Missed

### 1. The dual provider resolution path (resolve_provider vs resolve_execution_provider)

This is the most significant finding in my review that the consumer advocate's review does not surface. The engine has two different functions for resolving providers: `auth.py:resolve_provider()` (used by MCP handlers) and `run.py:resolve_execution_provider()` (used by CLI). They resolve different provider sets and have different fallback behavior. The consumer advocate correctly notes that "9 providers have execution classes but no auth wiring" (echoing the spec) but does not identify *why* -- the dual resolution path is the root cause, and the fix is in `handlers.py` (calling the right function), not in `auth.py` (adding providers to OAUTH_CONFIGS).

The consumer advocate's review treats the 9 unwired providers as a flat fact. My review traces the bug to its code-level root cause and identifies the correct fix target. This matters for the spec because the implementation order (step 5: "wire remaining providers into auth resolver") is misdirected if the fix is actually in `handlers.py`.

### 2. MCP test isolation: settings cascade override of mock default

I specified (R9) that every MCP test must either mock `load_settings` or run in a clean temp directory with `HOME` overridden, because the default provider "mock" is treated as "not explicitly set" and the settings cascade can override it. The consumer advocate discusses the settings cascade testing (their 2.3) but does not connect it to the test isolation problem: if your CI runner has a `~/.conversus/settings.yml` that sets `default_provider: anthropic`, then every test that passes `provider="mock"` will silently use anthropic instead.

### 3. `quality_indicators` schema is wrong (nested object, not string array)

I identified (R2) that the spec's JSON schema shows `quality_indicators` as `["<string>", ...]` but the actual `ConversusOutput` model has it as a `QualityIndicators` object with integer fields. The consumer advocate does not mention this. It is a concrete factual error in the spec that will cause the output schema test (3.1.6) to fail immediately.

### 4. Intermediate phase output access for quality tests

I identified (R8) that deepeval quality tests for phase-level metrics (review independence, cross-review adversarial quality) require access to intermediate artifacts that are not exposed in the `DecideResult` return value. The consumer advocate does not discuss how quality tests access the per-phase outputs. This is a structural blocker for section 3.2.1.

### 5. `conversus status` command may not exist

I flagged (section 3.1.3) that I could not find a `status` command in the CLI module. The consumer advocate does not question the CLI command list.

### 6. The `_run_in_process` handler path also uses `resolve_provider`

I identified a fourth code path (beyond CLI, MCP, and SDK) that uses the wrong provider resolution function: `handlers.py:_run_in_process()`. This is the same G3 bug surface but in a different code path. The consumer advocate does not catch this.

### 7. First eval run sequencing error (step 3)

I identified (R6) that the first eval run (implementation step 3) will crash on infrastructure failures (ConfigError for red-blue mode) rather than surfacing the engine bugs the spec intends to test. The consumer advocate praises the implementation order as "practical" and says "ship the eval harness first, then fix what it catches" without noting that the harness itself will fail to *run* for red-blue mode, producing an infrastructure error rather than a meaningful test failure.

---

## Reconciliation: What the Spec Should Do

Combining both reviews, the spec needs these changes in priority order:

1. **Add the SDK surface** to cross-surface parity tests (consumer advocate's finding, I agree)
2. **Fix the `quality_indicators` schema** (my R2, consumer advocate missed)
3. **Scope step 3** to exclude red-blue mode for the first eval run (my R6, consumer advocate missed)
4. **Add env var layer** explicitly to settings cascade tests (consumer advocate's 2.3, I agree and upgrade from my "should fix" to "must fix")
5. **Specify intermediate artifact access** for quality tests (my R8, consumer advocate missed)
6. **Move SKILL.md parity** to step 4-5 in implementation order (consumer advocate's 6.4, I agree)
7. **Add governance exit code tests** for CI/CD (consumer advocate's 3.3, I missed)
8. **Correct G3 description** to identify dual resolution path as root cause (my R5, consumer advocate missed)
9. **Use wrapper script** for promptfoo exec provider (both reviews agree)
10. **Specify LLM judge model** for deepeval (my R10, consumer advocate did not address)

Items from the consumer advocate's review that I recommend *not* adopting: .mcpb bundle build test, Cursor tool count assertion, non-darwin platform test, paid tier HTTP placeholder test section, Cowork/claude.ai placeholder consumer entries. These are valid concerns for their respective domains but are out of scope for the engine eval spec.

---

## Verdict on the Consumer Advocate's Review

**Strong review, correct priorities, occasionally over-scoped.** The consumer advocate's instinct to expand the eval suite to cover every consumer touchpoint is the right instinct for their role. The SDK omission alone justifies the review. The governance exit code finding and the settings cascade env var escalation are both concrete improvements that I missed.

The main weakness is scope creep: about 30% of their recommendations (bundle tests, platform tests, future consumer placeholders, tool count limits) belong in other specs or other repos. The engine eval suite should test the engine. Distribution, packaging, and platform compatibility are downstream concerns.

Net: their review makes the spec better. Combined with my review, the spec has clear marching orders.
