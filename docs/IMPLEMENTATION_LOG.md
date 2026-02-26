# IMPLEMENTATION_LOG.md

## 2026-02-26 — Sprint-1 kickoff (Event/Realtime/Alerts)

### Scope (approved)
- Event Contracts v1 in code (typed envelope, versioning, idempotency)
- Realtime updates for dashboard (SSE/WebSocket)
- Alert Engine v1 (CTR/CR/margin/aging, open/ack/resolved, dedup)

### Working rules
- Small atomic commits
- Every step reflected in docs
- Backward compatibility for current API/UI
- Keep architecture flexible for tomorrow's expanded RAG context

### Planned deliverables
1. `docs/IMPLEMENTATION_LOG.md` (this file, step-by-step record)
2. `docs/CHANGELOG_SPRINT1.md` (final summary)
3. Updated code + tests + migration notes

## 2026-02-26 — Step 1 done: Event Contracts v1 in code

### Implemented
- Reworked `src/shared/events.py`:
  - `EventEnvelope`
  - `EventMeta`
  - `ActorType`, `RiskLevel`
- Upgraded `event_logs` schema in `src/infrastructure/persistence.py`:
  - `event_version`, `producer`, `correlation_id`, `causation_id`, `actor_type`, `actor_id`, `risk_level`
  - Added backward-safe column migration via `PRAGMA table_info + ALTER TABLE`.
- Updated event emission in `src/application/services.py`:
  - Single `_log_event(...)` with envelope + validation
  - `INSERT OR IGNORE` by event id (idempotency base)
  - Added producer/meta/risk on all business events
- Extended event API payload (`list_event_logs`) with new envelope fields.

### Notes
- Existing API/UI kept backward compatible.
- Current idempotency behavior: duplicate `event_id` ignored.

