# Synthesis: Spec 061 — Engine Eval Suite

**Phase**: 5 — Final Synthesis
**Date**: 2026-04-16
**Agents**: test-architect, engine-implementor, consumer-advocate
**Synthesized by**: Neutral synthesis agent

---

## 1. Overall Assessment

The three-agent deliberation produced substantial convergence. The spec's two-layer eval architecture (promptfoo for structural/functional, deepeval for LLM-as-judge quality) is unanimously endorsed as sound. The Known Gaps table (section 5), the test marker taxonomy (smoke/eval/live/integration), and the CI cadence mapping are strengths all three agents affirm. The spec correctly identifies the core problem -- a multi-surface, multi-provider engine with zero cross-cutting validation -- and proposes a credible framework to solve it.

The deliberation surfaced 6 remaining disputes, approximately 25 convergence points, and a prioritized action list of 35+ items. The spec requires meaningful revision before implementation, but the foundation is strong.

---

## 2. Convergence Points

The following items have full or near-full agreement across all three agents after revision. These should be treated as settled recommendations.

### 2.1 Unanimous Must-Fix Items

| Item | Description | Source |
|---|---|---|
| **quality_indicators schema** | Section 3.1.6 shows `quality_indicators` as a string array; the actual `QualityIndicators` Pydantic model is a nested object with integer fields (`agent_count`, `mode`, `phases_completed`, etc.). This factual error blocks the correctness of the output schema test. | Engine-implementor R2, endorsed by all |
| **First eval run scoping** | Step 3 must exclude red-blue mode (which will crash on ConfigError) and scope to cooperative, winner-take-all, and prisoners-dilemma with mock only. Add a pytest `xfail` test for adhoc red-blue `parse_config` to track G1. | Engine-implementor R6/S-3, test-architect xfail resolution, consumer-advocate P0 item 4 |
| **Settings cascade isolation** | A `clean_settings` conftest fixture that isolates HOME and project-level settings is a prerequisite for test reliability. `run_decide_mcp` treats `provider="mock"` as "not explicitly set," meaning the cascade can override it. | Engine-implementor R9 (upgraded to must-fix), test-architect P0, consumer-advocate P0 |
| **Promptfoo shell quoting** | Replace inline `{{prompt}}` shell expansion with a wrapper script, plus add a test case with shell metacharacters in the question. | Engine-implementor R3, consumer-advocate section 6.1, test-architect endorses |
| **Intermediate artifact access** | Specify `run_pipeline` (not `run_decide_mcp`) as the execution function for phase-level quality tests. Show the access pattern: `result.output_dir / "phase1" / "agent-0.md"`. | Engine-implementor R8, consumer-advocate section 3.12 |
| **Multi-round pipeline tests** | Rounds > 1 exercises the highest-complexity code paths (stagnation detection, cross-round synthesis, inter-round arbitration). At minimum: rounds=2 convergence, rounds=3 stagnation, asserting on `termination_reason`. Priority: P0. | Test-architect section 2.2, engine-implementor R15, consumer-advocate revision 3.2 |
| **SKILL.md parity** | Move from implementation step 9 to step 4-5. Parse SKILL.md examples, run each via CLI, verify each advertised provider resolves. | Consumer-advocate section 6.4, test-architect accepts, engine-implementor endorses |
| **G11: Dual provider resolution path** | `handlers.py` calls `resolve_provider` (auth.py) while CLI uses `resolve_execution_provider` (run.py). Both `run_decide_mcp` (~line 197) and `_run_in_process` (~line 491) are affected. Single fix: replace all `resolve_provider` calls in handlers.py. P1. | Engine-implementor original finding, consolidated in S-1, all three agree |
| **G3 description correction** | The 9 unwired providers ARE wired as ExecutionProviders in the registry; they are NOT wired through auth.py's `resolve_provider`. The fix target is `handlers.py`, not `auth.py`. | Engine-implementor R5/R7, consumer-advocate section 3.6, test-architect accepts |
| **Implementation step 5 target** | Clarify that wiring remaining providers means changing `handlers.py` to use `resolve_execution_provider`, not adding providers to `OAUTH_CONFIGS` in auth.py. | Engine-implementor R7, all agree |
| **SDK surface at P1** | Add SDK (`engine.sdk.Deliberation`) to cross-surface parity tests. Assert inner content parity (headline, summary, full_analysis, quality_indicators), not wrapper type identity. Originally disputed (consumer-advocate: P0, test-architect: P2), now converged at P1. | All three converge in revisions |
| **CI/CD governance exit codes** | Test the governance exit code scheme (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE). No reviewer had previously addressed this. P1. | Consumer-advocate section 3.3, test-architect accepts, engine-implementor R17 |
| **Extended modes: concrete tests** | Replace "(if supported in decide)" with concrete test cases for all 4 extended modes: each must produce either a valid output or a clear, documented error. | Engine-implementor R18, consumer-advocate section 1.2, test-architect dispute 6 |
| **Pydantic schema snapshot tests** | Dump each result model's JSON schema; fail on unexpected changes. Combined with cross-surface schema mapping against `ConversusOutput` as canonical model. P1. | Test-architect section 5.2, consumer-advocate endorses |
| **Promptfoo output assertions** | Strengthen from `is-json` + `headline !== undefined` to validate all 5 required output fields. Trivial fix with no reason to defer. | Test-architect section 4.2, consumer-advocate endorses |
| **Quality threshold calibration** | Run the quality suite once with anthropic provider, use resulting scores as baseline, set thresholds at baseline minus 0.1 regression margin. Do not guess thresholds a priori. | Consumer-advocate section 6.3, test-architect adopts, engine-implementor agrees |
| **JSON error output consistency** | `--format json` must produce parseable JSON on error paths, not plain text. Stdout must contain only JSON; stderr only log-level messages. | Consumer-advocate section 3.3 item 4, test-architect endorses |
| **VALID_PROVIDERS config bug** | `config.py` line 82 hardcodes `VALID_PROVIDERS = ("anthropic", "openai")`, rejecting all other providers in YAML configs while CLI `--provider` bypasses validation. Nominate as new known gap. P1. | Test-architect section 6.1, engine-implementor endorses, consumer-advocate endorses |
| **`conversus status` verification** | Section 3.1.3 lists `conversus status` as a test target. Confirm this command exists and specify its output contract, or remove it. | Engine-implementor M-5/R-CLI, consumer-advocate dispute 3, test-architect agrees in principle |
| **Conftest fixture reuse** | The eval suite should integrate with existing `engine/tests/conftest.py` shared fixtures rather than creating parallel infrastructure. | Engine-implementor, test-architect accepts |

