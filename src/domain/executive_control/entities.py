from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DecisionLog(BaseModel):
    id: str = Field(min_length=1)
    deal_id: str = Field(min_length=1)
    decision_type: str = Field(min_length=1)
    decision_text: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    expected_effect: str = Field(min_length=1)
    created_at: datetime


class Recommendation(BaseModel):
    id: str = Field(min_length=1)
    deal_id: str = Field(min_length=1)
    action_type: str = Field(min_length=1)
    why_text: str = Field(min_length=1)
    expected_effect: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    status: str = Field(min_length=1)
    created_at: datetime
    approved_at: datetime | None = None
    rejected_at: datetime | None = None
