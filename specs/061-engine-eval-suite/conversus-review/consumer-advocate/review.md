# Consumer Advocate Review: Spec 061 — Engine Eval Suite

**Reviewer role**: Consumer advocate — representing Claude Desktop, Claude Code, OpenCode, Codex Desktop, CI/CD pipelines, Cowork, claude.ai web skills, and the future paid API tier.

**Reviewed document**: `specs/061-engine-eval-suite.md`

**Verdict**: The spec is a strong foundation that correctly diagnoses the core problem (untested engine edges masked by flexible LLM consumers). It covers the four primary modes, both CLI and MCP surfaces, and establishes a credible two-layer eval framework. However, it has significant gaps from the consumer perspective: several real consumers are missing entirely, the composability contract is under-tested for the hardest integration patterns, consumer-specific failure modes are only partially addressed, and the paid tier transition receives a single sentence of motivation with zero concrete test coverage. The spec needs a second pass before it can claim to "validate composability" across all consumer surfaces.

---

## 1. Does the spec test what consumers actually need?

### 1.1 Correct: mode matrix and provider matrix are the right starting dimensions

The mode matrix (section 3.1.1) and provider matrix (section 3.1.2) establish the two axes that matter most to every consumer. Any consumer calling `conversus_decide` needs to trust that cooperative, winner-take-all, red-blue, and prisoners-dilemma all produce valid output. This is the right foundation.

### 1.2 Gap: four modes are tested; eight are advertised

The Desktop Extension manifest (`desktop-extension/manifest.json`) advertises **8 game theory modes**: cooperative, winner-take-all, prisoners-dilemma, red-blue, negotiation, resource-allocation, fair-division, and mechanism-design. The CLI (section 3.1.3) only accepts four. The mode matrix (section 3.1.1) lists all eight but marks four as "(if supported in decide)".

This ambiguity is consumer-hostile. A Desktop Extension user sees "8 game theory modes" in the extension description, tries `negotiation`, and gets... what? An unknown-mode error? A silent fallback to cooperative? The eval suite needs to make this explicit:

- **Add a test**: for each of the 4 extended modes, calling `conversus decide` with that mode produces either a clear "mode not yet supported in ad-hoc mode, use conversus_run with a config file" message **or** valid output. The current spec leaves the expected behavior unspecified.
- **Add a consistency test**: the set of modes accepted by CLI `decide` must be a documented subset of the modes accepted by `conversus_run` (config-based). If a mode is accepted by `run` but not `decide`, the error message from `decide` must reference `run` as the alternative.

### 1.3 Gap: consumer output expectations differ by surface but tests only check one schema

Section 3.1.6 defines the JSON output schema with five fields: `headline`, `summary`, `full_analysis`, `quality_indicators`, `debate_transcript`. Section 3.1.4 checks MCP Pydantic models with different shapes: `ValidateResult`, `RunResult`, `DecideResult`, `CostEstimate`.

But no test verifies that the CLI JSON output is derivable from the MCP Pydantic models. The CLI `--format json` output comes from `parse_synthesis()` which returns `ConversusOutput`, while MCP returns `DecideResult` which wraps `ConversusOutput` inside `.output`. A consumer switching from CLI to MCP (common for CI/CD pipelines migrating to programmatic integration) will hit a different schema. The spec should add an explicit **schema mapping test**: given the same question/mode/provider, CLI JSON output fields must be a strict subset of the MCP DecideResult.output fields, with documented field name mappings if any differ.

### 1.4 Gap: the SDK surface (engine.sdk.Deliberation) is completely absent

The engine has a typed Python SDK (`engine/sdk.py`) exposing `Deliberation`, `Result`, `ValidateResult`, `validate()`, and `classify()`. This is the primary consumer surface for CI/CD pipelines and any programmatic Python integration. The spec does not mention it once. The existing `test_sdk.py` tests exercise the SDK, but the eval suite should include the SDK in its cross-surface parity tests (section 3.3.3). Specifically:

- `Deliberation(question="Q", provider="mock", mode="cooperative").run()` must produce a `Result` whose fields structurally match the CLI JSON output and the MCP `DecideResult.output`.
- `validate(config_path)` must produce a `ValidateResult` whose fields structurally match `ValidateResult` from the MCP surface.
- Event callbacks (`d.on(PhaseStarted, ...)`) must fire for all phases in the same order as the events emitted during CLI and MCP runs.

