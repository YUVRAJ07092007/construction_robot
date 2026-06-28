"""Validate video-derived CSV rows against schema and construction logic rules."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.extraction_config import (  # noqa: E402
    ACCESS_CONDITION_FIELD,
    MIN_SEGMENT_DURATION_SEC,
    SUITABILITY_BANDS,
)

DATA_DIR = ROOT / "data"
TEMPLATES_DIR = DATA_DIR / "templates"

REQUIRED_METADATA_COLS = [
    "video_id",
    "video_url",
    "video_category",
    "platform",
    "title",
    "source_name",
    "access_date",
    "activity_focus",
    "construction_context",
    "total_video_duration",
    "visibility_quality",
    "coding_confidence",
    "inclusion_status",
    "suitability_total_score",
    "suitability_band",
    "notes",
]

REQUIRED_SEGMENT_COLS = [
    "segment_id",
    "video_id",
    "start_time",
    "end_time",
    "segment_duration_sec",
    "activity_type",
    "segment_category",
    "segment_quality",
    "duration_validity",
    "reason_for_rejection",
]

REQUIRED_CLEANED_COLS = [
    "observation_id",
    "video_id",
    "segment_id",
    "video_category",
    "activity_type",
    "workflow_stage",
    "labour_count_visible",
    "robot_operator_count",
    "movement_pattern",
    "operating_surface",
    "congestion_level",
    "reinforcement_complexity",
    ACCESS_CONDITION_FIELD,
    "safety_condition",
    "task_duration_observed",
    "duration_validity",
    "evidence_level",
    "coding_confidence",
    "source_type",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_columns(name: str, rows: list[dict[str, str]], required: list[str]) -> list[str]:
    errors: list[str] = []
    if not rows:
        return errors
    missing = [col for col in required if col not in rows[0]]
    if missing:
        errors.append(f"{name}: missing columns {missing}")
    return errors


def validate_suitability_scores(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        vid = row.get("video_id", "?")
        raw_score = (row.get("suitability_total_score") or "").strip()
        if not raw_score or raw_score.lower() in {"n/a", "na"}:
            continue
        try:
            score = int(raw_score)
        except ValueError:
            errors.append(f"video {vid}: suitability_total_score must be integer")
            continue
        band = row.get("suitability_band", "")
        expected = None
        for label, (lo, hi) in SUITABILITY_BANDS.items():
            if lo <= score <= hi:
                expected = label
                break
        if expected and band and band not in {expected, "manufacturer_reported_E3"}:
            errors.append(
                f"video {vid}: score {score} implies band '{expected}', got '{band}'"
            )
    return errors


def validate_cleaned_logic(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        oid = row.get("observation_id", "?")
        activity = (row.get("activity_type") or "").lower()
        stage = (row.get("workflow_stage") or "").lower()
        surface = (row.get("operating_surface") or "").lower()
        congestion = (row.get("congestion_level") or "").lower()
        access = (row.get(ACCESS_CONDITION_FIELD) or "").lower()
        safety = (row.get("safety_condition") or "").lower()
        duration_validity = (row.get("duration_validity") or "").lower()
        confidence = (row.get("coding_confidence") or "").lower()
        visibility = (row.get("visibility_quality") or "").lower()

        if "rebar" in activity and stage and stage not in {"pre-pour", "unknown", ""}:
            errors.append(f"{oid}: rebar activity should have workflow_stage pre-pour")
        if "leveling" in activity and surface and "wet" not in surface and surface != "unknown":
            errors.append(f"{oid}: leveling activity expects wet concrete surface")
        if "grinding" in activity and surface and "hardened" not in surface and surface != "unknown":
            errors.append(f"{oid}: grinding activity expects hardened concrete surface")
        if congestion == "high" and access == "open":
            errors.append(f"{oid}: high congestion conflicts with open access_condition")
        if duration_validity == "valid" and confidence == "low":
            errors.append(f"{oid}: low confidence should not pair with valid duration for quant use")
        if visibility == "low" and confidence == "high":
            errors.append(f"{oid}: low visibility_quality conflicts with high coding_confidence")

    return errors


def validate_segments(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        sid = row.get("segment_id", "?")
        try:
            duration = float(row.get("segment_duration_sec") or 0)
        except ValueError:
            errors.append(f"segment {sid}: segment_duration_sec must be numeric")
            continue
        rejected = (row.get("reason_for_rejection") or "").strip()
        if duration < MIN_SEGMENT_DURATION_SEC and not rejected:
            errors.append(
                f"segment {sid}: duration {duration}s below minimum "
                f"{MIN_SEGMENT_DURATION_SEC}s (reject or add reason_for_rejection)"
            )
    return errors


def main() -> int:
    all_errors: list[str] = []
    metadata = read_csv(DATA_DIR / "video_metadata.csv")
    segments = read_csv(DATA_DIR / "video_segments.csv")
    cleaned = read_csv(DATA_DIR / "cleaned_video_dataset.csv")

    all_errors.extend(check_columns("video_metadata", metadata, REQUIRED_METADATA_COLS))
    all_errors.extend(check_columns("video_segments", segments, REQUIRED_SEGMENT_COLS))
    all_errors.extend(check_columns("cleaned_video_dataset", cleaned, REQUIRED_CLEANED_COLS))
    all_errors.extend(validate_suitability_scores(metadata))
    all_errors.extend(validate_segments(segments))
    all_errors.extend(validate_cleaned_logic(cleaned))

    if all_errors:
        print("Validation failed:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
