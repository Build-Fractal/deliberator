"""What a shell command does with the paths it names: read them out, write them, send them,
run a program on them, or only mention them.

Hard asks are based on these operations, not on mentions: ``grep -v .git/``, ``find -not
-path './.git/*'``, ``cd <repo>/.claude/worktrees/x`` and a heredoc body only *mention* a
protected path, while ``cat ~/.aws/credentials``, ``echo x >> ~/.bashrc`` and ``rm -rf .git``
*operate* on one. A mention still keeps the call away from every shortcut (the judge rules);
only an operation can be a hard ask.

The parse is deliberately simple and errs towards "operation": an unknown program given a path
as an argument "runs" on it. What cannot be parsed is reported as ``opaque`` and the caller
falls back to the mention-based check.
"""

from __future__ import annotations

import os
import re
import shlex
from dataclasses import dataclass, field
from typing import Literal

Role = Literal["read", "write", "copy", "send", "run", "source"]

_HEREDOC = re.compile(r"<<-?[ \t]*(['\"]?)([A-Za-z_][\w-]*)\1")
_SUB = "__SUB__"
_SEMI = "__SEMI__"
_SEPARATORS = frozenset({";", "&&", "||", "|", "|&", "&", "(", ")", ";;", ";&"})
_WRITE_REDIRECTS = frozenset({">", ">>", ">|", "&>", "&>>", "<>"})
_MAX_DEPTH = 4


@dataclass(frozen=True)
class Op:
    role: Role
    word: str  # the path as written (variables assigned earlier in the command expanded)
    cwd: str  # the folder it is relative to (after any cd)


@dataclass(frozen=True)
class Delete:
    word: str  # the target as written (assigned variables expanded)
    cwd: str
    filtered: bool = False  # find -delete with a -name/-path/-type... test: not everything


@dataclass
class Parsed:
    ops: list[Op] = field(default_factory=list)
    # Why the command prints a secret (gh auth token, bare env, printenv TOKEN, ...), if it does.
    prints_secret: list[str] = field(default_factory=list)
    # It dumps the environment somewhere (env, printenv, set, export -p): sourcing a .env and
    # then printing the environment prints the secrets.
    prints_env: bool = False
    # git config writes ("config"), and writes of --global/--system config ("credential").
    git_config_writes: list[str] = field(default_factory=list)
    # git remote add/set-url/set-head/rename, submodule add/update/init/sync.
    git_setup: list[str] = field(default_factory=list)
    # Recursive deletes (rm -r, find -delete, rsync --delete, trash): each target.
    deletes: list[Delete] = field(default_factory=list)
    # Commands that wipe a machine: sudo rm, diskutil erase*, mkfs, dd to a disk device.
    wipes: list[str] = field(default_factory=list)
    opaque: bool = False


# ---------------------------------------------------------------------------------------------
# Scanning: heredocs, substitutions, newlines
# ---------------------------------------------------------------------------------------------


def _heredocs(command: str) -> tuple[str, list[str]]:
    """The command without heredoc bodies, and the bodies whose delimiter is unquoted (their
    $(..) and backticks still run)."""
    out, live, pos = [], [], 0
    for m in _HEREDOC.finditer(command):
        if m.start() < pos:
            continue
        start = command.find("\n", m.end())
        if start < 0:
            break
        end_m = re.compile(r"^[ \t]*" + re.escape(m.group(2)) + r"[ \t]*$", re.MULTILINE)
        end = end_m.search(command, start + 1)
        body = command[start + 1:end.start() if end else len(command)]
        out.append(command[pos:start + 1])
        if not m.group(1):
            live.append(body)
        pos = end.end() if end else len(command)
    out.append(command[pos:])
    return "".join(out), live


