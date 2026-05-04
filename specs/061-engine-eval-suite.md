# Spec 061: Engine Eval Suite — Composable Deliberation Testing

**Feature ID**: `061-engine-eval-suite`
**Created**: 2026-04-16
**Status**: Active (steps 1-4 complete, 3 gaps fixed, 24/24 eval baseline)
**Depends On**: `042-execution-providers`, `050-cascading-settings`, `055-capability-registry`
**Motivated By**: Extension builds breaking on untested engine; need to validate all edges before building consumer orchestration and paid tier

---

## 1. Problem

Conversus has one deliberation engine but multiple consumers call it through different surfaces:

| Consumer | Surface | Transport |
|---|---|---|
| Claude Desktop | MCP server (MCPB bundle) | stdio, `conversus_decide` / `conversus_run` tools |
| Claude Code | MCP server or CLI or Skill | stdio or subprocess or Agent dispatch |
| OpenCode | MCP server or CLI | stdio or subprocess |
| Codex Desktop | MCP server or CLI | stdio or subprocess |
| Direct user | CLI | `uv run conversus decide` |
| CI/CD | CLI (headless) | subprocess, `--format json` |
| Paid tier (future) | API server | HTTP, structured JSON |

**No eval suite validates the engine across these surfaces.** The Desktop extension has shipped 28 release candidates with bugs that would have been caught by running the engine once:

- `red-blue` mode broken in `decide` (default presets lack `role: red`)
- Target file path resolution doubles paths
- CLI advertises 12+ providers; auth resolver knows 3
- Question sufficiency gate rejects reasonable inputs
- `claude-desktop` provider not wired in auth resolver

The SKILL.md agent-dispatch implementation works because Claude is flexible — it masks engine bugs by reimplementing the pipeline as prompt instructions. This creates a false sense of health.

### 1.1 Strategic context

The OSS engine is the foundation for the paid tier. Every consumer (Desktop, Claude Code, OpenCode, Codex) must compose the same atomic capabilities reliably. Testing the engine's edges now prevents compounding defects when paid features (hosted API, team deliberations, persistent history) are built on top.

---

## 2. Architecture Under Test

### 2.1 Engine layers

```
┌─────────────────────────────────────────────┐
│  Consumers                                   │
│  Claude Desktop · Claude Code · OpenCode     │
│  Codex Desktop · CLI · CI/CD · Paid API      │
├─────────────────────────────────────────────┤
│  Surfaces                                    │
│  MCP Server  ·  CLI  ·  Skill  ·  HTTP API   │
│  (mcp_server.py) (engine/cli/) (SKILL.md)    │
├─────────────────────────────────────────────┤
│  Handlers                                    │
│  engine/handlers.py                          │
│  validate_mcp · run_mcp · run_decide_mcp     │
│  login_mcp                                   │
├─────────────────────────────────────────────┤
│  Engine Core                                 │
│  engine/config.py    — YAML parsing          │
│  engine/phases.py    — 5-phase pipeline      │
│  engine/dispatch.py  — agent dispatch        │
│  engine/execution/   — provider abstraction  │
│  engine/adhoc.py     — ad-hoc config gen     │
│  engine/auth.py      — credential resolution │
│  engine/events.py    — pipeline events       │
│  engine/persistence.py — output storage      │
│  engine/results.py   — Pydantic models       │
├─────────────────────────────────────────────┤
│  Providers                                   │
│  mock · anthropic · openai · gemini · ollama │
│  claude-code · aider · opencode · codex      │
│  copilot · pi · claude-desktop · demo        │
├─────────────────────────────────────────────┤
│  Config & Presets                             │
│  presets/ · schema/ · templates/             │
│  .conversus/settings.yml                     │
└─────────────────────────────────────────────┘
```

### 2.2 Composability contract

Every consumer must be able to configure:

1. **Provider** — which LLM backend to use
2. **Mode** — which game theory mode (8 total)
3. **Output format** — JSON, rich, structured Pydantic
4. **Max launches** — cost ceiling
5. **Presets** — which agent personas
6. **Target documents** — files to feed into agent context
7. **Settings cascade** — CLI flag → env var → project settings → global settings → defaults

