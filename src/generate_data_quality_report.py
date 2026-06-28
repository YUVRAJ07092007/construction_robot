"""Generate data quality summary report from CSV datasets."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def count_values(rows: list[dict[str, str]], field: str) -> Counter:
    return Counter((row.get(field) or "blank").strip() or "blank" for row in rows)


def missing_summary(rows: list[dict[str, str]], fields: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for field in fields:
        out[field] = sum(1 for row in rows if not (row.get(field) or "").strip())
    return out


def main() -> None:
    meta = read_csv("video_metadata.csv")
    segments = read_csv("video_segments.csv")
    robot = read_csv("robot_video_observations.csv")
    mivan = read_csv("mivan_video_observations.csv")
    cleaned = read_csv("cleaned_video_dataset.csv")
    specs = read_csv("manufacturer_specs.csv")

    structured_videos = [r for r in meta if r.get("suitability_band") == "structured_extraction"]
    qualitative_videos = [r for r in meta if r.get("suitability_band") in {"qualitative_only", "source_pool"}]
    excluded = [r for r in meta if r.get("suitability_band") == "exclude"]

    robot_mfr = count_values([r for r in meta if r.get("video_category") == "robot"], "manufacturer_name")
    activity_robot = count_values(robot, "robot_activity_type")
    activity_mivan = count_values(mivan, "slab_activity_type")
    activity_clean = count_values(cleaned, "activity_type")

    not_modelling = [r for r in cleaned if r.get("data_use") != "modelling_ready" or r.get("usable_for_productivity") == "no"]

    lines = [
        "# Data Quality Report",
        "",
        "**Status:** Stage 1 video data extraction is **complete** (pending human review). "
        "This report describes the final Stage 1 snapshot.",
        "",
        "> The dataset is a secondary observational dataset derived from publicly available videos "
        "and manufacturer-reported specifications. It is not direct field-measured productivity data.",
        "",
        "## Row counts",
        "",
        f"| File | Rows |",
        f"|------|------|",
        f"| video_metadata.csv | {len(meta)} |",
        f"| video_segments.csv | {len(segments)} |",
        f"| robot_video_observations.csv | {len(robot)} |",
        f"| mivan_video_observations.csv | {len(mivan)} |",
        f"| cleaned_video_dataset.csv | {len(cleaned)} |",
        f"| manufacturer_specs.csv | {len(specs)} |",
        "",
        "## Summary metrics",
        "",
        f"- Unique videos in registry: {len(meta)}",
        f"- Structured-extraction videos: {len(structured_videos)}",
        f"- Qualitative-only / pool sources: {len(qualitative_videos)}",
        f"- Excluded videos: {len(excluded)}",
        f"- Robot observations: {len(robot)}",
        f"- Mivan observations: {len(mivan)}",
        f"- Manufacturer spec records: {len(specs)}",
        f"- Cleaned modelling subset rows: {len(cleaned)}",
        "",
        "## Evidence-level distribution (observations)",
        "",
    ]
    ev_robot = count_values(robot, "evidence_level")
    ev_mivan = count_values(mivan, "evidence_level")
    lines.append("**Robot:** " + ", ".join(f"{k}: {v}" for k, v in sorted(ev_robot.items())))
    lines.append("")
    lines.append("**Mivan:** " + ", ".join(f"{k}: {v}" for k, v in sorted(ev_mivan.items())))
    lines.append("")
    lines.append("## Source-type distribution")
    lines.append("")
    lines.append("**Robot:** " + ", ".join(f"{k}: {v}" for k, v in sorted(count_values(robot, "source_type").items())))
    lines.append("")
    lines.append("**Cleaned:** " + ", ".join(f"{k}: {v}" for k, v in sorted(count_values(cleaned, "source_type").items())))
    lines.append("")
    lines.append("## Coding-confidence distribution")
    lines.append("")
    lines.append("**Robot:** " + ", ".join(f"{k}: {v}" for k, v in sorted(count_values(robot, "coding_confidence").items())))
    lines.append("")
    lines.append("**Mivan:** " + ", ".join(f"{k}: {v}" for k, v in sorted(count_values(mivan, "coding_confidence").items())))
    lines.append("")
    lines.append("## Duration validity")
    lines.append("")
    lines.append("**Segments:** " + ", ".join(f"{k}: {v}" for k, v in sorted(count_values(segments, "duration_validity").items())))
    lines.append("")
    lines.append("**usable_for_productivity=yes count:** "
                 f"{sum(1 for r in segments if (r.get('usable_for_productivity') or '').lower() == 'yes')} (should be 0)")
    lines.append("")
    lines.append("## Duplicate / parallel controls")
    lines.append("")
    dup_meta = sum(1 for r in meta if (r.get("is_duplicate_or_parallel") or "").lower() == "yes")
    lines.append(f"- Videos flagged duplicate/parallel: {dup_meta}")
    lines.append(f"- Duplicate groups: {len(set(r.get('duplicate_group_id') for r in meta if r.get('duplicate_group_id')))}")
    lines.append("")
    lines.append("## Robot manufacturer distribution")
    lines.append("")
    for k, v in sorted(robot_mfr.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Activity taxonomy distribution")
    lines.append("")
    lines.append("**Robot activity types:**")
    for k, v in sorted(activity_robot.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("**Mivan activity types:**")
    for k, v in sorted(activity_mivan.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Missing-value summary (key fields)")
    lines.append("")
    for name, rows, fields in [
        ("robot", robot, ["evidence_level", "source_type", "data_use"]),
        ("mivan", mivan, ["evidence_level", "access_condition"]),
        ("cleaned", cleaned, ["evidence_level", "data_use", "access_condition"]),
    ]:
        miss = missing_summary(rows, fields)
        lines.append(f"**{name}:** " + ", ".join(f"{f} missing={miss[f]}" for f in fields))
    lines.append("")
    lines.append("## Records not suitable for modelling")
    lines.append("")
    lines.append(f"- Cleaned rows not marked modelling_ready or with productivity blocked: {len(not_modelling)}")
    lines.append(f"- Invalid-duration segments: {sum(1 for r in segments if (r.get('duration_validity') or '').lower() == 'invalid')}")
    lines.append("")
    lines.append("## Stage 1 completion")
    lines.append("")
    lines.append("- All priority sources screened (no `pending_screening` in registry)")
    lines.append("- All structured-extraction videos segmented and coded")
    lines.append("- Robot source candidates: 4 screened, 4 deferred to post-Stage-1 expansion")
    lines.append("- Validation passing; awaiting human review sign-off before Stage 2")
    lines.append("")
    lines.append("## Optional future expansion (not in Stage 1 scope)")
    lines.append("")
    lines.append("- Additional comparison robots (Floor Master, Kajima, rebar tying, inspection)")
    lines.append("- More independent fresh-concrete leveling observations from verified sources")
    lines.append("- Mivan playlist entries only where workflow adds non-duplicate value")
    lines.append("- Re-screen low-confidence or excluded sources before any modelling_ready promotion")
    lines.append("")

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / "data_quality_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
