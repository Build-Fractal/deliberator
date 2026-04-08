# Deliberation Synthesis: 012-game-form-schemas

**Synthesizer**: neutral (no agent affiliation)
**Date**: 2026-03-22
**Target spec**: `/conversus/specs/012-game-form-schemas/spec.md`

---

## Process Summary

| Metric | Count |
|---|---|
| Agents | 3 (game-theorist, schema-engineer, spec-compliance) |
| Phase 1 reviews | 3 |
| Phase 1 recommendations total | 30 (game-theorist: 10, schema-engineer: 10, spec-compliance: 10) |
| Phase 2 cross-reviews | 6 (each agent reviewed both others) |
| Dangerous contradictions surfaced (Phase 2) | 13 across all cross-reviews |
| Tensions surfaced (Phase 2) | 15 across all cross-reviews |
| Safe agreements surfaced (Phase 2) | 13 across all cross-reviews |
| Phase 3 revisions | 3 |
| Recommendations surviving Phase 3 unchanged | 10 |
| Recommendations modified in Phase 3 | 14 |
| Recommendations withdrawn in Phase 3 | 1 (game-theorist Rec 8: information-structure field) |
| New recommendations added in Phase 3 | 8 (game-theorist: 3, schema-engineer: 3, spec-compliance: 3) |
| Phase 4 disputes remaining | 8 (game-theorist: 3, schema-engineer: 3, spec-compliance: 3) |
| Phase 4 convergence points | 15 (game-theorist: 5, schema-engineer: 5, spec-compliance: 5) |

