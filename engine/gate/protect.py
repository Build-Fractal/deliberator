"""Protected paths: calls that touch them always go to the judge.

A call touching the agent's own config (``~/.claude``, any ``.claude/`` or ``.deliberator/``
folder), the gate's log and config, shell rc files, ``~/.ssh``, ``~/.aws`` or ``.git``
internals is never allowed without a model call: no allow-list, no edits-in-project skip, no
reuse of an earlier ruling, no standing grant. The judge may still allow it, informed.

Exempt: git worktrees kept at ``<repo>/.claude/worktrees/<name>/`` (ordinary work, not
Claude config). Inside a worktree, its own ``.claude/``, ``.deliberator/`` and ``.git`` are
protected again. Everything under ``~/.claude/`` stays protected.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

PROTECTED_COMPONENTS = frozenset({".claude", ".deliberator", ".git"})
RC_FILES = frozenset({".zshrc", ".zprofile", ".zshenv", ".zlogin", ".bashrc", ".bash_profile",
                      ".bash_login", ".profile"})
EDIT_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})


def _home() -> Path:
    return Path(os.path.expanduser("~"))


def protected_dirs(extra: Iterable[str | Path] = ()) -> list[Path]:
    home = _home()
    dirs = [home / ".claude", home / ".local" / "share" / "deliberator",
            home / ".config" / "deliberator", home / ".ssh", home / ".aws"]
    dirs += [Path(os.path.expanduser(str(p))) for p in extra]
    return dirs


def _norm(raw: str, cwd: str) -> list[Path]:
    """The path as written (made absolute, `..` folded) and with symlinks resolved."""
    expanded = os.path.expandvars(os.path.expanduser(raw))
    p = Path(expanded)
    if not p.is_absolute():
        p = Path(cwd or ".") / p
    out = [Path(os.path.normpath(p))]
    try:
        out.append(p.resolve())
    except (OSError, RuntimeError):
        pass
    return out


def _after_worktree(parts: tuple[str, ...]) -> tuple[str, ...]:
    """Parts after the last `.claude/worktrees/<name>` segment (the worktree's own files)."""
    for i in range(len(parts) - 3, -1, -1):
        if parts[i] == ".claude" and parts[i + 1] == "worktrees":
            return parts[i + 3:]
    return parts


def path_is_protected(raw: str, cwd: str = "", extra: Iterable[str | Path] = ()) -> bool:
    dirs = protected_dirs(extra)
    for p in _norm(raw, cwd):
        for d in dirs:
            if p == d or d in p.parents:
                return True
        if p.name in RC_FILES:
            return True
        if PROTECTED_COMPONENTS & set(_after_worktree(p.parts)[:-1]):
            return True  # inside a .claude / .deliberator / .git folder
        if p.name in PROTECTED_COMPONENTS:
            return True  # the folder itself, or a worktree's .git file
    return False


# Bash: any mention of a protected location in the command text.
_B = r"(?:^|(?<=[\s/~'\"=:(<>{}$`]))"
_BASH_PROTECTED = re.compile(
    _B + r"\.(?:claude|deliberator)(?![\w-])"
    r"|\.config/deliberator\b|\.local/share/deliberator\b"
    + r"|" + _B + r"\.(?:ssh|aws)(?![\w-])"
    + r"|" + _B + r"\.(?:zshrc|zprofile|zshenv|zlogin|bashrc|bash_profile|bash_login|profile)\b"
    + r"|" + _B + r"\.git(?:/|\s*$|(?=[\s'\";|&)]))",
)
# `<repo>/.claude/worktrees/<name>` (but not under ~/.claude) is ordinary work.
_WORKTREE = re.compile(r"\.claude/worktrees/[^/\s'\"]+")
_HOME_PREFIXES = ("~/", "$HOME/", "${HOME}/")


def _strip_worktrees(text: str) -> str:
    home = str(_home()) + "/"

    def sub(m: re.Match[str]) -> str:
        before = text[:m.start()]
        if any(before.endswith(h) for h in (*_HOME_PREFIXES, home)):
            return m.group(0)
        return "WORKTREE"

    return _WORKTREE.sub(sub, text)


def command_is_protected(command: str, extra: Iterable[str | Path] = ()) -> bool:
    variants = {command, re.sub(r"[\"'\\]", "", command)}
    home = str(_home())
    for text in variants:
        text = _strip_worktrees(text)
        if _BASH_PROTECTED.search(text):
            return True
        for d in extra:
            ds = os.path.expanduser(str(d))
            short = ds.replace(home, "~", 1) if ds.startswith(home) else ds
            if ds in text or short in text:
                return True
    return False


def touches_protected(tool: str, tool_input: dict[str, Any], cwd: str = "",
                      extra: Iterable[str | Path] = ()) -> bool:
    """Whether a call reads or writes a protected location."""
    extra = list(extra)
    if tool == "Bash":
        return command_is_protected(str(tool_input.get("command", "")), extra)
    for key in ("file_path", "notebook_path", "path"):
        raw = tool_input.get(key)
        if isinstance(raw, str) and raw and path_is_protected(raw, cwd, extra):
            return True
    return False
