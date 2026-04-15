"""Registry-facing handler functions for conversus capabilities.

This module is the target of the ``handler`` import strings declared in
``capabilities.py`` at the repo root. Each handler is a plain Python
function — no Click decorators, no @mcp.tool wrapping — so the projector
can dispatch to it from the generated surface files with a one-line
``from engine.handlers import <name>; return <name>(**kwargs)`` wrapper.

Scope through Day 6: canonical handlers for ``decide``, ``run``, and
``validate`` on both the CLI and MCP surfaces. Result types live in
``engine/results.py`` (single source of truth — constitution principle
XI). Day 7 removes the hand-written ``mcp_server.py`` in favor of the
generated one; the handlers here stay as-is.

Handler naming
--------------
- ``run_decide_cli`` / ``run_decide_mcp`` — ad-hoc deliberation
- ``run_cli`` / ``run_mcp`` — full pipeline from a config file
- ``validate_cli`` / ``validate_mcp`` — config validation + cost estimate

The suffix always indicates the surface. ``mcp`` handlers return
structured result models (``DecideResult``, ``RunResult``,
``ValidateResult``); ``cli`` handlers print to stdout/stderr and exit
with a non-zero code on failure. The two shapes are irreconcilable —
MCP needs structured return, CLI needs side-effect-based output — which
is why the capability registry supports per-surface handlers via
``Capability.handlers``.

See ``specs/055-capability-registry.md`` sections 4 Day 5 and Day 6.
"""

from __future__ import annotations

import asyncio
import logging
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import click
import yaml

from engine._root import find_project_root
from engine.adhoc import build_adhoc_config
from engine.auth import resolve_provider
from engine.config import ConfigError, parse_config
from engine.events import CallbackEmitter, NullEmitter
from engine.phases import PipelineError, run_pipeline
from engine.providers import ProviderError
from engine.persistence import (
    cleanup_old_deliberations,
    find_project_root,
    is_persistence_enabled,
    list_deliberations as _list_deliberations,
    persist_deliberation,
    read_deliberation_file,
)
from engine.settings import load_settings, resolve_setting
from engine.results import (
    CostEstimate,
    DecideResult,
    ListResult,
    RunResult,
    ShowResult,
    ValidateResult,
    _estimate_cost,
)
from linter.output_contract import parse_synthesis
from linter.question_classifier import classify_question
from linter.validate import ValidationConfig, validate_all

logger = logging.getLogger("conversus.handlers")


# ---------------------------------------------------------------------------
# decide — MCP surface handler
# ---------------------------------------------------------------------------


