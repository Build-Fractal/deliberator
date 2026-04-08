"""Pure Python solver functions for Tier 1 game forms (spec 025).

Provides:
- Shapley value computation for coalitional games (N <= 10)
- Potential game diagnostic (symmetry check on payoff Jacobian)

No scipy, nashopt, or AMPL dependencies — pure Python only.
"""

from __future__ import annotations

from itertools import combinations
from math import factorial
from typing import Optional

from conversus.schemas.game_forms import CoalitionalGame


# ---------------------------------------------------------------------------
# Shapley value computation
# ---------------------------------------------------------------------------


def compute_shapley_values(game: CoalitionalGame) -> dict[str, float]:
    """Compute Shapley values for a coalitional game.

    The Shapley value for player i is:
        phi_i = sum over S subset of N\\{i}:
            |S|! * (|N|-|S|-1)! / |N|! * [v(S union {i}) - v(S)]

    Args:
        game: A validated CoalitionalGame instance.

    Returns:
        Dictionary mapping each player to their Shapley value.

    Raises:
        ValueError: If the game has more than 10 players (combinatorial
            explosion). Use sampling approximation for larger games.
    """
    n = len(game.players)
    if n > 10:
        raise ValueError(
            f"Exact Shapley computation supports at most 10 players, "
            f"got {n}. Use sampling approximation for larger games."
        )

    cf = game.characteristic_function
    n_factorial = factorial(n)
    shapley: dict[str, float] = {}

    for player in game.players:
        phi = 0.0
        others = [p for p in game.players if p != player]

        for size in range(0, n):
            for coalition_tuple in combinations(others, size):
                coalition = sorted(coalition_tuple)
                coalition_key = ",".join(coalition) if coalition else ""
                coalition_with_player = sorted(coalition + [player])
                coalition_with_key = ",".join(coalition_with_player)

                v_with = cf.get(coalition_with_key, 0.0)
                v_without = cf.get(coalition_key, 0.0)

                weight = factorial(size) * factorial(n - size - 1) / n_factorial
                phi += weight * (v_with - v_without)

        shapley[player] = phi

    return shapley


# ---------------------------------------------------------------------------
# Potential game diagnostic
# ---------------------------------------------------------------------------


def is_potential_game(payoff_matrix: list[list[float]]) -> bool:
    """Check whether a 2-player normal-form game is a potential game.

    A 2-player game is a potential game iff for every pair of strategy
    profiles that differ in exactly one player's strategy, the change in
    that player's payoff equals the change in a common potential function.

    For a 2x2 game with payoffs:
        (a11, b11) (a12, b12)
        (a21, b21) (a22, b22)

    The game is potential iff:
        a11 - a21 - a12 + a22 == b11 - b12 - b21 + b22

    This generalizes: the payoff Jacobian (matrix of cross-partial
    differences) must be symmetric.

    Args:
        payoff_matrix: 2D list where payoff_matrix[i][j] = [payoff_player1,
            payoff_player2] for a 2-player game.

    Returns:
        True if the game admits a potential function.
    """
    rows = len(payoff_matrix)
    if rows == 0:
        return True

    cols = len(payoff_matrix[0])

    # Check symmetry condition for all 2x2 sub-games
    for i1 in range(rows):
        for i2 in range(i1 + 1, rows):
            for j1 in range(cols):
                for j2 in range(j1 + 1, cols):
                    # Player 1's payoff differences (row changes)
                    delta_a = (
                        payoff_matrix[i1][j1][0]
                        - payoff_matrix[i2][j1][0]
                        - payoff_matrix[i1][j2][0]
                        + payoff_matrix[i2][j2][0]
                    )
                    # Player 2's payoff differences (column changes)
                    delta_b = (
                        payoff_matrix[i1][j1][1]
                        - payoff_matrix[i1][j2][1]
                        - payoff_matrix[i2][j1][1]
                        + payoff_matrix[i2][j2][1]
                    )
                    if abs(delta_a - delta_b) > 1e-9:
                        return False

    return True


def compute_potential(payoff_matrix: list[list[float]]) -> Optional[float]:
    """Compute the potential function value at the (0,0) strategy profile.

    Returns None if the game is not a potential game.

    For a potential game, the potential Phi satisfies:
        Phi(i,j) - Phi(i',j) = a(i,j) - a(i',j)  (player 1 deviations)
        Phi(i,j) - Phi(i,j') = b(i,j) - b(i,j')  (player 2 deviations)

    We set Phi(0,0) = 0 and compute from there. Returns the maximum
    potential value across all strategy profiles as a summary statistic.

    Args:
        payoff_matrix: 2D list where each cell is [payoff_p1, payoff_p2].

    Returns:
        The maximum potential value, or None if not a potential game.
    """
    if not is_potential_game(payoff_matrix):
        return None

    rows = len(payoff_matrix)
    if rows == 0:
        return 0.0
    cols = len(payoff_matrix[0])

    # Build potential matrix, anchored at Phi(0,0) = 0
    phi = [[0.0] * cols for _ in range(rows)]

    # Fill first column using player 1's payoffs
    for i in range(1, rows):
        phi[i][0] = phi[i - 1][0] + (
            payoff_matrix[i][0][0] - payoff_matrix[i - 1][0][0]
        )

    # Fill remaining columns using player 2's payoffs
    for i in range(rows):
        for j in range(1, cols):
            phi[i][j] = phi[i][j - 1] + (
                payoff_matrix[i][j][1] - payoff_matrix[i][j - 1][1]
            )

    return max(phi[i][j] for i in range(rows) for j in range(cols))
