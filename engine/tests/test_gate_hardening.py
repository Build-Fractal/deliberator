"""Gate hardening after the v2 security review: case-insensitive protected paths, quoting and
globbing in the allow-list fast path, per-command safe flags, credential reads, truncated
allows, dry-run cleanup and graph.json permissions.

"Not simple" sends a call to the judge (a model call), never straight to ask.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import pytest
from click.testing import CliRunner

from engine.gate import GateConfig, decide, prompted, protect, record

MOCK = GateConfig(provider="mock")
ASK = '{"verdict":"ask","reason":"x"}'
ALLOW = '{"verdict":"allow","reason":"ok"}'
HOME = Path.home()
# Brian's live allow-list (~/.config/deliberator/gate.yml, 2026-11-11).
LIVE_ALLOW = [
    r"^(ls|pwd|cat|head|tail|wc|grep|rg|find|which|echo|tree|du|df|date)\b",
    r"^git (status|diff|log|show|branch|rev-parse|fetch|worktree list|remote -v)\b",
]
LIVE = MOCK.model_copy(update={"allow_without_asking": LIVE_ALLOW})
# Not skipped: the judge rules ("model"), or a hard ask on a protected path ("protected").
JUDGED = ("model", "protected")


def _judge(reply: str, calls: list[str] | None = None):
    async def judge(prompt: str) -> tuple[str, int, int]:
        if calls is not None:
            calls.append(prompt)
        return reply, 1, 1
    return judge


async def _call(root: Path, tool: str, tool_input: dict, config: GateConfig = MOCK,
                cwd: Path | str | None = None, **kw):
    return await decide(root, config, tool=tool, tool_input=tool_input,
                        cwd=str(cwd or root), session="s1", push_graph=False, **kw)


def _approve(root: Path, tool: str, tool_input: dict) -> None:
    prompted(root, MOCK, tool=tool, tool_input=tool_input, session="s1")
    record(root, MOCK, tool=tool, tool_input=tool_input, session="s1", push_graph=False)


def _repo(path: Path) -> Path:
    (path / ".git").mkdir(parents=True)
    return path


# 1. Case-insensitive protected paths (APFS), `..` after a worktree, globs on dot-dirs -------

CASE_EDITS = [
    "{repo}/.Claude/settings.json",
    "{repo}/.CLAUDE/settings.local.json",
    "{repo}/.GIT/config",
    "{repo}/.Git/hooks/pre-commit",
    "{repo}/.DELIBERATOR/gate/log.jsonl",
    str(HOME / ".CLAUDE" / "settings.json"),
    str(HOME / ".Config" / "Deliberator" / "gate.yml"),
    str(HOME / ".ZSHRC"),
    "{repo}/.claude/worktrees/../settings.json",
    "{repo}/.claude/worktrees/wt/../../settings.json",
]


@pytest.mark.parametrize("path", CASE_EDITS)
async def test_case_variants_of_protected_paths_are_judged(tmp_path: Path, path: str) -> None:
    repo = _repo(tmp_path / "repo")
    path = path.format(repo=repo)
    calls: list[str] = []
    d = await _call(tmp_path, "Write", {"file_path": path, "content": "x"}, LIVE, cwd=repo,
                    judge=_judge(ALLOW, calls))
    assert d.protected and d.source in JUDGED and len(calls) == (d.source == "model"), path


def test_protected_dir_matched_by_inode(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A second name for a protected folder (case, firmlink, bind) is still protected."""
    real = tmp_path / "guarded"
    real.mkdir()
    (real / "f").write_text("x")
    alias = tmp_path / "alias"
    alias.symlink_to(real)
    # The alias is not resolved here (as with a firmlink): only the inode says it's the same.
    monkeypatch.setattr(protect, "_resolved", lambda p: p)
    assert protect.path_is_protected(str(alias / "f"), str(tmp_path), extra=[real])
    assert not protect.path_is_protected(str(tmp_path / "other"), str(tmp_path), extra=[real])


CASE_BASH = [
    "cp x $HOME/.Claude/settings.json",
    "cp x ~/.CLAUDE/settings.json",
    "cat .GIT/config",
    "git config -f .Git/config core.fsmonitor x",
    "echo x > .DELIBERATOR/gate/log.jsonl",
    "cat ~/.Local/share/Deliberator/log.jsonl",
    "cat ~/.SSH/id_ed25519",
    "cp x .claude/worktrees/../settings.json",
    "cp x .claude/worktrees/wt/../../settings.json",
    "cat ~/.cla*/settings.json",
    "cat ~/.c?aude/settings.json",
    "cat ~/.[c]laude/settings.json",
    "cat ~/.{claude,x}/settings.json",
    "cat .gi?/config",
    "ls ~/.*/",
]


@pytest.mark.parametrize("cmd", CASE_BASH)
async def test_bash_case_and_glob_variants_are_protected(tmp_path: Path, cmd: str) -> None:
    calls: list[str] = []
    d = await _call(tmp_path, "Bash", {"command": cmd},
                    MOCK.model_copy(update={"allow_without_asking": [".*"]}),
                    judge=_judge(ALLOW, calls))
    assert d.protected and d.source in JUDGED, cmd


