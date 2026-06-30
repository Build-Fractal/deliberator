#!/usr/bin/env bash
#
# run-v4.1.0-deliberation.sh — orchestrated runner for the v4.1.0 originating
# deliberation. Handles pre-flight checks, the actual deliberator run invocation,
# and post-flight commit + push of the outputs.
#
# Run this in a FRESH terminal (not via Claude Code's `!command` prefix —
# interactive prompts get EOF when stdin isn't a real tty). See README in this
# script's repository for the OAuth-helper workaround if needed.
#
# Usage:
#   ./scripts/run-v4.1.0-deliberation.sh                    # interactive (default)
#   ./scripts/run-v4.1.0-deliberation.sh --auto-commit      # commit + push without prompting
#   ./scripts/run-v4.1.0-deliberation.sh --skip-commit      # just run; you commit manually after

set -euo pipefail

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
SPEC_BRANCH="spec/v4.2.0-structured-deliberation-outputs"
DELIB_DIR="deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-rerun-2026-05-13"
CONFIG_PATH="${DELIB_DIR}/deliberator.yml"
PROVIDER="claude-code"
EXPECTED_LAUNCHES=42

# Colors (optional, no-op if not a tty)
if [[ -t 1 ]]; then
    BOLD=$(tput bold); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); RED=$(tput setaf 1); CYAN=$(tput setaf 6); RESET=$(tput sgr0)
else
    BOLD=""; GREEN=""; YELLOW=""; RED=""; CYAN=""; RESET=""
fi

say()  { echo "${CYAN}→${RESET} $*"; }
ok()   { echo "${GREEN}✓${RESET} $*"; }
warn() { echo "${YELLOW}⚠${RESET} $*"; }
fail() { echo "${RED}✗${RESET} $*" >&2; exit 1; }
hdr()  { echo; echo "${BOLD}${CYAN}=== $* ===${RESET}"; }

# --------------------------------------------------------------------------
# Argument parsing
# --------------------------------------------------------------------------
MODE="interactive"
for arg in "$@"; do
    case "$arg" in
        --auto-commit) MODE="auto-commit" ;;
        --skip-commit) MODE="skip-commit" ;;
        -h|--help)
            grep -E "^#" "$0" | head -30 | sed 's/^# \?//'
            exit 0 ;;
        *) fail "Unknown argument: $arg (use --help)" ;;
    esac
done

# --------------------------------------------------------------------------
# Pre-flight checks
# --------------------------------------------------------------------------
hdr "Pre-flight"

# We expect to be inside deliberator
if [[ ! -d "engine" || ! -d "linter" || ! -f "pyproject.toml" ]]; then
    fail "Not inside deliberator. cd to build-fractal/deliberator/deliberator/ first."
fi
ok "Inside deliberator ($(pwd))"

# Branch check
current_branch=$(git branch --show-current)
if [[ "$current_branch" != "$SPEC_BRANCH" ]]; then
    warn "Current branch: $current_branch (expected: $SPEC_BRANCH)"
    read -r -p "Switch to $SPEC_BRANCH? [y/N] " ans
    if [[ "$ans" =~ ^[Yy]$ ]]; then
        git fetch origin "$SPEC_BRANCH"
        git checkout "$SPEC_BRANCH"
        git -c submodule.recurse=false reset --hard "origin/$SPEC_BRANCH"
    else
        fail "Abort: not on spec branch."
    fi
fi
ok "On branch $SPEC_BRANCH"

# Config file exists
if [[ ! -f "$CONFIG_PATH" ]]; then
    fail "Deliberation config missing: $CONFIG_PATH"
fi
ok "Config present: $CONFIG_PATH"

# Deliberator CLI available
if ! command -v deliberator &>/dev/null; then
    fail "deliberator CLI not on PATH. Install or activate the venv first."
fi
ok "deliberator CLI: $(which deliberator)"

# Validate config
say "Validating config..."
if ! deliberator validate "$CONFIG_PATH" >/dev/null 2>&1; then
    warn "Validation reports issues; showing details:"
    deliberator validate "$CONFIG_PATH" || true
    read -r -p "Continue anyway? [y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || fail "Abort: config validation failed."
fi
ok "Config validated"

# Provider auth check
say "Checking $PROVIDER auth..."
auth_status=$(deliberator status 2>&1 | grep -A 1 "anthropic" | grep "logged in" || true)
if [[ -z "$auth_status" ]]; then
    warn "$PROVIDER does not show as logged in."
    cat <<EOF

If you need to refresh OAuth:
  1. Run: deliberator login anthropic
  2. Open the printed URL in your browser
  3. Complete OAuth, paste code at the prompt

(Make sure you run this in a REAL terminal, not via Claude Code's ! prefix —
the prompt gets EOF on non-tty stdin and aborts before you can paste.)

EOF
    fail "Abort: $PROVIDER auth not configured."
fi
ok "$PROVIDER logged in"

# Output dir cleanup
hdr "Cleanup partial state"
PARTIAL_DIRS=(strict-reader purist principle-xxviii-fit-auditor recursion-precedent-auditor summary arbitration)
cleaned=0
for d in "${PARTIAL_DIRS[@]}"; do
    if [[ -d "${DELIB_DIR}/${d}" ]]; then
        say "Removing partial output: ${DELIB_DIR}/${d}"
        rm -rf "${DELIB_DIR}/${d}"
        cleaned=$((cleaned + 1))
    fi
