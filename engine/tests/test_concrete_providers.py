"""Tests for concrete SubprocessProvider implementations.

Unit tests (no network, no subprocess) verify:
- Registry integration
- Protocol conformance
- Argv construction (secrets never in argv)
- Env construction (secrets in env)
- Output parsing (JSON for claude-code, plain text for aider/opencode)

Live integration tests (marked ``@pytest.mark.live``) actually spawn
the subprocess and verify end-to-end behavior.  These are skipped by
default; run with ``pytest -m live`` to execute them.
"""

from __future__ import annotations

import asyncio
import json
import shutil
from typing import Any
from unittest.mock import patch

import pytest

from engine.execution import (
    ExecutionProvider,
    ExecutionResult,
    ExecutionTask,
)
from engine.execution.providers import PROVIDER_REGISTRY, get_provider
from engine.execution.providers.claude_code import ClaudeCodeProvider
from engine.execution.providers.aider import AiderProvider
from engine.execution.providers.opencode import OpenCodeProvider
from engine.execution.providers.codex import CodexProvider
from engine.execution.providers.copilot import CopilotProvider
from engine.execution.providers.desktop_sampling import DesktopSamplingProvider
from engine.execution.providers.gemini import GeminiProvider
from engine.execution.providers.pi import PiProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_task(
    prompt: str = "Test prompt",
    output_path: str = "/tmp/test-output.md",
    agent_name: str = "test-agent",
    read_paths: list[str] | None = None,
    **extra_metadata: Any,
) -> ExecutionTask:
    metadata = {"agent_name": agent_name, "phase": "review", **extra_metadata}
    return ExecutionTask.from_prompt(
        prompt=prompt,
        output_path=output_path,
        read_paths=read_paths,
        metadata=metadata,
    )


# ═══════════════════════════════════════════════════════════════════════════
# ClaudeCodeProvider
# ═══════════════════════════════════════════════════════════════════════════


class TestClaudeCodeRegistry:
    def test_registered(self) -> None:
        assert "claude-code" in PROVIDER_REGISTRY
        assert PROVIDER_REGISTRY["claude-code"] is ClaudeCodeProvider

    def test_get_provider(self) -> None:
        provider = get_provider("claude-code")
        assert isinstance(provider, ClaudeCodeProvider)
        assert provider.name == "claude-code"


class TestClaudeCodeConformance:
    def test_isinstance(self) -> None:
        assert isinstance(ClaudeCodeProvider(), ExecutionProvider)

    def test_supports_tool_use(self) -> None:
        assert ClaudeCodeProvider().supports_tool_use is True

    def test_supports_pooling(self) -> None:
        assert ClaudeCodeProvider().supports_pooling is False


class TestClaudeCodeArgv:
    def test_basic_argv(self) -> None:
        provider = ClaudeCodeProvider(model="sonnet")
        task = _make_task(prompt="Hello")
        argv = provider._build_argv(task)

        assert argv[0].endswith("claude") or "claude" in argv[0]
        assert "-p" in argv
        # Prompt is piped via stdin, NOT in argv (avoids --- flag confusion)
        assert "Hello" not in argv
        assert "--output-format" in argv
        idx = argv.index("--output-format")
        assert argv[idx + 1] == "json"
        assert "--no-session-persistence" in argv
        assert "--model" in argv

    def test_prompt_piped_via_stdin(self) -> None:
        """Prompt goes via stdin to avoid CLI flag misinterpretation."""
        provider = ClaudeCodeProvider()
        task = _make_task(prompt="Review this --- FILE: test.md ---")
        stdin_data = provider._build_stdin(task)
        assert stdin_data is not None
        assert b"Review this --- FILE: test.md ---" in stdin_data

    def test_api_key_NOT_in_argv(self) -> None:
        """Secrets must never appear in argv — only in env."""
        provider = ClaudeCodeProvider()
        task = _make_task(api_key="sk-ant-secret-key")
        argv = provider._build_argv(task)
        assert "sk-ant-secret-key" not in " ".join(argv)

    def test_model_override_from_metadata(self) -> None:
        provider = ClaudeCodeProvider(model="sonnet")
        task = _make_task(model="opus")
        argv = provider._build_argv(task)
        idx = argv.index("--model")
        assert argv[idx + 1] == "opus"

    @pytest.mark.parametrize(
        "model_alias",
        [
            "haiku",
            "opus",
            "claude-3-5-haiku-20241022",
            "claude-3-7-sonnet-20250219",
            "future-model-id-not-yet-shipped",
        ],
    )
    def test_decide_unknown_model_does_not_trigger_blocklist_fallback(
        self, model_alias: str
    ) -> None:
        """Models NOT on the blocklist pass through to argv unchanged.

        Regression test for PR #52 Bug 3b's value-blocklist in
        `_build_argv`. The blocklist substitutes the legacy literal
        ``"claude-sonnet-4-20250514"`` with the provider's own
        default; this test guards against drift where the conditional
        becomes a substring/prefix match and starts swallowing
        legitimate model aliases.

        Per session-review deliberation P2 (issue #60). Lives in
        parallel with issue #54 (Optional[str] refactor that would
        retire the blocklist entirely).
        """
        provider = ClaudeCodeProvider(model="sonnet")
        task = _make_task(model=model_alias)
        argv = provider._build_argv(task)
        idx = argv.index("--model")
        # The exact alias the user passed must reach the subprocess.
        # If this assertion ever fails for a non-blocklisted alias,
        # the blocklist conditional has drifted to a non-exact match.
        assert argv[idx + 1] == model_alias, (
            f"Expected --model {model_alias!r}, got {argv[idx + 1]!r}. "
            f"The blocklist may have drifted to non-exact matching."
        )

    def test_none_model_falls_back_to_provider_default(self) -> None:
        """Issue #54 contract: task.metadata['model']=None → provider default.

        Replaces the prior PR #52 value-blocklist test. The dispatch
        layer no longer leaks ``DEFAULT_MODEL`` as a sentinel; instead
        it passes ``None`` to mean "no override". The provider falls
        back to its own configured default. This test pins the new
        contract: None propagation through to the provider's --model
        argv.
        """
        provider = ClaudeCodeProvider(model="sonnet")
        task = _make_task(model=None)
        argv = provider._build_argv(task)
        idx = argv.index("--model")
        # Provider's own configured default ("sonnet") is used when
        # the dispatch layer passes None.
        assert argv[idx + 1] == "sonnet"

    def test_explicit_legacy_literal_passes_through_unchanged(self) -> None:
        """Issue #54: with the value-blocklist retired, an explicit
        model literal passes through to the subprocess unchanged.

        Before issue #54, the provider rewrote ``claude-sonnet-4-20250514``
        to its own default to defend against silent dispatch leaks.
        After issue #54, dispatch passes None for "no override", so an
        explicit literal in task.metadata is treated as a deliberate
        user pin and forwarded as-is. Users who pass an OAuth-unreachable
        model id will see the underlying transport error rather than a
        silent rewrite — which is the correct behavior.
        """
        provider = ClaudeCodeProvider(model="sonnet")
        task = _make_task(model="claude-sonnet-4-20250514")
        argv = provider._build_argv(task)
        idx = argv.index("--model")
        # Explicit literal passes through unchanged (no substitution).
        assert argv[idx + 1] == "claude-sonnet-4-20250514"

    def test_read_paths_as_add_dir(self) -> None:
        provider = ClaudeCodeProvider()
        task = _make_task(read_paths=["/path/to/spec.md", "/path/to/target.md"])
        argv = provider._build_argv(task)
        assert argv.count("--add-dir") == 2

    def test_skip_permissions_flag(self) -> None:
        provider = ClaudeCodeProvider(skip_permissions=True)
        argv = provider._build_argv(_make_task())
        assert "--dangerously-skip-permissions" in argv

    def test_no_skip_permissions(self) -> None:
        provider = ClaudeCodeProvider(skip_permissions=False)
        argv = provider._build_argv(_make_task())
        assert "--dangerously-skip-permissions" not in argv

    def test_max_budget(self) -> None:
        provider = ClaudeCodeProvider(max_budget_usd=0.50)
        argv = provider._build_argv(_make_task())
        assert "--max-budget-usd" in argv
        idx = argv.index("--max-budget-usd")
        assert argv[idx + 1] == "0.5"

    def test_allowed_tools_empty(self) -> None:
        provider = ClaudeCodeProvider(allowed_tools="")
        argv = provider._build_argv(_make_task())
        assert "--allowedTools" in argv
        idx = argv.index("--allowedTools")
        assert argv[idx + 1] == ""

    def test_system_prompt(self) -> None:
        provider = ClaudeCodeProvider(system_prompt="You are a reviewer.")
        argv = provider._build_argv(_make_task())
        assert "--system-prompt" in argv


