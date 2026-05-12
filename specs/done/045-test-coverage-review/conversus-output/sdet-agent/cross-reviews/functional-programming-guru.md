# SDET Cross-Review of functional-programming-guru

**Cross-reviewer:** SDET agent
**Subject review:** `<HOME>/code/payer-index-mono/conversus/specs/045-test-coverage-review/conversus-output/functional-programming-guru/review.md`
**Round:** 1 cross-review (cooperative deliberation)
**Date:** 2026-04-03

---

## Opening position

The guru's review is strong and largely complementary to mine. Where we touch the same ground, the findings are reinforced by being reached from different angles; where we diverge, the divergences are real and the guru's type-level view catches things my behavioral view missed. But I want to push back in one specific place: the guru's P0 (convert strings to `Literal`/`StrEnum`, convert untyped dicts to Pydantic models) does **not** eliminate the need for the behavioral tests I flagged. In several cases the type fixes actually *generate* new test obligations. I walk through each axis below.

---

## 1. Convergence — we independently caught the same issues

### 1.1 Bare `pytest.raises(Exception)` — strong convergence

Guru §2 "Pydantic model tests: field constraints + type coercion" — specifically the paragraph at `review.md:66` — and my §1.2 (review.md:28-41) identify the **exact same six sites** as over-broad:

| Site | Guru | SDET |
|---|---|---|
| `tests/test_engine_config.py:854` | cited | cited (table row) |
| `tests/test_engine_config.py:869` | cited | cited |
| `tests/test_engine_phases.py:282` | cited | cited |
| `tests/test_linter_classifier.py:313` | cited | cited |
| `tests/test_linter_output_contract.py:356` | cited | cited |
| `tests/test_linter_output_contract.py:389` | cited | cited |

We agree on the fix (`pytest.raises(ValidationError)`) and the rationale (broad `Exception` catches unrelated runtime errors from bad refactors). This is the highest-confidence finding in the cross-review — two independent lenses, same sites, same fix. **Priority: P0, no further debate needed.**

### 1.2 Module-level mutable state in `engine/config.py:214` — strong convergence

Guru §4 (`review.md:103-111`) and SDET §6.1 (`review.md:291`) both identify `_preset_cache: dict[Path, dict[str, Any]] = {}` as the root cause of the repeated `setup_method` calls at `test_engine_config.py:968, 1069, 1143, 1254`.

Same root cause framed from two angles:
- **Guru:** purity violation — a pure `_load_preset_file` would not need `setup_method` resets.
- **SDET:** isolation/xdist risk — shared state breaks parallelism and creates order fragility.

The guru's proposed fix is better than mine: "thread the cache through as a parameter" (review.md:111). I called it an isolation risk but did not propose a refactor; the guru's injection proposal is the cleaner solution. **I adopt the guru's fix recommendation.**

### 1.3 Integration-in-unit-clothing at `tests/test_engine_phases.py:305-421` — convergence

Guru §1 "Bad" (review.md:33-40): flags `TestRunPipelineCooperative` as end-to-end rather than unit.

I did not call this out as sharply in my review — I treated it as acceptable pragmatic coverage. **This is a place the guru catches something I softballed.** The structural argument is correct: there is no unit-level test for `_run_single_round` in isolation (`engine/phases.py`), and the pipeline tests are the only path exercising it. An sdet-level rebuttal would be "but the pipeline tests do cover the phase branches via `_PhaseSelectiveProvider`" — which the guru acknowledges. The right sdet response is: **the pipeline tests cover the branches, but they don't isolate the failure, so when one fails the root cause is buried under 5 phases of orchestration noise.** I agree with the guru here and upgrade this finding's visibility in my own P0.

### 1.4 `_make_config` duplication — convergence, different framings

Guru §3 (review.md:88-89) and my §6 (implicit) both notice that `_make_config` appears in two test files. Guru frames it as a composability problem solved by promoting to `conftest.py`; I noticed it but did not flag it. **I concede the guru's finding is stronger than mine.**

---

## 2. Where the guru catches issues I missed

### 2.1 Weak types in the code under test — the whole of §5

My review is behavioral-assertion-focused. I checked whether tests *assert* the right thing. I almost entirely skipped whether the *code under test* has types that make wrong things possible. The guru's §5 is a systematic sweep of this dimension and finds:

