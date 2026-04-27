# Spec 052: Open Source Extraction

**Status**: Done — closed 2026-04-27 per spec hygiene audit. The OSS extraction has happened — this `conversus-oss` repo IS the public extraction; the private Build-Fractal/conversus repo holds the paid plugins.
**Author**: Brian Slater + Claude Opus 4.6
**Date**: 2026-04-07
**Depends on**: 050 (cascading settings / plugin approach)

---

## 1. Objective

Extract the conversus core deliberation engine into a public open-source package. The private Clariti-specific code (game theory plugins, domain implementations, web UI) stays in the Build-Fractal/conversus private repo. The public package ships as `conversus` on PyPI.

## 2. Repository Split

### Public: `conversus` (Apache-2.0)

```
conversus/
├── engine/                    # Core deliberation engine
│   ├── cli/                   # CLI: run, decide, validate, init, context, status
│   ├── execution/             # ExecutionProvider protocol
│   │   └── providers/         # 12 providers (mock through vllm)
│   ├── dispatch.py            # Agent dispatch + events
│   ├── phases.py              # 5-phase pipeline
│   ├── config.py              # YAML config parser
│   ├── events.py              # Event system
│   ├── output.py              # Output manager
│   ├── project.py             # conversus init
│   ├── templates.py           # Template engine
│   ├── run.py                 # Entry point
│   ├── cost.py                # Cost estimation
│   ├── errors.py              # Error mapping
│   └── auth.py                # Auth (OAuth client ID from config, not hardcoded)
├── linter/                    # Quality checks
├── templates/                 # Phase templates
├── presets/                   # Agent presets
├── install.sh                 # Installer
├── scripts/dev-setup.sh       # Dev env setup
├── pyproject.toml             # Package config (no supabase, no nashopt in core)
├── LICENSE                    # Apache-2.0
├── README.md                  # Public-facing (see spec 054)
└── .github/workflows/         # CI (see spec 053)
```

### Private: `conversus-internal` (proprietary, stays in Build-Fractal/conversus)

```
conversus-internal/
├── conversus/plugins/         # Game theory plugins
│   ├── nashopt/               # Equilibrium scorer, convergence predictor
│   ├── optimizer/             # Config optimizer (AMPL)
│   └── scenarios/             # Scenario storage
├── conversus/domains/         # Domain implementations
├── web/                       # Supabase web UI
├── schema/                    # Objective function templates
│   └── objective-functions/   # AMPL .mod files
├── packages/                  # Build configs for split packages
│   ├── solvers.toml
│   ├── scenarios.toml
│   └── swe.toml
└── pyproject.toml             # Dev config (depends on conversus)
```

## 3. Code Changes Required

### 3.1 Auth: Remove Hardcoded OAuth Client ID

**Current** (`engine/auth.py:39`):
```python
OAUTH_CONFIGS = {
    "anthropic": {
        "client_id": base64.b64decode("OWQxYzI1MGEt...").decode(),
        ...
    }
}
```

**Target**: Read from config or env var.
```python
OAUTH_CONFIGS = {
    "anthropic": {
        "client_id": os.environ.get(
            "CONVERSUS_ANTHROPIC_CLIENT_ID",
            _DEFAULT_CLIENT_ID,  # Conversus public OAuth app
        ),
        ...
    }
}
```

Register a public Conversus OAuth application with Anthropic so OSS users get a real client ID. Fall back to env var for custom deployments.

### 3.2 Claude Code Version: Derive from Environment

**Current** (`engine/providers/anthropic.py:18`):
```python
CLAUDE_CODE_VERSION = "2.1.62"
```

**Target**: Detect from installed Claude Code binary.
```python
def _detect_claude_version() -> str:
    result = subprocess.run(["claude", "--version"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "unknown"
```

### 3.3 Supabase: Move to Optional Extra

**Current** (`pyproject.toml:19`):
```toml
dependencies = [..., "supabase>=2.0.0", ...]
```

