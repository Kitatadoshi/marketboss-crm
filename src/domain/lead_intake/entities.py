from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from src.shared.types import LeadStatus


class Lead(BaseModel):
    id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    name: str = Field(min_length=1)
    contact: str = Field(min_length=1)
    status: LeadStatus = LeadStatus.NEW
    budget_hint: float | None = Field(default=None, ge=0)
    created_at: datetime
