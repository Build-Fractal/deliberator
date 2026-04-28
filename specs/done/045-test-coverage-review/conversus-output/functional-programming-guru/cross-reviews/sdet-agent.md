# Cross-Review of sdet-agent Review

**Reviewer:** functional-programming-guru
**Target:** sdet-agent's Round 1 review
**Round:** 2 of 2 (cooperative deliberation)
**Date:** 2026-04-03

---

## Executive Assessment

The sdet-agent's review is high-quality and carries findings I missed. The discipline-level concerns (match= specificity, parametrization of deterministic counts, branch-isolation for the `find_project_root` strategy chain) are exactly the kind of thing a type-systems lens tends to under-weigh, and most of them are correct. However, a non-trivial fraction of the sdet's "tighten the assertion" fixes are **redundant with a properly fixed type system** — once `phase`, `mode`, `provider`, `stagnation`, and `category` become `Literal` types, several of the "use `match=...`" recommendations become inapplicable because the model construction path that was being asserted against can no longer exist.

Below, a point-by-point cross-review organized against the five prompts.

---

## 1. Convergence — where we both land on the same finding

### 1.1 `with pytest.raises(Exception)` is too broad (STRONG AGREEMENT)

SDET §1.2 and §3.1 catalog six locations. My review §2 "Gaps" and §7 "Minor nits" flagged the same pattern at:

- `tests/test_engine_config.py:854, 869` (me: "too loose. `Exception` catches `AttributeError`, `TypeError`, `ValueError`, and `ValidationError` indiscriminately")
- `tests/test_engine_phases.py:282` (me: "Should be `pytest.raises(ValidationError)`")
- `tests/test_linter_classifier.py:313` (me: §7 minor nit)
- `tests/test_linter_output_contract.py:356, 389` (me: §2 gaps)

We describe the same root cause from different angles. SDET frames it as "over-broad exception catch can swallow a `NameError` or `AttributeError` from a bad refactor" (true). I frame it as "the test fails to distinguish the Pydantic frozen-violation surface from any other exception type" (true). Both framings converge on the same fix: `pytest.raises(ValidationError, match="frozen")`.

**Verdict: converge. The sdet's list is more complete than mine — adopt their enumeration.**

### 1.2 Global mutable `_preset_cache` is a test-isolation hazard

SDET §6.1 and §4.1 flag `_preset_cache.clear()` at `test_engine_config.py:968, 1069, 1143, 1254`. My §4 "Violations — mutable module state" flagged the same pattern at `engine/config.py:214`.

SDET correctly notes the three `setup_method` definitions are "evidence that the global cache is the wrong design." My review made the same argument and offered the same fix (thread the cache as a parameter). **Verdict: converge, same remedy.**

SDET goes further than I did in one respect: they identify that this breaks `pytest-xdist` parallel execution (SDET §12, item 1). I had implied this in §4 without stating it explicitly. Credit to SDET.

### 1.3 Unit/integration boundary is blurred

SDET §1.3 ("Ugly: tests that depend on real project layout") is not a section of theirs — but their §5.4 identifies that `test_importlib_resources_fallback_path` at `test_engine_core.py:681` "passes if any of strategies 2/3/4 succeed" — which is structurally the same bug I described in my §1 ("I/O coupled tests"): the test cannot isolate its target because the target depends on the real project layout.

**We converge on the problem; we differ on the fix.** SDET's remedy is "rename or fix the test so the name is truthful" (§8.3). My remedy is "refactor `find_project_root` to take strategies as injected functions so each can be tested in isolation" (§1, §5). Both are correct but operate at different levels. The SDET fix is correct for Round 1; the FP fix is the long-term remedy.

### 1.4 Templates round-trip tests are integration tests masquerading as unit tests

SDET does not flag this explicitly; I flagged `tests/test_engine_templates.py:619-647` in my §1. However, SDET's §5.8 notes "Real templates covered via `TestRealTemplateRoundTrip`. Good." We disagree on characterization — I say "smoke test that should be marked `@pytest.mark.integration`", SDET says "good." Not a contradiction, just different tolerances.

---

## 2. Where the sdet-agent catches issues I missed

