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

``gate_log``: the gate's own record (any ``.deliberator/gate/`` folder: log.jsonl,
graph.json; and a configured ``log_dir``). Reads and writes are a hard ask too:
redaction can miss a secret.

``config``: what steers the agent or the gate: ``~/.claude``, any ``.claude/``,
``.deliberator/`` or ``.git`` folder, ``~/.config/deliberator`` (gate.yml), shell rc files.
Reads go to the judge (never a shortcut); writes are a hard ask. The installed gate
(``~/.local/share/deliberator`` outside its log) counts as config.

``notes``: the agent's own working files under ``~/.claude`` (``projects/`` with memory
notes and transcripts, ``sessions/``, ``plans/``, ``todos/``). Reads and writes go to the
judge, never a shortcut: writing its memory is ordinary work for the agent.

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

Kind = Literal["credential", "gate_log", "config", "notes"]
_RANK: dict[str | None, int] = {None: 0, "notes": 1, "config": 2, "gate_log": 3, "credential": 4}

PROTECTED_COMPONENTS = frozenset({".claude", ".deliberator", ".git"})
RC_FILES = frozenset({".zshrc", ".zprofile", ".zshenv", ".zlogin", ".bashrc", ".bash_profile",
                      ".bash_login", ".profile"})
# Credential file names, wherever they are.
CREDENTIAL_NAMES = frozenset({".netrc", ".npmrc", ".pypirc", ".git-credentials", ".pgpass",
                              ".gitconfig", ".envrc", ".vault-token"})
_CREDENTIAL_NAME = re.compile(r"\.env(?:\.[\w.-]+)?|credentials.*|.*_history")
# `credentials*` with these extensions is code or docs (credentials_test.py), not a secret.
SOURCE_EXTS = ("py", "pyi", "ipynb", "ts", "tsx", "js", "jsx", "mjs", "cjs", "go", "rs",
               "java", "kt", "kts", "scala", "rb", "php", "cs", "c", "h", "cc", "cpp", "hpp",
               "swift", "m", "dart", "lua", "ex", "exs", "erl", "clj", "sh", "bash", "zsh",
               "md", "mdx", "rst", "adoc", "html", "css", "scss", "vue", "svelte", "snap")
_KEYCHAIN_SUFFIXES = (".keychain", ".keychain-db")
# Files that steer the agent wherever they are (MCP servers run commands).
CONFIG_NAMES = frozenset({".mcp.json", ".claude.json"})
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
    """The log itself (log.jsonl, graph.json): any `.deliberator/gate/` folder is matched by
    name; these are the shared log under ~/.local/share/deliberator and a configured log_dir."""
    return [_home() / ".local" / "share" / "deliberator" / ".deliberator" / "gate",
            *(Path(os.path.expanduser(str(p))) for p in extra)]


def config_dirs() -> list[Path]:
    """The agent's and the gate's settings, and the installed gate (venv, hook script)."""
    return [_home() / ".claude", _home() / ".claude.json", _home() / ".config" / "deliberator",
            _home() / ".local" / "share" / "deliberator"]


def notes_dirs() -> list[Path]:
    """The agent's own working files under ~/.claude: memory notes, transcripts, plans."""
    c = _home() / ".claude"
    return [c / "projects", c / "sessions", c / "plans", c / "todos"]


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
    if name.startswith("credentials") and name.rpartition(".")[2] in SOURCE_EXTS:
        return False  # credentials_test.py, credentials.ts: source, not a secret
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
        notes = _under(fp, notes_dirs())
        if notes:
            bump("notes")
            if _control_in_notes(parts):
                bump("config")  # a .claude/, hooks/ or settings*.json under projects/: config
        if (_under(fp, gate_log_dirs(extra))
                or any(a == ".deliberator" and b == "gate" for a, b in pairwise(parts))):
            bump("gate_log")
        if parts[-1] in CONFIG_NAMES:
            bump("config")
        if not notes and (_under(fp, config_dirs()) or parts[-1] in RC_FILES
                or parts[-1] in PROTECTED_COMPONENTS
                or PROTECTED_COMPONENTS & set(inner[:-1])):
            bump("config")
    if _RANK[best] < _RANK["credential"]:
        inodes = _inode_kinds(tuple(str(e) for e in extra))
        notes_only = best == "notes"
        for p in paths:
            k = _walk_kind(p, inodes)
            if k is not None and not (notes_only and k == "config"):
                bump(k)  # ~/.claude (config) above a notes folder that does not exist yet
    return best


