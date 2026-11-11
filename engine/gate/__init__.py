"""deliberator gate: graph-backed yes/no decisions for Claude Code tool calls.

A PreToolUse hook asks the gate whether a tool call may run. The gate applies the project's
rules (`.deliberator/gate.yml`), shows the judge model the most similar earlier decisions as
precedent, and answers allow, deny (with a reason Claude can act on) or ask. A PostToolUse
hook records that the call ran, so an approved ask becomes precedent. Every decision goes to
`.deliberator/gate/log.jsonl` and, folded with lattice-graph, to a graph database (Memgraph)
and `graph.json`.
"""

from engine.gate.config import GateConfig, load_config
from engine.gate.core import decide, hook_output, record
from engine.gate.ledger import Decision

__all__ = ["Decision", "GateConfig", "decide", "hook_output", "load_config", "record"]
