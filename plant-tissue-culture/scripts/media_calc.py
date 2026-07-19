#!/usr/bin/env python3
"""Media formulation calculator for plant tissue culture.

Two modes:

  Recipe   Build a printable recipe card for a batch of medium, including the exact
           volume of each PGR stock to pipette.

             python media_calc.py --volume 1L --base MS --sucrose 30 --agar 7 \
                 --pgr BAP=2.0 --pgr NAA=0.1

  Stock    Work out how to prepare a PGR stock solution.

             python media_calc.py --stock BAP --stock-conc 1.0 --stock-volume 100

The arithmetic here is trivial but it is also where batches are most often lost --
a tenfold slip on TDZ or a stock made at the wrong strength reads downstream as a
mysterious protocol failure. Running it beats doing it in your head.
"""

from __future__ import annotations

import argparse
import re
import sys

# Premix powder (g/L) giving full-strength medium, plus notes on where each base fits.
BASE_MEDIA = {
    "MS": (4.40, "Murashige & Skoog 1962 -- default for most herbaceous species"),
    "MS_NOVIT": (4.30, "MS basal salts without vitamins -- add vitamins separately"),
    "WPM": (2.41, "Lloyd & McCown Woody Plant Medium -- woody and ericaceous species"),
    "DKW": (5.32, "Driver & Kuniyuki Walnut -- temperate woody, fruit and nut trees"),
    "B5": (3.21, "Gamborg B5 -- legumes, protoplast and suspension culture"),
    "SH": (3.60, "Schenk & Hildebrandt -- monocots, some callus work"),
    "KC": (2.60, "Knudson C -- orchid seed and protocorm culture"),
    "VW": (2.60, "Vacin & Went -- orchid culture"),
}

# molar mass is not needed for mg/L work; what matters operationally is the solvent
# and whether the compound survives the autoclave.
PGRS = {
    # name:      (class,      solvent,             autoclavable, typical mg/L range)
    "BAP": ("cytokinin", "1N NaOH or 1N HCl", True, "0.5-3"),
    "BA": ("cytokinin", "1N NaOH or 1N HCl", True, "0.5-3"),
    "KIN": ("cytokinin", "1N NaOH, warm", True, "0.5-5"),
    "KINETIN": ("cytokinin", "1N NaOH, warm", True, "0.5-5"),
    "2IP": ("cytokinin", "1N NaOH", True, "1-15"),
    "TDZ": ("cytokinin", "DMSO or dilute NaOH", True, "0.01-1"),
    "MT": ("cytokinin", "1N NaOH", True, "0.5-5"),
    "META-TOPOLIN": ("cytokinin", "1N NaOH", True, "0.5-5"),
    "ZEATIN": ("cytokinin", "1N NaOH", False, "0.1-5"),
    "IBA": ("auxin", "1N NaOH or warm ethanol", True, "0.1-3"),
    "NAA": ("auxin", "1N NaOH or warm ethanol", True, "0.01-2"),
    "IAA": ("auxin", "1N NaOH or ethanol", False, "0.1-10"),
    "2,4-D": ("auxin", "1N NaOH or ethanol", True, "0.5-5"),
    "2,4D": ("auxin", "1N NaOH or ethanol", True, "0.5-5"),
    "GA3": ("gibberellin", "ethanol", False, "0.1-2"),
    "ABA": ("inhibitor", "1N NaOH or ethanol", False, "0.1-5"),
    "PBZ": ("retardant", "ethanol or DMSO", True, "0.1-5"),
    "PACLOBUTRAZOL": ("retardant", "ethanol or DMSO", True, "0.1-5"),
}

# Compounds where a tenfold error is especially likely or especially costly.
POTENCY_WARNINGS = {
    "TDZ": "TDZ is dosed 10-100x lower than BAP. Confirm you meant mg/L, not the BAP-scale number.",
    "2,4-D": "2,4-D drives somaclonal variation. Do not use it in a line meant to stay true-to-type.",
    "2,4D": "2,4-D drives somaclonal variation. Do not use it in a line meant to stay true-to-type.",
}


def parse_volume(text: str) -> float:
    """Return litres. Accepts '1L', '500mL', '250 ml', or a bare number (litres)."""
    match = re.fullmatch(r"\s*([\d.]+)\s*(l|ml|litre|liter|litres|liters)?\s*", text, re.I)
    if not match:
        raise argparse.ArgumentTypeError(f"could not read volume {text!r}; try '1L' or '500mL'")
    value = float(match.group(1))
    unit = (match.group(2) or "l").lower()
    return value / 1000.0 if unit == "ml" else value


