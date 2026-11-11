"""Decide on a tool call (PreToolUse) and record what happened (PostToolUse)."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from engine.gate import ledger, protect
from engine.gate.config import GateConfig
from engine.gate.judge import Judge, build_prompt, clip, make_judge, rule_on
from engine.gate.ledger import Decision, History, Outcome, Prompted
from engine.gate.redact import redact

logger = logging.getLogger("deliberator.gate")
GRAPH_JSON = Path(".deliberator") / "gate" / "graph.json"


def _push_quietly(root: Path, decisions: list[Decision], history: History,
                  config: GateConfig) -> None:
    """Write to the graph database if one is configured. Never fails the hook: the log is
    the record, and `deliberator gate sync` writes anything that was missed."""
    if not config.graph_uri:
        return
    try:
        from engine.gate.graph import push

        push(decisions, history, config)
    except Exception as exc:  # noqa: BLE001
        logger.warning("gate: graph write failed (%s); run `deliberator gate sync`", exc)


EDIT_TOOLS = protect.EDIT_TOOLS


def _not_a_project(base: Path) -> bool:
    home = Path.home().resolve()
    return base in (home, Path("/"), home / "code")


def _edit_inside(tool: str, tool_input: dict[str, Any], cwd: str) -> bool:
    """An edit tool writing a file inside the git repository that holds `cwd`.

    Refused when cwd is ~, / or ~/code, when cwd is in no git repo (or the repo is ~ or /),
    and for files outside the repo root. Protected paths (.git, .claude, ...) are checked
    separately and always go to the judge.
    """
    if tool not in EDIT_TOOLS or not cwd:
        return False
    raw = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not raw or not isinstance(raw, str):
        return False
    base = Path(cwd).expanduser().resolve()
    if _not_a_project(base):
        return False  # a session in ~, / or ~/code is not "a project"
    repo = ledger.git_root(str(base))
    if repo is None or _not_a_project(repo.resolve()):
        return False
    path = Path(raw).expanduser()
    path = (path if path.is_absolute() else base / path).resolve()
    try:
        path.relative_to(repo.resolve())
    except ValueError:
        return False
    return not _runs_code(path) and not _risky_content(_written_text(tool, tool_input))


# Files that run, or configure what runs: always judged, whatever the edit says.
_RUNNABLE_SUFFIXES = frozenset({
    ".sh", ".bash", ".zsh", ".fish", ".command", ".ps1", ".bat", ".cmd", ".service",
    ".plist", ".desktop",
})
_RUNNABLE_NAMES = frozenset({
    "makefile", "gnumakefile", "justfile", "dockerfile", "containerfile", "procfile",
    "package.json", "pyproject.toml", "setup.py", "setup.cfg", "conftest.py", ".envrc",
    "build.rs", "cargo.toml", ".pre-commit-config.yaml", ".npmrc", ".pypirc", "noxfile.py",
    "tox.ini", "vercel.json", "vercel.ts", "docker-compose.yml", "docker-compose.yaml",
    "compose.yml", "compose.yaml", ".gitattributes", ".gitmodules",
})
_RUNNABLE_DIRS = frozenset({".github", ".circleci", ".husky", "hooks", "bin", "scripts"})


def _runs_code(path: Path) -> bool:
    name = path.name.lower()
    return (path.suffix.lower() in _RUNNABLE_SUFFIXES or name in _RUNNABLE_NAMES
            or bool(_RUNNABLE_DIRS & {p.lower() for p in path.parts[:-1]}))


def _written_text(tool: str, tool_input: dict[str, Any]) -> str:
    """What the edit puts in the file (new text only)."""
    if tool == "Write":
        return str(tool_input.get("content") or "")
    if tool == "Edit":
        return str(tool_input.get("new_string") or "")
    if tool == "MultiEdit":
        return "\n".join(str(e.get("new_string") or "") for e in tool_input.get("edits") or []
                         if isinstance(e, dict))
    if tool == "NotebookEdit":
        return str(tool_input.get("new_source") or "")
    return ""


# Content that reaches the network, deletes, runs processes, touches credentials or talks to
# the gate: the judge reads it before it is written. Ordinary code and prose skips the model.
_RISKY_CONTENT = re.compile(
    r"\b(?:curl|wget|nc|ncat|netcat|socat|ssh|scp|sftp|telnet|ftp)\b"
    r"|rm\s+-[a-z]*[rf]|\brmtree\b|\bunlink\(|\bshred\b|\bmkfs\b|\bdd\s+if="
    r"|\bsudo\b|\bchmod\s+[0-7]*[+]?[sx]|\bchown\b"
    r"|\beval\s*\(|\bexec\s*\(|os\.system|os\.popen|\bsubprocess\b|child_process"
    r"|\bspawn\(|Runtime\.getRuntime|\bpty\b|\bsocket\b"
    r"|requests\.(?:post|put|patch)|\bfetch\s*\(|urllib|http\.client|httpx|aiohttp"
    r"|base64\s+-d|b64decode|atob\(|\bfromCharCode\b"
    r"|\.aws\b|\.ssh\b|id_rsa|id_ed25519|credentials|\.netrc|\.npmrc|keychain"
    r"|\.claude\b|\.deliberator\b|permission gate|previous instructions|\bverdict\b"
    r"|\bcrontab\b|launchctl|LaunchAgents|\.zshrc|\.bashrc|\.profile\b",
    re.IGNORECASE,
)


def _risky_content(text: str) -> bool:
    return bool(_RISKY_CONTENT.search(text))


def _risky_flags(subject: str) -> bool:
    """Flags that make a read-only-looking command write, delete, run or force something."""
    if _RISKY.search(subject):
        return True
    return subject.split()[:1] == ["git"] and bool(_GIT_F.search(subject))


_RISKY = re.compile(
    r"(?:^|\s)(?:-delete|-exec|-execdir|-ok|-okdir|-fprint\S*|-fls|--pre(?:-glob)?|--output\S*"
    r"|-o|-D|--force\S*|--delete\S*|--in-place\S*)(?=\s|=|$)"
    r"|(?:^|\s)-o\S"  # -ofile
)
_GIT_F = re.compile(r"(?:^|\s)-[A-Za-z]*f[A-Za-z]*(?=\s|$)")


async def decide(
    root: Path,
    config: GateConfig,
    *,
    tool: str,
    tool_input: dict[str, Any],
    cwd: str,
    session: str | None = None,
    tool_use_id: str | None = None,
    judge: Judge | None = None,
    push_graph: bool = True,
) -> Decision:
    """Rule on one tool call and log the decision.

    Order: allow-list or edit inside the repo (no model call) → a standing grant → identical
    earlier call (same command or path AND same content: reuse, or allowed because the
    person approved it) → the judge, shown the call's content and the closest precedents.
    Calls touching protected paths, and calls too long to show whole, skip the shortcuts and
    always go to the judge.
    """
    view = ledger.view_of(tool, tool_input)
    raw_subject = view.subject
    subject = redact(raw_subject)
    rules_hash = config.rules_hash()
    key = ledger.call_key(tool, raw_subject, cwd, rules_hash, view.digest)
    shown, cut = clip(redact(view.text))
    truncated = cut > 0
    extra = [config.store_root(root) / ledger.LOG_PATH.parent] if config.log_dir else []
    protected = protect.touches_protected(tool, tool_input, cwd, extra)
    project = ledger.project_of(cwd)
    history = ledger.read(root)
    base: dict[str, Any] = {
        "id": ledger.new_id(key), "at": ledger.now(), "session": session,
        "tool_use_id": tool_use_id, "tool": tool, "subject": subject, "cwd": cwd, "key": key,
        "rules_hash": rules_hash, "project": project, "truncated": truncated,
        "protected": protected,
    }
    shortcuts = not protected and not truncated

    decision: Decision | None = None
    if not protected and config.allow_edits_in_project and _edit_inside(tool, tool_input, cwd):
        decision = Decision(**base, verdict="allow", source="skip",
                            reason="an edit to a file inside the working repository")
    simple = tool != "Bash" or not (ledger.compound(raw_subject) or _risky_flags(raw_subject))
    for pattern in config.allow_without_asking if decision is None and simple and shortcuts \
            else ():
        try:
            if re.search(pattern, raw_subject):
                decision = Decision(**base, verdict="allow", source="skip",
                                    reason=f"allowed without asking: matches {pattern!r}")
                break
        except re.error:
            continue

    if decision is None and shortcuts and config.learn_from_approvals:
        grant = history.granted(tool, subject, project)
        if grant is not None:
            decision = Decision(**base, verdict="allow", source="approved",
                                reason=f"you said yes to calls like this ({grant.grant})",
                                precedents=(grant.id,))

    if decision is None and shortcuts and (config.reuse_identical or config.learn_from_approvals):
        for earlier in ledger.latest_for_key(history, key):
            if earlier.source in ("error", "skip") or earlier.truncated or earlier.protected:
                continue
            if config.learn_from_approvals and history.approved(earlier):
                decision = Decision(**base, verdict="allow", source="approved",
                                    reason=f"you approved this exact call before ({earlier.id})",
                                    precedents=(earlier.id,))
            elif config.reuse_identical and earlier.verdict in ("allow", "deny"):
                decision = Decision(**base, verdict=earlier.verdict, source="reuse",
                                    rule=earlier.rule, model=earlier.model,
                                    reason=f"{earlier.reason} (same as {earlier.id})",
                                    precedents=(earlier.id,))
            if decision is not None:
                break

    if decision is None:
        precedents = ledger.similar(history, tool=tool, subject=subject, cwd=cwd,
                                    k=config.precedents)
        prompt = build_prompt(config, tool=tool, subject=subject, cwd=cwd,
                              precedents=precedents, history=history, text=shown,
                              truncated=cut)
        ruling = await rule_on(prompt, judge or make_judge(config), subject,
                               timeout_s=config.timeout_s)
        failed = ruling.reason.startswith("gate could not rule")
        decision = Decision(
            **base, verdict=ruling.verdict, reason=redact(ruling.reason), rule=ruling.rule,
            source="error" if failed else "model", model=config.resolved_model(),
            precedents=tuple(p.id for p in precedents), latency_ms=ruling.latency_ms,
            input_tokens=ruling.input_tokens, output_tokens=ruling.output_tokens,
            grant=ruling.grant if shortcuts else None,
        )

    decision = ledger.redacted(decision)  # secrets never reach the log, graph or reply
    ledger.append(root, decision)
    if push_graph:
        history.decisions.append(decision)
        _push_quietly(root, [decision], history, config)
    return decision


def _pending(root: Path, tool: str, tool_input: dict[str, Any], session: str | None,
             tool_use_id: str | None) -> tuple[History, Decision | None]:
    history = ledger.read(root)
    subject = redact(ledger.subject_of(tool, tool_input))
    return history, ledger.find_pending(history, tool_use_id=tool_use_id, session=session,
                                        tool=tool, subject=subject)


def prompted(root: Path, config: GateConfig, *, tool: str, tool_input: dict[str, Any],
             session: str | None = None, tool_use_id: str | None = None) -> Decision | None:
    """Claude Code is showing the person a permission prompt for this call (PermissionRequest).

    Together with the tool running afterwards, this is what makes an ask an approval."""
    history, decision = _pending(root, tool, tool_input, session, tool_use_id)
    if decision is None or decision.id in history.prompted:
        return None
    ledger.append(root, Prompted(decision=decision.id, at=ledger.now()))
    return decision


def record(root: Path, config: GateConfig, *, tool: str, tool_input: dict[str, Any],
           session: str | None = None, tool_use_id: str | None = None,
           push_graph: bool = True) -> Decision | None:
    """The tool ran: log it against its decision. An ask that ran was approved."""
    history, decision = _pending(root, tool, tool_input, session, tool_use_id)
    if decision is None or decision.id in history.ran:
        return None
    ledger.append(root, Outcome(decision=decision.id, at=ledger.now()))
    history.ran.add(decision.id)
    if push_graph:
        _push_quietly(root, [decision], history, config)
    return decision


def hook_output(decision: Decision, config: GateConfig) -> dict[str, Any]:
    """Claude Code PreToolUse output. The reason is shown to Claude on deny, to you on ask."""
    rule = ""
    if decision.rule and 1 <= decision.rule <= len(config.rules):
        rule = f" (rule {decision.rule}: {config.rules[decision.rule - 1]})"
    grant = ""
    if decision.verdict == "ask" and decision.grant:
        grant = f" Yes is kept forever for calls matching {decision.grant}"
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision.verdict,
            "permissionDecisionReason": f"[deliberator gate] {decision.reason}{rule}{grant}",
        }
    }


def write_graph_json(root: Path, config: GateConfig) -> Path:
    from engine.gate.graph import node_link

    path = root / GRAPH_JSON
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(node_link(ledger.read(root), config), indent=1), encoding="utf-8")
    return path
