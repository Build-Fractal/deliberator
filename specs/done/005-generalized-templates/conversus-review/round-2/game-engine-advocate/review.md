# Game Engine Advocate -- Round 2 Review

**Reviewer role**: game-engine-advocate (spec 007)
**Target**: spec 005 -- Generalized Template Schema, Variables, and Linter
**Round**: 2 of 2
**Date**: 2026-03-21

---

## Executive Summary

Round 1 was a productive reckoning with scope discipline. I entered with 10 recommendations, conceded 7 as scope inflation, and exited with 4 active disputes. The synthesizer resolved all 4 in the Round 1 final synthesis. I engage with those resolutions here.

Of the 4 disputes, I accept the synthesizer's resolution on 3 and challenge the resolution on 1. My remaining position is narrow but substantive: the synthesizer's resolution of Dispute 1 (programmatic API parameter design) correctly chose the `ValidationConfig` Pydantic model pattern but drew the wrong conclusion about whether `known_plugin_variables` should appear in the initial model. The other 3 dispute resolutions are well-reasoned and I incorporate them without reservation.

The Round 1 deliberation produced a strong foundation. Spec 005's actionable spec changes (P1-1 through P3-5) are comprehensive and architecturally sound. My Round 2 role is to confirm the game engine's interests are protected by the chosen patterns, flag one residual concern, and identify opportunities the synthesis may have underweighted.

---

## Alignment

### A1: The synthesizer's "freeze first, compose later" principle is correct and well-articulated

The systemic contradiction analysis (Section 4, S1) identifies the deepest pattern in the deliberation: present correctness vs. future extensibility. The resolution -- "spec 005 optimizes for correctness of the current system; spec 007 designs extension mechanisms with full knowledge of the frozen foundation" -- is precisely right. This emerged from the cross-review process rather than being any agent's starting position, which validates the deliberation's value. I reaffirm this as the governing principle for my Round 2 positions.

### A2: Dispute 2 resolution (no `dict[str, Any]` on TemplateContext) is correct

The synthesizer's resolution of Dispute 2 affirms what all three agents converged on: no `dict[str, Any]` on any core TemplateContext model. integration-architect's concession in Phase 4 was the right call. The composition model (separate `PluginContext`) designed in spec 007 is architecturally superior to an untyped escape hatch on a frozen model. I have no residual concern here.

### A3: Dispute 3 resolution (`str` for `error_type` with registry validation) is the right pattern

The synthesizer resolved the `Literal` vs. `str` dispute for `error_type` by applying the same pattern that was unanimously adopted for modes: `str` with a `@field_validator` checking against a known registry (`KNOWN_ERROR_TYPES: frozenset[str]`). This is consistent and correct. integration-architect's distinction between schema-external types (modes) and code-internal types (error categories) was meaningful but ultimately insufficient to justify a different pattern. The synthesizer's reasoning -- that plugin-contributed validation rules need to return errors with plugin-defined types -- tracks the game engine's architecture precisely. Plugin validators producing `LintError(error_type="invalid_objective_schema")` need a runtime-open type, not a compile-time closed `Literal`.

I accept this resolution fully.

### A4: Dispute 4 resolution (bare import fix as part of P1 API work) is correct

The synthesizer resolved Dispute 4 by treating the import fix as part of the P1 programmatic API work item rather than a separate P2 deliverable. This is the correct sequencing: you cannot create a callable library function without fixing the imports. The synthesizer's distinction between "import fix as part of P1 API" and "pyproject.toml entry point as P2 packaging" is clean and implementable. I accept this without reservation.

### A5: The convergence scorecard accurately reflects the deliberation's intellectual movement

The synthesis tracked 29 original recommendations through 4 phases with transparent disposition tracking. The characterization of my own trajectory -- "made the largest positional shift, conceding 7 of 10 original recommendations as scope inflation" -- is factually accurate. The process worked: cross-review pressure forced genuine re-examination of positions rather than entrenchment.

### A6: P1-4 (`ConfigCondition` model) correctly serves the near-term need

The typed `ConfigCondition` model with `field: str` and `value: str` is the right abstraction for spec 006's conditional variables (e.g., `PRIOR_ARBITRATION_PATH` conditioned on `arbiter.timing: inter-round`). This was integration-architect's contribution, refined by functional-typing's insistence on typed Pydantic models over raw dicts. From the game engine perspective, this establishes a precedent: extension mechanisms use typed models, not untyped dicts. When spec 007 needs a `plugin_condition` or `objective_condition` axis, it composes with this pattern rather than replacing it.

