# Claude Desktop Extension (`.mcpb`)

The fastest way to get conversus running in Claude Desktop — **no Python install, no terminal, no pip**. Double-click a bundle file and Claude Desktop installs it in one click.

## What it is

A Claude Desktop **Extension** is a `.mcpb` (MCP Bundle) — a ZIP archive containing a manifest and a self-contained MCP server. When you install it, Claude Desktop registers the MCP server and makes its tools available to Claude automatically.

For conversus, the bundle ships three tools:

| Tool | What it does |
|---|---|
| `conversus_decide` | Run an ad-hoc deliberation on a natural-language question |
| `conversus_run` | Run or parse a full deliberation from a YAML config file |
| `conversus_validate` | Validate a config and show the estimated LLM launch count |

Once installed, Claude can invoke these tools autonomously — you just describe what you want in plain language ("deliberate on whether we should use Postgres or MongoDB") and Claude picks the right tool and calls it.

## Install (one click)

### Step 1: Download the bundle

Pick the bundle for your platform from the latest release:

| Platform | File |
|---|---|
| macOS (Apple Silicon) | [conversus-darwin-arm64.mcpb](https://github.com/Build-Fractal/conversus-oss/releases/latest/download/conversus-darwin-arm64.mcpb) |
| Linux (x86_64) | [conversus-linux-x86_64.mcpb](https://github.com/Build-Fractal/conversus-oss/releases/latest/download/conversus-linux-x86_64.mcpb) |
| Windows (x86_64) | [conversus-win-x86_64.mcpb](https://github.com/Build-Fractal/conversus-oss/releases/latest/download/conversus-win-x86_64.mcpb) |

!!! note "Intel Mac users"
    GitHub removed the free Intel Mac CI runner, so we don't ship a `darwin-x86_64.mcpb`. Install via `pip install git+https://github.com/Build-Fractal/conversus-oss.git` instead, or open an issue if you need a signed Intel Mac build.

### Step 2: Install in Claude Desktop

Two equivalent paths:

**Option A — Double-click**
Double-click the downloaded `.mcpb` file. Claude Desktop opens an install dialog showing the extension details and the three tools it exposes. Click **Install**.

**Option B — Settings menu**
1. Open Claude Desktop
2. Go to **Settings → Extensions**
3. Click **Install from file**
4. Select the downloaded `.mcpb`

### Step 3: Verify it's working

After install, ask Claude Desktop something like:

> Can you validate the conversus config at `~/my-deliberation/conversus.yml` and tell me how much it'll cost to run?

Claude should invoke the `conversus_validate` tool automatically and return the parsed config + LLM launch estimate.

## What's inside the bundle

The `.mcpb` is a ZIP with this structure:

```
conversus.mcpb (ZIP)
├── manifest.json         # MCPB v0.3 manifest describing the extension
└── server/
    ├── main.py           # Bootstrap entry point
    ├── mcp_server.py     # FastMCP server exposing the 3 tools
    └── lib/              # conversus + all Python dependencies (~90MB)
```

The bundle is **self-contained** — `server/lib/` ships the entire conversus Python package plus transitive dependencies (anthropic, openai, pydantic, mcp, click, rich, and ~40 more). Claude Desktop's bundled Python runs `server/main.py`, which bootstraps `sys.path` from the bundled `lib/` directory and starts the MCP server.

This means:

- **No separate `pip install`** is needed
- **No Python version management** — Claude Desktop ships its own Python
- **No PATH setup** — the bundle is entirely self-referential

## Permissions warning

When you install the extension, Claude Desktop shows a warning:

> Installing will grant this extension access to everything on your computer. Any developer information shown has not been verified by Anthropic. Ensure you trust the source of this extension before installation.

This is a **generic warning shown for all extensions**, not a security issue specific to conversus. It's accurate — an MCP server runs with the same permissions as Claude Desktop itself, and only you can verify that the code does what it claims.

To audit conversus before installing:

1. **Read the source** — everything that runs is in the [conversus-oss repo](https://github.com/Build-Fractal/conversus-oss). The `server/main.py` and `server/mcp_server.py` files inside the `.mcpb` are both in the repo and unmodified.
2. **Inspect the bundle yourself** — a `.mcpb` is just a ZIP: `unzip conversus-darwin-arm64.mcpb` and read the contents.
3. **Build it yourself** — clone the repo and run `desktop-extension/build.sh` to produce the same `.mcpb` from source.

## Updating

Extensions don't auto-update in Claude Desktop. To update:

1. Download the new `.mcpb` from the [releases page](https://github.com/Build-Fractal/conversus-oss/releases)
2. Settings → Extensions → find conversus → **Uninstall**
3. Double-click the new `.mcpb` to install

## Uninstalling

Settings → Extensions → conversus → **Uninstall**. The bundle and all extracted files are removed.

## Platform compatibility

| Platform | Status | Notes |
|---|---|---|
| macOS (Apple Silicon) | Supported | `darwin-arm64.mcpb` |
| macOS (Intel) | Not available | Use `pip install` instead — GitHub removed free Intel Mac CI runners |
| Linux (x86_64) | Supported | `linux-x86_64.mcpb` |
| Windows (x86_64) | Supported | `win-x86_64.mcpb` |
| Windows (ARM64) | Not available | Use WSL + `pip install` |
| Linux (ARM64) | Not available | Build from source — open an issue if you need a pre-built bundle |

## Relationship to other distribution artifacts

The Desktop Extension is one of four conversus distribution channels:

| Channel | Install | Best for |
|---|---|---|
| **Desktop Extension** (this page) | Double-click `.mcpb` | Claude Desktop users who want zero-setup install |
| **Claude Code / Cowork plugin** | `/plugin marketplace add` | Slash command UX (`/conversus:design`, `/conversus:decide`) |
| **MCP server** via `pip install` | `pip install git+...` + `claude mcp add` | Cursor, Windsurf, Zed, Continue, and any MCP client besides Claude Desktop |
| **Python CLI** | `pip install git+...` | Scripting, CI/CD, terminal power users |

All four channels expose the same underlying deliberation engine. You don't need to pick one — they compose freely, and you can use different channels on different machines.

## Next steps

- [Your First Deliberation](first-deliberation.md) — 5-minute walkthrough of the full pipeline
- [Building a Config](building-a-config.md) — manual config walkthrough with examples
- [MCP Setup](mcp-setup.md) — MCP server install for Cursor, Windsurf, and other non-Desktop editors
- [Modes](modes.md) — deep dive on the 8 deliberation modes
