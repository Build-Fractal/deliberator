# Feature Specification: nashopt Solver Integration

**Feature ID**: `021-nashopt-integration`
**Created**: 2026-03-25
**Status**: Draft
**Depends On**: `017-equilibrium-scorer` (heuristic scorer to upgrade), `015-feature-extraction` (feature vectors as solver input)
**Origin**: Review finding — spec 017 implements heuristic fallback only. This spec delivers the real solver.

---

## 1. Feature Summary

Replace the heuristic equilibrium scoring in `conversus-nashopt` with actual Nash equilibrium computation using the `nashopt` library (JAX-based). The heuristic remains as a zero-dependency fallback; this spec adds the premium path that runs when `nashopt` and `jax` are installed.

**What changes**: `conversus/plugins/nashopt/scorer.py` gains a real solver path. New `conversus/plugins/nashopt/solver.py` wraps nashopt API. Per-mode payoff matrices are constructed from feature vectors and fed to `nashopt.check_equilibrium()`.

**What does not change**: Plugin interface. Hook points. Heuristic fallback. Feature extraction. Output format (score 0.0-1.0 + analysis).

---

## 2. Technical Approach

### nashopt API Surface

```python
import nashopt

# Normal-form equilibrium check
result = nashopt.check_equilibrium(
    payoff_matrix,      # np.ndarray (N x N x actions)
    strategy_profile,   # Current agent positions as strategy vectors
)
# result.is_equilibrium: bool
# result.distance: float (0.0 = perfect equilibrium)
# result.best_responses: dict[agent, action]
```

### Per-Mode Payoff Matrix Construction

| Mode | Matrix Structure | Source |
|------|-----------------|--------|
| cooperative | N×N agreement/dispute matrix | Agreement matrix from features + dispute counts |
| winner-take-all | N×1 ranking payoff vector | Score differentials from features |
| prisoners-dilemma | N×N territory overlap matrix | Territory claims × overreach penalties |
| red-blue | 2×K severity/mitigation matrix | Severity vectors × mitigation rates |

### Scoring Formula

```
equilibrium_score = 1.0 - nashopt_result.distance
```

Where `distance` is normalized to [0.0, 1.0] by the maximum possible distance for the game form.

---

## 3. Functional Requirements

- **FR-001**: When `nashopt` and `jax` are importable, the scorer MUST use `nashopt.check_equilibrium()` instead of the heuristic path.
- **FR-002**: When `nashopt` is not importable, the scorer MUST fall back to the existing heuristic path with no behavioral change.
- **FR-003**: The solver MUST construct per-mode payoff matrices from `FeatureSet` data using documented formulas.
- **FR-004**: The solver MUST normalize the equilibrium distance to a 0.0-1.0 score compatible with the existing output format.
- **FR-005**: The solver MUST report which agents are NOT at their best response (i.e., which agents could improve their position by changing strategy).
- **FR-006**: The solver MUST handle degenerate cases: single-agent games, zero-variance payoff matrices, all agents at equilibrium.
- **FR-007**: Solver execution MUST be capped at a configurable timeout (default 30s). If exceeded, fall back to heuristic with a warning.
- **FR-008**: The `PluginResult.data` dict MUST include `solver: "nashopt"` (or `solver: "heuristic"`) so consumers know which path ran.

---

## 4. Success Criteria

- **SC-001**: Given a cooperative deliberation where all agents converge, the nashopt solver produces a score >= 0.9.
- **SC-002**: Given a deliberation with 3+ unresolved disputes, the solver produces a score < 0.5.
- **SC-003**: With nashopt uninstalled, behavior is identical to the current heuristic implementation.
- **SC-004**: Solver timeout produces a heuristic fallback score, not an error.

---

## 5. Dependencies

- `nashopt` — Nash equilibrium solver (JAX-based)
- `jax` — numerical computation (transitive via nashopt)
- Both are optional runtime dependencies, not package requirements.

---

## 6. Constraints

- Must NOT add nashopt/jax to core package requirements. They are optional.
- Must NOT change the Plugin interface or output format.
- Must NOT break the heuristic fallback path.
- The solver wrapper (`solver.py`) must be independently testable with mock payoff matrices.

---

## Amendment: Matrix Shape Clarification (spec 038, RE-2)

**Date**: 2026-04-01

The Section 2 table states that winner-take-all mode produces an "N×1 ranking payoff vector." The code in `solver.py::_build_wta_matrix()` matches this — it returns N rows of 1 element each.

However, the nashopt API signature shown in Section 2 expects `payoff_matrix` with shape `(N x N x actions)`. These are inconsistent.

**Resolution**: The table is correct for describing the *logical* payoff structure of WTA mode (each agent has a single scalar payoff based on ranking). The code handles the shape mismatch: `nashopt.check_equilibrium()` accepts non-square matrices for single-action games (each agent has exactly one "action" — their ranking payoff). The N×1 shape is a valid degenerate case of the N×N×A general form where A=1 and the interaction dimension collapses.

The Section 2 API comment `# np.ndarray (N x N x actions)` describes the *general* case for multi-action games. For WTA specifically, the matrix is N×1 because each agent has a single action (accept ranking position). No code change is needed.

---

## Amendment: Cooperative Payoff Matrix — Heuristic-Only (spec 038, RE-3)

**Date**: 2026-04-02

### Issue

The cooperative mode's payoff matrix construction (`solver.py::_build_cooperative_matrix()`) mixes two semantically different data sources:

- **Diagonal entries (self-payoff)**: `surviving_count` — how many of the agent's recommendations survived into synthesis.
- **Off-diagonal entries (interaction)**: `agreement_matrix` — pairwise agreement scores between agents.

These quantities have different scales and semantics. `surviving_count` is an absolute count (0, 1, 2, ...) while `agreement_matrix` entries are normalized agreement scores. Feeding the resulting matrix to `nashopt.check_equilibrium()` produces an equilibrium distance value, but the equilibrium found is not game-theoretically meaningful because the payoff function is not internally consistent — an agent's self-payoff is measured on a different axis than its interaction payoffs.

### Resolution

The cooperative payoff matrix is designated **heuristic-only**. It is designed for the heuristic scoring path (spec 017) where the matrix is used to compute a stability estimate, not a formal Nash equilibrium. The code already carries this designation via a docstring warning in `_build_cooperative_matrix()` (see `.. warning:: HEURISTIC APPROXIMATION`).

**Current behavior (heuristic path)**: The mixed-source matrix produces a useful stability signal. Higher `surviving_count` on the diagonal correlates with cooperative success; higher agreement off-diagonal correlates with consensus. The heuristic scorer interprets the resulting "distance" as a quality metric, not a true equilibrium distance. This is the intended behavior and is correct for the heuristic path.

**Solver-correct version (future)**: If the nashopt solver path is used for cooperative mode, the payoff matrix should use `agreement_matrix` consistently for all entries — including the diagonal, where the value would represent self-agreement (internal consistency of the agent's recommendations). Alternatively, `surviving_count` could be normalized to the same scale as `agreement_matrix` entries. This is deferred to a future spec that introduces solver-grade cooperative equilibrium computation.

No code change is needed. The `payoffs.py::cooperative_payoff()` function (used by the per-agent heuristic path) similarly uses `surviving_count` for its payoff calculation, which is consistent with the heuristic designation.
