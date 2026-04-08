"""Base class for subprocess-based execution providers (spec 042 Phase 2.4).

All execution providers that run an external CLI tool as a subprocess share
the same lifecycle concerns:

- **Process spawning**: ``asyncio.create_subprocess_exec`` with stdout/stderr
  capture.
- **Timeout enforcement**: kill the subprocess after a configurable deadline.
- **Signal propagation**: forward SIGTERM to the child so it can clean up.
- **Environment-only secrets**: API keys and tokens are passed via env vars,
  never via argv (which is visible in ``ps`` output and process listings).
- **Cold-start amortization hooks**: subprocesses like ``claude-code`` have
  a measurable cold start (1-3s).  The base class provides ``warm()`` and
  ``is_warm()`` hooks that subclasses can override to pre-spawn or keep
  alive a long-running process.
- **Output parsing**: subclasses implement ``_parse_output()`` to extract
  structured content from stdout/stderr.

Subclasses override:
- ``_build_argv(task)`` — construct the command-line arguments
- ``_build_env(task)`` — merge secrets into the subprocess environment
- ``_parse_output(stdout, stderr, returncode, task)`` — extract content
  from the subprocess output into an ``ExecutionResult``

The base class handles everything else: spawning, timeout, SIGTERM,
structured error reporting, duration measurement.

Phase 3 will land ``ClaudeCodeProvider`` and ``OpenCodeProvider`` on top
of this base.  This module is provider-agnostic.
"""

from __future__ import annotations

import asyncio
import os
import signal
import time
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from engine.execution.provider import (
    Cost,
    Duration,
    ExecutionResult,
    ExecutionTask,
)
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Default configuration
# ---------------------------------------------------------------------------

#: Default subprocess timeout in seconds.  Subclasses may override per-task
#: via ``task.metadata["timeout"]`` or per-provider via constructor arg.
DEFAULT_TIMEOUT_SECONDS = 300

#: Seconds to wait after SIGTERM before sending SIGKILL.
SIGTERM_GRACE_SECONDS = 5


# ---------------------------------------------------------------------------
# SubprocessProvider ABC
# ---------------------------------------------------------------------------