### A7: P2-6 (extension contract documentation) protects downstream specs

The synthesizer correctly elevated extension contract documentation to P2 and specified what it should contain: extension points (new variables, new modes, config conditions, plugin composition) and non-extension points (`extra = "forbid"`, template syntax, structural markers). This is the single most valuable non-code deliverable in spec 005 for spec 007's benefit. It converts implicit assumptions into explicit contracts that spec 007 can cite and build on.

---

## Engagement with the 4 Remaining Disputes

### Dispute 1 (Programmatic API parameter design): Partially accept the synthesizer's resolution

The synthesizer resolved this by choosing `ValidationConfig` as a Pydantic model (integration-architect's approach) with `root: Path` and `mode: Optional[str] = None`, explicitly excluding `known_plugin_variables` from the initial model. The rationale: "adding a field with a default to a Pydantic model is non-breaking," so the `ValidationConfig` model itself is the extension surface.

I accept the `ValidationConfig` model pattern. This is superior to bare parameters (functional-typing's position) and provides a stable extension surface. The synthesizer is correct that this addresses my concern about future extensibility.

However, I maintain a residual concern about the synthesizer's reasoning, not its conclusion. The synthesizer states: "since the API has no external consumers until spec 008 ships, any parameter addition before that point is non-breaking." This is true today but establishes a dangerous principle: it implies that API design can defer forward-compatibility decisions until external consumers exist. The value of forward-compatible design is precisely that it avoids the need to coordinate with consumers later. The `ValidationConfig` model happens to solve this problem (because adding fields with defaults to Pydantic models is non-breaking), but the reasoning would have led to bare parameters if functional-typing's approach had been chosen -- and bare parameters ARE breaking to extend.

**My revised position**: I accept `ValidationConfig` without `known_plugin_variables` in the initial model. The Pydantic model pattern provides a non-breaking extension path. But the `ValidationConfig` docstring should document not just that "spec 007 may extend this model" (as the synthesis specifies) but specifically that the anticipated extension is plugin-variable awareness. This costs nothing and gives spec 007 implementers a concrete expectation rather than a vague "may extend."

**Concession from Round 1 maintained**: I do not reverse my acceptance of the `ValidationConfig` approach. I refine it.

**Status**: Dispute narrowed to docstring specificity. This is a minor concern, not a blocking dispute.

### Dispute 2 (no `dict[str, Any]` on TemplateContext): Fully resolved

See Alignment A2. No residual concern.

### Dispute 3 (`error_type` as `str` with registry): Fully resolved

See Alignment A3. No residual concern.

### Dispute 4 (bare import fix sequencing): Fully resolved

See Alignment A4. No residual concern.

---

## Missed Opportunities

### MO-1: The `PHASE_CONTEXT_MODELS` registry extension path is under-specified

The synthesis lists P3-4 ("Make `VALID_PHASES` extensible") but does not address the related question of `PHASE_CONTEXT_MODELS` extensibility. In Round 1, functional-typing proposed `Final` on `PHASE_CONTEXT_MODELS` (FT-8), which was withdrawn after I identified it as a registry spec 007 needs to extend. The synthesis records the withdrawal (Convergence item 6: "No `PHASE_CONTEXT_MODELS` as `Final`") but does not document what SHOULD happen to `PHASE_CONTEXT_MODELS`.

The current state is an implicit agreement that `PHASE_CONTEXT_MODELS` is extensible -- but without documentation, a future implementer might re-add `Final` without realizing the deliberation explicitly removed it. The extension contract documentation (P2-6) should include `PHASE_CONTEXT_MODELS` as an explicitly extensible registry, alongside the already-documented extension points.

**Recommendation**: Add `PHASE_CONTEXT_MODELS` to the P2-6 extension contract documentation as an extensible registry. One sentence: "The `PHASE_CONTEXT_MODELS` dict maps phase names to their context model classes and is designed to be extended by downstream specs adding new phases or phase variants."

**Priority**: P2 (part of existing P2-6 deliverable, no additional work).

### MO-2: The `ModeSchema` model should anticipate per-mode configuration beyond `mode_in_phases`

The Round 1 synthesis correctly adds `mode_in_phases` to mode schema YAML files (P2-1). This is the third field added to `ModeSchema` by the deliberation process (after `disputes`, `arbitration`, and `cross_round_synthesis`). The pattern is clear: mode schemas accumulate per-mode configuration that the linter and orchestrator consume.

Spec 007 will need to attach per-mode plugin configuration to mode schemas (e.g., objective function template references, feature extraction schemas, equilibrium scoring parameters). The current `ModeSchema` Pydantic model in `models.py` (L105-123) has explicit fields for each config section. When spec 007 adds its configuration, it will need to either (a) add fields to `ModeSchema` or (b) use a composition pattern.

The synthesis's extension contract documentation (P2-6) should acknowledge that mode schemas are an extension point not just for new mode YAML files but also for new fields within existing mode schemas. This is already implicit in the synthesis (it says "new modes via YAML file creation" is an extension point) but does not address field-level extension within a mode schema.

**Recommendation**: Extend P2-6 to note that `ModeSchema` fields may be added by downstream specs, with unknown fields handled gracefully (either via `extra = "ignore"` on `ModeSchema` or by loading mode schemas with a version-aware parser). This is documentation only -- no implementation change in spec 005.

**Priority**: P3 (documentation refinement, low urgency).

### MO-3: The synthesis does not address how `schema_version` interacts with the linter

P2-4 specifies adding `schema_version: "1.0.0"` to `variables.yml` and a corresponding field on `VariablesSchema`. The synthesis says "the linter reports the schema version in its output" but does not specify whether the linter should validate schema version compatibility. For spec 005, this is fine -- there is only one version. But as spec 006 and 007 evolve the schema, the linter will need to know whether it is compatible with the schema version it reads.

This is a P3 documentation item: note in the spec that schema version validation (e.g., linter version X supports schema versions 1.0-1.2) is a future concern to be addressed when the second schema version is introduced.

**Recommendation**: Add a note to P2-4 that schema version compatibility checking is deferred to the spec that introduces schema version 2.0.

**Priority**: P3.

---

## Off-Base Assumptions

### OB-1: None identified in the synthesis

The Round 1 synthesis is well-grounded. Every claim traces to specific deliberation artifacts. The systemic contradiction analysis (Section 4) correctly identifies the scope inflation pattern in my own recommendations without overstating it. The synthesizer did not introduce new ideas or mischaracterize any agent's position.

The one area where I initially considered raising an off-base concern -- the characterization of my Round 1 trajectory as "the largest positional shift" -- is factually accurate. I did concede 7 of 10 recommendations. The synthesis correctly attributes this to "scope inflation" rather than to intellectual weakness, which is the right framing: the recommendations were valid for spec 007 but out of scope for spec 005.

---

## Actionable Recommendations

### R1: Refine `ValidationConfig` docstring to specify anticipated plugin extension (Priority: P2)

**What**: The `ValidationConfig` docstring should state not just "spec 007 may extend this model" but specifically: "Anticipated extensions include `known_plugin_variables: frozenset[str]` for declaring plugin-contributed variables that should not be flagged as unknown by the linter."

**Why**: Converts a vague extensibility note into a concrete contract that spec 007 can implement against. Costs nothing. Reduces the risk that spec 007 implementers design a different (potentially incompatible) extension mechanism because the intent was not documented.

**Scope**: Documentation only. One sentence in a docstring.

**Relationship to Round 1 Dispute 1**: This narrows Dispute 1 from "must include the parameter" to "must document the intended parameter." I accept the synthesizer's decision to exclude the parameter; I ask only that the intent be recorded.

### R2: Include `PHASE_CONTEXT_MODELS` in P2-6 extension contract documentation (Priority: P2)

**What**: Add `PHASE_CONTEXT_MODELS` to the extension contract documentation as an explicitly extensible registry. Document that it is not `Final` by deliberation consensus and that downstream specs may register new phase-to-model mappings.

**Why**: Prevents future implementers from re-adding `Final` without knowledge of the deliberation's decision. The withdrawal of FT-8 was unanimous but is not captured in the P2-6 specification.

**Scope**: One sentence in an existing P2-6 deliverable.

### R3: Note `ModeSchema` field-level extensibility in P2-6 documentation (Priority: P3)

**What**: Extend the P2-6 extension contract to acknowledge that downstream specs may add fields to `ModeSchema`. Note that unknown fields in mode schema YAML files should be handled gracefully (e.g., `extra = "ignore"` on `ModeSchema` or version-aware loading).

**Why**: The current `ModeSchema` in `models.py` uses Pydantic's default behavior (which rejects unknown fields unless configured otherwise). Spec 007 will need to add objective function template references to mode schemas. If `ModeSchema` rejects unknown fields, spec 007 must coordinate its schema additions with a linter update. If `ModeSchema` ignores unknown fields, spec 007 can add schema fields independently.

**Scope**: Documentation in spec 005. Implementation decision (ignore vs. version-aware) is a spec 007 concern.

### R4: Add schema version compatibility note to P2-4 (Priority: P3)

**What**: Add a note to the schema versioning item (P2-4) stating that schema version compatibility validation (linter version X supports schema versions Y-Z) is deferred to the spec that introduces schema version 2.0.

**Why**: Prevents premature implementation of version-checking logic while acknowledging the future need. The current spec says "the linter reports the schema version in its output" -- this note clarifies that reporting is sufficient for v1.0; validation comes later.

**Scope**: One sentence in an existing spec change item.

---

## Referenced Documentation

- **Round 1 Synthesis**: `conversus-review/round-1/summary/final.md` -- Dispute 1 resolution (L199-211), Dispute 2 resolution (L125-130), Dispute 3 resolution (L214-227), Dispute 4 resolution (L243-257), P2-6 spec change (L346-351), Systemic Contradiction S1 (L146-148)
- **Round 1 game-engine-advocate disputes**: `round-1/game-engine-advocate/disputes.md` -- Dispute 1 original position (L12-24), Dispute 2 position (L28-40), Dispute 3 position (L44-57), Dispute 4 position (L60-68)
- **Round 1 game-engine-advocate revision**: `round-1/game-engine-advocate/revision.md` -- Position summary (L178-210), scope inflation acknowledgment (L182-184)
- **Spec 007**: `specs/007-game-engine/spec.md` -- Plugin API (L129-158), lifecycle hooks (L96-112), design principles (L65-70), Phase 1 scope (L216-221)
- **Implementation artifacts**: `linter/models.py` L105-123 (ModeSchema), L129-140 (TemplateContext config), L262-270 (PHASE_CONTEXT_MODELS); `linter/validate.py` L108-144 (MODE_PRESENCE), L281-305 (validate_template)
- **Schema**: `schema/variables.yml` -- full variable registry

---

## Summary of Positions

| Item | Round 1 Position | Round 2 Position | Status |
|------|-----------------|-----------------|--------|
| Dispute 1: API parameter design | `known_plugin_variables` parameter required | Accept `ValidationConfig` without parameter; request specific docstring | **Narrowed** |
| Dispute 2: No `dict[str, Any]` | Non-negotiable | Fully resolved | **Closed** |
| Dispute 3: `error_type` as `str` | Non-negotiable | Fully resolved | **Closed** |
| Dispute 4: Import fix sequencing | Must be P1 prerequisite | Fully resolved | **Closed** |
| `PHASE_CONTEXT_MODELS` extensibility | Not `Final` (FT-8 withdrawal) | Document in P2-6 | **New recommendation** |
| `ModeSchema` field extensibility | Deferred ModeSchema extensions (GE-7) | Document graceful handling in P2-6 | **New recommendation** |
| Schema version compatibility | Not addressed in Round 1 | Defer validation to v2.0 introduction | **New recommendation** |

### Concessions maintained from Round 1

All 7 concessions from Round 1 are maintained without reversal:
1. Plugin variable namespace -- deferred to spec 007
2. `extra = "allow"` on TemplateContext -- withdrawn entirely
3. Float/number variable type -- withdrawn
4. ModeSchema extensions section -- deferred to spec 007
5. Reserved `schema/objectives/` directory -- withdrawn
6. Template-scanning for MODE_PRESENCE -- withdrawn
7. `VALID_MODES` downgraded from P1 to P2

### New positions in Round 2

All new positions are documentation refinements to existing synthesis deliverables, not new implementation requirements. Total new implementation cost: zero lines of code in spec 005.
