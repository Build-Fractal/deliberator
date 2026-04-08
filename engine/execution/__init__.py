"""Execution provider layer (spec 042).

Public interface for the agentic task-dispatch abstraction.  See
:mod:`engine.execution.provider` for the protocol definition and type shapes.

This package is distinct from :mod:`engine.providers`, which holds the raw
:class:`~engine.providers.ModelProvider` abstraction for LLM completion APIs.
``engine.execution`` is the *task-level* layer; ``engine.providers`` is the
*model-level* layer.  Both coexist — spec 042's ``ExecutionProvider``
delegates to a ``ModelProvider`` when its :attr:`supports_tool_use` is
``False``.

Per the spec 042 arbitration ruling (2026-04-05), v1 ships four execution
providers — ``mock``, ``anthropic``, ``claude-code``, ``opencode`` — plus
an optional ``litellm`` companion package.  Provider implementations land
in Phase 2+ of spec 042; this module currently exposes only the protocol
and type shapes (Phase 1).
"""

from __future__ import annotations

from engine.execution.provider import (
    Cost,
    Duration,
    ExecutionProvider,
    ExecutionResult,
    ExecutionTask,
    Reference,
    TaskPart,
    TaskPartMediaType,
)

__all__ = [
    "Cost",
    "Duration",
    "ExecutionProvider",
    "ExecutionResult",
    "ExecutionTask",
    "Reference",
    "TaskPart",
    "TaskPartMediaType",
]
