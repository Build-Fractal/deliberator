"""Run a structured review: review -> challenge -> respond -> arbitrate (only if needed).

Calls for N reviewers: N reviews, N challenges (not N(N-1) pair cross-reviews), at most N
responses (only reviewers who were objected to), and at most one arbitration (only when a
finding is still contested). There is no synthesis call: the report is rendered from the graph.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from engine.dispatch import dispatch_phase
from engine.events import (
    AgentCompleted,
    CallbackEmitter,
    EngineEvent,
    EventEmitter,
    NullEmitter,
)
from engine.review import prompts
from engine.review.parse import (
    ArbitrateOut,
    ChallengeOut,
    RespondOut,
    ReviewOut,
    parse_reply,
)
from engine.review.protocol import Protocol, load_protocol
from engine.review.record import (
    ENGINE,
    Envelope,
    all_moves,
    append_log,
    contest_move,
    graph_json,
    label,
    write_envelope,
)
from engine.review.report import (
    ReviewResult,
    build_result,
    render_markdown,
    write_outputs,
)

DEFAULT_LENSES: tuple[tuple[str, str], ...] = (
    ("correctness", "is it right: logic, facts, edge cases, broken promises"),
    ("risk", "what fails in use: security, data loss, misuse, operational risk"),
    ("clarity", "can the intended reader use it: gaps, ambiguity, missing steps"),
)


@dataclass(frozen=True)
class Reviewer:
    """A player bound to the reviewer role for one run."""

    name: str
    lens: str
    provider: Any | None = None  # an ExecutionProvider; None = the run's provider
    model: str | None = None

    def config_hash(self, default_model: str | None) -> str:
        key = f"{self.lens}|{self.model or default_model or ''}"
        return hashlib.sha256(key.encode()).hexdigest()[:12]


DEFAULT_ARBITER = Reviewer("arbiter", "decide on the evidence")


@dataclass
class _Usage:
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    usd: float = 0.0
    unreported: int = 0
    prompt_chars: int = 0
    by_phase: dict[str, dict[str, float]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(float)))

    def record(self, event: AgentCompleted) -> None:
        if not event.success:
            return
        self.calls += 1
        phase = self.by_phase[event.phase]
        phase["calls"] += 1
        if event.cost_input_tokens is None and event.cost_output_tokens is None:
            self.unreported += 1
            return
        self.input_tokens += event.cost_input_tokens or 0
        self.output_tokens += event.cost_output_tokens or 0
        self.usd += event.cost_usd or 0.0
        phase["input_tokens"] += event.cost_input_tokens or 0
        phase["output_tokens"] += event.cost_output_tokens or 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "usd": round(self.usd, 6),
            "calls_without_usage": self.unreported,
            "prompt_chars": self.prompt_chars,
            "by_phase": {k: dict(v) for k, v in self.by_phase.items()},
        }


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "review"


def new_run_id(title: str) -> str:
    return f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}-{_slug(title)}"


async def run_review(
    targets: Sequence[tuple[str, str]],
    *,
    provider: Any,
    out_dir: Path,
    model: str | None = None,
    reviewers: Sequence[Reviewer] | None = None,
    arbiter: Reviewer | None = DEFAULT_ARBITER,
    run_id: str | None = None,
    protocol: Protocol | None = None,
    emitter: EventEmitter | None = None,
    number_lines: bool = True,
) -> ReviewResult:
    """Review `targets` ((name, text) pairs) and write the run to `out_dir/<run_id>/`."""
    protocol = protocol or load_protocol()
    reviewers = list(reviewers or [Reviewer(n, lens) for n, lens in DEFAULT_LENSES])
    names = [r.name for r in reviewers]
    if len(set(names)) != len(names) or any("/" in n for n in names):
        raise ValueError("reviewer names must be unique and contain no '/'")
    run_id = run_id or new_run_id(targets[0][0] if targets else "review")
    run_dir = out_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    usage = _Usage()
    outer = emitter or NullEmitter()

    def _on_event(event: EngineEvent) -> None:
        if isinstance(event, AgentCompleted):
            usage.record(event)
        outer.emit(event)

    tracked = CallbackEmitter(_on_event)
    shared = prompts.prefix(targets, protocol.text_words, number_lines=number_lines)
    by_name = {r.name: r for r in reviewers}
    providers = {r.name: r.provider for r in reviewers if r.provider is not None}
    models = {r.name: r.model for r in reviewers if r.model is not None}
    if arbiter is not None:
        if arbiter.provider is not None:
            providers[arbiter.name] = arbiter.provider
        if arbiter.model is not None:
            models[arbiter.name] = arbiter.model
    envelopes: list[Envelope] = []
    log: list[Any] = []

    def props(agent: str, role: str, **extra: Any) -> dict[str, Any]:
        player = by_name.get(agent) or arbiter
        return {"role": role, "config": player.config_hash(model) if player else None, **extra}

    async def call(phase: str, asks: list[tuple[str, str]]) -> dict[str, str]:
        if not asks:
            return {}
        cap = protocol.phases[phase].max_tokens
        full = [(agent, shared + body) for agent, body in asks]
        usage.prompt_chars += sum(len(p) for _, p in full)
        log.extend(_phase_input(run_id, phase, agent, len(p)) for agent, p in full)
        results = await dispatch_phase(
            agents=full, model=model, max_tokens=cap, provider=provider, emitter=tracked,
            phase=f"review:{phase}",
            agent_providers={a: providers[a] for a, _ in asks if a in providers} or None,
            agent_models={a: models[a] for a, _ in asks if a in models} or None,
        )
        return {agent: text for agent, text, error in results if error is None}

    def keep(phase: str, agent: str, raw: str, model_cls: Any, **extra: Any) -> Any:
        parsed = parse_reply(raw, model_cls)
        role = "arbiter" if phase == "arbitrate" else "reviewer"
        env = Envelope(run=run_id, phase=phase, agent=agent, raw=raw,
                       parsed=parsed.model_dump(mode="json") if parsed else None,
                       props=props(agent, role, **extra))
        envelopes.append(env)
        write_envelope(run_dir, env)
        return parsed

    # ── review ────────────────────────────────────────────────────────
    review_cap = protocol.phases["review"].max_items or 8
    replies = await call("review", [
        (r.name, prompts.review(r.name, r.lens, review_cap)) for r in reviewers
    ])
    findings: dict[str, dict[str, Any]] = {}  # "agent/F1" -> finding
    for r in reviewers:
        if r.name not in replies:
            continue
        out = keep("review", r.name, replies[r.name], ReviewOut)
        for f in (out.findings if out else [])[:review_cap]:
            findings.setdefault(f"{r.name}/{f.id}", f.model_dump())

    # ── challenge: one call per reviewer, compact lines of the others' findings ──
    challenge_cap = protocol.phases["challenge"].max_items or 6
    asks = []
    for r in reviewers:
        others = [(ref, f["sev"], f["claim"], f.get("at")) for ref, f in findings.items()
                  if ref.split("/")[0] != r.name]
        if others and r.name in replies:
            asks.append((r.name, prompts.challenge(r.name, r.lens, others, challenge_cap)))
    challenge_replies = await call("challenge", asks)
    objections: dict[str, list[tuple[str, str, str | None]]] = defaultdict(list)  # finding -> [(oref, why, at)]
    for agent, raw in challenge_replies.items():
        out = keep("challenge", agent, raw, ChallengeOut)
        for n, o in enumerate((out.objections if out else [])[:challenge_cap], start=1):
            if o.to in findings and o.to.split("/")[0] != agent:
                objections[o.to].append((f"{agent}/O{n}", o.why, o.at))

    # ── respond: only reviewers objected to, only their threads ───────
    asks, objected_by_agent = [], {}
    for r in reviewers:
        mine = {ref: objs for ref, objs in objections.items() if ref.split("/")[0] == r.name}
        if not mine:
            continue
        threads = [(ref.split("/")[1], findings[ref]["sev"], findings[ref]["claim"], objs)
                   for ref, objs in mine.items()]
        objected_by_agent[r.name] = {
            "objected": {oref: ref.split("/")[1] for ref, objs in mine.items() for oref, _, _ in objs},
            "findings": {ref.split("/")[1]: {k: findings[ref].get(k) for k in ("sev", "at", "fix")}
                         for ref in mine},
        }
        asks.append((r.name, prompts.respond(r.name, threads)))
    respond_replies = await call("respond", asks)
    defences: dict[str, list[tuple[str, str]]] = defaultdict(list)  # objection -> [(rebuttal ref, why)]
    for agent, raw in respond_replies.items():
        out = keep("respond", agent, raw, RespondOut, **objected_by_agent[agent])
        for n, reply in enumerate(out.replies if out else [], start=1):
            if reply.act == "defend" and reply.to in objected_by_agent[agent]["objected"]:
                defences[reply.to].append((f"{agent}/R{n}", reply.why))
                log.append(contest_move(run_id, reply.to, f"{agent}/R{n}"))

    labelled = label(all_moves(envelopes, log, protocol), protocol)

    # ── arbitrate: only contested findings, only their threads ────────
    contested = [ref for ref in findings
                 if labelled.status(f"{run_id}/{ref}") == "contested" and ref in objections]
    if arbiter is not None and contested:
        threads_payload, threads_prompt = {}, []
        for ref in contested:
            pairs, exchanges = [], []
            for oref, why, at in objections[ref]:
                rebuttals = defences.get(oref, [])
                exchanges.append((oref, why, at))
                for rref, rwhy in rebuttals:
                    exchanges.append((rref, rwhy, None))
                pairs.extend([[oref, rref] for rref, _ in rebuttals] or [[oref, None]])
            f = findings[ref]
            threads_payload[ref] = {"pairs": pairs}
            threads_prompt.append((ref, f["sev"], f["claim"], f.get("at"), exchanges))
        arb = await call("arbitrate", [(arbiter.name, prompts.arbitrate(threads_prompt))])
        if arbiter.name in arb:
            keep("arbitrate", arbiter.name, arb[arbiter.name], ArbitrateOut, threads=threads_payload)
            labelled = label(all_moves(envelopes, log, protocol), protocol)

    append_log(run_dir, log)
    result = build_result(run_id, run_dir, protocol, labelled, all_moves(envelopes, log, protocol),
                          usage.as_dict(), reviewers=[r.name for r in reviewers])
    write_outputs(run_dir, result, graph_json(labelled, protocol), render_markdown(result))
    return result


def _phase_input(run_id: str, phase: str, agent: str, chars: int) -> Any:
    from lattice_graph.moves import Move

    return Move(
        id=f"{run_id}/{ENGINE}/input:{phase}:{agent}", author=f"{run_id}/{ENGINE}",
        kind="phase-input", via="engine",
        props={"phase": phase, "agent": agent, "prompt_chars": chars, "est_tokens": chars // 4},
    )
