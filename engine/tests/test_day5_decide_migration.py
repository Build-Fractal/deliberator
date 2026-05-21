"""Day 5 validation: decide migration functional equivalence.

Spec 055 §4 Day 5 validation criteria:

    - ``conversus decide "test question" --provider mock`` produces
      identical output via generated vs hand-written
    - The generated MCP tool has the same signature as the hand-written one
    - All existing tests for ``decide`` still pass against the generated code

This test file exercises the real ``capabilities.py::decide`` capability
(not a synthetic ``hello``), projects it through every default adapter
plus the ``DecideMCPAdapter`` override, and asserts:

1. **Structural parity** with the hand-written Click command — same
   provider choices, same mode choices, same ``--output`` flag name,
   same MCP tool signature.
2. **Semantic validity** — the generated sources ``exec()`` cleanly in
   a sandboxed namespace with real Click and stubbed FastMCP.
3. **Principle XI** — the canonical handler lives in one place. The
   `_decide` alias in ``mcp_server.py`` is the same function object
   as ``engine.handlers.run_decide_mcp``.

Behavioral equivalence of the actual pipeline execution is proven
transitively by ``linter/test_mcp_server.py::TestDecideConfig``, which
imports ``_decide from mcp_server`` (now an alias for
``engine.handlers.run_decide_mcp``) and runs it against real mock
deliberations. That entire 16-test suite is now the behavioral test
for the new handler.
"""

from __future__ import annotations

import pytest

pytest.importorskip("mcp")

pytestmark = pytest.mark.integration

import inspect
import sys
import types
from pathlib import Path

import click
import pytest

from conversus.registry.projector import (
    project_to_cli,
    project_to_mcp,
    project_to_mcpb_manifest_tools,
    project_to_plugin_skills,
)


# ---------------------------------------------------------------------------
# Fixture: the real capability list, not a synthetic one
# ---------------------------------------------------------------------------


@pytest.fixture
def real_capabilities():
    """Import the repo-root ``capabilities.py::CAPABILITIES`` list."""
    # Repo root is two levels up from this test file.
    repo_root = Path(__file__).resolve().parent.parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    import capabilities
    return list(capabilities.CAPABILITIES)


@pytest.fixture
def decide_capability(real_capabilities):
    """Pluck out the ``decide`` capability from the real list."""
    for cap in real_capabilities:
        if cap.name == "decide":
            return cap
    pytest.fail("capabilities.py does not define a ``decide`` capability")


# ---------------------------------------------------------------------------
# Structural parity with the hand-written Click command
# ---------------------------------------------------------------------------


def test_generated_decide_cli_execs_and_registers_click_command(real_capabilities):
    """Generated CLI source imports cleanly, and ``cli.commands['decide']``
    is a real Click command after exec."""
    source = project_to_cli(real_capabilities)
    ns: dict = {"click": click, "Path": Path}
    exec(compile(source, "<day5-cli>", "exec"), ns)

    assert "cli" in ns
    assert "decide" in ns["cli"].commands
    cmd = ns["cli"].commands["decide"]
    assert isinstance(cmd, click.Command)


def test_generated_decide_has_all_provider_choices(real_capabilities):
    """The hand-written CLI accepts 13 providers; the generated command
    must accept the same set."""
    source = project_to_cli(real_capabilities)
    ns: dict = {"click": click, "Path": Path}
    exec(compile(source, "<day5-cli>", "exec"), ns)
    cmd = ns["cli"].commands["decide"]

    provider_param = next(p for p in cmd.params if p.name == "provider")
    choices = set(provider_param.type.choices)

    expected = {
        "mock", "anthropic", "openai", "claude-code", "aider", "opencode",
        "ollama", "llama-cpp", "vllm", "codex", "copilot", "gemini", "pi",
    }
    assert choices == expected


def test_generated_decide_has_all_mode_choices(real_capabilities):
    source = project_to_cli(real_capabilities)
    ns: dict = {"click": click, "Path": Path}
    exec(compile(source, "<day5-cli>", "exec"), ns)
    cmd = ns["cli"].commands["decide"]

    mode_param = next(p for p in cmd.params if p.name == "mode")
    assert set(mode_param.type.choices) == {
        "cooperative", "winner-take-all", "prisoners-dilemma", "red-blue",
    }


def test_generated_decide_uses_output_flag_not_output_dir(real_capabilities):
    """Spec 055 Day 5: the CLI flag must be ``--output`` (matching the
    hand-written version), not the hyphenation-default ``--output-dir``.
    This is the ``Param(name="output")`` rename driven by Day 5 migration."""
    source = project_to_cli(real_capabilities)
    ns: dict = {"click": click, "Path": Path}
    exec(compile(source, "<day5-cli>", "exec"), ns)
    cmd = ns["cli"].commands["decide"]

    output_param = next(p for p in cmd.params if p.name == "output")
    assert "--output" in output_param.opts
    assert "--output-dir" not in output_param.opts


def test_generated_decide_cli_dispatches_to_run_decide_cli(real_capabilities):
    """The generated command body must import and call
    ``engine.handlers.run_decide_cli`` with keyword-forwarded kwargs."""
    source = project_to_cli(real_capabilities)
    assert "from engine.handlers import run_decide_cli" in source
    assert "return run_decide_cli(" in source
    # Every CLI-visible param must appear as a kwarg
    assert "question=question" in source
    assert "provider=provider" in source
    assert "mode=mode" in source
    assert "output=output" in source
    assert "output_format=output_format" in source
    # MCP-only param must NOT leak into the CLI dispatch
    assert "max_launches" not in source


