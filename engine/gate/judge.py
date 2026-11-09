"""One model call that rules on a tool call: allow, deny or ask, with a reason.

The judge sees the project's rules (numbered), the closest earlier decisions as precedent
(including what the person approved), and the call itself. It replies with one JSON object.
Anything that goes wrong becomes ``ask``: the gate never allows by default.
"""

from __future__ import annotations

import json
import time
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from engine.gate.config import GateConfig
from engine.gate.ledger import Decision, History, Verdict


@dataclass(frozen=True)
class Ruling:
    verdict: Verdict
    reason: str
    rule: int | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0


# A judge takes the prompt and returns (reply text, input tokens, output tokens).
Judge = Callable[[str], Awaitable[tuple[str, int, int]]]

_INSTRUCTIONS = (
    "You are the permission gate for an AI coding agent working on a developer's machine. "
    "Rule on ONE tool call: allow it, deny it, or ask the developer. Apply the rules; follow "
    "precedent when a past case is alike (the developer's own approvals are strong "
    "precedent), and say so. Deny only with a reason the agent can act on: what is wrong and "
    "what to do instead. Ask when it is outside the rules and precedent gives no answer. "
    'Reply with ONE JSON object only: {"verdict":"allow|deny|ask","reason":"<=30 words",'
    '"rule":<rule number or null>}'
)


def _line(d: Decision, history: History) -> str:
    outcome = history.effective(d)
    who = "developer approved" if history.approved(d) else d.source
    subject = d.subject.replace("\n", " ")[:200]
    return f"- [{outcome}, {who}] {d.tool}: {subject} — {d.reason[:160]}"


def build_prompt(config: GateConfig, *, tool: str, subject: str, cwd: str,
                 precedents: Sequence[Decision], history: History) -> str:
    rules = "\n".join(f"{i}. {r}" for i, r in enumerate(config.rules, start=1))
    past = "\n".join(_line(d, history) for d in precedents) or "(none)"
    return (
        f"{_INSTRUCTIONS}\n\nRULES:\n{rules}\n\nPRECEDENT (most alike first):\n{past}\n\n"
        f"CALL:\ntool: {tool}\nfolder: {cwd}\ninput:\n{subject[:4000]}\n"
    )


def parse_ruling(text: str) -> tuple[Verdict, str, int | None] | None:
    start, end = text.find("{"), text.rfind("}")
    if not 0 <= start < end:
        return None
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    verdict = str(data.get("verdict", "")).lower().strip()
    if verdict not in ("allow", "deny", "ask"):
        return None
    reason = " ".join(str(data.get("reason") or "").split())[:400] or "(no reason given)"
    rule = data.get("rule")
    rule = int(rule) if isinstance(rule, int | float) and not isinstance(rule, bool) else None
    return verdict, reason, rule  # type: ignore[return-value]


async def rule_on(prompt: str, judge: Judge) -> Ruling:
    start = time.perf_counter()
    try:
        text, tin, tout = await judge(prompt)
    except Exception as exc:  # noqa: BLE001 - a failed judge asks; it never allows.
        return Ruling("ask", f"gate could not rule ({type(exc).__name__}: {exc})"[:300],
                      latency_ms=(time.perf_counter() - start) * 1000)
    parsed = parse_ruling(text)
    latency = (time.perf_counter() - start) * 1000
    if parsed is None:
        return Ruling("ask", "gate reply was not a ruling; asking instead", None, tin, tout,
                      latency)
    verdict, reason, rule = parsed
    return Ruling(verdict, reason, rule, tin, tout, latency)


# ---------------------------------------------------------------------------
# Judges per provider
# ---------------------------------------------------------------------------


def make_judge(config: GateConfig) -> Judge:
    model = config.resolved_model()
    if config.provider == "mock":
        return _mock_judge
    if config.provider == "claude-code":
        return _claude_code_judge(config, model)
    return _sdk_judge(config, model)


def _sdk_judge(config: GateConfig, model: str) -> Judge:
    async def judge(prompt: str) -> tuple[str, int, int]:
        import anthropic

        client: Any
        if config.provider == "bedrock":
            client = anthropic.AsyncAnthropicBedrockMantle(
                aws_region=config.aws_region, aws_profile=config.aws_profile,
                timeout=config.timeout_s, max_retries=1,
            )
        else:
            client = anthropic.AsyncAnthropic(timeout=config.timeout_s, max_retries=1)
        response = await client.messages.create(
            model=model,
            max_tokens=4000,  # includes thinking; effort keeps it short
            output_config={"effort": config.effort},
            messages=[{"role": "user", "content": prompt}],
        )
        if response.stop_reason == "refusal":
            return '{"verdict":"ask","reason":"the model declined to rule on this call"}', 0, 0
        text = "".join(b.text for b in response.content if b.type == "text")
        usage = response.usage
        return text, usage.input_tokens or 0, usage.output_tokens or 0

    return judge


def _claude_code_judge(config: GateConfig, model: str) -> Judge:
    async def judge(prompt: str) -> tuple[str, int, int]:
        # Lean calls load no settings, so the nested claude runs no hooks (no recursion).
        import tempfile

        from engine.execution.provider import ExecutionTask
        from engine.execution.providers import get_provider

        provider = get_provider("claude-code", lean=True, effort=config.effort)
        out = Path(tempfile.mkdtemp(prefix="gate-")) / "ruling.md"
        task = ExecutionTask.from_prompt(
            prompt, output_path=str(out), read_paths=[],
            metadata={"phase": "gate", "agent_name": "gate", "model": model,
                      "max_tokens": 4000},
        )
        result = await provider.execute(task)
        if not result.success:
            raise RuntimeError(str(result.error))
        cost = result.cost
        return (result.content or "", getattr(cost, "input_tokens", 0) or 0,
                getattr(cost, "output_tokens", 0) or 0)

    return judge


async def _mock_judge(prompt: str) -> tuple[str, int, int]:
    """Deterministic stand-in for tests and dry runs."""
    call = prompt.rsplit("CALL:", 1)[-1].lower()
    if "rm -rf /" in call or "--force" in call or "push -f" in call:
        return '{"verdict":"deny","reason":"destructive; use a scoped command","rule":2}', 0, 0
    if "git push" in call or "publish" in call:
        return '{"verdict":"ask","reason":"publishes outside the machine","rule":5}', 0, 0
    return '{"verdict":"allow","reason":"routine development","rule":6}', 0, 0
