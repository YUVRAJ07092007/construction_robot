# Cursor AI Prompt File: Final Reviewer-Readiness Improvements for `construction_robot`

## Repository

```text
https://github.com/YUVRAJ07092007/construction_robot
```

## Purpose of This File

This file contains the **remaining improvement prompts only** after the latest review of the GitHub repository.

The repository has already improved substantially and now contains reviewer-oriented documentation, validation reports, data-quality reports, reviewer notes, status matrix, DRI sensitivity report, license, citation file, and changelog.

However, a few important issues remain. These must be fixed before the repository can be safely presented as a **reviewer-ready methodological-support repository** for a paper targeted to the **Journal of Building Engineering**.

---

# Current Safe Position of the Repository

Use this position consistently across all files:

> This repository presents a video-informed and robot-agnostic methodological framework for converting publicly available construction robotics and aluminium formwork construction videos into structured secondary observational data. The resulting dataset supports framework development, pilot scenario generation, and scenario-relative readiness assessment. It does not constitute direct field-measured productivity evidence or field validation of construction robot performance.

---

# Important Restrictions

Do **not** overclaim.

Do **not** say the dataset proves robot productivity.

Do **not** say GAN/TVAE outputs are statistically robust.

Do **not** say public videos are real-site measured productivity data.

Do **not** make the repository BrightMaster-specific.

Do **not** treat manufacturer-reported values as independently verified data.

Do **not** delete useful records unless clearly invalid; prefer flagging and traceability.

---

# Remaining Priority Fixes

The latest review identified the following remaining issues:

1. `modelling_ready` still appears in data, reports, and schema.
2. `manufacturer_specs.csv` does not fully include manufacturer-claim control columns.
3. `concrete_finishing` activity taxonomy is still risky because it is mapped directly to post-cast coating.
4. Duplicate-group validation still gives suggestions for the Mivan 7-day slab-cycle duplicate group.
5. `paper_methods_draft.md` contains contradictory wording about GAN/synthetic-data stage.
6. Robot-agnostic design is structurally improved but still needs more non-BrightMaster source tracking.
7. Validation and data-quality reports should be regenerated after all fixes.

Use the prompts below in order.

---

# Prompt 1: Replace `modelling_ready` with `framework_seed_ready`

## Cursor Task

Search the full repository for:

```text
modelling_ready
```

Replace it with:

```text
framework_seed_ready
```

where it refers to video-derived or cleaned records suitable for framework seed use.

## Files to Check

Check at least:

```text
data/cleaned_video_dataset.csv
config/data_dictionary.yaml
README.md
data/README.md
reports/data_quality_report.md
reports/reviewer_readiness_report.md
reports/current_stage_readiness_review.md
docs/repository_status_matrix.md
docs/paper_methods_draft.md
docs/reviewer_notes.md
src/*.py
scripts/*.py
tests/*.py
```

## Required Meaning

`framework_seed_ready` means:

> The record is suitable for use as a seed record in framework demonstration or pilot scenario generation, but it is not direct field-measured data and should not be treated as empirical performance evidence.

## Acceptance Criteria

- No remaining `modelling_ready` text should exist unless mentioned only in a changelog as an old replaced term.
- `data_use` allowed values must include `framework_seed_ready`.
- `data_use` allowed values should not include `modelling_ready`.
- All validation logic and tests must be updated.
- Data-quality report must use “framework-seed-ready”, not “modelling-ready”.
- README must explain the meaning of `framework_seed_ready`.

---

# Prompt 2: Add Manufacturer-Claim Control Columns

## Cursor Task

Update:

```text
data/manufacturer_specs.csv
config/data_dictionary.yaml
src/validate_extractions.py
reports/data_quality_report.md
data/README.md
README.md
```

to ensure manufacturer-reported data are fully controlled.

## Add Required Columns to `manufacturer_specs.csv`

Add these columns:

```text
claim_type
claim_use
independent_verification_status
used_in_model
model_use_note
```

## Allowed Values

### `claim_type`

```text
efficiency
dimension
weight
navigation
endurance
flatness
manpower_reduction
completed_area
trained_operator_count
application_context
other
```

### `claim_use`

```text
specification_context
range_context_only
discussion_only
comparison_only
exclude
```

### `independent_verification_status`

```text
verified
not_verified
unknown
```

### `used_in_model`

```text
yes
no
```

## Rules

1. All manufacturer-specification rows must have `evidence_level = E3`.
2. All manufacturer rows must have `source_type = manufacturer_reported`.
3. Productivity, manpower reduction, flatness, completed area, and trained-operator claims should normally have:
   - `independent_verification_status = not_verified`
   - `used_in_model = no`
4. Technical dimensions or robot-category information may be used only as:
   - `claim_use = specification_context`
   - not as verified field data.
