"""Custom deepeval judges for the deliberator eval suite.

``ClaudeCodeJudge`` shells out to ``claude -p`` via the existing
:class:`engine.execution.providers.claude_code.ClaudeCodeProvider`, so
OAuth-only users (Claude Max subscription, no ``ANTHROPIC_API_KEY``) can
run the deepeval quality tests using their host Claude session for both
deliberation AND judging.

Per issue #87 / spec 061 step 7 follow-on: PR #85 introduced an
Anthropic-API-backed judge via deepeval's ``AnthropicModel`` and PR #86
flipped the deliberation default to ``claude-code``. Together those
left a gap: OAuth-only users could run the deliberation but the judge
still required ``ANTHROPIC_API_KEY``, causing the 5 quality tests to
skip cleanly but produce no signal. This module closes that gap by
exposing a ``DeepEvalBaseLLM`` subclass that drives the judge through
the same subprocess transport the deliberation uses.
"""

from __future__ import annotations

import asyncio
import tempfile
from typing import Any

from deepeval.models.base_model import DeepEvalBaseLLM


class ClaudeCodeJudge(DeepEvalBaseLLM):
    """Deepeval judge that delegates generation to ``claude -p``.

    Uses the host Claude session (OAuth, Claude Max) via
    :class:`engine.execution.providers.claude_code.ClaudeCodeProvider`
    so the deepeval suite can run without an Anthropic API key.

    Args:
        model: Claude model alias or full ID. Defaults to ``"sonnet"``,
            which the ``claude`` CLI resolves against the calling
            session — the safest choice for OAuth users whose
            entitlement is bound to a model alias rather than a
            specific dated model literal.
    """

    def __init__(self, model: str = "sonnet") -> None:
        self._model_name = model
        # Lazy provider construction so that importing this module on a
        # host without the ``claude`` binary does not fail (relevant for
        # CI workers that collect tests but never instantiate the judge).
        self._provider: Any | None = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_provider(self) -> Any:
        """Lazily construct and cache the underlying ClaudeCodeProvider."""
        from engine.execution.providers.claude_code import ClaudeCodeProvider

        if self._provider is None:
            self._provider = ClaudeCodeProvider(model=self._model_name)
        return self._provider

    # ------------------------------------------------------------------
    # DeepEvalBaseLLM contract
    # ------------------------------------------------------------------

    def load_model(self) -> Any:
        """Return the underlying provider (deepeval contract).

        deepeval calls ``load_model`` once per metric construction. We
        return the cached :class:`ClaudeCodeProvider` so subsequent
        ``generate``/``a_generate`` calls share the same configuration.
        """
        return self._get_provider()

    def generate(self, prompt: str) -> str:
        """Synchronous generation — runs the async path under ``asyncio.run``."""
        return asyncio.run(self.a_generate(prompt))

    async def a_generate(self, prompt: str) -> str:
        """Asynchronous generation via the ``claude -p`` subprocess.

        Constructs a minimal :class:`ExecutionTask` from the judge prompt
        and dispatches it through the provider. The output_path is a
        throwaway temp file because deepeval cares only about the text
        content returned by ``generate`` — but the provider contract
        requires a non-empty path.

        Raises:
            RuntimeError: If the subprocess fails. deepeval surfaces this
                to the test layer as a metric error rather than a
                misleading low score.
        """
        from engine.execution.provider import ExecutionTask

        provider = self._get_provider()
        # ``delete=False`` because the file may outlive the ``with`` block
        # if the subprocess writes to it; deepeval reads only the
        # in-memory ``content`` field, so the temp file is harmless.
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            output_path = f.name
        task = ExecutionTask.from_prompt(
            prompt=prompt,
            output_path=output_path,
            metadata={"agent_name": "deepeval-judge", "phase": "judge"},
        )
        result = await provider.execute(task)
        if not result.success:
            raise RuntimeError(
                f"ClaudeCodeJudge subprocess failed: {result.error}"
            )
        return result.content or ""

    def get_model_name(self) -> str:
        """Return a human-readable model identifier with provider suffix.

        The ``(claude-code)`` suffix lets test output and deepeval
        telemetry distinguish this judge from the API-backed
        ``AnthropicModel`` even when both share the same model alias.
        """
        return f"{self._model_name} (claude-code)"
