### Executive Summary

Spec 061 defines a composable evaluation suite to close a genuine gap: 28 release candidates shipped with bugs that a single engine invocation would have caught. The implementation order in §7 was designed to build the foundation first — fix known production bugs (G1, G6, G11), validate quality baselines, then build cross-surface parity infrastructure. The spec's architecture is sound.

The orchestrator's execution broke this design. Steps 1–4 were completed sequentially. Then the orchestrator jumped to steps 9, 10, 13, and 14, bypassing steps 5, 6, 7, and 8 entirely. Steps 5–8 include two open production bug fixes (G2: path doubling, G12: `VALID_PROVIDERS` hardcoded to only `anthropic` and `openai`). The skip means the engine ships to the smoke CI tier with a known parse-time defect that silently rejects `claude-code`, `gemini`, and every non-anthropic/openai provider in any YAML-configured run — while the step count displays eight strikethroughs. The tests backing steps 9, 13, and 14a are substantively written and not tautologies, but a CI that reports "smoke tests pass" while G12 is open is a false health signal.

The single most important recommendation is to add a visible warning to §7 that corrects the forward-progress framing: steps 5, 6, 7, and 8 are not done, two open severity-P1 bugs remain in production, and no further quality calibration (step 7) or baseline snapshotting (step 8) should run until step 6 closes.

---

### Alignment

- **Sequential dependency documented** (`specs/061-engine-eval-suite.md §7`): The spec explicitly notes "Steps 1–4 are complete. Remaining work starts at step 5." This formulation establishes a readable queue and makes the non-sequential execution gap legible to any auditor who checks the order. The dependency intent was stated; the violation is therefore unambiguous.

- **Marker taxonomy codified** (`specs/061-engine-eval-suite.md §4.3`): Defining four discrete markers (`live`, `integration`, `security`, `eval`) with explicit run conditions creates a falsifiable invariant. An auditor can check each test class against the taxonomy and find violations mechanically.

- **Known gaps table maintained** (`specs/061-engine-eval-suite.md §5`): G2 and G12 carry explicit "Open" status. The table is current. This transparency is correct audit posture and makes the skipped-step problem obvious rather than buried.

- **Step 14 labeled "PARTIALLY DONE," not DONE** (`specs/061-engine-eval-suite.md §7 step 14`): The spec correctly avoids marking step 14 as fully complete. Sub-item status is broken out with "PARTIALLY DONE," "blocked on spec 048," and "not yet implemented." This honesty is the correct pattern.

- **Success criteria numbered and binary** (`specs/061-engine-eval-suite.md §6`): Criteria 3, 4, and 7 carry no "ACHIEVED" marker, giving an unambiguous list of gaps independent of the step numbering.

---

### Missed Opportunities

- **§7 header now misleads navigators**: The header says "Steps 1–4 are complete. Remaining work starts at step 5." After non-sequential execution, steps 5, 6, 7, 8 are undone but steps 9, 10, 13, and 14a-partial are done. Any contributor following the header lands on step 5 (correct) but reads eight strikethroughs as eight forward steps rather than four forward plus four out-of-sequence. The false count is visible to anyone who does not read each strikethrough carefully. Impact: **high** — the progress narrative is wrong and G2/G12 stay invisible behind it.

- **Integration-marked tests run in the smoke CI tier**: `.github/workflows/evals.yml` (smoke job, "Run pytest smoke tests") runs `uv run pytest engine/tests/ -x -q --timeout=30` with no marker filter. Spec §4.3 defines `integration` as "multi-component but in-process" and specifies it runs "pre-release," not on every push. `test_persistence.py` marks `TestPersistListShowRoundTrip` as `@pytest.mark.integration`. That class runs on every push in the smoke tier. The marker taxonomy the spec codified is already violated by the first PR that uses `@pytest.mark.integration`. Impact: **high** — the taxonomy contract becomes meaningless immediately, and future contributors will stop trusting the markers.

- **G2 and G12 open while later steps are closed**: G12 (`VALID_PROVIDERS = ("anthropic", "openai")` hardcoded in `config.py`) means YAML-configured `conversus run` rejects `claude-code`, `gemini`, `ollama`, and all non-hardcoded providers at parse time. G2 (target path resolution doubles relative paths) corrupts file injection. Both are severity P1. The orchestrator closed steps 9, 10, 13, and 14a — none of which touch these bugs. Any quality baseline captured before step 6 closes will reflect a broken provider matrix. Impact: **high** — success criterion #5 claims G1, G3/G11, G6 are resolved but G2 and G12 remain open with no scheduled fix date.

