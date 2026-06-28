# Reviewer Readiness Report

**Generated:** 2026-06-28 (v2 pass)  
**Label:** **`reviewer_ready_with_limitations`**

Improvements applied per [`docs/cursor_repo_improvement_prompts_for_journal_reviewers.md`](../docs/cursor_repo_improvement_prompts_for_journal_reviewers.md) (re-upload synced).

---

## Checklist

| # | Question | Status | Notes |
|---|----------|--------|-------|
| 1 | Repository status internally consistent? | **Yes** | [`repository_status_matrix.md`](../docs/repository_status_matrix.md) reconciles README, reports, methods |
| 2 | Data files readable and formatted? | **Yes** | 93 files scanned; 0 formatting issues |
| 3 | Videos as secondary observational data? | **Yes** | Stated in README, reviewer notes, data/README |
| 4 | Manufacturer claims separated? | **Yes** | claim_type/claim_use/used_in_model on specs; validation enforced |
| 5 | Robot-agnostic? | **Partial** | Schema + candidates yes; sample BrightMaster-heavy (documented) |
| 6 | Duplicate/parallel sources controlled? | **Yes** | Flags + validation on all observation tables |
| 7 | Durations safely handled? | **Yes** | usable_for_productivity=yes count = 0 |
| 8 | Activity taxonomy clear? | **Yes** | Fresh vs post-cast; context-aware concrete_finishing |
| 9 | Synthetic outputs pilot-only? | **Yes** | pilot_only, not_for_statistical_inference on all synthetic rows |
| 10 | DRI scenario-relative + sensitivity? | **Yes** | 4 schemes tested; 51 weight-sensitive records documented |
| 11 | Validation report clean? | **Yes** | 0 critical errors |
| 12 | Suitable for methodology demonstration? | **Yes** | End-to-end pipeline reproducible |
| 13 | Future work? | See below | Field validation; robot diversity; techno-economic |

---

## Validation summary

- Critical errors: **0**
- Tests: **42 passed**
- Synthetic pilot rows patched: **200** (50 rule + 50 GAN + 100 combined)

---

## Limitations (for reviewers)

1. n=14 seed sample — pilot only  
2. BrightMaster majority in robot observations  
3. GAN/TVAE trained on small sample — not for statistical inference  
4. DRI rankings weight-sensitive (51/73 applicable records shift ≥5 ranks across schemes)  
5. No independent field validation  

---

## Future work

- Independent site validation  
- Additional comparison robot coding (Floor Master, Kajima, etc.)  
- Expert weight calibration for DRI  
- Techno-economic assessment module  

---

## Key new artifacts

| File | Purpose |
|------|---------|
| `docs/repository_status_matrix.md` | Stage status single source of truth |
| `docs/reviewer_notes.md` | Academic reviewer guide |
| `data/README.md` | Per-file CSV guide |
| `src/dri_weight_sensitivity.py` | DRI weight robustness |
| `scripts/complete_reviewer_improvements.py` | Idempotent reviewer pipeline |
| `scripts/apply_reviewer_schema_v2.py` | Duration + pilot filename aliases |
| `data/pilot_*_synthetic_scenarios.csv` | Reviewer-friendly synthetic aliases |
| `scripts/check_file_formatting.py` | Formatting QA |
| `CITATION.cff`, `LICENSE`, `CHANGELOG.md` | Citation and versioning |
