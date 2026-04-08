# Alignment Deliberation Synthesis: Engine vs Specs 006-013

**Synthesizer**: conversus alignment deliberation
**Date**: 2026-03-24
**Scope**: Engine implementation alignment with merged SKILL.md (specs 006-013)

---

## 1. Process Summary

| Metric | Count |
|--------|-------|
| Reviewing agents | 4 |
| Phase 1 reviews | 4 |
| Phase 2 cross-reviews | 12 |
| Phase 3 revisions | 4 |
| Phase 4 dispute files | 4 |
| Total recommendations (original) | 40 (10 per agent) |
| Recommendations surviving revision | 30 |
| Recommendations withdrawn | 5 (arb-R10, schema-R3 absorbed, schema-R4 deferred, spec-R08, guided-none) |
| Recommendations modified | 9 |
| New recommendations from cross-review | 8 (2 per agent) |
| Dangerous contradictions identified (Phase 2) | 12 unique (across 12 cross-reviews) |
| Remaining disputes (Phase 4) | 9 (across 4 agents, ~5 unique disputes) |
| Convergence points | 5 unanimous or near-unanimous |

---

## 2. Recommendation Scorecard

Legend: **S** = Surviving, **M** = Modified, **W** = Withdrawn, **N** = New (from cross-review)

### Guided Workflow Auditor

| ID | Recommendation | Original | Revised | Status | Notes |
|----|---------------|----------|---------|--------|-------|
| GW-R1 | `timing`/`influence` on `ArbiterConfig` | P1 | P1 | S | Unanimous |
| GW-R2 | Inter-round arbitration in `run_pipeline()` | P1 | P2 | M | Sequencing: depends on R1 |
| GW-R3 | Phase 6-only execution entry point | P1 | P2 | M | Enables delegation, not a correctness fix |
| GW-R4 | Public dispute-parsing API | P2 | P2 | S | |
| GW-R5 | `conversus_gate` MCP tool | P2 | P2 | S | |
| GW-R6 | `conversus_cost` MCP tool | P2 | P2 | S | |
| GW-R7 | `VALID_MODES` shared constants | P3 | P3 | S | Resisted P1 escalation |
| GW-R8 | `PRIOR_ARBITRATION_SECTION` population | P3 | P1 | M | Upgraded per arb-auditor argument |
| GW-R9 | Document dual-execution-path | P3 | P3 | S | |
| GW-R10 | Influence-aware heading validation | P3 | P3 | S | |
| GW-N1 | Verify `arbiter/`-vs-`arbitration/` ground truth | -- | P1-verify | N | |
| GW-N2 | Ship R1 + `extra="forbid"` atomically | -- | constraint | N | Sequencing constraint |

### Arbitration Auditor

| ID | Recommendation | Original | Revised | Status | Notes |
|----|---------------|----------|---------|--------|-------|
| AR-R1 | `timing`/`influence` on `ArbiterConfig` | P1 | P1 | S | Unanimous |
| AR-R2 | Inter-round arbitration in `run_pipeline()` | P1 | P2 | M | Sequencing concession |
| AR-R3 | `INFLUENCE_LEVEL` in `build_arbitration_context` | P1 | P1 | S | Unanimous |
| AR-R4 | `PRIOR_ARBITRATION_SECTION` in `build_review_context` | P1 | P1 | S | 3/4 agree P1 |
| AR-R5 | Influence-aware dispute counting | P2 | P2 | S | |
| AR-R6 | Cross-round synthesis arbitration context | P2 | P2 | S | Plumbing exists, wiring missing |
| AR-R7 | `PipelineResult.arbitration_ran` richer type | P2 | P2 | S | Dependency of R2 |
| AR-R8 | Integration test: inter-round + advisory | P3 | P3 | S | |
| AR-R9 | Influence-adjusted heading validation | P3 | P3 | S | |
| AR-R10 | Warning for unimplemented fields | P3 | -- | W | Superseded by R1 |
| AR-N1 | Verify `arbiter/`-vs-`arbitration/` ground truth | -- | P1-verify | N | |
| AR-N2 | Acknowledge dual-execution-path in arb recs | -- | note | N | Architectural acknowledgment |

### Schema Integration Auditor

