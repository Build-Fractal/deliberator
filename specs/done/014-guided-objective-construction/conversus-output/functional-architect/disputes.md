# Functional Architect Disputes

**Date**: 2026-03-24
**Inputs**: All 4 revisions

---

## Remaining Disputes

### Dispute 1: FR-003 scope -- minimal callback vs full implementation

Game-theorist's disputes document argues P1 must include an `InteractiveTemplateSelector` implementation, not just the callback. Schema-engineer argues P1 is the callback (contract), P2 is the implementations. I side with game-theorist's position with a caveat.

The spec says "MUST present them to the user with plain-language descriptions and ask for selection." A callback without an implementation is infrastructure, not compliance. However, implementing the interactive selector in the construction pipeline module couples the pipeline to interactive I/O. The clean approach: define a `TemplateSelector` protocol alongside `GapFiller`, provide `InteractiveTemplateSelector` and `NonInteractiveTemplateSelector` (auto-selects first), and make `construct_objective` accept a `template_selector` parameter defaulting to `NonInteractiveTemplateSelector()`.

**My position**: P1 includes the protocol, both implementations, and the parameter. This is ~30 lines of code and fully satisfies FR-003 without coupling the pipeline to I/O (the protocol abstracts it). The interactive implementation uses `input()` just like `InteractiveGapFiller`.

### Dispute 2: Constraint wiring -- P2 (my revision) vs P3 (game-theorist disputes)

Game-theorist's disputes document argues for reverting constraint wiring to P3, saying constraint names in the output are sufficient for the construction stage and parameter resolution belongs in the execution pipeline. My revision has it at P2.

I accept game-theorist's argument. The construction pipeline's job is to select and parameterize the *objective* template, not to resolve constraint parameters. Constraints are referenced by name; their parameters are resolved at evaluation time when the constraint is actually applied. The `load_constraint_templates` function exists for future use; it doesn't need to be wired in now.

**My position**: Accept P3. I withdraw my P2 classification.

### Dispute 3: `FilledParameters` as frozen dataclass vs Pydantic model

Schema-engineer's disputes document insists the source map return type must be a frozen dataclass for consistency with `ParameterGap` and `GapList`. I proposed `FilledParameters` as a dataclass, which is compatible. But there's a subtle question: should `FilledParameters` be a frozen *dataclass* or a frozen *Pydantic model*?

The precedent is mixed: `ParameterGap` and `GapList` are frozen dataclasses (intermediate state), but `AssembledObjective` is a Pydantic model (output state). `FilledParameters` is intermediate state (between Stage 2 and Stage 3), so frozen dataclass is correct by the project pattern.

**My position**: Frozen dataclass, not Pydantic model. This is consistent with `ParameterGap` and `GapList`. No dispute with schema-engineer on the fundamental point -- we agree on frozen dataclass.

## Convergence

### C-1: Four unanimous P1 items

All four revisions and all dispute documents converge on the same four P1 items:
1. `fill_parameter_gaps` returns `FilledParameters` (frozen dataclass with values + source map)
2. `_substitute_symbolic_form` uses `re.sub(rf'\b{re.escape(name)}\b', ...)`
3. FR-003 gets protocol + implementations + parameter on `construct_objective`
4. `AssembledObjective.source` becomes `SourceProvenance` Pydantic model

### C-2: P2 tier converged

No disputes on these P2 items:
- `GapFillRefused(Exception)` defined alongside `GapFiller`
- Boolean coercion: bidirectional with retry guidance
- Logging: `logging.getLogger(__name__)` matching `extraction.py`
- LLMGapFiller: deferred pending spec clarification on FR-016 conflict
- Provenance tag validation via `Literal` type
- Mode override test: rewrite or rename (not a code fix)
- FR-014 `conversus.yml`: utility function in CLI layer

### C-3: Architecture is unanimously sound

No revision or dispute challenges the three-stage pipeline, GapFiller protocol, frozen intermediates, or deterministic behavior. All four reviewers affirm the architecture.

### C-4: The `.yaml` extension question is closed

Schema-engineer withdrew. Convention is `.yml`, to be documented.

### C-5: `write_objective` extraction is P3

All revisions accept P3. No dispute.

---

## Final Position

### Non-Negotiables
1. `FilledParameters` must be a frozen dataclass (not Pydantic model) for consistency with `ParameterGap` and `GapList`.
2. The str.replace fix must use regex word boundaries. I was wrong to classify this as P2 initially.
3. FR-003 must include implementations, not just the callback. A callback nobody calls is dead code.

### Flexibility
- I can accept any `problem_md` approach (sentinel, constant, caller-provided) as long as it's required.
- I can accept P2 or P3 for constraint wiring -- I've come around to P3 per game-theorist's argument.
- I can accept P2 or P3 for the retry test -- the code works.
