# Cross-Review: spec-compliance reviewing game-theorist

**Spec**: 025-game-form-expansion

---

## Agreement

The game-theorist's mathematical review is authoritative and well-supported. I agree with:

- Shapley computation correctness (verified against the standard formula)
- Potential game diagnostic correctness for 2-player games
- The concern about BayesianGame prior key validation being missing

## Disagreements

### 1. Concern #1 severity should be higher (Medium -> High)

The game-theorist rates the 2-player limitation of `is_potential_game()` as Medium. From a spec-compliance perspective, I believe this is **High** because:

- FR-004 says "Potential game diagnostic MUST be implemented as a check function"
- Section 2.1 says "A check applied to existing game forms"
- "Existing game forms" include GNEP and parametric games, which are N-player

If the diagnostic only works on 2-player normal-form games, it cannot fulfill its stated purpose of checking "existing game forms" for potential game structure. The implementation needs either:
(a) Generalization to N-player games, or
(b) Clear documentation that the diagnostic is restricted to 2-player bimatrix games

I recommend (b) as the pragmatic path -- the 2-player case covers the most common use case (coordination/prisoners-dilemma) and N-player potential game detection is a research-level problem.

### 2. MechanismDesignGame sparseness (Agree with Low)

The game-theorist's Low rating for MechanismDesignGame sparseness is appropriate. Tier 2 models are schemas for future solver integration. Having the type discriminator and enum fields now enables mode mapping and template routing without premature field specification.

## Additions

The game-theorist did not assess whether the solver module (`solvers.py`) violates FR-005 (Tier 1 must work with pure Python + scipy only). The current implementation uses only stdlib (`itertools`, `math`), which satisfies FR-005. The module docstring claims "pure Python only" which is accurate. No scipy dependency exists despite FR-005 allowing it.
