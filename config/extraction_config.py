"""
Decisions for video-informed task-level data extraction.
Defaults chosen for research-safe, reproducible manual coding.
"""

# --- Field naming (single standard across all outputs) ---
ACCESS_CONDITION_FIELD = "access_condition"

# --- Segment rules ---
MIN_SEGMENT_DURATION_SEC = 8
# Shorter clips allowed only when activity is unambiguous (e.g. single robot pass).
MIN_SEGMENT_DURATION_EXCEPTION_SEC = 5
EXCEPTION_ACTIVITY_TYPES = frozenset(
    {
        "concrete_leveling",
        "concrete_finishing",
        "floor_grinding",
    }
)

# --- Mixed / dual-category videos ---
# Primary category drives main observation table; secondary noted in video_metadata.notes.
ALLOW_DUAL_CATEGORY_CODING = True

# --- Workflow ---
# Stage 1 approved 2026-06-27; Stage 2 complete 2026-06-28; Phase 3.1 + 3C complete 2026-06-28.
WORKFLOW = "stage_3_phase_3b_complete"

# --- Suitability criteria (max 2 points each, total max 14) ---
SUITABILITY_CRITERIA = {
    "relevance": {
        "label": "Relevance to construction robot or Mivan construction",
        "scores": {
            0: "Off-topic, unrelated construction, or wrong process",
            1: "Related construction but weak link to robot or Mivan/aluminium formwork",
            2: "Clear robot operation or Mivan/aluminium formwork slab-cycle content",
        },
    },
    "visual_clarity": {
        "label": "Clarity of visual content",
        "scores": {
            0: "Blurry, dark, heavily obstructed, or unusable resolution",
            1: "Partially clear; some frames usable with effort",
            2: "Activity and work zone clearly visible for most of the clip",
        },
    },
    "activity_continuity": {
        "label": "Continuity of construction activity",
        "scores": {
            0: "Fragmented, mostly cuts, or no continuous task shown",
            1: "Some continuous segments but frequent jumps or gaps",
            2: "Sustained continuous activity suitable for segment coding",
        },
    },
    "activity_identifiability": {
        "label": "Ability to identify the activity type",
        "scores": {
            0: "Activity unclear or ambiguous",
            1: "Broad activity guess only (e.g. 'site work')",
            2: "Specific activity identifiable (leveling, rebar, pour, stripping, etc.)",
        },
    },
    "interaction_visibility": {
        "label": "Ability to observe labour, robot, or work-zone interaction",
        "scores": {
            0: "No meaningful worker/robot/zone interaction visible",
            1: "Limited interaction visible",
            2: "Clear worker counts, robot movement, or congestion/access interaction",
        },
    },
    "editing_level": {
        "label": "Low editing / low promotional interruption",
        "scores": {
            0: "Heavy montage, time-lapse for timing, or promo-only",
            1: "Some editing or promotional inserts but core activity remains",
            2: "Mostly raw or lightly edited field/process footage",
        },
    },
    "parameter_measurability": {
        "label": "Suitability for parameter extraction",
        "scores": {
            0: "Cannot extract any structured variables reliably",
            1: "1–3 variables extractable with medium confidence",
            2: "Multiple variables extractable with E1/E2 coding",
        },
    },
}

SUITABILITY_MAX_SCORE = len(SUITABILITY_CRITERIA) * 2

SUITABILITY_BANDS = {
    "exclude": (0, 5),
    "qualitative_only": (6, 9),
    "structured_extraction": (10, 14),
}

# --- Evidence levels used in video extraction stage ---
VIDEO_EVIDENCE_LEVELS = frozenset({"E1", "E2"})
