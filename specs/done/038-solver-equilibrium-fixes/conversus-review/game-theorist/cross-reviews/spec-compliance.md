# Cross-Review of spec-compliance
**Reviewer**: game-theorist

## Agreements
- RE-2 NOT MET is correct — the spec amendment is the deliverable.
- RE-3 MET is correct — documentation option was taken.
- NEW-3 NOT MET is correct — spec text not updated.

## Challenges

### On compliance scope
The spec-compliance review correctly notes that RE-2 and NEW-3 are documentation tasks. However, the compliance review does not flag the cross-spec impact: RE-2's unresolved matrix shape means the equilibrium scorer produces trivial results for WTA mode. This affects spec 021 and spec 017 as well.

## Additions
My F-4 finding (missing payoff functions for 4 new modes) is not a spec 038 item but should be flagged as a cross-spec gap affecting spec 028 (mode expansion) and spec 017 (equilibrium scoring).