The eval suite validates that each configuration axis works independently and in combination.

---

## 3. Test Dimensions

### 3.1 Functional (promptfoo — outside-in)

Black-box tests through CLI and MCP surfaces. Each test runs the actual command/tool and validates output.

#### 3.1.1 Mode matrix

Every mode must produce valid output with mock provider:

| Mode | Expected behavior | Key assertion |
|---|---|---|
| `cooperative` | Agents seek convergence | Synthesis present, no "Error:" |
| `winner-take-all` | Synthesis picks one winner | Output contains winner declaration |
| `prisoners-dilemma` | Agents choose cooperate/defect | Payoff structure in output |
| `red-blue` | Asymmetric attack/defend | Red and blue agent roles present |
| `negotiation` | Offers and counteroffers | (if supported in decide) |
| `resource-allocation` | Budget competition | (if supported in decide) |
| `fair-division` | Fairness criteria | (if supported in decide) |
| `mechanism-design` | Incentive structures | (if supported in decide) |

#### 3.1.2 Provider matrix

Each provider must instantiate without error (mock credentials where needed):

| Provider | Auth method | Expected |
|---|---|---|
| `mock` | None | Instant synthetic output |
| `demo` | None (alias) | Same as mock |
| `anthropic` | `ANTHROPIC_API_KEY` | Real API call |
| `openai` | `OPENAI_API_KEY` | Real API call |
| `gemini` | `GOOGLE_API_KEY` | Real API call |
| `ollama` | `OLLAMA_BASE_URL` | Local server call |
| `claude-code` | Host session | Subprocess delegation |
| `claude-desktop` | MCP context | Sampling delegation |
| `aider` | Host session | Subprocess delegation |
| `opencode` | Host session | Subprocess delegation |
| `codex` | Host session | Subprocess delegation |
| `copilot` | Host session | Subprocess delegation |
| `pi` | Host session | Subprocess delegation |

**Known gap (G11, FIXED)**: MCP handlers called `resolve_provider` (auth.py, 3 providers) instead of `resolve_execution_provider` (run.py, 13+ providers). Fixed: both `run_decide_mcp` and `_run_in_process` now use `resolve_execution_provider`.

**Provider test taxonomy** (5 levels, test each provider at the appropriate level):

1. **Import** — class loads without error
2. **Instantiate** — constructor succeeds with default args
3. **Auth-resolve** — `resolve_execution_provider(name)` returns a provider
4. **Dispatch** — `execute(task)` returns an `ExecutionResult` (mock credentials)
5. **Error-message quality** — auth failures produce actionable messages naming the provider

#### 3.1.3 CLI surface tests

```
conversus decide <question> --provider mock --mode <mode> --format json
conversus decide <question> --provider mock --mode <mode> --format rich
conversus run <config.yml> --provider mock
conversus validate <config.yml>
conversus status
conversus login <provider>  (mock — should succeed or no-op)
conversus logout <provider>
conversus context
```

#### 3.1.4 MCP surface tests

Call each MCP tool handler directly (no stdio server needed):

```python
from engine.handlers import validate_mcp, run_mcp, run_decide_mcp, login_mcp

# validate
result = validate_mcp(config_yaml, question="")
assert result.valid is True
assert len(result.errors) == 0

# decide
result = run_decide_mcp("Should we use X or Y?", "mock", "cooperative", 20)
assert result.sufficient is True
assert result.output is not None

# run (validate-only mode)
result = run_mcp(config_yaml, output_path="", provider="")
assert result.validated is True

# run (in-process mode)
result = run_mcp(config_yaml, output_path="", provider="mock")
assert result.output is not None
```

#### 3.1.5 Config parsing tests

