# Test Coverage Review — Synthesis (Final)

**Spec:** 045-test-coverage-review
**Agents:** functional-programming-guru, sdet-agent
**Rounds:** review → cross-review → revision → disputes
**Date:** 2026-04-03
**Arbiter:** Not required — deliberation converged on source-code evidence

---

## 1. Executive Summary

**Verdict: Ready to ship, with a structured follow-up plan.**

The engine/ and linter/ test suite is in a strong, mergeable state. Total line coverage on the targeted modules now exceeds the 90% success criterion (engine/config 100%, engine/phases 99.72%, linter 97%), and the deliberation did not surface a single correctness-blocking gap. The ~565 new tests across 13 files are, on balance, behaviorally meaningful and architecturally sound.

**Findings accepted:** approximately 35–40 actionable items, split across three phases. Zero validity disputes remain after revision; the only open questions are sequencing and aesthetic choices, none of which block merge.

**Key insight from the deliberation:** the cooperative exchange resolved a real, load-bearing disagreement through direct source-code evidence. FP-guru initially claimed `engine/errors.py:79-83` was dead code that should be deleted once `ProviderError.category` became a `Literal`. SDET pushed back with a complete evidence chain — `engine/providers/__init__.py:41` (default value `"unknown"`), `engine/providers/anthropic.py:86-91, 121-126`, `engine/providers/openai.py:62, 99` — showing the branch is the primary-path handler for every generic SDK API error raised with the documented default category. FP-guru examined the cited code, wrote "I was wrong," and retracted the deletion recommendation in revision §1.3. Both agents independently converged on the corrected formulation: `Literal["auth", "rate_limit", "server", "unknown"]` — with `"unknown"` preserved as a first-class literal member. This is the paradigmatic example of cooperative deliberation working as designed: an initial claim was falsified by a peer's source evidence, not by an arbiter ruling.

---

## 2. Convergence Log

### 2.1 Accepted by both from the start

These were independently flagged in both Round 1 reviews — highest confidence items.

- **`pytest.raises(Exception)` is over-broad at six sites.** FP-guru §2 and SDET §1.2 enumerated the identical locations: `tests/test_engine_config.py:854, 869`, `tests/test_engine_phases.py:282`, `tests/test_linter_classifier.py:313`, `tests/test_linter_output_contract.py:356, 389`. Agreed fix: `pytest.raises(ValidationError, match=...)`.
- **`_preset_cache` is module-level mutable state.** FP-guru §4 (purity argument) and SDET §6.1 (xdist/isolation argument) both flagged `engine/config.py:214` and the three `setup_method` cache-clear definitions at `test_engine_config.py:968, 1069, 1143, 1254`. Agreed fix: thread the cache as a parameter.
- **Integration-in-unit-clothing.** `tests/test_engine_phases.py:305-421` (`TestRunPipelineCooperative`) reaches the full pipeline through `asyncio.run`. Both agents flagged this; both accept it is pragmatically acceptable pending a `_run_single_round` isolation refactor.
- **Most raise-site branches in `engine/config.py` and `engine/templates.py` are covered.** SDET §3.2 walked the raise sites; FP-guru did not contest.
- **`test_payoffs.py` is the reference pattern** for fixture composability and algebraic-law assertions. Both agents cited it.

### 2.2 FP-guru conceded (with evidence cited)

Three claims from FP-guru's original review were withdrawn after SDET's pushback.

- **`engine/errors.py:79-83` is NOT dead code.** FP-guru revision §1.3: "The one I was most wrong about, and the evidence is unambiguous." Evidence presented by SDET and verified by FP-guru: `engine/providers/__init__.py:41` declares `category: str = "unknown"` as a default; `anthropic.py:86-91, 121-126` and `openai.py:62, 99` raise `ProviderError(..., category="unknown")` on the generic `APIError` path; the fallback branch is the only handler that matches those errors. FP-guru's final position: "primary-path code for the documented default value of a public API." The deletion recommendation was retracted. Corrected typing both agents now endorse: `Literal["auth", "rate_limit", "server", "unknown"]` — `"unknown"` preserved.
- **`NotRequired[int]` does NOT eliminate the runtime shape test at `test_engine_core.py:731-738`.** FP-guru revision §1.1: `NotRequired` is a permissive type marker that widens the set of valid runtime values; the test asserts a specific runtime *choice* that no Python type system can encode without dependent types. Test stays.
- **Pydantic-izing `estimate_cost_usd` does NOT close the weak-assertion gap.** FP-guru revision §1.2: `assert result.estimated_usd >= 0` is tautological whether `result` is a dict or a `CostEstimate(BaseModel)`. The key-presence subset collapses under the type fix; the arithmetic-value subset remains and must still become `== pytest.approx(0.0048)`.

