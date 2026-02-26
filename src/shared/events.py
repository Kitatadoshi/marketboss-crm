from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class ActorType(str, Enum):
    AGENT = 'agent'
    HUMAN = 'human'
    SYSTEM = 'system'


class RiskLevel(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class EventMeta(BaseModel):
    actor_type: ActorType = ActorType.SYSTEM
    actor_id: str = 'system'
    risk_level: RiskLevel = RiskLevel.LOW


class EventEnvelope(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid4().hex[:12]}")
    event_name: str
    event_version: int = 1
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    producer: str
    aggregate_type: str
    aggregate_id: str
    correlation_id: str | None = None
    causation_id: str | None = None
    payload: dict[str, object] = Field(default_factory=dict)
    meta: EventMeta = Field(default_factory=EventMeta)
