"""Conversus capability registry — the single source of truth.

This module declares every conversus capability that the projector
(``scripts/build-surfaces.py``) walks to generate the four distribution
surface files: ``engine/cli/__init__.py``, ``mcp_server.py``,
``claude-code-plugin/skills/*/SKILL.md``, and ``desktop-extension/manifest.json``.

**How to add a capability**: construct a ``Capability`` instance at
module scope and append it to the ``CAPABILITIES`` list at the bottom
of the file. Do NOT reach for a decorator — constitution principle IX
forbids module-level mutable state, so there is no ``@capability``
decorator that appends to a hidden global. The explicit list is the
entire registration mechanism.

**How to customize per-surface UX**: subclass the appropriate
``Default*Adapter`` (not the bare ABC) and pass an instance via the
``cli_adapter`` / ``mcp_adapter`` / ``plugin_adapter`` / ``mcpb_adapter``
constructor kwarg. Subclassing the Default lets you inherit the
rendering and only override the attribute that differs — typically
``description`` for MCP, which Claude Desktop uses for tool selection.

**How to scope a param to specific surfaces**: set ``Param.surfaces=[...]``.
Useful when a capability has a CLI-only flag (e.g. ``--format rich|json``)
or an MCP-only safety cap (``max_launches``) that doesn't make sense
everywhere else.

**How to dispatch to different handlers per surface**: set
``Capability.handlers={Surface.MCP: "module:func"}`` in addition to
the default ``handler``. Only needed when the surfaces have
intrinsically different behavior (e.g. ``decide`` — CLI prints + exits,
MCP returns structured data).

See ``specs/055-capability-registry.md`` and ``CONSTITUTION.md``
principles IX, XI, XII, XIV.
"""

from __future__ import annotations

from pathlib import Path

from conversus.registry import (
    Capability,
    DefaultMCPAdapter,
    Param,
    PluginAdapter,
    Surface,
)


# ---------------------------------------------------------------------------
# decide — run an ad-hoc deliberation on a natural-language question
# ---------------------------------------------------------------------------


class DecideMCPAdapter(DefaultMCPAdapter):
    """Override adapter that gives ``decide`` a verbose MCP tool description.

    Claude Desktop and Cowork use the tool description to decide which
    tool to invoke when the user's request is ambiguous. The default
    adapter would emit ``capability.summary`` ("Run an ad-hoc
    deliberation") — that's enough for humans reading ``--help`` but
    not for tool-selection disambiguation. This override substitutes a
    longer, more concrete description.
    """

    description = """\
Run an ad-hoc deliberation on a natural-language question using the
built-in pragmatist + devil's advocate agents. Best for quick
decisions — no config file needed. Accepts a mode parameter
(cooperative, red-blue, winner-take-all, prisoners-dilemma).

Use this when the user describes a specific decision they are facing
(e.g. "Postgres or MongoDB?"). Don't use it for vague questions — the
sufficiency classifier rejects them before execution.
"""


