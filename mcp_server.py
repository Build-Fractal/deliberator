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

# NOTE: do NOT add ``from __future__ import annotations`` here.
# FastMCP uses return type annotations (``-> DecideResult``) to generate
# JSON schemas. With ``from __future__``, they become strings that
# FastMCP/Pydantic must resolve — and in bundled contexts (.mcpb,
# claude.ai deferred tool loading) the resolution fails with
# "model is not fully defined". Keeping eager annotation evaluation
# avoids the issue entirely.

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
    """Run or parse a full multi-agent deliberation from a YAML config.

    Use this tool when conversus_decide's built-in presets aren't enough —
    custom agent personas, target documents, specific game theory modes,
    multiple iterations, or an arbiter.

    Operates in three modes (auto-selected by which args you pass):

    **Validate-only** (no output_path, no provider): Validates the YAML config,
    estimates cost, and returns instructions to execute '/conversus run' in
    the editor.

    **Parse-results** (output_path provided): Validates config, reads the
    synthesis file at the given path, and returns structured ConversusOutput
    JSON identical to what '/conversus run' produces.

    **In-process** (provider set, no output_path): Validates config, runs the
    full engine pipeline in-process using the specified provider, and returns
    structured ConversusOutput JSON. Supported providers: 'mock', 'demo',
    'anthropic', 'openai', 'claude-desktop'.

    Config shape (minimal example):
        question: "Should we X or Y?"
        mode: cooperative  # or winner-take-all, red-blue, prisoners-dilemma
        agents:
          - preset: pragmatist
          - preset: devils-advocate
        iterations: 1

    Document analysis usage — add a target: list to feed docs into every
    agent's context:
        question: "Extract the key risks from these contracts."
        target:
          - ./contracts/vendor_a.pdf
          - ./contracts/vendor_b.pdf
        agents:
          - preset: pragmatist
          - preset: devils-advocate

    Cost reference: 2 agents / 1 iteration → ~9 LLM launches. Always run
    conversus_validate first to see exact cost before executing.

    Args:
        config_yaml: Full YAML configuration string for a conversus run.
        output_path: Optional path to an existing synthesis output file
                     (typically summary/final.md). When provided, the tool
                     parses the file into structured ConversusOutput JSON.
        provider: Optional provider name for in-process execution. When set
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
    ctx: object = None,
) -> DecideResult:
    """Run an ad-hoc multi-agent deliberation on a natural-language question.

    Classifies the question for sufficiency, generates a temporary config
    using pragmatist + devils-advocate presets, and runs the full 5-phase
    pipeline (review → cross-review → revision → disputes → synthesis).
    Insufficient questions are rejected before execution (quality gate).

    Recommended for quick, ad-hoc deliberations on technical/strategic
    decisions without writing a conversus.yml config file. For document
    analysis across multiple files, prefer conversus_run with target: set.

    Mode selection — pick intentionally:
      - cooperative       Agents seek convergence and surface integration
                          issues. Best for balanced trade-off analysis on
                          complex decisions where you want a nuanced
                          recommendation. Default choice when unsure.
      - winner-take-all   Each agent defends one position; synthesis MUST
                          pick a single winner with reasoning for why the
                          other lost. Best when you need commitment, not
                          a list of pros/cons. Use when hedging is costly.
      - red-blue          Asymmetric adversarial review: one agent attacks
                          (finds every flaw), one defends (makes strongest
                          case). Best for stress-testing a plan you're
                          leaning toward. Surfaces worst-case scenarios.
      - prisoners-dilemma Agents choose cooperate/defect with payoff
                          structure. Best for testing whether a trust-based
                          arrangement holds under individual incentives.
                          Niche; use when modeling multi-party commitments.

    Args:
        question: Natural-language question to deliberate (e.g.
            "Should we use SQLite or Postgres for our metadata store?").
        provider: Model provider for the deliberation. Supported values:
            'demo' (free test mode with mock responses),
            'claude-desktop' (uses host MCP session, no API key),
            'anthropic' (direct API, requires ANTHROPIC_API_KEY),
            'openai' (requires OPENAI_API_KEY).
        mode: Deliberation mode (see Mode selection above). One of:
            'cooperative' (default), 'winner-take-all',
            'prisoners-dilemma', 'red-blue'.
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
    # Pass MCP context for the claude-desktop provider (spec 060).
    # FastMCP injects ctx automatically when the tool handler has a
    # parameter named "ctx". For other providers, ctx is ignored.
    result = _decide(question, provider, mode, max_launches, mcp_context=ctx)
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
# conversus_login — OAuth login from chat (spec 059)
# ---------------------------------------------------------------------------
from engine.handlers import login_mcp as _login_mcp


