"""A review run's record: phase envelopes plus a move log, folded into an argument graph.

Storage follows the spec 074 verdict:

- ``phases/<phase>/<agent>.json``: one envelope per agent reply, holding the raw text and what
  was parsed from it. This is the source of truth for what each agent said.
- ``moves.jsonl``: moves that belong to no phase envelope (engine moves such as opening a
  contest when a finding is defended, phase-input and usage records).
- The graph is always rebuilt from those two by :func:`fold_run`. It is never edited.

Move ids are ``<run>/<agent>/<local>`` (opaque, no type names). Words come from the protocol
vocabulary; aliases are applied only by the fold.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from engine.review.parse import (
    ArbitrateOut,
    ChallengeOut,
    RespondOut,
    ReviewOut,
    clip,
    valid_local_id,
    valid_ref,
)
from engine.review.protocol import Protocol

ENVELOPE_VERSION = "1.0.0"
PHASE_ORDER = ("review", "challenge", "respond", "arbitrate")
ENGINE = "engine"

Status = Literal["stands", "withdrawn", "revised", "defeated", "contested"]

_MODELS = {
    "review": ReviewOut,
    "challenge": ChallengeOut,
    "respond": RespondOut,
    "arbitrate": ArbitrateOut,
}


def _graph() -> Any:
    try:
        import lattice_graph  # noqa: F401
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise ImportError(
            "Structured review needs lattice-graph, which is not on PyPI: run "
            "scripts/lattice-wheel.sh --install in the deliberator repo"
        ) from exc
    from lattice_graph import argument, build, moves, schema

    return argument, build, moves, schema


def review_schema(protocol: Protocol) -> Any:
    argument, _, _, schema = _graph()
    return schema.combine(
        argument.ARGUMENT_SCHEMA, name=f"deliberator-{protocol.protocol}", version=protocol.schema_version
    )


def vocabulary(protocol: Protocol) -> Any:
    _, _, moves, _ = _graph()
    return moves.Vocabulary(labels=protocol.vocabulary.labels, edges=protocol.vocabulary.edges)


# ---------------------------------------------------------------------------
# Envelopes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Envelope:
    run: str
    phase: str
    agent: str
    raw: str
    parsed: dict[str, Any] | None
    props: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": ENVELOPE_VERSION,
            "run": self.run,
            "phase": self.phase,
            "agent": self.agent,
            "props": self.props,
            "parsed": self.parsed,
            "raw": self.raw,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Envelope:
        return cls(
            run=data["run"],
            phase=data["phase"],
            agent=data["agent"],
            raw=data.get("raw", ""),
            parsed=data.get("parsed"),
            props=dict(data.get("props") or {}),
        )

    def model(self) -> Any:
        if self.parsed is None:
            return None
        return _MODELS[self.phase].model_validate(self.parsed)


def write_envelope(run_dir: Path, env: Envelope) -> Path:
    path = run_dir / "phases" / env.phase / f"{env.agent}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(env.to_json(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def read_envelopes(run_dir: Path) -> list[Envelope]:
    out: list[Envelope] = []
    for phase in PHASE_ORDER:
        for path in sorted((run_dir / "phases" / phase).glob("*.json")):
            out.append(Envelope.from_json(json.loads(path.read_text(encoding="utf-8"))))
    return out


# ---------------------------------------------------------------------------
# Envelopes -> moves
# ---------------------------------------------------------------------------


def objection_ref(agent: str, n: int) -> str:
    return f"{agent}/O{n}"


def envelope_moves(env: Envelope, protocol: Protocol) -> Iterator[Any]:
    """The moves one envelope stands for. Deterministic, so the graph can always be rebuilt."""
    _, _, moves, _ = _graph()
    Move, MoveEdge = moves.Move, moves.MoveEdge
    run, agent, words = env.run, env.agent, protocol.text_words
    author = f"{run}/{agent}"
    base = {"agent": agent, **{k: v for k, v in env.props.items() if k in ("config", "role")}}
    w = protocol.word

    def mid(local: str) -> str:
        return f"{run}/{local}" if "/" in local else f"{run}/{agent}/{local}"

    model = env.model() if env.parsed is not None else None
    if model is None:
        yield Move(id=f"{author}/{env.phase}-unparsed", author=author, kind="unparsed",
                   via="agent", props={**base, "phase": env.phase}, payload=env.raw)
        return

    if env.phase == "review":
        seen: set[str] = set()
        for f in model.findings[: protocol.phases["review"].max_items]:
            if not valid_local_id(f.id) or f.id in seen:
                continue
            seen.add(f.id)
            yield Move(
                id=mid(f.id), author=author, kind="finding", label=w("Claim"),
                props={**base, "sev": f.sev, "claim": clip(f.claim, words), "at": f.at,
                       "fix": clip(f.fix, words)},
            )

    elif env.phase == "challenge":
        cap = protocol.phases["challenge"].max_items or len(model.objections)
        for n, o in enumerate(model.objections[:cap], start=1):
            if not valid_ref(o.to) or o.to.split("/")[0] == agent:
                continue
            yield Move(
                id=f"{run}/{objection_ref(agent, n)}", author=author, kind="objection",
                label=w("Challenge"),
                edges=(MoveEdge(type=w("ATTACKS", edge=True), target=mid(o.to)),),
                props={**base, "to": o.to, "why": clip(o.why, words), "at": o.at},
            )
        agree = sorted({r for r in model.agree if valid_ref(r) and r.split("/")[0] != agent})
        if agree:
            yield Move(id=f"{author}/agree", author=author, kind="agree", props={**base, "refs": agree})
        same = {k: f"{agent}/{v}" for k, v in sorted(model.same.items())
                if valid_ref(k) and k.split("/")[0] != agent and valid_local_id(v)}
        if same:
            yield Move(id=f"{author}/same", author=author, kind="same", props={**base, "pairs": same})

    elif env.phase == "respond":
        revised_once: set[str] = set()
        for n, r in enumerate(model.replies, start=1):
            if not valid_ref(r.to):
                continue
            objection = mid(r.to)
            target = env.props.get("objected", {}).get(r.to)
            if target is None:  # a reply to an objection this agent wasn't shown
                continue
            finding = mid(target)
            why = clip(r.why, words)
            if r.act == "withdraw":
                yield Move(
                    id=f"{author}/W{n}", author=author, kind="withdraw", label=w("Concession"),
                    edges=(MoveEdge(type=w("CONCEDES", edge=True), target=finding),
                           MoveEdge(type="RESPONDS_TO", target=objection)),
                    props={**base, "why": why},
                )
            elif r.act == "defend":
                rebuttal = f"{author}/R{n}"
                yield Move(
                    id=rebuttal, author=author, kind="defend", label=w("Claim"),
                    edges=(MoveEdge(type=w("ATTACKS", edge=True), target=objection),
                           MoveEdge(type="RESPONDS_TO", target=objection)),
                    props={**base, "why": why},
                )
            else:  # revise: one revision per finding; later revise replies to it are dropped
                if finding in revised_once:
                    continue
                revised_once.add(finding)
                revised = f"{finding}r{n}"
                old = env.props.get("findings", {}).get(target, {})
                yield Move(
                    id=revised, author=author, kind="revise", label=w("Claim"),
                    edges=(MoveEdge(type=w("SUPERSEDES", edge=True), target=finding),
                           MoveEdge(type="RESPONDS_TO", target=objection)),
                    props={**base, "sev": old.get("sev", "minor"),
                           "claim": clip(r.claim or why, words), "at": old.get("at"),
                           "fix": old.get("fix"), "revises": target},
                )
                yield Move(
                    id=f"{author}/W{n}", author=author, kind="withdraw", label=w("Concession"),
                    edges=(MoveEdge(type=w("CONCEDES", edge=True), target=finding),),
                    props={**base, "why": "revised"},
                )

    elif env.phase == "arbitrate":
        threads: Mapping[str, Mapping[str, Any]] = env.props.get("threads", {})
        for n, ruling in enumerate(model.rulings, start=1):
            thread = threads.get(ruling.finding)
            if thread is None:
                continue
            finding = mid(ruling.finding)
            edges = []
            for pair in thread["pairs"]:  # [objection ref, rebuttal ref or null]
                objection = mid(pair[0])
                rebuttal = mid(pair[1]) if pair[1] else None
                if ruling.uphold:
                    edges.append(MoveEdge(type=w("PREFERS", edge=True), target=finding,
                                          key=objection, props={"over": objection}))
                    if rebuttal:
                        edges.append(MoveEdge(type=w("PREFERS", edge=True), target=rebuttal,
                                              key=objection, props={"over": objection}))
                else:
                    edges.append(MoveEdge(type=w("PREFERS", edge=True), target=objection,
                                          key=finding, props={"over": finding}))
                    if rebuttal:
                        edges.append(MoveEdge(type=w("PREFERS", edge=True), target=objection,
                                              key=rebuttal, props={"over": rebuttal}))
            yield Move(
                id=f"{author}/J{n}", author=author, kind="ruling", label=w("Ruling"),
                edges=tuple(edges),
                props={**base, "finding": ruling.finding, "uphold": ruling.uphold,
                       "why": clip(ruling.why, words)},
            )


def contest_move(run: str, objection: str, rebuttal: str) -> Any:
    """Engine move: a defended objection still stands against the defence until someone rules.

    Without it the last word would always win (an unattacked rebuttal is IN), so every defence
    would beat every objection. The mutual attack leaves both UNDEC: contested.
    """
    _, _, moves, _ = _graph()
    return moves.Move(
        id=f"{run}/{ENGINE}/contest:{objection}", author=f"{run}/{ENGINE}", kind="contest",
        via="engine",
        edges=(moves.MoveEdge(type="ATTACKS", source=f"{run}/{objection}", target=f"{run}/{rebuttal}"),),
    )


# ---------------------------------------------------------------------------
# Fold and labelling
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Labelled:
    fold: Any
    labels: dict[str, str]
    conceded: frozenset[str]
    superseded: frozenset[str]

    def status(self, key: str) -> Status:
        if key in self.superseded:
            return "revised"
        if key in self.conceded:
            return "withdrawn"
        return {"in": "stands", "out": "defeated", "undec": "contested"}.get(
            self.labels.get(key, "undec"), "contested"
        )


def all_moves(envelopes: Iterable[Envelope], log: Iterable[Any], protocol: Protocol) -> list[Any]:
    out: list[Any] = []
    for env in envelopes:
        out.extend(envelope_moves(env, protocol))
    out.extend(log)
    return out


def label(moves_: Iterable[Any], protocol: Protocol) -> Labelled:
    argument, _, moves, _ = _graph()
    folded = moves.fold(moves_, review_schema(protocol), vocabulary(protocol))
    projection = folded.projection
    labels = argument.grounded(argument.from_projection(projection))
    superseded = frozenset(e.target for e in projection.edges if e.type == "SUPERSEDES")
    return Labelled(
        fold=folded, labels=labels, conceded=argument.conceded(projection), superseded=superseded
    )


def read_log(run_dir: Path) -> list[Any]:
    _, _, moves, _ = _graph()
    path = run_dir / "moves.jsonl"
    if not path.exists():
        return []
    parsed, _problems = moves.parse_log(path.read_text(encoding="utf-8"))
    return list(parsed)


def append_log(run_dir: Path, items: Iterable[Any]) -> None:
    _, _, moves, _ = _graph()
    path = run_dir / "moves.jsonl"
    with path.open("a", encoding="utf-8") as f:
        for move in items:
            f.write(moves.dump_move(move) + "\n")


def fold_run(run_dir: Path, protocol: Protocol) -> Labelled:
    """Rebuild the graph and labels from a run directory's files alone."""
    return label(all_moves(read_envelopes(run_dir), read_log(run_dir), protocol), protocol)


def graph_json(labelled: Labelled, protocol: Protocol) -> dict[str, Any]:
    _, build, _, _ = _graph()
    return build.node_link(labelled.fold.projection, review_schema(protocol))
