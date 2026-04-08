# Game Engine Advocate -- Round 2 Revision

**Reviewer role**: game-engine-advocate (spec 007)
**Target**: spec 005 -- Generalized Template Schema, Variables, and Linter
**Round**: 2, Phase 3 (Revision after cross-reviews)
**Date**: 2026-03-21

---

## Recommendation Dispositions

### R1: Refine `ValidationConfig` docstring to specify anticipated plugin extension -- REVISED

**Original position**: The `ValidationConfig` docstring should specify `known_plugin_variables: frozenset[str]` as the anticipated extension, with concrete field name, type, and semantic description.

**Cross-review feedback**: Both functional-typing (DC-2) and integration-architect (DC-1) independently identified this as scope inflation dressed as documentation. functional-typing called it "a form of composing before freezing" that contradicts my own governing principle (A1). integration-architect called it "spec 005 reaching into spec 007's design space" and noted that if spec 007 discovers it needs a `PluginVariableRegistry` carrying metadata rather than a flat `frozenset[str]`, the docstring becomes misleading. Both reviewers noted that my "zero cost" framing understates the normative weight of spec text.

**Assessment**: The cross-reviews are correct. I concede this recommendation in its original form. Naming a specific field, type, and semantic description in spec 005's docstring is the same scope-inflation pattern I conceded 7 times in Round 1, applied to prose rather than code. The fact that two independent reviewers identified the same contradiction -- and that it mirrors my own Round 1 trajectory -- is dispositive. The synthesizer's formulation ("spec 007 may extend this model") is intentionally vague because the extension shape is spec 007's decision.

**Revised position**: The `ValidationConfig` docstring should say "downstream specs (particularly spec 007) may extend this model with plugin-aware configuration fields." This is the synthesizer's original intent, perhaps with one additional word ("plugin-aware") to orient future readers without prescribing a specific design. No field name, no type signature, no semantic description from spec 005.

**Status**: Conceded. Narrowed from specific field prescription to directional hint.

### R2: Include `PHASE_CONTEXT_MODELS` in P2-6 extension contract documentation -- MAINTAINED

**Original position**: Add `PHASE_CONTEXT_MODELS` to P2-6 as an explicitly extensible registry with one sentence of documentation.

**Cross-review feedback**: functional-typing (SA-4) explicitly agrees: "Including `PHASE_CONTEXT_MODELS` in P2-6's extension points list costs one sentence and prevents a future implementer from re-adding `Final`." integration-architect (T-2) agrees on substance ("I agree this is a gap in P2-6") but questions urgency, noting no one will re-add `Final` without checking the deliberation record.

**Assessment**: Both reviewers agree on substance. integration-architect's urgency concern is fair -- the risk is low. But the cost of including one sentence in an already-planned deliverable is also near zero, and the deliberation record (conversus review artifacts) is not a standard reference for implementers the way spec text is. A future contributor reading P2-6 for extension guidance will find it; a future contributor will not read Round 1 cross-review transcripts. The asymmetry between documentation cost and documentation value favors inclusion.

**Status**: Maintained at P2, as part of existing P2-6 deliverable.

### R3: Note `ModeSchema` field-level extensibility in P2-6 documentation -- REVISED

**Original position**: Document in P2-6 that downstream specs may add fields to `ModeSchema`, with unknown fields handled gracefully via `extra = "ignore"` or version-aware loading.

**Cross-review feedback**: integration-architect (DC-2) identified the `extra = "ignore"` suggestion as contradicting the unanimous `extra = "forbid"` consensus, calling it "the `extra = "allow"` argument (GE-2, withdrawn in Round 1) reappearing through a side door." functional-typing (T-2) raised the same concern: `extra = "ignore"` silently swallows typos and is the exact failure mode `extra = "forbid"` prevents. Both reviewers proposed the correct alternative: downstream specs add typed fields to `ModeSchema` explicitly, consistent with the pattern used for every other model.

**Assessment**: The cross-reviews are correct, and I should have caught this myself. Suggesting `extra = "ignore"` -- even as one of two documented options -- undermines the consensus I explicitly endorsed. The right extension pattern for `ModeSchema` is the same as for everything else: add typed fields to the model definition. This is what composition means in the Pydantic context.

**Revised position**: If P2-6 documents `ModeSchema` extensibility, it should state: "Downstream specs may add typed fields to `ModeSchema` by modifying the Pydantic model definition. The `extra = 'forbid'` constraint remains in effect; unknown fields in mode schema YAML files are validation errors, not silent extensions." This explicitly closes the `extra = "ignore"` path rather than leaving it open.

**Status**: Revised. The `extra = "ignore"` option is withdrawn. The documentation recommendation is maintained but now reinforces the `extra = "forbid"` consensus rather than hedging against it. Downgraded from P3 to P3 (unchanged priority, corrected content).

