"""Live integration tests against a real local model.

These tests prove that token-usage capture works end-to-end against a
real provider — they are NOT mocked.  The default provider is
``OllamaProvider`` (since Ollama exposes an OpenAI-compatible endpoint
at ``http://localhost:11434/v1`` and is the easiest local LLM to run
on a developer laptop).

Running locally
---------------

1. Install Ollama: https://ollama.com/download
2. Pull a small fast model:  ``ollama pull qwen3:0.6b``
3. Make sure the server is up:  ``ollama serve`` (or just open the app)
4. Run the live tests::

       OLLAMA_BASE_URL=http://localhost:11434/v1 \\
           uv run pytest -m live engine/tests/test_providers_live.py -v

The whole module is skipped — at collection time — if nothing is
listening on the configured TCP port.  CI runs with ``-m "not live"``
by default, so this file never blocks the default test run.

Adding more live tests
----------------------

If you want to exercise another provider against Ollama (e.g.
``LlamaCppProvider`` pointed at the same endpoint) just add another
``@pytest.mark.live`` test below.  Providers that talk to *other*
endpoints (Anthropic API, OpenAI API, claude-code subprocess) belong
in their own ``live`` test classes — most already exist in
``test_concrete_providers.py``.

The contract every live test must enforce:

- Response content is non-empty (proves the call actually round-tripped)
- ``result.cost`` is populated
- ``result.cost.input_tokens > 0`` and ``result.cost.output_tokens > 0``

That's the whole point of the file: prove real-world token capture
is wired correctly.
"""

from __future__ import annotations

import asyncio
import os
import socket
from urllib.parse import urlparse

import pytest

from engine.execution import ExecutionTask
from engine.execution.providers.openai_compat import (
    OllamaProvider,
    OpenAICompatibleProvider,
)


# ---------------------------------------------------------------------------
# Skip-the-whole-module guard
# ---------------------------------------------------------------------------

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:0.6b")


def _tcp_reachable(url: str, timeout: float = 0.5) -> bool:
    """Return True if a TCP socket can connect to the URL's host:port."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "localhost"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ValueError):
        return False


# Module-level skip:  if Ollama isn't reachable we don't even try to
# collect the tests — saves both noise in default ``pytest -m live``
# runs and accidental hangs on dead sockets.  The skip reason is
# explicit so the user sees what they need to start.
if not _tcp_reachable(OLLAMA_BASE_URL):
    pytest.skip(
        f"Ollama not reachable at {OLLAMA_BASE_URL}.  "
        f"Start it with `ollama serve` (or set OLLAMA_BASE_URL to a "
        f"different OpenAI-compatible endpoint) to run these tests.",
        allow_module_level=True,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hello_task() -> ExecutionTask:
    """A minimal task that should round-trip through any LLM."""
    return ExecutionTask.from_prompt(
        prompt="Say hello in one short sentence.",
        output_path="/tmp/deliberator-live-hello.md",
        metadata={"agent_name": "live-hello", "phase": "review"},
    )


# ---------------------------------------------------------------------------
# Live tests
# ---------------------------------------------------------------------------


@pytest.mark.live
class TestOllamaCapturesTokensLive:
    """End-to-end: send a prompt to Ollama, assert tokens are non-zero.

    These tests are slow (a few seconds each on a laptop CPU) but
    cheap — they don't cost API credits.
    """

    def test_ollama_via_default_provider(self) -> None:
        """OllamaProvider with its built-in qwen3:0.6b default."""
        provider = OllamaProvider(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
        result = asyncio.run(provider.execute(_hello_task()))

        assert result.success, f"call failed: {result.error}"
        assert result.content, "non-empty content expected"
        assert result.cost is not None, "live token capture must populate Cost"
        assert result.cost.input_tokens > 0, (
            f"input_tokens must be positive (got {result.cost.input_tokens}); "
            f"this is the whole reason for the live suite — Cost.input_tokens=0 "
            f"means we silently lost telemetry somewhere between Ollama's response "
            f"and OpenAICompatibleProvider._record_usage."
        )
        assert result.cost.output_tokens > 0, (
            f"output_tokens must be positive (got {result.cost.output_tokens})"
        )
        # Local models don't have a USD cost.
        assert result.cost.usd is None
        assert result.provider == "ollama"

    def test_openai_compatible_against_ollama(self) -> None:
        """The base OpenAICompatibleProvider should also capture tokens.

        Same endpoint, just a different class — proves the capture
        logic lives in the base class (not in Ollama-specific code).
        """
        provider = OpenAICompatibleProvider(
            base_url=OLLAMA_BASE_URL,
            model=OLLAMA_MODEL,
            api_key="not-needed",
            provider_name="openai-compat-live",
        )
        result = asyncio.run(provider.execute(_hello_task()))

        assert result.success, f"call failed: {result.error}"
        assert result.content
        assert result.cost is not None
        assert result.cost.input_tokens > 0
        assert result.cost.output_tokens > 0
