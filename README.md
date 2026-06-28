# Construction Robot — Video-Informed Data Extraction Pipeline

Structured observational coding pipeline for research on **construction robot deployment readiness** in **Mivan / aluminium formwork** high-rise building construction.

Public videos and manufacturer pages are used as **secondary observational sources** — not as field-measured productivity data. Outputs support framework development, scenario modelling, and (planned) GAN-ready seed dataset creation.

**Target paper context:** *Video-Informed and GAN-Augmented Framework for Assessing Construction Robot Deployment Readiness in Aluminium Formwork-Based High-Rise Building Construction* (Journal of Building Engineering).

---

## What this repository contains

| Area | Description |
|------|-------------|
| **Algorithm** | 10-step video-informed task-level extraction method |
| **Source review** | Curated BrightMaster robot + Mivan workflow video links |
| **CSV datasets** | Registry, segments, robot/Mivan observations, cleaned merge |
| **E3 specs** | Manufacturer-reported technical parameters (separate from video coding) |
| **Validation** | Python checks for schema and construction logic rules |

---

## Repository structure

```
construction_robot/
├── README.md
├── video_informed_task_level_data_extraction_algorithm.md   # Full extraction algorithm
├── brightmaster_mivan_video_links_suitability_review.md     # Source links & suitability notes
├── config/
│   └── extraction_config.py                                 # Rubric, thresholds, field names
├── data/
│   ├── video_metadata.csv                                   # Source registry + suitability scores
│   ├── video_segments.csv                                   # Usable activity segments
│   ├── robot_video_observations.csv                         # Robot-side coded parameters
│   ├── mivan_video_observations.csv                         # Mivan-side coded parameters
│   ├── cleaned_video_dataset.csv                            # Merged modelling subset
│   ├── manufacturer_specs.csv                               # E3 manufacturer-reported specs
│   ├── templates/                                           # Empty CSV headers
│   └── cache/                                               # Descriptions, transcripts (working files)
├── scripts/
│   ├── init_templates.py                                    # Create CSV templates
│   ├── seed_video_registry.py                               # Seed priority source list
│   └── batch_update_pipeline.py                             # Batch registry/observation updates
└── src/
    └── validate_extractions.py                              # Schema + logic validation
```

---

## Pipeline overview

### Stage 1 — Video extraction (in progress ~55%)

1. **Registry** — Record each video/source with metadata  
2. **Screen** — Score suitability 0–14 (7 criteria × 0–2)  
3. **Segment** — Split into usable activity clips  
4. **Extract** — Code robot-side and Mivan-side parameters  
5. **Evidence** — Label E1–E5; use mainly E1/E2 for video stage  
6. **Validate** — Apply construction logic rules  
7. **Export** — Five CSV outputs + cleaned merge  

**Suitability bands**

| Score | Band | Use |
|-------|------|-----|
| 0–5 | Exclude | Do not code |
| 6–9 | Qualitative only | Workflow understanding |
| 10–14 | Structured extraction | Full parameter coding |

### Stage 2 — GAN seed conversion (planned)

Convert cleaned video-derived data into normalised seed records for synthetic scenario generation. Not yet implemented.

---

## Current dataset status

| File | Rows (approx.) | Notes |
|------|----------------|-------|
| `video_metadata.csv` | 17 sources | 8 fully coded, 2 pools, 1 pending, 1 excluded |
| `video_segments.csv` | 38 | M01, M02, M03, M05, R02, R05–R07 |
| `robot_video_observations.csv` | 4 | BrightMaster robot demos |
| `mivan_video_observations.csv` | 29 | Slab-cycle workflow coding |
| `cleaned_video_dataset.csv` | 12 | Key rows for modelling |
| `manufacturer_specs.csv` | 10 | T01–T04 E3 reference values |

**Core coded videos:** M01, M02, M03, M05 (Mivan) · R02, R05, R06, R07 (BrightMaster robot)

---

## Quick start

Requires **Python 3.10+**. No pip dependencies for core scripts.

```bash
# Initialise empty CSV templates
python scripts/init_templates.py

# Seed priority video registry
python scripts/seed_video_registry.py

# Validate datasets after manual coding
python src/validate_extractions.py
```

Optional: install `yt-dlp` for metadata/subtitle download during source screening.

```bash
pip install yt-dlp
```

---

## Coding workflow

1. Add or update a row in `data/video_metadata.csv` (score all seven `score_*` columns; total max 14).  
2. Set `suitability_band`: `exclude` / `qualitative_only` / `structured_extraction`.  
3. For videos scoring **10+**, add segments to `video_segments.csv`.  
4. Code robot or Mivan observations in the matching CSV.  
5. Add representative rows to `cleaned_video_dataset.csv`.  
6. Run `python src/validate_extractions.py`.  

**Rules (summary)**

- Minimum segment length: **8 s** (5 s only for unambiguous robot passes)  
- Standard access field: `access_condition`  
- Manufacturer pages → `manufacturer_specs.csv` with **E3** only — do not mix into video observations  
- Mark promotional/time-lapsed segments: `duration_validity = invalid`  

Full rubric: `config/extraction_config.py`  
Full algorithm: `video_informed_task_level_data_extraction_algorithm.md`

---

## Evidence levels

| Level | Meaning |
|-------|---------|
| E1 | Directly visible from video |
| E2 | Visually estimated from video |
| E3 | Manufacturer-reported specification |
| E4 | Computed from extracted data |
| E5 | Assumption-based |

Video extraction stage uses mainly **E1** and **E2**.

---

## Research-safe description

Use wording like this in the paper:

> The selected videos were used to extract observable task-level parameters and workflow characteristics. Manufacturer pages were used only to define technical specification ranges. The video-derived dataset was not treated as direct field-measured productivity data, but as a structured secondary observational dataset for framework development and synthetic scenario generation.

---

## Key documentation

- [Video extraction algorithm](video_informed_task_level_data_extraction_algorithm.md)
- [Video & source suitability review](brightmaster_mivan_video_links_suitability_review.md)

---

## License

Research and educational use. Video sources remain subject to their original platform terms and uploader rights. Manufacturer specifications are cited as **manufacturer-reported (E3)** and are not independently verified field data.
