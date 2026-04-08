# Schema Engineer Revision: 012-game-form-schemas

**Reviewer**: schema-engineer
**Date**: 2026-03-22
**Revision**: 1 (post cross-review)

---

### Recommendation Dispositions

**Rec 1 — P1: Use `Literal` types for `form` discriminators.**
**Status: SURVIVING.**
All three reviewers agree this is needed. game-theorist calls it a prerequisite for their own solution-concept dispatch; spec-compliance agrees the fix is warranted but rates it P2 since no FR explicitly demands `Literal`. I maintain P1. The `Literal` constraint is not merely defensive -- it is load-bearing infrastructure for Rec 2 and for any downstream code that switches on `form`. A `NormalFormGame(form="gnep")` silently passing validation is a type-safety hole, not a spec-interpretation nicety. spec-compliance's point that FR-007 does not name `Literal` specifically is correct but immaterial: FR-007 says "enforce type constraints," and a bare `str` default with no constraint is the absence of enforcement.

**Rec 2 — P1: Create a discriminated union type `GameForm`.**
**Status: MODIFIED.** Downgraded to **P2**.
spec-compliance correctly identifies that no FR or SC in spec 012 requires a polymorphic union type. The union serves specs 013 and 016, not spec 012 itself. Calling it P1 conflates downstream ergonomics with the current spec's contract. game-theorist raises a sharper concern: building the union before adding a structured objective representation (optimization sense) creates adoption momentum for mathematically incomplete models. I accept both critiques. The union remains the right design, but its priority belongs in spec 013 or as an FR-012 amendment. Within spec 012's scope, the `Literal` fix (Rec 1) is the P1 prerequisite; the union is P2 contingent on confirming the objective representation is sufficient.

**Rec 3 — P1: Fix package data resolution for installed packages.**
**Status: SURVIVING.**
Universal agreement across all three reviews. The only tension is in the fix approach. spec-compliance notes that moving YAML files into `src/conversus_schemas/` would alter the paths mandated by FR-001, requiring a spec amendment. I accept this observation: the fix is not code-only. My updated recommendation: use `importlib.resources` with the YAML files relocated under `src/conversus_schemas/schema/game-forms/`, and amend FR-001 to reflect the new canonical location. Embedding as Python constants (one of my original suggestions) is withdrawn -- spec-compliance is right that it defeats the human-readable documentation purpose of the YAML files.

**Rec 4 — P1: Express `ParametricGame` inheritance from `GNEPGame`.**
**Status: MODIFIED.** Changed from direct inheritance to **extracted mixin/shared base**, downgraded to **P1 (implementation approach changed)**.
game-theorist raises a legitimate mathematical concern: a parametric game is not strictly a GNEP in the formal sense. The parameter vector changes solution existence conditions and algorithm selection. If `isinstance(parametric, GNEPGame)` returns `True`, solver plugins may silently apply GNEP algorithms to parametric problems. spec-compliance echoes this: `isinstance` contracts should not be established before downstream specs define whether they need them, and Pydantic model inheritance has subtle effects on `model_fields` merging and validator execution order.

I withdraw the recommendation for direct `ParametricGame(GNEPGame)` inheritance. The replacement: extract a `_GNEPStructureValidator` mixin (or private base class) containing the shared player-objective and player-decision-variable validation logic. Both `GNEPGame` and `ParametricGame` use this mixin, eliminating the verbatim code duplication (lines 137-163 vs. 186-215) without establishing a false is-a relationship. The `form` Literal discriminator (Rec 1) handles dispatch; `isinstance` is explicitly not the polymorphism mechanism. This satisfies the DRY principle, respects the mathematical distinction, and avoids locking in a subtype contract.

