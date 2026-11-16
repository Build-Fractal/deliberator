"""Protected paths, in three kinds, and what the gate does with each.

``credential``: files that hold secrets. ANY access (Read, Grep, Bash, an edit) is a hard
ask: no model call, no allow-list, no reuse, no standing grant. The person decides every time.
  ``~/.ssh``, ``~/.aws``, ``~/.gnupg``, ``~/.azure``, ``~/.config/{gh,hub,git,op,gcloud}``,
  ``~/.docker/config.json``, ``~/.kube/config``, ``~/Library/Keychains``,
  ``~/.cargo/credentials.toml``, ``~/.vault-token``, ``~/.yarnrc.yml``,
  ``~/.terraform.d/credentials.tfrc.json``, ``~/.cache/huggingface/token``,
  ``~/.codex/auth.json``, ``~/.m2/settings.xml``, ``~/.gem/credentials``; and these names
  anywhere: ``.netrc``, ``.npmrc``, ``.pypirc``, ``.git-credentials``, ``.pgpass``,
  ``.gitconfig``, ``.env``/``.env.*``, ``.envrc``, ``credentials*``, ``*_history``,
  ``*.keychain(-db)``; and ``security find-/dump-/export-`` commands.

``gate_log``: the gate's own record (``~/.local/share/deliberator``, any
``.deliberator/gate/``, and a configured ``log_dir``). Reads and writes are a hard ask too:
redaction can miss a secret.

``config``: what steers the agent or the gate: ``~/.claude``, any ``.claude/``,
``.deliberator/`` or ``.git`` folder, ``~/.config/deliberator`` (gate.yml), shell rc files.
Reads go to the judge (never a shortcut); writes are a hard ask, except the agent's own
memory notes (``~/.claude/projects/*/memory/``), which the judge rules on.

Names are compared case-insensitively (APFS: ``~/.CLAUDE`` is ``~/.claude``), and where a path
exists its folders are compared by inode with the protected ones. Glob and brace forms of a
protected name (``~/.cla*/``, ``~/.{claude,x}``) count as the name.

Exempt from ``config``: git worktrees kept at ``<repo>/.claude/worktrees/<name>/`` (ordinary
work). Inside a worktree, its own ``.claude/``, ``.deliberator/`` and ``.git`` are protected
again. Everything under ``~/.claude/`` stays protected.
"""

from __future__ import annotations

import fnmatch
import os
import re
import shlex
from collections.abc import Iterable
from functools import lru_cache
from itertools import pairwise
from pathlib import Path
from typing import Any, Literal

Kind = Literal["credential", "gate_log", "config"]
_RANK: dict[str | None, int] = {None: 0, "config": 1, "gate_log": 2, "credential": 3}

PROTECTED_COMPONENTS = frozenset({".claude", ".deliberator", ".git"})
RC_FILES = frozenset({".zshrc", ".zprofile", ".zshenv", ".zlogin", ".bashrc", ".bash_profile",
                      ".bash_login", ".profile"})
# Credential file names, wherever they are.
CREDENTIAL_NAMES = frozenset({".netrc", ".npmrc", ".pypirc", ".git-credentials", ".pgpass",
                              ".gitconfig", ".envrc", ".vault-token"})
_CREDENTIAL_NAME = re.compile(r"\.env(?:\.[\w.-]+)?|credentials.*|.*_history")
_KEYCHAIN_SUFFIXES = (".keychain", ".keychain-db")
EDIT_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})
READ_TOOLS = frozenset({"Read", "Grep", "Glob", "LS", "NotebookRead"})


def _home() -> Path:
    return Path(os.path.expanduser("~"))


