# Reviewer Notes

Concise research-safe logic for the `construction_robot` repository (Journal of Building Engineering context).

---

## 1. Why public videos are used

Construction robot deployment in Mivan/aluminium formwork high-rise sites is difficult to observe at scale through controlled field studies alone. Publicly available videos and manufacturer pages provide accessible, repeatable secondary sources for **visible task parameters**, workflow staging, and congestion/access patterns — suitable for **framework development**, not productivity proof.

## 2. Secondary observational data

All video-coded values are **E1/E2** evidence: directly or estimated from footage. They reflect what is visible in promotional, edited, or tutorial content — not instrumented site measurement.

## 3. Manufacturer claims are separated

Manufacturer specifications (`manufacturer_specs.csv`) are **E3** and stored with explicit `claim_type`, `claim_use`, and `used_in_model=no`. Productivity, manpower reduction, and flatness claims are **not verified** and are excluded from generative model inputs.

## 4. Robot-agnostic framework

BrightMaster is one source among several. The schema supports multiple manufacturers (`robot_source_candidates.csv`, R22 Bright Dream comparator). Current robot observations are BrightMaster-heavy — acknowledged as a **sample limitation**, not a design constraint.

## 5. Synthetic data are pilot-only

Rule-expanded and GAN/TVAE scenarios are marked `pilot_only=yes` and `not_for_statistical_inference=yes`. They stress-test constraint logic and DRI scoring on n=14 seeds — not substitute for observed data.

## 6. Field validation remains future work

Scenario-relative DRI scores demonstrate framework logic. Independent site validation is required before any quantitative deployment-readiness or productivity claims.

## 7. Contribution to Journal of Building Engineering

The repository offers:

- A reproducible **video-informed extraction pipeline** for construction robotics in formwork contexts
- **Construction-logic constraint validation** for scenario data
- A **Deployment Readiness Index** demonstration with weight sensitivity analysis
- Transparent **provenance and limitation** documentation for reviewer scrutiny

---

## Safe claim (use in paper and README)

> The repository presents a video-informed and robot-agnostic methodological framework for converting publicly available construction robotics and aluminium formwork construction videos into structured secondary observational data. The resulting dataset supports framework development, pilot scenario generation, and scenario-relative readiness assessment. It does not constitute direct field-measured productivity evidence or field validation of construction robot performance.