class TestClaudeCodeEnv:
    def test_api_key_in_env(self) -> None:
        provider = ClaudeCodeProvider()
        task = _make_task(api_key="sk-ant-test-key")
        env = provider._build_env(task)
        assert env["ANTHROPIC_API_KEY"] == "sk-ant-test-key"

    def test_no_api_key_empty_env(self) -> None:
        provider = ClaudeCodeProvider()
        env = provider._build_env(_make_task())
        assert "ANTHROPIC_API_KEY" not in env


class TestClaudeCodeOutputParsing:
    """Test JSON output parsing with synthetic claude-code output."""

    def _make_json_output(
        self,
        text: str = "Response text",
        is_error: bool = False,
        cost_usd: float = 0.05,
        duration_ms: int = 2000,
        input_tokens: int = 100,
        output_tokens: int = 50,
        errors: list[str] | None = None,
    ) -> str:
        """Build a synthetic claude-code JSON output."""
        messages = [
            {"type": "system", "subtype": "init", "session_id": "test-session"},
            {
                "type": "assistant",
                "message": {
                    "content": [{"type": "text", "text": text}],
                    "model": "claude-sonnet-4-20250514",
                },
            },
            {
                "type": "result",
                "subtype": "error_max_budget_usd" if is_error else "success",
                "is_error": is_error,
                "total_cost_usd": cost_usd,
                "duration_ms": duration_ms,
                "num_turns": 1,
                "stop_reason": "end_turn",
                "errors": errors or [],
                "modelUsage": {
                    "claude-sonnet-4-20250514": {
                        "inputTokens": input_tokens,
                        "outputTokens": output_tokens,
                        "cacheCreationInputTokens": 0,
                        "cacheReadInputTokens": 0,
                        "costUSD": cost_usd,
                    },
                },
            },
        ]
        return json.dumps(messages)

    def test_success_parsing(self) -> None:
        provider = ClaudeCodeProvider()
        stdout = self._make_json_output(text="The answer is 4.")
        result = provider._parse_output(stdout, "", 0, _make_task())

        assert result.success is True
        assert result.content == "The answer is 4."
        assert result.cost is not None
        assert result.cost.usd == 0.05
        assert result.cost.input_tokens == 100
        assert result.cost.output_tokens == 50

    def test_duration_parsing(self) -> None:
        provider = ClaudeCodeProvider()
        stdout = self._make_json_output(duration_ms=3500)
        result = provider._parse_output(stdout, "", 0, _make_task())

        assert result.duration is not None
        assert result.duration.total_seconds() == pytest.approx(3.5)

    def test_error_parsing(self) -> None:
        provider = ClaudeCodeProvider()
        stdout = self._make_json_output(
            text="",
            is_error=True,
            errors=["Reached maximum budget ($0.01)"],
        )
        # Error with no text content
        messages = json.loads(stdout)
        messages[1]["message"]["content"] = []
        stdout = json.dumps(messages)

        result = provider._parse_output(stdout, "", 1, _make_task())

        assert result.success is False
        assert result.error is not None
        assert "budget" in str(result.error).lower()

    def test_non_json_fallback(self) -> None:
        provider = ClaudeCodeProvider()
        result = provider._parse_output("plain text output", "", 0, _make_task())

        assert result.success is True
        assert result.content == "plain text output"
        assert result.metadata.get("raw_output") is True

    def test_non_json_with_error_exit(self) -> None:
        provider = ClaudeCodeProvider()
        result = provider._parse_output("", "Not logged in", 1, _make_task())

        assert result.success is False
        assert result.error is not None
        assert "Not logged in" in str(result.error)

    def test_metadata_includes_num_turns(self) -> None:
        provider = ClaudeCodeProvider()
        stdout = self._make_json_output()
        result = provider._parse_output(stdout, "", 0, _make_task())

        assert result.metadata["num_turns"] == 1
        assert result.metadata["stop_reason"] == "end_turn"

    def test_tool_use_only_response_is_success_when_artifact_written(
        self, tmp_path
    ) -> None:
        """Regression: when the agent completes via tool use only (no final
        text block) and the CLI spuriously reports is_error=True, the
        provider must trust the on-disk artifact and return success.

        Seen in red-blue dogfood runs where agents wrote substantive review
        artifacts (90-120 lines) but the CLI result envelope still carried
        is_error=True, causing the dispatcher to drop the phase.
        """
        provider = ClaudeCodeProvider()
        output_path = tmp_path / "review.md"
        output_path.write_text("# Review\n\nSubstantive content written via tool use.\n")

        messages = [
            {"type": "system", "subtype": "init", "session_id": "test-session"},
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "t1",
                            "name": "Write",
                            "input": {"file_path": str(output_path)},
                        }
                    ],
                    "model": "claude-sonnet-4-20250514",
                },
            },
            {
                "type": "result",
                "subtype": "error_during_execution",
                "is_error": True,
                "total_cost_usd": 0.05,
                "duration_ms": 100000,
                "num_turns": 3,
                "stop_reason": "end_turn",
                "errors": [],
                "modelUsage": {},
            },
        ]
        stdout = json.dumps(messages)
        task = _make_task(output_path=str(output_path))
        result = provider._parse_output(stdout, "", 0, task)

        assert result.success is True
        assert result.content is None
        assert result.metadata.get("tool_use_only") is True

    def test_tool_use_only_response_is_failure_when_no_artifact(
        self, tmp_path
    ) -> None:
        """Counterpart: if is_error=True, no text, AND no artifact on disk,
        the provider must still classify as failure — we're not broadening
        success semantics, just trusting the artifact when it exists.
        """
        provider = ClaudeCodeProvider()
        output_path = tmp_path / "never-written.md"

        messages = [
            {"type": "system", "subtype": "init", "session_id": "test-session"},
            {
                "type": "assistant",
                "message": {"content": [], "model": "claude-sonnet-4-20250514"},
            },
            {
                "type": "result",
                "subtype": "error_max_budget_usd",
                "is_error": True,
                "total_cost_usd": 0.01,
                "duration_ms": 500,
                "num_turns": 0,
                "stop_reason": "budget",
                "errors": ["Reached maximum budget"],
                "modelUsage": {},
            },
        ]
        stdout = json.dumps(messages)
        task = _make_task(output_path=str(output_path))
        result = provider._parse_output(stdout, "", 1, task)

        assert result.success is False
        assert result.error is not None

    # ----------------------------------------------------------------
    # Current `claude` (>= 2.x) single-object JSON shape
    #
    # The CLI changed `--output-format json` from emitting an array of
    # messages to emitting a single result object with `.result` holding
    # the assistant text.  The parser must handle both shapes so
    # deliberator works across claude-code versions — and against the
    # Max-plan OAuth path where each subprocess is a Claude Code
    # interactive session.

    def _make_json_single_object(
        self,
        text: str = "pong",
        is_error: bool = False,
        cost_usd: float = 0.075,
        duration_ms: int = 1126,
        input_tokens: int = 20097,
        output_tokens: int = 5,
    ) -> str:
        """Build a synthetic single-object claude JSON response (v2+)."""
        return json.dumps({
            "type": "result",
            "subtype": "error_max_budget_usd" if is_error else "success",
            "is_error": is_error,
            "api_error_status": None,
            "duration_ms": duration_ms,
            "duration_api_ms": duration_ms,
            "num_turns": 1,
            "result": text,
            "stop_reason": "end_turn",
            "session_id": "test-session",
            "total_cost_usd": cost_usd,
            "modelUsage": {
                "claude-sonnet-4-6": {
                    "inputTokens": 0,
                    "outputTokens": output_tokens,
                    "cacheCreationInputTokens": input_tokens,
                    "cacheReadInputTokens": 0,
                    "costUSD": cost_usd,
                },
            },
        })

    def test_single_object_success(self) -> None:
        provider = ClaudeCodeProvider()
        stdout = self._make_json_single_object(text="pong")
        result = provider._parse_output(stdout, "", 0, _make_task())

        assert result.success is True
        assert result.content == "pong"
        assert result.cost is not None
        assert result.cost.usd == pytest.approx(0.075)
        assert result.cost.output_tokens == 5
        assert result.duration is not None
        assert result.duration.total_seconds() == pytest.approx(1.126)

    def test_single_object_error_without_content(self) -> None:
        provider = ClaudeCodeProvider()
        stdout = self._make_json_single_object(text="", is_error=True)
        result = provider._parse_output(stdout, "", 1, _make_task())

        assert result.success is False
        assert result.error is not None

    def test_single_object_metadata(self) -> None:
        provider = ClaudeCodeProvider()
        stdout = self._make_json_single_object()
        result = provider._parse_output(stdout, "", 0, _make_task())

        assert result.metadata["num_turns"] == 1
        assert result.metadata["stop_reason"] == "end_turn"

    def test_json_scalar_fallback(self) -> None:
        """A JSON scalar (e.g. a bare string) should not crash the parser."""
        provider = ClaudeCodeProvider()
        result = provider._parse_output('"just a string"', "", 0, _make_task())

        assert result.success is True
        assert result.content == '"just a string"'
        assert result.metadata.get("raw_output") is True

