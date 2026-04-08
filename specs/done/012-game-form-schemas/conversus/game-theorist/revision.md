# Game-Theorist Revision: 012-game-form-schemas

**Reviewer**: game-theorist
**Revision iteration**: 1
**Date**: 2026-03-22

---

### Recommendation Dispositions

**Rec 1 — Add optimization-sense field (was P1): MODIFIED**

Both cross-reviewers challenged the priority, not the substance. schema-engineer (DC-1) correctly identified that introducing a structured `Objective` type conflicts with the current FR-003 closed type set, and that delivering the sense field without simultaneously expanding the type vocabulary would widen the YAML-Pydantic divergence. spec-compliance (DC-2) correctly noted that the current spec does not require optimization sense, so rating this P1 against the existing spec is overweighted — it should be P1 against a spec amendment or for specs 013+.

I accept both critiques. The mathematical necessity is unchanged — an objective without a sense is genuinely ambiguous, and every standard modeling framework (AMPL, GAMS, Pyomo) separates sense from expression. But I was wrong to frame this as a P1 implementation fix against the current spec. It is a P1 spec amendment that must be coordinated with FR-003 type-set expansion.

**Modified recommendation**: File a spec amendment adding `sense: minimize | maximize` as a required companion to every objective expression, and simultaneously expand FR-003 to include a structured objective type (or use schema-engineer's alternative of a parallel `optimization_sense: dict[str, Literal["minimize", "maximize"]]` top-level field that stays within the existing type vocabulary). Priority: P1 for the spec amendment; implementation follows the amendment. schema-engineer's alternative of a separate top-level field is a pragmatic compromise I endorse if the nested-struct approach is deferred.

---

**Rec 2 — Fix strategies type declaration in normal-form YAML (was P1): SURVIVING**

Both cross-reviewers independently confirmed this finding (schema-engineer SA-1, spec-compliance SA-1). All three reviews agree: the YAML declares `type: list[string]` but the actual structure is `dict[str, list[str]]`. The mathematical consequence I identified — that `list[string]` implies a symmetric game, which is a stronger condition — was not contested. The only question is whether the fix requires a spec amendment to FR-003 (spec-compliance's framing) or can be done directly (my framing).

I concede that spec-compliance is right: since `dict[string, list[string]]` is not in the current FR-003 closed type set, this fix does require expanding FR-003. But the direction is non-negotiable, as I noted in my cross-review of spec-compliance (DC-1): the Pydantic model has the correct mathematical structure and the YAML declaration has the wrong one. Retrograding the Pydantic model to match the YAML would destroy asymmetric game support. Priority remains P1. The implementation path is: amend FR-003, then fix the YAML declarations.

---

**Rec 3 — Add variable bounds/domain fields (was P1): MODIFIED**

spec-compliance (DC-3) argued this is scope creep beyond the current FRs, since variable bounds serve solver selection rather than game structure description. schema-engineer (T-2) noted that adding nested variable-bound structures would further widen the YAML-Pydantic gap and amplified the type-system debt concern.

I partially accept the scope-creep critique. Variable bounds are mathematically part of the problem formulation (they define the feasible region geometry), not merely solver metadata — this is where spec-compliance's framing is imprecise. In optimization theory, $x \in [0,1]$ is a constraint on the feasible set, structurally equivalent to but computationally distinct from $x - 1 \leq 0, -x \leq 0$. However, I accept that the current spec does not require this level of structural detail and that adding it now would compound the type-system debt that schema-engineer flagged.

**Modified recommendation**: Downgrade from P1 to P2. File as a forward-looking enhancement for spec 012a or spec 017 (where solver algorithm selection becomes operational). The mathematical argument stands but the sequencing argument against it is persuasive: fix the type system alignment first (schema-engineer's position), then add richer types.

---

**Rec 4 — Correct prisoner's-dilemma mode mapping (was P2): MODIFIED**

spec-compliance (DC-1) made the strongest counter-argument: the mapping `prisoners-dilemma -> gnep` is explicitly mandated by FR-004, so changing the implementation without a spec amendment would *introduce* a compliance violation rather than fix one. schema-engineer (DC-3) added that the spec prose justifies the GNEP mapping by referencing coupled constraints in the conversus PD mode.

I accept that my original recommendation was procedurally wrong. Changing the implementation without amending the spec would break FR-004. However, the mathematical objection survives scrutiny: the classical prisoner's dilemma is a 2x2 normal-form game with no coupled constraints. If the conversus PD mode genuinely has coupled constraints, then mapping it to GNEP is operationally correct but the mode name is misleading — it is not modeling a prisoner's dilemma in the game-theoretic sense. This is a naming/documentation issue, not an implementation bug.

**Modified recommendation**: Do not change the implementation. Instead, the spec amendment should either (a) strengthen the mode-mapping note to explicitly state: "The conversus prisoners-dilemma mode uses PD-like payoff incentives (T > R > P > S ordering) within a GNEP structure with coupled constraints; this differs from the classical 2x2 prisoner's dilemma which is a normal-form game," or (b) investigate whether the conversus PD mode actually requires coupled constraints, and if not, amend FR-004 to map it to normal-form. This is a domain decision for the spec author, not an implementation change. Downgrade from P2 to P3 for immediate action; flag for spec revision discussion.

---

**Rec 5 — Add solution-concept field (was P2): MODIFIED**

Both cross-reviewers pushed back on this, though from different angles. schema-engineer (T-3) argued that solution concepts mix definitional data with operational intent, and suggested placing them in the mode-mapping layer rather than game-form schemas. spec-compliance (T-3) argued it straddles the boundary between structure and computation that the spec explicitly separates.

These arguments are partially persuasive. I acknowledge that a `solution_concept` field on the game form itself blurs the schema/solver boundary. However, schema-engineer's alternative — placing solution concepts in the mode-mapping layer — is mathematically sound and actually more elegant. The mode mapping already carries `note` fields; formalizing them into `solution_concept` preserves the schema purity while carrying the intent.

**Modified recommendation**: Instead of adding `solution_concept` to each game form schema, add an optional `solution_concept` field to `ModeFormMapping` entries in mode-mapping.yml. This keeps game forms as pure structural descriptions while the mode mapping carries the operational intent. The mathematical content is the same; the architectural placement is better. Credit to schema-engineer for this suggestion.

---

**Rec 6 — Add mixed-strategy indicator to normal form (was P2): SURVIVING**

schema-engineer (T-1) acknowledged the mathematical motivation and proposed a clean implementation (`strategy_space: Literal["pure", "mixed"] = "pure"` with a descriptive annotation). spec-compliance (T-2) noted the conversus winner-take-all use case involves discrete alternative selection where pure strategies are natural, and that no current mode requires mixed strategies.

I accept spec-compliance's point about current mode requirements but maintain that this is a low-cost, high-value addition. As schema-engineer confirmed, it is a single Literal field with no structural change and no new validation logic. The implementation cost is trivial. The mathematical benefit is significant: without it, any downstream solver attempting to find Nash equilibria in normal-form games must decide unilaterally whether to search the mixed extension of the strategy space.

Priority remains P2. This should be included in any spec revision that touches the normal-form schema, as it requires no type-set expansion and no structural change.

---

**Rec 7 — Model bilevel structure in Stackelberg (was P2): MODIFIED**

schema-engineer (DC-4) made a compelling sequencing argument: implementing validators on the flat schema and then restructuring for bilevel nesting wastes validator work. Both schema-engineer and spec-compliance (T-1) agreed the mathematical argument for bilevel nesting is sound but questioned whether it belongs in spec 012 or in spec 017/018 where the structure becomes operationally necessary.

I accept the deferral argument. The bilevel structure is mathematically essential for correct Stackelberg equilibrium computation, but the current spec scopes itself as "mathematical vocabulary" — and the flat schema with role separation does capture the vocabulary (leader, follower, objectives, constraints). The bilevel nesting captures the *computation structure* (outer optimization over inner best-response), which is arguably solver-adjacent.

**Modified recommendation**: Defer bilevel nesting to spec 017 or 018 (Stackelberg solver plugin). For spec 012, add schema-engineer's validators (leader-not-in-followers disjointness, non-empty leader_variables) to the current flat structure, and add a `description` or `note` field documenting the bilevel anticipation assumption. This preserves the mathematical intent without restructuring. Downgrade from P2 to P3 for spec 012; flag as P1 for the Stackelberg solver spec.

---

**Rec 8 — Add information-structure field (was P3): WITHDRAWN**

schema-engineer (T-4) made the decisive argument: since `form == "normal-form"` always implies simultaneous and `form == "stackelberg"` always implies sequential, the field adds no information and violates DRY. I acknowledged this in my original review ("redundant with the form itself") but kept the recommendation for future extensibility.

On reflection, the future-extensibility argument is speculative and violates YAGNI. If extensive-form or Bayesian games are added in future specs, they will bring their own information-structure requirements that a simple `simultaneous | sequential | partial` enum would not capture anyway (extensive-form games need full game trees, not a metadata flag). The recommendation was well-intentioned but premature. Withdrawn.

---

**Rec 9 — Expand closed type set for schema correctness (was P3): SURVIVING**

All three reviews converge on this. The FR-003 type set cannot express the types actually in use. I upgrade this from P3 to P2 to align with its role as a prerequisite for multiple other fixes (Rec 1, Rec 2, and several schema-engineer recommendations). The direction — expand the type set to include mapping types — is agreed by all reviewers.

---

**Rec 10 — Add local-constraint generality note (was P3): SURVIVING**

No cross-reviewer contested this. My cross-review of spec-compliance (DC-2) noted that the choice of data structure (per-player mapping vs. flat list) for local constraints structurally encodes the variable-scoping assumption, and that the type-declaration fix and the clarifying note should be a single coordinated change. This remains a P3 documentation item with no detractors.

---

### New Recommendations

**New-1: ParametricGame should share GNEP validation logic (source: schema-engineer DC-2, spec-compliance SA-2)**

Both cross-reviewers flagged that `ParametricGame` duplicates all GNEP validation logic (lines 186-209 mirror lines 137-162). My original review was silent on this, which was a blind spot. The mathematical relationship is clear: a parametric game is a GNEP parameterized by exogenous variables. Any invariant that holds for GNEPs must hold for parametric games.

However, in my cross-review of schema-engineer (DC-1), I cautioned that naive Pydantic inheritance (`class ParametricGame(GNEPGame)`) creates a false `isinstance` contract — solver plugins might treat parametric games as plain GNEPs and ignore the parameter dependence. The resolution I proposed there stands: either use inheritance with mandatory `form` Literal discriminator enforcement (so dispatch always checks `form`, never `isinstance`), or extract a `_GNEPValidationMixin` / shared validation function that both models call without establishing an is-a relationship. Priority: P2.

**New-2: Coordinate optimization-sense addition with discriminated union sequencing (source: my cross-review of schema-engineer DC-2)**

schema-engineer's discriminated union `GameForm = Annotated[Union[...], Discriminator("form")]` is a high-value addition. But if it ships before the optimization-sense field is added, downstream consumers will adopt an API for producing mathematically incomplete game instances. Adding `sense` later changes the objective type from `str` to a structured object — a breaking change for every consumer that adopted the union.

Recommendation: if the discriminated union is implemented in this spec cycle, coordinate it with the optimization-sense spec amendment so the union is built on mathematically complete models from day one. If the union ships first, document the upcoming breaking change prominently. Priority: P2.

**New-3: Validate minimum player cardinality per game form (source: my cross-review of schema-engineer DC-3)**

schema-engineer proposed a non-empty player list validator, which is correct defensive programming. I extended this in my cross-review: a normal-form game with one player is technically a decision problem, not a game, and a one-player "game" will flow into multi-agent equilibrium solvers that assume N >= 2. A `min_players` check (2 for normal-form and GNEP, 1-leader + 1-follower for Stackelberg) would catch this semantically misleading case. Priority: P3.

---

### Position Summary

After reading the cross-reviews, I find my original review was mathematically sound in its diagnoses but procedurally overreaching in several priority assignments. The most important correction is distinguishing between implementation defects (fixable now) and spec gaps (requiring amendments before implementation). Recommendations 1, 3, and 4 were all framed as implementation fixes when they are actually spec-level changes. spec-compliance's insistence on this distinction is procedurally correct and I accept it fully. The optimization-sense field, variable bounds, and prisoner's-dilemma mapping all require FR amendments before the code should change.

The cross-reviews also surfaced a genuine design tension I had not articulated: how much mathematical structure belongs in a schema-only spec versus in the solver specs that consume it. My original review implicitly assumed the schemas should be mathematically complete — capturing enough structure that downstream solvers need not re-derive information. Both cross-reviewers pushed back with a minimalist position: the schemas should capture the vocabulary (players, strategies, objectives, constraints) and leave structural details (optimization sense, variable bounds, bilevel nesting) to the specs where they become operationally necessary. I now accept a phased approach: the current spec establishes vocabulary; a spec 012a amendment adds the mathematical metadata (sense, bounds, solution concepts) before specs 017-019 consume the schemas. The key constraint is that the amendment must land before the solver specs, not after — retrofitting mathematical structure into schemas that solvers have already adopted is far more costly than getting it right upfront.

Three items from my original review survive without modification: the strategies type-declaration fix (Rec 2), the mixed-strategy indicator (Rec 6), and the local-constraint generality note (Rec 10). These are uncontested, low-cost, and mathematically well-motivated. One item is withdrawn entirely (Rec 8, information structure), because the DRY argument against it is stronger than the extensibility argument for it. The remaining items are modified in priority, scope, or architectural placement, but the underlying mathematical reasoning in each case has not been refuted — only the sequencing and procedural framing needed correction.
