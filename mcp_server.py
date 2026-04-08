#!/usr/bin/env python3
"""
Conversus MCP Server

Exposes conversus deliberation tools via the Model Context Protocol (MCP).
Designed for use with Claude Code, Cursor, and other MCP-compatible editors.

Tools:
    conversus_validate — Validate a YAML config, classify questions, estimate cost
    conversus_run      — Validate config + parse existing synthesis output into
                         structured ConversusOutput JSON (hybrid execution model)
    conversus_decide   — Run an ad-hoc deliberation on a natural-language question
                         with question sufficiency gate and cost safeguards

Transport: stdio (launched by the editor process)

Usage:
    uv run python3 mcp_server.py          # starts the stdio MCP server
    uv run python3 mcp_server.py --help   # (reserved for future flags)
"""

from __future__ import annotations

import asyncio
import logging
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from engine.auth import resolve_provider
from engine.config import ConfigError, parse_config
from engine.events import NullEmitter
from engine.phases import PipelineError, run_pipeline
from engine.providers import ProviderError
from linter.output_contract import parse_synthesis
from linter.question_classifier import classify_question
from linter.validate import ValidationConfig, validate_all, find_project_root

# ---------------------------------------------------------------------------
# Logging — surface structured diagnostics without polluting MCP stdio
# ---------------------------------------------------------------------------

logger = logging.getLogger("conversus.mcp")
logger.addHandler(logging.StreamHandler(sys.stderr))
logger.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# FastMCP instance
# ---------------------------------------------------------------------------

mcp = FastMCP("conversus")

# ---------------------------------------------------------------------------
# Pydantic models — auto-generate JSON schemas for MCP tool responses
# ---------------------------------------------------------------------------


class CostEstimate(BaseModel):
    """Estimated launch cost for a conversus deliberation run.

    Each 'launch' is one LLM agent invocation. The per-phase breakdown
    shows exactly where the budget goes.
    """

    total_launches: int
    launches_per_phase: dict[str, int]
    agent_count: int
    iteration_count: int


class ValidateResult(BaseModel):
    """Result of validating a conversus YAML configuration.

    Returned by the conversus_validate MCP tool. Contains template
    validation errors, optional question classification, optional
    preset info, and a cost estimate when the config is parseable.
    """

    valid: bool
    errors: list[str]
    cost_estimate: CostEstimate | None = None
    classification: dict[str, Any] | None = None
    preset_info: list[str] | None = None


class RunResult(BaseModel):
    """Result of the conversus_run MCP tool.

    Operates in three modes:

    - **validate_only** (no output_path, no provider): validates config,
      estimates cost, and returns instructions to execute '/conversus run'.
    - **parsed_output** (output_path provided): validates config, reads the
      synthesis file, parses it into a structured ConversusOutput dict.
    - **in_process** (provider set, no output_path): validates config, runs
      the full engine pipeline in-process, and returns structured output.
    """

    mode: str  # "validate_only", "parsed_output", or "in_process"
    validated: bool
    errors: list[str]
    cost_estimate: CostEstimate | None = None
    instructions: str | None = None
    output: dict[str, Any] | None = None
    rounds_completed: int | None = None
    termination_reason: str | None = None


class DecideResult(BaseModel):
    """Result of an ad-hoc deliberation via conversus_decide.

    Returned by the conversus_decide MCP tool. Contains the question
    sufficiency verdict, optional classification details, pipeline
    output (when the question is sufficient and execution succeeds),
    cost estimate, and any errors encountered.

    Fields:
        sufficient: Whether the question passed the quality gate.
        classification: Full classification result from the question
            classifier (reason, missing fields, etc.).
        output: Structured ConversusOutput dict from the pipeline, or
            None if the question was insufficient or execution failed.
        cost_estimate: Estimated launch cost before execution, or None
            if estimation was not reached.
        errors: List of error messages (empty on success).
        rounds_completed: Number of deliberation rounds completed by
            the pipeline, or None if execution did not run.
        termination_reason: Why the pipeline stopped (e.g. 'completed',
            'max_rounds'), or None if execution did not run.
    """

    sufficient: bool
    classification: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    cost_estimate: CostEstimate | None = None
    errors: list[str] = []
    rounds_completed: int | None = None
    termination_reason: str | None = None


