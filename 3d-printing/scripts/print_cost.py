#!/usr/bin/env python3
"""Cost and quote calculator for 3D printed parts.

Builds the full cost stack rather than the "grams times filament price" estimate
that makes print businesses look profitable when they are not. The two lines
people leave out -- post-processing labour and the failure-rate uplift -- are
often larger than the material cost.

    python print_cost.py --grams 180 --hours 9.5 --material PETG --spool-price 24
    python print_cost.py --grams 45 --hours 3.2 --post-hours 0.5 --failure-rate 0.1 \
        --margin 0.5 --quantity 20 --setup-hours 1.5

Currency is whatever you pass in; the script does not care which.
"""

from __future__ import annotations

import argparse
import sys

# Typical average draw while printing, in watts. The heated bed dominates on FDM.
TYPICAL_WATTS = {
    "PLA": 100.0, "PETG": 120.0, "ABS": 150.0, "ASA": 150.0,
    "TPU": 110.0, "PA": 150.0, "NYLON": 150.0, "PC": 170.0,
    "PA-CF": 150.0, "PET-CF": 130.0, "RESIN": 70.0,
}


def money(value: float, symbol: str) -> str:
    return f"{symbol}{value:,.2f}"


def line(label: str, value: float, symbol: str, pct_of: float = 0.0) -> None:
    share = f"{100 * value / pct_of:5.1f}%" if pct_of else "     "
    # Truncate rather than let a long label overrun and break column alignment.
    print(f"    {label[:33] + ' ':.<34} {money(value, symbol):>12}   {share}")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Cost and quote a 3D print job.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--grams", type=float, required=True,
                   help="Material used per part, including supports and purge")
    p.add_argument("--hours", type=float, required=True, help="Print hours per part")
    p.add_argument("--material", default="PLA", help="Material name (sets typical wattage)")
    p.add_argument("--spool-price", type=float, default=20.0, help="Price per spool")
    p.add_argument("--spool-grams", type=float, default=1000.0, help="Grams per spool")
    p.add_argument("--quantity", type=int, default=1, help="Number of parts")

    p.add_argument("--printer-cost", type=float, default=400.0, help="Purchase price")
    p.add_argument("--printer-life-hours", type=float, default=4000.0,
                   help="Expected usable print hours over the machine's life")
    p.add_argument("--maintenance-per-hour", type=float, default=0.03,
                   help="Consumables and maintenance provision per print hour")

    p.add_argument("--watts", type=float, help="Average draw while printing (overrides default)")
    p.add_argument("--power-price", type=float, default=0.30, help="Price per kWh")

    p.add_argument("--post-hours", type=float, default=0.0,
                   help="Post-processing labour per part (support removal, sanding, packing)")
    p.add_argument("--setup-hours", type=float, default=0.0,
                   help="One-off setup/design/slicing time for the whole job")
    p.add_argument("--labour-rate", type=float, default=25.0, help="Your hourly rate")

    p.add_argument("--failure-rate", type=float, default=0.05,
                   help="Fraction of prints that fail (default 0.05)")
    p.add_argument("--consumables", type=float, default=0.0,
                   help="Extra consumables per part (adhesive, IPA, packaging)")
    p.add_argument("--shipping", type=float, default=0.0, help="Shipping cost per order")
    p.add_argument("--platform-fee", type=float, default=0.0,
                   help="Marketplace fee as a fraction of sale price, e.g. 0.10 for Etsy")
    p.add_argument("--margin", type=float, default=0.0,
                   help="Target margin on cost, e.g. 0.5 for a 1.5x markup")
    p.add_argument("--symbol", default="$", help="Currency symbol for display")

    a = p.parse_args()

    if not 0.0 <= a.failure_rate < 1.0:
        print("--failure-rate must be between 0 and 1 (exclusive of 1)", file=sys.stderr)
        return 1

    # ---- per-part direct costs --------------------------------------------------
    material = a.grams * (a.spool_price / a.spool_grams)
    machine_rate = (a.printer_cost / a.printer_life_hours) + a.maintenance_per_hour
    machine = a.hours * machine_rate
    watts = a.watts if a.watts is not None else TYPICAL_WATTS.get(a.material.upper(), 120.0)
    power = a.hours * (watts / 1000.0) * a.power_price
    post_labour = a.post_hours * a.labour_rate

    nominal = material + machine + power + post_labour + a.consumables
    # Good parts must carry the cost of the failed ones.
    with_failure = nominal / (1.0 - a.failure_rate)
    failure_uplift = with_failure - nominal

    setup_cost = a.setup_hours * a.labour_rate
    setup_per_part = setup_cost / a.quantity if a.quantity else setup_cost

    cost_per_part = with_failure + setup_per_part
    total_cost = cost_per_part * a.quantity + a.shipping

    symbol = a.symbol
    print()
    print("=" * 68)
    print(f"  PRINT COST  --  {a.quantity} x {a.material.upper()} part"
          f"{'s' if a.quantity != 1 else ''}")
    print("=" * 68)
    print(f"  {a.grams:g} g and {a.hours:g} h per part"
          f"  |  machine rate {money(machine_rate, symbol)}/h"
          f"  |  {watts:g} W")
    print()
    print("  PER PART")
    line("Material", material, symbol, with_failure)
    line("Machine time (deprec. + maint.)", machine, symbol, with_failure)
    line("Power", power, symbol, with_failure)
    if post_labour:
        line(f"Post-processing ({a.post_hours:g} h)", post_labour, symbol, with_failure)
    if a.consumables:
        line("Consumables", a.consumables, symbol, with_failure)
    print(f"    {'-' * 34} {'-' * 12}")
    line("Subtotal", nominal, symbol)
    if failure_uplift:
        line(f"Failure uplift ({100 * a.failure_rate:g}%)", failure_uplift, symbol, with_failure)
    if setup_per_part:
        line(f"Setup, amortised over {a.quantity}", setup_per_part, symbol, with_failure)
    print(f"    {'=' * 34} {'=' * 12}")
    line("COST PER PART", cost_per_part, symbol)

    print()
    print("  JOB TOTAL")
    line(f"Cost x {a.quantity}", cost_per_part * a.quantity, symbol)
    if a.shipping:
        line("Shipping", a.shipping, symbol)
    line("TOTAL COST", total_cost, symbol)

    # ---- pricing ----------------------------------------------------------------
    if a.margin or a.platform_fee:
        print()
        print("  PRICING")
        price = total_cost * (1.0 + a.margin)
        if a.platform_fee:
            if a.platform_fee >= 1.0:
                print("    --platform-fee must be a fraction below 1 (0.10 = 10%)", file=sys.stderr)
                return 1
            # Gross up so the fee comes out of the sale price, not the margin.
            price = price / (1.0 - a.platform_fee)
            fee = price * a.platform_fee
            line(f"Platform fee ({100 * a.platform_fee:g}%)", fee, symbol)
        line("SALE PRICE", price, symbol)
        if a.quantity > 1:
            line("  per part", price / a.quantity, symbol)
        profit = price - total_cost - (price * a.platform_fee)
        line("Profit", profit, symbol)
        if price:
            print(f"    {'Effective margin on price':.<34} {100 * profit / price:11.1f}%")
        hours_total = (a.hours * a.quantity) + (a.post_hours * a.quantity) + a.setup_hours
        active = (a.post_hours * a.quantity) + a.setup_hours
        if active > 0:
            print(f"    {'Profit per hour of YOUR time':.<34} "
                  f"{money(profit / active, symbol):>12}")
            print(f"    (your time = {active:g} h of setup and post-processing;")
            print(f"     the {a.hours * a.quantity:g} h of printing is machine time, not yours)")
        elif hours_total:
            print("    No labour hours entered -- add --post-hours and --setup-hours")
            print("    for a realistic picture. Unpaid labour is the usual reason a")
            print("    print business looks profitable and does not feel like it.")

    print()
    print("  NOTES")
    if not a.post_hours:
        print("    - No post-processing time entered. Support removal, sanding and packing")
        print("      are usually the largest cost for anything not shipped raw off the plate.")
    if a.failure_rate == 0:
        print("    - A 0% failure rate is not realistic. Even a well-run setup loses prints.")
    if a.margin and a.margin < 0.3:
        print(f"    - A {100 * a.margin:g}% margin leaves little room for returns, reprints")
        print("      and the time spent on listings and customer service.")
    print("    - Machine rate assumes the printer is replaced after")
    print(f"      {a.printer_life_hours:g} h. If you never reserve for replacement,")
    print("      you are consuming capital and calling it profit.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