- **Step 11 declined without a tracking issue**: Step 11 ("Build engine-first skill wrapping CLI") was declined as "too large." No GitHub issue was filed. Step 12 ("Cross-surface parity tests — CLI vs MCP vs SDK output comparison") requires step 11 because the CLI-vs-skill parity test requires a skill surface to compare against. Without step 11, step 12 has no implementation path. Success criterion #3 ("CLI, MCP, and SDK surfaces produce structurally identical output") is therefore unreachable. Impact: **high** — an untracked deferral of an architectural prerequisite is functionally abandoned; the success criterion cannot close.

- **"6 cross-axis smoke combinations" has no matching marker**: Step 14 specifies "6 cross-axis smoke combinations" (`specs/061-engine-eval-suite.md §7`), but the marker taxonomy (§4.3) defines no `smoke` marker. The CI labels a job "Smoke tests" but uses no `@pytest.mark.smoke` decorator — it runs all tests without a filter. When the combinatorial matrix is implemented, the developer will have no sanctioned marker to attach. Marking them `integration` (runs pre-release) conflicts with the "every push" intent; leaving them unmarked means they run in all tiers including live. Impact: **medium** — implementation ambiguity on a step that is still open, but the taxonomy gap will be inherited by whichever contributor closes step 14.

- **Step 10 "DONE" credit includes prior art**: The prompt establishes that the smoke CI tier pre-existed PR #101 (see PR #83 reference). PR #101 added the quality (Ollama) and deepeval tiers plus the `workflow_dispatch` inputs. The step 10 description credits PR #101 for the "three-tier" workflow, including the smoke tier PR #83 built. This inflates the orchestrator's contribution and misattributes the smoke tier's provenance. Impact: **medium** — the step is genuinely complete, but the credit narrative is factually wrong and will mislead anyone debugging the smoke tier.

- **Node version drift between spec and implementation**: Spec §7 step 10 states "specify runner requirements: Python 3.12, Node 18." `.github/workflows/evals.yml` uses `node-version: '22'` in both the smoke and quality jobs. This is a Principle XIV violation (CONSTITUTION.md): "After implementing an FR, re-read the FR text. If the implementation deviates, update the spec to match reality." Node 22 LTS is backward-compatible for promptfoo; the runtime risk is low. But the spec records the wrong version. Impact: **low** — but establishes a pattern of spec-vs-implementation drift in the eval suite itself.

---

### Off-Base Assumptions

- **"Remaining work starts at step 5" is now a false statement of sequence**: The spec (`§7`) presents this as a navigational anchor. After non-sequential execution, the anchor points to the right step (5 is indeed undone) but creates a false implication that all steps before 5 are done in order. Steps 9, 10, 13, and 14a are also done, non-sequentially. A contributor planning to add step 7 (deepeval quality calibration) will follow "remaining work starts at step 5" correctly — but the spec provides no warning that calibrating quality before step 6 (G2/G12 fixes) produces baselines against broken behavior. The assumption that sequential numbering implies sequential delivery has been falsified by the execution record.

- **Step 14's three sub-items are independently closeable**: The spec bundles "Governance exit codes, persistence round-trip, combinatorial matrix" as a single step (`§7 step 14`). The orchestrator decomposed it into three independently completable sub-items and marked one partially done. The bundling's rationale was that these three deliverables form a coherent CI/CD consumer contract: exit codes for machine consumption, persistence for human consumption, combinatorial matrix for cross-axis coverage. Treating them as parallel tracks creates a false partial-completion state: the exit-code emission is blocked on spec 048, the combinatorial matrix is deferred indefinitely, and only the persistence round-trip shipped. This is not "step 14 one-third done" — it is the human-facing piece done and the CI-facing pieces absent.

- **The CI smoke tier was established by PR #101**: The step 10 note says "DONE (PR #101): three-tier `.github/workflows/evals.yml` — `smoke` (mock, every push), `quality` (Ollama), `deepeval` (Anthropic)." If the smoke tier pre-existed from PR #83, then PR #101's actual contribution is the quality and deepeval tiers. The three-tier attribution gives PR #101 credit for work that was not its output. The assumption embedded in the DONE notation — that PR #101 introduced the complete workflow — is false.

---

### Actionable Recommendations

1. **Restate §7 progress header to reflect actual execution state** (Priority: P1)
   - **Current state**: "Steps 1–4 are complete. Remaining work starts at step 5." (`specs/061-engine-eval-suite.md §7`)
   - **Proposed change**: Replace with: "Steps 1–4, 9, 10, 13 complete; step 14 persistence sub-item partially done; steps 5, 6, 7, 8, 11, 12, and 14b/c remain open. Steps 6 (G2/G12 bug fixes) and 5 (SKILL.md parity) are the recommended next targets — quality calibration (step 7) and baseline snapshots (step 8) MUST NOT run before step 6 closes."
   - **Rationale**: The current header creates a false forward-progress signal. Eight strikethroughs imply eight sequential steps completed; the actual state is four sequential plus four out-of-sequence, with two P1 bugs still in the production code path.
   - **Risk if ignored**: A contributor starts step 7 (deepeval quality calibration) before step 6. Quality baselines are calibrated against an engine where G12 silently rejects `claude-code` and `gemini` providers. The baselines become permanently wrong.

