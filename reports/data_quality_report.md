# Data Quality Report

**Status:** Stage 1 approved (2026-06-27). Stage 2 GAN seed conversion **complete** (2026-06-28).

> The dataset is a secondary observational dataset derived from publicly available videos and manufacturer-reported specifications. It is not direct field-measured productivity data.

## Row counts

| File | Rows |
|------|------|
| video_metadata.csv | 32 |
| video_segments.csv | 46 |
| robot_video_observations.csv | 11 |
| mivan_video_observations.csv | 30 |
| cleaned_video_dataset.csv | 17 |
| gan_seed_dataset.csv | 14 |
| synthetic_scenario_dataset.csv | 50 |
| synthetic_scenario_dataset_gan.csv | 50 |
| synthetic_scenario_dataset_all.csv | 100 |
| manufacturer_specs.csv | 10 |

## Summary metrics

- Unique videos in registry: 32
- Structured-extraction videos: 16
- Qualitative-only / pool sources: 8
- Excluded videos: 4
- Robot observations: 11
- Mivan observations: 30
- Manufacturer spec records: 10
- Cleaned modelling subset rows: 17
- GAN seed records: 14
- Synthetic scenario records (rule): 50
- Synthetic scenario records (GAN pilot): 50
- Synthetic scenario records (combined): 100
- Cleaned rows promoted to modelling_ready: 14

## Evidence-level distribution (observations)

**Robot:** E1: 1, E2: 10

**Mivan:** E1: 7, E2: 23

## Source-type distribution

**Robot:** video_estimated: 10, video_observed: 1

**Cleaned:** video_estimated: 11, video_observed: 6

## Coding-confidence distribution

**Robot:** medium: 11

**Mivan:** high: 6, low: 2, medium: 22

## Duration validity

**Segments:** invalid: 46

**usable_for_productivity=yes count:** 0 (should be 0)

## Duplicate / parallel controls

- Videos flagged duplicate/parallel: 3
- Duplicate groups: 2

## Robot manufacturer distribution

- Bright Dream: 1
- BrightMaster: 19
- unknown: 2

## Activity taxonomy distribution

**Robot activity types:**
- concrete_leveling: 3
- floor_grinding: 4
- layout_marking: 1
- post_cast_coating: 3

**Mivan activity types:**
- MEP: 2
- concrete_pour: 3
- finishing: 5
- formwork: 15
- rebar: 4
- stripping: 1

## Missing-value summary (key fields)

**robot:** evidence_level missing=0, source_type missing=0, data_use missing=0
**mivan:** evidence_level missing=0, access_condition missing=0
**cleaned:** evidence_level missing=0, data_use missing=0, access_condition missing=0

## Modelling readiness

- modelling_ready cleaned rows: 14
- Not promoted (structured_coding / qualitative_only): 3
- Seed records (independent sample only): 14
- Invalid-duration segments: 46
- usable_for_productivity=yes count: 0 (should be 0)

## GAN seed dataset

- Mivan seeds: 7
- Robot seeds: 7
- All seeds duration_excluded=yes: True

## Synthetic scenario dataset (Phase 3.1)

- Rule-expanded scenarios: 50
- All is_synthetic=yes: True
- SF-DEPLOYMENT-JOINT: 10
- SF-MIVAN-SLAB-CYCLE: 16
- SF-ROBOT-FRESH-CONCRETE: 16
- SF-ROBOT-POST-CAST: 8

## Stage completion

- Stage 1 sign-off: `docs/stage1_signoff.md`
- Stage 2 seed conversion: `docs/stage2_signoff.md`
- Phase 3.1 rule expansion: `reports/synthetic_expansion_report.md`
- Phase 3B tabular GAN pilot: `reports/tabular_gan_pilot_report.md`
- Robot source candidates: 4 deferred to optional expansion

## Optional future expansion

- Additional comparison robots (Floor Master, Kajima, rebar tying, inspection)
- Field validation before quantitative deployment-readiness claims