### 2.3 SDET conceded (with evidence cited)

Six items from FP-guru's review that SDET had missed and adopted.

- **`_make_config` / `_write_yaml` should move to `conftest.py`.** SDET cross-review §1.4: "I concede the guru's finding is stronger than mine." The helpers are duplicated between `test_engine_phases.py:62-106` and `test_engine_templates.py:52-85`.
- **`log_usage` should split into `build_usage_entry()` (pure) + `append_usage_entry()` (effectful).** SDET cross-review §2.5: "strictly better than anything I proposed." Moves 10 of 12 tests in `test_linter_usage.py` into pure territory.
- **`_FALLBACK_DISPATCH: dict[str, FallbackFn]`** at `linter/quality.py:421`. SDET cross-review §2.4: "I missed this." Eliminates the `# type: ignore[operator]` at `linter/quality.py:471`.
- **`linter/usage.py` read path at line 261 uses `list[dict]`** when `UsageEntry` already exists at line 49-68. SDET cross-review §2.2: "Real issue. Real miss on my end."
- **Untyped dict returns from `engine/cost.py`** (`estimate_cost_usd(...) -> dict` with no type parameter). SDET cross-review §2.2: shape checks should be Pydantic-enforced, not hand-rolled in tests.
- **Missing frozen / required-field / coercion-failure tests** for `DisputeInfo`, `DisagreementResult`, `AttributionResult`, `QualityResult`, `UsageEntry`, `AdoptionMetrics`, `SynthesisMeta`. SDET revision §6: "I missed the enumeration completeness."

### 2.4 Resolved through debate (new understanding neither had at start)

These are insights that neither agent brought to Round 1 but emerged from the exchange.

- **Types constrain inputs; behavior tests verify outputs — and the two are orthogonal, not substitutes.** FP-guru entered with an implicit "type fixes obsolete ~5-7 of SDET's tests" claim. SDET responded with the orthogonality argument. FP-guru's revision §2 explicitly adopted the framing: "types and behavioral assertions are orthogonal. The guru's P0 does not eliminate my P0." The corrected accounting: 2 tests outright eliminated by type fixes, 4 simplified, ~6 new obligations created. Net test count after both efforts is roughly equal; quality improves sharply.
- **The correct `ProviderError.category` typing includes `"unknown"` as a first-class Literal member.** Neither agent proposed this in Round 1. FP-guru initially proposed `Literal["auth", "rate_limit", "server"]` (too restrictive). SDET initially defended the `str` type. After the source-code evidence surfaced, both independently wrote the same corrected formulation.
- **Phase A / B / C sequencing.** SDET's revision §5 proposed a three-phase decomposition: Phase A is ~15 type-independent test tightenings that land in ~1 day with zero risk; Phase B is the type refactor; Phase C is the post-refactor test cleanup. FP-guru conceded this is better engineering hygiene than the "types first" linear ordering originally proposed. This decomposition is the shipping plan.
- **`parse_synthesis` and `_FALLBACK_DISPATCH` share a root cause.** SDET disputes §4 New Finding N2: both are places where the code says "trust me" without type-system verification, and both are best fixed by lifting data into a discriminated type one level up (`ParsedSynthesis` for one, `dict[str, FallbackFn]` for the other). Neither agent saw the connection in Round 1.

---

## 3. New Findings Surfaced During the Deliberation

Six items from FP-guru's disputes document (A–F) and three from SDET's disputes document (N1–N3) are net-new, not present in either Round 1 review.

### FP-guru findings

