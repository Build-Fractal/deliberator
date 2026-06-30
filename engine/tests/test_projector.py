"""Tests for the capability registry projector (spec 055).

Day 3-4 validation criterion (section 4, Day 3-4):

    A registry with a single sample capability (e.g., `hello`) is
    projected to all 4 surfaces. The CLI command runs, the MCP tool
    registers, the plugin skill loads, the manifest tools[] entry is
    valid JSON.

Constitutional alignment: every test builds its own explicit list of
``Capability`` instances and passes it to the projector function. No
module-level registry, no clear() fixture — principle IX (no mutable
module-level state).
"""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest

from deliberator.registry import (
    Capability,
    CLIAdapter,
    DefaultCLIAdapter,
    DefaultMCPAdapter,
    MCPAdapter,
    Param,
    Surface,
)
from deliberator.registry.projector import (
    project_to_cli,
    project_to_mcp,
    project_to_mcpb_manifest_tools,
    project_to_plugin_skills,
)


# ---------------------------------------------------------------------------
# Fixtures — explicit lists, no module state
# ---------------------------------------------------------------------------


@pytest.fixture
def hello_capability() -> Capability:
    """A minimal sample capability exercising both arg and option paths."""
    return Capability(
        name="hello",
        summary="Say hello to someone",
        long_description="Greet a person by name, optionally in all caps.",
        surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
        params=[
            Param(name="who", type=str, required=True, help="Who to greet."),
            Param(
                name="loud",
                type=bool,
                default=False,
                help="Shout instead of whispering.",
            ),
        ],
        handler="deliberator.demo:say_hello",
    )


@pytest.fixture
def hello_list(hello_capability: Capability) -> list[Capability]:
    return [hello_capability]


# ---------------------------------------------------------------------------
# Helpers: exec generated source in a sandbox namespace
#
# ``exec()`` is strictly stronger than ``ast.parse()`` for validating
# generated code — it actually runs decorators at def time, so bad
# identifiers (e.g. ``default=false`` instead of ``default=False``) would
# raise NameError here instead of slipping through AST parsing.
# ---------------------------------------------------------------------------


def _exec_cli_source(source: str) -> dict:
    """Exec generated CLI source with a real ``click`` import."""
    import click

    ns = {"click": click, "Path": Path}
    exec(compile(source, "<generated-cli>", "exec"), ns)
    return ns


def _exec_mcp_source(source: str) -> dict:
    """Exec generated MCP source with a stubbed FastMCP.

    We don't want the test to depend on the real ``mcp`` package. A fake
    FastMCP that records ``.tool()`` registrations is enough.
    """

    class FakeFastMCP:
        def __init__(self, name):
            self.name = name
            self.tools: list = []

        def tool(self):
            def deco(fn):
                self.tools.append(fn)
                return fn
            return deco

        def run(self, transport="stdio"):
            pass

    fake_mcp = types.ModuleType("mcp")
    fake_server = types.ModuleType("mcp.server")
    fake_fastmcp_mod = types.ModuleType("mcp.server.fastmcp")
    fake_fastmcp_mod.FastMCP = FakeFastMCP
    fake_server.fastmcp = fake_fastmcp_mod
    fake_mcp.server = fake_server

    saved = {k: sys.modules.get(k) for k in (
        "mcp", "mcp.server", "mcp.server.fastmcp",
    )}
    sys.modules["mcp"] = fake_mcp
    sys.modules["mcp.server"] = fake_server
    sys.modules["mcp.server.fastmcp"] = fake_fastmcp_mod
    try:
        ns: dict = {}
        exec(compile(source, "<generated-mcp>", "exec"), ns)
        return ns
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v


# ---------------------------------------------------------------------------
# CLI projection
# ---------------------------------------------------------------------------


def test_project_to_cli_execs_cleanly(hello_list):
    """Strongest possible check — exec the generated CLI with real click.

    If the adapter ever emits a bad literal (``default=false`` instead of
    ``default=False``, ``default=null`` instead of ``default=None``), the
    decorator evaluation inside ``exec`` will raise NameError here.
    """
    source = project_to_cli(hello_list)
    ns = _exec_cli_source(source)
    assert "cli" in ns
    assert "hello" in ns
    assert "hello" in ns["cli"].commands


