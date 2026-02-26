from __future__ import annotations

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / 'data' / 'db' / 'crm.sqlite3'


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_column(cur: sqlite3.Cursor, table: str, column: str, ddl: str) -> None:
    cols = cur.execute(f"PRAGMA table_info({table})").fetchall()
    existing = {r[1] for r in cols}
    if column not in existing:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            status TEXT NOT NULL,
            budget_hint REAL,
            created_at TEXT NOT NULL
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS deals (
            id TEXT PRIMARY KEY,
            lead_id TEXT NOT NULL,
            stage TEXT NOT NULL,
            platform TEXT NOT NULL,
            target_revenue REAL NOT NULL,
            risk_profile TEXT NOT NULL,
            owner TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(lead_id) REFERENCES leads(id)
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS metric_snapshots (
            id TEXT PRIMARY KEY,
            deal_id TEXT NOT NULL,
            snapshot_date TEXT NOT NULL,
            impressions INTEGER NOT NULL,
            clicks INTEGER NOT NULL,
            orders_count INTEGER NOT NULL,
            buyouts INTEGER NOT NULL,
            revenue REAL NOT NULL,
            gross_profit REAL NOT NULL,
            FOREIGN KEY(deal_id) REFERENCES deals(id)
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS decision_logs (
            id TEXT PRIMARY KEY,
            deal_id TEXT NOT NULL,
            decision_type TEXT NOT NULL,
            decision_text TEXT NOT NULL,
            owner TEXT NOT NULL,
            expected_effect TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(deal_id) REFERENCES deals(id)
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS event_logs (
            id TEXT PRIMARY KEY,
            event_name TEXT NOT NULL,
            aggregate_type TEXT NOT NULL,
            aggregate_id TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            event_version INTEGER NOT NULL DEFAULT 1,
            producer TEXT NOT NULL DEFAULT 'system',
            correlation_id TEXT,
            causation_id TEXT,
            actor_type TEXT NOT NULL DEFAULT 'system',
            actor_id TEXT NOT NULL DEFAULT 'system',
            risk_level TEXT NOT NULL DEFAULT 'low'
        )
        '''
    )

    _ensure_column(cur, 'event_logs', 'event_version', 'event_version INTEGER NOT NULL DEFAULT 1')
    _ensure_column(cur, 'event_logs', 'producer', "producer TEXT NOT NULL DEFAULT 'system'")
    _ensure_column(cur, 'event_logs', 'correlation_id', 'correlation_id TEXT')
    _ensure_column(cur, 'event_logs', 'causation_id', 'causation_id TEXT')
    _ensure_column(cur, 'event_logs', 'actor_type', "actor_type TEXT NOT NULL DEFAULT 'system'")
    _ensure_column(cur, 'event_logs', 'actor_id', "actor_id TEXT NOT NULL DEFAULT 'system'")
    _ensure_column(cur, 'event_logs', 'risk_level', "risk_level TEXT NOT NULL DEFAULT 'low'")

    conn.commit()
    conn.close()