def _control_in_notes(parts: tuple[str, ...]) -> bool:
    """Under ~/.claude/<notes dir>/: a nested .claude/ or hooks/ folder, or a settings*.json,
    is agent control, not a note."""
    starts = [i for i in range(len(parts) - 1) if parts[i] == ".claude"
              and parts[i + 1] in ("projects", "sessions", "plans", "todos")]
    if not starts:
        return False
    i = starts[0]
    rel = parts[i + 2:]  # after ~/.claude/<projects|sessions|plans|todos>
    return (".claude" in rel or "hooks" in rel[:-1] or fnmatch.fnmatchcase(rel[-1] if rel else "",
                                                                         "settings*.json")
            or (rel[-1] if rel else "") in CONFIG_NAMES)


@lru_cache(maxsize=8)
def _inode_kinds(extra: tuple[str, ...]) -> dict[tuple[int, int], Kind]:
    """(device, inode) of each protected folder that exists -> its kind. One hook call is one
    process, so caching for its lifetime is safe."""
    out: dict[tuple[int, int], Kind] = {}
    for kind, dirs in (("config", config_dirs()), ("notes", notes_dirs()),
                       ("gate_log", gate_log_dirs(extra)), ("credential", credential_dirs())):
        for d in dirs:
            try:
                st = os.stat(d)
            except OSError:
                continue
            out[(st.st_dev, st.st_ino)] = kind  # type: ignore[assignment]
    return out


