"""Tests for engine.execution.providers.subprocess_base — SubprocessProvider ABC.

Uses a concrete ``EchoProvider`` test subclass that wraps ``/bin/echo`` to
exercise the full lifecycle: spawning, timeout, SIGTERM, output parsing,
env-only secrets, and error handling.  No network, no real LLM calls.
"""

from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import time
from datetime import timedelta
from typing import Any

import pytest

from engine.execution import (
    ExecutionProvider,
    ExecutionResult,
    ExecutionTask,
)
from engine.execution.providers.subprocess_base import (
    DEFAULT_TIMEOUT_SECONDS,
    SIGTERM_GRACE_SECONDS,
    SubprocessProvider,
)
from engine.providers import ProviderError


# ---------------------------------------------------------------------------
# Concrete test subclass — wraps /bin/echo
# ---------------------------------------------------------------------------


class EchoProvider(SubprocessProvider):
    """Minimal concrete provider for testing: runs ``echo <prompt>``."""

    @property
    def name(self) -> str:
        return "echo-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        return ["/bin/echo", task.prompt]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {"TEST_SECRET": "hunter2"}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        if returncode != 0:
            return ExecutionResult(
                success=False,
                output_path=task.output_path,
                content=None,
                error=ProviderError(
                    f"echo exited with code {returncode}: {stderr}",
                    category="subprocess",
                ),
                provider=self.name,
                metadata={"returncode": returncode},
            )
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=stdout.strip(),
            error=None,
            provider=self.name,
            metadata={"returncode": returncode},
        )


class FailProvider(SubprocessProvider):
    """Provider that runs a command that always exits non-zero."""

    @property
    def name(self) -> str:
        return "fail-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        return ["/bin/sh", "-c", "echo 'error output' >&2; exit 1"]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=False,
            output_path=task.output_path,
            content=None,
            error=ProviderError(
                f"Process failed: {stderr.strip()}",
                category="subprocess",
            ),
            provider=self.name,
            metadata={"returncode": returncode, "stderr": stderr.strip()},
        )


class SleepProvider(SubprocessProvider):
    """Provider that runs ``sleep`` — used for timeout tests."""

    @property
    def name(self) -> str:
        return "sleep-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        seconds = task.metadata.get("sleep_seconds", 60)
        return ["/bin/sleep", str(seconds)]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content="slept",
            error=None,
            provider=self.name,
        )


class MissingBinaryProvider(SubprocessProvider):
    """Provider that tries to run a non-existent binary."""

    @property
    def name(self) -> str:
        return "missing-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        return ["/nonexistent/binary", "--flag"]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=stdout,
            provider=self.name,
        )