These are findings my review did not include, and which survive my scrutiny.

### 2.1 Deterministic counts asserted with `>=` (I MISSED this)

SDET §1.1 identified:

- `test_linter_quality.py:170, 181, 281` — `assert result.dispute_count >= 1` on a deterministic fixture
- `test_linter_quality.py:326, 361` — `assert len(result.agent_names) >= 2`
- `test_linter_output_contract.py:180` — `count > 0`
- `test_engine_core.py:835` — `assert result.estimated_usd > 0` with `agent_count=0`

I reviewed these files and did not flag them. This is a legitimate blind spot in a type-systems review: a `dispute_count >= 1` assertion **typechecks correctly** even though the test is weak. The type lens sees "`int >= int`" and says "fine." The discipline lens sees "deterministic fixture means we know the answer — assert it." **SDET is correct; I missed this entirely. Adopt their recommendation.**

The last one — `test_engine_core.py:835` — is especially good because SDET actually computes the expected value: `synthesis=1 launch × (4000/1M × 3 + 2000/1M × 15)`. That's the right level of rigor for a cost calculation where the formula is deterministic.

### 2.2 Parametrization of `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` tables

SDET §4.1 flags `test_engine_core.py:846-852` and `:855-859`: table-driven loops inside test bodies that should be `@pytest.mark.parametrize` so individual rows report individually. I did not flag this — my review was focused on the fact that the test exists to compensate for a missing `TypedDict`/`BaseModel` definition.

**Both are correct, but the parametrization fix is the right *tactical* move regardless of whether the type fix lands.** If `PROVIDER_MODEL_OPTIONS` becomes `dict[str, list[ModelOption]]`, the test still exists (validating the actual data) and should still parametrize.

### 2.3 `_count_challenges` combined-path coverage gap

SDET §5.10: "Challenged By column" path and "inline cross-review" path are each tested, but not the combined case. I did not trace source-code branch structure at this level of detail. **Legitimate SDET catch.**

### 2.4 `build_disputes_context` iteration=2 off-by-one

SDET §5.8: `build_disputes_context` tested at `iterations=1` and `iterations=3` but not `iterations=2`. Classic off-by-one hole. I did not notice this because I was tracking type signatures, not input-coverage boundaries. **Legitimate SDET catch.**

### 2.5 `rounds: 1.5` float, `target: []`, `validate_templates: "true"` (string)

SDET §2.1 and §5.7 enumerate edge cases my review did not. The Pydantic coercion rules for these inputs are non-obvious — `1.5 → 1` may silently succeed (`int` coercion), `"true" → True` may succeed (bool coercion). **These are exactly the tests that `Literal` and `StrictInt`/`StrictBool` would make redundant, but until that refactor lands, SDET's tests are correct.** See §3 below for the type/test trade-off.

### 2.6 Test-naming gaps

SDET §8 catalogs `test_minimal`, `test_defaults`, `test_frozen`, `test_empty`, `test_simple_factual_interactive`. My review §9 explicitly said "the functional lens is insensitive to [test naming]." SDET is doing the job my lens can't do. All of their naming fixes should land.

### 2.7 `_find_conversus_root` / `find_project_root` strategy isolation

SDET §5.4 identifies that strategies 2 and 3 of `find_project_root` (in `engine/_root.py`) are **not independently exercised**. This is more precise than my §1 coupling finding. My review said "this test is coupled to the real project layout"; SDET said "and also, a broken strategy 3 would be silently masked by strategy 2." The second observation is the sharper one. **SDET is correct.**

### 2.8 `_has_alternatives` single-letter and whitespace edge cases

SDET §2.1: whitespace-only input to `classify_question` not tested; single-letter alternatives `"A or B"` not tested. These are specific input-space gaps a type review won't find because the input type is already `str`.

---

## 3. Where I push back — SDET fixes insufficient relative to a type-systems fix

### 3.1 "Add `match=...`" recommendations that disappear under a `Literal` refactor

SDET §3.1 recommends adding `match="frozen"`, `match="duration_ms"`, `match="agent_reviews"`, etc. across `tests/test_engine_core.py:98, 208, 328, 336, 394`.

