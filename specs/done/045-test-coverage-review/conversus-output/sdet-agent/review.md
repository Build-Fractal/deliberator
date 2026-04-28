# SDET Review — conversus Engine & Linter Test Suite

**Reviewer:** SDET agent (Round 1 of 2, cooperative deliberation)
**Scope:** 9 test files (~5,550 lines) covering `engine/` (errors, models, _root, cost, events, phases, config, templates) and `linter/` (validate, usage, quality, question_classifier, output_contract).
**Lens:** behavioral assertions, edge cases, error-path specificity, parametrization, branch coverage, isolation, mocking, naming.

Overall the suite is notably stronger than average — most tests check observable state, exception types are usually matched against substrings, and there is substantial use of fixtures and real reference files. The findings below are concrete weaknesses a cross-reviewer can challenge or extend; I flag everything that fails the discipline bar even when the test is "good enough" in practice.

---

## 1. BEHAVIORAL ASSERTIONS

### 1.1 Weak "not None / truthy / >= 0" assertions

| Finding | File:Line | Why it's weak |
|---|---|---|
| `assert result["estimated_usd"] >= 0` | `tests/test_engine_core.py:776` | Tautology for a cost calculation with positive constants; will pass even if the formula multiplies by zero. Should assert the concrete dollar figure (deterministic given inputs). |
| `assert duration_ms >= 0` | `tests/test_engine_phases.py:253` | Wall-clock timing is non-deterministic, but a tighter bound like `0 <= d < 1000` would at least catch a negative or astronomically large duration bug. |
| `assert isinstance(emitter, NullEmitter)` | `tests/test_engine_core.py:260` | Test body loops 10 emits but the only assertion is that the emitter is still its own type — asserts nothing about the emits. The invariant should be `emitter._queue` doesn't exist / no side effect observable. |
| `assert result.headline  # non-empty` | `tests/test_linter_output_contract.py:294` | Truthy check. Should assert exact or substring value. |
| `assert result.summary` | `tests/test_linter_output_contract.py:295` | Same issue. |
| `assert result.estimated_usd > 0` with `agent_count=0` | `tests/test_engine_core.py:835` | The comment says "Synthesis still runs → total_launches >= 1" — test only asserts `>0`. A specific expected USD (computable from `synthesis=1 launch × (4000/1M × 3 + 2000/1M × 15)`) should be asserted. |
| `assert result.dispute_count >= 1` | `tests/test_linter_quality.py:170, 181, 281` | `>=1` is weaker than an exact count — the fixture is deterministic, so we should know the true count. |
| `assert len(result.agent_names) >= 2` | `tests/test_linter_quality.py:326, 361` | Weak lower-bound on a deterministic fixture. |
| `assert count > 0` | `tests/test_linter_output_contract.py:180` | Again, `test_real_monorepo_has_convergence` should know the exact count. |
| `assert metrics.date_range == "N/A"` is fine, but the follow-up `assert metrics.run_distribution == {}` is the only use of equality in that test | `tests/test_linter_usage.py:335-336` | not a finding — noted as contrast. |

### 1.2 `with pytest.raises(Exception)` — over-broad

The suite repeatedly uses the bare `Exception` catch instead of the concrete `ValidationError` (Pydantic):

| Location | Current | Should be |
|---|---|---|
| `tests/test_engine_phases.py:282` | `with pytest.raises(Exception):  # ValidationError` | `pytest.raises(ValidationError)` (already imported elsewhere) |
| `tests/test_engine_config.py:854` | `with pytest.raises(Exception):  # pydantic raises ValidationError` | `pytest.raises(ValidationError, match="frozen")` |
| `tests/test_engine_config.py:869` | `with pytest.raises(Exception):` | Same |
| `tests/test_linter_classifier.py:313` | `with pytest.raises(Exception):` | `pytest.raises(ValidationError)` |
| `tests/test_linter_output_contract.py:356` | `with pytest.raises(Exception):` | Same |
| `tests/test_linter_output_contract.py:389` | `with pytest.raises(Exception):` | Same |

A bare `Exception` catch will silently swallow a `NameError` or `AttributeError` introduced by a bad refactor — it passes when the test body crashes instead of when frozen-ness is enforced. Zero-cost fix: import `ValidationError` and match a substring.

### 1.3 Functions called without asserting the return value

| Location | Issue |
|---|---|
| `tests/test_engine_core.py:285` | `int(entry.session_id, 16)` parses as hex but never asserts the result. If `token_hex` ever returned the empty string, `int("", 16)` would raise `ValueError` — the test would fail with the wrong message. Prefer: `assert re.fullmatch(r"[0-9a-f]{8}", entry.session_id)`. |
| `tests/test_linter_validate.py:242-243` | `names[0].index("AAA") >= 0` — `str.index` already raises `ValueError` on miss, so the comparison is vacuous. Use `names[0].startswith("...")` or `assert "AAA" in names[0]`. |
| `tests/test_linter_classifier.py:282-283` | `test_decision_missing_constraints_non_interactive` comments "may be sufficient or may fall to vague — either way check no crash" and asserts only `isinstance(result, ClassificationResult)`. This is effectively a smoke test. Pin the behavior: pick one input that deterministically lands in one branch and assert that branch. |