- **Finding A: `ProviderError`'s default `category="unknown"` is a first-class sanctioned value, not a sentinel.** The docstring at `engine/providers/__init__.py:37` explicitly lists `"unknown"` in the canonical category enumeration. Any tightening must preserve it as a first-class Literal member. Confirmed by independent verification of `anthropic.py:86-91, 121-126` and `openai.py:62, 99`.
- **Finding B: `tests/test_engine_providers.py:80` already exercises the default-category constructor.** `err = ProviderError("something broke")` is a live test that exercises the default path. When `test_engine_core.py:131` is renamed (Phase C), cross-reference this sibling test for future maintainers.
- **Finding C: `parse_synthesis` calls eight internal helpers, not one or two.** `_extract_agent_count`, `_extract_mode`, `_extract_phases_completed`, `_extract_cross_reviews_performed`, `check_disagreement`, `_extract_resolved_contradictions_count`, `_extract_headline`, `_extract_convergence_count`. This strengthens the SDET's "narrow the except + add a regression test" recommendation over FP-guru's "totality refactor" — the latter would require auditing all eight helpers. Totality refactor deferred to a future spec.
- **Finding D: Test count math was inflated in Round 1.** True impact of type fixes on test count: 2 outright eliminations, 4 simplifications, ~6 new obligations. Net: roughly unchanged. Quality improvement is the real value.
- **Finding E: `ProviderError.category` could be a `StrEnum` rather than a `Literal`.** Python 3.11+ `StrEnum` with members `AUTH`, `RATE_LIMIT`, `SERVER`, `UNKNOWN` gives IDE auto-complete, mypy exhaustiveness checks on the `if/elif` ladder in `errors.py:60-83`, runtime membership checks, and string-equality backward compatibility. Strictly stronger than `Literal`. Flagged as a Phase B enhancement.
- **Finding F: `engine/phases.py:70` `termination_reason: str | None` already has an inline comment listing the valid values** — `# One of: "converged", "max_iterations", "cost_cap", "error"`. The lowest-risk Literal conversion on the list; include in Phase B as the easiest change.

### SDET findings

- **Finding N1: FP-guru mischaracterized SDET's `StrictInt` stance as "agnostic."** SDET's actual position: adopt `StrictInt`/`StrictBool`, but keep the per-field test blast radius minimal (one wire-up test per strict type, not one test per coercion-rejection case). Corrected in disputes §1 S1.
- **Finding N2: The `parse_synthesis` except-narrowing and the `_FALLBACK_DISPATCH` type alias share a root cause.** Both are weakly-typed data that should be lifted into a discriminated type one level up. Recommendation to the shipping engineer: land both as a single "lift weakly-typed data into discriminated types" sub-theme in Phase B; the review value of seeing both together exceeds the diff cost.
- **Finding N3: FP-guru's concession on `errors.py:79-83` strengthens the `match=` tightening at `test_engine_core.py:131`.** Once `Literal["auth", "rate_limit", "server", "unknown"]` lands on `ProviderError.category`, the fallback branch is the **only** path reachable with `category="unknown"`, and its output (`WebError(category="provider_error", status_code=502)`) becomes the primary user-facing error contract for every generic SDK API failure. The `match=` assertion at that test site is load-bearing for the production error shape. This is called out as a Phase C priority.

---

## 4. Final Action Plan — Three Phases

This is the shipping plan. Phase A has zero dependencies on Phase B, so it can land immediately. Phase C has dependencies on Phase B types existing.

### Phase A — Independent Test Tightenings (~1 day, zero dependencies)

No source code changes. All items are test-file edits that can land in a single PR before any type refactor begins.

1. **Replace `pytest.raises(Exception)` with `pytest.raises(ValidationError, match=...)` at the six sites** — `tests/test_engine_config.py:854`, `tests/test_engine_config.py:869`, `tests/test_engine_phases.py:282`, `tests/test_linter_classifier.py:313`, `tests/test_linter_output_contract.py:356`, `tests/test_linter_output_contract.py:389`.
2. **Add `match=` substrings at type-independent `pytest.raises` sites** — `tests/test_engine_core.py:98` (`match="status_code"`), `tests/test_engine_core.py:328` (`match="frozen"`), `tests/test_engine_core.py:336` (`match="duration_ms"`), `tests/test_engine_core.py:394` (`match="agent_reviews"`), `tests/test_linter_usage.py:294` (`match="nonexistent.md"`), `tests/test_linter_quality.py:486-487` (`match="missing.md"`), `tests/test_linter_output_contract.py:273-274` (`match="empty"`).
3. **Replace weak deterministic-count assertions with exact values:**
   - `tests/test_linter_quality.py:170, 181, 281` — `dispute_count >= 1` → exact count.
   - `tests/test_linter_quality.py:326, 361` — `len(result.agent_names) >= 2` → exact list/count.
   - `tests/test_linter_output_contract.py:180` — `count > 0` → exact count.
   - `tests/test_engine_core.py:835` — `estimated_usd > 0` → `== pytest.approx(synthesis=1 × (4000/1M × 3 + 2000/1M × 15))`.
   - `tests/test_engine_core.py:776` — `>= 0` → exact expected dollar figure.
   - `tests/test_linter_output_contract.py:294, 295` — truthy `headline` / `summary` checks → substring or exact values.
