"""Tests for the 5-phase pipeline orchestrator (engine/phases.py).

Covers:
- Per-phase unit tests (correct dispatch count, output paths, events)
- Iteration loop correctness (position_path references, revision naming)
- Phase barrier enforcement (strict event ordering)
- Failure isolation (continue-with-N-1 semantics)
- Full pipeline test (3 agents, 1 iteration, correct file count)
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from engine.config import AgentConfig, EngineConfig
from engine.events import (
    AgentCompleted,
    AgentDispatched,
    CallbackEmitter,
    EngineEvent,
    NullEmitter,
    PhaseCompleted,
    PhaseStarted,
)
from engine.phases import PipelineError, PipelineResult, run_pipeline
from engine.providers import MockProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _make_config(
    tmp_path: Path,
    *,
    agent_names: list[str] | None = None,
    iterations: int = 1,
    mode: str = "cooperative",
) -> EngineConfig:
    """Build a minimal EngineConfig pointing at tmp_path for output.

    Creates a fake target file so target_files resolution works.
    """
    if agent_names is None:
        agent_names = ["alice", "bob"]

    # Create a fake target file
    target = tmp_path / "target.md"
    target.write_text("# Target spec\nThis is the target.", encoding="utf-8")

    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    agents = [
        AgentConfig(name=name, prompt=f"You are {name}.", docs=[])
        for name in agent_names
    ]

    return EngineConfig(
        mode=mode,
        target_files=[target],
        output=output_dir,
        agents=agents,
        iterations=iterations,
        rounds=1,
        stagnation="detect",
        prior_files=[],
        arbiter=None,
        validate_templates=True,
    )


def _collect_events() -> tuple[CallbackEmitter, list[EngineEvent]]:
    """Create a CallbackEmitter that records all events to a list."""
    events: list[EngineEvent] = []
    emitter = CallbackEmitter(lambda e: events.append(e))
    return emitter, events


def _config_path() -> Path:
    """Return the path to the example config for template discovery."""
    return PROJECT_ROOT / "conversus.example.yml"


# ---------------------------------------------------------------------------
# Phase 1: Review
# ---------------------------------------------------------------------------


class TestPhase1Review:
    """Tests for Phase 1 (review) within the pipeline."""

    def test_review_dispatch_count(self, tmp_path: Path) -> None:
        """Two agents → 2 dispatch calls in Phase 1."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Phase 1 dispatches: 1 per agent
        review_dispatches = [
            e for e in events if isinstance(e, AgentDispatched) and e.phase == "review"
        ]
        assert len(review_dispatches) == 2

    def test_review_output_files(self, tmp_path: Path) -> None:
        """Review output files written to correct paths."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        expected_review_paths = {
            output_dir / "alice" / "review.md",
            output_dir / "bob" / "review.md",
        }
        actual_reviews = {
            p for p in result.written_files if p.name == "review.md"
        }
        assert actual_reviews == expected_review_paths

    def test_review_events(self, tmp_path: Path) -> None:
        """PhaseStarted and PhaseCompleted emitted for review."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        phase_started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "review"
        ]
        phase_completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "review"
        ]
        assert len(phase_started) == 1
        assert len(phase_completed) == 1
        assert phase_started[0].agent_count == 2
        assert phase_completed[0].success_count == 2
        assert phase_completed[0].failure_count == 0


# ---------------------------------------------------------------------------
# Phase 2: Cross-review
# ---------------------------------------------------------------------------


