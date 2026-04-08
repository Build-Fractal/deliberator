# Schema Engineer Disputes

**Date**: 2026-03-24
**Inputs**: All 4 revisions

---

## Remaining Disputes

### Dispute 1: SourceProvenance.problem_md -- required with sentinel vs required without sentinel

Game-theorist's revision objects to the `"<stdin>"` sentinel, proposing instead that callers provide descriptive strings like `"programmatic"` or `"test"`. Spec-compliance and functional-architect accept the required-with-sentinel approach. I originally proposed optional; all cross-reviewers pushed back.

The dispute is narrow: sentinel string vs caller-provided string. From a schema perspective, both achieve the same result -- `problem_md` is always populated. The difference is discoverability: a sentinel like `"<stdin>"` is a convention that must be documented and checked for; a caller-provided string like `"test"` is self-describing but unpredictable.

**My position**: Define a `PROBLEM_MD_STDIN` constant (`"<stdin>"`) and use it as the default in `construct_objective`. Callers can override with any string. This gives the best of both worlds: a documented default for the common case and flexibility for tests/programmatic use. The constant makes the sentinel greppable and avoidable.

### Dispute 2: FR-003 scope -- callback only vs callback + implementation

Game-theorist's disputes document argues the P1 fix must include both the callback and an `InteractiveTemplateSelector` implementation. My revision accepts the callback-only approach as the P1 deliverable. The dispute: is a callback without an implementation spec-compliant?

From a schema perspective, the callback changes the `construct_objective` signature (a schema-level change). The implementation is runtime behavior. I'd argue the P1 deliverable is the *contract* (the callback parameter with its type signature), and the P2 deliverable is the *implementations*. This lets the pipeline evolve without blocking on interactive/non-interactive implementation details.

**My position**: P1 is the callback parameter with type `Callable[[list[ObjectiveTemplate]], ObjectiveTemplate]` (or a `TemplateSelector` protocol). P2 is the `InteractiveTemplateSelector` and `NonInteractiveTemplateSelector` implementations. The callback's default should be `lambda candidates: candidates[0]` for backward compatibility.

### Dispute 3: Retry test priority -- P2 (spec-compliance) vs P3 (schema-engineer)

Spec-compliance's revision maintains P2 for the retry test because FR-007 is a MUST requirement. My revision maintains P3 because the implementation exists and is correct by inspection. The dispute: does an untested MUST requirement count as partial compliance?

**My position**: P3. The implementation is present, correct, and covers the spec requirement. The test prevents regression but doesn't change compliance status. If we have limited engineering bandwidth, the four P1 items and the P2 items (boolean coercion, GapFillRefused, logging) should take priority over a test for code that already works.

## Convergence

### C-1: Four unanimous P1 items

All four revisions converge on:
1. `fill_parameter_gaps` returns `FilledParameters` with source map
2. `_substitute_symbolic_form` uses regex word boundaries
3. FR-003 gets at least a callback mechanism
4. `AssembledObjective.source` becomes `SourceProvenance` with `problem_md`

No revision disputes any of these four items. This is the strongest consensus the process has produced.

### C-2: P2 tier is stable

All revisions agree on these P2 items (no disputes):
- `GapFillRefused` exception
- Boolean coercion (bidirectional)
- Logging
- LLMGapFiller + gap_fill_model (deferred, bundled)

### C-3: `.yaml` extension support is withdrawn

My withdrawal of the `.yaml` extension recommendation was accepted without dispute. The convention is `.yml`, and documentation should state this explicitly.

### C-4: Mode parameter is a fallback, not an override

Functional-architect's revision downgrades the mode parameter fix from P1 to P2 (test-only fix), accepting spec-compliance's grammatical analysis. All revisions now agree: the `mode` parameter in `select_candidate_templates` is a fallback for unmapped decision types, not a user override. The test should be renamed or rewritten.

### C-5: `construct_objective` file I/O is acceptable

Functional-architect's revision downgrades `write_objective` extraction from P2 to P3. All revisions accept that the orchestrator can have side effects. No dispute.

---

## Final Position

### Non-Negotiables
1. `SourceProvenance` must be a Pydantic model with typed `filled_by` values (`Literal` types), not a plain dict. The project uses Pydantic for structured data.
2. `problem_md` must be required (not optional). The sentinel/constant approach is my preferred implementation.
3. The source map from `fill_parameter_gaps` must be a frozen dataclass, not a tuple. Consistency with `ParameterGap` and `GapList`.

### Flexibility
- I can accept game-theorist's "caller-provided string" approach for `problem_md` if a constant is provided as documentation.
- I can accept P2 or P1 for the FR-003 implementation scope -- the callback is the schema-level change; implementations can follow.
- I can accept P2 or P3 for the retry test -- the implementation is correct regardless.
