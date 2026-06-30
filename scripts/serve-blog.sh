#!/usr/bin/env bash
# serve-blog.sh — Build and serve the deliberator docs site (includes blog)
#
# The blog is powered by mkdocs-material's blog plugin. Posts live in
# docs/blog/posts/ as standard markdown with YAML frontmatter. The plugin
# handles index generation, category pages, archive, and RSS feed.
#
# Usage:
#   ./scripts/serve-blog.sh          # serve on default port 8800
#   ./scripts/serve-blog.sh 9000     # serve on custom port
#   ./scripts/serve-blog.sh --build  # build only (no serve)
#
# Prerequisites:
#   uv sync   (installs mkdocs-material, mkdocstrings, etc.)

set -euo pipefail

PORT="${1:-8800}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Validate blog structure
if [ ! -d "docs/blog/posts" ]; then
    echo "Error: docs/blog/posts/ directory not found."
    echo "Create it and add .md posts with frontmatter."
    exit 1
fi

if [ ! -f "docs/blog/.authors.yml" ]; then
    echo "Error: docs/blog/.authors.yml not found."
    echo "The blog plugin requires an authors file."
    exit 1
fi

POST_COUNT=$(ls docs/blog/posts/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "Found $POST_COUNT blog post(s) in docs/blog/posts/"

# Build-only mode
if [ "$PORT" = "--build" ]; then
    echo "Building docs site..."
    uv run mkdocs build 2>&1 | grep -E '(ERROR|WARNING|built in)'
    echo ""
    echo "Blog output: site/blog/"
    echo "Posts:"
    ls -1 docs/blog/posts/*.md | while read f; do
        title=$(grep '^title:' "$f" | head -1 | sed 's/title: *"\{0,1\}//' | sed 's/"\{0,1\} *$//')
        echo "  - $title"
    done
    exit 0
fi

# Serve mode
echo "Starting docs server on http://127.0.0.1:$PORT/deliberator/blog/"
echo "Press Ctrl+C to stop."
echo ""
uv run mkdocs serve --dev-addr "127.0.0.1:$PORT"