def run_decide_mcp(
    question: str,
    provider: str = "mock",
    mode: str = "cooperative",
    max_launches: int = 20,
    *,
    mcp_context: object | None = None,
) -> DecideResult:
    """Run an ad-hoc deliberation for the MCP surface.

    Behavior matches ``mcp_server._decide`` exactly — this function is
    the extraction target for the registry's MCP projection of the
    ``decide`` capability. Returns a structured ``DecideResult``; never
    prints or raises (errors propagate via ``result.errors``).

    Provider and mode resolve through the settings cascade (spec 057):
    CLI flag → project settings → global settings → built-in default.
    The ``"mock"`` default in the function signature is the last-resort
    fallback; if ``.conversus/settings.yml`` sets ``default_provider:
    anthropic``, that takes effect when the caller passes ``"mock"``
    (the signature default).
    """
    # Resolve settings cascade (spec 057)
    settings = load_settings()
    provider = resolve_setting(settings, provider if provider != "mock" else None, "default_provider")
    mode = resolve_setting(settings, mode if mode != "cooperative" else None, "default_mode")

    stripped = question.strip()
    if not stripped:
        logger.warning("run_decide_mcp: empty question rejected")
        return DecideResult(
            sufficient=False,
            errors=["Question must not be empty."],
        )

    classification: dict[str, Any] | None = None
    try:
        cr = classify_question(stripped, mode="non-interactive")
        classification = cr.model_dump()
        if not cr.sufficient:
            reason = cr.reason or "Question is insufficient for multi-agent deliberation."
            logger.warning("run_decide_mcp: question insufficient — %s", reason)
            return DecideResult(
                sufficient=False,
                classification=classification,
                errors=[reason],
            )
    except Exception as exc:
        logger.exception("Question classification error")
        return DecideResult(
            sufficient=False,
            errors=[f"Question classification error: {exc}"],
        )

    try:
        config_path, question_path, tmp_dir = build_adhoc_config(
            question=stripped,
            mode=mode,
        )
    except ConfigError as exc:
        return DecideResult(
            sufficient=True,
            classification=classification,
            errors=[str(exc)],
        )

    cost_estimate: CostEstimate | None = None
    try:
        config_content = config_path.read_text(encoding="utf-8")
        config_dict = yaml.safe_load(config_content)

        try:
            cost_estimate = _estimate_cost(config_dict)
            if cost_estimate.total_launches > max_launches:
                logger.warning(
                    "run_decide_mcp: cost limit exceeded (%d > %d)",
                    cost_estimate.total_launches,
                    max_launches,
                )
                return DecideResult(
                    sufficient=True,
                    classification=classification,
                    cost_estimate=cost_estimate,
                    errors=[
                        f"Estimated {cost_estimate.total_launches} launches exceeds "
                        f"max_launches={max_launches}. Increase max_launches to proceed."
                    ],
                )
        except Exception as exc:
            logger.exception("Cost estimation error in run_decide_mcp")
            return DecideResult(
                sufficient=True,
                classification=classification,
                errors=[f"Cost estimation error: {exc}"],
            )

        engine_config = parse_config(config_path)

        # Resolve the provider — claude-desktop uses MCP sampling
        # (spec 060), all others use direct API via resolve_provider.
        if provider == "claude-desktop" and mcp_context is not None:
            from engine.execution.providers.desktop_sampling import DesktopSamplingProvider
            model_provider = DesktopSamplingProvider(mcp_context=mcp_context)
        else:
            if provider == "claude-desktop":
                # MCP sampling context not available — fall back to anthropic
                # credentials if the user has them (from conversus login or
                # ANTHROPIC_API_KEY env var). This makes "claude-desktop" work
                # even when MCP sampling isn't wired yet.
                logger.info(
                    "claude-desktop provider requested but no MCP context — "
                    "falling back to anthropic credentials"
                )
                provider = "anthropic"
            try:
                model_provider = resolve_provider(provider)
            except ProviderError as exc:
                return DecideResult(
                    sufficient=True,
                    classification=classification,
                    cost_estimate=cost_estimate,
                    errors=[f"Provider error: {exc}"],
                )

        emitter = NullEmitter()
        result = asyncio.run(
            run_pipeline(
                engine_config,
                model_provider,
                emitter,
                config_path=config_path,
            )
        )

        synthesis_path = result.output_dir / "summary" / "final.md"
        if not synthesis_path.exists():
            return DecideResult(
                sufficient=True,
                classification=classification,
                cost_estimate=cost_estimate,
                errors=[f"Pipeline completed but synthesis file not found: {synthesis_path}"],
                rounds_completed=result.rounds_completed,
                termination_reason=result.termination_reason,
            )

        synthesis_text = synthesis_path.read_text(encoding="utf-8")
        parsed = parse_synthesis(synthesis_text, mode=mode)

        persisted_path: str | None = None
        _root = find_project_root()
        if is_persistence_enabled(_root):
            try:
                persisted = persist_deliberation(
                    source_dir=result.output_dir,
                    project_root=_root,
                    question=question,
                    config_path=config_path,
                )
                persisted_path = str(persisted)
                cleanup_old_deliberations(_root)
            except Exception:
                logger.warning("Failed to persist deliberation output", exc_info=True)

        return DecideResult(
            sufficient=True,
            classification=classification,
            output=parsed.model_dump(),
            cost_estimate=cost_estimate,
            rounds_completed=result.rounds_completed,
            termination_reason=result.termination_reason,
            output_path=persisted_path,
        )

    except ConfigError as exc:
        logger.exception("Config error during run_decide_mcp")
        return DecideResult(
            sufficient=True,
            classification=classification,
            errors=[f"Config error: {exc}"],
        )
    except PipelineError as exc:
        logger.exception("Pipeline error during run_decide_mcp")
        return DecideResult(
            sufficient=True,
            classification=classification,
            cost_estimate=cost_estimate,
            errors=[f"Pipeline error: {exc}"],
        )
    except Exception as exc:
        logger.exception("Unexpected error during run_decide_mcp")
        return DecideResult(
            sufficient=True,
            classification=classification,
            errors=[f"Execution error: {exc}"],
        )
    finally:
        if tmp_dir is not None and tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# decide — CLI surface handler
