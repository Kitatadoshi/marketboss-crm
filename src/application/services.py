from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from uuid import uuid4

from src.domain.analytics_bi.entities import MetricSnapshot
from src.domain.deal_strategy.entities import Deal
from src.domain.executive_control.entities import DecisionLog
from src.domain.lead_intake.entities import Lead
from src.infrastructure.persistence import get_conn
from src.shared.events import ActorType, EventEnvelope, EventMeta, RiskLevel
from src.shared.types import DealStage, LeadStatus, Platform


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _log_event(
    conn: sqlite3.Connection,
    event_name: str,
    aggregate_type: str,
    aggregate_id: str,
    payload: dict[str, object],
    *,
    producer: str,
    actor_type: ActorType = ActorType.SYSTEM,
    actor_id: str = 'system',
    risk_level: RiskLevel = RiskLevel.LOW,
    correlation_id: str | None = None,
    causation_id: str | None = None,
    event_id: str | None = None,
) -> None:
    event = EventEnvelope(
        event_id=event_id or f"evt_{uuid4().hex[:12]}",
        event_name=event_name,
        event_version=1,
        producer=producer,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        correlation_id=correlation_id,
        causation_id=causation_id,
        payload=payload,
        meta=EventMeta(actor_type=actor_type, actor_id=actor_id, risk_level=risk_level),
    )

    conn.execute(
        """
        INSERT OR IGNORE INTO event_logs (
            id,event_name,aggregate_type,aggregate_id,payload_json,created_at,
            event_version,producer,correlation_id,causation_id,actor_type,actor_id,risk_level
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            event.event_id,
            event.event_name,
            event.aggregate_type,
            event.aggregate_id,
            json.dumps(event.payload, ensure_ascii=False),
            event.occurred_at.isoformat(),
            event.event_version,
            event.producer,
            event.correlation_id,
            event.causation_id,
            event.meta.actor_type.value,
            event.meta.actor_id,
            event.meta.risk_level.value,
        ),
    )


def create_lead(source: str, name: str, contact: str, budget_hint: float | None) -> Lead:
    lead = Lead(
        id=_new_id('lead'),
        source=source,
        name=name,
        contact=contact,
        status=LeadStatus.NEW,
        budget_hint=budget_hint,
        created_at=datetime.now(UTC),
    )
    conn = get_conn()
    conn.execute(
        "INSERT INTO leads (id,source,name,contact,status,budget_hint,created_at) VALUES (?,?,?,?,?,?,?)",
        (
            lead.id,
            lead.source,
            lead.name,
            lead.contact,
            lead.status.value,
            lead.budget_hint,
            lead.created_at.isoformat(),
        ),
    )
    _log_event(
        conn,
        'lead.created',
        'lead',
        lead.id,
        {'source': lead.source, 'name': lead.name, 'status': lead.status.value},
        producer='lead_intake',
        actor_type=ActorType.AGENT,
        actor_id='marketboss',
    )
    conn.commit()
    conn.close()
    return lead


def list_leads() -> list[Lead]:
    conn = get_conn()
    rows = conn.execute('SELECT * FROM leads ORDER BY created_at DESC').fetchall()
    conn.close()
    return [
        Lead(
            id=r['id'],
            source=r['source'],
            name=r['name'],
            contact=r['contact'],
            status=LeadStatus(r['status']),
            budget_hint=r['budget_hint'],
            created_at=datetime.fromisoformat(r['created_at']),
        )
        for r in rows
    ]


def create_deal(
    lead_id: str,
    platform: Platform,
    target_revenue: float,
    risk_profile: str,
    owner: str,
) -> Deal:
    deal = Deal(
        id=_new_id('deal'),
        lead_id=lead_id,
        stage=DealStage.DIAGNOSTIC,
        platform=platform,
        target_revenue=target_revenue,
        risk_profile=risk_profile,
        owner=owner,
        created_at=datetime.now(UTC),
    )
    conn = get_conn()
    conn.execute(
        'INSERT INTO deals (id,lead_id,stage,platform,target_revenue,risk_profile,owner,created_at) VALUES (?,?,?,?,?,?,?,?)',
        (
            deal.id,
            deal.lead_id,
            deal.stage.value,
            deal.platform.value,
            deal.target_revenue,
            deal.risk_profile,
            deal.owner,
            deal.created_at.isoformat(),
        ),
    )
    _log_event(
        conn,
        'deal.created',
        'deal',
        deal.id,
        {'stage': deal.stage.value, 'platform': deal.platform.value, 'owner': deal.owner},
        producer='deal_strategy',
        actor_type=ActorType.AGENT,
        actor_id=deal.owner,
    )
    conn.commit()
    conn.close()
    return deal


def update_deal_stage(deal_id: str, stage: DealStage) -> Deal | None:
    conn = get_conn()
    row = conn.execute('SELECT * FROM deals WHERE id = ?', (deal_id,)).fetchone()
    if row is None:
        conn.close()
        return None

    conn.execute('UPDATE deals SET stage = ? WHERE id = ?', (stage.value, deal_id))
    _log_event(
        conn,
        'deal.stage.changed',
        'deal',
        deal_id,
        {'from': row['stage'], 'to': stage.value},
        producer='deal_strategy',
        actor_type=ActorType.AGENT,
        actor_id='marketboss',
        risk_level=RiskLevel.MEDIUM,
    )
    conn.commit()
    updated = conn.execute('SELECT * FROM deals WHERE id = ?', (deal_id,)).fetchone()
    conn.close()

    if updated is None:
        return None
    return Deal(
        id=updated['id'],
        lead_id=updated['lead_id'],
        stage=DealStage(updated['stage']),
        platform=Platform(updated['platform']),
        target_revenue=updated['target_revenue'],
        risk_profile=updated['risk_profile'],
        owner=updated['owner'],
        created_at=datetime.fromisoformat(updated['created_at']),
    )


def list_deals() -> list[Deal]:
    conn = get_conn()
    rows = conn.execute('SELECT * FROM deals ORDER BY created_at DESC').fetchall()
    conn.close()
    return [
        Deal(
            id=r['id'],
            lead_id=r['lead_id'],
            stage=DealStage(r['stage']),
            platform=Platform(r['platform']),
            target_revenue=r['target_revenue'],
            risk_profile=r['risk_profile'],
            owner=r['owner'],
            created_at=datetime.fromisoformat(r['created_at']),
        )
        for r in rows
    ]


def create_metric_snapshot(snapshot: MetricSnapshot) -> MetricSnapshot:
    conn = get_conn()
    conn.execute(
        'INSERT INTO metric_snapshots (id,deal_id,snapshot_date,impressions,clicks,orders_count,buyouts,revenue,gross_profit) VALUES (?,?,?,?,?,?,?,?,?)',
        (
            snapshot.id,
            snapshot.deal_id,
            snapshot.snapshot_date.isoformat(),
            snapshot.impressions,
            snapshot.clicks,
            snapshot.orders,
            snapshot.buyouts,
            snapshot.revenue,
            snapshot.gross_profit,
        ),
    )
    _log_event(
        conn,
        'metric.snapshot.recorded',
        'metric_snapshot',
        snapshot.id,
        {
            'deal_id': snapshot.deal_id,
            'revenue': snapshot.revenue,
            'gross_profit': snapshot.gross_profit,
            'ctr': snapshot.ctr,
            'cr_order': snapshot.cr_order,
        },
        producer='analytics_bi',
        actor_type=ActorType.AGENT,
        actor_id='marketboss',
    )
    conn.commit()
    conn.close()
    return snapshot


def list_metric_snapshots() -> list[MetricSnapshot]:
    conn = get_conn()
    rows = conn.execute('SELECT * FROM metric_snapshots ORDER BY snapshot_date DESC').fetchall()
    conn.close()
    return [
        MetricSnapshot(
            id=r['id'],
            deal_id=r['deal_id'],
            snapshot_date=datetime.fromisoformat(r['snapshot_date']).date(),
            impressions=r['impressions'],
            clicks=r['clicks'],
            orders=r['orders_count'],
            buyouts=r['buyouts'],
            revenue=r['revenue'],
            gross_profit=r['gross_profit'],
        )
        for r in rows
    ]


def create_decision_log(
    deal_id: str,
    decision_type: str,
    decision_text: str,
    owner: str,
    expected_effect: str,
) -> DecisionLog:
    item = DecisionLog(
        id=_new_id('decision'),
        deal_id=deal_id,
        decision_type=decision_type,
        decision_text=decision_text,
        owner=owner,
        expected_effect=expected_effect,
        created_at=datetime.now(UTC),
    )
    conn = get_conn()
    conn.execute(
        'INSERT INTO decision_logs (id,deal_id,decision_type,decision_text,owner,expected_effect,created_at) VALUES (?,?,?,?,?,?,?)',
        (
            item.id,
            item.deal_id,
            item.decision_type,
            item.decision_text,
            item.owner,
            item.expected_effect,
            item.created_at.isoformat(),
        ),
    )
    _log_event(
        conn,
        'decision.recorded',
        'decision_log',
        item.id,
        {'deal_id': item.deal_id, 'decision_type': item.decision_type, 'owner': item.owner},
        producer='executive_control',
        actor_type=ActorType.AGENT,
        actor_id=item.owner,
        risk_level=RiskLevel.MEDIUM,
    )
    conn.commit()
    conn.close()
    return item


def list_decision_logs() -> list[DecisionLog]:
    conn = get_conn()
    rows = conn.execute('SELECT * FROM decision_logs ORDER BY created_at DESC').fetchall()
    conn.close()
    return [
        DecisionLog(
            id=r['id'],
            deal_id=r['deal_id'],
            decision_type=r['decision_type'],
            decision_text=r['decision_text'],
            owner=r['owner'],
            expected_effect=r['expected_effect'],
            created_at=datetime.fromisoformat(r['created_at']),
        )
        for r in rows
    ]


def list_event_logs(limit: int = 100) -> list[dict[str, object]]:
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM event_logs ORDER BY created_at DESC LIMIT ?',
        (limit,),
    ).fetchall()
    conn.close()
    return [
        {
            'id': r['id'],
            'event_name': r['event_name'],
            'event_version': r['event_version'],
            'producer': r['producer'],
            'aggregate_type': r['aggregate_type'],
            'aggregate_id': r['aggregate_id'],
            'correlation_id': r['correlation_id'],
            'causation_id': r['causation_id'],
            'actor_type': r['actor_type'],
            'actor_id': r['actor_id'],
            'risk_level': r['risk_level'],
            'payload_json': r['payload_json'],
            'created_at': r['created_at'],
        }
        for r in rows
    ]


def _upsert_alert(
    conn: sqlite3.Connection,
    *,
    alert_key: str,
    level: str,
    text: str,
    source_type: str,
    source_id: str,
) -> None:
    now = datetime.now(UTC).isoformat()
    row = conn.execute('SELECT id, status FROM alerts WHERE alert_key = ?', (alert_key,)).fetchone()
    if row is None:
        conn.execute(
            '''
            INSERT INTO alerts (
              id, alert_key, level, text, status, source_type, source_id, first_seen_at, last_seen_at, resolved_at
            ) VALUES (?, ?, ?, ?, 'open', ?, ?, ?, ?, NULL)
            ''',
            (_new_id('alert'), alert_key, level, text, source_type, source_id, now, now),
        )
        return

    if row['status'] == 'resolved':
        conn.execute(
            '''
            UPDATE alerts SET status='open', level=?, text=?, source_type=?, source_id=?, last_seen_at=?, resolved_at=NULL
            WHERE alert_key = ?
            ''',
            (level, text, source_type, source_id, now, alert_key),
        )
    else:
        conn.execute(
            '''
            UPDATE alerts SET level=?, text=?, source_type=?, source_id=?, last_seen_at=?
            WHERE alert_key = ?
            ''',
            (level, text, source_type, source_id, now, alert_key),
        )


def _resolve_stale_alerts(conn: sqlite3.Connection, active_keys: set[str]) -> None:
    rows = conn.execute("SELECT alert_key FROM alerts WHERE status = 'open'").fetchall()
    now = datetime.now(UTC).isoformat()
    for row in rows:
        key = str(row['alert_key'])
        if key not in active_keys:
            conn.execute(
                "UPDATE alerts SET status='resolved', resolved_at=?, last_seen_at=? WHERE alert_key=?",
                (now, now, key),
            )


def refresh_alerts() -> list[dict[str, object]]:
    conn = get_conn()
    metrics = list_metric_snapshots()
    deals = list_deals()

    active_keys: set[str] = set()

    for m in metrics[:50]:
        if m.ctr < 0.02:
            key = f'ctr_low:{m.deal_id}'
            active_keys.add(key)
            _upsert_alert(
                conn,
                alert_key=key,
                level='warning',
                text=f'Низкий CTR ({m.ctr*100:.2f}%) по deal {m.deal_id}',
                source_type='metric',
                source_id=m.id,
            )
        if m.cr_order < 0.05:
            key = f'cr_low:{m.deal_id}'
            active_keys.add(key)
            _upsert_alert(
                conn,
                alert_key=key,
                level='warning',
                text=f'Низкий CR в заказ ({m.cr_order*100:.2f}%) по deal {m.deal_id}',
                source_type='metric',
                source_id=m.id,
            )
        if m.revenue > 0 and (m.gross_profit / m.revenue) < 0.1:
            key = f'margin_low:{m.deal_id}'
            active_keys.add(key)
            _upsert_alert(
                conn,
                alert_key=key,
                level='danger',
                text=f'Низкая маржа (<10%) по deal {m.deal_id}',
                source_type='metric',
                source_id=m.id,
            )

    now = datetime.now(UTC)
    for d in deals:
        if d.stage in {DealStage.WON, DealStage.LOST}:
            continue
        age_days = (now - d.created_at).days
        if age_days >= 7:
            key = f'aging_high:{d.id}'
            active_keys.add(key)
            _upsert_alert(
                conn,
                alert_key=key,
                level='danger',
                text=f'Deal {d.id} застрял на стадии {d.stage.value} уже {age_days} дн.',
                source_type='deal',
                source_id=d.id,
            )
        elif age_days >= 3:
            key = f'aging_warn:{d.id}'
            active_keys.add(key)
            _upsert_alert(
                conn,
                alert_key=key,
                level='warning',
                text=f'Deal {d.id} долго в стадии {d.stage.value}: {age_days} дн.',
                source_type='deal',
                source_id=d.id,
            )

    _resolve_stale_alerts(conn, active_keys)
    conn.commit()
    rows = conn.execute(
        "SELECT * FROM alerts WHERE status='open' ORDER BY CASE level WHEN 'danger' THEN 0 ELSE 1 END, last_seen_at DESC"
    ).fetchall()
    conn.close()

    return [
        {
            'id': r['id'],
            'alert_key': r['alert_key'],
            'level': r['level'],
            'text': r['text'],
            'status': r['status'],
            'source_type': r['source_type'],
            'source_id': r['source_id'],
            'first_seen_at': r['first_seen_at'],
            'last_seen_at': r['last_seen_at'],
            'resolved_at': r['resolved_at'],
        }
        for r in rows
    ]


def list_alerts(status: str = 'open', limit: int = 100) -> list[dict[str, object]]:
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM alerts WHERE status = ? ORDER BY last_seen_at DESC LIMIT ?',
        (status, limit),
    ).fetchall()
    conn.close()
    return [
        {
            'id': r['id'],
            'alert_key': r['alert_key'],
            'level': r['level'],
            'text': r['text'],
            'status': r['status'],
            'source_type': r['source_type'],
            'source_id': r['source_id'],
            'first_seen_at': r['first_seen_at'],
            'last_seen_at': r['last_seen_at'],
            'resolved_at': r['resolved_at'],
        }
        for r in rows
    ]


def ack_alert(alert_id: str) -> bool:
    conn = get_conn()
    cur = conn.execute("UPDATE alerts SET status='ack' WHERE id = ? AND status='open'", (alert_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed


def resolve_alert(alert_id: str) -> bool:
    conn = get_conn()
    now = datetime.now(UTC).isoformat()
    cur = conn.execute(
        "UPDATE alerts SET status='resolved', resolved_at=?, last_seen_at=? WHERE id = ? AND status != 'resolved'",
        (now, now, alert_id),
    )
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed
