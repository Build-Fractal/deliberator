"""OpenAI Codex CLI subprocess execution provider.

Wraps the ``codex`` CLI (OpenAI's coding agent) as an
:class:`ExecutionProvider` via :class:`SubprocessProvider`.

Codex is OpenAI's answer to Claude Code — a terminal-based coding agent
with file read/write, shell execution, and multi-turn conversation.
Non-interactive mode: ``codex --quiet --full-auto "prompt"``.

Install: ``npm install -g @openai/codex``
"""

from __future__ import annotations

import json
import shutil

from engine.execution.provider import ExecutionResult, ExecutionTask
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
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=stdout.strip(),
            error=None,
            provider=self.name,
            metadata={"returncode": returncode},
        )


from engine.execution.providers import register_provider  # noqa: E402

register_provider("codex", CodexProvider)
