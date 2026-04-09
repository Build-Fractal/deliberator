#!/usr/bin/env bash
# Build conversus.mcpb — a Claude Desktop Extension bundle.
# .mcpb files are ZIP archives containing manifest.json (and any bundled assets).
# For conversus, the server is the system `conversus` CLI — no files to bundle.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
OUT="$REPO_ROOT/conversus.mcpb"

echo "Building $OUT ..."

# Create the zip from the desktop-extension directory contents (not the dir itself).
cd "$SCRIPT_DIR"
zip -r "$OUT" manifest.json

echo "Done: $OUT"
echo ""
echo "Install: double-click conversus.mcpb, or drag it into Claude Desktop → Settings → Extensions."