### 2.2 Agreed Priority Assignments

| Priority | Items with full agreement |
|---|---|
| **P0** | Multi-round pipeline tests, settings cascade isolation, quality_indicators schema fix, first eval run scoping (exclude red-blue + xfail), red-blue adhoc end-to-end parse_config test, provider test levels taxonomy |
| **P1** | SDK cross-surface parity, SKILL.md parity (moved to step 4-5), CI/CD governance exit codes, arbiter smoke tests (trigger=always, trigger=disputes_remain with no disputes), iteration loop tests, Pydantic schema snapshots, VALID_PROVIDERS gap, G11 dual resolution path, extended modes concrete tests, JSON error output consistency, settings cascade provider key testing |
| **P2** | Arbiter functional tests (real disputes, binding vs advisory), deepeval judge model note, combinatorial smoke matrix (6 targeted combinations), Claude Code session detection, no-TTY login error, env var type coercion edge cases, cost telemetry test |
| **P3** | Cancellation tests, `--format rich` exit-code-zero only |

### 2.3 Agreed Withdrawals

The following items were proposed then withdrawn by their original advocates, with agreement from cross-reviewers:

- **Cowork HTTP transport and claude.ai web skills testing** (consumer-advocate: out of scope for engine eval)
- **.mcpb bundle build test** (consumer-advocate: belongs in Desktop Extension CI)
- **Non-darwin platform compatibility test** (consumer-advocate: platform restriction is packaging, not engine)
- **Paid tier HTTP surface placeholder test section** (consumer-advocate: premature; a TODO comment suffices)
- **R4 CLI flag name verification as must-fix** (engine-implementor: pre-implementation checklist, not spec revision)
- **R10 prescriptive LLM judge model** (engine-implementor: replaced with lighter note that quality tier requires LLM judge credentials)
- **`--format rich` structural testing beyond exit-code-zero** (test-architect: disproportionate CI effort)
- **Persistence internals** (disabled-via-settings, old-deliberation-cleanup) (test-architect: unit-test scope, not eval-suite)

