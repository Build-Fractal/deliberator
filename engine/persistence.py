"""Deliberation persistence utility for spec 056.

Provides functions for persisting, listing, and reading deliberation
output.  Called by handlers in ``engine/handlers.py`` after pipeline
completion.

Constitution compliance
-----------------------
- Principle IX: no mutable module-level state, explicit typing on every
  function signature, ``StrEnum`` for closed choice sets.
- Principle XI: single source of truth — all persistence logic lives
  here; callers import rather than reimplementing.

See ``specs/056-deliberation-persistence.md``.
"""

from __future__ import annotations

import logging
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger("conversus.persistence")

_CONVERSUS_DIR = Path(".conversus")
_DELIBERATIONS_REL = _CONVERSUS_DIR / "deliberations"
_SETTINGS_FILE = _CONVERSUS_DIR / "settings.yml"


# ---------------------------------------------------------------------------
# Project root discovery
# ---------------------------------------------------------------------------


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from *start* looking for a directory containing ``.conversus/``
    or ``conversus.yml``, returning the first match.

    Falls back to *start* (or ``Path.cwd()``) if no marker is found —
    this is the correct behavior for first-run scenarios where neither
    ``conversus init`` nor a previous deliberation has created the
    ``.conversus/`` directory yet.

    This is critical for MCP servers: Claude Desktop and other editors
    may launch the server with CWD set to the home directory or the
    bundle install directory, not the user's project. Walking up from
    the config file's parent (when available) or the CWD finds the
    project root reliably.
    """
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
# Public API
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
