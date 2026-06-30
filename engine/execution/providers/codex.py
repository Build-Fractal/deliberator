"""OpenAI Codex CLI subprocess execution provider.

Wraps the ``codex`` CLI (OpenAI's coding agent) as an
:class:`ExecutionProvider` via :class:`SubprocessProvider`.

Codex is OpenAI's answer to Claude Code — a terminal-based coding agent
with file read/write, shell execution, and multi-turn conversation.
Non-interactive mode uses the ``exec`` subcommand:

    codex exec --json --output-last-message <tmpfile> "<prompt>"

The ``--json`` (alias ``--experimental-json``) flag emits newline-delimited
JSON events on stdout; ``--output-last-message`` writes the final assistant
text to a file we can read back deterministically (no need to scrape the
event stream for the last ``agent_message``).

Per ``codex-rs/protocol/src/protocol.rs``, ``token_count`` events carry
the cumulative running totals (``info.total_token_usage``) and per-turn
delta (``info.last_token_usage``).  We take the **last** ``token_count``
event's ``total_token_usage`` rather than summing — because each event
already contains the running cumulative count.

Install: ``npm install -g @openai/codex``
Reference: https://developers.openai.com/codex/cli/reference
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from typing import Any

from engine.execution.provider import Cost, ExecutionResult, ExecutionTask
from engine.execution.providers.subprocess_base import SubprocessProvider
from engine.providers import ProviderError

DEFAULT_TIMEOUT = 600


class CodexProvider(SubprocessProvider):
    """Execute deliberator agent tasks via the OpenAI ``codex`` CLI.

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
        # Per-task last-message tempfile path.  Set in ``_build_argv``
        # and consumed in ``_parse_output``.  Single-task lifecycle —
        # SubprocessProvider runs each ``execute()`` independently so
        # there's no overlap concern.
        self._last_message_path: str | None = None

    @property
    def name(self) -> str:
        return "codex"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        # Issue #54 contract: None means "no override, use provider default".
        model = task.metadata.get("model") or self._model
        # Allocate a per-task tempfile for the final assistant message.
        # We use ``mkstemp`` (not ``NamedTemporaryFile``) so the path
        # outlives the descriptor — codex opens the path itself.  The
        # file is cleaned up in ``_parse_output`` after we read it.
        fd, path = tempfile.mkstemp(prefix="codex-last-msg-", suffix=".txt")
        os.close(fd)
        self._last_message_path = path
        return [
            self._binary,
            "exec",
            "--json",
            "--output-last-message", path,
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
        # Always read+remove the per-task tempfile, even on failure.
        last_message_text = self._consume_last_message_file()

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

        # Token usage: take the LAST ``token_count`` event's
        # ``total_token_usage`` — codex emits cumulative counts per
        # turn so summing would double-count.  Falls back to the
        # legacy flat ``input_tokens``/``output_tokens`` shape for
        # robustness against future schema changes.
        cost = _last_token_count_from_jsonl(stdout)

        # Prefer the deterministic last-message file over scraping the
        # event stream.  When the file is missing or empty (older codex
        # versions, or stream that didn't reach a final message) fall
        # back to the last ``agent_message`` event, then to raw stdout.
        agent_text: str | None = last_message_text
        if not agent_text:
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

    def _consume_last_message_file(self) -> str | None:
        """Read and remove the per-task ``--output-last-message`` file.

        Returns the trimmed contents, or ``None`` if the file is
        absent/empty/unreadable.  Always clears ``self._last_message_path``
        so a stale path can't leak into the next task.
        """
        path = self._last_message_path
        self._last_message_path = None
        if not path:
            return None
        try:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read().strip()
        except OSError:
            text = ""
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass
        return text or None


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


def _last_token_count_from_jsonl(stdout: str) -> Cost | None:
    """Return the last ``token_count`` event as a :class:`Cost`, or ``None``.

    Codex's ``token_count`` event payload (``info.total_token_usage``)
    is **cumulative**: each event resets the running totals to the latest
    snapshot, not a per-turn delta.  Taking the last event therefore
    yields the full session cost.

    Schema (per ``codex-rs/protocol/src/protocol.rs``)::

        {
          "type": "token_count",
          "info": {
            "total_token_usage": {
              "input_tokens": N,
              "cached_input_tokens": N,
              "output_tokens": N,
              "reasoning_output_tokens": N,
              "total_tokens": N
            },
            "last_token_usage": {...},
            "model_context_window": N
          },
          "rate_limits": {...}
        }

    For backward compatibility with the older flat shape
    ``{"type": "token_count", "input_tokens": N, "output_tokens": N}``
    (and the ``msg``-envelope form), we sum that variant across events
    if no ``info`` block is present.
    """
    last_total: dict[str, Any] | None = None
    flat_input_sum = 0
    flat_output_sum = 0
    saw_flat = False

    for obj in _iter_jsonl(stdout):
        # Tolerate optional ``msg`` envelope.
        msg = obj.get("msg") if isinstance(obj.get("msg"), dict) else obj
        kind = obj.get("type") or obj.get("event") or msg.get("type")
        if kind != "token_count":
            continue

        # Preferred shape: {info: {total_token_usage: {...}}}
        info = msg.get("info")
        if isinstance(info, dict):
            total = info.get("total_token_usage")
            if isinstance(total, dict):
                last_total = total
                continue

        # Legacy flat shape: {input_tokens, output_tokens} on the event itself.
        if "input_tokens" in msg or "output_tokens" in msg:
            flat_input_sum += int(msg.get("input_tokens", 0) or 0)
            flat_output_sum += int(msg.get("output_tokens", 0) or 0)
            saw_flat = True

    if last_total is not None:
        # Fold cached_input_tokens into input (it's still prompt context
        # the user paid attention budget for, matching how anthropic and
        # gemini providers handle their cache fields).
        input_tokens = (
            int(last_total.get("input_tokens", 0) or 0)
            + int(last_total.get("cached_input_tokens", 0) or 0)
        )
        # Reasoning tokens are billed as output; fold them in.
        output_tokens = (
            int(last_total.get("output_tokens", 0) or 0)
            + int(last_total.get("reasoning_output_tokens", 0) or 0)
        )
        return Cost(input_tokens=input_tokens, output_tokens=output_tokens, usd=None)

    if saw_flat:
        return Cost(
            input_tokens=flat_input_sum,
            output_tokens=flat_output_sum,
            usd=None,
        )

    return None


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
