# Revision — functional-programming-guru

**Reviewer:** functional-programming-guru
**Round:** Revision after Round 1 cross-review exchange
**Peer:** sdet-agent
**Date:** 2026-04-03

---

## Executive summary of the revision

The SDET's cross-review was sharp. Reading it forced me to re-examine three positions I held implicitly; one of them (`errors.py:79-83`) I was flat wrong about, and the code evidence is unambiguous once you look at `engine/providers/__init__.py:33-44`. Two others (`NotRequired[int]` phase-counts test and `estimate_cost_usd` arithmetic assertion) I was also wrong about, but for a subtler reason: **I conflated the contract the type expresses with the observation the test makes.** The type says "this value exists and has this shape"; the test says "this value is the specific number 0.048 for these specific inputs." These are orthogonal claims. I will now defend that distinction explicitly and recalibrate.

I still push back firmly on a smaller set of points — chief among them the `"mystery"` category test name (which is misleading even though the branch is reachable) and the SDET's framing of "dead-code-or-not" as a dichotomy. But overall the SDET's core argument — **types constrain inputs, behavior tests verify outputs, and the two are orthogonal** — is correct, and my original review overstated the test-elimination power of the type fixes.

---

## 1. Concessions — positions I was wrong on

### 1.1 CONCEDED: `NotRequired[int]` does not eliminate `test_engine_core.py:731-738`

**My original claim** (review §5b and cross-review §3.3 pushback): converting `estimate_cost` to return a `PhaseCounts` TypedDict with `arbitration: NotRequired[int]` would make `assert "arbitration" not in phases` "statically eliminable."

**SDET's rebuttal** (cross-review §3.3): "`NotRequired` means the key *may or may not* exist. At runtime the dict either has the key or doesn't — that's what this test asserts. The static type says 'maybe'; the test says 'in this specific call, not.'"

**The SDET is right.** `NotRequired` is a *permissive* type marker — it widens the set of valid runtime values, it doesn't narrow them. A function returning `PhaseCounts` with `arbitration: NotRequired[int]` is type-safe whether it emits the key or omits it; both are valid. The test at `test_engine_core.py:731-738` is asserting the **specific runtime behavior** of `estimate_cost(has_arbiter=False)` — namely that the function *chooses* to omit the key. No type system can encode that choice without making `has_arbiter` itself part of the type (a dependent type, which Python doesn't have).

The test must remain. I will not repeat this conflation.

Looking at the same file at `tests/test_engine_core.py:720-727`, the companion test `test_three_agents_two_iterations_with_arbiter` asserts the **whole dict equals** a literal — this is the gold standard and it is *not* redundant with types either. A `TypedDict` says every value is an `int`; the test says each value is the *correct* `int`. Arithmetic correctness is always a test obligation.

**Action:** Remove the "statically eliminable" framing from my action list. Keep the TypedDict recommendation (it has value — attribute access, key-typo detection) but drop the claim that it reduces test count.

### 1.2 CONCEDED: Pydantic-izing `estimate_cost_usd` does not close the exact-value assertion gap

**My original claim** (review §5b and cross-review §4.2): converting `estimate_cost_usd(...) -> dict` to return a `CostEstimate(BaseModel)` makes 3 of SDET's §1.1 weak-assertion findings special cases of my type fix.

**SDET's rebuttal** (cross-review §3.2): "`assert result.estimated_usd >= 0` is tautological whether `result` is a dict or a Pydantic model. The type system guarantees the value is a `float`; arithmetic correctness requires a test. `>= 0` has to become `== pytest.approx(0.0042)` regardless of the return type."

**The SDET is right.** The concrete dollar figure for `estimate_cost_usd(agent_count=2)` with default parameters is deterministic — it's a pure function of integer launch counts times fixed per-million-token pricing. The test should assert that specific number. The Pydantic model helps with **attribute-access type safety** (no more `result["estimated_USD"]` typos that return `KeyError` at runtime) but it doesn't help with "is the number correct."

