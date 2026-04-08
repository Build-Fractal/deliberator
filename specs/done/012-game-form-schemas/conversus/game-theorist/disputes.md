# Game-Theorist Final Disputes

**Reviewer**: game-theorist
**Phase**: Final (pre-synthesis)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: Optimization sense must not be deferred past the discriminated union

schema-engineer's revised position (New-2) leans toward adding `optimization_sense: dict[str, Literal["minimize", "maximize"]]` as a top-level optional field now — option (a) — rather than deferring the union to spec 013. I agree with (a) but dispute the "optional" qualifier.

The mathematical problem: an objective expression like `"x1^2 + x2^2 - y1"` is meaningless without a sense. Is the player trying to make this quantity small or large? Every standard optimization modeling language (AMPL, GAMS, Pyomo, CVXPY) requires the sense at declaration time — it is not metadata, it is part of the problem definition. The GNEP YAML example already embeds sense into the expression strings (`"minimize x1^2 + x2^2 - y1"`), proving the information is structurally necessary. But embedding sense in a free-text string is the worst of both worlds: the information is present but unparseable.

Making the field optional allows game instances with objectives that have no declared sense. A solver consuming such an instance must either refuse it (breaking the contract that schemas are sufficient structural descriptions) or guess (defaulting to minimize, which is a hidden assumption that silently corrupts maximization problems).

**My position**: `optimization_sense` should be required on GNEP, Parametric, and Stackelberg models, not optional. For the normal-form model it is inapplicable (payoffs are values, not expressions to optimize). If the field must ship as optional for backward compatibility in this spec cycle, the default must be explicitly documented as `"minimize"` per convention, and the schema description must state that omitting it implies minimization. An undocumented implicit default is the specific failure mode I am guarding against.

spec-compliance may argue that requiring a new field violates the current spec. I accept that a spec amendment is the proper vehicle. But the amendment must land in the same work unit as the discriminated union — not after. This is the sequencing constraint I raised in my revision (New-2), and schema-engineer partially endorsed it. I am sharpening it: the union must not ship with optional-sense objectives.

### Dispute 2: Minimum player cardinality is a schema concern, not a solver concern

schema-engineer's revision (Rec 5 modification) narrows the player validator to `len(players) >= 1` and explicitly defers form-specific minimum counts (N >= 2 for normal-form games) to "solver-adjacent metadata." I dispute this classification.

A normal-form game with one player is not a game. This is not a matter of mathematical opinion or convention — it is a definitional boundary. Von Neumann and Morgenstern's original formulation, Nash's existence theorem, every textbook definition of a strategic-form game requires N >= 2 players. A single-agent decision problem has no strategic interaction, no equilibrium concept, and no payoff interdependence. Allowing it through the schema layer means a consumer receiving a `NormalFormGame` instance cannot rely on the most basic property of the object it holds: that it describes a game.

schema-engineer argues the schema layer should not encode "mathematical semantics." But the schema already encodes mathematical semantics: the payoff matrix dimension validator checks that dimensions match strategy set cardinalities, the objective-player correspondence validator checks bijection between players and objectives, and the follower-variable matching validator checks structural consistency. All of these are mathematical invariants, not just structural shape checks. The line that schema-engineer draws — "structural validation yes, mathematical semantics no" — is not where the code actually draws it.

**My position**: `NormalFormGame` should validate `len(players) >= 2`. `GNEPGame` and `ParametricGame` should validate `len(players) >= 2`. `StackelbergGame` already structurally requires at least 2 (one leader + at least one follower). This is a single line of code per model (`if len(self.players) < 2: raise ValueError(...)`) with zero risk of false positives — no legitimate game instance has fewer than 2 players. Priority P3 is acceptable; the principle is not.

### Dispute 3: `constraint_list` / `constraint_map` split must preserve the mathematical distinction, not just the type-system distinction

All three reviewers agree that `constraint_list` mapping to two different Python types is broken and must be split. The convergence is on the action; the dispute is on the semantics of the split.

schema-engineer and spec-compliance frame this as a type-system hygiene issue: one YAML type name should not map to two Python types. This is correct but insufficient. The mathematical distinction between local constraints and coupled constraints is not merely a type difference — it is a structural property of the game that determines algorithm selection and solution existence.

Local constraints `g_i(x_i) <= 0` are separable: each constraint depends only on one player's variables. This separability is what allows decomposition algorithms (Jacobi, Gauss-Seidel best-response) to solve each player's subproblem independently. Coupled constraints `h(x_1, ..., x_N) <= 0` bind all players' decisions together, requiring shared-constraint algorithms (variational inequality methods, penalty approaches, augmented Lagrangian).

If the type split is done purely as a naming exercise — `constraint_list` for flat, `constraint_map` for per-player — without documenting the mathematical invariant that `constraint_map` entries must be separable by player, then the type system permits a `local_constraints` field containing constraints that reference other players' variables (e.g., `agent_1: ["x1 + y1 <= 5"]`). This would be a structurally valid but mathematically invalid GNEP instance: a local constraint that is actually coupled. The type system cannot enforce the algebraic separability condition at schema time, but the documentation must make the invariant explicit so that downstream validators or solvers can check it.

