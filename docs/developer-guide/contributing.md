# Contributing

## For AI coding agents: read the gotchas first

If you are an AI coding agent working on this codebase, start with
[**gotchas.md**](gotchas.md) before touching the capability registry,
the projector, or any generated surface file
(`engine/cli/__init__.py`, `mcp_server.py`, `claude-code-plugin/`,
`desktop-extension/manifest.json`). That file is a hand-off memo from
previous agents: subtle bugs they hit, Pydantic v2 behaviors that
disagreed with their mental model, and constitutional constraints that
bit them mid-implementation. It's unpublished on purpose — it's a
memo from agents to agents, not user documentation — but reading it
first will save you rediscovering the same traps.

When you finish work and discover a new gotcha, append an entry to
that file in the same format.

## Code style

### Pure functions

Service logic uses pure functions, not classes. Functions are stateless and composable. Type hints required on all signatures.

```python
# Good
def compute_equilibrium_score(
    mode: str, features: RoundFeatures, config: dict[str, Any]
) -> dict[str, Any]:
    ...

# Avoid (class-based service)
class EquilibriumService:
    def compute(self, ...):
        ...
```

Exceptions: Pydantic models, Plugin/DomainPlugin subclasses, Provider implementations (framework requirements).

### Frozen models

All Pydantic models must use `model_config = {"frozen": True}`. No mutation after construction. Use `model_copy(update={...})` to create modified copies.

### Import discipline

The `conversus/` package must not import from `engine/`, `linter/`, `web/`, or `mcp_server`. This is the fundamental coupling rule. Domain plugins must not import from `engine/` either.

```python
# conversus/plugins/nashopt/scorer.py
from conversus.plugins.base import Plugin       # OK: same package
from conversus.schemas.features import ...      # OK: schemas package
from engine.phases import run_pipeline          # FORBIDDEN
```

All imports at top of file (PEP 8). Only exception: circular import avoidance (documented with a comment).

### Naming

- Agent names: lowercase alphanumeric with hyphens/underscores (`^[a-z0-9][a-z0-9\-_]*$`).
- Plugin names: kebab-case (`equilibrium-scorer`).
- Domain names: kebab-case (`code-review`).
- Template variables: UPPER_SNAKE_CASE (`{AGENT_NAME}`).

## PR process

1. **Branch** from `main`. Use descriptive branch names (`012-game-form-schemas`, `fix-arbiter-trigger`).

2. **Write tests first** when practical. Tests go next to the code they test (`engine/tests/`, `tests/`, `linter/test_*.py`, `web/tests/`).

3. **Run the full suite** before pushing:

```bash
uv run pytest -x -q                    # 1300+ tests
uv run python3 -m linter.validate      # Template validation
```

4. **Write a conversus.yml** for non-trivial changes. Self-review your PR with conversus before requesting human review:

```yaml
mode: red-blue
target: path/to/your/changes.md
output: path/to/review/
agents:
  - name: attacker
    role: red
    preset: red-team
  - name: defender
    role: blue
    preset: blue-team
```

5. **PR title**: Short, imperative (`Add Bayesian game form`, `Fix arbiter trigger logic`).

6. **PR body**: What changed, why, and how to verify. Include conversus output if you ran a self-review.

## Spec-driven development

Major features start as specs in `specs/`. The workflow:

1. Write a spec (problem statement, requirements, success criteria).
2. Run conversus against the spec for adversarial review.
3. Implement based on the reviewed spec.
4. Run conversus gate checks against the implementation.

Specs live in `specs/done/{NNN}-{feature-name}/` after completion.

## Conversus reviews before merge

For significant changes, run a conversus deliberation before merge:

```bash
# Quick self-review
uv run conversus decide "Should we merge this change? [paste summary]" --provider anthropic

# Full review against the spec
uv run conversus run specs/my-feature/conversus.yml --provider anthropic
```

Include the conversus output (or a summary) in the PR description.

## Architecture decisions

When making architectural choices, consider:

- **Does this violate the layer coupling rules?** `conversus/` must not import `engine/`.
- **Is the model frozen?** All Pydantic models must be immutable.
- **Is the function pure?** Prefer pure functions over stateful classes.
- **Is the plugin isolated?** Plugin failures must not crash the pipeline.
- **Is the output advisory?** Plugins observe, never modify.

## Adding a new feature

Typical steps:

1. Add schema YAML if needed (`schema/`).
2. Add Pydantic models if needed (`conversus/schemas/`).
3. Implement core logic as pure functions.
4. Add tests alongside the implementation.
5. Wire into the engine if it's a pipeline change (`engine/`).
6. Update templates if it affects prompt structure (`templates/`).
7. Run the linter to validate template changes.
8. Update the MCP server if it exposes new tools (`mcp_server.py`).
