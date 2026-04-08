# Cross-Review of game-theorist's Review

**Cross-reviewer**: schema-engineer
**Reviewing**: game-theorist Phase 1 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: Optimization sense -- structured field vs. expression string scope

game-theorist's top recommendation (P1, Rec #1) proposes replacing `objectives: dict[str, str]` with `objectives: dict[str, Objective]` where `Objective` has `sense: Literal["minimize", "maximize"]` and `expression: str`. I agree this is mathematically correct and would eliminate string-parsing fragility. However, this recommendation conflicts with the spec's own FR-003, which defines a closed type set of `string`, `integer`, `float`, `list[string]`, `list[float]`, `matrix`, `function`, `constraint_list`. There is no `object` or `struct` type in this set. Introducing a nested `Objective` type in the Pydantic model while the YAML schema layer has no way to express it will widen the YAML-Pydantic divergence that both reviews flag (game-theorist Rec #2, schema-engineer Rec #8).

The contradiction is: game-theorist's Rec #1 makes the Pydantic layer richer, but game-theorist's own Rec #9 (expand the closed type set) only proposes `dict[string, list[string]]` and `dict[string, object]`, not a nested struct type. If we add `Objective` to Pydantic but leave the YAML schema declaring `objectives` as `type: function`, we get exactly the documentation fiction I flagged in my review (Off-Base Assumption #4 re: `constraint_list`).

**Resolution**: The optimization-sense field and the type-set expansion must be delivered together. Either extend FR-003's closed type set to include `struct` or inline compound types before adding the `Objective` model, or embed sense as a separate top-level field (`optimization_sense: dict[str, Literal["minimize", "maximize"]]`) that stays within the existing type vocabulary.

### DC-2: ParametricGame inheritance model

game-theorist validates that the parametric form "correctly models J_i(x_i, x_{-i}; p) where p is exogenous" (Alignment, bullet 5) and treats the flat-composition implementation as adequate. My review (Rec #4, P1) flags that `ParametricGame(BaseModel)` duplicating all GNEP fields and validation logic is a maintenance hazard and breaks `isinstance(parametric, GNEPGame)` -- a property downstream specs will rely on for polymorphic dispatch.

These positions are in direct tension. game-theorist's silence on the inheritance question implicitly endorses the current flat structure, while my review calls it P1. The code evidence is clear: `ParametricGame.validate_structure` (lines 186-215) is a verbatim copy of `GNEPGame.validate_structure` (lines 137-163) plus the parameter check. A bug fixed in one will not propagate to the other. Furthermore, game-theorist's own Rec #5 (solution-concept field) would need to be added to both models independently under flat composition, compounding the drift risk.

**Resolution**: game-theorist should explicitly weigh in on whether `ParametricGame` should inherit from `GNEPGame`. The mathematical relationship (parametric game *is-a* GNEP with exogenous parameters) supports inheritance. If there is a game-theoretic reason to keep them structurally independent (e.g., different solution-concept spaces), that rationale should be stated.

### DC-3: Prisoner's dilemma mapping -- normal-form vs. GNEP

game-theorist's Off-Base Assumption #1 correctly identifies that the classical prisoner's dilemma is a 2x2 normal-form game, not a GNEP, and recommends either remapping to `normal-form` or clarifying the note (Rec #4, P2). My review does not address this mapping question because it falls outside schema-engineering scope.

The contradiction is subtle but important: game-theorist proposes option (a) "map to normal-form" as the cleaner choice, but the spec prose (Section 2, GNEP Form, line 45) explicitly states the PD mode's use case justification as "coupled constraints (shared target document, budget, timeline)." If the conversus PD mode genuinely has coupled constraints, it cannot be a normal-form game -- normal form has no constraint concept. Mapping it to normal-form would require removing the coupled-constraint semantics that the spec says the mode needs. Mapping it to GNEP preserves the operational semantics but misuses the game-theoretic name.

**Resolution**: This needs a domain decision, not a schema decision. If the conversus PD mode has coupled constraints, keep the GNEP mapping but rename the note per game-theorist's option (b). If it truly models a 2x2 payoff matrix with no constraints, map it to normal-form. The schema layer should not encode a lie in either direction.

### DC-4: Bilevel structure in Stackelberg vs. schema-layer scope

game-theorist's Rec #7 (P2) proposes adding a `bilevel_structure` field or nesting the follower problem as an explicit inner problem with `leader_anticipates_best_response: true`. My review's Rec #6 and #7 for Stackelberg focus on missing validators (leader-not-in-followers disjointness, non-empty leader_variables) -- structural invariants that the current flat schema can enforce without changing the data model.

The contradiction: game-theorist's bilevel nesting proposal would fundamentally restructure `StackelbergGame`, while my validators work with the existing flat schema. If bilevel nesting is adopted, my disjointness validator becomes trivial (leader and followers are in different structural positions) and my non-empty-leader-variables check moves to the inner/outer problem boundary. Implementing my validators first, then restructuring for bilevel nesting, wastes the validator work.

**Resolution**: Sequence matters. If bilevel nesting is accepted (and I think the mathematical argument for it is sound), design the nested structure first, then add validators to the new structure. Do not add validators to the flat schema and then immediately restructure. My Rec #6 (leader-not-in-followers) should be implemented regardless of structure -- it is a semantic invariant, not a structural one.

---

## Tensions

### T-1: Mixed-strategy support -- schema change vs. interpretation flag

game-theorist's Rec #6 (P2) proposes adding `strategy_space: pure | mixed` to normal-form. This is mathematically well-motivated (Nash 1950 guarantees existence in mixed strategies). From a schema-engineering perspective, this is clean -- a single `Literal` field, no structural change. However, the tension is in what "mixed" means for the payoff matrix. Under mixed strategies, the payoff matrix still represents pure-strategy payoffs; the expected payoff is computed by the solver, not stored in the schema. game-theorist acknowledges this ("The schema structure does not change -- only the interpretation"), but a field that changes interpretation without changing validation is unusual in Pydantic modeling. It is metadata, not a validated constraint.

This is a legitimate tension, not a contradiction. Both approaches work. My preference: implement it as `strategy_space: Literal["pure", "mixed"] = "pure"` with a `Field(description=...)` annotation making the interpretation explicit. No validator needed -- it is solver guidance, not a structural invariant.

### T-2: Variable bounds vs. constraint encoding

game-theorist's Rec #3 (P1) proposes structured variable bounds (`domain: real, lower: 0, upper: 1`). My review does not flag this directly, but my Off-Base Assumption #4 (constraint_list as documentation fiction) is related: the current models already struggle to represent the types they declare. Adding a nested variable-bound structure would further widen the gap between the YAML schema's type vocabulary and the Pydantic model's actual types.

The tension: variable bounds are mathematically important for solver selection (game-theorist is right that box constraints vs. general constraints affects algorithm choice), but adding them now means extending the closed type set to support nested objects in the YAML layer. This amplifies the type-system debt I flagged. The question is whether to fix the type system first (my Rec #8, P2) or add bounds first (game-theorist Rec #3, P1).

My position: fix the type-system alignment (YAML types matching Pydantic types) before adding new complex types. Otherwise we accumulate more documentation fiction.

### T-3: Solution-concept field -- schema vs. runtime concern

game-theorist's Rec #5 (P2) proposes an optional `solution_concept` field on each game form. From a schema-engineering standpoint, this mixes definitional data (game structure) with operational intent (what to solve for). The spec explicitly says (Section 5, Constraint 1): "Must NOT include solver logic. These are data schemas, not computation." A `solution_concept` field does not contain solver logic per se, but it carries solver-selection intent.

The tension is real: game-theorist is right that the same game admits different equilibrium concepts, and my review's Rec #2 (discriminated union `GameForm`) would benefit from knowing the solution concept to dispatch correctly. But adding it here blurs the boundary between spec 012 (schemas) and spec 017-019 (solvers). An alternative: define solution concepts in the mode-mapping layer rather than in the game-form schema itself. The mode mapping already carries `note` fields that could be formalized into `solution_concept` without touching the game-form models.

### T-4: Information-structure field priority

game-theorist's Rec #8 (P3) proposes an `information_structure: simultaneous | sequential | partial` field. game-theorist self-assesses this as low priority ("the form names imply the information structure"). From a schema perspective, I agree with the low priority but for a different reason: adding a field whose value is fully determined by the `form` discriminator violates DRY. If `form == "normal-form"` always implies `simultaneous` and `form == "stackelberg"` always implies `sequential`, the field adds no information. It becomes useful only when a game form can have multiple information structures (e.g., a GNEP with sequential moves), which is not in the current spec scope.

Tension, not contradiction: game-theorist is thinking ahead to future extensibility; I am thinking about current schema minimality. Both perspectives are valid. The resolution is to defer this until a game form actually needs non-default information structure.

### T-5: `ModeMapping.lookup()` exception type

game-theorist's review does not address this, but my review (Missed Opportunities, bullet 7) flags that `lookup()` raises raw `KeyError`. The existing implementation (game_forms.py L291-296) already provides a clear error message in the `KeyError`, so the functional impact is low. The tension is between Pythonic convention (KeyError for missing dict keys is standard) and API ergonomics (a custom `ModeNotFoundError` is more discoverable). This is minor but worth noting for alignment: game-theorist's silence on exception design suggests it is not a game-theory concern, which is correct -- it is purely a schema-engineering concern.

---

## Safe Agreements

### SA-1: YAML-Pydantic type mismatch on `strategies` field

Both reviews independently flag the same defect. game-theorist (Off-Base #3, Rec #2 P1): "normal-form.yml declares `strategies` as `type: list[string]`, but the Pydantic model types it as `dict[str, list[str]]`." My review (Off-Base #3, Rec #8 P2): "YAML says `strategies` has type `list[string]`, but the model types it as `dict[str, list[str]]`." We agree on both the diagnosis and the fix: update the YAML schema's type declaration to match the Pydantic model. This is unambiguously a bug, not a design choice.

### SA-2: Structural validators are correctly placed and well-implemented

game-theorist's Alignment section validates the mathematical correctness of the payoff-tensor dimensionality check, player-objective bijection, and coupled/local constraint separation. My Alignment section validates the Pydantic implementation quality: correct use of `model_validator(mode="after")`, actionable error messages, proper `Optional` typing. We independently confirm the same conclusion from different angles: the validators that exist are correct and well-engineered. The gap is in validators that are missing (both reviews agree more are needed), not in validators that are wrong.

### SA-3: Package-data resolution via filesystem traversal will break on pip install

game-theorist does not flag this directly, but my review (Off-Base #1, Rec #3 P1) identifies that `_schema_dir()` uses `Path(__file__).parent.parent.parent / "schema"`, which fails outside the source tree. game-theorist's Alignment section implicitly assumes the schema files are accessible (all YAML file references use absolute paths from the source tree). Neither review disputes that FR-010 and FR-011 require pip-installable package data. The agreement is that the current filesystem traversal approach is incompatible with the spec's stated packaging requirements.

### SA-4: No solver imports -- correctly enforced and tested

game-theorist's Alignment confirms FR-008 compliance from the mathematical side (schemas contain no computation). My Alignment confirms it from the implementation side (`test_no_solver_imports` reloads the module and checks `sys.modules`). Both reviews treat this as a strength of the current implementation, not a concern.

---

## Summary

The two reviews are largely complementary: game-theorist evaluates mathematical completeness and fidelity to game-theoretic definitions, while schema-engineer evaluates type safety, validation coverage, and API ergonomics. The dangerous contradictions center on sequencing (which changes must land together to avoid widening the YAML-Pydantic gap) and structural decisions (inheritance vs. composition, flat vs. nested schemas) where the mathematical and engineering perspectives lead to different priorities. The safe agreements confirm that the existing implementation is sound within its scope -- the debate is about what that scope should be.
