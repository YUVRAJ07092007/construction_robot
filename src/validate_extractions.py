"""Validate video-derived CSV rows; emit reports with errors, warnings, and suggestions."""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.extraction_config import (  # noqa: E402
    ACCESS_CONDITION_FIELD,
    MIN_SEGMENT_DURATION_SEC,
    SUITABILITY_BANDS,
    VIDEO_EVIDENCE_LEVELS,
)

DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"

VALID_EVIDENCE = {"E1", "E2", "E3", "E4", "E5"}
VALID_SOURCE_TYPES = {
    "video_observed",
    "video_estimated",
    "video-observed",
    "video-estimated",
    "manufacturer_reported",
    "computed",
    "assumption_based",
    "literature_reported",
    "project_document_derived",
}
VALID_DATA_USE = {"exclude", "qualitative_only", "structured_coding", "modelling_ready"}
FRESH_ACTIVITIES = {"fresh_concrete_leveling", "fresh_concrete_finishing", "concrete_leveling"}
POST_CAST_ACTIVITIES = {"post_cast_floor_grinding", "post_cast_coating", "post_cast_surface_preparation", "floor_grinding"}
WET_SURFACES = {"wet_concrete", "pre_pour_slab", "pre-pour", "wet", "partially_set"}
HARDENED_SURFACES = {"hardened_concrete", "hardened", "post_cast", "post-cast"}

REQUIRED_METADATA_COLS = [
    "video_id", "video_url", "video_category", "platform", "title", "source_name",
    "access_date", "activity_focus", "construction_context", "total_video_duration",
    "visibility_quality", "coding_confidence", "inclusion_status", "suitability_total_score",
    "suitability_band", "notes",
]
REQUIRED_SEGMENT_COLS = [
    "segment_id", "video_id", "start_time", "end_time", "segment_duration_sec",
    "activity_type", "segment_category", "segment_quality", "duration_validity",
    "reason_for_rejection",
]
REQUIRED_CLEANED_COLS = [
    "observation_id", "video_id", "segment_id", "video_category", "activity_type",
    "workflow_stage", "labour_count_visible", "robot_operator_count", "movement_pattern",
    "operating_surface", "congestion_level", "reinforcement_complexity",
    ACCESS_CONDITION_FIELD, "safety_condition", "task_duration_observed",
    "duration_validity", "evidence_level", "coding_confidence", "source_type",
]


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def add(self, level: str, message: str) -> None:
        getattr(self, level).append(message)


@lru_cache(maxsize=1)
def load_activity_taxonomy() -> tuple[frozenset[str], dict[str, str]]:
    path = ROOT / "config" / "activity_taxonomy.yaml"
    if yaml is None:
        raise RuntimeError("PyYAML required for activity taxonomy validation")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    groups = frozenset(data["activity_groups"].keys())
    legacy = {str(k): str(v) for k, v in (data.get("legacy_label_map") or {}).items()}
    return groups, legacy


def resolve_activity_label(label: str, groups: frozenset[str], legacy: dict[str, str]) -> str | None:
    if not label or label.strip().lower() in {"", "unknown", "other"}:
        return label
    raw = label.strip()
    if raw in groups:
        return raw
    mapped = legacy.get(raw) or legacy.get(raw.lower())
    if mapped in groups:
        return mapped
    return None


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_columns(result: ValidationResult, name: str, rows: list[dict[str, str]], required: list[str]) -> None:
    if not rows:
        result.add("warnings", f"{name}: file empty or missing rows")
        return
    missing = [col for col in required if col not in rows[0]]
    if missing:
        result.add("errors", f"{name}: missing columns {missing}")


def validate_suitability_scores(result: ValidationResult, rows: list[dict[str, str]]) -> None:
    for row in rows:
        vid = row.get("video_id", "?")
        raw_score = (row.get("suitability_total_score") or row.get("suitability_score") or "").strip()
        if not raw_score or raw_score.lower() in {"n/a", "na"}:
            continue
        try:
            score = int(raw_score)
        except ValueError:
            result.add("errors", f"video {vid}: suitability score must be integer")
            continue
        band = row.get("suitability_band", "")
        expected = None
        for label, (lo, hi) in SUITABILITY_BANDS.items():
            if lo <= score <= hi:
                expected = label
                break
        if expected and band and band not in {expected, "manufacturer_reported_E3", "source_pool"}:
            result.add("errors", f"video {vid}: score {score} implies band '{expected}', got '{band}'")
        data_use = (row.get("data_use") or "").strip()
        if band == "structured_extraction" and data_use == "exclude":
            result.add("errors", f"video {vid}: structured_extraction must not have data_use=exclude")


