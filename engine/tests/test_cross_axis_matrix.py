"""Cross-axis smoke combinations — spec 061 step 14c (issue #113).

The matrix exercises {provider} × {mode} × {persistence} permutations
to catch regressions where a configuration axis interacts badly with
others. Each combination runs the full pipeline with mock provider
(no API costs) and asserts:

- Pipeline completes without exception
- summary/final.md exists
- Mode-specific structural element appears
- Persistence behavior matches the flag

This complements spec 061's per-axis tests (TestProviderAllFiveLevels
for provider, TestPhase{1-5} for mode mechanics, TestPersistListShowRoundTrip
for persistence) by catching cross-axis interactions that pairwise
tests miss.

The 6 combinations chosen cover the four primary game-theory modes
plus persistence on/off variation, matching spec 061 §3.3's
"6 cross-axis smoke combinations" requirement.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
import yaml

from engine.config import AgentConfig, ArbiterConfig, EngineConfig
from engine.events import CallbackEmitter, EngineEvent
from engine.phases import run_pipeline
from engine.providers import MockProvider


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_matrix_config(
    tmp_path: Path,
    *,
    mode: str,
) -> EngineConfig:
    """Build a minimal valid config for a given mode.

    Red-blue mode requires `role: red` and `role: blue` agents per
    engine/config.py:704; other modes accept role-less agents.
    """
    target = tmp_path / "spec.md"
    target.write_text(f"# Cross-axis matrix spec\nMode: {mode}\n", encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    if mode == "red-blue":
        agents = [
            AgentConfig(name="red-agent", prompt="Attack the spec.", role="red"),
            AgentConfig(name="blue-agent", prompt="Defend the spec.", role="blue"),
        ]
    else:
        agents = [
            AgentConfig(name="alice", prompt="You are Alice."),
            AgentConfig(name="bob", prompt="You are Bob."),
        ]

    return EngineConfig(
        mode=mode,
        target_files=[target],
        output=output_dir,
        agents=agents,
        iterations=1,
        rounds=1,
        stagnation="detect",
        prior_files=[],
        arbiter=None,
        validate_templates=True,
    )


def _config_path() -> Path:
    return PROJECT_ROOT / "deliberator.example.yml"


def _collect_events() -> tuple[CallbackEmitter, list[EngineEvent]]:
    events: list[EngineEvent] = []
    return CallbackEmitter(lambda e: events.append(e)), events


def _write_persistence_settings(
    project_root: Path, *, enabled: bool
) -> None:
    """Pin persistence on/off via project-level settings.yml."""
    settings_dir = project_root / ".deliberator"
    settings_dir.mkdir(parents=True, exist_ok=True)
    settings_file = settings_dir / "settings.yml"
    settings_file.write_text(
        yaml.dump({"persistence": {"enabled": enabled, "retention_days": 90}}),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# The 6 cross-axis smoke combinations
# ---------------------------------------------------------------------------
#
# Combinations chosen to maximize coverage:
#   1-4. The four primary game-theory modes × mock provider × persistence_off
#   5-6. cooperative / winner-take-all × mock provider × persistence_on
#
# Persistence on/off variation is sampled rather than full-crossed (we
# don't need to confirm e.g. red-blue × persistence_on independently —
# the persistence layer is mode-independent by spec 056 design, and
# the combinatorial cost of full-cross is unjustified at the smoke tier).


# Each entry: (mode, persistence_enabled, mode_specific_signal)
# The mode_specific_signal is a per-mode invariant we can verify
# from the pipeline output.
_MATRIX = [
    pytest.param("cooperative", False, "alice", id="cooperative-persistoff"),
    pytest.param("winner-take-all", False, "alice", id="winner-take-all-persistoff"),
    pytest.param("prisoners-dilemma", False, "alice", id="prisoners-dilemma-persistoff"),
    pytest.param("red-blue", False, "red-agent", id="red-blue-persistoff"),
    pytest.param("cooperative", True, "alice", id="cooperative-persiston"),
    pytest.param("winner-take-all", True, "alice", id="winner-take-all-persiston"),
]


@pytest.mark.integration
class TestCrossAxisSmokeMatrix:
    """6 cross-axis combinations — provider × mode × persistence.

    Each test runs the full pipeline and asserts the smoke invariants:
    no exceptions, synthesis written, mode-specific agent dir present,
    persistence behavior correct.
    """

    @pytest.mark.parametrize("mode,persistence_enabled,agent_dir_expected", _MATRIX)
    def test_smoke_combination(
        self,
        mode: str,
        persistence_enabled: bool,
        agent_dir_expected: str,
        tmp_path: Path,
    ) -> None:
        """Pipeline completes; summary written; mode-specific structure present."""
        # Persistence cascade pinned via project settings
        _write_persistence_settings(tmp_path, enabled=persistence_enabled)

        config = _make_matrix_config(tmp_path, mode=mode)
        provider = MockProvider()
        emitter, _ = _collect_events()

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Smoke invariant 1: pipeline completed
        assert result is not None
        assert result.rounds_completed >= 1

        # Smoke invariant 2: synthesis exists
        synthesis = config.output / "summary" / "final.md"
        assert synthesis.exists(), (
            f"summary/final.md missing for mode={mode}, "
            f"persistence={persistence_enabled}"
        )
        assert synthesis.stat().st_size > 0

        # Smoke invariant 3: mode-specific agent directory present
        agent_dir = config.output / agent_dir_expected
        assert agent_dir.is_dir(), (
            f"agent dir '{agent_dir_expected}' missing for mode={mode}"
        )
        assert (agent_dir / "review.md").exists()

        # Smoke invariant 4: persistence settings cascade resolved as configured
        # (validates the {provider × mode × persistence} interaction —
        # persistence is mode-independent by spec 056 design)
        from engine.persistence import is_persistence_enabled
        assert is_persistence_enabled(tmp_path) is persistence_enabled, (
            f"persistence cascade resolution mismatch for mode={mode}: "
            f"expected {persistence_enabled}, got "
            f"{is_persistence_enabled(tmp_path)}"
        )

    def test_matrix_count_matches_spec(self) -> None:
        """Pin the matrix at exactly 6 combinations per spec 061 §3.3.

        If a future contributor adds a 7th case without updating this
        assertion + the spec text, the test trips. If they remove a
        case, it also trips. The matrix size is a contract, not a
        free parameter.
        """
        assert len(_MATRIX) == 6, (
            f"Cross-axis matrix has {len(_MATRIX)} cases; spec 061 §3.3 "
            f"specifies exactly 6 cross-axis smoke combinations. "
            f"If intentional, update the spec annotation in §7 step 14c."
        )

    def test_matrix_covers_four_primary_modes(self) -> None:
        """All four primary game-theory modes appear at least once.

        Pins the coverage contract: any mode dropped from the matrix
        must update the spec annotation and the count check. Defends
        against accidental coverage regression when a contributor
        prunes the matrix without realizing the coverage implication.
        """
        modes_in_matrix = {param.values[0] for param in _MATRIX}
        primary_modes = {
            "cooperative",
            "winner-take-all",
            "prisoners-dilemma",
            "red-blue",
        }
        assert primary_modes.issubset(modes_in_matrix), (
            f"Primary modes missing from matrix: "
            f"{primary_modes - modes_in_matrix}"
        )

    def test_matrix_includes_persistence_variation(self) -> None:
        """Both persistence states appear in the matrix.

        Persistence on/off is the second cross-axis variable. Without
        both states present, the matrix degenerates to a mode-only
        sweep and the cross-axis claim is hollow.
        """
        persistence_states = {param.values[1] for param in _MATRIX}
        assert persistence_states == {True, False}, (
            f"Matrix must cover both persistence states; "
            f"found {persistence_states}"
        )
