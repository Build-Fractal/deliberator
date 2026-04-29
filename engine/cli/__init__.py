"""Click CLI for the conversus deliberation engine.

Provides the ``conversus`` command group with subcommands:
``run``, ``decide``, ``validate``, ``login``, ``logout``.

Entry point wired via ``pyproject.toml`` as::

    [project.scripts]
    conversus = "engine.cli:cli"

All user-facing errors are caught and printed cleanly — no raw tracebacks.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path

import click

from engine.config import ConfigError, parse_config
from engine.cost import estimate_cost
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Cost estimation (formatting only — formula in engine.cost)
# ---------------------------------------------------------------------------


def _format_cost_estimate(
    agent_count: int,
    iterations: int,
    has_arbiter: bool,
) -> str:
    """Return a human-readable cost estimate string."""
    phases = estimate_cost(agent_count, iterations, has_arbiter)
    total = sum(phases.values())
    lines = [
        f"Cost estimate: {total} total LLM launches",
        f"  Agents: {agent_count}",
        f"  Iterations: {iterations}",
        f"  Arbiter: {'yes' if has_arbiter else 'no'}",
        "",
        "  Per-phase breakdown:",
    ]
    for phase_name, count in phases.items():
        lines.append(f"    {phase_name}: {count}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------


@click.group(
    context_settings={"max_content_width": 120},
    epilog="""\b
Examples:
  # Quick ad-hoc deliberation
  conversus decide "Should we use Postgres or MongoDB?" --provider anthropic

  # Run a full deliberation from a config file
  conversus run path/to/conversus.yml --provider anthropic

  # Check provider authentication status
  conversus status
""",
)
def cli() -> None:
    """Conversus — competitive multi-agent deliberation engine."""
    pass


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Run with default mock provider
  conversus run path/to/conversus.yml

  # Run with Anthropic provider and a specific model
  conversus run path/to/conversus.yml --provider anthropic --model claude-sonnet-4-20250514

  # Run with Claude Code as agent runtime
  conversus run config.yml --provider claude-code

  # Run with local Ollama (free, no API key)
  conversus run config.yml --provider ollama --model llama3

  # Run only the review phase
  conversus run config.yml --provider openai --phase review
""",
)
@click.argument("config_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--provider",
    default="mock",
    type=click.Choice(
        ["mock", "anthropic", "openai", "claude-code", "aider", "opencode",
         "ollama", "llama-cpp", "vllm", "codex", "copilot", "gemini", "pi"],
        case_sensitive=False,
    ),
    help="Execution provider (default: mock).",
)
@click.option("--model", default=None, help="Override the LLM model identifier.")
@click.option("--rounds", default=None, type=int, help="Override deliberation rounds.")
@click.option(
    "--phase",
    default="all",
    type=click.Choice(
        ["all", "review"],
        case_sensitive=False,
    ),
    help="Phase to run (default: all). More phases will be added as execution paths are implemented.",
)
def run(
    config_path: Path,
    provider: str,
    model: str | None,
    rounds: int | None,
    phase: str,
) -> None:
    """Run a deliberation from a conversus config file."""
    from engine.cli.progress import RichProgressHandler
    from engine.events import CallbackEmitter
    from engine.run import run_engine

    progress_handler = RichProgressHandler()
    rich_emitter = CallbackEmitter(progress_handler)

    try:
        written_paths = asyncio.run(
            run_engine(
                config_path=config_path.resolve(),
                phase=phase,
                provider_name=provider,
                model=model,
                rounds=rounds,
                emitter=rich_emitter,
            )
        )
    except (ConfigError, ProviderError) as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    for p in written_paths:
        click.echo(str(p))


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Validate a config file
  conversus validate path/to/conversus.yml

  # Validate and classify a question for deliberation sufficiency
  conversus validate path/to/conversus.yml --question "Is this clear enough?"
""",
)
@click.argument("config_path", type=click.Path(exists=True, path_type=Path))
@click.option("--question", default=None, help="Classify a question for deliberation sufficiency.")
def validate(config_path: Path, question: str | None) -> None:
    """Validate a conversus config and print a cost estimate."""
    try:
        config = parse_config(config_path.resolve())
    except ConfigError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(f"Config valid: {config_path}")
    click.echo(f"Mode: {config.mode}")
    click.echo("")
    click.echo(
        _format_cost_estimate(
            agent_count=len(config.agents),
            iterations=config.iterations,
            has_arbiter=config.arbiter is not None,
        )
    )

    if question is not None:
        from linter.question_classifier import classify_question

        result = classify_question(question)
        click.echo("")
        click.echo(f"Question classification: {'sufficient' if result.sufficient else 'insufficient'}")
        if result.reason:
            click.echo(f"  Reason: {result.reason}")


# ---------------------------------------------------------------------------
# decide
# ---------------------------------------------------------------------------


def _find_project_root() -> Path:
    """Locate the conversus project root (directory containing presets/).

    Delegates to :func:`engine._root.find_project_root`.
    """
    from engine._root import find_project_root

    try:
        return find_project_root(marker="presets")
    except FileNotFoundError as exc:
        raise ConfigError(str(exc)) from exc


@cli.command(
    epilog="""\b
