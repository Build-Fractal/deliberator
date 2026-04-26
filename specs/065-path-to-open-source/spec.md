# Feature Specification: Path to Open Source

**Feature ID**: `065-path-to-open-source`
**Created**: 2026-04-25
**Status**: Draft v2 — amended to reference constitution v2.3.0 principles proposed by spec 066
**Depends On**: `052-open-source-extraction`, `053-public-ci-pipeline`, `054-public-documentation`, `066-constitution-v2.3.0` (proposed amendments referenced in gates G2/G5/G6/G9)
**Governed by**: `CONSTITUTION.md` (principle II — Stable Interfaces, principle XI — Single Source of Truth)
**Originating context**: Open-source readiness has been a moving target across multiple sessions. Specs 052/053/054 describe **what** to publish; this spec describes **the path** — gate ordering, decision criteria, and the readiness checklist to actually flip the repository from private to public.

> **Scope discipline**: This spec defines a launch-readiness gate sequence. It does NOT redefine what code ships (052), how CI runs (053), or what the README says (054). It does NOT decide the name (that is its own gate). It does NOT prescribe marketing or community-management posture beyond the minimum required for safe publication.

---

## 1. Summary

The `conversus-oss` repository at `Build-Fractal/conversus-oss` is currently private. Specs 052/053/054 describe the content shape of the eventual public package. Across recent sessions, several readiness questions have been raised and partially answered:

- "Are we ready to open source it?" — answered "I am okay with open source readiness; wait to execute, I want to prioritize the work."
- "I'm considering a name change so we need to decide on that before these [other gates]."
- The Wave 2 consolidation (specs 055/064/064.1) has merged; the OSS engine is functionally complete for its declared surface.
- Distribution mechanics (PR #11 wheel, PR #13 manifest version sync, PR #14 disabled-tools filter) have hardened.

**This spec answers**: given that the content is approximately ready, what is the **ordered sequence of gates** that must pass before the repository visibility flips from private to public, and what is the **decision criterion** for each gate?

## 2. Goals

1. Define a complete, ordered gate sequence from "private repo today" to "public repo with PyPI publishing pipeline live and announcement posted."
2. Make each gate **independently checkable** — every gate has an acceptance criterion that a single person can verify in <30 minutes.
3. Surface **decision-blocking gates** (name decision, license review, security audit) explicitly so they don't slip past as ambient assumptions.
4. Preserve **revertibility** at every gate before the visibility flip — anything before the flip is a private-repo change.
5. Define **post-launch obligations** so we don't ship a repository that becomes immediately stale.

## 3. Non-goals

- **Marketing/announcement strategy.** This spec lists the pre-flight checklist; the launch-day messaging is its own document.
- **Community management.** Issue triage cadence, governance model, contributor licensing — out of scope here. Cover separately if/when the repo gains external contributors.
- **License selection.** Apache-2.0 is already declared in `pyproject.toml`. Re-litigating this is not a gate.
- **The name decision itself.** This spec includes a name-decision gate but does not prescribe the answer.
- **Any work in `conversus-enhanced` (private).** This spec covers the public OSS repo only.

## 4. Pre-requisites already met

| Pre-requisite | Status | Evidence |
|---|---|---|
| Repo extraction | ✅ Done | `Build-Fractal/conversus-oss` exists with full engine, linter, registry |
| Apache-2.0 license declared | ✅ Done | `pyproject.toml` `license = { text = "Apache-2.0" }` |
| Wheel publishability | ✅ Done | PR #11 packaged `mcp_server.py` + `capabilities.py`; `uv build` produces a working wheel |
| MCP server operational | ✅ Done | 4 hand-coded tools + 7 prompts + spec 064.1 runtime registration |
| Desktop Extension build pipeline | ✅ Done | `desktop-extension/build.sh` + `release-mcpb.yml` produce 3-platform `.mcpb` |
| Manifest single-sourced version | ✅ Done | PR #13 |
| Operator tool filtering | ✅ Done | PR #14 (`CONVERSUS_DISABLED_TOOLS`) |
| Test coverage on prompts + tools | ✅ Done | PR #12 + existing `test_mcp_server.py` |
| Baseline CI green | ✅ Done | `Smoke tests (mock provider)` passing on main |

## 5. Open readiness gates

Ordered. Each gate is **blocking** for the next unless explicitly marked parallel.

### Gate G1 — Name decision

**Question**: Does the project ship as `conversus`, or under a different name?

**Why blocking**: PyPI dist name, GitHub URL, Claude Desktop bundle ID, and `manifest.json` `name` field are all set today to `conversus`. A rename touches: `pyproject.toml` `[project] name`, `package_name`, all `import` statements, `desktop-extension/manifest.json`, the GitHub repo URL itself, every doc reference, the `conversus` CLI entry point, every `@mcp.tool()` prefix.

**Decision criterion**: a written decision (this spec, or a referenced ADR) selecting either `conversus` or a replacement, with rationale. Defaults to `conversus` if no decision is filed within 7 days of this spec landing.

**Output**: a single line in this spec's §11 (Decisions) recording the choice + date.

### Gate G2 — Security audit (single source name in code)

**Question**: Does the codebase contain any secrets, internal-only references, or sensitive paths?

**Why blocking**: Once public, history is forever — a single committed API key requires a force-push + GitHub support ticket to scrub.

**Acceptance criterion** — all of:
- `gitleaks detect --source . --no-git -v` returns zero findings.
- Manual grep for known internal hostnames (`*.clariti.local`, `*.clariti.care`, `payer-index-mono`, internal Slack channel names, internal user emails other than commit authors) returns zero matches in code/docs.
- `git log --all --oneline | wc -l` matches `git log --all --diff-filter=A --name-only` for any historical key files (no force-pushed evidence of redaction).
- All `.env*` files are gitignored AND not present in any commit. `git log --all -- '*.env*'` is empty.

**Tooling**: `gitleaks` (Homebrew or release binary). Run as a one-time audit + add to CI per spec 053.

**Constitutional alignment** (post-v2.3.0): G2 satisfies the security half of Principle XXII (Distribution Surface Integrity). The remaining halves of XXII — single-source versioning and force-include discipline — are already met (PR #11, PR #13). The end-to-end install testing half is enforced at G9.

### Gate G3 — License header sweep

**Question**: Does every source file declare its license?

**Acceptance criterion**: Every `.py` file under `engine/`, `linter/`, `conversus/`, `mcp_server.py`, and `capabilities.py` has either a SPDX header (`# SPDX-License-Identifier: Apache-2.0`) or no header (acceptable — license declared in `pyproject.toml` + repo-root `LICENSE` file). Mixed states are not acceptable. Pick one and enforce.

**Default**: SPDX headers on top-level entry points (`mcp_server.py`, `capabilities.py`, `engine/cli/__init__.py`); no headers required on internal modules. Document the policy in `CONTRIBUTING.md`.

### Gate G4 — README + Quickstart parity (spec 054)

**Question**: Does spec 054's prescribed README exist on disk and match the current behavior?

**Acceptance criterion**: A reviewer following the README's quickstart exactly (`pip install conversus`, `conversus decide "..."`) reaches a working deliberation in under 5 minutes from a clean machine. The quickstart uses `--provider mock` so no API keys are required.

**Verification**: One-shot test — fresh Docker container, follow README copy-paste, observe success.

### Gate G5 — PyPI publishing pipeline

**Question**: Can a tag push (`v0.3.1`, etc.) automatically publish to PyPI?

**Why blocking**: Currently the only distribution path is `pip install git+ssh://...`. After flipping public, users will expect `pip install conversus`. Without a publish workflow, the first install attempt fails.

**Acceptance criterion**:
- `.github/workflows/publish-pypi.yml` exists, triggers on `v*` tag push, uses PyPI Trusted Publishing (no long-lived token).
- A test publish to TestPyPI succeeds end-to-end.
- The published package's import surface matches the source — `pip install conversus` then `from conversus.registry import Capability` works without errors.

**Constitutional alignment** (post-v2.3.0): G5 publishes a wheel whose providers satisfy Principle XXIII (Provider Robustness Contract) — token reporting, retry-with-jitter, protocol tolerance, structurally-valid response handling. PRs #5, #6, #8, #9 already established this baseline; G5 inherits these guarantees by virtue of publishing the wheel that contains them.

### Gate G6 — Public CI pipeline (spec 053)

**Question**: Does the CI run successfully on a fresh clone with no Build-Fractal-specific environment?

**Why blocking**: External PRs cannot reference Build-Fractal secrets. CI must be green for unauthenticated forks.

**Acceptance criterion**:
- Spec 053's prescribed `ci.yml` is in `.github/workflows/`.
- Smoke test: open a PR from a fork-equivalent (a branch with no secret access). CI must pass.
- All current secret references are scoped to optional jobs (e.g., live integration tests gated behind `secrets.ANTHROPIC_API_KEY` with a `continue-on-error` skip when absent).

**Constitutional alignment** (post-v2.3.0): G6 enforces Principle XXV (Live Test Cost Discipline). CI runs `pytest -m "not live"` by default; live tests run in a separate manually-triggered or scheduled job, never on fork-PRs (which cannot reference Build-Fractal secrets). The default test surface for external contributors is free-tier — Principle XXV makes this a constitutional requirement, not just a nicety.

### Gate G7 — Issue templates, CONTRIBUTING, code of conduct

**Acceptance criterion** — files present and current:
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `CONTRIBUTING.md` (covers: dev setup, test running, conventional commits, DCO sign-off if required)
- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1 verbatim is acceptable)
- `SECURITY.md` (how to report a vulnerability — currently absent)

### Gate G8 — Visibility flip (the actual public moment)

**Pre-conditions**: G1–G7 complete.

**Action**: GitHub repo Settings → Danger Zone → Change visibility → Public.

**Acceptance criterion**:
- The repo is reachable at `https://github.com/Build-Fractal/conversus-oss` without authentication.
- A clean `git clone` over HTTPS (no auth) succeeds.
- The most recent CI run on `main` is green and visible in the public Actions tab.

**Rollback**: Visibility can flip back to private within minutes. History is NOT retracted from any clone made during the public window — assume any commit made before this gate is permanently observable once the gate fires.

### Gate G9 — First public release

**Acceptance criterion**:
- A `v0.3.1` (or whatever version Gate G1 selects) tag is pushed.
- Both `release-mcpb.yml` and `publish-pypi.yml` workflows complete successfully.
- The release page on GitHub shows: 3 `.mcpb` artifacts (darwin/linux/win), the release notes, and links to the PyPI page.
- `pip install conversus` from a fresh venv succeeds and `conversus --help` works.

**Constitutional alignment** (post-v2.3.0): G9 satisfies Principle XXII (Distribution Surface Integrity) end-to-end install testing requirement. "It works in my dev checkout" is not sufficient — G9's fresh-venv test on each platform (or a documented manual test for at least the maintainer's primary platform) is the constitutional bar.

