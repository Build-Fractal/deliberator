"""Protected paths: calls that touch them always go to the judge.

A call touching the agent's own config (``~/.claude``, any ``.claude/`` or ``.deliberator/``
folder), the gate's log and config, shell rc files, ``~/.ssh``, ``~/.aws`` or ``.git``
internals is never allowed without a model call: no allow-list, no edits-in-project skip, no
reuse of an earlier ruling, no standing grant. The judge may still allow it, informed.

Credentials are protected the same way, for reads too: ``~/.netrc``, ``~/.npmrc``,
``~/.pypirc``, ``~/.git-credentials``, ``.env`` files, ``~/.config/gh``, ``~/.docker/config.json``,
keychains and ``security find-*-password``.

Names are compared case-insensitively (APFS: ``~/.CLAUDE`` is ``~/.claude``), and where a path
exists its folders are compared by inode with the protected ones. Glob and brace forms of a
protected name (``~/.cla*/``, ``~/.{claude,x}``) count as the name.

Exempt: git worktrees kept at ``<repo>/.claude/worktrees/<name>/`` (ordinary work, not
Claude config). Inside a worktree, its own ``.claude/``, ``.deliberator/`` and ``.git`` are
protected again. Everything under ``~/.claude/`` stays protected.
"""

from __future__ import annotations

import fnmatch
import os
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

PROTECTED_COMPONENTS = frozenset({".claude", ".deliberator", ".git"})
RC_FILES = frozenset({".zshrc", ".zprofile", ".zshenv", ".zlogin", ".bashrc", ".bash_profile",
                      ".bash_login", ".profile"})
# Files that hold credentials wherever they are: reading them is judged too.
CREDENTIAL_NAMES = frozenset({".netrc", ".npmrc", ".pypirc", ".git-credentials", ".pgpass"})
_ENV_FILE = re.compile(r"\.env(?:\.[\w.-]+)?")  # .env, .env.local (not .envrc)
_KEYCHAIN_SUFFIXES = (".keychain", ".keychain-db")
EDIT_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})


def _home() -> Path:
    return Path(os.path.expanduser("~"))


def protected_dirs(extra: Iterable[str | Path] = ()) -> list[Path]:
    """Protected folders (and single files), everything under them included."""
    home = _home()
    dirs = [home / ".claude", home / ".local" / "share" / "deliberator",
            home / ".config" / "deliberator", home / ".ssh", home / ".aws",
            home / ".config" / "gh", home / ".docker" / "config.json", home / ".gnupg",
            home / "Library" / "Keychains", home / ".kube" / "config",
            home / ".config" / "gcloud"]
    dirs += [Path(os.path.expanduser(str(p))) for p in extra]
    return dirs


def _resolved(p: Path) -> Path:
    return p.resolve()


def _norm(raw: str, cwd: str) -> list[Path]:
    """The path as written (made absolute, `..` folded) and with symlinks resolved."""
    expanded = os.path.expandvars(os.path.expanduser(raw))
    p = Path(expanded)
    if not p.is_absolute():
        p = Path(cwd or ".") / p
    out = [Path(os.path.normpath(p))]
    try:
        out.append(_resolved(p))
    except (OSError, RuntimeError):
        pass
    return out


def _fold(p: Path | str) -> str:
    # macOS (APFS, HFS+) and Windows file systems are case-insensitive: ~/.CLAUDE is ~/.claude.
    return str(p).casefold()


def _after_worktree(parts: tuple[str, ...]) -> tuple[str, ...]:
    """Parts after the last `.claude/worktrees/<name>` segment (the worktree's own files).
    `parts` are case-folded and `..`-free (normpath)."""
    for i in range(len(parts) - 3, -1, -1):
        if parts[i] == ".claude" and parts[i + 1] == "worktrees":
            return parts[i + 3:]
    return parts


def _inodes(dirs: Iterable[Path]) -> set[tuple[int, int]]:
    out = set()
    for d in dirs:
        try:
            st = os.stat(d)
        except OSError:
            continue
        out.add((st.st_dev, st.st_ino))
    return out


def _same_file_as(p: Path, inodes: set[tuple[int, int]]) -> bool:
    """`p`, or a folder above it that exists, is one of `inodes` (another name for a protected
    folder: different case, a firmlink such as /System/Volumes/Data, a bind mount)."""
    if not inodes:
        return False
    for q in (p, *p.parents):
        try:
            st = os.stat(q)
        except OSError:
            continue
        if (st.st_dev, st.st_ino) in inodes:
            return True
    return False


def _sensitive_name(name: str) -> bool:
    """A case-folded file name that is protected wherever it lives."""
    return (name in RC_FILES or name in CREDENTIAL_NAMES or name in PROTECTED_COMPONENTS
            or bool(_ENV_FILE.fullmatch(name)) or name.endswith(_KEYCHAIN_SUFFIXES))


