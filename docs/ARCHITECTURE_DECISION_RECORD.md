# Architecture Decision Record (ADR)

Стек и подход зафиксированы:

1. **Clean Architecture** — обязательная архитектурная основа
2. **Bootstrap** — UI и админка на Bootstrap 5
3. **Event Bus** — внутренняя шина доменных/интеграционных событий
4. **DDD** — моделирование предметной области через bounded contexts

## Цели
- Изолировать домен от инфраструктуры
- Быстро запускать UI для операционной работы
- Обеспечить расширяемость через события
- Снизить хаос в бизнес-логике за счёт доменной модели

## Обязательные правила
- Домен не зависит от фреймворков/БД/UI
- Все use-cases идут через Application layer
- Любое значимое изменение состояния публикует domain event
- Между bounded contexts — взаимодействие только через события/контракты

## Базовые bounded contexts (v1)
- Lead Management
- Deal Pipeline
- Task Execution
- Metrics & Reporting
- Knowledge/RAG Link

## События v1 (черновик)
- `lead.created`
- `lead.qualified`
- `deal.created`
- `deal.stage.changed`
- `task.created`
- `task.completed`
- `metric.snapshot.recorded`

## Технологический baseline (v1)
- Runtime: Node.js + TypeScript
- Storage (MVP): JSON/SQLite
- EventBus (MVP): in-memory pub/sub
- UI (MVP): Bootstrap 5 + server-rendered views

## Не делаем сейчас
- Распределённый брокер (Kafka/Rabbit) на MVP
- Микросервисы до стабилизации доменной модели

Дата фиксации: 2026-02-25
