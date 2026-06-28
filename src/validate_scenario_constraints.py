"""Validate logical consistency of scenario records (Stage 3 design — seed or synthetic)."""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML required") from exc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CONFIG_PATH = ROOT / "config" / "generative_augmentation_config.yaml"

# Reverse maps from seed_encoding_schema ordinals (approximate label lookup for matrix rows).
WORKFLOW_FROM_ENC = {"0": "unknown", "1": "pre-pour", "2": "pour", "3": "post-cast"}
SURFACE_FROM_ENC = {"0": "unknown", "1": "wet_concrete", "2": "pre_pour_slab", "3": "hardened_concrete"}
ACTIVITY_FROM_ENC: dict[str, str] = {}


@dataclass
class ScenarioValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def violation_count(self) -> int:
        return len(self.errors) + len(self.warnings)


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_activity_enc_map(config: dict) -> dict[str, str]:
    return {str(v): k for k, v in config["activity_group"].items()}


def validate_scenario_row(row: dict[str, str], config: dict, row_id: str) -> ScenarioValidationResult:
    result = ScenarioValidationResult()
    activity_map = load_activity_enc_map(config)
    constraints = config["scenario_constraints"]

    activity = row.get("activity_group") or activity_map.get(row.get("activity_group_enc", ""), "")
    workflow = row.get("workflow_stage") or WORKFLOW_FROM_ENC.get(row.get("workflow_stage_enc", ""), "")
    surface = row.get("operating_surface") or SURFACE_FROM_ENC.get(row.get("operating_surface_enc", ""), "")

    expected_workflow = constraints["workflow_activity_pairs"].get(activity)
    if expected_workflow and workflow and workflow != "unknown":
        allowed = expected_workflow if isinstance(expected_workflow, list) else [expected_workflow]
        if workflow not in allowed:
            result.errors.append(
                f"{row_id}: activity {activity} expects workflow in {allowed}, got {workflow}"
            )

    if activity in constraints["fresh_concrete_activities"]:
        if surface and surface not in constraints["fresh_surfaces"] and surface != "unknown":
            result.warnings.append(f"{row_id}: fresh-concrete activity expects wet surface, got {surface}")

    if activity in constraints["post_cast_activities"]:
        if surface and surface not in constraints["hardened_surfaces"] and surface != "unknown":
            result.warnings.append(f"{row_id}: post-cast activity expects hardened surface, got {surface}")

    congestion = (row.get("congestion_level") or "").lower()
    access_enc = row.get("access_condition_enc", "")
    access = (row.get("access_condition") or "").lower()
    if not access and access_enc == "1":
        access = "open"
    if congestion == "high" and access == "open":
        result.warnings.append(f"{row_id}: high congestion with open access may be inconsistent")

    return result


def validate_rows(rows: list[dict[str, str]]) -> ScenarioValidationResult:
    config = load_config()
    combined = ScenarioValidationResult()
    for row in rows:
        row_id = row.get("scenario_id") or row.get("seed_id") or row.get("source_observation_id") or "?"
        partial = validate_scenario_row(row, config, row_id)
        combined.errors.extend(partial.errors)
        combined.warnings.extend(partial.warnings)
    return combined


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    seed_path = ROOT / "data" / "gan_seed_dataset.csv"
    if not seed_path.exists():
        print(f"Not found: {seed_path}")
        return 1

    rows = read_csv(seed_path)
    result = validate_rows(rows)
    print(f"Validated {len(rows)} seed scenarios as constraint baseline.")
    print(f"Errors: {len(result.errors)}, Warnings: {len(result.warnings)}")
    for msg in result.errors:
        print(f"  ERROR: {msg}")
    for msg in result.warnings:
        print(f"  WARN: {msg}")
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
