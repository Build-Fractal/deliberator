#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# dev-setup.sh — Bootstrap a conversus development environment.
#
# Checks for required CLI tools and agent runtimes, installs missing ones
# (with user consent), and prints a summary table.
#
# Usage:
#   ./scripts/dev-setup.sh                  # install missing tools
#   ./scripts/dev-setup.sh --check-only     # just print status
#   ./scripts/dev-setup.sh --skip ollama,vllm  # skip specific tools
#
# Design:
#   - Idempotent and safe to re-run.
#   - Never fails on a single install error — reports and continues.
#   - Supports macOS (brew/npm) and Linux (apt/npm).
# ---------------------------------------------------------------------------

set -uo pipefail
# NOTE: we intentionally omit -e so individual install failures don't abort.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# ---------------------------------------------------------------------------
# Colors & output helpers
# ---------------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

ok()   { printf "${GREEN}  ✓${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}  ⚠${NC} %s\n" "$*"; }
fail() { printf "${RED}  ✗${NC} %s\n" "$*"; }
info() { printf "${CYAN}  ▸${NC} %s\n" "$*"; }

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

CHECK_ONLY=false
SKIP_LIST=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --check-only)
            CHECK_ONLY=true
            shift
            ;;
        --skip)
            SKIP_LIST="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: dev-setup.sh [--check-only] [--skip tool1,tool2]"
            echo ""
            echo "Options:"
            echo "  --check-only   Print status without installing anything"
            echo "  --skip LIST    Comma-separated list of tools to skip"
            echo ""
            echo "Tools: python, conversus, claude, aider, opencode, ollama,"
            echo "       codex, gemini, gh, llama-server, vllm"
            exit 0
            ;;
        *)
            echo "Unknown option: $1 (use --help for usage)"
            exit 1
            ;;
    esac
done

should_skip() {
    local tool="$1"
    echo ",$SKIP_LIST," | grep -qi ",$tool,"
}

# ---------------------------------------------------------------------------
# OS detection
# ---------------------------------------------------------------------------

OS="unknown"
if [[ "$(uname -s)" == "Darwin" ]]; then
    OS="macos"
elif [[ "$(uname -s)" == "Linux" ]]; then
    OS="linux"
fi

has_brew()  { command -v brew  &>/dev/null; }
has_npm()   { command -v npm   &>/dev/null; }
has_pip()   { command -v pip3  &>/dev/null || command -v pip &>/dev/null; }
has_apt()   { command -v apt-get &>/dev/null; }

pip_cmd() {
    if command -v pip3 &>/dev/null; then
        echo "pip3"
    else
        echo "pip"
    fi
}

# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------

# Parallel arrays for the summary table.
declare -a TOOL_NAMES=()
declare -a TOOL_STATUSES=()   # installed | skipped | failed | missing | info
declare -a TOOL_DETAILS=()

record() {
    TOOL_NAMES+=("$1")
    TOOL_STATUSES+=("$2")
    TOOL_DETAILS+=("$3")
}

# ---------------------------------------------------------------------------
# 1. Python 3.12+
# ---------------------------------------------------------------------------

check_python() {
    info "Checking Python 3.12+ ..."
    local py=""
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local ver
            ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
            local major minor
            major=$(echo "$ver" | cut -d. -f1)
            minor=$(echo "$ver" | cut -d. -f2)
            if [[ "$major" -ge 3 && "$minor" -ge 12 ]]; then
                py="$cmd"
                break
            fi
        fi
    done

    if [[ -n "$py" ]]; then
        local full_ver
        full_ver=$("$py" --version 2>&1 | awk '{print $2}')
        ok "Python $full_ver"
        record "python" "installed" "$full_ver"
        return 0
    fi

    if $CHECK_ONLY || should_skip "python"; then
        warn "Python 3.12+ not found"
        record "python" "missing" ">=3.12 required"
        return 1
    fi

    info "Attempting to install Python 3.12 ..."
    if [[ "$OS" == "macos" ]] && has_brew; then
        brew install python@3.12 && ok "Python installed" && record "python" "installed" "via brew" && return 0
    elif [[ "$OS" == "linux" ]] && has_apt; then
        sudo apt-get update -qq && sudo apt-get install -y -qq python3.12 python3.12-venv && \
            ok "Python installed" && record "python" "installed" "via apt" && return 0
    fi

    fail "Could not install Python 3.12+"
    record "python" "failed" "install manually: brew install python@3.12"
    return 1
}

