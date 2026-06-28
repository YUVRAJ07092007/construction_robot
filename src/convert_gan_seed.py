"""Convert approved Stage 1 cleaned observations into GAN-ready seed records (Stage 2)."""

from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML required for seed conversion") from exc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.validate_extractions import load_activity_taxonomy, read_csv, resolve_activity_label  # noqa: E402

DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
SCHEMA_PATH = ROOT / "config" / "seed_encoding_schema.yaml"
CLEANED_PATH = DATA_DIR / "cleaned_video_dataset.csv"
SEED_PATH = DATA_DIR / "gan_seed_dataset.csv"
ROBOT_PATH = DATA_DIR / "robot_video_observations.csv"

SEED_HEADER = [
    "seed_id",
    "source_observation_id",
    "source_video_id",
    "source_segment_id",
    "video_category",
    "video_category_enc",
    "activity_group",
    "activity_type_raw",
    "workflow_stage",
    "workflow_stage_enc",
    "labour_count_visible",
    "robot_operator_count",
    "movement_pattern",
    "movement_pattern_enc",
    "operating_surface",
    "operating_surface_enc",
    "congestion_level",
    "congestion_level_enc",
    "reinforcement_complexity",
    "reinforcement_complexity_enc",
    "access_condition",
    "access_condition_enc",
    "safety_condition",
    "safety_condition_enc",
    "evidence_level",
    "evidence_level_enc",
    "coding_confidence",
    "coding_confidence_enc",
    "manufacturer_name",
    "manufacturer_name_enc",
    "comparison_robot",
    "comparison_robot_enc",
    "robot_category",
    "independent_sample",
    "duration_excluded",
    "usable_for_productivity",
    "seed_provenance",
    "data_use",
    "seed_conversion_date",
    "exclusion_reason",
]


def load_schema() -> dict:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def encode(mapping: dict, value: str, default: int = 0) -> int:
    raw = (value or "").strip()
    if raw in mapping:
        return int(mapping[raw])
    key = raw.lower()
    if key in mapping:
        return int(mapping[key])
    return int(mapping.get("", default))


def is_eligible(row: dict[str, str], rules: dict) -> tuple[bool, str]:
    if (row.get("independent_sample") or "").lower() != "yes":
        return False, "not_independent_sample"
    if (row.get("is_duplicate_or_parallel") or "").lower() == "yes":
        return False, "duplicate_or_parallel"
    data_use = (row.get("data_use") or "").lower()
    if data_use == "qualitative_only":
        return False, "qualitative_only"
    if data_use not in {v.lower() for v in rules["allowed_data_use"]}:
        return False, f"data_use_{data_use or 'missing'}"
    confidence = (row.get("coding_confidence") or "").lower()
    if confidence not in {v.lower() for v in rules["allowed_coding_confidence"]}:
        return False, f"coding_confidence_{confidence or 'missing'}"
    evidence = (row.get("evidence_level") or "").upper()
    if evidence not in set(rules["allowed_evidence_level"]):
        return False, f"evidence_{evidence or 'missing'}"
    if (row.get("usable_for_productivity") or "").lower() == "yes":
        return False, "usable_for_productivity"
    return True, ""


def build_robot_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["observation_id"]: row for row in rows if row.get("observation_id")}


def convert_row(
    row: dict[str, str],
    seed_index: int,
    schema: dict,
    groups: frozenset[str],
    legacy: dict[str, str],
    robot_lookup: dict[str, dict[str, str]],
    conversion_date: str,
) -> dict[str, str]:
    oid = row["observation_id"]
    activity_raw = (row.get("activity_type") or "").strip()
    activity_group = resolve_activity_label(activity_raw, groups, legacy) or activity_raw

    robot_row = robot_lookup.get(oid, {})
    comparison = (robot_row.get("comparison_robot") or "").lower()
    if row.get("video_category") == "mivan":
        comparison = "na"

    mfr = (row.get("manufacturer_name") or "").strip()
    if row.get("video_category") == "mivan" and not mfr:
        mfr = "none"

    return {
        "seed_id": f"SEED-{seed_index:03d}",
        "source_observation_id": oid,
        "source_video_id": row.get("video_id", ""),
        "source_segment_id": row.get("segment_id", ""),
        "video_category": row.get("video_category", ""),
        "video_category_enc": str(encode(schema["video_category"], row.get("video_category", ""))),
        "activity_group": activity_group,
        "activity_type_raw": activity_raw,
        "workflow_stage": row.get("workflow_stage", ""),
        "workflow_stage_enc": str(encode(schema["workflow_stage"], row.get("workflow_stage", ""))),
        "labour_count_visible": row.get("labour_count_visible", ""),
        "robot_operator_count": row.get("robot_operator_count", ""),
        "movement_pattern": row.get("movement_pattern", ""),
        "movement_pattern_enc": str(encode(schema["movement_pattern"], row.get("movement_pattern", ""))),
        "operating_surface": row.get("operating_surface", ""),
        "operating_surface_enc": str(encode(schema["operating_surface"], row.get("operating_surface", ""))),
        "congestion_level": row.get("congestion_level", ""),
        "congestion_level_enc": str(encode(schema["ordinal_low_medium_high"], row.get("congestion_level", ""))),
        "reinforcement_complexity": row.get("reinforcement_complexity", ""),
        "reinforcement_complexity_enc": str(
            encode(schema["ordinal_low_medium_high"], row.get("reinforcement_complexity", ""))
        ),
        "access_condition": row.get("access_condition", ""),
        "access_condition_enc": str(encode(schema["access_condition"], row.get("access_condition", ""))),
        "safety_condition": row.get("safety_condition", ""),
        "safety_condition_enc": str(encode(schema["safety_condition"], row.get("safety_condition", ""))),
        "evidence_level": row.get("evidence_level", ""),
        "evidence_level_enc": str(encode(schema["evidence_level"], row.get("evidence_level", ""))),
        "coding_confidence": row.get("coding_confidence", ""),
        "coding_confidence_enc": str(encode(schema["coding_confidence"], row.get("coding_confidence", ""))),
        "manufacturer_name": mfr,
        "manufacturer_name_enc": str(encode(schema["manufacturer_name"], mfr)),
        "comparison_robot": comparison,
        "comparison_robot_enc": str(encode(schema["comparison_robot"], comparison)),
        "robot_category": row.get("robot_category", ""),
        "independent_sample": "yes",
        "duration_excluded": "yes",
        "usable_for_productivity": "no",
        "seed_provenance": "video_observed_secondary",
        "data_use": "framework_seed_ready",
        "seed_conversion_date": conversion_date,
        "exclusion_reason": "",
    }


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def update_cleaned_data_use(cleaned_rows: list[dict[str, str]], promoted_ids: set[str]) -> None:
    for row in cleaned_rows:
        oid = row.get("observation_id", "")
        if oid in promoted_ids:
            row["data_use"] = "framework_seed_ready"