# ---------------------------------------------------------------------------
# Pure functions — testable without MCP server running
# ---------------------------------------------------------------------------


def _estimate_cost(config: dict[str, Any]) -> CostEstimate:
    """Calculate the expected number of LLM launches for a deliberation run.

    Delegates the formula to :func:`engine.cost.estimate_cost` (D007) and
    wraps the result in a ``CostEstimate`` model for the MCP response.
    """
    from engine.cost import estimate_cost

    agents: list[dict[str, Any]] = config.get("agents", [])
    agent_count: int = len(agents)
    iteration_count: int = config.get("iterations", 1)
    has_arbiter: bool = config.get("arbiter") is not None

    launches_per_phase = estimate_cost(agent_count, iteration_count, has_arbiter)
    total = sum(launches_per_phase.values())

    return CostEstimate(
        total_launches=total,
        launches_per_phase=launches_per_phase,
        agent_count=agent_count,
        iteration_count=iteration_count,
    )


def _parse_and_validate_config(
    config_yaml: str,
) -> tuple[dict[str, Any] | None, list[str], CostEstimate | None]:
    """Parse YAML config, validate templates, and estimate cost.

    Shared logic used by both _validate_config and _run_config to avoid
    duplicating YAML parsing, template validation, and cost estimation.

    Returns:
        (config_dict, errors, cost_estimate) — config_dict is None if
        YAML parsing failed or the result is not a dict.
    """
    # --- Parse YAML ---
    try:
        config: dict[str, Any] = yaml.safe_load(config_yaml)
    except yaml.YAMLError as exc:
        logger.exception("YAML parse error")
        return None, [f"YAML parse error: {exc}"], None

    if not isinstance(config, dict):
        return None, ["Config must be a YAML mapping (dict), not a scalar or list"], None

    # --- Template validation via existing linter infrastructure ---
    errors: list[str] = []
    try:
        root = find_project_root()
        mode = config.get("mode", "cooperative")
        result = validate_all(ValidationConfig(root=root, mode=mode))
        if not result.passed:
            for err in result.errors:
                msg = f"{err.file_path}: {err.message}"
                if err.suggestion:
                    msg += f" {err.suggestion}"
                errors.append(msg)
    except Exception as exc:
        logger.exception("Template validation error")
        errors.append(f"Template validation error: {exc}")

    # --- Cost estimation ---
    cost_estimate: CostEstimate | None = None
    try:
        cost_estimate = _estimate_cost(config)
    except Exception as exc:
        logger.exception("Cost estimation error")
        errors.append(f"Cost estimation error: {exc}")

    return config, errors, cost_estimate


