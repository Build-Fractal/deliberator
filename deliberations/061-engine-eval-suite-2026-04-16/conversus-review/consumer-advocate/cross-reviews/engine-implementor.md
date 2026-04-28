# Cross-Review: Engine Implementor's Review of Spec 061

**Cross-reviewer**: Consumer advocate
**Reviewing**: Engine implementor's review (`engine-implementor/review.md`)
**Date**: 2026-04-16

---

## Overall Assessment

The engine-implementor review is the strongest of the three on codebase-level precision. It caught issues I did not catch, particularly around the dual provider-resolution paths and the implementation sequencing problem with the first eval run. However, it is narrowly scoped to "can I build this?" and does not adequately represent the consumer-facing consequences of the bugs it identifies. Several of its "should fix" items deserve higher severity when viewed through the consumer lens.

---

## Where I Agree

### 1. The dual provider-resolution path is a real bug (proposed G11)

The engine-implementor's most important finding is the divergence between `auth.py:resolve_provider()` (used by MCP handlers) and `run.py:resolve_execution_provider()` (used by CLI). I missed this entirely in my initial review. I flagged the *symptoms* -- 9 providers unwired, consumer confusion when switching surfaces -- but did not trace it to the root cause: two separate resolution codepaths that accept different provider sets.

This is a consumer-critical bug, not just an implementation detail. A user who gets `conversus decide "Q" --provider ollama` working via CLI will then try the MCP tool from Claude Desktop and hit an "Unknown provider" error because `run_decide_mcp` calls `resolve_provider` instead of `resolve_execution_provider`. The cross-surface parity test (3.3.3) would discover this, but only if it tests a provider beyond mock/anthropic/openai. I agree this should be listed as G11 and elevated to P1.

### 2. The first eval run sequencing problem (R6)

The engine-implementor correctly identifies that step 3 ("Run first eval -- capture current pass/fail state") will crash on red-blue with a ConfigError, producing infrastructure noise rather than useful baseline data. I did not call this out specifically. The recommendation to scope the first run to cooperative, winner-take-all, and prisoners-dilemma with mock provider only is practical and correct.

### 3. G3 description is imprecise (R5)

The engine-implementor's correction is precise: the 9 providers ARE wired as ExecutionProviders in the registry; they are NOT wired through `auth.py:resolve_provider()`. The fix target is `handlers.py` (to call `resolve_execution_provider` instead of `resolve_provider`), not adding 9 providers to `OAUTH_CONFIGS`. My review flagged the consumer impact but used the spec's imprecise framing. The engine-implementor's framing is more actionable.

### 4. The quality_indicators schema error (R2)

The engine-implementor caught that `quality_indicators` in the spec is shown as a string array but is actually a `QualityIndicators` Pydantic object with integer fields. I noted that "CLI JSON output fields must be a strict subset of the MCP DecideResult.output fields" but did not verify the actual field types. The engine-implementor did the homework. This is a must-fix because any consumer parsing this field as an array will crash.

### 5. Settings cascade isolation for tests (R9)

The engine-implementor flagged that `load_settings()` reads from `~/.conversus/settings.yml` and `<project>/.conversus/settings.yml`, and if either exists on the dev machine or CI runner, mock provider defaults get overridden. This is an important implementation detail I did not cover. My review focused on testing all 5 cascade levels; the engine-implementor focused on ensuring tests are hermetic. Both are needed.

### 6. The promptfoo shell-quoting problem (R3)

We both caught this. The engine-implementor goes further with a concrete solution: use a wrapper script that reads stdin or a temp file instead of inline shell expansion. I only flagged the problem and suggested either documenting the constraint or adding a test. The engine-implementor's solution is more practical.

### 7. Intermediate artifact access for quality tests (R8)

The engine-implementor correctly identifies that `run_decide_mcp` returns only the final synthesis, not intermediate phase outputs, and proposes either calling `run_pipeline` directly or reading from the persisted deliberation directory. My review did not address this access pattern, which means the phase-level quality tests I endorsed (review independence, cross-review adversarial quality, etc.) cannot actually be implemented as written. This is a real gap.

---

## Where I Disagree

### 1. Severity of R4 (CLI flag name verification) -- overstated as "Must fix"

The engine-implementor lists "Verify the actual CLI flag name for JSON format (`--format` vs `--output-format`)" as a must-fix. This is a lookup, not a design issue. The spec uses `--format json` throughout; if the actual flag is `--output-format`, the promptfoo config needs a string replacement. Marking this "Must fix" alongside genuine design problems like R1 (red-blue adhoc path) and R3 (shell injection) dilutes the severity signal. This is a "verify before implementing" note, not a spec revision.

