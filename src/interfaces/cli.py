from __future__ import annotations

import argparse
import json
from datetime import date
from uuid import uuid4

from src.application import services
from src.domain.analytics_bi.entities import MetricSnapshot
from src.shared.types import DealStage, Platform
from src.infrastructure.persistence import init_db


def _print(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def cmd_list(entity: str) -> None:
    if entity == 'leads':
        _print([x.model_dump(mode='json') for x in services.list_leads()])
    elif entity == 'deals':
        _print([x.model_dump(mode='json') for x in services.list_deals()])
    elif entity == 'metrics':
        _print([x.model_dump(mode='json') for x in services.list_metric_snapshots()])
    elif entity == 'decisions':
        _print([x.model_dump(mode='json') for x in services.list_decision_logs()])
    elif entity == 'events':
        _print(services.list_event_logs(200))


def main() -> None:
    init_db()
    parser = argparse.ArgumentParser(prog='crm')
    sub = parser.add_subparsers(dest='cmd', required=True)

    list_p = sub.add_parser('list')
    list_p.add_argument('entity', choices=['leads', 'deals', 'metrics', 'decisions', 'events'])

    add_lead = sub.add_parser('add-lead')
    add_lead.add_argument('--source', required=True)
    add_lead.add_argument('--name', required=True)
    add_lead.add_argument('--contact', required=True)
    add_lead.add_argument('--budget-hint', type=float, default=None)

    add_deal = sub.add_parser('add-deal')
    add_deal.add_argument('--lead-id', required=True)
    add_deal.add_argument('--platform', choices=['wb', 'ozon', 'both'], required=True)
    add_deal.add_argument('--target-revenue', type=float, required=True)
    add_deal.add_argument('--risk-profile', choices=['low', 'medium', 'high'], required=True)
    add_deal.add_argument('--owner', required=True)

    add_metric = sub.add_parser('add-metric')
    add_metric.add_argument('--deal-id', required=True)
    add_metric.add_argument('--date', required=True)
    add_metric.add_argument('--impressions', type=int, required=True)
    add_metric.add_argument('--clicks', type=int, required=True)
    add_metric.add_argument('--orders', type=int, required=True)
    add_metric.add_argument('--buyouts', type=int, required=True)
    add_metric.add_argument('--revenue', type=float, required=True)
    add_metric.add_argument('--gross-profit', type=float, required=True)


    move_stage = sub.add_parser('move-deal-stage')
    move_stage.add_argument('--deal-id', required=True)
    move_stage.add_argument('--stage', choices=['diagnostic','niche_test','economics','launch','optimize','scale','won','lost'], required=True)

    add_decision = sub.add_parser('add-decision')
    add_decision.add_argument('--deal-id', required=True)
    add_decision.add_argument('--decision-type', required=True)
    add_decision.add_argument('--decision-text', required=True)
    add_decision.add_argument('--owner', required=True)
    add_decision.add_argument('--expected-effect', required=True)

    args = parser.parse_args()

    if args.cmd == 'list':
        cmd_list(args.entity)
    elif args.cmd == 'add-lead':
        item = services.create_lead(args.source, args.name, args.contact, args.budget_hint)
        _print(item.model_dump(mode='json'))
    elif args.cmd == 'add-deal':
        item = services.create_deal(
            args.lead_id,
            Platform(args.platform),
            args.target_revenue,
            args.risk_profile,
            args.owner,
        )
        _print(item.model_dump(mode='json'))
    elif args.cmd == 'add-metric':
        m = MetricSnapshot(
            id=f'metric_{uuid4().hex[:10]}',
            deal_id=args.deal_id,
            snapshot_date=date.fromisoformat(args.date),
            impressions=args.impressions,
            clicks=args.clicks,
            orders=args.orders,
            buyouts=args.buyouts,
            revenue=args.revenue,
            gross_profit=args.gross_profit,
        )
        saved = services.create_metric_snapshot(m)
        _print(saved.model_dump(mode='json'))
    elif args.cmd == 'move-deal-stage':
        updated = services.update_deal_stage(args.deal_id, DealStage(args.stage))
        _print({'updated': bool(updated), 'deal_id': args.deal_id, 'stage': args.stage})
    elif args.cmd == 'add-decision':
        item = services.create_decision_log(
            args.deal_id,
            args.decision_type,
            args.decision_text,
            args.owner,
            args.expected_effect,
        )
        _print(item.model_dump(mode='json'))


if __name__ == '__main__':
    main()
