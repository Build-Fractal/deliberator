"""Tests for MCP @mcp.prompt() definitions in mcp_server.py.

The 7 prompts (deliberate, challenge, force_decision, design_deliberation,
analyze_documents, review_config, check_cost) are user-facing slash-command
templates registered with FastMCP. Each must return a list of role/content
message dicts in the shape FastMCP serializes for the MCP protocol.

These tests exercise the underlying functions directly. FastMCP's
``@mcp.prompt()`` registers the function with the server but leaves it
callable as-is, so we can verify return shape and parameter embedding
without spinning up a transport.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp_server import (
    analyze_documents,
    challenge,
    check_cost,
    deliberate,
    design_deliberation,
    force_decision,
    review_config,
)


VALID_ROLES = {"user", "assistant"}


PARAMETERIZED_PROMPTS = [
    ("deliberate", deliberate, {"question": "Should we ship this on Friday?"}),
    ("challenge", challenge, {"question": "Should we ship this on Friday?"}),
    ("force_decision", force_decision, {"question": "Should we ship this on Friday?"}),
    ("review_config", review_config, {"config_yaml": "mode: cooperative\nagents: []"}),
    ("check_cost", check_cost, {"config_yaml": "mode: cooperative\nagents: []"}),
]

ZERO_ARG_PROMPTS = [
    ("design_deliberation", design_deliberation),
    ("analyze_documents", analyze_documents),
]

ALL_PROMPT_NAMES = [name for name, *_ in PARAMETERIZED_PROMPTS] + [
    name for name, _ in ZERO_ARG_PROMPTS
]


def _assert_valid_message_list(messages: object, prompt_name: str) -> None:
    """Shared shape check — used across every prompt test."""
    assert isinstance(messages, list), (
        f"{prompt_name} must return a list, got {type(messages).__name__}"
    )
    assert len(messages) >= 1, f"{prompt_name} returned an empty list"
    for i, msg in enumerate(messages):
        assert isinstance(msg, dict), (
            f"{prompt_name}[{i}] must be a dict, got {type(msg).__name__}"
        )
        assert "role" in msg, f"{prompt_name}[{i}] missing 'role' key"
        assert "content" in msg, f"{prompt_name}[{i}] missing 'content' key"
        assert msg["role"] in VALID_ROLES, (
            f"{prompt_name}[{i}] has invalid role {msg['role']!r}"
        )
        assert isinstance(msg["content"], str), (
            f"{prompt_name}[{i}] content must be str, got {type(msg['content']).__name__}"
        )
        assert msg["content"].strip(), f"{prompt_name}[{i}] has empty content"


# ---------------------------------------------------------------------------
# Shape tests — every prompt returns a valid FastMCP message list
# ---------------------------------------------------------------------------


class TestPromptReturnShape:
    """Every prompt returns the FastMCP message-list shape."""

    @pytest.mark.parametrize("name,func,kwargs", PARAMETERIZED_PROMPTS)
    def test_parameterized_prompt_shape(
        self, name: str, func, kwargs: dict
    ) -> None:
        _assert_valid_message_list(func(**kwargs), name)

    @pytest.mark.parametrize("name,func", ZERO_ARG_PROMPTS)
    def test_zero_arg_prompt_shape(self, name: str, func) -> None:
        _assert_valid_message_list(func(), name)

    def test_all_seven_prompts_covered(self) -> None:
        """Smoke check: this file exercises all 7 prompts in mcp_server."""
        assert len(ALL_PROMPT_NAMES) == 7, (
            f"Expected 7 prompts, parametrize covers {len(ALL_PROMPT_NAMES)}: "
            f"{ALL_PROMPT_NAMES}"
        )


# ---------------------------------------------------------------------------
# Parameter embedding — caller-supplied data must appear in the message body
# ---------------------------------------------------------------------------


class TestPromptParameterEmbedding:
    """Prompts that accept parameters embed them in the rendered content."""

    def test_deliberate_embeds_question(self) -> None:
        question = "Should we adopt event sourcing for the orders service?"
        messages = deliberate(question=question)
        assert any(question in m["content"] for m in messages), (
            "deliberate must echo the question into at least one message"
        )

    def test_challenge_embeds_question(self) -> None:
        question = "Migrate the public schema in production this Friday?"
        messages = challenge(question=question)
        assert any(question in m["content"] for m in messages)

    def test_force_decision_embeds_question(self) -> None:
        question = "Pick: monorepo or polyrepo for the new platform team?"
        messages = force_decision(question=question)
        assert any(question in m["content"] for m in messages)

    def test_review_config_embeds_yaml(self) -> None:
        config = "mode: red-blue\nagents:\n  - name: red\n    role: red"
        messages = review_config(config_yaml=config)
        assert any(config in m["content"] for m in messages), (
            "review_config must include the supplied YAML verbatim"
        )

    def test_check_cost_embeds_yaml(self) -> None:
        config = "mode: cooperative\niterations: 3\nagents: []"
        messages = check_cost(config_yaml=config)
        assert any(config in m["content"] for m in messages)


# ---------------------------------------------------------------------------
# Mode hints — each prompt nudges toward the right conversus mode
# ---------------------------------------------------------------------------


class TestPromptModeHints:
    """Prompts surface the conversus mode they're designed to drive."""

    def test_deliberate_mentions_modes(self) -> None:
        messages = deliberate(question="x")
        joined = " ".join(m["content"] for m in messages).lower()
        # deliberate explains all four modes
        assert "cooperative" in joined
        assert "winner-take-all" in joined
        assert "red-blue" in joined

    def test_challenge_targets_red_blue(self) -> None:
        messages = challenge(question="x")
        joined = " ".join(m["content"] for m in messages).lower()
        assert "red-blue" in joined
        assert "red team" in joined
        assert "blue team" in joined

    def test_force_decision_targets_winner_take_all(self) -> None:
        messages = force_decision(question="x")
        joined = " ".join(m["content"] for m in messages).lower()
        assert "winner-take-all" in joined


