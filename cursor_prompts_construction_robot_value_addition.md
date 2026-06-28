# Cursor AI Prompt File: Value Addition for Construction Robot Video Data Extraction Repository

## Repository Context

GitHub repository: `YUVRAJ07092007/construction_robot`

Research direction:

**Video-informed and robot-agnostic data extraction framework for assessing construction robot deployment readiness in aluminium formwork-based high-rise building construction, commonly known in India as Mivan construction.**

The work is currently at the **data extraction stage**. Data extraction is ongoing and not complete. The immediate objective is to strengthen the quality, logic, traceability, and research-readiness of the extracted video-derived dataset.

The repository already contains a structure similar to:

```text
construction_robot/
├── config/
├── data/
├── scripts/
├── src/
├── brightmaster_mivan_video_links_suitability_review.md
└── video_informed_task_level_data_extraction_algorithm.md
```

The `data/` folder contains CSV files such as:

```text
video_metadata.csv
video_segments.csv
robot_video_observations.csv
mivan_video_observations.csv
cleaned_video_dataset.csv
manufacturer_specs.csv
```

The work must remain **robot-agnostic**. BrightMaster Robotics is only one source. Similar construction robots from other companies must also be allowed.

---

# Global Instructions for Cursor AI

Use these instructions for all prompts below.

## Main Goal

Improve the repository so that the extracted data becomes more logical, consistent, transparent, reproducible, and suitable for a research article in the **Journal of Building Engineering**.

## Do Not Do

Do not generate GAN data at this stage.

Do not create final Robot Deployment Readiness Index results at this stage.

Do not claim real-site validation.

Do not claim productivity improvement from public videos.

Do not treat manufacturer-reported specifications as independently verified field data.

Do not make the study BrightMaster-specific.

Do not delete existing useful data unless clearly invalid; prefer flagging, annotating, or moving to a qualitative-only category.

## Mandatory Research-Safe Principles

1. Public videos are secondary observational sources only.
2. Video-derived duration is not productivity unless the segment is continuous and clearly valid.
3. Manufacturer data must remain separate and marked as manufacturer-reported.
4. Each extracted value must have an evidence level.
5. Each observation must have a coding confidence level.
6. Similar robots from any manufacturer are valid if they are relevant to construction tasks.
7. Duplicate or parallel videos must not inflate independent sample counts.
8. Low-confidence records should remain qualitative-only unless corrected.
9. All schema changes must be backward-compatible where possible.

---

# Evidence-Level System

Use the following evidence levels consistently:

| Evidence Level | Meaning |
|---|---|
| E1 | Directly visible from video |
| E2 | Visually estimated from video |
| E3 | Manufacturer-reported specification or claim |
| E4 | Computed from extracted data |
| E5 | Assumption-based scenario value |

At the current extraction stage, most video observations should be **E1** or **E2**. Manufacturer specifications should be **E3**.

---

# Source-Type System

Use the following `source_type` values consistently:

| source_type | Meaning |
|---|---|
| video_observed | Directly visible in video |
| video_estimated | Estimated from video |
| manufacturer_reported | Product page, brochure, case page, company claim |
| computed | Calculated from other fields |
| assumption_based | Used only for later scenario modelling |
| literature_reported | Extracted from academic, standard, or industry literature |
| project_document_derived | Derived from project drawings, schedule, or anonymized documents |

---

# Data-Use System

Add or validate the column `data_use` where appropriate.

| data_use | Meaning |
|---|---|
| exclude | Not suitable for research use |
| qualitative_only | Useful for workflow understanding only |
| structured_coding | Suitable for structured extraction |
| modelling_ready | Suitable for future seed dataset use after validation |

At present, be conservative. Do not mark records as `modelling_ready` unless they pass schema, logic, confidence, and provenance checks.

---

# Prompt 1: Repository Audit Without Editing

## Cursor Prompt

Review the full repository structure and all CSV files under `data/`, plus all Python files under `src/`, `scripts/`, and all configuration files under `config/`.

