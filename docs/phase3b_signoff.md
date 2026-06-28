# Phase 3B Sign-Off — Tabular GAN/VAE Pilot

**Status:** Complete (pilot generation + validation)  
**Completion date:** 2026-06-28

---

## Deliverables

| Item | Location |
|------|----------|
| Pilot config | `config/tabular_gan_pilot_config.yaml` |
| Dependencies | `requirements-gan-pilot.txt` |
| Generator | `src/generate_tabular_gan_pilot.py` |
| Pipeline | `scripts/complete_stage3b.py` |
| **GAN output** | **`data/synthetic_scenario_dataset_gan.csv`** (50 rows) |
| **Combined output** | **`data/synthetic_scenario_dataset_all.csv`** (100 rows) |
| Report | `reports/tabular_gan_pilot_report.md` |

---

## Pilot summary

| Metric | Value |
|--------|-------|
| Training set | 14 rows (`modelling_feature_matrix.csv`) |
| Model | TVAE (CTGAN primary; TVAE fallback on small-sample fit) |
| Candidate pool | 400 sampled |
| Valid after constraint filter | 179 |
| Exported GAN scenarios | 50 |
| Constraint errors | 0 |
| Soft warnings (surface–activity) | 6 (12% of GAN export) |

### GAN scenario families

| Family | Count |
|--------|------:|
| SF-MIVAN-SLAB-CYCLE | 18 |
| SF-ROBOT-FRESH-CONCRETE | 14 |
| SF-DEPLOYMENT-JOINT | 10 |
| SF-ROBOT-POST-CAST | 8 |

---

## Extended DRI scoring

With `--all-synthetic`, DRI scoring includes seeds + rule synthetics + GAN synthetics:

| Metric | Value |
|--------|-------|
| Total records | 114 (14 + 50 + 50) |
| Full DRI applicable | 73 |

Default scoring (Phase 3C baseline) remains 64 records without the flag.

---

## Research-safe limits (binding)

- n=14 training set — **pilot only**, not production GAN augmentation
- Post-filtered by construction logic constraints; soft warnings retained for review
- No productivity or duration fields in generative targets
- Outputs are scenario-relative synthetic data, **not field-validated**

---

## Approval

Phase 3B pilot suitable for methods section as a **small-sample tabular generative augmentation demonstration**, alongside Phase 3.1 rule expansion.
