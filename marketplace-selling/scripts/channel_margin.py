#!/usr/bin/env python3
"""Channel margin and pricing calculator for Etsy, Amazon, and Facebook.

Answers the two questions that decide whether a product works:

  Margin mode   Given a price, what do I actually net on each channel?

      python channel_margin.py --cost 6.50 --price 24 --shipping 5.20 --channel all

  Target mode   Given a target margin, what should I list at on a channel?

      python channel_margin.py --cost 6.50 --shipping 5.20 --target-margin 0.35 --channel etsy

Fee rates are typical defaults and CHANGE -- override any of them on the command line with
the current rate from the channel's fee page. This does arithmetic, not fee lookup.
"""

from __future__ import annotations

import argparse
import sys

# Typical fee structure per channel. Rates change; these are starting points to override.
# fee_pct applies to (item price + shipping charged); fixed is a per-order flat fee.
CHANNELS = {
    "etsy": {
        "label": "Etsy",
        "fee_pct": 0.065,        # transaction fee on item + shipping
        "payment_pct": 0.030,    # payment processing
        "payment_fixed": 0.25,
        "listing_fixed": 0.20,   # per sale
        "note": "Add ~12-15% on any order that comes via Etsy Offsite Ads (unpredictable per order).",
    },
    "amazon": {
        "label": "Amazon",
        "fee_pct": 0.15,         # referral fee (category-dependent; 15% is the common case)
        "payment_pct": 0.0,      # bundled into the referral fee
        "payment_fixed": 0.0,
        "listing_fixed": 0.0,    # Pro plan is a monthly cost, amortised separately via --plan-per-order
        "note": "Referral fee varies 8-20% by category. Add FBA per-unit + storage if fulfilled by Amazon.",
    },
    "facebook": {
        "label": "Facebook Shops",
        "fee_pct": 0.05,         # shipped checkout selling fee
        "payment_pct": 0.0,
        "payment_fixed": 0.0,
        "listing_fixed": 0.0,
        "note": "Local Marketplace pickup is ~0% fee and no shipping -- often the best net for bulky/fragile goods.",
    },
}


def parse_weight(text: str) -> float:
    """Return grams. Accepts '400g', '1.2kg', '0.9lb', '14oz', or a bare number (grams)."""
    t = text.strip().lower()
    for suffix, factor in (("kg", 1000.0), ("lb", 453.592), ("oz", 28.3495), ("g", 1.0)):
        if t.endswith(suffix):
            return float(t[: -len(suffix)]) * factor
    return float(t)


def money(v: float) -> str:
    return f"{v:8.2f}"


def net_for(ch: dict, price: float, shipping_charged: float, cost: float,
            ship_cost: float, ship_materials: float, cogs_extra: float,
            return_rate: float, plan_per_order: float, fba: float) -> dict:
    """Compute the full margin stack for one channel at a given price."""
    gross = price + shipping_charged
    fees = gross * ch["fee_pct"] + gross * ch["payment_pct"] + ch["payment_fixed"] + ch["listing_fixed"]
    ship_total = ship_cost + ship_materials
    goods = cost + cogs_extra
    # Return reserve: expected loss per order from refunds. Treat a return as losing the
    # goods, the outbound shipping and the fees (the common non-recoverable case).
    return_reserve = return_rate * (goods + ship_total + fees)
    total_cost = fees + ship_total + goods + return_reserve + plan_per_order + fba
    net = gross - total_cost
    return {
        "gross": gross, "fees": fees, "ship": ship_total, "goods": goods,
        "return_reserve": return_reserve, "plan": plan_per_order, "fba": fba,
        "net": net, "margin": net / gross if gross else 0.0,
    }


