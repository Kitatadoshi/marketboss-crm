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


## 2026-02-26 — Step 2 done: Realtime stream (SSE)

### Implemented
- Added realtime API endpoints in `src/interfaces/http/app.py`:
  - `GET /api/alerts`
  - `GET /api/realtime`
  - `GET /api/events/stream` (Server-Sent Events)
- Added snapshot generator that streams updates when new event id appears.
- Upgraded dashboard template (`dashboard.html`):
  - live alerts container (`#alerts-container`)
  - live event log body (`#event-log-body`)
  - browser `EventSource` client that updates UI without reload.

### Notes
- Transport: SSE (lightweight and enough for v1 realtime).
- Poll interval in stream loop: 2 sec.


## 2026-02-26 — Step 3 done: Alert Engine v1 (stateful)

### Implemented
- Added `alerts` table in DB (`src/infrastructure/persistence.py`):
  - `alert_key` unique for dedup
  - status lifecycle: `open|ack|resolved`
  - timestamps: first_seen/last_seen/resolved_at
- Implemented stateful alert engine in `src/application/services.py`:
  - `refresh_alerts()` recalculates active signals
  - dedup by stable `alert_key`
  - stale alert auto-resolve
  - aging alerts by deal age (>=3 warning, >=7 danger)
  - endpoints helpers: `ack_alert`, `resolve_alert`, `list_alerts`
- Integrated alerts into API/UI (`src/interfaces/http/app.py`, `dashboard.html`):
  - `GET /api/alerts`
  - `POST /api/alerts/{id}/ack`
  - `POST /api/alerts/{id}/resolve`
  - dashboard alert buttons Ack/Resolve

### Alert rules v1
- CTR < 2% => warning
- CR(order) < 5% => warning
- Margin < 10% => danger
- Deal aging >=3d => warning
- Deal aging >=7d => danger

