from __future__ import annotations

import asyncio
import json
from datetime import date
from pathlib import Path
from typing import AsyncGenerator
from uuid import uuid4

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.application import services
from src.domain.analytics_bi.entities import MetricSnapshot
from src.infrastructure.persistence import init_db
from src.shared.types import DealStage, Platform

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

app = FastAPI(title='MarketBoss CRM Core', version='0.3.0')
app.mount('/static', StaticFiles(directory=str(BASE_DIR / 'static')), name='static')

PIPELINE_ORDER: list[DealStage] = [
    DealStage.DIAGNOSTIC,
    DealStage.NICHE_TEST,
    DealStage.ECONOMICS,
    DealStage.LAUNCH,
    DealStage.OPTIMIZE,
    DealStage.SCALE,
]


class LeadIn(BaseModel):
    source: str = Field(min_length=1)
    name: str = Field(min_length=1)
    contact: str = Field(min_length=1)
    budget_hint: float | None = Field(default=None, ge=0)


class DealIn(BaseModel):
    lead_id: str
    platform: Platform
    target_revenue: float = Field(ge=0)
    risk_profile: str
    owner: str


class DecisionIn(BaseModel):
    deal_id: str
    decision_type: str
    decision_text: str
    owner: str
    expected_effect: str


class MetricIn(BaseModel):
    deal_id: str
    snapshot_date: date
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    orders: int = Field(ge=0)
    buyouts: int = Field(ge=0)
    revenue: float = Field(ge=0)
    gross_profit: float


@app.on_event('startup')
def on_startup() -> None:
    init_db()


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


def _realtime_snapshot() -> dict[str, object]:
    events = services.list_event_logs(20)
    alerts = services.refresh_alerts()
    return {
        'events': events,
        'alerts': alerts,
        'event_count': len(events),
    }