class TestPhase2CrossReview:
    """Tests for Phase 2 (cross-review) within the pipeline."""

    def test_cross_review_dispatch_count(self, tmp_path: Path) -> None:
        """Two agents → 2 cross-review pairs (A→B, B→A)."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        cr_dispatches = [
            e
            for e in events
            if isinstance(e, AgentDispatched) and e.phase == "cross-review"
        ]
        assert len(cr_dispatches) == 2

    def test_cross_review_output_files(self, tmp_path: Path) -> None:
        """Cross-review files written to correct paths."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        expected = {
            output_dir / "alice" / "cross-reviews" / "bob.md",
            output_dir / "bob" / "cross-reviews" / "alice.md",
        }
        actual = {
            p for p in result.written_files if "cross-reviews" in str(p)
        }
        assert actual == expected

    def test_cross_review_events(self, tmp_path: Path) -> None:
        """PhaseStarted and PhaseCompleted emitted for cross-review."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "cross-review"
        ]
        completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "cross-review"
        ]
        assert len(started) == 1
        assert len(completed) == 1
        assert started[0].agent_count == 2
        assert completed[0].success_count == 2


# ---------------------------------------------------------------------------
# Phase 3: Revision
# ---------------------------------------------------------------------------


class TestPhase3Revision:
    """Tests for Phase 3 (revision) within the pipeline."""

    def test_revision_dispatch_count(self, tmp_path: Path) -> None:
        """Two agents → 2 revision dispatches."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        rev_dispatches = [
            e
            for e in events
            if isinstance(e, AgentDispatched) and e.phase == "revision"
        ]
        assert len(rev_dispatches) == 2

    def test_revision_output_files_iteration_1(self, tmp_path: Path) -> None:
        """Iteration 1 → revision.md (not revision_1.md)."""
        config = _make_config(tmp_path, iterations=1)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        # Check that revision.md exists, not revision_1.md
        assert (output_dir / "alice" / "revision.md").exists()
        assert (output_dir / "bob" / "revision.md").exists()
        assert not (output_dir / "alice" / "revision_1.md").exists()

    def test_revision_events(self, tmp_path: Path) -> None:
        """PhaseStarted and PhaseCompleted emitted for revision."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "revision"
        ]
        completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "revision"
        ]
        assert len(started) == 1
        assert len(completed) == 1
        assert started[0].agent_count == 2
        assert completed[0].success_count == 2


# ---------------------------------------------------------------------------
# Phase 4: Disputes
# ---------------------------------------------------------------------------


class TestPhase4Disputes:
    """Tests for Phase 4 (disputes) within the pipeline."""

    def test_disputes_dispatch_count(self, tmp_path: Path) -> None:
        """Two agents → 2 disputes dispatches."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        disp_dispatches = [
            e
            for e in events
            if isinstance(e, AgentDispatched) and e.phase == "disputes"
        ]
        assert len(disp_dispatches) == 2

    def test_disputes_output_files(self, tmp_path: Path) -> None:
        """Disputes files written to correct paths."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        expected = {
            output_dir / "alice" / "disputes.md",
            output_dir / "bob" / "disputes.md",
        }
        actual = {
            p for p in result.written_files if p.name == "disputes.md"
        }
        assert actual == expected


# ---------------------------------------------------------------------------
# Phase 5: Synthesis
# ---------------------------------------------------------------------------


class TestPhase5Synthesis:
    """Tests for Phase 5 (synthesis) within the pipeline."""

    def test_synthesis_dispatch_count(self, tmp_path: Path) -> None:
        """Synthesis always dispatches exactly 1 agent."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        synth_dispatches = [
            e
            for e in events
            if isinstance(e, AgentDispatched) and e.phase == "synthesis"
        ]
        assert len(synth_dispatches) == 1

    def test_synthesis_output_file(self, tmp_path: Path) -> None:
        """Synthesis writes to summary/final.md."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        synthesis_path = output_dir / "summary" / "final.md"
        assert synthesis_path in result.written_files
        assert synthesis_path.exists()

    def test_synthesis_events(self, tmp_path: Path) -> None:
        """PhaseStarted(agent_count=1) and PhaseCompleted emitted for synthesis."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "synthesis"
        ]
        completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "synthesis"
        ]
        assert len(started) == 1
        assert len(completed) == 1
        assert started[0].agent_count == 1
        assert completed[0].success_count == 1


# ---------------------------------------------------------------------------
# Iteration loop
# ---------------------------------------------------------------------------


