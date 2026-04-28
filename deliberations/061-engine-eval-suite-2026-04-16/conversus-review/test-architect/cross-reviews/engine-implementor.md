# Cross-Review: test-architect reviewing engine-implementor

**Date**: 2026-04-16
**Phase**: 2 -- Cross-Reviews

---

## Dangerous Contradictions

### DC-1: The provider resolution divergence is bigger than either of us stated

The engine-implementor's most valuable original finding is that `auth.py` `resolve_provider` and `run.py` `resolve_execution_provider` are two different code paths, and that MCP handlers use the former while CLI uses the latter. This is correct and important. The engine-implementor proposes adding this as G11.

I identified the same surface area in my review (section 6.1, "VALID_PROVIDERS is hardcoded to two" and section 6.2, "Two MCP servers, two result type hierarchies") but framed it as a config-parsing constraint and a type hierarchy issue rather than as a resolution-path divergence. The engine-implementor's framing is more precise: the root cause is not that VALID_PROVIDERS is too small, but that handlers.py calls the wrong function. My framing would lead to widening VALID_PROVIDERS; the engine-implementor's framing leads to fixing the call site in handlers.py. The engine-implementor's fix is correct and mine would have been a band-aid.

However, both of us understate the severity. The engine-implementor notes `_run_in_process` (handlers.py line 491) has the same bug but treats this as a separate observation ("missing from the spec, item 4"). It is not separate -- it is the same bug in a second call site. The spec needs a single G11 entry that names both `run_decide_mcp` and `_run_in_process` as affected, with a single fix: replace all `resolve_provider` calls in handlers.py with `resolve_execution_provider`. My review missed the `_run_in_process` path entirely.

### DC-2: We disagree on whether `conversus status` exists

The engine-implementor (section 3.1.3) says they "did not find" `conversus status` in the CLI module and flags it as a required change to verify or remove. My review did not question this command's existence because I was focused on test dimension gaps, not CLI command inventory. The engine-implementor is correct to flag this -- if the command does not exist, the spec is testing phantom functionality. I should have caught this as part of the surface coverage audit.

### DC-3: The `quality_indicators` schema error is a factual bug in the spec that I missed

The engine-implementor (R2) identifies that the spec's JSON schema shows `quality_indicators` as a string array, but the actual `ConversusOutput` Pydantic model defines it as a `QualityIndicators` object with integer fields (`agent_count`, `phases_completed`, etc.) plus one string field (`mode`). My review (section 4.2) criticized the `is-json` assertion as "too weak" and said the assertion should validate all 5 fields are present and non-empty. But I accepted the spec's schema as written -- I did not verify it against the actual Pydantic model. The engine-implementor did, found it wrong, and filed a must-fix. This is a clear miss on my part. Writing assertions against an incorrect schema is worse than writing weak assertions against a correct one.

---

## Tensions

### T-1: Scope of the first eval run

The engine-implementor (R6) says step 3 (first eval run) must explicitly exclude red-blue mode and limit to mock provider to get a clean baseline. My review (section 7, P0 item 3) says the spec must test adhoc red-blue end-to-end through `parse_config`, not just raw YAML inspection.