def validate_segments(result: ValidationResult, rows: list[dict[str, str]]) -> None:
    for row in rows:
        sid = row.get("segment_id", "?")
        try:
            duration = float(row.get("segment_duration_sec") or row.get("visible_segment_duration_sec") or 0)
        except ValueError:
            result.add("errors", f"segment {sid}: duration must be numeric")
            continue
        rejected = (row.get("reason_for_rejection") or "").strip()
        if duration < MIN_SEGMENT_DURATION_SEC and not rejected:
            result.add(
                "errors",
                f"segment {sid}: duration {duration}s below minimum {MIN_SEGMENT_DURATION_SEC}s",
            )
        productivity = (row.get("usable_for_productivity") or "").lower()
        validity = (row.get("duration_validity") or "").lower()
        if productivity == "yes":
            result.add("errors", f"segment {sid}: public video must not be usable_for_productivity=yes")
        if validity == "valid" and productivity == "yes":
            result.add("errors", f"segment {sid}: invalid productivity pairing")


def validate_cleaned_logic(result: ValidationResult, rows: list[dict[str, str]]) -> None:
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
        evidence = (row.get("evidence_level") or "").upper()
        source_type = (row.get("source_type") or "").lower()
        data_use = (row.get("data_use") or "").lower()
        productivity = (row.get("usable_for_productivity") or "").lower()

        if evidence and evidence not in VALID_EVIDENCE:
            result.add("errors", f"{oid}: invalid evidence_level '{evidence}'")
        if evidence in {"E3", "E4", "E5"}:
            result.add("errors", f"{oid}: video observation must not use evidence {evidence}")
        if "rebar" in activity and stage and stage not in {"pre-pour", "unknown", ""}:
            result.add("errors", f"{oid}: rebar activity should have workflow_stage pre-pour")
        if any(x in activity for x in ("concrete_pour", "concrete_pouring")) and stage and stage not in {"pour", "unknown", ""}:
            result.add("errors", f"{oid}: concrete pouring activity should have workflow_stage pour")
        if "fresh_concrete_finishing" in activity and surface:
            if not any(w in surface for w in WET_SURFACES | {"partially_set"}) and surface not in {"", "unknown"}:
                result.add("warnings", f"{oid}: fresh concrete finishing expects wet or partially set surface")
        if "post_cast_floor_grinding" in activity and surface:
            if not any(h in surface for h in HARDENED_SURFACES) and surface not in {"", "unknown"}:
                result.add("warnings", f"{oid}: post-cast grinding expects hardened surface")
        if "post_cast_coating" in activity and any(x in activity for x in ("fresh_concrete", "leveling")):
            result.add("errors", f"{oid}: post-cast coating must not be labelled as fresh concrete finishing")
        if any(x in activity for x in ("leveling", "fresh_concrete")) and surface:
            if not any(w in surface for w in WET_SURFACES) and surface != "unknown":
                result.add("warnings", f"{oid}: leveling/fresh activity expects wet surface")
        if any(x in activity for x in POST_CAST_ACTIVITIES) and surface:
            if not any(h in surface for h in HARDENED_SURFACES) and surface not in {"", "unknown"}:
                result.add("warnings", f"{oid}: post-cast activity expects hardened surface")
        if "coating" in activity and "wet" in surface:
            result.add("warnings", f"{oid}: post-cast coating should not use wet surface label")
        if congestion == "high" and access == "open":
            note = (row.get("label_revision_note") or row.get("parallel_source_note") or "").strip()
            if not note:
                result.add("warnings", f"{oid}: high congestion conflicts with open access_condition without note")
            else:
                result.add("warnings", f"{oid}: high congestion paired with open access_condition (see note)")
        exposure = (row.get("safety_exposure") or "").lower()
        if exposure == "high" and safety in {"good", "excellent"}:
            note = (row.get("label_revision_note") or row.get("parallel_source_note") or "").strip()
            if not note:
                result.add("warnings", f"{oid}: high safety exposure conflicts with good safety_condition without note")
        if duration_validity == "valid" and confidence == "low":
            result.add("warnings", f"{oid}: low confidence with valid duration")
        if visibility == "low" and confidence == "high":
            result.add("warnings", f"{oid}: low visibility conflicts with high confidence")
        if data_use == "modelling_ready" and confidence == "low":
            result.add("errors", f"{oid}: low-confidence record marked modelling_ready")
        if productivity == "yes":
            result.add("errors", f"{oid}: cleaned row must not be usable_for_productivity=yes")
        if "manufacturer" in source_type:
            result.add("errors", f"{oid}: manufacturer data must not appear in cleaned video dataset")