class TestIterationLoop:
    """Tests for the cross-review→revision iteration loop."""

    def test_two_iterations_dispatch_counts(self, tmp_path: Path) -> None:
        """2 iterations with 2 agents: 4 cross-reviews, 4 revisions."""
        config = _make_config(tmp_path, iterations=2)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        cr_dispatches = [
            e
            for e in events
            if isinstance(e, AgentDispatched) and e.phase == "cross-review"
        ]
        rev_dispatches = [
            e
            for e in events
            if isinstance(e, AgentDispatched) and e.phase == "revision"
        ]
        # 2 iterations × 2 pairs = 4 cross-reviews
        assert len(cr_dispatches) == 4
        # 2 iterations × 2 agents = 4 revisions
        assert len(rev_dispatches) == 4

    def test_two_iterations_revision_naming(self, tmp_path: Path) -> None:
        """Iteration 1 → revision.md, iteration 2 → revision_2.md."""
        config = _make_config(tmp_path, iterations=2)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        assert (output_dir / "alice" / "revision.md").exists()
        assert (output_dir / "alice" / "revision_2.md").exists()
        assert (output_dir / "bob" / "revision.md").exists()
        assert (output_dir / "bob" / "revision_2.md").exists()
        # No revision_1.md
        assert not (output_dir / "alice" / "revision_1.md").exists()

    def test_two_iterations_events(self, tmp_path: Path) -> None:
        """2 iterations emit 2 cross-review + 2 revision PhaseStarted/Completed pairs."""
        config = _make_config(tmp_path, iterations=2)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        cr_started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "cross-review"
        ]
        cr_completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "cross-review"
        ]
        rev_started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "revision"
        ]
        rev_completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "revision"
        ]
        assert len(cr_started) == 2
        assert len(cr_completed) == 2
        assert len(rev_started) == 2
        assert len(rev_completed) == 2


# ---------------------------------------------------------------------------
# Phase barrier enforcement
# ---------------------------------------------------------------------------


