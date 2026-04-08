# Cross-Review: spec-compliance reviewing functional-architect

## Dangerous Contradictions

### DC-1. Shadowed mode parameter: P1 bug or spec-correct behavior?

Functional-architect's R2 classifies the shadowed `mode` parameter as P1. I don't raise it because FR-018 defines a *fixed* decision-type-to-mode mapping. The contradiction: functional-architect argues callers should be able to override mode with `mode="cooperative"` for a SELECTION problem. But FR-018 says: "Decision type to mode mapping is explicit and deterministic." If the mapping is deterministic, the mode is *derived from* the decision type, not independently configurable. The `mode` parameter on `select_candidate_templates` is a fallback for custom decision types not in `_DECISION_TYPE_MODE`, not an override mechanism.

However, functional-architect raises a valid test-coverage concern: `test_explicit_mode_override` passes but doesn't verify that cooperative templates were actually selected. The test should be strengthened regardless of whether the mode parameter is an override or a fallback.

### DC-2. Constraint wiring as P1: overreach?

Functional-architect's R4 classifies constraint wiring as P1, arguing FR-011 requires "selected constraints with parameters." I assess FR-011 as MET because `AssembledObjective` includes `constraints: list[str]` and the model validates. The contradiction: functional-architect reads "with parameters" as requiring parameterized constraint objects in the output. I read it as the output *including* the constraint field (which it does). The spec says "template name, game form, mode, all parameters with provenance, selected constraints, and symbolic form." The "with parameters" modifies "all parameters," not "selected constraints." This is a grammatical ambiguity in the spec.

Rereading: "Output includes template name, game form, mode, **all parameters with provenance**, **selected constraints**, and symbolic form." The commas separate distinct items. "All parameters with provenance" is one item; "selected constraints" is another. Functional-architect's reading that constraints need parameters appears to be a misparse of the spec sentence.

### DC-3. File I/O extraction from `construct_objective`: priority disagreement

Functional-architect's R7 proposes extracting `write_objective` as P2. I don't raise it -- `construct_objective` is the orchestrator, and writing the output file is a reasonable orchestrator responsibility. The contradiction: functional-architect cites the pure-function mandate from CLAUDE.md, but orchestrators are not service functions. The `extraction.py` module has `write_features` as separate, which functional-architect cites as precedent, but `write_features` is called from outside the extraction pipeline -- a different architectural context.

## Tensions

### T-1. Logging priority: P2 (functional-architect) vs not raised (spec-compliance)

Functional-architect raises logging absence as P2 (R6). I don't mention logging because no FR requires it. The tension: logging is an operational concern, not a compliance concern. The spec doesn't require logging in the construction pipeline. Functional-architect is right that `extraction.py` establishes the pattern and that classification failures need observability, but this is a code-quality item, not a spec item. P3 from a compliance perspective.

### T-2. Mode override test strengthening

Functional-architect's R8 proposes strengthening the mode override test. I agree this test is weak -- it checks `obj.mode == "cooperative"` but doesn't verify template selection matched cooperative mode. However, the *reason* the test should be strengthened differs: functional-architect wants to catch the "shadowed mode" bug (R2), I want to ensure the test actually validates what it claims. If the mode parameter is a fallback (my reading), the test should be rewritten to test a *custom* decision type that triggers the fallback path, not a standard SELECTION type where the mode parameter is correctly ignored.

### T-3. `str.replace` fix priority: P2 (functional-architect) vs P1 (spec-compliance, aligned with schema-engineer and game-theorist)

Functional-architect classifies the string substitution fix as P2. Schema-engineer, game-theorist, and I all classify it as P1. The 3-to-1 priority split suggests functional-architect's P2 classification is the outlier. Functional-architect's reasoning ("hasn't triggered yet") is valid for risk assessment but not for priority -- the fix is trivial (one regex), and the bug is one template edit away from corrupting output. P1 is correct.

### T-4. Alias map on ParameterDefinition

Functional-architect proposes alias maps for better parameter extraction recall. I don't raise this -- it's a feature addition that requires a spec amendment. The tension: functional-architect sees it as improving the existing FR-004 implementation, I see it as expanding FR-004's scope beyond the current spec. Both are valid perspectives, but from a compliance standpoint, the current conservative extraction satisfies FR-004 as written.

## Safe Agreements

### SA-1. Source map must be returned from `fill_parameter_gaps`

Both reviews identify the same root cause. Functional-architect proposes `FilledParameters` dataclass; I propose restructuring within the source dict. Compatible fixes.

### SA-2. FR-003 multi-template presentation is unimplemented

Both reviews confirm `candidates[0]` is silently used. Both classify it as P1 (functional-architect R3, spec-compliance R1). Agreement on both diagnosis and priority.

### SA-3. Pipeline architecture follows established patterns

Both reviews affirm pure functions, frozen intermediates, protocol-based DI, and deterministic behavior. The architecture is sound.