def credential_dirs() -> list[Path]:
    h = _home()
    return [h / ".ssh", h / ".aws", h / ".gnupg", h / ".azure", h / ".config" / "gh",
            h / ".config" / "hub", h / ".config" / "git", h / ".config" / "op",
            h / ".config" / "gcloud", h / ".docker" / "config.json", h / ".kube" / "config",
            h / "Library" / "Keychains", h / ".cargo" / "credentials.toml",
            h / ".vault-token", h / ".yarnrc.yml", h / ".terraform.d" / "credentials.tfrc.json",
            h / ".cache" / "huggingface" / "token", h / ".codex" / "auth.json",
            h / ".m2" / "settings.xml", h / ".gem" / "credentials"]


def gate_log_dirs(extra: Iterable[str | Path] = ()) -> list[Path]:
    return [_home() / ".local" / "share" / "deliberator",
            *(Path(os.path.expanduser(str(p))) for p in extra)]


def config_dirs() -> list[Path]:
    return [_home() / ".claude", _home() / ".config" / "deliberator"]


def protected_dirs(extra: Iterable[str | Path] = ()) -> list[Path]:
    """Every protected folder (and single file), everything under them included."""
    return [*config_dirs(), *gate_log_dirs(extra), *credential_dirs()]


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


def _under(fp: str, dirs: Iterable[Path]) -> bool:
    for d in dirs:
        fd = _fold(d).rstrip("/")
        if fp == fd or fp.startswith(fd + "/"):
            return True
    return False


def _credential_name(name: str) -> bool:
    return (name in CREDENTIAL_NAMES or bool(_CREDENTIAL_NAME.fullmatch(name))
            or name.endswith(_KEYCHAIN_SUFFIXES))


def path_kind(raw: str, cwd: str = "", extra: Iterable[str | Path] = ()) -> Kind | None:
    """Which kind of protected path `raw` is (the most sensitive that applies), or None."""
    extra = list(extra)
    paths = _norm(raw, cwd)
    best: Kind | None = None

    def bump(kind: Kind) -> None:
        nonlocal best
        if _RANK[kind] > _RANK[best]:
            best = kind

    for p in paths:
        fp = _fold(p)
        parts = tuple(x.casefold() for x in p.parts)
        if _under(fp, credential_dirs()) or _credential_name(parts[-1]):
            return "credential"
        inner = _after_worktree(parts)
        if (_under(fp, gate_log_dirs(extra))
                or any(a == ".deliberator" and b == "gate" for a, b in pairwise(parts))):
            bump("gate_log")
        if (_under(fp, config_dirs()) or parts[-1] in RC_FILES
                or parts[-1] in PROTECTED_COMPONENTS
                or PROTECTED_COMPONENTS & set(inner[:-1])):
            bump("config")
    if _RANK[best] < _RANK["credential"]:
        inodes = _inode_kinds(tuple(str(e) for e in extra))
        for p in paths:
            k = _walk_kind(p, inodes)
            if k is not None:
                bump(k)
    return best


@lru_cache(maxsize=8)
def _inode_kinds(extra: tuple[str, ...]) -> dict[tuple[int, int], Kind]:
    """(device, inode) of each protected folder that exists -> its kind. One hook call is one
    process, so caching for its lifetime is safe."""
    out: dict[tuple[int, int], Kind] = {}
    for kind, dirs in (("config", config_dirs()), ("gate_log", gate_log_dirs(extra)),
                       ("credential", credential_dirs())):
        for d in dirs:
            try:
                st = os.stat(d)
            except OSError:
                continue
            out[(st.st_dev, st.st_ino)] = kind  # type: ignore[assignment]
    return out


def _walk_kind(p: Path, inodes: dict[tuple[int, int], Kind]) -> Kind | None:
    """The kind of the protected folder `p` (or a folder above it that exists) is another
    name for: different case, a firmlink such as /System/Volumes/Data, a bind mount."""
    best: Kind | None = None
    for q in (*reversed(p.parents), p):  # from / down: stop where the path stops existing
        try:
            st = os.stat(q)
        except OSError:
            break
        k = inodes.get((st.st_dev, st.st_ino))
        if _RANK[k] > _RANK[best]:
            best = k
    return best


