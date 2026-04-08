# Conversus Adoption Harness — Proposal

## Problem Statement

Conversus is a powerful multi-agent deliberation framework, but it currently requires:
- Hand-crafting YAML configuration files
- Understanding game theory modes to pick the right one
- Writing agent identity prompts
- Running inside Claude Code (locked to one model, one runtime)
- Technical proficiency to use at all

This limits conversus to power users who already understand multi-agent orchestration. The goal is to make conversus extremely easy to adopt for **everyone** — from non-technical people making everyday decisions to AI-native engineers plugging it into sophisticated workflows.

## Vision

Conversus should be a **general-purpose decision-making tool** usable for:
- Software engineering (spec review, architecture decisions, technology selection)
- Personal decisions (stock picking, career choices, vacation planning)
- Business strategy (market analysis, product direction, hiring decisions)
- Entertainment (movie/book/game recommendations via structured debate)
- Any multi-perspective question where structured disagreement surfaces better answers

## Proposed Architecture

### Three User Tiers

| Tier | User | Interface | Config Effort |
|------|------|-----------|---------------|
| **Just Ask** | Anyone — no technical knowledge | Single natural-language question | Zero — system infers everything |
| **Guided** | PMs, founders, team leads | Step-by-step wizard (spec 003 workflow) | Low — user confirms suggestions |
| **Power** | AI-native engineers | Hand-crafted YAML, full control | Full — user configures everything |

### "Just Ask" Mode

A single entry point where the user describes a question or decision in natural language. The system:

1. Classifies the question type (selection, integration, scoping, stress-test)
2. Auto-generates 2-4 appropriate agents with relevant perspectives
3. Picks the optimal competition mode
4. Runs a lightweight deliberation (2-3 agents, 1 round)
5. Returns a plain-English synthesis with the recommendation, supporting arguments, and dissenting views

Example: "Should I use Redis or Postgres for caching in my Django app?" Auto-generates redis-advocate, postgres-advocate, and architect agents. Runs winner-take-all. Returns a recommendation with trade-off analysis.

Example: "What are the best mid-cap stocks to buy right now?" Auto-generates bull-analyst, bear-analyst, and risk-assessor agents. Runs cooperative. Returns a balanced analysis with conviction levels.

### Distribution Formats

| Format | Audience | How |
|--------|----------|-----|
| **MCP Server** | Users of Claude Code, Cursor, Windsurf, VS Code, Codex | Python MCP server exposing conversus tools |
| **Python CLI** | Developers, CI/CD | `pip install conversus` — Click CLI wrapping the engine |
| **Web App** | Non-technical users | Next.js frontend, Python FastAPI backend |
| **Claude Code Skill** | Claude Code users | Current SKILL.md (maintained as-is) |
| **Python SDK** | Programmatic access | `from conversus import Deliberation` |

### Model Agnosticism

Currently locked to Claude via the Agent tool. Proposed change: use LiteLLM as the model abstraction layer.

```yaml
model:
  provider: anthropic    # or openai, ollama, google, litellm
  name: claude-sonnet-4-6  # any model the provider supports
```

This allows conversus to run on:
- Claude (Anthropic API)
- GPT-4o, o3 (OpenAI API)
- Gemini (Google API)
- Llama, Mistral, etc. (Ollama / vLLM for local)
- Any LiteLLM-supported provider

### MCP Server (Primary Integration Path)

An MCP server makes conversus instantly available in any MCP-compatible tool:

```
Tools exposed:
  conversus_decide     — "just ask" mode
  conversus_define     — spec 003 step 1
  conversus_interests  — spec 003 step 2
  conversus_mode       — spec 003 step 3
  conversus_converge   — full deliberation
  conversus_run        — power user YAML execution
```

### Web Application

For non-technical users, a browser-based interface:

- Landing page: single text input — "What decision are you facing?"
- Live deliberation view: see agents arguing in real-time
- Visual mode picker with plain-language descriptions (not "winner-take-all" but "Pick the best option")
- Result page: clear recommendation with supporting/dissenting arguments
- Decision history: all past deliberations, replayable
- Share links: send a deliberation result to anyone

Tech stack: Next.js frontend, Python FastAPI backend, WebSocket for streaming, PostgreSQL for history.

### Integration with Existing Orchestration Tools

- **spec-kit**: conversus as a spec-kit extension hook. Run deliberation on any spec before planning.
- **gsd2**: conversus as a verification/review step after phase completion, or during discuss-phase to surface competing approaches.
- **Claude Code**: maintain current skill, add MCP server for richer integration.
- **Cursor/Windsurf/VS Code**: via MCP server.
- **OpenAI Codex**: via MCP server (MCP support expected).

### Performance Optimizations

1. Parallel agent dispatch (already built)
2. Smart defaults for "just ask" (2-3 agents, 1 round — fast and cheap)
3. Streaming output for real-time progress
4. Response caching for identical inputs
5. Model tiering: cheap model for cross-reviews, expensive for synthesis
6. Community preset library to avoid writing prompts from scratch

## Proposed Build Order

1. Python engine extraction (SKILL.md logic → Python package)
2. LiteLLM integration (model agnosticism)
3. CLI (`pip install conversus`)
4. "Just ask" mode (NL → auto-config → deliberation → plain English)
5. MCP server (plug into Claude Code, Cursor, Windsurf, VS Code)
6. Spec 003 guided workflow (middle tier)
7. Web app (consumer-facing product)
8. Plugin system (spec 007 — game engine, scoring)

## Open Questions

1. Should the engine be extracted to Python or kept as a SKILL.md with adapters? Python gives portability; SKILL.md keeps the current Claude Code integration simple.
2. Is LiteLLM the right abstraction or should we build a custom provider interface?
3. Should the web app be a SaaS product or self-hostable (Docker)?
4. Should presets be community-contributed (npm-style registry) or curated?
5. Is MCP mature enough to be the primary integration strategy, or should we also build native plugins for Cursor/VS Code?
6. How do we handle multi-agent parallelism outside of Claude Code's Agent tool? (asyncio + concurrent API calls?)
7. Does "just ask" mode risk oversimplifying and producing shallow deliberations?
8. What's the right balance between auto-generating agents and letting users control them?

## Constraints

- Must not break existing `/conversus run` behavior
- Must not require any specific model or provider to function
- Must work for both trivial decisions (dinner) and high-stakes decisions (architecture)
- Must be self-explanatory for non-technical users without documentation
- Must remain useful for power users who want full control