decide = Capability(
    name="decide",
    summary="Run an ad-hoc deliberation on a natural-language question",
    long_description=(
        "Quick deliberation without needing a config file. Uses the "
        "built-in pragmatist + devils-advocate agents and runs the full "
        "5-phase pipeline. Insufficient questions are rejected before "
        "execution via the R020 quality gate."
    ),
    surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
    params=[
        Param(
            name="question",
            type=str,
            required=True,
            help="The decision to deliberate. Be specific.",
        ),
        Param(
            name="provider",
            type=str,
            default="mock",
            # Matches the full list of providers the hand-written CLI
            # command currently accepts. The registry is the single
            # source of truth (principle XI); whenever this list grows,
            # it grows here and is regenerated to every surface.
            choices=[
                "mock",
                "anthropic",
                "openai",
                "claude-code",
                "aider",
                "opencode",
                "ollama",
                "llama-cpp",
                "vllm",
                "codex",
                "copilot",
                "gemini",
                "pi",
            ],
            help="Execution provider (default: mock).",
        ),
        Param(
            name="mode",
            type=str,
            default="cooperative",
            choices=[
                "cooperative",
                "winner-take-all",
                "prisoners-dilemma",
                "red-blue",
            ],
            help="Deliberation mode (default: cooperative).",
        ),
        # CLI-only: output directory for intermediate artifacts. MCP
        # always uses a temp dir since the tool call returns a
        # structured result rather than writing to disk.
        #
        # The param name is ``output`` (not ``output_dir``) so the
        # generated Click flag becomes ``--output`` — matching the
        # hand-written CLI exactly. The handler signature in
        # ``engine/handlers.py::run_decide_cli`` also uses ``output``
        # as its kwarg name; they must agree for the projector's
        # keyword-forwarded dispatch to work.
        Param(
            name="output",
            type=str,
            default=None,
            help="Output directory (default: temp dir, cleaned up after).",
            surfaces=[Surface.CLI],
        ),
        # CLI-only: render format. MCP always returns a DecideResult
        # pydantic model — it's the MCP client's job to format it.
        Param(
            name="output_format",
            type=str,
            default="rich",
            choices=["rich", "json"],
            help="Output format (default: rich).",
            surfaces=[Surface.CLI],
        ),
        # MCP-only: safety cap on LLM launches. CLI users see
        # per-phase progress and can Ctrl-C; MCP tool calls are
        # fire-and-forget so the cap matters more there.
        Param(
            name="max_launches",
            type=int,
            default=20,
            help="Safety cap on LLM launches.",
            surfaces=[Surface.MCP],
        ),
    ],
    # Per-surface handlers: CLI prints + exits (returns None); MCP
    # returns a structured DecideResult. See
    # ``engine/handlers.py::run_decide_cli`` / ``run_decide_mcp``.
    handler="engine.handlers:run_decide_cli",
    handlers={Surface.MCP: "engine.handlers:run_decide_mcp"},
    mcp_adapter=DecideMCPAdapter(),
)


# ---------------------------------------------------------------------------
# run — validate + optionally execute a full deliberation from a config file
# ---------------------------------------------------------------------------
#
# run is the archetypal "data transformation" capability that spec 055 Day 6
# called out as "easy to migrate because [it has] minimal surface-specific
# UX". In practice it's more intricate than decide because its CLI and MCP
# surfaces take fundamentally different inputs:
#
#   CLI: config_path (filesystem path to a YAML file)
#   MCP: config_yaml (raw YAML string passed inline)
#
# and the MCP surface also has a 3-mode dispatcher (validate_only,
# parsed_output, in_process) driven by which of ``output_path`` /
# ``provider`` are set. Per-surface params + per-surface handlers handle
# both divergences cleanly.

run = Capability(
    name="run",
    summary="Run a deliberation from a conversus config file",
    long_description=(
        "Executes the full 5-phase deliberation pipeline from a conversus "
        "YAML config. On the CLI surface, takes a path to a config file and "
        "runs with Rich progress display. On the MCP surface, takes the "
        "config YAML inline and operates in one of three modes: validate-"
        "only (returns cost estimate), parsed-output (parses an existing "
        "synthesis file), or in-process (runs the full pipeline and "
        "returns structured output)."
    ),
    surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
    params=[
        # CLI-only: filesystem path to the config file.
        Param(
            name="config_path",
            type=str,
            required=True,
            help="Path to a conversus.yml config file.",
            surfaces=[Surface.CLI, Surface.PLUGIN],
        ),
        # MCP-only: full YAML text passed inline.
        Param(
            name="config_yaml",
            type=str,
            required=True,
            help="Full YAML configuration string for a conversus run.",
            surfaces=[Surface.MCP],
        ),
        # Shared: provider selection.
        Param(
            name="provider",
            type=str,
            default="mock",
            choices=[
                "mock",
                "anthropic",
                "openai",
                "claude-code",
                "aider",
                "opencode",
                "ollama",
                "llama-cpp",
                "vllm",
                "codex",
                "copilot",
                "gemini",
                "pi",
            ],
            help="Execution provider (default: mock).",
            surfaces=[Surface.CLI, Surface.PLUGIN],
        ),
        # MCP uses a narrower provider set (no choices — the MCP tool
        # accepts arbitrary strings and resolves them lazily). The
        # param exists on MCP without choices so the generated signature
        # is ``provider: str = ""``.
        Param(
            name="provider",
            type=str,
            default="",
            help="Provider name for in-process execution.",
            surfaces=[Surface.MCP],
        ),
        # CLI-only: model / rounds / phase overrides.
        Param(
            name="model",
            type=str,
            default=None,
            help="Override the LLM model identifier.",
            surfaces=[Surface.CLI],
        ),
        Param(
            name="rounds",
            type=int,
            default=None,
            help="Override deliberation rounds.",
            surfaces=[Surface.CLI],
        ),
        Param(
            name="phase",
            type=str,
            default="all",
            choices=["all", "review"],
            help="Phase to run (default: all).",
            surfaces=[Surface.CLI],
        ),
        # MCP-only: output_path selects parsed-output mode.
        Param(
            name="output_path",
            type=str,
            default="",
            help=(
                "Path to an existing synthesis output file. When set, "
                "the tool parses the file into structured output."
            ),
            surfaces=[Surface.MCP],
        ),
    ],
    handler="engine.handlers:run_cli",
    handlers={Surface.MCP: "engine.handlers:run_mcp"},
)


