#!/usr/bin/env bash
# Put the lattice-graph wheel where pyproject.toml expects it: .wheels/ in this checkout.
#
# lattice-graph is not on PyPI yet, so the `graph` extra installs a locally built wheel
# ([tool.uv.sources] in pyproject.toml). .wheels/ is git-ignored: the wheel is not published
# with this repo.
#
#   scripts/lattice-wheel.sh                    # copy from $LATTICE_WHEELS
#   scripts/lattice-wheel.sh --build <lattice>  # build it from a Lattice checkout first
#
# LATTICE_WHEELS defaults to ~/code/build-fractal-mono/wheels/lattice-graph.
# Remove this script and the [tool.uv.sources] entry once lattice-graph is on PyPI.

set -euo pipefail

WHEEL="lattice_graph-0.2.0-py3-none-any.whl"
STORE="${LATTICE_WHEELS:-$HOME/code/build-fractal-mono/wheels/lattice-graph}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ "${1:-}" == "--build" ]]; then
    src="${2:?usage: lattice-wheel.sh --build <path to a Lattice checkout>}"
    mkdir -p "$STORE"
    uv="$src/.tools/uv/uv"  # Lattice's own pinned uv, if it has one
    [[ -x "$uv" ]] || uv="uv"
    (cd "$src" && "$uv" build --package lattice-graph --wheel --out-dir "$STORE")
fi

if [[ ! -f "$STORE/$WHEEL" ]]; then
    echo "No $WHEEL in $STORE." >&2
    echo "Build it: scripts/lattice-wheel.sh --build <path to a Lattice checkout at lattice-graph 0.2>" >&2
    exit 1
fi

mkdir -p "$ROOT/.wheels"
cp "$STORE/$WHEEL" "$ROOT/.wheels/$WHEEL"
echo "$ROOT/.wheels/$WHEEL"
