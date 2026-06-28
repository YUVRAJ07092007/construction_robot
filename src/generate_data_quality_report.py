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
    seeds = read_csv("gan_seed_dataset.csv")
    synthetic = read_csv("synthetic_scenario_dataset.csv")
    synthetic_gan = read_csv("synthetic_scenario_dataset_gan.csv")
    synthetic_all = read_csv("synthetic_scenario_dataset_all.csv")

    structured_videos = [r for r in meta if r.get("suitability_band") == "structured_extraction"]
    qualitative_videos = [r for r in meta if r.get("suitability_band") in {"qualitative_only", "source_pool"}]
    excluded = [r for r in meta if r.get("suitability_band") == "exclude"]

    robot_mfr = count_values([r for r in meta if r.get("video_category") == "robot"], "manufacturer_name")
    activity_robot = count_values(robot, "robot_activity_type")
    activity_mivan = count_values(mivan, "slab_activity_type")
    activity_clean = count_values(cleaned, "activity_type")

    bm_robot = sum(1 for r in robot if (r.get("manufacturer_name") or "").lower() == "brightmaster")
    non_bm_robot = len(robot) - bm_robot
    data_use_cleaned = count_values(cleaned, "data_use")
    review_rows = [
        r for r in cleaned
        if (r.get("coding_confidence") or "").lower() == "low"
        or (r.get("data_use") or "") == "qualitative_only"
    ]
    framework_seed_ready = [r for r in cleaned if r.get("data_use") == "framework_seed_ready"]
    not_promoted = [r for r in cleaned if r.get("data_use") != "framework_seed_ready"]

    stage2_note = (
        "Stage 2 GAN seed conversion **complete** (2026-06-28)."
        if seeds
        else "Stage 2 GAN seed conversion not yet run."
    )

    lines = [
        "# Data Quality Report",
        "",
        "**Status:** Extraction **ongoing**; pilot/framework demonstration **reviewer_ready_with_limitations**. "
        "See `docs/repository_status_matrix.md`. " + stage2_note,
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
        f"| gan_seed_dataset.csv | {len(seeds)} |",
        f"| synthetic_scenario_dataset.csv | {len(synthetic)} |",
        f"| synthetic_scenario_dataset_gan.csv | {len(synthetic_gan)} |",
        f"| synthetic_scenario_dataset_all.csv | {len(synthetic_all)} |",
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
        f"- GAN seed records: {len(seeds)}",
        f"- Synthetic scenario records (rule): {len(synthetic)}",
        f"- Synthetic scenario records (GAN pilot): {len(synthetic_gan)}",
        f"- Synthetic scenario records (combined): {len(synthetic_all)}",
        f"- Cleaned rows promoted to framework_seed_ready: {len(framework_seed_ready)}",
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
    lines.append("## Robot manufacturer distribution (observations)")
    lines.append("")
    lines.append(f"- BrightMaster: {bm_robot}")
    lines.append(f"- Non-BrightMaster: {non_bm_robot}")
    lines.append("")
    for k, v in sorted(robot_mfr.items()):
        lines.append(f"- {k} (registry): {v}")
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
    lines.append("## Data-use distribution (cleaned)")
    lines.append("")
    for k, v in sorted(data_use_cleaned.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Records requiring review")
    lines.append("")
    lines.append(f"- Low-confidence or qualitative-only cleaned rows: {len(review_rows)}")
    lines.append("")
    lines.append("## Extraction gaps")
    lines.append("")
    lines.append("- More non-BrightMaster robot video coding needed for balanced demonstration")
    lines.append("- Field validation not yet performed")
    lines.append("- Synthetic GAN pilot limited to n=14 training seeds")
    lines.append("")
    lines.append("")
    for name, rows, fields in [
        ("robot", robot, ["evidence_level", "source_type", "data_use"]),
        ("mivan", mivan, ["evidence_level", "access_condition"]),
        ("cleaned", cleaned, ["evidence_level", "data_use", "access_condition"]),
    ]:
        miss = missing_summary(rows, fields)
        lines.append(f"**{name}:** " + ", ".join(f"{f} missing={miss[f]}" for f in fields))
    lines.append("")
    lines.append("## Modelling readiness")
    lines.append("")
    lines.append(f"- framework_seed_ready cleaned rows: {len(framework_seed_ready)}")
    lines.append(f"- Not promoted (structured_coding / qualitative_only): {len(not_promoted)}")
    lines.append(f"- Seed records (independent sample only): {len(seeds)}")
    lines.append(f"- Invalid-duration segments: {sum(1 for r in segments if (r.get('duration_validity') or '').lower() == 'invalid')}")
    lines.append(f"- usable_for_productivity=yes count: {sum(1 for r in segments if (r.get('usable_for_productivity') or '').lower() == 'yes')} (should be 0)")
    lines.append("")
    if seeds:
        lines.append("## GAN seed dataset")
        lines.append("")
        lines.append(f"- Mivan seeds: {sum(1 for r in seeds if r.get('video_category') == 'mivan')}")
        lines.append(f"- Robot seeds: {sum(1 for r in seeds if r.get('video_category') == 'robot')}")
        lines.append(f"- All seeds duration_excluded=yes: {all(r.get('duration_excluded') == 'yes' for r in seeds)}")
        lines.append("")
    if synthetic:
        lines.append("## Synthetic scenario dataset (Phase 3.1)")
        lines.append("")
        lines.append(f"- Rule-expanded scenarios: {len(synthetic)}")
        lines.append(f"- All is_synthetic=yes: {all(r.get('is_synthetic') == 'yes' for r in synthetic)}")
        fam = Counter(r.get("scenario_family", "?") for r in synthetic)
        for k, v in sorted(fam.items()):
            lines.append(f"- {k}: {v}")
        lines.append("")
    lines.append("## Stage completion")
    lines.append("")
    lines.append("- Stage 1 sign-off: `docs/stage1_signoff.md`")
    if seeds:
        lines.append("- Stage 2 seed conversion: `docs/stage2_signoff.md`")
    if synthetic:
        lines.append("- Phase 3.1 rule expansion: `reports/synthetic_expansion_report.md`")
    else:
        lines.append("- Phase 3.1 rule expansion: not started")
    if synthetic_gan:
        lines.append("- Phase 3B tabular GAN pilot: `reports/tabular_gan_pilot_report.md`")
    else:
        lines.append("- Phase 3B tabular GAN pilot: not started")
    lines.append("- Robot source candidates: 4 deferred to optional expansion")
    lines.append("")
    lines.append("## Optional future expansion")
    lines.append("")
    lines.append("- Additional comparison robots (Floor Master, Kajima, rebar tying, inspection)")
    lines.append("- Field validation before quantitative deployment-readiness claims")
    lines.append("")

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / "data_quality_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
