# Construction Robot — Video-Informed Data Extraction Pipeline

Structured observational coding pipeline for research on **construction robot deployment readiness** in **Mivan / aluminium formwork** high-rise building construction.

Public videos and manufacturer pages are used as **secondary observational sources** — not as field-measured productivity data. Outputs support framework development and scenario modelling.

**Project scope:** Stages 1–2 complete · Phase 3.1 (50 rule synthetics) · **Phase 3B GAN pilot complete** · **Phase 3C DRI framework complete**.

**Robot-agnostic design:** BrightMaster Robotics is one source among many. The schema supports comparison robots from any manufacturer (`manufacturer_name`, `comparison_robot`, `robot_source_candidates.csv`).

**Target paper context:** *Video-Informed and GAN-Augmented Framework for Assessing Construction Robot Deployment Readiness in Aluminium Formwork-Based High-Rise Building Construction* (Journal of Building Engineering).

**Repository status:** `reviewer_ready_with_limitations` — see [`docs/repository_status_matrix.md`](docs/repository_status_matrix.md).

Final fixes: [`docs/final_cursor_improvement_prompts_construction_robot.md`](docs/final_cursor_improvement_prompts_construction_robot.md)

> This repository does not contain direct field-measured productivity data. Public videos are used only as secondary observational sources for extracting visible task-level parameters and workflow characteristics.

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
| **Seed dataset** | GAN-ready seeds + 14×17 feature matrix |
| **Synthetic pilot** | Rule + GAN/TVAE scenarios (pilot-only) |
| **DRI framework** | Scenario-relative deployment readiness scoring |

---

## Repository structure

```text
construction_robot/
├── README.md
├── cursor_prompts_construction_robot_value_addition.md   # Stage 1 QA / schema hardening prompts (15/15 done)
├── video_informed_task_level_data_extraction_algorithm.md
├── brightmaster_mivan_video_links_suitability_review.md
├── config/
│   ├── extraction_config.py
│   ├── data_dictionary.yaml
│   ├── activity_taxonomy.yaml
│   ├── seed_encoding_schema.yaml
│   ├── generative_augmentation_config.yaml
│   └── dri_framework_config.yaml
├── data/
│   ├── video_metadata.csv
│   ├── video_segments.csv
│   ├── robot_video_observations.csv
│   ├── mivan_video_observations.csv
│   ├── cleaned_video_dataset.csv
│   ├── gan_seed_dataset.csv
│   ├── modelling_feature_matrix.csv
│   ├── synthetic_scenario_dataset.csv
│   ├── dri_scored_scenarios.csv
│   ├── manufacturer_specs.csv
│   ├── robot_source_candidates.csv
│   └── templates/
├── docs/
│   ├── video_coding_checklist.md
│   ├── current_stage_completion_checklist.md
│   ├── stage1_signoff.md
│   ├── stage2_signoff.md
│   ├── gan_seed_conversion_algorithm.md
│   ├── generative_augmentation_design.md
│   ├── deployment_readiness_index_design.md
│   ├── phase3_1_signoff.md
│   ├── phase3c_signoff.md
│   └── paper_methods_draft.md
├── reports/
│   ├── repo_audit_report.md
│   ├── validation_report.md
│   ├── data_quality_report.md
│   ├── seed_conversion_report.md
│   ├── synthetic_expansion_report.md
│   ├── dri_scoring_report.md
│   └── current_stage_readiness_review.md
├── scripts/
│   ├── complete_stage2.py
│   ├── complete_stage3.py
│   └── complete_stage3c.py
└── src/
    ├── validate_extractions.py
    ├── generate_data_quality_report.py
    ├── convert_gan_seed.py
    ├── expand_scenarios.py
    ├── compute_dri_scores.py
    └── validate_dri_scores.py
```

---

## Pipeline overview

### Stage 1 — Video extraction (**approved 2026-06-27**)

