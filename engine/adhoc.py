"""Shared ad-hoc config generation for SDK, CLI, and MCP consumers.

Deduplicates the tempdir → question.md → conversus.yml pattern that was
previously copy-pasted across ``engine.sdk._run_ad_hoc``,
``engine.cli.decide``, and ``mcp_server._decide``.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Sequence

from engine._root import find_project_root
from engine.config import AGENT_NAME_RE, ConfigError


def _sanitize_agent_name(display_name: str) -> str:
    """Convert a display name like 'UX Reviewer' to a valid config name like 'ux-reviewer'.

    Rules match ``AGENT_NAME_RE``: lowercase alphanumeric with hyphens/underscores,
    must start with a letter or digit.
    """
    slug = display_name.strip().lower()
    # Replace spaces and consecutive non-alnum chars with a single hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    # Strip leading/trailing hyphens
    slug = slug.strip("-")
    return slug or "agent"


# ---------------------------------------------------------------------------
# Agent spec for custom agent configurations
# ---------------------------------------------------------------------------


class AgentSpec:
    """Lightweight description of an agent for ad-hoc config generation.

    Attributes:
        name: Agent display name (used in output filenames and prompts).
        preset: Preset path relative to the ``presets/`` directory,
            e.g. ``"philosophy/pragmatist"`` or ``"consumer/financial-analyst"``.
    """

    __slots__ = ("name", "preset")

    def __init__(self, name: str, preset: str) -> None:
        self.name = name
        self.preset = preset

    def __repr__(self) -> str:
        return f"AgentSpec(name={self.name!r}, preset={self.preset!r})"


# Default agents when none are specified (backward-compatible)
DEFAULT_AGENTS: tuple[AgentSpec, ...] = (
    AgentSpec(name="pragmatist", preset="philosophy/pragmatist"),
    AgentSpec(name="devils-advocate", preset="role/devils-advocate"),
)

# Red-blue mode requires agents with role: red / role: blue.
# The default pair (pragmatist + devils-advocate) lacks these roles,
# so red-blue uses dedicated presets instead.
RED_BLUE_AGENTS: tuple[AgentSpec, ...] = (
    AgentSpec(name="red-team", preset="role/red-team"),
    AgentSpec(name="blue-team", preset="role/blue-team"),
)


def build_adhoc_config(
    question: str,
    mode: str = "cooperative",
    output_dir: Path | None = None,
    agents: Sequence[AgentSpec] | None = None,
) -> tuple[Path, Path, Path]:
    """Generate a temporary conversus config for an ad-hoc question.

    Creates a temp directory containing ``question.md`` and
    ``conversus.yml`` configured with the given agents and mode.

    Args:
        question: The deliberation question text (must be non-empty after
            stripping).
        mode: Deliberation mode (default: ``"cooperative"``).
        output_dir: Override for the output directory.  When ``None``,
            output is placed inside the temp directory.
        agents: Optional list of :class:`AgentSpec` defining which agents
            to use. When ``None``, falls back to the default pair
            (pragmatist + devils-advocate).

    Returns:
        A tuple of ``(config_path, question_path, tmp_dir)`` where:
        - *config_path* is the path to the generated ``conversus.yml``
        - *question_path* is the path to the generated ``question.md``
        - *tmp_dir* is the temp directory (caller is responsible for cleanup)

    Raises:
        ConfigError: If the conversus project root or required presets
            cannot be found.
    """
    stripped = question.strip()
    if not stripped:
        raise ConfigError("Question must not be empty.")

    # Red-blue mode needs agents with role: red/blue.  Use dedicated
    # presets when the caller didn't supply custom agents.
    if agents:
        effective_agents = agents
    elif mode == "red-blue":
        effective_agents = RED_BLUE_AGENTS
    else:
        effective_agents = DEFAULT_AGENTS

    if len(effective_agents) < 2:
        raise ConfigError("At least 2 agents are required for a deliberation.")

    # Locate project root for presets
    try:
        project_root = find_project_root(marker="presets")
    except FileNotFoundError as exc:
        raise ConfigError(str(exc)) from exc

    # Verify all presets exist
    for agent in effective_agents:
        preset_path = (project_root / "presets" / f"{agent.preset}.yml").resolve()
        if not preset_path.exists():
            raise ConfigError(f"Preset not found: {agent.preset}")

    # Create temp directory and files
    tmp_dir = Path(tempfile.mkdtemp(prefix="conversus-adhoc-"))
    effective_output = output_dir.resolve() if output_dir else (tmp_dir / "output")

    # Write question file
    question_path = tmp_dir / "question.md"
    question_path.write_text(
        f"# Question\n\n## Context\n\n{stripped}\n",
        encoding="utf-8",
    )

    # Build agents YAML block — sanitize display names (e.g. "UX Reviewer")
    # to valid config names (e.g. "ux-reviewer") and deduplicate.
    #
    # For red-blue mode, assign role: red to the first agent and role: blue
    # to the second.  For >2 agents the caller should specify roles via
    # AgentSpec, but the default 2-agent case is handled here.
    agents_yaml = "agents:\n"
    seen_names: set[str] = set()
    for idx, agent in enumerate(effective_agents):
        config_name = _sanitize_agent_name(agent.name)
        # Deduplicate: append a numeric suffix if the sanitized name collides
        base_name = config_name
        counter = 2
        while config_name in seen_names:
            config_name = f"{base_name}-{counter}"
            counter += 1
        seen_names.add(config_name)
        agents_yaml += f"  - name: {config_name}\n"
        agents_yaml += f"    preset: {agent.preset}\n"
        # Red-blue role assignment for the default 2-agent pair
        if mode == "red-blue":
            role = "red" if idx == 0 else "blue"
            agents_yaml += f"    role: {role}\n"

    # Build config YAML with absolute paths
    config_content = (
        f"mode: {mode}\n"
        f"target: {question_path.resolve()}\n"
        f"output: {effective_output.resolve()}\n"
        f"iterations: 1\n"
        f"{agents_yaml}"
    )

    config_path = tmp_dir / "conversus.yml"
    config_path.write_text(config_content, encoding="utf-8")

    return config_path, question_path, tmp_dir
