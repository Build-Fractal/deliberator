# Engine Implementor — Remaining Disputes

**Date**: 2026-04-16
**Phase**: 4 — Disputes
**Basis**: All three revised positions (engine-implementor, test-architect, consumer-advocate)

---

## Overview

After revision, the three reviews are substantially aligned on the core issues. The must-fix list (schema error, red-blue adhoc path, settings isolation, shell quoting, intermediate artifact access) is unanimous. The priority list has converged on most items. However, four genuine disputes remain where my revised position diverges from one or both of the other agents.

---

## Dispute 1: Mock provider fix — realistic response mode vs. targeted fixture test

**My position (R14)**: The mock provider must return output that exercises the production synthesis parsing path. Either enhance the mock provider with a "realistic response mode" or add a separate realistic mock. Priority: P0.

**Test-architect's revised position**: Withdrew their original P0 recommendation to rewrite the mock provider, accepting the consumer-advocate's counter-proposal. Their revised P0 is a targeted `parse_synthesis()` fixture test using a known-good markdown string.

**Consumer-advocate's revised position**: Originally accepted the test-architect's mock provider finding as their #1 P0 item and called for "realistic response mode." But the test-architect's revision withdrew this in favor of the consumer-advocate's own counter-proposal (the fixture test), which the consumer-advocate had not yet seen at revision time. The consumer-advocate's final P0 list item #1 still says "Fix mock provider to return parseable synthesis."

**Why I dispute**: The test-architect's revised approach (fixture test on `parse_synthesis` directly) is a unit test. It verifies that the parser works on well-formed input. It does not verify that the smoke tier's end-to-end tests exercise the production code path. After this fixture test is added, every smoke test still runs through the `bare except` fallback in `from_events()`, meaning the smoke tier still produces green results while the production parsing path is untouched. The fixture test catches parser regressions, but the smoke tier remains structurally misleading.

My R14 addresses a different problem: the smoke tier's claim that "the engine produces correct output" is false if every mock-based test silently falls through to the error-recovery path. A `parse_synthesis` unit test does not fix this. Either the mock returns parseable output so the smoke tests exercise the real path, or the spec must explicitly document that the smoke tier tests the fallback path and the fixture test covers the production path. The test-architect's revision does neither -- it replaces one concern (mock rewrite) with another (fixture test) without acknowledging that the smoke tier's structural regression value remains zero.