1. **Registry** — Record each video/source with metadata  
2. **Screen** — Score suitability 0–14 (7 criteria × 0–2)  
3. **Segment** — Split into usable activity clips  
4. **Extract** — Code robot-side and Mivan-side parameters  
5. **Evidence** — Label E1–E5; use mainly E1/E2 for video stage  
6. **Validate** — Apply construction logic rules  
7. **Export** — Five CSV outputs + cleaned merge  

Sign-off: [`docs/stage1_signoff.md`](docs/stage1_signoff.md)

### Stage 2 — GAN seed conversion (**complete 2026-06-28**)

1. **Promote** — Apply independent-sample and confidence rules to cleaned rows  
2. **Normalize** — Map activities to taxonomy groups  
3. **Encode** — Add integer `*_enc` columns per `seed_encoding_schema.yaml`  
4. **Export** — `gan_seed_dataset.csv` + update `framework_seed_ready` flags  
5. **Validate** — Seed schema checks + Stage 1 re-validation  

**Not included:** GAN model training or synthetic record generation.

```bash
python scripts/complete_stage2.py
```

Sign-off: [`docs/stage2_signoff.md`](docs/stage2_signoff.md)

### Stage 3 — Generative augmentation (**Phase 3.1 complete**)

Rule-based scenario expansion from 14 seeds → **50 synthetic scenarios**.

```bash
python scripts/complete_stage3.py
```

Docs: [`generative_augmentation_design.md`](docs/generative_augmentation_design.md) · [`phase3_1_signoff.md`](docs/phase3_1_signoff.md)

### Stage 3C — Deployment Readiness Index (**complete**)

Weighted composite scoring (5 dimensions) on seeds + synthetics. Scenario-relative; **not field-validated**.

```bash
python scripts/complete_stage3c.py
```

Docs: [`deployment_readiness_index_design.md`](docs/deployment_readiness_index_design.md) · [`phase3c_signoff.md`](docs/phase3c_signoff.md)

### Stage 3B — Tabular GAN/VAE pilot (**complete**)

CTGAN/TVAE pilot on 14×15 feature matrix → **50 GAN scenarios** (constraint-filtered), combined with rule synthetics → 100 total.

```bash
pip install -r requirements-gan-pilot.txt
python scripts/complete_stage3b.py
```

Docs: [`phase3b_signoff.md`](docs/phase3b_signoff.md) · [`reports/tabular_gan_pilot_report.md`](reports/tabular_gan_pilot_report.md)

**Deferred:** Expert weight calibration, field validation.

---

## Current dataset status

| File | Rows (approx.) | Notes |
|------|----------------|-------|
| `video_metadata.csv` | 32 | All R01 pool + R04 + M04 screened |
| `video_segments.csv` | 46 | M01–M03, M05–M06, R02, R05–R13, R15, R22 |
| `robot_video_observations.csv` | 11 | BrightMaster demos + Bright Dream R22 comparison |
| `mivan_video_observations.csv` | 30 | Slab-cycle workflow coding |
| `cleaned_video_dataset.csv` | 17 | 14 promoted to `framework_seed_ready` |
| `gan_seed_dataset.csv` | 14 | Independent-sample seeds |
| `synthetic_scenario_dataset.csv` | 50 | Rule-expanded Phase 3.1 |
| `pilot_rule_based_synthetic_scenarios.csv` | 50 | Reviewer alias of rule synthetics |
| `synthetic_scenario_dataset_gan.csv` | 50 | Tabular GAN/VAE Phase 3B |
| `pilot_gan_synthetic_scenarios.csv` | 50 | Reviewer alias of GAN synthetics |
| `synthetic_scenario_dataset_all.csv` | 100 | Rule + GAN combined |
| `pilot_combined_synthetic_scenarios.csv` | 100 | Reviewer alias of combined |
| `dri_scored_scenarios.csv` | 64 (114 with `--all-synthetic`) | DRI framework scores |
| `manufacturer_specs.csv` | 10 | T01–T04 E3 reference values |

