# M001 Foundation Review

## Summary

M001 delivers a solid foundational layer: two binary quality gates implemented as pure functions with frozen Pydantic models, a heuristic question classifier, a canonical output contract (QualityIndicators replacing the confidence float), an MCP server with three tools, 7 consumer presets, JSONL-based usage logging, and 11 integration tests crossing all module boundaries. The code is cleanly structured with good separation of concerns, 275 total tests across 7 test files, and strong adherence to the project's functional service layer pattern. The main gaps are around FR-002 (the "mini-cross-review" fallback is implemented as iteration-doubling in the skill rather than the spec-prescribed 4-launch pipeline) and some premature coupling to later-milestone modules in the MCP server.

## Spec Compliance Scorecard

| FR | Status | Evidence | Notes |
|----|--------|----------|-------|
| FR-001 | PASS | `linter/quality.py:check_disagreement()` + `check_attributions()` | Two binary gates: (a) substantive disagreement via DISPUTES markers with 2+ agent positions, (b) attributions requiring 2+ agents, 1+ challenge, 1+ concession, 3+ phase refs. Both gates are structural -- no LLM judge. |
| FR-002 | PARTIAL | `.claude/commands/conversus-ask.md` Step 6 | Spec requires "mini-cross-review pipeline (4 launches)". Implementation instead doubles iterations (1 to 2), which produces ~11 launches, not 4. The fallback mechanism exists but diverges from the specified architecture. |
| FR-003 | PASS | `quality-floor/worked-example.md` + `quality-floor/single-model-responses/` | Side-by-side comparison for lease-vs-buy and monorepo-vs-polyrepo. |
| FR-004 | PASS | `.claude/commands/conversus-ask.md` Steps 5-6 | Quality gate blocks presentation -- if failed, skill either presents degraded output with warning or retries. |
| FR-007 | PASS | `linter/output_contract.py:ConversusOutput` | 5 machine-extractable fields: headline, summary, full_analysis, quality_indicators, debate_transcript. |
| FR-008 | PASS | `linter/output_contract.py:QualityIndicators` | 6 fields: agent_count, mode, phases_completed, cross_reviews_performed, genuine_disagreements_surfaced, genuine_disagreements_surviving. |
| FR-009 | PASS | `linter/question_classifier.py:classify_question()` | Two modes: interactive (returns clarification_question) and non-interactive (returns missing_fields list). |
| FR-012 | PASS | `.claude/commands/conversus-ask.md` | 204-line skill uses config-generation + existing SKILL.md execution + output formatting. |
| FR-013 | PASS | MCP server ships in M001; CLI ships later | Build order correct. |
| FR-014 | PASS | `mcp_server.py` has all three tools | conversus_decide includes quality gate check. |
| FR-015 | PASS | `mcp_server.py` Pydantic models | ValidateResult, RunResult, DecideResult, CostEstimate -- all have defined schemas. |
| FR-024 | PASS | `linter/usage.py:UsageEntry` + `AdoptionMetrics` | Tracks trust_rate, return_rate, sharing_status, disagreement/attribution pass rates. |

## Code Quality Assessment

### Strengths
- Pure functions throughout: check_disagreement(), check_attributions(), check_quality_floor(), classify_question(), parse_synthesis(), log_usage(), summarize_usage()
- Frozen Pydantic models with immutability tests
- Two-tier parsing strategy (marker-based primary, heading-based fallback)
- 275 tests across 7 files using real reference outputs as fixtures
- Privacy-conscious logging (truncated SHA-256 hash, never raw question text)
- Clean module boundaries with minimal, acyclic dependency graph

### Issues
- [P2] FR-002 fallback diverges from spec (11 launches vs 4) -- `.claude/commands/conversus-ask.md` Step 6
- [P2] MCP server imports engine modules not built in M001 -- `mcp_server.py:13-20`
- [P3] JSONL file locking absent -- `linter/usage.py:log_usage()`
- [P3] Regex complexity in quality.py (12 compiled patterns) -- `linter/quality.py:60-120`
- [P3] Non-consumer presets are thin (1-3 sentence prompts vs 10-line consumer presets)
- [P3] try/except ImportError pattern in tests -- all test files

## Vision Alignment

### Supports Future Specs
- Spec 012: QualityIndicators.mode + 4-mode dispatch table extensible for game forms
- Spec 015: QualityIndicators emits 6 structured numeric/categorical fields feature extraction can consume
- Spec 017: genuine_disagreements_surfaced/surviving are direct equilibrium scoring inputs
- Ideas (Credibility): UsageEntry.agent_names + quality_passed enables per-agent tracking
- Ideas (Telemetry): JSONL usage logging is already a telemetry pipeline

### Blocks or Conflicts
- No blocking conflicts. All models are frozen and additive.

### Missing Extension Points
- No plugin registration or PresetRegistry protocol
- Mode-specific quality gate thresholds are hardcoded
- No event emission (FR-010 deferred to M002)
- debate_transcript == full_analysis (no split yet)

## Recommendations

| # | Priority | Recommendation | Rationale | Affects |
|---|----------|---------------|-----------|---------|
| 1 | P2 | Implement 4-launch mini-cross-review or amend spec | FR-002 specifies 4 launches; current fallback costs 2.75x more | M001 + spec |
| 2 | P2 | Gate MCP server engine imports behind runtime checks | mcp_server.py imports 7 modules that don't exist in M001 scope | M001 |
| 3 | P3 | Add conftest.py to linter/ to eliminate dual-import pattern | Reduces test boilerplate across 7 files | M001 |
| 4 | P3 | Define QualityGateConfig for mode-aware thresholds | Hardcoded thresholds won't generalize to all 4 modes | M001 + M002 |
| 5 | P3 | Enrich non-consumer presets to match consumer depth | Thin prompts risk undifferentiated agent output | M001 |
| 6 | P3 | Add file locking to log_usage() before M002 | JSONL append without locking is acknowledged as M001-only | M002 |

## Cross-Milestone Observations
- MCP server as integration surface -- pure function extraction + thin @mcp.tool() wrappers is the right architecture
- Reference outputs as test fixtures -- small fixture set (2 passing, 1 failing) needs expansion per mode
- Pydantic model accumulation -- 12 models across 4 files; watch for sprawl
- Regex-based markdown parsing -- works but fragile; consider markdown AST parser in M002