- **`engine/config.py:67` — `mode: str`** where `Literal["cooperative", ...]` belongs. I missed this entirely. A consequence for my review: my P2 item about `validate_templates: "true"` (string) coercion (review.md:247 of my review) is really the same class of problem — Pydantic does best-effort coercion because the types are too loose.
- **`engine/config.py:73` — `stagnation: str = "detect"`** should be `Literal["detect", "ignore"]`. I did not note this.
- **`engine/events.py:28, 39, 50, 63` — `phase: str`** where `Phase` enum exists in `linter/models.py:77-89`. This is a *cross-module typing consistency* issue and the guru is right that it's a latent bug farm. I did not notice this.
- **`engine/errors.py:28` — `category: str`** on `WebError`. I tested `category="mystery"` (review.md:71-72 of my review flags the missing `None` case) but never asked whether `category` should be a string in the first place. The guru is correct: it should be `Literal[...]`.
- **`engine/phases.py:70` — `termination_reason: str | None`** with an inline comment listing valid values. The guru's line "the inline comment is doing the work of a type" is exactly right. I wouldn't have caught this.

**Verdict: the guru's §5a findings are real and I missed them.**

### 2.2 Untyped dict returns — §5b

- **`engine/cost.py:106 — `estimate_cost_usd(...) -> dict`** with no type parameter at all. I tested this function extensively in my §1.1 (the `>= 0` weakness at `test_engine_core.py:776`), but I never noticed that the return type annotation is `dict` with no key/value types. The test at `test_engine_core.py:770-778` dereferences seven keys blind — the guru is right that a `CostEstimate(BaseModel)` would make the contract explicit and make my test assertion much tighter automatically (you'd just assert on a Pydantic equality, not on dict key presence).
- **`engine/cost.py:38 — `PROVIDER_MODEL_OPTIONS: dict[str, list[dict[str, str | float]]]`**. My §4.1 (review.md:174-178) flagged the parametrization opportunity at `test_engine_core.py:846-852`. The guru diagnoses the root cause: the code iterates the table and asserts "all four keys exist" because the type system doesn't guarantee it. A `TypedDict` would eliminate the need for the test row-by-row. **I missed this — my parametrization fix treats the symptom; the guru's TypedDict fix treats the disease.**
- **`linter/usage.py:261 — `entries: list[dict] = []`** on the read path. The existing `UsageEntry` Pydantic model exists at `linter/usage.py:49-68` but is not used on the read path. This is a bug-farm and I completely missed it. My review treats `linter/usage.py` tests as mostly fine; the guru correctly observes that the read-path `.get("quality_passed")` / `.get("session_id", "")` pattern silently swallows schema drift. **Real issue. Real miss on my end.**

### 2.3 Missing pydantic frozen/field tests — §2 "Gaps"

Guru at `review.md:67-69`:
- `DisputeInfo`, `DisagreementResult`, `AttributionResult`, `QualityResult` (`linter/quality.py:46, 55, 65, 77`) are frozen but have **zero** tests asserting frozen-ness or field validation.
- `UsageEntry`, `AdoptionMetrics`, `SynthesisMeta` (`linter/usage.py:52, 74, 92`) — same.

My review notes P1 "Tighten weak assertions" but does not enumerate the missing frozen-tests for these specific models. The guru is more comprehensive on this axis. **I should have caught this; I did not.**

### 2.4 `_FALLBACK_DISPATCH: dict[str, object]` at `linter/quality.py:421`

This is a specific `# type: ignore[operator]` at `linter/quality.py:471` that I did not look at closely. The guru diagnoses it correctly: the `object` value type loses the callable signature, forcing a type-ignore. Fixing to `dict[str, FallbackFn]` where `FallbackFn = Callable[[str], list[DisputeInfo]]` removes the ignore. **This is a latent testability issue** — if the callable signatures drift, the test suite won't catch it until runtime. I missed this.

### 2.5 The `log_usage` split proposal

Guru recommendation #4 at `review.md:300`: split `log_usage()` into `build_usage_entry()` + `append_usage_entry()`. I flagged nothing wrong with `test_linter_usage.py`; the guru correctly observes that 10 of 12 tests currently touch the filesystem *only* because the function signature conflates construction and persistence. This is a real design-level observation that would **retroactively simplify my assertion-tightening recommendations** — exact-value assertions become trivial when the function under test is pure. **Strong finding on the guru's side.**