Do not edit anything in this step.

Produce a concise audit report in `reports/repo_audit_report.md` with the following sections:

1. Current folder structure.
2. List of all data files and row counts.
3. List of all Python scripts and their purpose.
4. Existing schema columns in each CSV.
5. Missing or inconsistent columns.
6. Duplicate or parallel video/sample risks.
7. Duration-validity risks.
8. Manufacturer-data separation risks.
9. Robot-agnostic coverage status.
10. Priority fixes required before further extraction.

Acceptance criteria:

- The report must clearly say that extraction is ongoing.
- The report must not judge the dataset as final.
- The report must distinguish data quality issues from research-design issues.
- No files except `reports/repo_audit_report.md` should be changed.

---

# Prompt 2: Create a Central Data Dictionary

## Cursor Prompt

Create a central data dictionary file at:

```text
config/data_dictionary.yaml
```

The dictionary must define all accepted columns for the following files:

```text
video_metadata.csv
video_segments.csv
robot_video_observations.csv
mivan_video_observations.csv
manufacturer_specs.csv
cleaned_video_dataset.csv
```

For each column, include:

```yaml
column_name:
  description:
  data_type:
  allowed_values:
  required: true/false
  evidence_level_required: true/false
  notes:
```

The dictionary must include and standardize these important columns wherever relevant:

```text
video_id
segment_id
observation_id
video_category
manufacturer_name
robot_brand
robot_model
activity_type
source_type
evidence_level
coding_confidence
data_use
independent_sample
duration_validity
duration_validity_reason
is_duplicate_or_parallel
duplicate_group_id
```

Acceptance criteria:

- BrightMaster must not be hard-coded as the only robot manufacturer.
- Similar robots from other companies must be supported.
- Unknown values should be allowed as `unknown`, not blank.
- The file must be human-readable and suitable for validation scripts.

---

# Prompt 3: Standardize Robot-Agnostic Metadata Fields

## Cursor Prompt

Update the data schema and existing CSV files so the repository supports a robot-agnostic study.

Add or validate the following columns in `video_metadata.csv`, `robot_video_observations.csv`, and `manufacturer_specs.csv` where relevant:

```text
manufacturer_name
robot_brand
robot_model
robot_category
robot_activity_group
manufacturer_verified
comparison_robot
```

Use the following rules:

1. `manufacturer_name` may be BrightMaster, Bright Dream, Floor Master, Kajima, unknown, or any other manufacturer.
2. `robot_category` should use values such as:
   - concrete_leveling_robot
   - concrete_finishing_robot
   - floor_grinding_robot
   - rebar_tying_robot
   - layout_robot
   - inspection_robot
   - coating_robot
   - other
3. `comparison_robot = yes` means the robot is not BrightMaster but is relevant for comparison.
4. `manufacturer_verified = yes/no/unknown` must be used to avoid unclear claims.
5. Do not remove existing BrightMaster entries.

Acceptance criteria:

- The dataset must no longer appear BrightMaster-only.
- Unverified robots must be clearly marked.
- Related but unverified videos must not be treated as manufacturer-confirmed BrightMaster data.

---

# Prompt 4: Improve Activity Label Taxonomy

## Cursor Prompt

Review all activity labels in:

```text
robot_video_observations.csv
mivan_video_observations.csv
cleaned_video_dataset.csv
```

Create a standardized taxonomy file:

```text
config/activity_taxonomy.yaml
```

Use separate labels for fresh-concrete activities and post-cast activities.

Recommended activity groups:

```text
rebar_work
formwork_work
mep_conduit_work
concrete_pouring
fresh_concrete_leveling
fresh_concrete_finishing
post_cast_floor_grinding
post_cast_surface_preparation
post_cast_coating
layout_marking
inspection
robot_transport_setup
other
unknown
```

Update CSV activity labels only where the correction is clearly justified.

Important correction principle:

Do not label indoor coating or hardened-surface finishing as fresh concrete finishing.

