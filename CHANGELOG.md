# Changelog

All notable changes to the construction_robot repository.

## [0.4.2] - 2026-06-28

### Added
- Final reviewer prompt file and `scripts/complete_final_improvements.py`
- `data/duplicate_group_summary.csv` for authoritative duplicate-group control
- Context-aware `concrete_finishing` validation
- `robot_task_family` on robot source candidates; expanded non-BrightMaster candidates

### Changed
- Duplicate validation uses group summary (eliminates false suggestions)
- Manufacturer specs require all claim-control columns; `application_context` claim type
- `paper_methods_draft.md` Phase 3 wording made internally consistent

## [0.4.1] - 2026-06-28

### Added
- `scripts/apply_reviewer_schema_v2.py` — duration validity + pilot CSV aliases
- `scripts/complete_reviewer_improvements.py` — idempotent reviewer pipeline
- Pilot synthetic filename aliases (`pilot_*_synthetic_scenarios.csv`)
- `visible_duration_validity` on segments and observations
- `parallel_source_note` on robot/cleaned datasets

### Changed
- Updated journal reviewer guide (re-upload sync)
- DRI design doc: Phase 3B marked pilot complete

## [0.4.0] - 2026-06-28

### Added
- Journal reviewer improvement package (`docs/cursor_repo_improvement_prompts_for_journal_reviewers.md`)
- Repository status matrix, reviewer notes, data/README.md
- DRI weight sensitivity analysis (`src/dri_weight_sensitivity.py`)
- File formatting checker (`scripts/check_file_formatting.py`)
- CITATION.cff and LICENSE (MIT)
- Manufacturer claim controls on `manufacturer_specs.csv`
- Synthetic pilot metadata fields on scenario CSVs
- Structured `validation_issues.csv` output

### Changed
- Renamed `modelling_ready` → `framework_seed_ready` across codebase
- Activity taxonomy: context-aware `concrete_finishing` mapping
- Enhanced robot source candidates screening columns
- README and reports aligned for reviewer-safe wording

## [0.3.0] - 2026-06-28

### Added
- Phase 3B tabular GAN/VAE pilot (50 scenarios)
- Phase 3C Deployment Readiness Index framework
- Phase 3.1 rule-based scenario expansion (50 scenarios)
- Stage 2 GAN-ready seed conversion (14 seeds)

## [0.2.0] - 2026-06-27

### Added
- Stage 1 human sign-off and validation pipeline
- Value-addition schema improvements (taxonomy, duplicates, duration validity)

## [0.1.0] - 2026-06

### Added
- Initial video-informed extraction pipeline and CSV datasets
