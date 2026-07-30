#!/usr/bin/env python3
"""Portfolio analyzer for the independent investor.

Reads a holdings CSV and reports allocation, cost, and concentration; optionally reads a
return series and reports risk metrics (volatility, Sharpe, Sortino, max drawdown).

    python portfolio_analyzer.py holdings.csv
    python portfolio_analyzer.py holdings.csv --returns returns.csv --risk-free 0.04

This is an analytical aid, not advice. It describes a portfolio you supply; it does not tell
you what to buy, sell, or hold, and its risk metrics are backward-looking and blind to the
tail events that matter most. See references/portfolio-construction.md for how to read them.

Holdings CSV columns (see assets/holdings-template.csv):
    ticker, name, asset_class, value, expense_ratio   (expense_ratio as a percent, e.g. 0.03)
Returns CSV columns:
    date, return       (return as a period fraction, e.g. 0.012 for +1.2%), or
    date, value        (a value/price series; the script computes returns from it)
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict


def to_float(value, default=0.0) -> float:
    try:
        t = str(value).strip().replace(",", "").replace("$", "").replace("%", "")
        return float(t) if t else default
    except (TypeError, ValueError):
        return default


def load_holdings(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise SystemExit(f"{path}: no header row")
        fields = {f.strip().lower(): f for f in reader.fieldnames}

        def col(row, name):
            return row.get(fields.get(name, ""), "")

        rows = []
        for raw in reader:
            rows.append({
                "ticker": col(raw, "ticker").strip() or "?",
                "name": col(raw, "name").strip(),
                "asset_class": col(raw, "asset_class").strip() or "(unclassified)",
                "value": to_float(col(raw, "value")),
                "expense_ratio": to_float(col(raw, "expense_ratio")),  # percent
            })
    return [r for r in rows if r["value"] > 0]


def load_returns(path: str) -> list[float]:
    """Return a list of period returns. Accepts a 'return' column or a 'value' series."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise SystemExit(f"{path}: no header row")
        fields = {f.strip().lower(): f for f in reader.fieldnames}
        rows = list(reader)

    if "return" in fields:
        return [to_float(r[fields["return"]]) for r in rows if str(r[fields["return"]]).strip() != ""]
    if "value" in fields:
        vals = [to_float(r[fields["value"]]) for r in rows]
        vals = [v for v in vals if v > 0]
        return [(vals[i] / vals[i - 1]) - 1.0 for i in range(1, len(vals))]
    raise SystemExit(f"{path}: need a 'return' or 'value' column")


def bar(fraction: float, width: int = 28) -> str:
    filled = int(round(max(0.0, min(1.0, fraction)) * width))
    return "#" * filled + "." * (width - filled)


def money(v: float) -> str:
    return f"{v:,.0f}"


def analyze_holdings(holdings: list[dict], sym: str) -> None:
    total = sum(h["value"] for h in holdings)
    print()
    print("=" * 64)
    print("  PORTFOLIO ANALYSIS")
    print("=" * 64)
    print(f"  Holdings     : {len(holdings)}")
    print(f"  Total value  : {sym}{money(total)}")

    # Allocation by asset class
    by_class = defaultdict(float)
    for h in holdings:
        by_class[h["asset_class"]] += h["value"]
    print()
    print("  ALLOCATION BY ASSET CLASS")
    print("  " + "-" * 60)
    for cls in sorted(by_class, key=lambda c: -by_class[c]):
        w = by_class[cls] / total if total else 0
        print(f"  {cls[:20]:<20}{sym}{money(by_class[cls]):>12} {100 * w:6.1f}%  {bar(w, 22)}")

    # Cost
    weighted_er = sum(h["value"] * h["expense_ratio"] for h in holdings) / total if total else 0
    annual_fee = total * weighted_er / 100.0
    print()
    print("  COST")
    print("  " + "-" * 60)
    print(f"  Asset-weighted expense ratio ....... {weighted_er:.3f}%")
    print(f"  Annual fund fee at current value ... {sym}{money(annual_fee)}")
    print(f"  Over 30 yrs (fee only, no growth) .. ~{sym}{money(annual_fee * 30)} in fees,"
          f" before the compounding drag")
    if weighted_er > 0.5:
        print(f"  ! Weighted cost {weighted_er:.2f}% is high. Every 1% of fee can consume ~a")
        print(f"    quarter of 30-year wealth -- see scripts/projection.py to quantify it.")

    # Concentration
    print()
    print("  CONCENTRATION")
    print("  " + "-" * 60)
    ranked = sorted(holdings, key=lambda h: -h["value"])
    for h in ranked[:5]:
        w = h["value"] / total if total else 0
        print(f"  {h['ticker']:<8}{h['name'][:22]:<24}{100 * w:6.1f}%  {bar(w, 20)}")
    top = ranked[0]["value"] / total if total else 0
    top5 = sum(h["value"] for h in ranked[:5]) / total if total else 0
    print(f"  Largest position: {100 * top:.1f}%   Top 5: {100 * top5:.1f}%")
    hhi = sum((h["value"] / total) ** 2 for h in holdings) if total else 0
    eff_n = 1 / hhi if hhi else 0
    print(f"  Effective number of holdings (1/HHI): {eff_n:.1f}"
          f"   (concentration index {hhi:.3f})")
    if top > 0.25:
        print(f"  ! Largest single holding is {100 * top:.0f}% of the portfolio -- concentrated.")
    if len(by_class) < 2:
        print("  ! Only one asset class present -- no cross-class diversification.")


