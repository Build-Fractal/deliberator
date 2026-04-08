# Cross-Review: spec-compliance reviewing game-theorist

**Spec**: 025-game-form-expansion
**Reviewer**: spec-compliance
**Subject**: game-theorist Phase 1 review

---

## Verified Claims

### 1. Shapley axiom verification is authoritative

The game-theorist's four-axiom analysis (efficiency, symmetry, null player, additivity) provides definitive mathematical validation. Each axiom is mapped to a specific test case in the suite. The observation that additivity is inherent to the linear formula and needs no separate test is correct -- the Shapley value is the unique function satisfying all four axioms, and three are tested directly.

### 2. Potential game diagnostic characterization is correct

The reference to Monderer & Shapley (1996) and the cross-partial symmetry condition is the standard result. The game-theorist correctly identifies that this is the discrete version of the Jacobian symmetry condition for potential games.

### 3. Complexity guard rationale is sound

The N <= 10 cap with O(N * 2^N) justification is appropriate. At N=10, the computation involves ~10,240 iterations -- fast. At N=15, ~491,520 iterations. At N=20, ~20 million. The cap at 10 is conservative but reasonable for an exact computation.

---

## Disagreements

### 1. Finding #1 severity: I agree with HIGH but for different reasons

The game-theorist rates the 2-player limitation as HIGH based on mathematical generality. From a spec-compliance perspective, I rate it HIGH for a more specific reason: **FR-004 requires the diagnostic to be "a check applied to existing game forms."** The word "existing" refers to the forms defined before spec 025 (normal-form, gnep, parametric, stackelberg). The diagnostic is only applicable to NormalFormGame with 2 players.

This means:
- Normal-form 2-player: supported
- Normal-form 3+-player: NOT supported (function takes bimatrix, not N-dimensional tensor)
- GNEP: structurally inapplicable (no payoff matrix)
- Parametric: structurally inapplicable
- Stackelberg: structurally inapplicable

The diagnostic applies to a subset of one of four existing forms. This is a scope gap relative to the spec language, even though the 2-player bimatrix case is the most practically useful one.

**My recommendation**: Document the scope restriction in both the function docstring and the spec. Amend spec section 2.1 to say "a check applied to 2-player normal-form games" rather than "existing game forms."

### 2. Finding #5 (prior tolerance 1e-6) -- I would upgrade to Low

The game-theorist rates the tight tolerance as INFO. From a compliance standpoint, if a downstream component normalizes a Dirichlet-sampled prior and the sum is 1.0 + 2e-6 due to float accumulation, the model will reject a statistically valid prior. This is an interoperability concern.

The tolerance check `abs(total - 1.0) > 1e-6` should use a configurable or more forgiving threshold. I would rate this LOW rather than INFO because it could cause confusion in automated pipelines.

---

## Additions

### FR-005 vs. solver architecture

The game-theorist's review does not explicitly assess FR-005 compliance. The solvers.py module uses only `itertools` and `math` from stdlib. This satisfies FR-005 ("MUST work with pure Python + scipy only") and in fact exceeds it by not requiring scipy at all.

However, the solver module's docstring says "Pure Python solver functions for Tier 1 game forms." If a future contributor adds a Tier 1 solver that imports scipy (e.g., for Rosenthal potential optimization in congestion games), this is permitted by FR-005 but would invalidate the docstring's "pure Python" claim. The docstring should say "Pure Python + scipy solver functions" to match the FR-005 allowance.

### Missing test: is_potential_game with larger matrices

The test suite covers 2x2 games exclusively (coordination 2x2, PD 2x2, matching pennies 2x2). The function supports arbitrary MxN matrices for 2-player games. A test with a 3x3 or 3x2 game would verify that the nested loop over all 2x2 sub-games works correctly for non-square matrices.