# ---------------------------------------------------------------------------
# validate — validate a conversus config and print a cost estimate
# ---------------------------------------------------------------------------

validate = Capability(
    name="validate",
    summary="Validate a conversus config and print a cost estimate",
    long_description=(
        "Parses and validates a conversus YAML configuration, runs "
        "template validation, optionally classifies a deliberation "
        "question for sufficiency, and computes a cost estimate (number "
        "of LLM launches required). Returns before any pipeline execution "
        "— always run this before a real deliberation to know the cost."
    ),
    surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
    params=[
        Param(
            name="config_path",
            type=str,
            required=True,
            help="Path to a conversus.yml config file.",
            surfaces=[Surface.CLI, Surface.PLUGIN],
        ),
        Param(
            name="config_yaml",
            type=str,
            required=True,
            help="Full YAML configuration string for a conversus run.",
            surfaces=[Surface.MCP],
        ),
        Param(
            name="question",
            type=str,
            default=None,
            help="Optional question to classify for deliberation sufficiency.",
            surfaces=[Surface.CLI, Surface.PLUGIN],
        ),
        # MCP variant has default="" instead of None since the hand-written
        # signature uses an empty string. Both paths end up calling
        # classify_question only when the string is non-empty.
        Param(
            name="question",
            type=str,
            default="",
            help="Optional question to classify for deliberation sufficiency.",
            surfaces=[Surface.MCP],
        ),
    ],
    handler="engine.handlers:validate_cli",
    handlers={Surface.MCP: "engine.handlers:validate_mcp"},
)


# ---------------------------------------------------------------------------
# login — OAuth login for a model provider
# ---------------------------------------------------------------------------

login = Capability(
    name="login",
    summary="Log in to a model provider via OAuth",
    surfaces=[Surface.CLI, Surface.PLUGIN],
    params=[
        Param(name="provider", type=str, required=True, help="Provider to log in to."),
    ],
    handler="engine.handlers:login_cli",
)


# ---------------------------------------------------------------------------
# logout — remove stored credentials for a model provider
# ---------------------------------------------------------------------------

logout = Capability(
    name="logout",
    summary="Log out of a model provider",
    surfaces=[Surface.CLI, Surface.PLUGIN],
    params=[
        Param(name="provider", type=str, required=True, help="Provider to log out of."),
    ],
    handler="engine.handlers:logout_cli",
)


# ---------------------------------------------------------------------------
# status — show provider auth status
# ---------------------------------------------------------------------------

status = Capability(
    name="status",
    summary="Show authentication status for all providers",
    surfaces=[Surface.CLI, Surface.PLUGIN],
    params=[],
    handler="engine.handlers:status_cli",
)


# ---------------------------------------------------------------------------
# context — debug invocation context detection
# ---------------------------------------------------------------------------

