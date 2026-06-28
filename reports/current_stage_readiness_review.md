# Current Stage Readiness Review

**Date:** 2026-06-28  
**Reviewer:** Automated post-Stage-1 + value-addition review  
**Extraction status:** Ongoing — Stage 1 coded datasets complete; human review pending

---

## Review questions

### 1. Is the current dataset logical?

**Yes, with caveats.** Activity taxonomy separates fresh-concrete and post-cast tasks. Mivan slab-cycle stages align with workflow_stage. Robot demos are classified by surface type and activity group. Duplicate parallel uploads are flagged.

### 2. Is the extraction reproducible?

**Mostly yes.** Suitability rubric, data dictionary, coding checklist, and validation scripts provide reproducible rules. Manual segment boundaries remain coder-dependent for narrated documentaries.

### 3. Are the variables suitable for framework development?

**Yes.** Variables cover access_condition, congestion, robot movement, labour counts, evidence levels, and manufacturer-reported spec ranges — sufficient for deployment-readiness **framework** demonstration.

### 4. Are manufacturer claims properly separated?

**Yes.** E3 specs isolated in `manufacturer_specs.csv`. Video tables restricted to E1/E2. Validation blocks manufacturer source types in observation CSVs.

### 5. Are durations safely handled?

**Yes.** Segments marked invalid or visible-only; `usable_for_productivity=no` enforced. No productivity claims from public video timing.

### 6. Are duplicate sources controlled?

**Yes.** M01/M05 and R07/R13 groups documented with independent_sample flags.

### 7. Is the repo robot-agnostic?

**Partially.** Schema and candidate registry support any manufacturer. Current coded sample is BrightMaster-heavy. R03 excluded as unverified comparison.

### 8. Is the dataset suitable for a methodology demonstration?

**Yes.** Sufficient robot + Mivan coded observations, registry metadata, and validation pipeline for a methods section demonstration.

### 9. Is it ready for GAN-ready seed dataset preparation?

**Not yet.** Stage 2 is explicitly deferred. Seed conversion requires Stage 1 human review sign-off and broader robot-source balance.

### 10. What is still missing?

- Multi-manufacturer robot video coding (comparison robots)
- Normalization of legacy source_type hyphen/underscore values
- Additional independent fresh-concrete leveling observations
- Human review sign-off on coding quality
- Promotion path to modelling_ready (conservative; not yet applied)

---

## Readiness label

**`framework_ready`**

The repository supports framework development and structured secondary observational analysis. It is **not** seed_dataset_ready or final quantitative validation ready. Extraction remains open for robot-agnostic expansion.

---

## Research-safe statement

> This repository supports a video-informed, robot-agnostic data extraction framework for construction robot deployment readiness assessment in aluminium formwork-based high-rise building construction. The extracted data are secondary observational records derived from public videos, manufacturer-reported specifications, and structured coding rules. The dataset is intended for framework development and future scenario modelling, not for claiming verified real-site productivity or field performance.
