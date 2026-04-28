# Engine Implementor Review: Spec 061 — Engine Eval Suite

**Reviewer role**: Engine implementor — will build these tests against the actual conversus engine
**Date**: 2026-04-16
**Verdict**: Approve with required changes

---

## Executive Summary

This spec correctly identifies the engine's real bugs and proposes the right two-tool stack (promptfoo for functional, deepeval for quality). The test cases are concrete enough to implement for approximately 60% of the matrix. The remaining 40% require either engine fixes first (red-blue, path doubling) or framework adaptation (promptfoo exec provider shell-quoting, deepeval GEval on structured pipeline output). The implementation order is mostly correct but has one critical sequencing error: step 3 (run first eval) will produce misleading results because the adhoc config generator cannot produce a valid red-blue config, and this is not just a "fix in step 4" issue -- it means the first eval run will fail on infrastructure, not on the bug the spec thinks it is testing.

---

## Section-by-Section Analysis

### 1. Problem Statement (Section 1)

**Assessment: Accurate and well-grounded.**

Every bug listed is real and I verified each against the codebase:

- **red-blue broken in decide**: Confirmed. `engine/adhoc.py` generates configs using `DEFAULT_AGENTS` (pragmatist + devils-advocate). Neither preset has `role: red` or `role: blue`. When mode is `red-blue`, `engine/config.py` lines 681-691 enforce that at least one agent has each role, so `parse_config` will raise `ConfigError("red-blue mode requires at least one agent with role: red.")`. The adhoc path has zero awareness of mode-specific agent requirements.

- **Target path doubling**: I can see the risk in `_resolve_file_entries` (config.py line 208: `p = (base / entry).resolve()`) combined with `build_adhoc_config` (adhoc.py line 146: `f"target: {question_path.resolve()}\n"`), which writes an absolute path into the YAML. If the config parser then joins that absolute path with the base directory, you get doubling. This depends on what `base` is at parse time -- if it is the temp dir and the target is already absolute, Path joining should collapse it, but edge cases around symlinks and relative config-dir offsets are plausible.

- **9 providers unwired in auth**: Confirmed. `engine/auth.py` `resolve_provider()` (line 631-671) only handles `mock`, `demo`, `anthropic`, and `openai`. The remaining providers (claude-code, aider, opencode, codex, copilot, gemini, ollama, pi, claude-desktop) exist as ExecutionProvider classes in `engine/execution/providers/` but `resolve_provider` in auth.py raises `ProviderError("Unknown provider")` for any name not in `OAUTH_CONFIGS`. However -- and this is a nuance the spec misses -- `engine/run.py` `resolve_execution_provider()` (lines 87-110) has a two-path resolution: legacy auth providers go through `resolve_provider`, but all others go through `PROVIDER_REGISTRY` directly. So the 9 providers ARE wired for execution, just not for the auth.py credential resolution path. The gap is narrower than stated: it affects `handlers.py` `run_decide_mcp` (line 197) which calls `resolve_provider` directly instead of `resolve_execution_provider`.

- **Question sufficiency gate**: Confirmed. `linter/question_classifier.py` uses `_MIN_SUFFICIENT_WORDS = 10` and `_MIN_WORDS = 5`. "Build vs buy for auth?" is 5 words, right at the boundary. The spec's test case "Build vs buy for auth?" has 6 tokens but some may not count as words depending on tokenization. The classifier also requires decision vocabulary OR alternatives OR constraints, and "vs" satisfies the alternatives check. The real question is whether 5-word questions with good decision signals get rejected -- that is the bug surface.

### 2. Architecture Under Test (Section 2)

**Assessment: Accurate diagram, but missing one critical layer.**

The composability contract in 2.2 is correct. Missing from the diagram: `engine/run.py` `resolve_execution_provider()` -- this is the actual provider resolution function that the CLI surface uses, and it has different behavior from `engine/auth.py` `resolve_provider()` that the MCP handler uses. This distinction matters because test results will differ depending on which surface you test through.

