"""Shared project root discovery.

Provides a single ``find_project_root`` function used by the CLI, SDK,
and MCP server to locate the deliberator project directory.  Each caller
previously had its own copy of this logic — extracted here per CQ-3.

The ``engine/config.py`` root finder is intentionally *not* shared: it
checks for ``schema/`` + ``templates/`` (different markers) and raises
``ConfigError`` with config-specific messaging.
"""

from __future__ import annotations

from pathlib import Path


def find_project_root(
    *,
    marker: str = "presets",
    anchor: Path | None = None,
) -> Path:
    """Locate the deliberator project root by looking for a marker directory.

    Resolution order:
    1. Parent of *anchor* (if provided), walking up until *marker* is found.
    2. ``importlib.resources`` via ``deliberator.paths`` (works when pip-installed).
    3. Parent of this file's package (``engine/`` -> project root).
    4. Current working directory.

    Args:
        marker: Directory name to look for (default: ``"presets"``).
        anchor: Optional starting path.  When given, its parent chain is
            checked first.

    Returns:
        The first directory containing *marker*.

    Raises:
        FileNotFoundError: If no directory containing *marker* is found.
    """
    # Strategy 0: DELIBERATOR_ROOT env var — set by the Desktop Extension's
    # main.py to point at the bundled server/ directory.
    import os
    env_root = os.environ.get("DELIBERATOR_ROOT")
    if env_root:
        root = Path(env_root).resolve()
        if (root / marker).is_dir():
            return root

    # Strategy 1: anchor's parent chain
    if anchor is not None:
        candidate = anchor.resolve().parent
        for _ in range(10):  # prevent infinite walk
            if (candidate / marker).is_dir():
                return candidate
            parent = candidate.parent
            if parent == candidate:
                break
            candidate = parent

    # Strategy 2: importlib.resources (works when pip-installed)
    try:
        from deliberator.paths import resolve_package_path
        marker_path = resolve_package_path("deliberator", marker)
        if marker_path.is_dir():
            return marker_path.parent
    except (ImportError, FileNotFoundError):
        pass

    # Strategy 3: engine package's parent (engine/ is a direct child of the root)
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / marker).is_dir():
        return candidate

    # Strategy 4: cwd
    cwd = Path.cwd()
    if (cwd / marker).is_dir():
        return cwd

    raise FileNotFoundError(
        f"Cannot locate deliberator project root ({marker}/ directory). "
        "Run from the deliberator directory or ensure engine/ is inside it."
    )
