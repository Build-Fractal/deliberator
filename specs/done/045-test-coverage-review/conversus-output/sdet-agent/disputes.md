# SDET Disputes — Round 2 final

**Author:** SDET agent
**Round:** Disputes (post-revision)
**Peer:** functional-programming-guru
**Date:** 2026-04-03

---

## 0. Headline

**All major validity disputes are resolved. No dispute blocks merge.**

After review → cross-review → revision, the FP-guru conceded all three contested factual points:

1. `engine/errors.py:79-83` is live production code (not dead, not merely defensive). My source-code evidence chain (`engine/providers/__init__.py:41` default, `engine/providers/anthropic.py:86-91, 121-126`, `engine/providers/openai.py:62, 99`) was accepted unconditionally. The FP-guru's revision calls it "primary-path code for the documented default value of a public API" and has dropped the deletion recommendation.
2. `NotRequired[int]` on a `PhaseCounts` TypedDict does not eliminate the runtime shape test at `test_engine_core.py:731-738`. FP-guru conceded on the structural grounds I argued: `NotRequired` is a permissive type marker, the test asserts a specific runtime *choice*, and no Python type system encodes that choice without dependent types.
3. Pydantic-izing `estimate_cost_usd`'s return type does not close the arithmetic-correctness gap. FP-guru conceded that `assert result.estimated_usd >= 0` is tautological whether the return is a `dict` or a `CostEstimate(BaseModel)`; my "exact-value on deterministic fixture" recommendation stands.

FP-guru's revision states: "approximately **30-32 of the SDET's ~35 concrete test recommendations should still exist** (I originally estimated ~23-25 of ~30, which was too aggressive)." That's a ~30/35 survival rate, confirming that type fixes and behavioral tests are complementary rather than substitutable.

**Remaining items below are sequencing/priority decisions, not validity decisions. None of them block merge of the combined action list.**

---

## 1. Converged — no remaining dispute

These were disputed in round 1 and are now fully converged:

| Item | Round 1 disagreement | Round 2 status |
|---|---|---|
| `errors.py:79-83` dead-code claim | FP-guru said delete; I said keep | **Converged: keep branch and test.** FP-guru's revision §1.3 concedes fully; both agree it's load-bearing code for the `category="unknown"` default. |
| `NotRequired[int]` eliminates phases-dict test | FP-guru said statically eliminable; I said runtime shape claim | **Converged: test stays.** FP-guru's revision §1.1 concedes. |
| Pydantic `CostEstimate` eliminates weak `>=` assertions | FP-guru claimed 3 of my §1.1 findings were redundant | **Converged: test stays as exact-value assertion.** FP-guru's revision §1.2 concedes; only the key-presence subset collapses, not the value-correctness subset. |
| `_preset_cache` threading as parameter | Both agreed in cross-review | **Converged: my P0-8 adopts FP-guru's P0-6.** |
| `log_usage` split into pure builder + effectful appender | FP-guru recommended; I conceded in cross-review | **Converged: my P0-11 adopts it.** |
| Dependency-inject `load_template` at `run_pipeline` | Not contested either round | **Converged: FP-guru P2 item.** |
| `_FALLBACK_DISPATCH: dict[str, FallbackFn]` type alias | I missed in round 1 | **Converged: FP-guru caught it; I adopted.** |
| `linter/usage.py` read path using `UsageEntry.model_validate_json` | I missed in round 1 | **Converged: FP-guru caught it; I adopted.** |
| `pytest.raises(Exception) → ValidationError` at 6 sites | Convergent across both reviews | **Converged: P0 in both lists.** |
| Replace weak `>=` / `>` with exact values (SDET §1.1) | FP-guru initially dismissed as subsumed by type fixes | **Converged: FP-guru's revision §5 item 4 adopts in full, marked ★ as correction to original position.** |
| Parametrize `test_agent_name_regex_valid/_invalid` | Both agreed | **Converged: orthogonal to types.** |
| Frozen / required-field / coercion-failure tests on Pydantic models | I missed enumeration completeness | **Converged: adopted from FP-guru as P1-5.** |
| `_make_config` / `_write_yaml` promotion to conftest | I missed in round 1 | **Converged: adopted as P1-8.** |
| `find_project_root` strategy isolation | I proposed via coupling; FP-guru sharpened | **Converged: adopted FP-guru's sharper framing.** |

