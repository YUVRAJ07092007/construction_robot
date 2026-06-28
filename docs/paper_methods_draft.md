# Paper Methods Draft — Video-Informed Data Extraction (Stage 1)

**Target journal:** Journal of Building Engineering  
**Working title:** *Video-Informed and GAN-Augmented Framework for Assessing Construction Robot Deployment Readiness in Aluminium Formwork-Based High-Rise Building Construction*  
**Stage:** Methods section draft from approved Stage 1 dataset (`framework_ready`)  
**Sign-off:** [`stage1_signoff.md`](stage1_signoff.md) (2026-06-27)

> **Note for authors:** Stages 1–2, Phase 3.1 (synthetic expansion), Phase 3B (tabular GAN pilot), and Phase 3C (DRI framework) are complete. Field validation remains future work.

---

## 2.X Data sources and study design

Data were collected from publicly accessible online videos and manufacturer product pages. The construction context is **aluminium formwork (Mivan) high-rise slab-cycle workflow** on one side and **construction robot field or promotional demonstrations** on the other. The study design is **secondary observational**: videos provide visible task-level and work-zone parameters, not independently verified field productivity.

Two parallel observation streams were maintained:

1. **Mivan workflow observations** — human labour, access, congestion, and slab-cycle stages (pre-pour, pour, post-cast).
2. **Robot operation observations** — movement, surface type, guidance mode, and human–robot separation during robot tasks.

Manufacturer technical parameters were stored separately as **evidence level E3** (manufacturer-reported) and were not mixed with video-derived E1/E2 observations.

The robot sample is **BrightMaster-heavy** by source availability, with **one non-BrightMaster comparison** (Bright Dream ground-leveling robot, video R22) to preserve robot-agnostic schema intent. This sample composition is a stated limitation, not a claim of market representativeness.

---

## 2.X Video registry and suitability screening

Each candidate source was registered in `video_metadata.csv` with platform, title, channel, access date, activity focus, construction context, and visibility quality.

Suitability was scored on **seven criteria** (0–2 points each; maximum 14), following the rubric in `config/extraction_config.py` and the algorithm in `video_informed_task_level_data_extraction_algorithm.md`:

| Criterion | What it measures |
|-----------|------------------|
| Relevance | Link to Mivan workflow or construction robot task |
| Visual clarity | Whether activity and work zone are visible |
| Activity continuity | Sustained vs fragmented footage |
| Activity identifiability | Specific vs ambiguous task label |
| Interaction visibility | Worker counts, robot movement, congestion |
| Editing level | Raw field footage vs heavy montage |
| Parameter measurability | Whether structured E1/E2 variables can be coded |

**Classification bands:** 0–5 exclude; 6–9 qualitative workflow use only; **10–14 structured extraction**. Only high-band sources received segment boundaries and full parameter coding.

Thirty-two sources were screened; sixteen entered structured extraction. Four robot candidates remain deferred for optional post-Stage-1 expansion (`data/robot_source_candidates.csv`).

---

## 2.X Segmentation protocol

Full videos were not coded as single units. Usable **activity segments** were defined in `video_segments.csv` with start/end timestamps, activity type, segment quality, and duration validity.

**Minimum segment length:** 8 s default; **5 s** permitted for unambiguous single-pass robot activities (leveling, finishing, grinding).

Segments were rejected or retained with `duration_validity=invalid` when footage was narrated, chapter-based, promotional, or jump-cut. In the approved dataset, **all 46 segments** are marked invalid for productivity timing; visible duration is retained only as a segment boundary descriptor.

For long Mivan documentaries, segment bounds were aligned to YouTube chapter markers where available (e.g. formwork erection and concrete pour in video M02).

---

## 2.X Variable extraction and coding

Coding followed `config/data_dictionary.yaml` and `config/activity_taxonomy.yaml`. Field naming uses **`access_condition`** consistently across tables.

### Mivan-side parameters (examples)

Labour counts (visible min/max/dominant), congestion level, reinforcement complexity, conduit presence, material movement method, pour sequence, surface condition, safety exposure, workflow sequence, and floor-cycle stage (pre-pour / pour / post-cast).

### Robot-side parameters (examples)

Robot activity type, operating surface (e.g. wet concrete vs hardened concrete), movement pattern, guidance mode, operator/assistant counts, operational continuity, obstacle presence, human–robot separation, safety condition, and manufacturer metadata (`manufacturer_name`, `comparison_robot`).

