# Algorithm for Extraction of Suitable Data from Construction Robot and Mivan Construction Videos

## Algorithm Title

**Video-Informed Task-Level Data Extraction Algorithm for Construction Robot Deployment Readiness Assessment**

---

## Objective

The objective of this algorithm is to extract suitable, structured, and research-usable data from publicly available videos of construction robots and Mivan / aluminium formwork construction. The extracted data will be used later for seed dataset creation, synthetic scenario generation, and construction robot deployment readiness assessment.

The algorithm does not treat video data as direct field-measured productivity data. Instead, the videos are used as secondary observational sources for extracting visible task-level parameters, workflow characteristics, work-zone conditions, and robot-operation features.

---

## Input

- List of construction robot video URLs
- List of Mivan / aluminium formwork construction video URLs
- Video source details such as title, platform, channel name, and access date
- Predefined video suitability criteria
- Predefined coding variables for robot and Mivan construction activities

---

## Output

- Video metadata table
- Usable video segment table
- Robot-operation observation dataset
- Mivan-construction observation dataset
- Cleaned video-derived dataset suitable for further research modelling

---

## Step 1: Create Video Registry

For each selected video, create a video registry entry.

### Data to Record

| Field | Description |
|---|---|
| video_id | Unique video identification number |
| video_url | Source link of the video |
| video_category | Robot / Mivan / mixed / other |
| platform | YouTube / Facebook / manufacturer website / other |
| title | Title of the video |
| source_name | Channel name or uploader name |
| access_date | Date on which the video was accessed |
| activity_focus | Concrete leveling, finishing, rebar, formwork, slab cycle, etc. |
| construction_context | High-rise slab, indoor floor, open slab, podium, basement, etc. |
| total_video_duration | Full duration of the video |
| visibility_quality | High / medium / low |
| coding_confidence | High / medium / low |
| inclusion_status | Include / partial use / exclude |

---

## Step 2: Screen Video Suitability

Each video should be screened before detailed data extraction.

### Suitability Criteria

| Criterion | Score |
|---|---|
| Relevance to construction robot or Mivan construction | 0–2 |
| Clarity of visual content | 0–2 |
| Continuity of construction activity | 0–2 |
| Ability to identify the activity type | 0–2 |
| Ability to observe labour, robot, or work-zone interaction | 0–2 |
| Low editing / low promotional interruption | 0–2 |
| Suitability for parameter extraction | 0–2 |

Maximum score = **14**

### Suitability Classification

| Score | Classification | Use |
|---|---|---|
| 0–5 | Low suitability | Exclude |
| 6–9 | Medium suitability | Use only for qualitative workflow understanding |
| 10–14 | High suitability | Use for structured data extraction |

---

## Step 3: Identify Usable Video Segments

A complete video should not be coded as one unit. Instead, divide it into usable activity segments.

A **usable segment** is a continuous part of the video where one activity is clearly visible.

### Segment-Level Data

| Field | Description |
|---|---|
| segment_id | Unique segment number |
| video_id | Parent video ID |
| start_time | Segment start timestamp |
| end_time | Segment end timestamp |
| segment_duration | Duration of the selected segment |
| activity_type | Activity visible in the segment |
| segment_category | Robot operation / Mivan workflow |
| segment_quality | High / medium / low |
| duration_validity | Valid / invalid for time observation |
| reason_for_rejection | If segment is rejected |

Reject a segment if:

- activity is unclear;
- video is heavily edited;
- view is obstructed;
- activity duration is too short;
- no useful parameter can be extracted;
- the clip is time-lapsed or jump-cut for timing purposes.

---

## Step 4: Extract Robot-Operation Data

For videos showing construction robots, extract only visible and classifiable parameters.

### Robot-Side Parameters