def _closing(text: str, i: int) -> int:
    """Index of the `)` closing the `(` at text[i-1], skipping quotes; -1 if none."""
    depth, quote = 1, ""
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 1
            elif ch == quote:
                quote = ""
        elif ch == "\\":
            i += 1
        elif ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _scan(text: str, *, body: bool = False) -> tuple[str, list[str]] | None:
    """`text` with each $(..), `..`, <(..) and >(..) replaced by a placeholder word, unquoted
    newlines made `;` and `\\;` made a word; plus the substituted commands. In a heredoc body
    (`body`) quotes mean nothing and only substitutions are taken. None: unbalanced."""
    out: list[str] = []
    subs: list[str] = []
    quote = ""
    i = 0
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1:i + 2]
        if quote == "'" and not body:
            out.append(ch)
            if ch == "'":
                quote = ""
            i += 1
            continue
        if ch == "\\":
            if not quote and not body and nxt == ";":
                out.append(f" {_SEMI} ")
            else:
                out.append(text[i:i + 2])
            i += 2
            continue
        if (ch == "$" and nxt == "(") or (ch in "<>" and nxt == "(" and not quote):
            end = _closing(text, i + 2)
            if end < 0:
                return None
            subs.append(text[i + 2:end])
            out.append(_SUB)
            i = end + 1
            continue
        if ch == "`":
            end = text.find("`", i + 1)
            if end < 0:
                return None
            subs.append(text[i + 1:end])
            out.append(_SUB)
            i = end + 1
            continue
        if not body:
            if quote == '"':
                if ch == '"':
                    quote = ""
            elif ch in "'\"":
                quote = ch
            elif ch == "\n":
                ch = ";"
        out.append(ch)
        i += 1
    if quote and not body:
        return None
    return "".join(out), subs


def _segments(command: str, depth: int = 0) -> list[str] | None:
    """Every command string the shell runs: the command itself and each substitution."""
    if depth > _MAX_DEPTH:
        return []
    shell, bodies = _heredocs(command)
    scanned = _scan(shell)
    if scanned is None:
        return None
    main, subs = scanned
    for b in bodies:
        got = _scan(b, body=True)
        if got is None:
            return None
        subs += got[1]
    out = [main]
    for s in subs:
        inner = _segments(s, depth + 1)
        if inner is None:
            return None
        out += inner
    return out