### 1.4 Tests that assert something will happen but not *what*

| Location | Issue |
|---|---|
| `tests/test_engine_phases.py:283-287` | `test_pipeline_error_is_exception` raises `PipelineError("test")` inside `pytest.raises(PipelineError, match="test")` — that's fine. But the surrounding `test_frozen` catches bare `Exception`. |
| `tests/test_linter_usage.py:192-195` | `lines = usage_file.read_text().strip().splitlines(); assert len(lines) == 1; parsed = json.loads(lines[0]); assert parsed["quality_passed"] is True` — good. But no assertion on other required JSONL fields (`session_id`, `version`, `timestamp`, `dispute_count`). A regression that dropped `dispute_count` from the log would not be caught by this test. |
| `tests/test_engine_phases.py:136` | `test_cli_validates_successfully` asserts `"valid against schema" in result.output` but never inspects that `files_checked > 0` from the verbose path. A CLI that validates *zero* files would silently pass this assertion. |

---

## 2. EDGE CASES — gaps

### 2.1 Empty / boundary inputs not covered

| Module | Missing edge case |
|---|---|
| `engine.cost.estimate_cost_usd` | **Negative agent_count** — the formula `agent_count * (agent_count - 1)` yields positive nonsense for `agent_count=-1` (returns 2). No test pins this. |
| `engine.cost.estimate_cost_usd` | **Negative iterations** — test covers `iterations=0` for `estimate_cost` (line 757), but `estimate_cost_usd` never exercises 0 or negative. |
| `engine.cost.estimate_cost_usd` | **`avg_input_tokens=0, avg_output_tokens=0`** — cost should be exactly 0. |
| `engine.models.StructuredDeliberation.from_events` | **Empty events list** — never tested. `test_rounds_completed_defaults_to_one_with_no_review_phases` tests a list with one synthesis event, not `[]`. With `[]`, `rounds_completed` path is `sum(...) == 0 → rounds_completed = 1`, and the `unique_agents` set is empty — the code constructs a summary saying "0 agents in X mode completed 0 phases." That entire path is uncovered. |
| `engine.models.StructuredDeliberation.from_events` | **Both `- ` and `- **` bullet styles in dispute section** — `test_parses_disputes_bullet_list` covers this one specific pattern, but the regex in models.py:180-185 supports many more heading variants (`Key Disputes`, `Open Disputes`, `Outstanding Disputes`, `Disputed Areas`, `Unresolved Tensions`, `Remaining Contradictions`, etc.). None are tested. |
| `engine.errors.map_engine_error` | **`ProviderError` with `category=None`** — `getattr(exc, "category", "unknown")` path returns `"unknown"` and falls to the 502 branch. Not tested: only `"mystery"` string is (line 131). `None` and missing attribute are distinct paths. |
| `engine.events.AgentCompleted` | **Unicode agent names** — agent names like `"alice-β"` or `"Эмми"` never tested despite being valid strings. |
| `engine.templates.fill_template` | **`AGENT_NAME = ""`** (empty string) — substitution into `"Hello {AGENT_NAME}!"` would produce `"Hello !"` but nothing validates that this is intentional. |
| `engine.templates._extract_remaining_disputes` | **BEGIN marker followed immediately by END marker (empty block)** — untested. |
| `engine.templates._extract_remaining_disputes` | **Multiple BEGIN markers in one text** — untested (only first should win). |
| `linter.validate.extract_variables` | **Variable with digits only** like `{123}` — not tested. Pattern may or may not match; the test at `test_linter_validate.py:169-173` covers `MY_VAR_1` and `A2B` but not leading-digit or digit-only. |
| `linter.validate.extract_headings` | **Setext headings (`===` / `---`)** — only ATX (`#`) style is tested. If the parser supports setext it's untested; if not, a comment would document the limit. |
| `linter.validate.extract_headings` | **Headings with markdown embedded** like `## **bold** heading` — not tested. |
| `linter.quality._normalize_agent_name` | **Name with unicode diacritics** — `"josé"` → `"José"`? not tested. |
| `linter.quality._extract_dispute_block` | **Multiple BEGIN/END pairs** — ambiguous; untested. |
| `linter.question_classifier.classify_question` | **Whitespace-only string** — `test_empty_string` covers `""` and `test_none_input` covers `None`, but `"   \n\t  "` is not explicitly tested against the short-input rule. |
| `linter.question_classifier._has_alternatives` | **Single-letter alternatives** like `"A or B"` — not covered. `test_decision_alts_but_no_context_no_detail` uses `"Vue or React"`. |
| `linter.usage.summarize_usage` | **Single-line JSONL with unknown keys** — tolerated? untested. |
| `linter.output_contract._extract_agent_count` | **Whitespace-padded tables** — `|  Agents  |   2   |` — regex sensitivity untested. |
| `linter.output_contract._extract_phases_completed` | **Negative number in header** — `**Phases completed:** -3` — what happens? untested. |
| `engine.config.parse_config` | **`target: []`** (empty list) — behavior? untested; only `target: "empty/"` directory case is covered at line 366. |
| `engine.config.parse_config` | **Agent `name: ""`** (empty string) — probably caught by `AGENT_NAME_RE`, but not asserted. |
| `engine.config.parse_config` | **`rounds: 1.5`** (float instead of int) — not tested. `"many"` (string) is. |
| `engine.config.parse_config` | **`iterations: 10` (very large)** — no upper bound test; does a 10,000-iteration config parse? |
| `engine._root.find_project_root` | **Anchor walk depth > 10** — the code caps at 10 via `for _ in range(10)` (line 44). Cap boundary never exercised; a 12-deep tree would silently fall through to strategy 2/3, masking bugs. |