def validate_activity_labels(
    result: ValidationResult,
    rows: list[dict[str, str]],
    label: str,
    field: str,
    *,
    critical: bool = False,
) -> None:
    groups, legacy = load_activity_taxonomy()
    level = "errors" if critical else "warnings"
    for row in rows:
        raw = (row.get(field) or "").strip()
        if not raw:
            continue
        if resolve_activity_label(raw, groups, legacy) is None:
            rid = row.get("observation_id") or row.get("segment_id") or row.get("video_id") or "?"
            result.add(level, f"{label} {rid}: activity '{raw}' not in activity_taxonomy.yaml")


def validate_mivan_observations(result: ValidationResult, rows: list[dict[str, str]]) -> None:
    for row in rows:
        oid = row.get("observation_id", "?")
        evidence = (row.get("evidence_level") or "").upper()
        source = (row.get("source_type") or "").replace("-", "_")
        if evidence and evidence not in VIDEO_EVIDENCE_LEVELS:
            result.add("errors", f"{oid}: mivan observation must use E1 or E2, got '{evidence}'")
        if source == "manufacturer_reported":
            result.add("errors", f"{oid}: manufacturer_reported must not appear in mivan observations")
        productivity = (row.get("usable_for_productivity") or "").lower()
        if productivity == "yes":
            result.add("errors", f"{oid}: mivan observation must not be usable_for_productivity=yes")
        congestion = (row.get("congestion_level") or "").lower()
        access = (row.get(ACCESS_CONDITION_FIELD) or "").lower()
        exposure = (row.get("safety_exposure") or "").lower()
        safety = (row.get("safety_condition") or "").lower()
        note = (row.get("parallel_source_note") or "").strip()
        if congestion == "high" and access == "open" and not note:
            result.add("warnings", f"{oid}: high congestion conflicts with open access_condition without note")
        if exposure == "high" and safety in {"good", "excellent"} and not note:
            result.add("warnings", f"{oid}: high safety exposure conflicts with good safety_condition without note")
        data_use = (row.get("data_use") or "").lower()
        confidence = (row.get("coding_confidence") or "").lower()
        if data_use == "modelling_ready" and confidence == "low":
            result.add("errors", f"{oid}: low-confidence mivan record marked modelling_ready")


def validate_robot_observations(result: ValidationResult, rows: list[dict[str, str]]) -> None:
    for row in rows:
        oid = row.get("observation_id", "?")
        evidence = (row.get("evidence_level") or "").upper()
        source = (row.get("source_type") or "").replace("-", "_")
        if evidence and evidence not in VIDEO_EVIDENCE_LEVELS:
            if evidence == "E3":
                result.add("errors", f"{oid}: robot video observation must not use E3")
        if source == "manufacturer_reported":
            result.add("errors", f"{oid}: manufacturer_reported must not appear in robot observations")
        verified = (row.get("manufacturer_verified") or "").lower()
        mfr = (row.get("manufacturer_name") or "").lower()
        if verified == "yes" and mfr == "unknown":
            result.add("warnings", f"{oid}: manufacturer_verified=yes but manufacturer_name unknown")


