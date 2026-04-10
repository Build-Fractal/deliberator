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
