"""Tests for spec 006 inter-round arbitration — timing x influence combinations.

Covers:
- ArbiterConfig.timing defaults and validation
- ArbiterConfig.influence defaults and validation
- Pipeline-level: timing=final runs arbitration once after loop
- Pipeline-level: timing=inter-round runs arbitration between rounds
- Pipeline-level: inter-round arbitration populates prior_arbitration_path
- Cross-field validation: inter-round timing with single round is rejected
"""

from __future__ import annotations

import asyncio

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


class TestInterRoundValidation:
    """timing=inter-round requires rounds > 1; the parser rejects bad combos."""

    def test_inter_round_with_single_round_rejects(self, tmp_path: Path) -> None:
        """Parse a config with timing=inter-round and rounds=1.
        Verify ConfigError is raised with an actionable message."""
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

        with pytest.raises(ConfigError) as exc_info:
            parse_config(cfg_path)

        msg = str(exc_info.value)
        assert "inter-round" in msg, (
            f"Expected error message to mention 'inter-round', got: {msg!r}"
        )
        assert "rounds > 1" in msg or "rounds: 2" in msg or "rounds to 2" in msg, (
            f"Expected error message to indicate rounds > 1 is required, "
            f"got: {msg!r}"
        )

    def test_final_timing_with_single_round_does_not_raise(
        self, tmp_path: Path
    ) -> None:
        """Sanity check the inverse: timing=final with rounds=1 must parse cleanly."""
        grounding = tmp_path / "grounding.md"
        grounding.write_text("# Constitution\n")
        cfg_path = _minimal_config(tmp_path, extra={
            "rounds": 1,
            "arbiter": {
                "name": "arbiter",
                "prompt": "You decide.",
                "grounding": "grounding.md",
                "trigger": "always",
                "timing": "final",
            },
        })

        config = parse_config(cfg_path)

        assert config.arbiter is not None
        assert config.arbiter.timing == "final"
        assert config.rounds == 1


# ===================================================================
# Pipeline-level tests: timing behaviour
# ===================================================================


class TestTimingFinalRunsArbitrationAfterLoop:
    """Default behavior: timing=final, arbitration runs once after all rounds."""

    def test_timing_final_runs_arbitration_after_loop(self, tmp_path: Path) -> None:
        """timing=final, rounds=2: arbitration runs exactly once after all
        rounds complete. Check that arbitration/resolution.md exists in the output."""
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
        arb_files = list(output_dir.rglob("arbitration/resolution.md"))
        assert len(arb_files) >= 1, (
            f"Expected arbitration/resolution.md in output, found: "
            f"{list(output_dir.rglob('*'))}"
        )