2. **Fix CI smoke tier to exclude @pytest.mark.integration tests** (Priority: P1)
   - **Current state**: `.github/workflows/evals.yml` smoke job runs `pytest engine/tests/ -x -q --timeout=30` with no marker exclusion.
   - **Proposed change**: Change to `pytest engine/tests/ -x -q --timeout=30 -m "not integration and not live and not eval"`.
   - **Rationale**: Spec §4.3 defines `integration` as "multi-component but in-process" running pre-release, not on every push. `TestPersistListShowRoundTrip` is `@pytest.mark.integration` and currently runs on every push. The marker taxonomy is violated by the CI that was built to enforce it.
   - **Risk if ignored**: Integration tests accumulate in `engine/tests/` and execute on every push. The first slow or resource-intensive integration test silently degrades push-time CI. More fundamentally, `@pytest.mark.integration` stops meaning anything, and contributors stop trusting the taxonomy.

3. **File a tracking issue for step 11 and mark step 12 blocked** (Priority: P1)
   - **Current state**: Step 11 declined as "too large"; no tracking issue filed. Step 12 depends on step 11. Success criterion #3 requires step 12. (`specs/061-engine-eval-suite.md §7 steps 11–12, §6 criterion 3`)
   - **Proposed change**: File a GitHub issue for step 11 with scope boundaries. Add to step 12 in the spec: "BLOCKED on step 11 (GitHub issue #N)." Add to §6 criterion 3: "Not achievable until step 11 lands."
   - **Rationale**: An untracked deferral of an architectural prerequisite is functionally abandoned. Without a tracking vehicle, no contributor will pick up step 11, step 12 cannot be implemented, and success criterion #3 will never close.
   - **Risk if ignored**: The spec reaches a state where all remaining "easy" steps are closed. A future contributor declares the spec done, unaware that SC#3 has had no implementation path since step 11 was declined.

4. **Block steps 7 and 8 on step 6 completion** (Priority: P1)
   - **Current state**: Steps 7 (deepeval quality calibration) and 8 (baseline snapshots) are listed without dependency on step 6 (G2/G12 fixes). G12 is Open and causes YAML-configured `run` to silently reject 11 of 13 registered providers at parse time. (`specs/061-engine-eval-suite.md §5 gap table, §7`)
   - **Proposed change**: Add to step 7 in §7: "Prerequisite: step 6 (G2 and G12 fixes) must be complete. Calibrating quality thresholds before G12 is fixed produces baselines against incorrect provider-resolution behavior."
   - **Rationale**: The 24/24 promptfoo baseline used the mock provider and did not trigger G12. Any real-provider quality run will. A baseline captured before G12 is fixed permanently misrepresents the engine's provider-matrix behavior.
   - **Risk if ignored**: Quality baselines are established against a G12-broken engine. G12 is later fixed, changing provider behavior. The baselines are now stale and the quality CI will flag regressions that are actually improvements.

5. **Define a @pytest.mark.smoke marker or rename step 14's cross-axis deliverable** (Priority: P2)
   - **Current state**: Spec §4.3 defines four markers. Step 14 specifies "6 cross-axis smoke combinations." The CI labels a job "Smoke tests" but uses no marker annotation. (`specs/061-engine-eval-suite.md §4.3, §7 step 14`)
   - **Proposed change**: Either (a) add `smoke` to §4.3 with definition "mock-provider, structural validation, all modes, runs on every push," or (b) rename step 14's deliverable to use an existing marker and explain the choice.
   - **Rationale**: The combinatorial matrix tests, when written, will have no sanctioned home in the taxonomy. Leaving the choice to whichever contributor closes step 14 guarantees inconsistency with the marker contract.
   - **Risk if ignored**: Step 14's matrix tests are marked `integration` (pre-release only) when the spec's intent was every-push coverage, or left unmarked and run in all tiers including live.

6. **Mark step 10 "DONE" with accurate CI contribution attribution** (Priority: P2)
   - **Current state**: Step 10 credits PR #101 with the "three-tier" workflow including the smoke tier. (`specs/061-engine-eval-suite.md §7 step 10`)
   - **Proposed change**: Update step 10 DONE note to: "PR #83 established the smoke tier; PR #101 added the quality (Ollama) and deepeval (Anthropic) tiers and `workflow_dispatch` inputs."
   - **Rationale**: Accurate attribution ensures that the smoke tier's original authoring context is preserved. A contributor debugging the smoke tier should know which PR introduced it.
   - **Risk if ignored**: Low immediate risk. But incorrect provenance misleads anyone tracing CI regressions to their source.