@pytest.mark.parametrize("cmd", [
    "cd .claude/worktrees/feat && cargo test", "ls .github/workflows", "cat .gitignore",
    "ls *.py", "cat src/claude.py",
])
def test_ordinary_paths_are_not_protected(cmd: str) -> None:
    assert not protect.command_is_protected(cmd), cmd


# 2. Quoting, globbing and expansion: the fast path checks shell words, not raw text ---------

QUOTED = [
    "find . '-delete'", "find . -de''lete", "find . \"-exec\" rm x ;", "find . -ex\\ec rm x",
    "git branch '-D' main", "rg '--pre=./x' foo", "git diff '--output=f'",
    "git diff \"--output\"=f", "ls {a,b}", "cat *.py", "ls ~/.ssh*", "cat 'unclosed",
    "echo $ANTHROPIC_API_KEY", "echo \"$ANTHROPIC_API_KEY\"", "echo ${ANTHROPIC_API_KEY}",
    "cat `which x`", "echo \"`id`\"",
]


@pytest.mark.parametrize("cmd", QUOTED)
async def test_quoted_or_expanded_words_go_to_the_judge(tmp_path: Path, cmd: str) -> None:
    calls: list[str] = []
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, judge=_judge(ALLOW, calls))
    assert d.source in JUDGED and len(calls) == (d.source == "model"), cmd


# 3. Per-command safe flags; credential reads -----------------------------------------------

HARMFUL = [
    "git fetch --upload-pack='touch /tmp/pwn' origin", "git fetch --upload-pack 'sh x' origin",
    "git fetch -f origin", "git fetch origin +feat:main", "git fetch origin feat:main",
    "git branch -M main", "git branch -C feat main", "git branch -m feat main",
    "git branch newbranch", "git branch -f main HEAD~3", "git diff --ext-diff",
    "git log --textconv", "git log --output=x", "git show --ext-diff HEAD",
    "rg --hostname-bin=./x foo", "rg --pre ./x foo", "rg -z foo", "rg --search-zip foo",
    "tree -o out.txt", "tree -R -H x", "git -c core.pager=x log", "git -C .. status",
    "date 0101000026", "git remote -v add x y", "git worktree list --x", "du --fake",
]


@pytest.mark.parametrize("cmd", HARMFUL)
async def test_unknown_or_harmful_flags_go_to_the_judge(tmp_path: Path, cmd: str) -> None:
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, judge=_judge(ALLOW))
    assert d.source == "model", cmd


CREDENTIAL_BASH = [
    "cat ~/.netrc", "cat ~/.config/gh/hosts.yml", "cat $HOME/.docker/config.json",
    "cat ~/.aws/credentials", "head ~/.ssh/id_rsa", "cat .env", "cat app/.env.local",
    "cat ~/.npmrc", "cat ~/.pypirc", "cat ~/.git-credentials",
    "security find-generic-password -w -s x", "cat ~/Library/Keychains/login.keychain-db",
]


@pytest.mark.parametrize("cmd", CREDENTIAL_BASH)
async def test_credential_reads_are_judged(tmp_path: Path, cmd: str) -> None:
    allow_all = MOCK.model_copy(update={"allow_without_asking": [".*"]})
    calls: list[str] = []
    d = await _call(tmp_path, "Bash", {"command": cmd}, allow_all, judge=_judge(ALLOW, calls))
    again = await _call(tmp_path, "Bash", {"command": cmd}, allow_all, judge=_judge(ALLOW, calls))
    assert d.protected and d.source == again.source == "protected", cmd


@pytest.mark.parametrize("path", [
    str(HOME / ".netrc"), str(HOME / ".config" / "gh" / "hosts.yml"),
    str(HOME / ".docker" / "config.json"), str(HOME / ".npmrc"), str(HOME / ".pypirc"),
    "{repo}/.env", "{repo}/.env.production", str(HOME / ".git-credentials"),
    str(HOME / "Library" / "Keychains" / "login.keychain-db"),
])
async def test_credential_files_via_read_are_judged(tmp_path: Path, path: str) -> None:
    repo = _repo(tmp_path / "repo")
    d = await _call(tmp_path, "Read", {"file_path": path.format(repo=repo)},
                    MOCK.model_copy(update={"allow_without_asking": [".*"]}), cwd=repo,
                    judge=_judge(ALLOW))
    assert d.protected and d.source == "protected", path


FINE = [
    "ls", "ls -la", "ls -la src", "pwd", "cat README.md", "head -20 a.py", "head -n 5 a.py",
    "tail -n 50 log.txt", "tail -f log.txt", "wc -l a.py", "grep -n 'def main' a.py",
    "rg -n 'foo.*bar' engine", "rg -l -t py gate engine",
    "rg -t py -C 3 TODO", "find . -name '*.py' -type f", "find engine -maxdepth 2 -type d",
    "which python3", "echo hello", "tree -L 2", "du -sh .", "df -h", "date", "date +%Y-%m-%d",
    "git status", "git status -s", "git status --porcelain", "git diff", "git diff --stat",
    "git diff --cached -- a.py", "git log --oneline -5", "git log -n 3 --format='%h %s'",
    "git show HEAD --stat", "git branch", "git branch -a", "git branch --show-current",
    "git branch -vv", "git rev-parse --show-toplevel", "git rev-parse --abbrev-ref HEAD",
    "git worktree list", "git remote -v", "git log --oneline origin/main..HEAD",
]


