"""Claude Code subprocess execution provider.

Install: ``npm install -g @anthropic-ai/claude-code``
Repo: https://github.com/anthropics/claude-code

Wraps the ``claude`` CLI (Claude Code) as an :class:`ExecutionProvider` via
:class:`SubprocessProvider`.  Uses ``claude -p`` (print mode) for
non-interactive single-shot execution with JSON output for structured
result parsing.

This is the **primary Tier 1 agent runtime** in the spec 042 provider
hierarchy: ``claude-code`` supports tool use, autonomous file reading,
and writing — the agent manages its own I/O.  The engine passes the
prompt and read paths but does NOT pre-read files into the prompt
(unlike ``anthropic`` or ``litellm`` where ``supports_tool_use=False``).

Key design decisions:

- **JSON output format**: ``--output-format json`` gives us structured
  results including ``total_cost_usd``, ``duration_ms``, ``num_turns``,
  and per-model usage breakdown.  This satisfies binding conditions #5
  (cost telemetry) and #6 (structured duration) natively.
- **No permission prompts**: ``--dangerously-skip-permissions`` is
  required for headless execution.  Conversus runs agents in controlled
  sandbox directories — each agent writes to its own output path.
- **No session persistence**: ``--no-session-persistence`` prevents
  polluting the user's session list with deliberation noise.
- **Env-only secrets**: ``ANTHROPIC_API_KEY`` is passed via env, never
  argv (inherited from :class:`SubprocessProvider` security model).
- **Cold start**: ~1-3s per invocation due to Node.js startup + MCP
  server init.  ``warm()`` is stubbed for future process pool.
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import timedelta
from typing import Any

from engine.execution.provider import (
    Cost,
    ExecutionResult,
    ExecutionTask,
)
from engine.execution.providers.subprocess_base import SubprocessProvider
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

#: Default model — use the most capable Claude model available.
DEFAULT_MODEL = "sonnet"

#: Default timeout for claude-code invocations (seconds).
#: Higher than the base default because claude-code may do multi-turn
#: tool use that takes longer than a single completion.  Opus with
#: large doc sets (3000+ lines) can take 10+ minutes per agent.
DEFAULT_TIMEOUT = 1200


# ---------------------------------------------------------------------------
# ClaudeCodeProvider
# ---------------------------------------------------------------------------


class ClaudeCodeProvider(SubprocessProvider):
    """Execute conversus agent tasks via the ``claude`` CLI.

    Args:
        model: Model alias or full name (e.g., ``"sonnet"``, ``"opus"``,
            ``"claude-sonnet-4-20250514"``).  Per-task override via
            ``task.metadata["model"]``.
        timeout: Subprocess timeout in seconds.  Per-task override via
            ``task.metadata["timeout"]``.
        binary: Path to the ``claude`` binary.  Auto-detected from PATH
            if not provided.
        system_prompt: Optional system prompt prepended to every task.
        allowed_tools: Optional list of tools the agent is allowed to use.
            Empty string ``""`` means no tools.  ``None`` means all tools.
        max_budget_usd: Optional per-invocation cost cap.
        skip_permissions: If True (default), pass
            ``--dangerously-skip-permissions`` for headless execution.
    """

    supports_tool_use: bool = True
    supports_pooling: bool = False  # Future: process pool

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        timeout: float = DEFAULT_TIMEOUT,
        binary: str | None = None,
        system_prompt: str | None = None,
        allowed_tools: str | None = None,
        max_budget_usd: float | None = None,
        skip_permissions: bool = True,
        mcp_config: str | None = None,
        cwd: str | None = None,
    ) -> None:
        # If a .conversus/ dir exists with .claude/settings.json, use it
        # as cwd so claude picks up the permission grants automatically.
        # This means skip_permissions can be False when init has been run.
        if cwd is None:
            from engine.project import find_conversus_dir, read_settings
            from pathlib import Path

            conversus_dir = find_conversus_dir(Path.cwd())
            if conversus_dir and (conversus_dir / ".claude" / "settings.json").exists():
                cwd = str(conversus_dir)
                # If project has settings, respect its skip_permissions pref
                settings = read_settings(conversus_dir.parent)
                skip_permissions = settings.get("skip_permissions", skip_permissions)

        super().__init__(timeout=timeout, cwd=cwd)
        self._model = model
        self._binary = binary or shutil.which("claude") or "claude"
        self._system_prompt = system_prompt
        self._allowed_tools = allowed_tools
        self._max_budget_usd = max_budget_usd
        self._skip_permissions = skip_permissions
        self._mcp_config = mcp_config

    @property
    def name(self) -> str:
        return "claude-code"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        # Issue #54 contract: ``task.metadata.get("model")`` returns
        # ``None`` when the dispatch layer did not pin a specific model
        # id — fall back to this provider's own configured default
        # (the ``"sonnet"`` alias by default, which ``claude -p``
        # resolves against the calling OAuth session). The prior
        # value-blocklist guard against ``DEFAULT_MODEL``'s literal
        # leak (PR #52) is retired now that dispatch passes ``None``
        # rather than the literal.
        model = task.metadata.get("model") or self._model

        # Prompt is piped via stdin (see _build_stdin) rather than argv,
        # because prompts containing "---" markers (from file inlining)
        # get misinterpreted as CLI option flags.
        argv = [
            self._binary,
            "-p",  # print mode — reads prompt from stdin when no positional arg
            "--output-format", "json",
            "--no-session-persistence",
            "--model", model,
        ]

        if self._skip_permissions:
            argv.append("--dangerously-skip-permissions")

        if self._system_prompt:
            argv.extend(["--system-prompt", self._system_prompt])

        if self._allowed_tools is not None:
            argv.extend(["--allowedTools", self._allowed_tools])

        if self._max_budget_usd is not None:
            argv.extend(["--max-budget-usd", str(self._max_budget_usd)])

        if self._mcp_config is not None:
            argv.extend(["--mcp-config", self._mcp_config])

        # Pass read paths as --add-dir so the agent can read them
        for path in task.read_paths:
            argv.extend(["--add-dir", path])

        return argv

    def _build_stdin(self, task: ExecutionTask) -> bytes | None:
        """Pipe the prompt via stdin to avoid CLI flag misinterpretation."""
        return task.prompt.encode("utf-8")

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        env: dict[str, str] = {}
        # Pass API key from task metadata if provided (e.g., per-org keys)
        api_key = task.metadata.get("api_key")
        if api_key:
            env["ANTHROPIC_API_KEY"] = api_key
        return env

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        """Parse claude CLI JSON output into an ExecutionResult.

        The JSON output is an array of message objects.  We extract:
        - Text content from ``assistant`` messages
        - Cost/duration from the ``result`` message
        - Error details from the ``result`` message if ``is_error=True``
        """
        # Try to parse JSON
        try:
            parsed = json.loads(stdout)
        except (json.JSONDecodeError, ValueError):
            # Fallback: if not valid JSON, treat stdout as raw text
            if returncode != 0:
                return ExecutionResult(
                    success=False,
                    output_path=task.output_path,
                    content=None,
                    error=ProviderError(
                        f"claude-code exited {returncode}: {stderr[:500]}",
                        category="subprocess",
                    ),
                    provider=self.name,
                    metadata={"returncode": returncode, "stderr": stderr[:500]},
                )
            return ExecutionResult(
                success=True,
                output_path=task.output_path,
                content=stdout.strip(),
                provider=self.name,
                metadata={"returncode": returncode, "raw_output": True},
            )

        # `claude -p --output-format json` historically returned an array
        # of message objects (system/assistant/result).  Current `claude`
        # (>= 2.x) returns a single result object with the assistant text
        # in a top-level `result` field.  Support both shapes so the
        # provider works across claude-code versions — and against the
        # Max-plan OAuth surface where each subprocess is a fresh
        # interactive session.
        if isinstance(parsed, list):
            messages = parsed
            text_parts: list[str] = []
            for msg in messages:
                if isinstance(msg, dict) and msg.get("type") == "assistant":
                    content_blocks = msg.get("message", {}).get("content", [])
                    for block in content_blocks:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block["text"])
            content = "\n\n".join(text_parts) if text_parts else None
            result_msg = next(
                (m for m in messages if isinstance(m, dict) and m.get("type") == "result"),
                {},
            )
        elif isinstance(parsed, dict):
            result_msg = parsed
            result_text = result_msg.get("result")
            content = result_text if isinstance(result_text, str) and result_text else None
        else:
            # JSON parsed to a scalar (unexpected shape).  Treat as raw.
            return ExecutionResult(
                success=returncode == 0,
                output_path=task.output_path,
                content=stdout.strip() or None,
                provider=self.name,
                metadata={"returncode": returncode, "raw_output": True},
            )

        is_error = result_msg.get("is_error", False)
        cost_usd = result_msg.get("total_cost_usd")
        duration_ms = result_msg.get("duration_ms")
        num_turns = result_msg.get("num_turns", 0)

        # Extract token usage from modelUsage
        model_usage = result_msg.get("modelUsage", {})
        input_tokens = 0
        output_tokens = 0
        for _model_name, usage in model_usage.items():
            input_tokens += usage.get("inputTokens", 0)
            input_tokens += usage.get("cacheCreationInputTokens", 0)
            input_tokens += usage.get("cacheReadInputTokens", 0)
            output_tokens += usage.get("outputTokens", 0)

        cost = Cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            usd=cost_usd,
        ) if (input_tokens or output_tokens or cost_usd) else None

        duration = (
            timedelta(milliseconds=duration_ms)
            if duration_ms is not None
            else None
        )

        # Tool-use-only success: when the agent completes its task solely
        # via tool invocations (e.g., Write to task.output_path) and emits
        # no final text block, text_parts is empty and content is None.
        # In that mode the CLI's result envelope may spuriously surface
        # is_error=True even though the artifact is on disk.  Trust the
        # artifact: if task.output_path was written, treat as success.
        try:
            output_written = (
                os.path.exists(task.output_path)
                and os.path.getsize(task.output_path) > 0
            )
        except OSError:
            output_written = False

        if is_error and not content and not output_written:
            errors = result_msg.get("errors", [])
            error_msg = "; ".join(errors) if errors else f"claude-code reported error (rc={returncode})"
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=content,
                error=ProviderError(error_msg, category="subprocess"),
                cost=cost,
                duration=duration,
                provider=self.name,
                metadata={
                    "returncode": returncode,
                    "num_turns": num_turns,
                    "errors": errors,
                },
            )

        metadata: dict[str, Any] = {
            "returncode": returncode,
            "num_turns": num_turns,
            "stop_reason": result_msg.get("stop_reason"),
        }
        if is_error and not content and output_written:
            metadata["tool_use_only"] = True
            metadata["errors"] = result_msg.get("errors", [])

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=content,
            error=None,
            cost=cost,
            duration=duration,
            provider=self.name,
            metadata=metadata,
        )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

from engine.execution.providers import register_provider  # noqa: E402

register_provider("claude-code", ClaudeCodeProvider)
