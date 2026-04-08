# Feature Specification: Documentation System

**Feature ID**: `031-docs-and-vercel-compliance`
**Created**: 2026-04-02
**Status**: Draft
**Depends On**: All implemented specs (001-038)

---

## 1. Feature Summary

Build a complete documentation system using mkdocs-material + mkdocstrings. Auto-generated API reference from docstrings, hand-written user and developer guides, OpenAPI 3 REST API docs, local dev server, and GitHub Pages deployment. Structured by future package boundaries for clean splitting.

---

## 2. Tooling

### Dependencies (dev group in pyproject.toml)
```
mkdocs-material>=9.5
mkdocstrings[python]>=0.24
mike>=2.0
mkdocs-swagger-ui-tag>=0.6
mkdocs-git-revision-date-localized-plugin>=1.2
```

### Commands
- `mkdocs serve` — local dev server with hot reload (port 8000)
- `mkdocs build` — static site to `site/`
- `mkdocs gh-deploy` — push to GitHub Pages
- `mike deploy 0.1 latest` — versioned deployment

---

## 3. Site Structure

```
docs/
  index.md                          ← landing page

  # User Guide (hand-written)
  user-guide/
    quickstart.md                   ← first deliberation in 30 seconds
    cli.md                          ← all CLI commands with examples
    guided-workflow.md              ← define → interests → mode → converge
    modes.md                        ← 8 modes in plain language
    config-reference.md             ← conversus.yml full schema
    mcp-setup.md                    ← editor integration
    sdk.md                          ← Python SDK usage
    web-interface.md                ← BYOK web app

  # Developer Guide (hand-written)
  developer-guide/
    architecture.md                 ← system overview, package boundaries
    building-plugins.md             ← Plugin ABC, hooks, produces/consumes
    building-domains.md             ← DomainPlugin, extractors, scaffolds
    building-templates.md           ← mode templates, dispute headings
    game-forms.md                   ← adding game forms + objective templates
    testing.md                      ← test patterns, fixtures
    contributing.md                 ← code style, PR process

  # API Reference (auto-generated from docstrings)
  api/
    engine.md                       ← engine package overview
    schemas/
      construction.md               ← ::: conversus.schemas.construction
      extraction.md                 ← ::: conversus.schemas.extraction
      features.md                   ← ::: conversus.schemas.features
      objectives.md                 ← ::: conversus.schemas.objectives
      game-forms.md                 ← ::: conversus.schemas.game_forms
      solvers.md                    ← ::: conversus.schemas.solvers
      validation.md                 ← ::: conversus.schemas.validation
      modes.md                      ← ::: conversus.schemas.modes
    plugins/
      base.md                       ← ::: conversus.plugins.base
      nashopt.md                    ← ::: conversus.plugins.nashopt
      optimizer.md                  ← ::: conversus.plugins.optimizer
      scenarios.md                  ← ::: conversus.plugins.scenarios
    domains/
      base.md                       ← ::: conversus.domains.base
      store.md                      ← ::: conversus.domains.store
      api.md                        ← ::: conversus.domains.api
      code-review.md                ← ::: conversus.domains.implementations.code_review

  # REST API (OpenAPI 3)
  rest-api/
    index.md                        ← embedded Swagger UI from openapi.json
    openapi.json                    ← exported from FastAPI
```

---

## 4. Functional Requirements

### Tooling
- **FR-001**: `mkdocs serve` MUST work locally with hot reload.
- **FR-002**: `mkdocs build` MUST produce a complete static site.
- **FR-003**: API reference MUST be auto-generated from Python docstrings via mkdocstrings.
- **FR-004**: Pydantic models MUST render fields, types, validators, and descriptions.
- **FR-005**: REST API MUST be documented via OpenAPI 3 JSON exported from FastAPI.
- **FR-006**: OpenAPI viewer MUST be embedded in the docs site (Swagger UI or Redoc).

### Content
- **FR-007**: User guide MUST cover all 8 modes, CLI, SDK, MCP, and web interface.
- **FR-008**: Developer guide MUST cover plugins, domains, templates, and game forms.
- **FR-009**: Every public module in conversus.schemas, conversus.plugins, and conversus.domains MUST have an API reference page.
- **FR-010**: Quickstart MUST get a user from clone to first deliberation in under 5 minutes of reading.

### Package Awareness
- **FR-011**: API reference pages MUST be organized by future package boundary (schemas/, plugins/, domains/).
- **FR-012**: Cross-package imports in docs MUST use the public API paths.

### Deployment
- **FR-013**: Docs MUST deploy to GitHub Pages via `mkdocs gh-deploy`.
- **FR-014**: Versioned docs via `mike` (latest + version tags).

---

## 5. Success Criteria

- **SC-001**: `mkdocs serve` runs locally, all pages render without errors.
- **SC-002**: API reference pages show function signatures, parameters, return types, and docstrings.
- **SC-003**: OpenAPI 3 JSON validates against the OpenAPI 3.0 specification.
- **SC-004**: A new user following quickstart.md completes their first deliberation.
- **SC-005**: `mkdocs build` produces zero warnings.
