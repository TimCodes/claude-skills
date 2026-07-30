#!/usr/bin/env python3
"""Long-horizon growth projection and fee-drag illustrator.

Compounds a balance with regular contributions across a horizon, shows a range of return
assumptions, and -- its most useful job -- quantifies FEE DRAG: what a difference in annual
expense ratio costs over the horizon. Fees look trivial per year and are enormous over a
lifetime because they compound against you exactly as returns compound for you.

    python projection.py --initial 20000 --monthly 500 --years 30 --return 0.07
    python projection.py --initial 20000 --monthly 500 --years 30 --return 0.07 \
        --expense-a 0.03 --expense-b 1.00

This models assumptions YOU supply. It is not a prediction and not advice -- real returns are
uncertain and vary year to year; a single number here is a scenario, not a forecast. Withdrawal
sustainability especially depends on the ORDER of returns, which a smooth projection ignores.
"""

from __future__ import annotations

import argparse
import sys


def project(initial: float, monthly: float, years: int, annual_return: float,
            annual_expense: float, annual_inflation: float = 0.0) -> dict:
    """Compound monthly. Returns nominal and real ending balance and totals."""
    months = years * 12
    net_annual = annual_return - annual_expense / 100.0
    monthly_rate = (1.0 + net_annual) ** (1.0 / 12.0) - 1.0
    balance = initial
    contributed = initial
    for _ in range(months):
        balance = balance * (1.0 + monthly_rate) + monthly
        contributed += monthly
    real = balance / ((1.0 + annual_inflation) ** years) if annual_inflation else balance
    return {
        "ending": balance,
        "real_ending": real,
        "contributed": contributed,
        "growth": balance - contributed,
    }


def money(v: float, sym: str) -> str:
    return f"{sym}{v:,.0f}"


def main() -> int:
    p = argparse.ArgumentParser(
        description="Project growth with contributions and illustrate fee drag.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("--initial", type=float, default=0.0, help="Starting balance")
    p.add_argument("--monthly", type=float, default=0.0, help="Monthly contribution")
    p.add_argument("--years", type=int, default=30, help="Horizon in years (default 30)")
    p.add_argument("--return", dest="ret", type=float, default=0.07,
                   help="Assumed gross annual return as a fraction (default 0.07)")
    p.add_argument("--expense", type=float, default=0.0,
                   help="Annual expense ratio as a percent (e.g. 0.20). Single-scenario mode.")
    p.add_argument("--expense-a", type=float, help="Expense ratio A (percent) for fee-drag compare")
    p.add_argument("--expense-b", type=float, help="Expense ratio B (percent) for fee-drag compare")
    p.add_argument("--inflation", type=float, default=0.0,
                   help="Annual inflation to also show a real (today's-dollars) figure, e.g. 0.03")
    p.add_argument("--symbol", default="$", help="Currency symbol")
    a = p.parse_args()
    sym = a.symbol

    print()
    print("=" * 64)
    print("  GROWTH PROJECTION")
    print("=" * 64)
    print(f"  Start {money(a.initial, sym)}  +  {money(a.monthly, sym)}/mo  for {a.years} yrs"
          f"  @  {100 * a.ret:.1f}% assumed gross return")
    if a.inflation:
        print(f"  Inflation {100 * a.inflation:.1f}% -> also shown in today's dollars (real)")

    # --- fee-drag comparison mode ---
    if a.expense_a is not None or a.expense_b is not None:
        ea = a.expense_a if a.expense_a is not None else 0.0
        eb = a.expense_b if a.expense_b is not None else 0.0
        ra = project(a.initial, a.monthly, a.years, a.ret, ea, a.inflation)
        rb = project(a.initial, a.monthly, a.years, a.ret, eb, a.inflation)
        low, high = (ra, rb) if ea <= eb else (rb, ra)
        low_er, high_er = (ea, eb) if ea <= eb else (eb, ea)
        drag = low["ending"] - high["ending"]
        drag_pct = drag / low["ending"] if low["ending"] else 0.0

        print()
        print("  FEE DRAG")
        print("  " + "-" * 60)
        print(f"  {'Expense ratio':<26}{'Ending balance':>18}")
        print(f"  {format(low_er, '.2f') + '% (lower cost)':<26}{money(low['ending'], sym):>18}")
        print(f"  {format(high_er, '.2f') + '% (higher cost)':<26}{money(high['ending'], sym):>18}")
        print("  " + "-" * 60)
        print(f"  The extra {high_er - low_er:.2f}% annual fee costs "
              f"{money(drag, sym)} over {a.years} years")
        print(f"  -- {100 * drag_pct:.1f}% of the lower-cost ending balance, GONE to fees.")
        if a.inflation:
            print(f"  In today's dollars, that's {money(low['real_ending'] - high['real_ending'], sym)}.")
        print()
        print("  That is the whole case for minimising cost: a fee that looks negligible each")
        print("  year compounds into a life-changing sum, with certainty, while returns don't.")

    else:
        # --- single scenario, plus a return range for humility ---
        base = project(a.initial, a.monthly, a.years, a.ret, a.expense, a.inflation)
        print()
        if a.expense:
            print(f"  (Net of a {a.expense:.2f}% expense ratio.)")
        print(f"  Total contributed .................. {money(base['contributed'], sym)}")
        print(f"  Growth ............................. {money(base['growth'], sym)}")
        print(f"  Ending balance ..................... {money(base['ending'], sym)}")
        if a.inflation:
            print(f"  Ending balance (today's dollars) ... {money(base['real_ending'], sym)}")

        print()
        print("  RANGE OF OUTCOMES  (return is uncertain -- one number would be false precision)")
        print("  " + "-" * 60)
        print(f"  {'Assumed return':<20}{'Ending balance':>20}")
        for delta in (-0.03, -0.015, 0.0, 0.015, 0.03):
            r = a.ret + delta
            if r <= -1:
                continue
            res = project(a.initial, a.monthly, a.years, r, a.expense, a.inflation)
            tag = "  <- base" if abs(delta) < 1e-9 else ""
            print(f"  {format(100 * r, '.1f') + '%':<20}{money(res['ending'], sym):>20}{tag}")
        print()
        print("  The spread across plausible returns is enormous, which is the point: the future")
        print("  is a distribution, not a line. Plan against the range, not the midpoint.")

    print()
    print("  Scenario, not a forecast or advice. Returns vary year to year and the ORDER")
    print("  matters when withdrawing (sequence-of-returns risk). See references/portfolio-")
    print("  construction.md, and consult a fiduciary for planning tied to your situation.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