My pushback: **if `PhaseStarted.phase`, `PhaseCompleted.phase`, `AgentCompleted.phase`, `EngineConfig.mode`, etc. are retyped from `str` to `Literal[...]`** (my review §5a), then:

- `test_engine_core.py:208` — the test that passes `agent_count="three"` is still valid, but the *failure mode* shifts from "pydantic int-coercion rejects 'three'" to the same thing with a more specific message. `match="agent_count"` is still a good idea.
- `test_engine_core.py:208` — a new, **more valuable** test becomes possible: `PhaseStarted(phase="revieww", ...)` — currently this *succeeds* because `phase: str`. After the `Literal` fix, it raises `ValidationError` with `match="phase"`. That test does not exist today because *the bug it would catch is unfixable without the type change*.

**Conclusion:** SDET's `match=...` recommendations are correct and should land. But SDET is implicitly assuming the current type signature. Once `phase: Literal[...]` is in place, SDET's recommended tests become a subset of a larger set of tests that become newly expressible.

### 3.2 `rounds: 1.5`, `validate_templates: "true"`, `iterations: 10000` — type-system says reject at the boundary

SDET §2.1 and §5.7 recommend tests for:

- `rounds: 1.5` (float instead of int)
- `validate_templates: "true"` (string instead of bool)
- `validate_templates: 1` (int coerced to bool)
- `iterations: 10000` (no upper bound)

My pushback: these tests are all testing Pydantic's coercion layer, which is **configurable** at the model level. The right fix is to declare the model field as `StrictInt` / `StrictBool`:

```python
from pydantic import StrictInt, StrictBool

class EngineConfig(BaseModel):
    rounds: StrictInt  # refuses 1.5 and "5"
    validate_templates: StrictBool  # refuses 0, 1, "true"
    iterations: conint(ge=1, le=1000)  # explicit bounds
```

With `StrictInt`/`StrictBool`, the tests SDET recommends become **property-based** rather than enumeration-based: "any non-int rejects" is one test, not four. And `conint(ge=1, le=1000)` makes the "very large iterations" test into a boundary test with clear semantics ("1001 rejects") instead of SDET's more vague "10,000-iteration config parses?".

**Conclusion: SDET's tests would pass today but wouldn't pass tomorrow if we tightened coercion. The type fix is more durable.** That said, SDET's tests should land immediately because `StrictInt` is not yet in place — this is a "both, in sequence" situation, not an "either/or."

### 3.3 `category = getattr(exc, "category", "unknown")` — the test at `test_engine_core.py:131` shouldn't exist

SDET §2.1 says: "`ProviderError` with `category=None` — `getattr(exc, "category", "unknown")` path returns `"unknown"` and falls to the 502 branch. Not tested: only `"mystery"` string is (line 131). `None` and missing attribute are distinct paths."

This is correct about the current code. But my review §6a argued something stronger: **the `"unknown"` fallback branch is a bug farm, and the right fix is to make `ProviderError.category: Literal["auth", "rate_limit", "server"]` a required field.** Under that fix:

1. `getattr(exc, "category", "unknown")` becomes `exc.category` — no fallback.
2. The "unknown category → 502" branch at `engine/errors.py:78-83` becomes **unreachable code**.
3. The test at `test_engine_core.py:131-135` becomes **invalid** — you cannot construct a `ProviderError(category="mystery")` at all; mypy rejects it and the Pydantic validator (if applicable) rejects it at runtime.
4. SDET's "also test `category=None` and missing attribute" tests become **impossible to express** — they would be testing a state the type system says cannot exist.

**Conclusion: SDET's test recommendations here patch the symptom. The type fix removes the illness.** The fallback branch is dead code waiting to become a bug; deleting it is preferable to testing it. I believe SDET would agree if pushed — see their own §9 finding #5 ("`engine/models.py:159` — `except (ValueError, Exception)` is redundant"), which is the same kind of "testing a thing that shouldn't exist" observation.

### 3.4 `_normalize_agent_name` unicode test — property test, not enumeration

SDET §2.1: "Name with unicode diacritics — `"josé"` → `"José"`? not tested."