# ---------------------------------------------------------------------------


def run_decide_cli(
    question: str,
    provider: str = "mock",
    mode: str = "cooperative",
    output: str | None = None,
    output_format: str = "rich",
) -> None:
    """Run an ad-hoc deliberation for the CLI surface.

    Behavior mirrors the existing ``decide`` command body in
    ``engine/cli/__init__.py``: displays Rich progress, prints the
    synthesis in either Rich or JSON format, and exits non-zero on
    errors via ``sys.exit(1)``. Returns ``None`` because the CLI
    communicates via stdout/stderr + exit code.

    ``output`` is a string rather than a Path to keep the registry
    Param types aligned with the other surfaces; the handler converts
    internally. The parameter name matches the CLI flag (``--output``)
    and the capability's ``Param(name="output", ...)`` declaration —
    the projector's keyword-forwarded dispatch requires all three to
    agree.
    """
    # Resolve settings cascade (spec 057)
    settings = load_settings()
    provider = resolve_setting(settings, provider if provider != "mock" else None, "default_provider")
    mode = resolve_setting(settings, mode if mode != "cooperative" else None, "default_mode")

    stripped = question.strip()
    if not stripped:
        click.echo("Error: question must not be empty.", err=True)
        sys.exit(1)

    # Classify question — warn if insufficient but don't block
    classification = classify_question(stripped, mode="non-interactive")
    if not classification.sufficient:
        click.echo(
            f"Warning: {classification.reason}",
            err=True,
        )

    output_path: Path | None = Path(output) if output else None

    try:
        config_path, question_path, tmp_dir = build_adhoc_config(
            question=stripped,
            mode=mode,
            output_dir=output_path,
        )
        use_temp_output = output_path is None
        effective_output = (
            (tmp_dir / "output") if use_temp_output else output_path.resolve()
        )
    except ConfigError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    try:
        from engine.cli.progress import RichProgressHandler
        from engine.run import run_engine

        progress_handler = RichProgressHandler()
        rich_emitter = CallbackEmitter(progress_handler)

        try:
            asyncio.run(
                run_engine(
                    config_path=config_path.resolve(),
                    provider_name=provider,
                    emitter=rich_emitter,
                )
            )
        except (ConfigError, ProviderError) as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)
        except Exception as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)

        synthesis_path = effective_output / "summary" / "final.md"
        if not synthesis_path.exists():
            click.echo(
                "Error: Synthesis output not found — pipeline may have failed.",
                err=True,
            )
            sys.exit(1)

        synthesis_text = synthesis_path.read_text(encoding="utf-8")

        try:
            result = parse_synthesis(synthesis_text, mode=mode)
        except ValueError as exc:
            click.echo(f"Error: Failed to parse synthesis: {exc}", err=True)
            sys.exit(1)

        if output_format == "json":
            click.echo(result.model_dump_json(indent=2))
        else:
            from engine.cli.render import render_result

            render_result(result)

        try:
            persisted = persist_deliberation(
                source_dir=effective_output,
                project_root=find_project_root(),
                question=question,
                config_path=config_path,
            )
            click.echo(f"\nOutput saved to: {persisted}")
            cleanup_old_deliberations(find_project_root())
        except Exception:
            logger.warning("Failed to persist deliberation output", exc_info=True)

    finally:
        if use_temp_output and tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Shared MCP pipeline helpers (moved from mcp_server.py on Day 6)
#
# Used by ``validate_mcp`` and ``run_mcp``. ``mcp_server.py`` still has
# the ``_parse_and_validate_config`` and ``_run_in_process`` names at
# module scope via alias imports, so existing tests that do
# ``from mcp_server import _parse_and_validate_config`` keep working.
# ---------------------------------------------------------------------------


