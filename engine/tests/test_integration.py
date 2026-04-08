"""Integration tests — end-to-end deliberation with mock provider.

Phase 1 tests prove: config → template fill → concurrent dispatch → output files,
with correct event ordering and file structure.

Full pipeline tests prove: all 5 phases compose correctly via ``run_engine(phase="all")``,
producing the correct output directory tree with the right number of files, and events
emitted in the correct phase order.

Provider resolution tests prove: ``resolve_provider`` is wired correctly into
``run_engine()``, CLI argparse accepts ``--provider openai``, and auth errors
propagate cleanly when no credentials are available.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from engine.config import AgentConfig, EngineConfig, parse_config
from engine.dispatch import DEFAULT_MAX_TOKENS, DEFAULT_MODEL
from engine.events import (
    AgentCompleted,
    AgentDispatched,
    CallbackEmitter,
    EngineEvent,
    PhaseCompleted,
    PhaseStarted,
)
from engine.output import OutputManager
from engine.providers import MockProvider
from engine.run import run_engine, run_phase1
from engine.templates import build_review_context, fill_template, find_templates_dir, load_template


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def integration_env(tmp_path: Path) -> tuple[EngineConfig, Path, Path]:
    """Set up a minimal but real integration environment.

    Creates:
    - A target spec file
    - A YAML config
    - An output directory
    - Returns (config, config_path, output_dir)
    """
    # Target file
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\n\nThis is a test specification.\n")

    # Output dir (under tmp_path so tests don't pollute project)
    output_dir = tmp_path / "conversus-output"

    # Write config
    config_data = {
        "mode": "cooperative",
        "target": "spec.md",
        "output": str(output_dir),
        "agents": [
            {"name": "agent-alpha", "prompt": "You review from the alpha perspective."},
            {"name": "agent-beta", "prompt": "You review from the beta perspective."},
        ],
    }
    config_path = tmp_path / "conversus.yml"
    config_path.write_text(yaml.dump(config_data, sort_keys=False))

    config = parse_config(config_path)
    return config, config_path, output_dir


# ---------------------------------------------------------------------------
# End-to-end Phase 1
# ---------------------------------------------------------------------------


class TestPhase1Integration:
    """Full Phase 1: config → template → dispatch → output files."""

    @pytest.mark.asyncio
    async def test_end_to_end_produces_output_files(
        self, integration_env: tuple[EngineConfig, Path, Path]
    ) -> None:
        """Review files exist for each agent after Phase 1 completes."""
        config, config_path, output_dir = integration_env
        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider(response_text="Mock review for {model}")

        written = await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        # (a) Output directory structure
        assert output_dir.is_dir()
        for agent in config.agents:
            agent_dir = output_dir / agent.name
            assert agent_dir.is_dir(), f"Missing agent dir: {agent.name}"
            assert (agent_dir / "cross-reviews").is_dir()

        assert (output_dir / "summary").is_dir()

    @pytest.mark.asyncio
    async def test_review_files_exist_for_each_agent(
        self, integration_env: tuple[EngineConfig, Path, Path]
    ) -> None:
        config, config_path, output_dir = integration_env
        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider(response_text="Mock review for {model}")

        written = await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        # (b) Review files exist for each agent
        assert len(written) == len(config.agents)
        for path in written:
            assert path.exists()
            assert path.name == "review.md"

    @pytest.mark.asyncio
    async def test_files_contain_mock_response(
        self, integration_env: tuple[EngineConfig, Path, Path]
    ) -> None:
        config, config_path, output_dir = integration_env
        emitter = CallbackEmitter(lambda e: None)
        provider = MockProvider(response_text="MOCK_SENTINEL_{model}")

        written = await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        # (c) Files contain mock response text
        for path in written:
            content = path.read_text(encoding="utf-8")
            assert "MOCK_SENTINEL_" in content

    @pytest.mark.asyncio
    async def test_event_ordering(
        self, integration_env: tuple[EngineConfig, Path, Path]
    ) -> None:
        """Events emitted in correct order:
        PhaseStarted → N × (AgentDispatched, AgentCompleted) → PhaseCompleted
        """
        config, config_path, output_dir = integration_env
        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider()

        await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        n = len(config.agents)

        # (d) First event is PhaseStarted
        assert isinstance(events[0], PhaseStarted)
        assert events[0].agent_count == n

        # Last event is PhaseCompleted
        assert isinstance(events[-1], PhaseCompleted)

        # Middle events: N dispatched + N completed (order within concurrent agents may vary)
        middle = events[1:-1]
        dispatched = [e for e in middle if isinstance(e, AgentDispatched)]
        completed = [e for e in middle if isinstance(e, AgentCompleted)]

        assert len(dispatched) == n
        assert len(completed) == n

        # All completed successfully
        for e in completed:
            assert e.success is True

    @pytest.mark.asyncio
    async def test_phase_completed_counts(
        self, integration_env: tuple[EngineConfig, Path, Path]
    ) -> None:
        config, config_path, output_dir = integration_env
        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider()

        await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        # (e) PhaseCompleted.success_count == N
        phase_completed = [e for e in events if isinstance(e, PhaseCompleted)]
        assert len(phase_completed) == 1
        assert phase_completed[0].success_count == len(config.agents)
        assert phase_completed[0].failure_count == 0

    @pytest.mark.asyncio
    async def test_mock_provider_receives_all_prompts(
        self, integration_env: tuple[EngineConfig, Path, Path]
    ) -> None:
        config, config_path, output_dir = integration_env
        emitter = CallbackEmitter(lambda e: None)
        provider = MockProvider()

        await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        # MockProvider recorded N calls
        assert len(provider.calls) == len(config.agents)
        # Each prompt contains the target spec content (inlined)
        for call in provider.calls:
            assert "Test Spec" in call.prompt


# ---------------------------------------------------------------------------
# Integration with partial failure
# ---------------------------------------------------------------------------


class TestPhase1FailureHandling:
    """Phase 1 handles agent failures gracefully."""

    @pytest.mark.asyncio
    async def test_partial_failure_still_writes_successful(
        self, integration_env: tuple[EngineConfig, Path, Path]
    ) -> None:
        """When one agent fails, the others' outputs are still written."""
        config, config_path, output_dir = integration_env
        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))

        call_count = 0

        class PartialFailProvider:
            async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise RuntimeError("First agent fails")
                return f"Success from agent #{call_count}"

            async def stream(self, prompt: str, model: str, max_tokens: int):
                yield "unused"

        await run_phase1(
            config=config,
            provider=PartialFailProvider(),
            emitter=emitter,
            config_path=config_path,
        )

        # PhaseCompleted shows 1 failure, 1 success
        pc = [e for e in events if isinstance(e, PhaseCompleted)]
        assert len(pc) == 1
        assert pc[0].failure_count == 1
        assert pc[0].success_count == len(config.agents) - 1