def _validate_config(config_yaml: str, question: str = "") -> ValidateResult:
    """Core validation logic extracted for testability.

    Parses YAML, runs template validation, optionally classifies
    the question, and computes cost estimates.
    """
    config, errors, cost_estimate = _parse_and_validate_config(config_yaml)

    if config is None:
        return ValidateResult(
            valid=False,
            errors=errors,
        )

    # --- Question classification (optional) ---
    classification: dict[str, Any] | None = None
    if question.strip():
        try:
            cr = classify_question(question, mode="non-interactive")
            classification = cr.model_dump()
        except Exception as exc:
            logger.exception("Question classification error")
            errors.append(f"Question classification error: {exc}")

    # --- Preset info (extract mode and agent names for editor display) ---
    preset_info: list[str] | None = None
    agents = config.get("agents", [])
    if agents:
        mode_name = config.get("mode", "cooperative")
        agent_names = [a.get("name", "unnamed") for a in agents if isinstance(a, dict)]
        preset_info = [
            f"mode: {mode_name}",
            f"agents: {', '.join(agent_names)}",
            f"iterations: {config.get('iterations', 1)}",
        ]

    valid = len(errors) == 0

    return ValidateResult(
        valid=valid,
        errors=errors,
        cost_estimate=cost_estimate,
        classification=classification,
        preset_info=preset_info,
    )


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def conversus_validate(config_yaml: str, question: str = "") -> ValidateResult:
    """Validate a conversus YAML configuration without executing.

    Parses the YAML config, validates templates against the schema,
    optionally classifies the deliberation question, and returns a
    cost estimate (number of LLM launches required).

    Args:
        config_yaml: Full YAML configuration string for a conversus run.
        question: Optional deliberation question to classify for sufficiency.

    Returns:
        ValidateResult with validation status, errors, cost estimate,
        and optional question classification.
    """
    logger.info("conversus_validate called (config length=%d, question=%r)",
                len(config_yaml), bool(question))
    result = _validate_config(config_yaml, question)
    if not result.valid:
        logger.warning("Validation failed with %d error(s)", len(result.errors))
    return result


# ---------------------------------------------------------------------------
# conversus_run — pure function + MCP tool
# ---------------------------------------------------------------------------


def _run_in_process(
    config_yaml: str,
    provider_name: str,
    validated: bool,
    errors: list[str],
    cost_estimate: CostEstimate | None,
) -> RunResult:
    """Execute a full deliberation pipeline in-process and return structured output.

    Writes the config YAML to a temp file in the current working directory
    (so relative paths in the config resolve correctly), creates the provider,
    runs the async pipeline synchronously, and parses the synthesis output.
    """
    tmp_path: Path | None = None
    try:
        # Write temp config in CWD so relative paths resolve correctly.
        # parse_config resolves target/output/docs relative to config file parent.
        fd, tmp_str = tempfile.mkstemp(
            prefix=".conversus_mcp_", suffix=".yml", dir=Path.cwd()
        )
        tmp_path = Path(tmp_str)
        try:
            with open(fd, "w", encoding="utf-8") as f:
                f.write(config_yaml)
        except Exception:
            import os
            os.close(fd)
            raise

        engine_config = parse_config(tmp_path)

        # Create provider via resolve_provider (supports mock, anthropic, openai)
        try:
            model_provider = resolve_provider(provider_name)
        except ProviderError as exc:
            errors_out = list(errors)
            errors_out.append(str(exc))
            return RunResult(
                mode="in_process",
                validated=validated,
                errors=errors_out,
                cost_estimate=cost_estimate,
            )

        # Run the pipeline synchronously
        emitter = NullEmitter()
        result = asyncio.run(
            run_pipeline(
                engine_config,
                model_provider,
                emitter,
                config_path=tmp_path,
            )
        )

        # Read synthesis output
        synthesis_path = result.output_dir / "summary" / "final.md"
        if not synthesis_path.exists():
            return RunResult(
                mode="in_process",
                validated=validated,
                errors=errors + [f"Pipeline completed but synthesis file not found: {synthesis_path}"],
                cost_estimate=cost_estimate,
                rounds_completed=result.rounds_completed,
                termination_reason=result.termination_reason,
            )

        synthesis_text = synthesis_path.read_text(encoding="utf-8")
        mode_name = engine_config.mode
        parsed = parse_synthesis(synthesis_text, mode=mode_name)

        return RunResult(
            mode="in_process",
            validated=validated,
            errors=errors,
            cost_estimate=cost_estimate,
            output=parsed.model_dump(),
            rounds_completed=result.rounds_completed,
            termination_reason=result.termination_reason,
        )

    except ConfigError as exc:
        logger.exception("Engine config error during in-process execution")
        return RunResult(
            mode="in_process",
            validated=False,
            errors=errors + [f"Engine config error: {exc}"],
            cost_estimate=cost_estimate,
        )
    except PipelineError as exc:
        logger.exception("Pipeline error during in-process execution")
        return RunResult(
            mode="in_process",
            validated=validated,
            errors=errors + [f"Pipeline error: {exc}"],
            cost_estimate=cost_estimate,
        )
    except Exception as exc:
        logger.exception("Unexpected error during in-process execution")
        return RunResult(
            mode="in_process",
            validated=validated,
            errors=errors + [f"Execution error: {exc}"],
            cost_estimate=cost_estimate,
        )
    finally:
        # Clean up temp config file
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def _run_config(config_yaml: str, output_path: str = "", provider: str = "") -> RunResult:
    """Core run logic extracted for testability.

    Three modes:
    - **validate_only** (empty output_path, empty provider): validates config,
      estimates cost, returns execution instructions.
    - **parsed_output** (output_path set): validates config, reads and
      parses synthesis file at the path, returns structured ConversusOutput.
    - **in_process** (provider set, empty output_path): validates config, runs
      the full engine pipeline in-process, returns structured ConversusOutput.
    """
    config, errors, cost_estimate = _parse_and_validate_config(config_yaml)

    if config is None:
        return RunResult(
            mode="validate_only",
            validated=False,
            errors=errors,
            instructions="Config has errors — fix them before running.",
        )

    validated = len(errors) == 0

    # --- In-process execution mode ---
    if provider and provider.strip() and (not output_path or not output_path.strip()):
        return _run_in_process(config_yaml, provider.strip(), validated, errors, cost_estimate)

    # --- Mode dispatch ---
    if not output_path or not output_path.strip():
        # Validate-only mode: return instructions to run the deliberation
        instructions = (
            "Config valid. Execute '/conversus run <path>' in your editor "
            "to run the deliberation."
            if validated
            else "Config has errors — fix them before running."
        )
        return RunResult(
            mode="validate_only",
            validated=validated,
            errors=errors,
            cost_estimate=cost_estimate,
            instructions=instructions,
        )

    # --- Parse-results mode ---
    output_file = Path(output_path.strip())
    if not output_file.exists():
        return RunResult(
            mode="parsed_output",
            validated=validated,
            errors=errors + [f"Output file not found: {output_path}"],
            cost_estimate=cost_estimate,
        )

    try:
        synthesis_text = output_file.read_text(encoding="utf-8")
        mode_name = config.get("mode", "cooperative")
        parsed = parse_synthesis(synthesis_text, mode=mode_name)
        return RunResult(
            mode="parsed_output",
            validated=validated,
            errors=errors,
            cost_estimate=cost_estimate,
            output=parsed.model_dump(),
        )
    except Exception as exc:
        logger.exception("Synthesis parse error")
        return RunResult(
            mode="parsed_output",
            validated=validated,
            errors=errors + [f"Synthesis parse error: {exc}"],
            cost_estimate=cost_estimate,
        )


