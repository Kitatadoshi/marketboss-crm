# AGENT_OPERATING_MODEL.md

Дата: 2026-02-26

## Цель
Сделать MarketBoss CRM не просто системой учёта, а **AI-native операционной платформой**: агенты действуют, анализируют, мониторят процессы и дают рекомендации в реальном времени.

## Принципы
- Human-in-the-loop для рискованных действий.
- Все действия агентов трассируются (event log + audit).
- Любое советующее действие должно иметь объяснение и ожидаемый эффект.
- API/CLI — first-class интерфейсы для агентной оркестрации.

## Роли агентов (v1)
1. **Operator Agent**
   - CRUD в лидах/сделках/метриках/решениях.
   - Перевод стадий pipeline по правилам.
2. **Analyst Agent**
   - Расчёт KPI, диагностика просадок, weekly summary.
3. **Watcher Agent**
   - Мониторинг realtime-сигналов, алерты по SLA/аномалиям.
4. **Advisor Agent**
   - Next Best Action (NBA), гипотезы и ожидаемый impact.

## Контур исполнения
1) Событие/данные поступают в систему.
2) Watcher/Analyst формируют сигнал.
3) Advisor формирует рекомендацию (действие + why + expected effect).
4) Operator выполняет (или запрашивает подтверждение человека).
5) Результат фиксируется в decision log и event log.

## Уровни автономности (v1)
- **L0 Manual**: агент только предлагает.
- **L1 Assisted**: агент выполняет безопасные действия автоматически.
- **L2 Guarded Auto**: агент выполняет больше действий в рамках policy.
- **L3 Full Auto (ограниченно)**: только на чётко определённых low-risk сценариях.

## Safety / Governance
- RBAC + policy-check перед action.
- Risk scoring для действий (low/medium/high).
- Для medium/high: approval workflow.
- Full audit trail: кто/что/когда/почему/ожидаемый эффект/факт.

## KPI для agent-слоя
- MTTA/MTTR по алертам.
- % рекомендаций с подтверждённым положительным эффектом.
- Скорость прохождения стадий pipeline.
- Доля действий, выполненных без ручного вмешательства (при сохранении качества).

## План внедрения
- V1: базовые agent actions + rule-based alerts + decision log.
- V2: scoring/приоритизация рекомендаций + approval matrix.
- V3: semi-autonomous playbooks + continuous learning loop.
