"""Decide on a tool call (PreToolUse) and record what happened (PostToolUse)."""

from __future__ import annotations

import fnmatch
import json
import logging
import os
import re
import shlex
from pathlib import Path
from typing import Any

from engine.gate import ledger, ops, protect
from engine.gate.config import GateConfig
from engine.gate.judge import (
    BYPASS_NOTE,
    Judge,
    build_prompt,
    clip,
    make_judge,
    rule_on,
)
from engine.gate.ledger import Decision, History, Outcome, Prompted
from engine.gate.redact import redact
from engine.gate.simple import (
    repo_state,
    runs_git,
    safe_git,
    simple_words,
    untrusted_target,
)

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


# Files that run, configure what runs, or instruct the agent: an edit to one is always
# judged, whatever it says (never the in-repo skip). Matched case-insensitively.
_RUNNABLE_SUFFIXES = frozenset({
    ".sh", ".bash", ".zsh", ".fish", ".command", ".ps1", ".bat", ".cmd", ".service",
    ".plist", ".desktop", ".pth",
})
_RUNNABLE_NAMES = frozenset({
    # build, task and package scripts
    "makefile", "gnumakefile", "justfile", "taskfile.yml", "taskfile.yaml", "rakefile",
    "gradlew", "gradlew.bat", "build.gradle", "build.gradle.kts", "settings.gradle",
    "dockerfile", "containerfile", "procfile", "package.json", "pyproject.toml", "setup.py",
    "setup.cfg", "conftest.py", "sitecustomize.py", "usercustomize.py", "noxfile.py",
    "tox.ini", "pytest.ini", "build.rs", "cargo.toml", "vercel.json", "vercel.ts",
    "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml",
    # tool and hook config
    ".envrc", ".npmrc", ".pypirc", ".yarnrc", ".yarnrc.yml", "mise.toml", ".mise.toml",
    ".tool-versions", ".pre-commit-config.yaml", "lefthook.yml", "lefthook.yaml",
    ".lefthook.yml", ".gitattributes", ".gitmodules",
    # CI
    ".gitlab-ci.yml", "jenkinsfile", ".travis.yml", "azure-pipelines.yml",
    "bitbucket-pipelines.yml",
    # instructions to coding agents
    "claude.md", "claude.local.md", "agents.md", "gemini.md", ".cursorrules",
    ".windsurfrules", ".mcp.json",
})
_RUNNABLE_DIRS = frozenset({
    ".github", ".gitlab", ".circleci", ".husky", ".githooks", "hooks", "bin", "scripts",
    ".vscode", ".idea", ".devcontainer", ".cursor", ".cargo", "venv", ".venv",
    "node_modules", "site-packages", "dist-packages",
})
_REQUIREMENTS = re.compile(r"requirements[\w.-]*\.(?:txt|in)")


