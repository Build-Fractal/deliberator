"""Anthropic execution provider wrapping the official ``anthropic`` SDK.

This is the spec 042 Phase 2.3 :class:`ExecutionProvider` for direct
Anthropic API calls.  It wraps the existing
:mod:`engine.providers.anthropic` ``AnthropicProvider`` (which is a
:class:`ModelProvider`), but adds the execution-level features that
``ModelProvider`` cannot express:

- **Structured cost telemetry** (binding condition #5): the SDK's
  ``response.usage`` contains ``input_tokens`` and ``output_tokens``
  that the ``ModelProvider.complete()`` method discards (it only returns
  the text).  This provider accesses the raw SDK response to extract
  them into :attr:`~engine.execution.ExecutionResult.cost`.
- **Reference inlining**: because ``supports_tool_use=False``, any
  :class:`Reference` paths on the :class:`ExecutionTask` are read from
  disk and prepended to the prompt.  The model sees the file contents
  but cannot modify them — it only produces a text response.
- **Registry integration**: auto-registers under ``"anthropic"`` via
  :func:`~engine.execution.providers.register_provider`.

Why this wraps the SDK directly instead of wrapping
``AnthropicProvider``:

The ``ModelProvider`` contract returns ``str`` from ``complete()``.
To extract ``usage`` we need the raw ``Message`` response object.
Wrapping ``AnthropicProvider`` would throw away the usage data before
we could capture it.  So we duplicate the SDK call pattern (a thin
facade over ``client.messages.create``) and re-use the same error
mapping.  The duplication is ~20 lines of try/except and is worth the
cost telemetry payoff.

The existing ``AnthropicProvider`` remains in ``engine/providers/`` for
backward compatibility with the ``ModelProviderExecutionAdapter`` path
used by the streaming fallback in ``dispatch_agent()``.  When v2
streaming lands on ``ExecutionProvider``, the old ``ModelProvider`` can
be retired.
"""

from __future__ import annotations

import time
from datetime import timedelta
from pathlib import Path
from typing import Any

import anthropic

from engine.execution.provider import (
    Cost,
    ExecutionResult,
    ExecutionTask,
)
from engine.providers import ProviderError

# Re-use the version string and OAuth detection from the model provider.
from engine.providers.anthropic import CLAUDE_CODE_VERSION, is_oauth_token


# ---------------------------------------------------------------------------
# Reference inlining
# ---------------------------------------------------------------------------


def _inline_references(task: ExecutionTask) -> str:
    """Build a prompt with reference file contents prepended.

    For each :class:`Reference` on the task, read the file and insert its
    content as a fenced block before the main prompt.  Missing files are
    noted inline rather than raising — agent deliberations should not
    crash because a reference path is stale.

    Returns the full prompt string (references + original prompt).
    """
    if not task.references:
        return task.prompt

    blocks: list[str] = []
    for ref in task.references:
        path = Path(ref.uri)
        try:
            content = path.read_text(encoding="utf-8")
            label = ref.description or path.name
            blocks.append(
                f"<reference path=\"{ref.uri}\" label=\"{label}\">\n"
                f"{content}\n"
                f"</reference>"
            )
        except OSError:
            blocks.append(
                f"<reference path=\"{ref.uri}\" error=\"file not found or unreadable\" />"
            )

    return "\n\n".join(blocks) + "\n\n" + task.prompt


# ---------------------------------------------------------------------------
# AnthropicExecutionProvider
# ---------------------------------------------------------------------------


