# Integration Architect -- Round 2 Final Disputes

**Reviewer**: integration-architect
**Spec**: `005-generalized-templates`
**Round**: 2 of 2 (Phase 4 -- Final Statement before Synthesis)
**Date**: 2026-03-21

---

## Remaining Disputes

### None.

There are no remaining architectural disputes. Every substantive disagreement from this deliberation has been resolved through convergence, concession, or narrowing to documentation phrasing. The items below in Convergence represent the full set of agreements, including areas where minor phrasing differences exist but no agent contests the substance.

The closest candidates for "remaining dispute" are two items where agents agree on substance but differ on venue or phrasing. I address both here to confirm they are not disputes:

**1. Reverse template check priority: P3 standalone vs. P2-1 companion.**
game-engine-advocate (NR-2) argues the reverse template existence check should be bundled with P2-1 (MODE_PRESENCE as YAML), making bidirectional template validation a single deliverable. functional-typing accepts it at P3. My revision says I support bundling with P2-1 if the synthesizer agrees, but P3 standalone is defensible if P2-1's scope is already large. This is a priority/scoping question for the synthesizer, not a disagreement on whether the check should exist. All three agents endorse the check itself.

**2. `ValidationConfig` docstring phrasing.**
game-engine-advocate revised from prescribing `known_plugin_variables: frozenset[str]` to a directional hint: "downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields." functional-typing accepts with the qualification that no specific parameter name or type should appear. I agree with the revised formulation. The difference between "plugin-aware configuration fields" (game-engine-advocate) and "plugin-variable awareness" (functional-typing) is editorial, not architectural. The synthesizer can pick either phrasing.

---

## Convergence

The deliberation has produced consensus on every actionable item. Below is the complete convergence map, organized by the strength of agreement.

### Unanimous -- All Three Agents, Both Rounds

1. **P1-1: Purify schema-loading functions.** `load_variables_schema`, `load_mode_schema`, and `find_project_root` must raise exceptions instead of calling `sys.exit(2)`. The CLI `main()` catches and exits. This is the single highest-leverage change and the prerequisite for everything downstream. Unanimous in Round 1, reaffirmed by all three agents in Round 2.

2. **P1-2: Programmatic `validate_all(config: ValidationConfig) -> ValidationResult` API.** `ValidationConfig` is a Pydantic model with `root: Path` and `mode: Optional[str] = None`. No plugin-specific fields until a caller exists. The bare import fix (`from models` to `from .models`) is part of this deliverable, not a separate item. Unanimous.

3. **P1-4: `ConfigCondition` typed model for `config_conditions`.** `ConfigCondition(BaseModel)` with `field: str` and `value: str`. Enables spec 006's conditional variable requirements (e.g., `PRIOR_ARBITRATION_PATH` required only when `arbiter.timing: inter-round`). Unanimous.

4. **P2-1: MODE_PRESENCE migrated to mode schema YAML declarations.** The 28-entry hardcoded dict is replaced by `mode_in_phases` (or equivalent) declared in each mode schema YAML. Three agents arrived at the same solution from different analytical angles in Round 1; no challenge in Round 2.

5. **P2-4: Schema version field (`schema_version: "1.0.0"`) before spec 006 schema evolution.** Versioning precedes the first schema change. Compatibility validation deferred to the spec introducing version 2.0 (game-engine-advocate R4, accepted by all).

6. **P2-5: `frozen=True` on TemplateContext hierarchy.** Immutability on core models. Plugin extensibility via composition (separate `PluginContext`), not by relaxing immutability. "Freeze first, compose later" is the governing principle.

7. **P2-6: Extension contract documentation.** Spec 005 documents which surfaces are extension points and which are closed. This is the venue for several sub-items that reached consensus in Round 2 (see below).

8. **All Round 1 concessions maintained.** No agent reversed any Round 1 concession in Round 2. integration-architect: 5 concessions. game-engine-advocate: 7 concessions. functional-typing: 5 concessions. The deliberation's convergence trajectory is monotonically increasing.

### Converged in Round 2 -- After Cross-Review Corrections

9. **`error_type` validator rejects unknown types at construction time.** functional-typing withdrew the warning-only proposal after both cross-reviewers identified it as breaking pattern consistency with mode validation. All three agents now agree: the `@field_validator` raises `ValueError` for unregistered types. Plugins register their error types into `KNOWN_ERROR_TYPES` at initialization, before producing errors. One validation pattern for all extensible sets. game-engine-advocate's NR-1 and my New Rec B converge on this, and functional-typing explicitly concedes.

10. **No separate `ValidationContext` dataclass.** functional-typing withdrew this after both cross-reviewers identified the dual-abstraction hazard. Parameter-count concerns are addressed by deriving internal state from `ValidationConfig`, not by introducing a parallel configuration object. If parameter proliferation becomes unmanageable after P1-2 and P1-4 land, a derived internal view can be introduced in coordination with `ValidationConfig`.

