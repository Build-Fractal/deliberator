# Quality Floor

Reference artifacts and test fixtures for validating that deliberator multi-agent deliberation output is structurally differentiated from single-model responses.

## Purpose

This directory contains:
1. **Reference deliberation outputs** with known quality characteristics (passing and failing)
2. **Structural pattern definitions** for programmatic quality gate checking
3. **A worked side-by-side example** comparing deliberator output to single-model responses
4. **Deliberator configs and input questions** used to generate the reference outputs
5. **Single-model baseline responses** for the same questions as controls

These artifacts serve two purposes:
- **S01 (Quality Floor & Worked Example):** Empirically validate the deliberator product premise — that 2-agent cooperative output is structurally differentiated from single-model responses.
- **S02 (Quality Gate Checker):** Provide test fixtures with known pass/fail characteristics for the automated quality checker.

## Directory Structure

```
quality-floor/
├── README.md                           # This file
├── worked-example.md                   # Side-by-side comparison with 6 annotated structural differences
├── structural-definitions.md           # Formal pattern definitions with regex for quality gates
├── configs/                            # deliberator.yml configs used to generate outputs
│   ├── monorepo-vs-polyrepo.yml
│   ├── lease-vs-buy.yml
│   └── factual-capital.yml
├── questions/                          # Input question files referenced by configs
│   ├── monorepo-vs-polyrepo.md
│   ├── lease-vs-buy.md
│   └── factual-capital.md
├── single-model-responses/             # Single-model Claude responses (controls)
│   ├── monorepo-vs-polyrepo.md
│   └── lease-vs-buy.md
└── reference-outputs/                  # Deliberation outputs organized by expected quality
    ├── passing/                        # Outputs that PASS the quality floor
    │   ├── monorepo-vs-polyrepo/       # Dev question — full deliberation
    │   └── lease-vs-buy/               # Consumer question — full deliberation
    └── failing/                        # Outputs that FAIL the quality floor
        └── factual-capital/            # Factual question — negative control
```

## Reference Outputs

### Passing Fixtures

These deliberation outputs pass both quality gates (Substantive Disagreement + Agent Attributions).

#### `passing/monorepo-vs-polyrepo/`

- **Question:** "Should a team of 15 engineers with 3 polyglot services use a monorepo or polyrepo?"
- **Agents:** `philosophy/pragmatist` + `role/devils-advocate`
- **Mode:** Cooperative
- **Expected quality characteristics:**
  - **Substantive Disagreement: PASS** — 3 named disputes within `DISPUTES_BEGIN/END` block (Deferral Timeline Shape, Migration Investment Proportionality, Shared-Repo Escape Hatch Scope)
  - **Agent Attributions: PASS** — 2 distinct agents with attributed positions in Recommendation Scorecard, 9 concessions with phase citations, multiple cross-review challenge attributions
  - **Structural markers present:** Recommendation Scorecard with Agent/Challenged By columns, Dangerous Contradictions with resolution tracking, Convergence Strength assessment, Key Concessions with citation chains, DISPUTES_BEGIN/END delimiters

#### `passing/lease-vs-buy/`

- **Question:** "Should I lease or buy a mid-size sedan?"
- **Agents:** `philosophy/pragmatist` + `role/devils-advocate`
- **Mode:** Cooperative
- **Expected quality characteristics:**
  - **Substantive Disagreement: PASS** — 4 named disputes within `DISPUTES_BEGIN/END` block (Spec Directional Neutrality, Residual-Value Uncertainty Band, Lease-Favourable Lifestyle Scenarios, Insurance Cost Delta Inclusion)
  - **Agent Attributions: PASS** — 2 distinct agents with attributed positions in Recommendation Scorecard, 9 concessions with phase citations, multiple cross-review challenge attributions
  - **Structural markers present:** Same full synthesis structure as monorepo (scorecard, contradictions, convergence, concessions, dispute block)

### Failing Fixtures

These deliberation outputs fail the quality floor — they are expected to fail at least one quality gate.

#### `failing/factual-capital/`

- **Question:** "What is the capital of France?"
- **Agents:** `philosophy/pragmatist` + `role/devils-advocate`
- **Mode:** Cooperative
- **Why it fails:** This is a trivially factual question with a single correct answer (Paris). Agents cannot genuinely disagree on the answer, so the synthesis contains **zero substantive disputes**. The Remaining Disputes section explicitly states "None." This confirms that agents don't manufacture disagreement on factual questions.
- **Expected quality characteristics:**
  - **Substantive Disagreement: FAIL** — 0 disputes (agents both agree on the factual answer)
  - **Agent Attributions: PASS** — 2 distinct agents are still present with attributed positions and concessions (the deliberation structure exists, but there's nothing to disagree about)
  - **Quality Floor: FAIL** — fails the combined gate because substantive disagreement is missing
- **Diagnostic value:** This output serves as a negative control. If the quality checker marks it as passing, the checker has a false-positive bug — it's accepting manufactured or trivial disagreement.

## How S02 Should Use These Fixtures

The S02 quality gate checker should:

1. **Run passing fixtures through the checker expecting PASS:**
   - `quality-floor/reference-outputs/passing/monorepo-vs-polyrepo/summary/final.md` → expect quality floor PASS
   - `quality-floor/reference-outputs/passing/lease-vs-buy/summary/final.md` → expect quality floor PASS

2. **Run failing fixtures through the checker expecting FAIL:**
   - `quality-floor/reference-outputs/failing/factual-capital/summary/final.md` → expect quality floor FAIL (substantive disagreement gate fails)

3. **Verify specific gate results:**
   - Passing outputs should pass **both** Substantive Disagreement and Agent Attributions gates
   - Factual-capital should **fail** Substantive Disagreement but **pass** Agent Attributions

This creates a basic test matrix:
| Fixture | Substantive Disagreement | Agent Attributions | Quality Floor |
|---------|--------------------------|-------------------|---------------|
| monorepo-vs-polyrepo | ✅ PASS | ✅ PASS | ✅ PASS |
| lease-vs-buy | ✅ PASS | ✅ PASS | ✅ PASS |
| factual-capital | ❌ FAIL | ✅ PASS | ❌ FAIL |

## Related Files

- **[structural-definitions.md](structural-definitions.md)** — Formal pattern specifications with Python regex patterns, detection algorithms, examples from real output, and thresholds for both quality gates.
- **[worked-example.md](worked-example.md)** — Side-by-side comparison with 6 annotated structural differences between deliberator output and single-model responses.

## Inspection Commands

```bash
# List all completed deliberations
find quality-floor/reference-outputs -name 'final.md'

# Count dispute markers per synthesis
grep -c "Dispute:" quality-floor/reference-outputs/passing/*/summary/final.md
grep -c "Dispute:" quality-floor/reference-outputs/failing/*/summary/final.md

# Verify synthesis depth
wc -l quality-floor/reference-outputs/passing/*/summary/final.md
wc -l quality-floor/reference-outputs/failing/*/summary/final.md

# Check structural marker presence
grep -l "DISPUTES_BEGIN" quality-floor/reference-outputs/passing/*/summary/final.md
grep -l "Recommendation Scorecard" quality-floor/reference-outputs/passing/*/summary/final.md

# Verify negative control (should return 0 or "None")
grep "Dispute:" quality-floor/reference-outputs/failing/factual-capital/summary/final.md
```