def parse_pgr(text: str) -> tuple[str, float]:
    """Parse 'BAP=2.0' into ('BAP', 2.0) mg/L."""
    if "=" not in text:
        raise argparse.ArgumentTypeError(f"expected NAME=mg/L, got {text!r}")
    name, _, value = text.partition("=")
    try:
        return name.strip().upper(), float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"could not read a mg/L value from {text!r}")


def pgr_info(name: str):
    return PGRS.get(name.upper())


def recipe(args) -> int:
    litres = parse_volume(args.volume)
    base_key = args.base.upper()
    if base_key not in BASE_MEDIA:
        print(f"Unknown base medium {args.base!r}. Known: {', '.join(sorted(BASE_MEDIA))}",
              file=sys.stderr)
        return 1
    per_litre, base_note = BASE_MEDIA[base_key]
    strength = args.strength
    basal_g = per_litre * strength * litres

    print()
    print("=" * 66)
    print(f"  MEDIUM RECIPE  --  {litres:g} L")
    print("=" * 66)
    strength_label = "full" if strength == 1.0 else f"{strength:g}x"
    print(f"  Base medium : {base_key} ({strength_label} strength)")
    print(f"                {base_note}")
    print()
    print("  Weigh into ~2/3 the final volume of distilled water:")
    print()
    print(f"    {(base_key + ' premix '):.<36} {basal_g:8.3f} g"
          f"   ({per_litre * strength:g} g/L)")
    if args.sucrose:
        print(f"    {'Sucrose ':.<36} {args.sucrose * litres:8.3f} g"
              f"   ({args.sucrose:g} g/L)")
    if args.inositol:
        print(f"    {'Myo-inositol ':.<36} {args.inositol * litres:8.1f} mg"
              f"   ({args.inositol:g} mg/L)")
    for name, mg_per_l in args.additive:
        print(f"    {name[:33]:.<36} {mg_per_l * litres:8.1f} mg   ({mg_per_l:g} mg/L)")

    heat_labile: list[str] = []
    unknown: list[str] = []
    tiny: list[tuple[str, float]] = []
    if args.pgr:
        print()
        print(f"  Add PGR stocks (stocks at {args.stock_conc:g} mg/mL):")
        print()
        for name, mg_per_l in args.pgr:
            stock_ml = (mg_per_l * litres) / args.stock_conc
            info = pgr_info(name)
            flag = ""
            if info is None:
                unknown.append(name)
                flag = "  [unknown compound]"
            elif not info[2]:
                heat_labile.append(name)
                flag = "  [FILTER-STERILIZE]"
            if stock_ml < 0.1:
                tiny.append((name, stock_ml))
            print(f"    {name:<12} {mg_per_l:>6.3f} mg/L  ->  {stock_ml:7.3f} mL of stock{flag}")

    print()
    print(f"  Bring to {litres:g} L with distilled water.")
    print(f"  Adjust pH to {args.ph:g} with 0.1N KOH / HCl  (BEFORE adding gelling agent).")
    if args.agar:
        print(f"  Add agar ............................. {args.agar * litres:8.3f} g"
              f"   ({args.agar:g} g/L)")
    if args.gellan:
        print(f"  Add gellan gum ....................... {args.gellan * litres:8.3f} g"
              f"   ({args.gellan:g} g/L)")
    print(f"  Dispense, then autoclave 121 C / 15 psi for {args.autoclave} min.")
    print()

    notes: list[str] = []
    if heat_labile:
        notes.append(
            f"{', '.join(heat_labile)} is heat-labile. Do NOT autoclave it: filter-sterilize "
            "through 0.22 um and add to molten medium cooled to ~50 C (hand-warm)."
        )
    for name, _ in args.pgr:
        if name.upper() in POTENCY_WARNINGS:
            notes.append(POTENCY_WARNINGS[name.upper()])
    for name, volume in tiny:
        notes.append(
            f"{name} needs only {volume:.3f} mL of stock -- below reliable pipetting accuracy. "
            f"Make a 10x or 100x dilute working stock of {name} and pipette a larger volume, "
            "or scale the batch up. Measuring this by eye is how tenfold dosing errors happen."
        )
    if unknown:
        notes.append(
            f"No reference data for {', '.join(unknown)} -- verify its solvent, heat stability "
            "and working range against a source before use."
        )
    if args.agar and args.agar < 6:
        notes.append(
            f"Agar at {args.agar:g} g/L is soft. Below ~6 g/L hyperhydricity risk rises sharply."
        )
    if args.ph < 5.4 or args.ph > 6.0:
        notes.append(
            f"pH {args.ph:g} is outside the usual 5.7-5.8 window. Agar gels poorly below ~4.8 "
            "and iron availability drops above ~6.5."
        )
    cyto = sum(v for n, v in args.pgr if (pgr_info(n) or ("",))[0] == "cytokinin")
    auxin = sum(v for n, v in args.pgr if (pgr_info(n) or ("",))[0] == "auxin")
    if cyto and auxin:
        notes.append(
            f"Cytokinin:auxin ratio is {cyto / auxin:.1f}:1 "
            f"({cyto:g} : {auxin:g} mg/L). High favours shoots, balanced favours callus, "
            "low favours roots."
        )
    elif cyto and not auxin:
        notes.append(f"Cytokinin only ({cyto:g} mg/L) -- shoot multiplication medium.")
    elif auxin and not cyto:
        notes.append(f"Auxin only ({auxin:g} mg/L) -- rooting or callus induction medium.")

    if notes:
        print("  NOTES")
        for note in notes:
            print(f"    - {note}")
        print()
    print("  Record the basal salt LOT NUMBER against this batch. Lot-to-lot")
    print("  micronutrient differences explain many 'it suddenly stopped working' cases.")
    print()
    return 0