| ID | Recommendation | Original | Revised | Status | Notes |
|----|---------------|----------|---------|--------|-------|
| SI-R1 | `timing`/`influence` on `ArbiterConfig` | P1 | P1 | S | Unanimous |
| SI-R2 | Canonical mode list (shared constants) | P1 | P3 | M | 3 cross-reviews challenged P1 |
| SI-R3 | `extra="forbid"` on `ArbiterConfig` | P1 | absorbed | W | Absorbed into sequencing constraint |
| SI-R4 | 011a SKILL.md decomposition | P2 | deferred | W | No alignment impact |
| SI-R5 | `game_form` on `EngineConfig` | P2 | P3 | M | Informational-only, defer to spec 014 |
| SI-R6 | Fix spec 013 import path | P2 | P2 | S | Documentation fix |
| SI-R7 | `conversus_validate_schema` MCP tool | P3 | P3 | S | |
| SI-R8 | Cross-package mode-set assertion test | P3 | P3 | S | |
| SI-R9 | Add schemas to AGENTS.md | P3 | P3 | S | |
| SI-R10 | Document zero-dependency contract | P3 | P3 | S | |
| SI-N1 | Correct STATUS.md for specs 012/013 | -- | P2 | N | |
| SI-N2 | Dual-execution-path schema implications | -- | note | N | Architectural constraint for spec 014 |

### Spec Compliance Auditor

| ID | Recommendation | Original | Revised | Status | Notes |
|----|---------------|----------|---------|--------|-------|
| SC-R01 | `timing`/`influence` on `ArbiterConfig` | P1 | P1 | S | Unanimous |
| SC-R02 | `INFLUENCE_LEVEL` in `build_arbitration_context` | P1 | P1 | S | Unanimous |
| SC-R03 | Rename `arbiter/` to `arbitration/` | P1 | P1-verify | M | Pending ground truth verification |
| SC-R04 | `PRIOR_ARBITRATION_SECTION` population | P1 | P1 | S | 3/4 agree |
| SC-R05 | `PRIOR_ROUND_SECTION` population | P1 | P2 | M | Pre-existing gap, not post-merge |
| SC-R06 | Inter-round arbitration in `run_pipeline()` | P2 | P2 | S | Unanimous P2 |
| SC-R07 | Influence-aware dispute counting | P2 | P2 | S | |
| SC-R08 | Warn on unknown config fields | P2 | -- | W | Superseded by direct R01 implementation |
| SC-R09 | Document guided workflow architecture | P3 | P3 | M | Expanded to cover dual-execution-path |
| SC-R10 | Template variable population test | P3 | P3 | S | |
| SC-N1 | Correct STATUS.md | -- | P2 | N | |
| SC-N2 | Verify `arbiter/`-vs-`arbitration/` ground truth | -- | P1-verify | N | |

---

## 3. Dangerous Contradictions Found

### Resolved

**DC-R1. Inter-round arbitration priority (P1 vs P2)**
- Arbitration-auditor: P1 ("blocks spec 006 correctness")
- Spec-compliance-auditor: P2 ("feature addition, not a fix")
- **Resolution**: P2 by unanimous consensus after revision. The sequencing argument prevailed: R1 (fields) must ship before R2 (behavior) has any effect. P2 reflects implementation dependency, not diminished importance.

**DC-R2. `PRIOR_ARBITRATION_SECTION` priority (P1 vs P3)**
- Arbitration-auditor: P1 (spec 006 FR-014 requires it)
- Guided-workflow-auditor: P3 (guided handlers compose their own context)
- **Resolution**: P1 by 3-of-4 consensus after revision. The guided-workflow-auditor upgraded to P1, accepting that engine context builders must be correct for convergence. The arbitration-auditor's argument that agents without prior-ruling awareness is dangerous was decisive.

**DC-R3. `VALID_MODES` unification priority (P1 vs P3)**
- Schema-integration-auditor: P1 ("critical consistency risk")
- Guided-workflow-auditor, arbitration-auditor, spec-compliance-auditor: P3 (theoretical, never occurred)
- **Resolution**: P3 by 4-of-4 consensus after revision. The schema-integration-auditor accepted the downgrade. Values are identical, drift has never occurred, and any test would catch it.

**DC-R4. Dual-execution-path impact on priority classification**
- Spec-compliance-auditor: engine gaps are "runtime failures" (5 P1 items)
- Guided-workflow-auditor: engine gaps only affect engine-direct callers (3 P1 items)
- **Resolution**: Partially resolved. Both auditors acknowledge the dual-execution-path architecture. The spec-compliance-auditor narrowed impact claims (withdrew `/conversus arbitrate` failure claim for R03). Priority classification converged: 4 items at P1, inter-round arbitration at P2.

