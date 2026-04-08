# SDET Revision — Round 1 (post cross-review)

**Author:** SDET agent
**Round:** 1 revision of 2 (cooperative deliberation)
**Prior documents:**
- Original review: `/Users/business-daddy/code/payer-index-mono/conversus/specs/045-test-coverage-review/conversus-output/sdet-agent/review.md`
- FP-guru review: `/Users/business-daddy/code/payer-index-mono/conversus/specs/045-test-coverage-review/conversus-output/functional-programming-guru/review.md`
- My cross-review of FP-guru: `/Users/business-daddy/code/payer-index-mono/conversus/specs/045-test-coverage-review/conversus-output/sdet-agent/cross-reviews/functional-programming-guru.md`
- FP-guru's cross-review of me: `/Users/business-daddy/code/payer-index-mono/conversus/specs/045-test-coverage-review/conversus-output/functional-programming-guru/cross-reviews/sdet-agent.md`

**Date:** 2026-04-03

---

## 0. Summary of my revised position

The FP-guru's pushback clarified two real wins, one genuine concession, and one factual error that needs to be corrected for the arbiter. Specifically:

1. **Hold firm:** types and behavioral assertions are orthogonal. The guru's P0 does not eliminate my P0.
2. **Concede (narrow):** three specific tests from my P1/P2 list become redundant or simpler under the guru's type fixes. I enumerate them in §2 with the exact form of the simplification.
3. **Push back hard:** `engine/errors.py:79-83` is **not** dead code. I verified in production source — `engine/providers/anthropic.py:89, 124` and `engine/providers/openai.py:62, 99` raise `ProviderError(..., category="unknown")` on the generic `APIError` path. The fallback branch fires on every real anthropic/openai SDK error that isn't auth/rate-limit/server-status-code. The guru's proposed `Literal["auth", "rate_limit", "server"]` would **break production code** by making those existing call sites unconstructible. The test at `test_engine_core.py:131` should stay; so should the branch.
4. **Partial concede:** `engine/models.py:159` — the explicit `ValueError` branch is unreachable from this caller because of the `if synthesis_text.strip():` guard. But the broad `except Exception` is still defending against regex / helper errors in downstream extraction functions inside `parse_synthesis`. So "delete it" is too strong; "narrow the except and document the real failure surface" is the correct fix.
5. **Sequencing:** merge order matters for **efficiency**, not correctness. Doing types first avoids writing tests that will immediately be deleted. But doing it in the other order still produces the correct final state — it just wastes one commit's worth of work.

The rest of this document answers the arbiter's four explicit questions, one by one, with source citations.

---

## 1. Which specific tests from my P0/P1 list become redundant under Literal / StrictInt / conint type fixes?

I walk through every P0 and P1 item individually. For each I state: **(a)** whether the guru's type fix eliminates the test, **(b)** if eliminated, whether the *case* disappears or whether it just becomes a different test shape, and **(c)** whether a new test obligation replaces it.

### P0-1: Replace `pytest.raises(Exception)` with `pytest.raises(ValidationError, match=...)` at 6 sites

- **Fix status:** **not redundant.** Independent of any type change in source. This is a test-side tightening.
- **Guru's stance:** agrees; this was a convergence item in both cross-reviews.
- **Verdict:** P0 remains as written.

### P0-2: Test empty `events=[]` in `StructuredDeliberation.from_events`

- **Fix status:** **not redundant.** The type system cannot compute arithmetic. `sum(1 for ev in events if isinstance(ev, PhaseCompleted) and ev.phase == "review") == 0 → rounds_completed = 1` is a runtime branch, not a type constraint. Types say "events is a list"; behavior asks "what happens when the list is empty?"
- **Verdict:** P0 remains.

### P0-3: Isolate strategies 2 and 3 in `engine/_root.py:find_project_root`

- **Fix status:** **not redundant.** Branch isolation is a control-flow concern. The four strategies are sequential `try: / except:` fallbacks — no type change helps.
- **Verdict:** P0 remains.

### P0-4: `models.py:159` untested `except Exception` branch

