# Context Rationale (data-driven from RAG)

Источник анализа: `knowledge_master_marketplaces.db` (6116 записей).

## Что показал анализ
- Топ-темы в базе:
  - Логистика/поставки
  - Юнит-экономика и цена
  - Оптимизация карточек
  - Продвижение/реклама
  - Анализ ниши/конкурентов
- Частотные сигналы по тексту:
  - `реклам*`, `карточ*`, `конвер*`, `выкуп`, `ctr`, `акци*` — очень высокие
  - `кита*`, `закуп*`, `поставк*`, `склад` — высокий кластер supply/sourcing
- Ограничение данных: база сейчас перекошена в несколько крупных курсов (неравномерное покрытие), поэтому контексты должны быть стабильными и независимыми от одного курса.

## Принцип деления
Контексты делим по **устойчивым бизнес-способностям**, а не по названиям курсов:
1) Acquisition & Qualification
2) Niche & Offer Strategy
3) Sourcing & Supply Chain
4) Listing & Content Optimization
5) Promotion & Traffic
6) Unit Economics & Pricing
7) Operations & Platform Execution
8) Analytics & Control Tower
9) Knowledge & Playbooks

Это минимизирует риск переделки при расширении RAG-базы.