### Unresolved

**DC-U1. `arbiter/` vs `arbitration/` directory naming**
- Spec-compliance-auditor: engine uses `arbiter/`, SKILL.md uses `arbitration/`, this is P1
- Arbitration-auditor: "output directory layout matches spec 006 US-4"
- **Status**: Both claims are about the codebase. They cannot both be correct. Three auditors (guided-workflow, arbitration, spec-compliance) created ground-truth verification recommendations. **Requires codebase inspection to resolve.**

**DC-U2. Schema package existence**
- Spec-compliance-auditor (original): "does not exist on disk yet"
- Schema-integration-auditor: package IS implemented with working tests
- **Status**: Resolved factually (schemas exist) but the root cause (stale STATUS.md) is a systemic concern. Two auditors recommend STATUS.md correction.

---

## 4. Systemic Contradictions

### S1. Engine-as-sole-path vs dual-execution-path

The most significant architectural finding of the deliberation. Three of four auditors (arbitration, schema-integration, spec-compliance) initially reviewed the engine as if it were the sole execution path. The guided-workflow-auditor revealed that SKILL.md handlers are a parallel implementation: `/conversus converge` orchestrates phases via Agent tool calls, not via `run_pipeline()`. This means:

- Engine improvements (better error handling, streaming, cost tracking) do not automatically benefit guided workflow execution
- Engine bugs only affect engine-direct callers (MCP tools, SDK), not guided workflow commands
- Full spec compliance requires changes in both the engine AND SKILL.md handlers, or a convergence path (delegation via MCP tools)

The dual-execution-path is by design (SKILL.md handlers run in-conversation, engine runs headless), but the lack of documentation means future contributors may not understand that changes to pipeline logic must be made in both places.

### S2. STATUS.md as source of truth vs filesystem reality

The spec-compliance-auditor trusted STATUS.md and reached an incorrect conclusion about schema package existence. STATUS.md is a manually maintained file with no automated verification. Any audit that relies on STATUS.md without filesystem validation risks similar errors.

### S3. Priority classification criteria diverge across auditors

Each auditor used different P1 criteria:
- Guided-workflow-auditor: "blocks correct guided workflow execution"
- Arbitration-auditor: "blocks spec 006 correctness"
- Schema-integration-auditor: "critical consistency risk"
- Spec-compliance-auditor: "runtime failure or silent incorrectness"

These criteria yield different P1 sets for the same findings. The deliberation process successfully resolved these through cross-review, but the initial divergence created 12 dangerous contradictions, most of which were priority disagreements rather than substantive disagreements.

---

## 5. Convergence Achieved

Ordered by strength (unanimous first, then by count):

1. **`timing`/`influence` fields on `ArbiterConfig`** — 4/4 auditors, P1, unchanged through all phases. The anchor recommendation.
2. **`INFLUENCE_LEVEL` must be explicitly passed from config** — 4/4 auditors, P1. Identical mechanism identified by all.
3. **Inter-round arbitration is P2** — 4/4 auditors after revision. Resolved from initial P1/P2 split via sequencing argument.
4. **Engine's core pipeline (pre-spec-006) is a faithful SKILL.md extraction** — 4/4 auditors. All confirm config parsing, template loading/filling, pipeline orchestration, dispute parsing, and output structure are correct for pre-spec-006 features.
5. **`PRIOR_ARBITRATION_SECTION` population is P1** — 3/4 auditors. The guided-workflow-auditor's upgrade from P3 to P1 was the most significant position change in the deliberation.
6. **`arbiter/` vs `arbitration/` requires ground truth verification** — 3/4 auditors. Emerged from cross-review, not identified in any original review as requiring verification.
7. **Engine-schema zero-import isolation is correct** — 4/4 auditors. No integration needed for current modes.
8. **`VALID_MODES` values are currently identical** — 4/4 auditors. Unification is P3, not P1.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

