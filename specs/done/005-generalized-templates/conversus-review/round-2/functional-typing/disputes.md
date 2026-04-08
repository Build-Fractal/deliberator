# Cooperative Disputes -- Phase 4: functional-typing

**Agent**: functional-typing
**Perspective**: Functional programming and type safety (Python FP paradigm, Pydantic v2)
**Phase**: 4 -- Final statement before synthesis
**Date**: 2026-03-21

---

## Remaining Disputes

### Dispute A: Reverse template existence check priority -- P3 standalone vs. P2-1 bundling

**Parties**: game-engine-advocate (bundle with P2-1) vs. integration-architect (P3 standalone, willing to accept P2-1 bundling) vs. functional-typing (P3 standalone).

**The disagreement**: game-engine-advocate's NR-2 proposes that the reverse template existence check (orphaned templates on disk not listed in mode schema) should be scoped as part of P2-1 (MODE_PRESENCE migration to YAML), making it "bidirectional template validation as a single deliverable." integration-architect accepts this framing but hedges: "If P2-1's scope is already too large, P3 remains defensible."

**My position**: P3 standalone is the correct scoping. P2-1 already carries meaningful scope -- migrating MODE_PRESENCE from hardcoded checks to mode schema YAML declarations. Adding a new validation direction (reverse orphan detection) inflates P2-1's surface area and testing burden. The two validations are logically related but operationally independent: P2-1 can ship without the reverse check, and the reverse check can ship after P2-1 without rework. Bundling creates an artificial coupling that risks delaying P2-1 if the reverse check reveals unexpected edge cases (e.g., template files used by multiple modes, templates that exist for documentation purposes but are not actively linted).

This is a prioritization disagreement, not an architectural one. The synthesizer should resolve it based on implementation risk appetite. I flag it because game-engine-advocate's framing ("a single concept") obscures the fact that forward validation (declared template missing from disk) and reverse validation (disk template undeclared in schema) have different failure semantics and different error-handling requirements.

**Severity**: Low. Both outcomes are acceptable. My preference is P3 standalone with a dependency note that it should follow P2-1.

### Dispute B: Systematic schema-type audit scope -- spec deliverable vs. implementation hygiene

**Parties**: functional-typing (NEW-1: bundle audit with P1-3 as P2 deliverable) vs. integration-architect (implementation hygiene during P1-3 execution, not a spec deliverable).

**The disagreement**: I proposed (NEW-1) that P1-3 implementation should include a systematic audit of all model field comments and type annotations against their schema declarations, since P1-3 already requires examining every path-like field. integration-architect's Rec 3 disposition agrees the ROUND_SYNTHESES fix is valid but explicitly rejects the broader audit as a spec deliverable: "A systematic audit is implementation hygiene during P1-3 execution, not a separate spec deliverable."

**My position**: I accept integration-architect's framing. The distinction is correct: spec deliverables define what must be built and verified; implementation hygiene describes how the implementer should approach the work. An audit is a process recommendation, not a testable artifact. I withdraw NEW-1 as a formal deliverable and reframe it as an implementation note: "When implementing P1-3, the implementer should verify each field's comment and type annotation against the corresponding schema declaration, since the ROUND_SYNTHESES drift (Rec 3) suggests broader correspondence issues." This is a note in the synthesis, not a tracked work item.

**Severity**: None. This is effectively resolved. I concede integration-architect's framing.

---

## Convergence

The following positions have reached unanimous or near-unanimous agreement across all three agents. These should be treated as settled in the final synthesis.

### 1. `ValidationConfig` Pydantic model as the API boundary
All three agents endorse. No remaining disagreement on design, priority, or scope. The docstring should include a directional hint about plugin-aware extensions (game-engine-advocate revised R1, functional-typing accepted with qualification, integration-architect did not object).

