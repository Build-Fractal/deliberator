# Cross-Review: spec-compliance's Phase 1 Review

**Cross-reviewer**: game-theorist
**Reviewing**: spec-compliance's review of spec 012-game-form-schemas
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: The FR-003 type mismatch is a mathematical correctness problem, not just a compliance gap

spec-compliance correctly identifies that at least six fields declare `type: list[string]` in YAML while the Pydantic models and examples use `dict`-like structures (spec-compliance Rec 1, Missed Opportunities items 1-5). I flagged the same issue from a different angle: the `list[string]` declaration for `strategies` implies all players share a single strategy set, which is the definition of a symmetric game -- a much stronger mathematical condition than the general normal-form definition (game-theorist Off-Base item 3, Rec 2).

Where the two reviews risk contradiction: spec-compliance frames this as "expand the FR-003 type set or fix the YAML declarations" -- treating either direction as acceptable. From the game theory perspective, only one direction is correct. The YAML type declarations must change to mapping types. Collapsing per-player strategy sets into a flat list does not merely violate a compliance checklist; it destroys the mathematical structure of asymmetric games. Treating this as a two-sided option (fix spec or fix YAML) obscures the fact that the Pydantic model has the right mathematical structure and the YAML declaration has the wrong one. The spec's FR-003 closed type set needs to be expanded; retrograding the Pydantic models to match the YAML declarations would introduce mathematical errors.

**Resolution**: Both reviews should converge on expanding FR-003 to include `map[string, list[string]]`, `map[string, string]`, and potentially `map[string, object]`. The YAML declarations must then be updated to use those types. The reverse direction (simplifying Pydantic models to flat lists) is not viable.

### DC-2: `constraint_list` semantic ambiguity masks a structural modeling decision

spec-compliance notes (Rec 6) that `constraint_list` in the YAML schemas is typed as a flat list but modeled in Pydantic as `Optional[dict[str, list[str]]]` for local constraints (a per-player mapping) and `Optional[list[str]]` for coupled constraints (a flat list). spec-compliance proposes adding a `constraint_map` type or clarifying the semantics. My review (Off-Base item 2) raises a related but distinct issue: whether local constraints can depend on other players' variables (`g_i(x_i)` vs. `g_i(x_i, x_{-i})`).

These are dangerously intertwined. The choice of data structure -- flat list vs. per-player mapping -- is not just a type system question; it encodes a mathematical assumption about constraint scoping. If `local_constraints` is a per-player mapping `{agent_1: [...], agent_2: [...]}`, the schema structurally enforces that constraints are partitioned by player, which aligns with the strict `g_i(x_i)` formulation. If it were a flat list, the scoping would be ambiguous. spec-compliance treats this as a type-declaration issue; I treat it as a mathematical modeling decision. Both are right, but they need to be resolved jointly: fix the type declaration to `constraint_map` **and** add a note clarifying the variable-scoping convention, because the two issues are coupled.

**Resolution**: Add `constraint_map` (or `map[string, constraint_list]`) to FR-003 to match the Pydantic structure, and simultaneously add the clarifying note about local-constraint variable scoping that my review recommends (game-theorist Rec 10). These should be a single coordinated change.

### DC-3: `ParametricGame` inheritance vs. duplication -- compliance and mathematical consequences diverge

spec-compliance (Rec 5) identifies that `ParametricGame` duplicates `GNEPGame` validation logic (lines 186-209 mirror 137-162) instead of inheriting from `GNEPGame` as the spec states ("Inherits all GNEP fields"). This is framed as a code maintenance concern: "future GNEP invariant changes will not propagate."

From the game theory perspective, the consequence is more severe. A parametric game is mathematically defined as a GNEP parameterized by exogenous variables: the game structure is `GNEP + parameters`. If `ParametricGame` does not inherit from `GNEPGame`, then adding mathematical invariants to the GNEP model (for example, my recommendation for optimization-sense fields, or variable-bound specifications) will silently fail to apply to parametric games. This is not just code drift -- it means the parametric game schema could accept instances that are mathematically invalid GNEPs, which undermines the entire "inherits all GNEP fields" contract.