def _parse_and_validate_config(
    config_yaml: str,
) -> tuple[dict[str, Any] | None, list[str], CostEstimate | None]:
    """Parse YAML config, validate templates, and estimate cost.

    Shared logic used by both ``validate_mcp`` and ``run_mcp`` to avoid
    duplicating YAML parsing, template validation, and cost estimation.

    Returns:
        ``(config_dict, errors, cost_estimate)`` — ``config_dict`` is
        ``None`` if YAML parsing failed or the result is not a dict.
    """
    try:
        config: dict[str, Any] = yaml.safe_load(config_yaml)
    except yaml.YAMLError as exc:
        logger.exception("YAML parse error")
        return None, [f"YAML parse error: {exc}"], None

    if not isinstance(config, dict):
        return None, ["Config must be a YAML mapping (dict), not a scalar or list"], None

    errors: list[str] = []
    try:
        root = find_project_root()
        mode = config.get("mode", "cooperative")
        result = validate_all(ValidationConfig(root=root, mode=mode))
        if not result.passed:
            for err in result.errors:
                msg = f"{err.file_path}: {err.message}"
                if err.suggestion:
                    msg += f" {err.suggestion}"
                errors.append(msg)
    except Exception as exc:
        logger.exception("Template validation error")
        errors.append(f"Template validation error: {exc}")

    cost_estimate: CostEstimate | None = None
    try:
        cost_estimate = _estimate_cost(config)
    except Exception as exc:
        logger.exception("Cost estimation error")
        errors.append(f"Cost estimation error: {exc}")

    return config, errors, cost_estimate


def _run_in_process(
    config_yaml: str,
    provider_name: str,
    validated: bool,
    errors: list[str],
    cost_estimate: CostEstimate | None,
) -> RunResult:
    """Execute a full deliberation pipeline in-process and return structured output.

    Writes the config YAML to a temp file in the current working directory
    (so relative paths in the config resolve correctly), creates the provider,
    runs the async pipeline synchronously, and parses the synthesis output.
    """
    tmp_path: Path | None = None
    try:
        fd, tmp_str = tempfile.mkstemp(
            prefix=".conversus_mcp_", suffix=".yml", dir=Path.cwd()
        )
        tmp_path = Path(tmp_str)
        try:
            with open(fd, "w", encoding="utf-8") as f:
                f.write(config_yaml)
        except Exception:
            import os
            os.close(fd)
            raise

        engine_config = parse_config(tmp_path)

        try:
            model_provider = resolve_provider(provider_name)
        except ProviderError as exc:
            errors_out = list(errors)
            errors_out.append(str(exc))
            return RunResult(
                mode="in_process",
                validated=validated,
                errors=errors_out,
                cost_estimate=cost_estimate,
            )

        emitter = NullEmitter()
        result = asyncio.run(
            run_pipeline(
                engine_config,
                model_provider,
                emitter,
                config_path=tmp_path,
            )
        )

        synthesis_path = result.output_dir / "summary" / "final.md"
        if not synthesis_path.exists():
            return RunResult(
                mode="in_process",
                validated=validated,
                errors=errors + [f"Pipeline completed but synthesis file not found: {synthesis_path}"],
                cost_estimate=cost_estimate,
                rounds_completed=result.rounds_completed,
                termination_reason=result.termination_reason,
            )

        synthesis_text = synthesis_path.read_text(encoding="utf-8")
        mode_name = engine_config.mode
        parsed = parse_synthesis(synthesis_text, mode=mode_name)

        persisted_path: str | None = None
        try:
            question = ""
            if engine_config and hasattr(engine_config, "question"):
                question = getattr(engine_config, "question", "")
            persisted = persist_deliberation(
                source_dir=result.output_dir,
                project_root=find_project_root(),
                question=question,
                config_path=tmp_path,
            )
            persisted_path = str(persisted)
            cleanup_old_deliberations(find_project_root())
        except Exception:
            logger.warning("Failed to persist deliberation output", exc_info=True)

        return RunResult(
            mode="in_process",
            validated=validated,
            errors=errors,
            cost_estimate=cost_estimate,
            output=parsed.model_dump(),
            rounds_completed=result.rounds_completed,
            termination_reason=result.termination_reason,
            output_path=persisted_path,
        )

    except ConfigError as exc:
        logger.exception("Engine config error during in-process execution")
        return RunResult(
            mode="in_process",
            validated=False,
            errors=errors + [f"Engine config error: {exc}"],
            cost_estimate=cost_estimate,
        )
    except PipelineError as exc:
        logger.exception("Pipeline error during in-process execution")
        return RunResult(
            mode="in_process",
            validated=validated,
            errors=errors + [f"Pipeline error: {exc}"],
            cost_estimate=cost_estimate,
        )
    except Exception as exc:
        logger.exception("Unexpected error during in-process execution")
        return RunResult(
            mode="in_process",
            validated=validated,
            errors=errors + [f"Execution error: {exc}"],
            cost_estimate=cost_estimate,
        )
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# validate — MCP and CLI surface handlers
# ---------------------------------------------------------------------------


