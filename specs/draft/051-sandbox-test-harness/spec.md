# Spec 051: Sandbox Test Harness

**Status**: Draft
**Author**: Brian Slater + Claude Opus 4.6
**Date**: 2026-04-06
**Depends on**: 042 (execution providers), 050 (cascading settings)

---

## 1. Problem

Conversus has 12 execution providers but no way to validate them in isolation.
Unit tests mock the subprocess/HTTP layer; live tests hit real APIs and cost money.
There's no middle ground: a sandboxed environment where providers execute real
subprocesses against controlled inputs and we observe structured outputs.

We need:
- A way to invoke any provider in a sandbox and assert on the result
- Deterministic test fixtures (known prompts → expected output shapes)
- Cost tracking per test run (catch regressions in token usage)
- CI-compatible execution (ollama for free, mock as fallback)

## 2. Design: Provider Test Sandbox

### 2.1 Architecture

```
┌──────────────────────────────────────────────┐
│  Test Runner (pytest + sandbox fixtures)      │
│                                               │
│  ┌─────────────┐  ┌─────────────────────┐    │
│  │ SandboxEnv  │  │ ProviderUnderTest   │    │
│  │             │  │                     │    │
│  │ • tmpdir    │──│ • execute(task)     │    │
│  │ • fake files│  │ • observe result    │    │
│  │ • env vars  │  │ • assert structure  │    │
│  │ • .conversus│  │ • record cost       │    │
│  └─────────────┘  └─────────────────────┘    │
│                                               │
│  Assertions:                                  │
│  • result.success == True                     │
│  • result.content matches pattern             │
│  • result.cost.input_tokens > 0               │
│  • result.duration < timeout                  │
│  • no secrets in subprocess argv              │
└──────────────────────────────────────────────┘
```

### 2.2 SandboxEnv Fixture

A pytest fixture that creates an isolated environment for a single provider test:

```python
@pytest.fixture
def sandbox(tmp_path):
    """Create a sandboxed environment for provider testing."""
    env = SandboxEnv(tmp_path)
    
    # Create a minimal project with .conversus/ init'd
    env.init_project(runtimes=["claude-code", "ollama"])
    
    # Create test target files
    env.write_file("target.md", "# Test Target\nThis is a smoke test.")
    env.write_file("spec.md", "# Spec\nReview the target file.")
    
    return env
```

### 2.3 Provider Test Protocol

Each provider test follows the same pattern:

```python
@pytest.mark.sandbox
async def test_provider_ping_pong(sandbox, provider_name):
    """Every provider should be able to answer a trivial question."""
    provider = get_provider(provider_name)
    task = ExecutionTask.from_prompt(
        prompt="Reply with exactly the word pong.",
        output_path=str(sandbox.output_path("ping.md")),
    )
    result = await provider.execute(task)
    
    assert result.success is True
    assert result.content is not None
    assert "pong" in result.content.lower()
    assert result.provider == provider_name
```

### 2.4 Observation Points

The sandbox records everything for post-test analysis:

| Observation | How | Why |
|---|---|---|
| **stdout/stderr** | Captured by SubprocessProvider | Debug failures |
| **Exit code** | On ExecutionResult.metadata | Detect crashes |
| **Cost** | ExecutionResult.cost | Catch token regressions |
| **Duration** | ExecutionResult.duration | Catch latency regressions |
| **Files written** | Scan sandbox tmpdir | Verify agent file I/O |
| **Env vars** | Snapshot before/after | Verify env-only secrets |
| **Argv** | From SubprocessProvider._build_argv | Verify no secrets in argv |

### 2.5 Test Matrix

```python
PROVIDER_MATRIX = {
    # Free providers (always run in CI)
    "mock": {"cost": "free", "ci": True},
    "ollama": {"cost": "free", "ci": True, "requires": "ollama"},
    
    # Paid providers (run with -m paid or manual trigger)
    "claude-code": {"cost": "paid", "ci": False},
    "anthropic": {"cost": "paid", "ci": False},
    "aider": {"cost": "paid", "ci": False},
    
    # Local servers (run with -m local)
    "llama-cpp": {"cost": "free", "ci": False, "requires": "llama-server"},
    "vllm": {"cost": "free", "ci": False, "requires": "vllm"},
    
    # External CLIs (run with -m external)
    "codex": {"cost": "paid", "ci": False, "requires": "codex"},
    "gemini": {"cost": "paid", "ci": False, "requires": "gemini"},
    "copilot": {"cost": "paid", "ci": False, "requires": "gh"},
    "opencode": {"cost": "paid", "ci": False, "requires": "opencode"},
    "pi": {"cost": "paid", "ci": False, "requires": "pi"},
}
```

