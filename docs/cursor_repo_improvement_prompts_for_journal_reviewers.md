# Cursor AI Improvement Prompt File for `construction_robot` Repository

## Purpose

This file is prepared for improving the GitHub repository:

```text
https://github.com/YUVRAJ07092007/construction_robot
```

The repository supports the research article direction:

**Video-Informed and Robot-Agnostic Framework for Assessing Construction Robot Deployment Readiness in Aluminium Formwork-Based High-Rise Building Construction**

The target journal is:

**Journal of Building Engineering**

The objective of these prompts is to make the repository more acceptable to journal reviewers by improving:

- documentation consistency,
- research-safe wording,
- data provenance,
- robot-agnostic coverage,
- validation strength,
- activity taxonomy,
- duration handling,
- duplicate/parallel source control,
- pilot synthetic data caution,
- deployment-readiness index defensibility.

---

# Global Instructions for Cursor AI

Apply the following principles throughout the repository.

## Main Position of the Repository

The repository must be presented as a **reproducible methodological framework repository**, not as a completed empirical field-performance dataset.

Use this safe position consistently:

> This repository supports a video-informed, robot-agnostic data extraction and scenario-modelling framework for construction robot deployment readiness assessment in aluminium formwork-based high-rise building construction. The extracted data are secondary observational records derived from public videos, manufacturer-reported specifications, and structured coding rules. The dataset is intended for framework development and scenario exploration, not for claiming verified real-site productivity or field performance.

## Must Avoid

Do not claim:

- real-site validation;
- actual productivity improvement;
- verified robot performance on Indian Mivan sites;
- statistically robust GAN generation from the current seed set;
- BrightMaster-specific generalization;
- final empirical proof of deployment feasibility.

## Mandatory Caution

Public videos are **secondary observational sources only**.

Manufacturer-reported specifications are **not independently verified field data**.

GAN/TVAE synthetic scenarios are **pilot-only** unless future evidence expands the seed dataset.

Deployment Readiness Index scores are **scenario-relative**, not field-validated.

---

# Priority 1: Create Master Repository Status Matrix

## Cursor Prompt

Create a new file:

```text
docs/repository_status_matrix.md
```

The file must reconcile all stage-status language across:

```text
README.md
reports/current_stage_readiness_review.md
reports/data_quality_report.md
docs/paper_methods_draft.md
docs/deployment_readiness_index_design.md
```

The matrix must include:

| Stage | Output files | Current status | Evidence level | Safe claim | Not allowed claim |
|---|---|---|---|---|---|

Use these stages:

1. Video source identification
2. Video suitability screening
3. Segment-level video coding
4. Cleaned video-derived dataset
5. GAN-ready seed dataset
6. Rule-based scenario expansion
7. CTGAN/TVAE pilot generation
8. Deployment Readiness Index framework
9. Techno-economic assessment, if present
10. Future field validation

Use conservative status labels:

```text
ongoing
pilot_complete
framework_demo_complete
seed_ready
not_started
future_work
```

Acceptance criteria:

- The file must make clear that extraction work is ongoing.
- It must state that the current dataset is suitable for framework demonstration, not final empirical claims.
- All other documents must be updated to match this status matrix.
- Remove contradictory statements such as “not started” where pilot outputs already exist, or “complete” where only pilot demonstration exists.

---

# Priority 2: Fix Documentation Consistency

## Cursor Prompt

Review and update the following files for consistency with `docs/repository_status_matrix.md`:

```text
README.md
reports/current_stage_readiness_review.md
reports/data_quality_report.md
docs/paper_methods_draft.md
docs/deployment_readiness_index_design.md
```

Ensure the same terminology is used everywhere:

| Risky wording | Replace with |
|---|---|
| complete dataset | pilot video-derived dataset |
| modelling-ready | framework-seed-ready |
| GAN dataset complete | GAN/TVAE pilot scenario generation complete |
| validates robot deployment | demonstrates framework logic |
| productivity result | scenario-based indicator |
| robot performance proof | manufacturer-reported or video-derived observation |
| final readiness score | scenario-relative readiness score |