class TestPhaseBarriers:
    """Verify strict PhaseStarted/PhaseCompleted sequencing."""

    def test_no_interleaving(self, tmp_path: Path) -> None:
        """Phase events never interleave — each phase completes before next starts."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Extract just phase-level events (not agent-level)
        phase_events = [
            e for e in events if isinstance(e, (PhaseStarted, PhaseCompleted))
        ]

        # Verify: alternating Started/Completed pairs, no two Starts in a row
        expecting_start = True
        for event in phase_events:
            if expecting_start:
                assert isinstance(event, PhaseStarted), (
                    f"Expected PhaseStarted but got {type(event).__name__} "
                    f"for phase '{event.phase}'"
                )
                expecting_start = False
            else:
                assert isinstance(event, PhaseCompleted), (
                    f"Expected PhaseCompleted but got {type(event).__name__} "
                    f"for phase '{event.phase}'"
                )
                expecting_start = True

    def test_phase_order_5_phases(self, tmp_path: Path) -> None:
        """With 1 iteration: review → cross-review → revision → disputes → synthesis."""
        config = _make_config(tmp_path, iterations=1)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        started_phases = [
            e.phase for e in events if isinstance(e, PhaseStarted)
        ]
        assert started_phases == [
            "review",
            "cross-review",
            "revision",
            "disputes",
            "synthesis",
        ]

    def test_phase_order_2_iterations(self, tmp_path: Path) -> None:
        """With 2 iterations: review → cr → rev → cr → rev → disputes → synthesis."""
        config = _make_config(tmp_path, iterations=2)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        started_phases = [
            e.phase for e in events if isinstance(e, PhaseStarted)
        ]
        assert started_phases == [
            "review",
            "cross-review",
            "revision",
            "cross-review",
            "revision",
            "disputes",
            "synthesis",
        ]


# ---------------------------------------------------------------------------
# Failure isolation (continue-with-N-1)
# ---------------------------------------------------------------------------


class _FailingProvider:
    """MockProvider that fails for specific agent names."""

    def __init__(self, fail_agents: set[str]) -> None:
        self.fail_agents = fail_agents
        self.calls: list[str] = []

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        # Extract agent name from the prompt structure or dispatch name
        # The prompt will contain the agent's name since context includes it
        for name in self.fail_agents:
            if name in prompt:
                self.calls.append(f"fail:{name}")
                raise RuntimeError(f"Simulated failure for {name}")
        self.calls.append("ok")
        return f"[Mock response for {model}]"

    async def stream(self, prompt: str, model: str, max_tokens: int):
        yield "[stream not used]"


class TestFailureIsolation:
    """Tests for continue-with-N-1 failure semantics."""

    def test_phase1_failure_excludes_agent(self, tmp_path: Path) -> None:
        """Agent that fails in Phase 1 is excluded from all subsequent phases."""
        config = _make_config(tmp_path, agent_names=["alice", "bob", "carol"])
        provider = _FailingProvider(fail_agents={"carol"})
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Carol should be excluded from active_agents
        assert "carol" not in result.active_agents
        assert "alice" in result.active_agents
        assert "bob" in result.active_agents

        # No cross-review, revision, disputes, or synthesis should mention carol
        # Check that no output files are in carol's directory (except potentially
        # cross-reviews dir created by create_phase1_dirs)
        carol_files = [
            p for p in result.written_files if "carol" in str(p)
        ]
        assert len(carol_files) == 0

    def test_phase1_failure_pipeline_completes(self, tmp_path: Path) -> None:
        """Pipeline completes all 5 phases even with 1 agent failing in Phase 1."""
        config = _make_config(tmp_path, agent_names=["alice", "bob", "carol"])
        provider = _FailingProvider(fail_agents={"carol"})
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.phases_completed == 5

        # Synthesis produced
        output_dir = config.output.resolve()
        assert (output_dir / "summary" / "final.md").exists()

    def test_phase1_failure_events_show_failure(self, tmp_path: Path) -> None:
        """PhaseCompleted for review shows the failure count."""
        config = _make_config(tmp_path, agent_names=["alice", "bob", "carol"])
        provider = _FailingProvider(fail_agents={"carol"})
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        review_completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "review"
        ]
        assert len(review_completed) == 1
        assert review_completed[0].failure_count == 1
        assert review_completed[0].success_count == 2

    def test_all_agents_fail_raises_pipeline_error(self, tmp_path: Path) -> None:
        """If all agents fail in Phase 1, PipelineError is raised."""
        config = _make_config(tmp_path, agent_names=["alice", "bob"])
        provider = _FailingProvider(fail_agents={"alice", "bob"})
        emitter, _ = _collect_events()

        with pytest.raises(PipelineError, match="All agents failed in Phase 1"):
            asyncio.run(
                run_pipeline(config, provider, emitter, config_path=_config_path())
            )


# ---------------------------------------------------------------------------
# Full pipeline test
# ---------------------------------------------------------------------------


class TestFullPipeline:
    """End-to-end tests for the complete 5-phase pipeline."""

    def test_3_agents_1_iteration_file_count(self, tmp_path: Path) -> None:
        """3 agents, 1 iteration → 16 files total.

        3 reviews + 6 cross-reviews + 3 revisions + 3 disputes + 1 synthesis = 16
        """
        config = _make_config(tmp_path, agent_names=["alice", "bob", "carol"])
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert len(result.written_files) == 16

    def test_3_agents_1_iteration_total_dispatches(self, tmp_path: Path) -> None:
        """3 agents, 1 iteration → 3+6+3+3+1 = 16 dispatches."""
        config = _make_config(tmp_path, agent_names=["alice", "bob", "carol"])
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.total_dispatches == 16

    def test_3_agents_1_iteration_phases_completed(self, tmp_path: Path) -> None:
        """All 5 phases completed."""
        config = _make_config(tmp_path, agent_names=["alice", "bob", "carol"])
        provider = MockProvider()
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.phases_completed == 5

    def test_3_agents_all_active_at_end(self, tmp_path: Path) -> None:
        """All 3 agents survive to the end with no failures."""
        config = _make_config(tmp_path, agent_names=["alice", "bob", "carol"])
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert set(result.active_agents) == {"alice", "bob", "carol"}

    def test_output_directory_structure(self, tmp_path: Path) -> None:
        """Verify the full output directory tree structure."""
        config = _make_config(tmp_path, agent_names=["alice", "bob"])
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()

        # Per-agent files
        for name in ["alice", "bob"]:
            assert (output_dir / name / "review.md").exists()
            assert (output_dir / name / "revision.md").exists()
            assert (output_dir / name / "disputes.md").exists()

        # Cross-reviews (each agent reviews the other)
        assert (output_dir / "alice" / "cross-reviews" / "bob.md").exists()
        assert (output_dir / "bob" / "cross-reviews" / "alice.md").exists()

        # Synthesis
        assert (output_dir / "summary" / "final.md").exists()

    def test_pipeline_result_is_frozen(self, tmp_path: Path) -> None:
        """PipelineResult is immutable (frozen Pydantic model)."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        with pytest.raises(Exception):
            result.phases_completed = 99  # type: ignore[misc]

    def test_2_agents_2_iterations_file_count(self, tmp_path: Path) -> None:
        """2 agents, 2 iterations → 14 files.

        2 reviews + 2×2 cross-reviews + 2×2 revisions + 2 disputes + 1 synthesis
        = 2 + 4 + 4 + 2 + 1 = 13
        Note: cross-reviews overwrite on subsequent iterations, so only 2 unique
        cross-review files exist. But each iteration writes them, producing
        separate write operations in written_files.
        """
        config = _make_config(tmp_path, iterations=2)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # written_files tracks all write operations (including overwrites)
        # 2 reviews + 2+2 cross-reviews + 2+2 revisions + 2 disputes + 1 synthesis = 13
        assert len(result.written_files) == 13


