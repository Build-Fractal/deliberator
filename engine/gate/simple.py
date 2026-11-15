"""Whether a shell command is simple enough for the allow-list to skip the judge.

The allow-list (``allow_without_asking``) is a regex, and a regex over shell text can be
fooled: quoting (``find . '-delete'``), assignment prefixes (``ls=x env python3``), zsh
expansions (``echo =(id)``, ``ls x(e:'cmd':)``), valued flags that swallow the next flag
(``git diff -U --output=f``), unnormalised paths (``~/.config//gh``) and recursive reads of
a folder above a protected one (``rg secret ~``).

So the fast path is deliberately small, and anything it is unsure about goes to the judge
(a model call, ~2.5 s), never straight to ask:

- **Characters**: outside quotes only letters, digits, space and ``- _ . / : = + , @ %``; a
  leading ``~`` (``~`` or ``~/``) and ``~`` before a digit (``HEAD~2``). Inside single quotes
  anything but a newline; inside double quotes no ``$``, backtick, ``\\`` or ``!``. Every other
  character (globs, braces, parens, ``$``, ``\\``, ``^``, ``#``, ``!``, ``;``, ``|``, ``<``...)
  makes the command not simple, in bash or zsh. With that alphabet ``shlex`` splits the words
  the way the shell does.
- **Command**: the first word must be a known command (``COMMANDS`` or ``git`` with a known
  subcommand). No assignment, no path, no unknown command.
- **Words**: no word starts with ``=`` (zsh ``=cmd``). Every flag is on that command's safe
  list; a deny set is checked against every word wherever it sits (after ``--``, as a value).
  git's valued short flags never take the next word (``-U`` only takes ``-U3``).
- **Paths**: every word, and every flag value, is checked with ``protect.path_is_protected``
  (normalised, case-folded, by inode). Recursive readers (``rg``, ``find``, ``tree``, ``du``,
  ``ls -R``) are not simple when a path they walk (or the working folder, with none given)
  holds a protected folder: ``~``, ``~/.config``, ``/``.

The allow-list regex is then matched against the words joined by spaces, so it sees the
real argv[0] (``^ls\\b`` cannot match ``ls=x``).
"""

from __future__ import annotations

import os
import re
import shlex
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from engine.gate import protect

_PLAIN = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                   " -_./:=+,@%")
_DOUBLE_QUOTE_BAD = frozenset("$`\\!\n")


def plain(command: str) -> bool:
    """Only characters the shell (bash or zsh) takes literally; quotes balanced."""
    quote = ""
    prev = " "
    for i, ch in enumerate(command):
        if quote == "'":
            if ch == "\n":
                return False
            if ch == "'":
                quote = ""
        elif quote == '"':
            if ch in _DOUBLE_QUOTE_BAD:
                return False
            if ch == '"':
                quote = ""
        elif ch in "'\"":
            quote = ch
        elif ch == "~":
            nxt = command[i + 1:i + 2]
            word_start = prev in " \t"
            if not ((word_start and nxt in ("", "/", " ")) or (not word_start and nxt.isdigit())):
                return False
        elif ch not in _PLAIN:
            return False
        prev = ch
    return not quote


@dataclass(frozen=True)
class Spec:
    """Safe flags for one command.

    ``short``: single-letter flags that may be bundled (``-la``). ``valued``: short flags that
    take a value (attached ``-n5``, or the next word unless ``attached_only``). ``long``:
    ``--name`` flags (alone or ``--name=value``) and single-dash long flags (find ``-name``).
    ``spaced``: long flags whose value is the next word. ``numeric``: ``-20`` counts.
    ``deny``: prefixes refused in any word. ``positional``: a check on each non-flag word.
    ``recursive``: walks the folders it is given (or the working folder).
    """

    short: str = ""
    valued: str = ""
    long: frozenset[str] = field(default_factory=frozenset)
    spaced: frozenset[str] = field(default_factory=frozenset)
    numeric: bool = False
    attached_only: bool = False
    deny: tuple[str, ...] = ()
    positional: Callable[[str], bool] | None = None
    recursive: bool = False


