# MarketBoss CRM Core

CRM-ядро для управления запуском и ростом на маркетплейсах:
- Clean Architecture + DDD
- Python-only, strict typing
- API/CLI для агентов
- Web dashboard для человека

## Что внутри (MVP)
- Leads
- Deals (pipeline)
- Metric Snapshots
- Decision Log
- Control dashboard

## Быстрый старт (Docker)
```bash
docker compose up --build
```
Открыть:
- UI: http://localhost:8080
- Health: http://localhost:8080/health
- API: http://localhost:8080/api/leads

### Загрузить демо-данные в Docker
```bash
./scripts/seed_docker.sh
```

## Локальный запуск (без Docker)
```bash
PYTHONPATH=. python3 scripts/seed_demo.py
PYTHONPATH=. python3 -m uvicorn src.interfaces.http.app:app --host 0.0.0.0 --port 8080 --reload
```

## CLI (для агентов)
```bash
PYTHONPATH=. python3 -m src.interfaces.cli list leads
PYTHONPATH=. python3 -m src.interfaces.cli add-lead --source telegram --name "Test" --contact "@test"
PYTHONPATH=. python3 -m src.interfaces.cli list deals
```

## API endpoints (v1)
- `GET /health`
- `GET/POST /api/leads`
- `GET/POST /api/deals`
- `GET/POST /api/metrics`
- `GET/POST /api/decisions`

## Контексты
См. `docs/CONTEXT_MAP.md` (RAG-driven модель контекстов).
