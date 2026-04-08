"""Google Gemini CLI subprocess execution provider.

Wraps the ``gemini`` CLI (Google's coding agent) as an
:class:`ExecutionProvider` via :class:`SubprocessProvider`.

Gemini CLI is Google's answer to Claude Code — a terminal-based coding
agent with file read/write, shell execution, and multi-turn tool use.
Non-interactive mode: ``gemini -p "prompt"``.

Install: ``npm install -g @google/gemini-cli``
Repo: https://github.com/google-gemini/gemini-cli
Auth: ``GOOGLE_API_KEY`` env var or ``gemini auth login``
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

DEFAULT_MODEL = "gemini-2.5-pro"
DEFAULT_TIMEOUT = 600


class GeminiProvider(SubprocessProvider):
    """Execute conversus agent tasks via the Google ``gemini`` CLI.

    Args:
        model: Model name (e.g., ``"gemini-2.5-pro"``, ``"gemini-2.5-flash"``).
        timeout: Subprocess timeout in seconds.
        binary: Path to the ``gemini`` binary.
        sandbox: Sandbox mode for the CLI.
    """

    supports_tool_use: bool = True
    supports_pooling: bool = False

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        timeout: float = DEFAULT_TIMEOUT,
        binary: str | None = None,
        sandbox: str | None = None,
        cwd: str | None = None,
    ) -> None:
        super().__init__(timeout=timeout, cwd=cwd)
        self._model = model
        self._binary = binary or shutil.which("gemini") or "gemini"
        self._sandbox = sandbox

    @property
    def name(self) -> str:
        return "gemini"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        model = task.metadata.get("model", self._model)
        argv = [
            self._binary,
            "-p", task.prompt,
            "-m", model,
        ]
        if self._sandbox:
            argv.extend(["--sandbox", self._sandbox])
        # Add read paths as context
        for path in task.read_paths:
            argv.extend(["--add-dir", path])
        return argv

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        env: dict[str, str] = {}
        api_key = task.metadata.get("api_key")
        if api_key:
            env["GOOGLE_API_KEY"] = api_key
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
                    f"gemini exited {returncode}: {stderr[:500]}",
                    category="subprocess",
                ),
                provider=self.name,
                metadata={"returncode": returncode, "stderr": stderr[:500]},
            )
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=stdout.strip(),
            error=None,
            provider=self.name,
            metadata={"returncode": returncode},
        )


from engine.execution.providers import register_provider  # noqa: E402

register_provider("gemini", GeminiProvider)