However, Pydantic model inheritance has its own subtleties (validator method resolution order, field ordering). A naive `class ParametricGame(GNEPGame)` may not behave as expected with `model_validator` decorators on both parent and child. The implementation concern is real.

**Resolution**: The fix should use Pydantic inheritance with explicit validator chaining, or extract the shared validation logic into a reusable function called by both models. The mathematical requirement (parametric games must satisfy all GNEP invariants) is non-negotiable; only the implementation strategy is flexible.

### DC-4: Package naming and schema-dir resolution are entangled with mathematical usability

spec-compliance raises two P1 issues: the package name is `conversus` instead of `conversus-schemas` (Rec 2), and the `_schema_dir()` function uses relative path traversal that breaks after pip installation (Rec 3). My review does not address packaging at all -- it is outside my domain.

However, there is a dangerous implication for mathematical usability that neither review fully articulates. If downstream specs (013-020) cannot reliably load the YAML schemas at runtime, they cannot programmatically inspect the game form structure. This means solver plugins would have to hardcode their understanding of each game form's fields rather than discovering them from the schema. The mathematical vocabulary that spec 012 establishes becomes documentation rather than machine-readable structure -- which defeats the spec's stated purpose ("machine-readable," L15). spec-compliance's packaging recommendations are therefore not merely compliance items; they are preconditions for the schemas to function as the shared mathematical vocabulary they claim to be.

**Resolution**: I concur with spec-compliance's P1 prioritization for Recs 2 and 3. The `importlib.resources` approach or moving YAML files into the package directory should be prioritized before downstream specs begin consuming these schemas.

---

## Tensions

### T-1: Scope of the `form` field -- Literal enforcement vs. flexibility

spec-compliance (Rec 4) proposes using `Literal["normal-form"]` etc. for the `form` field, primarily as a compliance matter (FR-007 requires "type constraints") and to enable future discriminated unions. My review does not address this directly.

There is a tension: strict `Literal` typing makes the schemas rigid, which is correct for the four known forms. But if the game form library is intended to be extensible (the spec does not say one way or the other), `Literal` types would require code changes to add new forms. The mathematical question is whether the four forms constitute a closed taxonomy or an open one. Normal-form, GNEP, parametric, and Stackelberg do not cover all of game theory (extensive form, Bayesian games, mean-field games are absent). If extensibility is intended, a `Literal` union should be defined in a single place and extended centrally. If the taxonomy is closed for conversus purposes, `Literal` is the right choice.

This is a design decision the spec should make explicit, and both reviews would benefit from that clarity.

### T-2: VALID_FIELD_TYPES as dead code -- enforcement granularity

spec-compliance (Rec 9) notes that `VALID_FIELD_TYPES` is defined but never enforced -- no validation checks that YAML `type` values are members of this set. This is correct. My review does not raise this directly, but my recommendation to expand the type set (game-theorist Rec 9) implicitly assumes the set will eventually be enforced.

The tension: if `VALID_FIELD_TYPES` is enforced, every YAML schema addition requires updating the constant first. This is either a safeguard (prevents typos in type declarations) or a bottleneck (slows down schema evolution), depending on the development workflow. From a mathematical standpoint, a validated closed type set is valuable because it ensures all downstream tooling can handle every type that appears. But the enforcement must happen at the right layer -- in a schema-loading validation step, not in the Pydantic game models themselves (which validate game instances, not schema definitions).

### T-3: Optimization sense -- where it belongs in the spec lifecycle

My review (Rec 1, P1) calls for adding `sense: minimize | maximize` as a structured field on every objective. spec-compliance does not raise this issue at all, which is expected given its compliance-focused scope: the spec does not require optimization sense, so its absence is not a compliance gap.

The tension: from a spec-compliance perspective, adding optimization sense would be a scope expansion beyond the current FRs. From a game theory perspective, it is a mathematical necessity -- without it, the schemas are ambiguous. Both perspectives are valid. The resolution is that this should be raised as a spec amendment (adding a new FR) rather than treated as a defect in the current implementation. spec-compliance's silence on this point is procedurally correct even though the mathematical gap is real.

