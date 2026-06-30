# Architecture

Deliberator is organized into three layers with strict coupling rules.

!!! info "Design history"
    The architecture below is the result of specs and deliberations in the repo.
    See [Specs & Deliberations](specs-and-deliberations.md) for the decision record,
    including the packaging strategy deliberation that produced the three-layer model.

## Three layers

```
┌─────────────────────────────────────────────────────┐
│  domains/        Vertical domain plugins            │
│  (code-review, future: security, compliance, ...)   │
│  MAY import: deliberator.domains.base, deliberator.schemas, stdlib
│  MUST NOT import: engine.*, linter.*, web.*         │
├─────────────────────────────────────────────────────┤
│  deliberator/      Solvers + plugin infrastructure    │
│  (plugins/, schemas/, domains/)                     │
│  MAY import: pydantic, stdlib                       │
│  MUST NOT import: engine.*                          │
├─────────────────────────────────────────────────────┤
│  engine/         Core deliberation engine (free)    │
│  (cli/, providers/, phases, dispatch, events, sdk)  │
│  MAY import: deliberator.schemas, linter              │
│  linter/         Template validation + quality      │
│  web/            FastAPI backend                     │
└─────────────────────────────────────────────────────┘
```

**Key coupling rules:**
- The `deliberator/` package imports nothing from `engine/`, `linter/`, `web/`, or `mcp_server`.
- Domain plugins import only from `deliberator.domains.base`, `deliberator.schemas`, and stdlib.
- The engine imports from `deliberator.schemas` and `linter` but never from `deliberator.plugins` or `deliberator.domains` directly.

## Package boundaries

| Package | Contents | Dependencies |
|---------|----------|-------------|
| `engine/` | CLI, providers, phases pipeline, dispatch, events, SDK, auth, config, cost, templates | pydantic, click, anthropic, openai, yaml, rich |
| `linter/` | Template validation, output contract parsing, question classifier, quality checks | pydantic, yaml |
| `web/` | FastAPI app, Supabase DB, analyze endpoint | fastapi, supabase |
| `deliberator/schemas/` | Game forms, modes, objectives, features, construction pipeline, extraction, validation | pydantic, yaml |
| `deliberator/plugins/` | Plugin base class, hook execution, nashopt scorer, optimizer, scenarios | pydantic |
| `deliberator/domains/` | Domain plugin base, store (JSONL/SQLite), API router factory, code-review domain | pydantic, fastapi (api.py only) |
| `templates/` | Prompt templates -- 7 per mode (review, cross-review, revision, disputes, synthesis, arbitration, cross-round-synthesis) | N/A (markdown) |
| `schema/` | YAML schemas -- game forms, modes, features, objective functions, variables | N/A (data) |
| `presets/` | Agent presets -- YAML files organized by category | N/A (data) |

## Data flow

```
question / config.yml
        │
        ▼
   ┌─────────┐
   │  parse   │  engine/config.py: YAML → EngineConfig (frozen Pydantic)
   │  config  │  Resolves presets, targets, prior files, agent names
   └────┬─────┘
        │
        ▼
   ┌─────────┐
   │ resolve  │  engine/auth.py: provider name → ModelProvider
   │ provider │  env var → OAuth store → error
   └────┬─────┘
        │
        ▼
   ┌──────────────────────────────────────────┐
   │  run_pipeline (engine/phases.py)          │
   │                                           │
   │  for round in 1..rounds:                  │
   │    Phase 1: review (N parallel agents)    │
   │    for iter in 1..iterations:             │
   │      Phase 2: cross-review (NxN-1 pairs) │
   │      Phase 3: revision (N parallel)       │
   │    Phase 4: disputes (N parallel)         │
   │    Phase 5: synthesis (1 sequential)      │
   │    stagnation check → break if converged  │
   │                                           │
   │  cross-round synthesis (if rounds >= 2)   │
   │  Phase 6: arbitration (if configured)     │
   └────┬─────────────────────────────────────┘
        │
        ▼
   ┌──────────┐
   │  output   │  OutputManager writes markdown files
   │  files    │  summary/final.md is the synthesis
   └────┬──────┘
        │
        ▼
   ┌──────────┐
   │  parse    │  linter/output_contract.py: synthesis → DeliberatorOutput
   │  output   │  headline, summary, quality indicators, disputes
   └──────────┘
```

## Pipeline invariants

