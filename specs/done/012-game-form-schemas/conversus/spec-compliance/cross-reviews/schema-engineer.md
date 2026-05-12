# Cross-Review: schema-engineer (from spec-compliance)

**Cross-reviewer**: spec-compliance
**Reviewing**: schema-engineer's Phase 1 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: Discriminated union urgency vs. spec scope

**schema-engineer** elevates the discriminated union (`GameForm = Annotated[Union[...], Discriminator("form")]`) to P1, arguing it is "the single highest-impact change for downstream ergonomics" (Recommendation 2). **spec-compliance** did not flag this at P1 because the spec makes no requirement for a polymorphic union type -- FR-009 specifies four named exports, not a union, and no success criterion tests polymorphic deserialization.

The contradiction matters because treating a missing union as P1 conflates downstream spec needs (013, 016) with 012's actual contract. Adding a union type is a design enhancement for future consumers, not a compliance gap in the current spec. If the union is truly needed, the correct fix is to amend the spec (add an FR-012) rather than retroactively claim the implementation violates requirements it was never given. Promoting it to P1 risks scope creep in a schema-only spec that explicitly says "No solver, no optimizer, no plugin code."

Both reviews agree that `Literal` types on the `form` field are warranted (schema-engineer Rec 1, spec-compliance Rec 4). The `Literal` fix is prerequisite infrastructure for a discriminated union but is independently justified by FR-007's requirement to enforce type constraints. The union itself should be sequenced as a P2 enhancement or deferred to the spec that first needs it (013 or 016).

### DC-2: `ParametricGame` inheritance -- structural correctness vs. Pydantic pragmatism

Both reviews agree that `ParametricGame` duplicates GNEP validation verbatim and that the spec says "inherits all GNEP fields." schema-engineer goes further (Recommendation 4, Off-Base Assumptions) to argue that `isinstance(parametric_game, GNEPGame)` returning `False` will "surprise downstream code" and that Pydantic inheritance should be used.

spec-compliance flagged the same duplication (Rec 5) but at P2, focused on the maintenance/correctness risk of duplicated validators rather than on the `isinstance` contract. The dangerous contradiction is in the downstream promise: schema-engineer assumes specs 016-019 will use `isinstance` checks for polymorphic dispatch, but no downstream spec yet specifies this. If `ParametricGame` inherits from `GNEPGame`, Pydantic's model resolution, JSON schema generation, and field ordering all change in subtle ways (e.g., `model_fields` merging, validator execution order). This is not a trivial refactor.

The safe path is to address the duplication by extracting shared validators into a mixin or private base class that is not `GNEPGame` itself, preserving the flat model structure while eliminating the copy-paste. This avoids locking in an `isinstance` contract before downstream specs define whether they need it.

### DC-3: `VALID_FIELD_TYPES` -- dead code vs. documentation artifact

schema-engineer's review does not flag `VALID_FIELD_TYPES` as dead code. It notes the frozenset is "the right choice" (Alignment section) and recommends aligning YAML types with Pydantic types (Rec 8), but does not observe that `VALID_FIELD_TYPES` is never referenced by any validator or test.

spec-compliance identified this gap explicitly (Rec 9): FR-003 mandates a closed type set, the constant exists to represent it, but no code enforces membership. schema-engineer's Rec 8 (align YAML types with Pydantic types) actually makes this worse -- if the YAML types are updated to include `map[string, list[string]]` per schema-engineer's suggestion, but `VALID_FIELD_TYPES` is not updated to match and still is not enforced, the drift between the three layers (spec FR-003, `VALID_FIELD_TYPES` constant, YAML `type` declarations) becomes a three-way inconsistency rather than a two-way one.

The contradiction: schema-engineer treats type alignment as a YAML-only problem (fix the declared types), while spec-compliance treats it as a validation-layer problem (wire `VALID_FIELD_TYPES` into enforcement). Both fixes are needed simultaneously. Doing one without the other creates a false sense of correctness.

---

## Tensions

### T-1: Package data resolution -- `importlib.resources` vs. moving YAML files

Both reviews agree that `_schema_dir()` using `Path(__file__).parent.parent.parent` will break in installed packages (schema-engineer Rec 3, spec-compliance Rec 3). Both cite FR-011. The tension is in the proposed fix: schema-engineer offers three alternatives (importlib.resources, `[tool.setuptools.package-data]`, or embedding as Python constants), while spec-compliance is more prescriptive (move YAML into the package directory or use importlib.resources).

Embedding as Python constants would defeat the purpose of having human-readable YAML schema files that serve as documentation (FR-002). The `importlib.resources` approach is the cleanest, but it requires the YAML files to be inside the Python package directory structure, which means moving them from `schema/game-forms/` to `src/conversus_schemas/schema/game-forms/`. This changes the paths specified in FR-001. The tension is that fixing FR-011 may require amending FR-001, and neither review explicitly acknowledges this trade-off.

