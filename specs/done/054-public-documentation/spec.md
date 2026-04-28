# Spec 054: Public Documentation & README

**Status**: Draft
**Author**: Brian Slater + Claude Opus 4.6
**Date**: 2026-04-07
**Depends on**: 052 (open source extraction)

---

## 1. Objective

Write the public-facing README.md and documentation for the conversus open-source package. The README is the first thing a potential user sees — it must communicate what conversus does, why it's different, and how to start using it in under 60 seconds.

## 2. README Structure

### 2.1 Hero Section

```markdown
# conversus

Multi-agent deliberation engine. Pit AI agents against each other
in structured adversarial review using game theory modes.

pip install conversus
conversus decide "Should we use Postgres or MongoDB?" --provider ollama
```

### 2.2 Key Sections

1. **What is this?** — 3-sentence explanation
2. **Quickstart** — 60-second path from install to first deliberation
3. **Providers** — Table of 12 providers across 3 tiers
4. **Game Theory Modes** — cooperative, winner-take-all, prisoner's dilemma, red-blue
5. **Heterogeneous Deliberation** — different LLMs arguing (the marquee feature)
6. **Configuration** — conversus.yml example
7. **CLI Reference** — run, decide, validate, init
8. **Plugin System** — how to write plugins
9. **Contributing** — PR guidelines, test requirements
10. **License** — Apache-2.0

### 2.3 Quickstart Flow

```bash
# Install
pip install conversus

# Zero-cost local deliberation (ollama)
ollama pull qwen3:0.6b
conversus decide "Microservices vs monolith?" --provider ollama

# Cloud deliberation (needs API key)
export ANTHROPIC_API_KEY=sk-ant-...
conversus decide "Microservices vs monolith?" --provider anthropic

# Full pipeline from config
conversus init
conversus run my-review.yml --provider claude-code --model opus
```

### 2.4 Provider Table

```markdown
| Provider | Type | Tool Use | Cost | Install |
|---|---|---|---|---|
| mock | Direct SDK | No | Free | Built-in |
| anthropic | Direct SDK | No | Paid | ANTHROPIC_API_KEY |
| claude-code | Subprocess | Yes | Paid | npm i -g @anthropic-ai/claude-code |
| aider | Subprocess | Yes | Paid | pip install aider-chat |
| opencode | Subprocess | Yes | Paid | curl -fsSL https://opencode.ai/install \| bash |
| codex | Subprocess | Yes | Paid | npm i -g @openai/codex |
| gemini | Subprocess | Yes | Paid | npm i -g @google/gemini-cli |
| copilot | Subprocess | No | Paid | gh extension install github/gh-copilot |
| pi | Subprocess | No | Paid | Inflection CLI |
| ollama | HTTP/OpenAI | No | Free | https://ollama.com/download |
| llama-cpp | HTTP/OpenAI | No | Free | brew install llama.cpp |
| vllm | HTTP/OpenAI | No | Free | pip install vllm |
```

## 3. Additional Documentation

### 3.1 docs/ Directory

```
docs/
├── quickstart.md          # Extended quickstart tutorial
├── providers.md           # Provider deep-dive with auth setup
├── configuration.md       # conversus.yml reference
├── game-modes.md          # Game theory mode explanations
├── heterogeneous.md       # Per-agent provider setup
├── plugins.md             # Writing custom plugins
├── architecture.md        # ExecutionProvider protocol, dispatch flow
├── ci-integration.md      # Running in CI/CD (GitHub Actions, etc.)
└── contributing.md        # Development setup, test requirements
```

### 3.2 CONTRIBUTING.md

- Development setup: `git clone && pip install -e ".[test]"`
- Test: `pytest -m "not live"` (no API keys needed)
- Coverage: must maintain >85%
- PR process: tests pass, ruff clean, no coverage regression
- Architecture: ExecutionProvider protocol, SubprocessProvider for CLIs

### 3.3 CHANGELOG.md

Follow Keep a Changelog format. Start with v0.1.0 covering the initial release scope.

## 4. Non-Goals

- No hosted documentation site for v0.1.0 (README + docs/ is sufficient)
- No video tutorials (text-first)
- No blog post at launch (save for v0.2.0 with community feedback)

## 5. Success Criteria

- README has install → first result in under 60 seconds
- All 12 providers documented with install commands
- At least one heterogeneous deliberation example
- CONTRIBUTING.md enables first-time contributors
- No private repo references in any public documentation