def _tokens(text: str) -> list[str] | None:
    try:
        lexer = shlex.shlex(text, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        lexer.commenters = "#"
        return list(lexer)
    except ValueError:
        return None


# ---------------------------------------------------------------------------------------------
# Words and flags
# ---------------------------------------------------------------------------------------------

_VAR = re.compile(r"\$(?:\{(\w+)\}|(\w+))")
_ASSIGN = re.compile(r"[A-Za-z_]\w*=")
_SECRET_NAME = re.compile(r"token|secret|key|pass|credential|auth|private|session|cookie",
                          re.IGNORECASE)
_SECRET_VAR = re.compile(r"\$(?:\{([A-Za-z_]\w*)\}|([A-Za-z_]\w*))")


def _expand(word: str, env: dict[str, str]) -> str:
    def sub(m: re.Match[str]) -> str:
        name = m.group(1) or m.group(2)
        return env.get(name, m.group(0))

    return _VAR.sub(sub, word) if "$" in word else word


def _operands(words: list[str], valued: frozenset[str] = frozenset()) -> list[str]:
    """Non-flag words (after `--`, everything), skipping the values of `valued` flags."""
    out: list[str] = []
    skip = False
    flags = True
    for w in words:
        if skip:
            skip = False
            continue
        if not w:
            continue  # sed -i '' (macOS): the empty backup suffix
        if flags and w == "--":
            flags = False
            continue
        if flags and w.startswith("-") and w != "-":
            if w in valued or (len(w) == 2 and w in valued):
                skip = True
            continue
        out.append(w)
    return out


def _has_flag(words: list[str], short: str = "", long: tuple[str, ...] = ()) -> bool:
    for w in words:
        if w == "--":
            return False
        if w.startswith("--"):
            if w.split("=", 1)[0] in long:
                return True
        elif w.startswith("-") and len(w) > 1 and short and any(c in w[1:] for c in short):
            return True
    return False


# ---------------------------------------------------------------------------------------------
# Command tables
# ---------------------------------------------------------------------------------------------

# Operands are only named: listing, testing, hashing, changing folder, printing the word.
MENTION = frozenset({
    "cd", "pushd", "popd", "ls", "exa", "eza", "lsd", "tree", "du", "df", "stat", "file",
    "test", "[", "[[", "which", "type", "whence", "where", "hash", "echo", "printf", "realpath",
    "readlink", "dirname", "basename", "wc", "md5", "md5sum", "shasum", "sha1sum", "sha256sum",
    "sha512sum", "cksum", "b2sum", "lsof", "open", "local", "readonly", "unset", "alias",
    "true", "false", ":", "sleep", "date", "exit", "return", "kill", "ps", "pgrep", "pkill",
    "uname", "whoami", "id", "mount", "wait", "jobs", "trap", "shift", "read", "let", "pwd",
    "hostname", "sw_vers", "sysctl", "diskutil", "tput", "clear", "say", "fd", "fdfind",
    "mdfind", "locate", "for", "case", "select", "function", "mktemp", "seq", "yes", "tr",
    "pbcopy", "pbpaste", "osascript", "afplay", "uptime", "vm_stat", "top", "htop", "free",
    "lsblk", "getconf", "ulimit", "umask", "source_if_exists",
})
# Every operand's content is read out (printed, or passed down a pipe).
READ = frozenset({
    "cat", "tac", "nl", "head", "tail", "less", "more", "most", "bat", "batcat", "strings",
    "xxd", "hexdump", "od", "base64", "base32", "basenc", "sort", "uniq", "cut", "paste",
    "column", "fold", "fmt", "rev", "diff", "sdiff", "colordiff", "cmp", "comm", "join",
    "iconv", "zcat", "gzcat", "bzcat", "xzcat", "zless", "zmore", "gunzip", "gzip", "bzip2",
    "xz", "zstd", "unzip", "tar", "zip", "7z", "plutil", "gpg", "sqlite3", "xmllint", "mlr",
    "vim", "vi", "nvim", "nano", "emacs", "textutil", "pdftotext", "exiftool", "expand",
    "unexpand", "split", "csplit", "look", "vis", "unvis", "expect", "dos2unix", "unix2dos",
})
# The first operand is a program or filter, the rest are read.
FILTERS = frozenset({"jq", "yq", "gojq", "jaq"})
GREPS = frozenset({"grep", "egrep", "fgrep", "zgrep", "ggrep", "pcregrep", "rg", "ag", "ack"})
AWKS = frozenset({"awk", "gawk", "mawk", "nawk"})
# Every operand is written, moved or deleted.
WRITE = frozenset({"rm", "rmdir", "unlink", "shred", "srm", "trash", "touch", "mkdir", "mv",
                   "tee", "truncate", "setfacl", "mkfifo"})
# The first operand is a mode or owner; the rest are written.
CHMODS = frozenset({"chmod", "chown", "chgrp", "chflags"})
# Sources are copied (read), the last operand is written.
COPIES = frozenset({"cp", "ditto", "install", "gcp"})
# Operands go off the machine.
SENDERS = frozenset({"curl", "wget", "http", "https", "xh", "httpie", "nc", "ncat", "netcat",
                     "socat", "sftp", "ftp", "aws", "gsutil", "rclone", "az", "gcloud", "mail",
                     "sendmail", "mutt", "s3cmd", "rsync", "scp", "ssh", "gh", "glab",
                     "telnet", "openssl"})
SOURCES = frozenset({"source", "."})
# Words that start a command without being it.
_PREFIX = frozenset({"sudo", "command", "builtin", "exec", "nohup", "time", "nice", "!", "{",
                     "}", "then", "do", "else", "if", "elif", "while", "until", "caffeinate",
                     "noglob", "stdbuf", "doas", "unbuffer", "chronic", "env", "timeout"})
_PREFIX_VALUED = {"sudo": frozenset({"-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-U"}),
                  "nice": frozenset({"-n"}), "env": frozenset({"-u", "-C", "-S", "-P"}),
                  "timeout": frozenset({"-s", "-k", "--signal", "--kill-after"}),
                  "stdbuf": frozenset({"-i", "-o", "-e"})}
_ENDS = frozenset({"fi", "done", "esac", "}"})
_SHELLS = frozenset({"bash", "sh", "zsh", "dash", "ksh", "fish"})

_GREP_VALUED = frozenset({
    "-e", "-f", "-m", "-A", "-B", "-C", "-d", "-D", "-g", "-t", "-T", "-M", "-j", "-E", "-r",
    "--regexp", "--file", "--max-count", "--after-context", "--before-context", "--context",
    "--glob", "--iglob", "--type", "--type-not", "--include", "--exclude", "--exclude-dir",
    "--include-dir", "--max-depth", "--color", "--colors", "--sort", "--sortr", "--threads",
    "--max-filesize", "--encoding", "--engine", "--replace", "--path-separator", "--pre",
    "--pre-glob", "--ignore-file", "--type-add", "--label", "--binary-files", "--devices",
    "--directories", "--max-columns", "--field-match-separator", "--field-context-separator",
    "--context-separator", "--group-separator",
})
_GREP_NAMES_ONLY = ("-l", "-L", "-c", "-q", "--files-with-matches", "--files-without-match",
                    "--count", "--count-matches", "--quiet", "--files", "--stats", "--json")


_GREP_SHORT_VALUED = frozenset({"-e", "-f", "-m", "-A", "-B", "-C", "-d", "-D"})
_RG_SHORT_VALUED = frozenset({"-e", "-f", "-m", "-A", "-B", "-C", "-g", "-t", "-T", "-M",
                              "-j", "-E", "-r"})


def _grep_files(prog: str, words: list[str]) -> tuple[list[str], bool]:
    """(the files a grep reads, whether it prints their lines)."""
    short = _RG_SHORT_VALUED if prog in ("rg", "ag", "ack") else _GREP_SHORT_VALUED
    long = frozenset(w for w in _GREP_VALUED if w.startswith("--"))
    ops = _operands(words, short | long)
    given = any(w in ("-e", "-f", "--regexp", "--file")
                or w.startswith(("--regexp=", "--file="))
                or (len(w) > 2 and w[:2] in ("-e", "-f") and not w.startswith("--"))
                for w in words)
    files = ops if given or (prog == "rg" and "--files" in words) else ops[1:]
    names_only = any(w in _GREP_NAMES_ONLY or (not w.startswith("--")
                                               and any(c in w[1:] for c in "lLcq"))
                     for w in words if w.startswith("-") and w != "--")
    pattern_files = [words[i + 1] for i, w in enumerate(words[:-1]) if w in ("-f", "--file")]
    recursive = prog in ("rg", "ag", "ack") or _has_flag(words, "rR", (
        "--recursive", "--dereference-recursive"))
    if not files and recursive:
        files = ["."]
    return [*files, *pattern_files], not names_only


def _sed_files(words: list[str]) -> list[str]:
    valued = frozenset({"-e", "-f", "--expression", "--file", "-l", "--line-length"})
    ops = _operands(words, valued)
    given = any(w in ("-e", "-f") or w.startswith(("--expression", "--file")) for w in words)
    return ops if given else ops[1:]


def _awk_files(words: list[str]) -> list[str]:
    valued = frozenset({"-f", "-v", "-F", "--file", "--assign", "--field-separator"})
    ops = _operands(words, valued)
    if not any(w in ("-f", "--file") for w in words):
        ops = ops[1:]
    return [w for w in ops if not _ASSIGN.match(w)]


def _in_place(words: list[str]) -> bool:
    """sed -i, -i.bak, -Ei, --in-place; perl -pi -e."""
    for w in words:
        if w == "--":
            return False
        if w == "--in-place" or w.startswith("--in-place="):
            return True
        if w.startswith("-") and not w.startswith("--"):
            m = re.match(r"[A-Za-z]*", w[1:])
            if m and "i" in m.group(0):
                return True
    return False


_CURL_SEND = frozenset({"-d", "--data", "--data-binary", "--data-raw", "--data-ascii",
                        "--data-urlencode", "-F", "--form", "--form-string", "-T",
                        "--upload-file", "--json", "--post-file", "--body-file", "-f",
                        "--input", "--attach", "--raw-field", "--field"})
_CURL_WRITE = frozenset({"-o", "--output", "-O", "--output-document", "-D", "--dump-header",
                         "-c", "--cookie-jar", "--trace", "--trace-ascii", "--stderr"})
# Flags whose value is a key or config the tool *uses* (ssh -i key), not data it sends.
_USES = frozenset({"-i", "-F", "-o", "-K", "--config", "-E", "--cert", "--key", "--cacert",
                   "--netrc-file", "--capath", "--proxy-cert", "--proxy-key", "--identity",
                   "--profile", "-J", "-L", "-R", "-D", "-W", "-S", "-c", "-l", "-p", "-P",
                   "-b", "-e", "-m", "-O", "-Q", "-w"})


def _sent_files(prog: str, words: list[str]) -> tuple[list[str], list[str], list[str]]:
    """For network tools: (sent, written, used) paths."""
    sent, written, used = [], [], []
    send = _CURL_SEND - _SSH_USES if prog in _SSH_LIKE else _CURL_SEND
    uses = _USES | _SSH_USES if prog in _SSH_LIKE else _USES
    i = 0
    while i < len(words):
        w = words[i]
        name, eq, val = w.partition("=")
        if w.startswith("-") and eq and name in send | _CURL_WRITE | uses:
            w, nxt = name, val
            step = 1
        else:
            nxt = words[i + 1] if i + 1 < len(words) else ""
            step = 2
        if w in send and (w.startswith("--") or len(w) == 2):
            sent.append(nxt)
            i += step
            continue
        if w in _CURL_WRITE and prog not in _SSH_LIKE:
            written.append(nxt)
            i += step
            continue
        if w in uses:
            used.append(nxt)
            i += step
            continue
        if not w.startswith("-"):
            sent.append(w)
        i += 1
    out = []
    for s in sent:
        s = s.split("=", 1)[1] if "=@" in s or "=<" in s else s
        out.append(s.lstrip("@<"))
    return out, written, used


_FIND_TESTS = frozenset({"-name", "-iname", "-path", "-ipath", "-wholename", "-iwholename",
                         "-regex", "-iregex", "-type", "-newer", "-mtime", "-mmin", "-atime",
                         "-amin", "-ctime", "-cmin", "-size", "-empty", "-user", "-group",
                         "-perm", "-links", "-inum", "-samefile", "-lname", "-ilname"})
_SSH_LIKE = frozenset({"ssh", "scp", "sftp", "rsync"})
_SSH_USES = frozenset({"-F", "-i", "-o", "-e"})


def _rev_path(word: str) -> str:
    """git's `rev:path` names a file in a commit."""
    rev, colon, path = word.partition(":")
    return path if colon and rev and "/" not in rev and path else word


_GIT_GLOBAL_VALUED = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                                "--exec-path", "--config-env"})
_GIT_READ = frozenset({"show", "diff", "log", "blame", "annotate", "cat-file",
                       "archive", "format-patch", "difftool", "range-diff", "whatchanged"})
