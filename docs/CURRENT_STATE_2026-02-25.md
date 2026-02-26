# Current State — 2026-02-25

## Зафиксированные решения

1. Ядро системы: **CRM как бортовая панель бизнеса**
2. Архитектура: **Clean Architecture + DDD + EventBus**
3. Язык: **Python only** (без JS в core)
4. Типизация: **строгая** (`mypy strict`)
5. Доступы:
   - для агентов: API/CLI
   - для человека: Web (план: FastAPI + web-интерфейс)
6. Разработка идёт параллельно операционной работе:
   - поиск ниш
   - тест гипотез
   - запуск/оптимизация

## Контексты (v2, RAG-driven)

1. `acquisition_qualification`
2. `niche_offer_strategy`
3. `sourcing_supply_chain`
4. `listing_content_optimization`
5. `promotion_traffic`
6. `unit_economics_pricing`
7. `operations_platform_execution`
8. `analytics_control_tower`
9. `knowledge_playbooks`

## Что уже подготовлено

- `docs/ARCHITECTURE_DECISION_RECORD.md`
- `docs/CONTEXT_MAP.md`
- `docs/CONTEXT_RATIONALE.md`
- `docs/TECH_STACK.md`
- `docs/STRUCTURE.md`
- `docs/NEXT_STEPS.md`
- `pyproject.toml` со strict-правилами
- базовый каркас Python-проекта
- базовый EventBus (in-memory):
  - `src/application/contracts/event_bus.py`
  - `src/infrastructure/eventbus/in_memory.py`

## Операционная цель системы

Поточный конвейер формализованных объектов по этапам:

`Intake -> Qualification -> Niche Test -> Economics Check -> Launch -> Optimize -> Scale`

С обязательной фиксацией:
- статуса этапа
- метрик
- решений (Decision Log)
- причин перехода/блокировки

## Что ждёт подтверждения после догрузки базы

После расширения RAG-базы курсов:
1. финальная проверка контекстов (immutability v1)
2. фиксация event contracts
3. фиксация object model v1

## MVP, реализованный 2026-02-26

- FastAPI web + API интерфейс (`src/interfaces/http/app.py`)
- Bootstrap dashboard (`src/interfaces/http/templates/dashboard.html`)
- SQLite persistence (`data/db/crm.sqlite3`, `src/infrastructure/persistence.py`)
- CLI для агентов (`src/interfaces/cli.py`)
- Docker runtime (`Dockerfile`, `docker-compose.yml`, `docker-compose.dev.yml`)
- health endpoint: `/health`
- API endpoints: `/api/leads`, `/api/deals`, `/api/metrics`, `/api/decisions`
