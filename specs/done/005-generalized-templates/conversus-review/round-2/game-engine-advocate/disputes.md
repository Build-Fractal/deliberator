# Game Engine Advocate -- Final Disputes and Convergence (Round 2)

**Reviewer role**: game-engine-advocate (spec 007)
**Target**: spec 005 -- Generalized Template Schema, Variables, and Linter
**Phase**: 4 (Final Disputes -- Round 2)
**Date**: 2026-03-21

---

## Remaining Disputes

### Dispute A: `error_type` validator must reject unknown types, not warn

**Disputed with**: functional-typing (withdrawn by functional-typing in revision, but the synthesizer must still specify behavior)

functional-typing's Round 2 review proposed a warning-only `@field_validator` for unknown error types on `LintError`. Both integration-architect and I independently identified this as a dangerous contradiction with the mode validation pattern. functional-typing withdrew the proposal in revision, conceding that "a `frozenset` extended programmatically at load time is fundamentally different from a source-code `Literal` that requires redeployment."

The withdrawal resolves the inter-agent dispute. However, the synthesizer's Round 1 resolution of Dispute 2/3 specifies the mechanism (`str` with `@field_validator` against `KNOWN_ERROR_TYPES`) without specifying the enforcement behavior. All three agents now agree on rejection semantics, but this agreement exists only in deliberation artifacts. The synthesis must state it explicitly:

1. `KNOWN_ERROR_TYPES` is constructed at module load time from a base set plus any plugin-registered error types.
2. The `@field_validator` raises `ValueError` for types not in the constructed set.
3. Plugin initialization includes error type registration before any `LintError` construction.

This is not a new dispute between agents. It is a gap in the Round 1 synthesis that all three agents have now converged on filling with the same answer. The dispute is with the ambiguity, not with another reviewer.

**Status**: Convergent in substance, requires synthesizer specification. All three agents agree: reject, not warn.

---

### Dispute B: Reverse template existence check should be scoped within P2-1, not deferred to P3

**Disputed with**: integration-architect (priority, not substance)

integration-architect's Rec 2 proposes a reverse template existence check (templates on disk not listed in mode schema YAML) at P3 priority. I argued in my cross-review (T-1) that when P2-1 makes the mode schema `templates` list authoritative, bidirectional validation is a single logical concept: templates listed but not on disk (already validated) and templates on disk but not listed (the reverse check) are symmetric failure modes. Splitting them across priority tiers creates a window where the `templates` list is authoritative in one direction but not the other.

integration-architect's revision accepts this reasoning: "I accept this reasoning -- the reverse check is logically part of making the `templates` list authoritative. If the synthesizer bundles it with P2-1, I support that."

functional-typing's revision also accepts: "Accept at P3. Orphan template detection is a legitimate 'pit of success' improvement."

The remaining question is synthesizer discretion on scoping. My position: P2-1 should include bidirectional validation as a single deliverable. integration-architect defers to the synthesizer. functional-typing accepts at P3. The substance is agreed; only the packaging differs.

**Status**: Substance converged. Priority is a synthesizer scoping decision. My recommendation: bundle with P2-1.

---

## Convergence

### Convergence 1: All four Round 1 dispute resolutions are stable (unanimous)

All three agents accept all four of the synthesizer's Round 1 dispute resolutions without reversal:

1. **Dispute 1** (API parameter design): `ValidationConfig` Pydantic model accepted. My Round 1 non-negotiable (`known_plugin_variables` as a typed parameter) is fully satisfied by the model pattern, which absorbs new fields with defaults. I narrowed my docstring request further after cross-review -- from a specific field-name prescription to a directional hint ("downstream specs, particularly spec 007, may extend this model with plugin-aware configuration fields"). Both cross-reviewers correctly identified the original field-name prescription as scope inflation in prose form.

2. **Dispute 2** (no `dict[str, Any]` on TemplateContext): Fully closed. No agent proposes untyped extension fields. Composition via separate `PluginContext` (spec 007) is the agreed architecture.

3. **Dispute 3** (error_type as `str`, not `Literal`): Type choice fully closed. Enforcement behavior converged to rejection semantics (see Dispute A above for the specification gap).

4. **Dispute 4** (import fix sequencing): Fully closed. Import fix is part of the P1-2 programmatic API unit of work.

No Round 1 synthesis resolution has been reversed, weakened, or re-litigated by any agent in Round 2. The synthesis is stable.

### Convergence 2: `PHASE_CONTEXT_MODELS` belongs in P2-6 extension contract documentation (unanimous)

All three agents agree that `PHASE_CONTEXT_MODELS` should be documented as an explicitly extensible registry in P2-6. functional-typing (SA-4): "Including `PHASE_CONTEXT_MODELS` in P2-6's extension points list costs one sentence and prevents a future implementer from re-adding `Final`." integration-architect agrees on substance. My position is maintained: one sentence in an already-planned deliverable, zero marginal cost, prevents regression of the FT-8 withdrawal.