_GIT_WRITE = frozenset({"rm", "mv", "checkout", "restore", "clean", "apply", "am"})
_GIT_CONFIG_READ = re.compile(r"(?:^|\s)(?:--get[\w-]*|--list|-l|get|list)(?=\s|=|$)")


# ---------------------------------------------------------------------------------------------
# The walk
# ---------------------------------------------------------------------------------------------


def _secret_command(prog: str, args: list[str]) -> str | None:
    """Commands whose output is a secret."""
    words = [a for a in args if not a.startswith("-")]
    flags = set(args) - set(words)
    if prog == "gh" and (words[:2] == ["auth", "token"]
                         or (words[:2] == ["auth", "status"] and flags & {"-t", "--show-token"})):
        return "gh auth token"
    if prog == "op" and (words[:1] == ["read"] or (words[:2] == ["item", "get"]
                                                   and "--reveal" in flags)):
        return "op read"
    if prog == "gcloud" and "auth" in words and any(
            w.startswith("print-") and w.endswith("-token") for w in words):
        return "gcloud auth print-*-token"
    if prog == "aws" and "configure" in words:
        i = words.index("configure")
        if words[i + 1:i + 2] in (["export-credentials"], ["get"]):
            return "aws configure " + words[i + 1]
    return None


def _cd(cwd: str, target: str | None) -> str:
    if target is None or target in ("~", ""):
        return os.path.expanduser("~")
    if target == "-":
        return cwd
    t = os.path.expandvars(os.path.expanduser(target))
    return os.path.normpath(t if os.path.isabs(t) else os.path.join(cwd or ".", t))


