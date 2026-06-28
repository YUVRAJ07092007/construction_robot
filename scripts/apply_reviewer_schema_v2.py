"""Apply remaining reviewer-improvement schema updates (v2)."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

DURATION_MAP = {
    "invalid": "invalid",
    "valid": "valid_for_visible_segment_only",
    "valid_for_visible_segment_only": "valid_for_visible_segment_only",
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ensure_columns(header: list[str], rows: list[dict[str, str]], columns: list[str]) -> list[str]:
    out = list(header)
    for col in columns:
        if col not in out:
            out.append(col)
        for row in rows:
            row.setdefault(col, "")
    return out


def map_visible_duration(row: dict[str, str]) -> None:
    validity = (row.get("visible_duration_validity") or row.get("duration_validity") or "").strip().lower()
    row["visible_duration_validity"] = DURATION_MAP.get(validity, validity or "invalid")
    if not row.get("duration_validity"):
        row["duration_validity"] = row["visible_duration_validity"]
    if not row.get("visible_segment_duration_sec"):
        row["visible_segment_duration_sec"] = (
            row.get("segment_duration_sec") or row.get("task_duration_observed") or ""
        )
    if not row.get("duration_validity_reason") and row.get("reason_for_rejection"):
        row["duration_validity_reason"] = row["reason_for_rejection"]
    row.setdefault("usable_for_productivity", "no")
    if row.get("usable_for_productivity", "").lower() != "no":
        row["usable_for_productivity"] = "no"


def patch_segments() -> None:
    path = DATA / "video_segments.csv"
    header, rows = read_csv(path)
    header = ensure_columns(
        header,
        rows,
        [
            "visible_duration_validity",
            "duration_validity_reason",
            "continuous_unedited_segment",
            "time_lapse_or_jump_cut",
            "usable_for_productivity",
        ],
    )
    for row in rows:
        map_visible_duration(row)
        row.setdefault("continuous_unedited_segment", "no")
        row.setdefault("time_lapse_or_jump_cut", "yes" if row.get("duration_validity") == "invalid" else "no")
    write_csv(path, header, rows)


def patch_observations(name: str, *, add_parallel_note: bool) -> None:
    path = DATA / name
    header, rows = read_csv(path)
    extra = ["visible_duration_validity", "duration_validity_reason", "usable_for_productivity"]
    if add_parallel_note:
        extra.append("parallel_source_note")
    header = ensure_columns(header, rows, extra)
    for row in rows:
        map_visible_duration(row)
        if add_parallel_note and not row.get("parallel_source_note"):
            row["parallel_source_note"] = row.get("label_revision_note", "")
    write_csv(path, header, rows)


def patch_cleaned() -> None:
    path = DATA / "cleaned_video_dataset.csv"
    header, rows = read_csv(path)
    header = ensure_columns(
        header,
        rows,
        ["visible_duration_validity", "parallel_source_note", "continuous_unedited_segment", "time_lapse_or_jump_cut"],
    )
    for row in rows:
        map_visible_duration(row)
        if not row.get("parallel_source_note"):
            row["parallel_source_note"] = row.get("label_revision_note", "")
        row.setdefault("continuous_unedited_segment", "no")
        row.setdefault("time_lapse_or_jump_cut", "yes")
    write_csv(path, header, rows)


def sync_pilot_synthetic_names() -> None:
    mapping = {
        "synthetic_scenario_dataset.csv": "pilot_rule_based_synthetic_scenarios.csv",
        "synthetic_scenario_dataset_gan.csv": "pilot_gan_synthetic_scenarios.csv",
        "synthetic_scenario_dataset_all.csv": "pilot_combined_synthetic_scenarios.csv",
    }
    for src, dst in mapping.items():
        source = DATA / src
        if source.exists():
            shutil.copy2(source, DATA / dst)


def patch_manufacturer_template() -> None:
    path = DATA / "templates" / "manufacturer_specs_template.csv"
    header, rows = read_csv(path)
    header = ensure_columns(
        header,
        rows,
        [
            "claim_type",
            "claim_use",
            "independent_verification_status",
            "used_in_model",
            "model_use_note",
        ],
    )
    write_csv(path, header, rows)


def main() -> int:
    patch_segments()
    patch_observations("robot_video_observations.csv", add_parallel_note=True)
    patch_observations("mivan_video_observations.csv", add_parallel_note=False)
    patch_cleaned()
    sync_pilot_synthetic_names()
    patch_manufacturer_template()
    print("Reviewer schema v2 applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
