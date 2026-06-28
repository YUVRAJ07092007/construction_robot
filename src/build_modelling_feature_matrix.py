"""Build numeric modelling feature matrix from GAN seed dataset (Stage 3 design artifact)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML required") from exc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
CONFIG_PATH = ROOT / "config" / "generative_augmentation_config.yaml"
SEED_PATH = DATA_DIR / "gan_seed_dataset.csv"
OUT_PATH = DATA_DIR / "modelling_feature_matrix.csv"


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_int(value: str, default: int = 0) -> int:
    text = (value or "").strip()
    if not text:
        return default
    try:
        return int(float(text))
    except ValueError:
        return default


def build_matrix_rows(seeds: list[dict[str, str]], config: dict) -> tuple[list[str], list[dict[str, str]]]:
    activity_map = config["activity_group"]
    cat_cols = config["modelling_features"]["categorical_enc"]
    num_cols = config["modelling_features"]["numeric"]

    header = ["seed_id", "source_observation_id"] + cat_cols + num_cols

    rows: list[dict[str, str]] = []
    for seed in seeds:
        activity = (seed.get("activity_group") or "").strip()
        row = {
            "seed_id": seed.get("seed_id", ""),
            "source_observation_id": seed.get("source_observation_id", ""),
            "video_category_enc": seed.get("video_category_enc", "0"),
            "activity_group_enc": str(activity_map.get(activity, activity_map.get("unknown", 0))),
            "workflow_stage_enc": seed.get("workflow_stage_enc", "0"),
            "movement_pattern_enc": seed.get("movement_pattern_enc", "0"),
            "operating_surface_enc": seed.get("operating_surface_enc", "0"),
            "congestion_level_enc": seed.get("congestion_level_enc", "0"),
            "reinforcement_complexity_enc": seed.get("reinforcement_complexity_enc", "0"),
            "access_condition_enc": seed.get("access_condition_enc", "0"),
            "safety_condition_enc": seed.get("safety_condition_enc", "0"),
            "evidence_level_enc": seed.get("evidence_level_enc", "0"),
            "coding_confidence_enc": seed.get("coding_confidence_enc", "0"),
            "manufacturer_name_enc": seed.get("manufacturer_name_enc", "0"),
            "comparison_robot_enc": seed.get("comparison_robot_enc", "0"),
            "labour_count_visible": str(parse_int(seed.get("labour_count_visible", ""))),
            "robot_operator_count": str(parse_int(seed.get("robot_operator_count", ""))),
        }
        rows.append(row)

    return header, rows


def main() -> int:
    if not SEED_PATH.exists():
        print(f"Seed dataset not found: {SEED_PATH}")
        return 1

    config = load_config()
    with SEED_PATH.open(newline="", encoding="utf-8") as handle:
        seeds = list(csv.DictReader(handle))

    header, rows = build_matrix_rows(seeds, config)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUT_PATH} ({len(rows)} rows × {len(header)} columns)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
