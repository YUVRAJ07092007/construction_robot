"""Validate synthetic scenario datasets (Phase 3.1 rule + Phase 3B GAN)."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.validate_scenario_constraints import validate_rows  # noqa: E402

SYNTH_PATH = ROOT / "data" / "synthetic_scenario_dataset.csv"
GAN_PATH = ROOT / "data" / "synthetic_scenario_dataset_gan.csv"
ALL_PATH = ROOT / "data" / "synthetic_scenario_dataset_all.csv"
SEED_MATRIX_PATH = ROOT / "data" / "modelling_feature_matrix.csv"

FEATURE_COLS = [
    "video_category_enc",
    "activity_group_enc",
    "workflow_stage_enc",
    "movement_pattern_enc",
    "operating_surface_enc",
    "congestion_level_enc",
    "reinforcement_complexity_enc",
    "access_condition_enc",
    "safety_condition_enc",
    "evidence_level_enc",
    "coding_confidence_enc",
    "manufacturer_name_enc",
    "comparison_robot_enc",
    "labour_count_visible",
    "robot_operator_count",
]

ALLOWED_METHODS = {"rule_expanded", "tabular_gan", "tabular_vae"}


def fingerprint(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row.get(col, "") for col in FEATURE_COLS)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_file(path: Path, *, label: str) -> list[str]:
    if not path.exists():
        return [f"{label}: file not found"]

    synthetic = read_csv(path)
    seeds = read_csv(SEED_MATRIX_PATH) if SEED_MATRIX_PATH.exists() else []
    seed_fps = {fingerprint(row) for row in seeds}

    errors: list[str] = []
    for row in synthetic:
        sid = row.get("scenario_id", "?")
        if row.get("is_synthetic") != "yes":
            errors.append(f"{sid}: is_synthetic must be yes")
        method = row.get("generation_method", "")
        if method not in ALLOWED_METHODS:
            errors.append(f"{sid}: unexpected generation_method '{method}'")
        if fingerprint(row) in seed_fps:
            errors.append(f"{sid}: exact duplicate of seed feature vector")

    constraint = validate_rows(synthetic)
    errors.extend(constraint.errors)

    print(f"Validated {len(synthetic)} {label} scenarios.")
    print(f"Errors: {len(errors)}, Warnings: {len(constraint.warnings)}")
    for msg in errors:
        print(f"  ERROR: {msg}")
    for msg in constraint.warnings:
        print(f"  WARN: {msg}")
    if synthetic:
        warn_rate = sum(
            1 for r in synthetic if int(r.get("constraint_violation_count") or 0) > 0
        ) / len(synthetic)
        print(f"Violation rate (warnings+): {warn_rate * 100:.1f}%")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gan", action="store_true", help="Validate GAN pilot dataset")
    parser.add_argument("--all", action="store_true", help="Validate combined dataset")
    args = parser.parse_args()

    errors: list[str] = []
    if args.gan:
        errors.extend(validate_file(GAN_PATH, label="GAN"))
    elif args.all:
        errors.extend(validate_file(ALL_PATH, label="combined"))
    else:
        errors.extend(validate_file(SYNTH_PATH, label="rule-expanded"))

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
