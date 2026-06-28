"""DRI weight sensitivity analysis across alternative weighting schemes."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML required") from exc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.compute_dri_scores import (  # noqa: E402
    compute_all,
    read_csv,
    record_type_from_seed,
    record_type_from_synthetic,
    score_record,
    feature_row_from_seed,
    load_yaml,
    SEED_PATH,
    SYNTH_PATH,
    GAN_SYNTH_PATH,
    CONFIG_PATH,
)

REPORTS = ROOT / "reports"
OUT_CSV = REPORTS / "dri_weight_sensitivity_results.csv"
OUT_MD = REPORTS / "dri_weight_sensitivity_report.md"

SCHEMES = {
    "equal_weights": {
        "work_zone_access": 0.20,
        "workflow_fit": 0.20,
        "human_robot_coexistence": 0.20,
        "surface_task_alignment": 0.20,
        "evidence_confidence": 0.20,
    },
    "safety_heavy": {
        "work_zone_access": 0.35,
        "workflow_fit": 0.15,
        "human_robot_coexistence": 0.25,
        "surface_task_alignment": 0.15,
        "evidence_confidence": 0.10,
    },
    "workflow_heavy": {
        "work_zone_access": 0.15,
        "workflow_fit": 0.35,
        "human_robot_coexistence": 0.15,
        "surface_task_alignment": 0.25,
        "evidence_confidence": 0.10,
    },
    "evidence_heavy": {
        "work_zone_access": 0.15,
        "workflow_fit": 0.15,
        "human_robot_coexistence": 0.15,
        "surface_task_alignment": 0.15,
        "evidence_confidence": 0.40,
    },
}


def load_applicable_records(use_gan: bool = True) -> list[tuple[str, dict, bool, bool, str]]:
    records: list[tuple[str, dict, bool, bool, str]] = []
    for seed in read_csv(SEED_PATH):
        features = feature_row_from_seed(seed)
        rtype, _, dri_ok, sci = record_type_from_seed(seed)
        if dri_ok:
            records.append((seed["seed_id"], features, dri_ok, sci, rtype))
    synth_paths = [SYNTH_PATH]
    if use_gan and GAN_SYNTH_PATH.exists():
        synth_paths.append(GAN_SYNTH_PATH)
    for path in synth_paths:
        for syn in read_csv(path):
            features = {k: syn.get(k, "") for k in [
                "video_category_enc", "activity_group_enc", "workflow_stage_enc",
                "operating_surface_enc", "congestion_level_enc", "access_condition_enc",
                "evidence_level_enc", "coding_confidence_enc",
                "labour_count_visible", "robot_operator_count",
            ]}
            rtype, _, dri_ok, sci = record_type_from_synthetic(syn)
            if dri_ok:
                records.append((syn["scenario_id"], features, dri_ok, sci, rtype))
    return records


def score_with_scheme(records, dri_config: dict, weights: dict[str, float], scheme: str) -> dict[str, int]:
    cfg = dict(dri_config)
    dims = dict(cfg["dimensions"])
    for key, w in weights.items():
        dims[key] = dict(dims[key])
        dims[key]["weight"] = w
    cfg["dimensions"] = dims
    scores: dict[str, int] = {}
    for rid, features, dri_ok, sci, _rtype in records:
        row = score_record(
            features,
            dri_applicable=dri_ok,
            sci_only=sci,
            dri_config=cfg,
            scoring_date=date.today().isoformat(),
            record_id=rid,
            record_type="sensitivity",
            source_table="sensitivity",
            scenario_family="",
        )
        if row.get("dri_total_score"):
            scores[rid] = int(row["dri_total_score"])
    return scores


def rank_map(scores: dict[str, int]) -> dict[str, int]:
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return {rid: rank for rank, (rid, _) in enumerate(ordered, start=1)}


def main() -> int:
    dri_config = load_yaml(CONFIG_PATH)
    records = load_applicable_records(use_gan=True)
    if not records:
        print("No DRI-applicable records found.")
        return 1

    scheme_scores: dict[str, dict[str, int]] = {}
    scheme_ranks: dict[str, dict[str, int]] = {}
    for name, weights in SCHEMES.items():
        scheme_scores[name] = score_with_scheme(records, dri_config, weights, name)
        scheme_ranks[name] = rank_map(scheme_scores[name])

    baseline = scheme_ranks["equal_weights"]
    sensitive: list[str] = []
    for rid in baseline:
        ranks = [scheme_ranks[s].get(rid, 999) for s in SCHEMES]
        if max(ranks) - min(ranks) >= 5:
            sensitive.append(rid)

    top_stable = []
    for rid, rank in sorted(baseline.items(), key=lambda x: x[1])[:5]:
        ranks = [scheme_ranks[s][rid] for s in SCHEMES]
        top_stable.append((rid, rank, min(ranks), max(ranks)))

    REPORTS.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["scheme", "record_id", "dri_total_score", "rank", "rank_range"],
        )
        writer.writeheader()
        for scheme in SCHEMES:
            for rid, score in scheme_scores[scheme].items():
                ranks = [scheme_ranks[s].get(rid, 0) for s in SCHEMES]
                writer.writerow({
                    "scheme": scheme,
                    "record_id": rid,
                    "dri_total_score": score,
                    "rank": scheme_ranks[scheme][rid],
                    "rank_range": max(ranks) - min(ranks),
                })

    lines = [
        "# DRI Weight Sensitivity Report",
        "",
        f"**Generated:** {date.today().isoformat()} by `src/dri_weight_sensitivity.py`",
        "",
        "> Scenario-relative sensitivity analysis only. **Not field-validated.**",
        "",
        "## Schemes tested",
        "",
    ]
    for name in SCHEMES:
        lines.append(f"- {name}")
    lines.extend([
        "",
        f"## Records analysed (DRI-applicable): {len(records)}",
        "",
        "## Do rankings change under different weights?",
        "",
        f"- Weight-sensitive records (rank shift ≥5): **{len(sensitive)}**",
        "",
        "## Top 5 under equal weights (rank stability)",
        "",
        "| record_id | equal rank | min rank | max rank |",
        "|-----------|------------|----------|----------|",
    ])
    for rid, eq, mn, mx in top_stable:
        lines.append(f"| {rid} | {eq} | {mn} | {mx} |")
    lines.extend([
        "",
        "## Limitation statement",
        "",
        "DRI scores remain framework-derived and scenario-relative. Sensitivity analysis "
        "shows ranking stability under alternative weight assumptions; it does not validate "
        "field deployment readiness.",
        "",
        "## Outputs",
        "",
        f"- `{OUT_CSV}`",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    compute_all(use_all_synthetic=False)
    print(f"Sensitivity analysis complete: {len(sensitive)} weight-sensitive records.")
    print(f"Report: {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
