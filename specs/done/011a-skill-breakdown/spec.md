# Spec 011a: SKILL.md Decomposition

## Problem Statement

The conversus SKILL.md has grown to 2216 lines / 31k tokens — roughly 4x the agentskills.io recommended maximum of 500 lines / 5,000 tokens. Every invocation loads all 31k tokens regardless of which subcommand runs. A `/conversus define` invocation pays for the entire run engine, gate handler, and arbitration subsystem it will never use.

## Deliberation Record

This spec was hardened through a 5-agent cooperative conversus deliberation with inter-round binding arbitration:
- **Agents**: functional-decomposition, integration-specialist, apm-specialist, agentskills-specialist, agents-md-specialist
- **Phases**: 5 reviews, 20 cross-reviews, 5 revisions, 5 disputes, 1 synthesis, 1 arbitration
- **Result**: 37 agents launched, converged in 1 round after 4 binding arbiter rulings
- **Output**: `conversus/specs/011a-skill-breakdown/conversus-output/`

## Binding Arbiter Rulings

The following decisions are settled and non-negotiable:

1. **Run engine stays in root SKILL.md.** The two-hop chain problem (converge → handler-converge.md → handler-run.md) has no clean loading trigger. Silent degradation (agent orchestrating with a summary instead of the full engine spec) is worse than token overhead. Extraction permitted only after empirical testing post-Phase 2 demonstrates zero degradation.

2. **Multi-round orchestration is never extracted.** Single-round behavior is defined as the negation of multi-round behavior ("the multi-round loop with rounds=1"). Splitting them creates two sources of truth. The "do not decompose" constraint applies unconditionally — no dependency analysis gate.

3. **Two-tier naming convention.** `handler-` for subcommand dispatch targets, `subsystem-` for shared dependencies. No third tier (`notes-`) until 3+ informational files warrant it.

4. **Validation rules deferred.** Co-location in each handler is the default. A shared `subsystem-validation-rules.md` is created only if empirical count of patterns in 3+ handlers reaches 4+.

## Decomposition Mechanism

**`references/` conditional loading** is the primary decomposition mechanism (not APM sub-skills). This was the strongest consensus of the deliberation — all 5 agents converged after the apm-specialist withdrew sub-skill promotion, conceding that "APM solves distribution problems; conversus has a context window problem."

APM sub-skill promotion is deferred until the spec suite stabilizes and a second independent consumer appears.

## Target Architecture

After decomposition, the SKILL.md contains:
- Subcommand dispatch table with Class A load triggers (~40 lines)
- Non-negotiable multi-agent rules (~15 lines)
- Run engine: config parsing, validation, phase pipeline, template variable expansion, round/iteration state machine, dispute-parsing subsystem (~500-700 lines)
- Important Notes / operational gotchas (~40 lines)
- **Total root: ~600-800 lines / 6,000-8,000 tokens**

This exceeds the agentskills.io 500-line recommendation. The exception is documented: the run engine is the orchestration substrate that converge and gate delegate to, and extracting it creates an unanswered two-hop chain problem.

Per-invocation context drops from 31k tokens to:
- `/conversus define`: ~8k (root + handler-define)
- `/conversus run`: ~8k (root contains the engine)
- `/conversus gate`: ~11k (root + handler-gate)
- `/conversus converge`: ~10k (root + handler-converge)

## Phase 1: Must Implement

### 1.1 Extract gate handler

Move SKILL.md gate handler (~300 lines) to `references/handler-gate.md`. Replace in dispatch table with Class A load trigger. Includes gate-result.md schema, gates.yml config schema, exit codes, re-run behavior. This is the empirical validation test for reference-file loading.

### 1.2 Extract guided handlers

Extract each to its own reference file:
- `references/handler-define.md` (~150 lines)
- `references/handler-interests.md` (~200 lines)
- `references/handler-mode.md` (~180 lines)
- `references/handler-converge.md` (~210 lines, with explicit cross-reference to run engine)
- `references/handler-arbitrate.md` (~160 lines)

