"""Whether a shell command is simple enough for the allow-list to skip the judge.

The allow-list (``allow_without_asking``) is a regex over the raw command, so on its own it
can be fooled by shell syntax: quotes (``find . '-delete'``, ``-de''lete``), globs and brace
expansion, ``$VAR`` (``echo $ANTHROPIC_API_KEY``) and flags that make a read-only command
write or run something (``git fetch --upload-pack=cmd``, ``rg --pre``, ``git diff --output``).

A command is simple only when:

- the shell would expand nothing: no unquoted glob or brace (``* ? [ {``), no ``$`` or
  backtick outside single quotes, and it parses (``shlex``) to words;
- every flag, after unquoting, is on the safe list for that command (git: per subcommand);
  an unknown flag is not simple, so a new or rare flag goes to the judge;
- positional words pass the command's check where one exists (``git fetch`` refspecs,
  ``git branch`` names, ``date`` arguments).

Not simple never means ask: the judge rules, informed. This only decides whether the
allow-list may skip the model.
"""

from __future__ import annotations

import re
import shlex
from collections.abc import Callable
from dataclasses import dataclass, field

_UNQUOTED_EXPANDS = frozenset("*?[{$`")
_DOUBLE_QUOTED_EXPANDS = frozenset("$`")


def expands(command: str) -> bool:
    """The shell would expand something in this command: a glob, brace, ``$`` or backtick
    outside quotes, or ``$``/backtick inside double quotes. Unbalanced quotes count."""
    quote = ""
    escaped = False
    for ch in command:
        if escaped:
            escaped = False
            continue
        if quote == "'":
            if ch == "'":
                quote = ""
            continue
        if ch == "\\":
            escaped = True
            continue
        if quote == '"':
            if ch == '"':
                quote = ""
            elif ch in _DOUBLE_QUOTED_EXPANDS:
                return True
            continue
        if ch in "'\"":
            quote = ch
        elif ch in _UNQUOTED_EXPANDS:
            return True
    return bool(quote) or escaped


@dataclass(frozen=True)
class Spec:
    """Safe flags for one command.

    ``short``: single-letter flags that may be bundled (``-la``). ``valued``: short flags that
    take a value, attached (``-n5``) or as the next word. ``long``: ``--name`` flags (with or
    without ``=value``) and single-dash long flags such as find's ``-name``. ``numeric``:
    ``-20`` style counts are fine. ``positional``: a check on each non-flag word.
    """

    short: str = ""
    valued: str = ""
    long: frozenset[str] = field(default_factory=frozenset)
    numeric: bool = False
    positional: Callable[[str, list[str]], bool] | None = None


def _s(short: str = "", valued: str = "", long: str = "", numeric: bool = False,
       positional: Callable[[str, list[str]], bool] | None = None) -> Spec:
    return Spec(short, valued, frozenset(long.split()), numeric, positional)


def _date_arg(word: str, words: list[str]) -> bool:
    return word.startswith("+")  # a format; any other word would set the clock


def _no_positional(word: str, words: list[str]) -> bool:
    return False


def _fetch_arg(word: str, words: list[str]) -> bool:
    return ":" not in word and not word.startswith("+")  # a refspec can move local branches


_BRANCH_LIST_MODE = frozenset({"--list", "-l", "--contains", "--no-contains", "--merged",
                               "--no-merged", "--points-at"})


def _branch_arg(word: str, words: list[str]) -> bool:
    # A bare name creates a branch; in list mode words are patterns or commits.
    return any(w.split("=", 1)[0] in _BRANCH_LIST_MODE for w in words)


_LOG_LONG = (
    "--oneline --graph --decorate --no-decorate --all --branches --tags --remotes --stat "
    "--shortstat --numstat --name-only --name-status --patch --no-patch --format --pretty "
    "--since --until --after --before --author --committer --grep --reverse --first-parent "
    "--no-merges --merges --follow --abbrev-commit --abbrev --date --max-count --skip "
    "--left-right --cherry-pick --boundary --topo-order --date-order --color --no-color "
    "--source --simplify-by-decoration --regexp-ignore-case --extended-regexp --fixed-strings "
    "--all-match --invert-grep --walk-reflogs --no-ext-diff --no-textconv --summary "
    "--relative --diff-filter --unified --word-diff --ignore-all-space --mailmap --show-signature "
    "--decorate-refs --decorate-refs-exclude --exclude --no-walk --ancestry-path --cherry "
    "--full-history --minimal --patience --histogram --find-renames --find-copies --dirstat "
    "--compact-summary --full-index --binary --quiet"
)
_DIFF_LONG = (
    "--stat --shortstat --numstat --name-only --name-status --cached --staged --patch "
    "--no-patch --unified --ignore-all-space --ignore-space-change --ignore-blank-lines "
    "--color --no-color --color-words --word-diff --minimal --patience --histogram "
    "--find-renames --find-copies --summary --check --no-ext-diff --no-textconv --merge-base "
    "--diff-filter --relative --exit-code --quiet --dirstat --compact-summary --no-index "
    "--full-index --binary --abbrev --src-prefix --dst-prefix --no-prefix --submodule "
    "--ignore-submodules --raw --patch-with-stat --function-context --ita-visible-in-index"
)

