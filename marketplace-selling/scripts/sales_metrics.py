#!/usr/bin/env python3
"""Order-log analysis for a multi-channel selling business.

Reads an order log CSV and reports true net margin by channel and product line,
fee drag, refund rate, and which SKUs actually make money -- the numbers that
tell you where a busy-looking business is quietly losing money.

    python sales_metrics.py logs/orders.csv
    python sales_metrics.py logs/orders.csv --channel etsy --since 2026-06-01
    python sales_metrics.py logs/orders.csv --column-map sale_price=Revenue,channel=Marketplace

Expected columns are in assets/order-log-template.csv. Missing optional columns are
tolerated; affected metrics report as unavailable rather than being computed from
partial data.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime

CANONICAL = [
    "order_id", "date", "channel", "product_line", "sku", "qty",
    "sale_price", "shipping_charged", "channel_fees", "shipping_cost",
    "cost_of_goods", "status", "refund_amount", "return_reason", "notes",
]

REFUND_STATUSES = {"refunded", "partial-refund", "partial_refund", "cancelled", "canceled"}


def to_float(value, default=0.0) -> float:
    try:
        t = str(value).strip()
        return float(t) if t else default
    except (TypeError, ValueError):
        return default


def to_date(value):
    t = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            continue
    return None


def load(path: str, column_map: dict[str, str]) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit(f"{path}: no header row found")
        lookup = {}
        for canonical in CANONICAL:
            source = column_map.get(canonical, canonical)
            for field in reader.fieldnames:
                if field.strip().lower() == source.strip().lower():
                    lookup[canonical] = field
                    break
        return [{c: (raw.get(lookup[c], "") if c in lookup else "") for c in CANONICAL}
                for raw in reader]


def net_of(r: dict) -> float:
    """Net profit for one order row: gross received, minus fees, shipping, goods, refund."""
    gross = to_float(r["sale_price"]) + to_float(r["shipping_charged"])
    return (gross - to_float(r["channel_fees"]) - to_float(r["shipping_cost"])
            - to_float(r["cost_of_goods"]) - to_float(r["refund_amount"]))


def is_refunded(r: dict) -> bool:
    return r["status"].strip().lower() in REFUND_STATUSES or to_float(r["refund_amount"]) > 0


def pct(n: float, d: float) -> str:
    return f"{100 * n / d:5.1f}%" if d else "    --"


def money(v: float) -> str:
    return f"{v:,.2f}"


def bar(fraction: float, width: int = 16) -> str:
    filled = int(round(max(0.0, min(1.0, fraction)) * width))
    return "#" * filled + "." * (width - filled)


def section(title: str) -> None:
    print()
    print(title)
    print("-" * max(len(title), 62))


def group_report(rows: list[dict], key: str, label: str, symbol: str) -> list[str]:
    groups = defaultdict(lambda: {"orders": 0, "rev": 0.0, "fees": 0.0, "ship": 0.0,
                                  "net": 0.0, "refunds": 0, "refund_amt": 0.0})
    for r in rows:
        g = groups[r[key].strip() or "(unspecified)"]
        g["orders"] += 1
        g["rev"] += to_float(r["sale_price"]) + to_float(r["shipping_charged"])
        g["fees"] += to_float(r["channel_fees"])
        g["ship"] += to_float(r["shipping_cost"])
        g["net"] += net_of(r)
        if is_refunded(r):
            g["refunds"] += 1
            g["refund_amt"] += to_float(r["refund_amount"])
    if not groups:
        return []

    section(f"BY {label.upper()}")
    print(f"  {label:<14}{'Orders':>7}{'Revenue':>11}{'Net':>11}{'Margin':>8}"
          f"{'FeeDrag':>9}{'Refund%':>9}")
    alarms = []
    for name in sorted(groups, key=lambda n: groups[n]["net"], reverse=True):
        g = groups[name]
        margin = g["net"] / g["rev"] if g["rev"] else 0.0
        drag = (g["fees"] + g["ship"]) / g["rev"] if g["rev"] else 0.0
        print(f"  {name[:13]:<14}{g['orders']:>7}{symbol + money(g['rev']):>11}"
              f"{symbol + money(g['net']):>11}{pct(g['net'], g['rev']):>8}"
              f"{pct(g['fees'] + g['ship'], g['rev']):>9}{pct(g['refunds'], g['orders']):>9}")
        if g["rev"] and margin < 0:
            alarms.append(f"{label} {name!r} is running at a LOSS "
                          f"({symbol}{money(g['net'])} net on {symbol}{money(g['rev'])} revenue).")
        elif g["rev"] and 0 <= margin < 0.05 and g["orders"] >= 3:
            alarms.append(f"{label} {name!r} nets only {100 * margin:.1f}% -- after your time it "
                          "is likely underwater. Reprice, cut costs, or drop it.")
    return alarms


def main() -> int:
    p = argparse.ArgumentParser(
        description="Analyse a multi-channel order log CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("csv_path", help="Path to the order log CSV")
    p.add_argument("--channel", help="Filter to channels containing this text")
    p.add_argument("--product-line", help="Filter to product lines containing this text")
    p.add_argument("--since", help="Only orders on or after this date (YYYY-MM-DD)")
    p.add_argument("--top-skus", type=int, default=8, help="How many SKUs to list (default 8)")
    p.add_argument("--column-map", help="Map canonical columns to yours, e.g. channel=Marketplace")
    p.add_argument("--symbol", default="$", help="Currency symbol")
    a = p.parse_args()

    column_map = {}
    if a.column_map:
        for pair in a.column_map.split(","):
            if "=" not in pair:
                raise SystemExit(f"--column-map expects canonical=source pairs, got {pair!r}")
            c, _, s = pair.partition("=")
            column_map[c.strip()] = s.strip()

    try:
        rows = load(a.csv_path, column_map)
    except FileNotFoundError:
        print(f"No such file: {a.csv_path}", file=sys.stderr)
        return 1

    if a.channel:
        rows = [r for r in rows if a.channel.lower() in r["channel"].lower()]
    if a.product_line:
        rows = [r for r in rows if a.product_line.lower() in r["product_line"].lower()]
    if a.since:
        cutoff = to_date(a.since)
        rows = [r for r in rows if (d := to_date(r["date"])) and d >= cutoff]
    if not rows:
        print("No rows matched the filters.", file=sys.stderr)
        return 1

    sym = a.symbol
    revenue = sum(to_float(r["sale_price"]) + to_float(r["shipping_charged"]) for r in rows)
    fees = sum(to_float(r["channel_fees"]) for r in rows)
    ship = sum(to_float(r["shipping_cost"]) for r in rows)
    goods = sum(to_float(r["cost_of_goods"]) for r in rows)
    refund_amt = sum(to_float(r["refund_amount"]) for r in rows)
    net = sum(net_of(r) for r in rows)
    refunds = sum(1 for r in rows if is_refunded(r))
    dates = [d for r in rows if (d := to_date(r["date"]))]

    print()
    print("=" * 62)
    print("  SALES SUMMARY")
    print("=" * 62)
    print(f"  Orders       : {len(rows)}   ({refunds} refunded/cancelled)")
    if dates:
        print(f"  Period       : {min(dates)} to {max(dates)}")
    print(f"  Revenue      : {sym}{money(revenue)}")
    print(f"  Net profit   : {sym}{money(net)}   ({pct(net, revenue).strip()} margin)")
    print(f"  Fee drag     : {pct(fees + ship, revenue).strip()}  "
          f"(fees {sym}{money(fees)} + shipping {sym}{money(ship)})")
    print(f"  Cost of goods: {sym}{money(goods)}")
    if refund_amt:
        print(f"  Refunded     : {sym}{money(refund_amt)}   "
              f"({pct(refunds, len(rows)).strip()} of orders)")

    alarms: list[str] = []
    if revenue and net < 0:
        alarms.append("The business is net-negative over this period. Something is priced "
                      "below its true cost -- work the by-line and by-SKU tables to find it.")

    alarms += group_report(rows, "channel", "Channel", sym)
    alarms += group_report(rows, "product_line", "Product line", sym)

    # ---- SKU contribution -------------------------------------------------------
    skus = defaultdict(lambda: {"orders": 0, "rev": 0.0, "net": 0.0, "refunds": 0})
    for r in rows:
        s = skus[r["sku"].strip() or "(no sku)"]
        s["orders"] += 1
        s["rev"] += to_float(r["sale_price"]) + to_float(r["shipping_charged"])
        s["net"] += net_of(r)
        if is_refunded(r):
            s["refunds"] += 1
    if len(skus) > 1:
        section(f"SKU CONTRIBUTION (top and bottom by net)")
        ranked = sorted(skus.items(), key=lambda kv: kv[1]["net"], reverse=True)
        show = ranked[: a.top_skus]
        if len(ranked) > a.top_skus:
            show = ranked[: a.top_skus // 2] + ranked[-(a.top_skus - a.top_skus // 2):]
        print(f"  {'SKU':<20}{'Orders':>7}{'Revenue':>11}{'Net':>11}{'Margin':>8}")
        for name, s in show:
            margin = s["net"] / s["rev"] if s["rev"] else 0.0
            flag = "  <- LOSS" if s["net"] < 0 else ""
            print(f"  {name[:19]:<20}{s['orders']:>7}{sym + money(s['rev']):>11}"
                  f"{sym + money(s['net']):>11}{pct(s['net'], s['rev']):>8}{flag}")
        losers = [n for n, s in skus.items() if s["net"] < 0]
        if losers:
            alarms.append(f"{len(losers)} SKU(s) are net-negative: {', '.join(sorted(losers)[:5])}"
                          f"{' ...' if len(losers) > 5 else ''}. Reprice or delist them.")

    # ---- refund reasons ---------------------------------------------------------
    reasons = defaultdict(int)
    for r in rows:
        if is_refunded(r):
            reasons[r["return_reason"].strip().lower() or "(unrecorded)"] += 1
    if reasons:
        section("REFUND REASONS")
        for reason, count in sorted(reasons.items(), key=lambda kv: -kv[1]):
            print(f"  {reason[:28]:<30}{count:>4}  {pct(count, refunds):>7}   {bar(count / refunds)}")
        if reasons.get("(unrecorded)", 0) > refunds / 2:
            alarms.append("Over half of refunds have no recorded reason -- the reason column is "
                          "what turns refunds into a fixable pattern. Record it at the time.")

    section("FLAGS")
    if alarms:
        for alarm in dict.fromkeys(alarms):
            print(f"  ! {alarm}")
    else:
        print("  Nothing outside normal ranges.")
    print()
    print("  Net here counts recorded costs only. If cost_of_goods excludes YOUR labour on")
    print("  the maker lines, the real margin is lower than shown -- value your time in it.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