My pushback: if `_normalize_agent_name` is a pure string function (it is, at `linter/quality.py`), the right test isn't one unicode input — it's a Hypothesis property test: `normalize(normalize(s)) == normalize(s)` (idempotent) and `normalize(s).lower() == normalize(s.lower())` (case-stable). A single `"josé"` input is an anecdote. SDET's own §12 item 3 acknowledges "fp-guru may point out that this is a table-driven property test and suggest hypothesis instead of parametrize" — they anticipated this pushback and I confirm it.

### 3.5 Test that `log_usage` writes `dispute_count` to JSONL

SDET §1.4: "A regression that dropped `dispute_count` from the log would not be caught by this test." (`test_linter_usage.py:192-195`)

My pushback: this is only a testable regression because `log_usage` takes `quality_json: dict | str` and internally calls `.get("dispute_count", 0)` — schema drift is possible. If the function signature becomes `log_usage(quality: QualityReport)` where `QualityReport` is a frozen Pydantic model with a required `dispute_count: int` field, dropping the field causes **construction-time** failure in the call site, not log-read-time failure downstream.

SDET's test is a valid safety net for the current design. My suggestion: **the test should exist, but it's a test of the wrong thing.** The real assertion is "`QualityReport` round-trips through `log_usage` without field loss," which is one `assert json.loads(line)["dispute_count"] == report.dispute_count` after a single construction — not a survey of every field.

---

## 4. Architectural implications the sdet-agent missed

This is the most important section. **A material fraction of the sdet's recommended assertion-strength fixes become redundant if the type fixes from my review §5 land first.**

### 4.1 String-typed `phase`, `mode`, `provider`, `stagnation`, `category`

My review §5a cited (copying for reference):

- `engine/config.py:67` — `mode: str` should be `Literal[...8 modes...]`
- `engine/config.py:73` — `stagnation: str` should be `Literal["detect", "ignore"]`
- `engine/config.py:77` — `provider: str` should be `Literal["anthropic", "openai"]`
- `engine/events.py:28, 39, 50, 63` — `phase: str` should be `Phase` enum
- `engine/models.py:30, 41, 62, 63` — ditto
- `engine/phases.py:70` — `termination_reason: str | None` should be `Literal[...] | None`
- `engine/errors.py:28` — `category: str` should be `Literal[...]`

**Implicit dependency in the sdet's review:**

| sdet finding | depends on weak string type |
|---|---|
| §2.1 "`ProviderError` with `category=None`" edge case | `ProviderError.category: str` |
| §3.1 `match="frozen"` on `mode` tests | none — `match=` is orthogonal |
| §3.1 `match="agent_count"` on `PhaseStarted` tests | none — but new test becomes possible for `phase="typo"` |
| §5.7 "`validate_templates: "true"` string" | bool coercion on `Pydantic` — use `StrictBool` |
| §1.4 `test_cli_validates_successfully` checks `"valid against schema"` text but no `files_checked > 0` | none — orthogonal |
| §2.1 `ProviderError` category `"mystery"` unknown-fallback | **YES — test becomes impossible under `Literal`** |
| §5.7 `validate_templates: 1` coerced to bool | **YES — `StrictBool` makes test redundant** |
| §2.1 `negative agent_count` returns 2 (positive nonsense) | **YES — `conint(ge=0)` makes test impossible** |
| §2.1 `agent_count=0` cost calc | valid — keep |
| §2.1 `rounds: 1.5` float | **YES — `StrictInt` makes test redundant** |
| §8.3 `test_importlib_resources_fallback_path` rename | depends on `find_project_root` refactor, not types |

**Summary:** Of the sdet's 30-ish concrete test recommendations, I count approximately **5-7 that become redundant after the type fixes land**, and approximately **3-4 that become newly *possible*** (the "typo in mode/phase/category" tests that today silently succeed).

This is the most important finding of my cross-review: **SDET's recommendations should land in a specific order relative to my recommendations.**

1. Land type fixes first (§5a, §5b of my review).
2. Delete the unreachable fallback-branch tests (SDET §2.1 ProviderError mystery, §5.7 validate_templates string).
3. Land the remaining SDET `match=...` tightenings — these are pure discipline wins, no dependency.
4. Add new "typo" tests that the type system now supports (`phase="revieww"` → ValidationError).