| Config variant | Expected |
|---|---|
| Minimal (question + mode + agents) | Valid |
| With `target:` file list | Valid, files resolved |
| With `target:` — file missing | Error: file not found |
| With custom agent (inline prompt) | Valid |
| With preset agent | Valid, preset loaded |
| With arbiter | Valid |
| With `iterations: 3` | Valid, cost estimate reflects 3× |
| With `rounds: 2` | Valid |
| Invalid YAML syntax | Error: parse failure |
| Unknown mode | Error: invalid mode |
| Empty question | Error: question required |
| Missing agents | Error: agents required |

#### 3.1.6 Output schema validation

JSON output from `--format json` must match:

```json
{
  "headline": "<string, non-empty>",
  "summary": "<string, non-empty>",
  "full_analysis": "<string>",
  "quality_indicators": {
    "agent_count": "<int>",
    "mode": "<string>",
    "phases_completed": "<int>",
    "cross_reviews_performed": "<int>",
    "genuine_disagreements_surfaced": "<int>",
    "genuine_disagreements_surviving": "<int>"
  },
  "debate_transcript": "<string>"
}
```

Note: `quality_indicators` is a nested `QualityIndicators` Pydantic model, not a string array. All fields are deterministically extracted from the synthesis text.

MCP tool output must match Pydantic models:

- `ValidateResult(valid, errors, cost_estimate, question_classification)`
- `RunResult(mode, validated, errors, cost_estimate, output)`
- `DecideResult(sufficient, classification, output, cost_estimate, errors)`
- `CostEstimate(total_launches, per_phase)`

#### 3.1.7 Error handling tests

| Scenario | Expected |
|---|---|
| Provider not authenticated | Clear error message naming the provider |
| Provider API returns error | Graceful failure, partial output preserved |
| Max launches exceeded | Refused before execution, cost estimate shown |
| Question too short (1-2 words) | Rejected with improvement suggestion |
| Question adequate (10+ words) | Accepted |
| Config references nonexistent preset | Error: preset not found |
| Network timeout during API call | Timeout error, no hang |

#### 3.1.8 Target document tests

| Scenario | Expected |
|---|---|
| Single target file (exists) | Content fed to all agents |
| Multiple target files (all exist) | All content fed |
| Target file missing | Error with resolved path |
| Target with relative path from config dir | Correct resolution |
| Target with absolute path | Correct resolution |
| Target with `~/` path | Expanded correctly |

#### 3.1.9 Multi-round, arbiter, and iteration tests

| Scenario | Config | Key assertion |
|---|---|---|
| rounds=2, disputes converge | `rounds: 2`, mock provider | `termination_reason: "converged"`, only 1 round executed |
| rounds=3, stagnation | `rounds: 3, stagnation: detect`, mock provider | `termination_reason: "stagnation"`, ≤3 rounds |
| rounds=5, max reached | `rounds: 5`, mock provider | `termination_reason: "max_rounds"` |
| iterations=3 | `iterations: 3`, mock provider | 3 cross-review/revision cycles, cost estimate reflects 3× |
| arbiter trigger=always | `arbiter: {trigger: always}`, mock | Phase 6 runs, arbitration/ dir created |
| arbiter trigger=disputes_remain, no disputes | Mock (converged) | Phase 6 skipped |
| arbiter influence=binding vs advisory | Config variants | Output headings change per influence level |

Priority: P0 for rounds=2 convergence and rounds=3 stagnation. P1 for arbiter and iterations.

#### 3.1.10 Extended mode tests

The 4 extended modes must produce either valid output or a clear, documented error — not "(if supported in decide)":

| Mode | Expected | Pre-implementation: verify empirically |
|---|---|---|
| `negotiation` | Valid output with offers/counteroffers, or ConfigError with actionable message |
| `resource-allocation` | Valid output with budget structure, or ConfigError |
| `fair-division` | Valid output with fairness criteria, or ConfigError |
| `mechanism-design` | Valid output with incentive structure, or ConfigError |

Run each once with mock via adhoc path before writing test assertions.

### 3.2 Quality (deepeval — inside-out)

LLM-as-judge tests on actual deliberation output. Require a real provider (anthropic).

#### 3.2.1 Pipeline phase quality

