# Architecture (Draft v0.1)

## Контекст
CRM для маркетплейсов: WB/Ozon, с фокусом на управляемый рост до 1M+ оборота.

## Слои
1. **Domain layer** — сущности и правила
2. **Application layer** — сценарии (use-cases)
3. **Infrastructure layer** — БД, интеграции, импорт/экспорт
4. **Interface layer** — UI/API/бот

## Базовые bounded contexts
- Lead Management
- Deal Pipeline
- Task & Execution
- SKU & Unit Economics
- Metrics & Reporting

## Принципы
- data-first
- auditability (история изменений)
- KPI-driven decisions
- small iterations (HADI)
