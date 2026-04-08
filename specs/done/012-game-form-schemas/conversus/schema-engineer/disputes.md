# Schema Engineer — Final Disputes

**Reviewer**: schema-engineer
**Phase**: 4 (Final)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: `constraint_list` / `constraint_map` split MUST be part of the P1 atomic FR-003 remediation, not a separate work item

spec-compliance's New-1 correctly identifies that Recs 1, 6, and 9 should be an atomic FR-003 remediation. However, the proposed cluster omits my New-1 (the `constraint_list` / `constraint_map` type split) as a co-equal member of that cluster. spec-compliance elevates their Rec 6 to P1 as part of the cluster but frames it as constraint-type consistency — which is the same finding, differently worded.

The dispute is about completeness of the atomic unit. If we expand `VALID_FIELD_TYPES` to include `map[string, list[string]]` and `map[string, string]` (to cover `decision_variables`, `objectives`, `local_constraints`, `follower_variables`, `follower_objectives`, `follower_constraints`) but leave `constraint_list` as a single label mapping to two structurally different Python types (`list[str]` for `coupled_constraints`, `dict[str, list[str]]` for `local_constraints`), then the type set is internally inconsistent on the very fix we are making. `constraint_list` becomes a polymorphic type label in a system whose entire purpose is a closed, monomorphic type vocabulary.

The atomic unit must be: expand `VALID_FIELD_TYPES` with map types AND split `constraint_list` into `constraint_list` (flat) and `constraint_map` (per-player) AND update all YAML type declarations AND add the enforcement test. Doing the first without the second produces a type set that lies about its own closure property.

game-theorist has not contested this; spec-compliance agrees in substance (their Rec 6 revision). The dispute is only about whether this is explicitly inside the atomic P1 cluster or treated as a separate P1 that happens to land alongside it. I maintain it must be inside — partial type-set fixes are worse than the status quo because they create false confidence.

### Dispute 2: Minimum player count validation belongs in the schema layer, not deferred to solver specs

game-theorist's New-3 proposes `min_players` checks (N >= 2 for normal-form and GNEP, 1 leader + 1 follower for Stackelberg). In my revision, I narrowed my Rec 5 to `len(players) >= 1` only, arguing that form-specific minimums cross from structural validation into mathematical semantics.

On reflection, I conceded too much. The narrowing to `len >= 1` was correct as a floor, but I should not have deferred the N >= 2 check for normal-form and GNEP to solver specs. The argument that this is "solver-adjacent metadata" does not hold up. A zero-player or one-player NormalFormGame is not a degenerate game that solvers should handle gracefully — it is a structurally invalid instance that no solver can meaningfully process. The payoff matrix validator already assumes N >= 1 implicitly (it indexes `self.players`), and a one-player normal-form game collapses the payoff matrix to a 1D list of single-element payoffs, which is a decision problem with no game-theoretic content.

The spec says "finite players" (Section 2) and the Pydantic models are for "game theory form validation" (module docstring). A game with fewer than 2 players is not a game in any standard definition. This is a structural invariant, not a mathematical opinion. game-theorist agrees on the substance. spec-compliance has not addressed this directly.

I maintain: `len(players) >= 2` for NormalFormGame and GNEPGame, `len(followers) >= 1` for StackelbergGame (leader is already a single required field). Priority: P2 within spec 012, not deferred.

### Dispute 3: `frozen=True` should be P2, not P3

My Rec 10 proposed `model_config = ConfigDict(frozen=True)` at P3. No cross-reviewer contested it, but no one elevated it either. I now believe P3 underweights the risk.

These models represent mathematical definitions — game structures that, once validated, should be referentially stable. Without `frozen=True`, any downstream code can mutate a validated instance (e.g., `game.players.append("ghost_player")`) and the structural invariants verified by `model_validator` silently become stale. The model validators run at construction time only; post-construction mutation bypasses them entirely.

This is not hypothetical. In the conversus plugin architecture (specs 016-019), game form instances will be passed between the mode-mapping layer, the objective function library, and solver plugins. Any intermediate layer that accidentally mutates the instance (even appending to a list field) produces a validated-but-invalid object. `frozen=True` is the standard Pydantic mechanism to prevent this class of bug.

game-theorist's revision reinforces this: "these are definitional, mathematical structures" (their endorsement of my Rec 10). The risk profile is low (adding `frozen=True` is a one-line change per model) and the protection is high (prevents an entire category of post-validation corruption). P2 is the correct priority — it should ship with the `Literal` fix and the type-set remediation, not be deferred indefinitely.

---

## Convergence

### Convergence 1: Mixin extraction over direct inheritance for ParametricGame

All three reviewers now agree on the same approach: extract shared GNEP validation logic into a `_GNEPStructureValidator` mixin or private base class, used by both `GNEPGame` and `ParametricGame`. Direct `class ParametricGame(GNEPGame)` inheritance is withdrawn by all parties. game-theorist's mathematical argument (parametric games are not GNEPs in the formal sense) and my software engineering argument (false `isinstance` contract) converge on the same design. spec-compliance independently arrived at the same conclusion via a different path (spec says "inherits all GNEP fields," which is a composition statement, not a class hierarchy statement). This is genuine convergence from three independent lines of reasoning.

### Convergence 2: FR-003 type-set expansion is unidirectional — expand the spec to match the Pydantic models

All three reviewers agree the Pydantic models have the correct types and the YAML `type` declarations are wrong. The fix direction is to expand FR-003's closed type set and update the YAML declarations. No one advocates simplifying the Pydantic models to match the current YAML types. game-theorist provided the mathematical argument (retrograding destroys asymmetric game support); I provided the engineering argument (the Pydantic types are what downstream code actually consumes); spec-compliance withdrew the "or" framing and adopted the unidirectional position.