def write_conversion_report(
    *,
    total_cleaned: int,
    seed_rows: list[dict[str, str]],
    excluded: list[tuple[str, str]],
    conversion_date: str,
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    mivan = sum(1 for r in seed_rows if r["video_category"] == "mivan")
    robot = sum(1 for r in seed_rows if r["video_category"] == "robot")
    bm = sum(1 for r in seed_rows if r.get("manufacturer_name") == "BrightMaster")
    bd = sum(1 for r in seed_rows if r.get("manufacturer_name") == "Bright Dream")

    lines = [
        "# GAN Seed Conversion Report",
        "",
        f"**Generated:** {conversion_date} by `src/convert_gan_seed.py`",
        "",
        "> Seed records are normalized from approved Stage 1 observations. "
        "They are **not** synthetic GAN outputs and **exclude** video durations as productivity targets.",
        "",
        "## Summary",
        "",
        f"- Cleaned rows reviewed: {total_cleaned}",
        f"- Seed records produced: {len(seed_rows)}",
        f"- Excluded from seed set: {len(excluded)}",
        f"- Mivan seeds: {mivan}",
        f"- Robot seeds: {robot}",
        f"- BrightMaster robot seeds: {bm}",
        f"- Bright Dream comparison seeds: {bd}",
        "",
        "## Promotion rules applied",
        "",
        "- `independent_sample=yes`",
        "- Not flagged duplicate/parallel",
        "- `data_use` structured_coding (promoted to framework_seed_ready)",
        "- `coding_confidence` medium or high",
        "- Evidence E1 or E2 only",
        "- `usable_for_productivity=no` enforced",
        "",
        "## Seed records",
        "",
        "| seed_id | source_observation_id | category | activity_group | workflow_stage |",
        "|---------|----------------------|----------|----------------|----------------|",
    ]
    for row in seed_rows:
        lines.append(
            f"| {row['seed_id']} | {row['source_observation_id']} | {row['video_category']} | "
            f"{row['activity_group']} | {row['workflow_stage']} |"
        )
    lines.extend(["", "## Excluded rows", ""])
    if excluded:
        lines.append("| observation_id | reason |")
        lines.append("|----------------|--------|")
        for oid, reason in excluded:
            lines.append(f"| {oid} | {reason} |")
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Output files",
            "",
            "- `data/gan_seed_dataset.csv` — GAN-ready seed feature table",
            "- `data/cleaned_video_dataset.csv` — promoted rows marked `framework_seed_ready`",
            "",
            "## Research-safe note",
            "",
            "Seed conversion prepares feature vectors for **future** synthetic scenario generation. "
            "No GAN training or synthetic record generation is performed in this step.",
            "",
        ]
    )
    (REPORTS_DIR / "seed_conversion_report.md").write_text("\n".join(lines), encoding="utf-8")


def convert(*, write_cleaned: bool = True) -> dict:
    schema = load_schema()
    rules = schema["seed_promotion_rules"]
    groups, legacy, _context = load_activity_taxonomy()
    cleaned = read_csv(CLEANED_PATH)
    robot = read_csv(ROBOT_PATH)
    robot_lookup = build_robot_lookup(robot)
    conversion_date = date.today().isoformat()

    seed_rows: list[dict[str, str]] = []
    excluded: list[tuple[str, str]] = []
    promoted_ids: set[str] = set()
    seed_index = 1

    for row in cleaned:
        oid = row.get("observation_id", "?")
        ok, reason = is_eligible(row, rules)
        if not ok:
            excluded.append((oid, reason))
            continue
        seed_rows.append(
            convert_row(row, seed_index, schema, groups, legacy, robot_lookup, conversion_date)
        )
        promoted_ids.add(oid)
        seed_index += 1

    write_csv(SEED_PATH, SEED_HEADER, seed_rows)

    if write_cleaned:
        update_cleaned_data_use(cleaned, promoted_ids)
        write_csv(CLEANED_PATH, list(cleaned[0].keys()) if cleaned else [], cleaned)

    write_conversion_report(
        total_cleaned=len(cleaned),
        seed_rows=seed_rows,
        excluded=excluded,
        conversion_date=conversion_date,
    )

    return {
        "seed_count": len(seed_rows),
        "excluded_count": len(excluded),
        "promoted_ids": promoted_ids,
    }


def main() -> int:
    result = convert()
    print(f"Stage 2 seed conversion complete: {result['seed_count']} seeds, {result['excluded_count']} excluded.")
    print(f"Output: {SEED_PATH}")
    print(f"Report: {REPORTS_DIR / 'seed_conversion_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