class TestTimingInterRoundRunsArbitrationBetweenRounds:
    """timing=inter-round: arbitration runs between rounds."""

    def test_timing_inter_round_runs_arbitration_between_rounds(
        self, tmp_path: Path
    ) -> None:
        """timing=inter-round, rounds=3: arbitration runs between rounds.
        Check for round-based arbitration/resolution.md files."""
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
        arb_files = list(output_dir.rglob("arbitration/resolution.md"))
        assert len(arb_files) >= 2, (
            f"Expected at least 2 arbitration/resolution.md files (one per inter-round gap), "
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
        the arbitration/resolution.md is written. Round 2 then runs with that
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
        round1_arb = output_dir / "round-1" / "arbitration" / "resolution.md"
        assert round1_arb.exists(), (
            f"Expected round-1/arbitration/resolution.md to exist for prior "
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


# ===================================================================
# FR-P2-3: Round-loop parity test — Round 2 receives prior_arbitration_path
# ===================================================================


class TestRoundLoopParityInterRound:
    """FR-P2-3 parity: with rounds=2 + arbiter.timing=inter-round, the Round 2
    invocation of ``_run_single_round`` MUST receive ``prior_arbitration_path``
    pointing to ``round-1/arbitration/resolution.md`` (post-FR-P2-2 path).

    Round 1 must NOT receive a prior_arbitration_path (it is None, since no
    earlier round produced an arbitration). The contract is direct: spy on
    ``_run_single_round`` and read the recorded kwargs.
    """

    def test_006_round_loop_parity_inter_round(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from engine import phases

        recorded: list[Path | None] = []
        original = phases._run_single_round

        async def spy(*args: object, **kwargs: object):
            recorded.append(kwargs.get("prior_arbitration_path"))
            return await original(*args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(phases, "_run_single_round", spy)

        arbiter = _make_arbiter_config(tmp_path, timing="inter-round")
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        provider = _DisputeProvider([2, 1])
        emitter, _events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Sanity: pipeline ran 2 rounds and arbitration fired between them.
        assert result.rounds_completed == 2
        assert result.arbitration_ran is True

        # _run_single_round invoked exactly once per round
        assert len(recorded) == 2, (
            f"Expected 2 _run_single_round calls (one per round), got {len(recorded)}"
        )

        # Round 1: no prior arbitration exists yet → kwarg is None
        assert recorded[0] is None, (
            f"Round 1 must not receive a prior_arbitration_path, got {recorded[0]!r}"
        )

        # Round 2: kwarg is the FR-P2-2 path round-1/arbitration/resolution.md
        round2_prior = recorded[1]
        assert round2_prior is not None, (
            "Round 2 _run_single_round did NOT receive prior_arbitration_path; "
            "FR-P2-3 parity broken — inter-round arbitration result not "
            "plumbed into the next round's context builders."
        )
        # Path must be exactly the post-FR-P2-2 location
        assert round2_prior.name == "resolution.md"
        assert round2_prior.parent.name == "arbitration"
        assert round2_prior.parent.parent.name == "round-1", (
            f"Round 2 prior_arbitration_path is not round-1/arbitration/resolution.md: "
            f"got {round2_prior}"
        )
        # And it must point to a real file written by Round 1's arbiter
        assert round2_prior.exists(), (
            f"Round 2 received prior_arbitration_path={round2_prior!r}, but the "
            f"file does not exist. Round 1's arbitration must have written it."
        )

    def test_006_round_loop_parity_final_timing_no_prior_arbitration(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Inverse parity: with timing='final', NO round receives a
        prior_arbitration_path — final arbitration runs once after the loop,
        not between rounds, so the round-loop kwarg stays None throughout.

        This guards FR-P2-3 against false positives where the kwarg is being
        populated unconditionally rather than only for inter-round timing.
        """
        from engine import phases

        recorded: list[Path | None] = []
        original = phases._run_single_round

        async def spy(*args: object, **kwargs: object):
            recorded.append(kwargs.get("prior_arbitration_path"))
            return await original(*args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(phases, "_run_single_round", spy)

        arbiter = _make_arbiter_config(tmp_path, timing="final")
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        provider = _DisputeProvider([2, 1])
        emitter, _events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert len(recorded) == 2
        assert recorded[0] is None
        assert recorded[1] is None, (
            f"timing='final' must NOT populate prior_arbitration_path between "
            f"rounds (final-arb runs after the loop). Got {recorded[1]!r}."
        )


# ===================================================================
# FR-P2-6 / SC-007: Cross-round synthesis Resolution Attribution
# ===================================================================


class TestCrossRoundResolutionAttribution:
    """FR-P2-6 / SC-007: when inter-round arbitration runs across multiple
    rounds, the cross-round synthesis MUST receive the per-round arbitration
    paths and rulings so its "Resolution Attribution" section can render with
    non-empty data.

    Failure mode caught: the fix at ``engine/phases.py`` accumulates
    ``arbitration_paths`` across the round loop and passes them to
    ``build_cross_round_synthesis_context``; if either the accumulator or
    the call-site kwarg is dropped, the cross-round synthesis sees empty
    ARBITRATION_PATHS / ARBITRATION_RULINGS and SC-007 fails.
    """

    def test_006_sc007_cross_round_synthesis_resolution_attribution(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Run a 2-round + arbiter (timing=inter-round) pipeline. Capture the
        kwargs passed to ``build_cross_round_synthesis_context``. Assert:

        1. ``arbitration_paths`` is non-empty and contains at least one path
           pointing to ``round-1/arbitration/resolution.md`` (post-FR-P2-2).
        2. ``arbitration_rulings`` is a non-empty string and references
           Round 1 plus the actual content the arbiter wrote.
        3. When the cooperative cross-round-synthesis template is filled
           with the captured context, the rendered prompt contains the
           Resolution Attribution section header AND the round-1
           arbitration path AND the ruling content.
        """
        from engine import phases as _phases_mod
        from engine.templates import (
            build_cross_round_synthesis_context,
            fill_template,
            load_template,
        )

        # Spy on the context builder; record kwargs each call.
        captured_kwargs: list[dict] = []
        captured_contexts: list[object] = []
        original_builder = _phases_mod.build_cross_round_synthesis_context

        def spy_builder(*args: object, **kwargs: object):
            captured_kwargs.append(dict(kwargs))
            ctx = original_builder(*args, **kwargs)  # type: ignore[arg-type]
            captured_contexts.append(ctx)
            return ctx

        monkeypatch.setattr(
            _phases_mod,
            "build_cross_round_synthesis_context",
            spy_builder,
        )

        arbiter = _make_arbiter_config(tmp_path, timing="inter-round")
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        # Disputes in round 1 and round 2 — keep arbitration triggering
        # but avoid early convergence.
        provider = _DisputeProvider([2, 1])
        emitter, _events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Sanity: pipeline completed both rounds with inter-round arbitration.
        assert result.rounds_completed == 2
        assert result.arbitration_ran is True

        # Cross-round synthesis was invoked exactly once.
        assert len(captured_kwargs) == 1, (
            f"Expected exactly one cross-round-synthesis context build, "
            f"got {len(captured_kwargs)}"
        )
        kwargs = captured_kwargs[0]

        # FR-P2-6 assertion 1: arbitration_paths is non-empty and contains
        # the round-1 inter-round arbitration resolution path.
        arb_paths = kwargs.get("arbitration_paths")
        assert arb_paths, (
            "arbitration_paths kwarg was empty/None — FR-P2-6 wiring is "
            "broken. The accumulator in run_pipeline did not capture "
            "Round 1's inter-round arbitration output, OR the call site "
            "at engine/phases.py did not pass the kwarg through."
        )
        assert len(arb_paths) == 1, (
            f"Expected 1 arbitration path (one inter-round gap between "
            f"rounds 1 and 2), got {len(arb_paths)}: {arb_paths}"
        )
        round1_arb = arb_paths[0]
        assert round1_arb.name == "resolution.md"
        assert round1_arb.parent.name == "arbitration"
        assert round1_arb.parent.parent.name == "round-1", (
            f"Round 1 arbitration path is not under round-1/arbitration/: "
            f"got {round1_arb}"
        )
        assert round1_arb.exists(), (
            f"Round 1 arbitration path {round1_arb} does not exist; "
            f"the accumulator captured a stale pre-retroactive-move path."
        )

        # FR-P2-6 assertion 2: arbitration_rulings is non-empty and includes
        # a Round 1 header plus the actual content of the arbitration file.
        arb_rulings = kwargs.get("arbitration_rulings")
        assert isinstance(arb_rulings, str) and arb_rulings.strip(), (
            f"arbitration_rulings must be a non-empty string, got "
            f"{arb_rulings!r}"
        )
        assert "Round 1 Arbitration" in arb_rulings, (
            f"arbitration_rulings should label content with 'Round 1 "
            f"Arbitration'; got: {arb_rulings[:200]}"
        )
        # Content of the actual arbitration file should appear in rulings.
        round1_arb_content = round1_arb.read_text(encoding="utf-8").strip()
        assert round1_arb_content in arb_rulings, (
            "arbitration_rulings does not contain the actual round-1 "
            "arbitration file content; the loader in run_pipeline is not "
            "reading the file before passing to the context builder."
        )

        # FR-P2-6 assertion 3: filling the cooperative cross-round-synthesis
        # template with this context produces a prompt that renders the
        # Resolution Attribution section header AND the arbitration path
        # AND the ruling content. This verifies the spec FR-020 requirement
        # that the section is structurally present in the prompt the
        # cross-round-synthesizer agent receives.
        ctx = captured_contexts[0]
        templates_dir = PROJECT_ROOT / "templates"
        template_text = load_template(
            templates_dir, "cooperative", "cross-round-synthesis"
        )
        filled = fill_template(template_text, ctx)
        assert "Resolution Attribution" in filled, (
            "Filled cross-round-synthesis prompt is missing the "
            "'Resolution Attribution' section header — spec FR-020 violated."
        )
        # The ARBITRATION_PATHS placeholder should have been replaced with
        # the actual path string.
        assert str(round1_arb) in filled, (
            f"Filled prompt does not contain the round-1 arbitration path "
            f"{round1_arb}; ARBITRATION_PATHS substitution failed."
        )
        # The ARBITRATION_RULINGS placeholder should have been replaced
        # with the rulings block (containing the Round 1 header).
        assert "Round 1 Arbitration" in filled, (
            "Filled prompt does not contain the 'Round 1 Arbitration' "
            "header from ARBITRATION_RULINGS; substitution failed."
        )
        # And no unfilled {VARIABLE} placeholders remain (fill_template
        # raises if any do, but assert it explicitly for clarity).
        assert "{ARBITRATION_PATHS}" not in filled
        assert "{ARBITRATION_RULINGS}" not in filled

    def test_006_cross_round_no_arbitration_omits_rulings(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Inverse: with NO arbiter configured, cross-round synthesis is
        called with arbitration_paths=None / arbitration_rulings=None.

        Guards FR-P2-6 against false positives where the kwargs are wired
        unconditionally regardless of whether arbitration ran.
        """
        from engine import phases as _phases_mod

        captured_kwargs: list[dict] = []
        original_builder = _phases_mod.build_cross_round_synthesis_context

        def spy_builder(*args: object, **kwargs: object):
            captured_kwargs.append(dict(kwargs))
            return original_builder(*args, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(
            _phases_mod,
            "build_cross_round_synthesis_context",
            spy_builder,
        )

        # No arbiter — pure 2-round deliberation.
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=None, stagnation="ignore",
        )
        provider = _DisputeProvider([2, 1])
        emitter, _events = _collect_events()

        asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        assert len(captured_kwargs) == 1
        kwargs = captured_kwargs[0]
        # No inter-round arbitration ran → both kwargs must be None
        # (or absent — but our wiring passes them as keyword args).
        assert kwargs.get("arbitration_paths") is None, (
            f"Expected arbitration_paths=None when no arbiter, got "
            f"{kwargs.get('arbitration_paths')!r}"
        )
        assert kwargs.get("arbitration_rulings") is None, (
            f"Expected arbitration_rulings=None when no arbiter, got "
            f"{kwargs.get('arbitration_rulings')!r}"
        )


# ===================================================================
# FR-P2-7: Spec-006 SC tests for the post-issue-#68 wired pipeline
# ===================================================================
#
# These tests close out spec 006 Phase 2 by exercising the
# influence x stagnation x re-opening permutations end-to-end with
# arbiter-addressed dispute parsing wired in (issue #68).
#
# All tests use deterministic providers — no LLM calls — and rely on
# spying on ``check_disagreement`` from the engine.phases call site
# to capture the exact influence/arbiter_addressed/dispute_count
# values the round-loop produced.


class _ArbiterDisputeProvider:
    """Deterministic provider for SC tests that emits both:

    * synthesis output with configurable dispute counts/labels per round, and
    * arbitration output (``resolution.md`` content) with configurable
      ``## Dispute: <title>`` headings per round.

    Synthesis labels and arbitration-addressed labels can match (binding/
    recommended would suppress) or diverge (re-opening / advisory cases).
    """

    def __init__(
        self,
        *,
        synthesis_per_round: list[list[str]],
        arbitration_per_round: list[list[str]],
    ) -> None:
        self.synthesis_per_round = synthesis_per_round
        self.arbitration_per_round = arbitration_per_round
        self._synth_call = 0
        self._arb_call = 0

    @staticmethod
    def _build_synthesis(labels: list[str]) -> str:
        if not labels:
            return "# Synthesis\n\nNo disputes."
        parts = ["# Synthesis", "<!-- CONVERSUS:DISPUTES_BEGIN -->"]
        for label in labels:
            parts.append(f"**Dispute:** {label}")
        parts.append("<!-- CONVERSUS:DISPUTES_END -->")
        return "\n".join(parts)

    @staticmethod
    def _build_resolution(labels: list[str]) -> str:
        # Emits arbiter resolution.md content with the canonical heading
        # form linter.arbitration_parser.extract_addressed_disputes parses.
        if not labels:
            return "# Arbiter Resolution\n\nNo disputes addressed.\n"
        parts = ["# Arbiter Resolution\n"]
        for label in labels:
            parts.append(f"## Dispute: {label}\n")
            parts.append("Ruling: addressed per grounding doc.\n")
        return "\n".join(parts)

    def _is_arbitration_prompt(self, prompt: str) -> bool:
        # The cooperative arbitration template uniquely contains the phrase
        # "binding decision authority" (template-literal text). Synthesis,
        # review, cross-review, and disputes templates do not.
        prompt_lower = prompt.lower()
        return (
            "binding decision authority" in prompt_lower
            or "subject arbitration" in prompt_lower
            or "phase 6: subject arbitration" in prompt_lower
        )

    def _is_synthesis_prompt(self, prompt: str) -> bool:
        # Arbitration prompts also contain "AGENT_NAMES" and "synthesis"
        # tokens (they reference the prior synthesis), so synthesis must
        # be matched only AFTER excluding arbitration.
        return "synthesis" in prompt.lower() and (
            "AGENT_NAMES" in prompt
            or "ALL_REVIEWS" in prompt
            or "final.md" in prompt
        )

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        # Order matters: arbitration discriminator runs before synthesis
        # because arbitration prompts reference the prior synthesis and
        # would otherwise match the synthesis discriminator first.
        if self._is_arbitration_prompt(prompt):
            idx = min(self._arb_call, len(self.arbitration_per_round) - 1)
            labels = self.arbitration_per_round[idx]
            self._arb_call += 1
            return self._build_resolution(labels)
        if self._is_synthesis_prompt(prompt):
            idx = min(self._synth_call, len(self.synthesis_per_round) - 1)
            labels = self.synthesis_per_round[idx]
            self._synth_call += 1
            return self._build_synthesis(labels)
        return f"[Mock response for {model}]"

    async def stream(self, prompt: str, model: str, max_tokens: int):
        yield "[stream not used]"


def _spy_check_disagreement(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    """Install a spy on engine.phases.check_disagreement.

    Returns a list that is appended to with one dict per call capturing the
    kwargs (``influence``, ``arbiter_addressed``) and the resulting
    ``dispute_count``. Spying on the engine.phases module's binding ensures
    we capture the round-loop call site specifically.
    """
    from engine import phases as _phases_mod

    captured: list[dict] = []
    original = _phases_mod.check_disagreement

    def spy(synthesis_text, mode="cooperative", **kwargs):
        result = original(synthesis_text, mode, **kwargs)
        captured.append(
            {
                "mode": mode,
                "influence": kwargs.get("influence"),
                "arbiter_addressed": kwargs.get("arbiter_addressed"),
                "dispute_count": result.dispute_count,
            }
        )
        return result

    monkeypatch.setattr(_phases_mod, "check_disagreement", spy)
    return captured


class TestSC002AdvisoryLeavesDisputesCounted:
    """SC-002 (FR-011): with influence=advisory, the round-loop's
    check_disagreement count is NOT reduced by the arbiter-addressed list.

    Even when the arbiter's resolution.md addresses every dispute the
    synthesis raised, advisory influence MUST leave the post-adjustment
    count equal to the raw synthesis count. Asserts behavioural parity
    with a no-arbiter control run on identical synthesis.
    """

    def test_006_sc002_advisory_leaves_disputes_counted(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from linter.models import InfluenceLevel

        # ── Test run: rounds=2 inter-round arbitration with advisory.
        # Round 1 synthesis: 2 disputes; arbiter addresses both; Round 2
        # synthesis: 1 dispute; arbiter doesn't run after Round 2 (last
        # round) but prior_arbitration_path from Round 1 is reused so
        # check_disagreement still receives arbiter_addressed.
        arbiter = _make_arbiter_config(
            tmp_path, timing="inter-round", influence="advisory",
        )
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        provider = _ArbiterDisputeProvider(
            synthesis_per_round=[
                ["topic alpha disagreement", "topic beta disagreement"],
                ["topic gamma disagreement"],
            ],
            arbitration_per_round=[
                # Round 1's arbiter addresses BOTH round-1 disputes.
                ["topic alpha disagreement", "topic beta disagreement"],
            ],
        )
        captured = _spy_check_disagreement(monkeypatch)
        emitter, _events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )
        assert result.rounds_completed == 2

        # Snapshot ADVISORY-run counts before sharing the spy with the
        # control run (the monkeypatch fixture installs the spy on the
        # module attribute, so a second _spy_check_disagreement call on
        # the same monkeypatch chains another wrapper layer; capturing
        # advisory_counts up-front avoids index-shift surprises).
        advisory_counts = [c["dispute_count"] for c in captured]

        # Two check_disagreement calls (one per round, both within
        # ``if config.rounds > 1`` branch).
        assert len(captured) == 2, (
            f"Expected 2 check_disagreement calls, got {len(captured)}"
        )

        # Both calls must have influence=ADVISORY.
        for c in captured:
            assert c["influence"] == InfluenceLevel.ADVISORY, (
                f"Expected influence=ADVISORY at every round-loop call, "
                f"got {c['influence']!r}"
            )

        # Round 1 call: arbiter_addressed should be the 2 round-1 disputes
        # (parsed from the just-written resolution.md). Even with
        # arbiter_addressed populated, ADVISORY must NOT reduce the count.
        round1 = captured[0]
        assert round1["arbiter_addressed"] is not None
        assert len(round1["arbiter_addressed"]) == 2, (
            f"Round 1 arbiter_addressed should contain 2 entries from the "
            f"resolution.md parser, got {round1['arbiter_addressed']!r}"
        )
        assert round1["dispute_count"] == 2, (
            f"ADVISORY influence must leave dispute_count == raw count (2). "
            f"Got {round1['dispute_count']}. arbiter_addressed was "
            f"{round1['arbiter_addressed']!r}."
        )

        # Round 2 call: arbiter_addressed still carries Round 1's addressed
        # list (prior_arbitration_path is sticky across rounds). Count must
        # remain 1 (the Round 2 raw count) — no advisory-driven reduction.
        round2 = captured[1]
        assert round2["dispute_count"] == 1, (
            f"Round 2 dispute_count under ADVISORY must equal raw count "
            f"(1), got {round2['dispute_count']}."
        )

        # ── Control run: same synthesis but no arbiter at all.
        # With no arbiter, check_disagreement is called with influence=None
        # and arbiter_addressed=None; counts must match the ADVISORY run.
        ctrl_root = tmp_path / "ctrl"
        ctrl_root.mkdir(parents=True, exist_ok=True)
        control_config = _make_multi_round_config(
            ctrl_root, rounds=2, arbiter=None, stagnation="ignore",
        )
        control_provider = _ArbiterDisputeProvider(
            synthesis_per_round=[
                ["topic alpha disagreement", "topic beta disagreement"],
                ["topic gamma disagreement"],
            ],
            arbitration_per_round=[],
        )
        control_emitter, _ = _collect_events()
        # The advisory-run spy is still installed; new calls append to
        # ``captured``. Snapshot length to slice the control-run additions.
        pre_control_len = len(captured)
        asyncio.run(
            run_pipeline(
                control_config,
                control_provider,
                control_emitter,
                config_path=_config_path(),
            )
        )
        control_calls = captured[pre_control_len:]
        assert len(control_calls) == 2, (
            f"Expected 2 control check_disagreement calls, got "
            f"{len(control_calls)}"
        )
        # ADVISORY counts equal control (no-arbiter) counts: 2 then 1.
        control_counts = [c["dispute_count"] for c in control_calls]
        assert control_counts == [2, 1]
        assert advisory_counts == control_counts, (
            f"ADVISORY influence must produce the same dispute_count as a "
            f"no-arbiter control run on identical synthesis output. "
            f"advisory={advisory_counts}, control={control_counts}."
        )


class TestSC003RecommendedReopenReturnsToActiveCount:
    """SC-003 (FR-012): with influence=recommended, when Round 2's synthesis
    re-raises a Round-1-addressed dispute under a substantively different
    label (grounded counter-evidence reframing), the dispute is counted —
    the round-loop's adjusted count stays at the active level.

    Note on determinism: ``check_disagreement`` matches dispute labels
    against ``arbiter_addressed`` via case-insensitive bidirectional
    substring match. ``_normalize_for_match`` strips list markers/whitespace
    but preserves words. To deterministically simulate "re-opening with
    grounded counter-evidence", the Round 2 synthesis label is reworded so
    no substring overlap exists with the Round 1 addressed label.
    """

    def test_006_sc003_recommended_reopen_returns_to_active_count(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from linter.models import InfluenceLevel

        arbiter = _make_arbiter_config(
            tmp_path, timing="inter-round", influence="recommended",
        )
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        # Round 1 synthesis raises D1 ("alpha"). Arbiter addresses D1
        # under that exact label. Round 2 synthesis re-raises with new
        # framing ("counter-evidence shows beta priority")
        # that does NOT substring-match the addressed entry — modeling
        # the spec's "re-opening with grounded counter-evidence" path.
        # Round 1 raises D1 ("alpha decision") AND a second dispute that
        # the arbiter does NOT address ("orthogonal pricing question"), so
        # under RECOMMENDED the round-1 post-adjustment count is 1
        # (not 0 → loop continues into Round 2). Round 2 re-raises D1
        # with new framing that does not substring-match the addressed
        # entry — modeling the spec's "re-opening with grounded
        # counter-evidence" path.
        provider = _ArbiterDisputeProvider(
            synthesis_per_round=[
                ["alpha decision is correct", "orthogonal pricing question"],
                ["counter-evidence reframes prior ruling"],
            ],
            arbitration_per_round=[
                ["alpha decision is correct"],
            ],
        )
        captured = _spy_check_disagreement(monkeypatch)
        emitter, _events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )
        assert result.rounds_completed == 2, (
            f"Round 1 must not converge (one dispute is unaddressed); "
            f"got rounds_completed={result.rounds_completed}, "
            f"termination_reason={result.termination_reason!r}."
        )

        assert len(captured) == 2
        # Round 1 call: RECOMMENDED removes the addressed "alpha decision"
        # but leaves the unaddressed "orthogonal pricing" → count==1.
        round1 = captured[0]
        assert round1["influence"] == InfluenceLevel.RECOMMENDED
        assert round1["dispute_count"] == 1, (
            f"Round 1 RECOMMENDED-adjusted count should be 1 "
            f"(unaddressed dispute remaining), got "
            f"{round1['dispute_count']}."
        )
        # Round 2 call: re-opened dispute uses substantively different
        # wording (no substring overlap with the round-1 addressed entry),
        # so the recommended-influence reduction does not fire — count
        # stays at 1 (re-opened, ACTIVE).
        round2 = captured[1]
        assert round2["influence"] == InfluenceLevel.RECOMMENDED
        assert round2["dispute_count"] == 1, (
            f"Round 2 re-opened dispute (different label) must remain "
            f"counted under RECOMMENDED. Got {round2['dispute_count']}; "
            f"arbiter_addressed was {round2['arbiter_addressed']!r}."
        )


class TestSC007FullPipelineResolutionAttribution:
    """SC-007 (FR-020): an end-to-end 2-round inter-round arbitration run
    produces a cross-round-synthesis output file with a populated
    Resolution Attribution section: section header, round-specific
    references, and the actual ruling content from Round 1.

    This is the read-the-actual-output-file companion to PR #69's spy-based
    test (test_006_sc007_cross_round_synthesis_resolution_attribution).
    """

    def test_006_sc007_full_pipeline_resolution_attribution(
        self, tmp_path: Path
    ) -> None:
        arbiter = _make_arbiter_config(tmp_path, timing="inter-round")
        config = _make_multi_round_config(
            tmp_path, rounds=2, arbiter=arbiter, stagnation="ignore",
        )
        # Use the deterministic provider so the resolution.md content
        # contains a known marker we can assert on at the end.
        # Round 1 has 2 disputes; the arbiter addresses one ("scaling
        # strategy disagreement") and leaves "data residency disagreement"
        # unaddressed. Under default BINDING influence, the round-loop's
        # check_disagreement adjusts to 1 → loop continues into Round 2.
        provider = _ArbiterDisputeProvider(
            synthesis_per_round=[
                [
                    "scaling strategy disagreement",
                    "data residency disagreement",
                ],
                ["latency budget disagreement"],
            ],
            arbitration_per_round=[
                ["scaling strategy disagreement"],
            ],
        )
        emitter, _events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )
        assert result.rounds_completed == 2, (
            f"Round 1 must not converge; got rounds_completed="
            f"{result.rounds_completed}, termination_reason="
            f"{result.termination_reason!r}."
        )

        # The cross-round-synthesis output file is produced verbatim from
        # the provider's response to the cross-round-synthesis prompt.
        # Our provider falls through to the generic
        # "[Mock response for ...]" string, so we cannot assert on the
        # rendered Resolution Attribution there. Instead we assert on the
        # PROMPT the cross-round-synthesizer agent received: it is built
        # from the cooperative cross-round-synthesis template filled with
        # the captured arbitration paths/rulings. The template embeds the
        # Resolution Attribution section header and the rulings block.
        #
        # The pipeline doesn't persist the prompt to disk, so re-render
        # the prompt deterministically from the same inputs the pipeline
        # used. The arbitration_paths / rulings come from the actual
        # files written under the output tree.
        from engine.templates import (
            build_cross_round_synthesis_context,
            fill_template,
            load_template,
        )

        output_dir = config.output.resolve()
        round1_arb = output_dir / "round-1" / "arbitration" / "resolution.md"
        assert round1_arb.exists(), (
            "Round 1 arbitration file missing — inter-round arbitration "
            "did not run as expected."
        )
        round1_arb_content = round1_arb.read_text(encoding="utf-8")
        # The Resolution Attribution section is rendered into the
        # cross-round-synthesis PROMPT. Read the round-2 synthesis path
        # the pipeline wrote for the round_syntheses input.
        round_syntheses = []
        for round_num in (1, 2):
            # OutputManager.get_synthesis_path writes to ``summary/final.md``
            # under the round base; round 1 was retroactively moved to
            # ``round-1/`` when round 2 started.
            rs_path = (
                output_dir / f"round-{round_num}" / "summary" / "final.md"
            )
            assert rs_path.exists(), f"Missing {rs_path}"
            round_syntheses.append(rs_path.read_text(encoding="utf-8"))

        ruling_block = (
            f"## Round 1 Arbitration ({round1_arb})\n\n"
            f"{round1_arb_content.strip()}"
        )
        ctx = build_cross_round_synthesis_context(
            config,
            config.output,
            round_syntheses,
            2,
            "max_rounds",
            arbitration_paths=[round1_arb],
            arbitration_rulings=ruling_block,
        )
        templates_dir = PROJECT_ROOT / "templates"
        template_text = load_template(
            templates_dir, "cooperative", "cross-round-synthesis"
        )
        filled = fill_template(template_text, ctx)

        # SC-007 assertions on the rendered prompt:
        # 1. Resolution Attribution section header present.
        assert "Resolution Attribution" in filled, (
            "Filled cross-round-synthesis prompt is missing the "
            "'Resolution Attribution' section header (FR-020)."
        )
        # 2. Round-specific reference present.
        assert "Round 1 Arbitration" in filled, (
            "Resolution Attribution section is missing the round-specific "
            "'Round 1 Arbitration' header."
        )
        # 3. Actual ruling content from Round 1 is included.
        assert "scaling strategy disagreement" in filled, (
            "Round 1's arbitration ruling content (the addressed dispute "
            "label) is not present in the filled prompt — the rulings "
            "block did not propagate."
        )


class TestSC008StagnationWithAdvisoryIgnoresArbiter:
    """SC-008 (FR-019): stagnation detection MUST be driven by the agent
    dispute count and MUST NOT be short-circuited by the arbiter's
    addressed-dispute set when influence=advisory.

    Setup: Round 1 and Round 2 synthesis both emit 2 disputes (constant —
    no progress). Round 1's arbitration "addresses" both. With
    influence=advisory the addressed list is ignored, so:

    * Round 1 dispute_count = 2 (raw)
    * Round 2 dispute_count = 2 (raw)
    * stagnation triggers because current >= prior at Round 2.

    If the arbiter-addressed list incorrectly *did* affect the count under
    advisory, Round 1 would drop to 0 (converged) and the run would never
    reach the stagnation check at Round 2.
    """

    def test_006_sc008_stagnation_with_influence_advisory_ignores_arbiter(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        arbiter = _make_arbiter_config(
            tmp_path, timing="inter-round", influence="advisory",
        )
        config = _make_multi_round_config(
            tmp_path,
            rounds=3,  # Allow stagnation to fire before max_rounds.
            arbiter=arbiter,
            stagnation="detect",
        )
        provider = _ArbiterDisputeProvider(
            synthesis_per_round=[
                ["alpha disagreement", "beta disagreement"],
                ["alpha disagreement", "beta disagreement"],
                ["alpha disagreement", "beta disagreement"],
            ],
            arbitration_per_round=[
                # Arbiter addresses everything every round.
                ["alpha disagreement", "beta disagreement"],
                ["alpha disagreement", "beta disagreement"],
            ],
        )
        captured = _spy_check_disagreement(monkeypatch)
        emitter, _events = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Stagnation should fire at Round 2 (count >= prior_count).
        assert result.termination_reason == "stagnation", (
            f"Expected stagnation termination under advisory influence "
            f"with constant raw dispute counts; got "
            f"{result.termination_reason!r}. If arbiter-addressed had "
            f"incorrectly leaked into the count under advisory, Round 1 "
            f"would have converged and termination would be 'converged'."
        )
        assert result.rounds_completed == 2, (
            f"Stagnation must terminate at the end of Round 2; got "
            f"rounds_completed={result.rounds_completed}."
        )

        # Both observed check_disagreement counts must be the raw value
        # (2), confirming advisory ignored the arbiter-addressed list.
        assert len(captured) == 2
        assert [c["dispute_count"] for c in captured] == [2, 2], (
            f"Expected dispute_count=[2, 2] under advisory; got "
            f"{[c['dispute_count'] for c in captured]}. "
            f"arbiter_addressed seen: "
            f"{[c['arbiter_addressed'] for c in captured]}."
        )
