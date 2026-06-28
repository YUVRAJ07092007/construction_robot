"""Tests for Phase 3C DRI framework."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.compute_dri_scores import (  # noqa: E402
    clamp_score,
    score_access,
    score_surface,
    compute_all,
)

DRI_PATH = ROOT / "data" / "dri_scored_scenarios.csv"


def test_access_score_range():
    assert 0 <= score_access("1", "1") <= 100
    assert score_access("1", "1") > score_access("3", "3")


def test_fresh_concrete_surface_alignment():
    dri_config = __import__("yaml").safe_load(
        (ROOT / "config" / "dri_framework_config.yaml").read_text(encoding="utf-8")
    )
    assert score_surface("4", "1", dri_config) == 100
    assert score_surface("4", "3", dri_config) == 20


@pytest.fixture(scope="module")
def dri_rows():
    compute_all(use_all_synthetic=False)
    with DRI_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_dri_output_count(dri_rows):
    assert len(dri_rows) == 64  # 14 seeds + 50 synthetic


def test_robot_records_have_dri(dri_rows):
    robot = [r for r in dri_rows if r["dri_applicable"] == "yes"]
    assert len(robot) >= 30
    assert all(r["dri_total_score"] for r in robot)


def test_mivan_seeds_sci_only(dri_rows):
    mivan_seeds = [r for r in dri_rows if r["record_type"] == "mivan_seed"]
    assert len(mivan_seeds) == 7
    assert all(r["sci_only"] == "yes" for r in mivan_seeds)
    assert all(r["dri_applicable"] == "no" for r in mivan_seeds)


def test_provenance_marker(dri_rows):
    assert all(r["score_provenance"] == "framework_derived_scenario_relative" for r in dri_rows)


def test_all_synthetic_dri_count():
    gan_path = ROOT / "data" / "synthetic_scenario_dataset_gan.csv"
    if not gan_path.exists():
        pytest.skip("GAN pilot output not generated")
    compute_all(use_all_synthetic=True)
    with DRI_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 114
    compute_all(use_all_synthetic=False)