---

## 2. Is the composability contract (section 2.2) tested end-to-end?

### 2.1 Correct: the seven axes are well-chosen

Provider, mode, output format, max launches, presets, target documents, and settings cascade cover the configuration space that matters. This is a good enumeration.

### 2.2 Gap: combinatorial coverage is declared but not specified

The spec says "validates that each configuration axis works independently **and in combination**" but all concrete tests are single-axis. There are no cross-axis tests, for example:

- Provider=anthropic + mode=red-blue + format=json (the Desktop user who configured anthropic as default and asked for a red-blue deliberation)
- Settings cascade provider override + CLI mode override (project settings say provider=anthropic, CLI flag says mode=winner-take-all)
- Target documents + preset agents (custom config with target files and preset agents together)

The spec should define a small **combinatorial smoke matrix** (perhaps 8-12 combinations) that covers the most common consumer configurations. The pairwise testing technique would work well here: pick 2-3 values per axis and generate covering combinations.

### 2.3 Gap: settings cascade test (3.3.1) specifies the ordering but not the env var layer

The settings cascade in the actual code (`engine/settings.py`) has **five** levels, not four:

```
CLI flag > env var > project .conversus/settings.yml > global ~/.conversus/settings.yml > defaults
```

The spec's section 3.3.1 lists this correctly in the comment, but the test description says "set provider at each level and verifying which one wins" without specifying the env var level. The env var layer is critical because it is how **Claude Desktop Extension users** configure their provider (via `user_config` in manifest.json, which sets `CONVERSUS_DEFAULT_PROVIDER`). If the env var layer is not tested, the most common Desktop user path is untested.

The test should explicitly include:
1. Set `CONVERSUS_DEFAULT_PROVIDER=openai` as env var
2. Set `default_provider: anthropic` in project settings
3. Verify that env var wins over project settings
4. Set CLI flag `--provider mock`
5. Verify that CLI flag wins over env var

### 2.4 Gap: max_launches composability is specified but the overflow path is undertested

The spec tests "max launches exceeded" in section 3.1.7, but consumers need to know: when max_launches is set via settings cascade (e.g., project settings say `max_launches: 10`) and the ad-hoc `decide` command generates a config needing 9 launches, does it pass? What about 11? The settings cascade for `max_launches` is an integer, not a string, which means the env var parsing path (`CONVERSUS_MAX_LAUNCHES`) has a type coercion edge case. The spec should test:

- `CONVERSUS_MAX_LAUNCHES=15` (valid integer string) correctly overrides
- `CONVERSUS_MAX_LAUNCHES=abc` (invalid) falls through to the next cascade level with a warning, not a crash

The code in `engine/settings.py` lines 185-188 handles the invalid case, but this is not in the eval suite.

---

## 3. Are consumer-specific failure modes covered?

### 3.1 Claude Desktop Extension

**Partially covered.** The spec mentions Desktop in section 3.3.2 ("MCP tools, prompts, user_config env vars, OAuth login") and lists a test: "Start MCP server, call all 4 tools, verify responses." This is necessary but insufficient.

**Missing Desktop-specific failure modes:**

1. **Extension content scanner rejection**: The Desktop Extension has a prompt-content scanner that can reject prompts with instructional directives in the `user` role. The `mcp_server.py` code already uses a "role-split pattern" (assistant+user turn) in `design_deliberation()` and `analyze_documents()` to work around this. The eval suite should test that all 7 MCP prompts pass the content scanner. The spec does not test prompts at all.

2. **claude-desktop provider without MCP context**: When `provider=claude-desktop` but no MCP context is available (e.g., CLI invocation, not inside a Desktop MCP session), the handler falls back to `anthropic` credentials. This fallback is a consumer-facing behavior (Desktop users who later try CLI will hit it) and needs a test: `conversus decide "Q" --provider claude-desktop` from CLI should produce a clear error about MCP context OR successfully fall back to anthropic if credentials are available.

3. **user_config sensitive field handling**: The manifest declares `ANTHROPIC_API_KEY` as `sensitive: true`. The eval suite should verify that when this env var is set, it does not appear in any log output, error messages, or the `InvocationContext.env` debug snapshot.

4. **darwin-only compatibility**: The manifest declares `"platforms": ["darwin"]`. No test validates that the extension bundle or MCP server can be invoked on non-darwin platforms with a clear unsupported-platform message rather than a cryptic failure.