### R4: Add schema version compatibility note to P2-4 -- MAINTAINED

**Original position**: Note in P2-4 that schema version compatibility validation is deferred to the spec that introduces version 2.0.

**Cross-review feedback**: integration-architect (T-3) agrees this is "consistent" with the approach of establishing the version field now and deferring compatibility logic. No objections from either cross-reviewer.

**Status**: Maintained at P3. No revision needed.

---

## New Recommendations

### NR-1: Specify `@field_validator` enforcement behavior for `KNOWN_ERROR_TYPES` (Priority: P2)

**Source**: functional-typing's DC-1 cross-review of my Round 2 review, and my own DC-1 cross-review of functional-typing's Round 2 review.

**The gap**: My Round 2 review accepted the synthesizer's Dispute 3 resolution (`str` with `@field_validator` checking against `KNOWN_ERROR_TYPES`) without specifying enforcement behavior. functional-typing correctly identified this as ambiguous: does the validator reject unknown types (raising `ValueError`) or warn about them? functional-typing proposed warning-only validation. In my cross-review of functional-typing, I argued that warning-only validation provides no typo protection and creates inconsistency with mode validation (which rejects unknown modes).

**My position after reading cross-reviews**: The validator should **reject** unknown error types at construction time, consistent with mode validation behavior. The extension path for plugins is registration, not bypassing: spec 007 plugins register their error types into `KNOWN_ERROR_TYPES` at initialization time, just as they register mode YAML files. The synthesizer's resolution already states the registry "can be extended at load time." A `frozenset` that is constructed from a base set plus plugin-contributed types at module load time provides both typo protection and plugin extensibility without a warning-only compromise.

Concretely, the pattern is:

1. `KNOWN_ERROR_TYPES` is constructed at module load time from a base set plus any registered plugin error types.
2. The `@field_validator` raises `ValueError` for types not in the constructed set.
3. Spec 007's plugin initialization protocol includes error type registration before any validation calls.

This is consistent with the mode validation pattern (register YAML, then validate) and preserves typo catching. functional-typing's concern about "recreating the Literal problem" is addressed because the `frozenset` is constructed at runtime from dynamic inputs, not hardcoded in source.

**Recommendation**: P2-6 extension contract documentation should specify that `KNOWN_ERROR_TYPES` is an extensible registry with strict validation. Plugins register their error types at initialization; the validator rejects unregistered types. This makes the enforcement behavior explicit and consistent with mode validation.

### NR-2: Acknowledge integration-architect's reverse template check as a P2-1 companion (Priority: P2)

**Source**: integration-architect's MO-2 (reverse template existence check) and T-4 (my silence on it).

**The gap**: integration-architect noted that my review does not address the reverse template check, "despite the game engine being the most likely source of new template files." This is a fair observation. In my cross-review of integration-architect, I noted (T-1) that the reverse check is the natural companion to P2-1 (MODE_PRESENCE as YAML): when the `templates` list in mode schema YAML becomes authoritative, bidirectional validation is a single concept. Templates listed but not on disk, and templates on disk but not listed, are symmetric failure modes.

**My position**: The reverse template existence check should be scoped as part of P2-1 implementation rather than a separate P3 item. When P2-1 makes the mode schema `templates` list authoritative, the linter should validate in both directions: (1) every listed template exists on disk, and (2) every template on disk is listed in at least one mode schema. This is bidirectional validation as a single deliverable, not two separate work items.

**Recommendation**: Include the reverse template existence check in P2-1's scope. The P2-1 deliverable becomes: "Migrate MODE_PRESENCE to mode schema YAML declarations with bidirectional template validation (listed-but-missing and present-but-unlisted)."

### NR-3: Flag the P3-5 / P1-4 scope overlap for synthesizer resolution (Priority: documentation)

**Source**: My cross-review of functional-typing (T-1), where I engaged with functional-typing's OBA-2 analysis of the `condition` field.

**The gap**: functional-typing identified that the `condition` field in `variables.yml` contains prose documentation strings, not parseable expressions, and that `validate.py` never reads it. Meanwhile, P1-4 introduces `config_conditions` as the typed, machine-readable mechanism for conditional variable requirements. P3-5 specifies "formalize condition syntax" -- but if P1-4 already provides machine-readable conditions through `ConfigCondition`, P3-5's scope is unclear: does it extend `ConfigCondition` with more condition types, or does it formalize the prose `condition` field into a separate grammar?

**My position**: The synthesizer should clarify P3-5's relationship to P1-4 in the final synthesis. If P3-5 extends `ConfigCondition` (adding condition types beyond `field`/`value` matching), it is useful and should say so. If P3-5 formalizes the prose `condition` field into a parseable grammar independent of `ConfigCondition`, the value proposition is unclear and the work may be redundant. This is a scoping question, not a design recommendation -- I am not proposing an answer, but flagging that the two items interact in a way the Round 1 synthesis does not address.