Examples:
  # Quick ad-hoc deliberation with Anthropic
  conversus decide "Should we use Postgres or MongoDB?" --provider anthropic

  # Cooperative deliberation with JSON output
  conversus decide "Should we use Postgres or MongoDB?" --provider anthropic --mode cooperative --format json

  # Use a different deliberation mode
  conversus decide "Build vs buy?" --provider openai --mode red-blue
""",
)
@click.argument("question", type=str)
@click.option(
    "--provider",
    default="mock",
    type=click.Choice(
        ["mock", "anthropic", "openai", "claude-code", "aider", "opencode",
         "ollama", "llama-cpp", "vllm", "codex", "copilot", "gemini", "pi"],
        case_sensitive=False,
    ),
    help="Execution provider (default: mock).",
)
@click.option(
    "--mode",
    default="cooperative",
    type=click.Choice(
        ["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"],
        case_sensitive=False,
    ),
    help="Deliberation mode (default: cooperative).",
)
@click.option("--model", default=None, help="Override the LLM model identifier.")
@click.option(
    "--output",
    "output_dir",
    default=None,
    type=click.Path(path_type=Path),
    help="Output directory (default: temp dir, cleaned up after).",
)
@click.option(
    "--format",
    "output_format",
    default="rich",
    type=click.Choice(["rich", "json"], case_sensitive=False),
    help="Output format (default: rich).",
)
def decide(question: str, provider: str, mode: str, model: str | None, output_dir: Path | None, output_format: str) -> None:
    """Run an ad-hoc deliberation on a natural-language question.

    Generates a temporary conversus config using pragmatist + devils-advocate
    presets, runs the full pipeline, and prints structured results.
    """
    # Validate non-empty question
    stripped = question.strip()
    if not stripped:
        click.echo("Error: question must not be empty.", err=True)
        sys.exit(1)

    # Classify question — warn if insufficient but don't block
    from linter.question_classifier import classify_question

    classification = classify_question(stripped, mode="non-interactive")
    if not classification.sufficient:
        click.echo(
            f"Warning: {classification.reason}",
            err=True,
        )

    # Resolve ad-hoc config via shared builder
    try:
        from engine.adhoc import build_adhoc_config

        config_path, question_path, tmp_dir = build_adhoc_config(
            question=stripped,
            mode=mode,
            output_dir=output_dir,
        )
        use_temp_output = output_dir is None
        effective_output = (tmp_dir / "output") if use_temp_output else output_dir.resolve()
    except ConfigError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    try:
        # Run pipeline
        from engine.cli.progress import RichProgressHandler
        from engine.events import CallbackEmitter
        from engine.run import run_engine

        progress_handler = RichProgressHandler()
        rich_emitter = CallbackEmitter(progress_handler)

        try:
            asyncio.run(
                run_engine(
                    config_path=config_path.resolve(),
                    provider_name=provider,
                    model=model,
                    emitter=rich_emitter,
                )
            )
        except (ConfigError, ProviderError) as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)
        except Exception as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)

        # Parse synthesis output
        synthesis_path = effective_output / "summary" / "final.md"
        if not synthesis_path.exists():
            click.echo(
                "Error: Synthesis output not found — pipeline may have failed.",
                err=True,
            )
            sys.exit(1)

        synthesis_text = synthesis_path.read_text(encoding="utf-8")

        from linter.output_contract import parse_synthesis

        try:
            result = parse_synthesis(synthesis_text, mode=mode)
        except ValueError as exc:
            click.echo(f"Error: Failed to parse synthesis: {exc}", err=True)
            sys.exit(1)

        # Print formatted output based on output format
        if output_format == "json":
            click.echo(result.model_dump_json(indent=2))
        else:
            from engine.cli.render import render_result

            render_result(result)

    finally:
        # Clean up temp dir if we created the output there
        if use_temp_output and tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# login
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Log in to Anthropic via OAuth
  conversus login anthropic

  # Log in to OpenAI
  conversus login openai
""",
)
@click.argument("provider", type=str)
def login(provider: str) -> None:
    """Log in to a model provider via OAuth."""
    from engine import auth

    try:
        auth.login(provider)
    except ProviderError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo("Login successful")