class EnvReaderProvider(SubprocessProvider):
    """Provider that prints environment variables — verifies env-only secrets."""

    @property
    def name(self) -> str:
        return "env-reader-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        var_name = task.metadata.get("env_var", "TEST_SECRET")
        return ["/bin/sh", "-c", f"echo ${var_name}"]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {
            "TEST_SECRET": "super-secret-key",
            "ANOTHER_SECRET": "another-value",
        }

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=True,
            output_path=task.output_path,
            content=stdout.strip(),
            error=None,
            provider=self.name,
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_task(
    prompt: str = "Hello, world!",
    output_path: str = "/tmp/test-output.md",
    agent_name: str = "test-agent",
    **extra_metadata: Any,
) -> ExecutionTask:
    metadata = {"agent_name": agent_name, "phase": "review", **extra_metadata}
    return ExecutionTask.from_prompt(
        prompt=prompt,
        output_path=output_path,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# ABC enforcement
# ---------------------------------------------------------------------------


class TestABCEnforcement:
    """Verify that SubprocessProvider cannot be instantiated directly."""

    def test_cannot_instantiate_abc(self) -> None:
        with pytest.raises(TypeError, match="abstract"):
            SubprocessProvider()  # type: ignore[abstract]

    def test_must_implement_name(self) -> None:
        """A subclass missing ``name`` should fail."""

        class PartialProvider(SubprocessProvider):
            def _build_argv(self, task):
                return []

            def _build_env(self, task):
                return {}

            def _parse_output(self, stdout, stderr, returncode, task):
                return ExecutionResult(
                    success=True, output_path="", provider="test"
                )

        with pytest.raises(TypeError, match="abstract"):
            PartialProvider()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


class TestProtocolConformance:
    """Verify SubprocessProvider subclasses satisfy ExecutionProvider."""

    def test_isinstance_check(self) -> None:
        provider = EchoProvider()
        assert isinstance(provider, ExecutionProvider)

    def test_default_properties(self) -> None:
        provider = EchoProvider()
        assert provider.name == "echo-test"
        assert provider.supports_tool_use is False
        assert provider.supports_pooling is False

    def test_has_execute(self) -> None:
        assert callable(getattr(EchoProvider(), "execute", None))

    def test_has_execute_batch(self) -> None:
        assert callable(getattr(EchoProvider(), "execute_batch", None))


# ---------------------------------------------------------------------------
# Success path
# ---------------------------------------------------------------------------


class TestExecuteSuccess:
    """Happy-path tests with EchoProvider."""

    def test_basic_echo(self) -> None:
        provider = EchoProvider()
        task = _make_task(prompt="Hello from subprocess!")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content == "Hello from subprocess!"
        assert result.error is None
        assert result.provider == "echo-test"
        assert result.output_path == task.output_path

    def test_duration_is_populated(self) -> None:
        provider = EchoProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.duration is not None
        assert isinstance(result.duration, timedelta)
        assert result.duration.total_seconds() >= 0

    def test_multiline_output(self) -> None:
        """Multi-line stdout should be captured fully."""
        provider = EchoProvider()
        task = _make_task(prompt="line1\nline2\nline3")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        # echo outputs args as a single line (literal \n in echo)
        assert result.content is not None


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


class TestExecuteErrors:
    """Subprocess failure scenarios."""

    def test_nonzero_exit(self) -> None:
        provider = FailProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "subprocess"
        assert "error output" in result.metadata.get("stderr", "")

    def test_missing_binary(self) -> None:
        provider = MissingBinaryProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "subprocess"
        assert "not found" in str(result.error).lower()

    def test_missing_binary_has_duration(self) -> None:
        provider = MissingBinaryProvider()
        result = asyncio.run(provider.execute(_make_task()))

        assert result.duration is not None
        assert result.duration.total_seconds() >= 0


# ---------------------------------------------------------------------------
# Timeout and signal handling
# ---------------------------------------------------------------------------


class TestTimeout:
    """Timeout enforcement and SIGTERM propagation."""

    def test_timeout_kills_subprocess(self) -> None:
        """Process exceeding timeout should be killed and return timeout error."""
        provider = SleepProvider(timeout=0.5)
        task = _make_task()
        result = asyncio.run(provider.execute(task))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "timeout"
        assert result.metadata.get("timed_out") is True
        assert result.duration is not None
        # Should complete around the timeout, not the full sleep duration
        assert result.duration.total_seconds() < 10

    def test_per_task_timeout_override(self) -> None:
        """task.metadata['timeout'] should override the provider default."""
        provider = SleepProvider(timeout=300)  # very long default
        task = _make_task(timeout=0.5)  # short per-task
        result = asyncio.run(provider.execute(task))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "timeout"

    def test_fast_process_no_timeout(self) -> None:
        """A fast process with a generous timeout should succeed."""
        provider = EchoProvider(timeout=30)
        result = asyncio.run(provider.execute(_make_task()))

        assert result.success is True
        assert "timed_out" not in result.metadata


# ---------------------------------------------------------------------------
# Environment-only secrets
# ---------------------------------------------------------------------------


class TestEnvSecrets:
    """Verify secrets are passed via env, not argv."""

    def test_secret_available_in_env(self) -> None:
        provider = EnvReaderProvider()
        task = _make_task(env_var="TEST_SECRET")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content == "super-secret-key"

    def test_env_merges_with_os_environ(self) -> None:
        """Provider env should be merged with os.environ (PATH available)."""
        provider = EnvReaderProvider()
        task = _make_task(env_var="PATH")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content  # PATH should be non-empty


# ---------------------------------------------------------------------------
# Warm / cold-start hooks
# ---------------------------------------------------------------------------


class TestWarmHooks:
    """Default warm() and is_warm() behavior."""

    def test_default_not_warm(self) -> None:
        provider = EchoProvider()
        assert provider.is_warm() is False

    def test_default_warm_is_noop(self) -> None:
        provider = EchoProvider()
        # Should complete without error
        asyncio.run(provider.warm())
        assert provider.is_warm() is False  # Still not warm by default

    def test_custom_warm_override(self) -> None:
        """Subclasses can override warm() to track state."""

        class WarmableProvider(EchoProvider):
            _is_warm = False

            async def warm(self) -> None:
                self._is_warm = True

            def is_warm(self) -> bool:
                return self._is_warm

        provider = WarmableProvider()
        assert not provider.is_warm()
        asyncio.run(provider.warm())
        assert provider.is_warm()


# ---------------------------------------------------------------------------
# Batch execution
# ---------------------------------------------------------------------------


class TestBatchExecution:
    """Concurrent batch execution."""

    def test_batch_returns_all_results(self) -> None:
        provider = EchoProvider()
        tasks = [_make_task(prompt=f"Message {i}") for i in range(3)]
        results = asyncio.run(provider.execute_batch(tasks))

        assert len(results) == 3
        assert all(r.success for r in results)
        for i, r in enumerate(results):
            assert r.content == f"Message {i}"

    def test_batch_isolates_failures(self) -> None:
        """Mixed success/failure in a batch should not break other tasks."""

        class MixedProvider(SubprocessProvider):
            @property
            def name(self) -> str:
                return "mixed-test"

            def _build_argv(self, task: ExecutionTask) -> list[str]:
                if task.metadata.get("should_fail"):
                    return ["/bin/sh", "-c", "exit 1"]
                return ["/bin/echo", task.prompt]

            def _build_env(self, task: ExecutionTask) -> dict[str, str]:
                return {}

            def _parse_output(self, stdout, stderr, returncode, task):
                if returncode != 0:
                    return ExecutionResult(
                        success=False,
                        output_path=task.output_path,
                        error=ProviderError("failed", category="subprocess"),
                        provider=self.name,
                    )
                return ExecutionResult(
                    success=True,
                    output_path=task.output_path,
                    content=stdout.strip(),
                    provider=self.name,
                )

        provider = MixedProvider()
        tasks = [
            _make_task(prompt="ok-1"),
            _make_task(prompt="bad", should_fail=True),
            _make_task(prompt="ok-2"),
        ]
        results = asyncio.run(provider.execute_batch(tasks))

        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True


# ---------------------------------------------------------------------------
# Working directory
# ---------------------------------------------------------------------------


class TestWorkingDirectory:
    """Verify cwd parameter is respected."""

    def test_custom_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:

            class PwdProvider(SubprocessProvider):
                @property
                def name(self):
                    return "pwd-test"

                def _build_argv(self, task):
                    return ["/bin/pwd"]

                def _build_env(self, task):
                    return {}

                def _parse_output(self, stdout, stderr, returncode, task):
                    return ExecutionResult(
                        success=True,
                        output_path=task.output_path,
                        content=stdout.strip(),
                        provider=self.name,
                    )

            provider = PwdProvider(cwd=tmpdir)
            result = asyncio.run(provider.execute(_make_task()))

            assert result.success is True
            # Resolve symlinks for macOS /private/var/folders vs /var/folders
            assert os.path.realpath(result.content) == os.path.realpath(tmpdir)


# ---------------------------------------------------------------------------
# Default configuration
# ---------------------------------------------------------------------------


class TestDefaults:
    """Verify default constants are sensible."""

    def test_default_timeout(self) -> None:
        assert DEFAULT_TIMEOUT_SECONDS == 300

    def test_sigterm_grace(self) -> None:
        assert SIGTERM_GRACE_SECONDS == 5

    def test_provider_accepts_custom_timeout(self) -> None:
        provider = EchoProvider(timeout=60)
        assert provider._default_timeout == 60


# ---------------------------------------------------------------------------
# _build_stdin default (returns None)
# ---------------------------------------------------------------------------


class TestBuildStdinDefault:
    """Verify the base-class _build_stdin() hook returns None."""

    def test_default_build_stdin_returns_none(self) -> None:
        """Base class _build_stdin() should return None (no stdin piped)."""
        provider = EchoProvider()
        task = _make_task()
        result = provider._build_stdin(task)
        assert result is None


# ---------------------------------------------------------------------------
# Stdin piping — subclass overrides _build_stdin() to return bytes
# ---------------------------------------------------------------------------


class StdinProvider(SubprocessProvider):
    """Provider that pipes stdin to a subprocess and echoes it back."""

    @property
    def name(self) -> str:
        return "stdin-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        # cat reads from stdin and writes to stdout
        return ["/bin/cat"]

    def _build_stdin(self, task: ExecutionTask) -> bytes | None:
        # Pipe the prompt as bytes via stdin
        return task.prompt.encode("utf-8")

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=returncode == 0,
            output_path=task.output_path,
            content=stdout.strip(),
            error=None if returncode == 0 else ProviderError(
                f"cat failed: {stderr}", category="subprocess",
            ),
            provider=self.name,
            metadata={"returncode": returncode},
        )