def path_is_protected(raw: str, cwd: str = "", extra: Iterable[str | Path] = ()) -> bool:
    return path_kind(raw, cwd, extra) is not None


# Bash: mentions of protected locations in the command text (any case: APFS).
_B = r"(?:^|(?<=[\s/~'\"=:(<>{}$`,]))"
_BASH_CREDENTIAL = re.compile(
    _B + r"\.(?:ssh|aws|gnupg|azure|netrc|npmrc|pypirc|git-credentials|pgpass|gitconfig"
    r"|vault-token|envrc)(?![\w-])"
    + r"|" + _B + r"\.env(?:\.[\w.-]+)?(?![\w-])"
    + r"|\.config/(?:gh|hub|git|op|gcloud)(?![\w-])|\.docker/config\.json|\.kube/config\b"
    + r"|Library/Keychains\b|\.keychain(?:-db)?\b|\.cargo/credentials|\.yarnrc\.yml"
    + r"|\.terraform\.d/credentials|\.cache/huggingface/token|\.codex/auth\.json"
    + r"|\.m2/settings\.xml|\.gem/credentials"
    + r"|(?:" + _B + r"|/)credentials(?:\.[\w.-]+)?(?=$|[\s'\";|&)/]|\.)"
    + r"|(?:" + _B + r"\.|/)[\w.-]*_history(?![\w-])"
    + r"|(?:^|[\s;&|(`])security\s+(?:find|dump|export)-",
    re.IGNORECASE,
)
_BASH_GATE_LOG = re.compile(r"\.local/share/deliberator\b|\.deliberator/gate\b", re.IGNORECASE)
_BASH_CONFIG = re.compile(
    _B + r"\.(?:claude|deliberator)(?![\w-])"
    r"|\.config/deliberator\b"
    + r"|" + _B + r"\.(?:zshrc|zprofile|zshenv|zlogin|bashrc|bash_profile|bash_login|profile)\b"
    + r"|" + _B + r"\.git(?:/|\s*$|(?=[\s'\";|&),}]))",
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


# Glob and brace forms of protected names: ~/.cla*/, ~/.c?aude, ~/.[c]laude, ~/.{claude,x}.
_GLOB_NAMES: dict[str, Kind] = {
    **{n: "config" for n in PROTECTED_COMPONENTS | RC_FILES},
    **{n: "credential" for n in CREDENTIAL_NAMES | {".ssh", ".aws", ".gnupg", ".azure", ".env",
                                                     ".docker", ".config", ".kube", ".cargo",
                                                     ".codex", ".m2", ".gem", ".cache",
                                                     ".terraform.d", ".zsh_history",
                                                     ".bash_history", "credentials"}},
    ".local": "gate_log",
}
_SEGMENT = re.compile(r"[^\s/'\"=:;|&()<>]+")
_BRACE = re.compile(r"\{([^{}]*,[^{}]*)\}")
_TOKEN = re.compile(r"[^\s'\";|&()<>]+")  # linear: no backtracking on long text


def _glob_kind(text: str) -> Kind | None:
    best: Kind | None = None

    def match(pattern: str) -> None:
        nonlocal best
        for name, kind in _GLOB_NAMES.items():
            if _RANK[kind] > _RANK[best] and fnmatch.fnmatchcase(name, pattern):
                best = kind

    for seg in _SEGMENT.findall(text):
        if any(c in seg for c in "*?[{"):
            for alt in _braces(seg):
                if alt.startswith("."):  # a glob matches a leading dot only if it has one
                    match(alt.casefold())
    # With dotglob (bash) or GLOB_DOTS (zsh) on, `*` matches dot names too: a glob that is a
    # whole path component (~/*/settings.json, */config) may be a protected folder.
    for token in _TOKEN.findall(text):
        if "/" in token:
            for comp in token.split("/"):
                if any(c in comp for c in "*?["):
                    for alt in _braces(comp):
                        match(alt.casefold())
    return best


def _squash(text: str) -> str:
    """Path text folded the way normpath folds it: //, /./ and name/../ removed."""
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"/{2,}", "/", text)
        text = re.sub(r"/\.(?=/|\s|$|['\"])", "", text)
        text = re.sub(r"/(?!\.\.(?:/|$))[^/\s'\"]+/\.\.(?=/|\s|$|['\"])", "", text)
    return text


