from __future__ import annotations

from enum import StrEnum


class LeadStatus(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    LOST = "lost"


class DealStage(StrEnum):
    DIAGNOSTIC = "diagnostic"
    NICHE_TEST = "niche_test"
    ECONOMICS = "economics"
    LAUNCH = "launch"
    OPTIMIZE = "optimize"
    SCALE = "scale"
    WON = "won"
    LOST = "lost"


class Platform(StrEnum):
    WB = "wb"
    OZON = "ozon"
    BOTH = "both"
