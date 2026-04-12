"""Day 6 validation: run + validate migrations functional equivalence.

Spec 055 §4 Day 6 validation criteria:

    - All existing tests pass against the regenerated ``engine/cli/__init__.py``
      and ``mcp_server.py``.
    - ``mcp_server.py`` regenerated from the registry produces the same 3
      tools with the same JSON schemas (Claude Desktop's existing ``.mcpb``
      install continues to work without re-registration).

Behavioral equivalence of the actual pipeline execution is proven
transitively by the existing 63-test ``linter/test_mcp_server.py`` suite,
which imports ``_run_config``, ``_validate_config``, and
``_run_in_process`` from ``mcp_server`` — all three are now aliases for
``engine.handlers.run_mcp``, ``engine.handlers.validate_mcp``, and
``engine.handlers._run_in_process`` respectively. Every pre-existing
behavioral test therefore runs against the new canonical handlers.

This file adds the *structural* assertions: generated signatures match
hand-written ones, per-surface params filter correctly, and the
Capability declarations route to the right handlers.
"""

from __future__ import annotations

import inspect
import sys
import types
from pathlib import Path

import click
import pytest

from conversus.registry.projector import (
    project_to_cli,
    project_to_mcp,
    project_to_plugin_skills,
)


# ---------------------------------------------------------------------------
# Fixture — the real 3-capability registry
# ---------------------------------------------------------------------------


@pytest.fixture
def real_capabilities():
    repo_root = Path(__file__).resolve().parent.parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    import capabilities
    return list(capabilities.CAPABILITIES)


@pytest.fixture
def generated_cli_namespace(real_capabilities) -> dict:
    """Exec the generated CLI source in a clean namespace and return it."""
    source = project_to_cli(real_capabilities)
    ns: dict = {"click": click, "Path": Path}
    exec(compile(source, "<day6-cli>", "exec"), ns)
    return ns


@pytest.fixture
def generated_mcp_namespace(real_capabilities) -> dict:
    """Exec the generated MCP source with a stubbed FastMCP."""
    source = project_to_mcp(real_capabilities)
    return _exec_mcp_source(source)


# ---------------------------------------------------------------------------
# run: CLI surface
# ---------------------------------------------------------------------------


def test_generated_run_cli_registers_click_command(generated_cli_namespace):
    assert "run" in generated_cli_namespace["cli"].commands
    cmd = generated_cli_namespace["cli"].commands["run"]
    assert isinstance(cmd, click.Command)


def test_generated_run_cli_has_config_path_argument(generated_cli_namespace):
    cmd = generated_cli_namespace["cli"].commands["run"]
    param_names = [p.name for p in cmd.params]
    # config_path is a required positional argument
    assert "config_path" in param_names
    config_param = next(p for p in cmd.params if p.name == "config_path")
    assert config_param.required is True


def test_generated_run_cli_has_all_flag_options(generated_cli_namespace):
    """Hand-written run CLI has --provider, --model, --rounds, --phase."""
    cmd = generated_cli_namespace["cli"].commands["run"]
    param_names = {p.name for p in cmd.params}
    assert {"provider", "model", "rounds", "phase"} <= param_names


def test_generated_run_cli_dispatches_to_run_cli_handler(real_capabilities):
    source = project_to_cli(real_capabilities)
    assert "from engine.handlers import run_cli" in source
    assert "return run_cli(" in source
    # CLI-only params only
    assert "config_yaml" not in source.split("def run(")[1].split("def validate(")[0]
    assert "output_path" not in source.split("def run(")[1].split("def validate(")[0]


# ---------------------------------------------------------------------------
# run: MCP surface
# ---------------------------------------------------------------------------


def test_generated_run_mcp_has_same_signature_as_hand_written(generated_mcp_namespace):
    """Hand-written: ``conversus_run(config_yaml: str, output_path: str = "",
    provider: str = "")``. Parameter *set* must match exactly — ordering
    is allowed to differ because every existing call site uses kwargs."""
    fn = generated_mcp_namespace["conversus_run"]
    sig = inspect.signature(fn)
    param_names = set(sig.parameters.keys())

    assert param_names == {"config_yaml", "provider", "output_path"}

    # config_yaml is required
    assert sig.parameters["config_yaml"].default is inspect.Parameter.empty
    # provider and output_path default to empty string
    assert sig.parameters["provider"].default == ""
    assert sig.parameters["output_path"].default == ""


def test_generated_run_mcp_dispatches_to_run_mcp_handler(real_capabilities):
    source = project_to_mcp(real_capabilities)
    assert "from engine.handlers import run_mcp" in source
    # CLI-only params must NOT leak. Match the parameter declaration shape
    # (e.g. ``model: str``, ``phase: str``) rather than the bare word, so
    # the ``phase`` appearing in the docstring ("5-phase pipeline") doesn't
    # trip the assertion.
    run_block = source.split("def conversus_run(")[1].split("def conversus_validate(")[0]
    assert "config_path" not in run_block
    assert "model: str" not in run_block
    assert "rounds: int" not in run_block
    assert "phase: str" not in run_block


# ---------------------------------------------------------------------------
# validate: CLI surface
# ---------------------------------------------------------------------------


def test_generated_validate_cli_registers_click_command(generated_cli_namespace):
    assert "validate" in generated_cli_namespace["cli"].commands
    cmd = generated_cli_namespace["cli"].commands["validate"]
    assert isinstance(cmd, click.Command)


