"""Tests for :mod:`deliberator.registry.runtime` (spec 064.1).

Verifies the runtime registration helpers that complement spec 064's
discovery primitive. Mock-based — these tests do NOT install real wheels
or spawn real MCP servers; that's the job of the integration smoke
harness in the private ``deliberator-enhanced`` repo.

Coverage:

- empty discovery → no-op return value
- per-surface filtering: capability surfaces=[CLI] is skipped by
  register_discovered_mcp_tools and vice versa
- handler-resolution failure is isolated (other capabilities still register)
- mcp.add_tool raising is isolated
- click command construction maps params correctly
- click command callback runs the handler and prints the result
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import click
import pytest
from click.testing import CliRunner

from deliberator.registry import (
    Capability,
    Param,
    Surface,
    register_discovered_cli_commands,
    register_discovered_mcp_tools,
)
from deliberator.registry import runtime as runtime_module


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stub_handler(**kwargs: Any) -> dict[str, Any]:
    """Default handler used by test capabilities."""
    return {"got": kwargs}


def _make_capability(
    name: str = "stub",
    surfaces: list[Surface] | None = None,
    handler: str = "deliberator.registry.tests.test_runtime:_stub_handler",
    params: list[Param] | None = None,
) -> Capability:
    return Capability(
        name=name,
        summary=f"stub {name}",
        surfaces=surfaces if surfaces is not None else [Surface.CLI, Surface.MCP],
        params=params if params is not None else [],
        handler=handler,
    )


# ---------------------------------------------------------------------------
# MCP registration
# ---------------------------------------------------------------------------


def test_register_mcp_no_capabilities_returns_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [])
    mcp = MagicMock()
    assert register_discovered_mcp_tools(mcp) == 0
    mcp.add_tool.assert_not_called()


def test_register_mcp_skips_non_mcp_surfaces(monkeypatch: pytest.MonkeyPatch) -> None:
    cli_only = _make_capability("cli_only", surfaces=[Surface.CLI])
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [cli_only])
    mcp = MagicMock()
    assert register_discovered_mcp_tools(mcp) == 0
    mcp.add_tool.assert_not_called()


def test_register_mcp_uses_deliberator_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    cap = _make_capability("foo", surfaces=[Surface.MCP])
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [cap])
    mcp = MagicMock()
    register_discovered_mcp_tools(mcp)
    mcp.add_tool.assert_called_once()
    _, kwargs = mcp.add_tool.call_args
    assert kwargs["name"] == "deliberator_foo"
    assert kwargs["description"] == "stub foo"


def test_register_mcp_uses_adapter_description_when_set(monkeypatch: pytest.MonkeyPatch) -> None:
    from deliberator.registry.adapters.mcp import DefaultMCPAdapter

    class VerboseAdapter(DefaultMCPAdapter):
        description = "Verbose tool description for Claude Desktop"

    cap = _make_capability("decide", surfaces=[Surface.MCP])
    cap.mcp_adapter = VerboseAdapter()
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [cap])
    mcp = MagicMock()
    register_discovered_mcp_tools(mcp)
    _, kwargs = mcp.add_tool.call_args
    assert kwargs["description"] == "Verbose tool description for Claude Desktop"


def test_register_mcp_isolates_handler_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """A bad handler import on one cap doesn't break the others."""
    bad = _make_capability(
        "bad", surfaces=[Surface.MCP], handler="nonexistent.module:fn"
    )
    good = _make_capability("good", surfaces=[Surface.MCP])
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [bad, good])
    mcp = MagicMock()
    assert register_discovered_mcp_tools(mcp) == 1
    mcp.add_tool.assert_called_once()


def test_register_mcp_isolates_add_tool_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """If mcp.add_tool raises for one cap, others still register."""
    a = _make_capability("a", surfaces=[Surface.MCP])
    b = _make_capability("b", surfaces=[Surface.MCP])
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [a, b])
    mcp = MagicMock()
    mcp.add_tool.side_effect = [RuntimeError("name collision"), None]
    assert register_discovered_mcp_tools(mcp) == 1
    assert mcp.add_tool.call_count == 2


# ---------------------------------------------------------------------------
# CLI registration
# ---------------------------------------------------------------------------


def test_register_cli_no_capabilities_returns_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [])
    cli = click.Group("deliberator")
    assert register_discovered_cli_commands(cli) == 0
    assert cli.commands == {}


def test_register_cli_skips_non_cli_surfaces(monkeypatch: pytest.MonkeyPatch) -> None:
    mcp_only = _make_capability("mcp_only", surfaces=[Surface.MCP])
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [mcp_only])
    cli = click.Group("deliberator")
    assert register_discovered_cli_commands(cli) == 0
    assert cli.commands == {}


def test_register_cli_adds_command_with_capability_name(monkeypatch: pytest.MonkeyPatch) -> None:
    cap = _make_capability("solver", surfaces=[Surface.CLI])
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [cap])
    cli = click.Group("deliberator")
    assert register_discovered_cli_commands(cli) == 1
    assert "solver" in cli.commands
    assert cli.commands["solver"].help == "stub solver"


def test_register_cli_maps_params_to_options(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each capability Param becomes a click Option keyed on --name."""
    cap = _make_capability(
        "solver",
        surfaces=[Surface.CLI],
        params=[
            Param(name="question", type=str, required=True, help="What to ask"),
            Param(name="max_iter", type=int, required=False, default=3),
        ],
    )
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [cap])
    cli = click.Group("deliberator")
    register_discovered_cli_commands(cli)
    cmd = cli.commands["solver"]
    option_names = {p.name for p in cmd.params}
    assert option_names == {"question", "max_iter"}


def test_register_cli_callback_invokes_handler_and_prints(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End-to-end: click invocation runs the handler and prints the result."""
    cap = _make_capability(
        "echo",
        surfaces=[Surface.CLI],
        params=[Param(name="msg", type=str, required=True)],
    )
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [cap])
    cli = click.Group("deliberator")
    register_discovered_cli_commands(cli)
    runner = CliRunner()
    result = runner.invoke(cli, ["echo", "--msg", "hello"])
    assert result.exit_code == 0, result.output
    # The stub handler returns {"got": {"msg": "hello"}} which the
    # callback renders as JSON
    assert '"msg": "hello"' in result.output


def test_register_cli_isolates_handler_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    bad = _make_capability(
        "bad", surfaces=[Surface.CLI], handler="nonexistent.module:fn"
    )
    good = _make_capability("good", surfaces=[Surface.CLI])
    monkeypatch.setattr(runtime_module, "collect_capabilities", lambda: [bad, good])
    cli = click.Group("deliberator")
    assert register_discovered_cli_commands(cli) == 1
    assert "good" in cli.commands
    assert "bad" not in cli.commands


# ---------------------------------------------------------------------------
# Handler resolution
# ---------------------------------------------------------------------------


def test_resolve_handler_rejects_missing_colon() -> None:
    with pytest.raises(ValueError, match="module:function"):
        runtime_module._resolve_handler("nocolon")


def test_resolve_handler_raises_on_missing_module() -> None:
    with pytest.raises(ImportError):
        runtime_module._resolve_handler("nonexistent_xyz_pkg:fn")


def test_resolve_handler_raises_on_missing_attr() -> None:
    with pytest.raises(AttributeError):
        runtime_module._resolve_handler(
            "deliberator.registry.tests.test_runtime:does_not_exist"
        )