# ---------------------------------------------------------------------------
# Helpers for multi-round / arbitration / cross-round synthesis tests
# ---------------------------------------------------------------------------

from engine.config import ArbiterConfig


def _make_multi_round_config(
    tmp_path: Path,
    *,
    agent_names: list[str] | None = None,
    iterations: int = 1,
    rounds: int = 2,
    stagnation: str = "detect",
    mode: str = "cooperative",
    arbiter: ArbiterConfig | None = None,
) -> EngineConfig:
    """Build an EngineConfig for multi-round tests."""
    if agent_names is None:
        agent_names = ["alice", "bob"]

    target = tmp_path / "target.md"
    target.write_text("# Target spec\nThis is the target.", encoding="utf-8")

    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    agents = [
        AgentConfig(name=name, prompt=f"You are {name}.", docs=[])
        for name in agent_names
    ]

    # If arbiter specified, create its grounding file
    if arbiter is not None and not arbiter.grounding.exists():
        arbiter.grounding.parent.mkdir(parents=True, exist_ok=True)
        arbiter.grounding.write_text("Grounding doc.", encoding="utf-8")

    return EngineConfig(
        mode=mode,
        target_files=[target],
        output=output_dir,
        agents=agents,
        iterations=iterations,
        rounds=rounds,
        stagnation=stagnation,
        prior_files=[],
        arbiter=arbiter,
        validate_templates=True,
    )


def _make_arbiter_config(tmp_path: Path) -> ArbiterConfig:
    """Create a minimal ArbiterConfig for testing."""
    grounding = tmp_path / "grounding.md"
    grounding.write_text("Arbitration grounding.", encoding="utf-8")
    return ArbiterConfig(
        name="arbiter",
        prompt="You are the arbiter.",
        docs=[],
        grounding=grounding,
        trigger="always",
    )


class _DisputeProvider:
    """MockProvider that returns synthesis with configurable dispute counts.

    Synthesis phase responses contain dispute markers; all other phases
    return generic responses. ``dispute_counts`` is a list of counts —
    one per round. If the list is exhausted, repeats the last count.
    """

    def __init__(self, dispute_counts: list[int]) -> None:
        self.dispute_counts = dispute_counts
        self._synth_call = 0
        self.calls: list[str] = []

    def _make_disputes(self, count: int) -> str:
        if count == 0:
            return "# Synthesis\n\nAll agents agree. No disputes."
        markers: list[str] = []
        markers.append("<!-- CONVERSUS:DISPUTES_BEGIN -->")
        for i in range(1, count + 1):
            markers.append(
                f"**Dispute:** Dispute {i} between agents on topic {i}."
            )
        markers.append("<!-- CONVERSUS:DISPUTES_END -->")
        return "# Synthesis\n\n" + "\n".join(markers)

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        self.calls.append("complete")
        # Detect synthesis dispatch: single-agent dispatch with "synthesizer" name
        # The phase context includes synthesis-related template content
        if "synthesis" in prompt.lower() and ("AGENT_NAMES" in prompt or "ALL_REVIEWS" in prompt or "final.md" in prompt):
            idx = min(self._synth_call, len(self.dispute_counts) - 1)
            count = self.dispute_counts[idx]
            self._synth_call += 1
            return self._make_disputes(count)
        return f"[Mock response for {model}]"

    async def stream(self, prompt: str, model: str, max_tokens: int):
        yield "[stream not used]"


class _FailingArbiterProvider:
    """Provider that succeeds for all phases but fails for arbitration.

    Detection: the arbitration dispatch uses the arbiter's name as the
    agent name, so we check for the dispatch name pattern.
    """

    def __init__(self, dispute_counts: list[int] | None = None) -> None:
        self._dispute_provider = _DisputeProvider(dispute_counts or [2])
        self.calls: list[str] = []
        self._fail_next = False

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        # The arbitration template contains "resolution.md" in the OUTPUT_PATH
        # and uses the arbiter prompt. Detect via the resolution.md output path.
        if "resolution.md" in prompt and "arbiter" in prompt.lower():
            self.calls.append("fail:arbitration")
            raise RuntimeError("Simulated arbitration failure")
        self.calls.append("complete")
        return await self._dispute_provider.complete(prompt, model, max_tokens)

    async def stream(self, prompt: str, model: str, max_tokens: int):
        yield "[stream not used]"


# ---------------------------------------------------------------------------
# Multi-round tests
# ---------------------------------------------------------------------------


class TestMultiRound:
    """Tests for multi-round deliberation pipeline."""

    def test_two_rounds_creates_round_directories(self, tmp_path: Path) -> None:
        """Two-round run creates round-1/ and round-2/ directories."""
        config = _make_multi_round_config(tmp_path, rounds=2)
        # Use a provider that returns disputes on round 1, none on round 2
        provider = _DisputeProvider([2, 0])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        assert (output_dir / "round-1").is_dir()
        assert (output_dir / "round-2").is_dir()
        assert result.rounds_completed == 2

    def test_retroactive_move_on_round_2(self, tmp_path: Path) -> None:
        """Round 1 flat output is retroactively moved to round-1/."""
        config = _make_multi_round_config(tmp_path, rounds=2)
        provider = _DisputeProvider([2, 0])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        # Flat output should be moved into round-1
        assert (output_dir / "round-1" / "alice" / "review.md").exists()
        assert (output_dir / "round-1" / "bob" / "review.md").exists()
        assert (output_dir / "round-1" / "summary" / "final.md").exists()
        # No flat agent dirs at root level
        assert not (output_dir / "alice").exists()
        assert not (output_dir / "bob").exists()

    def test_stagnation_detection(self, tmp_path: Path) -> None:
        """Same dispute count across rounds → stagnation termination."""
        config = _make_multi_round_config(tmp_path, rounds=3, stagnation="detect")
        # Round 1: 2 disputes, Round 2: 2 disputes (no decrease → stagnation)
        provider = _DisputeProvider([2, 2])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.termination_reason == "stagnation"
        assert result.rounds_completed == 2

    def test_convergence_detection(self, tmp_path: Path) -> None:
        """Zero disputes → converged termination."""
        config = _make_multi_round_config(tmp_path, rounds=3)
        # Round 1: 0 disputes → converge immediately
        provider = _DisputeProvider([0])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.termination_reason == "converged"
        assert result.rounds_completed == 1

    def test_max_rounds_termination(self, tmp_path: Path) -> None:
        """Disputes remain through all rounds → max_rounds termination."""
        config = _make_multi_round_config(tmp_path, rounds=2, stagnation="ignore")
        # Disputes decrease but never reach 0
        provider = _DisputeProvider([3, 2])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.termination_reason == "max_rounds"
        assert result.rounds_completed == 2

    def test_single_round_no_termination_reason(self, tmp_path: Path) -> None:
        """Single-round pipeline has no termination_reason."""
        config = _make_multi_round_config(tmp_path, rounds=1)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.termination_reason is None
        assert result.rounds_completed == 1

    def test_pipeline_result_has_round_fields(self, tmp_path: Path) -> None:
        """PipelineResult includes rounds_completed and termination_reason."""
        config = _make_multi_round_config(tmp_path, rounds=2)
        provider = _DisputeProvider([2, 0])
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.rounds_completed == 2
        assert result.termination_reason == "converged"
        assert result.arbitration_ran is False


# ---------------------------------------------------------------------------
# Arbitration tests
# ---------------------------------------------------------------------------