@pytest.mark.parametrize("cmd", FINE)
async def test_ordinary_reads_still_skip(tmp_path: Path, cmd: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ASK))
    assert d.source == "skip", cmd


def test_is_simple_is_conservative_on_odd_input() -> None:
    from engine.gate.simple import is_simple

    assert not is_simple("")
    assert not is_simple("cat 'x")
    assert not is_simple("unknowncmd --flag")
    assert not is_simple("unknowncmd arg")  # unknown commands are never simple


# 9. A truncated call is never allowed outright ----------------------------------------------

async def test_model_allow_on_truncated_call_becomes_ask(tmp_path: Path) -> None:
    cmd = "echo " + "a" * 15000 + " MIDDLE " + "b" * 15000
    d = await _call(tmp_path, "Bash", {"command": cmd}, judge=_judge(ALLOW))
    assert d.truncated and d.verdict == "ask" and "truncated" in d.reason.lower()
    deny = await _call(tmp_path, "Bash", {"command": cmd + "z"},
                       judge=_judge('{"verdict":"deny","reason":"no"}'))
    assert deny.verdict == "deny"


# 12. `check --dry-run` leaves nothing behind ------------------------------------------------

def test_check_dry_run_removes_its_temp_copy(tmp_path: Path,
                                             monkeypatch: pytest.MonkeyPatch) -> None:
    import tempfile

    from engine.cli.gate import gate
    from engine.gate import config as config_mod

    user = tmp_path / "user.yml"
    user.write_text(f"provider: mock\nlog_dir: {tmp_path / 'store'}\n")
    monkeypatch.setattr(config_mod, "USER_CONFIG_PATH", user)
    log = tmp_path / "store" / ".deliberator" / "gate" / "log.jsonl"
    log.parent.mkdir(parents=True)
    log.write_text("")
    scratch = tmp_path / "tmp"
    scratch.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(scratch))
    monkeypatch.chdir(tmp_path)
    res = CliRunner().invoke(gate, ["check", "--dry-run", "-c", "make build"])
    assert res.exit_code == 0, res.output
    assert json.loads(res.output)["decision"]["verdict"]
    assert list(scratch.iterdir()) == []
    assert log.read_text() == ""


# 11. graph.json is private ------------------------------------------------------------------

async def test_graph_json_is_0600(tmp_path: Path) -> None:
    from engine.gate.core import write_graph_json

    await _call(tmp_path, "Bash", {"command": "make"}, judge=_judge(ALLOW))
    path = write_graph_json(tmp_path, MOCK)
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600


# Round 2: second-pass review bypasses. Each must reach the judge under the live allow-list.

ROUND2 = [
    # F1: assignment prefix, unknown command, `--`
    "ls=x env -- python3 -c 'import os'",
    "date=1 git push -- origin +HEAD:main",
    "ls=x GIT_SSH_COMMAND='touch /tmp/p' git fetch origin",
    "env ls", "ls-x foo",
    # F2: find predicates anywhere, after `--` too
    "find -- . -delete", "find -- . -exec sh -c id {} +", "find . -name x -- -delete",
    # F3: zsh process substitution and glob qualifiers
    "echo =(id)", "ls README.md(e:'touch /tmp/x':)", "ls =ls", "ls ^x", "ls x#",
    # F4: a valued short flag must not swallow the next one
    "git diff -U --output=~/.gitconfig",
    "git log -1 -U --output=~/.gitconfig --format='[core]%n%x09fsmonitor = touch /tmp/p'",
    "git log -n --output=x", "git show -O x HEAD", "git diff --open-files-in-pager=x",
    "git log --exec-path=/tmp", "rg -e x --pre ./y foo",
    # F5: recursive reads of a folder above a protected one
    "rg --hidden --no-ignore -i secret ~", "grep -r oauth_token ~/.config", "rg secret ~",
    "rg token ~/.config", "rg -uu token .", "ls -R ~", "tree ~/.config", "du -a ~",
    "find ~ -name hosts.yml", "find / -name x", "grep -R x ~",
    # F6: unnormalised paths, ANSI-C quoting
    "cat ~/.config//gh/hosts.yml", "cat ~/.config/./deliberator/gate.yml",
    "tail ~/.local//share/deliberator/log.jsonl", "cat ~/.config/../.netrc",
    "cat $'\\x7e'/.netrc",
    # git branch: never a write
    "git branch --format --list newbranch", "git branch --list -d x", "git branch --move a b",
    "git branch --contains x newbranch",
]


@pytest.mark.parametrize("cmd", ROUND2)
async def test_round2_bypasses_reach_the_judge(tmp_path: Path, cmd: str) -> None:
    calls: list[str] = []
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, judge=_judge(ALLOW, calls))
    assert d.source in JUDGED and len(calls) == (d.source == "model"), cmd


@pytest.mark.parametrize("cmd", [
    "cat ~/.config//gh/hosts.yml", "cat ~/.config/./deliberator/gate.yml",
    "tail ~/.local//share/deliberator/log.jsonl", "cat ~/.config/../.netrc",
    "cat $'\\x7e'/.netrc", "cat ~/*/settings.json", "cp x */settings.json",
])
def test_round2_paths_are_marked_protected(cmd: str) -> None:
    assert protect.touches_protected("Bash", {"command": cmd}, str(HOME)), cmd