class AnthropicExecutionProvider:
    """Direct Anthropic API execution provider with cost telemetry.

    Uses :class:`anthropic.AsyncAnthropic` to send a single-shot
    Messages API request and returns an :class:`ExecutionResult` with
    structured cost data extracted from ``response.usage``.

    Args:
        auth_token: Optional OAuth token for subscription-based auth.
            See :class:`engine.providers.anthropic.AnthropicProvider`
            for details on the ``sk-ant-oat`` prefix handling.
        model: Default model identifier.  Can be overridden per-task
            via ``task.metadata["model"]``.
        max_tokens: Default max tokens.  Can be overridden per-task
            via ``task.metadata["max_tokens"]``.
    """

    name: str = "anthropic"
    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(
        self,
        auth_token: str | None = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 16384,
    ) -> None:
        self._model = model
        self._max_tokens = max_tokens

        if auth_token is not None and is_oauth_token(auth_token):
            self._client = anthropic.AsyncAnthropic(
                auth_token=auth_token,
                default_headers={
                    "user-agent": f"claude-cli/{CLAUDE_CODE_VERSION}",
                    "x-app": "cli",
                    "anthropic-beta": "claude-code-20250219,oauth-2025-04-20",
                },
            )
        elif auth_token is not None:
            self._client = anthropic.AsyncAnthropic(auth_token=auth_token)
        else:
            self._client = anthropic.AsyncAnthropic()

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        """Execute a task via the Anthropic Messages API.

        Inlines reference file contents into the prompt (since
        ``supports_tool_use=False``), sends the request, and extracts
        cost telemetry from ``response.usage``.
        """
        model = task.metadata.get("model", self._model)
        max_tokens = task.metadata.get("max_tokens", self._max_tokens)
        prompt = _inline_references(task)

        start = time.monotonic()
        try:
            response = await self._client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.AuthenticationError as exc:
            return self._error_result(
                task, start, "auth",
                f"Anthropic authentication failed: {exc}", exc,
                model=model, max_tokens=max_tokens,
            )
        except anthropic.RateLimitError as exc:
            return self._error_result(
                task, start, "rate_limit",
                f"Anthropic rate limit exceeded: {exc}", exc,
                model=model, max_tokens=max_tokens,
            )
        except anthropic.APIStatusError as exc:
            return self._error_result(
                task, start, "server",
                f"Anthropic API error (status {exc.status_code}): {exc}", exc,
                model=model, max_tokens=max_tokens,
            )
        except anthropic.APIError as exc:
            return self._error_result(
                task, start, "unknown",
                f"Anthropic API error: {exc}", exc,
                model=model, max_tokens=max_tokens,
            )
        except Exception as exc:
            return self._error_result(
                task, start, "unknown",
                f"{type(exc).__name__}: {exc}", exc,
                model=model, max_tokens=max_tokens,
            )

        # Extract text content
        content = response.content[0].text if response.content else ""

        # Extract cost telemetry from the SDK response (binding condition #5).
        # The Anthropic SDK populates response.usage with input_tokens and
        # output_tokens.  We report the raw token counts; the dollar amount
        # is left as None because the SDK does not provide it — downstream
        # pricing tables in spec 033/040 compute the dollar cost from
        # model + token counts.
        cost = Cost(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            usd=None,
        )

        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=content,
            error=None,
            cost=cost,
            duration=timedelta(seconds=time.monotonic() - start),
            provider=self.name,
            metadata={
                "model": model,
                "max_tokens": max_tokens,
                "stop_reason": response.stop_reason,
                "message_id": response.id,
            },
        )

    async def execute_batch(
        self,
        tasks: list[ExecutionTask] | tuple[ExecutionTask, ...],
    ) -> list[ExecutionResult]:
        """Execute multiple tasks concurrently via ``asyncio.gather``."""
        import asyncio

        return list(await asyncio.gather(*(self.execute(t) for t in tasks)))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _error_result(
        self,
        task: ExecutionTask,
        start: float,
        category: str,
        message: str,
        original: BaseException,
        *,
        model: str,
        max_tokens: int,
    ) -> ExecutionResult:
        """Build a failure ExecutionResult with consistent shape."""
        return ExecutionResult(
            success=False,
            output_path=task.output_path,
            content=None,
            error=ProviderError(message, category=category, original=original),
            cost=None,
            duration=timedelta(seconds=time.monotonic() - start),
            provider=self.name,
            metadata={"model": model, "max_tokens": max_tokens},
        )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

from engine.execution.providers import register_provider  # noqa: E402

register_provider("anthropic", AnthropicExecutionProvider)