def validate_mcp(config_yaml: str, question: str = "") -> ValidateResult:
    """Validate a conversus YAML configuration for the MCP surface.

    Parses the YAML, runs template validation, optionally classifies
    the deliberation question, and computes cost estimates. Returns a
    structured ``ValidateResult``; errors propagate via
    ``result.errors`` rather than exceptions.
    """
    config, errors, cost_estimate = _parse_and_validate_config(config_yaml)

    if config is None:
        return ValidateResult(
            valid=False,
            errors=errors,
        )

    classification: dict[str, Any] | None = None
    if question.strip():
        try:
            cr = classify_question(question, mode="non-interactive")
            classification = cr.model_dump()
        except Exception as exc:
            logger.exception("Question classification error")
            errors.append(f"Question classification error: {exc}")

    preset_info: list[str] | None = None
    agents = config.get("agents", [])
    if agents:
        mode_name = config.get("mode", "cooperative")
        agent_names = [a.get("name", "unnamed") for a in agents if isinstance(a, dict)]
        preset_info = [
            f"mode: {mode_name}",
            f"agents: {', '.join(agent_names)}",
            f"iterations: {config.get('iterations', 1)}",
        ]

    valid = len(errors) == 0

    return ValidateResult(
        valid=valid,
        errors=errors,
        cost_estimate=cost_estimate,
        classification=classification,
        preset_info=preset_info,
    )


def validate_cli(config_path: str, question: str | None = None) -> None:
    """Validate a conversus YAML config for the CLI surface.

    Mirrors the hand-written ``engine.cli.validate`` body: parses the
    config via ``engine.config.parse_config``, prints a cost summary,
    optionally classifies the question, and exits non-zero on failure.
    ``config_path`` is a string rather than a Path because the
    constitution-compliant ``Param`` type set only includes primitives;
    the handler converts internally.
    """
    try:
        config = parse_config(Path(config_path).resolve())
    except ConfigError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(f"Config valid: {config_path}")
    click.echo(f"Mode: {config.mode}")
    click.echo("")
    # Cost summary: delegate to the same formatter used by the
    # hand-written CLI (kept there for Day 6 to avoid a second move).
    from engine.cli import _format_cost_estimate

    click.echo(
        _format_cost_estimate(
            agent_count=len(config.agents),
            iterations=config.iterations,
            has_arbiter=config.arbiter is not None,
        )
    )

    if question is not None:
        result = classify_question(question)
        click.echo("")
        click.echo(
            f"Question classification: "
            f"{'sufficient' if result.sufficient else 'insufficient'}"
        )
        if result.reason:
            click.echo(f"  Reason: {result.reason}")


# ---------------------------------------------------------------------------
# run — MCP and CLI surface handlers
# ---------------------------------------------------------------------------


def run_mcp(
    config_yaml: str,
    output_path: str = "",
    provider: str = "",
) -> RunResult:
    """Validate a config and optionally run or parse a deliberation.

    Three modes:

    - **validate_only** (empty ``output_path``, empty ``provider``):
      validates config, estimates cost, returns execution instructions.
    - **parsed_output** (``output_path`` set): validates config, reads
      and parses the synthesis file at the path, returns structured
      ``ConversusOutput``.
    - **in_process** (``provider`` set, empty ``output_path``): validates
      config, runs the full engine pipeline in-process, returns
      structured ``ConversusOutput``.
    """
    config, errors, cost_estimate = _parse_and_validate_config(config_yaml)

    if config is None:
        return RunResult(
            mode="validate_only",
            validated=False,
            errors=errors,
            instructions="Config has errors — fix them before running.",
        )

    validated = len(errors) == 0

    if provider and provider.strip() and (not output_path or not output_path.strip()):
        return _run_in_process(
            config_yaml, provider.strip(), validated, errors, cost_estimate
        )

    if not output_path or not output_path.strip():
        instructions = (
            "Config valid. Execute '/conversus run <path>' in your editor "
            "to run the deliberation."
            if validated
            else "Config has errors — fix them before running."
        )
        return RunResult(
            mode="validate_only",
            validated=validated,
            errors=errors,
            cost_estimate=cost_estimate,
            instructions=instructions,
        )

    output_file = Path(output_path.strip())
    if not output_file.exists():
        return RunResult(
            mode="parsed_output",
            validated=validated,
            errors=errors + [f"Output file not found: {output_path}"],
            cost_estimate=cost_estimate,
        )

    try:
        synthesis_text = output_file.read_text(encoding="utf-8")
        mode_name = config.get("mode", "cooperative")
        parsed = parse_synthesis(synthesis_text, mode=mode_name)
        return RunResult(
            mode="parsed_output",
            validated=validated,
            errors=errors,
            cost_estimate=cost_estimate,
            output=parsed.model_dump(),
        )
    except Exception as exc:
        logger.exception("Synthesis parse error")
        return RunResult(
            mode="parsed_output",
            validated=validated,
            errors=errors + [f"Synthesis parse error: {exc}"],
            cost_estimate=cost_estimate,
        )