async def test_recursive_read_with_no_path_uses_cwd(tmp_path: Path) -> None:
    for cmd in ("rg secret", "find . -name x", "tree", "du -sh ."):
        d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=HOME, judge=_judge(ALLOW))
        assert d.source == "model", cmd
    d = await _call(tmp_path, "Bash", {"command": "rg secret"}, LIVE, judge=_judge(ALLOW))
    assert d.source == "skip"


def test_judge_limit_is_20k() -> None:
    from engine.gate.judge import JUDGE_LIMIT

    assert JUDGE_LIMIT == 20000


def test_compound_sees_unquoted_parens_and_zsh_forms() -> None:
    from engine.gate.ledger import compound

    for cmd in ("echo =(id)", "ls README.md(e:'touch /tmp/x':)", "diff <(a) b", "(cd x)",
                "echo $(id)", "ls; id", "a | b", "x `id`"):
        assert compound(cmd), cmd
    for cmd in ("echo '(x)'", 'git log --format="%h (%s)"', "ls -la"):
        assert not compound(cmd), cmd


# Round 3 -----------------------------------------------------------------------------------

def _real_repo(path: Path) -> Path:
    """A repo git would accept: .git with HEAD, objects and refs."""
    g = path / ".git"
    (g / "objects").mkdir(parents=True)
    (g / "refs").mkdir()
    (g / "HEAD").write_text("ref: refs/heads/main\n")
    (g / "config").write_text("[core]\n\tbare = false\n")
    return path


def _bare(path: Path) -> Path:
    (path / "objects").mkdir(parents=True)
    (path / "refs").mkdir()
    (path / "HEAD").write_text("ref: refs/heads/main\n")
    (path / "config").write_text("[core]\n\tbare = true\n\tsshCommand = touch PWNED; false\n")
    return path


@pytest.mark.parametrize("cmd", [
    "rg -g '*' TOKEN", "rg -g '*env' KEY", "rg --glob '*' TOKEN", "rg --glob='*' TOKEN",
    "rg --iglob '*.ENV' KEY", "rg -n -g'*' TOKEN",
])
async def test_r3_rg_globs_reach_the_judge(tmp_path: Path, cmd: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ALLOW))
    assert d.source == "model", cmd


@pytest.mark.parametrize("cmd", [
    "git fetch origin", "git fetch", "git fetch --prune-tags --prune origin", "git fetch --all",
])
async def test_r3_git_fetch_is_never_skipped(tmp_path: Path, cmd: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ALLOW))
    assert d.source == "model", cmd


async def test_r3_git_skips_only_in_a_plain_repo_or_its_worktree(tmp_path: Path) -> None:
    repo = _real_repo(tmp_path / "repo")
    (repo / "src").mkdir()
    for cwd in (repo, repo / "src"):
        d = await _call(tmp_path, "Bash", {"command": "git status"}, LIVE, cwd=cwd,
                        judge=_judge(ALLOW))
        assert d.source == "skip", cwd
    # a worktree: .git is a file pointing into the main repo's .git/worktrees/
    wtgit = repo / ".git" / "worktrees" / "wt"
    wtgit.mkdir(parents=True)
    (wtgit / "HEAD").write_text("ref: refs/heads/wt\n")
    (wtgit / "commondir").write_text("../..\n")
    wt = tmp_path / "wt"
    wt.mkdir()
    (wt / ".git").write_text(f"gitdir: {repo / '.git' / 'worktrees' / 'wt'}\n")
    d = await _call(tmp_path, "Bash", {"command": "git log --oneline -5"}, LIVE, cwd=wt,
                    judge=_judge(ALLOW))
    assert d.source == "skip"


@pytest.mark.parametrize("where", ["bare_inside", "bare_inside_sub", "gitfile_elsewhere",
                                   "gitfile_garbage", "core_bare", "no_repo"])
async def test_r3_git_in_an_untrusted_repo_is_a_hard_ask(tmp_path: Path, where: str) -> None:
    repo = _real_repo(tmp_path / "victim")
    cwd = repo
    if where.startswith("bare_inside"):
        cwd = _bare(repo / "fx")
        if where == "bare_inside_sub":
            cwd = cwd / "objects"
    elif where.startswith("gitfile"):
        cwd = tmp_path / "x"
        cwd.mkdir()
        evil = _bare(tmp_path / "evil")
        target = evil if where == "gitfile_elsewhere" else "not a gitdir line"
        (cwd / ".git").write_text(f"gitdir: {target}\n" if where == "gitfile_elsewhere"
                                  else f"{target}\n")
    elif where == "core_bare":
        (repo / ".git" / "config").write_text("[core]\n\tbare = true\n")
    else:
        cwd = tmp_path / "plain"
        cwd.mkdir()
    calls: list[str] = []
    cmds = ("git status", "git log --oneline -5", "git diff --stat", "git fetch origin",
            "cd sub && git pull", "make test && git commit -am x")
    for cmd in cmds:
        d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=cwd,
                        judge=_judge(ALLOW, calls))
        if where == "no_repo":
            assert d.source == "model", (where, cmd)  # no repo: the judge decides
        else:
            assert (d.verdict, d.source, d.protected) == ("ask", "protected", True), (where, cmd)
    if where != "no_repo":
        assert calls == []
        # non-git commands are judged, told that the repo is untrusted
        d = await _call(tmp_path, "Bash", {"command": "make test"}, LIVE, cwd=cwd,
                        judge=_judge(ALLOW, calls))
        assert d.source == "model" and "untrusted" in calls[-1].lower()


