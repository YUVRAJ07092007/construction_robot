"""Add pilot metadata columns to existing synthetic scenario CSVs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.expand_scenarios import OUTPUT_HEADER, pilot_metadata, read_csv, write_csv  # noqa: E402

DATA = ROOT / "data"
FILES = {
    "synthetic_scenario_dataset.csv": "rule_expanded",
    "synthetic_scenario_dataset_gan.csv": "tabular_vae",
    "synthetic_scenario_dataset_all.csv": "mixed_pilot",
}


def patch_file(name: str, default_method: str) -> None:
    path = DATA / name
    if not path.exists():
        return
    rows = read_csv(path)
    for row in rows:
        method = row.get("generation_method") or row.get("synthetic_generation_method") or default_method
        meta = pilot_metadata(
            generation_method=method,
            note=row.get("generation_note") or f"Pilot synthetic row in {name}",
        )
        for key, value in meta.items():
            row.setdefault(key, value)
        if not row.get("record_origin"):
            row["record_origin"] = "synthetic_pilot"
    write_csv(path, OUTPUT_HEADER, rows)
    print(f"Patched {len(rows)} rows in {name}")


def main() -> int:
    for name, default in FILES.items():
        patch_file(name, default)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