# ═══════════════════════════════════════════════════════════════════════════
# AiderProvider
# ═══════════════════════════════════════════════════════════════════════════


class TestAiderRegistry:
    def test_registered(self) -> None:
        assert "aider" in PROVIDER_REGISTRY

    def test_get_provider(self) -> None:
        provider = get_provider("aider")
        assert isinstance(provider, AiderProvider)


class TestAiderConformance:
    def test_isinstance(self) -> None:
        assert isinstance(AiderProvider(), ExecutionProvider)

    def test_supports_tool_use(self) -> None:
        assert AiderProvider().supports_tool_use is True


class TestAiderArgv:
    def test_basic_argv(self) -> None:
        provider = AiderProvider(model="sonnet")
        task = _make_task(prompt="Review this")
        argv = provider._build_argv(task)

        assert "--message" in argv
        assert "Review this" in argv
        assert "--exit" in argv
        assert "--yes-always" in argv
        assert "--no-stream" in argv
        assert "--no-auto-commits" in argv

    def test_api_key_not_in_argv(self) -> None:
        provider = AiderProvider()
        task = _make_task(api_key="sk-secret")
        argv = provider._build_argv(task)
        assert "sk-secret" not in " ".join(argv)

    def test_read_paths_as_file(self) -> None:
        provider = AiderProvider()
        task = _make_task(read_paths=["/path/spec.md"])
        argv = provider._build_argv(task)
        assert "--file" in argv
        idx = argv.index("--file")
        assert argv[idx + 1] == "/path/spec.md"

    def test_extra_flags(self) -> None:
        provider = AiderProvider(extra_flags=["--architect"])
        argv = provider._build_argv(_make_task())
        assert "--architect" in argv


class TestAiderOutputParsing:
    def test_success(self) -> None:
        provider = AiderProvider()
        result = provider._parse_output("Aider response\n", "", 0, _make_task())
        assert result.success is True
        assert result.content == "Aider response"

    def test_failure(self) -> None:
        provider = AiderProvider()
        result = provider._parse_output("", "Error occurred", 1, _make_task())
        assert result.success is False
        assert result.error.category == "subprocess"

    def test_aider_captures_tokens(self) -> None:
        """Parse the 'Tokens: X sent, Y received.' summary line."""
        provider = AiderProvider()
        stdout = (
            "Aider v0.50\n"
            "Reasoning about the request...\n"
            "Here is the answer.\n"
            "Tokens: 1.2k sent, 234 received. Cost: $0.0042 message, $0.04 session.\n"
        )
        result = provider._parse_output(stdout, "", 0, _make_task())
        assert result.success is True
        assert result.cost is not None
        assert result.cost.input_tokens == 1200
        assert result.cost.output_tokens == 234
        assert result.cost.usd is None

    def test_aider_token_summary_no_k_suffix(self) -> None:
        provider = AiderProvider()
        stdout = "ok\nTokens: 47 sent, 12 received.\n"
        result = provider._parse_output(stdout, "", 0, _make_task())
        assert result.cost is not None
        assert result.cost.input_tokens == 47
        assert result.cost.output_tokens == 12

    def test_aider_token_summary_with_commas(self) -> None:
        provider = AiderProvider()
        stdout = "Tokens: 1,234 sent, 567 received.\n"
        result = provider._parse_output(stdout, "", 0, _make_task())
        assert result.cost is not None
        assert result.cost.input_tokens == 1234
        assert result.cost.output_tokens == 567

    def test_aider_uses_last_token_summary(self) -> None:
        """Multi-message runs reprint the line each turn — we want the last."""
        provider = AiderProvider()
        stdout = (
            "Tokens: 100 sent, 50 received.\n"
            "More work happening...\n"
            "Tokens: 200 sent, 75 received.\n"
        )
        result = provider._parse_output(stdout, "", 0, _make_task())
        assert result.cost is not None
        assert result.cost.input_tokens == 200
        assert result.cost.output_tokens == 75

    def test_aider_no_summary_means_no_cost(self) -> None:
        """No Tokens line → cost is None (preserves unknown != zero)."""
        provider = AiderProvider()
        result = provider._parse_output("just a reply", "", 0, _make_task())
        assert result.success is True
        assert result.cost is None