Re-reading my own review at §5b: I wrote "the test at `test_engine_core.py:770-778` that 'dereferences [7 keys] blind' becomes unnecessary because the model construction in `estimate_cost_usd` already validates all 7 fields." This is **half right and half wrong**. The part that's right: after Pydantic-ization, asserting "all 7 keys exist" is indeed redundant — Pydantic enforces that. The part that's wrong: the test is doing *two* things simultaneously — key presence *and* value sanity. Only the first is subsumed by the type fix. The value-sanity assertions (`estimated_usd >= 0`, `low <= estimated <= high`) all survive, and they should be tightened to exact values per SDET §1.1.

**Action:** Split the SDET §1.1 finding into two tranches in my updated action list:
1. The "key presence" part collapses under my type fix (shrinks the test body).
2. The "value correctness" part remains and should become `== pytest.approx(...)` assertions.

Both must land. Neither eliminates the other.

### 1.3 CONCEDED (fully): `engine/errors.py:79-83` is NOT dead code — it is reachable by default construction

This is the one I was most wrong about, and the evidence is unambiguous. I claimed in my cross-review §3.3 that "`getattr(exc, "category", "unknown")` becomes `exc.category` — no fallback" under a `Literal` refactor of `ProviderError.category`.

Let me lay out the code evidence, because it forced me to completely invert my position:

**`engine/providers/__init__.py:33-44`** — `ProviderError` definition:
```python
class ProviderError(Exception):
    """Typed wrapper for provider-layer failures.

    Attributes:
        category: One of ``"auth"``, ``"rate_limit"``, ``"server"``, ``"unknown"``.
        original: The underlying exception from the SDK, if any.
    """

    def __init__(self, message: str, *, category: str = "unknown", original: BaseException | None = None) -> None:
        super().__init__(message)
        self.category = category
        self.original = original
```

Three facts I missed on first read:

1. **`ProviderError` is a plain `Exception` subclass, not a Pydantic model.** There is no `BaseModel`, no validator, no `Literal` enforcement available at runtime without a full rewrite of the class. A `Literal` type hint on `category` would be a *lint-time* hint only; at runtime the class accepts any string.

2. **The default value of `category` is `"unknown"`.** Every single call site in the codebase that writes `raise ProviderError("something broke")` without specifying a category *produces* an object whose `.category == "unknown"`. This is not an exotic edge case; it is the documented default. I found it in use: `tests/test_engine_providers.py:80` — `err = ProviderError("something broke")`, which constructs exactly that default-category object.

3. **The docstring explicitly lists `"unknown"` as a valid category.** This is not a typo-catch fallback; `"unknown"` is a **first-class sanctioned value** of the category enumeration. The fallback branch at `errors.py:79-83` is the handler for this sanctioned value. Deleting the branch would introduce a silent behavior change for every call site that uses the default.

**The SDET's framing** (cross-review §4.4): "`ProviderError` could be raised by a third-party library that gets wrapped by `map_engine_error()` ... The `getattr(..., 'unknown')` fallback is defensive against that exact case."

The SDET's framing is correct *and* understates the case. It's not only defensive against third-party wrapping — it's the **handler for the library's own documented default category value.** Any refactor that deletes the branch would need to simultaneously delete the default, which would be a breaking API change to `ProviderError.__init__`.

**Concrete verdict on "dead code or defensive coding":** *Neither dead nor merely defensive.* The branch is **load-bearing code for the documented default value of a public API.** SDET's test at `test_engine_core.py:131-135` is correctly exercising a live branch and should stay. My recommendation to delete it was incorrect.

**What I would recommend instead** (moderating my original position): the test *name* should change. `test_provider_error_unknown_category_maps_to_502` is a better name than the current one because it ties the test to the documented default (`"unknown"`), not to an arbitrary typo (`"mystery"`). The fixture string `"mystery"` should become `"unknown"` (or the test should use `ProviderError("???")` with no category kwarg, which exercises the default path directly). This is a hygiene win, not a deletion — it's the only part of my original criticism that survives.

