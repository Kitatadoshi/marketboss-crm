# Context Map (v2, RAG-driven)

Контексты определены по устойчивым capability-кластерам из RAG-базы, чтобы не переделывать при росте данных.

## 1) acquisition_qualification
**Отдел:** Лиды и квалификация
**Ответственность:** inbound-лиды, первичная диагностика, ICP fit, приоритизация.
**Сущности:** Lead, QualificationProfile
**События:** `lead.created`, `lead.qualified`, `lead.lost`

## 2) niche_offer_strategy
**Отдел:** Ниши и продуктовая стратегия
**Ответственность:** выбор ниши, конкурентка, формирование SKU-гипотез.
**Сущности:** NicheHypothesis, OfferStrategy
**События:** `niche.hypothesis.created`, `niche.validated`, `offer.strategy.approved`

## 3) sourcing_supply_chain
**Отдел:** Закупки и supply chain
**Ответственность:** поставщики, закуп, Китай-контур, логистика, поставки, склады.
**Сущности:** Supplier, PurchaseBatch, ShipmentPlan
**События:** `supplier.approved`, `purchase.placed`, `shipment.dispatched`, `shipment.received`

## 4) listing_content_optimization
**Отдел:** Карточка и контент
**Ответственность:** фото/инфографика/описание/SEO, работа с отзывами и конверсией карточки.
**Сущности:** ListingCard, ContentRevision
**События:** `listing.created`, `listing.updated`, `content.tested`

## 5) promotion_traffic
**Отдел:** Реклама, акции, трафик
**Ответственность:** внутренний трафик, реклама, промо-циклы, контроль CTR/CR.
**Сущности:** Campaign, PromoRule, TrafficExperiment
**События:** `campaign.started`, `promo.applied`, `traffic.experiment.finished`

## 6) unit_economics_pricing
**Отдел:** Юнит-экономика и цена
**Ответственность:** маржа, пороги, сценарии цены/скидки, go/no-go.
**Сущности:** UnitEconomicsModel, PricingScenario
**События:** `economics.calculated`, `pricing.scenario.approved`, `margin.threshold.breached`

## 7) operations_platform_execution
**Отдел:** Операционка платформ
**Ответственность:** кабинетные операции WB/Ozon, SLA задач, статусы запуска/масштаба.
**Сущности:** ExecutionTask, PlatformOperation
**События:** `operation.scheduled`, `operation.completed`, `operation.failed`

## 8) analytics_control_tower
**Отдел:** Аналитика и контроль
**Ответственность:** воронка, KPI, weekly review, алерты, решение по масштабированию.
**Сущности:** MetricSnapshot, KPIBoard, WeeklyReview
**События:** `metric.snapshot.recorded`, `weekly.review.published`, `alert.triggered`

## 9) knowledge_playbooks
**Отдел:** База знаний и плейбуки
**Ответственность:** RAG-источники, извлечение практик, канонические playbook’и.
**Сущности:** KnowledgeCard, Playbook, SourceDocument
**События:** `source.ingested`, `playbook.published`, `knowledge.versioned`

---

## Основные потоки между отделами
- `acquisition_qualification -> niche_offer_strategy` (квалифицированный спрос)
- `niche_offer_strategy -> unit_economics_pricing` (гипотеза в фин-модель)
- `unit_economics_pricing -> sourcing_supply_chain / promotion_traffic` (лимиты и пороги)
- `listing_content_optimization + promotion_traffic + sourcing_supply_chain -> analytics_control_tower`
- `knowledge_playbooks -> all` (стандарты и best practices)

## Граница контекстов
Только события/контракты. Прямые вызовы между доменными контекстами запрещены.
