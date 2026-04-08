# Round 2 Revision: functional-typing

**Agent**: functional-typing
**Perspective**: Functional programming and type safety (Python FP paradigm, Pydantic v2)
**Round**: 2 of 2 (Revision after cross-reviews)
**Date**: 2026-03-21

---

## Recommendation Dispositions

### From My Round 2 Review

#### REC-1: Dispute 1 -- Accept `ValidationConfig` model
**Original position**: Accept synthesizer's `ValidationConfig` Pydantic model as the API boundary.
**Cross-review feedback**: game-engine-advocate (SA-1) and integration-architect (SA-3) both endorse. No challenges.
**Disposition**: **Maintained.** Unanimous agreement across all three agents. No revision needed.

#### REC-2: Dispute 2 -- Accept `str` with `KNOWN_ERROR_TYPES`; warning-only validator for unknown types
**Original position**: Accept `str` with `@field_validator` against `KNOWN_ERROR_TYPES: frozenset[str]`, but the validator should issue a **warning** for unknown types rather than raise `ValueError`.
**Cross-review feedback**: Both game-engine-advocate (DC-1) and integration-architect (DC-1) flag the warning-only proposal as a dangerous contradiction. game-engine-advocate argues it breaks pattern consistency with mode validation (which rejects unknowns) and loses typo protection. integration-architect concurs, noting that a warning-only validator lets `"missing_variabel"` pass silently.
**Disposition**: **Withdrawn.** The cross-reviews are correct. My concern about "recreating the Literal problem in runtime form" was unfounded -- a `frozenset` extended programmatically at load time is fundamentally different from a source-code `Literal` that requires redeployment. The mode validation precedent should hold: unknown error types are rejected at `LintError` construction. Plugins register their types into `KNOWN_ERROR_TYPES` at initialization, before producing errors. This gives typo protection without requiring source-code modification. I concede this refinement entirely.

#### REC-3: Dispute 3 -- Accept P2 for schema version field
**Original position**: Accept P2 priority.
**Cross-review feedback**: No challenges from either reviewer.
**Disposition**: **Maintained.** No revision needed.

#### REC-4: Dispute 4 -- Accept import fix as part of P1-2
**Original position**: Accept synthesizer's sequencing.
**Cross-review feedback**: No challenges from either reviewer.
**Disposition**: **Maintained.** No revision needed.

#### REC-5 / MO-1: Introduce frozen `ValidationContext` dataclass for `validate_template` internal parameters
**Original position**: A frozen `ValidationContext` dataclass (distinct from the public `ValidationConfig` Pydantic model) bundling `variables_schema`, `mode_schema`, and `all_var_names` to reduce `validate_template`'s parameter count. Priority P2.
**Cross-review feedback**: Both game-engine-advocate (DC-2) and integration-architect (DC-2) flag this as creating a dangerous dual-abstraction pattern. game-engine-advocate argues that two configuration objects with overlapping concerns creates "which config do I update?" maintenance bugs. integration-architect notes the architectural coordination gap -- `ValidationConfig` and `ValidationContext` would have a dependency relationship designed across separate priority tiers. game-engine-advocate proposes deriving internal state from `ValidationConfig` via a factory function instead.
**Disposition**: **Revised.** The cross-reviews identify a real coordination risk I did not adequately address. I withdraw the separate `ValidationContext` dataclass. The parameter-count concern remains legitimate (`validate_template` taking 6+ parameters is unwieldy), but the solution should be internal derivation from `ValidationConfig`, not a parallel abstraction. Concretely: when P1-2 ships `ValidationConfig`, the `validate_all` function should construct the schemas and pass them as direct parameters or as properties derived from the config instance. If parameter proliferation becomes unmanageable after P1-2 and P1-4 land, a derived internal view can be introduced at that point -- but it should be designed in coordination with `ValidationConfig`, not independently at a different priority tier.

#### REC-6 / MO-2: Use `itertools.product` in test case generators
**Original position**: Use `itertools.product` in test case generators where it improves readability over nested list comprehensions. Priority P3.
**Cross-review feedback**: game-engine-advocate (T-2) notes this is technically sound but "noise by the review's own standard" in a Round 2 focused on architectural disputes. integration-architect (T-2) flags the optics of proposing another `itertools`-based refactor after the Round 1 `itertools.chain` withdrawal, but leans toward accepting it as distinct (test utilities vs. production error handling).
**Disposition**: **Maintained at P3 but deprioritized.** The recommendation is technically correct and the venue is genuinely different (test case generation, not production error aggregation). However, game-engine-advocate is right that it dilutes signal in a Round 2 review. I keep it on the record as a minor readability improvement but acknowledge it should not consume synthesis attention alongside the architectural items.