**Action:** Drop the "delete `errors.py:79-83`" recommendation entirely. Add a new, narrower recommendation: rename the test and rewrite the fixture to use the default-category constructor.

---

## 2. The SDET's core argument, addressed head-on

> "Type fixes and behavioral assertions are orthogonal. Types constrain inputs; behavior tests verify outputs."

**I now agree with this, with one qualification I'll defend below.**

The SDET's argument is structurally correct: the type system is a predicate on the *space of values* a variable can take; a test is an assertion about the *specific value* produced by a function for specific inputs. These are different mathematical claims. No type system can verify arithmetic correctness (without full dependent types, which Python lacks). No behavior test can verify that a value is the *only* possible output under the type (that's what types give you for free).

Where my original review went wrong was in over-counting the test-elimination power of type fixes. When I wrote "this test becomes statically eliminable," I was mostly right about the *kind* of test being eliminated (shape checks, key-presence checks, "is this a string" checks) and wrong about the *count* of tests eliminated (very few — maybe 2-3 shape-checks total, not the 5-7 I originally claimed).

**The one qualification I'll hold:** there is a narrow category of test where the type really IS the test — tests that exist *only* to assert shape, where the test body reduces to "assert isinstance(x, int)" or "assert key in d" or "assert all four keys exist in every row of this table." Those tests are *redundant* with the correct type, and they should be deleted rather than kept in parallel with the type fix. Not because "types replace tests" in general — because *that specific test exists to hand-roll a type check the type system can do for free.*

Concrete examples from the SDET's and my reviews:

| Test | Does the type fix eliminate it? | Why |
|---|---|---|
| `test_engine_core.py:776` `assert result["estimated_usd"] >= 0` | **No** — this is a (weak) value claim | Types don't verify arithmetic |
| `test_engine_core.py:738` `assert "arbitration" not in phases` | **No** — runtime shape under a specific input | `NotRequired` permits both; test asserts the choice |
| `test_engine_core.py:131-135` ProviderError unknown category | **No** — branch is reachable via default value | Not a type problem at all |
| `test_engine_core.py:846-852` "every PROVIDER_MODEL_OPTIONS row has 4 keys" | **Yes, the key-presence portion** | A `TypedDict` or Pydantic model enforces this at import time |
| `test_engine_core.py:847-851` "every tier value is 'default' / 'premium' / 'budget'" | **Yes, fully** | A `Literal` on `tier` enforces this at construction; the loop becomes impossible to write in a way that fails |
| `test_engine_core.py:208` `PhaseStarted(agent_count="three")` raises | **No** — the test exists regardless | But a companion test `PhaseStarted(phase="revieww")` becomes *newly possible* after `phase: Literal[...]` |

Counting across my original review's findings: of roughly 10 "the type makes this test unnecessary" implicit claims, **approximately 2-3 hold up after SDET's cross-review.** The other 7-8 shrink the test body (removing shape checks, replacing `.get("k", default)` with `.k`, etc.) but do not eliminate the test.

That's a material recalibration, and it changes the priority ordering I proposed in round 1.

---

## 3. Where I HOLD FIRM

### 3.1 Converting `phase: str` / `mode: str` / `stagnation: str` to `Literal[...]` is still the highest-value change

The SDET's cross-review did not contest this — they explicitly agreed in §2.1 that they missed it. My position is unchanged:

- `engine/events.py:28, 39, 50, 63` — `phase: str` should be `Literal[...]` or import the existing `Phase` enum from `linter/models.py:77-89`.
- `engine/config.py:67, 73, 77` — `mode`, `stagnation`, `provider` all `str` where `Literal` belongs.
- `engine/phases.py:70` — `termination_reason: str | None` with an inline comment listing valid values.

What my original review overstated was the *downstream test-count reduction*; what it got right was the *upstream bug-prevention value*. A `PhaseStarted(phase="revieww")` today constructs successfully and fails silently; after `Phase` enum adoption, it fails at construction with a message the user can act on.