| Metric | Criteria | Threshold |
|---|---|---|
| Review independence | Each agent's review is substantively different from others | 0.7 |
| Cross-review adversarial quality | Cross-reviews identify specific disagreements, not generic praise | 0.7 |
| Revision responsiveness | Revisions explicitly address cross-review challenges | 0.6 |
| Dispute specificity | Disputes name concrete disagreements with evidence | 0.7 |
| Synthesis grounding | Synthesis references specific claims from the pipeline record | 0.8 |

#### 3.2.2 Mode-specific quality

| Mode | Metric | Criteria |
|---|---|---|
| cooperative | Convergence quality | Synthesis identifies shared ground AND remaining tensions |
| winner-take-all | Decision commitment | Synthesis picks exactly one winner with explicit reasoning |
| red-blue | Adversarial coverage | Red team identifies at least 3 distinct attack vectors |
| prisoners-dilemma | Strategy clarity | Each agent's cooperate/defect choice is explicit with payoff reasoning |

#### 3.2.3 Regression baselines

For each standard test question, save the first passing output as a baseline. Future runs compare against the baseline using:

- Structural similarity (same phases, same agent count)
- Semantic similarity (embedding distance < threshold)
- Quality non-regression (LLM judge score >= baseline score)

### 3.3 Composition (integration tests)

Tests that verify the composability contract across surfaces.

#### 3.3.1 Settings cascade

```
CLI flag > env var > project .conversus/settings.yml > global ~/.conversus/settings.yml > defaults
```

Each level must override the one below it. Test by setting provider at each level and verifying which one wins.

#### 3.3.2 Consumer-specific composition

| Consumer | Required capabilities | Test |
|---|---|---|
| Claude Desktop | MCP tools, prompts, user_config env vars, OAuth login | Start MCP server, call all 4 tools, verify responses |
| Claude Code (MCP) | Same as Desktop minus prompts | Register as MCP server, call tools |
| Claude Code (CLI) | `conversus decide/run/validate` | Subprocess calls, JSON output parsing |
| Claude Code (Skill) | Agent dispatch, YAML config | Skill invocation (future — agent fallback) |
| OpenCode | MCP or CLI | Same tool surface, different host |
| Codex Desktop | MCP or CLI | Same tool surface, different host |
| CI/CD | CLI, `--format json`, non-interactive | No TTY, no prompts, exit codes |

#### 3.3.3 Cross-surface parity

The same question + mode + provider must produce structurally identical output regardless of surface:

```
CLI:  uv run conversus decide "Q" --provider mock --mode cooperative --format json
MCP:  run_decide_mcp("Q", "mock", "cooperative", 20)
SDK:  Deliberation("Q", provider="mock", mode="cooperative").run()
```

All three must return the same JSON schema with the same fields. Assert inner content parity (headline, summary, full_analysis, quality_indicators), not wrapper type identity. Content may differ (separate runs) but structure must match.

**Settings cascade isolation** (P0 infrastructure prerequisite): A `clean_settings` conftest fixture must isolate HOME and project-level settings before any eval runs. `run_decide_mcp` treats `provider="mock"` as "not explicitly set" — the cascade can silently override it. The fixture must clear `CONVERSUS_*` env vars and create a temp HOME.

**`conversus status` verification**: Section 3.1.3 lists `conversus status` as a test target. This command must be confirmed to exist and its output contract specified, or removed from the test list.

---

## 4. Eval Framework

### 4.1 Promptfoo (functional layer)

Uses a Python custom provider (`evals/provider.py`) to avoid shell quoting issues with `exec:` providers. Each provider instance is configured with a mode via `config.mode`.