def _s(short: str = "", valued: str = "", long: str = "", spaced: str = "", **kw) -> Spec:
    return Spec(short, valued, frozenset(long.split()), frozenset(spaced.split()), **kw)


def _never(word: str) -> bool:
    return False


def _date_arg(word: str) -> bool:
    return word.startswith("+")  # a format; any other word would set the clock


_REF = re.compile(r"[\w][\w./-]*")


def _fetch_arg(word: str) -> bool:
    # A remote or branch name. Refspecs (:), forced (+), URLs and paths are judged.
    return bool(_REF.fullmatch(word)) and ".." not in word


# Refused anywhere in a git command: they write files, run programs or read outside the repo.
_GIT_DENY = ("--output", "-O", "--open-files-in-pager", "--exec-path", "--upload-pack",
             "--receive-pack", "--ext-diff", "--textconv", "--config-env", "--git-dir",
             "--work-tree", "--namespace", "--super-prefix", "--no-index", "--paginate",
             "-c", "-C")
_BRANCH_DENY = _GIT_DENY + ("-m", "-M", "-d", "-D", "-f", "-u", "--force", "--move",
                            "--copy", "--delete", "--set-upstream", "--unset-upstream",
                            "--edit-description", "--track", "--no-track", "--create-reflog")

_LOG_LONG = (
    "--oneline --graph --decorate --no-decorate --all --branches --tags --remotes --stat "
    "--shortstat --numstat --name-only --name-status --patch --no-patch --format --pretty "
    "--since --until --after --before --author --committer --grep --reverse --first-parent "
    "--no-merges --merges --follow --abbrev-commit --abbrev --date --max-count --skip "
    "--left-right --cherry-pick --boundary --topo-order --date-order --color --no-color "
    "--source --simplify-by-decoration --regexp-ignore-case --all-match --invert-grep "
    "--no-ext-diff --no-textconv --summary --relative --diff-filter --unified --word-diff "
    "--ignore-all-space --mailmap --decorate-refs --decorate-refs-exclude --no-walk "
    "--ancestry-path --cherry --full-history --minimal --patience --histogram "
    "--find-renames --compact-summary --quiet"
)
_DIFF_LONG = (
    "--stat --shortstat --numstat --name-only --name-status --cached --staged --patch "
    "--no-patch --unified --ignore-all-space --ignore-space-change --ignore-blank-lines "
    "--color --no-color --color-words --word-diff --minimal --patience --histogram "
    "--find-renames --summary --check --no-ext-diff --no-textconv --merge-base "
    "--diff-filter --relative --exit-code --quiet --dirstat --compact-summary --raw "
    "--function-context"
)

GIT: dict[str, Spec] = {
    "status": _s("sbuvz", long="--short --branch --porcelain --untracked-files --ignored "
                 "--verbose --show-stash --long --ahead-behind --no-ahead-behind",
                 attached_only=True, deny=_GIT_DENY),
    "diff": _s("pRwbz", valued="U", long=_DIFF_LONG, attached_only=True, deny=_GIT_DENY),
    "log": _s("pi", valued="n", long=_LOG_LONG, numeric=True, attached_only=True,
              deny=_GIT_DENY),
    "show": _s("psq", valued="U", long=_LOG_LONG + " " + _DIFF_LONG, attached_only=True,
               deny=_GIT_DENY),
    # Listing only: a bare name creates a branch (and `--format --list x` hides one).
    "branch": _s("arv", long="--all --remotes --verbose --show-current --no-color --color",
                 attached_only=True, deny=_BRANCH_DENY, positional=_never),
    "rev-parse": _s("q", long="--show-toplevel --abbrev-ref --git-dir --short --verify "
                    "--is-inside-work-tree --git-common-dir --show-prefix --symbolic-full-name "
                    "--quiet --absolute-git-dir --show-cdup --is-bare-repository",
                    attached_only=True, deny=_GIT_DENY),
    "fetch": _s("pvq", long="--all --prune --tags --no-tags --dry-run --verbose --quiet "
                "--prune-tags --progress --no-progress", attached_only=True,
                deny=_GIT_DENY + ("-f", "--force", "--refmap"), positional=_fetch_arg),
    "worktree list": _s("v", long="--porcelain --verbose", attached_only=True,
                        deny=_GIT_DENY, positional=_never),
    "remote": _s("v", long="--verbose", attached_only=True, deny=_GIT_DENY,
                 positional=_never),
}

