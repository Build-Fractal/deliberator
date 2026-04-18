"""Package-aware path resolution for conversus data files.

Provides functions that work both in development (source tree) AND when
pip-installed as a package.  Uses ``importlib.resources`` as the primary
strategy and falls back to ``Path(__file__).parent`` traversal for
development convenience.

Three resource categories are handled:

- **Templates** (``templates/{mode}/{phase}.md``) -- competition-mode
  phase templates used by the engine.
- **Presets** (``presets/{category}/{name}.yml``) -- agent persona
  presets referenced in config files.
- **Scaffolds** (per-domain scoring scaffolds in domain implementation
  directories).

When pip-installed, templates and presets live inside the ``conversus``
package thanks to ``[tool.hatch.build.targets.wheel.force-include]`` in
``pyproject.toml``.  In the source tree they live at the project root
alongside ``engine/``, ``linter/``, etc.

Promoted from the private `conversus` repo 2026-04-18 to fix a latent
broken-wheel bug: OSS imported ``from conversus.paths import ...`` in
``engine/config.py``, ``engine/_root.py``, ``engine/templates.py``,
``linter/validate.py``, ``conversus/schemas/construction.py``, and
``conversus/schemas/game_forms.py`` -- but the module did not exist
in OSS. Published wheels would have failed on any code path that hit
those imports. See
``payer-index-mono/deliberations/conversus-divergence/private-decomposition-audit.md``
for the audit that surfaced this.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path


# ---------------------------------------------------------------------------
# Generic resolver
# ---------------------------------------------------------------------------


def resolve_package_path(package: str, *parts: str) -> Path:
    """Resolve a path inside a Python package that works both installed and in dev.

    Strategy:
      1. ``importlib.resources.files(package) / parts`` -- works when the
         package is pip-installed and the data files are included in the wheel.
      2. Walk up from this file's directory looking for the first path
         component -- works in the source tree where ``templates/`` and
         ``presets/`` sit at the project root alongside ``engine/``.

    Args:
        package: Top-level package name (e.g. ``"conversus"``).
        *parts: Path components relative to the package root
            (e.g. ``"templates", "cooperative", "review.md"``).

    Returns:
        Resolved ``Path`` to the resource.

    Raises:
        FileNotFoundError: If the resource cannot be found via either strategy.
    """
    joined = "/".join(parts)

    # Strategy 1: importlib.resources (pip-installed)
    try:
        ref = resources.files(package)
        for part in parts:
            ref = ref / part
        # Materialise to a real path -- works for packages on disk
        resolved = Path(str(ref))
        if resolved.exists():
            return resolved
    except (TypeError, FileNotFoundError, ModuleNotFoundError):
        pass

    # Strategy 2: walk up from this file to find the first path component
    # (e.g. "templates") at the project root.
    if parts:
        current = Path(__file__).resolve().parent  # conversus/
        for _ in range(5):  # max 5 levels up
            candidate = current / Path(*parts)
            if candidate.exists():
                return candidate
            current = current.parent

    raise FileNotFoundError(
        f"Cannot locate {joined} in package '{package}'. "
        "Ensure the conversus package is properly installed or run from "
        "the source tree."
    )


# ---------------------------------------------------------------------------
# Convenience: templates
# ---------------------------------------------------------------------------


def get_templates_dir() -> Path:
    """Locate the ``templates/`` directory.

    Returns:
        Path to the templates directory.

    Raises:
        FileNotFoundError: If templates/ cannot be found.
    """
    return resolve_package_path("conversus", "templates")


def get_template_path(mode: str, template_name: str) -> Path:
    """Resolve a specific template file path.

    Args:
        mode: Competition mode (e.g. ``"cooperative"``).
        template_name: Template filename (e.g. ``"review.md"``).

    Returns:
        Path to the template file.

    Raises:
        FileNotFoundError: If the template cannot be found.
    """
    return resolve_package_path("conversus", "templates", mode, template_name)


# ---------------------------------------------------------------------------
# Convenience: presets
# ---------------------------------------------------------------------------


def get_presets_dir() -> Path:
    """Locate the ``presets/`` directory.

    Returns:
        Path to the presets directory.

    Raises:
        FileNotFoundError: If presets/ cannot be found.
    """
    return resolve_package_path("conversus", "presets")


# ---------------------------------------------------------------------------
# Convenience: scaffolds (per-domain)
# ---------------------------------------------------------------------------


def get_scaffold_dir(domain_package: str, *subpath: str) -> Path:
    """Locate a domain's ``scaffolds/`` directory.

    Works for any domain implementation that stores scaffolds alongside
    its module.  E.g.::

        get_scaffold_dir(
            "conversus.domains.implementations.code_review",
            "scaffolds",
        )

    Args:
        domain_package: Fully-qualified package name of the domain.
        *subpath: Path components relative to the package
            (typically just ``"scaffolds"``).

    Returns:
        Path to the scaffolds directory.

    Raises:
        FileNotFoundError: If the scaffolds directory cannot be found.
    """
    return resolve_package_path(domain_package, *subpath)