| Parameter | Type | Description |
|---|---|---|
| robot_activity_type | Categorical | Leveling / finishing / grinding / inspection / other |
| operating_surface | Categorical | Wet concrete / hardened concrete / slab / indoor floor / unknown |
| movement_pattern | Categorical | Linear / grid-based / guided / edge-following / random / unknown |
| guidance_mode | Categorical | Manual / remote-controlled / autonomous / unknown |
| operator_count_visible | Integer | Number of visible robot operators |
| assistant_count_visible | Integer | Number of visible assistants |
| setup_visible | Yes/No | Whether setup activity is visible |
| setup_complexity | Ordinal | Low / medium / high |
| operational_continuity | Ordinal | Continuous / semi-continuous / interrupted |
| interruption_count | Integer | Number of visible interruptions |
| obstacle_presence | Yes/No | Whether obstacles are visible |
| human_robot_separation | Ordinal | Low / medium / high |
| safety_condition | Ordinal | Poor / moderate / good |
| edge_condition | Categorical | Protected edge / open edge / not visible |
| robot_transport_requirement | Categorical | Manual / lift / crane / unknown |
| task_duration_observed | Numeric | Duration of visible activity segment |
| duration_validity | Valid / invalid | Whether duration can be used as observed segment time |
| coding_confidence | Ordinal | Low / medium / high |

---

## Step 5: Extract Mivan / Aluminium Formwork Construction Data

For videos showing Mivan or aluminium formwork construction, extract workflow and site-condition parameters.

### Mivan-Side Parameters

| Parameter | Type | Description |
|---|---|---|
| slab_activity_type | Categorical | Formwork / rebar / MEP / concrete pour / leveling / finishing / stripping |
| floor_cycle_stage | Categorical | Pre-pour / pour / finishing / post-cast |
| labour_count_visible | Integer | Number of visible workers in active work zone |
| min_visible_labour | Integer | Minimum visible labour count |
| max_visible_labour | Integer | Maximum visible labour count |
| dominant_visible_labour | Integer | Most frequently visible labour count |
| congestion_level | Ordinal | Low / medium / high |
| reinforcement_complexity | Ordinal | Low / medium / high |
| conduit_presence | Ordinal | Low / medium / high / unknown |
| slab_opening_presence | Yes/No/Unknown | Visible openings in slab |
| access_condition | Ordinal | Open / partially restricted / congested |
| material_movement_method | Categorical | Manual / pump / crane / mixed / unknown |
| pour_sequence | Categorical | Continuous / segmented / delayed / interrupted / unknown |
| surface_condition | Categorical | Pre-pour / wet concrete / partially finished / hardened / finished |
| safety_exposure | Ordinal | Low / medium / high |
| edge_protection_visible | Yes/No/Unknown | Whether edge protection is visible |
| workflow_sequence | Text/Categorical | Observed order of activity |
| task_duration_observed | Numeric | Duration of visible segment |
| duration_validity | Valid / invalid | Whether duration is usable |
| coding_confidence | Ordinal | Low / medium / high |

---

## Step 6: Assign Evidence Level to Each Extracted Variable

Every extracted value must be labelled according to its evidence level.

### Evidence-Level Classification

| Evidence Level | Meaning |
|---|---|
| E1 | Directly visible from video |
| E2 | Visually estimated from video |
| E3 | Taken from manufacturer-reported specification |
| E4 | Computed from extracted data |
| E5 | Assumption-based value |

For the video extraction stage, use mainly **E1** and **E2**.

### Examples

| Variable | Evidence Level |
|---|---|
| visible operator count | E1 |
| movement pattern | E1 or E2 |
| congestion level | E2 |
| reinforcement complexity | E2 |
| task duration from continuous segment | E1 |
| actual productivity | Not extracted unless independently verified |

---

## Step 7: Assign Confidence Score

Each extracted record should have a confidence score.

### Confidence Classification

| Confidence Level | Meaning |
|---|---|
| High | Clear video, activity visible, low ambiguity |
| Medium | Partially clear, some estimation required |
| Low | Unclear, obstructed, or uncertain |

Low-confidence records should not be used for quantitative modelling unless clearly marked.

---

## Step 8: Apply Logical Consistency Rules

After extraction, apply construction logic filters.

### Logic Rules

1. If `activity_type = rebar tying`, then `floor_cycle_stage` should be `pre-pour`.
2. If `activity_type = concrete leveling`, then `surface_condition` should be `wet concrete`.
3. If `activity_type = floor grinding`, then `surface_condition` should be `hardened concrete`.
4. If `congestion_level = high`, then `site_access_condition` should not be marked as fully open.
5. If `safety_exposure = high`, then `safety_condition` should not be marked as good unless justified.
6. If the video is time-lapsed or edited, `duration_validity` should be marked as invalid.
7. If `visibility_quality = low`, the segment should not be used for structured quantitative extraction.
8. If robot activity is not clearly visible, robot-specific variables should be marked as unknown, not guessed.