The deliberation exhibited strong convergence on structural issues (type-system alignment, package data resolution, mixin extraction, Literal types) and productive tension on scope issues (how much mathematical metadata belongs in a schema-only spec vs. deferred to solver specs). One recommendation was withdrawn entirely. The remaining disputes are primarily about priority calibration, scope boundaries, and procedural sequencing -- not about whether the underlying issues are real.

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|---|---|---|---|---|---|---|
| GT-1 | game-theorist | Add optimization-sense field to objectives | P1 | MODIFIED to spec amendment; flexible on timeline | schema-engineer (type-set conflict), spec-compliance (scope creep beyond FRs) | Partial -- all agree sense is needed; dispute over required vs. optional and timing relative to union | Disputed: required vs. optional, timing |
| GT-2 | game-theorist | Fix strategies type declaration in normal-form YAML | P1 | SURVIVING | None -- universally confirmed | Full convergence (all 3 agents) | Resolved P1 |
| GT-3 | game-theorist | Add variable bounds/domain fields | P1 | MODIFIED: downgraded to P2, deferred to spec 012a or 017 | spec-compliance (scope creep), schema-engineer (type-system debt) | Partial -- mathematical merit accepted, scope deferred | Deferred to future spec |
| GT-4 | game-theorist | Correct prisoner's-dilemma mode mapping | P2 | MODIFIED: downgraded to P3, reframed as documentation/naming issue | spec-compliance (FR-004 compliance), schema-engineer (domain decision needed) | Partial -- mathematical objection valid, but FR-004 mandates current mapping | Deferred to spec author |
| GT-5 | game-theorist | Add solution-concept field | P2 | MODIFIED: moved from game-form models to mode-mapping layer | schema-engineer (schema/solver boundary), spec-compliance (scope) | Full convergence on placement change | Resolved P2 (mode-mapping layer) |
| GT-6 | game-theorist | Add mixed-strategy indicator to normal form | P2 | SURVIVING | spec-compliance (no current mode needs it) | Partial -- low-cost addition accepted | Surviving P2 |
| GT-7 | game-theorist | Model bilevel structure in Stackelberg | P2 | MODIFIED: deferred to spec 017/018, add validators + doc note instead | schema-engineer (sequencing), spec-compliance (scope) | Full convergence on deferral | Deferred; flat-schema validators accepted |
| GT-8 | game-theorist | Add information-structure field | P3 | WITHDRAWN | schema-engineer (DRY violation, redundant with form name) | Full convergence on withdrawal | Withdrawn |
| GT-9 | game-theorist | Expand closed type set (FR-003) | P3 | SURVIVING; upgraded to P2 | None | Full convergence (all 3 agents); subsumed into atomic FR-003 remediation | Resolved P1 (via atomic cluster) |
| GT-10 | game-theorist | Add local-constraint generality note | P3 | SURVIVING | None | Uncontested | Surviving P3 |
| GT-N1 | game-theorist | ParametricGame should share GNEP validation logic (mixin) | New (P2) | New in Phase 3 | None -- converges with SE-4 and SC-5 | Full convergence (all 3 agents) | Resolved P1 |
| GT-N2 | game-theorist | Coordinate optimization-sense with union sequencing | New (P2) | New in Phase 3 | None | Partial -- temporal constraint accepted; implementation timing disputed | Disputed (timing) |
| GT-N3 | game-theorist | Validate minimum player cardinality per game form | New (P3) | New in Phase 3 | schema-engineer (P3 narrowing to len>=1) | Disputed -- game-theorist and schema-engineer both now advocate N>=2; spec-compliance silent | Disputed (N>=1 vs. N>=2) |
| SE-1 | schema-engineer | Use `Literal` types for `form` discriminators | P1 | SURVIVING | None -- universally confirmed | Full convergence (all 3 agents) | Resolved P1 |
| SE-2 | schema-engineer | Create discriminated union type `GameForm` | P1 | MODIFIED: downgraded to P2, deferred | spec-compliance (no FR requires it), game-theorist (temporal ordering with sense field) | Full convergence on deferral | Deferred P2 |
| SE-3 | schema-engineer | Fix package data resolution (`importlib.resources`) | P1 | SURVIVING | None -- universally confirmed | Full convergence (all 3 agents) | Resolved P1 |
| SE-4 | schema-engineer | Express ParametricGame inheritance from GNEPGame | P1 | MODIFIED: changed to mixin extraction, not direct inheritance | game-theorist (false isinstance contract), spec-compliance (Pydantic MRO concerns) | Full convergence on mixin approach | Resolved P1 (mixin) |
| SE-5 | schema-engineer | Add `@field_validator("players")` for non-empty lists | P2 | MODIFIED: narrowed to len>=1 floor | game-theorist (argues N>=2 is the correct minimum) | Disputed -- len>=1 vs. len>=2 | Disputed (min cardinality) |
| SE-6 | schema-engineer | Stackelberg leader-not-in-followers validator | P2 | SURVIVING | game-theorist (accept now, may be superseded by bilevel nesting later) | Partial -- accepted for flat schema | Surviving P2 |
| SE-7 | schema-engineer | Stackelberg non-empty leader_variables validator | P2 | MODIFIED: downgraded to P3 | spec-compliance (degenerate case may be intentional) | Partial | Surviving P3 |
| SE-8 | schema-engineer | Align YAML schema field types with Pydantic model types | P2 | MODIFIED: elevated to P1, expanded to include VALID_FIELD_TYPES enforcement | spec-compliance (dead code concern) | Full convergence -- subsumed into atomic FR-003 remediation | Resolved P1 (via atomic cluster) |
| SE-9 | schema-engineer | Export `ModeFormMapping` from `__init__.py` | P3 | SURVIVING | None | Uncontested | Surviving P3 |
| SE-10 | schema-engineer | Add `frozen=True` to all game form models | P3 | SURVIVING; schema-engineer argues P2 in disputes | None contests the idea; priority disputed | Disputed (P2 vs. P3) | Disputed (priority) |
| SE-N1 | schema-engineer | Split `constraint_list` / `constraint_map` in type set | New (P1) | New in Phase 3 | None -- aligns with SC-6 and GT Dispute 3 | Full convergence on the split; dispute on whether it is inside or outside the atomic P1 cluster | Resolved P1 (inside atomic cluster) |
| SE-N2 | schema-engineer | Sequence union after optimization-sense field | New (P2) | New in Phase 3 | None | Aligns with GT-N2 | Surviving P2 (sequencing constraint) |
| SE-N3 | schema-engineer | Document `form` discriminator dispatch convention | New (P3) | New in Phase 3 | None | Uncontested | Surviving P3 |
| SC-1 | spec-compliance | Expand FR-003 type set or fix YAML type declarations | P1 | MODIFIED: direction locked to "expand type set" only | game-theorist (unidirectional) | Full convergence | Resolved P1 (via atomic cluster) |
| SC-2 | spec-compliance | Fix package name to `conversus-schemas` (FR-010) | P1 | MODIFIED: reframed as project-owner decision | schema-engineer (intent unclear) | Full convergence that mismatch is P1; direction needs project owner | Resolved P1 (needs project owner) |
| SC-3 | spec-compliance | Configure YAML files as package data (FR-011) | P1 | SURVIVING | schema-engineer (may conflict with FR-001 paths) | Full convergence; implementation detail open | Resolved P1 |
| SC-4 | spec-compliance | Add `Literal` types for `form` field (FR-007) | P2 | MODIFIED: elevated to P1 | None -- universally confirmed | Full convergence | Resolved P1 |
| SC-5 | spec-compliance | Make ParametricGame inherit from GNEPGame | P2 | MODIFIED: elevated to P1, implementation changed to mixin | game-theorist (isinstance concern), schema-engineer (same) | Full convergence on mixin | Resolved P1 (mixin) |
| SC-6 | spec-compliance | `constraint_list` type consistency in YAML | P2 | MODIFIED: elevated to P1 as part of atomic cluster | schema-engineer (documentation fiction) | Full convergence | Resolved P1 (via atomic cluster) |
| SC-7 | spec-compliance | SC-001 test granularity clarification | P2 | SURVIVING; flexible on P2 or P3 | schema-engineer (overweighted as P2) | Partial | Surviving P2-P3 |
| SC-8 | spec-compliance | Negative tests for `form` field mismatch | P3 | SURVIVING | None | Uncontested | Surviving P3 |
| SC-9 | spec-compliance | Test `VALID_FIELD_TYPES` covers all YAML types | P3 | MODIFIED: elevated to P1 | schema-engineer (dead code enforcement) | Full convergence -- part of atomic cluster | Resolved P1 (via atomic cluster) |
| SC-10 | spec-compliance | Add `ModeMapping`/`ModeFormMapping` to exports | P3 | SURVIVING | None | Uncontested | Surviving P3 |
| SC-N1 | spec-compliance | Treat Recs 1, 6, 9 as single atomic FR-003 remediation | New (P1) | New in Phase 3 | schema-engineer (must also include constraint split) | Full convergence on expanded cluster | Resolved P1 |
| SC-N2 | spec-compliance | Document constraint-scoping convention with type fix | New (P2) | New in Phase 3 | game-theorist (elevate to required, not optional) | Partial convergence | Disputed (required vs. nice-to-have) |
| SC-N3 | spec-compliance | Acknowledge FR-011 fix may require FR-001 amendment | New (P2) | New in Phase 3 | None | Uncontested | Surviving P2 |

