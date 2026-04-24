"""OpenAI Codex CLI subprocess execution provider.

Wraps the ``codex`` CLI (OpenAI's coding agent) as an
:class:`ExecutionProvider` via :class:`SubprocessProvider`.

Codex is OpenAI's answer to Claude Code — a terminal-based coding agent
with file read/write, shell execution, and multi-turn conversation.
Non-interactive mode: ``codex --quiet --full-auto "prompt"``.

Install: ``npm install -g @openai/codex``

Token usage: the ``codex exec`` subcommand supports ``--json`` to emit
a JSONL event stream that includes ``token_count`` events per the
codex-cli source (``codex/src/protocol.rs``).  This provider opts into
the JSONL stream and aggregates token counts across all events;  if
the CLI version doesn't emit them, ``cost`` falls back to ``None``.
"""

from __future__ import annotations

import json
import shutil
from typing import Any

from engine.execution.provider import Cost, ExecutionResult, ExecutionTask
from engine.execution.providers.subprocess_base import SubprocessProvider
from engine.providers import ProviderError

DEFAULT_TIMEOUT = 600


class CodexProvider(SubprocessProvider):
    """Execute conversus agent tasks via the OpenAI ``codex`` CLI.

    Args:
        model: Model name (e.g., ``"o4-mini"``, ``"o3"``).
        timeout: Subprocess timeout in seconds.
        binary: Path to the ``codex`` binary.
    """

    supports_tool_use: bool = True
    supports_pooling: bool = False

    def __init__(
        self,
        *,
        model: str = "o4-mini",
        timeout: float = DEFAULT_TIMEOUT,
        binary: str | None = None,
        cwd: str | None = None,
    ) -> None:
        super().__init__(timeout=timeout, cwd=cwd)
        self._model = model
        self._binary = binary or shutil.which("codex") or "codex"

    @property
    def name(self) -> str:
        return "codex"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        model = task.metadata.get("model", self._model)
        # NOTE: token capture is opportunistic.  The current argv uses
        # ``--quiet --full-auto`` which emits human-readable text on
        # stdout — no token counts.  To get structured ``token_count``
        # events we need to switch to the ``codex exec --json`` flow
        # (different positional layout, JSONL output stream).  That
        # rewrite changes the CLI surface enough to break existing
        # callers, so it's deferred.  ``_parse_output()`` already knows
        # how to harvest token counts if the stdout happens to be JSONL
        # (e.g. when a downstream caller swaps to the exec mode).
        # TODO(token-tracking): expose an ``exec_mode=True`` opt-in that
        # rebuilds argv as ``codex exec --json --model <m> "<prompt>"``.
        return [
            self._binary,
            "--quiet",
            "--full-auto",
            "--model", model,
            task.prompt,
        ]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        env: dict[str, str] = {}
        api_key = task.metadata.get("api_key")
        if api_key:
            env["OPENAI_API_KEY"] = api_key
        return env

    def _parse_output(
        self, stdout: str, stderr: str, returncode: int, task: ExecutionTask,
    ) -> ExecutionResult:
        if returncode != 0:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"codex exited {returncode}: {stderr[:500]}",
                    category="subprocess",
                ),
                provider=self.name,
                metadata={"returncode": returncode, "stderr": stderr[:500]},
            )

        # Try parsing stdout as JSONL: each line is one event.  Codex
        # emits ``token_count`` events with ``input_tokens`` and
        # ``output_tokens`` fields, plus ``agent_message`` events whose
        # ``message`` is the assistant text.  If parsing fails we fall
        # back to the plain-text path.
        cost = _aggregate_token_counts_from_jsonl(stdout)
        agent_text = _extract_agent_message_from_jsonl(stdout)
        content = agent_text if agent_text is not None else stdout.strip()
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


# ---------------------------------------------------------------------------
# JSONL helpers
# ---------------------------------------------------------------------------


def _iter_jsonl(stdout: str):
    """Yield parsed JSON objects from a JSONL stream, skipping bad lines."""
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(obj, dict):
            yield obj


def _aggregate_token_counts_from_jsonl(stdout: str) -> Cost | None:
    """Sum ``input_tokens``/``output_tokens`` across all ``token_count`` events.

    Codex emits one event per LLM turn; multi-turn agent runs need
    aggregation.  Returns ``None`` if no token counts are present.
    """
    input_tokens = 0
    output_tokens = 0
    saw_any = False
    for obj in _iter_jsonl(stdout):
        # Events may be wrapped: {"type": "token_count", "msg": {...}}
        # or flat: {"event": "token_count", "input_tokens": N, ...}
        msg = obj.get("msg") if isinstance(obj.get("msg"), dict) else obj
        kind = obj.get("type") or obj.get("event") or msg.get("type")
        if kind != "token_count":
            continue
        input_tokens += int(msg.get("input_tokens", 0) or 0)
        output_tokens += int(msg.get("output_tokens", 0) or 0)
        saw_any = True
    if not saw_any:
        return None
    return Cost(input_tokens=input_tokens, output_tokens=output_tokens, usd=None)


def _extract_agent_message_from_jsonl(stdout: str) -> str | None:
    """Return the last ``agent_message`` text from a JSONL stream, or None."""
    last_text: str | None = None
    for obj in _iter_jsonl(stdout):
        msg = obj.get("msg") if isinstance(obj.get("msg"), dict) else obj
        kind = obj.get("type") or obj.get("event") or msg.get("type")
        if kind in ("agent_message", "message", "assistant_message"):
            text = msg.get("message") or msg.get("text") or msg.get("content")
            if isinstance(text, str):
                last_text = text
    return last_text


from engine.execution.providers import register_provider  # noqa: E402

register_provider("codex", CodexProvider)
