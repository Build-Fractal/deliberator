"""Invocation context detection for the deliberator CLI.

Every invocation of deliberator runs in one of three contexts:

1. **Interactive terminal** — a human typed ``deliberator run`` at a TTY.
   Want human-readable progress rendering and interactive exit codes.

2. **Headless CI / cron / hook / MCP server** — a non-human caller
   invoked the CLI from GitHub Actions, a cron job, a git hook, or
   (post-spec-049) the deliberator MCP server running inside VSCode.
   Want structured JSON output and governance-style exit codes.

3. **Claude Code session** — deliberator is running inside a Claude Code
   interactive session (as opposed to being invoked by Claude Code as
   a subprocess).  Want to defer to the Claude Code host's own progress
   rendering; governance exit codes do not apply.

All three contexts share the same engine code path (spec 042 Phase 2
refactor routes every dispatch through :class:`~engine.execution.ExecutionProvider`).
What differs is the *wrapping layer* — the renderer, the default
provider, the exit code scheme — and that layer resolves once at CLI
startup via :func:`detect_context`.

This module is deliberately dependency-free: no click, no typer, no I/O
beyond ``os.environ`` and ``sys.stdout.isatty()``.  Tests pass the argv,
env, and isatty signals explicitly so every context path can be
exercised without mocking process state.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Literal

# ---------------------------------------------------------------------------
# Type aliases — closed Literals for exhaustive downstream dispatch
# ---------------------------------------------------------------------------

#: Renderer selected by context detection.
#:
#: - ``"tui"``: terminal UI with progress bars, live updates, colors.
#:   Used for interactive terminal sessions.
#: - ``"json"``: machine-readable structured output for CI log capture,
#:   MCP server responses, and programmatic consumers.
#: - ``"plain"``: uncolored plain text for file redirects and logs.
RendererMode = Literal["tui", "json", "plain"]


#: Exit code scheme selected by context detection.
#:
#: - ``"interactive"``: 0 on success, 1 on any failure.  The default for
#:   ``deliberator run`` from a terminal.
#: - ``"governance"``: structured exit codes for spec 048 governance
#:   gates: 0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE.  Selected when
#:   argv contains the ``governance`` subcommand.
ExitCodeScheme = Literal["interactive", "governance"]


# ---------------------------------------------------------------------------
# Constants — env var names we probe for context detection
# ---------------------------------------------------------------------------

#: Environment variable names that indicate a CI environment.  A hit on
#: any of these flips :attr:`InvocationContext.is_ci` to ``True``.
_CI_ENV_VARS: tuple[str, ...] = (
    "CI",                    # GitHub Actions, GitLab CI, CircleCI, Travis, generic
    "GITHUB_ACTIONS",        # GitHub Actions (more specific)
    "GITLAB_CI",             # GitLab CI
    "JENKINS_URL",           # Jenkins
    "CIRCLECI",              # CircleCI
    "BUILDKITE",             # Buildkite
    "TF_BUILD",              # Azure Pipelines
    "TEAMCITY_VERSION",      # TeamCity
    "APPVEYOR",              # AppVeyor
    "DRONE",                 # Drone CI
)

#: Environment variable names that indicate a Claude Code session.  A hit
#: on any of these flips :attr:`InvocationContext.is_claude_code_session`
#: to ``True``.  Multiple names are checked because the variable name has
#: shifted over Claude Code releases.
_CLAUDE_CODE_ENV_VARS: tuple[str, ...] = (
    "CLAUDECODE",            # current canonical name
    "CLAUDE_CODE",           # historical variant
    "CLAUDE_CODE_ACTIVE",    # historical variant
)

#: argv entries that select the governance exit code scheme.  The CLI
#: accepts ``deliberator governance ...``; if ``governance`` appears as the
#: first non-program arg, we flip to governance exit codes.
_GOVERNANCE_SUBCOMMANDS: tuple[str, ...] = (
    "governance",
    "gate",  # spec 011 phase consensus gate path also uses structured exit codes
)


# ---------------------------------------------------------------------------
# InvocationContext dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InvocationContext:
    """Resolved invocation context for a single ``deliberator`` CLI call.

    Constructed once at CLI startup by :func:`detect_context` and passed
    down into the engine.  All downstream code reads the resolved fields
    (``default_provider``, ``renderer``, ``exit_code_scheme``) rather than
    re-probing the environment.

    The raw signal fields (``is_tty``, ``is_ci``, ``is_claude_code_session``,
    ``is_background``, ``env``, ``argv``) are preserved for debugging and
    logging — they document *why* the resolved choices were made.

    Attributes:
        is_tty: ``stdout`` is attached to a terminal.  Proxy for
            "there is a human watching this output."
        is_ci: One of :data:`_CI_ENV_VARS` is set.  Proxy for
            "this is running in a CI/CD pipeline."
        is_claude_code_session: One of :data:`_CLAUDE_CODE_ENV_VARS` is
            set.  Proxy for "deliberator is running inside a Claude Code
            interactive session as the host process — NOT as a subprocess
            spawned by Claude Code."
        is_background: Neither TTY nor Claude Code.  Catches cron jobs,
            git hooks, the spec 049 MCP server, scheduled tasks, and
            pipeline workers that are not themselves CI.
        default_provider: Resolved provider name to use when
            ``deliberator.yml`` does not specify one.  Callers may override
            via explicit config.
        renderer: Renderer mode for output rendering.  The CLI picks a
            renderer class based on this value.
        exit_code_scheme: Exit code taxonomy in effect.
        env: Frozen snapshot of the env vars inspected at detection time,
            for diagnostics.  Not a full env dump — only the ones the
            detection logic consulted.
        argv: Frozen argv snapshot at detection time.
    """

    # Raw signals
    is_tty: bool
    is_ci: bool
    is_claude_code_session: bool
    is_background: bool

    # Resolved choices
    default_provider: str
    renderer: RendererMode
    exit_code_scheme: ExitCodeScheme

    # Debug / logging breadcrumbs
    env: dict[str, str] = field(default_factory=dict)
    argv: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Detection function — pure, all signals passed explicitly for testability
# ---------------------------------------------------------------------------


def detect_context(
    *,
    argv: list[str] | tuple[str, ...] | None = None,
    env: dict[str, str] | None = None,
    stdout_isatty: bool | None = None,
) -> InvocationContext:
    """Resolve the invocation context from process environment.

    Every input can be passed explicitly, so tests can exercise every
    path without mocking process state.  Callers in production leave
    all arguments as ``None`` to read from the real process environment.

    Resolution order:

    1. Read raw signals: ``stdout.isatty()``, CI env vars, Claude Code
       env vars, argv.
    2. Compute ``is_background`` as the inverse of "something human or
       CI is watching" — neither TTY nor Claude Code.
    3. Resolve ``default_provider`` per the spec 042 §5 defaults, with
       the invariant that no provider is selected that requires a
       runtime we cannot detect (e.g., we do not default to
       ``claude-code`` without at least some evidence that ``claude``
       is reachable).
    4. Resolve ``renderer`` from the TTY/CI pair.
    5. Resolve ``exit_code_scheme`` from argv.

    Args:
        argv: Argument list.  Defaults to ``sys.argv`` when ``None``.
        env: Environment mapping.  Defaults to ``os.environ`` when ``None``.
        stdout_isatty: TTY state.  Defaults to ``sys.stdout.isatty()``
            when ``None``.

    Returns:
        A fully-resolved :class:`InvocationContext`.
    """
    # ---- Read raw signals ----
    resolved_env: dict[str, str] = dict(os.environ) if env is None else dict(env)
    resolved_argv: tuple[str, ...] = tuple(sys.argv if argv is None else argv)
    resolved_isatty: bool = (
        bool(sys.stdout.isatty()) if stdout_isatty is None else bool(stdout_isatty)
    )

    # ---- Detect CI ----
    is_ci = any(var in resolved_env and resolved_env[var] for var in _CI_ENV_VARS)

    # ---- Detect Claude Code session ----
    is_claude_code_session = any(
        var in resolved_env and resolved_env[var]
        for var in _CLAUDE_CODE_ENV_VARS
    )

    # ---- Compute background flag ----
    #
    # "Background" means no human and no host session is watching output
    # directly.  A TTY means a human.  A Claude Code session means
    # deliberator's output is being consumed by the host's own renderer.
    # CI is a special case: it's non-human but counts as "watched" for
    # the purpose of rendering (we produce JSON, not TUI; we use
    # governance exit codes when invoked that way).  We still tag CI as
    # NOT background because the renderer and provider choice differ.
    is_background = not resolved_isatty and not is_claude_code_session and not is_ci

    # ---- Resolve default provider (spec 042 §5 + arbitration §0) ----
    #
    # The v1 providers are: mock, anthropic, claude-code, opencode, plus
    # optional litellm companion. Phase 3 has now landed (claude-code is
    # fully implemented), so the resolution prefers claude-code when the
    # session signals it is reachable.
    #
    # Resolution order:
    #   1. Claude Code session detected → "claude-code"
    #      The ``claude`` CLI subprocess uses the host OAuth session, so
    #      this is the safest default for users in Claude Code or Cowork
    #      where ``claude -p`` is reachable. No metered API charges for
    #      OAuth/subscription users.
    #   2. CI environment → "mock"
    #      CI runs without OAuth session by default; mock keeps the
    #      pipeline shape testable without requiring secrets to be
    #      provisioned.
    #   3. Background (no TTY, no CI, no Claude Code) → "mock"
    #      Cron jobs, git hooks, MCP servers spawned outside a session.
    #      Conservative default that won't surprise the operator with
    #      LLM calls.
    #   4. Plain interactive TTY → "mock"
    #      Direct CLI users get mock until they opt-in via settings or
    #      --provider flag.
    #
    # In all paths, an explicit ``settings.yml`` value or ``--provider``
    # flag still wins. This default is the SUGGESTED fallback — what
    # the engine would pick if the user never expressed a preference.
    if is_claude_code_session:
        default_provider = "claude-code"
    else:
        default_provider = "mock"

    # ---- Resolve renderer ----
    if resolved_isatty and not is_ci:
        renderer: RendererMode = "tui"
    elif is_ci:
        renderer = "json"
    else:
        renderer = "plain"

    # ---- Resolve exit code scheme from argv ----
    #
    # argv[0] is the program name; argv[1] is the subcommand.  We flip
    # to governance exit codes if argv[1] is "governance" or "gate".
    exit_code_scheme: ExitCodeScheme = "interactive"
    if len(resolved_argv) >= 2 and resolved_argv[1] in _GOVERNANCE_SUBCOMMANDS:
        exit_code_scheme = "governance"

    # ---- Collect debug env snapshot ----
    #
    # Record only the vars we actually consulted, so the context dict
    # is small and focused for logging.
    debug_env: dict[str, str] = {}
    for var in _CI_ENV_VARS + _CLAUDE_CODE_ENV_VARS:
        if var in resolved_env:
            debug_env[var] = resolved_env[var]

    return InvocationContext(
        is_tty=resolved_isatty,
        is_ci=is_ci,
        is_claude_code_session=is_claude_code_session,
        is_background=is_background,
        default_provider=default_provider,
        renderer=renderer,
        exit_code_scheme=exit_code_scheme,
        env=debug_env,
        argv=resolved_argv,
    )