def command_kind(command: str, extra: Iterable[str | Path] = ()) -> Kind | None:
    """The most sensitive protected location the command text mentions."""
    if "$'" in command or '$"' in command:
        return "credential"  # ANSI-C / locale quoting can spell any path, a credential too
    unquoted = re.sub(r"[\"'\\]", "", command)
    variants = {command, unquoted, _squash(command), _squash(unquoted)}
    home = str(_home())
    best: Kind | None = None
    for text in variants:
        text = _strip_worktrees(text)
        if _BASH_CREDENTIAL.search(text):
            return "credential"
        found: list[Kind | None] = [_glob_kind(text)]
        if _BASH_GATE_LOG.search(text):
            found.append("gate_log")
        folded = text.casefold()
        for d in extra:
            ds = os.path.expanduser(str(d))
            short = ds.replace(home, "~", 1) if ds.startswith(home) else ds
            if ds.casefold() in folded or short.casefold() in folded:
                found.append("gate_log")
        if _BASH_CONFIG.search(text):
            found.append("config")
        for k in found:
            if _RANK[k] > _RANK[best]:
                best = k
    return best


def command_is_protected(command: str, extra: Iterable[str | Path] = ()) -> bool:
    return command_kind(command, extra) is not None


_MAX_WORDS = 200
_MAX_PATH = 1024  # PATH_MAX on macOS: a longer word is not a path the call can open


def _words_kind(command: str, cwd: str, extra: list[str | Path]) -> Kind | None:
    """Each word that looks like a path (and each `--flag=path` value), classified the way
    a file_path is: normalised, case-folded, by inode."""
    try:
        words = shlex.split(command, posix=True)
    except ValueError:
        return None  # the text checks still apply
    best: Kind | None = None
    for word in words[:_MAX_WORDS]:
        for part in {word, word.partition("=")[2]}:
            if part and len(part) <= _MAX_PATH and ("/" in part or part.startswith((".", "~"))):
                k = path_kind(part, cwd, extra)
                if _RANK[k] > _RANK[best]:
                    best = k
    return best


def access_kind(tool: str, tool_input: dict[str, Any], cwd: str = "",
                extra: Iterable[str | Path] = ()) -> Kind | None:
    """The most sensitive kind of protected location a call touches, or None."""
    extra = list(extra)
    if tool == "Bash":
        command = str(tool_input.get("command", ""))
        a, b = command_kind(command, extra), None
        if a != "credential":
            b = _words_kind(command, cwd, extra)
        return a if _RANK[a] >= _RANK[b] else b
    best: Kind | None = None
    for key in ("file_path", "notebook_path", "path"):
        raw = tool_input.get(key)
        if isinstance(raw, str) and raw:
            k = path_kind(raw, cwd, extra)
            if _RANK[k] > _RANK[best]:
                best = k
    return best


def touches_protected(tool: str, tool_input: dict[str, Any], cwd: str = "",
                      extra: Iterable[str | Path] = ()) -> bool:
    """Whether a call reads or writes a protected location."""
    return access_kind(tool, tool_input, cwd, extra) is not None


_MEMORY = re.compile(r"/\.claude/projects/[^/]+/memory/[^/]+\.md$", re.IGNORECASE)


def is_agent_memory(tool_input: dict[str, Any], cwd: str = "") -> bool:
    """An edit to the agent's own memory notes (~/.claude/projects/<p>/memory/*.md)."""
    raw = tool_input.get("file_path")
    if not isinstance(raw, str) or not raw:
        return False
    home = _fold(_home())
    return all(_fold(p).startswith(home + "/") and _MEMORY.search(str(p))
               for p in _norm(raw, cwd))