@mcp.tool()
def conversus_run(config_yaml: str, output_path: str = "", provider: str = "") -> RunResult:
    """Validate a config and optionally run a deliberation or parse existing output.

    Operates in three modes:

    **Validate-only** (no output_path, no provider): Validates the YAML config,
    estimates cost, and returns instructions to execute '/conversus run' in
    the editor.

    **Parse-results** (output_path provided): Validates config, reads the
    synthesis file at the given path, and returns a structured ConversusOutput
    JSON identical to what '/conversus run' produces.

    **In-process** (provider set, no output_path): Validates config, runs the
    full engine pipeline in-process using the specified provider, and returns
    structured ConversusOutput JSON. Supported providers: 'mock', 'anthropic', 'openai'.

    Args:
        config_yaml: Full YAML configuration string for a conversus run.
        output_path: Optional path to an existing synthesis output file
                     (typically summary/final.md). When provided, the tool
                     parses the file into structured ConversusOutput JSON.
        provider: Optional provider name for in-process execution.
                  Supported values: 'mock', 'anthropic', 'openai'. When set
                  (and output_path is empty), the tool runs the full
                  deliberation pipeline in-process.

    Returns:
        RunResult with mode, validation status, cost estimate, and either
        execution instructions, parsed structured output, or in-process
        pipeline results.
    """
    logger.info("conversus_run called (config length=%d, output_path=%r, provider=%r)",
                len(config_yaml), bool(output_path), provider)
    result = _run_config(config_yaml, output_path, provider)
    if not result.validated:
        logger.warning("Run validation failed with %d error(s)", len(result.errors))
    if result.output:
        logger.info("Parsed synthesis output successfully (mode=%s)", result.mode)
    return result