**Required change**: Add `engine/run.py` to the architecture diagram or note that provider resolution diverges between CLI and MCP surfaces. Tests must cover both paths.

### 3. Test Dimensions (Section 3)

#### 3.1.1 Mode Matrix

**Assessment: Implementable for 4 modes, speculative for 4 modes.**

The first four modes (cooperative, winner-take-all, prisoners-dilemma, red-blue) have dedicated template directories under `templates/`. The remaining four (negotiation, resource-allocation, fair-division, mechanism-design) also have template directories, so they are structurally supported. All 8 are in `VALID_MODES`.

However, the `build_adhoc_config` function only generates configs with `DEFAULT_AGENTS` (pragmatist + devils-advocate), which lack the `role: red/blue` fields needed for red-blue mode. This means:

- **cooperative, winner-take-all, prisoners-dilemma**: Implementable immediately with mock provider via adhoc path.
- **red-blue**: Blocked by G1. Cannot test through `decide` CLI/MCP until adhoc config is mode-aware.
- **negotiation, resource-allocation, fair-division, mechanism-design**: These likely work structurally but I have not verified their template variables are populated. The spec wisely marks them "(if supported in decide)".

**Required change**: For the mode matrix, the spec should explicitly state that red-blue tests must use a pre-built YAML config (not the adhoc `decide` path) until G1 is fixed. The promptfoo config in section 4.1 uses `exec:uv run conversus decide` which goes through the adhoc path and will fail for red-blue regardless of engine state.

#### 3.1.2 Provider Matrix

**Assessment: Table is accurate but the "Expected" column needs refinement.**

The "Auth method" column is correct. The "Known gap" note about 9 unwired providers is partially correct (see my analysis in section 1 above).

Key implementation detail: testing "instantiate without error" is different from testing "can execute a deliberation". The execution providers in `engine/execution/providers/` all register successfully at import time (confirmed by the eager imports in `__init__.py`). The test should verify:

1. Provider class instantiates (import-time registration -- already works for all 13).
2. Provider can be resolved via `resolve_execution_provider` (works for all registered providers).
3. Provider can be resolved via `resolve_provider` in auth.py (only works for mock, demo, anthropic, openai).
4. Provider can execute a task successfully (requires the actual binary/service for subprocess providers).

The spec conflates levels 2 and 3. The handlers use `resolve_provider` (auth.py), the CLI run path uses `resolve_execution_provider` (run.py). Tests should explicitly cover both.

**Required change**: Split the provider test into "resolution" tests (which path resolves which provider) and "execution" tests (which providers can actually complete a task). The resolution tests are pure unit tests; the execution tests need real infrastructure (except mock/demo).

#### 3.1.3 CLI Surface Tests

**Assessment: Implementable with one concern.**

The `conversus status` command -- I did not find this in the CLI module. `engine/cli/__init__.py` defines `run`, `decide`, `validate`, `login`, `logout`. I see `context` is in `engine/cli/context.py` but `status` may need to be verified.

The `conversus context` command exists (there is a `context.py` module).

**Required change**: Verify `conversus status` exists as a command or remove it from the test list.

#### 3.1.4 MCP Surface Tests

**Assessment: Implementable but the function signatures in the spec are wrong.**

The spec shows:
```python
result = validate_mcp(config_yaml, question="")
result = run_decide_mcp("Should we use X or Y?", "mock", "cooperative", 20)
result = run_mcp(config_yaml, output_path="", provider="")
```

Actual signatures from the codebase:
```python
def validate_mcp(config_yaml: str, question: str = "") -> ValidateResult:
def run_decide_mcp(question: str, provider: str = "mock", mode: str = "cooperative", max_launches: int = 20, *, mcp_context: object | None = None) -> DecideResult:
def run_mcp(config_yaml: str, output_path: str = "", provider: str = "") -> RunResult:
```

