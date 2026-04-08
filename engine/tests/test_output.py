"""Tests for engine.output — directory creation, path computation, and file writing."""

from __future__ import annotations

from pathlib import Path

import pytest

from engine.config import AgentConfig
from engine.output import OutputManager


# ---------------------------------------------------------------------------
# Directory creation
# ---------------------------------------------------------------------------

class TestCreatePhase1Dirs:
    """create_phase1_dirs builds the expected directory layout."""

    def test_creates_agent_dirs_with_cross_reviews(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        agents = [
            AgentConfig(name="agent-a", prompt="A"),
            AgentConfig(name="agent-b", prompt="B"),
        ]
        mgr.create_phase1_dirs(agents)

        assert (tmp_output_dir / "agent-a" / "cross-reviews").is_dir()
        assert (tmp_output_dir / "agent-b" / "cross-reviews").is_dir()

    def test_creates_summary_dir(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        agents = [AgentConfig(name="a", prompt="A"), AgentConfig(name="b", prompt="B")]
        mgr.create_phase1_dirs(agents)
        assert (tmp_output_dir / "summary").is_dir()

    def test_creates_arbiter_dir_when_requested(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        agents = [AgentConfig(name="a", prompt="A"), AgentConfig(name="b", prompt="B")]
        mgr.create_phase1_dirs(agents, has_arbiter=True)
        assert (tmp_output_dir / "arbiter").is_dir()

    def test_no_arbiter_dir_by_default(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        agents = [AgentConfig(name="a", prompt="A"), AgentConfig(name="b", prompt="B")]
        mgr.create_phase1_dirs(agents)
        assert not (tmp_output_dir / "arbiter").exists()

    def test_idempotent(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        agents = [AgentConfig(name="a", prompt="A"), AgentConfig(name="b", prompt="B")]
        mgr.create_phase1_dirs(agents)
        mgr.create_phase1_dirs(agents)  # should not raise


# ---------------------------------------------------------------------------
# get_output_path (backward compatibility)
# ---------------------------------------------------------------------------

class TestGetOutputPath:
    """get_output_path returns expected paths."""

    def test_review_path(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_output_path("agent-a", "review")
        assert path == tmp_output_dir / "agent-a" / "review.md"

    def test_other_phase_path(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_output_path("agent-a", "revision")
        assert path == tmp_output_dir / "agent-a" / "revision.md"

    def test_revision_with_iteration(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_output_path("agent-a", "revision", iteration=2)
        assert path == tmp_output_dir / "agent-a" / "revision_2.md"

    def test_disputes_phase(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_output_path("agent-a", "disputes")
        assert path == tmp_output_dir / "agent-a" / "disputes.md"

    def test_synthesis_phase(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_output_path("agent-a", "synthesis")
        assert path == tmp_output_dir / "summary" / "final.md"


# ---------------------------------------------------------------------------
# Phase 1: Review paths
# ---------------------------------------------------------------------------

class TestGetReviewPath:
    """get_review_path returns the correct review file path."""

    def test_review_path(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_review_path("alpha") == tmp_output_dir / "alpha" / "review.md"


# ---------------------------------------------------------------------------
# Phase 2: Cross-review paths
# ---------------------------------------------------------------------------

class TestGetCrossReviewPath:
    """get_cross_review_path returns {output}/{reviewer}/cross-reviews/{reviewed}.md."""

    def test_two_agents(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_cross_review_path("alpha", "beta")
        assert path == tmp_output_dir / "alpha" / "cross-reviews" / "beta.md"

    def test_reversed_pair(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_cross_review_path("beta", "alpha")
        assert path == tmp_output_dir / "beta" / "cross-reviews" / "alpha.md"


# ---------------------------------------------------------------------------
# Phase 3: Revision paths (iteration naming convention)
# ---------------------------------------------------------------------------

class TestGetRevisionPath:
    """get_revision_path implements the revision naming convention."""

    def test_iteration_1_is_revision_md(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_revision_path("alpha", 1) == tmp_output_dir / "alpha" / "revision.md"

    def test_iteration_2_is_revision_2_md(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_revision_path("alpha", 2) == tmp_output_dir / "alpha" / "revision_2.md"

    def test_iteration_3_is_revision_3_md(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_revision_path("alpha", 3) == tmp_output_dir / "alpha" / "revision_3.md"

    def test_never_revision_1_md(self, tmp_output_dir: Path) -> None:
        """The name ``revision_1.md`` must NEVER appear — iteration 1 is ``revision.md``."""
        mgr = OutputManager(tmp_output_dir)
        path = mgr.get_revision_path("alpha", 1)
        assert "revision_1" not in path.name


class TestPositionPath:
    """position_path returns what agents READ at a given iteration."""

    def test_iteration_1_reads_review(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.position_path("alpha", 1) == tmp_output_dir / "alpha" / "review.md"

    def test_iteration_2_reads_revision_md(self, tmp_output_dir: Path) -> None:
        """Iteration 2 reads revision.md (NOT revision_1.md — that file never exists)."""
        mgr = OutputManager(tmp_output_dir)
        path = mgr.position_path("alpha", 2)
        assert path == tmp_output_dir / "alpha" / "revision.md"
        assert "revision_1" not in path.name

    def test_iteration_3_reads_revision_2(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.position_path("alpha", 3) == tmp_output_dir / "alpha" / "revision_2.md"

    def test_iteration_4_reads_revision_3(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.position_path("alpha", 4) == tmp_output_dir / "alpha" / "revision_3.md"


class TestGetFinalRevisionPath:
    """get_final_revision_path wraps get_revision_path with total iterations."""

    def test_single_iteration(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_final_revision_path("alpha", 1) == tmp_output_dir / "alpha" / "revision.md"

    def test_two_iterations(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_final_revision_path("alpha", 2) == tmp_output_dir / "alpha" / "revision_2.md"


# ---------------------------------------------------------------------------
# Phase 4: Disputes paths
# ---------------------------------------------------------------------------

class TestGetDisputesPath:
    """get_disputes_path returns {output}/{agent}/disputes.md."""

    def test_disputes_path(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_disputes_path("alpha") == tmp_output_dir / "alpha" / "disputes.md"


# ---------------------------------------------------------------------------
# Phase 5: Synthesis path
# ---------------------------------------------------------------------------

class TestGetSynthesisPath:
    """get_synthesis_path returns {output}/summary/final.md."""

    def test_synthesis_path(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_synthesis_path() == tmp_output_dir / "summary" / "final.md"


# ---------------------------------------------------------------------------
# List helpers
# ---------------------------------------------------------------------------

class TestListHelpers:
    """List helpers return correct paths for multiple agents."""

    AGENTS = ["alpha", "beta", "gamma"]

    def test_all_review_paths(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        paths = mgr.get_all_review_paths(self.AGENTS)
        assert len(paths) == 3
        assert paths[0] == tmp_output_dir / "alpha" / "review.md"
        assert paths[1] == tmp_output_dir / "beta" / "review.md"
        assert paths[2] == tmp_output_dir / "gamma" / "review.md"

    def test_all_cross_review_paths_2_agents(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        paths = mgr.get_all_cross_review_paths(["alpha", "beta"])
        # 2 agents → 2×1 = 2 cross-review paths
        assert len(paths) == 2
        assert tmp_output_dir / "alpha" / "cross-reviews" / "beta.md" in paths
        assert tmp_output_dir / "beta" / "cross-reviews" / "alpha.md" in paths

    def test_all_cross_review_paths_3_agents(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        paths = mgr.get_all_cross_review_paths(self.AGENTS)
        # 3 agents → 3×2 = 6 cross-review paths
        assert len(paths) == 6

    def test_all_final_revision_paths_single_iteration(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        paths = mgr.get_all_final_revision_paths(self.AGENTS, iterations=1)
        assert len(paths) == 3
        assert all(p.name == "revision.md" for p in paths)

    def test_all_final_revision_paths_two_iterations(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        paths = mgr.get_all_final_revision_paths(self.AGENTS, iterations=2)
        assert len(paths) == 3
        assert all(p.name == "revision_2.md" for p in paths)

    def test_all_disputes_paths(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        paths = mgr.get_all_disputes_paths(self.AGENTS)
        assert len(paths) == 3
        assert paths[0] == tmp_output_dir / "alpha" / "disputes.md"
        assert paths[1] == tmp_output_dir / "beta" / "disputes.md"
        assert paths[2] == tmp_output_dir / "gamma" / "disputes.md"


# ---------------------------------------------------------------------------
# write_agent_output
# ---------------------------------------------------------------------------

class TestWriteAgentOutput:
    """write_agent_output writes to the correct path."""

    def test_writes_file(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        content = "# Review by agent-a\n\nThis spec looks good."
        path = mgr.write_agent_output("agent-a", "review", content)

        assert path.exists()
        assert path.read_text(encoding="utf-8") == content
        assert path == tmp_output_dir / "agent-a" / "review.md"

    def test_creates_parent_dirs(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        # Parent doesn't exist yet
        assert not (tmp_output_dir / "new-agent").exists()
        mgr.write_agent_output("new-agent", "review", "content")
        assert (tmp_output_dir / "new-agent" / "review.md").exists()

    def test_returns_written_path(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        path = mgr.write_agent_output("a", "review", "data")
        assert isinstance(path, Path)
        assert path.is_file()


# ---------------------------------------------------------------------------
# Round-aware paths
# ---------------------------------------------------------------------------

class TestGetRoundBase:
    """get_round_base returns flat dir for round 1, round-N/ for round 2+."""

    def test_round_1_returns_root(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_round_base(1) == tmp_output_dir

    def test_round_2_returns_round_subdir(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_round_base(2) == tmp_output_dir / "round-2"

    def test_round_3_returns_round_subdir(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_round_base(3) == tmp_output_dir / "round-3"


class TestRetroactiveMoveToRound1:
    """retroactive_move_to_round_1 moves flat structure into round-1/."""

    def _populate_flat_output(self, out: Path) -> None:
        """Create a realistic flat output structure for testing."""
        (out / "alpha" / "cross-reviews").mkdir(parents=True)
        (out / "alpha" / "review.md").write_text("alpha review")
        (out / "beta" / "cross-reviews").mkdir(parents=True)
        (out / "beta" / "review.md").write_text("beta review")
        (out / "summary").mkdir(parents=True)
        (out / "summary" / "final.md").write_text("synthesis")

    def test_moves_agent_dirs_and_summary(self, tmp_output_dir: Path) -> None:
        self._populate_flat_output(tmp_output_dir)
        mgr = OutputManager(tmp_output_dir)
        mgr.retroactive_move_to_round_1()

        round_1 = tmp_output_dir / "round-1"
        assert round_1.is_dir()
        assert (round_1 / "alpha" / "review.md").read_text() == "alpha review"
        assert (round_1 / "beta" / "review.md").read_text() == "beta review"
        assert (round_1 / "summary" / "final.md").read_text() == "synthesis"
        # Original flat dirs should be gone
        assert not (tmp_output_dir / "alpha").exists()
        assert not (tmp_output_dir / "beta").exists()

    def test_moves_arbiter_dir(self, tmp_output_dir: Path) -> None:
        self._populate_flat_output(tmp_output_dir)
        (tmp_output_dir / "arbiter").mkdir()
        (tmp_output_dir / "arbiter" / "resolution.md").write_text("ruling")
        mgr = OutputManager(tmp_output_dir)
        mgr.retroactive_move_to_round_1()

        assert (tmp_output_dir / "round-1" / "arbiter" / "resolution.md").read_text() == "ruling"
        assert not (tmp_output_dir / "arbiter").exists()

    def test_updates_output_dir(self, tmp_output_dir: Path) -> None:
        self._populate_flat_output(tmp_output_dir)
        mgr = OutputManager(tmp_output_dir)
        mgr.retroactive_move_to_round_1()

        assert mgr.output_dir == tmp_output_dir / "round-1"

    def test_idempotent(self, tmp_output_dir: Path) -> None:
        self._populate_flat_output(tmp_output_dir)
        mgr = OutputManager(tmp_output_dir)
        mgr.retroactive_move_to_round_1()
        # Call again — should not raise, should still point to round-1
        mgr.retroactive_move_to_round_1()
        assert mgr.output_dir == tmp_output_dir / "round-1"
        assert (tmp_output_dir / "round-1" / "alpha" / "review.md").exists()

    def test_idempotent_with_new_manager(self, tmp_output_dir: Path) -> None:
        """A new OutputManager calling retroactive_move on already-moved output."""
        self._populate_flat_output(tmp_output_dir)
        mgr1 = OutputManager(tmp_output_dir)
        mgr1.retroactive_move_to_round_1()

        # New manager instance sees the already-moved structure
        mgr2 = OutputManager(tmp_output_dir)
        mgr2.retroactive_move_to_round_1()
        assert mgr2.output_dir == tmp_output_dir / "round-1"


class TestCreateRoundDirs:
    """create_round_dirs creates directory structure in the right round."""

    def test_round_2_dirs(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        agents = [
            AgentConfig(name="alpha", prompt="A"),
            AgentConfig(name="beta", prompt="B"),
        ]
        mgr.create_round_dirs(2, agents, has_arbiter=True)

        round_2 = tmp_output_dir / "round-2"
        assert (round_2 / "alpha" / "cross-reviews").is_dir()
        assert (round_2 / "beta" / "cross-reviews").is_dir()
        assert (round_2 / "summary").is_dir()
        assert (round_2 / "arbiter").is_dir()

    def test_does_not_change_output_dir(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        agents = [AgentConfig(name="a", prompt="A"), AgentConfig(name="b", prompt="B")]
        original_output_dir = mgr.output_dir
        mgr.create_round_dirs(3, agents)
        assert mgr.output_dir == original_output_dir


class TestGetArbitrationPath:
    """get_arbitration_path returns {base}/arbiter/resolution.md."""

    def test_default_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_arbitration_path() == tmp_output_dir / "arbiter" / "resolution.md"

    def test_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        assert mgr.get_arbitration_path(round_base=rb) == rb / "arbiter" / "resolution.md"


class TestGetCrossRoundSynthesisPath:
    """get_cross_round_synthesis_path returns top-level summary/final.md."""

    def test_returns_root_summary(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_cross_round_synthesis_path() == tmp_output_dir / "summary" / "final.md"

    def test_returns_root_even_after_retroactive_move(self, tmp_output_dir: Path) -> None:
        """After retroactive move, cross-round synthesis still uses root."""
        # Populate and move
        (tmp_output_dir / "alpha").mkdir()
        (tmp_output_dir / "summary").mkdir()
        (tmp_output_dir / "summary" / "final.md").write_text("s1")
        mgr = OutputManager(tmp_output_dir)
        mgr.retroactive_move_to_round_1()

        # Cross-round synthesis path should point to root, not round-1
        path = mgr.get_cross_round_synthesis_path()
        assert path == tmp_output_dir / "summary" / "final.md"
        assert path != tmp_output_dir / "round-1" / "summary" / "final.md"


class TestRoundAwarePathMethods:
    """Existing path methods accept round_base and preserve backward compat."""

    def test_review_path_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        assert mgr.get_review_path("alpha", round_base=rb) == rb / "alpha" / "review.md"

    def test_review_path_default(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        assert mgr.get_review_path("alpha") == tmp_output_dir / "alpha" / "review.md"

    def test_cross_review_path_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        path = mgr.get_cross_review_path("alpha", "beta", round_base=rb)
        assert path == rb / "alpha" / "cross-reviews" / "beta.md"

    def test_revision_path_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        assert mgr.get_revision_path("alpha", 1, round_base=rb) == rb / "alpha" / "revision.md"

    def test_disputes_path_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        assert mgr.get_disputes_path("alpha", round_base=rb) == rb / "alpha" / "disputes.md"

    def test_synthesis_path_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        assert mgr.get_synthesis_path(round_base=rb) == rb / "summary" / "final.md"

    def test_position_path_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        assert mgr.position_path("alpha", 1, round_base=rb) == rb / "alpha" / "review.md"

    def test_final_revision_path_with_round_base(self, tmp_output_dir: Path) -> None:
        mgr = OutputManager(tmp_output_dir)
        rb = tmp_output_dir / "round-2"
        assert mgr.get_final_revision_path("alpha", 2, round_base=rb) == rb / "alpha" / "revision_2.md"
