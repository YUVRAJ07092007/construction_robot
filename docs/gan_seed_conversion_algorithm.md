# Stage 2: GAN-Ready Seed Conversion Algorithm

**Title:** Cleaning and encoding approved Stage 1 observations into GAN-ready seed records

**Prerequisite:** Stage 1 human approval ([`stage1_signoff.md`](stage1_signoff.md))

---

## Objective

Convert validated video-derived observations into a **normalized seed feature table** suitable for future synthetic scenario generation (GAN or other generative models). This stage does **not** train a GAN or emit synthetic records.

---

## Input

- `data/cleaned_video_dataset.csv` — Stage 1 modelling subset
- `data/robot_video_observations.csv` — comparison_robot flags
- `config/seed_encoding_schema.yaml` — categorical encodings and promotion rules
- `config/activity_taxonomy.yaml` — activity group normalization

---

## Output

| File | Purpose |
|------|---------|
| `data/gan_seed_dataset.csv` | Normalized seed records with human-readable + `*_enc` columns |
| `data/cleaned_video_dataset.csv` | Promoted rows updated to `data_use=framework_seed_ready` |
| `reports/seed_conversion_report.md` | Conversion log and exclusions |
| `reports/seed_validation_report.md` | Seed schema validation |

---

## Step 1: Apply seed promotion rules

Include a cleaned row only if **all** conditions hold:

1. `independent_sample=yes`
2. `is_duplicate_or_parallel=no`
3. `data_use=structured_coding` (not `qualitative_only`)
4. `coding_confidence` ∈ {medium, high}
5. `evidence_level` ∈ {E1, E2}
6. `usable_for_productivity=no`

Excluded rows remain in `cleaned_video_dataset.csv` at `structured_coding` or `qualitative_only`.

---

## Step 2: Normalize activity labels

Map raw `activity_type` values to taxonomy `activity_group` labels using `activity_taxonomy.yaml` (including legacy_label_map).

---

## Step 3: Encode categorical features

Add integer `*_enc` columns per `seed_encoding_schema.yaml` for:

- video_category, workflow_stage, congestion, reinforcement complexity
- access_condition, safety_condition, operating_surface, movement_pattern
- evidence_level, coding_confidence, manufacturer_name, comparison_robot

Human-readable columns are retained for auditability.

---

## Step 4: Assign seed metadata

Each record receives:

- `seed_id` (SEED-001, …)
- `seed_provenance=video_observed_secondary`
- `duration_excluded=yes` — segment timing is **not** a GAN target
- `usable_for_productivity=no`
- `data_use=framework_seed_ready`
- `seed_conversion_date`

---

## Step 5: Validate and export

Run:

```bash
python scripts/complete_stage2.py
```

This executes seed conversion, seed validation, Stage 1 re-validation, and data quality report regeneration.

---

## Research-safe statement

> GAN-ready seed records were derived from approved secondary video observations through deterministic normalization and encoding. Seed conversion does not generate synthetic data and does not treat public video segment duration as productivity evidence. Manufacturer E3 specifications remain in `manufacturer_specs.csv` and are not merged into video seed rows.

---

## What Stage 2 does NOT include

- GAN model training or synthetic sample generation
- Robot Deployment Readiness Index scoring
- Productivity or cycle-time claims
- Automatic promotion of low-confidence or duplicate rows

---

## Next stage

Stage 3 generative augmentation **design** — [`generative_augmentation_design.md`](generative_augmentation_design.md). Phase 3.1 synthetic CSV generation requires design review approval per [`stage3_design_checklist.md`](stage3_design_checklist.md).
