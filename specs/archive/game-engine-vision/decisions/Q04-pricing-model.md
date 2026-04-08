# Q04: Pricing model

**Status**: Deferred — research complete, decision pending

---

## Context

Open Question #4 from spec 007 Section 13:

> "Per-run credit? Monthly subscription? Per-plugin? Free for open-source projects?"

## Constraints From Prior Decisions

- **Q05 (no telemetry, local-only)**: Rules out per-run credits, usage-based models, and any pricing that requires network calls at runtime.
- **Two paid packages**: `conversus-embeddings` (Tier 1, lighter) and `conversus-nashopt` (Tier 2, heavier).
- **~29 curated objective function templates** (Q06) ship with the paid tier.

## Research: Comparable Pricing Models

### Most Analogous: Sidekiq (OSS core + paid local packages)

- Free `sidekiq` gem on public RubyGems
- Paid `sidekiq-pro` ($99/mo) and `sidekiq-enterprise` ($269/mo) on private gem server
- Gating: HTTP Basic Auth credentials on private registry. No runtime license check.
- Per-organization pricing, not per-seat
- Lapsed subscription = can't download new versions, existing installs continue

### Also Relevant: AG Grid (local-only license key)

- Free Community (MIT), Enterprise $995-$1,295/dev/year
- License key validated 100% locally, zero network calls
- Key encodes expiration and product entitlements
- No telemetry

### Also Relevant: Nx Powerpack (repo-committed license)

- License file written to `.nx/powerpack/license.ini`, committed to repo
- All devs get access through version control
- No external API calls
- Free for open-source projects

### Market Context

- Pure game theory tools (Gambit, NashPy, nashopt) are all free/academic — no proven commercial market for game-theory developer tools
- Mathematical optimization tools (Gurobi, CPLEX) charge $285-$30K+/yr but target enterprise/academic markets
- Developer CLI tools with paid tiers: $19-$60/user/mo (Copilot, Cursor, GitLab)
- Local-only tools charge less than cloud tools due to zero marginal cost

### Models Ruled Out

| Model | Example | Why Not |
|-------|---------|---------|
| Per-run credits | Cursor, Copilot | Requires network calls (violates Q05) |
| Cloud-gated features | PostHog, dbt Cloud | Conversus is fully local |
| Usage-based | Augment Code | Requires telemetry (violates Q05) |
| BSL/legal gating | Terraform | Heavy, hard to enforce |

## Preliminary Recommendation (Not Decided)

**Sidekiq model**: private PyPI for distribution, per-org flat pricing, two tiers matching plugin packages.

| Tier | Package | Strawman Price |
|------|---------|---------------|
| Embeddings | `conversus-embeddings` | ~$29-49/mo per org |
| Nash Engine | `conversus-nashopt` | ~$99-149/mo per org |
| Bundle | Both | ~$119-179/mo per org |

Free for open-source projects and academic use.

**Distribution infrastructure options:**
- Self-hosted private PyPI (Sidekiq approach): Apache + Basic Auth. Cheapest, simplest.
- Keygen ($49-129/mo): License management + private package hosting. More sophisticated.
- Gemfury ($9+/mo): Simple private PyPI hosting, no license management.

## Why Deferred

Pricing is a product/market decision that should be informed by adoption data, competitive landscape at launch time, and customer conversations. The architectural decisions (local-only, no telemetry, pip-installable) constrain the model to credential-gated or license-key-gated distribution — the specific price points and tier structure should be decided closer to launch.

## Sources

- Sidekiq: sidekiq.org, Commercial FAQ, Mike Perham blog
- AG Grid: ag-grid.zendesk.com (license validation FAQ)
- Nx Powerpack: nx.dev/powerpack
- Gurobi: gurobi.com/academia
- IBM CPLEX: $285/user/mo developer subscription
- Keygen: keygen.sh/pricing
- Gemfury: fury.co/pricing
- GitHub Copilot: $10-39/user/mo
- Cursor: $20-200/mo
