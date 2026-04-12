#!/usr/bin/env python3
"""Regenerate all 4 distribution surfaces from the capability registry.

Reads the root-level ``capabilities.py`` (Day 5 creates it), walks the
resulting ``REGISTRY``, and writes:

- ``engine/cli/__init__.py`` — full rewrite
- ``mcp_server.py`` — full rewrite
- ``claude-code-plugin/skills/<name>/SKILL.md`` — one file per capability
- ``desktop-extension/manifest.json`` — patches only the ``tools`` array;
  every other manifest field is preserved.

Usage::

    python scripts/build-surfaces.py             # Real write (Day 5+)
    python scripts/build-surfaces.py --dry-run   # Print what would change
    python scripts/build-surfaces.py --output-dir /tmp/surfaces
                                                 # Sandbox test (Day 3-4)

Spec: ``specs/055-capability-registry.md``, section 3.4.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap — make ``capabilities`` + ``conversus.registry`` importable
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from conversus.registry import Capability  # noqa: E402
from conversus.registry.projector import (  # noqa: E402
    project_to_cli,
    project_to_mcp,
    project_to_mcpb_manifest_tools,
    project_to_plugin_skills,
)


# ---------------------------------------------------------------------------
# Paths the projector writes to (relative to REPO_ROOT)
# ---------------------------------------------------------------------------

CLI_PATH = Path("engine/cli/__init__.py")
MCP_PATH = Path("mcp_server.py")
PLUGIN_SKILLS_DIR = Path("claude-code-plugin/skills")
MCPB_MANIFEST = Path("desktop-extension/manifest.json")


def load_capabilities() -> list[Capability]:
    """Import the root ``capabilities.py`` and return its ``CAPABILITIES`` list.

    ``capabilities.py`` at the repo root is expected to define a
    module-level ``CAPABILITIES: list[Capability] = [...]`` — the one
    authoritative list of capabilities the projector walks. There is no
    module-level registry populated by decorator side effects
    (constitution principle IX).

    On Day 3-4 this file doesn't exist yet. We tolerate that by
    returning an empty list and emitting a warning, letting the
    projector run against an empty registry so the validation test can
    still exercise the wiring.
    """
    try:
        import capabilities as _caps_module  # noqa: F401
    except ModuleNotFoundError:
        print(
            "warning: capabilities.py not found at repo root — projecting an "
            "empty list. This is expected before Day 5 of spec 055.",
            file=sys.stderr,
        )
        return []

    caps = getattr(_caps_module, "CAPABILITIES", None)
    if caps is None:
        print(
            "warning: capabilities.py has no CAPABILITIES list — projecting "
            "an empty list.",
            file=sys.stderr,
        )
        return []
    return list(caps)


def write_cli(caps: list[Capability], output_dir: Path, *, dry_run: bool) -> None:
    source = project_to_cli(caps)
    target = output_dir / CLI_PATH
    _write(target, source, dry_run=dry_run, label="CLI")


def write_mcp(caps: list[Capability], output_dir: Path, *, dry_run: bool) -> None:
    source = project_to_mcp(caps)
    target = output_dir / MCP_PATH
    _write(target, source, dry_run=dry_run, label="MCP")


def write_plugin_skills(
    caps: list[Capability], output_dir: Path, *, dry_run: bool
) -> None:
    skills = project_to_plugin_skills(caps)
    skills_dir = output_dir / PLUGIN_SKILLS_DIR
    for name, content in skills.items():
        target = skills_dir / name / "SKILL.md"
        _write(target, content, dry_run=dry_run, label=f"plugin[{name}]")


def patch_mcpb_manifest(
    caps: list[Capability], output_dir: Path, *, dry_run: bool
) -> None:
    """Patch only the ``tools[]`` field of the MCPB manifest.

    Reads the existing manifest, replaces ``tools``, writes it back.
    Other fields (``display_name``, ``long_description``, ``server``,
    ``user_config``...) are preserved — the spec's file-affected list
    explicitly says only tools[] is regenerated.
    """
    tools = project_to_mcpb_manifest_tools(caps)
    target = output_dir / MCPB_MANIFEST
    if not target.exists():
        print(
            f"warning: {target} missing; skipping (run from repo root).",
            file=sys.stderr,
        )
        return

    manifest = json.loads(target.read_text())
    manifest["tools"] = tools
    new_text = json.dumps(manifest, indent=2) + "\n"
    _write(target, new_text, dry_run=dry_run, label="MCPB manifest")


def _write(target: Path, content: str, *, dry_run: bool, label: str) -> None:
    if dry_run:
        print(f"[dry-run] would write {label}: {target} ({len(content)} bytes)")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print(f"wrote {label}: {target} ({len(content)} bytes)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate conversus surface files from the capability registry."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing any files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT,
        help="Destination root (default: repo root). Use a tmp path to sandbox.",
    )
    args = parser.parse_args(argv)

    caps = load_capabilities()

    write_cli(caps, args.output_dir, dry_run=args.dry_run)
    write_mcp(caps, args.output_dir, dry_run=args.dry_run)
    write_plugin_skills(caps, args.output_dir, dry_run=args.dry_run)
    patch_mcpb_manifest(caps, args.output_dir, dry_run=args.dry_run)

    print(f"done — {len(caps)} capability(ies) projected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