4. **Replace vacuous assertions:**
   - `tests/test_engine_core.py:285` — `int(entry.session_id, 16)` → `assert re.fullmatch(r"[0-9a-f]{8}", entry.session_id)`.
   - `tests/test_linter_validate.py:242-243` — `names[0].index("AAA") >= 0` → `assert "AAA" in names[0]`.
   - `tests/test_engine_core.py:260` — `isinstance(emitter, NullEmitter)` → assert the queue/side-effect absence.
5. **Pin currently-vague tests to a single branch** — `tests/test_linter_classifier.py:282-283` (`test_decision_missing_constraints_non_interactive`): pick one deterministic input and assert the specific branch it lands in.
6. **Tighten `test_linter_usage.py:192-195`** — assert `session_id`, `version`, `timestamp`, `dispute_count` presence on the logged JSONL, not just `quality_passed`.
7. **Parametrize `test_agent_name_regex_valid` / `_invalid`** at `tests/test_engine_config.py:832-843` — 4+5 asserts become `@pytest.mark.parametrize` so individual rows report individually.
8. **Parametrize `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` row tests** at `tests/test_engine_core.py:846-852` and `:855-859` — loops become per-row parametrize cases.
9. **Promote `_make_config` / `_write_yaml` to `tests/conftest.py`** as shared fixtures — delete the duplicate at `test_engine_templates.py:52-85`.
10. **Test-name hygiene pass** — rename ambiguous tests: the 5 `test_minimal` occurrences in `test_engine_templates.py`, `test_defaults`, `test_frozen` where clearer names apply, `test_simple_factual_interactive`, `test_red_blue_valid`, `test_explicit_session_id`, per SDET §8.2.
11. **Rename or fix `test_importlib_resources_fallback_path`** at `tests/test_engine_core.py:681` — the current test does not actually isolate strategy 2 (passes if any of strategies 2/3/4 succeed). Either rename to match behavior or rewrite to isolate.
12. **Resolve `test_prior_arbitration_file_is_carried_through_retroactive_move`** at `tests/test_engine_phases.py:1191` — the docstring admits the code path is effectively dead. Phase A: rename to include "regression" semantics; Phase B makes the deletion decision (see bugs section).
13. **Document `_extract_remaining_disputes` single-heading coverage gap** — add a TODO or parametrize over all 8+ heading variants (`Remaining Disputes`, `Key Disputes`, `Open Disputes`, `Outstanding Disputes`, `Disputed Areas`, `Unresolved Tensions`, `Remaining Contradictions`, `Dangerous Contradictions Found`).
14. **Add the missing classifier edge-case tests** — whitespace-only `"   \n\t  "` input to `classify_question`, single-letter alternatives `"A or B"` for `_has_alternatives`, `_count_challenges` combined-path case, `CONCESSION_AGENT` `concedes` variant (SDET §5.10), `_extract_headline` fall-through from spec-changes when synthesis title is absent (SDET §5.12), `build_disputes_context` at `iterations=2` (SDET §5.8, off-by-one risk).
15. **Add empty `events=[]` test for `StructuredDeliberation.from_events`** — type-independent arithmetic branch that no test currently covers.

### Phase B — Type Refactor (~2–3 days, source changes)

All source-code changes grouped into one reviewable refactor.

1. **Convert string fields to `Literal` / `StrEnum`** —
   - `engine/config.py:67` `mode: str` → `Literal[...8 modes...]`.
   - `engine/config.py:73` `stagnation: str` → `Literal["detect", "ignore"]`.
   - `engine/config.py:77` `provider: str` → `Literal["anthropic", "openai"]`.
   - `engine/events.py:28, 39, 50, 63` `phase: str` → `Phase` enum (reuse `linter/models.py:77-89`).
   - `engine/models.py:30, 41, 62, 63` same `phase`/`mode`/`provider`.
   - `engine/phases.py:70` `termination_reason: str | None` → `Literal["converged", "max_iterations", "cost_cap", "error"] | None` (New Finding F — lowest-risk, documented inline).
   - `engine/errors.py:28` `WebError.category: str` → `Literal[...]`.