### Gate G10 — Announcement (parallel to G9)

**Acceptance criterion**:
- Announcement text drafted and reviewed.
- Posting channels selected (project README banner, Build-Fractal blog, Hacker News, X, MCP catalogs).
- Posting performed (or scheduled).

This gate does NOT block any other gate — it can fire any time after G8.

## 6. Gate dependency graph

```
G1 (name) ──► G2 (security) ──► G3 (license) ──► G4 (README) ──► G6 (CI) ──► G7 (templates) ──► G8 (FLIP)
                                                          │                                          │
                                                          └────► G5 (PyPI) ──────────────────────────┤
                                                                                                     ▼
                                                                                              G9 (release)
                                                                                                     │
                                                                                                     ▼
                                                                                              G10 (announce)
```

G5 and G6 can execute in parallel after G4. Everything else is strictly sequential.

## 7. Acceptance criteria for this spec

The spec itself is "done" when:

1. Each gate G1–G10 has a checkbox somewhere reachable from this spec (a tracking issue is acceptable).
2. The name decision (G1) is filed in §11 below.
3. The security audit (G2) has been run at least once and the findings (zero or otherwise) are recorded.
4. PyPI publishing (G5) has a draft workflow file in `.github/workflows/` (can be in a feature branch).
5. The constitution gap analysis (2026-04-25) has been merged into this spec via v2 — principles XXII (Distribution Surface Integrity), XXIII (Provider Robustness), XXIV (Safety-Critical Defense-in-Depth), XXV (Live Test Cost Discipline), and XXVII (Operator-Configurable Tool Surface) are referenced where they govern specific gates. ✅ Done in v2.
6. Spec 066 (constitution v2.3.0 amendment package) lands AND the implementation PR editing `CONSTITUTION.md` lands BEFORE G8 (visibility flip) — public-facing repo must reflect the constitution that governed the work it ships.