- **Fix status:** **partially addressed, not redundant.**
- **Finding after verification:** `parse_synthesis` (defined at `linter/output_contract.py:332`) only explicitly raises `ValueError` — and only on empty input. The caller at `engine/models.py:154` already guards with `if synthesis_text.strip():`, so the explicit `ValueError` path is unreachable from this caller. The guru is right about that narrow claim.
- **But:** `parse_synthesis` internally calls `_extract_agent_count`, `_extract_mode`, `_extract_phases_completed`, `_extract_cross_reviews_performed`, `check_disagreement`, `_extract_resolved_contradictions_count`, `_extract_headline`, `_extract_convergence_count`. Any of these could raise `AttributeError`, `IndexError`, or `re.error` on pathological input. The broad `except Exception` catches those. It is **not** dead code; it is **best-effort defense against downstream helper failures**.
- **Correct fix:** narrow the except to `except (ValueError, AttributeError, IndexError, re.error)` and add a test that constructs a synthesis text which makes one of the helpers raise. The guru's "delete" recommendation is too aggressive; my "test the branch" recommendation is correct but should be paired with the narrowing fix from the guru's lens.
- **Verdict:** P0 stays but reframes as "narrow the except clause and add one regression test exercising a helper-function failure mode." This is a compromise that takes both insights.

### P0-5: `engine/phases.py:661` prior_arbitration_path branch

- **Fix status:** **not redundant; still undetermined.** The current test docstring admits it's "effectively dead code," which is a test-suite smell regardless of the type system. No type change affects this.
- **Verdict:** P0 remains — but the action item is "decide: delete the code or write a test that actually reaches it," not "add a test."

**P0 summary: 5 of 5 items remain. Zero eliminated.**

### P1-6: Replace `>=` / `>` with exact values on deterministic fixtures

- **Fix status:** **not redundant, possibly easier.** Arithmetic correctness is not a type concern. The guru explicitly conceded this in their cross-review (`sdet-agent.md:65-68`): "I reviewed these files and did not flag them. This is a legitimate blind spot in a type-systems review."
- One nuance: for `assert result["estimated_usd"] >= 0` at `test_engine_core.py:776`, if the return becomes a Pydantic `CostEstimate` model, the assertion becomes `result.estimated_usd == pytest.approx(0.0042)` — which is cleaner syntax but the same test with the same arithmetic assertion. **The case doesn't disappear; the syntax gets better.**
- **Verdict:** P1 remains.

### P1-7: Add `match=` substring to `pytest.raises` at 9 sites

- **Fix status:** **not redundant, more valuable after type fixes.** After `phase: Literal[...]` / `mode: Literal[...]` etc. land, the error messages become the main user-facing contract. Matching the message is exactly what prevents regressions where the text degrades from "mode must be one of [...]" to "validation error at index 0".
- **Verdict:** P1 remains with stronger motivation.

### P1-8: Parametrize `test_agent_name_regex_valid` / `_invalid`

- **Fix status:** **not redundant.** Parametrization is a reporting concern, independent of types.
- **Verdict:** P1 remains.

### P1-9: Parametrize `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` row-by-row

- **Fix status:** **partially redundant.**
- If `PROVIDER_MODEL_OPTIONS` becomes `dict[str, list[ModelOption]]` where `ModelOption` is a Pydantic `BaseModel` with fields `id: str, name: str, tier: Literal["default", "premium", "budget"], description: str`, then:
  - The "each row has all four keys" assertion becomes enforced at **import time** when the constant is defined. If a row is missing `tier`, Python fails to import the module. **No test needed for shape.**
  - The "tier is one of three valid values" assertion becomes enforced at import time via `Literal`. **No test needed for tier validity.**
- **What remains:** a parametrized test that asserts **business invariants** — e.g., "every provider has at least one model with `tier == 'default'`." This is not the same as the current row-by-row shape check.
- **Verdict:** test count drops from ~12 (one per row × 3 providers) to 1 property test after the guru's fix. **Genuine simplification.** I concede this one. This is the test-count win the guru claimed — but note that it's a simplification of a P1 item, not an elimination of a P0 item.