@mcp.tool()
def conversus_login(provider: str) -> str:
    """Log in to a model provider via OAuth.

    Opens your browser for OAuth authentication. The token is stored
    locally so future deliberations use it automatically.

    Say "log in to anthropic" to authenticate — no CLI needed.

    Args:
        provider: Provider to authenticate with (e.g. 'anthropic', 'openai').

    Returns:
        Status message (success or error description).
    """
    logger.info("conversus_login called (provider=%r)", provider)
    return _login_mcp(provider)


# ---------------------------------------------------------------------------
# MCP Prompts — clickable actions in Claude Desktop (spec 059)
#
# Prompts are the Desktop equivalent of slash commands. They appear in
# the Claude Desktop UI as selectable actions so non-technical users can
# explicitly invoke conversus instead of hoping Claude picks the right
# tool from the description alone. All 5 prompts ship — the full
# capability set is visible, not hidden behind progressive disclosure
# (user override of deliberation recommendation).
# ---------------------------------------------------------------------------


@mcp.prompt()
def deliberate(question: str) -> list[dict]:
    """Run a multi-agent deliberation on a decision.

    Analyzes your question, recommends the right mode and agent setup,
    explains the reasoning, and waits for your approval before running.
    """
    return [{"role": "user", "content":
        f"I want to run a conversus deliberation on this question:\n\n"
        f"> {question}\n\n"
        f"Before running, analyze the question and recommend a deliberation setup. "
        f"Consider these conversus modes:\n\n"
        f"- **cooperative** — agents seek convergence, best for complex decisions where you want a balanced recommendation\n"
        f"- **winner-take-all** — each agent defends a position, synthesis picks ONE winner, best when you need a commitment not a list of pros/cons\n"
        f"- **red-blue** — one agent attacks, one defends, best for stress-testing a plan\n"
        f"- **prisoners-dilemma** — agents choose cooperate/defect, tests whether trust holds\n\n"
        f"Present your recommended config as a table:\n"
        f"- **Mode**: which mode and why\n"
        f"- **Why this mode**: 1-2 sentences on why it fits this question\n"
        f"- **What to expect**: what the 5-phase pipeline will produce for this question\n"
        f"- **Estimated cost**: ~9 LLM launches for 2 agents / 1 iteration\n\n"
        f"Then ask me: 'Ready to run this deliberation, or would you like to adjust the mode?'\n\n"
        f"Only call the conversus_decide tool AFTER I confirm. Use the mode you recommended "
        f"(or whatever I chose if I adjusted it)."}]


@mcp.prompt()
def challenge(question: str) -> list[dict]:
    """Red-team a decision — one agent attacks, one defends.

    Sets up an adversarial review where the red team finds every flaw
    while the blue team defends. Explains the setup before running.
    """
    return [{"role": "user", "content":
        f"I want to stress-test this decision with a conversus red-blue deliberation:\n\n"
        f"> {question}\n\n"
        f"Red-blue mode assigns one agent as the attacker (finds every flaw, worst-case scenario) "
        f"and one as the defender (makes the strongest possible case). The synthesis weighs both.\n\n"
        f"Before running, briefly explain:\n"
        f"- What the **red team** will try to break about this decision\n"
        f"- What the **blue team** will defend\n"
        f"- What kind of verdict the synthesis will produce\n\n"
        f"Then ask me: 'Ready to run the red-blue deliberation?'\n\n"
        f"Only call conversus_decide with mode 'red-blue' AFTER I confirm."}]