# ═══════════════════════════════════════════════════════════════════════════
# OpenCodeProvider
# ═══════════════════════════════════════════════════════════════════════════


class TestOpenCodeRegistry:
    def test_registered(self) -> None:
        assert "opencode" in PROVIDER_REGISTRY

    def test_get_provider(self) -> None:
        provider = get_provider("opencode")
        assert isinstance(provider, OpenCodeProvider)


class TestOpenCodeConformance:
    def test_isinstance(self) -> None:
        assert isinstance(OpenCodeProvider(), ExecutionProvider)

    def test_supports_tool_use(self) -> None:
        assert OpenCodeProvider().supports_tool_use is True


class TestOpenCodeArgv:
    def test_basic_argv(self) -> None:
        provider = OpenCodeProvider()
        task = _make_task(prompt="Analyze code")
        argv = provider._build_argv(task)

        assert "opencode" in argv[0] or argv[0].endswith("opencode")
        assert "run" in argv
        assert "Analyze code" in argv


class TestOpenCodeArgvRequestsJson:
    def test_argv_includes_format_json(self) -> None:
        """Without ``--format json`` opencode prints free-form text — no tokens."""
        provider = OpenCodeProvider(binary="opencode")
        argv = provider._build_argv(_make_task(prompt="hi"))
        assert "--format" in argv
        idx = argv.index("--format")
        assert argv[idx + 1] == "json"


class TestOpenCodeOutputParsing:
    def test_success(self) -> None:
        provider = OpenCodeProvider()
        result = provider._parse_output("Output here\n", "", 0, _make_task())
        assert result.success is True
        assert result.content == "Output here"

    def test_failure(self) -> None:
        provider = OpenCodeProvider()
        result = provider._parse_output("", "error", 1, _make_task())
        assert result.success is False

    def test_opencode_captures_tokens(self) -> None:
        """``message`` events with ``info.tokens.{input,output,...}`` → Cost."""
        provider = OpenCodeProvider()
        events = [
            {
                "info": {
                    "role": "assistant",
                    "tokens": {
                        "input": 120,
                        "output": 45,
                        "reasoning": 5,
                        "cache": {"read": 800, "write": 0},
                    },
                },
                "parts": [{"text": "Here is the answer."}],
            },
        ]
        stdout = "\n".join(json.dumps(e) for e in events)

        result = provider._parse_output(stdout, "", 0, _make_task())

        assert result.success is True
        assert result.content == "Here is the answer."
        assert result.cost is not None
        # 120 input + 800 cache_read = 920 input tokens
        assert result.cost.input_tokens == 920
        # 45 output + 5 reasoning = 50 output tokens
        assert result.cost.output_tokens == 50
        assert result.cost.usd is None

    def test_opencode_plain_text_fallback(self) -> None:
        """If stdout isn't JSONL we still surface content with cost=None."""
        provider = OpenCodeProvider()
        result = provider._parse_output("plain output", "", 0, _make_task())
        assert result.success is True
        assert result.content == "plain output"
        assert result.cost is None
        assert result.metadata.get("raw_output") is True


# ═══════════════════════════════════════════════════════════════════════════
# CodexProvider
# ═══════════════════════════════════════════════════════════════════════════


class TestCodexRegistry:
    def test_registered(self) -> None:
        assert "codex" in PROVIDER_REGISTRY
        assert PROVIDER_REGISTRY["codex"] is CodexProvider

    def test_get_provider(self) -> None:
        provider = get_provider("codex")
        assert isinstance(provider, CodexProvider)
        assert provider.name == "codex"


class TestCodexConformance:
    def test_isinstance(self) -> None:
        assert isinstance(CodexProvider(), ExecutionProvider)

    def test_supports_tool_use(self) -> None:
        assert CodexProvider().supports_tool_use is True

    def test_supports_pooling(self) -> None:
        assert CodexProvider().supports_pooling is False

    def test_provider_name(self) -> None:
        assert CodexProvider().name == "codex"


class TestCodexArgv:
    def test_basic_argv_contains_required_flags(self) -> None:
        """argv uses the ``exec --json`` flow with deterministic last-message file."""
        provider = CodexProvider(model="o4-mini", binary="/usr/bin/codex")
        task = _make_task(prompt="Review this code")
        argv = provider._build_argv(task)

        assert argv[0] == "/usr/bin/codex"
        # ``exec`` subcommand replaces the deprecated `--quiet --full-auto` flags.
        assert "exec" in argv
        assert argv[1] == "exec"
        assert "--json" in argv
        assert "--output-last-message" in argv
        assert "--model" in argv
        idx = argv.index("--model")
        assert argv[idx + 1] == "o4-mini"
        assert argv[-1] == "Review this code"

    def test_argv_includes_output_last_message_path(self) -> None:
        """``--output-last-message`` is followed by an absolute tempfile path."""
        provider = CodexProvider()
        argv = provider._build_argv(_make_task(prompt="hi"))
        idx = argv.index("--output-last-message")
        path = argv[idx + 1]
        # Path is absolute, points at an existing tempfile, and matches our prefix.
        assert path.startswith("/")
        assert "codex-last-msg-" in path
        # Cleanup — the file is created by ``mkstemp`` in _build_argv.
        try:
            import os as _os

            _os.unlink(path)
        except OSError:
            pass

    def test_argv_no_longer_uses_deprecated_quiet_full_auto(self) -> None:
        """The old ``--quiet --full-auto`` shape is gone — guard against regression."""
        provider = CodexProvider()
        argv = provider._build_argv(_make_task(prompt="hi"))
        assert "--quiet" not in argv
        assert "--full-auto" not in argv

    def test_argv_flag_order(self) -> None:
        """Verify ``exec`` comes immediately after the binary and prompt is last."""
        provider = CodexProvider(binary="codex")
        task = _make_task(prompt="Hello")
        argv = provider._build_argv(task)

        assert argv[0] == "codex"
        assert argv[1] == "exec"
        assert argv[-1] == "Hello"
        # --json appears before the positional prompt
        json_idx = argv.index("--json")
        assert json_idx < len(argv) - 1

    def test_api_key_not_in_argv(self) -> None:
        """Secrets must never appear in argv — only in env."""
        provider = CodexProvider()
        task = _make_task(api_key="sk-openai-secret-key-12345")
        argv = provider._build_argv(task)
        joined = " ".join(argv)
        assert "sk-openai-secret-key-12345" not in joined

    def test_model_override_from_metadata(self) -> None:
        """task.metadata['model'] overrides constructor default."""
        provider = CodexProvider(model="o4-mini")
        task = _make_task(model="o3")
        argv = provider._build_argv(task)
        idx = argv.index("--model")
        assert argv[idx + 1] == "o3"

    def test_default_model_when_no_metadata_override(self) -> None:
        """Constructor model is used when metadata has no model key."""
        provider = CodexProvider(model="o4-mini")
        task = _make_task()  # no model in metadata
        argv = provider._build_argv(task)
        idx = argv.index("--model")
        assert argv[idx + 1] == "o4-mini"

    def test_prompt_appears_as_positional_arg(self) -> None:
        """Codex takes the prompt as a positional argument, not a flag value."""
        provider = CodexProvider()
        task = _make_task(prompt="Explain the function")
        argv = provider._build_argv(task)
        assert "Explain the function" in argv
        # Prompt is not preceded by a flag
        prompt_idx = argv.index("Explain the function")
        assert prompt_idx == len(argv) - 1

    def test_custom_binary_path(self) -> None:
        provider = CodexProvider(binary="/opt/codex/bin/codex")
        argv = provider._build_argv(_make_task())
        assert argv[0] == "/opt/codex/bin/codex"


