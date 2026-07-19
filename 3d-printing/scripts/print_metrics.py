#!/usr/bin/env python3
"""Print log analysis for a 3D printing shop or farm.

Reads a job log CSV and reports the numbers that show whether a setup is healthy:
success rate by printer, material and profile; which failure causes dominate;
machine utilisation; material actually consumed per good part; and labour split.

    python print_metrics.py logs/prints.csv
    python print_metrics.py logs/prints.csv --printer voron-01 --since 2026-05-01
    python print_metrics.py logs/prints.csv --column-map printer=Machine,date=Date

Expected columns are documented in assets/print-log-template.csv. Missing optional
columns are tolerated -- affected metrics report as unavailable rather than being
silently computed from partial data.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime

CANONICAL = [
    "job_id", "date", "printer", "material", "filament_g", "print_hours",
    "status", "failure_cause", "parts", "post_hours", "profile", "nozzle", "notes",
]

SUCCESS_TARGET = 0.90
SUCCESS_ALARM = 0.80

# Where each failure cause usually actually lives, so the report points somewhere useful.
CAUSE_HINTS = {
    "adhesion": "bed cleanliness (soap and water, not just IPA), Z-offset, bed temperature",
    "warping": "enclosure and ambient temperature, draughts, brim, bottom-corner fillets",
    "clog": "filament moisture, nozzle wear, hotend fan, temperature",
    "layer shift": "belt tension, pulley grub screws, acceleration, collision with a curled part",
    "spaghetti": "an upstream failure -- find whether it detached or clogged",
    "stringing": "filament moisture first, then nozzle temperature and retraction",
    "layer separation": "nozzle temperature too low, cooling too high, moisture",
    "under-extrusion": "partial clog, worn nozzle, moisture, flow rate, volumetric flow ceiling",
    "power": "power stability and resume settings",
    "user error": "worth logging honestly -- it is often a slicing or file-selection workflow gap",
}


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
        return [{c: (raw.get(lookup[c], "") if c in lookup else "") for c in CANONICAL}
                for raw in reader]


def is_success(row: dict) -> bool:
    return row["status"].strip().lower() in ("success", "ok", "good", "complete", "completed")


def pct(numerator: float, denominator: float) -> str:
    return f"{100 * numerator / denominator:5.1f}%" if denominator else "    --"


def bar(fraction: float, width: int = 20) -> str:
    filled = int(round(max(0.0, min(1.0, fraction)) * width))
    return "#" * filled + "." * (width - filled)


def section(title: str) -> None:
    print()
    print(title)
    print("-" * max(len(title), 62))


def dominant_printer(failed: list[dict]) -> tuple[str, float] | None:
    """If one printer accounts for most failures in a group, name it.

    Material and profile breakdowns are confounded by which machine ran the job.
    A material looks bad when in truth one bad printer happened to run most of it,
    and flagging the material sends people to change filament instead of fixing
    the machine. Detecting the concentration turns four misleading flags into one
    honest observation.
    """
    if not failed:
        return None
    counts = defaultdict(int)
    for r in failed:
        counts[r["printer"].strip() or "(unspecified)"] += 1
    name, count = max(counts.items(), key=lambda kv: kv[1])
    share = count / len(failed)
    if len(failed) >= 2 and share >= 0.7:
        return name, share
    return None


def breakdown(rows: list[dict], key: str, label: str, check_confound: bool = False) -> list[str]:
    """Success rate grouped by one column. Returns any alarm strings raised."""
    groups = defaultdict(lambda: {"n": 0, "ok": 0, "g": 0.0, "h": 0.0, "failed": []})
    for r in rows:
        name = r[key].strip() or "(unspecified)"
        g = groups[name]
        g["n"] += 1
        if is_success(r):
            g["ok"] += 1
        else:
            g["failed"].append(r)
        g["g"] += to_float(r["filament_g"])
        g["h"] += to_float(r["print_hours"])
    if not groups or (len(groups) == 1 and "(unspecified)" in groups):
        return []

    section(f"BY {label.upper()}")
    print(f"  {label:<20}{'Jobs':>6}{'OK':>6}{'Rate':>8}{'Hours':>9}{'Filament':>11}")
    alarms = []
    for name in sorted(groups, key=lambda n: (groups[n]["ok"] / groups[n]["n"])):
        g = groups[name]
        rate = g["ok"] / g["n"]
        print(f"  {name[:19]:<20}{g['n']:>6}{g['ok']:>6}{pct(g['ok'], g['n']):>8}"
              f"{g['h']:>9.1f}{g['g']:>10.0f}g   {bar(rate, 14)}")
        if g["n"] >= 5 and rate < SUCCESS_ALARM:
            confound = dominant_printer(g["failed"]) if check_confound else None
            if confound:
                machine, share = confound
                print(f"      -> {100 * share:.0f}% of these failures were on {machine};"
                      f" likely the machine, not the {label.lower()}")
            else:
                alarms.append(
                    f"{label} {name!r}: {100 * rate:.0f}% success over {g['n']} jobs "
                    f"(target >{100 * SUCCESS_TARGET:.0f}%). Isolate this one rather than "
                    "absorbing it into the average."
                )
    return alarms


def main() -> int:
    p = argparse.ArgumentParser(
        description="Analyse a 3D print job log CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("csv_path", help="Path to the print log CSV")
    p.add_argument("--printer", help="Filter to printers containing this text")
    p.add_argument("--material", help="Filter to materials containing this text")
    p.add_argument("--since", help="Only jobs on or after this date (YYYY-MM-DD)")
    p.add_argument("--available-hours", type=float,
                   help="Machine-hours available in the period, to compute utilisation")
    p.add_argument("--column-map", help="Map canonical columns to yours, e.g. printer=Machine")
    a = p.parse_args()

    column_map = {}
    if a.column_map:
        for pair in a.column_map.split(","):
            if "=" not in pair:
                raise SystemExit(f"--column-map expects canonical=source pairs, got {pair!r}")
            canonical, _, source = pair.partition("=")
            column_map[canonical.strip()] = source.strip()

    try:
        rows = load(a.csv_path, column_map)
    except FileNotFoundError:
        print(f"No such file: {a.csv_path}", file=sys.stderr)
        return 1

    if a.printer:
        rows = [r for r in rows if a.printer.lower() in r["printer"].lower()]
    if a.material:
        rows = [r for r in rows if a.material.lower() in r["material"].lower()]
    if a.since:
        cutoff = to_date(a.since)
        rows = [r for r in rows if (d := to_date(r["date"])) and d >= cutoff]
    if not rows:
        print("No rows matched the filters.", file=sys.stderr)
        return 1

    total = len(rows)
    ok = sum(1 for r in rows if is_success(r))
    grams = sum(to_float(r["filament_g"]) for r in rows)
    hours = sum(to_float(r["print_hours"]) for r in rows)
    post = sum(to_float(r["post_hours"]) for r in rows)
    parts = sum(to_float(r["parts"]) for r in rows if is_success(r))
    good_grams = sum(to_float(r["filament_g"]) for r in rows if is_success(r))
    dates = [d for r in rows if (d := to_date(r["date"]))]

    print()
    print("=" * 68)
    print("  PRINT LOG SUMMARY")
    print("=" * 68)
    print(f"  Jobs         : {total}   ({ok} succeeded, {total - ok} failed)")
    print(f"  Success rate : {pct(ok, total).strip()}   {bar(ok / total)}")
    if dates:
        print(f"  Period       : {min(dates)} to {max(dates)}")
    print(f"  Print hours  : {hours:,.1f}")
    if post:
        print(f"  Labour hours : {post:,.1f}  ({pct(post, post + hours).strip()} of total time)")
    print(f"  Filament     : {grams:,.0f} g")
    if parts:
        print(f"  Good parts   : {parts:,.0f}")

    alarms: list[str] = []
    if total >= 5 and (ok / total) < SUCCESS_ALARM:
        alarms.append(
            f"Overall success rate {100 * ok / total:.0f}% is below the ~{100 * SUCCESS_ALARM:.0f}% "
            "point where something is usually systematically wrong, rather than bad luck."
        )

    # ---- true material cost -----------------------------------------------------
    if grams and parts:
        section("MATERIAL EFFICIENCY")
        wasted = grams - good_grams
        print(f"  Filament into good jobs ....... {good_grams:>9,.0f} g")
        print(f"  Filament lost to failures ..... {wasted:>9,.0f} g   ({pct(wasted, grams).strip()})")
        print(f"  Per good part ................. {grams / parts:>9,.1f} g  (all filament)")
        print(f"  Per good part ................. {good_grams / parts:>9,.1f} g  (successful jobs only)")
        print()
        print("  Cost per part must use the first number, not the second -- the good")
        print("  parts have to carry the filament burnt on the failures.")

    # ---- failure causes ---------------------------------------------------------
    causes = defaultdict(int)
    for r in rows:
        if not is_success(r):
            causes[r["failure_cause"].strip().lower() or "(unrecorded)"] += 1
    if causes:
        section("FAILURE CAUSES")
        for cause, count in sorted(causes.items(), key=lambda kv: -kv[1]):
            print(f"  {cause[:26]:<28}{count:>4}  {pct(count, total - ok):>7}"
                  f"   {bar(count / (total - ok), 14)}")
            for key, hint in CAUSE_HINTS.items():
                if key in cause:
                    print(f"      -> check {hint}")
                    break
        if causes.get("(unrecorded)", 0) > (total - ok) / 2:
            alarms.append(
                "More than half the failures have no recorded cause. The cause column is "
                "what turns this log from a tally into a diagnosis -- record it at the time."
            )

    alarms += breakdown(rows, "printer", "Printer")
    alarms += breakdown(rows, "material", "Material", check_confound=True)
    alarms += breakdown(rows, "profile", "Profile", check_confound=True)

    # ---- utilisation ------------------------------------------------------------
    if a.available_hours:
        section("UTILISATION")
        util = hours / a.available_hours
        print(f"  Printing {hours:,.1f} h of {a.available_hours:,.1f} available"
              f"   {pct(hours, a.available_hours).strip()}   {bar(util)}")
        print()
        if util < 0.4:
            print("  Low utilisation: the machines are not the constraint. Another printer")
            print("  will not help -- demand or post-processing throughput is the limit.")
        elif util > 0.8:
            print("  High utilisation: machine capacity is genuinely the constraint, so")
            print("  adding a printer may pay. Confirm post-processing can keep up first.")

    section("FLAGS")
    if alarms:
        for alarm in dict.fromkeys(alarms):
            print(f"  ! {alarm}")
    else:
        print("  Nothing outside normal ranges.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