@pytest.mark.parametrize("cmd", [
    "git log -p -- '*env'", "git show HEAD -- '*.env'", "git log -- ':(glob)**/.env'",
    "git diff -- 'a?'", "git show 'HEAD:[x]'", "git log ':(top)x'",
])
async def test_r3_git_pathspec_magic_reaches_the_judge(tmp_path: Path, cmd: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ALLOW))
    assert d.source in JUDGED, cmd


R3_CREDENTIALS = [
    str(HOME / ".gitconfig"), str(HOME / ".config" / "git" / "credentials"),
    str(HOME / ".config" / "git" / "config"), "{repo}/.envrc", str(HOME / ".zsh_history"),
    str(HOME / ".bash_history"), str(HOME / ".local" / "share" / "fish" / "fish_history"),
    str(HOME / ".cargo" / "credentials.toml"), str(HOME / ".vault-token"),
    str(HOME / ".config" / "hub"), str(HOME / ".yarnrc.yml"),
    str(HOME / ".terraform.d" / "credentials.tfrc.json"),
    str(HOME / ".cache" / "huggingface" / "token"), str(HOME / ".codex" / "auth.json"),
    str(HOME / ".m2" / "settings.xml"), str(HOME / ".gem" / "credentials"),
    str(HOME / ".azure" / "accessTokens.json"), str(HOME / ".config" / "op" / "config"),
    "{repo}/config/credentials.yml", "{repo}/sub/.gitconfig", "{repo}/.env",
    str(HOME / ".netrc"), str(HOME / ".ssh" / "id_ed25519"), str(HOME / ".aws" / "credentials"),
]