**P1 summary: 3 of 4 items remain. 1 simplified (not eliminated — the test still exists, it's just shorter).**

### P2 items — running through the guru's claim of "5-7 become redundant"

The guru's cross-review says approximately 5-7 of my recommendations become redundant after type fixes. Let me enumerate P2 items one by one and count honestly.

**P2-a: `rounds: 1.5` float coercion test (review.md:89)**
- **Fix status:** **simplified, not eliminated.**
- Under `rounds: StrictInt` in `EngineConfig`, Pydantic rejects `1.5` at model construction. But that doesn't mean the test disappears — it means the test becomes `"rounds: 1.5" in YAML → parse_config → ValidationError, match="int"`. **The test case still runs, asserting the same observable behavior through a different failure mechanism.**
- New obligation the type fix creates: a one-time "StrictInt is wired up correctly" test to prove the strict mode is actually enabled.
- **Net:** 1 test becomes 1 (possibly shorter) test. Not a count reduction.

**P2-b: `validate_templates: "true"` string coercion test (review.md:247)**
- **Fix status:** **simplified, not eliminated.**
- Under `validate_templates: StrictBool`, Pydantic rejects `"true"`. The test becomes "StrictBool refuses string" — same test, different failure mechanism. Test case still exists.
- **Net:** 1 → 1. Not a reduction.

**P2-c: `validate_templates: 1` int-to-bool coercion test**
- **Fix status:** **genuinely redundant with P2-b** if we adopt StrictBool, because StrictBool rejects *any* non-bool, so one test covers the whole space. **One test case eliminated.**
- **Net:** 1 → 0. **Legitimate elimination.**

**P2-d: `ProviderError` with `category=None` edge case (review.md:72)**
- **Fix status:** **would be eliminated IF the type fix were valid.** But the type fix is not valid — see §3 below. `ProviderError.category` must remain `str` (or at best `Literal["auth", "rate_limit", "server", "unknown"]` including the `"unknown"` literal) because production providers raise with `category="unknown"` today. So the test stays.
- **Net:** 1 → 1. Not eliminated.

**P2-e: Negative `agent_count` in `estimate_cost_usd`**
- **Fix status:** **NOT eliminated by `conint(ge=0)`.** Critical correction.
- The guru's claim (`sdet-agent.md:195, line "conint(ge=0) makes test impossible"`) assumes `estimate_cost_usd` is a Pydantic model or wrapped in `@validate_call`. Neither is proposed. `estimate_cost_usd` is a plain function: `def estimate_cost_usd(agent_count: int, ...) -> dict:` at `engine/cost.py:106`. Python does not enforce type hints at runtime. A caller can pass `-1` today and will still be able to pass `-1` after you change the annotation to `conint(ge=0)` — unless you additionally wrap the function in `@pydantic.validate_call`, which nobody has proposed.
- **To actually eliminate this test,** the fix would be: (i) wrap `estimate_cost_usd` in `@pydantic.validate_call`, OR (ii) add a manual `if agent_count < 0: raise ValueError` guard and test *that*, OR (iii) promote the argument into a `CostInputs(BaseModel)` wrapper. None of these are in the guru's P0.
- **Net:** 1 → 1. The guru's claim here is factually wrong.

**P2-f: `iterations: 10000` large-number edge case (review.md:90)**
- **Fix status:** **simplified if `iterations: conint(ge=1, le=1000)` lands.** The vague "does a 10000-iter config parse?" becomes a sharp "1001 rejects, 1000 accepts" boundary test. The case count stays the same but the test becomes sharper.
- **Net:** 1 → 1 (with improved assertion).

**P2-g: Negative `iterations` for `estimate_cost_usd`**
- **Fix status:** **same as P2-e.** Type hint on a plain function does not eliminate the behavioral test.
- **Net:** 1 → 1.

**P2-h: `agent_count=0` synthesis-still-runs case**
- **Fix status:** **not redundant.** Zero is a valid input; the test asserts an arithmetic property (synthesis launches stay at 1). No type fix helps.
- **Net:** 1 → 1.

**P2-i: Unicode agent names (`"alice-β"`, `"Эмми"`)**
- **Fix status:** **not redundant.** The guru proposed replacing enumeration with a Hypothesis property test. That's a different test *shape*, not elimination — and it's a P3 test-style concern, not a P0 type concern.
- **Net:** 1 → 1.

**P2-j: Empty events list in `from_events` (this is actually P0-2 above, listed here for symmetry)**
- **Fix status:** **not redundant.** Type-independent arithmetic branch.

**P2-k: `_preset_cache` per-function injection**
- **Fix status:** **eliminated.** This is exactly the guru's P0 #6 ("thread `_preset_cache` through as a parameter"). Once the cache is injected, the three `setup_method` definitions at `test_engine_config.py:968, 1069, 1143, 1254` all delete. The isolation concern disappears entirely.
- **Net:** 4 setup_methods + 1 class-level concern → 0. **Legitimate elimination.**

**P2-l through P2-r (strategy-2 isolation, CONCESSION_AGENT regex, `_extract_headline` fall-through, iteration=2 off-by-one, `_count_challenges` combined case, singular-word vs plural-unit, whitespace-only classifier input)**
- **Fix status:** **none eliminated.** All are control-flow, regex, or data-flow concerns that no type change addresses.

**P2 summary (honest count):**
- **Eliminated outright:** 2 items — P2-c (int-to-bool redundant with StrictBool) and P2-k (`_preset_cache` injection).
- **Simplified but not eliminated:** 4 items — P2-a, P2-b, P2-f, and P1-9 (the one from the P1 list).
- **Guru overclaimed:** 2 items — P2-d (ProviderError unknown category, see §3) and P2-e/P2-g (plain-function agent_count/iterations, see above).
- **Untouched by types:** 11+ items.

**Total elimination: 2 test cases. Total simplification: 4 test cases. Total new test obligations created by the type fixes: approximately 6 (model-frozen tests, StrictInt/StrictBool wire-up tests, discriminated union dispatch test, parser-layer regression tests).**

**Net test count after both reviews: roughly unchanged. Test *quality* significantly improved.**

---

## 2. For each "becomes redundant" test — are you REMOVING the test case or just SIMPLIFYING its assertion?

Direct answer per item from §1:

| Item | Action | Details |
|---|---|---|
| P1-9 (row-by-row parametrize of MODEL_PRICING) | **Remove most cases** | From ~12 per-row tests (shape validation) down to 1 property test (business invariant: every provider has ≥1 `default`-tier model). The ~12 are replaced by import-time `Literal`/`BaseModel` enforcement. |
| P2-a (`rounds: 1.5`) | **Simplify assertion** | Test still exists, failure message changes from generic to `match="int"`. |
| P2-b (`validate_templates: "true"`) | **Simplify assertion** | Same. |
| P2-c (`validate_templates: 1`) | **Remove** | Redundant with P2-b under StrictBool. |
| P2-f (`iterations: 10000`) | **Simplify (sharper boundary)** | Test becomes `1001 rejects, 1000 accepts` — sharper than the vague original. Still a test. |
| P2-k (`_preset_cache` isolation) | **Remove 4 setup_methods** | Plus one concern in my §6.1. The test cases that *use* the cache still run, they just no longer need setup/teardown. |

**Of the 6 items touched, 2 are removals (P1-9 reduction and P2-c), 3 are simplifications (P2-a, P2-b, P2-f), and 1 is a fixture-level cleanup that removes scaffolding but not test cases (P2-k).**

Out of the ~30 concrete recommendations across P0/P1/P2 in my original review, that's a reduction of **~3 test cases removed entirely and ~3 simplified** — **not** the 5-7 redundancy count the guru asserted. The guru's count was inflated by double-counting `ProviderError` and by assuming plain-function type hints act as runtime guards.

---

## 3. Is `engine/errors.py:79-83` actually dead? Find one scenario in production code where it fires.

**No, it is not dead. The guru is factually wrong on this point. I have direct evidence.**

### Evidence 1: `ProviderError.__init__` default

From `engine/providers/__init__.py:41`:

```python
def __init__(self, message: str, *, category: str = "unknown", original: BaseException | None = None) -> None:
```

The category parameter **defaults to `"unknown"`**. The docstring at line 37 explicitly lists `"unknown"` as a valid value:

```
Attributes:
    category: One of ``"auth"``, ``"rate_limit"``, ``"server"``, ``"unknown"``.
```

`"unknown"` is **part of the declared API**, not a leaked sentinel.

### Evidence 2: Production call sites raising `category="unknown"`

From `engine/providers/anthropic.py:86-91`:

```python
except anthropic.APIError as exc:
    raise ProviderError(
        f"Anthropic API error: {exc}",
        category="unknown",
        original=exc,
    ) from exc
```

And at `anthropic.py:121-126`, the symmetric handler in the `stream()` method:

```python
except anthropic.APIError as exc:
    raise ProviderError(
        f"Anthropic API error: {exc}",
        category="unknown",
        original=exc,
    ) from exc
```

Same pattern in `engine/providers/openai.py` at lines 62 and 99 — the generic fallback when the exception is an `APIError` subclass that isn't one of the specific ones (`AuthenticationError`, `RateLimitError`, `APIStatusError`).

### Evidence 3: The fallback branch is literally the only path for these real errors

`map_engine_error()` at `engine/errors.py:58-83`:

```python
if isinstance(exc, ProviderError):
    category = getattr(exc, "category", "unknown")
    if category == "auth":   # only matches anthropic.AuthenticationError path
        ...
    if category == "rate_limit":   # only matches anthropic.RateLimitError path
        ...
    if category == "server":   # only matches anthropic.APIStatusError path
        ...
    # Fallback for unknown ProviderError categories
    return WebError(
        error=str(exc),
        category="provider_error",
        status_code=502,
    )
```

A `ProviderError` raised with `category="unknown"` (the default, and the value used for every generic `anthropic.APIError` or `openai.*` generic API failure) falls through all three `if` checks and hits lines 79-83. **Every single generic API error from either SDK flows through this branch in production.**

### Why the guru's type fix would break production

The guru proposed `category: Literal["auth", "rate_limit", "server"]`. If adopted:

1. `ProviderError.__init__` signature becomes incompatible with every `category="unknown"` call site — mypy fails, and if enforced at runtime via `@validate_call`, the runtime fails too.
2. The anthropic/openai generic `APIError` handlers lose their exception-wrapping path. They would have to either (a) pick one of the three categories at random, which is semantically wrong, or (b) leak the underlying SDK exception unwrapped, which defeats the purpose of `ProviderError`.
3. The `test_engine_core.py:131` test would be deleted — and with it, the last remaining safety net proving that the 502 fallback behaves correctly.

### Correct resolution

If we want the type system to help here, the right fix is:

```python
category: Literal["auth", "rate_limit", "server", "unknown"] = "unknown"
```

— which **includes** `"unknown"` as a valid literal. Under this, the `errors.py:79-83` branch is still reachable for `category="unknown"`, the test at `test_engine_core.py:131` still passes (though the test input changes from `"mystery"` to `"unknown"`), and `getattr(exc, "category", "unknown")` in `map_engine_error` can collapse to `exc.category` (one micro-improvement).

**Under this correct typing, the branch stays, the test stays, and my P2 recommendation to also test `category=None` / missing-attribute becomes obsolete (because the Literal forbids it). That's a legitimate single test elimination.** But the main test I flagged in my original review (`"mystery"` → 502 fallback) stays.

**Strong rebuttal delivered. The fallback branch is not dead code, and the guru's Literal-without-unknown recommendation would constitute a regression.**

---

## 4. Is the merge order (types → deletions → assertions) necessary for correctness, or just efficient?

**Necessary for efficiency; sufficient but not required for correctness.** Details:

### Correctness

The final state — after all fixes from both reviews land — is **identical** regardless of order. The target state is:

- Types tightened (guru's recommendations in §5a, §5b, §5d of their review).
- Narrow exception handlers (both of us).
- Exact-value assertions on deterministic fixtures (SDET §1.1).
- `match=` substrings on `pytest.raises` (SDET §3.1).
- Parametrization of table-driven tests (SDET §4.1).
- Missing edge-case tests (SDET §2.1).
- Frozen-model / required-field tests for every Pydantic model (guru §2 "Gaps").
- Splits: `log_usage` into pure + effectful halves (guru §2.5); `_preset_cache` injected (both).

No order produces a different final state. No ordering introduces or eliminates bugs that aren't also introduced/eliminated by another ordering. **Correctness is order-independent.**

### Efficiency

The **guru's claimed ordering (types first → delete unreachable → apply match= tightenings) is the efficient path** because it avoids writing tests that will immediately be deleted. Specifically:

1. If SDET tests land first (e.g., the `validate_templates: 1` test, the `rounds: 1.5` test), they will need to be deleted or rewritten once `StrictBool` / `StrictInt` lands, because the failure message changes. That's ~5 files of churn.
2. If types land first, those tests are never written in the "wrong" form — they are written directly against the strict-typed model. That's 0 files of churn.

### But the guru's ordering has a cost too

The guru's order **delays** the highest-value, lowest-risk fixes — the `pytest.raises(Exception) → pytest.raises(ValidationError)` tightening at 6 sites. Those 6 tightenings are:

- Independent of any type change.
- Zero risk.
- Immediately valuable (they stop swallowing unrelated runtime errors).
- Executable in a single PR with no other dependencies.

Landing those 6 tightenings first — before *any* type work — gives the next engineer who breaks a Pydantic constraint a sharp, informative failure instead of a mysterious `Exception` swallow. **Waiting for the type refactor to complete means 6 tests stay vague for the duration of the refactor.**

### My proposed ordering (compromise)

A three-phase plan that respects both concerns:

**Phase A (independent, land first, ~1 day):**
- A1. Replace `pytest.raises(Exception)` with `pytest.raises(ValidationError, match=...)` at the 6 sites. [SDET P0-1, Guru concurs]
- A2. Add `match=` substrings at the 9 `pytest.raises` sites in SDET P1-7 that are independent of type changes. [SDET P1-7]
- A3. Parametrize `test_agent_name_regex_valid/_invalid`. [SDET P1-8]
- A4. Rename `test_minimal`, `test_defaults`, etc. [SDET P3]
- A5. Fix `test_importlib_resources_fallback_path` name vs behavior drift. [SDET P3]

All of phase A is independent of the type refactor. Land it in a single PR.

**Phase B (type refactor, ~2-3 days):**
- B1. Convert `mode`, `stagnation`, `provider`, `phase`, `termination_reason` to `Literal` / `StrEnum`. [Guru P0-1]
- B2. Convert `ProviderError.category` to `Literal["auth", "rate_limit", "server", "unknown"]` — **including `"unknown"`**, see §3. [Corrected from Guru P0-1]
- B3. Add `PresetFile(BaseModel)`, `ModelOption(BaseModel)`, `CostEstimate(BaseModel)`. [Guru P0-2, P0-3]
- B4. Add `PhaseCounts(TypedDict)` with `NotRequired[int]` for arbitration. [Guru P0-2]
- B5. Thread `_preset_cache` as a parameter, delete the 4 `setup_method` blocks. [Guru P0-6, SDET P2-k]
- B6. Narrow `engine/models.py:159` `except Exception` to a specific tuple and document the helper failure surface. [Compromise between SDET P0-4 and Guru "delete it"]
- B7. Split `log_usage()` into pure + effectful halves. [Guru P0-4]

**Phase C (post-type test work, ~1-2 days):**
- C1. Add exact-value assertions on deterministic fixtures (now cleaner because of Pydantic models). [SDET P1-6, simplified form]
- C2. Add empty `events=[]` test for `StructuredDeliberation.from_events`. [SDET P0-2]
- C3. Add strategy-2 and strategy-3 isolation tests for `find_project_root`. [SDET P0-3]
- C4. Resolve `phases.py:661` prior_arbitration_path — delete code or add exercising test. [SDET P0-5]
- C5. Add frozen / required-field / coercion-failure tests for every new Pydantic model from B3. [Guru §2 Gaps]
- C6. Parser-layer regression tests for `ConfigError` messages after `Literal` conversion. [SDET argued this in cross-review §3.1]
- C7. Add the remaining edge cases (unicode agent names, whitespace-only classifier input, iteration=2 off-by-one, CONCESSION_AGENT `concedes` variant, `_extract_headline` fall-through). [SDET P2]
- C8. Parametrize `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` — now as 1 property test instead of 12 row tests. [SDET P1-9, simplified]

**Why this ordering is better than the guru's straight sequence:**

- Phase A delivers 15+ low-risk test improvements in ~1 day, *before* the type refactor. The engineering team gets immediate value.
- Phase B is the type refactor in isolation — reviewer can focus on type-system correctness without test-churn noise.
- Phase C is the post-refactor test cleanup, now able to write exact tests against typed models.

No tests are written in phase A that need deletion in phase B. No tests are written in phase C that duplicate phase A work. Every item is in the earliest phase where its dependencies are met.

**Answer to the arbiter's question: merge order affects efficiency, not correctness. The guru's proposed order is more efficient than writing tests first, but my three-phase decomposition is strictly better than both because it lands the ~15 independent wins immediately.**

---

## 5. Updated P0 / P1 list

Given everything above, my revised prioritization (with sequencing annotations):

### Revised P0 (correctness-impacting)

| # | Finding | Phase | Status vs original |
|---|---|---|---|
| P0-1 | Replace `pytest.raises(Exception)` → `ValidationError, match=...` at 6 sites | A | unchanged |
| P0-2 | Test empty `events=[]` in `StructuredDeliberation.from_events` | C | unchanged |
| P0-3 | Isolate strategies 2 and 3 in `find_project_root` | C | unchanged |
| P0-4 | Narrow `engine/models.py:159` except and add regression test for helper failures | B + C | **reframed** (was "test the except"; guru's lens improved it to "narrow + test") |
| P0-5 | Resolve `engine/phases.py:661` prior_arbitration_path — delete or test | C | unchanged |
| P0-6 | Convert `mode`, `stagnation`, `provider`, `phase`, `termination_reason` to `Literal` / `StrEnum` | B | **adopted from guru** |
| P0-7 | Convert `ProviderError.category` to `Literal[..., "unknown"]` (**including `"unknown"`**) | B | **adopted with correction from guru — §3** |
| P0-8 | Thread `_preset_cache` as parameter, delete 4 `setup_method` blocks | B | **adopted from guru** |
| P0-9 | Replace `engine/cost.py` dict returns with Pydantic models | B | **adopted from guru** |
| P0-10 | Add `PresetFile(BaseModel)` and stop using `dict[str, Any]` in preset parser | B | **adopted from guru** |
| P0-11 | Split `log_usage()` into pure + effectful | B | **adopted from guru** |

11 P0 items. Up from my original 5 P0 items and the guru's ~10. The net is larger because the type-safety items and the behavioral items are genuinely complementary — not substitutes.

### Revised P1 (weak assertions / parametrization / missing frozen tests)

| # | Finding | Phase | Status |
|---|---|---|---|
| P1-1 | Replace `>=` / `>` weak assertions with exact values on deterministic fixtures | C | unchanged |
| P1-2 | Add `match=` substrings at remaining `pytest.raises` sites | A | unchanged |
| P1-3 | Parametrize `test_agent_name_regex_valid/_invalid` | A | unchanged |
| P1-4 | Property test for `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` business invariants | C | **simplified from row-by-row — guru concession** |
| P1-5 | Add frozen + required-field + coercion-failure tests for each Pydantic model (guru §2 Gaps) | C | **adopted from guru** |
| P1-6 | Parser-layer regression tests for `ConfigError` messages after Literal conversion | C | **newly surfaced in my cross-review** |
| P1-7 | Discriminator field on `EngineEvent` with dispatch test | B + C | **adopted from guru (reduced scope: Phase B adds the field, Phase C adds the round-trip test)** |
| P1-8 | Promote `_make_config` / `_write_yaml` to `conftest.py` fixtures | A | **adopted from guru** |
| P1-9 | `StrictInt` / `StrictBool` on `EngineConfig` top-level fields + one wire-up test | B | **adopted from guru with single wire-up test; not per-field coercion tests** |

### P2 (edge cases / hygiene)

Unchanged from original review with these deletions/simplifications:

- **Delete:** `validate_templates: 1` int-to-bool test (redundant with StrictBool).
- **Delete:** `_preset_cache` isolation concern (eliminated by P0-8).
- **Simplify:** `rounds: 1.5`, `validate_templates: "true"`, `iterations: 10000` tests — failure messages change, cases stay.
- **Keep:** negative `agent_count`, negative `iterations`, unicode agent names, whitespace classifier input, `CONCESSION_AGENT` regex variant, `_extract_headline` fall-through, iteration=2 off-by-one, `_count_challenges` combined case. **None of these are eliminated by the type refactor.**

---

## 6. Final disagreements to escalate to the arbiter

1. **`engine/errors.py:79-83` is NOT dead code.** I have direct source evidence — `engine/providers/anthropic.py:89, 124` and `engine/providers/openai.py:62, 99` raise `ProviderError(..., category="unknown")` on the generic SDK API error path. The guru's "delete the branch" recommendation is **factually wrong and would regress production error handling**. If the arbiter adopts the Literal conversion for `ProviderError.category`, it **must** include `"unknown"` in the literal. The test at `test_engine_core.py:131` stays (with input changed from `"mystery"` to `"unknown"`). See §3 for the evidence chain.

2. **`engine/models.py:159` is NOT fully dead either — partial concession.** The explicit `ValueError` branch is unreachable from this caller because of the `if synthesis_text.strip():` guard. But the broad `Exception` catch is still defending against `AttributeError` / `IndexError` / `re.error` from downstream helpers in `parse_synthesis`. Correct fix: narrow to `except (AttributeError, IndexError, re.error, ValueError)` and add a regression test. The guru's "delete" is too aggressive.

3. **Plain-function type hints do not act as runtime guards.** The guru's claim that `conint(ge=0)` on `agent_count` in `estimate_cost_usd` makes the negative-integer test impossible is incorrect — `estimate_cost_usd` is a plain function, not a Pydantic model or `@validate_call` target. The test stays unless the function signature itself is refactored. See §1 item P2-e.

4. **Merge-order disagreement is about efficiency, not correctness.** Both my proposed three-phase decomposition (A → B → C) and the guru's linear order (types → deletions → assertions) reach the same final state. I argue phase A (the ~15 type-independent test improvements) should land first because they have zero dependencies and immediate value. The guru's strict types-first order unnecessarily delays low-risk wins by 2-3 days.

5. **Guru's claim of "5-7 tests become redundant" is inflated.** True count: **2 outright eliminations** (P2-c `validate_templates: 1` and P2-k `_preset_cache` setup), **4 simplifications** (same test case, cleaner assertion or sharper failure message), and **~6 new test obligations** created by the type fixes themselves. Net test count is roughly unchanged; test quality improves substantially.

6. **Concessions I owe the guru, for the record:**
   - `_make_config` / `_write_yaml` promotion to `conftest.py` — good catch I missed.
   - `log_usage` split into pure + effectful — architectural improvement I missed.
   - `_FALLBACK_DISPATCH: dict[str, FallbackFn]` type fix to remove the `type: ignore` — I missed this.
   - Untyped dict returns from `engine/cost.py` — I tested the functions extensively but didn't notice the weak return annotations.
   - `UsageEntry` model existing but unused on the read path of `linter/usage.py` — I missed this entirely.
   - Missing frozen / required-field tests on `DisputeInfo`, `DisagreementResult`, `AttributionResult`, `QualityResult`, `AdoptionMetrics`, `SynthesisMeta` — I missed the enumeration completeness.

---

## 7. One-line summary for the arbiter

**The guru's type fixes and my behavioral tests are orthogonal, not substitutes. Land phase A (15+ independent test improvements) immediately, phase B (type refactor with `"unknown"` preserved in the `ProviderError.category` literal) next, phase C (post-refactor tests now expressible against typed models) last. The fallback branch at `engine/errors.py:79-83` is live production code and the guru's "delete it" recommendation is factually wrong.**

---

## Appendix: source-citation verification log

Direct verifications performed for this revision:

1. `engine/errors.py:58-83` — read and confirmed the fallback branch structure.
2. `engine/providers/__init__.py:33-44` — confirmed `ProviderError.__init__` has `category: str = "unknown"` default.
3. `engine/providers/anthropic.py:86-91, 121-126` — confirmed two production call sites raising `category="unknown"`.
4. `engine/providers/openai.py:62, 99` — confirmed two more production call sites raising `category="unknown"`.
5. `linter/output_contract.py:332-354` — confirmed `parse_synthesis` only explicitly raises `ValueError` on empty input.
6. `engine/models.py:140-165` — confirmed the `if synthesis_text.strip():` guard and the `except (ValueError, Exception)` catch.
7. `engine/cost.py:70-108` — confirmed `estimate_cost` / `estimate_cost_usd` are plain functions with no Pydantic validation layer.
8. `tests/test_engine_core.py:125-135` — confirmed current `test_provider_error_unknown_category_maps_to_502` test.

All file paths absolute and verified as of 2026-04-03.

**End of SDET revision (Round 1).**
