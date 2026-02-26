from __future__ import annotations

from datetime import date
from uuid import uuid4

from src.application import services
from src.domain.analytics_bi.entities import MetricSnapshot
from src.infrastructure.persistence import init_db
from src.shared.types import Platform


def main() -> None:
    init_db()
    lead = services.create_lead('telegram', 'Demo Seller', '@demo_seller', 300000)
    deal = services.create_deal(lead.id, Platform.WB, 1_000_000, 'medium', 'marketboss')
    services.create_metric_snapshot(
        MetricSnapshot(
            id=f'metric_{uuid4().hex[:10]}',
            deal_id=deal.id,
            snapshot_date=date.today(),
            impressions=1000,
            clicks=45,
            orders=8,
            buyouts=6,
            revenue=35000,
            gross_profit=9000,
        )
    )
    services.create_decision_log(
        deal.id,
        'go_no_go',
        'Запускаем тест SKU в нише аксессуаров.',
        'marketboss',
        'Получить первые 30 заказов за 14 дней.',
    )
    print('✅ Seed created', lead.id, deal.id)


if __name__ == '__main__':
    main()
