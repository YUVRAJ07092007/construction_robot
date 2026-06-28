# Data Quality Report

**Status:** Video data extraction is **ongoing**. This report describes the current snapshot only.

> The dataset is a secondary observational dataset derived from publicly available videos and manufacturer-reported specifications. It is not direct field-measured productivity data.

## Row counts

| File | Rows |
|------|------|
| video_metadata.csv | 31 |
| video_segments.csv | 45 |
| robot_video_observations.csv | 10 |
| mivan_video_observations.csv | 30 |
| cleaned_video_dataset.csv | 16 |
| manufacturer_specs.csv | 10 |

## Summary metrics

- Unique videos in registry: 31
- Structured-extraction videos: 15
- Qualitative-only / pool sources: 8
- Excluded videos: 4
- Robot observations: 10
- Mivan observations: 30
- Manufacturer spec records: 10
- Cleaned modelling subset rows: 16

## Evidence-level distribution (observations)

**Robot:** E1: 1, E2: 9

**Mivan:** E1: 7, E2: 23

## Source-type distribution

**Robot:** video_estimated: 9, video_observed: 1

**Cleaned:** video-estimated: 10, video-observed: 6

## Coding-confidence distribution

**Robot:** medium: 10

**Mivan:** high: 6, low: 2, medium: 22

## Duration validity

**Segments:** invalid: 45

**usable_for_productivity=yes count:** 0 (should be 0)

## Duplicate / parallel controls

- Videos flagged duplicate/parallel: 4
- Duplicate groups: 2

## Robot manufacturer distribution

- BrightMaster: 19
- unknown: 2

## Activity taxonomy distribution

**Robot activity types:**
- concrete_leveling: 2
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

- Cleaned rows not marked modelling_ready or with productivity blocked: 16
- Invalid-duration segments: 45

## Extraction gaps (priority)

- Expand robot-agnostic comparison sources beyond BrightMaster
- Add more independent fresh-concrete leveling observations from verified sources
- Continue Mivan playlist screening only where workflow adds non-duplicate value
- Re-screen low-confidence or excluded sources before any modelling_ready promotion