These are not contradictory but they create a sequencing tension. The engine-implementor wants a clean first run that avoids known failures. I want the red-blue regression test to exist from day one. The resolution is: the first promptfoo run excludes red-blue (engine-implementor's R6), but the pytest functional tier includes a red-blue test marked `xfail` that calls `parse_config` on adhoc-generated config and documents the expected failure (my P0 item 3). This way the baseline is clean for promptfoo, but the regression test exists immediately and will flip to pass when G1 is fixed.

### T-2: Priority framing -- implementation blockers vs coverage gaps

The engine-implementor's review is organized around implementability: "will this test work as written?" Their required changes (R1-R12) are framed as "must fix before implementation begins." My review is organized around coverage completeness: "what test dimensions are missing?" My recommendations (P0-P2) are framed as "must fix before the suite can serve as a quality gate."

These are complementary lenses but they produce different priority orderings. The engine-implementor puts the promptfoo shell-quoting issue (R3) as a must-fix; I did not mention it at all because I was evaluating the test matrix, not the framework mechanics. Conversely, I put multi-round pipeline tests as P0 item 1; the engine-implementor does not mention multi-round testing at all because the spec does not propose it, and the engine-implementor is reviewing what the spec proposes, not what it omits.

Both orderings are needed. The engine-implementor's R1-R8 must-fixes are prerequisites for the spec to be implementable. My P0 items 1-4 are prerequisites for the suite to be meaningful. The implementation plan should sequence: engine-implementor's R1-R8 first (make the spec correct), then my P0 items (make the spec complete).

### T-3: How to handle the settings cascade in tests

The engine-implementor (item 1 under "Missing from the Spec") identifies that `load_settings()` reads from `~/.conversus/settings.yml` and project-level settings, which can override mock provider defaults in tests. They recommend every test must mock `load_settings` or run in a clean temp directory with `HOME` overridden.

My review (section 3.4) identifies the settings cascade as an undertested combinatorial space -- each setting key at each cascade level at each surface. These are the same concern from opposite directions. The engine-implementor asks "how do we prevent the cascade from polluting tests?" I ask "where are the tests that verify the cascade itself works?"

Both are needed. The conftest.py fixtures should provide a `clean_settings` fixture (engine-implementor's concern) and the test matrix should include explicit cascade-level tests (my concern).

### T-4: deepeval judge model and embedding model

The engine-implementor (R10) flags that the spec does not specify the LLM judge model for deepeval (defaults to GPT-4). They also note (section 3.2.3) that regression baselines using embedding distance require an embedding model and `OPENAI_API_KEY` in CI. My review (section 4.3) flags that the quality thresholds are arbitrary without a calibration baseline, and (section 5.1) that the baseline storage and update workflow is underspecified.

We are both identifying the same problem from different angles: the deepeval tier has infrastructure dependencies that the spec does not enumerate. The engine-implementor identifies the specific dependencies (judge model, embedding model, API keys). I identify the process dependencies (calibration run, baseline storage, update workflow). The spec needs both: an explicit infrastructure requirements section and a baseline calibration plan.

---

## Safe Agreements

### SA-1: The two-tool architecture (promptfoo + deepeval) is correct

Both reviews endorse the tool split. The engine-implementor confirms promptfoo exec provider will work (with the shell-quoting fix) and deepeval GEval criteria are well-written. My review confirms the functional/quality split maps cleanly to CI cadence. Neither review suggests an alternative framework.

### SA-2: G1 (red-blue broken in decide) is P0 and blocks meaningful testing of the mode matrix

The engine-implementor verified the bug in detail (DEFAULT_AGENTS lack `role: red/blue`, parse_config enforces role presence). My review independently identifies the same bug and notes the existing test (`test_adhoc.py` line 49-57) only checks raw YAML, not `parse_config` success. Both reviews agree the fix is in `engine/adhoc.py` with mode-aware agent selection.

### SA-3: G3 description in the spec is imprecise

The engine-implementor correctly identifies that the 9 providers ARE wired as ExecutionProviders in the registry and are only missing from auth.py's `resolve_provider`. My review (section 6.1) identifies the same issue from the config side (VALID_PROVIDERS hardcoded to two). Both agree the spec's framing ("9 providers unwired in auth") overstates the gap -- the execution path works, only the handler path is broken.

### SA-4: The cross-surface parity test (3.3.3) is the highest-value integration test

The engine-implementor explicitly calls this "the most important integration test in the spec." My review identifies that the parity claim is incomplete because it omits the SDK surface, but agrees the CLI-vs-MCP parity test is essential. The engine-implementor adds the observation that this test will itself discover the provider resolution divergence (CLI through `resolve_execution_provider`, MCP through `resolve_provider`), which is a concrete prediction of test value.

### SA-5: The spec conflates provider instantiation with provider functionality

My review (section 4.4) defines four test levels: import, instantiation, auth-resolution, dispatch. The engine-implementor (section 3.1.2) independently defines the same four levels with the same conclusion: only the dispatch level is meaningful for catching real bugs. Both reviews agree the spec's "instantiate without error" criterion (section 3.1.2) is trivially insufficient.

### SA-6: CI requirements are missing

The engine-implementor (item 3 under "Missing from the Spec") identifies that the spec does not specify Docker image, Python version, Node.js for promptfoo, or API key secrets. My review does not flag CI requirements explicitly but notes (section 5.1) that baseline storage location is unspecified. The engine-implementor's coverage of CI requirements is more thorough than mine.

---

## What They Caught That I Missed

1. **The `_run_in_process` call site** (handlers.py line 491) using `resolve_provider` instead of `resolve_execution_provider`. I identified the surface-level divergence but missed this second call site.

2. **The `quality_indicators` schema is wrong** (R2). I reviewed the assertions against the spec's schema without verifying the schema against the Pydantic model. The engine-implementor verified and found a factual error.

3. **promptfoo shell-quoting injection** (R3). I evaluated the promptfoo config at the test-design level (is the matrix complete?) without evaluating whether the exec provider would actually execute correctly. The engine-implementor correctly identifies that `{{prompt}}` with shell metacharacters will cause injection or parse failures.

4. **The `--format json` flag name may be wrong** (R4). The spec uses `--format json` but the CLI may use `--output-format`. I did not verify flag names.

5. **`run_decide_mcp` default "mock" treated as "not explicitly set"** (section 3.1.4 note). The handler treats `provider == "mock"` as `None`, allowing the settings cascade to override it. This means mock-provider tests are not actually isolated from the environment. I missed this subtle interaction.

6. **conftest.py integration** (item 2 under "Missing from the Spec"). The existing test suite has shared fixtures that the eval suite should reuse. I proposed new test dimensions without mentioning integration with existing test infrastructure.

7. **`conversus status` may not exist** as a CLI command. I did not audit the CLI command inventory.

---

## What I Caught That They Missed

1. **Multi-round pipeline testing** (section 2.2). The spec mentions `rounds: 2` in config parsing tests but never tests the actual multi-round orchestrator: stagnation detection, cross-round synthesis, inter-round arbitration, termination reasons. The engine-implementor does not mention this gap. These are the highest-complexity code paths in the engine with zero dedicated test coverage.

2. **Arbiter interaction testing** (section 2.3). The arbiter is a conditional Phase 6 with trigger modes, influence levels, and timing variants. The engine-implementor does not mention arbiter testing. The spec only covers arbiter in config parsing.

3. **Iteration loop testing** (section 2.4). The cross-review/revision iteration loop is untested beyond config validation. The engine-implementor does not flag this.

4. **Desktop extension divergence** (section 2.5). The desktop extension has its own MCP server with inline result types that may drift from the main engine's `engine/results.py`. The engine-implementor does not address whether the two copies should be tested for parity.

5. **Persistence layer testing** (section 2.6). Write/read round-trip, list/show, cleanup, disable -- none covered. The engine-implementor mentions the persistence path as a way to access intermediate artifacts (section 3.2.1) but does not flag persistence itself as untested.

6. **Cancellation testing** (section 2.7). `engine/cancel.py` provides `CancellationFlag` used by `phases.py`. Mid-pipeline cancellation is untested. Not mentioned in the engine-implementor's review.

7. **SDK surface in cross-surface parity** (section 2.8). My review identifies that the SDK has different result types (`engine.sdk.Result` vs `engine.results.DecideResult`) and is excluded from the parity test. The engine-implementor discusses cross-surface parity but only for CLI vs MCP.

8. **Mock provider masks real failures** (section 4.1). The mock provider returns text that does not contain the markdown headings `parse_synthesis` expects. The `from_events()` method catches parse failures with a bare `except` and falls back to empty strings. This means the entire smoke tier tests the fallback path, not the production path. The engine-implementor mentions G6 (mock headline template) but does not connect it to the broader problem that the smoke tier is testing error-recovery code, not happy-path code.

9. **Pydantic schema snapshot tests** (section 5.2). If a field is added, removed, or renamed in the result types, MCP consumers break silently. No snapshot test exists to catch schema drift. Not mentioned in the engine-implementor's review.

10. **The mode x surface matrix is sparse** (section 3.1). All 8 modes tested via CLI only; MCP, SDK, and Skill surfaces are untested for most modes. The engine-implementor discusses mode implementability per-mode but does not map modes across surfaces.
