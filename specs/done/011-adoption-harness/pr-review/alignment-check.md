# Alignment Check: Engine Implementation vs Completed Specs

After merging main into the 011-adoption-harness branch, the following 9 specs that were completed on main now coexist with the PR's engine implementation. The question is whether the engine respects, conflicts with, or is unaware of each spec's requirements.

## Specs to Check

### Guided Workflow Layer (SKILL.md commands)
- **007 — Subcommand Dispatch & Define**: `/conversus define` handler, dispatch routing
- **008 — Interests & Mode**: `/conversus interests`, `/conversus mode` handlers
- **009 — Guided Execution**: `/conversus converge` wrapper
- **010 — Guided Arbitration**: `/conversus arbitrate` handler
- **011 — Phase Consensus Gates**: `/conversus gate` handler

### Engine Layer (SKILL.md execution model)
- **006 — Inter-Round Arbitration**: `timing` and `influence` fields, Phase 6 inter-round firing

### Schema Layer (Python code, new packages)
- **011a — SKILL.md Decomposition**: SKILL.md structural changes
- **012 — Game Form Schemas**: `conversus/schemas/game_forms.py`, YAML schemas
- **013 — Objective Function Templates**: `conversus/schemas/objectives.py`, YAML templates

## Key Questions

1. Does the engine's `parse_config()` handle `timing` and `influence` fields from spec 006?
2. Does the engine's `run_pipeline()` support inter-round arbitration (Phase 6 between rounds)?
3. Does the engine recognize the guided workflow subcommands, or does it only handle `run`?
4. Do the game form schemas in `conversus/schemas/` integrate with the engine's config/template system?
5. Are there import conflicts between the engine package and the new schemas package?
6. Does the engine's MCP server expose tools for the guided workflow commands?
7. Does SKILL.md's current structure (post-011a decomposition) match what the engine was built from?

## Context

The engine (M001-M005) was built from SKILL.md as it existed before specs 006-013 were implemented. The engine extracted concepts from SKILL.md into Python, but SKILL.md has since evolved significantly. The risk is that the engine is a snapshot of an older SKILL.md.
