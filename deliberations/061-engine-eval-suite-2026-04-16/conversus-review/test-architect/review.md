# Test Architecture Review: Spec 061 — Engine Eval Suite

**Reviewer role**: Test architecture specialist (coverage completeness, combinatorial gaps, regression strategy)
**Reviewed**: 2026-04-16
**Verdict**: Conditional approval -- strong foundations but several structural gaps in the test matrix, failure detection strategy, and regression machinery that must be addressed before the suite can serve as the paid-tier quality gate the spec intends.

---

## 1. What the spec gets right

The spec correctly identifies the core problem: a multi-surface, multi-provider engine with zero cross-cutting validation. The architecture-under-test diagram (section 2.1) is honest about the layers, and the Known Gaps table (section 5) is unusually candid for a spec -- it names real bugs with severities and surfaces. The two-layer eval strategy (promptfoo for structural/functional, deepeval for LLM-as-judge quality) is a sound split. The test markers (smoke/eval/live/integration) map cleanly to CI cadence.

The discovery that SKILL.md masks engine bugs by reimplementing the pipeline as prompt instructions (section 1, paragraph 4) is an important architectural insight that deserves to be an explicit test dimension, not just a motivating observation.

---

## 2. Missing test dimensions

### 2.1 Per-agent provider override (heterogeneous deliberation)

`AgentConfig` supports `provider`, `agent_model`, and `timeout` overrides (engine/config.py lines 49-61). A deliberation can have agent A on `anthropic` and agent B on `ollama`. The spec's provider matrix (3.1.2) tests each provider in isolation. There is no test for mixed-provider deliberations:

- Agent A resolves provider X, Agent B resolves provider Y, both complete, synthesis merges both.
- Agent A's provider fails, Agent B succeeds -- does the N-1 continuation work correctly?
- Per-agent model override (`agent_model`) interacts with the global `--model` flag.
- Per-agent timeout override.

This is not exotic -- the config schema supports it, so users will try it.

### 2.2 Multi-round deliberation (rounds > 1)

The spec mentions `rounds: 2` in the config parsing tests (3.1.5) but never tests the actual multi-round pipeline. The phases.py orchestrator implements a round loop with stagnation detection, cross-round synthesis, and inter-round arbitration. None of this appears in any test dimension:

- Rounds = 2, stagnation = "detect", agents converge after round 1 -- does termination_reason = "converged"?
- Rounds = 3, stagnation = "detect", agents repeat themselves -- does termination_reason = "stagnation"?
- Rounds = 5, no convergence -- does termination_reason = "max_rounds"?
- Inter-round arbitration (arbiter.timing = "inter-round") with rounds = 3.

These are the highest-complexity code paths in the engine and they have zero dedicated eval tests.

### 2.3 Arbiter interaction

Arbitration is a conditional Phase 6 that fires when `trigger: disputes_remain` and disputes are detected. The spec mentions arbiter in config parsing tests (3.1.5 row "With arbiter") but never tests:

- Arbiter fires and produces binding ruling -- does synthesis incorporate it?
- Arbiter fires with `influence: advisory` vs `influence: binding` -- behavioral difference?
- Arbiter fires with `trigger: always` -- does it run even without disputes?
- Arbiter with `timing: inter-round` and `rounds: 1` -- the engine logs a warning, but does it silently skip?

### 2.4 Iterations (iteration loop)

The pipeline has an iteration loop around cross-review and revision (Phase 2 and Phase 3). The spec lists `iterations: 3` only as a config validation test. There is no test that verifies:

- Iterations = 3 actually runs cross-review and revision 3 times.
- Cost estimate reflects 3x dispatches for those phases.
- Output directory structure contains the correct iteration-numbered files.

### 2.5 Desktop Extension divergence

The spec identifies `desktop-extension/server/lib/engine/` as a separate copy of the engine. This is a parallel universe: it has its own `mcp_server.py`, its own `test_integration.py`, its own result types (defined inline rather than imported from `engine/results.py`), and its own `test_concrete_providers.py` that does not exist in the main engine. The spec does not address:

- Are the two engine copies byte-identical? If not, which is canonical?
- Should evals run against both copies?
- The desktop extension `mcp_server.py` defines `CostEstimate`, `ValidateResult`, `RunResult`, `DecideResult` inline -- the main engine imports from `engine/results.py`. Schema drift between these is invisible.