def analyze_returns(returns: list[float], risk_free_annual: float, ppy: int, sym: str) -> None:
    if len(returns) < 2:
        print("\n  (Not enough return data for risk metrics.)")
        return
    n = len(returns)
    mean = sum(returns) / n
    var = sum((r - mean) ** 2 for r in returns) / (n - 1)
    sd = math.sqrt(var)
    downside = [min(0.0, r) for r in returns]
    dvar = sum(d ** 2 for d in downside) / (n - 1)
    dsd = math.sqrt(dvar)

    # Compounded (geometric) annualised return
    growth = 1.0
    for r in returns:
        growth *= (1.0 + r)
    ann_return = growth ** (ppy / n) - 1.0
    ann_vol = sd * math.sqrt(ppy)
    ann_dvol = dsd * math.sqrt(ppy)
    rf_period = risk_free_annual / ppy
    excess = mean - rf_period
    sharpe = (excess / sd) * math.sqrt(ppy) if sd else float("nan")
    sortino = (excess / dsd) * math.sqrt(ppy) if dsd else float("nan")

    # Max drawdown on the cumulative curve
    peak = 1.0
    curve = 1.0
    max_dd = 0.0
    for r in returns:
        curve *= (1.0 + r)
        peak = max(peak, curve)
        max_dd = min(max_dd, curve / peak - 1.0)

    print()
    print("  RISK & RETURN  (from supplied return series)")
    print("  " + "-" * 60)
    print(f"  Periods analysed ................... {n}  (annualised at {ppy}/yr)")
    print(f"  Annualised return (geometric) ...... {100 * ann_return:6.2f}%")
    print(f"  Annualised volatility .............. {100 * ann_vol:6.2f}%")
    print(f"  Downside deviation (annualised) .... {100 * ann_dvol:6.2f}%")
    print(f"  Max drawdown ....................... {100 * max_dd:6.2f}%")
    print(f"  Sharpe ratio (rf {100 * risk_free_annual:.1f}%) ......... {sharpe:6.2f}")
    print(f"  Sortino ratio ...................... {sortino:6.2f}")
    print()
    print("  Volatility and Sharpe treat risk as standard deviation -- they are blind to")
    print("  fat tails, illiquidity, and the fact that the next drawdown can exceed the")
    print("  worst in this sample. Read them as description, not prediction.")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Analyse a portfolio's allocation, cost, and risk.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("holdings", help="Holdings CSV (ticker, name, asset_class, value, expense_ratio)")
    p.add_argument("--returns", help="Optional return series CSV (date, return) or (date, value)")
    p.add_argument("--risk-free", type=float, default=0.04,
                   help="Annual risk-free rate for Sharpe/Sortino (default 0.04)")
    p.add_argument("--periods-per-year", type=int, default=12,
                   help="Return frequency for annualisation: 252 daily, 52 weekly, 12 monthly, "
                        "4 quarterly, 1 annual (default 12)")
    p.add_argument("--symbol", default="$", help="Currency symbol")
    a = p.parse_args()

    try:
        holdings = load_holdings(a.holdings)
    except FileNotFoundError:
        print(f"No such file: {a.holdings}", file=sys.stderr)
        return 1
    if not holdings:
        print("No holdings with positive value found.", file=sys.stderr)
        return 1

    analyze_holdings(holdings, a.symbol)

    if a.returns:
        try:
            returns = load_returns(a.returns)
        except FileNotFoundError:
            print(f"No such file: {a.returns}", file=sys.stderr)
            return 1
        analyze_returns(returns, a.risk_free, a.periods_per_year, a.symbol)

    print()
    print("  This is analysis of a portfolio you supplied, not investment advice. It does not")
    print("  recommend buying, selling, or holding anything. For a personalised decision tied")
    print("  to your full situation, consult a fee-only fiduciary. See the advice-boundary ref.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