**Rec 5 — P2: Add `@field_validator("players")` for non-empty player lists.**
**Status: MODIFIED.** Scope narrowed to `len(players) >= 1` only; single-player "game" warning deferred.
game-theorist observes that a single-player game is mathematically degenerate (a decision problem, not a game) and suggests minimum player counts per form. This is mathematically sound but crosses from structural validation into mathematical semantics -- the kind of boundary the spec explicitly draws (Section 5: "data schemas, not computation"). A non-empty check (`len >= 1`) catches the trivially invalid case with no mathematical interpretation baked in. Form-specific minimum player counts (e.g., `N >= 2` for normal-form) are solver-adjacent metadata that belongs in mode-mapping notes or spec 017's solver configuration, not in the schema layer.

**Rec 6 — P2: Add `StackelbergGame` validator ensuring leader is not in followers.**
**Status: SURVIVING.**
game-theorist notes that if the Stackelberg schema is restructured for bilevel nesting, this check becomes structurally impossible (leader and followers are in different problem levels). However, game-theorist also concedes that bilevel restructuring is out of scope for spec 012 and should be deferred to spec 018. Within the current flat schema, the disjointness check is a semantic invariant that prevents a nonsensical game instance. I maintain P2. If bilevel nesting arrives later, the validator is trivially removed or becomes a no-op.

**Rec 7 — P2: Add `StackelbergGame` validator ensuring `leader_variables` is non-empty.**
**Status: MODIFIED.** Downgraded to **P3**.
spec-compliance observes that a degenerate Stackelberg game with no leader variables reduces to a standard game, which might be intentionally representable. This is a valid perspective -- the schema layer should not prohibit degenerate representations unless they produce undefined behavior. An empty `leader_variables` list is unusual but not structurally invalid. The check remains a good idea for a warning-level annotation or a strict validation mode, but it should not be a hard validation error at P2.

**Rec 8 — P2: Align YAML schema field types with Pydantic model types.**
**Status: MODIFIED.** Elevated to **P1** and expanded to include `VALID_FIELD_TYPES` enforcement.
spec-compliance's cross-review (DC-3) exposes a blind spot in my original recommendation: I treated this as a YAML-only fix (update the declared types), but `VALID_FIELD_TYPES` is dead code -- never referenced by any validator or test. Fixing the YAML types without wiring `VALID_FIELD_TYPES` into enforcement produces a three-way inconsistency (spec FR-003, the Python constant, the YAML declarations) instead of a two-way one. The correct fix is atomic: (1) expand `VALID_FIELD_TYPES` to include map types matching the actual Pydantic model types, (2) update the YAML `type` declarations to use the expanded vocabulary, and (3) add a validator or test that checks YAML field type declarations against `VALID_FIELD_TYPES`. This makes FR-003's "closed type set" an enforced contract rather than a documentation artifact. Elevated to P1 because the type system is foundational to every downstream spec that reads the YAML schemas.

**Rec 9 — P3: Export `ModeFormMapping` from `__init__.py`.**
**Status: SURVIVING.** No cross-reviewer disputed this. Remains a minor ergonomic improvement at P3.

**Rec 10 — P3: Add `model_config = ConfigDict(frozen=True)` to all game form models.**
**Status: SURVIVING.** No cross-reviewer disputed this. game-theorist's emphasis on these being definitional, mathematical structures reinforces the case for immutability. Remains P3 -- low urgency, high correctness signal.

---

### New Recommendations

**New-1 — P1: `constraint_list` must map to consistent Pydantic types or be split into `constraint_list` / `constraint_map`.**
This emerged from spec-compliance's cross-review (DC-3) and sharpens my original Off-Base Assumption #4. The YAML schemas use `constraint_list` for both `coupled_constraints: Optional[list[str]]` (a flat list) and `local_constraints: Optional[dict[str, list[str]]]` (a per-player mapping). The same type name mapping to structurally different Python types depending on context is a type-system violation. Either split the YAML type into `constraint_list` (flat) and `constraint_map` (per-player) with corresponding entries in `VALID_FIELD_TYPES`, or define `constraint_list` as always meaning the flat form and introduce `constraint_map` for the per-player form. This must be resolved alongside Rec 8 (type-set enforcement) since both touch `VALID_FIELD_TYPES` and the YAML type declarations.