### 2. The `conversus status` command question (section 3.1.3) -- understated

The engine-implementor notes "I did not find `conversus status` in the CLI module" and marks it as "Required change: Verify exists or remove." From the consumer perspective this matters more than a simple verification. If `conversus status` does not exist, the spec is specifying tests for a nonexistent feature. That is not a "verify" -- it is either a spec error (remove the test) or a feature gap (the command should exist because consumers need a quick health check). My review did not catch this either. The engine-implementor found it but underweighted its significance.

### 3. The deepeval judge model choice (R10) -- I would deprioritize

The engine-implementor asks the spec to specify the LLM judge model for deepeval (GPT-4 vs Anthropic). From the consumer perspective, the judge model is an implementation detail that does not affect whether the eval suite catches the bugs consumers hit. The eval suite should use whatever model produces the most reliable quality scores. Specifying the judge model in the spec over-constrains the implementation. I would drop this to "nice to have" or handle it in the eval harness configuration, not the spec.

### 4. Missing emphasis on the `_run_in_process` path (missing item #4)

The engine-implementor's "Missing from the Spec" item #4 identifies that `_run_in_process` in `handlers.py` also calls `resolve_provider` (not `resolve_execution_provider`), creating the same provider resolution bug surface as the main MCP handler. This is important but the engine-implementor buries it in a "missing" section. From the consumer perspective, the in-process execution path is the one that matters most for MCP consumers (it avoids subprocess overhead). If this path cannot resolve 9 of 13 providers, the MCP surface is fundamentally broken for those providers. This should be elevated to the G11 discussion, not listed as a separate missing item.

---

## What They Caught That I Missed

### 1. The `run_decide_mcp` mock provider default is treated as "not explicitly set"

The engine-implementor identified that `handlers.py` line 105-107 treats `provider="mock"` as "not explicitly set" (`provider if provider != "mock" else None`), meaning the settings cascade can override it. This means MCP tests that pass `provider="mock"` may silently use a different provider if the test environment has settings files. I missed this entirely, and it undermines every MCP test in the spec that relies on mock provider.

### 2. The `--format` vs `--output-format` flag name discrepancy

I did not verify the actual CLI flag name. The engine-implementor's instinct to check was correct.

### 3. conftest.py fixture reuse

The engine-implementor notes that the existing `engine/tests/conftest.py` has shared fixtures and the eval suite should integrate with them rather than creating parallel infrastructure. This is a practical implementation concern that I, as consumer advocate, would not typically catch, but it affects eval suite maintainability which ultimately affects consumers (an unmaintained eval suite stops catching bugs).

### 4. CI runner requirements

Python 3.12, Node.js 18 for promptfoo, API key secrets -- the engine-implementor correctly identifies that the spec says "eval suite runs in CI" without specifying the runner environment. My review did not address CI infrastructure at all.

---

## What I Caught That They Missed

### 1. The SDK surface (`engine.sdk.Deliberation`) is entirely absent

The engine-implementor does not mention the SDK at all. The test-architect caught it (section 2.8 of their review), and I elevated it to P0. The SDK is the primary programmatic surface for CI/CD pipelines and Python library consumers. Its absence from the eval suite means the most automation-friendly consumer surface has zero cross-surface parity coverage. The engine-implementor's review is CLI-and-MCP-centric; the SDK is a third surface with different types (`engine.sdk.Result` vs `engine.results.DecideResult`) that needs explicit coverage.

### 2. The env var cascade level is undertested

My review (section 2.3) identifies that the spec's settings cascade test describes 5 levels but does not specify testing the env var level. The env var layer is how Claude Desktop Extension users configure their provider (via `user_config` in manifest.json setting `CONVERSUS_DEFAULT_PROVIDER`). The engine-implementor acknowledges cascade isolation (R9) but does not call out the missing env var level specifically.

### 3. Desktop Extension content scanner rejection

My review (section 3.1, item 1) identifies that the Desktop Extension has a prompt-content scanner that can reject prompts with instructional directives. The engine uses a "role-split pattern" in `design_deliberation()` and `analyze_documents()` to work around this. The eval suite should test that all 7 MCP prompts pass the content scanner. The engine-implementor does not mention prompts at all -- their MCP surface analysis focuses exclusively on tools.

### 4. Paid tier groundwork

My review (section 4) covers HTTP surface shape, `PAID_TIER_REQUIRED` error handling, persistence round-trips, and cost telemetry. The engine-implementor mentions none of these. Their review is focused on making the current eval suite implementable, which is appropriate for their role, but the spec explicitly positions the eval suite as "the foundation for the paid tier" (section 1.1). The eval suite should lay groundwork for paid tier testing even if it does not implement it yet.

