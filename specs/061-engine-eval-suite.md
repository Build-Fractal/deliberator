# Spec 061: Engine Eval Suite — Composable Deliberation Testing

**Feature ID**: `061-engine-eval-suite`
**Created**: 2026-04-16
**Status**: Draft
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

**Known gap**: Only `mock`, `demo`, `anthropic`, `openai` resolve through `engine/auth.py`. The remaining 9 providers have execution classes but no auth wiring.

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
  "quality_indicators": ["<string>", ...],
  "debate_transcript": "<string>"
}
```

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
```

Both must return the same JSON schema with the same fields. Content may differ (separate runs) but structure must match.

---

## 4. Eval Framework

### 4.1 Promptfoo (functional layer)

```yaml
# evals/promptfooconfig.yaml
providers:
  - id: exec:uv run conversus decide "{{prompt}}" --provider mock --mode cooperative --format json
    label: cooperative-mock
  - id: exec:uv run conversus decide "{{prompt}}" --provider mock --mode winner-take-all --format json
    label: wta-mock
  - id: exec:uv run conversus decide "{{prompt}}" --provider mock --mode prisoners-dilemma --format json
    label: pd-mock
  - id: exec:uv run conversus decide "{{prompt}}" --provider mock --mode red-blue --format json
    label: redblue-mock

tests:
  - description: "Basic deliberation question"
    vars:
      prompt: "Should we use Postgres or MongoDB for our metadata store?"
    assert:
      - type: is-json
      - type: javascript
        value: "JSON.parse(output).headline !== undefined"
      - type: not-contains
        value: "Error:"
  
  - description: "Short but valid question"
    vars:
      prompt: "Build vs buy for auth?"
    assert:
      - type: is-json
      - type: not-contains
        value: "too short"
```

Run: `npx promptfoo eval -c evals/promptfooconfig.yaml`

### 4.2 DeepEval (quality layer)

```python
# engine/tests/test_evals.py
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval

from engine.handlers import run_decide_mcp

SYNTHESIS_QUALITY = GEval(
    name="Synthesis Grounding",
    criteria="""The synthesis must:
    1. Reference specific claims from individual agent reviews
    2. Acknowledge where agents disagreed
    3. Provide a clear verdict or recommendation
    4. Not introduce claims absent from the pipeline record
    Score 0 if verdict is missing. Score 0.5 if verdict exists but
    doesn't reference the debate. Score 1 if fully grounded.""",
    threshold=0.7,
)

@pytest.mark.eval
class TestDeliberationQuality:
    def test_cooperative_synthesis_quality(self):
        result = run_decide_mcp(
            "Should we use Postgres or MongoDB for metadata?",
            "anthropic", "cooperative", 20
        )
        test_case = LLMTestCase(
            input="Should we use Postgres or MongoDB for metadata?",
            actual_output=result.output.get("full_analysis", ""),
        )
        assert_test(test_case, [SYNTHESIS_QUALITY])
```

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

| # | Gap | Severity | Surface |
|---|---|---|---|
| G1 | `red-blue` mode fails in `decide` — default presets lack `role: red/blue` | P0 | CLI, MCP |
| G2 | Target path resolution doubles relative paths | P1 | CLI, MCP |
| G3 | 9 providers (claude-code, aider, opencode, ollama, etc.) have execution classes but no auth wiring | P1 | CLI, MCP |
| G4 | `claude-desktop` provider not in auth resolver (only in handlers.py special case) | P2 | MCP |
| G5 | Question sufficiency gate rejects short but clear questions | P2 | CLI, MCP |
| G6 | `headline` is `[Change label]` in mock output (template not filled) | P3 | CLI, MCP |
| G7 | CLI `--format json` mixed with rich stderr on some error paths | P3 | CLI |
| G8 | Settings cascade untested end-to-end | P2 | All |
| G9 | MCP tool output schema not validated against Pydantic models in CI | P2 | MCP |
| G10 | SKILL.md and engine implementations diverged — no parity test | P1 | Skill |

---

## 6. Success Criteria

1. **All 4 primary modes** pass smoke tests with mock provider (0 errors, valid JSON)
2. **All registered providers** instantiate without import errors
3. **CLI and MCP surfaces** produce structurally identical output for the same input
4. **Quality metrics** score >= 0.7 on synthesis grounding with anthropic provider
5. **Known gaps G1-G5** resolved and covered by regression tests
6. **Eval suite runs in CI** — smoke tests on every push, quality evals on release tags
7. **Baseline snapshots** saved for 5 standard test questions across all modes

---

## 7. Implementation Order

1. Install promptfoo + deepeval, create `evals/` directory
2. Write promptfoo config — smoke tests for all modes × mock
3. Run first eval — capture current pass/fail state
4. Fix G1 (red-blue presets) and G2 (target paths) — re-run evals
5. Wire remaining providers into auth resolver (G3) — re-run evals
6. Write deepeval quality tests — run with anthropic provider
7. Save baseline snapshots
8. Add eval commands to CI workflow
9. Build engine-first skill that wraps CLI (replaces agent-dispatch SKILL.md)
10. Cross-surface parity tests (CLI vs MCP output comparison)