**New-2 — P2: Sequence the discriminated union (Rec 2) after game-theorist's optimization-sense field.**
game-theorist's cross-review (Dangerous Contradiction 2) identifies a temporal ordering problem I missed: if the `GameForm` union is adopted by specs 013 and 016 before objectives are restructured from `str` to a structured `{sense, expression}` type, the `str` representation becomes load-bearing across multiple consumers, making the sense field a breaking change to retrofit. The resolution is not to abandon the union but to ensure the objective representation is finalized first. This is a sequencing constraint, not a design change. Concretely: spec 012 should either (a) add `optimization_sense: dict[str, Literal["minimize", "maximize"]]` as a top-level optional field on GNEP/Parametric/Stackelberg models now (staying within the existing type vocabulary), or (b) defer the union to spec 013 where the objective template can define the structured representation. I lean toward (a) because it is additive and backward-compatible.

**New-3 — P3: Document that solver plugins must dispatch on `form` discriminator, not `isinstance`.**
This emerged from the intersection of game-theorist's mathematical concern about `ParametricGame` not being a true GNEP subtype and my modified Rec 4 (mixin instead of inheritance). If neither inheritance nor `isinstance` is the polymorphism mechanism, the codebase needs an explicit convention. A brief docstring or module-level comment in `game_forms.py` stating "Downstream consumers should dispatch on the `form` field (or the `GameForm` discriminated union when available), not on `isinstance` checks" would prevent the exact failure mode game-theorist warned about.

---

### Position Summary

The cross-reviews from game-theorist and spec-compliance exposed two genuine blind spots in my original review. First, I treated the `ParametricGame` inheritance question as a pure software engineering problem (DRY, isinstance polymorphism) without weighing the mathematical consequence: a parametric game is not a GNEP in the formal sense, and establishing that subtype relationship in code would create a false contract for solver plugins. The mixin approach preserves code reuse without the misleading type hierarchy. Second, I treated the YAML-Pydantic type mismatch as a documentation fix (update the YAML declarations) without recognizing that `VALID_FIELD_TYPES` is dead code. spec-compliance correctly identified that fixing the YAML layer without wiring enforcement into the Python layer creates a worse inconsistency than the current state. The atomic fix -- expand the type set, update the YAML, and add enforcement -- is the right approach.

The discriminated union downgrade from P1 to P2 is the most significant change in this revision. spec-compliance's argument is correct on the merits: spec 012 does not require a union, and adding one conflates downstream needs with the current spec's contract. game-theorist's temporal ordering concern adds a second reason for caution: the union should not be built on mathematically incomplete models. I still believe the union is the single highest-impact design choice for the conversus schema ecosystem, but its proper home is in spec 013 or as a spec 012 amendment, not as a retroactive P1 compliance finding.

What survives scrutiny without modification: `Literal` types on `form` fields (Rec 1), package data resolution via `importlib.resources` (Rec 3), Stackelberg leader-follower disjointness (Rec 6), `frozen=True` for immutability signaling (Rec 10), and the new recommendation to split `constraint_list` / `constraint_map` (New-1). These are structural, low-risk, and uncontested. The revised priority ordering is: P1 = {Rec 1 (Literal), Rec 3 (package data), Rec 8 (type-set enforcement + YAML alignment), New-1 (constraint type split), Rec 4 (mixin extraction)}; P2 = {Rec 2 (union, sequenced after sense field), Rec 5 (non-empty players), Rec 6 (leader disjointness), New-2 (union sequencing)}; P3 = {Rec 7 (non-empty leader_variables), Rec 9 (exports), Rec 10 (frozen), New-3 (dispatch convention docs)}.