# ---------------------------------------------------------------------------
# 2. conversus (local editable install)
# ---------------------------------------------------------------------------

check_conversus() {
    info "Checking conversus package ..."

    if should_skip "conversus"; then
        warn "Skipping conversus"
        record "conversus" "skipped" "--skip"
        return 0
    fi

    if command -v conversus &>/dev/null; then
        ok "conversus already installed"
        record "conversus" "installed" "$(command -v conversus)"
        return 0
    fi

    if $CHECK_ONLY; then
        warn "conversus not installed"
        record "conversus" "missing" "pip install -e ."
        return 1
    fi

    info "Installing conversus from local repo (editable) ..."
    local pip
    pip="$(pip_cmd)"
    if (cd "$PROJECT_ROOT" && "$pip" install -e . 2>&1); then
        ok "conversus installed"
        record "conversus" "installed" "editable from $PROJECT_ROOT"
        return 0
    fi

    fail "conversus install failed"
    record "conversus" "failed" "run: cd $PROJECT_ROOT && pip install -e ."
    return 1
}

# ---------------------------------------------------------------------------
# 3. External CLI agent runtimes
# ---------------------------------------------------------------------------

install_npm_tool() {
    local name="$1" bin="$2" pkg="$3"

    info "Checking $name ..."

    if should_skip "$name"; then
        warn "Skipping $name"
        record "$name" "skipped" "--skip"
        return 0
    fi

    if command -v "$bin" &>/dev/null; then
        ok "$name already installed"
        record "$name" "installed" "$(command -v "$bin")"
        return 0
    fi

    if $CHECK_ONLY; then
        warn "$name not found"
        record "$name" "missing" "npm install -g $pkg"
        return 1
    fi

    if ! has_npm; then
        fail "$name requires npm (not found)"
        record "$name" "failed" "install Node.js/npm first"
        return 1
    fi

    info "Installing $name ..."
    if npm install -g "$pkg" 2>&1; then
        ok "$name installed"
        record "$name" "installed" "via npm"
        return 0
    fi

    fail "$name install failed"
    record "$name" "failed" "npm install -g $pkg"
    return 1
}

install_pip_tool() {
    local name="$1" bin="$2" pkg="$3"

    info "Checking $name ..."

    if should_skip "$name"; then
        warn "Skipping $name"
        record "$name" "skipped" "--skip"
        return 0
    fi

    if command -v "$bin" &>/dev/null; then
        ok "$name already installed"
        record "$name" "installed" "$(command -v "$bin")"
        return 0
    fi

    if $CHECK_ONLY; then
        warn "$name not found"
        record "$name" "missing" "pip install $pkg"
        return 1
    fi

    if ! has_pip; then
        fail "$name requires pip (not found)"
        record "$name" "failed" "install pip first"
        return 1
    fi

    info "Installing $name ..."
    local pip
    pip="$(pip_cmd)"
    if "$pip" install "$pkg" 2>&1; then
        ok "$name installed"
        record "$name" "installed" "via pip"
        return 0
    fi

    fail "$name install failed"
    record "$name" "failed" "$pip install $pkg"
    return 1
}

check_claude() {
    install_npm_tool "claude" "claude" "@anthropic-ai/claude-code"
}

check_aider() {
    install_pip_tool "aider" "aider" "aider-chat"
}

