"""Tests for spec 006 inter-round arbitration — timing x influence combinations.

Covers:
- ArbiterConfig.timing defaults and validation
- ArbiterConfig.influence defaults and validation
- Pipeline-level: timing=final runs arbitration once after loop
- Pipeline-level: timing=inter-round runs arbitration between rounds
- Pipeline-level: inter-round arbitration populates prior_arbitration_path
- Cross-field warning: inter-round timing with single round
"""

from __future__ import annotations

import asyncio
import logging

import pytest

pytestmark = pytest.mark.integration
from pathlib import Path

import pytest
import yaml

from engine.config import (
    ArbiterConfig,
    AgentConfig,
    ConfigError,
    EngineConfig,
    parse_config,
)
from engine.events import (
    CallbackEmitter,
    EngineEvent,
    PhaseCompleted,
    PhaseStarted,
)
from engine.phases import PipelineResult, run_pipeline
from engine.providers import MockProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _config_path() -> Path:
    """Return the path to the example config for template discovery."""
    return PROJECT_ROOT / "conversus.example.yml"


def _collect_events() -> tuple[CallbackEmitter, list[EngineEvent]]:
    """Create a CallbackEmitter that records all events to a list."""
    events: list[EngineEvent] = []
    emitter = CallbackEmitter(lambda e: events.append(e))
    return emitter, events


def _write_yaml(path: Path, data: dict) -> Path:
    """Write a YAML dict to *path* and return the path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, sort_keys=False), encoding="utf-8")
    return path


def _minimal_config(
    tmp_path: Path,
    *,
    mode: str = "cooperative",
    agents: list[dict] | None = None,
    extra: dict | None = None,
) -> Path:
    """Write a minimal valid config with a real target file."""
    target = tmp_path / "target.md"
    target.write_text("# Target spec\n", encoding="utf-8")

    data: dict = {
        "mode": mode,
        "target": "target.md",
        "output": "out/",
        "agents": agents or [
            {"name": "agent-a", "prompt": "You are agent A."},
            {"name": "agent-b", "prompt": "You are agent B."},
        ],
    }
    if extra:
        data.update(extra)

    return _write_yaml(tmp_path / "conversus.yml", data)


def _make_arbiter_config(
    tmp_path: Path,
    *,
    timing: str = "final",
    influence: str = "binding",
    trigger: str = "always",
) -> ArbiterConfig:
    """Create an ArbiterConfig for testing with spec-006 fields."""
    grounding = tmp_path / "grounding.md"
    grounding.write_text("Arbitration grounding.", encoding="utf-8")
    return ArbiterConfig(
        name="arbiter",
        prompt="You are the arbiter.",
        docs=[],
        grounding=grounding,
        trigger=trigger,
        timing=timing,
        influence=influence,
    )


def _make_multi_round_config(
    tmp_path: Path,
    *,
    agent_names: list[str] | None = None,
    iterations: int = 1,
    rounds: int = 2,
    stagnation: str = "ignore",
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

    # If arbiter specified, ensure grounding file exists
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


class _DisputeProvider:
    """MockProvider that returns synthesis with configurable dispute counts.

    Synthesis phase responses contain dispute markers; all other phases
    return generic responses.  ``dispute_counts`` is a list of counts --
    one per round.  If the list is exhausted, repeats the last count.
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
        if (
            "synthesis" in prompt.lower()
            and ("AGENT_NAMES" in prompt or "ALL_REVIEWS" in prompt or "final.md" in prompt)
        ):
            idx = min(self._synth_call, len(self.dispute_counts) - 1)
            count = self.dispute_counts[idx]
            self._synth_call += 1
            return self._make_disputes(count)
        return f"[Mock response for {model}]"

    async def stream(self, prompt: str, model: str, max_tokens: int):
        yield "[stream not used]"


# ===================================================================
# Config-level tests: defaults and validation
# ===================================================================