### Convergence 3: Discriminated union deferred to spec 013 or a spec 012 amendment

All three reviewers agree the `GameForm = Annotated[Union[...], Discriminator("form")]` union is the right design but belongs outside spec 012's current scope. I downgraded it from P1 to P2; spec-compliance confirmed no FR requires it; game-theorist added the temporal ordering constraint (union should not be built on mathematically incomplete models missing optimization sense). The `Literal` fix (my Rec 1) ships now as the prerequisite; the union ships when the objective representation is finalized.

### Convergence 4: `VALID_FIELD_TYPES` enforcement must be wired, not left as dead code

All three reviewers agree that `VALID_FIELD_TYPES` in its current form is dead code — defined but never referenced by any validator or test. spec-compliance elevated their Rec 9 from P3 to P1 after my cross-review identified the three-way inconsistency risk. game-theorist's type-set expansion recommendation (their Rec 9) is predicated on enforcement existing. The convergence is on both the problem (unenforced type sets are worse than no type sets) and the solution (a test that loads every YAML schema and asserts all `type` values are members of `VALID_FIELD_TYPES`).

### Convergence 5: `_schema_dir()` path resolution must use `importlib.resources`

All three reviewers identify `Path(__file__).resolve().parent.parent.parent` as broken for pip-installed deployments. All agree on `importlib.resources` as the fix mechanism. The only open question — whether YAML files move into `src/conversus_schemas/` (requiring an FR-001 amendment) or stay at `schema/game-forms/` with `[tool.setuptools.package-data]` configuration — is a project-level decision, not a design disagreement. Both approaches are acceptable; the current state is acceptable to no one.

---

## Final Position Statement

### Non-Negotiables

1. **`Literal` types on all `form` fields.** `form: str = "normal-form"` accepting arbitrary strings is a type-safety hole. Each model must constrain its `form` field to a single `Literal` value. This is P1 and prerequisite to any union type, any dispatch mechanism, and any downstream spec that pattern-matches on form identifiers. The implementation is trivial (`form: Literal["normal-form"] = "normal-form"`); the protection is foundational.

2. **FR-003 type-set remediation as a single atomic work unit.** The type-set expansion, the `constraint_list`/`constraint_map` split, the YAML declaration updates, the `VALID_FIELD_TYPES` constant update, and the enforcement test must ship together. Partial fixes create false confidence. This is P1. The specific types to add: `map[string, string]`, `map[string, list[string]]`, and the constraint type split replacing the polymorphic `constraint_list` with `constraint_list` (flat) and `constraint_map` (per-player keyed).

3. **`_schema_dir()` must use `importlib.resources`.** The current `Path(__file__).parent.parent.parent` resolution is broken for any non-editable install. This is not a theoretical concern — it is a `FileNotFoundError` waiting to happen for every downstream consumer that pip-installs the package. P1.

4. **Mixin extraction for GNEP/ParametricGame shared validation.** The 28 lines of verbatim-duplicated validation logic (lines 137-163 vs. 186-215 in `game_forms.py`) must be extracted into a shared mixin or private base class. Direct `ParametricGame(GNEPGame)` inheritance is explicitly rejected due to false `isinstance` contracts. The mixin approach is agreed by all three reviewers.

5. **Dispatch convention: `form` discriminator, not `isinstance`.** If neither inheritance nor `isinstance` is the polymorphism mechanism (and all three reviewers agree it should not be), the codebase needs an explicit statement. A module-level docstring or comment in `game_forms.py` establishing that downstream consumers must dispatch on the `form` field is the minimum viable documentation for this convention. Without it, the first solver plugin author will reach for `isinstance` and reintroduce the exact problem the mixin design was built to avoid.

### Flexibility

1. **Player count minimums.** I argue for `len(players) >= 2` on NormalFormGame/GNEPGame (Dispute 2 above), but I acknowledge this is debatable. If the group consensus is that single-player validation belongs in solver specs rather than the schema layer, I will accept `len >= 1` as the floor with a documented note that single-player instances are degenerate. I will not accept `len >= 0` (empty player list) passing validation under any framing.

2. **`frozen=True` priority.** I argue P2 (Dispute 3 above). If the group concludes P3 is appropriate given the current spec scope, I accept the deferral — provided it is explicitly tracked for the spec 013 work where game form instances start flowing between multiple consumers.

3. **Optimization sense field placement.** game-theorist's recommendation for a top-level `optimization_sense: dict[str, Literal["minimize", "maximize"]]` field is a clean, backward-compatible approach that stays within the existing type vocabulary. I endorse this over a structured objective type for spec 012. But I am flexible on whether it lands in spec 012 as an additive field or in a spec 012a amendment — the key constraint is that it must land before the discriminated union is published, per game-theorist's temporal ordering argument.

4. **Package naming (`conversus` vs. `conversus-schemas`).** This is a project-level architectural decision, not a schema engineering question. I flagged the mismatch; the resolution depends on whether the project intends `conversus` as an umbrella package. I defer to the project owner on direction and will implement whichever naming is chosen.

5. **Stackelberg leader-not-in-followers validator.** I maintain this at P2, but if bilevel restructuring is planned for spec 018 and would make the check structurally impossible, I accept deferring the validator to avoid throwaway work. However, the flat schema without this check allows `StackelbergGame(leader="X", followers=["X", "Y"])` to pass validation, which is nonsensical. If the validator is deferred, the gap should be documented.
