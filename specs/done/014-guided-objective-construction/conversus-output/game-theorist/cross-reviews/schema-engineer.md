# Cross-Review: game-theorist reviewing schema-engineer

## Dangerous Contradictions

### DC-1. Priority of `_substitute_symbolic_form` bug fix

We both identify the `str.replace` substring collision as a bug and propose the same regex word-boundary fix. However, schema-engineer classifies this as P1 while I also classify it P1. No contradiction here on priority, but we diverge on the trigger scenario. Schema-engineer describes the `w` inside `score` scenario (replacing `w` corrupts the word `score`). This is incorrect for the current sort-by-length-descending implementation -- `score` (length 5) would be replaced before `w` (length 1), so the literal `w` in `score` is already gone by the time `w` is processed. The real danger is the reverse: a *value* substitution introducing a new matchable substring. For example, replacing `score` with `10w` (a valid float-like string) would then have `w` matched in a second pass. Both the schema-engineer's example and my example are valid failure modes, but confusing them could lead to an incomplete fix that only addresses one.

### DC-2. Source map structure: flat dict vs nested model

Schema-engineer's R1 proposes restructuring `source` into a `SourceProvenance` Pydantic model with `problem_md` and `filled_by` sub-dict. I agree the source map must be returned from `fill_parameter_gaps`, but the FR-020 spec language is ambiguous about whether `problem_md` is a field *inside* the source dict or a sibling field on `AssembledObjective`. If `problem_md` is added as a top-level field on `AssembledObjective` rather than nested inside `source`, the flat `dict[str, str]` for `source` (with the source map properly returned) may be sufficient. This is a spec-interpretation disagreement that could lead to different implementations.

### DC-3. Boolean coercion: silent failure vs explicit error

We both identify the boolean coercion gap. Schema-engineer's fix returns `None` for unrecognized boolean strings (e.g., `"maybe"`), which means the coercion silently fails and the parameter is not extracted. I propose a simpler `value_str.lower() in ("true", "1", "yes")` that returns a boolean. The difference: schema-engineer's version handles `"false"` explicitly (returns `False`), while mine only detects truthy values and implicitly treats everything else as `False` via the return type. Schema-engineer's approach is more correct -- a boolean parameter should distinguish "user said false" from "coercion failed."

## Tensions

### T-1. FR-003 priority: P2 (schema-engineer) vs P2 (game-theorist)

We agree on P2 for FR-003 multi-template presentation, but for different reasons. I frame it as a template ranking problem (alphabetical ordering is semantically arbitrary). Schema-engineer frames it as a spec compliance gap (the spec says MUST). The tension is that a MUST-level spec requirement arguably deserves P1, but both of us deprioritized it because the pipeline functions correctly for single-candidate cases and the current template library rarely produces ambiguous multi-candidate scenarios.

### T-2. Scope of `GapFillRefused` exception

Schema-engineer proposes `GapFillRefused(Exception)`. I propose three alternatives (is_interactive property, isinstance check, dedicated exception). The tension is whether the fix should be minimal (custom exception only) or structural (protocol-level change). A protocol-level `is_interactive` property would be a breaking change for existing GapFiller implementations; the custom exception is non-breaking.

### T-3. `.yaml` extension support

Schema-engineer raises `.yaml` extension support as P3. I do not mention it. This is a legitimate robustness concern but arguably a documentation issue rather than a code change -- the convention should be documented, not silently expanded, since adding `.yaml` support changes the contract for template authors.

### T-4. Provenance tag validation

Schema-engineer proposes validating source tags against a closed set `{"explicit", "default", "gap_filled", "deferred"}`. I don't raise this. It's a good defensive measure that would have caught the source-map reconstruction bug earlier (a typo in a tag string would be caught at validation time).

## Safe Agreements

### SA-1. Source map must be returned from `fill_parameter_gaps`

Both reviews identify this as the same bug with the same root cause and propose the same structural fix (return a tuple or dataclass). This is the highest-confidence finding across both reviews.

### SA-2. `NonInteractiveGapFiller` exception pattern is fragile

Both reviews identify the `RuntimeError` catch as semantically wrong and propose moving to a dedicated exception or explicit detection. The specific fix differs but the diagnosis is identical.

### SA-3. Template loading is correct and deterministic

Both reviews confirm that `load_objective_templates` follows established patterns, uses sorted glob, and produces deterministic results. No issues raised by either reviewer.