**Crucially**, per the SDET's §5.2 analysis: "after the type fix, the error messages become the main user-facing contract. Matching the message is exactly what prevents regressions where the text degrades." This means the SDET's `match=...` recommendations become **more valuable**, not less, after my type fix lands. We're not in competition; we're in sequence.

### 3.2 `_preset_cache` threading as a parameter

SDET conceded this as the better fix (cross-review §1.2). I hold.

### 3.3 `log_usage` split into pure builder + effectful appender

SDET conceded this (cross-review §2.5: "strictly better than anything I proposed"). I hold.

### 3.4 Dependency-inject `load_template` at `run_pipeline` level

Neither of us contested this in the cross-review round. I hold.

### 3.5 `_FALLBACK_DISPATCH: dict[str, FallbackFn]` type alias

SDET conceded this (cross-review §2.4: "I missed this"). I hold.

### 3.6 `linter/usage.py` read path uses `dict` instead of `UsageEntry`

SDET conceded this (cross-review §2.2). I hold.

### 3.7 `parse_synthesis` should return a total `ParsedSynthesis`, eliminating `engine/models.py:159` except branch

This is the one place I'm *mostly* holding firm, but with a moderation. In my cross-review §5.5 I argued that `except (ValueError, Exception)` at `models.py:159` is dead code masquerading as best-effort, and that refactoring `parse_synthesis` to be total over all strings would let me delete the except clause entirely.

The SDET's response (cross-review §5.1 table): "still needed; the except swallows errors from `parse_synthesis`; typing cannot verify runtime exception behavior."

**My moderated position:** the SDET is right *as long as `parse_synthesis` remains a partial function that raises*. If we don't refactor `parse_synthesis`, then yes, the except clause is load-bearing and the test (which currently doesn't exist) should be added. But my recommendation was *to refactor `parse_synthesis` to totality*, after which the except clause becomes provably dead and deletable.

The ordering matters. I'm not claiming the current except is dead code. I'm claiming it becomes dead code after a specific refactor, and that refactor is the correct fix. The SDET is claiming that in the absence of the refactor, the current code needs test coverage for the except branch. Both are correct; they apply under different assumptions about whether the refactor lands.

**Action:** Keep the `parse_synthesis` totality refactor as a type-fix recommendation. If the refactor is rejected, fall back to SDET's position (add a test for the except branch). Do not claim the except is currently dead code.

---

## 4. Answers to the four key questions

### Q1: After `StrictInt` / `Literal` / `conint` fixes land, which SDET behavioral tests should still exist?

After an exhaustive walk of the SDET's findings list, approximately **30-32 of the SDET's ~35 concrete test recommendations should still exist** (I originally estimated ~23-25 of ~30, which was too aggressive).

Surviving SDET tests include:
- **All six `pytest.raises(Exception)` → `ValidationError` replacements** (SDET §1.2) — purely test-side, no type dependency.
- **All `match=...` tightenings** (SDET §3.1) — become *more* important after the type fix, not less.
- **All exact-value assertion replacements** (SDET §1.1) — arithmetic is always a behavior claim. This includes `estimated_usd >= 0 → ==0.0048`, `dispute_count >= 1 → == 3`, etc.
- **All control-flow branch isolation tests** (SDET §5.4 find_project_root, §5.5 models.py:159, §5.6 phases.py:661) — type-system-invisible.
- **All input-space edge cases** (SDET §2.1) that are not about type coercion: empty events list, unicode agent names, setext headings, whitespace-only classifier inputs, BEGIN/END marker pairs, etc.
- **All test-name hygiene fixes** (SDET §8) — orthogonal to types.
- **Parametrization of regex valid/invalid tests** (SDET §4.1 `test_agent_name_regex_valid/_invalid`) — reporting concern, not type concern.
- **Test that `log_usage` writes `dispute_count` to JSONL** (SDET §1.4) — survives, though becomes easier after my `log_usage` split.