**My position**: The `constraint_map` type definition in YAML and its `VALID_FIELD_TYPES` entry must carry a description stating that per-player constraint entries are semantically local — they encode the assumption that each entry depends only on the keyed player's decision variables. spec-compliance's New-2 (document constraint-scoping convention) aligns with this, and I endorse it fully. But I want it elevated from "nice-to-have documentation" to a required part of the type-split work unit. The type name change without the semantic annotation solves half the problem.

---

## Convergence

### Convergence 1: FR-003 type-set expansion is the foundational fix

All three reviewers agree that the FR-003 closed type set cannot express the types actually in use (`dict[str, list[str]]`, `dict[str, str]`), that the fix direction is unidirectional (expand the type set, do not regress the Pydantic models), and that the fix must be atomic: expand `VALID_FIELD_TYPES`, update all YAML `type` declarations, and add enforcement that validates YAML types against the constant. spec-compliance's New-1 (treat Recs 1, 6, and 9 as a single atomic FR-003 remediation) captures this correctly. I endorse this as the single highest-priority work unit.

### Convergence 2: `Literal` types on `form` fields are a prerequisite, not an option

All three reviewers agree that `form: str = "normal-form"` with no constraint is a type-safety hole. A `NormalFormGame(form="gnep")` silently passing validation violates FR-007's "enforce type constraints" requirement. The `Literal` fix is P1 and is a prerequisite for any discriminated union work. No remaining dispute.

### Convergence 3: ParametricGame validation deduplication via mixin, not inheritance

All three reviewers converge on: (a) the verbatim code duplication between `GNEPGame` and `ParametricGame` validators is a correctness risk (drift will happen), (b) direct `class ParametricGame(GNEPGame)` inheritance creates a false `isinstance` contract, (c) a shared mixin or private base class eliminates duplication without establishing the misleading subtype relationship. schema-engineer proposed this in their revised Rec 4; I endorsed it in my revision (New-1); spec-compliance confirmed the approach in their revised Rec 5. The implementation detail (mixin vs. private base) is a code-review-level decision, not a design dispute.

### Convergence 4: Bilevel Stackelberg nesting deferred to spec 017/018

All three reviewers agree the flat Stackelberg schema with role separation is adequate for spec 012's "mathematical vocabulary" scope. The bilevel nesting — outer optimization over inner best-response — is structurally necessary for solver implementation but belongs in the Stackelberg solver spec, not the schema spec. In the interim, the flat schema should have: (a) leader-follower disjointness validation (schema-engineer Rec 6, uncontested), and (b) a documentation note that the leader's objective implicitly assumes anticipation of follower best-response. No remaining dispute on sequencing.

### Convergence 5: Package data resolution is broken and must be fixed atomically

All three reviewers independently confirmed that `_schema_dir()` using `Path(__file__).parent.parent.parent` will fail in any pip-installed deployment. The fix is `importlib.resources` with appropriate `package-data` configuration. If file relocation is required, FR-001 must be amended in the same work unit. No remaining dispute.

---

## Final Position Statement

### Non-Negotiables

1. **The strategies type declaration in normal-form YAML must be fixed to a mapping type.** The current `type: list[string]` declares a symmetric game; the Pydantic model and example both use `dict[str, list[str]]` (asymmetric, which is the general case). This is not a cosmetic mismatch — it is a mathematically incorrect declaration. Any consumer reading the YAML schema to understand the data contract will build a symmetric-game parser that fails on asymmetric instances. The fix direction is unidirectional: expand FR-003 and update the YAML, never regress the Pydantic model.

2. **Optimization sense must be structurally present before the discriminated union is adopted.** An objective without a declared sense is an incomplete mathematical object. If the union ships with `str`-typed objectives and no sense field, every downstream consumer adopts an API for producing ambiguous game instances, and adding sense later is a breaking change. The sense field — whether as a companion field on game models or as a structured objective type — must be part of the same work unit as the union. If the union is deferred, the sense field should still be added proactively; but the union must never ship without it.

3. **The `constraint_map` type split must carry semantic documentation of the separability assumption.** Renaming the type without documenting what it means mathematically (per-player entries depend only on the keyed player's variables) solves the type-system problem while leaving the mathematical problem unaddressed. The documentation is not optional garnish; it is the only mechanism the schema layer has to communicate the separability invariant that determines algorithm selection downstream.

### Flexibility

- **Priority of the optimization-sense field**: I am flexible on whether it ships as P1 in this spec cycle or as a mandatory prerequisite in a spec 012a amendment, as long as the sequencing constraint relative to the union is maintained. The mathematical requirement is firm; the timeline is negotiable.

- **Priority of minimum player cardinality**: I accept P3. The principle matters more than urgency. If schema-engineer and spec-compliance agree it should exist but at low priority, I can live with that ordering.

- **Placement of solution-concept metadata**: I withdrew my original recommendation to put `solution_concept` on the game form models and endorsed schema-engineer's alternative of placing it in the mode-mapping layer. I remain flexible on exact placement as long as the information is machine-readable somewhere in the schema ecosystem.

- **Prisoner's-dilemma mode mapping**: I accept that the current `prisoners-dilemma -> gnep` mapping is procedurally mandated by FR-004 and should not be changed without a spec amendment. My residual concern (the mode name is misleading if the conversus PD mode genuinely uses coupled constraints) is a documentation/naming issue, not an implementation dispute. I defer to the spec author on whether to amend the note or the mapping.

- **`frozen=True` on models**: I support this for mathematical correctness (game definitions are immutable mathematical objects) but it is not load-bearing for any current use case. P3 is fine.
