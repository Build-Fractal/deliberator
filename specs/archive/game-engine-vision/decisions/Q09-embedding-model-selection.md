# Q09: Embedding model selection — bundled or user-configured?

**Status**: Decided
**Decision**: Bundled default, user-overridable (Option C)

---

## Context

Open Question #9 from spec 007 Section 13:

> "Should conversus-embeddings ship with a specific MTEB model, or let users configure their own?"

## Decision

**Ship a proven MTEB top-10 default. Users override in plugin config for domain-specific needs.**

```yaml
plugins:
  - name: convergence-scorer
    package: conversus-embeddings
    config:
      model: null  # default: top MTEB model shipped with package
      # model: "medical-domain-model"  # override for specialized domains
```

## Rejected Alternatives

- **Bundled only** rejected: doesn't support domain-specific models (medical, legal)
- **User-configured only** rejected: unnecessary setup friction for the common case
