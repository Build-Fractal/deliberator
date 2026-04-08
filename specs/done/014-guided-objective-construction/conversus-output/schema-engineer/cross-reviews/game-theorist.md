# Cross-Review: schema-engineer reviewing game-theorist

## Dangerous Contradictions

### DC-1. str.replace collision: which failure mode is the real threat?

Game-theorist describes the substitution bug as "a value substitution could introduce new matchable substrings" and acknowledges the sort-by-length-descending mitigation. I describe it as "single-character parameter names like `w` will corrupt any word containing `w`." These are *different failure modes*. Game-theorist's scenario (value injection) requires a multi-pass substitution where an earlier replacement creates a new target -- but the implementation does a single pass per parameter, so the replaced text for `score` won't be re-scanned for `w`. My scenario (substring within a longer token) is the immediate threat: in `"J = -w * score + penalty * overlap"`, after replacing `overlap` (7 chars) and `score` (5 chars), the `w` in the *original* form text at position "- **w** *" is correctly targeted, but if by some template edit a parameter named `win` exists alongside `w`, the sort-by-length mitigation works. The *actual* failure case is simpler: `w` appears as a standalone token in the form, but `str.replace` would also match the `w` in `new_score` if such a variable existed. The regex word-boundary fix addresses both, but we should agree on the test case.

### DC-2. Template ranking: semantic concern vs type-safety concern

Game-theorist's Recommendation 10 proposes improving template ranking with keyword overlap, priority fields, or parameter-name matching. I don't raise template ranking at all because my scope is schema/type safety, not semantic correctness. The contradiction: game-theorist sees alphabetical ordering as a correctness issue (wrong template selected), while I see template selection as outside the type system. However, if the wrong template is selected due to poor ranking, the assembled objective will have wrong parameter names and wrong symbolic form -- which *is* a schema issue. Game-theorist is right to raise this, and I should acknowledge it as a contributor to incorrect output.

### DC-3. Disambiguation for multi-type keyword matches

Game-theorist's Recommendation 3 proposes raising `ValueError` when the top two decision types have match counts within 1 of each other. I don't raise classification ambiguity at all. The contradiction: game-theorist sees this as P1 (correctness), but raising an error on ambiguous input is a conservative design choice, not a correctness fix. The current behavior (pick the highest, break ties by enum order) is *deterministic and documented* (FR-012). Raising an error changes the contract -- callers that previously got a classification now get an exception. This should be P2 at most, and the error should be a specific `AmbiguousClassification` exception, not `ValueError`.

## Tensions

### T-1. Source map reconstruction: same diagnosis, different fix scope

Both reviews identify the source map being discarded. Game-theorist proposes changing the return type to `tuple[dict, dict]`. I propose a `FillResult` dataclass. The tension is cosmetic -- a named dataclass is more self-documenting but adds a type to the module. Given the project's pattern of frozen dataclasses for intermediate state (ParameterGap, GapList), a `FillResult` dataclass is more consistent.

### T-2. Boolean coercion: truthy-only vs bidirectional

Game-theorist's fix returns `value_str.lower() in ("true", "1", "yes")` -- a boolean expression that returns True or False. This means *every* input produces a boolean, including garbage like `"maybe"` (returns False). My fix has explicit branches for true-like and false-like strings, returning `None` for unrecognized input, which lets the caller detect coercion failure. The tension: game-theorist's approach never fails (always returns a bool), mine can signal failure. For parameter extraction (where failure means "don't extract"), mine is correct. For gap-filling (where the user already answered), game-theorist's approach might silently map "maybe" to False, which is wrong.

### T-3. Constraint parameter gap-filling priority

Game-theorist raises constraint parameter gap-filling as P3 (Recommendation 8). I don't raise it at all. The tension: constraints are loaded but their parameters are never filled, which means the assembled objective references constraints with unknown parameter values. Game-theorist is right to flag this but P3 seems correct -- the constraint parameters can be filled in a follow-up without breaking the current pipeline.

### T-4. `problem.md` parser (FR-019)

Game-theorist's Recommendation 9 proposes a `parse_problem_md` function. I raise the `problem_md` path as missing from the `source` model but don't propose a parser. The tension: a parser would make the explicit-type extraction path work end-to-end, but it's a new function with its own test surface. Game-theorist treats this as P3 (completeness), which seems right -- the `explicit_type` parameter to `classify_decision_type` already works; what's missing is the caller that reads from a file.

## Safe Agreements

### SA-1. `fill_parameter_gaps` source map must be returned

Identical diagnosis, same root cause, compatible fix proposals (tuple vs dataclass). Highest-confidence finding.

### SA-2. NonInteractiveGapFiller exception pattern is fragile

Both reviews identify RuntimeError as too broad. Game-theorist offers three options; I propose a custom exception. The custom exception is the minimal fix both agree on.

### SA-3. Deferred parameter handling is correct

Both reviews confirm function-type parameters with `derived_from` are properly handled. No issues raised.

### SA-4. Template loading and determinism are correct

Both reviews confirm sorted glob, deterministic ordering, and no randomness. FR-012 compliance is unanimous.