#### REC-7 / OBA-2: Clarify `condition` field's relationship to `config_conditions` (P1-4)
**Original position**: The `condition` field in `variables.yml` is documentation-only (never read by `validate.py`), and P3-5 (formalize condition syntax) should specify whether it extends, replaces, or complements P1-4's `config_conditions`.
**Cross-review feedback**: game-engine-advocate (T-1) accepts the analysis as correct but notes the implication is stronger than I stated: if P1-4's `ConfigCondition` is the machine-readable mechanism, P3-5's scope shrinks to "make the documentation string parseable for... what consumer?" integration-architect (T-3) identifies a complementary finding (ROUND_SYNTHESES type mismatch) and suggests both are instances of a broader spec-implementation divergence pattern needing systematic audit.
**Disposition**: **Strengthened.** game-engine-advocate's sharpening is correct: P3-5's scope must be explicitly defined relative to P1-4. Either P3-5 adds new condition types to the `ConfigCondition` model (useful, but then it is a P1-4 extension, not a separate item), or P3-5 formalizes the prose `condition` field into a separate grammar (redundant with P1-4 and of unclear value). The synthesis should resolve this scoping question. Additionally, integration-architect's observation about ROUND_SYNTHESES suggests the `condition` field issue is not isolated -- a systematic audit of schema-type-to-implementation-type correspondence should accompany P1-3 (PathList conversion), since that work already requires examining every field.

#### OBA-1: Synthesizer's "no external consumers" reasoning needs qualification
**Original position**: The synthesizer's reasoning that "no external consumers means non-breaking" is imprecise; internal tests are consumers.
**Cross-review feedback**: game-engine-advocate (T-3) agrees but notes it is a reasoning shortcut on an already-resolved dispute. integration-architect (T-1) agrees it is correct but applies to a resolved dispute with no actionable consequence for Round 2.
**Disposition**: **Maintained as editorial note.** Both cross-reviews agree the observation is valid. Both also agree it has no actionable consequence since the `ValidationConfig` model resolves the practical concern. I keep this on the record as a principle clarification: "no external consumers" is not a general justification for breaking changes, and future specs should not cite it. But I do not elevate it to a recommendation.

---

### From Cross-Reviews of Other Agents

#### game-engine-advocate R1: Refine `ValidationConfig` docstring to specify anticipated plugin extension
**game-engine-advocate's position**: The docstring should specify `known_plugin_variables: frozenset[str]` as the anticipated extension, not just "spec 007 may extend this model."
**My cross-review assessment (DC-2)**: I flagged this as mild scope inflation -- encoding a specific parameter name commits spec 005 to an extension shape that spec 007 has not yet designed. The "freeze first, compose later" principle suggests the docstring should be deliberately vague.
**Disposition after reading integration-architect's cross-review**: integration-architect did not challenge this recommendation. game-engine-advocate's framing as "zero cost" is slightly misleading (a specific parameter name in a docstring creates an implicit contract), but the practical risk is genuinely low -- docstrings are trivially updated. I **accept with qualification**: the docstring should note that plugin-variable awareness is an anticipated extension direction, but should not commit to a specific parameter name or type signature. Phrasing like "Anticipated extensions include plugin-variable awareness (see spec 007)" is preferable to `known_plugin_variables: frozenset[str]`.

#### game-engine-advocate R2: Include `PHASE_CONTEXT_MODELS` in P2-6 extension contract
**game-engine-advocate's position**: Document `PHASE_CONTEXT_MODELS` as explicitly extensible in P2-6 to prevent future re-addition of `Final`.
**My cross-review assessment (SA-4)**: Safe agreement. The FT-8 withdrawal was unanimous but undocumented outside deliberation artifacts.
**Disposition**: **Accept.** One sentence in P2-6, no cost, prevents regression.