11. **`PHASE_CONTEXT_MODELS` documented as extensible registry in P2-6.** game-engine-advocate proposed (R2), functional-typing agreed (SA-4), I agreed on substance while noting low urgency (T-2). One sentence in P2-6 prevents a future implementer from re-adding `Final` without checking the deliberation record. Cost: trivial. The FT-8 withdrawal decision should be captured in spec text, not only in deliberation artifacts.

12. **`ModeSchema` extensibility documented in P2-6 with `extra = "forbid"` reinforced.** game-engine-advocate revised R3 to remove the `extra = "ignore"` suggestion after both cross-reviewers identified it as the withdrawn GE-2 argument reappearing. The agreed formulation: "Downstream specs may add typed fields to `ModeSchema` by modifying the Pydantic model definition. The `extra = 'forbid'` constraint remains in effect; unknown fields in mode schema YAML files are validation errors, not silent extensions."

13. **Filename-phase constraint documented in P2-6 as a constraint, not a prescription.** My Rec 4 was modified after game-engine-advocate (DC-2) correctly identified that prescribing conditional blocks as the workaround oversteps spec 005's authority. Agreed formulation: "Template filenames map 1:1 to phase names (`phase = tmpl_path.stem`). This is a load-bearing assumption in the linter. Downstream specs that need per-phase variants should be aware that introducing multiple template files for a single phase would require linter changes."

14. **`validate_templates` evolution noted in P2-6 without backward-compatibility commitment.** functional-typing (T-3) correctly identified that committing to backward compatibility of the boolean form constrains spec 007's design space. Agreed formulation: "The `validate_templates` field is boolean in v1. Granular validation control (per-mode, per-check-type) is a potential future concern but is not designed here." No shape suggestion. No backward-compatibility promise.

15. **`ROUND_SYNTHESES` comment fix and exclusion from P1-3 PathList conversion.** My Rec 3, accepted by both cross-reviewers. The comment changes from "newline-separated paths" to "pre-formatted synthesis content per round." The explicit exclusion prevents mechanical over-application of PathList during P1-3 implementation. Priority: P3.

16. **Reverse template existence check endorsed by all agents.** My Rec 2. functional-typing accepts at P3. game-engine-advocate accepts and proposes bundling with P2-1 as bidirectional validation. I support either scoping. The check itself is not disputed. New Rec A (validate mode schema `templates` entries against known phase names) bridges this check with the filename-phase constraint into a coherent three-part validation chain.

17. **P3-5 scope must be resolved relative to P1-4.** functional-typing (NEW-2) and game-engine-advocate (NR-3) independently surface the same question: if P1-4's `ConfigCondition` is the machine-readable mechanism for conditional variable requirements, what does P3-5 ("formalize condition syntax") add? Either P3-5 extends `ConfigCondition` with new condition types (useful, fold into P1-4 extensions) or P3-5 formalizes the prose `condition` field in `variables.yml` into a separate grammar (unclear value, no identified consumer). The synthesizer should resolve this scoping question.

18. **Rec 1 (SKILL.md `allowed-tools`) withdrawn.** Both cross-reviewers correctly identified this as scope inflation into spec 008's domain. functional-typing's critique is dispositive: I simultaneously endorsed the programmatic API as the canonical interface and then recommended solving the invocation problem by shelling out to the CLI, meaning the primary consumer never exercises the decoupled property P1-2 was designed to achieve. The SKILL.md invocation pathway is a spec 008 concern. Withdrawn without replacement.

19. **Systematic schema-type-to-implementation audit alongside P1-3.** functional-typing's NEW-1 generalizes the pattern identified by my MO-3 (ROUND_SYNTHESES) and functional-typing's OBA-2 (condition field): drift between schema declarations and model implementations is not isolated. When P1-3 examines every path-like field, extending the pass to a full correspondence check adds minimal marginal effort. I agree this is implementation hygiene during P1-3 execution rather than a separate spec deliverable, but it should be noted as an implementation instruction.

20. **`ValidationConfig` docstring references plugin extensibility directionally, without prescribing field names or types.** game-engine-advocate revised from specific field prescription to directional hint. functional-typing accepted with minor phrasing qualification. I accept. The docstring should orient future readers toward plugin-aware extensions without committing spec 005 to a specific design that is spec 007's decision.

---

## Final Position Statement

### Deliberation Trajectory