def path_is_protected(raw: str, cwd: str = "", extra: Iterable[str | Path] = ()) -> bool:
    dirs = protected_dirs(extra)
    folded_dirs = [_fold(d).rstrip("/") for d in dirs]
    for p in _norm(raw, cwd):
        fp = _fold(p)
        if any(fp == d or fp.startswith(d + "/") for d in folded_dirs):
            return True
        parts = tuple(x.casefold() for x in p.parts)
        if _sensitive_name(parts[-1]):
            return True  # an rc or credential file, or a .claude / .deliberator / .git itself
        if PROTECTED_COMPONENTS & set(_after_worktree(parts)[:-1]):
            return True  # inside a .claude / .deliberator / .git folder
    return any(_same_file_as(p, _inodes(dirs)) for p in _norm(raw, cwd))


# Bash: any mention of a protected location in the command text (any case: APFS).
_B = r"(?:^|(?<=[\s/~'\"=:(<>{}$`,]))"
_BASH_PROTECTED = re.compile(
    _B + r"\.(?:claude|deliberator)(?![\w-])"
    r"|\.config/deliberator\b|\.local/share/deliberator\b"
    + r"|" + _B + r"\.(?:ssh|aws|gnupg)(?![\w-])"
    + r"|" + _B + r"\.(?:zshrc|zprofile|zshenv|zlogin|bashrc|bash_profile|bash_login|profile)\b"
    + r"|" + _B + r"\.git(?:/|\s*$|(?=[\s'\";|&),}]))"
    # credentials: read only with the judge's say-so
    + r"|" + _B + r"\.(?:netrc|npmrc|pypirc|git-credentials|pgpass)(?![\w-])"
    + r"|" + _B + r"\.env(?:\.[\w.-]+)?(?![\w-])"
    + r"|\.config/(?:gh|gcloud)\b|\.docker/config\.json|\.kube/config\b|Library/Keychains\b"
    + r"|\.keychain(?:-db)?\b"
    + r"|(?:^|[\s;&|(`])security\s+(?:find|dump|export)-",
    re.IGNORECASE,
)
# `<repo>/.claude/worktrees/<name>` (but not under ~/.claude) is ordinary work.
_WORKTREE = re.compile(r"\.claude/worktrees/([^/\s'\"]+)", re.IGNORECASE)
_HOME_PREFIXES = ("~/", "$HOME/", "${HOME}/")
_DOTDOT = re.compile(r"(?:^|/)\.\.(?:/|$)")


def _strip_worktrees(text: str) -> str:
    home = str(_home()) + "/"

    def sub(m: re.Match[str]) -> str:
        before = text[:m.start()].casefold()
        if any(before.endswith(h.casefold()) for h in (*_HOME_PREFIXES, home)):
            return m.group(0)
        rest = re.match(r"[^\s'\"]*", text[m.end():])
        if m.group(1) in (".", "..") or _DOTDOT.search(rest.group(0) if rest else ""):
            return m.group(0)  # `..` climbs out of the worktree: judge it as written
        return "WORKTREE"

    return _WORKTREE.sub(sub, text)


# Glob and brace forms of protected names: ~/.cla*/, ~/.c?aude, ~/.[c]laude, ~/.{claude,x}.
_GLOB_NAMES = (PROTECTED_COMPONENTS | RC_FILES | CREDENTIAL_NAMES
               | {".ssh", ".aws", ".gnupg", ".env", ".docker", ".config", ".local", ".kube"})
_SEGMENT = re.compile(r"[^\s/'\"=:;|&()<>]+")
_BRACE = re.compile(r"\{([^{}]*,[^{}]*)\}")


def _braces(seg: str, limit: int = 64) -> list[str]:
    out, todo = [], [seg]
    while todo and len(out) + len(todo) < limit:
        s = todo.pop()
        m = _BRACE.search(s)
        if not m:
            out.append(s)
            continue
        todo += [s[:m.start()] + alt + s[m.end():] for alt in m.group(1).split(",")]
    return out + todo


def _glob_hits(text: str) -> bool:
    for seg in _SEGMENT.findall(text):
        if not any(c in seg for c in "*?[{"):
            continue
        for alt in _braces(seg):
            alt = alt.casefold()
            # a glob matches a leading dot only when the pattern starts with one
            if alt.startswith(".") and any(fnmatch.fnmatchcase(n, alt) for n in _GLOB_NAMES):
                return True
    return False


def command_is_protected(command: str, extra: Iterable[str | Path] = ()) -> bool:
    variants = {command, re.sub(r"[\"'\\]", "", command)}
    home = str(_home())
    for text in variants:
        text = _strip_worktrees(text)
        if _BASH_PROTECTED.search(text) or _glob_hits(text):
            return True
        folded = text.casefold()
        for d in extra:
            ds = os.path.expanduser(str(d))
            short = ds.replace(home, "~", 1) if ds.startswith(home) else ds
            if ds.casefold() in folded or short.casefold() in folded:
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
