"""OpenCode subprocess execution provider.

Wraps the ``opencode`` CLI as an :class:`ExecutionProvider` via
:class:`SubprocessProvider`.  Uses ``opencode run --format json
"message"`` for non-interactive execution with a parseable event
stream.

Repo: https://opencode.ai/

OpenCode is a Go-based coding agent that supports Anthropic, OpenAI,
and other providers.  It has a TUI, a web UI, and a headless ``run``
mode suitable for subprocess dispatch.

Key flags:
- ``opencode run "message"`` — non-interactive execution
- ``--format json`` — emit raw JSON events on stdout (includes a
  ``message`` event whose ``info.tokens`` block carries
  ``input``/``output``/``reasoning``/``cache.{read,write}``)
- OpenCode reads configuration from ``.opencode/config.toml``
"""

from __future__ import annotations

import json
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

DEFAULT_TIMEOUT = 300


# ---------------------------------------------------------------------------
# OpenCodeProvider
# ---------------------------------------------------------------------------


class OpenCodeProvider(SubprocessProvider):
    """Execute deliberator agent tasks via the ``opencode`` CLI.

    Args:
        timeout: Subprocess timeout in seconds.
        binary: Path to the ``opencode`` binary.  Auto-detected from PATH.
    """

    supports_tool_use: bool = True
    supports_pooling: bool = False

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        binary: str | None = None,
        cwd: str | None = None,
    ) -> None:
        super().__init__(timeout=timeout, cwd=cwd)
        self._binary = binary or shutil.which("opencode") or "opencode"

    @property
    def name(self) -> str:
        return "opencode"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        # ``--format json`` emits a JSONL event stream that includes a
        # ``message`` event whose ``info.tokens.{input,output,...}``
        # block carries token usage.  Without it, opencode prints
        # human-formatted text — no token telemetry.
        argv = [
            self._binary,
            "run",
            "--format", "json",
            task.prompt,
        ]
        return argv

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        env: dict[str, str] = {}
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
        """Parse opencode output — JSONL events when ``--format json`` is set.

        Opencode emits a stream of events on stdout; ``message`` events
        with ``info.role == "assistant"`` carry the agent's text in
        ``parts[*].text`` and token totals in
        ``info.tokens.{input,output,reasoning,cache:{read,write}}``.
        Older versions or human-format runs may emit plain text — fall
        back to that path with ``cost=None``.
        """
        if returncode != 0:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=stdout.strip() if stdout else None,
                error=ProviderError(
                    f"opencode exited {returncode}: {stderr[:500]}",
                    category="subprocess",
                ),
                provider=self.name,
                metadata={"returncode": returncode, "stderr": stderr[:500]},
            )

        cost, agent_text = _parse_opencode_jsonl(stdout)
        content = agent_text if agent_text is not None else (stdout.strip() if stdout else None)
        metadata: dict[str, Any] = {"returncode": returncode}
        if agent_text is None:
            metadata["raw_output"] = True

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=content,
            error=None,
            cost=cost,
            provider=self.name,
            metadata=metadata,
        )


def _parse_opencode_jsonl(stdout: str) -> tuple[Cost | None, str | None]:
    """Extract (cost, last assistant text) from an opencode JSONL stream.

    Returns ``(None, None)`` if stdout is not parseable as JSONL or
    contains no recognisable assistant message.
    """
    if not stdout:
        return None, None

    cost: Cost | None = None
    assistant_text: str | None = None
    saw_any_json = False

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(obj, dict):
            continue
        saw_any_json = True

        # Event envelope: {"type": "message", "properties": {...}}
        # or flat {"info": {...}, "parts": [...]} on some versions.
        info = obj.get("info") if isinstance(obj.get("info"), dict) else None
        parts = obj.get("parts") if isinstance(obj.get("parts"), list) else None
        if info is None and isinstance(obj.get("properties"), dict):
            props = obj["properties"]
            info = props.get("info") if isinstance(props.get("info"), dict) else None
            parts = props.get("parts") if isinstance(props.get("parts"), list) else None
        if info is None:
            continue
        if info.get("role") != "assistant":
            continue

        # Token totals live on ``info.tokens``.
        tokens = info.get("tokens")
        if isinstance(tokens, dict):
            input_tokens = int(tokens.get("input", 0) or 0)
            output_tokens = int(tokens.get("output", 0) or 0)
            output_tokens += int(tokens.get("reasoning", 0) or 0)
            cache = tokens.get("cache")
            if isinstance(cache, dict):
                input_tokens += int(cache.get("read", 0) or 0)
                input_tokens += int(cache.get("write", 0) or 0)
            if input_tokens or output_tokens:
                cost = Cost(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    usd=None,
                )

        # Concatenate text parts for content.
        if isinstance(parts, list):
            chunks = [
                p.get("text") for p in parts
                if isinstance(p, dict) and isinstance(p.get("text"), str)
            ]
            if chunks:
                assistant_text = "\n".join(chunks).strip()

    if not saw_any_json:
        return None, None
    return cost, assistant_text


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

from engine.execution.providers import register_provider  # noqa: E402

register_provider("opencode", OpenCodeProvider)