**Structured-extraction videos:** M01–M03, M05–M06 · R02, R05–R07, R09–R13, R15, R22

---

## Data-use system

| data_use | Meaning |
|----------|---------|
| exclude | Not used in framework |
| qualitative_only | Descriptive context only |
| structured_coding | Coded but not seed-promoted |
| framework_seed_ready | Suitable for seed-dataset use (not field-validated) |

---

## Manufacturer-claim warning

All rows in `manufacturer_specs.csv` are **E3 manufacturer-reported**. Claims include `claim_type`, `claim_use`, and `used_in_model=no`. Productivity and manpower-reduction claims are **not independently verified**.

---

## Duplicate / parallel-source control

Videos and observations use `is_duplicate_or_parallel`, `duplicate_group_id`, and `independent_sample`. Only one record per duplicate group should count as an independent sample.

---

## Synthetic data pilot warning

Rule-expanded and GAN/TVAE scenarios are marked `pilot_only=yes` and `not_for_statistical_inference=yes`. They stress-test framework logic — not observed site data.

---

## DRI scenario-relative warning

Deployment Readiness Index scores in `dri_scored_scenarios.csv` enable **scenario-relative ranking** within the coded corpus. They are **not field-validated** deployment performance. Run weight sensitivity: `python src/dri_weight_sensitivity.py`.

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
# Validate Stage 1 datasets
python src/validate_extractions.py

# Stage 2: convert seeds + validate + refresh reports
python scripts/complete_stage2.py

# Stage 3 design: feature matrix + constraint baseline
python scripts/complete_stage3_design.py

# Phase 3.1: expand synthetic scenarios
python scripts/complete_stage3.py

# Phase 3C: DRI framework scoring
python scripts/complete_stage3c.py

# Phase 3B: tabular GAN pilot
python scripts/complete_stage3b.py

# DRI weight sensitivity
python src/dri_weight_sensitivity.py

# File formatting check
python scripts/check_file_formatting.py

# Final reviewer-safe schema + reports
python scripts/complete_final_improvements.py

# Reviewer-safe schema + reports (prior pass)
python scripts/complete_reviewer_improvements.py

# Generate data quality report
python src/generate_data_quality_report.py

# Run all tests
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
- [Value-addition prompts](cursor_prompts_construction_robot_value_addition.md) — schema/QA hardening (15/15 complete)
- [Stage 1 sign-off](docs/stage1_signoff.md)
- [Stage 2 sign-off](docs/stage2_signoff.md)
- [GAN seed conversion algorithm](docs/gan_seed_conversion_algorithm.md)
- [Generative augmentation design](docs/generative_augmentation_design.md)
- [Deployment Readiness Index design](docs/deployment_readiness_index_design.md)
- [Phase 3C sign-off](docs/phase3c_signoff.md)
- [Paper Methods draft](docs/paper_methods_draft.md)
- [Current stage completion checklist](docs/current_stage_completion_checklist.md)
- [Repository status matrix](docs/repository_status_matrix.md)
- [Reviewer notes](docs/reviewer_notes.md)
- [Data directory guide](data/README.md)
- [Final reviewer improvement prompts](docs/final_cursor_improvement_prompts_construction_robot.md)
- [Phase 3B sign-off](docs/phase3b_signoff.md)
- [Readiness review](reports/current_stage_readiness_review.md) — label: **reviewer_ready_with_limitations**
- [Reviewer readiness report](reports/reviewer_readiness_report.md)
- [Prompts execution status](reports/prompts_execution_status.md)

---

## License

MIT License — see [`LICENSE`](LICENSE). Cite via [`CITATION.cff`](CITATION.cff).

Video sources remain subject to platform terms. Manufacturer specifications are **manufacturer-reported (E3)** and not independently verified field data.