Without testing parity between these copies, the spec's "cross-surface parity" claim (3.3.3) is incomplete.

### 2.6 Persistence layer

`engine/persistence.py` is imported and used by `engine/handlers.py` to persist deliberation results. The spec does not test:

- Persistence writes to the correct path.
- `ListResult` and `ShowResult` round-trip correctly.
- Persistence disabled via settings (`persistence.enabled: false`).
- Old deliberation cleanup (`cleanup_old_deliberations`).

### 2.7 Cancellation

`engine/cancel.py` provides `CancellationFlag`, which `phases.py` imports. The spec does not test:

- Mid-pipeline cancellation.
- Cancellation between phases vs mid-dispatch.
- Whether partial output is preserved on cancellation.

### 2.8 SDK surface

Section 2.1 lists the SDK (`engine/sdk.py`) as a consumer but section 3 only tests CLI and MCP surfaces. The SDK has its own `Deliberation` class, `Result` model, and `validate()` function with different types than the MCP result types. The cross-surface parity test (3.3.3) compares CLI and MCP but omits SDK:

```python
# SDK surface (untested)
result = await Deliberation(question="Q", provider="mock").run()
# result is engine.sdk.Result (headline, summary, full_analysis, quality_indicators, debate_transcript)

# MCP surface (tested)
result = run_decide_mcp("Q", "mock", "cooperative", 20)
# result is engine.results.DecideResult (sufficient, classification, output, cost_estimate, errors)
```

These are different types with different fields. "Structurally identical output" is undefined when the types differ.

---

## 3. Combinatorial gaps in the test matrix

### 3.1 Mode x Surface matrix

The spec tests all 8 modes via CLI (promptfoo, section 4.1) but only tests MCP handlers with implicit defaults. There is no explicit mode x surface matrix:

| Mode | CLI | MCP | SDK | Skill |
|---|---|---|---|---|
| cooperative | Y | ? | - | - |
| winner-take-all | Y | ? | - | - |
| prisoners-dilemma | Y | ? | - | - |
| red-blue | Y | ? | - | - |
| negotiation | Y (marked "if supported") | - | - | - |
| resource-allocation | Y (marked "if supported") | - | - | - |
| fair-division | Y (marked "if supported") | - | - | - |
| mechanism-design | Y (marked "if supported") | - | - | - |

The 4 advanced modes (negotiation, resource-allocation, fair-division, mechanism-design) are valid in `VALID_MODES` (conversus/schemas/modes.py) but marked "(if supported in decide)" in section 3.1.1. This is ambiguous -- they either work or they do not. The eval should explicitly test them or explicitly skip them with a documented reason.

### 3.2 Mode x Provider matrix

The promptfoo config (section 4.1) tests 4 modes x 1 provider (mock). It does not test even one real provider across modes. The deepeval quality tests (section 4.2) use anthropic but only test `cooperative`. The mode x provider matrix is:

| | mock | anthropic | openai | claude-code | ollama | ... |
|---|---|---|---|---|---|---|
| cooperative | promptfoo | deepeval | - | - | - | - |
| winner-take-all | promptfoo | - | - | - | - | - |
| red-blue | promptfoo | - | - | - | - | - |
| prisoners-dilemma | promptfoo | - | - | - | - | - |

This is extremely sparse. At minimum, each mode should have one real-provider quality test.

### 3.3 Format x Surface matrix

The spec lists `--format json` and `--format rich` for CLI (section 3.1.3) but does not define what `--format rich` output should look like or how to validate it. Is it a visual-only test? Does it have structural assertions? The MCP surface always returns Pydantic models. The SDK returns different Pydantic models. There is no test that verifies `--format rich` output can be consumed by a terminal renderer without errors.

### 3.4 Settings cascade x Provider x Surface

The settings cascade test (3.3.1) says "Test by setting provider at each level and verifying which one wins." This is a 5-level cascade with at least 3 surfaces. The combinatorial space is 5 levels x 3 surfaces = 15 tests. The spec does not enumerate them, and G8 acknowledges this is untested. But even the proposed test is underspecified:

- What about `default_mode` in the cascade?
- What about `default_model` in the cascade?
- What about `max_launches` in the cascade?
- What about `persistence.enabled` in the cascade?