2. **`ProviderError.category` tightening — with `"unknown"` preserved** — `Literal["auth", "rate_limit", "server", "unknown"]` or (stronger, New Finding E) `StrEnum`. Do NOT drop `"unknown"` — every generic SDK `APIError` path in `anthropic.py:86-91, 121-126` and `openai.py:62, 99` depends on it.
3. **Replace `engine/cost.py` dict returns with Pydantic models** —
   - `estimate_cost_usd(...) -> CostEstimate` where `CostEstimate(BaseModel)` has typed `phases`, `total_launches`, `model`, `estimated_usd`, `low_estimate_usd`, `high_estimate_usd`, `pricing_per_1m_tokens` fields.
   - `estimate_cost(...) -> PhaseCounts` as a `TypedDict` with `arbitration: NotRequired[int]` or a frozen Pydantic model.
   - `PROVIDER_MODEL_OPTIONS` inner values become `ModelOption(BaseModel)` with typed `id`, `name`, `tier: Literal["default", "premium", "budget"]`, `description`.
4. **`_FALLBACK_DISPATCH` typing** at `linter/quality.py:421` — `FallbackFn = Callable[[str], list[DisputeInfo]]`; dispatch becomes `dict[str, FallbackFn]`; delete the `# type: ignore[operator]` at line 471. (Land with the `parse_synthesis` narrow-except change per SDET New Finding N2 — shared "lift weakly-typed data into discriminated types" theme.)
5. **Narrow `engine/models.py:159` `except Exception`** to `except (ValueError, AttributeError, IndexError, re.error)` — documents the real failure surface from the eight `parse_synthesis` helpers (FP-guru New Finding C). The totality refactor of `parse_synthesis` is deferred to a future spec per FP-guru's concession in disputes §1.2.
6. **`_preset_cache` dependency injection** — thread the cache through `_load_preset_file(path, cache: dict[Path, PresetFile])`. Delete the four `setup_method` blocks at `test_engine_config.py:968, 1069, 1143, 1254`. Add `PresetFile(BaseModel)` to replace `dict[str, Any]` at `engine/config.py:214`.
7. **Split `log_usage()` into `build_usage_entry() -> UsageEntry` (pure) and `append_usage_entry(entry, path)` (effectful).**
8. **Rewrite `linter/usage.py:261` read path** to use `UsageEntry.model_validate_json(line)` instead of `list[dict]` plus `.get()` fallbacks.
9. **Add `StrictInt` / `StrictBool` on `EngineConfig.rounds`, `.iterations`, `.validate_templates`** — with a single wire-up test per strict type (per SDET disputes S1).
10. **Add `EngineEvent` discriminator** — `type: Literal[...]` field on each event subclass, `EngineEvent = Annotated[Union[...], Field(discriminator="type")]`. Dispatch test lands in Phase C.

### Phase C — Post-Refactor Tests (~1–2 days, depends on Phase B types existing)

Tests that require Phase B types to exist before they can be expressed.