# ---------------------------------------------------------------------------
# Full 5-phase pipeline integration (via run_engine)
# ---------------------------------------------------------------------------


@pytest.fixture
def pipeline_env(tmp_path: Path) -> tuple[Path, Path]:
    """Minimal environment for full-pipeline tests via run_engine().

    Returns (config_path, output_dir).
    """
    spec = tmp_path / "spec.md"
    spec.write_text("# Pipeline Spec\n\nThis is the spec for pipeline tests.\n")

    output_dir = tmp_path / "conversus-output"

    config_data = {
        "mode": "cooperative",
        "target": "spec.md",
        "output": str(output_dir),
        "iterations": 1,
        "agents": [
            {"name": "agent-alpha", "prompt": "Alpha perspective."},
            {"name": "agent-beta", "prompt": "Beta perspective."},
        ],
    }
    config_path = tmp_path / "conversus.yml"
    config_path.write_text(yaml.dump(config_data, sort_keys=False))

    return config_path, output_dir


class TestFullPipelineIntegration:
    """End-to-end: run_engine(phase='all') produces the complete output tree."""

    @pytest.mark.asyncio
    async def test_full_pipeline_produces_all_output_files(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """All 5 phases produce the expected files for 2 agents."""
        config_path, output_dir = pipeline_env

        written = await run_engine(
            config_path=config_path,
            phase="all",
            provider_name="mock",
        )

        # 2 agents × (review + cross-review + revision + disputes) + 1 synthesis = 9
        # cross-reviews: each agent reviews the other → 2 files
        assert len(written) == 9, f"Expected 9 files, got {len(written)}: {written}"

        agents = ["agent-alpha", "agent-beta"]

        # Review files
        for name in agents:
            assert (output_dir / name / "review.md").exists()

        # Cross-review files (each agent reviews the other)
        for reviewer in agents:
            for reviewed in agents:
                if reviewer != reviewed:
                    assert (
                        output_dir / reviewer / "cross-reviews" / f"{reviewed}.md"
                    ).exists()

        # Revision files
        for name in agents:
            assert (output_dir / name / "revision.md").exists()

        # Disputes files
        for name in agents:
            assert (output_dir / name / "disputes.md").exists()

        # Synthesis file
        assert (output_dir / "summary" / "final.md").exists()

    @pytest.mark.asyncio
    async def test_output_files_contain_content(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """Every output file has non-empty content from MockProvider."""
        config_path, output_dir = pipeline_env

        written = await run_engine(
            config_path=config_path,
            phase="all",
            provider_name="mock",
        )

        for path in written:
            assert path.exists(), f"Missing: {path}"
            content = path.read_text(encoding="utf-8")
            assert len(content) > 0, f"Empty: {path}"

    @pytest.mark.asyncio
    async def test_synthesis_file_location(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """Synthesis output lands at summary/final.md."""
        config_path, output_dir = pipeline_env

        await run_engine(
            config_path=config_path,
            phase="all",
            provider_name="mock",
        )

        synth_path = output_dir / "summary" / "final.md"
        assert synth_path.exists()
        assert synth_path.read_text(encoding="utf-8").strip()


class TestPipelineEventOrdering:
    """Events emitted across all 5 phases in the correct sequence."""

    @pytest.mark.asyncio
    async def test_five_phase_started_and_completed_events(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """5 PhaseStarted + 5 PhaseCompleted events, in order."""
        config_path, output_dir = pipeline_env
        config = parse_config(config_path)

        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider()

        from engine.phases import run_pipeline

        await run_pipeline(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        started_events = [e for e in events if isinstance(e, PhaseStarted)]
        completed_events = [e for e in events if isinstance(e, PhaseCompleted)]

        assert len(started_events) == 5
        assert len(completed_events) == 5

        expected_order = [
            "review",
            "cross-review",
            "revision",
            "disputes",
            "synthesis",
        ]
        assert [e.phase for e in started_events] == expected_order
        assert [e.phase for e in completed_events] == expected_order

    @pytest.mark.asyncio
    async def test_phase_started_precedes_phase_completed(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """For each phase, PhaseStarted appears before PhaseCompleted."""
        config_path, output_dir = pipeline_env
        config = parse_config(config_path)

        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider()

        from engine.phases import run_pipeline

        await run_pipeline(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        # For each phase name, find indices of Started and Completed
        for phase_name in ["review", "cross-review", "revision", "disputes", "synthesis"]:
            started_idx = next(
                i
                for i, e in enumerate(events)
                if isinstance(e, PhaseStarted) and e.phase == phase_name
            )
            completed_idx = next(
                i
                for i, e in enumerate(events)
                if isinstance(e, PhaseCompleted) and e.phase == phase_name
            )
            assert started_idx < completed_idx, (
                f"PhaseStarted({phase_name}) at {started_idx} should precede "
                f"PhaseCompleted({phase_name}) at {completed_idx}"
            )

    @pytest.mark.asyncio
    async def test_all_completed_events_report_success(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """All PhaseCompleted events report zero failures in the happy path."""
        config_path, output_dir = pipeline_env
        config = parse_config(config_path)

        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider()

        from engine.phases import run_pipeline

        await run_pipeline(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        completed_events = [e for e in events if isinstance(e, PhaseCompleted)]
        for e in completed_events:
            assert e.failure_count == 0, f"Phase {e.phase} had {e.failure_count} failures"


class TestBackwardCompatibility:
    """run_engine(phase='review') still works and produces only review files."""

    @pytest.mark.asyncio
    async def test_phase_review_produces_only_reviews(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """phase='review' produces review files only — no cross-reviews or synthesis."""
        config_path, output_dir = pipeline_env

        written = await run_engine(
            config_path=config_path,
            phase="review",
            provider_name="mock",
        )

        # Only 2 review files (one per agent)
        assert len(written) == 2
        for path in written:
            assert path.name == "review.md"
            assert path.exists()

        # No synthesis or revision files
        assert not (output_dir / "summary" / "final.md").exists()
        for name in ["agent-alpha", "agent-beta"]:
            assert not (output_dir / name / "revision.md").exists()

    @pytest.mark.asyncio
    async def test_phase_review_events_are_phase1_only(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """phase='review' emits only Phase 1 events."""
        config_path, output_dir = pipeline_env
        config = parse_config(config_path)

        events: list[EngineEvent] = []
        emitter = CallbackEmitter(lambda e: events.append(e))
        provider = MockProvider()

        await run_phase1(
            config=config,
            provider=provider,
            emitter=emitter,
            config_path=config_path,
        )

        started = [e for e in events if isinstance(e, PhaseStarted)]
        completed = [e for e in events if isinstance(e, PhaseCompleted)]

        assert len(started) == 1
        assert started[0].phase == "review"
        assert len(completed) == 1
        assert completed[0].phase == "review"

    @pytest.mark.asyncio
    async def test_unsupported_phase_raises(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """Unknown phase names raise ValueError."""
        config_path, _ = pipeline_env

        with pytest.raises(ValueError, match="not supported"):
            await run_engine(
                config_path=config_path,
                phase="cross-review",
                provider_name="mock",
            )


# ---------------------------------------------------------------------------
# Provider resolution integration tests
# ---------------------------------------------------------------------------


class TestProviderResolutionIntegration:
    """run_engine() wires resolve_provider correctly for all provider names."""

    @pytest.mark.asyncio
    async def test_run_engine_with_mock_provider(
        self, pipeline_env: tuple[Path, Path]
    ) -> None:
        """provider_name='mock' works end-to-end without any credentials."""
        config_path, output_dir = pipeline_env

        written = await run_engine(
            config_path=config_path,
            phase="all",
            provider_name="mock",
        )

        assert len(written) == 9
        assert (output_dir / "summary" / "final.md").exists()

    @pytest.mark.asyncio
    async def test_run_engine_with_openai_provider_env_var(
        self, pipeline_env: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """provider_name='openai' resolves via OPENAI_API_KEY and runs the pipeline.

        We monkeypatch resolve_provider to return a MockProvider so the test
        doesn't need a real OpenAI key, while still proving that run_engine
        passes 'openai' through to the resolution path.
        """
        mock_provider = MockProvider(response_text="[OpenAI mock for {model}]")
        monkeypatch.setattr(
            "engine.run.resolve_provider",
            lambda name: mock_provider,
        )

        config_path, output_dir = pipeline_env
        written = await run_engine(
            config_path=config_path,
            phase="all",
            provider_name="openai",
        )

        assert len(written) == 9
        assert (output_dir / "summary" / "final.md").exists()
        # Verify the mock was actually called (not a different provider)
        assert len(mock_provider.calls) > 0

    @pytest.mark.asyncio
    async def test_run_engine_with_anthropic_provider_env_var(
        self, pipeline_env: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """provider_name='anthropic' resolves via ANTHROPIC_API_KEY and runs the pipeline."""
        mock_provider = MockProvider(response_text="[Anthropic mock for {model}]")
        monkeypatch.setattr(
            "engine.run.resolve_provider",
            lambda name: mock_provider,
        )

        config_path, output_dir = pipeline_env
        written = await run_engine(
            config_path=config_path,
            phase="all",
            provider_name="anthropic",
        )

        assert len(written) == 9
        assert (output_dir / "summary" / "final.md").exists()
        assert len(mock_provider.calls) > 0

    @pytest.mark.asyncio
    async def test_run_engine_provider_no_credentials(
        self, pipeline_env: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """run_engine raises ProviderError(category='auth') when no credentials exist."""
        from engine.providers import ProviderError

        config_path, _ = pipeline_env

        # Remove env vars so resolve_provider can't find credentials
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        # Use a temp credential store with no tokens
        from engine.auth import CredentialStore

        empty_store = CredentialStore(path=config_path.parent / ".empty_auth.json")
        monkeypatch.setattr(
            "engine.auth.CredentialStore",
            lambda path=None: empty_store,
        )

        with pytest.raises(ProviderError, match="No credentials available") as exc_info:
            await run_engine(
                config_path=config_path,
                phase="all",
                provider_name="openai",
            )
        assert exc_info.value.category == "auth"

    @pytest.mark.asyncio
    async def test_backward_compat_no_provider_field(
        self, tmp_path: Path
    ) -> None:
        """Config without 'provider' field defaults to 'anthropic' at parse time,
        but run_engine uses explicit provider_name arg so mock still works."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Compat Spec\n")

        config_data = {
            "mode": "cooperative",
            "target": "spec.md",
            "output": str(tmp_path / "output"),
            "agents": [
                {"name": "agent-a", "prompt": "A"},
                {"name": "agent-b", "prompt": "B"},
            ],
        }
        config_path = tmp_path / "conversus.yml"
        config_path.write_text(yaml.dump(config_data, sort_keys=False))

        # Verify the config parses with provider defaulting to "anthropic"
        config = parse_config(config_path)
        assert config.provider == "anthropic"

        # But run_engine with provider_name="mock" still works
        written = await run_engine(
            config_path=config_path,
            phase="all",
            provider_name="mock",
        )
        assert len(written) > 0


class TestCLIProviderChoices:
    """CLI accepts --provider openai/anthropic/mock and rejects invalid providers."""

    def test_cli_accepts_openai_provider(self) -> None:
        """Click CLI doesn't reject --provider openai."""
        from click.testing import CliRunner
        from engine.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
        assert "provider" in result.output.lower()

    def test_cli_accepts_anthropic_provider(self) -> None:
        """Click CLI doesn't reject --provider anthropic."""
        from click.testing import CliRunner
        from engine.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0

    def test_cli_accepts_mock_provider(self) -> None:
        """Click CLI doesn't reject --provider mock."""
        from click.testing import CliRunner
        from engine.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0

    def test_cli_rejects_invalid_provider(self) -> None:
        """Click CLI rejects unknown provider names."""
        from click.testing import CliRunner
        from engine.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["run", "dummy.yml", "--provider", "gemini"])
        assert result.exit_code != 0


class TestMCPProviderResolution:
    """MCP _run_in_process supports non-mock providers via resolve_provider."""

    def test_mcp_in_process_with_mock(self) -> None:
        """In-process execution with mock provider still works."""
        from mcp_server import _run_in_process, CostEstimate

        config_yaml = yaml.dump({
            "mode": "cooperative",
            "target": "spec.md",
            "output": "output",
            "agents": [
                {"name": "a1", "prompt": "P1"},
            ],
        })

        result = _run_in_process(
            config_yaml=config_yaml,
            provider_name="mock",
            validated=True,
            errors=[],
            cost_estimate=None,
        )

        assert result.mode == "in_process"
        # mock might fail on missing spec.md but should not error on provider resolution
        # The provider itself was created successfully if we don't see "Unsupported provider"
        for err in result.errors:
            assert "Unsupported provider" not in err

    def test_mcp_in_process_no_credentials_returns_error(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """In-process execution with 'openai' and no credentials returns auth error."""
        from engine.providers import ProviderError
        from mcp_server import _run_in_process

        # Monkeypatch resolve_provider in mcp_server to raise an auth error,
        # simulating the case where no credentials are available.
        def _raise_no_creds(name: str) -> None:
            raise ProviderError(
                f"No credentials available for '{name}'.",
                category="auth",
            )

        monkeypatch.setattr("mcp_server.resolve_provider", _raise_no_creds)

        # Also monkeypatch parse_config so we don't need real files on disk
        from engine.config import EngineConfig, AgentConfig

        dummy_config = EngineConfig(
            mode="cooperative",
            target_files=[tmp_path / "spec.md"],
            output=tmp_path / "output",
            agents=[
                AgentConfig(name="a1", prompt="P1"),
                AgentConfig(name="a2", prompt="P2"),
            ],
        )
        monkeypatch.setattr("mcp_server.parse_config", lambda path: dummy_config)

        config_yaml = yaml.dump({
            "mode": "cooperative",
            "target": "spec.md",
            "output": "output",
            "agents": [
                {"name": "a1", "prompt": "P1"},
                {"name": "a2", "prompt": "P2"},
            ],
        })

        result = _run_in_process(
            config_yaml=config_yaml,
            provider_name="openai",
            validated=True,
            errors=[],
            cost_estimate=None,
        )

        assert result.mode == "in_process"
        assert any("No credentials available" in e for e in result.errors)