class TestCodexEnv:
    def test_api_key_in_env(self) -> None:
        provider = CodexProvider()
        task = _make_task(api_key="sk-openai-test-key")
        env = provider._build_env(task)
        assert env["OPENAI_API_KEY"] == "sk-openai-test-key"

    def test_no_api_key_empty_env(self) -> None:
        provider = CodexProvider()
        env = provider._build_env(_make_task())
        assert "OPENAI_API_KEY" not in env
        assert env == {}

    def test_env_only_contains_api_key(self) -> None:
        """Env should contain only OPENAI_API_KEY, nothing else from metadata."""
        provider = CodexProvider()
        task = _make_task(api_key="sk-key", model="o3", phase="review")
        env = provider._build_env(task)
        assert len(env) == 1
        assert "OPENAI_API_KEY" in env


class TestCodexOutputParsing:
    def test_success_path_rc0(self) -> None:
        provider = CodexProvider()
        task = _make_task()
        result = provider._parse_output("The code looks good.\n", "", 0, task)

        assert result.success is True
        assert result.content == "The code looks good."
        assert result.error is None
        assert result.provider == "codex"
        assert result.metadata["returncode"] == 0

    def test_success_strips_whitespace(self) -> None:
        provider = CodexProvider()
        result = provider._parse_output("  output  \n\n", "", 0, _make_task())
        assert result.content == "output"

    def test_failure_path_nonzero_rc(self) -> None:
        provider = CodexProvider()
        task = _make_task()
        result = provider._parse_output("", "Error: auth failed", 1, task)

        assert result.success is False
        assert result.content is None
        assert result.error is not None
        assert result.error.category == "subprocess"
        assert "codex exited 1" in str(result.error)
        assert "auth failed" in str(result.error)
        assert result.provider == "codex"
        assert result.metadata["returncode"] == 1

    def test_failure_stderr_truncated_to_500(self) -> None:
        """Long stderr is truncated to 500 chars in error message and metadata."""
        provider = CodexProvider()
        long_stderr = "x" * 1000
        result = provider._parse_output("", long_stderr, 2, _make_task())

        assert result.success is False
        # The error message should contain at most 500 chars of stderr
        assert len(str(result.error)) < 600  # "codex exited 2: " + 500 chars
        assert result.metadata["stderr"][-1] == "x"
        assert len(result.metadata["stderr"]) == 500

    def test_empty_stdout_success(self) -> None:
        """Empty stdout with rc=0 is still success (content is empty string)."""
        provider = CodexProvider()
        result = provider._parse_output("", "", 0, _make_task())
        assert result.success is True
        assert result.content == ""

    def test_output_path_propagated(self) -> None:
        """output_path from the task carries through to the result."""
        provider = CodexProvider()
        task = _make_task(output_path="/tmp/codex-output.md")
        result = provider._parse_output("content", "", 0, task)
        assert result.output_path == "/tmp/codex-output.md"

    def test_failure_with_signal_exit_code(self) -> None:
        """Negative/signal exit codes are reported correctly."""
        provider = CodexProvider()
        result = provider._parse_output("", "Killed", -9, _make_task())
        assert result.success is False
        assert "codex exited -9" in str(result.error)

    def test_codex_captures_tokens_from_info_total_shape(self) -> None:
        """Documented shape: ``token_count`` events carry ``info.total_token_usage``.

        Per ``codex-rs/protocol/src/protocol.rs``, each ``token_count``
        event re-publishes the **cumulative** running totals (not a
        per-turn delta) — so ``_parse_output`` should take the LAST
        event's totals, not sum across events.
        """
        provider = CodexProvider()
        jsonl = "\n".join([
            json.dumps({
                "type": "token_count",
                "info": {
                    "total_token_usage": {
                        "input_tokens": 100,
                        "cached_input_tokens": 0,
                        "output_tokens": 25,
                        "reasoning_output_tokens": 0,
                        "total_tokens": 125,
                    },
                    "last_token_usage": {
                        "input_tokens": 100,
                        "output_tokens": 25,
                    },
                    "model_context_window": 200_000,
                },
            }),
            json.dumps({"type": "agent_message", "message": "First reply."}),
            # Second turn: cumulative grows to 130/37, NOT a delta of 30/12.
            json.dumps({
                "type": "token_count",
                "info": {
                    "total_token_usage": {
                        "input_tokens": 130,
                        "cached_input_tokens": 0,
                        "output_tokens": 37,
                        "reasoning_output_tokens": 0,
                        "total_tokens": 167,
                    },
                    "last_token_usage": {
                        "input_tokens": 30,
                        "output_tokens": 12,
                    },
                    "model_context_window": 200_000,
                },
            }),
            json.dumps({"type": "agent_message", "message": "Final answer is 42."}),
        ])

        result = provider._parse_output(jsonl, "", 0, _make_task())

        assert result.success is True
        assert result.cost is not None
        # Last event's cumulative totals — NOT 100+130=230.
        assert result.cost.input_tokens == 130
        assert result.cost.output_tokens == 37
        assert result.cost.usd is None
        # Final agent_message wins as fallback content (no last-message file).
        assert result.content == "Final answer is 42."

    def test_codex_folds_cached_input_and_reasoning_tokens(self) -> None:
        """``cached_input_tokens`` → input; ``reasoning_output_tokens`` → output.

        Matches how anthropic/gemini providers fold cache + reasoning fields.
        """
        provider = CodexProvider()
        jsonl = json.dumps({
            "type": "token_count",
            "info": {
                "total_token_usage": {
                    "input_tokens": 50,
                    "cached_input_tokens": 200,
                    "output_tokens": 30,
                    "reasoning_output_tokens": 70,
                    "total_tokens": 350,
                },
            },
        })
        result = provider._parse_output(jsonl, "", 0, _make_task())
        assert result.cost is not None
        assert result.cost.input_tokens == 250  # 50 + 200 cached
        assert result.cost.output_tokens == 100  # 30 + 70 reasoning

    def test_codex_legacy_flat_shape_still_aggregates(self) -> None:
        """Older codex versions used a flat ``input_tokens``/``output_tokens``
        shape on the event itself.  Preserve that path as a fallback so we
        don't regress users on pinned older codex CLI builds.
        """
        provider = CodexProvider()
        jsonl = "\n".join([
            json.dumps({"type": "token_count", "input_tokens": 100, "output_tokens": 25}),
            json.dumps({"type": "token_count", "input_tokens": 30, "output_tokens": 12}),
        ])
        result = provider._parse_output(jsonl, "", 0, _make_task())
        assert result.cost is not None
        # Legacy shape doesn't carry cumulative totals — sum is correct here.
        assert result.cost.input_tokens == 130
        assert result.cost.output_tokens == 37

    def test_codex_jsonl_with_msg_envelope(self) -> None:
        """Codex sometimes wraps payloads in a ``msg`` envelope — handle both."""
        provider = CodexProvider()
        jsonl = json.dumps({
            "type": "token_count",
            "msg": {"input_tokens": 7, "output_tokens": 3},
        })
        result = provider._parse_output(jsonl, "", 0, _make_task())
        assert result.cost is not None
        assert result.cost.input_tokens == 7
        assert result.cost.output_tokens == 3

    def test_codex_no_token_events_falls_back_to_text(self) -> None:
        """When stdout has no ``token_count`` events at all, cost is None."""
        provider = CodexProvider()
        result = provider._parse_output("Just plain text\n", "", 0, _make_task())
        assert result.success is True
        assert result.content == "Just plain text"
        assert result.cost is None

    def test_codex_prefers_last_message_file_over_event_stream(self, tmp_path) -> None:
        """``--output-last-message`` file is the authoritative source for content.

        When ``_build_argv`` sets up a tempfile and codex writes to it,
        ``_parse_output`` should read that file rather than scraping the
        event stream.  This test simulates the file having content while
        the JSONL stream's last ``agent_message`` says something different.
        """
        provider = CodexProvider()
        # Simulate ``_build_argv`` having allocated a tempfile.
        msg_file = tmp_path / "last-msg.txt"
        msg_file.write_text("Authoritative final answer.\n")
        provider._last_message_path = str(msg_file)

        jsonl = "\n".join([
            json.dumps({"type": "agent_message", "message": "Stale streaming text."}),
        ])
        result = provider._parse_output(jsonl, "", 0, _make_task())
        assert result.success is True
        # File wins over event-stream agent_message.
        assert result.content == "Authoritative final answer."
        # File is consumed (deleted) after read.
        assert not msg_file.exists()
        assert provider._last_message_path is None

    def test_codex_falls_back_to_event_stream_when_message_file_empty(
        self, tmp_path,
    ) -> None:
        """If the last-message file exists but is empty, fall back to events."""
        provider = CodexProvider()
        msg_file = tmp_path / "last-msg.txt"
        msg_file.write_text("")
        provider._last_message_path = str(msg_file)

        jsonl = json.dumps({"type": "agent_message", "message": "Stream wins."})
        result = provider._parse_output(jsonl, "", 0, _make_task())
        assert result.content == "Stream wins."

    def test_codex_cleans_up_message_file_on_failure(self, tmp_path) -> None:
        """Even when codex exits non-zero, the tempfile must be removed."""
        provider = CodexProvider()
        msg_file = tmp_path / "last-msg.txt"
        msg_file.write_text("partial")
        provider._last_message_path = str(msg_file)

        result = provider._parse_output("", "auth failed", 1, _make_task())
        assert result.success is False
        assert not msg_file.exists()
        assert provider._last_message_path is None


