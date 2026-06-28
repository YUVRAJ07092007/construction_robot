# Deployment Readiness Index (DRI) — Framework Design (Phase 3C)

**Status:** Framework design complete · demonstration scoring implemented  
**Date:** 2026-06-28  
**Config:** [`config/dri_framework_config.yaml`](../config/dri_framework_config.yaml)

> **Critical limitation:** DRI scores are **scenario-relative framework outputs** derived from secondary video-coded features. They are **not** field-validated deployment performance measures.

---

## 1. Purpose

The Deployment Readiness Index (DRI) provides a **structured composite score** for ranking construction robot deployment scenarios in **Mivan / aluminium formwork high-rise** contexts.

DRI supports:

- Comparing robot and joint-deployment scenarios within the seed + synthetic corpus  
- Stress-testing how access, workflow, and coexistence features affect relative readiness  
- Paper Methods demonstration of the GAN-augmented assessment **framework**

DRI does **not** predict real-site productivity, cycle-time savings, or manufacturer-generalisable performance.

---

## 2. Scoring scope

| Record type | Full DRI | SCI only |
|-------------|----------|----------|
| Robot seeds (`robot_seed`) | Yes | No |
| Robot synthetics | Yes | No |
| Joint synthetics (`SF-DEPLOYMENT-JOINT`) | Yes | No |
| Mivan-only seeds/synthetics | No | Yes (Site Context Index) |

**Site Context Index (SCI):** Mivan-only rows receive a partial score (access + workflow fit) to characterise worksite conditions without implying robot deployment readiness.

---

## 3. DRI dimensions and weights

| Dimension | Weight | Inputs | Interpretation (higher = more ready) |
|-----------|--------|--------|-------------------------------------|
| Work-zone access | 0.25 | congestion, access | Lower congestion + more open access |
| Workflow fit | 0.25 | activity, workflow stage | Taxonomy-aligned stage pairing |
| Human–robot coexistence | 0.20 | labour, robot operators | Supported ops; moderate labour density |
| Surface–task alignment | 0.20 | activity, surface | Wet vs hardened surface rules |
| Evidence confidence | 0.10 | E1/E2, coding confidence | Stronger video provenance |

Weights sum to **1.0**. Each sub-score is normalised to **0–100**.

---

## 4. Composite formula

```
DRI_total = Σ (dimension_score × weight)
```

Bands (scenario-relative):

| Band | Score range |
|------|-------------|
| low | 0–39 |
| medium | 40–69 |
| high | 70–100 |

**Ranking:** `dri_rank` assigned within all `dri_applicable=yes` records (seeds + synthetics), descending by `dri_total_score`.

---

## 5. Explicit exclusions

- Video segment duration / productivity timing  
- E3 manufacturer efficiency claims (`manufacturer_specs.csv`)  
- Absolute field-calibrated thresholds  
- BrightMaster-specific generalisation without further validation  

---

## 6. Outputs

| File | Description |
|------|-------------|
| `data/dri_scored_scenarios.csv` | 64 rows (14 seeds + 50 synthetic) |
| `reports/dri_scoring_report.md` | Band distribution and top ranks |
| `score_provenance` | Always `framework_derived_scenario_relative` |

---

## 7. Implementation

```bash
python scripts/complete_stage3c.py
```

| Script | Role |
|--------|------|
| `src/compute_dri_scores.py` | Compute sub-scores and composite |
| `src/validate_dri_scores.py` | Range and ranking checks |
| `scripts/complete_stage3c.py` | Pipeline runner |

---

## 8. Research-safe statement (for paper)

> Deployment Readiness Index scores were computed as a weighted composite of video-derived scenario features for framework demonstration. Scores enable scenario-relative ranking within the coded and synthetically expanded dataset; they do not represent independently validated field deployment performance.

---

## 9. Future work

| Item | Status |
|------|--------|
| Expert weight calibration | Not done |
| Independent site validation | Required before quantitative claims |
| Phase 3B tabular GAN + DRI on larger corpus | **Pilot complete** (n=14); weight sensitivity in `dri_weight_sensitivity_report.md` |
| Joint scenario DRI modifier using paired SCI | Optional enhancement |

---

## 10. Related documents

- [`generative_augmentation_design.md`](generative_augmentation_design.md) — Phase 3A/3B context  
- [`phase3_1_signoff.md`](phase3_1_signoff.md) — Synthetic scenario input  
- [`phase3c_signoff.md`](phase3c_signoff.md) — Phase 3C completion record