context = Capability(
    name="context",
    summary="Print the detected invocation context and exit",
    long_description=(
        "Debug helper that resolves which provider, renderer, and exit "
        "code scheme would be selected for the current shell environment "
        "without running a deliberation. Useful for verifying context "
        "detection in CI, cron, hooks, and Claude Code sessions."
    ),
    surfaces=[Surface.CLI],
    params=[
        Param(
            name="as_json",
            type=bool,
            default=False,
            help="Output as machine-readable JSON instead of a formatted table.",
        ),
    ],
    handler="engine.handlers:context_cli",
)


# ---------------------------------------------------------------------------
# mcp — start the MCP server (meta-command, CLI-only)
# ---------------------------------------------------------------------------

mcp = Capability(
    name="mcp",
    summary="Start the Conversus MCP server (stdio transport)",
    long_description=(
        "Launches an MCP-compatible server that exposes conversus "
        "deliberation tools to editors such as Claude Code, Cursor, "
        "and Windsurf. Requires the mcp extras: pip install conversus[mcp]"
    ),
    surfaces=[Surface.CLI],
    params=[],
    handler="engine.handlers:mcp_cli",
)


# ---------------------------------------------------------------------------
# init — initialize project-level runtime permissions
# ---------------------------------------------------------------------------

init = Capability(
    name="init",
    summary="Initialize a .conversus/ directory with runtime permissions",
    long_description=(
        "Creates the project-level configuration so conversus agents can "
        "run non-interactively without permission prompts. Each runtime "
        "gets its own config file (claude-code, opencode, copilot, etc.)."
    ),
    surfaces=[Surface.CLI, Surface.PLUGIN],
    params=[
        Param(
            name="runtimes",
            type=str,
            default="claude-code",
            help=(
                "Comma-separated AI runtimes to configure "
                "(e.g. 'claude-code,opencode,gemini')."
            ),
        ),
        Param(
            name="default_provider",
            type=str,
            default="claude-code",
            help="Default execution provider.",
        ),
        Param(
            name="default_model",
            type=str,
            default="sonnet",
            help="Default model identifier.",
        ),
        Param(name="force", type=bool, default=False, help="Overwrite existing settings."),
    ],
    handler="engine.handlers:init_cli",
)


# ---------------------------------------------------------------------------
# design — conversational config wizard (Plugin surface ONLY)
#
# Spec 055 NO list rule #1: "Don't auto-generate conversational skill
# bodies. The design wizard SKILL.md body stays hand-written."
#
# This capability registers the METADATA in the registry (name, summary,
# surfaces) so the projector knows it exists, but the PluginAdapter
# override returns the hand-written SKILL.md verbatim from disk rather
# than generating a generic dispatch template.
# ---------------------------------------------------------------------------

_DESIGN_SKILL_PATH = Path(__file__).parent / "claude-code-plugin" / "skills" / "design" / "SKILL.md"


class DesignPluginAdapter(PluginAdapter):
    """Override adapter that preserves the hand-written design wizard SKILL.md.

    The ``design`` command is a conversational multi-step wizard that
    guides the user through config creation. Its SKILL.md body contains
    question-by-question flow logic that can't be auto-generated from
    capability metadata. This override reads the existing file and
    returns it verbatim, so ``make build-surfaces`` is a no-op for this
    one skill (read → write-back → identical file).
    """

    def render(self, capability: "Capability") -> str:
        return _DESIGN_SKILL_PATH.read_text(encoding="utf-8")


design = Capability(
    name="design",
    summary="Guided config builder — create a conversus.yml interactively",
    surfaces=[Surface.PLUGIN],
    params=[],
    handler="engine.handlers:design_cli",  # placeholder — design is plugin-only
    plugin_adapter=DesignPluginAdapter(),
)


# ---------------------------------------------------------------------------
# The capability list — what the projector walks
# ---------------------------------------------------------------------------

#: Explicit, authoritative list of conversus capabilities. The projector
#: imports this name directly and iterates it. There is no module-level
#: registry populated by decorators — this list is the registration
#: mechanism (constitution principle IX).
CAPABILITIES: list[Capability] = [
    decide,
    run,
    validate,
    login,
    logout,
    status,
    context,
    mcp,
    init,
    design,
]
