# Spec 053: Public CI Pipeline

**Status**: Draft
**Author**: Brian Slater + Claude Opus 4.6
**Date**: 2026-04-07
**Depends on**: 052 (open source extraction), 051 (sandbox test harness)

---

## 1. Objective

GitHub Actions CI for the public conversus repo. Free-tier friendly — uses ollama for zero-cost provider testing in CI. No API keys required for the default test suite.

## 2. Workflows

### 2.1 `ci.yml` — Pull Request

```yaml
name: CI
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      ollama:
        image: ollama/ollama
        ports: ["11434:11434"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -e ".[test]"
      - run: ollama pull qwen3:0.6b
      - run: pytest -m "not live and not paid" --cov=engine --cov-report=xml
      - uses: codecov/codecov-action@v4

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install ruff mypy
      - run: ruff check engine/ linter/
      - run: mypy engine/ --ignore-missing-imports
```

### 2.2 `release.yml` — Tag Push

```yaml
name: Release
on:
  push:
    tags: ["v*.*.*"]

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write  # Trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install hatchling build
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

### 2.3 `sandbox.yml` — Weekly Provider Validation

```yaml
name: Sandbox
on:
  schedule: [{ cron: "0 6 * * 1" }]  # Monday 6am UTC
  workflow_dispatch: {}

jobs:
  sandbox:
    runs-on: ubuntu-latest
    services:
      ollama:
        image: ollama/ollama
        ports: ["11434:11434"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ".[test]"
      - run: ollama pull qwen3:0.6b
      - run: pytest -m "sandbox and free" --sandbox-report=report.json
      - uses: actions/upload-artifact@v4
        with: { name: sandbox-report, path: report.json }
```

## 3. Test Markers

| Marker | What | Runs in CI |
|---|---|---|
| (default) | Unit tests, mocked providers | Always |
| `sandbox and free` | Real subprocess tests (mock + ollama) | Always |
| `sandbox and paid` | Real API tests (anthropic, claude-code) | Manual only |
| `live` | Full live provider tests | Manual only |

## 4. Required Secrets

| Secret | Used by | Required |
|---|---|---|
| (none for default CI) | — | — |
| `PYPI_TOKEN` | release.yml trusted publishing | Release only |
| `ANTHROPIC_API_KEY` | sandbox paid tests | Optional manual |

## 5. Coverage Requirements

- Minimum: 85% (current: 92.47%)
- Enforced by codecov config
- New PRs must not decrease coverage

## 6. Ollama in CI

The ollama Docker service starts automatically. Key details:
- `ollama/ollama` official image
- Port 11434 mapped
- `ollama pull qwen3:0.6b` during setup (~400MB download, cached by GH Actions)
- Tests use `OllamaProvider(base_url="http://localhost:11434/v1")`
- Zero cost, runs on every PR
