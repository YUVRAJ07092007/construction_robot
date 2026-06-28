"""Add robot-agnostic metadata, duplicate controls, and duration-validity fields."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

BAND_TO_DATA_USE = {
    "exclude": "exclude",
    "qualitative_only": "qualitative_only",
    "structured_extraction": "structured_coding",
    "source_pool": "qualitative_only",
    "manufacturer_reported_E3": "structured_coding",
}

ROBOT_META = {
    "R02": ("BrightMaster", "BrightMaster", "unknown", "concrete_leveling_robot", "fresh_concrete_leveling", "yes", "no"),
    "R04": ("BrightMaster", "BrightMaster", "unknown", "concrete_leveling_robot", "robot_transport_setup", "yes", "no"),
    "R05": ("BrightMaster", "BrightMaster", "unknown", "coating_robot", "post_cast_coating", "yes", "no"),
    "R06": ("BrightMaster", "BrightMaster", "unknown", "floor_grinding_robot", "post_cast_floor_grinding", "yes", "no"),
    "R07": ("BrightMaster", "BrightMaster", "NP320", "coating_robot", "post_cast_coating", "yes", "no"),
    "R08": ("BrightMaster", "BrightMaster", "unknown", "other", "other", "yes", "no"),
    "R09": ("BrightMaster", "BrightMaster", "unknown", "concrete_leveling_robot", "fresh_concrete_leveling", "yes", "no"),
    "R10": ("BrightMaster", "BrightMaster", "unknown", "floor_grinding_robot", "post_cast_floor_grinding", "yes", "no"),
    "R11": ("BrightMaster", "BrightMaster", "unknown", "floor_grinding_robot", "post_cast_floor_grinding", "yes", "no"),
    "R12": ("BrightMaster", "BrightMaster", "unknown", "floor_grinding_robot", "post_cast_floor_grinding", "yes", "no"),
    "R13": ("BrightMaster", "BrightMaster", "NP320pro", "coating_robot", "post_cast_coating", "yes", "no"),
    "R14": ("BrightMaster", "BrightMaster", "unknown", "coating_robot", "post_cast_coating", "yes", "no"),
    "R15": ("BrightMaster", "BrightMaster", "unknown", "layout_robot", "layout_marking", "yes", "no"),
    "R16": ("BrightMaster", "BrightMaster", "unknown", "other", "other", "yes", "no"),
    "R17": ("BrightMaster", "BrightMaster", "unknown", "other", "other", "yes", "no"),
    "R18": ("BrightMaster", "BrightMaster", "unknown", "other", "other", "yes", "no"),
    "R19": ("BrightMaster", "BrightMaster", "unknown", "other", "other", "yes", "no"),
    "R20": ("BrightMaster", "BrightMaster", "unknown", "other", "other", "yes", "no"),
    "R21": ("BrightMaster", "BrightMaster", "unknown", "other", "other", "yes", "no"),
    "R03": ("unknown", "unknown", "unknown", "concrete_finishing_robot", "fresh_concrete_finishing", "no", "yes"),
}

DUPLICATE_VIDEO = {
    "M01": ("yes", "DUP-MIVAN-SLAB-7DAY", "yes", "Primary DND slab-cycle documentary"),
    "M05": ("yes", "DUP-MIVAN-SLAB-7DAY", "no", "Parallel Civil Construct upload of M01 workflow"),
    "R07": ("yes", "DUP-BMR-NP320-COATING", "yes", "Primary NP320 indoor coating demo"),
    "R13": ("yes", "DUP-BMR-NP320-COATING", "no", "NP320pro variant; cross-check only"),
}

ACTIVITY_REVISIONS = {
    "concrete_finishing": ("post_cast_coating", "Indoor coating on hardened surface; not fresh concrete"),
    "coating_finishing": ("post_cast_coating", "Post-cast coating activity separated from fresh concrete finishing"),
}


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def extend_fields(fields: list[str], extra: list[str]) -> list[str]:
    out = list(fields)
    for col in extra:
        if col not in out:
            out.append(col)
    return out


def band_data_use(row: dict) -> str:
    band = (row.get("suitability_band") or "").strip()
    override = (row.get("manual_data_use_override") or "").strip()
    if override:
        return override
    return BAND_TO_DATA_USE.get(band, "qualitative_only")


def main() -> None:
    meta_fields, meta_rows = read_csv(DATA / "video_metadata.csv")
    meta_extra = [
        "manufacturer_name",
        "robot_brand",
        "robot_model",
        "robot_category",
        "robot_activity_group",
        "manufacturer_verified",
        "comparison_robot",
        "suitability_score",
        "data_use",
        "manual_data_use_override",
        "override_reason",
        "is_duplicate_or_parallel",
        "duplicate_group_id",
        "independent_sample",
        "parallel_source_note",
    ]
    meta_fields = extend_fields(meta_fields, meta_extra)
    for row in meta_rows:
        vid = row["video_id"]
        if vid in ROBOT_META:
            vals = ROBOT_META[vid]
            row.update(
                dict(
                    zip(
                        [
                            "manufacturer_name",
                            "robot_brand",
                            "robot_model",
                            "robot_category",
                            "robot_activity_group",
                            "manufacturer_verified",
                            "comparison_robot",
                        ],
                        vals,
                    )
                )
            )
        elif row.get("video_category") == "technical_spec":
            row.update(
                {
                    "manufacturer_name": "BrightMaster",
                    "robot_brand": "BrightMaster",
                    "robot_model": "unknown",
                    "robot_category": "other",
                    "robot_activity_group": row.get("activity_focus", "unknown"),
                    "manufacturer_verified": "yes",
                    "comparison_robot": "no",
                }
            )
        else:
            row.update(
                {
                    "manufacturer_name": "unknown",
                    "robot_brand": "unknown",
                    "robot_model": "unknown",
                    "robot_category": "unknown",
                    "robot_activity_group": "unknown",
                    "manufacturer_verified": "unknown",
                    "comparison_robot": "no",
                }
            )
        score = (row.get("suitability_total_score") or "").strip()
        row["suitability_score"] = score if score and score.lower() not in {"n/a", "na"} else ""
        row["data_use"] = band_data_use(row)
        dup = DUPLICATE_VIDEO.get(vid)
        if dup:
            row["is_duplicate_or_parallel"], row["duplicate_group_id"], row["independent_sample"], row["parallel_source_note"] = dup
        else:
            row.setdefault("is_duplicate_or_parallel", "no")
            row.setdefault("duplicate_group_id", "")
            row.setdefault("independent_sample", "yes" if row.get("data_use") == "structured_coding" else "")
            row.setdefault("parallel_source_note", "")
    write_csv(DATA / "video_metadata.csv", meta_fields, meta_rows)

    seg_fields, seg_rows = read_csv(DATA / "video_segments.csv")
    seg_extra = [
        "visible_segment_duration_sec",
        "duration_validity_reason",
        "continuous_unedited_segment",
        "time_lapse_or_jump_cut",
        "usable_for_productivity",
    ]
    seg_fields = extend_fields(seg_fields, seg_extra)
    for row in seg_rows:
        dur = row.get("segment_duration_sec", "")
        row["visible_segment_duration_sec"] = dur
        reason = row.get("reason_for_rejection", "")
        row["duration_validity_reason"] = reason
        invalid = (row.get("duration_validity") or "").lower() == "invalid"
        row["continuous_unedited_segment"] = "no" if invalid else "yes"
        row["time_lapse_or_jump_cut"] = "yes" if invalid else "no"
        row["usable_for_productivity"] = "no"
        act = row.get("activity_type", "")
        if act in ACTIVITY_REVISIONS:
            new_act, note = ACTIVITY_REVISIONS[act]
            row["activity_type"] = new_act
            row["label_revision_note"] = note
    if "label_revision_note" not in seg_fields:
        seg_fields.append("label_revision_note")
    write_csv(DATA / "video_segments.csv", seg_fields, seg_rows)

    robot_fields, robot_rows = read_csv(DATA / "robot_video_observations.csv")
    robot_extra = [
        "manufacturer_name",
        "robot_brand",
        "robot_model",
        "robot_category",
        "robot_activity_group",
        "manufacturer_verified",
        "comparison_robot",
        "source_type",
        "data_use",
        "label_revision_note",
        "visible_segment_duration_sec",
        "duration_validity_reason",
        "usable_for_productivity",
        "is_duplicate_or_parallel",
        "duplicate_group_id",
        "independent_sample",
    ]
    robot_fields = extend_fields(robot_fields, robot_extra)
    for row in robot_rows:
        vid = row["video_id"]
        if vid in ROBOT_META:
            vals = ROBOT_META[vid]
            row.update(dict(zip(robot_extra[:7], vals)))
        act = row.get("robot_activity_type", "")
        if act in ACTIVITY_REVISIONS:
            new_act, note = ACTIVITY_REVISIONS[act]
            row["robot_activity_type"] = new_act
            row["label_revision_note"] = note
        elif act == "concrete_leveling":
            row["robot_activity_group"] = "fresh_concrete_leveling"
        elif act == "floor_grinding":
            row["robot_activity_group"] = "post_cast_floor_grinding"
        elif act == "layout_marking":
            row["robot_activity_group"] = "layout_marking"
        row["source_type"] = "video_estimated" if row.get("evidence_level") == "E2" else "video_observed"
        row["data_use"] = "structured_coding"
        row["visible_segment_duration_sec"] = row.get("task_duration_observed", "")
        row["duration_validity_reason"] = "promotional or edited demo; not productivity time"
        row["usable_for_productivity"] = "no"
        dup = DUPLICATE_VIDEO.get(vid)
        if dup:
            row["is_duplicate_or_parallel"], row["duplicate_group_id"], row["independent_sample"], _ = dup
        else:
            row["is_duplicate_or_parallel"] = "no"
            row["duplicate_group_id"] = ""
            row["independent_sample"] = "yes"
    write_csv(DATA / "robot_video_observations.csv", robot_fields, robot_rows)

    mivan_fields, mivan_rows = read_csv(DATA / "mivan_video_observations.csv")
    mivan_extra = [
        "source_type",
        "data_use",
        "visible_segment_duration_sec",
        "duration_validity_reason",
        "usable_for_productivity",
        "is_duplicate_or_parallel",
        "duplicate_group_id",
        "independent_sample",
        "parallel_source_note",
    ]
    mivan_fields = extend_fields(mivan_fields, mivan_extra)
    for row in mivan_rows:
        vid = row["video_id"]
        row["source_type"] = "video_estimated" if row.get("evidence_level") == "E2" else "video_observed"
        row["data_use"] = "structured_coding"
        row["visible_segment_duration_sec"] = row.get("task_duration_observed", "")
        row["duration_validity_reason"] = "edited or narrated footage; visible duration only"
        row["usable_for_productivity"] = "no"
        dup = DUPLICATE_VIDEO.get(vid)
        if dup:
            row["is_duplicate_or_parallel"], row["duplicate_group_id"], row["independent_sample"], row["parallel_source_note"] = dup
        else:
            row["is_duplicate_or_parallel"] = "no"
            row["duplicate_group_id"] = ""
            row["independent_sample"] = "yes"
            row["parallel_source_note"] = ""
    write_csv(DATA / "mivan_video_observations.csv", mivan_fields, mivan_rows)

    clean_fields, clean_rows = read_csv(DATA / "cleaned_video_dataset.csv")
    clean_extra = [
        "data_use",
        "visible_segment_duration_sec",
        "duration_validity_reason",
        "usable_for_productivity",
        "is_duplicate_or_parallel",
        "duplicate_group_id",
        "independent_sample",
        "label_revision_note",
        "manufacturer_name",
        "robot_category",
    ]
    clean_fields = extend_fields(clean_fields, clean_extra)
    for row in clean_rows:
        act = row.get("activity_type", "")
        if act in ACTIVITY_REVISIONS:
            new_act, note = ACTIVITY_REVISIONS[act]
            row["activity_type"] = new_act
            row["label_revision_note"] = note
        row["data_use"] = "structured_coding"
        if row.get("coding_confidence") == "low":
            row["data_use"] = "qualitative_only"
        row["visible_segment_duration_sec"] = row.get("task_duration_observed", "")
        row["duration_validity_reason"] = "public video segment; not verified productivity duration"
        row["usable_for_productivity"] = "no"
        vid = row["video_id"]
        dup = DUPLICATE_VIDEO.get(vid)
        if dup:
            row["is_duplicate_or_parallel"], row["duplicate_group_id"], row["independent_sample"], _ = dup
        else:
            row["is_duplicate_or_parallel"] = "no"
            row["duplicate_group_id"] = ""
            row["independent_sample"] = "yes"
        if row.get("video_category") == "robot":
            meta = ROBOT_META.get(vid)
            if meta:
                row["manufacturer_name"] = meta[0]
                row["robot_category"] = meta[3]
        else:
            row["manufacturer_name"] = "unknown"
            row["robot_category"] = ""
    write_csv(DATA / "cleaned_video_dataset.csv", clean_fields, clean_rows)

    spec_fields, spec_rows = read_csv(DATA / "manufacturer_specs.csv")
    spec_extra = [
        "manufacturer_name",
        "robot_brand",
        "robot_model",
        "robot_category",
        "source_type",
        "data_use",
        "manufacturer_verified",
    ]
    spec_fields = extend_fields(spec_fields, spec_extra)
    for row in spec_rows:
        row.update(
            {
                "manufacturer_name": "BrightMaster",
                "robot_brand": "BrightMaster",
                "robot_model": "unknown",
                "robot_category": row.get("robot_or_process", "other"),
                "source_type": "manufacturer_reported",
                "data_use": "structured_coding",
                "manufacturer_verified": "yes",
            }
        )
    write_csv(DATA / "manufacturer_specs.csv", spec_fields, spec_rows)

    print("Schema enhancements applied.")


if __name__ == "__main__":
    main()
