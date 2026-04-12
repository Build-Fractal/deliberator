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
# Result types moved to engine/results.py (constitution principle XI:
# single source of truth). Re-exported below at module scope so existing
# imports like ``from mcp_server import CostEstimate`` keep working.
from engine.results import (
    CostEstimate,
    DecideResult,
    RunResult,
    ValidateResult,
    _estimate_cost,
)
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
#
# ``CostEstimate``, ``ValidateResult``, ``RunResult``, and ``DecideResult``
# all live in ``engine/results.py`` as the single source of truth
# (constitution principle XI). They are imported at the top of this file
# and re-exported at module scope so downstream imports
# (``from mcp_server import CostEstimate``) keep working.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Pure functions — testable without MCP server running
#
# ``_estimate_cost`` moved to ``engine/results.py`` alongside ``CostEstimate``
# (constitution principle XI). Imported at the top of this file and
# re-exported at module scope for backward compatibility.
# ---------------------------------------------------------------------------


# ``_parse_and_validate_config`` and ``_validate_config`` moved to
# ``engine/handlers.py`` (constitution principle XI — single source of
# truth). The aliases below preserve the ``from mcp_server import
# _parse_and_validate_config, _validate_config`` import paths used by
# existing tests in ``linter/test_mcp_server.py``.
from engine.handlers import _parse_and_validate_config  # noqa: E402
from engine.handlers import validate_mcp as _validate_config  # noqa: E402


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
# conversus_run — MCP tool
#
# ``_run_in_process`` and ``_run_config`` moved to ``engine/handlers.py``
# (constitution principle XI — single source of truth). Aliases below
# preserve existing ``from mcp_server import _run_config, _run_in_process``
# imports used by ``linter/test_mcp_server.py`` and
# ``engine/tests/test_integration.py``.
# ---------------------------------------------------------------------------
from engine.handlers import _run_in_process  # noqa: E402
from engine.handlers import run_mcp as _run_config  # noqa: E402


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


# ``_decide`` moved to ``engine/handlers.py::run_decide_mcp`` as the
# canonical MCP-surface handler (constitution principle XI — single
# source of truth). The alias below preserves the ``from mcp_server
# import _decide`` import path used by the existing
# ``linter/test_mcp_server.py::TestDecideFunction`` tests, which are
# now transitively exercising ``run_decide_mcp``.
from engine.handlers import run_decide_mcp as _decide


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