check_opencode() {
    local name="opencode"
    info "Checking $name ..."

    if should_skip "$name"; then
        warn "Skipping $name"
        record "$name" "skipped" "--skip"
        return 0
    fi

    if command -v opencode &>/dev/null; then
        ok "$name already installed"
        record "$name" "installed" "$(command -v opencode)"
        return 0
    fi

    if $CHECK_ONLY; then
        warn "$name not found"
        record "$name" "missing" "curl -fsSL https://opencode.ai/install | bash"
        return 1
    fi

    info "Installing $name ..."
    if curl -fsSL https://opencode.ai/install | bash 2>&1; then
        ok "$name installed"
        record "$name" "installed" "via curl installer"
        return 0
    fi

    fail "$name install failed"
    record "$name" "failed" "curl -fsSL https://opencode.ai/install | bash"
    return 1
}

check_ollama() {
    local name="ollama"
    info "Checking $name ..."

    if should_skip "$name"; then
        warn "Skipping $name"
        record "$name" "skipped" "--skip"
        return 0
    fi

    if command -v ollama &>/dev/null; then
        ok "$name already installed"
        record "$name" "installed" "$(command -v ollama)"
        return 0
    fi

    if $CHECK_ONLY; then
        warn "$name not found"
        record "$name" "missing" "brew install ollama (macOS)"
        return 1
    fi

    info "Installing $name ..."
    if [[ "$OS" == "macos" ]] && has_brew; then
        if brew install ollama 2>&1; then
            ok "$name installed"
            record "$name" "installed" "via brew"
            return 0
        fi
    elif [[ "$OS" == "linux" ]]; then
        if curl -fsSL https://ollama.com/install.sh | sh 2>&1; then
            ok "$name installed"
            record "$name" "installed" "via curl installer"
            return 0
        fi
    fi

    fail "$name install failed"
    record "$name" "failed" "see https://ollama.com/download"
    return 1
}

check_codex() {
    install_npm_tool "codex" "codex" "@openai/codex"
}

check_gemini() {
    install_npm_tool "gemini" "gemini" "@google/gemini-cli"
}

check_gh() {
    local name="gh"
    info "Checking GitHub CLI ..."

    if should_skip "$name"; then
        warn "Skipping $name"
        record "$name" "skipped" "--skip"
        return 0
    fi

    if command -v gh &>/dev/null; then
        ok "gh already installed"

        # Check for copilot extension
        if gh extension list 2>/dev/null | grep -q "gh-copilot"; then
            record "$name" "installed" "$(command -v gh) + copilot"
        else
            if ! $CHECK_ONLY; then
                info "Installing gh-copilot extension ..."
                gh extension install github/gh-copilot 2>&1 || true
            fi
            if gh extension list 2>/dev/null | grep -q "gh-copilot"; then
                record "$name" "installed" "$(command -v gh) + copilot"
            else
                record "$name" "installed" "$(command -v gh) (copilot ext missing)"
            fi
        fi
        return 0
    fi

    if $CHECK_ONLY; then
        warn "$name not found"
        record "$name" "missing" "brew install gh"
        return 1
    fi

    info "Installing $name ..."
    local gh_ok=false
    if [[ "$OS" == "macos" ]] && has_brew; then
        brew install gh 2>&1 && gh_ok=true
    elif [[ "$OS" == "linux" ]] && has_apt; then
        # Official GH CLI install for Debian/Ubuntu
        (type -p wget >/dev/null || sudo apt-get install wget -y) && \
        sudo mkdir -p -m 755 /etc/apt/keyrings && \
        wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
        sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg && \
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
        sudo apt-get update -qq && sudo apt-get install gh -y -qq && gh_ok=true
    fi

    if $gh_ok; then
        ok "$name installed"
        info "Installing gh-copilot extension ..."
        gh extension install github/gh-copilot 2>&1 || true
        record "$name" "installed" "via package manager"
        return 0
    fi

    fail "$name install failed"
    record "$name" "failed" "see https://cli.github.com"
    return 1
}

# ---------------------------------------------------------------------------
# 4. Local inference servers
# ---------------------------------------------------------------------------