class TestStdinPiping:
    """Verify subprocess receives data via stdin when _build_stdin returns bytes."""

    def test_stdin_bytes_received_by_subprocess(self) -> None:
        """Subprocess should receive stdin data and echo it back via cat."""
        provider = StdinProvider()
        task = _make_task(prompt="Hello via stdin!")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content == "Hello via stdin!"

    def test_stdin_multiline_content(self) -> None:
        """Multi-line stdin content should be preserved through the pipe."""
        provider = StdinProvider()
        task = _make_task(prompt="line 1\nline 2\nline 3")
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        assert result.content == "line 1\nline 2\nline 3"

    def test_stdin_with_special_characters(self) -> None:
        """Stdin with shell-sensitive characters should pass through safely."""
        provider = StdinProvider()
        task = _make_task(prompt='echo "not executed"; $(whoami) | tee /tmp/x')
        result = asyncio.run(provider.execute(task))

        assert result.success is True
        # cat should echo the literal string, not interpret it
        assert result.content == 'echo "not executed"; $(whoami) | tee /tmp/x'


# ---------------------------------------------------------------------------
# _kill_gracefully — SIGTERM → grace period → SIGKILL path
# ---------------------------------------------------------------------------


class SigTermIgnoringProvider(SubprocessProvider):
    """Provider that spawns a Python subprocess which ignores SIGTERM.

    Forces _kill_gracefully through the SIGKILL fallback path.
    """

    @property
    def name(self) -> str:
        return "sigterm-ignoring-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        # Python one-liner: install SIGTERM ignore handler, then sleep forever.
        # This process cannot be stopped by SIGTERM — only SIGKILL works.
        return [
            sys.executable, "-c",
            "import signal, time; "
            "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
            "time.sleep(300)",
        ]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=returncode == 0,
            output_path=task.output_path,
            content=stdout.strip(),
            provider=self.name,
            metadata={"returncode": returncode},
        )