@pytest.mark.parametrize("path", R3_CREDENTIALS)
async def test_r3_credential_reads_are_a_hard_ask(tmp_path: Path, path: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    path = path.format(repo=repo)
    allow_all = MOCK.model_copy(update={"allow_without_asking": [".*"]})
    calls: list[str] = []
    for tool, ti in (("Read", {"file_path": path}), ("Bash", {"command": f"cat {path}"}),
                     ("Bash", {"command": f"head -5 '{path}'"})):
        d = await _call(tmp_path, tool, ti, allow_all, cwd=repo, judge=_judge(ALLOW, calls))
        assert (d.verdict, d.source, d.grant) == ("ask", "protected", None), (tool, path)
        _approve(tmp_path, tool, ti)
        again = await _call(tmp_path, tool, ti, allow_all, cwd=repo, judge=_judge(ALLOW, calls))
        assert (again.verdict, again.source) == ("ask", "protected"), (tool, path)
    assert calls == []  # the judge never decides a credential read


@pytest.mark.parametrize("target", [
    ("Read", {"file_path": str(HOME / ".local" / "share" / "deliberator" / ".deliberator"
                                / "gate" / "log.jsonl")}),
    ("Read", {"file_path": "{repo}/.deliberator/gate/log.jsonl"}),
    ("Read", {"file_path": "{repo}/.deliberator/gate/graph.json"}),
    ("Grep", {"pattern": "x", "path": "{repo}/.deliberator/gate"}),
    ("Bash", {"command": "tail ~/.local/share/deliberator/.deliberator/gate/log.jsonl"}),
    ("Bash", {"command": "cat .deliberator/gate/graph.json"}),
])
async def test_r3_gate_log_reads_are_a_hard_ask(tmp_path: Path, target) -> None:
    repo = _real_repo(tmp_path / "repo")
    tool, ti = target
    ti = {k: v.format(repo=repo) for k, v in ti.items()}
    calls: list[str] = []
    d = await _call(tmp_path, tool, ti, LIVE, cwd=repo, judge=_judge(ALLOW, calls))
    assert (d.verdict, d.source) == ("ask", "protected") and calls == [], ti


async def test_r3_gate_config_reads_stay_with_the_judge(tmp_path: Path) -> None:
    for tool, ti in (("Read", {"file_path": str(HOME / ".config" / "deliberator" / "gate.yml")}),
                     ("Bash", {"command": "cat ~/.config/deliberator/gate.yml"}),
                     ("Bash", {"command": "cat ~/.claude/CLAUDE.md"}),
                     ("Read", {"file_path": str(HOME / ".claude" / "settings.json")})):
        d = await _call(tmp_path, tool, ti, LIVE, judge=_judge(ALLOW))
        assert (d.verdict, d.source, d.protected) == ("allow", "model", True), ti


@pytest.mark.parametrize("target", [
    ("Write", {"file_path": str(HOME / ".claude" / "settings.json"), "content": "[]"}),
    ("Edit", {"file_path": "{repo}/.git/config", "old_string": "a", "new_string": "b"}),
    ("Write", {"file_path": "{repo}/.claude/settings.local.json", "content": "[]"}),
    ("Write", {"file_path": str(HOME / ".config" / "deliberator" / "gate.yml"),
               "content": "provider: mock\n"}),
    ("Edit", {"file_path": str(HOME / ".zshrc"), "old_string": "a", "new_string": "b"}),
    ("Bash", {"command": "cp x ~/.claude/settings.json"}),
    ("Bash", {"command": "echo x >> ~/.bashrc"}),
    ("Bash", {"command": "git config -f .git/config core.fsmonitor x"}),
    ("Bash", {"command": "rm -rf .deliberator"}),
])
async def test_r3_protected_writes_are_a_hard_ask(tmp_path: Path, target) -> None:
    repo = _real_repo(tmp_path / "repo")
    tool, ti = target
    ti = {k: v.format(repo=repo) for k, v in ti.items()}
    calls: list[str] = []
    allow_all = MOCK.model_copy(update={"allow_without_asking": [".*"]})
    d = await _call(tmp_path, tool, ti, allow_all, cwd=repo, judge=_judge(ALLOW, calls))
    assert (d.verdict, d.source) == ("ask", "protected") and calls == [], ti


async def test_r3_agent_memory_writes_stay_with_the_judge(tmp_path: Path) -> None:
    path = HOME / ".claude" / "projects" / "-p" / "memory" / "note.md"
    d = await _call(tmp_path, "Write", {"file_path": str(path), "content": "x"},
                    judge=_judge(ALLOW))
    assert (d.verdict, d.source, d.protected) == ("allow", "model", True)


def test_r3_kinds_are_explicit() -> None:
    k = protect.path_kind
    assert k(str(HOME / ".netrc")) == "credential"
    assert k(str(HOME / ".local" / "share" / "deliberator" / ".deliberator" / "gate"
                 / "log.jsonl")) == "gate_log"
    assert k("/r/.deliberator/gate/graph.json") == "gate_log"
    assert k(str(HOME / ".local" / "share" / "deliberator" / "venv" / "x")) == "config"
    assert k(str(HOME / ".claude" / "projects" / "p" / "memory" / "m.md")) == "notes"
    assert k(str(HOME / ".claude" / "settings.json")) == "config"
    assert k(str(HOME / ".config" / "deliberator" / "gate.yml")) == "config"
    assert k(str(HOME / "code" / "x.py")) is None
    for name in ("credentials", "credentials.json", "credentials.toml", "credentials.yml",
                 "credentials.yaml", "credentials.xml", "credentials.ini", "credentials.txt",
                 "credentials.conf", "credentials.tfrc.json", "credentials.json.bak"):
        assert k(f"/r/x/{name}") == "credential", name
    for name in ("credentials_test.py", "credentials.ts", "credentials.js", "credentials.go",
                 "credentials.rs", "credentials.java", "credentials.rb", "credentials.md",
                 "credentials.tsx", "credentials.kt", "credentials.swift", "credentials.c"):
        assert k(f"/r/src/{name}") is None, name


@pytest.mark.parametrize("cmd", [
    "grep -E 'passed$' log.txt | tail -1", "rg 'x$' a.py && echo done",
    "ls /private/tmp/out/*", "wc -l dir/*.py; cat x", "cat scratch/*/notes.md | head",
    "ls ~/.local/share/deliberator/venv/bin | head",
])
def test_r3_no_false_credential_or_log_hits(cmd: str) -> None:
    assert protect.access_kind("Bash", {"command": cmd}, str(HOME / "code" / "x")) in (
        None, "config"), cmd


@pytest.mark.parametrize("cmd", [
    "echo $'x' > ~/.netrc", "cat ~/*/hosts.yml", "ls $HOME/*/", ("cat ~/.local/share/"
    "deliberator/.deliberator/gate/log.jsonl | jq ."),
])
def test_r3_real_hits_stay(cmd: str) -> None:
    assert protect.access_kind("Bash", {"command": cmd}, str(HOME)) in ("credential",
                                                                        "gate_log"), cmd


async def test_r3_agent_notes_in_bash_go_to_the_judge(tmp_path: Path) -> None:
    for cmd in ("cd ~/.claude/projects/-p/memory && echo '- note' >> MEMORY.md",
                f"tail -5 {HOME}/.claude/projects/-p/abc.jsonl | jq .type",
                "ls ~/.claude/sessions | head"):
        d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, judge=_judge(ALLOW))
        assert (d.source, d.protected) == ("model", True), cmd
    d = await _call(tmp_path, "Bash", {"command": "cd ~/.claude && echo x >> settings.json"},
                    LIVE, judge=_judge(ALLOW))
    assert d.source == "protected"


@pytest.mark.parametrize("cmd", [
    "P=$HOME/.claude/projects/-p/abc.jsonl; tail -3 $P | jq .",
    "cd ~/.claude/sessions; ls | head",
    "python3 - <<'EOF'\nopen('x').write(\"cat >> ~/.claude/projects/-p/memory/n.md\")\nEOF",
    "python3 - <<'EOF'\nimport re\nre.match(r\"^a\\d+$\", x)\nEOF",
    'until grep -qE "(passed|failed).* in [0-9.]+s" /tmp/out.txt; do sleep 5; done',
])
def test_r3_notes_and_quoted_text_are_not_config_or_credential(cmd: str) -> None:
    assert protect.access_kind("Bash", {"command": cmd}, str(HOME / "code" / "x")) in (
        None, "notes"), cmd


