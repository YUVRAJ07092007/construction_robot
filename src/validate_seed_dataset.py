"""Validate GAN seed dataset produced by Stage 2 conversion."""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.validate_extractions import load_activity_taxonomy, resolve_activity_label  # noqa: E402

DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
SEED_PATH = DATA_DIR / "gan_seed_dataset.csv"

REQUIRED_COLS = [
    "seed_id",
    "source_observation_id",
    "video_category",
    "activity_group",
    "workflow_stage",
    "data_use",
    "duration_excluded",
    "usable_for_productivity",
    "independent_sample",
]


@dataclass
class SeedValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_seed_dataset(rows: list[dict[str, str]]) -> SeedValidationResult:
    result = SeedValidationResult()
    if not rows:
        result.add_error("gan_seed_dataset.csv is empty")
        return result

    missing = [col for col in REQUIRED_COLS if col not in rows[0]]
    if missing:
        result.add_error(f"missing columns: {missing}")
        return result

    groups, legacy, _context = load_activity_taxonomy()
    seen_ids: set[str] = set()
    seen_sources: set[str] = set()

    for row in rows:
        sid = row.get("seed_id", "?")
        if sid in seen_ids:
            result.add_error(f"{sid}: duplicate seed_id")
        seen_ids.add(sid)

        source = row.get("source_observation_id", "")
        if source in seen_sources:
            result.add_error(f"{sid}: duplicate source_observation_id {source}")
        seen_sources.add(source)

        if row.get("data_use") != "framework_seed_ready":
            result.add_error(f"{sid}: data_use must be framework_seed_ready")
        if row.get("duration_excluded") != "yes":
            result.add_error(f"{sid}: duration_excluded must be yes")
        if row.get("usable_for_productivity") != "no":
            result.add_error(f"{sid}: usable_for_productivity must be no")
        if row.get("independent_sample") != "yes":
            result.add_error(f"{sid}: independent_sample must be yes")

        activity = (row.get("activity_group") or "").strip()
        if activity and resolve_activity_label(activity, groups, legacy) is None:
            result.add_error(f"{sid}: activity_group '{activity}' not in taxonomy")

        if row.get("seed_provenance") != "video_observed_secondary":
            result.add_warning(f"{sid}: unexpected seed_provenance")

    return result


def write_report(result: SeedValidationResult) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Seed Dataset Validation Report",
        "",
        f"- **Critical errors:** {len(result.errors)}",
        f"- **Warnings:** {len(result.warnings)}",
        "",
    ]
    for title, items in (("Critical errors", result.errors), ("Warnings", result.warnings)):
        lines.append(f"## {title}")
        lines.append("")
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- None")
        lines.append("")
    (REPORTS_DIR / "seed_validation_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not SEED_PATH.exists():
        print(f"Seed dataset not found: {SEED_PATH}")
        return 1
    rows = read_csv(SEED_PATH)
    result = validate_seed_dataset(rows)
    write_report(result)
    if result.errors:
        for err in result.errors:
            print(f"  - {err}")
        return 1
    print(f"Seed validation passed ({len(rows)} records).")
    if result.warnings:
        print(f"Warnings: {len(result.warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
