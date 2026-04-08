# Implementation Plan: Agent Antipattern Steering

**Branch**: `010-antipattern-steering` | **Date**: 2026-03-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/010-antipattern-steering/spec.md`

## Summary

Create a structured antipattern catalog that records observed agent behavioral mistakes with enough context for agents to recognize and avoid repeating them. Integrate the catalog into conversus agent prompts via SKILL.md instructions so agents check it before proposing new artifacts. The catalog is a single markdown file with a summary index and self-contained entries, seeded with the "redundant-cache" antipattern from the STATUS.md incident. P2 adds keyword-based retrieval for scaling beyond 10 entries.

## Technical Context

**Language/Version**: Markdown (specification documents, no code)
**Primary Dependencies**: SKILL.md (agent orchestration spec), conversus templates, constitution.md
**Storage**: Filesystem — single markdown catalog file + SKILL.md edits
**Testing**: Manual acceptance testing via agent behavioral verification against acceptance scenarios
**Target Platform**: AI agent context (Claude Code, conversus deliberation agents)
**Project Type**: Specification/documentation artifact (prompt engineering)
**Performance Goals**: Antipattern check adds <30s overhead to agent task startup (SC-002); catalog supports 50+ entries before retrieval degrades (SC-003)
**Constraints**: Every entry must reference a real observed incident (SC-004); catalog is append-mostly (FR-010); entries are self-contained (FR-004)
**Scale/Scope**: Initial seed of 1 antipattern entry, designed to scale to 50+ entries with keyword retrieval

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Status | Notes |
|---|-----------|--------|-------|
| I | Spec-Driven Development | PASS | Spec 010 exists and precedes implementation |
| II | Stable Interfaces | PASS | No existing interfaces modified; catalog is a new artifact. SKILL.md additions are additive |
| III | Backward-Compatible Extension | PASS | Adds new catalog and agent instructions; no existing behavior changes. Omitting the catalog preserves current behavior |
| IV | Documentation Is the Product | PASS | The catalog and SKILL.md instructions ARE the implementation — documentation is literally the product here |
| V | Observable Deliberation | N/A | Feature does not modify phase execution or output validation |
| VI | Scripts Over Markdown | JUSTIFIED | The catalog is markdown consumed by agents as reading context, not parsed programmatically. Agents read markdown natively — structured YAML would add parsing overhead without benefit. The catalog uses structured sections (frontmatter-like headers per entry) to remain machine-scannable. See Complexity Tracking |
| VII | Reproducibility Over Inconsistency | PASS | Same catalog contents produce same agent behavior. No ambient state |
| VIII | Templating Engines Over Inference | JUSTIFIED | Antipattern matching is inherently a reasoning task — agents must judge whether current work resembles a cataloged pattern. Templates constrain the check with explicit instructions (read index first, match by symptoms, cite the entry). See Complexity Tracking |
| IX | Zen of Python Output | PASS | Single catalog file, flat structure, scannable index at top, one entry = one purpose |

**Gate result**: PASS (2 justified deviations, 0 violations)

## Project Structure

### Documentation (this feature)

```text
specs/010-antipattern-steering/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── catalog-format.md
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Implementation Files (repository root)

```text
conversus/
├── SKILL.md                          # ADD: antipattern check instruction in agent prompt section
├── antipatterns/
│   └── catalog.md                    # NEW: the antipattern catalog with summary index + entries
├── .specify/memory/constitution.md   # UPDATE: Known Antipatterns section references catalog location
└── antipatterns/
    └── examples/redundant-cache/     # EXISTING: seed data for first catalog entry
```

**Structure Decision**: No `src/` or `tests/` directories — this feature is pure documentation/specification. The catalog lives in `antipatterns/catalog.md` at the conversus root, adjacent to `presets/` and `templates/`, following the flat project layout convention. SKILL.md edits add agent instructions inline.

## Complexity Tracking

> **Justified deviations from Constitution Check**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| VI. Markdown catalog (not YAML/script) | Agents consume the catalog by reading it as context, not by parsing it programmatically. Markdown with structured sections is the most natural format for both agent consumption and human maintenance | YAML catalog would require a parsing/rendering step to present entries to agents. The catalog IS the prompt content — rendering adds complexity for no benefit |
| VIII. Agent inference for pattern matching | Recognizing whether current work matches an antipattern is inherently a judgment call — no mechanical rule can cover all cases | A rule-based matcher would require encoding all possible symptom variations, which is brittle and would miss novel manifestations of known antipatterns. The spec constrains inference with structured entries and explicit check instructions |
