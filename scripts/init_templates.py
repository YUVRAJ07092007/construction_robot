"""Write empty CSV templates with standard headers."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLATES = DATA / "templates"

HEADERS = {
    "video_metadata.csv": [
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
        "score_relevance",
        "score_visual_clarity",
        "score_activity_continuity",
        "score_activity_identifiability",
        "score_interaction_visibility",
        "score_editing_level",
        "score_parameter_measurability",
        "suitability_total_score",
        "suitability_band",
        "notes",
    ],
    "video_segments.csv": [
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
    ],
    "robot_video_observations.csv": [
        "observation_id",
        "video_id",
        "segment_id",
        "robot_activity_type",
        "operating_surface",
        "movement_pattern",
        "guidance_mode",
        "operator_count_visible",
        "assistant_count_visible",
        "setup_visible",
        "setup_complexity",
        "operational_continuity",
        "interruption_count",
        "obstacle_presence",
        "human_robot_separation",
        "safety_condition",
        "edge_condition",
        "robot_transport_requirement",
        "task_duration_observed",
        "duration_validity",
        "evidence_level",
        "coding_confidence",
    ],
    "mivan_video_observations.csv": [
        "observation_id",
        "video_id",
        "segment_id",
        "slab_activity_type",
        "floor_cycle_stage",
        "labour_count_visible",
        "min_visible_labour",
        "max_visible_labour",
        "dominant_visible_labour",
        "congestion_level",
        "reinforcement_complexity",
        "conduit_presence",
        "slab_opening_presence",
        "access_condition",
        "material_movement_method",
        "pour_sequence",
        "surface_condition",
        "safety_exposure",
        "edge_protection_visible",
        "workflow_sequence",
        "task_duration_observed",
        "duration_validity",
        "evidence_level",
        "coding_confidence",
    ],
    "cleaned_video_dataset.csv": [
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
        "access_condition",
        "safety_condition",
        "task_duration_observed",
        "duration_validity",
        "evidence_level",
        "coding_confidence",
        "source_type",
        "visibility_quality",
    ],
}


def write_csv(path: Path, headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)


def main() -> None:
    for name, headers in HEADERS.items():
        write_csv(TEMPLATES / name, headers)
        write_csv(DATA / name, headers)
    print(f"Templates written to {TEMPLATES} and {DATA}")


if __name__ == "__main__":
    main()
