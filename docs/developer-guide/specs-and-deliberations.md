# Specs and Deliberations

Conversus decisions are documented as specs in the repo, and many of them were produced by running conversus on itself — multi-agent deliberations evaluating proposals before implementation.

This page links to the authoritative sources on GitHub rather than duplicating content here. The repo provides better browsing, history, file linking, and search than a docs mirror could.

## Specs

All active and completed specs live in [`specs/`](https://github.com/Build-Fractal/conversus-oss/tree/main/specs) on GitHub.

### Featured specs

| Spec | What it covers |
|------|----------------|
| [distribution-strategy](https://github.com/Build-Fractal/conversus-oss/blob/main/specs/distribution-strategy.md) | Three-layer OSS distribution: PyPI, MCP server, Claude Code plugin. Covers Cowork, Claude Desktop, and claude.ai Skills compatibility. |
| [007-game-engine](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/007-game-engine) | The deliberation engine — phases, agents, game theory modes |
| [008-executable-conversus](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/008-executable-conversus) | CLI + SDK interface for running deliberations |
| [042-execution-providers](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/042-execution-providers) | Provider abstraction: anthropic, openai, claude-code, ollama, etc. |
| [043-ampl-game-solvers](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/043-ampl-game-solvers) | AMPL-based solvers for equilibrium computation |
| [048-autonomous-governance-mode](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/048-autonomous-governance-mode) | Unattended deliberation mode for CI/CD |
| [049-universal-skill-mcp-server](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/049-universal-skill-mcp-server) | MCP server exposing conversus to any MCP-compatible editor |
| [052-open-source-extraction](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/052-open-source-extraction) | OSS/paid boundary — what lives in conversus-oss vs. the paid version |
| [054-public-documentation](https://github.com/Build-Fractal/conversus-oss/tree/main/specs/054-public-documentation) | This docs site — scope, structure, and principles |

Browse the full list: [specs/ directory](https://github.com/Build-Fractal/conversus-oss/tree/main/specs)

## Deliberations

Each deliberation is a real run of conversus, preserved with the config, proposal, per-agent reviews, cross-reviews, revisions, disputes, and final synthesis. Read them as case studies of the tool in action.

### Packaging strategy

**Question**: How should conversus be packaged and distributed? PyPI, Claude Code plugin, MCP server, APM, or something else?

- **Mode**: mechanism-design
- **Agents**: 4 (APM maximizer, non-tech user, technical power user, fact-based arbiter)
- **LLM launches**: 29
- **Outcome**: Three-layer architecture — PyPI canonical package, MCP as universal protocol, Claude Code plugin for marketplace reach

[Read the full deliberation →](https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations/packaging-strategy)

### Docs review

**Question**: Are the conversus OSS docs accurate, accessible to new users, and mergeable with paid docs?

- **Mode**: cooperative
- **Agents**: 3 + arbiter (code-verifier, new-user, mergeability-auditor, docs-architect)
- **LLM launches**: 17
- **Outcome**: P1 fixes for install instructions, CLI command count, and paid-feature references. Docs approved for release.

[Read the full deliberation →](https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations/docs-review)

### Docs-specs integration (meta)

**Question**: How should specs and deliberations be surfaced in these very docs?

- **Mode**: cooperative
- **Agents**: 4 + arbiter (information-architect, decision-log-advocate, meta-showcase-advocate, minimalist)
- **LLM launches**: 26
- **Outcome**: This page. Option F — link out to GitHub, duplicate nothing.

[Read the full deliberation →](https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations/docs-specs-integration)

## Running your own deliberations

Every deliberation above started with a `conversus.yml` config and a proposal markdown file. You can adapt them for your own decisions:

```bash
# Copy a deliberation structure
cp -r deliberations/packaging-strategy deliberations/my-decision
# Edit the proposal.md with your question
# Edit the conversus.yml with your agents
conversus run deliberations/my-decision/conversus.yml --provider claude-code
```

See the [Modes](../user-guide/modes.md) page for when to use cooperative, mechanism-design, red-blue, and other modes.
