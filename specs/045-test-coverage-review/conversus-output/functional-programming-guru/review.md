# Functional Programming & Type Systems Review — Conversus Test Suite

**Reviewer:** functional-programming-guru
**Round:** 1 of 2 (cooperative deliberation with sdet-agent)
**Scope:** Engine + linter test files and their source modules
**Date:** 2026-04-03

---

## Executive Summary

The test suite has a solid foundation — frozen Pydantic models, mostly pure check functions in the linter, event emitters built from a Protocol. But the type safety story degrades sharply once you cross into the engine layer: `str` fields where `Literal[...]` belongs, `dict` return types that force every caller to re-narrow, global mutable module state that silently couples tests, and pervasive I/O coupling in "unit" tests that run a full async pipeline through `tmp_path`. The linter files (`question_classifier.py`, `quality.py`, `output_contract.py`) are the strongest; `engine/config.py`, `engine/cost.py`, and `engine/phases.py` have the most room to tighten types.

Below I walk each of the six review dimensions with specific file:line citations.

---

## 1. Purity: tests testing pure functions vs. I/O-coupled tests

### Good: genuinely pure tests

These are the examples to emulate:

- **`tests/test_engine_core.py:64-146`** — `TestWebErrorModel`, `TestMapEngineError`. `map_engine_error()` is a referentially transparent function from `Exception → WebError`; every test constructs input in-memory and asserts on the returned model. No fixture coupling, no tmp_path.
- **`tests/test_engine_core.py:154-310`** — all event emitter tests. Construction + `emit()` assertions against an in-memory list. `AsyncQueueEmitter` tests (`:263-310`) are the cleanest async test pattern in the suite.
- **`tests/test_engine_core.py:715-835`** — `TestEstimateCostFormula` and `TestEstimateCostUsd`. `estimate_cost()` is a pure function of three scalars, and the test at `:818-822` explicitly verifies the linearity law: `cost(2x tokens) ≈ 2 × cost(x tokens)`. This is exactly the kind of algebraic-property assertion that pure functions enable.
- **`tests/test_linter_quality.py:108-313`** — every `TestExtract*` / `TestFallback*` / `TestCount*` class tests a pure function with a string input and primitive output.
- **`tests/test_linter_classifier.py:32-121`** — `TestHasDecisionWords`, `TestHasAlternatives`, `TestHasConstraints`, `TestIsFactual`. These are straight `str → bool` tests.
- **`tests/test_linter_output_contract.py:56-260`** — all extraction helpers tested as pure text→value functions.

### Bad: tests dressed as unit tests but really running integration

- **`tests/test_engine_phases.py:305-421`** (`TestRunPipelineCooperative`) — every test here calls `asyncio.run(run_pipeline(...))`, which writes to disk, loads real template files from `PROJECT_ROOT / "conversus.example.yml"`, and exercises a 5-phase orchestrator with a mock provider. These are **end-to-end tests**, not unit tests. The fact that `_assemble_phase_prompt` at `phases.py:90-131` *is* a pure function, and has its own pure tests at `test_engine_phases.py:114-214`, is correct — but then there's no unit-level test for `_run_single_round` in isolation; it's only exercised through the full pipeline.
- **`tests/test_engine_phases.py:1020-1150`** — the arbitration-failure tests pre-seed files on disk, monkey-patch `phases_mod.load_template`, run the full pipeline, and then re-read the filesystem. The test logic is sound, but every assertion is gated on filesystem side effects. There's no way to test the "outer except clause unlinks the file" branch without this coupling because the unlink is a method of the pipeline orchestrator.
  - **Functional remedy:** extract the branch logic into a pure helper — e.g., `_arbitration_result_to_action(success, stale_exists) -> Literal["keep", "unlink", "noop"]` — and test the pure helper separately from the filesystem effect.