def _walk_kind(p: Path, inodes: dict[tuple[int, int], Kind]) -> Kind | None:
    """The kind of the protected folder `p` (or a folder above it that exists) is another
    name for: different case, a firmlink such as /System/Volumes/Data, a bind mount.
    The deepest match wins (~/.claude/projects is notes, not config)."""
    best: Kind | None = None
    for q in (*reversed(p.parents), p):  # from / down: stop where the path stops existing
        try:
            st = os.stat(q)
        except OSError:
            break
        best = inodes.get((st.st_dev, st.st_ino), best)
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
    + r"|(?:" + _B + r"|/)credentials(?![\w.-]*\.(?:" + "|".join(SOURCE_EXTS)
    + r")(?=$|[\s'\";|&)]))(?:\.[\w.-]+)?(?=$|[\s'\";|&)/]|\.)"
    + r"|(?:" + _B + r"\.|/)[\w.-]*_history(?![\w-])"
    + r"|(?:^|[\s;&|(`])security\s+(?:find|dump|export)-",
    re.IGNORECASE,
)
_BASH_GATE_LOG = re.compile(r"\.deliberator/gate\b", re.IGNORECASE)
_BASH_CONFIG = re.compile(
    _B + r"\.(?:claude|deliberator)(?![\w-])"
    r"|\.config/deliberator\b|\.local/share/deliberator\b"
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


def _glob_kind(text: str, cwd_is_home: bool = False) -> Kind | None:
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
    # With dotglob (bash) or GLOB_DOTS (zsh) on, `*` matches dot names too: a glob right
    # under home (~/*/settings.json, $HOME/*) may be a protected folder.
    homes = {"~", "$home", "${home}", _fold(_home())} | ({""} if cwd_is_home else set())
    for token in _TOKEN.findall(text):
        comps = token.split("/")
        for i in range(0 if cwd_is_home else 1, len(comps) if "/" in token else 0):
            if any(c in comps[i] for c in "*?[") and _fold("/".join(comps[:i])) in homes:
                for alt in _braces(comps[i]):
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


_HEREDOC = re.compile(r"<<-?[ \t]*(['\"]?)([A-Za-z_][\w-]*)\1")


def strip_heredocs(command: str) -> str:
    """The command without heredoc bodies. A body is never parsed as shell words: no
    globbing, no $'..'; with an unquoted delimiter only $var, $(..) and backticks expand, and
    those are kept (the body is kept whole when the delimiter is unquoted and it has any)."""
    out, pos = [], 0
    for m in _HEREDOC.finditer(command):
        if m.start() < pos:
            continue
        start = command.find("\n", m.end())
        if start < 0:
            break
        end_m = re.compile(r"^[ \t]*" + re.escape(m.group(2)) + r"[ \t]*$", re.MULTILINE)
        end = end_m.search(command, start + 1)
        stop = end.end() if end else len(command)
        body = command[start + 1:end.start() if end else len(command)]
        out.append(command[pos:start + 1])
        if not m.group(1) and ("$" in body or "`" in body):
            out.append(body)  # unquoted delimiter: substitutions in the body still run
        out.append("\n")
        pos = stop
    out.append(command[pos:])
    return "".join(out)


def _mask_quoted_globs(command: str) -> str:
    """Glob characters inside quotes are literal: replace them so only live globs remain."""
    out, quote, escaped = [], "", False
    for ch in command:
        if escaped:
            escaped = False
            out.append("x" if ch in "*?[{" else ch)
            continue
        if ch == "\\" and quote != "'":
            escaped = True
        elif quote:
            if ch == quote:
                quote = ""
            elif ch in "*?[{":
                ch = "x"
        elif ch in "'\"":
            quote = ch
        out.append(ch)
    return "".join(out)


def _ansi_c(command: str) -> bool:
    """An unquoted $'...' or $"..." (ANSI-C or locale quoting), not a `$'` inside quotes."""
    quote = ""
    escaped = False
    for i, ch in enumerate(command):
        if escaped:
            escaped = False
        elif quote:
            if ch == quote:
                quote = ""
            elif ch == "\\" and quote == '"':
                escaped = True
        elif ch == "\\":
            escaped = True
        elif ch == "$" and command[i + 1:i + 2] in ("'", '"'):
            return True
        elif ch in "'\"":
            quote = ch
    return False


_NOTES = re.compile(r"(?:~|\$HOME|\$\{HOME\}|" + re.escape(str(_home()))
                    + r")/\.claude/(?:projects|sessions|plans|todos)(?=/|$|[\s'\";|&)])",
                    re.IGNORECASE)


_C = r"(?:^|(?<=[\s;&|(`{!/=]))"  # start of a command word
_GIT = _C + r"git(?:\s+(?:-[Cc]\s*\S+|--[\w-]+(?:=\S+)?|-\w))*\s+"
# Commands that print secrets: a hard ask like a credential file.
_SECRET_PRINTERS = re.compile(
    _GIT + r"credential\b"
    + r"|" + _C + r"gh\s+auth\s+token\b"
    + r"|" + _C + r"op\s+read\b"
    + r"|" + _C + r"gcloud\s+auth\s+print-(?:access|identity)-token\b"
    + r"|" + _C + r"aws\s+configure\s+(?:export-credentials|get)\b"
    + r"|" + _C + r"(?:env|printenv)(?:\s+-\w+)*\s*(?=$|[;&|)\n])"
    + r"|" + _C + r"printenv\s+(?:-\w+\s+)*\w*(?:token|secret|key|pass|credential|auth|private"
    r"|session|cookie)\w*",
    re.IGNORECASE,
)
_GIT_CONFIG = re.compile(_GIT + r"config\b(?P<rest>[^;&|)\n]*)")
_GIT_CONFIG_READ = re.compile(r"(?:^|\s)(?:--get[\w-]*|--list|-l|get|list)(?=\s|=|$)")
_GIT_CONFIG_SCOPE = re.compile(r"(?:^|\s)--(?:global|system)\b")
# Reads that dump many keys at once (and so can print a token in url.*.insteadOf or a
# credential-store path) are treated like a secret key.
_GIT_CONFIG_DUMP = re.compile(r"(?:^|\s)(?:--list|-l|list|--get-regexp|--get-urlmatch)(?=\s|=|$)")
# Other git calls that change what runs: remotes, submodules. (`worktree add` is ordinary
# work and goes to the judge; in an untrusted repo any git is a hard ask anyway.)
_GIT_SETUP = re.compile(_GIT + r"(?:remote\s+(?:add|set-url|set-head|rename)|submodule\s+add)\b")
# Keys whose values are secrets or redirect where credentials go.
_SECRET_KEY = re.compile(r"credential|token|password|helper|insteadof", re.IGNORECASE)


def _git_setup_kind(text: str) -> Kind | None:
    """git config writes, remote add/set-url and submodule add change what git and its hooks
    run: config. --global/--system writes, and reads of secret-looking keys there
    (credential, token, password, helper, url.*.insteadOf) or dumps of many keys (--list,
    --get-regexp), are credential. Other
    --global/--system reads go to the judge."""
    best: Kind | None = None
    for m in _GIT_CONFIG.finditer(text):
        rest = m.group("rest")
        read = _GIT_CONFIG_READ.search(rest) is not None
        if _GIT_CONFIG_SCOPE.search(rest):
            if not read or _SECRET_KEY.search(rest) or _GIT_CONFIG_DUMP.search(rest):
                return "credential"  # user/system config holds credential helpers
            continue
        if rest.strip() and not read:
            best = "config"
    if best is None and _GIT_SETUP.search(text):
        best = "config"
    return best


def command_kind(command: str, extra: Iterable[str | Path] = (),
                 cwd: str = "") -> Kind | None:
    """The most sensitive protected location the command text mentions."""
    shell = strip_heredocs(command)
    if _ansi_c(shell):
        return "credential"  # ANSI-C / locale quoting can spell any path, a credential too
    unquoted = re.sub(r"[\"'\\]", "", command)
    variants = {command, unquoted, _squash(command), _squash(unquoted)}
    home = str(_home())
    at_home = bool(cwd) and _fold(os.path.normpath(cwd)) == _fold(_home())
    best: Kind | None = _glob_kind(_strip_worktrees(_mask_quoted_globs(shell)), at_home)
    for text in variants:
        text = _strip_worktrees(text)
        if _BASH_CREDENTIAL.search(text) or _SECRET_PRINTERS.search(text):
            return "credential"
        setup = _git_setup_kind(text)
        if setup == "credential":
            return "credential"
        found: list[Kind | None] = [setup]
        if _BASH_GATE_LOG.search(text):
            found.append("gate_log")
        folded = text.casefold()
        for d in extra:
            ds = os.path.expanduser(str(d))
            short = ds.replace(home, "~", 1) if ds.startswith(home) else ds
            if ds.casefold() in folded or short.casefold() in folded:
                found.append("gate_log")
        if _NOTES.search(text):
            found.append("notes")
        if _BASH_CONFIG.search(_NOTES.sub("AGENT_NOTES", text)):
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
        lexer = shlex.shlex(strip_heredocs(command), posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        words = list(lexer)
    except ValueError:
        return None  # the text checks still apply
    best: Kind | None = None
    for word in words[:_MAX_WORDS]:
        name, eq, rhs = word.partition("=")
        parts = {rhs} if eq and "/" not in name else {word, rhs}  # NAME=path: the path
        for part in parts:
            if (part and len(part) <= _MAX_PATH and not any(c.isspace() for c in part)
                    and ("/" in part or part.startswith((".", "~")))):
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
        a, b = command_kind(command, extra, cwd), None
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
