# Cross-Review: schema-engineer's Review of 012-game-form-schemas

**Cross-reviewer**: game-theorist
**Reviewing**: schema-engineer's Phase 1 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. ParametricGame inheritance — the polymorphism assumption conflicts with mathematical precision

schema-engineer recommends P1 priority: "Express `ParametricGame` inheritance from `GNEPGame`" so that `isinstance(parametric, GNEPGame)` returns `True` (schema-engineer Rec 4, lines 76-80). This is motivated by downstream polymorphism — specs 016-017 could accept "any GNEP-like game."

I did not flag this in my review, and I acknowledge schema-engineer's DRY reasoning is sound from a software engineering perspective. However, there is a mathematical tension: a parametric game is not a GNEP in the strict sense. A GNEP has objectives J_i(x_i, x_{-i}); a parametric game has objectives J_i(x_i, x_{-i}; p) where p is exogenous. The parameter vector changes the mathematical structure — sensitivity analysis, solution existence conditions, and solution algorithms are different. If `isinstance(parametric_game, GNEPGame)` returns `True`, solver plugins (spec 017) may silently apply GNEP algorithms to parametric problems, ignoring the parameter dependence entirely and producing incorrect results.

The danger is not inheritance itself but the implicit contract it creates. If downstream code treats every `GNEPGame` instance uniformly, parametric games lose their defining characteristic. A mixin or protocol-based approach that shares validation logic without establishing an is-a relationship would satisfy schema-engineer's DRY goal without creating a false mathematical subtyping claim. At minimum, if inheritance is used, the `form` Literal discriminator (schema-engineer Rec 1) must be enforced simultaneously so that solver dispatch always checks `form` rather than relying on `isinstance`.

**Resolution path**: Implement both Rec 1 (Literal discriminators) and Rec 4 (inheritance) together, and document that solver plugins MUST dispatch on the `form` discriminator, never on `isinstance` checks. Alternatively, extract a `_GNEPValidationMixin` that both `GNEPGame` and `ParametricGame` use without establishing an inheritance relationship.

### 2. Discriminated union without optimization sense creates a type-safe path to mathematically ambiguous games

schema-engineer's highest-impact recommendation is the discriminated union `GameForm` (Rec 2, lines 64-68): `GameForm = Annotated[Union[NormalFormGame, GNEPGame, ParametricGame, StackelbergGame], Discriminator("form")]`. This would let downstream specs write `game: GameForm` and get automatic deserialization.

In my review, I flagged that the schemas lack an optimization sense field (game-theorist Rec 1) — objectives like `"minimize x1^2 + x2^2 - y1"` embed the sense in the string, making it unparseable by machines. If the discriminated union is implemented before the sense field is added, we create a polished, ergonomic API for producing mathematically incomplete game instances. Downstream specs 013, 016, and 017 would adopt `GameForm` immediately, and every consumer would inherit the ambiguity.

The contradiction is temporal, not logical: both recommendations are independently correct, but implementing the union first creates adoption momentum that makes the sense field harder to retrofit. Adding `sense` later changes the `Objective` type from `str` to a structured object, which is a breaking change for every consumer that has already adopted the union.

**Resolution path**: Add the structured objective representation (`sense` + `expression` fields) to GNEP, parametric, and Stackelberg models before or simultaneously with the discriminated union. This ensures the union is built on mathematically complete models from day one.

### 3. Empty player list validator addresses the wrong mathematical concern

schema-engineer recommends a `@field_validator("players")` to reject empty player lists (Rec 5, lines 82-86), noting that an empty list "produces confusing downstream errors." I agree this is useful defensive programming, but there is a deeper mathematical gap both reviews should reconcile: the models also do not validate that `players` contains at least two entries for game forms where a single player is mathematically degenerate.

A normal-form game with one player is a decision problem, not a game. A GNEP with one player is a standard optimization problem. These are not invalid per se, but they change the mathematical category. schema-engineer's validator catches the trivially invalid case (zero players) but not the semantically misleading case (one player labeled as a "game"). Meanwhile, my review focused on higher-level mathematical omissions (mixed strategies, bilevel structure) without flagging this basic cardinality issue.