- **`tests/test_engine_config.py:78-84`** (`test_minimal_valid_config`) — every `parse_config()` test writes YAML to disk and reads it back. `parse_config()`'s signature is `Path → EngineConfig`, so there's no way around some disk touch — but a `parse_config_from_mapping(data: dict, base_path: Path)` factored out of the current monolithic `parse_config()` would move 90% of the tests into pure territory. As currently written, `parse_config()` at `engine/config.py:495-659` mixes *parsing the file* with *validating the structure* — two separable concerns.
- **`tests/test_engine_templates.py:619-647`** (`TestRealTemplateRoundTrip`) — reads actual shipped templates from `PROJECT_ROOT / "templates"`. These are smoke tests, not unit tests; they will fail if anyone edits a shipped template. Not wrong, but should be marked `@pytest.mark.integration` and not counted as "template module coverage".
- **`tests/test_linter_validate.py:372-423`** (`TestValidateTemplate.test_real_templates_are_clean`) — same issue. Parametrized over every mode, runs validation against every shipped template. The same structural information (`"every mode's templates lint cleanly"`) belongs in one integration test, not eight.
- **`tests/test_linter_usage.py:156-319`** — every `log_usage` test writes a JSONL file to `tmp_path`. The function signature at `linter/usage.py:161-247` *forces* this because `log_usage` both constructs a `UsageEntry` and appends it to disk. The two concerns should be split: `build_usage_entry(...) -> UsageEntry` (pure) + `append_entry(entry, path)` (effectful). Then 10 of the 12 tests in the file could be pure.

### Ugly: tests that depend on real project layout

These will break in CI if someone renames a directory, and they pollute unit-test execution time with filesystem walks:

- **`tests/test_engine_core.py:635-640`** (`test_finds_real_project_root_from_engine_package`) — calls `find_project_root()` with no anchor and asserts `(root / "presets").is_dir()`. Hardcoded to the dev checkout layout. The test at `:664-670` is worse: it calls `find_project_root(anchor=tmp_path)` and still expects the *real* project root, because the function falls through to strategy 3. The test is correct about what the code does; the code just has too many "oh fine, let me guess" fallback strategies. See §5 below.
- **`tests/test_linter_validate.py:60-72`** — `project_root` fixture is `scope="session"` and calls `find_project_root()`. Every test that depends on it is implicitly coupled to the real project layout.

---

## 2. Pydantic model tests: field constraints + type coercion

Pydantic tests are uneven. Some hit both dimensions, others only check "happy path construction works".

### Covered well

- **`tests/test_engine_core.py:97-99`** — `test_missing_required_field_raises` for `WebError`. Correct: asserts `ValidationError`.
- **`tests/test_engine_core.py:207-209`** — asserts `PhaseStarted(phase="review", agent_count="three", ...)` raises. This is the correct level of paranoia.
- **`tests/test_engine_core.py:184-194`** — `test_agent_completed_frozen` asserts immutability. Good.
- **`tests/test_engine_core.py:335-342`** — `test_phase_result_invalid_data_raises` passes `duration_ms="lots"`. Correct coercion-failure test.
- **`tests/test_engine_config.py:852-870`** — `test_agent_config_frozen` / `test_engine_config_frozen`.

### Gaps