7. **Correct Node version requirement in step 10** (Priority: P2)
   - **Current state**: Step 10 specifies "runner requirements: Python 3.12, Node 18." `.github/workflows/evals.yml` uses `node-version: '22'`. (`specs/061-engine-eval-suite.md §7 step 10; .github/workflows/evals.yml`)
   - **Proposed change**: Update step 10 requirement to "Node 22 LTS."
   - **Rationale**: CONSTITUTION.md Principle XIV requires specs to match what was built. Node 22 is what runs; Node 18 is what the spec claims.
   - **Risk if ignored**: A future contributor downgrades the CI node version "to match spec," introducing a breaking change in the eval pipeline.

8. **Document the step 14 bundle intent to prevent sub-item-closing the full step** (Priority: P2)
   - **Current state**: Step 14 has three sub-items with mixed completion. No note explains their interdependence. (`specs/061-engine-eval-suite.md §7 step 14`)
   - **Proposed change**: Add to step 14: "These three deliverables form the CI/CD consumer contract: exit-code emission (machine consumption) and combinatorial matrix (cross-axis coverage) are co-dependent with spec 048's gate command. The persistence round-trip sub-item MAY ship independently but does NOT close step 14."
   - **Rationale**: Without this documentation, a contributor who closes the exit-code sub-item (when spec 048 lands) may mark the full step done, leaving the combinatorial matrix permanently deferred.
   - **Risk if ignored**: Step 14 is declared done with the combinatorial matrix never implemented, defeating the foundational cross-axis coverage tier the step was named for.

9. **Require step 5 (SKILL.md parity) before any quality-tier work** (Priority: P3)
   - **Current state**: Step 5 is untouched. G10 ("SKILL.md and engine implementations diverged — no parity test") remains Open. (`specs/061-engine-eval-suite.md §5, §7 step 5`)
   - **Proposed change**: Add to §7: "Step 5 is a prerequisite for steps 7–12. Without SKILL.md parity, the engine's Python surface and the SKILL.md surface (used by Claude Code, Codex, OpenCode) can diverge silently. G10 cannot close until step 5 delivers a parity check."
   - **Rationale**: The spec's original motivation (§1: "SKILL.md agent-dispatch masks engine bugs by reimplementing the pipeline as prompt instructions") is exactly the divergence G10 describes. Every step that adds Python-surface tests without a skill-surface check widens the gap.
   - **Risk if ignored**: Steps 7–13 achieve high Python-surface coverage. SKILL.md diverges further. The eval suite closes while the surface that most users actually invoke remains untested.

---

### Referenced Documentation

- `specs/061-engine-eval-suite.md` — §1 (strategic context, SKILL.md masking of engine bugs), §4.3 (marker taxonomy: `live`, `integration`, `security`, `eval`), §5 (gap table: G2, G10, G12 Open), §6 (success criteria 3, 4, 7 unmarked), §7 (implementation order, steps 5–14 with DONE notations and sub-item breakdowns)
- `engine/tests/test_settings.py` — `TestProviderAllFiveLevels` (cascade precedence ordering), `TestEnvVarTypeCoercion` (int coercion, empty-string passthrough), `TestCleanSettingsFixtureInvariants` (fixture contract, `_ENV_VAR_FOR_FIELD` lockstep test)
- `engine/tests/test_phases.py` — `TestIterationLoop.test_three_iterations_dispatch_counts`, `TestIterationLoop.test_three_iterations_revision_naming`, `TestMultiRound.test_stagnation_detection`, `TestMultiRound.test_convergence_detection`, `TestMultiRound.test_pipeline_result_has_round_fields`
- `engine/tests/test_persistence.py` — `TestPersistListShowRoundTrip.test_single_deliberation_round_trip`, `TestPersistListShowRoundTrip.test_multiple_deliberations_round_trip_each`, `TestPersistListShowRoundTrip.test_list_after_cleanup_excludes_pruned`; `@pytest.mark.integration` decorator placement
- `.github/workflows/evals.yml` — smoke job step "Run pytest smoke tests" (no `-m` filter), quality job `workflow_dispatch` gate, deepeval job `ANTHROPIC_API_KEY` guard, `node-version: '22'` in smoke and quality jobs
- `CONSTITUTION.md` — Principle XIV (Spec-Implementation Parity), Principle II (Stable Interfaces: "Changing a stable interface requires updating every consumer in a single atomic change")