done
if [[ $cleaned -eq 0 ]]; then
    ok "No partial state to clean."
else
    ok "Cleaned $cleaned partial phase directory/ies."
fi

# --------------------------------------------------------------------------
# Run the deliberation
# --------------------------------------------------------------------------
hdr "Run originating deliberation"
cat <<EOF
${BOLD}This will dispatch up to ${EXPECTED_LAUNCHES} LLM calls across 6 phases:${RESET}
  Phase 1: 4 review agents (parallel)
  Phase 2 (×2 iterations): 12 cross-reviews each
  Phase 3 (×2 iterations): 4 revisions each
  Phase 4: 4 dispute agents (parallel)
  Phase 5: 1 synthesis agent
  Phase 6: 1 arbiter (fires if disputes remain)

Expected wall-clock: 15-45 minutes depending on $PROVIDER latency.

EOF
if [[ "$MODE" == "interactive" ]]; then
    read -r -p "Proceed? [y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || fail "Abort."
fi

start_ts=$(date +%s)
log_file="/tmp/deliberator-v4.2.0-self-consistency-rerun-$(date +%Y%m%d-%H%M%S).log"
say "Logging to: $log_file"

set +e
deliberator run "$CONFIG_PATH" --provider "$PROVIDER" 2>&1 | tee "$log_file"
exit_code=${PIPESTATUS[0]}
set -e

end_ts=$(date +%s)
duration=$((end_ts - start_ts))
duration_min=$((duration / 60))
duration_sec=$((duration % 60))

if [[ $exit_code -ne 0 ]]; then
    cat <<EOF

${RED}Deliberation failed${RESET} after ${duration_min}m${duration_sec}s (exit $exit_code).
Log: $log_file

Common causes:
  - Rate limit (429): wait 5-10 min, re-run; Anthropic OAuth budget is per-minute
  - Auth (401): token expired, run \`deliberator login anthropic\` in a real terminal
  - Provider model mismatch: check $CONFIG_PATH agents have valid model names
  - Arbitration prompt overflow: only if synthesis output is huge (>200K chars)

EOF
    exit $exit_code
fi

ok "Deliberation completed in ${duration_min}m${duration_sec}s"

# --------------------------------------------------------------------------
# Verdict inspection
# --------------------------------------------------------------------------
hdr "Verdict inspection"
summary_path="${DELIB_DIR}/summary/final.md"
arbitration_path="${DELIB_DIR}/arbitration/resolution.md"

if [[ -f "$summary_path" ]]; then
    ok "Synthesis written: $summary_path"
else
    warn "No synthesis output — Phase 5 may have failed."
fi

if [[ -f "$arbitration_path" ]]; then
    ok "Arbitration verdict: $arbitration_path"
    echo
    echo "${BOLD}--- First 60 lines of arbitration/resolution.md ---${RESET}"
    head -60 "$arbitration_path"
    echo "${BOLD}--- (truncated; read full file for complete rulings) ---${RESET}"
else
    warn "No arbitration output — Phase 6 either did not fire (no disputes) or failed."
fi

# --------------------------------------------------------------------------
# Commit + push
# --------------------------------------------------------------------------
hdr "Commit + push outputs"
git_status=$(git status --short -- "$DELIB_DIR/")
if [[ -z "$git_status" ]]; then
    warn "No new files under $DELIB_DIR/ — nothing to commit."
    exit 0
fi
echo "Files staged for commit:"
echo "$git_status"
echo

case "$MODE" in
    auto-commit)
        commit_now=1 ;;
    skip-commit)
        say "Skipping commit (--skip-commit). Run \`git add ${DELIB_DIR}/\` and commit manually when ready."
        commit_now=0 ;;
    interactive)
        read -r -p "Commit + push these outputs to $SPEC_BRANCH? [y/N] " ans
        [[ "$ans" =~ ^[Yy]$ ]] && commit_now=1 || commit_now=0 ;;
esac

if [[ $commit_now -eq 1 ]]; then
    git add "$DELIB_DIR/"
    git commit -m "$(cat <<EOF
spec: originating deliberation v4.1.0 outputs

Wall-clock: ${duration_min}m${duration_sec}s on $PROVIDER.
Up to ${EXPECTED_LAUNCHES} LLM launches across 6 phases.

See arbitration/resolution.md for per-question rulings (Q1/Q2/Q3).
See summary/final.md for Phase 5 synthesis.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
    git push origin "$SPEC_BRANCH"
    ok "Pushed to origin/$SPEC_BRANCH"
fi

# --------------------------------------------------------------------------
# Final summary
# --------------------------------------------------------------------------
hdr "Done"
cat <<EOF
${GREEN}Deliberation complete.${RESET}

Wall-clock:     ${duration_min}m${duration_sec}s
Outputs:        $DELIB_DIR/
Verdict file:   $arbitration_path
Log:            $log_file
Branch:         $SPEC_BRANCH ($(git rev-parse --short HEAD))

Next steps:
  1. Read $arbitration_path for per-question rulings.
  2. Report back to Claude Code with the verdict + any APPROVE-WITH-FIXES items.
  3. Claude Code will dispatch the self-consistency verification agent next.

EOF