---

## Dangerous Contradictions Found

### Resolved Contradictions

**1. Type-set expansion direction (unidirectional vs. bidirectional)**
- spec-compliance originally framed the FR-003 type mismatch as "expand type set OR fix YAML declarations," implying either direction was acceptable.
- game-theorist identified that simplifying the Pydantic models to match the current YAML types would destroy asymmetric game support -- a mathematical regression.
- **Resolution**: spec-compliance withdrew the "or" framing in Phase 3. All three agents agree the fix is unidirectional: expand FR-003's type set to accommodate the Pydantic model types. The YAML declarations change; the Pydantic models do not.

**2. ParametricGame: direct inheritance vs. mixin**
- schema-engineer originally proposed `class ParametricGame(GNEPGame)` for DRY and `isinstance` polymorphism.
- game-theorist argued a parametric game is not mathematically a GNEP (different solution existence conditions, algorithm selection), so `isinstance(parametric, GNEPGame)` returning `True` would mislead solver plugins.
- spec-compliance added that Pydantic model inheritance has MRO and field-ordering subtleties.
- **Resolution**: All three agents converge on extracting a `_GNEPStructureValidator` mixin or private base class that both `GNEPGame` and `ParametricGame` use. No `isinstance` contract. Dispatch via `form` Literal discriminator. Unanimously resolved.

**3. Discriminated union priority (P1 vs. deferred)**
- schema-engineer originally rated the `GameForm` discriminated union as the "single highest-impact change" at P1.
- spec-compliance noted no FR or SC in spec 012 requires it.
- game-theorist added a temporal ordering constraint: the union should not ship before objectives gain a structured `sense` field, or consumers adopt an API for mathematically incomplete models.
- **Resolution**: schema-engineer downgraded to P2. All three agree the union is the right eventual design but should be introduced via spec 013 or a spec 012 amendment, after the objective representation is finalized.

**4. Prisoner's-dilemma mapping (normal-form vs. GNEP)**
- game-theorist argued the classical PD is a 2x2 normal-form game, so mapping it to GNEP is mathematically imprecise.
- spec-compliance noted FR-004 explicitly mandates `prisoners-dilemma -> gnep`, so changing the mapping without a spec amendment would introduce a compliance violation.
- schema-engineer noted the spec prose justifies GNEP by referencing coupled constraints in the conversus PD mode.
- **Resolution**: game-theorist accepted the procedural argument and reframed as a documentation/naming issue. The mapping stays as-is; the recommendation is downgraded to P3 (clarify the mode-mapping note). Deferred to the spec author for a naming/documentation decision.

### Unresolved Contradictions

**5. Optimization sense: required vs. optional field**
- game-theorist insists `optimization_sense` must be required (an objective without a sense is an incomplete mathematical object; defaults create hidden assumptions).
- schema-engineer endorses adding it but leans toward optional for backward compatibility.
- spec-compliance considers it a spec amendment, not a compliance finding against current FRs.
- **Synthesizer assessment**: game-theorist's mathematical argument is sound -- an objective expression without a declared sense is genuinely ambiguous. However, spec-compliance is procedurally correct that this requires a spec amendment. The pragmatic resolution is to add it as required in the spec amendment, with a documented default convention (`minimize`) for any transitional period where instances lack the field. The requirement should be part of the same work unit as the discriminated union.