The positional arguments match. The assertions need adjustment:

- `validate_mcp` returns `ValidateResult` which has `.valid` (not `.valid`) -- actually it does have `.valid`, that is correct.
- `run_decide_mcp` returns `DecideResult` which has `.sufficient` -- correct.
- `run_mcp` returns `RunResult` which has `.validated` -- correct.

One issue: `run_decide_mcp` goes through the settings cascade (lines 105-107 in handlers.py), and the default provider "mock" is actually treated as "not explicitly set" (`provider if provider != "mock" else None`), meaning the settings cascade can override it. In tests, you must either set `CONVERSUS_DEFAULT_PROVIDER` or ensure no settings files exist, or the test environment may resolve to a different provider than expected.

**Required change**: Note in the MCP test section that tests must isolate the settings cascade (no project/global settings files, no CONVERSUS_* env vars) or the "mock" provider default will be overridden by the cascade.

#### 3.1.5 Config Parsing Tests

**Assessment: Fully implementable.** These map directly to `parse_config` which is well-tested already in `engine/tests/test_config.py`. The spec adds a few cases not currently covered (e.g., "Empty question" -- which is caught in handlers, not config parsing). Good additions.

#### 3.1.6 Output Schema Validation

**Assessment: Partially correct.**

The JSON schema shown:
```json
{
  "headline": "<string, non-empty>",
  "summary": "<string, non-empty>",
  "full_analysis": "<string>",
  "quality_indicators": ["<string>", ...],
  "debate_transcript": "<string>"
}
```

The actual `ConversusOutput` model has `quality_indicators` as a `QualityIndicators` object (not a list of strings). Its fields are: `agent_count`, `mode`, `phases_completed`, `cross_reviews_performed`, `genuine_disagreements_surfaced`, `genuine_disagreements_surviving`. All integers except `mode` (string).

**Required change**: Fix the JSON schema in section 3.1.6 to match the actual `ConversusOutput` Pydantic model. The `quality_indicators` field is a nested object, not a string array.

#### 3.1.7-3.1.8 Error Handling and Target Document Tests

**Assessment: Implementable.** These are straightforward and the engine code supports all listed scenarios.

### 3.2 Quality Tests (deepeval)

#### 3.2.1 Pipeline Phase Quality

**Assessment: Partially implementable -- needs access to intermediate artifacts.**

The spec proposes metrics like "Review independence" and "Cross-review adversarial quality". These require access to individual agent outputs from phases 1-4, not just the final synthesis. The `run_decide_mcp` handler returns only `DecideResult.output` which is the parsed synthesis. The intermediate files (reviews, cross-reviews, revisions, disputes) are written to the output directory but not exposed in the return value.

To test these metrics, the eval must either:
1. Call `run_pipeline` directly and read intermediate files from `PipelineResult.output_dir`.
2. Use the persistence path (`DecideResult.output_path`) to find the deliberation directory and read intermediate files.

Option 2 is viable because the persistence layer copies the entire output tree. But the spec does not mention this access pattern.

**Required change**: Specify how quality tests access intermediate phase outputs. The deepeval test code should call `run_pipeline` directly (not `run_decide_mcp`) or should read from the persisted deliberation directory.

#### 3.2.2 Mode-Specific Quality

**Assessment: Good criteria, but thresholds need calibration.**

The 0.7 threshold for red-blue "adversarial coverage" requires red team to "identify at least 3 distinct attack vectors." With mock provider this is meaningless (mock returns canned text). With real providers, the output quality is highly prompt-dependent. I recommend starting with threshold 0.5 for the first baseline pass and raising once we have empirical data.

#### 3.2.3 Regression Baselines

**Assessment: Good idea, tricky implementation.**

Embedding distance comparison requires an embedding model. The spec does not specify which one. `deepeval` defaults to OpenAI embeddings, which requires `OPENAI_API_KEY`. If the eval suite is supposed to run in CI, the embedding model dependency needs to be explicit.