### 3.2 Claude Code (MCP + CLI + Skill)

**Partially covered.** The spec distinguishes three Claude Code integration modes (MCP, CLI, Skill) in section 3.3.2, which is correct.

**Missing Claude Code failure modes:**

1. **SKILL.md divergence (G10)**: Listed as a known gap but no concrete test is specified. The spec says "SKILL.md and engine implementations diverged -- no parity test" but the implementation order (section 7, step 9) defers it to last. The divergence test should be in the smoke suite, not deferred: parse the SKILL.md's example commands, run each one via CLI, and verify the exit code matches what the SKILL.md suggests. The `claude-code-plugin/skills/decide/SKILL.md` lists specific providers (`mock`, `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`) while `auth.py` only resolves `mock`, `demo`, `anthropic`, `openai`. This mismatch is the divergence and the test should catch it by attempting to resolve each SKILL.md-advertised provider.

2. **Claude Code session detection**: The engine has explicit Claude Code session detection (`engine/cli/context.py`) that checks `CLAUDECODE`, `CLAUDE_CODE`, `CLAUDE_CODE_ACTIVE` env vars and adjusts renderer and provider defaults. No eval tests exercise this detection with those env vars set. Add: run CLI with `CLAUDECODE=1` and verify `InvocationContext.is_claude_code_session` is True and renderer is not `tui`.

3. **Subprocess delegation for claude-code provider**: When Claude Code is used as a *provider* (not a host), the `ClaudeCodeProvider` uses `--dangerously-skip-permissions` for headless execution. The eval suite should verify this flag is present in the constructed argv and that the provider does not hang waiting for interactive permission prompts.

### 3.3 CI/CD Pipelines

**Weakly covered.** Section 3.3.2 lists "CLI, `--format json`, non-interactive" with assertions "No TTY, no prompts, exit codes." This is the right idea but too vague.

**Missing CI/CD failure modes:**

1. **Exit code semantics**: The engine has two exit code schemes (`interactive` and `governance`). CI/CD pipelines using conversus as a quality gate need governance exit codes (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE). The eval suite does not test governance exit codes at all. Add tests for `conversus governance ...` with the governance exit code scheme.

2. **No TTY, no prompts guarantee**: The question classifier has an `interactive` vs `non-interactive` mode. In `non-interactive` mode (all handler paths), insufficient questions are rejected without prompting. But what about `conversus login` in CI? The OAuth flow opens a browser and waits for input. The eval suite should verify that `conversus login anthropic` in a headless CI environment (no TTY, CI=true) produces a clear "OAuth login requires an interactive terminal" error rather than hanging.

3. **JSON output on stderr contamination**: Gap G7 notes "CLI `--format json` mixed with rich stderr on some error paths." The eval suite should add an explicit test: capture stdout and stderr separately, verify stdout is valid JSON and stderr contains only log-level messages (no Rich formatting that breaks log parsers).

4. **Structured output for CI consumption**: CI/CD pipelines need machine-parseable output. Test that `--format json` output can be piped to `jq` without errors for every success and failure path. The output schema test in 3.1.6 checks the happy path but not error paths (does `--format json` produce JSON even on failure, or does it fall back to plain text?).

### 3.4 OpenCode and Codex Desktop

**Not meaningfully covered.** Section 3.3.2 says "Same tool surface, different host" for both. This is accurate in theory (they use MCP or CLI) but ignores host-specific behaviors:

1. **OpenCode HTTP provider**: OpenCode has an HTTP server mode. The `OpenCodeProvider` in `engine/execution/providers/opencode.py` uses `opencode run "message"` for non-interactive execution. The eval suite should verify the argv construction and that the output parsing works with OpenCode's response format. Even if we cannot run a live OpenCode instance in CI, a mock-based unit test of argv construction and output parsing is essential.

2. **Codex provider specifics**: The `CodexProvider` exists in `engine/execution/providers/codex.py` but has no auth wiring (Gap G3). The eval suite lists G3 as a known gap but does not specify what "wiring remaining providers into auth resolver" means for Codex specifically. Does Codex need an API key? An environment variable? A host session? The eval should at minimum verify that `get_provider("codex")` returns a valid `ExecutionProvider` instance without crashing.

### 3.5 Cowork and claude.ai Web Skills