@mcp.prompt()
def force_decision(question: str) -> list[dict]:
    """Force a definitive answer — no compromise, pick one winner.

    Winner-take-all mode where the synthesis must choose one side.
    Explains the setup before running.
    """
    return [{"role": "user", "content":
        f"I need a definitive answer on this — no 'it depends', no balanced trade-offs:\n\n"
        f"> {question}\n\n"
        f"Winner-take-all mode: each agent defends a position. The synthesis MUST pick one winner "
        f"and explain why the other lost. No compromise.\n\n"
        f"Before running, briefly explain:\n"
        f"- What the **two competing positions** will likely be\n"
        f"- Why winner-take-all is the right mode (vs cooperative which would hedge)\n"
        f"- That the verdict will be decisive — one winner, one loser, with reasoning\n\n"
        f"Then ask me: 'Ready to force a decision?'\n\n"
        f"Only call conversus_decide with mode 'winner-take-all' AFTER I confirm."}]


@mcp.prompt()
def design_deliberation() -> list[dict]:
    """Build a custom deliberation config through conversation.

    Walks you through creating a conversus.yml step by step — question,
    mode, agents, iterations, arbiter. Ask one question at a time.
    """
    # Role-split pattern (spec 060 note): short user turn + assistant turn
    # containing the setup logic. Assistant-role content reads as prior
    # model output rather than third-party user input, which should pass
    # Desktop's prompt-content scanner more easily than a long user-role
    # message full of instructional directives.
    return [
        {"role": "user", "content":
            "Let's design a conversus deliberation config together."},
        {"role": "assistant", "content":
            "Great — I'll help you build one. I need a few things from you, "
            "and I'll ask one at a time so we can iterate:\n\n"
            "1. What's the decision or question?\n"
            "2. Which mode fits best — cooperative (balanced), "
            "winner-take-all (pick one), red-blue (attack/defend), or "
            "prisoners-dilemma (trust test)?\n"
            "3. Which agent perspectives should weigh in?\n"
            "4. How many rounds?\n"
            "5. Do you want an arbiter?\n\n"
            "Once I have those, I'll show you the final YAML and we can run "
            "it with conversus_run. What's your decision?"},
    ]


@mcp.prompt()
def analyze_documents() -> list[dict]:
    """Multi-agent analysis over one or many documents.

    Extract key claims, compare across docs, surface contradictions,
    or run an open review. Agents read the docs independently, then
    cross-review each other so disagreements about what the docs
    actually say become explicit.
    """
    # Role-split pattern — see design_deliberation note.
    return [
        {"role": "user", "content":
            "Let's run a conversus document analysis."},
        {"role": "assistant", "content":
            "I'll set that up. Conversus will run multiple agents over "
            "your docs independently, then cross-review so disagreements "
            "about what the docs say become explicit. I need three things:\n\n"
            "1. Which documents? Paths or URLs — one or many.\n"
            "2. What kind of analysis — extract key claims, compare across "
            "docs, find contradictions, or open review?\n"
            "3. Which analytical lenses — skeptic + advocate, legal + "
            "technical, domain expert + layperson, or something custom?\n\n"
            "Once I have those, I'll build a YAML config with your docs "
            "in target: and run it with conversus_run. What documents would "
            "you like to start with?"},
    ]


@mcp.prompt()
def review_config(config_yaml: str) -> list[dict]:
    """Run a full deliberation from a YAML config file.

    For reproducible deliberations with custom agents, target documents,
    and advanced game theory modes. Pass the full YAML config content.
    """
    return [{"role": "user", "content":
        f"Use the conversus_run tool with this config:\n\n"
        f"```yaml\n{config_yaml}\n```"}]


@mcp.prompt()
def check_cost(config_yaml: str) -> list[dict]:
    """Check the cost of a deliberation before running it.

    Validates the YAML config, estimates the number of LLM launches
    required, and reports any schema errors — without executing anything.
    """
    return [{"role": "user", "content":
        f"Use the conversus_validate tool to check this config before running:\n\n"
        f"```yaml\n{config_yaml}\n```"}]


# ---------------------------------------------------------------------------
# Spec 064.1 — runtime registration of entry-point-discovered capabilities
# ---------------------------------------------------------------------------
#
# Capabilities shipped by paid wheels (``conversus-enhanced`` etc.) advertise
# themselves via setuptools entry points under the four functional groups
# defined in :data:`conversus.registry.discovery.CAPABILITY_GROUPS`. The
# registration call below walks those discoveries and registers each as a
# live MCP tool. Static ``@mcp.tool()`` decorations above are unaffected.
from conversus.registry.runtime import register_discovered_mcp_tools

register_discovered_mcp_tools(mcp)


# ---------------------------------------------------------------------------
# Entry point — stdio transport
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