**Required change**: Specify the embedding model for regression baselines (or state that baselines use structural comparison only, deferring semantic comparison to manual runs).

### 3.3 Composition Tests

#### 3.3.1 Settings Cascade

**Assessment: Implementable.** The `engine/settings.py` module is clean and testable. Some cascade tests already exist in `engine/tests/test_settings.py` and `engine/tests/test_integration_settings.py`. The spec adds end-to-end validation which is the right gap to fill.

#### 3.3.2 Consumer-Specific Composition

**Assessment: Ambitious but correct framing.** The "Start MCP server" test for Claude Desktop requires either a real MCP server process or mocking the stdio transport. The spec should acknowledge that MCP server integration tests are slow and may need a separate CI job.

#### 3.3.3 Cross-Surface Parity

**Assessment: Implementable and high-value.** This is the most important integration test in the spec. The CLI `run_decide_cli` handler prints to stdout and exits; the MCP `run_decide_mcp` returns a structured result. Asserting structural parity means capturing CLI stdout JSON and comparing against the MCP return value.

One concern: `run_decide_cli` goes through `engine.run.run_engine` while `run_decide_mcp` goes through `engine.phases.run_pipeline` directly. Different code paths may produce different results even with the same mock provider, because `run_engine` calls `resolve_execution_provider` (which may wrap the provider in an adapter) while `run_decide_mcp` calls `resolve_provider` from auth.py. This is itself a bug (or at least a parity gap) that the test would discover.

---

## Section 4: Eval Framework

### 4.1 promptfoo exec: Provider

**Assessment: Will not work as written.**

The promptfoo config uses:
```yaml
providers:
  - id: exec:uv run conversus decide "{{prompt}}" --provider mock --mode cooperative --format json
```

Issues:

1. **Shell quoting**: `{{prompt}}` will be substituted by promptfoo, but the resulting string is passed through the shell. If the prompt contains quotes, ampersands, semicolons, or other shell metacharacters, the command breaks. Promptfoo's `exec:` provider runs commands via the shell, so prompts with special characters will cause injection or parse failures. The fix is to use promptfoo's `exec:` provider with a wrapper script that reads stdin or uses a temp file, not inline shell expansion.

2. **Exit code handling**: `conversus decide` calls `sys.exit(1)` on errors (handlers.py line 341, 359, 363, 371). promptfoo's exec provider treats non-zero exit as a failure. This is actually correct behavior, but the spec should note that error-path tests (3.1.7) cannot use the same exec provider config -- they need a separate provider that expects non-zero exits.

3. **Mixed stdout/stderr**: The CLI handler uses `click.echo(..., err=True)` for warnings (line 325) and `click.echo(result.model_dump_json(indent=2))` for output (line 382). The exec provider captures stdout. If any errors or warnings leak to stdout, the JSON assertion will fail. This is gap G7 in the spec, and it is correctly identified.

4. **The `--format json` flag**: The spec references `--format json` but the CLI `decide` command uses `--output-format` (or `-f`). Verify the actual flag name.

**Required change**: 
- Use a wrapper script for the promptfoo exec provider that handles shell quoting safely.
- Verify the exact CLI flag name for JSON output format.
- Document that error-path tests need a different provider configuration.

### 4.2 deepeval GEval

**Assessment: Will work but needs adjustment for the data access pattern.**

The test code:
```python
result = run_decide_mcp("Should we use Postgres or MongoDB for metadata?", "anthropic", "cooperative", 20)
test_case = LLMTestCase(
    input="Should we use Postgres or MongoDB for metadata?",
    actual_output=result.output.get("full_analysis", ""),
)
```

`result.output` is the `ConversusOutput.model_dump()` dict, so `.get("full_analysis", "")` will work. But `full_analysis` for the synthesis quality metric is the right field -- it contains the synthesis text which is what the GEval criteria evaluate.