Acceptance criteria:

- No document should overstate the current evidence level.
- All documents must say the repository is robot-agnostic.
- All documents must state that videos are secondary observational sources.
- All documents must clearly distinguish observed, estimated, manufacturer-reported, computed, and synthetic data.

---

# Priority 3: Check and Fix File Formatting

## Cursor Prompt

Run a repository-wide formatting check for `.csv`, `.py`, `.yaml`, `.yml`, and `.md` files.

Use or create a script:

```text
scripts/check_file_formatting.py
```

The script must identify possible single-line or poorly formatted files.

Suggested logic:

```python
from pathlib import Path

for p in Path(".").rglob("*"):
    if p.is_file() and p.suffix in {".csv", ".py", ".yaml", ".yml", ".md"}:
        text = p.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        if len(lines) <= 3 and len(text) > 1000:
            print("POSSIBLE SINGLE-LINE FILE:", p, "lines=", len(lines), "chars=", len(text))
```

If files are actually one-line/minified, reformat them with proper line breaks.

Acceptance criteria:

- CSV files must be readable line-by-line.
- YAML files must be valid and human-readable.
- Python scripts must have normal line breaks and pass basic syntax check.
- Markdown files must be readable in GitHub preview.
- Create report:

```text
reports/file_formatting_report.md
```

---

# Priority 4: Rename “modelling_ready” to “framework_seed_ready”

## Cursor Prompt

Search the repository for the term:

```text
modelling_ready
```

Replace it with:

```text
framework_seed_ready
```

where it refers to video-derived records suitable for framework demonstration.

Reason:

The term `modelling_ready` may suggest field-quality empirical data. `framework_seed_ready` is safer because the current dataset is derived from videos, manufacturer sources, and structured coding.

Update all affected:

```text
CSV files
Python scripts
YAML configs
README
reports
docs
tests
```

Acceptance criteria:

- No broken validation logic.
- Existing meaning is preserved.
- README explains that `framework_seed_ready` means suitable for seed-dataset use, not field-validated modelling.

---

# Priority 5: Strengthen Manufacturer-Reported Data Controls

## Cursor Prompt

Update `manufacturer_specs.csv` and relevant schema/config files to include:

```text
claim_type
claim_use
independent_verification_status
used_in_model
model_use_note
```

Allowed values:

```text
claim_type:
  efficiency
  dimension
  weight
  navigation
  endurance
  flatness
  manpower_reduction
  completed_area
  trained_operator_count
  other

claim_use:
  specification_context
  range_context_only
  discussion_only
  comparison_only
  exclude

independent_verification_status:
  verified
  not_verified
  unknown

used_in_model:
  yes
  no
```

Rules:

1. Manufacturer-reported claims must be evidence level `E3`.
2. Manufacturer claims should not be treated as video-observed values.
3. Claims such as productivity, manpower reduction, flatness, or completed area must be marked `not_verified` unless independently validated.
4. Use manufacturer specifications mainly for context, range framing, or comparison.

Acceptance criteria:

- No manufacturer claim is silently used as field evidence.
- `manufacturer_specs.csv` clearly separates specification context from model input.
- Validation script checks these rules.

---

# Priority 6: Improve Duration Handling and Naming

## Cursor Prompt

Standardize duration-related columns across all files.

Replace ambiguous columns such as:

```text
task_duration_observed
segment_duration_sec
```

with clearer fields:

```text
visible_segment_duration_sec
visible_duration_validity
duration_validity_reason
continuous_unedited_segment
time_lapse_or_jump_cut
usable_for_productivity
```

Rules:

1. Public video duration should not be used for productivity unless independently verified.
2. If the segment is edited, promotional, time-lapsed, narrated montage, or jump-cut:
   - `visible_duration_validity = invalid`
   - `usable_for_productivity = no`
3. If the segment is continuous:
   - `visible_duration_validity = valid_for_visible_segment_only`
   - `usable_for_productivity = no`
4. `usable_for_productivity = yes` should almost never appear in the current dataset.

Acceptance criteria:

