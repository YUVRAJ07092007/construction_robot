"""Tests for Phase 3B tabular GAN/VAE pilot."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.expand_scenarios import FEATURE_COLS, OUTPUT_HEADER  # noqa: E402
from src.generate_tabular_gan_pilot import (  # noqa: E402
    discretize_sample,
    scenario_family_from_features,
    select_diverse,
)

GAN_PATH = ROOT / "data" / "synthetic_scenario_dataset_gan.csv"
ALL_PATH = ROOT / "data" / "synthetic_scenario_dataset_all.csv"
PILOT_CONFIG = ROOT / "config" / "tabular_gan_pilot_config.yaml"


def test_discretize_clamps_and_access_repair():
    ranges = {
        "congestion_level_enc": [1, 3],
        "access_condition_enc": [1, 3],
        "video_category_enc": [0, 1],
        "labour_count_visible": [0, 12],
        "robot_operator_count": [0, 2],
    }
    for col in FEATURE_COLS:
        ranges.setdefault(col, [0, 99])

    raw = {col: 99.7 for col in FEATURE_COLS}
    raw["congestion_level_enc"] = 3
    raw["access_condition_enc"] = 1  # invalid for congestion 3
    raw["video_category_enc"] = 0
    raw["labour_count_visible"] = 0
    out = discretize_sample(raw, ranges)
    assert out["congestion_level_enc"] == "3"
    assert out["access_condition_enc"] == "2"
    assert out["robot_operator_count"] == "0"
    assert int(out["labour_count_visible"]) >= 2


def test_scenario_family_mapping():
    assert scenario_family_from_features({"video_category_enc": "0"}) == "SF-MIVAN-SLAB-CYCLE"
    assert scenario_family_from_features({"video_category_enc": "1", "activity_group_enc": "4"}) == "SF-ROBOT-FRESH-CONCRETE"
    assert scenario_family_from_features({"video_category_enc": "1", "workflow_stage_enc": "3"}) == "SF-ROBOT-POST-CAST"
    assert scenario_family_from_features({"video_category_enc": "1", "activity_group_enc": "1"}) == "SF-DEPLOYMENT-JOINT"


def test_select_diverse_respects_target():
    pool = []
    for i in range(30):
        pool.append(
            {
                "scenario_family": "SF-MIVAN-SLAB-CYCLE",
                "manufacturer_name_enc": "0",
                **{col: str(i) for col in FEATURE_COLS},
            }
        )
    picked = select_diverse(pool, 10)
    assert len(picked) == 10
    fps = {tuple(r.get(c, "") for c in FEATURE_COLS) for r in picked}
    assert len(fps) == 10


@pytest.mark.skipif(not GAN_PATH.exists(), reason="GAN pilot output not generated")
def test_gan_dataset_schema():
    with GAN_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 50
    assert all(r["is_synthetic"] == "yes" for r in rows)
    assert all(r["generation_method"] in {"tabular_gan", "tabular_vae"} for r in rows)
    assert list(rows[0].keys()) == OUTPUT_HEADER


@pytest.mark.skipif(not ALL_PATH.exists(), reason="Combined synthetic output not generated")
def test_combined_dataset_row_count():
    with ALL_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 100


@pytest.mark.skipif(not PILOT_CONFIG.exists(), reason="Pilot config missing")
def test_pilot_config_targets():
    import yaml

    cfg = yaml.safe_load(PILOT_CONFIG.read_text(encoding="utf-8"))
    assert cfg["generation"]["target_export"] == 50
    assert cfg["model"]["primary"] == "ctgan"