**Target**:
```toml
dependencies = [...]  # No supabase in core

[project.optional-dependencies]
web = ["supabase>=2.0.0", "fastapi>=0.115.0", "uvicorn[standard]>=0.34.0"]
```

### 3.4 Plugin System: Keep Wiring, Remove Implementations

The plugin base class (`conversus/plugins/base.py`) and hook wiring in `phases.py` stay in the public repo. The plugin implementations (nashopt, optimizer, scenarios) move to the private repo as optional `pip install conversus-plugins` extras.

### 3.5 Private References: Scrub

Grep for and remove:
- `clariti-care/` org references
- `Build-Fractal/` private repo references (keep public repo refs)
- Internal Slack channel references
- Customer-specific data references

## 4. License

**Apache-2.0** — permissive with patent grant and attribution requirement.

Rationale:
- 60% of comparable AI projects use MIT, 30% Apache-2.0
- Apache-2.0 provides explicit patent grant (protects contributors)
- Requires attribution (NOTICE file) — commercial users must credit
- Compatible with MIT dependencies
- Allows commercial use but gives leverage for enterprise licensing
- Aider, vLLM, OpenAI SDK use Apache-2.0 for similar reasons

### Dual Licensing Option

For future enterprise/commercial licensing:
- Open source: Apache-2.0 (free for all use)
- Enterprise: Commercial license with SLA, priority support, private plugins
- The plugin architecture naturally supports this: core is OSS, premium plugins are commercial

## 5. PyPI Publishing

- Package name: `conversus` (confirmed available)
- Publish via GitHub Actions on tag push (`v*.*.*`)
- Build with `hatchling` (already configured in `packages/core.toml`)
- Test on TestPyPI first

## 6. Migration Steps

| Step | What | Effort |
|---|---|---|
| 1 | Create `conversus-internal/` directory in private repo | 10 min |
| 2 | Move plugins/, web/, schema/objective-functions/ to internal | 30 min |
| 3 | Fix auth.py — env var OAuth client ID | 15 min |
| 4 | Fix anthropic provider — derive Claude version | 15 min |
| 5 | Move supabase to `[web]` optional extra | 10 min |
| 6 | Scrub private references | 1 hour |
| 7 | Write Apache-2.0 LICENSE + NOTICE | 15 min |
| 8 | Write public README (spec 054) | 1-2 hours |
| 9 | Set up CI (spec 053) | 1-2 hours |
| 10 | Make Build-Fractal/conversus repo public | 5 min |
| 11 | Publish to PyPI | 15 min |
| 12 | Create `conversus-internal` private repo for plugins | 30 min |

**Total**: ~5-7 hours of work.

## 7. Open Questions

1. **Should specs/ be public?** They document the architecture openly — good for community trust. But they reference internal decisions. Recommendation: include specs, scrub internal refs.
2. **Should the game engine plugin hooks stay in the public engine?** The hooks are in `phases.py` and cost nothing when no plugins are loaded. Keeping them lets the community write plugins. Recommendation: yes, keep hooks.
3. **Monorepo vs standalone repo?** Currently conversus is a submodule in payer-index-mono. For OSS, it should be a standalone repo. Recommendation: make Build-Fractal/conversus the public repo, create a new private repo for internal plugins.

---

## Closure note (2026-04-27)

**Why closed**: The repo split has happened. The directory containing this spec (`conversus-oss/`) IS the extracted OSS package. The split topology shipped per `feedback_conversus_oss_trunk_topology.md`: OSS-trunk + sibling-wheels (`conversus` core public + `conversus-enhanced` private with paid capabilities). This spec is now a historical record of the extraction plan.

**Where the work lives**:
- This repository (`conversus-oss`) — the extracted public package, published as `conversus` on PyPI
- Build-Fractal org on GitHub — public repo home (per `project_conversus_org_move.md`)
- `conversus-enhanced` (private) — sibling wheel containing paid plugins/domain-specific code
- `specs/065-path-to-open-source/` — the active roadmap spec for ongoing OSS work

**Reference**: `specs/AUDIT-2026-04-27.md` §A "052-open-source-extraction" — definitively shipped, recommended close.