5. If any manufacturer value is used as a range context, explain it in `model_use_note`.

## Example Rows

```text
operating_efficiency,>=300 m2/h,E3,manufacturer_reported,efficiency,range_context_only,not_verified,no,Manufacturer-reported efficiency; used only for contextual range discussion.
manpower_reduction,>30%,E3,manufacturer_reported,manpower_reduction,discussion_only,not_verified,no,Manufacturer-reported claim; not used as field-verified productivity evidence.
flatness_tolerance,±3 mm,E3,manufacturer_reported,flatness,discussion_only,not_verified,no,Manufacturer-reported claim; not independently verified.
```

## Acceptance Criteria

- `manufacturer_specs.csv` has all required control columns.
- Validation script flags any manufacturer row without these fields.
- No manufacturer claim is marked as field-verified unless evidence exists.
- README and data guide clearly explain manufacturer data limitations.

---

# Prompt 3: Make `concrete_finishing` Taxonomy Context-Based

## Cursor Task

Update:

```text
config/activity_taxonomy.yaml
src/validate_extractions.py
tests/test_validation_logic.py
data/robot_video_observations.csv
data/mivan_video_observations.csv
data/cleaned_video_dataset.csv
```

so that `concrete_finishing` is not automatically treated as post-cast coating.

## Required Taxonomy Logic

Use context-aware mapping:

```yaml
concrete_finishing:
  default_group: unknown
  requires_surface_check:
    wet_concrete: fresh_concrete_finishing
    partially_finished: fresh_concrete_finishing
    hardened_concrete: post_cast_surface_preparation
    indoor_hardened_floor: post_cast_coating
    finished: post_cast_surface_preparation
    unknown: unknown
```

## Required Rule

If `activity_type = concrete_finishing` and surface condition is unknown, do not guess. Mark:

```text
activity_group = unknown
requires_review = yes
label_revision_note = concrete_finishing requires surface-condition-based classification
```

## Acceptance Criteria

- Fresh concrete finishing and post-cast coating are not confused.
- Validation checks surface condition before assigning final activity group.
- Any corrected record has `label_revision_note`.
- Existing robot observations showing indoor coating/hardened surface should be labelled as post-cast coating or post-cast surface preparation only if surface context supports it.

---

# Prompt 4: Resolve Duplicate-Group Validation Suggestions

## Cursor Task

The validation report still gives suggestions for duplicate group:

```text
DUP-MIVAN-SLAB-7DAY
```

Fix either the data or the validation logic so the duplicate-group status is clear and no false suggestion remains.

## Add a Duplicate Summary File

Create:

```text
data/duplicate_group_summary.csv
```

with columns:

```text
duplicate_group_id
primary_video_id
parallel_video_ids
independent_sample_video_id
independent_sample_count
parallel_record_count
duplicate_group_note
```

## Required Rules

1. Each duplicate group must have exactly one `independent_sample_video_id`.
2. Parallel videos may be used for cross-checking.
3. Parallel videos must not inflate independent sample count.
4. Do not delete duplicate/parallel videos unless unusable.
5. Validation script should read this summary file, if present.

## Example

```text
DUP-MIVAN-SLAB-7DAY,M01,M05,M01,1,1,M05 is a parallel/alternate source aligned to M01 and should not be counted as an independent sample.
```

## Acceptance Criteria

- `validation_report.md` should not show unresolved duplicate-group suggestions if the group is correctly defined.
- `validation_issues.csv` should not include false duplicate warnings.
- `data_quality_report.md` should show duplicate/parallel-source summary.
- Analysis can filter independent records using `independent_sample = yes`.

---

# Prompt 5: Clean Contradictions in `paper_methods_draft.md`

## Cursor Task

Review and revise:

```text
docs/paper_methods_draft.md
```

Remove contradictions about:

- whether synthetic records were generated,
- whether GAN/TVAE was performed,
- whether Phase 3 was started or deferred,
- whether outputs are final or pilot-only.

## Required Safe Wording

Use this wording:

> Phase 3.1 rule-based scenario expansion and Phase 3B tabular GAN/TVAE pilot generation have been implemented as pilot-only scenario-generation demonstrations. Because the seed dataset contains only 14 framework-seed-ready records, these outputs are used only for stress-testing framework logic and scenario diversity. They are not used for statistical inference, field-performance validation, or productivity claims.

## Also Include

> The current dataset remains a secondary observational and framework-seed dataset. Direct field validation on active aluminium formwork-based high-rise construction projects remains future work.

## Acceptance Criteria

- No statement says GAN was not performed if pilot GAN/TVAE files exist.
- No statement says GAN output is robust or final.
- No statement says synthetic data are field data.
- Phase/stage descriptions match `docs/repository_status_matrix.md`.