# ═══════════════════════════════════════════════════════════════════════════
# GeminiProvider
# ═══════════════════════════════════════════════════════════════════════════


class TestGeminiRegistry:
    def test_registered(self) -> None:
        assert "gemini" in PROVIDER_REGISTRY
        assert PROVIDER_REGISTRY["gemini"] is GeminiProvider


class TestGeminiArgvRequestsJson:
    def test_argv_includes_json_output_flag(self) -> None:
        """Without ``-o json`` the CLI emits free-form text — no token data."""
        provider = GeminiProvider(binary="gemini")
        argv = provider._build_argv(_make_task(prompt="hi"))
        assert "-o" in argv
        idx = argv.index("-o")
        assert argv[idx + 1] == "json"


class TestGeminiOutputParsing:
    def test_gemini_captures_tokens(self) -> None:
        """``stats.models[*].tokens.{prompt,candidates,cached}`` → Cost."""
        provider = GeminiProvider()
        envelope = {
            "response": "Hello there.",
            "stats": {
                "models": {
                    "gemini-2.5-pro": {
                        "tokens": {
                            "prompt": 250,
                            "candidates": 75,
                            "cached": 0,
                            "total": 325,
                        },
                    },
                },
            },
        }
        result = provider._parse_output(json.dumps(envelope), "", 0, _make_task())
        assert result.success is True
        assert result.content == "Hello there."
        assert result.cost is not None
        assert result.cost.input_tokens == 250
        assert result.cost.output_tokens == 75
        assert result.cost.usd is None

    def test_gemini_folds_cached_tokens_into_input(self) -> None:
        """``cached`` tokens are read-from-cache prompt context — count as input."""
        provider = GeminiProvider()
        envelope = {
            "response": "ok",
            "stats": {
                "models": {
                    "gemini-2.5-pro": {
                        "tokens": {"prompt": 50, "candidates": 10, "cached": 200},
                    },
                },
            },
        }
        result = provider._parse_output(json.dumps(envelope), "", 0, _make_task())
        assert result.cost is not None
        assert result.cost.input_tokens == 250  # 50 + 200 cached
        assert result.cost.output_tokens == 10

    def test_gemini_plain_text_fallback(self) -> None:
        """If the CLI emits plain text instead of JSON, cost is None."""
        provider = GeminiProvider()
        result = provider._parse_output("just plain text", "", 0, _make_task())
        assert result.success is True
        assert result.content == "just plain text"
        assert result.cost is None
        assert result.metadata.get("raw_output") is True


# ═══════════════════════════════════════════════════════════════════════════
# PiProvider
# ═══════════════════════════════════════════════════════════════════════════


class TestPiRegistry:
    def test_registered(self) -> None:
        assert "pi" in PROVIDER_REGISTRY
        assert PROVIDER_REGISTRY["pi"] is PiProvider

    def test_get_provider(self) -> None:
        provider = get_provider("pi")
        assert isinstance(provider, PiProvider)
        assert provider.name == "pi"


