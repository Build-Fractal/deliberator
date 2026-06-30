# Python SDK

The SDK provides programmatic access to deliberator for pipelines, scripts, and custom tooling.

## Installation

```bash
pip install deliberator              # recommended
# or, for development from source:
uv sync
```

!!! info "Two namespaces: `engine` and `deliberator`"
    The wheel installs three top-level packages: `engine`, `linter`, and `deliberator`. They serve different layers:

    - **`engine`** — the deliberation runtime. The SDK (`Deliberation`, `Result`, `validate`, `classify`) lives here because it depends on the full pipeline (auth, config, dispatch, phases, providers).
    - **`deliberator`** — the foundation layer: schemas, plugins, registry, paths, presets. Anything that *doesn't* depend on the engine runtime.
    - **`linter`** — output-contract parsing and the question classifier (consumed by the engine, not user-facing).

    ```python
    from engine import Deliberation, Result, validate   # SDK — runtime-dependent
    from deliberator.schemas.construction import construct_objective  # primitives — runtime-free
    from deliberator.plugins.base import Plugin                       # primitives — runtime-free
    ```

    The split is enforced by a coupling rule: `deliberator/` MUST NOT import from `engine/`, but `engine/` MAY import from `deliberator/`. That's what makes `deliberator/` reusable as a primitive layer.

## Quick start

```python
import asyncio
from engine import Deliberation, Result, validate

async def main():
    result = await Deliberation(
        question="Should we rewrite the auth system?",
        provider="anthropic",
    ).run()

    print(result.headline)
    print(result.summary)
    print(f"Rounds: {result.rounds_completed}")

asyncio.run(main())
```

!!! info "Async-native"
    Deliberator is async-native. The `asyncio.run()` wrapper above lets you run it as a plain Python script. In async contexts (FastAPI, event handlers), use `await` directly -- see [Async patterns](#async-patterns) below.

## Deliberation class

The main orchestrator. Supports two modes:

### Config-path mode

```python
from pathlib import Path
from engine import Deliberation

result = await Deliberation(
    config_path=Path("deliberator.yml"),
    provider="anthropic",
).run()
```

### Ad-hoc question mode

```python
result = await Deliberation(
    question="Should we use SQLite or Postgres for metadata?",
    provider="mock",
    mode="winner-take-all",
).run()
```

### Constructor parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config_path` | `Path \| None` | `None` | Path to `deliberator.yml` |
| `question` | `str \| None` | `None` | Ad-hoc question text |
| `provider` | `str` | `"mock"` | `"mock"`, `"anthropic"`, `"openai"` |
| `mode` | `str` | `"cooperative"` | Deliberation mode (ad-hoc only) |
| `output_dir` | `Path \| None` | `None` | Override output directory |

At least one of `config_path` or `question` is required.

### Cost estimation

Check cost before running:

```python
d = Deliberation(config_path=Path("deliberator.yml"))
print(d.cost_estimate)
# {'review': 3, 'cross_review': 6, 'revision': 3, 'disputes': 3, 'synthesis': 1}
```

!!! note "`cost_estimate` can return `None`"
    `cost_estimate` returns `None` when the config cannot be parsed or the agent count is indeterminate (e.g., ad-hoc mode with no config file). Always check for `None` before summing values.

### Dollar cost estimation

`estimate_cost_usd()` converts the launch count into an approximate dollar cost based on the provider's per-token pricing.

```python
d = Deliberation(config_path=Path("deliberator.yml"), provider="anthropic")
usd = d.estimate_cost_usd()
if usd is not None:
    print(f"Estimated cost: ${usd:.2f}")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| (none -- called on instance) | -- | -- | Uses the `provider` and `model` from the `Deliberation` constructor |

**Returns:** `float | None`. Returns `None` when `cost_estimate` is `None` or the provider has no pricing data (e.g., `mock`).

## Event subscription

Subscribe to lifecycle events before calling `run()`:

```python
from engine.events import PhaseStarted, PhaseCompleted, AgentCompleted

d = Deliberation(question="Redis vs Postgres?", provider="mock")

d.on(PhaseStarted, lambda e: print(f"Phase {e.phase} started ({e.agent_count} agents)"))
d.on(PhaseCompleted, lambda e: print(f"Phase {e.phase} done in {e.duration_ms}ms"))
d.on(AgentCompleted, lambda e: print(f"  Agent {e.agent_name}: {'ok' if e.success else e.error}"))

result = await d.run()
```

### Event types

| Event | Fields | When |
|-------|--------|------|
| `PhaseStarted` | `phase`, `agent_count`, `timestamp` | Phase begins |
| `AgentDispatched` | `phase`, `agent_name`, `model`, `timestamp` | Agent sent to provider |
| `AgentCompleted` | `phase`, `agent_name`, `success`, `error`, `duration_ms`, `response_text` | Agent finishes |
| `PhaseCompleted` | `phase`, `agent_count`, `success_count`, `failure_count`, `duration_ms` | All agents in phase done |

## Result model

`Deliberation.run()` returns a frozen `Result`:

```python
result.headline              # str: one-sentence verdict
result.summary               # str: agent/phase/dispute summary
result.full_analysis         # str: complete synthesis markdown
result.quality_indicators    # QualityIndicators: structured metrics
result.debate_transcript     # str: full transcript
result.rounds_completed      # int: how many rounds ran
result.termination_reason    # str | None: "converged", "stagnation", "max_rounds"
result.written_files         # list[Path]: all output files
result.output_dir            # Path: root output directory
```

## Validation without execution

```python
from engine import validate

vr = validate(Path("deliberator.yml"))
if not vr.valid:
    for error in vr.errors:
        print(f"Error: {error}")
else:
    print(f"Valid. Cost: {sum(vr.cost_estimate.values())} launches")
    print(f"Mode: {vr.config.mode}")
    print(f"Agents: {[a.name for a in vr.config.agents]}")
```

## Question classification

```python
from engine import classify

cr = classify("Should we use Redis?")
print(cr.sufficient)  # True/False
print(cr.reason)      # Why insufficient (if applicable)
```

!!! warning "Failure mode"
    `classify()` raises `ValueError` if the input is empty or not a string.

## Objective construction

Build parameterized objective functions from problem descriptions:

```python
from deliberator.schemas.construction import construct_objective

objective = construct_objective(
    problem_text="Choose between Redis and Postgres for caching. Budget is $500/month.",
    mode="winner-take-all",
)

print(objective.template_name)   # e.g., "competitive-selection"
print(objective.game_form)       # e.g., "normal-form"
print(objective.parameters)      # Extracted + filled parameters
print(objective.symbolic_form)   # Mathematical formulation
```

!!! warning "Failure modes"
    `construct_objective()` raises `RuntimeError` if template resolution fails (e.g., unknown mode) and `ValueError` if `problem_text` is empty or the extracted parameters fail validation.

## Async patterns

The SDK is async-first. In a sync context, use `asyncio.run()`:

```python
import asyncio
from engine import Deliberation

result = asyncio.run(
    Deliberation(question="Build vs buy?", provider="mock").run()
)
```

In an async context (FastAPI, Celery with async, etc.), await directly:

```python
async def my_pipeline():
    result = await Deliberation(
        question="Build vs buy?",
        provider="anthropic",
    ).run()
    return result.headline
```