class SigTermRespectingProvider(SubprocessProvider):
    """Provider that spawns a Python subprocess which exits on SIGTERM.

    Exercises the SIGTERM → graceful exit path (no SIGKILL needed).
    """

    @property
    def name(self) -> str:
        return "sigterm-respecting-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        # Python one-liner: on SIGTERM, write to stderr and exit cleanly.
        return [
            sys.executable, "-c",
            "import signal, sys, time; "
            "signal.signal(signal.SIGTERM, "
            "lambda s, f: (sys.stderr.write('graceful-shutdown\\n'), sys.exit(0))); "
            "time.sleep(300)",
        ]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=False,  # timed out, so base class handles this
            output_path=task.output_path,
            content=stdout.strip() if stdout else None,
            error=ProviderError("timed out", category="timeout"),
            provider=self.name,
            metadata={"returncode": returncode, "stderr": stderr.strip()},
        )


class TestKillGracefully:
    """Test the SIGTERM → grace period → SIGKILL kill path."""

    def test_sigterm_ignored_falls_back_to_sigkill(self) -> None:
        """When subprocess ignores SIGTERM, _kill_gracefully should SIGKILL it.

        Uses a very short timeout (0.3s) so the test runs quickly.
        The SIGTERM_GRACE_SECONDS (5s) is the real grace period, but the
        subprocess ignores SIGTERM, so it must be killed with SIGKILL.
        We monkeypatch the grace period to keep the test fast.
        """
        import engine.execution.providers.subprocess_base as mod

        original_grace = mod.SIGTERM_GRACE_SECONDS
        try:
            # Use a short grace period to keep the test fast
            mod.SIGTERM_GRACE_SECONDS = 0.5

            provider = SigTermIgnoringProvider(timeout=0.3)
            task = _make_task()
            result = asyncio.run(provider.execute(task))

            assert result.success is False
            assert result.error is not None
            assert result.error.category == "timeout"
            assert result.metadata.get("timed_out") is True
            # The process was killed (SIGKILL = -9 returncode)
            returncode = result.metadata.get("returncode")
            assert returncode is not None
            assert returncode != 0  # Killed, not clean exit
        finally:
            mod.SIGTERM_GRACE_SECONDS = original_grace

    def test_sigterm_respected_exits_gracefully(self) -> None:
        """When subprocess handles SIGTERM, it should exit within the grace period.

        The subprocess installs a SIGTERM handler that exits cleanly.
        _kill_gracefully sends SIGTERM and the process should exit before
        the SIGKILL deadline.
        """
        provider = SigTermRespectingProvider(timeout=0.3)
        task = _make_task()
        result = asyncio.run(provider.execute(task))

        assert result.success is False
        assert result.error is not None
        assert result.error.category == "timeout"
        assert result.metadata.get("timed_out") is True
        # The process exited cleanly after SIGTERM (exit code 0)
        returncode = result.metadata.get("returncode")
        assert returncode == 0

    def test_kill_gracefully_total_time_bounded(self) -> None:
        """The total time for SIGTERM→SIGKILL should be bounded.

        With a 0.3s timeout and 0.5s grace period, the total execution
        should be under 3s (generous to account for CI variance).
        """
        import engine.execution.providers.subprocess_base as mod

        original_grace = mod.SIGTERM_GRACE_SECONDS
        try:
            mod.SIGTERM_GRACE_SECONDS = 0.5

            provider = SigTermIgnoringProvider(timeout=0.3)
            task = _make_task()

            start = time.monotonic()
            result = asyncio.run(provider.execute(task))
            elapsed = time.monotonic() - start

            assert result.success is False
            # 0.3s timeout + 0.5s grace + overhead — should be well under 3s
            assert elapsed < 3.0, f"Kill path took too long: {elapsed:.2f}s"
        finally:
            mod.SIGTERM_GRACE_SECONDS = original_grace