### 2.2 Off-by-one / single-element coverage

| Test | Issue |
|---|---|
| `tests/test_engine_core.py:740-745` (`test_one_agent_yields_zero_cross_review`) | Good single-agent case. But the **two-agent** `cross_review = 2 * 1 = 2` case is in a different test and not asserted side-by-side. Fine. |
| `tests/test_engine_phases.py:290-298` | `_RoundResult.defaults` — good. No test for a list with exactly one item. |
| `tests/test_linter_output_contract.py:145-149` | `cross_reviews_performed` covers 0, 1, 2, 3 agents — correct boundary coverage. Good. |
| `tests/test_linter_validate.py:215-219` (`test_no_errors_when_all_known`) | Covers multi-element known set but not single-element `known = frozenset({"X"})`. Low risk. |

---

## 3. ERROR PATHS

### 3.1 `pytest.raises` without `match=` (weak)

| Location | Current | Should match |
|---|---|---|
| `tests/test_engine_core.py:98` | `pytest.raises(ValidationError)` | `match="status_code"` or similar — tests the specific missing-field |
| `tests/test_engine_core.py:208` | `pytest.raises(ValidationError)` | `match="agent_count"` — pins the int coercion failure |
| `tests/test_engine_core.py:328` | `pytest.raises(ValidationError)` | `match="frozen"` |
| `tests/test_engine_core.py:336` | `pytest.raises(ValidationError)` | `match="duration_ms"` |
| `tests/test_engine_core.py:394` | `pytest.raises(ValidationError)` | `match="agent_reviews"` or the first missing field |
| `tests/test_linter_usage.py:294` | `pytest.raises(FileNotFoundError)` | `match="nonexistent.md"` — ensures the path is in the message |
| `tests/test_linter_quality.py:486-487` | `pytest.raises(FileNotFoundError)` | `match="missing.md"` |
| `tests/test_linter_output_contract.py:273-274` | `pytest.raises(ValueError)` | already matched at line 269 (`"empty"`) for one test — the whitespace test should match too. `match="empty"` |
| `tests/test_engine_templates.py:148` | `pytest.raises(TemplateError, match="not found")` | **Good** — this is the pattern the whole suite should adopt |
| `tests/test_engine_templates.py:336, 343` | `pytest.raises(TemplateError, match="not found")` | **Good** |
| `tests/test_engine_phases.py:436` | `pytest.raises(asyncio.CancelledError)` | No `match` possible on `CancelledError` itself — acceptable |
| `tests/test_engine_phases.py:287` | `pytest.raises(PipelineError, match="test")` | **Good** |
| `tests/test_engine_phases.py:472` | `pytest.raises(PipelineError, match="Phase 1")` | **Good, specific** |
| `tests/test_engine_phases.py:704` | `pytest.raises(PipelineError, match=r"Phase 3 \(revision")` | **Excellent** — regex + phase label |

### 3.2 Missing error-path tests for source-code `raise` sites

From `grep raise \w+Error` I identified these raise sites; cross-referencing with test coverage:

**`engine/config.py`** — 46 raise sites. Covered tests:
- Lines 191, 196, 203 (preset name/category/prompt validation) → covered by `TestLoadPresetFile`.
- Lines 223, 229, 234, 241, 247, 250 → **all covered**.
- Lines 266 (composition non-composable) → `test_non_composable_in_composition_raises`.
- Lines 289 (3-preset max), 298 (ambiguous unqualified) → covered.
- Lines 322, 330 → preset-resolution errors, covered.
- Line 375 (`agents[{i}]: name required`) → `test_agent_missing_name`.
- Lines 387 (agent name regex), 400 (duplicate) → covered.
- Lines 425, 437, 448, 455, 464, 470, 478 (arbiter validation) → **all covered** by `TestArbiterValidation` and `TestArbiterPresetAndDocs`.
- Line 517 (config not found), 523 (not a mapping), 535 (mode), 543 (output), 549 (target), 561 (invalid mode), 574 (rounds), 579 (stagnation), 584 (validate_templates), 589 (provider), 597 (<2 agents), 602 (agent not mapping), 606, 613, 622, 631, 635, 644 → **covered**.
- **Gap**: line 107 `_assemble_prompt` escape paths not in this test scope; line 161 (composition type check) — only reached via exotic preset combos.
- **Gap**: line 387 tests `uppercase` and `starts-with-hyphen`, but not `starts-with-underscore` nor `contains exclamation`. The regex test at `test_agent_name_regex_invalid` (line 838-843) covers these at the regex level but NOT through `parse_config`, so the error-message path for these particular failures is untested.