### T-4: Prisoner's dilemma mapping -- compliance vs. mathematical precision

My review (Off-Base item 1, Rec 4) flags the `prisoners-dilemma -> gnep` mapping as mathematically imprecise: the prisoner's dilemma is the canonical normal-form game, not a GNEP. spec-compliance marks FR-004 as "Fully met" because the mapping matches the spec's explicit requirement.

Both positions are correct within their frames. The spec says `prisoners-dilemma -> gnep`, and the implementation matches. But the spec itself may encode a mathematical error if the conversus prisoners-dilemma mode does not actually involve coupled constraints (the defining feature of GNEP). The resolution depends on whether the mode genuinely has shared feasibility constraints or merely PD-like payoff incentives. This is a question about the upstream mode definitions (which are outside spec 012's scope) but has mathematical consequences for the schema layer.

### T-5: SC-001 literal interpretation vs. correct testing

spec-compliance (Rec 7) notes that SC-001's literal code (`NormalFormGame.model_validate(yaml.safe_load(open(...)))`) would validate the entire YAML file, not just the `example` key, and would fail because the top-level file contains `fields` and `description` which are not game model fields. The test correctly extracts `data["example"]` first.

This is a genuine tension in the spec: SC-001 as literally written is a failing test, yet the intent is clear. spec-compliance correctly identifies this and recommends either clarifying SC-001's wording or adding a comment. From the game theory perspective, the test is mathematically correct -- the example data is the game instance, not the schema metadata. The spec's success criterion conflates the schema definition document with the game instance it describes. This should be fixed in the spec text, not in the test.

---

## Safe Agreements

### SA-1: Player-objective bijection enforcement is mathematically sound

Both reviews agree that the Pydantic validators correctly enforce a one-to-one mapping between players and objectives (spec-compliance Alignment FR-007, game-theorist Alignment items 1-2). In game theory, a game is not well-defined unless every player has exactly one objective function. The validators for `GNEPGame`, `ParametricGame`, and `StackelbergGame` all check this invariant, and the tests in `TestSC002GNEPMismatch` cover missing-objective, extra-objective, and cross-form scenarios. This is correct and complete.

### SA-2: Payoff tensor validation captures the right mathematical structure

Both reviews agree that the recursive `_validate_matrix` in `NormalFormGame` correctly enforces that the payoff tensor has dimensions |S_1| x |S_2| x ... x |S_N| x N (spec-compliance Alignment FR-007, game-theorist Alignment item 4). This matches the mathematical definition: a normal-form game's payoff function u: S_1 x S_2 x ... x S_N -> R^N must assign a real-valued payoff to each player for every joint strategy profile. The implementation handles N-player games correctly through recursion, not just the 2-player case shown in the example.

### SA-3: Solver-library boundary is correctly maintained

Both reviews confirm that FR-008 is fully met: no solver imports appear in `game_forms.py`, and the test `test_no_solver_imports` checks for `nashopt`, `jax`, `scipy`, and `amplpy` (spec-compliance Alignment FR-008, game-theorist Alignment -- implicit in the "no solver logic" scope agreement). This boundary is mathematically appropriate: game form schemas define the problem structure, not the solution method. Mixing schema and solver concerns would violate the standard separation between problem formulation and algorithm selection in computational game theory.

---

## Summary

The two reviews are broadly complementary. spec-compliance focuses on FR/SC coverage and packaging mechanics; the game-theorist review focuses on mathematical fidelity and downstream solver implications. The most important convergence point is the FR-003 type mismatch (DC-1): both reviews identify it, but the resolution must go in one direction only (expand the type set, not simplify the models). The most important divergence is on items like optimization sense (T-3) where spec-compliance's procedural correctness ("the spec doesn't require it") conflicts with mathematical necessity. These tensions should be resolved through spec amendments before downstream specs 013-020 consume the schemas.