### 2. `str` with `KNOWN_ERROR_TYPES` and strict rejection validator
All three agents now agree: the `@field_validator` should **reject** unknown error types at construction time, not warn. functional-typing withdrew the warning-only proposal after both cross-reviewers independently identified it as pattern-inconsistent with mode validation and destructive of typo protection. The extension path is plugin registration into `KNOWN_ERROR_TYPES` at initialization time, mirroring the mode registration pattern.

### 3. P2 for schema version field
Unanimous. No remaining dispute.

### 4. Import fix sequenced within P1-2
Unanimous. No remaining dispute.

### 5. `PHASE_CONTEXT_MODELS` documented as extensible in P2-6
game-engine-advocate proposed (R2), functional-typing accepted (SA-4), integration-architect agreed on substance. One sentence in P2-6.

### 6. `ModeSchema` extensibility documented with `extra = "forbid"` reinforcement
game-engine-advocate revised R3 to reinforce `extra = "forbid"` (withdrawing the `extra = "ignore"` suggestion). functional-typing accepted the documentation, rejected `extra = "ignore"` as the mechanism. integration-architect identified the original suggestion as the withdrawn GE-2 argument reappearing. All three agents now agree: downstream specs add typed fields explicitly; `extra = "forbid"` catches typos; the documentation should close the `extra = "ignore"` door, not leave it ajar.

### 7. Filename-phase constraint documented in P2-6 (descriptive, not prescriptive)
integration-architect revised Rec 4 to document the constraint without prescribing how future specs handle variants. game-engine-advocate's DC-2 correctly identified the original conditional-blocks prescription as overstepping spec 005's authority. functional-typing accepted the addendum. The revised phrasing ("Template filenames map 1:1 to phase names... downstream specs should be aware that introducing multiple template files for a single phase would require linter changes") is the consensus formulation.

### 8. `validate_templates` evolution note (observational, not prescriptive)
integration-architect revised Rec 5 to an observational note with no backward-compatibility commitment. functional-typing accepted with weakened phrasing. game-engine-advocate raised a YAGNI concern. The consensus formulation: "The `validate_templates` field is boolean in v1. Granular validation control is a potential future concern but is not designed here."

### 9. SKILL.md linter invocation is a spec 008 concern, not spec 005
integration-architect withdrew Rec 1 after both cross-reviewers identified it as scope inflation. Unanimous agreement that spec 005 delivers the library API; spec 008 defines how the orchestrator calls it.

### 10. `ROUND_SYNTHESES` comment fix at P3
integration-architect's Rec 3, endorsed by all agents. Change the misleading comment, exclude from P1-3 PathList conversion.

### 11. P3-5 scope must be resolved relative to P1-4
All three agents independently converged on this: functional-typing (NEW-2), game-engine-advocate (NR-3), and integration-architect (implicitly through the original Rec disposition). The `condition` field in `variables.yml` is prose, never read by `validate.py`. P1-4's `ConfigCondition` is the typed mechanism. P3-5's scope is unclear unless the synthesizer specifies whether it extends `ConfigCondition` or formalizes the prose field into a separate grammar. This is an editorial resolution for the synthesizer, not implementation work.

### 12. Reverse template check accepted (priority disputed, concept settled)
All three agents agree the reverse template existence check is a valid "pit of success" improvement. The only disagreement is priority/bundling (see Dispute A above).

### 13. Phase-name validation for mode schema `templates` entries
integration-architect's New Rec A, which bridges the reverse template check and the filename-phase constraint. functional-typing identified the bridging need (DC-2 in cross-review). game-engine-advocate did not object. Validates that each entry in the mode schema `templates` list corresponds to a recognized phase name. Accepted at P3.

### 14. No separate `ValidationContext` dataclass
Both cross-reviewers identified the dual-abstraction risk. functional-typing withdrew. The parameter-count concern is real but should be addressed by deriving internal state from `ValidationConfig`, not by introducing a parallel configuration object.

### 15. `itertools.product` in test generators deprioritized
functional-typing maintains as P3 but acknowledges game-engine-advocate's point that it dilutes signal. On the record as a minor readability improvement; should not consume synthesis attention.

---

## Final Position Statement