class TestPiConformance:
    def test_isinstance(self) -> None:
        assert isinstance(PiProvider(), ExecutionProvider)

    def test_supports_tool_use(self) -> None:
        """Pi is a conversational model, not an agent runtime — no tool use."""
        assert PiProvider().supports_tool_use is False

    def test_supports_pooling(self) -> None:
        assert PiProvider().supports_pooling is False

    def test_provider_name(self) -> None:
        assert PiProvider().name == "pi"


class TestPiArgv:
    def test_basic_argv_contains_message_flag(self) -> None:
        provider = PiProvider(binary="/usr/bin/pi")
        task = _make_task(prompt="What is this code doing?")
        argv = provider._build_argv(task)

        assert argv[0] == "/usr/bin/pi"
        assert "--message" in argv
        idx = argv.index("--message")
        assert argv[idx + 1] == "What is this code doing?"

    def test_argv_only_contains_binary_and_message(self) -> None:
        """Pi has a minimal argv: just binary + --message + prompt."""
        provider = PiProvider(binary="pi")
        task = _make_task(prompt="Hello")
        argv = provider._build_argv(task)
        assert len(argv) == 3
        assert argv == ["pi", "--message", "Hello"]

    def test_api_key_not_in_argv(self) -> None:
        provider = PiProvider()
        task = _make_task(api_key="inflection-secret-key-abc123")
        argv = provider._build_argv(task)
        joined = " ".join(argv)
        assert "inflection-secret-key-abc123" not in joined

    def test_model_metadata_not_in_argv(self) -> None:
        """Pi has no --model flag — metadata model is ignored in argv."""
        provider = PiProvider()
        task = _make_task(model="pi-3")
        argv = provider._build_argv(task)
        assert "--model" not in argv
        assert "pi-3" not in argv

    def test_custom_binary_path(self) -> None:
        provider = PiProvider(binary="/custom/path/to/pi")
        argv = provider._build_argv(_make_task())
        assert argv[0] == "/custom/path/to/pi"

    def test_prompt_with_special_characters(self) -> None:
        """Prompts with dashes/pipes should appear verbatim in argv."""
        provider = PiProvider(binary="pi")
        task = _make_task(prompt="Analyze --- section: pipe | filter")
        argv = provider._build_argv(task)
        idx = argv.index("--message")
        assert argv[idx + 1] == "Analyze --- section: pipe | filter"


class TestPiEnv:
    def test_api_key_in_env(self) -> None:
        provider = PiProvider()
        task = _make_task(api_key="inflection-test-key")
        env = provider._build_env(task)
        assert env["INFLECTION_API_KEY"] == "inflection-test-key"

    def test_no_api_key_empty_env(self) -> None:
        provider = PiProvider()
        env = provider._build_env(_make_task())
        assert "INFLECTION_API_KEY" not in env
        assert env == {}

    def test_env_only_contains_api_key(self) -> None:
        """Only INFLECTION_API_KEY should appear, not other metadata."""
        provider = PiProvider()
        task = _make_task(api_key="key123", model="pi-3", phase="synthesis")
        env = provider._build_env(task)
        assert len(env) == 1
        assert env["INFLECTION_API_KEY"] == "key123"


class TestPiOutputParsing:
    def test_success_path_rc0(self) -> None:
        provider = PiProvider()
        task = _make_task()
        result = provider._parse_output("Here is my analysis.\n", "", 0, task)

        assert result.success is True
        assert result.content == "Here is my analysis."
        assert result.error is None
        assert result.provider == "pi"
        assert result.metadata["returncode"] == 0

    def test_success_strips_whitespace(self) -> None:
        provider = PiProvider()
        result = provider._parse_output("\n  response  \n", "", 0, _make_task())
        assert result.content == "response"

    def test_failure_path_nonzero_rc(self) -> None:
        provider = PiProvider()
        task = _make_task()
        result = provider._parse_output("", "connection refused", 1, task)

        assert result.success is False
        assert result.content is None
        assert result.error is not None
        assert result.error.category == "subprocess"
        assert "pi exited 1" in str(result.error)
        assert "connection refused" in str(result.error)
        assert result.provider == "pi"
        assert result.metadata["returncode"] == 1

    def test_failure_stderr_truncated_to_500(self) -> None:
        provider = PiProvider()
        long_stderr = "E" * 1000
        result = provider._parse_output("", long_stderr, 3, _make_task())

        assert result.success is False
        assert len(result.metadata["stderr"]) == 500

    def test_empty_stdout_success(self) -> None:
        provider = PiProvider()
        result = provider._parse_output("", "", 0, _make_task())
        assert result.success is True
        assert result.content == ""

    def test_output_path_propagated(self) -> None:
        provider = PiProvider()
        task = _make_task(output_path="/tmp/pi-output.md")
        result = provider._parse_output("content", "", 0, task)
        assert result.output_path == "/tmp/pi-output.md"

    def test_failure_preserves_returncode_in_metadata(self) -> None:
        provider = PiProvider()
        result = provider._parse_output("", "err", 137, _make_task())
        assert result.metadata["returncode"] == 137

    def test_failure_error_message_includes_exit_code(self) -> None:
        provider = PiProvider()
        result = provider._parse_output("", "timeout", 124, _make_task())
        assert "pi exited 124" in str(result.error)


# ═══════════════════════════════════════════════════════════════════════════
# CopilotProvider
# ═══════════════════════════════════════════════════════════════════════════


class TestCopilotRegistry:
    def test_registered(self) -> None:
        assert "copilot" in PROVIDER_REGISTRY
        assert PROVIDER_REGISTRY["copilot"] is CopilotProvider

    def test_get_provider(self) -> None:
        provider = get_provider("copilot")
        assert isinstance(provider, CopilotProvider)
        assert provider.name == "copilot"


class TestCopilotConformance:
    def test_isinstance(self) -> None:
        assert isinstance(CopilotProvider(), ExecutionProvider)

    def test_supports_tool_use(self) -> None:
        """Copilot CLI is explain/suggest, not an agent — no tool use."""
        assert CopilotProvider().supports_tool_use is False

    def test_supports_pooling(self) -> None:
        assert CopilotProvider().supports_pooling is False

    def test_provider_name(self) -> None:
        assert CopilotProvider().name == "copilot"


