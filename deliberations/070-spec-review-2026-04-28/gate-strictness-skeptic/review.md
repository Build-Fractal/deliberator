### Executive Summary

Spec 070 performs a criterion-by-criterion audit of three grandfathered constitutional principles (VI, X, XVI) against the v2.4.0 Constitutional Inclusion Criteria gate, concluding that all three should be migrated to operational guidance. However, the audit applies the gate criteria with excessive strictness, interpreting requirements more narrowly than the gate text supports and focusing on aesthetic framing rather than substantive enforcement mechanisms. Most critically, the spec's "SPLIT" verdict on Principle XVI reveals internal inconsistency—acknowledging that the principle's structural substrate passes both mechanical verification and falsifiability criteria while still classifying it as failing the gate. My assessment is that all three principles can pass the gate with reasonable interpretation of the criteria, particularly when considering that the gate requires concrete paths to mechanical verification, not perfect mechanical verification of every word. The most important recommendation is to recognize that Principle XVI's structural substrate already satisfies the gate requirements and should remain in the constitution without migration.

### Alignment

- **Path-to-mechanical-check interpretation** (L52-55): The spec correctly identifies that the v2.4.0 gate requires sketching a concrete path to mechanical checking, not implementing the check at amendment time. This aligns with the gate's practical intent to filter out inherently subjective principles while allowing enforceable rules that require implementation effort.

- **Mechanical substrate recognition** (L74-75): The spec accurately identifies that Principle X contains mechanically-checkable bullets (directory depth, file existence checks) beneath its aesthetic framing. This demonstrates proper parsing of principles as containing both enforceable and aspirational elements.

- **Structural enforceability analysis** (L92-96): The spec thoroughly documents Principle XVI's mechanically verifiable substrate (parameter pinning, plain-language pairing, shape determinism), providing concrete examples like "CI lint detecting re-entrant GapFiller.fill() calls." This analysis correctly identifies the principle's enforcement mechanisms.

- **Falsifiability precedent citation** (L100-101): The spec appropriately references the v2.3.2 amendment's explicit falsification criteria for Principle XVI, demonstrating that existing constitutional text already provides concrete violation patterns.

### Missed Opportunities

- **Gate interpretation breadth**: The spec applies a word-by-word strictness test rather than evaluating principles as coherent units with core enforceable claims and supporting design intent. The gate's "concrete enough that an engineer can sketch the check" language suggests unit-level evaluation, not clause-by-clause parsing. Impact: high.

- **Directory-scoped enforcement paths**: For Principle VI, the spec dismisses path-prefixed linting (L54-55) as "narrower than the principle states" without considering whether targeted enforcement of high-value directories (`skills/`, `presets/`, `templates/`) satisfies the gate's practical intent. Most principle violations occur in these structured directories, not general documentation. Impact: medium.

- **Subset mechanization precedent**: The spec acknowledges Principle X's mechanically-checkable bullets but doesn't explore whether partial mechanical verification satisfies the gate criteria. Constitutional principles routinely contain both enforceable rules and design guidance; the gate may not require mechanizing aesthetic elements. Impact: high.

- **SPLIT verdict resolution logic**: The spec creates a "SPLIT" category for Principle XVI but then defaults to "FAILS" without justifying why structural enforceability doesn't outweigh headline framing concerns. The gate criteria are conjunctive (all three must be met), but within each criterion, the principle should pass if its core claims are verifiable. Impact: high.

- **Precedent from existing principles**: The spec doesn't examine how other accepted principles handle similar design-intent framing alongside enforceable rules. If principles routinely contain aspirational language beyond their mechanically-verifiable core, this precedent should inform the strictness of gate application. Impact: medium.

- **Engineering sketch sufficiency**: The spec requires mechanical verification paths to be "concrete enough" but doesn't establish clear standards for sufficiency. A sketch that identifies specific lint rules, test patterns, and failure modes may be adequate even if it doesn't mechanize aesthetic judgments. Impact: medium.

### Off-Base Assumptions

- **Word-level vs. principle-level gate application** (L73-75, L94-95): The spec assumes the gate requires every element of a principle to be mechanically verifiable, treating aesthetic framing as disqualifying even when the principle's core enforcement mechanisms are concrete. The gate text evaluates principles as units, not individual clauses.

- **SPLIT verdicts automatically fail** (L107-108): The spec creates a "SPLIT" classification for Principle XVI, acknowledging its structural substrate passes both mechanical verification and falsifiability criteria, then concludes it "fails the gate." This conflates headline framing issues with substantive enforceability failures.

- **Migration as default for any gate tension** (L24-25): The spec assumes principles that create "two-tier constitution" concerns should migrate to operational guidance, without considering whether the gate criteria are satisfied by the principles' enforceable cores. This bias toward migration doesn't follow from the gate text.