**RD-1. `arbiter/` vs `arbitration/` directory naming — P1 or non-issue?**
- Spec-compliance-auditor: P1 pending verification (track at P1 to prevent deprioritization)
- Guided-workflow-auditor: verify first, then classify (prevent wasted effort on potentially non-existent issue)
- Arbitration-auditor: verify first (their original review claimed paths match)
- **Synthesizer assessment**: Verify immediately. This is a factual question, not a judgment call. If confirmed, P1 for engine consumers. The rename is a straightforward `arbiter/` -> `arbitration/` in `engine/output.py`. If not confirmed, remove from all lists.
- **Recommended resolution**: Check `engine/output.py` for the directory constant. Compare against SKILL.md. Act on the result.

**RD-2. MCP delegation tools — how many at P2?**
- Guided-workflow-auditor: 3 MCP tools at P2 (dispute parsing, gate, cost)
- Spec-compliance-auditor: 1 MCP tool at P2 (dispute parsing), others P3
- Arbitration-auditor: no MCP tools recommended
- Schema-integration-auditor: defer to after delegation tools exist
- **Synthesizer assessment**: The guided-workflow-auditor's dual-execution-path finding makes the case for at least one delegation tool. Dispute parsing is the most broadly needed (used by converge, arbitrate, and gate handlers). One P2 tool establishes the pattern; additional tools can follow.
- **Recommended resolution**: 1 MCP tool (dispute parsing) at P2. `conversus_gate` and `conversus_cost` at P3. This balances the guided-workflow-auditor's architectural concern with the other auditors' focus on engine correctness first.

**RD-3. `PRIOR_ROUND_SECTION` — in scope or out of scope?**
- Spec-compliance-auditor: P2, in scope (detectable against current SKILL.md)
- Guided-workflow-auditor: out of scope (pre-existing gap, spec 004 era)
- **Synthesizer assessment**: Both positions are valid. The finding is real (the engine does not populate this variable), but it pre-dates the spec 006-013 merge.
- **Recommended resolution**: Include under "pre-existing gaps surfaced during alignment" in the actionable changes. This respects scope boundaries while not losing the finding.

**RD-4. R1 + R2 atomicity — ship together or separately?**
- Arbitration-auditor: ship atomically (parsed-but-inert field is a correctness trap)
- Spec-compliance-auditor: ship together or with committed timeline + warning
- Guided-workflow-auditor: flexible on separate PRs with tracking ticket
- **Synthesizer assessment**: The arbitration-auditor's concern about parsed-but-inert `timing: inter-round` is valid. The risk is real but mitigatable.
- **Recommended resolution**: Ship R1 with a code-level warning when `timing: inter-round` is parsed but not yet implemented. Ship R2 in the next PR with a committed timeline. This avoids blocking R1 on the larger R2 implementation while preventing the silent correctness trap.

**RD-5. Phase 6-only entry point — P2 or unaddressed?**
- Guided-workflow-auditor: P2 (key to resolving dual-execution-path for arbitration)
- Arbitration-auditor: acknowledged as complementary to R2
- Spec-compliance-auditor, schema-integration-auditor: not addressed
- **Synthesizer assessment**: This is the bridge between the engine and the guided `/conversus arbitrate` handler. Without it, the guided handler must remain a parallel implementation. It is the natural companion to R2.
- **Recommended resolution**: P2, grouped with the inter-round arbitration family. Implementation: `Deliberation.arbitrate(output_dir, arbiter_config)` or `run_engine(config_path, phase="arbitration")`.
<!-- CONVERSUS:DISPUTES_END -->

---

## 6. Actionable Spec Changes

### Tier 1 — Blocks Correctness (must-fix before any engine consumer can rely on spec 006)

| ID | Change | File(s) | Traceability | Priority |
|----|--------|---------|-------------|----------|
| T1-1 | Add `timing: Literal["final", "inter-round"] = "final"` and `influence: Literal["binding", "recommended", "advisory"] = "binding"` to `ArbiterConfig`. Parse in `_resolve_arbiter`. Add FR-003 validation: `timing: inter-round` requires `rounds > 1`. | `engine/config.py` | GW-R1, AR-R1, SI-R1, SC-R01 (4/4 unanimous P1) | P1 |
| T1-2 | Pass `INFLUENCE_LEVEL` from `config.arbiter.influence` (mapped to `InfluenceLevel` enum) in `build_arbitration_context()`. | `engine/templates.py` | AR-R3, SC-R02 (4/4 unanimous P1) | P1 |
| T1-3 | Populate `PRIOR_ARBITRATION_SECTION` in `build_review_context()` when `prior_arbitration_path` exists. Construct influence-aware text block per SKILL.md FR-014 using `config.arbiter.influence`. | `engine/templates.py` | AR-R4, SC-R04, GW-R8 (3/4 P1) | P1 |
| T1-4 | **Verify** `arbiter/` vs `arbitration/` directory name in `engine/output.py` against SKILL.md. If mismatch confirmed, rename to `arbitration/` in `OutputManager` methods, directory layout constants, and tests. | `engine/output.py` | SC-R03, GW-N1, AR-N1, SC-N2 (3/4 verification) | P1 (pending verification) |

