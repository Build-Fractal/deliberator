# Claude Desktop Extension (`.mcpb`)

The fastest way to get deliberator running in Claude Desktop — **no Python install, no terminal, no pip**. Double-click a bundle file and Claude Desktop installs it in one click.

## What it is

A Claude Desktop **Extension** is a `.mcpb` (MCP Bundle) — a ZIP archive containing a manifest and a self-contained MCP server. When you install it, Claude Desktop registers the MCP server and makes its tools available to Claude automatically.

For deliberator, the bundle ships three tools:

| Tool | What it does |
|---|---|
| `deliberator_decide` | Run an ad-hoc deliberation on a natural-language question |
| `deliberator_run` | Run or parse a full deliberation from a YAML config file |
| `deliberator_validate` | Validate a config and show the estimated LLM launch count |

Once installed, Claude can invoke these tools autonomously — you just describe what you want in plain language ("deliberate on whether we should use Postgres or MongoDB") and Claude picks the right tool and calls it.

## Install (one click)

### Step 1: Download the bundle

Pick the bundle for your platform from the latest release:

| Platform | File |
|---|---|
| macOS (Apple Silicon) | [deliberator-darwin-arm64.mcpb](https://github.com/Build-Fractal/deliberator/releases/latest/download/deliberator-darwin-arm64.mcpb) |
| Linux (x86_64) | [deliberator-linux-x86_64.mcpb](https://github.com/Build-Fractal/deliberator/releases/latest/download/deliberator-linux-x86_64.mcpb) |
| Windows (x86_64) | [deliberator-win-x86_64.mcpb](https://github.com/Build-Fractal/deliberator/releases/latest/download/deliberator-win-x86_64.mcpb) |

!!! note "Intel Mac users"
    GitHub removed the free Intel Mac CI runner, so we don't ship a `darwin-x86_64.mcpb`. Install via `pip install git+https://github.com/Build-Fractal/deliberator.git` instead, or open an issue if you need a signed Intel Mac build.

### Step 2: Install in Claude Desktop

Two equivalent paths:

**Option A — Double-click**
Double-click the downloaded `.mcpb` file. Claude Desktop opens an install dialog showing the extension details and the three tools it exposes. Click **Install**.

**Option B — Settings menu**
1. Open Claude Desktop
2. Go to **Settings → Extensions**
3. Click **Install from file**
4. Select the downloaded `.mcpb`

### Step 3: Use it

Once installed, the extension works through **natural language**, not slash commands or menus. Claude Desktop reads the three tool descriptions from the manifest and picks the right one when your request matches.

!!! tip "There's no walkthrough or help screen — the tool descriptions are the help"
    Unlike plugins with slash commands, MCP extensions don't have a "getting started" button after install. You just open a new chat and describe what you want. Claude figures out which tool to call based on the phrasing.

## Example prompts

Copy-paste these into a new Claude Desktop chat to see each tool in action:

### For an ad-hoc decision (`deliberator_decide`)

> Use deliberator to deliberate on whether we should use Postgres or MongoDB for a user profile service. Use the cooperative mode.

> Run `deliberator_decide` on this question: "Should a 3-person team start with microservices or a monolith?" — use red-blue mode.

> I need to pick between Redis and Memcached for session caching. Can you run a quick deliberator deliberation on it?

### For a full deliberation from a config file (`deliberator_run`)

> Run the deliberator deliberation at `/path/to/my-review/deliberator.yml` using the anthropic provider.

> Parse the existing deliberator output at `/path/to/deliberations/auth-review/output/` and summarize the verdict.

### For cost estimation before committing (`deliberator_validate`)

> Validate the deliberator config at `/path/to/my-deliberation/deliberator.yml` and tell me how many LLM launches it'll take.

> Check if this config is valid and show me the cost: `/path/to/deliberator.yml`

## How Claude picks which tool to call

When you send a message in Claude Desktop, it matches your intent against the tool descriptions in the manifest:

| If you say... | Claude calls... |
|---|---|
| "Deliberate on...", "decide between...", "which should we pick..." (with a question, no config file) | `deliberator_decide` |
| "Run the deliberator config at...", "parse this output..." (with a file path) | `deliberator_run` |
| "Validate this config", "check the cost", "how many launches..." | `deliberator_validate` |

You can also **explicitly name the tool**: "Use `deliberator_decide` to …" bypasses the routing and forces Claude to call that specific tool.

## Troubleshooting: "nothing happens after install"

If you install the extension, ask Claude a question, and nothing happens:

1. **Restart Claude Desktop.** Extensions load at startup — a new install may not take effect until you close and reopen the app.
2. **Check the extensions panel.** Settings → Extensions — deliberator should appear with a green "Installed" indicator. If it shows an error, the bundle failed to load (usually a Python version mismatch or missing compiled dependency).
3. **Verify the tools are registered.** Start a new chat and ask: "What MCP tools do you have access to?" Claude should list `deliberator_decide`, `deliberator_run`, and `deliberator_validate`. If it doesn't, the MCP server failed to start.
4. **Check the logs.** Claude Desktop writes MCP server output to its logs — look for errors from the deliberator server. On macOS: `~/Library/Logs/Claude/mcp.log` (or similar).
5. **Test with an explicit tool call.** Try: "Call the `deliberator_decide` tool with the question 'Postgres or MongoDB?' and the provider 'mock'". If this works but natural language doesn't, it's a phrasing problem — match the verbs in the tool descriptions more closely.

## What's inside the bundle

The `.mcpb` is a ZIP with this structure:

```
deliberator.mcpb (ZIP)
├── manifest.json         # MCPB v0.3 manifest describing the extension
└── server/
    ├── main.py           # Bootstrap entry point
    ├── mcp_server.py     # FastMCP server exposing the 3 tools
    └── lib/              # deliberator + all Python dependencies (~90MB)
```

The bundle is **self-contained** — `server/lib/` ships the entire deliberator Python package plus transitive dependencies (anthropic, openai, pydantic, mcp, click, rich, and ~40 more). Claude Desktop's bundled Python runs `server/main.py`, which bootstraps `sys.path` from the bundled `lib/` directory and starts the MCP server.

This means:

- **No separate `pip install`** is needed
- **No Python version management** — Claude Desktop ships its own Python
- **No PATH setup** — the bundle is entirely self-referential

## Permissions warning

When you install the extension, Claude Desktop shows a warning:

> Installing will grant this extension access to everything on your computer. Any developer information shown has not been verified by Anthropic. Ensure you trust the source of this extension before installation.

This is a **generic warning shown for all extensions**, not a security issue specific to deliberator. It's accurate — an MCP server runs with the same permissions as Claude Desktop itself, and only you can verify that the code does what it claims.

To audit deliberator before installing:

1. **Read the source** — everything that runs is in the [deliberator repo](https://github.com/Build-Fractal/deliberator). The `server/main.py` and `server/mcp_server.py` files inside the `.mcpb` are both in the repo and unmodified.
2. **Inspect the bundle yourself** — a `.mcpb` is just a ZIP: `unzip deliberator-darwin-arm64.mcpb` and read the contents.
3. **Build it yourself** — clone the repo and run `desktop-extension/build.sh` to produce the same `.mcpb` from source.

## Updating

Extensions don't auto-update in Claude Desktop. To update:

1. Download the new `.mcpb` from the [releases page](https://github.com/Build-Fractal/deliberator/releases)
2. Settings → Extensions → find deliberator → **Uninstall**
3. Double-click the new `.mcpb` to install

## Uninstalling

Settings → Extensions → deliberator → **Uninstall**. The bundle and all extracted files are removed.

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

The Desktop Extension is one of four deliberator distribution channels:

| Channel | Install | Best for |
|---|---|---|
| **Desktop Extension** (this page) | Double-click `.mcpb` | Claude Desktop users who want zero-setup install |
| **Claude Code plugin** | `/plugin marketplace add` | Slash command UX (`/deliberator:design`, `/deliberator:decide`) |
| **MCP server** via `pip install` | `pip install git+...` + `claude mcp add` | Cursor, Windsurf, Zed, Continue, and any MCP client besides Claude Desktop |
| **Python CLI** | `pip install git+...` | Scripting, CI/CD, terminal power users |

All four channels expose the same underlying deliberation engine. You don't need to pick one — they compose freely, and you can use different channels on different machines.

## Next steps

- [Your First Deliberation](first-deliberation.md) — 5-minute walkthrough of the full pipeline
- [Building a Config](building-a-config.md) — manual config walkthrough with examples
- [MCP Setup](mcp-setup.md) — MCP server install for Cursor, Windsurf, and other non-Desktop editors
- [Modes](modes.md) — deep dive on the 8 deliberation modes
