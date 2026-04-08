"""OpenCode subprocess execution provider.

Wraps the ``opencode`` CLI as an :class:`ExecutionProvider` via
:class:`SubprocessProvider`.  Uses ``opencode run "message"`` for
non-interactive single-shot execution.

Repo: https://opencode.ai/

OpenCode is a Go-based coding agent that supports Anthropic, OpenAI,
and other providers.  It has a TUI, a web UI, and a headless ``run``
mode suitable for subprocess dispatch.  OpenCode also supports the
Agent Client Protocol (ACP) via ``opencode acp`` for server-mode
operation — but this provider uses the simpler ``run`` subprocess
path for v1.

Key flags:
- ``opencode run "message"`` — non-interactive execution
- OpenCode reads configuration from ``.opencode/config.toml``
"""

from __future__ import annotations

import shutil
from datetime import timedelta
from typing import Any

from engine.execution.provider import (
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
    """Execute conversus agent tasks via the ``opencode`` CLI.

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
        argv = [
            self._binary,
            "run",
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
        """Parse opencode output — plain text from run mode."""
        content = stdout.strip() if stdout else None

        if returncode != 0:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=content,
                error=ProviderError(
                    f"opencode exited {returncode}: {stderr[:500]}",
                    category="subprocess",
                ),
                provider=self.name,
                metadata={"returncode": returncode, "stderr": stderr[:500]},
            )

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=content,
            error=None,
            cost=None,
            provider=self.name,
            metadata={"returncode": returncode},
        )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

from engine.execution.providers import register_provider  # noqa: E402

register_provider("opencode", OpenCodeProvider)