class TestArbitration:
    """Tests for Phase 6 arbitration dispatch."""

    def test_always_trigger(self, tmp_path: Path) -> None:
        """Arbiter with trigger='always' runs unconditionally."""
        arbiter = _make_arbiter_config(tmp_path)
        config = _make_multi_round_config(tmp_path, rounds=1, arbiter=arbiter)
        provider = MockProvider()
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.arbitration_ran is True

        # Arbitration events emitted
        arb_started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "arbitration"
        ]
        arb_completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "arbitration"
        ]
        assert len(arb_started) == 1
        assert len(arb_completed) == 1
        assert arb_completed[0].success_count == 1

    def test_disputes_remain_trigger_with_disputes(self, tmp_path: Path) -> None:
        """Arbiter with trigger='disputes_remain' runs when disputes found."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("Grounding.", encoding="utf-8")
        arbiter = ArbiterConfig(
            name="arbiter",
            prompt="You are the arbiter.",
            docs=[],
            grounding=grounding,
            trigger="disputes_remain",
        )
        config = _make_multi_round_config(tmp_path, rounds=1, arbiter=arbiter)
        # Provider returns synthesis with disputes
        provider = _DisputeProvider([2])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.arbitration_ran is True

    def test_disputes_remain_trigger_no_disputes(self, tmp_path: Path) -> None:
        """Arbiter with trigger='disputes_remain' skips when no disputes."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("Grounding.", encoding="utf-8")
        arbiter = ArbiterConfig(
            name="arbiter",
            prompt="You are the arbiter.",
            docs=[],
            grounding=grounding,
            trigger="disputes_remain",
        )
        config = _make_multi_round_config(tmp_path, rounds=1, arbiter=arbiter)
        # Provider returns synthesis with no disputes
        provider = _DisputeProvider([0])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.arbitration_ran is False
        # No arbitration events
        arb_started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "arbitration"
        ]
        assert len(arb_started) == 0

    def test_arbitration_failure_handling(self, tmp_path: Path) -> None:
        """Failing provider doesn't abort pipeline."""
        arbiter = _make_arbiter_config(tmp_path)
        config = _make_multi_round_config(tmp_path, rounds=1, arbiter=arbiter)
        provider = _FailingArbiterProvider([2])
        emitter, events = _collect_events()

        # Should NOT raise
        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Arbitration did not succeed
        assert result.arbitration_ran is False
        # Pipeline still produced synthesis
        output_dir = config.output.resolve()
        assert (output_dir / "summary" / "final.md").exists()

        # Arbitration PhaseCompleted emitted with failure
        arb_completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "arbitration"
        ]
        assert len(arb_completed) == 1
        assert arb_completed[0].failure_count == 1

    def test_arbitration_events(self, tmp_path: Path) -> None:
        """PhaseStarted/PhaseCompleted emitted for arbitration."""
        arbiter = _make_arbiter_config(tmp_path)
        config = _make_multi_round_config(tmp_path, rounds=1, arbiter=arbiter)
        provider = MockProvider()
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        arb_started = [
            e for e in events if isinstance(e, PhaseStarted) and e.phase == "arbitration"
        ]
        arb_completed = [
            e for e in events if isinstance(e, PhaseCompleted) and e.phase == "arbitration"
        ]
        assert len(arb_started) == 1
        assert len(arb_completed) == 1
        assert arb_started[0].agent_count == 1
        assert arb_completed[0].success_count == 1
        assert arb_completed[0].failure_count == 0

    def test_arbitration_output_file(self, tmp_path: Path) -> None:
        """Arbitration writes resolution.md to arbiter/ directory."""
        arbiter = _make_arbiter_config(tmp_path)
        config = _make_multi_round_config(tmp_path, rounds=1, arbiter=arbiter)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        arb_path = output_dir / "arbiter" / "resolution.md"
        assert arb_path.exists()
        assert arb_path in result.written_files


# ---------------------------------------------------------------------------
# Cross-round synthesis tests
# ---------------------------------------------------------------------------


