# Disputes — functional-programming-guru

**Reviewer:** functional-programming-guru
**Round:** Post-revision disputes (Round 2)
**Peer:** sdet-agent
**Date:** 2026-04-03

---

## 0. Convergence status

**Substantially converged.** My revision conceded three major points (`errors.py:79-83` is not dead code; `NotRequired[int]` does not eliminate the phase-counts test; Pydantic-izing `estimate_cost_usd` does not close the exact-value assertion gap). The SDET's revision conceded six specific items to me (conftest promotion, `log_usage` split, `_FALLBACK_DISPATCH` typing, `cost.py` dict returns, `UsageEntry` unused on read path, missing frozen-model tests). On substantive validity we agree on every action item. The combined P0 list has grown, not shrunk. Both lenses contribute irreducibly.

**On the `errors.py:79-83` / `ProviderError.category` question specifically, we have fully converged** — my revision explicitly adopted the SDET's position *and* the SDET's revision independently proposed the same corrected formulation (`Literal["auth", "rate_limit", "server", "unknown"]` with `"unknown"` included). This is no longer a dispute; it is shared analysis arriving from opposite starting points.

The remaining disputes are **priority and sequencing disputes, not validity disputes**. They do not block merge. Every item from either review should land; we disagree only on the order and (in two narrow cases) on the shape of the implementation.

---

## 1. Remaining disputes

### Dispute 1: Merge order — types-first linear vs three-phase A/B/C

1. **Dispute**: Should independent test-side tightenings (pytest.raises → ValidationError, match= additions, parametrization renames, conftest promotion) land *before* the type refactor, or should the type refactor land first and the test tightenings follow?

2. **My position**: Land the type refactor (Literals, Pydantic models, `_preset_cache` threading, `log_usage` split) first at P0, then the behavioral tightenings at P1. My rationale: if the SDET's `rounds: 1.5` / `validate_templates: "true"` / per-row shape tests land first, they will need rewriting once `StrictInt` / `StrictBool` / `ModelOption(BaseModel)` land — that's unnecessary churn. The ordering in my revision §5 is P0 types, P1 tightenings-that-benefit-from-types, P2 discriminators and totality refactors.

3. **SDET's position** (revision §4 and §5.A/B/C): Three-phase decomposition. Phase A is ~15 test improvements that are fully independent of type work (six `pytest.raises(Exception) → ValidationError`, nine `match=` additions, regex parametrization, test-name hygiene, `_make_config` promotion to conftest) and should land in ~1 day *before* any type work begins. Phase B is the type refactor in isolation. Phase C is the post-refactor test cleanup against typed models. Rationale: Phase A has zero dependencies on the type refactor, zero risk, and immediate value — waiting 2-3 days for the refactor delays sharp failure messages that already could land today.

4. **Fact basis**: Both orderings reach the identical final state (SDET revision §4 "Correctness" subsection: "No order produces a different final state. Correctness is order-independent."). The efficiency argument cuts both ways:
   - **My direction**: If SDET tests ship first, the `rounds: 1.5` test currently asserts `pytest.raises(Exception, match="greater than")` and will need to re-assert against a Pydantic `StrictInt` error message after refactor — ~5 files of churn per SDET's own accounting.
   - **SDET's direction**: The six `pytest.raises(Exception) → ValidationError` tightenings are truly independent — they do not touch any field that changes type. They currently swallow *all* exceptions; tightening them to `ValidationError` adds no dependency on any downstream type refactor. Same for the nine `match=` additions at sites not governed by Literal fields.
   - **The two sets partially overlap**: the `pytest.raises` sites tied to `mode`/`stagnation`/`provider`/`phase` fields are entangled with the Literal refactor. The `pytest.raises` sites tied to independent validators (`agent_name`, `session_id`, `temperature` bounds) are not.

5. **Blocks merge?**: **No.** Both orderings produce the correct final state. This is a project-management preference, not a correctness question. The SDET's three-phase decomposition is arguably better engineering hygiene (immediate wins, isolated reviews), and I would accept it as the preferred path if the arbiter rules. My only operational caveat: Phase A should explicitly *exclude* the `pytest.raises` sites tied to fields that will become Literals in Phase B, so those don't churn. SDET's Phase A description already restricts itself to the six type-independent sites, so this caveat is likely moot.

---

### Dispute 2: `parse_synthesis` totality refactor vs narrowed except + regression test