The danger: if we add a non-empty validator and stop there, we have a false sense of safety. One-player "games" will pass validation and flow into multi-agent equilibrium solvers that assume N >= 2.

**Resolution path**: The non-empty check is still worth adding (schema-engineer is right that zero players produces cryptic errors). But it should be accompanied by at least a warning-level annotation or a `min_players` field with form-specific defaults (2 for normal-form, 2 for GNEP, 1-leader + 1-follower for Stackelberg). This can be P2 alongside schema-engineer's P2 recommendation.

---

## Tensions

### 1. Scope of structural validation: how much math belongs in a schema?

schema-engineer's review focuses on what Pydantic can enforce: Literal types, discriminated unions, field validators, frozen models, JSON schema generation (Recs 1-3, 5-7, 10). My review focuses on what the mathematical structure demands: optimization sense, variable bounds, bilevel nesting, information structure, solution concepts (game-theorist Recs 1, 3, 5, 7, 8).

These are complementary, not conflicting, but they create a scope tension: how much mathematical structure should the Pydantic models enforce vs. how much should be delegated to downstream specs? schema-engineer implicitly draws the line at structural type safety — the models should use Pydantic's full type system to prevent invalid data shapes. My review implicitly draws the line at mathematical completeness — the models should capture enough structure that downstream solvers do not need to re-derive information.

This tension is productive. The resolution is probably phased: P1 includes schema-engineer's Literal/union changes and my optimization-sense field (both are structural, not computational). P2-P3 includes richer mathematical metadata (bounds, solution concepts, information structure) that may belong in a spec 012a amendment rather than the initial schema.

### 2. YAML-Pydantic type misalignment: cosmetic fix or structural problem?

Both reviews flag the `strategies: type: list[string]` vs. `dict[str, list[str]]` mismatch (schema-engineer Off-Base 3, lines 52-54; game-theorist Missed Opportunities, line 47, and Rec 2). schema-engineer frames this as a documentation/type-system problem — the YAML schema's declared types do not match the Pydantic models. I frame it as a mathematical ambiguity — `list[string]` implies a shared strategy set (symmetric game), which is a stronger condition.

The tension: schema-engineer recommends fixing the YAML type declarations to match the Pydantic models (Rec 8, line 100-104). I recommend the same (Rec 2, lines 65-69) but additionally call out that the closed type set (FR-003) needs expansion to include mapping types (Rec 9, lines 107-111). If the YAML types are fixed without expanding the closed type set, we violate FR-003. If we expand FR-003, we are amending the spec, not just fixing an implementation bug.

This is a genuine spec-level decision that both reviews surface from different angles. The resolution requires a spec amendment to FR-003, not just a code change.

### 3. Stackelberg validators: defensive programming vs. bilevel structure

schema-engineer recommends two Stackelberg validators: leader not in followers (Rec 6) and non-empty leader_variables (Rec 7). Both are correct structural checks. My review goes further and argues the Stackelberg schema is structurally incomplete because it does not model the bilevel optimization problem (game-theorist Rec 7, lines 95-99) — the follower's best-response mapping as a nested inner problem.

The tension: schema-engineer's validators make the current flat structure more robust. My recommendation would restructure the Stackelberg model significantly (adding `inner_problem` or `bilevel_structure` fields). These cannot both be P1 — adding validators to a structure that may be restructured creates throwaway work. If the bilevel restructuring happens, the leader/follower disjointness check would be expressed differently (leader is defined at the outer level, followers at the inner level, so overlap becomes structurally impossible).

The resolution depends on whether spec 012 is considered "schema vocabulary" (minimal structure, validators sufficient) or "mathematical formalization" (bilevel nesting required). I lean toward adding schema-engineer's validators now as P2 defensive measures, with my bilevel restructuring deferred to a spec 012a or spec 018 (Stackelberg solver spec).

### 4. Prisoner's dilemma mapping: game theory correctness vs. system design intent

