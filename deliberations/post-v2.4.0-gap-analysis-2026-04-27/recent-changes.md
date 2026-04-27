# Changes Since v2.3.0 Gap Analysis (2026-04-25 → 2026-04-27)

The 2026-04-25 deliberation reviewed PRs #4-#14 and produced the v2.3.0
amendment. This file summarizes what has shipped *since then*. The
question for this deliberation is whether anything in this layer
embodies an unwritten invariant that should be codified — operating
under the v2.4.0 Constitutional Inclusion Criteria gate.

The gate (Governance §Constitutional Inclusion Criteria, v2.4.0)
requires every proposed new principle to satisfy:
1. Mechanical verification capability
2. Falsifiable scope
3. Distinct from existing principles

Test each proposal in this deliberation against the gate.

---

## Constitutional amendments shipped

- **#15** Spec 065 (path to open source) — 10 launch gates G1-G10
- **#16** Governance log file (`CONSTITUTIONAL_CONVERSATIONS.md`) +
  first entry for the 2026-04-25 gap analysis
- **#17** Spec 066 — v2.3.0 amendment package (proposal)
- **#18** Phase 1 — manifest.json tools[] projected from CAPABILITIES;
  found 2 missing tools and a stale description
- **#19** Constitution v2.2.0 → v2.3.0 (6 new principles + 2 extensions)
- **#20** Constitution v2.3.0 → v2.3.1 PATCH (XV registry-boundary
  clarification, completing the blind-verification finding #1 split
  between XV and XXVII)
- **#21** Spec 067 — verification methodology requires BOTH self-
  consistency AND blind (proposal)
- **#22** Phase 2 — mcp_server.py drift guard + 2 missing tool
  decorators surfaced by the test
- **#23** Spec 067 §4.3.1 — use existing role presets, do NOT
  hand-roll; codifies the lesson from the v2.3.0 blind run
- **#24** Spec 066 §7 superseded annotation pointing to spec 067
- **#25** `scripts/strip-constitution-for-blind.py` reference
  implementation of spec 067 §4.2's stripping recipe
- **#26** Spec 068 — Principle XVI determinism-scope clarification
  (proposal)
- **#27** Spec 069 — mechanical verification gate for constitutional
  inclusion (proposal)
- **#28** Naming deliberation prompt + walkthrough for `fractal <verb>`
  consolidation
- **#29** Constitution v2.3.1 → v2.3.2 PATCH (XVI determinism-scope,
  with 7 ACCEPT fixes from both verification methodologies)
- **#31** Governance log housekeeping — committed 75 deliberation
  artifacts + 4 governance log entries
- **#32** Constitution v2.3.2 → v2.4.0 MINOR (Constitutional Inclusion
  Criteria gate, with 3 ACCEPT fixes from blind verification)
- **#33** `.aider*` gitignore rule that had been a session-long stash
  floater

## Methodology evolution

The v2.3.0 gap analysis ran a 4-agent cooperative deliberation over
2 rounds with subject arbitration. Since then:

- **Spec 067 codified both-methodologies requirement.** Every
  constitutional amendment from spec 068 forward ran self-consistency
  AND blind verification. The blind run on spec 068 caught 4 ACCEPT
  findings the self-consistency run missed; on spec 069 it caught 3
  where self-consistency caught 0.
- **Spec 067 §4.3.1 prohibits hand-rolling agent personas** when
  presets exist. Subsequent deliberations used `devils-advocate` and
  `balanced-arbiter` presets.
- **Stripping recipe now mechanical.** PR #25's
  `scripts/strip-constitution-for-blind.py` automates the §4.2 recipe
  (5 steps + zero-leakage check).
- **Agents Write their own files.** Mid-session pivot from
  orchestrator-writes-from-response to agents-Write-directly. Memory
  entry `feedback_subagents_write_their_own_files.md` captures this.
- **Implementation can run parallel to verification.** Spec 069's
  implementation subagent ran concurrently with the spec 069 blind
  Phase 1 reviews — used the 17-agent deliberation runtime to also
  produce the implementation PR.

## Operational issues encountered

- **Overnight infrastructure stalls (claude-code provider).** Three
  agents stalled at 1054s/6146s/7466s vs normal ~80s. All recovered
  or were retried. No methodology issue, but worth noting that
  agents-Write-directly let work survive the orchestrator stream
  failures.
- **GitHub force-push closes PRs unexpectedly.** PR #30 was force-
  pushed after a clean rebase; GitHub auto-closed it instead of
  refreshing. PR #32 is its replacement. Lesson: prefer opening a
  replacement PR over force-rebasing in place when the target branch
  has just been updated.

## Cross-cutting themes that may warrant new principles (test against
the v2.4.0 gate)

1. **Verification cost discipline** — both-methodologies now requires
   ~34 launches per amendment minimum (17 self + 17 blind). Should
   the constitution mandate cost reporting for verification runs?
   Test: mechanical verification (count agent launches per
   amendment, log to governance log) — passes? falsifiable scope
   (check for verification cost line in each governance log entry)
   — passes? distinct from existing — XXV (Live Test Cost
   Discipline) covers test costs but not deliberation costs;
   probably distinct.
2. **Implementation parallelization** — the spec 069 implementation
   subagent ran concurrently with verification. Should this become
   constitutional pattern? Probably no — XIV (Spec-Implementation
   Parity) covers the result, not the parallel pattern. Operational
   guidance, not constitutional.
3. **PR replacement after force-push** — GitHub's behavior surprised
   us. Operational learning, not a principle. Belongs in
   `CONTRIBUTING.md` once it exists (per spec 065 G7).
4. **Audit trail completeness** — 75 deliberation artifacts now in
   git, 4 governance log entries filed. Should "verification
   artifacts MUST live in git" be codified? Test against gate:
   mechanical (CI check that the deliberations/ directory has the
   expected structure for each named amendment) — passes?
   falsifiable — passes; distinct — XI Single Source of Truth
   covers it implicitly but doesn't say so for governance artifacts.
5. **Subagent-Write discipline** — agents-Write-directly is a
   methodology rule, not a content rule. Lives in spec 067 / the
   memory entry. Probably operational.
6. **Stagnation detection in deliberations** — the prior gap analysis
   ran 2 rounds with stagnation: detect; this session's verifications
   ran 1 round each. Should stagnation detection be required? Spec 067
   doesn't currently mandate it. Probably operational guidance.

These themes are the seed. Agents should evaluate each against the
v2.4.0 gate and surface ones not listed here.
