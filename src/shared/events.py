from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Mapping


@dataclass(frozen=True, slots=True)
class DomainEvent:
    name: str
    payload: Mapping[str, object]
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
