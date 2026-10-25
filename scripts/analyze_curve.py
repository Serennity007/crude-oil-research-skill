#!/usr/bin/env python3
"""Describe one benchmark's dated oil futures curve; no price forecast or roll return."""
import argparse
from datetime import date
from pathlib import Path
import re

from market_io import timestamp, number, records, provenance, emit, kind


def analyze(raw, as_of, data_kind):
    cutoff = timestamp(as_of)
    rows = records(raw, ["contract", "delivery_month", "price", "quote_time", "benchmark", "currency", "unit"])
    selected, excluded, contracts, months = [], 0, set(), set()
    for row in rows:
        observed = timestamp(row["quote_time"])
        if observed > cutoff:
            excluded += 1
            continue
        month = row["delivery_month"]
        if not re.fullmatch(r"\d{4}-\d{2}", month):
            raise ValueError("delivery_month must be YYYY-MM")
        date.fromisoformat(month + "-01")
        if not row["contract"] or row["contract"] in contracts or month in months:
            raise ValueError("contracts and delivery months must be unique")
        contracts.add(row["contract"])
        months.add(month)
        if row["benchmark"] not in ("WTI", "BRENT", "SC") or not re.fullmatch(r"[A-Z]{3}", row["currency"]) or row["unit"] != "currency_per_barrel":
            raise ValueError("declare benchmark, three-letter currency and currency_per_barrel units")
        selected.append({"contract": row["contract"], "delivery_month": month,
                         "price": number(row["price"]), "quote_time": observed.isoformat(),
                         "benchmark": row["benchmark"], "currency": row["currency"], "unit": row["unit"]})
    if len(selected) < 2:
        raise ValueError("at least two included delivery months are needed")
    for field in ("benchmark", "currency", "unit"):
        if len({row[field] for row in selected}) != 1:
            raise ValueError("mixed benchmarks/currencies/units cannot form this curve")
    selected.sort(key=lambda row: row["delivery_month"])
    differences = [right["price"] - left["price"] for left, right in zip(selected, selected[1:])]
    shape = "contango" if all(x > 0 for x in differences) else "backwardation" if all(x < 0 for x in differences) else "flat" if all(x == 0 for x in differences) else "mixed"
    near, far = selected[0], selected[-1]
    times = [timestamp(row["quote_time"]) for row in selected]
    return {"schema_version": 1, "data_kind": kind(data_kind), "as_of_utc": cutoff.isoformat(),
            "benchmark": near["benchmark"], "currency": near["currency"], "unit": near["unit"],
            "quotes": selected, "curve_shape": shape, "near_minus_far": near["price"] - far["price"],
            "near_minus_far_over_near": (near["price"] - far["price"]) / near["price"] if near["price"] > 0 else None,
            "nonpositive_quotes_present": any(row["price"] <= 0 for row in selected),
            "quote_span_seconds": (max(times) - min(times)).total_seconds(),
            "oldest_quote_age_seconds": (cutoff - min(times)).total_seconds(),
            "excluded_future_quotes": excluded, "source_sha256": provenance(raw),
            "scope": "Curve description only; futures curve is not a guaranteed forecast, roll return or realized P&L.",
            "limitations": ["No exchange expiry/calendar, liquidity, inventory or active-contract verification",
                            "Quotes may be asynchronous; inspect their span and ages",
                            "Signed prices allowed; percentage spread omitted for nonpositive near price"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--data-kind", required=True, choices=("synthetic", "imported_observations"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = analyze(args.csv.read_bytes(), args.as_of, args.data_kind)
        emit(result, args.out, [args.csv])
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(f"Saved {result['curve_shape']} curve / {result['data_kind']}; no trade instruction.")


if __name__ == "__main__":
    main()
