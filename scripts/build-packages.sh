#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# hatch does not support an external config file override.
# Strategy: temporarily swap pyproject.toml for each package config,
# build, then restore the original.

ORIGINAL="pyproject.toml"
BACKUP=".pyproject.toml.bak"

cleanup() {
    if [ -f "$BACKUP" ]; then
        mv "$BACKUP" "$ORIGINAL"
    fi
}
trap cleanup EXIT

echo "Building deliberator packages..."

cp "$ORIGINAL" "$BACKUP"

for config in packages/*.toml; do
    name=$(basename "$config" .toml)
    echo "  Building $name..."
    cp "$config" "$ORIGINAL"
    hatch build -t wheel 2>&1 | tail -1
done

# Restore original
mv "$BACKUP" "$ORIGINAL"
trap - EXIT

echo ""
echo "Wheels built:"
ls -la dist/*.whl 2>/dev/null || echo "  (check dist/ directory)"