### Non-Negotiables

These are positions I will not yield on. They represent type-safety and functional-programming principles that are load-bearing for spec 005's correctness.

1. **`ValidationConfig` as the sole public configuration model.** No parallel `ValidationContext`, no untyped `**kwargs`, no pre-emptive plugin parameters. One Pydantic model, extended by downstream specs via field addition with defaults. This is the foundation of the programmatic API's type safety.

2. **Strict rejection for unknown error types.** The `@field_validator` on `LintError.error_type` must raise `ValueError` for types not in `KNOWN_ERROR_TYPES`. Warning-only validation defeats typo protection, creates pattern inconsistency with mode validation, and is unnecessary given the plugin registration path. I conceded my warning-only proposal in this round; the concession is final.

3. **`extra = "forbid"` on all Pydantic models, with no documented exceptions.** The `extra = "ignore"` suggestion was correctly identified as the withdrawn GE-2 argument reappearing through documentation. The consensus is unanimous. Downstream specs add typed fields explicitly; unknown fields are validation errors. P2-6 should close this door, not hedge.

4. **P1-1 (purify schema-loading) is the highest-leverage change.** `sys.exit()` inside library functions is the most severe functional-programming violation in the current codebase. `SchemaLoadError` restores composability, testability, and caller control. This must not be deprioritized or deferred.

5. **P1-3 (PathList custom type) must use Pydantic v2's `BeforeValidator` pattern.** The `Annotated[list[Path], BeforeValidator(parse_newline_paths)]` approach is the standard Pydantic v2 mechanism for custom deserialization. Ad hoc string-splitting in property accessors is an antipattern that P1-3 eliminates.

### Flexibility

These are positions where I am willing to accept alternative formulations without compromising my core concerns.

1. **Reverse template check priority.** I prefer P3 standalone over P2-1 bundling, but either outcome is acceptable. The synthesizer should decide based on P2-1's implementation scope.

2. **Systematic audit framing.** I withdraw NEW-1 as a formal deliverable. An implementation note in the synthesis is sufficient. integration-architect's "implementation hygiene" framing is correct.

3. **`ValidationConfig` docstring specificity.** I prefer the directional hint without field names ("downstream specs may extend this model with plugin-aware configuration fields"), but game-engine-advocate's further-narrowed formulation is also acceptable. The key constraint is that spec 005's docstring must not prescribe a specific parameter name or type signature that belongs to spec 007.

4. **`itertools.product` in test generators.** P3, not load-bearing for the review. I keep it on the record but do not press for synthesis inclusion if the synthesizer judges it noise.

5. **P3-5 scope resolution.** I proposed two options (extend `ConfigCondition` vs. formalize prose `condition`). I do not have a strong preference between them; I only insist that the synthesizer makes the scoping decision explicit rather than leaving the ambiguity for implementers to discover.

6. **Phase-name validation for mode schema `templates` entries.** integration-architect's New Rec A is sound. I accept P3 priority. If the synthesizer bundles it with P2-1 (per game-engine-advocate's framing), that is also acceptable.

---

## Deliberation Assessment

This deliberation has converged. The Round 2 cross-review process produced two genuine corrections to my review (warning-only validator and dual-abstraction `ValidationContext`), both identified independently by both cross-reviewers. Both corrections were refinements I proposed beyond the synthesizer's Round 1 resolutions, and both were correctly identified as overreach. The corrections did not reverse any Round 1 dispute resolution -- the Round 1 synthesis is stable through Round 2.

The remaining disputes are prioritization disagreements (P2-1 bundling vs. P3 standalone) and framing disagreements (spec deliverable vs. implementation hygiene). Neither involves architectural or type-safety disagreement. The 15 convergence items represent the substantive output of the deliberation: a prioritized, typed, composable action plan for spec 005 that respects the freeze-first principle and preserves spec 007's design freedom.

No agent has reversed a Round 1 concession. All three agents have made additional Round 2 concessions in response to cross-review feedback. The deliberation process is working as designed.
