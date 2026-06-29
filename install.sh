#!/usr/bin/env bash
# Deliberator installer — installs the deliberator CLI globally.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Build-Fractal/deliberator/main/install.sh | bash
#
# Or with options:
#   curl -fsSL ... | bash -s -- --method pipx
#   curl -fsSL ... | bash -s -- --method pip --extras all
#   curl -fsSL ... | bash -s -- --from-source
#
# Requires Python 3.12+ and one of: pipx, pip, or uv.

set -euo pipefail

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

REPO="Build-Fractal/deliberator"
PACKAGE="deliberator"
MIN_PYTHON_VERSION="3.12"
METHOD=""          # auto-detect if empty
EXTRAS=""          # optional extras: "all", "nashopt", "solvers"
FROM_SOURCE=false
LOCAL_PATH=""      # install from local directory
BRANCH="main"

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}▸${NC} $*"; }
ok()    { echo -e "${GREEN}✓${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC} $*"; }
fail()  { echo -e "${RED}✗${NC} $*"; exit 1; }

# ---------------------------------------------------------------------------
# Parse args
# ---------------------------------------------------------------------------

while [[ $# -gt 0 ]]; do
    case "$1" in
        --method)   METHOD="$2"; shift 2 ;;
        --extras)   EXTRAS="$2"; shift 2 ;;
        --from-source) FROM_SOURCE=true; shift ;;
        --local)    LOCAL_PATH="$2"; shift 2 ;;
        --branch)   BRANCH="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: install.sh [--method pipx|pip|uv] [--extras all] [--from-source] [--local /path] [--branch main]"
            exit 0
            ;;
        *) fail "Unknown option: $1" ;;
    esac
done

# ---------------------------------------------------------------------------
# Check Python version
# ---------------------------------------------------------------------------

info "Checking Python version..."

PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
        major=$(echo "$ver" | cut -d. -f1)
        minor=$(echo "$ver" | cut -d. -f2)
        if [[ "$major" -ge 3 && "$minor" -ge 12 ]]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [[ -z "$PYTHON" ]]; then
    fail "Python ${MIN_PYTHON_VERSION}+ is required but not found. Install it first:
  brew install python@3.12   # macOS
  sudo apt install python3.12  # Ubuntu/Debian"
fi

ok "Python $("$PYTHON" --version 2>&1 | awk '{print $2}')"

# ---------------------------------------------------------------------------
# Detect install method
# ---------------------------------------------------------------------------

if [[ -z "$METHOD" ]]; then
    if command -v pipx &>/dev/null; then
        METHOD="pipx"
    elif command -v uv &>/dev/null; then
        METHOD="uv"
    elif command -v pip3 &>/dev/null; then
        METHOD="pip"
    elif command -v pip &>/dev/null; then
        METHOD="pip"
    else
        fail "No package installer found. Install one of: pipx, uv, or pip.
  brew install pipx && pipx ensurepath   # recommended
  curl -LsSf https://astral.sh/uv/install.sh | sh   # fast alternative"
    fi
fi

info "Install method: ${CYAN}${METHOD}${NC}"

# ---------------------------------------------------------------------------
# Build install target
# ---------------------------------------------------------------------------

if [[ -n "$LOCAL_PATH" ]]; then
    # Resolve to absolute path
    LOCAL_PATH="$(cd "$LOCAL_PATH" && pwd)"
    TARGET="$LOCAL_PATH"
    info "Installing from local path: ${CYAN}${LOCAL_PATH}${NC}"
elif $FROM_SOURCE; then
    # Use SSH if available (private repos), fall back to HTTPS
    if [[ -n "${GIT_SSH_KEY:-}" ]] || ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        TARGET="git+ssh://git@github.com/${REPO}.git@${BRANCH}"
        info "Installing from source via SSH (${BRANCH})..."
    else
        TARGET="git+https://github.com/${REPO}.git@${BRANCH}"
        info "Installing from source via HTTPS (${BRANCH})..."
    fi
else
    TARGET="${PACKAGE}"
    if [[ -n "$EXTRAS" ]]; then
        TARGET="${PACKAGE}[${EXTRAS}]"
    fi
    info "Installing ${CYAN}${TARGET}${NC}..."
fi

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------

case "$METHOD" in
    pipx)
        if $FROM_SOURCE; then
            pipx install "git+https://github.com/${REPO}.git@${BRANCH}"
        else
            pipx install "$TARGET"
        fi
        ;;
    uv)
        if $FROM_SOURCE; then
            uv tool install "git+https://github.com/${REPO}.git@${BRANCH}"
        else
            uv tool install "$TARGET"
        fi
        ;;
    pip)
        PIP_CMD="pip3"
        command -v pip3 &>/dev/null || PIP_CMD="pip"
        if $FROM_SOURCE; then
            "$PIP_CMD" install "git+https://github.com/${REPO}.git@${BRANCH}"
        else
            "$PIP_CMD" install "$TARGET"
        fi
        ;;
    *)
        fail "Unknown method: $METHOD. Use pipx, uv, or pip."
        ;;
esac

# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------

echo ""
if command -v deliberator &>/dev/null; then
    ok "deliberator installed successfully!"
    echo ""
    deliberator --help | head -5
    echo ""
    info "Get started:"
    echo "  deliberator init                          # set up a project"
    echo "  deliberator decide \"question\" --provider anthropic  # quick deliberation"
    echo "  deliberator run config.yml --provider claude-code    # full pipeline"
else
    warn "deliberator was installed but is not in PATH."
    echo "  If using pipx, run: pipx ensurepath"
    echo "  If using pip, ensure ~/.local/bin is in PATH"
fi
