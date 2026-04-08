# Cooperative Arbitration — Round 1 Inter-Round

**Arbiter**: conversus-constitution
**Influence**: advisory

---

### Process Note

- **Trigger**: `disputes_remain` — 4 disputes remain from the Round 1 synthesis.
- **Agents**: functional-typing, integration-architect, devils-advocate
- **Mode**: cooperative deliberation with advisory subject arbitration
- **Influence level**: advisory — agents are not bound by these positions and may freely propose alternatives

### Decision Framework

The following principles from the grounding document (spec 011) are relevant to the remaining disputes:

- **Thin orchestration principle** (spec L19): "Gates are a thin orchestration layer." The gate reads config, generates conversus.yml, invokes the engine, parses results, reports verdict.

- **Engine independence constraint** (spec L56-57, L100): "Gates MUST NOT modify the conversus engine." Gate improvements do not require engine changes.

- **CI/CD-friendly constraint** (spec L102): "Must be CI/CD-friendly. Exit codes, structured output, no interactive prompts during execution (configuration is declarative)."

- **Machine-readable output requirement** (spec L47-49): Exit codes and gate-result.md must be machine-parseable for pipeline consumption.

- **Declarative configuration** (spec L102): "Configuration is declarative." No interactive prompts during execution.

- **FR-004 optional fields** (spec L37): "Each gate MAY define: mode, rounds, arbiter, output." The spec uses MAY, indicating optional configuration.

### Advisory Opinions

#### Dispute: Gate config schema — stagnation and iterations

**Positions:**
- **integration-architect**: Stagnation and iterations should be in the gate config schema. Gate configs should be self-documenting. `rounds: 2` without visible stagnation config creates invisible default dependency.
- **functional-typing**: Minimum viable schema. The run engine defaults handle stagnation and iterations.

**Synthesizer's assessment:** Include stagnation, defer iterations.

**Opinion:** The synthesizer's split recommendation is well-reasoned. The thin orchestration principle supports minimalism, but the CI/CD-friendly constraint supports explicitness. Stagnation is a behavioral modifier that changes whether a multi-round gate terminates early. Users configuring `rounds: 2` in a CI/CD pipeline should see whether stagnation detection is active. Iterations, by contrast, has a universally sensible default (1) that does not need visibility.

I agree with the synthesizer: include `stagnation` as an optional field, defer `iterations`. This is consistent with FR-004's use of "MAY" — stagnation is an optional field that, when relevant (rounds > 1), materially affects behavior and should be visible.

**Required changes:** N/A (advisory — for agent consideration in Round 2).

---

#### Dispute: Gate bypass (--force-pass) in spec 011

**Positions:**
- **devils-advocate + integration-architect**: Include `--force-pass --force-pass-reason "reason"` in spec 011. It is a gate feature (affects gate-result.md), not an operational concern.
- **functional-typing**: Defer to follow-up spec. `pass: always` already provides non-blocking behavior.

**Synthesizer's assessment:** Include bypass. Bilateral support. Low scope addition.

**Opinion:** The CI/CD-friendly constraint (spec L102) is relevant here. Real CI/CD pipelines need emergency overrides — this is a well-established pattern. The spec says "configuration is declarative," which `--force-pass` does not violate (it is an invocation flag, not config). The key question is whether `pass: always` is sufficient.

`pass: always` serves a different purpose: it configures a gate as permanently advisory. `--force-pass` serves a temporary need: bypass a normally-blocking gate for a specific run. These are genuinely different capabilities. However, I note that bypass adds schema complexity to gate-result.md (new fields: Bypass, Bypass Reason) and a new flag to the CLI surface.

My opinion: bypass is appropriate for spec 011 given its low scope. But functional-typing's concern about scope creep is legitimate — if bypass opens the door to other operational flags, the gate's simplicity erodes. The spec should include bypass but explicitly state: "Bypass is the sole operational override. Additional operational concerns (timeout, resource limits) are CI/CD runner responsibilities."

**Required changes:** N/A (advisory).

---

#### Dispute: Execution metadata in gate-result.md

**Positions:**
- **devils-advocate**: Include `## Execution` section with agent count, rounds, mode.
- **No explicit opposition** from other agents.

**Synthesizer's assessment:** Accept as P3.

**Opinion:** The machine-readable output requirement (spec L47-49) supports structured metadata. The gate-result.md is a new schema — this is the right time to include diagnostic fields. The cost is minimal (3 lines in a structured document). The value is real for CI/CD operators tuning gate configurations.

I agree with the synthesizer's P3 assessment. This is useful but not blocking.

**Required changes:** N/A (advisory).

---

#### Dispute: Stagnation only (without iterations)

**Positions:** Sub-dispute resolved by the synthesizer's recommendation to include stagnation, defer iterations.

**Opinion:** Agree with the synthesizer's resolution. This is not an independent dispute but a consequence of the stagnation/iterations dispute resolution.

**Required changes:** N/A (advisory).

---

### Considerations for Next Round

1. **Stagnation in gate config** (from Dispute 1): Agents should consider whether the advisory opinion strengthens the case for inclusion. integration-architect's core argument (self-documenting configs) is sound. functional-typing may accept inclusion given that the arbitration supports it and the scope addition is minimal (one optional field with a sensible default).

2. **Gate bypass** (from Dispute 2): The bilateral support (2 of 3 agents) plus advisory arbitration support makes this likely to converge in Round 2. functional-typing should consider whether their scope-creep concern is addressed by explicitly limiting bypass as the sole operational override.

3. **Execution metadata** (from Dispute 3): This is likely to converge as P3 given no explicit opposition. Agents should either endorse or explicitly object in Round 2.

### Confidence Assessment

| Dispute | Opinion | Confidence | Basis |
|---------|---------|------------|-------|
| Stagnation + iterations | Include stagnation, defer iterations | High | Grounded in FR-004 (MAY), CI/CD constraint, thin orchestration principle |
| Gate bypass | Include in spec 011 with scope boundary | Medium | Grounded in CI/CD constraint, but functional-typing's scope concern is legitimate |
| Execution metadata | Accept as P3 | High | Grounded in machine-readable output requirement, no opposition |
| Stagnation-only (sub-dispute) | Resolved by parent dispute | High | Derivative resolution |

Overall, the deliberation quality is strong. All three agents made substantive concessions in Phase 3, indicating genuine engagement. The remaining disputes are scope decisions (what belongs in spec 011 vs. follow-up), not fundamental disagreements about gate design. Round 2 should focus on convergence: can functional-typing's scope concerns be addressed with explicit boundaries?