class TestTimingDefault:
    """ArbiterConfig.timing defaults to 'final'."""

    def test_timing_final_is_default(self, tmp_path: Path) -> None:
        """Parse a config with an arbiter but no timing field.
        Verify config.arbiter.timing == 'final'."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "always",
                # timing omitted — should default to "final"
            }
        })
        config = parse_config(cfg_path)
        assert config.arbiter is not None
        assert config.arbiter.timing == "final"


class TestInfluenceDefault:
    """ArbiterConfig.influence defaults to 'binding'."""

    def test_influence_binding_is_default(self, tmp_path: Path) -> None:
        """Parse a config with an arbiter but no influence field.
        Verify config.arbiter.influence == 'binding'."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "always",
                # influence omitted — should default to "binding"
            }
        })
        config = parse_config(cfg_path)
        assert config.arbiter is not None
        assert config.arbiter.influence == "binding"


class TestInfluenceFieldParsed:
    """All three influence values parse correctly."""

    @pytest.mark.parametrize("influence", ["binding", "recommended", "advisory"])
    def test_influence_values(self, influence: str, tmp_path: Path) -> None:
        """Parse configs with each influence value and verify all three parse."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "always",
                "influence": influence,
            }
        })
        config = parse_config(cfg_path)
        assert config.arbiter is not None
        assert config.arbiter.influence == influence


class TestInvalidTiming:
    """Invalid timing value raises ConfigError."""

    def test_invalid_timing_raises(self, tmp_path: Path) -> None:
        """Parse a config with timing: 'invalid'. Verify ConfigError is raised."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "always",
                "timing": "invalid",
            }
        })
        with pytest.raises(ConfigError, match="timing"):
            parse_config(cfg_path)