def test_project_to_cli_contains_expected_command_block(hello_list):
    source = project_to_cli(hello_list)
    # Preamble
    assert "import click" in source
    assert "def cli() -> None:" in source
    # Capability block
    assert '@cli.command("hello"' in source
    assert '@click.argument("who", type=str)' in source
    assert '@click.option(' in source
    assert '"--loud"' in source
    assert "def hello(who: str, loud: bool = False) -> None:" in source
    # Lazy handler import
    assert "from deliberator.demo import say_hello" in source
    assert "return say_hello(who=who, loud=loud)" in source


def test_cli_hyphenation_rewrites_underscore_params():
    """An ``optional_multi_word`` param becomes ``--optional-multi-word``."""
    caps = [
        Capability(
            name="demo",
            summary="demo",
            surfaces=[Surface.CLI],
            params=[Param(name="max_launches", type=int, default=20, help="Safety cap.")],
            handler="m:f",
        )
    ]

    source = project_to_cli(caps)
    assert '"--max-launches"' in source
    assert '"max_launches"' in source  # rebinding
    assert "def demo(max_launches: int = 20)" in source


def test_cli_choices_param_emits_click_choice():
    caps = [
        Capability(
            name="demo",
            summary="demo",
            surfaces=[Surface.CLI],
            params=[
                Param(
                    name="mode",
                    type=str,
                    default="cooperative",
                    choices=["cooperative", "winner-take-all", "red-blue"],
                    help="Mode.",
                ),
            ],
            handler="m:f",
        )
    ]

    source = project_to_cli(caps)
    assert "click.Choice(" in source
    assert '"cooperative"' in source
    assert '"winner-take-all"' in source
    assert "case_sensitive=False" in source


# ---------------------------------------------------------------------------
# MCP projection
# ---------------------------------------------------------------------------


def test_project_to_mcp_execs_cleanly(hello_list):
    source = project_to_mcp(hello_list)
    ns = _exec_mcp_source(source)
    assert "mcp" in ns
    assert "deliberator_hello" in ns
    tool_names = [fn.__name__ for fn in ns["mcp"].tools]
    assert "deliberator_hello" in tool_names


def test_project_to_mcp_contains_expected_tool_block(hello_list):
    source = project_to_mcp(hello_list)
    assert "from mcp.server.fastmcp import FastMCP" in source
    assert 'mcp = FastMCP("deliberator")' in source
    assert "@mcp.tool()" in source
    assert "def deliberator_hello(" in source
    assert "who: str" in source
    # Python bool literal — capital F, not "false" (JSON)
    assert "loud: bool = False" in source
    assert "from deliberator.demo import say_hello" in source
    assert 'mcp.run(transport="stdio")' in source


def test_mcp_uses_long_description_when_available(hello_list):
    source = project_to_mcp(hello_list)
    assert "Greet a person by name" in source


# ---------------------------------------------------------------------------
# Plugin SKILL.md projection
# ---------------------------------------------------------------------------


def test_project_to_plugin_skills_has_valid_frontmatter(hello_list):
    skills = project_to_plugin_skills(hello_list)
    assert "hello" in skills

    md = skills["hello"]
    assert md.startswith("---\n")
    frontmatter_end = md.index("\n---\n", 4)
    frontmatter = md[4:frontmatter_end]
    assert "description:" in frontmatter
    assert "Greet a person" in frontmatter


def test_plugin_skill_body_includes_install_check_and_run_section(hello_list):
    md = project_to_plugin_skills(hello_list)["hello"]
    assert "# Deliberator Hello" in md
    assert "## Step 0: Check installation" in md
    assert "deliberator --version" in md
    assert "## Step 1: Parse arguments" in md
    assert "`who` (required)" in md
    assert "`--loud`" in md
    assert "## Step 2: Run" in md
    assert 'deliberator hello "<who>"' in md
    assert "## Troubleshooting" in md
    assert "`deliberator hello --help`" in md


# ---------------------------------------------------------------------------
# MCPB manifest tools[] projection
# ---------------------------------------------------------------------------


def test_project_to_mcpb_manifest_tools_returns_valid_entries(hello_list):
    tools = project_to_mcpb_manifest_tools(hello_list)
    assert isinstance(tools, list)
    assert len(tools) == 1

    entry = tools[0]
    assert isinstance(entry, dict)  # TypedDict is a dict at runtime
    assert entry["name"] == "deliberator_hello"
    assert isinstance(entry["description"], str)
    assert "Greet a person" in entry["description"]
    # JSON round-trip (what the projector actually does)
    round_tripped = json.loads(json.dumps(entry))
    assert round_tripped == entry


