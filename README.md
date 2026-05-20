# conversus

Multi-agent deliberation engine. Pit AI agents against each other in structured adversarial review using game theory modes.

```bash
pip install git+https://github.com/Build-Fractal/conversus-oss.git
conversus decide "Should we use Postgres or MongoDB?" --provider ollama
```

## What is this?

Conversus orchestrates multiple AI agents in structured debates. Each agent reviews a target document from a different perspective, cross-reviews each other's work, revises under pressure, disputes remaining disagreements, and produces a synthesized verdict. The engine supports 4 game theory modes (cooperative, winner-take-all, prisoner's dilemma, red-blue) and 13 execution providers spanning cloud APIs, local models, and CLI coding agents.

## Quickstart

```bash
# Install from GitHub
pip install git+https://github.com/Build-Fractal/conversus-oss.git

# Zero-cost local deliberation (requires ollama)
ollama pull qwen3:0.6b
conversus decide "Microservices vs monolith for a 3-person team?" --provider ollama

# Using your Claude subscription (if claude CLI is installed)
conversus decide "Microservices vs monolith?" --provider claude-code --model opus

# Full pipeline from config
conversus run my-review.yml --provider claude-code
```

## Providers

Conversus wraps any CLI agent or API as a deliberation participant. 13 providers ship built-in across 4 tiers (`demo` is a friendly alias for `mock`):

| Provider | Type | Tool Use | Cost | Install |
|---|---|---|---|---|
| `mock` (alias: `demo`) | Direct SDK | No | Free | Built-in |
| `anthropic` | Direct SDK | No | Paid | `ANTHROPIC_API_KEY` |
| `claude-code` | Subprocess | Yes | Paid | `npm i -g @anthropic-ai/claude-code` |
| `claude-desktop` | MCP sampling | Yes | Paid | Claude Desktop with conversus MCP server |
| `aider` | Subprocess | Yes | Paid | `pip install aider-chat` |
| `opencode` | Subprocess | Yes | Paid | [opencode.ai](https://opencode.ai/) |
| `codex` | Subprocess | Yes | Paid | `npm i -g @openai/codex` |
| `gemini` | Subprocess | Yes | Paid | `npm i -g @google/gemini-cli` |
| `copilot` | Subprocess | No | Paid | `gh extension install github/gh-copilot` |
| `pi` | Subprocess | No | Paid | Inflection CLI |
| `ollama` | HTTP/OpenAI | No | Free | [ollama.com](https://ollama.com/download) |
| `llama-cpp` | HTTP/OpenAI | No | Free | `brew install llama.cpp` |
| `vllm` | HTTP/OpenAI | No | Free | `pip install vllm` |

## Heterogeneous Deliberation

Different agents can use different providers in the same deliberation — the marquee feature:

```yaml
# conversus.yml
subject: "Architecture Review"
question: "Review the migration plan"
mode: red-blue

target:
  - migration-plan.md

output: review-output/

agents:
  - name: cloud-advocate
    provider: claude-code
    model: opus
    role: blue
    prompt: "Defend the cloud migration plan..."

  - name: skeptic
    provider: ollama
    model: llama3:70b
    role: red
    prompt: "Challenge every assumption..."

  - name: cost-analyst
    provider: anthropic
    model: haiku
    role: red
    prompt: "Analyze cost implications..."
```

```bash
conversus run conversus.yml
```

Claude Opus defends, a local Llama attacks, and Haiku analyzes costs — all in the same structured deliberation.

## Game Theory Modes

| Mode | Agents | Dynamics |
|---|---|---|
| `cooperative` | All work toward consensus | Collaborative synthesis |
| `winner-take-all` | Compete for best recommendation | Arbiter picks winner |
| `red-blue` | Red team attacks, blue defends | Adversarial stress test |
| `prisoners-dilemma` | Strategic cooperation/defection | Game-theoretic scoring |

## Pipeline Phases

Every deliberation runs through 5 phases (6 with arbitration):

1. **Review** — Each agent writes an independent review
2. **Cross-review** — Agents critique each other's reviews
3. **Revision** — Agents revise under pressure from cross-reviews
4. **Disputes** — Agents identify remaining disagreements
5. **Synthesis** — Unified verdict combining all perspectives
6. **Arbitration** (optional) — Binding resolution of unresolved disputes

## Project Setup

```bash
# Initialize conversus in your project
conversus init

# This creates:
#   .conversus/settings.json    — project defaults
#   .conversus/output/          — deliberation output
#   .claude/settings.json       — permissions for claude-code agents
```

## CLI Reference

```bash
conversus decide "question"          # Quick ad-hoc deliberation
conversus run config.yml             # Full pipeline from config
conversus validate config.yml        # Validate config + cost estimate
conversus init                       # Initialize project
conversus status                     # Check provider auth status
conversus context                    # Debug invocation context
```

## Writing Plugins

The plugin system exposes 4 lifecycle hooks. Plugins are optional — the engine works without any:

```python
from conversus.plugins.base import Plugin, HookPoint, PluginResult

class MyPlugin(Plugin):
    name = "my-plugin"
    hooks = [HookPoint.POST_PHASE_5]

    def execute(self, state):
        return PluginResult(
            recommendation="Your analysis here",
            data={"score": 0.85},
        )
```

## License

Apache-2.0. See [LICENSE](LICENSE) for details.

## Contributing

```bash
git clone https://github.com/Build-Fractal/conversus-oss.git
cd conversus
pip install -e ".[dev]"
pytest -m "not live"  # No API keys needed
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
