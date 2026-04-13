"""Canonical result types for conversus ad-hoc deliberations.

This is the single source of truth for ``CostEstimate``, ``DecideResult``,
and the ``_estimate_cost`` helper (constitution principle XI). Both
``mcp_server.py`` and ``engine/handlers.py`` import from here rather
than defining their own copies. ``mcp_server.py`` re-exports the names
at module scope for backward compatibility with existing test imports
(``linter/test_mcp_server.py``, ``engine/tests/test_integration.py``).

Why this module was extracted
-----------------------------
The original structure had these types defined in ``mcp_server.py``.
Day 5 of spec 055 needs ``engine/handlers.py`` to return ``DecideResult``
from its ``run_decide_mcp`` handler, and the first-draft plan called
for *duplicating* the definitions into ``engine/handlers.py`` as a
temporary convenience. That duplication would have violated
``CONSTITUTION.md`` principle XI ("If you find yourself writing the same
fact in two places, stop"), so the spec was amended to extract into
this shared module before any duplication happened.

See ``specs/055-capability-registry.md`` §4 Day 5 (Pre-work — extract
shared result types).
"""

# NOTE: do NOT add ``from __future__ import annotations`` to this file.
# Pydantic v2 needs to evaluate type annotations at class definition time
# so it can resolve ``CostEstimate | None``, ``dict[str, Any]``, etc.
# With ``from __future__ import annotations``, all annotations become
# strings that Pydantic must resolve lazily — and in some import contexts
# (the .mcpb bundle, deferred tool loading on claude.ai), the resolution
# fails with "model is not fully defined; you should define 'Any'".
# See docs/developer-guide/gotchas.md for the full explanation.

import logging
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger("conversus.results")


class CostEstimate(BaseModel):
    """Estimated launch cost for a conversus deliberation run.

    Each 'launch' is one LLM agent invocation. The per-phase breakdown
    shows exactly where the budget goes.
    """

    total_launches: int
    launches_per_phase: dict[str, int]
    agent_count: int
    iteration_count: int


class DecideResult(BaseModel):
    """Result of an ad-hoc deliberation.

    Returned by ``engine.handlers.run_decide_mcp`` (and, historically,
    by ``mcp_server._decide``, which is now a thin re-export). Contains
    the question sufficiency verdict, optional classification, pipeline
    output when execution succeeds, cost estimate, and any errors.
    """

    sufficient: bool
    classification: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    cost_estimate: CostEstimate | None = None
    errors: list[str] = []
    rounds_completed: int | None = None
    termination_reason: str | None = None
    output_path: str | None = None
    """Path where the deliberation was persisted (spec 056).

    Example: ``.conversus/deliberations/20260412T173000-postgres-vs-mongodb/``.
    ``None`` when persistence is disabled or the run failed before persistence.
    """


class ValidateResult(BaseModel):
    """Result of validating a conversus YAML configuration.

    Returned by ``engine.handlers.validate_mcp``. Contains template
    validation errors, optional question classification, optional
    preset info, and a cost estimate when the config is parseable.
    """

    valid: bool
    errors: list[str]
    cost_estimate: CostEstimate | None = None
    classification: dict[str, Any] | None = None
    preset_info: list[str] | None = None


class RunResult(BaseModel):
    """Result of the ``run`` capability via the MCP surface.

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
    output_path: str | None = None
    """Path where the deliberation was persisted (spec 056).

    Example: ``.conversus/deliberations/20260412T173000-postgres-vs-mongodb/``.
    ``None`` when persistence is disabled or the run failed before persistence.
    """


class ListResult(BaseModel):
    """Result of listing past deliberations from .conversus/deliberations/."""

    deliberations: list[dict[str, Any]]
    count: int
    project_root: str


class ShowResult(BaseModel):
    """Result of reading a file from a past deliberation."""

    content: str
    deliberation_path: str
    file_path: str
    errors: list[str] = []


def _estimate_cost(config: dict[str, Any]) -> CostEstimate:
    """Calculate the expected number of LLM launches for a deliberation run.

    Delegates the formula to :func:`engine.cost.estimate_cost` and wraps
    the result in a ``CostEstimate`` model for the MCP / handler response
    layer. This function is the canonical caller of ``estimate_cost`` —
    any consumer that wants a typed cost estimate should go through here,
    not reimplement the wrapping.
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
