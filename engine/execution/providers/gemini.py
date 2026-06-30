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
    """Execute deliberator agent tasks via the Google ``gemini`` CLI.

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
        # Issue #54 contract: None means "no override, use provider default".
        model = task.metadata.get("model") or self._model
        # Request JSON output so we can parse structured token usage.
        # Gemini CLI ≥ 0.4 documents ``-o json`` (alias of
        # ``--output-format json``) — the envelope carries ``response``
        # plus ``stats.models[*].tokens.{prompt,candidates,cached,total}``.
        argv = [
            self._binary,
            "-p", task.prompt,
            "-m", model,
            "-o", "json",
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

        # Try to parse JSON envelope from ``-o json``.  Older versions of
        # the CLI may still print plain text — fall back gracefully.
        content: str | None = None
        cost = None
        metadata: dict[str, Any] = {"returncode": returncode}
        try:
            envelope = json.loads(stdout)
        except (json.JSONDecodeError, ValueError):
            content = stdout.strip()
            metadata["raw_output"] = True
        else:
            if isinstance(envelope, dict):
                # The "response" field is the agent's text reply.
                response_value = envelope.get("response")
                if isinstance(response_value, str):
                    content = response_value.strip()
                else:
                    # Some versions emit a structured object — fall back
                    # to the full envelope's string repr for the content
                    # so we don't drop the agent's reply silently.
                    content = stdout.strip()

                # Extract token totals from ``stats.models[*].tokens``.
                # Schema (per ``gemini --help`` and the gemini-cli repo):
                #   stats: {
                #     models: {
                #       "<model>": {
                #         tokens: { prompt, candidates, cached, total, ... }
                #       }
                #     }
                #   }
                stats = envelope.get("stats")
                if isinstance(stats, dict):
                    models = stats.get("models")
                    if isinstance(models, dict):
                        input_tokens = 0
                        output_tokens = 0
                        for _name, mstats in models.items():
                            if not isinstance(mstats, dict):
                                continue
                            tokens = mstats.get("tokens", {}) or {}
                            input_tokens += int(tokens.get("prompt", 0) or 0)
                            input_tokens += int(tokens.get("cached", 0) or 0)
                            output_tokens += int(tokens.get("candidates", 0) or 0)
                        if input_tokens or output_tokens:
                            cost = Cost(
                                input_tokens=input_tokens,
                                output_tokens=output_tokens,
                                usd=None,
                            )
            else:
                content = stdout.strip()
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


from engine.execution.providers import register_provider  # noqa: E402

register_provider("gemini", GeminiProvider)