def test_project_to_mcpb_description_is_single_line(hello_list):
    tools = project_to_mcpb_manifest_tools(hello_list)
    assert "\n" not in tools[0]["description"]


# ---------------------------------------------------------------------------
# Skip-a-surface — projector honors surfaces=[...] opt-in
# ---------------------------------------------------------------------------


def test_cli_only_capability_omitted_from_mcp_and_mcpb():
    caps = [
        Capability(
            name="login",
            summary="OAuth login",
            surfaces=[Surface.CLI, Surface.PLUGIN],  # not MCP, not MCPB
            params=[Param(name="provider", type=str, required=True)],
            handler="deliberator.engine.auth:oauth_login",
        )
    ]

    cli_source = project_to_cli(caps)
    mcp_source = project_to_mcp(caps)
    skills = project_to_plugin_skills(caps)
    mcpb_tools = project_to_mcpb_manifest_tools(caps)

    assert '@cli.command("login"' in cli_source
    assert "deliberator_login" not in mcp_source
    assert "login" in skills
    assert mcpb_tools == []


# ---------------------------------------------------------------------------
# Override adapters take precedence over defaults
# ---------------------------------------------------------------------------


def test_override_cli_adapter_replaces_default_projection():
    """``cap.cli_adapter or DefaultCLIAdapter()`` fallback must prefer the override."""

    class CustomCLIAdapter(DefaultCLIAdapter):
        def render(self, capability):
            return "# CUSTOM_CLI_MARKER"

    caps = [
        Capability(
            name="decide",
            summary="Run a deliberation",
            surfaces=[Surface.CLI],
            params=[Param(name="q", type=str, required=True)],
            handler="m:decide",
            cli_adapter=CustomCLIAdapter(),
        )
    ]

    source = project_to_cli(caps)
    assert "# CUSTOM_CLI_MARKER" in source
    assert '@cli.command("decide"' not in source


def test_override_mcp_adapter_replaces_default_projection():
    class CustomMCPAdapter(DefaultMCPAdapter):
        def render(self, capability):
            return "# CUSTOM_MCP_MARKER"

    caps = [
        Capability(
            name="decide",
            summary="Run a deliberation",
            surfaces=[Surface.MCP],
            params=[],
            handler="m:decide",
            mcp_adapter=CustomMCPAdapter(),
        )
    ]

    source = project_to_mcp(caps)
    assert "# CUSTOM_MCP_MARKER" in source
    assert "def deliberator_decide(" not in source


# ---------------------------------------------------------------------------
# Day 5 extensions — per-surface handlers and param visibility end-to-end
# ---------------------------------------------------------------------------


def test_per_surface_params_filtered_by_projector():
    """CLI-only and MCP-only params land in their correct generated source."""
    caps = [
        Capability(
            name="decide",
            summary="Run a deliberation",
            surfaces=[Surface.CLI, Surface.MCP],
            params=[
                Param(name="question", type=str, required=True),
                Param(
                    name="output_format",
                    type=str,
                    default="rich",
                    surfaces=[Surface.CLI],
                ),
                Param(
                    name="max_launches",
                    type=int,
                    default=20,
                    surfaces=[Surface.MCP],
                ),
            ],
            handler="engine.adhoc:run_decide",
        )
    ]

    cli_source = project_to_cli(caps)
    mcp_source = project_to_mcp(caps)

    # CLI gets output_format but NOT max_launches
    assert '"--output-format"' in cli_source
    assert "max_launches" not in cli_source
    assert "--max-launches" not in cli_source

    # MCP gets max_launches but NOT output_format
    assert "max_launches: int = 20" in mcp_source
    assert "output_format" not in mcp_source


def test_per_surface_handlers_routed_by_projector():
    """CLI projection calls ``handler_for(Surface.CLI)``; MCP calls
    ``handler_for(Surface.MCP)``. The two can differ."""
    caps = [
        Capability(
            name="decide",
            summary="Run a deliberation",
            surfaces=[Surface.CLI, Surface.MCP],
            params=[Param(name="q", type=str, required=True)],
            handler="engine.handlers:run_decide_cli",
            handlers={Surface.MCP: "engine.handlers:run_decide_mcp"},
        )
    ]

    cli_source = project_to_cli(caps)
    mcp_source = project_to_mcp(caps)

    assert "from engine.handlers import run_decide_cli" in cli_source
    assert "from engine.handlers import run_decide_mcp" in mcp_source
    # Crucially, they don't bleed across surfaces
    assert "run_decide_mcp" not in cli_source
    assert "run_decide_cli" not in mcp_source
