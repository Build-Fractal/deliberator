#!/usr/bin/env bash
# Fetch lattice-graph's release wheels into .wheels/ in this checkout, and optionally install it.
#
# lattice-graph powers structured review, trials and the gate's graph. It is not on PyPI and
# Deliberator does not declare it as a dependency: it comes from Lattice's release wheels
# (Build-Fractal/lattice-releases, one folder per release, with SHA256SUMS; private) and is
# installed separately. It is PolyForm Noncommercial 1.0.0. Without it, the rest of
# Deliberator works and the graph features say how to install it.
#
#   scripts/lattice-wheel.sh            # copy into .wheels/, downloading if missing
#   scripts/lattice-wheel.sh --download # download the release again (needs `gh` access)
#   scripts/lattice-wheel.sh --install  # and install it into ./.venv (or $VIRTUAL_ENV)
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

if [[ "${1:-}" == "--install" ]]; then
    py="${VIRTUAL_ENV:-$ROOT/.venv}/bin/python"
    # Install this platform's wheel by file, so lattice-graph never comes from an index.
    case "$(uname -s)-$(uname -m)" in
        Darwin-arm64) tag="macosx_11_0_arm64" ;;
        Linux-x86_64) tag="manylinux_2_36_x86_64" ;;
        Linux-aarch64) tag="manylinux_2_36_aarch64" ;;
        *) echo "No lattice-graph wheel for $(uname -s)-$(uname -m)." >&2; exit 1 ;;
    esac
    uv pip install --python "$py" "$ROOT/.wheels/lattice_graph-${VERSION}-cp312-cp312-${tag}.whl"
fi