def _runs_code(path: Path) -> bool:
    name = path.name.lower()
    return (path.suffix.lower() in _RUNNABLE_SUFFIXES or name in _RUNNABLE_NAMES
            or bool(_REQUIREMENTS.fullmatch(name))
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


_UNTRUSTED_NOTE = ("the folder is inside an UNTRUSTED git repository (a bare-repository folder, "
                   "a .git file pointing outside a real repo, or core.bare=true, possibly "
                   "shipped by a cloned repo): its config can make git and git-aware tools "
                   "run commands. Weigh that.")


BYPASS = "bypassPermissions"
ACCEPT_EDITS = "acceptEdits"
_CONTENT_TOOLS = frozenset({"Read", "Grep", "NotebookRead"})
_ROLE_WORDS = {"read": "reads out", "copy": "copies", "send": "sends", "run": "hands a program",
               "write": "writes, moves or deletes", "source": "loads"}


def session_signals(environ: dict[str, str]) -> tuple[str | None, bool | None]:
    """(entrypoint, attended) from the environment Claude Code gives its hooks.

    attended: CLAUDE_CODE_SESSION_ATTENDED when set ("1" yes, "0"/"false" no); without it, a
    child session (CLAUDE_CODE_CHILD_SESSION) counts as unattended; else unknown (None).
    An explicit ATTENDED=1 wins: subagents of an attended session carry CHILD_SESSION=1 too.
    """
    entry = environ.get("CLAUDE_CODE_ENTRYPOINT") or None
    raw = (environ.get("CLAUDE_CODE_SESSION_ATTENDED") or "").strip().lower()
    if raw in ("1", "true", "yes"):
        return entry, True
    if raw in ("0", "false", "no"):
        return entry, False
    child = (environ.get("CLAUDE_CODE_CHILD_SESSION") or "").strip().lower()
    if child in ("1", "true", "yes"):
        return entry, False
    return entry, None


def _hard_ask(kind: protect.Kind | None, tool: str, tool_input: dict[str, Any], cwd: str,
              extra: list[Path] | None = None, mode: str | None = None) -> str | None:
    """Why this call is a hard ask (the person decides; no model, no shortcut), or None.

    Based on what the call DOES, not on what it mentions (engine.gate.ops). In every mode
    but bypassPermissions:
      credential files: reading their contents (Read, Grep, cat, a pipe, a copy) or sending
      one (a program given one, or a write to one, is judged); commands that print a secret (gh auth
      token, printenv TOKEN, a bare env, git config dumps); sourcing a .env and then printing
      the environment. Sourcing a .env for local use is judged.
      the gate's log: writes (reads are judged; secrets are redacted before they are stored).
      protected config (~/.claude, .git, .claude/, .deliberator/, gate.yml, rc files): writes.
    In bypassPermissions ("don't ask me"), only printing or sending a secret, and writes to
    Claude's settings and hooks or to the gate's own install, config and log.
    A mention (grep -v .git/, find -not -path, cd into a worktree, a heredoc body) is judged.
    """
    extra = extra or []
    bypass = mode == BYPASS
    if tool in EDIT_TOOLS:
        raw = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
        if raw and (kind == "gate_log" or protect.is_control(raw, cwd, extra)):
            return "writes the agent's or the gate's own settings, hooks or log: you decide"
        if bypass:
            return None
        if kind == "credential":
            return "writes a credential file: you decide, every time (never judged or reused)"
        if kind == "config":
            return "writes protected config (agent, git or gate settings): you decide"
        return None
    if tool in _CONTENT_TOOLS:
        if kind == "credential":
            return "reads a credential file: you decide, every time (never judged or reused)"
        return None
    if tool != "Bash":
        return None  # Glob, LS: names only
    command = str(tool_input.get("command", ""))
    parsed = ops.parse(command, cwd)
    if parsed.opaque:
        # Not parseable: fall back to mentions for credentials (outside bypass).
        if not bypass and not protect._ansi_c(protect.strip_heredocs(command)) \
                and protect.command_kind(command, extra, cwd) == "credential":
            return ("a command the gate cannot parse names a credential file: you decide, "
                    "every time")
        return None
    if parsed.prints_secret:
        return (f"prints a secret ({parsed.prints_secret[0]}): you decide, every time "
                "(never judged or reused)")
    loads_secrets = False
    for op in parsed.ops:
        k = protect.word_kind(op.word, op.cwd, extra)
        if k is None or k == "notes":
            continue
        if op.role == "write" and (k == "gate_log" or protect.is_control(op.word, op.cwd, extra)):
            return "writes the agent's or the gate's own settings, hooks or log: you decide"
        if k == "credential":
            if op.role == "source":
                loads_secrets = True
                continue
            if op.role in ("read", "send") or (not bypass and op.role == "copy"):
                return (f"{_ROLE_WORDS[op.role]} a credential file ({redact(op.word)}): you "
                        "decide, every time (never judged or reused)")
        elif k == "config" and op.role == "write" and not bypass:
            return f"writes protected config ({redact(op.word)}): you decide"
    if loads_secrets and parsed.prints_env:
        return "loads a credential file and prints the environment: you decide, every time"
    if parsed.git_config_writes and not bypass:
        if "credential" in parsed.git_config_writes:
            return "writes global or system git config (credential helpers live there): you decide"
        return "writes git config (it can make git run commands): you decide"
    if parsed.git_setup and not bypass:
        return (f"changes what git fetches and runs ({parsed.git_setup[0]}): you decide")
    return None


# ---------------------------------------------------------------------------------------------
# The delete floor: deterministic, in every mode (bypassPermissions included).
# ---------------------------------------------------------------------------------------------

def _catastrophic() -> list[str]:
    h = str(Path.home())
    return [os.path.normpath(p) for p in (
        "/", "/System", "/Library", "/usr", "/bin", "/sbin", "/etc", "/var", "/private",
        "/Applications", "/Users", "/opt", "/Volumes", h, f"{h}/code", f"{h}/Library",
        f"{h}/Documents", f"{h}/Desktop", f"{h}/.ssh", f"{h}/.claude")]


# Build and cache folders: anything inside one (or the folder itself) is the agent's to delete.
_BUILD_DIRS = frozenset({"node_modules", ".venv", "venv", "target", "dist", "build",
                         "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".next",
                         ".turbo", ".parcel-cache", ".tox", ".nox", ".gradle", ".svelte-kit",
                         "coverage", ".coverage", "htmlcov", ".eggs", ".astro", ".vite",
                         ".angular", ".nuxt", ".output"})
_UNRESOLVED = re.compile(r"\$|[*?\[{]")


def _fold(p: str) -> str:
    return p.casefold().rstrip("/") or "/"


def _agent_space(path: str, session_cwd: str) -> bool:
    """The session's repo or worktree (not its root), ~/code/scratch/*, /tmp/*, the session
    scratchpad, and build or cache folders."""
    parts = Path(path).parts
    if _BUILD_DIRS & set(parts) or ".cache" in parts[:-1] or ".scratch" in parts[:-1]:
        return True
    home = str(Path.home())
    roots = [f"{home}/code/scratch", "/tmp", "/private/tmp"]
    if session_cwd:
        base = Path(session_cwd).expanduser()
        repo = ledger.git_root(str(base))
        if repo is not None and not _not_a_project(repo.resolve()):
            roots += [str(repo), str(repo.resolve())]
    fp = _fold(path)
    return any(fp.startswith(_fold(r) + "/") for r in roots)


def _could_be(word: str, target: str) -> bool:
    """Could `word` (absolute, with unresolved $VAR or glob parts) name `target`?"""
    w = [p for p in word.split("/") if p]
    t = [p.casefold() for p in target.split("/") if p]
    dollar = [i for i, p in enumerate(w) if "$" in p]
    if not dollar:  # globs match one component each
        return len(w) == len(t) and all(fnmatch.fnmatchcase(b, a.casefold())
                                        for a, b in zip(w, t, strict=True))
    first, last = dollar[0], dollar[-1]
    head, tail = w[:first], w[last + 1:]
    if ".." in tail:
        tail = []
    if len(t) < len(head) + len(tail):
        return False
    ok_head = all(fnmatch.fnmatchcase(b, a.casefold()) for a, b in zip(head, t, strict=False))
    ok_tail = all(fnmatch.fnmatchcase(b, a.casefold())
                  for a, b in zip(reversed(tail), reversed(t), strict=False))
    return ok_head and ok_tail


def _floor(tool: str, tool_input: dict[str, Any], cwd: str) -> tuple[str, str] | None:
    """(verdict, reason) for mass or catastrophic deletes, in every mode, or None.

    deny: a recursive delete of /, /System, /Library, /usr, /bin, /etc, /private,
    /Applications, /Users, ~, ~/code, ~/Library, ~/Documents, ~/Desktop, ~/.ssh or ~/.claude
    (or a target with $VAR, a glob or `..` that could be one of them); sudo rm; diskutil
    erase*; mkfs; dd to a disk device.
    ask: any other recursive delete outside the agent's space (see _agent_space).
    """
    if tool != "Bash":
        return None
    parsed = ops.parse(str(tool_input.get("command", "")), cwd)
    if parsed.wipes:
        return "deny", f"wipes the machine or a disk ({parsed.wipes[0]}): never allowed here"
    cat = _catastrophic()
    ask: str | None = None
    for d in parsed.deletes:
        word = os.path.expandvars(os.path.expanduser(d.word))
        base = os.path.expandvars(d.cwd)
        if "$" in base:
            word = f"$CWD/{word}" if not word.startswith("/") else word
        elif not word.startswith("/") and not word.startswith("$"):
            word = os.path.join(base, word)
        shown = redact(d.word)
        if _UNRESOLVED.search(word):
            comps = word.split("/")
            k = next(i for i, c in enumerate(comps) if _UNRESOLVED.search(c))
            static = "/".join(comps[:k])
            fixed = static.startswith("/") and ".." not in comps[k:]
            hits = [c for c in cat if _could_be(word, c)]
            if hits and not d.filtered:
                return "deny", (f"recursive delete of {shown}, which could resolve to {hits[0]}:"
                                " never allowed here")
            build = bool(_BUILD_DIRS & set(comps[k + 1:]))
            if not build and not (fixed and _agent_space(os.path.normpath(static) + "/x", cwd)):
                ask = ask or f"recursive delete outside the agent's space ({shown}): you decide"
            continue
        paths = {os.path.normpath(word)}
        try:
            paths.add(os.path.realpath(word))
        except (OSError, ValueError):
            pass
        folded = {_fold(c) for c in cat}
        if any(_fold(p) in folded for p in paths):
            if d.filtered:
                ask = ask or f"deletes matching files across {shown}: you decide"
                continue
            return "deny", f"recursive delete of {shown}: never allowed here"
        if not all(_agent_space(p + "/x" if d.filtered else p, cwd) for p in paths):
            ask = ask or f"recursive delete outside the agent's space ({shown}): you decide"
    return ("ask", ask) if ask else None


def _scratch(path: Path) -> bool:
    """Persistent scratch (~/code/scratch) or an agent session scratchpad."""
    s = str(path)
    home = Path.home().resolve()
    return (path.is_relative_to(home / "code" / "scratch") or ".scratch" in path.parts[:-1]
            or re.match(r"^/(?:private/)?tmp/claude-\d+/", s) is not None)


def _edit_in_trusted(tool: str, tool_input: dict[str, Any], cwd: str, *,
                     scratch: bool = False) -> bool:
    """An edit to a file inside the trusted git repository that holds `cwd` (or, with
    `scratch`, in a scratch folder). No content checks: acceptEdits and bypassPermissions
    let edits through."""
    if tool not in EDIT_TOOLS or not cwd:
        return False
    raw = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not raw or not isinstance(raw, str):
        return False
    base = Path(cwd).expanduser().resolve()
    path = Path(raw).expanduser()
    path = (path if path.is_absolute() else base / path).resolve()
    if scratch and _scratch(path):
        return True
    if _not_a_project(base) or repo_state(str(base)) != "trusted":
        return False
    repo = ledger.git_root(str(base))
    if repo is None or _not_a_project(repo.resolve()):
        return False
    return path.is_relative_to(repo.resolve())


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
    permission_mode: str | None = None,
    entrypoint: str | None = None,
    attended: bool | None = None,
) -> Decision:
    """Rule on one tool call and log the decision.

    Order: allow-list or edit inside the repo (no model call) → a standing grant → identical
    earlier call (same command or path AND same content: reuse, or allowed because the
    person approved it) → the judge, shown the call's content and the closest precedents.
    Calls touching protected paths, and calls too long to show whole, skip the shortcuts and
    always go to the judge.

    `permission_mode` is Claude Code's mode. In bypassPermissions few calls are hard asks
    (see _hard_ask), the judge is told to ask only for irreversible harm, an ask that names no
    such harm is allowed, and a truncated edit in a trusted repo or scratch stays allowed.
    In acceptEdits and bypassPermissions an edit inside the trusted repo is allowed outright.

    `attended` False (an unattended or child session, see session_signals): nobody can answer
    an ask, so the call is ruled as in bypassPermissions and then every ask becomes a ruling:
    the floor and the remaining hard asks (secret exfil, control writes, mass deletes outside
    the agent's space) are denied, the judge's asks are allowed.
    """
    mode = permission_mode or None
    unattended = attended is False
    bypass = mode == BYPASS or unattended
    view = ledger.view_of(tool, tool_input)
    raw_subject = view.subject
    subject = redact(raw_subject)
    rules_hash = config.rules_hash()
    key = ledger.call_key(tool, raw_subject, cwd, rules_hash, view.digest)
    shown, cut = clip(redact(view.text))
    truncated = cut > 0
    extra = [config.store_root(root) / ledger.LOG_PATH.parent] if config.log_dir else []
    kind = protect.access_kind(tool, tool_input, cwd, extra)
    command = str(tool_input.get("command", "")) if tool == "Bash" else ""
    # The cwd, or a folder the command sends git to (cd, -C, --git-dir, --work-tree).
    untrusted = (untrusted_target(command, cwd) if tool == "Bash"
                 else repo_state(cwd) == "untrusted")
    untrusted_git = untrusted and tool == "Bash" and runs_git(command)
    var_command = tool == "Bash" and ops.parse(command, cwd).var_command
    protected = kind is not None or untrusted_git or var_command
    project = ledger.project_of(cwd)
    history = ledger.read(root)
    base: dict[str, Any] = {
        "id": ledger.new_id(key), "at": ledger.now(), "session": session,
        "tool_use_id": tool_use_id, "tool": tool, "subject": subject, "cwd": cwd, "key": key,
        "rules_hash": rules_hash, "project": project, "truncated": truncated,
        "protected": protected, "mode": mode, "entrypoint": entrypoint, "attended": attended,
    }
    shortcuts = not protected and not truncated

    decision: Decision | None = None
    floor = _floor(tool, tool_input, cwd)
    if floor is not None:
        verdict = "deny" if unattended else floor[0]
        reason = floor[1] + (" (unattended session: nobody can answer, so denied)"
                             if unattended and floor[0] == "ask" else "")
        decision = Decision(**{**base, "protected": True}, verdict=verdict, source="protected",
                            reason=reason)
    hard = None if decision is not None else _hard_ask(kind, tool, tool_input, cwd, extra,
                                                      BYPASS if bypass else mode)
    if not hard and untrusted_git and not bypass:
        hard = ("git in a repository that is not an ordinary checkout (a bare-repository "
                "folder, a foreign .git file or core.bare): its config can run commands. "
                "You decide.")
    if hard:
        if unattended:
            decision = Decision(**base, verdict="deny", source="protected",
                                reason=f"{hard} (unattended session: nobody can answer, so "
                                       "denied)")
        else:
            decision = Decision(**base, verdict="ask", source="protected", reason=hard)
    if decision is None and not protected and config.allow_edits_in_project \
            and _edit_inside(tool, tool_input, cwd):
        decision = Decision(**base, verdict="allow", source="skip",
                            reason="an edit to a file inside the working repository")
    if decision is None and not protected and (mode == ACCEPT_EDITS or bypass) \
            and _edit_in_trusted(tool, tool_input, cwd):
        decision = Decision(**base, verdict="allow", source="skip",
                            reason=f"an edit inside the trusted repository ({mode})")
    # Bash: the allow-list skips the judge only for one plain command whose every flag is on
    # that command's safe list (engine.gate.simple); anything else is judged, not asked.
    # The regex sees the words joined, so it matches the real argv[0] (not `ls=x env ...`).
    if tool == "Bash":
        words = None if ledger.compound(raw_subject) else simple_words(raw_subject, cwd, extra=extra)
        matched = " ".join(words) if words is not None else None
    else:
        matched = raw_subject
    for pattern in config.allow_without_asking if decision is None and matched is not None \
            and shortcuts else ():
        try:
            if re.search(pattern, matched):
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
        notes = [n for n in (_UNTRUSTED_NOTE if untrusted else None,
                             BYPASS_NOTE if bypass else None) if n]
        note = "\nNOTE: ".join(notes) or None
        prompt = build_prompt(config, tool=tool, subject=subject, cwd=cwd,
                              precedents=precedents, history=history, text=shown,
                              truncated=cut, note=note)
        ruling = await rule_on(prompt, judge or make_judge(config), subject,
                               timeout_s=config.timeout_s)
        failed = ruling.reason.startswith("gate could not rule")
        verdict, reason = ruling.verdict, ruling.reason
        if bypass and verdict == "ask" and not failed and ruling.harm is None:
            verdict = "allow"
            reason = f"bypassPermissions, and no irreversible harm named: {reason}"
        if truncated and verdict == "allow" and bypass and not untrusted \
                and _edit_in_trusted(tool, tool_input, cwd, scratch=True) \
                and not _risky_content(_written_text(tool, tool_input)):
            pass  # the whole file goes into a trusted repo or scratch, with nothing risky in it
        elif truncated and verdict == "allow" and not unattended:
            # The judge saw head and tail only: what it allowed may not be what runs.
            verdict = "ask"
            reason = f"truncated call (the judge saw only its head and tail): {reason}"
        if unattended and verdict == "ask" and not failed:
            verdict = "allow"
            reason = f"unattended session (nobody can answer an ask): {reason}"
        decision = Decision(
            **base, verdict=verdict, reason=redact(reason), rule=ruling.rule,
            source="error" if failed else "model", model=config.resolved_model(),
            precedents=tuple(p.id for p in precedents), latency_ms=ruling.latency_ms,
            input_tokens=ruling.input_tokens, output_tokens=ruling.output_tokens,
            grant=ruling.grant if shortcuts and verdict == "ask" else None,
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


def hook_output(decision: Decision, config: GateConfig,
                tool_input: dict[str, Any] | None = None) -> dict[str, Any]:
    """Claude Code PreToolUse output. The reason is shown to Claude on deny, to you on ask.

    A git call the fast path allowed is rewritten (updatedInput, which replaces the whole
    input) so repo config cannot run anything: `git -c core.fsmonitor=false -c
    core.hooksPath=/dev/null <sub>`, plus --no-ext-diff --no-textconv for diff/log/show."""
    rule = ""
    if decision.rule and 1 <= decision.rule <= len(config.rules):
        rule = f" (rule {decision.rule}: {config.rules[decision.rule - 1]})"
    grant = ""
    if decision.verdict == "ask" and decision.grant:
        grant = f" Yes is kept forever for calls matching {decision.grant}"
    out: dict[str, Any] = {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision.verdict,
        "permissionDecisionReason": f"[deliberator gate] {decision.reason}{rule}{grant}",
    }
    rewritten = _safe_git_input(decision, tool_input)
    if rewritten is not None:
        out["updatedInput"] = rewritten
    return {"hookSpecificOutput": out}


def _safe_git_input(decision: Decision, tool_input: dict[str, Any] | None
                    ) -> dict[str, Any] | None:
    if (tool_input is None or decision.tool != "Bash" or decision.source != "skip"
            or decision.verdict != "allow"):
        return None
    command = tool_input.get("command")
    if not isinstance(command, str):
        return None
    try:
        words = shlex.split(command)
    except ValueError:
        return None
    if len(words) < 2 or words[0] != "git":
        return None
    return {**tool_input, "command": safe_git(words)}


def write_graph_json(root: Path, config: GateConfig) -> Path:
    from engine.gate.graph import node_link

    path = root / GRAPH_JSON
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(node_link(ledger.read(root), config), indent=1)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(fd, 0o600)  # an existing file keeps its old mode otherwise
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(data)
    return path
