"""Gate decisions as a graph (lattice-graph), written to graph.json and to Memgraph.

Schema ``deliberator-gate`` 1.0.0. Labels carry a ``Gate`` prefix so they can share a
database with other graphs.

- ``GateDecision`` (one ruling): verdict, reason, source, model, latency, tokens, effective
  verdict (an approved ask is allow), approved.
- ``GateCall`` (what was ruled on: tool + input + folder, keyed by content), so repeated
  calls meet at one node.
- ``GateRule`` (one rule's text, keyed by content), ``GateSession``.

Edges: ``RULES_ON`` (decision → call), ``CITES_RULE`` (decision → rule), ``FOLLOWS``
(decision → an earlier decision it was shown as precedent), ``IN_SESSION``.

The log is the record; the graph is rebuilt from it, and Cypher ``MERGE`` makes every write
idempotent, so pushing the same decision twice changes nothing.
"""

from __future__ import annotations

import hashlib
import os
from collections.abc import Iterable, Sequence
from typing import Any

from engine.gate.config import GateConfig
from engine.gate.ledger import Decision, History

SCHEMA_NAME = "deliberator-gate"
SCHEMA_VERSION = "1.0.0"


def gate_schema() -> Any:
    from lattice_graph.schema import EdgeType, GraphSchema, NodeType

    return GraphSchema(
        name=SCHEMA_NAME,
        version=SCHEMA_VERSION,
        nodes=(
            NodeType(name="GateDecision", description="One ruling on one tool call"),
            NodeType(name="GateCall", description="A tool call: tool, input and folder"),
            NodeType(name="GateRule", description="One rule's text"),
            NodeType(name="GateSession", description="A Claude Code session"),
        ),
        edges=(
            EdgeType(name="RULES_ON", sources=("GateDecision",), targets=("GateCall",)),
            EdgeType(name="CITES_RULE", sources=("GateDecision",), targets=("GateRule",)),
            EdgeType(name="FOLLOWS", sources=("GateDecision",), targets=("GateDecision",)),
            EdgeType(name="IN_SESSION", sources=("GateDecision",), targets=("GateSession",)),
        ),
    )


def _rule_key(text: str) -> str:
    return "rule:" + hashlib.sha256(text.encode()).hexdigest()[:12]


def projection(decisions: Sequence[Decision], history: History,
               config: GateConfig) -> Any:
    """Nodes and edges for `decisions`. Precedent edges only to decisions in the set or
    already written (MERGE matches by key)."""
    from lattice_graph.projection import Edge, Node, Projection

    nodes: dict[str, Node] = {}
    edges: list[Edge] = []
    known = {d.id for d in history.decisions}

    def add(node: Node) -> None:
        nodes.setdefault(node.key, node)

    for d in decisions:
        dk = f"decision:{d.id}"
        add(Node(label="GateDecision", key=dk, props={
            "verdict": d.verdict, "effective": history.effective(d),
            "approved": history.approved(d), "reason": d.reason, "source": d.source,
            "model": d.model, "at": d.at, "tool": d.tool, "latency_ms": round(d.latency_ms),
            "input_tokens": d.input_tokens, "output_tokens": d.output_tokens,
            "rules_hash": d.rules_hash,
        }))
        ck = f"call:{d.key}"
        add(Node(label="GateCall", key=ck, props={
            "tool": d.tool, "subject": d.subject[:2000], "cwd": d.cwd}))
        edges.append(Edge(type="RULES_ON", source=dk, target=ck))
        if d.rule is not None and 1 <= d.rule <= len(config.rules) \
                and d.rules_hash == config.rules_hash():
            text = config.rules[d.rule - 1]
            rk = _rule_key(text)
            add(Node(label="GateRule", key=rk, props={"text": text}))
            edges.append(Edge(type="CITES_RULE", source=dk, target=rk))
        if d.session:
            sk = f"session:{d.session}"
            add(Node(label="GateSession", key=sk, props={}))
            edges.append(Edge(type="IN_SESSION", source=dk, target=sk))
    in_set = {d.id for d in decisions}
    for d in decisions:
        for p in d.precedents:
            if p in in_set or p in known:
                if p not in in_set:
                    # Ensure the endpoint exists in this projection; MERGE leaves its props.
                    add(Node(label="GateDecision", key=f"decision:{p}", props={}))
                edges.append(Edge(type="FOLLOWS", source=f"decision:{d.id}",
                                  target=f"decision:{p}"))
    return Projection(nodes=tuple(nodes.values()), edges=tuple(edges))


def node_link(history: History, config: GateConfig) -> dict[str, Any]:
    from lattice_graph.build import node_link as to_node_link

    return to_node_link(projection(history.decisions, history, config), gate_schema())


def push(decisions: Iterable[Decision], history: History, config: GateConfig,
         *, session_factory: Any = None) -> int:
    """Write `decisions` to the graph database at `config.graph_uri`. Returns statements run.

    `session_factory` is for tests: a callable returning an object with ``run(cypher,
    params)`` used as a context manager.
    """
    from lattice_graph.projection import statements

    batch = list(decisions)
    if not batch:
        return 0
    stmts = statements(projection(batch, history, config), gate_schema())
    if session_factory is None:
        if not config.graph_uri:
            return 0
        from neo4j import GraphDatabase  # Memgraph speaks bolt; the neo4j driver works.

        password = os.environ.get(config.graph_password_env or "", "")
        auth = (config.graph_user, password) if config.graph_user else None
        driver = GraphDatabase.driver(config.graph_uri, auth=auth,
                                      connection_timeout=3.0)
        try:
            with driver.session() as session:
                for cypher, params in stmts:
                    session.run(cypher, params)
        finally:
            driver.close()
        return len(stmts)
    with session_factory() as session:
        for cypher, params in stmts:
            session.run(cypher, params)
    return len(stmts)
