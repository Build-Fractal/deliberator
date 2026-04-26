### Executive Summary

The CONSTITUTION.md v2.3.0 amendment introduces six new principles (XXII-XXVII) and extends two existing principles (IX, XI) to address distribution integrity, provider robustness, safety-critical systems, test discipline, meta-testing, and operator configuration. From a wording precision perspective, the amendment demonstrates strong use of RFC 2119 keywords (MUST/SHOULD/MAY) with generally clear operational definitions. However, several principles contain imprecise terminology that could lead to enforcement ambiguity, particularly around boundary definitions ("real-world cost," "source code changes," "parametrized set of capabilities"). The amendment maintains good structural consistency with existing principles while introducing necessary technical precision in areas like token consumption reporting and defense-in-depth requirements. **The most critical issue is the lack of precise operational boundaries in Principle XXV's "real-world cost" definition, which could lead to inconsistent test categorization.**

### Alignment

- **Consistent MUST/SHOULD/MAY usage** (`L447-523`): All new principles correctly use MUST for non-negotiable requirements, with particularly strong examples in XXII's "MUST satisfy three invariants" and XXIV's "MUST implement three-layer defense."

- **Structured enumeration** (`L447-523`): Each principle follows the established pattern of numbered requirements (three invariants, four guarantees, four rules), providing clear checklists for compliance verification.

- **Specific technical terminology** (`L466-480`): Principle XXIII uses precise technical terms like "HTTP 429," "exponential backoff with jitter," and "subscription-level concurrency limits" that eliminate ambiguity.

- **Operational test definitions** (`L543-559`): The IX extension provides a concrete operational test for distinguishing shape tests from behavior tests with specific examples.

- **Clear asymmetric permissions** (`L522-526`): Principle XXVII correctly uses "MAY restrict" vs "MAY NOT extend" to establish precise operator boundaries.

### Missed Opportunities

- **Boundary definition precision**: The constitution lacks precise definitions for terms like "real-world cost" (`L495`) and "source code changes" (`L520`), creating enforcement ambiguity that could undermine compliance checking.

- **Quantitative thresholds**: Principles like XXV mention "measurable cost" without defining measurement units or thresholds, missing opportunities for objective compliance criteria.

- **Exception handling patterns**: The constitution doesn't establish consistent patterns for documenting SHOULD violations, leaving gap in how documented exceptions are structured and validated.

- **Cross-principle consistency checking**: No mechanism ensures that operational definitions across principles don't conflict (e.g., what constitutes a "change" in different contexts).

- **Enforcement mechanism specification**: While principles define requirements clearly, they don't specify how violations are detected or measured programmatically.

- **Scope boundary markers**: Principles lack explicit statements about what is NOT covered, creating potential for scope creep during enforcement.

### Off-Base Assumptions

- **Universal RFC 2119 interpretation**: The constitution assumes consistent interpretation of MUST/SHOULD/MAY across all contributors without establishing project-specific refinements of these terms in technical contexts.

- **Obviousness of technical boundaries**: Principle XXII assumes "packaged Python directory" (`L450`) is unambiguous, but Python packaging has multiple valid organizational patterns that could create confusion.

- **Self-evident operational definitions**: Several principles assume terms like "capabilities" (`L511`) and "real-world cost" (`L495`) are operationally obvious when they require precise scoping.

### Actionable Recommendations

1. **Define real-world cost precisely** (Priority: P1)
   - **Current state**: "Tests that consume API credits, spawn subprocesses, or otherwise incur real-world cost" (`L495`)
   - **Proposed change**: Add specific definition: "Real-world cost includes: API credits charged to account, subprocess spawning with measurable CPU/memory allocation, network I/O to external services, persistent storage writes >1MB"
   - **Rationale**: Vague cost definition leads to inconsistent test categorization and disputed @pytest.mark.live applications
   - **Risk if ignored**: Test suite organization becomes arbitrary, CI costs unpredictable

2. **Clarify source code change boundaries** (Priority: P1)
   - **Current state**: "without source code changes" (`L520`)
   - **Proposed change**: "without modifying files tracked in version control under src/, excluding configuration files with .json, .yml, .toml, .env extensions"
   - **Rationale**: Configuration vs code boundary determines operator autonomy scope
   - **Risk if ignored**: Operator/developer responsibility becomes disputed territory

3. **Operationalize parametrized capabilities** (Priority: P2)
   - **Current state**: "parametrized set of capabilities" (`L511`)
   - **Proposed change**: "capabilities registered in conversus/registry/ or declared in schema/modes/*.yml, schema/variables.yml"
   - **Rationale**: Precise capability definition enables automated meta-test enforcement
   - **Risk if ignored**: Meta-testing principle becomes selectively applied

4. **Specify packaged Python directory** (Priority: P2)
   - **Current state**: "packaged Python directory" (`L450`)
   - **Proposed change**: "Python packages listed in [tool.hatch.build.targets.wheel.packages] or automatically discovered under src/"
   - **Rationale**: Python packaging allows multiple valid structures; precision prevents force-include disputes
   - **Risk if ignored**: Distribution integrity violations go undetected

5. **Add measurement units for cost thresholds** (Priority: P2)
   - **Current state**: "measurable cost" (`L500`)
   - **Proposed change**: "cost >$0.01 USD equivalent or >10 seconds wall-clock time or >100MB disk I/O"
   - **Rationale**: Quantitative thresholds enable objective live test categorization
   - **Risk if ignored**: "Measurable" becomes subjective judgment call

6. **Define exception documentation format** (Priority: P2)
   - **Current state**: SHOULD statements lack exception documentation requirements
   - **Proposed change**: Add: "SHOULD violations MUST include inline comment: `# SHOULD-EXCEPTION: [rationale]`"
   - **Rationale**: Consistent exception documentation enables compliance auditing
   - **Risk if ignored**: SHOULD violations become invisible technical debt

7. **Establish scope exclusion statements** (Priority: P3)
   - **Current state**: Principles define positive requirements only
   - **Proposed change**: Add "Out of scope:" subsection to each principle listing what is NOT covered
   - **Rationale**: Explicit scope boundaries prevent enforcement mission creep
   - **Risk if ignored**: Principles gradually expand beyond original intent

8. **Add cross-principle consistency check** (Priority: P3)
   - **Current state**: No mechanism prevents conflicting operational definitions
   - **Proposed change**: Add constitutional amendment requirement: "New principles MUST include consistency check against existing operational definitions"
   - **Rationale**: Prevents contradictory requirements across principles
   - **Risk if ignored**: Constitution becomes internally inconsistent over time

### Referenced Documentation

No external documentation files were provided for this wording-precision review. All observations are based on direct analysis of the target constitution text and general technical writing precision principles.