---

## Position Summary

### Governing principle

"Freeze first, compose later" remains the governing principle. Spec 005 defines the frozen foundation; spec 007 designs extension mechanisms with full knowledge of that foundation. All of my revised positions in this document are tested against this principle. Where cross-reviewers identified violations (R1 docstring specificity, R3 `extra = "ignore"` suggestion), I have conceded.

### Trajectory

Round 1 began with 10 recommendations. I conceded 7 as scope inflation and exited with 4 active disputes. The synthesizer resolved all 4 disputes. Round 2 began with acceptance of 3 dispute resolutions, a narrowed position on Dispute 1, and 3 new documentation recommendations (MO-1 through MO-3). After cross-review feedback, I have:

- **Conceded R1** (docstring specificity) -- both cross-reviewers correctly identified this as scope inflation in prose form. Revised to directional hint without field-name prescription.
- **Maintained R2** (PHASE_CONTEXT_MODELS in P2-6) -- both cross-reviewers agree on substance.
- **Revised R3** (ModeSchema extensibility) -- withdrew the `extra = "ignore"` suggestion after both cross-reviewers identified it as contradicting the `extra = "forbid"` consensus. Revised to reinforce the consensus rather than hedge against it.
- **Maintained R4** (schema version compatibility note) -- no objections.
- **Added NR-1** (error_type validator enforcement behavior) -- responding to functional-typing's DC-1, which identified a genuine ambiguity in my acceptance of Dispute 3.
- **Added NR-2** (reverse template check as P2-1 companion) -- responding to integration-architect's observation that this is on the game engine's radar.
- **Added NR-3** (P3-5 / P1-4 scope overlap) -- surfacing a cross-review finding for synthesizer resolution.

### Final disposition table

| Item | Round 1 | Round 2 Review | Round 2 Revision | Status |
|------|---------|---------------|-----------------|--------|
| Dispute 1: API parameter design | `known_plugin_variables` required | Accept `ValidationConfig`; request specific docstring | Accept `ValidationConfig`; directional hint only | **Conceded further** |
| Dispute 2: No `dict[str, Any]` | Non-negotiable | Fully resolved | Fully resolved | **Closed** |
| Dispute 3: `error_type` as `str` | Non-negotiable | Fully resolved | Resolved; add enforcement behavior spec | **Closed + addendum** |
| Dispute 4: Import fix sequencing | Must be P1 prerequisite | Fully resolved | Fully resolved | **Closed** |
| R2: `PHASE_CONTEXT_MODELS` in P2-6 | N/A | Document as extensible registry | Maintained | **Active (P2)** |
| R3: `ModeSchema` extensibility | N/A | Document with `extra = "ignore"` option | Revised: reinforce `extra = "forbid"` | **Revised** |
| R4: Schema version deferral note | N/A | Defer validation to v2.0 | Maintained | **Active (P3)** |
| NR-1: Error type validator behavior | N/A | N/A | Strict rejection + plugin registration | **New (P2)** |
| NR-2: Reverse template check scope | N/A | N/A | Include in P2-1 as bidirectional validation | **New (P2)** |
| NR-3: P3-5 / P1-4 overlap | N/A | N/A | Flag for synthesizer clarification | **New (documentation)** |

### Concessions maintained from Round 1 (all 7, no reversals)

1. Plugin variable namespace -- deferred to spec 007
2. `extra = "allow"` on TemplateContext -- withdrawn entirely
3. Float/number variable type -- withdrawn
4. ModeSchema extensions section -- deferred to spec 007
5. Reserved `schema/objectives/` directory -- withdrawn
6. Template-scanning for MODE_PRESENCE -- withdrawn
7. `VALID_MODES` downgraded from P1 to P2

### Cross-review learnings

The cross-reviews applied the same corrective pressure in Round 2 that the deliberation applied in Round 1. Two patterns were flagged:

1. **Scope inflation via documentation**: Both cross-reviewers identified R1 (docstring field-name prescription) as encoding spec 007 assumptions into spec 005 through prose rather than code. This is the same impulse that drove my 7 Round 1 concessions, expressed in a subtler form. The lesson: scope discipline applies to documentation as much as to implementation. A specific field name in a docstring carries normative weight.

2. **Consensus erosion via hedging**: integration-architect identified R3 (`extra = "ignore"` as an option) as the withdrawn GE-2 argument "reappearing through a side door." functional-typing concurred. The lesson: presenting a rejected approach as "one option among several" in documentation undermines the deliberation's resolution. If the deliberation rejected `extra = "allow/ignore"`, the documentation should close the door, not leave it ajar.

These are genuine corrections. The cross-review process surfaced blind spots that self-review did not catch. The revised positions are stronger for it.