def price_for_target(ch: dict, target: float, shipping_charged: float, cost: float,
                     ship_cost: float, ship_materials: float, cogs_extra: float,
                     return_rate: float, plan_per_order: float, fba: float) -> float:
    """Solve for the item price that yields the target margin (net/gross) on this channel.

    net = gross - fees - ship - goods - return_reserve - plan - fba
    fees          = gross*(fee_pct+payment_pct) + payment_fixed + listing_fixed
    return_reserve= r*(goods + ship + fees)
    We want net = target*gross. Everything is linear in gross, so solve directly.
    """
    fee_rate = ch["fee_pct"] + ch["payment_pct"]
    fee_fixed = ch["payment_fixed"] + ch["listing_fixed"]
    ship = ship_cost + ship_materials
    goods = cost + cogs_extra
    # fees = fee_rate*gross + fee_fixed
    # return_reserve = r*(goods + ship + fee_rate*gross + fee_fixed)
    # net = gross - (fee_rate*gross+fee_fixed) - ship - goods
    #        - r*(goods+ship+fee_rate*gross+fee_fixed) - plan - fba
    # net = target*gross  ->  solve for gross
    # Coeff of gross on RHS: 1 - fee_rate - r*fee_rate
    a = 1.0 - fee_rate - return_rate * fee_rate - target
    b = (fee_fixed + ship + goods
         + return_rate * (goods + ship + fee_fixed) + plan_per_order + fba)
    if a <= 0:
        return float("nan")  # target margin unreachable given fee structure
    gross = b / a
    return gross - shipping_charged  # item price = gross - shipping charged to buyer


def print_margin(name: str, ch: dict, r: dict, symbol: str) -> None:
    print(f"  {ch['label']}")
    print(f"    {'Gross (item + shipping charged)':.<36}{symbol}{money(r['gross'])}")
    print(f"    {'- Channel + payment fees':.<36}{symbol}{money(-r['fees'])}")
    print(f"    {'- Shipping (label + materials)':.<36}{symbol}{money(-r['ship'])}")
    print(f"    {'- Cost of goods':.<36}{symbol}{money(-r['goods'])}")
    if r["return_reserve"]:
        print(f"    {'- Return reserve':.<36}{symbol}{money(-r['return_reserve'])}")
    if r["plan"]:
        print(f"    {'- Plan (amortised)':.<36}{symbol}{money(-r['plan'])}")
    if r["fba"]:
        print(f"    {'- FBA fulfilment':.<36}{symbol}{money(-r['fba'])}")
    print(f"    {'= NET PROFIT':.<36}{symbol}{money(r['net'])}   ({100 * r['margin']:.1f}% margin)")
    drag = (r["fees"] + r["ship"]) / r["gross"] if r["gross"] else 0.0
    print(f"    {'  fees + shipping as % of gross':.<36}{100 * drag:6.1f}%")
    if r["net"] < 0:
        print("    ** LOSS at this price on this channel. **")
    print()


