# Task: Make Conversus Executable

**Status**: Done — closed 2026-04-27 per spec hygiene audit. Implemented by SKILL.md; conversus CLI executes deliberations from `conversus.yml` today.

## Goal

Build a CLI skill that reads a `conversus.yml` config file and executes the full 5-phase deliberation process — launching parallel agents, collecting outputs, and producing the synthesis — without manual orchestration.

## Input

A `conversus.yml` in the target directory:

```yaml
mode: cooperative                    # cooperative | winner-take-all | prisoners-dilemma | red-blue
target: specs/001-speckit-orchestrator/spec.md
output: specs/001-speckit-orchestrator/conversus/
iterations: 1                        # number of review/revision cycles

agents:
  - name: apm
    prompt: |
      You are APM (Agent Package Manager). You represent the perspective
      of packaging, distribution, context compilation, and agent primitives.
    docs:
      - apm/docs/
      - apm/README.md

  - name: spec-kit
    prompt: |
      You are spec-kit (the SDD framework). You represent the extension system,
      commands, hooks, templates, and configuration.
    docs:
      - spec-kit/README.md
      - spec-kit/templates/
      - spec-kit/extensions/

  - name: gh-aw
    prompt: |
      You are gh-aw (GitHub Agentic Workflows). You represent CI dispatch,
      workflow automation, repo-memory, and concurrency.
    docs:
      - gh-aw/docs/
      - gh-aw/README.md
```

## Output

Running `/conversus run` (or `conversus run conversus.yml`) produces:

```
{output}/
├── {agent}/
│   ├── review.md
│   ├── revision.md
│   ├── disputes.md
│   └── cross-reviews/
│       └── {other-agent}.md
└── summary/
    └── final.md
```

## Implementation Plan

### Phase 1: Skill Definition

Create a Claude Code skill at `conversus/SKILL.md` that:
- Triggers on `/conversus run` or `/conversus run <path-to-config>`
- Reads `conversus.yml` from CWD or specified path
- Validates the config (mode, agents, target exist)

### Phase 2: Prompt Templates

Create prompt templates per mode × phase in `conversus/templates/`:

```
templates/
├── cooperative/
│   ├── review.md        # Phase 1 prompt template
│   ├── cross-review.md  # Phase 2 prompt template
│   ├── revision.md      # Phase 3 prompt template
│   ├── disputes.md      # Phase 4 prompt template
│   └── synthesis.md     # Phase 5 prompt template
├── winner-take-all/
│   ├── review.md
│   ├── cross-review.md
│   ├── revision.md
│   ├── disputes.md
│   └── synthesis.md
├── prisoners-dilemma/
│   ├── ...
└── red-blue/
    ├── ...
```

Each template uses `{variables}` that the skill fills from the config:
- `{agent_name}`, `{agent_prompt}`, `{target_path}`, `{output_dir}`
- `{other_agent_name}`, `{other_agent_review_path}`
- `{all_revision_paths}`, `{all_artifact_paths}`

### Phase 3: Orchestration Engine

The skill's main loop:

```
1. Parse conversus.yml
2. Validate config
3. Create output directory structure
4. For each iteration:
   a. Phase 1 — Launch N agents in parallel (one per agent)
      - Fill review template with agent config
      - Wait for all to complete
   b. Phase 2 — Launch N*(N-1) agents in parallel
      - Fill cross-review template with pairs
      - Wait for all to complete
   c. Phase 3 — Launch N agents in parallel
      - Fill revision template with cross-review paths
      - Wait for all to complete
   d. Phase 4 — Launch N agents in parallel
      - Fill disputes template with revision paths
      - Wait for all to complete
5. Phase 5 — Launch 1 synthesis agent
   - Fill synthesis template with all artifact paths
   - Wait for completion
6. Report results
```

The skill uses Claude Code's `Agent` tool for parallel dispatch. Each agent gets:
- The filled prompt template
- Instructions to read specific files (target, docs, other agents' outputs)
- Instructions to write to a specific output path

### Phase 4: Mode-Specific Scoring

For modes that score agents (Prisoner's Dilemma, Winner Take All):
- Scoring criteria embedded in the synthesis prompt template
- Synthesis agent produces scores as part of `final.md`
- No separate scoring infrastructure needed initially

### Phase 5: Config Validation

The skill validates before running:
- `mode` is one of the four supported modes
- `target` file exists
- All agent `docs` paths exist
- `output` directory is writable
- For `red-blue` mode: at least one agent has `role: red` and one `role: blue`

## Key Decisions

1. **Skill, not CLI** — runs inside Claude Code via `/conversus run`, not as a standalone binary. This gives us `Agent` tool for parallel dispatch without building process management.

2. **Templates, not hardcoded prompts** — prompt engineering lives in markdown files, not code. Users can customize mode behavior by editing templates.

3. **YAML config, not CLI flags** — a `conversus.yml` is reproducible, committable, and self-documenting. Complex agent definitions don't fit in CLI args.

4. **Iterations configurable** — default 1 (5 phases). Can set higher for deeper deliberation (each iteration adds another cross-review → revision cycle before disputes).

## Files to Create

```
conversus/
├── SKILL.md                         # Claude Code skill definition
├── README.md                        # Already exists (docs)
├── templates/
│   ├── cooperative/
│   │   ├── review.md
│   │   ├── cross-review.md
│   │   ├── revision.md
│   │   ├── disputes.md
│   │   └── synthesis.md
│   ├── winner-take-all/
│   │   ├── review.md
│   │   ├── cross-review.md
│   │   ├── revision.md
│   │   ├── disputes.md
│   │   └── synthesis.md
│   ├── prisoners-dilemma/
│   │   ├── review.md
│   │   ├── cross-review.md
│   │   ├── revision.md
│   │   ├── disputes.md
│   │   └── synthesis.md
│   └── red-blue/
│       ├── review.md
│       ├── cross-review.md
│       ├── revision.md
│       ├── disputes.md
│       └── synthesis.md
└── tasks/
    └── 001-executable-conversus.md  # This file
```

## Acceptance Criteria

- [ ] `/conversus run` reads `conversus.yml` and executes all 5 phases
- [ ] Agents run in parallel within each phase
- [ ] All four modes produce correct prompt templates
- [ ] Output directory structure matches spec
- [ ] Config validation catches missing files, invalid modes
- [ ] A re-run of the speckit-orchestrator conversus using the skill produces equivalent output
- [ ] `conversus.yml` is the single source of truth for a run — no manual prompt crafting needed

---

## Closure note (2026-04-27)

**Why closed**: Implemented by `SKILL.md` and the conversus CLI (`/conversus run`). The CLI today reads a `conversus.yml`, dispatches agents in parallel through the 5-phase pipeline, collects outputs, and produces synthesis — exactly the goal stated above. `ideas.md` confirms: "008 was already implemented by SKILL.md."

**Where the work lives**:
- `SKILL.md` (repo root) — the executable skill definition
- `engine/cli/` — `/conversus run`, `validate`, `init` commands
- `engine/dispatch.py` — agent dispatch + events
- `engine/phases.py` — 5-phase pipeline

**Reference**: `specs/AUDIT-2026-04-27.md` §A "008-executable-conversus" — definitively shipped, recommended close.