def validate_manufacturer_specs(result: ValidationResult, rows: list[dict[str, str]]) -> None:
    for row in rows:
        sid = row.get("spec_id", "?")
        evidence = (row.get("evidence_level") or "").upper()
        source = (row.get("source_type") or "").replace("-", "_")
        if evidence != "E3":
            result.add("errors", f"{sid}: manufacturer spec must be E3")
        if source and source not in {"manufacturer_reported", ""}:
            result.add("warnings", f"{sid}: expected source_type manufacturer_reported")


def validate_duplicate_controls(result: ValidationResult, rows: list[dict[str, str]], label: str) -> None:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if (row.get("is_duplicate_or_parallel") or "").lower() != "yes":
            continue
        gid = row.get("duplicate_group_id") or ""
        if not gid:
            result.add("warnings", f"{label} {row.get('observation_id') or row.get('video_id')}: duplicate flagged without group id")
            continue
        groups.setdefault(gid, []).append(row)
    for gid, members in groups.items():
        independent = [m for m in members if (m.get("independent_sample") or "").lower() == "yes"]
        if len(independent) > 1:
            result.add("warnings", f"{label} group {gid}: multiple independent_sample=yes")
        if not independent:
            result.add("suggestions", f"{label} group {gid}: consider marking one independent_sample=yes")


def write_reports(result: ValidationResult) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    issues_path = REPORTS_DIR / "validation_issues.csv"
    with issues_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["severity", "message"])
        writer.writeheader()
        for level in ("errors", "warnings", "suggestions"):
            for msg in getattr(result, level):
                writer.writerow({"severity": level[:-1], "message": msg})

    report_path = REPORTS_DIR / "validation_report.md"
    lines = [
        "# Validation Report",
        "",
        "Generated by `src/validate_extractions.py`. Extraction is ongoing; this is not a final sign-off.",
        "",
        f"- **Critical errors:** {len(result.errors)}",
        f"- **Warnings:** {len(result.warnings)}",
        f"- **Suggestions:** {len(result.suggestions)}",
        "",
    ]
    for title, items in (
        ("Critical errors", result.errors),
        ("Warnings", result.warnings),
        ("Suggestions", result.suggestions),
    ):
        lines.append(f"## {title}")
        lines.append("")
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- None")
        lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    result = ValidationResult()
    metadata = read_csv(DATA_DIR / "video_metadata.csv")
    segments = read_csv(DATA_DIR / "video_segments.csv")
    cleaned = read_csv(DATA_DIR / "cleaned_video_dataset.csv")
    robot = read_csv(DATA_DIR / "robot_video_observations.csv")
    mivan = read_csv(DATA_DIR / "mivan_video_observations.csv")
    specs = read_csv(DATA_DIR / "manufacturer_specs.csv")

    check_columns(result, "video_metadata", metadata, REQUIRED_METADATA_COLS)
    check_columns(result, "video_segments", segments, REQUIRED_SEGMENT_COLS)
    check_columns(result, "cleaned_video_dataset", cleaned, REQUIRED_CLEANED_COLS)

    validate_suitability_scores(result, metadata)
    validate_segments(result, segments)
    validate_activity_labels(result, segments, "segment", "activity_type")
    validate_cleaned_logic(result, cleaned)
    validate_activity_labels(result, cleaned, "cleaned", "activity_type", critical=True)
    validate_robot_observations(result, robot)
    validate_activity_labels(result, robot, "robot", "robot_activity_type", critical=True)
    validate_mivan_observations(result, mivan)
    validate_activity_labels(result, mivan, "mivan", "slab_activity_type", critical=True)
    validate_manufacturer_specs(result, specs)
    validate_duplicate_controls(result, metadata, "video")
    validate_duplicate_controls(result, segments, "segment")
    validate_duplicate_controls(result, robot, "robot")
    validate_duplicate_controls(result, mivan, "mivan")
    validate_duplicate_controls(result, cleaned, "cleaned")

    write_reports(result)

    if result.errors:
        print("Validation failed (critical errors):")
        for err in result.errors:
            print(f"  - {err}")
        print(f"Report: {REPORTS_DIR / 'validation_report.md'}")
        return 1

    print("Validation passed.")
    if result.warnings:
        print(f"Warnings: {len(result.warnings)} (see report)")
    print(f"Report: {REPORTS_DIR / 'validation_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