def run_cli(
    config_path: str,
    provider: str = "mock",
    model: str | None = None,
    rounds: int | None = None,
    phase: str = "all",
) -> None:
    """Run a deliberation from a conversus config file (CLI surface).

    Mirrors the hand-written ``engine.cli.run`` body: runs the engine
    asynchronously with Rich progress display, prints each written
    output path on success, and exits non-zero on failure.
    """
    from engine.cli.progress import RichProgressHandler
    from engine.run import run_engine

    progress_handler = RichProgressHandler()
    rich_emitter = CallbackEmitter(progress_handler)

    try:
        written_paths = asyncio.run(
            run_engine(
                config_path=Path(config_path).resolve(),
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

    try:
        # Derive output directory from written paths; fall back to config sibling
        if written_paths:
            output_dir = Path(written_paths[0]).resolve().parent
            # Walk up to the root output directory (above phase subdirectories)
            config_parent = Path(config_path).resolve().parent
            while output_dir != config_parent and output_dir.parent != output_dir:
                if output_dir.parent == config_parent:
                    break
                output_dir = output_dir.parent
        else:
            output_dir = Path(config_path).resolve().parent / "output"

        if output_dir.is_dir():
            persisted = persist_deliberation(
                source_dir=output_dir,
                project_root=find_project_root(),
                question="",
                config_path=Path(config_path),
            )
            click.echo(f"\nOutput saved to: {persisted}")
            cleanup_old_deliberations(find_project_root())
    except Exception:
        logger.warning("Failed to persist deliberation output", exc_info=True)


# ---------------------------------------------------------------------------
# login / logout — CLI-only auth commands
# ---------------------------------------------------------------------------


def login_cli(provider: str) -> None:
    """Log in to a model provider via OAuth (CLI surface)."""
    from engine import auth

    try:
        auth.login(provider)
    except ProviderError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo("Login successful")


def login_mcp(provider: str) -> str:
    """Log in to a model provider via OAuth (MCP surface).

    Opens the user's browser for OAuth authentication. The token is
    stored in ``~/.conversus/auth.json`` so subsequent deliberations
    use it automatically. Desktop Extension users can say "log in to
    anthropic" in their chat and the browser opens — no CLI needed.

    Returns a status message (success or error description).
    """
    from engine import auth

    try:
        auth.login(provider)
        return f"Login successful for {provider}. Your credentials are stored securely and will be used for future deliberations."
    except ProviderError as exc:
        return f"Login failed for {provider}: {exc}"
    except Exception as exc:
        return f"Login error: {exc}"


def logout_cli(provider: str) -> None:
    """Log out of a model provider (CLI surface)."""
    from engine import auth

    auth.logout(provider)
    click.echo("Logged out")


# ---------------------------------------------------------------------------
# status — CLI-only auth status table
# ---------------------------------------------------------------------------


def status_cli() -> None:
    """Show authentication status for all providers (CLI surface).

    Renders a Rich table with the auth state (logged in, env var
    fallback, or not configured) for every known OAuth provider.
    """
    import os
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
            table.add_row(provider, "[yellow]env var[/yellow]", config["env_var"])

        else:
            table.add_row(provider, "[red]not configured[/red]", "—")

    console.print(table)


# ---------------------------------------------------------------------------
# context — CLI-only debug context detection
# ---------------------------------------------------------------------------


def context_cli(as_json: bool = False) -> None:
    """Print the detected invocation context (CLI surface).

    Renders the resolved provider, renderer, and exit code scheme either
    as a Rich table (default) or machine-readable JSON (``--json``).
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
# mcp — CLI-only server launcher
# ---------------------------------------------------------------------------


def mcp_cli() -> None:
    """Start the Conversus MCP server on stdio transport (CLI surface).

    This is a "meta-command" that loads ``mcp_server.py`` and invokes
    its ``FastMCP.run(transport='stdio')``. It does not project to any
    other surface because MCP servers are by definition launched by the
    editor process, not by other tools.
    """
    try:
        from mcp.server.fastmcp import FastMCP  # noqa: F401 — presence check
    except ImportError:
        click.echo(
            "Error: MCP dependencies are not installed.\n"
            "Install them with: pip install conversus[mcp]",
            err=True,
        )
        sys.exit(1)

    import importlib.util as _ilu

    _server_path = Path(__file__).parent.parent / "mcp_server.py"
    if not _server_path.exists():
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
# init — CLI-only project initialization
# ---------------------------------------------------------------------------


def init_cli(
    runtimes: str = "claude-code",
    default_provider: str = "claude-code",
    default_model: str = "sonnet",
    force: bool = False,
) -> None:
    """Initialize a .conversus/ directory with runtime permissions (CLI surface).

    ``runtimes`` is a comma-separated string (e.g. ``"claude-code,opencode"``)
    because the registry Param type set only includes scalar primitives.
    The hand-written CLI uses Click's ``multiple=True`` for repeatable
    ``--runtime`` flags; this is a known divergence noted in
    ``docs/developer-guide/gotchas.md`` and tracked as a framework
    polish item (``Param.multiple`` support).
    """
    from engine.project import init_project

    project_root = find_project_root()
    runtime_list = [r.strip() for r in runtimes.split(",") if r.strip()]

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

    # --- spec 057: create .conversus/settings.yml with init defaults -------
    try:
        settings_dir = project_root / ".conversus"
        settings_dir.mkdir(parents=True, exist_ok=True)
        settings_file = settings_dir / "settings.yml"
        if not settings_file.exists() or force:
            settings_data = {
                "default_provider": default_provider,
                "default_model": default_model,
                "default_mode": "cooperative",
                "max_launches": 20,
                "persistence": {
                    "enabled": True,
                    "retention_days": 90,
                },
            }
            settings_file.write_text(
                yaml.dump(settings_data, default_flow_style=False, sort_keys=False),
                encoding="utf-8",
            )
            created["settings"] = settings_file

        # spec 056: proactively create deliberations directory
        (settings_dir / "deliberations").mkdir(exist_ok=True)

        # global ~/.conversus/ directory with empty settings.yml
        global_dir = Path.home() / ".conversus"
        global_settings = global_dir / "settings.yml"
        if not global_settings.exists():
            global_dir.mkdir(parents=True, exist_ok=True)
            global_settings.write_text(
                "# Global conversus defaults\n# See: specs/057-settings-architecture.md\n",
                encoding="utf-8",
            )
    except Exception as settings_exc:
        click.echo(
            f"Warning: settings creation failed: {settings_exc}", err=True,
        )

    click.echo(f"Initialized .conversus/ in {project_root}")
    for desc, path in created.items():
        rel = path.relative_to(project_root) if path.is_relative_to(project_root) else path
        click.echo(f"  {desc}: {rel}")

    click.echo("")
    click.echo(f"Runtimes configured: {', '.join(runtime_list)}")
    click.echo(f"Default provider: {default_provider}")
    click.echo(f"Default model: {default_model}")


# ---------------------------------------------------------------------------
# list / show deliberations — MCP and CLI surface handlers (spec 056)
# ---------------------------------------------------------------------------


def list_deliberations_mcp(project_root: str = "") -> ListResult:
    """List past deliberations for the MCP surface."""
    root: Path = Path(project_root) if project_root else find_project_root()
    deliberations: list[dict[str, Any]] = _list_deliberations(root)
    return ListResult(
        deliberations=deliberations,
        count=len(deliberations),
        project_root=str(root),
    )


def list_deliberations_cli(as_json: bool = False) -> None:
    """List past deliberations for the CLI surface."""
    root: Path = find_project_root()
    deliberations: list[dict[str, Any]] = _list_deliberations(root)

    if as_json:
        import json as _json

        click.echo(_json.dumps(deliberations, indent=2, default=str))
        return

    if not deliberations:
        click.echo("No deliberations found in .conversus/deliberations/")
        return

    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title=f"Deliberations ({len(deliberations)})")
    table.add_column("Date", style="cyan")
    table.add_column("Question", style="white", max_width=50)
    table.add_column("Mode", style="yellow")
    table.add_column("Synthesis", style="green")

    for d in deliberations:
        table.add_row(
            d.get("timestamp", "?"),
            d.get("question", "?")[:50],
            d.get("mode", "?"),
            "yes" if d.get("has_synthesis") else "no",
        )

    console.print(table)


def show_deliberation_mcp(deliberation_path: str, file_path: str) -> ShowResult:
    """Read a file from a past deliberation for the MCP surface."""
    root: Path = find_project_root()
    try:
        content: str = read_deliberation_file(root, deliberation_path, file_path)
        return ShowResult(
            content=content,
            deliberation_path=deliberation_path,
            file_path=file_path,
        )
    except (ValueError, FileNotFoundError) as exc:
        return ShowResult(
            content="",
            deliberation_path=deliberation_path,
            file_path=file_path,
            errors=[str(exc)],
        )


def show_deliberation_cli(deliberation_path: str, file_path: str) -> None:
    """Read a file from a past deliberation for the CLI surface."""
    root: Path = find_project_root()
    try:
        content: str = read_deliberation_file(root, deliberation_path, file_path)
        click.echo(content)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)


# ---------------------------------------------------------------------------
# skills / skill — list and view capability guidance (spec 059 Phase 2)
# ---------------------------------------------------------------------------

_SKILLS_DIR = Path(__file__).resolve().parent.parent / "claude-code-plugin" / "skills"


def skills_cli() -> None:
    """List all available conversus skills with summaries (CLI surface)."""
    # Import the real CAPABILITIES list to get summaries
    try:
        _repo_root = Path(__file__).resolve().parent.parent
        _sys_path_added = False
        if str(_repo_root) not in sys.path:
            sys.path.insert(0, str(_repo_root))
            _sys_path_added = True
        from capabilities import CAPABILITIES
        if _sys_path_added:
            sys.path.remove(str(_repo_root))
    except ImportError:
        click.echo("Error: capabilities.py not found at repo root.", err=True)
        sys.exit(1)

    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="Conversus Skills")
    table.add_column("Skill", style="bold cyan")
    table.add_column("Summary", style="white")
    table.add_column("Surfaces", style="dim")

    for cap in CAPABILITIES:
        surfaces = ", ".join(s.value for s in cap.surfaces)
        table.add_row(cap.name, cap.summary, surfaces)

    console.print(table)
    click.echo(f"\nUse 'conversus skill <name>' to see the full guided workflow.")


def skill_cli(name: str) -> None:
    """Print the SKILL.md guided workflow for a capability (CLI surface)."""
    skill_path = _SKILLS_DIR / name / "SKILL.md"
    if not skill_path.is_file():
        # Try hyphenated name (list-deliberations → list-deliberations/)
        skill_path = _SKILLS_DIR / name.replace("_", "-") / "SKILL.md"

    if not skill_path.is_file():
        click.echo(f"Error: no skill found for '{name}'.", err=True)
        click.echo(f"Available skills: {', '.join(d.name for d in _SKILLS_DIR.iterdir() if d.is_dir())}", err=True)
        sys.exit(1)

    click.echo(skill_path.read_text(encoding="utf-8"))