### Tier 2 — Blocks Spec 006 Features (required for full spec 006 compliance)

| ID | Change | File(s) | Traceability | Priority |
|----|--------|---------|-------------|----------|
| T2-1 | Implement inter-round arbitration in `run_pipeline()`. After `_run_single_round` returns, if `config.arbiter.timing == "inter-round"`, evaluate trigger and dispatch Phase 6. Write to `round_base/arbitration/resolution.md`. Pass prior arbitration path to next round. Keep post-loop arbitration for `timing: final`. Ship with warning if R1 ships separately: `logger.warning("Inter-round arbitration not yet implemented")`. | `engine/phases.py` | AR-R2, GW-R2, SC-R06 (4/4 P2) | P2 |
| T2-2 | Implement influence-aware dispute counting for stagnation detection. After inter-round arbitration: `binding` subtracts addressed disputes, `recommended` subtracts provisionally, `advisory` does not adjust. Requires new helper to parse arbitration output for addressed dispute count. | `engine/phases.py` | AR-R5, SC-R07 (P2) | P2 |
| T2-3 | Add Phase 6-only execution entry point: `run_engine(config_path, phase="arbitration")` or `Deliberation.arbitrate(output_dir, arbiter_config)`. Loads existing synthesis, evaluates trigger, dispatches arbiter agent. Enables `/conversus arbitrate` to delegate to engine. | `engine/run.py`, `engine/sdk.py` | GW-R3, AR-N2 (P2) | P2 |
| T2-4 | Pass `arbitration_paths` and `arbitration_rulings` to `build_cross_round_synthesis_context()`. Collect per-round arbitration paths in the round loop. Function signature already supports these parameters. | `engine/phases.py` | AR-R6 (P2) | P2 |
| T2-5 | Expose `extract_remaining_disputes()` as public API (drop underscore prefix) and export from `engine/__init__.py`. Alternatively, expose via `conversus_disputes` MCP tool for SKILL.md handler consumption. | `engine/templates.py`, `mcp_server.py` | GW-R4 (P2) | P2 |

### Tier 3 — Future Readiness (improves architecture, prepares for specs 014+)

| ID | Change | File(s) | Traceability | Priority |
|----|--------|---------|-------------|----------|
| T3-1 | Create a canonical `VALID_MODES` source consumed by both `engine/config.py` and `conversus/schemas/objectives.py`. Options: shared module (`conversus/modes.py`), or consume existing `schema/game-forms/mode-mapping.yml`. **Trigger condition**: escalate to P2 when a new mode is added to either package. | `engine/config.py`, `conversus/schemas/objectives.py` | SI-R2, GW-R7 (P3) | P3 |
| T3-2 | Add `game_form` as optional auto-resolved field on `EngineConfig`. When present, validate against game form schemas. When absent, auto-resolve from mode via `load_mode_mapping()`. Informational-only in current engine. | `engine/config.py` | SI-R5 (P3) | P3 |
| T3-3 | Document dual-execution-path architecture. Explain that SKILL.md handlers and the Python engine are parallel implementations. Changes to pipeline logic must be made in both places or a convergence path (MCP delegation) must be chosen. | `engine/__init__.py` or new doc | GW-R9, SC-R09, AR-N2 (P3) | P3 |
| T3-4 | Change `PipelineResult.arbitration_ran` from `bool` to richer type (e.g., `arbitration_rounds: list[int]`). Keep backward compatibility via computed property. Dependency of T2-1. | `engine/phases.py` | AR-R7 (P2, deferred to after T2-1) | P3 |
| T3-5 | Add `conversus_gate` MCP tool for CI/CD integration. Accept gate config, generate temp config, run pipeline, parse disputes, return `{verdict, dispute_count, exit_code}`. | `mcp_server.py` | GW-R5 (P2 in original, P3 in synthesis) | P3 |
| T3-6 | Add `conversus_cost` MCP tool. Accept `agent_count, iterations, rounds, has_arbiter`, return cost estimate. Eliminates formula duplication between SKILL.md and `engine.cost.estimate_cost()`. | `mcp_server.py` | GW-R6 (P2 in original, P3 in synthesis) | P3 |