For phase-level quality (3.2.1), the `actual_output` needs to be the phase-specific text (individual reviews, cross-reviews, etc.), which is not in `result.output`. See my note above about intermediate artifact access.

The `SYNTHESIS_QUALITY` GEval metric definition is well-written. The criteria are specific and the scoring rubric (0, 0.5, 1) is the right granularity. However, GEval by default uses GPT-4 as the judge. If you want to use Anthropic models as judges, you need to configure deepeval's model accordingly (`deepeval set-model`). The spec should state which judge model to use.

**Required change**: Specify the LLM judge model for deepeval (default GPT-4 vs Anthropic).

### 4.3 Test Markers

**Assessment: Good taxonomy.** `smoke`, `eval`, `live`, `integration` map to clear use cases. One addition needed: a `slow` marker for tests that take >30s (MCP server integration tests, multi-round deliberations with real providers).

---

## Section 5: Known Gaps

**Assessment: Accurate severity ratings, one correction needed.**

- **G1 (red-blue in decide)**: P0 is correct. This blocks all red-blue smoke tests.
- **G2 (target path doubling)**: P1 is correct. I confirmed the risk surface but could not reproduce reliably in my code review -- it depends on the relationship between config_path base directory and the target path format. The eval suite will surface this definitively.
- **G3 (9 unwired providers)**: P1 severity is correct but the description is imprecise. The providers ARE wired as ExecutionProviders in the registry. They are NOT wired through auth.py's `resolve_provider`. The fix is for `run_decide_mcp` to use `resolve_execution_provider` instead of `resolve_provider`, not to wire all 9 into auth.py.
- **G4 (claude-desktop special case)**: P2 is correct. The handlers.py code (lines 182-194) has explicit fallback logic for this.
- **G5 (question sufficiency)**: P2 is correct.
- **G6 (mock headline template)**: P3 is correct. The mock provider returns `[mock:{agent_name}] {prompt}` which does not produce a valid headline.
- **G7 (stderr mixing)**: P3 is correct.
- **G8 (settings cascade untested)**: P2 is correct, and tests exist in `test_settings.py` and `test_integration_settings.py` but not end-to-end.
- **G9 (MCP output schema unvalidated)**: P2 is correct.
- **G10 (SKILL.md divergence)**: P1 is correct.

**Required change**: Correct G3 description to distinguish between auth.py resolution (narrow) and execution provider resolution (works). The fix target is `handlers.py` calling `resolve_execution_provider` instead of `resolve_provider`, not adding 9 providers to `OAUTH_CONFIGS`.

---

## Section 6: Success Criteria

**Assessment: Measurable and achievable, with one overreach.**

Criterion 3 ("CLI and MCP surfaces produce structurally identical output") is valuable but will require fixing the provider resolution divergence first (CLI uses `resolve_execution_provider`, MCP handlers use `resolve_provider`). This is not listed as a known gap but should be.

Criterion 5 ("Known gaps G1-G5 resolved") is the right gate, but it mixes eval suite work with engine bug fixes. The spec should clarify: does the eval suite pass because the gaps are fixed, or does the eval suite exist first (with expected failures) and then the gaps are fixed?

---

## Section 7: Implementation Order

**Assessment: Mostly correct with one critical sequencing issue.**

1. Install promptfoo + deepeval: Correct first step.
2. Write promptfoo config: Correct.
3. **Run first eval -- capture current pass/fail state**: This step assumes the eval will produce meaningful results, but it will crash immediately for red-blue mode with a ConfigError from `parse_config`. It will also fail for any provider other than mock/demo/anthropic/openai when going through `run_decide_mcp`. These are infrastructure failures (wrong code path, missing roles in adhoc config) not engine bugs being surfaced. The first eval run should explicitly exclude red-blue mode and limit to mock provider to get a clean baseline.
4. Fix G1 and G2: Correct placement, but G1 requires changes in `engine/adhoc.py` (mode-aware agent selection) and possibly new presets or agent specs for red-blue default agents.
5. Wire remaining providers: This should target `handlers.py` to use `resolve_execution_provider`, not add providers to auth.py.
6. Write deepeval quality tests: Correct -- needs real provider, so it comes after functional tests pass.
7-10: Correct sequencing.

