"""MCP Sampling provider — routes agent calls through the host's LLM (spec 060).

Instead of calling the Anthropic API directly, this provider sends each
agent's prompt via MCP ``sampling/createMessage`` to the MCP client
(Claude Desktop). The client forwards the request through its own Claude
session and returns the response. Zero configuration — uses the host's
subscription, no API key needed.

This is the zero-config path for Desktop Extension users:

    Install .mcpb → run a deliberation → done

No console.anthropic.com, no API keys, no extension settings.

Usage::

    from engine.execution.providers.desktop_sampling import DesktopSamplingProvider

    # The MCP context is passed from the @mcp.tool() handler
    provider = DesktopSamplingProvider(mcp_context=ctx)
    result = await provider.execute(task)

See ``specs/060-mcp-sampling-provider.md`` for the full design.
"""

import asyncio
import logging
import time
from datetime import timedelta

from engine.execution.provider import (
    Cost,
    Duration,
    ExecutionProvider,
    ExecutionResult,
    ExecutionTask,
)

logger = logging.getLogger("conversus.providers.desktop_sampling")


class DesktopSamplingProvider:
    """Execution provider that routes agent calls through MCP sampling.

    Each ``execute()`` call sends a ``sampling/createMessage`` request to
    the MCP client (Claude Desktop), which forwards it through its own
    Claude session. The response text becomes the agent's output.

    The provider requires an ``mcp_context`` — the FastMCP ``Context``
    object available inside ``@mcp.tool()`` handlers. This context
    provides the ``sample()`` method for sending sampling requests.

    Attributes:
        name: ``"claude-desktop"``
        supports_tool_use: ``False`` — sampling returns text, not tool calls
        supports_pooling: ``False`` — each request is independent
    """

    name: str = "claude-desktop"
    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(self, mcp_context: object | None = None) -> None:
        """Create a DesktopSamplingProvider.

        Args:
            mcp_context: The FastMCP ``Context`` object from the active
                ``@mcp.tool()`` handler. Must have a ``session`` attribute
                with a ``send_request`` method for ``sampling/createMessage``.
                If ``None``, ``execute()`` will raise ``RuntimeError``.
        """
        self._ctx = mcp_context

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        """Execute a task via MCP sampling/createMessage.

        Sends the task's prompt text to the MCP client as a sampling
        request. The client routes it through its own LLM session and
        returns the generated text.

        Args:
            task: The structured task to execute.

        Returns:
            An ``ExecutionResult`` with the sampled text as ``content``.
            Cost is reported as zero (the host absorbs the actual cost).
        """
        if self._ctx is None:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content="",
                error="DesktopSamplingProvider requires an MCP context "
                      "(only available when running inside an MCP tool handler)",
                cost=None,
                provider=self.name,
            )

        # Extract the prompt text from the task's parts
        prompt = "\n\n".join(part.content for part in task.parts)
        if not prompt:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content="",
                error="Empty prompt — task has no content parts",
                cost=None,
                provider=self.name,
            )

        start = time.monotonic()

        try:
            # Use the MCP context to send a sampling request.
            # FastMCP's Context.sample() sends sampling/createMessage
            # to the client and returns the response.
            from mcp.types import (
                CreateMessageRequest,
                CreateMessageResult,
                SamplingMessage,
                TextContent,
            )

            # Build the sampling request
            messages = [
                SamplingMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt),
                )
            ]

            max_tokens = task.metadata.get("max_tokens", 4096) if task.metadata else 4096

            # Send via the context's session
            result = await self._ctx.session.send_request(
                CreateMessageRequest(
                    method="sampling/createMessage",
                    params={
                        "messages": [m.model_dump() for m in messages],
                        "maxTokens": max_tokens,
                    },
                ),
                CreateMessageResult,
            )

            elapsed = timedelta(seconds=time.monotonic() - start)
            response_text = ""
            if hasattr(result, "content") and hasattr(result.content, "text"):
                response_text = result.content.text
            elif isinstance(result.content, str):
                response_text = result.content

            logger.info(
                "sampling/createMessage completed (%s, %d chars)",
                elapsed,
                len(response_text),
            )

            return ExecutionResult(
                success=True,
                output_path=task.output_path,
                content=response_text,
                error=None,
                cost=Cost(input_tokens=0, output_tokens=0),
                duration=elapsed,
                provider=self.name,
            )

        except Exception as exc:
            elapsed = timedelta(seconds=time.monotonic() - start)
            logger.exception("sampling/createMessage failed")
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content="",
                error=f"MCP sampling failed: {exc}",
                cost=None,
                duration=elapsed,
                provider=self.name,
            )

    async def execute_batch(
        self,
        tasks: list[ExecutionTask] | tuple[ExecutionTask, ...],
    ) -> list[ExecutionResult]:
        """Execute tasks sequentially via sampling.

        MCP sampling is sequential by spec ("only in association with an
        originating client request"). Each task is sent one at a time.
        """
        results = []
        for task in tasks:
            result = await self.execute(task)
            results.append(result)
        return results


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

from engine.execution.providers import register_provider  # noqa: E402

register_provider("claude-desktop", DesktopSamplingProvider)