### Actionable Recommendations

1. **Reclassify Principle XVI as PASS** (Priority: P1)
   - **Current state**: §4.3 gives XVI a "SPLIT" verdict, then concludes it "FAILS the gate" (L107-108).
   - **Proposed change**: Change verdict to PASS based on structural substrate passing 2 of 3 criteria. The mechanically-verifiable enforcement (parameter pinning, shape determinism, plain-language pairing) satisfies the gate requirements.
   - **Rationale**: The spec's own analysis proves XVI's core claims are mechanically verifiable and falsifiable. Headline framing about "user understanding" is design intent, not the enforceable rule.
   - **Risk if ignored**: Migrating a principle that actually passes the gate undermines the audit's credibility and creates precedent for over-strict gate application.

2. **Develop directory-scoped enforcement path for Principle VI** (Priority: P2)
   - **Current state**: §4.1 dismisses path-prefixed linting as "narrower than the principle states" (L54-55).
   - **Proposed change**: Evaluate whether CI hooks targeting `skills/`, `presets/`, `templates/` directories provide a "concrete enough" enforcement path per the gate's language.
   - **Rationale**: Most violations occur in structured directories where automation parsing is expected. Targeted enforcement may satisfy gate requirements even if broader principle framing requires judgment.
   - **Risk if ignored**: Migrating a principle with viable enforcement paths weakens the constitution's coverage of automation-critical file formats.

3. **Clarify subset mechanization standards for Principle X** (Priority: P2)
   - **Current state**: §4.2 acknowledges mechanically-checkable bullets but concludes principle fails because headline framing is aesthetic (L73-75).
   - **Proposed change**: Evaluate whether the mechanically-checkable subset (directory depth, file existence, error handling) satisfies Criterion 1 for the principle as a unit.
   - **Rationale**: Constitutional principles routinely contain both enforceable rules and aspirational guidance. The gate may not require mechanizing aesthetic elements if core structural claims are verifiable.
   - **Risk if ignored**: Over-strict interpretation creates precedent that any aesthetic language disqualifies otherwise enforceable principles.

4. **Establish principle-level vs. clause-level gate interpretation** (Priority: P1)
   - **Current state**: The audit applies word-by-word strictness without justifying this interpretation level.
   - **Proposed change**: Add §4.0 methodology section clarifying whether the gate evaluates principles as coherent units (core claims + supporting guidance) or requires clause-by-clause mechanical verification.
   - **Rationale**: Gate text refers to "the principle" as evaluation unit. Engineering sketches can target core enforcement without mechanizing every design-intent statement.
   - **Risk if ignored**: Inconsistent interpretation standards undermine the audit's methodological rigor and create unclear precedent for future gate applications.

5. **Resolve SPLIT verdict logic** (Priority: P3)
   - **Current state**: §4.3 creates "SPLIT" category without defining how it maps to pass/fail determinations (L93, L99, L107-108).
   - **Proposed change**: Either eliminate SPLIT as a verdict category or define clear rules for when split criteria result in overall pass vs. fail.
   - **Rationale**: The gate has binary requirements (3 criteria must be met). SPLIT verdicts within criteria don't automatically disqualify principles if the substantive enforcement passes.
   - **Risk if ignored**: Methodological ambiguity in the most contentious case (XVI) undermines confidence in the audit's other verdicts.

6. **Survey existing principle precedents** (Priority: P3)
   - **Current state**: The audit evaluates VI, X, XVI in isolation without reference to how accepted principles handle similar design-intent language.
   - **Proposed change**: Add brief survey of 2-3 accepted principles that contain aspirational language alongside enforceable rules, as precedent for gate interpretation strictness.
   - **Rationale**: Constitutional interpretation should be consistent across principles. If accepted principles routinely contain non-mechanical elements, this informs appropriate strictness levels.
   - **Risk if ignored**: Audit may apply inconsistent standards, migrating principles that are structurally similar to accepted ones.

7. **Define "concrete enough" sketch standards** (Priority: P3)
   - **Current state**: The audit requires "concrete enough" enforcement paths but doesn't establish sufficiency criteria (L54-55, L74-75).
   - **Proposed change**: Add brief definition of what constitutes an adequate engineering sketch per the gate requirements—specific lint rules, test patterns, and failure modes.
   - **Rationale**: Clear standards improve consistency between this audit and future gate applications. Vague requirements enable arbitrary strictness.
   - **Risk if ignored**: Subjective "concrete enough" judgments undermine the gate's objective intent and create unclear precedent.

### Referenced Documentation

- `specs/070-grandfathered-audit/spec.md` — sections/lines cited: L52-55, L73-75, L92-96, L100-101, L107-108
- `deliberations/070-spec-review-2026-04-28/audit-context.md` — sections/lines cited: L19-25, L49-62, L74-78