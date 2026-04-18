"""Tests for :mod:`conversus.paths`.

Regression tests for the promote-from-private hot-fix (2026-04-18).
The module is imported by ``engine/config.py``, ``engine/_root.py``,
``engine/templates.py``, ``linter/validate.py``, and two
``conversus/schemas/*.py`` files. Before the promote, those imports
resolved only if the private repo was on the Python path simultaneously;
published OSS wheels would fail on any code path hitting them.
"""

from __future__ import annotations

from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Acceptance: module + symbols exist
# ---------------------------------------------------------------------------


def test_conversus_paths_module_importable() -> None:
    """``from conversus.paths import ...`` resolves — the module exists."""
    import conversus.paths  # noqa: F401


def test_public_symbols_present() -> None:
    """All five public symbols referenced by OSS consumers are importable."""
    from conversus.paths import (
        get_presets_dir,
        get_scaffold_dir,
        get_template_path,
        get_templates_dir,
        resolve_package_path,
    )

    assert callable(resolve_package_path)
    assert callable(get_templates_dir)
    assert callable(get_template_path)
    assert callable(get_presets_dir)
    assert callable(get_scaffold_dir)


# ---------------------------------------------------------------------------
# Behavior: templates / presets resolve from the conversus package
# ---------------------------------------------------------------------------


def test_get_templates_dir_returns_existing_path() -> None:
    """``get_templates_dir()`` returns a path that exists on disk."""
    from conversus.paths import get_templates_dir

    templates = get_templates_dir()
    assert isinstance(templates, Path)
    assert templates.exists(), f"templates dir resolved to {templates} but not on disk"
    assert templates.is_dir()


def test_get_template_path_cooperative_review() -> None:
    """A known template (cooperative review) resolves to a real file."""
    from conversus.paths import get_template_path

    path = get_template_path("cooperative", "review.md")
    assert path.exists(), f"expected cooperative/review.md at {path}"
    assert path.is_file()


def test_get_presets_dir_returns_existing_path() -> None:
    """``get_presets_dir()`` returns a path that exists on disk."""
    from conversus.paths import get_presets_dir

    presets = get_presets_dir()
    assert isinstance(presets, Path)
    assert presets.exists(), f"presets dir resolved to {presets} but not on disk"
    assert presets.is_dir()


# ---------------------------------------------------------------------------
# Behavior: resolve_package_path error path
# ---------------------------------------------------------------------------


def test_resolve_package_path_raises_on_missing() -> None:
    """Unresolvable paths raise ``FileNotFoundError`` with an informative message."""
    from conversus.paths import resolve_package_path

    with pytest.raises(FileNotFoundError, match="Cannot locate"):
        resolve_package_path("conversus", "this-dir-does-not-exist-xyz123")


# ---------------------------------------------------------------------------
# Regression: the six OSS consumers can import what they need
# ---------------------------------------------------------------------------


def test_engine_config_import_path() -> None:
    """``engine/config.py`` imports ``get_presets_dir`` — verify it resolves."""
    from conversus.paths import get_presets_dir

    assert callable(get_presets_dir)


def test_engine_templates_import_path() -> None:
    """``engine/templates.py`` imports ``get_templates_dir``."""
    from conversus.paths import get_templates_dir

    assert callable(get_templates_dir)


def test_schemas_construction_import_path() -> None:
    """``conversus/schemas/construction.py`` imports ``resolve_package_path``."""
    from conversus.paths import resolve_package_path

    assert callable(resolve_package_path)
