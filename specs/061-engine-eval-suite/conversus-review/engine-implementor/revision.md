# Engine Implementor — Revised Position

**Date**: 2026-04-16
**Phase**: 3 — Revision
**Input**: Cross-reviews from test-architect and consumer-advocate

---

## Preamble

Both cross-reviews were substantive and fair. The test-architect's review is the more technically consequential of the two — it identified a structural flaw in the smoke tier that I missed entirely. The consumer-advocate's review correctly identified my blind spot on consumer breadth. Neither reviewer manufactured disagreements, and their criticisms of my review are almost entirely warranted.

My original review asked: "Can I build the tests this spec describes?" The cross-reviews collectively asked the harder question: "Even if built, will the tests catch real bugs?" The answer to the second question exposed gaps that the answer to the first did not.

---

## What I Withdraw

### W-1: R4 severity — "Must fix" was wrong for the CLI flag name check

The consumer-advocate is right (their disagreement #1): listing "verify `--format` vs `--output-format`" as a must-fix alongside genuine design problems like shell injection and the red-blue adhoc path dilutes the severity signal. This is a lookup to perform at implementation time, not a spec revision. I withdraw R4 from the must-fix tier. It remains a pre-implementation checklist item.

**R4 moves from "Must fix" to "Verify before implementing" (no spec change needed).**

### W-2: R10 — specifying the LLM judge model in the spec

The consumer-advocate argues (their disagreement #3) that the judge model is an implementation detail that over-constrains the spec. On reflection, they are right. The spec should state that deepeval quality tests require an LLM judge and that the CI pipeline must provision API credentials for it. It should not prescribe GPT-4 vs Claude as the judge. The team implementing the eval harness should choose based on cost, reliability, and score consistency during the calibration run.

**R10 is withdrawn as a spec revision. Replaced by a lighter requirement: "Section 4.2 must note that the quality tier requires LLM judge API credentials and that the judge model should be selected during the calibration baseline run."**

### W-3: My framing of cancellation testing priority

In my cross-review of the test-architect, I placed cancellation tests at P3. Neither cross-reviewer of me pushed back on this, but on re-reading I realize the test-architect never asked for P0/P1 on cancellation either — they listed it as a missing dimension without priority. The consumer-advocate did not mention it. There is no disagreement to resolve here, but I want to explicitly note that I am comfortable with P3 for cancellation and do not need to revise.

**No change. Cancellation stays at P3. Noted for completeness.**

---

## What I Strengthen

### S-1: G11 — the dual provider-resolution path is a single bug with multiple call sites

The test-architect's cross-review (DC-1) correctly points out that I identified the `_run_in_process` call site as a separate "missing from the spec" item when it is actually the same bug as the `run_decide_mcp` call site. Both use `resolve_provider` from auth.py instead of `resolve_execution_provider` from run.py. The consumer-advocate's cross-review independently endorses G11 and elevates it to P1.

I strengthen my original position: G11 should name both `run_decide_mcp` (handlers.py ~line 197) and `_run_in_process` (handlers.py ~line 491) as affected call sites, with a single fix: replace all `resolve_provider` calls in handlers.py with `resolve_execution_provider`. This is not two observations — it is one bug with two manifestations. The test-architect's framing is cleaner than mine.

**G11 consolidated: single gap entry naming both call sites, single fix target (handlers.py), P1 severity. This is stronger than my original position which split it across two sections.**

### S-2: The `quality_indicators` schema error is even more consequential than I stated

Both cross-reviewers agree this is a must-fix (test-architect's DC-3 and consumer-advocate's agreement #4). The test-architect adds that they accepted the spec's schema without verifying it against the Pydantic model — meaning my codebase verification was the only review that caught a factual error in the spec. The consumer-advocate adds the consumer angle: "any consumer parsing this field as an array will crash."

I strengthen R2: the schema error is not just wrong, it is actively dangerous because the output schema test (3.1.6) would be written against the wrong schema, producing a test that passes with incorrect assertions. A test that validates the wrong schema is worse than no test — it creates false confidence.

**R2 severity upgraded from "Must fix" to "Must fix — blocks correctness of output schema test (3.1.6)." No change to the recommendation itself, but the rationale is stronger.**

### S-3: First eval run scoping (R6) — the test-architect's xfail resolution is the right answer

The test-architect (T-1) resolves the tension between my R6 ("exclude red-blue from the first promptfoo run") and their own P0 item 3 ("the red-blue regression test must exist from day one"). Their resolution: the promptfoo first run excludes red-blue (my R6), but a pytest functional test marked `xfail` calls `parse_config` on adhoc-generated red-blue config and documents the expected ConfigError. The `xfail` test flips to pass when G1 is fixed, providing the regression gate without polluting the first baseline with infrastructure noise.

I adopt this resolution. It is better than my original position (which only said "exclude red-blue") because it preserves the regression test while keeping the baseline clean.

**R6 revised: exclude red-blue from promptfoo first run AND add a pytest xfail test for adhoc red-blue parse_config. This is a synthesis of my R6 and the test-architect's P0 item 3.**

### S-4: Settings cascade isolation must be P0, not "should fix"

The consumer-advocate's cross-review (agreement #5) and the test-architect's cross-review (T-3) both address my R9. The consumer-advocate explicitly endorses it. The test-architect frames the same concern from the opposite direction: I asked "how do we prevent the cascade from polluting tests?" while they asked "where are the tests that verify the cascade itself works?" Both are needed.

More importantly, the consumer-advocate's original review identified that the env var layer (`CONVERSUS_DEFAULT_PROVIDER`) is the primary configuration path for Desktop Extension users, which I did not mention. My R9 focused on test hygiene; the consumer-advocate correctly connects it to a specific consumer population.

I strengthen R9 from "should fix" to "must fix" and expand scope: the spec must require (a) a `clean_settings` conftest fixture that isolates HOME and project-level settings, and (b) explicit test cases for each cascade level including env vars.

**R9 upgraded from "Should fix" to "Must fix." Scope expanded to include cascade level test cases, not just isolation fixtures.**

### S-5: The promptfoo shell-quoting fix (R3) needs the consumer-advocate's test case too

My original R3 recommended a wrapper script. The consumer-advocate independently recommended the same fix and added: include a test with quotes in the question to verify the fix. Both the fix and the verification are needed.

**R3 expanded: wrapper script (my recommendation) + a promptfoo test case with shell metacharacters in the question (consumer-advocate's recommendation).**

---

## What I Modify

### M-1: My treatment of the SDK surface — from absent to required

This is the most significant revision. Both cross-reviewers called me out for not mentioning the SDK at all:

- The test-architect (section "What I Caught That They Missed", item 7) notes the SDK has different result types (`engine.sdk.Result` vs `engine.results.DecideResult`) and is excluded from the parity test.
- The consumer-advocate (disagreement #1, and "What I Caught That They Missed", item 1) calls the SDK the "primary programmatic surface for CI/CD pipelines" and says its absence from the eval suite means "the most automation-friendly consumer surface has zero cross-surface parity coverage."

They are both right, and I was wrong to omit it. In my cross-review of the test-architect, I partially disagreed on framing — I said SDK parity should test inner content equivalence, not wrapper type identity. I still believe that framing is correct, but I was using it to soften the gap instead of addressing it head-on.

The SDK must be in the cross-surface parity test (3.3.3). The assertion should be: given the same question, provider, and mode, the `engine.sdk.Deliberation.run()` result's inner content (headline, summary, full_analysis, quality_indicators) must structurally match the MCP `DecideResult.output` content. The wrapper types will differ by design — that is fine. The content must not.

**New required change R13: Add the SDK surface to cross-surface parity tests (3.3.3). Assert inner content parity, not wrapper type identity. Priority: Must fix.**

### M-2: Mock provider synthesis path — adopting the test-architect's finding

The test-architect's most important finding (section 4.1 of their review, which I discussed at length in my cross-review of them) is that mock provider output does not contain the markdown headings that `parse_synthesis` expects, so `StructuredDeliberation.from_events()` catches the parse failure with a bare `except` and falls back to empty strings. This means every mock-based smoke test exercises the error-recovery path, not the production path.

I missed this entirely in my original review. I flagged G6 (mock headline template) as P3. The test-architect correctly identifies that G6 is not a cosmetic issue — it invalidates the smoke tier's claim to detect structural regressions. The consumer-advocate's cross-review does not mention this (they focus on consumer surfaces, not mock provider internals), but the test-architect's finding stands on its own.

I modify my position: either the mock provider must be enhanced to return synthesis-parseable output (a "realistic response mode"), or the spec must acknowledge that the smoke tier tests the fallback path and add a separate "realistic provider" tier that tests the production parsing path. The former is preferable because it makes the existing smoke tests meaningful without requiring additional infrastructure.

**New required change R14: The mock provider must return output that exercises the production synthesis parsing path, not the bare-except fallback. Either enhance mock provider or add a "realistic mock" mode. Priority: P0 — without this, the smoke tier has no structural regression value.**

### M-3: Multi-round pipeline tests — adopting the test-architect's finding

The test-architect identified (section 2.2 of their review) that `rounds > 1` is a high-complexity code path with zero dedicated eval tests. Stagnation detection, cross-round synthesis, inter-round arbitration, and termination reason reporting are the most intricate code paths in `phases.py`. My original review did not address this because I reviewed only what the spec proposes, not what it omits.

Both cross-reviewers are silent on multi-round — neither the test-architect's cross-review of me nor the consumer-advocate's cross-review of me mentions it. But I flagged it in my cross-review of the test-architect as a P0 gap, and I maintain that position here.

**New required change R15: Add multi-round pipeline tests to the functional tier. Minimum: rounds=2 with convergence, rounds=3 with stagnation detection. Assert on `termination_reason` field. Priority: P0.**

### M-4: Arbiter interaction tests — from unaddressed to P1

The test-architect identified (section 2.3) that arbitration is a conditional Phase 6 with trigger modes, influence levels, and timing variants, and that the spec covers arbiter only as a config parsing test. I agreed in my cross-review of the test-architect but noted that arbiter tests require a provider that produces genuine disputes — mock provider will not generate the structured disagreement markers that the dispute detection logic looks for.

With M-2 above (mock enhancement to realistic mode), the arbiter-fires path becomes testable with mock. But even without it, the "arbiter does not fire when no disputes exist" path is immediately testable and valuable.

**New required change R16: Add arbiter interaction tests. Minimum: trigger=disputes_remain with no disputes (arbiter should not fire), trigger=always (arbiter should always fire). Priority: P1.**

### M-5: `conversus status` — from "verify" to "remove or specify"

The test-architect's cross-review (DC-2) agrees with my flag but notes that I underweighted it. The consumer-advocate's cross-review (disagreement #2) says it more sharply: "If `conversus status` does not exist, the spec is specifying tests for a nonexistent feature. That is not a 'verify' — it is either a spec error (remove the test) or a feature gap (the command should exist because consumers need a quick health check)."

The consumer-advocate is right. The spec cannot list tests for a command that may not exist and mark it "verify." The spec author must decide: does this command exist? If yes, confirm the exact command name and surface. If no, remove it from 3.1.3 and optionally file a feature request.

**R-CLI (originally section 3.1.3 note) upgraded: the spec must confirm `conversus status` exists and specify its output contract, or remove it from the CLI surface tests. This is not a "verify before implementing" item — it is a spec correctness issue.**

### M-6: Intermediate artifact access (R8) — specify the concrete mechanism

My original R8 said quality tests need access to intermediate phase outputs and proposed two options: call `run_pipeline` directly or read from the persisted deliberation directory. The consumer-advocate's cross-review (agreement #7) endorses this and notes that without it, the phase-level quality tests in 3.2.1 "cannot actually be implemented as written."

I refine R8: the spec should specify `run_pipeline` as the execution function for quality tests (not `run_decide_mcp`), because `run_pipeline` returns `PipelineResult` which contains `output_dir` pointing to the directory with all intermediate files. The quality test code in section 4.2 should be updated to show this access pattern. Reading from the persistence layer is a fallback option but adds a dependency on persistence being enabled, which is not always the case.

**R8 refined: specify `run_pipeline` as the execution function for phase-level quality tests. Show the access pattern: `result = run_pipeline(config); review_text = (result.output_dir / "phase1" / "agent-0.md").read_text()`. Priority: Must fix.**

### M-7: Consumer-specific concerns I acknowledge but place out of scope

The consumer-advocate's cross-review identifies several items I did not address:

1. **Desktop Extension content scanner rejection** (their "What I Caught" item 3): Valid concern, but this is a Desktop Extension integration test, not an engine eval test. The role-split workaround in `design_deliberation()` and `analyze_documents()` is engine code, but the content scanner is a Claude Desktop platform constraint. I acknowledge this exists but maintain it belongs in Desktop Extension CI, not Spec 061.

2. **Paid tier groundwork** (their "What I Caught" item 4): The consumer-advocate is correct that the spec positions itself as "the foundation for the paid tier." I maintain that placeholder test sections are premature (per my cross-review of them), but I modify my position to agree that section 1's consumer table should note the HTTP/paid tier surface as planned, so the spec author can design the test architecture with future extensibility in mind. This is a documentation note, not a test requirement.

3. **Governance exit codes** (their "What I Caught" item 8): I missed this. The consumer-advocate is right that CI/CD pipelines acting as quality gates need a defined exit code contract. I adopt this as a new required change.

**New required change R17: Section 3.3.2 (CI/CD composition) must specify the governance exit code contract (0=PASS, 1=BLOCK, 2=ERROR) and include test assertions for each. Priority: P1.**

4. **Extended modes (negotiation, resource-allocation, fair-division, mechanism-design)** (their "What I Caught" item 5): The consumer-advocate says the spec's "(if supported in decide)" hedge is not a valid test specification. I partially agree. The eval suite should determine whether extended modes produce a valid deliberation or a clear error. The test should be: for each extended mode, call `decide` with mock provider; assert either a valid output or a specific, user-readable error message. "Unknown error" or a stack trace is a test failure.

**New required change R18: Replace "(if supported in decide)" with concrete test cases: each extended mode must produce either a valid output or a clear, documented error. Priority: P1.**

---

## Revised Required Changes Table

Incorporating all withdrawals, strengthenings, and modifications:

| # | Section | Change | Priority | Status vs Original |
|---|---------|--------|----------|-------------------|
| R1 | 3.1.1 | Red-blue tests must use pre-built YAML configs, not the adhoc decide path | Must fix | Unchanged |
| R2 | 3.1.6 | Fix quality_indicators schema to match actual QualityIndicators Pydantic model (nested object, not string array) — blocks correctness of 3.1.6 | Must fix | Strengthened (S-2) |
| R3 | 4.1 | Replace inline shell expansion with wrapper script + add test case with shell metacharacters in question | Must fix | Expanded (S-5) |
| ~~R4~~ | ~~4.1~~ | ~~Verify CLI flag name for JSON format~~ | ~~Withdrawn~~ | Withdrawn (W-1), pre-implementation checklist only |
| R5 | 5, G3 | Correct G3 description: distinguish auth.py resolution from execution provider resolution; fix target is handlers.py | Should fix | Unchanged |
| R6 | 7, Step 3 | Exclude red-blue from promptfoo first run; add pytest xfail test for adhoc red-blue parse_config | Must fix | Revised (S-3), adopted test-architect's xfail resolution |
| R7 | 7, Step 5 | Clarify fix target is handlers.py, not auth.py | Should fix | Unchanged |
| R8 | 3.2.1 | Specify `run_pipeline` as execution function for phase-level quality tests; show intermediate file access pattern | Must fix | Refined (M-6) |
| R9 | 3.1.4, 3.3.1 | Settings cascade: clean_settings conftest fixture + explicit test cases for each cascade level including env vars | Must fix | Upgraded from "Should fix" (S-4) |
| ~~R10~~ | ~~4.2~~ | ~~Specify LLM judge model for deepeval~~ | ~~Withdrawn~~ | Withdrawn (W-2), replaced by lighter note requirement |
| R11 | 2.1 | Add engine/run.py resolve_execution_provider to architecture diagram | Nice to have | Unchanged |
| R12 | New | Add CI runner requirements (Python 3.12, Node 18, API key secrets) | Should fix | Unchanged |
| R13 | 3.3.3 | Add SDK surface to cross-surface parity tests; assert inner content parity | Must fix | New (M-1) |
| R14 | New | Mock provider must return synthesis-parseable output (realistic response mode) | P0 — Must fix | New (M-2) |
| R15 | New | Add multi-round pipeline tests (rounds=2 convergence, rounds=3 stagnation) | P0 — Must fix | New (M-3) |
| R16 | New | Add arbiter interaction tests (trigger modes, at minimum no-disputes and always) | P1 | New (M-4) |
| R17 | 3.3.2 | Specify governance exit code contract for CI/CD (0=PASS, 1=BLOCK, 2=ERROR) with assertions | P1 | New (M-7) |
| R18 | 3.1.1 | Replace "(if supported)" for extended modes with concrete pass-or-clear-error test cases | P1 | New (M-7) |
| R-CLI | 3.1.3 | Confirm `conversus status` exists and specify output, or remove from test list | Must fix | Upgraded (M-5) |
| G11 | 5 | Add gap: dual provider-resolution path (resolve_provider vs resolve_execution_provider), both call sites in handlers.py | P1 | Strengthened (S-1) |

---

## Revised Verdict

**Approve with required changes.** The must-fix list is now larger than my original (R1, R2, R3, R6, R8, R9, R13, R14, R15, R-CLI) but more precisely targeted. Two items were withdrawn (R4, R10) as over-specified. Six items were added from the cross-reviews (R13-R18, R-CLI upgrade).

The most significant revision is the addition of R14 (mock provider realistic mode). This was the test-architect's finding, not mine, and it is the single most consequential gap in the spec. Without it, the entire smoke tier validates error-recovery code paths rather than production code paths. I should have caught this during my initial codebase trace of the mock provider through the synthesis parser, and I did not.

The second most significant revision is R13 (SDK surface in parity tests). Both cross-reviewers independently identified this omission in my review. The SDK is a shipped, importable API with a third provider-resolution path, and I did not mention it once. This is the clearest blind spot in my original review.

The implementation order from section 7 remains sound with three adjustments:
1. Step 3 scoped per R6 (exclude red-blue, add xfail).
2. Step 4 expanded to include mock provider realistic mode (R14) alongside G1/G2 fixes.
3. SKILL.md parity moved from step 9 to step 5, per the consumer-advocate's recommendation that I endorsed in my cross-review.

The spec, with these changes, is ready for implementation.