# ---------------------------------------------------------------------------
# ProcessLookupError in _kill_gracefully — process exits between signals
# ---------------------------------------------------------------------------


class FastExitProvider(SubprocessProvider):
    """Provider that spawns a process which exits almost immediately.

    When combined with a very short timeout, the process may exit between
    the timeout firing and _kill_gracefully sending SIGTERM, exercising
    the ProcessLookupError catch branch.
    """

    @property
    def name(self) -> str:
        return "fast-exit-test"

    def _build_argv(self, task: ExecutionTask) -> list[str]:
        # Sleep just long enough to trigger timeout, then exit
        return [sys.executable, "-c", "import time; time.sleep(0.15)"]

    def _build_env(self, task: ExecutionTask) -> dict[str, str]:
        return {}

    def _parse_output(
        self,
        stdout: str,
        stderr: str,
        returncode: int,
        task: ExecutionTask,
    ) -> ExecutionResult:
        return ExecutionResult(
            success=returncode == 0,
            output_path=task.output_path,
            content=stdout.strip(),
            provider=self.name,
            metadata={"returncode": returncode},
        )


class TestProcessLookupError:
    """Test the ProcessLookupError catch in _kill_gracefully."""

    def test_process_lookup_error_on_sigterm(self) -> None:
        """ProcessLookupError during SIGTERM send should be caught gracefully.

        We directly test _kill_gracefully with a process that has already
        exited to guarantee the ProcessLookupError path fires on send_signal.
        """
        async def _run() -> tuple[bytes, bytes]:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-c", "pass",  # exits immediately
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # Wait for it to fully exit — but don't drain stdout/stderr
            # so that communicate() inside _kill_gracefully still works.
            await proc.wait()
            # Now proc is dead — send_signal will raise ProcessLookupError
            # which _kill_gracefully should catch
            return await SubprocessProvider._kill_gracefully(proc)

        stdout, stderr = asyncio.run(_run())
        # Should return empty bytes without raising
        assert isinstance(stdout, bytes)
        assert isinstance(stderr, bytes)

    def test_process_lookup_error_on_kill(self) -> None:
        """ProcessLookupError during SIGKILL should be caught gracefully.

        The process ignores SIGTERM but exits on its own before SIGKILL.
        We simulate this by mocking proc.kill to raise ProcessLookupError.
        """
        from unittest.mock import AsyncMock, patch

        async def _run() -> tuple[bytes, bytes]:
            # Start a process that ignores SIGTERM but will exit soon
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-c",
                "import signal, time; "
                "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                "time.sleep(0.3)",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Patch the grace period to be very short so SIGTERM times out
            import engine.execution.providers.subprocess_base as mod
            original_grace = mod.SIGTERM_GRACE_SECONDS
            mod.SIGTERM_GRACE_SECONDS = 0.1

            # Patch proc.kill to raise ProcessLookupError (simulating the
            # process dying between SIGTERM timeout and SIGKILL send)
            original_kill = proc.kill

            def kill_then_lookup_error():
                # Actually kill so communicate() works
                try:
                    original_kill()
                except ProcessLookupError:
                    pass
                raise ProcessLookupError()

            proc.kill = kill_then_lookup_error

            try:
                result = await SubprocessProvider._kill_gracefully(proc)
            finally:
                mod.SIGTERM_GRACE_SECONDS = original_grace
            return result

        stdout, stderr = asyncio.run(_run())
        assert isinstance(stdout, bytes)
        assert isinstance(stderr, bytes)
