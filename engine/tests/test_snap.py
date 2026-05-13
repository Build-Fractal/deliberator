"""Unit tests for engine.cli.snap — snap-verdict deliberation prototype.

Uses a mock provider so no real LLM calls are made. Tests cover:
- Verdict parsing from agent raw output (well-formed and malformed)
- Aggregation rule (any-DENY-wins, then any-ASK-wins, else unanimous-ALLOW)
- Native output shape (CLI default)
- Hook-mode output shape (Claude Code hookSpecificOutput contract)
- Failure-mode fallback (ASK on infrastructure errors, per Principle V)

The aggregation logic is deterministic and the most testable piece. The
LLM-driven verdict-emission is mocked so tests stay fast + free.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass

import pytest

from engine.cli.snap import (
    AgentVerdict,
    SnapResult,
    _aggregate,
    _hook_output,
    _native_output,
    _parse_agent_output,
    run_snap,
)


# ────────────────────────────────────────────────────────────────────────────
# Verdict parsing
# ────────────────────────────────────────────────────────────────────────────


def test_parse_well_formed_output_extracts_verdict_and_rationale():
    """A well-formed 'VERDICT: X\nRATIONALE: ...' is parsed cleanly."""
    raw = "VERDICT: ALLOW\nRATIONALE: routine ls command in the project directory.\n"
    verdict, rationale = _parse_agent_output(raw)
    assert verdict == "ALLOW"
    assert rationale == "routine ls command in the project directory."


def test_parse_case_insensitive_verdict():
    """VERDICT line is case-insensitive (e.g., 'verdict: deny')."""
    raw = "verdict: deny\nrationale: rm -rf at root\n"
    verdict, rationale = _parse_agent_output(raw)
    assert verdict == "DENY"
    assert rationale == "rm -rf at root"


def test_parse_with_surrounding_prose_still_works():
    """Tolerant of LLMs that add preamble or trailing prose."""
    raw = (
        "Looking at this command, my assessment is:\n\n"
        "VERDICT: ASK\n"
        "RATIONALE: The destination path is ambiguous; user intent unclear.\n\n"
        "Hope that helps!"
    )
    verdict, rationale = _parse_agent_output(raw)
    assert verdict == "ASK"
    assert rationale == "The destination path is ambiguous; user intent unclear."


def test_parse_no_verdict_line_defaults_to_ASK():
    """Missing VERDICT line → conservative ASK fallback (never silent ALLOW)."""
    raw = "I'm not sure what to make of this command."
    verdict, _ = _parse_agent_output(raw)
    assert verdict == "ASK"


def test_parse_empty_output_defaults_to_ASK():
    """Empty agent output → ASK."""
    verdict, rationale = _parse_agent_output("")
    assert verdict == "ASK"
    assert rationale == "(no rationale)"


# ────────────────────────────────────────────────────────────────────────────
# Aggregation rule
# ────────────────────────────────────────────────────────────────────────────


def _av(agent: str, verdict: str, rationale: str = "") -> AgentVerdict:
    """Test helper: build an AgentVerdict."""
    return AgentVerdict(
        agent=agent, verdict=verdict, rationale=rationale,
        raw_output="", latency_ms=0.0,
    )


def test_aggregate_unanimous_allow_returns_allow():
    """All three agents say ALLOW → ALLOW, consensus=unanimous-allow."""
    verdicts = [_av("pragmatist", "ALLOW"), _av("devils-advocate", "ALLOW"), _av("safety", "ALLOW")]
    final, _, consensus = _aggregate(verdicts)
    assert final == "ALLOW"
    assert consensus == "unanimous-allow"


def test_aggregate_unanimous_deny_returns_deny_with_label():
    """All three agents say DENY → DENY, consensus=unanimous-deny."""
    verdicts = [_av("p", "DENY", "p reason"), _av("d", "DENY"), _av("s", "DENY")]
    final, rationale, consensus = _aggregate(verdicts)
    assert final == "DENY"
    assert consensus == "unanimous-deny"
    assert "p reason" in rationale


def test_aggregate_any_deny_wins_over_two_allows():
    """Even one DENY beats two ALLOWs (safety-wins rule)."""
    verdicts = [_av("p", "ALLOW"), _av("d", "ALLOW"), _av("safety", "DENY", "destructive")]
    final, rationale, consensus = _aggregate(verdicts)
    assert final == "DENY"
    assert consensus == "mixed-deny-wins"
    assert "safety: destructive" in rationale


def test_aggregate_ask_beats_allow_when_no_deny():
    """Any ASK + no DENY → ASK."""
    verdicts = [_av("p", "ALLOW"), _av("d", "ASK", "unclear scope"), _av("s", "ALLOW")]
    final, rationale, consensus = _aggregate(verdicts)
    assert final == "ASK"
    assert consensus == "mixed-ask-wins"
    assert "d: unclear scope" in rationale


def test_aggregate_deny_beats_ask():
    """DENY trumps ASK trumps ALLOW — strict precedence."""
    verdicts = [_av("p", "ASK"), _av("d", "DENY", "destructive"), _av("s", "ALLOW")]
    final, _, consensus = _aggregate(verdicts)
    assert final == "DENY"
    assert consensus == "mixed-deny-wins"


# ────────────────────────────────────────────────────────────────────────────
# Output shapes
# ────────────────────────────────────────────────────────────────────────────


def _snap_result(final: str = "ALLOW") -> SnapResult:
    return SnapResult(
        final_verdict=final,  # type: ignore[arg-type]
        rationale="test rationale",
        agent_verdicts=[
            _av("pragmatist", "ALLOW", "p rationale"),
            _av("devils-advocate", "ALLOW", "d rationale"),
            _av("safety-auditor", "ALLOW", "s rationale"),
        ],
        consensus="unanimous-allow",
        total_latency_ms=1234.5,
    )


def test_native_output_shape():
    """Native CLI output has verdict, rationale, consensus, and per-agent breakdown."""
    payload = _native_output(_snap_result())
    assert payload["verdict"] == "ALLOW"
    assert payload["rationale"] == "test rationale"
    assert payload["consensus"] == "unanimous-allow"
    assert payload["total_latency_ms"] == 1234.5
    assert len(payload["agent_verdicts"]) == 3
    assert payload["agent_verdicts"][0]["agent"] == "pragmatist"


@pytest.mark.parametrize(
    "internal_verdict,expected_hook_decision",
    [
        ("ALLOW", "allow"),
        ("DENY", "deny"),
        ("ASK", "ask"),
    ],
)
def test_hook_output_maps_to_claude_code_contract(internal_verdict, expected_hook_decision):
    """Per https://code.claude.com/docs/en/hooks: ALLOW→allow, DENY→deny, ASK→ask."""
    payload = _hook_output(_snap_result(final=internal_verdict))

    # Per the hooks contract: hookSpecificOutput.hookEventName + permissionDecision.
    assert payload["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
    assert payload["hookSpecificOutput"]["permissionDecision"] == expected_hook_decision
    assert "permissionDecisionReason" in payload["hookSpecificOutput"]


def test_hook_output_carries_rationale_in_decision_reason():
    """The hook's permissionDecisionReason includes the consensus + rationale for user feedback."""
    payload = _hook_output(_snap_result(final="DENY"))
    reason = payload["hookSpecificOutput"]["permissionDecisionReason"]
    assert "conversus snap" in reason
    assert "unanimous-allow" in reason or "test rationale" in reason


# ────────────────────────────────────────────────────────────────────────────
# Async dispatch with a mock provider (no real LLM calls)
# ────────────────────────────────────────────────────────────────────────────


@dataclass
class _MockProvider:
    """Mock provider that returns a fixed response per agent.

    `responses` is a dict from agent name → raw output string. The provider
    routes by looking at the prompt to figure out which agent it represents
    (each agent's prompt mentions the agent identity). If not matched,
    defaults to ALLOW.
    """

    responses: dict[str, str]

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        for agent_name, response in self.responses.items():
            # The agent identity appears in the prompt as the agent's role
            # description; match on a distinctive substring per agent.
            if agent_name == "pragmatist" and "pragmatist" in prompt:
                return response
            if agent_name == "devils-advocate" and "devil's-advocate" in prompt:
                return response
            if agent_name == "safety-auditor" and "safety auditor" in prompt:
                return response
        return "VERDICT: ALLOW\nRATIONALE: default mock response"


def test_run_snap_unanimous_allow_with_mock_provider():
    """End-to-end: 3 ALLOW responses → final ALLOW."""
    provider = _MockProvider(
        responses={
            "pragmatist": "VERDICT: ALLOW\nRATIONALE: routine command",
            "devils-advocate": "VERDICT: ALLOW\nRATIONALE: no escalation path",
            "safety-auditor": "VERDICT: ALLOW\nRATIONALE: no data loss risk",
        }
    )

    result = asyncio.run(run_snap(command="ls -la", provider=provider))

    assert result.final_verdict == "ALLOW"
    assert result.consensus == "unanimous-allow"
    assert len(result.agent_verdicts) == 3


def test_run_snap_safety_deny_wins():
    """Safety auditor DENY + others ALLOW → DENY (any-deny-wins)."""
    provider = _MockProvider(
        responses={
            "pragmatist": "VERDICT: ALLOW\nRATIONALE: routine",
            "devils-advocate": "VERDICT: ALLOW\nRATIONALE: routine",
            "safety-auditor": "VERDICT: DENY\nRATIONALE: rm -rf at filesystem root",
        }
    )

    result = asyncio.run(run_snap(command="rm -rf /", provider=provider))

    assert result.final_verdict == "DENY"
    assert result.consensus == "mixed-deny-wins"
    assert "safety-auditor" in result.rationale
    assert "filesystem root" in result.rationale


def test_run_snap_devils_advocate_ask_wins():
    """Devils-advocate ASK + others ALLOW → ASK."""
    provider = _MockProvider(
        responses={
            "pragmatist": "VERDICT: ALLOW\nRATIONALE: looks routine",
            "devils-advocate": "VERDICT: ASK\nRATIONALE: typo risk on path",
            "safety-auditor": "VERDICT: ALLOW\nRATIONALE: path is bounded",
        }
    )

    result = asyncio.run(run_snap(command="rm -rf build", provider=provider))

    assert result.final_verdict == "ASK"
    assert result.consensus == "mixed-ask-wins"
    assert "devils-advocate" in result.rationale


# ────────────────────────────────────────────────────────────────────────────
# Failure-mode fallback (Principle V)
# ────────────────────────────────────────────────────────────────────────────


@dataclass
class _FailingProvider:
    """Provider that always raises — for testing the ASK fallback."""

    async def complete(self, prompt: str, model: str, max_tokens: int) -> str:
        raise RuntimeError("simulated LLM failure")


def test_run_snap_agent_errors_become_ASK_verdicts():
    """When an agent's LLM call fails, that agent contributes ASK (never silent ALLOW)."""
    provider = _FailingProvider()

    result = asyncio.run(run_snap(command="any command", provider=provider))

    # All 3 agents fail → all 3 vote ASK → final ASK.
    assert result.final_verdict == "ASK"
    assert all(v.verdict == "ASK" for v in result.agent_verdicts)
    assert all("simulated LLM failure" in v.rationale for v in result.agent_verdicts)


def test_full_workflow_emits_valid_hook_json():
    """The full pipeline → JSON dump produces valid Claude Code hook payload."""
    provider = _MockProvider(
        responses={
            "pragmatist": "VERDICT: ALLOW\nRATIONALE: routine",
            "devils-advocate": "VERDICT: ALLOW\nRATIONALE: routine",
            "safety-auditor": "VERDICT: ALLOW\nRATIONALE: routine",
        }
    )

    result = asyncio.run(run_snap(command="ls", provider=provider))
    payload = _hook_output(result)
    serialized = json.dumps(payload)
    reparsed = json.loads(serialized)

    assert reparsed["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
    assert reparsed["hookSpecificOutput"]["permissionDecision"] == "allow"
