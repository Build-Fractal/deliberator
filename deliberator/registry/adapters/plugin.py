"""DefaultPluginAdapter — projects a Capability to a SKILL.md file body.

The projector writes the rendered text to
``claude-code-plugin/skills/<name>/SKILL.md`` — the file layout expected
by Claude Code / Cowork plugins (official ``.claude-plugin`` format).

Generated SKILL.md shape (for a capability named ``hello``)::

    ---
    description: Say hello to someone
    ---

    # Deliberator Hello

    Say hello to someone.

    ## Step 0: Check installation

    ```bash
    deliberator --version 2>/dev/null || echo "NOT_INSTALLED"
    ```

    If `NOT_INSTALLED`, install with:
    `pip install git+https://github.com/Build-Fractal/deliberator.git`

    ## Step 1: Parse arguments

    - `who` (required): Who to greet.
    - `--loud` (default: `false`): Shout instead.

    ## Step 2: Run

    ```bash
    deliberator hello "<who>" [--loud ...]
    ```

    Show the CLI output verbatim.

    ## Troubleshooting

    - For full help: `deliberator hello --help`

**NO list rule #1** (spec 055, section 5): "Don't auto-generate
conversational skill bodies. The ``design`` wizard SKILL.md body stays
hand-written." For ``design`` and any other conversational capability,
register an override PluginAdapter that returns the hand-written file
text verbatim — ``DefaultPluginAdapter`` should not be used for those.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from deliberator.registry.adapters.base import PluginAdapter
from deliberator.registry.params import Surface

if TYPE_CHECKING:
    from deliberator.registry.capability import Capability
    from deliberator.registry.params import Param


#: Canonical install hint surfaced inside generated SKILL.md files.
#: Kept as a module constant so the projector can update it in one place
#: if the repo URL changes.
INSTALL_HINT = (
    "`pip install git+https://github.com/Build-Fractal/deliberator.git`"
)


class DefaultPluginAdapter(PluginAdapter):
    """Projects a capability to a SKILL.md file body."""

    def render(self, capability: "Capability") -> str:
        # Plugin SKILL.md documents the CLI invocation, so it sees the
        # CLI param set — not the MCP one. Per-surface param visibility
        # means CLI-only flags like --format appear here but MCP-only
        # flags like --max-launches do not.
        params = capability.params_for(Surface.CLI)
        description = (
            capability.long_description.strip()
            or capability.summary
        )
        sections = [
            self._frontmatter(description),
            self._title(capability),
            self._installation_check(),
            self._arguments(params),
            self._run(capability, params),
            self._troubleshooting(capability),
        ]
        return "\n\n".join(sections).rstrip() + "\n"

    # ------------------------------------------------------------------

    def _frontmatter(self, description: str) -> str:
        # Single-line description only — matches the existing hand-written
        # SKILL.md files, and avoids YAML quoting gotchas with multiline
        # markdown-flavored descriptions.
        one_liner = " ".join(description.split())
        return f"---\ndescription: {one_liner}\n---"

    def _title(self, cap: "Capability") -> str:
        heading = "Deliberator " + cap.name.replace("-", " ").replace("_", " ").title()
        body = cap.long_description.strip() or cap.summary
        return f"# {heading}\n\n{body}"

    def _installation_check(self) -> str:
        return (
            "## Step 0: Check installation\n\n"
            "```bash\n"
            'deliberator --version 2>/dev/null || echo "NOT_INSTALLED"\n'
            "```\n\n"
            f"If `NOT_INSTALLED`, install with:\n{INSTALL_HINT}"
        )

    def _arguments(self, params: list["Param"]) -> str:
        if not params:
            return "## Step 1: Parse arguments\n\nThis command takes no arguments."

        lines = ["## Step 1: Parse arguments", ""]
        for param in params:
            lines.append(f"- {_arg_bullet(param)}")
        return "\n".join(lines)

    def _run(self, cap: "Capability", params: list["Param"]) -> str:
        cmd = _cli_invocation(cap, params)
        return (
            "## Step 2: Run\n\n"
            "```bash\n"
            f"{cmd}\n"
            "```\n\n"
            "Show the CLI output verbatim."
        )

    def _troubleshooting(self, cap: "Capability") -> str:
        return (
            "## Troubleshooting\n\n"
            f"- For full help: `deliberator {cap.name} --help`"
        )


# ---------------------------------------------------------------------------
# Helpers private to this module
# ---------------------------------------------------------------------------


def _arg_bullet(param: "Param") -> str:
    """One bullet in the SKILL.md "Parse arguments" section."""
    if param.required:
        label = f"`{param.name}` (required)"
    else:
        flag = "--" + param.name.replace("_", "-")
        label = f"`{flag}` (default: `{param.default}`)"

    help_text = param.help or ""
    if param.choices:
        help_text = (help_text + " " if help_text else "") + (
            f"Choices: {', '.join(str(c) for c in param.choices)}."
        )
    return f"{label}: {help_text.strip()}" if help_text else label


def _cli_invocation(cap: "Capability", params: list["Param"]) -> str:
    """Render a representative ``deliberator <cap> ...`` shell invocation."""
    parts = [f"deliberator {cap.name}"]
    for param in params:
        if param.required:
            parts.append(f'"<{param.name}>"')
        else:
            flag = "--" + param.name.replace("_", "-")
            parts.append(f"[{flag} <{param.name}>]")
    return " ".join(parts)