1. **Dispute**: Should `parse_synthesis` be refactored to be a total function over all strings (making `engine/models.py:159`'s `except Exception` provably dead and deletable), or should the except clause be narrowed to a specific tuple (`except (ValueError, AttributeError, IndexError, re.error)`) with a regression test added for helper-function failure modes?

2. **My position** (revision §3.7 and §6 item 3): Prefer the totality refactor as the type-fix path — redesign `parse_synthesis` so every string input yields a `ParsedSynthesis` with well-defined defaults for missing fields, then delete the except clause entirely. Concede that if the refactor is rejected, the SDET's narrow-the-except approach is strictly correct and should land unconditionally. My revision explicitly says "If the refactor is rejected, fall back to SDET's position (add a test for the except branch). Do not claim the except is currently dead code."

3. **SDET's position** (revision §1 P0-4 and §6 item 2): Narrow the `except Exception` to `except (ValueError, AttributeError, IndexError, re.error)` and add a regression test that constructs a synthesis text which makes one of the internal helpers (`_extract_agent_count`, `_extract_mode`, `_extract_phases_completed`, `_extract_cross_reviews_performed`, `check_disagreement`, `_extract_resolved_contradictions_count`, `_extract_headline`, `_extract_convergence_count`) raise. The SDET frames the totality refactor as too aggressive because the broad `except` is currently serving a real purpose — defending against downstream helper errors.

4. **Fact basis**: From SDET revision §1 P0-4: `parse_synthesis` is defined at `linter/output_contract.py:332` and only explicitly raises `ValueError` on empty input. The caller at `engine/models.py:154` already guards with `if synthesis_text.strip():`, so the explicit `ValueError` path is unreachable from this caller. But `parse_synthesis` internally calls eight helper functions that can raise `AttributeError` / `IndexError` / `re.error` on pathological input. Those are the real failure modes the broad `except` catches.

   Both approaches are valid:
   - **Totality refactor**: Make each `_extract_*` helper return `Optional[T]` with a default, eliminate all internal raises from `parse_synthesis`, then the except clause becomes provably unreachable. Larger refactor, more files touched.
   - **Narrow + test**: Keep the current semi-partial design, tighten the except to a specific tuple, and add one regression test per helper failure mode. Smaller change, preserves current architecture.

5. **Blocks merge?**: **No.** These are two valid implementations of the same correctness goal. Under either approach, the observable behavior (failures in `parse_synthesis` produce a sentinel/fallback `SynthesisMeta` rather than crashing the engine) is preserved. I am willing to concede this to the SDET unconditionally — the narrow-and-test path is smaller, lower-risk, and lands sooner. My totality refactor can become a separate future spec if desired.

---

### Dispute 3: `StrictInt` / `StrictBool` adoption scope on `EngineConfig`

1. **Dispute**: Should `rounds`, `iterations`, `validate_templates` on `EngineConfig` be tightened to `StrictInt` / `StrictBool` (my position), or should they remain as-is with the behavioral tests covering float/string coercion staying as P2 items (SDET's implicit position — they neither advocated for nor against strict mode)?

2. **My position** (revision §6 item 1): Adopt `StrictInt` on `rounds` / `iterations` and `StrictBool` on `validate_templates`. This eliminates the "int-to-bool coercion" test outright (SDET P2-c) and simplifies the "float coercion" and "string-to-bool" tests to sharper boundary assertions. One new "wire-up" test proves strict mode is enabled; the rest become tighter.

3. **SDET's position** (revision §5 P1-9 and §1 P2-a/b/c): Agnostic but pragmatically adopts strict mode conditionally. Their revision accepted the StrictInt/StrictBool fix with a single wire-up test (not per-field coercion tests) in their P1-9. But their revision §1 P2-a/b also argues that `rounds: 1.5` and `validate_templates: "true"` tests are "simplified, not eliminated" — test case still exists, only the failure message changes. The ambiguity is whether "adopt StrictInt" is a source change they endorse or a source change they tolerate.

4. **Fact basis**: Both of us agree the test count change is small (2 tests eliminated under SDET's own count, ~4 simplified). The difference is whether strict mode is *worth* the one-time wire-up cost for the failure-message sharpness win. No code evidence resolves this — it is a taste question about strictness.

   From SDET revision §5, P1-9: "`StrictInt` / `StrictBool` on `EngineConfig` top-level fields + one wire-up test — adopted from guru with single wire-up test; not per-field coercion tests". That's actually endorsement, not agnosticism. Re-reading, the SDET has already conceded this in their revised P1. This may not be a live dispute.

5. **Blocks merge?**: **No.** Both of us end up endorsing `StrictInt` / `StrictBool` adoption in our revised lists. On re-reading the SDET's revision P1-9, I may have overstated the disagreement — the SDET already adopted my recommendation with a single-wire-up-test scope. I withdraw this as a dispute and mark it converged. **Leaving this entry in the disputes list for transparency, with the note that it resolved during write-up.**

---

## 2. Converged items (no longer disputed)

For the record, these were live disagreements in Round 1 that are now fully resolved:

- **`errors.py:79-83` status**: I was wrong; the branch is load-bearing for `ProviderError`'s default `category="unknown"` value. My revision §1.3 conceded this fully. The SDET's revision §3 independently verified the production call sites at `engine/providers/anthropic.py:86-91, 121-126` and `engine/providers/openai.py:62, 99`. Both of us now endorse `Literal["auth", "rate_limit", "server", "unknown"]` (with `"unknown"` included) as the corrected typing, and both of us endorse keeping the test at `test_engine_core.py:131` with the fixture string changed from `"mystery"` to `"unknown"`.

- **`NotRequired[int]` eliminating phase-counts test**: I was wrong; `NotRequired` widens rather than narrows the runtime value space. Test stays. Revision §1.1.

- **Pydantic-izing `estimate_cost_usd` eliminating weak-assertion tests**: I was half-wrong; the Pydantic fix collapses the key-presence subset of assertions but not the arithmetic-value subset. Both parts of the fix must land independently. Revision §1.2.

- **`_preset_cache` threading**: SDET conceded (cross-review §1.2) this is the better fix than per-test setup/teardown. My recommendation holds and lands as P0.

- **`log_usage` split into pure builder + effectful appender**: SDET conceded (cross-review §2.5) this is "strictly better than anything I proposed." Holds as P0.

- **`_FALLBACK_DISPATCH: dict[str, FallbackFn]` type alias**: SDET conceded (cross-review §2.4) they missed this. Holds.

- **`linter/usage.py` read path using `UsageEntry.model_validate_json`**: SDET conceded (cross-review §2.2). Holds.

- **Missing frozen / required-field / coercion-failure tests** for `DisputeInfo`, `DisagreementResult`, `AttributionResult`, `QualityResult`, `UsageEntry`, `AdoptionMetrics`, `SynthesisMeta`: SDET conceded (revision §6 item 6) they missed the enumeration completeness. Holds.

- **`_make_config` / `_write_yaml` promotion to `conftest.py`**: SDET conceded (revision §6 item 6). Lands in Phase A.

- **Untyped dict returns from `engine/cost.py`**: SDET conceded (revision §6 item 6). Lands in Phase B as P0.

- **`EngineEvent` discriminator field**: Both of us endorse adding `type: Literal[...]` for discriminated-union dispatch. SDET accepts (P1-7 in their revised list) at lower priority than me, but both agree it should land. Not disputed on validity.

- **Dependency-injecting `load_template` at `run_pipeline` level**: Neither contested. Lands as P2.

- **Test-name hygiene pass** (renaming `test_minimal`, `test_defaults`, `test_frozen`, `test_empty`): I abdicated on this in Round 1; SDET kept it as P3; my revision §5 item 18 adopted it. Lands.

- **SDET's exact-value assertion replacements** (`>=` → `pytest.approx`): I originally framed these as enabled-by my type fix. Now I recognize they are independent and should land anyway. Revision §5 item 4. No dispute.

---

## 3. New findings discovered during revision

These are items I surfaced while writing my revision that were not in either Round 1 review. They are additive; neither of us has had a chance to cross-examine them yet.

### New finding A: `ProviderError`'s default `category="unknown"` is a first-class sanctioned value, not a sentinel

While tracing the `errors.py:79-83` dispute, I discovered that the `ProviderError` docstring at `engine/providers/__init__.py:37` explicitly lists `"unknown"` in the canonical category enumeration. This is stronger than "it's the default fallback" — it's documented API surface. Any refactor that tightens the category type must preserve `"unknown"` as a first-class literal value, not treat it as a typo-catch. The SDET's independent verification of the production call sites at `anthropic.py:86-91, 121-126` and `openai.py:62, 99` confirms this — the SDKs' generic `APIError` paths *require* `"unknown"` as a live category value. **Action**: the `Literal["auth", "rate_limit", "server", "unknown"]` formulation that both of us converged on is the only correct typing.

### New finding B: The test at `test_engine_providers.py:80` already exercises the default-category constructor

I noticed during the revision write-up that `tests/test_engine_providers.py:80` does `err = ProviderError("something broke")` with no category kwarg. This is a live test that exercises the default path — meaning the test at `test_engine_core.py:131` is not the *only* test touching the default-category branch, just the one that most clearly ties it to the 502-mapping contract. **Action**: when we rename the test to `test_provider_error_unknown_category_maps_to_502`, we should cross-reference `test_engine_providers.py:80` so future maintainers know both tests exist and serve different purposes.

### New finding C: `parse_synthesis` internal helper enumeration is larger than the Round 1 reviews indicated

The SDET's revision §1 P0-4 enumerates eight internal helpers called from `parse_synthesis`: `_extract_agent_count`, `_extract_mode`, `_extract_phases_completed`, `_extract_cross_reviews_performed`, `check_disagreement`, `_extract_resolved_contradictions_count`, `_extract_headline`, `_extract_convergence_count`. My Round 1 review treated `parse_synthesis` as a small function with one or two failure modes. In fact there are at least eight distinct helper failure modes, each of which could produce a different exception type. **This strengthens the SDET's "narrow the except to a specific tuple" recommendation over my "totality refactor" recommendation**, because a totality refactor would need to touch all eight helpers — a much larger surface than I originally scoped. **Action**: defer the totality refactor to a future spec; adopt the SDET's narrow-and-test approach for this cycle.

### New finding D: The test count math in my Round 1 review was inflated

Re-counting after the concessions: of the ~10 implicit "this test becomes unnecessary" claims in my Round 1 review, only **2-3 hold up** (P2-c `validate_templates: 1` under StrictBool, the key-presence subset of `test_engine_core.py:846-852`, and the per-row tier-validity checks that collapse under `Literal`). The other 7-8 shrink test bodies (removing shape checks, replacing `.get("k", default)` with `.k`) but do not eliminate tests. **Net test count after both reviews is roughly equal to or slightly higher than today**, not lower as my Round 1 implied. Test *quality* improves sharply; test *count* stays flat. SDET's revision §1 independently reached the same count (2 eliminations, 4 simplifications, ~6 new obligations). **Action**: update any stakeholder communication that anchored on "type fixes reduce test count" — the correct framing is "type fixes reduce test *brittleness* and catch bugs at construction rather than assertion."

### New finding E: The correct typing for `ProviderError.category` is arguably a `StrEnum`, not a `Literal`

A subtle point I didn't raise in the revision: `Literal["auth", "rate_limit", "server", "unknown"]` is fine for type-checker purposes but provides no runtime enforcement on a plain `Exception` subclass. If we want the default-value handling and the category-comparison logic in `errors.py:60-83` to be refactor-safe, a `StrEnum` (Python 3.11+) with members `AUTH`, `RATE_LIMIT`, `SERVER`, `UNKNOWN` gives us: (a) `IDE auto-complete on category comparisons`, (b) `mypy exhaustiveness checking on the if/elif ladder`, (c) `runtime membership checks via isinstance`, and (d) `string equality comparisons that still work for backward compatibility`. This is a strictly stronger fix than the `Literal` both of us endorsed. **Action**: flag as a possible Phase B enhancement; not a dispute, just a strengthening. I'd defer to the SDET's preference here since they did the production-call-site verification.

### New finding F: `engine/phases.py:70` `termination_reason: str | None` has an inline comment listing valid values

This is a minor Round 2 find: the Round 1 reviews both noted that `termination_reason` is `str | None` but neither of us pulled the actual string. It's documented inline in the source as `# One of: "converged", "max_iterations", "cost_cap", "error"`. This is an even stronger argument for `Literal` conversion than I made in Round 1 — the values are *already* documented, just not enforced. A mechanical Literal conversion has zero risk here because the intended value set is already specified in-place. **Action**: this should be the easiest Literal conversion on the list; include it in Phase B as the lowest-risk change.

---

## 4. Summary for arbiter

Three disputes remain, **none of which block merge**:

| # | Dispute | Type | Blocks merge? | My willingness to concede |
|---|---|---|---|---|
| 1 | Merge order: linear types-first vs three-phase A/B/C | Sequencing | No | Willing — SDET's three-phase is arguably better engineering hygiene |
| 2 | `parse_synthesis` totality refactor vs narrow-except + test | Implementation shape | No | Willing — totality refactor is larger than I initially scoped (see New Finding C) |
| 3 | `StrictInt`/`StrictBool` adoption scope | Already converged during write-up | No | Already converged |

Dispute 3 resolved while writing this document (SDET revision P1-9 already adopts my recommendation). Disputes 1 and 2 are priority/shape questions where both approaches reach the identical final state — the arbiter can rule either way without loss of correctness.

**On validity, there is 100% convergence.** Every finding from both Round 1 reviews lands in the combined action list (with the single exception of my originally-wrong "delete `errors.py:79-83`" recommendation, which I retract entirely). The SDET's Round 1 findings all stand. My Round 1 findings all stand except for the three overclaims I conceded in revision §1.

**Recommended arbiter decision**: Adopt SDET's three-phase sequencing (Phase A immediate wins, Phase B type refactor, Phase C post-refactor tests) with my type-refactor content, plus the `"unknown"`-inclusive `ProviderError.category` Literal formulation both of us independently converged on. Defer the `parse_synthesis` totality refactor to a future spec; land SDET's narrow-and-test approach now.

**End of disputes document.**
