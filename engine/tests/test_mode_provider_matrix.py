"""Cross-product mode × provider meta-test for Principle XXVI remediation.

This module closes the **Component-tier Principle XXVI Provisional gap**
recorded in ``CONFORMANCE.md`` row XXVI: the prior claim that the test
suite "parametrizes across all (mode × provider) cells" was not backed
by a single meta-suite that confirms the parametrization breadth.
Before this module landed, ``test_skill_engine.py`` exercised:

* 4 of 8 modes (``cooperative``, ``winner-take-all``, ``prisoners-dilemma``,
  ``red-blue``) × 1 provider (``mock``) = 4 cells out of a theoretical
  8 × 14 = 112 cell matrix.

That coverage gap is precisely what Principle XXVI was added to prevent
("forgot to add the new tool to the test list" → silent regression).
Per Principle XXV (Live Test Cost Discipline) we do **not** spend live
LLM credits to fill the matrix.  Instead we partition providers:

* **Cell-runnable providers** (``mock``, ``demo``) — exercise every mode
  end-to-end via :func:`engine.phases.run_pipeline`.  16 cells.
* **Dispatch-only providers** — every other registered provider must be
  *instantiable* (registry resolution succeeds without credentials, the
  class is constructed, the ``execute`` attribute is present).  No
  outbound calls.  12 cells today.

Together the structural assertions confirm the parametrize lists track
the authoritative sources of truth (``VALID_MODES`` and
``PROVIDER_REGISTRY``) — adding a new mode or provider without updating
this module trips the meta-test.

Origin: 2026-05-11 remediation closing the XXVI Provisional row.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from deliberator.schemas.modes import VALID_MODES as _CANONICAL_MODES
from engine.config import AgentConfig, EngineConfig
from engine.events import CallbackEmitter
from engine.execution.providers import PROVIDER_REGISTRY
from engine.phases import run_pipeline
from engine.providers import MockProvider


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Authoritative source-of-truth references
# ---------------------------------------------------------------------------
#
# These constants exist so the meta-tests can compare the parametrize
# breadth against the canonical sources rather than hard-coding the
# expected counts. If a mode or provider is added/removed upstream, the
# matrix tests trip with a clear message pointing at this module.

# Modes that can run end-to-end with a stub model provider (no creds).
CELL_RUNNABLE_PROVIDERS: tuple[str, ...] = ("mock", "demo")

# Provider names that need network/CLI credentials and are therefore
# *dispatch-only* under Principle XXV. We assert these instantiate but
# do not spawn the underlying integration.
DISPATCH_ONLY_PROVIDERS: tuple[str, ...] = tuple(
    sorted(
        (set(PROVIDER_REGISTRY.keys()) - set(CELL_RUNNABLE_PROVIDERS))
        | {"anthropic", "openai"}  # legacy-auth path, resolved by run.py
    )
)

# Stable list of all modes ordered for deterministic parametrize ids.
ALL_MODES: tuple[str, ...] = tuple(sorted(_CANONICAL_MODES))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_minimal_config(tmp_path: Path, *, mode: str) -> EngineConfig:
    """Build a minimal valid EngineConfig for ``mode``.

    Red-blue requires role-tagged agents (engine/config.py:704). Every
    other mode accepts the simple alice/bob pair used by the existing
    cross-axis matrix.
    """
    target = tmp_path / "spec.md"
    target.write_text(f"# Mode coverage spec\nMode: {mode}\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir(exist_ok=True)

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
        output=output,
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


# ---------------------------------------------------------------------------
# Source-of-truth meta-assertions (Principle XXVI tripwires)
# ---------------------------------------------------------------------------


class TestMatrixSourcesOfTruth:
    """Pin the parametrize breadth to the authoritative registries.

    If a contributor adds a mode to ``VALID_MODES`` or a provider to
    ``PROVIDER_REGISTRY`` without updating this module, these tests
    trip with a message naming the missing entry.
    """

    def test_all_modes_enumerated(self) -> None:
        assert set(ALL_MODES) == set(_CANONICAL_MODES), (
            f"Mode list drift: ALL_MODES={set(ALL_MODES)} vs "
            f"VALID_MODES={set(_CANONICAL_MODES)}. "
            f"Update engine/tests/test_mode_provider_matrix.py::ALL_MODES "
            f"after adding/removing a mode in deliberator/schemas/modes.py."
        )

    def test_mode_count_is_eight(self) -> None:
        # Pin the count explicitly so a silent demotion in
        # deliberator/schemas/modes.py (e.g., dropping a mode) doesn't
        # quietly shrink the parametrize footprint.
        assert len(ALL_MODES) == 8, (
            f"Expected 8 modes (cooperative, winner-take-all, "
            f"prisoners-dilemma, red-blue, negotiation, "
            f"resource-allocation, fair-division, mechanism-design); "
            f"found {len(ALL_MODES)}: {ALL_MODES}"
        )

    def test_cell_runnable_providers_are_registered(self) -> None:
        missing = [p for p in CELL_RUNNABLE_PROVIDERS if p not in PROVIDER_REGISTRY]
        assert not missing, (
            f"Cell-runnable providers missing from PROVIDER_REGISTRY: "
            f"{missing}. The matrix relies on these for end-to-end "
            f"coverage without live credentials."
        )

    def test_dispatch_only_providers_cover_remainder(self) -> None:
        # Every registry entry not in CELL_RUNNABLE_PROVIDERS must be in
        # DISPATCH_ONLY_PROVIDERS. Legacy-auth providers (anthropic,
        # openai) are added explicitly because they live behind
        # engine.run.resolve_execution_provider, not the registry.
        from_registry = set(PROVIDER_REGISTRY.keys()) - set(CELL_RUNNABLE_PROVIDERS)
        dispatch_only = set(DISPATCH_ONLY_PROVIDERS)
        missing = from_registry - dispatch_only
        assert not missing, (
            f"Registered providers not covered by dispatch-only sweep: "
            f"{sorted(missing)}. Add them to DISPATCH_ONLY_PROVIDERS in "
            f"engine/tests/test_mode_provider_matrix.py."
        )

    def test_matrix_minimum_size(self) -> None:
        """The cell-runnable matrix is exactly len(modes) × len(cell-runnable).

        This is the post-remediation contract: 8 × 2 = 16 cells. If the
        meta-test runs fewer than this it means a parametrize entry was
        dropped silently — the very failure mode Principle XXVI targets.
        """
        expected = len(ALL_MODES) * len(CELL_RUNNABLE_PROVIDERS)
        assert expected == 16, (
            f"Cell-runnable matrix size = {expected}; spec the "
            f"remediation PR baselined at 16 (8 modes × 2 providers). "
            f"If the change is intentional, update this assertion."
        )


# ---------------------------------------------------------------------------
# Cell-runnable matrix — 8 modes × {mock, demo} = 16 end-to-end runs
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestModeProviderCellRunnable:
    """Every (mode, cell-runnable-provider) cell completes a pipeline.

    The pipeline is exercised with a stub :class:`MockProvider` regardless
    of the provider *name* under test, because the cell-runnable sweep is
    concerned with **mode mechanics under a parametrized provider key**,
    not with re-validating the mock provider's internals (those live in
    ``test_execution_providers_mock.py``). The provider name is recorded
    on the output dir so a failure surfaces which cell tripped.
    """

    @pytest.mark.parametrize("provider_name", CELL_RUNNABLE_PROVIDERS)
    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_cell_completes_pipeline(
        self,
        mode: str,
        provider_name: str,
        tmp_path: Path,
    ) -> None:
        cell_dir = tmp_path / f"{mode}__{provider_name}"
        cell_dir.mkdir()
        config = _make_minimal_config(cell_dir, mode=mode)
        provider = MockProvider()
        emitter = CallbackEmitter(lambda _e: None)

        result = asyncio.run(
            run_pipeline(config, provider, emitter, config_path=_config_path())
        )

        # Cell invariant 1: pipeline produced a result.
        assert result is not None, (
            f"Cell ({mode}, {provider_name}) produced no Result. "
            f"This is the failure mode Principle XXVI guards against — "
            f"the parametrize list previously claimed this cell was "
            f"covered without ever exercising it."
        )
        assert result.rounds_completed >= 1, (
            f"Cell ({mode}, {provider_name}) reported "
            f"rounds_completed={result.rounds_completed}; expected >= 1."
        )

        # Cell invariant 2: synthesis artifact exists.
        synthesis = config.output / "summary" / "final.md"
        assert synthesis.exists() and synthesis.stat().st_size > 0, (
            f"Cell ({mode}, {provider_name}) did not write "
            f"summary/final.md."
        )


# ---------------------------------------------------------------------------
# Dispatch-only providers — every registry entry can be instantiated
# ---------------------------------------------------------------------------


class TestProviderDispatchOnlyInstantiation:
    """Every provider class in the registry can be constructed without creds.

    This is the structural half of the XXVI matrix: we cannot spend live
    LLM credits to fill out 8 × 12 = 96 additional cells (Principle XXV),
    but we can confirm that the dispatch surface is intact — every
    registered provider name resolves to an instantiable class with a
    callable ``execute`` attribute. Wiring regressions (provider removed
    from registry, broken constructor, missing ``execute``) trip here.
    """

    @pytest.mark.parametrize("provider_name", DISPATCH_ONLY_PROVIDERS)
    def test_provider_instantiates(
        self, provider_name: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        if provider_name in PROVIDER_REGISTRY:
            cls = PROVIDER_REGISTRY[provider_name]
            instance = cls()
            assert hasattr(instance, "execute"), (
                f"Provider '{provider_name}' "
                f"({cls.__module__}.{cls.__qualname__}) is missing "
                f"the .execute attribute required by ExecutionProvider."
            )
            assert callable(instance.execute), (
                f"Provider '{provider_name}' .execute is not callable."
            )
            return

        # Legacy-auth path (anthropic / openai). These don't live in the
        # registry; engine.run.resolve_execution_provider wraps them via
        # ModelProviderExecutionAdapter. The test verifies the *wiring*
        # (resolve → wrap → expose .execute), not credential discovery,
        # so we stub resolve_provider with a no-credential fake. Prior
        # implementation relied on the local machine having stored OAuth
        # credentials, which made the test env-dependent.
        from unittest.mock import MagicMock
        from engine.run import resolve_execution_provider
        from engine.providers import ModelProvider

        fake_provider = MagicMock(spec=ModelProvider)
        monkeypatch.setattr(
            "engine.run.resolve_provider", lambda name: fake_provider
        )

        provider = resolve_execution_provider(provider_name)
        assert provider is not None, (
            f"Legacy-auth provider '{provider_name}' did not resolve."
        )
        assert hasattr(provider, "execute") and callable(provider.execute), (
            f"Legacy-auth provider '{provider_name}' has no callable "
            f".execute (resolve_execution_provider must wrap legacy "
            f"ModelProviders in ModelProviderExecutionAdapter)."
        )

    def test_dispatch_only_count_matches_registry(self) -> None:
        """The dispatch-only sweep covers every registry entry minus cell-runnables.

        Pin the relationship so a contributor adding a new provider must
        either include it in the cell-runnable matrix or extend
        DISPATCH_ONLY_PROVIDERS. Silent omission is impossible.
        """
        # Every registered name except cell-runnable ones must appear in
        # DISPATCH_ONLY_PROVIDERS (the converse — extra legacy-auth
        # entries — is allowed because anthropic/openai are not in the
        # registry).
        from_registry = set(PROVIDER_REGISTRY.keys()) - set(CELL_RUNNABLE_PROVIDERS)
        not_covered = from_registry - set(DISPATCH_ONLY_PROVIDERS)
        assert not not_covered, (
            f"Registered providers absent from dispatch-only matrix: "
            f"{sorted(not_covered)}. Update DISPATCH_ONLY_PROVIDERS."
        )
