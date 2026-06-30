"""``deliberator snap`` — snap-verdict deliberation for Claude Code PreToolUse hooks.

Cheap (3 agents, single phase, Haiku-default) deliberation evaluating whether
Claude Code should proceed with a tool call (typically a Bash command). Returns
a verdict (ALLOW / DENY / ASK) usable as a Claude Code hook gate.

Reference: https://code.claude.com/docs/en/hooks-guide

Architectural notes:

- This is a **prototype** (no formal spec yet). If validated by real use, it
  promotes to a v4.3.0+ mode spec (`snap-gate`) with the four-stage protocol.
- It runs *outside* the full phase pipeline. No cross-reviews, revisions,
  disputes, synthesis, or arbiter — just three parallel reviews + a
  deterministic aggregation rule. Target wall-clock: 1-3 seconds.
- It dogfoods Component Principle XXIX informally: verdicts are emitted as
  structured JSON (not prose) so hook scripts can `jq` them mechanically.

Usage:

    # Direct invocation (native verdict shape):
    deliberator snap --command "rm -rf /tmp/build"

    # As a Claude Code PreToolUse hook (reads stdin per hooks contract):
    echo '{"tool_input": {"command": "rm -rf /tmp/build"}}' | deliberator snap --hook-mode

The --hook-mode flag emits Claude Code's `hookSpecificOutput` JSON shape
directly (per https://code.claude.com/docs/en/hooks) so a hook config can
pipe stdin straight into it without an adapter shell script.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from typing import Literal

import click

# Default model for snap-verdict deliberations. Haiku is the right choice:
# fast, cheap, and the verdict task (Should Claude run this command?) does
# not need the depth of Sonnet/Opus. Tunable via --model.
_DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Default agent budget: 3 agents in parallel. More agents = more thorough
# but slower + costlier. 3 is the smallest set that gets adversarial-
# composition value (pragmatist vs devil's-advocate vs safety-auditor).
_AGENT_PROMPTS: dict[str, str] = {
    "pragmatist": (
        "You are a pragmatist. You evaluate whether running this command is a "
        "reasonable next step given a typical developer workflow. You weigh "
        "convenience against risk and prefer letting routine work proceed. "
        "You DENY only when the command is clearly destructive with no "
        "redeeming use case in the apparent context."
    ),
    "devils-advocate": (
        "You are a devil's-advocate. You look for ways this command could "
        "go wrong: typos that escalate scope (`rm -rf .` vs `rm -rf ./build`), "
        "commands that exfiltrate data, commands with dangerous default "
        "behavior. You lean toward ASK or DENY when the command's blast "
        "radius exceeds the apparent task."
    ),
    "safety-auditor": (
        "You are a safety auditor. You focus on data loss, irrecoverable "
        "operations, and operations that touch shared/production state. "
        "You DENY commands that delete uncommitted work, force-push to "
        "shared branches, or modify state outside the current project. "
        "You ASK when intent is unclear."
    ),
}

_SYSTEM_PROMPT_PREAMBLE = (
    "You are evaluating whether Claude Code should proceed with running a shell "
    "command on the user's behalf. Your job is to return a single verdict.\n\n"
    "Reply in EXACTLY this format (two lines, nothing else):\n\n"
    "VERDICT: <ALLOW|DENY|ASK>\n"
    "RATIONALE: <one short sentence>\n\n"
    "VERDICT semantics:\n"
    "- ALLOW: the command is safe and routine; proceed without prompting the user.\n"
    "- DENY: the command is clearly unsafe; block it.\n"
    "- ASK: the command's intent or scope is unclear; ask the user to confirm.\n\n"
    "Be concise. Do not add preamble, do not repeat the command, do not explain "
    "the rules.\n\n"
)

_VERDICT_RE = re.compile(r"^\s*VERDICT:\s*(ALLOW|DENY|ASK)\s*$", re.IGNORECASE | re.MULTILINE)
_RATIONALE_RE = re.compile(r"^\s*RATIONALE:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)


Verdict = Literal["ALLOW", "DENY", "ASK"]


@dataclass(frozen=True)
class AgentVerdict:
    """A single agent's verdict on a command."""

    agent: str
    verdict: Verdict
    rationale: str
    raw_output: str
    latency_ms: float


@dataclass(frozen=True)
class SnapResult:
    """Aggregated snap-verdict deliberation result.

    The aggregation rule is deterministic:
    - If ANY agent says DENY → final verdict DENY (safety wins).
    - Else if ANY agent says ASK → final verdict ASK (escalate to user).
    - Else (all ALLOW) → final verdict ALLOW.
    """

    final_verdict: Verdict
    rationale: str
    agent_verdicts: list[AgentVerdict]
    consensus: Literal["unanimous-allow", "unanimous-deny", "mixed-deny-wins", "mixed-ask-wins"]
    total_latency_ms: float


# ---------------------------------------------------------------------------
# Verdict parsing
# ---------------------------------------------------------------------------