Output schemas co-located in each handler file (problem.md schema in handler-define, interests.md schema in handler-interests, etc.).

### 1.3 Staged execution

Execute decomposition in three phases with validation gates:
1. Extract gate handler + define handler. Validate correct reference-file loading and output fidelity.
2. If Phase 1 succeeds, extract remaining 4 guided handlers.
3. If Phase 2 succeeds, extract conditional subsystems (preset resolution).

Each phase gated on the previous phase's success. If any phase fails, stop and debug before proceeding.

### 1.4 Fix root AGENTS.md

Remove nonexistent `tasks/` from structure section. Add `schema/`, `linter/`, `presets/`, `antipatterns/`. Add linter as pre-contribution check. Note that subdirectories with their own AGENTS.md have directory-specific guidance. Keep under 70 lines. 15-minute task — proceed immediately.

### 1.5 Create `linter/AGENTS.md`

30-45 lines: Python version, `uv sync`, linter command (`uv run python linter/validate.py`), test command, what the linter checks, how to interpret failures. The canonical example of contribution guidance with zero dual-ownership risk.

### 1.6 Load trigger model

Dispatch table tells agents which handler to load. Handlers tell agents which subsystems to load. Document in root SKILL.md.

## Phase 2: Should Implement

### 2.1 Extract preset resolution

Move preset resolution algorithm (~75 lines) to `references/subsystem-preset-resolution.md`. Trigger: "If any agent entry has a `preset` field, read this file before validation."

### 2.2 AGENTS.md pointer convention

AGENTS.md files use "See [file] for authoritative rules" pointers, never inline rule restatement, for any content also enforced at runtime. One pointer line + one linter command line per rule.

### 2.3 Per-item Important Notes triage

Retain in root: overwrite semantics, model selection, rounds/iterations orthogonality, background dispatch, agent count formulas. Move to `references/notes-operational.md`: worked formula examples, baseline feature inventory, detailed orthogonality explanation. Do once, not an ongoing process.

### 2.4 Antipattern check placement

The antipattern check remains in root SKILL.md, executed pre-dispatch. All subcommands inherit it. AGENTS.md may also mention it as a contribution guideline.

### 2.5 Linter expansion (Phase 1 only)

Extend the linter to validate that template variables in handler reference files match `schema/variables.yml`. Further expansion (reference file header validation, AGENTS.md file reference checking) deferred until realistic.

## Phase 3: Consider Later

### 3.1 Per-invocation token budget

Document once at decomposition time as a measurement in this spec. Not a maintained table.

### 3.2 Nested AGENTS.md for templates/, presets/, schema/

15-30 line pointer files. Defer until someone outside Claude Code needs contribution guidance for these directories.

### 3.3 Gate as APM sub-skill

Defer until a second consumer with independent activation needs appears and reference structure has proven stable across two spec iterations.

### 3.4 Run engine extraction test

After Phase 2 succeeds, optionally test engine-in-reference-file vs engine-in-root. Only if token reduction is insufficient.

## Non-Extractable Core (Constitutional)

Per constitution v2.2.0, Principle XIX, these must remain in root SKILL.md:
- Subcommand dispatch table
- Non-negotiable multi-agent rules
- Phase-level execution flow (the full run engine, per arbiter ruling)
- Important Notes / operational gotchas

## Content Classification Rule (Constitutional)

Per constitution v2.2.0, Principle XVII:
- **Execution logic** → SKILL.md or `references/`
- **Contribution guidelines** → AGENTS.md
- Runtime-enforced rules MUST NOT be split across both formats

## Status

Deliberation: complete (37 agents, 1 round, 4 binding rulings)
Constitution: updated to v2.2.0 (5 new principles XVII-XXI)
Implementation: pending (staged execution plan defined above)