### Convergence 3: `ModeSchema` extensibility documentation must reinforce `extra = "forbid"` (unanimous)

My original R3 suggested `extra = "ignore"` as one possible extension mechanism for `ModeSchema`. Both cross-reviewers identified this as the withdrawn GE-2 argument (`extra = "allow"`) reappearing through documentation. I conceded and revised: the P2-6 documentation should state that downstream specs add typed fields to `ModeSchema` explicitly, and that `extra = "forbid"` remains in effect. Unknown fields in mode schema YAML are validation errors, not silent extensions. All three agents now agree on this formulation.

### Convergence 4: Filename-phase constraint documentation should be descriptive, not prescriptive (unanimous)

integration-architect's original Rec 4 prescribed that "variant templates for the same phase must use conditional blocks within a single template, not separate files." I identified this (DC-2) as the same scope-inflation pattern the Round 1 deliberation corrected in my original recommendations -- prescribing how future specs must handle a constraint rather than documenting the constraint itself. integration-architect accepted and revised: "Document the constraint. Remove the prescription." The agreed formulation: "Template filenames map 1:1 to phase names (`phase = tmpl_path.stem`). This is a load-bearing assumption in the linter. Downstream specs that need per-phase variants should be aware that introducing multiple template files for a single phase would require linter changes."

### Convergence 5: `validate_templates` evolution note should be observational, not prescriptive (unanimous)

integration-architect's original Rec 5 committed to backward compatibility of the boolean form: "the boolean form must remain valid." functional-typing and I both flagged this as contradicting "freeze first, compose later." integration-architect revised to observational phrasing: "The `validate_templates` field is boolean in v1. Granular validation control is a potential future concern but is not designed here." No backward-compatibility commitment, no shape suggestion. All three agents agree.

### Convergence 6: SKILL.md linter invocation is a spec 008 concern, not spec 005 (unanimous)

integration-architect withdrew Rec 1 after both functional-typing and I identified it as scope inflation into spec 008's domain. functional-typing provided the sharpest critique: recommending CLI shell-out in spec 005 contradicts the P1-2 programmatic API's purpose. The SKILL.md invocation pathway belongs to spec 008 (executable conversus). All three agents agree on the withdrawal.

### Convergence 7: `ROUND_SYNTHESES` comment fix and PathList exclusion (unanimous)

integration-architect's Rec 3 (fix the misleading "newline-separated paths" comment on `ROUND_SYNTHESES` and exclude it from P1-3 PathList conversion) is accepted by all three agents at P3. functional-typing extends the observation to recommend a systematic audit of schema-type-to-implementation-type correspondence alongside P1-3. I agree the point fix is correct and the audit is good implementation hygiene, though it need not be a separate spec deliverable.

### Convergence 8: P3-5 scope must be resolved relative to P1-4 (functional-typing + game-engine-advocate)

functional-typing's OBA-2 identified that the `condition` field in `variables.yml` is prose documentation, not a parseable expression, and that `validate.py` never reads it. I sharpened this (T-1 in my cross-review): if P1-4's `ConfigCondition` is the machine-readable mechanism, P3-5's scope is unclear. functional-typing strengthened this in revision, proposing that the synthesis explicitly resolve whether P3-5 (a) extends `ConfigCondition` with new condition types, or (b) formalizes the prose `condition` field into a separate grammar. Option (a) is useful. Option (b) is redundant with P1-4 and of unclear value. integration-architect's Rec A (validate templates against phase names) is a separate but complementary finding that reinforces the need for systematic schema-implementation correspondence checking.

### Convergence 9: New bridging validation -- mode schema `templates` entries against known phase names (integration-architect + game-engine-advocate)

integration-architect's New Rec A proposes validating that each entry in the mode schema `templates` list corresponds to a recognized phase name. This bridges the reverse template check (Rec 2) and the filename-phase constraint (Rec 4) into a coherent three-part validation chain: (1) every template on disk must be declared in the schema, (2) every declaration must correspond to a recognized phase, (3) every recognized phase must have a template on disk. functional-typing endorses this bridging logic. All three agents agree on the concept; priority depends on whether the reverse check is bundled with P2-1 or deferred to P3.

### Convergence 10: `ValidationConfig` docstring should use directional hint, not field-name prescription

My original R1 proposed encoding `known_plugin_variables: frozenset[str]` in the `ValidationConfig` docstring. Both cross-reviewers independently identified this as scope inflation -- the same pattern I conceded 7 times in Round 1, applied to prose. I conceded and narrowed to a directional hint: "downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields." functional-typing accepted with the qualification that the docstring should not commit to a specific parameter name. The agreed formulation avoids prescribing a design that belongs to spec 007.

---

## Final Position Statement

### Trajectory

This deliberation began with 10 recommendations from my perspective. Seven were correctly identified as scope inflation in Round 1 and conceded -- each on the basis of a specific, concrete argument rather than abstract scope hygiene. The Round 1 synthesis resolved all four remaining disputes. Round 2 introduced documentation-level refinements. After Round 2 cross-reviews, I made two additional concessions (R1 docstring specificity, R3 `extra = "ignore"` suggestion), both identified independently by both cross-reviewers as recurrences of the same scope-inflation pattern I conceded in Round 1.