This deliberation began with 10 recommendations from game-engine-advocate (7 withdrawn as scope inflation), multiple architectural disagreements on `extra = "forbid"` vs. `extra = "allow"`, `Literal` vs. `str`, `dict[str, Any]` vs. typed models, and competing visions for plugin extensibility. After two rounds of review, cross-review, revision, and disputes, the deliberation has reached full convergence. No architectural disputes remain. All positions are either unanimous or narrowed to documentation phrasing choices that the synthesizer can resolve editorially.

The trajectory is instructive:

- **Round 1** resolved the structural disputes: `extra = "forbid"` is unanimous, `ValidationConfig` replaces the parameter-design dispute, `str` with validated registry replaces the `Literal` vs. `str` dispute, composition replaces `plugin_data`, and MODE_PRESENCE moves to YAML declarations.
- **Round 2** resolved the refinement disputes: warning-only validation was correctly identified as pattern-inconsistent, the `ValidationContext` dual-abstraction was correctly identified as a coordination hazard, `extra = "ignore"` on `ModeSchema` was correctly identified as a consensus regression, and prescriptive documentation was correctly narrowed to descriptive documentation.

The cross-review mechanism was the primary corrective force in both rounds. Every withdrawal in Round 2 was prompted by convergent criticism from both cross-reviewers identifying the same flaw independently. This convergent, independent identification is the strongest signal that corrections are substantive rather than positional.

### My Concessions (Complete Record)

**Round 1 (5 concessions, all maintained):**
1. MODE_PRESENCE endorsement retraction -- the hardcoded table is not the right approach
2. Loader purity retraction -- I failed to identify that `sys.exit()` contradicts my own programmatic API recommendation
3. ConfigCondition typing upgrade -- `dict[str, str]` replaced by `ConfigCondition(BaseModel)`
4. `plugin_data: dict[str, Any]` withdrawal -- composition model is architecturally superior
5. Schema version priority upgrade -- P3 to P2, versioning should precede first schema evolution

**Round 2 (1 concession):**
6. Rec 1 (SKILL.md `allowed-tools`) withdrawal -- scope belongs to spec 008, not spec 005

**Round 2 modifications (not concessions, but disciplined narrowing):**
- Rec 4: Document the filename-phase constraint, but do not prescribe how future specs must work around it
- Rec 5: Note `validate_templates` may evolve, but do not commit to backward compatibility of the boolean form

### Items I Accept from Other Agents

From **functional-typing**:
- `ValidationConfig` Pydantic model as the API boundary (Dispute 1 resolution)
- Rejection of warning-only validator (Dispute 2 correction -- functional-typing proposed it, then correctly withdrew it)
- Systematic audit alongside P1-3 (NEW-1, as implementation instruction)
- P3-5 scope resolution relative to P1-4 (NEW-2, for synthesizer)

From **game-engine-advocate**:
- `PHASE_CONTEXT_MODELS` in P2-6 extension contract (R2)
- `ModeSchema` extensibility documentation reinforcing `extra = "forbid"` (R3, revised)
- Schema version compatibility deferral note (R4)
- Reverse template check as potential P2-1 companion (NR-2)
- P3-5 / P1-4 scope overlap flag (NR-3)

### Non-Negotiables (Unchanged from Round 1)

These remain the positions I hold without compromise. None were challenged in Round 2:

1. **`extra = "forbid"` on all core TemplateContext models.** Unanimous across all agents, both rounds.
2. **Spec 006 variables as explicit typed fields, not deferred to plugin mechanisms.** No challenge in Round 2.
3. **Schema-loading functions purified before any downstream spec ships.** Unanimous as the highest-leverage change.
4. **Structured validation errors with strict `error_type` validation.** The `Literal` vs. `str` dispute is resolved (I accepted `str` with validated registry in Round 1), and the enforcement behavior (reject, not warn) is now unanimous in Round 2.
5. **Sequencing discipline: concrete needs first, speculative extensibility second.** Reinforced by both rounds. Rec 1 withdrawal in Round 2 applies this principle to my own recommendation.

### Assessment of the Deliberation

The spec 005 foundation is ready for synthesis. The deliberation produced 20 convergence items with no remaining disputes. The most significant outcomes:

- **P1-1 (purify loaders)** is the highest-leverage change, enabling every downstream integration. Unanimous across all agents, both rounds.
- **The "freeze first, compose later" principle** governed the entire deliberation and resolved every scope-inflation question. It was applied equally to all three agents -- game-engine-advocate's 7 Round 1 concessions, functional-typing's 2 Round 2 withdrawals, and my own Rec 1 withdrawal all follow the same principle.
- **The cross-review mechanism worked.** Every Round 2 correction was independently identified by both cross-reviewers. This convergent criticism is the strongest quality signal in the deliberation. Single-reviewer objections might be positional; dual-reviewer convergent objections are almost certainly substantive.

The synthesizer has a clean field. No disputes to arbitrate. The synthesis task is consolidation, not resolution.
