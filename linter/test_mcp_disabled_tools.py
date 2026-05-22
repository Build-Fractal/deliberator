"""Tests for CONVERSUS_DISABLED_TOOLS env-var-driven tool filtering.

The mcp_server module reads ``CONVERSUS_DISABLED_TOOLS`` at import time
and skips FastMCP registration for any tool whose name appears in the
list. This lets operators (Desktop user_config, MCP launcher env, CI
bundles) hide specific tools without forking the server code.

Test layers:

1. ``_parse_disabled_tools`` — pure parser unit tests.
2. ``_optional_tool`` — decorator behavior with monkeypatched
   ``_DISABLED_TOOLS`` set: skips registration when disabled, registers
   normally when enabled, returns a still-callable function in both cases.
3. Integration with FastMCP — using a fresh ``FastMCP`` instance and
   asyncio.run(list_tools()), confirm disabled tools are absent from
   the actual MCP tool listing while enabled tools appear.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

pytest.importorskip("mcp")

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import mcp_server
from mcp_server import _optional_tool, _parse_disabled_tools


# ---------------------------------------------------------------------------
# _parse_disabled_tools — pure parser
# ---------------------------------------------------------------------------


class TestParseDisabledTools:
    """``CONVERSUS_DISABLED_TOOLS`` env-value parser."""

    def test_none_returns_empty(self) -> None:
        assert _parse_disabled_tools(None) == frozenset()

    def test_empty_string_returns_empty(self) -> None:
        assert _parse_disabled_tools("") == frozenset()

    def test_whitespace_only_returns_empty(self) -> None:
        assert _parse_disabled_tools("   ") == frozenset()

    def test_single_name(self) -> None:
        assert _parse_disabled_tools("conversus_login") == frozenset({"conversus_login"})

    def test_multiple_names(self) -> None:
        assert _parse_disabled_tools("conversus_login,conversus_run") == frozenset(
            {"conversus_login", "conversus_run"}
        )

    def test_whitespace_around_names_stripped(self) -> None:
        assert _parse_disabled_tools(" a , b ,  c  ") == frozenset({"a", "b", "c"})

    def test_skips_empty_segments(self) -> None:
        """Trailing/repeated commas don't produce empty entries."""
        assert _parse_disabled_tools(",,a,,b,") == frozenset({"a", "b"})

    def test_returns_frozenset(self) -> None:
        """Result is immutable so callers can't accidentally mutate it."""
        result = _parse_disabled_tools("a,b")
        assert isinstance(result, frozenset)


# ---------------------------------------------------------------------------
# _optional_tool — decorator behavior with monkeypatched disabled set
# ---------------------------------------------------------------------------


class TestOptionalToolDecorator:
    """``_optional_tool`` registers conditionally based on ``_DISABLED_TOOLS``."""

    def test_disabled_tool_not_registered(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Disabled tools never call mcp.tool() — they pass through unwrapped."""
        monkeypatch.setattr(mcp_server, "_DISABLED_TOOLS", frozenset({"my_tool"}))

        registration_calls: list[str] = []

        def fake_tool():
            def deco(func):
                registration_calls.append(func.__name__)
                return func
            return deco

        monkeypatch.setattr(mcp_server.mcp, "tool", fake_tool)

        @_optional_tool()
        def my_tool() -> str:
            return "hello"

        assert registration_calls == [], (
            "Disabled tool should not have been passed to mcp.tool()"
        )

    def test_disabled_tool_still_callable(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Disabled tool function is returned unchanged — still importable + callable."""
        monkeypatch.setattr(mcp_server, "_DISABLED_TOOLS", frozenset({"my_tool"}))

        @_optional_tool()
        def my_tool() -> str:
            return "still works"

        assert my_tool() == "still works"

    def test_enabled_tool_is_registered(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Tools NOT in the disabled set go through mcp.tool() normally."""
        monkeypatch.setattr(mcp_server, "_DISABLED_TOOLS", frozenset())

        registration_calls: list[str] = []

        def fake_tool():
            def deco(func):
                registration_calls.append(func.__name__)
                return func
            return deco

        monkeypatch.setattr(mcp_server.mcp, "tool", fake_tool)

        @_optional_tool()
        def my_tool() -> str:
            return "registered"

        assert registration_calls == ["my_tool"]

    def test_partial_disable_filters_correctly(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Only the named tool is filtered; others register as usual."""
        monkeypatch.setattr(
            mcp_server, "_DISABLED_TOOLS", frozenset({"hidden_tool"})
        )

        registered: list[str] = []

        def fake_tool():
            def deco(func):
                registered.append(func.__name__)
                return func
            return deco

        monkeypatch.setattr(mcp_server.mcp, "tool", fake_tool)

        @_optional_tool()
        def hidden_tool() -> str:
            return "x"

        @_optional_tool()
        def visible_tool() -> str:
            return "y"

        assert registered == ["visible_tool"]


# ---------------------------------------------------------------------------
# Integration with FastMCP — confirm disabled tools are absent from the
# actual MCP tool listing
# ---------------------------------------------------------------------------


class TestFastMCPIntegration:
    """End-to-end: disabled tools don't appear in mcp.list_tools()."""

    def test_disabled_tool_absent_from_list_tools(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A fresh FastMCP + monkeypatched disabled set proves the filter takes effect."""
        fake_mcp = FastMCP("test_disable_filter")
        monkeypatch.setattr(mcp_server, "mcp", fake_mcp)
        monkeypatch.setattr(
            mcp_server, "_DISABLED_TOOLS", frozenset({"hidden_tool"})
        )

        @_optional_tool()
        def hidden_tool() -> str:
            """A tool that should be filtered out."""
            return "hidden"

        @_optional_tool()
        def visible_tool() -> str:
            """A tool that should appear in the listing."""
            return "visible"

        tools = asyncio.run(fake_mcp.list_tools())
        tool_names = {t.name for t in tools}

        assert "visible_tool" in tool_names, (
            f"Enabled tool missing from listing: {tool_names}"
        )
        assert "hidden_tool" not in tool_names, (
            f"Disabled tool leaked into listing: {tool_names}"
        )

    def test_no_disabled_tools_lists_all(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """With an empty disabled set, every tool registers normally."""
        fake_mcp = FastMCP("test_no_filter")
        monkeypatch.setattr(mcp_server, "mcp", fake_mcp)
        monkeypatch.setattr(mcp_server, "_DISABLED_TOOLS", frozenset())

        @_optional_tool()
        def tool_a() -> str:
            return "a"

        @_optional_tool()
        def tool_b() -> str:
            return "b"

        tools = asyncio.run(fake_mcp.list_tools())
        tool_names = {t.name for t in tools}

        assert tool_names >= {"tool_a", "tool_b"}, (
            f"Expected both tools registered, got {tool_names}"
        )