### Activity taxonomy rule

**Fresh-concrete tasks** (e.g. concrete leveling during pour) are separated from **post-cast tasks** (floor grinding, coating on hardened surfaces). This prevents misleading cross-stage comparisons in deployment-readiness framing.

Each observation received:

- **Evidence level** E1 (directly visible) or E2 (visually estimated) for video data
- **Coding confidence** (low / medium / high)
- **source_type** (`video_observed` or `video_estimated`)
- **data_use** (`structured_coding` or `qualitative_only`; no rows promoted to `modelling_ready` at Stage 1)

---

## 2.X Duplicate and parallel source control

Parallel uploads of the same workflow or product demo were flagged to avoid inflated independent sample counts:

| Group ID | Primary | Parallel (excluded from independent counts) |
|----------|---------|-----------------------------------------------|
| `DUP-MIVAN-SLAB-7DAY` | M01 | M05 |
| `DUP-BMR-NP320-COATING` | R07 | R13 |

The `independent_sample` flag in observation CSVs determines inclusion in summary statistics. Paper sample counts should use **primary rows only**.

---

## 2.X Cleaned modelling subset

Representative rows were merged into `cleaned_video_dataset.csv` for framework demonstration. At Stage 1 approval:

| Category | Independent-sample rows |
|----------|-------------------------|
| Mivan workflow | 12 |
| Robot operations | 7 (6 BrightMaster + 1 Bright Dream) |
| Fresh-concrete leveling robots | 3 (R02, R09 BrightMaster; R22 Bright Dream) |

All cleaned rows have `usable_for_productivity=no` and `duration_validity=invalid`.

---

## 2.X Manufacturer specifications (E3)

Product-page and brochure values for selected BrightMaster references (sources T01–T04) were stored in `manufacturer_specs.csv` with `source_type=manufacturer_reported` and evidence level **E3**. These records support specification-range context for the framework but are **not** treated as independently verified field performance.

---

## 2.X Quality assurance and reproducibility

Stage 1 quality controls were implemented following the fifteen-prompt value-addition plan in [`cursor_prompts_construction_robot_value_addition.md`](../cursor_prompts_construction_robot_value_addition.md) (execution log: `reports/prompts_execution_status.md`):

1. Repository audit and data dictionary  
2. Activity taxonomy and robot-agnostic metadata fields  
3. Suitability scoring and duration-validity rules  
4. Duplicate controls and automated validation (`src/validate_extractions.py`)  
5. Data quality reporting (`src/generate_data_quality_report.py`)  
6. CSV templates and human coding checklist (`docs/video_coding_checklist.md`)  
7. Unit tests for validation logic (`tests/test_validation_logic.py`)

Validation enforces schema completeness, evidence-level constraints (no E3 in video observation tables), productivity blocking on invalid durations, and duplicate-flag consistency. Reports are regenerated from the same scripts to keep documentation aligned with CSV snapshots.

Manual segment boundaries for narrated documentaries remain coder-dependent; reproducibility is supported by documented rubrics and checklists, not by fully automated timestamp detection.

---

## 2.X GAN-ready seed conversion (Stage 2)

Approved cleaned observations were converted into a normalized seed feature table (`gan_seed_dataset.csv`) following [`gan_seed_conversion_algorithm.md`](gan_seed_conversion_algorithm.md).

### Promotion criteria

Rows entered the seed set only if they had `independent_sample=yes`, were not duplicate/parallel sources, used `structured_coding` (excluding `qualitative_only`), had medium or high coding confidence, evidence E1/E2, and `usable_for_productivity=no`.

### Encoding

Categorical fields were mapped to integer `*_enc` columns using `config/seed_encoding_schema.yaml` (workflow stage, congestion, access, surface type, manufacturer, etc.). Activity labels were normalized to taxonomy `activity_group` values.

### Seed dataset composition

| Metric | Count |
|--------|-------|
| Seed records | 14 |
| Mivan seeds | 7 |
| Robot seeds | 7 (6 BrightMaster + 1 Bright Dream) |
| Excluded cleaned rows | 3 (non-independent duplicates) |

Every seed record carries `duration_excluded=yes` and `usable_for_productivity=no`. **No GAN training or synthetic records were generated in this stage.**

### Reproducibility

```bash
python scripts/complete_stage2.py
```

---

## 2.X Generative augmentation design (Stage 3)