## 8. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Secret in git history surfaces post-flip | High | G2 covers active checks; consider `git filter-repo` rewrite if any finding |
| Name change requested after G8 | Medium | G1 is explicitly blocking. Default-to-`conversus`-after-7-days locks the decision in one direction |
| PyPI namespace squat | Low | Reserve the name early — register a placeholder `conversus` package with a "coming soon" README well before G5 |
| External issue flood post-launch | Medium | Triage cadence in `CONTRIBUTING.md`; close-with-comment policy for off-topic |
| Paid features confused with OSS | High | README must clearly state "this is the OSS engine; paid solvers ship via `conversus-enhanced`" |

## 9. Post-launch obligations

After G9, the project takes on these standing commitments — failure to meet them eats the goodwill earned by going public:

1. **Issue response SLA**: acknowledge within 7 days, even if the response is "we'll get to it."
2. **Security disclosure SLA**: respond to `SECURITY.md` reports within 72 hours.
3. **Release cadence**: at least one tagged release per quarter, even if patch-only.
4. **CI green on main**: a red main is not acceptable for >24 hours.
5. **Dependency updates**: `dependabot` or equivalent must run; security-flagged updates merged within 14 days.

## 10. Open questions

- Q1: Should we register `conversus` on PyPI **before** G8 (visibility flip) to prevent squatting? Argument for: low effort, high protection. Argument against: registering a public PyPI package while the repo is private is a partial-publication that might confuse anyone discovering the PyPI page.
- Q2: Trusted Publishing requires a configured "environment" with restricted access. Who's the maintainer with the credentials to configure this? Currently sole maintainer is the repo owner.
- Q3: Does `conversus-enhanced` (private) need any updates to align with the public release? E.g., does its `git+ssh://` dependency reference need to change to a PyPI version reference once `conversus` publishes?

## 11. Decisions (filled in as gates close)

| Date | Gate | Decision | Filed by |
|---|---|---|---|
| _pending_ | G1 (name) | _TBD — defaults to `conversus` if not filed by 2026-05-02_ | |
| _pending_ | G2 (security) | _TBD — gitleaks run not yet performed_ | |

## 12. References

- Spec 052 — Open Source Extraction (content shape)
- Spec 053 — Public CI Pipeline (CI mechanics)
- Spec 054 — Public Documentation (README content)
- CONSTITUTION.md (governance principles)
- `deliberations/constitution-gap-analysis-2026-04-25/` — deliberation that produced the v2.3.0 amendment package referenced throughout v2
- `CONSTITUTIONAL_CONVERSATIONS.md` — entry: 2026-04-25 (governance log)
- Spec 066 — Constitution v2.3.0 Amendment Package (proposes the principles this spec references)
- PyPI Trusted Publishing: https://docs.pypi.org/trusted-publishers/ (referenced for G5)
