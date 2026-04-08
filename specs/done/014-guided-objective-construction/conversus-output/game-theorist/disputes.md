# Game-Theorist Disputes

**Date**: 2026-03-24
**Inputs**: All 4 revisions

---

## Remaining Disputes

### Dispute 1: FR-003 minimal fix scope -- callback default vs true presentation

All four revisions agree FR-003 is P1. The dispute is on the *scope* of the P1 fix. My revision proposes a `template_selector` callback defaulting to `lambda candidates: candidates[0]`, which satisfies the protocol requirement without changing behavior for existing callers. Schema-engineer and spec-compliance accept this as "the right incremental approach." Functional-architect also agrees.

However, this minimal fix does not actually satisfy FR-003's MUST language: "present them to the user with plain-language descriptions and ask for selection." A callback that defaults to auto-select is the *infrastructure* for FR-003, not the *implementation*. If we ship the callback but no implementation actually presents templates, FR-003 is still NOT MET.

**My position**: The P1 deliverable should include both the callback infrastructure *and* an `InteractiveTemplateSelector` implementation that uses the `InteractiveGapFiller` pattern (print descriptions, prompt for choice). The NonInteractive variant auto-selects `candidates[0]`. This fully satisfies FR-003 with minimal effort.

### Dispute 2: SourceProvenance `problem_md` as required vs optional with sentinel

Schema-engineer's revision and spec-compliance's revision both want `problem_md` required with a sentinel `"<stdin>"` for programmatic use. Functional-architect's revision adopts this. I'm concerned about the sentinel approach: `"<stdin>"` is a magic string that callers must know about. An alternative: `problem_md: str` is required when `construct_objective` is called with a file path, and the *caller* is responsible for providing it. If the caller doesn't have a file path, they construct the `AssembledObjective` directly without going through `construct_objective`.

**My position**: Make `problem_md` required on `SourceProvenance` but do not define a sentinel. Let the caller provide the actual path. If there is no file, the caller provides a descriptive string like `"programmatic"` or `"test"`. This is more honest than a magic sentinel.

### Dispute 3: Constraint wiring priority -- P2 vs P3

My revision has constraint gap-filling at P2 (upgraded from P3). Spec-compliance leaves constraints at P2 implicitly (not in their final P1 list, not separately called out). Functional-architect downgrades constraint wiring from P1 to P2. Schema-engineer doesn't raise it.

The dispute: is constraint wiring genuinely needed in the near term? The assembled objective includes constraint names (`constraints: list[str]`), which is sufficient for template selection and symbolic form assembly. Constraint *parameters* (like `budget_limit`) are only needed when the constraint is evaluated at runtime, which is outside the construction pipeline's scope. I'd argue P3 is still correct for the construction pipeline; constraint parameter resolution belongs in the execution pipeline.

**My position**: Revert to P3. Constraint names in the output are sufficient for the construction stage. Parameter resolution is an execution-stage concern.

## Convergence

### C-1: P1 items are now unanimous

All four revisions converge on the same four P1 items:
1. Source map return from `fill_parameter_gaps` (FilledParameters dataclass)
2. `_substitute_symbolic_form` regex word-boundary fix
3. FR-003 multi-template presentation (at least the callback infrastructure)
4. FR-020 SourceProvenance model with `problem_md`

This is strong convergence from divergent starting positions (reviewers initially had 3-5 P1 items each with different compositions).

### C-2: Boolean coercion is P2

All revisions now agree boolean coercion is P2 (latent bug, no current trigger). Schema-engineer's bidirectional approach (true/false/None) is the accepted fix, including boolean-specific retry guidance.

### C-3: GapFillRefused exception is P2

All revisions agree on a custom `GapFillRefused(Exception)` defined alongside the `GapFiller` protocol. No dispute on the approach.

### C-4: LLMGapFiller is deferred pending spec clarification

Spec-compliance downgrades from P1 to P2 and acknowledges the FR-016 dependency conflict. All revisions agree the GapFiller protocol infrastructure is correct and the LLM implementation is a follow-up that requires spec clarification.

### C-5: Logging is P2

All revisions that mention logging (game-theorist, schema-engineer, functional-architect) agree on P2. Spec-compliance doesn't prioritize it but doesn't object.

---

## Final Position

### Non-Negotiables
1. Source map must be returned from `fill_parameter_gaps`. The value-comparison reconstruction is a correctness bug.
2. `_substitute_symbolic_form` must use regex word-boundary replacement. The str.replace approach is one template away from producing wrong output.
3. FR-003 must have both callback infrastructure *and* at least one interactive implementation. A callback that nobody calls is not compliance.

### Flexibility
- I can accept `problem_md` as required with any reasonable non-file value (sentinel, descriptive string, or caller-provided).
- I can accept P2 or P3 for constraint wiring -- it doesn't affect the construction pipeline's correctness.
- I can accept any of the three LLMGapFiller dependency-injection approaches (callable, protocol, or lazy import) as long as FR-016 is preserved.
