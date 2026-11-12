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

from engine.gate import GateConfig, decide, protect


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
    assert d.protected and d.source == "model" and len(calls) == 1, path


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
    assert d.protected and d.source == "model", cmd


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
    assert d.source == "model" and d.verdict == "allow" and len(calls) == 1, cmd


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
    assert d.protected and (d.source, again.source) == ("model", "model"), cmd


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
    assert d.protected and d.source == "model", path


FINE = [
    "ls", "ls -la", "ls -la src", "pwd", "cat README.md", "head -20 a.py", "head -n 5 a.py",
    "tail -n 50 log.txt", "tail -f log.txt", "wc -l a.py", "grep -rn 'def main' engine",
    "rg -n 'foo.*bar' engine", "rg -l --hidden -g '*.py' gate",
    "rg -t py -C 3 TODO", "find . -name '*.py' -type f", "find engine -maxdepth 2 -type d",
    "which python3", "echo hello", "tree -L 2", "du -sh .", "df -h", "date", "date +%Y-%m-%d",
    "git status", "git status -s", "git status --porcelain", "git diff", "git diff --stat",
    "git diff --cached -- a.py", "git log --oneline -5", "git log -n 3 --format='%h %s'",
    "git show HEAD --stat", "git branch", "git branch -a", "git branch --show-current",
    "git branch -vv", "git rev-parse --show-toplevel", "git rev-parse --abbrev-ref HEAD",
    "git fetch", "git fetch origin", "git fetch --prune origin", "git fetch origin main",
    "git worktree list", "git remote -v", "git log --oneline origin/main..HEAD",
]


@pytest.mark.parametrize("cmd", FINE)
async def test_ordinary_reads_still_skip(tmp_path: Path, cmd: str) -> None:
    d = await _call(tmp_path, "Bash", {"command": cmd}, LIVE, judge=_judge(ASK))
    assert d.source == "skip", cmd


def test_is_simple_is_conservative_on_odd_input() -> None:
    from engine.gate.simple import is_simple

    assert not is_simple("")
    assert not is_simple("cat 'x")
    assert not is_simple("unknowncmd --flag")
    assert is_simple("unknowncmd arg")  # positional words only: the regex decides


# 9. A truncated call is never allowed outright ----------------------------------------------

async def test_model_allow_on_truncated_call_becomes_ask(tmp_path: Path) -> None:
    cmd = "echo " + "a" * 5000 + " MIDDLE " + "b" * 5000
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
