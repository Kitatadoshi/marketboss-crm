# EVENT_CONTRACTS_V1.md

Дата: 2026-02-26

## Цель
Стандартизировать события между контекстами MarketBoss CRM для real-time мониторинга, аналитики и агентных действий.

## Базовый envelope
```json
{
  "event_id": "evt_xxx",
  "event_name": "deal.stage.changed",
  "event_version": 1,
  "occurred_at": "2026-02-26T14:00:00Z",
  "producer": "deal_strategy",
  "aggregate_type": "deal",
  "aggregate_id": "deal_123",
  "correlation_id": "corr_abc",
  "causation_id": "cmd_456",
  "payload": {},
  "meta": {
    "actor_type": "agent|human|system",
    "actor_id": "marketboss",
    "risk_level": "low|medium|high"
  }
}
```

## События v1

### Lead Intake
- `lead.created`
- `lead.qualified`
- `lead.rejected`

Payload minimal:
```json
{ "source": "telegram", "status": "new|qualified|rejected" }
```

### Deal Strategy
- `deal.created`
- `deal.stage.changed`
- `deal.closed.won`
- `deal.closed.lost`

Payload minimal:
```json
{ "from": "diagnostic", "to": "niche_test", "owner": "marketboss" }
```

### Analytics BI
- `metric.snapshot.recorded`
- `kpi.threshold.breached`
- `anomaly.detected`

Payload minimal:
```json
{ "deal_id": "deal_123", "ctr": 0.018, "cr_order": 0.043, "gross_margin": 0.08 }
```

### Executive Control
- `decision.recorded`
- `recommendation.created`
- `recommendation.approved`
- `recommendation.rejected`

Payload minimal:
```json
{ "decision_type": "pricing_test", "expected_effect": "+8% conversion" }
```

## Правила совместимости
- `event_name` неизменяем; изменения через `event_version`.
- Добавление новых полей в payload — backward-compatible.
- Удаление/переименование полей — только в новой версии.

## Routing v1
- `deal.stage.changed` -> analytics_control_tower + advisor agent.
- `kpi.threshold.breached` -> watcher agent + UI alerts.
- `decision.recorded` -> reporting + learning loop.

## Delivery semantics (v1)
- At-least-once delivery.
- Идемпотентность на стороне consumer по `event_id`.
- Retry with backoff для временных ошибок.

## Хранилище (текущее)
- SQLite table `event_logs` (MVP).
- Next: append-only event store + подписки.