If steps 1-2 are reversed, we land dead tests that then need to be deleted — wasted effort.

### 4.2 `engine/cost.py` dict returns

My review §5b flagged `estimate_cost() -> dict[str, int]` (line 70) and `estimate_cost_usd() -> dict` (line 106, no type param!). SDET §1.1 correctly says `assert result["estimated_usd"] >= 0` is tautological.

**Architectural implication SDET missed:** if `estimate_cost_usd` returns `CostEstimate(BaseModel)` as I proposed, then:
- `result["estimated_usd"] >= 0` becomes `result.estimated_usd >= 0` — mypy now typechecks the attribute access, so a typo like `result.estimated_USD` fails statically.
- The "assert the concrete dollar figure" recommendation SDET makes becomes `assert result.estimated_usd == 0.048` — exact, typed, specific.
- The test at `test_engine_core.py:770-778` that "dereferences [7 keys] blind" becomes unnecessary because the model construction in `estimate_cost_usd` already validates all 7 fields.

**Conclusion: 3 of SDET's §1.1 weak-assertion fixes are special cases of my §5b type fix.**

### 4.3 `EngineEvent` discriminated union

My review §5d recommended adding a `type: Literal[...]` discriminator to `PhaseStarted`, `AgentDispatched`, `AgentCompleted`, `PhaseCompleted`.

**SDET missed implication:** with a discriminator, the `isinstance` chains in `engine/models.py:106-128` that SDET references in §5.5 collapse to a dict dispatch. The branch-coverage analysis SDET did in §5.5 (covering `rounds_completed == 0`, `synthesis_text.strip()` false, etc.) is still valid — those are control-flow branches, not type branches. But the `isinstance(ev, AgentCompleted)` filtering at `test_engine_core.py:455-474` becomes `ev.type == "agent_completed"`, and mypy narrows through it. **SDET's branch coverage doesn't change; the test style does.**

---

## 5. SDET §12 "items for cross-review" — my answers

### 5.1 `_preset_cache` as module state

SDET: "FP lens would likely argue for pure injection; I'm agnostic on the refactor priority."

**My answer: YES, refactor to injection.** This is not "nice to have" — it's a prerequisite for `pytest-xdist` parallel execution, which SDET themselves noted in §12. Thread the cache as `_load_preset_file(path, cache: dict[Path, PresetFile])` where `cache` defaults to a fresh dict. In tests, every test supplies its own empty cache. The three `setup_method` definitions at `test_engine_config.py:968, 1069, 1143, 1254` delete.

Going further: once we have `PresetFile(BaseModel)` instead of `dict[str, Any]`, the cache becomes `dict[Path, PresetFile]`, and the test at `test_engine_config.py:972-989` that mutates disk to verify caching identity (`first is second`) still works because Pydantic models are frozen and identity-comparable.

### 5.2 Monkey-patching `load_template`

SDET: "The alternative is to construct real failing inputs. FP lens may prefer dependency injection at the `run_pipeline` level."

**My answer: YES, dependency inject `load_template`.** The current monkey-patch at `test_engine_phases.py:1089` (`monkeypatch.setattr(phases_mod, "load_template", _bad_load)`) is exactly the kind of internal-API coupling that breaks under refactoring. The fix is to accept a `template_loader: Callable[[str, str], str]` parameter on `run_pipeline()` — in production, defaults to `load_template`; in tests, pass a failing lambda. No monkeypatch needed, no reliance on import-time binding.

Strong argument in favor: SDET's own §7.2 notes this is "internal-API patching" and warns that "if the arbitration path is refactored to inline template loading, the test will silently stop exercising the intended except branch." That warning disappears entirely under dependency injection.

### 5.3 Parametrization of `MODEL_PRICING` / Hypothesis

SDET: "I recommend per-row parametrization; fp-guru may point out that this is a table-driven property test and suggest hypothesis."

**My answer: both, at different layers.**

1. **Per-row parametrization is correct for tabular invariants** — "every entry has keys X, Y, Z, W" should parametrize over rows so failures report per-row (exactly as SDET says).
2. **Hypothesis is correct for algebraic invariants** — "cost is linear in tokens" (the law my review praised at `test_engine_core.py:818-822`) should be a `@given(st.integers(...))` property.