# ---------------------------------------------------------------------------
# conversus_decide — pure function + MCP tool
# ---------------------------------------------------------------------------


def _find_conversus_root() -> Path:
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


def _decide(
    question: str,
    provider: str = "mock",
    mode: str = "cooperative",
    max_launches: int = 20,
) -> DecideResult:
    """Run an ad-hoc deliberation on a natural-language question.

    Pure function extracted for testability — same pattern as ``_run_config()``.

    Generates a temporary conversus config using pragmatist + devils-advocate
    presets, validates the question via the classifier (rejecting insufficient
    questions), checks cost against the max_launches safeguard, runs the full
    pipeline, and returns structured results.

    Args:
        question: Natural-language question to deliberate.
        provider: Model provider name (``'mock'``, ``'anthropic'``, ``'openai'``).
        mode: Deliberation mode (``'cooperative'``, ``'winner-take-all'``,
            ``'prisoners-dilemma'``, ``'red-blue'``).
        max_launches: Maximum allowed LLM launches. Execution is refused
            when the estimated total exceeds this threshold.

    Returns:
        DecideResult with sufficiency verdict, classification, pipeline output,
        cost estimate, and any errors.
    """
    # --- Validate non-empty question ---
    stripped = question.strip()
    if not stripped:
        logger.warning("conversus_decide: empty question rejected")
        return DecideResult(
            sufficient=False,
            errors=["Question must not be empty."],
        )

    # --- Classify question — reject if insufficient (R020 quality gate) ---
    classification: dict[str, Any] | None = None
    try:
        cr = classify_question(stripped, mode="non-interactive")
        classification = cr.model_dump()
        if not cr.sufficient:
            reason = cr.reason or "Question is insufficient for multi-agent deliberation."
            logger.warning("conversus_decide: question insufficient — %s", reason)
            return DecideResult(
                sufficient=False,
                classification=classification,
                errors=[reason],
            )
    except Exception as exc:
        logger.exception("Question classification error")
        return DecideResult(
            sufficient=False,
            errors=[f"Question classification error: {exc}"],
        )

    # --- Build ad-hoc config via shared builder ---
    from engine.adhoc import build_adhoc_config

    try:
        config_path, question_path, tmp_dir = build_adhoc_config(
            question=stripped,
            mode=mode,
        )
    except ConfigError as exc:
        return DecideResult(
            sufficient=True,
            classification=classification,
            errors=[str(exc)],
        )

    cost_estimate: CostEstimate | None = None
    try:
        # --- Cost safeguard: estimate launches and refuse if over limit ---
        config_content = config_path.read_text(encoding="utf-8")
        config_dict = yaml.safe_load(config_content)

        try:
            cost_estimate = _estimate_cost(config_dict)
            if cost_estimate.total_launches > max_launches:
                logger.warning(
                    "conversus_decide: cost limit exceeded (%d > %d)",
                    cost_estimate.total_launches,
                    max_launches,
                )
                return DecideResult(
                    sufficient=True,
                    classification=classification,
                    cost_estimate=cost_estimate,
                    errors=[
                        f"Estimated {cost_estimate.total_launches} launches exceeds "
                        f"max_launches={max_launches}. Increase max_launches to proceed."
                    ],
                )
        except Exception as exc:
            logger.exception("Cost estimation error in _decide")
            return DecideResult(
                sufficient=True,
                classification=classification,
                errors=[f"Cost estimation error: {exc}"],
            )

        # --- Run pipeline ---
        engine_config = parse_config(config_path)

        try:
            model_provider = resolve_provider(provider)
        except ProviderError as exc:
            return DecideResult(
                sufficient=True,
                classification=classification,
                cost_estimate=cost_estimate,
                errors=[f"Provider error: {exc}"],
            )

        emitter = NullEmitter()
        result = asyncio.run(
            run_pipeline(
                engine_config,
                model_provider,
                emitter,
                config_path=config_path,
            )
        )

        # --- Parse synthesis output ---
        synthesis_path = result.output_dir / "summary" / "final.md"
        if not synthesis_path.exists():
            return DecideResult(
                sufficient=True,
                classification=classification,
                cost_estimate=cost_estimate,
                errors=[f"Pipeline completed but synthesis file not found: {synthesis_path}"],
                rounds_completed=result.rounds_completed,
                termination_reason=result.termination_reason,
            )

        synthesis_text = synthesis_path.read_text(encoding="utf-8")
        parsed = parse_synthesis(synthesis_text, mode=mode)

        return DecideResult(
            sufficient=True,
            classification=classification,
            output=parsed.model_dump(),
            cost_estimate=cost_estimate,
            rounds_completed=result.rounds_completed,
            termination_reason=result.termination_reason,
        )

    except ConfigError as exc:
        logger.exception("Config error during conversus_decide")
        return DecideResult(
            sufficient=True,
            classification=classification,
            errors=[f"Config error: {exc}"],
        )
    except PipelineError as exc:
        logger.exception("Pipeline error during conversus_decide")
        return DecideResult(
            sufficient=True,
            classification=classification,
            cost_estimate=cost_estimate,
            errors=[f"Pipeline error: {exc}"],
        )
    except Exception as exc:
        logger.exception("Unexpected error during conversus_decide")
        return DecideResult(
            sufficient=True,
            classification=classification,
            errors=[f"Execution error: {exc}"],
        )
    finally:
        # Always clean up temp directory
        if tmp_dir is not None and tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)