# ---------------------------------------------------------------------------
# logout
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Log out of Anthropic
  conversus logout anthropic

  # Log out of OpenAI
  conversus logout openai
""",
)
@click.argument("provider", type=str)
def logout(provider: str) -> None:
    """Log out of a model provider."""
    from engine import auth

    auth.logout(provider)
    click.echo("Logged out")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Check authentication status for all providers
  conversus status
""",
)
def status() -> None:
    """Show authentication status for all providers."""
    from datetime import datetime, timezone

    from rich.console import Console
    from rich.table import Table

    from engine.auth import OAUTH_CONFIGS, CredentialStore
    from engine.providers.anthropic import is_oauth_token

    store = CredentialStore()
    console = Console()
    table = Table(title="Provider Authentication Status")
    table.add_column("Provider", style="bold")
    table.add_column("Status")
    table.add_column("Details")

    for provider, config in OAUTH_CONFIGS.items():
        creds = store.get(provider)

        if creds and creds.get("access_token"):
            # Stored OAuth credentials
            token = creds["access_token"]
            token_type = "subscription" if is_oauth_token(token) else "OAuth token"

            details_parts = [token_type]

            expires_at = creds.get("expires_at")
            if expires_at is not None:
                expiry_dt = datetime.fromtimestamp(expires_at, tz=timezone.utc)
                now = datetime.now(tz=timezone.utc)
                if expiry_dt < now:
                    details_parts.append(f"expired {expiry_dt:%Y-%m-%d %H:%M UTC}")
                else:
                    details_parts.append(f"expires {expiry_dt:%Y-%m-%d %H:%M UTC}")

            table.add_row(provider, "[green]logged in[/green]", ", ".join(details_parts))

        elif os.environ.get(config["env_var"]):
            # Environment variable fallback
            table.add_row(provider, "[yellow]env var[/yellow]", config["env_var"])

        else:
            table.add_row(provider, "[red]not configured[/red]", "—")

    console.print(table)


# ---------------------------------------------------------------------------
# context (debug)
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Print the detected invocation context (interactive terminal)
  conversus context

  # Simulate CI context
  CI=1 conversus context

  # Simulate Claude Code session context
  CLAUDECODE=1 conversus context

  # Force JSON output even on a TTY
  conversus context --json
""",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    default=False,
    help="Output as machine-readable JSON instead of a formatted table.",
)
def context(as_json: bool) -> None:
    """Print the detected invocation context and exit.

    Debug helper for spec 042 Phase 2.0.  Resolves which provider,
    renderer, and exit code scheme would be selected for the current
    shell environment without actually running a deliberation.

    Useful for verifying that context detection works correctly in CI,
    cron, hooks, and Claude Code sessions before committing to a
    specific conversus.yml configuration.
    """
    from engine.cli.context import detect_context

    ctx = detect_context()

    if as_json:
        import json as _json
        payload = {
            "is_tty": ctx.is_tty,
            "is_ci": ctx.is_ci,
            "is_claude_code_session": ctx.is_claude_code_session,
            "is_background": ctx.is_background,
            "default_provider": ctx.default_provider,
            "renderer": ctx.renderer,
            "exit_code_scheme": ctx.exit_code_scheme,
            "env": ctx.env,
            "argv": list(ctx.argv),
        }
        click.echo(_json.dumps(payload, indent=2))
        return

    # Formatted table output
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="Conversus Invocation Context", show_header=True)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="white")

    def _bool(v: bool) -> str:
        return "[green]true[/green]" if v else "[dim]false[/dim]"

    table.add_row("is_tty", _bool(ctx.is_tty))
    table.add_row("is_ci", _bool(ctx.is_ci))
    table.add_row("is_claude_code_session", _bool(ctx.is_claude_code_session))
    table.add_row("is_background", _bool(ctx.is_background))
    table.add_row("", "")
    table.add_row("default_provider", f"[bold yellow]{ctx.default_provider}[/bold yellow]")
    table.add_row("renderer", f"[bold yellow]{ctx.renderer}[/bold yellow]")
    table.add_row("exit_code_scheme", f"[bold yellow]{ctx.exit_code_scheme}[/bold yellow]")

    if ctx.env:
        table.add_row("", "")
        table.add_row(
            "env (consulted)",
            "\n".join(f"{k}={v}" for k, v in sorted(ctx.env.items())),
        )

    console.print(table)


# ---------------------------------------------------------------------------
# mcp
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Start the MCP server (stdio transport, for use with Claude Code / Cursor)
  conversus mcp

  # Add to Claude Code via CLI
  claude mcp add conversus -- conversus mcp
""",
)
def mcp() -> None:
    """Start the Conversus MCP server (stdio transport).

    Launches an MCP-compatible server that exposes conversus deliberation
    tools to editors such as Claude Code, Cursor, and Windsurf.

    Requires the mcp extras: pip install conversus[mcp]

    Tools exposed:
      conversus_validate — validate a YAML config and estimate cost
      conversus_run      — validate config and parse/run a deliberation
      conversus_decide   — run an ad-hoc deliberation on a question

    Transport: stdio (launched by the editor process, not by the user)
    """
    try:
        from mcp.server.fastmcp import FastMCP  # noqa: F401 — presence check only
    except ImportError:
        click.echo(
            "Error: MCP dependencies are not installed.\n"
            "Install them with: pip install conversus[mcp]",
            err=True,
        )
        sys.exit(1)

    # Import the pre-built FastMCP instance from mcp_server.py.
    # We resolve the path relative to this file so it works regardless of CWD.
    import importlib.util as _ilu

    _server_path = Path(__file__).parent.parent.parent / "mcp_server.py"
    if not _server_path.exists():
        # Installed package layout: mcp_server.py ships as a top-level module.
        try:
            import mcp_server as _mcp_mod
        except ImportError:
            click.echo(
                "Error: mcp_server.py not found. "
                "Re-install the package or run from the repo root.",
                err=True,
            )
            sys.exit(1)
    else:
        _spec = _ilu.spec_from_file_location("mcp_server", _server_path)
        _mcp_mod = _ilu.module_from_spec(_spec)  # type: ignore[arg-type]
        _spec.loader.exec_module(_mcp_mod)  # type: ignore[union-attr]

    _mcp_mod.mcp.run(transport="stdio")


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------


