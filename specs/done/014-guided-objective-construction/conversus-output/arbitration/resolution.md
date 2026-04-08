# Arbitration Resolution -- Spec 014: Guided Objective Construction

**Date**: 2026-03-24
**Arbitrator**: conversus (Phase 6)
**Spec**: `specs/014-guided-objective-construction/spec.md`
**Synthesis**: `conversus-output/summary/final.md`

---

## Process Note

This arbitration resolves three surviving disputes from the four-agent deliberation on spec 014's guided objective construction pipeline. The deliberation achieved 100% convergence on the four P1 items themselves; the disputes concern scope, value strategy, and test priority -- not whether the items belong in P1.

The arbitrator reviewed: the conversus README (grounding on the system's purpose and architectural invariants), the final synthesis, and all four agents' dispute filings. Rulings below are binding. Implementation proceeds under these terms.

---

## Decision Framework

Three criteria govern these rulings:

1. **Spec fidelity**: MUST-level requirements in the spec are non-negotiable. A fix that leaves a MUST unsatisfied is not a fix.
2. **Marginal cost vs marginal risk**: When the cost of the broader scope is trivial (~30 lines), the burden of proof falls on the party arguing for deferral, not on the party arguing for inclusion.
3. **Pipeline as bridge**: Spec 014's pipeline serves as the bridge between `/conversus` mode and the plugin system. Decisions should favor the pipeline being self-contained and usable at the point of delivery, not requiring follow-up work to become functional.

---

## Binding Decisions

### Dispute A: FR-003 Implementation Scope

**Positions**: 3 agents (game-theorist, functional-architect, spec-compliance) want P1 to include the `TemplateSelector` protocol, `InteractiveTemplateSelector`, `NonInteractiveTemplateSelector`, and the `template_selector` parameter on `construct_objective`. 1 agent (schema-engineer) wants P1 limited to the callback parameter, with implementations deferred to P2.

**Ruling: Full implementation ships as P1. The 3-1 majority is sustained.**

Reasoning:

- FR-003 uses MUST language: "present them to the user with plain-language descriptions and ask for selection." A callback parameter that defaults to auto-selecting `candidates[0]` does not present anything to anyone. It is infrastructure for compliance, not compliance itself.
- Schema-engineer's argument that "P1 is the contract, P2 is the behavior" draws a distinction the spec does not. The spec requires behavior, not a contract. The contract is a means to deliver the behavior.
- The cost is ~30 lines of code for both implementations, following the established `InteractiveGapFiller` / `NonInteractiveGapFiller` pattern already present in the codebase. This is not a case where deferral saves meaningful engineering effort.
- A shipped pipeline that claims FR-003 compliance but cannot actually present templates to a user undermines the pipeline's purpose as a functional bridge to the plugin system.

**Required deliverables for P1-FEAT-1**:
1. `TemplateSelector` protocol with `select(candidates: list[ObjectiveTemplate], descriptions: list[str]) -> ObjectiveTemplate`
2. `InteractiveTemplateSelector` -- prints descriptions, prompts for choice (mirrors `InteractiveGapFiller`)
3. `NonInteractiveTemplateSelector` -- returns `candidates[0]`
4. `template_selector` parameter on `construct_objective`, defaulting to `NonInteractiveTemplateSelector()`

### Dispute B: `problem_md` Value Strategy

**Positions**: 3 agents (schema-engineer, functional-architect, spec-compliance) want `problem_md` required with a `PROBLEM_MD_STDIN` sentinel constant (`"<stdin>"`) as the default. 1 agent (game-theorist) wants `problem_md` required but with no sentinel -- callers provide descriptive strings like `"programmatic"` or `"test"`.

**Ruling: Sentinel constant with override capability. The 3-1 majority is sustained, with a refinement.**

Reasoning:

- Both sides agree `problem_md` must be required. The dispute is purely about the default value when callers do not have a file path.
- Game-theorist's concern about magic strings is valid in principle but mitigated in practice. A named constant (`PROBLEM_MD_STDIN = "<stdin>"`) is greppable, documented by its name, and explicitly signals "this is the default, override me if you have something better." This is a standard pattern for typed sentinel values.
- Game-theorist's alternative -- callers providing ad-hoc strings like `"programmatic"` or `"test"` -- creates the opposite problem: unpredictable, un-greppable, un-checkable values that vary across callers. The sentinel gives the ecosystem a canonical fallback; callers who have richer provenance information override it.
- The synthesizer's assessment is correct: the two approaches are compatible. The constant provides discoverability; caller override provides flexibility.

**Required deliverables for P1-FEAT-2**:
1. `PROBLEM_MD_STDIN: str = "<stdin>"` constant defined at module level
2. `SourceProvenance.problem_md: str` required, no default on the model itself
3. `construct_objective` accepts `problem_md_path: str = PROBLEM_MD_STDIN` and threads it into `SourceProvenance`
4. Callers may pass any descriptive string; the constant is the documented fallback, not a constraint

### Dispute C: Retry Test Priority

**Positions**: 3 agents (game-theorist, functional-architect, spec-compliance) classify the retry/re-ask test (FR-007) as P2. 1 agent (schema-engineer) classifies it as P3.

**Ruling: P2, explicitly ranked last within the P2 tier. The 3-1 majority is sustained with acknowledgment of schema-engineer's bandwidth concern.**

Reasoning:

- FR-007 is a MUST requirement. The implementation exists and is correct by inspection, but correctness-by-inspection is not a testing strategy. An untested MUST is a regression vector: if the retry logic is accidentally broken in a future refactor, nothing catches it.
- Schema-engineer's argument -- "the code works, testing it doesn't change compliance" -- is true today and irrelevant tomorrow. Tests exist to preserve properties across changes, not to verify properties at a single point in time.
- However, spec-compliance's own filing acknowledges this is the lowest-priority P2 item, ranking below GapFillRefused, boolean coercion, and logging. This is correct. The test does not block shipping. It blocks closing the P2 tier.
- The test design is already specified: `SequentialGapFiller` with `["invalid", "999", "5.0"]` for a range-constrained parameter. This is a single test function, not a test suite.

**Required deliverable for P2-7**:
1. Priority: P2, ranked last within the P2 tier (after GapFillRefused, boolean coercion, logging, provenance tags, FR-014 utility, and LLMGapFiller design)
2. Implementation: `SequentialGapFiller` with invalid-then-valid sequence, asserting third answer accepted
3. Classification: Required for P2 tier completion, not for P1 acceptance gate

---

## Summary of Changes Required

### To the implementation plan (final.md scorecard):

| ID | Before | After | Change |
|---|---|---|---|
| **FEAT-1** | P1, scope disputed (3-1) | P1, full scope binding | Protocol + both implementations + parameter. No partial delivery. |
| **FEAT-2** | P1, value strategy disputed (3-1) | P1, sentinel constant binding | `PROBLEM_MD_STDIN` constant as default; callers override freely. |
| **TEST-2** | P2, priority disputed (3-1) | P2, last in tier, binding | Required for P2 completion. Does not gate P1 acceptance. |

### No changes to:

- The four P1 items as a unit (unanimous, locked)
- The P2 tier composition (all items remain P2)
- The P3 tier (all items remain P3)
- Architecture assessment (unanimously sound)
- Dispute D from synthesis (constraint wiring P3, resolved by concession -- no arbitration needed)

### Acceptance gate for spec 014:

The pipeline is ready for P1 acceptance when all four P1 items are implemented per the rulings above. The P2 tier is a follow-up commitment, not a blocker. The architecture is sound, the agent convergence is strong (100% on P1 items from divergent starting positions), and the remaining work is well-scoped.