@mcp.tool()
def conversus_decide(
    question: str,
    provider: str = "mock",
    mode: str = "cooperative",
    max_launches: int = 20,
) -> DecideResult:
    """Run an ad-hoc deliberation on a natural-language question.

    Classifies the question for sufficiency, generates a temporary config
    using pragmatist + devils-advocate presets, and runs the full pipeline.
    Insufficient questions are rejected before execution (quality gate).

    This is the recommended tool for quick, ad-hoc deliberations on
    technical decisions without writing a conversus.yml config file.

    Args:
        question: Natural-language question to deliberate (e.g.
            "Should we use SQLite or Postgres for our metadata store?").
        provider: Model provider for the deliberation. Supported values:
            'mock' (default, no API key needed), 'anthropic', 'openai'.
        mode: Deliberation mode. One of: 'cooperative' (default),
            'winner-take-all', 'prisoners-dilemma', 'red-blue'.
        max_launches: Maximum allowed LLM launches (default: 20). Execution
            is refused when the estimated total exceeds this threshold.
            For 2 agents / 1 iteration the default config needs 9 launches.

    Returns:
        DecideResult with sufficiency verdict, question classification,
        structured deliberation output (when successful), cost estimate,
        and any errors encountered.
    """
    logger.info(
        "conversus_decide called (question_len=%d, provider=%r, mode=%r, max_launches=%d)",
        len(question),
        provider,
        mode,
        max_launches,
    )
    result = _decide(question, provider, mode, max_launches)
    if not result.sufficient:
        logger.warning(
            "conversus_decide: question rejected — %s",
            "; ".join(result.errors) if result.errors else "insufficient",
        )
    elif result.errors:
        logger.warning(
            "conversus_decide: execution error(s) — %s",
            "; ".join(result.errors),
        )
    elif result.output:
        logger.info("conversus_decide: deliberation completed successfully")
    return result


# ---------------------------------------------------------------------------
# Entry point — stdio transport
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
