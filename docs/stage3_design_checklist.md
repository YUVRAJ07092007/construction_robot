# Stage 3 Design Checklist — Generative Augmentation

Use before implementing Phase 3A (rule-based scenario expansion) or Phase 3B (tabular GAN pilot).

---

## Design artifacts (Phase 3.0)

- [x] Architecture document — [`generative_augmentation_design.md`](generative_augmentation_design.md)
- [x] Machine-readable config — [`config/generative_augmentation_config.yaml`](../config/generative_augmentation_config.yaml)
- [x] Modelling feature matrix builder — `src/build_modelling_feature_matrix.py`
- [x] Scenario constraint validator — `src/validate_scenario_constraints.py`
- [x] Synthetic output template — `data/templates/synthetic_scenario_dataset_template.csv`
- [x] Feature matrix exported — `data/modelling_feature_matrix.csv`

---

## Approval gates before Phase 3.1 (implementation)

- [ ] Human review of hybrid strategy (rule-first, GAN-deferred given n=14)
- [ ] Confirm scenario families SF-MIVAN / SF-ROBOT / SF-JOINT are sufficient for paper
- [ ] Confirm no duration/productivity fields in generative targets
- [ ] Confirm E3 specs remain separate from generative training

---

## Phase 3.1 implementation checklist

- [x] Implement `src/expand_scenarios.py` (rule-based expander)
- [x] Generate `data/synthetic_scenario_dataset.csv` (50 rows)
- [x] Run constraint validation; violation rate 0%
- [ ] Human spot-check ≥ 5 synthetic scenarios per family (recommended)
- [x] Sign-off record — [`phase3_1_signoff.md`](phase3_1_signoff.md)

---

## Phase 3B checklist (deferred)

- [ ] Seed count ≥ 30 OR Phase 3A validation passed
- [ ] Select tabular model (CTGAN / TVAE)
- [ ] Post-filter all synthetic rows through constraint validator
- [ ] Compare marginals to seed distribution (report only)

---

## Phase 3C checklist

- [x] DRI framework config and design doc
- [x] `src/compute_dri_scores.py` demonstration scoring
- [x] `data/dri_scored_scenarios.csv` (64 records)
- [x] Sign-off — [`phase3c_signoff.md`](phase3c_signoff.md)
- [ ] Expert weight calibration (future)
- [ ] Independent field validation (required for quantitative claims)

---

## Research-safe reminders

- All synthetic rows: `is_synthetic=yes`
- No productivity or cycle-time generation
- Bright Dream comparison stratum preserved in fresh-concrete family
- Duplicate video groups never re-introduced via synthesis

---

## Run design baseline

```bash
python scripts/complete_stage3_design.py
```
