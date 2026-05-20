# PyPI release setup (maintainer guide)

This guide is for maintainers wiring up the **one-time** PyPI Trusted Publishing setup. After this is done, releases are triggered by tagging — no API tokens, no manual `twine upload`.

## One-time setup

### 1. Claim the `conversus` name on PyPI

Pick the publishing entity:

- **Build Fractal PyPI organization** (recommended for long-term):
  1. Create an organization at https://pypi.org/account/organizations/. Name suggestion: `build-fractal`.
  2. Verify the organization (PyPI may require domain or DNS verification depending on tier).
  3. Add maintainers as organization members.
- **Personal account** (faster):
  - Log in to the maintainer's PyPI account.

Then publish a placeholder release to claim the name:

```bash
# In a clean checkout
git checkout main && git pull
python -m pip install --upgrade build twine
python -m build  # creates dist/conversus-0.4.0-py3-none-any.whl + sdist
python -m twine upload dist/*
# Provide PyPI credentials (or use ~/.pypirc)
```

Once published, the `conversus` project on PyPI is reserved. Squat risk is eliminated.

If you'd rather claim the name without shipping the current `0.4.0` content (e.g., to preserve a clean release narrative), temporarily bump `pyproject.toml` to `0.0.1`, publish, then revert. The `0.0.1` artifact stays on PyPI as a placeholder — that's the cost of reserving the name without shipping the real thing.

### 2. Configure Trusted Publishing on PyPI

On https://pypi.org/manage/project/conversus/settings/publishing/ add a Trusted Publisher:

| Field | Value |
|---|---|
| Publisher | GitHub |
| Owner | `Build-Fractal` |
| Repository | `conversus` (post-rename) or `conversus-oss` (pre-rename) |
| Workflow filename | `release-pypi.yml` |
| Environment | `pypi-publish` |

Repeat on https://test.pypi.org/manage/project/conversus/settings/publishing/ with environment `testpypi-publish` if you want TestPyPI smoke tests.

### 3. Create the GitHub environments

In repo settings → Environments, create two environments (matching the workflow):

- `pypi-publish` — production. Optionally add a required reviewer for production releases.
- `testpypi-publish` — smoke. No required reviewer needed.

Environments enforce the OIDC trust boundary — only workflow runs inside these environments can mint the OIDC token PyPI will accept.

## Releasing

Once setup is complete, releases follow the same shape every time:

1. **Update `CHANGELOG.md`** with the user-facing changes since the last release. Move any `[Unreleased]` entries under a new versioned heading.
2. **Bump versions across all 5 surfaces** (the constitutional XXII drift surface). All 5 must match:
   ```bash
   pyproject.toml                                # `version = "X.Y.Z"`
   engine/__init__.py                             # `__version__ = "X.Y.Z"`
   .claude-plugin/marketplace.json                # `"version": "X.Y.Z"`
   claude-code-plugin/.claude-plugin/plugin.json  # `"version": "X.Y.Z"`
   desktop-extension/manifest.json                # `"version": "X.Y.Z"`
   ```
3. **Commit + push** the version bump + CHANGELOG update. Open as a PR if desired; merge to main.
4. **Tag the release** at the merge commit:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
5. The `release-pypi.yml` workflow fires automatically. It:
   - Builds `sdist` + `wheel` via `python -m build`
   - Asserts the tag's version matches `pyproject.toml` (catches drift)
   - Publishes to TestPyPI (smoke, non-blocking)
   - Publishes to PyPI (production)
6. Verify the published artifact: `pip install conversus==X.Y.Z` in a clean venv.

## What to do if something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Workflow fails at "Assert pyproject version" | Tag and pyproject disagree | Re-tag or fix pyproject; one of the two is wrong |
| PyPI publish step fails "no trusted publisher configured" | Step 2 above not done, or environment name mismatch | Re-check PyPI publisher settings + GitHub environment name |
| TestPyPI publish fails but production succeeds | TestPyPI hiccup, expected | Workflow ignores TestPyPI failure intentionally |
| Wheel built but `pip install conversus==X.Y.Z` fails downstream | Package data not bundled — common with `templates/`, `presets/`, `schema/` | Check `pyproject.toml` `[tool.hatch.build.targets.wheel]` `force-include`. The .mcpb smoke test (in `.github/workflows/distribution-surface-integrity.yml`) catches this before release. |
| Need to yank a release | A published artifact has a bug | `pip install twine && twine upload --skip-existing dist/*` won't help — use https://pypi.org/manage/project/conversus/releases/ to yank via the web UI |

## Future: extending Principle XXII

The 5-surface version sync is currently manual. A small CI check that asserts all 5 versions match would prevent the drift that bit us at v0.4.0. Worth a small amendment after launch.
