# CHANGELOG_SPRINT1.md

Дата: 2026-02-26

## Scope
Sprint-1: Event Contracts v1 + Realtime + Alert Engine + Agent Action API (guarded) + Recommendations v1.

## Delivered

### 1) Event Contracts v1
- Typed `EventEnvelope` + `EventMeta`.
- Extended event schema fields: version, producer, correlation/causation, actor/risk.
- Idempotent event insert (`INSERT OR IGNORE` by event id).

### 2) Realtime Dashboard
- SSE endpoint: `GET /api/events/stream`.
- Realtime snapshot endpoint: `GET /api/realtime`.
- Dashboard live updates for alerts + event log (+ recommendations).

### 3) Alert Engine v1
- Stateful alerts table with dedup key and lifecycle.
- Statuses: `open`, `ack`, `resolved`.
- Endpoints:
  - `GET /api/alerts`
  - `POST /api/alerts/{id}/ack`
  - `POST /api/alerts/{id}/resolve`
- Rules:
  - CTR < 2%
  - CR < 5%
  - margin < 10%
  - aging >= 3d (warning), >= 7d (danger)

### 4) Agent Action API (guarded)
- Endpoint: `POST /api/agent/actions/move-deal-stage`.
- Guard policy by risk + approval flag.
- `agent_action_logs` for audit trail.

### 5) Recommendations v1
- Recommendations lifecycle: proposed -> approved/rejected.
- Endpoints:
  - `GET /api/recommendations`
  - `POST /api/recommendations`
  - `POST /api/recommendations/{id}/approve`
  - `POST /api/recommendations/{id}/reject`
- Realtime list in dashboard + approve/reject UI.

## Notes
- Current implementation keeps backward compatibility with existing MVP forms/APIs.
- Next sprint can focus on richer policy engine, RBAC, and explicit approval workflows for all medium/high actions.
