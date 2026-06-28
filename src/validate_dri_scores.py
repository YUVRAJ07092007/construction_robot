"""Validate DRI scored output (Phase 3C framework)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRI_PATH = ROOT / "data" / "dri_scored_scenarios.csv"


def main() -> int:
    if not DRI_PATH.exists():
        print(f"Not found: {DRI_PATH}")
        return 1

    with DRI_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    errors: list[str] = []
    for row in rows:
        rid = row.get("record_id", "?")
        if row.get("score_provenance") != "framework_derived_scenario_relative":
            errors.append(f"{rid}: invalid score_provenance")
        if row.get("dri_applicable") == "yes":
            score = row.get("dri_total_score", "")
            if not score:
                errors.append(f"{rid}: missing dri_total_score")
            else:
                val = int(score)
                if not 0 <= val <= 100:
                    errors.append(f"{rid}: dri_total_score out of range")
        for col in ("dri_access_score", "dri_workflow_score", "dri_surface_score", "dri_evidence_score"):
            if row.get(col):
                val = int(row[col])
                if not 0 <= val <= 100:
                    errors.append(f"{rid}: {col} out of range")

    applicable = [r for r in rows if r.get("dri_applicable") == "yes"]
    ranks = [int(r["dri_rank"]) for r in applicable if r.get("dri_rank")]
    if ranks and sorted(ranks) != list(range(1, len(ranks) + 1)):
        errors.append("dri_rank not a contiguous ranking")

    print(f"Validated {len(rows)} DRI records ({len(applicable)} full DRI).")
    for msg in errors:
        print(f"  ERROR: {msg}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
