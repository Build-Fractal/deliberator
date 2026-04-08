# Feature Specification: Plugin System Infrastructure

**Feature ID**: `016-plugin-system`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: None (infrastructure foundation for all plugin specs)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 3: Plugin System, FR-001 through FR-009). The scaffolding that makes plugins possible, without any specific plugin.

---

## 1. Feature Summary

Define the plugin loading mechanism, lifecycle hooks, state interface, and output namespace that all conversus plugins share. This spec builds the framework; specs 017-019 build individual plugins on top of it.

The plugin system follows five design principles from the game engine vision:
1. **Core works alone.** Removing all plugins produces exactly current conversus behavior.
2. **Plugins are optional.** Each is independently installable.
3. **Plugins are swappable.** The interface is defined; implementations vary.
4. **Data flows one direction.** Core produces artifacts; plugins consume them. Plugins never modify core artifacts.
5. **Plugin output is advisory.** Plugins provide recommendations. The user decides.

**What changes**: New `plugins:` config section in `conversus.yml`. New Python base class and hook system. New `{output}/plugins/` output directory. Plugin loading at orchestrator startup.

**What does not change**: Core deliberation behavior. Template system. Phase 1-6 execution. Output format (core output is identical with or without plugins).

---

## 2. Plugin Interface

### Base Class

```python
from conversus.plugins import Plugin, HookPoint, DeliberationState, PluginResult

class MyPlugin(Plugin):
    name = "my-plugin"
    hooks = [HookPoint.POST_PHASE_5, HookPoint.POST_DELIBERATION]

    def execute(self, state: DeliberationState, config: dict) -> PluginResult:
        # Plugin logic here
        return PluginResult(
            recommendation="Human-readable insight",
            data={"score": 0.85, "details": {}},
            advisory=True
        )
```

### Lifecycle Hooks

| Hook | When | Use Case |
|------|------|----------|
| `PRE_EXECUTION` | Before Phase 1, after config parsing | Config optimization, scenario loading |
| `POST_PHASE_5` | After each round's synthesis | Convergence prediction, per-round scoring |
| `POST_DELIBERATION` | After all rounds complete | Final equilibrium scoring, quality audit |
| `POST_ARBITRATION` | After Phase 6 | Re-scoring after arbiter rulings |

### DeliberationState

The read-only state object passed to plugins at each hook point:

- `mode: str` -- current deliberation mode
- `round: int` -- current round number (0-indexed)
- `agents: list[AgentState]` -- per-agent state (name, positions, concessions, recommendations)
- `synthesis: Optional[str]` -- current round's synthesis content (None for PRE_EXECUTION)
- `history: list[RoundState]` -- all prior rounds' states
- `output_dir: Path` -- path to the output directory
- `config: dict` -- full conversus.yml config

### PluginResult

- `recommendation: str` -- human-readable recommendation or insight
- `data: dict` -- machine-readable structured data (written to plugin output file)
- `advisory: bool` -- whether this result is advisory (True) or actionable (False; reserved for future autonomous mode)

---

## 3. Functional Requirements

### Configuration

- **FR-001**: A `plugins` field in `conversus.yml` MUST allow declaring plugins as a list of objects with `name` (string), `package` (string, pip package name), and `config` (dict, plugin-specific configuration).
- **FR-002**: An empty `plugins: []` or absent `plugins` field MUST produce identical behavior to a run without the plugins field. Zero behavioral change.

### Plugin Loading

- **FR-003**: The orchestrator MUST load plugins at startup by importing the package specified in `package` and instantiating the plugin class.
- **FR-004**: Plugins MUST be installable via `pip install {package-name}`. The orchestrator uses Python's `importlib` for dynamic loading.
- **FR-005**: If a declared plugin's package is not installed, the orchestrator MUST emit a warning and continue without that plugin. No crash.

### Hook Execution

- **FR-006**: At each lifecycle hook point, the orchestrator MUST call `execute()` on every plugin registered for that hook, passing the current `DeliberationState`.
- **FR-007**: Plugins registered for the same hook MUST execute sequentially in declaration order (order in `conversus.yml`).
- **FR-008**: Plugin execution MUST NOT block core deliberation. If a plugin's `execute()` raises an exception, the orchestrator MUST log the error, skip that plugin, and continue.

### Plugin Output

- **FR-009**: Plugin output MUST be written to `{output}/plugins/{plugin-name}.json`. One file per plugin per hook invocation (filename includes hook and round if applicable: `{plugin-name}-{hook}-round-{N}.json`).
- **FR-010**: Plugins MUST NOT write to core output directories (`summary/`, `{agent}/`, `arbitration/`). Plugin output is namespaced.
- **FR-011**: Core deliberation output MUST be identical with or without plugins installed. This is the fundamental isolation guarantee.

### Plugin API Package

- **FR-012**: The plugin base class, hook points, state objects, and result type MUST ship in a `conversus-plugins` package (pip installable).
- **FR-013**: Dependencies of `conversus-plugins` MUST be limited to `pydantic` (for state/result models). No solver, no ML, no heavyweight libraries.
- **FR-014**: Plugin implementations (specs 017-019) depend on `conversus-plugins`; the core conversus engine does not.

### Constitution Grounding

- **FR-015**: The plugin system MUST adhere to Constitution Principle XV (Plugin Isolation): plugins observe and advise; they do not control or modify core deliberation.

---

## 4. Success Criteria

- **SC-001**: A conversus run with `plugins: []` produces byte-identical core output to a run without the `plugins` field.
- **SC-002**: A conversus run with a configured plugin produces core output unchanged plus a `plugins/{name}.json` file.
- **SC-003**: Declaring a plugin whose package is not installed emits a warning but does not crash or alter the run.
- **SC-004**: A plugin that raises an exception during `execute()` is logged and skipped; the deliberation completes normally.
- **SC-005**: Two plugins at the same hook point execute in declaration order, and the second plugin's failure does not affect the first plugin's output.

---

## 5. Constraints

- **Must NOT add any runtime dependency to the core engine.** The plugin system is opt-in infrastructure. The core engine imports `conversus-plugins` only when `plugins:` is declared in config.
- **Must NOT let plugins modify core artifacts.** This is the non-negotiable isolation boundary. Plugins read `DeliberationState`; they write to `plugins/`. Period.
- **Must NOT make plugin output authoritative by default.** Plugins are advisory. A future autonomous mode may act on plugin recommendations, but that is a separate spec.
- **Must NOT define any specific plugins.** This spec is the framework. Individual plugins are specs 017-019.