### 5. Extended mode behavior (negotiation, resource-allocation, fair-division, mechanism-design)

My review (section 1.2) calls out that the Desktop Extension manifest advertises 8 modes while the CLI accepts 4, and demands that the eval suite specify what happens when a user tries an extended mode via `decide`. The engine-implementor notes the 4+4 split (section 3.1.1) but accepts the spec's "(if supported in decide)" hedge without pushing for a concrete test. From the consumer perspective, "if supported" is not a valid test specification -- the eval suite's job is to determine what is supported and make the unsupported case produce a clear error.

### 6. Consumer-specific failure modes (Cowork, claude.ai, Cursor tool limits)

My review covers Cowork HTTP+OAuth transport, claude.ai web skills SKILL.md validation, and Cursor's 40-tool limit. The engine-implementor does not mention any of these. Some are P2/P3 and reasonably deferred, but the Cursor tool-count assertion is a concrete, cheap test that prevents a real deployment failure.

### 7. Sensitive field handling and platform compatibility

My review (section 3.1, items 3-4) covers `ANTHROPIC_API_KEY` not appearing in logs and darwin-only compatibility for the Desktop Extension. The engine-implementor does not address security or platform concerns.

### 8. Governance exit codes for CI/CD

My review (section 3.3, item 1) identifies that CI/CD pipelines need governance exit codes (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE). The engine-implementor mentions exit code handling in the context of promptfoo (non-zero exits treated as failures) but does not address the governance exit code scheme as a consumer-facing contract.

### 9. The `.mcpb` bundle build test

My review (section 5.3) identifies that the Desktop Extension ships as a `.mcpb` bundle and the eval suite should verify the bundle can be built and contains all required files. The engine-implementor does not mention distribution artifacts.

---

## Synthesis: Combined Priority List

Taking both reviews together, the combined priority order should be:

| Priority | Item | Source |
|---|---|---|
| P0 | Red-blue tests must use pre-built YAML, not adhoc path (R1) | Engine-implementor |
| P0 | Fix quality_indicators schema to match actual Pydantic model (R2) | Engine-implementor |
| P0 | Add SDK surface to cross-surface parity tests | Consumer advocate |
| P0 | Scope first eval run to exclude red-blue (R6) | Engine-implementor |
| P0 | Test all 5 settings cascade levels including env vars | Consumer advocate |
| P0 | Specify SKILL.md divergence test concretely, move earlier in order | Consumer advocate |
| P1 | Add G11: dual provider-resolution path divergence | Engine-implementor (proposed), consumer advocate (endorsed) |
| P1 | Replace inline shell expansion with wrapper script (R3) | Engine-implementor |
| P1 | Specify intermediate artifact access for quality tests (R8) | Engine-implementor |
| P1 | Correct G3 description to distinguish auth vs execution resolution (R5) | Engine-implementor |
| P1 | Add CI/CD-specific tests: governance exit codes, no-TTY, stderr, JSON errors | Consumer advocate |
| P1 | Test extended modes for clear error or valid output | Consumer advocate |
| P1 | Note settings cascade isolation in MCP tests (R9) | Engine-implementor |
| P2 | Add CI runner requirements (R12) | Engine-implementor |
| P2 | Specify LLM judge model (R10) | Engine-implementor (I would deprioritize to P3) |
| P2 | Paid tier placeholder tests | Consumer advocate |
| P2 | Desktop Extension content scanner, sensitive fields, platform tests | Consumer advocate |
| P2 | Verify `conversus status` exists or remove from test list | Engine-implementor |
| P3 | Cursor tool-count assertion, Cowork transport notes | Consumer advocate |
| P3 | `.mcpb` bundle build test | Consumer advocate |

---

## Final Assessment

The engine-implementor's review is essential reading for anyone implementing this spec. It is the only review that traced bugs to specific line numbers and verified claims against the actual codebase. The proposed G11 (dual provider-resolution paths) is the single most important finding across all three reviews because it explains why the same provider works on one surface and fails on another -- exactly the cross-surface parity failure that the eval suite is supposed to catch.

Where the engine-implementor's review falls short is in consumer breadth. It treats the eval suite as a tool for engine developers, not as a quality contract for consumers. The SDK surface, the paid tier, Desktop-specific failure modes, and CI/CD exit code semantics are all consumer-facing concerns that the engine-implementor does not address. The combined reviews cover the full picture: the engine-implementor provides the "how to build it" precision, and the consumer advocate provides the "what to build" scope.

The two reviews are complementary with no real conflicts. The few disagreements (R4 severity, R10 priority) are minor prioritization differences, not substantive disagreements about what the spec needs.
