# PR #1 Global Synthesis — 011-adoption-harness

**Branch**: `011-adoption-harness`
**Commits**: 90 (+47,472 lines, 277 files)
**Milestones**: M001-M005
**Reviewers**: 5 parallel agents
**Date**: 2026-03-23

## Aggregate Statistics

| Milestone | Files | Lines | Tests | FRs Scored | Pass | Partial | Fail |
|-----------|-------|-------|-------|------------|------|---------|------|
| M001 Foundation | ~40 | ~4,200 | 275 | 12 | 10 | 2 | 0 |
| M002 Engine | ~25 | ~8,500 | 281 | 7 | 4 | 3 | 0 |
| M003 Provider+CLI+SDK | ~20 | ~5,600 | 262 | 8 | 5 | 1 | 1 |
| M004 CLI Polish | ~13 | ~1,440 | ~100 | 7 | 5 | 2 | 0 |
| M005 Web Interface | ~96 | ~19,200 | ~400 | 8 | 7 | 1 | 0 |
| **Total** | **~194** | **~39,000** | **~1,318** | **42** | **31** | **9** | **1** |

## Global Issues by Priority

### P1 — Must Fix Before Merge

| # | Issue | Source | Impact | Fix Complexity |
|---|-------|--------|--------|----------------|
| G1 | **Linter↔engine dependency inversion** — engine imports context models, quality gates, and output parsing from linter | M001, M002 | Blocks clean packaging; confuses module ownership; will deepen with every new milestone | Medium — move models to engine/ or shared package |
| G2 | **OAuth state not validated locally** — Anthropic code-paste flow generates state but never compares returned state to local value | M004 | CSRF vector per OAuth 2.0 spec | Small — add `assert state_returned == state` |
| G3 | **BYOK key via os.environ mutation** — temporarily sets API key as process-level env var during request handling | M005 | Race condition in concurrent requests; key briefly visible in process environment | Medium — pass key directly to provider constructor |
| G4 | **CLI --phase advertises unsupported values** — click.Choice includes cross-review, revision, disputes, synthesis but only "all" and "review" work | M003 | RuntimeError for users selecting advertised options | Small — remove unsupported choices or implement them |
| G5 | **RLS / user_id mismatch** — Migration 002 requires auth.uid() = user_id but backend never populates user_id | M005 | Functional bug: backend inserts/reads fail with anon key when migration 002 applied | Medium — use service role key or populate user_id |

### P2 — Should Fix

| # | Issue | Source | Impact |
|---|-------|--------|--------|
| G6 | FR-020 per-phase model routing not implemented | M002, M003 | Spec requires interface "from day one"; single model used for all phases |
| G7 | FR-002 fallback diverges (11 launches vs spec-prescribed 4) | M001 | 2.75x cost premium on quality gate fallback |
| G8 | Missing plugin lifecycle hooks (spec 016 blocker) | M002 | No PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION hooks for plugin system |
| G9 | Stealth header version hardcoded (2.1.62) | M004 | Silent breakage when Claude Code updates |
| G10 | Empty Anthropic client_id breaks real OAuth | M003 | Production login flow will fail |
| G11 | No rate limiting on web /api/deliberate | M005 | Each request spawns full engine pipeline; no abuse protection |
| G12 | OutputManager.retroactive_move_to_round_1() mutates state | M002 | Stale path references after mutation |
| G13 | No StorageWriter abstraction (FR-011) | M002 | Direct filesystem writes throughout; blocks non-filesystem backends |
| G14 | ModelProvider is text-only (FR-019) | M002 | No tool_use, structured_output, or capability validation |
| G15 | Inconsistent --provider validation between CLI commands | M003 | run uses click.Choice, decide uses freeform string |
| G16 | No max_length on web question field | M005 | Token exhaustion / oversized payloads |
| G17 | FRONTEND_URL missing from DO app spec | M005 | Share URLs point to localhost in production |

### P3 — Nice to Have