**`engine/templates.py`** — raise sites at 104, 133, 143, 206, 275, 605:
- 104 (templates_dir not found after all strategies): **not covered** — the test `test_falls_back_to_engine_parent` (line 122-133) always succeeds because the real templates dir exists. There's no test that drives `find_templates_dir` into its `raise` branch.
- 133, 143 (load_template not found / draft marker): covered by `test_missing_template_raises` and `test_draft_template_rejected`.
- 206 (fill_template unfilled var): covered by `test_unfilled_variable_raises`.
- 275 (agent not found in cross-review ctx): covered.
- 605 (arbiter not configured for arbitration ctx): covered.

**`linter/validate.py`** — raise sites at 119 (can't locate root), 133 (variables.yml missing), 147 (mode schema missing):
- 119: covered by CLI test `test_cli_exits_2_when_project_root_missing` via monkeypatch, **but not by a direct `find_project_root()` call** in an environment where all three strategies legitimately fail. The existing test patches `find_project_root` to raise, which doesn't exercise the real branches.
- 133: covered by `test_missing_file_raises`.
- 147: covered by `test_missing_mode_raises`.

**`linter/output_contract.py`** — single raise at line 351 (`"empty"`): covered by `test_empty_text_raises` and `test_whitespace_only_raises`.

**`linter/models.py`** — raise sites at 154, 165 (Pydantic validators): **not covered in test_linter_validate.py**. These are `raise ValueError(...)` inside Pydantic validators for `VariableDefinition` and `ModeSchema` — they fire when a variables.yml / mode YAML file has a malformed entry. No test constructs such a malformed file. These raise sites live behind the `VariablesSchema.model_validate` and `ModeSchema.model_validate` calls.

**`engine/phases.py`** — raise sites at 275, 439:
- 275 (`PipelineError` — Phase 1 all agents fail): covered by `test_all_agents_fail_phase_1_raises`.
- 439 (`PipelineError` — Phase 3 all agents fail): covered by `test_revision_failure_counted_surviving_agents_filtered`.

### 3.3 Exception-type vs message

`tests/test_engine_core.py:672-679` (`test_raises_filenotfound_when_nothing_matches`) **does it correctly** — matches both type and message substring. Good model to follow.

---

## 4. PARAMETRIZATION

### 4.1 Loops inside test bodies that should be `@pytest.mark.parametrize`

| Location | Loop | Fix |
|---|---|---|
| `tests/test_engine_core.py:249-258` | `for i in range(10): emitter.emit(...)` | Acceptable — not varying inputs, testing emit-many semantics. No fix needed. |
| `tests/test_engine_core.py:846-852` | `for provider, options in PROVIDER_MODEL_OPTIONS.items(): for entry in options: assert ...` | Should parametrize over `(provider, entry)` so individual rows report individually. First failure currently hides subsequent ones. |
| `tests/test_engine_core.py:855-859` | `for model_id, pricing in MODEL_PRICING.items(): assert ...` | Same — parametrize over model_id. |
| `tests/test_linter_quality.py:289-313` | `TestFallbackFunctions` has 6 independent tests — already flat. Good. |
| `tests/test_linter_usage.py:205-211` | `for _ in range(3): log_usage(...)` | Valid — this is "stress" exercise, not input variation. OK. |
| `tests/test_linter_usage.py:405-422` | Two loops setting up 2 passing + 2 failing fixtures | Acceptable — fixtures, not assertions. |
| `tests/test_engine_config.py:832-836` | `test_agent_name_regex_valid` — 4 separate asserts | Should parametrize: `@pytest.mark.parametrize("name", ["alice", "agent-1", "agent_name", "a1"])`. |
| `tests/test_engine_config.py:838-843` | `test_agent_name_regex_invalid` — 5 separate asserts | Same. |
| `tests/test_linter_validate.py:75-84` | `ALL_MODES` list used via `@pytest.mark.parametrize("mode", ALL_MODES)` at line 123 and 373 | **Good pattern — already parametrized**. |

### 4.2 Tests that already parametrize well (positive examples)

- `test_linter_classifier.py:33-44` — `TestHasDecisionWords.test_detects_decision_words` uses `@pytest.mark.parametrize("text", [...])`. Reference quality.
- `test_linter_classifier.py:56-62, 68-79, 92-102` — all parametrized.
- `test_linter_validate.py:123-127` — `test_loads_every_mode` parametrized over all 8 modes.
- `test_linter_validate.py:373-396` — `test_real_templates_are_clean` parametrized over all modes (excellent).

---

## 5. BRANCH COVERAGE — gaps by source-file branch

### 5.1 `engine/errors.py`

All 8 branches covered (`TestMapEngineError` is exhaustive, including the unknown-category fallback). **No gap.**

### 5.2 `engine/events.py`

Branches covered: CallbackEmitter.emit (both single and many), NullEmitter.emit, AsyncQueueEmitter init/emit/close/events, sentinel-based termination. **One gap:** the `while True` loop in `events()` (line 142) has only one branch exercised — events then sentinel. The path where the consumer is cancelled mid-iteration (via an external `task.cancel()`) is not tested. Minor.

### 5.3 `engine/cost.py`

- `estimate_cost`: both `has_arbiter` branches covered.
- `estimate_cost_usd`: `model or PROVIDER_DEFAULT_MODELS.get(provider, fallback)` has three outcomes — explicit model (covered), provider default (covered), unknown provider fallback (covered at line 800). **All branches covered.**

### 5.4 `engine/_root.py`

`find_project_root` has 4 strategies. Tests cover:
- Strategy 1 (anchor walk-up) — `test_finds_root_via_anchor_walk_up`, `test_anchor_resolution_uses_custom_marker`.
- Strategy 2 (importlib.resources) — `test_importlib_resources_fallback_path` claims to cover this but the docstring admits "Simpler: just confirm that calling with marker='presets' and an anchor that definitely doesn't contain 'presets' still works because the package-resources strategy finds it." — This does NOT actually isolate strategy 2; it passes if any of strategies 2/3/4 succeed. **Real strategy-2 isolation gap.**
- Strategy 3 (engine package parent) — `test_finds_real_project_root_from_engine_package`, but again not isolated; strategy 1 is skipped only because no anchor is passed.
- Strategy 4 (cwd fallback) — `test_strategy_four_cwd_fallback` **correctly isolates** strategy 4 by using a unique marker.
- `raise FileNotFoundError` branch — covered by `test_raises_filenotfound_when_nothing_matches`.

**Branch-isolation gap**: strategies 2 and 3 are not independently exercised. If strategy 3 silently broke, the test pass/fail would depend on whether strategy 2 picks up the slack.

### 5.5 `engine/models.py` (`StructuredDeliberation.from_events`)

Critical path `rounds_completed == 0 → rounds_completed = 1` (line 137-138): covered by `test_rounds_completed_defaults_to_one_with_no_review_phases`. Good.

`synthesis_text.strip()` **false** path (empty/whitespace): covered by `test_empty_synthesis_leaves_headline_and_summary_empty` which passes `"   "`.

`synthesis_text.strip()` **true** path with `try/except (ValueError, Exception)` fallback at line 159: **not explicitly tested**. The except swallows errors from `parse_synthesis`. No test constructs a synthesis that makes `parse_synthesis` raise something other than `ValueError("empty")`. This except-block is effectively dead code in the current test suite.

Dispute bullet vs numbered: both covered.

Convergence numbered: covered. Convergence bullet: **not explicitly covered** — `test_parses_disputes_bullet_list` only covers the disputes section. The symmetric convergence path (bullet list under `### Common Ground`) is only tested via `test_parses_disputes_bullet_list` which uses `"- Everyone agrees on X"` + `"- **Shared goal**"`, asserting `len(convergence_points) == 2`. Acceptable.

Summary pluralization branches: `test_summary_singular_grammar` covers 1-agent grammar. Multi-agent and 0-agent paths are covered implicitly via other tests.

### 5.6 `engine/phases.py`

Excellent coverage with `_PhaseSelectiveProvider` exercising per-phase failure branches. Noteworthy gaps:

- **`test_cancel_before_start_raises`** only tests cancel-before. The cancel-between-phase tests (1133-1253) cover Phase 2-5 entry checks but **not** the cancel check inside the arbitration or cross-round-synthesis phases. If cancel is set during arbitration, does the pipeline propagate `CancelledError`?
- `prior_arbitration_path` branch at phases.py:661 is documented in `test_prior_arbitration_file_is_carried_through_retroactive_move` (line 1192) as **effectively dead code**. If it's dead, it should be removed, not documented in a test. This is a red flag — a test exists to "document current behavior" of unreachable code.
- `check_disagreement` output-driven convergence termination is tested. Stagnation is tested. But the interaction between `stagnation='detect'` and a dispute count that **decreases then increases** across rounds is not tested.

### 5.7 `engine/config.py`

- Constants tests cover `VALID_MODES`, `VALID_PROVIDERS`, `AGENT_NAME_RE`. Good.
- `_find_conversus_root` fallbacks: three strategies, all exercised including the all-fail case.
- `_load_preset_file` cache: covered.
- Composition templates (2, 3 presets) both covered; 4 rejected.
- **Gap**: `validate_templates` field has three states (true, false, default). All three covered. But `validate_templates: "true"` (string) — would it parse? Not tested. Also `validate_templates: 1` / `0` (int) — not tested.

### 5.8 `engine/templates.py`

Real templates covered via `TestRealTemplateRoundTrip`. Good.

**Gap**: `build_disputes_context` only tested for `iterations=1` and `iterations=3`, not `iterations=2`. Off-by-one risk in the `revision_N.md` naming logic.

### 5.9 `linter/validate.py`

- CLI exit codes 0, 1, 2 all tested via monkeypatch.
- `check_unknown_variables` suggestion path via difflib covered.
- **Gap**: `check_missing_required_variables` has a conditional involving `vd.modes` — `if not vd.modes or "cooperative" in vd.modes` (test line 256). The "vd.modes is not empty AND current mode not in modes" branch (i.e., a variable that's required in mode X but not mode Y) is not explicitly tested in isolation.

### 5.10 `linter/quality.py`

- All four fallback functions (`_fallback_cooperative`, `_fallback_red_blue`, `_fallback_prisoners_dilemma`, `_fallback_winner_take_all`) have at least a no-section test. Red-blue has a positive test; cooperative has an empty test but the positive path is exercised indirectly via `test_cooperative_fallback`. Prisoners-dilemma fallback positive path tested via `test_prisoners_dilemma_fallback`.
- `test_fallback_winner_take_all_empty_runner_up` is subtle — it asserts that an empty `## Runner-Up` section still produces a dispute entry labeled "Runner-Up". This documents a surprising behavior; good that it's pinned.
- **Gap**: `CONCESSION_AGENT` regex has many variants (`conceded`, `concedes`). Only the past-tense is tested.
- **Gap**: `_count_challenges` "Challenged By column" path and "inline cross-review" path are both tested, but the combined case (both present in the same text) is not.

### 5.11 `linter/question_classifier.py`

- `_has_decision_words` case insensitivity tested.
- `_has_alternatives` tested.
- `_has_constraints` — interesting: `test_plural_unit_misses_singular_word` documents the "3 months" miss as a known limitation. Good — this is exactly the "document current behavior" pattern done right (flagging a bug for later fix).
- `_is_factual` — starter-word exclusion via decision vocabulary tested.
- Rules 1, 2, 3, 4 all exercised.
- **Gap**: `classify_question` with `mode="interactive"` on a factual question asserts `"reframe" in result.clarification_question.lower()`. But the non-interactive factual path asserts `result.missing_fields is not None` without asserting which fields are listed. A regression that emptied `missing_fields` but left it as `[]` would still pass (line 148: `len(result.missing_fields) > 0`).

### 5.12 `linter/output_contract.py`

- `_extract_phases_completed` has three branches: explicit header with synthesis, explicit header without, inference from section structure. All covered.
- **Gap**: `_extract_headline` priority chain (convergence → spec-changes → synthesis title). Test `test_convergence_takes_priority` pins the precedence, good. But what if both convergence and spec-changes are present while synthesis title is absent? Not tested — the fall-through from spec-changes is only tested when convergence is missing.
- `test_surfaced_vs_surviving` is a great pin — asserts `surfaced = surviving + resolved` explicitly. Model test case.

---

## 6. TEST ISOLATION

### 6.1 Shared-state risks

| Location | Issue |
|---|---|
| `tests/test_engine_config.py:968-970, 1069-1070, 1143-1144, 1254-1255` | `engine_config_mod._preset_cache.clear()` in `setup_method`. This is necessary because the cache is module-level mutable state. **Isolation risk**: if a test in the same process runs BEFORE the setup method fires (e.g., a session-scoped fixture populates the cache), pollution is possible. The current arrangement is safe but brittle. Consider making `_preset_cache` per-function or injecting it. |
| `tests/test_engine_core.py:705-707` | `monkeypatch.chdir(fake_root)` — correctly uses pytest's monkeypatch which auto-restores. Good. |
| `tests/test_engine_config.py:913-923, 937-952` | `sys.modules["conversus.paths"] = None` with a `try/finally` to restore. **Works but fragile** — if an assertion inside the try raises an exception *other than* AssertionError, the finally correctly runs. Good. |
| `tests/test_engine_phases.py:600` | `monkeypatch.chdir(PROJECT_ROOT)` — `PROJECT_ROOT` is a module constant (`Path(__file__).resolve().parent.parent`). Portable across environments. Good. |
| `tests/test_linter_validate.py:60-73` | Session-scoped fixtures for `project_root`, `variables_schema`, `all_var_names`. These are read-only, no mutation. Good. |
| `tests/test_linter_quality.py:55-100` | Module-scoped `monorepo_text`, `red_blue_text` etc. fixtures. Read-only. Good. |

### 6.2 Environment-variable / filesystem leakage

- `tests/test_linter_usage.py` writes to `tmp_path / ".conversus" / "usage.jsonl"` — fully isolated to tmp.
- No test touches `os.environ` directly without `monkeypatch.setenv`.
- No test writes to `~/.conversus` or user HOME.

**Net**: isolation is generally strong, but `_preset_cache.clear()` is a module-state leak that should ideally be refactored rather than patched.

### 6.3 Order dependencies

I found no explicit order dependencies. All tests use `tmp_path`, `monkeypatch`, or read-only fixtures. **No findings.**

---

## 7. MOCKING

### 7.1 Appropriate mocking

- `tests/test_engine_phases.py:452-463` — `_FailingProvider`, `_PhaseSelectiveProvider`, `_CancelOnPhaseProvider` are **test-double providers** implementing the real `ModelProvider` protocol. This is the right pattern: mock the external LLM boundary, not the internals.
- `tests/test_linter_validate.py:561-566, 574-581, 588-611` — monkeypatches `linter.validate.find_project_root` and `linter.validate.validate_all` to force error paths into the CLI. Justifiable because it's the only way to exercise CLI exit codes 1 and 2 without corrupting real schema files.

### 7.2 Questionable mocking

| Location | Concern |
|---|---|
| `tests/test_engine_phases.py:1089` | `monkeypatch.setattr(phases_mod, "load_template", _bad_load)` — patches an internal module function to test the outer `except` clause at `engine/phases.py` around arbitration. This is **internal-API patching** — `load_template` is not an interface but an implementation detail of `phases.py`. If the arbitration path is refactored to inline template loading, the test will silently stop exercising the intended except branch. **Flag**: prefer constructing a real failing condition (e.g., pre-writing a draft template so `load_template` naturally raises). |
| `tests/test_engine_config.py:893` | `monkeypatch.setattr(engine_config_mod, "__file__", str(fake_engine))` — patches a dunder attribute to force strategy fallbacks. Also internal. The comment acknowledges "In the dev checkout strategy 1 always succeeds, so we have to monkey-patch the module's __file__ to force the fallbacks." This is necessary given the strategy design, but the brittleness should be documented in a comment inside the strategy-2 resolver itself. |
| `tests/test_engine_config.py:915-924` | `sys.modules["conversus.paths"] = None` — same concern as above. |

### 7.3 Over-mocking / under-mocking

- No pure function is mocked (good).
- `MockProvider` from `engine.providers` is the intended seam — used correctly throughout `test_engine_phases.py`.
- `tests/test_linter_usage.py` never mocks `secrets.token_hex` — instead asserts the hex property of the generated ID. This is **correct** (hash the generator output, not the generator).

---

## 8. TEST NAMING

### 8.1 Names that describe behavior (good examples)

- `test_config_error_maps_to_400` (`test_engine_core.py:105`) — subject + verb + expected outcome.
- `test_provider_error_auth_maps_to_401` — same pattern.
- `test_rounds_too_high_mentions_arbiter` — asserts a specific side-effect of an error (the message mentions arbiter).
- `test_skips_agent_completed_without_response_text` — behavioral, not structural.
- `test_cross_review_failure_counted` — clear signal.
- `test_arbiter_disputes_remain_skips_when_empty` — excellent.
- `test_cancel_after_review_aborts_before_cross_review` — pinpoint behavior.
- `test_red_blue_requires_red` — concise contract statement.

### 8.2 Names that are too generic

| Test | File:Line | Recommendation |
|---|---|---|
| `test_minimal` | `test_engine_templates.py:272, 325, 375, 402, 429` | Many test classes have a `test_minimal` — 5 occurrences. Rename to describe what is being verified, e.g., `test_builds_review_context_with_defaults`. |
| `test_defaults` | `test_engine_phases.py:262, 291` | Ambiguous — "defaults of what?". `test_pipeline_result_defaults_rounds_to_one` is better. |
| `test_frozen` | `test_engine_phases.py:274`, `test_linter_classifier.py:306`, etc. | OK in context but `test_pipeline_result_is_immutable` is clearer. |
| `test_minimal_valid_config` | `test_engine_config.py:77` | Better — "valid config". Retained. |
| `test_explicit_session_id` | `test_linter_usage.py:252` | Describes input, not behavior. `test_log_usage_uses_explicit_session_id_when_provided`. |
| `test_case_insensitive` | `test_linter_classifier.py:51` | Acceptable short form given the class scope. |
| `test_simple_factual_interactive` | `test_linter_classifier.py:131` | Describes input but not outcome. The test asserts `sufficient is False` and `clarification_question is not None`. `test_factual_question_in_interactive_mode_returns_insufficient_with_clarification`. |
| `test_red_blue_valid` | `test_engine_config.py:521` | Binary. Replace with `test_red_blue_requires_both_red_and_blue_roles`. |
| `test_empty` | `test_linter_quality.py:407, 436`, `test_linter_output_contract.py:173` | 3 occurrences. Not descriptive enough standalone; inside class context acceptable. |

### 8.3 Names that misdescribe

- `tests/test_engine_core.py:681` — `test_importlib_resources_fallback_path` promises strategy-2 coverage but the docstring admits it doesn't actually isolate strategy 2. **Rename** or **fix the test** so the name is truthful.
- `tests/test_engine_phases.py:1191` — `test_prior_arbitration_file_is_carried_through_retroactive_move` — the docstring says "the prior_arbitration_path branch is effectively dead code". If dead, the test name should include "regression" or the branch should be deleted. As-is the name suggests live coverage.

---

## 9. SOURCE-CODE FINDINGS SURFACED BY TESTS

These are bugs/smells I noticed in the source code while checking test coverage. Out of scope for the fp-guru's lens but within mine:

1. **`engine/phases.py:661` dead code** — confirmed dead by a test whose docstring admits it. Should be removed.
2. **`engine/_root.py` strategy-2 importability** — the `try: from conversus.paths import resolve_package_path` catch swallows both `ImportError` and `FileNotFoundError`, making it impossible to distinguish "conversus is not installed" from "the resource path is wrong." Consider narrowing.
3. **`engine/errors.py:59`** — `category = getattr(exc, "category", "unknown")` sets a sentinel string that then never matches any `if` branch, falling through to 502. If `ProviderError` ever gains a `category=None` default instead of a required field, this string-equality check silently hides the misconfiguration.
4. **`linter/quality.py:CONCESSION_AGENT`** regex supports `conceded` and `concedes` but tests only cover one. If the regex is restricted to past tense later, nothing catches it.
5. **`engine/models.py:159`** — `except (ValueError, Exception)` is redundant (`Exception` is a superset of `ValueError`). Style nit, not a bug, but signals lack of thought about the specific exception surface of `parse_synthesis`.

---

## 10. SUMMARY — ORDERED FINDINGS BY SEVERITY

### P0 — Correctness-impacting gaps

1. **`with pytest.raises(Exception)` occurrences** (section 1.2) — 6 locations. Replace with `pytest.raises(ValidationError, match=...)`. Zero-cost, prevents false-positive passes.
2. **Empty `events=[]` not tested in `StructuredDeliberation.from_events`** (section 2.1). Critical happy-path.
3. **`engine/_root.py` strategies 2 and 3 not isolated** (section 5.4). A broken strategy 3 would silently be masked by strategy 2 and vice versa.
4. **`models.py:159` except branch is untested** (section 5.5). Dead-until-proven-reachable.
5. **`engine/phases.py:661` prior_arbitration_path branch** (section 5.6) — test documents it as dead. Either delete the code or write a test that exercises it legitimately.

### P1 — Weak assertions that should be tightened

6. Replace `>=` / `>` truthy checks on deterministic fixtures with exact values (section 1.1).
7. Add `match=` substring to all `pytest.raises` for Pydantic `ValidationError` and `FileNotFoundError` (section 3.1).
8. Parametrize `test_agent_name_regex_valid` / `_invalid` (section 4.1).
9. Parametrize `test_provider_model_options_entries_have_required_keys` and `test_model_pricing_has_input_and_output_for_every_entry` so individual rows report individually (section 4.1).

### P2 — Missing edge-case coverage

10. Negative / zero / unicode / empty-list edge cases across cost, config, events, and question_classifier (section 2.1).
11. Strategy-2 isolation in `find_project_root` (section 5.4) — needs a test that forces the real importlib.resources branch independently of strategies 1/3/4.
12. `CONCESSION_AGENT` `concedes` variant (section 5.10).
13. `_extract_headline` fall-through from spec-changes when synthesis title is absent (section 5.12).
14. `build_disputes_context` iteration=2 off-by-one in revision naming (section 5.8).
15. `_preset_cache` per-function injection vs global clear (section 6.1).

### P3 — Naming & hygiene

16. Rename `test_minimal`, `test_defaults`, `test_frozen`, `test_empty`, `test_simple_factual_interactive` to behavior-describing names (section 8.2).
17. Fix `test_importlib_resources_fallback_path` so the name and behavior agree (section 8.3).
18. Decide whether `test_prior_arbitration_file_is_carried_through_retroactive_move` documents live code or dead code (section 8.3).
19. Replace internal monkey-patching (`load_template`, `__file__`) with real failure constructions where possible (section 7.2).

---

## 11. POSITIVE PATTERNS WORTH PROPAGATING

These patterns in the existing suite should be mirrored in any new tests:

- **Phase-selective provider pattern** (`tests/test_engine_phases.py:616-663`) — a single test double with a phase marker detector lets one class cover every failure branch. Excellent reuse.
- **Regex-matched raises** — `pytest.raises(PipelineError, match=r"Phase 3 \(revision")` (line 704).
- **Parametrized mode coverage** — `@pytest.mark.parametrize("mode", ALL_MODES)` in `test_linter_validate.py:373`.
- **Roundtrip equality assertions** — `WebError(**dumped) == err` (line 95), `StructuredDeliberation(**dumped) == d` (line 391). These pin the full serialization contract.
- **Pinning known limitations as tests** — `test_plural_unit_misses_singular_word` (`test_linter_classifier.py:84-88`) documents a heuristic miss as a test so it's discoverable when fixed.
- **Real fixture files** — `quality-floor/reference-outputs/` loaded via `pytest.skip` if missing, reused across `test_linter_quality.py` and `test_linter_output_contract.py`. The skip guard keeps the suite robust to fixture-directory drift.

---

## 12. ITEMS FOR CROSS-REVIEW WITH FP-GURU

I flagged these for deliberate discussion in Round 2 — the fp-guru's functional-programming lens may disagree or extend:

1. **`_preset_cache` as module state** (section 6.1). FP lens would likely argue for pure injection; I'm agnostic on the refactor priority but note the test brittleness.
2. **Monkey-patching `load_template`** (section 7.2). The alternative is to construct real failing inputs. FP lens may prefer dependency injection at the `run_pipeline` level so the test doesn't need the monkeypatch at all.
3. **Parametrization of `MODEL_PRICING` table tests** (section 4.1) — I recommend per-row parametrization for reporting; fp-guru may point out that this is a table-driven property test and suggest `hypothesis` instead of parametrize.
4. **`_extract_remaining_disputes` heading regex proliferation** — the source and tests both show a large OR-chain of headings. fp-guru may have views on unifying via a data-driven pattern table instead of regex branches.
5. **Except-branch in `models.py:159`** — is this a functional-style "best-effort" parser, or dead code? The FP lens may have an opinion on whether swallowing `Exception` is acceptable here.

---

**End of SDET review (Round 1).**
