"""Decide on a tool call (PreToolUse) and record what happened (PostToolUse)."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from engine.gate import ledger
from engine.gate.config import GateConfig
from engine.gate.judge import Judge, build_prompt, make_judge, rule_on
from engine.gate.ledger import Decision, History, Outcome

logger = logging.getLogger("deliberator.gate")
GRAPH_JSON = Path(".deliberator") / "gate" / "graph.json"


def _push_quietly(root: Path, decisions: list[Decision], history: History,
                  config: GateConfig) -> None:
    """Write to the graph database if one is configured. Never fails the hook: the log is
    the record, and `deliberator gate sync` writes anything that was missed."""
    if not config.graph_uri:
        return
    try:
        from engine.gate.graph import push

        push(decisions, history, config)
    except Exception as exc:  # noqa: BLE001
        logger.warning("gate: graph write failed (%s); run `deliberator gate sync`", exc)


EDIT_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit"})


def _edit_inside(tool: str, tool_input: dict[str, Any], cwd: str) -> bool:
    """An edit tool writing a file under `cwd`, not inside a .git folder."""
    if tool not in EDIT_TOOLS or not cwd:
        return False
    raw = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not raw:
        return False
    base = Path(cwd).resolve()
    path = Path(raw) if Path(raw).is_absolute() else base / raw
    path = path.resolve()
    if base == Path.home().resolve() or base == Path("/"):
        return False  # a session in ~ or / is not "a project"
    try:
        rel = path.relative_to(base)
    except ValueError:
        return False
    return ".git" not in rel.parts


async def decide(
    root: Path,
    config: GateConfig,
    *,
    tool: str,
    tool_input: dict[str, Any],
    cwd: str,
    session: str | None = None,
    tool_use_id: str | None = None,
    judge: Judge | None = None,
    push_graph: bool = True,
) -> Decision:
    """Rule on one tool call and log the decision.

    Order: allow-list (no model call) → identical earlier call (reuse, or allowed because the
    person approved it) → the judge, shown the closest precedents.
    """
    subject = ledger.subject_of(tool, tool_input)
    rules_hash = config.rules_hash()
    key = ledger.call_key(tool, subject, cwd, rules_hash)
    history = ledger.read(root)
    base: dict[str, Any] = {
        "id": ledger.new_id(key), "at": ledger.now(), "session": session,
        "tool_use_id": tool_use_id, "tool": tool, "subject": subject, "cwd": cwd, "key": key,
        "rules_hash": rules_hash,
    }

    decision: Decision | None = None
    if config.allow_edits_in_project and _edit_inside(tool, tool_input, cwd):
        decision = Decision(**base, verdict="allow", source="skip",
                            reason="an edit to a file inside the working folder")
    simple = tool != "Bash" or not ledger.compound(subject)
    for pattern in config.allow_without_asking if decision is None and simple else ():
        try:
            if re.search(pattern, subject):
                decision = Decision(**base, verdict="allow", source="skip",
                                    reason=f"allowed without asking: matches {pattern!r}")
                break
        except re.error:
            continue

    if decision is None and config.learn_from_approvals:
        grant = history.granted(tool, subject)
        if grant is not None:
            decision = Decision(**base, verdict="allow", source="approved",
                                reason=f"you said yes to calls like this ({grant.grant})",
                                precedents=(grant.id,))

    if decision is None and (config.reuse_identical or config.learn_from_approvals):
        for earlier in ledger.latest_for_key(history, key):
            if earlier.source in ("error", "skip"):
                continue
            if config.learn_from_approvals and history.approved(earlier):
                decision = Decision(**base, verdict="allow", source="approved",
                                    reason=f"you approved this exact call before ({earlier.id})",
                                    precedents=(earlier.id,))
            elif config.reuse_identical and earlier.verdict in ("allow", "deny"):
                decision = Decision(**base, verdict=earlier.verdict, source="reuse",
                                    rule=earlier.rule, model=earlier.model,
                                    reason=f"{earlier.reason} (same as {earlier.id})",
                                    precedents=(earlier.id,))
            if decision is not None:
                break

    if decision is None:
        precedents = ledger.similar(history, tool=tool, subject=subject, cwd=cwd,
                                    k=config.precedents)
        prompt = build_prompt(config, tool=tool, subject=subject, cwd=cwd,
                              precedents=precedents, history=history)
        ruling = await rule_on(prompt, judge or make_judge(config), subject)
        failed = ruling.reason.startswith("gate could not rule")
        decision = Decision(
            **base, verdict=ruling.verdict, reason=ruling.reason, rule=ruling.rule,
            source="error" if failed else "model", model=config.resolved_model(),
            precedents=tuple(p.id for p in precedents), latency_ms=ruling.latency_ms,
            input_tokens=ruling.input_tokens, output_tokens=ruling.output_tokens,
            grant=ruling.grant,
        )

    ledger.append(root, decision)
    if push_graph:
        history.decisions.append(decision)
        _push_quietly(root, [decision], history, config)
    return decision


def record(root: Path, config: GateConfig, *, tool: str, tool_input: dict[str, Any],
           session: str | None = None, tool_use_id: str | None = None,
           push_graph: bool = True) -> Decision | None:
    """The tool ran: log it against its decision. An ask that ran was approved."""
    history = ledger.read(root)
    subject = ledger.subject_of(tool, tool_input)
    decision = ledger.find_pending(history, tool_use_id=tool_use_id, session=session,
                                   tool=tool, subject=subject)
    if decision is None or decision.id in history.ran:
        return None
    ledger.append(root, Outcome(decision=decision.id, at=ledger.now()))
    history.ran.add(decision.id)
    if push_graph:
        _push_quietly(root, [decision], history, config)
    return decision


def hook_output(decision: Decision, config: GateConfig) -> dict[str, Any]:
    """Claude Code PreToolUse output. The reason is shown to Claude on deny, to you on ask."""
    rule = ""
    if decision.rule and 1 <= decision.rule <= len(config.rules):
        rule = f" (rule {decision.rule}: {config.rules[decision.rule - 1]})"
    grant = ""
    if decision.verdict == "ask" and decision.grant:
        grant = f" Yes is kept forever for calls matching {decision.grant}"
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision.verdict,
            "permissionDecisionReason": f"[deliberator gate] {decision.reason}{rule}{grant}",
        }
    }


def write_graph_json(root: Path, config: GateConfig) -> Path:
    from engine.gate.graph import node_link

    path = root / GRAPH_JSON
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(node_link(ledger.read(root), config), indent=1), encoding="utf-8")
    return path
