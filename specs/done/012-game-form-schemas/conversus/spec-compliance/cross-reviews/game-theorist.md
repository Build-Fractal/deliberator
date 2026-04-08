# Cross-Review of game-theorist's Review

**Cross-reviewer**: spec-compliance
**Target review**: game-theorist review of 012-game-form-schemas
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: Prisoner's Dilemma Mapping -- Mathematical Purity vs. Spec Compliance

game-theorist (Off-Base Assumptions, para 1) argues that mapping `prisoners-dilemma` to GNEP is "mathematically imprecise" because the classical prisoner's dilemma is a 2x2 normal-form game with no coupled constraints, and recommends either remapping to `normal-form` or renaming the mode.

From a spec compliance perspective, this recommendation is at odds with FR-004, which explicitly mandates `prisoners-dilemma -> gnep`. The spec text (Section 2, GNEP Form) also deliberately names prisoners-dilemma as a GNEP use case: "cooperative, prisoners-dilemma, and red-blue modes. Most real deliberations have coupled constraints." The implementation correctly follows the spec.

game-theorist's mathematical objection is legitimate in the abstract, but if the fix is to change the mapping, it requires a spec amendment to FR-004, not an implementation change. My own review (Alignment, FR-004) confirmed the mapping as fully compliant. The dangerous contradiction is this: game-theorist's Recommendation 4 (P2) advises changing the mode mapping, which would *break* FR-004 compliance if done without a corresponding spec revision. The right sequencing is: propose a spec amendment first, then change the implementation. Treating this as an implementation fix would introduce a spec violation.

### DC-2: Optimization Sense Field -- Severity Assessment Divergence

game-theorist (Missed Opportunities, para 1; Recommendation 1, P1) identifies the missing `sense: minimize | maximize` field as the single most important recommendation, rating it P1. My own review does not flag this because the spec's FR-003 closed type set does not include a structured objective type, and FR-002/FR-007 do not require the schema to distinguish optimization sense from expression content. The objectives are typed as `function` (FR-003) and stored as strings; this is what the spec asks for.

The contradiction is about severity and scope. game-theorist is right that downstream solver specs (017-019) will need to know the sense. But from a compliance standpoint, adding a structured `Objective` type (with `sense` and `expression` subfields) would require expanding FR-003's closed type set, modifying the YAML schema structure beyond what FR-002 specifies, and changing the Pydantic model field types. This is a spec-level change, not an implementation gap. Rating it P1 against the current spec is overweighted; it should be P1 against the *next spec revision* or filed as a requirement for spec 013+ where solver integration begins.

### DC-3: Variable Bounds/Domains -- Scope Creep Beyond FR Boundary

game-theorist (Recommendation 3, P1) calls for adding `domain`, `lower`, and `upper` fields to decision variable definitions, arguing that variable bounds are structurally distinct from constraints in mathematical programming.

My review does not raise this because the spec explicitly scopes this as a schema-only deliverable with no solver logic (Section 1: "schemas describe the mathematical structure of games -- what players exist, what strategies they have, what payoffs result -- without any solver logic"; Section 5: "Must NOT include solver logic"). Variable bounds and domains are solver-relevant metadata; the choice between box constraints and general constraints is an algorithm-selection concern, which the spec deliberately defers to plugin specs (017-019).

The contradiction: game-theorist rates this P1 (must-fix), but implementing it would add fields that serve solver selection rather than game structure description. None of the FRs require bound or domain information. This is a forward-looking enhancement, not a compliance gap. If prioritized as P1, it risks scope creep that delays the current spec's completion without satisfying any existing requirement.

---

## Tensions

### T-1: Bilevel Structure in Stackelberg -- Degree of Structural Explicitness

game-theorist (Recommendation 7, P2) argues the Stackelberg schema should structurally represent the bilevel program (nesting the follower problem as an inner optimization problem), because without it the schema is "indistinguishable from a sequential game without anticipation."

My review does not flag this. The spec (Section 2, Stackelberg Form) describes the bilevel structure in prose -- "Leader anticipates follower responses when choosing" -- and the YAML schema's `description` field captures this intent. The Pydantic model validates the structural invariants the spec requires (follower-objective bijection, follower-variable bijection). FR-007 requires enforcement of "required fields, type constraints, and structural invariants," and the stated invariants are enforced.

The tension: game-theorist is correct that mathematical distinctness is lost in the flat schema structure. But the spec does not define bilevel nesting as a required structural invariant. This is a genuine gap between mathematical completeness and spec compliance. The resolution likely belongs in a spec amendment or in spec 017 (solver plugins), where the bilevel structure becomes operationally necessary.

### T-2: Mixed Strategy Support -- Schema Expressiveness vs. Spec Scope

game-theorist (Recommendation 6, P2) wants a `strategy_space: pure | mixed` field on normal-form games, citing Nash's existence theorem. My review does not raise this because the spec (Section 2, Normal Form) explicitly defines strategy sets as "per-player, finite" and payoff structure as a tensor over joint strategy profiles. The spec describes pure strategies and does not mention mixed strategies.

