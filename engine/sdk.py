"""Typed programmatic Python API for conversus.

Provides the public SDK surface for CI/CD pipelines, custom tooling, and
programmatic composition of multi-agent deliberations.

Public API:
    Deliberation   — async orchestrator: configure → subscribe to events → run
    Result         — frozen Pydantic model wrapping pipeline output + metadata
    ValidateResult — frozen Pydantic model for config validation + cost estimate
    validate()     — validate config without running (returns ValidateResult)
    classify()     — classify question sufficiency (delegates to question_classifier)

Usage:
    from engine import Deliberation, Result, validate

    # Config-path mode
    result = await Deliberation(config_path=Path("conversus.yml")).run()
    print(result.headline)

    # Ad-hoc question mode
    result = await Deliberation(
        question="Should we use Postgres or SQLite?",
        provider="mock",
    ).run()

    # Validation without execution
    vr = validate(Path("conversus.yml"))
    if not vr.valid:
        print(vr.errors)
"""

from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable

import yaml

from engine.auth import resolve_provider
from engine.config import ConfigError, EngineConfig, parse_config
from engine.cost import estimate_cost
from engine.events import (
    CallbackEmitter,
    EngineEvent,
    NullEmitter,
)
from engine.phases import PipelineError, run_pipeline
from engine.providers import ProviderError
from linter.output_contract import ConversusOutput, QualityIndicators, parse_synthesis
from linter.question_classifier import ClassificationResult, classify_question

from pydantic import BaseModel

logger = logging.getLogger("conversus.sdk")

# ---------------------------------------------------------------------------
# Result models — frozen Pydantic per Constitution Principle IX
# ---------------------------------------------------------------------------


class Result(BaseModel):
    """Typed result of a conversus deliberation.

    Wraps the canonical ``ConversusOutput`` fields (headline, summary,
    full_analysis, quality_indicators, debate_transcript) with pipeline
    metadata (rounds_completed, termination_reason, written_files,
    output_dir) for programmatic consumption.
    """

    model_config = {"frozen": True}

    headline: str
    summary: str
    full_analysis: str
    quality_indicators: QualityIndicators
    debate_transcript: str
    rounds_completed: int
    termination_reason: str | None
    written_files: list[Path]
    output_dir: Path


class ValidateResult(BaseModel):
    """Result of validating a conversus config without execution.

    Contains the validation verdict, structured error list, the parsed
    config (when valid), and a cost estimate showing per-phase launch
    counts.
    """

    model_config = {"frozen": True}

    valid: bool
    errors: list[str]
    config: EngineConfig | None = None
    cost_estimate: dict[str, int] | None = None


# ---------------------------------------------------------------------------
# Cost estimation helper (delegates to engine.cost)
# ---------------------------------------------------------------------------


def _estimate_cost(config: EngineConfig) -> dict[str, int]:
    """Calculate per-phase launch counts for a parsed config.

    Returns a dict mapping phase names to launch counts, matching the
    MCP server's cost estimation formula (D007).
    """
    return estimate_cost(
        agent_count=len(config.agents),
        iterations=config.iterations,
        has_arbiter=config.arbiter is not None,
    )


# ---------------------------------------------------------------------------
# Deliberation class — the main SDK orchestrator
# ---------------------------------------------------------------------------