| # | Issue | Source |
|---|-------|--------|
| G18 | JSONL file locking absent | M001 |
| G19 | Non-consumer presets too thin | M001 |
| G20 | conftest.py missing (dual-import pattern) | M001 |
| G21 | Module-level _preset_cache thread-unsafe | M002 |
| G22 | Agent lookup linear scan | M002 |
| G23 | ProviderError.category lost on string conversion | M003 |
| G24 | No timeout on httpx.post calls | M003 |
| G25 | _CallbackHandler.authorization_code class variable | M003 |
| G26 | No --verbose flag for CLI output | M004 |
| G27 | is_oauth_token in wrong module | M004 |
| G28 | CORS overly permissive | M005 |
| G29 | No unshare endpoint | M005 |
| G30 | SDK Deliberation.run() async-only | M003 |
| G31 | No per_agent_outputs in SDK Result | M003 |
| G32 | debate_transcript == full_analysis (no split) | M001 |

## Cross-Cutting Patterns

### Strong Patterns (Maintain)
1. **Pure function extraction** — every milestone extracts testable pure functions behind thin wrappers (MCP tools, CLI commands, SDK methods). This is excellent architecture.
2. **Frozen Pydantic models** — immutability enforced and tested throughout. Constitution Principle IX compliance.
3. **Test culture** — 1,318+ tests across all milestones; 3x spec requirements in M002; real fixtures over mocks.
4. **Protocol-based typing** — ModelProvider, EventEmitter, CancellationFlag all use @runtime_checkable Protocol, not ABCs.
5. **Event-driven architecture** — EventEmitter + CallbackEmitter + AsyncQueueEmitter bridges sync engine to async consumers cleanly.

### Weak Patterns (Fix Globally)
1. **Linter/engine coupling** — engine imports from linter in 3 places (models, quality, output_contract). Must resolve.
2. **Auth complexity** — auth.py is ~300+ lines handling 2 OAuth flows, PKCE, storage, refresh, and resolution. Should split.
3. **Missing extension points** — no plugin hooks, no per-phase model routing, no storage abstraction, no provider middleware.
4. **Environment variable patterns** — BYOK key via os.environ mutation, stealth header version hardcoded, EngineConfig.provider ignored at runtime.

## Vision Alignment Summary

### Ready for Game Engine (Specs 012-020)
- Config parser supports 4 modes; extensible for game forms (012)
- QualityIndicators emits structured data for feature extraction (015)
- PipelineResult + StructuredDeliberation are JSON-serializable for scenarios (020)
- Multi-round orchestration emits per-round data for convergence prediction (018)
- EngineConfig is Pydantic with validate() + estimate_cost() for optimizer (019)

### Needs Work for Game Engine
- **Plugin hooks (016)**: No lifecycle hooks in pipeline. EventEmitter is observe-only.
- **Feature extraction (015)**: debate_transcript == full_analysis; per-agent outputs not in SDK Result
- **Provider capabilities (019)**: ModelProvider is text-only; can't express tool_use or structured_output
- **Per-phase routing (014, 019)**: Single model for all phases; optimizer can't assign models per phase

### Ideas Alignment
- **Credibility scoring**: UsageEntry.agent_names + quality_passed enables tracking; QualityIndicators extensible
- **Telemetry**: JSONL usage logging + usage_events table + EventEmitter = multi-layer telemetry
- **Training data**: perceived_value feedback + stored Q&A in Supabase + StructuredDeliberation = preference dataset
- **Schema query tool**: Not yet needed (schema < 100 variables) but index format compatible

## Deliberation Questions for Synthesis

The following questions should drive the conversus deliberation across all 5 milestone reviews:

1. **Dependency structure**: Should linter models move to engine, to a shared package, or should the direction be reversed?
2. **Security bar**: Which P1 security issues (OAuth state, BYOK race, RLS) must be fixed before any milestone merges?
3. **Plugin readiness**: Should lifecycle hooks be added now (enabling spec 016) or deferred to a separate PR?
4. **Per-phase routing**: Is FR-020 a hard merge blocker or acceptable technical debt for v1?
5. **PR strategy**: One mega-PR with all fixes, or per-milestone PRs with cross-references?
