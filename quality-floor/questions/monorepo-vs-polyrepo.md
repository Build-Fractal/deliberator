# Monorepo vs Polyrepo Decision

## Question

Should a team of 15 engineers with 3 services use a monorepo or polyrepo?

## Context

We are a mid-stage startup with 15 engineers split across three squads, each owning one core service: an API gateway (Node.js/Express), a data processing pipeline (Python/FastAPI), and a real-time notification service (Go). The services communicate via gRPC and share 4 protobuf schema files. We deploy to Kubernetes on AWS EKS.

Currently we have 3 separate repositories. Cross-service changes (especially protobuf schema updates) require coordinating PRs across repos, and we have had two production incidents in the last quarter caused by schema version mismatches that passed CI in isolation but broke at integration. Our CI runs take 8-12 minutes per repo. We have no dedicated platform/infra team — each squad manages its own CI and deployment pipeline.

We are evaluating whether to consolidate into a monorepo (using Nx, Turborepo, or Bazel for build orchestration) or to stay with polyrepo and invest in better cross-repo tooling (a shared schema registry, contract testing, and a release coordination bot). The decision needs to account for: developer experience during the transition, CI/CD complexity, code ownership boundaries, and the fact that we plan to grow to 25-30 engineers in the next 12 months.

## Decision Criteria

- Migration cost and timeline
- Impact on developer velocity (daily workflow)
- CI/CD reliability and speed
- Code ownership clarity as the team scales
- Risk of the two approaches diverging from our growth trajectory