Each setting key should be tested at each cascade level.

---

## 4. The gap between "test exists" and "test is meaningful"

### 4.1 Mock provider masks real failures

The entire smoke tier runs on `mock`, which returns canned text like `[mock:agent-name] {prompt}`. This text does not contain markdown headings that `parse_synthesis` needs (`### Headline`, `### Summary`, etc.). The `StructuredDeliberation.from_events()` method (engine/models.py) catches parse failures with a bare `except` and falls back to empty strings. This means mock-provider smoke tests will always pass on structure but never validate that the pipeline produces parseable synthesis.

The spec acknowledges G6 (`headline` is `[Change label]` in mock output) but does not propose a solution. The mock provider needs a "realistic response mode" that returns well-structured markdown for each phase, or the entire smoke tier is testing the fallback path rather than the production path.

### 4.2 Promptfoo `is-json` assertion is too weak

The promptfoo config (section 4.1) asserts `is-json` and checks that `headline !== undefined`. But the JSON schema defined in section 3.1.6 has 5 required fields (`headline`, `summary`, `full_analysis`, `quality_indicators`, `debate_transcript`). The assertion should validate all 5 fields are present and non-empty. Also, `quality_indicators` is an array -- is it always populated? What are valid quality indicator strings?

### 4.3 Quality thresholds are arbitrary

The deepeval thresholds (section 3.2.1) range from 0.6 to 0.8. There is no justification for these numbers. What baseline performance produced these thresholds? A threshold of 0.7 on "review independence" could mean anything without knowing the score distribution. The spec should either:

- Run the eval once, observe the distribution, set thresholds at P25 (deliberately lenient initially).
- Or declare the thresholds as aspirational with a plan to calibrate after the first baseline run.

### 4.4 Provider instantiation != provider functionality

Section 3.1.2 says "Each provider must instantiate without error." This is a necessary but trivially insufficient condition. An `__init__` that does not raise tells you nothing about whether `execute()` works, whether auth resolves, or whether the provider handles timeouts. The spec should distinguish:

- **Import test**: The module imports without error (Python-level).
- **Instantiation test**: `get_provider(name)` returns an instance (registry-level).
- **Auth resolution test**: `resolve_execution_provider(name)` succeeds with appropriate credentials (auth-level).
- **Dispatch test**: `provider.execute(task)` returns a valid `ExecutionResult` (protocol-level).

Only the last is meaningful for catching bugs like G3 (providers without auth wiring).

---

## 5. Regression detection strategy

### 5.1 Baselines are underspecified

Section 3.2.3 says "save the first passing output as a baseline" and compare future runs using structural similarity, semantic similarity, and quality non-regression. But:

- **Storage**: Where do baselines live? In the repo? In a CI artifact store? If in-repo, do they get reviewed?
- **Versioning**: When a legitimate change improves output, how is the baseline updated? Manual approval? Automatic?
- **Flakiness**: LLM output is non-deterministic. Even with the same provider and prompt, two runs produce different text. What is the semantic similarity threshold? How many runs establish a stable baseline?
- **Mode-specific baselines**: 8 modes x 5 questions = 40 baselines. Who reviews 40 golden files?

### 5.2 No snapshot testing for Pydantic schemas

The spec defines result schemas (`ValidateResult`, `RunResult`, `DecideResult`, `CostEstimate`) but does not test schema stability. If a field is added, removed, or renamed, MCP consumers break. There should be a snapshot test that dumps each model's JSON schema and fails if the schema changes without an explicit version bump.

### 5.3 No regression test for the G1 bug pattern

G1 (red-blue mode fails in `decide`) is a specific pattern: `build_adhoc_config` generates config with default agents that lack `role: red/blue`, then `parse_config` rejects it. The existing test (`test_adhoc.py` line 49-57) only checks the raw YAML, not whether `parse_config(config_path)` succeeds. This is exactly the kind of "test exists but is not meaningful" gap that the eval suite should prevent.

The fix for G1 is straightforward (use red-team/blue-team presets with roles when mode=red-blue), but the regression test must call `parse_config` on the generated config, not just read the YAML.

---

## 6. Structural concerns

### 6.1 config.py VALID_PROVIDERS is hardcoded to two