Tests that are *eliminated* or *reshaped* by type fixes (2-4 items, not 5-7):
- **`test_engine_core.py:846-852` "all 4 keys present in every PROVIDER_MODEL_OPTIONS row"** — eliminated by `TypedDict` or `ModelOption(BaseModel)`. The row-by-row parametrization becomes a check of *value* invariants (positive, non-zero) after the shape invariants are auto-enforced.
- **SDET §5.7 `validate_templates: 1` coerced to bool** — eliminated by `StrictBool`.
- **SDET §2.1 `rounds: 1.5` float coercion** — eliminated by `StrictInt`.
- **SDET §2.1 negative `agent_count` returns positive nonsense** — eliminated by `conint(ge=0)` or `PositiveInt`. (SDET conceded this one in their cross-review §5.3.)

Tests that are *created* by type fixes (4-6 items — these are new obligations, not eliminations):
- **Parser-layer ConfigError regression tests** (SDET §3.1, exactly their point) — after `Literal` on `mode`, we need to verify the parser's friendly error message doesn't degrade to raw `ValidationError`.
- **Frozen / required-field / coercion-failure tests** for new Pydantic models (`PresetFile`, `CostEstimate`, `ModelOption`).
- **Discriminator dispatch tests** for `EngineEvent` after adding the `type: Literal[...]` field.
- **"Typo in phase/mode/category" tests** that are newly expressible and newly valuable.

**Net conclusion:** my type fixes and the SDET's behavioral fixes are not competing. They're complementary, and the total post-refactor test count is roughly equal to or slightly *higher* than today. Test *quality* goes up sharply; test *count* stays flat.

### Q2: Is `errors.py:79-83` "defensive coding" or "dead code"?

**Pick one:** Neither. It is **load-bearing code for the documented default value of a public API.**

**Code evidence** (re-stated for clarity):
- `engine/providers/__init__.py:41` — `def __init__(self, message: str, *, category: str = "unknown", ...) -> None`
- `engine/providers/__init__.py:37` — docstring: `category: One of "auth", "rate_limit", "server", "unknown"`.
- `tests/test_engine_providers.py:80` — live test constructs `ProviderError("something broke")` with no category argument, meaning the default `"unknown"` is what the code produces.
- `engine/errors.py:78-83` — the fallback branch in `map_engine_error` is the only place that handles `category="unknown"`; none of the `if category == "auth|rate_limit|server"` branches matches it.

If the fallback branch is deleted, every `ProviderError("...")` call without an explicit category flows through to... nowhere. The `if/elif` ladder at `errors.py:60-77` would fall off the end and return whatever the outer function returns for unmatched exceptions, which changes the error surface for library consumers using the default.

