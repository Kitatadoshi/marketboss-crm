# REALTIME_CONTROL_TOWER_SPEC.md

Дата: 2026-02-26

## Цель
Единый экран управления, где человек и агенты видят состояние pipeline в реальном времени, риски и рекомендации.

## Основные блоки UI (v1)
1. **KPI Header**
   - Leads, Deals, Revenue, Gross Profit, конверсии, маржа.
2. **Pipeline Kanban**
   - Стадии + количество сделок + aging по стадии.
3. **Alerts Panel**
   - CTR/CR/маржа/SLA-алерты с приоритетами.
4. **Recommendations Feed**
   - NBA от Advisor Agent: действие, аргументация, expected effect.
5. **Decision Log**
   - Принятые решения, owner, timestamp, outcome.
6. **Event Stream**
   - Поток бизнес-событий (фильтры по deal/context/criticality).

## Real-time сигналы (v1)
- `kpi.threshold.breached`
- `anomaly.detected`
- `deal.stage.changed`
- `recommendation.created`

## Правила алертов (первичные)
- CTR < 2% -> warning
- CR(order) < 5% -> warning
- Gross margin < 10% -> danger
- Deal aging > X дней на стадии -> warning/danger

## Действия из UI
- Смена стадии сделки.
- Создание decision log.
- Подтверждение/отклонение рекомендации агента.
- Назначение владельца/дедлайна по задаче.

## Agent integrations
- Operator Agent API: mutate operations (guarded).
- Analyst Agent API: summary + diagnostics.
- Watcher Agent API: alert generation.
- Advisor Agent API: recommendation generation.

## SLA и качество
- TTI для critical alert <= 60 сек.
- Дедупликация повторных алертов.
- Визуальный статус: open / acknowledged / resolved.

## V2 roadmap
- WebSocket/SSE для live updates.
- Alert correlation (объединение связанных сигналов).
- Playbooks: полуавтономное выполнение рекомендаций по policy.
- Прогнозный блок: short-term forecast по revenue/margin.