**Entirely absent.** The distribution strategy spec lists Cowork (same plugin format as Claude Code) and claude.ai web skills (SKILL.md format) as P1 and P2 distribution targets respectively. Neither appears in the consumer table (section 1) or the consumer-specific composition tests (section 3.3.2).

For Cowork, this matters because Cowork uses HTTP+OAuth transport for MCP (per the distribution strategy), not stdio. If the MCP server is only tested with stdio transport, the HTTP transport path is untested. Even if Cowork is not yet shipping, the eval suite should document it as a planned consumer and note which transport tests need to exist.

For claude.ai web skills, the SKILL.md format must pass Anthropic's review. No eval tests validate that the SKILL.md files in `claude-code-plugin/skills/` are syntactically valid and self-consistent.

---

## 4. Does the spec account for the paid tier transition?

### 4.1 The spec mentions the paid tier exactly twice, tests it zero times

Section 1.1 says: "The OSS engine is the foundation for the paid tier." Section 1's table lists "Paid tier (future) | API server | HTTP, structured JSON." That is the extent of paid tier coverage.

**Missing paid tier considerations:**

1. **HTTP surface testing**: The paid tier uses an HTTP API server. The current eval suite tests CLI (subprocess) and MCP (handler functions). There is no HTTP surface. Even without the paid tier shipping, the eval suite should define the HTTP surface test shape so it can be added later. At minimum, document the expected HTTP endpoint contract (e.g., POST /v1/decide with JSON body, returning DecideResult JSON) and add a placeholder test section.

2. **Free/paid tier boundary testing**: Spec 049 defines paid-tier tools (`conversus_score`, `conversus_solve`, etc.) that return `PAID_TIER_REQUIRED` errors when `conversus-solvers` is not installed. The eval suite should verify that calling a paid-tier tool without the paid package returns the correct structured error, not a crash. This is a consumer-facing behavior: a free-tier user seeing an error message suggesting they upgrade is a conversion funnel moment.

3. **Team deliberations and persistent history**: The paid tier plans include team deliberations and persistent history. The persistence infrastructure (`engine/persistence.py`) already exists for the free tier. The eval suite tests should verify that persistence works correctly (section 3.1.8 covers target documents but not output persistence) and that the persistence format is stable enough for the paid tier to build on. Add: verify that `persist_deliberation()` creates the expected directory structure and that `list_deliberations()` can read back what was persisted.

4. **Cost tracking for metering**: Spec 042 binding condition #5 requires per-execution cost telemetry (`Cost` dataclass with `input_tokens`, `output_tokens`, `usd`). The paid tier will need this for billing. The eval suite does not test that providers report cost data. Add: for every provider that supports cost reporting (anthropic, openai), verify that `ExecutionResult.cost` is populated after execution.

---

## 5. Missing consumers and integration patterns

### 5.1 Cursor, Windsurf, Zed, VS Code+Copilot

The distribution strategy lists these as MCP-compatible editors. They use the same stdio MCP transport as Claude Code. The eval suite should note them as MCP consumers and call out any known behavioral differences (e.g., Cursor has a 40-tool limit per the distribution strategy -- does conversus fit within that?). At minimum, add a test that counts the number of MCP tools exposed and asserts it is under the Cursor limit.

### 5.2 Python library consumers (direct import)

The SDK (`engine.sdk`) is a first-class consumer surface. Developers will `from engine import Deliberation` and call it from their own Python code. As noted in 1.4, this surface is entirely absent from the eval suite.

### 5.3 The .mcpb bundle as a distribution artifact

The Desktop Extension ships as a `.mcpb` bundle (ZIP archive). The eval suite does not test that the bundle can be built and that the entry point inside the bundle resolves correctly. Add: a build test that runs `desktop-extension/build.sh` and verifies the resulting `.mcpb` file contains all required files per the manifest.

---

## 6. Specific technical issues

### 6.1 The promptfoo config (section 4.1) has a quoting vulnerability

The exec provider template is:
```
exec:uv run conversus decide "{{prompt}}" --provider mock --mode cooperative --format json
```

If `{{prompt}}` contains double quotes, the shell command breaks. Promptfoo's exec provider may or may not handle shell escaping. The eval suite should either: (a) note that prompts must not contain shell-special characters, or (b) include a test with a question containing quotes and verify it does not crash.