@pytest.mark.parametrize("cmd", [
    "cat ~/.cl$'a'ude/settings.json", "cat <<EOF\n$(cat ~/.netrc)\nEOF",
    "x=~/.ssh/id_rsa; cat $x", "cd ~/.claude; cat settings.json",
])
def test_r3_protected_still_found_past_assignments_and_heredocs(cmd: str) -> None:
    assert protect.access_kind("Bash", {"command": cmd}, str(HOME)) in (
        "credential", "config"), cmd


async def test_r3_trusted_repos_still_skip_and_get_no_note(tmp_path: Path) -> None:
    repo = _real_repo(tmp_path / "repo")
    wtgit = repo / ".git" / "worktrees" / "wt"
    wtgit.mkdir(parents=True)
    (wtgit / "HEAD").write_text("ref: refs/heads/wt\n")
    (wtgit / "commondir").write_text("../..\n")
    wt = tmp_path / "wt"
    wt.mkdir()
    (wt / ".git").write_text(f"gitdir: {wtgit}\n")
    calls: list[str] = []
    for cwd in (repo, wt):
        d = await _call(tmp_path, "Bash", {"command": "git status"}, LIVE, cwd=cwd,
                        judge=_judge(ALLOW, calls))
        assert d.source == "skip", cwd
        await _call(tmp_path, "Bash", {"command": "make test"}, LIVE, cwd=cwd,
                    judge=_judge(ALLOW, calls))
    assert calls and not any("untrusted" in c.lower() for c in calls)


@pytest.mark.parametrize("cmd", ["cat src/credentials_test.py", "rg x src/credentials.ts"])
async def test_r3_credential_source_files_are_not_hard_asks(tmp_path: Path, cmd: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ALLOW))
    assert d.source != "protected", cmd


# Round 4: Claude's control files ----------------------------------------------------------

@pytest.mark.parametrize("path", [
    str(HOME / ".claude.json"), str(HOME / ".CLAUDE.json"),
    str(HOME / ".claude" / "projects" / "x" / ".claude" / "settings.json"),
    str(HOME / ".claude" / "projects" / "x" / "hooks" / "h.sh"),
    str(HOME / ".claude" / "projects" / "x" / "settings.local.json"),
    str(HOME / ".claude" / "projects" / "x" / "memory" / ".claude" / "x.md"),
    "/r/repo/.mcp.json", "/r/repo/sub/.MCP.json",
])
def test_r4_control_files_are_config(path: str) -> None:
    assert protect.path_kind(path) == "config", path


def test_r4_notes_stay_notes() -> None:
    for p in ("projects/x/memory/MEMORY.md", "projects/x/abc.jsonl", "sessions/s.json",
              "plans/p.md", "todos/t.json"):
        assert protect.path_kind(str(HOME / ".claude" / p)) == "notes", p


R4_NO_SKIP = [
    "CLAUDE.md", "docs/AGENTS.md", "sub/claude.md", "GEMINI.md", ".cursorrules",
    ".vscode/settings.json", ".idea/workspace.xml", ".devcontainer/devcontainer.json",
    ".githooks/pre-push", ".husky/pre-commit", "lefthook.yml", ".pre-commit-config.yaml",
    "mise.toml", ".mise.toml", ".tool-versions", ".yarnrc.yml", ".npmrc", "package.json",
    "Makefile", "Justfile", "Taskfile.yml", "Rakefile", "gradlew", ".cargo/config.toml",
    "pytest.ini", "setup.cfg", "pyproject.toml", "tox.ini", "conftest.py", "tests/conftest.py",
    "sitecustomize.py", "lib/x.pth", ".github/workflows/ci.yml", ".gitlab-ci.yml",
    "Jenkinsfile", "requirements.txt", "requirements-dev.txt", "reqs/requirements_test.txt",
    "venv/lib/x.py", ".venv/bin/activate", "node_modules/a/index.js",
    "lib/python3.12/site-packages/a.py",
]


@pytest.mark.parametrize("rel", R4_NO_SKIP)
async def test_r4_control_files_in_the_repo_never_skip(tmp_path: Path, rel: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    calls: list[str] = []
    d = await _call(tmp_path, "Write", {"file_path": str(repo / rel), "content": "x = 1\n"},
                    LIVE, cwd=repo, judge=_judge(ALLOW, calls))
    assert d.source in JUDGED and d.source != "skip", rel


@pytest.mark.parametrize("rel", ["src/app.py", "README.md", "docs/guide.md", "tests/test_a.py",
                                 "src/credentials_test.py", "src/requirements.py"])
async def test_r4_ordinary_files_still_skip(tmp_path: Path, rel: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    d = await _call(tmp_path, "Write", {"file_path": str(repo / rel), "content": "x = 1\n"},
                    LIVE, cwd=repo, judge=_judge(ASK))
    assert d.source == "skip", rel


# Round 5 ------------------------------------------------------------------------------------

def _evil_gitdir_of_files(path: Path) -> Path:
    """git's is_git_directory: HEAD valid, objects and refs pass access(X_OK): files do."""
    path.mkdir(parents=True)
    (path / "HEAD").write_text("ref: refs/heads/main\n")
    for name in ("objects", "refs"):
        (path / name).write_text("")
        (path / name).chmod(0o755)
    (path / "config").write_text('[core]\n\tbare = false\n\tworktree = .\n'
                                 '\tfsmonitor = "touch PWNED; echo"\n')
    return path


async def test_r5_gitdir_made_of_executable_files_is_untrusted(tmp_path: Path) -> None:
    repo = _real_repo(tmp_path / "repo")
    evil = _evil_gitdir_of_files(repo / "evil")
    (evil / "sub").mkdir()
    for cwd in (evil, evil / "sub"):
        for cmd in ("git status", "git diff", "git log"):
            d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=cwd,
                            judge=_judge(ALLOW))
            assert (d.verdict, d.source) == ("ask", "protected"), (cwd, cmd)


@pytest.mark.parametrize("cmd", [
    "rg SECRET", "rg --files", "rg -n SECRET .", "rg SECRET src", "rg -e SECRET",
    "rg . ~/.pulumi", "rg . ~/.local/share/fish",
])
async def test_r5_recursive_rg_reaches_the_judge(tmp_path: Path, cmd: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    (repo / "src").mkdir()
    (repo / ".rgignore").write_text("!.env\n!.git/\n!.deliberator/\n")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ALLOW))
    assert d.source in JUDGED, cmd


