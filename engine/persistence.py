"""Deliberation persistence utility.

Provides functions for persisting, listing, and reading deliberation
output. Called by handlers in ``engine/handlers.py`` after pipeline
completion (spec 056) and by phase writers on every output emission
(v4.2.0 spec § 5.1 D1).

Constitution compliance
-----------------------
- Principle V (non-blocking writes): ``persist_output`` writes the file
  UNCONDITIONALLY before any validation. Malformed output is preferred
  over no output. See § 5.1 D1.
- Principle IX: no mutable module-level state, explicit typing on every
  function signature, ``StrEnum`` for closed choice sets.
- Principle XI: single source of truth — all persistence logic lives
  here; callers import rather than reimplementing.

See ``specs/056-deliberation-persistence.md`` (post-run copy) and
``specs/v4.2.0-structured-deliberation-outputs/spec.md`` § 5.1 (per-output
unconditional-write + post-validate).
"""

from __future__ import annotations

import json
import logging
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Protocol

import yaml

from engine.schema_validator import SchemaValidator

logger = logging.getLogger("conversus.persistence")


class EventStream(Protocol):
    """Minimal interface persist_output needs from the engine event stream.

    The full event-stream API lives in the engine's orchestration layer; we
    declare only the surface persist_output touches so this module stays
    decoupled from orchestration internals.
    """

    def warn(self, *, event: str, **fields: Any) -> None: ...

_CONVERSUS_DIR = Path(".conversus")
_DELIBERATIONS_REL = _CONVERSUS_DIR / "deliberations"
_SETTINGS_FILE = _CONVERSUS_DIR / "settings.yml"


# ---------------------------------------------------------------------------
# Project root discovery
# ---------------------------------------------------------------------------


def find_user_project_root(start: Path | None = None) -> Path:
    """Discover the user's conversus *workspace* root.

    This is the directory that holds (or should hold) the user's
    ``.conversus/`` folder — i.e. the place where deliberation output,
    project-level settings, and other persistent artifacts live. It is
    distinct from :func:`engine._root.find_project_root`, which locates
    the conversus *package install root* (the directory containing
    ``presets/``, ``schema/``, and ``templates/``). Mixing the two roots
    causes ``_parse_and_validate_config`` to look for ``schema/`` under
    the user's home directory and raise ``SchemaLoadError`` whenever
    ``~/.conversus/`` exists.

    Resolution order:

    1. ``CONVERSUS_ROOT`` environment variable — set by the Desktop
       Extension's ``main.py`` to point at the bundled ``server/``
       directory. This is the highest priority because the bundle's
       runtime data (presets, schema, templates) is at a known path.
    2. Walk up from *start* (or CWD) looking for ``.conversus/`` or
       ``conversus.yml`` — the standard marker-based discovery for the
       user workspace.
    3. Fall back to *start* (or CWD) — correct for first-run scenarios.

    This is critical for MCP servers: Claude Desktop may launch the
    server with CWD set to the home directory, not the project.
    """
    import os

    env_root = os.environ.get("CONVERSUS_ROOT")
    if env_root:
        root = Path(env_root).resolve()
        if root.is_dir():
            return root

    current = (start or Path.cwd()).resolve()
    for parent in [current, *current.parents]:
        if (parent / _CONVERSUS_DIR).is_dir():
            return parent
        if (parent / "conversus.yml").is_file():
            return parent
    # No marker found — fall back to start directory
    return current


def is_persistence_enabled(project_root: Path) -> bool:
    """Check whether persistence is enabled via the settings cascade.

    Delegates to ``engine.settings.load_settings`` (spec 057) which
    resolves the full cascade: project ``.conversus/settings.yml`` →
    global ``~/.conversus/settings.yml`` → built-in defaults.

    Returns ``True`` by default when no settings files exist (persist-
    by-default per spec 056). Returns ``False`` only when a settings
    file explicitly sets ``persistence: enabled: false``.
    """
    from engine.settings import load_settings

    settings = load_settings(project_root)
    return settings.persistence.enabled


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _make_slug(text: str, max_len: int = 40) -> str:
    """Sanitize *text* to a filesystem-safe slug.

    Lowercases, replaces non-alphanumeric runs with a single hyphen,
    strips leading/trailing hyphens, and truncates to *max_len*.
    """
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:max_len]


