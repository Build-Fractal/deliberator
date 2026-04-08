# Meta-Review Instructions

## Scope
A meta-review synthesizes findings from multiple per-spec conversus deliberations. It reads all syntheses AND actual implementation code.

## Mandatory Checks

### 1. Read All Rounds (not just final synthesis)
When per-spec deliberations ran multiple rounds, the meta-review MUST read Round 1 synthesis AND Round 2+ syntheses. Items "resolved" by concession in Round 1 may contain valid findings that were dropped under social pressure rather than evidence.

For each concession in Phase 3 revisions:
- Was the counter-evidence that prompted withdrawal actually correct?
- Is the original finding still present in the code?
- Was it truly out of scope, or was it deferred without a tracking mechanism?

### 2. Verify Concessions Against Code
When agent A withdrew a finding after agent B challenged it:
- Read the code at the specific location agent A cited
- Verify agent B's counter-argument is factually correct
- If agent B was wrong, reinstate agent A's finding at its original priority

### 3. Flag "Resolved Via Scoping" Items
When a dispute was "resolved" by declaring it "out of scope":
- Record it as DEFERRED, not RESOLVED
- Add it to the meta-review's action items with a "tracking" tag
- Note which spec or future work should address it

### 4. Account for All P1s
If a per-spec synthesis had N P1 findings but the meta-review only carries M (where M < N):
- Explicitly list the (N - M) items that were dropped
- For each dropped P1, state why: absorbed into another finding, downgraded with evidence, or genuinely resolved
- Never silently drop a P1

### 5. Cross-Spec Impact Check
For each per-spec P1 finding, check whether it affects other specs:
- Does a bug in spec A break an assumption in spec B?
- Does a concession in spec A invalidate a "MET" verdict in spec B?
- Are there circular dependencies between spec findings?

## Output Format
The meta-review synthesis MUST include:
1. Standard sections (Process Summary, Scorecard, Contradictions, Convergence, Disputes, Changes, Concessions)
2. **Dropped Items Table** — every per-spec finding not in the meta-review, with reason
3. **Deferred Items Table** — every "out of scope" resolution, with tracking pointer
4. **Concession Audit** — every Phase 3 withdrawal verified against code
