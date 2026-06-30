"""Inflection Pi CLI subprocess execution provider.

Wraps the ``pi`` CLI (Inflection AI's conversational agent) as an
:class:`ExecutionProvider` via :class:`SubprocessProvider`.

Pi is Inflection AI's conversational model, known for empathetic and
nuanced responses.  When available as a CLI tool, non-interactive mode
pipes a prompt via stdin and captures stdout.

Install: Check Inflection AI's official distribution for CLI access.
Auth: ``INFLECTION_API_KEY`` env var or via Pi CLI auth flow.

Note: Pi's CLI interface may vary.  This provider assumes a
``pi --message "prompt"`` pattern.  Adjust ``_build_argv`` if the
actual CLI differs.
"""

from __future__ import annotations

import shutil

from engine.execution.provider import ExecutionResult, ExecutionTask
from engine.execution.providers.subprocess_base import SubprocessProvider
from engine.providers import ProviderError

DEFAULT_TIMEOUT = 300


class PiProvider(SubprocessProvider):
    """Execute deliberator agent tasks via the Inflection ``pi`` CLI.

    Args:
        timeout: Subprocess timeout in seconds.
        binary: Path to the ``pi`` binary.
    """

    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        binary: str | None = None,
        cwd: str | None = None,
    ) -> None:
        super().__init__(timeout=timeout, cwd=cwd)
        self._binary = binary or shutil.which("pi") or "pi"

    @property
    def name(self) -> str:
        return "pi"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        return [
            self._binary,
            "--message", task.prompt,
        ]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        env: dict[str, str] = {}
        api_key = task.metadata.get("api_key")
        if api_key:
            env["INFLECTION_API_KEY"] = api_key
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
                    f"pi exited {returncode}: {stderr[:500]}",
                    category="subprocess",
                ),
                provider=self.name,
                metadata={"returncode": returncode, "stderr": stderr[:500]},
            )
        # TODO(token-tracking): Inflection's ``pi`` CLI does not document
        # a structured-output mode (``--json``, ``-o json``, etc.) and
        # the public API surface for token telemetry is undocumented as
        # of writing.  Leaving ``cost=None`` until the CLI surfaces
        # usage (or until we move to the HTTP API which carries
        # ``usage`` per the OpenAI-compatible response shape).
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=stdout.strip(),
            error=None,
            provider=self.name,
            metadata={"returncode": returncode},
        )


from engine.execution.providers import register_provider  # noqa: E402

register_provider("pi", PiProvider)