- Existing duration values are preserved as visible segment durations.
- Reports explicitly state that zero records are used for productivity unless verified.
- Validation script flags any questionable productivity use.

---

# Priority 7: Improve Activity Taxonomy for Fresh vs Post-Cast Activities

## Cursor Prompt

Review and improve:

```text
config/activity_taxonomy.yaml
```

Ensure it separates:

```text
fresh_concrete_leveling
fresh_concrete_finishing
post_cast_floor_grinding
post_cast_surface_preparation
post_cast_coating
```

Important correction:

Do not automatically map `concrete_finishing` to `post_cast_coating`.

Instead, use context-aware mapping based on surface condition.

Recommended logic:

```yaml
concrete_finishing:
  default_group: unknown
  requires_surface_check:
    wet_concrete: fresh_concrete_finishing
    partially_finished: fresh_concrete_finishing
    hardened_concrete: post_cast_surface_preparation
    indoor_hardened_floor: post_cast_coating
    unknown: unknown
```

Acceptance criteria:

- Fresh concrete finishing and post-cast coating/grinding are not confused.
- If surface condition is unknown, the activity should remain `unknown` or `requires_review`.
- If labels are changed, add or update `label_revision_note`.
- Validation script must enforce taxonomy rules.

---

# Priority 8: Strengthen Robot-Agnostic Source Coverage

## Cursor Prompt

Improve:

```text
data/robot_source_candidates.csv
```

Add or validate the following columns:

```text
task_similarity_to_mivan
source_stability
video_available
spec_available
included_in_current_dataset
reason_not_included
screening_status
```

Suggested allowed values:

```text
task_similarity_to_mivan:
  high
  medium
  low
  unknown

source_stability:
  official_page
  youtube
  facebook
  third_party
  unstable
  unknown

video_available:
  yes
  no
  unknown

spec_available:
  yes
  no
  unknown

included_in_current_dataset:
  yes
  no
  partial

screening_status:
  included
  qualitative_only
  comparison_only
  deferred
  excluded
```

Rules:

1. BrightMaster must be only one source, not the only source.
2. Comparable robots from other companies should be listed where source URLs exist.
3. Unverified robots must be marked clearly.
4. Similar robots may include concrete leveling, concrete finishing, floor grinding, rebar tying, layout, inspection, coating, and surface-preparation robots.

Acceptance criteria:

- Repository visibly supports a robot-agnostic framework.
- Current BrightMaster-heavy data is acknowledged as a sample limitation.
- Non-BrightMaster sources are recorded even if not yet fully coded.

---

# Priority 9: Add Duplicate and Parallel Source Controls

## Cursor Prompt

Ensure all relevant CSV files include:

```text
is_duplicate_or_parallel
duplicate_group_id
independent_sample
parallel_source_note
```

Rules:

1. If two videos show the same or parallel workflow, mark them in the same duplicate group.
2. Only one record in each duplicate group should have `independent_sample = yes`.
3. Parallel records may be used for cross-checking but not for inflating independent sample counts.
4. Do not delete parallel entries; flag them.

Acceptance criteria:

- Analysis can filter by `independent_sample = yes`.
- Reports show duplicate/parallel-source count.
- Validation script flags duplicate groups without one clear independent sample.

---

# Priority 10: Upgrade Validation Script and Issue Report

## Cursor Prompt

Upgrade or rewrite:

```text
src/validate_extractions.py
```

The script must validate:

1. Required columns by file.
2. Allowed values from config files.
3. Evidence levels.
4. Source types.
5. Data-use values.
6. Activity taxonomy.
7. Duration validity.
8. Manufacturer claim separation.
9. Duplicate/parallel controls.
10. Robot-agnostic metadata fields.
11. Fresh vs post-cast activity logic.
12. Low-confidence records not marked `framework_seed_ready`.
13. Synthetic outputs marked as pilot-only, if synthetic files exist.

Required outputs:

```text
reports/validation_report.md
reports/validation_issues.csv
```

`validation_issues.csv` must contain:

```text
issue_id
file
row_identifier
severity
field
problem
suggested_fix
status
```

Severity values:

```text
critical
warning
suggestion
```

Acceptance criteria:

- Validation must not silently modify data.
- Critical issues should be separated from warnings.
- The script should run with:

```bash
python src/validate_extractions.py
```

- If tests exist, they must pass.

---

# Priority 11: Add Data Quality Report Enhancements

## Cursor Prompt

Upgrade or create:

```text
src/generate_data_quality_report.py
```

Generate:

```text
reports/data_quality_report.md
```

The report must include:

1. Extraction status: ongoing / pilot / framework-ready.
2. Row count per file.
3. Robot observation count.
4. Mivan observation count.
5. Manufacturer-spec count.
6. Unique video count.
7. Robot manufacturer distribution.
8. BrightMaster vs non-BrightMaster distribution.
9. Activity taxonomy distribution.
10. Evidence-level distribution.
11. Source-type distribution.
12. Data-use distribution.
13. Coding-confidence distribution.
14. Duration-validity summary.
15. Productivity-usable duration count.
16. Duplicate/parallel-source summary.
17. Framework-seed-ready count.
18. Records requiring review.
19. Most important extraction gaps.

Acceptance criteria:

- Report must explicitly say extraction is ongoing if applicable.
- It must not present pilot data as final empirical results.
- It must clearly state where more robot-side data are needed.

---

# Priority 12: Mark Synthetic Data as Pilot-Only

## Cursor Prompt

If synthetic scenario files exist, rename or document them as pilot outputs.

Preferred names:

```text
pilot_rule_based_synthetic_scenarios.csv
pilot_gan_synthetic_scenarios.csv
pilot_combined_synthetic_scenarios.csv
```

Add fields:

```text
record_origin
pilot_only
training_seed_count
not_for_statistical_inference
synthetic_generation_method
generation_note
```

Rules:

1. Synthetic records must never appear as observed records.
2. CTGAN/TVAE records generated from small seed data must be marked pilot-only.
3. The README and methods draft must say these are for stress-testing framework logic, not statistical inference.

Acceptance criteria:

- No synthetic record is mixed with video-observed data.
- The repository clearly distinguishes observed, seed, rule-synthetic, and GAN/TVAE-synthetic records.
- Reports mention the small seed size limitation.

---

# Priority 13: Add Deployment Readiness Index Weight Sensitivity

## Cursor Prompt

Create or improve:

```text
src/dri_weight_sensitivity.py
```

Generate:

```text
reports/dri_weight_sensitivity_report.md
reports/dri_weight_sensitivity_results.csv
```

Test at least four weighting schemes:

| Scheme | Purpose |
|---|---|
| equal_weights | neutral baseline |
| safety_heavy | construction-site safety emphasis |
| workflow_heavy | Mivan cycle integration emphasis |
| evidence_heavy | conservative data-quality emphasis |

The report must answer:

1. Do readiness rankings change under different weights?
2. Which dimensions dominate?
3. Are top-ranked scenarios stable?
4. Which scenarios are weight-sensitive?
5. What should be stated as limitation?

Acceptance criteria:

- DRI results must be described as scenario-relative.
- The report must not claim field-validated readiness.
- If rankings are unstable, state this clearly.

---

# Priority 14: Improve README for Reviewer Use

## Cursor Prompt

Update `README.md` so it is suitable for a journal reviewer or collaborator.

Must include:

1. Research purpose.
2. Robot-agnostic scope.
3. Repository status: ongoing/pilot/framework.
4. Folder structure.
5. Evidence-level system.
6. Source-type system.
7. Data-use system.
8. Manufacturer-claim warning.
9. Duration-validity warning.
10. Duplicate/parallel-source control.
11. Synthetic data pilot warning.
12. DRI scenario-relative warning.
13. How to run validation.
14. How to generate data-quality report.
15. What not to claim from the dataset.
16. Next steps.

Use this mandatory wording:

> This repository does not contain direct field-measured productivity data. Public videos are used only as secondary observational sources for extracting visible task-level parameters and workflow characteristics.

