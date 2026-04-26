I need to read the target files and relevant documentation to provide a proper packaging-distribution perspective review.

### Executive Summary

The CONSTITUTION.md codifies core principles for the conversus codebase, establishing contracts for spec-driven development, stable interfaces, and architectural invariants. From a packaging-distribution perspective, the constitution effectively captures several distribution-relevant principles but misses critical packaging invariants that the recent PRs (#11, #13, #14) have demonstrated are essential for system integrity. The constitution's emphasis on Single Source of Truth (Principle XI) and No Dead Infrastructure (Principle XII) provides strong foundation for packaging discipline, but lacks explicit coverage of wheel contents validation, cross-surface artifact projection, and deployment-time configurability. The most important recommendation is establishing a Distribution Surface Integrity principle requiring single-source versioning, explicit force-include declarations, and end-to-end distribution testing.

### Alignment

- **Single Source of Truth enforcement** (L241-265): Principle XI's requirement that "every piece of information MUST have exactly one authoritative source" directly supports the packaging pattern where `pyproject.toml [project] version` serves as the canonical version source projected to `manifest.json` via build scripts. [pyproject.toml, L4-6; desktop-extension/build.sh, L35-54]

- **No Dead Infrastructure validation** (L266-289): Principle XII's requirement that "every provisioned capability MUST have at least one consumer" aligns with wheel force-include discipline, preventing packaging of unused files that would violate the consumer requirement. [pyproject.toml, L115-126; capabilities.py, L721-736]

- **Functional Programming constraints** (L164-218): Principle IX's mandate for explicit typing and stateless functions supports the capability registry pattern that drives cross-surface artifact projection, ensuring deterministic build outputs. [capabilities.py, L1-36; scripts/build-surfaces.py, L93-103]

- **Stable Interfaces protection** (L47-71): Principle II's breaking change registry covers reference file paths and dispatch table subcommands, which extends to distribution artifacts that must maintain API compatibility across surfaces. [desktop-extension/manifest.json, L141-158]

### Missed Opportunities

- **Distribution Surface Integrity**: The constitution lacks any principle governing wheel contents validation or build-time artifact projection. PR #11's missing `mcp_server.py` + `capabilities.py` represents a systematic distribution failure that constitutional guidance could prevent. The force-include pattern and version sync mechanisms are critical infrastructure with no constitutional backing. Reference: [pyproject.toml, L115-126; desktop-extension/build.sh, L32-54]. Impact: high.

- **Cross-Surface Artifact Projection**: No principle mandates that distribution surfaces derive from authoritative registries. The capability registry drives CLI, MCP, plugin skills, and MCPB manifest generation, but this projection discipline lacks constitutional protection against drift. Reference: [capabilities.py, L717-736; scripts/build-surfaces.py, L58-91]. Impact: high.

- **Deployment-Time Configurability**: Missing principle requiring operator-configurable tool surfaces without code changes. The `CONVERSUS_DISABLED_TOOLS` pattern and `user_config` schemas provide runtime configuration, but lack constitutional mandate for deployment-time tool surface control. Reference: [desktop-extension/manifest.json, L52-97; mcp_server.py, L79-85]. Impact: medium.

- **Build-Time Validation Requirements**: No constitutional requirement for distribution artifact validation. The build scripts implement Python compilation checks and meta-tests, but this validation discipline isn't constitutionally mandated. Reference: [scripts/build-surfaces.py, L140-167; linter/test_mcp_prompts.py, L94-100]. Impact: medium.

- **Version Projection Discipline**: While Single Source of Truth covers data duplication, it doesn't explicitly require version fields in surface artifacts to derive from `pyproject.toml`. The build-time sync pattern lacks constitutional backing. Reference: [desktop-extension/build.sh, L35-54; desktop-extension/manifest.json, L5]. Impact: medium.

- **Registry-First Capability Declaration**: Missing principle that capabilities must be declared in the registry before surface projection. The `CAPABILITIES` list serves as authoritative declaration, but constitutional protection against bypass is absent. Reference: [capabilities.py, L717-736; deliberations/constitution-gap-analysis-2026-04-25/round-1/recent-changes.md, L120-127]. Impact: low.

- **Meta-Test Coverage Requirements**: No principle requiring drift guard tests for parametrized surfaces. The MCP prompts test includes meta-test asserting coverage of all 7 prompts, but this pattern lacks constitutional mandate. Reference: [linter/test_mcp_prompts.py, L94-100]. Impact: low.

- **Package Boundary Enforcement**: No constitutional guidance on what belongs in wheels versus external dependencies. The force-include pattern for repo-root modules suggests unclear boundaries that constitutional guidance could clarify. Reference: [pyproject.toml, L120-126]. Impact: low.

### Off-Base Assumptions

- **Distribution testing scope** (implied throughout): The constitution assumes that testing requirements apply only to execution logic, but distribution artifacts require equal testing rigor. Build-time validation and end-to-end distribution testing are as critical as runtime validation for system integrity.

- **Artifact projection timing** (Principle XI, L247-258): The constitution treats single source of truth as a static constraint, but distribution artifacts require build-time projection discipline where timing of derivation matters. Version sync must happen before packaging, not just "when two sources disagree."

### Actionable Recommendations

1. **Add Distribution Surface Integrity Principle** (Priority: P1)
   - **Current state**: Constitution lacks any principle governing distribution artifact validation or wheel contents integrity.
   - **Proposed change**: Extend Principle XI with distribution-specific requirements: "Distribution artifacts MUST derive from authoritative sources. Version fields in surface artifacts (manifest.json, plugin.json) MUST be projected from pyproject.toml [project] version. Wheel contents MUST be explicit via force-include declarations. Distribution paths MUST be validated end-to-end."
   - **Rationale**: PR #11's missing wheel contents and PR #13's version drift demonstrate immediate user-visible failures when distribution integrity lacks constitutional protection. [deliberations/constitution-gap-analysis-2026-04-25/round-1/recent-changes.md, L73-105]
   - **Risk if ignored**: Continued distribution failures affecting every deployment path, user-reported broken installs, and systematic packaging drift.

2. **Mandate Cross-Surface Artifact Projection** (Priority: P1)
   - **Current state**: Line 247-258 covers data duplication but doesn't require surface artifacts to derive from registries.
   - **Proposed change**: Add to Principle XI: "Distribution surface files (CLI commands, MCP tools, plugin skills, MCPB manifest tools) MUST be generated from capability registries, not hand-maintained."
   - **Rationale**: The projector pattern prevents surface drift but lacks constitutional protection. [scripts/build-surfaces.py, L58-91; capabilities.py, L717-736]
   - **Risk if ignored**: Surface artifacts diverge from registry truth, breaking the single-source-of-truth guarantee across distribution channels.

3. **Establish Build-Time Validation Requirements** (Priority: P2)
   - **Current state**: Constitution mentions runtime validation but ignores build-time validation needs.
   - **Proposed change**: Add new principle: "Build artifacts MUST be validated before distribution. Generated Python surfaces MUST pass compilation checks. Meta-tests MUST verify coverage completeness for parametrized surfaces."
   - **Rationale**: Build-time validation prevents distribution of broken artifacts. [scripts/build-surfaces.py, L140-167; linter/test_mcp_prompts.py, L94-100]
   - **Risk if ignored**: Broken artifacts reach users, distribution channels ship non-functional packages.

4. **Require Deployment-Time Configurability** (Priority: P2)
   - **Current state**: No constitutional mandate for operator-configurable tool surfaces.
   - **Proposed change**: Add principle: "Deployment-time tool surfaces MUST be configurable without code changes. Environment variables and configuration schemas MUST control runtime tool availability."
   - **Rationale**: Operator control over tool exposure is essential for enterprise deployment. [desktop-extension/manifest.json, L90-96; mcp_server.py, L79-85]
   - **Risk if ignored**: Deployment flexibility constrained, operators cannot restrict tool surfaces for security or policy compliance.

5. **Mandate Registry-First Capability Declaration** (Priority: P2)
   - **Current state**: Constitution doesn't require capabilities to be declared in registries before surface availability.
   - **Proposed change**: Add to Principle XII: "Capabilities MUST be declared in authoritative registries before surface projection. Surface-specific implementations MUST NOT bypass registry declaration."
   - **Rationale**: Registry-first prevents surface-specific capability drift. [capabilities.py, L717-736]
   - **Risk if ignored**: Capabilities appear on some surfaces but not others, breaking cross-surface consistency guarantees.

6. **Extend Enum Completeness to Surface Artifacts** (Priority: P3)
   - **Current state**: Principle XIII covers code-level enum completeness but ignores surface artifact consistency.
   - **Proposed change**: Add to Principle XIII: "When enums define surface-visible values (provider names, mode choices), ALL surface artifacts MUST use enum members consistently."
   - **Rationale**: Surface artifacts like provider choice lists must stay synchronized with code enums. [capabilities.py, L174-189]
   - **Risk if ignored**: Surface artifacts advertise capabilities that code doesn't recognize, causing runtime failures.

7. **Establish Package Boundary Discipline** (Priority: P3)
   - **Current state**: No constitutional guidance on package boundaries for repo-root modules.
   - **Proposed change**: Add principle: "Package boundaries MUST be explicit. Repo-root modules required for package functionality MUST use force-include declarations with documented rationale."
   - **Rationale**: Clear boundaries prevent accidental exclusions from distribution packages. [pyproject.toml, L120-126]
   - **Risk if ignored**: Unclear boundaries lead to missing distribution content, requiring post-release patches.

### Referenced Documentation

- `pyproject.toml` — sections/lines cited: L4-6, L115-126, L120-126
- `capabilities.py` — sections/lines cited: L1-36, L174-189, L717-736
- `scripts/build-surfaces.py` — sections/lines cited: L58-91, L93-103, L140-167
- `desktop-extension/build.sh` — sections/lines cited: L32-54, L35-54
- `desktop-extension/manifest.json` — sections/lines cited: L5, L52-97, L90-96, L141-158
- `linter/test_mcp_prompts.py` — sections/lines cited: L94-100
- `mcp_server.py` — sections/lines cited: L79-85
- `deliberations/constitution-gap-analysis-2026-04-25/round-1/recent-changes.md` — sections/lines cited: L73-105, L120-127