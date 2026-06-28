# Tabular GAN/VAE Pilot Report (Phase 3B)

**Generated:** 2026-06-28 by `src/generate_tabular_gan_pilot.py`

- Model used: **TVAE**
- Training rows: 14 (modelling_feature_matrix.csv)
- Candidate pool sampled: 400
- Valid after constraint filter: 179
- Rejected: 221
- Exported GAN scenarios: 50 (target 50)

## Scenario families (GAN export)

- SF-DEPLOYMENT-JOINT: 10
- SF-MIVAN-SLAB-CYCLE: 18
- SF-ROBOT-FRESH-CONCRETE: 14
- SF-ROBOT-POST-CAST: 8

## Outputs

- `data/synthetic_scenario_dataset_gan.csv`
- `data/synthetic_scenario_dataset_all.csv` (50 rule + 50 GAN)

## Research-safe note

Pilot trained on n=14 seeds. Outputs are post-filtered synthetic scenarios, not field-validated performance data.
