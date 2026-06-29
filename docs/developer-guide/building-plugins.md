# Building Plugins

Plugins observe deliberation state and produce advisory output. They never modify core artifacts.

## Plugin ABC

Every plugin extends `deliberator.plugins.base.Plugin`:

```python
from deliberator.plugins.base import (
    DeliberationState,
    HookPoint,
    Plugin,
    PluginResult,
)

class MyPlugin(Plugin):
    name = "my-plugin"                        # Unique identifier
    hooks = [HookPoint.POST_PHASE_5]          # When to run
    produces = ["my_metric"]                   # Data keys this plugin emits
    consumes = []                              # Data keys from other plugins

    def execute(self, state: DeliberationState) -> PluginResult:
        score = compute_something(state)
        return PluginResult(
            recommendation=f"Score is {score:.2f}",
            data={"my_metric": score},
            advisory=True,
        )
```

**Class attributes (required):**
- `name`: Non-empty string. Used in output filenames.
- `hooks`: Non-empty list of `HookPoint` values.

**Class attributes (optional):**
- `produces`: Data keys this plugin outputs. Other plugins can consume them.
- `consumes`: Data keys this plugin reads from other plugins.

Both are validated at class definition time via `__init_subclass__`.

## HookPoint lifecycle

| Hook | When it fires | Typical use |
|------|--------------|-------------|
| `PRE_EXECUTION` | After config parsing, before first agent launch | Validate preconditions, initialize resources |
| `POST_PHASE_5` | After each round's synthesis completes | Score equilibrium, measure convergence |
| `POST_DELIBERATION` | After final round (or stagnation) | Aggregate metrics, produce final report |
| `POST_ARBITRATION` | After arbitration resolves disputes | Evaluate ruling quality |

## DeliberationState

The frozen state object passed to every `execute()` call:

```python
class DeliberationState(BaseModel):
    model_config = {"frozen": True}

    mode: str                              # "cooperative", "red-blue", etc.
    round: int                             # Current round number
    agents: list[AgentState]               # Per-agent metrics
    synthesis: str | None                  # Synthesis text (POST_PHASE_5+)
    history: list[RoundState]              # Prior rounds
    output_dir: Path                       # Where files are written
    config: dict[str, Any]                 # Raw config dict
    plugin_results: dict[str, Any]         # Data from prior plugins (this hook)
```

`AgentState` captures per-agent participation:
```python
class AgentState(BaseModel):
    name: str
    recommendation_count: int = 0
    concession_count: int = 0
    surviving_count: int = 0
    positions: list[dict[str, Any]] = []
```

## PluginResult

What your plugin returns:

```python
class PluginResult(BaseModel):
    recommendation: str              # Plain-language advisory text
    data: dict[str, Any] = {}        # Structured data (published via produces)
    advisory: bool = True            # Always True for now
```

The `data` dict is where you put values declared in `produces`. The orchestrator extracts them and makes them available to downstream plugins via `state.plugin_results`.

## Cross-plugin data flow

Declare `produces` and `consumes` to create a data dependency graph:

```python
class MetricProducer(Plugin):
    name = "metric-producer"
    hooks = [HookPoint.POST_PHASE_5]
    produces = ["equilibrium_score"]

    def execute(self, state):
        score = compute_equilibrium(state)
        return PluginResult(
            recommendation=f"EQ score: {score}",
            data={"equilibrium_score": score},
        )


class MetricConsumer(Plugin):
    name = "metric-consumer"
    hooks = [HookPoint.POST_PHASE_5]
    consumes = ["equilibrium_score"]

    def execute(self, state):
        eq = state.plugin_results.get("equilibrium_score", 0.0)
        return PluginResult(
            recommendation=f"Using EQ score: {eq}",
            data={"combined": eq * 2},
        )
```

The orchestrator sorts plugins topologically so producers run before consumers. Cycles raise `PluginDependencyCycleError`. Duplicate producers raise `DuplicateProducerError`.

## Plugin output

Results are written to `{output_dir}/plugins/{name}-{hook}-round-{N}.json`:

```json
{
  "plugin": "my-plugin",
  "hook": "post_phase_5",
  "round": 1,
  "recommendation": "Score is 0.85",
  "data": {"my_metric": 0.85},
  "advisory": true
}
```

## Plugin configuration

Plugin-specific config is passed at instantiation via the config file:

```yaml
plugins:
  - name: equilibrium-scorer
    package: deliberator.plugins.nashopt
    config:
      threshold: 0.85
      gamma: 1.0
      solver_timeout: 30.0
```

Access config in your plugin via `self.plugin_config`:

```python
def execute(self, state):
    threshold = self.plugin_config.get("threshold", 0.85)
    # ...
```

## Dynamic loading

Plugins are loaded by `load_plugins()` from config entries:

1. Import the package via `importlib.import_module(package)`.
2. Find the first `Plugin` subclass in the module.
3. Instantiate with the plugin-specific config.

If a package is not installed, a warning is logged and that plugin is skipped. No crash.

## Example: Build a logging plugin

```python
"""Simple plugin that logs deliberation metrics."""

from deliberator.plugins.base import (
    DeliberationState,
    HookPoint,
    Plugin,
    PluginResult,
)

class LoggingPlugin(Plugin):
    name = "deliberation-logger"
    hooks = [HookPoint.POST_PHASE_5, HookPoint.POST_DELIBERATION]

    def execute(self, state: DeliberationState) -> PluginResult:
        agent_count = len(state.agents)
        dispute_count = 0
        if state.history:
            dispute_count = state.history[-1].dispute_count

        msg = (
            f"Round {state.round}: {agent_count} agents, "
            f"{dispute_count} disputes, mode={state.mode}"
        )

        return PluginResult(
            recommendation=msg,
            data={
                "agent_count": agent_count,
                "dispute_count": dispute_count,
                "round": state.round,
            },
        )
```

## Wiring your plugin

To make the engine discover and load your plugin at runtime:

1. **Make the module importable.** Either install your plugin package (`pip install -e .` or `uv pip install -e .`) or ensure its parent directory is on `sys.path`.

2. **Set the `package` field** in your config entry to the dotted import path of the module containing your `Plugin` subclass:

    ```yaml
    plugins:
      - name: my-plugin
        package: my_package.plugins.scoring
        config:
          threshold: 0.9
    ```

3. **How discovery works.** The engine calls `importlib.import_module()` on the `package` string, then iterates `dir()` on the imported module in alphabetical order and picks the first class that is a subclass of `Plugin` (excluding `Plugin` itself). If your module contains multiple `Plugin` subclasses, the one whose class name comes first alphabetically will be selected.

4. **Failure mode.** If the import fails (e.g., the package is not installed), a warning is logged and the plugin is skipped. This is non-fatal -- the rest of the deliberation proceeds without that plugin. The same catch-and-skip behavior applies if the module contains no `Plugin` subclass or if instantiation raises an exception.

## Error handling

The framework uses a catch-and-skip strategy for plugin failures:

1. **Exceptions in `execute()` are caught and logged.** If your plugin raises during execution, the orchestrator logs the exception at warning level (with traceback) and continues with the next plugin. The deliberation is never aborted by a plugin failure.

2. **Recommended patterns:**
    - **Raise freely.** You do not need to wrap your `execute()` body in try/except. The framework catches all exceptions, so let errors propagate naturally.
    - **Use safe access for consumed data.** When reading data from upstream plugins, use `state.plugin_results.get("key", default)` rather than direct indexing. If a producer plugin failed or was skipped, the key will be absent.
    - **Check warning-level logs during development.** Plugin load failures, missing `produces` keys, and execution exceptions all appear at warning level in the `deliberator.plugins` logger.

These are recommended patterns based on the current implementation, not contractual guarantees.

## Existing plugins

| Plugin | Package | Hooks | Produces |
|--------|---------|-------|----------|
| `equilibrium-scorer` | `deliberator.plugins.nashopt` | POST_PHASE_5, POST_DELIBERATION | `equilibrium_score` |
| `optimizer` | `deliberator.plugins.optimizer` | POST_DELIBERATION | (configurable) |
| `scenarios` | `deliberator.plugins.scenarios` | POST_PHASE_5 | (configurable) |