**Total count:** every round-1 validity dispute is resolved. The combined action list is roughly 35-40 items, with the type fixes and behavioral fixes landing in sequence, not in competition.

---

## 2. Remaining sequencing/priority questions (NOT validity disputes)

These are the only open items. None of them block merge — they are decisions the arbiter (or the shipping engineer) can make independently.

### Dispute S1: Scope of `StrictInt` / `StrictBool` adoption on `EngineConfig`

1. **Dispute:** Whether `EngineConfig.rounds`, `EngineConfig.iterations`, and `EngineConfig.validate_templates` should adopt `StrictInt` / `StrictBool` in this cycle, or remain permissively coerced.

2. **Your (SDET) position:** Adopt `StrictInt` / `StrictBool` on the three top-level fields **in Phase B**, add exactly one wire-up test per strict type (proving the strict mode is wired and not accidentally bypassed), and do **not** add per-field coercion-rejection tests. The existing round-1 tests (`rounds: 1.5`, `validate_templates: "true"`, `validate_templates: 1`) become simplified or merged under strict typing:
   - `rounds: 1.5` → same test, sharper failure message (`match="int"`).
   - `validate_templates: "true"` → same test, sharper failure message (`match="bool"`).
   - `validate_templates: 1` → **eliminated** (StrictBool rejects any non-bool, so `"true"` and `1` become the same case).
   One net test removal, three simplifications.

3. **FP-guru's position:** Agnostic in the revision; flagged as an open arbiter question in their §6 item 1: "Scope of `StrictInt` / `StrictBool` adoption on `EngineConfig`. I recommend yes... SDET is agnostic." (Note: FP-guru's characterization of me as "agnostic" is wrong — I'm pro-StrictInt, just with a smaller per-field test blast radius. Corrected here for the record.)

4. **Fact basis:**
   - `engine/config.py:60-80` declares `rounds: int`, `iterations: int`, `validate_templates: bool` with plain annotations — no `StrictInt` / `StrictBool` today.
   - Pydantic v2 default behavior coerces `1.5 → 1` (truncation), `"true" → True`, `1 → True`, etc. This is permissive by design.
   - `pydantic.StrictInt` / `pydantic.StrictBool` reject coercion at construction time with `ValidationError`.
   - `tests/test_engine_config.py` currently relies on Pydantic's permissive coercion succeeding in some places (e.g., YAML produces strings that become ints). Switching to strict would require the parser to cast explicitly upstream. This is a non-trivial blast radius.

5. **Blocks merge?** **No.** Either choice produces a consistent final state. If the arbiter rejects strict adoption, my original P2-a / P2-b / P2-c tests land unchanged. If strict is adopted, my revised P2 section drops P2-c and simplifies P2-a/b.

---

### Dispute S2: Priority of `EngineEvent` discriminator refactor

1. **Dispute:** Whether adding `type: Literal[...]` to `EngineEvent` subclasses (enabling `Annotated[Union[...], Field(discriminator="type")]` dispatch) should be P1 or P2.

2. **Your (SDET) position:** **P1** in my revised list (item P1-7). Phase B adds the discriminator field on the models; Phase C adds the round-trip dispatch test. Rationale: the ergonomic and correctness value lands as soon as the field exists; the test can follow in the same PR or the next one. Splitting across phases keeps the type PR focused on type changes and the test PR focused on new test obligations.

3. **FP-guru's position:** **P2** in their revised list (revision §5 Priority 2 item 14). FP-guru frames it as "Developer-ergonomics win; SDET correctly notes (cross-review §3.4) that it's a syntax change, not a test elimination." Their ordering puts it behind core type fixes and `log_usage` splitting.

4. **Fact basis:**
   - `engine/events.py` defines `PhaseStarted`, `PhaseCompleted`, `ArbitrationRequired`, and siblings as separate Pydantic models with no discriminator field.
   - `EngineEvent` is currently a `Union[PhaseStarted, PhaseCompleted, ...]` without `Field(discriminator="type")`, so deserialization falls back to the "try each, first success wins" slow path.
   - Current Pydantic docs recommend discriminated unions for any Union that is deserialized from JSON (which this one is, via usage log round-trip).
   - The test obligation FP-guru acknowledges in their revision §4 Q1: "Discriminator dispatch tests for `EngineEvent` after adding the `type: Literal[...]` field" — we both agree the test is needed; the dispute is only when in the sequence.

