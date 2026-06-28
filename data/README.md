# Data Directory Guide

Plain-language descriptions for journal reviewers and collaborators.

> This repository does not contain direct field-measured productivity data. Public videos are used only as secondary observational sources for extracting visible task-level parameters and workflow characteristics.

See also: [`docs/repository_status_matrix.md`](../docs/repository_status_matrix.md)

---

## Core video-derived files

### `video_metadata.csv`

| Aspect | Detail |
|--------|--------|
| Purpose | Registry of all screened video and spec sources |
| Source type | Public URLs (YouTube, manufacturer pages) |
| Evidence level | E1–E3 depending on row |
| Record type | **Observed registry** |
| Safe use | Source tracking, suitability screening, duplicate control |
| Not allowed | Productivity benchmarking without field validation |

### `video_segments.csv`

| Aspect | Detail |
|--------|--------|
| Purpose | Timestamped segments within structured-extraction videos |
| Key columns | `start_time`, `end_time`, `visible_segment_duration_sec`, `duration_validity`, `usable_for_productivity` |
| Evidence level | E1/E2 |
| Record type | **Observed (segment)** |
| Safe use | Workflow structure, activity timing context |
| Not allowed | **`usable_for_productivity` must remain `no`** for public video |

### `robot_video_observations.csv` / `mivan_video_observations.csv`

| Aspect | Detail |
|--------|--------|
| Purpose | Task-level coding from visible footage |
| Evidence level | E1/E2 only |
| Record type | **Observed** |
| Safe use | Framework demonstration, taxonomy validation |
| Not allowed | Manufacturer performance claims |

### `cleaned_video_dataset.csv`

| Aspect | Detail |
|--------|--------|
| Purpose | Merged modelling subset from robot + Mivan observations |
| Key columns | `data_use`, `framework_seed_ready` rows, duplicate flags |
| Record type | **Observed / computed merge** |
| Safe use | Seed promotion when `data_use=framework_seed_ready` |
| Not allowed | Treating as complete empirical corpus |

**`framework_seed_ready`** means suitable for seed-dataset use in framework demonstration — **not** field-validated modelling data.

---

## Manufacturer-reported file

### `manufacturer_specs.csv`

| Aspect | Detail |
|--------|--------|
| Purpose | E3 specification and case-study claims from manufacturer pages |
| Evidence level | **E3 only** |
| Record type | **Manufacturer-reported** |
| Key controls | `claim_type`, `claim_use`, `independent_verification_status`, `used_in_model=no` |
| Safe use | Context, range framing, discussion |
| Not allowed | Silent use as field evidence or model input |

---

## Seed and synthetic files

### `gan_seed_dataset.csv` / `modelling_feature_matrix.csv`

| Aspect | Detail |
|--------|--------|
| Purpose | 14 encoded framework seeds for scenario modelling |
| Record type | **Seed (computed encoding from E1/E2 observations)** |
| Safe use | Feature inputs for rule/GAN pilot expansion |
| Not allowed | Population inference |

### `synthetic_scenario_dataset.csv` (rule-expanded pilot)

Also exported as **`pilot_rule_based_synthetic_scenarios.csv`** (reviewer-friendly alias).

| Aspect | Detail |
|--------|--------|
| Purpose | 50 constraint-filtered pilot scenarios |
| Record type | **Synthetic pilot** (`pilot_only=yes`) |
| Safe use | Stress-test framework logic and DRI |
| Not allowed | Statistical inference or observed-data claims |

### `synthetic_scenario_dataset_gan.csv` (TVAE/CTGAN pilot)

Also exported as **`pilot_gan_synthetic_scenarios.csv`**.

| Aspect | Detail |
|--------|--------|
| Purpose | 50 generative pilot scenarios (trained on n=14) |
| Record type | **Synthetic pilot** |
| Safe use | Compare rule vs generative augmentation approaches |
| Not allowed | Robust GAN augmentation claims |

### `synthetic_scenario_dataset_all.csv`

Also exported as **`pilot_combined_synthetic_scenarios.csv`**.

Combined rule + GAN pilot scenarios (100 rows). Same pilot-only restrictions.

### `dri_scored_scenarios.csv`

| Aspect | Detail |
|--------|--------|
| Purpose | Scenario-relative Deployment Readiness Index scores |
| Record type | **Computed** |
| Safe use | Relative ranking within coded/synthetic corpus |
| Not allowed | Field-validated deployment readiness |

---

## Duration warning

All video-derived durations are **visible segment durations** only. They are **not** verified productivity times. Zero records should have `usable_for_productivity=yes`.