#### game-engine-advocate R3: Note `ModeSchema` field-level extensibility in P2-6
**game-engine-advocate's position**: P2-6 should document that downstream specs may add fields to `ModeSchema`, with unknown fields handled gracefully (either `extra = "ignore"` or version-aware loading).
**My cross-review assessment (T-2)**: I flagged tension with the `extra = "forbid"` consensus. The suggestion to consider `extra = "ignore"` on `ModeSchema` would be the first exception.
**Disposition**: **Accept the documentation, reject `extra = "ignore"` as the mechanism.** P2-6 should acknowledge that `ModeSchema` is an extension point for field additions. But the extension mechanism should follow the same pattern as `TemplateContext`: downstream specs add fields explicitly (via model update or subclass), and `extra = "forbid"` continues to catch typos. The alternative (`extra = "ignore"`) silently swallows typos in mode schema YAML, which is the failure mode `extra = "forbid"` was designed to prevent.

#### game-engine-advocate R4: Add schema version compatibility note to P2-4
**game-engine-advocate's position**: Note in P2-4 that schema version compatibility validation is deferred to the spec introducing schema version 2.0.
**My cross-review assessment**: Not directly addressed in my cross-review, but consistent with "freeze first, compose later."
**Disposition**: **Accept.** Low-cost documentation that prevents premature implementation.

#### integration-architect Rec 1: Update SKILL.md `allowed-tools` for linter invocation
**integration-architect's position**: SKILL.md Step 3 should specify `Bash` tool with `uv run python linter/validate.py --mode {mode}`, and `allowed-tools` should be updated.
**My cross-review assessment (DC-1)**: I flagged this as contradicting the P1-2 programmatic API's purpose. If the programmatic API is the right abstraction, the invocation should use it as a library call, not shell out to the CLI. Recommending CLI shell-out in spec 005 is scope inflation -- SKILL.md invocation is a spec 008 concern.
**Disposition**: **Reject for spec 005 scope.** The linter invocation pathway from SKILL.md is a spec 008 (executable conversus) concern. Spec 005 delivers the library API and the CLI tool. How the orchestrator calls either is spec 008's design decision. Adding `allowed-tools` entries to spec 005's deliverables conflates the library layer with the orchestration layer.

#### integration-architect Rec 2: Add reverse template existence check
**integration-architect's position**: The linter should report template files on disk not listed in the mode schema's `templates` field.
**My cross-review assessment**: I noted a subtle tension with Rec 4 (filename-phase constraint) when both are applied, but the reverse check itself is sound.
**Disposition**: **Accept at P3.** Orphan template detection is a legitimate "pit of success" improvement. The tension with Rec 4 is resolvable: validate the mode schema's `templates` list against known phase names, making both checks reinforce rather than conflict.

#### integration-architect Rec 3: Fix `ROUND_SYNTHESES` comment in models.py
**integration-architect's position**: Change `# newline-separated paths` to `# pre-formatted synthesis content per round` and exclude from P1-3 PathList conversion.
**My cross-review assessment (SA-7)**: Safe agreement. The explicit exclusion prevents mechanical over-application of PathList.
**Disposition**: **Accept at P3.** Prevents a real bug during P1-3 implementation.

#### integration-architect Rec 4: Document filename-phase constraint in P2-6
**integration-architect's position**: Template filenames must match phase names exactly; variant templates use conditional blocks, not separate files.
**My cross-review assessment (DC-2)**: I noted tension with Rec 2 when both are applied simultaneously, but the constraint documentation itself is sound.
**Disposition**: **Accept as P2-6 addendum.** The filename-phase constraint is load-bearing and undocumented. Documenting it in the "NOT extension points" section of P2-6 is the right venue. The tension with Rec 2 is resolved by requiring the mode schema `templates` list to only contain recognized phase names, making both checks reinforce each other.

#### integration-architect Rec 5: Note `validate_templates` evolution path in P2-6
**integration-architect's position**: Document that `validate_templates` may evolve from boolean to structured config, with boolean remaining valid for backward compatibility.
**My cross-review assessment (T-3)**: I flagged that committing to backward compatibility of the boolean form contradicts "freeze first, compose later." The phrasing "must remain valid" is stronger than warranted.
**Disposition**: **Accept with weakened phrasing.** Document that `validate_templates` may evolve to structured config, but do NOT commit to backward compatibility of the boolean form. Phrasing should be: "The `validate_templates` field is boolean in v1. Future specs may replace or extend this to a structured config." This preserves spec 007's freedom to design the structured form without being constrained by a backward-compatibility commitment made prematurely.

---

## New Recommendations