5. **Blocks merge?** **No.** This is pure ordering. My P1/P2 distinction here is about when the test gets written, not whether.

---

### Dispute S3: `parse_synthesis` totality refactor ordering

1. **Dispute:** Whether `parse_synthesis` should be refactored to totality (returning a `ParsedSynthesis` with explicit failure modes, never raising) — and whether that refactor is the correct way to resolve the `engine/models.py:159` `except Exception` branch, or whether the except branch should be tested in place.

2. **Your (SDET) position:** **Narrow the except clause and add a regression test for the real failure surface** (my revised P0-4). The correct fix is:
   ```python
   except (ValueError, AttributeError, IndexError, re.error) as exc:
       logger.warning(...)
       return None
   ```
   Plus one test constructing a synthesis text that makes an extractor helper raise. This is strictly safer than the totality refactor because:
   - The helpers (`_extract_agent_count`, `_extract_headline`, `_extract_convergence_count`, etc.) already have many implicit failure modes — `re.error` from malformed patterns, `IndexError` from empty match groups, `AttributeError` from `None.group()`.
   - Refactoring `parse_synthesis` to totality means auditing every helper for every failure mode and rewriting each one to return `Optional[T]` instead of raising. That's a large, error-prone refactor for a caller that already degrades gracefully with `return None`.
   - Narrowing the except is surgical, low-risk, and documentable.
   I would **reject** the totality refactor for this cycle and **accept** the narrow-and-test fix.

3. **FP-guru's position:** **Prefer the totality refactor** as a P2 item (revision §3.7 and §5 Priority 2 item 15), with a fallback: "If the refactor is rejected, fall back to SDET's position (add a test for the except branch)." FP-guru has explicitly conceded that the current except is **not** dead code; the dispute is only about the refactor being the preferred shape of the fix. They also wrote in §6 item 3: "I put it at P2 behind 'if refactor is rejected, add the SDET's except-branch test.' SDET would prefer the test unconditionally. This is the one remaining validity-flavored dispute, and I'd concede it if the arbiter rules. (The refactor is nice but non-essential; the test is strictly safer.)"

4. **Fact basis:**
   - `linter/output_contract.py:332-354` — `parse_synthesis` definition. Only explicit raise is `ValueError` on empty input.
   - `linter/output_contract.py:200-330` (approx) — extractor helpers. Multiple implicit failure modes through regex, list indexing, and attribute access on regex match results.
   - `engine/models.py:140-165` — caller. Guards with `if synthesis_text.strip():`, then `try: parse_synthesis(synthesis_text) except (ValueError, Exception): return None`. The guard makes the explicit `ValueError` unreachable from this caller; the broad `Exception` catches implicit helper failures.
   - Test coverage for the except branch is currently zero — no test constructs a pathological input that reaches it. This gap exists regardless of whether the refactor happens.

5. **Blocks merge?** **No.** Even FP-guru has said they'd concede if the arbiter rules. The arbiter's choice affects whether we do 1 small PR (narrow + test) or 1 larger refactor PR (totality). Final test coverage is equivalent under either choice.

---

### Dispute S4: Hypothesis vs parametrize for `MODEL_PRICING` cost linearity