Acceptance criteria:

- Fresh concrete finishing and post-cast finishing/coating/grinding must be separated.
- No original record should lose traceability.
- If a label is changed, add or update a field `label_revision_note`.
- Keep uncertain labels as `unknown` or `other`, not guessed.

---

# Prompt 5: Strengthen Video Suitability Scoring

## Cursor Prompt

Update or create the suitability scoring logic in the config and validation code.

Use a 14-point scoring system:

| Criterion | Score |
|---|---|
| construction_relevance | 0–2 |
| visual_clarity | 0–2 |
| activity_continuity | 0–2 |
| activity_identifiability | 0–2 |
| interaction_visibility | 0–2 |
| low_editing_level | 0–2 |
| parameter_extractability | 0–2 |

Classification:

```text
0–5    = exclude
6–9    = qualitative_only
10–14  = structured_coding
```

Tasks:

1. Add these fields to `video_metadata.csv` if missing.
2. Add computed field `suitability_score`.
3. Add computed field `data_use`.
4. Ensure videos with low scores are not used for structured extraction.
5. Ensure medium-score videos are allowed only for qualitative workflow mapping.

Acceptance criteria:

- The scoring system must be explicit and reproducible.
- Manual override must be possible using `manual_data_use_override` and `override_reason`.
- No video should silently move from excluded to structured use.

---

# Prompt 6: Improve Duration Validity Logic

## Cursor Prompt

Review `video_segments.csv`, `robot_video_observations.csv`, `mivan_video_observations.csv`, and `cleaned_video_dataset.csv`.

Rename or add duration-related columns so there is no confusion between visible segment time and actual productivity time.

Use the following standard fields:

```text
visible_segment_duration_sec
duration_validity
duration_validity_reason
continuous_unedited_segment
time_lapse_or_jump_cut
usable_for_productivity
```

Rules:

1. If a segment is edited, time-lapsed, promotional, narrated montage, or jump-cut, then:
   - `duration_validity = invalid`
   - `usable_for_productivity = no`
2. If a segment is continuous and unedited:
   - `duration_validity = valid_for_visible_segment_only`
   - `usable_for_productivity = no`, unless independently verified
3. Public videos should almost never be marked as `usable_for_productivity = yes`.

Acceptance criteria:

- No invalid duration should be used for productivity modelling.
- Existing duration values should be retained as visible segment durations.
- Add notes explaining why duration is valid or invalid.

---

# Prompt 7: Add Duplicate and Independent-Sample Controls

## Cursor Prompt

Add duplicate/parallel-source controls to all relevant CSV files.

Add these fields where appropriate:

```text
is_duplicate_or_parallel
duplicate_group_id
independent_sample
parallel_source_note
```

Rules:

1. If two videos show the same or parallel construction workflow, mark them with the same `duplicate_group_id`.
2. Only one record in each duplicate group should be marked `independent_sample = yes`.
3. Parallel videos may be used for cross-checking but not for inflating sample counts.
4. Keep all records; do not delete parallel entries unless they are unusable.

Acceptance criteria:

- Duplicate risk must be visible in the data.
- Future analysis can filter by `independent_sample = yes`.
- Notes must explain the reason for duplicate or parallel classification.

---

# Prompt 8: Upgrade Validation Script

## Cursor Prompt

Improve or create the validation script at:

```text
src/validate_extractions.py
```

The script must validate:

1. Required columns exist.
2. Allowed values are respected.
3. Evidence levels are valid.
4. Source types are valid.
5. Duration validity rules are followed.
6. Activity labels match `config/activity_taxonomy.yaml`.
7. Manufacturer data is not mixed with video-observed data.
8. Duplicate controls are present.
9. Low-confidence records are not marked modelling-ready.
10. Logical construction rules are respected.

Include these construction logic checks:

```text
rebar_work must be pre-pour
concrete_pouring must be pour stage
fresh_concrete_leveling must be on wet concrete
fresh_concrete_finishing must be on wet or partially finished concrete
post_cast_floor_grinding must be on hardened concrete
post_cast_coating must not be treated as fresh concrete finishing
high congestion should not be paired with fully open access without note
high safety exposure should not be paired with good safety condition without note
```

Script output:

```text
reports/validation_report.md
reports/validation_issues.csv
```

Acceptance criteria:

- Validation must not silently modify data.
- It should report errors, warnings, and suggestions separately.
- It should exit with non-zero status only for critical schema or logic errors.
- It should be runnable using:
  python src/validate_extractions.py

---

# Prompt 9: Create a Data Quality Report Generator

## Cursor Prompt

Create a script:

```text
src/generate_data_quality_report.py
```

The script should read all CSV files under `data/` and create:

```text
reports/data_quality_report.md
```

The report must include:

1. Row count per file.
2. Number of robot observations.
3. Number of Mivan observations.
4. Number of manufacturer-spec records.
5. Number of unique videos.
6. Number of structured vs qualitative-only videos.
7. Evidence-level distribution.
8. Source-type distribution.
9. Coding-confidence distribution.
10. Duration-validity summary.
11. Duplicate/parallel sample summary.
12. Robot manufacturer distribution.
13. Activity taxonomy distribution.
14. Missing-value summary.
15. Records not suitable for modelling.

Acceptance criteria:

- The report must explicitly state that extraction is ongoing.
- It must not present the data as final results.
- It must identify where more extraction is needed, especially robot-side observations.

---

# Prompt 10: Add Extraction Templates for Future Coding

## Cursor Prompt

Create clean CSV templates under:

```text
data/templates/
```

Templates required:

```text
video_metadata_template.csv
video_segments_template.csv
robot_video_observations_template.csv
mivan_video_observations_template.csv
manufacturer_specs_template.csv
```

Each template must include all required columns from `config/data_dictionary.yaml`.

Also create:

```text
docs/video_coding_checklist.md
```

The checklist must guide manual extraction from videos.

It should include:

1. How to decide whether a video is usable.
2. How to assign suitability score.
3. How to segment the video.
4. How to count visible labour.
5. How to classify robot activity.
6. How to classify Mivan activity.
7. How to assign evidence level.
8. How to assign confidence level.
9. How to mark duration validity.
10. How to mark duplicate/parallel videos.

Acceptance criteria:

- A new researcher should be able to use the templates without asking for clarification.
- The checklist must be concise and operational.
- The templates must not contain sample rows unless clearly marked.

---

# Prompt 11: Create a Robot Source Expansion File

## Cursor Prompt

Create a file:

```text
data/robot_source_candidates.csv
```

This file should track possible robot video/spec sources beyond BrightMaster.

Required columns:

```text
candidate_id
manufacturer_name
robot_brand
robot_model
robot_category
country_or_region
source_url
source_type
manufacturer_verified
comparison_robot
relevance_to_mivan
recommended_use
review_status
notes
```

Rules:

1. Include BrightMaster as one source, not the only source.
2. Add rows for comparable robots only when there is a source URL.
3. Mark uncertain manufacturers as `manufacturer_verified = unknown`.
4. Use `recommended_use` values:
   - video_coding
   - manufacturer_specs
   - comparison_only
   - exclude
5. Do not make unsupported technical claims.

Acceptance criteria:

- The file must support robot-agnostic expansion.
- It must allow future inclusion of rebar tying, concrete leveling, finishing, grinding, layout, and inspection robots.
- It must not promote any one company.

---

# Prompt 12: Improve README for Research Workflow

## Cursor Prompt

Update `README.md` or create it if missing.

The README must explain:

1. Research purpose.
2. Robot-agnostic scope.
3. Current stage: ongoing video data extraction.
4. Repository folder structure.
5. Data files and their role.
6. Evidence-level system.
7. Source-type system.
8. Duration-validity warning.
9. How to run validation.
10. How to generate data quality report.
11. What should not be claimed from the dataset.
12. Next planned stage after extraction: GAN-ready seed dataset preparation.

