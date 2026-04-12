"""Tests for the capability registry data model (spec 055).

Covers Day 1-2 framework invariants plus the Day 5 framework extensions
(per-surface handlers, per-surface param visibility). Every test builds
its own explicit ``Capability`` instances — there is no module-level
registry to share state across tests, and no ``clear()`` fixture. This
is the constitutional principle IX (no mutable module-level state)
applied to the test suite.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from conversus.registry import (
    Capability,
    CLIAdapter,
    DefaultCLIAdapter,
    DefaultMCPAdapter,
    MCPAdapter,
    Param,
    Surface,
    for_surface,
    get,
)


# ---------------------------------------------------------------------------
# Capability construction and field access
# ---------------------------------------------------------------------------


def test_capability_construction_exposes_all_fields():
    cap = Capability(
        name="decide",
        summary="Run an ad-hoc deliberation",
        long_description="Quick deliberation without a config file.",
        surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
        params=[
            Param(name="question", type=str, required=True, help="Be specific."),
            Param(
                name="provider",
                type=str,
                default="mock",
                choices=["mock", "anthropic", "openai"],
                help="LLM provider.",
            ),
            Param(name="max_launches", type=int, default=20, help="Safety cap."),
        ],
        handler="conversus.engine.adhoc:run_decide",
    )

    assert cap.name == "decide"
    assert cap.summary == "Run an ad-hoc deliberation"
    assert cap.long_description.startswith("Quick deliberation")
    assert cap.handler == "conversus.engine.adhoc:run_decide"
    assert set(cap.surfaces) == {
        Surface.CLI,
        Surface.MCP,
        Surface.PLUGIN,
        Surface.MCPB,
    }

    names = [p.name for p in cap.params]
    assert names == ["question", "provider", "max_launches"]

    question = cap.params[0]
    assert question.required is True
    assert question.type is str
    assert question.help == "Be specific."

    provider = cap.params[1]
    assert provider.required is False
    assert provider.default == "mock"
    assert provider.choices == ["mock", "anthropic", "openai"]


def test_skip_a_surface_is_supported():
    cap = Capability(
        name="login",
        summary="OAuth login",
        surfaces=[Surface.CLI, Surface.PLUGIN],  # not MCP, not MCPB
        params=[Param(name="provider", type=str, required=True)],
        handler="conversus.engine.auth:oauth_login",
    )

    assert Surface.CLI in cap.surfaces
    assert Surface.PLUGIN in cap.surfaces
    assert Surface.MCP not in cap.surfaces
    assert Surface.MCPB not in cap.surfaces


# ---------------------------------------------------------------------------
# Override adapter attachment — via constructor kwargs and post-construction
# ---------------------------------------------------------------------------


def test_override_adapter_attaches_via_constructor():
    class CustomMCPAdapter(DefaultMCPAdapter):
        description = "Verbose MCP tool description for Claude's selection."

    cap = Capability(
        name="decide",
        summary="Run a deliberation",
        surfaces=[Surface.CLI, Surface.MCP],
        params=[Param(name="q", type=str, required=True)],
        handler="m:decide",
        mcp_adapter=CustomMCPAdapter(),
    )

    assert isinstance(cap.mcp_adapter, MCPAdapter)
    assert isinstance(cap.mcp_adapter, CustomMCPAdapter)
    assert cap.mcp_adapter.description.startswith("Verbose")
    # cli_adapter remains unset — overrides are per-surface and independent
    assert cap.cli_adapter is None


def test_override_adapter_attaches_post_construction():
    """``validate_assignment=True`` on Capability lets us set adapter
    slots after construction and still get type validation."""

    class CustomCLI(DefaultCLIAdapter):
        def render(self, capability):
            return "# custom"

    class CustomMCP(DefaultMCPAdapter):
        def render(self, capability):
            return "# custom"

    cap = Capability(
        name="decide",
        summary="Run a deliberation",
        surfaces=[Surface.CLI, Surface.MCP],
        params=[],
        handler="m:decide",
    )

    cap.cli_adapter = CustomCLI()
    cap.mcp_adapter = CustomMCP()

    assert isinstance(cap.cli_adapter, CustomCLI)
    assert isinstance(cap.mcp_adapter, CustomMCP)
    assert cap.plugin_adapter is None
    assert cap.mcpb_adapter is None


# ---------------------------------------------------------------------------
# Day 5 framework extensions — per-surface handlers + per-surface params
# ---------------------------------------------------------------------------


def test_per_surface_handlers_fall_back_to_default():
    """``handler_for(surface)`` returns the per-surface override if one
    is set, else the default ``handler``. Day 5 uses this so ``decide``
    can dispatch to ``run_decide_cli`` for CLI and ``run_decide_mcp``
    for MCP from a single capability declaration."""

    cap = Capability(
        name="decide",
        summary="",
        surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN],
        params=[],
        handler="engine.handlers:run_decide_cli",
        handlers={Surface.MCP: "engine.handlers:run_decide_mcp"},
    )

    assert cap.handler_for(Surface.CLI) == "engine.handlers:run_decide_cli"
    assert cap.handler_for(Surface.MCP) == "engine.handlers:run_decide_mcp"
    # Plugin has no override → falls back to default
    assert cap.handler_for(Surface.PLUGIN) == "engine.handlers:run_decide_cli"


def test_per_surface_param_visibility():
    """``Param.surfaces=[...]`` restricts a param to the listed surfaces.

    Day 5 uses this so ``decide`` can expose ``--format`` only on CLI
    (where rendering makes sense) and ``max_launches`` only on MCP
    (where the safety cap matters)."""
    shared = Param(name="question", type=str, required=True)
    cli_only = Param(
        name="output_format",
        type=str,
        default="rich",
        surfaces=[Surface.CLI],
    )
    mcp_only = Param(
        name="max_launches",
        type=int,
        default=20,
        surfaces=[Surface.MCP],
    )

    cap = Capability(
        name="decide",
        summary="",
        surfaces=[Surface.CLI, Surface.MCP],
        params=[shared, cli_only, mcp_only],
        handler="m:d",
    )

    cli_params = cap.params_for(Surface.CLI)
    assert [p.name for p in cli_params] == ["question", "output_format"]

    mcp_params = cap.params_for(Surface.MCP)
    assert [p.name for p in mcp_params] == ["question", "max_launches"]

    # Visibility predicate works on its own too
    assert shared.visible_on(Surface.CLI)
    assert shared.visible_on(Surface.MCP)
    assert cli_only.visible_on(Surface.CLI)
    assert not cli_only.visible_on(Surface.MCP)
    assert not mcp_only.visible_on(Surface.CLI)
    assert mcp_only.visible_on(Surface.MCP)


# ---------------------------------------------------------------------------
# Lookup helpers — pure functions over an explicit list
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_caps() -> list[Capability]:
    return [
        Capability(
            name="decide",
            summary="",
            surfaces=[Surface.CLI, Surface.MCP],
            params=[],
            handler="m:decide",
        ),
        Capability(
            name="run",
            summary="",
            surfaces=[Surface.CLI, Surface.MCP],
            params=[],
            handler="m:run",
        ),
        Capability(
            name="login",
            summary="",
            surfaces=[Surface.CLI],  # CLI-only
            params=[],
            handler="m:login",
        ),
    ]


def test_get_returns_capability_by_name(sample_caps):
    cap = get("run", sample_caps)
    assert cap.name == "run"


def test_get_raises_keyerror_for_missing_name(sample_caps):
    with pytest.raises(KeyError, match="no capability named 'missing'"):
        get("missing", sample_caps)


def test_for_surface_filters_by_surface_opt_in(sample_caps):
    mcp_caps = list(for_surface(Surface.MCP, sample_caps))
    assert [c.name for c in mcp_caps] == ["decide", "run"]

    cli_caps = list(for_surface(Surface.CLI, sample_caps))
    assert [c.name for c in cli_caps] == ["decide", "run", "login"]


# ---------------------------------------------------------------------------
# Pydantic validation — sanity checks that rejecting bad values still works
# ---------------------------------------------------------------------------


def test_capability_rejects_missing_required_fields():
    with pytest.raises(ValidationError):
        Capability(name="decide")  # missing summary, surfaces, params, handler


def test_param_rejects_any_type_default():
    """Day 5 constitutional compliance: Param.default is typed as
    ``str | int | bool | None``. Passing an object outside that set
    must be rejected by Pydantic validation."""
    with pytest.raises(ValidationError):
        Param(
            name="who",
            type=str,
            default={"not": "primitive"},  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# Surface is a StrEnum — principle IX compliance
# ---------------------------------------------------------------------------


def test_surface_is_strenum():
    """Principle IX: closed behavioral choices must use StrEnum."""
    from enum import StrEnum

    assert issubclass(Surface, StrEnum)
    # StrEnum members are string-equal to their values
    assert Surface.CLI == "cli"
    assert Surface.MCP == "mcp"
    assert Surface.PLUGIN == "plugin"
    assert Surface.MCPB == "mcpb"
