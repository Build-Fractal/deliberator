"""deliberator gate: decisions, precedent, approvals, hook output, graph."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from engine.gate import GateConfig, decide, hook_output, prompted, record
from engine.gate.judge import build_prompt, parse_ruling
from engine.gate.ledger import read, similar

MOCK = GateConfig(provider="mock")


def _judge(reply: str, calls: list[str] | None = None):
    async def judge(prompt: str) -> tuple[str, int, int]:
        if calls is not None:
            calls.append(prompt)
        return reply, 10, 5
    return judge


async def _bash(root: Path, cmd: str, config: GateConfig = MOCK, **kw):
    return await decide(root, config, tool="Bash", tool_input={"command": cmd},
                        cwd=str(root), session="s1", push_graph=False, **kw)


async def test_deny_carries_reason_and_rule(tmp_path: Path) -> None:
    d = await _bash(tmp_path, "git push --force origin main")
    out = hook_output(d, MOCK)["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny"
    assert "rule 2" in out["permissionDecisionReason"]
    assert read(tmp_path).decisions[-1].id == d.id


async def test_allow_list_skips_the_model(tmp_path: Path) -> None:
    calls: list[str] = []
    cfg = MOCK.model_copy(update={"allow_without_asking": [r"^git status\b"]})
    d = await _bash(tmp_path, "git status -s", cfg, judge=_judge("{}", calls))
    assert (d.verdict, d.source, calls) == ("allow", "skip", [])


async def test_identical_call_reuses_the_ruling(tmp_path: Path) -> None:
    calls: list[str] = []
    j = _judge('{"verdict":"deny","reason":"no","rule":1}', calls)
    first = await _bash(tmp_path, "rm -rf src", judge=j)
    again = await _bash(tmp_path, "rm -rf src", judge=j)
    assert len(calls) == 1
    assert again.source == "reuse" and again.verdict == "deny"
    assert again.precedents == (first.id,)


async def test_rules_change_invalidates_reuse(tmp_path: Path) -> None:
    calls: list[str] = []
    j = _judge('{"verdict":"allow","reason":"ok"}', calls)
    await _bash(tmp_path, "make deploy", judge=j)
    cfg = MOCK.model_copy(update={"rules": ["Deny deploys."]})
    await _bash(tmp_path, "make deploy", cfg, judge=j)
    assert len(calls) == 2


async def test_approved_ask_becomes_allow(tmp_path: Path) -> None:
    calls: list[str] = []
    j = _judge('{"verdict":"ask","reason":"publishes"}', calls)
    asked = await _bash(tmp_path, "git push origin feat/x", judge=j)
    assert asked.verdict == "ask"
    prompted(tmp_path, MOCK, tool="Bash", tool_input={"command": "git push origin feat/x"},
             session="s1")
    record(tmp_path, MOCK, tool="Bash", tool_input={"command": "git push origin feat/x"},
           session="s1", push_graph=False)
    assert read(tmp_path).approved(asked)
    again = await _bash(tmp_path, "git push origin feat/x", judge=j)
    assert (again.verdict, again.source) == ("allow", "approved")
    assert len(calls) == 1


async def test_unapproved_ask_is_asked_again(tmp_path: Path) -> None:
    calls: list[str] = []
    j = _judge('{"verdict":"ask","reason":"publishes"}', calls)
    await _bash(tmp_path, "git push origin feat/y", judge=j)
    await _bash(tmp_path, "git push origin feat/y", judge=j)
    assert len(calls) == 2  # an ask is not reused: the person never said yes


async def test_precedent_reaches_the_prompt(tmp_path: Path) -> None:
    await _bash(tmp_path, "git push --force origin main")
    calls: list[str] = []
    await _bash(tmp_path, "git push --force origin release",
                judge=_judge('{"verdict":"deny","reason":"x"}', calls))
    assert "git push --force origin main" in calls[0]
    assert "PRECEDENT" in calls[0]


async def test_judge_failure_asks(tmp_path: Path) -> None:
    async def broken(prompt: str) -> tuple[str, int, int]:
        raise ConnectionError("no route")

    d = await _bash(tmp_path, "ls", judge=broken)
    assert (d.verdict, d.source) == ("ask", "error")
    nonsense = await _bash(tmp_path, "pwd", judge=_judge("sure, go ahead"))
    assert nonsense.verdict == "ask"


async def test_errors_are_never_reused(tmp_path: Path) -> None:
    async def broken(prompt: str) -> tuple[str, int, int]:
        raise TimeoutError

    await _bash(tmp_path, "make", judge=broken)
    d = await _bash(tmp_path, "make", judge=_judge('{"verdict":"allow","reason":"ok"}'))
    assert d.verdict == "allow" and d.source == "model"


def test_parse_ruling() -> None:
    assert parse_ruling('```json\n{"verdict":"DENY","reason":"bad","rule":2}\n```') == (
        "deny", "bad", 2)
    assert parse_ruling('{"verdict":"maybe"}') is None
    assert parse_ruling('{"verdict":"allow","rule":true}') == ("allow", "(no reason given)",
                                                               None)


def test_similar_prefers_same_tool_and_approvals(tmp_path: Path) -> None:
    history = read(tmp_path)
    assert similar(history, tool="Bash", subject="x", cwd="/", k=3) == []


def test_prompt_numbers_rules() -> None:
    p = build_prompt(MOCK, tool="Bash", subject="ls", cwd="/p", precedents=[],
                     history=read(Path("/nonexistent")))
    assert "1. Never lose work" in p and "(none)" in p


async def test_graph_projection_and_push(tmp_path: Path) -> None:
    pytest.importorskip("lattice_graph")
    from engine.gate.graph import node_link, push

    a = await _bash(tmp_path, "git push --force origin main")
    b = await _bash(tmp_path, "git push --force origin dev")
    history = read(tmp_path)
    graph = node_link(history, MOCK)
    labels = {n["label"] for n in graph["nodes"]}
    assert labels == {"GateDecision", "GateCall", "GateRule", "GateSession"}
    assert b.precedents == (a.id,)

    ran: list[tuple[str, dict]] = []

    class Session:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def run(self, cypher: str, params: dict) -> None:
            ran.append((cypher, params))

    n = push(history.decisions, history, MOCK, session_factory=Session)
    assert n == len(ran) and n > 0
    assert any("FOLLOWS" in c for c, _ in ran)
    assert all("MERGE" in c for c, _ in ran)


def test_hook_command_always_answers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from engine.cli.gate import gate
    from engine.gate import config as config_mod

    user = tmp_path / "user.yml"
    user.write_text("provider: mock\n")
    monkeypatch.setattr(config_mod, "USER_CONFIG_PATH", user)
    (tmp_path / ".deliberator").mkdir()
    runner = CliRunner()
    event = {"cwd": str(tmp_path), "tool_name": "Bash", "session_id": "s",
             "tool_input": {"command": "git push --force origin main"}}
    out = json.loads(runner.invoke(gate, ["hook"], input=json.dumps(event)).output)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    bad = json.loads(runner.invoke(gate, ["hook"], input="not json").output)
    assert bad["hookSpecificOutput"]["permissionDecision"] == "ask"
    user.write_text("provider: nonsense\n")
    cfg_err = json.loads(runner.invoke(gate, ["hook"], input=json.dumps(event)).output)
    assert cfg_err["hookSpecificOutput"]["permissionDecision"] == "ask"


async def test_edits_inside_the_folder_skip_the_model(tmp_path: Path) -> None:
    calls: list[str] = []
    j = _judge('{"verdict":"ask","reason":"x"}', calls)

    (tmp_path / ".git").mkdir()  # edits skip the judge only inside a git repository

    async def edit(path: str):
        return await decide(tmp_path, MOCK, tool="Edit", tool_input={"file_path": path},
                            cwd=str(tmp_path), session="s1", push_graph=False, judge=j)

    assert (await edit(str(tmp_path / "src" / "a.py"))).source == "skip"
    assert (await edit("src/b.py")).source == "skip"
    assert (await edit(str(tmp_path / ".git" / "config"))).source == "model"
    assert (await edit("/etc/hosts")).source == "model"
    assert (await edit(str(tmp_path / ".." / "other" / "x"))).source == "model"
    assert len(calls) == 3


def test_user_config_and_shared_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from engine.gate import config as config_mod

    user = tmp_path / "user" / "gate.yml"
    user.parent.mkdir()
    user.write_text(f"provider: mock\nlog_dir: {tmp_path / 'shared'}\n")
    monkeypatch.setattr(config_mod, "USER_CONFIG_PATH", user)
    project = tmp_path / "proj"
    project.mkdir()
    cfg = config_mod.load_config(project)
    assert cfg.provider == "mock" and cfg.store_root(project) == tmp_path / "shared"
    (project / ".deliberator").mkdir()
    (project / ".deliberator" / "gate.yml").write_text(
        "provider: claude-code\nlog_dir: /elsewhere\n")
    assert config_mod.load_config(project).provider == "mock"  # not opted in: ignored
    user.write_text(f"provider: mock\nlog_dir: {tmp_path / 'shared'}\n"
                    "allow_project_config: true\n")
    cfg = config_mod.load_config(project)
    assert cfg.provider == "claude-code"
    assert cfg.store_root(project) == tmp_path / "shared"  # a project can't move the log


async def test_approved_grant_covers_calls_of_the_same_kind(tmp_path: Path) -> None:
    from engine.gate.ledger import Revoke, append, now

    calls: list[str] = []
    grant = r"^echo \w+ >> ~/notes/[\w.-]+$"
    j = _judge(json.dumps({"verdict": "ask", "reason": "writes memory", "grant": grant}),
               calls)
    asked = await _bash(tmp_path, "echo a >> ~/notes/x.md", judge=j)
    assert asked.grant == grant
    assert "kept forever" in hook_output(asked, MOCK)["hookSpecificOutput"][
        "permissionDecisionReason"]
    prompted(tmp_path, MOCK, tool="Bash", tool_input={"command": "echo a >> ~/notes/x.md"},
             session="s1")
    record(tmp_path, MOCK, tool="Bash", tool_input={"command": "echo a >> ~/notes/x.md"},
           session="s1", push_graph=False)
    other = await _bash(tmp_path, "echo b >> ~/notes/y.md", judge=j)
    assert (other.verdict, other.source, len(calls)) == ("allow", "approved", 1)
    append(tmp_path, Revoke(decision=asked.id, at=now()))
    again = await _bash(tmp_path, "echo c >> ~/notes/z.md", judge=j)
    assert again.verdict == "ask" and len(calls) == 2


def test_grant_patterns_must_be_narrow() -> None:
    from engine.gate.judge import parse_grant

    def reply(g: str) -> str:
        return json.dumps({"verdict": "ask", "reason": "r", "grant": g})

    narrow = "^npm publish( --dry)?$"
    assert parse_grant(reply(narrow), "npm publish --dry") == narrow
    assert parse_grant(reply("^npm publish\\b"), "npm publish --dry") is None  # riders
    assert parse_grant(reply(".*"), "anything") is None  # not anchored
    assert parse_grant(reply("^.*"), "anything") is None  # matches everything
    assert parse_grant(reply("^git push"), "rm -rf x") is None  # does not cover the call
    assert parse_grant(reply("^(unclosed"), "x") is None


async def test_allow_list_does_not_cover_redirects_or_chains(tmp_path: Path) -> None:
    cfg = MOCK.model_copy(update={"allow_without_asking": [r"^(cat|echo|ls)\b"]})
    j = _judge('{"verdict":"ask","reason":"x"}')
    for cmd in ("cat a > b", "echo x >> ~/.bashrc", "ls; rm -rf src", "cat $(whoami)",
                "ls && git push", "cat x | sh"):
        d = await _bash(tmp_path, cmd, cfg, judge=j)
        assert d.source == "model", cmd
    assert (await _bash(tmp_path, "cat README.md", cfg, judge=j)).source == "skip"


async def test_secrets_never_reach_the_log(tmp_path: Path) -> None:
    from engine.gate.ledger import LOG_PATH, scrub

    cmd = "curl -H 'Authorization: Bearer abcdef123456789' https://api.example.com --token=s3cr3tvalue"
    d = await _bash(tmp_path, cmd, judge=_judge('{"verdict":"allow","reason":"ok"}'))
    text = (tmp_path / LOG_PATH).read_text()
    assert "abcdef123456789" not in text and "s3cr3tvalue" not in text
    assert "[REDACTED]" in d.subject
    assert oct((tmp_path / LOG_PATH).stat().st_mode)[-3:] == "600"
    record(tmp_path, MOCK, tool="Bash", tool_input={"command": cmd}, session="s1",
           push_graph=False)
    assert read(tmp_path).ran == {d.id}
    # an old unredacted line is cleaned by scrub
    raw = {"kind": "decision", "id": "x", "at": "t", "tool": "Bash", "cwd": "/", "key": "k",
           "subject": "export AWS_SECRET_ACCESS_KEY=abcdEFGHijklMNOPqrst1234", "verdict": "allow",
           "reason": "r", "rules_hash": "h", "source": "model"}
    with (tmp_path / LOG_PATH).open("a") as fh:
        fh.write(json.dumps(raw) + "\n")
    assert scrub(tmp_path)[0] == 1
    assert "abcdEFGHijklMNOPqrst1234" not in (tmp_path / LOG_PATH).read_text()