async def test_r5_rg_on_named_files_still_skips(tmp_path: Path) -> None:
    repo = _real_repo(tmp_path / "repo")
    (repo / "a.py").write_text("x\n")
    (repo / "b.py").write_text("y\n")
    for cmd in ("rg -n x a.py", "rg x a.py b.py", "rg -e x a.py"):
        d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ASK))
        assert d.source == "skip", cmd


def test_r5_recursive_listing_honours_log_dir(tmp_path: Path) -> None:
    from engine.gate.simple import simple_words

    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    assert simple_words(f"find {tmp_path} -name x", str(tmp_path)) is not None
    assert simple_words(f"find {tmp_path} -name x", str(tmp_path), extra=[log_dir]) is None


@pytest.mark.parametrize("cmd", [
    "git -C evil status", "cd evil && git status", "cd evil; git log", "git --git-dir=evil status",
    "git --work-tree=evil --git-dir=evil status", "pushd evil && git diff",
])
async def test_r5_git_targeting_an_untrusted_repo_is_a_hard_ask(tmp_path: Path, cmd: str) -> None:
    repo = _real_repo(tmp_path / "repo")
    _bare(repo / "evil")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=repo, judge=_judge(ALLOW))
    assert (d.verdict, d.source) == ("ask", "protected"), cmd


async def test_r5_non_git_into_untrusted_repo_gets_the_note(tmp_path: Path) -> None:
    repo = _real_repo(tmp_path / "repo")
    _bare(repo / "evil")
    calls: list[str] = []
    d = await _call(tmp_path, "Bash", {"command": "cd evil && make"}, LIVE, cwd=repo,
                    judge=_judge(ALLOW, calls))
    assert d.source == "model" and "untrusted" in calls[-1].lower()


@pytest.mark.parametrize("cmd", ['"git" status', "'git' log", "=git status", "g''it status",
                                 "\\git status", "command git status"])
async def test_r5_disguised_git_in_an_untrusted_repo_is_a_hard_ask(tmp_path: Path,
                                                                    cmd: str) -> None:
    cwd = _bare(tmp_path / "evil")
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, cwd=cwd, judge=_judge(ALLOW))
    assert (d.verdict, d.source) == ("ask", "protected"), cmd


@pytest.mark.parametrize(("cmd", "kind"), [
    ("git config core.fsmonitor ./x.sh", "config"),
    ("git config --add core.hooksPath x", "config"),
    ("git config set core.pager x", "config"),
    ("git -C sub config core.sshCommand x", "config"),
    ("git remote add evil https://x.example/r", "config"),
    ("git remote set-url origin https://x.example/r", "config"),
    ("git submodule add https://x.example/r sub", "config"),
    ("git worktree add ../wt -b wt", "config"),
    ("git config --global credential.helper x", "credential"),
    ("git config --system core.editor x", "credential"),
    ("git config --global --get user.name", "credential"),
    ("git credential fill", "credential"), ("gh auth token", "credential"),
    ("op read op://vault/item/field", "credential"),
    ("gcloud auth print-access-token", "credential"),
    ("gcloud auth print-identity-token", "credential"),
    ("aws configure export-credentials --profile p", "credential"),
    ("aws configure get aws_secret_access_key", "credential"),
    ("env", "credential"), ("printenv", "credential"), ("env | sort", "credential"),
    ("printenv ANTHROPIC_API_KEY", "credential"), ("printenv GITHUB_TOKEN", "credential"),
])
def test_r5_config_writes_and_secret_printers(cmd: str, kind: str) -> None:
    assert protect.access_kind("Bash", {"command": cmd}, "/r") == kind, cmd


@pytest.mark.parametrize("cmd", ["git config --get user.name", "git config --list",
                                 "git config -l", "git config get user.email",
                                 "git remote -v", "printenv PATH", "env FOO=1 make",
                                 "git worktree list"])
def test_r5_harmless_git_config_and_env_reads(cmd: str) -> None:
    assert protect.access_kind("Bash", {"command": cmd}, "/r") is None, cmd


async def test_r5_config_writes_are_hard_asks(tmp_path: Path) -> None:
    repo = _real_repo(tmp_path / "repo")
    d = await _call(tmp_path, "Bash", {"command": "git config core.fsmonitor ./x.sh"}, LIVE,
                    cwd=repo, judge=_judge(ALLOW))
    assert (d.verdict, d.source) == ("ask", "protected")