Use research-safe wording:

```text
The dataset is a secondary observational dataset derived from publicly available videos and manufacturer-reported specifications. It is not direct field-measured productivity data.
```

Acceptance criteria:

- The README must be suitable for a journal reviewer or collaborator.
- It must not overclaim.
- It must clearly state that extraction is ongoing.

---

# Prompt 13: Create Tests for Validation Logic

## Cursor Prompt

Create a test file:

```text
tests/test_validation_logic.py
```

Test the validation rules for:

1. Missing required columns.
2. Invalid evidence levels.
3. Invalid source types.
4. Fresh concrete activity on wrong surface.
5. Post-cast activity wrongly labelled as fresh concrete finishing.
6. Invalid duration used for productivity.
7. Manufacturer-reported values treated as video-observed values.
8. Low-confidence record marked modelling-ready.
9. Duplicate group without independent sample control.
10. Unknown manufacturer treated as verified.

Acceptance criteria:

- Use simple test data inside the test file or small fixture CSVs.
- Tests should be runnable with:
  pytest
- Do not require internet access.
- Tests should not depend on actual YouTube downloads.

---

# Prompt 14: Create a Current-Stage Completion Checklist

## Cursor Prompt

Create:

```text
docs/current_stage_completion_checklist.md
```

This checklist should define when the video-extraction stage can be considered sufficiently complete for the next stage.

Include the following minimum checks:

1. Every video has metadata.
2. Every structured video has suitability score.
3. Every usable segment has timestamp and activity type.
4. Every observation has evidence level.
5. Every observation has confidence score.
6. Every duration has validity status.
7. Every manufacturer value is marked E3 and manufacturer_reported.
8. Every duplicate/parallel video is flagged.
9. Activity labels follow taxonomy.
10. Validation script produces no critical errors.
11. Data quality report has been generated.
12. Robot-side observations are sufficient for framework demonstration.
13. Mivan-side observations are sufficient for workflow representation.
14. Low-confidence records are not used as modelling-ready records.

Acceptance criteria:

- The checklist must be practical.
- It must not require completion of GAN modelling.
- It must clearly say that final quantitative claims require future validation.

---

# Prompt 15: Final Current-Stage Review Prompt

## Cursor Prompt

After completing the above improvements, review the repository again and create:

```text
reports/current_stage_readiness_review.md
```

The review must answer:

1. Is the current dataset logical?
2. Is the extraction reproducible?
3. Are the variables suitable for framework development?
4. Are manufacturer claims properly separated?
5. Are durations safely handled?
6. Are duplicate sources controlled?
7. Is the repo robot-agnostic?
8. Is the dataset suitable for a methodology demonstration?
9. Is it ready for GAN-ready seed dataset preparation?
10. What is still missing?

The final conclusion must use one of these labels:

```text
not_ready
pilot_ready
framework_ready
seed_dataset_ready
```

Do not overstate readiness. If data extraction is ongoing, the likely conclusion should be either `pilot_ready` or `framework_ready`, not final.

---

# Recommended Work Order in Cursor

Use the prompts in this order:

```text
1. Repository audit
2. Data dictionary
3. Activity taxonomy
4. Robot-agnostic metadata
5. Suitability scoring
6. Duration validity
7. Duplicate controls
8. Validation script
9. Data quality report
10. Templates and coding checklist
11. Robot source expansion file
12. README update
13. Tests
14. Completion checklist
15. Current-stage readiness review
```

---

# Final Research-Safe Position for the Repository

Use this statement in documents and reports:

> This repository supports a video-informed, robot-agnostic data extraction framework for construction robot deployment readiness assessment in aluminium formwork-based high-rise building construction. The extracted data are secondary observational records derived from public videos, manufacturer-reported specifications, and structured coding rules. The dataset is intended for framework development and future scenario modelling, not for claiming verified real-site productivity or field performance.