class TestInvalidInfluence:
    """Invalid influence value raises ConfigError."""

    def test_invalid_influence_raises(self, tmp_path: Path) -> None:
        """Parse a config with influence: 'invalid'. Verify ConfigError is raised."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "always",
                "influence": "invalid",
            }
        })
        with pytest.raises(ConfigError, match="influence"):
            parse_config(cfg_path)


class TestInterRoundWithSingleRoundWarns:
    """timing=inter-round with rounds=1 logs a warning."""

    def test_inter_round_timing_with_single_round_warns(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Parse a config with timing=inter-round and rounds=1.
        Verify a warning is logged."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "rounds": 1,
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "always",
                "timing": "inter-round",
            },
        })
        with caplog.at_level(logging.WARNING, logger="engine.config"):
            config = parse_config(cfg_path)

        assert config.arbiter is not None
        assert config.arbiter.timing == "inter-round"
        # Verify the warning was logged
        warning_messages = [
            r.message for r in caplog.records if r.levelno >= logging.WARNING
        ]
        assert any("inter-round" in msg for msg in warning_messages), (
            f"Expected warning about inter-round timing with single round, "
            f"got: {warning_messages}"
        )


# ===================================================================
# Pipeline-level tests: timing behaviour
# ===================================================================


class TestTimingFinalRunsArbitrationAfterLoop:
    """Default behavior: timing=final, arbitration runs once after all rounds."""

    def test_timing_final_runs_arbitration_after_loop(self, tmp_path: Path) -> None:
        """timing=final, rounds=2: arbitration runs exactly once after all
        rounds complete. Check that arbiter/resolution.md exists in the output."""
        arbiter = _make_arbiter_config(tmp_path, timing="final")
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        # Disputes remain across both rounds so the pipeline runs both,
        # then arbitration fires after the loop.
        provider = _DisputeProvider([2, 1])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Arbitration ran
        assert result.arbitration_ran is True

        # Exactly one arbitration phase start/complete (post-loop)
        arb_started = [
            e for e in events
            if isinstance(e, PhaseStarted) and e.phase == "arbitration"
        ]
        arb_completed = [
            e for e in events
            if isinstance(e, PhaseCompleted) and e.phase == "arbitration"
        ]
        assert len(arb_started) == 1
        assert len(arb_completed) == 1
        assert arb_completed[0].success_count == 1

        # resolution.md exists in the output
        output_dir = config.output.resolve()
        # For multi-round final arbitration, resolution is at the last round's base
        arb_files = list(output_dir.rglob("arbiter/resolution.md"))
        assert len(arb_files) >= 1, (
            f"Expected arbiter/resolution.md in output, found: "
            f"{list(output_dir.rglob('*'))}"
        )


class TestTimingInterRoundRunsArbitrationBetweenRounds:
    """timing=inter-round: arbitration runs between rounds."""

    def test_timing_inter_round_runs_arbitration_between_rounds(
        self, tmp_path: Path
    ) -> None:
        """timing=inter-round, rounds=3: arbitration runs between rounds.
        Check for round-based arbiter/resolution.md files."""
        arbiter = _make_arbiter_config(tmp_path, timing="inter-round")
        config = _make_multi_round_config(
            tmp_path, rounds=3, arbiter=arbiter, stagnation="ignore",
        )
        # Disputes decrease each round but never reach 0
        provider = _DisputeProvider([3, 2, 1])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Inter-round arbitration should have run between rounds (after round 1
        # and after round 2, but NOT after round 3 — per the code's guard).
        arb_started = [
            e for e in events
            if isinstance(e, PhaseStarted) and e.phase == "arbitration"
        ]
        assert len(arb_started) == 2, (
            f"Expected 2 inter-round arbitration phases (between 3 rounds), "
            f"got {len(arb_started)}"
        )

        # Arbitration ran
        assert result.arbitration_ran is True

        # Verify resolution files exist in round directories
        output_dir = config.output.resolve()
        arb_files = list(output_dir.rglob("arbiter/resolution.md"))
        assert len(arb_files) >= 2, (
            f"Expected at least 2 arbiter/resolution.md files (one per inter-round gap), "
            f"found: {arb_files}"
        )


class TestInterRoundPopulatesPriorArbitrationPath:
    """timing=inter-round: round 2's agents get prior arbitration context."""

    def test_timing_inter_round_populates_prior_arbitration_path(
        self, tmp_path: Path
    ) -> None:
        """timing=inter-round, rounds=2: verify that round 2's agent reviews
        have access to prior arbitration context by checking that the
        prior_arbitration_path was passed through.

        We verify this indirectly: after round 1's inter-round arbitration,
        the arbiter/resolution.md is written. Round 2 then runs with that
        path available. We check the arbitration file from round 1 exists
        and that the pipeline completes successfully with both rounds."""
        arbiter = _make_arbiter_config(tmp_path, timing="inter-round")
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        # Disputes in round 1, fewer in round 2
        provider = _DisputeProvider([2, 1])
        emitter, events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert result.rounds_completed == 2
        assert result.arbitration_ran is True

        # Round 1's arbitration was produced (this is the prior_arbitration_path
        # that gets fed into round 2)
        output_dir = config.output.resolve()
        round1_arb = output_dir / "round-1" / "arbiter" / "resolution.md"
        assert round1_arb.exists(), (
            f"Expected round-1/arbiter/resolution.md to exist for prior "
            f"arbitration context, but it does not. "
            f"Output tree: {list(output_dir.rglob('*'))}"
        )

        # Arbitration event happened exactly once (only between round 1 and 2;
        # inter-round does NOT fire after the last round)
        arb_started = [
            e for e in events
            if isinstance(e, PhaseStarted) and e.phase == "arbitration"
        ]
        assert len(arb_started) == 1

        # Round 2 still completed (showing prior arb path was consumed without error)
        review_events = [
            e for e in events
            if isinstance(e, PhaseStarted) and e.phase == "review"
        ]
        # Two review phases — one per round
        assert len(review_events) == 2
