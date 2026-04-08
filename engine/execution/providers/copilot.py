"""GitHub Copilot CLI subprocess execution provider.

Wraps ``gh copilot`` as an :class:`ExecutionProvider` via
:class:`SubprocessProvider`.

GitHub Copilot CLI is part of the ``gh`` CLI extension ecosystem.
It provides ``suggest`` (shell command generation) and ``explain``
(code explanation) subcommands.  For conversus deliberation, we use
it in explain mode with the prompt piped as the question.

Install: ``gh extension install github/gh-copilot``
Repo: https://github.com/features/copilot/cli
Requires: ``gh`` CLI authenticated with a Copilot-enabled account.
"""

from __future__ import annotations

import shutil

from engine.execution.provider import ExecutionResult, ExecutionTask
from engine.execution.providers.subprocess_base import SubprocessProvider
from engine.providers import ProviderError

DEFAULT_TIMEOUT = 120


class CopilotProvider(SubprocessProvider):
    """Execute conversus agent tasks via ``gh copilot``.

    Args:
        mode: Copilot subcommand (``"explain"`` or ``"suggest"``).
        timeout: Subprocess timeout in seconds.
        binary: Path to the ``gh`` binary.
    """

    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(
        self,
        *,
        mode: str = "explain",
        timeout: float = DEFAULT_TIMEOUT,
        binary: str | None = None,
        cwd: str | None = None,
    ) -> None:
        super().__init__(timeout=timeout, cwd=cwd)
        self._mode = mode
        self._binary = binary or shutil.which("gh") or "gh"

    @property
    def name(self) -> str:
        return "copilot"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        return [
            self._binary,
            "copilot",
            self._mode,
            task.prompt,
        ]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self, stdout: str, stderr: str, returncode: int, task: ExecutionTask,
    ) -> ExecutionResult:
        if returncode != 0:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"gh copilot exited {returncode}: {stderr[:500]}",
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

register_provider("copilot", CopilotProvider)
