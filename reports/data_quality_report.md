# Data Quality Report

**Status:** Stage 1 video data extraction is **complete** (pending human review). This report describes the final Stage 1 snapshot.

> The dataset is a secondary observational dataset derived from publicly available videos and manufacturer-reported specifications. It is not direct field-measured productivity data.

## Row counts

| File | Rows |
|------|------|
| video_metadata.csv | 32 |
| video_segments.csv | 46 |
| robot_video_observations.csv | 11 |
| mivan_video_observations.csv | 30 |
| cleaned_video_dataset.csv | 17 |
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

## Records not suitable for modelling

- Cleaned rows not marked modelling_ready or with productivity blocked: 17
- Invalid-duration segments: 46

## Stage 1 completion

- All priority sources screened (no `pending_screening` in registry)
- All structured-extraction videos segmented and coded
- Robot source candidates: 4 screened, 4 deferred to post-Stage-1 expansion
- Validation passing; awaiting human review sign-off before Stage 2

## Optional future expansion (not in Stage 1 scope)

- Additional comparison robots (Floor Master, Kajima, rebar tying, inspection)
- More independent fresh-concrete leveling observations from verified sources
- Mivan playlist entries only where workflow adds non-duplicate value
- Re-screen low-confidence or excluded sources before any modelling_ready promotion
