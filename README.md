# conversus

**Stop trusting single-LLM answers that sound confident even when wrong.** Conversus pits AI agents against each other in structured adversarial review so weak arguments get exposed *before* you ship the decision.

```bash
pip install git+https://github.com/Build-Fractal/conversus-oss.git
conversus decide "Should we use Postgres or MongoDB?" --provider mock
```

The `--provider mock` flag runs the full 5-phase pipeline with synthetic responses — no API key, nothing to install, no cost. You see exactly what conversus does in ~10 seconds. Swap to a real provider once you're sold.

## What is this?

Conversus orchestrates multiple AI agents in structured debates. Each agent reviews a target document from a different perspective, cross-reviews each other's work, revises under pressure, disputes remaining disagreements, and produces a synthesized verdict. The engine supports 8 game theory modes (cooperative, winner-take-all, prisoner's dilemma, red-blue, negotiation, resource-allocation, fair-division, mechanism-design) and 13 execution providers spanning cloud APIs, local models, and CLI coding agents.

## Why conversus?

| If you've used... | Conversus differs by... |
|---|---|
| **CrewAI / AutoGen** | Adversarial-by-default. Agents critique each other through a *structured* cross-review phase, not just a chat loop. Disagreements get surfaced as explicit disputes rather than averaged away. |
| **LangGraph** | No graph to design. The 5-phase pipeline is fixed; you configure agents and mode. Game-theory mode (red-blue, prisoner's dilemma, etc.) selects the competitive dynamic. |
| **AutoGPT / single-agent loops** | Multiple agents with *different* providers (e.g. Claude defends, local Llama attacks, GPT scores) in one deliberation. Heterogeneous deliberation is the marquee feature. |
| **Just asking Claude / GPT once** | Conversus produces a record. Every position, cross-review, revision, and dispute is written to disk. You can read *why* the verdict landed where it did and audit the deliberation post-hoc. |

## Showcase: deliberations that earned their keep

These are real deliberations from the project's own development — kept because they caught things single-stage review missed.

- **[v4.1.0 persistence-contract self-consistency](deliberations/v4.1.0-persistence-contract-discipline-self-consistency-2026-05-12/)** — four agents unanimously caught a tier-evidence mismatch that a single review pass had approved. The amendment was reworked before ratification.
- **[v2.3.0 blind-verification](deliberations/v2.3.0-blind-verification-2026-04-25/)** — surfaced an internal constitutional contradiction with line-precise citations. Used to seed the "blind verification" pathway now baked into the constitution.
- **[061 engine-eval-suite](deliberations/061-engine-eval-suite-2026-04-16/)** — spec-review deliberation accidentally surfaced **four real engine code bugs** that pytest hadn't covered.

For the project's own discovery that it was systematically biased toward ratifying its own proposals — and how it amended the protocol to correct that — see [CONSTITUTIONAL_CONVERSATIONS.md](CONSTITUTIONAL_CONVERSATIONS.md).

## Quickstart

```bash
# Install from GitHub
pip install git+https://github.com/Build-Fractal/conversus-oss.git

# Zero-cost mock deliberation — no API keys, runs in seconds
conversus decide "Microservices vs monolith for a 3-person team?" --provider mock

# Real LLM via your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...
conversus decide "Microservices vs monolith?" --provider anthropic

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
#   .conversus/settings.yml       — project defaults (provider, model, mode)
#   .conversus/deliberations/     — output directory for `decide` and `run`
#   .claude/settings.json         — permissions for claude-code agents
#   ~/.conversus/settings.yml     — global defaults
```

## CLI Reference

```bash
# Running deliberations
conversus decide "question"                       # Quick ad-hoc deliberation
conversus run config.yml                          # Full pipeline from config
conversus run config.yml --phase review           # Stop after Phase 1 (initial reviews)
conversus validate config.yml                     # Validate config + cost estimate
                                                  # Add `arbiter:` block to config for Phase 6

# Project setup
conversus init                                    # Initialize .conversus/ in project
conversus status                                  # Check provider auth + settings cascade
conversus context                                 # Debug invocation context (runtime/provider)

# Auth
conversus login anthropic                         # OAuth login (also: openai)
conversus logout anthropic                        # Remove stored credentials

# Integration
conversus mcp                                     # Start MCP server (stdio transport)
conversus snap                                    # Snap-verdict for Claude Code PreToolUse hooks

# Skill discovery
conversus skills                                  # List all skills
conversus skill <name>                            # Print a SKILL.md guided workflow
```

12 commands total. Full reference with options + defaults: [docs/user-guide/cli.md](docs/user-guide/cli.md). Things going wrong? See [Troubleshooting & FAQ](docs/user-guide/troubleshooting.md).

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

## What's new

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## Contributing

```bash
git clone https://github.com/Build-Fractal/conversus-oss.git
cd conversus
pip install -e ".[dev]"
pytest -m "not live"  # No API keys needed
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
