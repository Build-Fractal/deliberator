#!/usr/bin/env bash
# Put the lattice-graph wheels where pyproject.toml expects them: .wheels/ in this checkout.
#
# lattice-graph is not on PyPI. The `graph` extra installs it from Lattice's release wheels
# (Build-Fractal/lattice-releases, one folder per release, with SHA256SUMS), found through
# [tool.uv] find-links = [".wheels"]. .wheels/ is git-ignored: the wheels are not published
# with this repo. lattice-graph is PolyForm Noncommercial 1.0.0.
#
#   scripts/lattice-wheel.sh            # copy from $LATTICE_WHEELS, downloading if missing
#   scripts/lattice-wheel.sh --download # download the release again (needs `gh` access)
#
# LATTICE_WHEELS defaults to ~/code/build-fractal-mono/wheels/lattice-graph.
# The wheels are compiled for CPython 3.12 (macOS arm64, manylinux_2_36 x86_64/aarch64).

set -euo pipefail

RELEASE="2026-11-10"
VERSION="0.2.1"
REPO="Build-Fractal/lattice-releases"
STORE="${LATTICE_WHEELS:-$HOME/code/build-fractal-mono/wheels/lattice-graph}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PATTERN="lattice_graph-${VERSION}-*.whl"

download() {
    mkdir -p "$STORE"
    local names
    names=$(gh api "repos/$REPO/contents/$RELEASE" -q '.[].name' | grep -E "^(SHA256SUMS|lattice_graph-${VERSION}-.*\.whl)$")
    for f in $names; do
        gh api -H 'Accept: application/vnd.github.raw' "repos/$REPO/contents/$RELEASE/$f" > "$STORE/$f"
    done
}

shopt -s nullglob
wheels=("$STORE"/$PATTERN)
if [[ "${1:-}" == "--download" || ${#wheels[@]} -eq 0 ]]; then
    download
    wheels=("$STORE"/$PATTERN)
fi
(cd "$STORE" && grep "lattice_graph-${VERSION}-" SHA256SUMS | shasum -a 256 -c --quiet)

mkdir -p "$ROOT/.wheels"
rm -f "$ROOT"/.wheels/lattice_graph-*.whl
cp "${wheels[@]}" "$ROOT/.wheels/"
ls "$ROOT/.wheels"