**6. Minimum player cardinality: len>=1 vs. len>=2**
- schema-engineer initially proposed len>=1, arguing form-specific minimums are "mathematical semantics" beyond the schema layer.
- game-theorist and schema-engineer (revised position in disputes) both now advocate len>=2, arguing a one-player game is definitionally not a game.
- spec-compliance has not directly addressed this.
- **Synthesizer assessment**: game-theorist's definitional argument is correct -- a one-player instance of `NormalFormGame` is a decision problem, not a game, and the models already encode mathematical invariants (payoff dimensionality, player-objective bijection) of comparable specificity. The len>=2 check for NormalFormGame and GNEPGame is appropriate at P2-P3. It is a single line of code per model with no false-positive risk.

---

## Systemic Contradictions

### 1. Schema minimalism vs. mathematical completeness
The most pervasive tension across the deliberation. spec-compliance consistently argues that spec 012 should implement exactly what its FRs require -- no more, no less. game-theorist consistently argues that schemas should capture enough mathematical structure that downstream solvers do not need to re-derive information. schema-engineer mediates between these positions, generally siding with structural type safety now and deferring richer mathematical metadata. This tension manifests in the optimization-sense dispute, the variable-bounds deferral, the solution-concept placement, and the mixed-strategy indicator debate. The resolution pattern that emerged: mathematical enrichments are accepted in principle but routed through spec amendments rather than treated as implementation bugs in the current spec.

