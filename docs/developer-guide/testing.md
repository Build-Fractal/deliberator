# Testing

Conversus has ~1400 tests across engine, linter, MCP server, web backend, and frontend.

## Running tests

```bash
# All engine + linter + MCP tests
uv run pytest -x -q

# Web backend
uv run pytest web/tests/ -x -q

# Frontend
cd frontend && pnpm test

# Template validation (linter)
uv run python3 -m linter.validate

# Specific test file
uv run pytest tests/test_plugins.py -x -v

# Specific test
uv run pytest tests/test_plugins.py::test_echo_plugin -x -v
```

## Test organization

| Directory | Tests | Count |
|-----------|-------|-------|
| `engine/tests/` | CLI, config, dispatch, events, phases, providers, SDK, auth, templates, progress, render | ~600 |
| `tests/` | Schemas, plugins, domains, game forms, construction, extraction, convergence, solver | ~700 |
| `linter/` | Validation, quality, output contract, question classifier, presets, MCP server | ~100 |
| `web/tests/` | FastAPI app, Supabase DB | ~43 |
| `frontend/` | React components | ~94 |

## Frozen Pydantic models

All models use `model_config = {"frozen": True}`. In tests, construct them directly:

```python
from conversus.plugins.base import AgentState, DeliberationState

state = DeliberationState(
    mode="cooperative",
    round=1,
    agents=[
        AgentState(name="agent-a", recommendation_count=3, surviving_count=2),
        AgentState(name="agent-b", recommendation_count=2, surviving_count=1),
    ],
    output_dir=tmp_path,
)

# Immutable -- this raises:
# state.round = 2  # ValidationError
```

To create a modified copy:

```python
updated = state.model_copy(update={"round": 2})
```

## Mock providers

The `MockProvider` returns synthetic responses without API calls. It is always available:

```python
from engine.providers import MockProvider

provider = MockProvider()
# Returns deterministic mock text for any prompt
```

For provider tests, mock the HTTP layer:

```python
from unittest.mock import AsyncMock, patch

async def test_anthropic_dispatch():
    mock_provider = AsyncMock()
    mock_provider.complete.return_value = "Mock response text"

    result = await dispatch_agent(
        prompt="test prompt",
        agent_name="test-agent",
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        provider=mock_provider,
        emitter=NullEmitter(),
    )
    assert result[0] == "Mock response text"
```

## Mock gap fillers

For construction pipeline tests, use `NonInteractiveGapFiller` (fails on gaps) or write a custom one:

```python
from conversus.schemas.construction import GapFiller

class FixedGapFiller:
    """Returns predetermined answers for testing."""

    def __init__(self, answers: dict[str, str]):
        self.answers = answers
        self._call_index = 0

    def fill(self, question: str, context: str) -> str:
        # Return answers in order
        answer = list(self.answers.values())[self._call_index]
        self._call_index += 1
        return answer
```

## Fixture data

Reference deliberation outputs for testing live in `specs/` subdirectories. These are real conversus runs committed as test fixtures. The output contract parser tests use them to verify parsing against known-good synthesis output.

For domain plugin tests, construct `DomainContext` with a temp workspace:

```python
def test_code_review_scoring(tmp_path):
    domain = CodeReviewDomain()

    context = DomainContext(
        workspace=tmp_path,
        changed_files=[tmp_path / "main.py"],
        metadata={"language": "python"},
    )

    # Write fixture data that extractors will read
    (tmp_path / "coverage.json").write_text('{"totals": {"percent_covered": 85}}')

    variables = domain.extract(context)
    score = domain.score(variables, "startup-mvp")

    assert score.verdict in ("pass", "revise", "block")
    assert 0.0 <= score.overall <= 1.0
```

## Test patterns

### Plugin isolation

Plugin tests verify that failures are isolated -- a crashing plugin does not abort the deliberation:

```python
def test_plugin_failure_isolation(tmp_path):
    plugins = [FailingPlugin(), EchoPlugin()]
    state = DeliberationState(mode="cooperative", round=1, output_dir=tmp_path)

    results = execute_hooks(HookPoint.POST_PHASE_5, plugins, state, tmp_path)

    # FailingPlugin raised, but EchoPlugin still ran
    assert len(results) == 1
    assert results[0].recommendation.startswith("Echo")
```

### Config validation

Config tests cover the full validation matrix -- valid configs, missing fields, invalid modes, duplicate agent names, bad presets:

```python
def test_invalid_mode(tmp_path):
    config_path = tmp_path / "conversus.yml"
    config_path.write_text("mode: invalid\ntarget: x.md\noutput: out/\nagents: []")

    with pytest.raises(ConfigError, match="is not valid"):
        parse_config(config_path)
```

### Testing custom plugins

To test a plugin, construct a `DeliberationState` with the fields your plugin reads, call `execute()`, and assert on the returned `PluginResult`:

```python
from pathlib import Path
from conversus.plugins.base import (
    AgentState,
    DeliberationState,
    HookPoint,
    Plugin,
    PluginResult,
)

class ScorePlugin(Plugin):
    name = "test-scorer"
    hooks = [HookPoint.POST_PHASE_5]
    produces = ["my_score"]

    def execute(self, state: DeliberationState) -> PluginResult:
        score = len(state.agents) / 10.0
        return PluginResult(
            recommendation=f"Score: {score}",
            data={"my_score": score},
        )


def test_score_plugin(tmp_path):
    plugin = ScorePlugin()
    state = DeliberationState(
        mode="cooperative",
        round=1,
        agents=[
            AgentState(name="a", recommendation_count=3, surviving_count=2),
            AgentState(name="b", recommendation_count=1, surviving_count=1),
        ],
        output_dir=tmp_path,
    )

    result = plugin.execute(state)

    assert result.data["my_score"] == 0.2
    assert "Score" in result.recommendation
```

To test a plugin that consumes data from another plugin, populate `plugin_results` on the state:

```python
def test_consumer_plugin(tmp_path):
    plugin = MyConsumerPlugin()
    state = DeliberationState(
        mode="cooperative",
        round=2,
        output_dir=tmp_path,
        plugin_results={"upstream_metric": 0.75},
    )

    result = plugin.execute(state)
    assert result.data["derived_metric"] == 0.75 * 2
```

### Testing custom domains

Construct a `DomainContext` with a temporary workspace, write any fixture files your extractors need, then run the extract-score pipeline:

```python
import json
from pathlib import Path
from typing import Any
from conversus.domains.base import DomainContext, DomainPlugin, VariableExtractor


class StubExtractor:
    name = "stub"
    variables = ["coverage", "lint_issues"]

    def extract(self, context: DomainContext) -> dict[str, Any]:
        data = json.loads((context.workspace / "metrics.json").read_text())
        return {
            "coverage": data["coverage"] / 100.0,
            "lint_issues": 1.0 / (1.0 + data["lint_issues"]),
        }


class StubDomain(DomainPlugin):
    name = "stub-domain"
    version = "1.0.0"

    def __init__(self, scaffold_dir: Path):
        self.scaffold_dir = scaffold_dir

    def get_extractors(self) -> list[VariableExtractor]:
        return [StubExtractor()]


def test_domain_scoring(tmp_path):
    # Write fixture data
    (tmp_path / "metrics.json").write_text('{"coverage": 85, "lint_issues": 3}')

    # Write scaffold
    scaffold_dir = tmp_path / "scaffolds"
    scaffold_dir.mkdir()
    (scaffold_dir / "default.yml").write_text(
        "name: default\nweights:\n  coverage: 2.0\n  lint_issues: 1.0\n"
        "thresholds:\n  coverage: 0.7\nhard_blocks: []\n"
    )

    domain = StubDomain(scaffold_dir=scaffold_dir)
    context = DomainContext(
        workspace=tmp_path,
        changed_files=[tmp_path / "main.py"],
    )

    variables = domain.extract(context)
    assert "coverage" in variables

    score = domain.score(variables, "default")
    assert score.verdict in ("pass", "revise", "block")
    assert 0.0 <= score.overall <= 1.0
    assert score.scaffold_name == "default"
```

To test `create_record()` and persistence:

```python
def test_domain_record_creation(tmp_path):
    domain = StubDomain(scaffold_dir=tmp_path)
    context = DomainContext(workspace=tmp_path)

    # Use a pre-built score (bypass extraction)
    from conversus.domains.base import DomainScore
    score = DomainScore(
        overall=0.8, verdict="pass", dimensions={"coverage": 0.85},
        hard_blocks=[], recommendations=[], variables={"coverage": 0.85},
    )

    record = domain.create_record(score, context)
    assert record.domain == "stub-domain"
    assert record.score.verdict == "pass"
    assert record.context_summary["workspace"] == str(tmp_path)
```

### Async pipeline tests

Pipeline tests use `MockProvider` and `NullEmitter` to run the full pipeline synchronously:

```python
async def test_full_pipeline(tmp_path):
    config = EngineConfig(
        mode="cooperative",
        target_files=[tmp_path / "spec.md"],
        output=tmp_path / "output",
        agents=[
            AgentConfig(name="a", prompt="Agent A"),
            AgentConfig(name="b", prompt="Agent B"),
        ],
    )

    result = await run_pipeline(
        config, MockProvider(), NullEmitter(), config_path=None,
    )

    assert result.phases_completed >= 5
    assert len(result.written_files) > 0
```

## pytest configuration

From `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
pythonpath = ["."]
```

`asyncio_mode = "auto"` means async test functions are detected and run automatically without `@pytest.mark.asyncio`.