My review flags the prisoner's-dilemma-to-GNEP mapping as mathematically imprecise (game-theorist Off-Base 1). schema-engineer's review does not address this mapping, focusing instead on implementation quality.

This is not a contradiction between our reviews but an unresolved tension in the spec itself: is the mode-mapping meant to be game-theoretically precise (PD is a normal-form game) or system-design pragmatic (the conversus PD mode uses coupled constraints, so GNEP is the right implementation form)? If schema-engineer's discriminated union (Rec 2) is implemented, the mapping becomes load-bearing — `mode_mapping.lookup("prisoners-dilemma")` would dispatch to `GNEPGame` validation, which would reject a standard PD payoff matrix because it lacks `decision_variables` and `objectives` fields.

The resolution requires a design decision from the spec author: either the PD mode genuinely uses GNEP structure (in which case the mode should document how the classic PD payoffs translate to continuous objectives with coupled constraints), or the mapping should be corrected to `normal-form`.

### 5. Package data resolution: agree on the problem, differ on urgency

schema-engineer flags `_schema_dir()` filesystem traversal as P1 (Rec 3, lines 70-74), arguing it will break when pip-installed. My review does not address packaging at all, focusing purely on mathematical structure. I acknowledge this is a blind spot in my review — schema-engineer is correct that the current code violates FR-010/FR-011 when installed outside the source tree. From my perspective, this is a P1 engineering concern that does not affect mathematical correctness, but it absolutely blocks the "pip-installable" requirement. No tension here — just an acknowledgment that schema-engineer caught something I did not.

---

## Safe Agreements

### 1. YAML schema type declarations must match Pydantic model types

Both reviews independently identify the same mismatch: `strategies` declared as `type: list[string]` in normal-form.yml but typed as `dict[str, list[str]]` in the Pydantic model (schema-engineer Off-Base 3; game-theorist Off-Base 3 and Rec 2). Both reviews agree this must be fixed, and both point to the closed type set (FR-003) as the root cause. This is a clear, uncontested P1 fix.

### 2. The form discriminator must be constrained, not a bare string

schema-engineer recommends `Literal` types on `form` fields (Rec 1, lines 58-62). My review does not explicitly recommend this but implicitly depends on it — my recommendation for a solution-concept field (Rec 5) assumes the form field reliably identifies the game type. A `NormalFormGame` with `form: "gnep"` would make my solution-concept validation logic incorrect.

Both reviews agree that `form: str` is too permissive. The Literal constraint is a prerequisite for schema-engineer's discriminated union and for my recommendation that the form field carry mathematical semantics. No disagreement.

### 3. Solver logic must remain out of scope

schema-engineer's Executive Summary explicitly endorses the "no solver imports" boundary (Alignment, line 24). My review's Executive Summary agrees that separating mathematical structure from solver logic is "standard practice in computational game theory." Neither review recommends pulling solver logic into the schema layer. My recommendations for optimization sense, variable bounds, and solution concepts are all metadata fields — they inform solvers without implementing them. schema-engineer's recommendations for validators, unions, and frozen models are all structural enforcement — they constrain data shapes without computing solutions.

This shared boundary is important because the pressure to add solver-adjacent logic will increase as specs 013-019 build on these schemas. Both reviews implicitly agree the line should hold.

### 4. Structural validators catch real mathematical invariants

schema-engineer praises the `model_validator(mode="after")` usage for cross-field checks (Alignment, line 19). My review confirms the same validators correspond to necessary mathematical conditions (game-theorist Alignment, lines 21-28). The player-objective bijection in GNEP, the payoff tensor dimensionality in normal-form, and the non-empty parameter vector in parametric games are all mathematically required structural invariants that the validators correctly enforce. Neither review disputes the existing validators — the disagreements are about what additional invariants are missing.

---

*Cross-review complete. The two reviews are largely complementary: schema-engineer optimizes the Pydantic implementation for type safety and ergonomics; game-theorist optimizes the mathematical content for downstream correctness. The three dangerous contradictions (inheritance semantics, union-before-sense ordering, and player cardinality scope) all have clear resolution paths that honor both perspectives.*