```yaml
# evals/promptfooconfig.yaml
providers:
  - id: "file://provider.py"
    label: cooperative-mock
    config: { mode: cooperative, provider: mock }
  - id: "file://provider.py"
    label: wta-mock
    config: { mode: winner-take-all, provider: mock }
  - id: "file://provider.py"
    label: pd-mock
    config: { mode: prisoners-dilemma, provider: mock }
  - id: "file://provider.py"
    label: redblue-mock
    config: { mode: red-blue, provider: mock }

tests:
  - description: "Standard tech decision question"
    vars:
      prompt: "Should we use Postgres or MongoDB for our metadata store?"
    assert:
      - type: is-json
      - type: javascript
        value: |
          const d = JSON.parse(output);
          return d.headline !== undefined &&
            d.summary !== undefined &&
            d.full_analysis !== undefined &&
            d.quality_indicators !== undefined &&
            d.debate_transcript !== undefined;
      - type: javascript
        value: |
          const d = JSON.parse(output);
          return typeof d.quality_indicators === 'object' &&
            typeof d.quality_indicators.agent_count === 'number' &&
            typeof d.quality_indicators.phases_completed === 'number';
      - type: not-contains
        value: "\"error\": true"
```

Run: `npx promptfoo eval -c evals/promptfooconfig.yaml`

Current baseline: **24/24 PASS** (4 modes × 6 test cases).

### 4.2 DeepEval (quality layer)

Quality tests use `run_pipeline` (not `run_decide_mcp`) to access intermediate phase outputs. The pipeline returns events from which per-phase artifacts can be read.

```python
# engine/tests/test_evals.py
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval

from engine.phases import run_pipeline
from engine.config import parse_config

SYNTHESIS_QUALITY = GEval(
    name="Synthesis Grounding",
    criteria="""The synthesis must:
    1. Reference specific claims from individual agent reviews
    2. Acknowledge where agents disagreed
    3. Provide a clear verdict or recommendation
    4. Not introduce claims absent from the pipeline record
    Score 0 if verdict is missing. Score 0.5 if verdict exists but
    doesn't reference the debate. Score 1 if fully grounded.""",
    threshold=0.7,  # Calibrate from baseline: set to baseline - 0.1
)

@pytest.mark.eval
class TestDeliberationQuality:
    def test_cooperative_synthesis_quality(self):
        # Use run_pipeline for intermediate artifact access
        config = parse_config("path/to/test-config.yml")
        provider = resolve_execution_provider("anthropic")
        result = asyncio.run(run_pipeline(config, provider, NullEmitter()))
        # Read synthesis from output directory
        synthesis = (config.output_dir / "summary" / "final.md").read_text()
        test_case = LLMTestCase(
            input=config.question,
            actual_output=synthesis,
        )
        assert_test(test_case, [SYNTHESIS_QUALITY])
```

**Threshold calibration**: Run quality suite once with anthropic, use scores as baseline, set thresholds at `baseline - 0.1` margin. Do not guess thresholds a priori.

**LLM judge**: Quality tests require LLM judge credentials (ANTHROPIC_API_KEY or OPENAI_API_KEY). Judge model selected during calibration.

Run: `uv run deepeval test run engine/tests/test_evals.py`

### 4.3 Test markers

| Marker | What it runs | When to use |
|---|---|---|
| `pytest.mark.smoke` | Mock provider, all modes, structural only | Every commit |
| `pytest.mark.eval` | Real provider, quality metrics | Pre-release |
| `pytest.mark.live` | Real provider, full pipeline | Manual |
| `pytest.mark.integration` | Cross-surface parity | Pre-release |

---

## 5. Known Gaps (pre-eval findings)

These were discovered during spec research and should be the first eval failures to fix:

| # | Gap | Severity | Surface | Status |
|---|---|---|---|---|
| G1 | `red-blue` mode fails in `decide` — default presets lack `role: red/blue` | P0 | CLI, MCP | **FIXED** — adhoc uses red-team/blue-team presets with role assignment |
| G2 | Target path resolution doubles relative paths | P1 | CLI, MCP | Open |
| G3 | MCP handlers used `resolve_provider` (auth.py, 3 providers) instead of `resolve_execution_provider` (run.py, 13+ providers). Fix target: `handlers.py`, not `auth.py`. | P1 | MCP | **FIXED** (see G11) |
| G4 | `claude-desktop` provider not in auth resolver (only in handlers.py special case) | P2 | MCP | Open |
| G5 | Question sufficiency gate rejects short but clear questions | P2 | CLI, MCP | Open |
| G6 | Mock synthesis output unparseable by `parse_synthesis` — smoke tier tested error-recovery path | P0 | CLI, MCP | **FIXED** — mock returns structured markdown for synthesis phase |
| G7 | CLI `--format json` mixed with rich stderr on some error paths | P3 | CLI | Open |
| G8 | Settings cascade untested end-to-end | P2 | All | Open |
| G9 | MCP tool output schema not validated against Pydantic models in CI | P2 | MCP | Open |
| G10 | SKILL.md and engine implementations diverged — no parity test | P1 | Skill | Open |
| G11 | Dual provider resolution path: `resolve_provider` (auth.py) vs `resolve_execution_provider` (run.py). Both `run_decide_mcp` and `_run_in_process` affected. | P1 | MCP | **FIXED** — handlers.py now uses `resolve_execution_provider` |
| G12 | `VALID_PROVIDERS` in `config.py` hardcoded to `("anthropic", "openai")`. YAML configs reject all other providers at parse time. CLI `--provider` bypasses this. | P1 | CLI (run), MCP (run) | Open |

---

## 6. Success Criteria

1. **All 4 primary modes** pass smoke tests with mock provider (0 errors, valid JSON) — **ACHIEVED** (24/24 PASS)
2. **All registered providers** resolve via `resolve_execution_provider` without import errors — **ACHIEVED** (13/13 resolve)
3. **CLI, MCP, and SDK surfaces** produce structurally identical output for the same input — **NOT ACHIEVABLE until step 11 lands** (engine-first skill is the prerequisite for cross-surface parity tests in step 12; per the strip-script-061-substeps deliberation 2026-05-01, this dependency is now explicit)
4. **Quality metrics** score >= baseline - 0.1 on synthesis grounding with anthropic provider
5. **Known gaps G1, G3/G11, G6** resolved and covered by regression tests — **ACHIEVED** (3/12 fixed)
6. **Eval suite runs in CI** — smoke tests on every push, quality evals on release tags
7. **Baseline snapshots** saved for 5 standard test questions across all modes
8. **Mock provider exercises production parsing path** — `parse_synthesis` succeeds on mock output — **ACHIEVED**

---

## 7. Implementation Order

