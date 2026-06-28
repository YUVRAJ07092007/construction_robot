"""Tests for Stage 3 design artifacts."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.build_modelling_feature_matrix import build_matrix_rows, load_config  # noqa: E402
from src.validate_scenario_constraints import validate_rows  # noqa: E402


@pytest.fixture
def seeds():
    path = ROOT / "data" / "gan_seed_dataset.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_feature_matrix_row_count_matches_seeds(seeds):
    config = load_config()
    header, rows = build_matrix_rows(seeds, config)
    assert len(rows) == len(seeds) == 14
    assert len(header) == 17


def test_all_seeds_have_activity_group_enc(seeds):
    config = load_config()
    _, rows = build_matrix_rows(seeds, config)
    for row in rows:
        assert int(row["activity_group_enc"]) > 0


def test_seed_constraint_baseline_no_errors(seeds):
    result = validate_rows(seeds)
    assert not result.errors
