#!/usr/bin/env python3
"""Culture log analysis for a plant tissue culture lab.

Reads a culture log CSV and reports the numbers that decide whether a lab is
healthy: contamination rate by stage and cause, realised multiplication rate by
genotype, off-type rate, subculture-number exposure, and a forward inventory
projection.

    python culture_metrics.py logs/cultures.csv
    python culture_metrics.py logs/cultures.csv --genotype "Monstera Albo" --project-cycles 6
    python culture_metrics.py logs/cultures.csv --column-map batch=BatchRef,date=Date

Expected columns are documented in assets/culture-log-template.csv. Missing
optional columns are tolerated -- the affected metrics are reported as
unavailable rather than silently computed from partial data, because a
contamination rate built from half the records is worse than no number at all.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime, date

CANONICAL = [
    "batch_id", "date", "genotype", "stage", "subculture_no",
    "vessels_in", "explants_in", "vessels_clean", "explants_out",
    "contaminated_bacterial", "contaminated_fungal", "contaminated_other",
    "off_type", "medium_id", "operator", "notes",
]

# Stage II contamination above this is a systems problem, not bad luck.
STAGE_II_CONTAM_ALARM = 0.05
SUBCULTURE_CEILING = 12
SUBCULTURE_WARN = 8

STAGE_ORDER = {"0": 0, "I": 1, "1": 1, "II": 2, "2": 2, "III": 3, "3": 3, "IV": 4, "4": 4}


def stage_key(stage: str) -> tuple[int, str]:
    return (STAGE_ORDER.get(stage.strip().upper(), 99), stage)


def is_stage_ii(stage: str) -> bool:
    return stage.strip().upper() in ("II", "2")


def to_float(value, default=0.0) -> float:
    try:
        text = str(value).strip()
        return float(text) if text else default
    except (TypeError, ValueError):
        return default


def to_date(value):
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
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
        rows = []
        for raw in reader:
            row = {c: (raw.get(lookup[c], "") if c in lookup else "") for c in CANONICAL}
            rows.append(row)
    return rows


def pct(numerator: float, denominator: float) -> str:
    return f"{100 * numerator / denominator:5.1f}%" if denominator else "    --"


def bar(fraction: float, width: int = 24) -> str:
    filled = int(round(max(0.0, min(1.0, fraction)) * width))
    return "#" * filled + "." * (width - filled)


def section(title: str) -> None:
    print()
    print(title)
    print("-" * max(len(title), 60))


def report(rows: list[dict], args) -> int:
    if args.genotype:
        needle = args.genotype.lower()
        rows = [r for r in rows if needle in r["genotype"].lower()]
    if args.since:
        cutoff = to_date(args.since)
        rows = [r for r in rows if (d := to_date(r["date"])) and d >= cutoff]
    if not rows:
        print("No rows matched the filters.", file=sys.stderr)
        return 1

    dates = [d for r in rows if (d := to_date(r["date"]))]
    print()
    print("=" * 66)
    print("  CULTURE LOG SUMMARY")
    print("=" * 66)
    print(f"  Records   : {len(rows)}")
    if dates:
        print(f"  Period    : {min(dates)} to {max(dates)}")
    genotypes = sorted({r["genotype"] for r in rows if r["genotype"]})
    print(f"  Genotypes : {len(genotypes)}")
    if args.genotype:
        print(f"  Filtered  : {args.genotype!r}")

    # ---- contamination by stage -------------------------------------------------
    section("CONTAMINATION BY STAGE")
    by_stage = defaultdict(lambda: {"in": 0.0, "bact": 0.0, "fung": 0.0, "other": 0.0})
    for r in rows:
        s = by_stage[r["stage"].strip() or "?"]
        s["in"] += to_float(r["vessels_in"])
        s["bact"] += to_float(r["contaminated_bacterial"])
        s["fung"] += to_float(r["contaminated_fungal"])
        s["other"] += to_float(r["contaminated_other"])

    print(f"  {'Stage':<8}{'Vessels':>9}{'Bact':>7}{'Fungal':>8}{'Other':>7}{'Rate':>8}   ")
    alarms: list[str] = []
    for stage in sorted(by_stage, key=stage_key):
        s = by_stage[stage]
        lost = s["bact"] + s["fung"] + s["other"]
        rate = lost / s["in"] if s["in"] else 0.0
        print(f"  {stage:<8}{s['in']:>9.0f}{s['bact']:>7.0f}{s['fung']:>8.0f}"
              f"{s['other']:>7.0f}{pct(lost, s['in']):>8}   {bar(rate, 16)}")
        if stage.upper() in ("II", "2") and rate > STAGE_II_CONTAM_ALARM and s["in"]:
            alarms.append(
                f"Stage II contamination is {100 * rate:.1f}% (target <2-3%). This is a systems "
                "problem. Audit in order: autoclave indicator strips, HEPA filter and hood "
                "airflow, media pH and sterilisation, vessel closures, then technique."
            )
    total_in = sum(s["in"] for s in by_stage.values())
    total_lost = sum(s["bact"] + s["fung"] + s["other"] for s in by_stage.values())
    print(f"  {'ALL':<8}{total_in:>9.0f}"
          f"{sum(s['bact'] for s in by_stage.values()):>7.0f}"
          f"{sum(s['fung'] for s in by_stage.values()):>8.0f}"
          f"{sum(s['other'] for s in by_stage.values()):>7.0f}"
          f"{pct(total_lost, total_in):>8}")
    if total_lost:
        b = sum(s["bact"] for s in by_stage.values())
        f = sum(s["fung"] for s in by_stage.values())
        dominant = "bacterial" if b > f else "fungal"
        hint = ("Bacterial losses point at the source plant and endophytes (Stage I) or "
                "technique and autoclave (Stage II)."
                if dominant == "bacterial" else
                "Fungal losses are usually airborne -- check hood airflow, filter age, "
                "and vessel closure integrity.")
        print(f"\n  Predominantly {dominant}. {hint}")

    # ---- per genotype -----------------------------------------------------------
    section("BY GENOTYPE")
    # Multiplication rate is only meaningful for Stage II rows -- Stage I establishment
    # and Stage III/IV rows always run at or below 1x, so pooling every stage drags the
    # figure down and makes a healthy line look like a failing one.
    by_geno = defaultdict(lambda: {"in": 0.0, "out": 0.0, "v_in": 0.0, "lost": 0.0,
                                   "off": 0.0, "sub": [], "latest": (None, 0.0)})
    for r in rows:
        g = by_geno[r["genotype"] or "(unspecified)"]
        g["v_in"] += to_float(r["vessels_in"])
        g["lost"] += (to_float(r["contaminated_bacterial"])
                      + to_float(r["contaminated_fungal"])
                      + to_float(r["contaminated_other"]))
        if is_stage_ii(r["stage"]):
            g["in"] += to_float(r["explants_in"])
            g["out"] += to_float(r["explants_out"])
            g["off"] += to_float(r["off_type"])
        if (sub := r["subculture_no"].strip()):
            g["sub"].append(to_float(sub))
        row_date = to_date(r["date"])
        if row_date and (g["latest"][0] is None or row_date >= g["latest"][0]):
            g["latest"] = (row_date, to_float(r["explants_out"]))

    print("  Multiplication and off-type are computed from Stage II rows only.")
    print()
    print(f"  {'Genotype':<32}{'Mult':>7}{'Contam':>9}{'Off-type':>10}{'Subcult':>9}")
    for name in sorted(by_geno):
        g = by_geno[name]
        mult = g["out"] / g["in"] if g["in"] else 0.0
        mult_text = f"{mult:.2f}x" if g["in"] else "   --"
        sub_text = f"{max(g['sub']):.0f}" if g["sub"] else "--"
        print(f"  {name[:31]:<32}{mult_text:>7}{pct(g['lost'], g['v_in']):>9}"
              f"{pct(g['off'], g['out']):>10}{sub_text:>9}")

        if g["sub"] and max(g["sub"]) >= SUBCULTURE_CEILING:
            alarms.append(
                f"{name}: at subculture {max(g['sub']):.0f}, past the usual 8-12 ceiling. "
                "Somaclonal variation accumulates with cycles -- restart from mother stock. "
                "Re-initiation takes months, so start now."
            )
        elif g["sub"] and max(g["sub"]) >= SUBCULTURE_WARN:
            alarms.append(
                f"{name}: at subculture {max(g['sub']):.0f}, approaching the 8-12 ceiling. "
                "Plan a restart from mother stock before it is urgent."
            )
        if g["in"] and 0 < (g["out"] / g["in"]) < 1.5:
            alarms.append(
                f"{name}: multiplication rate {g['out'] / g['in']:.2f}x is low. Consider raising "
                "cytokinin one step, or check whether the subculture interval is too short."
            )
        if g["out"] and (g["off"] / g["out"]) > 0.30:
            alarms.append(
                f"{name}: off-type rate {100 * g['off'] / g['out']:.0f}%. Normal for a chimeral "
                "variegate; for a stable cultivar it signals somaclonal drift -- check the "
                "subculture count and the cytokinin level."
            )

    # ---- projection -------------------------------------------------------------
    if args.project_cycles:
        section(f"INVENTORY PROJECTION -- {args.project_cycles} cycles ahead")
        print(f"  Assuming a {args.cycle_days}-day cycle and each genotype's realised Stage II")
        print("  rate, net of its observed contamination and off-type losses. 'Now' is the")
        print("  shoot count from that genotype's most recent logged transfer.")
        print()
        print(f"  {'Genotype':<32}{'Now':>8}{'Rate':>8}{'Projected':>12}{'Days':>7}")
        for name in sorted(by_geno):
            g = by_geno[name]
            if not g["in"] or not g["out"]:
                continue
            gross = g["out"] / g["in"]
            survival = 1.0 - (g["lost"] / g["v_in"] if g["v_in"] else 0.0)
            trueness = 1.0 - (g["off"] / g["out"] if g["out"] else 0.0)
            net = gross * max(survival, 0.0) * max(trueness, 0.0)
            current = g["latest"][1]
            projected = current * (net ** args.project_cycles)
            print(f"  {name[:31]:<32}{current:>8.0f}{net:>7.2f}x{projected:>12,.0f}"
                  f"{args.project_cycles * args.cycle_days:>7}")
        print()
        print("  Net rate = multiplication x (1 - contamination) x (1 - off-type).")
        print("  Compounding makes small rate differences enormous over several cycles, and")
        print("  makes optimistic loss assumptions expensive. Treat this as an upper bound.")

    # ---- operator ---------------------------------------------------------------
    ops = defaultdict(lambda: {"in": 0.0, "lost": 0.0})
    for r in rows:
        if r["operator"].strip():
            o = ops[r["operator"].strip()]
            o["in"] += to_float(r["vessels_in"])
            o["lost"] += (to_float(r["contaminated_bacterial"])
                          + to_float(r["contaminated_fungal"])
                          + to_float(r["contaminated_other"]))
    if len(ops) > 1:
        section("BY OPERATOR")
        print("  Clustering by operator usually means a fixable technique detail, not a")
        print("  bad technician. Watch for reaching over open vessels and instrument cooling.")
        print()
        for name in sorted(ops, key=lambda n: -(ops[n]["lost"] / ops[n]["in"] if ops[n]["in"] else 0)):
            o = ops[name]
            r = o["lost"] / o["in"] if o["in"] else 0.0
            print(f"  {name[:25]:<26}{o['in']:>8.0f} vessels{pct(o['lost'], o['in']):>9}"
                  f"   {bar(r, 16)}")

    # ---- alarms -----------------------------------------------------------------
    if alarms:
        section("FLAGS")
        for a in dict.fromkeys(alarms):
            print(f"  ! {a}")
    else:
        section("FLAGS")
        print("  Nothing outside normal ranges.")
    print()
    return 0


def parse_column_map(text: str | None) -> dict[str, str]:
    if not text:
        return {}
    mapping = {}
    for pair in text.split(","):
        if "=" not in pair:
            raise SystemExit(f"--column-map expects canonical=source pairs, got {pair!r}")
        canonical, _, source = pair.partition("=")
        mapping[canonical.strip()] = source.strip()
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyse a plant tissue culture log CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("csv_path", help="Path to the culture log CSV")
    parser.add_argument("--genotype", help="Filter to genotypes containing this text")
    parser.add_argument("--since", help="Only records on or after this date (YYYY-MM-DD)")
    parser.add_argument("--project-cycles", type=int, default=0,
                        help="Project inventory this many subculture cycles ahead")
    parser.add_argument("--cycle-days", type=int, default=35,
                        help="Days per subculture cycle for the projection (default 35)")
    parser.add_argument("--column-map",
                        help="Map canonical columns to yours, e.g. batch_id=BatchRef,date=Date")
    args = parser.parse_args()

    try:
        rows = load(args.csv_path, parse_column_map(args.column_map))
    except FileNotFoundError:
        print(f"No such file: {args.csv_path}", file=sys.stderr)
        return 1
    return report(rows, args)


if __name__ == "__main__":
    sys.exit(main())
