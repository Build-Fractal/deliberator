# Cross-Review: functional-architect reviewing schema-engineer

## Dangerous Contradictions

### DC-1. `AssembledObjective.source` restructuring scope

Schema-engineer proposes a `SourceProvenance` Pydantic model with `problem_md` and `filled_by` fields. I propose a `FilledParameters` dataclass for the `fill_parameter_gaps` return value but don't restructure `AssembledObjective.source` itself. The contradiction: schema-engineer's fix changes the public API of `AssembledObjective` (any code that reads `source["param_name"]` breaks). My fix keeps `source` as `dict[str, str]` and adds `problem_md` as a separate field on `AssembledObjective`. These are incompatible approaches. Schema-engineer's approach is more spec-faithful (the spec describes `source` as containing both problem_md and filled_by). Mine is less disruptive to existing consumers. The right call depends on whether any code outside the test suite reads `AssembledObjective.source` today.

### DC-2. `.yaml` extension support as a code change

Schema-engineer's P3 recommendation adds `*.yaml` glob to `load_objective_templates`. I'd push back: adding a second glob pattern means template authors can use either extension, creating inconsistency. The project should pick one convention and enforce it. If `.yml` is the convention (which it is -- all existing templates use `.yml`), then `.yaml` files should be *flagged as errors*, not silently loaded. This is a documentation fix, not a code change.

### DC-3. Boolean coercion: schema-engineer's `None` return for unrecognized strings

Schema-engineer's boolean coercion fix returns `None` for strings that are neither true-like nor false-like. This is correct for `extract_explicit_parameters` (where `None` means "don't extract"), but in `_fill_single_gap`, a `None` return from coercion triggers a retry. This means a user who types "maybe" for a boolean parameter gets retried, which is the correct behavior. However, schema-engineer's fix doesn't account for the retry message -- `_fill_single_gap` constructs guidance for numeric ranges but has no guidance path for boolean parameters. The fix should include a guidance message like "Please answer yes/no or true/false."

## Tensions

### T-1. Provenance tag validation: useful or over-engineering?

Schema-engineer proposes validating source tags against `{"explicit", "default", "gap_filled", "deferred"}`. I don't raise this. The tension: this is good defensive programming but adds a validation check that will only catch bugs during development. In production, the tags are set by `construct_objective` and `fill_parameter_gaps`, which already use the correct strings. A `Literal` type annotation would catch this at type-check time without runtime overhead. If the project uses mypy, the `Literal` type is strictly better than a runtime check.

### T-2. GapFillRefused exception: non-breaking vs protocol change

Schema-engineer proposes a custom `GapFillRefused(Exception)` to replace `RuntimeError`. I agree with the diagnosis. The tension is whether this should be a `GapFiller` protocol requirement (document that refusal raises `GapFillRefused`) or just an implementation detail of `NonInteractiveGapFiller`. If it's a protocol requirement, all GapFiller implementations must know about `GapFillRefused`, which adds coupling. If it's an implementation detail, `fill_parameter_gaps` must still catch it specifically, which means it depends on the implementation. The clean solution: define `GapFillRefused` in the same module as `GapFiller` and document it as the standard refusal signal.

### T-3. `FillResult` vs `SourceProvenance`: two new types for one fix

Schema-engineer proposes `SourceProvenance` (on the output side). I propose `FilledParameters` (on the intermediate side). Both address the source-map problem but at different points in the pipeline. The tension: adding both types is the right thing to do -- `FillResult` carries the source map from Stage 2 to Stage 3, and `SourceProvenance` structures it in the output model. But adding two new types for what is fundamentally "carry the source map through" feels heavy. Alternatively, `fill_parameter_gaps` returns a plain tuple, and `AssembledObjective.source` becomes `SourceProvenance`. This minimizes new types while fixing both the data-loss and the schema-compliance issues.

### T-4. P1 count: schema-engineer has 4 P1s

Schema-engineer classifies four items as P1: source structure, source map return, str.replace fix, and boolean coercion. I have three P1s: source map return, mode override fix, FR-003 multi-template. Having 4+ P1s dilutes priority. Not all of these are equally urgent -- the boolean coercion bug has no current trigger (no boolean parameters in the template library), while the source map and str.replace bugs affect existing templates. I'd reclassify boolean coercion as P2 (latent bug, no current impact).

## Safe Agreements

### SA-1. Source map must be returned from `fill_parameter_gaps`

Identical diagnosis, compatible fix proposals. This is the unanimous finding.

### SA-2. `_substitute_symbolic_form` uses fragile string replacement

Both reviews identify the same bug with the same regex word-boundary fix. Difference is only priority (P1 vs P2).

### SA-3. FR-003 multi-template presentation is unimplemented

Both reviews confirm `candidates[0]` is silently used. Compatible fix proposals involving a selection protocol.

### SA-4. Template loading and Pydantic validation are correct

Both reviews affirm that `load_objective_templates`, `ObjectiveTemplate.model_validate`, and the `AssembledObjective` model validator work correctly for the current template library.