### 2. Spec compliance vs. spec correctness
spec-compliance treats the spec text as the contract and flags deviations from it. game-theorist and schema-engineer sometimes identify cases where the spec itself is wrong (FR-003's type set is too narrow, FR-004's PD mapping may be mathematically imprecise, SC-001's literal code would fail). The tension between "the implementation diverges from the spec" and "the spec is wrong" recurs in at least four recommendation pairs. The resolution pattern: when the spec is wrong, the fix requires a spec amendment first, then an implementation change -- never an implementation-only change that contradicts the spec text.

### 3. Type-system debt accumulation
Multiple recommendations propose adding richer types (structured objectives, variable bounds, nested bilevel structures) to the Pydantic models. schema-engineer consistently warns that adding Pydantic complexity without corresponding YAML type vocabulary expansion creates "documentation fiction" -- the YAML schemas become less trustworthy as the Pydantic models grow more expressive. This tension led to the atomic FR-003 remediation cluster and the principle that type-set expansion and enforcement must be delivered together.

### 4. Downstream coupling vs. spec isolation
schema-engineer and game-theorist frequently justify recommendations by referencing downstream specs (013 objective templates, 016 plugin system, 017-019 solver plugins). spec-compliance consistently pushes back: spec 012's scope is defined by its own FRs, and downstream needs should drive downstream specs or spec amendments, not retroactive priority inflation. This tension is healthy and produced the correct resolution in most cases (discriminated union deferred, variable bounds deferred, bilevel nesting deferred), but it also means some mathematically important additions (optimization sense) risk being perpetually "next spec's problem."

### 5. Procedural sequencing vs. implementation pragmatism
spec-compliance insists that spec amendments must precede implementation changes when the spec text itself needs to change (FR-003 expansion, package naming). schema-engineer and game-theorist tend toward implementation-first approaches where the code change is clearly correct and the spec amendment is a paperwork formality. The resolution pattern: spec-compliance's procedural position is formally correct, but in practice the spec amendment and implementation change should be coordinated as a single work unit rather than serialized into separate phases.

---

## Convergence Achieved

Listed in order of strength (unanimous first).

### 1. YAML-Pydantic type mismatch is the highest-impact bug (UNANIMOUS)
All three agents independently identified that at least 6 YAML fields declare `type: list[string]` while examples, Pydantic models, and mathematical semantics all require mapping types (`dict[str, list[str]]`, `dict[str, str]`). The fix direction is unidirectional (expand FR-003's type set). The fix must be atomic: amend FR-003, expand `VALID_FIELD_TYPES`, update YAML declarations, add enforcement testing. This is the single strongest consensus finding across the entire deliberation.

### 2. `Literal` types on `form` fields are required (UNANIMOUS)
All three agents agree that `form: str = "normal-form"` accepting arbitrary strings is a type-safety hole. `Literal["normal-form"]` is independently justified by FR-007 ("enforce type constraints") and is a prerequisite for any future discriminated union. The implementation is trivial; the protection is foundational.

### 3. `_schema_dir()` path resolution is broken for installed packages (UNANIMOUS)
All three agents independently confirmed that `Path(__file__).parent.parent.parent` will produce `FileNotFoundError` in any pip-installed deployment, violating FR-011. The fix is `importlib.resources` with `[tool.setuptools.package-data]` configuration. If YAML files are relocated, FR-001 must be amended in the same work unit.

### 4. ParametricGame validation deduplication via mixin, not inheritance (UNANIMOUS)
All three agents converge from independent reasoning paths: game-theorist (false mathematical subtyping), schema-engineer (false `isinstance` contract), spec-compliance ("inherits all GNEP fields" is a composition statement, not a class hierarchy statement). The agreed design: `_GNEPStructureValidator` mixin or private base class, used by both models, with `form` Literal discriminator for dispatch.

### 5. Discriminated union deferred to spec 013 or a spec 012 amendment (UNANIMOUS)
All three agree the `GameForm` union is the right eventual design but is out of scope for the current spec. The `Literal` fix ships now as the prerequisite. The union ships when objective representation is finalized and a downstream spec needs it.

### 6. `constraint_list` must be split into `constraint_list` / `constraint_map` (UNANIMOUS)
All three agree that one YAML type name mapping to two structurally different Python types (`list[str]` for coupled constraints, `dict[str, list[str]]` for local constraints) is a type-system violation. The split must be part of the atomic FR-003 remediation cluster. Minor dispute remains on whether the semantic documentation of the separability assumption is "required" (game-theorist) or "recommended" (spec-compliance).

### 7. Solver-library boundary is correctly maintained (UNANIMOUS)
All three agents confirm FR-008 is fully met. No solver imports appear in the schema code, and the test suite explicitly checks for prohibited libraries. This boundary is well-tested and should hold as downstream specs build on the schemas.

### 8. Package name mismatch requires project-owner resolution (UNANIMOUS)
All three agents agree the discrepancy between FR-010 (`conversus-schemas`) and `pyproject.toml` (`conversus`) is a P1 violation. The direction of resolution (rename the package or amend FR-010) depends on project-level architectural intent that no reviewer can determine unilaterally.

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

### Dispute 1: Optimization sense -- required vs. optional, and timing relative to discriminated union

**Positions**:
- **game-theorist**: `optimization_sense` must be a required field on GNEP, Parametric, and Stackelberg models. An objective without a declared sense is an incomplete mathematical object. If the field ships as optional, the default must be explicitly documented as `"minimize"`. The field must be part of the same work unit as the discriminated union -- the union must never ship with optional-sense objectives.
- **schema-engineer**: Endorses adding the field as a top-level `optimization_sense: dict[str, Literal["minimize", "maximize"]]` for backward compatibility. Leans toward adding it in spec 012 as an additive, optional field. Agrees with the temporal sequencing constraint relative to the union.
- **spec-compliance**: Treats this as a spec amendment, not a compliance finding. Does not contest the mathematical argument but insists the amendment must precede the implementation. Flexible on whether the amendment happens now or is deferred to specs 017-019.

**Arguments**:
- game-theorist's core argument is sound: every standard optimization modeling framework (AMPL, GAMS, Pyomo, CVXPY) requires sense at declaration time. The GNEP YAML example already embeds sense in expression strings (`"minimize x1^2 + x2^2 - y1"`), proving the information is structurally necessary but currently unparseable by machines.
- spec-compliance's procedural argument is also sound: the current spec does not require this field, and adding it requires an FR amendment.
- The "required vs. optional" sub-dispute is a backward-compatibility question. Making it required would break existing valid YAML instances; making it optional with a documented default is the pragmatic path.

**Synthesizer assessment**: The mathematical argument for the field's existence is conclusive. The "required vs. optional" question should be resolved in favor of required-in-the-spec-amendment with a documented convention that omission implies `minimize` for a transitional period. The temporal sequencing constraint (field must precede or accompany the union) is well-reasoned and should be adopted. This dispute is primarily about timing, not substance.

**Recommended resolution**: File a spec 012a amendment adding `optimization_sense` as a required field. The amendment and the discriminated union should be coordinated as a single work unit. During the transitional period before the amendment is implemented, document that omission implies minimization.

---

### Dispute 2: Minimum player cardinality -- len>=1 vs. len>=2

**Positions**:
- **game-theorist**: `NormalFormGame` and `GNEPGame` should validate `len(players) >= 2`. A one-player game is not a game by any standard definition (Von Neumann-Morgenstern, Nash). This is a structural invariant of the same kind already enforced (payoff dimensionality, player-objective bijection).
- **schema-engineer**: Initially proposed len>=1 only. Revised position in disputes: now argues for len>=2 on NormalFormGame and GNEPGame, and `len(followers) >= 1` for StackelbergGame. Accepts P2 priority.
- **spec-compliance**: Has not directly addressed this. General position is that validators not enumerated in the spec are "hardening recommendations," not compliance gaps.

**Synthesizer assessment**: game-theorist's definitional argument is correct, and schema-engineer now agrees. The models already enforce mathematical invariants of comparable specificity (payoff tensor dimensions matching strategy cardinalities is a mathematical invariant, not just a structural shape check). A one-player `NormalFormGame` is meaningless in game theory. The implementation cost is one line per model. P2-P3 is the appropriate priority.

**Recommended resolution**: Add `len(players) >= 2` validation to NormalFormGame and GNEPGame, and `len(followers) >= 1` to StackelbergGame, at P2 priority. These are defensive validators that do not require a spec amendment (FR-007 says "enforce structural invariants" without enumerating which ones).

---

### Dispute 3: `constraint_map` semantic documentation -- required part of type split vs. optional enhancement

**Positions**:
- **game-theorist**: The `constraint_map` type definition must carry documentation stating that per-player constraint entries are semantically local -- they depend only on the keyed player's decision variables. This documentation is a required part of the type-split work unit, not optional garnish. Without it, the type system permits structurally valid but mathematically invalid GNEP instances.
- **spec-compliance**: Agrees in substance (their New-2 recommends documenting the scoping convention). Frames it as P2 documentation, not as a required companion to the P1 type fix.
- **schema-engineer**: Implicitly agrees through their endorsement of the atomic remediation cluster but does not explicitly address the documentation requirement.

**Synthesizer assessment**: game-theorist is correct that the type name change without semantic documentation solves only half the problem. However, spec-compliance's point that the documentation is a different deliverable from the type-system fix has merit -- the type labels can be correct even if the documentation is incomplete. The pragmatic resolution is to include the semantic documentation in the same PR as the type split, but not to block the type split on the documentation if they are developed by different authors.

**Recommended resolution**: Include constraint-scoping documentation (local constraints depend only on the keyed player's variables; coupled constraints may involve all players) in the YAML schema `description` fields as part of the FR-003 remediation work unit. P1 for the type split; P2 for the documentation, but both should land in the same PR.

---

### Dispute 4: `frozen=True` priority -- P2 vs. P3

**Positions**:
- **schema-engineer**: Argues P2. Game form instances will flow between multiple consumers in specs 016-019. Without `frozen=True`, post-construction mutation bypasses validators. One-line change per model, high protection.
- **game-theorist**: Supports for mathematical correctness (game definitions are immutable mathematical objects). Accepts P3.
- **spec-compliance**: Has not contested the idea. Implicitly accepts P3 by not engaging.

**Synthesizer assessment**: The risk of post-validation mutation is real but theoretical in the current spec scope (no consumers yet exist). The fix is trivial. P3 is appropriate for spec 012; P2 is appropriate for the work unit that introduces multi-consumer flows (spec 016).

**Recommended resolution**: P3 for spec 012. Elevate to P2 when spec 016 (plugin system) implementation begins, as that is when game form instances start flowing between multiple consumers.

---

### Dispute 5: FR-003 amendment sequencing -- spec amendment before or alongside implementation

**Positions**:
- **spec-compliance**: The FR-003 type set is an explicit spec requirement. Implementation changes that use types not in FR-003 without a formal spec amendment create "a codebase that contradicts its own spec." The deliverable sequence must be: (1) FR-003 spec amendment, (2) code changes, (3) compliance re-verification.
- **schema-engineer**: Treats the atomic remediation (expand VALID_FIELD_TYPES, update YAML, add enforcement test) as self-contained. Does not explicitly require a formal spec amendment step.
- **game-theorist**: Agrees the direction is non-negotiable but does not address the procedural sequencing.

**Synthesizer assessment**: spec-compliance is formally correct that changing implementation to use types not in FR-003 without amending FR-003 produces a non-compliant codebase. However, requiring strict sequential ordering (amendment document first, then code) is unnecessarily rigid when both can be delivered in the same PR. The spec amendment and the code change are logically atomic.

**Recommended resolution**: The FR-003 spec amendment and the implementation changes should be delivered as a single atomic work unit (same PR or same release). The spec amendment text should be finalized before or alongside the code, never after.

---

### Dispute 6: `Literal` type justification -- intrinsic FR-007 vs. downstream union needs

**Positions**:
- **spec-compliance**: `Literal` types are P1 because FR-007 says "enforce type constraints" and `form: str` with no constraint is not enforcement. This justification is intrinsic to spec 012 and independent of any downstream union.
- **schema-engineer**: `Literal` types are P1 primarily as infrastructure for the discriminated union.
- **game-theorist**: `Literal` types are P1 as a prerequisite for solution-concept dispatch.

**Synthesizer assessment**: This is a disagreement about justification, not about the recommendation itself. All three agents agree on the action and the priority. spec-compliance's argument is the most robust because it does not depend on future specs. The `Literal` constraint should be justified on FR-007 grounds and documented as such, with downstream benefits noted as secondary.

**Recommended resolution**: No action needed beyond noting that the canonical justification is FR-007 compliance ("enforce type constraints"), not downstream union needs.

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1 (Must Implement)

**P1-1: Atomic FR-003 type-set remediation** (traces to GT-2, GT-9, SE-8, SE-N1, SC-1, SC-6, SC-9, SC-N1)

A single coordinated work unit:
1. Amend FR-003 to add `map[string, string]`, `map[string, list[string]]`, and split `constraint_list` into `constraint_list` (flat, for coupled constraints) and `constraint_map` (per-player, for local constraints).
2. Update `VALID_FIELD_TYPES` constant in `game_forms.py` to include all new types.
3. Update every YAML schema field `type` declaration to use the correct type from the expanded set. At minimum: `strategies`, `decision_variables`, `objectives`, `local_constraints`, `follower_variables`, `follower_objectives`, `follower_constraints`.
4. Add an enforcement test that loads every YAML schema file, extracts all `type` values, and asserts membership in `VALID_FIELD_TYPES`.
5. Update YAML `description` fields for `constraint_map` entries to document the per-player variable-scoping convention.

**P1-2: `Literal` types on all `form` fields** (traces to SE-1, SC-4)

Change each model's `form` field from `form: str = "normal-form"` to `form: Literal["normal-form"] = "normal-form"` (and analogously for each game form). Justified by FR-007 ("enforce type constraints"). Prerequisite for any future discriminated union.

**P1-3: Package data resolution via `importlib.resources`** (traces to SE-3, SC-3)

Replace `_schema_dir()` filesystem traversal (`Path(__file__).parent.parent.parent`) with `importlib.resources` for runtime YAML file access. Add `[tool.setuptools.package-data]` configuration to `pyproject.toml`. If YAML files are relocated into the package directory, amend FR-001 paths in the same work unit. This fixes FR-011 non-compliance.

**P1-4: ParametricGame validation deduplication via mixin** (traces to GT-N1, SE-4, SC-5)

Extract the shared player-objective correspondence and player-decision-variable validation logic (currently duplicated across lines 137-163 and 186-215 of `game_forms.py`) into a `_GNEPStructureValidator` mixin or private base class. Both `GNEPGame` and `ParametricGame` use the mixin. Do not use direct `class ParametricGame(GNEPGame)` inheritance to avoid false `isinstance` contracts. Document that downstream dispatch should use the `form` discriminator, not `isinstance`.

**P1-5: Package name resolution (FR-010)** (traces to SC-2)

Resolve the mismatch between FR-010 (which says `conversus-schemas`) and `pyproject.toml` (which says `conversus`). This requires a project-owner decision: either rename the package in `pyproject.toml` to `conversus-schemas`, or amend FR-010 to match the actual package name `conversus`. The current state blocks downstream consumers who reference `pip install conversus-schemas`.

### P2 (Should Implement)

**P2-1: Discriminated union `GameForm` type** (traces to SE-2, SE-N2, GT-N2)

Create `GameForm = Annotated[Union[NormalFormGame, GNEPGame, ParametricGame, StackelbergGame], Discriminator("form")]`. Sequence this after the optimization-sense field is added (via spec 012a amendment or spec 013), so the union is built on mathematically complete models. Introduce via spec 013 or a spec 012 amendment, not as a retroactive P1 finding.

**P2-2: Optimization-sense field** (traces to GT-1, GT-N2, SE-N2)

File a spec 012a amendment adding `optimization_sense: dict[str, Literal["minimize", "maximize"]]` as a required companion to objectives on GNEP, Parametric, and Stackelberg models. Must land before or alongside the discriminated union. Use a top-level field (not a nested struct) to stay within the existing type vocabulary until the type system supports compound object types.

**P2-3: Stackelberg leader-not-in-followers validator** (traces to SE-6)

Add validation in `StackelbergGame.validate_structure` that asserts `self.leader not in self.followers`. A player cannot simultaneously commit first and respond to their own commitment. This is a semantic invariant of the Stackelberg form.

**P2-4: Mixed-strategy indicator on normal-form** (traces to GT-6)

Add `strategy_space: Literal["pure", "mixed"] = "pure"` to `NormalFormGame`. No structural change, no new validation logic. Communicates to downstream solvers whether to search the mixed extension of the strategy space.

**P2-5: Solution-concept metadata in mode-mapping** (traces to GT-5)

Add an optional `solution_concept` field to `ModeFormMapping` entries in `mode-mapping.yml`. Valid values per form (e.g., `nash`, `variational-equilibrium`, `strong-stackelberg`). Keeps game forms as pure structural descriptions while the mode mapping carries operational intent.

**P2-6: Minimum player cardinality validation** (traces to GT-N3, SE-5)

Add `len(players) >= 2` for NormalFormGame and GNEPGame. Add `len(followers) >= 1` for StackelbergGame. A one-player game is a decision problem, not a game.

**P2-7: Non-empty player list validation** (traces to SE-5)

If P2-6 is deferred, at minimum add `len(players) >= 1` as a floor. An empty player list produces cryptic downstream validator errors.

**P2-8: FR-011/FR-001 coordination documentation** (traces to SC-N3)

If the package data fix (P1-3) requires relocating YAML files, document and execute the FR-001 path amendment in the same work unit.

### P3 (Consider Implementing)

**P3-1: Prisoner's-dilemma mode-mapping clarification** (traces to GT-4)

Strengthen the mode-mapping note for `prisoners-dilemma` to explicitly state: "The conversus prisoners-dilemma mode uses PD-like payoff incentives (T > R > P > S ordering) within a GNEP structure with coupled constraints; this differs from the classical 2x2 prisoner's dilemma which is a normal-form game." Alternatively, investigate whether the conversus PD mode actually requires coupled constraints. This is a spec-author decision.

**P3-2: `frozen=True` on all game form models** (traces to SE-10)

Add `model_config = ConfigDict(frozen=True)` to prevent post-validation mutation. Low urgency now; elevate to P2 when spec 016 introduces multi-consumer game form instance flows.

**P3-3: Stackelberg non-empty leader_variables validator** (traces to SE-7)

Add validation that `leader_variables` is non-empty. A Stackelberg leader with no decision variables is a degenerate case. Acceptable as a warning rather than a hard error.

**P3-4: Local-constraint generality note** (traces to GT-10)

Add a note to `gnep.yml` clarifying: "In the GNEP formulation used here, local constraints depend only on the owning player's variables. Constraints involving other players' variables must be placed in coupled_constraints."

**P3-5: Dispatch convention documentation** (traces to SE-N3)

Add a module-level docstring or comment in `game_forms.py` establishing that downstream consumers must dispatch on the `form` field, not `isinstance`. Prevents solver plugin authors from reintroducing the polymorphism problem the mixin design was built to avoid.

**P3-6: Negative tests for `form` field mismatch** (traces to SC-8)

Add tests verifying that `NormalFormGame(form="gnep", ...)` is rejected after Literal types are implemented.

**P3-7: SC-001 test comment** (traces to SC-7)

Add a comment in the test explaining why `data["example"]` is validated rather than the entire YAML file, documenting the intentional deviation from SC-001's literal wording.

**P3-8: Export `ModeMapping` and `ModeFormMapping` from `__init__.py`** (traces to SE-9, SC-10)

Add to `__all__` for downstream type-hinting ergonomics.

**P3-9: Variable bounds/domain fields** (traces to GT-3)

Deferred to spec 012a or spec 017. The mathematical argument stands (variable bounds define feasible set geometry and affect algorithm selection), but the current spec does not require this level of structural detail.

**P3-10: Bilevel structure in Stackelberg** (traces to GT-7)

Deferred to spec 017 or 018 (Stackelberg solver plugin). For spec 012, the flat schema with role separation and a documentation note about the leader's anticipation assumption is sufficient. The bilevel nesting captures computation structure, which is solver-adjacent.

---

## Key Concessions

1. **game-theorist conceded on procedural framing** (Phase 3 revision): "My original review was mathematically sound in its diagnoses but procedurally overreaching in several priority assignments." Accepted that optimization sense, variable bounds, and PD mapping all require spec amendments before implementation -- they are spec gaps, not implementation bugs.

2. **game-theorist withdrew the information-structure field** (Phase 3): Accepted schema-engineer's DRY argument that a field whose value is fully determined by the `form` discriminator adds no information. Acknowledged the future-extensibility argument was speculative and violated YAGNI.

3. **spec-compliance withdrew the bidirectional framing of FR-003** (Phase 3): Originally presented the type mismatch as "expand type set OR fix YAML." After game-theorist's mathematical argument that simplifying Pydantic models would destroy asymmetric game support, withdrew the "or" framing and adopted the unidirectional position (expand the type set only).

4. **schema-engineer withdrew direct ParametricGame inheritance** (Phase 3): Originally proposed `class ParametricGame(GNEPGame)` for DRY and `isinstance` polymorphism. After game-theorist's mathematical argument about false subtyping and spec-compliance's Pydantic MRO concern, changed to mixin extraction -- the most significant implementation approach change in the deliberation.

5. **schema-engineer downgraded discriminated union from P1 to P2** (Phase 3): Accepted spec-compliance's argument that no FR requires a union type, and game-theorist's temporal ordering constraint relative to the optimization-sense field.

6. **game-theorist moved solution-concept field from game forms to mode-mapping** (Phase 3): Accepted schema-engineer's argument that solution concepts mix definitional data with operational intent. Credited schema-engineer for the alternative architectural placement.

7. **schema-engineer conceded on `VALID_FIELD_TYPES` enforcement** (Phase 3): Originally treated the YAML-Pydantic type mismatch as a YAML-only fix. After spec-compliance's cross-review identified that `VALID_FIELD_TYPES` is dead code, expanded the recommendation to include enforcement wiring as part of the atomic remediation.

8. **game-theorist accepted bilevel Stackelberg nesting deferral** (Phase 3): Conceded that the flat schema captures "vocabulary" (leader, follower, objectives) while bilevel nesting captures "computation structure" (outer optimization over inner best-response), which is solver-adjacent and belongs in spec 017/018.