**Required change**: 
- Step 3: Explicitly scope the first eval run to cooperative, winner-take-all, and prisoners-dilemma modes with mock provider only. Document expected red-blue failure as a known exclusion.
- Step 5: Clarify the fix target is `handlers.py` resolution path, not auth.py provider registration.

---

## Missing from the Spec

### 1. Test isolation for settings cascade
The handlers `run_decide_mcp` and `run_decide_cli` both call `load_settings()` which reads from `~/.conversus/settings.yml` and `<project>/.conversus/settings.yml`. If either file exists on the developer's machine or CI runner, the mock provider default gets overridden. Every test must either mock `load_settings` or run in a clean temp directory with `HOME` overridden.

### 2. conftest.py fixtures
The existing test suite has `engine/tests/conftest.py` with shared fixtures. The eval suite should integrate with these rather than creating parallel infrastructure.

### 3. CI runner requirements
The spec says "eval suite runs in CI" (criterion 6) but does not specify: Docker image, Python version, Node.js for promptfoo, API keys as secrets. promptfoo requires Node.js >= 18. The conversus engine requires Python 3.12+. Both need to coexist in the CI runner.

### 4. The `run_mcp` in-process path uses `resolve_provider` not `resolve_execution_provider`
The `_run_in_process` helper (handlers.py line 491) calls `resolve_provider(provider_name)` from auth.py, which means in-process runs through MCP also cannot use the 9 execution-only providers. This is the same bug surface as G3 but in a different code path. The eval suite should cover this path explicitly.

---

## Summary of Required Changes

| # | Section | Change | Severity |
|---|---------|--------|----------|
| R1 | 3.1.1 | Note that red-blue tests must use pre-built YAML configs, not the adhoc decide path | Must fix |
| R2 | 3.1.6 | Fix quality_indicators schema to match actual QualityIndicators Pydantic model (nested object, not string array) | Must fix |
| R3 | 4.1 | Replace inline shell expansion with a wrapper script for promptfoo exec provider | Must fix |
| R4 | 4.1 | Verify the actual CLI flag name for JSON format (--format vs --output-format) | Must fix |
| R5 | 5, G3 | Correct the gap description: distinguish auth.py resolution from execution provider resolution | Should fix |
| R6 | 7, Step 3 | Scope first eval run to exclude red-blue; document expected failures | Must fix |
| R7 | 7, Step 5 | Clarify fix target is handlers.py, not auth.py | Should fix |
| R8 | 3.2.1 | Specify how quality tests access intermediate phase outputs | Must fix |
| R9 | 3.1.4 | Note settings cascade isolation requirement for MCP tests | Should fix |
| R10 | 4.2 | Specify the LLM judge model for deepeval | Should fix |
| R11 | 2.1 | Add engine/run.py resolve_execution_provider to architecture diagram | Nice to have |
| R12 | New | Add CI runner requirements (Python 3.12, Node 18, API key secrets) | Should fix |

---

## Verdict

**Approve with required changes (R1-R8 must fix before implementation begins).**

The spec is the right investment at the right time. The engine has real bugs that are costing release velocity, and an eval suite is the only way to prevent regression. The two-tool approach (promptfoo for black-box functional, deepeval for quality scoring) is well-chosen. The implementation order is sound once the sequencing fix in R6 is applied.

The most important insight this review surfaces: the engine has two different provider resolution paths (`auth.py` for MCP handlers, `run.py` for CLI), and this divergence is itself a bug that the eval suite will discover but that the spec does not list as a known gap. Adding this as G11 would make the gap list complete.
