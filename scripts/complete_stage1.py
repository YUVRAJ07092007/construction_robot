"""Complete Stage 1: screen remaining sources and code structured-extraction videos."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ACCESS = date.today().isoformat()
INVALID_PROMO = "promotional or edited demo footage; timing for workflow reference only"
INVALID_SHORT = "below minimum segment duration; exclude from structured coding"


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def meta_row(
    vid: str,
    url: str,
    title: str,
    activity: str,
    context: str,
    duration: str,
    vis: str,
    conf: str,
    status: str,
    scores: tuple[str, ...],
    total: str,
    band: str,
    notes: str,
) -> dict:
    return {
        "video_id": vid,
        "video_url": url,
        "video_category": "robot",
        "platform": "YouTube",
        "title": title,
        "source_name": "Brightmasterrobotics_BMR",
        "access_date": ACCESS,
        "activity_focus": activity,
        "construction_context": context,
        "total_video_duration": duration,
        "visibility_quality": vis,
        "coding_confidence": conf,
        "inclusion_status": status,
        "score_relevance": scores[0],
        "score_visual_clarity": scores[1],
        "score_activity_continuity": scores[2],
        "score_activity_identifiability": scores[3],
        "score_interaction_visibility": scores[4],
        "score_editing_level": scores[5],
        "score_parameter_measurability": scores[6],
        "suitability_total_score": total,
        "suitability_band": band,
        "notes": notes,
    }


def main() -> None:
    meta_fields, meta_rows = read_csv(DATA / "video_metadata.csv")

    # R04 Facebook screening
    for row in meta_rows:
        if row["video_id"] == "R04":
            row.update(
                {
                    "total_video_duration": "unknown",
                    "visibility_quality": "medium",
                    "coding_confidence": "medium",
                    "inclusion_status": "qualitative_only",
                    "score_relevance": "2",
                    "score_visual_clarity": "1",
                    "score_activity_continuity": "1",
                    "score_activity_identifiability": "2",
                    "score_interaction_visibility": "1",
                    "score_editing_level": "1",
                    "score_parameter_measurability": "1",
                    "suitability_total_score": "9",
                    "suitability_band": "qualitative_only",
                    "notes": (
                        "Facebook supplementary source; transport/lifting/leveling logistics; "
                        "less stable citation than YouTube; no structured segment coding"
                    ),
                }
            )
        if row["video_id"] == "R01":
            row["notes"] = (
                "17 channel videos catalogued; R02 and R05-R21 individually screened "
                "(structured: R09-R13,R15; qualitative: R04,R14,R16-R20; exclude: R21)"
            )
        if row["video_id"] == "M04":
            row["notes"] = (
                "8-video playlist screened; M06 added from pool; remaining entries overlap M01/M02/M05"
            )

    new_meta = [
        meta_row(
            "R09",
            "https://www.youtube.com/watch?v=YXiwIc6AH4Y",
            "03【BMR】Concrete Leveling Robot 地面整平机器人",
            "concrete_leveling",
            "open_slab",
            "79",
            "high",
            "medium",
            "include",
            ("2", "2", "2", "2", "1", "1", "2"),
            "12",
            "structured_extraction",
            "Official BrightMaster fresh-concrete leveling demo",
        ),
        meta_row(
            "R10",
            "https://www.youtube.com/watch?v=blDA7WRcL0I",
            "01【BMR】Floor Grinding Robot 地坪研磨机器人",
            "floor_grinding",
            "indoor_floor",
            "79",
            "high",
            "medium",
            "include",
            ("2", "2", "2", "2", "1", "1", "2"),
            "12",
            "structured_extraction",
            "Official BrightMaster floor grinding demo; post-cast surface",
        ),
        meta_row(
            "R11",
            "https://www.youtube.com/watch?v=eJ13b9CT8io",
            "02-Interior Concrete Wall Grinding Robot",
            "floor_grinding,wall_surface",
            "indoor_wall",
            "90",
            "high",
            "medium",
            "include",
            ("2", "2", "2", "2", "1", "1", "1"),
            "11",
            "structured_extraction",
            "Interior wall grinding robot; post-cast hardened surface",
        ),
        meta_row(
            "R12",
            "https://www.youtube.com/watch?v=6y8Fz8oBIYE",
            "01-Interior Concrete Ceiling Grinding Robot",
            "floor_grinding,ceiling_surface",
            "indoor_ceiling",
            "64",
            "high",
            "medium",
            "include",
            ("2", "2", "2", "2", "1", "1", "1"),
            "11",
            "structured_extraction",
            "Ceiling grinding robot; overhead post-cast surface prep",
        ),
        meta_row(
            "R13",
            "https://www.youtube.com/watch?v=hYF0dL1tfVQ",
            "04-indoor coating robot NP320pro",
            "coating,finishing",
            "indoor_floor",
            "158",
            "high",
            "medium",
            "include",
            ("2", "2", "2", "2", "1", "1", "1"),
            "11",
            "structured_extraction",
            "NP320pro indoor coating; parallel variant to R07",
        ),
        meta_row(
            "R14",
            "https://www.youtube.com/watch?v=BDlcgA2LoN8",
            "07-Exterior Wal Coating Robot",
            "coating,exterior_wall",
            "exterior_facade",
            "123",
            "medium",
            "low",
            "qualitative_only",
            ("2", "1", "1", "2", "1", "1", "1"),
            "9",
            "qualitative_only",
            "Exterior wall coating promo; qualitative workflow mapping only",
        ),
        meta_row(
            "R15",
            "https://www.youtube.com/watch?v=xKegkxzEOr0",
            "【BMR】Measuring Robot 测量机器人",
            "layout_marking,measurement",
            "indoor_slab",
            "94",
            "high",
            "medium",
            "include",
            ("2", "2", "2", "2", "1", "1", "1"),
            "11",
            "structured_extraction",
            "Layout/measurement robot demo; supports pre-pour layout context",
        ),
        meta_row(
            "R16",
            "https://www.youtube.com/watch?v=gLkFvaStjzA",
            "Immersive experience: how robots work in construction site?",
            "multi_robot,montage",
            "mixed_site",
            "52",
            "medium",
            "low",
            "qualitative_only",
            ("2", "1", "1", "1", "0", "0", "1"),
            "6",
            "qualitative_only",
            "Edited montage; workflow context only",
        ),
        meta_row(
            "R17",
            "https://www.youtube.com/watch?v=LrG7mUlH1y0",
            "Witness future of construction in 90 Seconds I 2026 BrightMaster Innovation Launch",
            "promotional,product_launch",
            "event",
            "114",
            "medium",
            "low",
            "qualitative_only",
            ("1", "1", "0", "1", "0", "0", "1"),
            "4",
            "exclude",
            "Launch promo montage; excluded from coding",
        ),
        meta_row(
            "R18",
            "https://www.youtube.com/watch?v=DYN9N7-7ZGE",
            "About BrightMaster Robotics products",
            "product_overview",
            "promotional",
            "103",
            "medium",
            "low",
            "qualitative_only",
            ("2", "1", "1", "1", "0", "1", "1"),
            "7",
            "qualitative_only",
            "Product taxonomy overview; no structured segment coding",
        ),
        meta_row(
            "R19",
            "https://www.youtube.com/watch?v=HDSjL2hw7dU",
            "Who has the most complete product line of construction robots?",
            "product_overview",
            "promotional",
            "103",
            "medium",
            "low",
            "qualitative_only",
            ("1", "1", "1", "1", "0", "1", "1"),
            "6",
            "qualitative_only",
            "Marketing comparison reel; qualitative only",
        ),
        meta_row(
            "R20",
            "https://www.youtube.com/watch?v=RoIMb8TKrvg",
            "The Construction Crisis: low Profit, Aging Workers, Safety Risks",
            "industry_overview,promotional",
            "presentation",
            "1971",
            "medium",
            "low",
            "qualitative_only",
            ("1", "1", "1", "1", "0", "0", "1"),
            "5",
            "exclude",
            "Long promotional presentation; excluded from structured coding",
        ),
        meta_row(
            "R21",
            "https://www.youtube.com/watch?v=FcXXe9oKcts",
            "Behind the Scenes: 2026 BrightMaster Embodied Construction Robot Innovation Launch",
            "event_highlights",
            "event",
            "32",
            "low",
            "low",
            "exclude",
            ("1", "1", "0", "1", "0", "0", "0"),
            "3",
            "exclude",
            "32s highlight reel; below usability threshold",
        ),
        {
            "video_id": "M06",
            "video_url": "https://www.youtube.com/watch?v=CAI35CJ62kw",
            "video_category": "mivan",
            "platform": "YouTube",
            "title": "MIVAN Formwork l Finishing work l High Rise Building",
            "source_name": "Civil Construct",
            "access_date": ACCESS,
            "activity_focus": "finishing,post_cast,formwork_stripping",
            "construction_context": "high-rise",
            "total_video_duration": "415",
            "visibility_quality": "medium",
            "coding_confidence": "medium",
            "inclusion_status": "include",
            "score_relevance": "2",
            "score_visual_clarity": "2",
            "score_activity_continuity": "1",
            "score_activity_identifiability": "2",
            "score_interaction_visibility": "1",
            "score_editing_level": "1",
            "score_parameter_measurability": "1",
            "suitability_total_score": "10",
            "suitability_band": "structured_extraction",
            "notes": "From M04 playlist pool; post-cast finishing context for Mivan workflow",
        },
    ]
    meta_rows.extend(new_meta)
    write_csv(DATA / "video_metadata.csv", meta_fields, meta_rows)

    _, seg_rows = read_csv(DATA / "video_segments.csv")
    seg_template = {
        "segment_category": "robot_operation",
        "segment_quality": "high",
        "duration_validity": "invalid",
        "reason_for_rejection": INVALID_PROMO,
    }
    robot_segments = [
        ("R09-S01", "R09", "00:00:00", "00:01:19", 79, "concrete_leveling"),
        ("R10-S01", "R10", "00:00:00", "00:01:19", 79, "floor_grinding"),
        ("R11-S01", "R11", "00:00:00", "00:01:30", 90, "floor_grinding"),
        ("R12-S01", "R12", "00:00:00", "00:01:04", 64, "floor_grinding"),
        ("R13-S01", "R13", "00:00:00", "00:02:38", 158, "post_cast_coating"),
        ("R15-S01", "R15", "00:00:00", "00:01:34", 94, "layout_marking"),
    ]
    for sid, vid, start, end, dur, act in robot_segments:
        seg_rows.append(
            {
                "segment_id": sid,
                "video_id": vid,
                "start_time": start,
                "end_time": end,
                "segment_duration_sec": str(dur),
                "activity_type": act,
                **seg_template,
            }
        )
    seg_rows.append(
        {
            "segment_id": "M06-S01",
            "video_id": "M06",
            "start_time": "00:00:30",
            "end_time": "00:04:30",
            "segment_duration_sec": "240",
            "activity_type": "post_cast_finishing",
            "segment_category": "mivan_workflow",
            "segment_quality": "medium",
            "duration_validity": "invalid",
            "reason_for_rejection": INVALID_PROMO,
        }
    )
    write_csv(DATA / "video_segments.csv", list(seg_rows[0].keys()), seg_rows)

    _, robot_rows = read_csv(DATA / "robot_video_observations.csv")
    robot_obs = [
        ("OBS-R09-001", "R09", "R09-S01", "concrete_leveling", "wet_concrete", "linear", "remote_control", 79),
        ("OBS-R10-001", "R10", "R10-S01", "floor_grinding", "hardened_concrete", "grid-based", "autonomous", 79),
        ("OBS-R11-001", "R11", "R11-S01", "floor_grinding", "hardened_concrete", "vertical_scan", "autonomous", 90),
        ("OBS-R12-001", "R12", "R12-S01", "floor_grinding", "hardened_concrete", "overhead_scan", "autonomous", 64),
        ("OBS-R13-001", "R13", "R13-S01", "post_cast_coating", "hardened_concrete", "grid-based", "autonomous", 158),
        ("OBS-R15-001", "R15", "R15-S01", "layout_marking", "pre_pour_slab", "point_to_point", "autonomous", 94),
    ]
    for oid, vid, sid, act, surface, move, guide, dur in robot_obs:
        robot_rows.append(
            {
                "observation_id": oid,
                "video_id": vid,
                "segment_id": sid,
                "robot_activity_type": act,
                "operating_surface": surface,
                "movement_pattern": move,
                "guidance_mode": guide,
                "operator_count_visible": "0" if "leveling" not in act else "1",
                "assistant_count_visible": "0",
                "setup_visible": "no",
                "setup_complexity": "unknown",
                "operational_continuity": "continuous",
                "interruption_count": "0",
                "obstacle_presence": "no",
                "human_robot_separation": "high",
                "safety_condition": "good",
                "edge_condition": "not_visible",
                "robot_transport_requirement": "unknown",
                "task_duration_observed": str(dur),
                "duration_validity": "invalid",
                "evidence_level": "E2",
                "coding_confidence": "medium",
            }
        )
    write_csv(DATA / "robot_video_observations.csv", list(robot_rows[0].keys()), robot_rows)

    _, mivan_rows = read_csv(DATA / "mivan_video_observations.csv")
    mivan_rows.append(
        {
            "observation_id": "OBS-M06-001",
            "video_id": "M06",
            "segment_id": "M06-S01",
            "slab_activity_type": "finishing",
            "floor_cycle_stage": "post-cast",
            "labour_count_visible": "4",
            "min_visible_labour": "3",
            "max_visible_labour": "6",
            "dominant_visible_labour": "4",
            "congestion_level": "medium",
            "reinforcement_complexity": "low",
            "conduit_presence": "unknown",
            "slab_opening_presence": "unknown",
            "access_condition": "partially_restricted",
            "material_movement_method": "manual",
            "pour_sequence": "unknown",
            "surface_condition": "hardened_concrete",
            "safety_exposure": "medium",
            "edge_protection_visible": "unknown",
            "workflow_sequence": "stripping>surface_prep>finishing",
            "task_duration_observed": "240",
            "duration_validity": "invalid",
            "evidence_level": "E2",
            "coding_confidence": "medium",
        }
    )
    write_csv(DATA / "mivan_video_observations.csv", list(mivan_rows[0].keys()), mivan_rows)

    _, cleaned_rows = read_csv(DATA / "cleaned_video_dataset.csv")
    cleaned_add = [
        ("OBS-R09-001", "R09", "R09-S01", "robot", "concrete_leveling", "pour", "", "1", "linear", "wet_concrete"),
        ("OBS-R10-001", "R10", "R10-S01", "robot", "floor_grinding", "post-cast", "", "0", "grid-based", "hardened_concrete"),
        ("OBS-R15-001", "R15", "R15-S01", "robot", "layout_marking", "pre-pour", "", "0", "point_to_point", "pre_pour_slab"),
        ("OBS-M06-001", "M06", "M06-S01", "mivan", "post_cast_finishing", "post-cast", "4", "", "", ""),
    ]
    for oid, vid, sid, cat, act, stage, labour, rop, move, surface in cleaned_add:
        cleaned_rows.append(
            {
                "observation_id": oid,
                "video_id": vid,
                "segment_id": sid,
                "video_category": cat,
                "activity_type": act,
                "workflow_stage": stage,
                "labour_count_visible": labour,
                "robot_operator_count": rop,
                "movement_pattern": move,
                "operating_surface": surface,
                "congestion_level": "low" if cat == "robot" else "medium",
                "reinforcement_complexity": "" if cat == "robot" else "low",
                "access_condition": "open" if cat == "robot" else "partially_restricted",
                "safety_condition": "good" if cat == "robot" else "moderate",
                "task_duration_observed": {
                    "R09": "79",
                    "R10": "79",
                    "R15": "94",
                    "M06": "240",
                }.get(vid, ""),
                "duration_validity": "invalid",
                "evidence_level": "E2",
                "coding_confidence": "medium",
                "source_type": "video-estimated",
                "visibility_quality": "high" if cat == "robot" else "medium",
            }
        )
    write_csv(DATA / "cleaned_video_dataset.csv", list(cleaned_rows[0].keys()), cleaned_rows)

    print("Stage 1 completion batch update finished.")


if __name__ == "__main__":
    main()
