#!/usr/bin/env bash
# Install `deliberator gate` for Claude Code hooks in its own environment, independent of any
# checkout, with a launcher that fails closed.
#
#   scripts/install-gate.sh            # install or update from this checkout
#
# Puts:
#   $GATE_HOME/venv                 a Python 3.12 environment with deliberator[graph,gate]
#                                   (a copy, not an editable install: deleting this checkout
#                                   or its worktree does not break the hook)
#   $GATE_HOME/gate-hook.sh         the command for the hooks:
#                                   `gate-hook.sh hook`   (PreToolUse)
#                                   `gate-hook.sh record` (PostToolUse)
#
# If the environment is ever missing or broken, the PreToolUse launcher prints an "ask"
# decision, so Claude Code prompts you instead of running the tool unchecked.
# GATE_HOME defaults to ~/.local/share/deliberator.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GATE_HOME="${GATE_HOME:-$HOME/.local/share/deliberator}"
VENV="$GATE_HOME/venv"

"$ROOT/scripts/lattice-wheel.sh" >/dev/null
mkdir -p "$GATE_HOME"
[[ -x "$VENV/bin/python" ]] || uv venv -q --python 3.12 "$VENV"
uv pip install -q --python "$VENV/bin/python" --reinstall-package deliberator \
    --find-links "$ROOT/.wheels" "$ROOT[graph,gate]"

cat > "$GATE_HOME/gate-hook.sh.new" <<EOF
#!/usr/bin/env bash
# deliberator gate launcher for Claude Code hooks (written by scripts/install-gate.sh).
# Fails closed: if the gate can't run, PreToolUse answers "ask".
BIN="$VENV/bin/deliberator"
mode="\${1:-hook}"
if [[ "\$mode" == "hook" ]]; then
    input=\$(cat)
    if [[ -x "\$BIN" ]] && out=\$(printf '%s' "\$input" | "\$BIN" gate hook 2>/dev/null) && [[ -n "\$out" ]]; then
        printf '%s\n' "\$out"
    else
        printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"[deliberator gate] the gate is not installed or failed to start; asking instead. Reinstall: scripts/install-gate.sh in the deliberator repo."}}'
    fi
else
    [[ -x "\$BIN" ]] && "\$BIN" gate record 2>/dev/null
    exit 0
fi
EOF
chmod +x "$GATE_HOME/gate-hook.sh.new"
mv "$GATE_HOME/gate-hook.sh.new" "$GATE_HOME/gate-hook.sh"

"$VENV/bin/deliberator" gate --help >/dev/null
echo "Installed. Hook commands:"
echo "  PreToolUse:  $GATE_HOME/gate-hook.sh hook"
echo "  PostToolUse: $GATE_HOME/gate-hook.sh record"
