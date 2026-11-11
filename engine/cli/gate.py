"""``deliberator gate``: graph-backed yes/no hooks for Claude Code.

    deliberator gate hook      # PreToolUse: reads hook JSON on stdin, prints the decision
    deliberator gate record    # PostToolUse: the tool ran; an approved ask becomes precedent
    deliberator gate check -c "git push --force origin main"
    deliberator gate log       # recent decisions
    deliberator gate sync      # write graph.json and every decision to the graph database
    deliberator gate init      # write .deliberator/gate.yml and print the hook settings
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

import click

HOOK_SETTINGS = {
    "hooks": {
        "PreToolUse": [{
            "matcher": "Bash|Write|Edit|MultiEdit|NotebookEdit",
            "hooks": [{"type": "command", "command": "deliberator gate hook", "timeout": 60}],
        }],
        "PostToolUse": [{
            "matcher": "Bash|Write|Edit|MultiEdit|NotebookEdit",
            "hooks": [{"type": "command", "command": "deliberator gate record", "timeout": 15}],
        }],
    }
}


def _root(cwd: str | None) -> Path:
    from engine.persistence import find_user_project_root

    return find_user_project_root(Path(cwd) if cwd else None)


def _ask(reason: str) -> dict[str, Any]:
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "ask",
        "permissionDecisionReason": f"[deliberator gate] {reason}"[:500]}}


@click.group(name="gate")
def gate() -> None:
    """Graph-backed allow/deny/ask decisions for Claude Code tool calls."""


@gate.command(name="hook")
def hook_cmd() -> None:
    """PreToolUse hook: read the hook JSON on stdin, print the decision JSON.

    Anything that goes wrong prints an ask, so you get a permission prompt; it never
    allows by default.
    """
    try:
        event = json.loads(sys.stdin.read() or "{}")
        from engine.gate import decide, hook_output, load_config

        cwd = event.get("cwd") or str(Path.cwd())
        root = _root(cwd)
        config = load_config(root)
        decision = asyncio.run(decide(
            config.store_root(root), config, tool=str(event.get("tool_name", "")),
            tool_input=event.get("tool_input") or {}, cwd=cwd,
            session=event.get("session_id"), tool_use_id=event.get("tool_use_id"),
        ))
        payload = hook_output(decision, config)
    except Exception as exc:  # noqa: BLE001 - the hook must always answer.
        payload = _ask(f"gate failed ({type(exc).__name__}: {exc}); asking instead")
    click.echo(json.dumps(payload))


@gate.command(name="record")
def record_cmd() -> None:
    """PostToolUse hook: record that the tool ran. Prints nothing; never blocks."""
    try:
        event = json.loads(sys.stdin.read() or "{}")
        from engine.gate import load_config, record

        root = _root(event.get("cwd"))
        config = load_config(root)
        record(config.store_root(root), config, tool=str(event.get("tool_name", "")),
               tool_input=event.get("tool_input") or {}, session=event.get("session_id"),
               tool_use_id=event.get("tool_use_id"))
    except Exception as exc:  # noqa: BLE001
        click.echo(f"deliberator gate record: {exc}", err=True)


@gate.command(name="check")
@click.option("--command", "-c", "command", required=True, help="A shell command to rule on.")
@click.option("--tool", default="Bash", show_default=True)
@click.option("--provider", default=None, help="Override the configured provider.")
@click.option("--dry-run", is_flag=True, help="Do not write the decision to the log.")
def check_cmd(command: str, tool: str, provider: str | None, dry_run: bool) -> None:
    """Rule on one command from the terminal and print the decision."""
    import tempfile

    from engine.gate import decide, hook_output, load_config

    root = _root(None)
    config = load_config(root)
    if provider:
        config = config.model_copy(update={"provider": provider})
    target = config.store_root(root)
    store = target
    if dry_run:
        # Read precedent from the real log, write to a throwaway copy.
        target = Path(tempfile.mkdtemp(prefix="gate-dry-"))
        src = store / ".deliberator" / "gate" / "log.jsonl"
        if src.is_file():
            (target / ".deliberator" / "gate").mkdir(parents=True)
            (target / ".deliberator" / "gate" / "log.jsonl").write_bytes(src.read_bytes())
    tool_input = {"command": command} if tool == "Bash" else {"file_path": command}
    decision = asyncio.run(decide(target, config, tool=tool, tool_input=tool_input,
                                  cwd=str(Path.cwd()), push_graph=not dry_run))
    click.echo(json.dumps({"decision": decision.model_dump(),
                           "hook": hook_output(decision, config)}, indent=1))


@gate.command(name="log")
@click.option("-n", "limit", default=20, show_default=True)
def log_cmd(limit: int) -> None:
    """Recent decisions, newest last."""
    from engine.gate import load_config
    from engine.gate.ledger import read

    root = _root(None)
    history = read(load_config(root).store_root(root))
    for d in history.decisions[-limit:]:
        mark = " (approved)" if history.approved(d) else ""
        click.echo(f"{d.at[:19]}  {d.verdict:5}{mark:11} {d.source:8} {d.tool}: "
                   f"{d.subject[:70]!s}  — {d.reason[:80]}")


@gate.command(name="grants")
def grants_cmd() -> None:
    """Standing yeses: asks you approved, and the pattern of calls each one now allows."""
    from engine.gate import load_config
    from engine.gate.ledger import read

    root = _root(None)
    history = read(load_config(root).store_root(root))
    grants = history.grants()
    if not grants:
        click.echo("No standing grants.")
    for d in grants:
        click.echo(f"{d.id}  {d.tool}: {d.grant}\n    first approved for: {d.subject[:100]}")


@gate.command(name="revoke")
@click.argument("decision_id")
def revoke_cmd(decision_id: str) -> None:
    """Withdraw a standing grant (and the exact-call approval) by its decision id."""
    from engine.gate import load_config
    from engine.gate.ledger import Revoke, append, now, read

    root = _root(None)
    store = load_config(root).store_root(root)
    if decision_id not in {d.id for d in read(store).decisions}:
        raise click.ClickException(f"no decision {decision_id}; see `deliberator gate grants`")
    append(store, Revoke(decision=decision_id, at=now()))
    click.echo(f"Revoked {decision_id}.")


@gate.command(name="sync")
def sync_cmd() -> None:
    """Write graph.json, and every decision to the graph database if one is configured."""
    from engine.gate import load_config
    from engine.gate.core import write_graph_json
    from engine.gate.graph import push
    from engine.gate.ledger import read

    root = _root(None)
    config = load_config(root)
    store = config.store_root(root)
    path = write_graph_json(store, config)
    click.echo(f"graph.json: {path}")
    if config.graph_uri:
        history = read(store)
        n = push(history.decisions, history, config)
        click.echo(f"{config.graph_uri}: {len(history.decisions)} decisions, {n} statements")
    else:
        click.echo("No graph_uri in .deliberator/gate.yml; database write skipped.")


@gate.command(name="init")
@click.option("--force", is_flag=True, help="Overwrite an existing gate.yml.")
def init_cmd(force: bool) -> None:
    """Write .deliberator/gate.yml and print the hook settings to add."""
    from engine.gate.config import CONFIG_PATH, EXAMPLE_CONFIG

    root = _root(None)
    path = root / CONFIG_PATH
    if path.exists() and not force:
        click.echo(f"{path} exists (use --force to overwrite).")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(EXAMPLE_CONFIG, encoding="utf-8")
        click.echo(f"Wrote {path}")
    click.echo("\nFor every project, put the config in ~/.config/deliberator/gate.yml instead.")
    click.echo("\nAdd to .claude/settings.json (project) or ~/.claude/settings.json:\n")
    click.echo(json.dumps(HOOK_SETTINGS, indent=2))