**Resolution I would accept**: Both. Add the `parse_synthesis` fixture test (test-architect's proposal) AND either (a) enhance mock to return parseable output for at least one mode, or (b) add a single integration test that uses a realistic markdown fixture piped through the full `from_events()` path (not just `parse_synthesis` in isolation). The fixture test alone is necessary but not sufficient.

---

## Dispute 2: Red-blue smoke test path — pre-built YAML (my R1) vs. adhoc path (test-architect's revised P0)

**My position (R1, maintained through revision)**: Red-blue tests must use pre-built YAML configs, not the adhoc `decide` path, because `build_adhoc_config` cannot generate valid red-blue configs (no `role: red/blue` agents).

**Test-architect's revised position (their modification #4)**: The red-blue smoke test should use the adhoc path, not pre-built YAML. Their reasoning: if the smoke test uses pre-built YAML, it bypasses `build_adhoc_config` entirely, and the G1 regression path is untested. They frame this as a tension between my R1 and my own G1 regression position.

**Consumer-advocate's revised position**: Aligns with me -- scope step 3 to exclude red-blue for the first eval run (their P0 item #4), with red-blue tested after G1 is fixed.

**Why I dispute**: The test-architect identifies a real tension, but their resolution creates a worse problem. If the red-blue smoke test uses the adhoc path, it is blocked until G1 is fixed. There is no red-blue smoke test at all until then. My R1 (pre-built YAML) plus my R6/S-3 (pytest xfail test for adhoc red-blue `parse_config`) covers both concerns:

1. Pre-built YAML red-blue smoke test verifies the engine handles red-blue mode correctly, independent of the adhoc config generator.
2. The xfail test verifies that `build_adhoc_config` for red-blue currently fails, and flips to pass when G1 is fixed.

The test-architect's resolution collapses these into one test, which means the engine's red-blue mode has zero smoke coverage until the adhoc path is fixed. The point of using pre-built YAML is to decouple "does red-blue mode work?" from "does the adhoc config generator support red-blue?" These are independent questions and should be independently testable.

**Resolution I would accept**: Pre-built YAML for the red-blue mode smoke test (verifies engine correctness) AND the adhoc-path xfail test (tracks G1 regression). This is my existing revised position from S-3. Both tests exist from day one. The test-architect's concern about the adhoc path being untested is addressed by the xfail test without sacrificing red-blue mode coverage.

---

## Dispute 3: Mock provider realistic mode priority — P0 (me) vs. withdrawn (test-architect)

This is related to but distinct from Dispute 1. The question is not just what to do, but when.

**My position**: R14 is P0 because without it, the smoke tier has no structural regression value. A test suite that cannot detect regressions in the production code path is not ready for CI gating.

**Test-architect's revised position**: Withdrew mock provider modification entirely. Their P0 list includes the fixture test but not the mock enhancement. Implicitly, any mock enhancement is deferred indefinitely.

**Consumer-advocate's revised position**: Lists "Fix mock provider to return parseable synthesis" as P0 item #1 in their revised priority list, agreeing with me.

**Why I dispute**: The test-architect's withdrawal was motivated by the consumer-advocate's argument that mock provider enhancement is "a test infrastructure project masquerading as a bug fix" that "blurs the clean separation between test tiers." I disagree with this framing. Adding a `realistic_response: true` flag to the mock provider that returns markdown with `## Headline\n...` and `## Summary\n...` headers is not a test infrastructure project -- it is a one-function change that makes the existing smoke tests exercise the production path instead of the error path. The mock provider already returns mode-specific canned responses; making those responses parseable by `parse_synthesis` is a refinement, not a rewrite.

The consumer-advocate agrees with me on priority. The test-architect's revised position is the outlier. However, since the test-architect is the role most responsible for test architecture, their withdrawal carries weight. I maintain my P0 position but acknowledge this requires synthesis-phase resolution.

---

## Dispute 4: Desktop Extension content scanner testing — engine eval scope vs. out of scope

**My position (M-7, item 1)**: Desktop Extension content scanner rejection is a valid concern but belongs in Desktop Extension CI, not in Spec 061. The role-split workaround is engine code, but the content scanner is a Claude Desktop platform constraint.

**Consumer-advocate's revised position (their strengthened item 2.5)**: All 7 MCP prompts must be tested against content scanner patterns. Rated P1. Both the test-architect and engine-implementor acknowledged the finding.

**Test-architect's revised position**: Accepted from consumer-advocate as P2 (section "Items I Did Not Originally Address", item 3 under consumer-advocate findings). Did not explicitly place it in or out of engine eval scope.

**Why I dispute**: The content scanner is not part of the conversus engine. It is a Claude Desktop runtime constraint that varies by Desktop version and Anthropic's content policy updates. Testing MCP prompts against content scanner patterns means:

1. The eval suite must encode assumptions about what the content scanner rejects, which are not documented or stable.
2. A content scanner policy change at Anthropic can break tests without any engine code change.
3. The role-split workaround in `design_deliberation()` and `analyze_documents()` is engine code, but it exists specifically because the engine cannot control the scanner. Testing the workaround means testing against an external, undocumented, mutable constraint.

The correct location for this test is the Desktop Extension's own CI, where the actual content scanner can be exercised against the actual prompts in the context of the actual Desktop runtime. The engine eval suite should test that MCP prompts are well-formed and produce correct results. Whether those prompts survive a third-party content filter is not an engine correctness concern.

I acknowledge the consumer-advocate's point that this is a real failure mode for real users. But scoping the eval suite to include third-party runtime constraints sets a precedent that makes the suite fragile. If content scanner testing is included, what about Cursor's tool limit? (The consumer-advocate themselves withdrew that.) The principle should be consistent: the eval suite tests engine behavior, not host-environment behavior.

**Resolution I would accept**: Document the content scanner risk in the spec's consumer table or in a "known external risks" section. Do not add content scanner pattern tests to the engine eval suite. Optionally, file a separate spec for Desktop Extension integration testing that includes content scanner coverage.

---

## Summary

| # | Topic | My position | Opposing position(s) | Severity |
|---|-------|-------------|----------------------|----------|
| 1 | Mock provider fix approach | Realistic mock mode + fixture test (both) | Test-architect: fixture test only (withdrawn mock rewrite) | High -- determines whether smoke tier has structural regression value |
| 2 | Red-blue smoke test path | Pre-built YAML + xfail adhoc test | Test-architect: adhoc path only (no pre-built YAML) | Medium -- determines whether red-blue has coverage before G1 fix |
| 3 | Mock realistic mode priority | P0 (agrees with consumer-advocate) | Test-architect: withdrawn/deferred | Medium -- determines implementation order |
| 4 | Content scanner testing scope | Out of engine eval scope | Consumer-advocate: P1 in engine eval | Low -- scope boundary question, not correctness |

Disputes 1-3 are interconnected. They all stem from the same root question: does the smoke tier need to exercise the production synthesis parsing path, or is a separate fixture test sufficient? The test-architect says the fixture test is sufficient. The consumer-advocate and I say the smoke tier must also exercise the production path. This is the single remaining axis of genuine disagreement across all three reviews.

Dispute 4 is a scope question. If the synthesis phase rules that the engine eval suite covers only engine code paths (not host-environment constraints), it resolves in my favor. If the synthesis phase rules that the eval suite covers all failure modes a consumer can experience through engine entry points, it resolves in the consumer-advocate's favor.
