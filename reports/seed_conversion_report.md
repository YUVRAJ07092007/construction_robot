# GAN Seed Conversion Report

**Generated:** 2026-06-28 by `src/convert_gan_seed.py`

> Seed records are normalized from approved Stage 1 observations. They are **not** synthetic GAN outputs and **exclude** video durations as productivity targets.

## Summary

- Cleaned rows reviewed: 17
- Seed records produced: 14
- Excluded from seed set: 3
- Mivan seeds: 7
- Robot seeds: 7
- BrightMaster robot seeds: 6
- Bright Dream comparison seeds: 1

## Promotion rules applied

- `independent_sample=yes`
- Not flagged duplicate/parallel
- `data_use` structured_coding (promoted to framework_seed_ready)
- `coding_confidence` medium or high
- Evidence E1 or E2 only
- `usable_for_productivity=no` enforced

## Seed records

| seed_id | source_observation_id | category | activity_group | workflow_stage |
|---------|----------------------|----------|----------------|----------------|
| SEED-001 | OBS-M01-003 | mivan | formwork_work | pre-pour |
| SEED-002 | OBS-M02-005 | mivan | formwork_work | pre-pour |
| SEED-003 | OBS-M02-009 | mivan | mep_conduit_work | pre-pour |
| SEED-004 | OBS-M02-010 | mivan | concrete_pouring | pour |
| SEED-005 | OBS-M02-013 | mivan | formwork_work | post-cast |
| SEED-006 | OBS-R02-001 | robot | fresh_concrete_leveling | pour |
| SEED-007 | OBS-R05-001 | robot | post_cast_coating | post-cast |
| SEED-008 | OBS-R06-001 | robot | post_cast_floor_grinding | post-cast |
| SEED-009 | OBS-M03-002 | mivan | formwork_work | pre-pour |
| SEED-010 | OBS-R09-001 | robot | fresh_concrete_leveling | pour |
| SEED-011 | OBS-R10-001 | robot | post_cast_floor_grinding | post-cast |
| SEED-012 | OBS-R15-001 | robot | layout_marking | pre-pour |
| SEED-013 | OBS-M06-001 | mivan | post_cast_surface_preparation | post-cast |
| SEED-014 | OBS-R22-001 | robot | fresh_concrete_leveling | pour |

## Excluded rows

| observation_id | reason |
|----------------|--------|
| OBS-M01-005 | not_independent_sample |
| OBS-M01-008 | not_independent_sample |
| OBS-M05-003 | not_independent_sample |

## Output files

- `data/gan_seed_dataset.csv` — GAN-ready seed feature table
- `data/cleaned_video_dataset.csv` — promoted rows marked `framework_seed_ready`

## Research-safe note

Seed conversion prepares feature vectors for **future** synthetic scenario generation. No GAN training or synthetic record generation is performed in this step.
