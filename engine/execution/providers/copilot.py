"""GitHub Copilot CLI subprocess execution provider.

Wraps ``gh copilot`` as an :class:`ExecutionProvider` via
:class:`SubprocessProvider`.

GitHub Copilot CLI is part of the ``gh`` CLI extension ecosystem.
It provides ``suggest`` (shell command generation) and ``explain``
(code explanation) subcommands.  For deliberator deliberation, we use
it in explain mode with the prompt piped as the question.

Install: ``gh extension install github/gh-copilot``
Repo: https://github.com/features/copilot/cli
Requires: ``gh`` CLI authenticated with a Copilot-enabled account.

Token capture status (probed 2026-04-18): NOT WIRED.  The Copilot CLI
exposes token usage only via the interactive ``/context`` slash
command — there is no documented ``--json`` / ``--verbose`` /
``--debug`` flag on the non-interactive surface.  BYOK mode
(`COPILOT_PROVIDER_BASE_URL` etc.) routes to an OpenAI-compatible
endpoint whose HTTP traffic includes ``usage``, but the Copilot CLI
does not surface it on stdout.  See ``_parse_output()`` for the full
finding and the doc URLs we tracked.  ``cost`` returns ``None``
("unknown != zero") until upstream adds a structured-output flag.
"""

from __future__ import annotations

import shutil

from engine.execution.provider import ExecutionResult, ExecutionTask
from engine.execution.providers.subprocess_base import SubprocessProvider
from engine.providers import ProviderError

DEFAULT_TIMEOUT = 120


class CopilotProvider(SubprocessProvider):
    """Execute deliberator agent tasks via ``gh copilot``.

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
        # TODO(token-tracking, 2026-04-18): re-probed against current
        # GitHub Copilot CLI surface — token capture remains gated.
        #
        # Findings (https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli):
        #   • Programmatic mode is `copilot -p "<prompt>"` (the new CLI)
        #     or the legacy `gh copilot {explain,suggest}` extension this
        #     provider currently invokes.  Neither documents a `--json`,
        #     `--output-format`, `--verbose`, or `--debug` flag.
        #   • Token usage IS surfaced — but only via the interactive
        #     `/context` slash command ("shows a detailed token usage
        #     breakdown" per the docs), which is unreachable from the
        #     non-interactive `-p` path we use here.
        #   • BYOK mode (https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models)
        #     adds `COPILOT_PROVIDER_BASE_URL` / `COPILOT_PROVIDER_TYPE` /
        #     `COPILOT_PROVIDER_API_KEY` / `COPILOT_MODEL` env vars to
        #     route to an OpenAI-compatible endpoint.  The underlying
        #     HTTP traffic carries `usage` per the OpenAI schema, but the
        #     Copilot CLI does not pass it through to stdout in any
        #     documented output mode.
        #
        # Revisit when GitHub adds either a `--json` programmatic-output
        # flag or a `/context`-equivalent CLI flag.  Keep returning
        # ``cost=None`` for now — ``unknown != zero`` per binding
        # condition #5.
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