`engine/config.py` line 82: `VALID_PROVIDERS = ("anthropic", "openai")`. The `parse_config` function rejects any other provider string in the YAML `provider:` field. But `run_engine()` and `resolve_execution_provider()` accept 13+ provider names via the execution registry. This means:

- A full YAML config can only specify `provider: anthropic` or `provider: openai`.
- The CLI `--provider` flag overrides this at the `run_engine()` level.
- Ad-hoc mode via `build_adhoc_config` does not write a `provider:` key, so it bypasses validation entirely.

The eval suite tests "all registered providers instantiate" (section 3.1.2) but does not test whether they can be used end-to-end through each surface. A provider that instantiates fine but cannot be specified in a config file is not actually usable by the CLI `run` command.

### 6.2 Two MCP servers, two result type hierarchies

The main repo has `mcp_server.py` (imports from `engine/results.py`). The desktop extension has `desktop-extension/server/mcp_server.py` (defines its own `CostEstimate`, `ValidateResult`, etc. inline). The spec's MCP surface tests (3.1.4) test `engine.handlers` directly, which is neither of these MCP servers. If the goal is to validate that MCP consumers get correct responses, the test should call the actual `@mcp.tool()` functions or at least validate that the handler return types match the MCP tool type annotations.

### 6.3 No test for the `login_mcp` handler

Section 3.1.4 mentions `login_mcp` in the MCP surface tests but does not define any assertions for it. Section 3.1.3 lists `conversus login <provider>` and `conversus logout <provider>` but with no expected behavior or assertions. Auth lifecycle is load-bearing for real providers and deserves at least:

- Login with mock provider: should succeed or no-op.
- Login with real provider, no credentials: should return a clear error naming the provider.
- Logout when not logged in: should succeed idempotently.
- Credential state persists across login/validate/run cycle.

---

## 7. Recommendations (prioritized)

### P0 (must fix before implementation)

1. **Add multi-round pipeline tests** to the functional tier. At minimum: rounds=2 with mock, verifying 2 review phases in event log and correct termination_reason.
2. **Fix the mock provider to return parseable synthesis**. Without this, the entire smoke tier tests fallback code paths. Create a `response_fn` that generates well-structured markdown per phase and mode.
3. **Test adhoc red-blue end-to-end** through `parse_config`, not just raw YAML inspection. This is the regression test for G1.
4. **Define provider test levels** (import / instantiate / auth-resolve / dispatch) and test each provider at the appropriate level based on whether credentials are available.

### P1 (should fix before the paid tier)

5. **Add per-agent provider override tests** -- mixed-provider deliberation with N-1 failure semantics.
6. **Add arbiter tests** -- at least trigger=disputes_remain with and without disputes, influence=binding vs advisory.
7. **Address desktop extension divergence** -- either test both copies or document that one is canonical and the other is a build artifact.
8. **Add Pydantic schema snapshot tests** for all result types to catch breaking changes.
9. **Enumerate the settings cascade test matrix** explicitly -- each setting key x each cascade level x each surface.
10. **Test all 8 modes explicitly**, not 4 real + 4 "if supported." The eval suite's job is to determine what is supported.

### P2 (should fix before declaring the suite complete)

11. **Specify baseline storage and update workflow** -- in-repo golden files with CI approval gate.
12. **Add SDK surface to cross-surface parity tests**.
13. **Add cancellation tests**.
14. **Add persistence round-trip tests**.
15. **Calibrate deepeval thresholds** after the first baseline run rather than guessing numbers.
16. **Add `--format rich` structural tests** (at minimum: exits 0, produces output to stderr, does not produce JSON to stdout).

---

## 8. Summary

The spec identifies the right problem and proposes a reasonable two-layer eval architecture. But it has a structural blind spot: it tests the "simple center" of the configuration space (mock provider, cooperative mode, single round, no arbiter, CLI surface) while leaving the "complex edges" untested (multi-round, mixed providers, arbitration, all 8 modes through all surfaces, settings cascade). The edges are where the 28 release candidates worth of bugs live.

The most dangerous gap is that the mock provider's canned output does not exercise the synthesis parser's production path. A smoke suite built on top of unparseable mock output will show green while the real pipeline remains broken. Fixing this is the single highest-leverage change to the spec.