---

## Step 9: Generate Clean Video-Derived Dataset

After coding and logical checking, generate the final cleaned dataset.

### Final Dataset Columns

| Column | Description |
|---|---|
| observation_id | Unique observation ID |
| video_id | Parent video ID |
| segment_id | Segment ID |
| video_category | Robot / Mivan |
| activity_type | Observed activity |
| workflow_stage | Pre-pour / pour / finishing / post-cast |
| labour_count_visible | Visible labour count |
| robot_operator_count | Visible robot operator count |
| movement_pattern | Robot movement pattern |
| operating_surface | Working surface |
| congestion_level | Low / medium / high |
| reinforcement_complexity | Low / medium / high |
| access_condition | Open / restricted / congested |
| safety_condition | Poor / moderate / good |
| task_duration_observed | Observed duration |
| duration_validity | Valid / invalid |
| evidence_level | E1 / E2 / E3 / E4 / E5 |
| coding_confidence | Low / medium / high |
| source_type | Video-observed / video-estimated / manufacturer-reported / computed / assumption-based |

---

## Step 10: Export Dataset for Further Research Use

Export the extracted data into separate files.

### Recommended Output Files

| File Name | Purpose |
|---|---|
| video_metadata.csv | Stores video registry and suitability score |
| video_segments.csv | Stores usable video segment details |
| robot_video_observations.csv | Stores robot-side extracted data |
| mivan_video_observations.csv | Stores Mivan-side extracted data |
| cleaned_video_dataset.csv | Final cleaned dataset for research modelling |

---

# Consolidated Pseudocode

```text
Algorithm: Video-Informed Task-Level Data Extraction

Input:
    Robot video URLs
    Mivan construction video URLs
    Suitability criteria
    Coding variable dictionary

Output:
    Cleaned video-derived dataset

Steps:

1. Initialize video metadata table.

2. For each video:
       Record video URL, title, platform, source, access date and category.

3. For each video:
       Score suitability using relevance, visibility, continuity,
       activity identifiability, interaction visibility, editing level,
       and parameter measurability.

4. If suitability score is low:
       Exclude video.
   Else if suitability score is medium:
       Use only for qualitative workflow mapping.
   Else:
       Select for structured data extraction.

5. For each selected video:
       Divide video into usable activity segments.
       Record start time, end time, segment duration and activity type.

6. For each robot-operation segment:
       Extract robot activity type, operating surface, movement pattern,
       guidance mode, operator count, setup visibility, interruption count,
       obstacle presence, safety condition and human–robot separation.

7. For each Mivan-construction segment:
       Extract slab activity type, floor-cycle stage, visible labour count,
       congestion level, reinforcement complexity, access condition,
       material movement method, surface condition and safety exposure.

8. For each extracted variable:
       Assign evidence level:
           E1 = directly visible
           E2 = visually estimated
           E3 = manufacturer-reported
           E4 = computed
           E5 = assumption-based

9. For each extracted observation:
       Assign coding confidence:
           High, Medium or Low.

10. Apply logical consistency rules:
       Remove or flag impossible combinations such as:
           rebar tying after concrete finishing,
           concrete leveling on hardened surface,
           floor grinding on wet concrete,
           high congestion with fully open access,
           edited video segment used as valid timing data.

11. Remove low-quality records or mark them as qualitative only.

12. Export:
       video_metadata.csv
       video_segments.csv
       robot_video_observations.csv
       mivan_video_observations.csv
       cleaned_video_dataset.csv
```

---

# Research-Safe Statement

The extracted dataset should be described in the paper as follows:

> The video-derived dataset was generated through a structured observational coding process applied to publicly available construction robotics and aluminium formwork construction videos. Only visible or reasonably classifiable parameters were extracted. Each extracted value was assigned an evidence level and confidence score. The resulting dataset was used as a secondary observational dataset for framework development and subsequent scenario modelling, not as direct field-measured productivity evidence.

---

# Note for Next Stage

This is the **first-stage algorithm** for video data extraction only.

After this algorithm is finalized, the next algorithm should be for:

**Cleaning and converting the extracted dataset into GAN-ready seed data.**