### T-2: Severity of the package name mismatch (FR-010)

Both reviews flag the `pyproject.toml` naming `conversus` instead of `conversus-schemas` (schema-engineer Off-Base Assumptions, spec-compliance Rec 2). spec-compliance rates it P1; schema-engineer mentions it in the Off-Base section and in Rec 3 but does not give it a separate numbered recommendation.

The tension is whether this is a spec bug or an implementation bug. If the project intends `conversus` to be the installable package with `conversus_schemas` as a sub-package (which is how the code is currently structured), then FR-010's text is the error, not the implementation. If the project intends a standalone `conversus-schemas` package, then the entire `pyproject.toml` and directory structure need restructuring. Neither review investigates the project's intent by examining adjacent specs or the broader monorepo structure. The resolution requires a design decision, not just a code fix.

### T-3: Stackelberg structural invariants -- how far to go

schema-engineer proposes two additional Stackelberg validators: leader-not-in-followers (Rec 6) and non-empty leader_variables (Rec 7). spec-compliance did not flag either. The tension: FR-007 says models must enforce "structural invariants" but does not enumerate which invariants. schema-engineer infers two from game theory semantics; spec-compliance sticks to what the spec explicitly mentions.

Both positions are defensible. The leader-not-in-followers check is mathematically necessary (a player cannot commit first and also respond to their own commitment). The non-empty leader_variables check is debatable -- a degenerate Stackelberg game with no leader variables reduces to a standard game, which might be intentionally representable. Adding validators that the spec does not mention is prudent engineering but is not a compliance gap. The right framing is "hardening recommendation" rather than "compliance finding."

### T-4: SC-001 literal interpretation

spec-compliance flagged (Rec 7) that SC-001's literal code `NormalFormGame.model_validate(yaml.safe_load(open("schema/game-forms/normal-form.yml")))` would validate the entire file (including `fields`, `description`), which would fail, while the test correctly validates only `data["example"]`. schema-engineer's review does not mention this discrepancy.

This is a minor tension but illustrative: spec-compliance reads success criteria as literal contracts, while schema-engineer evaluates implementation quality. Both approaches are valid but yield different findings. The test is correct; SC-001's wording is imprecise. A comment in the test documenting the intentional deviation would resolve this.

### T-5: `ModeMapping.lookup()` error type

schema-engineer recommends a custom `ModeNotFoundError(KeyError)` subclass (Missed Opportunities, low priority). spec-compliance did not flag this. The tension is minimal -- both agree the current behavior is functional. schema-engineer's suggestion improves downstream ergonomics but is genuinely low priority and not a compliance gap. Noted here for completeness.

---

## Safe Agreements

### SA-1: FR-003 type declarations are materially wrong in the YAML schemas

Both reviews independently identified that multiple YAML fields declare `type: list[string]` while the actual data structure (in both examples and Pydantic models) is `dict[str, list[str]]` or `dict[str, str]`. schema-engineer (Rec 8) lists specific fields: `strategies`, `decision_variables`, `objectives`, `follower_variables`, `follower_objectives`. spec-compliance (Rec 1) lists the same fields with line-number references. Both rate this P1/P2.

The YAML schemas are meant to be the authoritative reference for data shape. When the declared types contradict the examples embedded in the same file, consumers cannot trust either. This is the highest-confidence finding across both reviews.

### SA-2: `_schema_dir()` path traversal will break in installed packages (FR-011)

Both reviews independently identified the same root cause (`Path(__file__).parent.parent.parent`) and the same consequence (`FileNotFoundError` in pip-installed environments). Both rate it P1. Both cite FR-011. The fix (importlib.resources or relocating YAML files) is agreed in direction if not in exact implementation.

### SA-3: `form` field needs `Literal` type constraints (FR-007)

Both reviews agree that `form: str = "normal-form"` with no validation allows cross-contamination (e.g., `NormalFormGame(form="gnep")` passes silently). schema-engineer rates it P1; spec-compliance rates it P2. The underlying finding is identical: FR-007 requires enforcement of type constraints, and the `form` discriminator is unconstrained. The priority difference reflects schema-engineer's emphasis on downstream union dispatch vs. spec-compliance's focus on what the spec literally requires today.

---

### Referenced Documentation

- schema-engineer review: `<HOME>/code/payer-index-mono/conversus/specs/012-game-form-schemas/conversus/schema-engineer/review.md`
- spec-compliance review: `<HOME>/code/payer-index-mono/conversus/specs/012-game-form-schemas/conversus/spec-compliance/review.md`
- spec: `<HOME>/code/payer-index-mono/conversus/specs/012-game-form-schemas/spec.md`
- game_forms.py: `<HOME>/code/payer-index-mono/conversus/src/conversus_schemas/game_forms.py`
