"""Aider subprocess execution provider.

Wraps the ``aider`` CLI as an :class:`ExecutionProvider` via
:class:`SubprocessProvider`.  Uses ``aider --message ... --exit`` for
non-interactive single-shot execution.

Install: ``pip install aider-chat``
Docs: https://aider.chat/docs/install.html

Aider is a Tier 1 agent runtime — it supports autonomous code editing
via its diff-based edit system.  However, for conversus deliberation
tasks, we use it in a simpler mode: send a message, capture the
response, exit.  Aider's full editing capabilities are available via
the ``--file`` flag for tasks that need file modification.

Key flags:
- ``--message "prompt"`` — send a single message non-interactively
- ``--exit`` — exit after processing the message
- ``--yes-always`` — auto-accept all prompts
- ``--no-stream`` — buffer output for clean capture
- ``--no-auto-commits`` — don't auto-commit changes
- ``--no-auto-lint`` — don't auto-lint
- ``--model`` — model selection (supports anthropic, openai, etc.)
"""

from __future__ import annotations

import re
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


# Aider prints a "Tokens" summary line after each message in --no-stream
# mode; we parse it for token telemetry.  Format examples:
#   "Tokens: 1.2k sent, 234 received."
#   "Tokens: 1,234 sent, 567 received. Cost: $0.0042 message, $0.04 session."
#   "Tokens: 12 sent, 8 received."
_AIDER_TOKENS_RE = re.compile(
    r"Tokens:\s*([\d,.]+\s*[kKmM]?)\s+sent,\s*([\d,.]+\s*[kKmM]?)\s+received",
)


def _parse_count(raw: str) -> int:
    """Parse an aider token count like '1.2k', '234', or '1,234' → int."""
    s = raw.strip().replace(",", "")
    multiplier = 1
    if s and s[-1] in "kK":
        multiplier = 1_000
        s = s[:-1]
    elif s and s[-1] in "mM":
        multiplier = 1_000_000
        s = s[:-1]
    try:
        return int(round(float(s) * multiplier))
    except (TypeError, ValueError):
        return 0


def _parse_aider_token_summary(text: str) -> Cost | None:
    """Return a Cost from the latest 'Tokens: X sent, Y received' line, or None."""
    if not text:
        return None
    matches = list(_AIDER_TOKENS_RE.finditer(text))
    if not matches:
        return None
    # Use the last match — covers multi-message --message runs that
    # reprint the line each turn.
    last = matches[-1]
    return Cost(
        input_tokens=_parse_count(last.group(1)),
        output_tokens=_parse_count(last.group(2)),
        usd=None,
    )


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "sonnet"
DEFAULT_TIMEOUT = 300


# ---------------------------------------------------------------------------
# AiderProvider
# ---------------------------------------------------------------------------


class AiderProvider(SubprocessProvider):
    """Execute conversus agent tasks via the ``aider`` CLI.

    Args:
        model: Model name (e.g., ``"sonnet"``, ``"claude-3-5-sonnet"``).
            Per-task override via ``task.metadata["model"]``.
        timeout: Subprocess timeout in seconds.
        binary: Path to the ``aider`` binary.  Auto-detected from PATH.
        extra_flags: Additional CLI flags to pass (e.g., ``["--architect"]``).
    """

    supports_tool_use: bool = True
    supports_pooling: bool = False

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        timeout: float = DEFAULT_TIMEOUT,
        binary: str | None = None,
        extra_flags: list[str] | None = None,
        cwd: str | None = None,
    ) -> None:
        super().__init__(timeout=timeout, cwd=cwd)
        self._model = model
        self._binary = binary or shutil.which("aider") or "aider"
        self._extra_flags = extra_flags or []

    @property
    def name(self) -> str:
        return "aider"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        model = task.metadata.get("model", self._model)

        argv = [
            self._binary,
            "--message", task.prompt,
            "--exit",
            "--yes-always",
            "--no-stream",
            "--no-auto-commits",
            "--no-auto-lint",
            "--model", model,
        ]

        # Add files for aider to read/edit
        for path in task.read_paths:
            argv.extend(["--file", path])

        argv.extend(self._extra_flags)
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
        """Parse aider output — plain text, strip ANSI codes and prompt noise."""
        # Aider output includes prompts, diffs, and the actual response.
        # We capture everything — the caller can filter if needed.
        content = stdout.strip() if stdout else None

        if returncode != 0:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=content,
                error=ProviderError(
                    f"aider exited {returncode}: {stderr[:500]}",
                    category="subprocess",
                ),
                provider=self.name,
                metadata={"returncode": returncode, "stderr": stderr[:500]},
            )

        # Aider prints a "Tokens: X sent, Y received." line after each
        # turn (in --no-stream mode); parse it best-effort.  ``None`` when
        # the line is absent (e.g., aider --help, --show-prompts, or
        # exit-before-message paths).
        cost = _parse_aider_token_summary(stdout)

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=content,
            error=None,
            cost=cost,
            provider=self.name,
            metadata={"returncode": returncode},
        )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

from engine.execution.providers import register_provider  # noqa: E402

register_provider("aider", AiderProvider)