These are not competing recommendations. The per-row parametrize is for "the data table is well-formed"; the Hypothesis is for "the formula has the right algebraic structure." Different tests, different targets.

**However**: if `MODEL_PRICING` becomes a `dict[str, ModelPricing]` where `ModelPricing(BaseModel)` has `input: float` and `output: float` as required fields, then Pydantic enforces "every row has both keys" at construction time, and SDET's parametrized test "asserts each row has input and output" becomes **redundant** — the model validates at import time. The parametrized test should still exist for *value* invariants (positive, non-zero), not *shape* invariants.

### 5.4 `_extract_remaining_disputes` heading regex proliferation

SDET: "fp-guru may have views on unifying via a data-driven pattern table instead of regex branches."

**My answer: YES, and the unification is straightforward.** The heading list at `engine/models.py:180-185` (and the symmetric one in `engine/templates.py`) is currently an OR-chain inside a regex. The right abstraction is:

```python
DISPUTE_HEADINGS: frozenset[str] = frozenset({
    "Remaining Disputes",
    "Dangerous Contradictions Found",
    "Key Disputes",
    "Open Disputes",
    "Outstanding Disputes",
    "Disputed Areas",
    "Unresolved Tensions",
    "Remaining Contradictions",
    # ...
})

def _is_dispute_heading(line: str) -> bool:
    stripped = line.strip().lstrip("#").strip()
    return stripped in DISPUTE_HEADINGS
```

This:
1. Makes the list *data*, not *regex syntax*. Adding a new heading is a frozenset entry, not a regex edit.
2. Makes the test `test_parses_disputes_bullet_list` parametrizable over every heading in `DISPUTE_HEADINGS` — SDET §2.1 specifically notes that only "Remaining Disputes" is tested out of ~8 variants. A parametrized test fixes this in one line.
3. Eliminates the regex-escape bug risk.

**This is a win on both lenses.** SDET gets coverage of all variants; I get a typed data-driven dispatch.

### 5.5 Except-branch in `models.py:159` — dead code or best-effort?

SDET: "is this a functional-style 'best-effort' parser, or dead code? The FP lens may have an opinion on whether swallowing `Exception` is acceptable here."

**My answer: it's dead code masquerading as best-effort, and it should be deleted.** Examining `engine/models.py:154-162`:

```python
if synthesis_text.strip():
    try:
        parsed = parse_synthesis(synthesis_text, mode=mode)
        headline = parsed.headline
        summary = parsed.summary
    except (ValueError, Exception):  # line 159
        headline = ""
        summary = ""
```

Three observations:

1. **`except (ValueError, Exception)` is redundant** — `Exception` subsumes `ValueError`. SDET spotted this in their §9 finding #5. The fact that the code was written this way suggests the author was unsure about the exception surface of `parse_synthesis`.

2. **Best-effort parsing is a code smell when the contract isn't written down.** If `parse_synthesis` has a documented contract `str → ParsedSynthesis` where the `ParsedSynthesis` type encodes "headline may be missing" via `headline: str` (empty on miss), then the caller never needs `try/except` — it just uses the result. The current design has `parse_synthesis` raising `ValueError` on empty input, and the caller catching it to produce the same empty result. **Round-trip through an exception is pure overhead.**

3. **The "functional" take is: `parse_synthesis(text: str) -> ParsedSynthesis` where `ParsedSynthesis(headline: str, summary: str, ...)` is total over all strings — empty input returns `ParsedSynthesis(headline="", summary="", ...)`, not a raise.** Then the try/except disappears and the test SDET flagged as "not explicitly tested" doesn't need to exist because the failure mode doesn't exist.

**Concretely: delete lines 159-162 from `engine/models.py`. Refactor `parse_synthesis` to return a total `ParsedSynthesis` instead of raising on empty. Delete the corresponding test.** This is three lines of deletion plus one function refactor, and it eliminates SDET's "dead-until-proven-reachable" finding entirely.

---

## 6. What I'd change if I could only merge one thing