_FIND_DENY = ("-delete", "-exec", "-ok", "-fprint", "-fls", "-D", "--")
_RG_DENY = ("--pre", "--hostname-bin", "--search-zip", "-z", "--hidden", "--no-ignore",
            "--unrestricted", "-u", "--follow", "-L", "--ignore-file", "--no-config")

COMMANDS: dict[str, Spec] = {
    "ls": _s("1aAbBcCdeFfgGhHiklLmnopqrRsStTuUvwx@", long="--color --all --almost-all "
             "--human-readable --classify --reverse --recursive --directory "
             "--group-directories-first --long"),
    "pwd": _s("LP"),
    "cat": _s("nbsvetAETu"),
    "head": _s("qv", valued="nc", long="--lines --bytes --quiet --verbose", numeric=True),
    "tail": _s("qvfFr", valued="nc", long="--lines --bytes --quiet --verbose --follow",
               numeric=True),
    "wc": _s("lwcmL", long="--lines --words --bytes --chars --max-line-length"),
    # Not recursive here (-r/-R would read a whole tree, .env files included): judged.
    "grep": _s("ivnlLcwxEFGhHsqIoaZ", valued="eABCm",
               long="--color --colour --max-count --ignore-case --invert-match --line-number "
               "--files-with-matches --files-without-match --count --word-regexp "
               "--line-regexp --extended-regexp --fixed-strings --no-filename --with-filename "
               "--only-matching --quiet --silent --context --after-context --before-context "
               "--regexp --text --null --no-messages",
               deny=("-r", "-R", "--recursive", "--dereference-recursive", "-d", "--directories",
                     "-f", "--file")),
    "rg": _s("iSswxvnNlcFHIqoaP", valued="eABCgtTmM",
             long="--files --type --type-not --glob --iglob --max-count --max-depth --json "
             "--count --count-matches --files-with-matches --files-without-match "
             "--line-number --no-line-number --no-heading --heading --color --context "
             "--after-context --before-context --sort --sortr --type-list --multiline "
             "--trim --stats --no-filename --with-filename --ignore-case --smart-case "
             "--case-sensitive --word-regexp --line-regexp --invert-match --fixed-strings "
             "--only-matching --regexp --max-columns --vimgrep --column --text --passthru "
             "--null --quiet --no-messages",
             deny=_RG_DENY, recursive=True),
    "find": _s("", long="-name -iname -type -maxdepth -mindepth -path -ipath -not -print "
               "-print0 -mtime -mmin -size -prune -and -or -a -o -empty -depth",
               spaced="-name -iname -type -maxdepth -mindepth -path -ipath -mtime -mmin "
               "-size", deny=_FIND_DENY, recursive=True),
    "which": _s("as"),
    "echo": _s("n"),
    "tree": _s("adfisughpDCnNQFrtx", valued="L", long="--gitignore --noreport --dirsfirst",
               deny=("-o", "-R", "-H", "--fromfile", "-l"), recursive=True),
    "du": _s("shckmgx", valued="d", long="--max-depth --summarize --human-readable --total",
             deny=("-L", "--dereference"), recursive=True),
    "df": _s("hkmgHlPTi", long="--human-readable --si --local --portability --print-type "
             "--inodes --total"),
    "date": _s("u", long="--utc", positional=_date_arg),
}