def test_generated_validate_cli_has_config_path_and_optional_question(
    generated_cli_namespace,
):
    cmd = generated_cli_namespace["cli"].commands["validate"]
    config_param = next(p for p in cmd.params if p.name == "config_path")
    assert config_param.required is True

    question_param = next(p for p in cmd.params if p.name == "question")
    assert question_param.required is False
    assert question_param.default is None


def test_generated_validate_cli_dispatches_to_validate_cli_handler(real_capabilities):
    source = project_to_cli(real_capabilities)
    assert "from engine.handlers import validate_cli" in source
    assert "return validate_cli(" in source


# ---------------------------------------------------------------------------
# validate: MCP surface
# ---------------------------------------------------------------------------


def test_generated_validate_mcp_has_same_signature_as_hand_written(
    generated_mcp_namespace,
):
    """Hand-written: ``conversus_validate(config_yaml: str, question: str = "")``"""
    fn = generated_mcp_namespace["conversus_validate"]
    sig = inspect.signature(fn)
    param_names = list(sig.parameters.keys())

    assert param_names == ["config_yaml", "question"]
    assert sig.parameters["config_yaml"].default is inspect.Parameter.empty
    assert sig.parameters["question"].default == ""


def test_generated_validate_mcp_dispatches_to_validate_mcp_handler(real_capabilities):
    source = project_to_mcp(real_capabilities)
    assert "from engine.handlers import validate_mcp" in source


# ---------------------------------------------------------------------------
# Principle XI — single source of truth for the new handlers
# ---------------------------------------------------------------------------


def test_mcp_server_run_config_is_alias_for_handlers_run_mcp():
    """After Day 6, ``mcp_server._run_config`` and
    ``engine.handlers.run_mcp`` must be the same function object."""
    from mcp_server import _run_config
    from engine.handlers import run_mcp

    assert _run_config is run_mcp


def test_mcp_server_validate_config_is_alias_for_handlers_validate_mcp():
    from mcp_server import _validate_config
    from engine.handlers import validate_mcp

    assert _validate_config is validate_mcp


def test_mcp_server_run_in_process_is_alias_for_handlers_run_in_process():
    from mcp_server import _run_in_process as from_mcp
    from engine.handlers import _run_in_process as from_handlers

    assert from_mcp is from_handlers


def test_mcp_server_parse_and_validate_config_is_alias_for_handlers():
    from mcp_server import _parse_and_validate_config as from_mcp
    from engine.handlers import _parse_and_validate_config as from_handlers

    assert from_mcp is from_handlers


def test_validate_result_is_single_definition():
    from engine.results import ValidateResult as canonical
    from mcp_server import ValidateResult as from_mcp

    assert canonical is from_mcp


def test_run_result_is_single_definition():
    from engine.results import RunResult as canonical
    from mcp_server import RunResult as from_mcp

    assert canonical is from_mcp


# ---------------------------------------------------------------------------
# Per-surface isolation — CLI params don't leak into MCP and vice versa
# ---------------------------------------------------------------------------


def test_cli_run_has_model_rounds_phase_but_mcp_run_does_not(real_capabilities):
    cli_source = project_to_cli(real_capabilities)
    mcp_source = project_to_mcp(real_capabilities)

    # CLI-only params appear in the CLI block for run
    cli_run_block = cli_source.split("def run(")[1].split("def validate(")[0]
    assert "model: str" in cli_run_block
    assert "rounds: int" in cli_run_block
    assert "phase: str" in cli_run_block

    # MCP run doesn't see these
    mcp_run_block = mcp_source.split("def conversus_run(")[1].split("def conversus_validate(")[0]
    assert "model:" not in mcp_run_block
    assert "rounds:" not in mcp_run_block
    assert "phase:" not in mcp_run_block


def test_mcp_run_has_config_yaml_and_output_path_but_cli_run_does_not(real_capabilities):
    cli_source = project_to_cli(real_capabilities)
    mcp_source = project_to_mcp(real_capabilities)

    cli_run_block = cli_source.split("def run(")[1].split("def validate(")[0]
    assert "config_yaml" not in cli_run_block
    assert "output_path" not in cli_run_block

    mcp_run_block = mcp_source.split("def conversus_run(")[1].split("def conversus_validate(")[0]
    assert "config_yaml: str" in mcp_run_block
    assert "output_path" in mcp_run_block


# ---------------------------------------------------------------------------
# Plugin SKILL.md projection
# ---------------------------------------------------------------------------


def test_all_plugin_opted_skills_generated(real_capabilities):
    """Every capability that opts into Surface.PLUGIN gets a SKILL.md."""
    from conversus.registry.params import Surface

    skills = project_to_plugin_skills(real_capabilities)
    expected = {
        cap.name
        for cap in real_capabilities
        if Surface.PLUGIN in cap.surfaces
    }
    assert set(skills.keys()) == expected
    # Spot-check that generated skills (not the design override) have
    # the standard frontmatter structure.
    for name in ["decide", "run", "validate"]:
        md = skills[name]
        assert md.startswith("---\n")
        assert "## Step 0: Check installation" in md


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _exec_mcp_source(source: str) -> dict:
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
        exec(compile(source, "<day6-mcp>", "exec"), ns)
        return ns
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