1. **Frozen / required-field / coercion-failure tests** for every new Pydantic model from Phase B (`CostEstimate`, `ModelOption`, `PresetFile`, `PhaseCounts`) and every existing frozen model without them (`DisputeInfo`, `DisagreementResult`, `AttributionResult`, `QualityResult`, `UsageEntry`, `AdoptionMetrics`, `SynthesisMeta`).
2. **"Typo in phase/mode/category" tests that are newly expressible** — `PhaseStarted(phase="revieww")` → `ValidationError`; `EngineConfig(mode="zebra")` → `ValidationError`. These assertions cannot be written today because the current `str` typing silently accepts the typo.
3. **Parser-layer `ConfigError` regression tests** — after `Literal[...]` lands on `mode`/`stagnation`/`provider`, verify the parser's friendly error message at `engine/config.py:495-659` doesn't degrade to raw `ValidationError` text. This is where the user-facing contract lives after the type refactor.
4. **Rename `test_provider_error_unknown_category_maps_to_502`** (currently at `tests/test_engine_core.py:131`) and change the fixture from `"mystery"` to `"unknown"` (the documented default). This is load-bearing for the production error shape per SDET New Finding N3 — add a `match=` assertion on the `WebError` payload.
5. **Cross-reference `tests/test_engine_providers.py:80`** in the comment at the renamed test so future maintainers know both tests exist and serve different purposes (FP-guru New Finding B).
6. **`EngineEvent` discriminator round-trip dispatch test** — verify Pydantic dispatches `PhaseStarted`/`AgentDispatched`/`AgentCompleted`/`PhaseCompleted` correctly under the new `Field(discriminator="type")`.
7. **Exact-value cost assertions against the new `CostEstimate` model** — `assert result.estimated_usd == pytest.approx(0.0048)`, etc. The key-presence subset of the tests at `test_engine_core.py:770-778` collapses (Pydantic enforces shape); the arithmetic subset remains and tightens.
8. **Parametrize `MODEL_PRICING` / `PROVIDER_MODEL_OPTIONS` as property tests against `ModelOption(BaseModel)`** — shape is enforced at import time; tests assert business invariants (e.g., every provider has ≥1 model with `tier == "default"`).
9. **`find_project_root` strategy isolation** — inject the four strategies as parameters and test each in isolation. Closes the "strategy 2 and 3 are not independently exercised" gap (SDET §5.4).
10. **`parse_synthesis` helper-failure regression test** — construct a pathological synthesis text that makes one of the eight extractor helpers raise, verify the narrowed `except` at `engine/models.py:159` catches it and returns the sentinel `SynthesisMeta`.
11. **`_preset_cache` injection regression tests** — verify per-function cache isolation; enables `pytest-xdist` parallel execution.
12. **Unify dispute-heading detection** — either `frozenset[str]` with a helper function, or parametrize the existing regex test over all 8+ headings (per FP-guru cross-review §5.4).

---

## 5. Bugs Discovered in Source Code

Real source-code issues surfaced during the deliberation that should be tracked separately from test improvements.

- **`linter/question_classifier.py` — `_has_constraints` misses plural time units.** The test `test_plural_unit_misses_singular_word` at `tests/test_linter_classifier.py:84-88` documents the current behavior: the constraint pattern catches singular units but misses constructions like `"3 months"`. The test pins the bug so it's discoverable when fixed. Not a test gap — a source bug with a named regression test.
- **`engine/phases.py:661` — documented dead code (arbitration carry-through).** The test at `tests/test_engine_phases.py:1192` (`test_prior_arbitration_file_is_carried_through_retroactive_move`) has a docstring explicitly admitting "the `prior_arbitration_path` branch is effectively dead code." Phase B decision: delete the branch. Phase A renames the test to flag the status.
- **`engine/_root.py` strategy-2 `try: from conversus.paths import resolve_package_path`** swallows both `ImportError` and `FileNotFoundError` indistinguishably, hiding "conversus is not installed" from "the resource path is wrong" (SDET §9 item 2). Narrow in Phase B.
- **`engine/errors.py:59` `category = getattr(exc, "category", "unknown")`** sets a sentinel string that falls through to the 502 branch. Safe today because `ProviderError.category` is `str` with default `"unknown"`; if the default ever changes to `None`, the string-equality check silently hides the misconfiguration (SDET §9 item 3). Phase B eliminates the risk via `Literal["auth", "rate_limit", "server", "unknown"]`.
- **`linter/quality.py` — `CONCESSION_AGENT` regex supports both `conceded` and `concedes`, but only past-tense is tested** (SDET §5.10). Not a source bug, but a latent regression risk — Phase A adds the `concedes` test.
- **`engine/models.py:159` — `except (ValueError, Exception)` is redundant.** `Exception` is a superset of `ValueError` (SDET §9 item 5). Phase B narrows to the actual failure surface.

---

## 6. Key Philosophical Conclusion

**Types constrain inputs; behavior tests verify outputs. Type fixes and behavioral assertions are complementary, not substitutes.**

This is the load-bearing conclusion of the deliberation. FP-guru entered Round 1 with an implicit model in which a properly tightened type system would retire ~5–7 of SDET's behavioral tests. SDET's cross-review falsified that model on multiple dimensions, and FP-guru's revision §2 adopted the corrected framing in full: "No type system in Python can verify arithmetic correctness (without full dependent types, which Python lacks). No behavior test can verify that a value is the *only* possible output under the type (that's what types give you for free)."

The `errors.py:79-83` story is the paradigmatic example. FP-guru's Round 1 cross-review §3.3 claimed the fallback branch was "unreachable code... a win" once `ProviderError.category` became a `Literal`. SDET's cross-review §4.4 pushed back with a defensive-coding argument. FP-guru's revision §1.3 then went and read the cited source files — `engine/providers/__init__.py:41`, `engine/providers/anthropic.py:86-91, 121-126`, `engine/providers/openai.py:62, 99`, `tests/test_engine_providers.py:80` — and wrote:

> "Three facts I missed on first read: (1) `ProviderError` is a plain `Exception` subclass, not a Pydantic model. A `Literal` type hint on `category` would be a lint-time hint only; at runtime the class accepts any string. (2) The default value of `category` is `"unknown"`. Every single call site in the codebase that writes `raise ProviderError("something broke")` without specifying a category produces an object whose `.category == "unknown"`. (3) The docstring explicitly lists `"unknown"` as a valid category. This is not a typo-catch fallback; `"unknown"` is a first-class sanctioned value."

And then, unambiguously: "I was wrong. SDET was closer than I was... my 'delete it' conclusion was wrong."

This is what cooperative deliberation is supposed to produce: a claim ("this branch is dead") was falsified by a peer's direct source-code citation, not by an arbiter ruling, and the claimant retracted and publicly corrected. Both agents then independently converged on the right fix (`Literal["auth", "rate_limit", "server", "unknown"]`, `"unknown"` preserved) from opposite starting points.

The philosophical generalization: most of the time, a type fix and a behavior test are doing different jobs. The narrow exceptions — tests that exist only to hand-roll a shape check the type system can do for free — are a small minority. FP-guru originally estimated that minority at 5–7 out of ~35; after the deliberation the honest count is 2 eliminations and 4 simplifications, with ~6 new test obligations created by the type fixes themselves. Net test count is flat; test quality improves sharply.

---

## 7. Coverage Achievement

**Starting state (pre-review):** engine/ at 19%, linter/ at 31%. Total project coverage 56.37% with inverted distribution — paid-tier modules well covered, core engine/linter under-tested.

**Final state (post Wave 1-3, pre-synthesis):**
- `engine/config.py` — 100%
- `engine/phases.py` — 99.72%
- `linter/` — 97%
- Overall engine/ + linter/ exceeds the 90% success criterion.

**Volume:** ~565 new tests across 13 test files covering engine (errors, models, `_root`, cost, events, phases, config, templates) and linter (validate, usage, quality, question_classifier, output_contract).

**Still uncovered and intentionally out of scope for this review:**
- `engine/providers/*` — provider SDK wrappers (anthropic, openai). Integration-heavy, requires real credentials or complex SDK mocking.
- `engine/auth.py` — auth layer, depends on secrets management outside the test environment.
- `engine/run.py`, `engine/adhoc.py` — CLI runtime wrappers.
- `web/*` — FastAPI web layer, separate review scope.
- Paid-tier modules (`nashopt`, `optimizer`) — excluded from this spec per `conversus.yml:135`.

The ~90% success criterion applies to engine/ + linter/ only; out-of-scope modules will be covered in subsequent specs.

---

## 8. No Arbiter Required

**This deliberation converged on source-code evidence alone.** No arbiter ruling was requested, and none is needed. The three originally-contested validity claims were resolved by FP-guru's revision §1 after examining the cited source files. The remaining open items are sequencing questions (linear types-first vs. three-phase A/B/C), implementation shape questions (`parse_synthesis` totality vs. narrow-except + test), and aesthetic questions (Hypothesis vs. parametrize for cost linearity) — none of which block merge.

Both agents' disputes documents end with zero validity disputes. FP-guru disputes §4 table:

> "All validity disputes are resolved. No dispute blocks merge... Three disputes remain, none of which block merge."

SDET disputes §3 headline:

> "All major validity disputes are resolved. No dispute blocks merge... Seven items. Three converged. Four sequencing questions, none blocking. Zero remaining validity disputes."

<!-- CONVERSUS:DISPUTES_BEGIN -->
<!-- CONVERSUS:DISPUTES_END -->

The machine-readable disputes block is empty by design. Every finding from both Round 1 reviews lands in the combined three-phase action plan above, with the single exception of FP-guru's originally-wrong "delete `engine/errors.py:79-83`" recommendation, which was retracted in revision.

**Recommended shipping action:** execute Phase A immediately (≤1 day), then Phase B as a single type-refactor PR (2–3 days), then Phase C as the post-refactor test pass (1–2 days). Total ~1 week for the full follow-up plan. The current suite ships as-is today; the three-phase plan is the quality-hardening follow-up.

---

**End of synthesis.**
