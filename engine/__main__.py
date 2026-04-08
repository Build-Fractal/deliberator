"""CLI entry point for ``python -m engine``.

Delegates to the Click CLI defined in :mod:`engine.cli`.
"""

from engine.cli import cli

if __name__ == "__main__":
    cli()