### NEW-1: Systematic schema-type-to-implementation audit alongside P1-3
**Source**: Convergence of my OBA-2 (condition field as prose), integration-architect's MO-3 (ROUND_SYNTHESES comment drift), and integration-architect's cross-review T-3 (both are instances of the same pattern).
**Recommendation**: When P1-3 (PathList custom type) is implemented, conduct a systematic audit of all model field comments and type annotations against their corresponding schema declarations in `variables.yml`. The ROUND_SYNTHESES and `condition` field issues suggest broader drift between the schema's declared types and the model's implemented types/comments. P1-3 already requires examining every path-like field; extending this to a full correspondence check adds minimal marginal effort.
**Priority**: P2 (bundled with P1-3 implementation, no separate deliverable).

### NEW-2: P3-5 scope resolution relative to P1-4
**Source**: My OBA-2, strengthened by game-engine-advocate's T-1.
**Recommendation**: The synthesis should explicitly resolve P3-5's scope: does it (a) add new condition types to P1-4's `ConfigCondition` model, or (b) formalize the prose `condition` field in `variables.yml` into a separate parseable grammar? Option (a) is useful and should be folded into P1-4's future extensions. Option (b) is of unclear value since `validate.py` never reads the `condition` field and `ConfigCondition` already provides the machine-readable mechanism. If (b), the synthesis should identify the consumer that would parse the formalized condition.
**Priority**: Editorial (synthesis scoping clarification, not implementation work).

---

## Position Summary

### Maintained Positions
1. **`ValidationConfig` Pydantic model as API boundary** -- unanimous agreement, no revision.
2. **`str` with `KNOWN_ERROR_TYPES` for `error_type`** -- type choice maintained (warning-only refinement withdrawn; see below).
3. **P2 for schema version field** -- maintained.
4. **Import fix as part of P1-2** -- maintained.
5. **P1-1 (purify schema-loading) is highest-leverage change** -- maintained, unanimous.
6. **P1-3 (PathList custom type) is the right Pydantic v2 approach** -- maintained.
7. **P2-5 (frozen=True on TemplateContext) with composition for plugins** -- maintained.
8. **`itertools.product` in test generators (P3)** -- maintained but deprioritized.
9. **OBA-1 (non-breaking qualification)** -- maintained as editorial note, not elevated to recommendation.

### Withdrawn Positions
1. **Warning-only `@field_validator` for unknown error types** (Dispute 2 refinement) -- withdrawn after both cross-reviews correctly identified this as breaking pattern consistency with mode validation and losing typo protection. The `frozenset` extended at load time resolves the plugin extensibility concern without weakening validation.
2. **Separate `ValidationContext` frozen dataclass** (MO-1) -- withdrawn after both cross-reviews identified the dual-abstraction maintenance hazard. Parameter-count concerns should be addressed by deriving internal state from `ValidationConfig`, not by introducing a parallel configuration object.

### Refined Positions
1. **game-engine-advocate's docstring recommendation** -- accepted with qualification: document plugin-variable awareness as an anticipated extension direction, but do not commit to a specific parameter name or type signature.
2. **integration-architect's `validate_templates` evolution note** -- accepted with weakened phrasing: do not commit to backward compatibility of the boolean form.
3. **OBA-2 (condition field analysis)** -- strengthened by game-engine-advocate's sharpening: P3-5's scope must be explicitly resolved relative to P1-4.

### Concessions from Round 1 (all maintained)
1. FT-3 withdrawal (extra = "forbid" deferred to P2)
2. FT-8 withdrawal (no `Final` on `PHASE_CONTEXT_MODELS`)
3. FT-5 modification (Literal to str with validation for modes)
4. `itertools.chain.from_iterable` withdrawal (error aggregation)
5. FT-7 deferral (PathList conversion details)

### New Concessions in Round 2
6. Warning-only `@field_validator` on `error_type` -- withdrawn.
7. Separate `ValidationContext` dataclass -- withdrawn.

---

## Deliberation Health Assessment

The cross-review process in Round 2 produced two genuine corrections to my review (warning-only validator and dual-abstraction pattern), both identified independently by both cross-reviewers. This convergent criticism is the strongest signal that the corrections are substantive rather than positional. Neither correction changes the Round 1 dispute resolutions -- both were refinements I proposed beyond the synthesizer's resolutions, and both were correctly identified as overreach.

The deliberation has no remaining architectural disputes. All positions are either unanimous or narrowed to documentation phrasing. The Round 1 synthesis is stable through Round 2 without reversal from any agent.
