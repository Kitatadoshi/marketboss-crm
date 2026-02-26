# COMPETITIVE_MATRIX.md

Дата: 2026-02-26

Цель: сравнить существующие решения с целевой моделью **MarketBoss CRM Control Tower** (CRM + pipeline + marketplace-native аналитика + event log + API/CLI для агентной оркестрации).

## 1) Наша целевая модель (эталон)

Обязательные capability-блоки:
- CRM: лиды, сделки, стадии
- Pipeline/Kanban: управление этапами запуска и роста
- Marketplace-native KPI: CTR, CR, выкупы, маржа, unit economics
- Decision Log: фиксация управленческих решений и ожидаемого эффекта
- Event Log / Event contracts: трассируемый поток бизнес-событий
- Agent-ready interface: API + CLI для автономных/полуавтономных агентов

## 2) Краткая карта рынка

### A. CRM-платформы (сильны в воронке, слабы в marketplace-native слое)
- HubSpot
- Pipedrive
- Bitrix24
- amoCRM
- Salesforce

### B. E-commerce OMS/ERP/Operations (сильны в операционке, слабы в CRM decision-loop)
- Odoo
- ERPNext
- Sellercloud
- Linnworks
- Extensiv (Skubana)

### C. Marketplace интеграторы и фиды (каналы/листинги/синхронизация)
- ChannelEngine
- Channable
- Lengow
- ChannelAdvisor (Rithum)

### D. Marketplace аналитика/оптимизация (KPI и прогнозы, но не CRM-ядро)
- DataHawk
- Helium 10
- Jungle Scout
- Sellics/Perpetua
- MPStats/Moneyplace (RU-сегмент аналитики)

### E. Open-source CRM/ERP базы для кастомизации
- Odoo Community
- ERPNext
- SuiteCRM
- EspoCRM

## 3) Сравнение: «насколько заменяет нас»

Шкала:
- 3 = закрывает нативно
- 2 = частично (с доработками)
- 1 = сильно кастомизировать
- 0 = практически нет

### 3.1 CRM-платформы
- HubSpot: CRM 3 / Pipeline 3 / Marketplace KPI 1 / Decision log 1 / Event layer 2 / Agent API-CLI 2 → **частичная замена**
- Pipedrive: CRM 3 / Pipeline 3 / KPI 1 / Decision 1 / Event 1 / Agent 2 → **частичная замена**
- Bitrix24: CRM 3 / Pipeline 3 / KPI 1 / Decision 1 / Event 1 / Agent 1 → **частичная замена**
- amoCRM: CRM 3 / Pipeline 3 / KPI 1 / Decision 1 / Event 1 / Agent 1 → **частичная замена**

### 3.2 OMS/ERP
- Odoo: CRM 2 / Pipeline 2 / KPI 2 / Decision 1 / Event 1 / Agent 1 → **сильная база, но нужен слой оркестрации**
- ERPNext: CRM 2 / Pipeline 2 / KPI 2 / Decision 1 / Event 1 / Agent 1 → **сильная база, но нужен слой оркестрации**
- Sellercloud/Linnworks/Skubana: CRM 1 / Pipeline 1 / KPI 2 / Decision 0 / Event 1 / Agent 1 → **операционный контур, не CRM-control tower**

### 3.3 Marketplace-интеграторы
- ChannelEngine/Channable/Lengow/ChannelAdvisor:
  CRM 0 / Pipeline 0 / KPI 1 / Decision 0 / Event 1 / Agent 1 → **не заменяют CRM-control tower**

### 3.4 Analytics-инструменты
- DataHawk/Helium10/JungleScout/Perpetua/MPStats:
  CRM 0 / Pipeline 0 / KPI 3 / Decision 1 / Event 0-1 / Agent 0-1 → **аналитический слой, не CRM-ядро**

## 4) Главный вывод

На рынке почти нет решения, которое одновременно даёт:
1) CRM-процессы,
2) marketplace-native метрики и управленческий контур,
3) event-driven трассируемость,
4) агентный интерфейс (API/CLI) как first-class.

Поэтому стратегия "собственное ядро + точечные интеграции" остаётся правильной.

## 5) Практическая стратегия интеграций (recommended)

- CRM-процесс и decision-loop: держим в нашем ядре.
- Marketplace данные: забираем через коннекторы/выгрузки (WB/Ozon/другие источники).
- При необходимости внешней CRM: используем как front-of-funnel, но источник истины для control tower — наш домен.
- Event contracts v1: фиксируем как внутренний стандарт интеграций.

## 6) Где внешний софт реально полезен уже сейчас

- Odoo/ERPNext: как back-office и мастер-данные (если понадобится ERP-слой).
- ChannelEngine/Channable: при мультиканальной экспансии в будущем.
- Analytics tools: как дополнительная верификация KPI/прогнозов, но не как система принятия решений.

## 7) Следующий шаг (в проекте)

Собрать **vendor matrix v1** в machine-readable JSON (для агента выбора стека):
- `docs/vendor_matrix.v1.json`
- критерии: стоимость, API, webhooks, latency интеграции, сложность внедрения, vendor lock-in, соответствие 9 контекстам.

Это позволит автоматически рекомендовать стек под сценарий (MVP / growth / enterprise).