A hybrid augmentation architecture was designed given **n = 14** independent seeds ([`generative_augmentation_design.md`](generative_augmentation_design.md)).

### Strategy

| Phase | Method | Status |
|-------|--------|--------|
| 3A | Constraint-guided rule expansion → 50 pilot scenarios | **Complete** (Phase 3.1) |
| 3B | Tabular GAN/VAE pilot (CTGAN/TVAE) | **Complete** — 50 GAN scenarios from n=14 training set |
| 3C | Deployment Readiness Index (DRI) | **Complete** — framework + demonstration scoring |

### Modelling feature vector

`modelling_feature_matrix.csv` exports 17 columns (13 categorical encodings + 2 counts + lineage IDs) from seeds. Duration and productivity fields are **excluded** from generative targets.

### Scenario families

Four families: Mivan slab-cycle (`SF-MIVAN-SLAB-CYCLE`), fresh-concrete robots (`SF-ROBOT-FRESH-CONCRETE`), post-cast robots (`SF-ROBOT-POST-CAST`), and joint deployment pairs (`SF-DEPLOYMENT-JOINT`).

### Constraint validation

Synthetic rows (future) must pass the same construction-logic rules as seeds (`validate_scenario_constraints.py`), including activity–workflow coherence and fresh- vs post-cast surface alignment.

**No synthetic records or GAN training were performed at the design stage. Phase 3.1 rule expansion produced 50 synthetic scenarios — see [`phase3_1_signoff.md`](phase3_1_signoff.md).**

### Phase 3.1 results

| Metric | Value |
|--------|-------|
| Synthetic scenarios | 50 |
| Generation method | `rule_expanded` |
| Constraint violation rate | 0% |
| Families | Mivan slab-cycle (16), fresh-concrete robot (16), post-cast robot (8), joint deployment (10) |

All synthetic rows: `is_synthetic=yes`; no duration/productivity fields.

---

## 2.X Deployment Readiness Index (Phase 3C)

A five-dimension weighted composite ranks robot and joint-deployment scenarios — see [`deployment_readiness_index_design.md`](deployment_readiness_index_design.md).

| Dimension | Weight |
|-----------|--------|
| Work-zone access | 0.25 |
| Workflow fit | 0.25 |
| Human–robot coexistence | 0.20 |
| Surface–task alignment | 0.20 |
| Evidence confidence | 0.10 |

Mivan-only rows receive **Site Context Index (SCI)** only. Output: `dri_scored_scenarios.csv` (64 records). All scores carry `score_provenance=framework_derived_scenario_relative`.

**Not field-validated** — scenario-relative ranking for framework demonstration only.

---

## 2.X Limitations (Methods-relevant)

1. **Secondary data only** — Public videos and manufacturer pages; no controlled site measurement.  
2. **No productivity claims** — Segment durations are not valid productivity times; excluded from seed features.  
3. **Manufacturer imbalance** — Robot observations are mostly BrightMaster; one Bright Dream comparator (R22).  
4. **Edited and promotional footage** — Especially robot demos and long Mivan tutorials with voiceover.  
5. **Small seed sample** — 14 seeds; suitable for framework demonstration, not population inference.  
6. **Generative augmentation** — Phase 3.1 complete (50 rule-expanded scenarios); tabular GAN pilot deferred.  
7. **DRI scoring** — Phase 3C framework complete; scores are scenario-relative, **not field-validated**.

---

## Suggested figure / table placeholders for the paper

- **Table 1:** Suitability rubric (seven criteria × 0–2)  
- **Table 2:** Evidence-level and source-type definitions (E1–E3)  
- **Table 3:** Approved sample composition + seed record counts (14 seeds)  
- **Table 4:** Seed encoding schema summary (`*_enc` columns)  
- **Figure 1:** Ten-step extraction workflow (from `video_informed_task_level_data_extraction_algorithm.md`)  
- **Figure 2:** Slab-cycle workflow stages mapped to Mivan activity taxonomy  
- **Figure 3:** Stage 1 → Stage 2 → Stage 3 augmentation pipeline  
- **Figure 4:** Scenario family diagram (Mivan / robot / joint)

---

## Repository reference (Data availability statement draft)

> …Approvals are recorded in `docs/stage1_signoff.md` and `docs/stage2_signoff.md`. Stage 3 generative augmentation design is in `docs/generative_augmentation_design.md`.