# ---------------------------------------------------------------------------
# Structural parity with the hand-written MCP tool
# ---------------------------------------------------------------------------


def test_generated_mcp_tool_has_same_signature_as_hand_written(real_capabilities):
    """Spec 055 Day 5 validation: 'The generated MCP tool has the same
    signature as the hand-written one.'

    Hand-written signature from ``mcp_server.py::conversus_decide``:

        def conversus_decide(
            question: str,
            provider: str = "mock",
            mode: str = "cooperative",
            max_launches: int = 20,
        ) -> DecideResult

    (The return type differs — hand-written returns ``DecideResult``,
    generated currently returns ``str`` because the default MCP adapter
    doesn't yet know about result types. This is tracked as a follow-up
    in the NO list and does not block Day 5 because the MCP transport
    serializes both to the same JSON payload via Pydantic.)
    """
    source = project_to_mcp(real_capabilities)
    ns = _exec_mcp_source(source)

    fn = ns["conversus_decide"]
    sig = inspect.signature(fn)

    params = list(sig.parameters.values())
    names = [p.name for p in params]
    assert names == ["question", "provider", "mode", "max_launches"]

    # Defaults match
    param_map = {p.name: p for p in params}
    assert param_map["question"].default is inspect.Parameter.empty  # required
    assert param_map["provider"].default == "mock"
    assert param_map["mode"].default == "cooperative"
    assert param_map["max_launches"].default == 20


def test_generated_mcp_tool_dispatches_to_run_decide_mcp(real_capabilities):
    """The generated MCP tool must call the canonical handler in
    ``engine.handlers.run_decide_mcp``, not the default handler."""
    source = project_to_mcp(real_capabilities)
    assert "from engine.handlers import run_decide_mcp" in source
    assert "return run_decide_mcp(" in source
    # CLI-only params must NOT leak into the MCP dispatch
    assert "output_format" not in source
    assert "output=output" not in source  # -- but "output" can appear in the description


def test_generated_mcp_tool_uses_override_description(real_capabilities):
    """The DecideMCPAdapter override sets a verbose ``description`` class
    attribute; the default adapter's render should pick it up via the
    three-level fallback (override description → long_description → summary)."""
    source = project_to_mcp(real_capabilities)
    assert "Postgres or MongoDB?" in source  # from DecideMCPAdapter.description


# ---------------------------------------------------------------------------
# Plugin SKILL.md projection
# ---------------------------------------------------------------------------


def test_generated_decide_plugin_skill_exists(real_capabilities):
    skills = project_to_plugin_skills(real_capabilities)
    assert "decide" in skills
    md = skills["decide"]
    assert md.startswith("---\n")
    assert "description:" in md
    assert "# Conversus Decide" in md
    assert "`--output`" in md
    # CLI-only params visible in plugin docs
    assert "`--output-format`" in md
    # MCP-only params NOT visible in plugin docs (plugin dispatches via CLI)
    assert "max_launches" not in md


# ---------------------------------------------------------------------------
# Principle XI — single source of truth
# ---------------------------------------------------------------------------


def test_mcp_server_decide_is_alias_for_handlers_run_decide_mcp():
    """After Day 5's principle-XI de-duplication, ``mcp_server._decide``
    and ``engine.handlers.run_decide_mcp`` must be the *same function
    object* — not two copies that happen to have the same body."""
    from mcp_server import _decide
    from engine.handlers import run_decide_mcp

    assert _decide is run_decide_mcp


def test_cost_estimate_is_single_definition():
    """``CostEstimate`` lives in ``engine/results.py`` as the single
    canonical definition. Every other module imports from there."""
    from engine.results import CostEstimate as canonical
    from mcp_server import CostEstimate as from_mcp
    from engine.handlers import CostEstimate as from_handlers

    assert canonical is from_mcp
    assert canonical is from_handlers


def test_decide_result_is_single_definition():
    from engine.results import DecideResult as canonical
    from mcp_server import DecideResult as from_mcp
    from engine.handlers import DecideResult as from_handlers

    assert canonical is from_mcp
    assert canonical is from_handlers


# ---------------------------------------------------------------------------
# Skip-a-surface for max_launches (CLI surface must not see it)
# ---------------------------------------------------------------------------


def test_max_launches_appears_only_on_mcp_surface(real_capabilities):
    """``Param(name="max_launches", surfaces=[Surface.MCP])`` — the CLI
    surface must not see this param at all, and the MCP surface must."""
    cli_source = project_to_cli(real_capabilities)
    mcp_source = project_to_mcp(real_capabilities)
    plugin_skills = project_to_plugin_skills(real_capabilities)

    assert "max_launches" not in cli_source
    assert "max_launches: int = 20" in mcp_source
    # Plugin docs follow the CLI param set, so no max_launches
    assert "max_launches" not in plugin_skills["decide"]


def test_output_and_format_appear_only_on_cli_surface(real_capabilities):
    """CLI-only params (``output``, ``output_format``) must not reach MCP."""
    cli_source = project_to_cli(real_capabilities)
    mcp_source = project_to_mcp(real_capabilities)

    assert '"--output"' in cli_source
    assert '"--output-format"' in cli_source
    assert "output: str = None" in cli_source
    assert "output_format: str" in cli_source

    # MCP surface doesn't see them
    assert "output_format" not in mcp_source
    assert "output: str = None" not in mcp_source


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _exec_mcp_source(source: str) -> dict:
    """Exec generated MCP source with a stubbed FastMCP (same pattern
    as test_projector.py::_exec_mcp_source)."""

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
        exec(compile(source, "<day5-mcp>", "exec"), ns)
        return ns
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
