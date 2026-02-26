# Next Steps

## Sprint 1.1
1. Перенести текущие модули в целевую структуру `domain/application/infrastructure/interfaces`
2. Ввести базовый `EventBus` интерфейс + in-memory реализацию
3. Ввести domain events для Lead/Deal/Task/Metric
4. Зафиксировать контракты репозиториев на уровне domain

## Sprint 1.2
1. Добавить HTTP слой (Bootstrap-страницы):
   - Leads board
   - Deal pipeline
   - Task board
   - Metrics summary
2. Подключить SQLite адаптер
3. Добавить миграции начальной схемы

## Sprint 1.3
1. Добавить журнал событий (event log)
2. Добавить weekly report генератор
3. Добавить HADI модуль как bounded context
