# Video Coding Checklist

Operational guide for manual extraction from construction robot and Mivan workflow videos.

**Reminder:** Public videos are secondary observational sources only. Do not treat visible duration as verified productivity.

---

## 1. Decide whether a video is usable

- [ ] Confirm construction relevance (robot operation or Mivan/aluminium formwork slab cycle)
- [ ] Check manufacturer/source attribution (`manufacturer_verified`: yes / no / unknown)
- [ ] Note platform stability (YouTube/manufacturer page preferred over social clips)
- [ ] If promotional montage only → qualitative_only or exclude

---

## 2. Assign suitability score (0–14)

Score each criterion 0–2:

| Criterion | Field |
|-----------|-------|
| Construction relevance | score_relevance |
| Visual clarity | score_visual_clarity |
| Activity continuity | score_activity_continuity |
| Activity identifiability | score_activity_identifiability |
| Interaction visibility | score_interaction_visibility |
| Low editing level | score_editing_level |
| Parameter extractability | score_parameter_measurability |

**Bands:** 0–5 exclude · 6–9 qualitative_only · 10–14 structured_extraction

Set `data_use` accordingly. Use `manual_data_use_override` + `override_reason` only when justified.

---

## 3. Segment the video

- Minimum segment: **8 s** (5 s only for unambiguous robot pass on leveling/finishing/grinding)
- Record `start_time`, `end_time`, `visible_segment_duration_sec`
- Reject sub-threshold clips with `reason_for_rejection`
- Mark edited/montage segments `duration_validity=invalid`

---

## 4. Count visible labour (Mivan)

- Record `labour_count_visible`, min/max range when partially occluded
- Note congestion and `access_condition` (open / partially_restricted / congested)
- Do not infer off-screen workers without marking confidence lower

---

## 5. Classify robot activity

Use taxonomy in `config/activity_taxonomy.yaml`:

- Fresh concrete: `fresh_concrete_leveling`, `fresh_concrete_finishing`
- Post-cast: `post_cast_floor_grinding`, `post_cast_coating`, `post_cast_surface_preparation`
- Do **not** label hardened-surface coating as fresh concrete finishing

---

## 6. Classify Mivan activity

Map to: `rebar_work`, `formwork_work`, `mep_conduit_work`, `concrete_pouring`, etc.

Set `floor_cycle_stage`: pre-pour / pour / post-cast

---

## 7. Assign evidence level

| Level | When to use |
|-------|-------------|
| E1 | Directly visible in video |
| E2 | Visually estimated |
| E3 | Manufacturer page only (specs CSV) |

Video observations: E1 or E2 only.

---

## 8. Assign confidence level

- **high** — clear visibility, minimal ambiguity
- **medium** — usable with conservative interpretation
- **low** — qualitative context only; do not mark modelling_ready

---

## 9. Mark duration validity

| Condition | duration_validity | usable_for_productivity |
|-----------|-------------------|-------------------------|
| Edited / montage / promo | invalid | no |
| Continuous unedited clip | valid_for_visible_segment_only | no |
| Independently verified field time | rare; document in notes | only if verified |

Always add `duration_validity_reason`.

---

## 10. Mark duplicate / parallel videos

- Same workflow, different upload → shared `duplicate_group_id`
- Only one `independent_sample=yes` per group
- Keep all rows; document in `parallel_source_note`

---

## After coding

```bash
python src/validate_extractions.py
python src/generate_data_quality_report.py
```

Review `reports/validation_report.md` before adding rows to `cleaned_video_dataset.csv`.