1. **Dispute:** Whether the cost-linearity algebraic law at `test_engine_core.py:818-822` should be covered by `@hypothesis.given` (FP-guru's preference) or a small fixed parametrization (my preference, by default).

2. **Your (SDET) position:** Parametrize with 4-6 hand-picked inputs covering the algebraic corners (1 agent, 2 agents, 10 agents, large agent count). Hypothesis is nice-to-have but adds a test runtime budget concern and a "CI flakiness from seed drift" concern. I would not oppose Hypothesis as an additional layer, but I would not make it the primary test.

3. **FP-guru's position:** Suggested Hypothesis in their revision §6 item 4 as an open question: "Hypothesis vs parametrize for `MODEL_PRICING` / cost linearity. I'd add Hypothesis for the algebraic law at `test_engine_core.py:818-822`. SDET is silent. Both work." FP-guru explicitly marks "both work."

4. **Fact basis:**
   - `engine/cost.py:70-108` — `estimate_cost` / `estimate_cost_usd` are pure arithmetic over integer launch counts and fixed per-million-token prices. Linear in `agent_count`.
   - `tests/test_engine_core.py:818-822` — current test asserts a single concrete pair, not the algebraic law.
   - The law is: `estimate_cost_usd(n, ...) = estimate_cost_usd(1, ...) * k_n` where `k_n` encodes the (non-1) launch multiplier for n agents. Hypothesis could fuzz `n`; parametrize could pin 4-6 cases.

5. **Blocks merge?** **No.** FP-guru acknowledges "both work." This is aesthetic.

---

## 3. Summary table

| Dispute | Type | Blocks merge? | Arbiter needed? |
|---|---|---|---|
| `errors.py:79-83` live code | Factual | No | No — converged |
| `NotRequired[int]` eliminates runtime test | Factual | No | No — converged |
| Pydantic CostEstimate closes `>=` gap | Factual | No | No — converged |
| S1: StrictInt/StrictBool scope | Sequencing | No | Optional (either works) |
| S2: EngineEvent discriminator P1 vs P2 | Sequencing | No | Optional |
| S3: parse_synthesis totality refactor order | Sequencing | No | Optional (FP-guru willing to concede) |
| S4: Hypothesis vs parametrize for cost linearity | Style | No | No — both work |

**Seven items. Three converged. Four sequencing questions, none blocking. Zero remaining validity disputes.**

---

## 4. New findings that surfaced during revision

Two items appeared for the first time during my revision that are worth calling out:

### New finding N1: FP-guru mis-characterized my StrictInt stance as "agnostic"

In their revision §6 item 1, FP-guru wrote "SDET is agnostic" about StrictInt adoption. That's not accurate. My position throughout has been: **adopt StrictInt/StrictBool, but keep the per-field test blast radius minimal** (one wire-up test per strict type, not one test per coercion-rejection case). The distinction matters because it changes the sequencing: under FP-guru's reading, my P2 tests are ordering-independent; under my actual position, my P2 tests want to land *after* the strict adoption so they're written against the final shape. This is corrected in Dispute S1 above.

### New finding N2: The `parse_synthesis` except narrowing and the `_FALLBACK_DISPATCH` type alias share a root cause

While writing this disputes document, I noticed a pattern: both `engine/models.py:159` and `linter/quality.py:471` (the `# type: ignore` comment site) are places where the code says "trust me, this dict access / this exception catch is correct" without the type system being able to verify it. The right fix in both cases is *not* to tighten the type in place but to **lift the data into a discriminated type one level up** — `ParsedSynthesis` in one case, `_FALLBACK_DISPATCH: dict[str, FallbackFn]` in the other. This is a shared architectural insight that I missed in my round 1 review and that FP-guru partially surfaced (they caught the `_FALLBACK_DISPATCH` case but didn't connect it to `parse_synthesis`).

**Recommendation to the shipping engineer:** when landing Phase B (type refactor), treat `parse_synthesis` totality and `_FALLBACK_DISPATCH` typing as a single "lift weakly-typed data into discriminated types" sub-theme. Same PR if possible. The review value of seeing both changes together is higher than the diff cost.

### New finding N3: FP-guru's concession on `errors.py:79-83` strengthens my `match=` recommendation

In FP-guru's revision §3.1, they wrote: "The SDET's `match=...` recommendations become **more valuable**, not less, after my type fix lands. We're not in competition; we're in sequence."

This is a strategic insight I should call out explicitly: **after `Literal["auth", "rate_limit", "server", "unknown"]` lands on `ProviderError.category`, the fallback branch at `errors.py:79-83` is the only path that can be reached with `category="unknown"`, and its output (`WebError(category="provider_error", status_code=502)`) becomes the primary user-facing error contract for every generic SDK exception.** That means the test at `test_engine_core.py:131` is not only still needed — its `match=` assertion on the error payload becomes *load-bearing* for the production error shape that users see on every generic anthropic / openai API failure. My P1-7 (add `match=` substrings) applies directly here.

---

## 5. Final recommendation to the arbiter

**Accept both lenses in full. Ship the combined 35-40 item list in three phases (A: independent test tightenings, B: type refactor, C: post-refactor tests against typed models). No validity disputes remain. The four sequencing questions have safe defaults under either choice.**

The cooperative deliberation worked: my source-code evidence forced FP-guru to concede `errors.py:79-83`; FP-guru's type-system framing forced me to adopt 6 items I missed (log_usage split, conftest fixture promotion, `_FALLBACK_DISPATCH` typing, `UsageEntry` read path, Pydantic-izing cost returns, frozen-model test enumeration). The final state is strictly better than either initial review.

**End of disputes document.**