_NUMERIC = re.compile(r"-\d+")


def _denied(word: str, deny: tuple[str, ...]) -> bool:
    for d in deny:
        if d.startswith("--"):
            if d in word:
                return True
        elif word.startswith(d):
            return True
    return False


def _flag(word: str, spec: Spec) -> tuple[bool, bool, str | None]:
    """(safe, takes the next word as its value, attached value to check as a path)."""
    name, _, value = word.partition("=")
    if word.startswith("--") or name in spec.long:
        if name not in spec.long:
            return False, False, None
        return True, (not value and name in spec.spaced), value or None
    if spec.numeric and _NUMERIC.fullmatch(word):
        return True, False, None
    letters = word[1:]
    for i, ch in enumerate(letters):
        if ch in spec.valued:
            rest = letters[i + 1:]
            if rest:
                return True, False, rest
            return True, not spec.attached_only, None
        if ch not in spec.short:
            return False, False, None
    return True, False, None


def _spec_for(words: list[str]) -> tuple[Spec | None, list[str]]:
    name = words[0]
    if name == "git":
        if len(words) < 2:
            return None, []
        if words[1] == "worktree":
            return (GIT["worktree list"], words[3:]) if words[2:3] == ["list"] else (None, [])
        return GIT.get(words[1]), words[2:]  # git -c/-C/...: no subcommand spec: judged
    return COMMANDS.get(name), words[1:]


def _norm(word: str, cwd: str) -> str:
    p = os.path.expanduser(word)
    if not os.path.isabs(p):
        p = os.path.join(cwd or ".", p)
    return os.path.normpath(p).casefold()


def _holds_protected(folder: str, cwd: str) -> bool:
    """`folder` (as written) is a protected folder or above one: walking it reads them."""
    f = _norm(folder, cwd).rstrip("/") or "/"
    targets = [Path.home(), *protect.protected_dirs()]
    for t in targets:
        for form in {os.path.normpath(str(t)).casefold(), str(_safe_resolve(t)).casefold()}:
            if form == f or form.startswith(f.rstrip("/") + "/"):
                return True
    return False


def _safe_resolve(p: Path) -> Path:
    try:
        return p.resolve()
    except (OSError, RuntimeError):
        return p


def simple_words(command: str, cwd: str = "") -> list[str] | None:
    """The command's words when the allow-list may skip the judge for it, else None."""
    if not command.strip() or not plain(command):
        return None
    try:
        words = shlex.split(command, posix=True)
    except ValueError:
        return None
    if not words or any(w.startswith("=") for w in words):
        return None
    spec, args = _spec_for(words)
    if spec is None:
        return None
    paths: list[str] = []
    positionals: list[str] = []
    takes_value = end_of_flags = recursive = False
    for word in args:
        if _denied(word, spec.deny):
            return None
        if takes_value:
            takes_value = False
            paths.append(word)
            continue
        if not end_of_flags and word == "--":
            end_of_flags = True
            continue
        if not end_of_flags and word.startswith("-") and word != "-":
            ok, takes_value, value = _flag(word, spec)
            if not ok:
                return None
            if value:
                paths.append(value)
            if words[0] == "ls" and ("R" in word.lstrip("-") and not word.startswith("--")
                                     or word == "--recursive"):
                recursive = True
            continue
        if spec.positional is not None and not spec.positional(word):
            return None
        positionals.append(word)
        paths.append(word)
    if any(protect.path_is_protected(p, cwd) for p in paths if p):
        return None
    if spec.recursive or recursive:
        # rg's first word is usually the pattern: check it as a folder too (harmless), and
        # add the working folder when no folder follows it.
        walked = list(positionals)
        if not positionals or (words[0] == "rg" and len(positionals) == 1):
            walked.append(".")
        if any(_holds_protected(w, cwd) for w in walked):
            return None
    return words


def is_simple(command: str, cwd: str = "") -> bool:
    return simple_words(command, cwd) is not None