class TestCopilotArgv:
    def test_basic_argv_explain_mode(self) -> None:
        provider = CopilotProvider(binary="/usr/bin/gh")
        task = _make_task(prompt="What does this function do?")
        argv = provider._build_argv(task)

        assert argv[0] == "/usr/bin/gh"
        assert argv[1] == "copilot"
        assert argv[2] == "explain"
        assert argv[3] == "What does this function do?"

    def test_suggest_mode(self) -> None:
        """Mode can be set to 'suggest' for command generation."""
        provider = CopilotProvider(mode="suggest", binary="gh")
        task = _make_task(prompt="Find all python files")
        argv = provider._build_argv(task)

        assert argv[0] == "gh"
        assert argv[1] == "copilot"
        assert argv[2] == "suggest"
        assert argv[3] == "Find all python files"

    def test_argv_has_exactly_four_elements(self) -> None:
        """Copilot argv is minimal: gh copilot <mode> <prompt>."""
        provider = CopilotProvider(binary="gh")
        argv = provider._build_argv(_make_task(prompt="test"))
        assert len(argv) == 4

    def test_api_key_not_in_argv(self) -> None:
        """Even if api_key is in metadata, it must not leak to argv."""
        provider = CopilotProvider()
        task = _make_task(api_key="ghp_secret_token_12345")
        argv = provider._build_argv(task)
        joined = " ".join(argv)
        assert "ghp_secret_token_12345" not in joined

    def test_no_model_flag(self) -> None:
        """Copilot does not accept a --model flag."""
        provider = CopilotProvider()
        task = _make_task(model="gpt-4")
        argv = provider._build_argv(task)
        assert "--model" not in argv
        # model value should not appear in argv either
        assert "gpt-4" not in argv

    def test_default_mode_is_explain(self) -> None:
        provider = CopilotProvider(binary="gh")
        argv = provider._build_argv(_make_task())
        assert argv[2] == "explain"

    def test_custom_binary_path(self) -> None:
        provider = CopilotProvider(binary="/opt/homebrew/bin/gh")
        argv = provider._build_argv(_make_task())
        assert argv[0] == "/opt/homebrew/bin/gh"


class TestCopilotEnv:
    def test_env_always_empty(self) -> None:
        """Copilot uses gh auth, not API key env vars."""
        provider = CopilotProvider()
        env = provider._build_env(_make_task())
        assert env == {}

    def test_env_empty_even_with_api_key_metadata(self) -> None:
        """api_key in metadata is ignored — copilot relies on gh auth."""
        provider = CopilotProvider()
        task = _make_task(api_key="ghp_some_token")
        env = provider._build_env(task)
        assert env == {}
        assert "GITHUB_TOKEN" not in env
        assert "GH_TOKEN" not in env


class TestCopilotOutputParsing:
    def test_success_path_rc0(self) -> None:
        provider = CopilotProvider()
        task = _make_task()
        result = provider._parse_output(
            "This function sorts a list using quicksort.\n", "", 0, task,
        )

        assert result.success is True
        assert result.content == "This function sorts a list using quicksort."
        assert result.error is None
        assert result.provider == "copilot"
        assert result.metadata["returncode"] == 0

    def test_success_strips_whitespace(self) -> None:
        provider = CopilotProvider()
        result = provider._parse_output("  output  \n", "", 0, _make_task())
        assert result.content == "output"

    def test_failure_path_nonzero_rc(self) -> None:
        provider = CopilotProvider()
        task = _make_task()
        result = provider._parse_output("", "not authenticated", 1, task)

        assert result.success is False
        assert result.content is None
        assert result.error is not None
        assert result.error.category == "subprocess"
        assert "gh copilot exited 1" in str(result.error)
        assert "not authenticated" in str(result.error)
        assert result.provider == "copilot"
        assert result.metadata["returncode"] == 1

    def test_failure_stderr_truncated_to_500(self) -> None:
        provider = CopilotProvider()
        long_stderr = "Z" * 1000
        result = provider._parse_output("", long_stderr, 1, _make_task())

        assert result.success is False
        assert len(result.metadata["stderr"]) == 500

    def test_empty_stdout_success(self) -> None:
        provider = CopilotProvider()
        result = provider._parse_output("", "", 0, _make_task())
        assert result.success is True
        assert result.content == ""

    def test_output_path_propagated(self) -> None:
        provider = CopilotProvider()
        task = _make_task(output_path="/tmp/copilot-output.md")
        result = provider._parse_output("explanation", "", 0, task)
        assert result.output_path == "/tmp/copilot-output.md"

    def test_failure_various_exit_codes(self) -> None:
        """Different exit codes are reported correctly in the error message."""
        provider = CopilotProvider()
        for rc in [1, 2, 127, 130]:
            result = provider._parse_output("", "err", rc, _make_task())
            assert result.success is False
            assert f"gh copilot exited {rc}" in str(result.error)
            assert result.metadata["returncode"] == rc


# ═══════════════════════════════════════════════════════════════════════════
# Cross-provider: full registry inventory
# ═══════════════════════════════════════════════════════════════════════════


class TestFullRegistry:
    """Verify all expected providers are registered after package import."""

    def test_all_providers_present(self) -> None:
        expected = {"mock", "anthropic", "claude-code", "aider", "opencode", "codex", "copilot", "pi"}
        assert expected.issubset(set(PROVIDER_REGISTRY.keys()))

    # Known aliases: registry name → canonical provider name
    _ALIASES = {"demo": "mock"}

    def test_all_providers_instantiate(self) -> None:
        for name in PROVIDER_REGISTRY:
            provider = get_provider(name)
            assert isinstance(provider, ExecutionProvider)
            expected = self._ALIASES.get(name, name)
            assert provider.name == expected, (
                f"Registry name {name!r}: expected provider.name={expected!r}, "
                f"got {provider.name!r}"
            )

    def test_unknown_provider_error_lists_all(self) -> None:
        with pytest.raises(ValueError, match="Available:"):
            get_provider("nonexistent")


# ═══════════════════════════════════════════════════════════════════════════
# Live integration tests (skipped by default, run with -m live)
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.live
class TestClaudeCodeLive:
    """Actually spawn ``claude -p`` and verify end-to-end.

    These tests are slow (~2-5s each) and cost real API credits.
    Run with: ``pytest -m live engine/tests/test_concrete_providers.py``
    """

    @pytest.fixture(autouse=True)
    def _skip_if_no_binary(self) -> None:
        if not shutil.which("claude"):
            pytest.skip("claude binary not found")

    def test_ping_pong(self) -> None:
        """The simplest possible live test: ask for 'pong', get 'pong'."""
        provider = ClaudeCodeProvider(
            model="haiku",
            skip_permissions=True,
        )
        task = _make_task(prompt="Reply with exactly the word pong. No other text.")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content is not None
        assert "pong" in result.content.lower()
        assert result.cost is not None
        assert result.cost.usd is not None
        assert result.cost.usd > 0
        assert result.duration is not None
        assert result.duration.total_seconds() > 0
        assert result.provider == "claude-code"

    def test_cost_telemetry(self) -> None:
        """Verify cost data is structured and realistic."""
        provider = ClaudeCodeProvider(model="haiku")
        task = _make_task(prompt="Say hello in one word.")
        result = asyncio.run(provider.execute(task))

        assert result.cost is not None
        assert result.cost.input_tokens > 0
        assert result.cost.output_tokens > 0
        assert result.cost.usd is not None


@pytest.mark.live
class TestAiderLive:
    """Live aider tests."""

    @pytest.fixture(autouse=True)
    def _skip_if_no_binary(self) -> None:
        if not shutil.which("aider"):
            pytest.skip("aider binary not found")

    def test_basic_message(self) -> None:
        provider = AiderProvider(model="sonnet")
        task = _make_task(prompt="Reply with exactly: hello from aider")
        result = asyncio.run(provider.execute(task))
        # Aider may or may not succeed depending on auth config
        assert isinstance(result, ExecutionResult)
        assert result.provider == "aider"
