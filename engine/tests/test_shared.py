"""Tests for shared engine utilities — cost estimation and root discovery."""

from __future__ import annotations

from pathlib import Path

import pytest

from engine.cost import estimate_cost
from engine._root import find_project_root


# ---------------------------------------------------------------------------
# estimate_cost
# ---------------------------------------------------------------------------


class TestEstimateCost:
    """Canonical D007 formula: shared cost estimation."""

    def test_two_agents_one_iteration_no_arbiter(self) -> None:
        result = estimate_cost(agent_count=2, iterations=1, has_arbiter=False)
        assert result == {
            "review": 2,
            "cross_review": 2,
            "revision": 2,
            "disputes": 2,
            "synthesis": 1,
        }
        assert sum(result.values()) == 9

    def test_three_agents_two_iterations_with_arbiter(self) -> None:
        # Per the spec 061 step 13 cost-estimate gap fix, cross_review
        # scales by iterations (the iteration loop runs Phase 2 once
        # per iteration). Prior to the fix this asserted 6 (the buggy
        # N × (N-1) formula); the corrected formula is
        # N × (N-1) × iterations = 3 × 2 × 2 = 12.
        result = estimate_cost(agent_count=3, iterations=2, has_arbiter=True)
        assert result["review"] == 3
        assert result["cross_review"] == 12  # 3 * (3 - 1) * 2
        assert result["revision"] == 6  # 3 * 2
        assert result["disputes"] == 3
        assert result["synthesis"] == 1
        assert result["arbitration"] == 1
        assert sum(result.values()) == 26  # 3 + 12 + 6 + 3 + 1 + 1

    def test_no_arbiter_excludes_arbitration_key(self) -> None:
        result = estimate_cost(agent_count=2, iterations=1, has_arbiter=False)
        assert "arbitration" not in result

    def test_with_arbiter_includes_arbitration_key(self) -> None:
        result = estimate_cost(agent_count=2, iterations=1, has_arbiter=True)
        assert "arbitration" in result
        assert result["arbitration"] == 1

    def test_single_agent_zero_cross_reviews(self) -> None:
        result = estimate_cost(agent_count=1, iterations=1, has_arbiter=False)
        assert result["cross_review"] == 0

    def test_four_agents_cross_review_formula(self) -> None:
        result = estimate_cost(agent_count=4, iterations=1, has_arbiter=False)
        assert result["cross_review"] == 12  # 4 * 3


# ---------------------------------------------------------------------------
# find_project_root
# ---------------------------------------------------------------------------


class TestFindProjectRoot:
    """Shared root discovery used by CLI, SDK, and MCP server."""

    def test_finds_root_from_engine_package(self) -> None:
        """The real project should be findable."""
        root = find_project_root(marker="presets")
        assert (root / "presets").is_dir()

    def test_finds_root_with_custom_marker(self) -> None:
        root = find_project_root(marker="templates")
        assert (root / "templates").is_dir()

    def test_raises_for_nonexistent_marker(self, tmp_path: Path) -> None:
        # Use a marker that doesn't exist anywhere
        with pytest.raises(FileNotFoundError, match="Cannot locate"):
            find_project_root(marker="this_marker_does_not_exist_xyz")

    def test_anchor_resolution(self, tmp_path: Path) -> None:
        """When anchor points inside a dir with the marker, find it."""
        marker_dir = tmp_path / "my_marker"
        marker_dir.mkdir()
        sub = tmp_path / "sub" / "deep"
        sub.mkdir(parents=True)
        anchor_file = sub / "file.yml"
        anchor_file.touch()

        root = find_project_root(marker="my_marker", anchor=anchor_file)
        assert root == tmp_path