GIT: dict[str, Spec] = {
    "status": _s("sbuvz", long="--short --branch --porcelain --untracked-files --ignored "
                 "--verbose --show-stash --long --ahead-behind --no-ahead-behind --renames "
                 "--no-renames --column --no-column --ignore-submodules"),
    "diff": _s("pRwbzMCB", valued="U", long=_DIFF_LONG),
    "log": _s("pgiEFPS", valued="nUSGL", long=_LOG_LONG, numeric=True),
    "show": _s("psqwzMC", valued="U", long=_LOG_LONG + " " + _DIFF_LONG),
    "branch": _s("arvl", long="--all --remotes --verbose --list --show-current --merged "
                 "--no-merged --contains --no-contains --sort --format --color --no-color "
                 "--points-at --column --no-column --ignore-case --abbrev --no-abbrev",
                 positional=_branch_arg),
    "rev-parse": _s("q", long="--show-toplevel --abbrev-ref --git-dir --short --verify "
                    "--is-inside-work-tree --git-common-dir --show-prefix --symbolic-full-name "
                    "--quiet --absolute-git-dir --show-cdup --is-bare-repository "
                    "--is-shallow-repository --symbolic --show-superproject-working-tree "
                    "--path-format --default"),
    "fetch": _s("pvqtn", long="--all --prune --tags --no-tags --dry-run --verbose --quiet "
                "--depth --prune-tags --unshallow --progress --no-progress --jobs "
                "--no-recurse-submodules --multiple --shallow-since --deepen --filter "
                "--no-write-fetch-head --show-forced-updates",
                positional=_fetch_arg),
    "worktree list": _s("vz", long="--porcelain --verbose -z", positional=_no_positional),
    "remote": _s("v", long="--verbose", positional=_no_positional),
}

COMMANDS: dict[str, Spec] = {
    "ls": _s("1aAbBcCdeFfgGhHiklLmnopqrRsStTuUvwx@O%,", long="--color --all --almost-all "
             "--human-readable --classify --sort --time --reverse --recursive --directory "
             "--group-directories-first --long --size"),
    "pwd": _s("LP"),
    "cat": _s("nbsvetAETul"),
    "head": _s("qv", valued="nc", long="--lines --bytes --quiet --verbose", numeric=True),
    "tail": _s("qvfFr", valued="nc", long="--lines --bytes --quiet --verbose --follow",
               numeric=True),
    "wc": _s("lwcmL", long="--lines --words --bytes --chars --max-line-length"),
    "grep": _s("ivnrRlLcwxEFGhHsqIozabUZP", valued="eABCmf",
               long="--include --exclude --exclude-dir --color --colour --max-count "
               "--ignore-case --invert-match --line-number --recursive --files-with-matches "
               "--files-without-match --count --word-regexp --line-regexp --extended-regexp "
               "--fixed-strings --no-filename --with-filename --only-matching --quiet "
               "--silent --context --after-context --before-context --regexp --text "
               "--binary-files --null --perl-regexp --no-messages --label"),
    "rg": _s("iSswxvnNlcFuUHIqoaPpL", valued="eABCgtTmMdj",
             long="--hidden --no-ignore --no-ignore-vcs --files --type --type-not --glob "
             "--iglob --follow --max-count --max-depth --json --count --count-matches "
             "--files-with-matches --files-without-match --line-number --no-line-number "
             "--no-heading --heading --color --context --after-context --before-context "
             "--sort --sortr --type-list --multiline --pcre2 --trim --stats --no-filename "
             "--with-filename --ignore-case --smart-case --case-sensitive --word-regexp "
             "--line-regexp --invert-match --fixed-strings --only-matching --regexp "
             "--max-columns --max-columns-preview --vimgrep --column --byte-offset --text "
             "--unrestricted --replace --passthru --null --quiet --debug --no-messages "
             "--max-filesize --multiline-dotall --crlf --engine --one-file-system "
             "--threads --path-separator --no-config"),
    "find": _s("LHPEsx", long="-name -iname -type -maxdepth -mindepth -path -ipath -not "
               "-print -print0 -newer -mtime -mmin -atime -amin -ctime -cmin -size -perm "
               "-prune -and -or -a -o -regex -iregex -empty -follow -ls -depth -user -group "
               "-links -wholename -iwholename -lname -ilname -readable -writable -executable "
               "-true -false -nouser -nogroup -xdev -mount -samefile -inum -quit -d -E"),
    "which": _s("as"),
    "echo": _s("neE"),
    "tree": _s("adfisughpDCnNQFlrtxJ", valued="LIP", long="--gitignore --noreport "
               "--dirsfirst --prune --filelimit --sort --charset -L -I -P"),
    "du": _s("shcakmgxLHAP", valued="dBI", long="--max-depth --summarize --human-readable "
             "--total --apparent-size --si"),
    "df": _s("hkmgHlPTiaY", long="--human-readable --si --local --portability --print-type "
             "--inodes --all --total --output"),
    "date": _s("uRjn", valued="Ivfr", long="--iso-8601 --rfc-3339 --utc --universal "
               "--rfc-email --date --reference", positional=_date_arg),
}
# Not on the safe lists (never simple), for the record: find -delete -exec -execdir -ok
# -okdir -fprint* -fls; rg --pre --pre-glob --hostname-bin -z/--search-zip; tree -o -R -H;
# git fetch --upload-pack -f/--force --refmap; git branch -d/-D/-m/-M/-c/-C/-f/-u
# --set-upstream-to --edit-description; git diff/log/show --output --ext-diff --textconv;
# git -c / -C / --exec-path and every other global option before the subcommand; date -s.

