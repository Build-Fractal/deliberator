#!/usr/bin/env bash
# Build conversus.mcpb — a self-contained Claude Desktop Extension bundle.
#
# Bundles:
#   - manifest.json (MCPB v0.3 manifest)
#   - server/main.py (entry point that bootstraps sys.path)
#   - server/mcp_server.py (FastMCP server with 3 tools)
#   - server/lib/ (conversus + all Python dependencies, ~90MB)
#
# The result is a self-contained .mcpb that does NOT require `pip install
# conversus` on the recipient's machine. Claude Desktop's bundled Python
# runs server/main.py directly.
#
# Platform: this build bundles darwin-arm64 native wheels (pydantic-core,
# _cffi_backend, etc). For Windows/Linux, rebuild on the target platform or
# use pip --platform to cross-build.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
OUT="$REPO_ROOT/conversus.mcpb"

echo "Building $OUT ..."

if [[ ! -d "$SCRIPT_DIR/server/lib" ]]; then
  echo "Error: server/lib/ not found. Run this first:"
  echo "  pip install --target desktop-extension/server/lib --upgrade . 'mcp[cli]>=1.0.0'"
  exit 1
fi

# Sync manifest.json version + tools[] from registry — single source of truth.
# Mirrors the .github/workflows/release-mcpb.yml step so local and CI builds
# always emit a manifest synced with pyproject + CAPABILITIES.
#
# Constitution Principle XXII (Distribution Surface Integrity, v2.3.0):
# version single-sourced from pyproject.toml; tools[] single-sourced from
# the capability registry. Hand-editing either field is prohibited.
python3 - "$REPO_ROOT" "$SCRIPT_DIR/manifest.json" <<'PY'
import json
import sys
import tomllib
from pathlib import Path

repo_root = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])

# Repo root has capabilities.py + conversus/ — add to sys.path so we can
# import without requiring a dev install.
sys.path.insert(0, str(repo_root.resolve()))

from capabilities import CAPABILITIES
from conversus.registry.projector import project_to_mcpb_manifest_tools

pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text())
version = pyproject["project"]["version"]
projected_tools = [dict(e) for e in project_to_mcpb_manifest_tools(CAPABILITIES)]

manifest = json.loads(manifest_path.read_text())
changed = False
if manifest.get("version") != version:
    manifest["version"] = version
    changed = True
if manifest.get("tools") != projected_tools:
    manifest["tools"] = projected_tools
    changed = True

if changed:
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"manifest.json synced — version={version}, tools={len(projected_tools)}")
else:
    print(f"manifest.json already in sync — version={version}, tools={len(projected_tools)}")
PY

# Zip from the desktop-extension directory so paths inside the archive are
# manifest.json, server/main.py, server/mcp_server.py, server/lib/...
cd "$SCRIPT_DIR"
rm -f "$OUT"
zip -r -q "$OUT" manifest.json server -x 'server/__pycache__/*' -x 'server/lib/**/__pycache__/*' -x 'server/lib/**/*.pyc'

SIZE_HUMAN="$(du -h "$OUT" | cut -f1)"
echo "Done: $OUT ($SIZE_HUMAN)"
echo ""
echo "Install: double-click conversus.mcpb, or drag it into"
echo "         Claude Desktop → Settings → Extensions → Install from file."
