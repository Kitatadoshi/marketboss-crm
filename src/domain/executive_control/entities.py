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