### 2.6 Pytest Marks

```
pytest -m sandbox                  # all sandbox tests
pytest -m "sandbox and free"       # free providers only (CI default)
pytest -m "sandbox and paid"       # paid providers (manual)
pytest -m "sandbox and local"      # local server providers
```

## 3. Test Categories

### 3.1 Conformance Tests (every provider)

- `test_ping_pong` — trivial prompt, verify response exists
- `test_result_shape` — ExecutionResult has all required fields
- `test_duration_positive` — duration > 0
- `test_provider_name` — result.provider matches expected name
- `test_error_on_bad_input` — empty prompt produces clean error

### 3.2 Feature Tests (capability-dependent)

- `test_cost_telemetry` — providers that report cost have non-None Cost
- `test_reference_inlining` — `supports_tool_use=False` providers inline files
- `test_file_write` — `supports_tool_use=True` providers write to output_path
- `test_model_override` — task metadata model overrides provider default

### 3.3 Security Tests (all subprocess providers)

- `test_no_secrets_in_argv` — API keys never appear in process argv
- `test_secrets_in_env` — API keys are in subprocess env only
- `test_timeout_kills_process` — long-running task gets killed
- `test_sigterm_propagation` — SIGTERM sent before SIGKILL

### 3.4 Regression Tests (cost/latency baselines)

```python
def test_cost_regression(sandbox, provider_name, baseline_file):
    """Token count should not increase more than 20% from baseline."""
    result = await execute_standard_task(provider_name, sandbox)
    baseline = load_baseline(baseline_file, provider_name)
    
    if result.cost and baseline.get("input_tokens"):
        ratio = result.cost.input_tokens / baseline["input_tokens"]
        assert ratio < 1.2, f"Token regression: {ratio:.1%} increase"
```

## 4. CI Integration

### 4.1 GitHub Actions

```yaml
sandbox-tests:
  runs-on: ubuntu-latest
  services:
    ollama:
      image: ollama/ollama
      ports: ["11434:11434"]
  steps:
    - uses: actions/checkout@v4
    - run: pip install conversus[test]
    - run: ollama pull qwen3:0.6b
    - run: pytest -m "sandbox and free" --sandbox-report=report.json
    - uses: actions/upload-artifact@v4
      with:
        name: sandbox-report
        path: report.json
```

### 4.2 Sandbox Report

Each test run produces a JSON report:

```json
{
  "timestamp": "2026-04-06T17:00:00Z",
  "providers_tested": 2,
  "results": [
    {
      "provider": "mock",
      "tests_passed": 5,
      "tests_failed": 0,
      "total_cost_usd": 0,
      "total_duration_ms": 12
    },
    {
      "provider": "ollama",
      "tests_passed": 5,
      "tests_failed": 0,
      "total_cost_usd": 0,
      "total_duration_ms": 3400,
      "total_input_tokens": 245,
      "total_output_tokens": 38
    }
  ]
}
```

## 5. Implementation Phases

| Phase | What | LoC |
|---|---|---|
| 1 | `SandboxEnv` fixture + `test_conformance.py` | ~200 |
| 2 | Security tests (argv/env/timeout) | ~100 |
| 3 | Cost/latency regression baselines | ~80 |
| 4 | CI pipeline (GitHub Actions + ollama service) | ~50 |
| 5 | Sandbox report generator | ~100 |

**Total**: ~530 lines. The `SandboxEnv` fixture is the core; everything
else is test cases that use it.

## 6. Open Questions

1. **Should sandbox tests be in `engine/tests/` or a top-level `sandbox/` directory?** Recommendation: `engine/tests/sandbox/` — they're engine tests, just with a different execution profile.
2. **Should we snapshot baselines automatically?** On first run, record the baseline. On subsequent runs, compare. Recommendation: yes, store in `engine/tests/sandbox/baselines/`.
3. **Docker isolation?** For maximum isolation, sandbox tests could run each provider in a Docker container. Overkill for v1 — tmpdir isolation is sufficient.
