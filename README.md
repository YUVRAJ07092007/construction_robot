# Construction Robot — Video-Informed Data Extraction Pipeline

Structured observational coding pipeline for research on **construction robot deployment readiness** in **Mivan / aluminium formwork** high-rise building construction.

Public videos and manufacturer pages are used as **secondary observational sources** — not as field-measured productivity data. Outputs support framework development and scenario modelling.

**Project scope:** **Stage 1 complete — pending review.** Stage 2 (GAN seed conversion) is **deferred** until Stage 1 is reviewed and approved.

**Robot-agnostic design:** BrightMaster Robotics is one source among many. The schema supports comparison robots from any manufacturer (`manufacturer_name`, `comparison_robot`, `robot_source_candidates.csv`).

**Target paper context:** *Video-Informed and GAN-Augmented Framework for Assessing Construction Robot Deployment Readiness in Aluminium Formwork-Based High-Rise Building Construction* (Journal of Building Engineering).

> The dataset is a secondary observational dataset derived from publicly available videos and manufacturer-reported specifications. It is not direct field-measured productivity data.

---

## What this repository contains

| Area | Description |
|------|-------------|
| **Algorithm** | 10-step video-informed task-level extraction method |
| **Source review** | Curated robot + Mivan workflow video links |
| **CSV datasets** | Registry, segments, robot/Mivan observations, cleaned merge |
| **E3 specs** | Manufacturer-reported technical parameters (separate from video coding) |
| **Validation** | Python checks + reports for schema and construction logic |
| **Data dictionary** | `config/data_dictionary.yaml`, `config/activity_taxonomy.yaml` |

---

## Repository structure

```text
construction_robot/
├── README.md
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
│   └── templates/
├── docs/
│   ├── video_coding_checklist.md
│   └── current_stage_completion_checklist.md
├── reports/
│   ├── repo_audit_report.md
│   ├── validation_report.md
│   ├── data_quality_report.md
│   └── current_stage_readiness_review.md
├── scripts/
└── src/
    ├── validate_extractions.py
    └── generate_data_quality_report.py
```

---

## Pipeline overview

### Stage 1 — Video extraction (**complete — pending review**)

1. **Registry** — Record each video/source with metadata  
2. **Screen** — Score suitability 0–14 (7 criteria × 0–2)  
3. **Segment** — Split into usable activity clips  
4. **Extract** — Code robot-side and Mivan-side parameters  
5. **Evidence** — Label E1–E5; use mainly E1/E2 for video stage  
6. **Validate** — Apply construction logic rules  
7. **Export** — Five CSV outputs + cleaned merge  

**Stop point:** Stage 1 coding complete. **Pause for human review.** Do not proceed to Stage 2.

**Stage 1 completion checklist**

- [x] All priority sources screened in `video_metadata.csv`
- [x] Structured-extraction videos segmented and coded
- [x] `manufacturer_specs.csv` populated for E3 references (T01–T04)
- [x] `python src/validate_extractions.py` passes
- [ ] Review sign-off on coding quality and research-safe framing

### Stage 2 — GAN seed conversion (deferred)

Convert cleaned video-derived data into normalised seed records for synthetic scenario generation. **Not in scope until Stage 1 review approval.**

---

## Current dataset status

| File | Rows (approx.) | Notes |
|------|----------------|-------|
| `video_metadata.csv` | 31 | All R01 pool + R04 + M04 screened |
| `video_segments.csv` | 45 | M01–M03, M05–M06, R02, R05–R13, R15 |
| `robot_video_observations.csv` | 10 | BrightMaster robot demos + leveling/layout |
| `mivan_video_observations.csv` | 30 | Slab-cycle workflow coding |
| `cleaned_video_dataset.csv` | 16 | Key rows for modelling |
| `manufacturer_specs.csv` | 10 | T01–T04 E3 reference values |

**Structured-extraction videos:** M01–M03, M05–M06 · R02, R05–R07, R09–R13, R15

---

## Evidence levels

| Level | Meaning |
|-------|---------|
| E1 | Directly visible from video |
| E2 | Visually estimated from video |
| E3 | Manufacturer-reported specification |
| E4 | Computed from extracted data |
| E5 | Assumption-based |

Video extraction uses mainly **E1** and **E2**. Manufacturer pages use **E3** only in `manufacturer_specs.csv`.

---

## Source-type system

| source_type | Meaning |
|-------------|---------|
| video_observed | Directly visible in video |
| video_estimated | Estimated from video |
| manufacturer_reported | Product page or company claim |
| computed | Calculated from other fields |
| assumption_based | Scenario modelling only |

---

## Duration-validity warning

Visible segment duration is **not** productivity time unless independently verified. Edited, promotional, or narrated montage segments are marked `duration_validity=invalid` with `usable_for_productivity=no`.

---

## Quick start

Requires **Python 3.10+**. Core scripts use stdlib only; `pytest` optional for tests.

```bash
# Validate datasets
python src/validate_extractions.py

# Generate data quality report
python src/generate_data_quality_report.py

# Run validation tests
pytest tests/
```

Optional: `pip install yt-dlp` for metadata download during source screening.

---

## Coding workflow

See `docs/video_coding_checklist.md` for the full operational guide.

1. Add/update `video_metadata.csv` with suitability scores and `data_use`  
2. For score 10+, add segments to `video_segments.csv`  
3. Code observations in robot or Mivan CSV  
4. Add representative rows to `cleaned_video_dataset.csv`  
5. Run validation and data quality report  

**Key rules:** min segment 8 s (5 s robot-pass exception) · field name `access_condition` · separate fresh vs post-cast activities

---

## What should NOT be claimed

- Real-site validated productivity improvement  
- Independent verification of manufacturer efficiency claims  
- BrightMaster-specific generalisation to all construction robots  
- Quantitative cycle-time savings from public video duration alone  

---

## Key documentation

- [Video extraction algorithm](video_informed_task_level_data_extraction_algorithm.md)
- [Video & source suitability review](brightmaster_mivan_video_links_suitability_review.md)
- [Current stage completion checklist](docs/current_stage_completion_checklist.md)
- [Readiness review](reports/current_stage_readiness_review.md) — label: **framework_ready**

---

## License

Research and educational use. Video sources remain subject to platform terms. Manufacturer specifications are **manufacturer-reported (E3)** and not independently verified field data.