check_llama_server() {
    local name="llama-server"
    info "Checking $name ..."

    if should_skip "$name"; then
        warn "Skipping $name"
        record "$name" "skipped" "--skip"
        return 0
    fi

    if command -v llama-server &>/dev/null; then
        ok "$name already installed"
        record "$name" "installed" "$(command -v llama-server)"
        return 0
    fi

    if $CHECK_ONLY; then
        warn "$name not found"
        record "$name" "missing" "brew install llama.cpp"
        return 1
    fi

    info "Installing llama.cpp ..."
    if [[ "$OS" == "macos" ]] && has_brew; then
        if brew install llama.cpp 2>&1; then
            ok "$name installed"
            record "$name" "installed" "via brew"
            return 0
        fi
    elif [[ "$OS" == "linux" ]] && has_brew; then
        if brew install llama.cpp 2>&1; then
            ok "$name installed"
            record "$name" "installed" "via brew"
            return 0
        fi
    fi

    fail "$name install failed"
    record "$name" "failed" "brew install llama.cpp"
    return 1
}

check_vllm() {
    local name="vllm"
    info "Checking $name ..."

    if should_skip "$name"; then
        warn "Skipping $name"
        record "$name" "skipped" "--skip"
        return 0
    fi

    # vLLM is GPU-only; we just report status, never auto-install.
    if command -v vllm &>/dev/null; then
        ok "$name already installed"
        record "$name" "installed" "$(command -v vllm)"
    else
        record "$name" "info" "GPU-only — pip install vllm (requires CUDA)"
        printf "${DIM}  ℹ${NC} vLLM is GPU-only and cannot be auto-installed.\n"
        printf "${DIM}    Install manually: pip install vllm (requires NVIDIA GPU + CUDA)${NC}\n"
    fi
}

# ---------------------------------------------------------------------------
# 5. Summary table
# ---------------------------------------------------------------------------

print_summary() {
    echo ""
    printf "${BOLD}${CYAN}%-20s %-12s %s${NC}\n" "Tool" "Status" "Details"
    printf "%-20s %-12s %s\n"   "--------------------" "------------" "-------------------------------"

    for i in "${!TOOL_NAMES[@]}"; do
        local name="${TOOL_NAMES[$i]}"
        local status="${TOOL_STATUSES[$i]}"
        local detail="${TOOL_DETAILS[$i]}"

        local color="$NC"
        local symbol=""
        case "$status" in
            installed) color="$GREEN";  symbol="✓" ;;
            skipped)   color="$YELLOW"; symbol="⚠" ;;
            missing)   color="$YELLOW"; symbol="–" ;;
            failed)    color="$RED";    symbol="✗" ;;
            info)      color="$DIM";    symbol="ℹ" ;;
        esac

        printf "${color} %s %-18s %-12s${NC} %s\n" "$symbol" "$name" "$status" "$detail"
    done

    echo ""

    # Count statuses
    local installed=0 missing=0 failed=0 skipped=0
    for s in "${TOOL_STATUSES[@]}"; do
        case "$s" in
            installed) installed=$((installed + 1)) ;;
            missing)   missing=$((missing + 1))     ;;
            failed)    failed=$((failed + 1))       ;;
            skipped)   skipped=$((skipped + 1))     ;;
        esac
    done

    local total=${#TOOL_NAMES[@]}
    printf "${BOLD}Summary:${NC} %s/%s installed" "$installed" "$total"
    [[ $skipped -gt 0 ]] && printf ", %s skipped" "$skipped"
    [[ $missing -gt 0 ]] && printf ", ${YELLOW}%s missing${NC}" "$missing"
    [[ $failed  -gt 0 ]] && printf ", ${RED}%s failed${NC}" "$failed"
    echo ""
    echo ""
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    echo ""
    printf "${BOLD}${CYAN}conversus dev-setup${NC}"
    if $CHECK_ONLY; then
        printf " ${DIM}(check-only mode)${NC}"
    fi
    echo ""
    echo ""

    check_python
    check_conversus

    # Agent runtimes
    check_claude
    check_aider
    check_opencode
    check_ollama
    check_codex
    check_gemini
    check_gh

    # Local inference
    check_llama_server
    check_vllm

    print_summary
}

main
