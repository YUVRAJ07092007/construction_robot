# Repository Audit Report

**Date:** 2026-06-28  
**Scope:** Full read-only audit of `construction_robot` repository  
**Status:** Video data extraction is **ongoing**. This audit does **not** judge the dataset as final.

---

## 1. Current folder structure

```text
construction_robot/
├── README.md
├── cursor_prompts_construction_robot_value_addition.md
├── video_informed_task_level_data_extraction_algorithm.md
├── brightmaster_mivan_video_links_suitability_review.md
├── config/
│   ├── extraction_config.py
│   ├── data_dictionary.yaml
│   └── activity_taxonomy.yaml
├── data/
│   ├── video_metadata.csv
│   ├── video_segments.csv
│   ├── robot_video_observations.csv
│   ├── mivan_video_observations.csv
│   ├── cleaned_video_dataset.csv
│   ├── manufacturer_specs.csv
│   ├── robot_source_candidates.csv
│   ├── templates/
│   └── cache/
├── docs/
│   ├── video_coding_checklist.md
│   └── current_stage_completion_checklist.md
├── reports/
│   ├── repo_audit_report.md
│   ├── validation_report.md
│   ├── validation_issues.csv
│   ├── data_quality_report.md
│   └── current_stage_readiness_review.md
├── scripts/
│   ├── init_templates.py
│   ├── seed_video_registry.py
│   ├── batch_update_pipeline.py
│   ├── complete_stage1.py
│   └── apply_schema_enhancements.py
├── src/
│   ├── validate_extractions.py
│   └── generate_data_quality_report.py
└── tests/
    └── test_validation_logic.py
```

---

## 2. Data files and row counts

| File | Rows (approx.) |
|------|----------------|
| video_metadata.csv | 31 |
| video_segments.csv | 45 |
| robot_video_observations.csv | 10 |
| mivan_video_observations.csv | 30 |
| cleaned_video_dataset.csv | 16 |
| manufacturer_specs.csv | 10 |
| robot_source_candidates.csv | 8+ |

---

## 3. Python scripts and purpose

| Script | Purpose |
|--------|---------|
| `scripts/init_templates.py` | Create empty CSV templates |
| `scripts/seed_video_registry.py` | Seed priority source registry |
| `scripts/batch_update_pipeline.py` | Batch registry/observation updates |
| `scripts/complete_stage1.py` | Complete Stage 1 screening and coding |
| `scripts/apply_schema_enhancements.py` | Add robot-agnostic and QC columns |
| `src/validate_extractions.py` | Schema + logic validation with reports |
| `src/generate_data_quality_report.py` | Data quality summary report |

---

## 4. Schema columns by file

See `config/data_dictionary.yaml` for authoritative column definitions. Core legacy columns remain; extended columns include `manufacturer_name`, `robot_category`, `data_use`, `source_type`, duplicate controls, and duration-validity fields.

---

## 5. Missing or inconsistent columns

**Research-design gaps (expected at this stage):**
- Robot-side observations still dominated by one manufacturer (BrightMaster)
- `modelling_ready` not yet assigned conservatively
- Some pool sources catalogued but not individually coded

**Data-quality gaps:**
- Legacy `source_type` values use both hyphen and underscore forms in cleaned dataset (`video-observed` vs `video_observed`)
- Not all observation tables yet expose `label_revision_note` uniformly

These are addressable without breaking backward compatibility.

---

## 6. Duplicate or parallel video risks

| Group | Members | Control |
|-------|---------|---------|
| DUP-MIVAN-SLAB-7DAY | M01, M05 | M01 independent; M05 parallel cross-check |
| DUP-BMR-NP320-COATING | R07, R13 | R07 independent; R13 parallel variant |

Risk is **visible and controlled** via `duplicate_group_id` and `independent_sample`.

---

## 7. Duration-validity risks

- All coded segments currently marked `duration_validity=invalid` or non-productivity
- `usable_for_productivity=no` enforced across segments and cleaned rows
- Promotional/edited footage explicitly documented in `duration_validity_reason`

**Risk level:** Low for productivity overclaim; durations retained as visible segment times only.

---

## 8. Manufacturer-data separation risks

- Manufacturer pages (T01–T04) isolated in `manufacturer_specs.csv` with E3
- Validation rejects E3 in video observation tables
- R03 excluded due to unverified manufacturer attribution

**Risk level:** Low with current validation rules.

---

## 9. Robot-agnostic coverage status

- Schema supports any manufacturer (`manufacturer_name`, `comparison_robot`, `manufacturer_verified`)
- `data/robot_source_candidates.csv` tracks expansion targets
- Current coded robot videos are primarily BrightMaster official demos
- R03 flagged as comparison/unverified example

**Status:** Framework is robot-agnostic; sample coverage is not yet balanced across manufacturers.

---

## 10. Priority fixes before further extraction

1. Add comparison robot sources with verified URLs to candidates file and screen individually
2. Normalize legacy `source_type` hyphen/underscore values
3. Promote additional robot activity types (rebar tying, inspection) when suitable videos found
4. Keep duplicate controls updated when parallel uploads are added
5. Do **not** proceed to GAN seed conversion (Stage 2) until Stage 1 review sign-off

---

## Audit conclusion

The repository is **logically structured** for ongoing video-informed extraction. Data quality controls and research-safe framing are in place. Extraction remains **in progress**; the dataset is suitable for framework development demonstration, not final quantitative claims.
