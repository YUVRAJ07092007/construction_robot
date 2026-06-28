"""Tests for Phase 3.1 rule-based scenario expansion."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.expand_scenarios import expand, fingerprint, read_csv  # noqa: E402
from src.validate_synthetic_scenarios import FEATURE_COLS  # noqa: E402
from src.validate_scenario_constraints import validate_rows  # noqa: E402

SYNTH_PATH = ROOT / "data" / "synthetic_scenario_dataset.csv"
MATRIX_PATH = ROOT / "data" / "modelling_feature_matrix.csv"


@pytest.fixture(scope="module")
def expansion_result():
    return expand()


@pytest.fixture(scope="module")
def synthetic_rows():
    if not SYNTH_PATH.exists():
        expand()
    return read_csv(SYNTH_PATH)


def test_generates_target_count(expansion_result):
    assert expansion_result["generated"] == 50
    assert expansion_result["generated"] <= expansion_result["candidates"]


def test_all_synthetic_flagged(synthetic_rows):
    assert len(synthetic_rows) == 50
    assert all(r["is_synthetic"] == "yes" for r in synthetic_rows)
    assert all(r["generation_method"] == "rule_expanded" for r in synthetic_rows)


def test_no_constraint_errors(synthetic_rows):
    result = validate_rows(synthetic_rows)
    assert not result.errors


def test_no_exact_seed_duplicates(synthetic_rows):
    seeds = read_csv(MATRIX_PATH)
    seed_fps = {fingerprint({c: r.get(c, "") for c in FEATURE_COLS}) for r in seeds}
    for row in synthetic_rows:
        fp = fingerprint({c: row.get(c, "") for c in FEATURE_COLS})
        assert fp not in seed_fps


def test_scenario_families_represented(synthetic_rows):
    families = {r["scenario_family"] for r in synthetic_rows}
    assert "SF-MIVAN-SLAB-CYCLE" in families
    assert "SF-ROBOT-FRESH-CONCRETE" in families
    assert "SF-DEPLOYMENT-JOINT" in families


def test_bright_dream_stratum_preserved(synthetic_rows):
    assert any(r["manufacturer_name_enc"] == "2" for r in synthetic_rows)
