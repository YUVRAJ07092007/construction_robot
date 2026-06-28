# Stage 1 Sign-Off Record

**Status:** Approved  
**Approved by:** Project lead (human review)  
**Approval date:** 2026-06-27  
**Readiness label:** `framework_ready`

---

## Sign-off statement

Stage 1 video-informed data extraction is **approved** for use in framework development and the Journal of Building Engineering methods paper. The coded datasets, validation pipeline, and research-safe framing are accepted under the limits below.

Stage 2 (GAN seed conversion) **complete** — see [`stage2_signoff.md`](stage2_signoff.md).

---

## Spot-check basis (2026-06-27)

Three high-value rows in `data/cleaned_video_dataset.csv` were video-verified:

| observation_id | Video | Activity | Result |
|----------------|-------|----------|--------|
| OBS-M02-005 | M02 (19:23–22:51) | Formwork erection | Pass — chapter-aligned Mivan panel erection |
| OBS-M02-010 | M02 (38:22–41:47) | Concrete pour | Pass — “Concrete of MIVAN Slab” chapter and pour content |
| OBS-R22-001 | R22 (full 55 s) | Bright Dream leveling | Pass — wet-slab screeding robot; comparison source |

---

## Accepted research limits (binding for paper)

1. **Secondary observational data only** — no productivity or cycle-time claims from public video timing.
2. **BrightMaster-heavy robot sample + one Bright Dream comparison (R22)** — not manufacturer-generalisable without further sources.
3. **Duplicate controls** — do not double-count M01/M05 (`DUP-MIVAN-SLAB-7DAY`) or R07/R13 (`DUP-BMR-NP320-COATING`); use primary rows only in sample counts.

---

## Approved dataset snapshot

| File | Rows | Notes |
|------|------|-------|
| `video_metadata.csv` | 32 | 16 structured-extraction videos |
| `video_segments.csv` | 46 | All `duration_validity=invalid` |
| `robot_video_observations.csv` | 11 | 10 BrightMaster + 1 Bright Dream |
| `mivan_video_observations.csv` | 30 | Slab-cycle workflow |
| `cleaned_video_dataset.csv` | 17 | Modelling subset; none `framework_seed_ready` |
| `manufacturer_specs.csv` | 10 | E3 only (T01–T04) |

**Independent-sample counts (cleaned subset):** 12 Mivan + 7 robot observations (6 BrightMaster + 1 Bright Dream).

**Validation:** `python src/validate_extractions.py` passing; pytest 13 passed at sign-off.

---

## Repository enhancements completed

Value-addition work was executed per [`cursor_prompts_construction_robot_value_addition.md`](../cursor_prompts_construction_robot_value_addition.md) (15/15 prompts). See [`reports/prompts_execution_status.md`](../reports/prompts_execution_status.md).

Deliverables include: data dictionary, activity taxonomy, validation script, data quality report, coding checklist, CSV templates, robot source candidates, tests, and readiness review.

---

## Next steps (post-approval)

| Priority | Action | Status |
|----------|--------|--------|
| 1 | Draft paper **Methods** section | See [`paper_methods_draft.md`](paper_methods_draft.md) |
| 2 | Optional source expansion | 4 candidates in `robot_source_candidates.csv` (`deferred_post_stage1`) |
| 3 | Stage 2 GAN seed conversion | **Complete** — [`stage2_signoff.md`](stage2_signoff.md) |

---

## Research-safe statement

> This repository supports a video-informed, robot-agnostic data extraction framework for construction robot deployment readiness assessment in aluminium formwork-based high-rise building construction. The extracted data are secondary observational records derived from public videos, manufacturer-reported specifications, and structured coding rules. The dataset is intended for framework development and future scenario modelling, not for claiming verified real-site productivity or field performance.