If I had to prioritize a single merge order across both reviews combined:

1. **First**: Convert `phase`, `mode`, `provider`, `stagnation`, `termination_reason`, `category` from `str` to `Literal[...]` / enum types (my §5a).
2. **Second**: Delete the now-unreachable fallback branches and their tests (SDET §2.1 ProviderError mystery, `engine/errors.py:78-83`, `engine/models.py:159`).
3. **Third**: Apply SDET's `match=...` tightenings across all `pytest.raises` sites (SDET §3.1).
4. **Fourth**: Replace `engine/cost.py` dict returns with Pydantic models (my §5b) and collapse SDET's tautological cost assertions to exact-value assertions (SDET §1.1).
5. **Fifth**: Thread `_preset_cache` as a parameter (both §6.1 of SDET and my §4).

Steps 1-2 before 3-4 because step 3-4's test edits depend on knowing which tests survive step 2's deletions.

---

## 7. Where the sdet-agent's review is better than mine

Three places, for the record:

1. **Enumeration completeness** — SDET found six `pytest.raises(Exception)` sites; I found five. They found the deterministic-count weak-assertion pattern at 5 locations I missed.
2. **Branch-level precision** — SDET's §5 walks source-file branches and checks each against tests. My review walks source-file types and checks each against usage. Both are valid, but SDET's is more directly tied to coverage.
3. **Test-name hygiene** — I explicitly abdicated on this in my review; SDET's §8 is thorough and should land as-is.

---

## 8. Where my review is better than the sdet-agent's

Two places:

1. **Architectural level** — SDET's recommendations are almost all at the test file. Mine span test → model → type signature → discriminator. This matters for step-ordering (§4 above).
2. **Algebraic properties** — I called out the `test_engine_core.py:818-822` linearity law as a model test to emulate; SDET's §1.1 instead flags a sibling test (`estimated_usd > 0`) as weak. Both correct, but the FP lens sees the law as the better target for Hypothesis.

---

## 9. Items for Round 2 synthesis

For the synthesis agent, the cooperatively-agreed conclusions:

1. **Replace all `pytest.raises(Exception)` with `pytest.raises(ValidationError, match=...)`** — 6 sites. No dependencies; land first.
2. **Thread `_preset_cache` as a parameter** — eliminates three `setup_method` definitions and enables `pytest-xdist`.
3. **Convert weak deterministic assertions to exact values** — SDET §1.1 list.
4. **Parametrize `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` table tests** — SDET §4.1.
5. **Rename `test_minimal`, `test_defaults`, `test_frozen`, etc.** — SDET §8.2.
6. **Convert `phase`, `mode`, `provider`, `stagnation`, `category` to `Literal`/enum** — my §5a. Must land before some of SDET's tests are written (§4 above).
7. **Convert `engine.cost` dict returns to Pydantic models** — my §5b. Makes SDET §1.1 fixes concrete.
8. **Delete dead fallback branches**: `engine/errors.py:78-83` unknown-category fallback, `engine/models.py:159` best-effort except. Fix the type signature instead.
9. **Add `PresetFile(BaseModel)` in `engine/config.py`** — eliminates `dict[str, Any]` from 7 sites.
10. **Split `log_usage()` into `build_usage_entry()` + `append_usage_entry()`** — unit/integration separation, enables SDET's "assert all fields present" as a round-trip test on the pure builder.

Divergences for arbiter / synthesis to resolve:

- **Scope of `StrictInt` / `StrictBool` adoption.** SDET's tests for `rounds: 1.5`, `validate_templates: "true"`, etc. work with current Pydantic coercion. If the fix is `StrictInt`, those tests change shape. My recommendation: `StrictInt` for `EngineConfig` top-level fields; default coercion elsewhere. But this is a judgment call.
- **`EngineEvent` discriminated union.** My review recommends; SDET does not address. SDET's branch-coverage concerns don't change under the refactor, but the churn is non-trivial.
- **Hypothesis vs parametrize for algebraic laws.** I'd like `test_engine_core.py:818-822` cost linearity to become a Hypothesis property. SDET does not weigh in.

---

**End of cross-review of sdet-agent (Round 2).**
