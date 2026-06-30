# API Reference

Auto-generated reference documentation for the `deliberator` Python package. Each page uses [mkdocstrings](https://mkdocstrings.github.io/) to render docstrings, type annotations, and signatures directly from source code.

## Packages

### Schemas

Core data models and processing pipelines for deliberation artifacts.

- [Construction Pipeline](schemas/construction.md) -- guided objective function construction (spec 014)
- [Feature Extraction](schemas/extraction.md) -- deterministic text-to-vector extraction (spec 015)
- [Feature Models](schemas/features.md) -- Pydantic models for deliberation feature vectors (spec 015)
- [Objective Templates](schemas/objectives.md) -- objective function validation models (spec 013)
- [Game Forms](schemas/game-forms.md) -- game theory form schemas and solvers (specs 012, 025)
- [Solver Validation](schemas/validation.md) -- validation flow for solver output review (spec 027)
- [Modes](schemas/modes.md) -- canonical mode definitions (8 modes)

### Plugins

Extensible plugin framework for adding custom scoring, optimization, and analysis to deliberations.

- [Plugin Framework](plugins/base.md) -- plugin ABC, hooks, state, and orchestration

### Domains

Domain-specific scoring plugins and persistence layer.

- [Domain Framework](domains/base.md) -- DomainPlugin ABC, scoring, and lifecycle
- [Domain Store](domains/store.md) -- persistence backends for domain records
- [Domain API Router](domains/api.md) -- FastAPI router factory for domain endpoints