class SubprocessProvider(ABC):
    """Abstract base class for subprocess-based execution providers.

    Subclasses must implement:
    - :meth:`_build_argv` — command + arguments to execute
    - :meth:`_build_env` — environment dict (secrets go here, not argv)
    - :meth:`_parse_output` — extract result content from process output

    Optional overrides:
    - :attr:`name` — provider registry name (must be overridden)
    - :attr:`supports_tool_use` — True for agent runtimes like claude-code
    - :attr:`supports_pooling` — True if warm() is implemented
    - :meth:`warm` / :meth:`is_warm` — cold-start amortization
    """

    supports_tool_use: bool = False
    supports_pooling: bool = False

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        cwd: str | None = None,
    ) -> None:
        """
        Args:
            timeout: Default subprocess timeout in seconds.  Per-task
                override via ``task.metadata["timeout"]``.
            cwd: Working directory for the subprocess.  If ``None``,
                inherits the engine's cwd.
        """
        self._default_timeout = timeout
        self._cwd = cwd

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider registry name (e.g., ``"claude-code"``)."""
        ...

    # ------------------------------------------------------------------
    # Subclass hooks — MUST override
    # ------------------------------------------------------------------

    @abstractmethod
    def _build_argv(self, task: ExecutionTask) -> list[str]:
        """Return the command + arguments to execute.

        The returned list is passed directly to
        ``asyncio.create_subprocess_exec(*argv)``.  Secrets MUST NOT
        appear in argv — use :meth:`_build_env` instead.

        Args:
            task: The execution task.  Subclasses read ``task.prompt``,
                ``task.read_paths``, ``task.output_path``, and
                ``task.metadata`` to construct the command.
        """
        ...

    def _build_stdin(self, task: ExecutionTask) -> bytes | None:
        """Return bytes to pipe to the subprocess's stdin.

        Default returns ``None`` (no stdin).  Subclasses that need to
        pass large content (e.g., prompts with ``---`` markers that
        would confuse CLI parsers) should override this and pipe
        the content via stdin instead of argv.
        """
        return None

    @abstractmethod
    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        """Return the environment dict for the subprocess.

        This is where API keys and tokens go.  The base class merges
        the returned dict with ``os.environ`` (returned values override).

        Args:
            task: The execution task.
        """
        ...

    @abstractmethod
    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        """Parse subprocess output into an ExecutionResult.

        Called after the subprocess exits (including on non-zero return
        codes).  Subclasses decide what constitutes success vs. failure
        based on the specific CLI tool's output conventions.

        Args:
            stdout: Captured stdout as a string.
            stderr: Captured stderr as a string.
            returncode: Process exit code.
            task: The original task (for output_path, metadata).

        Returns:
            A fully populated :class:`ExecutionResult`.
        """
        ...

    # ------------------------------------------------------------------
    # Optional hooks — MAY override
    # ------------------------------------------------------------------

    async def warm(self) -> None:
        """Pre-warm the provider to reduce cold-start latency.

        Default is a no-op.  Subclasses that can pre-spawn a process,
        pre-load a model, or establish a persistent connection should
        override this.  The engine calls ``warm()`` before large phases.
        """

    def is_warm(self) -> bool:
        """Return True if the provider is pre-warmed.

        Default returns False.  Subclasses that implement ``warm()``
        should track state and return True when warm.
        """
        return False

    # ------------------------------------------------------------------
    # ExecutionProvider protocol
    # ------------------------------------------------------------------

    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        """Spawn a subprocess, capture output, enforce timeout.

        The full lifecycle:
        1. Build argv and env via subclass hooks
        2. Spawn via ``asyncio.create_subprocess_exec``
        3. Wait with timeout
        4. On timeout: SIGTERM → grace period → SIGKILL
        5. Parse output via subclass hook
        6. Return structured ExecutionResult with duration
        """
        timeout = task.metadata.get("timeout", self._default_timeout)
        argv = self._build_argv(task)
        env = {**os.environ, **self._build_env(task)}
        stdin_data = self._build_stdin(task)

        start = time.monotonic()

        try:
            proc = await asyncio.create_subprocess_exec(
                *argv,
                stdin=asyncio.subprocess.PIPE if stdin_data is not None else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=self._cwd,
            )
        except FileNotFoundError as exc:
            # Binary not found — e.g., claude-code not installed
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"Subprocess binary not found: {argv[0]}",
                    category="subprocess",
                    original=exc,
                ),
                cost=None,
                duration=timedelta(seconds=time.monotonic() - start),
                provider=self.name,
                metadata={"argv_0": argv[0]},
            )
        except OSError as exc:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"Failed to spawn subprocess: {exc}",
                    category="subprocess",
                    original=exc,
                ),
                cost=None,
                duration=timedelta(seconds=time.monotonic() - start),
                provider=self.name,
                metadata={"argv_0": argv[0]},
            )

        # Wait with timeout, capture output
        timed_out = False
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(input=stdin_data),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            timed_out = True
            stdout_bytes, stderr_bytes = await self._kill_gracefully(proc)

        stdout = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
        stderr = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
        elapsed = timedelta(seconds=time.monotonic() - start)
        returncode = proc.returncode if proc.returncode is not None else -1

        if timed_out:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"Subprocess timed out after {timeout}s",
                    category="timeout",
                ),
                cost=None,
                duration=elapsed,
                provider=self.name,
                metadata={
                    "returncode": returncode,
                    "stderr_tail": stderr[-500:] if stderr else "",
                    "timed_out": True,
                },
            )

        # Delegate output parsing to subclass
        result = self._parse_output(stdout, stderr, returncode, task)
        # Ensure duration is always set by the base class
        if result.duration is None:
            result.duration = elapsed
        return result

    async def execute_batch(
        self,
        tasks: list[ExecutionTask] | tuple[ExecutionTask, ...],
    ) -> list[ExecutionResult]:
        """Execute multiple tasks concurrently via ``asyncio.gather``."""
        return list(await asyncio.gather(*(self.execute(t) for t in tasks)))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    async def _kill_gracefully(
        proc: asyncio.subprocess.Process,
    ) -> tuple[bytes, bytes]:
        """Send SIGTERM, wait for grace period, then SIGKILL if needed.

        Returns captured (stdout, stderr) bytes.
        """
        # Try SIGTERM first
        try:
            proc.send_signal(signal.SIGTERM)
        except ProcessLookupError:
            # Already exited
            pass

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=SIGTERM_GRACE_SECONDS,
            )
            return stdout or b"", stderr or b""
        except asyncio.TimeoutError:
            # SIGTERM didn't work — force kill
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            # Drain remaining output
            stdout, stderr = await proc.communicate()
            return stdout or b"", stderr or b""
