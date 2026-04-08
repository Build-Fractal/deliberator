# Meta-Reviews

A meta-review is a cross-spec consistency audit that reads all per-spec conversus syntheses
plus actual implementation code. Run one after each wave of spec implementations.

## When to Run
- After implementing 2+ specs in parallel
- After applying P1 fixes from per-spec reviews
- Before merging a wave PR to main

## How to Run
Use 4 auditors: consistency-auditor, implementation-verifier, dependency-auditor, test-coverage-auditor.
Each reads all syntheses + key implementation files.

## Template
Follow `templates/meta-review-instructions.md` for mandatory checks.