Acceptance criteria:

- README must not overclaim.
- README must clearly say BrightMaster is not the sole focus.
- README must make the repository understandable without reading all code.

---

# Priority 15: Add `data/README.md`

## Cursor Prompt

Create:

```text
data/README.md
```

Explain each data file in plain language:

```text
video_metadata.csv
video_segments.csv
robot_video_observations.csv
mivan_video_observations.csv
manufacturer_specs.csv
cleaned_video_dataset.csv
gan_seed_dataset.csv
pilot synthetic scenario files, if present
```

For each file, describe:

1. Purpose.
2. Source type.
3. Key columns.
4. Evidence level.
5. Whether it is observed, manufacturer-reported, computed, seed, or synthetic.
6. Safe use.
7. Not allowed use.

Acceptance criteria:

- A reviewer must be able to understand every CSV without asking.
- The file must explicitly warn against using video duration for productivity.

---

# Priority 16: Add Reviewer Notes

## Cursor Prompt

Create:

```text
docs/reviewer_notes.md
```

The file must explain the research-safe logic of the repository:

1. Why public videos are used.
2. Why this is secondary observational data.
3. Why manufacturer claims are separated.
4. Why the framework is robot-agnostic.
5. Why synthetic data are pilot-only.
6. Why real-site validation remains future work.
7. Why the repository still adds value for Journal of Building Engineering.

Use concise academic language.

Acceptance criteria:

- No defensive tone.
- No overclaiming.
- Clear limitation statement.
- Clear contribution statement.

---

# Priority 17: Add Citation and License Files

## Cursor Prompt

Add:

```text
CITATION.cff
LICENSE
CHANGELOG.md
```

Use an appropriate open-source license if the repository is meant to be shared publicly.

`CHANGELOG.md` must record:

1. Initial video extraction stage.
2. Schema and validation improvements.
3. Robot-agnostic expansion.
4. Synthetic-pilot stage, if applicable.
5. DRI framework stage, if applicable.

Acceptance criteria:

- Repository becomes easier to cite and review.
- Changelog records stage-wise evolution.
- License is clear.

---

# Priority 18: Final Reviewer-Readiness Report

## Cursor Prompt

After completing the above improvements, create:

```text
reports/reviewer_readiness_report.md
```

The report must answer:

1. Is repository status internally consistent?
2. Are all data files readable and formatted?
3. Are videos treated as secondary observational data?
4. Are manufacturer claims separated?
5. Is the repository robot-agnostic?
6. Are duplicate/parallel sources controlled?
7. Are durations safely handled?
8. Is activity taxonomy scientifically clear?
9. Are synthetic outputs marked pilot-only?
10. Is DRI scenario-relative and sensitivity-tested?
11. Is validation report clean?
12. Is the dataset suitable for methodology demonstration?
13. What remains future work?

Final readiness label must be one of:

```text
not_ready
pilot_ready
framework_ready
reviewer_ready_with_limitations
```

Use `reviewer_ready_with_limitations` only if all critical issues are fixed.

---

# Recommended Execution Order

Use the prompts in this order:

```text
1. Repository status matrix
2. Documentation consistency
3. File formatting check
4. Rename modelling_ready to framework_seed_ready
5. Manufacturer-reported data controls
6. Duration handling
7. Activity taxonomy correction
8. Robot-agnostic source coverage
9. Duplicate/parallel controls
10. Validation script upgrade
11. Data quality report enhancement
12. Synthetic pilot marking
13. DRI weight sensitivity
14. README update
15. data/README.md
16. reviewer_notes.md
17. CITATION, LICENSE, CHANGELOG
18. Reviewer-readiness report
```

---

# Final Safe Claim for the Paper and Repository

Use this exact statement wherever needed:

> The repository presents a video-informed and robot-agnostic methodological framework for converting publicly available construction robotics and aluminium formwork construction videos into structured secondary observational data. The resulting dataset supports framework development, pilot scenario generation, and scenario-relative readiness assessment. It does not constitute direct field-measured productivity evidence or field validation of construction robot performance.