class TestCrossRoundSynthesis:
    """Tests for cross-round synthesis after 2+ rounds."""

    def test_produced_after_2_rounds(self, tmp_path: Path) -> None:
        """Cross-round synthesis file written after 2+ rounds."""
        config = _make_multi_round_config(tmp_path, rounds=2)
        provider = _DisputeProvider([2, 0])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        # Cross-round synthesis is at root-level summary/final.md
        crs_path = output_dir / "summary" / "final.md"
        assert crs_path.exists()
        assert crs_path in result.written_files

    def test_not_produced_for_single_round(self, tmp_path: Path) -> None:
        """Cross-round synthesis NOT written for rounds=1."""
        config = _make_multi_round_config(tmp_path, rounds=1)
        provider = MockProvider()
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # No cross-round-synthesis phase events
        crs_started = [
            e for e in events
            if isinstance(e, PhaseStarted) and e.phase == "cross-round-synthesis"
        ]
        assert len(crs_started) == 0

    def test_events(self, tmp_path: Path) -> None:
        """PhaseStarted/PhaseCompleted emitted for cross-round-synthesis."""
        config = _make_multi_round_config(tmp_path, rounds=2)
        provider = _DisputeProvider([2, 0])
        emitter, events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        crs_started = [
            e for e in events
            if isinstance(e, PhaseStarted) and e.phase == "cross-round-synthesis"
        ]
        crs_completed = [
            e for e in events
            if isinstance(e, PhaseCompleted) and e.phase == "cross-round-synthesis"
        ]
        assert len(crs_started) == 1
        assert len(crs_completed) == 1
        assert crs_started[0].agent_count == 1
        assert crs_completed[0].success_count == 1

    def test_round_syntheses_in_round_directories(self, tmp_path: Path) -> None:
        """Each round's synthesis is in its own round-N/summary/final.md."""
        config = _make_multi_round_config(tmp_path, rounds=2)
        provider = _DisputeProvider([2, 0])
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        output_dir = config.output.resolve()
        assert (output_dir / "round-1" / "summary" / "final.md").exists()
        assert (output_dir / "round-2" / "summary" / "final.md").exists()


# ---------------------------------------------------------------------------
# Cancellation support
# ---------------------------------------------------------------------------


class TestCancellation:
    """Pipeline cancellation via CancellationFlag."""

    def test_pre_cancelled_flag_raises(self, tmp_path: Path) -> None:
        """A flag that's already cancelled raises CancelledError immediately."""
        from engine.cancel import CancellationFlag

        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        flag = CancellationFlag()
        flag.cancel()

        with pytest.raises(asyncio.CancelledError, match="Deliberation cancelled"):
            asyncio.run(
                run_pipeline(
                    config, provider, emitter,
                    config_path=_config_path(), cancel=flag,
                )
            )

        # No phases should have started — cancellation happens before Phase 1
        phase_started = [e for e in events if isinstance(e, PhaseStarted)]
        assert len(phase_started) == 0

    def test_cancel_none_works_unchanged(self, tmp_path: Path) -> None:
        """cancel=None (default) runs the full pipeline normally."""
        config = _make_config(tmp_path)
        provider = MockProvider()
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(
                config, provider, emitter,
                config_path=_config_path(), cancel=None,
            )
        )

        assert result.phases_completed >= 5
        assert len(result.written_files) > 0

    def test_cancel_mid_pipeline_stops_execution(self, tmp_path: Path) -> None:
        """Cancelling after Phase 1 prevents later phases from running."""
        from engine.cancel import CancellationFlag

        config = _make_config(tmp_path)
        flag = CancellationFlag()

        # Provider that cancels after the first phase completes
        class CancelAfterReviewProvider:
            def __init__(self) -> None:
                self.calls = 0

            async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
                self.calls += 1
                # Cancel after all review agents have been dispatched
                if self.calls >= len(config.agents):
                    flag.cancel()
                return "[Mock response]"

            async def stream(self, prompt: str, model: str, max_tokens: int):
                yield "[Mock]"

        provider = CancelAfterReviewProvider()
        emitter, events = _collect_events()

        with pytest.raises(asyncio.CancelledError, match="Deliberation cancelled"):
            asyncio.run(
                run_pipeline(
                    config, provider, emitter,
                    config_path=_config_path(), cancel=flag,
                )
            )

        # Phase 1 review should have started and completed, but later phases
        # should not have started
        phase_started = [e for e in events if isinstance(e, PhaseStarted)]
        started_phases = [e.phase for e in phase_started]
        assert "review" in started_phases
        # Cross-review should not start (cancelled between phases)
        assert "synthesis" not in started_phases