_NUMERIC = re.compile(r"-\d+")


def _flag_ok(word: str, spec: Spec) -> tuple[bool, bool]:
    """(the flag is safe, it consumes the next word as its value)."""
    if word in spec.long:
        return True, word in _SPACED_LONG
    if word.startswith("--"):
        return word.split("=", 1)[0] in spec.long, False
    if spec.numeric and _NUMERIC.fullmatch(word):
        return True, False
    if word.split("=", 1)[0] in spec.long:  # find-style -name, or -L=2
        return True, False
    letters = word[1:]
    for i, ch in enumerate(letters):
        if ch in spec.valued:
            return True, i == len(letters) - 1  # value attached (-n5) or the next word
        if ch not in spec.short:
            return False, False
    return True, False


# Single-dash long flags that take the next word (find predicates, tree's -L/-I/-P).
_SPACED_LONG = frozenset({
    "-name", "-iname", "-type", "-maxdepth", "-mindepth", "-path", "-ipath", "-newer",
    "-mtime", "-mmin", "-atime", "-amin", "-ctime", "-cmin", "-size", "-perm", "-regex",
    "-iregex", "-user", "-group", "-links", "-wholename", "-iwholename", "-lname", "-ilname",
    "-samefile", "-inum", "-L", "-I", "-P",
})


def _spec_for(words: list[str]) -> tuple[Spec | None, list[str]]:
    """The spec for this command and the words after the command (and git subcommand)."""
    name = words[0]
    if name == "git":
        if len(words) < 2 or words[1].startswith("-"):
            return None, []  # git -c / -C / --exec-path ...: global options are never simple
        if words[1] == "worktree":
            if len(words) < 3 or words[2] != "list":
                return None, []
            return GIT["worktree list"], words[3:]
        return GIT.get(words[1]), words[2:]
    return COMMANDS.get(name, _s(positional=None)), words[1:]


def is_simple(command: str) -> bool:
    """True when the allow-list may skip the judge for this (non-compound) command."""
    if not command.strip() or expands(command):
        return False
    try:
        words = shlex.split(command, posix=True)
    except ValueError:
        return False
    if not words:
        return False
    spec, args = _spec_for(words)
    if spec is None:
        return False
    takes_value = False
    end_of_flags = False
    for word in args:
        if takes_value:
            takes_value = False
            continue
        if not end_of_flags and word == "--":
            end_of_flags = True
            continue
        if not end_of_flags and word.startswith("-") and word != "-":
            ok, takes_value = _flag_ok(word, spec)
            if not ok:
                return False
            continue
        if spec.positional is not None and not spec.positional(word, args):
            return False
    return True