1. **Phase barriers**: No phase starts until the previous phase completes for all agents.
2. **Continue-with-N-1**: If an agent fails in any phase, it drops out. Pipeline continues as long as at least 1 agent survives.
3. **Independent agents**: Every output file is produced by its own independent agent with isolated context. No agent sees another's raw response during the same phase.
4. **Frozen models**: All Pydantic models use `model_config = {"frozen": True}`. No mutation after construction.
5. **Stagnation detection**: Multi-round mode stops early if dispute count does not decrease between rounds.

## Equilibrium scoring

The nashopt plugin provides equilibrium scoring via two paths:

- **Heuristic path** (default, zero dependencies): Per-agent payoff functions in `payoffs.py` compute `(payoff, best_response_payoff)` tuples. The scorer aggregates these into a 0.0-1.0 equilibrium score.
- **Solver path** (requires `nashopt` + `jax`): `solver.py` constructs per-mode payoff matrices and calls `nashopt.check_equilibrium()` for exact Nash equilibrium computation.

**Matrix shapes by mode**: Cooperative and prisoners-dilemma produce N x N matrices. Winner-take-all produces N x 1 (a degenerate case of the general N x N x A form where A=1). Red-blue produces 2 x K (severity levels).

**Cooperative payoff matrix caveat**: The cooperative mode's matrix mixes `surviving_count` (diagonal) with `agreement_matrix` (off-diagonal). This is a **heuristic approximation** -- it produces a useful stability signal but not a game-theoretically grounded equilibrium. The heuristic scorer is the intended consumer. A solver-correct cooperative matrix would need a single consistent data source for all entries. See spec 021 amendment RE-3.

## Event system

The engine emits lifecycle events through the `EventEmitter` protocol. Three implementations:

| Emitter | Transport | Use case |
|---------|-----------|----------|
| `CallbackEmitter` | Sync callback | CLI (Rich progress), SDK |
| `AsyncQueueEmitter` | asyncio.Queue | Web (SSE streaming) |
| `NullEmitter` | Discard | MCP server, tests |

Events are frozen Pydantic models. No transport assumption -- the emitter just receives events and decides what to do.

## Template system

Templates live in `templates/{mode}/` with 7 files per mode. Template variables (defined in `schema/variables.yml`) are filled by context builders in `engine/templates.py`. The linter validates all templates against the variable schema.

Key variables: `{AGENT_NAME}`, `{AGENT_PROMPT}`, `{MODE}`, `{TARGET_FILES}`, `{AGENT_DOCS}`, `{OUTPUT_PATH}`, `{DISPUTES_BEGIN}`, `{DISPUTES_END}`.

## Domain-engine integration

Domains operate alongside -- but are decoupled from -- the core engine pipeline. The engine imports from `deliberator.schemas` and `linter` but never from `deliberator.domains` directly. Domains are activated via configuration and execute their own lifecycle.

### Where domains fit in the deliberation lifecycle

```
  Engine pipeline (engine/phases.py)        Domain pipeline (domains/base.py)
  ──────────────────────────────────        ────────────────────────────────
  Config parsing                            Domain + store instantiation
         │                                           │
         ▼                                           ▼
  Phases 1-5: deliberation rounds           Extract: run VariableExtractors
         │                                  against workspace + changed_files
         ▼                                           │
  Post-deliberation                                  ▼
         │                                  Score: evaluate variables against
         ▼                                  scaffold (weights, thresholds,
  Arbitration (optional)                    hard blocks) → DomainScore
                                                     │
                                                     ▼
                                            Persist: create_record() → store
                                                     │
                                                     ▼
                                            Serve: REST API via router factory
```

### Integration points

- **Domain extraction** happens independently of the engine rounds. A domain can be triggered before a deliberation (to score the input artifact), after (to score the output), or both.
- **Domain scoring** uses scaffolds (YAML weight configs) that are separate from the engine's template system. Scaffolds define what quality means for that domain; engine templates define how agents deliberate.
- **Domain persistence** writes `DomainRecord` objects to a store (JSONL or SQLite). These records are not part of the engine's output directory -- they live in a separate review store that accumulates across runs.
- **Plugins bridge the two.** A plugin subscribed to `POST_DELIBERATION` can instantiate a domain, run extraction and scoring against the deliberation output, and emit the domain score as plugin data for downstream consumers.

### Coupling rules

Domains import only from `deliberator.domains.base`, `deliberator.schemas`, and stdlib. They never import from `engine/`, `linter/`, `web/`, or `mcp_server`. This means domain logic is testable in isolation without the engine installed.