The corrective pressure was consistent and well-calibrated across both rounds. No correction was reversed. No concession was regretted.

### What the deliberation achieved

The deliberation transformed spec 005 from a loose implementation with implicit contracts into a foundation with explicit architectural decisions:

- **API design**: From bare function signatures to a `ValidationConfig` Pydantic model that absorbs future extensions without breaking changes.
- **Error typing**: From `list[str]` returns to structured `LintError` models with `str` error types validated against an extensible runtime registry.
- **Schema loading**: From `sys.exit()` side effects to `SchemaLoadError` exceptions, enabling library consumption.
- **Mode validation**: From hardcoded `Literal` sets to filesystem-derived dynamic registries.
- **Extension contract**: From implicit assumptions to explicit P2-6 documentation of what is extensible, what is frozen, and how composition works.

Each of these outcomes is stronger than any single agent's original proposal because the deliberation forced each proposal through adversarial pressure from agents with different priorities. functional-typing's type safety concerns caught my untyped escape hatches. My extensibility concerns caught functional-typing's overly rigid `Literal` types. integration-architect's practical implementation focus caught both of our tendencies toward speculative architecture.

### What I am carrying forward to spec 007

The deliberation's outcome is exactly the foundation spec 007 needs:

1. **`ValidationConfig` as the composition surface.** Spec 007 adds plugin-aware fields to this model. The model's Pydantic defaults ensure backward compatibility. No API signature changes required.

2. **`KNOWN_ERROR_TYPES` as the registration pattern.** Plugin `check_*` functions register their error types at initialization. The `@field_validator` rejects unregistered types. The pattern is identical to mode registration.

3. **`PHASE_CONTEXT_MODELS` as the extensible registry.** New phase context models for plugin phases are registered here. The explicit documentation in P2-6 prevents re-addition of `Final`.

4. **Composition, not inheritance, for plugin data.** A separate `PluginContext` alongside frozen `TemplateContext`, with typed plugin models. No `dict[str, Any]`, no `extra = "allow"`, no untyped escape hatches.

5. **Filename-phase constraint as a documented assumption.** Spec 007 knows that introducing multi-template phases requires linter changes, and can design accordingly.

### Non-negotiables that survived

My Round 1 non-negotiable -- "the programmatic validation API must include a typed mechanism for declaring additional known variables" -- is fully satisfied by `ValidationConfig`. The mechanism is more general than my original proposal (a model rather than a single `frozenset[str]` parameter), which means spec 007 can extend it in ways I did not anticipate. This is a better outcome than what I originally asked for.

My Round 1 non-negotiable on `dict[str, Any]` -- "no untyped escape hatches on core models" -- is fully satisfied. No agent proposed it in Round 2. The composition architecture is unanimous.

My Round 1 non-negotiable on `error_type` -- "`str` with runtime validation, not `Literal`" -- is fully satisfied. The enforcement behavior (reject, not warn) is now also converged across all three agents.

### Remaining items for synthesizer resolution

Two items require synthesizer action, neither of which involves inter-agent disagreement:

1. **Specify `error_type` validator enforcement behavior** (Dispute A). All three agents agree: reject unknown types at construction time. The Round 1 synthesis should be updated to state this explicitly.

2. **Scope the reverse template check relative to P2-1** (Dispute B). Substance is agreed. I recommend bundling with P2-1 for logical completeness. integration-architect defers to synthesizer discretion. functional-typing accepts at P3.

### Concessions summary

**Round 1 (7 concessions, all maintained):**
1. Plugin variable namespace -- deferred to spec 007
2. `extra = "allow"` on TemplateContext -- withdrawn entirely
3. Float/number variable type -- withdrawn
4. ModeSchema extensions section -- deferred to spec 007
5. Reserved `schema/objectives/` directory -- withdrawn
6. Template-scanning for MODE_PRESENCE -- withdrawn
7. `VALID_MODES` downgraded from P1 to P2

**Round 2 (3 additional concessions):**
8. R1 docstring field-name prescription -- narrowed to directional hint
9. R3 `extra = "ignore"` on ModeSchema -- withdrawn, revised to reinforce `extra = "forbid"`
10. Warning-only `@field_validator` -- never my position, but I endorsed the convergent rejection of functional-typing's proposal

### Assessment of the deliberation process

The cross-review mechanism was the most effective corrective instrument. In both rounds, the pattern was consistent: scope inflation identified independently by two agents is scope inflation. The two corrections I received in Round 2 (docstring specificity and `extra = "ignore"` hedging) were both instances of conceded Round 1 patterns reappearing in subtler forms. The fact that both cross-reviewers caught both instances, using the same reasoning I had already accepted in Round 1, demonstrates that the deliberation created genuine shared understanding rather than positional compromise.

The deliberation is converged. No architectural disputes remain. The synthesis can proceed.
