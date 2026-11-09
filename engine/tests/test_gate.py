"""deliberator gate: decisions, precedent, approvals, hook output, graph."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from engine.gate import GateConfig, decide, hook_output, record
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
    assert "1. Deny anything that deletes" in p and "(none)" in p


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


def test_hook_command_always_answers(tmp_path: Path) -> None:
    from engine.cli.gate import gate

    (tmp_path / ".deliberator").mkdir()
    (tmp_path / ".deliberator" / "gate.yml").write_text("provider: mock\n")
    runner = CliRunner()
    event = {"cwd": str(tmp_path), "tool_name": "Bash", "session_id": "s",
             "tool_input": {"command": "git push --force origin main"}}
    out = json.loads(runner.invoke(gate, ["hook"], input=json.dumps(event)).output)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    bad = json.loads(runner.invoke(gate, ["hook"], input="not json").output)
    assert bad["hookSpecificOutput"]["permissionDecision"] == "ask"
    (tmp_path / ".deliberator" / "gate.yml").write_text("provider: nonsense\n")
    cfg_err = json.loads(runner.invoke(gate, ["hook"], input=json.dumps(event)).output)
    assert cfg_err["hookSpecificOutput"]["permissionDecision"] == "ask"
