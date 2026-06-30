#!/usr/bin/env python3
"""
Deliberator MCP Server — Claude Desktop Extension entry point.

This is the bundled entry point launched by Claude Desktop when the .mcpb
extension is installed. It:

  1. Prepends the bundled `lib/` directory to sys.path so deliberator and
     all its transitive dependencies resolve from the bundle (no system
     `pip install deliberator` required).
  2. Imports the sibling `mcp_server.py` module and runs its FastMCP
     instance via stdio transport.

Claude Desktop also sets PYTHONPATH via the manifest; we prepend explicitly
here as a belt-and-suspenders fallback.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _bootstrap_sys_path() -> None:
    """Prepend bundled lib/ to sys.path so deliberator + deps resolve."""
    here = Path(__file__).resolve().parent
    bundled_lib = here / "lib"
    if bundled_lib.is_dir():
        lib_str = str(bundled_lib)
        if lib_str not in sys.path:
            sys.path.insert(0, lib_str)


def _load_mcp_server():
    """Load the sibling mcp_server.py module."""
    here = Path(__file__).resolve().parent
    server_path = here / "mcp_server.py"
    if not server_path.exists():
        sys.stderr.write(
            f"Fatal: mcp_server.py not found next to main.py at {server_path}\n"
        )
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("deliberator_mcp_server", server_path)
    if spec is None or spec.loader is None:
        sys.stderr.write("Fatal: could not create module spec for mcp_server.py\n")
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    _bootstrap_sys_path()

    # Set CWD to the server/ directory AND DELIBERATOR_ROOT env var
    # so the engine's find_project_root and find_project_root() in
    # linter/validate.py find the bundled presets/, schema/, and
    # templates/ directories. Without this, CWD is wherever Claude
    # Desktop launched us (typically ~ or the bundle install dir).
    import os
    here = Path(__file__).resolve().parent
    os.chdir(here)
    os.environ["DELIBERATOR_ROOT"] = str(here)

    mcp_module = _load_mcp_server()
    mcp_module.mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
