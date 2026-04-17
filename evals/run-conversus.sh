#!/usr/bin/env bash
# Wrapper script for promptfoo exec: provider.
# Avoids shell quoting issues with inline {{prompt}} expansion.
#
# Usage: ./evals/run-conversus.sh <mode> <question>
# Returns JSON on stdout, logs on stderr.

set -euo pipefail

MODE="${1:?Usage: run-conversus.sh <mode> <question>}"
QUESTION="${2:?Usage: run-conversus.sh <mode> <question>}"

cd "$(dirname "$0")/.."

exec uv run conversus decide "$QUESTION" \
    --provider mock \
    --mode "$MODE" \
    --format json \
    2>/dev/null