def main() -> int:
    p = argparse.ArgumentParser(
        description="Channel margin and pricing for Etsy, Amazon, Facebook.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("--cost", type=float, required=True,
                   help="Cost of goods per unit: landed cost for resale, or make-cost incl. labour")
    p.add_argument("--price", type=float, help="Item price to evaluate (margin mode)")
    p.add_argument("--target-margin", type=float,
                   help="Target net margin as a fraction, e.g. 0.35 (target mode)")
    p.add_argument("--channel", default="all",
                   help="etsy | amazon | facebook | all (default all)")

    p.add_argument("--shipping", type=float, default=0.0,
                   help="Shipping label cost you pay per order")
    p.add_argument("--ship-weight", help="Alternative to --shipping: weight (e.g. 400g, 1.2kg) "
                                          "estimated at --rate-per-kg")
    p.add_argument("--rate-per-kg", type=float, default=12.0,
                   help="Estimated shipping cost per kg when using --ship-weight (default 12)")
    p.add_argument("--ship-materials", type=float, default=1.50,
                   help="Box, padding, tape, heat/cold packs per order (default 1.50)")
    p.add_argument("--shipping-charged", type=float, default=0.0,
                   help="Shipping charged to the buyer (0 = free shipping baked into price)")
    p.add_argument("--cogs-extra", type=float, default=0.0,
                   help="Extra per-order cost of goods (inserts, care card, etc.)")
    p.add_argument("--return-rate", type=float, default=0.0,
                   help="Expected refund rate as a fraction, e.g. 0.10. Live goods run high")
    p.add_argument("--plan-per-order", type=float, default=0.0,
                   help="Amazon Pro plan ($39.99/mo) amortised per order, e.g. 0.40 at 100 orders")
    p.add_argument("--fba", type=float, default=0.0, help="Amazon FBA per-unit fulfilment fee")
    p.add_argument("--fee", action="append", default=[], metavar="CHANNEL=PCT",
                   help="Override a channel's fee percentage with the current rate, repeatable. "
                        "e.g. --fee amazon=0.08 --fee etsy=0.07")
    p.add_argument("--symbol", default="$", help="Currency symbol for display")
    a = p.parse_args()

    for override in a.fee:
        if "=" not in override:
            print(f"--fee expects CHANNEL=PCT, got {override!r}", file=sys.stderr)
            return 1
        name, _, pct = override.partition("=")
        name = name.strip().lower()
        if name not in CHANNELS:
            print(f"--fee: unknown channel {name!r}", file=sys.stderr)
            return 1
        try:
            CHANNELS[name]["fee_pct"] = float(pct)
        except ValueError:
            print(f"--fee: could not read a rate from {pct!r} (use a fraction like 0.08)",
                  file=sys.stderr)
            return 1

    if not (a.price or a.target_margin):
        print("Give either --price (margin mode) or --target-margin (pricing mode).", file=sys.stderr)
        return 1
    if a.price and a.target_margin:
        print("Give --price OR --target-margin, not both.", file=sys.stderr)
        return 1

    ship_cost = a.shipping
    if a.ship_weight:
        ship_cost = (parse_weight(a.ship_weight) / 1000.0) * a.rate_per_kg

    if a.channel.lower() == "all":
        channels = list(CHANNELS)
    elif a.channel.lower() in CHANNELS:
        channels = [a.channel.lower()]
    else:
        print(f"Unknown channel {a.channel!r}. Use etsy, amazon, facebook, or all.", file=sys.stderr)
        return 1

    sym = a.symbol
    print()
    print("=" * 60)
    mode = "MARGIN" if a.price else "TARGET PRICING"
    print(f"  CHANNEL {mode}")
    print("=" * 60)
    print(f"  Cost of goods {sym}{a.cost:.2f}  |  shipping {sym}{ship_cost:.2f}"
          f" + {sym}{a.ship_materials:.2f} materials"
          f"{'  |  return rate ' + format(100 * a.return_rate, '.0f') + '%' if a.return_rate else ''}")
    print()

    if a.price:
        results = {}
        for name in channels:
            ch = CHANNELS[name]
            fba = a.fba if name == "amazon" else 0.0
            plan = a.plan_per_order if name == "amazon" else 0.0
            r = net_for(ch, a.price, a.shipping_charged, a.cost, ship_cost, a.ship_materials,
                        a.cogs_extra, a.return_rate, plan, fba)
            results[name] = r
            print_margin(name, ch, r, sym)
        if len(results) > 1:
            best = max(results, key=lambda n: results[n]["net"])
            print(f"  Best net: {CHANNELS[best]['label']} at {sym}{results[best]['net']:.2f} "
                  f"({100 * results[best]['margin']:.1f}%).")
            print()
    else:
        print(f"  To net a {100 * a.target_margin:.0f}% margin, list the item at:")
        print()
        for name in channels:
            ch = CHANNELS[name]
            fba = a.fba if name == "amazon" else 0.0
            plan = a.plan_per_order if name == "amazon" else 0.0
            price = price_for_target(ch, a.target_margin, a.shipping_charged, a.cost, ship_cost,
                                     a.ship_materials, a.cogs_extra, a.return_rate, plan, fba)
            if price != price or price <= 0:  # NaN or nonpositive
                print(f"    {ch['label']:<16} unreachable at this margin given the fee structure")
            else:
                gross = price + a.shipping_charged
                print(f"    {ch['label']:<16} {sym}{price:8.2f}   "
                      f"(gross {sym}{gross:.2f}; buyer pays {sym}{gross:.2f})")
        print()

    print("  NOTES")
    for name in channels:
        print(f"    - {CHANNELS[name]['label']}: {CHANNELS[name]['note']}")
    print("    - Fee rates are typical defaults and change. Confirm the current rate on the")
    print("      channel's fee page and pass it in (--fee channel=pct) before a real decision.")
    if not a.return_rate:
        print("    - No return reserve applied. For live plants and terrariums, set")
        print("      --return-rate (0.08-0.20 is realistic) -- it is often the largest hidden cost.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
