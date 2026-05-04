I'll analyze all the provided files and produce the completeness audit review as requested.

Now I have everything I need. Let me also verify the `_make_arbiter_config` helper in `test_phases.py` to confirm no influence variant is set in any of the three arbiter tests:

I now have all the evidence needed. Let me produce the complete audit review.

---

### Executive Summary

Spec 061 is building a composable validation layer for the deliberation engine — a test suite that covers the engine's CLI, MCP, and SDK surfaces with progressively deeper coverage (smoke → quality → deepeval) and validates that orchestration features (multi-round, arbiter, iterations, settings cascade) all behave as specified. The four steps under review form the CI scaffolding and advanced-scenario testing backbone that makes the rest of the suite trustworthy.

Of the four DONE markers, two are accurate (Step 9 MATCH, Step 14's PARTIALLY DONE MATCH), one requires a documented correction to the spec itself (Step 10 REVISE), and one requires follow-up issues to be filed before §3.1.9's P1 rows can be considered closed (Step 13 REVISE). No step rises to ACCEPT: the orchestrator did not falsely claim coverage it didn't produce, but step 13 left two §3.1.9 P1 rows implicitly unaddressed in its DONE annotation.

The most important recommendation: file two follow-up issues against step 13 — one for the `iterations=3` cost-estimate assertion gap and one for the arbiter influence variant pipeline-output gap — and update the step 13 DONE annotation to enumerate what it did and did not cover from §3.1.9.

---

### Alignment

- **Step 9 — "Provider key" correctly scoped to `default_provider`** (`specs/061-engine-eval-suite.md §7 step 9`, `engine/tests/test_settings.py TestProviderAllFiveLevels`): The spec's phrase "provider key at all 5 levels" maps to §3.3.1's "Test by setting provider at each level" — a reference to `default_provider` specifically, not all cascade-eligible fields. `TestProviderAllFiveLevels` correctly exercises `default_provider` with distinct sentinels at env, project, global, and default tiers, then verifies cascade-layer attribution. The multi-field cascade semantics for `default_mode`, `default_model`, and `max_launches` are covered separately in the existing `TestInspectSettingsCascade` class. The implementation correctly partitions these concerns.

- **Step 9 — Type coercion complete within declared type vocabulary** (`engine/tests/test_settings.py TestEnvVarTypeCoercion`): `ConversusSettings` declares exactly one non-string typed field: `max_launches: int`. `TestEnvVarTypeCoercion` covers int coercion (`"42"` → `42`), invalid-int-falls-through-to-default, invalid-int-falls-through-to-lower-tier (preserving global YAML's value without clobbering), string round-trip, and empty-string-treated-as-unset. There are no bool or list fields in the model, so "env var type coercion (plural)" is fully satisfied by the existing type vocabulary.

- **Step 9 — Lockstep enforcement guards against future drift** (`engine/tests/conftest.py:91-96`, `engine/tests/test_settings.py TestCleanSettingsFixtureInvariants`): `conftest._CASCADE_ENV_VARS` is defined as a module-level constant and asserted against `engine.settings._ENV_VAR_FOR_FIELD` in `test_cascade_env_var_list_matches_settings_module`. This is the correct structural guard: any new cascade-eligible field added to `settings.py` that doesn't update `conftest.py` produces a test failure rather than silent test pollution.

- **Step 10 — Three-tier cost partitioning matches §4.3's marker taxonomy** (`evals.yml`, `specs/061-engine-eval-suite.md §4.3`): Smoke / quality / deepeval tiers map to `pytest.mark.smoke` / `pytest.mark.eval` / `pytest.mark.live` respectively. The `workflow_dispatch` gating for Ollama and deepeval tiers correctly implements the "separate, manually-triggered job" that §4.3 and Principle XXIV require for cost-bearing tests.

- **Step 13 — iterations=3 event ordering verified** (`engine/tests/test_phases.py TestIterationLoop.test_three_iterations_events`): The three new tests pin dispatch counts (6 cross-reviews, 6 revisions), filename boundaries (revision.md, revision_2.md, revision_3.md; no _1, no _4), and PhaseStarted/PhaseCompleted pair counts (3 of each). "Cycle count" in the spec's step 13 annotation refers to this event-level verification, and all three axes are covered.

- **Step 14 — PARTIALLY DONE marker accurately self-assessed** (`specs/061-engine-eval-suite.md §7 step 14`): The orchestrator correctly splits the step into done (persist→list→show API round-trip), blocked (exit codes pending spec 048), and not-yet-started (6 combinatorial matrix). The PARTIALLY DONE designation is not a retroactive excuse — it appears in the spec itself as the canonical status.

---

### Missed Opportunities

- **iterations=3 cost-estimate assertion absent**: §3.1.9's "iterations=3" row specifies two key assertions: "3 cross-review/revision cycles" (covered) and "cost estimate reflects 3×" (not covered). `TestCostEstimate` in `test_sdk.py` tests cost estimate structure for default 1-iteration configs but has no parametrized variant for `iterations=3`. The step 13 DONE annotation enumerates only the dispatch/naming/events axes, silently leaving the cost-estimate axis unclaimed. A regression where the cost estimate ignores the `iterations` multiplier (returning 1× instead of 3×) passes all current tests. Impact: **high** — §3.1.9 explicitly marks this P1; the cost estimate is the user-visible ceiling that gates whether a run is authorized.

- **Arbiter influence variant pipeline output not tested**: §3.1.9 specifies "arbiter influence=binding vs advisory | Config variants | Output headings change per influence level" as P1. Template context tests in `test_templates.py TestBuildArbitrationContextInfluenceLevel` verify that `build_arbitration_context` populates `INFLUENCE_LEVEL` correctly in context (`ctx.INFLUENCE_LEVEL == InfluenceLevel.ADVISORY`). Config-parsing tests in `test_006_inter_round_arbitration.py TestInfluenceFieldParsed` verify that all three values parse. But neither verifies that the rendered `resolution.md` file actually contains different heading text across influence levels. The `_make_arbiter_config` helper in `test_phases.py` creates `ArbiterConfig` with no `influence` argument (defaults to "binding") for all three arbitration trigger tests. No pipeline-level test runs with `influence="advisory"` and asserts heading-level output differences. Impact: **high** — §3.1.9 marks this P1; an influence-level heading regression would be invisible to the entire test suite.

- **Node 18→22 upgrade undocumented**: The spec step 10 explicitly says "Node 18"; `evals.yml` uses `node-version: '22'` throughout with no inline comment, no SIR entry, and no spec annotation acknowledging the change. Principle XIV (Spec-Implementation Parity) identifies this as a spec bug: "If the implementation deviates… update the spec to match reality." Node 22 is the correct choice (Node 18 reached EOL April 2025), but the spec's runner requirements are now stale. Impact: **medium** — the discrepancy is harmless in practice but creates the same spec-drift problem the spec's own §14 test caught for the CLI slug contract.

- **OPENAI_API_KEY and GOOGLE_API_KEY not wired in CI**: The spec's provider matrix at §3.1.2 lists `openai (OPENAI_API_KEY)` and `gemini (GOOGLE_API_KEY)` as real-API-call providers with Auth method = direct API key. The orchestrator's rationale ("GitHub Actions can't run the `claude` CLI") covers subprocess-based providers (claude-code, aider, opencode, codex) but not API-key providers. `openai` and `gemini` require only env var secrets — the same mechanism that provisions `ANTHROPIC_API_KEY`. These providers are never exercised in CI with real credentials. Impact: **medium** — provider-specific auth bugs (e.g., rate-limit header differences, Gemini response format variations) are only caught locally or in production.

- **CLI persist→list→show not tested**: `TestPersistListShowRoundTrip` exercises `persist_deliberation`, `list_deliberations`, and `read_deliberation_file` at the module-API level. No test calls `uv run conversus list` or `uv run conversus show <slug>` as a subprocess and parses the output. §3.1.3 explicitly lists CLI surface tests for `conversus status`; list and show are the analogous persistence surface commands. An argument-parsing regression in the CLI entry points for these commands goes undetected. The step 14 annotation acknowledges the gap implicitly but doesn't file it as a follow-up issue. Impact: **medium** — the API tests validate the module but not the user-facing surface.

- **Synthesis assertion in round-trip is shape-level**: `test_single_deliberation_round_trip` asserts `"Synthesis" in synthesis` and `"verdict" in synthesis`. Per Principle IX's behavior-over-shape extension, these are shape tests (substring presence) rather than behavioral assertions. A regression where the persisted synthesis is truncated to 20 bytes containing both words passes both assertions. A behavioral assertion would constrain minimum length, heading structure, or the presence of specific verdict language anchored to the deliberation's inputs. Impact: **low** — latent, not a blocking gap.

- **`clean_settings` not used by persistence round-trip tests**: `TestPersistListShowRoundTrip` uses `project_root` (a bare `tmp_path / "project"`) without `clean_settings`. Currently safe because `persist_deliberation` takes an explicit `project_root` and doesn't read the settings cascade. If a future implementation routes persistence through settings-aware paths, the round-trip tests will silently inherit the developer's real `CONVERSUS_*` environment. Impact: **low** — no current failure, purely defensive gap.

---

### Off-Base Assumptions

- **"Step 13 covers arbiter trigger conditions" subsumes §3.1.9's influence row**: The step 13 DONE annotation lists three arbiter trigger tests as covering "arbiter trigger conditions" from §3.1.9. But §3.1.9 contains a separate P1 row for "arbiter influence=binding vs advisory | Output headings change per influence level" that is distinct from trigger conditions. The annotation treats the two rows as one. This is not a false reading of the spec — the step 13 original description says "arbiter trigger conditions" without explicitly naming the influence row — but it creates an implicit closure of a P1 item that has no test coverage at the pipeline output level. The correct understanding: trigger condition coverage (3 tests) and influence variant output coverage (0 pipeline tests) are different rows with different verification requirements.

- **"iterations=3 cycle count" is fully satisfied by dispatch count + event ordering**: The step 13 annotation claims the three new tests cover "iterations=3 cycle count" as enumerated in the spec. §3.1.9's row for iterations=3 specifies two key assertions joined with a comma: "3 cross-review/revision cycles, cost estimate reflects 3×." The annotation addresses only the first half. The cost estimate assertion ("reflects 3×") requires testing through the handler or SDK layer, not at the `run_pipeline` level — `PipelineResult` does not expose a cost estimate field. `TestCostEstimate` in `test_sdk.py` exists but does not include an iterations=3 variant. The correct understanding: the DONE annotation should explicitly note which part of the §3.1.9 row it covers and which part remains open.

---

### Actionable Recommendations

1. **File iterations=3 cost-estimate issue** (Priority: P1)
   - **Current state**: Step 13 DONE annotation lists `test_three_iterations_dispatch_counts` / `_revision_naming` / `_events` as covering §3.1.9's iterations=3 row. The "cost estimate reflects 3×" assertion from that row is not tested anywhere. `TestCostEstimate` in `test_sdk.py` tests only the default 1-iteration config.
   - **Proposed change**: File GitHub issue: "spec 061 §3.1.9 follow-up — iterations=3 cost estimate assertion." Add a parametrized test in `test_sdk.py TestCostEstimate`: `d = Deliberation(question="...", provider="mock", iterations=3); cost = d.cost_estimate; assert cost["cross_review"] == 6` (3 iterations × 2 pairs). Update the step 13 DONE annotation: "cost estimate 3× assertion: not yet covered — tracked in issue #N."
   - **Rationale**: §3.1.9 marks this P1 and the assertion is explicit in the spec row text. The dispatch count is a proxy; the cost estimate is the user-visible ceiling enforced before a run executes.
   - **Risk if ignored**: A cost estimate bug that undercounts for iterations > 1 would silently allow runs that exceed the user's stated `max_launches` budget.

2. **File arbiter influence output-heading issue** (Priority: P1)
   - **Current state**: Template context tests (`test_templates.py TestBuildArbitrationContextInfluenceLevel`) verify `INFLUENCE_LEVEL` is populated in context. No test runs the pipeline with `influence="advisory"` and asserts the `resolution.md` heading differs from `influence="binding"`.
   - **Proposed change**: File GitHub issue: "spec 061 §3.1.9 follow-up — arbiter influence variant output heading test." Add one new test in `test_phases.py TestArbitration` using `_make_arbiter_config` with explicit `influence="advisory"`, run the pipeline, read `arbitration/resolution.md`, and assert the heading contains the influence-level string. Update step 13 DONE annotation: "influence variant output headings: not yet covered — tracked in issue #N."
   - **Rationale**: §3.1.9 marks this P1 with a specific behavioral assertion ("Output headings change per influence level"). Template context tests verify the variable is in scope; they do not verify that the template renders it into the output file, and they do not test the pipeline-level behavior.
   - **Risk if ignored**: An influence-level heading regression is invisible to all existing tests. A binding ruling mislabeled as advisory has semantic downstream consequences for any agent reading the resolution file.

3. **Update spec Node version to match evals.yml** (Priority: P1)
   - **Current state**: `specs/061-engine-eval-suite.md §7 step 10` says "runner requirements: Python 3.12, Node 18, API key secrets provisioning." `evals.yml` uses `node-version: '22'` throughout.
   - **Proposed change**: Update step 10's DONE annotation to: "Node 22 LTS (spec said Node 18 — Node 18 EOL April 2025; bumped to Node 22 Active LTS, undocumented). Update spec runner requirement to Node 22."
   - **Rationale**: Principle XIV (Spec-Implementation Parity): "If the implementation deviates… update the spec to match reality. A spec that says X when the implementation does Y is a bug in the spec." The Node version is a stated runner requirement.
   - **Risk if ignored**: A future CI maintainer sees "Node 18" in the spec, pins `node-version: '18'` restoring EOL behavior, and breaks the pipeline silently.

4. **Track §3.1.9 influence row explicitly in step 13 annotation** (Priority: P1)
   - **Current state**: Step 13 DONE annotation says "arbiter triggers: test_always_trigger, test_disputes_remain_trigger_with_disputes, test_disputes_remain_trigger_no_disputes" and implies §3.1.9's arbiter rows are covered. The influence row is not enumerated as DONE or as an open gap.
   - **Proposed change**: Add to step 13 annotation: "NOT YET COVERED from §3.1.9: arbiter influence=binding vs advisory output heading verification — tracked in issue #N (see recommendation 2 above)."
   - **Rationale**: The omission creates an implicit false closure. The spec's §7 is the implementation ledger; rows that aren't explicitly marked open will be assumed done by future readers.
   - **Risk if ignored**: The §3.1.9 influence P1 row has no owner and no issue, making it easy to miss in the next release gate.

5. **Wire OPENAI_API_KEY in a provider-matrix CI job** (Priority: P2)
   - **Current state**: `evals.yml` deepeval job provisions only `ANTHROPIC_API_KEY`. §3.1.2's `openai (OPENAI_API_KEY)` and `gemini (GOOGLE_API_KEY)` providers are never exercised in CI with real credentials.
   - **Proposed change**: Add a `provider-matrix` job (workflow_dispatch only, not on push): run `uv run conversus decide "Test question" --provider openai --format json` and `--provider gemini`, guarded by `if: secrets.OPENAI_API_KEY != ''` etc. Mark corresponding tests `@pytest.mark.live`. Document in step 10 annotation.
   - **Rationale**: §3.1.2 lists both providers as "real API call" requiring auth. The subprocess-provider constraint (no `claude` CLI on runners) does not apply to direct-API providers. The existing reasoning conflates two different provider categories.
   - **Risk if ignored**: Openai- or Gemini-specific auth, rate-limit, or response-format regressions are invisible in CI.

6. **File CLI persist→list→show follow-up issue** (Priority: P2)
   - **Current state**: `TestPersistListShowRoundTrip` tests module APIs. No CLI subprocess test for `conversus list` / `conversus show <slug>` exists. Step 14 acknowledges the gap implicitly ("the actual CLI workflow") but has no associated issue number.
   - **Proposed change**: File GitHub issue: "spec 061 step 14 follow-up — CLI-surface persist→list→show." Test via `subprocess.run(["uv", "run", "conversus", "list", "--format", "json"])` and `subprocess.run(["uv", "run", "conversus", "show", slug])`. Add to step 14 annotation as an explicitly tracked open item.
   - **Rationale**: §3.1.3 lists CLI commands as outside-in surface tests. Module-API tests catch implementation bugs but not CLI argument parsing, flag handling, or format-output regressions.
   - **Risk if ignored**: A `conversus show` argument parsing regression goes undetected until user report.

7. **Clarify step 9's scope annotation** (Priority: P3)
   - **Current state**: Step 9 says "provider key at all 5 levels" — ambiguous between "one key (default_provider)" and "all cascade-eligible keys."
   - **Proposed change**: Update to: "provider key (`default_provider`) at all 5 levels — cascade semantics for `default_mode`, `default_model`, `max_launches` covered by `TestInspectSettingsCascade`."
   - **Rationale**: Prevents a future reviewer from filing a "TestProviderAllFiveLevels is incomplete" issue. The multi-field coverage exists; it's in a different test class.
   - **Risk if ignored**: Low — the current annotation is unambiguous to anyone who reads both the spec text and §3.3.1 together. Pure clarity improvement.

8. **Harden round-trip synthesis assertion** (Priority: P3)
   - **Current state**: `test_single_deliberation_round_trip` asserts `"Synthesis" in synthesis` and `"verdict" in synthesis`.
   - **Proposed change**: Replace with: `assert synthesis.startswith("# Synthesis")` (structural heading) and `assert len(synthesis) > 100` (non-trivial content). Optionally assert `"The verdict is" in synthesis` using content from the `fake_output` fixture's known synthesis text.
   - **Rationale**: Principle IX behavior-over-shape: the current assertions are shape tests (substring presence). The `fake_output` fixture writes a known synthesis with deterministic content; the test can assert that deterministic content survives the round-trip verbatim.
   - **Risk if ignored**: A truncation or encoding bug in `persist_deliberation` → `read_deliberation_file` passes the round-trip test.

---

### Summary Verdicts

| Step | Verdict | Rationale |
|---|---|---|
| Step 9 | **MATCH** | "Provider key" = `default_provider` correct; type coercion complete per model; `clean_settings` P0 scoping accurate |
| Step 10 | **REVISE** | Node 18→22 undocumented (Principle XIV); API key scope acceptable for 3-tier design but should be explicitly narrowed in spec |
| Step 13 | **REVISE** | Enumerated trigger conditions covered; two §3.1.9 P1 rows (cost estimate 3×, influence output headings) implicitly unclosed |
| Step 14 | **MATCH** | PARTIALLY DONE marker accurate; API-level done, CLI surface and combinatorial matrix correctly identified as open |

---

### Referenced Documentation

- `conversus-oss/specs/061-engine-eval-suite.md` — §2.2 (composability contract / max launches), §3.1.2 (provider matrix), §3.1.3 (CLI surface tests), §3.1.9 (multi-round/arbiter/iteration test rows with P1 designations), §3.3.1 (settings cascade definition), §4.3 (test markers), §6 (success criteria), §7 (implementation order steps 9, 10, 13, 14)
- `conversus-oss/engine/tests/test_settings.py` — TestProviderAllFiveLevels (L lines covering all 5 tiers), TestEnvVarTypeCoercion, TestCleanSettingsFixtureInvariants.test_cascade_env_var_list_matches_settings_module
- `conversus-oss/engine/tests/conftest.py` — `_CASCADE_ENV_VARS` (L91–96), `clean_settings` fixture (L114–137)
- `conversus-oss/engine/tests/test_phases.py` — TestIterationLoop.test_three_iterations_dispatch_counts, test_three_iterations_revision_naming, test_three_iterations_events; TestArbitration.test_always_trigger, test_disputes_remain_trigger_with_disputes, test_disputes_remain_trigger_no_disputes; `_make_arbiter_config` (L907–916 — no influence field set)
- `conversus-oss/engine/tests/test_templates.py` — `_make_config_with_arbiter_influence` (L773–798), TestBuildArbitrationContextInfluenceLevel (L801–855)
- `conversus-oss/engine/tests/test_006_inter_round_arbitration.py` — TestInfluenceDefault (L226–245), TestInfluenceFieldParsed (L248–267)
- `conversus-oss/engine/tests/test_persistence.py` — TestPersistListShowRoundTrip (test_single_deliberation_round_trip, test_multiple_deliberations_round_trip_each, test_list_after_cleanup_excludes_pruned)
- `conversus-oss/engine/tests/test_sdk.py` — TestCostEstimate (L357–393; iterations=3 variant absent)
- `conversus-oss/.github/workflows/evals.yml` — smoke/quality/deepeval job definitions, `node-version: '22'`, secrets provisioning
- `conversus-oss/engine/config.py` — `ArbiterConfig.influence` field (L73), three-value Literal constraint (L73, L550–564)
- `conversus-oss/CONSTITUTION.md` — Principle IX behavior-over-shape extension; Principle XIV (Spec-Implementation Parity)