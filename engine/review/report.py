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
    duplicate_of: str | None = None
    also: tuple[str, ...] = ()


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
    same_pairs: list[tuple[str, str]] = []
    for m in moves:
        if m.kind == "agree":
            for ref in m.props.get("refs", []):
                endorsed[ref].add(str(m.props.get("agent")))
        elif m.kind == "objection":
            objections[str(m.props.get("to"))] += 1
        elif m.kind == "same":
            same_pairs.extend(m.props.get("pairs", {}).items())
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
    findings = _merge_duplicates(findings, same_pairs)
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


_STATUS_RANK: dict[Status, int] = {
    "stands": 0, "contested": 1, "revised": 2, "withdrawn": 3, "defeated": 4}


def _merge_duplicates(findings: list[Finding], pairs: Iterable[tuple[str, str]]) -> list[Finding]:
    """Group findings reviewers said are the same; the strongest member represents the group.

    Every member stays in the result (and counts toward the verdict); the others point at the
    representative with ``duplicate_of`` and the representative lists them in ``also``.
    """
    refs = {f.ref for f in findings}
    parent = {r: r for r in refs}

    def root(r: str) -> str:
        while parent[r] != r:
            parent[r] = parent[parent[r]]
            r = parent[r]
        return r

    for a, b in pairs:
        if a in refs and b in refs:
            parent[root(a)] = root(b)
    groups: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        groups[root(f.ref)].append(f)
    rep_of: dict[str, Finding] = {}
    for members in groups.values():
        rep = min(members, key=lambda f: (_STATUS_RANK[f.status], _ORDER[f.sev]))
        for f in members:
            rep_of[f.ref] = rep
    out = []
    for f in findings:
        rep = rep_of[f.ref]
        group = groups[root(f.ref)]
        if f.ref == rep.ref:
            others = tuple(g.ref for g in group if g.ref != f.ref)
            endorsers = set(f.endorsed_by).union(*(g.endorsed_by for g in group))
            endorsers.update(g.agent for g in group if g.ref != f.ref)
            endorsers.discard(f.agent)
            out.append(f.model_copy(update={"also": others, "endorsed_by": tuple(sorted(endorsers))}))
        else:
            out.append(f.model_copy(update={"duplicate_of": rep.ref}))
    return out


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
    shown = sorted((f for f in result.findings if f.status in _SHOWN and f.duplicate_of is None),
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
    dropped = [f for f in result.findings if f.status not in _SHOWN and f.duplicate_of is None]
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
