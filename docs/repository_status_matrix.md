# Repository Status Matrix

**Last updated:** 2026-06-28  
**Purpose:** Single source of truth for stage status across README, reports, and methods draft.

> This repository supports a video-informed, robot-agnostic data extraction and scenario-modelling framework for construction robot deployment readiness assessment in aluminium formwork-based high-rise building construction. The extracted data are secondary observational records derived from public videos, manufacturer-reported specifications, and structured coding rules. The dataset is intended for framework development and scenario exploration, not for claiming verified real-site productivity or field performance.

---

## Stage matrix

| Stage | Output files | Current status | Evidence level | Safe claim | Not allowed claim |
|-------|--------------|----------------|----------------|------------|-------------------|
| 1. Video source identification | `data/video_metadata.csv`, `data/robot_source_candidates.csv` | **pilot_complete** | E1–E3 registry | Curated public sources screened for Mivan/robot relevance | Complete global robot coverage |
| 2. Video suitability screening | `data/video_metadata.csv` (suitability fields) | **pilot_complete** | Rubric-scored | Structured-extraction subset identified | All videos equally reliable |
| 3. Segment-level video coding | `data/video_segments.csv`, observation CSVs | **pilot_complete** | E1/E2 video-derived | Task-level parameters coded from visible footage | Field-measured productivity |
| 4. Cleaned video-derived dataset | `data/cleaned_video_dataset.csv` | **pilot_complete** | E1/E2 | Pilot video-derived dataset for framework seeds | Empirical performance dataset |
| 5. GAN-ready seed dataset | `data/gan_seed_dataset.csv`, `data/modelling_feature_matrix.csv` | **seed_ready** | Encoded E1/E2 features | 14 independent framework seeds prepared | Statistically representative sample |
| 6. Rule-based scenario expansion | `data/synthetic_scenario_dataset.csv` | **pilot_complete** | Computed / synthetic | 50 constraint-filtered pilot scenarios | Observed site data |
| 7. CTGAN/TVAE pilot generation | `data/synthetic_scenario_dataset_gan.csv` | **pilot_complete** | Synthetic pilot | Stress-test framework logic with generative pilot (n=14 training) | Robust GAN augmentation |
| 8. Deployment Readiness Index | `data/dri_scored_scenarios.csv`, `config/dri_framework_config.yaml` | **framework_demo_complete** | Computed scenario-relative | Scenario-relative ranking demonstration | Field-validated readiness |
| 9. Techno-economic assessment | — | **not_started** | — | — | Cost/benefit claims without data |
| 10. Future field validation | — | **future_work** | — | Planned independent validation | Substitute for current pilot |

---

## Readiness labels

| Label | Meaning |
|-------|---------|
| `ongoing` | Active extraction or review in progress |
| `pilot_complete` | Demonstration outputs exist; not final empirical corpus |
| `framework_demo_complete` | Scoring/design logic demonstrated on pilot data |
| `seed_ready` | Seeds validated for framework use |
| `not_started` | No outputs yet |
| `future_work` | Explicitly out of scope for current repo |

**Current repository label:** `reviewer_ready_with_limitations`

---

## Data-type legend

| Type | Examples | Use |
|------|----------|-----|
| Observed (video) | Robot/Mivan observations | Framework coding, qualitative patterns |
| Manufacturer-reported (E3) | `manufacturer_specs.csv` | Context, range framing — not field evidence |
| Seed (encoded) | `gan_seed_dataset.csv` | Feature inputs for scenario modelling |
| Rule-synthetic | `synthetic_scenario_dataset.csv` | Pilot scenario exploration |
| GAN/TVAE-synthetic | `synthetic_scenario_dataset_gan.csv` | Pilot-only; not for statistical inference |
| Computed | DRI scores | Scenario-relative ranking only |

---

## Terminology (consistent across docs)

| Avoid | Use instead |
|-------|-------------|
| complete dataset | pilot video-derived dataset |
| framework_seed_ready | framework_seed_ready |
| GAN dataset complete | GAN/TVAE pilot scenario generation complete |
| validates robot deployment | demonstrates framework logic |
| final readiness score | scenario-relative readiness score |

---

## Related documents

- [`cursor_repo_improvement_prompts_for_journal_reviewers.md`](cursor_repo_improvement_prompts_for_journal_reviewers.md)
- [`reviewer_notes.md`](reviewer_notes.md)
- [`../reports/reviewer_readiness_report.md`](../reports/reviewer_readiness_report.md)