def _parse_agent_output(raw: str) -> tuple[Verdict, str]:
    """Extract VERDICT + RATIONALE from an agent's raw text output.

    Tolerant of capitalization and surrounding text. If no recognized
    VERDICT line is found, defaults to ASK (the most conservative non-deny
    fallback — never silently allow a missed parse).
    """
    verdict_match = _VERDICT_RE.search(raw)
    rationale_match = _RATIONALE_RE.search(raw)

    if verdict_match:
        verdict: Verdict = verdict_match.group(1).upper()  # type: ignore[assignment]
    else:
        verdict = "ASK"

    if rationale_match:
        rationale = rationale_match.group(1).strip()
    else:
        # Take the first non-empty line that isn't the verdict line, as a fallback.
        non_empty = [
            ln.strip() for ln in raw.splitlines()
            if ln.strip() and not _VERDICT_RE.match(ln)
        ]
        rationale = non_empty[0] if non_empty else "(no rationale)"

    return verdict, rationale


def _aggregate(agent_verdicts: list[AgentVerdict]) -> tuple[Verdict, str, str]:
    """Apply the deterministic aggregation rule. Returns (final, rationale, consensus_label)."""
    verdicts = [v.verdict for v in agent_verdicts]

    if "DENY" in verdicts:
        deny_agent = next(v for v in agent_verdicts if v.verdict == "DENY")
        consensus = "unanimous-deny" if all(v == "DENY" for v in verdicts) else "mixed-deny-wins"
        return "DENY", f"{deny_agent.agent}: {deny_agent.rationale}", consensus

    if "ASK" in verdicts:
        ask_agent = next(v for v in agent_verdicts if v.verdict == "ASK")
        return "ASK", f"{ask_agent.agent}: {ask_agent.rationale}", "mixed-ask-wins"

    # All ALLOW.
    return "ALLOW", agent_verdicts[0].rationale, "unanimous-allow"


# ---------------------------------------------------------------------------
# Async dispatch
# ---------------------------------------------------------------------------


async def _run_agent(
    provider,  # ModelProvider (duck-typed)
    agent_name: str,
    agent_prompt: str,
    command: str,
    cwd: str | None,
    model: str,
    max_tokens: int = 200,
) -> AgentVerdict:
    """Run one agent against the command. Returns its AgentVerdict.

    Errors are converted to ASK verdicts (conservative fallback): if the
    LLM fails, we don't know enough to ALLOW or DENY, so we escalate.
    """
    context_line = f"Current working directory: {cwd}\n" if cwd else ""
    prompt = (
        f"{_SYSTEM_PROMPT_PREAMBLE}"
        f"{agent_prompt}\n\n"
        f"---\n\n"
        f"{context_line}"
        f"Command to evaluate:\n\n```\n{command}\n```\n"
    )

    start_ns = time.perf_counter_ns()
    try:
        raw = await provider.complete(prompt=prompt, model=model, max_tokens=max_tokens)
    except Exception as exc:  # noqa: BLE001 — Principle V: never raise; convert to ASK.
        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
        return AgentVerdict(
            agent=agent_name,
            verdict="ASK",
            rationale=f"(agent error: {type(exc).__name__}) {exc}",
            raw_output="",
            latency_ms=latency_ms,
        )

    latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0
    verdict, rationale = _parse_agent_output(raw)
    return AgentVerdict(
        agent=agent_name,
        verdict=verdict,
        rationale=rationale,
        raw_output=raw,
        latency_ms=latency_ms,
    )


async def run_snap(
    command: str,
    cwd: str | None = None,
    model: str = _DEFAULT_MODEL,
    provider=None,
) -> SnapResult:
    """Run a snap-verdict deliberation. Provider can be injected for tests."""
    if provider is None:
        # Lazy construct an Anthropic provider. Resolution order matches the
        # documented contract in the `deliberator:status` skill:
        #   1. ANTHROPIC_API_KEY env var (the Anthropic SDK reads this
        #      automatically when constructed with auth_token=None)
        #   2. Stored OAuth credential (per-provider file or legacy auth.json)
        #   3. SDK raises 401 at first call → each agent reports
        #      ProviderError → aggregator returns ASK (never silent ALLOW)
        #
        # Why env-var-first: subscription OAuth tokens can stop working
        # (expired, scope-restricted, account changes) while an
        # ANTHROPIC_API_KEY in env is the explicit override the user reaches
        # for to fix the breakage. Putting OAuth first means the explicit
        # override is silently ignored.
        import os

        from engine.providers.anthropic import AnthropicProvider

        if os.environ.get("ANTHROPIC_API_KEY"):
            # Let the Anthropic SDK pick up the env var. auth_token=None is
            # the documented opt-in path for env-var auth.
            provider = AnthropicProvider(auth_token=None)
        else:
            from engine.auth import get_credentials

            creds = get_credentials("anthropic")
            token = creds.get("access_token") if creds else None
            provider = AnthropicProvider(auth_token=token)

    start_ns = time.perf_counter_ns()
    tasks = [
        _run_agent(provider, name, agent_prompt, command, cwd, model)
        for name, agent_prompt in _AGENT_PROMPTS.items()
    ]
    agent_verdicts = await asyncio.gather(*tasks)
    total_latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000.0

    final_verdict, final_rationale, consensus = _aggregate(list(agent_verdicts))

    return SnapResult(
        final_verdict=final_verdict,
        rationale=final_rationale,
        agent_verdicts=list(agent_verdicts),
        consensus=consensus,  # type: ignore[arg-type]
        total_latency_ms=total_latency_ms,
    )