@app.get('/', response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    leads = services.list_leads()
    deals = services.list_deals()
    metrics = services.list_metric_snapshots()
    decisions = services.list_decision_logs()
    events = services.list_event_logs(60)

    revenue_total = round(sum(m.revenue for m in metrics), 2)
    gross_profit_total = round(sum(m.gross_profit for m in metrics), 2)

    stage_counts: dict[str, int] = {}
    stage_board: dict[str, list[object]] = {stage.value: [] for stage in PIPELINE_ORDER}
    for d in deals:
        stage_counts[d.stage.value] = stage_counts.get(d.stage.value, 0) + 1
        if d.stage.value in stage_board:
            stage_board[d.stage.value].append(d)

    alerts = services.refresh_alerts()

    return templates.TemplateResponse(
        request,
        'dashboard.html',
        {
            'leads': leads,
            'deals': deals,
            'metrics': metrics[:20],
            'decisions': decisions[:20],
            'events': events,
            'alerts': alerts,
            'stage_counts': stage_counts,
            'stage_board': stage_board,
            'pipeline_order': [s.value for s in PIPELINE_ORDER],
            'kpi': {
                'leads': len(leads),
                'deals': len(deals),
                'snapshots': len(metrics),
                'revenue_total': revenue_total,
                'gross_profit_total': gross_profit_total,
            },
        },
    )


@app.post('/web/leads')
def create_lead_web(
    source: str = Form(...),
    name: str = Form(...),
    contact: str = Form(...),
    budget_hint: float | None = Form(default=None),
) -> RedirectResponse:
    payload = LeadIn(source=source, name=name, contact=contact, budget_hint=budget_hint)
    services.create_lead(payload.source, payload.name, payload.contact, payload.budget_hint)
    return RedirectResponse(url='/', status_code=303)


@app.post('/web/deals')
def create_deal_web(
    lead_id: str = Form(...),
    platform: str = Form(...),
    target_revenue: float = Form(...),
    risk_profile: str = Form(...),
    owner: str = Form(...),
) -> RedirectResponse:
    payload = DealIn(
        lead_id=lead_id,
        platform=Platform(platform),
        target_revenue=target_revenue,
        risk_profile=risk_profile,
        owner=owner,
    )
    services.create_deal(
        payload.lead_id,
        payload.platform,
        payload.target_revenue,
        payload.risk_profile,
        payload.owner,
    )
    return RedirectResponse(url='/', status_code=303)


@app.post('/web/deals/stage')
def update_deal_stage_web(deal_id: str = Form(...), stage: str = Form(...)) -> RedirectResponse:
    services.update_deal_stage(deal_id, DealStage(stage))
    return RedirectResponse(url='/', status_code=303)


@app.post('/web/metrics')
def create_metric_web(
    deal_id: str = Form(...),
    snapshot_date: str = Form(...),
    impressions: int = Form(...),
    clicks: int = Form(...),
    orders: int = Form(...),
    buyouts: int = Form(...),
    revenue: float = Form(...),
    gross_profit: float = Form(...),
) -> RedirectResponse:
    payload = MetricIn(
        deal_id=deal_id,
        snapshot_date=date.fromisoformat(snapshot_date),
        impressions=impressions,
        clicks=clicks,
        orders=orders,
        buyouts=buyouts,
        revenue=revenue,
        gross_profit=gross_profit,
    )
    item = MetricSnapshot(id=f'metric_{uuid4().hex[:10]}', **payload.model_dump())
    services.create_metric_snapshot(item)
    return RedirectResponse(url='/', status_code=303)


@app.post('/web/decisions')
def create_decision_web(
    deal_id: str = Form(...),
    decision_type: str = Form(...),
    decision_text: str = Form(...),
    owner: str = Form(...),
    expected_effect: str = Form(...),
) -> RedirectResponse:
    payload = DecisionIn(
        deal_id=deal_id,
        decision_type=decision_type,
        decision_text=decision_text,
        owner=owner,
        expected_effect=expected_effect,
    )
    services.create_decision_log(
        payload.deal_id,
        payload.decision_type,
        payload.decision_text,
        payload.owner,
        payload.expected_effect,
    )
    return RedirectResponse(url='/', status_code=303)


@app.get('/api/leads')
def list_leads_api() -> list[dict[str, object]]:
    return [item.model_dump(mode='json') for item in services.list_leads()]


@app.post('/api/leads')
def create_lead_api(payload: LeadIn) -> dict[str, object]:
    item = services.create_lead(payload.source, payload.name, payload.contact, payload.budget_hint)
    return item.model_dump(mode='json')


@app.get('/api/deals')
def list_deals_api() -> list[dict[str, object]]:
    return [item.model_dump(mode='json') for item in services.list_deals()]


@app.post('/api/deals')
def create_deal_api(payload: DealIn) -> dict[str, object]:
    item = services.create_deal(
        payload.lead_id,
        payload.platform,
        payload.target_revenue,
        payload.risk_profile,
        payload.owner,
    )
    return item.model_dump(mode='json')


@app.post('/api/deals/{deal_id}/stage/{stage}')
def update_deal_stage_api(deal_id: str, stage: str) -> dict[str, object]:
    updated = services.update_deal_stage(deal_id, DealStage(stage))
    return {'updated': bool(updated)}


@app.get('/api/metrics')
def list_metrics_api() -> list[dict[str, object]]:
    return [item.model_dump(mode='json') for item in services.list_metric_snapshots()]


@app.post('/api/metrics')
def create_metric_api(payload: MetricIn) -> dict[str, object]:
    item = MetricSnapshot(id=f'metric_{uuid4().hex[:10]}', **payload.model_dump())
    saved = services.create_metric_snapshot(item)
    return saved.model_dump(mode='json')


@app.get('/api/decisions')
def list_decisions_api() -> list[dict[str, object]]:
    return [item.model_dump(mode='json') for item in services.list_decision_logs()]


@app.post('/api/decisions')
def create_decision_api(payload: DecisionIn) -> dict[str, object]:
    item = services.create_decision_log(
        payload.deal_id,
        payload.decision_type,
        payload.decision_text,
        payload.owner,
        payload.expected_effect,
    )
    return item.model_dump(mode='json')


@app.get('/api/events')
def list_events_api() -> list[dict[str, object]]:
    return services.list_event_logs(200)


@app.get('/api/alerts')
def list_alerts_api() -> list[dict[str, object]]:
    return services.refresh_alerts()


@app.post('/api/alerts/{alert_id}/ack')
def ack_alert_api(alert_id: str) -> dict[str, object]:
    return {'updated': services.ack_alert(alert_id)}


@app.post('/api/alerts/{alert_id}/resolve')
def resolve_alert_api(alert_id: str) -> dict[str, object]:
    return {'updated': services.resolve_alert(alert_id)}


@app.get('/api/realtime')
def realtime_snapshot_api() -> dict[str, object]:
    return _realtime_snapshot()


@app.get('/api/events/stream')
async def stream_events() -> StreamingResponse:
    async def event_generator() -> AsyncGenerator[str, None]:
        last_event_id: str | None = None
        while True:
            snapshot = _realtime_snapshot()
            current = snapshot['events'][0]['id'] if snapshot['events'] else None
            if current != last_event_id:
                last_event_id = current
                payload = json.dumps(snapshot, ensure_ascii=False)
                yield f"event: snapshot\ndata: {payload}\n\n"
            await asyncio.sleep(2)

    return StreamingResponse(event_generator(), media_type='text/event-stream')
