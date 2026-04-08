# Feature Specification: Package Splitting (Build-Time)

**Feature ID**: `032-package-splitting`
**Created**: 2026-04-01
**Updated**: 2026-04-03
**Status**: Ready — all dependencies met, MIT-1 passed.
**Depends On**: `031-docs-and-vercel-compliance` (DONE), `030-domain-plugin-architecture` (DONE), `038-solver-equilibrium-fixes` (DONE), `039-new-mode-payoffs` (DONE), MIT-1 (DONE)
**Docs Update**: Rewrite docs/index.md install section for pip; add per-package README; update pyproject.toml
**Trigger**: Execute now — this is the critical path to users testing conversus.

---

## 1. Approach: Build-Time Splitting (Not Physical Extraction)

The source code stays as a single monolith. The build system produces multiple pip packages from the same source tree. Development workflow is unchanged — `uv run pytest` runs everything.

**Why not physical extraction:** Moving files breaks imports, splits the test suite, and creates multi-repo coordination overhead. Build-time splitting avoids all of this.

**Why not submodules (yet):** Submodule extraction becomes relevant when premium packages need private repos (spec 033 monetization). MIT-1 proved zero coupling — extraction to submodules is mechanical whenever needed. Build-time splitting ships first, submodules follow monetization.

---

## 2. Package Map

### Free Tier (MIT License — `pip install conversus`)

| Package | PyPI Name | Source Included | Contents |
|---------|-----------|----------------|----------|
| Core | `conversus` | engine/, linter/, web/, mcp_server.py, templates/, presets/, schema/ | Deliberation engine, CLI, MCP server, web UI, 8 mode templates, all presets |
| Schemas | included in core | conversus/schemas/ | Game forms, objectives, construction, features, validation |
| Plugin Framework | included in core | conversus/plugins/base.py, config.py | Plugin ABC, hooks, loading |
| Domain Framework | included in core | conversus/domains/base.py, store.py, api.py | Domain ABC, stores, API router |

### Paid Tier (Commercial License — separate packages)

| Package | PyPI Name | Source Included | Contents |
|---------|-----------|----------------|----------|
| Solvers | `conversus-solvers` | conversus/plugins/nashopt/, conversus/plugins/optimizer/ | EquilibriumScorer (heuristic + nashopt), Kalman convergence predictor, AMPL config optimizer, all 8 mode payoff functions |
| Scenarios | `conversus-scenarios` | conversus/plugins/scenarios/ | Scenario storage, cross-run analysis |
| SWE Domain | `conversus-swe` | conversus/domains/implementations/code_review/ | Code review domain implementation |

### Install Patterns

```bash
pip install conversus                    # Free: engine + 8 modes + templates
pip install conversus-solvers            # Paid: equilibrium scoring, convergence, AMPL
pip install conversus-swe                # Paid: code review domain
pip install conversus[all]               # Everything (free + all paid)
```

---

## 3. Build Configuration

Single source tree, multiple build targets via `packages/` directory:

```
conversus/
├── pyproject.toml            # Dev: installs everything (editable)
├── packages/
│   ├── core.toml             # Free: conversus wheel
│   ├── solvers.toml          # Paid: conversus-solvers wheel
│   ├── scenarios.toml        # Paid: conversus-scenarios wheel
│   └── swe.toml              # Paid: conversus-swe wheel
└── scripts/
    └── build-packages.sh     # Builds all wheels from source
```

### Core Package Config (`packages/core.toml`)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "conversus"
version = "0.1.0"
description = "Multi-agent deliberation engine with game theory"
license = "MIT"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "pyyaml>=6.0",
    "click>=8.0",
    "fastapi>=0.100",
    "uvicorn>=0.20",
]

[project.optional-dependencies]
all = ["conversus-solvers", "conversus-scenarios", "conversus-swe"]

[tool.hatch.build.targets.wheel]
packages = ["engine", "linter", "web", "conversus"]
exclude = [
    "conversus/plugins/nashopt",
    "conversus/plugins/optimizer",
    "conversus/plugins/scenarios",
    "conversus/domains/implementations",
]

[tool.hatch.build.targets.wheel.force-include]
"schema" = "conversus/schema"
"templates" = "conversus/templates"
"presets" = "conversus/presets"
```

### Solvers Package Config (`packages/solvers.toml`)

```toml
[project]
name = "conversus-solvers"
version = "0.1.0"
description = "Equilibrium scoring, convergence prediction, and optimization for conversus"
license = "LicenseRef-Proprietary"
dependencies = ["conversus>=0.1.0"]

[project.optional-dependencies]
nashopt = ["nashopt", "jax"]
ampl = ["amplpy", "highspy"]
all = ["nashopt", "jax", "amplpy", "highspy"]

[tool.hatch.build.targets.wheel]
packages = ["conversus"]
include = [
    "conversus/plugins/nashopt/**",
    "conversus/plugins/optimizer/**",
]
```

### Build Script

```bash
#!/usr/bin/env bash
# scripts/build-packages.sh — build all wheels from single source
for config in packages/*.toml; do
    name=$(basename "$config" .toml)
    echo "Building $name..."
    hatch -c "$config" build -t wheel
done
```

---

## 4. Functional Requirements

- **FR-001**: `pip install conversus` MUST install only the free tier. No paid dependencies.
- **FR-002**: `pip install conversus-solvers` MUST add all scoring/optimization features.
- **FR-003**: Dev workflow MUST be unchanged — `uv run pytest` runs all tests.
- **FR-004**: Each wheel MUST be independently installable in a clean venv.
- **FR-005**: `import conversus` MUST NOT trigger import of nashopt, jax, amplpy, or highspy.
- **FR-006**: Removing `conversus-solvers` MUST revert to deliberation-only (no scoring).
- **FR-007**: `pip install conversus[all]` MUST install everything.

---

## 5. Success Criteria

- **SC-001**: `pip install conversus` in clean venv → `conversus run config.yml` works (8 modes).
- **SC-002**: `pip install conversus-solvers` in clean venv → equilibrium scoring appears in output.
- **SC-003**: `uv run pytest` from source tree passes (unchanged dev workflow).
- **SC-004**: Each wheel builds without error via `scripts/build-packages.sh`.

---

## 6. Constraints

- Source tree stays monolithic. No file moves, no import changes.
- Package versions synchronized (same version across all packages per release).
- Build-time splitting is reversible — delete `packages/` dir to go back to monolith.
- Submodule extraction (private repos for paid packages) deferred to when monetization requires access control.