class Deliberation:
    """Async orchestrator for conversus deliberations.

    Supports two modes:
    - **Config-path mode:** ``Deliberation(config_path=Path("conversus.yml"))``
    - **Ad-hoc question mode:** ``Deliberation(question="Should we...", provider="mock")``

    Subscribe to lifecycle events before calling ``run()``:

        d = Deliberation(config_path=path)
        d.on(PhaseStarted, lambda e: print(e.phase))
        result = await d.run()

    Parameters:
        config_path: Path to a conversus YAML config file.
        question: Natural-language question for ad-hoc deliberation.
        provider: Provider name (``"mock"``, ``"anthropic"``, ``"openai"``).
        mode: Deliberation mode (default: ``"cooperative"``).
        output_dir: Override output directory (optional).

    Raises:
        ValueError: If neither ``config_path`` nor ``question`` is provided.
    """

    def __init__(
        self,
        *,
        config_path: Path | None = None,
        question: str | None = None,
        provider: str = "mock",
        mode: str = "cooperative",
        output_dir: Path | None = None,
    ) -> None:
        if config_path is None and (question is None or not question.strip()):
            raise ValueError(
                "At least one of 'config_path' or 'question' must be provided."
            )

        self._config_path = config_path
        self._question = question.strip() if question else None
        self._provider = provider
        self._mode = mode
        self._output_dir = output_dir
        self._callbacks: list[tuple[type, Callable]] = []

    def on(self, event_type: type, callback: Callable) -> None:
        """Register a callback for a specific event type.

        The callback is invoked synchronously each time the engine emits
        an event matching ``event_type``.

        Args:
            event_type: An ``EngineEvent`` subclass (e.g. ``PhaseStarted``).
            callback: A callable that accepts a single event argument.
        """
        self._callbacks.append((event_type, callback))

    @property
    def cost_estimate(self) -> dict[str, int] | None:
        """Per-phase launch counts for the configured deliberation.

        Parses the config (if ``config_path`` is set) and returns
        a dict mapping phase names to expected launch counts.  Returns
        ``None`` if config cannot be parsed.
        """
        if self._config_path is not None:
            try:
                config = parse_config(self._config_path)
                return _estimate_cost(config)
            except (ConfigError, Exception):
                return None
        # For ad-hoc question mode, return the default 2-agent cost
        if self._question:
            return {
                "review": 2,
                "cross_review": 2,
                "revision": 2,
                "disputes": 2,
                "synthesis": 1,
            }
        return None

    def _build_emitter(self) -> CallbackEmitter | NullEmitter:
        """Build an event emitter from registered callbacks."""
        if not self._callbacks:
            return NullEmitter()

        callbacks = self._callbacks  # capture for closure

        def _dispatch(event: EngineEvent) -> None:
            for event_type, callback in callbacks:
                if isinstance(event, event_type):
                    callback(event)

        return CallbackEmitter(_dispatch)

    async def run(self) -> Result:
        """Execute the deliberation and return a typed Result.

        For config-path mode, parses the config, resolves the provider,
        runs the pipeline, and parses the synthesis output.

        For ad-hoc question mode, generates a temporary config using
        pragmatist + devils-advocate presets, then follows the same flow.

        Returns:
            A frozen ``Result`` model with all deliberation output.

        Raises:
            ConfigError: If the config is invalid.
            PipelineError: If all agents fail.
            ProviderError: If the provider cannot be resolved.
            ValueError: If synthesis output cannot be parsed.
        """
        if self._config_path is not None:
            return await self._run_config_path()
        else:
            return await self._run_ad_hoc()

    async def _run_config_path(self) -> Result:
        """Execute using a config file path."""
        config_path = self._config_path
        assert config_path is not None

        engine_config = parse_config(config_path)
        provider = resolve_provider(self._provider)
        emitter = self._build_emitter()

        pipeline_result = await run_pipeline(
            engine_config,
            provider,
            emitter,
            config_path=config_path,
        )

        return self._build_result(pipeline_result, engine_config.mode)

    async def _run_ad_hoc(self) -> Result:
        """Execute an ad-hoc question deliberation with temp config."""
        assert self._question is not None

        from engine.adhoc import build_adhoc_config

        tmp_dir: Path | None = None
        try:
            config_path, question_path, tmp_dir = build_adhoc_config(
                question=self._question,
                mode=self._mode,
                output_dir=self._output_dir,
            )

            engine_config = parse_config(config_path)
            provider = resolve_provider(self._provider)
            emitter = self._build_emitter()

            pipeline_result = await run_pipeline(
                engine_config,
                provider,
                emitter,
                config_path=config_path,
            )

            return self._build_result(pipeline_result, self._mode)
        finally:
            # Clean up temp directory only if we created the output inside it
            if tmp_dir is not None and self._output_dir is None and tmp_dir.exists():
                shutil.rmtree(tmp_dir, ignore_errors=True)

    @staticmethod
    def _find_project_root() -> Path:
        """Locate the conversus project root (directory containing presets/).

        Delegates to :func:`engine._root.find_project_root`.

        Raises:
            ConfigError: If no directory with a ``presets/`` subdirectory is found.
        """
        from engine._root import find_project_root

        try:
            return find_project_root(marker="presets")
        except FileNotFoundError as exc:
            raise ConfigError(str(exc)) from exc

    @staticmethod
    def _build_result(pipeline_result: Any, mode: str) -> Result:
        """Parse synthesis output and construct a typed Result."""
        # Find synthesis file
        synthesis_path = pipeline_result.output_dir / "summary" / "final.md"
        if not synthesis_path.exists():
            raise ValueError(
                f"Pipeline completed but synthesis file not found: {synthesis_path}"
            )

        synthesis_text = synthesis_path.read_text(encoding="utf-8")
        parsed = parse_synthesis(synthesis_text, mode=mode)

        return Result(
            headline=parsed.headline,
            summary=parsed.summary,
            full_analysis=parsed.full_analysis,
            quality_indicators=parsed.quality_indicators,
            debate_transcript=parsed.debate_transcript,
            rounds_completed=pipeline_result.rounds_completed,
            termination_reason=pipeline_result.termination_reason,
            written_files=list(pipeline_result.written_files),
            output_dir=pipeline_result.output_dir,
        )


# ---------------------------------------------------------------------------
# validate() — config validation without execution
# ---------------------------------------------------------------------------


def validate(config_path: Path) -> ValidateResult:
    """Validate a conversus config file without executing the pipeline.

    Parses the config, catches any ``ConfigError``, and computes a cost
    estimate from the parsed config.

    Args:
        config_path: Path to a conversus YAML config file.

    Returns:
        A frozen ``ValidateResult`` with validity, errors, parsed config,
        and cost estimate.

    Note:
        This function never raises — all errors are captured in the
        ``errors`` list of the returned ``ValidateResult``.
    """
    try:
        config = parse_config(config_path)
    except ConfigError as exc:
        logger.warning("Config validation failed: %s", exc)
        return ValidateResult(
            valid=False,
            errors=[str(exc)],
        )
    except Exception as exc:
        logger.exception("Unexpected error during config validation")
        return ValidateResult(
            valid=False,
            errors=[f"Unexpected error: {exc}"],
        )

    cost = _estimate_cost(config)

    return ValidateResult(
        valid=True,
        errors=[],
        config=config,
        cost_estimate=cost,
    )


# ---------------------------------------------------------------------------
# classify() — question classification (thin wrapper)
# ---------------------------------------------------------------------------


def classify(
    question: str,
    *,
    mode: str = "non-interactive",
) -> ClassificationResult:
    """Classify whether a question is sufficient for multi-agent deliberation.

    Thin wrapper over ``linter.question_classifier.classify_question()`` —
    no duplicate logic.

    Args:
        question: The question to classify.
        mode: Classification mode (``"interactive"`` or ``"non-interactive"``).

    Returns:
        A frozen ``ClassificationResult`` with sufficiency verdict and guidance.
    """
    return classify_question(question, mode=mode)