---

# Prompt 6: Strengthen Non-BrightMaster Robot Source Tracking

## Cursor Task

Improve:

```text
data/robot_source_candidates.csv
```

so the repository clearly supports a robot-agnostic framework.

## Add or Validate Columns

```text
task_similarity_to_mivan
source_stability
video_available
spec_available
included_in_current_dataset
reason_not_included
screening_status
robot_task_family
```

## Recommended `robot_task_family` Values

```text
fresh_concrete_leveling
fresh_concrete_finishing
floor_grinding
surface_preparation
rebar_tying
layout_marking
inspection
coating
robot_transport_setup
other
```

## Rules

1. BrightMaster must be only one source category.
2. Add more non-BrightMaster candidates where source URLs exist.
3. If source reliability is unclear, use `source_stability = third_party` or `unknown`.
4. If not currently coded, set `included_in_current_dataset = no` and explain why.
5. Do not make unsupported claims about non-BrightMaster robots.
6. Candidates may be marked `comparison_only`, `qualitative_only`, or `deferred`.

## Acceptance Criteria

- Repository visibly supports robot-agnostic comparison.
- Data-quality report shows BrightMaster vs non-BrightMaster candidate distribution.
- README honestly states that coded observations are currently BrightMaster-heavy but the framework is robot-agnostic.

---

# Prompt 7: Regenerate Validation and Data-Quality Reports

## Cursor Task

After implementing Prompts 1–6, rerun or update:

```text
python src/validate_extractions.py
python src/generate_data_quality_report.py
pytest tests/
```

Regenerate:

```text
reports/validation_report.md
reports/validation_issues.csv
reports/data_quality_report.md
reports/reviewer_readiness_report.md
```

## Expected Result

Validation should ideally show:

```text
critical errors: 0
warnings: 0
suggestions: 0 or only minor non-blocking suggestions
```

Data-quality report should use:

```text
framework_seed_ready
```

not:

```text
modelling_ready
```

## Acceptance Criteria

- Tests pass.
- Reports reflect the latest data and terminology.
- No report contradicts another report.
- Reviewer-readiness label remains:
  - `reviewer_ready_with_limitations`
  only if all critical fixes are complete.

---

# Prompt 8: Final Consistency Search

## Cursor Task

Perform a final full-repository text search for risky or inconsistent terms.

Search for:

```text
modelling_ready
modeling_ready
field validated
field-validated
productivity improvement
proves
validated robot performance
GAN dataset complete
BrightMaster-specific
direct field data
real-site productivity
```

## Rules

- Keep terms only if they appear inside a “not allowed claim” or limitation statement.
- Replace overclaiming statements with safer language.

## Safe Replacements

| Risky Term | Safe Replacement |
|---|---|
| modelling_ready | framework_seed_ready |
| field validated | future field validation required |
| productivity improvement | scenario-based productivity indicator |
| proves | demonstrates / illustrates |
| validated robot performance | scenario-relative readiness assessment |
| GAN dataset complete | pilot GAN/TVAE scenario generation |
| BrightMaster-specific | robot-agnostic with BrightMaster-heavy current sample |
| direct field data | secondary observational data |

## Acceptance Criteria

- No overclaiming statement remains.
- Repository language is conservative and reviewer-safe.
- README, methods draft, reviewer notes, and reports are aligned.

---

# Prompt 9: Final Reviewer-Readiness Sign-Off

## Cursor Task

Update:

```text
reports/reviewer_readiness_report.md
```

Add a final section:

```text
## Final Sign-Off After Remaining Fixes
```

Answer the following:

1. Were all `modelling_ready` references replaced?
2. Were manufacturer-claim control columns added?
3. Was concrete-finishing taxonomy made context-based?
4. Was duplicate-group validation resolved?
5. Was the methods draft made internally consistent?
6. Was robot-agnostic source tracking strengthened?
7. Were validation and data-quality reports regenerated?
8. Are synthetic outputs clearly pilot-only?
9. Are DRI outputs clearly scenario-relative?
10. Is the repository suitable as a methodology-support repository for Journal of Building Engineering?

## Final Label

Use one of:

```text
not_ready
pilot_ready
framework_ready
reviewer_ready_with_limitations
```

Only use:

```text
reviewer_ready_with_limitations
```

if all above items are complete.

---

# Final Expected Repository Position

After these fixes, the repository should be safe to describe as:

> A reviewer-ready-with-limitations repository supporting a video-informed, robot-agnostic methodological framework for construction robot deployment readiness assessment in aluminium formwork-based high-rise building construction. The repository is suitable for methodology demonstration and transparent supplementary material, but not for claiming verified field productivity or final deployment performance.