The branch is reachable by construction, reachable in tests, reachable in production via `engine/auth.py:193, 243, 295, 304, 377, 431, 500, 536, 576, 584, 628, 659` (where `ProviderError(...)` is raised — I haven't checked every one, but the pattern is the same: callers use the `category` kwarg some of the time and not others).

**Verdict:** The branch is neither "defensive coding" (which implies it protects against an unusual condition) nor "dead code" (which implies it is unreachable). It is **primary-path code for the default argument value.** SDET was closer than I was; the accurate label is neither of the two they offered, but SDET's "keep it" conclusion is 100% correct and my "delete it" conclusion was wrong.

### Q3: Is the ideal final state "10 of your fixes + 5 of SDET's" or "10 of your fixes + 9 of SDET's"?

**Neither — the ideal final state is closer to "10 of mine + 30+ of SDET's."**

My original synthesis (cross-review §9) listed 10 items, 5 from me and 5 from SDET. That was already too stingy on the SDET's side. After re-reading with the concessions above, the realistic combined P0 + P1 list is:

- **10-ish of my type fixes** (literal conversions, Pydantic-izing dict returns, splitting log_usage, `_preset_cache` threading, `_FALLBACK_DISPATCH` typing, dependency-injecting `load_template`, adding `EngineEvent` discriminator, typing cleanups in `engine/phases.py`, moving `_make_config` to conftest, `parse_synthesis` totality refactor).
- **25-30 of SDET's behavioral fixes** across §1.1 (weak assertions), §1.2 (`pytest.raises(Exception)`), §1.4 (schema round-trip), §2.1 (edge cases), §3.1 (match= tightenings), §4.1 (parametrization), §5 (branch coverage gaps), §6 (isolation), §7 (mocking hygiene), §8 (naming).

Total in the neighborhood of 35-40 items, with the caveat that several SDET items become *easier or more focused* after the corresponding type fix lands (exact-value assertions are cleaner against Pydantic models; `match=` tightenings pair with `Literal` for maximum leverage).

**The disagreement between us is about which items sit at P0.** I would still rank my type fixes higher than the SDET does — not because they eliminate tests, but because they prevent future bugs at construction time, and because they unlock the more specific `match=` message assertions SDET recommends. But that's a priority dispute, not a validity dispute. Every one of SDET's findings is valid and should land.

### Q4: Where is the line between "the type IS the test" and "the type needs a test"?

This is the clearest axis to restate, now that I've been forced to be precise about it.

**"The type IS the test"** applies when:
1. The test's entire body is checking *shape* — key presence, instance check, "is this a string," length of a list of known structure.
2. The test would still pass under *any* valid value of the correct type — i.e., the test does not pin a specific output for specific input.
3. The test exists only because the current type is too loose (`dict[str, Any]`, `object`, raw `str`).

Under all three conditions, the type fix makes the test's assertions tautological, and the test body shrinks to zero or to a construction-time validation of the underlying data. Example: SDET §4.1 "`PROVIDER_MODEL_OPTIONS` rows all have four keys" — that becomes import-time Pydantic validation under my `ModelOption(BaseModel)` fix. The test is eliminated.

**"The type needs a test"** applies when:
1. The test makes a specific *value* claim — arithmetic, string equality to a known literal, exact structure mapping.
2. The test distinguishes *which* of several type-valid runtime behaviors occurs — e.g., "for this input the function chooses to omit this `NotRequired` key."
3. The test exercises a control-flow branch — any `if/elif/else`, any `match`, any early return.
4. The test verifies that error **messages** are actionable and user-facing (SDET §3.1 `match=` pattern).
5. The test verifies ordering, emission, or protocol semantics (events, JSONL lines, file writes).

Under any of these five conditions, no type system in Python can replace the test. Most of the SDET's findings fall into (1), (3), (4), and (5).

**My original review's mistake was misclassifying tests from the second category into the first.** Specifically:
- `test_engine_core.py:731-738` phases-dict assertion — I said "the type eliminates it." It doesn't (category 2).
- `test_engine_core.py:770-778` `estimate_cost_usd` result dereferencing — I said "the type eliminates it." The type eliminates the *key-presence* subset only; the value-correctness assertions remain (category 1 for part, category 1-subset for other parts).
- `test_engine_core.py:131-135` ProviderError mystery category — I said "the type makes it unreachable." Completely wrong (the branch is reachable by default argument value, not unreachable under any refactor that respects the public API).

The line is not fuzzy — once you ask "what claim does this test body actually make?" the line is sharp. My original review didn't ask that question carefully enough for several findings.

---

## 5. Revised prioritized action list

This is the updated list, replacing the one in my original review §10 and cross-review §6. Items marked ★ are new or significantly revised relative to round 1.

### Priority 0 (land first, gate subsequent work)

1. **Convert string enums to `Literal` / enum types** — `phase`, `mode`, `stagnation`, `provider`, `termination_reason` across `engine/events.py`, `engine/config.py`, `engine/models.py`, `engine/phases.py`. (`category` on `WebError` also; `category` on `ProviderError` **deferred** — see ★ below.)

2. **Replace all `pytest.raises(Exception)` with `pytest.raises(ValidationError, match=...)`** — 6 sites. (SDET §1.2, my §2. Convergent finding, highest confidence.)

3. **Thread `_preset_cache` as a parameter, delete `setup_method` calls** — enables `pytest-xdist` parallelism. (SDET §6.1 and my §4, convergent.)

4. ★ **Replace weak `>=` / `> 0` / `>= 1` assertions with exact values on deterministic fixtures** — SDET §1.1 list in full. This was on my original list but misframed as "enabled by" my type fix. It's **independent** of my type fix and should land anyway.

5. **Replace `dict` returns in `engine/cost.py` with Pydantic models** (`CostEstimate`, `PhaseCounts` as TypedDict or model, `ModelOption`). This eliminates the key-presence subset of SDET §4.1 parametrization and enables cleaner assertions for SDET §1.1.

### Priority 1 (land with or shortly after P0)

6. **Add `match=...` to all unmatched `pytest.raises` sites** — SDET §3.1 list. Becomes *more* valuable after my `Literal` fix, not less (because the error message IS the contract).

7. **Split `log_usage()` into `build_usage_entry()` + `append_usage_entry()`**. Moves 10 of 12 tests in `test_linter_usage.py` into pure territory.

8. ★ **Add `dispute_count` / `session_id` / `version` / `timestamp` assertions to `test_linter_usage.py:192-195`** — SDET §1.4. My original position was "this test is testing the wrong thing; fix the schema with a Pydantic model." SDET is right that the test should exist *regardless* of the schema fix — the test verifies round-trip integrity, which is load-bearing.

9. **Parametrize `test_agent_name_regex_valid/_invalid`** — SDET §4.1. Orthogonal to type work.

10. **Parametrize `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` row-by-row** — after the `ModelOption(BaseModel)` lands, the shape checks collapse but the *value* checks (positive pricing, tier validity) remain and should parametrize for per-row failure reporting.

11. **Test empty `events=[]` in `StructuredDeliberation.from_events`** — SDET §2.1. Type-independent behavioral gap.

12. **Isolate `find_project_root` strategies via injection** — SDET §5.4 and my §1. Refactor + test each strategy in isolation.

### Priority 2 (land after P0/P1)

13. **Dependency-inject `load_template` at `run_pipeline` level** — eliminates monkey-patching at `test_engine_phases.py:1089`. My original recommendation.

14. **Add `EngineEvent` discriminator** (`type: Literal[...]`). Developer-ergonomics win; SDET correctly notes (cross-review §3.4) that it's a syntax change, not a test elimination.

15. **Refactor `parse_synthesis` to be total over all strings**, enabling deletion of `engine/models.py:159` except branch. *If refactor is rejected*, fall back to SDET §5.5 and add the missing except-branch test.

16. **Unify dispute-heading detection as a `frozenset[str]`** (see my cross-review §5.4). Parametrizes SDET §2.1 gap over all 8+ headings.

17. **Add frozen / required-field / coercion-failure tests** for `DisputeInfo`, `DisagreementResult`, `AttributionResult`, `QualityResult`, `UsageEntry`, `AdoptionMetrics`, `SynthesisMeta`, and any new Pydantic models introduced by P0 items. (My §2 gap list.)

18. **Test-name hygiene pass** — rename `test_minimal`, `test_defaults`, `test_frozen`, `test_empty` to behavior-describing names. (SDET §8 in full; I abdicated on this in round 1.)

19. **`_FALLBACK_DISPATCH: dict[str, FallbackFn]`** — eliminates `# type: ignore` at `linter/quality.py:471`.

20. **`linter/usage.py` read path uses `UsageEntry.model_validate_json`** — eliminates the `.get()` fallback chain on load.

### Deferred / rejected from my original list

- ★ **DROP: "delete `engine/errors.py:79-83` fallback branch."** Wrong. The branch is load-bearing for `ProviderError`'s default category value. Keep the branch; keep the test.
- ★ **DROP: "`Literal` on `ProviderError.category`."** `ProviderError` is a plain `Exception` subclass with a `str` default of `"unknown"`. Tightening to `Literal` would either require making the class a Pydantic model (larger refactor) or would be lint-only (runtime default still lands in the fallback branch). Either way, the test at `test_engine_core.py:131-135` survives. I'm removing this from my recommendations list.
- ★ **REVISE: "`NotRequired[int]` for arbitration makes the test statically eliminable."** The test is not eliminable. The TypedDict fix has value for attribute access and refactoring safety, but it does *not* reduce test count.
- ★ **MODERATE: "Pydantic-izing `estimate_cost_usd` collapses the weak-assertion findings."** It collapses the shape-check subset only. The arithmetic-value subset remains and should be tightened independently per SDET §1.1.

### Additions from SDET that I'm now adopting

- ★ **ADD: Parser-layer ConfigError regression tests** — after `Literal[...]` lands on `mode`/`stagnation`/`provider`, the parser's user-facing error messages need `match=` regression tests to prevent degradation. (SDET §3.1 implicit; explicit in their cross-review §5.4.)
- ★ **ADD: Rename `test_provider_error_unknown_category` and use the default constructor.** Narrower version of my originally-wrong deletion recommendation. Ties the test to the documented default value, not an arbitrary typo string.
- ★ **ADD: `_FALLBACK_DISPATCH` callable type alias** — SDET caught this at §2.4.
- ★ **ADD: strategy-isolation for `find_project_root`** — SDET §5.4 is sharper than my original §1 coupling finding; I adopt theirs.
- ★ **ADD: deterministic-count tightening at `test_linter_quality.py:170, 181, 281, 326, 361` and `test_linter_output_contract.py:180`** — I missed these entirely in round 1. Full credit to SDET §1.1.
- ★ **ADD: `_count_challenges` combined-path coverage gap** — SDET §5.10, I missed.
- ★ **ADD: `build_disputes_context` iteration=2 off-by-one** — SDET §5.8, I missed.
- ★ **ADD: `_has_alternatives` single-letter / whitespace edge cases** — SDET §2.1, I missed.

---

## 6. Remaining substantive disputes for arbiter (if any)

After concessions, the disputes that remain are priority disputes, not validity disputes. The SDET and I both accept the other's findings; we disagree on ordering:

1. **Scope of `StrictInt` / `StrictBool` adoption on `EngineConfig`.** I recommend yes (for top-level fields `rounds`, `iterations`, `validate_templates`). SDET is agnostic. This determines whether SDET's "`rounds: 1.5` float" and "`validate_templates: 'true'` string" tests land immediately (current world) or are replaced by property-based "any non-int rejects" tests (post-`StrictInt` world). I prefer the latter; SDET prefers the former. Both are defensible. **Arbiter decision: is `StrictInt` adoption in scope for this cycle?**

2. **Priority of `EngineEvent` discriminator refactor.** I put it at P2; the SDET doesn't weigh in. Under my ordering it ships after the core type fixes. Low stakes.

3. **Priority of `parse_synthesis` totality refactor.** I put it at P2 behind "if refactor is rejected, add the SDET's except-branch test." SDET would prefer the test unconditionally. This is the one remaining validity-flavored dispute, and I'd concede it if the arbiter rules. (The refactor is nice but non-essential; the test is strictly safer.)

4. **Hypothesis vs parametrize for `MODEL_PRICING` / cost linearity.** I'd add Hypothesis for the algebraic law at `test_engine_core.py:818-822`. SDET is silent. Both work.

No item from the SDET's round 1 review is being rejected in this revision. **All of the SDET's findings land; I am correcting my over-claims about which ones are obsoleted by type fixes.**

---

## 7. Closing

The SDET's pushback was correct on all three contested points. The root cause of my overclaim was a conflation of "the type system encodes the contract" with "the test body verifies the output" — those are different jobs, and in the overwhelming majority of the SDET's findings, the behavioral test is doing work the type system cannot do. My original review was correct about *which fixes to land* and overclaimed about *how many tests collapse under them*. The revision above corrects the overclaim.

If the arbiter has to rule, the remaining disputes are narrow ordering questions, not validity questions. The combined action list has grown — not shrunk — relative to my round 1 position. Both lenses contribute irreducibly.

**End of revision (Round 1 → 2).**