---

## 3. Where the guru's fixes are insufficient

This is where I want to push back — not to reject the guru's P0, but to argue that the type fixes do **not** eliminate the behavioral tests and, in several cases, create new ones.

### 3.1 Converting `mode: str` to `Literal[...]` does not close the test-coverage gap at `engine/config.py`

The guru's P0 item #1 says: make `mode`, `stagnation`, `provider`, `phase`, `termination_reason` into `Literal`/`StrEnum`. I agree it's a good change. But:

- **The `Literal` only catches invalid values at `model_validate()` time, not at parser time.** `parse_config()` at `engine/config.py:495-659` explicitly validates `mode` against `VALID_MODES` at line 534 because the raw YAML string has to be validated *before* it's handed to the Pydantic constructor. If we tighten the Pydantic model to `Literal[...]`, the parser check becomes redundant in *one* direction (the Pydantic side) but not the other (giving the user a friendly ConfigError instead of a cryptic ValidationError).
- **So we still need tests for both layers:** (a) "bogus mode in YAML raises ConfigError with a specific message", (b) "bogus mode passed directly to `EngineConfig(mode=...)` raises ValidationError". These are not the same test. The guru's review does not distinguish them. The guru's fix adds layer (b) but does not relieve layer (a).
- **New test obligation the guru creates:** after the Literal change, we need to verify that the parser's ConfigError message is still helpful (doesn't degrade into a ValidationError that the user can't interpret). My §3 error-message-match recommendations (`review.md:106-125` of my review) become **more** important after the type fix, not less.

### 3.2 Converting `estimate_cost_usd` return to `CostEstimate(BaseModel)` does not close my P1 assertion-strengthening finding

The guru's P0 #2 says: replace `dict` returns in `engine/cost.py` with Pydantic models. I agree. But:

- **The weak assertion I flagged at `test_engine_core.py:776` (`assert result["estimated_usd"] >= 0`) is *still* weak even if `result` is now a Pydantic model.** The assertion checks a tautology: a cost-calculation with positive constants is always >= 0. The type system cannot tell you whether the number is *correct*, only whether it's a number. The fix is still "assert the exact computed value" — and the test becomes `assert result.estimated_usd == pytest.approx(0.0042)` instead of `>= 0`.
- **New test obligation the guru creates:** the Pydantic model itself needs frozen/required-field tests (see guru's §2 "Gaps" at review.md:67-69 — he's already pointed this out; I'm just flagging that the P0 type fix *adds* those tests to the queue, not removes them).

### 3.3 TypedDict for `PhaseCounts` doesn't eliminate the `test_engine_core.py:731-738` "arbitration not in phases" assertion

The guru says (review.md:164): "The test at `test_engine_core.py:731-738` has to assert `'arbitration' not in phases` — an assertion that would be statically eliminable with the right type."

**This is not quite right.** With `NotRequired`, `arbitration` is statically absent *at the type level*, but at runtime the dict either has the key or doesn't. The test is asserting the runtime shape: "when there is no arbiter, the returned dict does not include an `arbitration` key." That's behavior, not typing. The static type system says "this key may or may not exist"; the test says "in this specific input, it does not exist." The guru is conflating **type presence** with **runtime presence**. The test still needs to run.

**Verdict: this is a place the guru overstates the power of the type fix.**

### 3.4 Discriminated union on `EngineEvent` — §5d, review.md:198-211

The guru recommends adding a `type: Literal[...]` discriminator to each event class. I agree it's a good change. But:

- The existing test at `test_engine_core.py:455-474` that does `isinstance(ev, AgentCompleted) and ev.response_text` works today. After the discriminator is added, the test becomes `ev.type == "agent_completed" and ev.response_text`. **The test still exists, it just changes syntax.** The guru's framing ("mypy can narrow through") is a developer-ergonomics win, not a test-elimination win.
- **New test obligation:** after the discriminator is added, `StructuredDeliberation.from_events` at `engine/models.py:106-128` can be refactored to use the discriminator instead of `isinstance`. That refactor needs tests to prove it still handles all four event types — which means the existing `test_engine_core.py` tests need to be **re-run against the new implementation**, not deleted.

---

## 4. Does fixing the type weaknesses eliminate the need for behavioral assertions?

**Clear position: no, it does not. The type fixes and the behavioral tests are orthogonal concerns.**

Here is my argument, with specific examples:

### 4.1 Types constrain inputs; behavior tests verify outputs

- A `Literal["cooperative", "winner-take-all", ...]` type on `mode` guarantees that no caller inside the codebase can construct an `EngineConfig` with `mode="zebra"`. This eliminates one class of bug at construction time.
- But the behavior of `_assemble_phase_prompt` at `engine/phases.py:90-131` when given `mode="cooperative"` versus `mode="winner-take-all"` is **not** constrained by the type. Two different modes produce two different prompts. The type system says "both are valid strings"; the test says "mode X produces prompt Y." These are different claims.
- **My P1 recommendation "add exact-value assertions for `estimate_cost_usd`" is not about whether the return is a dict or a Pydantic model. It's about whether the numeric value is right.** The type fix does not compute arithmetic.

### 4.2 Type coercion at the boundary creates new test obligations

Pydantic, by default, coerces strings to ints, floats to ints, etc. A field typed `Literal["detect", "ignore"]` will **not** coerce `"Detect"` (capital D) or `"DETECT"`. Will the config parser normalize case before calling the model? If not, the type fix introduces a subtle regression for users whose YAML has `stagnation: Detect`.

**New test obligation the guru's type fix creates:**

1. `test_stagnation_lowercase_valid` — existing behavior
2. `test_stagnation_capital_d_currently_works_but_shouldnt` — new test after the type fix
3. `test_stagnation_normalizes_case` — if we want to preserve backward compatibility

These are all behavioral tests. They would not exist without the type fix.

### 4.3 Even frozen Pydantic models need coercion-failure tests

The guru is correct that `DisputeInfo`, `DisagreementResult`, `AttributionResult`, `QualityResult` have no frozen or field-rejection tests. But adding those tests is orthogonal to adding types — it's adding **more** tests, not fewer.

### 4.4 The "dead fallback" at `engine/errors.py:79-83` is a gray area

The guru writes at review.md:235: "If `ProviderError.category: Literal['auth', 'rate_limit', 'server']` were declared, the `getattr` becomes `exc.category` and the 'mystery' fallback branch at `:79-83` (tested at `test_engine_core.py:131-135`) becomes **unreachable code** — which is a win."

**I half-agree.** Yes, once `category` is a `Literal`, the unknown-category branch becomes structurally unreachable **within the codebase**. But `ProviderError` could be raised by a third-party library that gets wrapped by `map_engine_error()` (e.g., an anthropic SDK exception that has a `.category` attribute set to a string the SDK picked). The `getattr(..., "unknown")` fallback is defensive against that exact case. Removing the branch makes the code less robust to upstream changes. **The test at `test_engine_core.py:131-135` should stay, and the fallback branch should stay, even after the type fix.**

This is a genuine disagreement with the guru's framing.

---

## 5. Practical sequencing — if we do the guru's type fixes first

Suppose we adopt all 10 of the guru's prioritized recommendations (review.md:296-307) before touching any test. What happens to my recommendations?

### 5.1 My P0 items — status after guru's fixes

| SDET P0 | Still needed? | Why |
|---|---|---|
| Replace `pytest.raises(Exception)` with `pytest.raises(ValidationError)` (§1.2) | **Still needed** | Independent of source-code types. The test-side tightening is orthogonal. |
| Test empty `events=[]` in `StructuredDeliberation.from_events` (§2.1) | **Still needed** | The type system does not compute `rounds_completed` arithmetic. |
| Isolate strategies 2 and 3 in `engine/_root.py:find_project_root` (§5.4) | **Still needed** | Strategy isolation is a control-flow concern, not a type concern. |
| `models.py:159` untested except branch (§5.5) | **Still needed** | The except swallows errors from `parse_synthesis`; typing cannot verify runtime exception behavior. |
| `engine/phases.py:661` prior_arbitration_path branch (§5.6) | **Still needed** | If it's dead code, typing doesn't help; we still need to decide to delete or test it. |

**Zero of my P0 items are eliminated by the guru's fixes.** All five remain.

### 5.2 My P1 items — status after guru's fixes

| SDET P1 | Still needed? | Why |
|---|---|---|
| Replace `>=` / `>` with exact values on deterministic fixtures (§1.1) | **Still needed; possibly easier** | Pydantic models give cleaner equality assertions but the arithmetic correctness claim is unchanged. |
| Add `match=` substrings to `pytest.raises` (§3.1) | **Still needed and more valuable** | After the type fix, the error messages become the main user-facing contract. Matching the message is exactly what prevents regressions where the text degrades. |
| Parametrize `test_agent_name_regex_valid/_invalid` (§4.1) | **Still needed** | Parametrization is a reporting concern, not a type concern. |
| Parametrize `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` row-by-row (§4.1) | **Partially obsoleted** | If `PROVIDER_MODEL_OPTIONS` becomes `list[ModelOption]` with a Pydantic schema, the "all four keys exist" row-by-row check is enforced at construction. The **tier value validity** check ("is the string one of `default/premium/budget`") is auto-enforced by a `Literal`. My parametrization becomes one test `assert len(PROVIDER_MODEL_OPTIONS["anthropic"]) > 0` plus a single `model.tier == expected_tier` assertion. **This is where the guru's fix genuinely reduces test surface area.** |

So **one** of my P1 items (row-by-row parametrization of the model-pricing table) becomes substantially simpler after the guru's `ModelOption` Pydantic model. The other three P1 items remain.

### 5.3 My P2 items — status after guru's fixes

| SDET P2 | Still needed? | Why |
|---|---|---|
| Negative/zero/unicode/empty edge cases for cost, config, events (§2.1) | **Mostly still needed** | Negative `agent_count` behavior is arithmetic — types can forbid it via `PositiveInt`, which would actually *eliminate* this test by making the invalid input impossible to construct. **This is a legitimate elimination.** But unicode agent names, empty events list, etc. remain behavior questions. |
| Strategy-2 isolation in `find_project_root` (§5.4) | **Still needed** | No type change helps here. |
| `CONCESSION_AGENT` `concedes` variant (§5.10) | **Still needed** | Regex alternation is behavioral. |
| `_extract_headline` fall-through (§5.12) | **Still needed** | Priority logic is behavioral. |
| `build_disputes_context` iteration=2 off-by-one (§5.8) | **Still needed** | Arithmetic / naming logic. |
| `_preset_cache` per-function injection (§6.1) | **Eliminated** | This is exactly the guru's recommendation #6. Once the cache is injected, my isolation concern disappears. **Good elimination.** |

**Two of my P2 items are eliminated** (negative-int via `PositiveInt`, `_preset_cache` injection). The remaining ~8 P2 items stand.

### 5.4 Items where the guru's fix creates NEW test obligations

These are tests that don't currently exist and are not in my review either, but become necessary after the guru's refactor:

1. **`build_usage_entry` + `append_usage_entry` split tests** — after splitting `log_usage`, we need (a) pure tests for `build_usage_entry` (easy, many), (b) one filesystem test for `append_usage_entry` (easy). Net increase in test count, but simpler tests.
2. **`CostEstimate` model frozen/validation tests** — after promoting the dict return to a Pydantic model, the model itself needs the "three tests per model" the guru cites (frozen, required, coercion).
3. **`PresetFile(BaseModel)` validation tests** — same.
4. **`ModelOption(BaseModel)` validation tests** — same. This one partially offsets the row-by-row parametrization elimination in §5.2.
5. **`EngineEvent` discriminator dispatch test** — needs a test that round-trips each of the four event types through the discriminated union to verify Pydantic dispatches correctly.
6. **Parser-layer error-message regression tests** — after moving validation into `Literal[...]`, the parser's `ConfigError` messages need regression tests to prove they don't degrade into raw `ValidationError` text (see my §3.1 on why this matters).

### 5.5 Summary — practical sequencing

If we do the guru's type fixes first:

- **5 of my 5 P0 items remain.** No elimination.
- **3 of my 4 P1 items remain.** 1 partial elimination (row-by-row parametrization).
- **~8 of my ~10 P2 items remain.** 2 eliminations (`_preset_cache`, `PositiveInt` on negative agent_count).
- **~6 new test obligations** are created by the guru's fixes that neither of us flagged in our first-round reviews.

**Net: the guru's type fixes are worth doing, but they do not reduce the test burden — they shift it.** Pure tests replace filesystem-coupled tests (good); exact-value assertions replace truthy assertions (good); model-validation tests are added (new); parser-layer regression tests are added (new). The total test *count* after both efforts may actually be higher than before, though the *quality* is much better and the per-test execution time should drop sharply.

---

## 6. Specific disagreements to flag for round 2 deliberation

1. **`engine/errors.py:79-83` fallback branch.** Guru calls this "unreachable after type fix." I argue it's a defensive branch against third-party exception wrapping and should stay. (§4.4 above.)
2. **`NotRequired[int]` for `arbitration` does not eliminate the test at `test_engine_core.py:731-738`.** Guru implies it does. I argue it doesn't. (§3.3 above.)
3. **The guru's §5a `Literal` conversion is not always backward-compatible with lowercase-normalization quirks in `parse_config`.** The type fix may need to be paired with explicit normalization before Pydantic construction, which is itself a behavioral test obligation. (§4.2 above.)
4. **I concede the guru's `log_usage` split is strictly better than anything I proposed.** (§2.5 above — not really a disagreement, an acknowledgment.)
5. **I concede the guru's `_make_config` promotion is a hygiene improvement I should have called out.** (§1.4 above.)

---

## 7. Cross-review verdict

The guru's review is a genuine value-add. The findings at §5 (types in code under test) cover a dimension I almost completely missed, and they surface real testability improvements. The guru's P0 recommendations are mechanically sound and should be adopted.

**But my P0 items are not superseded.** The behavioral-assertion layer is orthogonal to the type-correctness layer. After the guru's type fixes land, the SDET test suite still needs:

- Error-message regression tests (sharper, because types eliminate other assertions that would have masked drift)
- Control-flow branch isolation tests (unchanged by typing)
- Exact-value arithmetic assertions (unchanged by typing)
- Unicode / empty-string / boundary behavior tests (unchanged by typing)
- Dead-code confirmation tests (the `models.py:159` except branch, the `phases.py:661` prior_arbitration branch — typing cannot tell us whether these are reachable in practice)

**Recommendation for cooperative round 2:** sequence the guru's type fixes first (they reduce fixture complexity and enable cleaner assertions), then apply the SDET's behavioral tightening on top of the typed codebase. Neither review's P0 list should be discounted. The combined P0 set is:

1. (Guru) Convert string fields to `Literal` / `StrEnum` at the 7 cited sites.
2. (Guru) Replace dict returns in `engine/cost.py` with Pydantic models.
3. (Guru) Split `log_usage()` into pure + effectful halves.
4. (Guru) Thread `_preset_cache` through as a parameter.
5. (Both) Replace `pytest.raises(Exception)` with `pytest.raises(ValidationError)` at the 6 cited sites.
6. (SDET) Test empty `events=[]` in `StructuredDeliberation.from_events`.
7. (SDET) Isolate strategies 2 and 3 in `find_project_root`.
8. (SDET) Resolve the `models.py:159` and `phases.py:661` "dead-code-or-not" questions.
9. (Both) Add frozen / required-field / coercion-failure tests for the Pydantic models flagged in guru §2 and SDET §5.

Nine P0 items. All actionable. All justified from at least one of the two lenses.

---

## Appendix: cited file paths

- `<HOME>/code/payer-index-mono/conversus/specs/045-test-coverage-review/conversus-output/functional-programming-guru/review.md`
- `<HOME>/code/payer-index-mono/conversus/specs/045-test-coverage-review/conversus-output/sdet-agent/review.md`
- `<HOME>/code/payer-index-mono/conversus/engine/config.py`
- `<HOME>/code/payer-index-mono/conversus/engine/cost.py`
- `<HOME>/code/payer-index-mono/conversus/engine/errors.py`
- `<HOME>/code/payer-index-mono/conversus/engine/events.py`
- `<HOME>/code/payer-index-mono/conversus/engine/models.py`
- `<HOME>/code/payer-index-mono/conversus/engine/phases.py`
- `<HOME>/code/payer-index-mono/conversus/engine/_root.py`
- `<HOME>/code/payer-index-mono/conversus/linter/quality.py`
- `<HOME>/code/payer-index-mono/conversus/linter/usage.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_engine_core.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_engine_config.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_engine_phases.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_linter_classifier.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_linter_output_contract.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_linter_usage.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_linter_quality.py`

**End of SDET cross-review of functional-programming-guru (Round 1).**