def _split(tokens: list[str]) -> list[tuple[list[str], str]]:
    """Simple commands, each with the operator that follows it."""
    out: list[tuple[list[str], str]] = []
    cur: list[str] = []
    for t in tokens:
        if t in _SEPARATORS:
            out.append((cur, t))
            cur = []
        else:
            cur.append(t)
    out.append((cur, ""))
    return out


class _Walker:
    def __init__(self, cwd: str) -> None:
        self.cwd = cwd or "."
        self.env: dict[str, str] = {}
        self.parsed = Parsed()
        self.extra_segments: list[str] = []

    def add(self, role: Role, word: str, cwd: str | None = None) -> None:
        if not word or word in (_SUB, _SEMI) or len(word) > 1024 or "\n" in word:
            return
        if role in ("send", "run") and any(c.isspace() for c in word):
            return  # text or inline code handed to a program, not a path
        self.parsed.ops.append(Op(role, word, cwd or self.cwd))

    def segment(self, text: str) -> bool:
        tokens = _tokens(text)
        if tokens is None:
            return False
        commands = _split(tokens)
        upstream: list[str] = []  # paths named earlier in the current pipeline
        for idx, (words, op) in enumerate(commands):
            piped_to = commands[idx + 1][0] if op in ("|", "|&") and idx + 1 < len(commands) \
                else None
            named = self.simple(words, piped_to, upstream)
            upstream = (upstream + named) if op in ("|", "|&") else []
        return True

    def simple(self, words: list[str], piped_to: list[str] | None,
               upstream: list[str]) -> list[str]:
        """One simple command. Returns the words it names (for a following xargs)."""
        words = [_expand(w, self.env) for w in words]
        rest: list[str] = []
        i = 0
        while i < len(words):  # redirects
            w = words[i]
            nxt = words[i + 1] if i + 1 < len(words) else ""
            if w in _WRITE_REDIRECTS:
                self.add("write", nxt)
                i += 2
            elif w == ">&":
                if nxt and not nxt.isdigit() and nxt != "-":
                    self.add("write", nxt)
                i += 2
            elif w == "<":
                self.add("read", nxt)
                i += 2
            elif w in ("<<", "<<-", "<<<", "<&"):
                i += 2
            elif w.isdigit() and nxt in (*_WRITE_REDIRECTS, ">&", "<", "<&"):
                i += 1
            else:
                rest.append(w)
                i += 1
        words = rest
        # Leading assignments and prefixes.
        sudo = False
        while words:
            w = words[0]
            if _ASSIGN.match(w):
                name, _, value = w.partition("=")
                self.env[name] = value
                words = words[1:]
            elif w == "env" and all(x.startswith("-") or _ASSIGN.match(x) for x in words[1:]):
                break  # bare `env`: prints the environment
            elif w in _PREFIX:
                sudo = sudo or w in ("sudo", "doas")
                valued = _PREFIX_VALUED.get(w, frozenset())
                words = words[1:]
                while words and words[0].startswith("-") and words[0] != "-":
                    words = words[2:] if words[0] in valued else words[1:]
                if w == "timeout" and words:
                    words = words[1:]  # the duration
            elif w in _ENDS:
                words = words[1:]
            else:
                break
        if not words:
            return []
        prog = os.path.basename(words[0])
        args = words[1:]
        self.wipe(prog, args, sudo)
        return self.dispatch(prog, args, piped_to, upstream)

    def wipe(self, prog: str, args: list[str], sudo: bool) -> None:
        w = self.parsed.wipes
        if sudo and prog in ("rm", "rmdir", "unlink", "shred", "srm", "find", "rsync", "mv",
                             "dd", "trash"):
            w.append(f"sudo {prog}")
        if prog == "diskutil" and args and args[0].lower().startswith(
                ("erase", "zerodisk", "secureerase", "randomdisk", "partitiondisk",
                 "reformat")):
            w.append(f"diskutil {args[0]}")
        if prog.startswith(("mkfs", "newfs")) or prog in ("wipefs", "fdisk", "gpt", "sgdisk"):
            w.append(prog)
        if prog == "dd" and any(re.match(r"of=/dev/(?:r?disk|sd|nvme|hd|xvd|mmcblk)", a)
                                for a in args):
            w.append("dd to a disk device")

    def dispatch(self, prog: str, args: list[str], piped_to: list[str] | None,
                 upstream: list[str]) -> list[str]:
        p = self.parsed
        if prog in ("cd", "pushd"):
            ops = _operands(args)
            self.cwd = _cd(self.cwd, ops[0] if ops else None)
            return []
        if prog in ("echo", "printf"):
            for w in args:
                for m in _SECRET_VAR.finditer(w):
                    name = m.group(1) or m.group(2)
                    if (name not in self.env and _SECRET_NAME.search(name)
                            and not re.search(r"\$\{" + name + r":?[+#]", w)):
                        p.prints_secret.append(f"prints ${name}")
            return list(args)
        if prog in ("env", "printenv", "set", "export", "declare", "typeset"):
            return self.env_dump(prog, args, piped_to)
        secret = _secret_command(prog, args)
        if secret:
            p.prints_secret.append(secret)
            return []
        if prog == "security" and args and re.match(r"(find|dump|export)-", args[0]):
            p.prints_secret.append("reads the keychain")
            return []
        if prog in _SHELLS or prog == "eval":
            code = (args[args.index("-c") + 1] if "-c" in args and args.index("-c") + 1
                    < len(args) else None) if prog != "eval" else " ".join(args)
            if code is not None:
                self.extra_segments.append(code)
                return []
            for w in _operands(args):
                self.add("run", w)
            return []
        if prog in MENTION:
            return list(args)
        if prog == "xargs":
            valued = frozenset({"-I", "-L", "-n", "-P", "-s", "-E", "-d", "-a"})
            j = 0
            while j < len(args) and args[j].startswith("-"):
                j += 2 if args[j] in valued else 1
            sub = args[j:]
            if not sub:
                return []
            before = len(self.parsed.deletes)
            named = self.dispatch(os.path.basename(sub[0]), [*sub[1:], *upstream], None, [])
            # xargs deletes what the pipe lists (files found inside), not the folder named.
            self.parsed.deletes[before:] = [Delete(d.word, d.cwd, True)
                                            for d in self.parsed.deletes[before:]]
            return named
        if prog in READ:
            for w in _operands(args):
                self.add("read", w)
            return []
        if prog in FILTERS:
            ops = _operands(args, frozenset({"--arg", "--argjson", "-L", "--indent", "-f",
                                             "--from-file"}))
            for w in (ops if "-f" in args or "--from-file" in args else ops[1:]):
                self.add("read", w)
            return []
        if prog in GREPS:
            files, prints = _grep_files(prog, args)
            for w in files:
                if prints:
                    self.add("read", w)
            return files
        if prog in ("sed", "gsed"):
            role: Role = "write" if _in_place(args) else "read"
            for w in _sed_files(args):
                self.add(role, w)
            return []
        if prog in ("perl", "ruby"):
            role = "write" if _in_place(args) else "run"
            for w in _operands(args, frozenset({"-e", "-E", "-I", "-M"})):
                self.add(role, w)
            return []
        if prog in AWKS:
            for w in _awk_files(args):
                self.add("read", w)
            return []
        if prog in WRITE:
            ops = _operands(args, frozenset({"-s", "--size", "-m", "--mode"}))
            for w in ops:
                self.add("write", w)
            recursive = prog in ("trash",) or (prog in ("rm", "srm") and _has_flag(
                args, "rR", ("--recursive",)))
            if recursive:
                for w in ops:
                    self.delete(w)
            return []
        if prog in CHMODS:
            ops = _operands(args, frozenset({"--reference"}))
            for w in ops[1:]:
                self.add("write", w)
            return []
        if prog in COPIES or prog == "ln":
            ops = _operands(args, frozenset({"-t", "--target-directory", "-S", "--suffix",
                                             "-m", "--mode", "-o", "-g"}))
            if ops:
                self.add("write", ops[-1])
                if prog != "ln":
                    for w in ops[:-1]:
                        self.add("copy", w)
            return []
        if prog == "dd":
            for w in args:
                if w.startswith("if="):
                    self.add("read", w[3:])
                elif w.startswith("of="):
                    self.add("write", w[3:])
            return []
        if prog == "find":
            return self.find(args)
        if prog == "git":
            return self.git(args)
        if prog in SOURCES:
            ops = _operands(args)
            if ops:
                self.add("source", ops[0])
            return []
        if prog == "rsync" and any(a.startswith(("--delete", "--del")) or a == "--remove-source-files"
                                   for a in args):
            ops = _operands(args, frozenset({"-e", "--rsh", "--exclude", "--include",
                                             "--filter", "-f"}))
            if ops:
                self.delete(ops[-1])
        if prog in SENDERS:
            sent, written, _used = _sent_files(prog, args)
            for w in sent:
                self.add("send", w)
            for w in written:
                self.add("write", w)
            return []
        # Anything else is a program the call runs: a path handed to it may be read and sent.
        for w in args:
            if w.startswith("-"):
                _, eq, val = w.partition("=")
                if eq:
                    self.add("run", val)
                continue
            if any(c.isspace() for c in w):
                continue  # inline code or text, not a path
            for part in {w, *re.split(r"[=:,]", w)}:
                self.add("run", part)
        return []

    def delete(self, word: str, filtered: bool = False) -> None:
        if word and word not in (_SUB, _SEMI):
            self.parsed.deletes.append(Delete(word, self.cwd, filtered))

    def env_dump(self, prog: str, args: list[str], piped_to: list[str] | None) -> list[str]:
        p = self.parsed
        names = [a for a in args if not a.startswith("-") and not _ASSIGN.match(a)]
        if prog == "env" and names:
            return []  # `env` with only flags prints everything (else it runs a command)
        if prog == "printenv" and names:
            for n in names:
                if _SECRET_NAME.search(n):
                    p.prints_secret.append(f"prints ${n}")
            return []
        if prog == "set" and args:
            return []  # set -e, set -- a b: only a bare `set` prints the variables
        if prog in ("export", "declare", "typeset") and (
                [a for a in args if not a.startswith("-")] or not set(args) <= {"-p", "-x"}):
            return []
        if prog in ("declare", "typeset") and not any(a in ("-p", "-x") for a in args):
            return []
        p.prints_env = True
        filtered = piped_to is not None and piped_to and os.path.basename(piped_to[0]) in GREPS \
            and not any(a in ("-v", "--invert-match") for a in piped_to)
        if not filtered:
            p.prints_secret.append(f"prints the whole environment ({prog})")
        return []

    def find(self, args: list[str]) -> list[str]:
        starts: list[str] = []
        i = 0
        while i < len(args) and not args[i].startswith(("-", "(", "!")) and args[i] != _SEMI:
            starts.append(args[i])
            i += 1
        if not starts:
            starts = ["."]
        expr = args[i:]
        if "-delete" in expr:
            filtered = any(w in _FIND_TESTS for w in expr)
            for s in starts:
                self.add("write", s)
                self.delete(s, filtered)
        j = 0
        while j < len(expr):
            if expr[j] in ("-exec", "-execdir", "-ok", "-okdir"):
                k = j + 1
                while k < len(expr) and expr[k] not in (_SEMI, "+", ";"):
                    k += 1
                sub = expr[j + 1:k]
                if sub:
                    filtered = any(w in _FIND_TESTS for w in expr[:j])
                    before = len(self.parsed.deletes)
                    for s in starts:
                        # {} stands for each file found: inside the start folders.
                        self.dispatch(os.path.basename(sub[0]),
                                      [s if w == "{}" else w for w in sub[1:]], None, [])
                    if filtered:
                        self.parsed.deletes[before:] = [Delete(d.word, d.cwd, True) for d in
                                                        self.parsed.deletes[before:]]
                j = k + 1
            else:
                j += 1
        return starts

    def git(self, args: list[str]) -> list[str]:
        i = 0
        while i < len(args) and args[i].startswith("-"):
            i += 2 if args[i] in _GIT_GLOBAL_VALUED else 1
        if i >= len(args):
            return []
        sub, rest = args[i], args[i + 1:]
        if sub == "config":
            self.git_config(rest)
            return []
        if sub == "credential":
            self.parsed.prints_secret.append("git credential")
            return []
        if sub == "remote" and rest[:1] and rest[0] in ("add", "set-url", "set-head", "rename"):
            self.parsed.git_setup.append(f"git remote {rest[0]}")
        if sub == "submodule" and any(w in ("add", "update", "init", "sync") for w in rest[:3]):
            self.parsed.git_setup.append("git submodule")
        if sub == "grep":
            files = _operands(rest, frozenset({"-e", "-f", "-m", "-A", "-B", "-C", "-O"}))
            given = any(w in ("-e", "-f") for w in rest)
            for w in files if given else files[1:]:
                self.add("read", _rev_path(w))
        elif sub in _GIT_READ:
            for w in _operands(rest, frozenset({"-n", "-U", "-S", "-G", "--format", "-L"})):
                self.add("read", _rev_path(w))
        elif sub in _GIT_WRITE:
            for w in _operands(rest, frozenset({"-b", "-B", "-s", "--source", "-p"})):
                self.add("write", w)
        return []

    def git_config(self, rest: list[str]) -> None:
        text = " " + " ".join(rest)
        scoped = re.search(r"\s--(?:global|system)\b", text) is not None
        read = _GIT_CONFIG_READ.search(text) is not None
        dump = re.search(r"\s(?:--list|-l|list|--get-regexp|--get-urlmatch)(?=\s|=|$)", text)
        local = re.search(r"\s(?:--local|--worktree|--file|-f|--blob)(?=\s|=|$)", text)
        secret_key = re.search(r"credential|token|password|helper|insteadof", text, re.IGNORECASE)
        if read:
            if (scoped and (secret_key or dump)) or (dump and not local):
                self.parsed.prints_secret.append("prints git config that can hold credentials")
            return
        if not text.strip():
            return
        self.parsed.git_config_writes.append("credential" if scoped else "config")


def parse(command: str, cwd: str = "") -> Parsed:
    """What `command` does with the paths it names. See the module docstring."""
    segments = _segments(command)
    if segments is None:
        return Parsed(opaque=True)
    walker = _Walker(cwd)
    todo = list(segments)
    seen = 0
    while todo and seen < 64:
        seg = todo.pop(0)
        seen += 1
        if not walker.segment(seg):
            return Parsed(opaque=True)
        if walker.extra_segments:
            for extra in walker.extra_segments:
                more = _segments(extra)
                if more is None:
                    return Parsed(opaque=True)
                todo += more
            walker.extra_segments = []
    return walker.parsed