@cli.command(
    epilog="""\b
Examples:
  # Init with Claude Code only (default)
  conversus init

  # Init with multiple runtimes
  conversus init --runtime claude-code --runtime opencode --runtime gemini

  # Init with Opus as default model
  conversus init --model opus

  # Re-init to update settings
  conversus init --force
""",
)
@click.option(
    "--runtime",
    "runtimes",
    multiple=True,
    default=["claude-code"],
    type=click.Choice(
        ["claude-code", "opencode", "copilot", "gemini", "codex", "aider"],
        case_sensitive=False,
    ),
    help="AI runtimes to configure permissions for (repeatable).",
)
@click.option(
    "--provider",
    "default_provider",
    default="claude-code",
    help="Default execution provider.",
)
@click.option(
    "--model",
    "default_model",
    default="sonnet",
    help="Default model identifier.",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Overwrite existing settings files.",
)
def init(
    runtimes: tuple[str, ...],
    default_provider: str,
    default_model: str,
    force: bool,
) -> None:
    """Initialize a .conversus/ directory with runtime permissions.

    Creates the project-level configuration so conversus agents can
    run non-interactively without permission prompts.  Each runtime
    gets its own config file:

    \b
      claude-code  → .claude/settings.json (permission grants)
      opencode     → .opencode/config.toml (auto_approve)
      copilot      → .github/copilot-settings.json
      gemini       → .gemini/settings.json
      codex        → .codex/settings.json
      aider        → .aider.conf.yml (yes-always, no-auto-commits)

    Run this once per project, then all `conversus run --provider <runtime>`
    commands work without interactive permission dialogs.
    """
    from engine.project import init_project

    project_root = Path.cwd()
    runtime_list = list(runtimes)

    try:
        created = init_project(
            project_root,
            runtimes=runtime_list,
            default_provider=default_provider,
            default_model=default_model,
            force=force,
        )
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    if not created:
        click.echo("Already initialized (use --force to overwrite).")
        return

    click.echo(f"Initialized .conversus/ in {project_root}")
    for desc, path in created.items():
        rel = path.relative_to(project_root) if path.is_relative_to(project_root) else path
        click.echo(f"  {desc}: {rel}")

    click.echo("")
    click.echo(f"Runtimes configured: {', '.join(runtime_list)}")
    click.echo(f"Default provider: {default_provider}")
    click.echo(f"Default model: {default_model}")
    click.echo("")
    click.echo("You can now run:")
    click.echo(f"  conversus run conversus.yml --provider {default_provider}")


# ---------------------------------------------------------------------------
# Spec 064.1 — runtime registration of entry-point-discovered capabilities
# ---------------------------------------------------------------------------
#
# Capabilities shipped by paid wheels (``conversus-enhanced`` etc.) advertise
# themselves via setuptools entry points under the four functional groups
# defined in :data:`conversus.registry.discovery.CAPABILITY_GROUPS`. The
# registration call below walks those discoveries and installs each as a
# subcommand on the ``cli`` group. Hand-coded ``@cli.command()`` decorators
# above are unaffected.
from conversus.registry.runtime import register_discovered_cli_commands

register_discovered_cli_commands(cli)