**Progress (2026-05-03)**: Steps 1-4 complete (smoke baseline). Steps 9 (PR #100), 10 annotation only (PR #101 + #109), 14a persistence sub-item (PR #106) complete. Step 13 DONE WITH OPEN GAPS (PR #102 closed the iterations=3 dispatch/naming/events tests; the §3.1.9 cost estimate and influence output heading sub-rows are open and tracked as GitHub issues per the strip-script-061-substeps deliberation 2026-05-01).

**Open**: Steps 5, 6, 7, 8, 11, 12, 14b (CI/CD exit codes — blocked on spec 048's gate command), 14c (combinatorial matrix). Step 12 is BLOCKED on step 11; SC #3 (composability invariants verified) is unreachable until step 11 lands.

**P1 open bugs**: G2 (target path doubling), G12 (VALID_PROVIDERS hardcoded). Both gate step 6 closure.

1. ~~Install promptfoo + deepeval, create `evals/` directory~~ **DONE**
2. ~~Write promptfoo config — Python custom provider, 4 modes × 6 tests~~ **DONE** (24/24 PASS)
3. ~~Run first eval — capture baseline pass/fail~~ **DONE**
4. ~~Fix G1 (red-blue presets), G6 (mock synthesis), G11 (provider resolution)~~ **DONE**
5. **SKILL.md parity test** — parse examples, verify provider list, run each via CLI
6. **Fix G2** (target path doubling) and **G12** (VALID_PROVIDERS hardcoded) — re-run evals
7. **Write deepeval quality tests** — use `run_pipeline` for intermediate artifacts. Calibrate thresholds from first baseline run (baseline - 0.1 margin).
8. **Save baseline snapshots** for 5 standard test questions across all modes
9. ~~**Settings cascade tests** — provider key at all 5 levels, env var type coercion. Requires `clean_settings` conftest fixture (P0 infrastructure).~~ **DONE** (PR #100): 14 tests in `TestProviderAllFiveLevels` + `TestEnvVarTypeCoercion` + `TestCleanSettingsFixtureInvariants`; `clean_settings` fixture at `engine/tests/conftest.py:81`; lockstep test against `engine/settings._ENV_VAR_FOR_FIELD` prevents env-var drift.
10. ~~**Add eval commands to CI workflow** — specify runner requirements: Python 3.12, Node 22 LTS (spec said Node 18 — Node 18 EOL April 2025; Principle XIV deprecation discipline applies), API key secrets provisioning~~ **DONE**: PR #83 established the smoke tier (mock, every push); PR #101 added the `quality` tier (Ollama, dispatch+tags) and `deepeval` tier (Anthropic judge, dispatch+tags) and `workflow_dispatch` inputs (`run_ollama`, `run_deepeval`) and the `ANTHROPIC_API_KEY` secret guard. Annotation correction per the strip-script-061-substeps deliberation 2026-05-01.
11. **Build engine-first skill** wrapping CLI (replaces agent-dispatch SKILL.md). **OPEN** (issue #111). Blocks step 12 + SC #3.
12. **Cross-surface parity tests** — CLI vs MCP vs SDK output comparison (inner content parity). **BLOCKED on step 11**.
13. **Multi-round, arbiter, and iteration tests** — rounds=2 convergence, rounds=3 stagnation, arbiter trigger conditions, iterations=3 cycle count. **DONE WITH OPEN GAPS** (PR #102 closed three sub-rows; two §3.1.9 sub-rows open per the strip-script-061-substeps deliberation 2026-05-01):
    - rounds=2 convergence: `test_pipeline_result_has_round_fields` (rounds=2, [2,0] → `termination_reason="converged"`) — DONE.
    - rounds=3 stagnation: `test_stagnation_detection` (rounds=3, [2,2] → `termination_reason="stagnation"`) — DONE.
    - arbiter triggers: `test_always_trigger`, `test_disputes_remain_trigger_with_disputes`, `test_disputes_remain_trigger_no_disputes` — DONE.
    - iterations=3 dispatch/naming/events: PR #102 — `test_three_iterations_dispatch_counts` / `_revision_naming` / `_events` pin 6 cross-reviews, 6 revisions, revision.md/_2/_3 naming. DONE.
    - **OPEN** (issue #109): §3.1.9 `iterations=3` cost estimate assertion (`TestCostEstimate` variant in `engine/tests/test_sdk.py` asserting `cost_estimate["cross_review"] == 6`).
    - **OPEN** (issue #110): §3.1.9 `influence="advisory"` output heading test (in `engine/tests/test_phases.py::TestArbitration` — runs the pipeline and asserts heading differences in `arbitration/resolution.md`).
14. **Governance exit codes, persistence round-trip, combinatorial matrix** — CI/CD exit code scheme, persist→list→show, 6 cross-axis smoke combinations. **REVISE** — the persistence sub-item shipped (PR #106) but the bundled step is NOT closed; CI/CD exit codes and the combinatorial matrix have no tracking infrastructure yet. Verdict updated MATCH→REVISE per the strip-script-061-substeps deliberation 2026-05-01 (Convergence §6).
    - **persist→list→show round-trip**: DONE (PR #106) — `TestPersistListShowRoundTrip` (3 tests) pins the slug-as-public-id contract end-to-end: single round-trip with synthesis read-back, multi-deliberation round-trip with no cross-contamination, post-cleanup round-trip showing pruned runs disappear from list while survivors remain readable. Note: persistence sub-item delivery does NOT close step 14.
    - **CI/CD exit code scheme** (issue #112): scheme SELECTION covered by `TestExitCodeSchemeResolution` in `test_cli_context.py`. Actual emission (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE, 4=WARNING per spec 048 §5) is blocked on spec 048's gate command landing.
    - **6 cross-axis smoke combinations** (issue #113): not yet implemented. Would exercise {provider} × {mode} × {persistence} permutations as a combinatorial matrix; mock provider + parametrized fixtures sufficient (no API credits needed).
