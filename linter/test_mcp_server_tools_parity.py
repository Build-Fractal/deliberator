"""Phase 2 drift guard — mcp_server.py static tools match CAPABILITIES.

Constitution Principles XI (Single Source of Truth, Registry-First
Declaration extension) and XXVI (Meta-Testing for Parametrized
Capabilities) require that the capability registry remain the
authoritative source for tool availability across every distribution
surface. Phase 1 (PR #18) wired this for ``manifest.json``. Phase 2
(this test) wires it for ``mcp_server.py``.

The test imports ``mcp_server`` once at module load — this triggers
FastMCP registration of every static ``@_optional_tool()`` decorator
plus the spec 064.1 runtime registration of entry-point-discovered
tools. We then compare the FastMCP-registered tool names against the
expected set derived from ``CAPABILITIES`` filtered to ``Surface.MCP``.

Behavior on drift:
- A Capability declares ``Surface.MCP`` but no ``@_optional_tool()``
  is wired in mcp_server.py → test fails with the missing tool name.
- A static ``@_optional_tool()`` exists in mcp_server.py for which no
  Capability is declared → test fails with the unexpected tool name.

The OSS test environment installs no paid extensions, so the spec
064.1 runtime hook registers zero additional tools. Any actual-vs-
expected mismatch therefore identifies a real drift between the
registry and mcp_server.py — not noise from entry points.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

pytest.importorskip("mcp")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from capabilities import CAPABILITIES
from conversus.registry import Surface

import mcp_server  # noqa: E402 — must come after sys.path setup


def _expected_mcp_tool_names() -> set[str]:
    """Tool names every static MCP tool MUST register.

    Derived from ``CAPABILITIES`` filtered to ``Surface.MCP``. Names
    use the ``conversus_`` prefix and replace ``-`` with ``_`` (matching
    the projector + ``@_optional_tool()`` convention).
    """
    return {
        "conversus_" + cap.name.replace("-", "_")
        for cap in CAPABILITIES
        if Surface.MCP in cap.surfaces
    }


def _actual_mcp_tool_names() -> set[str]:
    """Tool names FastMCP has registered after importing mcp_server."""
    tools = asyncio.run(mcp_server.mcp.list_tools())
    return {t.name for t in tools}


def test_every_mcp_capability_has_a_static_tool() -> None:
    """Every Capability with Surface.MCP must have a registered tool.

    On failure, add the missing ``@_optional_tool()`` decorator to
    ``mcp_server.py`` so the function name (with ``conversus_`` prefix
    and dashes-to-underscores) matches the capability.
    """
    expected = _expected_mcp_tool_names()
    actual = _actual_mcp_tool_names()

    missing = expected - actual
    assert not missing, (
        f"mcp_server.py is missing {len(missing)} tool(s) declared by "
        f"the capability registry with Surface.MCP: {sorted(missing)}.\n"
        f"  Fix: add a @_optional_tool() decorator in mcp_server.py for "
        f"each missing tool. Function name MUST match "
        f"'conversus_' + capability.name.replace('-', '_')."
    )


def test_every_static_tool_has_a_capability() -> None:
    """No tool should be registered without a corresponding Capability.

    The OSS test env loads no entry-point-discovered extensions, so
    every registered tool must trace back to a Capability declaring
    Surface.MCP. Hand-coded tools without a Capability are violations
    of Principle XI's Registry-First Declaration extension.
    """
    expected = _expected_mcp_tool_names()
    actual = _actual_mcp_tool_names()

    unexpected = actual - expected
    assert not unexpected, (
        f"mcp_server.py registered {len(unexpected)} tool(s) with no "
        f"corresponding Capability declaring Surface.MCP: "
        f"{sorted(unexpected)}.\n"
        f"  Fix: either (a) add a Capability to capabilities.py declaring "
        f"the tool, or (b) remove the @_optional_tool() decorator from "
        f"mcp_server.py. Hand-coded tools without registry backing "
        f"violate Principle XI (Registry-First Declaration)."
    )


def test_static_tool_count_matches_registry() -> None:
    """Belt-and-suspenders count check.

    The two tests above already cover this via set equality, but a
    separate count check produces a more readable failure when the
    discrepancy is "wrong number of tools" rather than "specific tools
    missing." Useful diagnostic when the count drifts dramatically.
    """
    expected = _expected_mcp_tool_names()
    actual = _actual_mcp_tool_names()

    assert len(actual) == len(expected), (
        f"Tool count mismatch: registry declares {len(expected)} "
        f"Surface.MCP capabilities; mcp_server.py registers "
        f"{len(actual)} tools.\n"
        f"  Registry expected: {sorted(expected)}\n"
        f"  mcp_server actual: {sorted(actual)}"
    )


@pytest.mark.parametrize(
    "tool_name",
    sorted(_expected_mcp_tool_names()),
)
def test_each_expected_tool_present_individually(tool_name: str) -> None:
    """Per-tool parametrized coverage — meta-test per Principle XXVI.

    Failures report which specific tool is missing, rather than dumping
    a set diff. Easier to act on for the developer who broke the test.
    """
    actual = _actual_mcp_tool_names()
    assert tool_name in actual, (
        f"Tool {tool_name!r} declared in CAPABILITIES (Surface.MCP) but "
        f"not registered by mcp_server.py."
    )