### Tier 4 — Spec Hygiene (documentation, tests, process)

| ID | Change | File(s) | Traceability | Priority |
|----|--------|---------|-------------|----------|
| T4-1 | Update STATUS.md to reflect actual implementation state of specs 012 and 013. Schemas package exists with working tests. | `specs/STATUS.md` | SI-N1, SC-N1 (P2) | P2 |
| T4-2 | Fix spec 013 FR-011 import path: change `from conversus_schemas.objectives` to `from conversus.schemas.objectives`. | `specs/done/013-*/spec.md` | SI-R6 (P2) | P2 |
| T4-3 | Populate `PRIOR_ROUND_SECTION` in `build_review_context()` for round 2+. Pre-existing gap (spec 004 era), not a post-merge regression. Individual path variables (`PRIOR_SYNTHESIS_PATH`, `PRIOR_ROUND_DIR`) partially mitigate. | `engine/templates.py` | SC-R05 (P2, pre-existing) | P2 (pre-existing) |
| T4-4 | Add integration test: `timing: inter-round` + `influence: advisory` scenario with mock provider. | `engine/tests/` | AR-R8 (P3) | P3 |
| T4-5 | Add cross-package mode-set assertion test: `set(engine_modes) == schema_modes`. | `tests/` | SI-R8 (P3) | P3 |
| T4-6 | Add influence-adjusted arbitration output heading validation (warning, not blocking). | `engine/phases.py` | AR-R9, GW-R10 (P3) | P3 |
| T4-7 | Add `PRIOR_ARBITRATION_SECTION` template variable population test. | `engine/tests/` | SC-R10 (P3) | P3 |
| T4-8 | Add `conversus/schemas` to project AGENTS.md structure section. | `AGENTS.md` | SI-R9 (P3) | P3 |
| T4-9 | Document zero-dependency contract in `conversus/schemas/__init__.py` docstring. | `conversus/schemas/__init__.py` | SI-R10 (P3) | P3 |
| T4-10 | Add `conversus_validate_schema` MCP tool for game form/objective YAML validation. | `mcp_server.py` | SI-R7 (P3) | P3 |

---

## 7. Key Concessions

1. **Schema-integration-auditor: `VALID_MODES` P1 -> P3.** The most significant priority downgrade. Three cross-reviews challenged the P1 rating with evidence that the values are identical and drift has never occurred. The auditor accepted the downgrade gracefully, adding a trigger condition ("escalate to P2 when a new mode is added") that preserves the intent.

2. **Guided-workflow-auditor: `PRIOR_ARBITRATION_SECTION` P3 -> P1.** The most significant priority upgrade. The arbitration-auditor's argument -- that engine context builders must be correct for convergence even if guided handlers currently bypass the engine -- was accepted. This was the single largest position change in the deliberation.

3. **Arbitration-auditor: inter-round arbitration P1 -> P2.** A sequencing concession, not a priority concession. The auditor accepts that the fields (R1) must exist before the behavior (R2) and that P2 reflects implementation order. The auditor explicitly notes this is not a signal that inter-round arbitration is less important.

4. **Spec-compliance-auditor: `PRIOR_ROUND_SECTION` P1 -> P2, `/conversus arbitrate` failure claim withdrawn.** Two concessions in one revision. The `PRIOR_ROUND_SECTION` downgrade accepts it is a pre-existing gap. The withdrawal of the claim that `/conversus arbitrate` would fail accepts the guided-workflow-auditor's finding that the handler does not read engine output.

5. **Spec-compliance-auditor: STATUS.md reliance acknowledged as methodology error.** Called it "the most embarrassing finding." Accepted the schema-integration-auditor's correction and created a STATUS.md update recommendation.

6. **Schema-integration-auditor: `extra="forbid"` absorbed into sequencing constraint.** The standalone recommendation was withdrawn because applying it before R1 would break existing configs. The intent (prevent silent field drops) is preserved by coupling it with R1 implementation.

7. **Schema-integration-auditor: 011a decomposition deferred entirely.** Accepted that SKILL.md decomposition has no alignment impact and does not belong in this review's priority list.
