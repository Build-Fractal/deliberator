# Cross-Review: functional-architect reviewing game-theorist

## Dangerous Contradictions

### DC-1. str.replace fix: regex word boundary may not be sufficient

Game-theorist proposes `re.sub(rf'\b{re.escape(name)}\b', str(value), result)` as the fix for substring collision. I agree with the diagnosis but the fix has a subtle flaw: `\b` (word boundary) matches between a word character (`\w`) and a non-word character. Parameter names like `w_i` contain underscores, which are word characters. So `\bw\b` would *not* match the `w` in `w_i` -- that's correct. But `\bw\b` *would* fail to match `w` when it appears after an operator like `-w` because `-` is a non-word character and `w` is followed by ` ` (also non-word-to-word boundary). Actually, `-w * score` would match `w` correctly: the boundary is between `-` (non-word) and `w` (word), and between `w` (word) and ` ` (non-word). So the regex fix does work for the mathematical expression case. My concern was misplaced -- the word-boundary approach is correct for typical symbolic forms. I withdraw this concern.

However, there is a real issue: parameter names that start with digits (e.g., `3sigma`) would not have a word boundary at the start when preceded by another digit. This is an edge case unlikely to occur with well-named parameters but worth noting.

### DC-2. Disambiguation via ValueError: too aggressive?

Game-theorist's Recommendation 3 proposes raising `ValueError` when the top two decision types have match counts within 1 of each other. This contradicts the pipeline's design philosophy of being conservative but never failing. The current behavior is deterministic (pick highest, break ties by enum order). Raising an error on ambiguous input means the pipeline can *refuse to produce output* -- which is worse than producing output for a slightly-wrong classification, because the user can correct the classification via `explicit_type` but cannot recover from an exception without code changes. I'd prefer a warning + the current deterministic behavior, not an exception.

### DC-3. Constraint gap-filling priority: P3 (game-theorist) vs P1 (functional-architect)

Game-theorist classifies constraint parameter gap-filling as P3 (Recommendation 8, "Completeness"). I classify constraint wiring as P1 (R4) because FR-011 requires "selected constraints with parameters" in the output. The contradiction: if the assembled objective includes constraint names but not their parameter values, downstream consumers cannot use the constraints. Game-theorist may be reading "constraints with parameters" as "constraints that have parameters" (a description) rather than "constraints including their parameter values" (a data requirement). I maintain P1 because an incompletely parameterized constraint is not actionable.

## Tensions

### T-1. Template ranking importance

Game-theorist devotes significant attention to template ranking (Recommendation 10, off-base assumption #1) and proposes keyword overlap, priority fields, or parameter-name matching. I don't raise template ranking because I see it as a separate concern from the pipeline architecture. The tension: game-theorist is right that alphabetical ordering is semantically arbitrary, but the fix (adding ranking heuristics) is a feature addition with its own test surface and design decisions. It should be a follow-up spec amendment, not a P3 fix. However, game-theorist's point that `budget-constrained` ranks above `competitive-selection` for SELECTION problems is a compelling concrete example.

### T-2. Non-interactive detection: three options vs one

Game-theorist offers three alternatives for replacing the RuntimeError-catching pattern (is_interactive property, isinstance check, dedicated exception). I agree with the diagnosis but prefer a single, opinionated recommendation. The custom exception (`GapFillRefused`) is the least-invasive fix -- it doesn't change the protocol, doesn't require isinstance checks, and is backward-compatible. The is_interactive property changes the protocol (breaking change). The isinstance check couples the pipeline to a specific implementation class.

### T-3. Explicit parameter extraction conservatism

Game-theorist praises the extraction as "appropriately conservative." I flag it as "conservative to a fault" and propose alias maps. The tension is about the intended user experience: game-theorist values avoiding false positives (extracting the wrong parameter), I value reducing the number of interactive gaps. Both are valid -- the right balance depends on whether the typical use case is interactive (where fewer gaps means less friction) or non-interactive (where false positives mean wrong output with no correction opportunity). For non-interactive mode, conservative is correct; for interactive mode, more aggressive extraction with user confirmation would be better.

### T-4. `problem.md` parser priority

Game-theorist raises the missing `problem.md` parser as P3 (Recommendation 9). I don't raise it. The tension: the parser is a nice-to-have that would complete the FR-019 story, but `classify_decision_type` already accepts `explicit_type` as a parameter. The caller can parse `problem.md` externally and pass the type. A built-in parser would reduce integration friction but isn't required for pipeline correctness.

## Safe Agreements

### SA-1. Source map discarded by `fill_parameter_gaps`

Both reviews identify the same root cause, the same value-comparison fragility in `construct_objective`, and propose the same structural fix (typed return). This is the consensus finding across all reviewers.

### SA-2. Boolean coercion is a latent bug

Both reviews identify `_coerce_value` returning `None` for boolean type. Game-theorist proposes a simple truthy check; I don't propose a specific fix in my review but acknowledge the gap. The fix is straightforward.

### SA-3. FR-003 multi-template presentation is needed

Both reviews confirm `candidates[0]` is silently used. Game-theorist frames it as a ranking problem; I frame it as a missing user interaction. Both agree the fix involves a protocol-based selection mechanism.