# ---------------------------------------------------------------------------
# Role-split prompts — design_deliberation + analyze_documents use the
# user→assistant pattern (spec 060) for Desktop content-scanner tolerance.
# ---------------------------------------------------------------------------


class TestRoleSplitPrompts:
    """Zero-arg prompts use the role-split pattern from spec 060."""

    def test_design_deliberation_has_user_then_assistant(self) -> None:
        messages = design_deliberation()
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"

    def test_analyze_documents_has_user_then_assistant(self) -> None:
        messages = analyze_documents()
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"


# ---------------------------------------------------------------------------
# Tool-call hints — prompts steer toward the correct conversus_* tool.
# This guards against silent drift if a prompt forgets to reference its
# tool (which would render the prompt useless for end-to-end completion).
# ---------------------------------------------------------------------------


class TestPromptToolReferences:
    """Each prompt references the conversus tool it expects to drive."""

    def test_deliberate_references_decide(self) -> None:
        messages = deliberate(question="x")
        joined = " ".join(m["content"] for m in messages)
        assert "conversus_decide" in joined

    def test_challenge_references_decide(self) -> None:
        messages = challenge(question="x")
        joined = " ".join(m["content"] for m in messages)
        assert "conversus_decide" in joined

    def test_force_decision_references_decide(self) -> None:
        messages = force_decision(question="x")
        joined = " ".join(m["content"] for m in messages)
        assert "conversus_decide" in joined

    def test_review_config_references_run(self) -> None:
        messages = review_config(config_yaml="mode: cooperative")
        joined = " ".join(m["content"] for m in messages)
        assert "conversus_run" in joined

    def test_check_cost_references_validate(self) -> None:
        messages = check_cost(config_yaml="mode: cooperative")
        joined = " ".join(m["content"] for m in messages)
        assert "conversus_validate" in joined


# ---------------------------------------------------------------------------
# Determinism — zero-arg prompts return identical output across calls.
# ---------------------------------------------------------------------------


class TestPromptDeterminism:
    """Prompts are pure functions — same input ⇒ same output."""

    def test_design_deliberation_is_deterministic(self) -> None:
        assert design_deliberation() == design_deliberation()

    def test_analyze_documents_is_deterministic(self) -> None:
        assert analyze_documents() == analyze_documents()

    def test_deliberate_is_deterministic(self) -> None:
        q = "same question"
        assert deliberate(question=q) == deliberate(question=q)