### 6.2 Cross-surface parity test (3.3.3) is structurally sound but needs a concrete assertion

The spec says "Both must return the same JSON schema with the same fields." This is correct but the test should be concrete: define a Pydantic model that both CLI JSON and MCP DecideResult.output must validate against. The `ConversusOutput` model from `linter/output_contract.py` is the natural candidate. The test should be: CLI JSON parses into `ConversusOutput`, MCP `DecideResult.output` parses into `ConversusOutput`, both produce identical field sets.

### 6.3 Quality thresholds (section 3.2.1) may be too tight or too loose without baselines

The spec sets thresholds (0.6 to 0.8) for LLM-as-judge metrics but notes in 3.2.3 that baselines are saved "for each standard test question." The thresholds should be calibrated against the baselines, not set a priori. Recommend: run the quality suite once with anthropic provider, use the resulting scores as baseline, and set thresholds at baseline minus a regression margin (e.g., 0.1). This prevents the common failure mode of eval suites that are either always-green (thresholds too low) or perpetually-red (thresholds too high from the start).

### 6.4 Implementation order puts SKILL.md parity last (step 9) -- should be earlier

The SKILL.md divergence (G10) is a P1 gap that affects every Claude Code Skill user today. The implementation order puts it at step 9 (of 10). Consumers hitting this divergence right now are getting incorrect behavior. Recommend moving SKILL.md parity to step 4 or 5, immediately after fixing the P0 red-blue and P1 target-path bugs.

---

## 7. Summary of recommended additions

| Priority | Addition | Consumer impact |
|---|---|---|
| P0 | Add SDK surface (`engine.sdk.Deliberation`) to cross-surface parity tests | CI/CD, Python library consumers |
| P0 | Test all 5 settings cascade levels including env vars | Claude Desktop Extension users |
| P0 | Specify SKILL.md divergence test concretely, move earlier in implementation order | Claude Code Skill users |
| P1 | Add CI/CD-specific tests: governance exit codes, no-TTY login error, stderr contamination, JSON error output | CI/CD pipelines |
| P1 | Test the 4 extended modes (negotiation, resource-allocation, fair-division, mechanism-design) for clear error or valid output | Desktop Extension users who read the manifest |
| P1 | Add persistence round-trip tests (persist then list/read) | Paid tier foundation, all consumers with history |
| P1 | Add env var type coercion edge cases (`CONVERSUS_MAX_LAUNCHES=abc`) | Desktop Extension users who misconfigure settings |
| P2 | Add paid tier placeholder: HTTP surface shape, PAID_TIER_REQUIRED error test, cost telemetry verification | Future paid tier consumers |
| P2 | Add Cowork and claude.ai as planned consumers with transport notes | Non-technical users |
| P2 | Add MCP tool count assertion (Cursor 40-tool limit) | Cursor, Windsurf, Zed users |
| P2 | Add .mcpb bundle build test | Desktop Extension distribution |
| P3 | Add combinatorial smoke matrix (8-12 cross-axis combinations) | All consumers hitting unusual config combos |
| P3 | Add promptfoo shell-quoting test for questions with special characters | Eval suite reliability |
| P3 | Calibrate quality thresholds from baselines rather than setting a priori | Eval suite maintainability |

---

## 8. What the spec gets right

To be clear about the strengths:

- **The problem statement is exactly right.** 28 release candidates with bugs the engine could have caught is a compelling motivation. The observation that SKILL.md masks engine bugs by reimplementing the pipeline as prompt instructions is sharp and important.
- **The layered eval architecture (promptfoo for functional, deepeval for quality) is the right design.** Functional tests catch structural regressions cheaply on every commit; quality tests catch semantic regressions at higher cost on releases.
- **The known gaps table (section 5) is honest and specific.** G1-G10 are real bugs that real consumers have hit. Listing them with severity and affected surface is consumer-friendly.
- **The test markers (section 4.3) correctly separate smoke/eval/live/integration.** Every commit gets smoke; every release gets quality. This is the right economics.
- **The implementation order is practical.** Starting with promptfoo + smoke tests, capturing the current pass/fail state, then fixing bugs and re-running is the right sequence. Ship the eval harness first, then fix what it catches.

The spec is a solid 70% of what consumers need. The remaining 30% is the SDK surface, the env var cascade layer, CI/CD-specific failure modes, SKILL.md parity, and paid tier groundwork.