---

## 3. Dispute Resolutions and Recommendations

### Dispute 1: Mock Provider Strategy — Realistic Response Mode vs. Fixture Test

**Positions**:
- *Test-architect (revised)*: Withdrew mock provider rewrite. Recommends a targeted `parse_synthesis()` fixture test with known-good markdown. The mock provider stays cheap and deterministic. The smoke tier tests pipeline completion; the fixture test catches parser regressions separately.
- *Engine-implementor (R14)*: Mock provider must return synthesis-parseable output. Without this, every smoke test exercises the bare-except fallback in `from_events()`, making the smoke tier structurally misleading. P0.
- *Consumer-advocate (revised)*: Agrees with engine-implementor. Lists mock provider fix as P0 item 1. However, the consumer-advocate originally proposed the fixture test alternative that the test-architect adopted, creating an internal inconsistency in the consumer-advocate's revision.

**Analysis**: This is the most consequential remaining dispute. The test-architect's concern about maintenance coupling (mock output must track synthesis format changes, recreating SKILL.md-like divergence) is legitimate. The engine-implementor's concern that the smoke tier exercises only the fallback path is equally legitimate.

**Recommendation: Do both.** The positions are not mutually exclusive, and the engine-implementor explicitly states this as an acceptable resolution. Specifically:

1. Add the `parse_synthesis()` fixture test (test-architect's proposal). This is a low-cost unit test that directly regresses the parser.
2. Enhance the mock provider to return output with correct markdown heading structure (`## Headline`, `## Summary`, etc.) for at least the 4 primary modes. This is a template refinement, not a subsystem rewrite -- the mock provider already returns mode-specific canned responses. Making those responses parseable by `parse_synthesis` closes the gap where the smoke tier exercises only the fallback path.
3. The maintenance coupling concern is mitigated by the fixture test: if the synthesis format changes and the mock is not updated, the fixture test catches the format change, and the smoke test will start hitting the fallback path again (detectable by asserting that `quality_indicators` fields are populated, not empty/zero).

Priority: P0 for the mock enhancement (at least one mode with parseable output); the fixture test can land alongside it.

---

### Dispute 2: Red-Blue Smoke Test Path — Adhoc vs. Pre-Built YAML

**Positions**:
- *Engine-implementor (R1, unchanged)*: Red-blue tests must use pre-built YAML configs. Rationale: decouples "does red-blue mode work?" from "does the adhoc config generator support red-blue?" and provides coverage before G1 is fixed.
- *Test-architect (revised)*: The adhoc path is the path real users take. If the smoke test uses pre-built YAML, the G1 regression path is untested. After G1 is fixed, the adhoc-path test should be the primary smoke gate.
- *Consumer-advocate*: Sides with test-architect. The consumer-relevant path is `conversus decide --mode red-blue`, not hand-authored YAML.

**Analysis**: The engine-implementor's concern about having zero red-blue coverage before G1 is fixed is valid. The test-architect's concern about the G1 regression path being permanently untested if pre-built YAML is the only test is also valid.

**Recommendation: Both tests, with the adhoc path as primary after G1 is fixed.** Specifically:

1. **Before G1 fix**: A pre-built YAML red-blue test verifies the engine handles red-blue mode correctly (engine-implementor's concern). A pytest `xfail` test calls `build_adhoc_config` for red-blue and documents the expected ConfigError (all three agree on xfail).
2. **After G1 fix**: The adhoc-path test becomes the primary red-blue smoke test because it exercises the path consumers actually use. The pre-built YAML test remains as a supplementary engine-level validation.
3. The engine-implementor's R1 should be modified from "use pre-built YAML instead of adhoc" to "use pre-built YAML in addition to adhoc, with adhoc as primary after G1."

This resolves the tension the test-architect identified between R1 and the G1 regression position.

---

### Dispute 3: Settings Cascade Testing Priority — P0 vs. P1

**Positions**:
- *Consumer-advocate (revised)*: Full cascade testing (all 5 levels, including env vars) at P0.
- *Test-architect (revised)*: Cascade *isolation* (fixtures) at P0; cascade *testing* (verify provider wins at each level) at P1.
- *Engine-implementor*: R9 upgraded isolation to must-fix; silent on cascade testing priority.

**Analysis**: The test-architect's distinction between isolation (infrastructure) and testing (coverage) is the correct framing. The eval suite can produce meaningful results with hardcoded mock provider even if the cascade is not yet fully tested. The consumer-advocate's argument about Desktop Extension users depending on the env var layer is about correctness, not about whether the eval suite can run.

**Recommendation: Adopt the test-architect's split.** Settings cascade isolation is P0 infrastructure. Settings cascade testing (provider key at each of 5 levels) is P1, implemented alongside SKILL.md parity and SDK testing. The env var layer must be included in the P1 cascade tests (consumer-advocate's 5-step test is the right test design).

---

### Dispute 4: Persistence Round-Trip Test Priority — P1 vs. P3

**Positions**:
- *Consumer-advocate*: P1 -- `persist_deliberation()` and `list_deliberations()` are shipping engine code called by handlers today. The paid tier depends on this layer.
- *Test-architect*: P3 -- persistence write/read is internal; the eval suite validates externally observable behavior.
- *Engine-implementor*: Silent on priority; uses persistence as an intermediate artifact access mechanism (R8).

**Analysis**: The consumer-advocate correctly distinguishes persistence internals (which all three agree are out of eval scope) from the round-trip integration test (`persist -> list -> show`). If `conversus list` and `conversus show` are consumer-facing CLI commands, testing them is testing externally observable behavior. However, the test-architect is right that P1 would place this ahead of arbiter tests, iteration loop tests, and schema snapshots, all of which test more critical pipeline behavior.

**Recommendation: P2.** The persistence round-trip is externally observable (the consumer-advocate is right that it is not purely internal), but it is lower risk than pipeline correctness tests. P2 places it after the P1 pipeline and schema tests but before the P3 edge cases. The test-architect's P3 underweights the consumer-facing nature of `list/show`; the consumer-advocate's P1 overweights it relative to pipeline correctness.

---

### Dispute 5: Desktop Extension Content Scanner Testing — In Scope vs. Out of Scope

**Positions**:
- *Consumer-advocate (revised, strengthened)*: P1. The prompts are engine code. The role-split workaround is in `mcp_server.py`. If the engine changes a prompt's structure and breaks the pattern, the failure surfaces in the primary consumer environment.
- *Engine-implementor (M-7)*: Out of engine eval scope. The content scanner is a Claude Desktop platform constraint that varies by Desktop version and Anthropic's content policy updates.
- *Test-architect*: Endorsed the finding in cross-review but did not prioritize it in the revised table.

**Analysis**: Both positions have merit. The engine-implementor's principled argument about scope is sound: testing against an external, undocumented, mutable constraint makes the eval suite fragile. The consumer-advocate's pragmatic argument is also sound: the prompts are engine code, and the engine controls whether they trigger the scanner.

**Recommendation: Include a lightweight static lint, not a runtime test. Scope it to P2.** Specifically:

1. Add a static check that the 7 MCP prompts in `mcp_server.py` maintain the role-split pattern (assistant + user turn structure) where instructional content appears. This is a pattern match on engine code, not a test against an external scanner.
2. This satisfies the consumer-advocate's concern (prompt format regressions are caught) without the engine-implementor's fragility concern (no dependency on external scanner rules).
3. P2, not P1, because the role-split pattern has not changed since it was introduced and the risk is lower than pipeline correctness concerns.

---

### Dispute 6 (Residual): Extended Modes — Empirical Verification Needed

**Status**: Not a dispute between agents. All three agree the 4 extended modes need concrete tests. The test-architect flags that no reviewer has verified whether these modes actually work through the adhoc path. The engine-implementor says "these likely work structurally but I have not verified their template variables are populated."

**Recommendation**: Before writing R18's test cases, the spec author must run each extended mode once with mock provider through the adhoc decide path and record whether it produces output or errors. The test expectations depend on this empirical fact. Add this as a pre-implementation step.

---

### Dispute 7 (Closed): `conversus status` in Section 3.1.3

The engine-implementor and consumer-advocate agree this is a spec correctness issue: the command either exists (specify its output contract) or it does not (remove from the test list). The test-architect did not include it in their revised priority table but did not dispute the point.

**Recommendation**: The spec author must confirm whether `conversus status` exists. If yes, specify the output contract. If no, remove from section 3.1.3. This is a must-fix spec correction.

---

## 4. Prioritized Action List for Spec Update

### P0 — Must fix before implementation begins

| # | Action | Spec Section | Source |
|---|--------|-------------|--------|
| 1 | Fix `quality_indicators` schema in section 3.1.6 to match actual `QualityIndicators` Pydantic model (nested object with `agent_count`, `mode`, `phases_completed`, etc., not a string array) | 3.1.6 | Engine-implementor R2 |
| 2 | Add multi-round pipeline tests: rounds=2 convergence, rounds=3 stagnation, rounds=5 max_rounds. Assert on `termination_reason` field. | New in 3.1 | Test-architect 2.2, engine-implementor R15 |
| 3 | Enhance mock provider to return synthesis-parseable markdown for primary modes AND add a `parse_synthesis()` fixture test with known-good markdown | New in 3.1 + unit tests | Dispute 1 resolution (engine-implementor R14 + test-architect fixture) |
| 4 | Add settings cascade isolation to shared test fixtures: clean HOME, no project settings, `CONVERSUS_*` env vars cleared | 3.1.4, 3.3.1 | Engine-implementor R9, test-architect P0 |
| 5 | Scope implementation step 3 to exclude red-blue; add pytest `xfail` for adhoc red-blue `parse_config` | 7, Step 3 | Engine-implementor R6/S-3, test-architect xfail |
| 6 | Define 5-level provider test taxonomy (import / instantiate / auth-resolve / dispatch / error-message-quality) and test each provider at the appropriate level, covering both `auth.py` and `run.py` resolution paths | 3.1.2 | Test-architect 4.4, engine-implementor R5 |
| 7 | Answer the desktop extension canonicality question: which engine copy is canonical? Does the eval suite test one or both? | 2.1 or new section | Test-architect 2.5, consumer-advocate framing |
| 8 | Confirm `conversus status` exists and specify output contract, or remove from section 3.1.3 | 3.1.3 | Engine-implementor R-CLI, consumer-advocate dispute 3 |
| 9 | Replace promptfoo inline shell expansion with a wrapper script; add test with shell metacharacters | 4.1 | Engine-implementor R3, consumer-advocate 6.1 |
| 10 | Specify `run_pipeline` as execution function for phase-level quality tests; show intermediate file access pattern | 3.2.1, 4.2 | Engine-implementor R8 |
| 11 | Red-blue smoke test: pre-built YAML test (immediate coverage) + adhoc-path test as primary after G1 fix | 3.1.1, 4.1 | Dispute 2 resolution |

### P1 — Must fix before the paid tier

| # | Action | Spec Section | Source |
|---|--------|-------------|--------|
| 12 | Add SDK surface (`engine.sdk.Deliberation`) to cross-surface parity tests (3.3.3). Assert inner content parity. | 3.3.3 | All three converge |
| 13 | Move SKILL.md parity test to step 4-5; parse examples, verify each advertised provider resolves | 7 | Consumer-advocate 6.4, both endorse |
| 14 | Add CI/CD governance exit code tests: 0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE | 3.3.2 | Consumer-advocate 3.3, engine-implementor R17 |
| 15 | Add arbiter smoke tests: trigger=disputes_remain with no disputes (should not fire), trigger=always (should fire) | New in 3.1 | Test-architect 2.3, engine-implementor R16 |
| 16 | Add iteration loop tests: iterations=3 produces 3 cross-review/revision rounds, cost estimate reflects 3x dispatches | New in 3.1 | Test-architect 2.4 |
| 17 | Add Pydantic schema snapshot tests for all result types + cross-surface schema mapping against `ConversusOutput` | New section | Test-architect 5.2, consumer-advocate endorses |
| 18 | Strengthen promptfoo assertions to validate all 5 required output fields (not just `headline`) | 4.1 | Test-architect 4.2 |
| 19 | Nominate VALID_PROVIDERS (`config.py` line 82) as new known gap; add `parse_config` test per registered provider | 5 | Test-architect 6.1 |
| 20 | Add G11 to Known Gaps: dual provider resolution path, both call sites in handlers.py, fix target is handlers.py | 5 | Engine-implementor S-1, all agree |
| 21 | Correct G3 description to distinguish auth.py from execution provider resolution; fix target is handlers.py not auth.py | 5 | Engine-implementor R5 |
| 22 | Clarify implementation step 5 target: handlers.py resolution path, not auth.py registration | 7, Step 5 | Engine-implementor R7 |
| 23 | Test all 4 extended modes with concrete pass-or-clear-error assertions (replace "if supported in decide") | 3.1.1 | Engine-implementor R18, consumer-advocate |
| 24 | Add settings cascade provider key tests at each of 5 levels (CLI flag, env var, project settings, global settings, defaults) including env var type coercion edge cases | 3.3.1 | Consumer-advocate 2.3, test-architect P1 |
| 25 | JSON error output: `--format json` produces parseable JSON on all error paths; stdout is JSON-only, stderr is log-only | 3.1.7 | Consumer-advocate 3.3 |
| 26 | Add per-agent provider override tests (heterogeneous deliberation, N-1 failure semantics) | New in 3.1 | Test-architect 2.1 |
| 27 | Integrate eval suite with existing `engine/tests/conftest.py` fixtures | 4 | Engine-implementor |
| 28 | Calibrate deepeval thresholds after first baseline run using baseline-minus-0.1 methodology | 3.2.1 | Consumer-advocate 6.3, test-architect adopts |
| 29 | Add PAID_TIER_REQUIRED structured error test (existing engine behavior when paid tools called without solver package) | New in 3.1 | Consumer-advocate 4.1 |
| 30 | Add persistence round-trip test: persist, list, show | New in 3.3 | Consumer-advocate 4.1 (recommended P2 per dispute 4 resolution, but grouped here for continuity) |

### P2 — Before declaring the suite complete

| # | Action | Spec Section | Source |
|---|--------|-------------|--------|
| 31 | Add arbiter functional tests: real disputes, binding vs advisory, inter-round timing | New in 3.1 | Test-architect 2.3 |
| 32 | Desktop extension schema parity test (after canonicality question resolved) | New section | Test-architect 2.5 |
| 33 | Persistence round-trip integration test (persist -> list -> show) | New in 3.3 | Dispute 4 resolution |
| 34 | Add combinatorial smoke matrix: 6 cross-axis combinations covering common consumer configs | 3.3 | Consumer-advocate 4.2 |
| 35 | Lightweight static lint for MCP prompt role-split pattern (content scanner mitigation) | New | Dispute 5 resolution |
| 36 | Add Claude Code session detection test (`CLAUDECODE=1`) | 3.3.2 | Consumer-advocate 3.2 |
| 37 | Add no-TTY login error test for headless CI | 3.3.2 | Consumer-advocate 3.3 |
| 38 | Note in section 4.2 that quality tier requires LLM judge credentials; judge model selected during calibration | 4.2 | Engine-implementor W-2 |
| 39 | Add MCP tool count assertion (prevent accidental tool proliferation) | New | Consumer-advocate 5.1 (re-adopted at P2) |
| 40 | Sensitive field handling: API keys must not appear in logs or error output | New | Consumer-advocate 3.1 |
| 41 | Add CI runner requirements: Python 3.12, Node 18, API key secrets provisioning | New section | Engine-implementor R12 |
| 42 | Verify extended modes empirically before writing test expectations | Pre-implementation | Test-architect dispute 6 residual |

### P3 — Edge cases and low-priority items

| # | Action | Spec Section | Source |
|---|--------|-------------|--------|
| 43 | Cancellation tests (mid-pipeline, partial output) | New | Test-architect 2.7, all agree P3 |
| 44 | `--format rich` exit-code-zero test | 3.1.3 | Test-architect, demoted |

---

## 5. Revised Implementation Order

Based on the convergence and dispute resolutions above, the spec's implementation order (section 7) should be revised as follows:

1. **Install promptfoo + deepeval; create `evals/` directory** (unchanged)
2. **Write promptfoo config** -- smoke tests for cooperative, winner-take-all, prisoners-dilemma with mock. Red-blue excluded. Strengthen assertions to validate all 5 output fields. Use wrapper script for shell quoting. (modified per R3, R6, action 9, 18)
3. **Run first eval** -- capture current pass/fail state. Red-blue excluded with documented xfail. (modified per R6/S-3)
4. **Fix G1** (red-blue presets) **and G2** (target paths). **Enhance mock provider** with synthesis-parseable output for primary modes. Add `parse_synthesis` fixture test. Re-run evals. (expanded per dispute 1 resolution)
5. **SKILL.md parity test** -- parse examples, verify provider list, run each via CLI. (moved from step 9 per all three agents)
6. **Wire remaining providers** -- fix `handlers.py` to use `resolve_execution_provider` (not auth.py). Add VALID_PROVIDERS fix or gap documentation. (clarified per R5/R7)
7. **Write deepeval quality tests** -- use `run_pipeline` for intermediate artifact access. Calibrate thresholds from first baseline. (modified per R8, calibration methodology)
8. **Save baseline snapshots** (unchanged)
9. **Settings cascade tests** -- provider key at all 5 levels, env var type coercion. (moved earlier from implicit later position)
10. **Add eval commands to CI workflow** -- specify runner requirements (Python 3.12, Node 18, secrets). (expanded per R12)
11. **Build engine-first skill** wrapping CLI (replaces agent-dispatch SKILL.md) (unchanged)
12. **Cross-surface parity tests** -- CLI vs MCP vs SDK output comparison. (expanded to include SDK)
13. **Multi-round, arbiter, and iteration tests** (new)
14. **Governance exit codes, persistence round-trip, combinatorial matrix** (new)

---

## 6. New Known Gaps to Add to Section 5

| # | Gap | Severity | Surface | Source |
|---|-----|----------|---------|--------|
| G11 | Dual provider resolution path: `resolve_provider` (auth.py) vs `resolve_execution_provider` (run.py). Both `run_decide_mcp` and `_run_in_process` in handlers.py use the narrower auth.py path. Fix: replace with `resolve_execution_provider`. | P1 | MCP | Engine-implementor, all agree |
| G12 | `VALID_PROVIDERS` in config.py hardcoded to `("anthropic", "openai")`. YAML configs with any other provider rejected at parse time. CLI `--provider` bypasses this. | P1 | CLI (run), MCP (run) | Test-architect 6.1 |

---

## 7. Architecture Diagram Update

Add `engine/run.py` (`resolve_execution_provider`) to the architecture diagram in section 2.1, noting that provider resolution diverges between CLI and MCP surfaces. This is not cosmetic -- it is load-bearing for understanding why tests may produce different results depending on which surface they exercise.

---

## 8. Key Insight from the Deliberation

The most consequential finding across all three reviews is not a single bug or missing test, but a structural observation: **the smoke tier as currently designed (mock provider, all modes, structural assertions) tests the error-recovery code path, not the production code path.** The mock provider's canned output does not contain the markdown headings that `parse_synthesis` needs, so `StructuredDeliberation.from_events()` catches the parse failure with a bare `except` and falls back to empty strings. Every green smoke test masks this.

This was identified by the test-architect in Phase 1, disputed in terms of remedy through Phase 4, and resolved in this synthesis by recommending both the mock enhancement and the fixture test. The spec author should treat this as the single highest-leverage change: without it, the eval suite's foundational claim -- that smoke tests catch structural regressions on every commit -- is false.
