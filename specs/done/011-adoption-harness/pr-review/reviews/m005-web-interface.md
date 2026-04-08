# M005 Web Interface Review

## Summary

M005 delivers a well-architected minimal web interface spanning 96 files (+19,207 lines) across a FastAPI backend with SSE streaming, Supabase persistence/auth, and a Next.js 16 frontend with shadcn/ui (base-nova). The implementation cleanly separates the "minimal hosted form" (FR-016) from a future "full web app" (FR-017) and includes proper BYOK API key handling, anonymous sessions, share links, and consumer metrics. Code quality is high throughout with thorough test coverage on both backend and frontend.

## Spec Compliance Scorecard

| FR | Status | Evidence | Notes |
|----|--------|----------|-------|
| FR-016 | PASS | /deliberate page: provider select, BYOK key input, question textarea, SSE streaming | Single page, no history, share page present |
| FR-016 (BYOK) | PASS | useState only; backend restores env var | Key never persisted to disk, DB, or cookies |
| FR-016 (Share) | PASS | POST /api/deliberations/{id}/share + GET /api/public/{share_id} + SSR share page | Self-contained link, no login required |
| FR-017 | PASS | No user accounts, no history, no dashboard | Clean boundary maintained |
| US-4 | PASS | Progressive disclosure: provider -> key -> question -> SSE result | End-to-end flow implemented |
| US-4 Scenario 2 | PASS | ShareButton + SSR share page with OG metadata | No login required to view |
| US-4 Scenario 3 | PASS | usage_events table + track* functions | Separate from engine metrics |
| FR-025 | PARTIAL | Three event types: task_completed, share_created, perceived_value | No session-level telemetry yet |

## Architecture Assessment

### Backend (FastAPI + SSE)
- AsyncQueueEmitter bridges sync engine to async SSE cleanly
- _event_stream() properly manages full lifecycle with finally cleanup
- Error mapping provides structured categories for frontend

### Database (Supabase)
- Three well-structured incremental migrations
- deliberations table with status constraint, timestamps, JSONB results
- Dependency injection via optional client parameter
- RLS / user_id MISMATCH: Migration 002 requires auth.uid() = user_id but backend never populates user_id

### Frontend (Next.js 16)
- Modern stack: React 19, Tailwind v4, shadcn/ui, pnpm
- Custom SSE parser for POST (since EventSource only supports GET)
- PhaseTimeline with real-time per-agent status
- MarkdownRenderer with DOMPurify XSS sanitization
- Dark mode with FOUC prevention
- Share pages are SSR with OG metadata and 60s ISR

### Separation of Concerns
- engine/ is pure domain, web/ is FastAPI adapter, frontend/ is independent
- StructuredDeliberation is canonical cross-layer contract

## Security Assessment

### BYOK API Key Handling (P1)
- Frontend: useState only (memory), never persisted
- Backend: Temporarily set as os.environ, used, immediately restored
- RACE CONDITION: In concurrent requests, different keys can race on os.environ
- Risk: Key briefly visible as process-level env var

### Supabase Security (P1)
- RLS enabled on both tables
- Migration 002 user-scoped policies BUT backend doesn't populate user_id
- FUNCTIONAL BUG: Backend inserts would fail RLS unless service role key used
- Migration 003 correctly adds public read for shared deliberations

### Share Links
- /share/{share_id} with 8 hex chars (32 bits entropy) -- adequate for MVP
- Only completed deliberations can be shared
- No "unshare" mechanism currently

### CORS
- Overly permissive: allow_methods=["*"], allow_headers=["*"]
- Should restrict to GET, POST, OPTIONS and Content-Type, Authorization

## Deployment Assessment

### DigitalOcean
- basic-xxs instance with /api/health check
- MISSING: FRONTEND_URL env var (defaults to localhost:3000 in production)
- MISSING: No frontend deployment in app spec (Vercel separate)
- MISSING: No CORS_ORIGINS default value

### Packaging
- web included in hatch wheel (fix commit 57bd5aa)
- supabase + fastapi moved to core deps (fix commit 18a18ed)

## Code Quality Assessment

### Strengths
- Consistent event type taxonomy across backend and frontend
- Comprehensive test coverage: 427 lines test_app.py, 437 lines test_db.py, ~1900 lines frontend tests
- Graceful Supabase-optional degradation
- Complete docs/web.md reference
- Custom design tokens with OKLCH color space

### Issues
- [P1] os.environ race condition for BYOK keys
- [P1] RLS / user_id gap -- migration 002 blocks backend
- [P2] No rate limiting on /api/deliberate
- [P2] No max_length on question field
- [P3] provider defaults to "mock" -- should be required in production
- [P3] No unshare endpoint

## Vision Alignment

### Supports Future Specs
- FR-017: Clean boundary; accounts/history/dashboard can build on existing auth + tables
- Spec 020: deliberations.structured_result JSONB = full StructuredDeliberation for export
- Training Data: perceived_value feedback + stored Q&A = natural preference dataset
- Telemetry: usage_events table + trackEvent() extensible

### Blocks or Conflicts
- RLS mismatch could block deployment
- No unshare mechanism for sensitive deliberations

## Recommendations

| # | Priority | Recommendation | Rationale | Affects |
|---|----------|---------------|-----------|---------|
| 1 | P1 | Pass API key directly to provider constructor instead of os.environ | Race condition + brief env var exposure | M005 |
| 2 | P1 | Fix RLS / user_id: use service role key OR populate user_id OR add backend policy | Migration 002 blocks backend reads/writes | M005 |
| 3 | P2 | Add FRONTEND_URL to .do/app.yaml | Share URLs point to localhost in production | M005 |
| 4 | P2 | Add max_length to question field (e.g. 10,000 chars) | Prevents token exhaustion | M005 |
| 5 | P2 | Add basic rate limiting on POST /api/deliberate | Each request spawns full pipeline; no abuse protection | M005 |
| 6 | P3 | Restrict CORS allow_methods and allow_headers | Defense in depth | M005 |
| 7 | P3 | Add unshare endpoint | Users should be able to revoke shared links | M005 |
| 8 | P3 | Move import json to top of web/app.py | Code hygiene | M005 |

## Cross-Milestone Observations
- M005 is heaviest milestone at ~19,200 lines; frontend lockfile accounts for ~8,000
- engine/adhoc.py deduplication (S01/T01) was smart prerequisite
- StructuredDeliberation as cross-layer contract is well-designed
- AsyncQueueEmitter correctly placed in engine layer (not web layer)
- Fix commits suggest packaging/deployment needed iteration -- normal for new target
