# Contributing to Conversus

Welcome. This page gets you contributing in under five minutes. For deep technical conventions (code style, frozen models, import discipline, the layer coupling rules), see [docs/developer-guide/contributing.md](docs/developer-guide/contributing.md).

## What kind of contributor are you?

| You are... | Start here |
|---|---|
| **Fixing a typo or small bug** | Jump to [Quick fix](#quick-fix) |
| **Adding a feature or new behavior** | Read [Feature work](#feature-work) |
| **Proposing a constitutional amendment** (changing engine invariants, principles, or governance rules) | Read [Governance changes](#governance-changes) |
| **Building a plugin or domain** | Read [docs/developer-guide/building-plugins.md](docs/developer-guide/building-plugins.md) — you don't need to touch core engine code |
| **Researching the project for an article or comparison** | Read [docs/index.md](docs/index.md) + the [showcase deliberations](README.md#showcase-deliberations-that-earned-their-keep) linked from the README |

## Quick fix

```bash
# 1. Fork on GitHub, then clone your fork
git clone https://github.com/<your-username>/conversus-oss.git
cd conversus-oss

# 2. Set up the dev environment (pick one)
pip install -e ".[dev]"          # straight pip
# or
uv sync                          # if you use uv (prefix all commands below with `uv run`)

# 3. Run tests to confirm the baseline is green
pytest -q -m "not live and not integration and not eval"

# 4. Make your change, add a test if applicable, commit, push, open a PR
```

The PR template will guide you through the rest. Maintainers triage within a few days.

## Feature work

In addition to [Quick fix](#quick-fix) above:

1. **Open an issue first** if the change is non-trivial. This gives maintainers a chance to flag any conflicts with in-flight work or constitutional constraints before you invest hours.
2. **Test discipline:** new code goes in the package it belongs to (e.g. `engine/`, `conversus/`, `linter/`, `web/`). Tests live next to the code (`<pkg>/tests/test_*.py`).
3. **Read the gotchas memo** at [docs/developer-guide/gotchas.md](docs/developer-guide/gotchas.md) before touching the capability registry, the projector, or any generated surface file (`engine/cli/__init__.py`, `mcp_server.py`, `claude-code-plugin/`, `desktop-extension/manifest.json`). It's a hand-off log of subtle bugs prior contributors hit.
4. **Self-review with conversus** for non-trivial PRs — write a `conversus.yml` that critiques your own change. The pattern is documented in [docs/developer-guide/contributing.md §PR process](docs/developer-guide/contributing.md#pr-process). Optional but appreciated; needs API access.
5. **Run the full suite** before pushing: `pytest -q` (or `pytest -m "not live and not eval"` to skip the paid suites). Smoke + unit should take under two minutes.

## Governance changes

Constitutional changes (anything in [`CONSTITUTION.md`](CONSTITUTION.md)) follow a stricter pathway:

1. Read [`CONSTITUTIONAL_CONVERSATIONS.md`](CONSTITUTIONAL_CONVERSATIONS.md) for precedent.
2. Run a multi-stage verification deliberation. Most amendments use the four-stage protocol from spec 067 (originating proposal → self-consistency → blind verification → governance ratification).
3. Open a draft PR with the spec and the deliberation outputs in `deliberations/<amendment-id>/`.
4. Maintainers will run the ratification stage and log the outcome.

This sounds heavy — and it is, on purpose. The verification protocol is itself a deliberation that the project re-runs against its own proposals. The [v4.1.0 self-consistency deliberation](deliberations/v4.1.0-persistence-contract-discipline-self-consistency-2026-05-12/) is a worked example of the full flow.

If you're not sure whether a change is "governance" or "feature work," open an issue and ask.

## Authoring conventions

When contributing prose (specs, READMEs, doc pages):

- **Scripts Over Markdown:** prefer executable scripts or structured data when the artifact drives behavior. Static markdown is fine for human orientation. See [docs/developer-guide/contributing.md](docs/developer-guide/contributing.md) for details.
- **Output conventions** for CLI / MCP / plugin output live in [docs/output-conventions.md](docs/output-conventions.md). New output-emitting code SHOULD follow them.

## Code of conduct

By participating in this project, you agree to abide by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## Where to ask questions

- **Bug reports / feature requests:** [open an issue](https://github.com/Build-Fractal/conversus-oss/issues/new/choose) (templates provided)
- **Security issues:** see [SECURITY.md](SECURITY.md) for the private disclosure path
- **General questions:** GitHub Discussions (once enabled), or open an issue tagged `question`

## License

Apache-2.0. By contributing, you agree your contributions will be licensed under the same terms. See [LICENSE](LICENSE).