The tension: game-theorist's point is mathematically well-founded -- mixed strategies are central to normal-form game theory. But the conversus use case for normal-form (winner-take-all mode, per Section 2) involves discrete alternative selection, where pure strategies are the natural representation. Adding mixed-strategy support addresses mathematical completeness at the cost of schema complexity that no current mode requires. This is a legitimate design tension that should be resolved in the spec revision process, not unilaterally in the implementation.

### T-3: Solution Concept Field -- Schema Intent vs. Schema Structure

game-theorist (Recommendation 5, P2) proposes an optional `solution_concept` field per game form (e.g., `nash`, `variational-equilibrium`, `strong-stackelberg`). My review does not raise this. The spec (Section 1) explicitly separates structure from computation: "schemas describe the mathematical structure of games... without any solver logic." A solution concept field straddles this boundary -- it carries intent about how to solve the game, which is adjacent to solver logic.

The tension: game-theorist argues this eliminates "implicit coupling that the schema layer was meant to eliminate." My compliance view is that the mode-to-form mapping (FR-004) already serves as the intent carrier, and the solver specs (017-019) should own solution concept selection based on mode + form. Adding it to the schema is not wrong, but it is not required by any FR and shifts responsibility from the solver layer to the schema layer.

### T-4: N-Player Normal Form Type Declaration

game-theorist (Missed Opportunities, para 8) and my review (Missed Opportunities, FR-003 type mismatch) both identify the `strategies: type: list[string]` declaration in normal-form.yml as incorrect, since the actual data structure is `dict[str, list[str]]`. We agree on the finding but differ on framing.

game-theorist frames this as a mathematical ambiguity ("if someone reads the YAML schema literally, they would think all players share a single strategy set (symmetric game)"). My review frames it as a compliance gap against FR-003's closed type set, which does not include `dict`-like types. The tension is whether the fix is to expand the type set (my recommendation) or to change the type declaration without expanding the set (which would require inventing a non-standard type name). Both paths require a spec amendment to FR-003.

### T-5: Information Structure Field -- Useful Enhancement vs. Redundant Metadata

game-theorist (Recommendation 8, P3) proposes an `information_structure` field. game-theorist acknowledges this is "redundant with the form itself" for Stackelberg and correctly rates it P3. My review does not raise this. I agree with the low priority and note that since the game form name already implies the information structure (normal-form = simultaneous, Stackelberg = sequential), this is metadata duplication. The tension is minimal but worth noting: if additional game forms are added in future specs (e.g., extensive-form, Bayesian), the implicit convention would indeed break down, making game-theorist's forward-looking concern valid at a longer time horizon.

---

## Safe Agreements

### SA-1: FR-003 Type Set Is Insufficient for Actual Data Structures

game-theorist (Recommendation 9, P3; Recommendation 2, P1) and my review (Off-Base Assumptions, para 1; Recommendation 1, P1) converge completely on this finding. The YAML schemas declare `type: list[string]` for fields that are actually `dict[str, list[str]]` or `dict[str, str]` in both the examples and the Pydantic models. At least 6 fields across 4 schemas have this mismatch.

Both reviews agree this must be fixed. game-theorist recommends fixing the YAML type declarations; my review recommends expanding the FR-003 type set and then fixing the declarations. Both approaches arrive at the same destination: the YAML schemas must be self-consistent with their own examples and with the Pydantic models.

### SA-2: `ParametricGame` Should Inherit from `GNEPGame`

game-theorist (Alignment, para 5) notes the parametric game "correctly models" the GNEP extension. My review (Off-Base Assumptions, para 2) flags that the implementation does not actually inherit from `GNEPGame` -- it duplicates all validation logic (lines 186-209 mirror lines 137-162). The spec says "Inherits all GNEP fields," which implies structural inheritance.

Both reviews effectively agree that the current duplication is a defect: game-theorist's implicit endorsement of the inheritance relationship and my explicit call for `ParametricGame` to extend `GNEPGame` (Recommendation 5, P2) point in the same direction. Validation drift between the two models is an avoidable correctness risk.

### SA-3: Package Deployment Gaps (FR-010 and FR-011)

My review (Recommendations 2-3, P1) identifies the package name mismatch (`conversus` vs. `conversus-schemas`) and the missing package data configuration as compliance failures against FR-010 and FR-011. game-theorist does not address these because they fall outside the game theory domain.

These are not contested findings. They are straightforward compliance gaps that both reviews can agree need resolution regardless of the mathematical concerns. I include this as a safe agreement because game-theorist's silence on packaging does not constitute disagreement -- it simply falls outside that reviewer's scope.

---

### Summary

game-theorist's review is mathematically thorough and identifies genuine gaps that will matter for downstream specs 013-020. The dangerous contradictions arise primarily from scope: several P1 recommendations (optimization sense, variable bounds, prisoner's dilemma remapping) would require spec amendments to implement correctly, and treating them as implementation fixes risks introducing new compliance violations. The tensions reflect a healthy design debate between mathematical completeness and spec-scoped minimalism. The safe agreements on FR-003 type mismatches and `ParametricGame` inheritance are high-confidence shared findings that can be acted on immediately.
