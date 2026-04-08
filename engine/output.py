"""Output directory management for the conversus engine.

Provides ``OutputManager`` which creates the flat output directory structure
for deliberation runs and writes agent response files to the correct paths.

Directory layout for a single-round (flat) run::

    {output}/
    ├── {agent-name}/
    │   ├── review.md
    │   ├── cross-reviews/
    │   │   └── {other-agent}.md
    │   ├── revision.md           (iteration 1)
    │   ├── revision_2.md         (iteration 2, if iterations > 1)
    │   └── disputes.md
    ├── {agent-name-2}/
    │   └── ...
    ├── arbiter/          (if arbiter configured)
    └── summary/
        └── final.md

Multi-round layout (round 2+ triggers retroactive move)::

    {output}/
    ├── round-1/          (retroactively moved from flat layout)
    │   ├── {agent-name}/...
    │   ├── arbiter/
    │   └── summary/final.md
    ├── round-2/
    │   ├── {agent-name}/...
    │   ├── arbiter/
    │   └── summary/final.md
    └── summary/
        └── final.md      (cross-round synthesis, top-level)

Revision naming convention (critical for correctness):
  - iteration 1 → ``revision.md`` (never ``revision_1.md``)
  - iteration N (N > 1) → ``revision_{N}.md``
"""

from __future__ import annotations

import shutil
from pathlib import Path

from engine.config import AgentConfig

# Directories that belong to the flat output layout and are subject
# to retroactive move into ``round-1/``.
_FLAT_LAYOUT_DIRS = frozenset({"summary", "arbiter"})