def _make_timestamp() -> str:
    """Return an ISO 8601 compact UTC timestamp (``YYYYMMDDTHHMMSS``)."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def _parse_dir_timestamp(name: str) -> datetime | None:
    """Extract the leading timestamp from a deliberation directory name.

    Expected format: ``YYYYMMDDTHHMMSS-<slug>``.  Returns ``None`` if
    the timestamp prefix cannot be parsed (caller should skip, not
    delete).
    """
    parts = name.split("-", 1)
    if not parts:
        return None
    ts_part = parts[0]
    try:
        return datetime.strptime(ts_part, "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Public API — per-output write (v4.2.0 spec § 5.1 D1)
# ---------------------------------------------------------------------------


_DEFAULT_SCHEMA_VERSION = "1.0.0-rc.1"


def _read_schema_version(content: bytes) -> str:
    """Extract ``schema_version`` from envelope JSON bytes.

    Returns the validator's default (``1.0.0-rc.1``) when the bytes are not
    valid JSON, are not an object, or do not declare ``schema_version``. Per
    Principle V this MUST NOT raise — the unconditional write in
    ``persist_output`` has already happened by the time we read this, and any
    parse failure here surfaces downstream as a validation warning instead.
    """
    try:
        envelope = json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _DEFAULT_SCHEMA_VERSION
    if isinstance(envelope, dict):
        version = envelope.get("schema_version")
        if isinstance(version, str) and version:
            return version
    return _DEFAULT_SCHEMA_VERSION


def persist_output(
    path: Path,
    content: bytes,
    validator: SchemaValidator,
    event_stream: EventStream,
) -> None:
    """Persist a single deliberation output to disk with non-blocking validation.

    Per v4.2.0 spec § 5.1 D1. The order of operations is load-bearing:

    1. ``path.write_bytes(content)`` — UNCONDITIONAL. Per Principle V
       (build-fractal/CONSTITUTION.md L76-78): "malformed output is better
       than no output". This MUST be the first side effect.
    2. ``validator.validate(content, schema_version)`` — produces
       ``ValidationResult``. Contractually non-raising on conformance failure.
    3. If ``not result.is_conformant``: emit a ``schema_validation_failed``
       warning to the event stream + write the ``.validation-warnings.json``
       sidecar via ``validator.emit_warning``.

    There is NO exception path that prevents step 1. If anything between steps
    1 and 3 raises an unexpected error (e.g., validator infra fault that
    bypassed startup detection), the exception propagates AFTER the bytes are
    on disk — Principle V is preserved.

    The schema version is read from the envelope itself; callers do not pass
    it. This keeps the call site minimal and avoids drift between what the
    envelope declares and what the validator was told to expect.
    """
    # Step 1 — unconditional write (Principle V). Must be the first side effect.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)

    # Step 2 — post-write validation. validate() is non-raising.
    schema_version = _read_schema_version(content)
    result = validator.validate(content, schema_version)

    # Step 3 — non-blocking warning + sidecar on non-conformance.
    if not result.is_conformant:
        event_stream.warn(
            event="schema_validation_failed",
            path=str(path),
            output_type=result.output_type,
            schema_version=result.schema_version,
            warnings=[w.to_dict() for w in result.warnings],
        )
        validator.emit_warning(result, path)


# ---------------------------------------------------------------------------
# Public API — post-run deliberation copy (spec 056)
# ---------------------------------------------------------------------------


def persist_deliberation(
    source_dir: Path,
    project_root: Path,
    question: str,
    config_path: Path | None = None,
) -> Path:
    """Copy a completed deliberation's output tree into persistent storage.

    Creates the directory
    ``<project_root>/.conversus/deliberations/<timestamp>-<slug>/output/``
    and copies the full *source_dir* tree into it.  A ``question.md``
    file is written alongside ``output/``.  If *config_path* is
    provided, it is copied as ``conversus.yml`` into the deliberation
    directory.

    The ``.conversus/deliberations/`` directory is created lazily if it
    does not already exist.

    Args:
        source_dir: The engine output directory to persist.
        project_root: The project root containing ``.conversus/``.
        question: The deliberation question text.
        config_path: Optional path to the ``conversus.yml`` used for the
            run.  Copied into the persisted directory for provenance.

    Returns:
        The path to the newly created deliberation directory.
    """
    timestamp = _make_timestamp()
    slug = _make_slug(question)
    dir_name = f"{timestamp}-{slug}" if slug else timestamp

    delib_dir = project_root / _DELIBERATIONS_REL / dir_name
    delib_dir.mkdir(parents=True, exist_ok=True)

    # Copy output tree
    output_dest = delib_dir / "output"
    shutil.copytree(str(source_dir), str(output_dest), dirs_exist_ok=True)

    # Write question text
    question_file = delib_dir / "question.md"
    question_file.write_text(question, encoding="utf-8")

    # Copy config if provided
    if config_path is not None and config_path.exists():
        shutil.copy2(str(config_path), str(delib_dir / "conversus.yml"))

    logger.info("Persisted deliberation to %s", delib_dir)
    return delib_dir


def cleanup_old_deliberations(
    project_root: Path,
    retention_days: int = 90,
) -> int:
    """Delete deliberation directories older than *retention_days*.

    Scans ``<project_root>/.conversus/deliberations/``, parses the
    timestamp prefix of each subdirectory, and removes those whose
    timestamp is older than the retention window.

    Directories with unparseable timestamps are silently skipped —
    don't delete what you don't understand.

    Args:
        project_root: The project root containing ``.conversus/``.
        retention_days: Number of days to retain deliberations.

    Returns:
        The number of directories deleted.
    """
    delib_root = project_root / _DELIBERATIONS_REL
    if not delib_root.is_dir():
        return 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    deleted = 0

    for child in sorted(delib_root.iterdir()):
        if not child.is_dir():
            continue

        ts = _parse_dir_timestamp(child.name)
        if ts is None:
            logger.warning(
                "Skipping directory with unparseable timestamp: %s",
                child.name,
            )
            continue

        if ts < cutoff:
            shutil.rmtree(str(child), ignore_errors=True)
            logger.info("Deleted old deliberation: %s", child.name)
            deleted += 1

    return deleted


def list_deliberations(project_root: Path) -> list[dict[str, Any]]:
    """List all persisted deliberations with metadata.

    Scans ``<project_root>/.conversus/deliberations/`` and for each
    directory extracts the timestamp, reads ``question.md``, and reads
    ``conversus.yml`` for mode and agent names.

    Returns:
        A list of dicts sorted by timestamp descending (newest first).
        Each dict contains:

        - ``timestamp`` — the parsed UTC datetime or ``None``
        - ``question`` — the question text or ``""``
        - ``mode`` — the deliberation mode from config or ``None``
        - ``agents`` — list of agent name strings or ``[]``
        - ``path`` — absolute ``Path`` to the deliberation directory
        - ``has_synthesis`` — whether ``output/summary/final.md`` exists
    """
    delib_root = project_root / _DELIBERATIONS_REL
    if not delib_root.is_dir():
        return []

    results: list[dict[str, Any]] = []

    for child in delib_root.iterdir():
        if not child.is_dir():
            continue

        ts = _parse_dir_timestamp(child.name)

        # Read question
        question_file = child / "question.md"
        question = ""
        if question_file.exists():
            try:
                question = question_file.read_text(encoding="utf-8").strip()
            except OSError:
                logger.warning("Could not read %s", question_file)

        # Read config for mode and agents
        mode: str | None = None
        agents: list[str] = []
        config_file = child / "conversus.yml"
        if config_file.exists():
            try:
                config_data = yaml.safe_load(
                    config_file.read_text(encoding="utf-8")
                )
                if isinstance(config_data, dict):
                    mode = config_data.get("mode")
                    raw_agents = config_data.get("agents", [])
                    if isinstance(raw_agents, list):
                        agents = [
                            a.get("name", "unnamed")
                            for a in raw_agents
                            if isinstance(a, dict)
                        ]
            except (yaml.YAMLError, OSError):
                logger.warning("Could not parse %s", config_file)

        # Check for synthesis
        has_synthesis = (child / "output" / "summary" / "final.md").exists()

        results.append(
            {
                "timestamp": ts,
                "question": question,
                "mode": mode,
                "agents": agents,
                "path": child,
                "has_synthesis": has_synthesis,
            }
        )

    # Sort by timestamp descending; entries without a timestamp sort last
    results.sort(
        key=lambda d: d["timestamp"] or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return results


def read_deliberation_file(
    project_root: Path,
    deliberation_path: str,
    file_path: str,
) -> str:
    """Read a file from a past deliberation.

    Resolves the requested path and validates that it falls inside
    ``<project_root>/.conversus/deliberations/`` to prevent path
    traversal attacks.

    Args:
        project_root: The project root containing ``.conversus/``.
        deliberation_path: Relative or absolute path to the deliberation
            directory (e.g. the ``path`` value from
            :func:`list_deliberations`).
        file_path: Relative path to the file within the deliberation
            directory (e.g. ``"output/summary/final.md"``).

    Returns:
        The file contents as a string.

    Raises:
        ValueError: If the resolved path escapes the deliberations
            directory (path traversal).
        FileNotFoundError: If the target file does not exist.
    """
    delib_root = (project_root / _DELIBERATIONS_REL).resolve()
    target = (project_root / Path(deliberation_path) / file_path).resolve()

    if not target.is_relative_to(delib_root):
        raise ValueError(
            f"Path traversal rejected: {target} is not inside {delib_root}"
        )

    if not target.is_file():
        raise FileNotFoundError(f"File not found: {target}")

    return target.read_text(encoding="utf-8")
