from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class MetricSnapshot(BaseModel):
    id: str = Field(min_length=1)
    deal_id: str = Field(min_length=1)
    snapshot_date: date
    impressions: int = Field(ge=0)
    clicks: int = Field(ge=0)
    orders: int = Field(ge=0)
    buyouts: int = Field(ge=0)
    revenue: float = Field(ge=0)
    gross_profit: float

    @property
    def ctr(self) -> float:
        return (self.clicks / self.impressions) if self.impressions else 0.0

    @property
    def cr_order(self) -> float:
        return (self.orders / self.clicks) if self.clicks else 0.0
