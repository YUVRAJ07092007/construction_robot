"""Tests for Stage 2 GAN seed conversion logic."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.convert_gan_seed import encode, is_eligible, load_schema  # noqa: E402
from src.validate_seed_dataset import validate_seed_dataset  # noqa: E402


def _cleaned_row(**overrides) -> dict[str, str]:
    base = {
        "observation_id": "OBS-T-001",
        "video_id": "M02",
        "segment_id": "M02-S05",
        "video_category": "mivan",
        "activity_type": "formwork_erection",
        "workflow_stage": "pre-pour",
        "labour_count_visible": "8",
        "robot_operator_count": "",
        "movement_pattern": "",
        "operating_surface": "",
        "congestion_level": "high",
        "reinforcement_complexity": "medium",
        "access_condition": "congested",
        "safety_condition": "moderate",
        "task_duration_observed": "208",
        "duration_validity": "invalid",
        "evidence_level": "E1",
        "coding_confidence": "high",
        "source_type": "video_observed",
        "visibility_quality": "high",
        "data_use": "structured_coding",
        "visible_segment_duration_sec": "208",
        "duration_validity_reason": "test",
        "usable_for_productivity": "no",
        "is_duplicate_or_parallel": "no",
        "duplicate_group_id": "",
        "independent_sample": "yes",
        "label_revision_note": "",
        "manufacturer_name": "unknown",
        "robot_category": "",
    }
    base.update(overrides)
    return base


class TestSeedPromotion:
    @pytest.fixture
    def rules(self):
        return load_schema()["seed_promotion_rules"]

    def test_eligible_row(self, rules):
        ok, reason = is_eligible(_cleaned_row(), rules)
        assert ok is True
        assert reason == ""

    def test_rejects_duplicate(self, rules):
        ok, reason = is_eligible(_cleaned_row(is_duplicate_or_parallel="yes"), rules)
        assert ok is False
        assert reason == "duplicate_or_parallel"

    def test_rejects_low_confidence(self, rules):
        ok, reason = is_eligible(_cleaned_row(coding_confidence="low"), rules)
        assert ok is False
        assert "coding_confidence" in reason

    def test_rejects_qualitative_only(self, rules):
        ok, reason = is_eligible(_cleaned_row(data_use="qualitative_only"), rules)
        assert ok is False
        assert reason == "qualitative_only"


class TestEncoding:
    def test_encode_case_insensitive_manufacturer(self):
        schema = load_schema()
        assert encode(schema["manufacturer_name"], "BrightMaster") == 1
        assert encode(schema["manufacturer_name"], "Bright Dream") == 2


class TestSeedValidation:
    def test_valid_seed_row(self):
        row = {
            "seed_id": "SEED-001",
            "source_observation_id": "OBS-M02-005",
            "video_category": "mivan",
            "activity_group": "formwork_work",
            "workflow_stage": "pre-pour",
            "data_use": "modelling_ready",
            "duration_excluded": "yes",
            "usable_for_productivity": "no",
            "independent_sample": "yes",
            "seed_provenance": "video_observed_secondary",
        }
        result = validate_seed_dataset([row])
        assert not result.errors

    def test_rejects_productivity_flag(self):
        row = {
            "seed_id": "SEED-001",
            "source_observation_id": "OBS-X",
            "video_category": "robot",
            "activity_group": "fresh_concrete_leveling",
            "workflow_stage": "pour",
            "data_use": "modelling_ready",
            "duration_excluded": "yes",
            "usable_for_productivity": "yes",
            "independent_sample": "yes",
            "seed_provenance": "video_observed_secondary",
        }
        result = validate_seed_dataset([row])
        assert any("usable_for_productivity" in e for e in result.errors)