# ---------------------------------------------------------------------------
# Output shapes
# ---------------------------------------------------------------------------


def _native_output(result: SnapResult) -> dict:
    """Native verdict JSON for direct CLI use."""
    return {
        "verdict": result.final_verdict,
        "rationale": result.rationale,
        "consensus": result.consensus,
        "total_latency_ms": round(result.total_latency_ms, 1),
        "agent_verdicts": [
            {
                "agent": v.agent,
                "verdict": v.verdict,
                "rationale": v.rationale,
                "latency_ms": round(v.latency_ms, 1),
            }
            for v in result.agent_verdicts
        ],
    }


def _hook_output(result: SnapResult) -> dict:
    """Claude Code PreToolUse hook JSON.

    Per https://code.claude.com/docs/en/hooks: emit hookSpecificOutput
    with permissionDecision in {allow, deny, ask}.
    """
    decision_map: dict[Verdict, str] = {
        "ALLOW": "allow",
        "DENY": "deny",
        "ASK": "ask",
    }
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision_map[result.final_verdict],
            "permissionDecisionReason": (
                f"[deliberator snap, {result.consensus}] {result.rationale}"
            ),
        }
    }


# ---------------------------------------------------------------------------
# Click command
# ---------------------------------------------------------------------------


@click.command(
    name="snap",
    help="Snap-verdict deliberation for Claude Code PreToolUse hooks.",
    epilog="""\b
Examples:
  # Evaluate a command directly:
  deliberator snap --command "rm -rf /tmp/build"

  # Use as a Claude Code PreToolUse hook (reads stdin):
  echo '{"tool_input": {"command": "git push --force"}}' | deliberator snap --hook-mode

Add to .claude/settings.json:

  {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{
    "type": "command",
    "if": "Bash(rm * | git push --force* | DROP TABLE*)",
    "command": "deliberator snap --hook-mode"
  }]}]}}
""",
)
@click.option(
    "--command", "-c",
    type=str,
    default=None,
    help="Command to evaluate. If omitted, reads JSON from stdin (hook mode).",
)
@click.option(
    "--hook-mode",
    is_flag=True,
    help="Emit Claude Code hookSpecificOutput JSON; otherwise emit native verdict.",
)
@click.option(
    "--model",
    type=str,
    default=_DEFAULT_MODEL,
    show_default=True,
    help="Anthropic model identifier.",
)
def snap(command: str | None, hook_mode: bool, model: str) -> None:
    """Run a snap-verdict deliberation against a single command.

    Exit codes follow the Claude Code hooks contract
    (https://code.claude.com/docs/en/hooks):
    - 0: success, stdout JSON is parsed by Claude Code
    - 2: blocking error (stderr fed back to Claude; tool call prevented)
    """
    # Resolve command from argv or stdin.
    cwd: str | None = None
    if command is None:
        try:
            stdin_data = sys.stdin.read()
            stdin_json = json.loads(stdin_data) if stdin_data.strip() else {}
            command = (stdin_json.get("tool_input") or {}).get("command")
            cwd = stdin_json.get("cwd")
        except (json.JSONDecodeError, AttributeError) as exc:
            print(f"deliberator snap: malformed stdin JSON: {exc}", file=sys.stderr)
            sys.exit(2)

    if not command:
        print("deliberator snap: no command provided (use --command or pipe hook JSON)", file=sys.stderr)
        sys.exit(2)

    # Run the deliberation.
    try:
        result = asyncio.run(run_snap(command=command, cwd=cwd, model=model))
    except Exception as exc:  # noqa: BLE001 — Principle V: never block on infra failure.
        # If the deliberation itself fails (auth, network, etc.), default to
        # ASK so the user gets a permission prompt rather than a silent allow.
        fallback_payload = (
            _hook_output(
                SnapResult(
                    final_verdict="ASK",
                    rationale=f"snap deliberation failed: {type(exc).__name__}: {exc}",
                    agent_verdicts=[],
                    consensus="mixed-ask-wins",
                    total_latency_ms=0.0,
                )
            )
            if hook_mode
            else {
                "verdict": "ASK",
                "rationale": f"snap deliberation failed: {type(exc).__name__}: {exc}",
                "consensus": "mixed-ask-wins",
                "total_latency_ms": 0.0,
                "agent_verdicts": [],
            }
        )
        print(json.dumps(fallback_payload, indent=2 if not hook_mode else None))
        sys.exit(0)  # Non-blocking; the ASK verdict is the signal.

    payload = _hook_output(result) if hook_mode else _native_output(result)
    print(json.dumps(payload, indent=2 if not hook_mode else None))
    sys.exit(0)
