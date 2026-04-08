# M002 Engine Review

## Summary

M002 extracts the conversus engine from the SKILL.md prototype into a well-structured Python package (engine/) comprising 20+ modules across config parsing, template management, async dispatch, pipeline orchestration, output management, events, providers, SDK, CLI, auth, and error handling. The implementation delivers all 5 deliberation phases plus multi-round orchestration, arbitration, cross-round synthesis, and cancellation support. Test coverage is strong at 281+ test methods across 7 dedicated test files (4,678 lines). The architecture is clean, composable, and well-positioned for future specs.

## Spec Compliance Scorecard

| FR | Status | Evidence | Notes |
|----|--------|----------|-------|
| FR-005 | PASS | engine/config.py, templates.py, dispatch.py, templates._extract_remaining_disputes(), output.py | All 5 sub-phases independently importable and testable |
| FR-006 | PASS | Commit history shows SKILL.md prototype in M001, then extraction in M002 | Clean lineage |
| FR-010 | PASS | engine/events.py: PHASE_STARTED, AGENT_DISPATCHED, AGENT_COMPLETED, PHASE_COMPLETED | AsyncQueueEmitter enables SSE streaming |
| FR-011 | PARTIAL | OutputManager writes to filesystem directly; EventEmitter is transport-agnostic | File writing needs abstraction for non-filesystem backends |
| FR-019 | PARTIAL | ModelProvider protocol with complete()/stream(). No tool_use, structured_output, or capability validation. | Text-only signatures; sufficient for M002 but needs extension |
| FR-020 | PARTIAL | dispatch_phase() accepts single model parameter | Per-phase model routing not implemented; single model across all phases |
| FR-021 | PASS | asyncio.gather(return_exceptions=True), continue-with-N-1, ProviderError.category taxonomy | Proven by TestFailureIsolation |

## Architecture Assessment

### Design Decisions
- Frozen Pydantic models everywhere -- GOOD (Constitution Principle IX)
- Protocol-based ModelProvider (no base class) -- GOOD (structural subtyping)
- EventEmitter as protocol with multiple implementations -- GOOD (clean separation)
- Single _run_single_round() extraction -- GOOD (round vs deliberation level)
- Retroactive move for multi-round -- CONCERNING (mutates self.output_dir, stale path risk)
- Direct filesystem writes in pipeline -- CONCERNING (FR-011 compliance)

### Coupling Analysis
- engine/templates.py -> linter/models.py: INVERTED DEPENDENCY (engine should not depend on linter)
- engine/phases.py -> linter/quality.py: Engine coupled to linter quality gate logic
- engine/sdk.py -> linter/output_contract.py: Another engine-to-linter dependency
- No circular dependencies detected

### Extension Points
- EventEmitter protocol (new consumers just implement emit())
- ModelProvider protocol (new providers implement complete()/stream())
- CredentialStore (pluggable via constructor injection)
- CancellationFlag (cooperative cancellation)
- SDK Deliberation.on() (type-filtered event subscription)
- MISSING: No plugin lifecycle hooks, no per-phase model routing, no StorageWriter abstraction

## Code Quality Assessment

### Strengths
- Comprehensive docstrings with Args/Returns/Raises
- Robust config validation with actionable error messages
- 281+ test methods in 4,678 lines (3x spec requirement)
- Clean async with asyncio.gather(return_exceptions=True)
- Cost estimation centralized in engine/cost.py

### Issues
- [P2] engine/templates.py imports from linter.models -- inverted dependency
- [P2] engine/phases.py imports private _extract_remaining_disputes from templates
- [P2] OutputManager mutation in retroactive_move_to_round_1() -- footgun
- [P3] Module-level _preset_cache is thread-unsafe
- [P3] Agent lookup uses linear scan in _run_single_round()
- [P3] Anthropic client ID base64-encoded (security through obscurity)
- [P3] Stealth headers hardcoded in AnthropicProvider

## Vision Alignment

### Supports Future Specs
- Spec 012: Config parser supports 4 modes; game form definitions extensible
- Spec 015: Pipeline emits AgentCompleted events; StructuredDeliberation.from_events() reconstructable
- Spec 017: PipelineResult exposes active_agents, rounds_completed, termination_reason
- Spec 018: Multi-round orchestration emits per-round dispute counts
- Spec 019: EngineConfig is Pydantic with model_copy(update={}); validate() + estimate_cost() support dry-run
- Spec 020: PipelineResult + StructuredDeliberation are JSON-serializable

### Blocks or Conflicts
- Spec 016: No lifecycle hooks (PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION). EventEmitter is observe-only.
- FR-011: Direct filesystem writes need StorageWriter abstraction
- FR-019: ModelProvider.complete() is text-only; no tool_use or structured_output

### Missing Extension Points
- Plugin lifecycle hooks
- Per-phase model routing
- Abstract storage writer
- Provider capability negotiation
- Telemetry aggregation/export

## Recommendations

| # | Priority | Recommendation | Rationale | Affects |
|---|----------|---------------|-----------|---------|
| 1 | P1 | Move context models from linter/models.py to engine/ | Inverted dependency blocks clean packaging | global |
| 2 | P1 | Add per-phase model routing to EngineConfig | FR-020 requires this "from day one" | global |
| 3 | P2 | Introduce StorageWriter protocol for OutputManager | FR-011 non-filesystem storage | global |
| 4 | P2 | Extend ModelProvider with optional tool_use() + capabilities | FR-019 layer 2 | global |
| 5 | P2 | Add lifecycle hook mechanism to run_pipeline() | Spec 016 requires hooks | global |
| 6 | P2 | Replace retroactive_move mutation with immutable pattern | Mutating output_dir is a footgun | M002 |
| 7 | P3 | Make _extract_remaining_disputes() public | Private function imported across modules | M002 |
| 8 | P3 | Build agent name-to-config dict once | Linear scan repeated in inner loops | M002 |
| 9 | P3 | Remove stealth headers or make configurable | Brittle coupling to undocumented API surface | M002 |

## Cross-Milestone Observations
- Linter dependency inversion is the top technical debt
- M002 exceeds stated scope (SDK, CLI, auth, cost estimation included beyond S01-S03)
- Multi-round architecture is production-ready
- Test count 3x spec requirement
