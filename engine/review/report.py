"""The result of a structured review: verdict, findings with their status, and token usage.

Rendered from the graph, never by another LLM call. ``review.json`` is the machine contract
(for CI gates and other tools); ``review.md`` is for people.
"""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from engine.review.protocol import Protocol, Severity, Verdict
from engine.review.record import Labelled, Status

RESULT_VERSION = "1.0.0"
_RANK: dict[Verdict, int] = {"pass": 0, "changes": 1, "block": 2}
_COUNTS_TOWARD_VERDICT: tuple[Status, ...] = ("stands", "contested")


class Finding(BaseModel):
    model_config = ConfigDict(frozen=True)

    ref: str
    agent: str
    sev: Severity
    claim: str
    at: str | None = None
    fix: str | None = None
    status: Status
    endorsed_by: tuple[str, ...] = ()
    objections: int = 0
    revises: str | None = None
    ruling: str | None = None


class ReviewResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    schema_version: Literal["1.0.0"] = RESULT_VERSION
    run_id: str
    run_dir: str
    protocol: str
    verdict: Verdict
    reviewers: tuple[str, ...]
    findings: tuple[Finding, ...]
    usage: dict[str, Any]
    unparsed_share: float
    problems: int

    @property
    def exit_code(self) -> int:
        """0 pass, 1 changes, 2 block: for CI gates."""
        return _RANK[self.verdict]


def _verdict(protocol: Protocol, findings: Iterable[Finding]) -> Verdict:
    worst: Verdict = "pass"
    for f in findings:
        if f.status not in _COUNTS_TOWARD_VERDICT:
            continue
        v = protocol.verdict.get(f.sev, "pass")
        if _RANK[v] > _RANK[worst]:
            worst = v
    return worst


def build_result(
    run_id: str,
    run_dir: Path,
    protocol: Protocol,
    labelled: Labelled,
    moves: Sequence[Any],
    usage: dict[str, Any],
    *,
    reviewers: Sequence[str],
) -> ReviewResult:
    prefix = f"{run_id}/"
    endorsed: dict[str, set[str]] = defaultdict(set)
    objections: dict[str, int] = defaultdict(int)
    rulings: dict[str, str] = {}
    for m in moves:
        if m.kind == "agree":
            for ref in m.props.get("refs", []):
                endorsed[ref].add(str(m.props.get("agent")))
        elif m.kind == "objection":
            objections[str(m.props.get("to"))] += 1
        elif m.kind == "ruling":
            verdict = "upheld" if m.props.get("uphold") else "rejected"
            rulings[str(m.props.get("finding"))] = f"{verdict}: {m.props.get('why')}"

    findings = []
    for m in moves:
        if m.kind not in ("finding", "revise"):
            continue
        ref = m.id.removeprefix(prefix)
        findings.append(
            Finding(
                ref=ref,
                agent=str(m.props["agent"]),
                sev=m.props.get("sev", "minor"),
                claim=str(m.props.get("claim") or ""),
                at=m.props.get("at"),
                fix=m.props.get("fix"),
                status=labelled.status(m.id),
                endorsed_by=tuple(sorted(endorsed.get(ref, ()))),
                objections=objections.get(ref, 0),
                revises=m.props.get("revises"),
                ruling=rulings.get(ref),
            )
        )
    return ReviewResult(
        run_id=run_id,
        run_dir=str(run_dir),
        protocol=protocol.protocol,
        verdict=_verdict(protocol, findings),
        reviewers=tuple(reviewers),
        findings=tuple(findings),
        usage=usage,
        unparsed_share=round(labelled.fold.unparsed_share, 4),
        problems=len(labelled.fold.problems),
    )


_ORDER = {"block": 0, "major": 1, "minor": 2}
_SHOWN: tuple[Status, ...] = ("stands", "contested")


def render_markdown(result: ReviewResult) -> str:
    u = result.usage
    lines = [
        f"# Review: {result.verdict.upper()}",
        "",
        f"Run `{result.run_id}`. Reviewers: {', '.join(result.reviewers)}. "
        f"{u.get('calls', 0)} calls, {u.get('input_tokens', 0):,} input and "
        f"{u.get('output_tokens', 0):,} output tokens"
        + (f" ({u['calls_without_usage']} calls reported no usage)." if u.get("calls_without_usage")
           else "."),
        "",
    ]
    shown = sorted((f for f in result.findings if f.status in _SHOWN),
                   key=lambda f: (_ORDER[f.sev], f.status != "stands", f.ref))
    if shown:
        lines += ["| Sev | Finding | Where | Fix | Status |", "|---|---|---|---|---|"]
        for f in shown:
            status = f.status + (f" (+{len(f.endorsed_by)})" if f.endorsed_by else "")
            lines.append(
                f"| {f.sev} | {_cell(f.claim)} | {_cell(f.at)} | {_cell(f.fix)} | {status} |"
            )
    else:
        lines.append("No findings stand.")
    dropped = [f for f in result.findings if f.status not in _SHOWN]
    if dropped:
        lines += ["", "Withdrawn, revised or defeated:", ""]
        lines += [f"- {f.ref} ({f.status}): {f.claim}" for f in dropped]
    if result.unparsed_share or result.problems:
        lines += ["", f"Unparsed replies: {result.unparsed_share:.0%}. Graph problems: {result.problems}."]
    return "\n".join(lines) + "\n"


def _cell(text: str | None) -> str:
    return (text or "").replace("|", "/").replace("\n", " ")


def write_outputs(run_dir: Path, result: ReviewResult, graph: dict[str, Any], markdown: str) -> None:
    (run_dir / "review.json").write_text(
        json.dumps(result.model_dump(mode="json"), indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (run_dir / "graph.json").write_text(
        json.dumps(graph, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (run_dir / "review.md").write_text(markdown, encoding="utf-8")