def stock(args) -> int:
    name = args.stock.upper()
    info = pgr_info(name)
    mg_needed = args.stock_conc * args.stock_volume

    print()
    print("=" * 66)
    print(f"  STOCK SOLUTION  --  {name}")
    print("=" * 66)
    print(f"  Target : {args.stock_conc:g} mg/mL  ({args.stock_conc * 1000:g} ppm)"
          f" in {args.stock_volume:g} mL")
    print()
    print(f"    1. Weigh {mg_needed:.1f} mg of {name}.")
    if info:
        print(f"    2. Dissolve in a minimum volume of {info[1]} -- a few drops, warming gently.")
    else:
        print("    2. Dissolve in the minimum volume of the appropriate solvent")
        print("       (auxins: 1N NaOH or warm ethanol; cytokinins: 1N NaOH or HCl).")
    print(f"    3. Once fully dissolved, bring to {args.stock_volume:g} mL with distilled water.")
    print("    4. Label with compound, concentration, solvent and date. Store at 4 C, amber.")
    print()
    if args.stock_conc == 1.0:
        print("  At 1 mg/mL, 1 mL of stock per litre of medium = 1 mg/L final.")
    else:
        per_mg = 1.0 / args.stock_conc
        print(f"  At {args.stock_conc:g} mg/mL, {per_mg:.3f} mL per litre of medium = 1 mg/L final.")
    if info:
        print(f"  Class: {info[0]}.  Typical working range: {info[3]} mg/L.")
        print("  Autoclavable." if info[2] else
              "  HEAT-LABILE -- filter-sterilize, add to medium cooled to ~50 C.")
    print()
    print("  Discard auxin and GA3 stocks after ~1 month, cytokinins after ~3.")
    print("  A degraded stock presents as an unexplained protocol failure.")
    print()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plant tissue culture media and stock solution calculator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--volume", default="1L",
                        help="Batch volume, e.g. 1L, 500mL. Bare numbers are litres.")
    parser.add_argument("--base", default="MS",
                        help=f"Base medium: {', '.join(sorted(BASE_MEDIA))}")
    parser.add_argument("--strength", type=float, default=1.0,
                        help="Fraction of full strength, e.g. 0.5 for half-MS (default 1.0)")
    parser.add_argument("--sucrose", type=float, default=30.0, help="g/L (default 30)")
    parser.add_argument("--agar", type=float, default=7.0, help="g/L (default 7; 0 to omit)")
    parser.add_argument("--gellan", type=float, default=0.0, help="g/L gellan gum (default 0)")
    parser.add_argument("--inositol", type=float, default=0.0,
                        help="mg/L myo-inositol (usually already in 'with vitamins' premixes)")
    parser.add_argument("--ph", type=float, default=5.7, help="Target pH (default 5.7)")
    parser.add_argument("--autoclave", type=int, default=20, help="Minutes at 121 C (default 20)")
    parser.add_argument("--pgr", action="append", type=parse_pgr, default=[], metavar="NAME=MG/L",
                        help="PGR at mg/L, repeatable. e.g. --pgr BAP=2.0 --pgr NAA=0.1")
    parser.add_argument("--additive", action="append", type=parse_pgr, default=[],
                        metavar="NAME=MG/L", help="Other additive in mg/L, repeatable")
    parser.add_argument("--stock-conc", type=float, default=1.0,
                        help="PGR stock concentration in mg/mL (default 1.0)")
    parser.add_argument("--stock", metavar="NAME",
                        help="Stock-preparation mode: how to make a stock of this compound")
    parser.add_argument("--stock-volume", type=float, default=100.0,
                        help="Stock volume to prepare, mL (default 100)")

    args = parser.parse_args()
    return stock(args) if args.stock else recipe(args)


if __name__ == "__main__":
    sys.exit(main())