- **`tests/test_engine_core.py:393-399`** (`StructuredDeliberation.test_missing_required_field_raises`) — good, but there is **no test** for "passing a `str` where `list[AgentReview]` is expected" or "passing `None` where `rounds_completed: int` is required". Pydantic will coerce some of these silently (e.g., it'll accept `"5"` as `rounds_completed=5`). The model has 12 fields; the test covers exactly one failure case.
- **`engine/models.py:25-74`** — none of the frozen models have field validators. `phase: str`, `mode: str`, `provider: str`, `category: str`, `termination_reason: str | None` — all unconstrained strings where a `Literal[...]` would catch typos at construction time. See §5.
- **`tests/test_engine_config.py:851-870`** (`TestPydanticModels`) — tests frozen-ness with `pytest.raises(Exception)` (line 854, 869). **This is too loose.** `Exception` catches `AttributeError`, `TypeError`, `ValueError`, and `ValidationError` indiscriminately. Should be `pytest.raises(ValidationError)`. The same broad-exception pattern appears at `test_engine_phases.py:282` (`pytest.raises(Exception): result.phases_completed = 99`), `test_linter_classifier.py:313`, and `test_linter_output_contract.py:356, 389`.
- **`tests/test_linter_quality.py`** — **zero tests** assert that `DisputeInfo`, `DisagreementResult`, `AttributionResult`, or `QualityResult` are frozen or reject bad types. These are Pydantic models with `model_config = {"frozen": True}` (at `linter/quality.py:46, 55, 65, 77`), but only their "happy path" factory behavior (constructed inside `check_*` functions) is tested.
- **`tests/test_linter_usage.py`** — `UsageEntry`, `AdoptionMetrics`, `SynthesisMeta` have `model_config = {"frozen": True}` at `linter/usage.py:52, 74, 92`. No test verifies the frozen constraint. No test verifies that passing a negative `dispute_count` or a non-`bool` `quality_passed` raises.
- **`tests/test_linter_validate.py:505-524`** (`TestValidationResult`) — tests the `.passed` property branch but does not test that `errors` rejects non-`LintError` items or that `files_checked=-1` is either accepted (bug) or rejected.

### Pattern to adopt

The `test_payoffs.py` reference (`tests/test_payoffs.py:30-80`) shows the right pattern: fixtures build full `RoundFeatures` models with real numbers, and the tests exercise algebraic properties of the payoff functions. The engine/linter tests should follow: build fixtures once, use them to test *both* field-constraint failures *and* the business logic that consumes them.

---

## 3. Fixture composability

### Good

- **`tests/test_linter_validate.py:60-84`** — `project_root`, `variables_schema`, `all_var_names` fixtures are `scope="session"`, depend on each other via pytest fixture injection, and are read-only. These are fully composable.
- **`tests/test_linter_quality.py:56-101`** — reference-output fixtures with `scope="module"` and `pytest.skip` when missing. Composable, idempotent.
- **`tests/test_linter_usage.py:36-83`** — `question_file`, `synthesis_file`, `quality_json_passing`, `quality_json_failing`, `usage_file` are per-test-function fixtures that build inputs without sharing state. Composable.
- **`tests/test_payoffs.py:32-80`** (reference example) — `negotiation_features`, `resource_allocation_features` are pure data constructors returning frozen models. Perfect composability.

### Bad

- **`tests/test_engine_phases.py:62-106`** — `_make_config()` is a module-level helper, not a pytest fixture. It takes `tmp_path` as a positional arg and creates files on disk as a side effect. This cannot be composed across test files — if `test_engine_templates.py` wants the same config builder it has to duplicate the function (and indeed it does: see `test_engine_templates.py:52-85`, which is a near-copy with the `prior_files` parameter dropped). Two copies of the same "minimal engine config" factory is a code smell.
  - **Fix:** move `_make_config` into `tests/conftest.py` as a `@pytest.fixture` that returns a `Callable[..., EngineConfig]`, so both files can share one definition.
- **`tests/test_engine_config.py:38-68`** — `_write_yaml`, `_make_target`, `_minimal_config_dict`, `_write_minimal` are module-private functions, not fixtures. They work only because every test in the file accepts `tmp_path`. Not reusable across files.
- **`tests/test_engine_config.py:968-970`** — `TestLoadPresetFile.setup_method` calls `engine_config_mod._preset_cache.clear()`. This is mutable **module-global state** leaking into the test class. Same pattern repeats at `:1069-1070` and `:1143-1144`. See §4.

### Coupling smell

The `_example_config_path()` helper at `test_engine_phases.py:57-59` returns `PROJECT_ROOT / "conversus.example.yml"` — every pipeline test depends on a file in the repo root. If that file is renamed, ~30 tests break. This should be a fixture that copies or generates the minimum viable example, not a hardcoded path.

---

## 4. Order-independence

### Violations — mutable module state

- **`engine/config.py:214`** — `_preset_cache: dict[Path, dict[str, Any]] = {}` is a module-level mutable dict. `parse_config()` clears it (`:513`), but `_load_preset_file()` is tested directly at `test_engine_config.py:972-989` **and** the test mutates disk to verify cache semantics:
  ```python
  first = _load_preset_file(preset)
  preset.write_text("bogus: yaml\n")  # mutate disk
  second = _load_preset_file(preset)
  assert first is second
  ```
  This only works because `setup_method` (`:968-970`) clears the cache. If pytest runs `TestResolveSinglePreset` before `TestLoadPresetFile` in the same session **without** cache clearing (e.g., if someone removes the `setup_method`), the second call might return stale data from a different test. The fact that three separate `setup_method` definitions exist (`:968, :1069, :1143`) to defend against this is evidence that the global cache is the wrong design.
  - **Fix:** thread the cache through as a parameter: `_load_preset_file(path, cache: dict[Path, dict]) -> dict`. Now every test supplies its own fresh cache and there is no cross-test coupling.

### Violations — cwd mutation

- **`tests/test_engine_core.py:697-707`** (`test_strategy_four_cwd_fallback`) — uses `monkeypatch.chdir(fake_root)`. Pytest's `monkeypatch` correctly reverts this, but the test documents that `find_project_root()` reads `Path.cwd()` as a fallback (`engine/_root.py:67-69`), and **any** test that runs after this one in the same process sees whatever cwd pytest restored — which is fine for this case but creates a "don't forget to monkeypatch" footgun.
- **`tests/test_engine_config.py:927-953`** (`test_cwd_fallback_succeeds_when_cwd_has_schema_and_templates`) — monkey-patches `sys.modules["conversus.paths"] = None` and then restores in a `try/finally`. Correct, but **brittle**: if the `finally` block has a bug or the test itself raises between the mutation and the `try`, the entire session's `conversus.paths` import is broken for every subsequent test.
- **`tests/test_engine_phases.py:591-608`** (`test_config_path_none_uses_cwd`) — uses `monkeypatch.chdir(PROJECT_ROOT)`. Same category.
- **`tests/test_engine_templates.py:44`** — `PROJECT_ROOT = Path(__file__).resolve().parent.parent` at module level. Not a mutation risk, but the `TestFindTemplatesDir.test_falls_back_to_engine_parent` test at `:122-133` asserts `assert (found / "cooperative" / "review.md").exists()`, which couples the test to the real templates directory.

### Violations — test-method setup_method

The `setup_method` usage at `test_engine_config.py:968, 1069, 1143, 1254` is not a pytest anti-pattern per se, but it's a strong signal that the code under test has hidden state. Each call to `_preset_cache.clear()` is admitting: "my function is not pure, and I need to reset it between tests".

### Order-independent, good

- All tests in `test_linter_classifier.py` — pure functions, no fixtures with side effects.
- All tests in `test_linter_output_contract.py` — module-scoped text fixtures that are immutable strings.
- `test_linter_quality.py` — reference-output strings loaded once per module, never mutated.

---

## 5. Types in code under test

This is the area with the most room for improvement. Findings, specific and cited:

### 5a. String enums where `Literal[...]` belongs

- **`engine/config.py:67`** — `mode: str` on `EngineConfig`. Every consumer of this field has to trust that it's one of the values in `VALID_MODES`, but Pydantic only checks at *parse* time in `parse_config` (line 534), not at *model* construction. If you construct `EngineConfig(mode="zebra", ...)` directly, you get a valid object. Should be:
  ```python
  mode: Literal[
      "cooperative", "winner-take-all", "prisoners-dilemma", "red-blue",
      "negotiation", "resource-allocation", "fair-division", "mechanism-design",
  ]
  ```
  Even better: reuse `VALID_MODES` from `conversus/schemas/modes.py` and derive the `Literal` programmatically, or use a `StrEnum` (the `linter/models.py:77-89` `Phase` enum is the pattern to copy).
- **`engine/config.py:73`** — `stagnation: str = "detect"`. Only valid values per the parser (line 578) are `"detect"` or `"ignore"`. Should be `Literal["detect", "ignore"]`.
- **`engine/config.py:77`** — `provider: str = "anthropic"`. `VALID_PROVIDERS` is declared at line 59 as a tuple. Should be `Literal["anthropic", "openai"]`.
- **`engine/events.py:28, 39, 50, 63`** — every event has `phase: str`. The valid phase names are enumerated in `linter.models.Phase` (`linter/models.py:77-89`). The engine already imports from linter (`engine/templates.py:23-33`); it should import `Phase` here too and use `phase: Phase` (or `phase: Literal[...]`). Right now `PhaseStarted(phase="revieww", ...)` constructs successfully and only explodes downstream when someone tries to match on it.
- **`engine/models.py:30, 41, 62, 63`** — `phase: str`, `mode: str`, `provider: str`. Same fix.
- **`engine/phases.py:70`** — `termination_reason: str | None = None  # "converged", "stagnation", "max_rounds"`. The inline comment is doing the work of a type. Should be `Literal["converged", "stagnation", "max_rounds"] | None`.
- **`engine/errors.py:28`** — `category: str` on `WebError`. Per the docstring and the mapping function (`:52-104`), the valid values are `"config_error" | "pipeline_error" | "auth_error" | "rate_limit" | "provider_error" | "validation_error" | "internal_error"`. Should be `Literal[...]`.

### 5b. Weak return types — `dict` where a TypedDict/model belongs

- **`engine/cost.py:70-103`** — `estimate_cost(...) -> dict[str, int]`. The returned dict has a fixed shape: `review`, `cross_review`, `revision`, `disputes`, `synthesis` always present, `arbitration` conditionally. This is exactly what a `TypedDict` with `NotRequired` is for:
  ```python
  class PhaseCounts(TypedDict):
      review: int
      cross_review: int
      revision: int
      disputes: int
      synthesis: int
      arbitration: NotRequired[int]
  ```
  Better: a frozen Pydantic model with `arbitration: int | None = None`. The test at `test_engine_core.py:731-738` has to assert `"arbitration" not in phases` — an assertion that would be statically eliminable with the right type.
- **`engine/cost.py:106-158`** — `estimate_cost_usd(...) -> dict`. No type parameter at all! The return value has 7 fixed keys. The test at `test_engine_core.py:770-778` dereferences them all blind. This should be a Pydantic model:
  ```python
  class CostEstimate(BaseModel):
      phases: PhaseCounts
      total_launches: int
      model: str
      estimated_usd: float
      low_estimate_usd: float
      high_estimate_usd: float
      pricing_per_1m_tokens: dict[str, float]
  ```
- **`engine/cost.py:38`** — `PROVIDER_MODEL_OPTIONS: dict[str, list[dict[str, str | float]]]`. The inner `dict[str, str | float]` has four fixed keys (`id`, `name`, `tier`, `description`) all of which are strings. The test at `test_engine_core.py:845-852` iterates every entry and asserts each of the four keys exists — which is the test suite hand-rolling what a `TypedDict` would give for free. Furthermore, `tier` is always one of `"default" | "premium" | "budget"` — another lost `Literal`.
- **`engine/config.py:214`** — `_preset_cache: dict[Path, dict[str, Any]]`. The inner `dict[str, Any]` is actually a preset file: name, category, description, prompt, optional docs, optional composable. Should be a `PresetData(BaseModel)`. The current signature invites `.get("name")` / `.get("prompt")` everywhere (`:232-247`, `:317-318`, `:329`, `:338-351`, `:358`), forcing every caller to re-narrow.
- **`engine/config.py:366`** — `_resolve_agent(raw: dict[str, Any], ...)`. The `raw` dict is a parsed YAML agent entry with known fields (`name`, `prompt`, `preset`, `docs`, `role`). Instead of `.get()` everywhere, a `RawAgentInput(BaseModel)` would make the schema explicit and catch typos at parse time.
- **`engine/config.py:417`** — `_resolve_arbiter(raw: dict[str, Any], ...)`. Same as above for the arbiter shape.
- **`linter/usage.py:164`** — `log_usage(..., quality_json: dict | str, ...)`. The `dict` could be a `QualityReport(BaseModel)` with typed subfields (`disagreement.passed`, `disagreement.dispute_count`, `attributions.passed`). The current implementation at `:204-211` does `.get("passed", False)` / `.get("dispute_count", 0)` which silently defaults on schema drift.
- **`linter/usage.py:261`** — `entries: list[dict] = []`. Every line loaded from the JSONL. Then at `:298-315` every aggregation does `.get("quality_passed")` / `.get("session_id", "")`. A `UsageEntry.model_validate_json(line)` would give typed access and catch corruption earlier than the "corrupt_lines" counter. (The existing `UsageEntry` model at `:49-68` *is* the right shape; it's just not used on the read path.)

### 5c. Missing type hints

- **`engine/phases.py:218`** — `round_kw: dict = dict(...)`. Untyped dict. Should be a `TypedDict` or just keyword arguments.
- **`linter/quality.py:421`** — `_FALLBACK_DISPATCH: dict[str, object] = {...}`. The values are all `Callable[[str], list[DisputeInfo]]`. The `object` type is a workaround because the functions have the same signature but mypy sees them as different types. The `# type: ignore[operator]` at `:471` is evidence — a proper `Callable` type annotation would eliminate it. Should be:
  ```python
  FallbackFn = Callable[[str], list[DisputeInfo]]
  _FALLBACK_DISPATCH: dict[str, FallbackFn] = {...}
  ```
- **`engine/phases.py:461-463`** (`_FailingProvider` in tests) — `async def stream(self, prompt, model, max_tokens):  # type: ignore[no-untyped-def]`. The `# type: ignore` is covering up a missing return type. Should be `AsyncIterator[str]`.
- **`engine/phases.py:655`** (`_PhaseSelectiveProvider.stream`) — same `# type: ignore[no-untyped-def]`.
- **`engine/phases.py:781`** (`_CancelOnPhaseProvider.stream`) — same.
- **`linter/validate.py:135, 149`** — `raw: dict = yaml.safe_load(f)`. Bare `dict`. Should at least be `dict[str, Any]`, though ideally validated into a typed intermediate model.

### 5d. Unions where discriminated unions belong

- **`engine/events.py:75`** — `EngineEvent = Union[PhaseStarted, AgentDispatched, AgentCompleted, PhaseCompleted]`. This is used everywhere with `isinstance()` checks (e.g., `engine/models.py:107, 120, 150`, `tests/test_engine_core.py:443-450`). A **discriminated union** via a `type: Literal[...]` discriminator field would let Pydantic dispatch on the type string and let consumers pattern-match without `isinstance`:
  ```python
  class PhaseStarted(BaseModel):
      type: Literal["phase_started"] = "phase_started"
      phase: Phase
      ...
  # and then:
  EngineEvent = Annotated[
      Union[PhaseStarted, AgentDispatched, AgentCompleted, PhaseCompleted],
      Field(discriminator="type"),
  ]
  ```
  The test at `test_engine_core.py:455-474` is filtering by `isinstance(ev, AgentCompleted) and ev.response_text`. With a discriminator, that's `ev.type == "agent_completed" and ev.response_text` — which mypy can narrow through.

### 5e. `dict | str` union on the boundary

- **`linter/usage.py:164`** — `quality_json: dict | str`. The union exists because the function accepts either a dict *or* a JSON string and calls `json.loads()` internally. Functionally this is two functions glued together. Better: make the caller parse (`log_usage(..., quality: QualityReport)`) and provide a `log_usage_from_json_string(...)` helper for the CLI entry point. The current test at `test_linter_usage.py:215-230` literally tests both branches, which is only necessary because the function accepts both types.

### 5f. Protocol types on arguments — good, but under-used

- **`engine/events.py:82-91`** — `EventEmitter(Protocol)` is the right pattern. Used correctly in `phases.py`.
- **`engine/providers`** — `ModelProvider` is used as a parameter annotation in `engine/phases.py:193, 575`. But the test provider classes `_FailingProvider`, `_PhaseSelectiveProvider`, `_CancelOnPhaseProvider` at `test_engine_phases.py:451, 616, 760` don't declare that they conform to the protocol. If `ModelProvider` were a runtime-checkable Protocol, the tests could assert `isinstance(_FailingProvider(), ModelProvider)` to verify structural conformance. As written, these test classes work only because Python's duck typing doesn't care; a type checker would accept them but wouldn't verify the async generator signature.

---

## 6. Type-information leverage in code under test

Places where the code could use types to eliminate runtime checks:

### 6a. `isinstance` chains that should be discriminated unions

- **`engine/errors.py:51-104`** — `map_engine_error()` is a textbook candidate for pattern matching on a discriminated exception type. The current isinstance-chain works, but:
  ```python
  if isinstance(exc, ProviderError):
      category = getattr(exc, "category", "unknown")  # line 59
  ```
  The `getattr(..., "unknown")` fallback exists because `ProviderError.category` is not typed on the class. If `ProviderError.category: Literal["auth", "rate_limit", "server"]` were declared, the `getattr` becomes `exc.category` and the "mystery" fallback branch at `:79-83` (tested at `test_engine_core.py:131-135`) becomes **unreachable code** — which is a win, because unreachable fallback code is a bug farm.
- **`engine/models.py:106-128`** — two separate loops over `events`, one filtering for `AgentCompleted`, one for `PhaseCompleted`. With a discriminated union this could be a single pass with `match` or a dict-based dispatcher.

### 6b. Functions returning `None` where `Result[T, Err]` belongs

- **`engine/templates.py:524-543`** — `_extract_section_text(text, heading_pattern) -> str | None`. Every caller has to `if section is not None` guard. An `Optional` return is fine, but the tests at `test_engine_templates.py:598-607` cover both branches — the `None` branch is meaningful. A `Result` type would at least document that absence is expected, not an error.
- **`engine/templates.py:546-574`** — `_extract_remaining_disputes` returns `""` on failure. There's no way for a caller to distinguish "found the section, it was empty" from "no section found". Should return `str | None` or use a discriminated result.
- **`linter/quality.py:181-195`** — `_extract_dispute_block(text) -> str | None`. Same category; at least this one is honest about absence via `Optional`.

### 6c. Generics that would eliminate duplication

- **`engine/templates.py:218-499`** — seven `build_*_context` functions that all take `config`, `output_dir`, and kwargs and return a context subclass. They share the round-kwargs boilerplate (`round`, `prior_synthesis_path`, `prior_round_dir`, `prior_arbitration_path`). This is crying out for:
  ```python
  class RoundContext(BaseModel):
      round: int = 1
      prior_synthesis_path: str | None = None
      prior_round_dir: str | None = None
      prior_arbitration_path: Path | None = None
  ```
  Then each `build_*_context` takes `round_context: RoundContext` and doesn't have to list the four fields seven times. The test at `test_engine_templates.py:298-310` works because all seven functions accept the same parameters — the duplication is load-bearing, not ergonomic.

### 6d. `Any` leakage

- **`engine/config.py:214, 217, 256, 306, 326, 367, 418`** — `dict[str, Any]` on every preset/agent/arbiter raw input. Once the raw YAML is parsed, it should be validated into a typed model immediately. The current "validate field by field with `.get()`" pattern at `:232-250` is brittle:
  ```python
  expected_name = path.stem
  if data.get("name") != expected_name:
      raise ConfigError(...)
  ```
  becomes, with a model:
  ```python
  raw = PresetFile.model_validate(yaml.safe_load(f))
  if raw.name != path.stem:
      raise ConfigError(...)
  ```
  The Pydantic model catches type errors (name must be string) for free; the dict version hand-rolls each check.

### 6e. `TypedDict` candidates I already cited above — bundled here for reference

| Location | Current | Should be |
|---|---|---|
| `engine/cost.py:70` | `dict[str, int]` | `PhaseCounts(TypedDict)` |
| `engine/cost.py:106` | `dict` (no param!) | `CostEstimate(BaseModel)` |
| `engine/cost.py:38` | `dict[str, list[dict[str, str \| float]]]` | `dict[str, list[ModelOption]]` with `ModelOption(BaseModel)` |
| `engine/phases.py:218` | `dict` | `TypedDict` or explicit kwargs |

---

## 7. Minor nits

- **`tests/test_engine_core.py:184-194`** — `test_agent_completed_frozen` uses `# type: ignore[misc]` on the mutation line. This is correct pytest-for-pydantic idiom, but the test itself could be tightened by asserting the specific error message contains "frozen" to catch regressions where the field becomes mutable but raises a different error.
- **`tests/test_engine_phases.py:54`** — `PROJECT_ROOT = Path(__file__).resolve().parent.parent`. Module-level constant computed at import time. If pytest is launched from a symlinked directory, this might resolve unexpectedly. Minor, but should be a session fixture.
- **`linter/quality.py:471`** — `fallback_fn(synthesis_text)  # type: ignore[operator]`. The `type: ignore` is hiding the typing issue I described in §5c. Fixing `_FALLBACK_DISPATCH` to `dict[str, FallbackFn]` removes the ignore.
- **`engine/phases.py:852`** — returns `PipelineResult(output_dir=output_mgr._root_dir, ...)` accessing a private attribute of `output_mgr`. Breaking encapsulation. Not a test issue per se but a typing smell — there should be an `output_mgr.root_dir` public accessor.
- **`tests/test_linter_classifier.py:313`** — `with pytest.raises(Exception):` on line 313 is too broad. Should be `ValidationError`.

---

## 8. Prioritized recommendations

Ranked by what will most improve type safety / purity per unit of effort:

1. **Convert `mode`, `stagnation`, `provider`, `phase`, `termination_reason` to `Literal` or `StrEnum`** across `engine/config.py`, `engine/events.py`, `engine/models.py`, `engine/phases.py`. High impact, mechanical change. Removes a whole class of "typo bug that only fires in production" defects.
2. **Replace `engine.cost` dict returns with Pydantic models.** Immediate win for `estimate_cost_usd()` which currently has `-> dict` with no type parameter at all.
3. **Add `PresetFile(BaseModel)` to `engine/config.py`** and stop calling `.get("name")` on raw dicts. Eliminates 7 `dict[str, Any]` annotations and removes the hand-rolled field-presence checks at `_load_preset_file`.
4. **Split `log_usage()` into pure `build_usage_entry()` + effectful `append_usage_entry()`.** Converts 10 of 12 tests in `test_linter_usage.py` from filesystem-coupled to pure.
5. **Promote `_make_config` and `_write_yaml` to `tests/conftest.py` fixtures.** Eliminates the duplication between `test_engine_phases.py` and `test_engine_templates.py`.
6. **Thread `_preset_cache` through as a parameter** instead of module state. Eliminates three `setup_method` definitions and makes preset tests fully order-independent.
7. **Tighten `pytest.raises(Exception)` to `pytest.raises(ValidationError)`** at the 5 sites I cited. Cheap fix that catches regressions where the wrong error is raised.
8. **Add a discriminator field to `EngineEvent`.** Enables Pydantic discriminated-union parsing and removes `isinstance` chains in `engine/models.py:from_events`.
9. **Add missing Pydantic field-rejection tests** for `StructuredDeliberation`, `PipelineResult`, `UsageEntry`, `DisputeInfo`. Every frozen model should have (a) frozen test, (b) required-field test, (c) type-coercion-failure test — three tests, one per model. Currently only `WebError` has all three.
10. **Introduce `RoundContext`** to deduplicate the round kwargs across `build_*_context` functions.

---

## 9. Note for cross-review with sdet-agent

My review focuses on types and purity. An sdet-agent reviewing the same suite is more likely to catch:

- Whether the test **assertions** are strong enough (e.g., I noted that `test_two_rounds_creates_round_dirs` at `test_engine_phases.py:541-568` asserts conditional directory existence — that's weak; the test should force one branch or the other).
- Whether **failure modes** are covered (I noted gaps at `TestRunPipelineFailures` only testing Phase 1 failure in isolation; an sdet would list every phase with "what if this fails" cases).
- Whether the **test names** document behavior clearly (the functional lens is insensitive to this).
- Whether fixtures scale to **parallel test execution** (I noted the module-level `_preset_cache` as a purity issue; an sdet would also note it will break `pytest-xdist`).

I expect convergence on the top findings:
- Tests mixing unit and integration concerns (§1)
- Weak exception assertions (§2)
- Global mutable cache in `engine/config.py` (§4)

I expect divergence on:
- Whether the discriminated-union refactor is worth the churn. (Functional lens: yes. SDET lens: probably "nice to have, not a bug".)
- Whether `_make_config` duplication is a test-hygiene issue or a typing issue. (Functional lens: typing. SDET lens: hygiene.)

---

## Appendix: cited file paths

All paths absolute:

- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_engine_core.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_engine_phases.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_engine_config.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_engine_templates.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_linter_validate.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_linter_usage.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_linter_quality.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_linter_classifier.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_linter_output_contract.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/errors.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/models.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/_root.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/cost.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/events.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/phases.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/config.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/engine/templates.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/validate.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/usage.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/quality.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/question_classifier.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/output_contract.py`
- `/Users/business-daddy/code/payer-index-mono/conversus/linter/models.py` (reference — good patterns to replicate)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/modes.py` (reference)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/features.py` (reference)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/plugins/nashopt/payoffs.py` (reference)
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_payoffs.py` (reference)