class OutputManager:
    """Manages the output directory structure and file writing for engine runs.

    Attributes:
        output_dir: The resolved base output directory path.
        _root_dir: The original output directory (never changes). Used for
            cross-round synthesis paths that live at the top level.
    """

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = Path(output_dir).resolve()
        self._root_dir = self.output_dir

    # ------------------------------------------------------------------
    # Directory creation
    # ------------------------------------------------------------------

    def create_phase1_dirs(
        self,
        agents: list[AgentConfig],
        *,
        has_arbiter: bool = False,
    ) -> None:
        """Create the directory layout for Phase 1 (reviews).

        Creates per-agent directories with cross-reviews/ subdirectory,
        a summary/ directory, and optionally an arbiter/ directory.

        Args:
            agents: List of agent configurations to create directories for.
            has_arbiter: Whether to create an arbiter output directory.
        """
        for agent in agents:
            agent_dir = self.output_dir / agent.name / "cross-reviews"
            agent_dir.mkdir(parents=True, exist_ok=True)

        summary_dir = self.output_dir / "summary"
        summary_dir.mkdir(parents=True, exist_ok=True)

        if has_arbiter:
            arbiter_dir = self.output_dir / "arbiter"
            arbiter_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Phase 1: Review paths
    # ------------------------------------------------------------------

    def get_review_path(self, agent_name: str, *, round_base: Path | None = None) -> Path:
        """Return ``{base}/{agent}/review.md``.

        Args:
            agent_name: The agent's name.
            round_base: Optional round directory to use as base.  When *None*,
                uses ``self.output_dir`` (backward-compatible).
        """
        base = round_base if round_base is not None else self.output_dir
        return base / agent_name / "review.md"

    # ------------------------------------------------------------------
    # Phase 2: Cross-review paths
    # ------------------------------------------------------------------

    def get_cross_review_path(
        self, reviewer: str, reviewed: str, *, round_base: Path | None = None
    ) -> Path:
        """Return ``{base}/{reviewer}/cross-reviews/{reviewed}.md``."""
        base = round_base if round_base is not None else self.output_dir
        return base / reviewer / "cross-reviews" / f"{reviewed}.md"

    # ------------------------------------------------------------------
    # Phase 3: Revision paths (iteration-aware naming)
    # ------------------------------------------------------------------

    def get_revision_path(
        self, agent: str, iteration: int, *, round_base: Path | None = None
    ) -> Path:
        """Return the revision output path for a given iteration.

        Naming convention:
          - iteration 1 → ``revision.md``
          - iteration N > 1 → ``revision_{N}.md``
        """
        base = round_base if round_base is not None else self.output_dir
        if iteration == 1:
            return base / agent / "revision.md"
        return base / agent / f"revision_{iteration}.md"

    def position_path(
        self, agent: str, iteration: int, *, round_base: Path | None = None
    ) -> Path:
        """Return the path that cross-reviews/revisions READ at a given iteration.

        This is the "prior position" that informs the current iteration:
          - iteration 1 → ``review.md`` (Phase 1 output)
          - iteration 2 → ``revision.md`` (first revision, i.e. iteration 1 output)
          - iteration N > 2 → ``revision_{N-1}.md``
        """
        base = round_base if round_base is not None else self.output_dir
        if iteration == 1:
            return base / agent / "review.md"
        if iteration == 2:
            return base / agent / "revision.md"
        return base / agent / f"revision_{iteration - 1}.md"

    def get_final_revision_path(
        self, agent: str, iterations: int, *, round_base: Path | None = None
    ) -> Path:
        """Return the path of the final revision after all iterations complete.

        Wraps ``get_revision_path`` with the total iteration count:
          - iterations=1 → ``revision.md``
          - iterations=N (N>1) → ``revision_{N}.md``
        """
        return self.get_revision_path(agent, iterations, round_base=round_base)

    # ------------------------------------------------------------------
    # Phase 4: Disputes paths
    # ------------------------------------------------------------------

    def get_disputes_path(self, agent: str, *, round_base: Path | None = None) -> Path:
        """Return ``{base}/{agent}/disputes.md``."""
        base = round_base if round_base is not None else self.output_dir
        return base / agent / "disputes.md"

    # ------------------------------------------------------------------
    # Phase 5: Synthesis path
    # ------------------------------------------------------------------

    def get_synthesis_path(self, *, round_base: Path | None = None) -> Path:
        """Return ``{base}/summary/final.md``."""
        base = round_base if round_base is not None else self.output_dir
        return base / "summary" / "final.md"

    # ------------------------------------------------------------------
    # Round-aware paths and directory management
    # ------------------------------------------------------------------

    def get_round_base(self, round_num: int) -> Path:
        """Return the base directory for a specific round.

        Round 1 uses the flat output directory (``self._root_dir``).
        Round 2+ uses ``{root}/round-{N}``.

        After ``retroactive_move_to_round_1()`` has been called,
        ``self.output_dir`` already points to ``round-1/``; this method
        always computes from the original root.
        """
        if round_num == 1:
            return self._root_dir
        return self._root_dir / f"round-{round_num}"

    def retroactive_move_to_round_1(self) -> None:
        """Move all flat agent directories, summary/, and arbiter/ into ``round-1/``.

        Called when round 2 begins, to retroactively organize round 1 output.
        Idempotent — if ``round-1/`` already exists, this is a no-op.

        After the move, updates ``self.output_dir`` to ``{root}/round-1/``
        so subsequent path computations (for round 1 context references)
        resolve correctly.
        """
        round_1_dir = self._root_dir / "round-1"
        if round_1_dir.exists():
            # Already moved — idempotent.
            self.output_dir = round_1_dir
            return

        round_1_dir.mkdir(parents=True)

        for child in sorted(self._root_dir.iterdir()):
            # Skip the newly-created round-1 directory itself
            if child.name == "round-1":
                continue
            # Skip any existing round-N directories (shouldn't exist, but be safe)
            if child.name.startswith("round-"):
                continue
            shutil.move(str(child), str(round_1_dir / child.name))

        self.output_dir = round_1_dir

    def create_round_dirs(
        self,
        round_num: int,
        agents: list[AgentConfig],
        has_arbiter: bool = False,
    ) -> None:
        """Create the directory structure for a new round.

        Delegates to ``create_phase1_dirs`` with the round-specific base path.

        Args:
            round_num: The round number (1-based).
            agents: List of agent configurations.
            has_arbiter: Whether to create an arbiter directory.
        """
        round_base = self.get_round_base(round_num)
        # Temporarily swap output_dir so create_phase1_dirs writes to the right place
        saved = self.output_dir
        self.output_dir = round_base
        try:
            self.create_phase1_dirs(agents, has_arbiter=has_arbiter)
        finally:
            self.output_dir = saved

    def get_arbitration_path(self, *, round_base: Path | None = None) -> Path:
        """Return ``{base}/arbiter/resolution.md``.

        Args:
            round_base: Optional round directory.  Defaults to ``self.output_dir``.
        """
        base = round_base if round_base is not None else self.output_dir
        return base / "arbiter" / "resolution.md"

    def get_cross_round_synthesis_path(self) -> Path:
        """Return ``{root}/summary/final.md`` (top-level, outside any round).

        This is the final cross-round synthesis that lives at the output root,
        not inside any round directory.
        """
        return self._root_dir / "summary" / "final.md"

    # ------------------------------------------------------------------
    # List helpers (all agents)
    # ------------------------------------------------------------------

    def get_all_review_paths(self, agents: list[str]) -> list[Path]:
        """Return review paths for all agents."""
        return [self.get_review_path(a) for a in agents]

    def get_all_cross_review_paths(self, agents: list[str]) -> list[Path]:
        """Return all cross-review paths for every reviewer/reviewed pair.

        Each agent reviews every other agent, so for N agents this returns
        N×(N-1) paths.
        """
        paths: list[Path] = []
        for reviewer in agents:
            for reviewed in agents:
                if reviewer != reviewed:
                    paths.append(self.get_cross_review_path(reviewer, reviewed))
        return paths

    def get_all_final_revision_paths(
        self, agents: list[str], iterations: int
    ) -> list[Path]:
        """Return the final revision path for each agent."""
        return [self.get_final_revision_path(a, iterations) for a in agents]

    def get_all_disputes_paths(self, agents: list[str]) -> list[Path]:
        """Return disputes paths for all agents."""
        return [self.get_disputes_path(a) for a in agents]

    # ------------------------------------------------------------------
    # Generic output path (backward-compatible, delegates to specific helpers)
    # ------------------------------------------------------------------

    def get_output_path(
        self,
        agent_name: str,
        phase: str,
        iteration: int | None = None,
    ) -> Path:
        """Compute the output file path for an agent's phase output.

        Delegates to the phase-specific helpers. Prefer calling those
        directly for clarity.

        Args:
            agent_name: The agent's name.
            phase: The phase name (e.g. ``review``, ``cross-review``,
                ``revision``, ``disputes``).
            iteration: Iteration number (required for ``revision``).

        Returns:
            The resolved output file path.
        """
        if phase == "review":
            return self.get_review_path(agent_name)
        if phase == "revision":
            return self.get_revision_path(agent_name, iteration or 1)
        if phase == "disputes":
            return self.get_disputes_path(agent_name)
        if phase == "synthesis":
            return self.get_synthesis_path()
        # Fallback for unknown phases
        return self.output_dir / agent_name / f"{phase}.md"

    # ------------------------------------------------------------------
    # File writing
    # ------------------------------------------------------------------

    def write_agent_output(
        self,
        agent_name: str,
        phase: str,
        content: str,
        iteration: int | None = None,
    ) -> Path:
        """Write agent output content to the correct file path.

        Creates parent directories automatically if they don't exist.

        Args:
            agent_name: The agent's name.
            phase: The phase name (e.g. ``review``).
            content: The content to write.
            iteration: Optional iteration number.

        Returns:
            The path the content was written to.
        """
        path = self.get_output_path(agent_name, phase, iteration)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path
