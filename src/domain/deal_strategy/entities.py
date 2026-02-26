from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from src.shared.types import DealStage, Platform


class Deal(BaseModel):
    id: str = Field(min_length=1)
    lead_id: str = Field(min_length=1)
    stage: DealStage = DealStage.DIAGNOSTIC
    platform: Platform
    target_revenue: float = Field(ge=0)
    risk_profile: str = Field(pattern=r"^(low|medium|high)$")
    owner: str = Field(min_length=1)
    created_at: datetime
