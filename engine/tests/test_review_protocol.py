"""Structured review (spec 074): the protocol run end to end with a scripted provider."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("lattice_graph")

from engine.execution.provider import Cost, ExecutionResult, ExecutionTask
from engine.review import Reviewer, load_protocol, run_review
from engine.review.parse import ReviewOut, extract_json, parse_reply
from engine.review.record import fold_run

TARGET = [("plan.md", "Step 1: drop the users table.\nStep 2: restore from backup.\nStep 3: done.")]


class Scripted:
    """An ExecutionProvider answering by (phase, agent) from a script. Records every prompt."""

    name = "scripted"
    supports_tool_use = False
    supports_pooling = False

    def __init__(self, script: dict[tuple[str, str], Any]) -> None:
        self.script = script
        self.prompts: dict[tuple[str, str], str] = {}
        self.max_tokens: dict[tuple[str, str], int] = {}

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        phase = task.metadata["phase"].removeprefix("review:")
        agent = task.metadata["agent_name"]
        self.prompts[(phase, agent)] = task.parts[0].content
        self.max_tokens[(phase, agent)] = task.metadata["max_tokens"]
        reply = self.script.get((phase, agent), {})
        text = reply if isinstance(reply, str) else json.dumps(reply)
        return ExecutionResult(
            success=True, output_path=task.output_path, content=text, provider="scripted",
            cost=Cost(input_tokens=len(task.parts[0].content) // 4, output_tokens=len(text) // 4),
        )

    async def execute_batch(self, tasks: Any) -> list[ExecutionResult]:
        return [await self.execute(t) for t in tasks]


REVIEWERS = [Reviewer("ann", "correctness"), Reviewer("bob", "risk"), Reviewer("cat", "clarity")]


def _script(overrides: dict[tuple[str, str], Any] | None = None) -> dict[tuple[str, str], Any]:
    script: dict[tuple[str, str], Any] = {
        ("review", "ann"): {"findings": [
            {"id": "F1", "sev": "block", "claim": "Drops table before backup exists", "at": "plan.md:1",
             "fix": "Back up first"},
            {"id": "F2", "sev": "minor", "claim": "Step 3 says nothing", "at": "plan.md:3"},
        ]},
        ("review", "bob"): {"findings": [
            {"id": "F1", "sev": "major", "claim": "No rollback test", "at": "plan.md:2"},
        ]},
        ("review", "cat"): "```json\n{\"findings\": []}\n```",
        ("challenge", "ann"): {"objections": [], "agree": ["bob/F1"]},
        ("challenge", "bob"): {"objections": [
            {"to": "ann/F2", "why": "Harmless; nothing to fix", "at": "plan.md:3"},
        ], "agree": ["ann/F1"]},
        ("challenge", "cat"): {"objections": [
            {"to": "bob/F1", "why": "Step 2 restores; that is the test", "at": "plan.md:2"},
        ], "agree": []},
        ("respond", "ann"): {"replies": [{"to": "bob/O1", "act": "withdraw", "why": "fair"}]},
        ("respond", "bob"): {"replies": [{"to": "cat/O1", "act": "defend",
                                          "why": "Restoring is not testing a restore"}]},
        ("arbitrate", "arbiter"): {"rulings": [{"finding": "bob/F1", "uphold": True,
                                                "why": "Untested restore"}]},
    }
    script.update(overrides or {})
    return script


async def _run(tmp_path: Path, script: dict, **kw: Any):
    provider = Scripted(script)
    result = await run_review(TARGET, provider=provider, out_dir=tmp_path, reviewers=REVIEWERS,
                              run_id="r1", **kw)
    return result, provider


@pytest.mark.asyncio
async def test_full_run_statuses_and_verdict(tmp_path: Path) -> None:
    result, provider = await _run(tmp_path, _script())
    status = {f.ref: f.status for f in result.findings}
    assert status == {"ann/F1": "stands", "ann/F2": "withdrawn", "bob/F1": "stands"}
    assert result.verdict == "block" and result.exit_code == 2
    endorsed = {f.ref: f.endorsed_by for f in result.findings}
    assert endorsed["ann/F1"] == ("bob",) and endorsed["bob/F1"] == ("ann",)
    assert next(f for f in result.findings if f.ref == "bob/F1").ruling.startswith("upheld")
    # calls: 3 reviews + 3 challenges + 2 responses + 1 arbitration; no synthesis, no pairs
    assert result.usage["calls"] == 9
    assert sorted(provider.prompts) == sorted([
        ("review", "ann"), ("review", "bob"), ("review", "cat"),
        ("challenge", "ann"), ("challenge", "bob"), ("challenge", "cat"),
        ("respond", "ann"), ("respond", "bob"), ("arbitrate", "arbiter")])


@pytest.mark.asyncio
async def test_rejected_ruling_defeats_the_finding(tmp_path: Path) -> None:
    script = _script({("arbitrate", "arbiter"): {"rulings": [
        {"finding": "bob/F1", "uphold": False, "why": "Step 2 suffices"}]}})
    result, _ = await _run(tmp_path, script)
    assert {f.ref: f.status for f in result.findings}["bob/F1"] == "defeated"
    assert result.verdict == "block"  # ann/F1 still stands


@pytest.mark.asyncio
async def test_no_arbiter_leaves_defended_finding_contested(tmp_path: Path) -> None:
    result, provider = await _run(tmp_path, _script(), arbiter=None)
    assert {f.ref: f.status for f in result.findings}["bob/F1"] == "contested"
    assert ("arbitrate", "arbiter") not in provider.prompts


@pytest.mark.asyncio
async def test_unanswered_objection_defeats(tmp_path: Path) -> None:
    script = _script({("respond", "bob"): "sorry, cannot comply"})
    result, _ = await _run(tmp_path, script)
    assert {f.ref: f.status for f in result.findings}["bob/F1"] == "defeated"
    assert result.unparsed_share > 0


@pytest.mark.asyncio
async def test_revise_replaces_the_finding(tmp_path: Path) -> None:
    script = _script({("respond", "bob"): {"replies": [
        {"to": "cat/O1", "act": "revise", "why": "narrower", "claim": "Restore never rehearsed"}]}})
    result, provider = await _run(tmp_path, script)
    status = {f.ref: f.status for f in result.findings}
    assert status["bob/F1"] == "revised" and status["bob/F1r1"] == "stands"
    assert ("arbitrate", "arbiter") not in provider.prompts


@pytest.mark.asyncio
async def test_later_phases_see_only_compact_lines(tmp_path: Path) -> None:
    _, provider = await _run(tmp_path, _script())
    challenge = provider.prompts[("challenge", "ann")]
    assert "bob/F1|major|No rollback test|plan.md:2" in challenge
    assert "ann/F1" not in challenge.split("=== END plan.md ===")[1]  # own findings not resent
    respond = provider.prompts[("respond", "bob")]
    assert "cat/O1|Step 2 restores; that is the test|plan.md:2" in respond
    assert "ann/F1" not in respond.split("=== END plan.md ===")[1]
    # every call shares one prefix (cacheable)
    prefixes = {p.split("ROLE:")[0] for p in provider.prompts.values()}
    assert len(prefixes) == 1
    assert provider.max_tokens[("review", "ann")] == load_protocol().phases["review"].max_tokens


@pytest.mark.asyncio
async def test_run_rebuilds_from_files_alone(tmp_path: Path) -> None:
    result, _ = await _run(tmp_path, _script())
    run_dir = tmp_path / "r1"
    rebuilt = fold_run(run_dir, load_protocol())
    for f in result.findings:
        assert rebuilt.status(f"r1/{f.ref}") == f.status
    graph = json.loads((run_dir / "graph.json").read_text())
    assert graph["schema"] == {"name": "deliberator-review", "version": "1.0.0"}
    review = json.loads((run_dir / "review.json").read_text())
    assert review["verdict"] == "block"
    assert (run_dir / "review.md").read_text().startswith("# Review: BLOCK")
    kinds = [json.loads(line)["kind"] for line in (run_dir / "moves.jsonl").read_text().splitlines()]
    assert "contest" in kinds and kinds.count("phase-input") == 9


@pytest.mark.asyncio
async def test_no_findings_skips_later_phases(tmp_path: Path) -> None:
    script = {("review", n): {"findings": []} for n in ("ann", "bob", "cat")}
    result, _provider = await _run(tmp_path, script)
    assert result.verdict == "pass" and result.findings == ()
    assert result.usage["calls"] == 3


@pytest.mark.asyncio
async def test_renamed_vocabulary_folds_to_same_graph(tmp_path: Path) -> None:
    """A rename is a protocol change only; the folded graph's schema types are unchanged."""
    base = load_protocol()
    renamed = base.model_copy(update={"vocabulary": base.vocabulary.model_copy(update={
        "labels": {"Issue": "Claim", "Objection": "Challenge", "Withdrawal": "Concession",
                   "Ruling": "Ruling"}})})
    a, _ = await _run(tmp_path / "a", _script())
    b, _ = await _run(tmp_path / "b", _script(), protocol=renamed)
    assert [(f.ref, f.status) for f in a.findings] == [(f.ref, f.status) for f in b.findings]
    lines = (tmp_path / "b" / "r1" / "phases" / "review" / "ann.json").read_text()
    assert json.loads(lines)["parsed"]["findings"][0]["id"] == "F1"


def test_parse_is_lenient() -> None:
    assert extract_json('Here you go:\n{"findings": []}\nThanks') == {"findings": []}
    out = parse_reply('{"findings":[{"id":"F1","sev":"Blocker","claim":"x"}]}', ReviewOut)
    assert out is not None and out.findings[0].sev == "block"
    assert parse_reply("no json here", ReviewOut) is None
