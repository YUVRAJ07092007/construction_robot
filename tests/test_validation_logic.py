"""Tests for validation logic — no network or external files required."""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import validate_extractions as v  # noqa: E402


def _rows(header: list[str], *data: tuple) -> list[dict[str, str]]:
    return [dict(zip(header, row)) for row in data]


META_HEADER = ["video_id", "suitability_total_score", "suitability_band", "data_use"]
SEG_HEADER = [
    "segment_id", "segment_duration_sec", "reason_for_rejection",
    "duration_validity", "usable_for_productivity", "activity_type",
]
CLEAN_HEADER = [
    "observation_id", "activity_type", "workflow_stage", "operating_surface",
    "congestion_level", "access_condition", "safety_condition",
    "duration_validity", "coding_confidence", "visibility_quality",
    "evidence_level", "source_type", "data_use", "usable_for_productivity",
]


class TestValidationLogic:
    def test_missing_required_columns(self):
        result = v.ValidationResult()
        v.check_columns(result, "test", [{"video_id": "X"}], ["video_id", "missing_col"])
        assert any("missing columns" in e for e in result.errors)

    def test_invalid_evidence_levels(self):
        result = v.ValidationResult()
        rows = _rows(CLEAN_HEADER, ("O1", "formwork", "pre-pour", "", "low", "open", "good", "invalid", "medium", "high", "E9", "video_observed", "structured_coding", "no"))
        v.validate_cleaned_logic(result, rows)
        assert any("invalid evidence_level" in e for e in result.errors)

    def test_invalid_source_types_in_cleaned(self):
        result = v.ValidationResult()
        rows = _rows(CLEAN_HEADER, ("O2", "formwork", "pre-pour", "", "low", "open", "good", "invalid", "medium", "high", "E1", "manufacturer_reported", "structured_coding", "no"))
        v.validate_cleaned_logic(result, rows)
        assert any("manufacturer data" in e for e in result.errors)

    def test_fresh_concrete_on_wrong_surface(self):
        result = v.ValidationResult()
        rows = _rows(CLEAN_HEADER, ("O3", "fresh_concrete_leveling", "pour", "hardened_concrete", "low", "open", "good", "invalid", "medium", "high", "E2", "video_estimated", "structured_coding", "no"))
        v.validate_cleaned_logic(result, rows)
        assert any("wet surface" in w for w in result.warnings)

    def test_post_cast_wrongly_on_wet_surface(self):
        result = v.ValidationResult()
        rows = _rows(CLEAN_HEADER, ("O4", "post_cast_coating", "post-cast", "wet_concrete", "low", "open", "good", "invalid", "medium", "high", "E2", "video_estimated", "structured_coding", "no"))
        v.validate_cleaned_logic(result, rows)
        assert any("coating" in w for w in result.warnings)

    def test_invalid_duration_for_productivity(self):
        result = v.ValidationResult()
        rows = _rows(SEG_HEADER, ("S1", "10", "", "valid", "yes", "formwork"))
        v.validate_segments(result, rows)
        assert any("usable_for_productivity" in e for e in result.errors)

    def test_manufacturer_in_robot_observations(self):
        result = v.ValidationResult()
        rows = [{"observation_id": "R1", "evidence_level": "E3", "source_type": "manufacturer_reported", "manufacturer_verified": "yes", "manufacturer_name": "BrightMaster"}]
        v.validate_robot_observations(result, rows)
        assert any("must not use E3" in e for e in result.errors)

    def test_low_confidence_modelling_ready(self):
        result = v.ValidationResult()
        rows = _rows(CLEAN_HEADER, ("O5", "formwork", "pre-pour", "", "low", "open", "good", "invalid", "low", "high", "E2", "video_estimated", "modelling_ready", "no"))
        v.validate_cleaned_logic(result, rows)
        assert any("modelling_ready" in e for e in result.errors)

    def test_duplicate_group_without_independent_sample(self):
        result = v.ValidationResult()
        rows = [{"video_id": "M05", "is_duplicate_or_parallel": "yes", "duplicate_group_id": "G1", "independent_sample": "no"}]
        v.validate_duplicate_controls(result, rows, "video")
        assert any("independent_sample" in s for s in result.suggestions)

    def test_unknown_manufacturer_treated_as_verified(self):
        result = v.ValidationResult()
        rows = [{"observation_id": "R2", "evidence_level": "E2", "source_type": "video_estimated", "manufacturer_verified": "yes", "manufacturer_name": "unknown"}]
        v.validate_robot_observations(result, rows)
        assert any("manufacturer_verified=yes but manufacturer_name unknown" in w for w in result.warnings)

    def test_rebar_must_be_pre_pour(self):
        result = v.ValidationResult()
        rows = _rows(CLEAN_HEADER, ("O6", "rebar_work", "pour", "", "high", "congested", "moderate", "invalid", "medium", "medium", "E2", "video_estimated", "structured_coding", "no"))
        v.validate_cleaned_logic(result, rows)
        assert any("rebar activity" in e for e in result.errors)

    def test_segment_below_minimum_without_rejection(self):
        result = v.ValidationResult()
        rows = _rows(SEG_HEADER, ("S2", "4", "", "invalid", "no", "formwork"))
        v.validate_segments(result, rows)
        assert any("below minimum" in e for e in result.errors)
